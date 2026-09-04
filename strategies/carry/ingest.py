"""Pull every source once, log raw responses, append deduped rows. Idempotent: safe to run any number of times."""
from __future__ import annotations

import csv
import io
import json
import math
import time
from datetime import datetime, timedelta

from harness import http, rawlog
from harness.clock import hour_bucket, iso, now
from strategies.carry import tables as T

CDE_PRODUCTS_URL = "https://api.coinbase.com/api/v3/brokerage/market/products?product_type=FUTURE"
SPOT_URL = "https://api.exchange.coinbase.com/products/{product}/ticker"
CBOE_URL = "https://www.cboe.com/us/futures/cryptocurrency/continuous-futures/funding-rate-data/csv/previous-trading-date/"
TREASURY_URL = ("https://home.treasury.gov/resource-center/data-chart-center/interest-rates/daily-treasury-rates.csv/"
                "{year}/all?type=daily_treasury_bill_rates&field_tdr_date_value={year}&page&_format=csv")
YAHOO_URL = "https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?range=10d&interval=1d"
BROWSER_UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"}

MONTH_CODES = "FGHJKMNQUVXZ"


def _f(x) -> str:
    """Normalize numeric strings; empty for missing."""
    if x is None or x == "":
        return ""
    try:
        v = float(x)
    except (TypeError, ValueError):
        return ""
    return "" if math.isnan(v) else repr(v) if v != int(v) else str(int(v))


def ingest_cde(at: datetime) -> dict:
    r = http.get(CDE_PRODUCTS_URL)
    data = json.loads(r.body)
    cde = [p for p in data.get("products", []) if p.get("product_id", "").endswith("-CDE")]
    rawlog.write(T.STRATEGY, "cde_products", cde, at)
    funding, dated = [], []
    for p in cde:
        fd = p.get("future_product_details") or {}
        pid = p["product_id"]
        common = dict(price=_f(p.get("price")), mid=_f(p.get("mid_market_price")),
                      settlement_price=_f(fd.get("settlement_price")), open_interest=_f(fd.get("open_interest")),
                      volume_24h=_f(p.get("volume_24h")), fetched_at=iso(at))
        if fd.get("funding_interval") and fd.get("funding_time"):
            funding.append(dict(funding_time=fd["funding_time"], product_id=pid, funding_rate=_f(fd.get("funding_rate")),
                                index_price=_f(fd.get("index_price")), **common))
        elif pid.split("-")[0] in T.DATED_ROOTS:
            dated.append(dict(hour_time=hour_bucket(at), product_id=pid, contract_expiry=fd.get("contract_expiry", ""), **common))
    return {"funding": T.FUNDING.append(funding), "dated": T.DATED.append(dated), "products_seen": len(cde)}


def ingest_spot(at: datetime) -> dict:
    rows = []
    for prod in T.SPOT_PRODUCTS:
        r = http.get(SPOT_URL.format(product=prod))
        rawlog.write(T.STRATEGY, f"spot_{prod}", r.body, at)
        d = json.loads(r.body)
        rows.append(dict(hour_time=hour_bucket(at), product=prod, price=_f(d.get("price")), bid=_f(d.get("bid")),
                         ask=_f(d.get("ask")), trade_time=d.get("time", ""), fetched_at=iso(at)))
    return {"spot": T.SPOT.append(rows)}


def _thin_cboe(rows: list[dict]) -> list[dict]:
    """Keep the first sample of each hour and the final print of each trading date, per root."""
    keep, last_hour, last_by_root_date = [], {}, {}
    for r in rows:
        root, hour = r["futures_root"], r["sample_time"][:13]
        if last_hour.get(root) != hour:
            keep.append(r)
            last_hour[root] = hour
        last_by_root_date[(root, r["trading_date"])] = r
    seen = {(r["futures_root"], r["sample_time"]) for r in keep}
    keep += [r for r in last_by_root_date.values() if (r["futures_root"], r["sample_time"]) not in seen]
    return keep


def ingest_cboe(at: datetime) -> dict:
    r = http.get(CBOE_URL, headers=BROWSER_UA)
    rawlog.write(T.STRATEGY, "cboe_funding", r.body, at)
    rows = list(csv.DictReader(io.StringIO(r.text())))
    out = [dict(sample_time=x["sample_time"], futures_root=x["futures_root"], trading_date=x["trading_date"],
                spot_price=_f(x["spot_price"]), futures_price=_f(x["futures_price"]), sample_basis=_f(x["sample_basis"]),
                funding_rate=_f(x["funding_rate"]), clamped_funding_rate=_f(x["clamped_funding_rate"]), fetched_at=iso(at))
           for x in _thin_cboe(rows)]
    return {"cboe": T.CBOE.append(out)}


def ingest_treasury(at: datetime) -> dict:
    r = http.get(TREASURY_URL.format(year=at.year), headers=BROWSER_UA)
    rawlog.write(T.STRATEGY, "treasury_bills", r.body, at)
    out = []
    for x in csv.DictReader(io.StringIO(r.text())):
        d = datetime.strptime(x["Date"], "%m/%d/%Y").strftime("%Y-%m-%d")
        ce = {k.split()[0]: v for k, v in x.items() if k.endswith("COUPON EQUIVALENT")}
        out.append(dict(date=d, wk4=_f(ce.get("4")), wk8=_f(ce.get("8")), wk13=_f(ce.get("13")), wk26=_f(ce.get("26")),
                        wk52=_f(ce.get("52")), fetched_at=iso(at)))
    return {"treasury": T.TREASURY.append(out)}


def cme_symbols(at: datetime, months_ahead: int = 3) -> list[str]:
    """Front continuous plus the next monthly contracts. CME BTC lists monthly; expiry is the last Friday."""
    syms = ["BTC=F"]
    y, m = at.year, at.month
    for _ in range(months_ahead):
        syms.append(f"BTC{MONTH_CODES[m - 1]}{y % 100:02d}.CME")
        m += 1
        if m > 12:
            m, y = 1, y + 1
    return syms


def ingest_cme(at: datetime) -> dict:
    out, errors = [], []
    for i, sym in enumerate(cme_symbols(at)):
        if i:
            time.sleep(1.5)  # Yahoo rate-limits bursts
        try:
            r = http.get(YAHOO_URL.format(symbol=sym), headers=BROWSER_UA, retries=2)
        except Exception as e:  # cross-check source: never fail the run
            errors.append(f"{sym}: {e}")
            continue
        rawlog.write(T.STRATEGY, f"yahoo_{sym.replace('=', '_')}", r.body, at)
        try:
            res = json.loads(r.body)["chart"]["result"][0]
            closes = res["indicators"]["quote"][0]["close"]
            for ts, c in zip(res["timestamp"], closes):
                if c is None:
                    continue
                d = datetime.fromtimestamp(ts, tz=at.tzinfo).strftime("%Y-%m-%d")
                out.append(dict(date=d, symbol=sym, close=_f(c), fetched_at=iso(at)))
        except (KeyError, IndexError, TypeError) as e:
            errors.append(f"{sym}: parse {e}")
    return {"cme": T.CME.append(out), "cme_errors": errors}


CRITICAL = ("cde", "spot")   # failures here fail the run; the rest are best-effort backfill sources


def run(at: datetime | None = None) -> dict:
    at = at or now()
    summary: dict = {"at": iso(at)}
    errors = []
    for name, fn in (("cde", ingest_cde), ("spot", ingest_spot), ("cboe", ingest_cboe),
                     ("treasury", ingest_treasury), ("cme", ingest_cme)):
        try:
            summary.update(fn(at))
        except Exception as e:
            errors.append(f"{name}: {type(e).__name__}: {e}")
            if name in CRITICAL:
                summary["errors"] = errors
                raise RuntimeError(json.dumps(summary)) from e
    summary["errors"] = errors
    return summary

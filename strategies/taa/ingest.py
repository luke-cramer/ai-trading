"""Daily closes, dividends and splits for the ETF universe. Tiingo (official, free key) when TIINGO_TOKEN is set,
else the Yahoo Finance chart API (unofficial; blocks GitHub runner IPs, so only useful from a laptop)."""
from __future__ import annotations

import json
import os
import time
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from harness import http, rawlog
from harness.clock import iso, now
from strategies.taa import tables as T

TIINGO_URL = "https://api.tiingo.com/tiingo/daily/{symbol}/prices?startDate={start}&format=json"
YAHOO_URL = "https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?period1={p1}&period2=9999999999&interval=1d&events=div,splits"
BROWSER_UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"}
NY = ZoneInfo("America/New_York")
RECENT_DAYS = 120          # incremental pull window; backfills any gap shorter than this
CLOSE_FINAL_HOUR = 16.5    # 16:30 NY: a bar dated today is only stored after the close


def _ny_date(ts: int) -> str:
    return datetime.fromtimestamp(ts, NY).strftime("%Y-%m-%d")


def parse_chart(body: bytes, at: datetime, symbol: str) -> tuple[list[dict], list[dict]]:
    """Rows for PRICES and EVENTS. Bars for today's NY date are dropped until the session has closed."""
    res = json.loads(body)["chart"]["result"][0]
    ny_now = at.astimezone(NY)
    today = ny_now.strftime("%Y-%m-%d")
    closed = ny_now.hour + ny_now.minute / 60 >= CLOSE_FINAL_HOUR
    q = res["indicators"]["quote"][0]
    prices = []
    for ts, c, v in zip(res["timestamp"], q["close"], q.get("volume") or [None] * len(res["timestamp"])):
        d = _ny_date(ts)
        if c is None or (d == today and not closed) or d > today:
            continue
        prices.append(dict(date=d, symbol=symbol, close=f"{c:.6f}", volume="" if v is None else str(int(v)), fetched_at=iso(at)))
    events = []
    ev = res.get("events") or {}
    for e in (ev.get("dividends") or {}).values():
        events.append(dict(date=_ny_date(e["date"]), symbol=symbol, kind="dividend", value=f"{float(e['amount']):.6f}", fetched_at=iso(at)))
    for e in (ev.get("splits") or {}).values():
        events.append(dict(date=_ny_date(e["date"]), symbol=symbol, kind="split", value=f"{float(e['numerator']) / float(e['denominator']):.6f}",
                           fetched_at=iso(at)))
    return prices, events


def parse_tiingo(body: bytes, at: datetime, symbol: str) -> tuple[list[dict], list[dict]]:
    """Tiingo daily rows carry the unadjusted close plus divCash / splitFactor on the ex-date."""
    ny_now = at.astimezone(NY)
    today = ny_now.strftime("%Y-%m-%d")
    closed = ny_now.hour + ny_now.minute / 60 >= CLOSE_FINAL_HOUR
    prices, events = [], []
    for row in json.loads(body):
        d = row["date"][:10]
        if row.get("close") is None or (d == today and not closed) or d > today:
            continue
        v = row.get("volume")
        prices.append(dict(date=d, symbol=symbol, close=f"{float(row['close']):.6f}", volume="" if v is None else str(int(v)), fetched_at=iso(at)))
        if float(row.get("divCash") or 0) > 0:
            events.append(dict(date=d, symbol=symbol, kind="dividend", value=f"{float(row['divCash']):.6f}", fetched_at=iso(at)))
        if float(row.get("splitFactor") or 1) != 1:
            events.append(dict(date=d, symbol=symbol, kind="split", value=f"{float(row['splitFactor']):.6f}", fetched_at=iso(at)))
    return prices, events


def fetch(symbol: str, at: datetime, full: bool) -> tuple[list[dict], list[dict]]:
    token = os.environ.get("TIINGO_TOKEN")
    if token:
        start = "1990-01-01" if full else (at - timedelta(days=RECENT_DAYS)).strftime("%Y-%m-%d")
        r = http.get(TIINGO_URL.format(symbol=symbol, start=start), headers={"Authorization": f"Token {token}"}, retries=3, backoff_s=5.0)
        rawlog.write(T.STRATEGY, f"tiingo_{symbol}", r.body, at)
        return parse_tiingo(r.body, at, symbol)
    p1 = 0 if full else int(at.timestamp()) - RECENT_DAYS * 86400
    r = http.get(YAHOO_URL.format(symbol=symbol, p1=p1), headers=BROWSER_UA, retries=4, backoff_s=5.0)
    rawlog.write(T.STRATEGY, f"yahoo_{symbol}", r.body, at)
    return parse_chart(r.body, at, symbol)


def run(at: datetime | None = None, full: bool = False, symbols: tuple[str, ...] = T.UNIVERSE) -> dict:
    """Pull every symbol; full=True fetches the entire history (first run / repair), else the recent window."""
    at = at or now()
    source = "tiingo" if os.environ.get("TIINGO_TOKEN") else "yahoo"
    summary = {"at": iso(at), "source": source, "prices": 0, "events": 0, "splits": [], "errors": []}
    for i, sym in enumerate(symbols):
        if i:
            time.sleep((10.0 if full else 1.5) if source == "yahoo" else 0.5)  # Yahoo rate-limits bursts
        try:
            prices, events = fetch(sym, at, full)
        except Exception as e:
            summary["errors"].append(f"{sym}: {type(e).__name__}: {e}")
            continue
        summary["prices"] += T.PRICES.append(prices)
        new_events = T.EVENTS.append(events)
        summary["events"] += new_events
        if new_events and any(e["kind"] == "split" for e in events):
            summary["splits"].append(sym)
    if len(summary["errors"]) == len(symbols):
        raise RuntimeError(json.dumps(summary))
    return summary

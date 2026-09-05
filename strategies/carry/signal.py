"""Daily carry spread from the logged tables. Pure functions; replayable over any date range.

Definitions (fixed in PREREG.md — do not tune):
  funding_apr   = mean(hourly funding_rate over the UTC day) * 24 * 365
  basis_apr     = mean over hours of ln(F / S) / T, F = BIT front-month mid, S = BIP index price, T = years to expiry
  spread_gross  = funding_apr - basis_apr          (what a short-perp / long-dated book earns before costs)
  spread_net    = spread_gross - cost drag (costs.drag_apr at the day's mean index price)
Front month = nearest BIT expiry with at least MIN_DAYS_TO_EXPIRY days left at that hour.
"""
from __future__ import annotations

import math
from datetime import datetime, timezone

import numpy as np
import pandas as pd

from harness.clock import iso, now
from strategies.carry import costs
from strategies.carry import tables as T

MIN_DAYS_TO_EXPIRY = 7
HOURS_PER_YEAR = 24 * 365


def _num(s: pd.Series) -> pd.Series:
    return pd.to_numeric(s, errors="coerce")


def _ts(s: pd.Series) -> pd.Series:
    return pd.to_datetime(s, utc=True, errors="coerce")


def funding_daily(funding: pd.DataFrame, product: str = T.PERP_BTC) -> pd.DataFrame:
    f = funding[funding["product_id"] == product].copy()
    if f.empty:
        return pd.DataFrame(columns=["date", "funding_apr", "hours_observed", "index_mean"])
    f["t"] = _ts(f["funding_time"])
    f["rate"] = _num(f["funding_rate"])
    f["idx"] = _num(f["index_price"])
    f["date"] = f["t"].dt.strftime("%Y-%m-%d")
    g = f.groupby("date").agg(rate=("rate", "mean"), hours_observed=("funding_time", "nunique"), index_mean=("idx", "mean"))
    g["funding_apr"] = g["rate"] * HOURS_PER_YEAR
    return g.reset_index()[["date", "funding_apr", "hours_observed", "index_mean"]]


def front_month(dated_hour: pd.DataFrame, at: pd.Timestamp, root: str = T.DATED_ROOT_BTC) -> pd.Series | None:
    """Row of the nearest-expiry contract with >= MIN_DAYS_TO_EXPIRY days left; None if nothing qualifies."""
    d = dated_hour[dated_hour["product_id"].str.startswith(root + "-")].copy()
    if d.empty:
        return None
    d["exp"] = _ts(d["contract_expiry"])
    d["dte"] = (d["exp"] - at).dt.total_seconds() / 86400
    d = d[d["dte"] >= MIN_DAYS_TO_EXPIRY].sort_values("dte")
    return None if d.empty else d.iloc[0]


def basis_hourly(dated: pd.DataFrame, funding: pd.DataFrame, root: str = T.DATED_ROOT_BTC, perp: str = T.PERP_BTC) -> pd.DataFrame:
    """Per hour: annualized log basis of the front dated future vs the perp's index price (same index, same venue)."""
    idx = funding[funding["product_id"] == perp][["funding_time", "index_price"]].rename(columns={"funding_time": "hour_time"})
    idx["S"] = _num(idx["index_price"])
    d = dated.merge(idx[["hour_time", "S"]], on="hour_time", how="inner")
    rows = []
    for hour, grp in d.groupby("hour_time"):
        at = pd.Timestamp(hour)
        fm = front_month(grp, at, root)
        if fm is None:
            continue
        F = _num(pd.Series([fm["mid"] if fm["mid"] != "" else fm["price"]])).iloc[0]
        S = float(fm["S"])
        if not (F > 0 and S > 0):
            continue
        rows.append(dict(hour_time=hour, product_id=fm["product_id"], days_to_expiry=fm["dte"],
                         basis_apr=math.log(F / S) / (fm["dte"] / 365.0), F=F, S=S))
    return pd.DataFrame(rows, columns=["hour_time", "product_id", "days_to_expiry", "basis_apr", "F", "S"])


def basis_daily(bh: pd.DataFrame) -> pd.DataFrame:
    if bh.empty:
        return pd.DataFrame(columns=["date", "front_product", "front_days_to_expiry", "basis_apr", "basis_hours"])
    bh = bh.copy()
    bh["date"] = _ts(bh["hour_time"]).dt.strftime("%Y-%m-%d")
    g = bh.groupby("date").agg(front_product=("product_id", "last"), front_days_to_expiry=("days_to_expiry", "mean"),
                               basis_apr=("basis_apr", "mean"), basis_hours=("hour_time", "nunique"))
    return g.reset_index()


def cboe_daily(cboe: pd.DataFrame, root: str = "PBT") -> pd.DataFrame:
    """Cboe publishes a per-day funding rate; the 15:00 final print of each trading date is the one that settles."""
    c = cboe[cboe["futures_root"] == root].copy()
    if c.empty:
        return pd.DataFrame(columns=["date", "cboe_funding_apr"])
    c = c.sort_values("sample_time").groupby("trading_date").last().reset_index()
    c["cboe_funding_apr"] = _num(c["clamped_funding_rate"]) * 365
    return c.rename(columns={"trading_date": "date"})[["date", "cboe_funding_apr"]]


def cme_daily(cme: pd.DataFrame, spot_close: pd.DataFrame) -> pd.DataFrame:
    """Front monthly CME contract close vs our spot close on the same date. Cross-check only."""
    c = cme[cme["symbol"] != "BTC=F"].copy()
    if c.empty or spot_close.empty:
        return pd.DataFrame(columns=["date", "cme_front_symbol", "cme_basis_apr"])
    c["exp"] = c["symbol"].map(_cme_expiry)
    c["close_f"] = _num(c["close"])
    rows = []
    for date, grp in c.groupby("date"):
        at = pd.Timestamp(date, tz="UTC")
        grp = grp.assign(dte=(grp["exp"] - at).dt.total_seconds() / 86400)
        grp = grp[grp["dte"] >= MIN_DAYS_TO_EXPIRY].sort_values("dte")
        s = spot_close.loc[spot_close["date"] == date, "spot_close"]
        if grp.empty or s.empty or not (s.iloc[0] > 0):
            continue
        fm = grp.iloc[0]
        rows.append(dict(date=date, cme_front_symbol=fm["symbol"], cme_basis_apr=math.log(fm["close_f"] / s.iloc[0]) / (fm["dte"] / 365.0)))
    return pd.DataFrame(rows, columns=["date", "cme_front_symbol", "cme_basis_apr"])


def _cme_expiry(symbol: str) -> pd.Timestamp:
    """CME BTC futures expire the last Friday of the contract month (16:00 London); approximate with 15:00 UTC."""
    code, yy = symbol[3], int(symbol[4:6])
    month = "FGHJKMNQUVXZ".index(code) + 1
    year = 2000 + yy
    last = pd.Timestamp(year=year, month=month, day=1, tz="UTC") + pd.offsets.MonthEnd(0)
    back = (last.weekday() - 4) % 7
    return (last - pd.Timedelta(days=back)).replace(hour=15)


def spot_close_daily(spot: pd.DataFrame, product: str = "BTC-USD") -> pd.DataFrame:
    """Spot at 20:00 UTC (16:00 New York, CME daily close) or the latest earlier hour that day."""
    s = spot[spot["product"] == product].copy()
    if s.empty:
        return pd.DataFrame(columns=["date", "spot_close"])
    s["t"] = _ts(s["hour_time"])
    s["date"] = s["t"].dt.strftime("%Y-%m-%d")
    s = s[s["t"].dt.hour <= 20].sort_values("t").groupby("date").last().reset_index()
    s["spot_close"] = _num(s["price"])
    return s[["date", "spot_close"]]


def rf_daily(treasury: pd.DataFrame, dates: pd.Series) -> pd.DataFrame:
    if treasury.empty:
        return pd.DataFrame({"date": dates, "rf_apr": np.nan})
    t = treasury[["date", "wk4"]].copy()
    t["rf_apr"] = _num(t["wk4"]) / 100
    t = t.set_index("date").sort_index()["rf_apr"]
    out = pd.DataFrame({"date": sorted(set(dates))})
    out["rf_apr"] = out["date"].map(lambda d: t[t.index <= d].iloc[-1] if (t.index <= d).any() else np.nan)
    return out


def compute_daily(funding: pd.DataFrame, dated: pd.DataFrame, spot: pd.DataFrame, cboe: pd.DataFrame,
                  treasury: pd.DataFrame, cme: pd.DataFrame, computed_at: datetime | None = None) -> pd.DataFrame:
    computed_at = computed_at or now()
    fd = funding_daily(funding)
    bd = basis_daily(basis_hourly(dated, funding))
    sc = spot_close_daily(spot)
    df = fd.merge(bd, on="date", how="left").merge(cboe_daily(cboe), on="date", how="left")
    df = df.merge(cme_daily(cme, sc), on="date", how="left").merge(sc, on="date", how="left")
    df = df.merge(rf_daily(treasury, df["date"]), on="date", how="left")
    df["spread_gross_apr"] = df["funding_apr"] - df["basis_apr"]
    df["cost_drag_apr"] = df["index_mean"].map(lambda p: costs.drag_apr(p) if p and p > 0 else np.nan)
    df["spread_net_apr"] = df["spread_gross_apr"] - df["cost_drag_apr"]
    df["computed_at"] = iso(computed_at)
    for c in T.DAILY.columns:
        if c not in df.columns:
            df[c] = np.nan
    out = df[T.DAILY.columns].copy()
    for c in out.columns:
        if c not in ("date", "front_product", "cme_front_symbol", "computed_at"):
            out[c] = out[c].map(lambda v: "" if pd.isna(v) else f"{float(v):.8g}")
    return out.fillna("")


# Statistics live in harness.stats; re-exported so PREREG references and tests keep working.
from harness.stats import newey_west_mean, probabilistic_sharpe  # noqa: E402,F401

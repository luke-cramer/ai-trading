"""HAA-Balanced (Keller & Keuning 2023) monthly signal. Pure functions over the stored tables; replayable.

Definitions (fixed in PREREG.md — do not tune):
  total-return price  = close adjusted backward for cash dividends (factor 1 - div / prior close) and splits
  month-end price     = last trading day of each calendar month
  momentum (13612U)   = mean over k in {1,3,6,12} months of P0 / P_k - 1
  risk-on             = momentum(TIP) > 0
  risk-on portfolio   = top-4 offensive by momentum, equal weight; any with momentum <= 0 is replaced by the
                        best defensive asset (IEF or BIL, higher momentum)
  risk-off portfolio  = 100% best defensive asset
Signal is computed at the month-end close; the paper fill happens at the next trading day's close.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from strategies.taa import prereg
from strategies.taa import tables as T


def total_return_prices(prices: pd.DataFrame, events: pd.DataFrame) -> pd.DataFrame:
    """Wide frame (date index × symbol) of total-return-adjusted closes."""
    if prices.empty:
        return pd.DataFrame()
    p = prices.copy()
    p["close"] = pd.to_numeric(p["close"], errors="coerce")
    wide = p.pivot(index="date", columns="symbol", values="close").sort_index()
    ev = events.copy() if not events.empty else pd.DataFrame(columns=T.EVENTS.columns)
    ev["value"] = pd.to_numeric(ev["value"], errors="coerce")
    out = {}
    for sym in wide.columns:
        s = wide[sym].dropna()
        factor = pd.Series(1.0, index=s.index)
        for _, e in ev[ev["symbol"] == sym].iterrows():
            if e["date"] not in s.index:
                continue
            i = s.index.get_loc(e["date"])
            if e["kind"] == "dividend" and i > 0:
                factor.iloc[i] *= 1 - e["value"] / s.iloc[i - 1]
            elif e["kind"] == "split" and i > 0:
                factor.iloc[i] /= e["value"]
        # adjusted[t] = close[t] * prod(factor[u] for u > t): dividends before t leave the latest price untouched
        cum = factor[::-1].cumprod()[::-1].shift(-1).fillna(1.0)
        out[sym] = s * cum
    return pd.DataFrame(out).sort_index()


def month_end(tr: pd.DataFrame) -> pd.DataFrame:
    """Last trading day of each calendar month (only months followed by a later date, i.e. complete months)."""
    if tr.empty:
        return tr
    idx = pd.to_datetime(tr.index)
    ym = idx.strftime("%Y-%m")
    last = pd.Series(range(len(tr)), index=tr.index).groupby(ym).last()
    complete = last.iloc[:-1] if len(last) else last     # the newest month is never known to be complete
    return tr.iloc[complete.values]


def momentum(me: pd.DataFrame, lags=prereg.MOMENTUM_LAGS_MONTHS) -> pd.DataFrame:
    parts = [me / me.shift(k) - 1 for k in lags]
    return sum(parts) / len(lags)


def allocate(mom: pd.Series) -> tuple[dict[str, float], bool]:
    """HAA-Balanced weights for one month-end. Returns (weights, canary_on). NaN momentum = not investable."""
    m = mom.dropna()
    if T.CANARY not in m or not set(T.DEFENSIVE) <= set(m.index):
        return {}, False
    defensive = max(T.DEFENSIVE, key=lambda s: (m[s], s))
    if m[T.CANARY] <= 0:
        return {defensive: 1.0}, False
    off = sorted([s for s in T.OFFENSIVE if s in m], key=lambda s: (-m[s], s))[:prereg.TOP_N]
    w: dict[str, float] = {}
    for s in off:
        pick = s if m[s] > 0 else defensive
        w[pick] = w.get(pick, 0.0) + 1.0 / prereg.TOP_N
    return w, True


def signals(tr: pd.DataFrame) -> pd.DataFrame:
    """Long frame: date, symbol, momentum, weight, canary_on for every complete month-end with a full universe."""
    me = month_end(tr)
    mom = momentum(me)
    rows = []
    for d, row in mom.iterrows():
        w, on = allocate(row)
        if not w:
            continue
        for sym in T.UNIVERSE:
            if sym in row and row[sym] == row[sym]:
                rows.append(dict(date=d, symbol=sym, momentum=float(row[sym]), weight=w.get(sym, 0.0), canary_on=on))
    return pd.DataFrame(rows, columns=["date", "symbol", "momentum", "weight", "canary_on"])

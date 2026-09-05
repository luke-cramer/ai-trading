"""Paper execution: fills at the close of the first trading day after each signal, fractional shares, no leverage."""
from __future__ import annotations

import numpy as np
import pandas as pd

from strategies.taa import costs


def simulate(tr: pd.DataFrame, sig: pd.DataFrame, start_nav: float, start: str, end: str | None = None,
             one_way_bps: float = costs.ONE_WAY_BPS) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Run the rotation from the first signal date >= start. Returns (nav by date, fills)."""
    dates = list(tr.index)
    empty = (pd.DataFrame(columns=["date", "nav", "cash"]),
             pd.DataFrame(columns=["date", "symbol", "weight", "price", "shares", "traded_usd", "cost_usd"]))
    if sig.empty:
        return empty
    sig = sig[sig["date"] >= start]
    if end:
        sig = sig[sig["date"] <= end]
    fills, nav_rows = [], []
    shares: dict[str, float] = {}
    cash = start_nav
    fill_by_date: dict[str, pd.DataFrame] = {}
    for d, grp in sig.groupby("date"):
        later = [x for x in dates if x > d]
        if later:
            fill_by_date[later[0]] = grp
    first_fill = min(fill_by_date) if fill_by_date else None
    if first_fill is None:
        return empty
    for d in dates:
        if d < first_fill or (end and d > end):
            continue
        px = tr.loc[d]
        if d in fill_by_date:
            nav = cash + sum(n * px[s] for s, n in shares.items() if px[s] == px[s])
            targets = {r["symbol"]: r["weight"] for _, r in fill_by_date[d].iterrows() if r["weight"] > 0}
            names = sorted(set(shares) | set(targets))
            for s in names:
                if px.get(s) != px.get(s):
                    raise ValueError(f"no price for {s} on fill date {d}")
            current = {s: shares.get(s, 0.0) * px[s] for s in names}
            est_cost = sum(costs.trade_cost(nav * targets.get(s, 0.0) - current[s], one_way_bps) for s in names)
            nav_net = nav - est_cost           # size targets net of costs so cash never goes negative (no leverage)
            new_shares: dict[str, float] = {}
            for s in names:
                target_usd = nav_net * targets.get(s, 0.0)
                traded = target_usd - current[s]
                if target_usd > 0:
                    new_shares[s] = target_usd / px[s]
                fills.append(dict(date=d, symbol=s, weight=targets.get(s, 0.0), price=float(px[s]), shares=new_shares.get(s, 0.0),
                                  traded_usd=float(traded), cost_usd=float(costs.trade_cost(traded, one_way_bps))))
            cash = nav_net - sum(nav_net * w for w in targets.values())
            shares = new_shares
        nav = cash + sum(n * px[s] for s, n in shares.items())
        nav_rows.append(dict(date=d, nav=float(nav), cash=float(cash)))
    return pd.DataFrame(nav_rows), pd.DataFrame(fills)


def fixed_mix(tr: pd.DataFrame, weights: dict[str, float], start_nav: float, start: str, end: str | None = None,
              one_way_bps: float = costs.ONE_WAY_BPS) -> pd.DataFrame:
    """Benchmark: constant weights rebalanced at the same month-end cadence, same fill rule and costs."""
    me_dates = [d for d in tr.index if d >= start]
    ym = pd.to_datetime(pd.Index(me_dates)).strftime("%Y-%m")
    last_of_month = pd.Series(me_dates).groupby(ym.values).last().tolist()[:-1]
    sig = pd.DataFrame([dict(date=d, symbol=s, weight=w) for d in last_of_month for s, w in weights.items()], columns=["date", "symbol", "weight"])
    nav, _ = simulate(tr, sig, start_nav, start, end, one_way_bps)
    return nav

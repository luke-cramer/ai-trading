"""Trading cost model for monthly ETF rotation in a cash account. Sources and rationale in PREREG.md."""
from __future__ import annotations

COMMISSION_USD = 0.0          # zero-commission ETF trading at every major US broker
ONE_WAY_BPS = 5.0             # half-spread + impact, conservative for these ETFs (quoted spreads 0.4-4 bp)


def trade_cost(traded_usd: float, one_way_bps: float = ONE_WAY_BPS) -> float:
    """Cost of trading `traded_usd` of notional one way (buy or sell)."""
    return abs(traded_usd) * one_way_bps / 1e4 + (COMMISSION_USD if traded_usd else 0.0)

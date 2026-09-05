"""Table schemas for the ETF TAA build. Dates are New York trading dates (YYYY-MM-DD); fetched_at is UTC."""
from __future__ import annotations

from harness.storage import Table

STRATEGY = "taa"

OFFENSIVE = ("SPY", "IWM", "VEA", "VWO", "VNQ", "DBC", "IEF", "TLT")   # HAA-Balanced offensive universe
DEFENSIVE = ("IEF", "BIL")
CANARY = "TIP"
BENCHMARK_6040 = {"SPY": 0.6, "IEF": 0.4}
UNIVERSE = tuple(dict.fromkeys(OFFENSIVE + DEFENSIVE + (CANARY,)))

# Unadjusted daily closes (Yahoo). Never overwritten: total return is rebuilt from EVENTS, not from Yahoo's adj close.
PRICES = Table(STRATEGY, "prices", ["date", "symbol", "close", "volume", "fetched_at"], key=["date", "symbol"], partition="year")

# Cash dividends (per share) and splits (ratio) by ex-date.
EVENTS = Table(STRATEGY, "events", ["date", "symbol", "kind", "value", "fetched_at"], key=["date", "symbol", "kind"], partition="year")

# Derived, replayable: month-end momentum and target weights.
SIGNALS = Table(STRATEGY, "signals", ["date", "symbol", "momentum", "weight", "canary_on", "computed_at"], key=["date", "symbol"], partition="year")

# Derived, replayable: paper fills (first trading day after the signal) and daily NAV.
LEDGER = Table(STRATEGY, "ledger", ["date", "symbol", "weight", "price", "shares", "traded_usd", "cost_usd", "computed_at"],
               key=["date", "symbol"], partition="year")
NAV = Table(STRATEGY, "nav", ["date", "nav", "cash", "bench_6040", "spy", "computed_at"], key=["date"], partition="year")

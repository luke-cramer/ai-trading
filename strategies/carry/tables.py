"""Table schemas for the carry measurement build. All timestamps UTC ISO; dedupe keys listed per table."""
from __future__ import annotations

from harness.storage import Table

STRATEGY = "carry"

# Hourly funding print per CDE perpetual-style future. Keyed on the exchange's own funding_time.
FUNDING = Table(STRATEGY, "funding",
    ["funding_time", "product_id", "funding_rate", "index_price", "settlement_price", "mid", "price",
     "open_interest", "volume_24h", "fetched_at"],
    key=["funding_time", "product_id"])

# Hourly snapshot of the CDE dated futures we care about (BTC/ETH roots). First poll of the hour wins.
DATED = Table(STRATEGY, "dated",
    ["hour_time", "product_id", "contract_expiry", "price", "mid", "settlement_price", "open_interest",
     "volume_24h", "fetched_at"],
    key=["hour_time", "product_id"])

# Coinbase Exchange spot ticker, hourly.
SPOT = Table(STRATEGY, "spot",
    ["hour_time", "product", "price", "bid", "ask", "trade_time", "fetched_at"],
    key=["hour_time", "product"])

# Cboe continuous-futures funding samples: first sample of each hour plus the final daily print.
CBOE = Table(STRATEGY, "cboe",
    ["sample_time", "futures_root", "trading_date", "spot_price", "futures_price", "sample_basis",
     "funding_rate", "clamped_funding_rate", "fetched_at"],
    key=["sample_time", "futures_root"])

# Treasury bill coupon-equivalent yields (percent), one row per business day.
TREASURY = Table(STRATEGY, "treasury",
    ["date", "wk4", "wk8", "wk13", "wk26", "wk52", "fetched_at"],
    key=["date"])

# CME BTC futures daily closes via Yahoo Finance. Cross-check only; unofficial and delayed.
CME = Table(STRATEGY, "cme",
    ["date", "symbol", "close", "fetched_at"],
    key=["date", "symbol"])

# Derived daily series (replayable from the tables above).
DAILY = Table(STRATEGY, "daily",
    ["date", "funding_apr", "hours_observed", "front_product", "front_days_to_expiry", "basis_apr",
     "basis_hours", "spread_gross_apr", "cost_drag_apr", "spread_net_apr", "cboe_funding_apr", "cme_front_symbol",
     "cme_basis_apr", "rf_apr", "spot_close", "computed_at"],
    key=["date"])

DATED_ROOTS = ("BIT", "ET")        # nano BTC / nano ETH dated futures on CDE
PERP_BTC = "BIP-20DEC30-CDE"
DATED_ROOT_BTC = "BIT"
SPOT_PRODUCTS = ("BTC-USD", "ETH-USD")

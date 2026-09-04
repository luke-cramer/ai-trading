"""Cost model for short BIP perp vs long BIT dated future on Coinbase Derivatives. Fully collateralized (1x), no leverage.

Sources (see PREREG.md for the evidence grade of each):
- Exchange fee $0.10/side per nano contract: CDE fee schedule, research/crypto-us-venues.md §1.3.
- All-in round turn ~9-10 bps via IBKR at ~$78k BTC: research/crypto-us-venues.md §2 -> implies ~$0.30/side broker fee.
- Slippage: BIP tick is $5 on ~$81k (0.6 bps); assume one tick per side on the perp, two on the thinner dated leg.
"""
from __future__ import annotations

from dataclasses import dataclass

CONTRACT_BTC = 0.01           # nano contract size (BIP and BIT)
EXCHANGE_FEE_PER_SIDE = 0.10  # USD, CDE schedule
BROKER_FEE_PER_SIDE = 0.30    # USD, assumption backed out of the IBKR ~10 bps round-turn figure
PERP_SLIPPAGE_TICKS = 1
DATED_SLIPPAGE_TICKS = 2
TICK_USD = 5.0


@dataclass(frozen=True)
class RoundTrip:
    fees_usd: float
    slippage_usd: float
    notional_usd: float

    @property
    def bps(self) -> float:
        return (self.fees_usd + self.slippage_usd) / self.notional_usd * 1e4


def round_trip(price: float, slippage_ticks: int) -> RoundTrip:
    """One contract in and out: two sides of fees plus slippage on each side."""
    notional = price * CONTRACT_BTC
    fees = 2 * (EXCHANGE_FEE_PER_SIDE + BROKER_FEE_PER_SIDE)
    slip = 2 * slippage_ticks * TICK_USD * CONTRACT_BTC
    return RoundTrip(fees, slip, notional)


def drag_apr(price: float, perp_hold_days: float = 90.0, dated_roll_days: float = 30.0) -> float:
    """Annualized cost drag as a fraction of one leg's notional.

    The perp leg is entered once per measurement horizon; the dated leg rolls every expiry cycle.
    """
    perp = round_trip(price, PERP_SLIPPAGE_TICKS).bps / 1e4 * (365.0 / perp_hold_days)
    dated = round_trip(price, DATED_SLIPPAGE_TICKS).bps / 1e4 * (365.0 / dated_roll_days)
    return perp + dated

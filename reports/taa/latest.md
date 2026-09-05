# TAA paper report — 2026-09-05 (computed 2026-09-05T01:19:03Z)

Long-only HAA-Balanced rotation, paper only, no leverage. Rules and criteria: `strategies/taa/PREREG.md` v1.

## Latest signal (2026-08-31) — canary RISK-OFF

| symbol | momentum | weight |
|---|---|---|
| BIL | +1.67% | 100% |
| DBC | +20.71% | 0% |
| IWM | +10.39% | 0% |
| VEA | +9.43% | 0% |
| SPY | +9.25% | 0% |
| VWO | +7.25% | 0% |
| VNQ | +2.62% | 0% |
| TIP | -0.40% | 0% |
| IEF | -1.04% | 0% |
| TLT | -2.33% | 0% |

## Forward paper record (from PREREG PAPER_START, $10000 notional)

No fills yet: the first fill is the trading day after the first month-end on or after 2026-09-30.

## Pre-registered criteria

- [ ] forward record: 0/36 months
- [x] drawdown within envelope: n/a
- [x] not underperforming 60/40 without drawdown benefit: n/a
- [x] verdict: not yet — keep paper trading

## Implementation-check backtest (reference only, not a selection step)

- 2008-06-02 → 2026-09-03: CAGR +9.1%, max drawdown -14.6%, vol +11.1%; 60/40 CAGR +8.7%, max drawdown -30.4%
- Monthly excess vs 60/40 +0.0% ± +0.2%, PSR 0.54

Data: 8457 trading days, 10 symbols, newest close 2026-09-03.

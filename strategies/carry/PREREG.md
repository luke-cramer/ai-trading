# Pre-registration — Build #2: onshore crypto carry measurement

**Version 1 · registered 2026-09-04 (UTC) · before the first report was computed.**
Changing anything below after this date requires a "Version 2" section with the reason; the original stays.

## Hypothesis

H1: On Coinbase Derivatives (CDE), the hourly funding rate paid by longs on the nano BTC perpetual-style
future (BIP) exceeds the annualized basis of the same venue's nano BTC dated future (BIT front month) by
at least 2 percentage points per year net of round-trip costs, persistently over 60 days.

Null: the net spread is ≤ 2 pp, or not distinguishable from zero, or positive on fewer than 60% of days.

Prior evidence: a 44-hour sample in phase 1 showed BIP funding ≈ 10.9% APR against a CME curve of
≈ 5.5–5.7% (research/crypto-us-venues.md §1.8, §2.2). That sample is a snapshot, not a distribution.
CDE publishes no funding history, so this measurement cannot be backtested. It is forward-only by construction.

## Universe

- Perp leg: `BIP-20DEC30-CDE` (nano BTC perpetual-style, 0.01 BTC, hourly funding).
- Dated leg: nearest `BIT-*-CDE` expiry with ≥ 7 days to expiry at the observation hour (roll rule fixed here).
- Spot reference: the perp's own `index_price` from the same API response (same index for both legs).
- ETH (`ETP` / `ET`) is logged but is not part of H1. No other symbol is evaluated.

## Data sources (all verified free and reachable from this machine on 2026-09-04)

| Role | Source | Notes |
|---|---|---|
| Primary | `api.coinbase.com/api/v3/brokerage/market/products?product_type=FUTURE` | public, no key; funding_rate, funding_time, index_price, dated prices |
| Spot | `api.exchange.coinbase.com/products/BTC-USD/ticker` | public |
| Cross-check | Cboe continuous-futures funding CSV (previous trading date) | official, daily |
| Cross-check | CME BTC monthly closes via Yahoo Finance chart API | unofficial, delayed; never load-bearing |
| Risk-free | Treasury daily bill rates CSV (4-week coupon equivalent) | official |
| Not used | cmegroup.com | blocks scripts and its terms prohibit automation |

## Definitions (fixed)

- `funding_apr(d)` = mean of the hourly `funding_rate` prints on UTC day d × 24 × 365.
- `basis_apr(d)` = mean over hours of ln(F/S) / T, F = BIT front mid, S = BIP index price, T = years to expiry.
- `spread_gross(d)` = funding_apr − basis_apr. Sign convention: positive means short-perp/long-dated earns.
- `cost_drag` = annualized round-trip cost from `costs.py`: $0.10/side exchange fee [verified, CDE schedule],
  $0.30/side broker fee [assumption, backed out of the ~10 bps IBKR round-turn figure in the corpus],
  1 tick slippage per side on BIP and 2 on BIT [assumption]; perp leg amortized over 90 days, dated leg over
  a 30-day roll. At $80k BTC this is ≈ 2.0% APR, three quarters of it from the monthly dated roll.
- `spread_net(d)` = spread_gross − cost_drag.
- A day is **complete** with ≥ 20 of 24 funding prints. Missing hours are recorded, never interpolated.

## Evaluation (one look, at the decision date)

- Decision window: 60 complete days. If more than 20% of expected hours are missing at day 60, extend to
  90 days before deciding. No intermediate decision. Daily reports are monitoring, not decisions.
- Statistic: mean of `spread_net` over complete days with a Newey-West (Bartlett, 5 lags) standard error;
  fraction of days with `spread_net > 0`; probabilistic Sharpe ratio of the daily series against SR* = 0.
  There is exactly one pre-registered trial, so the deflated Sharpe ratio equals the PSR.
- **GO** (proceed to a *paper* phase 2 design) requires all of: mean net ≥ 2 pp, NW 95% CI lower bound > 0,
  ≥ 60% of days positive.
- **KILL** otherwise: publish the dataset, do not trade, close the build.
- No parameter in this file or in `prereg.py` changes after the first out-of-sample look.

## Capital and leverage

Phase 1 (this build): zero capital, no accounts touched, no orders of any kind.
Any phase 2 must be fully collateralized: notional of each leg ≤ cash posted for it (1x). No leverage, ever.
Phase 2 also requires a tax practitioner's read on §1256 treatment of funding payments before real size
(research/gap-2.md §tax) and separate written approval.

## Known limitations recorded up front

- Funding accrues hourly but cash-settles twice daily; the realized stream depends on the FCM's schedule.
- BIT back months are illiquid (Oct-26 OI 683 on 2026-09-04); the front-month rule keeps us in the liquid contract.
- GitHub Actions cron is best-effort; polling twice per hour with dedupe on `funding_time` tolerates delays
  up to ~50 minutes. Longer outages lose hours permanently (CDE's public history page blocks scripts).

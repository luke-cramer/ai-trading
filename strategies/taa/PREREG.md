# Pre-registration — ETF TAA (HAA-Balanced), build #1

Version 1, drafted 2026-09-05. **Registers (freezes) the moment the implementation-check backtest is first run.**
Any later change is a new version with a dated changelog entry at the bottom, and no forward result computed
under an old version is discarded.

## Hypothesis

A long-only monthly rotation across liquid US-listed ETFs, with a single canary asset deciding risk-on/off
(Keller & Keuning, *Hybrid Asset Allocation*, 2023, SSRN 4346906; "HAA-Balanced"), delivers equity-like
long-run return with materially smaller drawdowns than a 60/40 portfolio. Expected excess CAGR versus 60/40
over a full cycle: −1 to +2 pp/yr. The benefit we are paying for is the drawdown profile, not alpha.
REPORT.md ranks this #1 because it is $0/month, unlevered, and has decades of out-of-sample evidence.

## Universe (fixed)

| Role | Symbols |
|---|---|
| Offensive (8) | SPY, IWM, VEA, VWO, VNQ, DBC, IEF, TLT |
| Defensive (2) | IEF, BIL |
| Canary (1) | TIP |
| Benchmarks | 60/40 = SPY 60% / IEF 40% rebalanced monthly with the same fill rule and costs; SPY buy-and-hold |

## Data

- Daily unadjusted closes, cash dividends and splits from the Yahoo Finance chart API (`v8/finance/chart`,
  unofficial, free, verified live 2026-09-04: SPY daily bars from 1993-01-29 with dividend events).
- Total-return prices are rebuilt by us: on each ex-date, prior closes are multiplied by `1 − dividend / prior close`
  (and divided by the split ratio). Yahoo's own adjusted close is not stored because it changes retroactively.
- A bar dated "today" (New York) is only stored after 16:30 New York. Stored closes are never overwritten.
- Missing days are gaps; nothing is interpolated. Yahoo rate-limits (429) are retried with backoff; a failed day
  is retried the next day from the 120-day window, so the committed history heals itself.

## Signal (fixed)

1. Month-end price = close on the last trading day of each calendar month (a month counts once a later date exists).
2. Momentum (13612U) = mean over k ∈ {1, 3, 6, 12} months of `P0 / Pk − 1` on total-return prices.
3. Risk-on iff momentum(TIP) > 0.
4. Risk-on: hold the top 4 offensive assets by momentum at 25% each; any selected asset with momentum ≤ 0 is
   replaced by the best defensive asset (IEF or BIL, higher momentum). Ties: alphabetical.
5. Risk-off: 100% in the best defensive asset.
6. Fill at the close of the first trading day after the month-end (no same-day look-ahead). Fractional shares,
   fully collateralized, cash earns 0. **No leverage, no shorts, no margin, ever.**

## Costs

- Commission $0 (Fidelity, Schwab, Alpaca, Robinhood all charge $0 for US ETFs; verified on their fee pages
  2026-09-05).
- Spread + impact: 5 bp per side on traded notional. Quoted 30-day median bid-ask spreads for these ETFs are
  roughly 0.4 bp (SPY), 1–2 bp (IWM, VEA, VWO, IEF, TLT, TIP, BIL), 2–4 bp (VNQ, DBC) per issuer pages; the
  round-trip half-spread is therefore ≤ 2 bp and 5 bp leaves room for impact and bad fills at the close.
- Expected turnover ≈ 50–80% of NAV per month in rotation months ⇒ cost drag on the order of 0.3–0.5%/yr.
- Expense ratios are inside the ETF prices already. Taxes are out of scope for paper trading (see Open items).

## Evaluation

**Implementation check (one backtest, reference only).** 2008-01-31 → PAPER_START with $10,000. Expected,
from the published record on proxies and the 2008–2022 ETF era: CAGR 5–10%, max drawdown −10% to −25%, both
better on drawdown than 60/40 (≈ −30% in 2008–09). Result outside that range means a bug or a data problem to
investigate, not a parameter to tune. The rules above are published and are not changed after this run.

**Forward paper record (the evidence).** Starts at the first month-end on or after **2026-09-30**, $10,000
notional. Every month: NAV, drawdown, holdings, and the excess monthly return versus 60/40 with a Newey-West
(3-lag) standard error and the probabilistic Sharpe ratio (one trial ⇒ deflated Sharpe = PSR).

**Kill criteria (checked monthly, any one triggers KILL):**
- Forward drawdown worse than 1.25 × backtest max drawdown, or worse than −30%.
- After 36 months: forward CAGR below 60/40 by more than 3 pp *and* forward max drawdown not better than 60/40's.

**GO (earliest after 36 months of paper):** no kill triggered. GO means "eligible for a phase-2 review", which
needs Luke's written approval in a later session, a tax review, a broker with fractional shares, and remains
1x fully collateralized. Nothing in this document authorizes real money.

## Limitations

- ETF history limits the backtest to 2008 (BIL 2007, VEA 2007, DBC 2006). The 2008 crash and 2022's
  stock/bond drawdown are both inside the window, which is the point.
- Yahoo is unofficial and can throttle or change format; the raw responses are logged so re-parsing is possible.
- Corporate actions other than cash dividends and splits (none expected for these ETFs) are not modelled.
- 36 months of paper cannot statistically confirm a 1–2 pp edge. It can catch implementation errors and
  regime failure; the long-run evidence is the published record, which is why the expected excess is modest.

## Open items (not blockers for paper)

- Tax treatment of monthly rotation in a taxable account versus an IRA before any live decision.
- Broker choice for fractional ETF shares (Fidelity, Schwab, Alpaca all offer them).

## Changelog

- v1 (draft 2026-09-05): initial registration. Registers on first backtest run.

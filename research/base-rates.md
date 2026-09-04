# Part 4 — Who Actually Wins: Base Rates for Retail (and Algorithmic Retail) Traders

**Evidence tags:** `[verified]` = track-recorded, audited, regulatory, or published academic data. `[anon]` = plausible but unverifiable forum/practitioner account. `[promo]` = author sells something; discount heavily.

**Bottom line up front:** across every large-sample dataset that exists, the fraction of retail speculators who earn a *persistent, cost-adjusted* profit is between **0.1% and 3%**, and the fraction who earn a *living* is between **0.5% and 1.1%**. For algorithmic retail specifically, the single best dataset (888 real strategies with honest out-of-sample periods) finds backtest Sharpe explains **2% of the variance** in live Sharpe, with a median degradation of roughly **1.0–1.5 Sharpe points** on going live. Risk metrics transfer out-of-sample almost perfectly (volatility R²=0.67); return metrics do not transfer at all. That asymmetry is the entire game.

---

## 1. Population base rates: the academic core

### 1.1 Taiwan — Barber, Lee, Liu, Odean (2014) `[verified]`

The most complete dataset in existence: **entire-market** transaction data for the Taiwan Stock Exchange, 1992–2006, 3.7 billion two-sided transactions worth ~NT$310 trillion (~US$10 trillion). Not a single broker's book — the whole market, with trader identity.
Source: https://faculty.haas.berkeley.edu/odean/papers/day%20traders/The%20Cross-Section%20of%20Speculator%20Skill.pdf (J. Financial Markets 18 (2014) 1–24)

- ~**450,000** individuals day trade in the average year; day trading is **17% of all TSE volume**, stable across the 15 years.
- ~**277,000** individuals/year day trade more than NT$600,000 (~US$20,000) annually. Of these, **17–20% earn positive abnormal returns net of fees in a given year** — a figure the authors explicitly attribute substantially to luck.
- **~4,000 traders (<1% of the day-trader population)** predictably and reliably earn positive abnormal returns net of costs in the *following* year. This is the real number.
- The spread is enormous: top-500 traders (ranked on prior year) go on to earn **61.3 bps gross / 37.9 bps net per day**; bottom-ranked traders earn **−11.5 / −28.9 bps per day**. A **73 bps/day** gross spread — an order of magnitude larger than comparable skill spreads found in Finland (4.4 bps for high-IQ investors) or US discount-broker data (5 bps).
- Companion work (Barber et al. 2009) puts aggregate Taiwanese individual-investor losses at **>2% of national GDP annually**.

**Read this correctly.** The paper is often cited as "day trading doesn't work." It actually proves the opposite *and* the harder point: skill is real, large, and persistent — and it lives in roughly 1-in-100 to 1-in-900 of the participating population. The top 500 of 450,000 is 0.11%.

### 1.2 Brazil — Chague, De-Losso, Giovannetti (2020) `[verified]`

Regulatory (CVM) records on **19,646 individuals** who began day trading mini-Ibovespa futures 2013–2015, tracked through 2017. This is the cleanest test of the "just persist and you'll learn" hypothesis.
Sources: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3423101 · https://www.tradicted.com/research/chagu-day-2020/

- **50.8%** traded between 2 and 50 days. Only **7.9%** persisted beyond 300 trading days.
- Of the **1,551** who persisted >300 days: **97% lost money** net of fees.
- **1.1% (17 individuals)** earned more than the Brazilian minimum wage.
- **0.5% (8 individuals)** earned more than a bank teller's starting salary.
- The single best performer averaged **US$310/day with a daily standard deviation of US$2,560** — a daily Sharpe of ~0.12 (~1.9 annualized), but note the absolute scale. Profitable traders' daily P&L standard deviations ranged **US$632 to US$3,308**.
- **No learning effect.** Regression coefficient on trade sequence: **−0.019 (SE 0.011)** across 714,637 observations. Experience did not improve performance.

Compounded: ~**0.24%** of starters both persisted *and* earned above minimum wage. Survivorship is doing violent work here — 92% quit before the sample even starts being interesting.

### 1.3 US futures — CFTC Office of the Chief Economist (Ferko, Mixon, Onur, Feb 2024) `[verified]`

Regulatory data on overnight positions and margins: **36,538 retail traders** across **50 futures markets**, Feb 2021 – Nov 2022.
Source: https://www.cftc.gov/sites/default/files/2024-11/Retail_Traders_Futures_V2_new_ada.pdf (OCE Staff Papers 2023-002)

- The **median trader has 4 distinct trading events**, trades 2 markets, holds ~4 days. These are dabblers, not operators.
- Median estimated loss: **$100–$200**.
- **The 60th percentile of the P&L distribution breaks even** → roughly **60% lose money**. The distribution is left-skewed; losses are "measured in thousands of dollars" and exceed gains in aggregate.
- **Larger dollar losses on the first trade are significantly associated with leaving the market permanently.**

The "only 60% lose" figure looks mild versus CFD numbers — because loss rate scales with turnover and exposure. Four trades gives you four coin flips; four thousand gives you the expectation.

### 1.4 CFD/FX — ESMA and broker disclosures `[verified — regulatory]`

- ESMA's national-competent-authority analyses across EU jurisdictions: **74–89% of retail CFD accounts lose money**, with average losses per client of **€1,600 to €29,000**.
  https://www.esma.europa.eu/press-news/esma-news/esma-agrees-prohibit-binary-options-and-restrict-cfds-protect-retail-investors
- The mandated warning format is per-provider: "[X]% of retail CFD accounts lose money." Current disclosed figures run **~68–71%** (CMC Markets UK 68%, IG UK 68%, IG International 71%).
  https://brokerchooser.com/broker-reviews/fxcm-review/cfd-risk-warning

Note the post-2018 improvement (89% → high 60s) tracks ESMA's leverage caps and negative-balance protection, not any improvement in trader skill. **Regulation moved the loss rate ~20 points by capping leverage.** That is a direct, quantified statement about how much of retail loss is leverage rather than selection.

### 1.5 US equities and options `[verified]`

- **Barber & Odean (2000)**, 66,465 households 1991–1996: the most active quintile earned **11.4%/yr vs 17.9% market** — a **6.5 pp annual drag**, almost entirely trading costs.
- **De Silva, So & Smith (2022)** "Losing is Optional": retail lost ~**$3bn** in options, Jan 2010 – Feb 2021.
- **Bryzgalova, Pavlova & Sikorskaya (J. Finance 2023)**: aggregate retail options portfolio lost **$2.1bn** Nov 2019 – Jun 2021. Average retail options gross monthly loss: **1.81%**.
  https://www.advisorperspectives.com/articles/2023/02/19/the-wealth-destroying-behavior-of-retail-option-trading

---

## 2. The algorithmic-specific base rate — the number that matters most

### 2.1 Quantopian: "All That Glitters Is Not Gold" (Wiecki, Campbell, Lent, Stauth, 2016) `[verified]`

This is the only large, honest, retail-algorithm dataset ever published, and it should anchor every expectation in this project.
Sources: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2745220 · PDF: https://community.portfolio123.com/uploads/short-url/3WHpAUOzhCG8QAUez71HpoWnA62.pdf

**Method quality is high.** Platform users had run **800,000+ backtests**. Initial sample 7,152 algorithms → **888** after filtering out single-stock strategies, Sharpe < −1.0, <500 backtest days, clones, and outliers. All backtested 2010–2015 in Zipline on **minute bars with transaction costs, order delays, liquidity constraints, market impact and slippage**. Critically, **algorithm code is versioned in a point-in-time database at creation**, so the in-sample/out-of-sample split cannot be gamed and the logic could not be edited during the ≥6-month OOS period. This is a cleaner IS/OOS separation than most hedge funds achieve internally.

**Headline results:**

| Metric | IS → OOS Pearson R² |
|---|---|
| Sharpe ratio | **0.02** |
| Annual returns | **0.015** — and the correlation is **negative** |
| Information ratio | <0.005 (n.s.) |
| Calmar ratio | <0.005 (n.s.) |
| Financial alpha | <0.005 (n.s.) |
| *Sharpe, IS-year → IS-year (baseline ceiling)* | *0.21* |
| Sharpe using only last backtest year | 0.05 |
| **Annual volatility** | **0.67** |
| **Maximum drawdown** | **0.34** |
| Tail ratio (95th/5th pctile) | 0.025 |

Three things follow, and they are the most actionable findings in this entire report:

1. **A backtest Sharpe explains ~2% of live Sharpe variance** — against a measurable ceiling of 21% (that's the year-to-year Sharpe correlation *within* the backtest). So backtest Sharpe delivers about a tenth of the predictive power that's theoretically available. It is very close to worthless as a selection criterion.
2. **Backtest annual returns are *negatively* correlated with live returns.** Selecting on backtest return is worse than selecting at random.
3. **Risk transfers; return does not.** Volatility R²=0.67 and drawdown R²=0.34 are strong, stable relationships. If your backtest is volatile, your live account will be volatile — that promise is kept. If your backtest is profitable, nothing is promised.

**Direct measurement of overfitting.** The authors computed "Sharpe ratio shortfall" (IS Sharpe − OOS Sharpe) and regressed it on log total backtest days. Result: a weak but **highly significant positive correlation (Spearman R²=0.017, p<0.0001)** — *the more backtesting a quant did, the higher the IS Sharpe, the lower the OOS Sharpe, and the larger the shortfall.* Higher in-sample volatility also predicted greater shortfall (R²=0.02, p<0.0001).

From the paper's Figure 4 scatter distributions: IS Sharpe clusters around **0.75–1.0**; OOS Sharpe clusters around **−0.25 to 0**; the shortfall distribution centers around **+1.0 to +1.5**. In plain terms: **the median Quantopian strategy went from a backtest Sharpe near 1 to a live Sharpe near zero or slightly negative.**

Two constructive findings: hedged/market-neutral strategies had significantly lower volatility both IS (t=5.78) and OOS (t=4.62); and a machine-learning model trained on **57 behavioral features of the backtest process** predicted OOS Sharpe at R²=0.17 — nearly the theoretical ceiling. The *process* by which a strategy was developed carries far more information than the strategy's headline performance.

### 2.2 Quantopian's fate `[verified]`

Shut down November 2020 after 9 years and **200,000+ users**; returned investor capital, left only open-source tools (Zipline, Pyfolio, Alphalens).
https://en.wikipedia.org/wiki/Quantopian · https://www.quantrocket.com/blog/quantopian-shutting-down/

A crowdsourced fund with 200,000 contributors, professional infrastructure, institutional capital and its own published overfitting research still could not assemble a viable portfolio from retail-authored algorithms. Note the second-order problem flagged by practitioners: anyone who *did* find a real edge had every incentive to leave and trade it privately rather than license it `[anon]`.

### 2.3 Edge decay — McLean & Pontiff (J. Finance, 2016) `[verified]`

97 published cross-sectional return predictors:
- Returns are **26% lower out-of-sample** and **58% lower post-publication**.
- ~32 pp of that decay is attributable to publication-informed arbitrage; ~26 pp to data mining in the original研究.
- **Decay is larger for predictors with higher in-sample returns.**
- Surviving returns concentrate in **high-idiosyncratic-risk, low-liquidity stocks** — precisely where retail transaction costs are worst.
https://onlinelibrary.wiley.com/doi/abs/10.1111/jofi.12365

Practitioner anchor: Robert Carver (ex-AHL portfolio manager, publishes his systematic futures research openly) states **"the average trading rule on the typical instrument has a SR of around 0.15."** `[verified — credible practitioner, no product sold on this claim]` https://qoppac.blogspot.com/

### 2.4 Vendor claims that contradict all of the above `[promo]`

Broker/platform blogs assert retail algo traders have a "60% chance of showing positive returns annually," with "the top 10% of automated strategies achieving more than 50% returns annually" (traderspost.io). No sample, no methodology, no OOS discipline, published by a company selling automated-execution software. **This is marketing and contradicts every large-sample dataset.** A survey figure worth more: 58% of retail traders report using AI/algo tools but only **21% report measurable profitability improvement**, and **30% report worse results** (Traders Union) — `[promo]`, but at least directionally consistent with the academic record.

---

## 3. The prop-firm path: pass rates and counterparty risk

**Pass/payout statistics — mostly unsourced, treat with suspicion.** The prop-firm statistics ecosystem is almost entirely SEO content citing each other. Semi-primary figures:
- Earn2Trade: **10.42%** verified pass rate, 2024.
- Take Profit Trader: **20.37%** pass rate, Jan–Aug 2023.
- Apex Trader Funding: 15–20% first-attempt, 40% with resets (**firm claim, unverified**).
- Industry consensus: **5–10%** pass evaluations.
- **"Only ~7% of funded accounts ever receive a payout"** — repeated everywhere, **no traceable primary source**. `[anon]`
- Combined estimates: **1–2% of challenge buyers ever receive a payout**; **1–3%** still withdrawing beyond six months. Average spend on evaluations ~**$4,270** with 60% losing that capital `[anon]`. Average return for those who profit: **4% of allocated funds** `[anon]`.
https://www.quantvps.com/blog/prop-firm-statistics

**Counterparty risk is the bigger story, and it is verified.** `[verified — regulatory/press]`
- **80–100 prop firms shut down in 2024** (Finance Magnates Intelligence). A Brokeree study of 82 firms found only 71 still operating — roughly a **1-in-7 annual closure rate**.
- **My Forex Funds**: closed Aug 2023; CFTC alleged fraud involving **$310m across 135,000+ customers**. The case was **dismissed in May 2025**, with the judge finding the CFTC acted in bad faith and ordering it to pay **$3.1m+** in costs. The firm nonetheless remains permanently closed with customers unresolved — regulatory action itself is a counterparty risk.
- **The Funded Trader**: paused 28 Mar 2024; **80,000+ accounts**; **$2m+ denied payouts** in Jan–Feb 2024 alone.
- **True Forex Funds**: closed 13 May 2024; ~**$1.2m unpaid** to ~300 traders, triggered by MetaQuotes license revocation.
- **SurgeTrader**: closed 24 May 2024 with payouts owed. **FundingTicks**: wound down Jan 2026 after retroactively changing rules to reduce trader profits.
- Estimated **$50m+** in blocked or unrecovered trader funds across closures.
https://thepropfirmguide.com/prop-firms-that-shut-down/ · https://www.financemagnates.com/forex/mff-case-misconduct-embarrassment-for-the-cftc-but-not-yet-a-win-for-prop-trading/

Two structural points: (a) a firm whose revenue is challenge fees is structurally misaligned with paying you; (b) the **MetaQuotes license revocations of Feb 2024** took down multiple firms simultaneously — a single vendor is a systemic chokepoint for the whole sector.

---

## 4. Profile of the minority who sustain profits

**From the Taiwan data (the only rigorous profile that exists) `[verified]`:**
- **Past performance is, "by a large margin," the best predictor of future performance.** Skill is persistent and measurable.
- The **second-best predictor is concentration in a few stocks** — winners specialize rather than diversify their ideas.
- Profitable traders' returns are **higher in hard-to-value stocks (small, volatile) and around earnings announcements**; losers lose in the same places. Winners are forecasting short-horizon prices where information asymmetry is high.
- **It is not liquidity provision.** Nearly two-thirds of profitable traders' trades come from aggressive orders, and order aggressiveness is an economically weak predictor of profitability. The "get paid the spread" story does not explain retail winners.

**From the Quantopian data `[verified]`:** survivors were lower-volatility, more often hedged/market-neutral, and — most tellingly — **had run fewer backtests**. Restraint in the research process was a measurable predictor of live performance.

**Verified individual track record — Kevin Davey `[verified for results, [promo] for teaching]`:** placed 2nd/1st/2nd in the Robbins World Cup Trading Championship (a real-money, broker-verified, year-long contest running since 1984) in 2005/2006/2007 with **+148%, +107%, +112%**. Engineering background, systematic futures. https://kjtradingsystems.com/about.html · https://trading-tournaments.com/tournaments/championships/wctc
**Important caveat:** contest accounts are small and deliberately run at extreme risk to win a ranking. Triple-digit contest returns are not a Sharpe-optimized track record and do not translate to running meaningful capital. Davey now sells books and courses — his *instructional* claims are `[promo]`, his contest placements are third-party verified.

**Synthesized survivor traits (mixed evidence quality):** low-frequency and execution-insensitive enough to run alongside a day job; structural/economic edges (trend, carry, vol risk premium) rather than discovered chart patterns; diversification across *many instruments* while remaining concentrated in *few ideas*; and risk management as the primary discipline — which is exactly what the Quantopian volatility R²=0.67 result would predict, since risk is the only thing you can reliably control out-of-sample. `[anon]` for the framing, `[verified]` for the underlying mechanism.

---

## 5. Blow-up patterns for algorithmic retail specifically

1. **Overfit backtest goes live** — the modal failure by a wide margin. Median Sharpe degradation ~1.0–1.5 points; backtest Sharpe R²=0.02; backtest returns *negatively* predictive; **more backtesting makes it strictly worse**. `[verified — Quantopian]`
2. **Leverage + fat tail.** 15 Jan 2015, the SNB abandoned the EUR/CHF peg: ~**2,000 pips / 20% in minutes**. Stops were not honored; accounts were wiped out and went *negative*. FXCM took a **$225m** client-deficit hit; **Alpari UK filed for bankruptcy**; Excel Markets ceased operations. Brokers split on forgiveness — Oanda and IG forgave deficits; Citi pursued under-collateralized clients for years. `[verified]` EU/UK retail now has negative-balance protection; **US retail futures does not**. https://www.financemagnates.com/terms/s/swiss-national-bank-snb-crisis/
3. **Exchange / counterparty / platform failure.** Prop firm closures above; crypto exchange insolvencies; the MetaQuotes licensing chokepoint. Your capital is at risk from the venue *independent of strategy performance* — an uncorrelated, uninsurable loss channel that no backtest models. `[verified]`
4. **Bug in order logic.** Systematically under-represented in the literature because it produces no publishable dataset, but it is the failure mode most specific to this user's build. Canonical institutional case: Knight Capital, **$440m in ~45 minutes** from a deployment error. Retail analogues: duplicate order submission, unhandled partial fills, reconnect logic re-firing entries, timezone/DST boundary errors, position-state desync between broker and local store after a disconnect. Note that the Quantopian dataset *cannot* capture this class — it was simulated, not live-executed.
5. **Martingale / grid death spiral.** Mathematically guaranteed eventual ruin dressed as a smooth equity curve. Documented pattern: long clean uptrend, then 70%+ drawdown in days. One vendor's forward-tested accounts: EUR/GBP **+590%** while the AUD/USD account on the same system was **almost completely wiped out**. The vendor survivorship mechanic is explicit — developers run many accounts and parameter sets in parallel and publish only the survivors on Myfxbook. `[promo]` sources, but the arithmetic is not in dispute. https://forexrobotlab.com/forextruck-ea-review/
6. **Strategy decay unnoticed.** 58% post-publication decay `[verified]`, and the Brazilian learning coefficient (−0.019) shows traders do not self-correct from experience. Without a pre-committed monitoring and kill discipline, a dead edge is statistically indistinguishable from a normal drawdown in real time — which is precisely the condition under which people add size.

---

## 6. What "success" realistically looks like

**The statistical power problem is the most under-appreciated fact in this entire domain.** To reject Sharpe = 0 at t ≈ 2, you need `t = SR × √years`. So:

| True Sharpe | Years to statistical significance |
|---|---|
| 0.3 | ~44 |
| 0.5 | **16** |
| 1.0 | **4** |
| 2.0 | 1 |

A part-time solo algo trader plausibly operating at **SR 0.3–0.7** cannot know whether they have an edge inside the horizon at which almost everyone quits. In Brazil, 92.1% quit before 300 days — long before any signal could have emerged. This means **the correct success metric for the first 2–3 years is process quality, not P&L.**

**Calibrated expectations for this profile (competent, part-time, solo, systematic):**
- **Target Sharpe 0.3–0.7 net of all costs.** Carver's SR≈0.15 per rule, combined across many rules and instruments, is the honest route to SR ~0.5–1.0; anything advertised above SR 2 on retail-accessible data and infrastructure should be assumed overfit until three years of live data say otherwise.
- On **$25k** at SR 0.5 and 12% vol: roughly **$1,500/yr expected**, with a realistic **15–30% drawdown** and a meaningful probability of a losing year. On $100k, ~$6,000/yr. These numbers are small relative to the effort, which is the point — the honest case for this project is learning and system-building, with profit as a call option.
- **Documented ceiling of retail skill:** the top 500 of 450,000 Taiwanese day traders earned 37.9 bps/day net — but that is the 0.11th percentile of a leveraged intraday book, not a target.
- **Prop firms are not a shortcut:** ~1–2% of challenge buyers ever get paid, ~$4,270 average spend `[anon]`, against a verified ~1-in-7 annual firm-closure rate `[verified]`.
- **The edge you should expect to find is risk management, not alpha.** It is the only quantity the data says transfers out-of-sample (volatility R²=0.67, drawdown R²=0.34, returns R²≈0.015 and negative).

---

## 7. Evidence gaps in this pass

- **Reddit/Arctic Shift archive returned HTTP 500 and 429 on every attempt** across four queries against r/algotrading. No `[anon]` practitioner texture was collected. This is a real gap for failure-story hunting — the academic record covers discretionary day traders well and algorithmic retail only via the 2016 Quantopian dataset. **Recommend re-running the Reddit sweep in a later pass.**
- **No broker or exchange has ever published loss statistics segmented by API/algo traders.** Quantopian (2016, US equities, unlevered, simulated execution) is the only proxy and is now ten years stale.
- **Prop-firm payout statistics are effectively unsourced.** The load-bearing "7% of funded accounts get paid" figure has no traceable origin; treat the entire category as `[anon]` unless a firm publishes audited data.
- **Order-logic bug frequency is unmeasured** — no dataset exists, despite it being the failure mode most under this user's direct control.
- Web search budget (200 calls) was exhausted during this pass; remaining gaps were closed with direct WebFetch on primary PDFs.

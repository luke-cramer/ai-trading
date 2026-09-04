# Classic Systematic Strategies — Solo-Retail Viability, 2025–2026

**Scope:** momentum/trend (incl. dual momentum, TAA), mean reversion, pairs/stat-arb, seasonality/calendar, PEAD & event anomalies, volatility (options selling, wheel, vol targeting, VIX term structure).

**Evidence tags:** `[verified]` = audited/published/track-recorded data · `[anon]` = plausible anonymous or self-reported practitioner account · `[promo]` = author is selling something, discount heavily.

**Method limitation (state this to the orchestrator):** the Reddit archive API (Arctic Shift) was down for this run (HTTP 500 on every query, then 429). Practitioner colour below therefore comes from named blogs and self-reported accounts rather than forum aggregation. Another agent in the fan-out should retry Reddit. Web-search budget was exhausted mid-run (200/200); later facts were gathered by direct fetch.

---

## 0. The cross-cutting facts that dominate every strategy below

**Post-publication decay is the base rate, not the exception.** McLean & Pontiff studied 97 published cross-sectional predictors: returns are **26% lower out-of-sample and 58% lower post-publication**, with ~32 points of that attributable to publication-informed trading rather than statistical overfit `[verified]` (https://onlinelibrary.wiley.com/doi/abs/10.1111/jofi.12365, working paper https://www.hec.ca/finance/Fichier/McLean.pdf). Replicated since by Jacobs & Müller, Chen & Zimmermann, and Jensen et al. Chen & Zimmermann's open dataset (319 characteristics from 153 papers; ~161 remain "clear predictors" out-of-sample; data refreshed October 2025) is the single most useful free resource for sanity-checking any anomaly before you build it `[verified]` (https://www.openassetpricing.com/, https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3604626).

**Planning number: assume any published edge you find delivers ~40–50% of its paper Sharpe, before your costs.** Then subtract costs.

**Backtest quality predicts almost nothing at retail scale.** Quantopian's own 2016 study "All That Glitters Is Not Gold" found backtest performance metrics offered "little value in predicting out-of-sample performance" across a large cohort of user algorithms; the platform shut down its community and returned fund capital in November 2020 after failing to find crowdsourced alpha that survived live `[verified]` (https://www.quantrocket.com/blog/quantopian-shutting-down/, https://en.wikipedia.org/wiki/Quantopian). This is the most important survivorship-bias datapoint in the retail-quant universe: thousands of smart people, free infra, professional-grade data, ~zero durable alpha.

**Attrition base rate:** Fung & Hsieh found a ~20% annual probability that a CTA ceases operation, with 3.4%/yr survivorship bias in reported index returns `[verified]` (https://people.duke.edu/~dah7/jpm1997.htm). Retail attrition is worse and entirely unmeasured.

### Recurring cost stack (realistic 2026 dollars)

| Item | Cost | Notes |
|---|---|---|
| Daily-bar US equity/ETF EOD data | **$0–25/mo** | Stooq/Yahoo free; paid tiers cheap. Sufficient for trend/TAA/dual-momentum/seasonality. |
| IBKR API data | **$0** for non-consolidated US equities (Cboe One + IEX) + free FX/crypto `[verified]` (https://www.interactivebrokers.com/en/pricing/market-data-pricing.php) | Base 100 concurrent market-data lines; scales as commissions/8 or equity×100/$1M. No proration — subscribe on the 28th, pay the full month. |
| Polygon (rebranded **Massive**, 2026) Stocks Advanced | **$199/mo** | Options Starter $29/mo (15-min delayed), Options Developer $79/mo. Each asset class bills separately `[verified]`, secondary-sourced from vendor comparison pages (https://aifinhub.io/articles/market-data-apis-compared-2026/) |
| Databento | **$199/mo** Standard; historical **$1–5/GB**; ~**$125/mo** typical retail metered spend for a medium universe on minute bars | Metered — spend varies ±50% with schema/query pattern `[promo]`/vendor-derived |
| VPS / cloud host | **$5–40/mo** | A $6 VPS runs daily-bar strategies fine. |
| Broker commissions | ~$0 equities at most US brokers; ~$0.65/contract options at IBKR/Schwab tier | Exchange + regulatory fees are the real floor on index options. |
| Short borrow (pairs/stat-arb only) | **0.25%–>20%/yr**, hard-to-borrow can require a double-digit decline just to break even `[verified]` (https://www.interactivebrokers.com/en/pricing/short-sale-cost.php) | Swedroe: securities-lending inefficiency now exceeds **$300M/day** (https://larryswedroe.substack.com/p/the-rising-cost-of-short-selling) |

**The single biggest cost lever is timeframe.** Daily bars = $0–25/mo and free EOD history. Minute bars = $125–200/mo. Tick/OPRA options = $200–500+/mo. Every strategy below is graded on which it needs.

---

## 1. Time-series momentum / trend following

**Mechanism.** Buy assets whose trailing 3–12 month return (or price vs. a 10-month/200-day MA) is positive, short or exit those that are negative, size inversely to volatility, rebalance monthly. The premium is usually explained by slow diffusion of information plus herding and risk-management flows — investors under-react then over-react. Applied across futures (diversified CTA) or long-only across ETFs, it is the closest thing to a free crisis hedge: it went long bonds/short equities in 2008 and long commodities in 2022.

**Status 2025–2026: the worst stretch of the modern era, and there is a credible structural explanation.** `[verified]` Calendar-2025 returns: SG Trend Index **+2.39%**, Barclay BTOP50 **+2.81%**, TTU Trend Index **+1.78%** — against S&P 500 TR **+17.89%** (https://www.toptradersunplugged.com/trend-following-performance-report-december-2025/). Since Jan 2000: SG Trend CAGR **5.33%** / maxDD 20.61%; TTU TF **7.43%** / 20.93%; BTOP50 **4.08%** / 15.94%; S&P 500 TR **7.98%** / **50.95%**. So a quarter-century of trend has roughly matched equities with less than half the drawdown — but has added nothing on top, and 2023–2025 were three lean years.

The 2026 paper *"Is Trend Still Your Friend? A Microstructural Account of the Demise of Short-Term Trend-Following"* is the most important recent result on your beat `[verified]` (https://arxiv.org/abs/2607.01550). Across ~100 liquid futures, 1995–2025: **short-horizon trend P&L collapsed post-2009 on small-tick contracts while remaining essentially intact on large-tick ones.** The authors argue the mechanism is not crowding — crowding decay shows a recovery signature after positions unwind, and trend shows none — but HFT market-makers withdrawing liquidity ahead of predictable directional flow, which breaks the impact-feedback loop that made trend self-fulfilling. Practical read: **short-term trend on liquid small-tick instruments is structurally impaired; multi-month trend on large-tick contracts is not.** Man Group's own 2025 note argues the recent drawdown is within historical norms `[promo]` (https://www.man.com/insights/is-this-time-different) — they sell trend products, so discount.

**Cross-sectional (relative) momentum in equities is a different animal and did fine.** MTUM was +15.5% YTD through July 2025, roughly double the S&P `[verified]` (https://capitalspectator.substack.com/p/momentum-is-still-2025s-top-performer). But decile-based cross-sectional momentum is crash-prone and one secondary source claims a **Sharpe of roughly −0.7 on US equities post-1995** for the naive decile version, salvageable only with vol-scaling and market-state conditioning — treat that specific figure as unverified secondary (https://blog.harbourfronts.com/2025/08/28/cross-sectional-momentum-results-from-commodities-and-equities/).

**Solo retail:** long-only ETF trend / vol-targeted futures trend is the most defensible thing on this list *because it survives publication* — its premium is a risk/behavioural premium, not a mispricing that arbitrage closes. Daily bars, monthly rebalance. **Data: $0–25/mo. Infra: a cron job. Babysitting: ~15–30 min/month.** Capital: works from $5k in ETFs; futures-based diversified trend realistically needs $50k–100k+ for meaningful contract granularity (micros help but still ~$25k+ for 6–10 markets).

**Honest verdict:** highest durability, lowest running cost, lowest babysitting — and low expected excess return. Expect to spend 2–4 years underperforming SPY and questioning yourself. That psychological cost is the real cost.

---

## 2. Dual momentum (GEM) and tactical asset allocation

**Mechanism.** Antonacci's Global Equities Momentum: compare 12-month returns of US equities vs. international; hold the winner if its absolute momentum beats T-bills, else hold aggregate bonds. TAA generalises this to a broader menu (equities, bonds, gold, REITs, commodities) with a monthly ranking and often a "canary" risk-off asset.

**Status: the published GEM backtest has not survived live, and 2022 exposed the binary flaw.** Original 1974–2013 backtest: ~17.4% CAGR, ~−22% maxDD, Sharpe ~0.9 `[promo]` (author's book). Since popularisation, ~11% CAGR 1990–2026 and real-world post-2015 results "may struggle in extended U.S. bull markets" `[anon]` (https://www.traderounds.com/p/model-autopsy-dual-momentum). **2022 is the smoking gun: GEM returned −17.53% with a −20.93% drawdown, ranking 11th of 13 tested strategies, worse than plain 60/40 at −15.68%, while canary models with short-duration Treasury access (BAA-G4) returned +2.78%** `[verified]` backtest (https://bestfolio.app/blog/dual-momentum-2022-canary-models). The failure mode is structural, not bad luck: GEM's only defensive asset is AGG, and in a rates-driven joint stock/bond drawdown the "safe haven" was the worst major asset class.

Allocate Smartly tracks **100+ published TAA strategies in near-real-time**, which is the closest thing to an out-of-sample registry for this family `[promo]` (paid service, but the tracking is genuine and the site publishes losses). Their findings: TAA "did not manage losses during the 2022 bear market as well as it has during previous downturns"; **diversification has been a ~2.1%/yr drag vs 60/40 over 15+ years** because US equities dominated; 2025 was reasonable and 2026 YTD strong, with 57% of outperformance from generally-held assets and only **43% from timing** (https://allocatesmartly.com/category/taa-performance/, https://allocatesmartly.com/why-taa-is-performing-well-now-outperformance-attribution/). That 43% number is the honest measure of the actual timing edge.

**Solo retail:** trivially cheap. Monthly close data on 5–15 ETFs, one rebalance a month, ~10 minutes. **Data $0. Infra $0–6/mo. Babysitting ~10 min/month.** Capital: $5k+. Tax drag matters in a taxable account (monthly rotation generates short-term gains).

**Honest verdict:** a fine *portfolio* choice and an excellent first build. As an "edge" it is weak, well-known, and its worst-case (2022) is a correlated stock/bond drawdown where the rules actively hurt. If you build it, use a multi-asset canary variant, not vanilla GEM, and blend several lookbacks to cut whipsaw.

---

## 3. Mean reversion (equities and ETFs)

**Mechanism.** Buy short-term oversold names (RSI(2) < 5, N-day new low, distance below a moving average), exit on a bounce or after N days. Return source: liquidity provision to forced/impatient sellers plus over-reaction. Holding periods 1–10 days.

**Status: the canonical published version is dead; the family is alive but shifted to people with execution advantages.** Connors published RSI(2) in 2008 with >75% win rates on S&P names; the vanilla strategy has "lost most of its power" since `[anon]` (https://www.quantitativo.com/p/squeezing-more-profits-with-cumulative). A textbook McLean–Pontiff outcome. A modernised cumulative-RSI variant backtests to **26.6–26.8% CAGR, Sharpe 1.18, −37% maxDD, 1999–2024** on large/mega caps with a 5%-of-ADV position cap and max 3 concurrent positions — and the author's own conclusion is *"Would I trade this strategy? No,"* citing the 37% drawdown `[anon]`. Note the vanilla version's drawdown was −57%. That is the honest shape of this family: high CAGR, brutal tail, heavy left skew, all your losses in one week.

Two structural risks are well documented. **Crowding/unwind:** Khandani & Lo showed the August 2007 "quant quake" losses originated in a rapid unwind of leveraged equity market-neutral mean-reversion books; the same fragility hit stat-arb in March 2020 while other strategy types were flat or profitable `[verified]` (https://arxiv.org/pdf/2006.05632). **Execution migration:** the emerging consensus is that mean-reversion profits now accrue primarily to participants with lower latency, better data and lower costs, rather than to those with better signals — short-horizon stat-arb has become an infrastructure business.

**Timeframe/data:** daily bars are enough for the 2–10 day version, but you need **survivorship-bias-free, delisting-adjusted, split/dividend-adjusted history** or your backtest is a lie. That is the one place worth paying: a clean point-in-time universe (Norgate/Sharadar/Databento-class) at **$30–200/mo**. Free Yahoo data will systematically overstate mean-reversion returns because it omits the stocks that went to zero.

**Solo retail:** viable but the honest expectation is a low-single-digit Sharpe improvement over buy-and-hold with much worse skew. Daily-close signal generation, MOC/next-open execution, **~10–20 min/day** while live (you must handle halts, splits, and delisting-risk names manually the first year). Capital: $10k+ to diversify across 5–20 positions; below $25k the **PDT rule** blocks the intraday variants entirely in a US margin account.

**Verdict:** good learning project, real but shrinking edge, and the tail risk is the thing that ends accounts. Cap position sizes at a small % of ADV and never lever it.

---

## 4. Pairs trading / statistical arbitrage

**Mechanism.** Find two securities whose price ratio or cointegrating spread is stable; short the rich leg, buy the cheap leg when the spread exceeds ~2σ; unwind on convergence. Market-neutral in theory. Return source: temporary relative mispricing plus liquidity provision; risks are non-convergence, fundamental divergence, and synchronisation risk.

**Status: long, well-documented secular decline.** Do & Faff's "Does Simple Pairs Trading Still Work?" confirmed a continuing downward trend in profitability, with the only exceptions being the 2000–02 and 2007–09 bear markets `[verified]` (https://www.researchgate.net/publication/47554136_Does_Simple_Pairs_Trading_Still_Work). The distance method — the version in every tutorial — "no longer delivers robust returns"; cointegration and regime-switching variants still show empirical support, but "profitability today is weaker, highly dependent on market regimes, and much more sensitive to transaction costs and execution" `[anon]` (https://harbourfrontquant.substack.com/p/modern-pairs-trading-what-still-works). Recent work explicitly models pairs trading *with* stock-borrowing fees because the fee is now first-order (https://doi.org/10.1080/14697688.2025.2596920).

**The retail killer is the short leg.** Borrow accrues daily regardless of whether the trade is winning; on hard-to-borrow names it can demand a double-digit price decline just to break even `[verified]`. Add: short-sale margin (Reg T ~150% of short proceeds), hard-to-borrow recalls, dividend obligations on the short, and the fact that the pairs with the widest spreads are exactly the ones that are expensive to borrow. ETF pairs (sector vs. sector, dual-listed, commodity ETFs) avoid the worst of this and are the only version I'd call retail-tractable.

**Timeframe/data:** the surviving edge has largely migrated intraday, which means minute-or-better data (**$125–200/mo**) and low-latency execution you will not have. Daily-bar ETF cointegration is cheap ($0–25/mo) but is also the most picked-over corner.

**Solo retail:** **not recommended as a profit centre.** Costs (borrow + spread + commissions) eat a decayed edge, the intraday version requires infrastructure you can't match, and the market-neutral framing hides the fact that the failure mode is a slow bleed you rationalise for months. **Babysitting: 30–60 min/day** — pairs break and you must decide whether it's noise or a regime change, and that decision is discretionary no matter how you code it. Good learning project for cointegration/Kalman filtering; bad expected value.

---

## 5. Seasonality & calendar effects

**Mechanism.** Systematic time-of-period return patterns: turn-of-the-month (last trading day through 3rd of next month), Halloween/Sell-in-May (Nov–Apr > May–Oct), January effect, day-of-week, intramonth momentum cycles. Explanations are flow-based — pension/401(k) contributions clustering at month-end, tax-loss and window-dressing flows, summer attention effects.

**Status: unusually resistant to decay, which is itself suspicious and also the point.** Turn-of-the-month has "shown no clear sign of decay since its initial publication" and is confirmed across ~30 markets; Quantpedia's SPY implementation backtests to **7.2% CAGR, Sharpe ~1.04, ~20% time in market** `[verified]` backtest (https://quantpedia.com/strategies/turn-of-the-month-in-equity-indexes). That ~20% exposure is the real selling point: similar return to buy-and-hold with a fifth of the market exposure. The mechanism (month-end structural cash flows) is a flow effect, not a mispricing, which is *why* arbitrage hasn't closed it.

Halloween/Sell-in-May: "strongly weakened or even diminished in recent years" in some studies, yet other work finds it persisting and even strengthening globally through the 2010s (https://www.sciencedirect.com/science/article/abs/pii/S0261560620302242). A 2025 paper offers a new mechanism — SEC filing volumes 17% higher in winter, with 22% more insider trading, 13% more private offerings, 12% more activist activity (https://www.mdpi.com/2227-7072/13/4/208) `[verified]`. Critically, other research finds that **after controlling for fund flows, both Sell-in-May and the January effect become insignificant** — i.e. it's a flow artefact, and flows can change.

New and interesting: Nathan, Suominen & Tasa (2026) document an intramonth momentum cycle — US momentum returns concentrate in six trading days per month ending four days before month-end. $1 in a value-weighted WML portfolio held only those six days grows to **$18.78** over 1980–2025 vs **$2.37** otherwise `[verified]` (via https://quantpedia.com/sectoral-intramonth-momentum-cycle/). Treat as fresh and unreplicated.

**Solo retail: the best cost/effort ratio on this entire list.** Daily bars, one or two trades a month, **$0 data, $0 infra, ~5 min/month babysitting**, works at any account size, and the effect is flow-driven rather than mispricing-driven. The catch: the standalone edge is small (a few hundred bps/yr of alpha at best), returns are noisy enough that you cannot distinguish success from luck for a decade, and Quantpedia itself cautions that "calendar effects tend to vanish or rotate to different days in a month."

**Verdict:** build it as an overlay/timing filter on top of an existing allocation, not as a standalone system.

---

## 6. Post-earnings announcement drift and other event anomalies

**Mechanism.** Stocks with large positive earnings surprises (SUE or announcement-day abnormal return) continue drifting in the surprise direction for ~60 days. Explanation: investor under-reaction to earnings news, limited attention, and limits-to-arbitrage in the names where it's strongest.

**Status: the cleanest example of an anomaly arbitraged into the ground in the segment retail can access.** In developed markets, especially the US, PEAD magnitude "has been declining from annualized abnormal returns of 18% to the point of insignificance in some cases," and for large firms "seems to be becoming small to non-existent" `[verified]` (https://www.sciencedirect.com/science/article/pii/S2214635020303750). Drivers: decimalization (2001) collapsing spreads and enabling arbitrage; faster information dissemination and HFT; and stronger *immediate* announcement-day reactions leaving less room to drift. Columbia work attributes much of the decline to reduced earnings-news persistence (https://business.columbia.edu/sites/default/files-efs/imce-uploads/CEASA/Events%20Page/PEAD_Declined_over_time.pdf).

**Where drift survives is exactly where you can't trade it profitably:** PEAD is consistently strongest in stocks with wider bid-ask spreads, lower price, lower volume, lower institutional ownership, less analyst coverage, and higher idiosyncratic vol `[verified]`. The residual edge lives in illiquid microcaps whose round-trip cost exceeds the drift.

**Timeframe/data:** daily bars suffice for the holding period, but you need **point-in-time earnings estimates and actuals with correct announcement timestamps** (before/after the bell) — this is the expensive part, roughly **$50–300/mo** for a usable estimates history, and free sources are riddled with look-ahead bias in the consensus figure. That data cost against a decayed edge is the whole argument.

**Solo retail: skip PEAD as a primary strategy.** Adjacent event anomalies worth more attention as *learning* projects: index-add/delete flows (also decayed), post-buyback-announcement drift, and short-interest/squeeze dynamics. **Babysitting: 20–40 min/day during earnings season**, which is 8 weeks per quarter of real work.

---

## 7. Volatility strategies

### 7a. Options selling / the wheel

**Mechanism.** Sell cash-secured puts on a stock you'd own; if assigned, sell covered calls until called away; repeat. You are harvesting the volatility risk premium (implied > realised) and being paid to provide insurance.

**Status: the premium is real and long-documented; the wheel packaging is where retail loses.** CBOE BXM (buy-write on SPX) returned **8.4%/yr since June 1986 vs 10.9% for S&P 500 TR**, with volatility **10.7% vs 15.2%**, Sharpe **0.53 vs 0.54**, maxDD **−35.8% vs −50.9%** `[verified]` (https://cdn.cboe.com/resources/indices/factsheet/CboeGlobalIndices_BXM-Index.pdf, https://cdn.cboe.com/resources/education/research_publications/IbbotsonAug30final.pdf). Read that carefully: **identical Sharpe, lower return, lower vol.** Systematic index option selling does not beat the index; it reshapes the return distribution and truncates the right tail. The CBOE PUT index shows higher Sharpe/Sortino than SPX over 32.5 years, but Cboe's own materials flag the negative skew that makes Sharpe misleading here `[promo]` (Cboe markets these indices).

The best structural critique of the wheel specifically comes from Early Retirement Now `[anon]`, and is qualitative but correct: the wheel accumulates delta exactly when you don't want it (a falling stock takes you from 20-delta to 100-delta), premium collection collapses during long drawdowns because strikes sit far above price, and post-WWII bear markets average 1.3 years with 3.6-year recoveries — during 2000–2013 the S&P spent most of its time underwater (https://earlyretirementnow.com/2024/09/17/the-wheel-strategy-doesnt-work-options-series-part-12/). He explicitly declines to backtest it. One circulating backtest claims **1.03% CAGR with 15.08% maxDD over 2015–2025** for a wheel implementation — unverified single source, cite with caution.

**The accounting trap is the real retail failure mode:** wheel practitioners report realised premium while unrealised losses sit in assigned shares. Every "I made $X this month" post has an invisible denominator.

**Costs/capital:** $0.65/contract at IBKR-class brokers. Cash-secured means real capital — one SPY put at $650 ties up ~$65,000; a single-name wheel needs $5k–30k per position and you want 5+ positions, so **$50k+ to run it properly**. Data: EOD chains are fine ($0–79/mo via Massive Options Starter/Developer). **Babysitting: 20–40 min/day** — assignment, rolls, earnings avoidance, and dividend/early-exercise risk are all manual judgement calls. This is one of the highest-babysitting strategies on the list.

### 7b. Short vol — the failure archive

This is where retail accounts actually die, and the evidence is unambiguous.

**Feb 5, 2018 ("Volmageddon"):** VIX rose 17.31 → 37.32 in a day (+115.6%); XIV fell **~93–96%** and shrank from **$1.9B to $63M in one session** before termination `[verified]` (https://rpc.cfainstitute.org/research/financial-analysts-journal/2021/volmageddon-failure-short-volatility-products, https://www.cnbc.com/2018/02/06/the-obscure-volatility-security-thats-become-the-focus-of-this-sell-off-is-halted-after-an-80-percent-plunge.html). Mechanism: the ETPs' own rebalancing (buying VIX futures to stay neutral as their short exposure grew) created a reflexive feedback loop.

**Aug 5, 2024:** VIX spiked to **65** intraday from ~20 the prior week — the fastest IV spike on record — on an S&P only ~10% off its July peak `[verified]` (https://www.bis.org/publ/bisbull95.htm, https://www.ice.com/insights/conversations/inside-the-ice-house/market-storylines/08-05-2024). Practitioner account: a "1-1-2" /ES seller went **from +$11,000 to −$17,000 overnight on two contracts** (a 250% loss) with 90% of buying power deployed; he reports "many seasoned traders" saw accounts cut **30–50% overnight** by forced broker liquidation, and several professional advisors lost years of profit `[anon]` (https://datadrivenoptions.com/112-cautionary-tale/). The leverage math: /ES 112 trades let you control ~$500,000 notional on ~$5,000 of buying power. Naked sellers get hit twice simultaneously — premium marks explode *and* margin requirements explode — in an illiquid market.

**Read this as the base rate, not the tail.** Two account-ending events in six and a half years, both arriving with no warning from any signal you would have.

### 7c. VIX term structure

**Mechanism.** VIX futures sit above spot ~**84% of days since 2004**, with M1:M2 daily contango averaging ~5.6% (median 6.3%); longest contango run 273 trading days, longest backwardation run 76 days (2011) `[verified]` (https://www.quantvps.com/blog/vix-futures-curve-explained). Long-vol ETPs bleed structurally: **VXX three-year return −76.02% as of 24 Dec 2025**. Shorting that decay (short VXX, long SVXY, short VIX futures, calendar spreads) is the trade.

**Status:** the roll yield still exists — it's a compensation-for-insurance premium, not a mispricing. But it is the single most negatively-skewed trade available to retail. And regime matters: as of March 2026 the curve was in **backwardation**, meaning short-vol was paying the roll rather than collecting it (https://www.sixfigureinvesting.com/tag/vix-term-structure/). Post-2018, SVXY runs at −0.5x rather than −1x, which caps but does not remove the risk.

**Solo retail:** daily data, ~10 min/day. Capital: workable from $5k in ETPs. **The only responsible version is defined-risk** (put spreads on VXX, or a short-vol sleeve sized to survive a −80% day). Never short VIX futures naked in a retail account.

### 7d. Vol targeting / volatility-managed portfolios

**Mechanism.** Scale exposure inversely to recent realised volatility. Moreira & Muir (2017) showed this raises Sharpe.

**Status: largely refuted out-of-sample.** Cederburg, O'Doherty, Wang & Yan (2020) showed the strategies fail out of sample, with reasonable real-time versions earning **lower certainty-equivalent returns and Sharpes than the unmanaged portfolios**; Barroso & Detzel (2020) showed they don't survive transaction costs; the failure stems from structural instability in the underlying spanning regressions `[verified]` (https://www.sciencedirect.com/science/article/abs/pii/S0304405X2030132X, https://onlinelibrary.wiley.com/doi/full/10.1111/jofi.13395).

**Caveat that matters for you:** vol targeting *as a risk-management overlay on a trend or momentum book* is well-supported and standard practice; vol *timing as a standalone alpha source* is not. Use it as sizing, not as signal. **$0 marginal cost, no babysitting.**

### 7e. 0DTE selling

The best recent evidence is Vilkov's "0DTE Trading Rules" on SPXW, Sep 2016 – Jan 2026 `[verified]` (https://ssrn.com/abstract=4641356, annotated at https://github.com/vilkovgr/0dte-strategies). A positive 0DTE variance risk premium exists but the **median realised VRP from 10:00 ET to expiry is ~0.0011% of the underlying** — economically tiny. After half-spread + 0.5bp slippage: put ratio spreads **Sharpe 1.18 → 0.93**, strangles/straddles **0.56 → 0.39**, **iron butterflies/condors 0.77 → −0.20** (the most popular retail structure turns negative after costs), diversified top-3 basket **1.12 → 0.82**. 1% expected shortfall runs 0.58–1.58% of underlying *per day*. Author's conclusion: unconditional 0DTE selling is "difficult to justify as a standing allocation." Context: 0DTE is now ~50–63% of SPX volume with retail near half of total options volume — this is the most crowded retail trade in existence.

---

## 8. Ranking for this specific profile (build cost ≈ 0; running cost, edge, babysitting matter)

| Strategy | Recurring $/mo | Min capital | Edge durability 2026 | Babysitting | Verdict |
|---|---|---|---|---|---|
| Seasonality / turn-of-month overlay | **$0** | $2k | High (flow-driven, no decay observed) | 5 min/mo | **Build first.** Best ratio on the list. |
| Long-only ETF trend / TAA | $0–25 | $5k | Medium-high (risk premium, survives publication) | 15–30 min/mo | **Build.** Low return, high durability. |
| Vol targeting as sizing overlay | $0 | — | N/A (risk mgmt, not alpha) | 0 | **Adopt everywhere.** |
| VIX term structure, defined-risk | $0–25 | $5k | Medium (real premium, extreme skew) | 10 min/day | Small sleeve only. |
| Mean reversion, daily, large-cap | $30–200 (clean data) | $10k ($25k for PDT) | Medium-low, decayed | 10–20 min/day | Good learning, bad skew. Cap at % of ADV. |
| Wheel / index put-writing | $0–79 | $50k | Real premium, zero excess Sharpe vs index | 20–40 min/day | Distribution reshaping, not alpha. |
| Dual momentum (vanilla GEM) | $0 | $5k | Low (2022 broke the rule) | 10 min/mo | Use a canary variant instead. |
| PEAD | $50–300 | $25k | **Very low** — decayed to insignificance in tradeable names | 20–40 min/day in season | Skip. |
| Pairs / stat-arb | $125–200 | $25k+ borrow | **Low** — decayed, borrow-fee dominated | 30–60 min/day | Learn the math, don't fund it. |
| Naked short vol / 0DTE iron condors | $79–200 | any (that's the problem) | Negative net of costs (Vilkov) | constant | **Don't.** Two account-killers since 2018. |

---

## 9. Gaps / next steps

1. **Reddit was unavailable.** Re-run `r/algotrading`, `r/quant`, `r/thetagang`, `r/options` for live-vs-backtest divergence reports and wheel P&L disclosures — that's the missing `[anon]` layer.
2. **No audited retail track records found.** Collective2/Darwinex publish per-strategy stats but I found no aggregate survival statistics; worth a direct scrape.
3. **Unverified figures to re-check:** the wheel 1.03% CAGR backtest; the −0.7 Sharpe for post-1995 decile cross-sectional momentum; Alpaca/Tiingo/Norgate current pricing (not confirmed this run).
4. **Not covered on this beat, needed elsewhere:** crypto funding-rate carry, futures spreads, ML/alt-data, tax treatment (Section 1256 60/40 on index options is materially favourable and should be priced into the vol-strategy comparison).

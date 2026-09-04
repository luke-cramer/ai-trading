# ML- and Data-Driven Trading Strategies: Retail Viability Audit (2025–2026)

**Beat:** ML price prediction, RL agents, order-flow/microstructure, sentiment/news/event, LLM-native strategies.
**Evidence tags:** `[verified]` = published/audited/track-recorded data · `[anon]` = plausible anonymous practitioner account · `[promo]` = author sells something, discount heavily.

**Method caveat:** the Arctic Shift Reddit archive API returned HTTP 500 on every endpoint during this session, so r/algotrading / r/quant primary threads are absent. Practitioner voice here comes instead from public issue trackers (freqtrade), open-source backtest repos with published numbers (hftbacktest), broker/vendor price pages, and papers that explicitly audit other papers. Treat the retail-anecdote layer as thinner than it should be. Web search budget was also exhausted mid-research; several intended primary sources (Cont/Kukanov/Stoikov OFI, Rithmic/CQG fee schedules, Elite Trader threads) were not fetched.

---

## 0. The overfitting problem, quantified — read this before anything else

This is not a caveat section, it is the main finding. Every strategy family below is dominated by it.

**The single best dataset on retail-built quant strategies.** Quantopian's Wiecki et al. studied **888 user-built algorithms with ≥6 months of genuine out-of-sample performance** after the backtest was frozen. In-sample Sharpe explained **1–2% of out-of-sample behaviour (R² 0.01–0.02)**; in-sample *annual return* had a **slightly negative** correlation with out-of-sample return. The metrics that did carry over were the ones nobody optimises: annual volatility R²=0.67, max drawdown R²=0.34. And critically: **the more backtesting the developer had done (measured in total backtest-days consumed), the larger the in-sample/out-of-sample gap.** `[verified]` — https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2745220 · summary with numbers: https://www.cxoadvisory.com/big-ideas/in-sample-vs-out-of-sample-performance-of-888-trading-strategies/

One genuinely useful positive from the same paper: an **ML meta-model that predicted out-of-sample Sharpe from backtest features achieved R²=0.17**, and a portfolio of its top-10 picks hit **1.8 annualised Sharpe, beating 99% of random strategy portfolios.** `[verified]` The best documented use of ML in this dataset was *selecting among strategies*, not generating the signal.

**The academic ML-for-equities literature is mostly unusable.** A review of 27 peer-reviewed ML equity-investment experiments found **15/27 (55%) ran multiple model configurations in the test phase** (mean 70.7 configurations, median 5) — "the only number which works in real-life investing is 1"; 12 reported MAPE/RMSE-type error metrics that mask directional failure; reported hit rates where disclosed were **47–69%**, i.e. several at or below coin-flip; most ignored transaction costs entirely. Real-world counterweight from the same paper: total "pure AI" fund AUM ≈ **$10B** against $93.8T for the 500 largest non-hedge funds; Aidya liquidated in under a year; Sentient Technologies burned $143M VC and liquidated in 2018; the Eurekahedge AI index returned **114.98% vs the S&P 500's 209.74% (2011–2020)**. `[verified]` — https://pmc.ncbi.nlm.nih.gov/articles/PMC8019690/

**The statistical machinery you should actually use.** Bailey & López de Prado's Deflated Sharpe Ratio and Probability of Backtest Overfitting exist precisely to price in the number of trials, non-normality and sample length. `[verified]` — https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2460551 · https://www.davidhbailey.com/dhbpapers/backtest-prob.pdf · practical write-up: https://stefan-jansen.github.io/machine-learning-for-trading/08_ml4t_workflow/01_multiple_testing/

**Implication for a zero-build-cost operator.** Cheap iteration is the *hazard*, not the advantage. If Claude lets you run 500 feature/model/timeframe variants in a weekend, your effective multiple-testing burden is 500 and your required Sharpe threshold rises accordingly. The Quantopian result says the marginal backtest actively destroys expected out-of-sample value. The correct posture is: pre-register a small hypothesis set, one configuration per hypothesis, purged/embargoed walk-forward CV, deflated Sharpe, then a **paper-trading incubation of 3–12 months** before capital.

---

## 1. Supervised ML price prediction (GBM, LSTM, transformers on OHLCV + features)

**Mechanism.** Label forward returns (or triple-barrier events), engineer features (technicals, cross-sectional ranks, volatility, calendar, alt-data), fit LightGBM/XGBoost or a sequence model, threshold predictions into positions. Cross-sectional equity ranking is the version with the most academic support; single-asset directional prediction is the version most retail people build.

**Data/infra cost.** Genuinely near-zero at daily frequency. Alpaca free tier gives 7+ years history and IEX real-time (15-min delayed via REST, 30-symbol websocket); **Algo Trader Plus is $99/mo** for full SIP + OPRA — https://alpaca.markets/data. Add a $5–20/mo VPS. Intraday minute-bar work is still cheap; anything needing L2 is a different cost class (§3).

**Edge decay 2025–2026.** The honest read is that decay is less "the edge died" and more "the edge was never there net of costs." The AlphaCrafter paper (itself promoting a competing method, so `[promo]`-adjacent but peer-reviewable) ran an **actual paper-trading forward test Mar 2 – Jun 12 2026** (69 CSI-300 / 73 S&P-500 trading days, 2bp/1bp costs): **LSTM 20.11% backtest AR → 3.22% live on CSI-300, 16.26% → 7.52% on S&P-500; XGBoost 16.26% → 3.40% and 2.08% → 9.68%** — https://arxiv.org/html/2605.05580v2. Note the paper's own abstract elsewhere claims a **−20.40% live AR for XGBoost and a Sharpe of 1.3431 in backtest**, which does not reconcile with the v2 table; treat the specific magnitudes as unreliable and the *direction* (large forward-test degradation) as the finding. `[promo]`

Background decay rate for any published predictor: McLean & Pontiff's canonical result — ~**26% lower returns out-of-sample and ~58% lower post-publication** across 97 documented predictors. `[verified]` — https://onlinelibrary.wiley.com/doi/10.1111/jofi.12365. Anything you find in a paper, an OpenBB tutorial, or a Claude-generated feature list is post-publication by definition.

**Live retail evidence.** Weak but non-zero. **Numerai** is the strongest verifiable case of retail-scale ML producing real payouts: tabular obfuscated features, 20-day rounds, payout `stake * clip(payout_factor * score, -0.05, 0.05)`, burned NMR is destroyed, `payout_factor = min(1, 72000/total_at_risk)` so yields dilute as total stake grows — https://docs.numer.ai/numerai-tournament/staking. Numerai reports >$1M paid to data scientists in January 2025 alone and >$43M cumulative `[promo]` (self-reported by the operator). Individual outcomes are not aggregated publicly, and the honest framing is: this is a **skill-graded ML competition with real capital at risk and NMR price risk stacked on top of model risk** `[anon]` — https://www.alphanova.tech/blog/is-numerai-worth-it (author runs a competing platform, discount).

Retail vendor claims of 63–279% annualised from "AI robots" are `[promo]` marketing and should be assumed fabricated or cherry-picked; one review noted only **5 of 12 "AI" bots tested actually used ML at all** `[promo]` — https://algoalpha.co/blog/best-ai-trading-bots-honest-guide.

**Babysitting.** Low-to-moderate at daily frequency: a nightly retrain + predict cron, a fill reconciler, and a monthly review. The real time sink is research discipline, not ops.

**Verdict.** Best learning-to-value ratio of everything on this list. Realistic expectation: no durable alpha, but a genuinely good systems-building exercise. Cap capital accordingly.

---

## 2. Reinforcement learning trading agents

**Mechanism.** Agent observes a market state, emits position/size actions, is rewarded on PnL or a risk-adjusted proxy; PPO/SAC/TD3/A2C over a simulated environment (FinRL, freqtrade's RL module).

**Data/infra cost.** Same data as §1 plus real GPU/compute for training. FinRL's own contest paper reports **1,649.93× sampling speedup with 2,048 parallel environments at 227,212 samples/sec on A100s** — i.e. the field's headline engineering achievement is throughput. `[verified]` — https://arxiv.org/html/2504.02281v1

**Edge decay / does it ever work.** The most damning fact about RL trading is negative evidence: **that same FinRL benchmarking paper reports no Sharpe ratios, no returns, and no live-deployment comparison at all.** It is an infrastructure paper. `[verified]` The community's own framing, surfaced repeatedly, is the "if it worked we'd trade it" problem — published Sharpes that would generate billions are not being traded by their authors `[anon]` — https://medium.com/@liangnguyen612/reinforcement-learning-in-finance-a-practitioners-roadmap-2b84d84686a6 (403'd on direct fetch; claim is from the search index, treat as unconfirmed).

The failure mode that actually kills retail RL deployments is not alpha decay, it's **sim-to-real observation drift**. A detailed practitioner post-mortem (author selling nothing) itemises: normalisation z-score parameters recomputed from live data instead of frozen from training; position state encoded 0/1/2 in training and −1/0/1 in production, producing **confidently inverted decisions**; session flags six hours off from a UTC/local mismatch; inference on partially-formed bars (`Close[0]`) instead of closed bars. Recommended controls: serialise normalisation params, historical replay parity test to **<1e-6** max difference, then **minimum lot size on 5–10% of capital for two weeks** against the paper baseline. `[anon]` — https://www.mql5.com/en/blogs/post/773136

Confirmatory operational evidence from freqtrade's public tracker: **"FreqAI RL: Model expired for ETH/USDT:USDT due to NaNs in features"** with 13 comments — https://github.com/freqtrade/freqtrade/issues/12872. This is the real texture of running RL live at retail.

**Live retail evidence.** I found **none** — no retail practitioner with a verifiable live RL track record. The closest documented forward result in this beat is a `[promo]` case of "+2.16% over four months with a 16.86% max drawdown" at daily frequency, surfaced in an LLM-agent paper's related work rather than independently verified.

**Babysitting.** Highest of any family. Non-stationary reward landscapes force periodic retraining; every retrain is a fresh chance to ship a silently broken policy. Budget several hours/week and expect silent-failure classes that don't throw exceptions.

**Verdict.** The clearest "works in papers only" category. Build it to learn RL, not to make money. If you want RL to earn its keep, the credible application is **execution/trade scheduling** (a well-posed cost-minimisation problem with a dense reward), not alpha generation.

---

## 3. Order flow / microstructure (footprint, imbalance) at retail scale

Split this by venue, because the economics are completely different.

### 3a. US equities
Structurally hostile to retail. Full-depth consolidated data is expensive, marketable retail flow is internalised by wholesalers under PFOF so you are not competing on the lit book, and the horizon of order-flow-imbalance predictability is sub-second to seconds — below any retail round-trip latency. The academic retail-order-imbalance signal (Boehmer–Jones–Zhang–Zhang sub-penny classification) is real in-sample but is (a) published, therefore subject to the McLean–Pontiff haircut, and (b) contested on classification accuracy post-2020 — I could not verify the specific rebuttal literature within budget, so treat this as **unverified caution**, not fact. A decade-scale Korean-exchange study with explicit trader IDs finds retail–retail market orders produce **return continuation** while retail demand met by institutions produces **reversals**, i.e. the sign flips depending on counterparty — a detail no retail proxy can observe. `[verified]` (paywalled preview) — https://mlquants.substack.com/p/the-anatomy-of-retail-order-flow

### 3b. CME futures
The only order-flow venue with an honest retail price. Databento passes CME licence fees through: **non-professional CME licence from ~$32.65–36.50/month**, professional non-display **$1,219/month**; access plans are usage-based, **Standard $199/mo**, Plus $1,750/mo, Unlimited $4,500/mo, with $125 of free historical credits at signup. `[verified]` — https://databento.com/pricing · https://roadmap.databento.com/announcements/live-cme-data-is-now-open-to-all-users-starting-at-3265month. So **~$230/mo all-in for live MBO plus a plan** is the realistic recurring number for a solo footprint/imbalance system, before broker/routing (Rithmic/CQG-class fees not verified this session).

### 3c. Crypto perps — where the only concrete numbers live
`hftbacktest` publishes a reproducible order-book-imbalance market-making backtest on Binance Futures with queue-position and latency modelling from real order logs. The decay curve is the most useful single artefact in this entire report:

| Period | Instrument | Sharpe | Return | Trades/day | Return per trade |
|---|---|---|---|---|---|
| May 2023 | BTC/USDT | 10.83 | 34.2% | 4,120 | 0.0139% |
| Jan–Feb 2025 | BTC/USDT | 5.37 | 45.96% | 4,534 | 0.0086% |
| May–Jul 2025 | BTC/USDT | 3.04 | 25.03% | 3,096 | 0.0044% |

`[verified]` (open-source, reproducible) — https://hftbacktest.readthedocs.io/en/latest/tutorials/Market%20Making%20with%20Alpha%20-%20Order%20Book%20Imbalance.html

Read it carefully: **all of it assumes a 0.005% maker rebate — the single best market-maker rebate on Binance Futures — against a 0.07% taker fee.** By mid-2025 return-per-trade (0.0044%) is *below the rebate itself*, meaning the residual edge is essentially the fee schedule, not the imbalance signal. The author also had to make the queue model harsher for 2025 data "to reflect market changes and a more challenging fill." A retail account without market-maker tier rebates runs this strategy at negative expectancy. Sharpe fell **10.8 → 3.0 in ~two years**; that is the cleanest quantitative measurement of microstructure alpha decay I found.

**Babysitting.** Very high. Thousands of trades/day, exchange API/rate-limit changes, fee-tier maintenance, inventory risk, and connectivity incidents that turn into real losses in minutes. Not compatible with "check it weekly."

**Verdict.** Real edge exists here and is measurable — and it is being competed away, is rebate-gated, and demands the most operational attention of anything listed. Viable only as a deliberate high-effort project on crypto, with an explicit expectation that you are renting an edge that is shrinking ~50% per year.

---

## 4. Sentiment / news / event-driven (incl. WSB scrapers)

**Mechanism.** Ingest news/filings/social, score sentiment (FinBERT/BERTweet/LLM), trade the drift or the surprise.

**Data cost.** Free-to-cheap options: Alpaca's news feed (Benzinga-sourced) on the free tier; Benzinga expansions via Massive (ex-Polygon.io) **from $99/mo** — https://massive.com/partners/benzinga. Institutional-grade (RavenPack/Bigdata) is out of scope on price. Reddit/X scraping is free but increasingly rate-limited and — as this very session demonstrated — dependent on community archives with **no uptime guarantee**.

**Does the alpha survive costs?** The most directly relevant primary source says no. A FinBERT study over S&P 500 names using AccessWire/Benzinga/Reuters/Seeking Alpha found **positive returns before transaction costs and that realistic trading costs eliminate the apparent alpha**. `[verified]` — https://arxiv.org/pdf/2507.03350

**The WSB case specifically.** The strongest pro-WSB result is a BERTweet study over **2M+ r/wallstreetbets comments** building a "Sentiment Volume Change" metric, backtested 2020–2023: **+70% vs buy-and-hold in 2023, +84.4% in 2021, 4% loss mitigation in 2022.** `[verified]` (published) — https://arxiv.org/abs/2508.02089. But: it is a pure backtest, the outperformance is concentrated in the two most extreme retail-mania bull years, the abstract makes no transaction-cost claim, and the strategy is "decisions relied solely on SVC," which is a single-feature fit to a regime that has not recurred.

The commercial live counterexample is decisive: the **VanEck BUZZ Social Sentiment ETF returned −3.58% from April 2021 to March 2024, underperforming SPY by 15.16 percentage points** — a real fund, real money, on exactly this thesis. `[verified]` (figure sourced via Alpha Architect's review, https://alphaarchitect.com/wallstreetbets/, which 403'd on direct fetch; the number came from the search index — verify before relying on the decimal).

**Edge decay 2025–2026.** Two forces. First, the retail-mania regime that made WSB sentiment tradeable is over. Second, sentiment extraction is now a commodity — FinBERT is free, LLM scoring costs cents, and everyone is running it, which compresses the drift window. Small-cap/illiquid names decay slower (lower liquidity, slower information incorporation) — but that is also where your slippage lives. `[promo]` — RavenPack research, https://www.ravenpack.com/research/news-sentiment-everywhere/

**Babysitting.** Moderate. Feed outages, ticker-mapping errors, and the endless problem of one viral post dominating your signal. Corporate-action and symbology hygiene is the unglamorous 80%.

**Verdict.** Event-driven at *daily* horizon with a real news feed is a defensible learning project. WSB scraping specifically is a solved-and-decayed 2021 trade; build it as a data-engineering exercise, not an alpha source.

---

## 5. LLM-native strategies (LLM reads filings/news/transcripts → signal; LLM as PM)

**The strongest positive result in this entire report** is also the one with the clearest built-in expiry. Lopez-Lira & Tang (published in *Finance Research Letters* Vol. 85, 2025; v6 posted Oct 2025) show GPT-4 scoring post-knowledge-cutoff headlines achieves ~**90% portfolio-day hit rates on the non-tradable initial reaction**, and that its scores **significantly predict the subsequent drift, especially for small stocks and negative news**. And then, verbatim from the abstract: *"Strategy returns decline as LLM adoption rises, consistent with improved price efficiency."* `[verified]` — https://arxiv.org/abs/2304.07619 · https://www.sciencedirect.com/science/article/abs/pii/S0304405X26001066

Note what "works" means there: the 90% number is on the **non-tradable** initial reaction. The tradable component is the drift, it lives in small caps and negative news (i.e. wide spreads, hard-to-borrow, worst execution), and it is explicitly documented as decaying with adoption. In 2023 you were early. In 2026 you are not.

**The multi-agent LLM literature is not evidence.** An audit-oriented survey of **77 LLM-trading-agent studies** screened through 2026-03-09 found that of the 19 that even clear the bar of "emits actions + closed-loop evaluation": **2/19 report time-consistent train/test splits, 1/19 has an explicit transaction-cost model, 1/19 documents survivorship handling, 11/19 report execution timing, and 0/19 reach the top reproducibility tier.** `[verified]` — https://arxiv.org/abs/2605.19337. That is the whole field, measured.

The bias-corrected head-to-head is worse. Re-running FinMem and FinAgent over **2004–2024 across 63–91 symbols** with survivorship, look-ahead and data-snooping controls: **FinMem Sharpe 0.203–0.641 vs buy-and-hold 0.461–0.630**, FinAgent generally worse, **all alpha p-values > 0.34**. In bull markets the agents are pathologically conservative (0.12 vs 0.61 Sharpe); in bear markets pathologically aggressive (−0.38 vs −0.28). Prior LLM trading papers, per their Table 1, were evaluated over **8 months to 1 year 3 months on 3–100 symbols**. Conclusion, verbatim: *"LLM-derived alpha is likely a methodological artefact of narrow, biased evaluations."* `[verified]` — https://arxiv.org/html/2505.07078v5

**TradingAgents**, the most-forked open-source framework, is explicit if you read past the README: the authors themselves flag the Sharpe 5–8 as an artifact of a pullback-free quarter, the backtest is one quarter long, each decision costs **11 LLM calls + 20+ tool calls**, and it **has never been deployed live**. `[verified]` — https://arxiv.org/abs/2412.20138 · https://github.com/TauricResearch/TradingAgents

**Look-ahead bias is a first-class problem unique to LLMs.** An LLM trained on internet-scale text has memorised what happened. Dedicated work now exists to detect it (https://arxiv.org/pdf/2512.23847) and benchmark it (https://arxiv.org/pdf/2601.13770); the finding is that a substantial share of apparent LLM forecasting skill evaporates once you restrict to genuinely post-cutoff dates. `[verified]` **Practical rule: any LLM backtest on pre-cutoff data is worthless.** The only valid evaluation is forward, from today, on data the model cannot have seen — which means you cannot shortcut the incubation period with a backtest, at all. This is the single most important design constraint in this beat.

**LLM as portfolio manager — real money, real tickers.** Intelligent Alpha runs ETFs whose "investment committee" is GPT + Claude + Gemini. The Atlas ETF (**ticker GPT**, inception 2024-09-17, AUM $23.69M, ER 0.69%) shows **17.43% annualised since inception / +22.13% trailing year** as of 2026-08-28 `[verified]` — https://stockanalysis.com/etf/gpt/ — while Morningstar graded its May 2026 month **"F"** (1.0% vs a 4.1% category average) with **264% portfolio turnover** `[verified]` — https://www.aaii.com/etf/ticker/GPT. Verdict: live, plausible, not yet distinguishable from beta, and paying a lot of turnover for the privilege.

The longer-running AI-picks-stocks fund, **AIEQ**, has returned **10.04% annualised since Oct 2017 on a 0.75% ER with $109.6M AUM** — materially behind a plain S&P 500 fund over the same window. `[verified]` — https://stockanalysis.com/etf/aieq/

Institutional base rate: Mercer finds **55% of asset managers use AI somewhere in the investment process; 8% report measurable return improvement.** MIT: ~**95% of GenAI pilots** across industries show no measurable profit. `[verified]` — https://rpc.cfainstitute.org/blogs/enterprising-investor/2026/most-asset-managers-use-ai-few-turn-into-alpha (same author reports a 10-month live model portfolio beating MSCI World by 14pp gross of fees — **unaudited, model portfolio only** `[promo]`).

**Cost.** This is the one family with a real per-decision marginal cost. At Claude Opus 5 pricing ($5/$25 per MTok), a TradingAgents-style 11-call + 20-tool-call decision across a 50-name universe run daily is plausibly **$50–500/month**; Haiku-tier models or aggressive prompt caching cut that by an order of magnitude. Budget it explicitly — it is the only strategy family here where scaling the universe scales your bill linearly.

**Babysitting.** Low mechanical load, high *judgment* load: prompt drift, model deprecations changing behaviour under you, and the temptation to intervene when the agent's written rationale sounds wrong.

**Verdict.** Highest learning value, most fun, essentially zero verified retail edge. The defensible niche is **structured extraction rather than prediction**: use the LLM to turn 8-Ks, transcripts and filings into clean numeric features (guidance direction, litigation flags, segment deltas), then feed those into a boring linear or GBM model you can actually validate. Let the LLM be the parser, not the portfolio manager.

---

## 6. Live-evidence scoreboard

| Strategy | Retail live evidence? | Recurring data/infra $/mo | Babysitting | Decay 2025–26 |
|---|---|---|---|---|
| Supervised ML, daily cross-sectional | Weak; Numerai is the closest verifiable case | $0–99 | Low | Slow; mostly never had edge net of costs |
| Supervised ML, intraday directional | None found | $0–199 | Medium | Fast |
| RL agents | **None found** | $0–199 + GPU | **High** | N/A — no established edge to decay |
| Order flow, US equities | None found | $$$ | High | Structurally blocked (PFOF, latency) |
| Order flow, CME futures | Not verified this session | ~$230 | High | Unmeasured |
| Order flow / MM, crypto perps | Yes, reproducible open-source | $0–50 | **Very high** | **Sharpe 10.8→3.0 in ~2 yrs; measured** |
| News/event sentiment, daily | Mixed; costs eat it | $0–99 | Medium | Commoditised |
| WSB social sentiment | Live counterexample is negative (BUZZ) | $0 | Medium | Regime gone |
| LLM news → drift | Yes (published), explicitly decaying with adoption | $50–500 LLM | Low-med | **Self-documenting decay** |
| LLM as PM | Live ETFs; not beating beta | $50–500 LLM | Low | Unproven |

---

## 7. Recommendations for this operator

1. **Treat backtests as a filter for obviously-broken ideas only.** Given the Quantopian R²=0.01–0.02 result, allocate your effort to forward paper-trading infrastructure, not backtest fidelity. Three months minimum incubation; six to twelve is the institutional norm.
2. **Count your trials and deflate.** Zero build cost means unlimited trials means an unlimited multiple-testing penalty. Log every variant tried; compute the deflated Sharpe against that count.
3. **Never backtest an LLM on pre-cutoff data.** It is structurally invalid. Forward-only.
4. **The highest-expected-value build is boring:** LLM-as-extractor → numeric features → GBM → daily cross-sectional ranking on liquid names, incubated on paper, with volatility and drawdown as the metrics you actually trust (they're the ones that persisted in the Quantopian data).
5. **If you want a real, measurable edge to study, it's crypto microstructure** — and go in knowing the edge is rebate-dependent, decaying ~50%/yr, and needs daily attention.
6. **Capital sizing.** Context: 97% of Brazilian day traders persisting >300 days lost money, with ~1.1% earning above minimum wage `[verified]` — https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3423101. Size the account so total loss is an acceptable tuition payment.

## 8. Gaps / unresolved

- **Reddit archive down** — no r/algotrading or r/quant practitioner threads. This is the biggest hole; the retail failure-story layer is under-sampled and survivorship bias is correspondingly under-corrected here.
- **AlphaCrafter's LSTM/XGBoost live numbers contradict between paper versions** (v2 table vs abstract elsewhere); direction is trustworthy, magnitudes are not.
- **BUZZ ETF −3.58% / −15.16pp figure** came via search index, not a direct fetch (Alpha Architect 403s). Verify before citing.
- **Not verified:** Rithmic/CQG/Sierra Chart retail fee schedules; Cont–Kukanov–Stoikov OFI predictive horizons; the BJZZ sub-penny classification rebuttal literature; freqtrade/FreqAI community *performance* reports (only bug reports were reachable).
- **No source found** for any retail practitioner with an audited multi-year live ML or RL track record. Absence of evidence here is fairly strong evidence of absence, given how loudly such a record would be marketed.

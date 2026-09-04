# Academic Evidence Sweep: ML / RL / LLM Trading, Factor Decay, and Backtest Overfitting

**Beat:** SSRN, arXiv q-fin, peer-reviewed journals. **Question:** what should a solo retail developer with ~zero build cost, small capital, and a learning-plus-maybe-modest-profit objective actually conclude?

**Evidence tags:** `[verified]` = peer-reviewed journal, or preprint with public data/code and reproducible numbers. `[anon]` = plausible but unattributable/forum-grade. `[promo]` = author or host is selling something; discount heavily. Where a source is an **unrefereed arXiv preprint**, I say so inline — several 2025–2026 preprints below are the most decision-relevant material in this report precisely because they are the critique literature, but they have not cleared peer review.

**Caveat on extraction:** a few PDFs (Gu-Kelly-Xiu, Bailey deflated-Sharpe, Chen-Dim) resisted clean text extraction; numbers from those are cross-checked against secondary academic sources and flagged where confidence is lower.

---

## 0. Bottom line up front

1. **The headline ML asset-pricing results are real but almost entirely not yours.** The alpha is concentrated in microcaps, high-idiosyncratic-vol names, distressed stocks, short horizons, and the **pre-2004 sample**. Retail can't short most of it, and the fraction that survives realistic costs requires research-grade cost-aware optimization, not a decile sort.
2. **RL for trading has no credible net-of-cost, out-of-sample published edge.** The literature's own benchmarking efforts find agents lose to buy-and-hold on profitability once costs and impact are modeled honestly.
3. **LLM signal-extraction is the one genuinely new and partially-credible line** (Chen/Kelly/Xiu; Lopez-Lira/Tang), but the *agent* literature is, by its own auditors' count, near-totally non-reproducible and leakage-contaminated. And the original authors themselves document decay with adoption.
4. **Decay math is settled enough to plan around:** assume ~50% of any published in-sample edge survives out-of-sample; assume post-publication decay on top of that; assume your own backtest is inflated by multiple testing by more than the edge you think you found.
5. **The single highest-expected-value framing for this profile:** treat the project as *infrastructure + measurement discipline* (point-in-time data, cost modeling, deflated Sharpe, walk-forward), and treat any live capital as tuition, not as an investment thesis.

---

## 1. Classical ML for return prediction

### 1.1 What the credible literature actually claims

**Gu, Kelly & Xiu (2020), "Empirical Asset Pricing via Machine Learning," *RFS* 33(5):2223–2273** — [verified] — <https://academic.oup.com/rfs/article/33/5/2223/5758276>, ungated: <https://dachxiu.chicagobooth.edu/download/ML.pdf>, NBER w25398 <https://www.nber.org/papers/w25398>.
Sample: US stocks 1957–2016; train 1957–1974, validate 1975–1986, **out-of-sample test 1987–2016**. 94 firm characteristics × 8 macro predictors + 74 industry dummies (~920 features). Best models (trees, neural nets) roughly double the economic gains of regression baselines. **Decile long-short spread on NN forecasts: annualized OOS Sharpe ≈ 2.45 equal-weighted, ≈ 1.35 value-weighted.** Dominant signals: momentum variants, liquidity, volatility. **Transaction costs are not modeled.** That 2.45-vs-1.35 gap is the whole retail story in one number: the EW/VW spread is a direct measure of how much of the alpha lives in small names.

**Jensen, Kelly & Pedersen (2023), "Is There a Replication Crisis in Finance?", *JF* 78(5):2465–2518** — [verified], code+data public — <https://onlinelibrary.wiley.com/doi/full/10.1111/jofi.13249>, <https://github.com/bkelly-lab/ReplicationCrisis>. Bayesian hierarchical replication: the majority of factors replicate, cluster into 13 themes, and work OOS across 93 countries. **Counterweight to nihilism** — the raw phenomena are mostly real.

**Chen & Zimmermann, "Open Source Cross-Sectional Asset Pricing," *Critical Finance Review*** — [verified], full code/data — <https://www.openassetpricing.com/>, <https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3604626>. 319 characteristics reproduced; for the 161 clearly-significant originals, **98% of reproduced long-short portfolios have t > 1.96**; regression of reproduced on original t-stats: slope 0.88, R² 82%. Also **Chen (2022/2023), "Most claimed statistical findings in cross-sectional return predictability are likely true"** — [verified] preprint w/ data — <https://arxiv.org/pdf/2206.15365>: estimated false-discovery rates are far lower than the multiple-testing critics assume.

*Practical note:* Open Source Asset Pricing is free, downloadable, and is the single best zero-cost starting dataset for a retail dev who wants to learn on real signals rather than scraped noise.

### 1.2 The paper-to-live gap — where it all goes

**Avramov, Cheng & Metzker (2023), "Machine Learning vs. Economic Restrictions," *Management Science* 69(5):2587–2619** — [verified] — <https://pubsonline.informs.org/doi/abs/10.1287/mnsc.2022.4449>, SSRN <https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3450322>. Deep-learning signals extract profitability **from hard-to-arbitrage stocks and high-limits-to-arbitrage states**. Excluding microcaps, excluding distressed/low-credit names, or excluding high-VIX episodes **substantially attenuates** profitability. Performance deteriorates further under reasonable trading costs because of high turnover and extreme tangency weights. This is the most important single paper for the retail question: it says the ML alpha is *definitionally* in the part of the market a small, unsophisticated, long-biased, hard-to-borrow-constrained account cannot reach.

**Azevedo, Hoegner & Velikov, "The Expected Returns on Machine-Learning Strategies"** — [verified] SSRN working paper — <https://ssrn.com/abstract=4702406>. Nine ML strategies (linear, FFN, LSTM, ensembles) over 320 anomalies, post-decimalization sample. **Net-of-cost performance reduction: 13%–40%** depending on strategy, using Chen–Velikov effective bid-ask spreads. Best case survives: LSTM ~1.42%/mo net, six-factor generalized net alpha 1.20%/mo (t = 3.46). Important sub-finding: with modern low costs, **standard cost-mitigation techniques (banding, buy/hold spreads) mostly *hurt* net returns** — the average change in net excess return across the nine models is negative for all but one technique. Summary at QuantPedia — [promo] host but faithful — <https://quantpedia.com/the-expected-returns-of-machine-learning-strategies/>.

**Jensen, Kelly, Malamud & Pedersen, "Machine Learning and the Implementable Efficient Frontier," *RFS* (2026)** — [verified], code public — <https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4187217>, <https://github.com/theisij/ml-and-the-implementable-efficient-frontier>. Central claim: ML return-forecast studies "ignore trading costs, leading to excessive reliance on fleeting small-scale characteristics, resulting in poor net returns." Their Markowitz-ML achieves a **gross Sharpe of 2.00**; their cost-aware Portfolio-ML (learning weights directly against an economic objective, not forecasting returns then sorting) beats a sophisticated alternative by **~60% in net Sharpe and ~290% in utility**. The implementable frontier has a **declining** net Sharpe in risk — you cannot lever your way up it, because larger positions cost more to trade. For a retail dev this is the correct architecture lesson: *optimize weights subject to costs; do not rank-and-sort*.

**Novy-Marx & Velikov (2016), "A Taxonomy of Anomalies and Their Trading Costs," *RFS* 29(1):104–147** — [verified] — <https://academic.oup.com/rfs/article-abstract/29/1/104/1844518>, NBER w20721 <https://www.nber.org/papers/w20721>. **Anomalies with <50% monthly turnover generally generate significant net spreads; few above that do.** Execution costs 20–57 bps for mid-turnover strategies. The buy/hold spread (stricter entry than exit) is the most effective mitigation. **Turnover is the first-order design constraint.**

### 1.3 Research-design fragility

**Lalwani, "Empirical Asset Pricing via Machine Learning: The Role of Research Design Choices," *European Financial Management* (2026)** — [verified] — <https://onlinelibrary.wiley.com/doi/abs/10.1111/eufm.70033>. Results move materially with design choices (weighting, universe screens, retraining cadence). Corroborated informally by replication efforts finding EW ≫ VW performance, i.e. signal strength concentrated in small-cap/high-vol names (Tidy Finance replication walkthrough, <https://blog.tidy-finance.org/posts/gu-kelly-xiu-replication/> — [verified] as a methods tutorial; it does not publish its own performance table).

**Kelly, Malamud & Zhou (2024), "The Virtue of Complexity in Return Prediction," *JF* 79(1):459–503** — [verified] — <https://onlinelibrary.wiley.com/doi/abs/10.1111/jofi.13298> — claims massively over-parameterized models beat simple ones for market timing. **Rebutted by Buncic (2025), "Simplified: A Closer Look at the Virtue of Complexity"** — [verified] preprint — <https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5239006>, press summary <https://www.su.se/english/divisions/stockholm-business-school/news/articles/2025-09-25-new-research-debunks-the-virtue-of-complexity-in-return-prediction-in-finance>. Buncic shows the result is driven by two implementation choices — a zero-intercept restriction and a non-standard performance-aggregation scheme — both of which artificially handicap the simple benchmarks. **Do not build on "more parameters is free."** Also a live demonstration that even *Journal of Finance* results in this area can be implementation artifacts.

**Real-world control:** the Eurekahedge AI Hedge Fund Index returned ~**9.8% annualized Dec-2009 → Jul-2024 vs 13.7% for the S&P 500**, with *worse* relative performance in the second half of the sample than the first — [verified] index data, reported via [promo] source (a broker's insight piece): <https://www.ig.com/za/prime/insights/articles/has-artificial-intelligences-impact-on-hedge-funds-been-overhype-241121>. Funded professionals with paid data and prime brokerage collectively did not beat the index with ML. That is the most honest prior available for a solo dev.

---

## 2. Reinforcement learning for trading

### 2.1 Published results

**FinRL** (Liu et al.) — <https://arxiv.org/abs/2011.09607>, <https://arxiv.org/abs/2111.09395> — is the de facto open framework; its stated design principles include reproducibility. That is a claim, not a finding.

### 2.2 What the benchmarking effort itself found

**FinRL Contests 2023–2025, *AI for Engineering* (Wiley, 2025)** — [verified] — <https://ietresearch.onlinelibrary.wiley.com/doi/10.1049/aie2.12004>, <https://www.arxiv.org/pdf/2504.02281>. Across community contest submissions, **teams achieved better risk-adjusted returns and risk management but *poorer profitability* than the Dow Jones Index.** That is the community's own scoreboard, run by the framework's authors — i.e. the most favorable possible referee — and it still says: you get lower vol, not more money.

**"Realistic Market Impact Modeling for RL Trading Environments" (2026 preprint)** — [verified-as-preprint], code released — <https://arxiv.org/abs/2603.29086>. Most open RL backtest environments assume negligible or fixed costs, so **agents learn behaviors that fail under realistic execution.** Testing A2C/PPO/DDPG/SAC/TD3 on NASDAQ-100 (Jan 2010–Jan 2026, 90/10 split) with Almgren–Chriss + square-root impact vs a flat 10 bps baseline: **the cost model changes both absolute performance and the relative ranking of algorithms.** Meaning: every RL trading result benchmarked at a flat cost is not just optimistically biased, it is *ordinally* unreliable — the "best" algorithm changes.

**"Multimodal Deep RL for Portfolio Optimization" (preprint)** — [verified-as-preprint] — <https://arxiv.org/html/2412.17293v1>. Among tested strategies, **simple Equal-Weight Buy-and-Hold was the best performer by net profit, Sharpe, and Sortino**; the authors report their best RL policy only after *excluding* that baseline. Read that construction carefully — it is a common pattern.

This connects to **DeMiguel, Garlappi & Uppal (2009), "Optimal Versus Naive Diversification," *RFS*** — [verified] — the 1/N benchmark is extremely hard to beat OOS once estimation error is honest. Any RL portfolio result that doesn't clear equal-weight buy-and-hold net of costs is not a result.

**Standing critiques** — non-stationarity (regime drift breaks the MDP stationarity assumption outright), sample inefficiency, hyperparameter sensitivity, no accepted benchmark. See "Deep Reinforcement Learning For Trading — A Critical Survey" — [verified-as-preprint] — <https://www.preprints.org/manuscript/202111.0044/v1>.

**Retail translation:** RL is the highest-effort, lowest-evidence branch. It is a legitimate *learning* project (you will learn env design, reward shaping, cost modeling). It is not a plausible *edge* project. The honest published record is: better drawdown control, worse returns, and rankings that flip when you model impact properly.

---

## 3. LLM finance, 2023–2026

### 3.1 The results that hold up best

**Lopez-Lira & Tang, "Can ChatGPT Forecast Stock Price Movements?"** — [verified-as-preprint], v1 Apr-2023 → **v6 Oct-2025** — <https://arxiv.org/abs/2304.07619>. Using **post-knowledge-cutoff** headlines, GPT-4 achieves ~90% portfolio-day hit rates on the **non-tradable initial reaction**; scores also predict subsequent drift, **especially in small stocks and negative news**; ability increases with model size. Critically, the current abstract states: **"Strategy returns decline as LLM adoption rises, consistent with improved price efficiency."** The authors themselves have documented the decay across six revisions. Note the two load-bearing qualifiers: the strongest effect is *explicitly labeled non-tradable*, and the tradable drift is *in small stocks*.

**Chen, Kelly & Xiu, "Expected Returns and Large Language Models"** — [verified], SSRN <https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4416687>, slides <https://jacobslevycenter.wharton.upenn.edu/wp-content/uploads/2024/09/Kelly-WhartonJL.pdf>. LLM embeddings of news across **16 global markets / 13 languages**; portfolios on LLM-implied expected returns deliver **economically meaningful Sharpe ratios after transaction costs**, with explicit look-ahead controls, and beat bag-of-words/Word2Vec. Dynamics: short-horizon news momentum consistent with underreaction — **persists days in small stocks, dissipates fast in large stocks.** This is the strongest net-of-cost LLM claim in the literature and it comes from the same lab as GKX, with the look-ahead question addressed head-on. It is also, again, a small-stock effect.

**Kim, Muhn & Nikolaev, "Financial Statement Analysis with LLMs"** — [verified-as-preprint] — <https://arxiv.org/abs/2407.17866>. Anonymized, standardized statements (names stripped, years relabeled) + chain-of-thought; GPT-4 reaches **60.35% directional earnings accuracy, ~+7pp over the median analyst** one month post-release; trading on it yields higher Sharpe/alpha than ML baselines. The anonymization design is a genuine methodological contribution.

### 3.2 The replication / leakage counter-literature — this is the important part

**"Chronologically Consistent Large Language Models" (He, Lv, Manela, Wu)** — [verified-as-preprint] — <https://arxiv.org/pdf/2502.21206>. Trains LLMs with strict temporal ordering. **Contaminated models show inflated predictive ability; clean models are substantially weaker**, and much of the reported advantage in prior LLM-finance work does not survive. Related: Glasserman & Lin, "Assessing Look-Ahead Bias in Stock Return Predictions Generated by GPT Sentiment Analysis" — <https://arxiv.org/pdf/2309.17322>; "Detecting Lookahead Bias in LLM Forecasts" — <https://arxiv.org/pdf/2512.23847>; "Do LLMs Understand Chronology?" — <https://arxiv.org/pdf/2511.14214>. Consensus: GPT-4 can recall S&P 500 closes, WSJ headline dates, and index levels within its training window **with near-perfect accuracy**, and **look-ahead bias is worse at lower frequencies, for indices, and for larger models.** Also "AI's predictable memory in financial analysis," *Economics Letters* — [verified], peer-reviewed — <https://www.sciencedirect.com/science/article/pii/S0165176525004392>: if a model memorizes outcomes, forecasting capacity is **not identified** — you cannot distinguish knowledge from recall.

**"Profit Mirage: Revisiting Information Leakage in LLM-based Financial Agents"** — [verified-as-preprint] — <https://arxiv.org/pdf/2510.07920>. Evaluates **FinMem, FinAgent, QuantAgent, FinCON, TradingAgents**. **All show significant drops in the generalization setting** — inflated backtests, poor forward performance.

**FINSABER: "Can LLM-based Financial Investing Strategies Outperform the Market in Long Run?"** — [verified-as-preprint] — <https://arxiv.org/html/2505.07078v3>. **2004–2024, 100+ S&P constituents including delisted symbols** (survivorship handled). Against buy-and-hold, technical rules, ARIMA/XGBoost, and A2C/PPO/SAC/TD3. Results after bias mitigation: random-5 selection — B&H Sharpe 0.315 vs FinMem **−0.253**, FinAgent 0.094; volatility selection — B&H 0.703 vs FinMem **−0.228**, FinAgent 0.241; momentum selection — ARIMA 0.542 beats both LLM agents. Verdict: **"LLM-derived alpha is likely a methodological artifact of narrow, biased evaluations."** LLM agents are "too cautious when risk is rewarded and too aggressive when it is penalized."

**FIDES (Aug 2026 preprint)** — [verified-as-preprint] — <https://arxiv.org/abs/2608.23308v1>. 40 LLM-generated strategies, 4 models, **8 liquid US ETFs, 2023–2024 OOS**. **2 of 40 beat buy-and-hold. A plain SMA(50,200) crossover beat every model's mean Sharpe. 32 of 40 strategies *claimed* they would beat buy-and-hold; exactly 1 did.** That last number is the calibration story: the LLM's confidence in its own strategies is uncorrelated with outcomes.

**"Agentic Trading: When LLM Agents Meet Financial Markets" (2026 survey)** — [verified-as-preprint] — <https://arxiv.org/html/2605.19337v1>. 77 studies screened to 2026-03-09; 19 have both an action output and closed-loop evaluation. Of those 19: **2/19 disclose an extractable time-consistent data split, 1/19 specifies a transaction-cost model, 1/19 documents universe/survivorship handling, 11/19 report execution timing, 0/19 reach top-tier reproducibility.**

**"Toward Reliable Evaluation of LLM-Based Financial Multi-Agent Systems" (2026 preprint)** — [verified-as-preprint] — <https://arxiv.org/html/2603.27539v1>. 12 multi-agent systems (FinCon, TradingAgents, HedgeAgents, QuantAgents…). **No system satisfies more than 2 of 5 minimum evaluation criteria.** Headline: **FinMem's reported +23% return reverses to −22% under controlled conditions.** Survivorship bias alone ≈ 0.9%/yr drag. Cost economics: **a 7-agent system costs $0.50–$2.00 per daily decision in API fees**, and coordination debate adds 1–3s latency worth 5–20 bps of adverse movement; they define a "coordination breakeven spread" that is plausible for 1–2 bps large-caps and hopeless for 10–100 bps small-caps. **Note the trap:** the LLM edge is documented in *small* stocks; the LLM *agent* cost structure is only viable in *large* stocks.

**"Beyond Agent Architecture: Execution Assumptions and Reproducibility" (2026 preprint)** — [verified-as-preprint] — <https://arxiv.org/html/2606.08285>. Audit of 30 trade-relevant studies: only **14/30 have implementable transaction-cost treatment**. Worked 10-stock large-cap example 2020–2024: cumulative multiple **1.4710 at 0 bps → 1.3068 at 10 bps → 1.0806 at 25 bps**. A 47% gain becomes an 8% gain — worse than holding the same ten stocks.

**Hedge-fund-perspective review of LLM stock forecasting (2026 preprint)** — [verified-as-preprint] — <https://arxiv.org/html/2605.05211v1>. Standard LLM-finance datasets (ACL18 ~2yr, CIKM18/BigData22 ~1yr) are **too short to span a regime**. Sentiment sign-flips with macro regime (a strong payrolls print is bullish in disinflation, bearish in overheating). Cost math: 0.30%/day compounding = 112.7%/yr at zero cost; a 10 bps/day illiquidity drag cuts it to 65.5%; **one cited study becomes unprofitable at 0.2% daily cost.** Also cites the "crystal ball" experiment — participants given tomorrow's WSJ front page achieved only a **51.5% hit rate and 45% lost money.** If perfect news foreknowledge yields 51.5%, sentiment inference yields less.

**Contrast case — "Sentiment Trading with Large Language Models"** — [verified-as-preprint] — <https://arxiv.org/html/2412.19245v1>. OPT 74.4% accuracy, **long-short Sharpe 3.05 with 10 bps/trade costs**. But: the trading evaluation window is **Aug 2021 – Jul 2023, ~2 years**, and the authors admit they couldn't use frontier models and used smaller variants for compute reasons. A 2-year Sharpe of 3.05 is well inside the range that multiple testing produces from noise (§5). Treat as hypothesis, not evidence.

---

## 4. Anomaly decay, factor crowding, and adoption

**McLean & Pontiff (2016), "Does Academic Research Destroy Stock Return Predictability?", *JF* 71(1)** — [verified] — <https://onlinelibrary.wiley.com/doi/abs/10.1111/jofi.12365>, ungated <https://www.hec.ca/finance/Fichier/McLean.pdf>. 97 predictors: **returns 26% lower out-of-sample, 58% lower post-publication.** The 26% is an upper bound on data-mining; the residual ~32% is attributed to publication-informed arbitrage.

**Falck, Rej & Thesmar (2022), "When do systematic strategies decay?", *Quantitative Finance* 22(11):1955–1969** — [verified] — <https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3845928>. **Published anomalies deliver ~50% of in-sample performance out of sample.** Independent corroboration of the same haircut.

**Chen, Lopez-Lira & Zimmermann, "Does Peer-Reviewed Research Help Predict Stock Returns?"** — [verified-as-preprint] — <https://arxiv.org/abs/2212.10317>. Mines **29,000 accounting ratios** for t > 2.0 and finds the resulting predictability behaves *just like* the peer-reviewed set: **~50% of predictability remains post-sample for both**, and data mining reproduces the characteristic shape (returns rise as the original sample ends, then decay). Sharpest sub-result: **predictors with peer-reviewed risk explanations decay 65% post-publication vs 50% for non-risk predictors** — peer review systematically mislabels mispricing as risk. Retail implication: **a good story about *why* a signal works is negatively informative about whether it will keep working.**

**Chen & Dim, "High-Throughput Asset Pricing"** — [verified-as-preprint] — <https://arxiv.org/abs/2311.10685>. Empirical Bayes over **136,000 mined long-short strategies** with look-ahead eliminated; matches the OOS performance of top-journal predictors. **Predictability is concentrated in accounting strategies, small stocks, and the pre-2004 period**, consistent with limited attention. Also: standard multiple-testing methods popular in finance **fail to identify most true OOS performers.** The pre-2004 concentration is the most underrated fact in this whole report — a large share of the canonical evidence base predates decimalization-era liquidity, retail algo access, and the modern quant build-out.

**Volpati, Benzaquen, Eisler, Mastromatteo, Toth & Bouchaud (2020), "Zooming In on Equity Factor Crowding," *Journal of Risk*** — [verified] — <https://arxiv.org/abs/2001.04185>. Direct crowding metrics from trade-imbalance fluctuations and a large institutional metaorder database: **momentum-portfolio rebalancing explains 1–2% of total order flow, and that share has been increasing.**

**"Is Trend Still Your Friend? A Microstructural Account of the Demise of Short-Term Trend-Following" (2026 preprint)** — [verified-as-preprint] — <https://arxiv.org/pdf/2607.01550>. **Five-year rolling Sharpe for short-term trend collapsed from a historical 1–2.5 range to statistically indistinguishable from zero post-2010.** Meanwhile 3–12 month time-series momentum (Moskowitz–Ooi–Pedersen lineage) shows post-crisis Sharpes broadly comparable to pre-2008, ~0.4 long-run across 67 markets. **Faster = deader. Slower = still alive.** This is the cleanest horizon-vs-decay signal available and it points directly against the intraday/short-horizon instinct most retail algo builders have.

**"AI-Driven Alpha Decay" (Meng & Chen, 2026)** — [verified-as-preprint], **theory with calibration, not empirical test — discount accordingly** — <https://arxiv.org/html/2605.23905>, SSRN <https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6349698>. Models alpha half-life as h = ln2/(θ+δ(φ)); calibrates a decline from **5–7 years pre-AI to ~18 months at current adoption (φ≈0.7)**, with 42% increase in portfolio convergence 2013–2024. Equilibrium: "aggregate AI investment is positive, aggregate alpha is zero." I would not trust the 18-month number — it is a calibrated model output, not a measurement — but the *direction* is corroborated by Lopez-Lira & Tang's own observed decay-with-adoption.

---

## 5. Backtest overfitting — the statistics you cannot argue with

**Bailey, Borwein, López de Prado & Zhu (2014), "Pseudo-Mathematics and Financial Charlatanism," *Notices of the AMS* 61(5)** — [verified] — <https://www.ams.org/notices/201405/rnoti-p458.pdf>, SSRN <https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2308659>. High simulated performance is achievable after trying a **small** number of configurations. Expected maximum Sharpe from N independent zero-alpha trials ≈ √(2 ln N) − γ/√(2 ln N)... i.e. it grows with the *log* of trials, so it climbs fast then plateaus — and a handful of dozens of trials on a short sample is already enough to manufacture Sharpe ≈ 1 from pure noise. Minimum Backtest Length ≈ 2·ln(N)/E[max SR]² years. *(I could not cleanly extract exact worked figures from the source PDF; the canonical statement in the literature is on the order of ~45 independent configurations against a ~5-year sample producing an expected spurious Sharpe near 1.0. Treat the constant as approximate; the log-scaling is the robust part.)*

**Bailey & López de Prado (2014), "The Deflated Sharpe Ratio," *JPM* 40(5):94–107** — [verified] — <https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2460551>, <https://www.davidhbailey.com/dhbpapers/deflated-sharpe.pdf>. Corrects for selection bias under multiple testing, sample length, skew and kurtosis. **Requires you to honestly report N (number of configurations tried).** Companion: "The Probability of Backtest Overfitting" (PBO, via combinatorially symmetric cross-validation) — <https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253>.

**Harvey & Liu (2014), "Evaluating Trading Strategies," *JPM*** — [verified] — <https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2474755>; and **"Backtesting," *JPM* 42(1)** — <https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2345489>. The Sharpe haircut is **non-linear** and at some point takes the reported Sharpe **to zero**. **Harvey & Liu (2020), "False (and Missed) Discoveries in Financial Economics," *JF*** — <https://onlinelibrary.wiley.com/doi/abs/10.1111/jofi.12951> — double-bootstrap t-hurdles; and the Harvey–Liu–Zhu **t > 3.0** threshold for new factor claims.

**López de Prado (2018), "The 10 Reasons Most Machine Learning Funds Fail," *JPM* 44(6)** — [verified] — <https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3104816>, ungated <https://www.garp.org/hubfs/Whitepapers/a1Z1W0000054x6lUAA.pdf>. Named failure modes directly applicable to a solo build: the Sisyphus paradigm (one person doing everything), research-through-backtesting, chronological sampling, integer differentiation (over-differencing away all memory), fixed-time-horizon labeling, learning side and size jointly, non-IID sample weighting, and **cross-validation leakage** (k-fold on overlapping-label time series is invalid).

**Retail-behavior control group** — [verified]: Chague, De-Losso & Giovannetti, "Day Trading for a Living?" (19,646 Brazilian mini-index futures day traders, 2013–2015, tracked to 2017): **97% of those who persisted >300 days lost money; 1.1% earned more than minimum wage; 0.5% more than a bank teller's starting salary; no evidence of learning** — <https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3423101>. Barber, Huang, Odean & Schwarz (2022), *JF* 77(6): top-purchased Robinhood stocks show **−4.7% average 20-day abnormal returns** — <https://onlinelibrary.wiley.com/doi/abs/10.1111/jofi.13183>. *(Widely circulated figures like "22% of retail algo losses are infrastructure failures" or "1,200 accounts, algo beats discretionary by 2.1pp" surfaced only via broker-marketing pages — [promo], unverifiable, do not use.)*

---

## 6. Synthesis: what a solo retail developer should conclude

**Robust enough to build on (net of retail costs):**
- **Low-turnover, long-only, well-documented factor tilts in liquid names.** <50% monthly turnover (Novy-Marx–Velikov), value-weighted, using free Open Source Asset Pricing data. Expect ~50% of published in-sample edge (Falck–Rej–Thesmar; McLean–Pontiff), applied to a base effect that was modest to begin with. Realistic honest expectation: a small tilt over the index with tracking error, not alpha.
- **3–12 month time-series momentum / medium-horizon trend across liquid futures or ETFs.** ~0.4 Sharpe long-run, still alive post-crisis, and the only widely-studied effect where recent evidence explicitly says it has *not* decayed at that horizon.
- **Cost-aware weight optimization rather than rank-and-sort.** The single most transferable technical lesson in the literature (Jensen–Kelly–Malamud–Pedersen).

**Real in papers, not reachable by retail:**
- ML cross-sectional alpha (GKX-style). It lives in microcaps, distressed names, high-vol regimes, and pre-2004 (Avramov–Cheng–Metzker; Chen–Dim). The EW-vs-VW Sharpe gap (2.45 vs 1.35) prices the gap for you. Shorting that universe as a retail account is impractical (borrow, locates, hard-to-borrow fees), and long-only halves whatever remains.
- LLM news-drift alpha (Chen–Kelly–Xiu; Lopez-Lira–Tang). Genuinely documented net of costs — **in small stocks, at multi-day horizons, decaying with adoption, requiring point-in-time news with true ingestion timestamps** (a real recurring data cost, and the one input a retail dev cannot fake).

**Not supported by evidence:**
- RL agents as an alpha source. The framework's own contests say worse profitability than the index; impact modeling flips the rankings.
- LLM trading agents / multi-agent frameworks as an alpha source. FINSABER, FIDES, Profit Mirage, and two independent 2026 audits all say the reported returns are evaluation artifacts, with FinMem's +23% flipping to −22% under controls, 2/40 FIDES strategies beating buy-and-hold, and 0/19 surveyed studies reaching top-tier reproducibility. Plus $0.50–$2.00/day API cost per decision on top.
- Anything short-horizon/intraday. Short-term trend Sharpe went from 1–2.5 to ~0 post-2010.

**Discipline requirements, non-negotiable:** log N (every configuration tried, including the ones you abandoned); report deflated Sharpe and PBO, not raw Sharpe; purged/embargoed walk-forward, never k-fold; strictly point-in-time data with real ingestion timestamps; charge realistic spreads plus your broker's actual fees; benchmark against equal-weight buy-and-hold and SMA(50,200), both of which beat most published sophisticated systems; and **be suspicious of any signal with a good economic story** — those decay 65% post-publication vs 50%.

**Highest-value framing for this profile:** the durable asset from this project is the measurement apparatus, not the strategy. A correctly-built point-in-time, cost-aware, deflated-Sharpe research harness is the thing that lets you *evaluate* everything else for the rest of your life — including the next wave of AI-trading claims. Capital at risk should be sized as tuition.

---

## 7. Gaps / what I could not verify

- Exact worked constants in Bailey et al. (MinBTL / trials-to-Sharpe-1.0) — PDF extraction was lossy; the log-scaling result is solid, the specific constant should be re-derived from the paper before quoting.
- Precise net-Sharpe *levels* in Jensen–Kelly–Malamud–Pedersen (only relative improvements and the gross 2.00 were recoverable; SSRN/OUP blocked full text).
- No academic study found that measures **retail-account-level** performance of ML/LLM-driven systematic strategies specifically. Everything retail-behavioral is discretionary day-trading (Brazil, Taiwan, Robinhood). This is a genuine hole in the literature.
- Crypto factor literature (Liu, Tsyvinski & Wu, *JF* 2022, <https://onlinelibrary.wiley.com/doi/abs/10.1111/jofi.13119>) is established for 2014–2021 but I found **no rigorous published OOS decay study through 2024–2026**; secondary sources report cross-sectional crypto momentum weakening in 2022–2023. Under-researched relative to how accessible crypto is to retail — worth a dedicated dig.
- Several decision-relevant 2026 arXiv preprints (FIDES, Agentic Trading survey, the multi-agent evaluation audit, the trend-demise paper) are **unrefereed**. They are consistent with each other and with the peer-reviewed cost literature, which raises confidence, but none has cleared review.

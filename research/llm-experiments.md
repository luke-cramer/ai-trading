# LLMs in Trading: Track-Record Investigation

**Scope:** Have individuals actually made money using LLMs in trading? Three tracks: (a) LLM as coding assistant for conventional strategies, (b) LLM as signal generator, (c) LLM making live trade decisions. Evidence tags: `[verified]` = track-recorded/audited/published/on-chain data; `[anon]` = plausible but unverified forum/blog account; `[promo]` = author sells something, discount heavily.

**Research date:** 2026-08-28. **Coverage gap:** the Arctic Shift Reddit archive API returned HTTP 500 for the entire session, so r/algotrading primary threads are absent. Community-consensus evidence below leans on Hacker News comment archives (Algolia API) instead, which are similarly anonymous but at least attributable to named accounts with stated backgrounds.

---

## 0. Bottom line up front

The evidence separates cleanly by track, and it separates in a way that is bad news for the glamorous use case and good news for the boring one.

- **(c) LLM as trade decider: no credible positive evidence.** Every contamination-controlled benchmark run in 2025–2026 finds LLM agents at or below buy-and-hold once frictions and post-cutoff data are enforced. The one flagship public real-money competition (Alpha Arena) had four of six models lose 30–59% in two weeks.
- **(b) LLM as signal generator: a real but small, decaying, and contested academic effect.** The headline paper's own authors document that returns decline with LLM adoption, and the biggest reported number is for a reaction they explicitly label non-tradable.
- **(a) LLM as coding assistant: almost certainly the highest-value use, and almost entirely undocumented.** Nobody has published a verified track record of "LLM wrote my strategy, here's the broker statement." The evidence is structural rather than empirical, and it comes with a specific, severe hazard discussed in §5.

The single most important finding for a builder whose *build cost is near zero*: in this domain, near-zero build cost is a **liability, not an advantage**. It removes the natural multiple-testing brake. Novy-Marx and Velikov (NBER WP 33363, 2025) demonstrate LLMs can generate complete, publication-shaped research papers from a pool of **over 30,000 candidate signals** — what the Alpha Illusion authors call "industrialized HARKing" ([arXiv:2605.16895](https://arxiv.org/abs/2605.16895), §2.4). Cheap iteration means you will find a beautiful backtest. It says nothing about whether it is real.

---

## 1. Track (c): LLMs making live trade decisions

### 1.1 Alpha Arena (Nof1) — the flagship real-money experiment

Season 1 ran **Oct 18 – Nov 3, 2025**: six frontier models, **$10,000 of real USDC each**, crypto perpetuals on Hyperliquid, identical prompts and price-only inputs, fully autonomous. On-chain and therefore genuinely `[verified]` in a way almost nothing else in this report is.

| Model | Final | Return |
|---|---|---|
| Qwen3 Max | $12,231 | **+22.31%** |
| DeepSeek V3.1 | $10,489 | +4.89% |
| Claude Sonnet 4.5 | $5,799 | −42.01% |
| Gemini 2.5 Pro | $5,445 | −45.55% |
| Grok 4 | $4,208 | −57.92% |
| GPT-5 | $4,126 | −58.74% |

(Table per [traderank.ai](https://www.traderank.ai/blog/alpha-arena-alternatives-2026). Note secondary sources **disagree on the middle rankings' percentages** — [iweaver.ai](https://www.iweaver.ai/blog/alpha-arena-ai-trading-season-1-results/) reports Claude −30.81% and Gemini −56.71%, swapping 3rd/4th place drawdowns. The final dollar balances are consistent across sources; the derived percentages are not. Treat any specific % as ±15pp.)

**The critique is more informative than the result.** Boris Tseitlin's teardown ([borisagain.substack.com](https://borisagain.substack.com/p/why-alpha-arena-is-literally-the)) `[anon, but methodologically sound]`: n=1 run per model; two weeks; the highest-variance asset class in existence; price statistics only, no tools or reasoning scaffolding; and a prompt he characterises as inducing hallucination. His summary of what shorting Bitcoin at 15x on price stats alone measures: luck, not intelligence. The spread (−4.5% to −57.9% in his framing of a crash window) is exactly what you'd expect from six random leverage draws.

Aggregate reporting across Season 1 and 1.5 `[anon, secondary]`: the combined portfolio lost roughly a third of its value, with **6 of 32 trading sessions profitable**, and extreme dispersion in turnover — **Qwen executed 1,418 trades in a single round (~one per minute) against Grok's 158** ([BigGo Finance](https://finance.biggo.com/news/5BSX_Z0BaoGGrU-ID27J)). Overtrading and fee burn are a named failure mode, not an incidental one.

Season 1.5 (US equities, eight models, closed Dec 2025) was won by a "Mystery Model" later revealed as Grok 4.20 at **+12.11%**. **No Season 2 results have been published as of August 2026**, despite announced plans for web search, longer thinking time, and multi-step execution; Nof1 raised $15M in May 2026 and is reportedly building a consumer product. Draw your own inference about a benchmark company that stops publishing its benchmark.

### 1.2 StockBench — the best-designed public benchmark

[arXiv:2510.02209](https://arxiv.org/abs/2510.02209) (Tsinghua) `[verified]` is the most useful single document in this section because it is explicitly **contamination-free**: Mar 3 – Jun 30 2025 (82 trading days, entirely post-cutoff for the tested models), top-20 DJIA stocks, $100,000, three runs per model averaged.

| Model | Return | Max DD | Sortino |
|---|---|---|---|
| Qwen3-235B-Think | **+2.5%** | −14.9% | 0.0309 |
| Qwen3-235B-Ins | +2.4% | **−11.2%** | 0.0299 |
| Kimi-K2 | +1.9% | −11.8% | **0.0420** |
| OpenAI-O3 | +1.9% | −13.2% | 0.0267 |
| Claude-4-Sonnet | +2.2% | −14.2% | 0.0245 |
| DeepSeek-V3.1 | +1.1% | −14.1% | 0.0210 |
| GPT-5 | +0.3% | −13.1% | 0.0132 |
| **Passive baseline** | **+0.4%** | **−15.2%** | **0.0155** |
| GPT-OSS-120B | −0.9% | −14.0% | 0.0156 |
| GPT-OSS-20B | −2.8% | −14.4% | −0.0069 |

Read that carefully before getting excited. The top models beat buy-and-hold by ~2 percentage points over four months on 20 mega-caps — **before any transaction cost, slippage, or market-impact modelling is described**. The paper's own conclusion: "although current agents can be profitable, they rarely outperform simple baselines."

Three findings inside StockBench matter more than the leaderboard:

1. **The outperformance is long-bias, not skill.** Splitting into a downturn window (Jan–Apr 2025) and an upturn window (May–Aug 2025), "**all LLM agents underperform the passive baseline during the downturn but outperform it in the upturn**" (§4.4, Fig. 4). That is the signature of levered beta. GPT-OSS-120B went from bottom-ranked in the downturn to top-ranked in the upturn.
2. **It does not scale.** Performance degrades monotonically as the universe grows from 5 → 30 stocks; return variability rises. GPT-OSS-120B's coefficient of variation blows out to 10.2 at 20 stocks.
3. **Basic numeracy failures are common.** Arithmetic errors (miscalculating share quantities) ran 4.0–14.5% depending on model; JSON schema violations 0.4–8.0%. Reasoning-tuned variants made *fewer* arithmetic errors but *more* schema errors.

### 1.3 AMA / "When Agents Trade" — a positive result that does not survive inspection

[arXiv:2510.11695](https://arxiv.org/abs/2510.11695) (Qian et al., co-authored by Lopez-Lira) runs 5 backbones × 4 agent frameworks live on TSLA/BMRN/BTC/ETH, Aug 1 – Sep 30 2025, and concludes "**LLM-based agents can indeed trade profitably in real time, often surpassing simple buy-and-hold**."

I read the results table (Table 1) directly and I do not think that conclusion is supported:

- **Buy-and-hold on TSLA returned +46.88% over the window. Every single agent/model pairing underperformed it** — the best was InvestorAgent+GPT-4.1 at +40.83%. The "surpasses buy-and-hold" claim rests on BMRN (B&H −6.89%) and BTC (B&H +0.66%), i.e. on the assets where the benchmark was flat or negative.
- **The HedgeFundAgent rows are byte-identical across all five backbone models.** TSLA: CR −29.15, ARR −84.86, AV 40.94, SR −4.39, MDD 29.15 for GPT-4o, GPT-4.1, Gemini-2.0-flash, Claude-3.5-haiku, *and* Claude-sonnet-4. Same on BMRN (23.70), BTC (−9.09), ETH (39.66). TradeAgent's TSLA row is likewise identical across four of five backbones. Either the backbone was not actually varying, or a cached/fallback path was serving results. This is a reproducibility red flag the paper does not address, and it directly undercuts the paper's headline claim that agent architecture dominates backbone choice.
- **Sharpe of 6.47 on a two-month single-stock window**, and annualised returns of −84.86% / +783.38% extrapolated from 60 days, are precisely the artifacts §1.5 below is about.

I include this because it is the strongest pro-LLM live result in the literature and it is the one a search will surface first.

### 1.4 Other public benchmarks

- **DayTradingBench** ([daytradingbench.com](https://daytradingbench.com)) `[anon]` — an individual running 11 LLMs on live DAX/Nasdaq index day trading, identical prompt and data every 15 minutes, $100k virtual, text-OHLCV vs vision-candlestick modes. Creator's reported observation: "the performance gap between models is much larger than I expected, even though they all receive identical instructions." **The public leaderboard endpoint returned zero rows when I fetched it**, so there is no extractable P&L. Useful design, no usable result.
- **EdotEnv (YC S26)**, cofounder RuiWang0811 (background: G-Research, TransMarketGroup) `[anon, strong credentials, and note they sell RL environments to AI labs — so this is a claim *against* their commercial interest]`, HN comment July 2026: tested SOTA reasoning LLMs on real historical market data — "**they suck, and reasoning doesn't help. No model came close to a simple static benchmark**" chosen by an experienced human quant. Behavioural detail worth remembering: "**when losing, LLMs trade less rather than smarter.**"
- **KTD-Fin** ([arXiv:2605.28359](https://arxiv.org/abs/2605.28359)) — ten frontier LLMs on CSI300 with identifiers and calendar information masked. Finding: "**limited evidence of persistent stock-selection alpha**"; agent returns "**largely explained by passive market and style exposure**."

### 1.5 The agent-paper literature and its demolition

The 2024–2025 wave (FinMem, TradingAgents, FinAgent, FinCon, QuantAgent, FLAG-Trader) reported eye-watering numbers: TradingAgents AAPL Sharpe **8.21**, GOOGL **6.39**; FinCon NFLX **2.37**, portfolio **3.27**; FinMem TSLA **2.68**; FinAgent TSLA **2.01**.

**"The Alpha Illusion"** ([arXiv:2605.16895](https://arxiv.org/abs/2605.16895), May 2026, Fudan / SWUFE / Imperial / Peng Cheng Lab) `[verified]` dismantles them, and it is the single most valuable citation in this report:

- **Direct reproduction.** One-year backtest, Jan 2025 – Jan 2026, $100K, equal-weight TSLA/NVDA/KO/XOM/MSTR, charging commission, token cost, spread, and market impact. Buy-and-hold ends at **$104.8K**. TradingAgents: **$106.4K gross → $102.3K net**. QuantAgent: **$81.4K gross → $77.9K net**. Portfolio Sharpe falls **0.43 → 0.22** for TradingAgents and **−0.96 → −1.15** for QuantAgent. **Both agents finish below buy-and-hold.**
- **Frictions are simply not modelled.** Across FinMem, TradingAgents, FinAgent, FinCon and QuantAgent, **35 of 40 system × friction-component cells are unmodeled**. Only commissions are handled by all five; market impact, latency, slippage, financing, taxes and token cost are absent from most.
- **Contamination is measurable and huge.** Li et al. ([arXiv:2510.07920](https://arxiv.org/abs/2510.07920), "Profit Mirage") compare inside vs. outside the pretraining cutoff: **FinMem's total return drops ≈71.85%** and **QuantAgent's Sharpe ≈51.48%** once the window crosses the cutoff.
- **Those Sharpes are statistically meaningless.** Applying Lo (2002)'s standard error, `SE(SR) ≈ sqrt((K + SR²/2)/T)`, TradingAgents' AAPL Sharpe of 8.21 is computed on **T ≈ 60 daily observations**; GOOGL's 6.39 on T ≈ 60. The 95% CI half-widths "routinely exceed typical between-system gaps." The FinBen GPT-4 FinTrade Sharpe is reported as **1.51 ± 1.08** — a standard error exceeding half the mean.
- **Multi-agent debate doesn't help.** Zhang et al. ([arXiv:2502.08788](https://arxiv.org/abs/2502.08788)): across 36 configurations (4 models × 9 benchmarks), **multi-agent debate wins under 20% of the time**, and adding rounds or agents does not improve — and may degrade — performance.
- **LLM financial knowledge is not point-in-time.** Shah et al. (COLM 2025, [arXiv:2504.00042](https://arxiv.org/abs/2504.00042)): LLMs answer revenue questions correctly for **54.17% of large-cap firms in 2017 but only 6.32% in 1995**. So a recent mega-cap backtest is *doubly* misleading — it leaks future information through semantic memory *and* rests on knowledge gaps for exactly the smaller/older names real deployment must handle.
- **Best title in the field:** Jang et al., "The Losing Winner: An LLM Agent That Predicts the Market but Loses Money" (NeurIPS 2025 Workshop on GenAI in Finance) — RL training measurably improves BTC market-state classification accuracy while cumulative simulated returns *decline*. Optimising the gross-side proxy actively degrades the net-side reality.

Corroborating work: **"Beyond Agent Architecture"** ([arXiv:2606.08285](https://arxiv.org/abs/2606.08285)) surveys 30 trade-relevant studies and finds reproducibility artifacts mostly at the lowest tier (15/19 at R0, 3/19 at R2, **0/19 at R3**). **OpenPM** ([arXiv:2608.09988](https://arxiv.org/abs/2608.09988)) states plainly that even under auditable point-in-time evaluation, "all returns are upper bounds on a single frozen window without market impact, **not validated alpha**," and that **turnover is the main cost driver**. **TradeTrap** ([arXiv:2512.02261](https://arxiv.org/abs/2512.02261)) shows single-component perturbations cascade into "extreme concentration, runaway exposure, and large portfolio drawdowns" — these agents can be **systematically misled at the system level**.

**Telling detail:** the TradingAgents repo now has **101.6k stars** and a README that has quietly retreated to: "Backtest results are not guaranteed to match any published figure… treat this as **a research scaffold for studying multi-agent analysis, not as a strategy with a fixed, replicable return**" ([github.com/TauricResearch/TradingAgents](https://github.com/TauricResearch/TradingAgents)). Similarly, virattt's `ai-hedge-fund` (~59k stars) states it "**does not actually make any trades**" and is educational only. The two most-starred LLM trading repos on GitHub both disclaim the thing people star them for.

### 1.6 Individual live experiments — how they actually ended

- **ChatGPT Micro-Cap Experiment** (Nathan Smith, [github.com/LuckyOne7777/LLM-Trading-Lab](https://github.com/LuckyOne7777/LLM-Trading-Lab), 7,497 stars) `[verified — daily CSV logs, forward-only, publicly committed]`. $100, **Jun 27 – Dec 26 2025**, ChatGPT selecting micro-caps under hard stop-loss constraints. Month one drew press for +25% vs S&P <3% ([Futurism](https://futurism.com/chatgpt-stocks-100-dollars)). **The ending is the interesting part.** His final 40-page evaluation explicitly *declines* to make an alpha claim: benchmarks were "included to provide contextual reference for broad market conditions… **rather than to evaluate relative performance**." His conclusions: equity was "**dominated by a small number of high-impact trades**"; "high position concentration amplified exposure to individual ticker outcomes, with a single adverse position exerting a disproportionate influence"; the model **re-entered tickers after realising losses on them**, and "tickers subject to repeated buy-side entries accounted for the largest cumulative equity losses." His summary: the LLM behaves like "high-conviction, thesis-driven discretionary trading" with "**asymmetric downside exposure**." He also flags that temperature was never fixed and models were swapped as released — so it isn't a controlled experiment. This is the most honest retail write-up I found, and it converged on *behavioural characterisation*, not profit.
- **Lobstar Wilde** `[verified — on-chain]`. Nik Pash (OpenAI Codex team) launched an autonomous Solana trading agent on **Feb 19, 2026** with $50k in SOL and a goal of $1M. On **Feb 22 — day three** — an X user replied to the bot's post with a sob story about an uncle's tetanus treatment, a request for 4 SOL (~$310), and a wallet address. The agent sent **52.4 million LOBSTAR tokens, ~$441,780 notional** (~$40k realised given liquidity) ([Cointelegraph](https://cointelegraph.com/news/openai-employee-s-ai-agent-accidentally-sent-442k-to-beggar)). Root cause per the postmortem: a tooling crash lost conversational state; the agent recovered its persona from logs but reconstructed the wallet balance wrongly, then made a decimal error sending a "small" tip — roughly 5% of the token's entire supply. Built by an OpenAI engineer, dead in 72 hours, killed by a stranger's plain-text request. **Treat this as the canonical argument for a hard, non-LLM execution layer.**
- **SF Standard survey** ([sfstandard.com](https://sfstandard.com/2025/10/31/ai-told-stocks-buy-results-wild/)) `[anon, self-reported]` — the "AI beat the market" stories, and they need deflating. Daniel Padilla: Perplexity portfolio +49%, ChatGPT +52% (Mar–Oct 2025) vs S&P +22%. Harpaul Sambhi: ChatGPT Deep Research 35% over a year vs his human wealth manager's 40% and S&P ~15%. Note what both are: **AI-themed stock portfolios during an AI-stock bull market.** That is sector beta with a chatbot attached, and Sambhi's own AI portfolio *lost to his human advisor*. Both participants keep the bulk of their money in index funds.
- **Retail losses** `[anon]` — a one-month ChatGPT-5 Thinking forex experiment with $300 ending −20%; a $10,000 crypto run losing $7,200 in a week with 42 of 44 trades negative. Neither is verifiable (the forex site's domain no longer resolves). Directionally consistent with everything above; do not cite the specific numbers.
- **"I built an agentic trading bot that made 200% in days — here's why I shut it down"** `[anon, paywalled/403]` — the retrievable detail is the mechanism: the author **removed the risk-management agents because with them the bot took almost no trades**. That is the retail failure loop in one sentence.
- **deemwar.com**, "We ran autonomous AI agents on a live brokerage account for a day (it lost money)" — surfaced via HN, body not retrievable. Title logged for completeness.

---

## 2. Track (b): LLMs as signal generators

This is where the only defensible academic effect lives, and it is smaller and more fragile than the headlines.

**Lopez-Lira & Tang, "Can ChatGPT Forecast Stock Price Movements?"** ([arXiv:2304.07619](https://arxiv.org/abs/2304.07619), v1 Apr 2023 → v6 Oct 2025, now published in *Journal of Financial Economics*) `[verified]`. The famous "~90% portfolio-day hit rate" applies to the **initial market reaction, which the authors themselves label non-tradable**. The tradable claim is the subsequent drift, concentrated in **small stocks and negative news**. And the paper's own abstract contains the decay finding: "**Strategy returns decline as LLM adoption rises, consistent with improved price efficiency.**" Lopez-Lira has said publicly that paper results are "much more optimistic than what the performance in reality would be with a reasonable investment size" ([CNBC](https://www.cnbc.com/2023/04/12/chatgpt-may-be-able-to-predict-stock-movements-finance-professor-says.html)). The author of the paper that launched this field is telling you the edge shrinks as you and everyone else adopt it.

**The look-ahead literature:**
- **Glasserman & Lin** ([arXiv:2309.17322](https://arxiv.org/abs/2309.17322)) separate two biases: look-ahead (memorised outcomes) and a "distraction effect" (general company knowledge polluting sentiment measurement). Counterintuitive result: **anonymising company identifiers *improved* in-sample returns**, especially for large firms — distraction dominates look-ahead in-sample. Their recommendation, anonymisation, is directly actionable.
- **"Detecting Lookahead Bias in LLM Forecasts"** ([arXiv:2512.23847](https://arxiv.org/abs/2512.23847)) builds a Lookahead Propensity score that is "materially positive throughout the in-sample period and **collapses essentially to zero right after the training-data cutoff**." The predictive power amplification on high-LAP firm-date pairs "loses significance on post-training-cutoff samples." Translation: much of what looks like forecasting skill *is* memorisation, and it is now measurable.

**Follow-ups with honest effect sizes** (via [algotrader.ch](https://algotrader.ch/ai-trading/chatgpt-trading/), a review site that sells nothing and is explicitly skeptical of AI marketing):
- **Anic et al. (2025)**: an LLM news filter produced **out-of-sample alpha of 3.26%/year, significant only at the 10% level**.
- **LoGrasso (2025)**: GPT-4 stock picks produced **27% raw returns but statistically insignificant risk-adjusted alpha**.
- **ChatGPT vs DeepSeek on WSJ articles** ([arXiv:2502.10008](https://arxiv.org/abs/2502.10008)): ChatGPT shows predictive power sourced from **investor underreaction to positive news**, strongest in downturns and high-uncertainty regimes; negative news correlates but does not predict; DeepSeek underperforms.

That is the honest picture of track (b): a low-single-digit annual alpha, marginal significance, concentrated in small caps and news underreaction, decaying with adoption, and requiring anonymisation to even measure honestly.

**The one live product** `[promo — discount heavily]`: Lopez-Lira partnered with Autopilot (CEO Brian Schardt) on "Portfolio GPT" — 15 monthly-rebalanced assets (10 stocks, 5 sector ETFs), reportedly **~32% YTD vs S&P ~28% as of March 2026**, ~$11.3M in the strategy ([ai-street.co](https://www.ai-street.co/p/chatgpt-portfolio-outperforming-s-p500)). Self-reported, not independently audited, ~4pp over benchmark in a strong tape, and there is a fee-charging product attached. Not evidence.

**Adjacent verified failure:** the Amplify AI Powered Equity ETF (AIEQ, launched Oct 2017) has averaged **~10.00%/yr since inception**, materially behind an S&P 500 index fund over the same span; its sibling AI Powered International Equity ETF (AIIQ) was **liquidated July 29, 2022** ([stockanalysis.com/etf/aieq](https://stockanalysis.com/etf/aieq/), [StreetInsider](https://www.streetinsider.com/Business+Wire/AIIQ+Fund+Closure+Announcement/20268089.html)). Pre-LLM ML, but it is the longest real-money AI-stock-picking track record that exists, it is public, and it lost to the index.

---

## 3. Track (a): LLM as coding assistant — the strongest case, and the thinnest evidence

**I could not find a single verified track record of "an LLM helped me build a conventional strategy, here is the broker statement."** That absence is itself the finding. What exists:

- **Practitioner testimony** `[anon]`, HN, Jan 2026, user *KellyCriterion*: "**my system was heavily built with Claude, though not per vibe coding, more like a junior supporting me**" — coupled with a warning that real-money systems need professional oversight and that account losses drive non-professional builders out fast. This is the modal credible account: LLM as a fast junior, human owning the design.
- **The structural argument** from algotrader.ch: LLMs reliably deliver **idea generation, code scaffolding, and summarising large text volumes (filings)**. They do not deliver execution, risk control, live data, or validated strategies. The key line, and it is the best sentence in this entire research sweep: "*A language model optimizes for a plausible answer, and in ChatGPT trading research **a plausible backtest is precisely the dangerous kind***."
- **Tooling is real and maturing.** QuantConnect ships an official MCP server letting LLMs create projects, run backtests, and deploy live algorithms ([quantconnect.com/mcp](https://www.quantconnect.com/mcp)); an Agentic Studio and GPU-accelerated parallel LEAN for mass hyperparameter search followed. Note the hazard: institutional-grade infrastructure for running *thousands* of variants, handed to someone with no multiple-testing discipline.
- **Vibe-trading content is uniformly `[promo]`.** NexusTrade's "Claude Opus 4.5 built a strategy that is destroying the market" reports a leveraged-ETF (TQQQ) drawdown-accumulation rule with backtests of +356.3% (2020–22), **−53.1% (2021–23)**, +0.18% (2022–24), +526% (2023–Nov 2025), max drawdowns **51–76%**, and no clear in-sample/out-of-sample split — while selling the platform it was built on ([nexustrade.io](https://nexustrade.io/blog/i-asked-claude-opus-45-to-autonomously-develop-a-trading-strategy-it-is-destroying-the-market-20251125)). A "vibe-coded" 3x-QQQ dip-buyer is a bull-market beta machine; the −53% period is the honest number. The Rogue Quant's "ChatGPT vs Claude cage match" claims profit factor 2 → 5 with **the results, code, and any out-of-sample validation behind a paywall** — sales content, not evidence.
- **The Medium piece "I gave Claude Code 100k to trade with and beat the market"** returned 403 through every route I tried. Unverified, and a one-month equity-market outperformance claim is not distinguishable from noise regardless.

**Crucially, the skeptics' own recommendation lands here.** The Alpha Illusion's §5 prescribes exactly this architecture: LLMs as **auditable information interfaces upstream** of independent calibration, risk, and execution modules — Stage 1 (schema-bound extraction from news, filings, calls) with LLM involvement tapering to observer/explainer roles by the sizing and execution stages. "Final decision authority does not rest on an uncalibrated LLM." The most rigorous critics of LLM trading and the most credible practitioners converge on the same design.

---

## 4. Community consensus

Hacker News comment archive `[anon, but named accounts with stated backgrounds]`:

- *atomicnumber3* (Apr 2025), working alongside financial analysts: "**getting token predicted answers is just going to get you the same as everyone else, which means zero alpha**." Beating markets requires criteria others haven't found; LLMs are consensus machines by construction.
- *Karrot_Kream* (Mar 2026): "**algo trading shops use AI all the time, they just don't use LLMs.**" LLMs are good for coding scaffolding, unreliable for numerical optimisation.
- *browningstreet* (Aug 2025): asked frontier models for guidance on making $200k/yr as an algo trader — "**no uplift**."
- *RuiWang0811* (Jul 2026, ex-G-Research/TMG): quoted in §1.4 — SOTA reasoning models lose to a simple static human-quant benchmark.

Synthesised consensus: **LLMs are components inside a system, not sources of alpha.** No credible practitioner in the sources I found claims otherwise. The claims that do run the other way come from people selling platforms, subscriptions, or managed strategies.

---

## 5. The specific hazard for a zero-build-cost solo builder

Worth stating separately because it inverts the user's assumed advantage:

1. **Multiple testing without a brake.** Novy-Marx & Velikov show LLMs generating papers from 30,000+ candidate signals. Harvey, Liu & Zhu's classic result — cited in the Alpha Illusion — is that the factor zoo demands a **t-statistic hurdle above 3.0**, not 2.0. If Claude can produce and backtest 200 strategy variants in a weekend at zero marginal cost, your best backtest is an order statistic, not a discovery.
2. **The realistic ceiling is tiny.** Empirical asset pricing (Gu, Kelly & Xiu 2020, cited ibid.) finds monthly stock-level R² rarely exceeds **~0.4%** and portfolio-level R² **~1–2%** even with disciplined ML pipelines. Any LLM backtest implying more is measuring something other than predictability.
3. **Frictions decide the outcome, and are exactly what the LLM will omit.** The Alpha Illusion's reproduction moved TradingAgents from beating buy-and-hold to losing to it purely by charging commission, spread, token cost, and impact. OpenPM: **turnover is the main cost driver**. An LLM writing your backtest will default to frictionless fills unless you force it not to.
4. **Inference cost is a friction too.** Multi-agent LLM systems pay token cost and inference latency on the *right-hand side* of the net-PnL equation. A pipeline of 8 agents debating each trade has a real per-decision cost that must clear before you see a dollar.
5. **Autonomy is the acute failure mode.** Lobstar Wilde lost ~$440k of notional in 72 hours to a text message, built by an OpenAI engineer. TradeTrap shows single-component perturbations cascading to runaway exposure. Anything with an LLM holding final execution authority is one lost-state event from a total loss.

---

## 6. Gaps and caveats in this research

- **Reddit is missing.** The Arctic Shift archive API returned HTTP 500 for every query across the session (r/algotrading, all phrasings). r/algotrading's collective opinion on LLM strategies — the single best source of unfiltered retail failure stories — is unrepresented here.
- **Web search budget was exhausted mid-sweep** (200/200), so the back half relies on direct fetches of known URLs, the arXiv API, GitHub, and the HN Algolia API.
- **Several key sources were unfetchable**: nof1.ai (HTTP 429 on both attempts — I have no *organiser-stated* caveats about Alpha Arena's statistical power, only third-party critique); the Medium Claude Code and agentic-bot-shutdown posts (403); the cybernews debunk of a viral AI trading claim (403); DayTradingBench's leaderboard (empty).
- **Alpha Arena percentage figures conflict across secondary sources.** Dollar balances agree; derived returns do not. On-chain verification would resolve this and I did not do it.
- **Survivorship bias persists despite effort.** Blown accounts mostly do not get written up. The retail failure stories I found are the ones people chose to publish — the true distribution is worse than what is documented here.

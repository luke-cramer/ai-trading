# AI Trading Research Spike — Final Report

**Date:** 2026-08-29 · **Phase 1 deliverable** for the ai-trading project.
**Method:** 18-agent research workflow (13 parallel researchers across strategy/AI/market/base-rate beats, 1 adversarial critic, 3 gap-fill verifications), synthesized by hand. Every claim inherits an evidence tag: **[verified]** = primary source fetched (paper, regulator, exchange API, own replication) · **[anon]** = plausible but unverifiable practitioner account · **[promo]** = the source sells something. Raw research corpus: 17 files, preserved in the session scratchpad; key sources in the appendix.
**Not investment advice.** This is a research synthesis for a personal learning project.
**Web version:** https://claude.ai/code/artifact/729358ff-4141-45e4-8f51-059e2c7b0b48

---

## Executive summary

**The honest headline: retail algorithmic trading is a negative-expectation hobby for the median participant, a roughly break-even one for a disciplined operator, and the durable asset you build is the measurement apparatus, not the strategy.** Size capital as tuition.

The five facts that shaped every ranking below:

1. **Backtests are nearly worthless as return predictors.** In the only large honest dataset ever published (Quantopian, 888 real algorithms, point-in-time code, ≥6-month out-of-sample), backtest Sharpe explained **~2% of live Sharpe variance**, backtest *returns* were **negatively** correlated with live returns, and more backtesting predicted worse live results. What transferred: **risk** (volatility R²=0.67, drawdown R²=0.34). You can control risk; you cannot trust projected return. [verified]

2. **Your "zero build cost" advantage inverts into your biggest risk.** Cheap iteration with Claude means you can run the overfitting loop faster than anyone in history. The Quantopian finding — more backtests → bigger in-sample/out-of-sample gap — is a direct warning. Countermeasures are process, not code: pre-registered hypotheses, one-shot out-of-sample tests, deflated Sharpe ratios, and **forward-only evaluation for anything LLM-touched** (any LLM backtest over pre-training-cutoff data is contaminated; FinMem's return dropped ~72% post-cutoff). [verified]

3. **Published edges decay ~50% and the verification pass killed our own #1.** McLean–Pontiff: 26% lower out-of-sample, 58% lower post-publication. Our first-pass research ranked the turn-of-the-month effect #1 ("no decay observed"); an independent verification agent then replicated it from raw S&P data and found it **statistically dead in US equities since ~2001** (t=0.39 post-2002), killed by the collapse in transaction costs. The lesson generalizes: any edge you can find on a vendor site is priced until proven otherwise. [verified — own replication]

4. **LLMs are components, not sources of alpha.** Across every credible 2024–2026 test, LLM-as-live-decision-maker has no positive evidence net of costs (Alpha Arena real money: 4/6 frontier models −30% to −59% in two weeks; a frozen static rulebook beat four frontier LLMs rewriting their strategy daily). LLM-as-feature-extractor (news → structured features → conventional ML) has real but small, decaying evidence. LLM-as-coding-assistant is the strongest use and is exactly your plan. [verified]

5. **The base rate for "beats the benchmark net of costs over 3 years" is ~10–20%, and the modal death is leverage, not decayed alpha.** Brazil futures day traders persisting >300 days: 97% lost money. Collective2 futures strategies still profitable at 24 months: 5.8%. The dominant kill mechanism on every marketplace: leverage + averaging down, converting a mediocre edge into a terminal drawdown. **An unlevered strategy structurally cannot die this way — it can only underperform.** That one design choice buys more survival probability than any signal. [verified/anon]

**What survives for your profile:** unlevered ETF trend/tactical allocation (durable, cheap, safe), a zero-capital crypto carry *measurement* system on the newly-available CFTC-regulated onshore perp venue (the single best learning-per-dollar project found), risk-targeting as the one edge that provably transfers, cross-sectional ML on daily bars with LLM-extracted features (breadth = fast evidence), and medium-horizon trend on micro futures. Everything fast, levered, offshore, or LLM-autonomous is tuition at best.

---

## Part 1 — Strategy universe: verdicts

Grouped by verdict, with the evidence that drove it. (Full detail per family in the research corpus.)

### Durable enough to build on

- **Long-only ETF trend / tactical asset allocation (dual momentum with canary assets, TAA).** Decades of out-of-sample data; behavioral/institutional-flow mechanism; survives costs because turnover is monthly and instruments are free to trade. Caveat learned in 2022: vanilla GEM lost −17.5% (bonds failed as the safe asset); modern variants use canary assets (e.g. BAA/HAA) for the risk-off signal. Excess return honest range: 0–2%/yr over benchmark with materially lower drawdowns. [verified — academic + long practitioner record]
- **Medium-horizon time-series momentum (3–12 month) on diversified futures.** Post-2010, short-term trend is dead; 3–12-month TSMOM survives at ~0.4 Sharpe. "Faster = deader" held in every dataset. Carver's honest anchor: the average single rule on a single instrument is ~0.15 Sharpe — the edge comes from combining many rules × many instruments. [verified]
- **Volatility targeting as a sizing overlay.** Not alpha — but risk is the only quantity that transfers out-of-sample (Quantopian R²=0.67), and vol-targeted versions of everything above show better realized Sharpe and drastically better drawdowns. This is the highest-confidence "edge" in the corpus. [verified]
- **Low-turnover long-only factor tilts (value/momentum/quality blends, <50%/mo turnover).** Post-publication factor returns are ~40–50% of paper returns, and implementation costs eat 2–4%/yr from theoretical factor returns — but low-turnover long-only implementations keep a thin, durable premium. Slow to generate evidence. [verified]
- **Crypto funding/basis carry — onshore, conditionally.** The one crypto edge that survived scrutiny, with a 2026 plot twist: see Part 3. The offshore version (4–10% net APY) is closed to US persons; the onshore version is now legal and liquid (Coinbase Derivatives nano BTC perp, $149M OI) but naive spot+perp carry ≈ **a T-bill with a 24/7 pager**. The residual candidate is the perp-funding-vs-CME-basis spread (~5pp gross in a 44-hour sample — persistence completely unverified). [verified venue data; unverified edge]

### Decayed — tuition only

- **Turn-of-the-month / calendar seasonality (SPY).** Refuted by our own replication: alpha +2.96%/yr with t=3.79 through 2001 → **+0.28%/yr, t=0.18 after costs, 2006–2026**. In a taxable account the short-term-gains drag makes it net negative. The effect survives only in high-cost venues retail can't reach (CEE markets, thin ag futures) — which is exactly what a real, structurally-killed edge looks like. Still an excellent *first harness test*: trivial data, four trades of logic, built-in lesson. [verified — own replication]
- **Daily mean reversion in US equities.** Decayed hard post-2010, brutal left skew, and requires survivorship-bias-free data ($30–200/mo) to research honestly. [verified]
- **PEAD / earnings drift.** Decayed to statistical insignificance in tradeable (mid/large-cap) names. [verified]
- **Pairs / stat-arb.** Decayed, and borrow fees dominate the residual. [verified]
- **Sell-in-May.** The single calendar effect that survives data-mining correction — and only in the international cross-section, weakly. A tilt, not a strategy. [verified]

### Structurally negative at retail — do not build

- **Short volatility without defined risk (naked strangles, 0DTE condors).** Vilkov: iron condor Sharpe 0.77 → **−0.20 after real costs**. The strategy family that produces the most confident sellers and the most dead accounts. [verified]
- **Market making / grid bots at retail fee tiers.** Retail makers *pay* fees on most venues (Binance's rebate program starts at $20M/month volume); grid trading is short gamma without collecting premium; Hummingbot-class inventory risk gives back weeks of spread in one trending session. A real-world Polymarket MM build log: 719,624 orders, 0.17% fill rate, fills skewed 8:1 toward the losing side. [verified/anon]
- **Triangular & cross-exchange crypto arb.** Provably dead: a 2025 study put realizable retail profit at $12–17/week and required ≤146ms execution. Multiple independent HN post-mortems agree — the visible spread is compensation for counterparty/withdrawal risk. [verified]
- **AMM liquidity provision.** Fees < impermanent loss/LVR across multiple studies. Structurally negative. [verified]
- **Retail scalping / sub-30-minute systems.** Breakeven win rate at typical retail costs: ~90% on 1-minute bars vs ~53% on daily bars. The author of that math: "I never managed a significantly positive walk-forward test below 30-minute bars." [verified/promo-adjacent, against interest]

---

## Part 2 — AI/LLM track record, by sub-track

**(a) LLM as coding assistant — your plan.** Strongest use, zero verified track records *of the resulting systems*, which is expected: the LLM writes the harness, the edge still has to exist. Consensus across every credible source: "LLMs are components inside a system, not sources of alpha." The risk this track adds is industrialized overfitting (30,000-signal HARKing is now free) — see countermeasures in the exec summary. [verified consensus]

**(b) LLM as signal generator (news/sentiment → features).** Real but small: ~3.3%/yr at weak significance in the original Lopez-Lira work, concentrated in small caps, decaying with adoption per the author's own abstract; naive FinBERT-style sentiment is eliminated by costs (the BUZZ sentiment ETF trailed SPY by 15pp). The defensible architecture: **LLM extracts structured features → numeric features feed a gradient-boosted model → daily cross-sectional portfolio → forward-only evaluation**. [verified]

**(c) LLM as live decision-maker.** No credible positive evidence, multiple credible negatives: Alpha Arena real-money (4/6 models −30% to −59% in 2 weeks); StockBench (+2pp over passive, pre-costs, upturn-only long bias); the "Alpha Illusion" reproduction (TradingAgents net $102.3K vs buy-and-hold $104.8K); TradingAgents' own maintainer conceding non-reproducibility after a user found 2025 news leaking into a 2024 backtest; a frozen rulebook beating four frontier LLMs that rewrote their strategy daily (+15.6% vs +5.7% best LLM). Plus the safety case: an autonomous agent lost ~$440k notional in 72 hours to a social-engineering reply — the canonical argument for a **hard, non-LLM execution/risk layer** in anything you build. [verified]

**(d) Classical ML (GBM/random forests on tabular features).** The workhorse. Academic ML alpha (Gu-Kelly-Xiu Sharpe 2.45 equal-weighted) concentrates in microcaps retail can't trade at size; value-weighted it drops to 1.35 and costs take most of the rest. Honest planning number: **~50% haircut from any paper result**, worse for predictors with good "risk story" explanations (65% decay). [verified]

**(e) Reinforcement learning.** Zero retail live evidence anywhere in the corpus. FinRL's own contest results underperform the DJIA; its own papers concede the sim-to-real gap. Community issue trackers are dominated by "the demo notebook doesn't run." RL for *execution* (order slicing) is legitimate later; RL for *alpha* is a research trap. [verified]

---

## Part 3 — Market choice

Ranked for your profile (daily-bar frequency, small capital, low babysitting, US person):

1. **US equities/ETFs, daily bars, cash account — the learning venue.** Round-trip costs 0.2–0.5bps in liquid names. Free adequate data (daily bars $0; survivorship-free Norgate $630/yr only when you need it). Alpaca free API (IEX feed), IBKR $10/mo bundle (waived at $30 commissions). The **PDT rule is abolished** (FINRA 26-10, effective June 2026, phased through Oct 2027) — irrelevant anyway at daily frequency. Cash account = structurally cannot blow up.
2. **CME micro futures — the real-system venue.** MES round trip ~0.7–0.9bps; §1256 tax (60/40, mark-to-market, no wash sales, one line on Form 6781 — worth more than most edges for a high-frequency bot); data ~free with a funded NinjaTrader/Tradovate account. Least forgiving: leverage built in, **no negative-balance protection for US retail futures**. Go here after bugs have cost you money somewhere safer.
3. **Crypto — onshore derivatives only, and the 2026 story is genuinely new.** Offshore perps (Hyperliquid, Binance, Bybit) are contractually closed to US persons — Hyperliquid's geoblock verified live from this machine, with an explicit warranty against location-disguising. But **Coinbase Derivatives (CFTC-designated contract market, cleared at Nodal) now lists nano BTC/ETH perpetual-style futures with real liquidity** ($149M OI, ~$400–640M/day on the BTC perp), $0.10/side exchange fee (~9–10bps all-in round turn via IBKR), free self-serve API, 24/7, and a plausible §1256 tax reading. Kraken/Bitnomial is the second onshore route (16 perp markets) but had no working API for perps as of mid-2026. Never use Coinbase *spot* as an execution leg at small size (60bps taker at tier 0 — arithmetically dead); IBKR spot is 36bps round trip. Exchange-insolvency attrition continues (BitMEX closing 2026-09-23).
4. **Options — bad first bot.** Retail options flow lost $2.1B in 19 months in the cleanest study; defined-risk VIX-structure trades are the only entry that made the Top 20.
5. **Forex — avoid.** 68–89% of retail CFD/FX accounts lose (regulator-mandated disclosures); dealing-desk counterparty structure; the CFTC-mandated quarterly disclosures show ~two-thirds of accounts unprofitable *every quarter*.

**Realistic recurring budget: $0–45/mo** for everything in the Top 5 picks below. The data-cost lever is timeframe: daily bars are free-to-cheap everywhere; minute bars are $125–200/mo and push you toward strategies the cost math kills anyway.

---

## Part 4 — Who actually wins

- **Population base rates [verified]:** Taiwan (whole-market, 15 years): <1% of day traders predictably profitable net of costs; top 0.11% earn 38bps/day — skill exists, is persistent, and is astonishingly rare. Brazil (all new futures day traders, 2013–2015): 97% of >300-day persisters lost; **no learning effect** (experience did not improve results). US retail futures (CFTC): ~60% lose, median dabbler loses $100–200 and quits. Options: aggregate retail loss $2.1B in 19 months.
- **Algorithmic retail specifically [verified]:** the Quantopian 888 result (exec summary #1) is the anchor. Quantopian itself — 200,000 users, $250M committed, its own overfitting research — could not assemble a viable portfolio from crowdsourced retail algorithms and shut down in 2020. QuantConnect's Alpha Streams marketplace is also dead (404s, 2026). Two of the three serious retail-alpha marketplaces failed; that is itself a base rate.
- **Marketplace attrition [anon but specific]:** Collective2 futures strategies profitable at 24 months: 5.8% (19 of 325). Five-year survivors: ~19 against "thousands" failed, none with a clean annual record. Founder's own words: edges "inevitably tend to degrade as the markets discover whatever the strategy knows."
- **Numerai [verified — own API pull]:** median staked model +7.6% in NMR terms over 52 weeks — and **−37.8% in USD** (token fell 42%); payouts currently diluted to ~8.5% of raw scores by over-staking. A leaderboard truncated to the top 5,000 rows inflated the median ~4× — a live demonstration of why every marketplace leaderboard is unusable as a base rate.
- **Prop firms:** ~1–2% of challenge buyers ever receive a payout [anon]; verified 1-in-7 annual firm-closure rate, $50M+ in blocked payouts across 2024 closures [verified]. Not a shortcut; a fee funnel with counterparty risk.
- **The statistical trap that frames everything:** at the Sharpe you should actually expect (0.3–0.7 net), proving the edge exists takes **16–44 years** of live data on a single-signal strategy. You cannot validate a monthly-rebalance timing signal within a human timeframe. The only lever is **breadth** — cross-sectional strategies over hundreds of names generate independent bets (and therefore evidence) orders of magnitude faster. This is why the ranking rewards strategies that *learn fast about themselves*.
- **Calibrated dollar expectations:** at Sharpe 0.5 and 12% vol on $25k: **~$1,500/yr expected, ±$4,500 swings, losing years normal.** The honest case for this project is the one you already made: learning + a real system, with profit as a call option.

---

## The Top 20

**Ranking method:** expected value for your stated profile — build complexity weighted ~zero; heavy weights on recurring cost, capital at risk, edge durability into 2026+, and babysitting; a bonus for *evidence velocity* (how fast the strategy tells you whether it's working) and for learning value. "Tuition" entries are ranked on what they teach per dollar of expected loss.

**Fields:** What/Why · Evidence (strong/medium/anecdotal) · Expected outcome · Costs & capital · Biggest risk · Babysitting.

---

**1. Dual-momentum ETF trend/TAA with canary assets × US ETFs (cash account, daily/monthly bars)**
Long-only rotation across equity/bond/real-asset ETFs, risk-off via canary assets (BAA/HAA-family), monthly rebalance. Ranks #1 because it maximizes every one of your weights simultaneously: $0 recurring, unlevered (cannot blow up, only underperform — the design choice that dodges the #1 documented killer), durable mechanism, ~30 min/month. **Evidence: strong** (decades OOS, academic + practitioner; 2022 canary lesson incorporated). **Expected outcome:** market-like CAGR, materially lower drawdowns, 0–2%/yr excess; some multi-year stretches of trailing buy-and-hold. **Costs:** $0/mo; works from $5k. **Biggest risk:** whipsaw regimes (2022-style) eroding faith before the mechanism pays. **Babysitting: ~0.5 hr/wk.**

**2. Crypto carry measurement system → conditional perp-vs-basis trade × Coinbase Derivatives/CME (onshore)**
Phase 1: a bot that logs CDE's hourly funding table and the CME MBT settlement curve daily for 60–90 days and computes the realized perp-minus-dated spread net of the verified fee schedule. Phase 2 *only if* the ~5pp gross gap persists: short nano BTC perp vs long dated future (both §1256, same-clearinghouse margin offset possible). Ranks #2 on learning-per-dollar: real DCM, real clearinghouse, real funding mechanics, free API, **zero capital at risk in phase 1**, and it produces the one number that decides whether the trade exists. **Evidence: strong for the venue, none yet for the edge** (44-hour funding sample). **Expected outcome:** phase 1 — a dataset nobody publishes; phase 2 — 3–5% net *if* the spread is real, else you decline the trade having spent $0. **Costs:** $0–20/mo (VPS); phase 2 works from ~$10k. **Biggest risk:** treating the 44-hour funding snapshot as a regime; funding-payment tax characterization genuinely unsettled. **Babysitting:** 0 hr/wk phase 1; 2–4 hr/wk phase 2 (24/7 margin cycles).

**3. Volatility-targeting overlay × everything you run (ETFs/futures)**
Scale every position so the portfolio targets constant realized vol (e.g. 10–12%), cutting size as vol rises. Not alpha — but it's the only thing the best dataset says transfers out-of-sample, and it converts the strategies above from "hope the backtest holds" to "the risk promise will be kept." **Evidence: strong** (Quantopian vol R²=0.67; ubiquitous institutional practice). **Expected outcome:** similar returns, 20–40% smaller drawdowns, better realized Sharpe on everything it wraps. **Costs:** $0. **Biggest risk:** vol-scaling into a gap (it manages continuous risk, not jumps). **Babysitting: 0** (it's code inside other entries).

**4. Cross-sectional GBM on daily bars with LLM-extracted features × US equities (paper → small live)**
LLM reads filings/news/transcripts → structured numeric features → gradient-boosted model ranks a few hundred liquid names daily → long top decile (long-only first), forward-only evaluation from day one. The flagship "AI" build. Ranks #4 because breadth generates evidence fast (hundreds of independent bets/month vs 12/year for a timing signal) — the fix for the 16-to-44-year validation trap. **Evidence: medium** (LLM-feature alpha real-but-small and decaying; GKX caveat: paper alpha lives in microcaps — stay in liquid names and expect less). **Expected outcome:** most likely statistically flat net of costs; genuine shot at a thin real edge; the best evidence-generating machine on this list. **Costs:** $0–99/mo (Alpaca free tier → ATP); $10–25k live after ≥3 months paper. **Biggest risk:** contaminated evaluation (any backtest over the LLM's training window is fiction — forward-only, pre-registered). **Babysitting: 1–2 hr/wk.**

**5. Medium-horizon trend following (3–12mo TSMOM) × CME micro futures (start on ETFs)**
Classic diversified trend: 20–40 markets via micros, multiple lookbacks, vol-targeted sizing, weekly execution. The most durable *positive-expectancy* systematic edge in the academic record that retail can actually implement. Start with the ETF version (#1) and graduate here for §1256 tax and capital efficiency. **Evidence: strong** (century-scale TSMOM literature; ~0.4 Sharpe post-decay; Carver's live-published framework). **Expected outcome:** long-run Sharpe 0.3–0.5 net; multi-year flat stretches guaranteed. **Costs:** ~$0–15/mo data (funded-account feeds); realistically $15–25k+ to diversify micros. **Biggest risk:** leverage discipline — futures margin lets you oversize; trend crisis-alpha arrives late in gap events. **Babysitting: ~1 hr/wk.**

**6. Low-turnover factor tilts (value/momentum/quality blend) × US equities**
Monthly-rebalanced long-only portfolio tilted toward 2–3 factors with <50%/mo turnover, built from the free Open Source Asset Pricing data. **Evidence: strong for existence, medium for magnitude** (post-publication haircut ~50%; costs 2–4%/yr on naive implementations — low turnover is the whole game). **Expected outcome:** 0.5–2%/yr excess over index, slow evidence. **Costs:** $0/mo; $10k+. **Biggest risk:** decade-scale factor winters (value 2010–2020). **Babysitting: ~0.5 hr/wk.**

**7. LLM news-sentiment signal, forward-only × US small/mid caps (paper first)**
The Lopez-Lira track: LLM scores firm-specific news, daily cross-sectional portfolio. Kept separate from #4 because it's the purest test of "does LLM reading add alpha" — and the published edge is small, small-cap-concentrated (where your costs are worst), and decaying with adoption per its own author. **Evidence: medium.** **Expected outcome:** likely flat-to-thin net of costs; high research value as a #4 feature even if standalone fails. **Costs:** $0–50/mo (news API). **Biggest risk:** execution costs in small caps eating the entire gross edge. **Babysitting: 1 hr/wk.**

**8. CME quarterly BTC cash-and-carry (short MBT vs long spot) × CME + IBKR**
Short the quarterly future against spot at IBKR (36bps round trip), roll quarterly (~30bps/yr), collect the basis. **Evidence: strong** (verified curve: ~5.5–5.7% annualized, deeply arbitraged). **Expected outcome:** ~1.5–2% over T-bills — real, small, honest; a plumbing apprenticeship with positive carry. **Costs:** ~$0/mo; ~$9.6k minimum (one MBT unit + margin). **Biggest risk:** two-account margin fragility — spot gains can't meet futures margin calls; a fast rally forces manual cash moves. **Babysitting: 0.5–1 hr/wk, spiking on trend days.**

**9. Onshore perp funding carry (short nano BTC perp vs long spot) × Coinbase Derivatives**
The naive version of #2's phase 2. Included honestly: at verified retail fee tiers it returns ~3.1–4.9% against a 3.9–4.15% T-bill — **a T-bill with basis risk, mixed-straddle tax pain, and a 24/7 pager**. Ranks this high only because the plumbing skills transfer directly to #2. **Evidence: strong (all costs verified).** **Expected outcome:** ≈ cash; learning value real. **Costs:** $0–20/mo; $10–25k. **Biggest risk:** liquidation-cascade tail (Oct 2025: $19.3B liquidated; ADL closed *winning* legs while rejecting reduce-only orders). **Babysitting: 2–3 hr/wk.**

**10. Sell-in-May international seasonality tilt × global ETFs**
Halve international equity exposure May–October. The only calendar effect that survives modern data-mining correction, and only in the international cross-section. **Evidence: medium.** **Expected outcome:** noise-level improvement, maybe 0–1%/yr; two decisions a year. **Costs:** $0; any size. **Biggest risk:** it quietly joins its dead calendar siblings. **Babysitting: ~0 (10 min, twice a year).**

**11. VIX term-structure signal with defined-risk options × US options**
Trade the VX futures curve state (contango/backwardation) via defined-risk spreads only, small sleeve. **Evidence: medium** (volatility risk premium is real and structural; retail *implementations* mostly die — defined risk is the survival constraint). **Expected outcome:** modest positive expectancy punctuated by full-sleeve losses in vol spikes; sized so that's survivable. **Costs:** $0–25/mo; $5–10k sleeve max. **Biggest risk:** exactly the vol spike the premium pays you to insure. **Babysitting: 1–2 hr/wk.**

**12. Numerai tournament (unstaked → token-sized stake) × abstract equities**
Build models on their free obfuscated dataset; scoreboard = free out-of-sample grading of your ML pipeline. **Evidence: strong that the *platform* works; verified-terrible economics** — median staker −37.8% in USD last year (token depreciation), payouts diluted to ~8.5% by over-staking. **Expected outcome:** excellent ML calibration practice; roughly $0 income; stake only what you'd burn. **Costs:** $0. **Biggest risk:** NMR token risk swamping model skill. **Babysitting: ~0.5 hr/wk once automated.**

**13. Crypto trend on BTC/ETH × CME micro futures**
TSMOM (#5's logic) applied to the two liquid crypto majors via MBT/MET — clean venue, §1256, no exchange custody risk. **Evidence: medium** (crypto momentum profitable historically, decaying, two-instrument concentration). **Expected outcome:** high-variance version of #5; a diversifier inside #5 rather than standalone. **Costs:** ~$0; $10k+. **Biggest risk:** 70–80% asset-class drawdowns overwhelm any trend filter's exit speed. **Babysitting: ~0.5 hr/wk.**

**14. Long-side daily mean reversion (pullback-in-uptrend) × US equities with survivorship-free data**
Buy sharp 2–5-day pullbacks in uptrending liquid names, exit on bounce. The most-taught retail algo strategy; edge decayed hard post-2010 and the skew is brutal (many small wins, occasional catastrophic holds). **Evidence: medium-to-weak for 2026.** **Expected outcome:** roughly break-even net of costs; a good laboratory for slippage/fill modeling. **Costs:** $30/mo (Norgate) — the first entry where data is a real line item; $10k+. **Biggest risk:** the falling knife that doesn't bounce (single-name gap risk). **Babysitting: 1–2 hr/wk.**

**15. Marketplace publishing (Collective2 / Darwinex Zero) × your own strategies**
Publish a strategy for third-party-verified track record and commitment discipline — explicitly *not* income (C2: ~$100/mo listing + ~50% revenue cut; realistic DarwinIA outcome: a few hundred euros against hedge-fund-grade qualification gates). **Evidence: strong that it's not income** [verified/anon]. **Expected outcome:** an auditable track record and enforced discipline; net cost ~$100/mo. **Biggest risk:** optimizing the equity curve for subscribers instead of yourself — the documented death spiral of C2 leaders. **Babysitting: +0.5 hr/wk.** Only worth it once something has 12+ live months.

**16. PEAD / earnings-drift × US mid/large caps**
Buy positive-surprise names, hold weeks. In tradeable names the edge has decayed to insignificance; survives only in microcaps where costs eat it. **Evidence: strong that it's dead.** **Expected outcome:** flat; useful as a falsification exercise (rediscover the decay yourself with event-study tooling that transfers to #4). **Costs:** $0–30/mo; any size. **Biggest risk:** none material — that's the point; it just won't pay. **Babysitting: 0.5 hr/wk.**

**17. Order-book-imbalance features on CDE nano perp × crypto (research only)**
Microstructure imbalance signals had measurable, published edge on crypto perps — Sharpe 10.8 → 3.0 in two years, and profitable only at maker-rebate fee tiers you don't have. On CDE's flat $0.10/side there's no rebate to earn. **Evidence: medium (for the decay).** **Expected outcome:** negative expectancy if traded; genuine microstructure education if only researched against the free feed. **Costs:** $0–20/mo. **Biggest risk:** convincing yourself the backtest survives fees you can't actually get. **Babysitting: n/a as research.**

**18. Intraday opening-range breakout × MES (micro E-mini)**
Now legal for small accounts (PDT abolished) and the standard "funded trader" strategy. The cost math is the problem: retail breakeven win rates on sub-hourly bars sit near levels no verified system sustains. **Evidence: strong that retail intraday is negative-sum; anecdotal that outliers exist.** **Expected outcome:** slow bleed of commissions/slippage; teaches execution engineering fast. **Costs:** ~$0–15/mo; $5k+. **Biggest risk:** leverage — the one entry here where a bug or a fat tail produces a five-figure loss on a five-figure account (no negative-balance protection). **Babysitting: high — it trades when you're at work.** Tuition entry; ranked above #19–20 only for the execution skills it builds.

**19. Turn-of-the-month overlay × SPY — as a calibration exercise**
Hold SPY the last trading day through the third of the month; T-bills otherwise. Our verification killed it as an edge (post-2006 alpha +0.28%/yr, t=0.18, net negative after taxes) — it's in the Top 20 as the **best possible first harness test**: trivial data, four trades of logic, and a built-in lesson in why a 1926–2005 backtest with Sharpe "1.04" (actually 0.54, honestly computed) dies in subperiods. Build it, watch it do nothing, and you'll have calibrated your skepticism against every vendor page you'll ever read. **Evidence: strong (that it's dead).** **Expected outcome:** ≈0; permanent immunity to seasonality marketing. **Costs:** $0; any size. **Risk:** none if unlevered. **Babysitting: 5 min/mo.**

**20. Autonomous LLM trader (TradingAgents-style) × paper account only**
The thing this project is nominally about, ranked last as a *trading* strategy and included because you should run it once: multi-agent LLM debates → paper trades → forward-only scoring against a frozen-rules control and buy-and-hold. Every credible test says the control wins. **Evidence: strong (negative).** **Expected outcome:** underperforms its own baseline; produces the most instructive failure log in the project; ~$10–50/mo in API costs is the entire downside if you never wire it to real money. **Biggest risk:** promotion to real capital after a lucky month — pre-commit that it never touches a live account without 12+ months of forward outperformance vs its frozen control (which no published system has achieved). **Babysitting: 1 hr/wk.**

---

## Top 3 picks

**Pick 1 — Entry #1 (ETF trend/TAA) as the first real system.** It is the only entry that scores near-maximum on every constraint you set: zero recurring cost, no leverage (immune to the failure mode that kills the majority of documented dead strategies), a mechanism with decades of out-of-sample evidence, and a babysitting load measured in minutes. It will not make you rich and will sometimes trail buy-and-hold for uncomfortable stretches — but it gets a real system live end-to-end (data → signal → orders → monitoring → monthly report) with essentially no way to blow up while you learn. Everything harder inherits this harness.

**Pick 2 — Entry #2 (crypto carry measurement) as the best pure-learning build.** This is the standout discovery of the research spike: a CFTC-regulated, genuinely liquid onshore perp venue now exists, its funding prints hourly on a free public endpoint, nobody publishes the history, and the difference between its funding rate and the CME basis *is* the entire candidate edge. A logger + daily spread computation is a real production system (scheduling, data integrity, reconciliation, alerting) with zero capital at risk, and in 60–90 days it hands you a go/no-go number no amount of backtesting could. Measurement-before-position is also exactly the habit the Quantopian evidence says separates survivors.

**Pick 3 — Entry #4 (cross-sectional GBM with LLM-extracted features) as the flagship AI build.** This is where your actual advantage — building sophisticated pipelines cheaply with Claude — meets the strongest evidence-backed architecture: LLM as feature extractor, conventional ML as the decision layer, hard non-LLM risk rails, forward-only evaluation. Critically, its cross-sectional breadth is the only honest answer to the validation trap: hundreds of independent bets per month means that within a year you'll have *statistical evidence* about whether you have anything, instead of the 16–44 years a timing signal needs. Run it paper-first for a quarter; even a null result is a publishable-quality artifact.

Run all three in parallel: #1 is live capital (small), #2 is zero capital, #3 is paper. Combined babysitting ≈ 2–4 hrs/week. Combined recurring cost ≈ $0–40/mo.

---

## Avoid entirely

- **Offshore perps via VPN** (Hyperliquid/Binance/Bybit) — geoblocks verified live; location-disguising is an explicit ToS breach; a delta-neutral book that can be administratively closed isn't a book.
- **Naked short volatility / 0DTE income strategies** — negative net of costs in the best study; unbounded left tail.
- **Grid / martingale bots** — mathematically guaranteed eventual ruin dressed as a smooth equity curve; vendors survive by publishing only the surviving parameter sets.
- **Prop-firm challenges** — ~1–2% ever see a payout; 1-in-7 annual firm-closure rate; the business model is your evaluation fee.
- **Retail forex/CFDs** — 68–89% loss rates on regulator-mandated disclosures; dealing-desk conflict.
- **Triangular / cross-exchange crypto arb** — $12–17/week realizable at retail; needs ≤146ms execution.
- **AMM liquidity provision** — structurally negative (fees < LVR).
- **Sub-30-minute systems at retail cost structures** — breakeven win rates no real system sustains.
- **Copy trading as a strategy** — negative expectancy in every study that includes dead accounts.
- **RL for alpha** — zero live evidence; sim-to-real gap unsolved even by its own research community.
- **Autonomous LLM execution with real money** — every real-money test negative; social-engineering attack surface; keep LLMs out of the execution path.
- **Anything requiring paid courses/signals to learn** — the promo ledger in this corpus is long, and every "realistic returns" claim from a seller cross-read worse than its free academic equivalent.

---

## Source appendix (by evidence grade)

### [verified] — primary sources, regulators, or own replication
- Wiecki et al. 2016, "All That Glitters Is Not Gold" (Quantopian 888-algo IS/OOS study) — SSRN 2745220. The anchor result.
- McLean & Pontiff 2016, J. Finance — post-publication decay 26%/58%.
- Barber, Lee, Liu, Odean 2014 (Taiwan, whole-market); Chague et al. 2020 (Brazil, SSRN 3423101); CFTC OCE 2024 (US retail futures); ESMA CFD disclosures; Bryzgalova et al. 2023 (retail options, −$2.1B).
- Gu–Kelly–Xiu ML asset pricing; Falck–Rej–Thesmar OOS haircuts; Chen & Velikov 2022 (post-cost anomaly returns ~4bps/mo); Open Source Asset Pricing dataset (own decay computation: 53% mean post-publication decay across 212 signals).
- Han, Han & Tian 2025, "The disappearing turn-of-month effect," Finance Research Letters + **own replication** from raw ^GSPC/^IRX data, 1950–2026 (scripts preserved) + Zakamulin 2026 bootstrap.
- Lopez-Lira & Tang (LLM news signal); Alpha Arena real-money results; StockBench; "Alpha Illusion" (arXiv 2605.16895); TradingAgents GitHub issues #168/#225 and maintainer's reproducibility concession; molbal/trading-llm-experiment (9.12% directional accuracy — open negative result); Apollo Research deceptive-trading paper.
- Coinbase Derivatives: CFTC DCM registry, rulebook Rule 1129, fee schedules (PDFs), live API pulls (specs, OI, volume, funding — 1,293 hourly rows), help-center funding methodology. CME MBT specs/margins/settlement curve. IBKR commission & crypto fee schedules. Hyperliquid ToS §1.6/§1.9 fetched live. 26 U.S.C. §1256 text. IRS digital-assets page. Treasury daily yield curve. CFTC v. Binance (2023), CFTC DeFi orders (Opyn/ZeroEx/Deridex).
- Numerai tournament API (16,620 models, own population pull + USD arithmetic); CFTC Reg 5.5(e) forex disclosures (OANDA, tastyfx); FINRA 26-10 (PDT abolition); Vilkov (condor costs); Quantopian/QuantConnect-Alpha-Streams shutdowns.
- GitHub ecosystem telemetry: freqtrade (Edge module removed), FinRL issue tracker, Zenbot race conditions, backtrader abandonment — all from live `gh api` pulls.

### [anon] — plausible practitioner accounts, unaudited
- Collective2 forum archive: 5.8%-at-24-months attrition table; ~19 five-year survivors; founder's decay concession; 2025 martingale open letter. HN "Ask HN: algorithmic trading" (2018) practitioner consensus; Elite Trader dom993's "200 live trades is no guarantee"; QuantConnect live-vs-backtest divergence threads; the freqtrade 3-year/100-strategy null-result blog; dev.to Polymarket MM build log (0.17% fill rate); smdz's 5–8 hr/day time-cost account.
- Reddit: **not collected** — the archive API was down/saturated for the entire research window across four independent attempts. Pattern-level recollections were used nowhere in the rankings.

### [promo] — sellers; used only where against interest or cross-verified
- Quantpedia (TOM backtest — the page our verification dismantled; sectoral intramonth momentum), Robot Wealth (Sharpe 1.0–1.5 claim; founder's own "$10k→$25k was luck" admission), Ernie Chan (decay taxonomy), Financial Hacker (scalping cost math + own EUR/CHF blowup — against interest), QuantStart, Alpha Architect (2–4%/yr factor implementation costs), Darwinex/C2 marketing, traderspost "60% profitable" (contradicted by every dataset; cited as an example of the genre), Kevin Davey (contest results third-party verified; teaching promo).

---

## Gaps & next steps

1. **Reddit practitioner sweep never ran** — Arctic Shift API was down/saturated throughout. Worth one retry on a quiet day; it's texture, not load-bearing.
2. **CDE funding persistence is the live question** — 44 hours of data ≠ a regime. Entry #2 phase 1 answers it for $0.
3. **Unresolved cost items:** whether Coinbase Financial Markets pays interest on futures margin (worth ~91bps of the carry trade); professional market-data fee classification for automated accounts; Coinbase Advanced spot tier confirmation.
4. **Unresolved tax items:** §1256 treatment of perp *funding payments* (the entire carry return); whether 2025–26 legislation extended wash-sale rules to digital assets. Needs a practitioner before real size in entry #2/8/9.
5. **Unverified figures stripped from rankings:** OKX $505M DOJ settlement, "14,000 accounts closed for geolocation fraud," prop-firm "7% payout" origin — all uncited in any primary source we could reach; none load-bearing above.
6. **Suggested phase 2:** pick the three parallel builds (top 3 picks), define the pre-registration template (hypothesis, universe, costs, kill criteria — written *before* the first backtest), and stand up the shared harness: data ingestion, signal, paper/live execution via Alpaca + IBKR, and a nightly report.

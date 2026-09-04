# Gap-1 Verification: Does the calendar-seasonality edge survive for a solo retail trader in 2026?

**Assignment:** independently verify or refute the turn-of-the-month (TOM) / calendar-seasonality edge that `strat-classic.md` ranks #1 ("Build first. Best ratio on the list.", "High durability — flow-driven, no decay observed").

**Answer up front: refuted.** The effect is real in the historical record, published repeatedly, and **statistically dead in US equities after roughly 2001**. This is not my inference alone — there is a 2025 peer-reviewed paper whose title is literally "The disappearing turn-of-month effect," and I independently reproduced its result from raw price data. The #1 ranking rests on a vendor page reporting a **1926–2005** backtest that the sibling report presented as if it were a current edge.

Evidence tags: `[verified]` = I fetched a primary source (paper abstract via publisher/RePEc, dataset, raw price data) and can cite it; `[anon]` = unaudited forum/blog; `[promo]` = source sells something; `[own]` = my own computation from raw data in this session, scripts on disk.

---

## 1. Audit of the source the #1 ranking rests on

The single citation is Quantpedia's SPY turn-of-the-month strategy page (https://quantpedia.com/strategies/turn-of-the-month-in-equity-indexes) `[promo]` — Quantpedia sells a subscription strategy database. I fetched it. What it actually says `[verified, promo]`:

- **Rule:** buy SPY at the close one day before month-end, sell at the close of the third trading day of the following month — the McConnell–Xu **(-1, +3)** window.
- **Backtest period: 1926–2005.** Not 2026. Not even 2010. The sibling report cited a twenty-year-stale backtest as evidence of a live edge and paired it with "no decay observed."
- **CAGR 7.2%, Sharpe 1.04, max DD −20.79%, volatility 6.9%.**
- **Returns are computed "without cash (during days not invested in market)"** — Quantpedia's own wording. No T-bill is credited on the ~81% of days out of market.
- Source paper: McConnell & Xu, *Equity Returns at the Turn of the Month*.

Two things follow immediately.

**(a) The Sharpe ratio is not a Sharpe ratio.** 7.2 / 6.9 = 1.043 ≈ the reported 1.04. The number is CAGR ÷ volatility with the risk-free rate set to zero, over a 1926–2005 sample in which T-bills averaged roughly 3.5–4%. `[own]` arithmetic on `[promo]` inputs. A genuine excess-return Sharpe over that period is far lower; my own reconstruction (§3) puts the honest full-sample Sharpe at **0.54**, not 1.04.

**(b) The "~20% time in market" selling point cuts the other way once cash is credited.** Because Quantpedia credits zero interest, their 7.2% understates what the strategy would actually have earned (add T-bills on 81% of days) *and* their volatility/Sharpe overstates the risk-adjusted quality (no rf subtraction). These two errors do not cancel; they push in opposite directions on different statistics, which is why you have to rebuild it rather than adjust it.

The claim that TOM has "shown no clear sign of decay since its initial publication" appears **nowhere on the Quantpedia page I fetched** and is unsourced in `strat-classic.md`. I could not locate any primary source for it. Marked **unverified and, per §2–§3, false**.

---

## 2. The primary academic record, and the decay paper nobody found

**Origin.** Ariel (1987), "A monthly effect in stock returns," *Journal of Financial Economics*, DOI 10.1016/0304-405X(87)90066-3 `[verified]` (citation confirmed via Crossref). Lakonishok & Smidt (1988), "Are Seasonal Anomalies Real? A Ninety-Year Perspective," *Review of Financial Studies* 1(4):403, DOI 10.1093/rfs/1.4.403 `[verified]`. A contemporaneous skeptic exists and is rarely cited: Jaffe & Westerfield (1989), "Is there a monthly effect in stock market returns?", *Journal of Banking & Finance*, DOI 10.1016/0378-4266(89)90062-9 `[verified]`.

**The canonical paper.** McConnell & Xu (2008), *Financial Analysts Journal* 64(2), DOI 10.2469/faj.v64.n2.11. Abstract, verbatim in relevant part `[verified]`: "The turn-of-the-month effect in U.S. equities is found to be so powerful in the **1926–2005** period that, on average, investors received no reward for bearing market risk except at turns of the month… it occurs in 31 of the 35 countries examined. Furthermore, **it is not caused by month-end buying pressure as measured by trading volume or net flows to equity funds.** This persistent peculiarity in returns remains a puzzle in search of an answer."

This is important and the sibling report gets it backwards. `strat-classic.md` argues the edge is durable *because* "the mechanism (month-end structural cash flows) is a flow effect, not a mispricing, which is why arbitrage hasn't closed it." **The canonical paper explicitly tested and rejected the fund-flow explanation.** McConnell & Xu called it an unexplained puzzle. Building a durability argument on a mechanism the source paper ruled out is the weakest link in the whole ranking.

**The flow mechanism does have a serious paper behind it**, but a different one: Etula, Rinne, Suominen & Vaittinen, "Dash for Cash: Monthly Market Impact of Institutional Liquidity Needs," *Review of Financial Studies* 33(1):75–111 (2020), DOI 10.1093/rfs/hhz054 `[verified]` (abstract via RePEc, https://ideas.repec.org/a/oup/rfinst/v33y2020i1p75-111..html). It documents month-end payment-cycle patterns globally and "investigate[s] the limits to arbitrage that prevent markets from functioning efficiently." Note the editorial dates in the abstract: **received January 2018, accepted January 2019** — the evidence base predates the period in question, and the paper's own framing is about *costs borne by institutions*, not a retail-tradeable index-timing edge.

### The paper that settles it

**Han, Han & Tian (2025), "The disappearing turn-of-month effect," *Finance Research Letters* 71:106461, DOI 10.1016/j.frl.2024.106461** `[verified]` — abstract obtained verbatim via RePEc (https://ideas.repec.org/a/eee/finlet/v71y2025ics1544612324014909.html) and independently via CoLab; ScienceDirect and SSRN both refused fetch (Cloudflare/403), so I did not read the full text — **the abstract is verified, the internal tables are not.**

> "We document that the turn-of-the-month (TOM) effect, historically a highly significant regularity where the market yields higher returns around the turn of the month, **disappears entirely after 2001**. The liquidity-based explanation proposed by Ogden (1990) no longer holds over the past two decades. We hypothesize and provide evidence that the **drastic reduction in transaction costs after 2001** likely diminishes the TOM effect, by enabling arbitragers to trade against it more effectively and allowing investors to trade more frequently rather than concentrating their activity at the end of the month."

Yufeng Han (UNC Charlotte) is an established asset-pricing author; FRL is a Q1 journal (impact factor 7.1 per CoLab metadata). The paper has 3 citations as of this session — recent but not fringe.

The mechanism matters for the ranking. Decimalization and the collapse of retail commissions **removed the friction that created the pattern**. That is a one-way structural change, not a cyclical lull. It cannot un-happen.

**Corroborating older work:** Marquering, Nisser & Valla (2006), "Disappearing anomalies: a dynamic analysis of the persistence of anomalies," *Applied Financial Economics*, DOI 10.1080/09603100500400361 `[verified]`: "strong evidence is found that the weekend effect, the holiday effect, **the time-of-the-month effect** and the January effect have disappeared after these anomalies have been published." Also Wong, Agarwal & Wong (2006) on Singapore `[verified]` (calendar anomalies "largely disappeared"), and Irtiza, Khan & Baig (2021), *Future Business Journal*, DOI 10.1186/s43093-021-00087-4 `[verified]`: in Pakistan TOM "is significant only during 2013–2016, while it vanishes for 2017 and 2018."

---

## 3. My own replication (the part I can fully stand behind)

I refused to rest this on abstracts. I pulled **S&P 500 daily closes from Yahoo Finance (`^GSPC`), 1950-01-03 → 2026-08-27, 19,285 bars**, and **13-week T-bill yields (`^IRX`), 1960 → 2026**, and rebuilt the strategy. `[own, verified data]` Scripts: `.../scratchpad/research/gap1/tom.py` and `sim.py`.

Definition: TOM = **(-1, +3)**, the last trading day of the prior month plus the first three trading days — exactly Quantpedia's rule. That is 4 days ≈ **19.1% of trading days**, matching their "~20% time in market."

### 3a. Raw day-level effect, price index, no cash, no costs

| Period | TOM day (bp) | t | Other days (bp) | **diff t** | Window-only CAGR | Buy&hold CAGR |
|---|---|---|---|---|---|---|
| 1950–2026 (full) | 11.14 | 6.97 | 1.92 | **5.16** | 5.26% | 8.35% |
| 1950–1986 (pre-Ariel) | 13.58 | 7.23 | 0.73 | **6.18** | 6.59% | 7.53% |
| 1987–2001 (post-pub) | 15.23 | 3.97 | 2.24 | **3.01** | 7.30% | 10.91% |
| 1950–2005 (≈Quantpedia sample) | 13.43 | 7.87 | 1.12 | **6.48** | 6.47% | 8.03% |
| **2002–2026** | **4.98** | 1.49 | 3.51 | **0.39** | 2.09% | 8.06% |
| **2006–2026** (OOS vs. QP backtest) | **4.92** | 1.33 | 4.10 | **0.20** | 2.06% | 9.25% |
| **2016–2026** | **6.68** | 1.41 | 5.35 | **0.25** | 2.98% | 13.34% |

The pre-2002 numbers reproduce the literature (my 1950–2005 window-only CAGR of 6.47% brackets Quantpedia's 7.2% on 1926–2005 — different start, different index, same ballpark, which validates the method). **Post-2001 the difference between TOM days and every other day is t = 0.39.** In 2016–2026 it is t = 0.25. There is no effect left.

### 3b. Honest strategy: T-bills credited out of market, alpha vs. a beta-matched benchmark

This answers the brief's exact questions. Strategy = long index on TOM days, 13-week T-bill otherwise. Alpha and beta from regressing strategy excess return on market excess return (so the benchmark *is* the ~0.18-beta mix of index and cash, not buy-and-hold). Sharpe is a real excess-return Sharpe on the **full calendar**, not on the 19% of days invested.

| Period | Strat CAGR | Mkt CAGR | Cash CAGR | Strat vol | **Sharpe (strat)** | Sharpe (mkt) | beta | **alpha** | **t(alpha)** |
|---|---|---|---|---|---|---|---|---|---|
| 1960–2026 | 8.01% | 7.58% | 4.32% | 6.96% | **0.54** | 0.27 | 0.182 | **+2.96%** | **3.79** |
| 1960–1986 | 10.19% | 5.33% | 6.28% | 5.71% | 0.66 | −0.01 | 0.203 | +3.87% | 3.87 |
| 1987–2001 | 11.80% | 10.91% | 5.21% | 7.17% | 0.88 | 0.39 | 0.174 | +5.29% | 3.07 |
| **2002–2026** | 3.48% | 8.06% | 1.68% | 8.00% | **0.26** | 0.41 | 0.177 | **+0.68%** | **0.46** |
| **2006–2026** | 3.43% | 9.25% | 1.67% | 8.09% | **0.25** | 0.47 | 0.175 | **+0.47%** | **0.29** |
| **2016–2026** | 4.84% | 13.34% | 2.23% | 7.46% | **0.37** | 0.67 | 0.174 | **+0.73%** | **0.35** |

Findings that directly answer the brief:

- **Does the Quantpedia backtest credit T-bill interest? No** (their own wording, §1). Crediting it raises the full-sample CAGR from ~6.5% to **8.01%** — but this flatters the *level*, not the *edge*: cash return is not alpha.
- **Sharpe on the full calendar, properly computed: 0.54 full-sample, not 1.04.** Post-2001 it is **0.26, below the market's own 0.41**. The strategy is now a worse risk-adjusted holding than just owning the index.
- **Alpha vs. a beta-matched benchmark: +2.96%/yr full sample (t=3.79) → +0.47%/yr since 2006 (t=0.29).** The realized beta is 0.175–0.182 across every subperiod, so the "0.2-beta benchmark" framing in the brief was exactly right.
- **Round-trip costs are trivial and confirm as expected.** Adding 1.5 bp per round trip (SPY half-spread each way; SPY quotes ~1 cent on a ~$650 price ≈ 1.5 bp round trip) over 12 round trips/year costs ~18 bp/yr: 2006–2026 alpha falls from 0.47% to **0.28% (t=0.18)**; 2016–2026 from 0.73% to 0.54%. Costs are not what killed it — but they are now the same order of magnitude as the entire remaining edge.

*Caveats on my own work, stated plainly:* `^GSPC` is a **price index**, so dividends are excluded from both the strategy leg and the benchmark leg. Because the strategy holds 19.1% of days and the benchmark leg carries beta 0.177, the dividend omission biases alpha by roughly +0.03%/yr — negligible. T-bill discount yields from `^IRX` are converted to daily compounding as an approximation. t-statistics are OLS, not Newey–West; daily index returns have negligible autocorrelation so this is unlikely to matter materially, but I did not test it. A real SPY total-return series would be marginally better.

### 3c. The multiple-testing knob, quantified

The brief asked how many window variants exist and whether any were reported. Quantpedia reports **one**. I tested **16** and report all of them. Alpha and t(alpha) vs. beta-matched benchmark: `[own]`

| Window | 1960–2001 alpha / t | **2002–2026 alpha / t** |
|---|---|---|
| (−1,+1) | 2.02% / 3.03 | 0.64% / 0.57 |
| (−1,+2) | 3.12% / 3.94 | 1.06% / 0.81 |
| **(−1,+3) ← published** | **4.34% / 4.87** | **0.68% / 0.46** |
| (−1,+4) | 4.21% / 4.38 | 0.31% / 0.19 |
| (−1,+5) | 3.86% / 3.79 | −0.07% / −0.04 |
| (−2,+2) | 3.35% / 3.75 | 2.06% / 1.39 |
| (−2,+3) | 4.57% / 4.71 | 1.68% / 1.05 |
| (−3,+2) | 3.34% / 3.45 | 2.51% / 1.56 |
| (−3,+3) | 4.56% / 4.43 | 2.12% / 1.24 |
| **(−4,+3) ← best post-2001** | 4.69% / 4.39 | **4.03% / 2.21** |
| (−4,+4) | 4.56% / 4.15 | 3.65% / 1.93 |
| (−5,+5) | 3.04% / 2.69 | 2.46% / 1.27 |
| (0,+1) | 0.94% / 1.94 | 1.27% / 1.39 |
| (0,+3) | 3.24% / 4.10 | 1.31% / 0.97 |
| (−1,0) | 1.06% / 2.24 | −0.62% / −0.90 |
| (−2,0) | 1.29% / 1.95 | 0.37% / 0.35 |

Read this carefully, because it is the whole trap. In **1960–2001 every single window works** (13 of 16 with t > 2.5) — that is what a real effect looks like: robust to definition. In **2002–2026 the published window is dead (t=0.46)** and the *best of 16 searched windows* reaches t = 2.21. Sixteen heavily overlapping tests; a nominal t of 2.21 is unremarkable after any data-mining adjustment. If you build this and it "works," you will have found (−4,+3) by searching, which is precisely the failure mode.

This is exactly what Quantpedia's own caveat warns about — "calendar effects tend to vanish or rotate to different days in a month" `[promo]`, quoted in `strat-classic.md` and then ignored by it. My table shows the rotation is **noise**, not a migrating signal.

### 3d. Corroboration from the formal data-mining literature

**Zakamulin (2026), "Calendar anomalies: Real patterns or data-mining artifacts?", *North American Journal of Economics and Finance* 85:102653, DOI 10.1016/j.najef.2026.102653** `[verified]` — abstract via RePEc (https://ideas.repec.org/a/eee/ecofin/v85y2026ics1062940826000756.html); ScienceDirect 403'd, so full text unread. Zakamulin applies "data-mining-adjusted bootstrap tests that mimic a researcher's within-family search across alternative calendar definitions" — i.e. formally what I did by hand above. Result, verbatim: day-of-week, **week-of-the-month**, and month-of-year "remain statistically significant in the full sample, with the strongest evidence coming from the earlier part of the sample… At the same time, we find that **these anomalies largely disappear in later subsamples beginning in the early 1990s.**" Sell-in-May internationally is the one survivor.

Three independent methods — Han et al.'s subperiod test, Zakamulin's bootstrap, and my own replication — converge on the same break somewhere between the early 1990s and 2001.

---

## 4. The Open Source Asset Pricing dataset: what it does and does not settle

I downloaded Chen & Zimmermann's `SignalDoc.csv` (331 signals) and `PredictorSummary2024.xlsx` from https://github.com/OpenSourceAP/CrossSection and computed the decay statistics myself. `[verified data, own computation]`

**First, a structural finding the brief anticipated but did not confirm: OP contains no turn-of-the-month signal at all.** OP is a *cross-sectional* predictor library — it ranks stocks against each other. TOM is a *time-series market-timing* effect. The brief called OP "the cleanest available decay test" for TOM; it is not, because TOM is out of scope for it. That is why §3 mattered — I had to build the test.

**What OP does contain is cross-sectional seasonality**, and it decays hard. Monthly long-short returns, in-sample vs. post-publication, computed by me from the OP files `[own]`:

| Signal | Pub | In-samp %/mo (t) | Post-pub %/mo (t) | Decay |
|---|---|---|---|---|
| MomSeasonShort (Heston & Sadka 2008) | 2008 | 1.36 (8.63) | 0.06 (0.19) | **−96%** |
| MomSeason | 2008 | 0.81 (5.85) | 0.11 (0.35) | **−86%** |
| DivSeason (Hartzmark & Salomon 2013) | 2013 | 0.33 (14.58) | 0.08 (1.86) | −76% |
| MomSeason06YrPlus | 2008 | 0.74 (6.16) | 0.23 (0.96) | −69% |
| MomSeason11YrPlus | 2008 | 0.75 (6.95) | 0.23 (1.11) | −69% |
| MomOffSeason16YrPlus | 2008 | 0.36 (2.58) | 0.12 (0.54) | −67% |
| MomOffSeason | 2008 | 1.31 (4.94) | 0.58 (1.28) | −56% |
| Mom12mOffSeason | 2008 | 1.23 (3.85) | 0.86 (1.32) | −30% |
| MomSeason16YrPlus | 2008 | 0.59 (5.05) | 0.52 (2.59) | −12% |
| MomOffSeason06YrPlus | 2008 | 0.59 (4.36) | 0.76 (2.82) | +29% |

**9 of 11 seasonality signals have post-publication |t| < 2.** Subgroup mean falls 0.755 → 0.332 %/mo, a **ratio of 0.439**.

For calibration, across all **212** OP long-short signals I compute mean in-sample **0.690 %/mo → post-publication 0.324 %/mo, ratio 0.470** (53% decay), and an intermediate "post-sample but pre-publication" mean of 0.427 (38% decay). `[own]` That is McLean & Pontiff's shape reproduced from the free data — and **seasonality decays slightly worse than the average anomaly (0.439 vs 0.470), not better.** The sibling report's "unusually resistant to decay" claim is contradicted by the only clean dataset that speaks to it.

**Capstone:** Chen & Velikov (2022), "Zeroing In on the Expected Returns of Anomalies," *JFQA*, DOI 10.1017/s0022109022000874 `[verified]` (abstract via OpenAlex): accounting for effective bid–ask spreads, post-publication effects, and "**the modern era of trading technology that began in the early 2000s**," across 204 anomalies "the average anomaly's expected return is a measly 4 bps per month. The strongest anomalies net, at best, 10 bps after controlling for data mining." Their structural break is the *same* early-2000s break Han et al. identify as the cause of TOM's death. Two literatures, one mechanism.

---

## 5. The fresh, unreplicated 2026 claim

`strat-classic.md` cites "Nathan, Suominen & Tasa (2026)" for an intramonth momentum cycle, $1 → $18.78 vs $2.37, and tags it `[verified]`. I traced it.

**The paper exists:** Daniel Nathan (Hong Kong Polytechnic), Matti Suominen and Joni Tasa (Aalto), "The Intramonth Momentum Cycle," **SSRN working paper 6426026**, DOI 10.2139/ssrn.6426026, 2026, **0 citations** `[verified via OpenAlex]`. **SSRN is Cloudflare-gated and I could not read the paper or its abstract; no OA copy exists (Unpaywall: closed, no repository copy). Everything below about its contents comes from Quantpedia's summary, not from the paper.** Note the author overlap: Suominen is also an author of the "Dash for Cash" paper — the same research group, extending its own prior mechanism.

**The route by which the numbers reached the sibling report is a Quantpedia blog post** (https://quantpedia.com/sectoral-intramonth-momentum-cycle/) `[promo]`, which is itself promoting Quantpedia's *own* derivative SSRN paper: Vojtko & Dujava, "Sectoral Intramonth Momentum Cycle Exploiting Turn-of-the-Month Patterns in Sector ETF Strategies," SSRN 7313598 `[verified via OpenAlex]` — Radovan Vojtko is Quantpedia's CEO. So the chain is: unread working paper → vendor blog promoting the vendor's own paper → sibling report, tagged `[verified]`. It should be `[promo]`.

What Quantpedia's page reports about the original `[promo]`: value-weighted winners-minus-losers on **individual US equities**, 1980–2025, six trading days per month ending four days before month-end; "77% of momentum's cumulative return is earned in those six days, which comprise only 29% of the trading month"; reproduced across 19 developed markets.

**Four things the sibling report should have flagged:**

1. **This is not a cheap seasonality overlay — it is a momentum long-short in single stocks.** $18.78 requires running a value-weighted WML book: long winners, *short losers*, rebalanced monthly. That is a completely different cost, margin, borrow and babysitting profile from "buy SPY for four days." Putting it under a "$0 data, $0 infra, 5 min/month" heading is a category error.
2. **$18.78 is not a discovery of free money.** $18.78 × $2.37 ≈ 44× over 45 years ≈ **9.5%/yr gross** for the whole WML portfolio — roughly the known momentum premium. The paper redistributes when momentum earns its return; it does not create a new one.
3. **Transaction costs: unknown for the original; explicitly absent from the vendor's version.** Quantpedia's own sectoral ETF extension states "no explicit transaction cost assumptions."
4. **Quantpedia's own tradeable version is far less impressive than the headline.** Nine sector SPDRs + SPY, Dec 1998 – Jun 2026: **long-short 5.99% annualized, Sharpe 0.55, max DD −21.7%**; market-neutral **3.77%, Sharpe 0.54, −14.7%** `[promo]` — gross of all costs. A Sharpe of ~0.55 before costs, from the vendor's own promotional backtest, is the honest ceiling here.

**Verdict on this strand: fresh, unread by me, unreplicated (0 citations), promoted by an interested party, and materially misrepresented in the ranking.** It is a research lead, not a build candidate.

---

## 6. Halloween / Sell-in-May and January — resolving the contradiction

The sibling report asserted without citation that "after controlling for fund flows, both Sell-in-May and the January effect become insignificant." **I found the paper.**

**Wagner, Lee & Margaritis (2022), "Mutual fund flows and seasonalities in stock returns," *Journal of Banking & Finance*, DOI 10.1016/j.jbankfin.2022.106623** `[verified]`, abstract verbatim: "We propose a flow-based explanation for two long-standing anomalies in empirical finance – Sell in May and the January effect. We find that mutual fund flows exhibit similar seasonal patterns as stock returns. **After controlling for fund flows both calendar effects become insignificant.** … return seasonality is due to unanticipated fund flow driven by uninformed (flow-motivated) retail investor trading."

Weigh this against Zakamulin (2026) `[verified]`, which after data-mining correction finds January "largely disappear[s] in later subsamples beginning in the early 1990s" but that **Sell-in-May international evidence "remains robust to data-mining concerns."**

**Resolution:** January is finished — both papers agree, from different angles. Sell-in-May is the one calendar effect with a live case, and only in the *international* cross-section, not US-only. Note the strategic irony: Wagner et al.'s flow explanation is a *deflation* of the effect (it is not alpha, it is exposure to retail flow), yet `strat-classic.md` invokes flow mechanics as the *reason for durability*. Both cannot be true. And Curto, Oliveira & Matilde (2014) `[verified via OpenAlex`, ISCTE repository] find the Halloween effect "has disappeared after the Bouman and Jacobsen" publication in European equity mutual funds — the standard post-publication pattern again.

---

## 7. Execution venue — and where TOM is still alive

**SPY / equity ETFs.** Confirmed above: the venue is not the problem. 12 round trips/year at ~1.5 bp costs ~18 bp/yr, which would be nothing against a 3% edge and is fatal against a 0.3% one. `[own]`

**CME Micro E-mini S&P 500 (MES).** I attempted to fetch CME contract specs and IBKR futures commissions; **both timed out or returned 403 — I could not verify current multipliers or fee schedules and will not quote them from memory.** Marked **unverified**. Directionally it does not matter: futures would let you express the same view with less capital, but there is no view left to express. Futures also convert the tax position (see below) and add roll and overnight-margin babysitting for a strategy whose measured alpha is statistically zero.

**Where TOM does still appear — and why that is consistent with it being dead in SPY.** Árendáš & Kotlebová (2019), *IJFS* 7(4):57, DOI 10.3390/ijfs7040057 `[verified]`: a significant TOM effect in **7 of 11 Central and Eastern European markets, 1999–2018**. Árendáš & Kotlebová (2023), *Agricultural Economics*, DOI 10.17221/17/2023-agricecon `[verified]`: TOM significant in **3 of 8 agricultural commodities** (rice, coffee, sugar), 2001–2021 — but note they tested "three different alternatives of the ToM window," i.e. 24 tests for 3 hits, roughly what chance delivers.

This is the Han et al. mechanism confirmed from the other direction: **TOM survives where transaction costs are still high** (illiquid CEE markets, thin ag futures) and is extinct where they collapsed (US large-cap index). Those are exactly the venues a solo retail developer cannot cheaply or safely trade — the effect has retreated to where you can't reach it. That symmetry is the strongest argument that the decay is real and structural rather than a run of bad luck.

**Practitioner evidence:** I searched Reddit (r/algotrading, r/quant, r/investing and others) for TOM trading experience and **found essentially no substantive retail discussion** — no success reports, no blowup stories. Weak, mostly-absence-of-evidence, marked `[anon, null result]`. It is consistent with a strategy nobody bothers to run, but proves nothing.

---

## 8. Tax drag — the item that flips the sign in a taxable account

Not verifiable from a source; this is arithmetic, stated so you can check it. `[own]`

The strategy generates **12 round trips per year, all held 4 days, all short-term capital gains**, realized annually. A buy-and-hold SPY position defers gains indefinitely. At a US federal marginal rate of 32–37% plus 3.8% NIIT plus state, call it ~35–40% on realized short-term gains versus ~0% deferred.

Post-2005 the strategy's *gross* return is ~3.4%/yr (§3b) of which ~1.7% is T-bill interest (taxed as ordinary income either way) and ~1.7% is equity gain. Taxing that equity gain annually at short-term rates instead of deferring it costs roughly **0.5–0.7%/yr** relative to holding. That is **larger than the entire measured post-2005 alpha of 0.28–0.47%**. In a taxable account the strategy has a **negative expected net edge**. In an IRA the tax point vanishes and you are left with an alpha statistically indistinguishable from zero.

---

## 9. What I could not verify

Stated explicitly so nothing here is over-claimed:

- **Full texts of Han, Han & Tian (2025) and Zakamulin (2026)** — ScienceDirect returned 403; no OA copies exist. I have their abstracts verbatim from RePEc and CoLab. Their internal tables, exact subperiod coefficients and robustness checks are **unread**.
- **Nathan, Suominen & Tasa (2026)** — SSRN is Cloudflare-gated; I did not bypass it. I have the title, authors, affiliations and DOI from OpenAlex only. Everything about its methodology in §5 is **Quantpedia's characterization**, not the paper's.
- **CME MES contract specs and IBKR futures commissions** — fetch failures; no figures quoted.
- Quantpedia's exact index series and dividend treatment for their 1926–2005 backtest.
- My replication uses `^GSPC` price returns, not SPY total returns; see the caveats in §3b.

---

## VERDICT

**No. Turn-of-the-month / calendar seasonality should not hold the #1 slot, and on edge-durability grounds it does not belong in the top ten.** The #1 ranking rested on a single vendor page reporting a **1926–2005** backtest with the risk-free rate set to zero (which inflates the quoted 1.04 Sharpe to roughly double its honest value of ~0.54) and no interest credited on the 81% of days out of market — paired with an unsourced "no decay" assertion that is contradicted by a 2025 peer-reviewed paper titled "The disappearing turn-of-month effect," by Zakamulin's 2026 data-mining-adjusted bootstrap, by the free Open Source Asset Pricing data where seasonality signals decay *worse* than the average anomaly (ratio 0.439 vs 0.470), and by my own replication from raw S&P 500 daily data. The durability argument was also built on a flow mechanism that the canonical source paper (McConnell & Xu 2008) explicitly tested and rejected. **Honest expected net edge on the published (−1,+3) SPY window: +0.28%/yr after 1.5 bp round-trip costs over 2006–2026, with t = 0.18 — a 95% confidence interval of roughly −2.9% to +3.5%/yr, i.e. indistinguishable from zero and straddling it symmetrically.** In a taxable account the ~0.5–0.7%/yr short-term-gains drag from 12 forced annual realizations makes the expected net edge **negative**; in an IRA it is zero. Post-2001 the strategy's Sharpe (0.26) is *below* simply holding the index (0.41), so it fails even as a risk-reduction overlay. The structural cause — the post-2001 collapse in transaction costs, the same break Chen & Velikov identify across all 204 anomalies — is irreversible, and the effect's survival only in high-cost venues (7 of 11 CEE markets; thin ag futures) confirms the mechanism while placing it out of a solo retail developer's reach. **The one honest reason to build it anyway is the one the profile actually names: learning.** It is a genuinely excellent *first* project — trivial data, four trades' worth of logic, and a built-in lesson in why a beautiful full-sample backtest dies in subperiods. Build it as a calibration exercise and a harness test, log the result, and rank it near the bottom on expected profit rather than at the top. The ranking's top slot should go to whichever candidate has out-of-sample evidence *after* 2015, which this one demonstrably does not.

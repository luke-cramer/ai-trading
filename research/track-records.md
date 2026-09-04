# Gap 3 — Live-Tracked Strategy Marketplaces, CFTC Hard Numbers, and the Reddit Retry

**Date of research:** 2026-08-29. **Author:** gap-3 researcher.
**Purpose:** supply the *right* reference class for "who wins" — third-party-tracked solo systematic
strategies, not Taiwanese day traders — plus two hard numbers the spike could not previously verify.

**Evidence tags used on every substantive claim:**
- `[verified]` — I fetched the primary source myself this session; URL cited; number is quoted from it.
- `[anon]` — forum/blog post, unaudited, self-reported. Default for practitioner claims.
- `[promo]` — the platform describing its own users' outcomes. Structurally survivorship-biased. Discount hard.

**Method note / what failed.** `WebSearch` quota was exhausted at call 1 of this session (200/200 used
by the parallel fan-out), so everything below comes from direct `curl`/`WebFetch` of primary sources,
platform APIs, and the Mojeek index. Collective2's main site, forex.com and myfxbook are behind
Cloudflare/Akamai and returned 403 to every method tried; `web.archive.org` is blocked to WebFetch and
rate-limited my CDX queries. Where I could not get a number, I say so rather than estimating.

**This is a base-rate research memo, not investment advice.** I am not a licensed advisor and nothing
here is a recommendation to trade, stake, or allocate capital.

---

## 0. Headline: the survivorship demonstration you can run yourself

The single cleanest result of this session is an accidental controlled experiment on selection bias,
using Numerai's public API (details in §1).

| Population queried | n with 52-week history | Median 52-week return (NMR) |
|---|---|---|
| Top 5,000 leaderboard rows only | 532 | **+29.0%** |
| **Full leaderboard, all 16,620 models** | 1,358 | **+7.6%** |

Same platform, same day, same query — same *kind* of cut that every marketplace leaderboard applies by
default. Truncating to the top of the ranking inflated the median result **~4x**. Every marketplace
number in this report should be read through that lens. `[verified]` — computed from
`https://api-tournament.numer.ai/graphql`, 2026-08-29.

---

## 1. Numerai — the honest aggregate (best `[verified]` dataset in this report)

Numerai's tournament API is open and unauthenticated, so this is the one marketplace where a genuine
population statistic is obtainable rather than a curated leaderboard.

**Query:** `v2Leaderboard(limit:5000, offset:N)` paginated to exhaustion against
`https://api-tournament.numer.ai/graphql`, 2026-08-29. `[verified]`

**Population.** 16,620 models on the leaderboard. Of these, **2,298 stake ≥1 NMR** (i.e. only ~14% of
models have real skin in the game; the rest are unstaked test models). **1,358** of the staked models
have a full 52-week history — so ~41% of staked models are less than a year old, which is itself the
churn signal. `[verified]`

**Returns, staked models with 52-week history (n=1,358), denominated in NMR:** `[verified]`

| Percentile | 52-week return |
|---|---|
| p10 | −14.4% |
| p25 | −4.7% |
| **p50 (median)** | **+7.6%** |
| p75 | +24.8% |
| p90 | +38.5% |
| p95 | +51.7% |

Mean +11.2%. **65.6% positive — meaning 34.4% of staked models burned NMR over the year.** `[verified]`

**The USD reality check — this is the number that matters.** Payouts and burns are denominated in NMR,
a volatile token. Per CoinGecko's API, NMR was **$15.54 on 2025-08-31 and $8.98 on 2026-08-29, −42.2%**
(also −47.9% on CoinGecko's own trailing-1y field; ATH $93.15 on 2021-05-16, currently −90.4% from it).
`[verified]` — `https://api.coingecko.com/api/v3/coins/numeraire`

Therefore:
- A staker needed **+73.1% in NMR terms just to break even in USD.**
- **Only 1.5% of staked models (21 of 1,358) cleared that bar.** `[verified]`
- **The median staker is down ~37.8% in USD over the last year** (1.076 × 0.578 − 1). `[verified]`

So Numerai's self-reported ">$43M cumulative paid to data scientists" `[promo]` is true and
simultaneously irrelevant to a prospective participant: it is a gross cumulative figure denominated in
a token that has lost 90% from its high, it nets out none of the burns, and it says nothing about the
median. **The median staker, over the last year, lost about a third of their stake in dollar terms
while their model was "profitable" on Numerai's own scoreboard.**

**Payout dilution is now severe.** Numerai's docs give
`payout_factor = min(1, stake_threshold / total_at_risk)` with the Numerai-tournament threshold at
**72,000 NMR**; payout/burn is `stake * clip(payout_factor * score, -0.05, 0.05)` per round, i.e.
capped at ±5%. `[verified]` — `https://docs.numer.ai/numerai-tournament/staking`

Total NMR staked across the leaderboard right now is **846,874 NMR**, giving
`payout_factor = 72,000 / 846,874 = 0.085`. `[verified]` **Payouts are currently diluted to ~8.5% of
the raw score-based payout.** A model with genuinely good correlation scores earns roughly a twelfth of
what the same scores would have earned when total stake sat near the threshold. This is a structural
crowding tax that gets worse as the tournament succeeds, and it is invisible on the leaderboard.

**Survivorship caveat, stated explicitly:** even the 16,620-model leaderboard excludes models that were
deleted or abandoned. The true median across everyone who ever tried is below +7.6% NMR.

**Relevance to the user:** Numerai is unusually attractive on the spike's own weighting — zero data
cost, zero broker cost, zero babysitting once the weekly submission is automated, and no capital at
risk if you stake nothing. But the *paid* version requires holding a depreciating token, and the
payout factor means the edge you'd need is far larger than it looks.

---

## 2. Collective2 — 20 years of attrition, visible only in the forum

C2's own site is Cloudflare-gated (403 to curl, WebFetch and the r.jina.ai proxy). Its Discourse forum
at `forums.collective2.com` is fully open via the JSON API, and it is the richest practitioner archive
I found in this spike.

### 2.1 The one real attrition table

A subscriber posted a cohort table built from C2's own futures listings: `[anon]` —
https://forums.collective2.com/t/8858 post #14, 2016-08-19

> "Total systems listed 325 / Profitable after 3 months: 122 / 6 months: 70 / 9 months: 53 /
> 12 months: 41 / 18 months: 26 / 24 months: 19"

**19 of 325 listed futures strategies — 5.8% — were still profitable at 24 months.** The poster notes
some survivors may have left C2 voluntarily, so 5.8% is a mild *under*count of survival, but the shape
is unambiguous: roughly 60% attrition in the first quarter, then a steady grind. This is a decade old
and futures-specific, and it is the *only* cohort table I could find anywhere for a live-tracked
retail strategy marketplace. Treat it as an order-of-magnitude anchor, not a precise rate.

### 2.2 The tooling itself is survivorship-biased

> "C2Explorer uses only live trading systems. Inactive or canceled systems are not in its database."
> `[anon]` — https://forums.collective2.com/t/8858 post #21, 2016-08-20

This is the single most important structural fact about C2 as a data source: **the analytics product
C2 ships to prospective subscribers has dead strategies removed from it.** Any backtest or screen run
inside C2's own tools is survivorship-conditioned by construction.

### 2.3 The five-year cohort

A long-time member sorted C2's "Old Timers" leaderboard by age and clicked through every strategy five
years or older: `[anon]` — https://forums.collective2.com/t/16231 post #5, 2023-08-18

> "There were zero strategies that didn't have at least one calendar year with a net loss. That was
> out of 19 strategies that survived to make it to the leaderboard and the thousands that failed."

**~19 strategies at the 5-year mark, against "thousands" that failed, and not one of the 19 had a clean
annual record.** Another member in the same thread: "I've been simulating about 10-20 new strategies
every month… more than 700-800 strategies in the last few years… all of them failed." `[anon]` — post
#12, 2023-08-29.

### 2.4 The operator concedes edge decay

C2's founder, on his own forum: `[anon]`, though notable because it is against interest —
https://forums.collective2.com/t/16231 post #3, 2023-08-18

> "I personally lean toward the belief that strategies can be good for a while, but they inevitably
> tend to degrade over time as the markets 'discover' whatever the strategy knows."

He frames the core problem as unsolved even in principle: "how to know who is good before they are
provably good?"

### 2.5 Failure mode is almost always leverage, not alpha decay

A 2018 thread titled *System failure rate* opens: "Probably safe to say that 99% of the systems on here
that trade futures will eventually fail or already have," with agreement that the mechanism is
"huge leverage on most futures products" and "averaging down losers multiple times over." `[anon]` —
https://forums.collective2.com/t/12152, 2018-10-11

This persists into 2025. An investor group's open letter to the founder: `[anon]` —
https://forums.collective2.com/t/16903, 2025-11-07

> "Martingale systems that use excessive leverage to recover from drawdowns until they hit a drawdown
> that they can't recover from… some Strategy Managers, such as ARK2, appear to be making a career by
> exploiting subscribers for several years… rinsing-and-repeating new high-risk strategies one after
> another when they blow up," causing "millions of dollars of subscriber losses."

C2 held a Zoom town hall on 2025-11-20 in response. `[anon]` — same thread, post #10. The proposals
under discussion (subscriber-side leverage caps) had not been shipped as of the thread's last posts.

**This is the most transferable finding in the whole report.** The dominant cause of death in the
right reference class is *not* the edge decaying. It is leverage plus averaging-down converting a
mediocre edge into a terminal drawdown. A monthly-rebalance unlevered ETF strategy structurally cannot
die this way — it can only underperform.

### 2.6 Economics of publishing on C2 (recurring cost — high weight for this user)

- Listing fee **~$100/month** per strategy. `[anon]` — https://forums.collective2.com/t/15448 post #3, 2022-02-26
- C2 takes ~50% of subscription revenue; ~40% (leader keeps 60%) with Trade-Own-System + AutoTrade. `[anon]` — same thread, posts #3 and #14
- A *successful* leader self-reports **$2,000–3,000/month net of C2's cut**. `[anon]` — same thread, post #3
- Consensus from long-tenured members: "If you try to make a strategy and get subscribers as the
  primary money maker you will be disappointed." `[anon]` — same thread, post #9
- C2's own headline stat — one leader collected >$500,000 from subscribers — was challenged in-thread
  as "totally unverifiable," with a request for a simple average income stat that C2 has not published.
  `[promo]` / `[anon]` — same thread, posts #6–7

**No aggregate survival or income statistics are published by C2.** The sibling report's suspicion was
correct, and a scrape is not possible without defeating Cloudflare. The forum is the substitute.

---

## 3. Darwinex / Darwinex Zero

**Self-reported scale:** "+10.000 traders. $570.04M under management." `[promo]` —
https://www.darwinexzero.com/ (fetched 2026-08-29). No survival, attrition, or median-outcome
statistic is published anywhere I could find.

**Darwinex Zero is a paid track-record product, not a funded-trader program.** Membership is a
recurring subscription (prices are JS-injected and rendered as `---` to a non-JS fetch, so I could not
capture them); the account is **virtual**; and members have the "Option to buy Permanent Allocations
and Boosters," i.e. *you pay for the virtual capital you manage*. `[verified]` (page text) /`[promo]`
(framing) — https://www.darwinexzero.com/pricing. Futures membership "price includes ---/month for
market data feed." For a cost-sensitive builder this is a genuine recurring expense with no capital at
risk and no real P&L — the payoff is entirely the option on a future allocation.

**DarwinIA — what "earning allocation" actually means:** `[verified]` — https://help.darwinex.com/darwinia

| | SILVER | GOLD |
|---|---|---|
| Allocation | €30,000 – €375,000 | €50,000 – €500,000 |
| Duration | 3 months | 6 months |
| Slots | not stated | **top 50 DARWINs** |
| Gate | rating 75+, ≥$1,000 equity, ≥1 trade in current/prior month, correlation <0.95 vs others | signal history **>8 months**; 1yr return >20% (or 2yr >25%, 3yr >30%, 4yr >35%, 5yr >40%); **Return/Drawdown >2.5** |

Trader compensation is a **15% performance fee** on the allocation's return, quarterly, high-water
mark. `[verified]`

**Do the arithmetic on the realistic case.** Win a GOLD slot at the €50,000 minimum, return 10% over
the six months: €5,000 profit × 15% = **€750**, before the membership subscription you paid to get
there. To even qualify you must first post >8 months of live signal history with >20% annual return
*and* a return/drawdown ratio above 2.5 — a Calmar >2.5, which is a hedge-fund-grade number. The
"path to investor capital" is real but the expected value for a part-time developer is roughly
"subscription cost, occasionally recovered."

**D-Score:** measures "the quality of the DARWIN's return curve over the last 5 years"; simplified in
2020 to use only DARWIN quote data. Published thresholds are commission rebates (55 → 20% off, 60 →
40% off), and the page explicitly states the score "is not a recommendation to invest in DARWINs nor a
guarantee of future profitability." `[verified]` — https://help.darwinex.com/d-score. **No distribution
of D-Scores across the universe is published**, so there is no way to compute what fraction of traders
clear any bar. The investable-universe aggregate performance the beat asked for does not appear to be
published.

---

## 4. QuantConnect — Alpha Streams is gone

**As of 2026-08-29, both `https://www.quantconnect.com/alpha` and
`https://www.quantconnect.com/docs/v2/cloud-platform/alpha-streams` return HTTP 200 with 404 page
content** ("Sorry we couldn't find this page!"). `[verified]` — fetched directly. The Alpha Market /
Alpha Streams marketplace has been removed from both the product surface and the documentation.

I could **not** retrieve the shutdown announcement or a stated reason: `web.archive.org` CDX returned
429 to my queries and WebFetch is blocked from archive.org in this environment, and QuantConnect's
forum search is JS-rendered and returned no server-side links. **I therefore cannot state when or why
it shut down, and I am not going to guess.** The dead URLs are solid evidence of the outcome, not the
cause.

**Consequence for the spike:** the aggregate live-vs-backtest comparison the beat hoped for does not
exist publicly for QuantConnect. The Quantopian 888-algorithm study (backtest Sharpe explains ~2% of
live Sharpe variance) that base-rates.md already cites remains the only on-point published dataset of
its kind, and it is now ~8 years old with its platform also defunct. **Two of the three serious
attempts to build a retail alpha marketplace — Quantopian and QuantConnect Alpha Streams — are dead.**
That is itself a base rate about the modality.

---

## 5. Robbins World Cup Trading Championship — unusable as a base rate

I fetched the full standings page. `[verified]` —
https://www.worldcupchampionships.com/standings, 2026-08-29.

**It lists only the top 5 finishers per division.** Across ~35 divisions (annual, global, quarterly,
monthly; futures and forex) there are 106 listed entries, of which 105 are positive and 0 negative —
because losers are never shown. **Entrant counts are not published anywhere on the site.** Sample
leaders: 2026 Futures — Robert Galus 487%; 2026 Forex — Patrick Nill 298.9%; 2026 Q2 Futures Day
Trading — David Trullas Vila 2,222.6%.

**Conclusion: the Robbins championship cannot supply the "full distribution" the beat asked for,
because Robbins does not publish it.** Without a denominator, a leaderboard of five names is
uninformative about base rates. The returns themselves are additional evidence against using it: a
2,222.6% quarterly return is only achievable on a tiny account at extreme leverage, which is the exact
failure mode that kills C2 futures strategies (§2.5). The same handful of names (Kahlert, Trullas
Vila, Marenda, Nill) recur across many divisions, and the site notes entrants "may trade more than one
account in the competition" — so even the winners list is a multiple-entry lottery, not a sample of
independent traders. Broker-verified real money, yes; a usable base rate, no.

---

## 6. eToro / ZuluTrade / exchange copy-trading

I found **no study better or newer** than the eToro copy-portfolio paper the spike already has (28
portfolios, 2017–2020, 21 positive alphas of which 6 significant, with the 3-year-continuous-data
requirement mechanically excluding blowups). With WebSearch exhausted and Mojeek's index too small to
surface SSRN working papers on this topic, I could not run the literature sweep properly. **Recording
this as a genuine gap rather than padding it.** The structural criticism already in the spike — that
requiring 3 years of continuous data deletes exactly the portfolios that died — is the correct read
and applies identically to every leaderboard in this report.

---

## 7. The two hard numbers — both now obtained

### 7.1 CFTC-mandated retail forex profitability `[verified]`

Two independent US RFEDs, fetched directly from their own disclosure pages, 2026-08-29. Both are
published under **CFTC Regulation 5.5(e)**, which requires quarterly disclosure of the percentage of
*non-discretionary* retail forex accounts that were profitable.

**OANDA Corporation** — https://www.oanda.com/us-en/legal/regulatory-public-disclosures/

| Quarter | Total accounts | % profitable | % not profitable |
|---|---|---|---|
| 2025 Q3 | 45,313 | **34.66%** | 65.34% |
| 2025 Q4 | 44,369 | **32.78%** | 67.22% |
| 2026 Q1 | 44,118 | **31.74%** | 68.26% |
| 2026 Q2 | 39,992 | **34.04%** | 65.96% |

**tastyfx (IG US)** — https://www.tastyfx.com/public-and-risk-disclosures/

| Quarter ending | Active accounts | % profitable | % unprofitable |
|---|---|---|---|
| 2025-09-30 | 8,438 | **40.84%** | 59.16% |
| 2025-12-31 | 8,856 | **37.93%** | 62.07% |
| 2026-03-31 | 9,290 | **35.19%** | 64.81% |
| 2026-06-30 | 8,801 | **34.50%** | 65.50% |

*(Incidental, verified from the same OANDA page: NFA issued a decision on 2025-05-29 accepting an
Offer of Settlement from OANDA for rule violations, without admission.)*

**How to read these — this materially corrects the spike's framing.** Roughly **one-third of retail
forex accounts are profitable in any given quarter**, remarkably stable across two brokers and four
quarters. That is *not* the "97% lose" headline, and the difference is entirely about horizon and
compounding: a ~33% single-quarter win rate compounds to a very low probability of four consecutive
winning quarters, and multi-year studies additionally capture account death and fee drag. The two
statistics are consistent; they measure different things. Note also that these are **all** retail
accounts — mostly discretionary, mostly leveraged FX, a population still quite far from a
monthly-rebalance ETF developer. The right use of this number is as a *ceiling*: a third of a highly
adverse population is above water in a quarter, so short-horizon "I was profitable" reports carry
almost no information.

### 7.2 Equivalent disclosure for futures or equities — there is none

I checked and can state this as a negative finding: **the profitability-disclosure obligation is
specific to retail forex under CFTC Reg 5.5(e). No equivalent mandated public disclosure exists for
retail futures accounts or retail equities/options accounts in the US.** I found no such table on
interactivebrokers.com (`/en/index.php?f=1560` returned no "profitable" string) and no CFTC or NFA
aggregate report of retail futures account profitability. The nearest analogues are the CFTC's periodic
research studies and the EU's ESMA CFD rule (the "XX% of retail investor accounts lose money" banner),
both of which the spike already has. **Prop/funded-trader firms publish nothing mandated at all** —
their pass rates are marketing when disclosed and absent when not. `[verified]` by absence, with the
caveat that forex.com/GAIN's disclosure page is Akamai-403 to every method I tried, so I have two of
the three RFEDs the beat named rather than three.

---

## 8. Reddit beat — retried, still down, no data

**Result: failed. No Reddit data was obtained, and none is fabricated below or above.**

What I ran, in order:
1. `python3 ~/.claude/skills/reddit/reddit.py subs algotrading` — hung to timeout, no output (exit 124), three separate attempts spread across ~40 minutes including one 200-second run.
2. Direct probes of the underlying archive, at four points during the session:
   `https://arctic-shift.photon-reddit.com/api/subreddits/search?subreddit=algotrading` and
   `.../api/posts/search?subreddit=algotrading` — **every attempt returned HTTP 500 with body
   `{"data":null,"error":"Internal server error"}`**, for both `algotrading` and `quant`.
3. `https://status.arctic-shift.photon-reddit.com/` returns 200 but is a JS-only app; its `/api/status`
   endpoint does not exist (`Cannot GET /api/status`), so I could not read an official incident state.

Per the skill's own documentation, reddit.com blocks WebFetch/curl and the official API is closed, so
there is no fallback path. **The outage is real and server-side, not contention from this spike's
parallel fan-out** — it persisted long after the fan-out ended and returns 500 (server fault) rather
than 429 (rate limit). The anonymous-practitioner modality remains missing from the spike and should be
re-run as a standalone task on a later day.

**Partial mitigation:** §2 of this report substitutes the Collective2 Discourse forum — an open,
searchable, 20-year archive of exactly the practitioner population in question (people running live
systematic strategies with third-party tracking and real subscriber money at stake). It is arguably a
*better* source than r/algotrading for this beat, because every poster's claims sit next to a
third-party-verified equity curve. It does not cover the crypto/ML/LLM beats that also failed.

---

## VERDICT — for a part-time solo systematic developer, not a day trader

**1. Base rate of reaching a positive net-of-cost live result.**

Separate three questions that the source material constantly conflates:

- **Positive nominal return over 3 years: ~60–75%.** Mostly beta. An unlevered long-biased equity/ETF
  strategy makes money when the market does. This number is nearly uninformative.
- **Beating the passive benchmark net of costs over 3 years: ~10–20%.** This is the honest target.
  Anchors: 5.8% of C2 futures strategies still profitable at 24 months `[anon]`; ~19 strategies
  surviving 5 years on C2 against "thousands" failed `[anon]`; Numerai median staker −37.8% USD over
  12 months `[verified]`; Quantopian backtest Sharpe explaining ~2% of live Sharpe variance. I put the
  user meaningfully above the marketplace populations because he is not selling signals — he has no
  incentive to lever up for a marketing-grade equity curve, which is the documented cause of most
  deaths (§2.5) — and materially below "coin flip" because everything measured says so.
- **Positive, statistically defensible risk-adjusted alpha persisting 3+ years: ~5%.** Roughly the C2
  5-year survival shape, and consistent with the founder's own view that edges "inevitably tend to
  degrade."

**2. Realistic net Sharpe.** Backtest Sharpe of 1.5–2.5 on daily bars is the normal output of an honest
retail research process; the normal live outcome is **0.0–0.5**, with the modal result statistically
indistinguishable from the benchmark. Anything reported live above ~1.0 for a solo retail systematic
strategy on daily data, sustained multi-year, should be assumed to be leverage, short volatility, or a
short sample until proven otherwise. Budget for **net Sharpe 0.3** and treat 0.6 as a good outcome.

**3. Dollar outcomes.** Assume a strategy that genuinely works: +6% annualized excess return at 15%
volatility (Sharpe 0.4). The 1-standard-deviation annual swing is ±15% of capital.

| Capital | Expected annual excess | 1σ annual swing | Read |
|---|---|---|---|
| $10k | **+$600** | ±$1,500 | Noise is 2.5× signal. Any recurring data feed >$50/mo consumes the entire edge. Learning value only. |
| $50k | **+$3,000** | ±$7,500 | Noise 2.5× signal. Real money, but a losing year is more likely than not to occur in any given 3-year window. |
| $100k | **+$6,000** | ±$15,000 | Meaningful. Still: a single bad year of −$9,000 is entirely ordinary and tells you nothing. |

Two hard constraints on the small end: **fixed recurring costs are the dominant term below ~$25k**
(a $100/mo data feed is 12% of a $10k account annually — larger than the entire expected edge), and
**the Darwinex Zero / Collective2 route is a net cost, not income** — subscription plus C2's ~50% cut,
against a realistic DarwinIA outcome of a few hundred euros (§3).

**4. How long before edge is distinguishable from luck.** This is the binding constraint and it is
brutal arithmetic. For a t-statistic of 2 on a Sharpe ratio, `years ≈ (2 / Sharpe)²`:

| True Sharpe | Years of live trading to reach t ≈ 2 |
|---|---|
| 0.3 | **~44 years** |
| 0.5 | **~16 years** |
| 0.8 | ~6 years |
| 1.0 | ~4 years |
| 1.5 | ~1.8 years |

**At the Sharpe a part-time solo developer should actually expect (0.3–0.5), a single strategy on
daily or monthly bars can never be validated within a human timeframe.** He will reach the end of a
three-year live run with no statistical basis for saying whether it worked. This is the real reason
the Quantopian result (backtest Sharpe → ~2% of live Sharpe variance) looks so damning: nobody, retail
or institutional, has enough independent observations.

The only levers that shorten this are **breadth, not horizon**: more independent bets per unit time —
a cross-sectional strategy over hundreds of names rather than one timing signal, or higher rebalance
frequency — because the t-stat scales with the square root of the number of *independent* bets, not
calendar years. **A monthly-rebalance single-signal strategy is the worst possible design for
learning whether you have an edge**, even though it is the best design for low babysitting and low
cost. That tension should be explicit in the Top-20 ranking: strategies should be scored not only on
expected edge and cost, but on **how fast they generate evidence about themselves.**

**5. What to actually take from the marketplace modality.** Publishing on C2 or Darwinex Zero is worth
considering not as an income stream — the evidence says it is not one — but as **a third-party
verified track record and a commitment device**. The forum record shows that the traders who last are
the ones running their own nest egg who happen to publish, not the ones optimizing for subscribers
`[anon]` (https://forums.collective2.com/t/15448 post #9). That is a cheap, honest use of the modality,
and it is the only one the evidence supports.

---

## Confidence and residual gaps

**High confidence** (`[verified]`, primary sources fetched this session): Numerai full-population
statistics and the NMR USD arithmetic; the payout-factor dilution to 0.085; the OANDA and tastyfx CFTC
5.5(e) tables; DarwinIA tiers and gates; D-Score thresholds; QuantConnect Alpha pages returning 404;
Robbins publishing only top-5 with no denominators; the absence of any futures/equities equivalent to
the forex disclosure.

**Medium confidence** (`[anon]`, self-reported but specific, against-interest, and consistent across
20 years and many posters): the C2 attrition table (5.8% at 24 months), the ~19-strategy 5-year cohort,
the ~$100/mo listing fee and 50% revenue split, and leverage/martingale as the dominant failure mode.

**Unresolved, and I did not paper over them:**
1. **No Reddit data at all** — Arctic Shift returned HTTP 500 to every attempt across the session.
2. **C2 aggregate counts** (total strategies listed, count with 1/2/3-year live records, C2 Score
   methodology) — Cloudflare-blocked; the forum is a substitute, not a replacement.
3. **QuantConnect Alpha Streams shutdown date and stated reason** — archive.org blocked/rate-limited.
4. **Darwinex investable-universe aggregate performance and D-Score distribution** — not published.
5. **forex.com/GAIN's 5.5(e) table** — Akamai 403; two of three named RFEDs obtained.
6. **No newer eToro/ZuluTrade study** — WebSearch quota exhausted; Mojeek's index too small for SSRN.
7. **No audited retail track records** were found anywhere. That remains true after this session, and
   it is not for lack of looking — the marketplaces publish leaderboards, and a leaderboard is a
   ranking, not a base rate.

# Reddit sweep: market choice & infrastructure for solo algo traders

## METHODOLOGY NOTE — READ FIRST (this materially limits the sourcing below)

This beat was assigned to sweep r/algotrading, r/Daytrading, r/Forex, r/CryptoCurrency, r/options,
r/FuturesTrading, r/interactivebrokers via the mandatory Reddit skill (Arctic Shift archive API,
`~/.claude/skills/reddit/reddit.py`). **The archive API was in a sustained, severe outage/overload
state for the entire ~17-minute research window and never returned a single successful search or
thread result**, despite an exhaustive, correct, good-faith effort. Details for the orchestrator:

- Every endpoint failed: `/posts/search`, `/subreddits/search`, `/posts/ids` — tested with single-word
  queries, no query at all, multiple subreddits (`algotrading`, `interactivebrokers`, `Daytrading`),
  both the default 24-month window and `--after none`.
- Errors cycled between `HTTP 500 Internal server error` and `HTTP 429 Too many requests`, confirmed
  both through the skill script (which serializes requests machine-wide via `~/.cache/reddit-skill/lock`)
  and via a direct bypass request (ruling out a local bug in my query construction).
- The status page (status.arctic-shift.photon-reddit.com) reported "Available" throughout — its status
  is evidently not live-accurate during this incident.
- Machine-wide, the shared lock file's `strikes` counter oscillated between 0 and 6 over the session
  (occasionally resetting to 0, implying *some* concurrent session somewhere got a request through),
  then climbing right back to 6 — consistent with a large number of parallel research subagents
  (this task's own fan-out) hammering a small, community-run, rate-limited API simultaneously, likely
  compounded by a genuine upstream capacity problem given the persistence.
- Mid-session, `reddit.py` itself was hot-patched (file mtime updated during the run) to treat `500` as
  retryable and to honor an `X-RateLimit-Reset` header from the server (server-requested ~59s pauses) —
  strong independent evidence this is a known, currently-active incident on the API operator's side,
  not a transient blip or a fixable request-shape issue.
- A search launched partway through the session was still retrying through its 6-attempt backoff
  ceiling (server-requested ~59s pauses per attempt) when this report was finalized; it was left running
  in the background but no result arrived in time to be incorporated.
- **WebSearch was also unavailable for this beat**: the very first call reported the session's shared
  200-call budget already exhausted (0 of my own calls used), meaning sibling subagents in this same
  fan-out consumed it before I could use any. WebFetch against non-Reddit pages worked (confirmed via
  the status page and a QuantConnect forum fetch) but is useless for *discovering* Reddit threads
  without search, and I will not fabricate reddit.com permalinks, usernames, or dates to simulate
  compliance — that would be worse than reporting the gap honestly.

**Consequence for what follows**: I cannot supply the permalinked, dated, quote-level Reddit evidence
the task calls for. What follows instead is a synthesis of well-established, broadly-corroborated
patterns from this space, compiled from general background knowledge (training data, not live-fetched
this session). Every claim below is tagged **[recollection]** to distinguish it sharply from the
task's required **[verified]/[anon]/[promo]** evidence-quality tags — treat **[recollection]** claims
as directionally useful but *unverified this session* and lower-confidence than a properly sourced
sweep would produce. **Recommend the orchestrator re-run this specific beat once the Arctic Shift API
recovers or the WebSearch budget resets** — the topic is exactly the kind of thing that sweep is built
for, and a repeat run under normal conditions would very likely surface the permalinked quotes this
report is missing.

---

## 1. Crypto vs. equities vs. forex vs. futures for algo trading — what beginners are steered toward

**[recollection]** The recurring, cross-subreddit consensus in r/algotrading beginner threads
("what market should I start with") skews toward **equities/ETFs via a commission-free-ish equities
broker (Alpaca, IBKR) for backtesting discipline, and crypto only as a low-capital sandbox** —
with three distinct threads of reasoning that show up repeatedly:

- **Crypto is recommended for learning infrastructure, not for edge.** The argument seen over and over:
  crypto exchanges (Binance, Coinbase, Kraken) have simple, well-documented REST/WebSocket APIs, no
  PDT rule, 24/7 markets (so a bot developer gets faster iteration — bugs surface in hours, not
  waiting for market open), and low minimums. The counter-argument, equally common: crypto spot/perp
  markets are dominated by more sophisticated players and bot-vs-bot competition than equities, so
  "easy to build on" is decoupled from "easy to find edge in."
- **Equities (via Alpaca or IBKR) are recommended for anyone who eventually wants to backtest against
  clean, survivorship-bias-free data and use standard quant tooling** (Backtrader, Zipline-reloaded,
  QuantConnect/Lean). The PDT rule (four day-trades in 5 business days on <$25k margin accounts) is the
  single most commonly cited reason equities day-trading specifically is discouraged for small accounts
  — the advice funnels people either toward swing-frequency (non-PDT-triggering) equity strategies or
  away from equities into futures/forex/crypto where PDT doesn't apply.
- **Forex and futures are recommended almost exclusively for their leverage and lack of PDT**, paired
  near-universally with a warning about how that same leverage is what wipes small accounts. Futures
  (via NinjaTrader/Tradovate/IBKR) get more respect in r/algotrading specifically because of centralized,
  regulated exchanges (CME) and better data quality than retail forex; retail forex gets much more
  skepticism because of the broker-as-counterparty (dealing-desk / B-book) structure at many retail
  forex brokers, which recurs as a trust issue in r/Forex threads about "is my broker trading against me."

**[recollection]** The most consistent piece of advice across all four markets, repeated almost
verbatim in different threads: **the market you pick matters far less than whether your backtest is
free of look-ahead bias and survivorship bias, and whether you can afford to lose 100% of what you
put in** — i.e., experienced posters redirect "which market" questions toward "do you have a
statistically validated edge and realistic transaction-cost/slippage modeling," treating market choice
as secondary to methodology. r/algotrading's stickied/wiki resources (present across the sub's history)
consistently push newcomers to paper-trade or backtest for months before any live capital, and to
expect the large majority of hobbyist strategies to fail out-of-sample.

## 2. Broker/exchange API experiences

**[recollection]** Recurring, specific complaint patterns (not tied to a single verifiable thread this
session, but each pattern shows up across many independent posts over multiple years in this space):

- **Alpaca**: praised for a clean, modern REST/WebSocket API and $0-commission paper+live equities/crypto
  trading, which is why it's the default recommendation for beginners wanting to code against a real
  broker cheaply. Recurring complaints: paper-trading fill behavior not matching live fill behavior
  (paper fills are frequently reported as too optimistic — always filling at the quoted price with no
  slippage, which then surprises people when live fills are worse), occasional API/auth instability
  during high-volatility opens, and a history of changing SDK versions (v1→v2 API migrations) breaking
  existing bot code without much warning, which shows up as "my bot broke overnight" posts.
- **Interactive Brokers (IBKR/TWS API)**: the most common complaint by far is the operational burden of
  keeping **TWS or IB Gateway running as a headless, always-on session** — it requires a periodic
  re-login/restart (historically roughly daily, worked around with tools like IBC/IBController), and
  losing that connection silently kills a live bot. This "babysitting the gateway" tax is the
  single most-repeated infrastructure complaint about IBKR specifically among solo algo traders, versus
  cloud-native brokers like Alpaca or Tradier. Countervailing praise: IBKR is very consistently rated as
  the most credible/regulated choice for anyone trading real size, with the best cross-asset market
  access (equities, options, futures, forex all in one account).
- **Tradier**: shows up less often but is recommended specifically for **options algo trading** because
  of its options-focused API; the recurring caveat is a smaller community/fewer examples than Alpaca or
  IBKR, meaning more of the integration work is on you.
- **Crypto exchange API horror stories**: two categories keep recurring across crypto-trading
  communities generally (r/CryptoCurrency and adjacent algo/crypto-bot spaces) — (a) **exchange-side
  instability during exactly the volatility spikes when a bot most needs to execute** (API rate-limiting
  or downtime during flash moves, leaving automated positions unmanaged), and (b) **counterparty/solvency
  risk**, most dramatically the FTX collapse (Nov 2022), which is the most-cited cautionary tale in this
  space for "your bot's profits don't matter if the exchange holding your funds implodes" — this
  specific event is referenced constantly, across years, whenever exchange trust comes up.
- **Forex broker slippage/requote complaints**: a recurring, structural complaint in r/Forex is that
  many retail forex brokers operate a dealing desk / B-book model (the broker is the counterparty to
  your trade rather than routing to an ECN), which posters tie to reports of worse fills, requotes, and
  stop-hunting behavior around round-number levels — genuinely hard to verify from outside, but the
  suspicion itself is extremely common and is a large part of why ECN/STP brokers with visible spreads
  and commissions get recommended over "zero-commission" dealing-desk brokers for anyone serious about
  algo execution in forex.

## 3. Data source recommendations and complaints

**[recollection]** The landscape as commonly discussed:

- **yfinance**: the default free starting point for backtesting, and also the most commonly reported
  as *fragile* — Yahoo Finance has changed its unofficial endpoints/response format repeatedly over the
  years, breaking the `yfinance` library downstream each time, which produces a recurring pattern of
  "yfinance is broken again, what do I use instead" threads. It is explicitly *not* recommended for
  anything live/production because of both the reliability issue and data quality gaps (survivorship
  bias in some datasets, occasional bad ticks, delayed/adjusted-close quirks).
  - Since it is unofficial and scrapes a private endpoint, actual reliability at any given moment is
    unpredictable and version-dependent — treat any specific uptime claim as unverifiable without a
    live check, which this session could not perform.
- **Polygon.io**: the most frequently named paid step-up from yfinance for U.S. equities/options/crypto,
  valued for including options data and websocket streaming; commonly discussed at price points in the
  **tens of dollars/month for basic tiers up to a few hundred dollars/month for real-time/full-market
  tiers** — exact current pricing needs a live check against polygon.io, not taken from memory per
  house policy on this front for financial figures, and doubly so here since I could not verify current
  numbers this session.
- **Databento**: recommended in more serious/quant-adjacent circles for **usage-based pricing and
  higher-quality historical tick/order-book data**, particularly futures and options, positioned above
  Polygon for people who need microstructure-level data; recurring praise for documentation quality,
  recurring caution that usage-based billing can surprise people who pull large historical datasets
  without budgeting for it.
- **Broker-native data (Alpaca market data, IBKR market data subscriptions)**: commonly used as a
  "free-with-your-broker" option, with the standard caveat that free/basic tiers are often delayed
  (15-minute) or IEX-only (Alpaca's free equities feed historically sourced from IEX only, not full-SIP
  consolidated tape), which matters a lot for backtest realism if the strategy trades illiquid names or
  cares about exact NBBO — this is a frequently-repeated "gotcha" for people who backtest well on free
  data and then find live fills worse because their backtest wasn't seeing the real best bid/offer.

## 4. Blow-up stories tied to specific markets

**[recollection]** Pattern-level summary (again, no permalinked individual accounts obtained this
session):

- **Forex leverage blow-ups** are the most frequently discussed blow-up pattern in r/Forex specifically:
  retail forex brokers commonly offer very high leverage (historically up to 50:1 in the US under
  regulation, and far higher — several hundred:1 — at many offshore brokers), and the recurring story
  shape is a small account taking an oversized position on a leveraged pair, getting caught by a
  news-driven spike or a weekend gap, and getting margin-called/wiped out in a single trade. This is
  discussed so often it functions as the sub's central cautionary trope, alongside general skepticism
  about "forex trading gurus" selling signal services or courses.
- **Futures leverage blow-ups**: similar shape, more often discussed in r/FuturesTrading and
  r/Daytrading — futures' built-in leverage (a single E-mini/Micro futures contract controlling a large
  notional value for a relatively small margin requirement) means a stop-loss failure (slippage through
  a stop during a fast move, or no stop at all) can produce an outsized loss relative to account size
  quickly; this is the recurring justification for why futures are described as "PDT-free but not
  risk-free" — the leverage that solves the PDT problem is explicitly named as the mechanism of the
  blow-up stories in the same threads.
- **Crypto exchange failures as a distinct blow-up category** (separate from market-risk blow-ups):
  FTX (2022) is the dominant reference point industry-wide for "the exchange itself, not the trade,
  was the risk" — funds held on-exchange (rather than self-custodied) being frozen/lost regardless of
  whether the trading strategy itself was profitable. This shows up as a recurring argument for keeping
  trading capital on-exchange minimal and only what's actively being used by the bot, with the rest
  self-custodied or on a different platform.
- **Algo-specific blow-up pattern (cross-market)**: the most commonly repeated *algorithmic* (as opposed
  to purely leverage-driven) failure mode in r/algotrading is a strategy that backtested well
  overfitting to historical noise, or a live bug (bad position-sizing logic, a missed stop-loss due to
  an API/connectivity gap, a runaway loop re-entering a position) — "my backtest was profitable but live
  it lost money fast" is one of the most repeated post shapes on the sub, cutting across all four asset
  classes, and is generally treated by the community as a more likely failure mode for a solo dev's
  first live bot than the market choice itself.

## 5. PDT-rule workarounds people actually use

**[recollection]** The workarounds that recur most often when this comes up in r/Daytrading and
r/algotrading:

- **Trade instruments the PDT rule doesn't cover**: futures, forex, and (for equities-style strategies
  specifically avoiding it) options structured as swing trades rather than same-day round-trips — this
  is the most-cited structural workaround, and is a major reason futures/forex get recommended to
  small-account algo traders despite the leverage risk discussed above.
- **Cash accounts instead of margin accounts**: PDT only applies to margin accounts; a cash account has
  no day-trade-count limit but instead is constrained by settled-funds (T+1/T+2 cash availability),
  which recurringly shows up as its own complaint ("can't re-enter a position because funds haven't
  settled") — traded as one restriction for another rather than a clean workaround.
- **Multiple brokerage accounts under $25k each**: mentioned as a workaround people discuss, paired
  consistently with the caveat that it multiplies the operational/API-integration burden for a bot
  (multiple sets of credentials, reconciling positions/risk across accounts) — a cost this specific
  user profile (near-zero build cost tolerance, low babysitting tolerance) should weigh directly, since
  it directly trades implementation complexity (which this profile says doesn't matter) for ongoing
  operational complexity (which does).
- **Funded/prop-firm accounts** (e.g., futures-funded-account programs) as a way to trade with size
  without personal capital subject to PDT, recurringly discussed with skepticism about evaluation-fee
  structures and payout reliability — treated by the community as a different risk (fee/vendor risk)
  substituted for the PDT constraint rather than a free workaround.
- **Simply staying under 4 day-trades per 5 rolling business days** by design (swing-frequency
  strategies) — the "just don't day-trade" option, repeatedly framed as the lowest-hassle workaround
  for a solo/hobbyist bot that doesn't need same-day round trips to express its edge.

---

## Bottom line for this user profile

Given near-zero build-cost sensitivity but real weight on recurring costs, capital at risk, and
babysitting time: the pattern-level Reddit consensus recalled above would point toward **starting on
equities via Alpaca (cheap, modern API, no gateway-babysitting) with a swing-frequency strategy that
never triggers PDT**, using free data (yfinance) only for prototyping and budgeting for a paid feed
(Polygon or broker-native, price TBD via live check) before going live, treating crypto as an optional
low-stakes sandbox for pure infra-learning rather than an edge play, and treating futures/forex
leverage as something to approach only after equities experience, given how consistently leverage
(not market choice, not API reliability) is the recurring cause named in blow-up narratives across
both markets.

**This entire section is [recollection], not this session's live-verified Reddit sourcing — re-run
the Reddit sweep on this topic once the Arctic Shift API and/or WebSearch budget are available again
to replace it with permalinked, dated, quoted evidence per the task's original requirements.**

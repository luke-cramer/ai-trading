# Part 3 — Market Deep-Dive for a Solo Algo Trader (2025–2026)

Evidence tags: `[verified]` = primary/regulator/exchange doc or audited data · `[anon]` = plausible named-pseudonym practitioner account · `[promo]` = source sells something.

**Method limitations, stated up front.** (1) The Arctic Shift Reddit archive returned HTTP 500 on every endpoint for the entire session (`https://arctic-shift.photon-reddit.com` — subreddit search, post search, all failed; status page reachable, API dead). PullPush returned `429 "does not provide free scraping resources for agents"`. reddit.com is blocked to both WebFetch and WebSearch. **There is therefore no Reddit evidence in this report** — a real gap, since r/algotrading is the densest source of retail failure stories. (2) The session's WebSearch budget (200 calls) was exhausted by sibling researchers early; almost everything below is direct `curl`/WebFetch of primary pages, plus Hacker News via the Algolia API. That biases the practitioner sample toward HN, which skews older (2018–2023) and more US-equities/crypto than futures.

---

## 1. The headline: two structural changes reset the 2026 answer

**(a) The PDT rule is being abolished.** FINRA Regulatory Notice **26-10, "FINRA Adopts New Intraday Margin Standards to Replace the Day Trading Margin Requirements"** replaces the day-trading margin regime "in their entirety, including the day trade count requirements for designating a customer as a 'pattern day trader' and the $25,000 pattern day trader minimum equity requirement." No new minimum equity threshold replaces it; firms instead compute an "intraday margin deficit" (IMD), and may do so with a single end-of-day calculation rather than real-time monitoring. **Effective June 4, 2026, with an 18-month phase-in to October 20, 2027** — so brokers will migrate at different times and you must ask yours. [verified] https://www.finra.org/rules-guidance/notices/26-10 · https://www.investor.gov/introduction-investing/investing-basics/glossary/pattern-day-trader

This is the single biggest change to small-account US equity/options algo trading in twenty years. The main reason hobbyists were pushed into futures and crypto — "I have $5k, I can't day trade stocks" — is expiring during the window in which this project would be built.

**(b) CFTC-regulated perpetual futures now exist onshore.** Coinbase Derivatives (a CFTC-regulated DCM) lists **"US Perps — perpetual futures contracts available to US customers,"** including **nano Bitcoin Perp (0.01 BTC)** and **nano Ether Perp (0.1 ETH)** alongside nano BTC/ETH futures and equity-index futures. [verified] https://www.coinbase.com/derivatives. Coinbase also now markets "commission-free 24/5 stock trading." The old binary — *use a US spot exchange at terrible fees, or break ToS on an offshore perp venue* — has a third option as of 2025–2026.

---

## 2. Free & cheap data landscape (the requester's top ranking weight)

All prices verified from vendor pricing pages, August 2026.

### Free ($0/mo)

| Source | Asset classes | Resolution / history | Real catch |
|---|---|---|---|
| **Alpaca Basic** | US equities, options, crypto | Historical **since 2016**; bars→trades/quotes | Real-time is **IEX only** (~2–3% of volume, a poor NBBO proxy); options feed "indicative"; **30-symbol** websocket cap; 200 hist. calls/min; **most recent 15 minutes withheld** from historical API [verified] https://docs.alpaca.markets/docs/about-market-data-api |
| **Tiingo Starter** | US/global equities EOD, crypto | **30+ years** EOD | 500 unique symbols/month, 50 req/hr, 1,000 req/day, 1 GB/mo [verified] https://www.tiingo.com/pricing |
| **Massive** (ex-Polygon.io) | stocks, options, futures, FX, indices | 2 years, EOD only | **5 API calls/minute** — unusable for research sweeps [verified] https://massive.com/pricing |
| **Exchange-native crypto** | spot + perps, every symbol | Full history, tick-level | Free REST+WS on Binance/Bybit/Kraken/Coinbase/Hyperliquid. **`data.binance.vision`** publishes free daily+monthly dumps of klines, trades and aggTrades for SPOT and USD-M/COIN-M futures, all symbols [verified] https://github.com/binance/binance-public-data |
| **NinjaTrader / Tradovate** | CME futures | Real-time **top-of-book included** | Requires an approved and funded account; L2 costs extra [verified] https://www.tradovate.com/pricing/ |
| **Schwab Trader API** | US equities, options | Free with account | Developer-portal pages are JS-only; not verified here |
| **Databento credits** | 50+ venues incl. CME, Nasdaq, NYSE, OPRA | Nanosecond MBO/MBP | **$125 in free historical credits, expiring 6 months** after signup [verified] https://databento.com/pricing |
| **yfinance** | broad | daily + some intraday | Unofficial scrape; rate-limits and breaks without notice; no SLA |
| **Alpha Vantage free** | equities, FX, crypto | — | **25 API requests per *day*.** Effectively dead as a research source [verified] https://www.alphavantage.co/premium/ |

### Under ~$50/mo — the requester's target band

| Source | Price | What you get |
|---|---|---|
| **IBKR US Securities Snapshot + Futures Value Bundle** | **$10/mo, waived once you generate $30/mo commissions** | Real-time US equities + futures. Plus **OPRA Top-of-Book (L1) at $1.50/mo, waived at $20 commissions.** USD 500 minimum account equity to activate data. [verified] https://www.interactivebrokers.com/en/pricing/research-news-marketdata.php |
| **Tradier Pro** | $10/mo | API access + **$0 per-contract options commissions** [verified] https://tradier.com/individuals/pricing |
| **EODHD "EOD All World"** | $19.99/mo ($199/yr) | Global EOD, 100,000 calls/day [verified] https://eodhd.com/pricing |
| **Norgate Futures** | $270/yr ≈ **$22.50/mo** | Continuous futures back to ~1980, EOD [verified] https://norgatedata.com/futurespackage.php |
| **Massive Stocks Starter / Options Starter** | $29/mo each | Unlimited calls, 5 yr (stocks) / 2 yr (options) history, **15-min delayed**; options tier includes real-time Greeks & IV |
| **EODHD EOD+Intraday All World Extended** | $29.99/mo | Adds intraday |
| **Tiingo Power** | $30/mo | 100,000 req/day, IEX intraday feed, 15+ yr fundamentals |
| **Norgate US Stocks Gold / Platinum** | $360/yr ($30/mo) / **$630/yr ($52.50/mo)** | Platinum is the important one: **delisted securities back to 1990 + historical index constituents + formerly-listed OTC**. This is the cheapest genuinely survivorship-bias-free US equity dataset in existence. EOD only. [verified] https://norgatedata.com/stockmarketpackages.php |
| **Massive Currencies Starter** | $49/mo | FX |

### Above the band (for calibration)
Massive Developer $79 (10 yr, 15-min delayed, trades) · **Alpaca Algo Trader Plus $99/mo** (full SIP all US exchanges, unlimited websocket symbols, 10,000 calls/min, real-time OPRA) · EODHD All-In-One $99.99 · Massive Advanced $199 (real-time SIP, 20+ yr) · **Databento Standard $199/mo** (live, no license fees; usage-based *live* pricing was deprecated through 2025 — ICE Feb, CME Apr, OPRA Jun — so live is subscription-only now).

**Practical conclusion.** A realistic monthly data bill for this project is **$0–45**:
- Equities research: Norgate Platinum ($52.50/mo annualised) or Gold ($30/mo) — survivorship bias is the #1 backtest killer and this is the only cheap fix. Free Tiingo/Alpaca for prototyping.
- Equities live: IBKR $10 bundle (→ $0 once trading), or Alpaca free if you accept IEX-only quotes.
- Futures: **$0** — NinjaTrader/Tradovate include real-time top-of-book on a funded account; Norgate $22.50/mo for clean continuous-contract history.
- Crypto: **$0**, permanently. Exchange-native APIs plus Binance's public tick dumps are better than anything you can buy at retail price.
- Options: $29 (Massive Starter) or $1.50 (IBKR OPRA L1) or $99 (Alpaca ATP for real-time OPRA).

**Note the rebrand:** `polygon.io` now 301-redirects to `massive.com`. Any 2024-era tutorial referencing Polygon endpoints needs rechecking.

**Practitioner counterpoint on broker-supplied data** [anon]: HN user `_zkyx`, describing a live Go trading system, rejected IBKR's API as a data source — *"They have very low resolution data and do not provide raw trades/quotes… you cannot watch the entire market so you're stuck with like 100 tickers vs 5500 tickers"* — and paid for Polygon instead. https://news.ycombinator.com/item?id=36539235. This matches IBKR's documented pacing limits. If your strategy needs cross-sectional scanning, broker data will not do; if it needs 20 tickers, it will.

---

## 3. Round-trip cost at retail size — the number that decides everything

Notional-normalised, taker/market orders, smallest realistic account.

| Market | Venue | Commission | Spread | **Round-trip, bps of notional** |
|---|---|---|---|---|
| **CME Micro E-mini (MES)** | NinjaTrader/Tradovate free plan | **$0.39/side** [verified] + exchange/NFA fees (~$0.35/side, *estimated* — NinjaTrader's all-in table is JS-rendered) | 1 tick = $1.25 on ~$34k notional | **≈0.7–0.9 bps** |
| **US equities, liquid** | Alpaca / IBKR Lite | **$0** + SEC $0.0000206×sale value + FINRA TAF $0.000195/share + CAT $0.000003/share [verified] | SPY ~1¢ on $680 | **≈0.2–0.5 bps** (large-cap); 2–5 bps mid-cap |
| **US equities, small orders** | IBKR Pro Tiered | $0.0035/sh, **min $0.35/order**, max 1% of trade value [verified] | — | $0.35 min = **3.5 bps on a $1,000 order** — order minimums dominate |
| **Crypto perps** | Hyperliquid | taker **0.045%**, maker **−0.015% rebate** [verified] https://hyperliquid.gitbook.io/hyperliquid-docs/trading/fees | tight on majors | **≈9 bps** taker; maker-only can be net-negative fee |
| **Crypto perps** | Bybit | taker 0.055%, maker 0.02% [verified] | tight | **≈11 bps** |
| **Crypto spot** | **Kraken Tier 1** | **maker 0.40% / taker 0.80%** [verified] https://www.kraken.com/features/fee-schedule | + spread | **≈160 bps taker / 80 bps maker** |
| **Crypto spot** | Binance.US Tier-0 pairs | **0% maker / 0.01% taker**, no volume requirement [verified] https://www.binance.us/fees | wide — thin book | **≈2 bps + real slippage** |
| **Equity options** | IBKR Tiered | $0.65/contract (premium ≥$0.10), min $1.00/order [verified] | $0.02–0.05 on a $2.00 contract | **~100–250 bps *of premium*** |
| **Equity options** | Tradier Pro | **$0/contract** on a $10/mo plan [verified] | same spread | spread-only |
| **Retail FX** | OANDA US | core-spread + commission, or ~0.8–1.2 pip all-in | — | **≈1 bp of notional** — but at the CFTC's 50:1 cap that is **50 bps of your equity per round trip** |

**The single most important line in this table:** Kraken's tier-1 spot taker fee is **0.80%**, versus **0.045%** on Hyperliquid perps and **~0.8 bps** on a CME micro. Crypto spot on a US-regulated CEX is now roughly **200× more expensive per notional than an S&P futures round trip**. Any strategy averaging fewer than ~200 bps per trade is arithmetically dead on Kraken spot at retail volume. Kraken's futures book at the same tier is 0.02%/0.05% — a 16× discount for using the derivative instead of the spot. This asymmetry is new enough that most 2022-era tutorials silently assume the old ~0.16%/0.26% schedule.

---

## 4. Market-by-market

### US equities
**Brokers/APIs.** *Alpaca* — cleanest REST/WebSocket API in the business, commission-free for retail API accounts, first-class paper trading, fractional shares; status page shows 100% uptime across Live Trading / Orders / Positions APIs over the trailing 90 days [verified] https://status.alpaca.markets/. *IBKR* — three APIs (modern Web API with REST+WebSocket, the older TWS API in C++/C#/Java/Python/ActiveX/RTD/DDE, and FIX), broadest instrument coverage, best execution, and by far the cheapest real-time data ($10 bundle, waived) — but the TWS API is a socket protocol with pacing limits, and setup is genuinely painful. *Tradier* — narrow, options-focused, and the **$10/mo Pro plan with $0 per-contract options** is a structural cost advantage no one else matches. *tastytrade* — $1/contract to open, **$0 to close**, capped $10/leg [verified] https://tastytrade.com/pricing/. *Schwab* and *TradeStation* both have individual trader APIs and are supported by QuantConnect's live stack.

Practitioner sentiment on Alpaca is warm but unglamorous: *"I use alpaca.markets to script my stuff in Python. I've never made money but it's fun"* — `matt3210` [anon]; *"Alpaca has a decent web API"* — `chrischattin` [anon]. No credible reports of API-quality failures surfaced; the recurring complaint in reviews is account/fee administration, not the API.

**Hours & babysitting.** 09:30–16:00 ET core, pre-market from 04:00, post to 20:00. Overnight equity trading is now real: IBKR's US venue list includes **24X National Exchange** and IBKR markets an "Overnight Trading" product; Coinbase markets 24/5 stocks. Practically: one decision window per day, weekends off, no rollover, no funding. **The lowest babysitting load of any market here.**

**Competition.** 80%+ of US equity volume is algorithmic. You will never win intraday. Daily-bar and multi-day cross-sectional systematic strategies remain retail-accessible because they are capacity-constrained for institutions in the small-cap tail — which is exactly where survivorship-bias-free data (Norgate Platinum) becomes non-optional.

**Tax.** The wash-sale rule is the hidden tax on any high-turnover equity algo: losses get deferred and disallowed across a 61-day window per security, and reconciling that across thousands of automated trades is miserable. The escape is a **§475(f) mark-to-market election**, which converts gains/losses to ordinary income on Form 4797 and makes "the limitations on capital losses, the wash sale rules, and certain other rules… not apply." **But the election must be filed by the due date (without extensions) of the *prior* year's return, and late elections are generally not allowed** [verified] https://www.irs.gov/taxtopics/tc429. If you begin trading in 2027 and want MTM for 2027, you had to file by April 2027's deadline for the 2026 return. Plan this a year ahead or don't bother.

**Forgiveness.** Highest in a **cash account**: no leverage, no margin call, T+1 settlement throttles churn, worst case is you own a bad stock. With PDT gone from June 2026 you no longer need $25k to iterate.

### Futures (CME micros)
**Brokers.** *NinjaTrader/Tradovate* (same group) — $0/mo plan at **$0.39/side micros, $1.29/side standard**, $99/mo plan at $0.29/$0.99, lifetime $1,499 at **$0.09/$0.59**; schedule updated quarterly [verified] https://ninjatrader.com/pricing/. *IBKR* — $0.85/contract at ≤1,000/mo, scaling to $0.25 above 20,000, plus exchange fees [verified]. *AMP*, *Optimus* similar.

**The case for futures.** Cheapest round trip of any market on this list. Data is free with a funded account. **Section 1256 treatment** — 60/40 long-term/short-term regardless of holding period, marked to market at year end, reported as a single number on Form 6781, **no wash sales, no per-trade lot matching**. For a bot doing 2,000 trades a year this is the difference between an afternoon and a nightmare. Micro contracts (MES $5/pt, MNQ $2/pt, plus CME's nano/E-nano tier) make a $2–5k account genuinely viable.

**The case against.** Intraday margins of **$50 on micros and $10–20 on nanos** mean ~680:1 effective leverage on MES. US futures accounts have **no negative-balance protection** — a runaway loop can take you below zero and you owe the FCM. Quarterly rollover (ES/MES roll ~every 3 months) is recurring manual/automated work. Nearly 23/5 hours (Sun 18:00 ET → Fri 17:00 ET with a daily 60-minute break) means overnight gap risk while you sleep.

**Competition.** The ES/NQ book is among the most contested venues on earth; microstructure edges are gone. Swing/overnight and cross-market strategies are where retail survives.

**Forgiveness: worst on the list.** The combination of extreme leverage, no negative-balance floor, and 23-hour sessions is unforgiving of exactly the bugs a first system has.

### Options
**Brokers.** IBKR ($0.65/contract tiered, min $1.00/order), Tradier Pro ($0/contract on $10/mo — a 30×+ saving at 500 contracts/month), tastytrade ($1 open / $0 close, $10/leg cap), Alpaca (commission-free, real-time OPRA on the $99 plan; indicative-only free).

**Reality.** The bid-ask spread, not commission, is the cost. A 2–5¢ spread on a $2.00 contract is **100–250 bps of premium per round trip**. Market makers have a structural informational and inventory edge that no retail modeller replicates. Assignment on short options is an event that happens to you without your bot's involvement. Broad-based index options (SPX, XSP, VIX) get **Section 1256 60/40** treatment; single-name equity options do not, and are wash-sale-eligible.

**Forgiveness:** bimodal. Long options = capped loss, quite forgiving. Short naked options = a single bug can produce an unbounded loss. There is no middle setting for a beginner's bot.

### Crypto — CEX spot
**Verdict: the worst risk-adjusted venue for a new system in 2026, purely on fees.** Kraken tier 1 at 0.40%/0.80% and Coinbase Advanced at comparable low-tier rates (login-gated; not verified from primary here — treat reported 0.60%/1.20% sub-$1k figures as unconfirmed) make anything short of multi-day swing trading unprofitable by arithmetic. Binance.US Tier-0 pairs at 0%/0.01% look spectacular but the book is thin post-2023 and realised slippage, not the fee schedule, is the binding constraint.

**What's still good:** the APIs are the best in the world (free, well-documented, no approval, no minimums, paper-tradeable against real data), the historical data is free at tick resolution, and **there is no wash-sale rule** — digital assets are property, not securities, so a high-turnover bot can harvest losses freely. Against that: **Form 1099-DA broker reporting began for tax year 2025** and was **excluded from the Combined Federal/State Filing Program for TY2025** (IRS notice 07-JAN-2026), with corrections issued to the 2025 instructions on de minimis reporting [verified] https://www.irs.gov/forms-pubs/about-form-1099-da. Combined with wallet-by-wallet basis tracking, crypto tax admin for a high-frequency bot is materially worse than equities-without-MTM, and vastly worse than futures.

### Crypto — perps and DEX
**Fees are 10–20× better than spot.** Hyperliquid base tier: **0.045% taker / 0.015% maker rebate**, tiers set on rolling 14-day volume with spot volume counting double [verified]. Bybit 0.055%/0.02%. Kraken Futures tier 1 0.05%/0.02%.

**Access.** Binance, Bybit, OKX and Hyperliquid geoblock US persons; I could not fetch Hyperliquid's terms directly (403) to quote the restricted-persons clause, so treat the specific wording as unverified — but the practical position is well established: VPN access is a ToS violation with account-seizure and withdrawal-freeze risk, and it is not a basis on which to build a system you intend to fund. The 2025–2026 answer for a US person is **Coinbase Derivatives US Perps** (nano BTC 0.01, nano ETH 0.1) on a CFTC-regulated DCM [verified].

**Babysitting: worst on the list.** 24/7/365, no close, no weekend. Funding settles every 8 hours (hourly on Hyperliquid). Every bug has a 3am variant. Liquidation cascades are the norm, not the tail.

**Competition.** The retail-accessible arbitrage window closed years ago and the practitioner record is blunt about it. `rthomas6` on a Binance triangular-arb bot: *"made like 0.01 ETH with ~0.3 ETH"* — because *"the price anomaly would be gone before I could make all three trades."* `simonhughes22` on cross-exchange arb: blocked by deposits/withdrawals being offline, transfer times of *"6 hours to a week,"* and the conclusion that opportunities *"are exploited as soon as they exist, I suspect a lot of the time by the exchanges themselves."* `IgorPartola` on a lead-lag bot: *"lost money more often than not,"* attributed to latency and fees. And `jmhyer123`, who reported ~50% over three months on ~$250 of crypto capital, added the decay observation directly: patterns *"quickly disappear as automated trading picks them up. The window goes from 5–10 minutes to seconds or less."* All [anon], https://news.ycombinator.com/item?id=16922538

### Forex
**Brokers.** OANDA US, forex.com, IBKR. OANDA quotes 68 pairs on a core-spread-plus-commission or all-in spread basis.

**Regulatory ceiling.** *"The Commodity Futures Trading Commission (CFTC) limits leverage available to retail forex traders in the United States to 50:1 on major currency pairs and 20:1 for all other pairs"* [verified] https://www.oanda.com/us-en/trading/spreads-margin/. US persons cannot trade CFDs at all, must use registered RFEDs, and are subject to the NFA's FIFO rule which forbids hedged positions — this silently breaks a large fraction of naive strategy designs.

**Outcome data — the best `[verified]` evidence on retail outcomes anywhere.** ESMA's national-regulator analyses found **74–89% of retail CFD accounts lose money, with average losses per client of €1,600 to €29,000**, which is why the EU capped leverage at 30:1–2:1 and mandated negative-balance protection [verified] https://www.esma.europa.eu/press-news/esma-news/esma-agrees-prohibit-binary-options-and-restrict-cfds-protect-retail-investors. HN commenters in the 2018 thread cited IBKR's own disclosure that fewer than half its forex clients were profitable [anon] — I could not re-verify the current quarterly CFTC-mandated disclosure (broker pages 403'd).

**Verdict.** Cheap per notional (~1 bp round trip) but the 50:1 cap turns that into ~50 bps of *equity* per round trip, retail FX flow is largely B-booked against the broker, and the regulator-published loss rates are the worst of any market here. **Nothing recommends it for this profile.**

---

## 5. Where do successful hobbyists actually concentrate — and the 2025–26 shift

The migration path, as best it can be reconstructed:

- **2015–2021: crypto.** Free APIs, no gatekeeping, no PDT, real exploitable inefficiency. The HN record above is the archaeology of that era — and of its closure.
- **2021–2025: CME micros.** Micro/nano contracts made $2–5k accounts viable, PDT didn't apply, real-time data was free with a funded account, and Section 1256 removed the tax-admin tax. This is where the serious solo builders went, and it's still the strongest default.
- **2025–2026: three things moved at once.**
  1. **PDT is being eliminated** (June 2026 → Oct 2027 phase-in), removing the structural reason small accounts avoided US equities.
  2. **US CEX spot fees rose sharply** (Kraken tier 1 now 0.40%/0.80%), pushing crypto retail out of spot and into perps — and simultaneously, **CFTC-regulated US perps arrived** (Coinbase Derivatives), so that migration no longer requires going offshore.
  3. **Options data got cheap** ($29 Massive options tier with real-time Greeks/IV; $1.50/mo IBKR OPRA L1), though options *execution* costs did not improve.

Ecosystem activity corroborates where the tooling energy is: `ccxt` (crypto-only) 43.8k stars / 828 open issues, `nautilus_trader` 28.0k stars, QuantConnect `Lean` 21.4k stars, all with commits within 24 hours [verified, GitHub API]. Crypto still has the largest library ecosystem by a wide margin; multi-asset frameworks are the fastest-growing.

**Best fit for this specific profile** (zero build cost, low recurring cost, capital preservation, learning value, 24/7 babysitting is a cost not a feature):

1. **US equities, daily bars, cash account** — as the learning and iteration vehicle. Data $0–52/mo, execution ~0.3 bps, most forgiving failure mode, PDT gone, and by far the richest free/cheap data ecosystem. Alpaca for the API, Norgate Platinum for bias-free backtests.
2. **CME micro futures** — as the "real system" target once risk plumbing is proven. Cheapest execution on earth at retail size, free data, Section 1256. Do not start here: $50 intraday margin plus no negative-balance protection is the least forgiving environment available.
3. **Crypto perps (Coinbase US Perps, or a non-US venue if not a US person)** — optional third leg, and only after a bug has already cost you money somewhere safer. Free data forever, decent fees, but 24/7 operations is a genuine ongoing time tax.
4. **Options** — good for learning pricing; bad for a first automated system (spread cost, assignment risk, unbounded short-side loss).
5. **Retail FX** — avoid. Regulator-published loss rates, leverage cap that inverts the cost advantage, FIFO rule, B-book counterparty.

---

## 6. Gaps and things I could not verify

- **No Reddit evidence** — Arctic Shift API returned HTTP 500 for the whole session; PullPush rate-limited agents. r/algotrading, r/FuturesTrading and r/Forex failure stories are the biggest missing input. Re-run when the archive recovers.
- **NinjaTrader/Tradovate all-in exchange+NFA fees** are in a JS-rendered table; the ~$0.35/side figure used above is an estimate, not verified. It changes the MES round-trip number by roughly ±0.3 bps.
- **Coinbase Advanced spot fee tiers** are login-gated; low-tier rates unconfirmed from primary.
- **Hyperliquid's restricted-jurisdiction clause** not quoted from primary (403).
- **Current CFTC-mandated quarterly forex profitability disclosures** (the % of non-discretionary retail FX accounts profitable) — broker pages 403'd; only the ESMA CFD figures are `[verified]` here.
- **Cboe 0DTE share of SPX volume** — not retrieved; competition-intensity claim for options rests on structure, not on a fresh statistic.
- **FINRA 26-10 broker-level rollout**: the phase-in means Alpaca/IBKR/Schwab may each adopt on different dates between June 2026 and October 2027. Ask the specific broker before planning around it.

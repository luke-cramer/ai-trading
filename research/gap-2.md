# GAP-2 — Does any crypto strategy survive a US-person legality filter?

Snapshot: **2026-08-29**, BTC ≈ $77,624, ETH ≈ $2,437.74 (Coinbase spot, live).
Evidence tags: **[verified]** primary source fetched + URL · **[promo]** source sells the thing · **[anon]** forum/practitioner · **[unconfirmed]** page blocked/gated in-session.

> **Note on file path:** the task gave two output paths. `crypto-us-venues.md` already held a substantial
> prior report on this beat, so this document was written to `gap-2.md` rather than overwriting it.

**Method / limits.** WebSearch quota was exhausted (200/200) before I started, so everything here is direct
`curl`/WebFetch or a real browser driven against exchange, CFTC, IRS, Treasury and clearinghouse pages.
`coinbase.com`, `cmegroup.com`, `justice.gov` and `bybit.com` block plain fetchers; Coinbase and CME were
obtained via a real browser, justice.gov and bybit.com refused even that. **No practitioner/forum sourcing** —
Reddit and HN were not reachable in this session, so there is no `[anon]` tier below and nothing here is
survivor-tested by real operators. Treat every number as a spec-and-tape derivation, not a lived P&L.

---

## 0. Bottom line

`strat-crypto.md`'s premise — the only residual retail crypto edge lives on venues that geoblock US persons —
is **wrong on venue and right on edge**. There are now three CFTC-regulated onshore routes to perpetual-style
crypto futures, and the leading one is genuinely liquid and *cheaper per side than Hyperliquid*. `markets.md`'s
escape-hatch claim is confirmed with real tape behind it.

But the edge does not survive contact with the risk-free rate. **Every compliant delta-neutral construction I
could price lands at 3.1%–5.4% on deployed capital against a 3.90% 3-month T-bill and 4.15% 1-year
[verified, treasury.gov].** The best case beats cash by roughly 100bps, requires 24/7 margin babysitting across
two legally separate accounts that do not cross-margin, and carries a mixed-straddle tax problem that likely
defers your losses. The venue problem is solved. The edge problem is not.

---

## 1. Coinbase Derivatives (CDE) — primary-source specs

### 1.1 Regulatory plumbing [verified]

- **Coinbase Derivatives, LLC** is a CFTC-designated contract market, **designated 11/23/2020**, formerly LMX
  Labs, LLC d/b/a FairX. https://www.cftc.gov/IndustryOversight/IndustryFilings/TradingOrganizations
- Clearing is at **Nodal Clear**. "All trades are cleared through Nodal Clear, which calculates and processes
  variation margin and funding payments. **Participants must access the market through an approved FCM, with
  all positions cleared in the FCM's name.**"
  https://help.coinbase.com/derivatives/perpetual-style-futures/margin-and-clearing
- FCMs: ABN AMRO Clearing USA, ADM Investor Services, Advantage Futures, Clear Street, **Coinbase Financial
  Markets, Inc.**, Marex, StoneX, Wedbush. IBs: Dorman, Ironbeam, NinjaTrader, Phillip Capital, Tradovate,
  Webull. https://help.coinbase.com/derivatives/general/access

### 1.2 Contract specs, live from the public API [verified]

All pulled unauthenticated from `https://api.coinbase.com/api/v3/brokerage/market/products?product_type=FUTURE`
— **no login, no API key**, which also answers the API-access question: market data is fully self-serve.

| | nano BTC Perp `BIP-20DEC30-CDE` | nano ETH Perp `ETP-20DEC30-CDE` |
|---|---|---|
| Contract size | 0.01 BTC (**$776 notional**) | 0.1 ETH (**$244 notional**) |
| Tick | $5/BTC = $0.05/contract = **0.64 bps** | $0.50/ETH = $0.05 = **2.05 bps** |
| Nominal expiry | 2030-12-20 (`contract_expiry_type: EXPIRING`) | 2030-12-20 |
| 24h volume | 563,760 contracts = **$437.6M** | 377,435 = $92.0M |
| Open interest | 192,974 = **$149.8M** | 347,050 = $84.6M |
| Funding interval | **3600s (hourly)** | hourly |
| Funding rate (snapshot) | 0.000006/hr → **5.26% APR** | 0.000009/hr → **7.88% APR** |
| Intraday margin | ~10.0% (10x) | ~10% |
| **Overnight margin** | long 24.56% / **short 30.64%** | long 24.53% / short 33.48% |
| Trading | `twenty_four_by_seven: true` | same |
| Launched (`new_at`) | **2025-07-18** | 2025-07-18 |

A second pull ~1h later gave funding 0.000006 and 0.000009 again (an earlier sibling-report pull saw 0.000007 /
0.000011). Call BTC perp funding **5.3–6.1% APR** and ETH **7.9–9.6% APR** as of this week.

**The nominal 2030 expiry is a red herring but worth flagging honestly:** the API reports
`contract_expiry_type: EXPIRING` with a 2030-12-20 date and ~136bn ms to expiry, while Coinbase's help center
markets these as perpetual-style. Economically it is a perp with hourly funding; the "perp vs 5-year future"
ambiguity matters only for the §1256 argument in §6, where it cuts *in favor* of clean futures treatment.

### 1.3 Fee schedule [verified — Coinbase's own PDF, effective 2026-08-17]

https://assets.ctfassets.net/k3n74unfin40/4NUcmzSIiQpa6kyg5t0eE6/e46de319573b782f3dbee6794b7fbad1/Fee_Schedule_as_of_08172026.pdf

Fees are **per side, per contract**:

| Product group | Market Maker | Non-Professional | Professional |
|---|---|---|---|
| Bitcoin/Ether/Solana/XRP Futures (BTI, ETI, SLC, XRL) | $0.45 elec / $0.20 block | $0.75 / $0.20 | $0.75 / $0.20 |
| **All nano + all Perp-Style** (BIT, **BIP**, ET, **ETP**, SLP, XPP, …) | $0.07 / $0.01 | **$0.10 / $0.01** | **$0.10 / $0.01** |

Converted to bps at snapshot prices:

- **BIP: $0.10 on $776 = 1.29 bps/side, 2.58 bps round turn.** That is genuinely cheap — cheaper than
  Hyperliquid's taker tier and roughly half Binance's taker.
- **ETP: $0.10 on $244 = 4.10 bps/side, 8.20 bps round turn.** The flat per-contract fee makes the nano ETH
  perp **3.2× more expensive in bps than the nano BTC perp.** Same for the tick: 2.05 bps vs 0.64 bps. Any
  strategy on ETP is structurally handicapped; trade BIP.

**Nuance the exchange buries:** "Non-Professional Trader" requires, among other things, "**C. Not using a fully
automated order generating computer system**" [verified, same PDF]. An algo trader is a *Professional*. For
nano/perp products this is economically irrelevant (both $0.10), but it is a real classification and it changes
the fee on the full-size BTI/ETI contracts to nothing better.

### 1.4 Funding mechanism [verified]

https://help.coinbase.com/derivatives/perpetual-style-futures/funding-rate

- `Premium = TWAP([(Futures mark − spot mark)/spot mark/24], 1 hour, 3min)` — 20 samples/hour, **scaled down by
  a factor of 24**, then smoothed `(Premium × 0.75) + (Previous Funding Rate × 0.25)`.
- Calculated hourly by Nodal Clear; **debits/credits applied twice daily** at the mid-day and end-of-day margin
  cycles, "as separate cash adjustment entries in the clearing files [that] do not affect variation margin."
- **"Real time and projected funding rate data is published via FIX and SBE market data. Historical funding rate
  data is available upon request."**

That last line is a material research cost: **you cannot backtest CDE funding from public history.** You can
poll `funding_rate` off the free REST endpoint hourly and build your own series going forward, but any claim
about CDE's historical funding distribution — including mine — is a snapshot, not a distribution. Cboe is the
opposite (§5.1) and publishes a downloadable file.

---

## 2. Is the carry trade actually executable? Priced end-to-end

### 2.1 The spot leg is the binding constraint [verified]

Coinbase Advanced's fee page is login-gated (I confirmed: `coinbase.com/advanced-fees` 403s to fetchers and
redirects a browser to `login.coinbase.com`) — `markets.md` was right. But **Coinbase Exchange's schedule is
public** and is the same order-book venue Advanced routes to
(https://help.coinbase.com/en/exchange/trading-and-funding/exchange-fees, fetched via browser):

| 30-day volume tier | Taker | Maker |
|---|---|---|
| **$0K–$10K** | **60 bps** | **40 bps** |
| $10K–$50K | 40 bps | 25 bps |
| $50K–$100K | 25 bps | 15 bps |
| $100K–$1M | 20 bps | 10 bps |

[unconfirmed] I could not verify that Coinbase *Advanced* uses identical numbers; the Advanced schedule is
gated. Coinbase's own disclosure says "All trades from your Primary Balance are executed through Coinbase
Exchange's central limit order book" [verified,
https://help.coinbase.com/en/coinbase/trading-and-funding/pricing-and-fees/fees], which makes identity likely
but not proven. **Coinbase One** offers "zero trading fees ... with certain limitations," but the same page
warns "members may still have a spread included in their quoted prices" and it does not apply to the 1% limit-
order execution fee on simple orders [verified, same page]. That is a retail-broker benefit with an undisclosed
volume cap, not a clean way to run a $50k order-book leg — I would not underwrite the carry trade on it.

**A $10k–50k account is in the worst tier.** 60 bps taker × 2 sides = **120 bps round trip on the spot leg**,
versus 2.58 bps for the entire perp round trip. The spot leg costs ~46× the futures leg.

### 2.2 The FCM commission is the one number I could not get [unconfirmed]

The $0.10/side above is the **exchange** fee. Your FCM (Coinbase Financial Markets, or NinjaTrader/Tradovate/
Ironbeam as IB) charges a separate commission. Coinbase's futures commission schedule is behind login;
help.coinbase.com has no futures-fee article (the Derivatives help index has an "Exchange Fees" page only);
NinjaTrader's and Ironbeam's public pricing pages did not render a crypto per-contract line to a fetcher.
**Treat $0.10/side as a floor, not the all-in.** At retail FCM rates of roughly $0.25–$1.00/contract/side this
would add 3–13 bps/side on a $776 contract — which would swamp the exchange fee and change the numbers below
materially. This is the single largest unresolved cost in this report and is checkable in five minutes by
anyone with a funded account.

### 2.3 Four constructions, priced

Capital = spot notional (1.0) + futures margin. Perp short overnight margin 30.64%; dated future 23.44%.

| Construction | Gross | Capital mult. | Year 1 | Steady state |
|---|---|---|---|---|
| Short BIP perp / long spot, tier-0 taker, margin earns 0% | 5.26% | 1.306 | **3.09%** | 4.03% |
| …same, margin cash earns 3.90% | 5.26% | 1.306 | **4.00%** | 4.94% |
| …tier-1 maker (25bps×2), margin earns 3.90% | 5.26% | 1.306 | **4.54%** | 4.94% |
| Short BIT dated / long spot, 5.7% fwd basis, margin earns 3.90% | 5.70% | 1.234 | **4.37%** | 5.36% |

**Benchmark: 3-month T-bill 3.90%, 6-month 4.02%, 1-year 4.15% on 2026-08-28** [verified,
https://home.treasury.gov/resource-center/data-chart-center/interest-rates/daily-treasury-rates.csv/2026/all].

Read that table honestly: **in year one, at realistic retail fee tiers, the compliant perp carry trade returns
less than a Treasury bill.** It only clears cash if (a) you hold long enough to amortize the 120bps spot entry
over multiple years, and (b) your FCM pays interest on margin cash. **(b) is decisive and unverified** — it is
worth ~91bps of the ~104bps of excess return. If Coinbase Financial Markets pays 0% on futures margin (common
for crypto-native FCMs), the whole trade is a worse T-bill.

### 2.4 The basis, measured three ways

Coinbase settlement prices, 2026-08-28: BIP perp 77,525; BIT-25SEP26 78,030; BIT-30OCT26 78,460.

- **Front basis:** BIT Sep vs BIP perp = 505 pts / 28d = **8.49% ann.** Against live spot 77,624: **7.42% ann.**
- **Inter-month (Coinbase):** Oct vs Sep = 430 pts / 35d = **5.75% ann.**
- **Inter-month (CME):** MBT Dec26 78,925 vs Sep26 77,835 = **5.62% ann**; Dec27 83,270 vs Sep26 = **5.59% ann.**

The two venues' forward curves agree at **~5.6–5.8%**, which is the number I would trust. The 7.4–8.5% front
basis is measured against a spot mark taken at a slightly different instant during a −2.6% day and is probably
overstated; **do not build a Top-20 entry on an 8% carry assumption.** Note also that Coinbase's Sep future
settled 195 pts (25 bps) above CME's Sep future — different indices and settlement times, but that gap is
itself larger than any fee in this report, which tells you the marks are noisy at the bps level where this
trade lives.

### 2.5 Roll cost kills the dated version

Coinbase lists nano BTC futures **monthly** (Sep/Oct/Nov). Open interest: **Sep 162,272 contracts vs Oct 590
vs Nov 0** [verified, API]. CME MBT is the same shape: Sep volume 78,747, Oct 809, Nov 30, Dec 11 [verified,
cmegroup.com volume & OI, trade date 2026-08-28]. The back month is empty until roll week, so you cross a wide
spread every time.

- Monthly roll, 12×/yr at 5–10 bps all-in = **0.6–1.2%/yr**, which erases the entire excess-over-cash.
- Quarterly roll (CME has Mar/Jun/Sep/Dec), 4× at ~8 bps = **0.32%/yr** — survivable.

**Conclusion: if you run cash-and-carry, run it on quarterly CME contracts, not monthly Coinbase ones.**

---

## 3. CME cash-and-carry — the classic compliant alternative [verified]

Micro Bitcoin (MBT), https://www.cmegroup.com/markets/cryptocurrencies/bitcoin/micro-bitcoin.contractSpecs.html:

- Contract unit **0.10 BTC** (~$7,790), settled to the CME CF Bitcoin Reference Rate, **financially settled**.
- Tick $5.00/BTC = **$0.50/contract** (0.64 bps); BTIC and calendar-spread tick $0.10/contract.
- **24/7** on Globex except Sat 02:00–04:00 CT and daily 16:00–16:02 CT.
- Listed: 6 consecutive months + 4 additional quarterlies + a second Dec.
- **Margin: maintenance short $1,713 for Sep 2026 = 22.0% of notional**; vol scan 50%
  (https://www.cmegroup.com/markets/cryptocurrencies/bitcoin/micro-bitcoin.margins.html).
- **Liquidity is the best of any venue here: 84,852 contracts on 2026-08-28 = $658M notional; OI 54,060 =
  $420M.**
- Minimum viable size: one contract ≈ $7,790 of futures + a matching spot leg → **a ~$9,600 position**, so a
  $10k account can do exactly one unit and a $50k account about five. Granularity is 8× coarser than Coinbase's
  nano ($776), which matters when you are trying to stay delta-flat.
- CME per-contract exchange+clearing fees for a non-member retail account were **not** obtainable in-session
  [unconfirmed]; retail all-in is typically a few dollars/side, which on $7,790 is a few bps.

At the verified 5.6% forward basis, 22% margin, quarterly rolls: **~4.3–5.3% on capital depending on whether
margin earns interest** — the same band as Coinbase, with better liquidity, coarser granularity, and a cleaner
tax story (§6).

---

## 4. The liquidity filter kills two of five venues

| Venue / product | Daily notional | OI notional | Verdict |
|---|---|---|---|
| **CME MBT micro BTC** (dated) | **$659M** | **$420M** | Real |
| **Coinbase BIP nano BTC perp** | **$438M** | **$150M** | Real |
| Coinbase BIT nano BTC Sep (dated) | $106M | $126M | Real, front month only |
| **Bitnomial BTC perp** | $4.7M | **$0.33M** | Marginal |
| **Cboe PBT continuous BTC** (20d avg) | **$85K** | **$530K** | **Dead** |

Sources: Coinbase API [verified]; CME volume & OI page [verified]; Bitnomial `/market/data` rendered in browser
[verified]; Cboe `cfevoloi.csv` [verified].

### 4.1 Cboe Continuous Futures — a perfect product nobody trades

Cboe Bitcoin (**PBT**) and Ether (**PET**) Continuous Futures listed **2025-12-15**, up to three 120-month
expirations, 0.01 BTC contract size, tick $1.00/BTC = **$0.01/contract (0.13 bps — the tightest tick of any
venue here)**, daily cash adjustment at 15:00 CT against the Cboe Kaiko Real-Time Rate
[verified, https://cdn.cboe.com/resources/membership/Cboe_Bitcoin_Continuous_Futures_Contract_Specifications.pdf].
Uniquely, **Cboe publishes the funding series as a downloadable CSV** (current and prior trading date)
[verified, https://www.cboe.com/tradable-products/cryptocurrency/continuous-futures/funding-rate-data/].

I pulled it. On trading date 2026-08-28 the final (15:00:04) funding rates were **PBT 0.00008251/day → 3.01%
APR** and **PET 0.00034970/day → 12.76% APR**, clamped at ±0.002/day
[verified, https://www.cboe.com/us/futures/cryptocurrency/continuous-futures/funding-rate-data/csv/previous-trading-date/
and the Funding Amount Methodology PDF].

A 12.8% APR short-funding rate on a CFTC-regulated venue would be the single best line in this whole research
spike — except that **PET's open interest is ~$68K and PBT's is ~$530K, with many days of literally zero
volume** (2026-08-05 through 2026-08-18: PBT traded 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0 contracts). The 12.76%
funding rate is an artifact of a quote-driven basis in a market with no participants. **You cannot deploy
$10k–50k here.** It also is not 24/7 — CFE runs Mon–Fri with a 16:00 CT close [verified, PBT spec sheet], so a
delta-neutral book has an unhedgeable weekend gap on the futures leg while spot trades continuously.

### 4.2 Bitnomial — real, crypto-native, and now Kraken's

Bitnomial Exchange, LLC is a DCM **designated 04/17/2020** [verified, CFTC]. It operates DCM + DCO + FCM in one
group and claims "**First-ever CFTC-regulated perpetual futures**," crypto as margin collateral, up to 6x
leverage, and a unified collateral pool across perps/futures/options/spot [promo, https://bitnomial.com/].
Explicitly open to US residents [promo, same].

**Payward (Kraken's parent) completed its acquisition of Bitnomial on 2026-05-01** [verified,
https://bitnomial.com/news/2026-05-01/payward-completes-acquisition-bitnomial/]: "Payward now owns the complete
US derivatives stack — a Futures Commission Merchant (FCM), a Designated Contract Market (DCM), and a
Derivatives Clearing Organization (DCO)... We're starting with spot margin on Kraken, with **perpetuals and
options to follow**." So the answer to "Kraken Futures US" is: **coming, through Bitnomial's licenses, not yet
launched on Kraken** as of this snapshot.

Liquidity today is thin: 24h total across all Bitnomial products $62.4M, but **total open interest across the
entire exchange is $1.60M**, of which the BTC perp is $325K (417 contracts) and the ETH perp $273K [verified,
rendered `/market/data`]. Watch it; don't fund it yet.

### 4.3 Venue attrition [partially verified]

- **BitMEX: confirmed closing.** Its homepage carries "[Important Announcement] **BitMEX Exchange is closing on
  23 September 2026 at UTC 04:00:00.**" [verified, https://www.bitmex.com/] — the sibling report's date is right.
- **AscendEX 2026-07-01 shutdown:** [unconfirmed], not checked.
- **Coinbase/Deribit:** Coinbase's futures product schema now carries a `deribit_product_details` field, but it
  is null on all 100 CDE products [verified, API] — no US-facing Deribit options are surfaced through this API
  yet. Whether the acquisition opens US access to crypto options is **[unconfirmed]**.

---

## 5. Geoblock verification

**Hyperliquid — verified live, from this machine's US IP.** The app rendered: "**You are accessing the website
from a restricted jurisdiction - see the Terms of Use.**" Terms last updated 2026-06-15, §1.6: "The Interface
is not available to '**Restricted Persons**.' ... Restricted Persons include: (a) persons or entities who
reside in, are located in, are incorporated in, or have a registered office in **the United States of America
or Ontario, Canada** ... Restricted Persons are **strictly prohibited** from accessing or using the Interface."
§1.9: "you expressly represent and warrant that ... **you are not using any technology or method to disguise
your location or otherwise evade any access restriction**." [verified, https://app.hyperliquid.xyz/terms]

Two honest nuances. First, §1.1–1.2 disclaim that the operator controls the chain: "The Company does not own,
control, or operate Hyperliquid ... **The Interface is not the exclusive means of accessing Hyperliquid**." The
ToS restricts the *website*, not the protocol — which is why "just use the API" is a widely repeated idea. That
does not make it lawful for a US person to trade offshore leveraged derivatives; it only means the ToS is not
the operative prohibition. **I am not qualified to opine on that and this report does not.**

**Binance — enforcement verified, ToS not.** CFTC charged Binance and CZ on **2023-03-27** with offering
"commodity derivatives transactions to and for U.S. persons from July 2019 through the present," and alleged
the firm "instructed its customers — in particular its commercially valuable U.S.-based VIP customers — on the
best methods for evading Binance's compliance controls," including instructing US customers "to access the
trading facility through a **virtual private network** to avoid Binance's IP address-based controls or create
'new' accounts through off-shore shell companies" [verified,
https://www.cftc.gov/PressRoom/PressReleases/8680-23]. binance.com/en/terms returned an empty SPA shell to every
fetcher and archive.org's snapshot is a 202 placeholder [unconfirmed].

**Bybit:** bybit.com refused both fetcher and browser navigation; the archive.org snapshot renders empty
[unconfirmed]. I could not verify its restricted-persons clause.

**OKX $505M DOJ settlement: could not verify.** The URL slug returns justice.gov's soft-404, archive.org has no
snapshot of it, and justice.gov blocked browser navigation. **Do not carry the $505M figure forward as
verified** on the strength of this report.

**"14,000+ accounts closed for geolocation fraud in 2025 with forced liquidation": could not verify** — no
primary source reachable without WebSearch. Flag it as an unsourced claim in `strat-crypto.md`.

**What is verifiable about the consequence of VPN use** is narrower and more useful than the rumor: the CFTC's
Binance action establishes that (i) *the exchange*, not the retail customer, is the enforcement target, and
(ii) the regulator treats VPN evasion as evidence of the venue's willfulness. The customer-side risk that is
actually documented is contractual, not criminal: Hyperliquid's §1.9 makes location-disguising a breach of the
terms you warranted, which is the hook for account closure. **Account seizure vs. freeze vs. closure is
[unconfirmed]** and I would not assert a specific outcome.

---

## 6. Tax — what is settled and what genuinely is not

**Settled (statute, verified at https://www.law.cornell.edu/uscode/text/26/1256):**

1. §1256(a)(3): gain/loss is **40% short-term, 60% long-term**, plus year-end mark-to-market under (a)(1).
2. §1256(b)(1)(A): a **regulated futures contract** is a §1256 contract.
3. §1256(g)(1): an RFC is a contract "(A) with respect to which the amount required to be deposited and the
   amount which may be withdrawn **depends on a system of marking to market**, and (B) which is **traded on or
   subject to the rules of a qualified board or exchange**."
4. §1256(g)(7)(B): a qualified board or exchange includes "**a domestic board of trade designated as a contract
   market by the Commodity Futures Trading Commission**."

CDE is a CFTC-designated contract market [verified, CFTC], and its positions are margined and marked to market
twice daily through Nodal Clear [verified, Coinbase help center]. **On the face of the statute, every element
for §1256 treatment of the nano BTC Perp is satisfied.** Bitnomial markets the same conclusion — "Blended 60%
long term, 40% short term US capital gains tax treatment on eligible trades" with a consult-your-advisor
asterisk [promo, https://bitnomial.com/].

**Genuinely unresolved — two issues, both material, neither addressed by any guidance I could find:**

- **§1256(b)(2)(B)** excludes "any interest rate swap, currency swap, basis swap, ... **commodity swap**, ... or
  **similar agreement**" [verified]. A never-expiring contract whose economics are delivered through a periodic
  funding payment referencing the futures-vs-spot spread has swap-like mechanics. Whether a DCM-listed
  perpetual-style future is a "similar agreement" is, as far as I can find, unaddressed. (Coinbase's nominal
  2030 expiry and Cboe's 120-month expiry arguably exist partly to keep these looking like futures.)
- **Funding payments may not be §1256 gain at all.** Coinbase states funding is applied "as separate cash
  adjustment entries in the clearing files and **do not affect variation margin**" and is "recorded
  independently of variation margin" [verified, help center]. Whether that stream is swept into §1256
  mark-to-market or characterized separately (potentially as ordinary income) is an open question I found no
  guidance on. For a carry trade, funding *is* the entire return — so this is not a footnote.

**The mixed-straddle problem — the finding that most changes the answer.** §1256(a)(4) turns off §1092 and
§263(g) only "**if all** the offsetting positions making up any straddle consist of section 1256 contracts"
[verified]. A delta-neutral book of **spot BTC (not a §1256 contract) + short nano perp (a §1256 contract) is a
mixed straddle**, so §1092 loss deferral and §263(g) carrying-charge capitalization are back on. In a trade
whose entire thesis is "collect 5% and stay flat," having your losing leg's losses deferred while the winning
leg marks to market at year end is a real, recurring administrative and cash-flow cost. **A futures-only
construction (e.g. short dated CME future vs. long CME perp-style, or a calendar spread) avoids this; a
spot-plus-futures construction does not.**

**Spot crypto:** "For U.S. tax purposes, digital assets are considered **property, not currency**." Form
1099-DA broker reporting effective **2025-01-01** for gross proceeds, **basis reporting from 2026**, with
good-faith transition relief under Notices 2024-56 and 2025-33 [verified,
https://www.irs.gov/filing/digital-assets]. That page contains **no** mention of wash sales or §1256 for
digital assets. §1091 by its terms applies to "stock or securities"; **I could not verify in-session whether
any 2025–2026 legislation extended wash-sale treatment to digital assets** — treat the "no wash sale rule"
assumption as [unconfirmed], not settled.

*Nothing here is tax advice; it is a report of what the cited sources say.*

---

## 7. Babysitting load and the failure mode nobody prices

- **The two legs live in two legally separate accounts that do not cross-margin.** Spot sits at Coinbase
  (Advanced/Exchange); the perp is "cleared in the FCM's name" at Nodal Clear via a separate futures account
  [verified]. A BTC rally makes your short perp lose while your spot leg gains — but the spot gain **cannot
  meet the futures margin call.** You must move cash between accounts, and Nodal Clear runs **two margin cycles
  a day** on a market that trades **24/7**. That is the operational shape of every blown delta-neutral account:
  solvent in aggregate, liquidated on one leg.
- Short overnight margin is **30.64%** on BIP, so a ~33% adverse move against an unfunded short wipes the
  posted margin. You would run it at half that, which halves the return on capital again.
- Funding is **variable and can go negative**; the 5.26% snapshot is one hour of one day, and no public history
  exists to characterize the distribution (§1.4). The honest statement is that nobody — including this report —
  can tell you the realized 12-month funding on this venue.
- Realistic load: hourly automated margin/funding polling, an alerting path, and manual cash sweeps between two
  institutions on rallies. Call it **30–60 min/week steady-state, spiking to hours on trend days**, on top of
  building your own funding history because the venue does not publish one.

---

## 8. VERDICT

**Does any crypto strategy survive the US-person legality filter? Yes — one, barely, and it should rank low.**

1. **Delta-neutral perp funding carry on Coinbase Derivatives (short BIP / long Coinbase spot).**
   Venue: CDE via an approved FCM. Net expected return **3.1%–4.9% on deployed capital** (year 1 vs steady
   state; the 4.9% requires the unverified assumption that your FCM pays interest on margin cash). Benchmark
   3.90–4.15% T-bills. Recurring cost: $0 data (free public REST API), exchange fee 2.58 bps round turn, spot
   leg 120 bps round trip at tier 0, plus an **unquantified FCM commission**. Babysitting: 30–60 min/week with
   24/7 tail risk. **Include in a Top-20 ranking only as a "learn the plumbing" entry, ranked below cash.**
   It is an excellent *engineering* project — real DCM, real clearinghouse, real funding mechanics, free API —
   and a poor *return* project.

2. **CME quarterly cash-and-carry (short MBT / long spot).** ~4.3–5.3% on capital at the verified 5.6% forward
   basis; best liquidity of any venue ($659M/day, $420M OI); quarterly rolls cost ~32 bps/yr vs ~60–120 bps for
   Coinbase's monthly ladder; cleanest §1256 story. Minimum viable ~$9.6k/unit. **Ranks above #1** on
   robustness, below it on granularity and on 24/7 fit.

3. **Everything else: no.** Cboe PBT/PET is a well-designed dead market ($85K/day, days of zero volume) despite
   publishing the best funding data of anyone — do not be seduced by its 12.76% PET print. Bitnomial is real
   and now Kraken-owned but has **$1.6M of open interest exchange-wide**; revisit in 2027 when Payward launches
   perps on Kraken/NinjaTrader. Kraken US perps do not exist yet. BitMEX closes 2026-09-23. Offshore venues
   (Hyperliquid, Binance, Bybit) are contractually closed to US persons — Hyperliquid verified live from this
   IP, with an explicit warranty against location-disguising technology.

**The honest summary for the ranking:** the jurisdiction hole `strat-crypto.md` opened is closed — a US person
can legally trade a liquid, cheap, CFTC-regulated perpetual with a free self-serve API. But the ~4–10% net APY
that made offshore funding carry interesting does not exist onshore. Onshore funding is 5.3% gross, the
forward basis is 5.6%, capital efficiency is ~0.77×, and the risk-free rate is 3.90%. **The compliant crypto
carry trade is a T-bill with basis risk, two-account margin fragility, a mixed-straddle tax problem, and a
24/7 pager.** Roughly one Top-20 slot, ranked on learning value, not on edge.

### Open items worth 30 minutes each
1. **The FCM commission** (login-gated) — largest unresolved cost; could flip #1 negative.
2. **Does Coinbase Financial Markets pay interest on futures margin?** Worth ~91 bps of ~104 bps of excess return.
3. Whether Coinbase Advanced's tier table matches Coinbase Exchange's.
4. OKX/DOJ $505M and the "14,000 accounts" claim — both unverifiable here; strip from sibling reports until sourced.
5. Whether 2025–26 legislation extended the wash-sale rule to digital assets.

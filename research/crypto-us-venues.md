# Crypto strategies through a US-person legality filter — venues, economics, tax

Research date: **2026-08-28 / 2026-08-29**. All prices/rates are that snapshot. BTC ≈ **$77,400**, ETH ≈ **$2,427** (derived from CDE's own published futures marks, below).

Evidence tags: **[verified]** = primary source fetched, URL cited · **[anon]** = forum/practitioner · **[promo]** = source sells the thing · **[unconfirmed]** = page 403'd / 404'd / login-gated in this session.

**Method note:** WebSearch quota was exhausted at the start of this task. Everything below comes from direct WebFetch, curl, or a real headless browser against exchange, CFTC, IRS and clearinghouse pages. Coinbase, CME, IBKR and justice.gov all block plain curl/WebFetch (Cloudflare/Akamai); the Coinbase and CME material was obtained by driving a real browser. Anything I could not reach is marked, not guessed.

---

## 0. Headline answer

**The jurisdiction hole closes.** `strat-crypto.md`'s premise — that the only residual retail crypto edge (perp funding carry) lives exclusively on venues that geoblock US persons — is **false as of August 2026**. There are now at least **three** CFTC-regulated onshore routes to perpetual-style crypto futures for a US person, and the leading one has real liquidity, a published fee schedule, a published funding-rate series, and a self-serve retail API.

`markets.md`'s escape-hatch claim is **confirmed and then some**: Coinbase Derivatives nano BTC Perp is not a paper listing. It carried **~$149M open interest and ~$641M/day notional volume** on the day sampled.

---

## 1. Coinbase Derivatives (CDE) — primary-source specs

### 1.1 Regulatory status and plumbing

- **Coinbase Derivatives, LLC** is a CFTC-designated contract market, **designated 11/23/2020** — originally LMX Labs, LLC d/b/a FairX, later rebranded Coinbase. [verified] https://www.cftc.gov/IndustryOversight/IndustryFilings/TradingOrganizations
- Clearing is at **Nodal Clear**, a CFTC-registered DCO, which "is proud to be the first clearing house to ever offer 24x7 clearing for margined futures contracts" and clears for "Nodal Exchange and Coinbase Derivatives." [verified] https://www.nodalclear.com/
- "Participants must access the market through an **approved FCM**, with all positions cleared in the FCM's name." [verified] https://help.coinbase.com/derivatives/perpetual-style-futures/margin-and-clearing
- FCMs: ABN AMRO Clearing USA, ADM Investor Services, Advantage Futures, Clear Street, **Coinbase Financial Markets, Inc.**, Marex, StoneX, Wedbush. IBs: Dorman, Ironbeam, NinjaTrader, Phillip Capital, Tradovate, Webull. [verified] https://help.coinbase.com/derivatives/general/access — **Interactive Brokers** also carries the products (own landing page, below) though it is absent from that help-center table.

### 1.2 Contract specifications [verified]

| | nano BTC Perp | nano ETH Perp | nano SOL Perp | nano XRP Perp |
|---|---|---|---|---|
| Symbol / prod code | **BIP** / 3986 | **ETP** / 3988 | SLP / 4642 | XPP / 4731 |
| Contract size | 0.01 BTC | 0.10 ETH | 5 SOL | 500 XRP |
| Tick (index pts) | 5 | 0.5 | 0.01 | 0.0001 |
| Tick value | $0.05 | $0.05 | $0.05 | $0.05 |
| Notional @ snapshot | **~$774** | **~$243** | ~$519 | ~$690 |
| Tick as bps of notional | **0.65 bps** | **2.06 bps** | — | — |
| Max order qty | 5,000 | 5,000 | — | — |

Sources: https://help.coinbase.com/derivatives/perpetual-style-futures/contract-specifications and the CDE Product Reference PDF (03-02-2026) https://assets.ctfassets.net/k3n74unfin40/4lqaVpEz7Ey6HZSrNM6fyl/07b6ba282c84002bb81951bf21a06be2/CDE_Product_Reference_-_03_02_2026.pdf

**Rulebook, Rule 1129 (nano Bitcoin Perp), August 2026** [verified] https://assets.ctfassets.net/k3n74unfin40/23uJIkpQ2WjBwAvgpvKG6u/e47d63995663375e1275564a11dac608/Coinbase_Derivatives_Rulebook_Aug172026.docx.pdf:
- "Only one (1) BIP Contract will be listed at any given time. **The Contract has no expiration date and no final settlement date.**"
- Index = **MarketVector™ Coinbase Bitcoin Benchmark Rate**, calculated by MarketVector Indexes GmbH.
- Position limit **6,500,000 contracts**; **reportable level 25 contracts** (= ~$19,350 notional — a $50k book is a reportable position and will be reported by your FCM).
- Price fluctuation limits: hourly Reference Price ±10%, 1-minute halt on breach.
- Cash settled.

**Note a real discrepancy:** the June 2025 launch blog described these as "long-dated futures contracts (**5 year expirations**) with 24/7 trading hours" [verified] https://www.coinbase.com/blog/coming-july-21-us-perpetual-style-futures, and the live symbols still carry a dated suffix (`BIPZ30`, `ETPZ30` — December 2030). The August 2026 rulebook and the current help center both say "no expiration date and no final settlement date." Treat the contract as economically perpetual with a legacy Z30 symbol; the §1256 analysis in §4 is unaffected either way.

**Hours:** "The contracts trade continuously, 24 hours a day, 7 days a week, with the exception of a **1 hour maintenance period on Fridays from 5pm–6pm ET**." [verified]

### 1.3 Fee schedule — per side, per contract [verified]

From the CDE Fee Schedule PDF effective trade date June 17, 2026 https://assets.ctfassets.net/7ca8qfn907uv/5SapocS5FUm4XCjgbG9Vcn/b27be194c7b31fd489c229f0b83d8bb7/Fee_Schedule_6.17.2026.pdf (a newer 8/17/2026 schedule exists at https://assets.ctfassets.net/k3n74unfin40/4NUcmzSIiQpa6kyg5t0eE6/e46de319573b782f3dbee6794b7fbad1/Fee_Schedule_as_of_08172026.pdf; I extracted the 6/17 version):

| Product group | Market Maker (elec/block) | Non-Professional (elec/block) | Professional (elec/block) |
|---|---|---|---|
| Bitcoin/Ether/Solana/XRP Futures (BTI, ETI, SLC, XRL) | $0.45 / $0.20 | $0.75 / $0.20 | $0.75 / $0.20 |
| **All nano + all Perp-Style contracts** (BIT, **BIP**, ET, **ETP**, SLP, XPP, …) | $0.07 / $0.05 | **$0.10 / $0.05** | **$0.10 / $0.05** |

**Trap worth flagging:** the schedule's "Non-Professional Trader" definition requires the account be "**C. Not using a fully automated order generating computer system**." An algo trader is a *Professional* by CDE's own definition. On nano contracts this costs **nothing** (Non-Pro and Pro are both $0.10 electronic), but it changes market-data entitlement classification at every broker, and professional market-data fees are a real recurring cost line an algo builder should price before signing up.

### 1.4 Broker commissions on top [verified]

Interactive Brokers publishes per-contract commissions https://www.interactivebrokers.com/en/pricing/commissions-futures.php?re=amer:

| Contract | IBKR commission ≤1,000 contracts/mo | >20,000/mo |
|---|---|---|
| **Coinbase Nano Bitcoin (BIT/BIP) and Nano Ether (ET/ETP)** | **USD 0.20/contract** | USD 0.11 |
| CME Bitcoin Micro (MBT) | USD 0.85 | USD 0.43 |
| CME Bitcoin Friday (BFF) | USD 0.25 | USD 0.13 |
| CME Ethereum Micro (MET) | USD 0.20 | USD 0.11 |
| CME Bitcoin full-size (BRR) | USD 5.00 | USD 2.60 |

Exchange and regulatory fees are additional pass-throughs. NFA assessment and any Nodal Clear clearing fee are **[unconfirmed]** — not published on the pages I could reach.

Tradovate advertises "$0 Market Data Fees & Day Trade Margins as low as $25" on Coinbase Derivatives nano contracts [promo] https://info.tradovate.com/coinbase-derivatives-nano-bitcoin.

### 1.5 All-in cost of the perp leg

nano BTC Perp notional **$774**:

| Component | $/side | bps/side |
|---|---|---|
| CDE exchange fee | $0.10 | 1.29 |
| IBKR commission | $0.20 | 2.58 |
| NFA + clearing | ~$0.02–0.04 [unconfirmed] | ~0.3–0.5 |
| **Subtotal** | **~$0.32–0.34** | **~4.2–4.4** |
| Crossing 1 tick | $0.05 | 0.65 |

**Round turn ≈ 9–10 bps** on the perp leg. nano ETH Perp is worse: $0.10 exchange fee on a $243 notional is **4.1 bps/side** and one tick is **2.06 bps**, so an ETH round turn is roughly **17–19 bps**. **For carry, use BIP, not ETP** — the fee is a flat dollar amount and the BTC contract is 3.2× the notional.

### 1.6 Liquidity — this is a real venue

Exchange-published stats, homepage snapshot 2026-08-28 [verified, exchange's own numbers] https://www.coinbase.com/derivatives:

| Contract | Open interest (contracts) | Daily volume (contracts) | OI notional | Volume notional |
|---|---|---|---|---|
| **nano Bitcoin Perp (BIP)** | 192,974 | 827,523 | **~$149M** | **~$641M/day** |
| nano Bitcoin (BIT, dated) | 199,583 | 210,777 | ~$154M | ~$163M/day |
| **nano Ether Perp (ETP)** | 347,050 | 564,952 | ~$84M | ~$137M/day |
| nano Ether (ET, dated) | 101,120 | 127,008 | ~$25M | ~$31M/day |
| nano XRP Perp | 42,915 | 124,665 | ~$30M | — |
| nano Solana Perp | 30,059 | 197,162 | ~$16M | — |

Cross-check from Coinbase's consolidated derivatives market-data page, 8/29/26 [verified] https://www.coinbase.com/market-data/derivatives: **Coinbase Derivatives daily OI $1.13B, 24H volume $1.65B**. Consistent.

`strat-crypto.md`'s own risk rule — "avoid instruments under $50M OI" — is satisfied by BIP ($149M) and ETP ($84M), and *not* by the XRP/SOL perps. That rule is the right filter and it points at exactly two instruments.

### 1.7 Funding mechanism [verified]

https://help.coinbase.com/derivatives/perpetual-style-futures/funding-rate

- Computed **hourly**. `Premium = TWAP([(Futures mark − spot mark)/spot mark/24], 1 hour, 3min)` — 20 three-minute samples per hour.
- Smoothed: `Funding = Premium×0.75 + PreviousFunding×0.25`.
- Marks fall back from 3m VWAP → 3m TWAP of the BBO midpoint → carried-forward basis when there are no quotes.
- **Accrues hourly, cash-settled twice daily** at the mid-day and end-of-day margin runs, "as a **separate cash adjustment**… recorded independently of variation margin in the clearing file." Rulebook Rule 1129(g) says the same. "FCMs may choose to process the cash adjustments once or twice per day."
- Worked example given by Coinbase: "+0.1% for an hour, 1 nano BTC Perp long, BTC at $100,000 → funding debit of approximately $1.00."
- Published via FIX and SBE market data; **historical funding "available upon request"** — but the last ~48h is free on the public web page (§1.8).

### 1.8 Funding actually paid — measured, not asserted

I scraped CDE's own published hourly funding table [verified] https://www.coinbase.com/derivatives/funding-rates-data — **1,293 rows across 30 symbols, 44 hourly prints per symbol, 2026-08-26 21:00 → 2026-08-28 16:00 CT**:

| Symbol | Mean %/hr | **Annualized (×8760)** | Min | Max | Share of hours negative |
|---|---|---|---|---|---|
| **BIPZ30** (nano BTC Perp) | +0.001241% | **+10.87%** | +0.0003% | +0.0020% | **0 / 44** |
| **ETPZ30** (nano ETH Perp) | +0.001786% | **+15.65%** | +0.0002% | +0.0028% | **0 / 44** |
| SLPZ30 (nano SOL Perp) | −0.000366% | **−3.21%** | −0.0012% | +0.0010% | 70% |
| XPPZ30 (nano XRP Perp) | +0.000674% | +5.91% | −0.0012% | +0.0019% | 28% |

**Caveat, stated loudly: 44 hours is 1.8 days.** This is a snapshot, not a regime estimate, taken during a window when BTC drifted from ~$77.9k to ~$77.4k. It is *not* evidence of a durable 10.87% rate. It is evidence that (a) the mechanism works and publishes, (b) the sign was consistently positive for BTC and ETH over the window, and (c) the venue is not paying a *worse* rate than the offshore average `strat-crypto.md` cites (~11% in 2024, ~5% in 2025). **Anyone acting on this must log the funding table daily for 60–90 days before sizing.** That logging costs nothing and is the single highest-value pre-commitment build in this whole report.

### 1.9 API access [verified]

- **Direct CDE connectivity:** FIX 4.4 (order entry + market data + drop copy), SBE (order entry, **market makers only**), UDP multicast (market data only). **No REST or WebSocket for retail.** https://help.coinbase.com/derivatives/perpetual-style-futures/market-access
- **Retail path is the FCM's API.** Coinbase's Advanced Trade REST API exposes CFM (Coinbase Financial Markets) futures endpoints — e.g. `GET /api/v3/brokerage/cfm/balance_summary` — whose schema includes `intraday_margin_window_measure`, `overnight_margin_window_measure`, liquidation threshold/buffer, and **funding PnL for "US Perpetuals Futures"** [verified] https://docs.cdp.coinbase.com/api-reference/advanced-trade-api/rest-api/futures/get-futures-balance-summary. Access is a self-serve CDP API key.
- **IBKR:** futures permission is self-serve — "Trading permission requests are typically approved within 24 hours." [verified] https://www.interactivebrokers.com/en/trading/coinbase-derivatives.php
- **Not approval-gated in any meaningful sense** for a retail account at Coinbase or IBKR. The gate is FCM onboarding, not exchange membership.

### 1.10 Margin — the one number I could not get

Nodal Clear's margin rate file 404'd at every URL I tried; CDE does not publish BIP margin on any public page I reached; IBKR's futures margin table for CDE nanos was not on the commissions page. **BIP initial/maintenance margin is [unconfirmed].** The only figures found are marketing: Tradovate "day trade margins as low as $25" [promo] and Kraken's "as little as $25 in intraday margin" for Bitnomial perps [promo]. For a delta-neutral carry book the binding constraint is not initial margin anyway — it is the variation-margin buffer (§5.3).

---

## 2. Is the carry trade actually executable?

### 2.1 Cost of the non-perp leg

| Long leg | Fee | Round trip | Notes |
|---|---|---|---|
| **Spot BTC at IBKR** (Paxos / Zero Hash) | **0.18%** of trade value ≤$100k/mo; 0.15% to $1M; 0.12% above. **$1.75 min/order, capped at 1% of trade value.** [verified] https://www.interactivebrokers.com/en/pricing/commissions-cryptocurrencies.php | **36 bps** | Custody is at Paxos/Zero Hash **outside IB**, and **"Digital assets held with Paxos or Zero Hash are not protected by SIPC."** Plus a USD 0.15/month Paxos account fee. |
| **Spot BTC on Coinbase Advanced** | **[unconfirmed — login-gated]**. Coinbase's own help article says: *"To see the complete fee structure, sign in to your Coinbase.com account."* [verified that it is gated] https://help.coinbase.com/en/coinbase/trading-and-funding/advanced-trade/advanced-trade-fees. `markets.md`'s reported 0.60%/1.20% sub-$1k figures remain unconfirmed. | 80–240 bps if those figures are right | Same conclusion as `markets.md`: **do not use Coinbase spot as the long leg.** |
| **Long CDE nano BTC dated future (BIT)** | $0.10 exchange + $0.20 IBKR = $0.30/side | ~8 bps | Same exchange, same clearinghouse, same index → best chance of margin offset. But you then pay the CDE dated basis instead of holding spot. |
| **Long CME MBT** | $0.85 IBKR + CME fee, on $7,784 notional = **~1.1 bps/side** commission | ~3 bps | Different index (CME CF BRR vs MarketVector Coinbase BRR), different clearinghouse → **no margin offset with Nodal**. Quarterly roll. |

**IBKR is the cheapest compliant venue for the spot leg by a wide margin** — 36 bps round trip versus a Coinbase Advanced schedule nobody outside the login wall can see.

### 2.2 Net APY, three structures

**(A) Short BIP + long spot BTC at IBKR.** Perp round turn ~10 bps + spot round turn 36 bps ≈ **46 bps of one-time entry+exit friction**. Against the measured +10.87% annualized funding, year-1 net ≈ **10.4% gross of financing**. This is at or above `strat-crypto.md`'s 4–10% estimate for offshore venues — but see §2.3 before believing it.

**(B) Short BIP perp + long BIT dated future (same exchange).** No spot leg, no custody risk, no Paxos, both legs §1256, capital requirement is margin only. Return = perp funding − CDE dated basis. I do **not** have CDE's dated-futures term structure (the exchange-products page didn't surface a curve), so this spread is **[unconfirmed]** — but it is the structurally cleanest trade available to a US person and should be the first thing measured.

**(C) Short BIP perp + long CME MBT.** Return = perp funding − CME dated basis. CME's own settles, 29 Aug 2026 [verified] https://www.cmegroup.com/markets/cryptocurrencies/bitcoin/micro-bitcoin.quotes.html:

| Month | Prior settle |
|---|---|
| Sep 2026 (MBTU6) | 77,835 |
| Dec 2026 | 78,925 |
| Mar 2027 | 79,985 |
| Sep 2027 | 82,125 |
| Dec 2027 | 83,270 |

Annualized calendar-implied rates (spot-independent, so robust): Sep→Dec26 **5.74%**, Sep→Mar27 **5.62%**, Sep→Sep27 **5.51%**, Sep→Dec27 **5.55%**. **The CME curve prices crypto financing at a very flat ~5.5–5.7% annualized.**

**This is the single most important number in the report.** CME's term structure is the market's clean, deeply-arbitraged read on the crypto carry rate. CDE's measured perp funding over the same window was **10.87%**. That **~5.2–5.4 pp gap is the entire candidate edge** — and it is exactly the kind of gap you would expect on a venue that a much smaller set of arbitrageurs can reach. It is also exactly the kind of gap that could be a 2-day artifact. Measuring whether it persists is a free experiment; assuming it persists is how accounts die.

### 2.3 The framing that kills naive numbers

**Carry is a spread over the risk-free rate, not an absolute return.** In cash-and-carry you tie up full notional in BTC; the alternative use of that cash is T-bills. Excess return = basis − r_f. I could not retrieve the current T-bill curve (treasury.gov timed out) **[unconfirmed]**, but the point is structural: if bills yield anywhere near 3.5–4%, the CME cash-and-carry's **5.5% gross becomes ~1.5–2% excess** for taking basis-convergence, exchange, and custody risk — which is not a strategy, it is a rounding error with tail risk.

The perp-vs-dated spread structures (B) and (C) are immune to this critique because they are financed positions on both sides — the risk-free rate cancels. **That is why (B)/(C) are the interesting trades and (A)/(D) mostly are not.**

### 2.4 CME cash-and-carry, sized

- **MBT** = 0.10 BTC, CME CF BRR settled, financially settled, tick $5/BTC = $0.50/contract, monthly ×6 + quarterly ×4, terminates 4:00pm London last Friday of the month, Globex 24/7 with maintenance windows. [verified] https://www.cmegroup.com/markets/cryptocurrencies/bitcoin/micro-bitcoin.contractSpecs.html
- **Margin:** maintenance short **$1,713–1,832** per contract across the curve, vol scan 50%. On $7,784 notional that is **~22–24%**. [verified] https://www.cmegroup.com/markets/cryptocurrencies/bitcoin/micro-bitcoin.margins.html
- **Minimum viable size:** one MBT unit needs $7,784 of spot BTC plus ~$1,750 futures margin ≈ **$9,500**. A $10k account does exactly one unit. Nano BTC (0.01 BTC, $774) is **10× more granular** and is the correct retail instrument.
- **Roll cost:** quarterly, ~1.1 bps/side IBKR commission on MBT plus CME fees plus a tick of spread — call it **~5–8 bps per roll, ~20–30 bps/yr**, against a ~5.5% gross basis. Roll cost is not the problem; the risk-free hurdle is.
- Liquidity warning: MBTU6 volume 3,439 that morning, and **every back month showed zero volume** (Oct 2026 traded 1 contract; Nov 2026 onward zero) [verified from the same quotes page]. The CME curve beyond the front two months is settlement-price-only. Do not plan a long-dated CME leg at retail size.

---

## 3. Verifying the geoblock claims

### 3.1 Hyperliquid — verified verbatim, and the 403 in `markets.md` is resolved

Fetched by driving a real browser to https://app.hyperliquid.xyz/terms on 2026-08-29. The site itself rendered a live banner:

> **"You are accessing the website from a restricted jurisdiction - see the Terms of Use. If you think this is an error, try refreshing the page or opening a support ticket."** [verified]

Terms of Use, last updated **June 15, 2026**, §1.6 [verified, verbatim]:

> "The Interface is not available to 'Restricted Persons.' For the purposes of these Terms, Restricted Persons include: (a) persons or entities who reside in, are located in, are incorporated in, or have a registered office in **the United States of America** or Ontario, Canada; … Restricted Persons are **strictly prohibited** from accessing or using the Interface described herein."

§1.9 [verified, verbatim]:

> "you expressly represent and warrant that your activities are lawful under such applicable laws, and that **you are not using any technology or method to disguise your location or otherwise evade any access restriction**."

§1.8: "You must not circumvent, attempt to circumvent or assist any other person to circumvent any such measures that we implement."

**The honest nuance nobody in the sibling reports flagged:** these Terms bind the *Interface*, not the chain. §1.1: "The Company does not own, control, or operate Hyperliquid… **The Interface is not the exclusive means of accessing Hyperliquid.**" So a US person hitting the Hyperliquid API directly is not breaching *this contract* — they never accepted it. The exposure is statutory, not contractual: trading leveraged retail commodity transactions on an unregistered facility implicates the CEA. The relevant precedent is CFTC's simultaneous 2023 orders against **Opyn ($250,000), ZeroEx ($200,000) and Deridex ($100,000)** for failing to register as a DCM/SEF and FCM and offering illegal leveraged and margined retail commodity transactions, with the enforcement director quoted: *"DeFi operators got the idea that unlawful transactions become lawful when facilitated by smart contracts. They do not."* [verified] https://www.cftc.gov/PressRoom/PressReleases/8774-23 — **note carefully: those were actions against operators, not against users.** I found no primary source in this session showing CFTC enforcement against an individual US retail trader for using a geoblocked perp venue.

### 3.2 Coinbase's own products confirm the split [verified]

Coinbase's consolidated derivatives page carries this banner:

> **"Coinbase Derivatives offers perpetual-style futures. Coinbase International Exchange and Deribit are only available to non-US customers in select jurisdictions."** https://www.coinbase.com/market-data/derivatives

And the Coinbase Advanced perpetuals marketing page — 50× leverage, "0.0% maker and 0.0% taker fees when you trade perpetual futures," "up to 12% rewards on your USDC collateral" — is footnoted throughout: *"Zero trading fees are only available for **non-US** users in select jurisdictions"*; *"Available via Coinbase Advanced for retail traders in eligible **non-US** jurisdictions"*; stock and commodity perps "are offered by **Coinbase Bermuda Ltd.**" [verified] https://www.coinbase.com/advanced-trade/crypto-futures. **The zero-fee, high-leverage, USDC-yield perp product is explicitly not for US persons.** US persons get CDE nano perps at $0.10/side through an FCM.

### 3.3 Claims I could NOT verify in this session

- **OKX $505M DOJ settlement (Feb 2025)** — justice.gov returns 403 to this session's fetcher on every URL tried; Reuters and web.archive.org are both blocked for this tool. **[unconfirmed here]** — not disputed, just not independently verified.
- **"14,000+ accounts closed for geolocation fraud in 2025, with forced liquidation of open positions on detection."** No primary source reached. **[unconfirmed]** — and note `strat-crypto.md` itself tagged it "secondary but consistent across sources."
- **Binance and Bybit restricted-persons clauses** — not fetched (budget). **[unconfirmed]**
- **BitMEX ceasing 2026-09-23 / AscendEX 2026-07-01** — https://www.bitmex.com/app/notices showed **no such notice**; also 2026-09-23 is in the future relative to today, so at best that is an announced future date, not an accomplished shutdown. **[unconfirmed]**

**Bottom line on consequence:** the strongest *verified* statement available is that Hyperliquid's current terms flatly prohibit US persons, prohibit location-disguising technology, and the site actively detects and blocks. Whether the downstream consequence is closure, freeze, or seizure is not established from primary sources here. It does not matter much: a delta-neutral carry book whose short leg can be administratively closed at the venue's discretion is not a book, it is a bet on not being noticed.

---

## 4. Tax treatment — what is settled, what is not

**Not tax advice. Reporting what the sources say.**

### 4.1 The §1256 chain of reasoning is clean on the face of the statute

26 U.S.C. §1256 [verified, verbatim] https://www.law.cornell.edu/uscode/text/26/1256:

- §1256(g)(1): *"The term 'regulated futures contract' means a contract—(A) with respect to which the amount required to be deposited and the amount which may be withdrawn depends on a system of marking to market, and (B) which is traded on or subject to the rules of a qualified board or exchange."*
- §1256(g)(7): *"The term 'qualified board or exchange' means—(A) a national securities exchange which is registered with the Securities and Exchange Commission, **(B) a domestic board of trade designated as a contract market by the Commodity Futures Trading Commission**, or (C) any other exchange, board of trade, or other market which the Secretary determines has rules adequate to carry out the purposes of this section."*
- §1256(a): mark to market on the last business day of the year; **60% long-term / 40% short-term** regardless of holding period.
- **The statute contains no expiration requirement.** A never-expiring contract does not fall out of the definition on that basis.

Applied to CDE nano perps:
1. CDE **is** "a domestic board of trade designated as a contract market by the CFTC" — from the CFTC's own registry [verified, §1.1].
2. CDE perps **are** margined on a system of marking to market — initial margin at trade, variation margin computed from settlement prices twice daily through Nodal Clear [verified, §1.7].
3. → On the statutory text, they look like §1256 contracts: **60/40, year-end MTM, one number on Form 6781, no wash-sale matching, no per-lot reconciliation.**

For a bot doing thousands of trades a year this is worth more than most edges. `markets.md` makes the same point about CME micros; it extends to CDE nanos and, if the analysis holds, to the perps.

### 4.2 What is genuinely unclear

- **No IRS ruling, notice, or regulation specifically addressing perpetual-style futures on a US DCM** surfaced in this session. The conclusion in §4.1 is a reading of the statute, not a cited authority. I attempted a practitioner analysis (thetaxadviser.com) — 404. **[unconfirmed]**
- **The funding payment is the open question.** Coinbase's own documentation says funding is booked as *"separate cash adjustment entries in the clearing files and **do not affect variation margin**"* [verified]. Whether a cash flow that the clearinghouse deliberately segregates from variation margin is part of the §1256 gain/loss on the contract, or is ordinary income/expense outside §1256, is **not settled by anything I could find**. For a carry strategy this is not a footnote — the funding stream *is* the entire return. A 60/40 versus ordinary characterization on the whole P&L is a material difference.
- **Mixed straddle exposure.** Short §1256 perp + long spot BTC (property, not a §1256 contract) is a straddle. §1092 straddle rules and the §1256(d) mixed-straddle election plausibly apply, and can defer or recharacterize losses. I did not analyze this and it needs a practitioner. Structures (B) and (C) — perp vs. dated future, both §1256 — sidestep the mismatch, which is another argument for them.

### 4.3 Spot leg [verified]

https://www.irs.gov/businesses/small-businesses-self-employed/digital-assets (page last reviewed **August 28, 2026**):
- *"For U.S. tax purposes, digital assets are considered **property, not currency**."*
- *"This reporting is required to be made on **Form 1099-DA beginning with transactions on or after Jan. 1, 2025**"* — final regs 09-Jul-2024, gross proceeds from 2025, **basis reporting from 2026**.
- The page contains **no** guidance on wash sales for digital assets and **no** guidance on digital-asset derivatives. The absence of a wash-sale rule for crypto follows from §1091 applying to "stock or securities," not from an affirmative IRS statement.

---

## 5. Other compliant venues

### 5.1 Bitnomial + Kraken Derivatives US — the second route, and it is real

- **Bitnomial Exchange, LLC** is a CFTC-designated contract market, **designated 04/17/2020** [verified] https://www.cftc.gov/IndustryOversight/IndustryFilings/TradingOrganizations
- Bitnomial's own site: *"Leveraged spot, perpetuals, futures, options, and prediction markets, all on one CFTC-regulated exchange with crypto margin and settlement."* … *"Futures accounts are offered by **Bitnomial Clearing, LLC, a CFTC-registered FCM and NFA member**."* It operates **DCM + DCO + FCM** subsidiaries, and is *"open to residents of the United States and around the world."* [verified] https://bitnomial.com/
- **Kraken Derivatives US** [verified] https://pro.kraken.com/perpetual-futures: *"US residents can trade Perpetual Futures directly on Kraken Pro. You'll need to complete identity verification and pass the Futures eligibility check."* The offering entity is *"**NinjaTrader Clearing LLC (dba Kraken Derivatives US)**, a CFTC-registered Futures Commission Merchant and NFA Member (**NFA ID: 0309379**)"*, trading on Bitnomial's DCM/DCO. **16 crypto perpetual markets** (BTC, ETH, SOL, XRP, DOGE, AAVE, BCH, XLM, HBAR, LTC, DOT and others). *"All 16 contracts support intraday margin,"* some requiring *"as little as $25 in intraday margin."* *"Certain states may have restrictions — eligibility is confirmed at sign-up."*
- **Fees: [unconfirmed].** Every Bitnomial and Kraken fee-schedule URL I tried 404'd. Kraken says only "maker orders pay less, and fees drop further as your 30-day volume grows."
- **The API gap is the practitioner-flagged problem.** [anon] r/algotrading, 2026-07-31, "US Crypto Perpetual Futures API" (9 comments): *"Does anybody know of an exchange or platform which offers crypto perpetual futures WITH API in the US? Kraken disappointingly only has API keys for spot+margin. I know Kraken's perps are offered via B[itnomial]…"* — a builder in July 2026 could not reach Kraken's US perps programmatically through Kraken's own keys. This is exactly the constraint that matters for a zero-babysitting bot, and it is a point in **Coinbase Derivatives'** favour, since Coinbase's Advanced Trade REST API and IBKR's API both reach CDE contracts today. Related [anon] threads: r/algotrading 2025-08-23 "Coinbase Futures API for trading?" and 2025-01-30 "Help Automating Bitcoin Futures Trading" (22 comments) — the latter is a retail trader who *"identified some cash-and-carry arbitrage opportunities in the Bitcoin futures market"* and was looking for automation, i.e. the trade is being attempted at retail scale.
- **Signal from silence:** targeted Reddit searches surfaced almost no practitioner discussion of CDE nano perps specifically. Either retail algo adoption is thin, or the archive coverage is poor. Do not read this as endorsement; read it as "you will be an early user with few people to ask."

### 5.2 Other DCMs

- **Rothera Exchange and Clearing LLC** — DCM designated 06/24/2019; formerly LedgerX, then MIAX Derivatives Exchange (MIAXdx); renamed after a **Jan 20, 2026** corporate transaction. [verified, CFTC registry]
- **CME** — crypto futures and options; MBT verified in §2.4. CME did not appear on page 1 of the CFTC DCM listing I fetched (the list is paginated); that is a fetch limitation, not a status change.
- **Cboe Digital** — https://www.cboe.com/digital/ returned 404 in this session. **Status [unconfirmed].**
- **Deribit** — now Coinbase-owned and by far the largest crypto options venue ($38.31B OI on 8/29/26 [verified]). Per Coinbase's own banner it is *"only available to non-US customers in select jurisdictions."* **The Deribit acquisition does not open US-person access to crypto options.** CME crypto options remain the compliant route; I did not price them.

### 5.3 Operational reality of running the book

- **24/7 except Fri 5–6pm ET.** [verified] Genuinely no weekends off.
- **Funding cash-adjusts twice daily**, and "FCMs may choose to process the cash adjustments once or twice per day" [verified] — so your realized funding accrual schedule depends on your FCM, not just the exchange. Reconcile against the exchange's published hourly table.
- **The real capital tax is variation margin, not initial margin.** *"Funding debits and variation losses reduce account equity and net liquidity"* [verified]. If the long leg sits in a different account (IBKR crypto is custodied at Paxos/Zero Hash **outside IB**; a spot ETF sits in the securities account), there is **no cross-margin offset** with the Nodal-cleared short. A 10% adverse BTC move on $50k of short perp notional is a **$5,000** variation-margin draw, twice a day, against a hedge that cannot be pledged. Structures (B) and (C) — perp vs. dated future — are the only ones where offset is even plausible, and only (B) (same exchange, same clearinghouse) has a real chance of it.
- **Reportable at 25 contracts** (~$19,350 notional) [verified, Rule 1129(e)]. A $50k book is a reportable position.
- **Recurring cost floor:** hourly funding data is free on the public page; historical data "available upon request"; Tradovate advertises $0 market data on these contracts [promo]. Realistically **$0–20/mo** (a VPS) **plus** whatever professional market-data fee your broker charges once you are classified Professional for using "a fully automated order generating computer system" — **[unconfirmed], and worth pricing before you build.**

---

## VERDICT

**Does any crypto strategy survive a US-person legality filter?** Yes — exactly one, and it survives better than the sibling reports assumed.

### What belongs in a Top-20 ranking

**1. Perpetual-vs-dated basis capture on Coinbase Derivatives.** Short nano BTC Perp (BIP), long a dated BTC future — ideally CDE's own nano BTC (BIT) for same-clearinghouse offset, else CME MBT.
- **Venue:** Coinbase Derivatives (CFTC DCM, designated 2020), cleared at Nodal Clear, accessed through Coinbase Financial Markets or IBKR. Fully legal for a US person; no VPN, no ToS violation, no seizure risk.
- **Net expected return:** the measured gap between CDE perp funding (**+10.87% annualized over a 44-hour window**) and the CME-implied crypto financing rate (**~5.5–5.7% annualized, from the 29-Aug-2026 settlement curve**) is **~5.2–5.4 pp gross**. Round-trip friction ~9–10 bps on the perp leg, ~3 bps on an MBT leg. **Call it 3–5% net if the gap persists, and treat "if" as the whole question.** That lands in the same band as `strat-crypto.md`'s 4–10% offshore estimate — with none of the jurisdiction risk.
- **Recurring cost:** $0–20/mo, plus an unpriced professional market-data fee.
- **Babysitting:** genuine 24/7 exposure, twice-daily margin and funding cycles, variation-margin monitoring on an unoffset short leg. **Call it 2–4 h/week once stable, with hard tail events.** Higher than `strat-crypto.md`'s 1–3 h/wk, because the margin plumbing sits at an FCM you must reconcile against.
- **Capital:** works from ~$10k (nano = $774/contract, 10× more granular than MBT). $25k–50k is the sweet spot. Above ~$19k notional you become a reportable position.

**2. The zero-capital version, which is the one to actually build first.** Log CDE's public hourly funding table and the CME MBT settlement curve every day for 60–90 days and compute the realized perp-minus-dated spread, net of the fee schedule in §1.3–1.4. That is a real system, it costs nothing, it produces the one number that decides whether trade #1 exists, and it is a better artifact than any backtest. **For a builder optimizing learning-per-dollar this dominates everything else in this report.**

### What does NOT belong

- **Anything on Binance, Bybit, OKX or Hyperliquid.** Hyperliquid's terms, verified verbatim today, prohibit US persons and prohibit location-disguising technology, and the site actively blocks. There is no version of this that is a system rather than a bet on not being caught.
- **Coinbase's flagship perps product** — 50× leverage, 0% fees, 12% USDC collateral yield. Explicitly non-US. So is Deribit, so is Coinbase International Exchange.
- **nano ETH Perp for carry.** The $0.10 flat exchange fee on a $243 notional is 4.1 bps/side and the tick is 2.06 bps — roughly double BIP's friction, for the same mechanism.
- **nano SOL / nano XRP perps.** Both below the $50M-OI floor, and SOL's funding was *negative* 70% of sampled hours.
- **Straight CME cash-and-carry (long spot, short MBT).** ~5.5% gross is a spread over the risk-free rate; strip out T-bills and the excess is ~1.5–2% for real convergence and custody risk. Also, every CME back month showed zero volume that session.
- **Kraken Derivatives US / Bitnomial — not yet.** Legally clean and structurally interesting (DCM+DCO+FCM under one roof, 16 perps, $25 intraday margin), but the fee schedule is unpublished and a practitioner reported in July 2026 that the perps were not reachable via Kraken's own API keys. **Re-check in 6 months; do not plan around it now.**

### The honest caveats

The 10.87% funding figure rests on **44 hours** of data. The perp-vs-dated spread is the edge, and I have not measured it even once — I have measured perp funding on one venue and dated basis on another, over overlapping but not identical windows, on **different indices** (MarketVector Coinbase BRR vs CME CF BRR). BIP margin is unconfirmed. Bitnomial and Kraken US fees are unconfirmed. The tax characterization of the funding stream is genuinely unsettled and it is the entire return. Coinbase Advanced spot fees remain behind a login wall, as `markets.md` found.

**But the structural finding is solid and it changes the ranking:** the sibling reports' conclusion that the surviving crypto edge sits on venues a US person cannot legally touch is wrong. It sits on a CFTC-regulated DCM with $149M of open interest, a published $0.10/side fee, a published hourly funding series, a self-serve retail API, and — on a plain reading of §1256(g) — 60/40 tax treatment with no wash sales. **Do not delete the crypto slots. Reduce them to one, point it at Coinbase Derivatives nano BTC Perp, and make the first deliverable a measurement rather than a position.**

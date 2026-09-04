# Strategy Universe: Crypto-Native & Arbitrage-Family

Research spike, as of 2026-08. Evidence tags: **[verified]** = published/audited/on-chain/peer-reviewed · **[anon]** = plausible anonymous practitioner account · **[promo]** = author sells something, discount heavily.

**Not investment advice.** This is a mechanism-and-economics catalog, not a recommendation to deploy capital.

**Method limitations (read first):** the Arctic Shift Reddit archive returned HTTP 500 on every query this session (7 attempts, multiple subs), so first-person forum accounts are under-represented relative to the brief. Web search budget was exhausted mid-session; later sourcing is direct WebFetch of primary documents. Where I could not reach a first-person practitioner, I substituted *public, on-chain, or audited proxies* for practitioner P&L (Hyperliquid HLP, Ethena sUSDe), which are strictly better evidence than forum anecdotes anyway.

---

## 0. The fee tiers, first — they decide most of these questions

Every strategy below is a bet that gross edge > round-trip cost. Retail round-trip cost is the single most under-modelled variable, so here it is up front, all **[verified]** from exchange fee pages fetched 2026-08.

| Venue | Product | Entry-tier maker / taker | What the next tier costs |
|---|---|---|---|
| Binance | Spot | 0.100% / 0.100% (0.075% w/ BNB) | VIP1 = $1M 30d vol **and** 5 BNB → 0.090/0.100 ([schedule](https://www.binance.com/en/fee/schedule)) |
| Binance | USDⓈ-M perp | ~0.020% / 0.050% | VIP3 (spot) = $20M 30d **and** 100 BNB → 0.040/0.060 |
| Kraken | Spot | **0.40% / 0.80%** at $0+ | needs $10M/30d to reach 0.00%/0.10% ([schedule](https://www.kraken.com/features/fee-schedule)) |
| Kraken | Futures | 0.020% / 0.050% | $5M+ → 0.0175/0.045 |
| Hyperliquid | Perp | 0.015% / 0.045% | Tier 1 = >$5M 14d volume ([docs](https://hyperliquid.gitbook.io/hyperliquid-docs/trading/fees)) |
| Hyperliquid | Spot | 0.040% / 0.070% | spot volume counts 2× toward tier |
| Bybit | Spot / perp | 0.100%/0.100% · 0.020%/0.055% | — |
| OKX | Spot / perp | 0.080%/0.100% · 0.020%/0.050% | VIP1 ≥ $5M/mo or $100k balance |

Two structural facts kill most retail "be the market maker" plans:

1. **Retail makers pay, they don't get paid.** Negative (rebate) maker fees exist only at institutional tiers. Hyperliquid's maker *rebate* tiers require >0.5% / 1.5% / 3.0% of **total platform maker volume** over 14 days for −0.001%/−0.002%/−0.003% [verified, HL docs]. Binance's Spot Liquidity Provider program requires **$20,000,000 30-day volume just to apply**, and pays ≤1 bp [verified, [Binance announcement](https://www.binance.com/en/support/announcement/binance-updates-spot-liquidity-provider-program-2024-09-09-6311b67d26804bf48c5d62f5beb91202); [The Block](https://www.theblock.co/post/356887/binance-altcoin-spot-liquidity-program)].
2. **Round-trip taker cost at retail is 0.10–1.60%** depending on venue. On Kraken spot at the entry tier a round trip costs **1.20%** — arbitrage there is arithmetically impossible for a beginner account.

---

## 1. Triangular arbitrage — settled question, and the evidence is unusually clean

**Mechanism:** three legs within one venue (USD→BTC→LTC→USD); profit if the exchange-rate product exceeds 1 net of three fees.

The best single piece of evidence in this whole beat is Muck, Schmidl & Wolf, *"Wish or reality? On the exploitability of triangular arbitrage in cryptocurrency markets,"* **Finance Research Letters 73 (2025) 106508** [verified] ([ScienceDirect](https://www.sciencedirect.com/science/article/pii/S154461232401537X)). Binance websocket order-book data, BTC/LTC/USD, 2024-06-03 → 2024-06-09:

- **4,879** triangular opportunities in one week. **88.89%** returned between 0% and 0.025% gross. **57.9%** lasted under 0.5 seconds.
- Profitability by Binance VIP tier is a straight line into the ground:

| Tier | Round-trip cost | Profitable opportunities | % of 4,879 |
|---|---|---|---|
| VIP 9 | 0.0540% | 150 | 3.07% |
| VIP 5 | 0.1080% | 53 | 1.09% |
| VIP 3 | 0.1350% | 38 | 0.78% |
| **Regular (retail)** | **0.2250%** | **18** | **0.37%** |

- **96.93% of opportunities are unprofitable even for a VIP 9 trader.**
- Retail's total realizable net profit for the entire week, constrained by book depth: **$12.43–$17.73**. A VIP 9 trader's best case: $170.76.
- Execution must complete in **≤146 ms** or slippage risk exceeds the edge.
- The authors' own latency work: 80 ms from a European server, **4 ms from Tokyo** (Binance's assumed colo region).

**Verdict:** dead for retail, and provably so. You would spend more on the Tokyo VPS than the strategy earns. The paper's conclusion — that opportunity *count* is not evidence of inefficiency — is exactly the trap arbitrage-scanner marketing sets.

**Babysitting:** N/A. **Build value:** high as a market-microstructure exercise (build it, log the 4,879-per-week signal, watch fees eat it, delete). Zero as a P&L strategy.

---

## 2. Cross-exchange (spatial) arbitrage

**Mechanism:** buy on venue A, sell on venue B. Practically it is *not* transfer-based — transfers are far too slow — it is **pre-funded inventory on both sides**, trading the spread and rebalancing occasionally.

**Numbers:**
- Break-even spread ≈ **0.30–0.50%** round trip once both taker legs, withdrawal fees ($5–25 per asset) and slippage are counted [promo, [HyroTrader](https://www.hyrotrader.com/blog/crypto-arbitrage-trading/) — sells funded accounts].
- BitMEX's own worked example: a 0.60% gross spread nets **0.27%**; they put minimum viable spatial-arb capital at **$10,000–20,000** to amortize fixed withdrawal costs [promo, [BitMEX blog](https://www.bitmex.com/blog/arbitrage-in-crypto)]. *Note the irony: BitMEX published this guide and then announced its own wind-down in July 2026.*
- Dislocations of **0.2–1.5%** do still appear across majors during volatility but last **seconds**; measured fill rate is **82% under 50 ms latency vs 31% above 50 ms** [promo, [Electronic Trading Hub](https://electronictradinghub.com/cross-exchange-arbitrage-and-the-crypto-oms-gap-why-manual-execution-caps-your-monthly-roi-at-0-5/) — sells HFT consulting].
- Spreads on majors between top venues are now "nearly identical … at any given second" because Jump, Wintermute, DRW/Cumberland arbitrage them continuously [promo/secondary].

**The real cost nobody prices:** pre-funding N venues means capital-at-risk = N × exchange counterparty risk, permanently, for a strategy whose gross edge is a few bps. See §9 — three exchanges wound down in July 2026 alone.

**Verdict:** majors are HFT-owned. The residual retail edge lives in *thin, ugly, slow* corners: newly listed alts, low-tier venues, regional/fiat-rail dislocations — which is precisely where insolvency and withdrawal-freeze risk is highest. That's not an accident; it's the compensation.

**Babysitting:** high — inventory rebalancing, stuck withdrawals, listing/delisting events, per-venue KYC/API drift. Call it 3–6 h/week once live.

---

## 3. Funding-rate / cash-and-carry basis harvesting

**Mechanism:** long spot (or long perp on the cheap venue), short perp on the venue paying funding; collect the funding stream delta-neutral. Two variants: single-venue spot-perp carry, and cross-venue funding-spread capture.

**This is the only strategy in the beat with a defensible retail edge — and it has decayed hard.** The cleanest public proxy is Ethena, which runs this trade at multi-billion scale and publishes yields [verified-ish; protocol-reported]:

| Period | sUSDe APY |
|---|---|
| 2024 launch | ~27%, spiking >60% |
| 2024 stabilized | ~19% |
| 2025 | 4–15% range |
| **March 2026** | **~3.72%** |

USDe supply tracked the same decay: **$14B+ peak mid-2025 → $5.92B (2026-03-16)** [[Q1 2026 report](https://stablecoininsider.org/ethena-usde-q1-2026-report/)]. Aggregate BTC/ETH funding averaged **~11% annualized in 2024, ~5% in 2025**.

Retail-scale worked examples:
- **~$333,000 of capital to generate $100/day** at a 0.01%-per-8h funding rate [promo, HyroTrader].
- $10k per side, Hyperliquid −0.08% vs Binance +0.02%: net $6 per 8h = $540/mo = ~32% APR gross, **18–25% net after fees/slippage** — but that example is picked from a wide-spread moment, not an average [promo, [Buildix](https://www.buildix.trade/blog/crypto-funding-rate-arbitrage-delta-neutral-hyperliquid-binance), sells a screener].
- Sell-side marketing claims of 25–50% "passive income" [promo] are describing the 2024 regime and should be read as ~4–8% in the 2026 regime, before an adverse event.

**The failure mode is not gradual — it is a cliff.** October 10, 2025:
- **$19.3B liquidated in ~24h, ~1.6M accounts**; $16.7B of it longs (6.7:1) [verified, widely reported].
- **USDe printed $0.60–0.65 on Binance's internal book while trading ~$1.00 everywhere else**, because Binance priced margin collateral off its own order book. Binance later paid **$283M in reimbursements for the collateral depeg — and explicitly not for API failures or ADL pricing** [[Forbes](https://www.forbes.com/sites/boazsobrado/2025/10/21/locked-out-and-liquidated-traders-blame-binance-for-19-billion-crash/)].
- **Auto-deleveraging (ADL) is the delta-neutral killer.** ADL closes your *winning* leg. "Cross-venue long/short farmers turned naked as ADL picked off one leg first"; "delta-neutral farmers got nuked" [[Unchained / The Chopping Block](https://unchainedcrypto.com/the-chopping-block-inside-the-19b-perp-crash-adl-explained-binances-usde-staked-token-depeg-and-the-hyperliquid-whale-debate/)]. Wintermute's CEO: ADL'd at $5 on a token trading near $1 — *a professional market maker with colocation and a legal team.*
- BTC **top-of-book depth fell >90%**; spreads went from single-digit bps to **double-digit percent** [[FTI Consulting](https://www.fticonsulting.com/insights/articles/crypto-crash-october-2025-leverage-met-liquidity)].

**The practitioner story to internalize [anon, well-documented]:** *812.eth*, an algorithmic trader whose system had run **1,137 consecutive days**, went from a **$3.9–4.1M balance to $0.22**. Logs show **200+ rejected ReduceOnly orders over 106 minutes** — error codes −2010, −4118, −2022, HTTP 503 — a near-100% rejection rate on risk-*reducing* orders between 05:12 and 07:02. Binance claimed a 10% rejection rate; market makers disputed it. Losses included ~$444k on DOGE and ~$148k on XRP [Forbes, above].

The lesson is not "he was reckless." It is that **your hedge is only as good as the exchange's willingness to let you close a position during the exact 90 minutes you need to.** No amount of local code quality fixes this.

**Verdict:** viable at small size, honestly ~4–10% net APY in the 2026 regime, with a genuine multi-sigma tail. Best-in-class risk controls are: low leverage (2–3× max), oversized margin on the short leg, avoid instruments under $50M OI, and — most importantly — **do not use exotic collateral** (USDe, LSTs, staked tokens) on a venue that marks it off its own book.

**Babysitting:** 1–3 h/week steady state, but requires an automated de-risk path and alerting; the whole strategy's risk is concentrated in ~4 hours a year.

---

## 4. Market making on CEX

**Mechanism:** quote both sides, earn spread + (maybe) rebate, pay inventory risk and adverse selection.

**The public benchmark is Hyperliquid's HLP vault** — an on-chain, continuously auditable market-making + backstop-liquidation book [verified]:
- Lifetime PnL **$136.9M** since May 2023.
- **~41% of lifetime profit came from two events**: +$41.5M over the Oct 10 2025 weekend (~10% in a weekend) and +$15M on Jan 31 2026 (5.8%).
- Losses: JELLYJELLY (Mar 2025) unrealized −$12–13.5M at peak; POPCAT (Nov 2025) $4.9M bad debt.
- **TVL: $603.9M peak (Sep 2025) → $268.6M (Jun 2026), −55%** [[CoinGecko analysis](https://www.coingecko.com/learn/hyperliquid-hlp-vault-analysis)].

Read that shape carefully: a *protocol-privileged* market maker with zero fees, first look at liquidations, and the whole book's flow earns lumpy returns concentrated in tail events, and its depositors have been leaving. A retail bot has none of those advantages and pays **0.015–0.10% per fill to make**.

The retail arithmetic: you must earn spread > 2× maker fee + adverse selection + inventory drift. On BTC/USDT the spread is ~1 bp and the maker fee is 1.5–10 bps. **You cannot make markets in liquid majors at retail fee tiers — it is negative before adverse selection.** The only accessible venues are wide-spread, thin, illiquid pairs, where the spread is wide precisely because inventory risk is enormous.

Hummingbot — the standard open-source MM stack — publishes the concepts but **quantifies no returns, no capital requirement, and no failure rates**, only "market making is not a risk-free, always profitable trading operation" [[hummingbot.org](https://hummingbot.org/blog/what-is-market-making/)]. The community-consensus summary is that makers "earned spreads for weeks and gave them back in one trending day" [secondary/uncorroborated].

**Verdict:** excellent build/learning project (order book handling, inventory skew, Avellaneda-Stoikov, latency), poor expected value. Expect to pay tuition.

**Babysitting:** very high — 5–10 h/week, plus the strategy is short-vol and needs a kill switch.

---

## 5. DEX / AMM liquidity provision

**Mechanism:** deposit into an AMM, earn fees, pay arbitrageurs (LVR / impermanent loss).

This is the most thoroughly falsified "passive income" story in crypto, and the academic record is unambiguous:

- **Loesch et al., *Impermanent Loss in Uniswap v3*** (arXiv [2111.09192](https://arxiv.org/abs/2111.09192)) [verified]: 17 major pools = 43% of TVL. **$199.3M in fees earned vs $260.1M in impermanent loss.** LPs would have been **$60.8M better off simply holding.**
- **Heimbach, Schertenleib & Wattenhofer, *Risks and Returns of Uniswap V3 LPs*** (arXiv [2205.08904](https://arxiv.org/abs/2205.08904)) [verified]: "providing liquidity has become a game reserved for sophisticated players with the introduction of Uniswap V3, where **retail traders do not stand a chance**"; significant returns require active management and increased risk; median stable-pool position width is **4 bps**, i.e. an HFT-grade rebalancing problem.
- **Fritsch & Canidio, *Measuring Arbitrage Losses and Profitability of AMM Liquidity*** (arXiv [2404.05803](https://arxiv.org/abs/2404.05803), Apr 2024) [verified]: **losses to arbitrageurs exceed fees earned across many of the largest Uniswap pools**; Uniswap **v2 outperformed v3 for passive LPs**; cutting Ethereum block time from 12s to 100ms would cut arb losses to LPs by 20–70% (i.e. most of your loss is a block-time artifact you cannot control).
- **~50% of Uniswap V3 positions run negative**, with some pools' IL exceeding fee income by 70–75% [Bancor/Topaze Blue study, secondary via [Nasdaq](https://www.nasdaq.com/articles/half-of-uniswap-liquidity-providers-are-losing-money)].
- **LVR magnitude**: ≈ σ²/8 per day. ETH-USDC at 5% daily vol ≈ **3.125 bps/day ≈ 11%/yr** bled to arbitrageurs before any fees. Milionis et al. show a 30 bp pool needs **10% of TVL traded daily** just to break even on LVR.
- The one profitable LP cohort — **JIT liquidity providers**, who supply for a single block and take zero IL — earned $1.27M. That is not LPing, that is MEV (§7).

**Verdict:** structurally negative-EV for passive retail. LPing is selling a free option to arbitrageurs; the fee is the premium and the premium is too low.

**Babysitting:** low if passive (and you lose), extremely high if active (and you're competing with §7).

---

## 6. Grid trading

**Mechanism:** ladder of buy/sell limit orders around a range; harvest oscillation. Economically it is **short gamma / short volatility with no premium collected** — you are selling a strangle ladder and getting paid only the grid spacing.

Evidence is thin and mostly vendor-owned, which is itself a finding. The best first-person account I could reach [anon, tinted [promo] — Pionex/KuCoin referral links, sells a Substack]: four bots at **$10,000 each**; three netted **~$300 combined**; one in the red since inception; later, **all four Martingale grid bots underwater and maxed out on position**; "I've had to stop at a loss several times to keep my bots active"; "bearish movement is not ideal for these bots" ([source](https://automatedincomelifestyle.substack.com/p/challenging-month-crypto-trading-bot-update-july-04-2024-6e790cb69f71)).

Vendor claims of "8–12% monthly in ranging markets" [promo, Pionex-adjacent] describe the strategy's good regime only. The honest framing appearing even in vendor content: "if you tell a bot to buy every 2% drop, it will dutifully buy you all the way to zero."

Cost floor: Pionex charges 0.05% maker and taker, so **every grid round trip costs 0.10%** — your grid spacing must exceed 0.10% plus slippage before any P&L exists. On Binance spot at 0.075% (BNB) that's 0.15% per round trip.

Regulatory note on the cheapest grid venue: **Pionex entered a multi-state US consent order in 2025** for unlicensed money transmission, was blacklisted by France's AMF, and drew warnings in the Philippines and Malaysia [secondary].

**Verdict:** not an edge; a payoff-shape transformation that converts many small wins into occasional large losses. Genuinely useful as a *first* real system (order management, state persistence, restart safety) if you accept it as tuition.

**Babysitting:** medium — 2–4 h/week, spiking to constant during trends.

---

## 7. DEX arbitrage / MEV at hobbyist scale

**Ethereum CEX-DEX** — the definitive dataset: *"Measuring CEX-DEX Extracted Value and Searcher Profitability"* (arXiv [2507.13023](https://arxiv.org/html/2507.13023v1)) [verified], Aug 2023 – Mar 2025:
- **$233.8M extracted** from 7,203,560 arbitrages on **$241.7B volume** — a ~10 bp gross business.
- **Top 3 searchers (Wintermute, SCP, Kayle) took ~73% of extracted value; ~90% by Q1 2025.**
- **Only 12 of 19 labeled searchers were still active by October 2024** — a >35% attrition rate among *professional* searchers in 14 months.
- Exclusive searchers hand **~90% of arbitrage revenue to their integrated builder**. Wintermute: $74.8B volume → $24.3M PnL (20.9% margin).
- One labeled searcher (Graves) ran **$229.3M of volume for −$179.7K PnL**. Professionals lose money here.
- Authors: "already high entry barriers such as capital requirements, low-latency infrastructure, inventory risk"; smaller searchers keep higher per-trade margins but their volume share keeps shrinking.

**Solana** [verified, Jito/Helius data]:
- **90,445,905 successful arbitrages** in a year for **$142.8M** total → **average profit per arbitrage: $1.58.**
- Bots pay **50–70% of expected profit as Jito tips** to land bundles.
- Peak revert rate **75.7%** of non-vote transactions (Apr 2024).
- Concentration: one sandwich program (Vpe) did 1.55M attacks at 88.9% success for $13.43M profit, paying $4.63M (34%) in tips — **~half of all Solana sandwich activity from one program.**

**Cross-chain comparison** [[Extropy Academy](https://academy.extropy.io/pages/articles/mev-crosschain-analysis-2025.html)]: Ethereum ~$180M/month MEV with a "viable professional arbitrage market … [that] often does not exceed 20" entities; Solana top-3 bots >60% share, top bot ~$300k/day; infra **$200–500/mo RPC on Ethereum, $1,800–3,800/mo RPC plus colocation on Solana**. Their explicit verdict on solo/hobbyist searchers on Ethereum and Solana: **"Effectively no."** On L2s (Optimism/Base) barriers are low but margins are "cents (offset by spam cost)" and two entities produce 80% of the spam.

**Verdict:** the clearest "do not attempt for profit" in the beat. As a build project it is superb (mempool, simulation, bundle construction, atomicity) and can be done at zero risk on testnets/forks. Recurring cost to be *competitive* is $2–4k/month — an immediate disqualifier under the "recurring costs matter" constraint.

**Babysitting:** would be a full-time job. Failure rate determines P&L more than strategy logic does.

---

## 8. Copy / social signal following

**Mechanism:** mirror a leaderboard trader's positions, pay a performance/spread fee.

Evidence is weaker than any other section, and the weakness is the finding:
- eToro copy-portfolio study, 28 hand-collected portfolios, Jan 2017 – Jan 2020 [verified, but methodologically compromised]: 21 positive / 7 negative Jensen's alphas, **but only 6 positive and 3 negative were statistically significant** — i.e. 19 of 28 estimates are indistinguishable from zero. Critically, the sample required **three years of continuous data**, which mechanically excludes every portfolio that blew up. **This is survivorship bias by construction and the headline "most outperform" should not be believed.**
- *Copy Trading*, **Management Science** (Apesteguia, Oechssler & Weidenholzer) [verified]: showing subjects others' success **significantly increases risk-taking**, and the effect is *larger* when direct copying is available.
- Crypto leaderboards are worse than eToro's: ranking is on realized return over short windows, which selects for maximum leverage and short-vol strategies that have not yet had their event. October 10, 2025 wiped 1.6M accounts in a day — exactly the population that populates leaderboards.

**Verdict:** negative expected value plus full counterparty and follower-fee drag, with no learning payoff (you build nothing). The only defensible version is *signal ingestion as a feature* — e.g. using leaderboard positioning as a crowding/contrarian input into your own model — which is a research idea, not a strategy.

**Babysitting:** low, which is the entire (bad) appeal.

---

## 9. Crypto-specific operational risk — this dominates strategy selection

**Exchange wind-downs and insolvency, 2025–2026** [verified via [FinanceFeeds](https://financefeeds.com/could-a-top-crypto-exchange-collapse/), [news.bitcoin.com](https://news.bitcoin.com/featured/over-60-crypto-firms-and-projects-fold-in-2026-as-bankruptcies-bear-market-and-hacks-rip-industry-apart/)]:

| Venue | Event | Detail |
|---|---|---|
| **BitMEX** | announced 2026-07-23, ceased **2026-09-23** | 12-year-old venue; *invented the perpetual swap* |
| **AscendEX** | ceased 2026-07-01 | failed MiCA licensing; reserves down to **$13.5M** |
| **BitMart** | phased shutdown from 2026-07-26 | balance-sheet deficit found April; **$2M on-chain reserves against $10M/mo outflows on $1.3B daily volume** |
| **Bit.com** | spot ended 2026-01-31 | withdrawal-only mode from 2026-02-01 |
| **Polynomial** | 2026-02-18 | **force-closed all positions**, shut down 2026-03-03 |
| **Bybit** | 2025-02 | **$1.4B hack** (Lazarus, per FBI) |

Market-implied odds of a top-5 CEX (Binance, Coinbase, Bybit, OKX, Kraken) insolvency by 2026-12-31: **~5%** on Polymarket. Binance's Aug 2026 proof-of-reserves: BTC 100.25%, USDT 103.62%, USDC 107.64% [verified].

**The pattern that matters for arbitrage specifically:** every strategy above that needs *multiple venues* multiplies exposure to this table, and the venues with the best residual edge (thin, low-tier, high-spread) are the ones on it. The second- and third-tier venues you'd want for cross-exchange arb in 2026 are exactly AscendEX, BitMart, Bit.com.

**API and access risk:**
- **Order rejection during stress is the norm, not the exception.** 812.eth's near-100% ReduceOnly rejection rate for 106 minutes is the canonical case. A hedged book that cannot close one leg is an unhedged book.
- **ADL socializes losses onto profitable hedgers.** Your winning leg gets closed at a price disconnected from the liquid market. There is no code you can write that prevents this.
- **Oracle/collateral design is a venue-selection decision.** Binance marking USDe off its own internal book at $0.60 while it traded $1.00 elsewhere is the whole 10/10 story in one sentence.

**Jurisdiction/geo (US-specific, directly relevant here):**
- OKX settled with DOJ for **$505M (Feb 2025)** and now runs seven separately licensed entities; **global OKX is closed to US persons**, who must use OKX US.
- Bybit/OKX/Bitget geofence US IPs. **Over 14,000 accounts were closed for geolocation fraud in 2025.** Detection (IP, device fingerprint, KYC docs, bank residency) triggers **account termination and liquidation of open positions** [secondary but consistent across sources].
- Practical consequence: a US-resident cross-venue delta-neutral book has a very short list of legal venues (Kraken, Coinbase, CME, US-licensed entities), and Kraken's entry-tier spot fees (0.40/0.80) plus Coinbase's retail tier make CEX spot arbitrage arithmetically dead there. Using a VPN to reach Binance/Bybit converts a trading strategy into a *ToS-violation strategy where the failure mode is forced liquidation of your hedge*.

---

## 10. Ranking for a solo builder optimizing learning + small P&L chance

| Strategy | Retail edge 2026 | Recurring cost | Capital at risk | Babysitting | Build/learning value |
|---|---|---|---|---|---|
| Funding/basis carry | **Real but thin (~4–10% net)** | ~$0–20/mo VPS | med (venue risk) | 1–3 h/wk | high |
| CEX market making (thin pairs) | negative→marginal | ~$0–50/mo | low if sized small | 5–10 h/wk | **highest** |
| Grid trading | none (payoff reshaping) | ~$0 | low | 2–4 h/wk | medium |
| Cross-exchange arb | majors dead; corners risky | ~$0–100/mo | **high (N venues)** | 3–6 h/wk | high |
| Triangular arb | **proven dead** | VPS + colo to try | low | n/a | high (as a null result) |
| AMM LPing | **structurally negative** | gas | med | low | low |
| DEX arb / MEV | **dead solo** | **$2–4k/mo** | high | full-time | very high |
| Copy trading | negative | fees | high | low | **none** |

The shape of the answer: **the strategies with the best learning-per-dollar are the ones with no edge** (triangular, MEV, market making), and **the one with residual edge (funding carry) is the one where the risk is entirely operational and entirely outside your code.** A build that instruments the dead strategies honestly — logging live opportunity counts, fills, and fee drag — is a genuinely valuable artifact, and it costs nothing but time.

---

## 11. Gaps / what I could not verify

1. **No first-person Reddit accounts** — Arctic Shift archive returned HTTP 500 across 7 attempts. A rerun should target r/algotrading, r/CryptoCurrency, r/quant, r/defi with "gave up", "shut it down", "blew up".
2. **No 2025–2026 study of Uniswap LP profitability** — the strong LP papers are 2021–2024. v4 hooks and dynamic fees may have changed the picture; unverified either way.
3. **No crypto-specific copy-trading performance data** — all quantitative evidence is eToro equities, pre-2020. Binance/Bybit copy-trading cohort returns are unpublished.
4. **Grid trading has no independent quantitative study at all** — everything is vendor-published or single-operator anecdote. Treat the entire category as unevidenced.
5. **Binance USDⓈ-M futures VIP0 taker** — the fee page fetch returned an ambiguous row; the 0.020%/0.050% figure is from a secondary aggregator and should be re-confirmed against binance.com before it is used in any break-even calculation.
6. **Ethena APY figures are protocol-reported**, not independently audited; the transparency dashboard is geo-blocked from this session.

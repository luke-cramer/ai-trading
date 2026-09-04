# Open-Source Trading Ecosystem Sweep (GitHub) — 2026

Method: GitHub API/`gh` CLI mining of stars/activity/issues across 15 major repos, plus web search and
direct doc/README fetches. Reddit archive API (arctic-shift) was returning HTTP 500 for the entire
session — no Reddit data could be pulled for this beat; gaps are filled with GitHub Issues/Discussions,
which turned out to be a richer failure-mode source than expected. WebSearch quota was also exhausted
mid-session (shared across the parallel fan-out), so later claims lean more heavily on gh API/WebFetch.

## Snapshot table (pulled live via `gh api repos/<owner>/<repo>`)

| Project | Stars | Forks | Open issues | Status | Last push |
|---|---|---|---|---|---|
| freqtrade/freqtrade | 53,782 | 11,167 | 25 open / 5,634 closed | active, daily commits | 2026-08-27 |
| nautechsystems/nautilus_trader | 28,038 | 3,621 | 113 | active, very high velocity | 2026-08-29 |
| mementum/backtrader | 23,012 | 5,254 | 63 | **dead** — no push since 2024-08-19 | 2024-08-19 |
| TauricResearch/TradingAgents | 101,608 | 19,520 | 390 | viral, stalled ~1 month as of late Aug 2026 | 2026-07-18 |
| QuantConnect/Lean | 21,390 | 5,203 | 258 | active, corporate-backed | 2026-08-28 |
| AI4Finance/FinGPT | 21,170 | 3,005 | 86 | research repo, sparse recent commits | 2026-08-02 |
| hummingbot/hummingbot | 19,689 | 4,875 | 151 | active | 2026-08-28 |
| AI4Finance/FinRL | 16,130 | 3,484 | 310 | research repo, high unresolved-issue ratio | 2026-07-13 |
| goldmansachs/gs-quant | 12,793 | 1,726 | 69 | active but thin external contribution (20 contributors) | 2026-08-26 |
| StockSharp/StockSharp | 10,658 | 2,261 | 2 (repo) / 1 (issue-search) | active, oddly low GitHub issue volume for its star count | 2026-08-28 |
| askmike/gekko | 10,186 | 3,789 | 0 | **archived** by author, 2019 | 2020-02-16 |
| jesse-ai/jesse | 8,391 | 1,212 | 16 | active, smaller community | 2026-08-27 |
| polakowo/vectorbt | 8,891 | 1,143 | 138 | maintenance-mode; new features pushed to paid PRO | 2026-08-02 |
| carlos8f/zenbot | 8,260 | 1,973 | 295 | **archived**, explicit "no longer maintained" banner | 2022-02-14 |
| Drakkar-Software/OctoBot | 6,483 | 1,269 | 165 | active | 2026-08-28 |

Source for all rows: live `gh api repos/<owner>/<repo>` calls, this session.

---

## 1. freqtrade — the ecosystem's center of gravity

53.8k stars, 5,634 closed issues vs. 25 open, PRs merging same-day (dependency bumps, Binance
leverage-tier updates) — by far the best-maintained project in the sweep. [verified, direct repo query]

**The disclaimer is real and blunt.** Straight from the repo README: *"This software is for
educational purposes only. Do not risk money which you are afraid to lose. USE THE SOFTWARE AT YOUR
OWN RISK. THE AUTHORS AND ALL AFFILIATES ASSUME NO RESPONSIBILITY FOR YOUR TRADING RESULTS."*
(github.com/freqtrade/freqtrade README, fetched via `gh api repos/freqtrade/freqtrade/readme`)
[verified]. The docs also flag a mechanical backtest/live gap: fees in backtest/dry-run use the
exchange's default tier, while live fees reflect your actual tier/rebates; and most trading callbacks
fire once per candle in backtest but ~every 5 seconds in live, which the docs say "can cause
backtesting mismatches" (freqtrade.io/en/stable/bot-basics/) [verified].

**Hyperopt overfitting is a first-party admitted problem, not FUD.** GitHub issue #2472 ("Hyperopt
and overfitting (discussion)") opens with the Fermi/von Neumann "four parameters to fit an elephant"
quote and lays out how hyperopt search finds parameter "peaks" that fit in-sample and lose money
out-of-sample; a raised concern was strategies converging on extreme settings like a −35% stoploss
paired with tiny profit targets that look great until a real losing streak hits
(github.com/freqtrade/freqtrade/issues/2472) [verified, primary source, low direct maintainer
rebuttal in the visible thread]. The project's own built-in statistical "Edge" position-sizing module
— literally named for computing your trading edge — was ultimately **removed from freqtrade entirely**
(PR #11867, "Remove Edge from Freqtrade") after years of confusing users (issue #1525 "Edge messages
enriched", #1490 wrong win-rate formula in the docs) [verified]. A feature built to quantify edge
didn't survive contact with reality.

**Best available "I actually ran this for years" account** comes from a blog, not Reddit (Reddit was
unreachable this session): a long-time user's post, ironically titled "Thanks Freqtrade!!! I'm
quitting my job right now!!!", is explicitly satirical bait-and-switch. The real content: ~3 years of
freqtrade use, roughly 100 different bot/strategy configurations tried, a best short-term run of "100%
in under a week" attributed mostly to luck, but **zero long-term profitable strategy** — the longest
sustained profitable stretch was 8 months before decaying. Explicit conclusion: trying to replace a
job income via freqtrade is "almost impossible"; the honest payoff was Python/trading literacy, not
money (botacademy.ddns.net, "Thanks Freqtrade!!! I'm quitting my job right now!!!") [anon, single
blogger, but detailed and non-promotional — no product being sold]. This lines up almost exactly with
the user's own stated goals (learning > profit).

**Exchange-side breakage is a recurring live-trading tax, not a one-off.** Issue #12610: Binance's
mandatory migration to its new Algo Order API broke stoploss orders in production with error `-4120`
(17 comments) [verified]. Related historical breakage: #6686 "Previously working Bots stop... could not
load markets," #9342 stoploss/trailing-stop errors on Binance, #10311 `ExchangeNotAvailable` on a VPS.
None of these are freqtrade bugs per se — they are the tax of running against exchange APIs that change
under you, and they recur across every bot in this sweep (see nautilus_trader §5, OctoBot §4).

## 2. hummingbot — market making, and the scam-brand problem

19.7k stars, actively maintained (151 open issues, daily commits). Real inventory-risk bugs exist
(#3196 "Price type 'inventory cost' is flawed and inventoryCost seems to be calculated incorrectly")
[verified], and hanging/stuck orders on individual exchange connectors are a recurring bug class
(#7996 BingX hanging orders, still open) [verified] — consistent with the general pattern that
exchange-connector edge cases, not the core market-making logic, are where live money gets stuck.

The more important finding: **Hummingbot's own brand is used as a lure for fund-custody scams that
have nothing to do with the software.** Hummingbot is self-hosted — keys never leave your machine,
and the project explicitly does not run managed accounts — yet social-media pitches offering to "run
Hummingbot on your funds" are a known scam pattern trading on the open-source name for credibility
[promo-adjacent claim from a review aggregator, directionally consistent with hummingbot's own
non-custodial architecture which is verifiable in the codebase]. This mirrors the OctoBot/"Octobits"
pattern below — it's an ecosystem-wide phenomenon, not one project's fault.

Market making itself is where the real losses live, and it's a professional discipline: spreads
earned over weeks can be given back in a single trending session because market makers carry
inventory risk by construction — a bot that is quoting both sides gets run over in a fast one-way
move. This is architectural, not a bug you can patch.

## 3. jesse — smaller, live-trading plumbing is the pain point

8.4k stars. Top-commented issues are almost entirely live/paper-trading infrastructure failures, not
strategy questions: #447 "semi-endless loop around add_candle call" (27 comments), #372/#371 websocket
disconnects in `LiveExchange`, #410 "wrong period starts for 45m candles in PAPERTRADE mode" [verified,
all from `gh api search/issues`]. The revealed pattern across this whole sweep: the hard, unglamorous
part of retail algo trading is keeping a websocket connection alive and candles correctly aligned
through exchange maintenance windows — not the strategy logic, which is comparatively easy to write.

## 4. OctoBot — same bug taxonomy, plus a brand-impersonation scam

165 open issues; top threads are config/connection breakage (#1699 "Nothing works, cannot connect to
any service," #1883 open, "Timestamp was 1000ms ahead of server's time" — a clock-drift bug that
silently fails order placement) [verified]. Issue #929 (Kraken starting-portfolio ignoring EUR config)
and #924 ("Issue with Profitability on Home screen") show the profitability-reporting layer itself has
had bugs — i.e., users have filed issues because the bot *told them the wrong P&L*, a failure mode
worth flagging explicitly since it undermines any self-reported "I'm profitable" claim from users who
haven't cross-checked against the exchange's own ledger.

Separately: **"Octobits"** (operating from `octobitstop.shop`) is a confirmed impersonation scam
riding OctoBot's name, described as having defrauded "thousands of people out of hundreds of thousands
if not millions of dollars" through a fake trading/deposit scheme that stops honoring withdrawals once
funds are in (malwaretips.com writeup on "Octobits Trading Bot Crypto Scam") [anon/journalistic source,
not independently audited, but the pattern — real permissionless OSS bot vs. brand-cloned custodial
scam — is now attested for at least two projects in this sweep (Hummingbot, OctoBot) and is a
structural risk of this ecosystem: popularity of the free tool creates a target for a paid-impersonator
scam].

## 5. QuantConnect/Lean & nautilus_trader — the "production-grade" tier

Lean (21.4k stars) is corporate-backed (QuantConnect Corp runs a hosted cloud/backtesting business on
top of the open engine) and is the most institutionally-styled OSS engine here; its retail usage is
mostly via the hosted platform rather than self-hosting the raw engine, which changes the cost profile
(cloud compute/data fees replace self-hosted infra costs).

nautilus_trader (28k stars, Rust-core rewrite of a production engine) is the highest-velocity project
in the sweep by recent push activity. Its own docs explicitly warn against production use of release
candidates for real capital, and stress that live trading "requires... understanding... the differences
between backtesting and live trading before deploying to production" (nautilustrader.io/docs, Live
Trading page) [verified]. Issue history shows the same two failure classes as everywhere else:
exchange-API breakage (#3287 "Binance Algo orders API breaking changes," 27 comments) and
reconciliation bugs between the bot's internal state and the broker's real state (#1190 "IB
positions/orders not syncing... when orders are placed externally") [verified] — this last one is a
sharp warning for anyone planning to hand-adjust positions alongside a running bot: state desync
between "what the bot thinks it holds" and "what you actually hold" is a named, recurring bug class,
not a hypothetical.

## 6. backtrader — dead, and it matters because it's still the most-cited teaching tool

23k stars but zero pushes since **August 2024**; multiple community forks (e.g. a "LucidInvestor"
fork) have emerged specifically because the original is abandoned [directionally verified via repo
push timestamp + fork existence, motive for the fork inferred rather than confirmed by author
statement]. Backtrader is still the default answer in tutorials and "learn backtesting" content
despite this — a real trap for a beginner following current blog/course content into an unmaintained
codebase with no path to Python-version compatibility fixes going forward.

## 7. vectorbt — open core with an intentional bait-to-paid funnel

Officially licensed Apache-2.0 + Commons Clause ("fair-code") — free to use, **not free to resell as a
service** (LICENSE.md) [verified]. In the project's own "Future of VectorBT" discussion (#619), the
maintainer confirmed the open-source edition stays in maintenance mode (bug fixes, Python-version
compat) but that "entirely new features should be developed by the community" — i.e., new capability
development is being steered toward the invite-only paid VectorBT PRO product, not the free one
[verified, maintainer's own words]. Community reaction in the visible thread was muted acceptance, not
backlash, but the pattern is clear and is common across this space: open-source edition as the funnel,
paid edition as the actual product being sold.

## 8. FinRL / FinGPT — academic reinforcement-learning trading, revealed as research-only in practice

FinRL (16.1k stars, 310 open issues — by far the highest unresolved-issue count relative to size in
this sweep) has its top-commented issues almost entirely about **broken tutorial notebooks and paper
trading demos**, not strategy performance: #573 "Paper Trading Demo does not handle tick level data"
(28 comments, open), #1011/#1013 Colab notebooks failing, #962 "Yahoo data downloader does not
download any data??" [verified, `gh api search/issues`]. This is a strong maintenance-quality signal
independent of any trading-edge question: a meaningful share of users can't even get the demo running.

On substance, FinRL's own affiliated research is candid about the core problem: a trained RL agent
faces a "simulation-to-reality gap" and "cannot be directly deployed in real-world markets" without
further work, and financial RL specifically suffers low signal-to-noise ratio, survivorship bias in
historical data, and backtest overfitting from repeated hyperparameter retuning to chase better
backtest numbers (arxiv.org/pdf/2209.05559, "Deep Reinforcement Learning for Cryptocurrency Trading:
Practical Approach to Address Backtest Overfitting") [verified, peer-reviewed, though authored by
people affiliated with the FinRL ecosystem — grade as verified-but-not-independent]. FinGPT is
narrower in scope than the name implies: in practice it's a sentiment-analysis/forecasting
fine-tuning toolkit (FinGPT-Forecaster, sentiment LoRA models on HuggingFace) rather than a
trading-execution system — there is no evidence in the repo of a live-trading component; its
"applications" are financial NLP research artifacts [verified via README/changelog contents].

## 9. gs-quant — Goldman's OSS release, thin external adoption

12.8k stars but only **20 external contributors** on a repo with 69 open issues and a 3-year+ commit
history — this reads as "GS publishes and lightly supports an internal quant toolkit for recruiting/PR
and to standardize how counterparties interact with GS Marquee," not a community-driven retail trading
project. Confirmed by an issue literally asking "GS Marquee demo account?" (#328, closed) — i.e. real
functionality is gated behind GS's own Marquee platform access, which retail users don't have
[verified via `gh api` issue listing]. Useful as a quant-finance *library* (curves, instruments,
backtesting scaffolding) but not a path to an independent retail trading system.

## 10. StockSharp — broad connector coverage, oddly quiet on GitHub for its size

10.7k stars but the GitHub issue tracker is nearly empty relative to that (1 open issue via search,
181 closed total) [verified, `gh api search/issues`], versus freqtrade's 5,634 closed issues at 5x the
stars. Either usage is much lower than star count implies, or (more likely per the README, which
funnels users to StockSharp's own chat/forum and doc site rather than GitHub Issues) support happens
off-GitHub — which itself is a signal: less of the debugging/failure history is publicly mineable for
this project than for the Python-ecosystem tools, reducing the due-diligence value of the OSS repo
itself. StockSharp is C#/.NET, broad-market (forex, futures, crypto, Russian-market-oriented brokers),
and ships free core tools (Designer, Hydra, Terminal, Shell, API) per its own README — no independent
evidence of a marketplace scam was found in this sweep, but also no independent verified live-trading
success stories.

## 11. Zenbot & Gekko — why the two OG bots actually died

**Zenbot**: archived with an explicit "project is no longer actively maintained" banner. Its own
README disclaimer, still visible today, states: *"Zenbot is NOT a sure-fire profit machine... Never
leave the bot un-monitored for long periods of time. Zenbot doesn't know when to stop, so be prepared
to stop it if too much loss occurs... default trade parameters will underperform vs. a buy-hold
strategy"* [verified, primary source] — an unusually honest disclaimer for 2016-era crypto-bot
marketing. Its open-issue history (295 issues, never triaged down) includes real live-trading damage:
#1089 "ZenbotGot stuck at sell price and constantly selling at same price at loss" (24 comments) and
#1629 "Buy can execute during a sell that is currently in process causing invalid profit/loss values"
— i.e., a race condition that could double-execute trades [verified].

**Gekko**: archived directly by the author (Mike van Rossum) in 2019. Two stated reasons converge in
public reporting: (1) the author's personal trading effort moved into a private trading firm
("Folkvang") rather than open tooling, and (2) a high-profile plagiarism incident — YouTuber Siraj
Raval reportedly took Gekko's code, rebranded it as his own in a video that drew ~200,000 views,
which is described as a demoralizing last straw for the maintainer [anon/secondary-source
consolidation, not a primary statement I could directly fetch — the "Archiving open source Gekko"
Medium post itself returned HTTP 403 to automated fetch]. Gekko's archival is frequently cited in the
ecosystem as the cautionary tale for solo-maintainer burnout plus IP-theft risk in this space —
relevant if the user ever considers open-sourcing their own system.

## 12. LLM-agent trading repos — hype velocity has fully decoupled from verified performance

**TradingAgents** is the standout data point of this entire sweep: from ~9,300 stars in March 2026 to
101,608 stars by late August 2026 — a >10x run in under six months, briefly gaining over 7,000 stars
in a single week in May 2026 — while commit activity had gone quiet for roughly a month as of the
snapshot date. The project's own README is explicit that it is "designed for research purposes...
[performance] may vary... It is not intended as financial, investment, or trading advice"
(github.com/TauricResearch/TradingAgents README) [verified, primary source].

The GitHub issue tracker is the single richest failure-mode source found in this entire sweep. Issue
#225, titled (translated from Chinese) **"Has anyone actually made money using this project?"**,
drew replies that are worth quoting directly [anon, unverifiable individual claims, but directionally
consistent and numerous]:
- *"This project was built to write a paper — look at how many open issues there are, barely
  maintained — in actual operation it's basically an automatic money-losing machine."*
- *"I looked over the project, and it seems like a money-losing machine to me as well."*
- *"I read through the code. This is a tool that pulls news via the finnhub.io API and has AI agents
  debate over that news. For me personally, I'd rather just use finnhub.io directly — less biased
  info — then apply my own reasoning to guide the analysis myself."*
- *"Haha, if it really made money, why open-source it — why not just quietly use it yourself?"*

Issue #168, **"Results are NOT reproducible with AAPL symbol in the same date as in the paper,"** is
even more concrete: an independent user backtested the exact ticker/date range from the published
paper and got **−25.4% return** (vs. whatever the paper reported), then discovered a **look-ahead data
leak** — news articles dated in 2025 were leaking into a backtest window of Jan–Mar 2024 — and reported
that re-running the identical backtest gave **materially different results each time** (non-determinism
in an LLM-agent pipeline). Cost was also flagged: roughly $0.12/decision and ~$10 per full backtest run
in OpenAI API spend at the time [verified, primary GitHub thread, multiple independent commenters
converging on the same leak]. The maintainer's eventual response (commit 8a22594) added a
"Reproducibility" section to the README conceding that *"backtest returns depend on the model,
temperature, date range, and data quality, and aren't guaranteed to match any published figure"* and
reframed the project as "a research scaffold rather than a fixed strategy" [verified, maintainer's own
words]. That is about as close to a maintainer-admitted retraction of implied performance claims as
this sweep found anywhere.

**FinGPT** (see §8) is the more sober LLM-finance entry — it never claimed a trading track record,
just NLP tooling.

---

## Revealed preference: what the ecosystem actually converges on

1. **Spot crypto grid/DCA/momentum bots against major CEX APIs (Binance/Bybit/OKX/Kraken) is the
   dominant hobbyist activity.** freqtrade, hummingbot, OctoBot, jesse, Zenbot/Gekko-in-their-day all
   target this niche; it's the largest cluster by stars and by issue-tracker volume, and the failure
   modes are near-identical across all of them: exchange API/connector breakage, websocket
   disconnects, and P&L-reporting bugs — never a "the strategy math was wrong" story. **The bottleneck
   the ecosystem has converged on solving is plumbing reliability, not alpha generation.**
2. **Equities/futures backtesting engines (Lean, nautilus_trader, backtrader, vectorbt) are used far
   more for research/backtesting than for verified live retail trading** — issue trackers there skew
   toward backtest engine correctness (timestamp bugs, data catalogs, reconciliation) rather than "my
   strategy lost money live," partly because going live on regulated equities/futures brokers is a
   higher-friction step retail users often don't take.
3. **Market making (hummingbot) and statistical "edge" quantification (freqtrade's now-removed Edge
   module) are the two strategy classes the ecosystem has partially walked back from** — market making
   because inventory risk is unforgiving in trending markets, and Edge because a generic win-rate/RR
   calculator didn't survive real usage.
4. **RL-based (FinRL) and LLM-agent-based (TradingAgents, FinGPT) trading remain almost entirely
   unverified as live-money systems.** Both ecosystems' own top-voted community threads are dominated
   by "I can't even get the demo running" and "I can't reproduce your own paper's numbers," and the
   LLM-agent cluster in particular shows textbook backtest-with-lookahead-leakage plus non-determinism
   — the two most classic ways a paper trading result fails to mean anything.
5. **Brand-impersonation custodial scams are a structural tax on this ecosystem's popularity** —
   confirmed patterns riding on both Hummingbot's and OctoBot's names — meaning part of the "ongoing
   babysitting" cost of running any of these bots is vigilance against fake support channels/Discord
   invites/managed-account pitches that clone a real project's branding.
6. **Solo-maintainer burnout and license bait-and-switch are the two ways a beloved OSS trading tool
   dies**: Gekko (burnout + IP theft), Zenbot (unmaintained, race-condition bugs left unfixed),
   backtrader (silent abandonment since Aug 2024), vectorbt (soft-forked into a paid PRO product with
   new features withheld from the free tier). None of the fifteen projects here died from "the
   strategy stopped working" — they died from maintainer economics, which is itself informative: the
   software layer is not the durable bottleneck; a maintainer's continued unpaid time is.

# Parked ideas

Not on the build order (carry → TAA → xs_gbm). Each entry records what was checked so it isn't re-researched.

## Reddit crowd sentiment (parked 2026-10-06)

**Idea:** LLM extracts ticker + direction from r/wallstreetbets / r/stocks posts, aggregate daily, test whether
consensus predicts 1–20 day returns. Evolved from "trade on aggregate live-trader / streamer calls".

**Prior evidence (REPORT.md):** copy trading is a do-not-build; LLM sentiment is real but small (~3.3%/yr, decaying,
small caps); crowd positioning tends to be contrarian at extremes. Best fit is as a feature in build #4, not a standalone bot.

**Data check (no returns looked at):**
- Streams: no reliable timestamped history (Twitch VODs expire), heavy transcription, ToS issues. Dropped.
- Arctic Shift API: ~2–3 req/min under load; Jan 2021 WSB fails with "Timeout. Maybe slow down a bit". Not a backtest source.
- WSB 2019-06-04 14–20 UTC: 69 posts, 35 not removed, 1 cashtag post. Pre-2020 signal is thin.
- Bulk history needs the Arctic Shift per-subreddit dumps (size unchecked, likely GBs; needs Luke's OK to download).

**To revive:** TAA running unattended first; PREREG before any return look; confirm LLM extraction stays $0.

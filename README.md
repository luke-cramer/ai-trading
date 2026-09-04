# ai-trading

Personal trading research harness. Phase 1 (`REPORT.md`) ranked 20 strategy × market combinations and
picked three parallel builds. Phase 2 builds them one at a time on a shared harness.

| Build | Status | What it does |
|---|---|---|
| #2 Crypto carry measurement | **running unattended** | Logs Coinbase Derivatives hourly funding vs the same venue's dated-future basis for 60–90 days, then a pre-registered go/no-go. Zero capital. |
| #1 ETF dual-momentum / TAA | not started | Long-only monthly rotation with canary assets, paper first. |
| #4 Cross-sectional GBM + LLM features | not started | Daily ranking of liquid US names, forward-only, paper first. |

Paper and logging only. No live brokerage, no real money, no leverage.

## How it runs

GitHub Actions is the scheduler; the repo is the database.

- `carry-ingest` runs at :07 and :37 every hour. It pulls all sources, appends deduped rows under
  `data/carry/`, gzips the raw responses under `data/raw/carry/`, fails loudly if the newest funding print is
  more than 3 hours old, and commits.
- `carry-report` runs daily at 00:20 UTC (17:20 Pacific). It recomputes `data/carry/daily/`, writes
  `reports/carry/YYYY-MM-DD.md` (also `latest.md`), posts a one-line summary to the webhook, and commits.
- `tests` runs pytest on every code push.

Any failure posts to the webhook and shows up in the Actions tab. A missed hour is a permanent gap
(the venue publishes no history), which is why ingest runs twice an hour.

## Run locally

```bash
python3 -m venv .venv && .venv/bin/pip install pandas numpy pytest
.venv/bin/python -m pytest -q
.venv/bin/python -m strategies.carry ingest
.venv/bin/python -m strategies.carry report --no-post
.venv/bin/python -m strategies.carry replay
.venv/bin/python -m strategies.carry status
```

Copy `.env.example` to `.env` and export `ALERT_WEBHOOK_URL` to test alerts locally. The same commands
can run from a laptop `launchd` job as a backup writer; rows dedupe on timestamp so two writers are safe.

## What to watch

- `reports/carry/latest.md`: latest complete day, running mean net spread with a Newey-West 95% CI, hours
  missing, and the kill/go criteria checklist from `strategies/carry/PREREG.md`.
- The webhook channel: one summary line per day, plus any failure or stale-data alert.
- The Actions tab if the channel goes quiet for a day.

Nothing is decided before 60 complete days. The daily report is monitoring, not a decision.

## What you must do manually

1. **Set the webhook secret** in the repo (Settings → Secrets → Actions → `ALERT_WEBHOOK_URL`), a Slack or
   Discord incoming-webhook URL. Until then alerts print into the workflow log only.
2. **Keep the repo private.** It contains the dataset and daily reports.
3. Later builds will need accounts (Alpaca paper for #1 and #4). Nothing here needs one.

## Data sources

| Table | Source | Cadence |
|---|---|---|
| `funding` | Coinbase Advanced Trade public products endpoint (all CDE perpetual-style futures) | hourly |
| `dated` | same endpoint, BIT/ET dated futures | hourly |
| `spot` | Coinbase Exchange ticker BTC-USD, ETH-USD | hourly |
| `cboe` | Cboe continuous-futures funding CSV (cross-check) | daily |
| `treasury` | Treasury daily bill rates (4-week coupon equivalent = risk-free) | daily |
| `cme` | CME BTC monthly closes via Yahoo Finance (unofficial, cross-check only) | daily |
| `daily` | derived: funding APR, front-month basis APR, gross and net spread, cross-checks | daily, replayable |

cmegroup.com itself blocks automation and its terms prohibit it; it is not used.

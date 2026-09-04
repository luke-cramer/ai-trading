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

- `carry-ingest` runs at :13 and :43 every hour (triggered externally, see below). It pulls all sources, appends deduped rows under
  `data/carry/`, gzips the raw responses under `data/raw/carry/`, fails loudly if the newest funding print is
  more than 3 hours old, and commits.
- `carry-report` runs daily at 00:20 UTC (17:20 Pacific). It recomputes `data/carry/daily/`, writes
  `reports/carry/YYYY-MM-DD.md` (also `latest.md`), posts a one-line summary to the webhook, and commits.
- `tests` runs pytest on every code push.

Any failure posts to the webhook and shows up in the Actions tab. A missed hour is a permanent gap
(the venue publishes no history), which is why ingest runs twice an hour.

### External trigger (required: GitHub's cron does not fire for this repo)

Both workflows declare a `schedule`, but on 2026-09-04 GitHub ran zero scheduled jobs in four hours
(a 5-minute canary workflow never fired either, with Actions status operational). Until that changes,
a free external pinger calls the GitHub API to dispatch each workflow. The cron lines stay in the
workflows; if GitHub's scheduler wakes up, runs just dedupe.

1. **Token** — <https://github.com/settings/personal-access-tokens/new>: name `carry-dispatch`, expiration
   1 year, Repository access → *Only select repositories* → `ai-trading`, Repository permissions →
   *Actions: Read and write*. Generate and copy it. Nothing else needs it; do not put it in the repo.
2. **Pinger** — <https://cron-job.org> (free). Create two cronjobs, timezone **UTC**, request method
   **POST**, body `{"ref":"main"}`, headers:

   ```
   Accept: application/vnd.github+json
   Authorization: Bearer <the token>
   ```

   | Title | URL | Schedule (UTC) |
   |---|---|---|
   | carry-ingest | `https://api.github.com/repos/luke-cramer/ai-trading/actions/workflows/carry-ingest.yml/dispatches` | minutes 13 and 43, every hour |
   | carry-report | `https://api.github.com/repos/luke-cramer/ai-trading/actions/workflows/carry-report.yml/dispatches` | 00:20 daily |

   A successful dispatch returns HTTP 204 with an empty body; enable "save responses" to see it. The
   run then appears in the Actions tab as `workflow_dispatch`.
3. Put the token's expiry date in your calendar. When it lapses, ingest stops and the stale alert fires.

## Run locally

```bash
python3 -m venv .venv && .venv/bin/pip install pandas numpy pytest
.venv/bin/python -m pytest -q
.venv/bin/python -m strategies.carry ingest
.venv/bin/python -m strategies.carry report --no-post
.venv/bin/python -m strategies.carry replay
.venv/bin/python -m strategies.carry status
```

Copy `.env.example` to `.env` and export `ALERT_WEBHOOK_URL` to test alerts locally.

### Laptop backup writer (optional)

GitHub's cron is best-effort and can skip slots. `bin/carry-local.sh` runs the same ingest from this
checkout and pushes; rows dedupe on timestamp, so two writers are safe. Install it as a user launchd job
(runs at :22 and :52 while the laptop is awake):

```bash
cp launchd/com.lukecramer.carry-ingest.plist ~/Library/LaunchAgents/ && launchctl load ~/Library/LaunchAgents/com.lukecramer.carry-ingest.plist
```

Remove with `launchctl unload` on the same path. Log: `reports/carry-local.log` (gitignored).

## What to watch

- `reports/carry/latest.md`: latest complete day, running mean net spread with a Newey-West 95% CI, hours
  missing, and the kill/go criteria checklist from `strategies/carry/PREREG.md`.
- The webhook channel: one summary line per day, plus any failure or stale-data alert.
- The Actions tab if the channel goes quiet for a day.
- cron-job.org's execution history if runs stop appearing as `workflow_dispatch`.

Nothing is decided before 60 complete days. The daily report is monitoring, not a decision.

## What you must do manually

1. **Set the webhook secret** in the repo (Settings → Secrets → Actions → `ALERT_WEBHOOK_URL`), a Slack or
   Discord incoming-webhook URL. Until then alerts print into the workflow log only.
2. **Keep the repo private.** It contains the dataset and daily reports.
3. **Set up the external trigger** (token + cron-job.org) as described above. Without it nothing runs on a schedule.
4. Later builds will need accounts (Alpaca paper for #1 and #4). Nothing here needs one.

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

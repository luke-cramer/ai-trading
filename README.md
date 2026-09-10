# ai-trading

Personal trading research harness. Phase 1 (`REPORT.md`) ranked 20 strategy × market combinations and
picked three parallel builds. Phase 2 builds them one at a time on a shared harness.

| Build | Status | What it does |
|---|---|---|
| #2 Crypto carry measurement | **running unattended** | Logs Coinbase Derivatives hourly funding vs the same venue's dated-future basis for 60–90 days, then a pre-registered go/no-go. Zero capital. |
| #1 ETF dual-momentum / TAA | **built, schedule off** | HAA-Balanced monthly rotation (8 offensive ETFs, IEF/BIL defensive, TIP canary), $10k paper ledger, pre-registered in `strategies/taa/PREREG.md`. Daily job enabled once #2 has run a full day unattended. |
| #4 Cross-sectional GBM + LLM features | not started | Daily ranking of liquid US names, forward-only, paper first. |

Paper and logging only. No live brokerage, no real money, no leverage.

## How it runs

GitHub Actions runs the jobs, cron-job.org triggers them, the repo is the database.

- `carry-ingest` runs every 15 minutes (dispatched by cron-job.org, see below). It pulls all sources, appends deduped rows under
  `data/carry/`, gzips the raw responses under `data/raw/carry/`, fails loudly if the newest funding print is
  more than 3 hours old, and commits.
- `carry-report` runs daily at 00:25 UTC (17:25 Pacific). It recomputes `data/carry/daily/`, writes
  `reports/carry/YYYY-MM-DD.md` (also `latest.md`), posts a one-line summary to the webhook, and commits.
- `taa-daily` (build #1) runs weekdays at 22:45 UTC after the NY close once enabled: pulls closes, recomputes
  signals and the paper NAV, writes `reports/taa/latest.md`, posts to the webhook only on rebalance days.
- `tests` runs pytest on every code push.

Any failure posts to the webhook and shows up in the Actions tab. A missed hour is a permanent gap
(the venue publishes no history), which is why ingest runs so often.

### External scheduler and a dead man's switch

GitHub's `schedule:` trigger is best-effort and here it fired about 7 times a day against 144 slots, with
the daily report landing 4.5 h late. It was removed on 2026-09-10; workflows are `workflow_dispatch` only.

1. **cron-job.org** (free) dispatches the workflows through the GitHub API. Setup:
   - Token: <https://github.com/settings/personal-access-tokens/new>. Name `carry-dispatch`, expiration
     1 year, Repository access → *Only select repositories* → `ai-trading`, Repository permissions →
     *Actions: Read and write*. Copy it; it lives only in cron-job.org.
   - Two cronjobs, timezone **UTC**, method **POST**, body `{"ref":"main"}`, headers
     `Accept: application/vnd.github+json` and `Authorization: Bearer <token>`:

     | Title | URL | Schedule (UTC) |
     |---|---|---|
     | carry-ingest | `https://api.github.com/repos/luke-cramer/ai-trading/actions/workflows/carry-ingest.yml/dispatches` | every 15 minutes |
     | carry-report | `https://api.github.com/repos/luke-cramer/ai-trading/actions/workflows/carry-report.yml/dispatches` | 00:25 daily |

   - A test run returns HTTP 204 (empty body) and a `workflow_dispatch` run appears in the Actions tab.
     Duplicate runs are harmless: rows dedupe on timestamp and the concurrency group serializes commits.
   - Calendar the token expiry. When it lapses nothing runs; healthchecks will tell you within 90 minutes.
   - Status: both jobs live since 2026-09-10 (job ids 8426776, 8426809); token `carry-dispatch` expires 2027-09-10.
     The cron-job.org URL field ignores browser autofill: click it and type. Test run is on the job edit page.
2. **healthchecks.io** (free) as a dead man's switch. The ingest job pings a URL after every success (and
   `/fail` on failure); if no ping arrives for 90 minutes healthchecks messages you. This is what catches
   scheduler silence, which the in-job stale check cannot. Setup: create a check with period 10 min,
   grace 80 min, add your Slack (or email) integration, then set the ping URL as the repo secret
   `HEALTHCHECK_URL`.

## Run locally

```bash
python3 -m venv .venv && .venv/bin/pip install pandas numpy pytest
.venv/bin/python -m pytest -q
.venv/bin/python -m strategies.carry ingest
.venv/bin/python -m strategies.carry report --no-post
.venv/bin/python -m strategies.carry replay
.venv/bin/python -m strategies.carry status
.venv/bin/python -m strategies.taa ingest --full     # first run: full ETF history (needs TIINGO_TOKEN or a laptop IP for Yahoo)
.venv/bin/python -m strategies.taa report --no-post  # signals, paper ledger, NAV, reports/taa/latest.md
.venv/bin/python -m strategies.taa replay            # evaluation + pre-registered criteria
```

Copy `.env.example` to `.env` and export `ALERT_WEBHOOK_URL` to test alerts locally.

### Laptop backup writer (optional)

A third writer if you want one. `bin/carry-local.sh` runs the same ingest from this
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
- healthchecks.io will message you if ingest stops pinging for 90 minutes.

Nothing is decided before 60 complete days. The daily report is monitoring, not a decision.

## What you must do manually

1. **Set the webhook secret** in the repo (Settings → Secrets → Actions → `ALERT_WEBHOOK_URL`), a Slack or
   Discord incoming-webhook URL. Until then alerts print into the workflow log only.
2. **Set the healthchecks secret** `HEALTHCHECK_URL` as described above. (cron-job.org dispatcher: done 2026-09-10.)
3. The repo is public: never commit `.env`, tokens, or account details. Secrets live in GitHub settings only.
4. **Build #1 needs a Tiingo token.** Free account at <https://www.tiingo.com>, copy the API token, add it as
   repo secret `TIINGO_TOKEN`. Yahoo returns 429 to GitHub runner IPs, so without it `taa-daily` fails.
5. Later builds will need accounts (Alpaca paper for #1 and #4). Nothing here needs one.

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
| `taa/prices`, `taa/events` | Tiingo daily prices API (primary, free token); Yahoo chart API (laptop fallback) | daily |
| `taa/signals`, `taa/ledger`, `taa/nav` | derived: month-end momentum and weights, paper fills, daily NAV vs 60/40 and SPY | replayable |

cmegroup.com itself blocks automation and its terms prohibit it; it is not used.

# ai-trading — project instructions

Personal research harness for the three builds ranked in `REPORT.md` (phase-1 research spike; its
conclusions are settled, do not re-litigate). Goals: learn, run a real system, small chance of modest profit.
Build complexity is free (built with Claude); recurring cost, capital at risk, and babysitting time are not.

## Hard rules (override everything else)

- **Paper / logging only.** Nothing touches a live brokerage or real money until Luke says so in a later
  session. **No leverage anywhere in the design, ever** (any future position must be fully collateralized at 1x).
- **Never handle secrets.** Tell Luke which env vars / repo secrets to set. `.env` is gitignored; keep `.env.example` current.
- **Build one thing to "running unattended" before touching the next.** Order: #2 carry measurement (live) → #1 ETF TAA → #4 cross-sectional GBM.
- **Commit small logical batches straight to `main`.** No PRs. Data commits come from the `carry-bot` workflows.
- **Scheduled jobs are idempotent**, store UTC, dedupe by timestamp, backfill what sources allow on restart. Gaps are recorded, never interpolated.
- **Small logged data (CSV) is committed** so the dataset survives. Raw I/O of every automated run is gzipped under `data/raw/`.
- **Tests for cost models and signal logic; a replay mode** so the pipeline can be checked against stored history.
- **Pre-registration before the first backtest/report** (`strategies/<name>/PREREG.md`): hypothesis, universe,
  costs with sources, evaluation, kill criteria. No parameter changes after the first out-of-sample look.
  Evaluation is forward-only with Newey-West errors and PSR/deflated Sharpe.
- **$0/mo recurring.** Ask before any paid tier or API. Verify live that a source is free and reachable before designing around it.

## Run

```bash
python3 -m venv .venv && .venv/bin/pip install pandas numpy pytest   # once
.venv/bin/python -m pytest -q
.venv/bin/python -m strategies.carry ingest        # pull all sources once (idempotent)
.venv/bin/python -m strategies.carry report        # recompute daily table, write reports/carry/, post summary
.venv/bin/python -m strategies.carry report --no-post
.venv/bin/python -m strategies.carry check-stale   # exit 1 + alert if newest funding print > 3h old
.venv/bin/python -m strategies.carry replay        # recompute daily table from stored CSVs, print stats
.venv/bin/python -m strategies.carry status        # row counts and newest timestamps
```

Env: `ALERT_WEBHOOK_URL` (Slack or Discord incoming webhook; unset → alerts print to stderr).
Local timezone is America/Los_Angeles; everything stored is UTC.

## Layout

```
harness/            shared, strategy-agnostic: clock (UTC), http (retries), rawlog (gz raw I/O),
                    storage (month-partitioned CSV tables deduped on key), alerts (one webhook)
strategies/carry/   build #2: tables.py (schemas) → ingest.py → signal.py (daily spread) → report.py
                    costs.py (cost model), prereg.py + PREREG.md (frozen evaluation), check.py (stale)
strategies/taa/     build #1 (not started)      strategies/xs_gbm/   build #4 (not started)
data/carry/<table>/YYYY-MM.csv   committed datasets      data/raw/carry/YYYY/MM/DD/   gz raw responses
reports/carry/YYYY-MM-DD.md      daily reports (+ latest.md)
.github/workflows/  carry-ingest (7,37 * * * *), carry-report (00:20 UTC), tests
research/           phase-1 corpus (read-only)
```

Every build follows the same shape: ingestion → signal → paper/live execution → nightly report, with
`harness.storage.Table` for data and `harness.alerts.send` for anything a human should see.

## Conventions

- Python 3.12, stdlib HTTP, pandas only for analysis. Keep dependencies minimal.
- Table first column is the UTC timestamp/date used for month partitioning; `key` columns define dedupe.
- Cross-check sources (Yahoo/CME, Cboe) never fail a run; primary sources (CDE, spot) do.
- Comments: one line, only for a non-obvious *why*. Sources for cost assumptions go in PREREG.md.
- Workflows push data with `git pull --rebase` + retry under the `carry-data` concurrency group.

## Data-source status (verified 2026-09-04)

- Coinbase Advanced Trade public products endpoint: free, no key, gives hourly funding + dated futures. Primary.
- cmegroup.com: blocks scripts and its terms prohibit automation. Never scrape it. CME closes come from Yahoo (unofficial, cross-check only).
- Coinbase funding-history web page: 403 to scripts. We build our own history; outages lose hours permanently.

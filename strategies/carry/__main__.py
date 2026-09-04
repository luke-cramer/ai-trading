"""CLI: python -m strategies.carry <ingest|report|check-stale|replay|status>"""
from __future__ import annotations

import argparse
import json
import sys

from harness import alerts
from strategies.carry.ingest import HOURLY, SOURCES


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="carry")
    sub = ap.add_subparsers(dest="cmd", required=True)
    i = sub.add_parser("ingest", help="pull sources once (idempotent)")
    i.add_argument("--sources", default=",".join(HOURLY), help=f"comma list from {','.join(SOURCES)}; default hourly set")
    r = sub.add_parser("report", help="recompute daily series, write markdown, post summary")
    r.add_argument("--no-post", action="store_true", help="do not post to the webhook")
    sub.add_parser("check-stale", help="exit 1 and alert if newest funding print is >3h old")
    sub.add_parser("replay", help="recompute the daily table from stored CSVs, print it, post nothing")
    sub.add_parser("status", help="row counts and newest timestamps per table")
    a = ap.parse_args(argv)

    if a.cmd == "ingest":
        from strategies.carry import ingest
        try:
            s = ingest.run(sources=tuple(a.sources.split(",")))
        except Exception as e:
            alerts.send(f"carry ingest FAILED: {e}", level="error")
            raise
        print(json.dumps(s))
        noisy = [e for e in s.get("errors", []) if not e.startswith("cme:")]
        if noisy:
            alerts.send("carry ingest: non-critical source errors: " + "; ".join(noisy), level="warn")
        return 0
    if a.cmd == "report":
        from strategies.carry import report
        p = report.run(post=not a.no_post)
        print(p)
        return 0
    if a.cmd == "check-stale":
        from strategies.carry import check
        return check.run()
    if a.cmd == "replay":
        from strategies.carry import report
        daily = report.recompute_daily()
        print(daily.to_string(index=False))
        ev = report.evaluation(daily)
        print(json.dumps({k: (None if v != v else v) for k, v in ev.items()}, indent=1, default=float))
        return 0
    if a.cmd == "status":
        from strategies.carry import tables as T
        for name in ("FUNDING", "DATED", "SPOT", "CBOE", "TREASURY", "CME", "DAILY"):
            t = getattr(T, name)
            df = t.read()
            print(f"{name:9s} rows={len(df):6d} newest={df[t.columns[0]].max() if len(df) else '-'}")
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(main())

"""CLI: python -m strategies.taa <ingest|report|replay|status>"""
from __future__ import annotations

import argparse
import json
import sys

from harness import alerts


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="taa")
    sub = ap.add_subparsers(dest="cmd", required=True)
    i = sub.add_parser("ingest", help="pull daily closes + events (idempotent)")
    i.add_argument("--full", action="store_true", help="fetch full history (first run or repair)")
    r = sub.add_parser("report", help="recompute signals/ledger/NAV, write reports/taa/, post on rebalance days")
    r.add_argument("--no-post", action="store_true")
    r.add_argument("--post", action="store_true", help="post the summary line even if today is not a rebalance day")
    sub.add_parser("replay", help="recompute everything from stored CSVs and print the evaluation")
    sub.add_parser("status", help="row counts and newest dates per table")
    a = ap.parse_args(argv)

    if a.cmd == "ingest":
        from strategies.taa import ingest
        from strategies.taa import tables as T
        try:
            s = ingest.run(full=a.full)
        except Exception as e:
            alerts.send(f"taa ingest FAILED: {e}", level="error")
            raise
        for t in (T.PRICES, T.EVENTS):
            t.compact()
        print(json.dumps(s))
        if s["splits"]:
            alerts.send(f"taa: split event stored for {s['splits']}; verify total-return adjustment before the next rebalance", level="warn")
        if s["errors"]:
            alerts.send("taa ingest: partial failure: " + "; ".join(s["errors"]), level="warn")
        return 0
    if a.cmd == "report":
        from strategies.taa import report
        try:
            print(report.run(post=not a.no_post, force_post=a.post))
        except Exception as e:
            alerts.send(f"taa report FAILED: {e}", level="error")
            raise
        return 0
    if a.cmd == "replay":
        from strategies.taa import prereg, report
        tr, sig = report.load()
        ev = report.evaluation(tr, sig)
        print(json.dumps({k: v for k, v in ev.items() if not k.startswith("_")}, indent=1, default=lambda v: None if v != v else float(v)))
        for name, ok, detail in prereg.criteria_status(ev):
            print(f"[{'x' if ok else ' '}] {name}: {detail}")
        return 0
    if a.cmd == "status":
        from strategies.taa import tables as T
        for name in ("PRICES", "EVENTS", "SIGNALS", "LEDGER", "NAV"):
            t = getattr(T, name)
            df = t.read()
            print(f"{name:8s} rows={len(df):6d} newest={df['date'].max() if len(df) else '-'}")
        return 0
    return 2


if __name__ == "__main__":
    sys.exit(main())

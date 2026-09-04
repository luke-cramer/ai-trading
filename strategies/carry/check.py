"""Stale-data check: fail loudly if the newest BIP funding print is older than the threshold."""
from __future__ import annotations

from datetime import timedelta

import pandas as pd

from harness import alerts
from harness.clock import iso, now
from strategies.carry import tables as T

STALE_AFTER = timedelta(hours=3)


def newest_funding_time() -> pd.Timestamp | None:
    f = T.FUNDING.read()
    f = f[f["product_id"] == T.PERP_BTC]
    return None if f.empty else pd.to_datetime(f["funding_time"], utc=True).max()


def run() -> int:
    t = newest_funding_time()
    at = now()
    if t is None:
        alerts.send(f"carry: no funding rows at all as of {iso(at)}", level="error")
        return 1
    age = at - t.to_pydatetime()
    if age > STALE_AFTER:
        alerts.send(f"carry: STALE funding data — newest {T.PERP_BTC} print {iso(t.to_pydatetime())} is {age} old", level="error")
        return 1
    print(f"ok: newest funding {iso(t.to_pydatetime())} ({age} old)")
    return 0

"""Pre-registered evaluation constants. Frozen at first commit; changing any value requires a new PREREG version."""
from __future__ import annotations

MEASUREMENT_DAYS = 60          # decision window, complete days
EXTENDED_DAYS = 90             # if data integrity fails at 60
MIN_HOURS_FOR_DAY = 20         # a day counts as complete with >= 20 of 24 funding prints
MAX_MISSING_FRAC = 0.20        # more than this missing -> extend, do not decide
GO_MIN_NET_APR = 0.02          # 2 pp net of costs
GO_MIN_FRAC_POSITIVE = 0.60
NW_LAGS = 5


def criteria_status(ev: dict) -> list[tuple[str, bool, str]]:
    days = ev["days_complete"]
    missing_frac = 1 - ev["hours_observed"] / ev["hours_expected"] if ev["hours_expected"] else 1.0
    enough = days >= MEASUREMENT_DAYS
    integrity = missing_frac <= MAX_MISSING_FRAC
    mean_ok = ev["mean_net"] == ev["mean_net"] and ev["mean_net"] >= GO_MIN_NET_APR
    ci_ok = ev["ci_low"] == ev["ci_low"] and ev["ci_low"] > 0
    frac_ok = ev["frac_positive"] == ev["frac_positive"] and ev["frac_positive"] >= GO_MIN_FRAC_POSITIVE
    verdict = "not yet — keep measuring"
    if enough and not integrity and days < EXTENDED_DAYS:
        verdict = f"EXTEND to {EXTENDED_DAYS} days (missing {missing_frac:.0%} > {MAX_MISSING_FRAC:.0%})"
    elif enough and (integrity or days >= EXTENDED_DAYS):
        verdict = "GO: spread persists — plan phase 2 (paper first)" if (mean_ok and ci_ok and frac_ok) else "KILL: no tradeable spread — publish the dataset, do not trade"
    return [
        (f"≥{MEASUREMENT_DAYS} complete days", enough, f"{days}/{MEASUREMENT_DAYS}"),
        (f"missing hours ≤ {MAX_MISSING_FRAC:.0%}", integrity, f"{missing_frac:.1%} missing"),
        (f"mean net spread ≥ {GO_MIN_NET_APR:.0%}", mean_ok, f"{ev['mean_net']*100:+.2f}%" if ev["mean_net"] == ev["mean_net"] else "n/a"),
        ("Newey-West 95% CI excludes 0", ci_ok, f"low {ev['ci_low']*100:+.2f}%" if ev["ci_low"] == ev["ci_low"] else "n/a"),
        (f"days net-positive ≥ {GO_MIN_FRAC_POSITIVE:.0%}", frac_ok, f"{ev['frac_positive']:.0%}" if ev["frac_positive"] == ev["frac_positive"] else "n/a"),
        ("verdict", enough and (mean_ok and ci_ok and frac_ok), verdict),
    ]

"""Frozen parameters of the pre-registered evaluation (PREREG.md v1). Do not tune after the implementation check."""
from __future__ import annotations

MOMENTUM_LAGS_MONTHS = (1, 3, 6, 12)   # 13612U: unweighted mean of 1, 3, 6, 12-month total returns
TOP_N = 4                              # offensive positions when the canary is risk-on
BACKTEST_START = "2008-01-31"          # first month-end where every ETF in the universe has 12 months of history
PAPER_START = "2026-09-30"             # first signal date of the forward paper record; fill on the next trading day
PAPER_NAV_USD = 10_000.0
FORWARD_MIN_MONTHS = 36                # months of paper record before a GO decision
KILL_DRAWDOWN_MULT = 1.25              # forward drawdown > this × backtest max drawdown ⇒ KILL
KILL_DRAWDOWN_ABS = -0.30
KILL_UNDERPERFORM_PP = 0.03            # 36-month CAGR below 60/40 by more than this, with no drawdown benefit ⇒ KILL
NW_LAGS = 3                            # monthly series


def criteria_status(ev: dict) -> list[tuple[str, bool, str]]:
    """Checklist against the pre-registered criteria on the forward paper record. ev from report.evaluation()."""
    out = []
    months = ev.get("forward_months", 0)
    enough = months >= FORWARD_MIN_MONTHS
    out.append(("forward record", enough, f"{months}/{FORWARD_MIN_MONTHS} months"))
    bt_dd, fw_dd = ev.get("backtest_max_dd"), ev.get("forward_max_dd")
    dd_ok = fw_dd is None or fw_dd != fw_dd or (fw_dd > KILL_DRAWDOWN_ABS and fw_dd > KILL_DRAWDOWN_MULT * bt_dd)
    out.append(("drawdown within envelope", dd_ok, f"forward {fw_dd:+.1%} vs limit {max(KILL_DRAWDOWN_ABS, KILL_DRAWDOWN_MULT * bt_dd):+.1%}"
                if fw_dd == fw_dd and fw_dd is not None else "n/a"))
    gap = ev.get("forward_cagr_vs_6040")
    dd_better = (ev.get("forward_max_dd") or 0) > (ev.get("forward_bench_max_dd") or 0)
    under_ok = gap is None or gap != gap or gap > -KILL_UNDERPERFORM_PP or dd_better
    out.append(("not underperforming 60/40 without drawdown benefit", under_ok, f"CAGR gap {gap:+.1%}" if gap == gap and gap is not None else "n/a"))
    if not dd_ok or (enough and not under_ok):
        verdict = "KILL"
    elif enough:
        verdict = "GO to phase-2 review (needs Luke's written approval + tax review; still no leverage)"
    else:
        verdict = "not yet — keep paper trading"
    out.append(("verdict", dd_ok and under_ok, verdict))
    return out

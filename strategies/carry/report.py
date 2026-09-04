"""Daily report: latest day, running evaluation stats, data-integrity flags. Markdown to reports/carry/, summary to webhook."""
from __future__ import annotations

from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd

from harness import alerts
from harness.clock import iso, now
from strategies.carry import prereg, signal
from strategies.carry import tables as T

REPORT_DIR = Path("reports/carry")


def _pct(v) -> str:
    try:
        return "n/a" if v == "" or pd.isna(float(v)) else f"{float(v) * 100:+.2f}%"
    except (TypeError, ValueError):
        return "n/a"


def _dte(v) -> str:
    try:
        return f"{float(v):.1f}"
    except (TypeError, ValueError):
        return "?"


def _load_all() -> dict[str, pd.DataFrame]:
    return {n: t.read() for n, t in (("funding", T.FUNDING), ("dated", T.DATED), ("spot", T.SPOT), ("cboe", T.CBOE),
                                      ("treasury", T.TREASURY), ("cme", T.CME))}


def recompute_daily(computed_at: datetime | None = None) -> pd.DataFrame:
    d = _load_all()
    daily = signal.compute_daily(d["funding"], d["dated"], d["spot"], d["cboe"], d["treasury"], d["cme"], computed_at)
    # derived table: rewrite in full (replay semantics), then read back so callers see the canonical form
    for p in (T.DAILY.dir.glob("*.csv") if T.DAILY.dir.exists() else []):
        p.unlink()
    T.DAILY.append(daily.to_dict("records"))
    return T.DAILY.read()


def hours_expected(daily: pd.DataFrame, at: datetime) -> int:
    """Hourly prints expected between the first logged funding hour and now, inclusive."""
    if daily.empty:
        return 0
    first = pd.Timestamp(daily["date"].min(), tz="UTC")
    f = T.FUNDING.read()
    f = f[f["product_id"] == T.PERP_BTC]
    if not f.empty:
        first = pd.to_datetime(f["funding_time"], utc=True).min()
    last = pd.Timestamp(at).floor("h")
    return max(int((last - first) / pd.Timedelta(hours=1)) + 1, 0)


def evaluation(daily: pd.DataFrame, at: datetime | None = None) -> dict:
    at = at or now()
    complete = daily[pd.to_numeric(daily["hours_observed"], errors="coerce") >= prereg.MIN_HOURS_FOR_DAY].copy()
    x = pd.to_numeric(complete["spread_net_apr"], errors="coerce").to_numpy()
    xg = pd.to_numeric(complete["spread_gross_apr"], errors="coerce").to_numpy()
    m, se, t = signal.newey_west_mean(x, lags=prereg.NW_LAGS)
    sr, psr = signal.probabilistic_sharpe(x)
    valid = x[~np.isnan(x)]
    return dict(
        days_total=len(daily), days_complete=len(complete), days_with_spread=int(len(valid)),
        mean_net=m, se_net=se, t_net=t, ci_low=m - 1.96 * se if se == se else float("nan"),
        ci_high=m + 1.96 * se if se == se else float("nan"),
        mean_gross=float(np.nanmean(xg)) if len(xg) and not np.all(np.isnan(xg)) else float("nan"),
        frac_positive=float((valid > 0).mean()) if len(valid) else float("nan"),
        sharpe_daily=sr, psr=psr,
        hours_expected=hours_expected(daily, at), hours_observed=int(pd.to_numeric(daily["hours_observed"], errors="coerce").fillna(0).sum()),
    )


def latest_day(daily: pd.DataFrame) -> pd.Series | None:
    """Most recent complete day; falls back to the newest partial day."""
    if daily.empty:
        return None
    hrs = pd.to_numeric(daily["hours_observed"], errors="coerce")
    complete = daily[hrs >= prereg.MIN_HOURS_FOR_DAY]
    return (complete if len(complete) else daily).iloc[-1]


def render(daily: pd.DataFrame, ev: dict, at: datetime) -> str:
    last = latest_day(daily)
    day_target = prereg.MEASUREMENT_DAYS
    lines = [f"# Carry measurement — daily report {at.strftime('%Y-%m-%d')} (generated {iso(at)})", ""]
    if last is not None:
        lines += [f"## Latest day: {last['date']} (UTC)", "",
                  f"| metric | value |", f"|---|---|",
                  f"| BIP funding APR | {_pct(last['funding_apr'])} ({last['hours_observed']}/24 hours) |",
                  f"| BIT front basis APR | {_pct(last['basis_apr'])} ({last['front_product'] or 'n/a'}, {_dte(last['front_days_to_expiry'])} dte, {last['basis_hours'] or 0} hrs) |",
                  f"| spread gross | {_pct(last['spread_gross_apr'])} |",
                  f"| cost drag | {_pct(last['cost_drag_apr'])} |",
                  f"| **spread net** | **{_pct(last['spread_net_apr'])}** |",
                  f"| Cboe PBT funding APR (cross-check) | {_pct(last['cboe_funding_apr'])} |",
                  f"| CME front basis APR (cross-check, {last['cme_front_symbol'] or 'n/a'}) | {_pct(last['cme_basis_apr'])} |",
                  f"| 4-week T-bill | {_pct(last['rf_apr'])} |", ""]
    miss = ev["hours_expected"] - ev["hours_observed"]
    lines += ["## Running evaluation (pre-registered; see PREREG.md)", "",
              f"- Days logged: {ev['days_total']} of {day_target} target; complete days (≥{prereg.MIN_HOURS_FOR_DAY}h): {ev['days_complete']}; days with a spread: {ev['days_with_spread']}",
              f"- Mean net spread: {_pct(ev['mean_net'])} (Newey-West 95% CI {_pct(ev['ci_low'])} to {_pct(ev['ci_high'])}, t={ev['t_net']:.2f})",
              f"- Mean gross spread: {_pct(ev['mean_gross'])}; days net-positive: {_pct(ev['frac_positive'])}",
              f"- Daily Sharpe of net spread: {ev['sharpe_daily']:.3f}; PSR(SR*=0): {ev['psr']:.3f}",
              f"- Hours observed: {ev['hours_observed']} / {ev['hours_expected']} ({miss} missing)", "",
              "## Kill / go criteria status", ""]
    for name, ok, detail in prereg.criteria_status(ev):
        lines.append(f"- {'✅' if ok else '⏳'} {name}: {detail}")
    lines += ["", "## Last 10 days", "", "| date | hrs | funding | basis | net | cboe | cme |", "|---|---|---|---|---|---|---|"]
    for _, r in daily.tail(10).iterrows():
        lines.append(f"| {r['date']} | {r['hours_observed']} | {_pct(r['funding_apr'])} | {_pct(r['basis_apr'])} | {_pct(r['spread_net_apr'])} | {_pct(r['cboe_funding_apr'])} | {_pct(r['cme_basis_apr'])} |")
    return "\n".join(lines) + "\n"


def summary_line(daily: pd.DataFrame, ev: dict) -> str:
    last = latest_day(daily)
    head = "carry daily report"
    if last is None:
        return f"{head}: no data yet"
    return (f"{head} {last['date']}: funding {_pct(last['funding_apr'])} | basis {_pct(last['basis_apr'])} | "
            f"net {_pct(last['spread_net_apr'])} ({last['hours_observed']}/24h). "
            f"Running: {ev['days_complete']}/{prereg.MEASUREMENT_DAYS} days, mean net {_pct(ev['mean_net'])} "
            f"[{_pct(ev['ci_low'])}, {_pct(ev['ci_high'])}], {ev['hours_expected'] - ev['hours_observed']} hrs missing.")


def run(at: datetime | None = None, post: bool = True) -> Path:
    at = at or now()
    daily = recompute_daily(at)
    ev = evaluation(daily, at)
    md = render(daily, ev, at)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    p = REPORT_DIR / f"{at.strftime('%Y-%m-%d')}.md"
    p.write_text(md)
    (REPORT_DIR / "latest.md").write_text(md)
    if post:
        alerts.send(summary_line(daily, ev))
    return p

"""Recompute signals, paper ledger and NAV from stored prices; write reports/taa/; post on rebalance days."""
from __future__ import annotations

import math
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd

from harness import alerts
from harness.clock import iso, now
from harness.stats import cagr, max_drawdown, newey_west_mean, probabilistic_sharpe
from strategies.taa import paper, prereg, signal
from strategies.taa import tables as T

REPORT_DIR = Path("reports/taa")
TRADING_DAYS = 252


def load() -> tuple[pd.DataFrame, pd.DataFrame]:
    tr = signal.total_return_prices(T.PRICES.read(), T.EVENTS.read())
    return tr, signal.signals(tr)


def _stats(nav: pd.DataFrame, bench: pd.DataFrame) -> dict:
    if nav.empty:
        return dict(months=0)
    n = nav["nav"].to_numpy()
    b = bench.set_index("date")["nav"].reindex(nav["date"]).to_numpy() if not bench.empty else np.full(len(n), np.nan)
    daily = np.diff(n) / n[:-1]
    m = nav.assign(ym=nav["date"].str[:7]).groupby("ym")["nav"].last()
    monthly = m.pct_change().dropna().to_numpy()
    bm = pd.Series(b, index=nav["date"]).groupby(nav["date"].str[:7].values).last().pct_change().dropna().to_numpy()
    excess = monthly - bm if len(bm) == len(monthly) else np.array([])
    nw = newey_west_mean(excess, prereg.NW_LAGS) if len(excess) else (math.nan, math.nan, math.nan)
    sr, psr = probabilistic_sharpe(excess) if len(excess) else (math.nan, math.nan)
    return dict(months=len(monthly), start=nav["date"].iloc[0], end=nav["date"].iloc[-1], nav=float(n[-1]),
                cagr=cagr(n, TRADING_DAYS), max_dd=max_drawdown(n), vol=float(daily.std(ddof=1) * math.sqrt(TRADING_DAYS)) if len(daily) > 1 else math.nan,
                bench_cagr=cagr(b, TRADING_DAYS) if not np.isnan(b).all() else math.nan, bench_max_dd=max_drawdown(b[~np.isnan(b)]),
                excess_monthly_mean=nw[0], excess_monthly_se=nw[1], excess_sr_monthly=sr, psr=psr)


def evaluation(tr: pd.DataFrame, sig: pd.DataFrame) -> dict:
    bt_nav, _ = paper.simulate(tr, sig, prereg.PAPER_NAV_USD, prereg.BACKTEST_START, end=prereg.PAPER_START)
    bt_bench = paper.fixed_mix(tr, T.BENCHMARK_6040, prereg.PAPER_NAV_USD, prereg.BACKTEST_START, end=prereg.PAPER_START)
    fw_nav, fills = paper.simulate(tr, sig, prereg.PAPER_NAV_USD, prereg.PAPER_START)
    fw_bench = paper.fixed_mix(tr, T.BENCHMARK_6040, prereg.PAPER_NAV_USD, prereg.PAPER_START)
    fw_spy = paper.fixed_mix(tr, {"SPY": 1.0}, prereg.PAPER_NAV_USD, prereg.PAPER_START)
    bt, fw = _stats(bt_nav, bt_bench), _stats(fw_nav, fw_bench)
    ev = {f"backtest_{k}": v for k, v in bt.items()} | {f"forward_{k}": v for k, v in fw.items()}
    ev["forward_cagr_vs_6040"] = fw.get("cagr", math.nan) - fw.get("bench_cagr", math.nan) if fw.get("months") else math.nan
    ev["_fw_nav"], ev["_fills"], ev["_fw_bench"], ev["_fw_spy"] = fw_nav, fills, fw_bench, fw_spy
    return ev


def _pct(v) -> str:
    return "n/a" if v is None or v != v else f"{v:+.1%}"


def render(tr: pd.DataFrame, sig: pd.DataFrame, ev: dict, at: datetime) -> str:
    latest = sig[sig["date"] == sig["date"].max()] if not sig.empty else sig
    lines = [f"# TAA paper report — {at.strftime('%Y-%m-%d')} (computed {iso(at)})", ""]
    lines += ["Long-only HAA-Balanced rotation, paper only, no leverage. Rules and criteria: `strategies/taa/PREREG.md` v1.", ""]
    if not latest.empty:
        d = latest["date"].iloc[0]
        on = bool(latest["canary_on"].iloc[0])
        lines += [f"## Latest signal ({d}) — canary {'RISK-ON' if on else 'RISK-OFF'}", "", "| symbol | momentum | weight |", "|---|---|---|"]
        for _, r in latest.sort_values(["weight", "momentum"], ascending=False).iterrows():
            lines.append(f"| {r['symbol']} | {r['momentum']:+.2%} | {r['weight']:.0%} |")
        lines.append("")
    fw = ev["_fw_nav"]
    lines += ["## Forward paper record (from PREREG PAPER_START, $%.0f notional)" % prereg.PAPER_NAV_USD, ""]
    if fw.empty:
        lines += ["No fills yet: the first fill is the trading day after the first month-end on or after "
                  f"{prereg.PAPER_START}.", ""]
    else:
        lines += [f"- {ev['forward_start']} → {ev['forward_end']}: NAV ${ev['forward_nav']:,.2f}, {ev['forward_months']} complete months",
                  f"- CAGR {_pct(ev['forward_cagr'])} vs 60/40 {_pct(ev['forward_bench_cagr'])}; max drawdown {_pct(ev['forward_max_dd'])} vs {_pct(ev['forward_bench_max_dd'])}",
                  f"- Monthly excess vs 60/40: {_pct(ev['forward_excess_monthly_mean'])} ± {_pct(ev['forward_excess_monthly_se'])} (Newey-West), PSR {ev['forward_psr']:.2f}"
                  if ev["forward_psr"] == ev["forward_psr"] else "- Monthly excess vs 60/40: n/a (need ≥3 months)", ""]
        fills = ev["_fills"]
        if not fills.empty:
            last = fills[fills["date"] == fills["date"].max()]
            lines += [f"### Last rebalance {last['date'].iloc[0]}", "", "| symbol | weight | price | shares | traded | cost |", "|---|---|---|---|---|---|"]
            for _, r in last.iterrows():
                lines.append(f"| {r['symbol']} | {r['weight']:.0%} | {r['price']:.2f} | {r['shares']:.4f} | {r['traded_usd']:+,.2f} | {r['cost_usd']:.2f} |")
            lines.append("")
    lines += ["## Pre-registered criteria", ""]
    for name, ok, detail in prereg.criteria_status(ev):
        lines.append(f"- [{'x' if ok else ' '}] {name}: {detail}")
    lines += ["", "## Implementation-check backtest (reference only, not a selection step)", "",
              f"- {ev.get('backtest_start', '?')} → {ev.get('backtest_end', '?')}: CAGR {_pct(ev.get('backtest_cagr'))}, max drawdown {_pct(ev.get('backtest_max_dd'))}, "
              f"vol {_pct(ev.get('backtest_vol'))}; 60/40 CAGR {_pct(ev.get('backtest_bench_cagr'))}, max drawdown {_pct(ev.get('backtest_bench_max_dd'))}",
              f"- Monthly excess vs 60/40 {_pct(ev.get('backtest_excess_monthly_mean'))} ± {_pct(ev.get('backtest_excess_monthly_se'))}, PSR {ev.get('backtest_psr', math.nan):.2f}", "",
              f"Data: {len(tr)} trading days, {len(tr.columns)} symbols, newest close {tr.index.max() if len(tr) else 'none'}."]
    return "\n".join(lines) + "\n"


def summary_line(sig: pd.DataFrame, ev: dict, at: datetime) -> str:
    latest = sig[sig["date"] == sig["date"].max()]
    held = ", ".join(f"{r['symbol']} {r['weight']:.0%}" for _, r in latest[latest["weight"] > 0].sort_values("weight", ascending=False).iterrows())
    on = "risk-on" if bool(latest["canary_on"].iloc[0]) else "RISK-OFF"
    fw = f"NAV ${ev['forward_nav']:,.0f} ({_pct(ev['forward_cagr'])} CAGR, dd {_pct(ev['forward_max_dd'])})" if ev["forward_months"] else "no fills yet"
    return f"taa {latest['date'].iloc[0]}: {on} → {held}. Paper: {fw}."


def run(at: datetime | None = None, post: bool = True, force_post: bool = False) -> Path:
    at = at or now()
    tr, sig = load()
    if sig.empty:
        raise RuntimeError("no signals: prices table is empty or too short")
    ev = evaluation(tr, sig)
    stamp = iso(at)
    T.SIGNALS.replace([dict(r, momentum=f"{r['momentum']:.6f}", weight=f"{r['weight']:.4f}", canary_on=int(r["canary_on"]), computed_at=stamp)
                       for r in sig.to_dict("records")])
    fills, nav = ev["_fills"], ev["_fw_nav"]
    T.LEDGER.replace([dict(r, computed_at=stamp) for r in fills.to_dict("records")])
    if not nav.empty:
        b = ev["_fw_bench"].set_index("date")["nav"].reindex(nav["date"]).to_numpy()
        s = ev["_fw_spy"].set_index("date")["nav"].reindex(nav["date"]).to_numpy()
        T.NAV.replace([dict(date=d, nav=f"{n:.2f}", cash=f"{c:.2f}", bench_6040=f"{bb:.2f}", spy=f"{ss:.2f}", computed_at=stamp)
                       for d, n, c, bb, ss in zip(nav["date"], nav["nav"], nav["cash"], b, s)])
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    text = render(tr, sig, ev, at)
    (REPORT_DIR / "latest.md").write_text(text)
    newest = tr.index.max()
    rebalanced_today = not fills.empty and fills["date"].max() == newest and newest == sig["date"].max() or False
    rebalanced_today = (not fills.empty) and fills["date"].max() == newest
    if rebalanced_today:
        (REPORT_DIR / f"{newest}.md").write_text(text)
    if post and (rebalanced_today or force_post):
        alerts.send(summary_line(sig, ev, at))
    return REPORT_DIR / "latest.md"

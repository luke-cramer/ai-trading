import math
from datetime import datetime, timezone

import numpy as np
import pandas as pd
import pytest

from harness.storage import Table
from strategies.carry import costs, ingest, prereg, signal
from strategies.carry import tables as T

UTC = timezone.utc


# ---------- harness.storage ----------

def test_table_dedupes_on_key_and_partitions_by_month(tmp_path):
    t = Table("s", "x", ["funding_time", "pid", "v"], key=["funding_time", "pid"], root=tmp_path)
    rows = [dict(funding_time="2026-09-04T09:00:00Z", pid="A", v="1"), dict(funding_time="2026-10-01T00:00:00Z", pid="A", v="2")]
    assert t.append(rows) == 2
    assert t.append(rows) == 0                                   # idempotent re-run
    assert t.append([dict(funding_time="2026-09-04T09:00:00Z", pid="A", v="9")]) == 0   # same key, later value ignored
    assert t.append([dict(funding_time="2026-09-04T09:00:00Z", pid="B", v="3")]) == 1
    assert sorted(p.name for p in (tmp_path / "s" / "x").glob("*.csv")) == ["2026-09.csv", "2026-10.csv"]
    df = t.read()
    assert len(df) == 3 and df.iloc[0]["v"] == "1"


def test_table_missing_columns_become_empty(tmp_path):
    t = Table("s", "y", ["date", "a", "b"], key=["date"], root=tmp_path)
    t.append([dict(date="2026-09-04", a=None)])
    df = t.read()
    assert df.iloc[0]["a"] == "" and df.iloc[0]["b"] == ""


# ---------- costs ----------

def test_round_trip_bps_scales_inversely_with_price():
    lo, hi = costs.round_trip(40_000, 1), costs.round_trip(80_000, 1)
    assert lo.fees_usd == hi.fees_usd == 2 * (costs.EXCHANGE_FEE_PER_SIDE + costs.BROKER_FEE_PER_SIDE)
    assert lo.bps == pytest.approx(2 * hi.bps, rel=0.05)


def test_drag_apr_components():
    p = 80_000
    perp = costs.round_trip(p, costs.PERP_SLIPPAGE_TICKS).bps / 1e4 * 365 / 90
    dated = costs.round_trip(p, costs.DATED_SLIPPAGE_TICKS).bps / 1e4 * 365 / 30
    assert costs.drag_apr(p) == pytest.approx(perp + dated)
    assert 0.015 < costs.drag_apr(p) < 0.025      # sanity: ~2% at $80k, documented in PREREG


# ---------- signal ----------

def _funding(hours, rate, idx=80_000.0, product=T.PERP_BTC, day="2026-09-04"):
    return [dict(funding_time=f"{day}T{h:02d}:00:00Z", product_id=product, funding_rate=str(rate), index_price=str(idx))
            for h in hours]


def test_funding_daily_annualizes_and_counts_hours():
    f = pd.DataFrame(_funding(range(24), 1e-5) + _funding(range(12), 2e-5, day="2026-09-05"), dtype=str)
    d = signal.funding_daily(f)
    assert list(d["date"]) == ["2026-09-04", "2026-09-05"]
    assert d.iloc[0]["funding_apr"] == pytest.approx(1e-5 * 24 * 365)
    assert d.iloc[0]["hours_observed"] == 24 and d.iloc[1]["hours_observed"] == 12


def test_basis_uses_front_month_with_min_days_to_expiry():
    hour = "2026-09-20T00:00:00Z"
    f = pd.DataFrame([dict(funding_time=hour, product_id=T.PERP_BTC, funding_rate="1e-5", index_price="80000")])
    dated = pd.DataFrame([
        dict(hour_time=hour, product_id="BIT-25SEP26-CDE", contract_expiry="2026-09-25T15:00:00Z", price="80100", mid="80100"),
        dict(hour_time=hour, product_id="BIT-30OCT26-CDE", contract_expiry="2026-10-30T16:00:00Z", price="80800", mid="80800"),
    ])
    bh = signal.basis_hourly(dated, f)
    assert len(bh) == 1
    assert bh.iloc[0]["product_id"] == "BIT-30OCT26-CDE"          # Sep has < 7 days left, so it rolls
    dte = (datetime(2026, 10, 30, 16, tzinfo=UTC) - datetime(2026, 9, 20, tzinfo=UTC)).total_seconds() / 86400
    assert bh.iloc[0]["basis_apr"] == pytest.approx(math.log(80800 / 80000) / (dte / 365))


def test_basis_skips_hours_without_index_or_price():
    hour = "2026-09-04T00:00:00Z"
    f = pd.DataFrame([dict(funding_time=hour, product_id=T.PERP_BTC, funding_rate="1e-5", index_price="80000")])
    dated = pd.DataFrame([dict(hour_time=hour, product_id="BIT-27NOV26-CDE", contract_expiry="2026-11-27T16:00:00Z", price="", mid="0")])
    assert signal.basis_hourly(dated, f).empty


def test_compute_daily_spread_and_costs():
    hours = range(24)
    f = pd.DataFrame(_funding(hours, 1e-5), dtype=str)
    dated = pd.DataFrame([dict(hour_time=r["funding_time"], product_id="BIT-30OCT26-CDE", contract_expiry="2026-10-30T16:00:00Z",
                               price="80400", mid="80400") for r in f.to_dict("records")])
    empty = pd.DataFrame()
    spot = pd.DataFrame(columns=T.SPOT.columns)
    daily = signal.compute_daily(f, dated, spot, pd.DataFrame(columns=T.CBOE.columns), pd.DataFrame(columns=T.TREASURY.columns),
                                 pd.DataFrame(columns=T.CME.columns), computed_at=datetime(2026, 9, 5, tzinfo=UTC))
    assert list(daily.columns) == T.DAILY.columns
    r = daily.iloc[0]
    fa, ba, drag = float(r["funding_apr"]), float(r["basis_apr"]), float(r["cost_drag_apr"])
    assert fa == pytest.approx(1e-5 * 24 * 365)
    assert float(r["spread_gross_apr"]) == pytest.approx(fa - ba, rel=1e-6)
    assert float(r["spread_net_apr"]) == pytest.approx(fa - ba - drag, rel=1e-6)
    assert drag == pytest.approx(costs.drag_apr(80_000))
    assert r["hours_observed"] == "24" and r["cboe_funding_apr"] == "" and r["rf_apr"] == ""


def test_cboe_daily_uses_final_print_of_trading_date():
    c = pd.DataFrame([
        dict(futures_root="PBT", trading_date="2026-09-03", sample_time="2026-09-02 17:01:04", clamped_funding_rate="0.0001"),
        dict(futures_root="PBT", trading_date="2026-09-03", sample_time="2026-09-03 15:00:04", clamped_funding_rate="0.0002"),
        dict(futures_root="PET", trading_date="2026-09-03", sample_time="2026-09-03 15:00:04", clamped_funding_rate="0.0009"),
    ])
    d = signal.cboe_daily(c)
    assert len(d) == 1 and d.iloc[0]["cboe_funding_apr"] == pytest.approx(0.0002 * 365)


def test_cme_expiry_is_last_friday():
    assert signal._cme_expiry("BTCU26.CME") == pd.Timestamp("2026-09-25T15:00Z")
    assert signal._cme_expiry("BTCZ26.CME") == pd.Timestamp("2026-12-25T15:00Z")


def test_cme_symbols_roll_year():
    syms = ingest.cme_symbols(datetime(2026, 11, 3, tzinfo=UTC), months_ahead=3)
    assert syms == ["BTC=F", "BTCX26.CME", "BTCZ26.CME", "BTCF27.CME"]


def test_rf_daily_forward_fills():
    t = pd.DataFrame([dict(date="2026-09-01", wk4="3.70"), dict(date="2026-09-03", wk4="3.80")])
    out = signal.rf_daily(t, pd.Series(["2026-09-02", "2026-09-04", "2026-08-30"]))
    m = dict(zip(out["date"], out["rf_apr"]))
    assert m["2026-09-02"] == pytest.approx(0.037) and m["2026-09-04"] == pytest.approx(0.038) and np.isnan(m["2026-08-30"])


# ---------- evaluation statistics ----------

def test_newey_west_matches_plain_se_for_iid_lag0():
    x = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
    m, se, t = signal.newey_west_mean(x, lags=0)
    assert m == 3.0 and se == pytest.approx(math.sqrt(2.0 / 5)) and t == pytest.approx(3.0 / se)


def test_newey_west_widens_se_for_autocorrelated_series():
    rng = np.random.default_rng(0)
    e = rng.standard_normal(2000)
    ar = np.zeros_like(e)
    for i in range(1, len(e)):
        ar[i] = 0.8 * ar[i - 1] + e[i]
    _, se0, _ = signal.newey_west_mean(ar, lags=0)
    _, se5, _ = signal.newey_west_mean(ar, lags=10)
    assert se5 > 1.5 * se0


def test_psr_bounds_and_direction():
    sr, psr = signal.probabilistic_sharpe(np.full(50, 0.01) + np.linspace(-1e-3, 1e-3, 50))
    assert sr > 5 and psr > 0.999
    _, psr_neg = signal.probabilistic_sharpe(np.linspace(-0.02, 0.0, 50))
    assert psr_neg < 0.01
    assert all(math.isnan(v) for v in signal.probabilistic_sharpe(np.array([1.0, 2.0])))


# ---------- pre-registered criteria ----------

def _ev(**kw):
    base = dict(days_complete=60, hours_observed=1440, hours_expected=1440, mean_net=0.03, ci_low=0.01, frac_positive=0.7)
    base.update(kw)
    return base


def test_criteria_go_and_kill_and_extend():
    assert prereg.criteria_status(_ev())[-1][2].startswith("GO")
    assert prereg.criteria_status(_ev(mean_net=0.01))[-1][2].startswith("KILL")
    assert prereg.criteria_status(_ev(ci_low=-0.001))[-1][2].startswith("KILL")
    assert prereg.criteria_status(_ev(frac_positive=0.5))[-1][2].startswith("KILL")
    assert prereg.criteria_status(_ev(hours_observed=1000))[-1][2].startswith("EXTEND")
    assert prereg.criteria_status(_ev(days_complete=90, hours_observed=1500, hours_expected=2160))[-1][2].startswith("GO")
    assert "keep measuring" in prereg.criteria_status(_ev(days_complete=10))[-1][2]


# ---------- ingest helpers ----------

def test_thin_cboe_keeps_first_of_hour_and_final_print():
    rows = [dict(futures_root="PBT", trading_date="d", sample_time=f"2026-09-03 {h:02d}:{m:02d}:04") for h in (10, 11) for m in (1, 2, 3)]
    rows.append(dict(futures_root="PBT", trading_date="d", sample_time="2026-09-03 15:00:04"))
    kept = [r["sample_time"] for r in ingest._thin_cboe(rows)]
    assert kept == ["2026-09-03 10:01:04", "2026-09-03 11:01:04", "2026-09-03 15:00:04"]


def test_numeric_normalization():
    assert ingest._f("81100") == "81100" and ingest._f("0.000012") == "1.2e-05" and ingest._f("") == "" and ingest._f(None) == ""
    assert float(ingest._f("1.2e-05")) == 1.2e-05

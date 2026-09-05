import json
from datetime import datetime, timezone

import numpy as np
import pandas as pd
import pytest

from strategies.taa import costs, ingest, paper, prereg, signal
from strategies.taa import tables as T

UTC = timezone.utc


def _prices(sym, closes, start="2020-01-01"):
    dates = pd.bdate_range(start, periods=len(closes)).strftime("%Y-%m-%d")
    return pd.DataFrame(dict(date=dates, symbol=sym, close=[str(c) for c in closes], volume="1", fetched_at="x"))


# ---------- total return ----------

def test_dividend_adjusts_history_backward_and_leaves_latest_untouched():
    p = _prices("A", [100, 100, 100, 100])
    ev = pd.DataFrame([dict(date=p["date"].iloc[2], symbol="A", kind="dividend", value="2", fetched_at="x")])
    tr = signal.total_return_prices(p, ev)["A"]
    assert tr.iloc[3] == 100 and tr.iloc[2] == 100
    assert tr.iloc[1] == pytest.approx(98) and tr.iloc[0] == pytest.approx(98)   # 1 - 2/100 applied to prior closes


def test_split_adjusts_prior_closes():
    p = _prices("A", [200, 200, 100, 100])
    ev = pd.DataFrame([dict(date=p["date"].iloc[2], symbol="A", kind="split", value="2", fetched_at="x")])
    tr = signal.total_return_prices(p, ev)["A"]
    assert list(tr.round(6)) == [100, 100, 100, 100]


# ---------- month-end and momentum ----------

def _monthly_frame(n_months, growth):
    dates = pd.bdate_range("2019-01-01", periods=n_months * 22)
    closes = 100 * (1 + growth) ** (np.arange(len(dates)) / 21)
    return pd.DataFrame({"A": closes}, index=dates.strftime("%Y-%m-%d"))


def test_month_end_drops_incomplete_newest_month():
    tr = _monthly_frame(3, 0.0)
    me = signal.month_end(tr)
    assert all(pd.to_datetime(me.index).is_month_end | (pd.to_datetime(me.index).day >= 28))
    assert me.index[-1][:7] != tr.index[-1][:7]


def test_momentum_13612u_is_mean_of_lag_returns():
    me = pd.DataFrame({"A": [100, 110, 121, 133.1, 146.41, 161.05, 177.16, 194.87, 214.36, 235.79, 259.37, 285.31, 313.84]})
    m = signal.momentum(me)["A"].iloc[-1]
    expected = np.mean([313.84 / me["A"].iloc[-1 - k] - 1 for k in (1, 3, 6, 12)])
    assert m == pytest.approx(expected)


# ---------- allocation rules ----------

def _mom(**kw):
    base = {s: 0.05 for s in T.UNIVERSE}
    base.update(kw)
    return pd.Series(base)


def test_risk_on_picks_top4_equal_weight():
    w, on = signal.allocate(_mom(SPY=0.5, IWM=0.4, VEA=0.3, VWO=0.2, TIP=0.01))
    assert on and w == {"SPY": 0.25, "IWM": 0.25, "VEA": 0.25, "VWO": 0.25}


def test_risk_on_replaces_nonpositive_with_best_defensive():
    w, on = signal.allocate(_mom(SPY=0.5, IWM=0.4, VEA=0.3, VWO=-0.01, VNQ=-0.2, DBC=-0.3, IEF=-0.5, TLT=-0.6, BIL=0.001, TIP=0.01))
    assert on and w == {"SPY": 0.25, "IWM": 0.25, "VEA": 0.25, "BIL": 0.25}


def test_risk_off_goes_fully_to_best_defensive():
    w, on = signal.allocate(_mom(TIP=-0.01, IEF=0.02, BIL=0.01))
    assert not on and w == {"IEF": 1.0}
    w, _ = signal.allocate(_mom(TIP=0.0, IEF=-0.02, BIL=0.01))
    assert w == {"BIL": 1.0}


def test_allocate_requires_canary_and_defensive():
    m = _mom().drop("TIP")
    assert signal.allocate(m) == ({}, False)


# ---------- paper simulation ----------

def _tr_two_assets():
    dates = pd.bdate_range("2024-01-01", periods=70).strftime("%Y-%m-%d")
    return pd.DataFrame({"A": np.linspace(100, 169, 70), "B": np.full(70, 50.0)}, index=dates)


def test_simulate_fills_next_day_and_charges_costs():
    tr = _tr_two_assets()
    sig_date = tr.index[10]
    sig = pd.DataFrame([dict(date=sig_date, symbol="A", weight=0.5), dict(date=sig_date, symbol="B", weight=0.5)])
    nav, fills = paper.simulate(tr, sig, 10_000, start=sig_date, one_way_bps=10)
    fill_date = tr.index[11]
    assert fills["date"].unique().tolist() == [fill_date]
    assert nav["date"].iloc[0] == fill_date
    assert fills["cost_usd"].sum() == pytest.approx(10_000 * 10 / 1e4, rel=1e-3)
    assert nav["cash"].iloc[0] >= 0                                     # no leverage, ever
    assert nav["nav"].iloc[0] == pytest.approx(10_000 - fills["cost_usd"].sum(), abs=0.05)
    pa = tr.loc[fill_date, "A"]
    a_ret = tr["A"].iloc[-1] / pa - 1
    assert nav["nav"].iloc[-1] == pytest.approx(nav["nav"].iloc[0] * (1 + 0.5 * a_ret), rel=1e-6)


def test_fixed_mix_spy_only_is_buy_and_hold_after_first_fill():
    tr = _tr_two_assets()
    nav = paper.fixed_mix(tr, {"A": 1.0}, 10_000, start=tr.index[0], one_way_bps=0)
    r_nav = nav["nav"].iloc[-1] / nav["nav"].iloc[0]
    r_px = tr.loc[nav["date"].iloc[-1], "A"] / tr.loc[nav["date"].iloc[0], "A"]
    assert r_nav == pytest.approx(r_px)


def test_trade_cost_zero_commission_bps_only():
    assert costs.trade_cost(10_000) == pytest.approx(5.0) and costs.trade_cost(-10_000) == pytest.approx(5.0) and costs.trade_cost(0) == 0


# ---------- ingest parsing ----------

def _chart(ts_close, divs=None, splits=None):
    body = {"chart": {"result": [{"timestamp": [t for t, _ in ts_close],
                                  "indicators": {"quote": [{"close": [c for _, c in ts_close], "volume": [1] * len(ts_close)}]},
                                  "events": {"dividends": divs or {}, "splits": splits or {}}}]}}
    return json.dumps(body).encode()


def test_parse_chart_drops_todays_bar_before_close_and_keeps_it_after():
    ts_yday, ts_today = 1725456600, 1725543000            # 2024-09-04 and 2024-09-05 09:30 New York
    body = _chart([(ts_yday, 100.0), (ts_today, 101.0)], divs={"x": {"amount": 0.5, "date": ts_yday}})
    before = datetime(2024, 9, 5, 15, 0, tzinfo=timezone.utc)   # 11:00 New York
    after = datetime(2024, 9, 5, 21, 0, tzinfo=timezone.utc)    # 17:00 New York
    p1, e1 = ingest.parse_chart(body, before, "SPY")
    p2, _ = ingest.parse_chart(body, after, "SPY")
    assert [r["date"] for r in p1] == ["2024-09-04"] and [r["date"] for r in p2] == ["2024-09-04", "2024-09-05"]
    assert e1 == [dict(date="2024-09-04", symbol="SPY", kind="dividend", value="0.500000", fetched_at=e1[0]["fetched_at"])]


def test_parse_tiingo_rows_and_events():
    body = json.dumps([
        dict(date="2024-09-04T00:00:00.000Z", close=100.0, volume=10, divCash=0.0, splitFactor=1.0),
        dict(date="2024-09-05T00:00:00.000Z", close=101.0, volume=11, divCash=0.25, splitFactor=1.0),
        dict(date="2024-09-06T00:00:00.000Z", close=50.0, volume=12, divCash=0.0, splitFactor=2.0),
    ]).encode()
    at = datetime(2024, 9, 6, 15, 0, tzinfo=timezone.utc)                 # 11:00 New York, session open: drop today's bar
    p, e = ingest.parse_tiingo(body, at, "SPY")
    assert [r["date"] for r in p] == ["2024-09-04", "2024-09-05"]
    assert [(r["kind"], r["value"]) for r in e] == [("dividend", "0.250000")]
    p2, e2 = ingest.parse_tiingo(body, datetime(2024, 9, 6, 22, 0, tzinfo=timezone.utc), "SPY")
    assert len(p2) == 3 and ("split", "2.000000") in [(r["kind"], r["value"]) for r in e2]


# ---------- criteria ----------

def test_criteria_verdicts():
    base = dict(forward_months=36, backtest_max_dd=-0.15, forward_max_dd=-0.10, forward_bench_max_dd=-0.20, forward_cagr_vs_6040=0.01)
    assert prereg.criteria_status(base)[-1][2].startswith("GO")
    assert prereg.criteria_status(base | dict(forward_max_dd=-0.25))[-1][2] == "KILL"
    assert prereg.criteria_status(base | dict(forward_cagr_vs_6040=-0.05, forward_max_dd=-0.25))[-1][2] == "KILL"
    assert prereg.criteria_status(base | dict(forward_cagr_vs_6040=-0.05, forward_bench_max_dd=-0.05, forward_max_dd=-0.1))[-1][2] == "KILL"
    assert "keep paper" in prereg.criteria_status(base | dict(forward_months=5))[-1][2]

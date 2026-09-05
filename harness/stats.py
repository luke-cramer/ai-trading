"""Evaluation statistics shared by every strategy (fixed in each PREREG.md)."""
from __future__ import annotations

import math

import numpy as np


def newey_west_mean(x: np.ndarray, lags: int = 5) -> tuple[float, float, float]:
    """Mean, HAC standard error (Bartlett kernel), t-stat. Handles autocorrelated return series."""
    x = np.asarray(x, dtype=float)
    x = x[~np.isnan(x)]
    n = len(x)
    if n < 2:
        return (float(x.mean()) if n else float("nan"), float("nan"), float("nan"))
    e = x - x.mean()
    s = float(e @ e) / n
    for k in range(1, min(lags, n - 1) + 1):
        w = 1 - k / (lags + 1)
        s += 2 * w * float(e[k:] @ e[:-k]) / n
    se = math.sqrt(max(s, 0.0) / n)
    m = float(x.mean())
    return m, se, (m / se if se > 0 else float("nan"))


def probabilistic_sharpe(x: np.ndarray, benchmark_sr: float = 0.0) -> tuple[float, float]:
    """Bailey & Lopez de Prado PSR per-period. With one pre-registered trial the deflated SR equals PSR."""
    x = np.asarray(x, dtype=float)
    x = x[~np.isnan(x)]
    n = len(x)
    if n < 3 or x.std(ddof=1) == 0:
        return float("nan"), float("nan")
    sr = x.mean() / x.std(ddof=1)
    z = (x - x.mean()) / x.std(ddof=1)
    skew = float((z**3).mean())
    kurt = float((z**4).mean())
    denom = math.sqrt(max(1 - skew * sr + (kurt - 1) / 4 * sr**2, 1e-12))
    stat = (sr - benchmark_sr) * math.sqrt(n - 1) / denom
    return float(sr), float(0.5 * (1 + math.erf(stat / math.sqrt(2))))


def cagr(nav: np.ndarray, periods_per_year: float) -> float:
    nav = np.asarray(nav, dtype=float)
    if len(nav) < 2 or nav[0] <= 0:
        return float("nan")
    return float((nav[-1] / nav[0]) ** (periods_per_year / (len(nav) - 1)) - 1)


def max_drawdown(nav: np.ndarray) -> float:
    nav = np.asarray(nav, dtype=float)
    if len(nav) == 0:
        return float("nan")
    peak = np.maximum.accumulate(nav)
    return float(((nav - peak) / peak).min())

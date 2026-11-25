"""Small, dependency-light metrics used by the preregistered experiments."""
from __future__ import annotations

import numpy as np


def portfolio_returns(weights: np.ndarray, asset_returns: np.ndarray, cost_bps: float = 0.0):
    """Return gross, net, and turnover with a flat initial portfolio."""
    w = np.asarray(weights, dtype=float)
    r = np.asarray(asset_returns, dtype=float)
    if w.shape != r.shape or w.ndim != 2:
        raise ValueError("weights and asset_returns must have the same 2-D shape")
    turnover = np.abs(np.diff(np.vstack([np.zeros((1, w.shape[1])), w]), axis=0)).sum(axis=1)
    gross = np.sum(w * r, axis=1)
    net = gross - cost_bps * 1e-4 * turnover
    return gross, net, turnover


def sharpe(x: np.ndarray, annualization: float = 252.0) -> float:
    x = np.asarray(x, dtype=float)
    if x.size < 2 or not np.isfinite(x).all() or np.std(x, ddof=1) == 0:
        return float("nan")
    return float(np.sqrt(annualization) * np.mean(x) / np.std(x, ddof=1))


def circular_block_bootstrap_delta(a: np.ndarray, b: np.ndarray, block: int = 20, draws: int = 2000, seed: int = 20261125):
    """Bootstrap mean Sharpe difference using paired circular blocks."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    if a.shape != b.shape or a.ndim != 1 or block < 1:
        raise ValueError("paired one-dimensional returns and positive block required")
    rng = np.random.default_rng(seed)
    n = len(a)
    out = np.empty(draws)
    for j in range(draws):
        idx = []
        while len(idx) < n:
            start = int(rng.integers(0, n))
            idx.extend((start + np.arange(block)) % n)
        ii = np.asarray(idx[:n])
        out[j] = sharpe(a[ii]) - sharpe(b[ii])
    return float(np.quantile(out, 0.025)), float(np.quantile(out, 0.975)), out

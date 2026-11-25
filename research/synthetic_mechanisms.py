"""Mechanism-only synthetic panels; never use these as financial evidence."""
from __future__ import annotations

import numpy as np


def make_panel(kind: str, seed: int = 7, t: int = 756, assets: int = 4):
    if kind not in {"trend_flip", "variance_only", "no_change"}:
        raise ValueError(kind)
    rng = np.random.default_rng(seed)
    r = rng.normal(0.0, 0.01, size=(t, assets))
    cp = t // 2
    if kind == "trend_flip":
        r[:cp] += 0.0005
        r[cp:] -= 0.0005
    elif kind == "variance_only":
        r[cp:] *= 2.0
    # score_t uses only the prefix ending at t-1; the first observation is neutral.
    score = np.zeros(t)
    score[1:] = np.mean(np.abs(r[1:] - r[:-1]), axis=1)
    return r, score, cp


def causal_momentum(r: np.ndarray, lookback: int = 21):
    signal = np.zeros_like(r)
    for t in range(lookback, len(r)):
        signal[t] = np.sign(np.mean(r[t - lookback:t], axis=0)) / r.shape[1]
    return signal


def gated_signal(r: np.ndarray, score: np.ndarray, threshold: float):
    w = causal_momentum(r)
    return np.where(score[:, None] >= threshold, w, 0.0)

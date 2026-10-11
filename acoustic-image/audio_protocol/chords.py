"""Espacio de 2^24 = 16.777.216 acordes: 6 voces × 16 tonos (f = 1000 + 1000·voz + 50·tono Hz)."""
from __future__ import annotations

import numpy as np

VOICES, TONES, STATES = 6, 16, 16 ** 6


def to_tones(v: int):
    return [(v >> (20 - 4 * j)) & 15 for j in range(VOICES)]


def freqs(v: int):
    return [1000.0 + 1000.0 * j + 50.0 * t for j, t in enumerate(to_tones(v))]


def synth(v: int, sr: int, dur: float) -> np.ndarray:
    n = int(round(sr * dur))
    t = np.arange(n) / sr
    x = sum(np.sin(2 * np.pi * f * t) for f in freqs(v)) / VOICES
    k = n // 10
    env = np.ones(n)
    env[:k], env[-k:] = np.linspace(0, 1, k), np.linspace(1, 0, k)
    return x * env


def analyze(window: np.ndarray, sr: int) -> int:
    w = np.asarray(window, float) * np.hanning(len(window))
    n = 4 * len(w)
    spec = np.abs(np.fft.rfft(w, n))
    df = sr / n
    v = 0
    for j in range(VOICES):
        mags = [spec[int(round((1000.0 + 1000.0 * j + 50.0 * k) / df))] for k in range(TONES)]
        v = (v << 4) | int(np.argmax(mags))
    return v

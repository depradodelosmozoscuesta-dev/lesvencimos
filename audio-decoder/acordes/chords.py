"""Espacio de 24 bits (16.777.216 acordes) y análisis espectral.

Un acorde = 6 voces (una por banda de 1 kHz), 16 tonos por voz => 16^6 = 2^24.
Mismo plan de frecuencias que audio-imagen/codec.js: f = 1000 + voz*1000 + tono*50 Hz.
"""
from __future__ import annotations

import numpy as np

VOICES, TONES = 6, 16
BASE_HZ, BAND_HZ, STEP_HZ = 1000.0, 1000.0, 50.0
STATES = TONES ** VOICES  # 16_777_216


def to_tones(value: int) -> tuple[int, ...]:
    """Valor de 24 bits -> 6 tonos (nibbles, voz 0 = más significativo)."""
    if not 0 <= value < STATES:
        raise ValueError("el acorde debe estar en 0..16777215")
    return tuple((value >> (20 - 4 * j)) & 15 for j in range(VOICES))


def to_value(tones) -> int:
    v = 0
    for t in tones:
        v = (v << 4) | int(t)
    return v


def freq(voice: int, tone: int) -> float:
    return BASE_HZ + voice * BAND_HZ + tone * STEP_HZ


def freq_vector(value: int) -> np.ndarray:
    """Vector de frecuencias del acorde (Hz)."""
    return np.array([freq(v, t) for v, t in enumerate(to_tones(value))])


def normalized_vector(value: int) -> np.ndarray:
    """Vector de frecuencias normalizado a 0..1 (equivalente a un RGB de 24 bits)."""
    return np.array(to_tones(value), dtype=float) / (TONES - 1)


def synth_chord(value: int, sr: int, dur: float, fade: float = 0.1) -> np.ndarray:
    n = int(round(sr * dur))
    t = np.arange(n) / sr
    x = sum(np.sin(2 * np.pi * f * t) for f in freq_vector(value)) / VOICES
    k = int(n * fade)
    if k:
        env = np.ones(n)
        env[:k] = np.linspace(0, 1, k)
        env[-k:] = np.linspace(1, 0, k)
        x = x * env
    return x


def analyze_chord(window: np.ndarray, sr: int) -> int:
    """Identifica el acorde (0..2^24-1) de una ventana de audio."""
    w = np.asarray(window, dtype=float)
    w = w * np.hanning(len(w))
    n = 1 << (len(w) - 1).bit_length()
    n = max(n, 4 * len(w))  # zero-padding: interpolación espectral
    spec = np.abs(np.fft.rfft(w, n))
    df = sr / n
    tones = []
    for v in range(VOICES):
        mags = [spec[int(round(freq(v, k) / df))] for k in range(TONES)]
        tones.append(int(np.argmax(mags)))
    return to_value(tones)

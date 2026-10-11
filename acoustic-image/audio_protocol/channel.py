"""Canal acústico simulado: ráfagas -> audio (silencio = delimitador) -> ráfagas."""
from __future__ import annotations

import numpy as np

from . import chords


def to_audio(bursts, sr=44100, sym_dur=0.03, silence=0.05, noise=0.0, seed=0) -> np.ndarray:
    gap = np.zeros(int(sr * silence))
    parts = [gap]
    for b in bursts:
        parts += [chords.synth(c, sr, sym_dur) for c in b] + [gap]
    x = np.concatenate(parts)
    return x + np.random.default_rng(seed).normal(0, noise, len(x)) if noise else x


def from_audio(x, sr=44100, sym_dur=0.03, silence=0.05, threshold=0.1) -> list[list[int]]:
    """Separa ráfagas por silencios (RMS bajo umbral), cuenta elementos y analiza cada acorde en orden."""
    frame = int(sr * 0.005)
    n = len(x) // frame
    rms = np.sqrt((np.asarray(x[: n * frame]).reshape(n, frame) ** 2).mean(axis=1))
    active = rms > threshold * rms.max()
    min_gap = max(1, int(round(silence * 0.6 / 0.005)))
    spans, start, last = [], None, None
    for i, a in enumerate(active):
        if not a:
            continue
        if start is None:
            start = i
        elif i - last > min_gap:
            spans.append((start, last + 1))
            start = i
        last = i
    if start is not None:
        spans.append((start, last + 1))
    out = []
    for s, e in spans:
        s, e = s * frame, e * frame
        k = max(1, int(round((e - s) / (sym_dur * sr))))  # nº de elementos entre silencios
        slot = (e - s) / k
        out.append([chords.analyze(x[int(s + i * slot + 0.2 * slot):int(s + (i + 1) * slot - 0.2 * slot)], sr)
                    for i in range(k)])
    return out

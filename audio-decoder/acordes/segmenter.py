"""Segmentación por silencios: el silencio delimita ráfagas (bloques)."""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .chords import analyze_chord


@dataclass
class Block:
    start: float          # s
    end: float            # s
    chords: list[int]     # acordes en orden de llegada

    @property
    def length(self) -> int:  # k = nº de elementos entre dos silencios
        return len(self.chords)


def find_bursts(x, sr, frame=0.005, threshold=0.1, min_silence=0.03, min_burst=0.02):
    """Devuelve [(inicio_s, fin_s)] de tramos con señal.

    threshold: fracción del pico RMS bajo la cual el frame es silencio.
    min_silence: duración mínima de silencio para cortar un bloque.
    """
    x = np.asarray(x, dtype=float)
    f = max(1, int(sr * frame))
    n = len(x) // f
    if n == 0:
        return []
    rms = np.sqrt((x[: n * f].reshape(n, f) ** 2).mean(axis=1))
    peak = rms.max()
    if peak <= 0:
        return []
    active = rms > threshold * peak
    gap = max(1, int(round(min_silence / frame)))
    bursts, start, last = [], None, None
    for i, a in enumerate(active):
        if a:
            if start is None:
                start = i
            elif i - last > gap:  # silencio suficiente: cierra el bloque anterior
                bursts.append((start, last + 1))
                start = i
            last = i
    if start is not None:
        bursts.append((start, last + 1))
    return [(s * frame, e * frame) for s, e in bursts if (e - s) * frame >= min_burst]


def segment(x, sr, sym_dur=0.06, **kw) -> list[Block]:
    """Segmenta, cuenta elementos por bloque (k) y decodifica cada acorde en orden."""
    x = np.asarray(x, dtype=float)
    blocks = []
    for s, e in find_bursts(x, sr, **kw):
        k = max(1, int(round((e - s) / sym_dur)))
        # reparte la ráfaga en k ranuras iguales (se usa su parte central, sin fundidos)
        slot = (e - s) / k
        chords = []
        for i in range(k):
            a = int((s + i * slot + 0.2 * slot) * sr)
            b = int((s + (i + 1) * slot - 0.2 * slot) * sr)
            chords.append(analyze_chord(x[a:b], sr))
        blocks.append(Block(s, e, chords))
    return blocks

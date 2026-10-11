"""Entrada de audio: archivo WAV o micrófono (opcional, requiere sounddevice)."""
from __future__ import annotations

import numpy as np
from scipy.io import wavfile

from .chords import synth_chord


def read_wav(path):
    sr, x = wavfile.read(path)
    if x.ndim > 1:
        x = x.mean(axis=1)
    if np.issubdtype(x.dtype, np.integer):
        x = x / np.iinfo(x.dtype).max
    return sr, x.astype(float)


def write_wav(path, x, sr):
    wavfile.write(path, sr, (np.clip(x, -1, 1) * 32767).astype(np.int16))


def record(seconds, sr=44100):
    try:
        import sounddevice as sd
    except ImportError as e:  # pragma: no cover
        raise SystemExit("Para el micrófono instala: pip install sounddevice") from e
    x = sd.rec(int(seconds * sr), samplerate=sr, channels=1, dtype="float32")
    sd.wait()
    return sr, x[:, 0].astype(float)


def simulate(blocks, sr=44100, sym_dur=0.06, silence=0.15, noise=0.0, seed=0):
    """Genera audio de prueba: lista de bloques (listas de acordes) separados por silencio."""
    gap = np.zeros(int(sr * silence))
    parts = [gap]
    for b in blocks:
        parts += [synth_chord(c, sr, sym_dur) for c in b] + [gap]
    x = np.concatenate(parts)
    if noise:
        x = x + np.random.default_rng(seed).normal(0, noise, len(x))
    return x

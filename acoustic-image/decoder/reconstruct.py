"""Reconstructor: aplica gradientes y capas de color acumulativas sobre el lienzo."""
from __future__ import annotations

import numpy as np
from PIL import Image

from audio_protocol import varint
from encoder import gradient
from encoder.peeling import MAGIC


def reconstruct(stream: bytes) -> Image.Image:
    if stream[:2] != MAGIC:
        raise ValueError("flujo de imagen inválido")
    r = varint.Reader(stream)
    r.i = 2
    w, h, block, ngrad = r.get(), r.get(), r.get(), r.get()
    canvas = np.zeros((h, w, 3), np.uint8)
    covered = np.zeros((h, w), bool)
    for _ in range(ngrad):
        bx, by = r.get(), r.get()
        params = [r.get_signed() for _ in range(9)]
        y0, x0 = by * block, bx * block
        bw, bh = min(block, w - x0), min(block, h - y0)
        canvas[y0:y0 + bh, x0:x0 + bw] = gradient.render(params, bw, bh)
        covered[y0:y0 + bh, x0:x0 + bw] = True
    free = np.flatnonzero(~covered.ravel())          # píxeles sin resolver (orden de lectura)
    flat = canvas.reshape(-1, 3)
    nlayers = r.get()
    for i in range(nlayers):
        color = bytes(r.byte() for _ in range(3))
        if i == nlayers - 1:
            flat[free] = np.frombuffer(color, np.uint8)
            break
        runs = [r.get() for _ in range(r.get())]
        mask = np.zeros(len(free), bool)
        pos, val = 0, False
        for n in runs:
            mask[pos:pos + n] = val
            pos, val = pos + n, not val
        flat[free[mask]] = np.frombuffer(color, np.uint8)
        free = free[~mask]
    return Image.fromarray(flat.reshape(h, w, 3))

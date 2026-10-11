"""Color Peeling: color dominante -> máscara sí/no -> se retiran los píxeles resueltos -> repetir."""
from __future__ import annotations

import numpy as np
from PIL import Image

from audio_protocol import varint
from . import gradient

MAGIC = b"CP"


def _reduce(pixels: np.ndarray, max_colors: int) -> np.ndarray:
    """Si hay más colores que capas permitidas, cuantiza (con pérdida) a una paleta adaptativa."""
    if len(np.unique(pixels, axis=0)) <= max_colors:
        return pixels
    im = Image.fromarray(pixels.reshape(1, -1, 3).astype(np.uint8)).quantize(max_colors, dither=Image.Dither.NONE)
    pal = np.array(im.getpalette()[: 3 * max_colors], dtype=np.uint8).reshape(-1, 3)
    return pal[np.array(im)].reshape(-1, 3)


def peel(pixels: np.ndarray):
    """pixels (n,3). Devuelve [(color, mask|None)]: mask sobre los píxeles aún sin resolver."""
    layers, remaining = [], pixels
    while len(remaining):
        colors, counts = np.unique(remaining, axis=0, return_counts=True)
        color = colors[counts.argmax()]
        mask = (remaining == color).all(axis=1)
        if mask.all():
            layers.append((tuple(int(v) for v in color), None))  # última capa: no necesita máscara
            break
        layers.append((tuple(int(v) for v in color), mask))
        remaining = remaining[~mask]
    return layers


def _rle(mask: np.ndarray) -> list[int]:
    """Longitudes alternas empezando por 'no' (puede ser 0)."""
    runs, cur, n = [], False, 0
    for v in mask:
        if bool(v) == cur:
            n += 1
        else:
            runs.append(n)
            cur, n = bool(v), 1
    runs.append(n)
    return runs


def compress(img: Image.Image, block: int = 8, tol: int = 1, max_layers: int = 64):
    """Imagen -> (stream bytes, info). Gradientes primero; el resto por capas de color."""
    a = np.asarray(img.convert("RGB"))
    h, w, _ = a.shape
    grads = gradient.detect(a, block, tol)
    covered = np.zeros((h, w), bool)
    for (bx, by) in grads:
        covered[by * block:(by + 1) * block, bx * block:(bx + 1) * block] = True
    rest = _reduce(a[~covered], max_colors=max_layers) if (~covered).any() else a[~covered]
    layers = peel(rest) if len(rest) else []

    out = bytearray(MAGIC)
    for v in (w, h, block, len(grads)):
        varint.put(out, v)
    for (bx, by), params in sorted(grads.items(), key=lambda kv: (kv[0][1], kv[0][0])):
        varint.put(out, bx), varint.put(out, by)
        for p in params:
            varint.put_signed(out, p)
    varint.put(out, len(layers))
    stats = []
    for color, mask in layers:
        out += bytes(color)
        if mask is not None:
            runs = _rle(mask)
            varint.put(out, len(runs))
            for r in runs:
                varint.put(out, r)
        stats.append({"rgb": color, "pixels": int(mask.sum()) if mask is not None else None,
                      "runs": None if mask is None else len(_rle(mask))})
    return bytes(out), {"gradient_blocks": len(grads), "layers": stats, "raw_bytes": w * h * 3}

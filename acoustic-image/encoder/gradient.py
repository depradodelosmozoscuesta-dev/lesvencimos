"""Detección de gradientes: bloques que se deducen con un plano c = base + dx·x + dy·y por canal."""
from __future__ import annotations

import numpy as np

SCALE = 256  # precisión de punto fijo de base y pendientes


def render(params, bw: int, bh: int) -> np.ndarray:
    """params = 6 enteros (base, dx, dy) × 3 canales en 1/SCALE. Devuelve (bh, bw, 3) uint8."""
    ys, xs = np.mgrid[0:bh, 0:bw]
    out = np.empty((bh, bw, 3))
    for c in range(3):
        base, dx, dy = params[3 * c: 3 * c + 3]
        out[..., c] = (base + dx * xs + dy * ys) / SCALE
    return np.clip(np.rint(out), 0, 255).astype(np.uint8)


def fit_block(block: np.ndarray, tol: int, min_colors: int = 4):
    """Ajusta un plano por mínimos cuadrados. Devuelve params o None si no cumple la tolerancia."""
    bh, bw, _ = block.shape
    if bw < 2 or bh < 2:
        return None
    if len({tuple(p) for p in block.reshape(-1, 3)}) < min_colors:
        return None  # lisos o casi lisos: los resuelve el pelado de color
    ys, xs = np.mgrid[0:bh, 0:bw]
    a = np.stack([np.ones(bw * bh), xs.ravel(), ys.ravel()], axis=1)
    params = []
    for c in range(3):
        sol = np.linalg.lstsq(a, block[..., c].ravel().astype(float), rcond=None)[0]
        params += [int(round(v * SCALE)) for v in sol]
    err = np.abs(render(params, bw, bh).astype(int) - block.astype(int)).max()
    return params if err <= tol else None


def detect(img: np.ndarray, block: int = 8, tol: int = 1) -> dict[tuple[int, int], list[int]]:
    """{(bx, by): params} para cada bloque que es un gradiente."""
    h, w, _ = img.shape
    found = {}
    for by in range(0, h, block):
        for bx in range(0, w, block):
            p = fit_block(img[by:by + block, bx:bx + block], tol)
            if p is not None:
                found[(bx // block, by // block)] = p
    return found

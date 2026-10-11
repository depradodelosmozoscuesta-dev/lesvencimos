"""End-to-end: imagen de prueba -> capas+gradientes -> ráfagas -> audio simulado -> decodificar -> reconstruir."""
from __future__ import annotations

import sys

import numpy as np
from PIL import Image, ImageDraw

from audio_protocol import bursts as B, channel
from decoder.reconstruct import reconstruct
from encoder.peeling import compress


def test_image(w=48, h=32) -> Image.Image:
    xs = np.linspace(0, 1, w)
    a = np.zeros((h, w, 3), np.uint8)
    a[:] = (20, 30, 60)                                   # fondo (color dominante)
    a[:, :, 0] = (60 + 190 * xs)[None, :]                 # luz lateral: gradiente horizontal
    a[:, :, 1] = (40 + 150 * xs)[None, :]
    a[:, :, 2] = (20 + 80 * xs)[None, :]
    im = Image.fromarray(a)
    d = ImageDraw.Draw(im)
    d.rectangle([4, 20, 20, 28], fill=(200, 30, 30))      # figuras planas (capas de color)
    d.ellipse([28, 18, 42, 30], fill=(30, 160, 60))
    return im


def run(img: Image.Image, audio=True, tol=1, verbose=True):
    stream, info = compress(img, tol=tol)
    bursts = B.encode(stream)
    if audio:
        x = channel.to_audio(bursts, noise=0.01)
        bursts = channel.from_audio(x)
        secs = len(x) / 44100
    else:
        secs = None
    out = reconstruct(B.decode(bursts))
    err = int(np.abs(np.asarray(out, int) - np.asarray(img.convert("RGB"), int)).max())
    if verbose:
        print(f"imagen {img.width}x{img.height}: {info['raw_bytes']} B crudos -> {len(stream)} B, "
              f"{len(bursts)} ráfagas, {info['gradient_blocks']} bloques de gradiente, {len(info['layers'])} capas"
              + (f", {secs:.1f} s de audio" if secs else "") + f", error máx. {err}")
    return out, err


if __name__ == "__main__":
    img = Image.open(sys.argv[1]) if len(sys.argv) > 1 else test_image()
    out, err = run(img)
    out.save("/tmp/reconstruida.png")
    sys.exit(0 if err <= 1 else 1)

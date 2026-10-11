"""CLI: python -m acordes.cli decode archivo.wav | mic SEGUNDOS | demo"""
from __future__ import annotations

import argparse

from . import audio_io
from .router import Router, describe
from .segmenter import segment


def demo_router() -> Router:
    r = Router()
    A, B, C = 0x123456, 0xABCDEF, 0x00FF00
    r.on_set([A, B], lambda d: "ENCENDER" if d.order_rank == 0 else "APAGAR")
    r.on_sequence([C, C, C], "ALARMA")
    r.on_length(1, lambda d: f"TONO_SIMPLE {d.chords[0]:06X}")
    return r


def run(sr, x, router, sym_dur):
    for i, b in enumerate(segment(x, sr, sym_dur=sym_dur)):
        d = describe(b)
        print(f"bloque {i}: t={b.start:.2f}-{b.end:.2f}s k={d.length} "
              f"orden={d.order_rank}/{d.order_count} acordes={[f'{c:06X}' for c in d.chords]} "
              f"-> {router.resolve(b)}")


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)
    for n in ("decode", "mic", "demo"):
        s = sub.add_parser(n)
        s.add_argument("--sym-dur", type=float, default=0.06)
        if n == "decode":
            s.add_argument("wav")
        if n == "mic":
            s.add_argument("seconds", type=float)
    a = p.parse_args(argv)
    router = demo_router()
    if a.cmd == "decode":
        sr, x = audio_io.read_wav(a.wav)
    elif a.cmd == "mic":
        sr, x = audio_io.record(a.seconds)
    else:
        sr = 44100
        x = audio_io.simulate([[0x123456, 0xABCDEF], [0xABCDEF, 0x123456], [0x00FF00] * 3, [0x0F0F0F]], sr, a.sym_dur)
    run(sr, x, router, a.sym_dur)


if __name__ == "__main__":
    main()

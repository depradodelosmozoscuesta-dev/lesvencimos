import itertools
import random
import unittest

from acordes import audio_io
from acordes.chords import STATES, analyze_chord, synth_chord, to_tones, to_value
from acordes.cli import demo_router
from acordes.permutation import permutations_count, rank, unrank
from acordes.segmenter import segment

SR = 44100
A, B, C = 0x123456, 0xABCDEF, 0x00FF00


class Tests(unittest.TestCase):
    def test_space(self):
        self.assertEqual(STATES, 16_777_216)
        for v in (0, 1, 0xFFFFFF, 0x123456):
            self.assertEqual(to_value(to_tones(v)), v)

    def test_chord_identification(self):
        rnd = random.Random(1)
        for v in [0, 0xFFFFFF] + [rnd.randrange(STATES) for _ in range(30)]:
            self.assertEqual(analyze_chord(synth_chord(v, SR, 0.06)[600:-600], SR), v)

    def test_permutation_rank(self):
        items = [5, 9, 2, 7]
        ranks = sorted(rank(p) for p in itertools.permutations(items))
        self.assertEqual(ranks, list(range(24)))
        for p in itertools.permutations(items):
            self.assertEqual(tuple(unrank(items, rank(p))), p)
        self.assertEqual(permutations_count([1, 1, 2]), 3)
        self.assertEqual(sorted(rank(p) for p in set(itertools.permutations([1, 1, 2]))), [0, 1, 2])

    def test_segmentation_and_order(self):
        x = audio_io.simulate([[A, B], [B, A], [C, C, C], [0x0F0F0F]], SR, noise=0.01)
        blocks = segment(x, SR)
        self.assertEqual([b.chords for b in blocks], [[A, B], [B, A], [C, C, C], [0x0F0F0F]])
        self.assertEqual([b.length for b in blocks], [2, 2, 3, 1])

    def test_router(self):
        x = audio_io.simulate([[A, B], [B, A], [C, C, C], [0x0F0F0F], [A, B, C]], SR, noise=0.01)
        r = demo_router()
        out = [r.resolve(b) for b in segment(x, SR)]
        self.assertEqual(out[:4], ["ENCENDER", "APAGAR", "ALARMA", "TONO_SIMPLE 0F0F0F"])
        self.assertEqual(out[4][0], "desconocido")


if __name__ == "__main__":
    unittest.main()

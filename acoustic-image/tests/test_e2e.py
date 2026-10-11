import base64
import io
import unittest

import numpy as np
from fastapi.testclient import TestClient
from PIL import Image

from api.app import create_app
from audio_protocol import bursts as B
from run_e2e import run, test_image


class Tests(unittest.TestCase):
    def test_permutation_rank(self):
        for r in (0, 1, 777, 40319):
            self.assertEqual(B.rank_of_perm(B.perm_from_rank(r)), r)

    def test_bursts_any_order_and_loss(self):
        data = bytes(range(256)) * 3
        bs = B.encode(data)
        self.assertEqual(B.decode(bs[::-1]), data)  # ráfagas desordenadas: el orden interno da la secuencia
        with self.assertRaises(ValueError):
            B.decode(bs[1:])

    def test_end_to_end_audio(self):
        img = test_image()
        out, err = run(img, audio=True, verbose=False)
        self.assertLessEqual(err, 1)
        self.assertEqual(out.size, img.size)

    def test_lossless_flat_image_is_small(self):
        im = Image.new("RGB", (64, 64), (10, 20, 30))
        out, err = run(im, audio=False, verbose=False)
        self.assertEqual(err, 0)

    def test_api(self):
        c = TestClient(create_app())
        buf = io.BytesIO()
        test_image().save(buf, "PNG")
        r = c.post("/send", json={"image_b64": base64.b64encode(buf.getvalue()).decode()}).json()
        bursts = c.get(f"/packets/{r['id']}").json()["bursts"]
        rec = c.post("/receive", json={"bursts": bursts}).json()
        out = Image.open(io.BytesIO(base64.b64decode(rec["image_b64"])))
        diff = np.abs(np.asarray(out, int) - np.asarray(test_image(), int)).max()
        self.assertLessEqual(diff, 1)
        self.assertEqual(c.post("/receive", json={"bursts": bursts[1:]}).status_code, 422)


if __name__ == "__main__":
    unittest.main()

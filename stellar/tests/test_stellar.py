import unittest
from datetime import datetime, timezone

from stellar.astro import coords
from stellar.catalog import loader
from stellar.catalog.repo import Repo
from stellar.engine import crypto
from stellar.engine.state_machine import StateMachine
from stellar.seed import build_demo
from stellar.sensors.fusion import OrientationFilter, altaz_from_vectors
from stellar.vision.calibrate import Calibration
from stellar.vision.star_detect import detect_stars

FAST = 1000


class CoordsTest(unittest.TestCase):
    def test_roundtrip(self):
        lst = coords.local_sidereal_time(datetime(2026, 1, 1, 22, tzinfo=timezone.utc), -4.7)
        ra, dec = coords.altaz_to_radec(40, 120, 41.6, lst)
        alt, az = coords.radec_to_altaz(ra, dec, 41.6, lst)
        self.assertAlmostEqual(alt, 40, 4)
        self.assertAlmostEqual(az, 120, 4)

    def test_lst_j2000(self):
        self.assertAlmostEqual(coords.local_sidereal_time(
            datetime(2000, 1, 1, 12, tzinfo=timezone.utc), 0), 280.46, 1)

    def test_polaris_alt_is_lat(self):
        alt, _ = coords.radec_to_altaz(0, 90, 41.6, 123.0)
        self.assertAlmostEqual(alt, 41.6, 4)

    def test_separation(self):
        self.assertAlmostEqual(coords.angular_separation(0, 0, 90, 0), 90, 6)


class CatalogTest(unittest.TestCase):
    def test_counts(self):
        con = loader.connect()
        loader.create_schema(con)
        loader.load_catalog(con)
        self.assertGreaterEqual(con.execute("SELECT COUNT(*) FROM star").fetchone()[0], 100)
        self.assertEqual(con.execute("SELECT COUNT(*) FROM star WHERE role='CONTROL'").fetchone()[0], 20)

    def test_edge_requires_option(self):
        con, _, _ = build_demo(iterations=FAST)
        sid = con.execute("SELECT id FROM star WHERE role='CONTROL'").fetchone()[0]
        import sqlite3
        with self.assertRaises(sqlite3.DatabaseError):
            con.execute("INSERT INTO menu_edge VALUES(1,?,2)", (sid,))


class FusionTest(unittest.TestCase):
    def test_looking_north_horizon(self):
        # móvil vertical, cámara al horizonte: up=+y; campo hacia el norte = -z (cámara)
        alt, az = altaz_from_vectors((0, 1, 0), (0, 0, -1))
        self.assertAlmostEqual(alt, 0, 5)
        self.assertAlmostEqual(az, 0, 5)

    def test_filter(self):
        f = OrientationFilter()
        alt, az = f.update((0, 1, 0), (0, 0, -1), (0, 0, 0), 0.02)
        self.assertAlmostEqual(alt, 0, 5)


class VisionTest(unittest.TestCase):
    def test_detect_and_calibrate(self):
        img = [[10] * 20 for _ in range(20)]
        img[5][7] = 255
        img[12][3] = 200
        s = detect_stars(img)
        self.assertEqual((round(s[0]["x"]), round(s[0]["y"])), (7, 5))
        c = Calibration.from_reference(10, 350, 12, 5)
        self.assertEqual(c.apply(10, 350), (12, 5.0))


class EngineTest(unittest.TestCase):
    def test_crypto(self):
        n, ct = crypto.encrypt([1, 2], b"x", b"s", FAST)
        self.assertEqual(crypto.decrypt([1, 2], n, ct, b"s", FAST), b"x")
        self.assertIsNone(crypto.decrypt([2, 1], n, ct, b"s", FAST))

    def _run(self, names):
        con, ev, seq = build_demo(iterations=FAST)
        repo = Repo(con)
        sm = StateMachine(repo, ev)
        t = 0.0
        for n in names(repo, seq):
            s = repo.star_by_name(n) if isinstance(n, str) else repo.star(n)
            for _ in range(3):
                sm.feed(s["ra_deg"] + 0.5, s["dec_deg"], t)
                t += 0.8
        return sm

    def test_correct_sequence_reveals(self):
        sm = self._run(lambda r, seq: list(seq) + ["Sirius"])
        self.assertEqual(sm.revealed["data"].decode(), "¿Quieres casarte conmigo?")

    def test_wrong_sequence_neutral(self):
        sm = self._run(lambda r, seq: list(reversed(seq)) + ["Sirius"])
        self.assertIsNone(sm.revealed)
        self.assertEqual(sm.buffer, [])
        self.assertEqual(sm.message, "Secuencia no reconocida")

    def test_dwell_required(self):
        con, ev, seq = build_demo(iterations=FAST)
        repo = Repo(con)
        sm = StateMachine(repo, ev)
        s = repo.star(seq[0])
        self.assertIsNone(sm.feed(s["ra_deg"], s["dec_deg"], 0))
        self.assertIsNone(sm.feed(s["ra_deg"], s["dec_deg"], 0.5))
        self.assertIsNotNone(sm.feed(s["ra_deg"], s["dec_deg"], 1.6))


if __name__ == "__main__":
    unittest.main()

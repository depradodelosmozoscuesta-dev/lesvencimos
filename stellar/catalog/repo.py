"""Consultas de solo lectura sobre la BD."""
from stellar.astro.coords import angular_separation


class Repo:
    def __init__(self, con):
        self.con = con
        self._stars = [dict(r) for r in con.execute("SELECT * FROM star")]
        self._by_id = {s["id"]: s for s in self._stars}

    def star(self, star_id):
        return self._by_id[star_id]

    def star_by_name(self, name):
        return next(s for s in self._stars if s["name"] == name)

    def nearest(self, ra, dec, tolerance_deg=4.0):
        """Estrella del catálogo más cercana dentro de la tolerancia (snap), o None."""
        best, best_d = None, tolerance_deg
        for s in self._stars:
            d = angular_separation(ra, dec, s["ra_deg"], s["dec_deg"])
            if d <= best_d:
                best, best_d = s, d
        return best

    def node(self, node_id):
        r = self.con.execute("SELECT * FROM menu_node WHERE id=?", (node_id,)).fetchone()
        return dict(r) if r else None

    def next_node(self, node_id, star_id):
        r = self.con.execute(
            "SELECT next_node FROM menu_edge WHERE node_id=? AND star_id=?",
            (node_id, star_id)).fetchone()
        return r[0] if r else None

    def candidates(self, node_id):
        """Estrellas que son ramas válidas desde el nodo (para resaltar en la guía)."""
        return [dict(r) for r in self.con.execute(
            "SELECT s.* FROM menu_edge e JOIN star s ON s.id=e.star_id WHERE e.node_id=?",
            (node_id,))]

"""Máquina de estados: puntería -> snap a estrella -> dwell -> comando u opción."""
from stellar.astro.coords import angular_separation

ROOT = 1


class StateMachine:
    def __init__(self, repo, evaluator, tolerance_deg=4.0, dwell_s=1.5):
        self.repo, self.evaluator = repo, evaluator
        self.tolerance, self.dwell = tolerance_deg, dwell_s
        self.node_id = ROOT
        self.buffer = []
        self.revealed = None
        self.message = ""
        self._target = None
        self._since = None
        self._fired = False

    def feed(self, ra, dec, t):
        """Procesa una lectura de puntería; devuelve la estrella activada o None."""
        star = self.repo.nearest(ra, dec, self.tolerance)
        if star is None or self._target is None or star["id"] != self._target["id"]:
            self._target, self._since, self._fired = star, t, False
            return None
        if self._fired or t - self._since < self.dwell:
            return None
        self._fired = True
        self._activate(star)
        return star

    def _activate(self, star):
        self.message = ""
        if star["role"] == "CONTROL":
            self._command(star["command"])
            return
        nxt = self.repo.next_node(self.node_id, star["id"])
        if nxt is not None:
            self.node_id = nxt
        self.buffer.append(star["id"])

    def _command(self, cmd):
        if cmd == "BACK":
            node = self.repo.node(self.node_id)
            if node and node["parent_id"]:
                self.node_id = node["parent_id"]
            if self.buffer:
                self.buffer.pop()
        elif cmd == "DELETE":
            if self.buffer:
                self.buffer.pop()
        elif cmd in ("HOME", "CANCEL", "CLEAR", "MENU"):
            self.node_id = ROOT
            self.buffer.clear()
        elif cmd == "CONFIRM":
            result = self.evaluator.evaluate(self.buffer)
            if result:
                self.revealed = result
            else:
                self.message = "Secuencia no reconocida"  # feedback neutro
            self.buffer.clear()
            self.node_id = ROOT

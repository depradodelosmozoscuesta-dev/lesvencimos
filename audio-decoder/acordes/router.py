"""Bloques semánticos: (acordes, longitud, orden) -> orden/estado/acción."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from .permutation import permutations_count, rank
from .segmenter import Block


@dataclass(frozen=True)
class Decoded:
    chords: tuple[int, ...]     # orden exacto de llegada
    length: int                 # k
    order_rank: int             # rango de la permutación
    order_count: int            # nº de órdenes posibles (k! si no hay repetidos)
    key: tuple[int, ...]        # acordes ordenados (conjunto del bloque)


def describe(block: Block) -> Decoded:
    c = tuple(block.chords)
    return Decoded(c, len(c), rank(c), permutations_count(c), tuple(sorted(c)))


class Router:
    """Tabla de enrutamiento extensible.

    Reglas, de más a menos específica:
      1. exacta: (acordes en orden de llegada)
      2. por conjunto + rango:  (conjunto ordenado, rango)
      3. por conjunto:          (conjunto ordenado)  -> la acción recibe el rango como metadato
      4. por longitud k
      5. por defecto
    """

    def __init__(self):
        self.exact, self.by_rank, self.by_set, self.by_len = {}, {}, {}, {}
        self.default: Callable[[Decoded], object] = lambda d: ("desconocido", d.chords)

    @staticmethod
    def _as(action):
        return action if callable(action) else (lambda d, a=action: a)

    def on_sequence(self, chords, action):
        self.exact[tuple(chords)] = self._as(action)

    def on_set(self, chords, action, rank_=None):
        key = tuple(sorted(chords))
        if rank_ is None:
            self.by_set[key] = self._as(action)
        else:
            self.by_rank[(key, rank_)] = self._as(action)

    def on_length(self, k, action):
        self.by_len[k] = self._as(action)

    def resolve(self, block: Block):
        d = describe(block)
        for table, key in ((self.exact, d.chords), (self.by_rank, (d.key, d.order_rank)),
                           (self.by_set, d.key), (self.by_len, d.length)):
            if key in table:
                return table[key](d)
        return self.default(d)

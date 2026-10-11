"""Orden de llegada dentro de un bloque: rango de la permutación (hasta k! valores)."""
from __future__ import annotations

from collections import Counter
from math import factorial


def permutations_count(chords) -> int:
    """Nº de órdenes distintos posibles (k! / prod(m_i!) para acordes repetidos)."""
    n = factorial(len(chords))
    for m in Counter(chords).values():
        n //= factorial(m)
    return n


def rank(chords) -> int:
    """Rango lexicográfico (0..) del orden de llegada respecto al orden canónico (ascendente)."""
    items = list(chords)
    cnt = Counter(items)
    r = 0
    for i, c in enumerate(items):
        remaining = len(items) - i
        for smaller in sorted(x for x in cnt if x < c and cnt[x] > 0):
            cnt[smaller] -= 1
            r += _multinomial(cnt, remaining - 1)
            cnt[smaller] += 1
        cnt[c] -= 1
    return r


def unrank(multiset, r: int) -> list[int]:
    """Inversa de `rank`: reconstruye el orden a partir del conjunto de acordes y su rango."""
    cnt = Counter(multiset)
    total = sum(cnt.values())
    if not 0 <= r < _multinomial(cnt, total):
        raise ValueError("rango fuera de rango")
    out = []
    for i in range(total):
        for c in sorted(x for x in cnt if cnt[x] > 0):
            cnt[c] -= 1
            n = _multinomial(cnt, total - i - 1)
            if r < n:
                out.append(c)
                break
            r -= n
            cnt[c] += 1
    return out


def _multinomial(cnt, n) -> int:
    v = factorial(n)
    for m in cnt.values():
        v //= factorial(m)
    return v

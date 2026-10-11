"""Bytes <-> ráfagas de acordes.

Ráfaga = K=8 acordes de 24 bits. Cada acorde = 3 bits de ranura + 21 bits de datos (168 bits = 21 bytes).
El ORDEN de llegada es una permutación de las 8 ranuras: su rango (0..8!-1, 15 bits utilizables) lleva
el nº de secuencia de la ráfaga sin gastar ancho de banda adicional. Las ranuras permiten al receptor
recuperar los datos aunque el orden de llegada sea distinto del de lectura.
"""
from __future__ import annotations

import zlib
from math import factorial

K = 8
DATA_BITS = 21
BYTES_PER_BURST = K * DATA_BITS // 8  # 21
MAX_SEQ = 1 << 15


def perm_from_rank(r: int, n: int = K) -> list[int]:
    items, out = list(range(n)), []
    for i in range(n, 0, -1):
        f = factorial(i - 1)
        out.append(items.pop(r // f))
        r %= f
    return out


def rank_of_perm(p: list[int]) -> int:
    items, r = sorted(p), 0
    for i, v in enumerate(p):
        j = items.index(v)
        r += j * factorial(len(p) - 1 - i)
        items.pop(j)
    return r


def encode(payload: bytes) -> list[list[int]]:
    """payload -> lista de ráfagas (cada una, 8 acordes en orden de emisión). Añade longitud y CRC32."""
    body = len(payload).to_bytes(4, "big") + payload
    body += zlib.crc32(body).to_bytes(4, "big")
    body += bytes(-len(body) % BYTES_PER_BURST)
    n = len(body) // BYTES_PER_BURST
    if n > MAX_SEQ:
        raise ValueError(f"mensaje demasiado grande: {n} ráfagas (máx. {MAX_SEQ})")
    bursts = []
    for s in range(n):
        v = int.from_bytes(body[s * BYTES_PER_BURST:(s + 1) * BYTES_PER_BURST], "big")
        slots = [(i << DATA_BITS) | ((v >> (DATA_BITS * (K - 1 - i))) & ((1 << DATA_BITS) - 1)) for i in range(K)]
        bursts.append([slots[i] for i in perm_from_rank(s)])
    return bursts


def decode(bursts: list[list[int]]) -> bytes:
    """ráfagas -> payload. Ordena por nº de secuencia (permutación) y verifica longitud y CRC."""
    parts = {}
    for b in bursts:
        if len(b) != K:
            raise ValueError(f"ráfaga con {len(b)} elementos (se esperaban {K})")
        order = [c >> DATA_BITS for c in b]
        if sorted(order) != list(range(K)):
            raise ValueError("ráfaga con ranuras repetidas o ausentes")
        by_slot = {c >> DATA_BITS: c & ((1 << DATA_BITS) - 1) for c in b}
        v = 0
        for i in range(K):
            v = (v << DATA_BITS) | by_slot[i]
        parts[rank_of_perm(order)] = v.to_bytes(BYTES_PER_BURST, "big")
    if sorted(parts) != list(range(len(parts))) or not parts:
        raise ValueError("faltan ráfagas (secuencia no contigua)")
    body = b"".join(parts[i] for i in sorted(parts))
    n = int.from_bytes(body[:4], "big")
    if 8 + n > len(body):
        raise ValueError("mensaje truncado")
    if zlib.crc32(body[:4 + n]).to_bytes(4, "big") != body[4 + n:8 + n]:
        raise ValueError("CRC incorrecto")
    return body[4:4 + n]

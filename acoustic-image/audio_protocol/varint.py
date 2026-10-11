"""Enteros de longitud variable (LEB128) y zigzag para enteros con signo."""


def put(out: bytearray, n: int) -> None:
    while True:
        b = n & 0x7F
        n >>= 7
        out.append(b | (0x80 if n else 0))
        if not n:
            return


def put_signed(out: bytearray, n: int) -> None:
    put(out, (n << 1) ^ (n >> 63) if n < 0 else n << 1)


class Reader:
    def __init__(self, data: bytes):
        self.d, self.i = data, 0

    def byte(self) -> int:
        b = self.d[self.i]
        self.i += 1
        return b

    def get(self) -> int:
        n = shift = 0
        while True:
            b = self.byte()
            n |= (b & 0x7F) << shift
            if not b & 0x80:
                return n
            shift += 7

    def get_signed(self) -> int:
        z = self.get()
        return (z >> 1) ^ -(z & 1)

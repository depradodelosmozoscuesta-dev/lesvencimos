"""Fusión acelerómetro + magnetómetro + giroscopio (filtro complementario).

Marco del dispositivo: x derecha, y arriba de la pantalla, z sale de la pantalla;
la cámara trasera apunta a -z. Se siguen los vectores 'arriba' y 'campo magnético'
en el marco del dispositivo.
"""
import math


def _norm(v):
    n = math.sqrt(sum(c * c for c in v))
    if n == 0:
        raise ValueError("vector nulo")
    return tuple(c / n for c in v)


def _cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def _dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def _rotate(v, w, dt):
    """Rota v por la velocidad angular w (rad/s) del dispositivo durante dt: v' = v - (w x v) dt."""
    c = _cross(w, v)
    return tuple(v[i] - c[i] * dt for i in range(3))


def altaz_from_vectors(up, mag, axis=(0.0, 0.0, -1.0)):
    """Altitud y azimut (respecto al norte magnético) del eje dado."""
    up = _norm(up)
    east = _norm(_cross(mag, up))
    north = _cross(up, east)
    alt = math.degrees(math.asin(max(-1.0, min(1.0, _dot(axis, up)))))
    az = math.degrees(math.atan2(_dot(axis, east), _dot(axis, north))) % 360.0
    return alt, az


class OrientationFilter:
    def __init__(self, alpha=0.98, declination_deg=0.0):
        self.alpha = alpha
        self.declination = declination_deg
        self.up = None
        self.mag = None

    def update(self, accel, mag, gyro=None, dt=0.0):
        accel, mag = _norm(accel), _norm(mag)
        if self.up is None:
            self.up, self.mag = accel, mag
        else:
            if gyro is not None and dt > 0:
                self.up = _rotate(self.up, gyro, dt)
                self.mag = _rotate(self.mag, gyro, dt)
            a = self.alpha
            self.up = _norm(tuple(a * s + (1 - a) * m for s, m in zip(self.up, accel)))
            self.mag = _norm(tuple(a * s + (1 - a) * m for s, m in zip(self.mag, mag)))
        return self.altaz()

    def altaz(self, axis=(0.0, 0.0, -1.0)):
        alt, az = altaz_from_vectors(self.up, self.mag, axis)
        return alt, (az + self.declination) % 360.0

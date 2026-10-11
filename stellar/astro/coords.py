"""Conversiones Alt/Az <-> RA/Dec, tiempo sidéreo y distancia angular. Ángulos en grados."""
import math
from datetime import datetime, timezone


def julian_date(dt):
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    dt = dt.astimezone(timezone.utc)
    y, m = dt.year, dt.month
    if m <= 2:
        y, m = y - 1, m + 12
    a = y // 100
    b = 2 - a + a // 4
    day = dt.day + (dt.hour + (dt.minute + (dt.second + dt.microsecond / 1e6) / 60) / 60) / 24
    return int(365.25 * (y + 4716)) + int(30.6001 * (m + 1)) + day + b - 1524.5


def local_sidereal_time(dt, lon_deg):
    """LST en grados (lon positiva al este)."""
    d = julian_date(dt) - 2451545.0
    gmst = 280.46061837 + 360.98564736629 * d
    return (gmst + lon_deg) % 360.0


def altaz_to_radec(alt, az, lat, lst):
    a, A, p = map(math.radians, (alt, az, lat))
    sin_dec = math.sin(p) * math.sin(a) + math.cos(p) * math.cos(a) * math.cos(A)
    dec = math.asin(max(-1.0, min(1.0, sin_dec)))
    H = math.atan2(-math.sin(A) * math.cos(a),
                   math.sin(a) * math.cos(p) - math.cos(a) * math.sin(p) * math.cos(A))
    ra = (lst - math.degrees(H)) % 360.0
    return ra, math.degrees(dec)


def radec_to_altaz(ra, dec, lat, lst):
    H = math.radians(lst - ra)
    d, p = math.radians(dec), math.radians(lat)
    sin_alt = math.sin(p) * math.sin(d) + math.cos(p) * math.cos(d) * math.cos(H)
    alt = math.asin(max(-1.0, min(1.0, sin_alt)))
    az = math.atan2(-math.cos(d) * math.sin(H),
                    math.sin(d) * math.cos(p) - math.cos(d) * math.sin(p) * math.cos(H))
    return math.degrees(alt), math.degrees(az) % 360.0


def angular_separation(ra1, dec1, ra2, dec2):
    r1, d1, r2, d2 = map(math.radians, (ra1, dec1, ra2, dec2))
    s = math.sin(d1) * math.sin(d2) + math.cos(d1) * math.cos(d2) * math.cos(r1 - r2)
    return math.degrees(math.acos(max(-1.0, min(1.0, s))))

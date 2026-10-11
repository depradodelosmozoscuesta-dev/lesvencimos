"""Abstracción de la fuente de orientación/cámara (el hardware real se inyecta)."""
from stellar.astro.coords import altaz_to_radec, local_sidereal_time


class PointingSource:
    """Convierte lecturas de sensores en (RA, Dec) aproximados de la cámara."""

    def __init__(self, orientation_filter, lat, lon, calibration=None):
        self.filter = orientation_filter
        self.lat, self.lon = lat, lon
        self.calibration = calibration

    def pointing(self, accel, mag, when, gyro=None, dt=0.0):
        alt, az = self.filter.update(accel, mag, gyro, dt)
        if self.calibration:
            alt, az = self.calibration.apply(alt, az)
        return altaz_to_radec(alt, az, self.lat, local_sidereal_time(when, self.lon))

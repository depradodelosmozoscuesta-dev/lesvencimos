"""Calibración manual de un punto: corrige el offset de azimut/altitud de los sensores."""


class Calibration:
    def __init__(self, d_alt=0.0, d_az=0.0):
        self.d_alt, self.d_az = d_alt, d_az

    @classmethod
    def from_reference(cls, measured_alt, measured_az, true_alt, true_az):
        d_az = (true_az - measured_az + 180.0) % 360.0 - 180.0
        return cls(true_alt - measured_alt, d_az)

    def apply(self, alt, az):
        return max(-90.0, min(90.0, alt + self.d_alt)), (az + self.d_az) % 360.0

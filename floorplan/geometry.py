import math


def orientation(p, q):
    """Angle of p->q in degrees, measured CCW from +x, in [0, 360)."""
    return math.degrees(math.atan2(q[1] - p[1], q[0] - p[0])) % 360


def distance(p, q):
    return math.hypot(q[0] - p[0], q[1] - p[1])

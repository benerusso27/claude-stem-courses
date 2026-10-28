"""Lab 2 physics in Python (SI base units). Independent re-implementation of the closed forms used by
lab02_simulation.html, plus helpers for the sample-data generator.

Members are linear elastic bars: elongation e = F L/(E A) + alpha dT L (Beer 8e Sec. 2.1G, 2.3).
Internal forces are tension-positive (Beer). Loads applied to the caps in the parallel configuration
are given as a compressive magnitude P (as on a press).
"""
import math


def area_circle(d):
    return math.pi * d * d / 4


def area_tube(do, di):
    return math.pi * (do * do - di * di) / 4


# ----------------------------------------------------------------------------- parallel members
def parallel(P, dT, m1, m2, g, contact=True, L2=None):
    """Two members between rigid caps.
    m = dict(E, A, L, alpha). Member 2 is shorter than member 1 by g (g < 0: longer, i.e. interference).
    P: compressive load on the caps (N, >= 0 pushes the caps together). contact=True: member 2 can only
    carry compression (rod in a tube on a press); contact=False: both ends attached (bolt and sleeve).
    Returns (F1, F2, cap displacement of member-1 end relative to its free length), tension positive."""
    k1 = m1["E"] * m1["A"] / m1["L"]
    L2 = m1["L"] - g if L2 is None else L2     # bonded joints: the page uses L2 = L (interference << L)
    k2 = m2["E"] * m2["A"] / L2
    # bonded solution: F1 + F2 = -P;  e1 - e2 = L2 - L1 = -g
    d_alpha = m1["alpha"] * m1["L"] - m2["alpha"] * L2
    F1 = (-g - dT * d_alpha - P / k2) / (1 / k1 + 1 / k2)
    F2 = -P - F1
    if contact and F2 > 0:          # member 2 would be in tension: it lifts off
        F1, F2 = -P, 0.0
    e1 = F1 / k1 + m1["alpha"] * dT * m1["L"]
    return F1, F2, e1


def gap_closing_load(m1, g):
    """Compressive load at which member 1 (alone) has shortened by the gap g."""
    return m1["E"] * m1["A"] / m1["L"] * g


def share_after_contact(m1, m2):
    """Fraction of additional load carried by member 2 once both carry load (equal lengths)."""
    a1, a2 = m1["E"] * m1["A"], m2["E"] * m2["A"]
    return a2 / (a1 + a2)


def thermal_clamp_force_per_degree(m_bolt, m_sleeve):
    """Change of bolt tension per kelvin for a bolt clamping a sleeve of equal length."""
    L = m_bolt["L"]
    return (m_sleeve["alpha"] - m_bolt["alpha"]) * L / (L / (m_bolt["E"] * m_bolt["A"]) + L / (m_sleeve["E"] * m_sleeve["A"]))


# ----------------------------------------------------------------------------- series bar
def flex_taper(L, E, da, db):
    """Flexibility L/(E A_eff) of a conical segment: integral dx/(E pi d(x)^2/4) = 4L/(pi E da db)."""
    return 4 * L / (math.pi * E * da * db)


def series(PB, dT, s1, s2, support="fixed", g=0.0):
    """Two segments, fixed at x = 0. Segment 1 may taper (d from da to db), segment 2 prismatic.
    PB: load at the junction, +x positive. support: 'fixed', 'free' or 'gap' (gap g to a rigid wall).
    Returns R (force of the right wall on the bar, positive toward -x), N1, N2 (tension +), delta_free."""
    f1 = flex_taper(s1["L"], s1["E"], s1["da"], s1["db"])
    f2 = s2["L"] / (s2["E"] * area_circle(s2["d"]))
    th = dT * (s1["alpha"] * s1["L"] + s2["alpha"] * s2["L"])
    delta_free = PB * f1 + th            # elongation of the whole bar with the right end free
    if support == "free":
        R = 0.0
    elif support == "fixed":
        R = delta_free / (f1 + f2)
    else:
        R = max(0.0, (delta_free - g) / (f1 + f2))
    return R, PB - R, -R, delta_free


def thermal_buckling_dT(d, L, alpha):
    """Temperature rise that buckles a solid round bar fixed at both ends (effective length L/2)."""
    r = d / 4
    return math.pi ** 2 * r * r / (alpha * (0.5 * L) ** 2)

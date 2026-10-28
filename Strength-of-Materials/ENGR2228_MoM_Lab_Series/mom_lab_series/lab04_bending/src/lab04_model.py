"""Lab 4 physics in Python (SI base units). Independent re-implementation of the closed forms used by
lab04_simulation.html, plus adaptive-quadrature section integrals for the generator and the tests.

Beer 8e conventions: tension positive; V and M as in Fig. 5.6 (M > 0 sags); w > 0 downward;
sigma_x = -M y / I with y upward from the neutral axis; curvature kappa > 0 for sagging.
"""
import math

from scipy import integrate, optimize


# ----------------------------------------------------------------------------- materials (uniaxial, odd in strain)
def sigma_of(m, e):
    s = -1.0 if e < 0 else 1.0
    a = abs(e)
    law = m["law"]
    if law == "epp":
        return s * min(m["E"] * a, m["sY"])
    if law == "ro":
        if a == 0:
            return 0.0
        f = lambda t: t / m["E"] + 0.002 * (t / m["sY"]) ** m["m"] - a  # noqa: E731
        hi = min(m["E"] * a, m["sY"] * (a / 0.002) ** (1 / m["m"]))
        return s * optimize.brentq(f, 0.0, hi * (1 + 1e-12), xtol=1e-12 * hi + 1e-30, rtol=1e-15, maxiter=500)
    if law == "plateau":
        eY = m["sY"] / m["E"]
        if a <= eY:
            return s * m["E"] * a
        if a <= m["eL"]:
            return s * m["sY"]
        return s * m["K"] * (a - m["eL"] + (m["sY"] / m["K"]) ** (1 / m["n"])) ** m["n"]
    raise ValueError(law)


# ----------------------------------------------------------------------------- beams (statics by direct formulas)
def four_point(P, L, a, x):
    """Simply supported span L, two loads P/2 at a and L - a. Returns (V, M) at x (left limits at loads)."""
    R = P / 2
    if x <= a:
        return R, R * x
    if x <= L - a:
        return 0.0, R * a
    return -R, R * (L - x)


def cantilever_triangle(w0, L, x):
    """Cantilever fixed at x = 0, load rising linearly from 0 at the wall to w0 at the free end x = L.
    Uses the right free body: V(x) = load to the right; M(x) = -(moment of that load about x)."""
    def w(t):
        return w0 * t / L
    F = integrate.quad(w, x, L, epsabs=0, epsrel=1e-13)[0]
    Mo = integrate.quad(lambda t: w(t) * (t - x), x, L, epsabs=0, epsrel=1e-13)[0]
    return F, -Mo


# ----------------------------------------------------------------------------- sections
def rect_props(b, h):
    I = b * h ** 3 / 12
    return dict(I=I, S=I / (h / 2), Z=b * h * h / 4, A=b * h)


def ibeam_props(bf, h, tf, tw):
    hw = h - 2 * tf
    I = bf * h ** 3 / 12 - (bf - tw) * hw ** 3 / 12
    Z = bf * tf * (h - tf) + tw * hw ** 2 / 4
    return dict(I=I, S=I / (h / 2), Z=Z)


def composite_props(b, h, ts, E1, E2):
    """Main rectangle b x h (modulus E1) on top of a strip b x ts (modulus E2). y from the bottom. Transformed to E1."""
    n = E2 / E1
    A1, y1 = b * h, ts + h / 2
    A2, y2 = n * b * ts, ts / 2
    ybar = (A1 * y1 + A2 * y2) / (A1 + A2)
    I = b * h ** 3 / 12 + A1 * (y1 - ybar) ** 2 + n * b * ts ** 3 / 12 + A2 * (y2 - ybar) ** 2
    return dict(ybar=ybar, I=I, n=n)


def epp_rect_M(b, h, E, sY, kappa):
    c = h / 2
    MY = sY * b * h * h / 6
    kY = sY / (E * c)
    if kappa <= kY:
        return MY * kappa / kY
    return 1.5 * MY * (1 - (kY / kappa) ** 2 / 3)


def section_moment(layers, mats, kappa):
    """Adaptive-quadrature M and neutral axis for a layered section at curvature kappa.
    layers: [(y0, y1, b, matname)], y from the bottom. Returns (M, yNA)."""
    H = max(l[1] for l in layers)

    def force(yNA):
        tot = 0.0
        for y0, y1, b, mn in layers:
            tot += b * integrate.quad(lambda y: sigma_of(mats[mn], -kappa * (y - yNA)), y0, y1,
                                      points=[yNA] if y0 < yNA < y1 else None, epsabs=0, epsrel=1e-12, limit=200)[0]
        return tot
    yNA = optimize.brentq(force, -H, 2 * H, xtol=1e-15 * H, rtol=1e-15, maxiter=500)
    M = 0.0
    for y0, y1, b, mn in layers:
        M -= b * integrate.quad(lambda y: (y - yNA) * sigma_of(mats[mn], -kappa * (y - yNA)), y0, y1,
                                points=[yNA] if y0 < yNA < y1 else None, epsabs=0, epsrel=1e-12, limit=200)[0]
    return M, yNA

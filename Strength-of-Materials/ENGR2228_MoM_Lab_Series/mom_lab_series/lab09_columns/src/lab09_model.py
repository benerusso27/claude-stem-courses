"""Lab 9 physics in Python (SI base units: N, m, Pa). Independent re-implementation of what lab09_simulation.html
computes, by different methods wherever possible:
  * closed forms: Euler's formula with effective lengths (Beer Eqs. 10.11, 10.13, Fig. 10.18), the characteristic
    equations of columns whose ends are rotational springs (derived in the handout's Appendix D), the imperfect and
    eccentric pinned column (Eqs. 10.26-10.36 plus a half-sine initial bow), the elastica of a pinned column
    (scipy elliptic integrals), the tangent- and reduced-modulus column curves for a Ramberg-Osgood material, and
    the Aluminum Association design formulas for 6061-T6 (Eqs. 10.43b-10.45b);
  * numerical: generalized eigenvalues of a Hermite-cubic finite-element model (scipy.linalg.eigh), the same model
    loaded with an initial bow and end eccentricities, a second-order finite-difference beam-column, a collocation
    BVP for the elastica (scipy solve_bvp), and a fiber-section model of the imperfect inelastic column
    (the page uses inverse iteration, RK4 shooting and its own fiber loop).

Beer 8e column conventions (Sec. 10.1A, Figs. 10.7, 10.20-10.23): x runs along the column from end A, y is the lateral
deflection; P is the compressive load, reported as a positive magnitude; EI y'' = M with M = -P y for the centric
column and M = -P (y + e) for a load applied at distance e from the axis. The column bows to +y, away from the load
line, so the lever arm at mid-length is e + y_max (Fig. 10.23). An initial bow y0(x) = delta0 sin(pi x / L) is
measured in the same +y direction, and the dial gage reads the CHANGE of deflection from the no-load reading.
Strains: tension positive; the +y face ("front") is the convex side.
"""
import math

import numpy as np
from scipy import integrate, linalg, optimize, special

PI = math.pi
Z_FP = 4.493409457909064                 # root of tan z = z (Beer Eq. 10.20)
K_FACTORS = {"free-fixed": 2.0, "pinned": 1.0, "fixed-pinned": PI / Z_FP, "fixed-fixed": 0.5}


# ----------------------------------------------------------------------------- sections
def rect(b, t):
    """Rectangle b (wide) x t (thin); buckling about the weak axis (bending in the t direction)."""
    A = b * t
    I = b * t ** 3 / 12
    return dict(A=A, I=I, r=math.sqrt(I / A), c=t / 2)


def tube(Do, tw):
    Di = Do - 2 * tw
    A = PI * (Do ** 2 - Di ** 2) / 4
    I = PI * (Do ** 4 - Di ** 4) / 64
    return dict(A=A, I=I, r=math.sqrt(I / A), c=Do / 2, Di=Di)


# ----------------------------------------------------------------------------- Euler and effective length
def euler(E, I, Le):
    return PI ** 2 * E * I / Le ** 2                    # Eq. 10.11b


def sigma_cr(E, slender):
    return PI ** 2 * E / slender ** 2                   # Eq. 10.13b


def spring_both(EI, L, k):
    """Both ends laterally held, each a rotational spring k (symmetric mode): tan(x) = -2 x EI / (k L), x = pL/2 in
    (pi/2, pi). k = 0 gives pinned ends, k -> inf fixed ends. Returns P_cr and K = Le / L."""
    if k <= 0:
        return PI ** 2 * EI / L ** 2, 1.0
    if math.isinf(k):
        return 4 * PI ** 2 * EI / L ** 2, 0.5
    g = 2 * EI / (k * L)
    x = optimize.brentq(lambda x_: math.sin(x_) + g * x_ * math.cos(x_), PI / 2, PI, xtol=1e-15)
    P = 4 * x ** 2 * EI / L ** 2
    return P, PI / (2 * x)


def spring_pin(EI, L, k):
    """One end a rotational spring k, the other pinned, both laterally held: tan z = z / (1 + z^2 EI/(k L)), z = pL in
    (pi, 4.4934). Returns P_cr and K."""
    if k <= 0:
        return PI ** 2 * EI / L ** 2, 1.0
    if math.isinf(k):
        return Z_FP ** 2 * EI / L ** 2, PI / Z_FP
    g = EI / (k * L)
    f = lambda z: math.sin(z) * (1 + z * z * g) - z * math.cos(z)     # noqa: E731  (zero <=> characteristic eq.)
    z = optimize.brentq(f, PI + 1e-12, Z_FP, xtol=1e-15)
    return z ** 2 * EI / L ** 2, PI / z


def k_from_sym(EI, L, P):
    """Invert spring_both: the rotational stiffness of each end that makes the symmetric mode buckle at P."""
    x = L / 2 * math.sqrt(P / EI)
    return -2 * x * EI / (L * math.tan(x))


# ----------------------------------------------------------------------------- imperfect and eccentric pinned column
def pinned_response(P, Pcr, L, x, delta0=0.0, e=0.0):
    """Lateral deflection CHANGE y - y0 of a pinned column with a half-sine bow delta0 and a load at distance e from the
    axis at both ends (Eq. 10.26 plus the bow amplification). Requires P < Pcr."""
    x = np.asarray(x, float)
    a = P / Pcr
    pL = PI * math.sqrt(a)
    p = pL / L
    bow = delta0 * a / (1 - a) * np.sin(PI * x / L)
    ecc = e * (math.tan(pL / 2) * np.sin(p * x) + np.cos(p * x) - 1)
    return bow + ecc


def ymax_secant(e, P, Pcr):
    return e * (1 / math.cos(PI / 2 * math.sqrt(P / Pcr)) - 1)                  # Eq. 10.31


def sigmax_secant(P, A, e, c, r, Pcr):
    return P / A * (1 + e * c / r ** 2 / math.cos(PI / 2 * math.sqrt(P / Pcr)))  # Eq. 10.35


def secant_P_yield(sY, A, e, c, r, E, Le):
    """P at first yield from the secant formula (Eq. 10.36) solved by Brent's method."""
    Pe = PI ** 2 * E * A * r * r / Le ** 2
    f = lambda P: P / A * (1 + e * c / r ** 2 / math.cos(0.5 * math.sqrt(P / (E * A)) * Le / r)) - sY   # noqa: E731
    hi = min(Pe * (1 - 1e-12), sY * A)
    return optimize.brentq(f, 1e-9, hi, xtol=1e-12)


def southwell(delta, P):
    """Southwell plot: delta/P = delta/Pcr + delta0/Pcr. Least squares of delta/P on delta.
    Returns Pcr, delta0, their standard uncertainties from the fit, and the fit residual rms."""
    d = np.asarray(delta, float)
    yv = d / np.asarray(P, float)
    X = np.column_stack([d, np.ones_like(d)])
    coef, res, *_ = np.linalg.lstsq(X, yv, rcond=None)
    s, b = coef
    n = len(d)
    rr = yv - X @ coef
    s2 = float(rr @ rr) / max(n - 2, 1)
    cov = s2 * np.linalg.inv(X.T @ X)
    Pcr = 1 / s
    d0 = b / s
    uP = math.sqrt(cov[0, 0]) / s ** 2
    J = np.array([-b / s ** 2, 1 / s])
    ud0 = math.sqrt(J @ cov @ J)
    return dict(Pcr=Pcr, delta0=d0, uPcr=uP, udelta0=ud0, rms=math.sqrt(s2), slope=s, icpt=b)


# ----------------------------------------------------------------------------- elastica of a pinned column
def elastica_pinned(k):
    """Pinned-pinned elastica with modulus k = sin(alpha/2) (alpha = end slope). Returns P/Pcr and delta/L."""
    m = k * k
    K = special.ellipk(m)
    return (2 * K / PI) ** 2, k / K


def elastica_pinned_bvp(PoPcr, n=801):
    """Same by collocation: theta'' + (pL)^2 sin(theta) = 0 on s in [0, 1] (s = arc length / L), theta'(0) = theta'(1) = 0
    (zero moment at the pins), symmetric mode; y' = sin(theta). Returns delta/L (lateral) and the end slope."""
    lam = PI ** 2 * PoPcr
    s = np.linspace(0, 1, n)

    def f(s_, Y):
        th, kap, yy = Y
        return np.vstack([kap, -lam * np.sin(th), np.sin(th)])

    def bc(ya, yb):
        return np.array([ya[1], yb[1], ya[2]])
    a0 = 2 * math.asin(min(0.999, math.sqrt(max(PoPcr - 1, 1e-6) * 2) / 1.0 * 0.9))
    guess = np.vstack([a0 * np.cos(PI * s), -a0 * PI * np.sin(PI * s), a0 / PI * np.sin(PI * s)])
    sol = integrate.solve_bvp(f, bc, s, guess, tol=1e-10, max_nodes=200000)
    if not sol.success:
        raise RuntimeError(sol.message)
    return float(sol.sol(0.5)[2]), float(sol.sol(0.0)[0])


# ----------------------------------------------------------------------------- material: Ramberg-Osgood
def ro_strain(s, E, s02, m):
    """Strain magnitude for stress magnitude s: s/E + 0.002 (s/s02)^m (Lab 1 fit)."""
    return s / E + 0.002 * (s / s02) ** m


def ro_stress(eps, E, s02, m):
    """Inverse of ro_strain (stress magnitude for strain magnitude) by Newton with a bracket."""
    eps = abs(eps)
    if eps == 0:
        return 0.0
    lo, hi = 0.0, min(E * eps, s02 * (eps / 0.002) ** (1 / m) * 1.0001 + 1.0)
    return optimize.brentq(lambda s: ro_strain(s, E, s02, m) - eps, lo, hi, xtol=1e-6)


def tangent_modulus(s, E, s02, m):
    return 1.0 / (1.0 / E + 0.002 * m * (s / s02) ** (m - 1) / s02)


def reduced_modulus_rect(E, Et):
    return 4 * E * Et / (math.sqrt(E) + math.sqrt(Et)) ** 2


def column_curve_tangent(slender, E, s02, m, reduced=False):
    """Critical stress at slenderness Le/r from sigma = pi^2 E_t(sigma) / (Le/r)^2 (Engesser), or with the reduced
    modulus of a rectangle; solved by Brent's method on sigma."""
    def f(s):
        Et = tangent_modulus(s, E, s02, m)
        Eu = reduced_modulus_rect(E, Et) if reduced else Et
        return s - PI ** 2 * Eu / slender ** 2
    hi = s02 * 1.6
    if f(hi) < 0:
        return hi
    return optimize.brentq(f, 1e-3, hi, xtol=1e-4)


# ----------------------------------------------------------------------------- design formulas
def aa_6061(slender):
    """Allowable stress (Pa) for 6061-T6, Aluminum Association formulas as given in Beer Eqs. 10.43b-10.45b."""
    if slender <= 17.8:
        return 146.3e6
    if slender < 66.0:
        return (173.9 - 1.602 * slender + 0.00323 * slender ** 2) * 1e6
    return 356e3 / slender ** 2 * 1e6


def aisc(slender, E, sY):
    """Beer Eqs. 10.38-10.42: critical stress and allowable stress (F.S. 1.67) for steel."""
    se = PI ** 2 * E / slender ** 2
    scr = 0.658 ** (sY / se) * sY if slender <= 4.71 * math.sqrt(E / sY) else 0.877 * se
    return scr, scr / 1.67


# ----------------------------------------------------------------------------- finite elements (Hermite cubic)
def fe_mats(EI, L, n):
    h = L / n
    k = EI / h ** 3 * np.array([[12, 6 * h, -12, 6 * h], [6 * h, 4 * h * h, -6 * h, 2 * h * h],
                                [-12, -6 * h, 12, -6 * h], [6 * h, 2 * h * h, -6 * h, 4 * h * h]])
    g = 1 / (30 * h) * np.array([[36, 3 * h, -36, 3 * h], [3 * h, 4 * h * h, -3 * h, -h * h],
                                 [-36, -3 * h, 36, -3 * h], [3 * h, -h * h, -3 * h, 4 * h * h]])
    N = 2 * (n + 1)
    K = np.zeros((N, N)); G = np.zeros((N, N))
    for e in range(n):
        idx = [2 * e, 2 * e + 1, 2 * e + 2, 2 * e + 3]
        K[np.ix_(idx, idx)] += k
        G[np.ix_(idx, idx)] += g
    return K, G


def fe_column(EI, L, n, ends):
    """ends = (endA, endB), each a dict(v=True if laterally held, k=rotational stiffness (0 pin, inf fixed)).
    Returns K (with springs), G and the list of free DOFs."""
    K, G = fe_mats(EI, L, n)
    fixed = []
    for node, end in ((0, ends[0]), (n, ends[1])):
        if end.get("v", True):
            fixed.append(2 * node)
        k = end.get("k", 0.0)
        if math.isinf(k):
            fixed.append(2 * node + 1)
        elif k > 0:
            K[2 * node + 1, 2 * node + 1] += k
    free = [i for i in range(K.shape[0]) if i not in fixed]
    return K, G, free


def fe_pcr(EI, L, n, ends, nmodes=1):
    K, G, free = fe_column(EI, L, n, ends)
    Kf, Gf = K[np.ix_(free, free)], G[np.ix_(free, free)]
    w, V = linalg.eigh(Kf, Gf)
    return (w[0] if nmodes == 1 else w[:nmodes]), V[:, 0], free


def fe_imperfect(EI, L, n, ends, P, delta0=0.0, eA=0.0, eB=0.0, harmonics=()):
    """Load-deflection by finite elements: stress-free shape w0 = delta0 sin(pi x/L) + sum a_j sin(j pi x/L) for
    (a_j, j) in harmonics (nodal values and slopes), load
    lines at distance eA, eB on the -y side of the two ends (end moments +P eA at A, -P eB at B; Beer Fig. 10.20).
    Solves (K - P G) u = P G w0 + f for the change u = v - w0, zero at held DOFs (a clamp grips the bar at its
    initial slope; a spring resists the change of slope). Returns x, v (total), w0, and the curvature change at every node (from the
    element on the left, averaged at interior nodes)."""
    K, G, free = fe_column(EI, L, n, ends)
    xn = np.linspace(0, L, n + 1)
    w0 = np.zeros(2 * (n + 1))
    w0[0::2] = delta0 * np.sin(PI * xn / L)
    w0[1::2] = delta0 * PI / L * np.cos(PI * xn / L)
    for aj, j in harmonics:
        w0[0::2] += aj * np.sin(j * PI * xn / L)
        w0[1::2] += aj * j * PI / L * np.cos(j * PI * xn / L)
    f = np.zeros_like(w0)
    f[1] += P * eA
    f[-1] -= P * eB
    rhs = P * (G @ w0) + f                     # unknown: u = v - w0 (zero where an end is held; clamps grip the initial slope)
    A = K - P * G
    v = w0.copy()
    v[free] += np.linalg.solve(A[np.ix_(free, free)], rhs[free])
    return xn, v, w0


def fe_curv_mid(v, w0, L, n):
    """Curvature change (v - w0)'' at mid-length from the Hermite interpolation of the element(s) touching x = L/2."""
    h = L / n
    d = v - w0
    if n % 2 == 0:
        e = n // 2 - 1                     # element ending at mid-length: xi = 1
        idx = slice(2 * e, 2 * e + 4)
        y1, t1, y2, t2 = d[idx]
        k_left = (6 * y1 + 2 * h * t1 - 6 * y2 + 4 * h * t2) / h ** 2   # at xi = 1
        y1, t1, y2, t2 = d[2 * (e + 1): 2 * (e + 1) + 4]
        k_right = (-6 * y1 - 4 * h * t1 + 6 * y2 - 2 * h * t2) / h ** 2  # at xi = 0
        return 0.5 * (k_left + k_right)
    e = n // 2
    y1, t1, y2, t2 = d[2 * e: 2 * e + 4]
    xi = 0.5
    return ((12 * xi - 6) * y1 + (6 * xi - 4) * h * t1 + (-12 * xi + 6) * y2 + (6 * xi - 2) * h * t2) / h ** 2


# ----------------------------------------------------------------------------- second-order finite differences (pinned)
def fd_pinned(EI, L, P, n, delta0=0.0, e=0.0):
    """EI w'' + P w = -P (y0 + e), w = y - y0, w(0) = w(L) = 0, on n intervals (tridiagonal solve)."""
    h = L / n
    x = np.linspace(0, L, n + 1)
    y0 = delta0 * np.sin(PI * x / L)
    m = n - 1
    main = np.full(m, -2 * EI / h ** 2 + P)
    off = np.full(m - 1, EI / h ** 2)
    rhs = -P * (y0[1:-1] + e)
    ab = np.zeros((3, m)); ab[0, 1:] = off; ab[1] = main; ab[2, :-1] = off
    w = np.zeros(n + 1)
    w[1:-1] = linalg.solve_banded((1, 1), ab, rhs)
    return x, w


# ----------------------------------------------------------------------------- imperfect inelastic column (fiber model)
def ro_stress_vec(eps, E, s02, m):
    """Vectorized inverse of ro_strain for strain magnitudes (Newton from a safe start; monotone, converges fast)."""
    eps = np.abs(np.asarray(eps, float))
    s = np.minimum(E * eps, s02 * np.maximum(eps / 0.002, 1e-300) ** (1 / m))
    for _ in range(60):
        f = s / E + 0.002 * (s / s02) ** m - eps
        df = 1 / E + 0.002 * m * (s / s02) ** (m - 1) / s02
        ds = f / df
        s = np.maximum(s - ds, 0.5 * s)
        if np.all(np.abs(ds) <= 1e-9 * np.maximum(s, 1.0)):
            break
    return s


class FiberColumn:
    """Pinned column, assumed half-sine deflected shape, fiber section at mid-length (rectangle b x t, bending in t).
    Material: Ramberg-Osgood envelope (Lab 1 fit), elastic unloading from the most compressive strain each fiber has
    reached, capped by the tension envelope. Displacement control on the mid-length deflection change delta."""

    def __init__(self, b, t, L, E, s02, m, delta0, e, nf=80):
        self.b, self.t, self.L, self.E, self.s02, self.m = b, t, L, E, s02, m
        self.delta0, self.e = delta0, e
        self.z = (np.arange(nf) + 0.5) / nf * t - t / 2           # fiber centers, + toward the +y (convex) face
        self.dA = b * t / nf
        self.emin = np.zeros(nf)                                   # most compressive strain reached (<= 0)
        self.smin = np.zeros(nf)

    def stress(self, eps, commit=False):
        E, s02, m = self.E, self.s02, self.m
        env_c = -ro_stress_vec(np.minimum(eps, 0.0), E, s02, m)
        load = eps <= self.emin
        s = np.where(load, env_c, self.smin + E * (eps - self.emin))
        pos = eps > 0
        if np.any(pos):
            s = np.where(pos, np.minimum(s, ro_stress_vec(np.maximum(eps, 0.0), E, s02, m)), s)
        if commit:
            self.emin = np.where(load, eps, self.emin)
            self.smin = np.where(load, env_c, self.smin)
        return s

    def solve(self, delta):
        """Return (P, centroid strain) at mid-length deflection change delta, and commit the fiber states."""
        L = self.L
        Y = self.delta0 + delta
        kap = PI ** 2 / L ** 2 * delta                          # curvature change (+ = convex on the +y face)

        def resid(e0):
            s = self.stress(e0 + kap * self.z)
            P = -float(np.sum(s) * self.dA)
            Msec = float(np.sum(s * self.z) * self.dA)
            return Msec - P * (Y + self.e), P
        e0 = optimize.brentq(lambda q: resid(q)[0], -0.08, 0.0, xtol=1e-15)
        P = resid(e0)[1]
        self.stress(e0 + kap * self.z, commit=True)
        return P, e0


def fiber_path(b, t, L, E, s02, m, delta0, e, dmax, nstep=400, nf=80):
    """Load-deflection path of the imperfect inelastic column; returns arrays delta, P and the peak load."""
    col = FiberColumn(b, t, L, E, s02, m, delta0, e, nf)
    ds = np.linspace(0, dmax, nstep + 1)[1:]
    Ps = []
    for d in ds:
        Ps.append(col.solve(d)[0])
    Ps = np.array(Ps)
    return ds, Ps, float(Ps.max())

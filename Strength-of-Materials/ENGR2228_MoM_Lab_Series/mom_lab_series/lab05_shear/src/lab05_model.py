"""Lab 5 physics in Python (SI base units). Independent re-implementation of what lab05_simulation.html computes,
using different methods wherever possible: adaptive quadrature for section integrals, a series in the other
direction for the wide-rectangle elasticity solution, ODE shooting (scipy) for partial-interaction beams.

Beer 8e conventions: V and M as in Fig. 5.6 (M > 0 sags); w > 0 downward; tau = VQ/(It) reported as a magnitude
(with Beer's V, tau_xy = -VQ/(It) on a cross-section); deflection y positive upward (a downward deflection is
reported as the magnitude delta).
"""
import math

import numpy as np
from scipy import integrate


# ----------------------------------------------------------------------------- sections (layers from the bottom)
def rect(b, h):
    return [(0.0, h, b)]


def ibeam(B, H, tf, tw):
    return [(0.0, tf, B), (tf, H - tf, tw), (H - tf, H, B)]


def tee(B, H, tf, tw):            # flange on top
    return [(0.0, H - tf, tw), (H - tf, H, B)]


def box(B, H, t):
    return [(0.0, t, B), (t, H - t, 2 * t), (H - t, H, B)]


def width_fn(layers):
    def b(y):
        for y0, y1, bb in layers:
            if y0 <= y <= y1:
                return bb
        return 0.0
    return b


def props(layers):
    """A, centroid height, I about the centroid, by quadrature over each layer."""
    A = sum(integrate.quad(lambda y, bb=bb: bb, y0, y1)[0] for y0, y1, bb in layers)
    Ay = sum(integrate.quad(lambda y, bb=bb: bb * y, y0, y1)[0] for y0, y1, bb in layers)
    yb = Ay / A
    I = sum(integrate.quad(lambda y, bb=bb: bb * (y - yb) ** 2, y0, y1)[0] for y0, y1, bb in layers)
    return dict(A=A, ybar=yb, I=I, H=max(l[1] for l in layers))


def Q_at(layers, y, yb):
    """First moment about the NA of the area above height y (from the bottom), by quadrature."""
    tot = 0.0
    for y0, y1, bb in layers:
        lo = max(y0, y)
        if y1 > lo:
            tot += integrate.quad(lambda e, bb=bb: bb * (e - yb), lo, y1)[0]
    return tot


def tau_at(layers, V, y):
    p = props(layers)
    b = width_fn(layers)(y)
    return V * Q_at(layers, y, p["ybar"]) / (p["I"] * b)


def form_factor(layers):
    """Energy shear form factor f_s = (A/I^2) * integral of Q^2/b dy (Beer-style tau = VQ/(Ib))."""
    p = props(layers)
    tot = 0.0
    for y0, y1, bb in layers:
        tot += integrate.quad(lambda y, bb=bb: Q_at(layers, y, p["ybar"]) ** 2 / bb, y0, y1, epsrel=1e-11, limit=200)[0]
    return p["A"] / p["I"] ** 2 * tot


# ----------------------------------------------------------------------------- circle
def circle_tau_max(V, d):
    c = d / 2
    A, I = math.pi * c ** 2, math.pi * c ** 4 / 4
    Q = 2 * c ** 3 / 3
    return V * Q / (I * 2 * c)


def circle_form_factor(d):
    c = d / 2
    A, I = math.pi * c ** 2, math.pi * c ** 4 / 4
    f = lambda u: ((2.0 / 3.0) * (c * c - u * u) ** 1.5) ** 2 / (2 * math.sqrt(c * c - u * u)) if abs(u) < c else 0.0  # noqa: E731
    return A / I ** 2 * integrate.quad(f, -c, c, epsrel=1e-12, limit=400)[0]


# ----------------------------------------------------------------------------- wide rectangle, Saint-Venant flexure
def rect_edge_ratio_xseries(b, h, nu, x_over_b=0.5, M=200000):
    """tau_yz(x, 0) / (VQ/Ib) for a rectangle (width b, depth h) by a Fourier series in x (the page uses a series in y).
    phi solves lap(phi) = (nu/(1+nu)) (V/I) x, phi = 0 on the boundary; tau = Vc^2/(2I) + phi_x on the neutral axis."""
    c = h / 2
    m = np.arange(1, M + 1, dtype=float)
    mu = 2 * m * np.pi / b
    sech = np.where(mu * c > 700, 0.0, 1.0 / np.cosh(np.minimum(mu * c, 700)))
    x = x_over_b * b
    # sine series in x: x = sum d_m sin(mu_m x), d_m = -2(-1)^m/mu_m; then phi_x(x,0)/k = sum 2(-1)^m (1 - sech(mu_m c)) cos(mu_m x)/mu_m^2
    terms = (2.0 / mu ** 2) * (1 - sech) * (-1.0) ** m * np.cos(mu * x)
    s = terms.sum()
    if abs(x_over_b - 0.5) < 1e-15:     # tail of sum 2/mu^2 (sech ~ 0 there): (b^2/(2 pi^2)) * sum_{m>M} 1/m^2
        s += b ** 2 / (2 * np.pi ** 2) * (1 / M - 1 / (2 * M ** 2) + 1 / (6 * M ** 3))
    return 1 + (nu / (1 + nu)) * (2 / c ** 2) * s


# ----------------------------------------------------------------------------- Timoshenko beam
def timoshenko_delta(P, L, E, G, I, A, fs, support="simple"):
    """Deflection under the load: simple span with a central load, or cantilever with an end load."""
    if support == "simple":
        return P * L ** 3 / (48 * E * I), fs * P * L / (4 * G * A)
    return P * L ** 3 / (3 * E * I), fs * P * L / (G * A)


# ----------------------------------------------------------------------------- partial-interaction two-layer beam
def two_layer(b, t1, t2, E):
    A1, A2 = b * t1, b * t2
    EAs = 1 / (1 / (E * A1) + 1 / (E * A2))
    EI0 = E * b * (t1 ** 3 + t2 ** 3) / 12
    r = (t1 + t2) / 2
    return dict(EAs=EAs, EI0=EI0, r=r, EIfull=EI0 + EAs * r * r)


def moment(load, L, x):
    if load["kind"] == "point":
        P = load["P"]
        return P / 2 * x if x <= L / 2 else P / 2 * (L - x)
    w = load["w"]
    return w * x * (L - x) / 2


def bolts_shoot(geom, L, load, bolts, kb):
    """Discrete connectors at positions `bolts` (each a spring kb between the layers). Slip s = u(bottom of top layer)
    - u(top of bottom layer); N = tension in the bottom layer (equal compression in the top one). Shoots on the
    unknown end slip with N(0) = 0 and requires N(L) = 0. Between bolts N is constant and s' = -N/EAs + r(M - rN)/EI0;
    at a bolt N drops by kb*s (the bolt's force on the bottom layer opposes the slip).
    Returns dict(delta (midspan, down), slip0, forces, N, x-grid)."""
    EAs, EI0, r = geom["EAs"], geom["EI0"], geom["r"]
    c1 = 1 / EAs + r * r / EI0
    pts = sorted(set([0.0, L / 2, L] + list(bolts)))

    def run(s0):
        N, s = 0.0, s0
        F = []
        Ns = []
        for a, b_ in zip(pts[:-1], pts[1:]):
            Ns.append((a, b_, N))
            Mint = (b_ - a) / 6 * (moment(load, L, a) + 4 * moment(load, L, 0.5 * (a + b_)) + moment(load, L, b_))   # Simpson: exact for M quadratic
            s = s - N * c1 * (b_ - a) + r / EI0 * Mint
            if any(abs(b_ - xb) < 1e-12 for xb in bolts):
                f = kb * s                        # connector force on the bottom layer is -kb*s (it resists the slip)
                F.append(f)
                N -= f
        return N, s, F, Ns

    N0, _, _, _ = run(0.0)
    N1, _, _, _ = run(1.0)
    s0 = -N0 / (N1 - N0)
    NL, sL, F, Ns = run(s0)

    m = lambda x: x / 2 if x <= L / 2 else (L - x) / 2  # noqa: E731   unit-load moment for the midspan deflection
    g = lambda x, Nv: (moment(load, L, x) - r * Nv) / EI0 * m(x)  # noqa: E731   cubic on each segment: Simpson is exact
    delta = sum((b_ - a) / 6 * (g(a, Nv) + 4 * g(0.5 * (a + b_), Nv) + g(b_, Nv)) for a, b_, Nv in Ns)
    return dict(delta=delta, slip0=s0, forces=F, residual=NL)


def smeared_bvp(geom, L, load, k, n=4001):
    """Continuous connection of stiffness k per unit length: N'' - alpha^2 N = -beta M, N(0) = N(L) = 0, solved with
    scipy's collocation BVP solver (independent of the closed form). Returns delta (midspan, down) and end slip."""
    EAs, EI0, r = geom["EAs"], geom["EI0"], geom["r"]
    a2 = k * (1 / EAs + r * r / EI0)
    be = k * r / EI0
    xs = np.linspace(0, L, n)

    def f(x, Y):
        M = np.array([moment(load, L, xx) for xx in x])
        return np.vstack([Y[1], a2 * Y[0] - be * M])

    def bc(ya, yb):
        return np.array([ya[0], yb[0]])
    sol = integrate.solve_bvp(f, bc, xs, np.zeros((2, n)), tol=1e-10, max_nodes=200000)
    xf = np.linspace(0, L, 20001)
    Nf = sol.sol(xf)[0]
    M = np.array([moment(load, L, xx) for xx in xf])
    kap = (M - r * Nf) / EI0
    mm = np.where(xf <= L / 2, xf / 2, (L - xf) / 2)
    delta = integrate.simpson(kap * mm, x=xf)
    slip0 = -sol.sol(0.0)[1] / k                   # dN/dx = -k s
    return dict(delta=delta, slip0=slip0, ok=sol.success)


def loose_delta(geom, L, load):
    if load["kind"] == "point":
        return load["P"] * L ** 3 / (48 * geom["EI0"])
    return 5 * load["w"] * L ** 4 / (384 * geom["EI0"])

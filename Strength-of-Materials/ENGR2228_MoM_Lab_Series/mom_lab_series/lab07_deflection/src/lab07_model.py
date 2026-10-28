"""Lab 7 physics in Python (SI base units: N, m, Pa). Independent re-implementation of what lab07_simulation.html
computes, by different methods wherever possible:
  * closed forms: Beer App. F cases combined by superposition (typed again here), with redundants from compatibility;
  * numerical: direct double integration of M(x)/EI on a fine grid (cumulative Simpson), with the integration constants
    and any redundants found from the boundary conditions (the page uses the Hermite finite elements of
    beam_deflection.cpp);
  * elastica: elliptic-integral closed form (scipy.special) and a collocation BVP with self-weight (scipy solve_bvp)
    (the page uses Carlson's symmetric integrals and RK4 shooting).

Beer 8e conventions: x from the left end, y (deflection) positive UPWARD, EI y'' = M (Eq. 9.4); M > 0 sags; V as in
Fig. 5.6 (V = sum of upward forces left of the cut, dV/dx = -w, dM/dx = V). Loads P and w are magnitudes acting
DOWNWARD; applied couples C are positive COUNTERCLOCKWISE (x right, y up, right-hand rule about z). Reaction forces
are reported upward positive, reaction couples counterclockwise positive.
"""
import math

import numpy as np
from scipy import integrate, optimize, special


# ----------------------------------------------------------------------------- closed forms (superposition)
def cant_point(P, a, EI, x):
    """Cantilever fixed at x = 0, downward P at x = a: (y, y')."""
    x = np.asarray(x, float)
    y = np.where(x <= a, -P * x ** 2 * (3 * a - x) / (6 * EI), -P * a ** 2 * (3 * x - a) / (6 * EI))
    t = np.where(x <= a, -P * x * (2 * a - x) / (2 * EI), -P * a ** 2 / (2 * EI) + 0 * x)
    return y, t


def cant_udl(w, L, EI, x):
    """Cantilever fixed at 0, uniform downward w over [0, L]."""
    x = np.asarray(x, float)
    return -w * x ** 2 * (6 * L ** 2 - 4 * L * x + x ** 2) / (24 * EI), -w * x * (3 * L ** 2 - 3 * L * x + x ** 2) / (6 * EI)


def cant_couple(C, c, EI, x):
    """Cantilever fixed at 0, counterclockwise couple C at x = c (sags the part x < c)."""
    x = np.asarray(x, float)
    return np.where(x <= c, C * x ** 2 / (2 * EI), C * c * (2 * x - c) / (2 * EI)), np.where(x <= c, C * x / EI, C * c / EI + 0 * x)


def ss_point(P, a, Ls, EI, x):
    """Simple span [0, Ls], downward P at a (Beer App. F case 5 generalized to any a)."""
    x = np.asarray(x, float)
    b = Ls - a
    xr = Ls - x
    y = np.where(x <= a, -P * b * x * (Ls ** 2 - b ** 2 - x ** 2) / (6 * EI * Ls), -P * a * xr * (Ls ** 2 - a ** 2 - xr ** 2) / (6 * EI * Ls))
    t = np.where(x <= a, -P * b * (Ls ** 2 - b ** 2 - 3 * x ** 2) / (6 * EI * Ls), P * a * (Ls ** 2 - a ** 2 - 3 * xr ** 2) / (6 * EI * Ls))
    return y, t


def ss_udl(w, Ls, EI, x):
    x = np.asarray(x, float)
    return -w * x * (Ls ** 3 - 2 * Ls * x ** 2 + x ** 3) / (24 * EI), -w * (Ls ** 3 - 6 * Ls * x ** 2 + 4 * x ** 3) / (24 * EI)


def ss_end_moment(MB, Ls, EI, x):
    """Simple span with a bending moment MB (sagging +) at its right end, zero at the left: M = MB x / Ls."""
    x = np.asarray(x, float)
    return MB * x * (x ** 2 - Ls ** 2) / (6 * EI * Ls), MB * (3 * x ** 2 - Ls ** 2) / (6 * EI * Ls)


def closed_form(beam, x):
    """beam: dict(family in {'ss','cant','propped','fixed'}, L (span or length), a_over (overhang, ss only), EI,
    P=[(P, a), ...], w (uniform over the whole length), C0 (ccw couple at the right end), k (rotational stiffness of the
    left fixed support, inf = rigid), s (settlement of the right support, up +; propped only)).
    Returns y, y', reactions dict and a list of superposed component curves."""
    fam, EI, w, C0 = beam["family"], beam["EI"], beam.get("w", 0.0), beam.get("C0", 0.0)
    x = np.asarray(x, float)
    Ps = beam.get("P", [])
    if fam == "ss":
        Ls, a = beam["L"], beam.get("a_over", 0.0)
        Lt = Ls + a
        comps = []
        yspan = np.zeros_like(x); tspan = np.zeros_like(x)
        xs = np.minimum(x, Ls)
        span_loads = [(P, p) for P, p in Ps if p <= Ls]
        over_loads = [(P, p) for P, p in Ps if p > Ls]
        for P, p in span_loads:
            yy, tt = ss_point(P, p, Ls, EI, xs)
            comps.append(("P at %.3f m" % p, yy)); yspan += yy; tspan += tt
        if w:
            yy, tt = ss_udl(w, Ls, EI, xs)
            comps.append(("w on the span", yy)); yspan += yy; tspan += tt
        MB = -sum(P * (p - Ls) for P, p in over_loads) - w * a ** 2 / 2 + C0      # sagging + at the roller
        if MB:
            yy, tt = ss_end_moment(MB, Ls, EI, xs)
            comps.append(("overhang moment at the roller", yy)); yspan += yy; tspan += tt
        _, thB = ss_end_moment(MB, Ls, EI, Ls) if MB else (0, 0.0)
        thB = float(sum(ss_point(P, p, Ls, EI, Ls)[1] for P, p in span_loads) + (ss_udl(w, Ls, EI, Ls)[1] if w else 0.0) + thB)
        u = np.maximum(x - Ls, 0.0)
        yo = thB * u
        to = thB + 0 * u
        for P, p in over_loads:
            yy, tt = cant_point(P, p - Ls, EI, u); yo = yo + yy; to = to + tt
        if w and a > 0:
            yy, tt = cant_udl(w, a, EI, u); yo = yo + yy; to = to + tt
        if C0 and a > 0:
            yy, tt = cant_couple(C0, a, EI, u); yo = yo + yy; to = to + tt
        y = np.where(x <= Ls, yspan, yo)
        t = np.where(x <= Ls, tspan, to)
        # reactions by statics: moments about the pin (ccw +)
        Wt = sum(P for P, _ in Ps) + w * Lt
        Mpin = sum(P * p for P, p in Ps) + w * Lt ** 2 / 2 - C0          # moment of the loads about x = 0 (clockwise +) minus ccw couple
        RB = Mpin / Ls
        RA = Wt - RB
        return dict(y=y, t=t, R=dict(RA=RA, RB=RB), comps=comps, Lt=Lt)
    # cantilever-based families: fixed (or spring) at x = 0
    L = beam["L"]
    k = beam.get("k", math.inf)
    s_set = beam.get("s", 0.0)

    def base(x_):
        y = np.zeros_like(np.asarray(x_, float)); t = np.zeros_like(y)
        for P, p in Ps:
            yy, tt = cant_point(P, p, EI, x_); y = y + yy; t = t + tt
        if w:
            yy, tt = cant_udl(w, L, EI, x_); y = y + yy; t = t + tt
        if C0:
            yy, tt = cant_couple(C0, L, EI, x_); y = y + yy; t = t + tt
        return y, t
    M0_loads = -sum(P * p for P, p in Ps) - w * L ** 2 / 2 + C0          # M(0+) from the loads (sagging +)
    flex = 0.0 if math.isinf(k) else 1.0 / k

    def total(R, CR, x_):
        """R: upward force at x = L; CR: ccw couple at x = L (both redundants or zero)."""
        y, t = base(x_)
        yR = R * np.asarray(x_) ** 2 * (3 * L - np.asarray(x_)) / (6 * EI)
        tR = R * np.asarray(x_) * (2 * L - np.asarray(x_)) / (2 * EI)
        yC, tC = cant_couple(CR, L, EI, x_)
        M0 = M0_loads + R * L + CR
        th0 = M0 * flex
        return y + yR + yC + th0 * np.asarray(x_), t + tR + tC + th0, M0
    if fam == "cant":
        R, CR = 0.0, 0.0
    elif fam == "propped":
        y0, _, _ = total(0.0, 0.0, L)
        y1, _, _ = total(1.0, 0.0, L)
        R = (s_set - y0) / (y1 - y0)
        CR = 0.0
    else:                                                              # fixed-fixed
        f = lambda R_, C_: np.array([total(R_, C_, L)[0], total(R_, C_, L)[1]], float)  # noqa: E731
        b0 = f(0.0, 0.0)
        A = np.column_stack([f(1.0, 0.0) - b0, f(0.0, 1.0) - b0])
        R, CR = np.linalg.solve(A, -b0)
    y, t, M0 = total(R, CR, x)
    comps = []
    for P, p in Ps:
        comps.append(("P at %.3f m" % p, cant_point(P, p, EI, x)[0]))
    if w:
        comps.append(("w", cant_udl(w, L, EI, x)[0]))
    if C0:
        comps.append(("end couple", cant_couple(C0, L, EI, x)[0]))
    if R:
        comps.append(("redundant R", R * x ** 2 * (3 * L - x) / (6 * EI)))
    if CR:
        comps.append(("redundant couple", cant_couple(CR, L, EI, x)[0]))
    if flex:
        comps.append(("wall rotation", M0 * flex * x))
    Wt = sum(P for P, _ in Ps) + w * L
    RA = Wt - R
    MA = -M0                                                           # reaction couple at the wall, ccw +: equals -M(0+)
    return dict(y=y, t=t, R=dict(RA=RA, MA=MA, RB=R, MB=CR), comps=comps, Lt=L, M0=float(M0))


def moment_statics(beam, R, x):
    """M(x) (sagging +) from the left free body with the given reactions."""
    x = np.asarray(x, float)
    fam, w = beam["family"], beam.get("w", 0.0)
    M = np.zeros_like(x)
    if fam == "ss":
        Ls = beam["L"]
        M += R["RA"] * x + R["RB"] * np.maximum(x - Ls, 0.0)
    else:
        M += R["RA"] * x - R["MA"]
    for P, p in beam.get("P", []):
        M -= P * np.maximum(x - p, 0.0)
    M -= w * x ** 2 / 2
    return M


# ----------------------------------------------------------------------------- independent numerical: integrate M/EI
def integrate_beam(beam, n=40001):
    """Double integration of y'' = M/EI on a fine grid (cumulative Simpson), constants and redundants from the BCs.
    Returns x, y, y', reactions. Redundants are found by superposing unit-redundant solutions numerically."""
    fam, EI = beam["family"], beam["EI"]
    Lt = beam["L"] + (beam.get("a_over", 0.0) if fam == "ss" else 0.0)
    x = np.linspace(0, Lt, n)
    loads, w, C0 = beam.get("P", []), beam.get("w", 0.0), beam.get("C0", 0.0)

    def M_of(RA, MA, RB, MB, Ls=None):
        M = RA * x - MA - w * x ** 2 / 2
        for P, p in loads:
            M -= P * np.maximum(x - p, 0.0)
        if fam == "ss":
            M += RB * np.maximum(x - Ls, 0.0)
        return M

    def ints(M):
        k = M / EI
        t = integrate.cumulative_simpson(k, x=x, initial=0.0)
        y = integrate.cumulative_simpson(t, x=x, initial=0.0)
        return t, y
    if fam == "ss":
        Ls = beam["L"]
        Wt = sum(P for P, _ in loads) + w * Lt
        RB = (sum(P * p for P, p in loads) + w * Lt ** 2 / 2 - C0) / Ls
        RA = Wt - RB
        M = M_of(RA, 0.0, RB, 0.0, Ls)
        t, y = ints(M)
        iB = np.searchsorted(x, Ls)
        yB = np.interp(Ls, x, y)
        th0 = -yB / Ls                                         # y(0) = 0, y(Ls) = 0
        y = y + th0 * x
        t = t + th0
        return dict(x=x, y=y, t=t, R=dict(RA=RA, RB=RB), M=M, iB=iB)
    L = beam["L"]
    k = beam.get("k", math.inf)
    flex = 0.0 if math.isinf(k) else 1.0 / k
    s_set = beam.get("s", 0.0)
    Wt = sum(P for P, _ in loads) + w * L
    Mload_end = sum(P * p for P, p in loads) + w * L ** 2 / 2       # clockwise moment of the loads about x = 0

    def sol(RB, MB):
        RA = Wt - RB
        MA = -(-Mload_end + RB * L + C0 + MB)                     # ccw +: equilibrium about x = 0
        M = M_of(RA, MA, 0, 0)                                    # couples at x = L enter only through MA
        t, y = ints(M)
        th0 = (-MA) * flex
        return x, y + th0 * x, t + th0, dict(RA=RA, MA=MA, RB=RB, MB=MB), M
    if fam == "cant":
        RB, MB = 0.0, 0.0
    elif fam == "propped":
        y0 = sol(0.0, 0.0)[1][-1]
        y1 = sol(1.0, 0.0)[1][-1]
        RB, MB = (s_set - y0) / (y1 - y0), 0.0
    else:
        def f(R_, C_):
            r = sol(R_, C_)
            return np.array([r[1][-1], r[2][-1]])
        b0 = f(0.0, 0.0)
        A = np.column_stack([f(1.0, 0.0) - b0, f(0.0, 1.0) - b0])
        RB, MB = np.linalg.solve(A, -b0)
    xx, y, t, R, M = sol(RB, MB)
    return dict(x=xx, y=y, t=t, R=R, M=M)


# ----------------------------------------------------------------------------- elastica (tip-loaded cantilever)
def elastica_closed(alpha):
    """Large-deflection cantilever, vertical dead load P at the tip, alpha = P L^2 / EI.
    Returns tip angle theta0 (rad), dv/L (downward tip deflection), x_tip/L. scipy elliptic integrals (parameter m = k^2)."""
    if alpha <= 0:
        return 0.0, 0.0, 1.0

    def g(th0):
        k2 = (1 + math.sin(th0)) / 2
        phi1 = math.asin(1 / math.sqrt(2 * k2))
        return special.ellipk(k2) - special.ellipkinc(phi1, k2) - math.sqrt(alpha)
    th0 = optimize.brentq(g, 1e-12, math.pi / 2 - 1e-12, xtol=1e-15)
    k2 = (1 + math.sin(th0)) / 2
    phi1 = math.asin(1 / math.sqrt(2 * k2))
    dv = 1 - 2 / math.sqrt(alpha) * (special.ellipe(k2) - special.ellipeinc(phi1, k2))
    xt = math.sqrt(2 * math.sin(th0) / alpha)
    return th0, dv, xt


def elastica_bvp(alpha, beta=0.0, n=401):
    """Same problem with a uniform self-weight beta = w L^3 / EI, by collocation (nondimensional s in [0, 1]):
    theta'' = -(alpha + beta (1 - s)) cos(theta); theta(0) = 0, theta'(1) = 0; x' = cos, y' = -sin (y up).
    Returns theta(1), dv/L (downward), x_tip/L."""
    s = np.linspace(0, 1, n)

    def f(s_, Y):
        th, kap, xx, yy = Y
        return np.vstack([kap, -(alpha + beta * (1 - s_)) * np.cos(th), np.cos(th), -np.sin(th)])

    def bc(ya, yb):
        return np.array([ya[0], yb[1], ya[2], ya[3]])
    guess = np.zeros((4, n))
    guess[2] = s
    th_lin = (alpha + beta / 3) * (s - s ** 2 / 2)
    guess[0] = np.minimum(th_lin, 1.4)
    guess[1] = (alpha + beta / 2) * (1 - s)
    sol = integrate.solve_bvp(f, bc, s, guess, tol=1e-10, max_nodes=200000)
    if not sol.success:
        raise RuntimeError(sol.message)
    th1, _, x1, y1 = sol.sol(1.0)
    return float(th1), float(-y1), float(x1), sol


def elastica_p5(target=0.05):
    """alpha at which the linear tip deflection alpha/3 exceeds the elastica value by `target`."""
    return optimize.brentq(lambda a: (a / 3) / elastica_closed(a)[1] - 1 - target, 1e-3, 5.0, xtol=1e-14)


# ----------------------------------------------------------------------------- cantilever with a flexible clamp
def cant_tip_flex(P, L, x, EI, k):
    """Downward deflection (magnitude) at x of a cantilever with tip load P and a clamp of rotational stiffness k."""
    return P * x ** 2 * (3 * L - x) / (6 * EI) + P * L * x / k

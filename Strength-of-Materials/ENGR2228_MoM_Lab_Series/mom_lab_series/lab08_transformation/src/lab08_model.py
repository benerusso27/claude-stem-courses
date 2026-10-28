"""Lab 8 physics in Python (SI base units: N, m, Pa). Independent re-implementation of what lab08_simulation.html
computes, by different methods wherever possible:
  * stress transformation: the 2x2 / 3x3 tensor rotated as R S R^T and diagonalized by numpy.linalg.eigh
    (the page uses Beer's Eqs. 7.5-7.14, Mohr's circle, the trigonometric solution of the cubic, and Jacobi rotations);
  * rosettes: least-squares solution of Eq. 7.60 with numpy (the page uses Beer Eq. 7.43 and Gaussian elimination);
  * tube: first moment Q by scipy dblquad over the annular sector, thick-wall (Lame) stresses by scipy solve_bvp on the
    radial displacement with the closed-end condition (the page uses closed forms and a finite-difference solver).

Beer 8e conventions. Plane stress components sx, sy, txy with txy > 0 on the +x face in the +y direction (Fig. 7.2);
theta counterclockwise from x. Mohr's circle: "clockwise above" (Fig. 7.15): the point of a face is plotted at
(sigma, -tau) with tau the shear on that face, so X = (sx, -txy). Tension positive. Strains: ex, ey, gxy with
e(theta) = ex cos^2 + ey sin^2 + gxy sin cos (Eq. 7.41).

Tube coordinates. X along the tube from the clamp toward the free end, Y up, Z = X x Y (toward the lever side).
A point on the outer surface is located by phi, measured from the top (phi = 0, point H) toward +Z (phi = 90 deg,
point K, the lever side). Local surface frame at the point: x = X; y = 90 deg counterclockwise from x as seen from
outside the tube (at H, y = -Z; at K, y = +Y). The load F acts downward at the free end, at a lever arm aL on the +Z
side, a distance Lb from the gage section; internal pressure p, closed ends.
"""
import math

import numpy as np
from scipy import integrate

MATERIALS = dict(al=dict(name="6061-T6 aluminum", E=68.9e9, nu=0.33, sY=273.7e6, rho=2700.0),
                 steel=dict(name="1018 steel", E=205e9, nu=0.29, sY=296.2e6, rho=7850.0))


# ----------------------------------------------------------------------------- stress at a point
def tensor2(sx, sy, txy):
    return np.array([[sx, txy], [txy, sy]], float)


def rotate2(sx, sy, txy, th):
    """Components on axes rotated counterclockwise by th, by R S R^T (no transformation formulas)."""
    c, s = math.cos(th), math.sin(th)
    Rm = np.array([[c, s], [-s, c]])
    S2 = Rm @ tensor2(sx, sy, txy) @ Rm.T
    return S2[0, 0], S2[1, 1], S2[0, 1]


def principal2(sx, sy, txy):
    """In-plane principal stresses and the angle (ccw from x) of the larger, by eigen-decomposition."""
    w, v = np.linalg.eigh(tensor2(sx, sy, txy))
    th = math.atan2(v[1, 1], v[0, 1])
    th = (th + math.pi / 2) % math.pi - math.pi / 2              # direction, not sense: fold into (-90, 90]
    return w[1], w[0], th


def principal3(S):
    """Principal stresses of a symmetric 3x3 tensor, largest first."""
    return np.sort(np.linalg.eigvalsh(np.asarray(S, float)))[::-1]


def abs_shear(sx, sy, txy, sz=0.0):
    p = principal3([[sx, txy, 0], [txy, sy, 0], [0, 0, sz]])
    return (p[0] - p[-1]) / 2, p


def von_mises(p):
    s1, s2, s3 = p
    return math.sqrt(((s1 - s2) ** 2 + (s2 - s3) ** 2 + (s3 - s1) ** 2) / 2)


# ----------------------------------------------------------------------------- strain, rosettes
RECT = (0.0, math.pi / 4, math.pi / 2)
DELTA = (0.0, math.pi / 3, 2 * math.pi / 3)


def strain_at(ex, ey, gxy, th):
    return ex * math.cos(th) ** 2 + ey * math.sin(th) ** 2 + gxy * math.sin(th) * math.cos(th)


def rosette_solve(angles, eps):
    """ex, ey, gxy from three (or more) gage readings: least squares on Eq. 7.60."""
    A = np.array([[math.cos(t) ** 2, math.sin(t) ** 2, math.sin(t) * math.cos(t)] for t in angles])
    sol, *_ = np.linalg.lstsq(A, np.asarray(eps, float), rcond=None)
    return tuple(sol)


def gage_readings(ex, ey, gxy, angles=RECT, beta=0.0, Kt=0.0, nu0=0.285, gf=None):
    """What the gages indicate: rosette turned by beta (ccw), transverse sensitivity Kt (gage factor calibrated in a
    field with transverse/axial strain = -nu0), and optional per-gage gage-factor ratios gf."""
    out = []
    for i, t in enumerate(angles):
        e_ax = strain_at(ex, ey, gxy, t + beta)
        e_tr = strain_at(ex, ey, gxy, t + beta + math.pi / 2)
        r = (e_ax + Kt * e_tr) / (1 - nu0 * Kt)
        out.append(r * (gf[i] if gf is not None else 1.0))
    return out


def kt_correct_numeric(readings, angles=RECT, Kt=0.0, nu0=0.285):
    """Invert the transverse-sensitivity model for (ex, ey, gxy) by least squares (any rosette)."""
    rows = []
    for t in angles:
        a = np.array([math.cos(t) ** 2, math.sin(t) ** 2, math.sin(t) * math.cos(t)])
        b = np.array([math.sin(t) ** 2, math.cos(t) ** 2, -math.sin(t) * math.cos(t)])
        rows.append((a + Kt * b) / (1 - nu0 * Kt))
    sol, *_ = np.linalg.lstsq(np.array(rows), np.asarray(readings, float), rcond=None)
    return tuple(sol)


def derotate(ex, ey, gxy, beta):
    """Strain components on axes turned by -beta (undo a rosette turned by +beta), by tensor rotation."""
    E = np.array([[ex, gxy / 2], [gxy / 2, ey]])
    c, s = math.cos(-beta), math.sin(-beta)
    Rm = np.array([[c, s], [-s, c]])
    E2 = Rm @ E @ Rm.T
    return E2[0, 0], E2[1, 1], 2 * E2[0, 1]


def hooke_plane_stress(ex, ey, gxy, E, nu):
    k = E / (1 - nu * nu)
    return k * (ex + nu * ey), k * (ey + nu * ex), E / (2 * (1 + nu)) * gxy


# ----------------------------------------------------------------------------- tube
def tube_props(Do, Di):
    ro, ri = Do / 2, Di / 2
    I = math.pi * (ro ** 4 - ri ** 4) / 4
    return dict(ro=ro, ri=ri, t=ro - ri, A=math.pi * (ro ** 2 - ri ** 2), I=I, J=2 * I)


def Q_quad(ro, ri, phi):
    """First moment about the neutral axis of the wall between the top (0) and phi, by double quadrature."""
    val, _ = integrate.dblquad(lambda r, psi: r * math.cos(psi) * r, 0.0, phi, lambda _: ri, lambda _: ro, epsabs=1e-16, epsrel=1e-13)
    return val


def lame_closed(p, ri, ro, r):
    A = p * ri ** 2 / (ro ** 2 - ri ** 2)
    B = p * ri ** 2 * ro ** 2 / (ro ** 2 - ri ** 2)
    return A - B / r ** 2, A + B / r ** 2, A                    # sigma_r, sigma_theta, sigma_x (closed ends)


def lame_bvp(p, ri, ro, E=68.9e9, nu=0.33):
    """Thick cylinder with closed ends by collocation: u'' + u'/r - u/r^2 = 0 for the radial displacement, with
    sigma_r(ri) = -p, sigma_r(ro) = 0, and a uniform axial strain ez fixed by the end force p*pi*ri^2 (generalized
    plane strain). Returns sigma_r, sigma_theta, sigma_x at the outer surface, and ez."""
    lam = E * nu / ((1 + nu) * (1 - 2 * nu))
    mu = E / (2 * (1 + nu))

    def stresses(r, u, du, ez):
        sr = lam * (du + u / r + ez) + 2 * mu * du
        st = lam * (du + u / r + ez) + 2 * mu * u / r
        sz = lam * (du + u / r + ez) + 2 * mu * ez
        return sr, st, sz

    def solve(ez):
        r = np.linspace(ri, ro, 41)
        sol = integrate.solve_bvp(lambda r_, Y: np.vstack([Y[1], -Y[1] / r_ + Y[0] / r_ ** 2]),
                                  lambda ya, yb: np.array([stresses(ri, ya[0], ya[1], ez)[0] + p, stresses(ro, yb[0], yb[1], ez)[0]]),
                                  r, np.zeros((2, r.size)), tol=1e-12, max_nodes=100000)
        rr = np.linspace(ri, ro, 4001)
        u, du = sol.sol(rr)
        sz = stresses(rr, u, du, ez)[2]
        Fz = integrate.simpson(sz * 2 * math.pi * rr, x=rr)
        return sol, Fz - p * math.pi * ri ** 2
    f0, f1 = solve(0.0)[1], solve(1e-4)[1]
    ez = -f0 * 1e-4 / (f1 - f0)                                  # the end condition is linear in ez
    sol, _ = solve(ez)
    u, du = sol.sol(ro)
    sr, st, sz = stresses(ro, u, du, ez)
    return float(sr), float(st), float(sz), ez


def tube_state(Do, Di, F, aL, Lb, p, phi, wall="lame", Q=None):
    """Local surface stresses (sx along the tube, sy around it, txy in the local frame) at angle phi."""
    tp = tube_props(Do, Di)
    ro, ri, I, J, t = tp["ro"], tp["ri"], tp["I"], tp["J"], tp["t"]
    sx_b = F * Lb * ro * math.cos(phi) / I                       # sigma = -My/I with M = -F*Lb (hogging)
    T = F * aL
    tauT = T * ro / J
    Qv = (ro ** 3 - ri ** 3) / 3 * math.sin(phi) if Q is None else Q
    tauV = F * Qv / (I * t)
    if wall == "lame":
        _, s_h, s_a = lame_closed(p, ri, ro, ro)
    else:
        s_h, s_a = p * ri / t, p * ri / (2 * t)
    return dict(sx=sx_b + s_a, sy=s_h, txy=-(tauT + tauV), sx_b=sx_b, tauT=tauT, tauV=tauV, s_h=s_h, s_a=s_a, T=T, M=F * Lb)


def state_strains(sx, sy, txy, E, nu):
    G = E / (2 * (1 + nu))
    return (sx - nu * sy) / E, (sy - nu * sx) / E, txy / G

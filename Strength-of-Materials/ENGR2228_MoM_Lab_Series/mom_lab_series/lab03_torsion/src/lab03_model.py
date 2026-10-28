"""Lab 3 physics in Python (SI base units: N, m, Pa, rad). Independent re-implementation of the
closed forms used by lab03_simulation.html, adaptive-quadrature torque integration, the Saint-Venant
series for a rectangle, and a sparse finite-difference solver for the Prandtl stress function.

Circular shafts: plane sections rotate rigidly, gamma = rho*theta (theta = twist per unit length),
T = integral of tau * rho dA (Beer 8e Sec. 3.1). Torque and twist follow the right-hand rule.
"""
import math

import numpy as np
from scipy import integrate, optimize, sparse
from scipy.sparse.linalg import spsolve


def J_polar(c, ci=0.0):
    return math.pi * (c ** 4 - ci ** 4) / 2


# ----------------------------------------------------------------------------- shear stress-strain laws
def tau_of(m, g):
    """Shear stress magnitude for shear strain g >= 0 (monotonic loading). m: dict with 'law' and parameters."""
    g = abs(g)
    law = m["law"]
    if law == "epp":
        return min(m["G"] * g, m["tauY"])
    if law == "plateau":
        gY = m["tauY"] / m["G"]
        if g <= gY:
            return m["G"] * g
        if g <= m["gL"]:
            return m["tauY"]
        ga = (m["tauY"] / m["A"]) ** (1 / m["n"])
        return m["A"] * (g - m["gL"] + ga) ** m["n"]
    if law == "ro":
        if g == 0:
            return 0.0
        f = lambda t: t / m["G"] + m["g0"] * (t / m["tauY"]) ** m["m"] - g  # noqa: E731
        hi = min(m["G"] * g, m["tauY"] * (g / m["g0"]) ** (1 / m["m"]))
        return optimize.brentq(f, 0.0, hi * (1 + 1e-12), xtol=1e-14 * hi, rtol=1e-15, maxiter=500)
    if law == "tanh":
        return m["tauc"] * math.tanh(m["G"] * g / m["tauc"])
    raise ValueError(law)


# ----------------------------------------------------------------------------- circular shafts
def epp_torque(c, ci, G, tauY, theta):
    if theta <= 0:
        return 0.0
    rY = tauY / (G * theta)
    if rY >= c:
        return J_polar(c, ci) * G * theta
    if rY <= ci:
        return 2 * math.pi / 3 * tauY * (c ** 3 - ci ** 3)
    return math.pi / 2 * tauY / rY * (rY ** 4 - ci ** 4) + 2 * math.pi / 3 * tauY * (c ** 3 - rY ** 3)


def torque_quad(m, c, ci, theta):
    """T = int_ci^c 2 pi rho^2 tau(rho theta) d rho by adaptive quadrature, splitting at known kinks."""
    brk = [ci, c]
    if m["law"] in ("epp", "plateau") and theta > 0:
        for g in ([m["tauY"] / m["G"]] + ([m["gL"]] if m["law"] == "plateau" else [])):
            r = g / theta
            if ci < r < c:
                brk.append(r)
    brk = sorted(brk)
    T = 0.0
    for a, b in zip(brk[:-1], brk[1:]):
        T += integrate.quad(lambda r: 2 * math.pi * r * r * tau_of(m, r * theta), a, b, epsabs=0, epsrel=1e-13, limit=200)[0]
    return T


def twist_for_torque(m, c, ci, T, L):
    """Angle of twist over L that produces torque T (root of torque_quad)."""
    f = lambda phi: torque_quad(m, c, ci, phi / L) - T  # noqa: E731
    hi = 1e-6
    while f(hi) < 0:
        hi *= 2
    return optimize.brentq(f, 0, hi, xtol=1e-15, rtol=1e-14)


def fiber_torque_path(m, c, ci, theta_path, nr=400):
    """Torque along a twist history that may reverse (load, unload, reload).
    Each ring follows the monotonic law when loading past its previous maximum strain and unloads
    elastically (slope G) otherwise, with reverse yielding at -tau(gmax) (kinematic-free, Masing-free model).
    Returns torque array. Rings by Gauss-Legendre quadrature for accuracy."""
    xg, wg = np.polynomial.legendre.leggauss(nr)
    r = 0.5 * (c - ci) * xg + 0.5 * (c + ci)
    w = 0.5 * (c - ci) * wg
    gmax = np.zeros(nr)      # largest strain reached by each ring
    tmax = np.zeros(nr)      # stress at that strain
    out = []
    for th in theta_path:
        g = r * th
        tau = np.empty(nr)
        for k in range(nr):
            if g[k] >= gmax[k]:
                gmax[k] = g[k]
                tmax[k] = tau_of(m, g[k])
                tau[k] = tmax[k]
            else:
                tau[k] = max(tmax[k] - m["G"] * (gmax[k] - g[k]), -tmax[k])
        out.append(float(np.sum(2 * math.pi * r * r * tau * w)))
    return np.array(out)


# ----------------------------------------------------------------------------- rectangle (Saint-Venant)
def rect_series(a, b, nterms=400):
    if a < b:
        a, b = b, a
    n = np.arange(1, 2 * nterms, 2, dtype=float)
    z = n * math.pi * a / (2 * b)
    s2 = np.sum(np.tanh(z) / n ** 5)
    with np.errstate(over="ignore"):
        sk = np.sum(np.where(z > 700, 0.0, 1 / (n * n * np.cosh(np.minimum(z, 700)))))
    c2 = (1 - 192 / math.pi ** 5 * (b / a) * s2) / 3
    k = 1 - 8 / math.pi ** 2 * sk
    return dict(c1=c2 / k, c2=c2, k=k)


def rect_fd(a, b, ny):
    """Independent FD solve of lap(psi) = -2 with scipy.sparse (direct solver), same 5-point stencil.
    Returns c2 and k (= tau_max / (G theta b))."""
    if a < b:
        a, b = b, a
    ny = max(2, 2 * round(ny / 2))
    nx = max(2, 2 * round(ny * a / b / 2))
    hx, hy = a / nx, b / ny
    mx, my = nx - 1, ny - 1
    Dx = sparse.diags([-1.0, 2.0, -1.0], [-1, 0, 1], shape=(mx, mx)) / hx ** 2
    Dy = sparse.diags([-1.0, 2.0, -1.0], [-1, 0, 1], shape=(my, my)) / hy ** 2
    A = sparse.kron(sparse.identity(my), Dx) + sparse.kron(Dy, sparse.identity(mx))
    psi = spsolve(A.tocsc(), 2 * np.ones(mx * my)).reshape(my, mx)
    c2 = 2 * psi.sum() * hx * hy / (a * b ** 3)
    ic = nx // 2 - 1
    p1 = psi[0, ic]
    p2 = psi[1, ic] if my > 1 else 0.0
    k = (4 * p1 - p2) / (2 * hy) / b
    return dict(c2=c2, k=k, c1=c2 / k)


# ----------------------------------------------------------------------------- thin-walled tube
def tube_bredt(dout, t, T, G):
    c = dout / 2
    rm = c - t / 2
    Am = math.pi * rm * rm
    return dict(tau=T / (2 * t * Am), theta=T * (2 * math.pi * rm / t) / (4 * Am * Am * G))


def tube_exact(dout, t, T, G):
    c = dout / 2
    J = J_polar(c, c - t)
    return dict(tau=T * c / J, theta=T / (J * G), J=J)

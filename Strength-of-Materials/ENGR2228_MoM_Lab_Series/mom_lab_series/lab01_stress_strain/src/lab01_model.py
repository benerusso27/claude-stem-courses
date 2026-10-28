"""Lab 1 physics in Python (SI base units: N, m, Pa).

Two jobs:
  1. "Truth" model used to generate realistic sample data (generate_sample_data.py).
  2. Independent re-implementation of the closed forms used by lab01_simulation.html,
     so the browser code can be checked against a second language and a second method
     (scipy root-finding / quadrature instead of the page's marching solver).

Physical model of the specimen ("zone model"):
  * The gage length L0 holds a short neck zone of length ell whose area is smaller by the
    fraction delta (a machining/material imperfection), and the remaining L0 - ell of
    nominal area A0. The rest of the reduced section (Lc - L0) also has area A0.
  * Equilibrium: the same axial force P acts on every cross-section (statics, no body force).
  * Constitutive law: true stress sigma = sigma_f(eps_p) while yielding, elastic otherwise;
    true strain eps_t = eps_p + sigma/E.
  * Plastic flow conserves volume: A = A_initial * exp(-eps_p).
  * Compatibility: elongations of the regions add.
  The zone's plastic strain is the monotonic driver; the other region follows the load
  (yields on the rising branch while P rises, unloads elastically once P falls).
"""
import math

import numpy as np
from scipy.optimize import brentq, minimize_scalar


# --------------------------------------------------------------------------- flow laws
class Swift:
    """sigma_f = K (eps0 + eps_p)^n with K eps0^n = sigma_e (continuous at the elastic limit)."""

    def __init__(self, K, n, sigma_e):
        self.K, self.n, self.sigma_e = K, n, sigma_e
        self.eps0 = (sigma_e / K) ** (1.0 / n)

    def __call__(self, ep):
        return self.K * (self.eps0 + ep) ** self.n


class SwiftAfterLuders:
    """Hardening that restarts at the end of a Luders plateau (eps_p >= eps_L)."""

    def __init__(self, K, n, sigma_start_true, eps_L):
        self.K, self.n, self.eps_L = K, n, eps_L
        self.eps0 = (sigma_start_true / K) ** (1.0 / n)

    def __call__(self, ep):
        return self.K * (self.eps0 + max(ep - self.eps_L, 0.0)) ** self.n


class RambergOsgoodPlastic:
    """Plastic part of Ramberg-Osgood: eps_p = 0.002 (sigma/s02)^m  ->  sigma = s02 (eps_p/0.002)^(1/m)."""

    def __init__(self, s02, m):
        self.s02, self.m = s02, m

    def __call__(self, ep):
        return self.s02 * (max(ep, 0.0) / 0.002) ** (1.0 / self.m)


# --------------------------------------------------------------------------- zone model
def simulate_zone(flow, E, A0, L0, Lc, ell, delta, eps_f, ep_start=0.0, n_steps=400, grading=3.0,
                  elastic_pts=40, sigma_e=None):
    """March the equilibrium path. Returns dict of arrays (SI).

    flow(ep) -> true flow stress for ep >= ep_start. If sigma_e is given (sharp elastic limit),
    an elastic segment is prepended up to the zone's first yield.
    """
    A0z = A0 * (1.0 - delta)
    g_rest = lambda x: flow(x) * A0 * math.exp(-x)          # noqa: E731  load capacity of the rest
    # peak of the rest's load capacity (Considere point of the uniform material)
    hi = ep_start + 3.0
    res = minimize_scalar(lambda x: -g_rest(x), bounds=(ep_start, hi), method="bounded",
                          options={"xatol": 1e-12})
    x_peak = res.x

    out = {k: [] for k in ("P", "ep_z", "ep_r", "sig_z", "sig_r", "et_z", "et_r", "d_gage", "d_red")}

    def record(P, epz, epr):
        sz = P / (A0z * math.exp(-epz))
        sr = P / (A0 * math.exp(-epr))
        etz, etr = epz + sz / E, epr + sr / E
        dg = ell * math.expm1(etz) + (L0 - ell) * math.expm1(etr)
        out["P"].append(P)
        out["ep_z"].append(epz)
        out["ep_r"].append(epr)
        out["sig_z"].append(sz)
        out["sig_r"].append(sr)
        out["et_z"].append(etz)
        out["et_r"].append(etr)
        out["d_gage"].append(dg)
        out["d_red"].append(dg + (Lc - L0) * math.expm1(etr))

    epr = ep_start
    if sigma_e is not None:
        for P in np.linspace(0.0, sigma_e * A0z * math.exp(-ep_start), elastic_pts):
            record(P, ep_start, ep_start)
    t = np.linspace(0.0, 1.0, n_steps + 1)[1:]
    for epz in ep_start + (eps_f - ep_start) * t ** grading:
        P = flow(epz) * A0z * math.exp(-epz)
        if P > g_rest(epr) and epr < x_peak:
            if P >= g_rest(x_peak):
                raise RuntimeError("load exceeds the capacity of the stronger region")
            epr = brentq(lambda x: g_rest(x) - P, epr, x_peak, xtol=1e-14)
        record(P, epz, epr)
    return {k: np.array(v) for k, v in out.items()}


# --------------------------------------------------------------------------- closed forms (Swift)
def swift_closed_forms(E, K, n, sigma_e):
    """Textbook-style closed forms for a uniform (perfect) bar with Swift hardening.

    Returns engineering quantities. Derivations are in the handout, Sec. 2.
    """
    eps0 = (sigma_e / K) ** (1.0 / n)
    # 0.2 % offset yield, small-strain form (true ~ engineering at eps ~ 0.2 %)
    sigY = K * (eps0 + 0.002) ** n
    # Considere (rigid-plastic hardening rate): d sigma/d eps_p = sigma  ->  eps0 + eps_p = n
    ep_u = n - eps0
    sig_t_u = K * n ** n
    et_u = ep_u + sig_t_u / E
    sigU = sig_t_u * math.exp(-et_u)
    e_u = math.expm1(et_u)
    # energy per unit initial volume to maximum load = integral sigma_t d eps_t (exact identity)
    uU = sig_t_u ** 2 / (2 * E) + K / (n + 1) * (n ** (n + 1) - eps0 ** (n + 1))
    return dict(eps0=eps0, sigY=sigY, ep_u=ep_u, sig_t_u=sig_t_u, et_u=et_u, sigU=sigU, e_u=e_u, uU=uU)


def swift_exact_by_quadrature(E, K, n, sigma_e):
    """Independent check of swift_closed_forms with scipy (root finding + quadrature),
    using the full finite-strain uniform-bar curve (no rigid-plastic approximation)."""
    from scipy.integrate import quad
    sw = Swift(K, n, sigma_e)
    # uniform bar: nominal stress s(ep) = sigma_f(ep) * exp(-eps_t), eps_t = ep + sigma_f/E
    s_of = lambda ep: sw(ep) * math.exp(-(ep + sw(ep) / E))  # noqa: E731
    r = minimize_scalar(lambda ep: -s_of(ep), bounds=(0, 2.0), method="bounded", options={"xatol": 1e-13})
    ep_u = r.x
    sigU = s_of(ep_u)
    et_u = ep_u + sw(ep_u) / E
    # energy: integral of sigma_t d eps_t = elastic part + integral sigma_f d(ep) + integral sigma d(sigma)/E
    uU = sw(ep_u) ** 2 / (2 * E) + quad(sw, 0, ep_u, epsabs=1e-6, limit=200)[0]
    # offset yield on the TRUE curve at eps_p = 0.002 (exact) and on the ENGINEERING curve (finite strain)
    sigY_true = sw(0.002)

    def offset_eng(ep):
        st = sw(ep)
        et = ep + st / E
        e = math.expm1(et)
        s = st * math.exp(-et)
        return s - E * (e - 0.002)
    ep_y = brentq(offset_eng, 1e-9, 0.05, xtol=1e-15)
    st = sw(ep_y)
    sigY_eng = st * math.exp(-(ep_y + st / E))
    return dict(ep_u=ep_u, sigU=sigU, e_u=math.expm1(et_u), uU=uU, sigY_true=sigY_true, sigY_eng=sigY_eng)

"""Lab 6 analysis: every number in the instructor key comes from this script.

    python3 lab06_analysis.py [data.csv] [measurements.json]   ->  results.json + printed summary
"""
import csv
import json
import math
import sys
from pathlib import Path

import numpy as np
from scipy import optimize

import lab06_model as LM

HERE = Path(__file__).resolve().parent
LAB = HERE.parent
R3 = math.sqrt(3)
GAGES = [f"g{k:02d}_ue" for k in range(1, 13)]

# D1: single-angle tension brace connected through one leg (Table D1 of the handout)
D1 = dict(T=40e3, L=1.50, a=0.075, tg=9.53e-3, sa_frac=0.6)
CATALOG = [  # name, vertical (outstanding) leg, horizontal (connected) leg, t, gage of the connected leg (mm)
    ("L38 × 38 × 4.8", 38.1, 38.1, 4.76, 22.2), ("L51 × 51 × 4.8", 50.8, 50.8, 4.76, 28.6), ("L51 × 51 × 6.4", 50.8, 50.8, 6.35, 28.6),
    ("L64 × 64 × 6.4", 63.5, 63.5, 6.35, 34.9), ("L76 × 51 × 6.4, long leg connected", 50.8, 76.2, 6.35, 44.5),
    ("L76 × 51 × 6.4, short leg connected", 76.2, 50.8, 6.35, 28.6), ("L76 × 76 × 6.4", 76.2, 76.2, 6.35, 44.5),
    ("L76 × 76 × 9.5", 76.2, 76.2, 9.53, 44.5)]
RHO = 2700.0


def load(path):
    rows = list(csv.DictReader(open(path, newline="")))
    f = lambda v: float(v) if v.strip() else np.nan  # noqa: E731
    return [{k: (v if k in ("part", "config") else f(v)) for k, v in r.items()} for r in rows]


def sel(rows, part, config):
    return [r for r in rows if r["part"] == part and r["config"] == config]


def loading(rr):
    Ps = [r["load_N"] for r in rr]
    imax = int(np.argmax(Ps))
    return [r for r in rr[: imax + 1] if r["load_N"] > 100]


def linfit(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    n = len(x)
    A = np.vstack([np.ones(n), x]).T
    coef, *_ = np.linalg.lstsq(A, y, rcond=None)
    res = y - A @ coef
    s2 = res @ res / max(n - 2, 1)
    cov = s2 * np.linalg.inv(A.T @ A)
    return coef[0], coef[1], math.sqrt(cov[0, 0]), math.sqrt(cov[1, 1]), cov


def mean_u(vals, acc):
    v = np.array(vals, float)
    return float(v.mean()), math.sqrt((v.std(ddof=1) / math.sqrt(len(v))) ** 2 + (acc / R3) ** 2)


def bc_factor(P, EI, L, a, x=None):
    """Beam-column factor C(x) = M(x)/(P e) of the tension member with rigid end blocks (Eq. 7 of the handout)."""
    b = LM.beam_column(P, EI, L, a, 1.0)
    return float(b["M"](L / 2 if x is None else x))


def analyze(rows, m):
    ref = m["reference"]
    E = ref["E_al_GPa"] * 1e3                     # N/mm^2 (MPa); lengths in mm below
    uE = ref["u_E_al_GPa"] / ref["E_al_GPa"]
    u_gf = m["gage_factor_tolerance_pct"] / 100 / R3
    u_P = m["load_cell_accuracy_pct"] / 100 / R3
    u_hole = m["hole_position_accuracy_mm"] / R3
    sY = ref["sY_al_MPa"]
    out = dict(E=E, uE=uE, sY=sY)
    # ------------------------------------------------------------------ bar (Parts A and C)
    bm = m["bar"]
    h, uh = mean_u(bm["h_mm"], m["caliper_accuracy_mm"])
    b, ub = mean_u(bm["b_mm"], m["micrometer_accuracy_mm"])
    A = b * h
    Iz, Iy = b * h ** 3 / 12, h * b ** 3 / 12
    L, a = bm["L_mm"], bm["a_mm"]
    uL = ua = m["rule_accuracy_mm"] / R3
    yF, yB = np.array(bm["y_front_mm"]), np.array(bm["y_back_mm"])
    ym = (yF + yB) / 2
    out["bar"] = dict(h=h, uh=uh, b=b, ub=ub, A=A, Iz=Iz, Iy=Iy, rz2=h * h / 12, ry2=b * b / 12, L=L, a=a,
                      PE_strong=math.pi ** 2 * E * Iz / L ** 2, PE_weak=math.pi ** 2 * E * Iy / L ** 2,
                      PEb_strong=LM.euler_load_blocks(E * Iz, L, a), PEb_weak=LM.euler_load_blocks(E * Iy, L, a))
    A_ = {}
    for cfg in ("e0", "e1", "e2"):
        rr = loading(sel(rows, "A", cfg))
        P = np.array([r["load_N"] for r in rr])
        eps = np.array([[r[g] for g in GAGES] for r in rr])
        avg = (eps[:, 0:5] + eps[:, 5:10]) / 2                       # front/back average at each y
        dfb = (eps[:, 0:5] - eps[:, 5:10]) / 2                       # half-difference: out-of-plane bending
        fits = [linfit(ym, row) for row in avg]                       # eps = eps0 + beta*y (microstrain, per mm)
        eps0 = np.array([f[0] for f in fits])
        beta = np.array([f[1] for f in fits])
        e_eff = (h * h / 12) * beta / eps0                           # mm  (E, gage factor and load cancel)
        k = -1
        f = fits[k]
        # gage positions: each averaged position is uncertain by u_y/sqrt(2); slope error = beta * u_y' / sqrt(sum (y - ybar)^2)
        u_ypos = m["gage_position_accuracy_mm"] / R3 / math.sqrt(2)
        rel_pos = u_ypos / math.sqrt(float(((ym - ym.mean()) ** 2).sum()))
        u_e_eff = math.sqrt((e_eff[k] * (f[3] / f[1])) ** 2 + (e_eff[k] * f[2] / f[0]) ** 2 + (e_eff[k] * 2 * uh / h) ** 2
                            + (e_eff[k] * rel_pos) ** 2) if abs(f[1]) > 1e-9 else (h * h / 12) * f[3] / f[0]
        e_hole = bm["yP_mm"][cfg]
        C = bc_factor(P[k], E * Iz, L, a)
        dC = [(bc_factor(P[k], E * Iz * (1 + 1e-4), L, a) - C) / 1e-4 * uE, (bc_factor(P[k], E * Iz, L + 0.01, a) - C) / 0.01 * uL,
              (bc_factor(P[k], E * Iz, L, a + 0.01) - C) / 0.01 * ua]
        uC = math.sqrt(sum(d * d for d in dC))
        pred_bc = e_hole * C
        u_pred_bc = math.hypot(u_hole * C, e_hole * uC)
        sig0 = E * eps0[k] * 1e-6
        PA = P[k] / A
        u_sig0 = sig0 * math.sqrt(uE ** 2 + u_gf ** 2 + (f[2] / f[0]) ** 2)
        u_PA = PA * math.sqrt(u_P ** 2 + (uh / h) ** 2 + (ub / b) ** 2)
        yNA = -eps0[k] / beta[k] if abs(beta[k]) > 1e-9 else -math.inf
        # out-of-plane bending: half front-minus-back difference, corrected for the small mismatch of the front and back
        # gage heights (the in-plane gradient beta times half the height difference)
        dfb_c = dfb[k] - beta[k] * (yF - yB) / 2
        pb = float(np.mean(dfb_c) / eps0[k])                         # fraction of bending (out of plane)
        pb_raw = float(np.mean(dfb[k]) / eps0[k])
        A_[cfg] = dict(P=P.tolist(), eps0=eps0.tolist(), beta=beta.tolist(), e_eff=e_eff.tolist(), e_eff_max=float(e_eff[k]),
                       u_e_eff=u_e_eff, e_hole=e_hole, u_hole=u_hole, C=C, uC=uC, pred_bc=pred_bc, u_pred_bc=u_pred_bc,
                       agree_bc=2 * math.hypot(u_e_eff, u_pred_bc), agree_450=2 * math.hypot(u_e_eff, u_hole),
                       sig0=sig0, u_sig0=u_sig0, PA=PA, u_PA=u_PA, yNA=yNA, yNA_pred=-(h * h / 12) / e_hole if e_hole > 1e-6 else -math.inf,
                       yNA_pred_bc=-(h * h / 12) / pred_bc if pred_bc > 1e-6 else -math.inf,
                       pct_bend_z=100 * pb, pct_bend_raw=100 * pb_raw, dfb_spread=float(np.ptp(dfb_c)), dfb_spread_raw=float(np.ptp(dfb[k])), ez_eff=pb * b / 6, avg_max=avg[k].tolist(), dfb_max=dfb[k].tolist(),
                       sig_max=E * 1e-6 * (eps0[k] + beta[k] * h / 2), sig_min=E * 1e-6 * (eps0[k] - beta[k] * h / 2),
                       sig_max_450=PA * (1 + 6 * e_hole / h), sig_min_450=PA * (1 - 6 * e_hole / h),
                       resid=[float(v) for v in (avg[k] - (eps0[k] + beta[k] * ym))])
        # trend of e_eff with P (Challenge C1): slope of e_eff vs P, and the beam-column prediction of the same slope
        if cfg != "e0":
            c0, c1, uc0, uc1, _ = linfit(P, e_eff)
            Ps = np.linspace(P[0], P[-1], 6)
            pc = [e_hole * bc_factor(pp, E * Iz, L, a) for pp in Ps]
            _, s_pred, *_ = linfit(Ps, pc)
            A_[cfg].update(trend=dict(e0=c0, ue0=uc0, slope=c1, uslope=uc1, slope_pred=s_pred, drop_pct=-100 * c1 * P[-1] / c0))
    out["A"] = A_
    # ------------------------------------------------------------------ Part C: weak-axis eccentricity
    rr = loading(sel(rows, "C", "ez"))
    P = np.array([r["load_N"] for r in rr])
    eps = np.array([[r[g] for g in GAGES] for r in rr])
    ax = (eps[:, 0:5] + eps[:, 5:10]).mean(axis=1) / 2
    bd = (eps[:, 0:5] - eps[:, 5:10]).mean(axis=1) / 2
    ax_end = (eps[:, 10] + eps[:, 11]) / 2
    bd_end = (eps[:, 10] - eps[:, 11]) / 2
    e_z = bm["zP_mm"]["ez"]
    Cmid_m = (bd / ax) * b / (6 * e_z)                               # M/(P e) = (eps_b/eps_ax) * r_y^2 / ((b/2) e)
    Cend_m = (bd_end / ax_end) * b / (6 * e_z)
    w = np.array([r["w_mid_mm"] for r in rr])
    xe = bm["x_end_mm"]
    Cmid_p = np.array([bc_factor(pp, E * Iy, L, a) for pp in P])
    Cend_p = np.array([bc_factor(pp, E * Iy, L, a, xe) for pp in P])
    w_p = e_z * (1 - Cmid_p)
    k = -1

    def uC_of(pp, x=None):
        c = bc_factor(pp, E * Iy, L, a, x)
        d = [(bc_factor(pp, E * Iy * (1 + 1e-4), L, a, x) - c) / 1e-4 * math.hypot(uE, 3 * ub / b),
             (bc_factor(pp, E * Iy, L + 0.01, a, x) - c) / 0.01 * uL, (bc_factor(pp, E * Iy, L, a + 0.01, x) - c) / 0.01 * ua,
             (bc_factor(pp * (1 + 1e-4), E * Iy, L, a, x) - c) / 1e-4 * u_P]
        return math.sqrt(sum(v * v for v in d))
    u_gf_ratio = math.sqrt(2 / 10) * u_gf * math.sqrt(2)            # random gage-factor errors, averaged over 10 gages
    u_Cmid_m = Cmid_m[k] * math.sqrt(u_gf_ratio ** 2 + (u_hole / e_z) ** 2 + (ub / b) ** 2 + (1.5 / math.sqrt(10) / bd[k]) ** 2)
    u_Cend_m = Cend_m[k] * math.sqrt(2 * u_gf ** 2 + (u_hole / e_z) ** 2 + (ub / b) ** 2)
    u_w_m = math.hypot(w[k] * m["lvdt_accuracy_pct"] / 100 / R3, m["lvdt_resolution_mm"] / R3)
    u_w_p = math.hypot(u_hole * (1 - Cmid_p[k]), e_z * uC_of(P[k]))

    # EI from the w(P) data (Challenge C2)
    def resid(EI):
        return np.array([wi - e_z * (1 - bc_factor(pp, EI, L, a)) for pp, wi in zip(P, w)])
    sol = optimize.least_squares(lambda v: resid(v[0] * 1e8), [E * Iy / 1e8])
    EI_fit = sol.x[0] * 1e8
    J = sol.jac
    s2 = float(sol.fun @ sol.fun) / max(len(P) - 1, 1)
    u_EI_stat = math.sqrt(s2 / (J.T @ J).item()) * 1e8
    dEI_de = (optimize.least_squares(lambda v: np.array([wi - (e_z + 0.01) * (1 - bc_factor(pp, v[0] * 1e8, L, a)) for pp, wi in zip(P, w)]),
                                     [EI_fit / 1e8]).x[0] * 1e8 - EI_fit) / 0.01
    dEI_dg = (optimize.least_squares(lambda v: np.array([wi * 1.001 - e_z * (1 - bc_factor(pp, v[0] * 1e8, L, a)) for pp, wi in zip(P, w)]),
                                     [EI_fit / 1e8]).x[0] * 1e8 - EI_fit) / 0.001
    dEI_da = (optimize.least_squares(lambda v: np.array([wi - e_z * (1 - bc_factor(pp, v[0] * 1e8, L, a + 0.5)) for pp, wi in zip(P, w)]),
                                     [EI_fit / 1e8]).x[0] * 1e8 - EI_fit) / 0.5
    u_EI_fit = math.sqrt(u_EI_stat ** 2 + (dEI_de * u_hole) ** 2 + (dEI_dg * m["lvdt_accuracy_pct"] / 100 / R3) ** 2 + (dEI_da * ua) ** 2)
    EI_ref = E * Iy
    u_EI_ref = EI_ref * math.hypot(uE, 3 * ub / b)
    # load where Eq. 4.50 overestimates the mid-length bending moment by 5 % (tension): 1/C = 1.05
    P5_weak = optimize.brentq(lambda pp: 1 / bc_factor(pp, E * Iy, L, a) - 1.05, 1.0, 1e6)
    P5_strong = optimize.brentq(lambda pp: 1 / bc_factor(pp, E * Iz, L, a) - 1.05, 1.0, 1e8)
    out["C"] = dict(P=P.tolist(), ax=ax.tolist(), bd=bd.tolist(), ax_end=ax_end.tolist(), bd_end=bd_end.tolist(), e=e_z, x_end=xe,
                    Cmid_m=Cmid_m.tolist(), Cend_m=Cend_m.tolist(), Cmid_p=Cmid_p.tolist(), Cend_p=Cend_p.tolist(), w=w.tolist(), w_p=w_p.tolist(),
                    u_Cmid_m=u_Cmid_m, u_Cmid_p=uC_of(P[k]), u_Cend_m=u_Cend_m, u_Cend_p=uC_of(P[k], xe), u_w_m=u_w_m, u_w_p=u_w_p,
                    agree_mid=2 * math.hypot(u_Cmid_m, uC_of(P[k])), agree_end=2 * math.hypot(u_Cend_m, uC_of(P[k], xe)),
                    agree_w=2 * math.hypot(u_w_m, u_w_p),
                    err450_mid_pct=100 * (1 / Cmid_m[k] - 1), err450_mid_pred_pct=100 * (1 / Cmid_p[k] - 1),
                    sig_front_450=P[k] / A * (1 + 6 * e_z / b), sig_front_mid=E * 1e-6 * (ax[k] + bd[k]), sig_front_end=E * 1e-6 * (ax_end[k] + bd_end[k]),
                    sig_back_450=P[k] / A * (1 - 6 * e_z / b), sig_back_mid=E * 1e-6 * (ax[k] - bd[k]),
                    EI_fit=EI_fit, u_EI_fit=u_EI_fit, EI_ref=EI_ref, u_EI_ref=u_EI_ref, agree_EI=2 * math.hypot(u_EI_fit, u_EI_ref),
                    P5_weak=P5_weak, P5_strong=P5_strong, P5w_over_PE=P5_weak / out["bar"]["PEb_weak"], P5s_over_PE=P5_strong / out["bar"]["PEb_strong"],
                    PA_check=P[k] / A, sig_ax=E * 1e-6 * ax[k])
    # ------------------------------------------------------------------ Part B: angle
    am = m["angle"]
    bV, ubV = mean_u(am["bV_mm"], m["caliper_accuracy_mm"])
    bH, ubH = mean_u(am["bH_mm"], m["caliper_accuracy_mm"])
    t, ut = mean_u(am["t_mm"], m["micrometer_accuracy_mm"])
    zL, yL = am["load_z_mm"], am["load_y_mm"]
    gnames = list(am["gages_mm"])
    gpos = [(am["gages_mm"][g]["z"], am["gages_mm"][g]["y"]) for g in gnames]
    rr = loading(sel(rows, "B", "angle"))
    P = np.array([r["load_N"] for r in rr])
    Pmax = 30e3

    def predict(bV_, bH_, t_, r_, zL_, yL_, gp, naive=False, bc=False):
        sec = LM.angle(bV_, bH_, t_, r_)
        pr = LM.props(sec)
        yP, zP = yL_ - pr["yc"], zL_ - pr["zc"]
        if not bc:
            return [LM.stress(pr, Pmax, yP, zP, y - pr["yc"], z - pr["zc"], naive=naive) for (z, y) in gp], pr
        w_, V_ = np.linalg.eigh(pr["S"])
        e_ = np.array([yP, zP])
        res = []
        for (z, y) in gp:
            r_ = np.array([y - pr["yc"], z - pr["zc"]])
            s = Pmax / pr["A"]
            for kk in range(2):
                d = V_[:, kk]
                s += Pmax * float(d @ e_) * bc_factor(Pmax, E * w_[kk], am["L_mm"], am["a_mm"]) * float(d @ r_) / w_[kk]
            res.append(s)
        return res, pr
    base, prB = predict(bV, bH, t, 0.0, zL, yL, gpos)
    naive, _ = predict(bV, bH, t, 0.0, zL, yL, gpos, naive=True)
    fil, prF = predict(bV, bH, t, am["r_mm"], zL, yL, gpos)
    filbc, _ = predict(bV, bH, t, am["r_mm"], zL, yL, gpos, bc=True)
    # prediction uncertainty: dimensions, load point, gage positions (finite-difference sensitivities)
    u_pos = m["gage_position_accuracy_mm"] / R3
    sens = []
    for dv, uv in ((dict(bV_=bV + 0.01), ubV), (dict(bH_=bH + 0.01), ubH), (dict(t_=t + 0.001), ut), (dict(zL_=zL + 0.01), u_hole),
                   (dict(yL_=yL + 0.01), u_hole)):
        kw = dict(bV_=bV, bH_=bH, t_=t, r_=0.0, zL_=zL, yL_=yL, gp=gpos)
        step = list(dv.values())[0] - kw[list(dv)[0]]
        kw.update(dv)
        s2_, _ = predict(**kw)
        sens.append([(s2_[i] - base[i]) / step * uv for i in range(4)])
    u_pred = []
    for i, (z, y) in enumerate(gpos):
        gp2 = list(gpos)
        gp2[i] = (z + (0.01 if abs(y) < 1e-9 else 0.0), y + (0.01 if abs(y) > 1e-9 else 0.0))
        s2_, _ = predict(bV, bH, t, 0.0, zL, yL, gp2)
        dpos = (s2_[i] - base[i]) / 0.01 * u_pos
        u_pred.append(math.sqrt(sum(sv[i] ** 2 for sv in sens) + dpos ** 2))
    meas, u_meas = [], []
    for i in range(4):
        _, sl, _, usl, _ = linfit(P, [r[GAGES[i]] for r in rr])       # microstrain per N
        sm = E * sl * 1e-6 * Pmax
        meas.append(sm)
        u_meas.append(abs(sm) * math.sqrt(uE ** 2 + u_gf ** 2 + u_P ** 2 + (usl / sl) ** 2))
    # neutral axis from the four gages (plane fit) vs prediction
    G = np.array([[1, y - prB["yc"], z - prB["zc"]] for (z, y) in gpos])
    cfit = np.linalg.lstsq(G, np.array(meas), rcond=None)[0]
    phi_meas = math.degrees(math.atan2(-cfit[2], cfit[1]))
    yPb, zPb = yL - prB["yc"], zL - prB["zc"]
    phi_pred = math.degrees(LM.na_angle(prB, Pmax, yPb, zPb))
    hullB = LM.to_centroidal(prB, LM.angle(bV, bH, t)["hull"])
    sig_hull = [LM.stress(prB, Pmax, yPb, zPb, y, z) for (y, z) in hullB]
    w_, V_ = np.linalg.eigh(prB["S"])
    kernB, kernB_area = LM.kern(prB, hullB)
    out["B"] = dict(bV=bV, ubV=ubV, bH=bH, ubH=ubH, t=t, ut=ut, A=prB["A"], yc=prB["yc"], zc=prB["zc"], Iz=prB["Iz"], Iy=prB["Iy"], Iyz=prB["Iyz"],
                    Imax=prB["Imax"], Imin=prB["Imin"], yP=yPb, zP=zPb, uP=float(V_[:, 0] @ np.array([yPb, zPb])), vP=float(V_[:, 1] @ np.array([yPb, zPb])),   # u along the major axis (eigenvector of the least spread)
                    A_fil=prF["A"], Imin_fil=prF["Imin"], gages=gnames, gpos=gpos, meas=meas, u_meas=u_meas, pred=base, u_pred=u_pred, naive=naive, fil=fil,
                    filbc=filbc, agree=[2 * math.hypot(a_, b_) for a_, b_ in zip(u_meas, u_pred)], Pmax=Pmax, PA=Pmax / prB["A"],
                    phi_meas=phi_meas, phi_pred=phi_pred, sig_hull=sig_hull, sig_max=max(sig_hull), sig_min=min(sig_hull),
                    C_minor=bc_factor(Pmax, E * w_[0], am["L_mm"], am["a_mm"]), C_major=bc_factor(Pmax, E * w_[1], am["L_mm"], am["a_mm"]),
                    kern_area=kernB_area, L=am["L_mm"], a=am["a_mm"], r=am["r_mm"])
    # ------------------------------------------------------------------ D1: single-angle brace
    sa = D1["sa_frac"] * sY
    des = []
    for name, bv, bh, tt, g in CATALOG:
        sec = LM.angle(bv, bh, tt)
        pr = LM.props(sec)
        yP, zP = -D1["tg"] * 1e3 / 2 - pr["yc"], -g - pr["zc"]
        hull = LM.to_centroidal(pr, sec["hull"])
        T = D1["T"]
        s458 = [LM.stress(pr, T, yP, zP, y, z) for (y, z) in hull]
        w2, V2 = np.linalg.eigh(pr["S"])
        e2 = np.array([yP, zP])

        def sbc(which):
            vals = []
            for (y, z) in hull:
                s = T / pr["A"]
                for kk in range(2):
                    d = V2[:, kk]
                    x = D1["L"] * 1e3 / 2 if which == "mid" else 0.0
                    s += T * float(d @ e2) * bc_factor(T, E * w2[kk], D1["L"] * 1e3, D1["a"] * 1e3, x) * float(d @ np.array([y, z])) / w2[kk]
                vals.append(s)
            return max(vals)
        des.append(dict(name=name, A=pr["A"], mass=pr["A"] * 1e-6 * RHO, PA=T / pr["A"], s458=max(s458), smin458=min(s458), send=sbc("end"),
                        smid=sbc("mid"), ok_naive=T / pr["A"] <= sa, ok=max(s458) <= sa, ratio=max(s458) / (T / pr["A"])))
    ok = [d for d in des if d["ok"]]
    best = min(ok, key=lambda d: (round(d["mass"], 3), d["s458"]))
    naive_best = min([d for d in des if d["ok_naive"]], key=lambda d: d["mass"])
    out["D1"] = dict(D1, sa=sa, table=des, best=best["name"], naive_best=naive_best["name"])
    return out


def main():
    data = sys.argv[1] if len(sys.argv) > 1 else LAB / "sample_data.csv"
    meas = sys.argv[2] if len(sys.argv) > 2 else HERE / "specimen_measurements.json"
    res = analyze(load(data), json.loads(Path(meas).read_text()))
    (HERE / "results.json").write_text(json.dumps(res, indent=1, default=float))
    A, B, C = res["A"], res["B"], res["C"]
    for cfg in ("e0", "e1", "e2"):
        r = A[cfg]
        print(f"A {cfg}: e_eff {r['e_eff_max']:.3f}±{r['u_e_eff']:.3f} hole {r['e_hole']:.2f} pred_bc {r['pred_bc']:.3f}±{r['u_pred_bc']:.3f} "
              f"(lim {r['agree_bc']:.3f}); sig0 {r['sig0']:.2f}±{r['u_sig0']:.2f} vs P/A {r['PA']:.2f}; yNA {r['yNA']:.2f} pred {r['yNA_pred']:.2f}/{r['yNA_pred_bc']:.2f}; "
              f"bend_z {r['pct_bend_z']:.2f}% ez {r['ez_eff']:.3f}; C {r['C']:.4f}" + (f"; trend {r['trend']}" if "trend" in r else ""))
    print("C:", {k: (round(v, 4) if isinstance(v, float) else v) for k, v in C.items() if not isinstance(v, list)})
    print("C Cmid_m", np.round(C["Cmid_m"], 4), "Cmid_p", np.round(C["Cmid_p"], 4))
    print("C Cend_m", np.round(C["Cend_m"], 4), "Cend_p", np.round(C["Cend_p"], 4))
    print("C w", C["w"], np.round(C["w_p"], 3))
    print("B meas", np.round(B["meas"], 2), "u", np.round(B["u_meas"], 2))
    print("B pred", np.round(B["pred"], 2), "u", np.round(B["u_pred"], 2), "naive", np.round(B["naive"], 2), "fil", np.round(B["fil"], 2), "filbc", np.round(B["filbc"], 2))
    print("B phi meas/pred", B["phi_meas"], B["phi_pred"], "sig max/min", B["sig_max"], B["sig_min"], "C", B["C_minor"], B["C_major"])
    for d in res["D1"]["table"]:
        print(f"D1 {d['name']:38s} A {d['A']:7.1f} m {d['mass']:.2f} P/A {d['PA']:6.1f} s458 {d['s458']:6.1f} end {d['send']:6.1f} mid {d['smid']:6.1f} ok {d['ok']}")
    print("D1 best", res["D1"]["best"], "naive", res["D1"]["naive_best"], "sa", res["D1"]["sa"])


if __name__ == "__main__":
    main()

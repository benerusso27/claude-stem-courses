"""Lab 8 analysis: every number in the instructor key comes from this script.

    python3 lab08_analysis.py [data.csv] [measurements.json]   ->  results.json + printed summary

Method. Readings are corrected for transverse sensitivity (rectangular-rosette formulas) and reduced with Beer
Eq. 7.43; each component is fitted against the load F (Parts A, B, C combined) or the pressure p (Part C) by least
squares. Rosette H is found to be turned by beta_H from the apparent shear strain under the uniaxial stress of Part A;
rosette K's turn beta_K from the torsion-only state (Part B minus Part A), which is pure shear. Strains are turned
back by these angles, converted to stresses with Lab 2's E and nu (plane stress), and compared with beam and
thick-wall (Lame) theory using the measured dimensions. Uncertainties are propagated by Monte Carlo (GUM
Supplement 1): every input is drawn from its distribution and the whole chain is re-evaluated, which keeps the
correlations between quantities that share inputs.
"""
import csv
import json
import math
import sys
from pathlib import Path

import numpy as np

import lab08_model as LM

HERE = Path(__file__).resolve().parent
LAB = HERE.parent
R3 = math.sqrt(3)
NMC = 4000
GAGES = [f"{g}{c}_ue" for g in ("H", "K") for c in "abc"]

# D1: pressurized swivel arm (Table 6 of the handout)
D1 = dict(p=20e6, T=300.0, M=300.0, n=1.8, twist_lim_deg_per_m=3.0, OD_max=50.8)
CATALOG = [(31.75, 3.18), (31.75, 4.78), (38.1, 2.11), (38.1, 3.18), (38.1, 4.78), (44.45, 2.11), (44.45, 3.18), (44.45, 4.78),
           (50.8, 2.11), (50.8, 3.18), (50.8, 4.78)]
RHO_AL = 2700.0


def load(path):
    rows = list(csv.DictReader(open(path, newline="")))
    keep = ("part", "config")
    return [{k: (v if k in keep else float(v)) for k, v in r.items()} for r in rows]


def sel(rows, part, config):
    return [r for r in rows if r["part"] == part and r["config"] == config]


def linfit(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    A = np.vstack([np.ones(len(x)), x]).T
    coef, *_ = np.linalg.lstsq(A, y, rcond=None)
    res = y - A @ coef
    s2 = res @ res / max(len(x) - 2, 1)
    cov = s2 * np.linalg.inv(A.T @ A)
    return coef[1], math.sqrt(cov[1, 1]), coef[0]


def mean_u(vals, acc):
    v = np.array(vals, float)
    return float(v.mean()), math.sqrt((v.std(ddof=1) / math.sqrt(len(v))) ** 2 + (acc / R3) ** 2)


def kt_rect(ea, eb, ec, Kt, nu0):
    """Transverse-sensitivity correction for a rectangular rosette (gage b's transverse direction is 135 deg,
    whose strain is ea + ec - eb)."""
    c = 1 - nu0 * Kt
    xa = c * (ea - Kt * ec) / (1 - Kt ** 2)
    xc = c * (ec - Kt * ea) / (1 - Kt ** 2)
    xb = (c * eb - Kt * (xa + xc)) / (1 - Kt)
    return xa, xb, xc


def reduce(ea, eb, ec):
    return ea, ec, 2 * eb - ea - ec                                # Beer Eq. 7.43


def turn(ex, ey, g, b):
    """Components on axes turned by b (ccw), Beer Eqs. 7.44, 7.45, 7.49."""
    a, d = (ex + ey) / 2, (ex - ey) / 2
    return a + d * math.cos(2 * b) + g / 2 * math.sin(2 * b), a - d * math.cos(2 * b) - g / 2 * math.sin(2 * b), -2 * d * math.sin(2 * b) + g * math.cos(2 * b)


def mohr(sx, sy, t):
    ave, R = (sx + sy) / 2, math.hypot((sx - sy) / 2, t)
    return ave + R, ave - R, 0.5 * math.atan2(t, (sx - sy) / 2), R


def tube(Do, t):
    ro = Do / 2
    ri = ro - t
    I = math.pi * (ro ** 4 - ri ** 4) / 4
    return ro, ri, I, 2 * I, (ro ** 3 - ri ** 3) / 3


def derive(I_):
    """Every result from one set of inputs (slopes in strain per N or per Pa, dimensions in m, moduli in Pa)."""
    o = {}
    sl, Do, t, Lb, aL = I_["sl"], I_["Do"], I_["t"], I_["Lb"], I_["aL"]
    E2, nu2 = I_["E2"], I_["nu2"]
    G2 = E2 / (2 * (1 + nu2))
    ro, ri, I, J, Qna = tube(Do, t)
    kF, kp = I_["kF"], I_["kp"]                                    # true load = reading / kF
    cg = I_["cg"]                                                  # indicated strain = true * cg

    def comp(cfg, g):
        a, b, c = (sl[(cfg, f"{g}{x}_ue")] / cg / I_["gi"][f"{g}{x}_ue"] for x in "abc")
        a, b, c = kt_rect(a, b, c, I_["Kt"], I_["nu0"])
        return reduce(a, b, c)
    # --- Part A: rosette H under uniaxial stress -> beta_H, E, nu
    exA, eyA, gA = comp("axis", "H")
    bH = -0.5 * math.asin(gA / (exA - eyA))
    exA, eyA, gA = turn(exA, eyA, gA, -bH)
    sxA = kF * Lb * ro / I                                          # stress per (indicated) newton
    o["E_A"] = sxA / exA
    o["nu_A"] = -eyA / exA
    o["beta_H"] = math.degrees(bH)
    # --- torsion only (B - A) at H and K: G, and beta_K
    exB, eyB, gB = comp("lever", "H")
    exBt, eyBt, gBt = turn(exB, eyB, gB, -bH)
    gT_H = gBt - gA
    kxA, kyA, kgA = comp("axis", "K")
    kxB, kyB, kgB = comp("lever", "K")
    dx, dy, dg = kxB - kxA, kyB - kyA, kgB - kgA                   # pure shear seen by a turned rosette
    bK = 0.5 * math.atan((dx - dy) / dg)                              # tan 2b = (ex'' - ey'')/g'' for pure shear
    o["beta_K"] = math.degrees(bK)
    kxA, kyA, kgA = turn(kxA, kyA, kgA, -bK)
    kxB, kyB, kgB = turn(kxB, kyB, kgB, -bK)
    gT_K = kgB - kgA
    tauT = kF * aL * ro / J                                         # per indicated newton
    o["G_H"] = -tauT / gT_H
    o["G_K"] = -tauT / gT_K
    o["G_A"] = o["E_A"] / (2 * (1 + o["nu_A"]))
    o["G_mean"] = (o["G_H"] + o["G_K"]) / 2
    # K position: bending strain leaking into K (Part A), relative to H
    o["phiK_off"] = math.degrees(math.asin(max(-1.0, min(1.0, kxA / exA))))
    # transverse shear at K under the axis load
    tauV = kF * Qna / (I * (ro - ri))
    o["gK_A_meas"] = kgA
    o["gK_A_pred"] = -tauV / G2
    o["tauV_meas"] = -kgA * G2
    o["tauV_pred"] = tauV
    # --- Part B at 600 N: stresses from strains (Lab 2 E, nu), principal values vs beam theory
    F = 600.0
    for g, (ex, ey, gg), phi in (("H", (exBt, eyBt, gBt), 0.0), ("K", (kxB, kyB, kgB), math.pi / 2)):
        sx, sy, txy = LM.hooke_plane_stress(ex * F, ey * F, gg * F, E2, nu2)
        s1, s2, th, R = mohr(sx, sy, txy)
        Ft = F * kF
        st = dict(sx=Ft * Lb * ro * math.cos(phi) / I, sy=0.0, txy=-(Ft * aL * ro / J + Ft * Qna * math.sin(phi) / (I * (ro - ri))))
        p1, p2, pth, pR = mohr(st["sx"], st["sy"], st["txy"])
        o.update({f"B{g}_sx": sx, f"B{g}_sy": sy, f"B{g}_txy": txy, f"B{g}_s1": s1, f"B{g}_s2": s2, f"B{g}_th": math.degrees(th), f"B{g}_R": R,
                  f"B{g}_sx_p": st["sx"], f"B{g}_txy_p": st["txy"], f"B{g}_s1_p": p1, f"B{g}_s2_p": p2, f"B{g}_th_p": math.degrees(pth), f"B{g}_R_p": pR,
                  f"B{g}_ex": ex * F, f"B{g}_ey": ey * F, f"B{g}_g": gg * F})
        for k in ("s1", "s2", "th", "R"):
            o[f"B{g}_d{k}"] = o[f"B{g}_{k}"] - o[f"B{g}_{k}_p"]
        o[f"B{g}_dtxy"] = txy - st["txy"]
        o[f"B{g}_dsx"] = sx - st["sx"]
    # Part A at 600 N (stresses from the turned-back strains, Lab 2 E and nu)
    for g, (ex, ey, gg) in (("H", (exA, eyA, gA)), ("K", (kxA, kyA, kgA))):
        sx, sy, txy = LM.hooke_plane_stress(ex * F, ey * F, gg * F, E2, nu2)
        s1, s2, th, R = mohr(sx, sy, txy)
        o.update({f"A{g}_s1": s1, f"A{g}_s2": s2, f"A{g}_sx": sx, f"A{g}_txy": txy})
    # uncorrected (no turn-back) principal direction and tau at H, for M1
    sxu, syu, tu = LM.hooke_plane_stress(exB * F, eyB * F, gB * F, E2, nu2)
    o["BH_txy_unturned"] = tu
    o["BH_sx_unturned"] = sxu
    o["BH_th_unturned"] = math.degrees(mohr(sxu, syu, tu)[2])
    # --- Part C: pressure (per MPa of indicated pressure)
    A_l = ri ** 2 / (ro ** 2 - ri ** 2)                             # Lame A / p
    for g, b in (("H", bH), ("K", bK)):
        ex, ey, gg = comp("pressure", g)
        ex, ey, gg = turn(ex, ey, gg, -b)
        r = ex / ey
        o[f"C{g}_nu"] = (0.5 - r) / (1 - 0.5 * r)
        sx, sy, _ = LM.hooke_plane_stress(ex * 1e6, ey * 1e6, 0.0, E2, nu2)
        o[f"C{g}_sth"] = sy / kp                                    # per MPa of true pressure (true p = indicated * kp)
        o[f"C{g}_sx"] = sx / kp
        o[f"C{g}_ex"], o[f"C{g}_ey"], o[f"C{g}_g"] = ex * 1e6, ey * 1e6, gg * 1e6
        s8 = LM.hooke_plane_stress(ex * 8e6, ey * 8e6, gg * 8e6, E2, nu2)
        m8 = mohr(*s8)
        o[f"C{g}_s1"], o[f"C{g}_s2"] = m8[0], m8[1]
    o["C_sth"] = (o["CH_sth"] + o["CK_sth"]) / 2
    o["C_sx"] = (o["CH_sx"] + o["CK_sx"]) / 2
    o["C_nu"] = (o["CH_nu"] + o["CK_nu"]) / 2
    o["C_sth_lame"], o["C_sx_lame"] = 2 * A_l * 1e6, A_l * 1e6
    o["C_sth_thin"], o["C_sx_thin"] = ri / t * 1e6, ri / (2 * t) * 1e6
    o["C_dsth_lame"] = o["C_sth"] - o["C_sth_lame"]
    o["C_dsth_thin"] = o["C_sth"] - o["C_sth_thin"]
    o["C_dsx_lame"] = o["C_sx"] - o["C_sx_lame"]
    o["C_dsx_thin"] = o["C_sx"] - o["C_sx_thin"]
    o["C_dnu"] = o["C_nu"] - nu2
    # --- Part C combined: 8 MPa (indicated) + 600 N on the lever, at H and K
    for g, b, phi in (("H", bH, 0.0), ("K", bK, math.pi / 2)):
        px, py, pg = comp("pressure", g)
        fx, fy, fg = comp("comb", g)
        ex, ey, gg = turn(px * 8e6 + fx * F, py * 8e6 + fy * F, pg * 8e6 + fg * F, -b)
        sx, sy, txy = LM.hooke_plane_stress(ex, ey, gg, E2, nu2)
        s1, s2, th, R = mohr(sx, sy, txy)
        tabs = (max(s1, s2, 0.0) - min(s1, s2, 0.0)) / 2
        Ft, pt = F * kF, 8e6 * kp
        st = dict(sx=Ft * Lb * ro * math.cos(phi) / I + pt * A_l, sy=2 * pt * A_l, txy=-(Ft * aL * ro / J + Ft * Qna * math.sin(phi) / (I * (ro - ri))))
        p1, p2, pth, pR = mohr(st["sx"], st["sy"], st["txy"])
        pabs = (max(p1, p2, 0.0) - min(p1, p2, 0.0)) / 2
        o.update({f"X{g}_sx": sx, f"X{g}_sy": sy, f"X{g}_txy": txy, f"X{g}_s1": s1, f"X{g}_s2": s2, f"X{g}_R": R, f"X{g}_tabs": tabs,
                  f"X{g}_s1_p": p1, f"X{g}_s2_p": p2, f"X{g}_R_p": pR, f"X{g}_tabs_p": pabs, f"X{g}_th": math.degrees(th),
                  f"X{g}_vm": math.sqrt(s1 ** 2 - s1 * s2 + s2 ** 2)})
        for k in ("s1", "s2", "R", "tabs"):
            o[f"X{g}_d{k}"] = o[f"X{g}_{k}"] - o[f"X{g}_{k}_p"]
    o["XH_ratio"] = o["XH_tabs"] / o["XH_R"]
    # --- E and nu without the transverse-sensitivity correction (M1)
    a, b_, c = (sl[("axis", f"H{x}_ue")] / cg / I_["gi"][f"H{x}_ue"] for x in "abc")
    ex0, ey0, g0 = reduce(a, b_, c)
    b0 = -0.5 * math.asin(g0 / (ex0 - ey0))
    ex0, ey0, _ = turn(ex0, ey0, g0, -b0)
    o["E_A_noKt"] = sxA / ex0
    o["nu_A_noKt"] = -ey0 / ex0
    # Part C hoop strain at H without the K_t correction, relative to corrected
    a, b_, c = (sl[("pressure", f"H{x}_ue")] / cg / I_["gi"][f"H{x}_ue"] for x in "abc")
    o["C_ey_noKt_ratio"] = reduce(a, b_, c)[1] / comp("pressure", "H")[1]
    o["C_ex_noKt_ratio"] = reduce(a, b_, c)[0] / comp("pressure", "H")[0]
    # C2: the tube as a load cell (Part B at 600 N indicated): F from the transverse shear, then the arms
    tH, tK = -o["BH_txy"], -o["BK_txy"]
    q1 = Qna / (I * (ro - ri))                                      # tau_V per newton at K
    Fe = (tK - tH) / q1
    o["C2_F"] = Fe
    o["C2_aL"] = tH * J / (Fe * ro)
    o["C2_Lb"] = o["BH_sx"] * I / (Fe * ro)
    o["C2_FLb"] = o["BH_sx"] * I / ro                               # F*Lb from the bending strain alone
    o["C2_FaL"] = tH * J / ro
    return o


def analyze(rows, m, nmc=NMC, seed=7):
    tb = m["tube"]
    Do, uDo = mean_u(tb["Do_mm"], m["micrometer_accuracy_mm"])
    t, ut = mean_u(tb["t_mm"], m["ball_micrometer_accuracy_mm"])
    u_rule = m["rule_accuracy_mm"] / R3
    ref = m["reference"]
    ros = m["rosette"]
    # slopes of every gage in every configuration
    sl, usl = {}, {}
    cfgs = {"axis": ("A", "axis", "load_N"), "lever": ("B", "lever", "load_N"), "pressure": ("C", "pressure", "p_MPa"), "comb": ("C", "combined", "load_N")}
    for k, (part, cfg, xc) in cfgs.items():
        rr = sel(rows, part, cfg)
        x = np.array([r[xc] for r in rr]) * (1e6 if xc == "p_MPa" else 1.0)
        for gname in GAGES:
            y = np.array([r[gname] for r in rr]) * 1e-6
            s, us, _ = linfit(x, y)
            # the strain indicator's resolution (1 microstrain) is already in the scatter
            sl[(k, gname)], usl[(k, gname)] = s, us
    nominal = dict(sl=sl, Do=Do * 1e-3, t=t * 1e-3, Lb=tb["Lb_mm"] * 1e-3, aL=tb["aL_mm"] * 1e-3, E2=ref["E_al_GPa"] * 1e9, nu2=ref["nu_al"],
                   kF=1.0, kp=1.0, cg=1.0, gi={g_: 1.0 for g_ in GAGES}, Kt=ros["Kt"], nu0=ros["nu0"])
    res = derive(nominal)
    rng = np.random.default_rng(seed)
    samples = {k: [] for k in res}
    for _ in range(nmc):
        I_ = dict(nominal)
        I_["sl"] = {k: v + usl[k] * rng.standard_normal() for k, v in sl.items()}
        I_["Do"] = (Do + uDo * rng.standard_normal()) * 1e-3
        I_["t"] = (t + ut * rng.standard_normal()) * 1e-3
        I_["Lb"] = (tb["Lb_mm"] + u_rule * rng.standard_normal()) * 1e-3
        I_["aL"] = (tb["aL_mm"] + u_rule * rng.standard_normal()) * 1e-3
        I_["E2"] = (ref["E_al_GPa"] + ref["u_E_al_GPa"] * rng.standard_normal()) * 1e9
        I_["nu2"] = ref["nu_al"] + ref["u_nu_al"] * rng.standard_normal()
        I_["kF"] = 1 + m["loadcell_accuracy_pct"] / 100 / R3 * rng.standard_normal()
        I_["kp"] = 1 + m["p_accuracy_MPa"] / R3 / 8.0 * rng.standard_normal()
        I_["cg"] = 1 + ros["GF_tol_pct"] / 100 / R3 * rng.standard_normal()
        I_["gi"] = {g_: 1 + m["strain_accuracy_pct"] / 100 / R3 * rng.standard_normal() for g_ in GAGES}
        I_["Kt"] = ros["Kt"] + 0.002 / R3 * rng.standard_normal()
        o = derive(I_)
        for k in samples:
            samples[k].append(o[k])
    unc = {k: float(np.std(v, ddof=1)) for k, v in samples.items()}
    out = dict(Do=Do, uDo=uDo, t=t, ut=ut, Di=Do - 2 * t, res={k: float(v) for k, v in res.items()}, u=unc,
               slopes={f"{k[0]}|{k[1]}": v for k, v in sl.items()}, uslopes={f"{k[0]}|{k[1]}": v for k, v in usl.items()})
    ro, ri, I, J, Qna = tube(Do * 1e-3, t * 1e-3)
    out["props"] = dict(ro=ro, ri=ri, I=I, J=J, Q=Qna, A=math.pi * (ro ** 2 - ri ** 2), ri_over_t=ri / (t * 1e-3))
    # --- D1: lightest tube of the catalog
    sY = ref["sY_al_MPa"] * 1e6
    G3 = ref["G_al_GPa"] * 1e9
    table = []
    for OD, wt in CATALOG:
        ro_, ri_ = OD / 2e3, OD / 2e3 - wt / 1e3
        I_, J_ = math.pi * (ro_ ** 4 - ri_ ** 4) / 4, math.pi * (ro_ ** 4 - ri_ ** 4) / 2
        A_ = D1["p"] * ri_ ** 2 / (ro_ ** 2 - ri_ ** 2)
        B_ = A_ * ro_ ** 2
        pts = []
        for where, r in (("outer", ro_), ("inner", ri_)):
            for side, sg in (("tension side", 1), ("compression side", -1)):
                sx = A_ + sg * D1["M"] * r / I_
                st = A_ + B_ / r ** 2
                sr = A_ - B_ / r ** 2
                tau = D1["T"] * r / J_
                pr = LM.principal3([[sx, tau, 0], [tau, st, 0], [0, 0, sr]])
                tin = math.hypot((sx - st) / 2, tau)
                pts.append(dict(where=where, side=side, sx=sx, st=st, sr=sr, tau=tau, p=list(map(float, pr)), tabs=(pr[0] - pr[2]) / 2, tin=tin, vm=LM.von_mises(pr)))
        w = max(pts, key=lambda q: q["tabs"])
        wi = max(pts, key=lambda q: q["tin"])
        wv = max(pts, key=lambda q: q["vm"])
        twist = math.degrees(D1["T"] / (G3 * J_))
        mass = math.pi * (ro_ ** 2 - ri_ ** 2) * RHO_AL
        sf_t, sf_in, sf_vm = sY / (2 * w["tabs"]), sY / (2 * wi["tin"]), sY / wv["vm"]
        table.append(dict(name=f"{OD} × {wt}", OD=OD, t=wt, mass=mass, sf_tresca=sf_t, sf_inplane=sf_in, sf_vm=sf_vm, twist=twist, crit=w, crit_vm=wv,
                          ok=bool(sf_t >= D1["n"] and twist <= D1["twist_lim_deg_per_m"] and OD <= D1["OD_max"]),
                          ok_inplane=bool(sf_in >= D1["n"] and twist <= D1["twist_lim_deg_per_m"]), ok_vm=bool(sf_vm >= D1["n"] and twist <= D1["twist_lim_deg_per_m"]),
                          ok_stress_only=bool(sf_t >= D1["n"])))
    byw = sorted(table, key=lambda d: d["mass"])
    out["D1"] = dict(D1, sY=sY / 1e6, G=G3 / 1e9, table=table, best=next(d["name"] for d in byw if d["ok"]),
                     best_inplane=next(d["name"] for d in byw if d["ok_inplane"]), best_vm=next(d["name"] for d in byw if d["ok_vm"]),
                     best_stress_only=next(d["name"] for d in byw if d["ok_stress_only"]))
    return out


def main():
    data = sys.argv[1] if len(sys.argv) > 1 else LAB / "sample_data.csv"
    meas = sys.argv[2] if len(sys.argv) > 2 else HERE / "specimen_measurements.json"
    out = analyze(load(data), json.loads(Path(meas).read_text()))
    (HERE / "results.json").write_text(json.dumps(out, indent=1, default=float))
    r, u = out["res"], out["u"]
    f = lambda k, s=1.0, nd=3: f"{r[k] * s:.{nd}f} ± {2 * u[k] * s:.{nd}f}"  # noqa: E731
    print("tube Do, t:", round(out["Do"], 4), round(out["t"], 4))
    print("A: E", f("E_A", 1e-9), "GPa; nu", f("nu_A", 1, 4), "; beta_H", f("beta_H", 1, 2), "deg; noKt E", round(r["E_A_noKt"] / 1e9, 3))
    print("G: H", f("G_H", 1e-9), "K", f("G_K", 1e-9), "from E,nu", f("G_A", 1e-9), "; beta_K", f("beta_K", 1, 2), "; phiK off", f("phiK_off", 1, 2))
    print("tauV at K (MPa per 600 N):", f("tauV_meas", 600e-6), "pred", f("tauV_pred", 600e-6))
    for g in "HK":
        print(f"B{g}: sx {r[f'B{g}_sx'] / 1e6:.2f} (pred {r[f'B{g}_sx_p'] / 1e6:.2f}), txy {r[f'B{g}_txy'] / 1e6:.2f} (pred {r[f'B{g}_txy_p'] / 1e6:.2f}),",
              "s1", f(f"B{g}_s1", 1e-6, 2), "pred", round(r[f"B{g}_s1_p"] / 1e6, 2), "diff", f(f"B{g}_ds1", 1e-6, 2), "; s2", f(f"B{g}_s2", 1e-6, 2), "pred",
              round(r[f"B{g}_s2_p"] / 1e6, 2), "; th", f(f"B{g}_th", 1, 2), "pred", round(r[f"B{g}_th_p"], 2))
    print("BH unturned: txy", round(r["BH_txy_unturned"] / 1e6, 2), "th", round(r["BH_th_unturned"], 2))
    print("C: nu", f("C_nu", 1, 4), "; sth per MPa", f("C_sth", 1e-6), "Lame", round(r["C_sth_lame"] / 1e6, 3), "thin", round(r["C_sth_thin"] / 1e6, 3),
          "; sx", f("C_sx", 1e-6), "Lame", round(r["C_sx_lame"] / 1e6, 3), "thin", round(r["C_sx_thin"] / 1e6, 3))
    for g in "HK":
        print(f"X{g}: s1", f(f"X{g}_s1", 1e-6, 2), "pred", round(r[f"X{g}_s1_p"] / 1e6, 2), "; s2", f(f"X{g}_s2", 1e-6, 2), "pred", round(r[f"X{g}_s2_p"] / 1e6, 2),
              "; R", f(f"X{g}_R", 1e-6, 2), "; tabs", f(f"X{g}_tabs", 1e-6, 2), "pred", round(r[f"X{g}_tabs_p"] / 1e6, 2))
    print("D1 best", out["D1"]["best"], "| in-plane mistake", out["D1"]["best_inplane"], "| von Mises", out["D1"]["best_vm"], "| stress only", out["D1"]["best_stress_only"])
    for d in out["D1"]["table"]:
        print(f"   {d['name']}: {d['mass']:.3f} kg/m Tresca {d['sf_tresca']:.2f} in-plane {d['sf_inplane']:.2f} vM {d['sf_vm']:.2f} twist {d['twist']:.2f} crit {d['crit']['where']}/{d['crit']['side']} ok {d['ok']}")


if __name__ == "__main__":
    main()

"""Lab 9 analysis: every number in the instructor key comes from this script.

    python3 lab09_analysis.py [data.csv] [measurements.json]   ->  results.json + printed summary

Method. Each test's mid-length deflection is reduced with a Southwell plot (delta/P against delta, least squares over
the readings with P >= 0.5 P_pred), which gives the critical load and the equivalent initial imperfection without
loading to failure. Euler predictions use Lab 2's E, the measured section and the measured lengths with Beer's ideal
effective lengths (Fig. 10.18). Part B backs the clamps' rotational stiffness out of the fixed-fixed result
(Appendix D.3) and uses it to predict the fixed-pinned test. Part C isolates the eccentric part of the response by
subtracting the Part A readings at the same loads (linear superposition holds at a fixed load) and fits the
eccentricity with the secant result (Eq. 10.31). Part D compares the short column's maximum load with Euler, the
squash load, the tangent- and reduced-modulus loads (Lab 1's Ramberg-Osgood fit) and the Aluminum Association
formula. Uncertainties: first-order propagation, and Monte Carlo (GUM Supplement 1, 4000 draws) where the chain is
nonlinear (the clamp stiffness and the fixed-pinned prediction that uses it).
"""
import csv
import json
import math
import sys
from pathlib import Path

import numpy as np

import lab09_model as LM

HERE = Path(__file__).resolve().parent
LAB = HERE.parent
R3 = math.sqrt(3)
NMC = 4000
PI = math.pi
RHO_AL = 2700.0

# D1: aluminum strut (handout Section 8 and Table 7)
D1 = dict(L=2.0, P=12e3, e=2e-3, FS=1.95, Dt_max=40.0, OD_max=76.2)
CATALOG = [(Do, t) for Do in (44.45, 50.8, 57.15, 63.5, 76.2) for t in (1.65, 2.11, 3.18, 4.78)]


def load(path):
    rows = list(csv.DictReader(open(path, newline="")))
    keep = ("part", "config")
    return [{k: (v if k in keep else (float(v) if v != "" else None)) for k, v in r.items()} for r in rows]


def sel(rows, part, config, L=None, e=None):
    return [r for r in rows if r["part"] == part and r["config"] == config and (L is None or r["L_mm"] == L) and (e is None or r["e_mm"] == e)]


def mean_u(vals, acc, res=0.01):
    v = np.array(vals, float)
    return float(v.mean()), math.sqrt((v.std(ddof=1) / math.sqrt(len(v))) ** 2 + (acc / R3) ** 2 + (res / math.sqrt(12)) ** 2)


def southwell_rows(rows, Ppred, frac=0.5):
    use = [r for r in rows if r["load_N"] >= frac * Ppred and r["defl_mm"] > 0]
    d = np.array([r["defl_mm"] * 1e-3 for r in use])
    P = np.array([r["load_N"] for r in use])
    sw = LM.southwell(d, P)
    sw["n"] = len(use)
    sw["Pmin"] = float(P.min())
    return sw


def main(data=LAB / "sample_data.csv", meas_path=HERE / "specimen_measurements.json"):
    rows = load(data)
    meas = json.loads(Path(meas_path).read_text())
    ref = meas["reference"]
    out = dict()
    # ------------------------------------------------------------------ section and reference values
    b, ub = mean_u(meas["bar"]["b_mm"], meas["micrometer_accuracy_mm"])
    t, ut = mean_u(meas["bar"]["t_mm"], meas["micrometer_accuracy_mm"])
    sec = LM.rect(b * 1e-3, t * 1e-3)
    urI = math.sqrt((ub / b) ** 2 + (3 * ut / t) ** 2)
    urA = math.sqrt((ub / b) ** 2 + (ut / t) ** 2)
    E, uE = ref["E_al_GPa"] * 1e9, ref["u_E_al_GPa"] * 1e9
    urE = uE / E
    EI = E * sec["I"]
    uL = meas["rule_accuracy_mm"] / R3
    ur_lc = meas["loadcell_accuracy_pct"] / 100 / R3
    sY = ref["sY_al_MPa"] * 1e6
    out["geom"] = dict(b=b, ub=ub, t=t, ut=ut, A=sec["A"] * 1e6, urA=urA, I=sec["I"] * 1e12, urI=urI, r=sec["r"] * 1e3, c=sec["c"] * 1e3, EI=EI, urEI=math.hypot(urE, urI))
    # ------------------------------------------------------------------ Part A: pinned, three lengths
    A = {}
    Ls = meas["lengths_mm"]
    for key, Lname in (("300", "A300"), ("450", "A450"), ("600", "A600")):
        L = Ls[Lname] * 1e-3
        rr = sel(rows, "A", "pinned", float(key))
        Pe = LM.euler(E, sec["I"], L)
        urPe = math.sqrt(urE ** 2 + urI ** 2 + (2 * uL / Ls[Lname]) ** 2)
        sw = southwell_rows(rr, Pe)
        uS = math.hypot(sw["uPcr"], sw["Pcr"] * ur_lc)
        ES = sw["Pcr"] * L ** 2 / (PI ** 2 * sec["I"])
        urES = math.sqrt((uS / sw["Pcr"]) ** 2 + urI ** 2 + (2 * uL / Ls[Lname]) ** 2)
        diff = sw["Pcr"] - Pe
        lim = 2 * math.hypot(uS, Pe * urPe)
        bow = meas["bow_mm"][Lname]
        A[key] = dict(L=L, Pe=Pe, uPe=Pe * urPe, PS=sw["Pcr"], uPS=uS, uPS_fit=sw["uPcr"], d0S=sw["delta0"] * 1e3, ud0S=sw["udelta0"] * 1e3,
                      n=sw["n"], Pmin=sw["Pmin"], rms=sw["rms"], diff_pct=100 * diff / Pe, lim_pct=100 * lim / Pe, agree=abs(diff) <= lim,
                      ES=ES / 1e9, uES=ES * urES / 1e9, bow=bow, e_eq=(sw["delta0"] * 1e3 - bow) * PI / 4,
                      slenderness=L / sec["r"], sigma_cr=sw["Pcr"] / sec["A"] / 1e6, Pmax_test=max(r["load_N"] for r in rr),
                      dmax_test=max(r["defl_mm"] for r in rr), ratio_last=max(r["load_N"] for r in rr) / sw["Pcr"])
    out["A"] = A
    lx = np.log([A[k]["L"] for k in A]); ly = np.log([A[k]["PS"] for k in A])
    X = np.column_stack([lx, np.ones(3)])
    coef, *_ = np.linalg.lstsq(X, ly, rcond=None)
    res = ly - X @ coef
    cov = (res @ res / 1) * np.linalg.inv(X.T @ X)
    w = np.array([1 / A[k]["uPS"] ** 2 * A[k]["PS"] ** 2 for k in A])
    out["A_slope"] = dict(slope=coef[0], u=math.sqrt(cov[0, 0]))
    ES_vals = np.array([A[k]["ES"] for k in A])
    ur_rand = np.mean([math.hypot(A[k]["uPS_fit"] / A[k]["PS"], 2 * uL / (A[k]["L"] * 1e3)) for k in A]) / math.sqrt(3)
    uES_mean = ES_vals.mean() * math.sqrt(ur_rand ** 2 + urI ** 2 + ur_lc ** 2)
    out["A_E"] = dict(ES=float(ES_vals.mean()), uES=uES_mean, diff_pct=100 * (ES_vals.mean() * 1e9 - E) / E,
                      lim_pct=200 * math.hypot(uES_mean * 1e9, uE) / E, agree=abs(ES_vals.mean() * 1e9 - E) <= 2 * math.hypot(uES_mean * 1e9, uE))
    # axial strain -> E (average of front and back, loads up to half the prediction)
    xs, ys = [], []
    for key in A:
        for r in sel(rows, "A", "pinned", float(key)):
            if r["load_N"] <= 0.5 * A[key]["Pe"]:
                xs.append(r["load_N"]); ys.append(-(r["eps_front_ue"] + r["eps_back_ue"]) / 2 * 1e-6)
    xs, ys = np.array(xs), np.array(ys)
    Xg = np.column_stack([xs, np.ones_like(xs)])
    cg, *_ = np.linalg.lstsq(Xg, ys, rcond=None)
    rg = ys - Xg @ cg
    ucg = math.sqrt(rg @ rg / (len(xs) - 2) * np.linalg.inv(Xg.T @ Xg)[0, 0])
    Eg = 1 / (sec["A"] * cg[0])
    urEg = math.sqrt((ucg / cg[0]) ** 2 + urA ** 2 + (meas["gage"]["GF_tol_pct"] / 100 / R3) ** 2 + ur_lc ** 2)
    out["A_gage"] = dict(E=Eg / 1e9, uE=Eg * urEg / 1e9, n=len(xs), icpt_ue=cg[1] * 1e6)
    # strain-based Southwell for the 450 mm bar (Challenge): bending strain / P against bending strain
    rr = [r for r in sel(rows, "A", "pinned", 450.0) if r["load_N"] >= 0.5 * A["450"]["Pe"]]
    eb = np.array([(r["eps_front_ue"] - r["eps_back_ue"]) / 2 * 1e-6 for r in rr]); Pp = np.array([r["load_N"] for r in rr])
    swe = LM.southwell(eb, Pp)
    out["A_strainSW"] = dict(PS=swe["Pcr"], uPS=math.hypot(swe["uPcr"], swe["Pcr"] * ur_lc), diff_pct=100 * (swe["Pcr"] / A["450"]["PS"] - 1),
                             eps0=swe["delta0"] * 1e6, n=len(rr))
    # ------------------------------------------------------------------ Part B: clamped ends
    B = {}
    Lff, Lfp = Ls["Bff"] * 1e-3, Ls["Bfp"] * 1e-3
    Pe_ff = LM.euler(E, sec["I"], 0.5 * Lff)
    Pe_fp = LM.euler(E, sec["I"], LM.K_FACTORS["fixed-pinned"] * Lfp)
    sw_ff = southwell_rows(sel(rows, "B", "fixed-fixed"), Pe_ff)
    sw_fp = southwell_rows(sel(rows, "B", "fixed-pinned"), Pe_fp)
    for nm, sw, Pe, L, K0 in (("ff", sw_ff, Pe_ff, Lff, 0.5), ("fp", sw_fp, Pe_fp, Lfp, LM.K_FACTORS["fixed-pinned"])):
        uS = math.hypot(sw["uPcr"], sw["Pcr"] * ur_lc)
        urPe = math.sqrt(urE ** 2 + urI ** 2 + (2 * uL / (L * 1e3)) ** 2)
        K = PI / L * math.sqrt(EI / sw["Pcr"])
        uK = K * 0.5 * math.sqrt((uS / sw["Pcr"]) ** 2 + urE ** 2 + urI ** 2 + (2 * uL / (L * 1e3)) ** 2)
        lim = 2 * math.hypot(uS, Pe * urPe)
        B[nm] = dict(L=L, Pe=Pe, uPe=Pe * urPe, PS=sw["Pcr"], uPS=uS, d0S=sw["delta0"] * 1e3, n=sw["n"], Pmin=sw["Pmin"], K=K, uK=uK, K0=K0,
                     diff_pct=100 * (sw["Pcr"] / Pe - 1), lim_pct=100 * lim / Pe, agree=abs(sw["Pcr"] - Pe) <= lim,
                     Pmax_test=max(r["load_N"] for r in sel(rows, "B", "fixed-fixed" if nm == "ff" else "fixed-pinned")))
    # clamp stiffness from the fixed-fixed test, and the fixed-pinned prediction that uses it (Monte Carlo)
    k0 = LM.k_from_sym(EI, Lff, sw_ff["Pcr"])
    Pfp0 = LM.spring_pin(EI, Lfp, k0)[0]
    rng = np.random.default_rng(9)
    ks, Pfps, ratios = [], [], []
    for _ in range(NMC):
        Ei = E + uE * rng.standard_normal()
        Ii = sec["I"] * (1 + urI * rng.standard_normal())
        g = 1 + ur_lc * R3 * rng.uniform(-1, 1)                        # the load-cell scale error is common to both tests
        Pff = (sw_ff["Pcr"] + sw_ff["uPcr"] * rng.standard_normal()) / g
        Pfp = (sw_fp["Pcr"] + sw_fp["uPcr"] * rng.standard_normal()) / g
        L1 = Lff + uL * 1e-3 * rng.standard_normal(); L2 = Lfp + uL * 1e-3 * rng.standard_normal()
        try:
            kk = LM.k_from_sym(Ei * Ii, L1, Pff)
            if kk <= 0:
                continue
            pp = LM.spring_pin(Ei * Ii, L2, kk)[0]
        except ValueError:
            continue
        ks.append(kk); Pfps.append(pp * g); ratios.append(Pfp / pp)
    ks, Pfps, ratios = np.array(ks), np.array(Pfps), np.array(ratios)
    upred = float(Pfps.std())
    diff = sw_fp["Pcr"] - Pfp0
    lim = 2 * math.hypot(upred, sw_fp["uPcr"])                          # the common load-cell error cancels in the comparison
    B["k"] = dict(k=k0, uk=float(ks.std()), k_lo=float(np.percentile(ks, 2.5)), k_hi=float(np.percentile(ks, 97.5)), ndraws=len(ks))
    B["fp_pred"] = dict(P=Pfp0, uP=upred, diff_pct=100 * diff / Pfp0, lim_pct=100 * lim / Pfp0, agree=abs(diff) <= lim,
                        K=LM.spring_pin(EI, Lfp, k0)[1], ratio_sd=float(ratios.std()))
    B["kL_EI"] = k0 * Lff / EI
    out["B"] = B
    # ------------------------------------------------------------------ Part C: eccentric load on the 450 mm bar
    C = {}
    Pcr450, uP450 = A["450"]["PS"], A["450"]["uPS"]
    rA = {r["load_N"]: r for r in sel(rows, "A", "pinned", 450.0)}
    for en in (1.0, 2.0):
        rc = sel(rows, "C", "eccentric", 450.0, en)
        common = [(r, rA[r["load_N"]]) for r in rc if r["load_N"] in rA and r["load_N"] > 0]
        P = np.array([a["load_N"] for a, _ in common])
        dd = np.array([(a["defl_mm"] - b_["defl_mm"]) * 1e-3 for a, b_ in common])
        f = np.array([1 / math.cos(PI / 2 * math.sqrt(p / Pcr450)) - 1 for p in P])
        e_fit = float(f @ dd / (f @ f))
        resid = dd - e_fit * f
        u_stat = math.sqrt(resid @ resid / (len(P) - 1) / (f @ f))
        # sensitivity to P_cr (it shifts the secant factor): finite difference
        f2 = np.array([1 / math.cos(PI / 2 * math.sqrt(p / (Pcr450 + uP450))) - 1 for p in P])
        e2 = float(f2 @ dd / (f2 @ f2))
        ue = math.hypot(u_stat, e2 - e_fit)
        # strain gages: change of bending strain gives the change of moment = P (e + change of deflection)
        dbend = np.array([((a["eps_front_ue"] - a["eps_back_ue"]) - (b_["eps_front_ue"] - b_["eps_back_ue"])) / 2 * 1e-6 for a, b_ in common])
        arm = dbend * EI / (P * sec["c"])                               # = e + change of mid-length deflection
        e_strain = arm - dd
        m = P >= 400
        # table rows for the key
        tab = [dict(P=float(p), dA=float(b_["defl_mm"]), dC=float(a["defl_mm"]), dd=float(x * 1e3), th=float(en * 1e-3 * fi * 1e3), arm=float(ar * 1e3))
               for (a, b_), p, x, fi, ar in zip(common, P, dd, f, arm)]
        i6, i12 = list(P).index(600.0), list(P).index(1200.0)
        C[str(int(en))] = dict(e_fit=e_fit * 1e3, ue=ue * 1e3, e_nom=en, agree=abs(e_fit * 1e3 - en) <= 2 * math.hypot(ue * 1e3, meas["offsets_mm"]["tolerance"] / R3),
                               e_strain=float(np.mean(e_strain[m]) * 1e3), ue_strain=float(np.std(e_strain[m], ddof=1) / math.sqrt(m.sum()) * 1e3),
                               n=len(P), Pmax_common=float(P.max()), tab=tab, ratio_12_6=float(dd[i12] / dd[i6]),
                               ratio_12_6_th=float(f[i12] / f[i6]), Pmax_test=max(r["load_N"] for r in rc), dmax_test=max(r["defl_mm"] for r in rc))
    # secant formula: first-yield load for e = 2 mm with P_cr (via E) from Part A
    Le = Ls["A450"] * 1e-3
    E_eff = Pcr450 * Le ** 2 / (PI ** 2 * sec["I"])                    # the E that reproduces the measured P_cr
    PY = {}
    for en in (1.0, 2.0):
        e = en * 1e-3
        PYs = LM.secant_P_yield(sY, sec["A"], e, sec["c"], sec["r"], E_eff, Le)
        PYlin = sY * sec["A"] / (1 + e * sec["c"] / sec["r"] ** 2)       # Eq. 10.37
        PY[str(int(en))] = dict(PY=PYs, PYlin=PYlin, over_pct=100 * (PYlin / PYs - 1), ratio_Pcr=PYs / Pcr450,
                                ymax_at_PY=LM.ymax_secant(e, PYs, Pcr450) * 1e3)
    C["PY"] = PY
    # stress at the back face at the last common load, e = 2 mm: measured vs Eq. 10.35 with e alone and with the Part A response added
    rc2 = {r["load_N"]: r for r in sel(rows, "C", "eccentric", 450.0, 2.0)}
    Pl = C["2"]["Pmax_common"]
    s_meas = -rc2[Pl]["eps_back_ue"] * 1e-6 * E
    s_1035 = LM.sigmax_secant(Pl, sec["A"], 2e-3, sec["c"], sec["r"], Pcr450)
    s_A = -rA[Pl]["eps_back_ue"] * 1e-6 * E
    s_1035_fit = LM.sigmax_secant(Pl, sec["A"], C["2"]["e_fit"] * 1e-3, sec["c"], sec["r"], Pcr450)
    C["stress"] = dict(P=Pl, s_meas=s_meas / 1e6, s_1035=s_1035 / 1e6, s_A=s_A / 1e6, s_axial=Pl / sec["A"] / 1e6,
                       s_sum=(s_1035 + s_A - Pl / sec["A"]) / 1e6, s_1035_fit=s_1035_fit / 1e6)
    out["C"] = C
    # ------------------------------------------------------------------ Part D: short column (instructor demonstration)
    rd = sel(rows, "D", "short")
    Pmax = max(r["load_N"] for r in rd)
    LD = Ls["D"] * 1e-3
    slD = LD / sec["r"]
    PeD = LM.euler(E, sec["I"], LD)
    s_t = LM.column_curve_tangent(slD, E, sY, ref["m_RO"])
    s_r = LM.column_curve_tangent(slD, E, sY, ref["m_RO"], reduced=True)
    aa = LM.aa_6061(slD)
    sl_Y = PI * math.sqrt(E / sY)
    out["D"] = dict(L=LD, slender=slD, Pmax=Pmax, smax=Pmax / sec["A"] / 1e6, PE=PeD, sE=PeD / sec["A"] / 1e6, PY=sY * sec["A"], s_t=s_t / 1e6, Pt=s_t * sec["A"],
                    s_r=s_r / 1e6, Pr=s_r * sec["A"], aa=aa / 1e6, Paa=aa * sec["A"], aa195=1.95 * aa / 1e6, sl_Y=sl_Y,
                    E_over=100 * (PeD / Pmax - 1), Y_over=100 * (sY * sec["A"] / Pmax - 1), t_over=100 * (s_t * sec["A"] / Pmax - 1),
                    d_at_max=[r["defl_mm"] for r in rd if r["load_N"] == Pmax][0], urP=meas["utm_accuracy_pct"] / 100 / R3,
                    Et_at_t=LM.tangent_modulus(s_t, E, sY, ref["m_RO"]) / 1e9)
    # column curve points of the tests (Le/r, sigma)
    out["curve"] = dict(A=[(A[k]["slenderness"], A[k]["sigma_cr"]) for k in A],
                        B=[(B[nm]["K"] * B[nm]["L"] / sec["r"], B[nm]["PS"] / sec["A"] / 1e6) for nm in ("ff", "fp")],
                        D=[(slD, Pmax / sec["A"] / 1e6)], slY=sl_Y, aa_trans=66.0)
    # ------------------------------------------------------------------ D1: strut design
    tab = []
    for Do, tw in CATALOG:
        s = LM.tube(Do * 1e-3, tw * 1e-3)
        row = dict(Do=Do, t=tw, mass=RHO_AL * s["A"], A=s["A"] * 1e6, r=s["r"] * 1e3, Dt=Do / tw)
        for K, tag in ((1.0, "pin"), (0.52, "clamp")):
            Le_ = K * D1["L"]
            sl = Le_ / s["r"]
            Pall = LM.aa_6061(sl) * s["A"]
            PYs = LM.secant_P_yield(sY, s["A"], D1["e"], s["c"], s["r"], E, Le_)
            Pcr = LM.euler(E, s["I"], Le_)
            row[tag] = dict(sl=sl, Pall=Pall, PY=PYs, Pcr=Pcr, ok=bool(Pall >= D1["P"] and PYs >= D1["FS"] * D1["P"] and Do / tw <= D1["Dt_max"]),
                            ok_all=bool(Pall >= D1["P"]), ok_sec=bool(PYs >= D1["FS"] * D1["P"]), ymax=LM.ymax_secant(D1["e"], D1["P"], Pcr) * 1e3 if D1["P"] < Pcr else None)
        tab.append(row)
    best = {tag: min((r for r in tab if r[tag]["ok"]), key=lambda r: r["mass"]) for tag in ("pin", "clamp")}
    out["D1"] = dict(spec=D1, table=tab, best={k: (v["Do"], v["t"]) for k, v in best.items()})
    # ------------------------------------------------------------------ extra numbers for the key
    from scipy import optimize as _opt
    xtra = {}
    # C3: Southwell on the raw Part C readings (bow + knife edges + groove offset act together)
    for en in (1.0, 2.0):
        rc = sel(rows, "C", "eccentric", 450.0, en)
        swc = southwell_rows(rc, A["450"]["Pe"])
        xtra[f"C{int(en)}_sw"] = dict(PS=swc["Pcr"], d0=swc["delta0"] * 1e3, n=swc["n"], e_from_d0=(swc["delta0"] * 1e3 - A["450"]["d0S"]) * PI / 4)
        # mistake: fitting Eq. 7 to the raw Part C readings (bow and knife-edge offset left in)
        P_ = np.array([r["load_N"] for r in rc if r["load_N"] > 0]); d_ = np.array([r["defl_mm"] * 1e-3 for r in rc if r["load_N"] > 0])
        ok = P_ < 0.99 * Pcr450
        f_ = np.array([1 / math.cos(PI / 2 * math.sqrt(p_ / Pcr450)) - 1 for p_ in P_[ok]])
        xtra[f"C{int(en)}_raw_e"] = float(f_ @ d_[ok] / (f_ @ f_)) * 1e3
    # M1(b): kL/EI that brings K within 1 % of 0.5
    xtra["kLEI_1pct"] = _opt.brentq(lambda g: LM.spring_both(1.0, 1.0, g)[1] - 0.505, 1.0, 1e6)
    # C2: sensitivity (dk/k)/(dP/P) of Eq. 3 at the fixed-fixed result
    xff = Lff / 2 * math.sqrt(sw_ff["Pcr"] / EI)
    xtra["C2_sens"] = 0.5 * (1 - xff / (math.sin(xff) * math.cos(xff)))
    xtra["C2_x"] = xff
    # fixed-pinned sensitivity, for comparison: z from the measured P, k from Eq. 4 rearranged
    def k_fp(P):                                    # Eq. 4 rearranged: P L / k = z cot z - 1, z = L sqrt(P/EI)
        z = Lfp * math.sqrt(P / EI)
        return P * Lfp / (z / math.tan(z) - 1)
    kfp0 = k_fp(sw_fp["Pcr"])
    zf = Lfp * math.sqrt(sw_fp["Pcr"] / EI)                         # exact: d ln k / d ln P = 1 - (z/2) g'(z)/g(z), g = z cot z - 1
    xtra["C2_sens_fp"] = 1 - zf / 2 * (1 / math.tan(zf) - zf / math.sin(zf) ** 2) / (zf / math.tan(zf) - 1)
    xtra["k_from_fp"] = kfp0
    # D1 details for the reference tube and the trap
    def tube_detail(Do, tw, K):
        s_ = LM.tube(Do * 1e-3, tw * 1e-3)
        Le_ = K * D1["L"]
        sl = Le_ / s_["r"]
        Pcr_ = LM.euler(E, s_["I"], Le_)
        PY_ = LM.secant_P_yield(sY, s_["A"], D1["e"], s_["c"], s_["r"], E, Le_)
        # the mistake: factor of safety on the stress, sigma_max(P) = sigma_Y / FS
        Pst = LM.secant_P_yield(sY / D1["FS"], s_["A"], D1["e"], s_["c"], s_["r"], E, Le_)
        return dict(A=s_["A"] * 1e6, I=s_["I"] * 1e12, r=s_["r"] * 1e3, sl=sl, sall=LM.aa_6061(sl) / 1e6, Pall=LM.aa_6061(sl) * s_["A"], Pcr=Pcr_, PY=PY_,
                    PY_FS=PY_ / D1["FS"], P_stressFS=Pst, ymax=LM.ymax_secant(D1["e"], D1["P"], Pcr_) * 1e3, mass=RHO_AL * s_["A"], Dt=Do / tw,
                    smax=LM.sigmax_secant(D1["P"], s_["A"], D1["e"], s_["c"], s_["r"], Pcr_) / 1e6)
    bp, bc = out["D1"]["best"]["pin"], out["D1"]["best"]["clamp"]
    xtra["D1_best"] = tube_detail(*bp, 1.0)
    xtra["D1_trap"] = tube_detail(*bc, 0.52)
    xtra["D1_trap_pin"] = tube_detail(*bc, 1.0)
    out["xtra"] = xtra
    # ------------------------------------------------------------------ model-break numbers
    k_el = np.linspace(0.01, 0.3, 30)
    out["M1"] = dict(
        elastica_at_L60=[(L, (LM.elastica_pinned(optimize_k(1 / 60))[0] - 1) * 100) for L in ("all",)][0][1],
        elastica_at_L10=(LM.elastica_pinned(optimize_k(0.1))[0] - 1) * 100,
        yield_defl_450=(sY - Pcr450 / sec["A"]) * sec["I"] / (Pcr450 * sec["c"]) * 1e3,
    )
    return out, meas


def optimize_k(dL):
    """elastica modulus k that gives a lateral deflection delta/L = dL."""
    from scipy import optimize
    return optimize.brentq(lambda k: LM.elastica_pinned(k)[1] - dL, 1e-9, 0.999)


def summary(out):
    g = out["geom"]
    print(f"section b {g['b']:.4f}±{g['ub']:.4f} t {g['t']:.4f}±{g['ut']:.4f} A {g['A']:.2f} I {g['I']:.1f} (u {100*g['urI']:.2f}%) r {g['r']:.4f}")
    for k, a in out["A"].items():
        print(f"A{k}: Pe {a['Pe']:.0f}±{a['uPe']:.0f}  PS {a['PS']:.0f}±{a['uPS']:.0f} (n {a['n']}, fit {a['uPS_fit']:.1f}) diff {a['diff_pct']:+.2f}% lim {a['lim_pct']:.2f}% agree {a['agree']}  "
              f"d0S {a['d0S']:.3f}±{a['ud0S']:.3f} bow {a['bow']} e_eq {a['e_eq']:.3f}  ES {a['ES']:.2f}±{a['uES']:.2f} L/r {a['slenderness']:.1f} last P/Pcr {a['ratio_last']:.3f}")
    print("slope", out["A_slope"], "E_S", out["A_E"], "gage", out["A_gage"], "strainSW", out["A_strainSW"])
    for nm in ("ff", "fp"):
        b_ = out["B"][nm]
        print(f"B{nm}: Pe {b_['Pe']:.0f}±{b_['uPe']:.0f} PS {b_['PS']:.0f}±{b_['uPS']:.0f} diff {b_['diff_pct']:+.2f}% lim {b_['lim_pct']:.2f} agree {b_['agree']} K {b_['K']:.4f}±{b_['uK']:.4f} n {b_['n']}")
    print("k", out["B"]["k"], "fp pred", out["B"]["fp_pred"], "kL/EI", out["B"]["kL_EI"])
    for en in ("1", "2"):
        c = out["C"][en]
        print(f"C{en}: e_fit {c['e_fit']:.3f}±{c['ue']:.3f} agree {c['agree']} e_strain {c['e_strain']:.3f}±{c['ue_strain']:.3f} n {c['n']} ratio {c['ratio_12_6']:.3f} th {c['ratio_12_6_th']:.3f}")
    print("PY", out["C"]["PY"], "stress", out["C"]["stress"])
    print("D", out["D"])
    print("D1 best", out["D1"]["best"])
    print("M1", out["M1"])


if __name__ == "__main__":
    args = sys.argv[1:]
    out, meas = main(*(Path(a) for a in args))
    (HERE / "results.json").write_text(json.dumps(out, indent=1, default=float))
    summary(out)

"""Lab 7 analysis: every number in the instructor key comes from this script.

    python3 lab07_analysis.py [data.csv] [measurements.json]   ->  results.json + printed summary
"""
import csv
import json
import math
import sys
from pathlib import Path

import numpy as np
from scipy import optimize

import lab07_model as LM

HERE = Path(__file__).resolve().parent
LAB = HERE.parent
R3 = math.sqrt(3)

# D1: overhanging deck beam (Table 6 of the handout)
D1 = dict(Lt=4.0, w=2.0e3, P=1.5e3, step=0.05, span_lim=360.0, tip_lim=180.0, sa_frac=0.6)
CATALOG = [  # name, H, B, tf, tw (mm), idealized without fillets
    ("I 76 × 51", 76.2, 50.8, 5.6, 4.3), ("I 102 × 64", 101.6, 63.5, 6.4, 4.8), ("I 102 × 76", 101.6, 76.2, 6.35, 4.8),
    ("I 127 × 76", 127.0, 76.2, 7.1, 5.1), ("I 152 × 102", 152.4, 101.6, 7.9, 5.8), ("I 178 × 102", 177.8, 101.6, 8.4, 6.1),
    ("I 203 × 127", 203.2, 127.0, 9.5, 6.4)]
RHO_AL = 2700.0


def load(path):
    rows = list(csv.DictReader(open(path, newline="")))
    keep = ("part", "config", "load_pos_mm")
    return [{k: (v if k in keep else (float(v) if _isnum(v) else np.nan)) for k, v in r.items()} for r in rows]


def _isnum(v):
    try:
        float(v)
        return True
    except ValueError:
        return False


def sel(rows, part, config):
    return [r for r in rows if r["part"] == part and r["config"] == config]


def linfit(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    n = len(x)
    A = np.vstack([np.ones(n), x]).T
    coef, *_ = np.linalg.lstsq(A, y, rcond=None)
    res = y - A @ coef
    s2 = res @ res / max(n - 2, 1)
    cov = s2 * np.linalg.inv(A.T @ A)
    return coef[0], coef[1], math.sqrt(cov[0, 0]), math.sqrt(cov[1, 1])


def mean_u(vals, acc):
    v = np.array(vals, float)
    return float(v.mean()), math.sqrt((v.std(ddof=1) / math.sqrt(len(v))) ** 2 + (acc / R3) ** 2)


def ss_compliance(x, a, L, EI):
    """Downward deflection at x per newton for a downward unit load at a on a simple span L (App. F case 5)."""
    return -float(LM.ss_point(1.0, a, L, EI, x)[0])


def analyze(rows, m):
    g = m["g"]
    ref = m["reference"]
    u_mass = m["mass_tolerance_pct"] / 100 / R3
    u_pos = m["rule_accuracy_mm"] / R3 * 1e-3
    u_ind = m["indicator_accuracy_mm"] / R3 * 1e-3
    out = dict(g=g)
    # ------------------------------------------------------------------ bar dimensions
    b, ub = mean_u(m["bar"]["b_mm"], m["caliper_accuracy_mm"])
    h, uh = mean_u(m["bar"]["h_mm"], m["micrometer_accuracy_mm"])
    I = b * h ** 3 / 12 * 1e-12
    uI = math.hypot(ub / b, 3 * uh / h)
    out["bar"] = dict(b=b, ub=ub, h=h, uh=uh, I=I * 1e12, uI=uI, w=7850 * g * b * h * 1e-6)
    # ------------------------------------------------------------------ Part A
    A = m["A"]
    L = A["span_mm"] * 1e-3
    xg = [v * 1e-3 for v in A["gage_x_mm"]]
    xl = {"P200": A["load_x_mm"][0] * 1e-3, "P600": A["load_x_mm"][1] * 1e-3}
    comp, ucomp = {}, {}
    for cfg in ("P600", "P200"):
        rr = [r for r in sel(rows, "A", cfg)]
        P = np.array([r["mass_kg"] * g for r in rr])
        for j, col in enumerate(("d1_mm", "d2_mm", "d3_mm")):
            d = np.array([r[col] for r in rr]) * 1e-3
            _, sl, _, usl = linfit(P, d)
            comp[(cfg, j)] = sl
            ucomp[(cfg, j)] = math.sqrt(usl ** 2 + (sl * u_mass) ** 2 + (u_ind / (P.max())) ** 2)
    # E from each coefficient: compliance = f(x, a, L)/(E I)
    E_list = []
    rowsA = []
    for cfg in ("P600", "P200"):
        a = xl[cfg]
        for j, x in enumerate(xg):
            f = ss_compliance(x, a, L, 1.0)                 # m/N per (1/EI)
            c = comp[(cfg, j)]
            E = f / (c * I)
            # position sensitivity (span, gage, load each +-0.5 mm), indicator, mass, I
            dfs = [(ss_compliance(x, a, L + 1e-4, 1.0) - f) / 1e-4, (ss_compliance(x + 1e-4, a, L, 1.0) - f) / 1e-4,
                   (ss_compliance(x, a + 1e-4, L, 1.0) - f) / 1e-4]
            u_f = math.sqrt(sum((d_ * u_pos) ** 2 for d_ in dfs))
            uE = E * math.sqrt((u_f / f) ** 2 + (ucomp[(cfg, j)] / c) ** 2 + uI ** 2)
            E_list.append((E, uE))
            rowsA.append(dict(cfg=cfg, x=x, a=a, c=c, uc=ucomp[(cfg, j)], f=f, E=E / 1e9, uE=uE / 1e9))
    Ew = np.array([e for e, _ in E_list])
    uw = np.array([u for _, u in E_list])
    # the coefficients share I and the span: average them, keep the common (I) part of the uncertainty in full
    E_mean = float(Ew.mean())
    u_rand = float(Ew.std(ddof=1) / math.sqrt(len(Ew)))
    # positions (span, gages, hangers) are common to all six coefficients: treat their effect as fully correlated
    u_posrel = float(np.mean([math.sqrt(max((r_["uE"] / r_["E"]) ** 2 - uI ** 2 - (r_["uc"] / r_["c"]) ** 2, 0.0)) for r_ in rowsA]))
    u_E = math.sqrt(u_rand ** 2 + (E_mean * uI) ** 2 + (E_mean * u_posrel) ** 2)
    EIA = E_mean * I
    # reciprocity: deflection at 200 under the load at 600 vs deflection at 600 under the load at 200
    c13, c31 = comp[("P600", 0)], comp[("P200", 2)]
    u13, u31 = ucomp[("P600", 0)], ucomp[("P200", 2)]
    c12, c32 = comp[("P600", 1)], comp[("P200", 1)]
    # superposition: both loads together
    rb = sel(rows, "A", "both")
    Pb600, Pb200 = 2.0 * g, 1.0 * g
    meas_both = np.array([rb[-1][c] - rb[0][c] for c in ("d1_mm", "d2_mm", "d3_mm")]) * 1e-3
    pred_both = np.array([comp[("P600", j)] * Pb600 + comp[("P200", j)] * Pb200 for j in range(3)])
    u_pred_both = np.array([math.hypot(ucomp[("P600", j)] * Pb600, ucomp[("P200", j)] * Pb200) for j in range(3)])
    u_meas_both = math.sqrt(2) * u_ind
    theory_both = np.array([ss_compliance(x, xl["P600"], L, EIA) * Pb600 + ss_compliance(x, xl["P200"], L, EIA) * Pb200 for x in xg])
    out["A"] = dict(L=L, xg=xg, rows=rowsA, E=E_mean / 1e9, uE=u_E / 1e9, E_ref=ref["E_st_GPa"], uE_ref=ref["u_E_st_GPa"],
                    E_agree=2 * math.hypot(u_E / 1e9, ref["u_E_st_GPa"]), EI=EIA, uEI=u_E * I, E_spread=float(Ew.max() - Ew.min()) / 1e9,
                    c13=c13, c31=c31, u13=u13, u31=u31, recip_d=c13 - c31, recip_lim=2 * math.hypot(u13, u31), c12=c12, c32=c32,
                    meas_both=meas_both.tolist(), pred_both=pred_both.tolist(), theory_both=theory_both.tolist(), u_pred_both=u_pred_both.tolist(),
                    u_meas_both=u_meas_both, both_lim=[2 * math.hypot(u_meas_both, up) for up in u_pred_both],
                    d_max_P600=float(max(r["d2_mm"] for r in sel(rows, "A", "P600"))), M_max=3.0 * g * 0.2 * 0.6 / 0.8)
    out["A"]["sig_max"] = out["A"]["M_max"] * (h / 2 * 1e-3) / I / 1e6
    # ------------------------------------------------------------------ Part B1: cantilever with a flexible clamp
    B = m["B"]
    LB = B["tip_load_x_mm"] * 1e-3
    xg_b = [v * 1e-3 for v in B["gage_x_mm"]]
    rr = sel(rows, "B", "cantilever")
    P = np.array([r["mass_kg"] * g for r in rr])
    cB, ucB = [], []
    for col in ("d1_mm", "d2_mm"):
        _, sl, _, usl = linfit(P, np.array([r[col] for r in rr]) * 1e-3)
        cB.append(sl)
        ucB.append(math.sqrt(usl ** 2 + (sl * u_mass) ** 2 + (u_ind / P.max()) ** 2))

    def solve_clamp(c1, c2, L_, x1, x2):
        Amat = np.array([[x1 ** 2 * (3 * L_ - x1) / 6, L_ * x1], [x2 ** 2 * (3 * L_ - x2) / 6, L_ * x2]])
        inv_EI, inv_k = np.linalg.solve(Amat, np.array([c1, c2]))
        return 1 / inv_EI, 1 / inv_k
    EIB, kB = solve_clamp(cB[0], cB[1], LB, xg_b[0], xg_b[1])
    # uncertainty by perturbation (compliances, positions)
    sens = []
    for i, (val, u) in enumerate(((cB[0], ucB[0]), (cB[1], ucB[1]))):
        cc = list(cB)
        cc[i] = val + u
        e2, k2 = solve_clamp(cc[0], cc[1], LB, xg_b[0], xg_b[1])
        sens.append((e2 - EIB, 1 / k2 - 1 / kB))
    for dL, dx1, dx2 in ((u_pos, 0, 0), (0, u_pos, 0), (0, 0, u_pos)):
        e2, k2 = solve_clamp(cB[0], cB[1], LB + dL, xg_b[0] + dx1, xg_b[1] + dx2)
        sens.append((e2 - EIB, 1 / k2 - 1 / kB))
    uEIB = math.sqrt(sum(s[0] ** 2 for s in sens))
    u_invk = math.sqrt(sum(s[1] ** 2 for s in sens))
    EI_rigid = LB ** 3 / (3 * cB[1])
    out["B1"] = dict(c_mid=cB[0], c_tip=cB[1], uc_mid=ucB[0], uc_tip=ucB[1], EI=EIB, uEI=uEIB, k=kB, invk=1 / kB, u_invk=u_invk,
                     uk=u_invk * kB ** 2, EI_rigid=EI_rigid, EI_rigid_err=100 * (EI_rigid / EIA - 1), EI_agree=2 * math.hypot(uEIB, out["A"]["uEI"]),
                     clamp_share=100 * (LB ** 2 / kB) / cB[1], P_max=float(P.max()), sig_root=float(P.max()) * LB * (h / 2 * 1e-3) / I / 1e6)
    # ------------------------------------------------------------------ Part B2: propped
    rr = sel(rows, "B", "propped")
    P = np.array([r["mass_kg"] * g for r in rr])
    Rm = np.array([r["R_N"] for r in rr])
    d = np.array([r["d1_mm"] for r in rr]) * 1e-3
    _, rsl, _, ursl = linfit(P, Rm)
    s_R = float(np.std(Rm - np.polyval(np.polyfit(P, Rm, 1), P), ddof=2))      # scatter of one load-cell reading
    u_lc = m["loadcell_accuracy_pct"] / 100 / R3
    ursl = math.sqrt(ursl ** 2 + (rsl * u_lc) ** 2 + (rsl * u_mass) ** 2)
    _, dsl, _, udsl = linfit(P, d)
    udsl = math.sqrt(udsl ** 2 + (dsl * u_mass) ** 2 + (u_ind / P.max()) ** 2)
    xm = B["mid_load_x_mm"] * 1e-3

    def prop_pred(EI_, k_):
        bm = dict(family="propped", L=LB, EI=EI_, P=[(1.0, xm)], k=k_)
        cf = LM.closed_form(bm, np.array([xg_b[0]]))
        return cf["R"]["RB"], -float(cf["y"][0])
    r_rigid, d_rigid = prop_pred(EIA, math.inf)
    r_k, d_k = prop_pred(EIB, kB)
    # uncertainty of the prediction with k: perturb EI and 1/k
    r1, _ = prop_pred(EIB + uEIB, kB)
    r2, _ = prop_pred(EIB, 1 / (1 / kB + u_invk))
    u_rk = math.hypot(r1 - r_k, r2 - r_k)
    _, d1_ = prop_pred(EIB + uEIB, kB)
    _, d2_ = prop_pred(EIB, 1 / (1 / kB + u_invk))
    u_dk = math.hypot(d1_ - d_k, d2_ - d_k)
    # k from the measured reaction alone (inverse problem)
    k_from_R = optimize.brentq(lambda kk: prop_pred(EIB, kk)[0] - rsl, 50.0, 1e9)
    out["B2"] = dict(r=rsl, ur=ursl, r_rigid=r_rigid, r_k=r_k, u_rk=u_rk, agree_k=2 * math.hypot(ursl, u_rk), d_rigid_r=abs(rsl - r_rigid),
                     dslope=dsl, udslope=udsl, d_rigid=d_rigid, d_k=d_k, u_dk=u_dk, d_agree=2 * math.hypot(udsl, u_dk), k_from_R=k_from_R,
                     r_ss=0.5, P_max=float(P.max()), M_wall=float(P.max()) * (3 / 16) * LB, R_max=float(Rm.max()))
    # ------------------------------------------------------------------ Part B3: settlement
    rr = sel(rows, "B", "settlement")
    dR = rr[1]["R_N"] - rr[0]["R_N"]
    u_dR = math.sqrt(2 * max(s_R, m["loadcell_resolution_N"] / math.sqrt(12)) ** 2 + (dR * m["loadcell_accuracy_pct"] / 100 / R3) ** 2)
    Delta = B["settle_mm"] * 1e-3
    dR_rigid = -3 * EIA * Delta / LB ** 3
    flexB = LB ** 3 / (3 * EIB) + LB ** 2 / kB
    dR_k = -Delta / flexB
    u_dRk = abs(dR_k) * math.sqrt((m["prop_screw_accuracy_mm"] / R3 / B["settle_mm"]) ** 2 + (uEIB / EIB) ** 2 * 0.5 + 0)
    out["B3"] = dict(dR=dR, u_dR=u_dR, dR_rigid=dR_rigid, dR_k=dR_k, u_dRk=u_dRk, agree=2 * math.hypot(u_dR, u_dRk), Delta=Delta,
                     dd=rr[1]["d1_mm"] - rr[0]["d1_mm"])
    # ------------------------------------------------------------------ Part C: elastica
    C = m["C"]
    bs, ubs = mean_u(C["b_mm"], m["caliper_accuracy_mm"])
    ts, uts = mean_u(C["t_mm"], m["micrometer_accuracy_mm"])
    rr0 = sel(rows, "C", "elastica")
    # the free length: the rule reading at the vise is good to +-0.5 mm; the zero-load grid reading of the tip, corrected for
    # the small self-weight curvature (x_tip/L = 0.9998 at beta = 0.115), is better
    Ls_rule = C["L_mm"] * 1e-3
    Ls = rr0[0]["x_tip_mm"] * 1e-3 / 0.99983
    Is = bs * ts ** 3 / 12 * 1e-12
    ws = C["rho_kg_m3"] * g * bs * ts * 1e-6
    rr = sel(rows, "C", "elastica")
    Pc = np.array([r["mass_kg"] * g for r in rr])
    xt = np.array([r["x_tip_mm"] for r in rr]) * 1e-3
    dv = -np.array([r["y_tip_mm"] for r in rr]) * 1e-3              # downward tip deflection
    u_grid = m["grid_reading_mm"] / R3 * 1e-3
    # EI from the small loads with linear theory (first four points, increments from zero load)
    nlin = 4
    _, sl, _, usl = linfit(Pc[:nlin], dv[:nlin])
    EI_lin = Ls ** 3 / (3 * sl)
    uEI_lin = EI_lin * math.sqrt((usl / sl) ** 2 + (3 * u_grid / Ls) ** 2)

    def model_pts(EI_, with_w=True):
        beta = ws * Ls ** 3 / EI_ if with_w else 0.0
        res = []
        for P_ in Pc:
            _, d_, x_, _ = LM.elastica_bvp(P_ * Ls ** 2 / EI_, beta)
            res.append((d_ * Ls, x_ * Ls))
        return np.array(res)

    def resid(v):
        mp = model_pts(v[0])
        return np.concatenate([mp[:, 0] - dv, mp[:, 1] - xt]) / u_grid
    fit = optimize.least_squares(resid, [EI_lin])
    EI_fit = float(fit.x[0])
    J = fit.jac
    chi2 = float(fit.fun @ fit.fun)
    dof = 2 * len(Pc) - 1
    uEI_fit_stat = math.sqrt(1 / float((J.T @ J)[0, 0]))
    uEI_fit = EI_fit * math.hypot(uEI_fit_stat / EI_fit * math.sqrt(max(chi2 / dof, 1.0)), 3 * u_grid / Ls)   # L enters as L^3
    mp_w = model_pts(EI_fit, True)
    mp_0 = model_pts(EI_fit, False)
    pts = []
    sag0 = mp_w[0, 0]
    for i, P_ in enumerate(Pc):
        alpha = P_ * Ls ** 2 / EI_fit
        lin = alpha / 3 * Ls + sag0
        th0, dvc, xtc = LM.elastica_closed(alpha) if alpha > 0 else (0.0, 0.0, 1.0)
        pts.append(dict(P=float(P_), alpha=alpha, dv=float(dv[i]), xt=float(xt[i]), dv_w=float(mp_w[i, 0]), xt_w=float(mp_w[i, 1]),
                        dv_tip=float(dvc * Ls + sag0), xt_tip=float(xtc * Ls), dv_lin=float(lin), lin_err=100 * (lin / dv[i] - 1) if dv[i] > 0 else 0.0,
                        tip_only_err=float(dvc * Ls + sag0 - dv[i]) * 1e3))
    a5 = LM.elastica_p5()
    # interpolate the measured linear-theory error to find where it crosses 5 %
    errs = np.array([p_["lin_err"] for p_ in pts[1:]])
    als = np.array([p_["alpha"] for p_ in pts[1:]])
    i5 = int(np.argmax(errs > 5))
    a5_meas = float(np.interp(5, errs[i5 - 1:i5 + 1], als[i5 - 1:i5 + 1])) if i5 > 0 else float("nan")
    # root stress at the largest load: M(0) = P x_tip + w * integral of x ds (from the model), sigma = M c / I
    _, _, _, solmax = LM.elastica_bvp(Pc[-1] * Ls ** 2 / EI_fit, ws * Ls ** 3 / EI_fit)
    kappa0 = float(solmax.sol(0.0)[1]) / Ls                           # theta'(0) in 1/m
    M_root = EI_fit * kappa0
    sig_root = M_root * (ts / 2 * 1e-3) / Is / 1e6
    out["C"] = dict(b=bs, ub=ubs, t=ts, ut=uts, L=Ls, L_rule=Ls_rule, I=Is * 1e12, w=ws, EI_lin=EI_lin, uEI_lin=uEI_lin, EI_fit=EI_fit, uEI_fit=uEI_fit,
                    chi2=chi2, dof=dof, E_fit=EI_fit / Is / 1e9, uE_fit=EI_fit / Is / 1e9 * math.hypot(uEI_fit / EI_fit, 3 * uts / ts, ubs / bs),
                    E_lin=EI_lin / Is / 1e9, lin_bias=100 * (EI_lin / EI_fit - 1), beta=ws * Ls ** 3 / EI_fit, sag0=sag0, pts=pts, a5=a5, a5_meas=a5_meas,
                    alpha_max=pts[-1]["alpha"], M_root=M_root, sig_root=sig_root, u_grid=u_grid)
    # ------------------------------------------------------------------ D1
    E_al = ref["E_al_GPa"] * 1e9
    sa = D1["sa_frac"] * ref["sY_al_MPa"] * 1e6
    Lt = D1["Lt"]
    table = []
    for name, H, Bf, tf, tw in CATALOG:
        hw = H - 2 * tf
        Ii = (Bf * H ** 3 - (Bf - tw) * hw ** 3) / 12 * 1e-12
        Ai = (2 * Bf * tf + hw * tw) * 1e-6
        c = H / 2 * 1e-3
        EI_ = E_al * Ii
        feas = []
        evals = []
        for Lsp in np.round(np.arange(2.5, Lt + 1e-9, D1["step"]), 2):
            a = Lt - Lsp
            bm = dict(family="ss", L=float(Lsp), a_over=float(a), EI=EI_, P=[(D1["P"], Lt)], w=D1["w"])
            x = np.linspace(0, Lt, 8001)
            cf = LM.closed_form(bm, x)
            Mx = LM.moment_statics(bm, cf["R"], x)
            s = float(np.max(np.abs(Mx))) * c / Ii
            ys = float(np.max(np.abs(cf["y"][x <= Lsp + 1e-12])))
            yt = abs(float(cf["y"][-1]))
            r_s, r_y, r_t = s / sa, ys / (Lsp / D1["span_lim"]), (yt / (2 * a / 360) if a > 1e-9 else 0.0)
            ok = r_s <= 1 and r_y <= 1 and r_t <= 1
            evals.append(dict(Ls=float(Lsp), s=s / 1e6, ys=ys * 1e3, yt=yt * 1e3, r_s=r_s, r_y=r_y, r_t=r_t, ok=ok,
                              Mmax=float(np.max(np.abs(Mx))), RA=cf["R"]["RA"], RB=cf["R"]["RB"]))
            if ok:
                feas.append(float(Lsp))
        table.append(dict(name=name, I=Ii * 1e12, A=Ai * 1e6, mass=Ai * RHO_AL, feas=feas, evals=evals))
    best = next(t for t in sorted(table, key=lambda t_: t_["mass"]) if t["feas"])
    noover = next(t for t in sorted(table, key=lambda t_: t_["mass"]) if Lt in t["feas"])
    out["D1"] = dict(D1, E=E_al / 1e9, sa=sa / 1e6, table=table, best=best["name"], noover=noover["name"])
    return out


def main():
    data = sys.argv[1] if len(sys.argv) > 1 else LAB / "sample_data.csv"
    meas = sys.argv[2] if len(sys.argv) > 2 else HERE / "specimen_measurements.json"
    res = analyze(load(data), json.loads(Path(meas).read_text()))
    (HERE / "results.json").write_text(json.dumps(res, indent=1, default=float))
    A, B1, B2, B3, C, D = res["A"], res["B1"], res["B2"], res["B3"], res["C"], res["D1"]
    print(f"A: E = {A['E']:.2f} ± {A['uE']:.2f} GPa (spread {A['E_spread']:.2f}); EI {A['EI']:.3f}; recip c13 {A['c13']*1e6:.4f} c31 {A['c31']*1e6:.4f} um/N (d {A['recip_d']*1e6:.4f}, lim {A['recip_lim']*1e6:.4f})")
    print("   both meas", np.round(np.array(A["meas_both"]) * 1e3, 4), "pred", np.round(np.array(A["pred_both"]) * 1e3, 4), "lim", np.round(np.array(A["both_lim"]) * 1e3, 4))
    print(f"B1: EI {B1['EI']:.3f} ± {B1['uEI']:.3f} (A: {A['EI']:.3f}); k {B1['k']:.0f} ± {B1['uk']:.0f}; EI rigid {B1['EI_rigid']:.3f} ({B1['EI_rigid_err']:.1f} %); clamp share {B1['clamp_share']:.1f} %")
    print(f"B2: R/P {B2['r']:.4f} ± {B2['ur']:.4f}; rigid {B2['r_rigid']:.4f}; with k {B2['r_k']:.4f} ± {B2['u_rk']:.4f}; k from R {B2['k_from_R']:.0f}; d/P {B2['dslope']*1e6:.3f} vs rigid {B2['d_rigid']*1e6:.3f} k {B2['d_k']*1e6:.3f}")
    print(f"B3: dR {B3['dR']:.3f} ± {B3['u_dR']:.3f}; rigid {B3['dR_rigid']:.3f}; k {B3['dR_k']:.3f}")
    print(f"C: EI lin {C['EI_lin']:.5f} ± {C['uEI_lin']:.5f}; fit {C['EI_fit']:.5f} ± {C['uEI_fit']:.5f} (chi2 {C['chi2']:.1f}/{C['dof']}); E fit {C['E_fit']:.1f}; a5 {C['a5']:.3f} meas {C['a5_meas']:.3f}; sig_root {C['sig_root']:.0f}; beta {C['beta']:.4f}")
    for p in C["pts"]:
        print(f"   a {p['alpha']:.3f} dv {p['dv']*1e3:.1f} w {p['dv_w']*1e3:.2f} tip {p['dv_tip']*1e3:.2f} lin {p['dv_lin']*1e3:.1f} ({p['lin_err']:.1f} %) xt {p['xt']*1e3:.1f} / {p['xt_w']*1e3:.2f}")
    for t in D["table"]:
        print(f"D1 {t['name']:12s} I {t['I']/1e6:.3f}e6 mass {t['mass']:.2f} feasible {t['feas'][:1]}–{t['feas'][-1:]}")
    print("D1 best", D["best"], "without overhang", D["noover"])


if __name__ == "__main__":
    main()

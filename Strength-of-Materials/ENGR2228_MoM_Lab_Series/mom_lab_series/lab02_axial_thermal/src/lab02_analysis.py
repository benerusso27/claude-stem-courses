"""Lab 2 analysis: every number in the instructor key comes from this script.

    python3 lab02_analysis.py [data.csv] [measurements.json]   ->  results.json + printed summary
"""
import csv
import json
import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
LAB = HERE.parent
R3 = math.sqrt(3)


def load(path):
    rows = list(csv.DictReader(open(path, newline="")))
    f = lambda r, c: float(r[c]) if r[c].strip() else np.nan  # noqa: E731
    out = {}
    for part in "ABC":
        rr = [r for r in rows if r["part"] == part]
        out[part] = {c: np.array([f(r, c) for r in rr]) for c in rows[0] if c != "part"}
    return out


def linfit(x, y):
    n = len(x)
    A = np.vstack([np.ones(n), x]).T
    coef, *_ = np.linalg.lstsq(A, y, rcond=None)
    res = y - A @ coef
    s2 = res @ res / (n - 2)
    cov = s2 * np.linalg.inv(A.T @ A)
    return coef[0], coef[1], math.sqrt(cov[0, 0]), math.sqrt(cov[1, 1])


def mean_u(vals, acc):
    v = np.array(vals, float)
    return v.mean(), math.sqrt((v.std(ddof=1) / math.sqrt(len(v))) ** 2 + (acc / R3) ** 2)


def piecewise(P, F):
    """Fit F = 0 for P < Pg, F = -s (P - Pg) for P >= Pg (least squares over Pg, closed form for s)."""
    best = None
    for Pg in np.linspace(0, P.max() * 0.8, 4001):
        x = np.clip(P - Pg, 0, None)
        s = -(x @ F) / (x @ x)
        r = F + s * x
        sse = r @ r
        if best is None or sse < best[0]:
            best = (sse, Pg, s)
    sse, Pg, s = best
    n = len(P)
    sig = math.sqrt(sse / (n - 2))
    # standard errors from the local curvature of SSE (numerical Jacobian of the 2-parameter model)
    def model(theta):
        return -theta[1] * np.clip(P - theta[0], 0, None)
    th = np.array([Pg, s])
    J = np.zeros((n, 2))
    for k, h in ((0, 1.0), (1, 1e-5)):
        d = np.zeros(2); d[k] = h
        J[:, k] = (model(th + d) - model(th - d)) / (2 * h)
    cov = sig ** 2 * np.linalg.inv(J.T @ J)
    return Pg, s, math.sqrt(cov[0, 0]), math.sqrt(cov[1, 1]), sig


def analyze(data, m):
    out = {}
    hb = m["handbook"]
    u_gf = m["gage_factor_tolerance_pct"] / 100 / R3
    u_load = m["load_cell_accuracy_pct"] / 100 / R3
    # ------------------------------------------------------------------ Part A
    A = data["A"]
    b, ub = mean_u(m["A_width_mm"], m["caliper_accuracy_mm"])
    t, ut = mean_u(m["A_thickness_mm"], m["caliper_accuracy_mm"])
    Aa = b * t
    urA = math.hypot(ub / b, ut / t)
    sig = A["load_N"] / Aa                                    # MPa
    ea = (A["strain_axial_front_ue"] + A["strain_axial_back_ue"]) / 2 * 1e-6
    et = (A["strain_transverse_front_ue"] + A["strain_transverse_back_ue"]) / 2 * 1e-6
    a0, E, ua0, uE_stat = linfit(ea, sig)
    E /= 1e3; uE_stat /= 1e3
    uE = E * math.sqrt((uE_stat / E) ** 2 + urA ** 2 + u_load ** 2 + u_gf ** 2)
    c0, slope_t, _, us = linfit(ea, et)
    nu = -slope_t
    unu = math.sqrt(us ** 2 + (0.005 / R3) ** 2)            # + transverse-sensitivity allowance (0.5 %)
    hi = A["load_N"] > 4000
    beta = float(np.mean((A["strain_axial_front_ue"][hi] - A["strain_axial_back_ue"][hi]) /
                         (A["strain_axial_front_ue"][hi] + A["strain_axial_back_ue"][hi])))
    e_mis = beta * t / 6
    E_front = linfit(A["strain_axial_front_ue"] * 1e-6, sig)[1] / 1e3
    E_back = linfit(A["strain_axial_back_ue"] * 1e-6, sig)[1] / 1e3
    G = E / (2 * (1 + nu))
    uG = G * math.sqrt((uE / E) ** 2 + (unu / (1 + nu)) ** 2)
    up = A["step"] <= np.argmax(A["load_N"])
    hyst = float(np.max(np.abs(np.interp(A["load_N"][~up], A["load_N"][up], ea[up]) - ea[~up]))) * 1e6
    out["A"] = dict(b=b, ub=ub, t=t, ut=ut, A=Aa, urA=urA, E=E, uE=uE, uE_stat=uE_stat, E_int_MPa=a0, nu=nu, unu=unu,
                    nu_int_ue=c0 * 1e6, beta=beta, e_mis_mm=e_mis, E_front=E_front, E_back=E_back, G=G, uG=uG,
                    hyst_ue=hyst, sig_max=float(sig.max()), ea_max_ue=float(ea.max() * 1e6),
                    E_agree_lim=2 * math.hypot(uE, 1.0), E_ref=hb["E_al_GPa"], nu_agree_lim=2 * math.hypot(unu, 0.01))
    # ------------------------------------------------------------------ Part B
    B = data["B"]
    d_rod, u_drod = mean_u(m["B_rod_d_mm"], m["caliper_accuracy_mm"])
    do, udo = mean_u(m["B_tube_do_mm"], m["caliper_accuracy_mm"])
    di, udi = mean_u(m["B_tube_di_mm"], m["bore_gage_accuracy_mm"])
    A_rod = math.pi * d_rod ** 2 / 4
    A_tube = math.pi * (do ** 2 - di ** 2) / 4
    uA_tube = math.pi / 2 * math.hypot(do * udo, di * udi)
    eps_t = (B["strain_tube_front_ue"] + B["strain_tube_back_ue"]) / 2 * 1e-6
    F_t = E * 1e3 * A_tube * eps_t                           # N (E in MPa)
    P = B["load_N"]
    upB = np.arange(len(P)) <= np.argmax(P)
    Pg, s, uPg, us_, sres = piecewise(P[upB], F_t[upB])
    E_st = hb["E_st_GPa"] * 1e3
    k_al, k_st = E * 1e3 * A_tube, E_st * A_rod
    share_th = k_al / (k_al + k_st)
    u_share_th = share_th * (1 - share_th) * math.sqrt((uE / E) ** 2 + (uA_tube / A_tube) ** 2 + (hb["u_E_st_GPa"] / hb["E_st_GPa"]) ** 2
                                                     + (2 * u_drod / d_rod) ** 2)
    u_share_meas = math.sqrt(us_ ** 2 + (s * u_gf) ** 2 + (s * uE / E) ** 2 + (s * uA_tube / A_tube) ** 2 + (s * u_load) ** 2)
    L = m["B_rod_L_mm"]
    gap = Pg * L / (E_st * A_rod)
    ugap = gap * math.sqrt((uPg / Pg) ** 2 + (hb["u_E_st_GPa"] / hb["E_st_GPa"]) ** 2)
    Pmax = float(P.max())
    Ft_max = float(F_t[np.argmax(P)])
    F_rod_max = -(Pmax + Ft_max)
    sig_rod_max = F_rod_max / A_rod
    sig_tube_max = Ft_max / A_tube
    # textbook formula ignoring the gap
    Ft_nogap = -share_th * Pmax
    # dial gage: slopes before and after the knee
    dial = B["dial_mm"]
    pre = upB & (P > 1500) & (P < Pg - 500)
    post = upB & (P > Pg + 2500)
    _, sl_pre, _, u_sl_pre = linfit(P[pre] / 1e3, dial[pre])            # mm/kN
    _, sl_post, _, u_sl_post = linfit(P[post] / 1e3, dial[post])
    C_rod = L / (E_st * A_rod) * 1e3                        # mm/kN
    C_both = L / (k_al + k_st) * 1e3
    C_cap_est = sl_pre - C_rod
    ratio = F_t / np.where(P > 0, -P, np.nan)
    i10, i20 = int(np.argmin(abs(P[upB] - 10e3))), int(np.argmin(abs(P[upB] - 20e3)))
    hB = upB & (P > Pg + 2000)
    beta_B = float(np.mean((B["strain_tube_front_ue"][hB] - B["strain_tube_back_ue"][hB]) / (B["strain_tube_front_ue"][hB] + B["strain_tube_back_ue"][hB])))
    u_hg = m["height_gage_accuracy_mm"] / R3
    g_direct = m["B_rod_L_mm"] - m["B_tube_L_mm"]
    ug_direct = math.sqrt(2) * u_hg
    # unloading branch: line fit above the knee, compare slope with loading branch
    dn = (~upB) & (P > Pg + 2000)
    s_unload = -linfit(P[dn], F_t[dn])[1]
    out["B"] = dict(d_rod=d_rod, A_rod=A_rod, do=do, di=di, A_tube=A_tube, uA_tube=uA_tube, Pg=Pg, uPg=uPg, share=s, u_share=u_share_meas,
                    share_th=share_th, u_share_th=u_share_th, gap_mm=gap, ugap_mm=ugap, Pmax=Pmax, Ft_max=Ft_max, F_rod_max=F_rod_max,
                    sig_rod_max=sig_rod_max, sig_tube_max=sig_tube_max, Ft_nogap=Ft_nogap, sl_pre=sl_pre, sl_post=sl_post,
                    C_rod=C_rod, C_both=C_both, C_cap_est=C_cap_est, C_cap_est2=sl_post - C_both,
                    ratio_at=dict((f"{int(p)}", float(r)) for p, r in zip(P[upB], ratio[upB]) if p > 0),
                    sres_N=sres, frac_err_nogap=(Ft_nogap - Ft_max) / Ft_max, u_sl_pre=u_sl_pre, u_sl_post=u_sl_post,
                    uC_cap_est=math.hypot(u_sl_pre, C_rod * hb["u_E_st_GPa"] / hb["E_st_GPa"]),
                    uC_cap_est2=math.hypot(u_sl_post, C_both * 0.01),
                    F10=float(F_t[upB][i10]), F20=float(F_t[upB][i20]), P10=float(P[upB][i10]), P20=float(P[upB][i20]),
                    beta_B=beta_B, g_direct=g_direct, ug_direct=ug_direct, s_unload=s_unload,
                    k1=E_st * A_rod / L, k2=k_al / L, s_th_nominal=share_th)
    # ------------------------------------------------------------------ Part C
    C = data["C"]
    db, udb = mean_u(m["C_bolt_d_mm"], m["caliper_accuracy_mm"])
    so, uso = mean_u(m["C_sleeve_do_mm"], m["caliper_accuracy_mm"])
    si, usi = mean_u(m["C_sleeve_di_mm"], m["caliper_accuracy_mm"])
    A_b = math.pi * db ** 2 / 4
    A_s = math.pi * (so ** 2 - si ** 2) / 4
    T = C["temperature_C"]
    eb = C["strain_bolt_ue"] * 1e-6
    c_int, slope, _, uslope = linfit(T, eb)
    dFdT = E_st * A_b * slope                                # N/K (E_st MPa * mm^2)
    u_app = 0.5e-6 / R3                                      # residual thermal output allowance
    u_dFdT = dFdT * math.sqrt((uslope / slope) ** 2 + (u_app / slope) ** 2 + u_gf ** 2 + (hb["u_E_st_GPa"] / hb["E_st_GPa"]) ** 2
                              + (2 * udb / db) ** 2)
    Lc = m["C_L_mm"]
    flex = Lc / (E_st * A_b) + Lc / (E * 1e3 * A_s)          # mm/N
    dalpha = hb["alpha_al"] - hb["alpha_st"]
    dFdT_th = dalpha * Lc / flex
    alpha_al_meas = hb["alpha_st"] + dFdT * flex / Lc
    u_flex_rel = 0.5 * math.hypot(uE / E, hb["u_E_st_GPa"] / hb["E_st_GPa"])
    u_alpha_al_meas = math.sqrt((u_dFdT * flex / Lc) ** 2 + hb["u_alpha"] ** 2 + (dFdT * flex / Lc * u_flex_rel) ** 2)
    u_dFdT_th = dFdT_th * math.sqrt((math.sqrt(2) * hb["u_alpha"] / dalpha) ** 2 + 0.25 * (uE / E) ** 2 + 0.25 * (hb["u_E_st_GPa"] / hb["E_st_GPa"]) ** 2)
    eps0 = float(np.mean(eb[np.abs(T - 20) < 1]))
    heat = np.arange(len(T)) <= np.argmax(T)
    dFdT_heat = E_st * A_b * linfit(T[heat], eb[heat])[1]
    dFdT_cool = E_st * A_b * linfit(T[~heat | (np.arange(len(T)) == np.argmax(T))], eb[~heat | (np.arange(len(T)) == np.argmax(T))])[1]
    Tm = T - T.mean()
    Aq = np.vstack([np.ones_like(Tm), Tm, Tm ** 2]).T
    cq, *_ = np.linalg.lstsq(Aq, eb, rcond=None)
    rq = eb - Aq @ cq
    covq = (rq @ rq / (len(T) - 3)) * np.linalg.inv(Aq.T @ Aq)
    c2_N = E_st * A_b * cq[2]; uc2_N = E_st * A_b * math.sqrt(covq[2, 2])

    F0 = E_st * A_b * eps0
    F80 = F0 + dFdT * 60
    out["C"] = dict(A_b=A_b, A_s=A_s, slope_ue_per_C=slope * 1e6, u_slope=uslope * 1e6, dFdT=dFdT, u_dFdT=u_dFdT, dFdT_th=dFdT_th,
                    u_dFdT_th=u_dFdT_th, F0=F0, F80=F80, sig_b80=F80 / A_b, sig_s80=-F80 / A_s, free_mismatch_mm=dalpha * 60 * Lc,
                    flex_mm_per_N=flex, dalpha=dalpha, dFdT_heat=dFdT_heat, dFdT_cool=dFdT_cool, c2_N_per_K2=c2_N, uc2_N_per_K2=uc2_N,
                    alpha_al_meas=alpha_al_meas, u_alpha_al_meas=u_alpha_al_meas, resid_bias_N_per_K=0.4e-6 * E_st * A_b,
                    eps0_ue=eps0 * 1e6, Tmax=float(T.max()))
    # ------------------------------------------------------------------ D1: rail expansion gap (handout Sec. 8)
    L_r, a_r = 3000.0, hb["alpha_al"]
    T_inst, T_lo, T_hi, dT_inst = 15.0, -25.0, 55.0, 5.0
    sig_allow, gap_cold_max = 40.0, 8.0
    E_lo = E - 2 * uE
    g_min = a_r * (T_hi - (T_inst - dT_inst)) * L_r - sig_allow * L_r / (E * 1e3)
    g_max = gap_cold_max - a_r * ((T_inst + dT_inst) - T_lo) * L_r
    g_min_nom = a_r * (T_hi - T_inst) * L_r - sig_allow * L_r / (E * 1e3)
    g_max_nom = gap_cold_max - a_r * (T_inst - T_lo) * L_r
    out["D"] = dict(g_min=g_min, g_max=g_max, g_min_nom=g_min_nom, g_max_nom=g_max_nom, free_exp_hot=a_r * (T_hi - T_inst) * L_r,
                    free_con_cold=a_r * (T_inst - T_lo) * L_r, sig_if_zero_gap=E * 1e3 * a_r * (T_hi - T_inst), E_lo=E_lo)
    return out


def main():
    data = load(Path(sys.argv[1]) if len(sys.argv) > 1 else LAB / "sample_data.csv")
    m = json.loads((Path(sys.argv[2]) if len(sys.argv) > 2 else HERE / "specimen_measurements.json").read_text())
    r = analyze(data, m)
    (HERE / "results.json").write_text(json.dumps(r, indent=1, default=float))
    for k, v in r.items():
        print(f"=== {k} ===")
        for kk, vv in v.items():
            if not isinstance(vv, dict):
                print(f"  {kk:18s} {vv:.6g}")


if __name__ == "__main__":
    main()

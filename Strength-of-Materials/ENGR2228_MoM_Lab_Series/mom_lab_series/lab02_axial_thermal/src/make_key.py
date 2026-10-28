"""Generate lab02_instructor_key.md from computed results (no hand-typed numbers).

    python3 lab02_analysis.py && python3 make_key.py

Inputs: results.json (lab02_analysis.py on sample_data.csv), specimen_measurements.json, and the
simulation's own model code (run in Node; dumped to sim_numbers.json). Placeholders are written «name».
"""
import json
import math
import re
import subprocess
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
LAB = HERE.parent
R = json.loads((HERE / "results.json").read_text())
MEAS = json.loads((HERE / "specimen_measurements.json").read_text())
HB = MEAS["handbook"]
A_, B_, C_, D_ = R["A"], R["B"], R["C"], R["D"]
V = {}
PI = math.pi


def f(x, nd):
    return f"{x:,.{nd}f}".replace(",", " ").replace("-", "−")


def pm(x, U, nd):
    return f"{f(x, nd)} ± {f(U, nd)}"


# ------------------------------------------------------------------ simulation numbers (exact page code)
JS = r"""
const {loadModel}=require('%s'); const M=loadModel('%s'); const o={};
const P=M.PRESETS;
const rt=Object.assign({},P.rodtube); const c=M.parallelClosed(rt);
o.rodtube={Pgap:c.Pgap, share:c.share, F2:c.F2, F1:c.F1, k1:c.k1, k2:c.k2,
  F2_10:M.parallelClosed(rt,10e3).F2, F2_20:M.parallelClosed(rt,20e3).F2};
const bo=Object.assign({},P.bolt); const cb=M.parallelClosed(bo);
o.bolt={dFdT:cb.dFdT, F1:cb.F1, F1_0:M.parallelClosed(bo,0,0).F1};
const sw=Object.assign({},P.bolt,{mat1:'al',mat2:'steel',dT:120}); const cs=M.parallelClosed(sw);
o.swap={dFdT:cs.dFdT, F1_120:cs.F1};
const gn=Object.assign({},P.rodtube,{g:0.4e-3,P:60e3}); const cg=M.parallelClosed(gn);
o.gapnever={Pgap:cg.Pgap, sig1:cg.F1/cg.A1, sy:M.MATERIALS.steel.sy};
const tp=Object.assign({},P.taper,{support:'fixed',N:1}); const cv=M.seriesConvergence(tp);
o.taper={rows:cv.rows, slope:cv.slope, R:M.seriesClosed(tp).R};
const bk=Object.assign({},P.stepped,{PB:0,dT:120,L1:0.6,L2:0.6,da:8e-3,db:8e-3,d2:6e-3}); const ck=M.seriesClosed(bk);
const m1=M.MATERIALS[bk.smat1], m2=M.MATERIALS[bk.smat2];
o.buckle={N1:ck.N1, N2:ck.N2, sig1:ck.sigmaMax1, sig2:ck.sigma2, L:ck.L,
  Pcr:Math.PI**2*Math.min(m1.E,m2.E)*Math.PI*Math.min(bk.da,bk.db,bk.d2)**4/64/(0.5*ck.L)**2, mat1:bk.smat1, mat2:bk.smat2};
o.mats=M.MATERIALS;
console.log(JSON.stringify(o));
""" % ((LAB.parent / "shared" / "test_harness.js").as_posix(), (LAB / "lab02_simulation.html").as_posix())
SIM = json.loads(subprocess.run(["node", "-e", JS], capture_output=True, text=True, check=True).stdout)
(HERE / "sim_numbers.json").write_text(json.dumps(SIM, indent=1))

# ------------------------------------------------------------------ pre-lab (nominal dimensions, Table 1 values)
E_al, E_st, nu_al = HB["E_al_GPa"] * 1e3, HB["E_st_GPa"] * 1e3, HB["nu_al"]       # MPa
a_al, a_st = HB["alpha_al"], HB["alpha_st"]
sy_st, sy_al = 370.0, 276.0
Aa = 25.40 * 6.35
sA = 18000 / Aa
V.update(P1_A=f(Aa, 2), P1_sig=f(sA, 1), P1_ex=f(sA / E_al * 1e6, 0), P1_ey=f(-nu_al * sA / E_al * 1e6, 0),
         P1_frac=f(100 * sA / sy_al, 0), P1_res2=f(100 / (2000 / Aa / E_al * 1e6), 2), P1_res18=f(100 / (sA / E_al * 1e6), 3))
A1n = PI / 4 * 12.70 ** 2
A2n = PI / 4 * (25.40 ** 2 - 19.05 ** 2)
k1n = E_st * A1n / 150.0
k2n = E_al * A2n / (150.0 - 0.040)
sn = k2n / (k1n + k2n)
Pgn = k1n * 0.040
V.update(A1n=f(A1n, 2), A2n=f(A2n, 2), k1n=f(k1n / 1e3, 1), k2n=f(k2n / 1e3, 1), Pgn=f(Pgn / 1e3, 3), sn=f(sn, 4))
for P in (10, 20, 30):
    V[f"F2n_{P}"] = f(-sn * (P * 1e3 - Pgn) / 1e3, 3)
V["F2n_2x10"] = f(-2 * sn * (10e3 - Pgn) / 1e3, 3)
V["P1_Ft_est"] = f(-0.4 * (30e3 - Pgn) / 1e3, 1)
V["P1_srod_est"] = f(-(30e3 - 0.4 * (30e3 - Pgn)) / A1n, 0)
Ab_n = PI / 4 * 10.0 ** 2
As_n = PI / 4 * (20.0 ** 2 - 10.5 ** 2)
flex_n = 100 / (E_st * Ab_n) + 100 / (E_al * As_n)
dFdT_n = (a_al - a_st) * 100 / flex_n
V.update(Ab_n=f(Ab_n, 2), As_n=f(As_n, 2), flex_n=f(flex_n * 1e6, 3), dFdT_n=f(dFdT_n, 2),
         mis_n=f((a_al - a_st) * 60 * 100, 4), deb_n=f(dFdT_n * 60 / (E_st * Ab_n) * 1e6, 0),
         kb_n=f(E_st * Ab_n / 100 / 1e3, 0), ks_n=f(E_al * As_n / 100 / 1e3, 0),
         F80_n=f((2000 + dFdT_n * 60) / 1e3, 3), sb80_n=f((2000 + dFdT_n * 60) / Ab_n, 1), ss80_n=f(-(2000 + dFdT_n * 60) / As_n, 1))
flex_sw = 100 / (E_al * Ab_n) + 100 / (E_st * As_n)
dFdT_sw = (a_st - a_al) * 100 / flex_sw
V.update(dFdT_sw=f(dFdT_sw, 2), dTsep=f(2000 / abs(dFdT_sw), 1))
V.update(P4_e=f(0.05 * 6.35 / 6, 4), P4_front=f(100 * (1 / 1.05 - 1), 1), P4_back=f(100 * (1 / 0.95 - 1), 1))
Fy = sy_st * A1n
Py = Pgn + (Fy - Pgn) / (1 - sn)
V.update(P6_Fy=f(Fy / 1e3, 1), P6_Py=f(Py / 1e3, 1), P6_fac=f(Py / 30e3, 2), P6_stube=f(sn * (Py - Pgn) / A2n, 0))
S = SIM
V.update(sim_Pgap=f(S["rodtube"]["Pgap"] / 1e3, 3), sim_share=f(100 * S["rodtube"]["share"], 2), sim_F2=f(S["rodtube"]["F2"] / 1e3, 3),
         sim_dFdT=f(S["bolt"]["dFdT"], 2), sim_F1_60=f(S["bolt"]["F1"] / 1e3, 3),
         sim_F2_10=f(S["rodtube"]["F2_10"] / 1e3, 3), sim_F2_20=f(S["rodtube"]["F2_20"] / 1e3, 3))

# ------------------------------------------------------------------ Part A
V.update(Ev_MPa=f(A_["E"] * 1e3, 0), b=f(A_["b"], 3), t=f(A_["t"], 3), A_A=f(A_["A"], 2), uA_rel=f(100 * A_["urA"], 2),
         E_A=pm(A_["E"], 2 * A_["uE"], 2), Ev=f(A_["E"], 2), UE=f(2 * A_["uE"], 2), Estat=f(100 * A_["uE_stat"] / A_["E"], 3),
         gf_rel=f(100 * 0.01 / math.sqrt(3), 2), load_rel=f(100 * 0.005 / math.sqrt(3), 2),
         Eint=f(A_["E_int_MPa"], 3), nu=pm(A_["nu"], 2 * A_["unu"], 3), nuint=f(A_["nu_int_ue"], 2),
         G=pm(A_["G"], 2 * A_["uG"], 2), hyst=f(A_["hyst_ue"], 1), Eagree_d=f(abs(A_["E"] - 68.9), 2),
         Eagree_lim=f(A_["E_agree_lim"], 2), nuagree_d=f(abs(A_["nu"] - 0.33), 4), nuagree_lim=f(A_["nu_agree_lim"], 3),
         beta=f(A_["beta"], 4), beta_pct=f(100 * A_["beta"], 2), e_mis=f(A_["e_mis_mm"], 4),
         E_front=f(A_["E_front"], 2), E_back=f(A_["E_back"], 2),
         E_harm=f(2 / (1 / A_["E_front"] + 1 / A_["E_back"]), 2), E_arith=f((A_["E_front"] + A_["E_back"]) / 2, 2),
         E_front_err=f(100 * (A_["E_front"] / A_["E"] - 1), 1), E_back_err=f(100 * (A_["E_back"] / A_["E"] - 1), 1),
         sig_max=f(A_["sig_max"], 1), ea_max=f(A_["ea_max_ue"], 0))
# ------------------------------------------------------------------ Part B
V.update(d_rod=f(B_["d_rod"], 3), A_rod=f(B_["A_rod"], 2), do=f(B_["do"], 3), di=f(B_["di"], 3), A_tube=f(B_["A_tube"], 2),
         uA_tube=f(B_["uA_tube"], 2), Pg=pm(B_["Pg"] / 1e3, 2 * B_["uPg"] / 1e3, 3), Pgv=f(B_["Pg"] / 1e3, 3),
         share=pm(B_["share"], 2 * B_["u_share"], 4), share_th=pm(B_["share_th"], 2 * B_["u_share_th"], 4),
         share_d=f(abs(B_["share"] - B_["share_th"]), 4), share_lim=f(2 * math.hypot(B_["u_share"], B_["u_share_th"]), 4),
         gap=pm(B_["gap_mm"], 2 * B_["ugap_mm"], 4), gap_direct=pm(B_["g_direct"], 2 * B_["ug_direct"], 3),
         gap_ratio=f(B_["ug_direct"] / B_["ugap_mm"], 0), gap_d=f(abs(B_["gap_mm"] - B_["g_direct"]), 4),
         gap_lim=f(2 * math.hypot(B_["ugap_mm"], B_["ug_direct"]), 4), k1=f(B_["k1"] / 1e3, 1), k2=f(B_["k2"] / 1e3, 1),
         sres=f(B_["sres_N"], 0), Ft30=f(B_["Ft_max"] / 1e3, 3), Frod30=f(B_["F_rod_max"] / 1e3, 2),
         srod30=f(B_["sig_rod_max"], 1), stube30=f(B_["sig_tube_max"], 1), Ft_nogap=f(B_["Ft_nogap"] / 1e3, 3),
         nogap_err=f(100 * B_["frac_err_nogap"], 1), beta_B=f(100 * B_["beta_B"], 1), s_unload=f(B_["s_unload"], 4),
         F10=f(B_["F10"] / 1e3, 3), F20=f(B_["F20"] / 1e3, 3), F_ratio=f(B_["F20"] / B_["F10"], 2))
Pmax = B_["Pmax"]
Ft_eq11 = -B_["share"] * (Pmax - B_["Pg"])
V["Ft_eq11"] = f(Ft_eq11 / 1e3, 3)
V["Ft_eq11_d"] = f(100 * (Ft_eq11 / B_["Ft_max"] - 1), 2)
app = sorted((int(k), v) for k, v in B_["ratio_at"].items() if int(k) > 1000)
pick = [min(app, key=lambda pv: abs(pv[0] - x)) for x in (8e3, 12e3, 20e3, 30e3)]
V["app_tab"] = ", ".join(f"{p / 1e3:.0f} kN: {v:.3f}" for p, v in pick)
V["app30"] = f(app[-1][1], 3)
V["app_th"] = f(B_["share"] * (1 - B_["Pg"] / Pmax), 3)
g5 = (30e3 / 21) / B_["k1"]
V.update(g5=f(g5 * 1e3, 1), Pg5=f(30 / 21, 2))
V.update(sl_pre=f(B_["sl_pre"] * 1e3, 2), usl_pre=f(B_["u_sl_pre"] * 1e3, 2), sl_post=f(B_["sl_post"] * 1e3, 3), usl_post=f(B_["u_sl_post"] * 1e3, 3),
         C_rod=f(B_["C_rod"] * 1e3, 2), C_both=f(B_["C_both"] * 1e3, 2),
         C1=pm(B_["C_cap_est"] * 1e3, B_["uC_cap_est"] * 1e3, 2), C2=pm(B_["C_cap_est2"] * 1e3, B_["uC_cap_est2"] * 1e3, 2),
         Cdiff_sig=f(abs(B_["C_cap_est"] - B_["C_cap_est2"]) / math.hypot(B_["uC_cap_est"], B_["uC_cap_est2"]), 1))
# extra Part B numbers quoted in the key
V["Pg_hg"] = pm(B_["k1"] * B_["g_direct"] / 1e3, B_["k1"] * 2 * B_["ug_direct"] / 1e3, 1)
first_nz = min(int(k) for k, v in B_["ratio_at"].items() if int(k) > 1000 and v > 0.01)
V["P_first"] = f(first_nz / 1e3, 0)
V["first_err"] = f(100 * (first_nz / B_["Pg"] - 1), 0)
import lab02_analysis as LA
_d = LA.load(LA.LAB / "sample_data.csv")["B"]
_P = _d["load_N"]; _up = np.arange(len(_P)) <= np.argmax(_P)
_Ft = A_["E"] * 1e3 * B_["A_tube"] * (_d["strain_tube_front_ue"] + _d["strain_tube_back_ue"]) / 2 * 1e-6
_s0 = -(_P[_up] @ _Ft[_up]) / (_P[_up] @ _P[_up])
_res = _Ft[_up] + _s0 * _P[_up]
V["origin_res"] = f(np.max(np.abs(_res[_P[_up] < 10e3])) / 1e3, 1)
V["C_frac"] = f(100 * B_["C_cap_est2"] / B_["sl_post"], 0)
# ------------------------------------------------------------------ Part C
V.update(A_b=f(C_["A_b"], 2), A_s=f(C_["A_s"], 2), slope=pm(C_["slope_ue_per_C"], 2 * C_["u_slope"], 3),
         dFdT=pm(C_["dFdT"], 2 * C_["u_dFdT"], 1), dFdT_th=pm(C_["dFdT_th"], 2 * C_["u_dFdT_th"], 1),
         dFdT_d=f(abs(C_["dFdT"] - C_["dFdT_th"]), 1), dFdT_lim=f(2 * math.hypot(C_["u_dFdT"], C_["u_dFdT_th"]), 1),
         dFdT_heat=f(C_["dFdT_heat"], 1), dFdT_cool=f(C_["dFdT_cool"], 1), F0=f(C_["F0"] / 1e3, 3), eps0=f(C_["eps0_ue"], 1),
         F80=f(C_["F80"] / 1e3, 3), sb80=f(C_["sig_b80"], 1), ss80=f(C_["sig_s80"], 1), flex=f(C_["flex_mm_per_N"] * 1e6, 4),
         resid=f(C_["resid_bias_N_per_K"], 1), resid05=f(C_["resid_bias_N_per_K"] * 0.5 / 0.4, 1),
         alpha_meas=pm(C_["alpha_al_meas"] * 1e6, 2 * C_["u_alpha_al_meas"] * 1e6, 2),
         alpha_d=f(abs(C_["alpha_al_meas"] - a_al) * 1e6, 2), alpha_lim=f(2 * math.hypot(C_["u_alpha_al_meas"], HB["u_alpha"]) * 1e6, 2),
         c2=pm(C_["c2_N_per_K2"], C_["uc2_N_per_K2"], 3), u_dFdT_rel=f(100 * C_["u_dFdT"] / C_["dFdT"], 1),
         u_app_rel=f(100 * 0.5 / math.sqrt(3) / C_["slope_ue_per_C"], 1), alpha_high=f(100 * (C_["alpha_al_meas"] / 23.4e-6 - 1), 1),
         E1U=f(100 * 2 * A_["uE"] / A_["E"], 1), oneg_ratio=f(abs(A_["E_front"] / A_["E"] - 1) / (2 * A_["uE"] / A_["E"]), 1))
# E(T) effect on the slope: average over the range and predicted curvature (X2)
Eb = E_st * C_["A_b"]
Es0 = A_["E"] * 1e3
L = 100.0


def F_of(dT, coeff=-3e-4):
    fb = L / Eb
    fs = L / (Es0 * (1 + coeff * dT) * C_["A_s"])
    I = C_["F0"] * (L / Eb + L / (Es0 * C_["A_s"]))
    return (I + (a_al - a_st) * dT * L) / (fb + fs)


dTs = np.linspace(0, 60, 61)
Fe = np.array([F_of(x) for x in dTs])
cq = np.polyfit(dTs, Fe, 2)
V["c2_pred"] = f(cq[0], 4)
V["slope_ET"] = f(np.polyfit(dTs, Fe, 1)[0], 1)
V["slope_noET"] = f(np.polyfit(dTs, np.array([F_of(x, 0.0) for x in dTs]), 1)[0], 1)
V["dev_ET"] = f(np.max(np.abs(Fe - np.polyval(np.polyfit(dTs, Fe, 1), dTs))), 1)
V["dev_ET_ue"] = f(np.max(np.abs(Fe - np.polyval(np.polyfit(dTs, Fe, 1), dTs))) / Eb * 1e6, 2)
V["ET_pct"] = f(100 * (np.polyfit(dTs, Fe, 1)[0] / np.polyfit(dTs, np.array([F_of(x, 0.0) for x in dTs]), 1)[0] - 1), 1)
# ------------------------------------------------------------------ M1
gcrit = sy_st * 150.0 / E_st
V.update(gcrit=f(gcrit, 3), gn_Pgap=f(S["gapnever"]["Pgap"] / 1e3, 1), gn_sig=f(-S["gapnever"]["sig1"] / 1e6, 0),
         sw_dFdT=f(S["swap"]["dFdT"], 2), sw_dTsep=f(2000 / abs(S["swap"]["dFdT"]), 1), sw_F120=f(S["swap"]["F1_120"] / 1e3, 2))
# ------------------------------------------------------------------ C1 convergence (taper)
rows = S["taper"]["rows"]
V["C1_tab"] = "; ".join(f"N = {r['N']}: {r['err']:.2e}" for r in rows)
V["C1_slope"] = f(S["taper"]["slope"], 3)
V["C1_R"] = f(S["taper"]["R"] / 1e3, 3)
# ------------------------------------------------------------------ C3 dilatation (Part A at 18 kN)
ex = A_["sig_max"] / (A_["E"] * 1e3)
ey = -A_["nu"] * ex
V.update(C3_ex=f(ex * 1e6, 0), C3_ey=f(ey * 1e6, 0), C3_db=f(ey * A_["b"] * 1e3, 1), C3_dt=f(ey * A_["t"] * 1e3, 1),
         C3_dil=f((1 - 2 * A_["nu"]) * ex * 1e6, 0), C3_K=f(A_["E"] / (3 * (1 - 2 * A_["nu"])), 1),
         C3_ucal=f(0.02 / math.sqrt(3) * 1e3, 0))
# ------------------------------------------------------------------ X1 thermal buckling
LdC = PI / 2 * math.sqrt(E_st / sy_st)
V.update(X1_Ld=f(LdC, 1), X1_dTy=f(sy_st / (E_st * a_st), 0))
bk = S["buckle"]
V.update(X1_N=f(-bk["N2"] / 1e3, 2), X1_Pcr=f(bk["Pcr"] / 1e3, 3), X1_dTcr=f(PI ** 2 * (6e-3 / 4) ** 2 / (a_al * (0.5 * bk["L"]) ** 2), 2))
# ------------------------------------------------------------------ X3 three members (independent event algorithm)
E3 = 97e3
A3 = PI / 4 * (32.0 ** 2 - 27.0 ** 2)
ks = [B_["k1"], B_["k2"], E3 * A3 / 150.0]
gaps = [0.0, B_["gap_mm"], B_["gap_mm"] + 0.040]
events = []
Pcur, Dcur = 0.0, 0.0
active = [True, False, False]
for j in (1, 2):
    kact = sum(k for k, a in zip(ks, active) if a)
    Pj = Pcur + (gaps[j] - Dcur) * kact
    events.append(Pj)
    Pcur, Dcur = Pj, gaps[j]
    active[j] = True
D30 = Dcur + (30e3 - Pcur) / sum(ks)
F3 = [-k * max(0.0, D30 - g) for k, g in zip(ks, gaps)]
V.update(X3_A3=f(A3, 1), X3_k3=f(ks[2] / 1e3, 1), X3_P1=f(events[0] / 1e3, 2), X3_P2=f(events[1] / 1e3, 2),
         X3_F1=f(F3[0] / 1e3, 2), X3_F2=f(F3[1] / 1e3, 2), X3_F3=f(F3[2] / 1e3, 2), X3_sum=f(sum(F3) / 1e3, 3))
# ------------------------------------------------------------------ D1
aL = a_al * 3000.0
V.update(D_aL=f(aL, 4), D_gmin=f(D_["g_min"], 2), D_gmax=f(D_["g_max"], 2), D_sigL_E=f(40 * 3000 / (A_["E"] * 1e3), 3),
         D_hot=f(a_al * 45 * 3000, 3), D_free_hot=f(D_["free_exp_hot"], 3), D_sig0=f(D_["sig_if_zero_gap"], 1),
         D_width=f(D_["g_max"] - D_["g_min"], 2), D_mid=f((D_["g_max"] + D_["g_min"]) / 2, 2),
         D_tol=f((D_["g_max"] - D_["g_min"]) / 2, 2), D_ua=f(math.sqrt(3) * 0 + 2 * HB["u_alpha"] * 45 * 3000, 3))
width_rule = 8.0 - a_al * 80 * 3000 + 40 * 3000 / (A_["E"] * 1e3)
V.update(D_rule_width=f(width_rule, 2), D_rule_tol=f(width_rule / 2, 2), D_rule_slope=f(aL, 4),
         D_rule_g15=f(8.0 - a_al * (15 + 25) * 3000 - width_rule / 2, 2))
# sensitivity of the bounds to E and alpha
V["D_dE"] = f(40 * 3000 / (A_["E"] * 1e3) * 2 * A_["uE"] / A_["E"], 3)

tmpl = (HERE / "lab02_instructor_key.template.md").read_text(encoding="utf-8")
missing = sorted(set(re.findall(r"«(\w+)»", tmpl)) - set(V))
if missing:
    raise SystemExit(f"missing values: {missing}")
out = re.sub(r"«(\w+)»", lambda m: V[m.group(1)], tmpl)
(HERE / "lab02_instructor_key.md").write_text(out, encoding="utf-8")
(HERE / "key_values.json").write_text(json.dumps(V, indent=1, ensure_ascii=False))
print("wrote lab02_instructor_key.md;", len(V), "values")

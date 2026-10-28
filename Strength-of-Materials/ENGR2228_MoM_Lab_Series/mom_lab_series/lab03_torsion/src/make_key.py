"""Generate lab03_instructor_key.md from computed results (no hand-typed numbers).

    python3 lab03_analysis.py && python3 make_key.py

Inputs: results.json (lab03_analysis.py on sample_data.csv), specimen_measurements.json, Lab 1's results.json
(for the Nadai comparison), and the simulation's own model code run in Node (dumped to sim_numbers.json).
Placeholders in the template are written «name».
"""
import json
import math
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
LAB = HERE.parent
R = json.loads((HERE / "results.json").read_text())
MEAS = json.loads((HERE / "specimen_measurements.json").read_text())
L1 = json.loads((LAB.parent / "lab01_stress_strain" / "src" / "results.json").read_text())["steel_1018HR"]
REF = MEAS["reference"]
S_, A_, CI, D_ = R["steel"], R["al"], R["ci"], R["design"]
V = {}
PI = math.pi
DEG = PI / 180


def f(x, nd):
    return f"{x:,.{nd}f}".replace(",", " ").replace("-", "−")


def pm(x, U, nd):
    return f"{f(x, nd)} ± {f(U, nd)}"


# ------------------------------------------------------------------ simulation numbers (exact page code)
JS = r"""
const {loadModel}=require('%s'); const M=loadModel('%s'); const o={};
const P=M.PRESETS, MA=M.MATERIALS;
for (const k of ['steel','al','ci']) { const p=Object.assign({},P[k]); const mat=MA[k]; const epp={law:'epp',G:mat.G,tauY:mat.tauY};
  const cf=M.circClosed(p,epp); const c=p.d/2;
  o[k]={TY:cf.TY,Tp:cf.Tp,phiY:cf.phiY,T_epp:cf.T,T_mat:M.torqueRings(mat,c,0,p.phi/p.L,64),phi:p.phi}; }
{ const p=Object.assign({},P.steel); const epp={law:'epp',G:MA.steel.G,tauY:MA.steel.tauY}; p.phi=3*epp.tauY*p.L/(epp.G*p.d/2);
  const cf=M.circClosed(p,epp); o.unload={phiP:cf.phiP,phi:p.phi,resSurf:cf.resSurf}; }
{ const p=Object.assign({},P.steel); p.phi=120*Math.PI/180; const mat=MA.steel, c=p.d/2, th=p.phi/p.L;
  const T=M.torqueRings(mat,c,0,th,256); o.beyond={T,elastic:T*c/M.Jp(c,0),surf:M.tauOf(mat,c*th),gamma:c*th}; }
{ const p=Object.assign({},P.al); const mat=MA.al, c=p.d/2, th=p.phi/p.L; o.al10={T_mat:M.torqueRings(mat,c,0,th,256),T_epp:M.eppTorque(c,0,mat.G,mat.tauY,th)}; }
{ const a=10e-3,b=10e-3,T=50; const s=M.rectSeries(a,b), fd=M.rectFD(a,b,16); const Jpol=a*b*(a*a+b*b)/12, cd=Math.hypot(a,b)/2;
  o.square={c1:s.c1,c2:s.c2,tau:T/(s.c1*a*b*b),misuse:T*cd/Jpol,tauFD:T/(fd.c1*a*b*b)}; }
{ const rows=[8,16,32].map((N)=>{const f=M.rectFD(2,1,N); return {N,c2:f.c2,k:f.k};}); o.rect2={rows,series:M.rectSeries(2,1)}; }
{ const p=Object.assign({},P.hollow); const epp={law:'epp',G:MA.epp.G,tauY:MA.epp.tauY}; const cf=M.circClosed(p,epp); o.hollow={ratio:cf.Tp/cf.TY, k:p.di/p.d}; }
{ const T=500,G=79.5e9; const b=M.tubeBredt(50e-3,10e-3,T,G), e=M.tubeExact(50e-3,10e-3,T,G); o.thick={bt:b.tau,et:e.tau,bth:b.theta,eth:e.theta}; }
console.log(JSON.stringify(o));
""" % ((LAB.parent / "shared" / "test_harness.js").as_posix(), (LAB / "lab03_simulation.html").as_posix())
SIM = json.loads(subprocess.run(["node", "-e", JS], capture_output=True, text=True, check=True).stdout)
(HERE / "sim_numbers.json").write_text(json.dumps(SIM, indent=1))

# ------------------------------------------------------------------ pre-lab (Table 1 values, nominal d)
c = 6.35e-3 / 2
J = PI * c ** 4 / 2
L = 50.8e-3
for key, sy, E, nu in (("s", 297.0, REF["E_steel_GPa"], REF["nu_steel"]), ("a", 274.0, REF["E_al_GPa"], REF["nu_al"])):
    tY = sy / math.sqrt(3) * 1e6
    G = E / (2 * (1 + nu)) * 1e9
    TY = tY * J / c
    phiY = tY * L / (G * c)
    V.update({f"P1_tY_{key}": f(tY / 1e6, 1), f"P1_G_{key}": f(G / 1e9, 2), f"P1_TY_{key}": f(TY, 2), f"P1_Tp_{key}": f(4 / 3 * TY, 2),
              f"P1_phiY_{key}": f(phiY / DEG, 3), f"P1_res_{key}": f(100 * 0.01 / (phiY / DEG), 2)})
V.update(P1_J=f(J * 1e12, 1), P1_Jc=f(J / c * 1e9, 2), P1_c3=f(c ** 3 * 1e9, 2), P1_Tmax=f(2 * PI / 3 * c ** 3 * 430e6, 1),
         P1_Tci=f(REF["sigUT_ci_MPa"] * 1e6 * J / c, 2))
k6 = 0.6
V["P2_hollow"] = f(4 / 3 * (1 - k6 ** 3) / (1 - k6 ** 4), 4)
Tm = 4 / 3 * (1 - 1 / 108)
V.update(P3_Tm=f(Tm, 4), P3_phip=f(3 - Tm, 4), P3_res_c=f(1 - Tm, 4), P3_res_rY=f(1 - Tm / 3, 4))
V.update(P4_pct=f(100 * 4 * 0.02 / 6.35, 2), P4_ud=f(0.0025 * 6.35 / 4 * 1e3, 1))
for k, kk in (("steel", "s"), ("al", "a"), ("ci", "c")):
    s = SIM[k]
    V.update({f"sim_TY_{kk}": f(s["TY"], 3), f"sim_Tp_{kk}": f(s["Tp"], 3), f"sim_Tepp_{kk}": f(s["T_epp"], 3), f"sim_Tmat_{kk}": f(s["T_mat"], 3)})
V["sim_al_diff"] = f(100 * (SIM["al"]["T_mat"] / SIM["al"]["T_epp"] - 1), 1)
V["sim_st_diff"] = f(100 * (SIM["steel"]["T_mat"] / SIM["steel"]["T_epp"] - 1), 2)
V["sim_phiP"] = f(SIM["unload"]["phiP"] / DEG, 3)
V["sim_phiA"] = f(SIM["unload"]["phi"] / DEG, 3)

# ------------------------------------------------------------------ analysis
for k, kk in (("steel", "s"), ("al", "a")):
    r = R[k]
    V.update({f"d_{kk}": f(r["d_mm"], 4), f"ud_{kk}": f(r["ud_mm"], 4), f"J_{kk}": f(r["J_mm4"], 2), f"uJ_{kk}": f(100 * r["uJ_rel"], 2),
              f"G_{kk}": pm(r["G_GPa"], 2 * r["uG_GPa"], 2), f"Gst_{kk}": f(100 * r["G_stat_rel"], 2), f"nG_{kk}": str(r["n_G"]),
              f"Gint_{kk}": f(r["G_int_Nm"], 3), f"Gp_{kk}": pm(r["G_pred_GPa"], 2 * r["uG_pred_GPa"], 2),
              f"Gd_{kk}": f(abs(r["G_GPa"] - r["G_pred_GPa"]), 2), f"Glim_{kk}": f(r["G_agree_lim"], 2),
              f"Gagree_{kk}": "agree" if abs(r["G_GPa"] - r["G_pred_GPa"]) <= r["G_agree_lim"] else "disagree",
              f"tY_{kk}": pm(r["tauY_MPa"], 2 * r["u_tauY_MPa"], 1), f"TY_{kk}": f(r["TY_Nm"], 3), f"Tp_{kk}": f(r["Tp_Nm"], 3),
              f"phiY_{kk}": f(r["phiY_deg"], 3), f"rms_{kk}": f(r["epp_rms_Nm"], 3), f"maxdev_{kk}": f(r["epp_maxdev_Nm"], 3),
              f"maxdevrel_{kk}": f(100 * r["epp_maxdev_rel"], 1), f"tYten_{kk}": f(r["tauY_from_tension_MPa"], 1), f"nfit_{kk}": str(r["n_fit"]),
              f"T10_{kk}": f(r["T_at_tropt_off"], 2), f"T10epp_{kk}": f(r["T_epp_at_off"], 3), f"T10ex_{kk}": f(100 * r["hardening_excess_rel"], 2),
              f"rYoff_{kk}": f(r["rY_over_c_off"], 3),
              f"Cm_{kk}": pm(r["Cm_deg_per_Nm"], r["uCm_deg_per_Nm"], 4), f"toe_{kk}": pm(r["toe_deg"], r["utoe_deg"], 3),
              f"hfrac_{kk}": f(100 * r["head_slope_frac"], 1), f"TU_{kk}": f(r["TU_Nm"], 2), f"RT_{kk}": pm(r["RT_MPa"], 2 * r["uRT_MPa"], 0),
              f"tpl_{kk}": f(r["tau_pl_MPa"], 0), f"gf_{kk}": f(r["gamma_f"], 3), f"rev_{kk}": f(r["phi_f_gage_rev"], 2),
              f"hrev_{kk}": f(r["head_f_rev"], 2), f"W_{kk}": f(r["W_J"], 0), f"dT_{kk}": f(r["dT_adiabatic_K"], 0),
              f"ttest_{kk}": f(r["test_time_s"], 0), f"V_{kk}": f(r["V_mm3"], 0)})
    if k == "steel":
        V["tYten_ratio_s"] = f(r["tauY_MPa"] / r["tauY_from_tension_MPa"], 3)
d_tY_a = A_["tauY_MPa"] - A_["tauY_from_tension_MPa"]
V["tYd_a"] = f(d_tY_a, 1)
V["tYd_a_pct"] = f(100 * d_tY_a / A_["tauY_from_tension_MPa"], 1)
V.update(phiA=f(S_["phiA_deg"], 2), TA=f(S_["TA_Nm"], 2), phires_m=f(S_["phi_res_meas_deg"], 2), phires_p=pm(S_["phi_res_pred_deg"], 2 * S_["u_phi_res_pred_deg"], 3),
         phires_ratio=f(S_["phi_res_epp_ratio"], 3), unl_slope=f(100 * S_["unload_slope_rel"], 2), res_c=f(S_["res_surf_MPa"], 1),
         res_rY=f(S_["res_rY_MPa"], 1), rY_A=f(S_["rY_A_mm"], 3))
V.update(Tf_ci=f(CI["Tf_Nm"], 2), RT_ci=pm(CI["RT_MPa"], 2 * CI["uRT_MPa"], 1), RTd_ci=f(abs(CI["RT_MPa"] - CI["sigUT_MPa"]), 1),
         RTlim_ci=f(CI["RT_agree_lim"], 1), d_ci=f(CI["d_mm"], 4), Gsl_ci=f(CI["G_secant_low_GPa"], 1), Gsf_ci=f(CI["G_secant_f_GPa"], 1),
         gf_ci=f(CI["gamma_f"], 5))
# Nadai vs Lab 1
K1, n1 = L1["K_hollomon"], L1["n_hollomon"]
rows = []
for gq in ("0.1", "0.5", "1.0", "1.5"):
    g = float(gq)
    t_nad = S_["nadai"][gq]["tau_MPa"]
    t_hol = K1 / math.sqrt(3) * (g / math.sqrt(3)) ** n1
    rows.append(f"γ = {gq}: Nadai {t_nad:.0f} MPa (fully plastic estimate {S_['nadai'][gq]['tau_pl_MPa']:.0f}, elastic formula {S_['nadai'][gq]['tau_el_MPa']:.0f}); Lab 1 Hollomon converted {t_hol:.0f} MPa")
V["nadai_rows"] = "; ".join(rows)
V.update(L1_K=f(K1, 0), L1_n=f(n1, 3), L1_neck_tau=f(L1["sig_t_neck_f"] / math.sqrt(3), 0), L1_neck_g=f(math.sqrt(3) * L1["eps_t_neck_f"], 2),
         nad15=f(S_["nadai"]["1.5"]["tau_MPa"], 0), nad01_a=f(A_["nadai"]["0.1"]["tau_MPa"], 0), nad05_a=f(A_["nadai"]["0.5"]["tau_MPa"], 0))
V["RT_over_nad"] = f(100 * (S_["RT_MPa"] / S_["nadai"]["1.5"]["tau_MPa"] - 1), 0)
# M1 from the simulation
b = SIM["beyond"]
V.update(M1_el=f(b["elastic"] / 1e6, 0), M1_surf=f(b["surf"] / 1e6, 0), M1_pct=f(100 * (b["elastic"] / b["surf"] - 1), 0), M1_g=f(b["gamma"], 3),
         M1_al_mat=f(SIM["al10"]["T_mat"], 3), M1_al_epp=f(SIM["al10"]["T_epp"], 3), M1_al_pct=f(100 * (SIM["al10"]["T_mat"] / SIM["al10"]["T_epp"] - 1), 1))
sq = SIM["square"]
V.update(sq_c1=f(sq["c1"], 4), sq_tau=f(sq["tau"] / 1e6, 1), sq_mis=f(sq["misuse"] / 1e6, 1), sq_pct=f(100 * (sq["misuse"] / sq["tau"] - 1), 1))
# C2, C3, X1
V.update(C2_06=V["P2_hollow"], C2_09=f(4 / 3 * (1 - 0.9 ** 3) / (1 - 0.9 ** 4), 4), C2_sim=f(SIM["hollow"]["ratio"], 4))
rr = SIM["rect2"]["rows"]
V["C3_rows"] = ", ".join(f"N = {r['N']}: {r['c2']:.5f}" for r in rr)
V["C3_rich"] = f((4 * rr[2]["c2"] - rr[1]["c2"]) / 3, 5)
V["C3_series"] = f(SIM["rect2"]["series"]["c2"], 5)
V["C3_ratio"] = f((rr[0]["c2"] - rr[1]["c2"]) / (rr[1]["c2"] - rr[2]["c2"]), 2)
th = SIM["thick"]
V.update(X1_bt=f(th["bt"] / 1e6, 1), X1_et=f(th["et"] / 1e6, 1), X1_pct=f(100 * (th["bt"] / th["et"] - 1), 1), X1_lead=f(-100 * 0.5 / 2, 0))
# X2 composite shaft
Gs, Ga = S_["G_GPa"] * 1e9, A_["G_GPa"] * 1e9
tYs, tYa = S_["tauY_MPa"] * 1e6, A_["tauY_MPa"] * 1e6
Js = PI * 0.010 ** 4 / 2
Ja = PI * (0.015 ** 4 - 0.010 ** 4) / 2
share = Js * Gs / (Js * Gs + Ja * Ga)
th_s, th_a = tYs / (Gs * 0.010), tYa / (Ga * 0.015)
th1 = min(th_s, th_a)
V.update(X2_Js=f(Js * 1e12, 0), X2_Ja=f(Ja * 1e12, 0), X2_share=f(share, 4), X2_ths=f(th_s, 4), X2_tha=f(th_a, 4),
         X2_first="the steel core" if th_s < th_a else "the aluminum sleeve", X2_T=f(th1 * (Js * Gs + Ja * Ga), 0))
# D1
V["D_T"] = f(D_["T_Nm"], 1)
for k, kk in (("steel", "s"), ("al", "a")):
    dd = D_[k]
    V.update({f"D_tlo_{kk}": f(dd["tau_lo_MPa"], 1), f"D_tall_{kk}": f(dd["tau_allow_MPa"], 1)})
    for name, nn in (("solid", "0"), ("hollow_0.6", "6"), ("hollow_0.8", "8")):
        o = dd["opts"][name]
        V.update({f"D_{kk}{nn}_ds": f(o["d_strength_mm"], 1), f"D_{kk}{nn}_dk": f(o["d_stiffness_mm"], 1), f"D_{kk}{nn}_d": f(o["d_mm"], 0),
                  f"D_{kk}{nn}_di": f(o["di_mm"], 1), f"D_{kk}{nn}_m": f(o["mass_kg"], 2), f"D_{kk}{nn}_cost": f(o["cost"], 2),
                  f"D_{kk}{nn}_tau": f(o["tau_max_MPa"], 1), f"D_{kk}{nn}_phi": f(o["phi_deg"], 3)})

tmpl = (HERE / "lab03_instructor_key.template.md").read_text(encoding="utf-8")
missing = sorted(set(re.findall(r"«(\w+)»", tmpl)) - set(V))
if missing:
    raise SystemExit(f"missing values: {missing}")
out = re.sub(r"«(\w+)»", lambda m: V[m.group(1)], tmpl)
(HERE / "lab03_instructor_key.md").write_text(out, encoding="utf-8")
(HERE / "key_values.json").write_text(json.dumps(V, indent=1, ensure_ascii=False))
print("wrote lab03_instructor_key.md;", len(V), "values")

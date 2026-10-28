"""Generate lab04_instructor_key.md from computed results (no hand-typed numbers).

    python3 lab04_analysis.py && python3 make_key.py

Inputs: results.json (lab04_analysis.py on sample_data.csv), specimen_measurements.json, and the simulation's own
model code run in Node (dumped to sim_numbers.json). Placeholders in the template are written «name».
"""
import json
import math
import re
import subprocess
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
LAB = HERE.parent
sys.path.insert(0, str(HERE))
from lab04_analysis import linfit, load, profile_fits  # noqa: E402
from lab04_model import composite_props, section_moment  # noqa: E402

R = json.loads((HERE / "results.json").read_text())
MEAS = json.loads((HERE / "specimen_measurements.json").read_text())
REF = MEAS["reference"]
G_, A_, B_, C_, D_ = R["geom"], R["A"], R["B"], R["C"], R["D"]
V = {}
R3 = math.sqrt(3)


def f(x, nd):
    return f"{x:,.{nd}f}".replace(",", " ").replace("-", "−")


def pm(x, U, nd):
    return f"{f(x, nd)} ± {f(U, nd)}"


def agree(d, lim):
    return "agree" if abs(d) <= lim else "disagree"


# ------------------------------------------------------------------ simulation numbers (exact page code)
JS = r"""
const {loadModel}=require('%s'); const M=loadModel('%s'); const o={};
const P=M.PRESETS, MA=M.MATERIALS;
{ const p=Object.assign({},P.fourpt); const c=M.beamClosed(p); const t=M.transformed(p,c.Mmax);
  o.A={Mmax:c.Mmax, smax:Math.abs(c.Mmax)*t.cTop/t.I, S:t.I/t.cTop, RA:c.re.RA}; }
{ const p=Object.assign({},P.composite); const t=M.transformed(p,1); o.B={ybar:t.ybar,I:t.I,n:MA.steel.E/MA.al.E};
  const q=Object.assign({},p,{mat2:'al'}); const t2=M.transformed(q,1); const Mb=1500;
  o.ign={ybar:t2.ybar, sb_true:M.MATERIALS.steel.E/MA.al.E*Mb*t.ybar/t.I, sb_ign:Mb*t2.ybar/t2.I, I2:t2.I}; }
{ const p=Object.assign({},P.plastic); const al=MA.al; const t=M.transformed(p,1);
  const mat=M.stripSolve(p,p.kappa,p.Ns,null), epp=M.stripSolve(p,p.kappa,p.Ns,{law:'epp'});
  o.C={k:p.kappa, Mmat:mat.M, Mepp_strip:epp.M, Mepp:M.eppRectM(p.b,p.h,al.E,al.sY,p.kappa), flex:mat.M*t.cBot/t.I, act:M.sigmaOf(al,p.kappa*mat.yNA),
       MY:al.sY*t.I/t.cTop, kY:al.sY/(al.E*t.cTop)};
  for (const P_ of [30e3,35e3,40e3]) { const Mx=P_/2*p.a; const k=M.invertKappa(p,Mx,400,null); const s=M.sigmaOf(al,k*p.h/2); (o.C.grow=o.C.grow||[]).push({P:P_,flex:Mx*t.cTop/t.I,act:s,k}); }
  const kY=al.sY/(al.E*p.h/2), k3=3*kY, Mu=M.stripSolve(p,k3,p.Ns,{law:'epp'}).M;
  o.unl={k:k3, M:Mu, kp:k3-Mu/(al.E*t.I), kpN:k3-M.invertKappa(p,Mu,p.Ns,{law:'epp',sY:1e30}), MY:al.sY*t.I/t.cTop};
  o.conv=[10,20,40].map((N)=>({N, err:(M.stripSolve(p,p.kappa,N,{law:'epp'}).M-o.C.Mepp)/o.C.Mepp}));
  o.convAll=M.stripConvergence(p,p.kappa,o.C.Mepp,{law:'epp'}); }
{ const p=Object.assign({},P.composite); const t=M.transformed(p,1); const Me=p.kappa*t.Eref*t.I;
  o.convB=[10,20,40].map((N)=>({N, M:M.stripSolve(p,p.kappa,N,{law:'epp',sY:1e30}).M, err:(M.stripSolve(p,p.kappa,N,{law:'epp',sY:1e30}).M-Me)/Me})); o.convB_Me=Me; }
{ const p=Object.assign({},P.ibeam); const z=M.plasticModulus(p), t=M.transformed(p,1); const mat=MA.epp; const k=0.2;
  const s=M.stripSolve(p,k,p.Ns,{law:'epp'}); o.I={Z:z.Z, S:t.I/(p.h/2), I:t.I, k:z.Z/(t.I/(p.h/2)), M02:s.M, MY:mat.sY*t.I/(p.h/2), Mp:mat.sY*z.Z, kY:mat.sY/(mat.E*p.h/2)};
  const q=Object.assign({},p,{shape:'tee'}); const zt=M.plasticModulus(q), tt=M.transformed(q,1); const cmax=Math.max(tt.cTop,tt.cBot);
  const big=1e4*mat.sY/(mat.E*p.h/2), st=M.stripSolve(q,big,4000,{law:'epp'});
  o.T={ybar:tt.ybar, yp:zt.yp, Z:zt.Z, S:tt.I/cmax, k:zt.Z/(tt.I/cmax), ypStrip:st.yNA, MpStrip:st.M, Mp:mat.sY*zt.Z, A:p.b*p.tf+p.tw*(p.h-p.tf)}; }
{ const p=Object.assign({},P.cantilever); const cv=M.beamConvergence(p,[2,4,8,16,32]); o.cant={rows:cv.rows, slope:cv.slope, Mmax:M.beamClosed(p).Mmax};
  const q=Object.assign({},P.fourpt,{N:2}); const cv2=M.beamConvergence(q,[2,4]); o.four=cv2.rows; }
console.log(JSON.stringify(o));
""" % ((LAB.parent / "shared" / "test_harness.js").as_posix(), (LAB / "lab04_simulation.html").as_posix())
SIM = json.loads(subprocess.run(["node", "-e", JS], capture_output=True, text=True, check=True).stdout)
(HERE / "sim_numbers.json").write_text(json.dumps(SIM, indent=1))

# ------------------------------------------------------------------ pre-lab (Table 1 values, nominal section)
E_al, nu_al, sY_al = REF["E_al_GPa"] * 1e9, REF["nu_al"], REF["sY_al_MPa"] * 1e6
E_st = REF["E_st_GPa"] * 1e9
b, h, L, a = 25.4e-3, 50.8e-3, 0.600, 0.200
I = b * h ** 3 / 12
S = I / (h / 2)
M20 = 20e3 / 2 * a
sig20 = M20 / S
eps20 = sig20 / E_al
k20 = M20 / (E_al * I)
MY = sY_al * S
PY = 2 * MY / a
Mp = 1.5 * MY
Pp = 2 * Mp / a
V.update(P1_I=f(I * 1e12 / 1e5, 4), P1_S=f(S * 1e9, 0), P1_M=f(M20, 0), P1_sig=f(sig20 / 1e6, 1), P1_eps=f(eps20 * 1e6, 0), P1_k=f(k20, 4),
         P1_rho=f(1 / k20, 2), P1_MY=f(MY, 0), P1_PY=f(PY / 1e3, 2), P1_Pp=f(Pp / 1e3, 2), P1_40Y=f(40e3 / PY, 3), P1_40p=f(40e3 / Pp, 3),
         P1_e25=f(eps20 / 8 * 1e6, 0), P1_res=f(100 / (eps20 / 8 * 1e6), 2), P1_tau=f(10e3 / (b * h) / 1e6, 2),
         P1_tau_pct=f(100 * (10e3 / (b * h)) / sig20, 1), P1_tau_max=f(1.5 * 10e3 / (b * h) / 1e6, 1))
# P2
for tag, a1, a2 in (("b", 0.2004, 0.3996), ("c", 0.2000, 0.3996)):
    RA = 0.5 * (2 * L - a1 - a2) / L               # per unit P
    Mmid = RA * L / 2 - 0.5 * (L / 2 - a1)          # per unit P (m)
    Vmid = RA - 0.5
    V.update({f"P2{tag}_RA": f(RA, 5), f"P2{tag}_RB": f(1 - RA, 5), f"P2{tag}_M": f(Mmid * 1e3, 3), f"P2{tag}_pct": f(100 * (Mmid / 0.1 - 1), 3),
              f"P2{tag}_V": f(Vmid, 6)})
V["P2c_dM"] = f(100 * abs(float(Vmid)) * 0.1996 / 0.1, 3)
# P3
cp = composite_props(25.4, 50.8, 6.35, E_al, E_st)
n = E_st / E_al
Mb = 15e3 / 2 * a
yb, It = cp["ybar"], cp["I"]
H = 50.8 + 6.35
s_st_bot = n * Mb * 1e3 * yb / It
s_al_int = -Mb * 1e3 * (6.35 - yb) / It
s_st_int = n * s_al_int
s_al_top = -Mb * 1e3 * (H - yb) / It
V.update(P3_n=f(n, 4), P3_ybar=f(yb, 3), P3_It=f(It / 1e5, 4), P3_Mb=f(Mb, 0), P3_stbot=f(s_st_bot, 1), P3_alint=f(s_al_int, 2), P3_stint=f(s_st_int, 1),
         P3_altop=f(s_al_top, 1), P3_Ibar=f(25.4 * 50.8 ** 3 / 12 / 1e5, 4), P3_gain=f(It / (25.4 * 50.8 ** 3 / 12), 3))
# P4 (EPP, nominal, Table 1)
kY = sY_al / (E_al * h / 2)
M40 = 40e3 / 2 * a
r = M40 / MY
yy = math.sqrt(3 * (1 - r / 1.5))                   # y_Y / c
k40 = kY / yy
kp = k40 - M40 / (E_al * I)
res_top = -sY_al + M40 / S
V.update(P4_MY=V["P1_MY"], P4_kY=f(kY, 4), P4_Mp=f(Mp, 0), P4_M=f(M40, 0), P4_r=f(r, 4), P4_yy=f(yy, 4), P4_k=f(k40, 4), P4_yY=f(yy * h / 2 * 1e3, 2),
         P4_kel=f(M40 / (E_al * I), 4), P4_kp=f(kp, 4), P4_res=f(res_top / 1e6, 1), P4_flex=f(M40 / S / 1e6, 1))
# P5 simulation
sA, sB, sC, sU = SIM["A"], SIM["B"], SIM["C"], SIM["unl"]
V.update(sim_MA=f(sA["Mmax"], 0), sim_sA=f(sA["smax"] / 1e6, 1), sim_ybB=f(sB["ybar"] * 1e3, 3), sim_IB=f(sB["I"] * 1e12 / 1e5, 4),
         sim_Cmat=f(sC["Mmat"], 0), sim_Cepp=f(sC["Mepp"], 0), sim_Cpct=f(100 * (sC["Mepp"] / sC["Mmat"] - 1), 2), sim_kC=f(sC["k"], 3),
         sim_unl_k=f(sU["k"], 4), sim_unl_kp=f(sU["kp"], 4), sim_unl_kpN=f(sU["kpN"], 4), sim_unl_M=f(sU["M"] / sU["MY"], 4))

# ------------------------------------------------------------------ analysis
V.update(b=pm(G_["b"], 2 * G_["ub"], 3), h=pm(G_["h"], 2 * G_["uh"], 3), ts=pm(G_["ts"], 2 * G_["uts"], 3), I=f(G_["I_mm4"] / 1e5, 4),
         uI=f(100 * G_["uI_rel"], 3), a=pm(G_["a"], 2 * G_["ua"], 2))
data = load(LAB / "sample_data.csv")
fitsA = profile_fits(data["A"], MEAS["yA_mm"], G_["h"])
PA = data["A"]["load_N"]
sel = PA > 1000
rmsA = [f_["rms"] for f_, s_ in zip(fitsA, sel) if s_]
V.update(A2_n=str(int(sel.sum())), A2_rmsmax=f(max(rmsA), 2), A2_rmsmin=f(min(rmsA), 2), A2_rms20=f(A_["rms20"], 2),
         A2_yNA=pm(A_["yNA"], 2 * A_["u_yNA"], 3), A2_h2=f(A_["h_half"], 3), A2_off=f(A_["yNA_off"], 3), A2_lim=f(2 * A_["u_yNA"], 3))
i20 = int(np.argmax(PA))
et, eb = data["A"]["strain_top_ue"][i20], data["A"]["strain_bottom_ue"][i20]
V.update(A2_et=f(et, 0), A2_eb=f(eb, 0), A2_k20=f(A_["kappa20"], 5))
for j, P_ in enumerate((5e3, 10e3, 20e3)):
    i = int(np.argmin(abs(PA[: i20 + 1] - P_)))
    V[f"A2_k{int(P_ / 1e3)}"] = f(fitsA[i]["kappa"], 5)
# A1
ex = A_["Ex"]
for k in ("100", "150", "300"):
    V[f"A1_M{k}"] = f(ex[k]["M_per_N"] * 1e3, 2)
    V[f"A1_S{k}"] = f(float(k) / 2, 1) if k != "300" else f(100.0, 1)
    V[f"A1_d{k}"] = f(100 * (ex[k]["M_per_N"] / (min(float(k), 200.0) / 2e3) - 1), 2)
slope = A_["V_per_N"]
icpt = ex["100"]["M_per_N"] - 0.1 * slope
V.update(A1_V=pm(slope, 2 * A_["uV_per_N"], 4), A1_Vd=f(abs(slope - 0.5), 4), A1_Vlim=f(2 * A_["uV_per_N"], 4), A1_icpt=f(icpt * 1e3, 3),
         A1_icpt_mm=f(-icpt / slope * 1e3, 2), A1_agree=agree(slope - 0.5, 2 * A_["uV_per_N"]), A1_uM=f(100 * ex["100"]["u_rel"], 2))
# A3
uE_rel = A_["uE"] / A_["E"]
terms = {"slope": A_["E_stat_rel"], "b": G_["ub"] / G_["b"], "h": 3 * G_["uh"] / G_["h"], "a": G_["ua"] / G_["a"],
         "P": MEAS["load_cell_accuracy_pct"] / 100 / R3, "GF": MEAS["gage_factor_tolerance_pct"] / 100 / R3}
V.update(A3_E=pm(A_["E"], 2 * A_["uE"], 2), A3_Eref=pm(REF["E_al_GPa"], 2 * REF["u_E_al_GPa"], 2), A3_d=f(abs(A_["E"] - REF["E_al_GPa"]), 2),
         A3_lim=f(A_["E_agree_lim"], 2), A3_agree=agree(A_["E"] - REF["E_al_GPa"], A_["E_agree_lim"]), A3_n=str(A_["n_steps"]),
         A3_urel=f(100 * uE_rel, 3), A3_sflex=f(A_["sigma_flex20"], 1), A3_sEe=f(A_["sigma_bot20"], 1), A3_eb=f(A_["eps_bot20"], 0),
         A3_EI=f(A_["E"] * 1e9 * G_["I_mm4"] * 1e-12, 0))
for k, v in terms.items():
    V[f"A3_t_{k}"] = f(100 * v, 3)
# A4
V.update(A4_nu=pm(A_["nu"], 2 * A_["unu"], 4), A4_d=f(abs(A_["nu"] - REF["nu_al"]), 4), A4_lim=f(A_["nu_agree_lim"], 4),
         A4_agree=agree(A_["nu"] - REF["nu_al"], A_["nu_agree_lim"]), A4_rho=f(1 / A_["kappa20"], 2), A4_rhop=f(1 / (A_["kappa20"] * A_["nu"]), 1),
         A4_ttop=f(data["A"]["strain_transverse_top_ue"][i20], 0))
# A5
lim_y = 2 * math.hypot(B_["u_yNA"], B_["u_ybar_pred"])
lim_EI = 2 * math.hypot(B_["uEI_meas"], B_["uEI_pred"])
V.update(A5_y=pm(B_["yNA"], 2 * B_["u_yNA"], 3), A5_yp=pm(B_["ybar_pred"], 2 * B_["u_ybar_pred"], 2), A5_yd=f(abs(B_["yNA"] - B_["ybar_pred"]), 3),
         A5_ylim=f(lim_y, 3), A5_yagree=agree(B_["yNA"] - B_["ybar_pred"], lim_y), A5_n=f(B_["n"], 4), A5_It=f(B_["I_t_mm4"] / 1e5, 4),
         A5_EI=pm(B_["EI_meas"], 2 * B_["uEI_meas"], 0), A5_EIp=pm(B_["EI_pred"], 2 * B_["uEI_pred"], 0), A5_EId=f(abs(B_["EI_meas"] - B_["EI_pred"]), 0),
         A5_EIlim=f(lim_EI, 0), A5_EIagree=agree(B_["EI_meas"] - B_["EI_pred"], lim_EI), A5_EIpct=f(100 * (B_["EI_meas"] / B_["EI_pred"] - 1), 2),
         A5_P=f(B_["P"] / 1e3, 3), A5_M=f(B_["M"], 1), A5_N=f(100 * B_["N_resid_frac"], 2), A5_gain=f(B_["stiff_gain"], 3), A5_rms=f(B_["rms"], 2),
         A5_H=f(B_["H"], 2), A5_hom=f(B_["ybar_homog"], 2), A5_EIal=f(B_["EI_alone"], 0))
for k in ("st_bot", "al_int", "st_int", "al_top"):
    V[f"A5_m_{k}"] = f(B_[f"sig_{k}"], 1)
    V[f"A5_p_{k}"] = f(B_[f"pred_{k}"], 1)
    V[f"A5_d_{k}"] = f(100 * (B_[f"sig_{k}"] / B_[f"pred_{k}"] - 1), 2)
# A6
nC = len(C_["M_epp"])
rowsC = []
for i in range(1, nC):
    rowsC.append(f"| {f(C_['P'][i] / 1e3, 1)} | {f(C_['M'][i], 0)} | {f(C_['kappa'][i], 4)} | {f(C_['M_epp'][i], 0)} | {f(C_['M_ro'][i], 0)} | {f(C_['yNA'][i], 2)} | {f(C_['rms'][i], 1)} |")
V["A6_table"] = "\n".join(rowsC)
Mmx, kmx = C_["Mmax"], C_["kmax"]
kel = Mmx / (A_["E"] * 1e9 * G_["I_mm4"] * 1e-12)
kY_m = C_["kY"]
r_m = Mmx / C_["MY"]
k_epp = kY_m / math.sqrt(3 * (1 - r_m / 1.5))
V.update(A6_MY=f(C_["MY"], 0), A6_Mp=f(C_["Mp"], 0), A6_kY=f(C_["kY"], 4), A6_kmax=f(kmx, 4), A6_Mmax=f(Mmx, 0), A6_Mepp=f(C_["M_epp_max"], 0),
         A6_Mro=f(C_["M_ro_max"], 0), A6_eppct=f(100 * (C_["M_epp_max"] / Mmx - 1), 2), A6_ropct=f(100 * (C_["M_ro_max"] / Mmx - 1), 2),
         A6_emax=f(C_["eps_max"] * 100, 3), A6_sflex=f(C_["sig_flex"], 1), A6_sact=f(C_["sig_actual"], 1), A6_over=f(100 * C_["flex_over"], 1),
         A6_kres=f(C_["k_res_meas"], 4), A6_kresp=pm(C_["k_res_pred"], 2 * C_["u_k_res_pred"], 4), A6_kel=f(kel, 4),
         A6_kresd=f(abs(C_["k_res_meas"] - C_["k_res_pred"]), 4), A6_kreslim=f(2 * C_["u_k_res_pred"], 4),
         A6_kresagree=agree(C_["k_res_meas"] - C_["k_res_pred"], 2 * C_["u_k_res_pred"]),
         A6_kepp=f(k_epp, 4), A6_kpepp=f(k_epp - kel, 4), A6_kp_ratio=f(C_["k_res_meas"] / (k_epp - kel), 2),
         A6_res=f(C_["res_surf"], 1), A6_rms40=f(C_["rms_max"], 2), A6_rms20=f(C_["rms_A20"], 2), A6_rmsk40=f(C_["rms_max"] / kmx, 1),
         A6_rmsk20=f(C_["rms_A20"] / A_["kappa20"], 1), A6_nueff=f(C_["nu_eff"], 3), A6_x150=f(C_["eps_x150_max"], 0), A6_x150r=f(C_["eps_x150_res"], 0),
         A6_yNA40=f(C_["yNA"][int(np.argmax(C_["P"]))], 2), A6_ratio=f(r_m, 3))
# A6: straightedge gap
V.update(A6_gap=pm(C_["gap_meas"], 2 * C_["u_gap_meas"], 2), A6_gapmid=pm(C_["gap_mid"], 2 * C_["u_gap_mid"], 2), A6_gapdata=f(C_["gap_data"], 2),
         A6_gapdiff=f(C_["gap_meas"] - C_["gap_mid"], 2), A6_gaplim=f(2 * math.hypot(C_["u_gap_meas"], C_["u_gap_mid"]), 2), A6_xY=f(C_["x_yield"], 1),
         A6_gappct=f(100 * (C_["gap_meas"] / C_["gap_mid"] - 1), 0))
# A6: residual surface strain from the measured permanent curvature
V["A6_eres"] = f(C_["k_res_meas"] * G_["h"] / 2 * 1e3, 0)
# M1 (simulation)
gr = SIM["C"]["grow"]
V["M1_grow"] = "; ".join(f"{g['P'] / 1e3:.0f} kN: {g['flex'] / 1e6:.0f} vs {g['act'] / 1e6:.0f} MPa ({100 * (g['flex'] / g['act'] - 1):.0f} %)" for g in gr)
V.update(M1_flex=f(sC["flex"] / 1e6, 1), M1_act=f(sC["act"] / 1e6, 1), M1_pct=f(100 * (sC["flex"] / sC["act"] - 1), 1), M1_ro=f(100 * (1 - sC["act"] / sC["flex"]), 0),
         M1_ign_y=f(SIM["ign"]["ybar"] * 1e3, 2), M1_true_y=f(sB["ybar"] * 1e3, 2), M1_dy=f((SIM["ign"]["ybar"] - sB["ybar"]) * 1e3, 2),
         M1_sb_true=f(SIM["ign"]["sb_true"] / 1e6, 1), M1_sb_ign=f(SIM["ign"]["sb_ign"] / 1e6, 1),
         M1_sb_ratio=f(SIM["ign"]["sb_true"] / SIM["ign"]["sb_ign"], 2))
# C1 (I-beam), C2 convergence, X3 T-section
sI = SIM["I"]
V.update(C1_Z=f(sI["Z"] * 1e9 / 1e3, 1), C1_S=f(sI["S"] * 1e9 / 1e3, 1), C1_k=f(sI["k"], 4), C1_M02=f(sI["M02"] / sI["MY"], 4), C1_kk=f(0.2 / sI["kY"], 1),
         C1_Mp=f(sI["Mp"] / 1e3, 1), C1_MY=f(sI["MY"] / 1e3, 1))
def sci(x, nd=2):
    m, e = f"{x:.{nd}e}".split("e")
    return f"{m.replace('-', '−')} × 10{''.join('⁰¹²³⁴⁵⁶⁷⁸⁹'[int(c)] if c.isdigit() else '⁻' for c in str(int(e)))}"


cv = SIM["conv"]
V["C2_rows"] = ", ".join(f"$N_s$ = {r_['N']}: {sci(r_['err'])}" for r_ in cv)
V["C2_ratio"] = f(cv[0]["err"] / cv[1]["err"], 1) + " and " + f(cv[1]["err"] / cv[2]["err"], 1)
V["C2_slopeAll"] = f(SIM["convAll"]["slope"], 2)
cb = SIM["convB"]
V["C2B_rows"] = ", ".join(f"$N_s$ = {r_['N']}: {sci(r_['err'])}" for r_ in cb)
V["C2B_ratio"] = f(cb[0]["err"] / cb[1]["err"], 3) + " and " + f(cb[1]["err"] / cb[2]["err"], 3)
rich = (4 * cb[2]["M"] - cb[1]["M"]) / 3
V["C2B_rich"] = sci((rich - SIM["convB_Me"]) / SIM["convB_Me"])
V["C2B_Me"] = f(SIM["convB_Me"], 2)
cr = SIM["cant"]["rows"]
V["C2_cant"] = ", ".join(f"N = {r_['N']}: {sci(r_['err'])}" for r_ in cr)
V["C2_slope"] = f(SIM["cant"]["slope"], 2)
V["C2_four"] = f(max(r_["err"] for r_ in SIM["four"]), 1) if max(r_["err"] for r_ in SIM["four"]) > 0 else "0"
sT = SIM["T"]
V.update(X3_ybar=f(sT["ybar"] * 1e3, 2), X3_yp=f(sT["yp"] * 1e3, 2), X3_Z=f(sT["Z"] * 1e9 / 1e3, 1), X3_S=f(sT["S"] * 1e9 / 1e3, 1), X3_k=f(sT["k"], 3),
         X3_ypS=f(sT["ypStrip"] * 1e3, 2), X3_MpS=f(sT["MpStrip"] / sT["Mp"], 5), X3_A=f(sT["A"] * 1e6, 0))
# C3 (c): sensitivity of kappa to a 0.1 mm error in one gage height (sample geometry, Part A at 20 kN)
y = np.r_[MEAS["yA_mm"], G_["h"], 0.0]
e = np.array([data["A"][c][i20] for c in ["strain_side1_ue", "strain_side2_ue", "strain_side3_ue", "strain_side4_ue", "strain_side5_ue", "strain_top_ue", "strain_bottom_ue"]])
_, s0, *_ = linfit(y, e)
worst = 0.0
for j in range(5):
    y2 = y.copy(); y2[j] += 0.1
    _, s1, *_ = linfit(y2, e)
    worst = max(worst, abs(s1 / s0 - 1))
V.update(C3_dk=f(100 * worst, 3), C3_eps=f(A_["kappa20"] * 0.1e-3 * 1e6, 1), C3_Sxx=f(float(np.sum((y - y.mean()) ** 2)), 0))
# X1 bimetal: free thermal curvature by equilibrium + compatibility (strip method), per kelvin, and interface stresses at 50 K
al_a, st_a = 23.6e-6, 11.7e-6
bb, hh, tt = G_["b"] * 1e-3, G_["h"] * 1e-3, G_["ts"] * 1e-3
Ea, Es = A_["E"] * 1e9, E_st


def bimetal(dT):
    # unknowns: strain at the bottom e0 and curvature k (sagging positive); eps(y) = e0 - k*y, y from the bottom
    # stresses: E(eps - alpha dT); N = 0, M = 0 about y = 0
    def NM(Ei, ai, y0, y1):
        A = bb * (y1 - y0); Q = bb * (y1 ** 2 - y0 ** 2) / 2; Iz = bb * (y1 ** 3 - y0 ** 3) / 3
        return np.array([[Ei * A, -Ei * Q], [Ei * Q, -Ei * Iz]]), np.array([Ei * ai * dT * A, Ei * ai * dT * Q])
    K1, r1 = NM(Es, st_a, 0, tt)
    K2, r2 = NM(Ea, al_a, tt, tt + hh)
    sol = np.linalg.solve(K1 + K2, r1 + r2)
    e0, k = sol
    eps_int = e0 - k * tt
    return k, Es * (eps_int - st_a * dT), Ea * (eps_int - al_a * dT), Es * (e0 - st_a * dT), Ea * (e0 - k * (tt + hh) - al_a * dT)


k1, *_ = bimetal(1.0)
k50, s_st_i, s_al_i, s_st_b, s_al_t = bimetal(50.0)
V.update(X1_k=f(k1 * 1e3, 4), X1_k50=f(k50, 4), X1_rho=f(1 / abs(k50), 1), X1_st_i=f(s_st_i / 1e6, 1), X1_al_i=f(s_al_i / 1e6, 1), X1_st_b=f(s_st_b / 1e6, 1),
         X1_al_t=f(s_al_t / 1e6, 1), X1_sense="hogging (concave down)" if k1 < 0 else "sagging (concave up)")
# X2: residual extreme-fiber stress after unloading from M_max (EPP rectangle), reverse yield moment
V.update(X2_resP=f(1 - 1.5, 2))
# D1
V["D_M"] = f(D_["M_Nm"] / 1e3, 3)
V["D_dmax"] = f(D_["dmax_mm"], 1)
for k, kk in (("steel", "s"), ("al", "a")):
    dd = D_["rows"][k]
    V.update({f"D_sY_{kk}": f(dd["sY_lo"], 1), f"D_sall_{kk}": f(dd["s_allow"], 1), f"D_Sreq_{kk}": f(dd["S_req"] / 1e3, 2), f"D_Ireq_{kk}": f(dd["I_req"] / 1e6, 3),
              f"D_best_{kk}": dd["best"]["name"], f"D_bm_{kk}": f(dd["best"]["mass"], 2), f"D_bM_{kk}": f(dd["best"]["mass"] * 3, 1), f"D_bc_{kk}": f(dd["best"]["cost"], 0),
              f"D_bs_{kk}": f(dd["best"]["sigma"], 1), f"D_bd_{kk}": f(dd["best"]["defl"], 2), f"D_bus_{kk}": f(dd["best"]["sigma"] / dd["s_allow"], 2),
              f"D_bud_{kk}": f(dd["best"]["defl"] / D_["dmax_mm"], 2)})
    rows = []
    for t in dd["table"]:
        rows.append(f"| {t['name']} | {f(t['mass'], 2)} | {f(t['sigma'], 1)} | {f(t['defl'], 2)} | {'yes' if t['ok'] else 'no'} |")
    V[f"D_table_{kk}"] = "\n".join(rows)
V["D_Eal"] = f(A_["E"], 2)

tmpl = (HERE / "lab04_instructor_key.template.md").read_text(encoding="utf-8")
missing = sorted(set(re.findall(r"«(\w+)»", tmpl)) - set(V))
if missing:
    raise SystemExit(f"missing values: {missing}")
out = re.sub(r"«(\w+)»", lambda m: V[m.group(1)], tmpl)
(HERE / "lab04_instructor_key.md").write_text(out, encoding="utf-8")
(HERE / "key_values.json").write_text(json.dumps(V, indent=1, ensure_ascii=False))
print("wrote lab04_instructor_key.md;", len(V), "values")

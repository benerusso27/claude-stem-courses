"""Generate lab08_instructor_key.md from computed results (no hand-typed numbers).

    python3 lab08_analysis.py && python3 make_key.py

Inputs: results.json (lab08_analysis.py on sample_data.csv), specimen_measurements.json, and the simulation's own
model code run in Node (dumped to sim_numbers.json). Placeholders in the template are written «name».
"""
import json
import math
import re
import subprocess
from pathlib import Path

import lab08_model as LM

HERE = Path(__file__).resolve().parent
LAB = HERE.parent
OUT = json.loads((HERE / "results.json").read_text())
R, U = OUT["res"], {k: 2 * v for k, v in OUT["u"].items()}            # U = 2u
MEAS = json.loads((HERE / "specimen_measurements.json").read_text())
REF = MEAS["reference"]
V = {}


def f(x, nd):
    if abs(x) < 0.5 * 10 ** (-nd):
        x = 0.0
    return f"{x:,.{nd}f}".replace(",", " ").replace("-", "−")


def pm(x, Ux, nd):
    return f"{f(x, nd)} ± {f(Ux, nd)}"


def agree(d, lim):
    return "agree" if abs(d) <= lim else "disagree"


MPa = 1e-6
# ------------------------------------------------------------------ simulation numbers (exact page code)
JS = r"""
const {loadModel}=require('%s'); const M=loadModel('%s'); const o={}, P=M.PRESETS, D=M.D;
const st=(k,phi)=>{ const s=M.tubeState(P[k],phi), m=M.mohr(s.sx,s.sy,s.txy), mat=M.MATERIALS.al, e=M.strainsOf(s.sx,s.sy,s.txy,mat.E,mat.nu); return {s1:m.s1,s2:m.s2,th:m.thp,R:m.R,rd:M.ktForward(e.ex,e.ey,e.g,M.ANGLES.rect,0,0), p3:M.principal3(s)}; };
o.H=st('partB',0); o.K=st('partBK',90*D); o.X=st('partCc',0);
const c0=M.rosetteReduce(P.crooked), c5=M.rosetteReduce(Object.assign({},P.crooked,{beta:5*D}));
const hs=(r)=>M.hooke(r.cf.ex,r.cf.ey,r.cf.g,P.crooked.E,P.crooked.nu);
o.cr={sx0:hs(c0).sx, t0:hs(c0).txy, sx5:hs(c5).sx, t5:hs(c5).txy, s10:M.mohr(hs(c0).sx,hs(c0).sy,hs(c0).txy).s1, s15:M.mohr(hs(c5).sx,hs(c5).sy,hs(c5).txy).s1};
console.log(JSON.stringify(o));
""" % ((LAB.parent / "shared" / "test_harness.js").as_posix(), (LAB / "lab08_simulation.html").as_posix())
SIM = json.loads(subprocess.run(["node", "-e", JS], capture_output=True, text=True, check=True).stdout)
(HERE / "sim_numbers.json").write_text(json.dumps(SIM, indent=1))

# ------------------------------------------------------------------ pre-lab (nominal tube, Table 1)
E2, nu2 = REF["E_al_GPa"] * 1e9, REF["nu_al"]
G2 = E2 / (2 * (1 + nu2))
Do, Di = 38.1e-3, 31.75e-3
tp = LM.tube_props(Do, Di)
H = LM.tube_state(Do, Di, 600, 0.2, 0.25, 0, 0.0)
K = LM.tube_state(Do, Di, 600, 0.2, 0.25, 0, math.pi / 2)
s1, s2, th = LM.principal2(H["sx"], H["sy"], H["txy"])
Rn = (s1 - s2) / 2
ex, ey, g = LM.state_strains(H["sx"], H["sy"], H["txy"], E2, nu2)
rd = LM.gage_readings(ex, ey, g)
V.update(P_I=f(tp["I"] * 1e12, 0), P_J=f(tp["J"] * 1e12, 0), P_Q=f(2 * (tp["ro"] ** 3 - tp["ri"] ** 3) / 3 * 1e9, 0), P_G=f(G2 / 1e9, 2),
         P1_sx=f(H["sx"] * MPa, 2), P1_t=f(H["txy"] * MPa, 2), P1_mt=f(-H["txy"] * MPa, 2), P1_ave=f((s1 + s2) / 2 * MPa, 2), P1_R=f(Rn * MPa, 2),
         P1_s1=f(s1 * MPa, 2), P1_s2=f(s2 * MPa, 2), P1_th=f(math.degrees(th), 2), P1_2th=f(abs(2 * math.degrees(th)), 1), P1_thabs=f(abs(math.degrees(th)), 1),
         P1_tT=f(K["tauT"] * MPa, 2), P1_tV=f(K["tauV"] * MPa, 2), P1_tK=f(K["txy"] * MPa, 2),
         P1_ex=f(ex * 1e6, 1), P1_ey=f(ey * 1e6, 1), P1_g=f(g * 1e6, 1), P1_rd=", ".join(f(x * 1e6, 1) for x in rd))
th_thin, x_thin = 8e6 * tp["ri"] / tp["t"], 8e6 * tp["ri"] / (2 * tp["t"])
_, th_l, x_l = LM.lame_closed(8e6, tp["ri"], tp["ro"], tp["ro"])
V.update(P1_th_thin=f(th_thin * MPa, 2), P1_x_thin=f(x_thin * MPa, 2), P1_th_lame=f(th_l * MPa, 2), P1_x_lame=f(x_l * MPa, 2))
r2 = LM.gage_readings(ex, ey, g, beta=math.radians(2))
e2x, e2y, g2_ = LM.rosette_solve(LM.RECT, r2)
V.update(P3_rd=", ".join(f(x * 1e6, 1) for x in r2), P3_ex=f(e2x * 1e6, 1), P3_g=f(g2_ * 1e6, 1), P3_dex=f((e2x - ex) * 1e6, 1), P3_dg=f((g2_ - g) * 1e6, 1),
         P3_e1=f(((e2x + e2y) / 2 + math.hypot((e2x - e2y) / 2, g2_ / 2)) * 1e6, 1))
X = LM.tube_state(Do, Di, 600, 0.2, 0.25, 8e6, 0.0)
x1, x2, _ = LM.principal2(X["sx"], X["sy"], X["txy"])
V.update(P4_sx=f(X["sx"] * MPa, 2), P4_sy=f(X["sy"] * MPa, 2), P4_s1=f(x1 * MPa, 2), P4_s2=f(x2 * MPa, 2), P4_R=f((x1 - x2) / 2 * MPa, 2), P4_tabs=f(x1 / 2 * MPa, 2))
S_ = SIM
V.update(sim_H_s1=f(S_["H"]["s1"] * MPa, 2), sim_H_s2=f(S_["H"]["s2"] * MPa, 2), sim_H_th=f(math.degrees(S_["H"]["th"]), 2), sim_H_rd=", ".join(f(x * 1e6, 1) for x in S_["H"]["rd"]),
         sim_K_s1=f(S_["K"]["s1"] * MPa, 2), sim_K_s2=f(S_["K"]["s2"] * MPa, 2), sim_K_th=f(math.degrees(S_["K"]["th"]), 1), sim_K_rd=", ".join(f(x * 1e6, 1) for x in S_["K"]["rd"]),
         sim_X_R=f(S_["X"]["R"] * MPa, 2), sim_X_tabs=f((S_["X"]["p3"][0] - S_["X"]["p3"][2]) / 2 * MPa, 2),
         sim_cr_sx0=f(S_["cr"]["sx0"] * MPa, 2), sim_cr_t0=f(S_["cr"]["t0"] * MPa, 2), sim_cr_sx5=f(S_["cr"]["sx5"] * MPa, 2), sim_cr_t5=f(S_["cr"]["t5"] * MPa, 2),
         sim_cr_s1=f(S_["cr"]["s15"] * MPa, 2))
assert abs(S_["cr"]["s10"] - S_["cr"]["s15"]) < 1e-6 * abs(S_["cr"]["s15"])
# P6: von Mises at 600 N with 8 MPa, outer (H) and inner surface at the top
vm_o = LM.von_mises(LM.principal3([[X["sx"], X["txy"], 0], [X["txy"], X["sy"], 0], [0, 0, 0]]))
ri, ro, I, J = tp["ri"], tp["ro"], tp["I"], tp["J"]
sr_i, st_i, sa_i = LM.lame_closed(8e6, ri, ro, ri)
sx_i, t_i = 600 * 0.25 * ri / I + sa_i, -600 * 0.2 * ri / J
vm_i = LM.von_mises(LM.principal3([[sx_i, t_i, 0], [t_i, st_i, 0], [0, 0, sr_i]]))
V.update(P6_vm=f(vm_o * MPa, 1), P6_vm_in=f(vm_i * MPa, 1), P6_pct=f(100 * max(vm_o, vm_i) / (REF["sY_al_MPa"] * 1e6), 0))

# ------------------------------------------------------------------ results at a glance and analysis
V.update(Do=pm(OUT["Do"], 2 * OUT["uDo"], 3), tw=pm(OUT["t"], 2 * OUT["ut"], 3), bH=pm(R["beta_H"], U["beta_H"], 2), bK=pm(R["beta_K"], U["beta_K"], 2),
         E_A=pm(R["E_A"] / 1e9, U["E_A"] / 1e9, 2), ref_E=pm(REF["E_al_GPa"], 2 * REF["u_E_al_GPa"], 2), nu_A=pm(R["nu_A"], U["nu_A"], 4),
         ref_nu=pm(REF["nu_al"], 2 * REF["u_nu_al"], 4), ref_G=pm(REF["G_al_GPa"], 2 * REF["u_G_al_GPa"], 2))
E_lim = 2 * math.hypot(U["E_A"] / 2 / 1e9, REF["u_E_al_GPa"])
nu_lim = 2 * math.hypot(U["nu_A"] / 2, REF["u_nu_al"])
V.update(E_ag=agree(R["E_A"] / 1e9 - REF["E_al_GPa"], E_lim), E_d=f(abs(R["E_A"] / 1e9 - REF["E_al_GPa"]), 2), E_lim=f(E_lim, 2),
         nu_ag=agree(R["nu_A"] - REF["nu_al"], nu_lim))
G3_lim = 2 * math.hypot(U["G_mean"] / 2 / 1e9, REF["u_G_al_GPa"])
dGA = R["G_mean"] - R["G_A"]
V.update(G_mean=pm(R["G_mean"] / 1e9, U["G_mean"] / 1e9, 2), G_A=pm(R["G_A"] / 1e9, U["G_A"] / 1e9, 2), G_H=pm(R["G_H"] / 1e9, U["G_H"] / 1e9, 2), G_K=pm(R["G_K"] / 1e9, U["G_K"] / 1e9, 2),
         G_ag3=agree(R["G_mean"] / 1e9 - REF["G_al_GPa"], G3_lim), G_d3=f(abs(R["G_mean"] / 1e9 - REF["G_al_GPa"]), 2), G_lim3=f(G3_lim, 2),
         G_agA=agree(dGA, 2 * math.hypot(U["G_mean"] / 2, U["G_A"] / 2)), G_pct=f(100 * abs(R["G_mean"] / 1e9 / REF["G_al_GPa"] - 1), 1))
for g in "HK":
    V.update({f"B{g}_s1": pm(R[f"B{g}_s1"] * MPa, U[f"B{g}_s1"] * MPa, 2), f"B{g}_s2": pm(R[f"B{g}_s2"] * MPa, U[f"B{g}_s2"] * MPa, 2),
              f"B{g}_th": pm(R[f"B{g}_th"], U[f"B{g}_th"], 2), f"B{g}_s1_p": f(R[f"B{g}_s1_p"] * MPa, 2), f"B{g}_s2_p": f(R[f"B{g}_s2_p"] * MPa, 2),
              f"B{g}_th_p": f(R[f"B{g}_th_p"], 2), f"B{g}_d1": f(abs(R[f"B{g}_ds1"]) * MPa, 2), f"B{g}_d2": f(abs(R[f"B{g}_ds2"]) * MPa, 2),
              f"B{g}_l1": f(U[f"B{g}_ds1"] * MPa, 2), f"B{g}_l2": f(U[f"B{g}_ds2"] * MPa, 2)})
    ok = abs(R[f"B{g}_ds1"]) <= U[f"B{g}_ds1"] and abs(R[f"B{g}_ds2"]) <= U[f"B{g}_ds2"]
    V[f"B{g}_ag"] = "both agree" if ok else ("σ_max agrees; σ_min does not" if abs(R[f"B{g}_ds1"]) <= U[f"B{g}_ds1"] else "disagree")
V["BH_th_ag"] = agree(R["BH_dth"], U["BH_dth"])
V["BK_s1_p"] = f(R["BK_s1_p"] * MPa, 2)
V["BK_sx"] = f(R["BK_sx"] * MPa, 2)
# K at its measured height: bending stress sx_K = sigma_top * sin(phi_off); principal values of (sx_K, 0, txy_pred)
sxK = R["BH_sx_p"] * math.sin(math.radians(R["phiK_off"]))
mK = LM.principal2(sxK, 0.0, R["BK_txy_p"])
V.update(BK_s1_c=f(mK[0] * MPa, 2), BK_s2_c=f(mK[1] * MPa, 2), BH_I1=f((R["BH_s1"] + R["BH_s2"]) * MPa, 2), BH_thabs=f(abs(R["BH_th"]), 1),
         BH_txy=f(R["BH_txy"] * MPa, 2), BH_R=f(R["BH_R"] * MPa, 2))
assert abs(mK[1] - R["BK_s2"]) <= U["BK_ds2"] and abs(mK[0] - R["BK_s1"]) <= U["BK_ds1"]
rows = []
for g in "HK":
    rows.append(f"| {g} | {f(R[f'B{g}_sx'] * MPa, 2)} | {f(R[f'B{g}_txy'] * MPa, 2)} | {pm(R[f'B{g}_s1'] * MPa, U[f'B{g}_s1'] * MPa, 2)} | {pm(R[f'B{g}_s2'] * MPa, U[f'B{g}_s2'] * MPa, 2)} | "
                f"{pm(R[f'B{g}_th'], U[f'B{g}_th'], 2)} | {f(R[f'B{g}_s1_p'] * MPa, 2)}, {f(R[f'B{g}_s2_p'] * MPa, 2)} | {f(R[f'B{g}_th_p'], 2)} |")
V["B_table"] = "\n".join(rows)
# slopes table (Kt corrected readings and reduced components, before turning back)
Kt, nu0 = MEAS["rosette"]["Kt"], MEAS["rosette"]["nu0"]
rows = []
for cfg, lab, sc in (("axis", "Part A", 100.0), ("lever", "Part B", 100.0), ("pressure", "Part C", 1e6)):
    for g in "HK":
        a, b, c = (OUT["slopes"][f"{cfg}|{g}{x}_ue"] for x in "abc")
        import lab08_analysis as LA  # noqa: E402
        a, b, c = LA.kt_rect(a, b, c, Kt, nu0)
        exx, eyy, gg = LA.reduce(a, b, c)
        rows.append(f"| {lab}, {g} | " + " | ".join(f(v * sc * 1e6, 2) for v in (a, b, c, exx, eyy, gg)) + " |")
V["A_table"] = "\n".join(rows)
a, b, c = (OUT["slopes"][f"axis|H{x}_ue"] for x in "abc")
a, b, c = LA.kt_rect(a, b, c, Kt, nu0)
exA, eyA, gA = LA.reduce(a, b, c)
bH = math.radians(R["beta_H"])
V.update(A1_ratio=f(gA / (exA - eyA), 4), A1_ex=f(LA.turn(exA, eyA, gA, -bH)[0] * 1e6, 4), A1_sxN=f(OUT["props"]["ro"] * 0.25 / OUT["props"]["I"] / 1e3, 3),
         A1_cos=f(math.cos(2 * bH), 5), A1_gapp=f(gA * 600 * 1e6, 0),
         nu_noKt=f(R["nu_A_noKt"], 4), nu_noKt_pct=f(100 * (R["nu_A_noKt"] / R["nu_A"] - 1), 1), E_noKt_pct=f(100 * (R["E_A_noKt"] / R["E_A"] - 1), 2))
# A2: torsion-only state at H (turned back by beta_H from Part A, an independent angle): ex - ey per 100 N, vs its gamma
ha, hb, hc = (OUT["slopes"][f"lever|H{x}_ue"] - OUT["slopes"][f"axis|H{x}_ue"] for x in "abc")
ha, hb, hc = LA.kt_rect(ha, hb, hc, Kt, nu0)
hx, hy, hg = LA.turn(*LA.reduce(ha, hb, hc), -math.radians(R["beta_H"]))
V["A2_dexy"] = f((hx - hy) * 100 * 1e6, 2)
V["A2_g"] = f(hg * 100 * 1e6, 1)
V["A2_res"] = f(abs(math.degrees(0.5 * math.atan((hx - hy) / hg))), 2)
# A4
V.update(CH_ex=f(R["CH_ex"] * 1e6, 2), CH_ey=f(R["CH_ey"] * 1e6, 2), CK_ex=f(R["CK_ex"] * 1e6, 2), CK_ey=f(R["CK_ey"] * 1e6, 2), C_nu=pm(R["C_nu"], U["C_nu"], 4),
         C_nu_ag=agree(R["C_dnu"], U["C_dnu"]), C_sth=pm(R["C_sth"] * MPa, U["C_sth"] * MPa, 3), C_sx=pm(R["C_sx"] * MPa, U["C_sx"] * MPa, 3),
         C_sth_lame=f(R["C_sth_lame"] * MPa, 3), C_sx_lame=f(R["C_sx_lame"] * MPa, 3), C_sth_thin=f(R["C_sth_thin"] * MPa, 3), C_sx_thin=f(R["C_sx_thin"] * MPa, 3),
         C_ag_lame=agree(R["C_dsth_lame"], U["C_dsth_lame"]) + ("" if abs(R["C_dsx_lame"]) <= U["C_dsx_lame"] else " (σ_x: disagree)"),
         C_ag_thin=agree(R["C_dsth_thin"], U["C_dsth_thin"]), C_thin_pct=f(100 * (R["C_sth_thin"] / R["C_sth_lame"] - 1), 1), C_ratio=f(R["C_sx"] / R["C_sth"], 3))
# A5
for g in "HK":
    V.update({f"X{g}_s1": pm(R[f"X{g}_s1"] * MPa, U[f"X{g}_s1"] * MPa, 2), f"X{g}_s2": pm(R[f"X{g}_s2"] * MPa, U[f"X{g}_s2"] * MPa, 2),
              f"X{g}_R": pm(R[f"X{g}_R"] * MPa, U[f"X{g}_R"] * MPa, 2), f"X{g}_tabs": pm(R[f"X{g}_tabs"] * MPa, U[f"X{g}_tabs"] * MPa, 2),
              f"X{g}_s1_p": f(R[f"X{g}_s1_p"] * MPa, 2), f"X{g}_s2_p": f(R[f"X{g}_s2_p"] * MPa, 2), f"X{g}_tabs_p": f(R[f"X{g}_tabs_p"] * MPa, 2)})
V.update(XH_ag=agree(R["XH_dtabs"], U["XH_dtabs"]), XH_ratio=f(R["XH_ratio"], 2), XH_pct=f(100 * (1 - 1 / R["XH_ratio"]), 0))
# M1
tp_m = OUT["props"]
V.update(M1_ratio=f((tp_m["ro"] + tp_m["ri"]) / (2 * tp_m["ri"]), 3), M1_tu=f(R["BH_txy_unturned"] * MPa, 2), M1_tu_pct=f(100 * (R["BH_txy_unturned"] / R["BH_txy"] - 1), 1),
         M1_thu=f(R["BH_th_unturned"], 2), C_ey_noKt_pct=f(100 * (R["C_ey_noKt_ratio"] - 1), 1), C_ex_noKt_pct=f(100 * (R["C_ex_noKt_ratio"] - 1), 1),
         M1_ratioK=f(math.sin(math.radians(R["phiK_off"])), 4), phiK=pm(R["phiK_off"], U["phiK_off"], 2))
# C1: delta rosette at K, Part B at 600 N (turned-back measured state)
exK, eyK, gK = R["BK_ex"], R["BK_ey"], R["BK_g"]
V.update(C1_rd=", ".join(f(LM.strain_at(exK, eyK, gK, t) * 1e6, 1) for t in LM.DELTA), C1_urect=f(1.5 * math.sqrt(6), 2), C1_udelta=f(1.5 * 2 * math.sqrt(2) / math.sqrt(3), 2))
# C2
V.update(C2_F=pm(R["C2_F"], U["C2_F"], 0), C2_aL=pm(R["C2_aL"] * 1e3, U["C2_aL"] * 1e3, 0), C2_Lb=pm(R["C2_Lb"] * 1e3, U["C2_Lb"] * 1e3, 0),
         C2_FLb=pm(R["C2_FLb"], U["C2_FLb"], 1), C2_FaL=pm(R["C2_FaL"], U["C2_FaL"], 1))
# C3: gage c error under uniaxial stress with nu = 0.33: reading/true - 1 = (1 - Kt/nu)/(1 - nu0 Kt) - 1
nu_t = R["nu_A"]
V["C3_c_pct"] = f(100 * abs((1 - Kt / nu_t) / (1 - nu0 * Kt) - 1), 1)
# X2
V["X2_R"] = f(2 * G2 * math.hypot((R["BH_ex"] - R["BH_ey"]) / 2, R["BH_g"] / 2) * MPa, 2)
# mistake 4: sigma = E*eps component by component (no Poisson coupling)
V["M7_sy"] = f(E2 * R["BH_ey"] * MPa, 1)
V["M7_pct"] = f(100 * (1 - E2 * R["CH_ey"] * 1e-6 / R["CH_sth"]), 0)

# ------------------------------------------------------------------ D1
D_ = OUT["D1"]
tall = D_["sY"] / (2 * D_["n"])
rows = []
for d in sorted(D_["table"], key=lambda d_: d_["mass"]):
    c = d["crit"]
    rows.append(f"| {d['name']} | {f(d['mass'], 3)} | {f(d['sf_tresca'], 2)} | {f(d['sf_inplane'], 2)} | {f(d['sf_vm'], 2)} | {f(d['twist'], 2)} | "
                f"{c['where']}, {c['side']} | {'yes' if d['ok'] else 'no'} |")
V["D_table"] = "\n".join(rows)
best = next(d for d in D_["table"] if d["name"] == D_["best"])
inpl = next(d for d in D_["table"] if d["name"] == D_["best_inplane"])
stro = next(d for d in D_["table"] if d["name"] == D_["best_stress_only"])
c = best["crit"]
V.update(D_tall=f(tall, 1), D_best=D_["best"], D_best_m=f(best["mass"], 3), D_crit=f"{c['where']} surface, {c['side']}", D_sx=f(c["sx"] * MPa, 1),
         D_st=f(c["st"] * MPa, 1), D_sr=f(c["sr"] * MPa, 1), D_tau=f(c["tau"] * MPa, 1), D_p=", ".join(f(x * MPa, 1) for x in c["p"]), D_tabs=f(c["tabs"] * MPa, 1),
         D_sf=f(best["sf_tresca"], 2), D_tin=f(c["tin"] * MPa, 1), D_vm=f(best["sf_vm"], 2), D_tw=f(best["twist"], 2), D_stress=D_["best_stress_only"],
         D_stress_sf=f(stro["sf_tresca"], 2), D_stress_tw=f(stro["twist"], 2), D_inplane=D_["best_inplane"], D_inplane_m=f(inpl["mass"], 3),
         D_inplane_sfin=f(inpl["sf_inplane"], 2), D_inplane_sf=f(inpl["sf_tresca"], 2))
assert D_["best_vm"] == D_["best"]

tmpl = (HERE / "lab08_instructor_key.template.md").read_text(encoding="utf-8")
missing = sorted(set(re.findall(r"«(\w+)»", tmpl)) - set(V))
if missing:
    raise SystemExit(f"missing values: {missing}")
out = re.sub(r"«(\w+)»", lambda m: V[m.group(1)], tmpl)
(HERE / "lab08_instructor_key.md").write_text(out, encoding="utf-8")
(HERE / "key_values.json").write_text(json.dumps(V, indent=1, ensure_ascii=False))
print("wrote lab08_instructor_key.md;", len(V), "values")

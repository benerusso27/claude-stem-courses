"""Generate lab07_instructor_key.md from computed results (no hand-typed numbers).

    python3 lab07_analysis.py && python3 make_key.py

Inputs: results.json (lab07_analysis.py on sample_data.csv), specimen_measurements.json, and the simulation's own
model code run in Node (dumped to sim_numbers.json). Placeholders in the template are written «name».
"""
import json
import math
import re
import subprocess
from pathlib import Path

import numpy as np

import lab07_model as LM

HERE = Path(__file__).resolve().parent
LAB = HERE.parent
R = json.loads((HERE / "results.json").read_text())
MEAS = json.loads((HERE / "specimen_measurements.json").read_text())
REF = MEAS["reference"]
G = 9.80665
A_, B1, B2, B3, C_, D_ = R["A"], R["B1"], R["B2"], R["B3"], R["C"], R["D1"]
V = {}


def f(x, nd):
    return f"{x:,.{nd}f}".replace(",", " ").replace("-", "−")


def sci(x):
    """1.7e-09 -> '1.7 × 10⁻⁹' (one or two significant figures)."""
    m, e = f"{x:.1e}".split("e")
    sup = str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹")
    return f"{m.rstrip('0').rstrip('.')} × 10{str(int(e)).translate(sup)}"


def sig(x, n=2):
    return f"{float(f'{x:.{n}g}'):g}".replace("-", "−")


def pm(x, U, nd):
    return f"{f(x, nd)} ± {f(U, nd)}"


def agree(d, lim):
    return "agree" if abs(d) <= lim else "disagree"


# ------------------------------------------------------------------ simulation numbers (exact page code)
JS = r"""
const {loadModel}=require('%s'); const M=loadModel('%s'); const o={};
const PP=(k,ov={})=>Object.assign({}, M.PRESETS[k], ov);
{ const p=PP('partAboth'), c=M.closedForm(p), xs=[0.2,0.4,0.6];
  o.Aboth={d:xs.map(x=>-c.y(x)), p600:xs.map(x=>-c.comps[0].f(x)), p200:xs.map(x=>-c.comps[1].f(x)), lab:c.comps.map(q=>q.label)}; }
{ const p=PP('partB2'); o.B2={k:M.closedForm(p).R.RB, rigid:M.closedForm(PP('partB2',{rigid:true})).R.RB, P:p.P1}; }
{ const p=PP('partC'), sp=M.stripProps(p), w=M.elasticaShoot(sp.alpha, sp.betaFull, p.Nrk), c=M.elasticaClosed(sp.alpha), a5=M.alpha5();
  o.C={L:p.Ls, dv_w:w.dv*p.Ls, dh_w:(1-w.xt)*p.Ls, dv:c.dv*p.Ls, dh:(1-c.xt)*p.Ls, a5, m5:a5*sp.EI/(p.Ls*p.Ls)/9.80665}; }
{ const sh=(p,span)=>{ const m=M.MATERIALS[p.mat], s=M.section(p), G=m.E/(2*(1+m.nu)); return {k:12*s.fs*m.E*s.I/(G*s.A), span}; };
  o.shear={bar:sh(PP('partA'),0.8), D1:sh(PP('design'),3.05)}; }
{ const c5=M.beamConvergence(PP('F5')), c6=M.beamConvergence(PP('F6'));
  o.conv={F5:Math.max(...c5.rows.map(r=>Math.max(r.err,r.errM))), F6y:c6.slope, F6M:c6.slopeM}; }
console.log(JSON.stringify(o));
""" % ((LAB.parent / "shared" / "test_harness.js").as_posix(), (LAB / "lab07_simulation.html").as_posix())
SIM = json.loads(subprocess.run(["node", "-e", JS], capture_output=True, text=True, check=True).stdout)
(HERE / "sim_numbers.json").write_text(json.dumps(SIM, indent=1))

# ------------------------------------------------------------------ pre-lab (nominal dimensions, Table 1)
Eb = REF["E_st_GPa"] * 1e9
Ib = 25.4e-3 * 6.35e-3 ** 3 / 12
EIb = Eb * Ib
Is_n = 12.7e-3 * 0.79e-3 ** 3 / 12
EIs_n = 203e9 * Is_n
PA = 3.0 * G
dA = [-LM.ss_point(PA, 0.6, 0.8, EIb, np.array([x]))[0][0] * 1e3 for x in (0.2, 0.4, 0.6)]
MA = PA * 0.6 * 0.2 / 0.8
sA = MA * 6.35e-3 / 2 / Ib / 1e6
PC = 0.62 * G
alpha_n = PC * 0.25 ** 2 / EIs_n
V.update(P1_I=f(Ib * 1e12, 1), P1_EI=f(EIb, 2), P1_Is=f(Is_n * 1e12, 4), P1_EIs=f(EIs_n, 4), P1_PA=f(PA, 2), P1_dA=", ".join(f(d, 3) for d in dA),
         P1_MA=f(MA, 3), P1_sA=f(sA, 1), P1_sAr=f(sA / REF["sY_st_MPa"], 3), P1_dB1=f(G * 0.7 ** 3 / (3 * EIb) * 1e3, 2),
         P1_PB2=f(4 * G, 2), P1_RB=f(5 * 4 * G / 16, 2), P1_PC=f(PC, 3), P1_alpha=f(alpha_n, 2), P1_dC=f(alpha_n / 3 * 250, 0))
y1 = -LM.ss_point(2 * G, 0.6, 0.8, EIb, np.array([0.4]))[0][0] * 1e3
y2 = -LM.ss_point(1 * G, 0.2, 0.8, EIb, np.array([0.4]))[0][0] * 1e3
V.update(P2_y1=f(y1, 3), P2_y2=f(y2, 3), P2_y=f(y1 + y2, 3), P2_c=f(0.2 * 0.2 * 0.56 / (6 * 0.8 * EIb) * 1e6, 2))
V.update(P3_r=f((5 / 16 + 0.06) / 1.12, 4), P3_dR=f(-3 * EIb * 0.5e-3 / 0.7 ** 3, 3))
c1, c2 = B1["c_mid"], B1["c_tip"]
V.update(P4_frac=f(100 * (16 * c1 - 5 * c2) / (16 * c1), 1), P4_uk=f(100 * 2 * B1["uk"] / B1["k"], 0), P4_uEI=f(100 * 2 * B1["uEI"] / B1["EI"], 1))
S = SIM
V.update(sim_A_both=", ".join(f(d * 1e3, 3) for d in S["Aboth"]["d"]), sim_A_600=", ".join(f(d * 1e3, 3) for d in S["Aboth"]["p600"]),
         sim_A_200=", ".join(f(d * 1e3, 3) for d in S["Aboth"]["p200"]), sim_B2_k=f(S["B2"]["k"], 2), sim_B2_rigid=f(S["B2"]["rigid"], 2),
         sim_B2_P=f(S["B2"]["P"], 2), sim_C_dv_w=f(S["C"]["dv_w"] * 1e3, 1), sim_C_dh_w=f(S["C"]["dh_w"] * 1e3, 1), sim_C_dv=f(S["C"]["dv"] * 1e3, 1),
         sim_C_dh=f(S["C"]["dh"] * 1e3, 1), sim_C_a5=f(S["C"]["a5"], 3), sim_C_m5=f(S["C"]["m5"], 3))
cb = 6.35e-3 / 2
V.update(P6_sA=f(3 * G * 0.2 * cb / Ib / 1e6, 1), P6_sB1=f(G * 0.7 * cb / Ib / 1e6, 1), P6_sB2=f(3 * 4 * G * 0.7 / 16 * cb / Ib / 1e6, 1))
V.update(C_Mroot=f(C_["M_root"], 3), C_sroot=f(C_["sig_root"], 0), C_sroot_r=f(C_["sig_root"] / REF["sY_spring_MPa_min"], 2))

# ------------------------------------------------------------------ results at a glance and analysis
bar = R["bar"]
V.update(bar_b=pm(bar["b"], 2 * bar["ub"], 3), bar_h=pm(bar["h"], 2 * bar["uh"], 4), A_I=f(bar["I"], 1),
         A_E=pm(A_["E"], 2 * A_["uE"], 2), ref_E=pm(REF["E_st_GPa"], 2 * REF["u_E_st_GPa"], 1), A_E_ag=agree(A_["E"] - REF["E_st_GPa"], A_["E_agree"]),
         A_dE=f(abs(A_["E"] - REF["E_st_GPa"]), 2), A_lim=f(A_["E_agree"], 2), A_spread=f(A_["E_spread"], 2), A_EI=pm(A_["EI"], 2 * A_["uEI"], 2))
rows = []
for r in A_["rows"]:
    rows.append(f"| {f(r['a'] * 1e3, 0)} mm | {f(r['x'] * 1e3, 0)} mm | {pm(r['c'] * 1e6, 2 * r['uc'] * 1e6, 3)} | {f(r['f'] * 1e3, 4)} | {pm(r['E'], 2 * r['uE'], 1)} |")
V["A1_table"] = "\n".join(rows)
# uncertainty budget per coefficient (same position model as the analysis: span, indicator, hanger each +-0.5 mm)
import lab07_analysis as LA  # noqa: E402
u_pos = MEAS["rule_accuracy_mm"] / math.sqrt(3) * 1e-3
ufs, ucs = [], []
for r in A_["rows"]:
    x, a0, L0 = r["x"], r["a"], MEAS["A"]["span_mm"] * 1e-3
    f0 = LA.ss_compliance(x, a0, L0, 1.0)
    ds = [(LA.ss_compliance(x, a0, L0 + 1e-4, 1.0) - f0) / 1e-4, (LA.ss_compliance(x + 1e-4, a0, L0, 1.0) - f0) / 1e-4,
          (LA.ss_compliance(x, a0 + 1e-4, L0, 1.0) - f0) / 1e-4]
    ufs.append(100 * math.sqrt(sum((d_ * u_pos) ** 2 for d_ in ds)) / f0)
    ucs.append(100 * r["uc"] / r["c"])
V.update(A1_uf=f"{f(min(ufs), 2)}–{f(max(ufs), 2)}", A1_uc=f"{f(min(ucs), 2)}–{f(max(ucs), 2)}", A1_uh=f(300 * bar["uh"] / bar["h"], 2),
         A1_ub=f(100 * bar["ub"] / bar["b"], 2), A1_hcal=f(300 * MEAS["caliper_accuracy_mm"] / math.sqrt(3) / bar["h"], 2))
meas = [d * 1e3 for d in A_["meas_both"]]
pred = [d * 1e3 for d in A_["pred_both"]]
diffs = [abs(m_ - p_) * 1e3 for m_, p_ in zip(meas, pred)]
lims = [l_ * 1e6 for l_ in A_["both_lim"]]
nag = sum(d <= l_ for d, l_ in zip(diffs, lims))
V.update(A2_meas=", ".join(f(x, 3) for x in meas), A2_pred=", ".join(f(x, 3) for x in pred), A2_diff=", ".join(f(x, 1) for x in diffs),
         A2_lims=", ".join(f(x, 1) for x in lims), A2_ag="all three agree" if nag == 3 else f"{nag} of 3 agree",
         A2_theory=", ".join(f(d * 1e3, 3) for d in A_["theory_both"]),
         A2_c13=pm(A_["c13"] * 1e6, 2 * A_["u13"] * 1e6, 3), A2_c31=pm(A_["c31"] * 1e6, 2 * A_["u31"] * 1e6, 3),
         A2_rec_d=f(A_["recip_d"] * 1e6, 3), A2_rec_lim=f(A_["recip_lim"] * 1e6, 3), A2_rec_ag=agree(A_["recip_d"], A_["recip_lim"]),
         A2_c12=f(A_["c12"] * 1e6, 3), A2_c32=f(A_["c32"] * 1e6, 3))
EI_rigid_E = B1["EI_rigid"] / (bar["I"] * 1e-12) / 1e9
V.update(B1_cmid=pm(B1["c_mid"] * 1e6, 2 * B1["uc_mid"] * 1e6, 2), B1_ctip=pm(B1["c_tip"] * 1e6, 2 * B1["uc_tip"] * 1e6, 2),
         B1_EI=pm(B1["EI"], 2 * B1["uEI"], 2), B1_k=f"{round(B1['k'], -1):,.0f} ± {round(2 * B1['uk'], -1):,.0f}".replace(",", " "),
         B1_dEI=f(abs(B1["EI"] - A_["EI"]), 2), B1_EI_lim=f(B1["EI_agree"], 2), B1_EI_ag=agree(B1["EI"] - A_["EI"], B1["EI_agree"]),
         B1_EIrigid=f(B1["EI_rigid"], 2), B1_EIrigid_err=f(abs(B1["EI_rigid_err"]), 1), B1_share=f(B1["clamp_share"], 1), B1_Eunsusp=f(EI_rigid_E, 0))
lam = B1["EI"] / (B1["k"] * MEAS["B"]["L_mm"] * 1e-3)
V.update(B2_r=pm(B2["r"], 2 * B2["ur"], 4), B2_rk=pm(B2["r_k"], 2 * B2["u_rk"], 4), B2_drig=f(B2["d_rigid_r"], 4), B2_xU=f(B2["d_rigid_r"] / (2 * B2["ur"]), 0),
         B2_ag_rigid=agree(B2["d_rigid_r"], 2 * B2["ur"]), B2_ag_k=agree(B2["r"] - B2["r_k"], B2["agree_k"]), B2_lam=f(lam, 4),
         B2_dk=f(abs(B2["r"] - B2["r_k"]), 4), B2_limk=f(B2["agree_k"], 4), B2_dslope=pm(B2["dslope"] * 1e6, 2 * B2["udslope"] * 1e6, 2),
         B2_drigid=f(B2["d_rigid"] * 1e6, 2), B2_dk_pred=pm(B2["d_k"] * 1e6, 2 * B2["u_dk"] * 1e6, 2), B2_ddd=f(abs(B2["dslope"] - B2["d_k"]) * 1e6, 2),
         B2_dlim=f(B2["d_agree"] * 1e6, 2), B2_kR=f(round(B2["k_from_R"], -1), 0), B2_rigid_pct=f(100 * (1 - 0.3125 / B2["r"]), 1))
R3kg = B2["r"] * 3 * G
V.update(B3_dR=pm(B3["dR"], 2 * B3["u_dR"], 3), B3_rigid=f(B3["dR_rigid"], 3), B3_k=pm(B3["dR_k"], 2 * B3["u_dRk"], 3),
         B3_ag_rigid=agree(B3["dR"] - B3["dR_rigid"], 2 * B3["u_dR"]), B3_ag_k=agree(B3["dR"] - B3["dR_k"], B3["agree"]),
         B3_dd=f(abs(B3["dR"] - B3["dR_k"]), 3), B3_lim=f(B3["agree"], 3), B3_ind=f(B3["dd"], 3), B3_pct=f(100 * abs(B3["dR"]) / R3kg, 1),
         B3_rigid_pct=f(100 * (B3["dR_rigid"] / B3["dR"] - 1), 0))
# Part C
pts = C_["pts"]
Lc = C_["L"]
sag0 = C_["sag0"]
rows = []
for p_ in pts:
    rows.append(f"| {f(p_['P'] / G, 2)} | {f(p_['alpha'], 3)} | {f(p_['dv'] * 1e3, 1)} | {f(p_['dv_lin'] * 1e3, 1)} | {f(p_['dv_tip'] * 1e3, 1)} | "
                f"{f(p_['dv_w'] * 1e3, 1)} | {f(p_['xt'] * 1e3, 1)} | {f(p_['xt_w'] * 1e3, 1)} | {f(p_['lin_err'], 1) if p_['P'] > 0 else '—'} |")
V["C_table"] = "\n".join(rows)
last = pts[-1]
i12 = next(i for i, p_ in enumerate(pts) if abs(p_["P"] / G - 0.12) < 1e-6)
Ug = 2 * C_["u_grid"] * 1e3
thmax = LM.elastica_bvp(C_["alpha_max"], C_["beta"])[0]
V.update(C_EIfit=pm(C_["EI_fit"], 2 * C_["uEI_fit"], 4), C_EIlin=pm(C_["EI_lin"], 2 * C_["uEI_lin"], 4), C_Efit=pm(C_["E_fit"], 2 * C_["uE_fit"], 1),
         C_dv_last=pm(last["dv"] * 1e3, Ug, 1), C_lin_last=f(last["dv_lin"] * 1e3, 1), C_tip_last=f(last["dv_tip"] * 1e3, 1), C_w_last=f(last["dv_w"] * 1e3, 1),
         C_a5m=f(C_["a5_meas"], 2), C_a5=f(C_["a5"], 3), C_sag0=f(sag0 * 1e3, 2), C_Ugrid=f(Ug, 2), C_slope=f(Lc ** 3 / (3 * C_["EI_lin"]) * 1e3, 2),
         C_L=f(Lc * 1e3, 2), C_lin_last_err=f(last["lin_err"], 0), C_tip_ok=f(max(abs(p_["tip_only_err"]) for p_ in pts if p_["alpha"] <= 1.0), 1),
         C_tip_last_d=f(last["tip_only_err"], 1), C_chi2=f(C_["chi2"], 1), C_dof=str(C_["dof"]), C_dh_last=f((Lc - last["xt"]) * 1e3, 1),
         C_factor=f(last["dv_lin"] / last["dv"], 2), C_amax=f(C_["alpha_max"], 2), C_th0=f(math.degrees(thmax), 1) + "°",
         C_slope2=f(math.tan(thmax) ** 2, 1), C_w12=f((pts[i12]["dv_w"] - (pts[i12]["dv_tip"] - sag0)) * 1e3, 2),
         C_w62=f((last["dv_w"] - (last["dv_tip"] - sag0)) * 1e3, 2), C_linbias=f(C_["lin_bias"], 2), C_a4=f(pts[3]["alpha"], 2),
         C_t_pct=f(300 * C_["ut"] / C_["t"], 2))
bs, ts = C_["b"] * 1e-3, C_["t"] * 1e-3
V["C_searle"] = f(bs ** 2 * C_["M_root"] / (C_["EI_fit"] * ts), 1)
# M1(d) shear
for key, tag in (("bar", "bar"), ("D1", "D1")):
    sk = SIM["shear"][key]
    Lsh = math.sqrt(sk["k"] / 0.05)
    V[f"M1_Lsh_{tag}"] = f(Lsh * 1e3, 0) if key == "bar" else f(Lsh, 2)
    V[f"M1_sh_{tag}"] = sig(100 * sk["k"] / sk["span"] ** 2, 2)
V["M1_Lsh_bar_r"] = f(math.sqrt(SIM["shear"]["bar"]["k"] / 0.05) / 6.35e-3, 1)
# C1
V.update(C1_F5_err=sci(SIM["conv"]["F5"]), C1_F6_sy=f(SIM["conv"]["F6y"], 2), C1_F6_sM=f(SIM["conv"]["F6M"], 2))
# C3
LB = MEAS["B"]["L_mm"] * 1e-3
RB4 = B2["r"] * B2["P_max"]
flex = LB ** 3 / (3 * B1["EI"]) + LB ** 2 / B1["k"]
D5 = 0.05 * RB4 * flex
V.update(C3_R=f(RB4, 2), C3_dR=f(0.05 * RB4, 3), C3_flex=f(flex * 1e3, 4), C3_D=f(D5 * 1e3, 3), C3_ratio=f(round(D5 / 2e-6, -1), 0))
# X1
th_, dv_, xt_ = LM.elastica_closed(0.01)
V.update(X1_c3=f((0.01 / 3 - dv_) / 0.01 ** 3, 5) + " (4/105 = " + f(4 / 105, 5) + ")", X1_t3=f((0.005 - th_) / 0.01 ** 3, 5) + " (11/240 = " + f(11 / 240, 5) + ")",
         X1_h2=f((1 - xt_) / 0.01 ** 2, 5) + " (1/15 = " + f(1 / 15, 5) + ")")
# X2, X3
a_, x_ = 0.35, LB
V["X2_c"] = f((a_ ** 2 * (3 * x_ - a_) / (6 * B1["EI"]) + a_ * x_ / B1["k"]) * 1e6, 2)
V.update(X3_tip=f(flex * G * 1e3, 3), X3_meas=f(B1["c_tip"] * G * 1e3, 3),
         X3_mid=f((0.35 ** 2 * (3 * LB - 0.35) / (6 * B1["EI"]) + LB * 0.35 / B1["k"]) * G * 1e3, 3), X3_mid_meas=f(B1["c_mid"] * G * 1e3, 3))

# ------------------------------------------------------------------ D1
sa = D_["sa"]
rows = []
for t in D_["table"]:
    if t["feas"]:
        evs = [e for e in t["evals"] if e["Ls"] in t["feas"]]
        feas = f"{f(t['feas'][0], 2)}–{f(t['feas'][-1], 2)}" if len(t["feas"]) > 1 else f(t["feas"][0], 2)
    else:
        evs = t["evals"]
        feas = "none"
    e = min(evs, key=lambda e_: max(e_["r_s"], e_["r_y"], e_["r_t"]))
    rows.append(f"| {t['name']} | {f(t['I'] / 1e6, 3)} | {f(t['mass'], 2)} | {feas}{'' if t['feas'] else ' (best ' + f(e['Ls'], 2) + ')'} | "
                f"{f(e['r_s'], 2)} | {f(e['r_y'], 2)} | {f(e['r_t'], 2)} |")
V["D_table"] = "\n".join(rows)
best = next(t for t in D_["table"] if t["name"] == D_["best"])
noov = next(t for t in D_["table"] if t["name"] == D_["noover"])
eb = min((e for e in best["evals"] if e["Ls"] in best["feas"]), key=lambda e_: max(e_["r_s"], e_["r_y"], e_["r_t"]))
Ls, Lt, w, P = eb["Ls"], D_["Lt"], D_["w"], D_["P"]
a = Lt - Ls
EId = D_["E"] * 1e9 * best["I"] * 1e-12
MB = -(w * a ** 2 / 2 + P * a)
bm = dict(family="ss", L=Ls, a_over=a, EI=EId, P=[(P, Lt)], w=w)
xs = np.linspace(0, Ls, 20001)
ysp = LM.closed_form(bm, xs)["y"]
im = int(np.argmax(np.abs(ysp)))
xm = xs[im]
y6 = LM.ss_udl(w, Ls, EId, np.array([xm]))[0][0]
y7 = LM.ss_end_moment(MB, Ls, EId, np.array([xm]))[0][0]
thB = LM.ss_udl(w, Ls, EId, np.array([Ls]))[1][0] + LM.ss_end_moment(MB, Ls, EId, np.array([Ls]))[1][0]
tP = LM.cant_point(P, a, EId, np.array([a]))[0][0]
tw = LM.cant_udl(w, a, EId, np.array([a]))[0][0]
RA, RB = eb["RA"], eb["RB"]
V.update(D_sa=f(sa, 1), D_best=D_["best"], D_best_Ls=f(Ls, 2), D_best_hi=f(best["feas"][-1], 2), D_best_a=f(a, 2), D_best_m=f(best["mass"], 2),
         D_RA=f(RA, 0), D_RB=f(RB, 0), D_sum=f(RA + RB, 0), D_MB=f(MB, 1), D_Mpos=f(RA ** 2 / (2 * w), 0), D_xpos=f(RA / w, 3), D_s=f(eb["s"], 1),
         D_rs=f(eb["r_s"], 2), D_y6=f(y6 * 1e3, 2), D_y7=f(y7 * 1e3, 2), D_ys=f((y6 + y7) * 1e3, 2), D_ys_lim=f(Ls / 360 * 1e3, 2), D_thB=f(thB * 1e3, 3),
         D_tip_rot=f(thB * a * 1e3, 2), D_tip_P=f(tP * 1e3, 2), D_tip_w=f(tw * 1e3, 2), D_yt=f((thB * a + tP + tw) * 1e3, 2), D_yt_lim=f(2 * a / 360 * 1e3, 2),
         D_noover=D_["noover"], D_noover_m=f(noov["mass"], 2), D_noover_ratio=f(noov["mass"] / best["mass"], 1))
# consistency with the analysis grid
assert abs(abs(y6 + y7) * 1e3 - eb["ys"]) < 5e-3 * eb["ys"], (y6 + y7, eb["ys"])
assert abs(abs(thB * a + tP + tw) * 1e3 - eb["yt"]) < 1e-6 * max(eb["yt"], 1), (thB * a + tP + tw, eb["yt"])
V["X1_a1"] = f(LM.elastica_p5(0.01), 2)

tmpl = (HERE / "lab07_instructor_key.template.md").read_text(encoding="utf-8")
missing = sorted(set(re.findall(r"«(\w+)»", tmpl)) - set(V))
if missing:
    raise SystemExit(f"missing values: {missing}")
out = re.sub(r"«(\w+)»", lambda m: V[m.group(1)], tmpl)
(HERE / "lab07_instructor_key.md").write_text(out, encoding="utf-8")
(HERE / "key_values.json").write_text(json.dumps(V, indent=1, ensure_ascii=False))
print("wrote lab07_instructor_key.md;", len(V), "values")

"""Generate lab05_instructor_key.md from computed results (no hand-typed numbers).

    python3 lab05_analysis.py && python3 make_key.py

Inputs: results.json (lab05_analysis.py on sample_data.csv), specimen_measurements.json, and the simulation's own
model code run in Node (dumped to sim_numbers.json). Placeholders in the template are written «name».
"""
import json
import math
import re
import subprocess
from pathlib import Path

import lab05_model as LM

HERE = Path(__file__).resolve().parent
LAB = HERE.parent
R = json.loads((HERE / "results.json").read_text())
MEAS = json.loads((HERE / "specimen_measurements.json").read_text())
REF = MEAS["reference"]
A_, B_, C_, D_ = R["A"], R["B"], R["C"], R["D"]
V = {}


def f(x, nd):
    return f"{x:,.{nd}f}".replace(",", " ").replace("-", "−")


def pm(x, U, nd):
    return f"{f(x, nd)} ± {f(U, nd)}"


def agree(d, lim):
    return "agree" if abs(d) <= lim else "disagree"


# ------------------------------------------------------------------ simulation numbers (exact page code)
JS = r"""
const {loadModel}=require('%s'); const M=loadModel('%s'); const P=M.PRESETS; const o={};
o.Rup=M.rectSeries(P.rectUp.b,P.rectUp.h,0.33,1); o.Rflat=M.rectSeries(P.rectFlat.b,P.rectFlat.h,0.33,1); o.Rflat0=M.rectSeries(P.rectFlat.b,P.rectFlat.h,0.33,0);
o.fd=[8,16,32,64].map((N)=>({N, v:M.rectFD(P.rectFlat.b,P.rectFlat.h,0.33,N).edge}));
{ const out=[]; for (const L of [0.3,0.9,1.2]) { const p=Object.assign({},P.ibeamSpan,{L}); const t=M.timoClosed(p); out.push({L, frac:t.frac, ratio:t.total/t.bend}); } o.span=out; o.L5=M.timoClosed(P.ibeamSpan).L5; o.fsI=M.timoClosed(P.ibeamSpan).sec.fs; }
{ const p=Object.assign({},P.layered); const c=M.newmarkClosed(p), d=M.boltsDiscrete(p), b=M.beerBoltForces(p);
  o.lay={dsm:c.delta, ssm:c.slip0, d:d.delta, s:d.slip0, Fd:Math.max(...d.forces.map(x=>Math.abs(x.F))), Fb:Math.max(...b.map(x=>x.F)), eta:(p.P*p.L**3/(48*d.delta)-c.g.EI0)/(c.g.EIfull-c.g.EI0), alpha:c.alpha,
         forces:d.forces.map(x=>x.F), loose:M.newmarkClosed(Object.assign({},p,{conn:'loose'})).delta, glue:M.newmarkClosed(Object.assign({},p,{conn:'glue'})).delta,
         sloose:M.newmarkClosed(Object.assign({},p,{conn:'loose'})).slip0, full:c.deltaFull}; }
{ const p=Object.assign({},P.layered,{s1:0.3,s2:0.3}); const c=M.newmarkClosed(p), d=M.boltsDiscrete(p), b=M.beerBoltForces(p); o.few={sm:c.delta, d:d.delta, n:d.n, alpha:c.alpha, ssm:c.slip0, sd:d.slip0, Fd:Math.max(...d.forces.map(x=>Math.abs(x.F))), Fb:Math.max(...b.map(x=>x.F))}; }
{ const p=Object.assign({},P.layered,{conn:'glue',Gg:50e6,tg:1e-3}); const c=M.newmarkClosed(p); o.soft={eta:c.eta, d:c.delta, full:c.deltaFull};
  const q=Object.assign({},P.layered,{conn:'glue',tg:0.15e-3}); let lo=1e3, hi=1e10; for (let k=0;k<200;k++){ const m=Math.sqrt(lo*hi); if (M.newmarkClosed(Object.assign({},q,{Gg:m})).eta<0.95) lo=m; else hi=m; } o.G95=Math.sqrt(lo*hi);
  o.etaLab=M.newmarkClosed(Object.assign({},q,{Gg:1.2e9})).eta; }
{ const p=Object.assign({},P.cantilever,{L:1.0}); const t=M.timoClosed(p); o.lock=[4,16,64].map((N)=>({N, full:M.timoFE(p,N,'full').delta/t.total, red:M.timoFE(p,N,'reduced').delta/t.total})); }
{ const p=Object.assign({},P.ibeamSpan,{L:0.3}); const t=M.timoClosed(p); o.short={ratio:t.total/t.bend, frac:t.frac}; }
console.log(JSON.stringify(o));
""" % ((LAB.parent / "shared" / "test_harness.js").as_posix(), (LAB / "lab05_simulation.html").as_posix())
SIM = json.loads(subprocess.run(["node", "-e", JS], capture_output=True, text=True, check=True).stdout)
(HERE / "sim_numbers.json").write_text(json.dumps(SIM, indent=1))

# ------------------------------------------------------------------ pre-lab (nominal dimensions, Table 1)
E, G, nu = REF["E_al_GPa"] * 1e3, REF["G_al_GPa"] * 1e3, REF["nu_al"]   # MPa
b, h = 25.4, 50.8
A = b * h
tau = 1.5 * 7500 / A
V.update(P1_A=f(A, 1), P1_tau=f(tau, 3), P1_g=f(tau / G * 1e6, 0), P1_M=f(15000 * 400 / 4 / 1e3, 0), P1_S=f(b * h * h / 6, 0),
         P1_sig=f(15000 * 400 / 4 / (b * h * h / 6), 1))
Bn, Hn, tfn, twn = 76.2, 101.6, 6.35, 4.76
lay = LM.ibeam(Bn, Hn, tfn, twn)
pr = LM.props(lay)
Aw = (Hn - 2 * tfn) * twn
tw_ = 10000 / Aw
V.update(P1_Aw=f(Aw, 1), P1_tweb=f(tw_, 2), P1_gweb=f(tw_ / G * 1e6, 0), P1_I=f(pr["I"] / 1e6, 4), P1_AI=f(pr["A"], 1), P1_fsA=f(pr["A"] / Aw, 3))
for L in (300, 1200):
    db = 10000 * L ** 3 / (48 * E * pr["I"])
    ds = (pr["A"] / Aw) * 10000 * L / (4 * G * pr["A"])
    V.update({f"P1c_b{L}": f(db, 4), f"P1c_s{L}": f(ds, 4), f"P1c_f{L}": f(100 * ds / (db + ds), 0)})
bc, tc, Lc = 50.8, 12.7, 600.0
EI0 = E * bc * 2 * tc ** 3 / 12                                        # N mm^2
d_l = 2000 * Lc ** 3 / (48 * EI0)
V.update(P1d_EI0=f(EI0 / 1e9, 1), P1d_loose=f(d_l, 2), P1d_bond=f(d_l / 4, 3), P1d_slip=f(tc * 2000 * Lc ** 2 / (16 * EI0), 3))
# P2
hw = Hn - 2 * tfn
I2 = (Bn * Hn ** 3 - (Bn - twn) * hw ** 3) / 12
Qf = Bn * tfn * (Hn - tfn) / 2
QNA = Qf + twn * hw ** 2 / 8
V.update(P2_I=f(I2 / 1e6, 4), P2_QNA=f(QNA, 0), P2_tNA=f(10000 * QNA / (I2 * twn), 2), P2_Qf=f(Qf, 0), P2_tj=f(10000 * Qf / (I2 * twn), 2),
         P2_tf=f(10000 * Qf / (I2 * Bn), 3), P2_Aw=f(10000 / Aw, 2), P2_ratio=f(Bn / twn, 2))
# P3
q = 3 * 1250 / (4 * tc)
V.update(P3_q=f(q, 1), P3_F=f(q * 100 / 1e3, 2), P3_tb=f(q * 100 / (math.pi * 9), 0))
# P5
sp = {round(r_["L"], 1): r_ for r_ in SIM["span"]}
V.update(sim_Rup=f(SIM["Rup"], 4), sim_Rflat=f(SIM["Rflat"], 4), sim_Rflat0=f(SIM["Rflat0"], 4), sim_f300=f(100 * sp[0.3]["frac"], 1), sim_f1200=f(100 * sp[1.2]["frac"], 1),
         sim_L5=f(SIM["L5"] * 1e3, 0), sim_fsI=f(SIM["fsI"], 4), sim_dlay=f(SIM["lay"]["d"] * 1e3, 3), sim_slay=f(SIM["lay"]["s"] * 1e3, 4),
         sim_dloose=f(SIM["lay"]["loose"] * 1e3, 3), sim_dglue=f(SIM["lay"]["glue"] * 1e3, 3), sim_sloose=f(SIM["lay"]["sloose"] * 1e3, 3))

# ------------------------------------------------------------------ analysis
V.update(bA=pm(A_["b"], 2 * A_["ub"], 3), hA=pm(A_["h"], 2 * A_["uh"], 3))
for cfg in ("upright", "flat"):
    a = A_[cfg]
    k = cfg[:2]
    V.update({f"A1_R_{k}": pm(a["ratio"], 2 * a["u_ratio"], 3), f"A1_P_{k}": pm(a["pred"], 2 * a["u_pred"], 4), f"A1_d_{k}": f(abs(a["ratio"] - a["pred"]), 4),
              f"A1_lim_{k}": f(a["agree_lim"], 4), f"A1_ag_{k}": agree(a["ratio"] - a["pred"], a["agree_lim"]), f"A1_bh_{k}": f(a["bh"], 4),
              f"A1_tw_{k}": f(100 * a["twist_frac"], 1), f"A1_tm_{k}": f(a["tau_max"], 2), f"A1_te_{k}": f(a["tau_elem_max"], 2), f"A1_g_{k}": f(a["gamma_max_ue"], 0),
              f"A1_V_{k}": f(a["V_max"] / 1e3, 3), f"A1_under_{k}": f(100 * (1 - 1 / a["ratio"]), 1), f"A1_err_{k}": f(100 * a["err_elem"], 1)})
V["A1_bias"] = f(100 * ((1 + 0.004) * REF["G_al_GPa"] / 25.90 - 1), 1)
V.update(B_H=pm(B_["H"], 2 * B_["uH"], 3), B_B=pm(B_["B"], 2 * B_["uB"], 3), B_tf=pm(B_["tf"], 2 * B_["utf"], 3), B_tw=pm(B_["tw"], 2 * B_["utw"], 4),
         B_I=f(B_["I"] / 1e6, 4), B_uI=f(100 * B_["uI"], 2), B_A=f(B_["A"], 1), B_Aw=f(B_["A_web"], 1), B_fs=f(B_["fs"], 4), B_fsA=f(B_["fs_approx"], 4),
         B_Awinv=f(B_["tau_Aweb_per_N"] * 1e3, 4))
rows = []
for j, w in enumerate(B_["web"]):
    rows.append(f"| {f(w['y'], 2)} | {f(w['Q'], 0)} | {pm(w['slope'] * 1e3, 2 * w['u_slope'] * 1e3, 4)} | {pm(w['pred'] * 1e3, 2 * w['u_pred'] * 1e3, 4)} | "
                f"{f(100 * (w['ratio'] - 1), 2)} | {agree(w['slope'] - w['pred'], w['agree_lim'])} | {f(100 * w['side_diff'], 1)} |")
V["A2_table"] = "\n".join(rows)
w0 = B_["web"][0]
V.update(A2_NA_Aw=f(100 * (w0["pred"] / B_["tau_Aweb_per_N"] - 1), 2), A2_bias=f(100 * (w0["ratio"] - 1), 1))
Qf_m = B_["B"] * B_["tf"] * (B_["H"] - B_["tf"]) / 2
V.update(A2_qj=f(10000 * Qf_m / B_["I"], 1), A2_tfl=f(10000 * Qf_m / (B_["I"] * B_["B"]), 3))
# share of V carried by the web: integral of tau t over the web / V (elementary distribution)
lay_m = LM.ibeam(B_["B"], B_["H"], B_["tf"], B_["tw"])
prm = LM.props(lay_m)
from scipy import integrate  # noqa: E402
web_share = integrate.quad(lambda y: LM.Q_at(lay_m, y, prm["ybar"]) / prm["I"], B_["tf"], B_["H"] - B_["tf"])[0]
V["A2_web_share"] = f(100 * web_share, 1)
dd = B_["defl"]
V.update(A3_E=pm(dd["E"], 2 * dd["uE"], 2), A3_G=pm(dd["G"], 2 * dd["uG"], 2), A3_Ed=f(abs(dd["E"] - REF["E_al_GPa"]), 2), A3_Elim=f(dd["E_lim"], 2),
         A3_Eag=agree(dd["E"] - REF["E_al_GPa"], dd["E_lim"]), A3_Gd=f(abs(dd["G"] - REF["G_al_GPa"]), 2), A3_Glim=f(dd["G_lim"], 2),
         A3_Gag=agree(dd["G"] - REF["G_al_GPa"], dd["G_lim"]), A3_a1=f(dd["a1"] * 1e12, 4), A3_a0=f(dd["a0"] * 1e9, 3),
         A3_ua1=f(100 * dd["ua1"] / dd["a1"], 2), A3_ua0=f(100 * dd["ua0"] / dd["a0"], 2), A3_Gapprox=f(dd["G"] * B_["fs_approx"] / B_["fs"], 2),
         A3_Gapprox_pct=f(100 * (B_["fs_approx"] / B_["fs"] - 1), 1))
rows = []
for r_ in dd["rows"]:
    rows.append(f"| {f(r_['L'], 0)} | {f(r_['L'] / B_['H'], 2)} | {f(r_['C'] * 1e3, 5)} | {f(r_['C_pred'] * 1e3, 5)} | {f(100 * r_['frac_meas'], 1)} | {f(100 * r_['frac_pred'], 1)} |")
V["A4_table"] = "\n".join(rows)
r300 = dd["rows"][0]
V.update(A4_L5f=f(dd["L5_fit"], 0), A4_L5p=f(dd["L5_pred"], 0), A4_hf=f(dd["h_ratio_fit"], 1), A4_hp=f(dd["h_ratio_pred"], 1),
         A4_EB300=f(100 * r300["frac_meas"], 0), A4_EBx=f(1 / (1 - r300["frac_meas"]), 2))
# rectangle of the same depth for comparison (f_s = 1.2, A = b H): L5/H = sqrt(19 * 1.2 * 48 E I/(4 G A))/H
L5rect = math.sqrt(19 * 1.2 * 48 * REF["E_al_GPa"] * (B_["H"] ** 2 / 12) / (4 * REF["G_al_GPa"])) / B_["H"]
V["A4_rect"] = f(L5rect, 1)
cc = C_
pd = cc["pred"]
V.update(A5_EI0=f(pd["EI0"], 0), A5_EIf=f(pd["EIfull"], 0), A5_dsh=f(100 * pd["dsh"] / cc["bonded"]["C"], 2), A5_slipL=f(pd["slip_loose"] * 1e9, 2))
for cfg in ("loose", "bolted", "bonded"):
    x = cc[cfg]
    V.update({f"A5_EI_{cfg}": pm(x["EI"], 2 * x["uEI"], 0), f"A5_r_{cfg}": f(x["ratio"], 3), f"A5_eta_{cfg}": f(x["eta"], 3),
              f"A5_C_{cfg}": f(x["C"] * 1e9, 4), f"A5_s_{cfg}": pm(x["slip"] * 1e9, 2 * x["uslip"] * 1e9, 3)})
V["A5_loose_vs"] = f(100 * (cc["loose"]["EI"] / pd["EI0"] - 1), 2)
V["A5_bond_vs"] = f(100 * (cc["bonded"]["EI"] / pd["EIfull"] - 1), 2)
V["A5_ratio_lb"] = f(cc["bonded"]["EI"] / cc["loose"]["EI"], 3)
V["A5_slip_ag"] = agree(cc["loose"]["slip"] - pd["slip_loose"], 2 * math.hypot(cc["loose"]["uslip"], pd["slip_loose"] * pd["uEI_rel"]))
kb = cc["kb"]
V.update(A6_kb=pm(kb["kb_disc"] / 1e6, 2 * kb["u_kb"] / 1e6, 2), A6_kbs=f(kb["kb_smeared"] / 1e6, 2), A6_kbd=f(100 * kb["smeared_vs_disc"], 1),
         A6_sp=f(kb["slip_pred_per_N"] * 1e9, 3), A6_sm=pm(kb["slip_meas_per_N"] * 1e9, 2 * kb["u_slip_meas"] * 1e9, 3),
         A6_sd=f(100 * (kb["slip_meas_per_N"] / kb["slip_pred_per_N"] - 1), 2), A6_Fmax=f(max(kb["forces_max"]) / 1e3, 2),
         A6_Fb=f(kb["F_beer"] / 1e3, 2), A6_Fover=f(100 * (kb["F_beer"] / max(kb["forces_max"]) - 1), 0),
         A6_Flist=", ".join(f(x / 1e3, 2) for x in kb["forces_max"][:3]), A6_q=f(kb["q_beer"], 1), A6_tg=f(cc["bonded"]["tau_glue"], 2),
         A6_Pb=f(cc["bolted"]["Pmax"] / 1e3, 1), A6_Pg=f(cc["bonded"]["Pmax"] / 1e3, 1), A6_tb=f(max(kb["forces_max"]) / (math.pi * 9), 0))
# M1 and challenge from the simulation
V.update(M1_flat=f(100 * (SIM["Rflat"] - 1), 1), M1_short=f(SIM["short"]["ratio"], 2), M1_Fd=f(SIM["lay"]["Fd"] / 1e3, 2), M1_Fb=f(SIM["lay"]["Fb"] / 1e3, 2),
         M1_few_sm=f(SIM["few"]["sm"] * 1e3, 3), M1_few_d=f(SIM["few"]["d"] * 1e3, 3), M1_few_pct=f(100 * (SIM["few"]["d"] / SIM["few"]["sm"] - 1), 1),
         M1_few_n=str(SIM["few"]["n"]), M1_few_s=f(100 * (SIM["few"]["sd"] / SIM["few"]["ssm"] - 1), 0), M1_few_Fd=f(SIM["few"]["Fd"] / 1e3, 2), M1_few_Fb=f(SIM["few"]["Fb"] / 1e3, 1), M1_ia=f(1e3 / SIM["lay"]["alpha"], 0), M1_ia_few=f(1e3 / SIM["few"]["alpha"], 0),
         M1_soft_eta=f(SIM["soft"]["eta"], 3), M1_G95=f(SIM["G95"] / 1e6, 1), M1_etaLab=f(SIM["etaLab"], 4))
fd = SIM["fd"]
V["C2_rows"] = ", ".join(f"N = {r_['N']}: {r_['v']:.5f}" for r_ in fd)
V["C2_ratio"] = f((fd[1]["v"] - fd[0]["v"]) / (fd[2]["v"] - fd[1]["v"]), 2) + " and " + f((fd[2]["v"] - fd[1]["v"]) / (fd[3]["v"] - fd[2]["v"]), 2)
V["C2_rich"] = f((4 * fd[3]["v"] - fd[2]["v"]) / 3, 5)
V["C3_rows"] = "; ".join(f"{r_['N']} elements: full {100 * r_['full']:.1f} %, reduced {100 * r_['red']:.2f} %" for r_ in SIM["lock"])
# X2 flange shear flow at the junction, V = 10 kN (measured section)
d_ = (B_["H"] - B_["tf"]) / 2
qhalf = 10000 * B_["tf"] * (B_["B"] - B_["tw"]) / 2 * d_ / B_["I"]
qweb = 10000 * B_["tw"] * B_["tf"] * d_ / B_["I"]
V.update(X2_qh=f(qhalf, 1), X2_qw=f(qweb, 1), X2_qj=f(2 * qhalf + qweb, 1))
# D1
dz = D_
bu, bs = dz["best"]["uniform"], dz["best"]["stepped"]
V.update(D_V=f(dz["Vmax"] / 1e3, 1), D_M=f(dz["Mmax"] / 1e3, 2), D_q0=f(dz["q0"] / 1e3, 0), D_smax=f(dz["s_max_end"] * 1e3, 1), D_kb=f(dz["kb_M10"] / 1e6, 1),
         D_full=f(dz["d_full"] * 1e3, 2), D_loose=f(dz["d_loose"] * 1e3, 2), D_allow=f(dz["d_allow"] * 1e3, 1), D_sig=f(dz["sigma"] / 1e6, 1), D_tau=f(dz["tau_int"] / 1e6, 2),
         D_u_s=f(bu["s1"] * 1e3, 0), D_u_n=str(bu["n"]), D_u_F=f(bu["Fbeer"] / 1e3, 2), D_u_Fm=f(bu["Fmodel"] / 1e3, 2), D_u_d=f(bu["delta"] * 1e3, 2),
         D_s_e=f(bs["e"] * 1e3, 0), D_s_s1=f(bs["s1"] * 1e3, 0), D_s_s2=f(bs["s2"] * 1e3, 0), D_s_n=str(bs["n"]), D_s_F=f(bs["Fbeer"] / 1e3, 2),
         D_s_Fm=f(bs["Fmodel"] / 1e3, 2), D_s_d=f(bs["delta"] * 1e3, 2), D_s_save=str(bu["n"] - bs["n"]))

tmpl = (HERE / "lab05_instructor_key.template.md").read_text(encoding="utf-8")
missing = sorted(set(re.findall(r"«(\w+)»", tmpl)) - set(V))
if missing:
    raise SystemExit(f"missing values: {missing}")
out = re.sub(r"«(\w+)»", lambda m: V[m.group(1)], tmpl)
(HERE / "lab05_instructor_key.md").write_text(out, encoding="utf-8")
(HERE / "key_values.json").write_text(json.dumps(V, indent=1, ensure_ascii=False))
print("wrote lab05_instructor_key.md;", len(V), "values")

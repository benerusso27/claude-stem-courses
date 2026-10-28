"""Generate lab09_instructor_key.md from computed results (no hand-typed numbers).

    python3 lab09_analysis.py && python3 make_key.py

Inputs: results.json (lab09_analysis.py on sample_data.csv), specimen_measurements.json, and the simulation's own
model code run in Node (dumped to sim_numbers.json). Placeholders in the template are written «name».
"""
import json
import math
import re
import subprocess
from pathlib import Path

import lab09_model as LM

HERE = Path(__file__).resolve().parent
LAB = HERE.parent
OUT = json.loads((HERE / "results.json").read_text())
MEAS = json.loads((HERE / "specimen_measurements.json").read_text())
TRUTH = json.loads((HERE / "truth.json").read_text())
REF = MEAS["reference"]
X = OUT["xtra"]
V = {}
PI = math.pi


def f(x, nd):
    if abs(x) < 0.5 * 10 ** (-nd):
        x = 0.0
    return f"{x:,.{nd}f}".replace(",", " ").replace("-", "−")


def pm(x, Ux, nd):
    return f"{f(x, nd)} ± {f(Ux, nd)}"


def agree(ok):
    return "agree" if ok else "disagree"


# ------------------------------------------------------------------ simulation numbers (exact page code)
JS = r"""
const {loadModel}=require('%s'); const M=loadModel('%s'); const o={}, P=M.PRESETS;
const sA=M.section(P.partA450); o.A450={cf:M.closedPcr(P.partA450,P.partA450.E,sA.I).P, fe:M.feBuckle(P.partA450.E*sA.I,P.partA450.L,P.partA450.Ne,M.endsOf(P.partA450)).P};
const pk=Object.assign({},P.springsB,{k:2800}); const sk=M.section(pk), ck=M.closedPcr(pk,pk.E,sk.I); o.spr={P:ck.P,K:ck.K, ideal:M.euler(pk.E,sk.I,0.5*pk.L)};
const c2=P.partC2, s2=M.section(c2); o.C2={PYn:M.secantPYnum(c2.E,s2.I,s2.A,s2.c,c2.L,c2.sY,c2.e,2*Math.round(c2.Nfd/2),c2.d0), lin:c2.sY*s2.A/(1+(c2.e+c2.d0*4/Math.PI)*s2.c/s2.r**2)};
const d=P.partD, sd=M.section(d), sl=d.L/sd.r; const st=M.tangentCurve(sl,d.E,d.sY,d.m);
const fp=M.fiberPath({b:d.b,t:d.t,L:d.L,E:d.E,s02:d.sY,m:d.m,d0:d.d0,e:d.e,dmax:Math.max(20*(d.d0+d.e),d.t*0.4),nstep:140,nf:d.nf});
o.D={E:M.euler(d.E,sd.I,d.L), t:st*sd.A, r:M.tangentCurve(sl,d.E,d.sY,d.m,true)*sd.A, fib:fp.Pmax, sl};
console.log(JSON.stringify(o));
""" % ((LAB.parent / "shared" / "test_harness.js").as_posix(), (LAB / "lab09_simulation.html").as_posix())
SIM = json.loads(subprocess.run(["node", "-e", JS], capture_output=True, text=True, check=True).stdout)
(HERE / "sim_numbers.json").write_text(json.dumps(SIM, indent=1))

# ------------------------------------------------------------------ pre-lab (nominal section, Table 1)
E2, sY = REF["E_al_GPa"] * 1e9, REF["sY_al_MPa"] * 1e6
nom = LM.rect(25.4e-3, 6.35e-3)
A_, I_, r_, c_ = nom["A"], nom["I"], nom["r"], nom["c"]
Pe = {L: LM.euler(E2, I_, L / 1e3) for L in (300, 450, 600)}
V.update(P_A=f(A_ * 1e6, 2), P_I=f(I_ * 1e12, 1), P_r=f(r_ * 1e3, 3), P_EI=f(E2 * I_, 2))
for L in (300, 450, 600):
    V[f"P1_sl{L}"] = f(L / 1e3 / r_, 1)
    V[f"P1_P{L}"] = f(Pe[L], 0)
    V[f"P1_s{L}"] = f(Pe[L] / A_ / 1e6, 2)
P_ff = LM.euler(E2, I_, 0.5 * 0.600)
P_fp = LM.euler(E2, I_, LM.K_FACTORS["fixed-pinned"] * 0.640)
P_90 = LM.euler(E2, I_, 0.090)
V.update(P1_ff=f(P_ff, 0), P1_fp=f(P_fp, 0), P1_90=f(P_90 / 1e3, 1), P1_s90=f(P_90 / A_ / 1e6, 0), P1_sYA=f(sY * A_ / 1e3, 1), P1_slY=f(PI * math.sqrt(E2 / sY), 1),
         P1_sl90=f(0.090 / r_, 1))
V.update(P1_d50=f(0.5 * 0.5 / 0.5, 2), P1_d75=f(0.5 * 0.75 / 0.25, 2), P1_d90=f(0.5 * 0.9 / 0.1, 2))
# P3 (readings generated from Eq. 5 with Pcr = 1800 N and delta0 = 0.5 mm)
pts = [(900, 0.50), (1200, 1.00), (1500, 2.50), (1650, 5.50)]
sw3 = LM.southwell([d * 1e-3 for _, d in pts], [P for P, _ in pts])
V.update(P3_y=", ".join(f(d / P * 1e3, 3) for P, d in pts), P3_P=f(sw3["Pcr"], 0), P3_d0=f(sw3["delta0"] * 1e3, 2), P3_slope=f(sw3["slope"] * 1e6, 1), P3_icpt=f(sw3["icpt"] * 1e6, 3))
# P4: 450 mm, e = 2 mm, P = 0.5 Pcr
P4 = 0.5 * Pe[450]
ym = LM.ymax_secant(2e-3, P4, Pe[450])
M4 = P4 * (2e-3 + ym)
s_ax, s_b, s_b0 = P4 / A_, M4 * c_ / I_, P4 * 2e-3 * c_ / I_
V.update(P4_P=f(P4, 0), P4_y=f(ym * 1e3, 2), P4_M=f(M4, 2), P4_s=f((s_ax + s_b) / 1e6, 1), P4_s0=f((s_ax + s_b0) / 1e6, 1), P4_ax=f(s_ax / 1e6, 2),
         P4_sb=f(s_b / 1e6, 1), P4_sb0=f(s_b0 / 1e6, 1), P4_fac=f(s_b / s_b0, 2), P4_secant=f(LM.sigmax_secant(P4, A_, 2e-3, c_, r_, Pe[450]) / 1e6, 1))
assert abs(LM.sigmax_secant(P4, A_, 2e-3, c_, r_, Pe[450]) - (s_ax + s_b)) < 1e-6 * s_b
# P5 (simulation, exact page code)
V.update(sim_A450=f(SIM["A450"]["cf"], 1), sim_A450fe=f(SIM["A450"]["fe"], 1), sim_sprP=f(SIM["spr"]["P"], 0), sim_sprK=f(SIM["spr"]["K"], 4),
         sim_sprI=f(SIM["spr"]["ideal"], 0), sim_C2PY=f(SIM["C2"]["PYn"], 0), sim_C2lin=f(SIM["C2"]["lin"], 0), sim_DE=f(SIM["D"]["E"] / 1e3, 2),
         sim_Dt=f(SIM["D"]["t"] / 1e3, 2), sim_Dr=f(SIM["D"]["r"] / 1e3, 2), sim_Dfib=f(SIM["D"]["fib"] / 1e3, 2), sim_Dsl=f(SIM["D"]["sl"], 1))
# P6
s6 = Pe[300] / A_ + Pe[300] * (0.3e-3 + 5e-3) * c_ / I_
V.update(P6_s=f(s6 / 1e6, 0), P6_pct=f(100 * s6 / sY, 0))
maxs = max(r["smax"] for r in TRUTH["rec"] if r.get("part") in ("A", "B", "C"))
V.update(P6_true=f(maxs / 1e6, 0), P6_true_pct=f(100 * maxs / sY, 0))

# ------------------------------------------------------------------ results
g = OUT["geom"]
V.update(b=pm(g["b"], 2 * g["ub"], 3), t=pm(g["t"], 2 * g["ut"], 3), A=f(g["A"], 2), I=f(g["I"], 1), uI=f(200 * g["urI"], 2), r=f(g["r"], 4), EI=f(g["EI"], 2))
A = OUT["A"]
rows = []
for k in ("300", "450", "600"):
    a = A[k]
    V[f"A{k}_PS"] = pm(a["PS"], 2 * a["uPS"], 0)
    V[f"A{k}_Pe"] = pm(a["Pe"], 2 * a["uPe"], 0)
    V[f"A{k}_d"] = f(a["diff_pct"], 2)
    V[f"A{k}_lim"] = f(a["lim_pct"], 2)
    V[f"A{k}_ag"] = agree(a["agree"])
    V[f"A{k}_d0"] = pm(a["d0S"], 2 * a["ud0S"], 3)
    V[f"A{k}_bow"] = f(a["bow"], 2)
    V[f"A{k}_eeq"] = f(a["e_eq"], 3)
    V[f"A{k}_ES"] = pm(a["ES"], 2 * a["uES"], 2)
    V[f"A{k}_n"] = str(a["n"])
    V[f"A{k}_Pmin"] = f(a["Pmin"], 0)
    V[f"A{k}_last"] = f(a["ratio_last"], 3)
    rows.append(f"| {k} | {f(a['slenderness'], 1)} | {pm(a['Pe'], 2 * a['uPe'], 0)} | {pm(a['PS'], 2 * a['uPS'], 0)} | {f(a['diff_pct'], 2)} | {f(a['lim_pct'], 2)} | "
                f"{pm(a['d0S'], 2 * a['ud0S'], 3)} | {f(a['bow'], 2)} | {pm(a['ES'], 2 * a['uES'], 2)} |")
V["A_table"] = "\n".join(rows)
V["eeq_mean"] = f(sum(A[k]["e_eq"] for k in A) / 3, 2)
xs_ = [A[k]["d0S"] - A[k]["bow"] for k in A]
V.update(bowx_lo=f(min(xs_), 2), bowx_hi=f(max(xs_), 2), last_lo=f(min(A[k]["ratio_last"] for k in A), 3), last_hi=f(max(A[k]["ratio_last"] for k in A), 3))
V.update(A_slope=pm(OUT["A_slope"]["slope"], 2 * OUT["A_slope"]["u"], 3), ES=pm(OUT["A_E"]["ES"], 2 * OUT["A_E"]["uES"], 2), ES_d=f(OUT["A_E"]["diff_pct"], 2),
         ES_lim=f(OUT["A_E"]["lim_pct"], 2), ES_ag=agree(OUT["A_E"]["agree"]), ref_E=pm(REF["E_al_GPa"], 2 * REF["u_E_al_GPa"], 2))
gE = OUT["A_gage"]
gE_lim = 2 * math.hypot(gE["uE"], REF["u_E_al_GPa"])
V.update(Eg=pm(gE["E"], 2 * gE["uE"], 2), Eg_n=str(gE["n"]), Eg_ag=agree(abs(gE["E"] - REF["E_al_GPa"]) <= gE_lim), Eg_d=f(gE["E"] - REF["E_al_GPa"], 2), Eg_lim=f(gE_lim, 2),
         Eg_icpt=f(gE["icpt_ue"], 1))
sS = OUT["A_strainSW"]
V.update(C1_PS=pm(sS["PS"], 2 * sS["uPS"], 0), C1_d=f(sS["diff_pct"], 2), C1_eps0=f(sS["eps0"], 0))
# Part B
B = OUT["B"]
for nm in ("ff", "fp"):
    b_ = B[nm]
    V.update({f"B{nm}_PS": pm(b_["PS"], 2 * b_["uPS"], 0), f"B{nm}_Pe": pm(b_["Pe"], 2 * b_["uPe"], 0), f"B{nm}_d": f(b_["diff_pct"], 2), f"B{nm}_lim": f(b_["lim_pct"], 2),
              f"B{nm}_ag": agree(b_["agree"]), f"B{nm}_K": pm(b_["K"], 2 * b_["uK"], 4), f"B{nm}_K0": f(b_["K0"], 3), f"B{nm}_over": f(100 * (b_["Pe"] / b_["PS"] - 1), 1),
              f"B{nm}_n": str(b_["n"]), f"B{nm}_d0": f(b_["d0S"], 3)})
k_ = B["k"]
V.update(B_k=f"{f(round(k_['k'], -1), 0)} ± {f(round(2 * k_['uk'], -1), 0)}", B_klo=f(round(k_["k_lo"], -1), 0),
         B_khi=f(round(k_["k_hi"], -1), 0), B_kLEI=f(B["kL_EI"], 1), B_pred=pm(B["fp_pred"]["P"], 2 * B["fp_pred"]["uP"], 0), B_pred_d=f(B["fp_pred"]["diff_pct"], 2),
         B_pred_lim=f(B["fp_pred"]["lim_pct"], 2), B_pred_ag=agree(B["fp_pred"]["agree"]), B_predK=f(B["fp_pred"]["K"], 4),
         k_true=f((TRUTH["k_clamp"][0] + TRUTH["k_clamp"][1]) / 2, 0), k_fp=f(round(X["k_from_fp"], -1), 0))
# Part C
C = OUT["C"]
for en in ("1", "2"):
    c = C[en]
    V.update({f"C{en}_e": pm(c["e_fit"], 2 * c["ue"], 3), f"C{en}_es": pm(c["e_strain"], 2 * c["ue_strain"], 3), f"C{en}_ag": agree(c["agree"]),
              f"C{en}_ratio": f(c["ratio_12_6"], 2), f"C{en}_raw": f(X[f"C{en}_raw_e"], 2), f"C{en}_swP": f(X[f"C{en}_sw"]["PS"], 0),
              f"C{en}_swd0": f(X[f"C{en}_sw"]["d0"], 3), f"C{en}_swe": f(X[f"C{en}_sw"]["e_from_d0"], 2)})
V["C_ratio_th"] = f(C["1"]["ratio_12_6_th"], 2)
rows = []
for r1, r2 in zip(C["1"]["tab"], C["2"]["tab"]):
    if int(r1["P"]) % 200 == 0:
        rows.append(f"| {f(r1['P'], 0)} | {f(r1['dA'], 2)} | {f(r1['dC'], 2)} | {f(r1['dd'], 2)} | {f(r1['th'], 2)} | {f(r2['dC'], 2)} | {f(r2['dd'], 2)} | {f(r2['th'], 2)} |")
V["C_table"] = "\n".join(rows)
PY = C["PY"]
V.update(PY1=f(PY["1"]["PY"], 0), PY2=f(PY["2"]["PY"], 0), PYl1=f(PY["1"]["PYlin"] / 1e3, 1), PYl2=f(PY["2"]["PYlin"] / 1e3, 1), PYr1=f(PY["1"]["ratio_Pcr"], 3),
         PYr2=f(PY["2"]["ratio_Pcr"], 3), PYo2=f(PY["2"]["PYlin"] / PY["2"]["PY"], 1), PYy2=f(PY["2"]["ymax_at_PY"], 1))
st = C["stress"]
V.update(st_P=f(st["P"], 0), st_meas=f(st["s_meas"], 1), st_1035=f(st["s_1035"], 1), st_A=f(st["s_A"], 1), st_ax=f(st["s_axial"], 2), st_sum=f(st["s_sum"], 1),
         st_pct=f(100 * (st["s_sum"] / st["s_meas"] - 1), 1), st_low=f(100 * (1 - st["s_1035"] / st["s_meas"]), 0))
# Part D
D = OUT["D"]
uPD = D["Pmax"] * D["urP"]
V.update(D_P=pm(D["Pmax"] / 1e3, 2 * uPD / 1e3, 2), D_s=f(D["smax"], 0), D_sl=f(D["slender"], 1), D_PE=f(D["PE"] / 1e3, 2), D_sE=f(D["sE"], 0), D_PY=f(D["PY"] / 1e3, 2),
         D_Pt=f(D["Pt"] / 1e3, 2), D_st=f(D["s_t"], 0), D_Pr=f(D["Pr"] / 1e3, 2), D_sr=f(D["s_r"], 0), D_aa=f(D["aa"], 1), D_Paa=f(D["Paa"] / 1e3, 2),
         D_aa195=f(D["aa195"], 0), D_Paa195=f(1.95 * D["Paa"] / 1e3, 2), D_Eo=f(D["E_over"], 0), D_Yo=f(D["Y_over"], 0), D_to=f(D["t_over"], 1), D_slY=f(D["sl_Y"], 1),
         D_aa_d=f(100 * (1.95 * D["Paa"] / D["Pmax"] - 1), 1), D_dmax=f(D["d_at_max"], 2), D_Et=f(D["Et_at_t"], 1))
# M1
M1 = OUT["M1"]
V.update(M1_L60=f(M1["elastica_at_L60"], 3), M1_L10=f(M1["elastica_at_L10"], 2), M1_yd=f(M1["yield_defl_450"], 1), M1_k1=f(X["kLEI_1pct"], 0))
V.update(C2_sens=f(X["C2_sens"], 1), C2_x=f(X["C2_x"], 4), C2_fp=f(X["C2_sens_fp"], 0))
# D1
D1 = OUT["D1"]
rows = []
for r in sorted(D1["table"], key=lambda r_: r_["mass"]):
    p_, c_ = r["pin"], r["clamp"]
    rows.append(f"| {f(r['Do'], 2)} × {f(r['t'], 2)} | {f(r['mass'], 3)} | {f(r['Dt'], 1)} | {f(p_['sl'], 1)} | {f(p_['Pall'] / 1e3, 2)} | {f(p_['PY'] / 1e3, 2)} | "
                f"{'yes' if p_['ok'] else 'no'} | {f(c_['Pall'] / 1e3, 2)} | {'yes' if c_['ok'] else 'no'} |")
V["D1_table"] = "\n".join(rows)
bt, tr, trp = X["D1_best"], X["D1_trap"], X["D1_trap_pin"]
bp, bc = D1["best"]["pin"], D1["best"]["clamp"]
V.update(D1_best=f"{f(bp[0], 2)} × {f(bp[1], 2)}", D1_trap=f"{f(bc[0], 2)} × {f(bc[1], 2)}", D1_m=f(bt["mass"], 3), D1_A=f(bt["A"], 1), D1_I=f(bt["I"] / 1e3, 1), D1_r=f(bt["r"], 2),
         D1_sl=f(bt["sl"], 1), D1_sall=f(bt["sall"], 1), D1_Pall=f(bt["Pall"] / 1e3, 2), D1_Pcr=f(bt["Pcr"] / 1e3, 2), D1_PY=f(bt["PY"] / 1e3, 2), D1_req=f(1.95 * 12, 1),
         D1_ymax=f(bt["ymax"], 2), D1_smax=f(bt["smax"], 1), D1_Dt=f(bt["Dt"], 1), D1_PstFS=f(bt["P_stressFS"] / 1e3, 1), D1_PYFS=f(bt["PY_FS"] / 1e3, 2),
         D1_tm=f(tr["mass"], 3), D1_tsl=f(tr["sl"], 1), D1_tPall=f(tr["Pall"] / 1e3, 2), D1_tPY=f(tr["PY"] / 1e3, 2), D1_tpsl=f(trp["sl"], 1),
         D1_tpPall=f(trp["Pall"] / 1e3, 2), D1_tpPcr=f(trp["Pcr"] / 1e3, 2), D1_tpPY=f(trp["PY"] / 1e3, 2), D1_save=f(100 * (1 - tr["mass"] / bt["mass"]), 0))
# truth description
T = TRUTH
V.update(T_E=f(T["E"] / 1e9, 1), T_b=f(T["b"] * 1e3, 2), T_t=f(T["t"] * 1e3, 3), T_gain=f(100 * (T["load_gain"] - 1), 1), T_ek=f(T["e_knife"] * 1e3, 2),
         T_k=", ".join(f(k, 0) for k in T["k_clamp"]), T_d0=", ".join(f(T["A"][k]["d0"] * 1e3, 2) for k in ("300", "450", "600")), T_C=", ".join(f(T["C"][k] * 1e3, 2) for k in ("1", "2")),
         T_s02=f(T["s02"] / 1e6, 0), T_m=str(T["m"]), T_DPm=f([r for r in T["rec"] if r.get("part") == "D"][0]["Pmax"] / 1e3, 2), T_utm=f(100 * (T["utm_gain"] - 1), 1))

tmpl = (HERE / "lab09_instructor_key.template.md").read_text(encoding="utf-8")
missing = sorted(set(re.findall(r"«(\w+)»", tmpl)) - set(V))
if missing:
    raise SystemExit(f"missing values: {missing}")
out = re.sub(r"«(\w+)»", lambda m: V[m.group(1)], tmpl)
(HERE / "lab09_instructor_key.md").write_text(out, encoding="utf-8")
(HERE / "key_values.json").write_text(json.dumps(V, indent=1, ensure_ascii=False))
print("wrote lab09_instructor_key.md;", len(V), "values")

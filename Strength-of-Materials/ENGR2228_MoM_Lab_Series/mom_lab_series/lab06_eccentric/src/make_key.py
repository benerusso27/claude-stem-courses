"""Generate lab06_instructor_key.md from computed results (no hand-typed numbers).

    python3 lab06_analysis.py && python3 make_key.py

Inputs: results.json (lab06_analysis.py on sample_data.csv), specimen_measurements.json, and the simulation's own
model code run in Node (dumped to sim_numbers.json). Placeholders in the template are written «name».
"""
import json
import math
import re
import subprocess
from pathlib import Path

import numpy as np

import lab06_model as LM

HERE = Path(__file__).resolve().parent
LAB = HERE.parent
R = json.loads((HERE / "results.json").read_text())
MEAS = json.loads((HERE / "specimen_measurements.json").read_text())
REF = MEAS["reference"]
A_, B_, C_, D_ = R["A"], R["B"], R["C"], R["D1"]
V = {}


def f(x, nd):
    return f"{x:,.{nd}f}".replace(",", " ").replace("-", "−")


def pm(x, U, nd):
    return f"{f(x, nd)} ± {f(U, nd)}"


def agree(d, lim):
    return "agree" if abs(d) <= lim else "disagree"


# ------------------------------------------------------------------ simulation numbers (exact page code)
JS = r"""
const {loadModel}=require('%s'); const M=loadModel('%s'); const o={};
const PP=(k,ov={})=>Object.assign(M.presetParams(k),ov);
{ const p=PP('partA2'), c=M.sectionClosed(p); const v=c.hull.map(([z,y])=>M.stressClosed(c,p.P,p.ey,p.ez,y-c.yc,z-c.zc)); o.A2={smax:Math.max(...v), smin:Math.min(...v), yNA:-(c.Iz/c.A)/p.ey}; }
{ const p=PP('partB'), c=M.sectionClosed(p); const g=[[0,0.044],[0,0.012],[-0.012,0],[-0.044,0]];
  o.B={s:g.map(([z,y])=>M.stressClosed(c,p.P,p.ey,p.ez,y-c.yc,z-c.zc)), n:g.map(([z,y])=>M.stressNaive(c,p.P,p.ey,p.ez,y-c.yc,z-c.zc)),
       nmax:Math.max(...c.hull.map(([z,y])=>M.stressNaive(c,p.P,p.ey,p.ez,y-c.yc,z-c.zc))), smax:Math.max(...c.hull.map(([z,y])=>M.stressClosed(c,p.P,p.ey,p.ez,y-c.yc,z-c.zc))),
       kern:M.polyArea(M.kernClosed(p,c)), th:c.th};
  const cs=M.columnSolve(p,512); o.B.Cmin=cs.dirs[0].cf.Cmid; o.B.Cmaj=cs.dirs[1].cf.Cmid;
  const pf=PP('partB',{r:4.8e-3}), cf=M.sectionClosed(pf); o.B.fil=g.map(([z,y])=>M.stressClosed(cf,pf.P,-4.76e-3-cf.yc,-28.58e-3-cf.zc,y-cf.yc,z-cf.zc)); }
{ const p=PP('partC'), cs=M.columnSolve(p,512), d=cs.dirs[0]; o.C={Cmid:d.cf.Cmid, Cend:d.cf.Cend, w:d.e*(1-d.cf.Cmid), P5:M.p5Closed(d.EI,p.L,p.a,1), Pcr:d.Pcr, PE:d.PE,
  Cc25:M.bcClosed(-25e3,d.EI,p.L,p.a).Cmid, Cc40:M.bcClosed(-40e3,d.EI,p.L,p.a).Cmid, P5c:M.p5Closed(d.EI,p.L,p.a,-1)}; }
{ const p=PP('partAcol'), cs=M.columnSolve(p,512), d=cs.dirs[1]; o.Acol={C:d.cf.Cmid, Pcr:d.Pcr, P5:M.p5Closed(d.EI,p.L,p.a,1)}; }
{ const p=PP('tube8'), top=M.tubeClosed(p,0), side=M.tubeClosed(p,Math.PI/2), other=M.tubeClosed(p,1.5*Math.PI); o.T={M:top.M, T:top.T, V:top.V, stop:top.sigma, ttop:top.tau, tT:top.tauT, tV:side.tauV, tside:side.tau, tother:other.tau, I:top.I, J:top.J, A:top.A}; }
{ const p=PP('design'), c=M.sectionClosed(p); o.D={smax:Math.max(...c.hull.map(([z,y])=>M.stressClosed(c,p.P,p.ey,p.ez,y-c.yc,z-c.zc)))}; }
console.log(JSON.stringify(o));
""" % ((LAB.parent / "shared" / "test_harness.js").as_posix(), (LAB / "lab06_simulation.html").as_posix())
SIM = json.loads(subprocess.run(["node", "-e", JS], capture_output=True, text=True, check=True).stdout)
(HERE / "sim_numbers.json").write_text(json.dumps(SIM, indent=1))

# ------------------------------------------------------------------ pre-lab (nominal dimensions, Table 1)
E = REF["E_al_GPa"] * 1e3                                              # MPa
h, b, L, a = 50.8, 12.7, 250.0, 25.0
A = h * b
PA = 30e3 / A
e2 = h / 3
s_at = lambda y: PA * (1 + 12 * e2 * y / h ** 2)  # noqa: E731
Iz, Iy = b * h ** 3 / 12, h * b ** 3 / 12
PEz, PEy = math.pi ** 2 * E * Iz / L ** 2, math.pi ** 2 * E * Iy / L ** 2
V.update(P1_A=f(A, 2), P1_PA=f(PA, 2), P1_smax=f(PA * 3, 1), P1_smin=f(-PA, 1), P1_y0=f(-h / 4, 1), P1_s20=f(s_at(20), 1), P1_sm20=f(s_at(-20), 1),
         P1_e20=f(s_at(20) / E * 1e6, 0), P1_em20=f(s_at(-20) / E * 1e6, 0))
PAc = 25e3 / A
V.update(P1_PAc=f(PAc, 2), P1_sf=f(PAc * (1 + 6 * (b / 2) / b), 1), P1_sb=f(PAc * (1 - 6 * (b / 2) / b), 1), P1_ef=f(PAc * 4 / E * 1e6, 0), P1_eb=f(PAc * -2 / E * 1e6, 0))
V.update(P1_Iz=f(Iz, 0), P1_Iy=f(Iy, 1), P1_PEz=f(PEz / 1e3, 0), P1_PEy=f(PEy / 1e3, 1), P1_rz=f(30e3 / PEz, 3), P1_ry=f(25e3 / PEy, 3),
         P1_ez=f(100 * math.pi ** 2 / 8 * 30e3 / PEz, 1), P1_ey=f(100 * math.pi ** 2 / 8 * 25e3 / PEy, 0))
# P3: nominal angle, two rectangles
bn, tn = 50.8, 6.35
sec = LM.angle(bn, bn, tn)
pr = LM.props(sec)
th = 0.5 * math.atan2(-2 * pr["Iyz"], pr["Iz"] - pr["Iy"])
toUV = lambda y, z: (z * math.cos(th) + y * math.sin(th), -z * math.sin(th) + y * math.cos(th))  # noqa: E731
yP, zP = -4.76 - pr["yc"], -28.58 - pr["zc"]
uP, vP = toUV(yP, zP)
V.update(P3_A=f(pr["A"], 1), P3_c=f(pr["yc"], 2), P3_I=f(pr["Iz"], 0), P3_Iyz=f(pr["Iyz"], 0), P3_Iu=f(pr["Imax"], 0), P3_Iv=f(pr["Imin"], 0),
         P3_yP=f(yP, 2), P3_zP=f(zP, 2), P3_uP=f(uP, 2), P3_vP=f(vP, 2), P3_PA=f(30e3 / pr["A"], 2), P3_th=f(math.degrees(th), 0))
gn = [(0, 44.0), (0, 12.0), (-12.0, 0), (-44.0, 0)]
rows = []
for k, (z, y) in enumerate(gn):
    yy, zz = y - pr["yc"], z - pr["zc"]
    u, v = toUV(yy, zz)
    s = LM.stress(pr, 30e3, yP, zP, yy, zz)
    sn = LM.stress(pr, 30e3, yP, zP, yy, zz, naive=True)
    rows.append(f"| G{k + 1} | {f(yy, 2)}, {f(zz, 2)} | {f(u, 2)}, {f(v, 2)} | {f(s, 1)} | {f(sn, 1)} |")
V["P3_table"] = "\n".join(rows)
# P5 from the simulation
V.update(sim_A2_smax=f(SIM["A2"]["smax"] / 1e6, 1), sim_A2_smin=f(SIM["A2"]["smin"] / 1e6, 2), sim_A2_y0=f(SIM["A2"]["yNA"] * 1e3, 2),
         sim_B=", ".join(f(x / 1e6, 1) for x in SIM["B"]["s"]), sim_Bn=f(SIM["B"]["nmax"] / 1e6, 1), sim_Bmax=f(SIM["B"]["smax"] / 1e6, 1),
         sim_C_Cmid=f(SIM["C"]["Cmid"], 4), sim_C_Cend=f(SIM["C"]["Cend"], 4), sim_C_w=f(SIM["C"]["w"] * 1e3, 3), sim_C_P5=f(SIM["C"]["P5"] / 1e3, 2),
         sim_C_Pcr=f(SIM["C"]["Pcr"] / 1e3, 1))

# ------------------------------------------------------------------ analysis
bar = R["bar"]
V.update(bar_h=pm(bar["h"], 2 * bar["uh"], 3), bar_b=pm(bar["b"], 2 * bar["ub"], 4), bar_r2=f(bar["rz2"], 1),
         bar_PEbs=f(bar["PEb_strong"] / 1e3, 0), bar_PEbw=f(bar["PEb_weak"] / 1e3, 1))
rows = []
for cfg, lab in (("e0", "0"), ("e1", "h/6"), ("e2", "h/3")):
    r = A_[cfg]
    d_bc = r["e_eff_max"] - r["pred_bc"]
    d_450 = r["e_eff_max"] - r["e_hole"]
    V.update({f"A1_{cfg}_eff": pm(r["e_eff_max"], 2 * r["u_e_eff"], 3), f"A1_{cfg}_hole": pm(r["e_hole"], 2 * r["u_hole"], 3),
              f"A1_{cfg}_bc": pm(r["pred_bc"], 2 * r["u_pred_bc"], 3), f"A1_{cfg}_dbc": f(abs(d_bc), 3), f"A1_{cfg}_lbc": f(r["agree_bc"], 3),
              f"A1_{cfg}_abc": agree(d_bc, r["agree_bc"]), f"A1_{cfg}_d450": f(abs(d_450), 3), f"A1_{cfg}_l450": f(r["agree_450"], 3),
              f"A1_{cfg}_a450": agree(d_450, r["agree_450"]), f"A1_{cfg}_sig0": pm(r["sig0"], 2 * r["u_sig0"], 2), f"A1_{cfg}_PA": pm(r["PA"], 2 * r["u_PA"], 2),
              f"A2_{cfg}_y0": f(r["yNA"], 2) if abs(r["yNA"]) < 10 * bar["h"] else "far outside", f"A2_{cfg}_p": f(r["yNA_pred"], 2) if abs(r["yNA_pred"]) < 10 * bar["h"] else "—",
              f"A2_{cfg}_pbc": f(r["yNA_pred_bc"], 2) if abs(r["yNA_pred_bc"]) < 10 * bar["h"] else "—", f"A3_{cfg}_pb": f(r["pct_bend_z"], 2), f"A3_{cfg}_ez": f(r["ez_eff"], 3),
              f"A2_{cfg}_prod": f(r["yNA"] * r["e_eff_max"], 1) if abs(r["yNA"]) < 10 * bar["h"] else "—"})
    rows.append(f"| {lab} | {pm(r['e_eff_max'], 2 * r['u_e_eff'], 3)} | {pm(r['e_hole'], 2 * r['u_hole'], 2)} | {agree(d_450, r['agree_450'])} | "
                f"{pm(r['pred_bc'], 2 * r['u_pred_bc'], 3)} | {agree(d_bc, r['agree_bc'])} | {pm(r['sig0'], 2 * r['u_sig0'], 2)} | "
                f"{V[f'A2_{cfg}_y0']} | {f(r['pct_bend_z'], 2)} |")
V["A1_table"] = "\n".join(rows)
V.update(A1_C=f(A_["e2"]["C"], 4), A1_uC=f(A_["e2"]["uC"], 4), A1_drop=f(100 * (1 - A_["e2"]["C"]), 1),
         A1_e1_drop=f(100 * (1 - A_["e1"]["e_eff_max"] / A_["e1"]["e_hole"]), 1), A1_e2_drop=f(100 * (1 - A_["e2"]["e_eff_max"] / A_["e2"]["e_hole"]), 1),
         A1_sig_max=f(A_["e2"]["sig_max"], 1), A1_sig_max450=f(A_["e2"]["sig_max_450"], 1), A1_sig_min=f(A_["e2"]["sig_min"], 1), A1_sig_min450=f(A_["e2"]["sig_min_450"], 1))
V["A2_edge"] = f(-bar["h"] / 2, 2)
V.update(A3_e0_spr=f(A_["e0"]["dfb_spread"], 0), A3_e2_sprr=f(A_["e2"]["dfb_spread_raw"], 0), A3_e2_spr=f(A_["e2"]["dfb_spread"], 0),
         A3_e2_raw=f(A_["e2"]["pct_bend_raw"], 2))
r2_ = A_["e2"]
V["A1_e2_sig0_ag"] = agree(r2_["sig0"] - r2_["PA"], 2 * math.hypot(r2_["u_sig0"], r2_["u_PA"]))
V["X1_ratio"] = f(LM.euler_load_blocks(1.0, 1.0, 0.1) / math.pi ** 2, 2)
V["A2_r2"] = f(-bar["rz2"], 1)
# A4 table
rows = []
for i, g in enumerate(B_["gages"]):
    d = B_["meas"][i] - B_["pred"][i]
    rows.append(f"| {g} | {pm(B_['meas'][i], 2 * B_['u_meas'][i], 1)} | {pm(B_['pred'][i], 2 * B_['u_pred'][i], 1)} | {f(d, 1)} | {f(B_['agree'][i], 1)} | "
                f"{agree(d, B_['agree'][i])} | {f(B_['naive'][i], 1)} | {f(B_['fil'][i], 1)} | {f(B_['filbc'][i], 1)} |")
V["A4_table"] = "\n".join(rows)
nagree = sum(abs(B_["meas"][i] - B_["pred"][i]) <= B_["agree"][i] for i in range(4))
nagree_bc = sum(abs(B_["meas"][i] - B_["filbc"][i]) <= B_["agree"][i] for i in range(4))
thB = 0.5 * math.atan2(-2 * B_["Iyz"], B_["Iz"] - B_["Iy"])
uPB = B_["zP"] * math.cos(thB) + B_["yP"] * math.sin(thB)
vPB = -B_["zP"] * math.sin(thB) + B_["yP"] * math.cos(thB)
V.update(B_bV=pm(B_["bV"], 2 * B_["ubV"], 2), B_bH=pm(B_["bH"], 2 * B_["ubH"], 2), B_t=pm(B_["t"], 2 * B_["ut"], 3), B_A=f(B_["A"], 1), B_yc=f(B_["yc"], 2),
         B_zc=f(B_["zc"], 2), B_Iz=f(B_["Iz"], 0), B_Iy=f(B_["Iy"], 0), B_Iyz=f(B_["Iyz"], 0), B_Iu=f(B_["Imax"], 0), B_Iv=f(B_["Imin"], 0),
         B_sum=f(B_["Imax"] + B_["Imin"], 0), B_sum2=f(B_["Iy"] + B_["Iz"], 0), B_th=f(math.degrees(thB), 2), B_yP=f(B_["yP"], 2), B_zP=f(B_["zP"], 2),
         B_uP=f(uPB, 2), B_vP=f(vPB, 2), B_PA=f(B_["PA"], 2), B_nagree=str(nagree), B_nagree_bc=str(nagree_bc), B_phim=f(B_["phi_meas"], 1),
         B_phip=f(B_["phi_pred"], 1), B_smax=f(B_["sig_max"], 1), B_smin=f(B_["sig_min"], 1), B_Cmin=f(B_["C_minor"], 3), B_Cmaj=f(B_["C_major"], 3),
         B_dA=f(100 * (B_["A_fil"] / B_["A"] - 1), 2), B_naive_err=f(max(abs(B_["naive"][i] - B_["pred"][i]) / abs(B_["pred"][i]) for i in range(4)) * 100, 0),
         B_G1_ratio=f(B_["meas"][0] / B_["PA"], 2))
resid = [B_["meas"][i] - B_["pred"][i] for i in range(4)]
V.update(B_res=", ".join(f(x, 1) for x in resid), B_res_fil=", ".join(f(B_["fil"][i] - B_["pred"][i], 1) for i in range(4)),
         B_res_bc=", ".join(f(B_["filbc"][i] - B_["fil"][i], 1) for i in range(4)))
# Part C (M1)
rows = []
for i, P in enumerate(C_["P"]):
    rows.append(f"| {f(P / 1e3, 2)} | {f(C_['Cmid_m'][i], 4)} | {f(C_['Cmid_p'][i], 4)} | {f(C_['Cend_m'][i], 4)} | {f(C_['Cend_p'][i], 4)} | "
                f"{f(C_['w'][i], 3)} | {f(C_['w_p'][i], 3)} |")
V["M1_table"] = "\n".join(rows)
k = -1
V.update(M1_Cm=pm(C_["Cmid_m"][k], 2 * C_["u_Cmid_m"], 4), M1_Cp=pm(C_["Cmid_p"][k], 2 * C_["u_Cmid_p"], 4), M1_Cd=f(abs(C_["Cmid_m"][k] - C_["Cmid_p"][k]), 4),
         M1_Cl=f(C_["agree_mid"], 4), M1_Ca=agree(C_["Cmid_m"][k] - C_["Cmid_p"][k], C_["agree_mid"]),
         M1_Em=pm(C_["Cend_m"][k], 2 * C_["u_Cend_m"], 4), M1_Ep=pm(C_["Cend_p"][k], 2 * C_["u_Cend_p"], 4), M1_Ed=f(abs(C_["Cend_m"][k] - C_["Cend_p"][k]), 4),
         M1_El=f(C_["agree_end"], 4), M1_Ea=agree(C_["Cend_m"][k] - C_["Cend_p"][k], C_["agree_end"]),
         M1_wm=pm(C_["w"][k], 2 * C_["u_w_m"], 3), M1_wp=pm(C_["w_p"][k], 2 * C_["u_w_p"], 3), M1_wd=f(abs(C_["w"][k] - C_["w_p"][k]), 3), M1_wl=f(C_["agree_w"], 3),
         M1_wa=agree(C_["w"][k] - C_["w_p"][k], C_["agree_w"]), M1_err=f(C_["err450_mid_pct"], 1), M1_errp=f(C_["err450_mid_pred_pct"], 1),
         M1_sf450=f(C_["sig_front_450"], 1), M1_sfmid=f(C_["sig_front_mid"], 1), M1_sfend=f(C_["sig_front_end"], 1),
         M1_sover=f(100 * (C_["sig_front_450"] / C_["sig_front_mid"] - 1), 0), M1_send_over=f(100 * (C_["sig_front_450"] / C_["sig_front_end"] - 1), 0),
         M1_P5w=f(C_["P5_weak"] / 1e3, 2), M1_P5s=f(C_["P5_strong"] / 1e3, 1), M1_P5wr=f(C_["P5w_over_PE"], 4), M1_P5sr=f(C_["P5s_over_PE"], 4),
         M1_Cc25=f(SIM["C"]["Cc25"], 3), M1_Cc40=f(SIM["C"]["Cc40"], 2), M1_P5c=f(SIM["C"]["P5c"] / 1e3, 2), M1_Pcr=f(SIM["C"]["Pcr"] / 1e3, 1),
         M1_PA=f(C_["PA_check"], 2), M1_sax=f(C_["sig_ax"], 2))
# C1 trends
for cfg in ("e1", "e2"):
    t = A_[cfg]["trend"]
    V.update({f"C1_{cfg}_s": pm(t["slope"] * 1e6, 2 * t["uslope"] * 1e6, 2), f"C1_{cfg}_sp": f(t["slope_pred"] * 1e6, 2), f"C1_{cfg}_e0": pm(t["e0"], 2 * t["ue0"], 3),
              f"C1_{cfg}_drop": f(t["drop_pct"], 1), f"C1_{cfg}_sig": f(abs(t["slope"]) / t["uslope"], 0)})
# C2
V.update(C2_EI=pm(C_["EI_fit"] / 1e6, 2 * C_["u_EI_fit"] / 1e6, 1), C2_EIr=pm(C_["EI_ref"] / 1e6, 2 * C_["u_EI_ref"] / 1e6, 1),
         C2_d=f(abs(C_["EI_fit"] - C_["EI_ref"]) / 1e6, 1), C2_l=f(C_["agree_EI"] / 1e6, 1), C2_a=agree(C_["EI_fit"] - C_["EI_ref"], C_["agree_EI"]),
         C2_pct=f(100 * (C_["EI_fit"] / C_["EI_ref"] - 1), 2))
# X2 tube
T = SIM["T"]
V.update(X2_M=f(T["M"], 1), X2_T=f(T["T"], 1), X2_V=f(T["V"], 0), X2_I=f(T["I"] * 1e12, 0), X2_J=f(T["J"] * 1e12, 0), X2_stop=f(T["stop"] / 1e6, 2),
         X2_tT=f(T["tT"] / 1e6, 2), X2_tV=f(T["tV"] / 1e6, 2), X2_tside=f(T["tside"] / 1e6, 2), X2_tother=f(T["tother"] / 1e6, 2))
# X3 kern of the nominal angle
hull_c = LM.to_centroidal(pr, sec["hull"])
K, karea = LM.kern(pr, hull_c)
ang = math.atan2(zP, yP)
dk = LM.kern_radius_along(pr, hull_c, ang)
V.update(X3_area=f(karea, 1), X3_sim=f(SIM["B"]["kern"] * 1e6, 1), X3_dk=f(dk, 2), X3_dP=f(math.hypot(yP, zP), 2), X3_nv=str(len(K)))
# D1
sa = D_["sa"]
rows = []
for d in D_["table"]:
    rows.append(f"| {d['name']} | {f(d['A'], 0)} | {f(d['mass'], 2)} | {f(d['PA'], 1)} | {f(d['s458'], 1)} | {f(d['smin458'], 1)} | {f(d['send'], 1)} | "
                f"{f(d['smid'], 1)} | {'yes' if d['ok'] else 'no'} |")
V["D_table"] = "\n".join(rows)
best = next(d for d in D_["table"] if d["name"] == D_["best"])
naive = next(d for d in D_["table"] if d["name"] == D_["naive_best"])
eq64 = next(d for d in D_["table"] if d["name"].startswith("L64"))
short = next(d for d in D_["table"] if "short" in d["name"])
l51 = next(d for d in D_["table"] if d["name"] == "L51 × 51 × 6.4")
V.update(D_sa=f(sa, 1), D_best=D_["best"], D_naive=D_["naive_best"], D_best_s=f(best["s458"], 1), D_best_m=f(best["mass"], 2), D_best_r=f(best["s458"] / sa, 2),
         D_naive_s=f(naive["s458"], 0), D_naive_r=f(naive["s458"] / sa, 2), D_naive_PA=f(naive["PA"], 1), D_64_s=f(eq64["s458"], 1),
         D_short_s=f(short["s458"], 1), D_51_s=f(l51["s458"], 1), D_51_end=f(l51["send"], 1), D_best_end=f(best["send"], 1), D_best_mid=f(best["smid"], 1),
         D_best_ratio=f(best["ratio"], 2), D_sim=f(SIM["D"]["smax"] / 1e6, 1), D_best_min=f(best["smin458"], 1))
V.update(ref_E=pm(REF["E_al_GPa"], 2 * REF["u_E_al_GPa"], 2), ref_sY=pm(REF["sY_al_MPa"], 2 * REF["u_sY_al_MPa"], 1))

tmpl = (HERE / "lab06_instructor_key.template.md").read_text(encoding="utf-8")
missing = sorted(set(re.findall(r"«(\w+)»", tmpl)) - set(V))
if missing:
    raise SystemExit(f"missing values: {missing}")
out = re.sub(r"«(\w+)»", lambda m: V[m.group(1)], tmpl)
(HERE / "lab06_instructor_key.md").write_text(out, encoding="utf-8")
(HERE / "key_values.json").write_text(json.dumps(V, indent=1, ensure_ascii=False))
print("wrote lab06_instructor_key.md;", len(V), "values")

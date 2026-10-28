"""Lab 6 independent verification (Python / numpy / scipy).

1. Cross-language, cross-method: the page's section properties (exact part formulas) vs Green's theorem on polygons
   plus adaptive quadrature for the fillet and the annulus (src/lab06_model.py).
2. The page's Eq. 4.58 in principal axes vs the general form sigma = P/A + P [yP zP] S^-1 [y z] (no principal axes).
3. The page's kern (antipoles of hull edges) vs an intersection of half-planes (scipy HalfspaceIntersection).
4. The page's beam-column closed forms vs scipy's collocation BVP solver; buckling loads vs brentq.
5. The page's tube formulas vs adaptive quadrature.
6. Closure: lab06_analysis.py on sample_data.csv recovers the generating (truth) values within its stated uncertainty.
"""
import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np

LAB = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LAB / "src"))
sys.path.insert(0, str(LAB.parent / "shared"))
from checklib import Checks  # noqa: E402
import lab06_model as PM  # noqa: E402

C = Checks("Lab 6 — independent checks (Python/scipy) and data-pipeline closure")
JS = r"""
const {loadModel}=require('%s'); const M=loadModel('%s'); const o={sec:[], bc:[], tube:[]};
const PP=(k,ov={})=>Object.assign(M.presetParams(k),ov);
const cases=[['partA2',{}],['partB',{}],['partB',{r:4.8e-3}],['tee',{}],['zsec',{}],['design',{}],['partA2',{shape:'channel',B:60e-3,H:120e-3,tf:8e-3,tw:6e-3,ey:10e-3,ez:15e-3}],['tube8',{mode:'section',P:20e3,ey:5e-3,ez:-8e-3}]];
for (const [k,ov] of cases) { const p=PP(k,ov), c=M.sectionClosed(p);
  const pts=c.hull.map(([z,y])=>({z,y,s:M.stressClosed(c,p.P,p.ey,p.ez,y-c.yc,z-c.zc)}));
  o.sec.push({k, p, A:c.A, yc:c.yc, zc:c.zc, Iz:c.Iz, Iy:c.Iy, Iyz:c.Iyz, Imax:c.Imax, Imin:c.Imin, pts, kern:M.kernClosed(p,c), karea:M.polyArea(M.kernClosed(p,c))}); }
for (const [P,EI,L,a] of [[25e3,590,0.25,0.025],[-25e3,590,0.25,0.025],[30e3,9500,0.25,0.025],[-40e3,590,0.25,0],[40e3,4113,1.5,0.075],[5e3,590,0.25,0.1]]) {
  const c=M.bcClosed(P,EI,L,a); o.bc.push({P,EI,L,a,Cmid:c.Cmid,Cend:c.Cend,Pcr:M.pcrClosed(EI,L,a)}); }
for (const phi of [0,0.6,Math.PI/2,2.4,3.9]) { const p=PP('tube8'); const t=M.tubeClosed(p,phi); o.tube.push({p,phi,sigma:t.sigma,tau:t.tau,tauV:t.tauV,tauT:t.tauT,I:t.I,J:t.J,Q:t.Q,A:t.A}); }
console.log(JSON.stringify(o));
""" % ((LAB.parent / "shared" / "test_harness.js").as_posix(), (LAB / "lab06_simulation.html").as_posix())
js = json.loads(subprocess.run(["node", "-e", JS], capture_output=True, text=True, check=True).stdout)


def py_section(p):
    s = p["shape"]
    if s == "rect":
        return PM.rect(p["h"], p["b"])
    if s == "angle":
        return PM.angle(p["bV"], p["bH"], p["t"], p["r"])
    if s == "tee":
        return PM.tee(p["B"], p["H"], p["tf"], p["tw"])
    if s == "channel":
        return PM.channel(p["B"], p["H"], p["tf"], p["tw"])
    if s == "zsec":
        return PM.zsec(p["B"], p["H"], p["tf"], p["tw"])
    return PM.tube(p["Do"], p["Di"])


for s in js["sec"]:
    p = s["p"]
    tag = f"{p['shape']}{' with fillet' if p.get('r') else ''} [{s['k']}]"
    sec = py_section(p)
    pr = PM.props(sec)
    C.rel(f"{tag}: A, JavaScript part formulas vs Python Green's theorem / quadrature", s["A"], pr["A"], 1e-11)
    C.abs(f"{tag}: centroid y (mm)", s["yc"] * 1e3, pr["yc"] * 1e3, 1e-9)
    C.abs(f"{tag}: centroid z (mm)", s["zc"] * 1e3, pr["zc"] * 1e3, 1e-9)
    C.rel(f"{tag}: I_z", s["Iz"], pr["Iz"], 1e-10)
    C.rel(f"{tag}: I_y", s["Iy"], pr["Iy"], 1e-10)
    C.abs(f"{tag}: I_yz / I_max", s["Iyz"] / s["Imax"], pr["Iyz"] / pr["Imax"], 1e-10)
    C.rel(f"{tag}: I_max, Mohr formula (JS) vs eigenvalue (numpy)", s["Imax"], pr["Imax"], 1e-10)
    C.rel(f"{tag}: I_min, Mohr formula (JS) vs eigenvalue (numpy)", s["Imin"], pr["Imin"], 1e-10)
    yP, zP = p["ey"], p["ez"]
    smax = max(abs(q["s"]) for q in s["pts"])
    worst = max(abs(q["s"] - PM.stress(pr, p["P"], yP, zP, q["y"] - pr["yc"], q["z"] - pr["zc"])) for q in s["pts"])
    C.abs(f"{tag}: corner stresses, Eq. 4.58 in principal axes (JS) vs general S⁻¹ form (Python), max |Δ|/σ_max", worst / smax, 0.0, 1e-10)
    if p["shape"] != "tube":
        K, area = PM.kern(pr, PM.to_centroidal(pr, sec["hull"]))
        C.rel(f"{tag}: kern area, antipoles (JS) vs half-plane intersection (scipy)", s["karea"], area, 1e-9)
        Kjs = np.array(s["kern"])
        dmin = max(min(np.hypot(*(Kjs[i] - k)) for i in range(len(Kjs))) for k in K)
        C.abs(f"{tag}: every kern vertex found by both methods (largest distance, mm)", dmin * 1e3, 0.0, 1e-9)
    else:
        ro, ri = p["Do"] / 2, p["Di"] / 2
        C.rel(f"{tag}: kern area vs π r_k², r_k = (c₂² + c₁²)/(4c₂) (360-gon)", s["karea"], math.pi * ((ro * ro + ri * ri) / (4 * ro)) ** 2, 2e-4)

for b in js["bc"]:
    tag = f"P = {b['P'] / 1e3:g} kN, EI = {b['EI']:g} N·m², L = {b['L']:g} m, a = {b['a'] * 1e3:g} mm"
    sol = PM.beam_column_bvp(b["P"], b["EI"], b["L"], b["a"], 1.0)
    C.rel(f"beam-column {tag}: C_mid, JS closed form vs scipy solve_bvp", b["Cmid"], sol["Cmid"], 1e-7)
    C.rel(f"beam-column {tag}: C at the ends of the free length", b["Cend"], sol["Cend"], 1e-7)
    C.rel(f"beam-column {tag}: buckling load with end blocks, JS bisection vs scipy brentq", b["Pcr"], PM.euler_load_blocks(b["EI"], b["L"], b["a"]), 1e-9)

for t in js["tube"]:
    p = t["p"]
    q = PM.tube_quadrature(p["Do"], p["Di"], t["phi"])
    loads = PM.tube_loads(p["F"], p["Lb"], p["aL"], p["Pax"])
    cf = PM.tube_point_stress(p["Do"], p["Di"], loads, t["phi"])
    tag = f"tube at φ = {math.degrees(t['phi']):.1f}°"
    if t["phi"] == 0:
        C.rel("tube: A, JS vs Python quadrature", t["A"], q["A"], 1e-10)
        C.rel("tube: I, JS vs Python quadrature", t["I"], q["I"], 1e-10)
        C.rel("tube: J, JS vs Python quadrature", t["J"], q["J"], 1e-10)
    else:
        C.rel(f"{tag}: Q of the wall from the top, JS closed form vs quadrature", t["Q"], q["Q"], 1e-9)
    if abs(t["sigma"]) > 1:
        C.rel(f"{tag}: σ_x, JS vs Python", t["sigma"], cf["sigma"], 1e-12)
    C.rel(f"{tag}: τ = Tc/J + VQ/(It), JS vs Python", t["tau"], cf["tauT"] + cf["tauV"], 1e-12)

# ---------------------------------------------------------------- closure: the analysis recovers the truth
T = json.loads((LAB / "src" / "truth.json").read_text())
R = json.loads((LAB / "src" / "results.json").read_text())
E = T["E"]
tb = T["bar"]
Iz_t, Iy_t = tb["b"] * tb["h"] ** 3 / 12, tb["h"] * tb["b"] ** 3 / 12
for cfg in ("e0", "e1", "e2"):
    r = R["A"][cfg]
    # truth effective eccentricity at the largest load (exact P without the load-cell gain: e_eff is a ratio)
    P = 30e3
    tr = tb["yP"][cfg] * PM.beam_column(P, E * Iz_t, tb["L"], tb["a"], 1.0)["Cmid"] * 1e3
    C.abs(f"closure Part A {cfg}: e_eff vs truth e·C_mid (mm), within 2u", r["e_eff_max"], tr, 2 * r["u_e_eff"])
    trz = tb["zP"][cfg] * PM.beam_column(P, E * Iy_t, tb["L"], tb["a"], 1.0)["Cmid"] * 1e3
    C.abs(f"closure Part A {cfg}: out-of-plane e_z vs truth (mm), within 0.02 mm", r["ez_eff"], trz, 0.02)
    C.rel(f"closure Part A {cfg}: σ₀ = Eε₀ vs P/A (truth E, truth A)", r["sig0"] * 68.9 / 68.46, P * T["load_gain"] / (tb["b"] * tb["h"]) / 1e6, 2 * r["u_sig0"] / r["sig0"])
rc = R["C"]
for i, P in enumerate(rc["P"]):
    Pt = P / T["load_gain"]
    tr = PM.beam_column(Pt, E * Iy_t, tb["L"], tb["a"], 1.0)
    if i == len(rc["P"]) - 1:
        C.abs("closure Part C at the largest load: C_mid vs truth, within 2u", rc["Cmid_m"][i], tr["Cmid"], 2 * rc["u_Cmid_m"])
        C.abs("closure Part C at the largest load: C near the block vs truth, within 2u", rc["Cend_m"][i],
              float(tr["M"](tb["x_end"])), 2 * rc["u_Cend_m"])
        C.abs("closure Part C at the largest load: w_mid vs truth (mm), within 2u", rc["w"][i], tb["zP"]["ez"] * tr["wmid"] * 1e3 * T["lvdt_gain"], 2 * rc["u_w_m"])
C.abs("closure Part C: EI from the LVDT fit vs truth E·hb³/12 (N·mm²), within 2u", rc["EI_fit"], E * 1e-6 * Iy_t * 1e12, 2 * rc["u_EI_fit"])
rb = R["B"]
ta = T["angle"]
truth_sig = [s / 1e6 for s in T["partB"]["run"][-2]["sig"]]       # 30 kN step
for i, g in enumerate(rb["gages"]):
    meas_true_scale = rb["meas"][i] * (68.9 / 68.46) / (T["gf_common"] + 1)  # remove the reference-E and common gage-factor bias
    C.abs(f"closure Part B {g}: measured σ (bias removed) vs truth (MPa), within 2u", meas_true_scale, truth_sig[i], 2 * rb["u_meas"][i])
# D1 cross-language: the simulation's design preset vs the analysis table
dj = subprocess.run(["node", "-e", r"""
const {loadModel}=require('%s'); const M=loadModel('%s'); const p=M.presetParams('design'), c=M.sectionClosed(p);
console.log(Math.max(...c.hull.map(([z,y])=>M.stressClosed(c,p.P,p.ey,p.ez,y-c.yc,z-c.zc))));
""" % ((LAB.parent / "shared" / "test_harness.js").as_posix(), (LAB / "lab06_simulation.html").as_posix())], capture_output=True, text=True, check=True).stdout
best = next(d for d in R["D1"]["table"] if d["name"] == R["D1"]["best"])
C.rel("D1: largest stress of the reference design, simulation preset (JS) vs analysis (Python)", float(dj) / 1e6, best["s458"], 1e-9)
C.true(f"D1: P/A alone picks {R['D1']['naive_best']}, which is overstressed", next(d for d in R["D1"]["table"] if d["name"] == R["D1"]["naive_best"])["s458"] > R["D1"]["sa"])

sys.exit(C.write(LAB / "tests" / "results_python.md"))

"""Lab 7 independent verification (Python / numpy / scipy).

1. Cross-language: the page's closed forms (App. F superposition, JavaScript) vs the same closed forms typed again in
   Python (src/lab07_model.py), for every preset and for variants that exercise overhangs, couples, springs and settlement.
2. Cross-method: the page's closed forms and its finite-element port of beam_deflection.cpp vs direct double integration
   of M/EI on a fine grid with the constants and redundants found numerically from the boundary conditions.
3. The page's elastica (Carlson's integrals, its own bisection, RK4 shooting) vs scipy's elliptic integrals with brentq
   and scipy's collocation BVP solver, with and without self-weight; the page's alpha5 vs brentq; Appendix E of the
   handout re-computed.
4. Closure: lab07_analysis.py on sample_data.csv recovers the generating (truth) values within its stated uncertainty.
5. D1: the page's numbers for the reference design vs the analysis table.
"""
import json
import math
import re
import subprocess
import sys
from pathlib import Path

import numpy as np

LAB = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LAB / "src"))
sys.path.insert(0, str(LAB.parent / "shared"))
from checklib import Checks  # noqa: E402
import lab07_model as LM  # noqa: E402

C = Checks("Lab 7 — independent checks (Python/scipy) and data-pipeline closure")
JS = r"""
const {loadModel}=require('%s'); const M=loadModel('%s'); const o={beams:[], ela:[], shape:[]};
const PP=(k,ov={})=>Object.assign({}, M.PRESETS[k], ov);
const cases=[['partA',{}],['partAboth',{}],['partB1',{}],['partB1',{rigid:true}],['partB2',{}],['partB2',{rigid:true}],['partB3',{}],['partB3',{rigid:true}],
  ['design',{}],['design',{L:3.05,aov:0.95}],['F1',{}],['F2',{}],['F3',{}],['F4',{}],['F5',{}],['F6',{}],['F7',{}],['fixedw',{}],
  ['fixedw',{rigid:false,k:2e5,P1:4000,a1:1.1,w:1500}],['partB2',{w:300,P2:20,a2:0.6,C0:3}],['F5',{aov:0.8,P2:2000,a2:3.6,C0:-1500,w:800}],
  ['partB1',{w:120,C0:-2,P2:15,a2:0.2}]];
for (const [k,ov] of cases) {
  const p=PP(k,ov); if (p.mode!=='beam') continue;
  const c=M.closedForm(p), f=M.feSolve(p,160), Lt=c.Lt, xs=Array.from({length:41},(_,i)=>Lt*i/40);
  o.beams.push({k, ov, p, EI:c.EI, Lt, Ps:M.pointLoads(p), xs, y:xs.map(c.y), t:xs.map(c.t), R:c.R, yfe:xs.map(f.y), tfe:xs.map(f.t),
    Rfe:f.reactions, Mst:xs.map(x=>M.momentStatics(p,c.R,x))});
}
for (const a of [0.05,0.3,1,2,3.641,5]) { const c=M.elasticaClosed(a), s0=M.elasticaShoot(a,0,400), sw=M.elasticaShoot(a,0.1154,400);
  o.ela.push({a, th0:c.th0, dv:c.dv, xt:c.xt, sdv:s0.dv, sxt:s0.xt, sth:s0.th0, wdv:sw.dv, wxt:sw.xt, wth:sw.th0}); }
for (const a of [1,3.641]) o.shape.push({a, pts:M.elasticaClosed(a).shape(8)});
o.a5=M.alpha5(); o.Eal=M.MATERIALS.al.E;
const pC=PP('partC'), sp=M.stripProps(pC); o.strip={EI:sp.EI, w:sp.w, alpha:sp.alpha, beta:sp.beta};
console.log(JSON.stringify(o));
""" % ((LAB.parent / "shared" / "test_harness.js").as_posix(), (LAB / "lab07_simulation.html").as_posix())
js = json.loads(subprocess.run(["node", "-e", JS], capture_output=True, text=True, check=True).stdout)


def py_beam(b):
    p = b["p"]
    d = dict(family=p["family"], L=p["L"], EI=b["EI"], P=[tuple(q) for q in b["Ps"]], w=p["w"], C0=p["C0"])
    if p["family"] == "ss":
        d["a_over"] = p["aov"]
    else:
        d["k"] = math.inf if p["rigid"] else p["k"]
        d["s"] = p["s"]
    return d


for b in js["beams"]:
    tag = b["k"] + (" " + ", ".join(f"{k}={v}" for k, v in b["ov"].items()) if b["ov"] else "")
    bm = py_beam(b)
    xs = np.array(b["xs"])
    cf = LM.closed_form(bm, xs)
    ib = LM.integrate_beam(bm)
    yref = max(np.max(np.abs(cf["y"])), 1e-300)
    tref = max(np.max(np.abs(cf["t"])), 1e-300)
    tol_x = 1e-12 if bm["family"] in ("ss", "cant") else 1e-9     # redundants: round-off of the compatibility solve
    C.abs(f"[{tag}] closed form y(x), JS vs Python, max |Δ|/|y|max", float(np.max(np.abs(np.array(b["y"]) - cf["y"]))) / yref, 0.0, tol_x)
    C.abs(f"[{tag}] closed form slope, JS vs Python, max |Δ|/|θ|max", float(np.max(np.abs(np.array(b["t"]) - cf["t"]))) / tref, 0.0, tol_x)
    yi = np.interp(xs, ib["x"], ib["y"])
    ti = np.interp(xs, ib["x"], ib["t"])
    C.abs(f"[{tag}] closed form y(x) (JS) vs double integration of M/EI (Python), max |Δ|/|y|max", float(np.max(np.abs(np.array(b["y"]) - yi))) / yref, 0.0, 1e-7)
    C.abs(f"[{tag}] finite elements y(x) (JS port of the C++) vs double integration (Python), max |Δ|/|y|max", float(np.max(np.abs(np.array(b["yfe"]) - yi))) / yref, 0.0, 1e-6)
    C.abs(f"[{tag}] finite elements slope vs double integration, max |Δ|/|θ|max", float(np.max(np.abs(np.array(b["tfe"]) - ti))) / tref, 0.0, 1e-5)
    Rjs, Rpy = b["R"], cf["R"]
    scale = max(abs(v) for v in Rpy.values() if isinstance(v, float)) or 1.0
    for key in ("RA", "RB", "MA", "MB"):
        if key in Rpy:
            C.abs(f"[{tag}] reaction {key}, JS vs Python closed form (relative to the largest reaction)", (Rjs[key] - Rpy[key]) / scale, 0.0, tol_x)
    # FE reactions vs the integrated solution's reactions
    Ri = ib["R"]
    fe = b["Rfe"]
    if bm["family"] == "ss":
        pairs = [("RA", fe[0]["F_up"]), ("RB", fe[1]["F_up"])]
    elif bm["family"] == "cant":
        pairs = [("RA", fe[0]["F_up"]), ("MA", fe[0]["M_ccw"])]
    elif bm["family"] == "propped":
        pairs = [("RA", fe[0]["F_up"]), ("MA", fe[0]["M_ccw"]), ("RB", fe[1]["F_up"])]
    else:
        pairs = [("RA", fe[0]["F_up"]), ("MA", fe[0]["M_ccw"]), ("RB", fe[1]["F_up"]), ("MB", fe[1]["M_ccw"])]
    sc = max(abs(Ri[k_]) for k_, _ in pairs) or 1.0
    worst = max(abs(v - Ri[k_]) for k_, v in pairs) / sc
    C.abs(f"[{tag}] finite-element reactions (Ku − F) vs double-integration reactions, worst relative to the largest", worst, 0.0, 1e-6)
    Mi = np.interp(xs, ib["x"], ib["M"])
    msc = max(np.max(np.abs(Mi)), 1e-300)
    C.abs(f"[{tag}] M(x) from statics with the JS reactions vs Python, max |Δ|/|M|max", float(np.max(np.abs(np.array(b["Mst"]) - Mi))) / msc, 0.0, 1e-6)

# ---------------------------------------------------------------- elastica
for e in js["ela"]:
    a = e["a"]
    th0, dv, xt = LM.elastica_closed(a)
    C.rel(f"elastica α = {a}: tip angle, Carlson R_F (JS) vs scipy ellipkinc + brentq", e["th0"], th0, 1e-10)
    C.rel(f"elastica α = {a}: δ_v/L, Carlson R_D (JS) vs scipy ellipeinc", e["dv"], dv, 1e-10)
    C.rel(f"elastica α = {a}: x_tip/L, JS vs scipy", e["xt"], xt, 1e-10)
    bth, bdv, bxt, _ = LM.elastica_bvp(a, 0.0)
    C.rel(f"elastica α = {a}: δ_v/L, RK4 shooting N = 400 (JS) vs collocation BVP (scipy)", e["sdv"], bdv, 1e-8)
    C.rel(f"elastica α = {a}: x_tip/L, RK4 shooting vs BVP", e["sxt"], bxt, 1e-8)
    wth, wdv, wxt, _ = LM.elastica_bvp(a, 0.1154)
    C.rel(f"elastica α = {a} with self-weight β = 0.1154: δ_v/L, RK4 shooting vs BVP", e["wdv"], wdv, 1e-7)
    C.rel(f"elastica α = {a} with self-weight: tip angle, RK4 shooting vs BVP", e["wth"], wth, 1e-7)
for s in js["shape"]:
    a = s["a"]
    sol = LM.elastica_bvp(a, 0.0)[3]
    worst = 0.0
    for pt in s["pts"]:
        _, _, xb, yb = sol.sol(pt["s"])
        worst = max(worst, math.hypot(pt["x"] - xb, pt["y"] - yb))
    C.abs(f"elastica α = {a}: elastic curve from the elliptic parameterization (JS) vs the BVP at the same arc length, max distance / L", worst, 0.0, 1e-7)
C.rel("α at which linear theory overstates δ_v by 5 %: JS bisection vs scipy brentq", js["a5"], LM.elastica_p5(), 1e-9)

# Appendix E of the handout, re-computed
H = (LAB / "src" / "lab07_handout.md").read_text(encoding="utf-8")
appE = H[H.index("## Appendix E"):]
rows = [ln for ln in appE.splitlines() if re.match(r"\| \d", ln)]
worst = 0.0
for ln in rows:
    c = [x.strip() for x in ln.strip("|").split("|")]
    a = float(c[0])
    th0, dv, xt = LM.elastica_closed(a)
    worst = max(worst, abs(float(c[1]) - dv), abs(float(c[2]) - xt), abs(float(c[3]) - math.degrees(th0)) / 100, abs(float(c[4]) - a / 3))
C.abs(f"handout Appendix E, {len(rows)} rows: every printed value vs scipy (largest error in the last printed digit)", worst, 0.0, 5.01e-5)

# ---------------------------------------------------------------- closure: the analysis recovers the truth
T = json.loads((LAB / "src" / "truth.json").read_text())
R = json.loads((LAB / "src" / "results.json").read_text())
EIt = T["EI_bar"]
C.abs("closure Part A: E from six compliances vs truth 205 GPa, within 2u", R["A"]["E"], T["bar"]["E"] / 1e9, 2 * R["A"]["uE"])
C.abs("closure Part A: EI vs truth (N·m²), within 2u", R["A"]["EI"], EIt, 2 * R["A"]["uEI"])
C.abs("closure Part A: reciprocity c13 − c31 (µm/N), within its limit", (R["A"]["c13"] - R["A"]["c31"]) * 1e6, 0.0, R["A"]["recip_lim"] * 1e6)
C.abs("closure Part B1: EI from two indicators vs truth (N·m²), within 2u", R["B1"]["EI"], EIt, 2 * R["B1"]["uEI"])
C.abs("closure Part B1: clamp stiffness k vs truth 4500 N·m/rad, within 2u", R["B1"]["k"], T["B"]["k"], 2 * R["B1"]["uk"])
tb = T["B"]
cfB2 = LM.closed_form(dict(family="propped", L=tb["L"], EI=EIt, P=[(1.0, tb["xP_mid"])], k=tb["k"]), np.array([0.0]))
C.abs("closure Part B2: R_B/P (load-cell gain included) vs truth model with the spring clamp, within 2u", R["B2"]["r"], cfB2["R"]["RB"] * tb["lc_gain"], 2 * R["B2"]["ur"])
C.true("closure Part B2: rigid-clamp 5/16 is rejected by the data (|r − 5/16| > 2u)", abs(R["B2"]["r"] - 5 / 16) > 2 * R["B2"]["ur"])
Pset = 3.0 * T["g"] * (1 + T["mass_err"] * 0.3)
r0 = LM.closed_form(dict(family="propped", L=tb["L"], EI=EIt, P=[(Pset, tb["xP_mid"])], k=tb["k"], s=0.0), np.array([0.0]))["R"]["RB"]
r1 = LM.closed_form(dict(family="propped", L=tb["L"], EI=EIt, P=[(Pset, tb["xP_mid"])], k=tb["k"], s=-tb["settle"]), np.array([0.0]))["R"]["RB"]
C.abs("closure Part B3: ΔR_B (N) vs truth (spring clamp, 0.502 mm, load-cell gain), within 2u", R["B3"]["dR"], (r1 - r0) * tb["lc_gain"], 2 * R["B3"]["u_dR"])
tc = T["C"]
EIs = tc["E"] * tc["b"] * tc["t"] ** 3 / 12
C.abs("closure Part C: strip EI from the large-deflection fit vs truth (N·m²), within 2u", R["C"]["EI_fit"], EIs, 2 * R["C"]["uEI_fit"])
C.abs("closure Part C: strip E (GPa) vs truth 203, within 2u", R["C"]["E_fit"], tc["E"] / 1e9, 2 * R["C"]["uE_fit"])
C.rel("closure Part C: free length from the zero-load grid reading vs truth (m)", R["C"]["L"], tc["L"], 5e-3)
C.true(f"closure Part C: χ² of the fit consistent with the reading noise (χ² = {R['C']['chi2']:.1f} for {R['C']['dof']} degrees of freedom)",
       R["C"]["chi2"] < R["C"]["dof"] + 3 * math.sqrt(2 * R["C"]["dof"]))
C.rel("analysis α5 (scipy) vs the page's alpha5 (JS)", R["C"]["a5"], js["a5"], 1e-9)
C.rel("simulation Part C preset: β = wL³/EI with E = 203 GPa vs the analysis β", js["strip"]["beta"], R["C"]["beta"], 0.01)

# ---------------------------------------------------------------- D1: the page vs the analysis table
D = R["D1"]
best = next(t for t in D["table"] if t["name"] == D["best"])
Ls0 = best["feas"][0]
ev = next(e for e in best["evals"] if abs(e["Ls"] - Ls0) < 1e-9)
db = next(b for b in js["beams"] if b["k"] == "design" and b["ov"])
xs = np.array(db["xs"])
fE = js["Eal"] / (D["E"] * 1e9)                       # the page uses E = 68.9 GPa; the analysis uses the Lab 2 value
span = xs <= Ls0 + 1e-12
C.rel(f"D1 reference design ({D['best']}, L_s = {Ls0} m): largest |y| on the span, page vs analysis (40 points vs 8000)",
      float(np.max(np.abs(np.array(db["y"])[span]))) * 1e3 * fE, ev["ys"], 2e-3, "page deflections scaled by 68.9/68.46")
C.rel("D1 reference design: tip deflection, page vs analysis", abs(db["y"][-1]) * 1e3 * fE, ev["yt"], 1e-9, "scaled by 68.9/68.46")
C.rel("D1 reference design: roller reaction, page vs analysis", db["R"]["RB"], ev["RB"], 1e-12)
C.true(f"D1: the lightest feasible section is {D['best']}; without an overhang it is {D['noover']}", D["best"] != D["noover"])

sys.exit(C.write(LAB / "tests" / "results_python.md"))

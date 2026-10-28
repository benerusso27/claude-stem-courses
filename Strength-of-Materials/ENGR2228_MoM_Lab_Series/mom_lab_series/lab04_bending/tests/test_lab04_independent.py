"""Lab 4 independent verification (Python / numpy / scipy).

1. Cross-language: the page's beam statics and section formulas vs src/lab04_model.py (typed independently).
2. Cross-method: the page's strip summation vs adaptive scipy.quad over the depth with brentq for the neutral axis.
3. Closure: lab04_analysis.py on sample_data.csv recovers the generating values within its stated uncertainty.
"""
import json
import math
import subprocess
import sys
import warnings
from pathlib import Path

LAB = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LAB / "src"))
sys.path.insert(0, str(LAB.parent / "shared"))
from checklib import Checks  # noqa: E402
import lab04_model as PM  # noqa: E402

warnings.filterwarnings("ignore", message="The occurrence of roundoff")
C = Checks("Lab 4 — independent checks (Python/scipy) and data-pipeline closure")
JS = r"""
const {loadModel}=require('%s'); const M=loadModel('%s'); const o={mats:M.MATERIALS, beams:[], secs:[], props:[]};
const P=M.PRESETS;
{ const p=Object.assign({},P.fourpt); const c=M.beamClosed(p); o.beams.push({kind:'fourpt',P:p.P,L:p.L,a:p.a,xs:[0.05,0.2,0.3,0.45,0.55].map(x=>({x,V:c.V(x),M:c.M(x)}))}); }
{ const p=Object.assign({},P.cantilever); const c=M.beamClosed(p); o.beams.push({kind:'cant',w0:p.w0,L:p.L,xs:[0.1,0.5,1.0,1.5,1.9].map(x=>({x,V:c.V(x),M:c.M(x)}))}); }
for (const [name,lawov] of [['al',null],['al',{law:'epp'}]]) for (const k of [0.05,0.2,0.4]) { const p=Object.assign({},P.plastic); const s=M.stripSolve(p,k,2000,lawov); o.secs.push({shape:'rect',mat:name,law:lawov?'epp':'own',k,M:s.M,yNA:s.yNA,b:p.b,h:p.h}); }
for (const k of [0.02,0.05]) { const p=Object.assign({},P.composite); const s=M.stripSolve(p,k,2000,{law:'epp',sY:1e30}); const s2=M.stripSolve(p,k*20,2000,null); o.secs.push({shape:'comp',k,M:s.M,yNA:s.yNA,k2:k*20,M2:s2.M,yNA2:s2.yNA,b:p.b,h:p.h,ts:p.ts}); }
{ const p=Object.assign({},P.ibeam,{mat:'steel'}); for (const k of [0.01,0.03]) { const s=M.stripSolve(p,k,2000,null); o.secs.push({shape:'ibeam',k,M:s.M,yNA:s.yNA,b:p.b,h:p.h,tf:p.tf,tw:p.tw}); } }
{ const p=Object.assign({},P.composite); const t=M.transformed(p,1); o.props.push({kind:'comp',ybar:t.ybar,I:t.I,b:p.b,h:p.h,ts:p.ts}); }
{ const p=Object.assign({},P.ibeam); const t=M.transformed(p,1); const z=M.plasticModulus(p); o.props.push({kind:'ibeam',I:t.I,Z:z.Z,b:p.b,h:p.h,tf:p.tf,tw:p.tw}); }
console.log(JSON.stringify(o));
""" % ((LAB.parent / "shared" / "test_harness.js").as_posix(), (LAB / "lab04_simulation.html").as_posix())
js = json.loads(subprocess.run(["node", "-e", JS], capture_output=True, text=True, check=True).stdout)
mats = js["mats"]

b0 = js["beams"][0]
for pt in b0["xs"]:
    V, M = PM.four_point(b0["P"], b0["L"], b0["a"], pt["x"])
    C.rel(f"4-point bending at x = {pt['x']} m: M, JavaScript vs Python (direct formula)", pt["M"], M, 1e-12)
    C.abs(f"4-point bending at x = {pt['x']} m: V/P", pt["V"] / b0["P"], V / b0["P"], 1e-12)
b1 = js["beams"][1]
for pt in b1["xs"]:
    V, M = PM.cantilever_triangle(b1["w0"], b1["L"], pt["x"])
    C.rel(f"cantilever, triangular load, x = {pt['x']} m: M, JavaScript vs scipy.quad (right free body)", pt["M"], M, 1e-11)
    C.rel(f"cantilever, triangular load, x = {pt['x']} m: V", pt["V"], V, 1e-11)
for s in js["secs"]:
    if s["shape"] == "rect":
        m = dict(mats[s["mat"]])
        if s["law"] == "epp":
            m["law"] = "epp"
        M, y = PM.section_moment([(0.0, s["h"], s["b"], "x")], {"x": m}, s["k"])
        C.rel(f"rectangle ({s['law']} law), κ = {s['k']}: strip summation (N = 2000) vs scipy.quad + brentq", s["M"], M, 2e-6, "midpoint rule O(N⁻²)")
        if s["law"] == "epp":
            C.rel(f"    … vs Python §4.6 formula", s["M"], PM.epp_rect_M(s["b"], s["h"], m["E"], m["sY"], s["k"]), 2e-6)
    elif s["shape"] == "comp":
        lay = [(0.0, s["ts"], s["b"], "steel"), (s["ts"], s["ts"] + s["h"], s["b"], "al")]
        el = {"steel": dict(law="epp", E=mats["steel"]["E"], sY=1e30), "al": dict(law="epp", E=mats["al"]["E"], sY=1e30)}
        M, y = PM.section_moment(lay, el, s["k"])
        C.rel(f"composite (elastic), κ = {s['k']}: M, strip vs quad", s["M"], M, 2e-6)
        C.rel(f"composite (elastic), κ = {s['k']}: neutral axis, strip vs brentq", s["yNA"], y, 1e-9)
        own = {"steel": mats["steel"], "al": mats["al"]}
        M2, y2 = PM.section_moment(lay, own, s["k2"])
        C.rel(f"composite (own curves, both yielding), κ = {s['k2']}: M, strip vs quad", s["M2"], M2, 2e-5)
        C.rel(f"composite (own curves), κ = {s['k2']}: neutral axis", s["yNA2"], y2, 2e-5)
    else:
        lay = [(0.0, s["tf"], s["b"], "s"), (s["tf"], s["h"] - s["tf"], s["tw"], "s"), (s["h"] - s["tf"], s["h"], s["b"], "s")]
        M, y = PM.section_moment(lay, {"s": mats["steel"]}, s["k"])
        C.rel(f"I-section (1018 curve), κ = {s['k']}: strip vs quad", s["M"], M, 2e-5)
for pr in js["props"]:
    if pr["kind"] == "comp":
        cp = PM.composite_props(pr["b"], pr["h"], pr["ts"], mats["al"]["E"], mats["steel"]["E"])
        C.rel("composite: transformed centroid, JavaScript vs Python", pr["ybar"], cp["ybar"], 1e-12)
        C.rel("composite: transformed I, JavaScript vs Python", pr["I"], cp["I"], 1e-12)
    else:
        ip = PM.ibeam_props(pr["b"], pr["h"], pr["tf"], pr["tw"])
        C.rel("I-section: I, JavaScript vs Python", pr["I"], ip["I"], 1e-12)
        C.rel("I-section: Z, JavaScript (equal-area routine) vs Python (formula)", pr["Z"], ip["Z"], 1e-12)

# ---------------- closure test of the data pipeline ----------------
subprocess.run([sys.executable, str(LAB / "src" / "lab04_analysis.py")], check=True, capture_output=True)
r = json.loads((LAB / "src" / "results.json").read_text())
t = json.loads((LAB / "src" / "truth.json").read_text())


def within(name, val, ref, U, note=""):
    C.true(f"closure: {name} recovered within U = {U:.3g} (value {val:.5g}, truth {ref:.5g})" + (f" — {note}" if note else ""), abs(val - ref) <= U)


gf = 1 + t["gf_error"]
within("E of 6061-T6 from M–κ (GPa)", r["A"]["E"], t["al"]["E"] / 1e9 / gf, 2 * r["A"]["uE"], "truth divided by the gage-factor error")
within("neutral axis height, Part A (mm)", r["A"]["yNA"], t["h"] * 1e3 / 2, 2 * r["A"]["u_yNA"] + 0.02)
within("Poisson's ratio from anticlastic strain", r["A"]["nu"], t["nu_al"], 2 * r["A"]["unu"])
within("shear V per unit load from the moment gradient", r["A"]["V_per_N"], 0.5, 2 * r["A"]["uV_per_N"])
within("composite neutral axis (mm)", r["B"]["yNA"], t["composite"]["ybar"] * 1e3, 2 * r["B"]["u_yNA"] + 0.05)
within("composite EI (N·m²)", r["B"]["EI_meas"], t["al"]["E"] * t["composite"]["I"] / gf, 2 * r["B"]["uEI_pred"])
within("Part C maximum curvature (1/m)", r["C"]["kmax"], t["partC"]["kappa_max"] * gf, 0.01 * t["partC"]["kappa_max"])
within("Part C residual curvature (1/m)", r["C"]["k_res_meas"], t["partC"]["kappa_residual"] * gf, 2 * r["C"]["u_k_res_pred"] + 0.001)
within("straightedge gap, κ_p(x) integrated from the measured M–κ curve (mm)", r["C"]["gap_data"], t["partC"]["straightedge_gap"] * 1e3, 2 * r["C"]["u_gap_meas"])
within("straightedge gap in the sample measurements (mm)", r["C"]["gap_meas"], t["partC"]["straightedge_gap"] * 1e3, 0.026, "rounded to the 0.05 mm feeler step")
sys.exit(C.write(LAB / "tests" / "results_python.md"))

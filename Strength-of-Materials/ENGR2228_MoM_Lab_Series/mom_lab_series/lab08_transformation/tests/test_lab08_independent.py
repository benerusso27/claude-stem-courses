"""Lab 8 independent verification (Python / numpy / scipy).

1. Cross-language, cross-method: the page's transformation formulas, Mohr's circle, trigonometric cubic and Jacobi
   rotations vs numpy (tensor rotation R S R^T, eigh) for random states.
2. The page's rosette reductions (rectangular, delta, any three angles, transverse sensitivity, turned rosette) vs
   least squares on Eq. 7.60 with numpy.
3. The page's tube stresses vs the Python model with Q from scipy dblquad and the thick cylinder from scipy solve_bvp.
4. Closure: lab08_analysis.py on sample_data.csv recovers the generating (truth) values within its stated uncertainty.
5. D1: the page's preset vs the analysis table.
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
import lab08_model as LM  # noqa: E402

C = Checks("Lab 8 — independent checks (Python/scipy) and data-pipeline closure")
D = math.pi / 180
rng = np.random.default_rng(88)
states = [list(map(float, rng.uniform(-150e6, 150e6, 6))) for _ in range(10)]
angles = [float(a) for a in rng.uniform(-math.pi / 2, math.pi / 2, 10)]
strains = [list(map(float, rng.uniform(-1.5e-3, 1.5e-3, 3))) for _ in range(8)]
JS = r"""
const {loadModel}=require('%s'); const M=loadModel('%s'); const IN=%s; const o={st:[], ro:[], tube:[]}, P=M.PRESETS, D=M.D;
for (const [i,v] of IN.states.entries()) { const th=IN.angles[i], r=M.transform(v[0],v[1],v[2],th), m=M.mohr(v[0],v[1],v[2]);
  const S3=[[v[0],v[2],v[5]],[v[2],v[1],v[4]],[v[5],v[4],v[3]]];
  o.st.push({v, th, r, m, cubic:M.eig3closed(S3), jac:M.jacobi(S3).vals, p2:M.principal3({sx:v[0],sy:v[1],txy:v[2],sz:v[3]})}); }
for (const e of IN.strains) {
  const rect=M.ANGLES.rect.map(t=>M.strainAt(e[0],e[1],e[2],t)), delta=M.ANGLES.delta.map(t=>M.strainAt(e[0],e[1],e[2],t));
  const cust=[0.2,1.1,2.4], rc=cust.map(t=>M.strainAt(e[0],e[1],e[2],t));
  const kt=M.ktForward(e[0],e[1],e[2],M.ANGLES.rect,3*D,0.02);
  const red=M.rosetteReduce(Object.assign({},P.rosHB,{ros:'rect',ea:kt[0],eb:kt[1],ec:kt[2],Kt:0.02,ktcorr:true,beta:3*D}));
  o.ro.push({e, rect, delta, cust, rc, kt, rcf:M.rosClosed('rect',...rect), dcf:M.rosClosed('delta',...delta), cnum:M.rosNumeric(cust,rc), red:red.cf}); }
for (const [k,phi] of [['partB',0],['partBK',90*D],['partB',-90*D],['partB',37*D],['partC',0],['partCc',0],['partCcK',90*D],['design',0],['thick',0]]) {
  const p=P[k], s=M.tubeState(p,phi), fd=M.lameFD(p.p||1e6,p.Di/2,p.Do/2,M.MATERIALS[p.mat].E,M.MATERIALS[p.mat].nu,1024);
  o.tube.push({k, phi, p, s:{sx:s.sx,sy:s.sy,txy:s.txy,sz:s.sz,Q:s.Q}, fd:{st:fd.st,sx:fd.sx,ist:fd.inner.st,isr:fd.inner.sr}, p3:M.principal3(s)}); }
console.log(JSON.stringify(o));
""" % ((LAB.parent / "shared" / "test_harness.js").as_posix(), (LAB / "lab08_simulation.html").as_posix(),
       json.dumps(dict(states=states, angles=angles, strains=strains)))
js = json.loads(subprocess.run(["node", "-e", JS], capture_output=True, text=True, check=True).stdout)

# ---------------------------------------------------------------- 1. stress transformation
for i, s in enumerate(js["st"]):
    sx, sy, t, sz, tyz, tzx = s["v"]
    sc = max(map(abs, s["v"]))
    a = LM.rotate2(sx, sy, t, s["th"])
    C.abs(f"state {i + 1}: Eqs. 7.5–7.7 (JS) vs R·S·Rᵀ (numpy), max |Δ|/scale", max(abs(s["r"]["sx1"] - a[0]), abs(s["r"]["sy1"] - a[1]), abs(s["r"]["t1"] - a[2])) / sc, 0.0, 1e-14)
    p1, p2, thp = LM.principal2(sx, sy, t)
    C.abs(f"state {i + 1}: Mohr σmax, σmin (JS) vs numpy eigh, max |Δ|/scale", max(abs(s["m"]["s1"] - p1), abs(s["m"]["s2"] - p2)) / sc, 0.0, 1e-14)
    C.abs(f"state {i + 1}: θp (JS, Eq. 7.12 with atan2) vs eigenvector of the larger eigenvalue (rad)", abs(math.sin(s["m"]["thp"] - thp)), 0.0, 1e-12)
    S3 = [[sx, t, tzx], [t, sy, tyz], [tzx, tyz, sz]]
    ev = LM.principal3(S3)
    C.abs(f"state {i + 1}: 3-D principal stresses, trigonometric cubic (JS) vs numpy eigvalsh, max |Δ|/scale", max(abs(x - y) for x, y in zip(s["cubic"], ev)) / sc, 0.0, 1e-12)
    C.abs(f"state {i + 1}: 3-D principal stresses, Jacobi (JS) vs numpy eigvalsh", max(abs(x - y) for x, y in zip(s["jac"], ev)) / sc, 0.0, 1e-12)
    ev2 = LM.principal3([[sx, t, 0], [t, sy, 0], [0, 0, sz]])
    C.abs(f"state {i + 1}: z principal: Mohr + σz (JS principal3) vs numpy", max(abs(x - y) for x, y in zip(s["p2"], ev2)) / sc, 0.0, 1e-13)

# ---------------------------------------------------------------- 2. rosettes
for i, r in enumerate(js["ro"]):
    e = r["e"]
    ls = LM.rosette_solve(LM.RECT, r["rect"])
    C.abs(f"strain {i + 1}: rectangular rosette Eq. 7.43 (JS) vs least squares (numpy), max |Δ| (µε)", max(abs(r["rcf"][k] - v) for k, v in zip(("ex", "ey", "g"), ls)) * 1e6, 0.0, 1e-9)
    ld = LM.rosette_solve(LM.DELTA, r["delta"])
    C.abs(f"strain {i + 1}: delta rosette formulas (JS) vs least squares, max |Δ| (µε)", max(abs(r["dcf"][k] - v) for k, v in zip(("ex", "ey", "g"), ld)) * 1e6, 0.0, 1e-9)
    lc = LM.rosette_solve([0.2, 1.1, 2.4], r["rc"])
    C.abs(f"strain {i + 1}: gages at 11.5°, 63.0°, 137.5°: Gaussian elimination (JS) vs least squares, max |Δ| (µε)", max(abs(r["cnum"][k] - v) for k, v in zip(("ex", "ey", "g"), lc)) * 1e6, 0.0, 1e-9)
    pyk = LM.gage_readings(*e, LM.RECT, 3 * D, 0.02)
    C.abs(f"strain {i + 1}: readings of a rosette turned 3° with K_t = 2 %, JS vs Python forward model (µε)", max(abs(a - b) for a, b in zip(r["kt"], pyk)) * 1e6, 0.0, 1e-9)
    kx, ky, kg = LM.kt_correct_numeric(pyk, LM.RECT, 0.02)
    bx, by, bg = LM.derotate(kx, ky, kg, 3 * D)
    C.abs(f"strain {i + 1}: page's K_t correction and turn-back (closed form) vs Python least squares and tensor rotation (µε)", max(abs(r["red"]["ex"] - bx), abs(r["red"]["ey"] - by), abs(r["red"]["g"] - bg)) * 1e6, 0.0, 1e-9)
    C.abs(f"strain {i + 1}: ... recovers the true strains (µε)", max(abs(bx - e[0]), abs(by - e[1]), abs(bg - e[2])) * 1e6, 0.0, 1e-9)

# ---------------------------------------------------------------- 3. tube
for tb in js["tube"]:
    p, phi = tb["p"], tb["phi"]
    tag = f"[{tb['k']}, φ = {phi / D:.0f}°{', inner surface' if p['surf'] == 'inner' else ''}]"
    py = LM.tube_state(p["Do"], p["Di"], p["F"], p["aL"], p["Lb"], p["p"], phi, wall=p["wall"], Q=LM.Q_quad(p["Do"] / 2, p["Di"] / 2, phi))
    if p["surf"] == "outer":
        sc = max(abs(py["sx"]), abs(py["sy"]), abs(py["txy"]), 1.0)
        C.abs(f"{tag} σx, σθ, τxy: JS closed forms vs Python with Q by scipy dblquad, max |Δ|/scale", max(abs(tb["s"]["sx"] - py["sx"]), abs(tb["s"]["sy"] - py["sy"]), abs(tb["s"]["txy"] - py["txy"])) / sc, 0.0, 1e-10)
    if abs(math.sin(phi)) > 1e-9:
        C.rel(f"{tag} Q of the wall from the top (JS closed form vs dblquad)", tb["s"]["Q"], LM.Q_quad(p["Do"] / 2, p["Di"] / 2, phi), 1e-10)
    if p["p"] > 0:
        sr, st, sx, _ = LM.lame_bvp(p["p"], p["Di"] / 2, p["Do"] / 2, LM.MATERIALS[p["mat"]]["E"], LM.MATERIALS[p["mat"]]["nu"])
        C.rel(f"{tag} hoop stress at r_o: JS finite differences (1024) vs scipy solve_bvp", tb["fd"]["st"], st, 1e-5)
        C.rel(f"{tag} axial stress: JS finite differences vs scipy solve_bvp", tb["fd"]["sx"], sx, 1e-5)
        C.rel(f"{tag} hoop stress at r_o: JS Lamé closed form vs scipy solve_bvp", LM.lame_closed(p["p"], p["Di"] / 2, p["Do"] / 2, p["Do"] / 2)[1], st, 1e-8)
    if p["surf"] == "inner":
        r_, A_ = p["Di"] / 2, p["p"] * (p["Di"] / 2) ** 2 / ((p["Do"] / 2) ** 2 - (p["Di"] / 2) ** 2)
        I_ = math.pi * ((p["Do"] / 2) ** 4 - r_ ** 4) / 4
        S3 = [[A_ + p["F"] * p["Lb"] * r_ / I_, -p["F"] * p["aL"] * r_ / (2 * I_), 0], [-p["F"] * p["aL"] * r_ / (2 * I_), A_ * (1 + (p["Do"] / p["Di"]) ** 2), 0], [0, 0, -p["p"]]]
        ev = LM.principal3(S3)
        C.abs(f"{tag} principal stresses at the inner surface (σr = −p): JS vs numpy, max |Δ| (MPa)", max(abs(a - b) for a, b in zip(tb["p3"], ev)) / 1e6, 0.0, 1e-8)

# ---------------------------------------------------------------- 4. closure: the analysis recovers the truth
T = json.loads((LAB / "src" / "truth.json").read_text())
OUT = json.loads((LAB / "src" / "results.json").read_text())
R, u = OUT["res"], OUT["u"]


def clos(name, val, truth, uu, scale=1.0, nd=3):
    k = abs(val - truth) / (2 * uu)
    C.abs(f"closure: {name} — |Δ| = {k:.2f} U", val * scale, truth * scale, 3 * uu * scale, note="within 3u (99.7 %); students use 2u")


clos("E from Part A vs truth 68.9 GPa", R["E_A"], T["E"], u["E_A"], 1e-9)
clos("ν from Part A vs truth 0.33", R["nu_A"], T["nu"], u["nu_A"])
clos("β_H vs truth 1.5°", R["beta_H"], math.degrees(T["H"]["beta"]), u["beta_H"])
clos("β_K vs truth −1.0°", R["beta_K"], math.degrees(T["K"]["beta"]), u["beta_K"])
G_t = T["E"] / (2 * (1 + T["nu"]))
clos("G (mean of H and K) vs truth E/2(1+ν)", R["G_mean"], G_t, u["G_mean"], 1e-9)
clos("K above mid-height vs truth 0.8°", R["phiK_off"], 90 - math.degrees(T["K"]["phi"]), u["phiK_off"])
clos("ν from the pressure strains vs truth", R["C_nu"], T["nu"], u["C_nu"])
ro_t, ri_t = T["Do"] / 2, T["Do"] / 2 - T["t"]
clos("hoop stress per MPa vs Lamé with the true tube", R["C_sth"], 2e6 * ri_t ** 2 / (ro_t ** 2 - ri_t ** 2), u["C_sth"], 1e-6)
for key, rec, g, nm in (("BH", "B", "H", "Part B at H"), ("BK", "B", "K", "Part B at K"), ("XH", "Cc", "H", "Part C + lever at H")):
    st = T["rec"][rec][-1]["s" + g]
    p1, p2, _ = LM.principal2(st["sx"], st["sy"], st["txy"])
    clos(f"σmax, {nm}, vs the truth state", R[f"{key}_s1"], p1, u[f"{key}_s1"], 1e-6)
    clos(f"σmin, {nm}, vs the truth state", R[f"{key}_s2"], p2, u[f"{key}_s2"], 1e-6)
st = T["rec"]["Cc"][-1]["sH"]
tabs = LM.abs_shear(st["sx"], st["sy"], st["txy"])[0]
clos("absolute τmax at H, Part C + lever, vs the truth state", R["XH_tabs"], tabs, u["XH_tabs"], 1e-6)
C.true(f"closure: at H with pressure and the lever both in-plane principal stresses are tensile (σmin = {R['XH_s2'] / 1e6:.2f} MPa)", R["XH_s2"] > 3 * u["XH_s2"])
C.true("closure: thin-wall hoop stress is rejected by the data (|Δ| > U)", abs(R["C_dsth_thin"]) > 2 * u["C_dsth_thin"])

# ---------------------------------------------------------------- 5. D1: page preset vs analysis
D1 = OUT["D1"]
best = next(d for d in D1["table"] if d["name"] == D1["best"])
dj = next(t for t in js["tube"] if t["k"] == "design")
tabs_js = (dj["p3"][0] - dj["p3"][2]) / 2
C.rel(f"D1: absolute τmax at the critical point of {D1['best']}, page preset (inner surface, top) vs analysis", tabs_js, best["crit"]["tabs"], 1e-12)
C.true(f"D1: the analysis's critical point for {D1['best']} is the inner surface, tension side", best["crit"]["where"] == "inner" and best["crit"]["side"] == "tension side")
C.true(f"D1: the in-plane trap picks {D1['best_inplane']}, lighter than {D1['best']} and unsafe by Tresca",
       next(d for d in D1["table"] if d["name"] == D1["best_inplane"])["sf_tresca"] < D1["n"] and next(d for d in D1["table"] if d["name"] == D1["best_inplane"])["mass"] < best["mass"])

sys.exit(C.write(LAB / "tests" / "results_python.md"))

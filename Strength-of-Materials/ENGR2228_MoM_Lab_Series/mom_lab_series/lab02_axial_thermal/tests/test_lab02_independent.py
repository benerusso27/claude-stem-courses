"""Lab 2 independent verification (Python / numpy / scipy).

1. Cross-language: the page's closed forms vs src/lab02_model.py.
2. Cross-method: scipy quadrature for the taper and a numpy least-squares solve of the redundant system.
3. Closure: lab02_analysis.py on sample_data.csv recovers the generating values within its stated uncertainty.
"""
import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np
from scipy.integrate import quad

LAB = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LAB / "src"))
sys.path.insert(0, str(LAB.parent / "shared"))
from checklib import Checks  # noqa: E402
import lab02_model as PM  # noqa: E402

C = Checks("Lab 2 — independent checks (Python/scipy) and data-pipeline closure")
JS = r"""
const {loadModel}=require('%s'); const M=loadModel('%s'); const out={};
for (const k of ['rodtube','bolt']) { const p=M.PRESETS[k]; out[k]={p, cf:M.parallelClosed(p), mats:M.MATERIALS}; }
for (const k of ['stepped','taper']) { const p=Object.assign({},M.PRESETS[k]); const cf=M.seriesClosed(p); out[k]={p, R:cf.R, uB:cf.uB, uC:cf.uC, f1:cf.f1, feR:M.seriesFE(p,512).R}; }
console.log(JSON.stringify(out));
""" % ((LAB.parent / "shared" / "test_harness.js").as_posix(), (LAB / "lab02_simulation.html").as_posix())
js = json.loads(subprocess.run(["node", "-e", JS], capture_output=True, text=True, check=True).stdout)
mats = js["rodtube"]["mats"]

for key in ("rodtube", "bolt"):
    p, cf = js[key]["p"], js[key]["cf"]
    m1 = dict(E=mats[p["mat1"]]["E"], A=PM.area_circle(p["d1"]), L=p["L"], alpha=mats[p["mat1"]]["alpha"])
    m2 = dict(E=mats[p["mat2"]]["E"], A=PM.area_tube(p["do"], p["di"]), L=p["L"], alpha=mats[p["mat2"]]["alpha"])
    if p["contact"]:
        g = p["g"]
    else:
        g = -p["F0"] * (1 / (m1["E"] * m1["A"] / p["L"]) + 1 / (m2["E"] * m2["A"] / p["L"]))
    F1, F2, _ = PM.parallel(p["P"], p["dT"], m1, m2, g, contact=p["contact"], L2=None if p["contact"] else p["L"])
    sc = max(abs(F1), abs(F2), 1)
    C.abs(f"[{key}] F1: JavaScript vs Python closed form (relative to largest force)", cf["F1"] / sc, F1 / sc, 1e-12)
    C.abs(f"[{key}] F2: JavaScript vs Python closed form", cf["F2"] / sc, F2 / sc, 1e-12)
    # numpy least squares on [equilibrium; compatibility] with both members active
    L2 = p["L"] - (p["contact"] and g or 0)
    k1, k2 = m1["E"] * m1["A"] / p["L"], m2["E"] * m2["A"] / L2
    A = np.array([[1.0, 1.0], [1 / k1, -1 / k2]])
    b = np.array([-p["P"], -g - p["dT"] * (m1["alpha"] * p["L"] - m2["alpha"] * L2)])
    x = np.linalg.solve(A, b)
    C.abs(f"[{key}] F1: JavaScript closed form vs numpy.linalg.solve of the 2×2 system", cf["F1"] / sc, x[0] / sc, 1e-12)
C.rel("rod in tube: gap-closing load k1·g (Python)", js["rodtube"]["cf"]["Pgap"], PM.gap_closing_load(
    dict(E=205e9, A=PM.area_circle(12.7e-3), L=0.15), 40e-6), 1e-12)
C.rel("bolt and sleeve: dF/dT JavaScript vs Python", js["bolt"]["cf"]["dFdT"], PM.thermal_clamp_force_per_degree(
    dict(E=205e9, A=PM.area_circle(10e-3), L=0.1, alpha=11.7e-6), dict(E=68.9e9, A=PM.area_tube(20e-3, 10.5e-3), L=0.1, alpha=23.6e-6)), 1e-12)

for key in ("stepped", "taper"):
    p = js[key]["p"]
    E1, a1 = mats[p["smat1"]]["E"], mats[p["smat1"]]["alpha"]
    E2, a2 = mats[p["smat2"]]["E"], mats[p["smat2"]]["alpha"]
    f1 = quad(lambda x: 1 / (E1 * PM.area_circle(p["da"] + (p["db"] - p["da"]) * x / p["L1"])), 0, p["L1"], epsabs=0, epsrel=1e-13)[0]
    C.rel(f"[{key}] segment-1 flexibility: closed form vs scipy.quad", js[key]["f1"], f1, 1e-11)
    R, N1, N2, dfree = PM.series(p["PB"], p["dT"], dict(L=p["L1"], E=E1, da=p["da"], db=p["db"], alpha=a1),
                                 dict(L=p["L2"], E=E2, d=p["d2"], alpha=a2), p["support"], p["g"])
    C.rel(f"[{key}] wall reaction: JavaScript vs Python closed form", js[key]["R"], R, 1e-12)
    C.rel(f"[{key}] wall reaction: closed form vs FE with N = 512", js[key]["feR"], R, 1e-5 if key == "taper" else 1e-10, "taper: discretization; prismatic: round-off only")

C.rel("thermal buckling ΔT for d = 10 mm, L = 0.5 m steel (Python vs hand: π²r²/(α(L/2)²))",
      PM.thermal_buckling_dT(10e-3, 0.5, 11.7e-6), math.pi ** 2 * (2.5e-3) ** 2 / (11.7e-6 * 0.25 ** 2), 1e-12)

# ---------------- closure test of the data pipeline ----------------
subprocess.run([sys.executable, str(LAB / "src" / "lab02_analysis.py")], check=True, capture_output=True)
r = json.loads((LAB / "src" / "results.json").read_text())
t = json.loads((LAB / "src" / "truth.json").read_text())


def within(name, val, ref, U, note=""):
    C.true(f"closure: {name} recovered within U = {U:.3g} (value {val:.5g}, truth {ref:.5g})" + (f" — {note}" if note else ""), abs(val - ref) <= U)


within("E of 6061-T6 (GPa)", r["A"]["E"], t["E_al"] / 1e9, 2 * r["A"]["uE"], "includes the +0.6 % gage-factor error")
within("Poisson's ratio", r["A"]["nu"], t["nu_al"], 2 * r["A"]["unu"])
within("bending fraction front/back", r["A"]["beta"], t["bend_A"], 0.005)
within("gap g (mm)", r["B"]["gap_mm"], t["gap"] * 1e3, 2 * r["B"]["ugap_mm"])
within("tube share after contact", r["B"]["share"], t["B_share"], 2 * r["B"]["u_share"])
within("bolt dF/dT (N/K)", r["C"]["dFdT"], t["C_dF_dT_true"], 2 * r["C"]["u_dFdT"], "residual thermal output of the gage biases it high")
within("bolt preload at 20 °C (N)", r["C"]["F0"], t["preload"], 0.03 * t["preload"])
sys.exit(C.write(LAB / "tests" / "results_python.md"))

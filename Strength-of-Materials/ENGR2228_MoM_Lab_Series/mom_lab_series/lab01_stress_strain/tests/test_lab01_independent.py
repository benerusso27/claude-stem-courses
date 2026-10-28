"""Lab 1 independent verification (Python / scipy).

    python3 tests/test_lab01_independent.py        (from lab01_stress_strain/)

1. Cross-language: the page's JavaScript closed forms vs a separate Python implementation.
2. Cross-method: the page's marching solver vs scipy root finding / bounded optimization / quadrature
   on the finite-strain uniform-bar curve.
3. Closure test of the data pipeline: lab01_analysis.py run on sample_data.csv must recover the
   values used to generate it (truth.json) within its own stated expanded uncertainty.
"""
import json
import math
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LAB = HERE.parent
sys.path.insert(0, str(LAB / "src"))
from lab01_model import swift_closed_forms, swift_exact_by_quadrature  # noqa: E402

rows = []


def check(name, val, ref, tol, note=""):
    rel = abs(val - ref) / max(abs(ref), 1e-300)
    rows.append((name + (f" — {note}" if note else ""), val, ref, rel, tol, rel <= tol))


JS = r"""
const {loadModel}=require('%s');
const M=loadModel('%s');
const out={};
for (const k of ['steel','al','ss']) {
  const p=Object.assign({},M.PRESETS[k],M.SPECIMEN);
  const cf=M.closedForms(p);
  const p0=Object.assign({},p,{delta:0});
  const x0=M.extract(M.simulate(p0,8192),p0);
  out[k]={p, cf, x0:{sigU:x0.sigU, e_u:x0.e_u, sigY:x0.sigY, uU:x0.uU}};
}
console.log(JSON.stringify(out));
""" % ((LAB.parent / "shared" / "test_harness.js").as_posix(), (LAB / "lab01_simulation.html").as_posix())

js = json.loads(subprocess.run(["node", "-e", JS], capture_output=True, text=True, check=True).stdout)

for key, r in js.items():
    p, cf, x0 = r["p"], r["cf"], r["x0"]
    py = swift_closed_forms(p["E"], p["K"], p["n"], p["sigma_e"])
    for name in ("sigY", "sigU", "e_u", "uU"):
        check(f"[{key}] {name}: JavaScript closed form vs Python closed form", cf[name], py[name], 1e-12)
    ex = swift_exact_by_quadrature(p["E"], p["K"], p["n"], p["sigma_e"])
    check(f"[{key}] σU: page solver (δ = 0) vs scipy bounded maximization", x0["sigU"], ex["sigU"], 1e-6)
    check(f"[{key}] εu: page solver (δ = 0) vs scipy maximization", x0["e_u"], ex["e_u"], 2e-3, "sample nearest the peak")
    check(f"[{key}] 0.2 % offset on engineering curve: page solver vs scipy brentq", x0["sigY"], ex["sigY_eng"], 5e-5)
    check(f"[{key}] energy to peak: page trapezoid vs scipy quad", x0["uU"], ex["uU"], 1e-3, "first-order endpoint, h = 1/8192")
    check(f"[{key}] Considère closed form σU vs scipy exact maximum", cf["sigU"], ex["sigU"], 1e-5, "rigid-plastic approximation at a stationary point")

# ---- 3. closure test of the measurement pipeline -----------------------------------------
subprocess.run([sys.executable, str(LAB / "src" / "lab01_analysis.py")], check=True, capture_output=True)
res = json.loads((LAB / "src" / "results.json").read_text())
truth = json.loads((LAB / "src" / "truth.json").read_text())
for key in ("steel_1018HR", "al_6061T6"):
    r, t = res[key], truth[key]

    def within(name, val, ref, U, note=""):
        ok = abs(val - ref) <= U
        rows.append((f"[{key}] closure: {name} recovered within its expanded uncertainty U = {U:.3g}" + (f" — {note}" if note else ""),
                     val, ref, abs(val - ref) / abs(ref), U / abs(ref), ok))
    within("E (GPa)", r["E"], t["E_GPa"], 2 * r["uE"] + 0.003 * t["E_GPa"], "plus 0.3 % finite-strain/neck-zone shift of the truth model")
    within("σU (MPa)", r["sigU"], t["sigma_U_MPa"], 2 * r["uU"])
    within("machine compliance (mm/kN)", r["Cm"], t["compliance_mm_per_kN"], 2 * r["uCm"] + 1e-5)
    within("grip seating toe (mm)", r["toe"], t["toe_mm"], 2 * r["u_toe"] + 1e-3)
    within("uniform elongation εu", r["e_u"], t["e_at_max_load"], 2 * r["u_eu"])
    within("elongation after fracture (%)", r["EL"], (t["Lf_mm"] - 50.0) / 50.0 * 100, 2 * r["u_EL"] + 0.1, "mark-measurement scatter 0.04 mm")
    within("true stress in neck at fracture (MPa)", r["sig_t_neck_f"], t["true_stress_neck_fracture_MPa"], 2 * r["u_sig_t_neck_f"])
    if key.startswith("steel"):
        within("upper yield point (MPa)", r["sig_uy"], t["sigma_uy_MPa"], 2 * r["u_uy"] + 2.0, "serration/noise on the peak sample")
        within("lower yield point (MPa)", r["sig_ly"], t["sigma_ly_MPa"] * (1 - t["delta"]), 2 * r["u_ly"], "plateau set by the weakest section")

lines = ["## Lab 1 — independent checks (Python/scipy) and data-pipeline closure", "",
         "| Test | Value | Reference | Rel. difference | Tolerance | Result |", "|---|---:|---:|---:|---:|---|"]
for name, v, ref, rel, tol, ok in rows:
    lines.append(f"| {name} | {v:.8g} | {ref:.8g} | {rel:.2e} | {tol:.1e} | {'PASS' if ok else '**FAIL**'} |")
nf = sum(not r[-1] for r in rows)
lines += ["", f"{len(rows) - nf} of {len(rows)} passed."]
(HERE / "results_python.md").write_text("\n".join(lines) + "\n")
print("\n".join(lines))
sys.exit(1 if nf else 0)

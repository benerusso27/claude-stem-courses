"""Lab 3 independent verification (Python / numpy / scipy).

1. Cross-language: the page's closed forms and series vs src/lab03_model.py.
2. Cross-method: the page's ring integration vs scipy.quad of the same laws; the page's conjugate-gradient
   finite differences vs a scipy.sparse direct solve of the same grid; the series vs Richardson-extrapolated FD.
3. Closure: lab03_analysis.py on sample_data.csv recovers the generating values within its stated uncertainty.
"""
import json
import math
import subprocess
import sys
from pathlib import Path

LAB = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LAB / "src"))
sys.path.insert(0, str(LAB.parent / "shared"))
from checklib import Checks  # noqa: E402
import lab03_model as PM  # noqa: E402

C = Checks("Lab 3 — independent checks (Python/scipy) and data-pipeline closure")
JS = r"""
const {loadModel}=require('%s'); const M=loadModel('%s'); const o={mats:M.MATERIALS, epp:[], rings:[], rect:[], fd:[], tube:[]};
const c=3.175e-3;
for (const [cc,cci] of [[c,0],[c,0.6*c],[25e-3,15e-3]]) for (const k of [0.7,1.5,4,50]) { const m=M.MATERIALS.steel; const th=k*m.tauY/(m.G*cc);
  o.epp.push({cc,cci,th,T:M.eppTorque(cc,cci,m.G,m.tauY,th)}); }
for (const key of ['steel','al','ci']) for (const k of [0.8,3,40]) { const m=M.MATERIALS[key]; const th=k*m.tauY/(m.G*c); if (key==='ci'&&k>2) continue;
  o.rings.push({key,th,T:M.torqueRings(m,c,0,th,2048)}); }
for (const ab of [1,1.5,3,10]) { const s=M.rectSeries(ab,1); o.rect.push({ab,c1:s.c1,c2:s.c2,k:s.k}); }
for (const [ab,N] of [[1,8],[2,16],[4,8]]) { const f=M.rectFD(ab,1,N); o.fd.push({ab,N,c2:f.c2,k:f.k}); }
for (const t of [1e-3,5e-3,15e-3]) o.tube.push({t,b:M.tubeBredt(50e-3,t,100,79.5e9),e:M.tubeExact(50e-3,t,100,79.5e9)});
console.log(JSON.stringify(o));
""" % ((LAB.parent / "shared" / "test_harness.js").as_posix(), (LAB / "lab03_simulation.html").as_posix())
js = json.loads(subprocess.run(["node", "-e", JS], capture_output=True, text=True, check=True).stdout)
mats = js["mats"]
st = mats["steel"]

for e in js["epp"]:
    C.rel(f"EPP torque, c = {e['cc'] * 1e3:.3g} mm, c_i/c = {e['cci'] / e['cc']:.2g}, θ = {e['th']:.4g}: JavaScript vs Python",
          e["T"], PM.epp_torque(e["cc"], e["cci"], st["G"], st["tauY"], e["th"]), 1e-13)
    m = dict(law="epp", G=st["G"], tauY=st["tauY"])
    C.rel("    … closed form vs scipy.quad of the EPP law", e["T"], PM.torque_quad(m, e["cc"], e["cci"], e["th"]), 1e-10)
for r in js["rings"]:
    m = dict(mats[r["key"]])
    C.rel(f"[{r['key']}] ring integration (N = 2048) vs scipy.quad of the same law, θ = {r['th']:.4g} rad/m",
          r["T"], PM.torque_quad(m, 3.175e-3, 0.0, r["th"]), 1e-6, "midpoint rule O(N⁻²)")
for r in js["rect"]:
    s = PM.rect_series(r["ab"], 1.0)
    C.rel(f"rectangle a/b = {r['ab']}: c₁ JavaScript vs Python series", r["c1"], s["c1"], 1e-12)
    C.rel(f"rectangle a/b = {r['ab']}: c₂ JavaScript vs Python series", r["c2"], s["c2"], 1e-12)
for f in js["fd"]:
    p = PM.rect_fd(f["ab"], 1.0, f["N"])
    C.rel(f"rectangle FD a/b = {f['ab']}, N = {f['N']}: conjugate gradients (page) vs sparse direct solve (scipy), c₂", f["c2"], p["c2"], 1e-9)
    C.rel(f"    … same grid, τ_max coefficient k", f["k"], p["k"], 1e-9)
for ab in (1.0, 2.0, 3.0):
    a1, a2 = PM.rect_fd(ab, 1.0, 32), PM.rect_fd(ab, 1.0, 64)
    s = PM.rect_series(ab, 1.0)
    C.rel(f"rectangle a/b = {ab}: series c₂ vs Richardson-extrapolated scipy FD (N = 32, 64)", s["c2"], (4 * a2["c2"] - a1["c2"]) / 3, 2e-5)
for t in js["tube"]:
    b, e = PM.tube_bredt(50e-3, t["t"], 100, 79.5e9), PM.tube_exact(50e-3, t["t"], 100, 79.5e9)
    C.rel(f"tube t = {t['t'] * 1e3:g} mm: Bredt stress JavaScript vs Python", t["b"]["tau"], b["tau"], 1e-13)
    C.rel(f"tube t = {t['t'] * 1e3:g} mm: exact stress JavaScript vs Python", t["e"]["tau"], e["tau"], 1e-13)

# ---------------- closure test of the data pipeline ----------------
subprocess.run([sys.executable, str(LAB / "src" / "lab03_analysis.py")], check=True, capture_output=True)
r = json.loads((LAB / "src" / "results.json").read_text())
t = json.loads((LAB / "src" / "truth.json").read_text())


def within(name, val, ref, U, note=""):
    C.true(f"closure: {name} recovered within U = {U:.3g} (value {val:.5g}, truth {ref:.5g})" + (f" — {note}" if note else ""), abs(val - ref) <= U)


gainG = t["torque_gain"] / t["tropt_gain"]
for k in ("steel", "al"):
    within(f"[{k}] G (GPa)", r[k]["G_GPa"], t[k]["G"] / 1e9 * gainG, 2 * r[k]["uG_GPa"], "truth includes the load-cell and troptometer gain errors")
    within(f"[{k}] compliance C_m (°/N·m)", r[k]["Cm_deg_per_Nm"], math.degrees(t["C_m"]), 2 * r[k]["uCm_deg_per_Nm"])
    within(f"[{k}] backlash (°)", r[k]["toe_deg"], math.degrees(t["backlash"]), max(2 * r[k]["utoe_deg"], 0.03), "toe not fully seated at 1.5 N·m")
    within(f"[{k}] fracture shear strain γ_f", r[k]["gamma_f"], t[k]["gf"], 0.02 * t[k]["gf"])
within("[steel] τ_Y from the EPP fit (MPa)", r["steel"]["tauY_MPa"], t["steel"]["tauY"] / 1e6 * t["torque_gain"], 2 * r["steel"]["u_tauY_MPa"])
within("[steel] permanent twist after unloading (°)", r["steel"]["phi_res_meas_deg"], r["steel"]["phi_res_pred_deg"], 2 * r["steel"]["u_phi_res_pred_deg"] + 0.02)
for gq in ("0.1", "0.5", "1.0"):
    tau_true = PM.tau_of(t["steel"], float(gq)) / 1e6 * t["torque_gain"]
    within(f"[steel] Nadai τ at γ = {gq} (MPa)", r["steel"]["nadai"][gq]["tau_MPa"], tau_true, 0.015 * tau_true)
within("[al] Nadai τ at γ = 0.5 (MPa)", r["al"]["nadai"]["0.5"]["tau_MPa"], PM.tau_of(t["al"], 0.5) / 1e6 * t["torque_gain"], 0.015 * 212)
within("[ci] secant G at low torque (GPa)", r["ci"]["G_secant_low_GPa"], t["ci"]["G"] / 1e9, 0.04 * 41, "nonlinearity lowers the secant slightly")
sys.exit(C.write(LAB / "tests" / "results_python.md"))

"""Lab 5 independent verification (Python / numpy / scipy).

1. Cross-language: the page's section properties, Q, tau and f_s vs adaptive quadrature (src/lab05_model.py).
2. Cross-method: the page's wide-rectangle series (cosine series in y) vs a sine series in x typed independently.
3. Cross-method: the page's partial-interaction closed form vs scipy's collocation BVP solver, and the page's
   discrete-spring solver vs a Python implementation.
4. Closure: lab05_analysis.py on sample_data.csv recovers the generating values within its stated uncertainty.
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
import lab05_model as PM  # noqa: E402

C = Checks("Lab 5 — independent checks (Python/scipy) and data-pipeline closure")
JS = r"""
const {loadModel}=require('%s'); const M=loadModel('%s'); const P=M.PRESETS; const o={sec:[], rect:[], timo:[], lay:[]};
for (const k of ['rectUp','ibeamWeb','tee','box','circle']) { const p=P[k], c=M.sectionClosed(p);
  o.sec.push({k, p, I:c.I, A:c.A, ybar:c.ybar, QNA:c.QNA, fs:c.fs, tauNA:c.tauNA(p.V), tq:[0.1,0.3,0.45].map(f=>({y:f*c.H, tau:c.tau(f*c.H, p.V)}))}); }
for (const [b,h,nu] of [[0.0254,0.0508,0.33],[0.0508,0.0254,0.33],[0.04,0.01,0.25],[0.01,0.03,0.30]]) for (const xi of [1,0,0.5])
  o.rect.push({b,h,nu,xi,v:M.rectSeries(b,h,nu,xi)});
for (const k of ['ibeamSpan','cantilever']) { const p=P[k], t=M.timoClosed(p); o.timo.push({k, p, I:t.sec.I, A:t.sec.A, fs:t.sec.fs, bend:t.bend, shear:t.shear, E:M.MATERIALS[p.mat].E, G:t.G}); }
for (const [k,ov] of [['layered',{}],['layered',{conn:'glue'}],['design',{s1:0.1,s2:0.1}],['design',{conn:'glue',Gg:30e6,tg:1e-3}],['layered',{s1:0.3,s2:0.3}],['design',{}]]) {
  const p=Object.assign({},P[k],ov); const c=M.newmarkClosed(p); const d=p.conn==='bolts'?M.boltsDiscrete(p):null;
  o.lay.push({p, k:c.k, delta:c.delta, slip0:c.slip0, disc:d?{delta:d.delta, slip0:d.slip0, F:d.forces.map(f=>f.F), xs:d.xs}:null}); }
console.log(JSON.stringify(o));
""" % ((LAB.parent / "shared" / "test_harness.js").as_posix(), (LAB / "lab05_simulation.html").as_posix())
js = json.loads(subprocess.run(["node", "-e", JS], capture_output=True, text=True, check=True).stdout)

for s in js["sec"]:
    p = s["p"]
    if p["shape"] == "circle":
        c = p["d"] / 2
        C.rel("circle: I = πc⁴/4, JavaScript vs Python", s["I"], math.pi * c ** 4 / 4, 1e-13)
        C.rel("circle: f_s, JavaScript 10/9 vs Python adaptive quadrature", s["fs"], PM.circle_form_factor(p["d"]), 1e-8)
        C.rel("circle: τ_max, JavaScript vs Python", s["tauNA"], PM.circle_tau_max(p["V"], p["d"]), 1e-12)
        continue
    lay = {"rect": lambda: PM.rect(p["b"], p["h"]), "ibeam": lambda: PM.ibeam(p["B"], p["H"], p["tf"], p["tw"]),
           "tee": lambda: PM.tee(p["B"], p["H"], p["tf"], p["tw"]), "box": lambda: PM.box(p["B"], p["H"], p["tw"]) if p["tf"] == p["tw"] else
           [(0.0, p["tf"], p["B"]), (p["tf"], p["H"] - p["tf"], 2 * p["tw"]), (p["H"] - p["tf"], p["H"], p["B"])]}[p["shape"]]()
    pr = PM.props(lay)
    C.rel(f"{s['k']}: I, JavaScript layer sums vs Python quadrature", s["I"], pr["I"], 1e-11)
    C.rel(f"{s['k']}: neutral axis", s["ybar"], pr["ybar"], 1e-11)
    C.rel(f"{s['k']}: Q at the NA", s["QNA"], PM.Q_at(lay, pr["ybar"], pr["ybar"]), 1e-11)
    C.rel(f"{s['k']}: f_s, JavaScript exact antiderivative vs Python nested quadrature", s["fs"], PM.form_factor(lay), 1e-8)
    for t in s["tq"]:
        C.rel(f"{s['k']}: τ = VQ/(It) at y = {t['y'] * 1e3:.2f} mm", t["tau"], PM.tau_at(lay, p["V"], t["y"]), 1e-10)
for r in js["rect"]:
    C.rel(f"wide rectangle b = {r['b'] * 1e3:.1f}, h = {r['h'] * 1e3:.1f} mm, ν = {r['nu']}, x = {r['xi']}·b/2: τ/(VQ/Ib), cosine series in y (JS) vs sine series in x (Python)",
          r["v"], PM.rect_edge_ratio_xseries(r["b"], r["h"], r["nu"], x_over_b=r["xi"] / 2), 2e-7)
for t in js["timo"]:
    p = t["p"]
    b, s = PM.timoshenko_delta(p["P"], p["L"], t["E"], t["G"], t["I"], t["A"], t["fs"], p["support"])
    C.rel(f"[{t['k']}] Timoshenko bending part, JavaScript vs Python", t["bend"], b, 1e-13)
    C.rel(f"[{t['k']}] Timoshenko shear part", t["shear"], s, 1e-13)
for L_ in js["lay"]:
    p = L_["p"]
    geom = PM.two_layer(p["b"], p["t1"], p["t2"], 68.9e9)
    load = dict(kind="point", P=p["P"]) if p["load"] == "point" else dict(kind="udl", w=p["w"])
    tag = f"{p['conn']}, {p['load']}, L = {p['L']} m" + (f", s = {p['s1'] * 1e3:.0f}/{p['s2'] * 1e3:.0f} mm" if p["conn"] == "bolts" else "")
    if p["conn"] == "bolts" and abs(p["s1"] - p["s2"]) > 1e-12:
        pass
    else:
        sol = PM.smeared_bvp(geom, p["L"], load, L_["k"])
        C.rel(f"[{tag}] midspan deflection: JavaScript closed form vs scipy solve_bvp", L_["delta"], sol["delta"], 2e-7)
        C.rel(f"[{tag}] end slip: closed form vs solve_bvp", L_["slip0"], abs(sol["slip0"]), 2e-5)
    if L_["disc"]:
        d = PM.bolts_shoot(geom, p["L"], load, L_["disc"]["xs"], p["kb"])
        C.rel(f"[{tag}] discrete springs: midspan deflection, JavaScript vs Python", L_["disc"]["delta"], d["delta"], 1e-10)
        C.rel(f"[{tag}] discrete springs: end slip", L_["disc"]["slip0"], abs(d["slip0"]), 1e-9)
        C.rel(f"[{tag}] discrete springs: largest bolt force", max(abs(f) for f in L_["disc"]["F"]), max(abs(f) for f in d["forces"]), 1e-9)

# ---------------- closure test of the data pipeline ----------------
subprocess.run([sys.executable, str(LAB / "src" / "lab05_analysis.py")], check=True, capture_output=True)
r = json.loads((LAB / "src" / "results.json").read_text())
t = json.loads((LAB / "src" / "truth.json").read_text())
m = json.loads((LAB / "src" / "specimen_measurements.json").read_text())


def within(name, val, ref, U, note=""):
    C.true(f"closure: {name} recovered within U = {U:.3g} (value {val:.6g}, truth {ref:.6g})" + (f" — {note}" if note else ""), abs(val - ref) <= U)


bias = (1 + t["gf_error"]) * m["reference"]["G_al_GPa"] * 1e9 / t["G"]          # strain-gage τ = G_ref γ_measured
for cfg in ("upright", "flat"):
    a = r["A"][cfg]
    within(f"Part A {cfg}: face τ/(VQ/Ib)", a["ratio"], t["partA"][cfg]["ratio"] * bias, 2 * a["u_ratio"], "truth × gage-factor and G biases")
for j, w in enumerate(r["B"]["web"]):
    within(f"Part B web gage {j + 1}: τ per newton of V (MPa/N)", w["slope"], t["partB"]["tau_per_V"][j] * 1e-6 * bias, 2 * w["u_slope"])
d = r["B"]["defl"]
within("Part B: E from the deflection fit (GPa)", d["E"], t["E"] / 1e9 / t["lvdt_gain"], 2 * d["uE"], "truth / LVDT gain")
within("Part B: G from the deflection fit (GPa)", d["G"], t["G"] / 1e9 / t["lvdt_gain"], 2 * d["uG"], "truth / LVDT gain")
within("Part B: shear factor f_s of the measured section vs truth section", r["B"]["fs"], t["partB"]["fs"], 0.002 * t["partB"]["fs"])
kb = r["C"]["kb"]
within("Part C: bolt slip modulus from the bolted deflection (N/m)", kb["kb_disc"], t["layered"]["kb"], max(2 * kb["u_kb"], 0.03 * t["layered"]["kb"]), "E from Lab 2, dimensions measured")
within("Part C: loose end slip per newton (m/N)", r["C"]["loose"]["slip"], t["partC"]["loose"]["slip_per_N"], 3 * r["C"]["loose"]["uslip"] + 1e-9)
within("Part C: bonded effective EI = full composite (N·m²)", r["C"]["bonded"]["EI"], t["partC"]["geom"]["EIfull"] / t["lvdt_gain"], 2 * r["C"]["bonded"]["uEI"] + 0.01 * t["partC"]["geom"]["EIfull"])
sys.exit(C.write(LAB / "tests" / "results_python.md"))

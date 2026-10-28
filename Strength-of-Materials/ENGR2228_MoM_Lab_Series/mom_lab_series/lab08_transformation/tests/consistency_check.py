"""Cross-file consistency for Lab 8: units, symbols, sign convention, constants, references.

    python3 tests/consistency_check.py      (from lab08_transformation/)
"""
import csv
import json
import re
import sys
from pathlib import Path

LAB = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LAB.parent / "shared"))
from consistency import run  # noqa: E402

H = (LAB / "src" / "lab08_handout.md").read_text(encoding="utf-8")
K = (LAB / "src" / "lab08_instructor_key.md").read_text(encoding="utf-8")
SIM = (LAB / "lab08_simulation.html").read_text(encoding="utf-8")
ANA = (LAB / "src" / "lab08_analysis.py").read_text(encoding="utf-8")
M = json.loads((LAB / "src" / "specimen_measurements.json").read_text())
L1 = json.loads((LAB.parent / "lab01_stress_strain" / "src" / "results.json").read_text())
L2 = json.loads((LAB.parent / "lab02_axial_thermal" / "src" / "results.json").read_text())
L3 = json.loads((LAB.parent / "lab03_torsion" / "src" / "results.json").read_text())
K6 = (LAB.parent / "lab06_eccentric" / "src" / "lab06_instructor_key.md").read_text(encoding="utf-8")

extra = []
appx = H[H.index("## Appendix A"):H.index("## Appendix B")]


def row(label):
    ln = [x for x in appx.splitlines() if x.startswith("| " + label)]
    return ln[0].split("|")[2].strip() if ln else ""


j = lambda v, nd: ", ".join(f"{x:.{nd}f}" for x in v)  # noqa: E731
tb, ros = M["tube"], M["rosette"]
for label, want in (("$D_o$ (mm)", j(tb["Do_mm"], 2)), ("Wall thickness (mm)", j(tb["t_mm"], 2)), ("$L_b$ / $a_L$ (mm)", f"{tb['Lb_mm']:.1f} / {tb['aL_mm']:.1f}"),
                    ("Rosettes", f"gage factor {ros['GF']:.2f} ± {ros['GF_tol_pct']:.1f} %, $K_t$ = {100 * ros['Kt']:.1f} %, $\\nu_0$ = {ros['nu0']}")):
    extra.append((f"Appendix A matches measurements JSON: {label}", row(label) == want, f"{row(label)} vs {want}"))
for label, val, phrase in (("micrometer", M["micrometer_accuracy_mm"], "micrometer is good to ±{:g} mm"), ("ball micrometer", M["ball_micrometer_accuracy_mm"], "ball micrometer to ±{:g} mm"),
                           ("rule", M["rule_accuracy_mm"], "the rule to ±{:g} mm"), ("load cell", M["loadcell_accuracy_pct"], "load cell to ±{:g} %"),
                           ("pressure", M["p_accuracy_MPa"], "pressure transducer to ±{:g} MPa")):
    extra.append((f"Table A2 caption accuracy matches measurements JSON: {label}", phrase.format(val) in H, phrase.format(val)))
ref = M["reference"]
extra.append(("Table 1: E and ν equal the Lab 2 results", abs(ref["E_al_GPa"] - round(L2["A"]["E"], 2)) < 1e-9 and abs(ref["nu_al"] - round(L2["A"]["nu"], 4)) < 1e-9
              and "68.46 ± 0.47 (your Lab 2)" in H and "0.3296 ± 0.0029 (your Lab 2)" in H))
extra.append(("Table 1: G equals the Lab 3 result for 6061-T6", abs(ref["G_al_GPa"] - round(L3["al"]["G_GPa"], 2)) < 1e-9 and "26.03 ± 0.12 (your Lab 3)" in H))
extra.append(("Table 1: σ_Y equals the Lab 1 result for 6061-T6", abs(ref["sY_al_MPa"] - round(L1["al_6061T6"]["sigY"], 1)) < 1e-9 and "273.7 ± 1.0 (your Lab 1)" in H))
extra.append(("simulation 6061-T6: E = 68.9 GPa (series truth value), σ_Y = Lab 1 value", "E: 68.9e9, nu: 0.33, sY: 273.7e6" in SIM))
# Lab 6 X2 predicted this tube's stresses; Lab 8's pre-lab must reproduce them
for nm, v6, v8 in (("σ at the top", "53.36", "$\\sigma_x$ = 53.36 MPa"), ("Tc/J", "21.34", "$Tc/J$ = 21.34"), ("VQ/It", "3.43", "$VQ/(It)$ = 3.43"), ("τ at K", "24.77", "$\\tau_{xy}$ = −24.77 MPa at K")):
    extra.append((f"Lab 6 X2 prediction carried into Lab 8 P1: {nm}", v6 in K6 and v8 in K, f"Lab 6 {v6}"))
# D1
cat = re.findall(r"\((\d+\.?\d*), (\d+\.\d+)\)", ANA[ANA.index("CATALOG = ["):ANA.index("RHO_AL")])
tab6 = H[H.index("| Tube | $D_o$ (mm) | Wall (mm) |"):H.index(": Table 6.")]
ok6 = len(cat) == 11 and all(f"| {a} × {b} | {float(a):.2f} | {b} |" in tab6 for a, b in cat)
extra.append(("D1 catalog: handout Table 6 equals the analysis catalog (11 tubes)", ok6, f"{len(cat)} tubes"))
extra.append(("D1 requirements in the handout match the analysis (20 MPa, 300 N·m, 300 N·m, 1.8, 3.0°/m, 50.8 mm)",
              "D1 = dict(p=20e6, T=300.0, M=300.0, n=1.8, twist_lim_deg_per_m=3.0, OD_max=50.8)" in ANA and "oil at 20 MPa" in H
              and "bending moment of 300 N·m and a torque of 300 N·m" in H and "\\sigma_Y/(2 \\times 1.8)" in H and "3.0° per meter" in H and "at most 50.8 mm" in H))
extra.append(("D1 simulation preset: M = T = 300 N·m (F 1000 N on 0.3 m arms), 20 MPa, 44.45 × 4.78, inner surface",
              "design: tubeOf({ Do: 44.45e-3, Di: 34.89e-3, F: 1000, aL: 0.3, Lb: 0.3, p: 20e6, phi: 0, surf: 'inner' })" in SIM))
# load limits and steps = data
rows = list(csv.DictReader(open(LAB / "sample_data.csv", newline="")))
mxF = max(float(r["load_N"]) for r in rows)
mxp = max(float(r["p_MPa"]) for r in rows)
extra.append(("safety limits equal the largest load and pressure in the data (600 N, 8 MPa)",
              "**Limits:** load 600 N; pressure 8 MPa; both together at most 600 N with 8 MPa" in H and mxF == 600 and mxp == 8))
extra.append(("procedure steps equal the data's (100 N steps; 2, 4, 6, 8 MPa; 200, 400, 600 N at 8 MPa)",
              "0 to 600 N in 100 N steps" in H and "2, 4, 6 and 8 MPa" in H and "200, 400 and 600 N" in H
              and [float(r["p_MPa"]) for r in rows if r["config"] == "pressure"] == [0, 2, 4, 6, 8]
              and [float(r["load_N"]) for r in rows if r["config"] == "combined"] == [0, 200, 400, 600]))
extra.append(("the local-axis convention is stated in the handout, the simulation and Figure 1",
              "$y$ is 90° counterclockwise from $x$ as seen from outside the tube" in H and "y is 90° counterclockwise from x as seen from outside the tube" in SIM
              and "y (90° ccw from x,\\nseen from outside)" in (LAB / "src" / "make_figures.py").read_text()))
extra.append(("thin-wall radius: Beer's inner radius used in the handout, the model and the page",
              "with $r$ the inner radius" in H and "p * ri / t" in (LAB / "src" / "lab08_model.py").read_text() and "p.p * tp.ri / tp.t" in SIM))

cfg = {
    "n": "08",
    "constants": {
        "tube 38.1 × 3.18": [("handout", "38.1 × 3.18 mm"), ("sim", "Do: 38.1e-3, Di: 31.75e-3"), ("gen", "Do=38.13e-3, t=3.205e-3"), ("figs", "DO, DI = 38.1e-3, 31.75e-3")],
        "arms 250 / 200 mm": [("handout", "L_b = 250 mm"), ("handout", "a_L = 200 mm"), ("sim", "F: 600, aL: 0.2, Lb: 0.25"), ("gen", "Lb=0.2506, aL=0.2002"),
                              ("figs", "$L_b$ = 250 mm"), ("figs", "$a_L$ = 200 mm")],
        "8 MPa": [("handout", "8 MPa"), ("sim", "p: 8e6"), ("gen", "8e6")],
        "K_t 1.2 %, ν0 0.285": [("handout", "$K_t$ = +1.2 %"), ("handout", "$\\nu_0$ = 0.285"), ("gen", "Kt=0.012, nu0=0.285"), ("sim", "nu0 = 0.285")],
    },
    "symbols": ["\\sigma_{ave}", "R", "\\theta_p", "\\sigma_1 \\ge \\sigma_2 \\ge \\sigma_3", "\\tau_{max}", "\\gamma_{xy}", "\\beta", "K_t", "G", "t_w = r_o - r_i",
                "Q", "a_L", "L_b", "\\sigma_\\theta", "\\sigma_r", "U = 2u"],
    "csv_columns": ["part", "config", "step", "load_N", "lever_mm", "p_MPa", "Ha_ue", "Hb_ue", "Hc_ue", "Ka_ue", "Kb_ue", "Kc_ue"],
    "sign_phrases": {"handout": ["Tension is positive", "plotted above the $\\sigma$ axis (Fig. 7.15)", "$(\\sigma_x, -\\tau_{xy})$", "counterclockwise from $x$"],
                     "sim": ["tension positive", "plotted above the σ axis (Fig. 7.15)", "X = (σ<sub>x</sub>, −τ<sub>xy</sub>)"],
                     "key": ["Mohr's circle \"clockwise above\""]},
    "extra": extra,
}
sys.exit(run(LAB, cfg))

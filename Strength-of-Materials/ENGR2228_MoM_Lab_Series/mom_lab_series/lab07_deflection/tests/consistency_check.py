"""Cross-file consistency for Lab 7: units, symbols, sign convention, constants, references.

    python3 tests/consistency_check.py      (from lab07_deflection/)
"""
import csv
import json
import re
import sys
from pathlib import Path

LAB = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LAB.parent / "shared"))
sys.path.insert(0, str(LAB / "src"))
from consistency import run  # noqa: E402

H = (LAB / "src" / "lab07_handout.md").read_text(encoding="utf-8")
K = (LAB / "src" / "lab07_instructor_key.md").read_text(encoding="utf-8")
SIM = (LAB / "lab07_simulation.html").read_text(encoding="utf-8")
GEN = (LAB / "src" / "generate_sample_data.py").read_text(encoding="utf-8")
ANA = (LAB / "src" / "lab07_analysis.py").read_text(encoding="utf-8")
M = json.loads((LAB / "src" / "specimen_measurements.json").read_text())
L1 = json.loads((LAB.parent / "lab01_stress_strain" / "src" / "results.json").read_text())
L2 = json.loads((LAB.parent / "lab02_axial_thermal" / "src" / "results.json").read_text())

extra = []
appx = H[H.index("## Appendix A"):H.index("## Appendix B")]


def row(label):
    ln = [x for x in appx.splitlines() if x.startswith("| " + label)]
    return ln[0].split("|")[2].strip() if ln else ""


j = lambda v, nd: ", ".join(f"{x:.{nd}f}" for x in v)  # noqa: E731
bm, am, bb, cm = M["bar"], M["A"], M["B"], M["C"]
for label, want in (("Bar $b$ (mm)", j(bm["b_mm"], 2)), ("Bar $h$ (mm)", j(bm["h_mm"], 3)),
                    ("Part A span / indicators / hangers (mm)", f"{am['span_mm']:.1f} / {j(am['gage_x_mm'], 1)} / {j(am['load_x_mm'], 1)}"),
                    ("Part B free length / indicators (mm)", f"{bb['L_mm']:.1f} / {j(bb['gage_x_mm'], 1)}"),
                    ("Part B3 prop lowered by (mm)", f"{bb['settle_mm']:.3f}"), ("Strip $b$ (mm)", j(cm["b_mm"], 2)),
                    ("Strip $t$ (mm)", j(cm["t_mm"], 3)), ("Strip free length by rule (mm)", f"{cm['L_mm']:.1f}")):
    extra.append((f"Appendix A matches measurements JSON: {label}", row(label) == want, f"{row(label)} vs {want}"))
for label, val, phrase in (("rule", M["rule_accuracy_mm"], "rule are good to ±{:g} mm"), ("prop screw", M["prop_screw_accuracy_mm"], "prop screw to ±{:g} mm"),
                           ("grid", M["grid_reading_mm"], "grid readings to ±{:g} mm")):
    extra.append((f"Table A2 caption accuracy matches measurements JSON: {label}", phrase.format(val) in H, phrase.format(val)))
ref = M["reference"]
extra.append(("Table 1 steel E and σ_Y equal the Lab 1 measured values",
              abs(ref["E_st_GPa"] - round(L1["steel_1018HR"]["E"], 1)) < 1e-9 and abs(ref["sY_st_MPa"] - round(L1["steel_1018HR"]["sigY"], 1)) < 1e-9
              and "205.2 ± 1.2 (your Lab 1)" in H and "296.2 ± 1.1 (your Lab 1)" in H))
extra.append(("Table 1 aluminum E (Lab 2) and σ_Y (Lab 1) equal the earlier labs' values",
              abs(ref["E_al_GPa"] - round(L2["A"]["E"], 2)) < 1e-9 and abs(ref["sY_al_MPa"] - round(L1["al_6061T6"]["sigY"], 1)) < 1e-9
              and "68.46 ± 0.47 (your Lab 2)" in H and "273.7 ± 1.0 (your Lab 1)" in H))
extra.append(("simulation materials: steel 205 GPa / 296.2 MPa, 6061-T6 68.9 GPa / 273.7 MPa, spring steel 203 GPa / 1300 MPa",
              "E: 205e9, sY: 296.2e6" in SIM and "E: 68.9e9, sY: 273.7e6" in SIM and "E: 203e9, sY: 1300e6" in SIM))
# D1 catalog: handout Table 6 vs the analysis
cat = re.findall(r'\("(I \d+ × \d+)", ([\d.]+), ([\d.]+), ([\d.]+), ([\d.]+)\)', ANA)
tab6 = H[H.index("| Section | $H$ (mm)"):H.index(": Table 6.")]
ok6 = len(cat) == 7 and all(f"| {n} | {Hh} | {B} | {tf} | {tw} |" in tab6 for n, Hh, B, tf, tw in cat)
extra.append(("D1 catalog: handout Table 6 equals the analysis catalog (7 sections)", ok6, f"{len(cat)} sections in the analysis"))
extra.append(("D1 load case in handout matches the analysis (4.0 m, 2.0 kN/m, 1.5 kN, 0.6 σ_Y, L/360, 2a/360)",
              "D1 = dict(Lt=4.0, w=2.0e3, P=1.5e3, step=0.05, span_lim=360.0, tip_lim=180.0, sa_frac=0.6)" in ANA
              and "4.0 m long" in H and "2.0 kN/m" in H and "1.5 kN railing post" in H and "$L_s/360$" in H and "$2a/360$" in H))
extra.append(("D1 simulation preset is the I 102 × 64 geometry on a 4.0 m beam (not the answer's roller position)",
              "H: 101.6e-3, B: 63.5e-3, tf: 6.4e-3, tw: 4.8e-3, L: 3.5, aov: 0.5, P1: 1500, a1: 4.0, w: 2000" in SIM))
# load limits = largest loads in the sample data
rows = list(csv.DictReader(open(LAB / "sample_data.csv", newline="")))
mx = lambda part, cfg: max(float(r["mass_kg"]) for r in rows if r["part"] == part and r["config"] in cfg)  # noqa: E731
extra.append(("safety load limits equal the largest loads in the procedure and data (3.0, 1.0, 4.0, 0.62 kg)",
              "Part A 3.0 kg on each hanger; Part B 1.0 kg at the tip without the prop and 4.0 kg at mid-length with the prop; Part C 0.62 kg" in H
              and mx("A", ("P600", "P200")) == 3.0 and mx("B", ("cantilever",)) == 1.0 and mx("B", ("propped",)) == 4.0 and mx("C", ("elastica",)) == 0.62))
extra.append(("Part C masses in the procedure equal the data's", "0.04, 0.07, 0.12, 0.17, 0.22, 0.32, 0.42, 0.52 and 0.62 kg" in H
              and [float(r["mass_kg"]) for r in rows if r["part"] == "C"] == [0, 0.02, 0.04, 0.07, 0.12, 0.17, 0.22, 0.32, 0.42, 0.52, 0.62]))
# C++ reference and its convention
cpp = (LAB / "reference" / "beam_deflection.cpp")
extra.append(("instructor's beam_deflection.cpp is shipped in reference/ and included verbatim by the test driver",
              cpp.exists() and '#include "../reference/beam_deflection.cpp"' in (LAB / "tests" / "cpp_driver.cpp").read_text()))
extra.append(("the C++ program's y-down convention is stated in the handout and the simulation",
              "takes $y$ positive downward internally" in H and "works with y downward internally" in SIM))
# Appendix E has the values the Python test re-computes; the key's alpha5 and the handout's 0.68 agree
KV = json.loads((LAB / "src" / "key_values.json").read_text())
a5 = float(KV["C_a5"])
extra.append(("α where Eq. 10 is 5 % high: handout '0.68' and the key's value agree to two decimals", "at $\\alpha \\approx 0.68$" in H and abs(a5 - 0.68) < 0.005, str(a5)))
# the handout's Part B check (about 10 % more than the rigid-clamp estimate) and the key's clamp share
share = float(re.search(r"clamp contributes ([\d.]+) %", K).group(1))
extra.append(("procedure step 3 'about 10 % more' matches the key's clamp share of the tip deflection", 7 <= share / (1 - share / 100) <= 13, f"{share} %"))
extra.append(("P5 tells students the B2 preset opens with a flexible clamp, as the simulation does",
              'it opens with a flexible clamp, $k$ = 4400 N·m/rad' in H and "partB2: P_({ family: 'propped', L: 0.7, P1: 4.0 * 9.80665, a1: 0.35, rigid: false, k: 4400 })" in SIM))

cfg = {
    "n": "07",
    "constants": {
        "Part A: span 800, hangers 200/600, indicators 200/400/600": [("handout", "knife edges 800 mm apart"), ("handout", "indicators at 200, 400 and 600 mm"),
                                                                     ("gen", "A=dict(L=0.8003"), ("sim", "L: 0.8, P1: 3.0 * 9.80665, a1: 0.6"), ("figs", "800")],
        "Part B: free length 700, indicators 350/700, prop 0.5 mm": [("handout", "700 mm free to the tip hanger"), ("handout", "indicators at 350 and 700 mm"),
                                                                    ("handout", "lower the prop by 0.500 mm"), ("gen", "B=dict(L=0.7004"),
                                                                    ("sim", "s: -0.5e-3"), ("figs", "700 mm")],
        "Part C: strip 12.7 × 0.79, 250 mm, 0.62 kg": [("handout", "12.7 × 0.79 mm"), ("handout", "250 mm free"), ("gen", "C=dict(E=203e9, b=12.70e-3, t=0.787e-3, L=0.2504"),
                                                       ("sim", "Ls: 0.25, bs: 12.7e-3, ts: 0.787e-3, Ps: 0.62 * 9.80665")],
        "bar 25.4 × 6.35": [("handout", "25.4 × 6.35"), ("sim", "b: 25.4e-3, h: 6.35e-3"), ("gen", "b=25.43e-3, h=6.362e-3")],
        "D1: 0.6 σ_Y": [("handout", "0.6\\,\\sigma_Y"), ("key", "0.6 × 273.7")],
    },
    "symbols": ["\\delta", "\\theta", "EI", "R_A", "M_A", "\\lambda = EI/(kL)", "\\Delta", "\\alpha = PL^2/EI", "\\beta = wL^3/EI", "\\theta_0",
                "\\delta_v", "\\delta_h", "K", "F", "E(\\cdot)", "c"],
    "csv_columns": ["part", "config", "step", "mass_kg", "load_pos_mm", "d1_mm", "d2_mm", "d3_mm", "R_N", "x_tip_mm", "y_tip_mm"],
    "sign_phrases": {"handout": ["Deflection $y$ is positive **upward**", "$EI\\,d^2y/dx^2 = M$ (Eq. 9.4)", "an applied couple is positive counterclockwise",
                                 "Reaction forces are positive upward, reaction couples positive counterclockwise", "Tension is positive"],
                     "sim": ["deflection y is positive upward and EI y″ = M (Eq. 9.4)", "an applied couple C is positive counterclockwise",
                             "Reactions: forces positive upward, couples positive counterclockwise"],
                     "key": ["$y$ up, $EI\\,y'' = M$, $M > 0$ sags"]},
    "extra": extra,
}
sys.exit(run(LAB, cfg))

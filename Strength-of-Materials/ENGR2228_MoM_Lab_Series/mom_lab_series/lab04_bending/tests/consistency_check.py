"""Cross-file consistency for Lab 4: units, symbols, sign convention, constants, references.

    python3 tests/consistency_check.py      (from lab04_bending/)
"""
import json
import sys
from pathlib import Path

LAB = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LAB.parent / "shared"))
sys.path.insert(0, str(LAB / "src"))
from consistency import run  # noqa: E402
from lab04_analysis import CATALOG  # noqa: E402

H = (LAB / "src" / "lab04_handout.md").read_text(encoding="utf-8")
K = (LAB / "src" / "lab04_instructor_key.md").read_text(encoding="utf-8")
SIM = (LAB / "lab04_simulation.html").read_text(encoding="utf-8")
M = json.loads((LAB / "src" / "specimen_measurements.json").read_text())
L1 = json.loads((LAB.parent / "lab01_stress_strain" / "src" / "results.json").read_text())
L2 = json.loads((LAB.parent / "lab02_axial_thermal" / "src" / "results.json").read_text())

extra = []
appx = H[H.index("## Appendix A"):H.index("## Appendix B")]


def row(label):
    ln = [x for x in appx.splitlines() if x.startswith("| " + label)]
    return ln[0].split("|")[2].strip() if ln else ""


for label, key, nd in (("Bar A width $b$ (mm)", "b_mm", 2), ("Bar A depth $h$ (mm)", "h_mm", 2), ("Bar B strip thickness $t_s$ (mm)", "ts_mm", 2),
                       ("Bar A side gages $y_h$ (mm)", "yA_mm", 2), ("Bar B side gages $y_h$ (mm)", "yB_mm", 2)):
    want = ", ".join(f"{v:.{nd}f}" for v in M[key])
    extra.append((f"Appendix A readings match measurements JSON: {key}", row(label) == want, f"{row(label)} vs {want}"))
extra.append(("Appendix A span and load rollers match JSON", row("Span / load rollers from left support (mm)") == f"{M['span_mm']:.1f} / {M['a1_mm']:.1f}, {M['a2_mm']:.1f}"))
extra.append(("Appendix A straightedge gap matches JSON", row("Straightedge gap at midspan after Part C, bar resting on its ends (mm)") == f"{M['straightedge_gap_mm']:.2f}"))
extra.append(("Appendix A bar length matches JSON", row("Bar A length (mm)") == f"{M['bar_length_mm']:.0f}"))
ref = M["reference"]
extra.append(("Table 1 aluminum E and ν equal the Lab 2 measured values (carried forward)",
              abs(ref["E_al_GPa"] - round(L2["A"]["E"], 2)) < 1e-9 and abs(ref["nu_al"] - round(L2["A"]["nu"], 3)) < 1e-9
              and "68.46 ± 0.47 (your Lab 2)" in H and "0.330 ± 0.003 (your Lab 2)" in H, f"Lab 2: E = {L2['A']['E']:.3f}, ν = {L2['A']['nu']:.4f}"))
extra.append(("Table 1 yield strengths equal the Lab 1 measured values (carried forward)",
              abs(ref["sY_al_MPa"] - round(L1["al_6061T6"]["sigY"], 1)) < 1e-9 and abs(ref["u_sY_al_MPa"] - round(L1["al_6061T6"]["uY"], 1)) < 1e-9
              and abs(ref["sY_st_MPa"] - round(L1["steel_1018HR"]["sig_ly"], 1)) < 1e-9 and abs(ref["u_sY_st_MPa"] - round(L1["steel_1018HR"]["u_ly"], 1)) < 1e-9
              and "273.7 ± 1.0" in H and "296.2 ± 1.1" in H))
extra.append(("steel E = 205 GPa as in Labs 1–3", "| 205 ± 3 |" in H and ref["E_st_GPa"] == 205.0 and "E: 205e9" in SIM))
extra.append(("simulation 6061-T6 curve = Lab 1 truth family (E 68.9 GPa, σ_Y 274 MPa, m 17)", "E: 68.9e9, law: 'ro', sY: 274e6, m: 17" in SIM))
cat_ok = []
for name, kind, h, b, t, tw in CATALOG:
    ln = [x for x in H.splitlines() if x.startswith(f"| {name} |")]
    cat_ok.append(bool(ln) and f"{h} × {b}" in ln[0] and f"| {t:.1f} |" in ln[0])
extra.append(("Table 6 catalog dimensions match the analysis catalog", all(cat_ok), str(cat_ok)))
extra.append(("no hogging-positive or compression-positive statement", "hogging is positive" not in (H + K + SIM).lower() and "compression positive" not in (H + K + SIM).lower()))
extra.append(("sign of the flexure formula: σ = −My/I in handout, key and simulation", "\\sigma_x = -\\frac{My}{I}" in H and "\\sigma_x = -My/I" in K and "−My/I" in SIM))

cfg = {
    "n": "04",
    "constants": {
        "span 600 mm": [("handout", "600 mm"), ("sim", "L: 0.600"), ("gen", "L=600.0e-3"), ("figs", "span L = 600 mm")],
        "shear span a = 200 mm": [("handout", "$a$ = 200 mm"), ("sim", "a: 0.200"), ("figs", "a = 200 mm")],
        "bar 25.4 × 50.8 mm": [("handout", "25.4 × 50.8"), ("sim", "b: 25.4e-3, h: 50.8e-3"), ("figs", "25.4 × 50.8")],
        "steel strip 6.35 mm": [("handout", "6.35 mm"), ("sim", "ts: 6.35e-3"), ("figs", "6.35 mm steel")],
        "bottom gages at x = 100, 150 mm": [("handout", "$x$ = 100 and 150 mm"), ("gen", "x_bottom=[100.0e-3, 150.0e-3]"), ("figs", "x = 100, 150 mm")],
        "load limits 20/15/40 kN, stops 22/17/42 kN": [("handout", "at 22 kN for Part A, 17 kN for Part B and 42 kN for Part C"),
                                                     ("handout", "do not exceed 20, 15 and 40 kN"), ("gen", "37e3, 40e3]"), ("sim", "P: 40e3")],
        "D1: 3.0 m, 3.0 kN/m, 5.0 kN, FS 1.67, L/240": [("handout", "spans 3.0 m"), ("handout", "3.0 kN/m"), ("handout", "5.0 kN point load"),
                                                      ("handout", "at least 1.67"), ("handout", "$L/240$")],
    },
    "symbols": ["\\kappa", "y_{NA}", "y_h", "I_t", "\\bar y", "M_Y", "\\kappa_Y", "M_p", "Z$", "S = I/c", "\\kappa_p", "\\sigma_{res}", "\\rho'",
                "n = E_2/E_1", "t_s", "y_Y", "\\varepsilon_z", "\\nu"],
    "csv_columns": ["part", "step", "load_N", "strain_side1_ue", "strain_side2_ue", "strain_side3_ue", "strain_side4_ue", "strain_side5_ue",
                    "strain_top_ue", "strain_bottom_ue", "strain_transverse_top_ue", "strain_bottom_x100_ue", "strain_bottom_x150_ue"],
    "sign_phrases": {"handout": ["$dV/dx = -w$", "**counterclockwise**", "$\\sigma_x = -My/I$"],
                     "sim": ["dV/dx = −w", "counterclockwise", "σ<sub>x</sub> = −My/I"]},
    "extra": extra,
}
sys.exit(run(LAB, cfg))

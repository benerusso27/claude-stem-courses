"""Cross-file consistency for Lab 6: units, symbols, sign convention, constants, references.

    python3 tests/consistency_check.py      (from lab06_eccentric/)
"""
import json
import sys
from pathlib import Path

LAB = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LAB.parent / "shared"))
from consistency import run  # noqa: E402

H = (LAB / "src" / "lab06_handout.md").read_text(encoding="utf-8")
K = (LAB / "src" / "lab06_instructor_key.md").read_text(encoding="utf-8")
SIM = (LAB / "lab06_simulation.html").read_text(encoding="utf-8")
M = json.loads((LAB / "src" / "specimen_measurements.json").read_text())
L1 = json.loads((LAB.parent / "lab01_stress_strain" / "src" / "results.json").read_text())
L2 = json.loads((LAB.parent / "lab02_axial_thermal" / "src" / "results.json").read_text())

extra = []
appx = H[H.index("## Appendix A"):H.index("## Appendix B")]


def row(label):
    ln = [x for x in appx.splitlines() if x.startswith("| " + label)]
    return ln[0].split("|")[2].strip() if ln else ""


j = lambda v, nd: ", ".join(f"{x:.{nd}f}".replace("-", "−") for x in v)  # noqa: E731
bm, am = M["bar"], M["angle"]
for label, want in (("Bar $h$ / $b$ (mm)", f"{j(bm['h_mm'], 2)} / {j(bm['b_mm'], 3)}"), ("Bar $L$ / $a$ (mm)", f"{bm['L_mm']:.1f} / {bm['a_mm']:.1f}"),
                    ("Hole offsets $e$: e0, e1, e2 / ez (mm)", f"{j([bm['yP_mm'][c] for c in ('e0', 'e1', 'e2')], 2)} / {bm['zP_mm']['ez']:.2f} (through the thickness)"),
                    ("Gage heights $y$, front (mm)", j(bm["y_front_mm"], 1)), ("Gage heights $y$, back (mm)", j(bm["y_back_mm"], 1)),
                    ("End pair, distance from the block face (mm)", f"{bm['x_end_mm']:.1f}"),
                    ("Angle legs $b_V$ / $b_H$ (mm)", f"{j(am['bV_mm'], 2)} / {j(am['bH_mm'], 2)}"), ("Angle thickness $t$ (mm)", j(am["t_mm"], 3)),
                    ("Angle root-fillet radius (mm)", f"{am['r_mm']:.1f}"), ("Angle $L$ / $a$ (mm)", f"{am['L_mm']:.1f} / {am['a_mm']:.1f}"),
                    ("Angle load point from the heel, $z$ / $y$ (mm)", f"{am['load_z_mm']:.2f} / {am['load_y_mm']:.2f}".replace("-", "−")),
                    ("G1, G2 ($z$ = 0) heights $y$ / G3, G4 ($y$ = 0) positions $z$ (mm)",
                     f"{j([am['gages_mm'][g]['y'] for g in ('G1', 'G2')], 1)} / {j([am['gages_mm'][g]['z'] for g in ('G3', 'G4')], 1)}")):
    extra.append((f"Appendix A matches measurements JSON: {label}", row(label) == want, f"{row(label)} vs {want}"))
ref = M["reference"]
extra.append(("Table 1 E equals the Lab 2 measured value", abs(ref["E_al_GPa"] - round(L2["A"]["E"], 2)) < 1e-9 and "68.46 ± 0.47 (your Lab 2)" in H))
extra.append(("Table 1 σ_Y equals the Lab 1 measured value", abs(ref["sY_al_MPa"] - round(L1["al_6061T6"]["sigY"], 1)) < 1e-9 and "273.7 ± 1.0 (your Lab 1)" in H))
extra.append(("simulation 6061-T6: E = 68.9 GPa (series truth value), σ_Y = Lab 1 value", "E: 68.9e9, sY: 273.7e6" in SIM))
extra.append(("Lab 8 tube in X2 matches the simulation preset (D_o 38.1, D_i 31.75, F 600 N, L_b 250, a_L 200)",
              "Do: 38.1e-3, Di: 31.75e-3, F: 600, Lb: 0.25, aL: 0.2" in SIM and "$D_o$ = 38.10 mm and $D_i$ = 31.75 mm, loaded by $F$ = 600 N at the end of a 200 mm lever arm, with the gage section 250 mm from the lever" in H))
extra.append(("D1 catalog: gage and thickness in the handout match the analysis catalog",
              all(s in H for s in ("| L51 × 51 × 6.4 | 51 | 6.35 | 28.6 |", "| L64 × 64 × 6.4 | 64 | 6.35 | 34.9 |", "| L76 × 51 × 6.4 | 76 or 51 | 6.35 | 44.5 or 28.6 |"))))
extra.append(("z points left in section views: stated in handout, simulation and figures",
              "z$ points to the **left**" in H and "z points to the left" in SIM and "z to the LEFT" in (LAB / "src" / "make_figures.py").read_text()))

cfg = {
    "n": "06",
    "constants": {
        "bar 50.8 × 12.7, L = 250, a = 25": [("handout", "50.8 × 12.7 mm"), ("handout", "the free length between them is 250 mm"), ("gen", "h=50.83e-3, b=12.68e-3, L=0.250, a=0.025"),
                                             ("sim", "h: 50.8e-3, b: 12.7e-3, P: 25e3, ey: 0, ez: 6.40e-3, L: 0.25, a: 0.025"), ("figs", "L = 250 mm")],
        "holes 0, h/6, h/3, b/2": [("handout", "in-plane offsets 0, 8.47 and 16.93 mm"), ("handout", "one offset 6.35 mm ($b/2$)"), ("sim", "ey: 8.49e-3"), ("sim", "ey: 16.95e-3")],
        "load limits 30 / 30 / 25 kN": [("handout", "Part A 30 kN in every hole; Part B 30 kN; Part C 25 kN"), ("gen", "25e3, 30e3, 0]"), ("gen", "20e3, 25e3, 0]")],
        "angle 50.8 × 50.8 × 6.35, gusset 9.53, gage 28.6, L 300": [("handout", "50.8 × 50.8 × 6.35 mm"), ("handout", "9.53 mm steel plate"), ("handout", "28.6 mm from the heel"),
                                                                    ("sim", "bV: 50.8e-3, bH: 50.8e-3, t: 6.35e-3, r: 0, P: 30e3, lz: -28.58e-3, ly: -4.76e-3, L: 0.3"),
                                                                    ("figs", "g = 28.6"), ("figs", "4.76")],
        "D1: 40 kN, 1.50 m, 75 mm, 0.6 σ_Y": [("handout", "$T$ = 40 kN"), ("handout", "1.50 m"), ("handout", "rigid block 75 mm long"), ("handout", "0.6\\,\\sigma_Y"),
                                               ("sim", "P: 40e3, lz: -44.5e-3, ly: -4.765e-3, L: 1.5, a: 0.075")],
    },
    "symbols": ["y_P", "z_P", "M_y", "M_z", "I_{yz}", "\\theta_p", "r_z^2", "y_0", "C = M/(Pe)", "P_{cr}", "e_{eff}", "\\varepsilon_b", "k = \\sqrt{P/EI}"],
    "csv_columns": ["part", "config", "step", "load_N", "w_mid_mm"] + [f"g{k:02d}_ue" for k in range(1, 13)],
    "sign_phrases": {"handout": ["$M_y = P z_P$ and $M_z = -P y_P$", "Tension is positive", "**toward the load line**"],
                     "sim": ["M<sub>y</sub> = P z<sub>P</sub> and M<sub>z</sub> = −P y<sub>P</sub>", "Tension positive", "toward the load line"]},
    "extra": extra,
}
sys.exit(run(LAB, cfg))

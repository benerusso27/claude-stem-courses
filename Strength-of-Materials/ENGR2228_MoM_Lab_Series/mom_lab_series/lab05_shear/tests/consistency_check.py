"""Cross-file consistency for Lab 5: units, symbols, sign convention, constants, references.

    python3 tests/consistency_check.py      (from lab05_shear/)
"""
import json
import sys
from pathlib import Path

LAB = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LAB.parent / "shared"))
from consistency import run  # noqa: E402

H = (LAB / "src" / "lab05_handout.md").read_text(encoding="utf-8")
K = (LAB / "src" / "lab05_instructor_key.md").read_text(encoding="utf-8")
SIM = (LAB / "lab05_simulation.html").read_text(encoding="utf-8")
M = json.loads((LAB / "src" / "specimen_measurements.json").read_text())
L1 = json.loads((LAB.parent / "lab01_stress_strain" / "src" / "results.json").read_text())
L2 = json.loads((LAB.parent / "lab02_axial_thermal" / "src" / "results.json").read_text())
L3 = json.loads((LAB.parent / "lab03_torsion" / "src" / "results.json").read_text())
L4M = json.loads((LAB.parent / "lab04_bending" / "src" / "specimen_measurements.json").read_text())

extra = []
appx = H[H.index("## Appendix A"):H.index("## Appendix B")]


def row(label):
    ln = [x for x in appx.splitlines() if x.startswith("| " + label)]
    return ln[0].split("|")[2].strip() if ln else ""


j = lambda v, nd: ", ".join(f"{x:.{nd}f}" for x in v)  # noqa: E731
ib, ly, ba = M["ibeam"], M["layered"], M["barA"]
for label, want in (("Bar A $b$ / $h$ (mm)", f"{j(ba['b_mm'], 2)} / {j(ba['h_mm'], 2)}"),
                    ("Part A span / gage station from the left support (mm)", f"{ba['span_mm']:.1f} / {ba['x_gage_mm']:.1f}"),
                    ("I-beam $H$ (mm)", j(ib["H_mm"], 2)), ("I-beam $B$ (mm)", j(ib["B_mm"], 2)), ("I-beam $t_f$ (mm)", j(ib["tf_mm"], 2)),
                    ("I-beam $t_w$ (mm)", j(ib["tw_mm"], 3)), ("Web gage heights above the bottom (mm)", j(ib["gage_height_mm"], 2)),
                    ("Part B web span / gage station (mm)", f"{ib['span_web_mm']:.1f} / {ib['x_gage_mm']:.1f}"),
                    ("Part C bars $b$ (mm)", j(ly["b_mm"], 2)), ("Part C top bar / bottom bar $t$ (mm)", f"{j(ly['t_top_mm'], 2)} / {j(ly['t_bot_mm'], 2)}"),
                    ("Part C span / bolt positions from the left support (mm)", f"{ly['span_mm']:.1f} / " + ", ".join(f"{x:.0f}" for x in ly["bolts_mm"]))):
    extra.append((f"Appendix A matches measurements JSON: {label}", row(label) == want, f"{row(label)} vs {want}"))
extra.append(("Part A bar is the Lab 4 bar (same caliper readings)", ba["b_mm"] == L4M["b_mm"] and ba["h_mm"] == L4M["h_mm"]))
ref = M["reference"]
extra.append(("Table 1 E and ν equal the Lab 2 measured values", abs(ref["E_al_GPa"] - round(L2["A"]["E"], 2)) < 1e-9 and abs(ref["nu_al"] - round(L2["A"]["nu"], 3)) < 1e-9
              and "68.46 ± 0.47 (your Lab 2)" in H and "0.330 ± 0.003 (your Lab 2)" in H))
extra.append(("Table 1 G and τ_Y equal the Lab 3 measured values (aluminum)", abs(ref["G_al_GPa"] - round(L3["al"]["G_GPa"], 2)) < 1e-9
              and abs(ref["u_G_al_GPa"] - round(L3["al"]["uG_GPa"], 2)) < 1e-9 and abs(ref["tauY_al_MPa"] - round(L3["al"]["tauY_MPa"], 1)) < 1e-9
              and "26.03 ± 0.12 (your Lab 3)" in H))
extra.append(("Table 1 σ_Y equals the Lab 1 measured value", abs(ref["sY_al_MPa"] - round(L1["al_6061T6"]["sigY"], 1)) < 1e-9 and "273.7 ± 1.0" in H))
extra.append(("simulation 6061-T6: E = 68.9 GPa, ν = 0.33 (series truth values)", "E: 68.9e9, nu: 0.33" in SIM))
extra.append(("no statement that τ_xy is positive for positive V", "positive v gives positive" not in (H + K + SIM).lower()))

cfg = {
    "n": "05",
    "constants": {
        "Part A span 400 mm, gage at 100 mm": [("handout", "400.0 mm"), ("gen", "L=0.400, xg=0.100"), ("figs", "400 mm")],
        "Part A loads 15 / 7.5 kN": [("handout", "upright 15 kN, flat 7.5 kN"), ("gen", "12.5e3, 15e3, 0]"), ("gen", "6.25e3, 7.5e3, 0]"), ("sim", "V: 7.5e3"), ("sim", "V: 3.75e3")],
        "I-beam 101.6 × 76.2 × 6.35": [("handout", "$H$ = 101.6 mm, $B$ = 76.2 mm, $t_f$ = 6.35 mm"), ("sim", "B: 76.2e-3, H: 101.6e-3, tf: 6.35e-3"), ("gen", "B=76.20e-3, H=101.60e-3, tf=6.35e-3")],
        "spans 300–1200 mm": [("handout", "300, 450, 600, 900 and 1200 mm"), ("gen", "spans=[0.300, 0.450, 0.600, 0.900, 1.200]"), ("figs", "span L = 300–1200 mm")],
        "Part C bars 50.8 × 12.7, span 600, bolts at 100 mm": [("handout", "50.8 × 12.7"), ("handout", "at 100 mm spacing"), ("sim", "t1: 12.7e-3, t2: 12.7e-3, L: 0.6"),
                                                               ("gen", "bolts=[0.05, 0.15, 0.25, 0.35, 0.45, 0.55]"), ("figs", "600 mm")],
        "Part C load limits 2.0 / 2.5 / 4.0 kN": [("handout", "2.0 kN loose, 2.5 kN bolted, 4.0 kN bonded"), ("gen", "[0, 500, 1000, 1500, 2000, 2500, 0]")],
        "D1: 2.4 m, 8.0 kN/m, 10 kN per bolt, L/300, M10 = 10/6 M6": [("handout", "spanning 2.4 m"), ("handout", "8.0 kN/m"), ("handout", "no more than 10 kN"),
                                                                   ("handout", "$L/300$"), ("handout", "$(10/6)$"), ("sim", "L: 2.4, load: 'udl', w: 8e3")],
    },
    "symbols": ["Q$", "q$", "\\tau", "\\gamma", "A_w", "f_s", "R$", "k_b", "EI_0", "EI_{full}", "EA^*", "\\eta", "\\alpha", "\\beta", "t_w", "t_f"],
    "csv_columns": ["part", "config", "span_mm", "step", "load_N", "defl_mm", "slip_mm", "gA_p45_ue", "gA_m45_ue", "gB_p45_ue", "gB_m45_ue",
                    "gC_p45_ue", "gC_m45_ue", "gD_p45_ue", "gD_m45_ue", "gE_p45_ue", "gE_m45_ue", "gF_p45_ue", "gF_m45_ue"],
    "sign_phrases": {"handout": ["$V = -\\int \\tau_{xy}\\,dA$", "**downward**" if "**downward**" in H else "downward", "Deflection $y$ is positive upward"],
                     "sim": ["V = −∫τ<sub>xy</sub> dA", "counterclockwise", "Deflection y is positive upward"]},
    "extra": extra,
}
sys.exit(run(LAB, cfg))

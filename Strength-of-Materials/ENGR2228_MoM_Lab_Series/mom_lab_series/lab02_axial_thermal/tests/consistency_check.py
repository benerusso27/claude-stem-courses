"""Cross-file consistency for Lab 2: units, symbols, sign convention, constants, references.

    python3 tests/consistency_check.py      (from lab02_axial_thermal/)
"""
import json
import sys
from pathlib import Path

LAB = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LAB.parent / "shared"))
from consistency import run  # noqa: E402

H = (LAB / "src" / "lab02_handout.md").read_text(encoding="utf-8")
K = (LAB / "src" / "lab02_instructor_key.md").read_text(encoding="utf-8")
SIM = (LAB / "lab02_simulation.html").read_text(encoding="utf-8")
FIGS = (LAB / "src" / "make_figures.py").read_text(encoding="utf-8")
M = json.loads((LAB / "src" / "specimen_measurements.json").read_text())

extra = []


def row(label):
    appx = H[H.index("## Appendix A"):H.index("## Appendix B")]
    lines = [ln for ln in appx.splitlines() if ln.startswith("| " + label)]
    return lines[0].split("|")[2].strip() if lines else ""


fmt = lambda v: ", ".join(f"{x:.2f}" for x in v)  # noqa: E731
for label, key in (("Part A width", "A_width_mm"), ("Part A thickness", "A_thickness_mm"), ("Part B rod diameter (mm)", "B_rod_d_mm"),
                   ("Part B tube outer diameter (mm)", "B_tube_do_mm"), ("Part B tube inner diameter (mm)", "B_tube_di_mm"),
                   ("Part C bolt shank diameter (mm)", "C_bolt_d_mm"), ("Part C sleeve outer diameter (mm)", "C_sleeve_do_mm"),
                   ("Part C sleeve inner diameter (mm)", "C_sleeve_di_mm")):
    extra.append((f"Appendix A readings match measurements JSON: {label}", row(label) == fmt(M[key]), f"{row(label)} vs {fmt(M[key])}"))
extra.append(("Appendix A rod/tube lengths match JSON", row("Part B rod length / tube length") == f"{M['B_rod_L_mm']:.2f} / {M['B_tube_L_mm']:.2f}",
              row("Part B rod length / tube length")))
extra.append(("Figure 3 example (brass rod 16 mm, steel tube 30×24 mm, g = 0.12 mm) matches handout text",
              "np.pi / 4 * 16 ** 2" in FIGS and "(30 ** 2 - 24 ** 2)" in FIGS and "200.0, 0.12" in FIGS and "$g$ = 0.12 mm" in H))
extra.append(("material E and α identical in handout Table 1, simulation and analysis reference values",
              "| 205 ± 3 |" in H and "E: 205e9, alpha: 11.7e-6" in SIM and "E: 68.9e9, alpha: 23.6e-6" in SIM
              and M["handbook"]["E_st_GPa"] == 205.0 and M["handbook"]["alpha_al"] == 23.6e-6 and M["handbook"]["alpha_st"] == 11.7e-6))
extra.append(("steel modulus matches Lab 1 (205 GPa) across the series",
              "E: 205e9" in (LAB.parent / "lab01_stress_strain" / "lab01_simulation.html").read_text(encoding="utf-8")))
extra.append(("no compression-positive statement anywhere", "compression positive" not in (H + K + SIM).lower()))

cfg = {
    "n": "02",
    "constants": {
        "Part A bar 25.40 mm × 6.35 mm": [("handout", "25.40 mm × 6.35 mm"), ("gen", "A_b=25.40e-3, A_t=6.35e-3")],
        "Part B rod d = 12.70 mm, L = 150 mm": [("handout", "$d$ = 12.70 mm"), ("handout", "150.00 mm"), ("sim", "d1: 12.70e-3"), ("sim", "L: 0.150"),
                                              ("gen", "B_rod_d=12.70e-3"), ("gen", "B_L=150.00e-3")],
        "Part B tube 25.40 × 19.05 mm": [("handout", "25.40 mm × 19.05 mm"), ("sim", "do: 25.40e-3, di: 19.05e-3"), ("gen", "B_tube_do=25.40e-3, B_tube_di=19.05e-3")],
        "Part B gap 0.040 mm": [("handout", "$g$ = 0.040 mm"), ("sim", "g: 40e-6"), ("gen", "gap=40e-6")],
        "Part C bolt 10.00 mm, sleeve 20.00 × 10.50 mm, L = 100 mm": [("handout", "20.00 mm × 10.50 mm"), ("sim", "d1: 10.00e-3, do: 20.00e-3, di: 10.50e-3, L: 0.100"),
                                                                     ("gen", "C_bolt_d=10.00e-3, C_sleeve_do=20.00e-3, C_sleeve_di=10.50e-3, C_L=100.0e-3")],
        "Part C preload 2.0 kN (124 µε)": [("handout", "2.0 kN"), ("handout", "124 µε"), ("sim", "F0: 2000"), ("gen", "preload=2.0e3"), ("key", "2.0 set")],
        "load limits 18 kN and 30 kN": [("handout", "Part A at most 18 kN"), ("handout", "Part B at most 30 kN"), ("gen", "np.arange(0, 18001, 2000)"),
                                        ("gen", "np.arange(0, 30001, 2000)")],
        "bath 20 → 80 °C": [("handout", "do not exceed 80 °C"), ("gen", "np.arange(20, 81, 5)"), ("figs", "20 → 80 °C")],
        "gage factor 2.10 ± 1 %": [("handout", "gage factor 2.10 ± 1 %")],
    },
    "symbols": ["k_i", "f_i", "P_{gap}", "\\beta", "C$", "\\Delta$", "F_0", "GF", "P_B", "d_a", "\\varepsilon_y", "\\alpha_b", "s$", "G$", "\\nu"],
    "csv_columns": ["part", "step", "temperature_C", "load_N", "strain_axial_front_ue", "strain_axial_back_ue", "strain_transverse_front_ue",
                    "strain_transverse_back_ue", "strain_tube_front_ue", "strain_tube_back_ue", "dial_mm", "strain_bolt_ue"],
    "sign_phrases": {"handout": ["Tension is positive", "positive **magnitude**", "$g < 0$ is an interference"],
                     "sim": ["tension positive", "compressive magnitude"]},
    "extra": extra,
}
sys.exit(run(LAB, cfg))

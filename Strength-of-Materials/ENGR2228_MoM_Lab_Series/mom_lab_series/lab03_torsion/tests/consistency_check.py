"""Cross-file consistency for Lab 3: units, symbols, sign convention, constants, references.

    python3 tests/consistency_check.py      (from lab03_torsion/)
"""
import json
import sys
from pathlib import Path

LAB = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LAB.parent / "shared"))
from consistency import run  # noqa: E402

H = (LAB / "src" / "lab03_handout.md").read_text(encoding="utf-8")
K = (LAB / "src" / "lab03_instructor_key.md").read_text(encoding="utf-8")
SIM = (LAB / "lab03_simulation.html").read_text(encoding="utf-8")
M = json.loads((LAB / "src" / "specimen_measurements.json").read_text())
L2 = json.loads((LAB.parent / "lab02_axial_thermal" / "src" / "results.json").read_text())

extra = []
appx = H[H.index("## Appendix A"):H.index("## Appendix B")]


def row(label):
    ln = [x for x in appx.splitlines() if x.startswith("| " + label)]
    return ln[0].split("|")[2].strip() if ln else ""


for label, key in (("Steel $d$ (mm)", "steel"), ("Aluminum $d$ (mm)", "al"), ("Cast iron $d$ (mm)", "ci")):
    want = ", ".join(f"{v:.3f}" for v in M["d_mm"][key])
    extra.append((f"Appendix A readings match measurements JSON: {key}", row(label) == want, f"{row(label)} vs {want}"))
extra.append(("Appendix A gage and reduced lengths match JSON", row("Gage length $L$ / reduced length $L_c$ (mm)") == f"{M['L_gage_mm']:.2f} / {M['L_reduced_mm']:.2f}"))
ref = M["reference"]
extra.append(("Table 1 aluminum E and ν equal the Lab 2 measured values (carried forward)",
              abs(ref["E_al_GPa"] - round(L2["A"]["E"], 2)) < 1e-9 and abs(ref["nu_al"] - round(L2["A"]["nu"], 3)) < 1e-9
              and "68.46 ± 0.47 (your Lab 2)" in H and "0.330 ± 0.003 (your Lab 2)" in H, f"Lab 2: E = {L2['A']['E']:.3f}, ν = {L2['A']['nu']:.4f}"))
extra.append(("Table 1 aluminum uncertainties equal Lab 2's standard uncertainties",
              abs(ref["u_E_al_GPa"] - round(L2["A"]["uE"], 2)) < 1e-9 and abs(ref["u_nu_al"] - round(L2["A"]["unu"], 3)) < 1e-9))
extra.append(("steel E = 205 GPa as in Labs 1 and 2", "| 205 ± 3 |" in H and ref["E_steel_GPa"] == 205.0))
extra.append(("simulation steel G ≈ E/(2(1 + ν)) with series values (79.5 GPa)", "G: 79.5e9" in SIM and abs(205 / 2.58 - 79.5) < 0.05))
extra.append(("no compression-positive or clockwise-positive torque statement", "clockwise is positive" not in (H + K + SIM).lower()))

cfg = {
    "n": "03",
    "constants": {
        "specimen d = 6.35 mm": [("handout", "$d$ = 6.35 mm"), ("sim", "d: 6.35e-3"), ("figs", "d = 6.35 mm")],
        "gage length 50.8 mm": [("handout", "50.80"), ("sim", "L: 50.8e-3"), ("gen", "L_GAGE, L_RED = 50.80e-3, 76.20e-3"), ("figs", "L = 50.8 mm")],
        "reduced length 76.2 mm": [("handout", "$L_c$ = 76.2 mm"), ("figs", "reduced section 76.2 mm")],
        "troptometer removed at 10°": [("handout", "10° on the gage"), ("gen", "tropt_off_deg=10.0"), ("sim", "phi: 10 * Math.PI / 180")],
        "head rates 0.25°/s and 15°/s": [("handout", "0.25°/s"), ("handout", "15°/s"), ("gen", "RATE_SLOW, RATE_FAST = 0.25, 15.0")],
        "machine capacity 60 N·m, stop 40 N·m": [("handout", "capacity is 60 N·m"), ("handout", "overload stop at 40 N·m"), ("key", "40 N·m")],
        "cast iron σ_UT 214 MPa": [("handout", "214 ± 15 MPa"), ("sim", "sigUT: 214e6"), ("gen", "sigUT=214e6")],
        "D1: 15 kW, 1200 rpm, 1.50 m, K = 1.6, FS 2.0, 1.0°": [("handout", "15 kW at 1200 rpm"), ("handout", "1.50 m"), ("handout", "$K$ = 1.6"),
                                                              ("handout", "at least 2.0"), ("handout", "no more than 1.0°")],
    },
    "symbols": ["\\varphi", "\\theta", "J$", "G$", "\\tau_Y", "T_Y", "\\rho_Y", "T_p", "T_U", "R_T", "\\varphi_p", "\\tau_{res}", "L_c", "C_m",
                "\\Delta_{head}", "\\Delta_{toe}", "c_1", "A_m", "\\sigma_{UT}"],
    "csv_columns": ["specimen", "time_s", "torque_Nm", "troptometer_deg", "head_deg"],
    "sign_phrases": {"handout": ["right-hand rule", "points out of the cut section"], "sim": ["right-hand rule", "points out of the cut section"]},
    "extra": extra,
}
sys.exit(run(LAB, cfg))

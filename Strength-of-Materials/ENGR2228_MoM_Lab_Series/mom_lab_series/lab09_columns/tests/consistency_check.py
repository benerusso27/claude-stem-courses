"""Cross-file consistency for Lab 9: units, symbols, sign convention, constants, references.

    python3 tests/consistency_check.py      (from lab09_columns/)
"""
import csv
import json
import math
import re
import sys
from pathlib import Path

LAB = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LAB.parent / "shared"))
from consistency import run  # noqa: E402

H = (LAB / "src" / "lab09_handout.md").read_text(encoding="utf-8")
K = (LAB / "src" / "lab09_instructor_key.md").read_text(encoding="utf-8")
SIM = (LAB / "lab09_simulation.html").read_text(encoding="utf-8")
ANA = (LAB / "src" / "lab09_analysis.py").read_text(encoding="utf-8")
FIGS = (LAB / "src" / "make_figures.py").read_text(encoding="utf-8")
KV = json.loads((LAB / "src" / "key_values.json").read_text())
M = json.loads((LAB / "src" / "specimen_measurements.json").read_text())
L1 = json.loads((LAB.parent / "lab01_stress_strain" / "src" / "results.json").read_text())
L2 = json.loads((LAB.parent / "lab02_axial_thermal" / "src" / "results.json").read_text())
H1 = (LAB.parent / "lab01_stress_strain" / "src" / "lab01_handout.md").read_text(encoding="utf-8")
H2 = (LAB.parent / "lab02_axial_thermal" / "src" / "lab02_handout.md").read_text(encoding="utf-8")
H6 = (LAB.parent / "lab06_eccentric" / "src" / "lab06_handout.md").read_text(encoding="utf-8")
rows = list(csv.DictReader(open(LAB / "sample_data.csv", newline="")))

extra = []
appx = H[H.index("## Appendix A"):H.index("## Appendix B")]


def row(label):
    ln = [x for x in appx.splitlines() if x.startswith("| " + label + " |")]
    return ln[0].split("|")[2].strip() if ln else ""


j = lambda v, nd: ", ".join(f"{x:.{nd}f}" for x in v)  # noqa: E731
Ls, bow = M["lengths_mm"], M["bow_mm"]
for label, want in (("$b$ (mm)", j(M["bar"]["b_mm"], 2)), ("$t$ (mm)", j(M["bar"]["t_mm"], 2)),
                    ("Lengths (mm)", f"A: {Ls['A300']:.1f}, {Ls['A450']:.1f}, {Ls['A600']:.1f}; B: {Ls['Bff']:.1f} (fixed–fixed), {Ls['Bfp']:.1f} (fixed–pinned); D: {Ls['D']:.1f}"),
                    ("Initial bows (mm)", f"A: {bow['A300']:.2f}, {bow['A450']:.2f}, {bow['A600']:.2f}; B: {bow['B']:.2f}; D: {bow['D']:.2f}"),
                    ("Groove offsets (mm)", f"{M['offsets_mm']['C1']:.2f} and {M['offsets_mm']['C2']:.2f}, ±{M['offsets_mm']['tolerance']:.2f}")):
    extra.append((f"Table A2 matches the measurements JSON: {label}", row(label) == want, f"{row(label)} vs {want}"))
for label, phrase in (("micrometer", f"micrometer is good to ±{M['micrometer_accuracy_mm']:g} mm"), ("rule", f"the rule to ±{M['rule_accuracy_mm']:g} mm"),
                      ("dial gage", f"the dial gage to ±{M['dial_accuracy_mm']:g} mm"),
                      ("load cell and UTM", f"the load cell and the UTM to ±{M['loadcell_accuracy_pct']:g} % of reading" if M["loadcell_accuracy_pct"] == M["utm_accuracy_pct"] else "MISMATCH"),
                      ("gage factor", f"the gage factor to ±{M['gage']['GF_tol_pct']:g} %")):
    extra.append((f"Table A2 caption accuracy matches the measurements JSON: {label}", phrase in H, phrase))
# Table 2 (equipment) against the measurements JSON
for label, phrase in (("gage factor", f"Gage factor {M['gage']['GF']:.2f} ± {M['gage']['GF_tol_pct']:g} %"),
                      ("load cell", f"{M['loadcell_capacity_N'] / 1000:g} kN load cell (±{M['loadcell_accuracy_pct']:g} % of reading)"),
                      ("UTM", f"100 kN UTM (±{M['utm_accuracy_pct']:g} % of reading)"),
                      ("grooves", f"at {M['offsets_mm']['C1']:.2f} and {M['offsets_mm']['C2']:.2f} mm from it (±{M['offsets_mm']['tolerance']:.2f} mm)"),
                      ("clamp grip", f"clamp blocks gripping {M['clamp_grip_mm']:g} mm of the bar"),
                      ("Part B bar", f"one {M['bar_B_length_mm']:g} mm bar with gages for Part B"),
                      ("dial", f"Dial gage at mid-length, {M['dial_division_mm']:g} mm divisions, ±{M['dial_accuracy_mm']:g} mm"),
                      ("micrometer and rule", f"Micrometer ±{M['micrometer_accuracy_mm']:g} mm; steel rule ±{M['rule_accuracy_mm']:g} mm")):
    extra.append((f"Table 2 (equipment) matches the measurements JSON: {label}", phrase in H, phrase))
extra.append(("Part B geometry: 680 mm bar − 2 × 40 mm grip = 600 mm free length (procedure, JSON, data)",
              M["bar_B_length_mm"] - 2 * M["clamp_grip_mm"] == 600 and "40 mm at each end (600 mm free length)" in H
              and abs(Ls["Bff"] - 600) <= 1.0))
# Table 1 = earlier labs' results; this bar stock is Lab 2's
ref = M["reference"]
extra.append(("Table 1: E equals the Lab 2 result (68.46 ± 0.47 GPa)", abs(ref["E_al_GPa"] - round(L2["A"]["E"], 2)) < 1e-9 and abs(ref["u_E_al_GPa"] - round(L2["A"]["uE"], 2)) < 1e-9
              and f"{ref['E_al_GPa']:.2f} ± {ref['u_E_al_GPa']:.2f} (your Lab 2)" in H))
extra.append(("Table 1: σ_Y equals the Lab 1 result for 6061-T6 (273.7 ± 1.0 MPa)", abs(ref["sY_al_MPa"] - round(L1["al_6061T6"]["sigY"], 1)) < 1e-9
              and abs(ref["u_sY_al_MPa"] - round(L1["al_6061T6"]["uY"], 1)) < 1e-9 and "273.7 ± 1.0 (your Lab 1)" in H))
extra.append(("Table 1: m = 17 is a fit to the Lab 1 curve, and D.7 says how to fit it", ref["m_RO"] == 17 and "17 (fit to the Lab 1 curve, Appendix D.7)" in H
              and "*Fitting $m$:*" in H and "6061-T6" in H1))
extra.append(("bar stock: 25.4 × 6.35 mm 6061-T6, the Lab 2 bar (Lab 2 measured b 25.40, t 6.35)", abs(L2["A"]["b"] - 25.40) < 0.01 and abs(L2["A"]["t"] - 6.35) < 0.01
              and "25.40" in H2 and "Lab 2 measured this same bar stock" in H))
extra.append(("kern t/6 = 1.06 mm (Lab 6 reference)", abs(6.35 / 6 - 1.06) < 0.005 and "$r^2/c = t/6$ = 1.06 mm, the edge of the section's kern (Lab 6)" in H and "kern" in H6))
extra.append(("simulation 6061-T6: E = 68.9 GPa (series truth), σ_Y and m equal Table 1; steel σ_Y = Lab 1",
              "al: { name: '6061-T6 aluminum', E: 68.9e9, sY: 273.7e6, m: 17" in SIM and f"sY: {round(L1['steel_1018HR']['sigY'], 1)}e6" in SIM))
# D1 catalog, requirements and simulation presets
m = re.search(r"CATALOG = \[\(Do, t\) for Do in \(([^)]*)\) for t in \(([^)]*)\)\]", ANA)
cD = [float(x) for x in m.group(1).split(",")]
cT = [float(x) for x in m.group(2).split(",")]
tD = [float(x) for x in re.search(r"Outside diameter \$D_o\$ \(mm\) \| ([\d., ]+) \|", H).group(1).split(",")]
tT = [float(x) for x in re.search(r"Wall thickness \$t\$ \(mm\) \| ([\d., ]+) \|", H).group(1).split(",")]
extra.append(("D1 catalog: handout Table 6 equals the analysis catalog (5 diameters × 4 walls = 20 tubes)", cD == tD and cT == tT and "every combination, 20 tubes" in H, f"{tD} × {tT}"))
extra.append(("D1 requirements in the handout match the analysis (2.0 m, 12 kN, e 2 mm, 1.95, D/t 40, 76.2 mm)",
              'D1 = dict(L=2.0, P=12e3, e=2e-3, FS=1.95, Dt_max=40.0, OD_max=76.2)' in ANA and "2.0 m long between the bolts" in H and "service load of 12 kN" in H
              and "up to 2 mm off the tube's axis" in H and "at least 1.95 times the service load" in H and "$D_o/t$ at most 40" in H and "at most 76.2 mm" in H))
bD, bT = (float(x) for x in KV["D1_best"].split("×"))
tD_, tT_ = (float(x) for x in KV["D1_trap"].split("×"))
extra.append((f"D1 simulation preset 'design' is the key's reference tube {KV['D1_best']} (pinned, 2.0 m, e 2 mm, 12 kN)",
              f"design: P_({{ mode: 'imperfect', L: 2.0, sec: 'tube', Do: {bD:g}e-3, tw: {bT:g}e-3, d0: 0, e: 2e-3, Pabs: 12e3 }})" in SIM))
extra.append((f"D1 simulation preset 'designTrap' is the key's fixed-end trap {KV['D1_trap']}",
              f"designTrap: P_({{ mode: 'buckle', ends: 'fixed-fixed', L: 2.0, sec: 'tube', Do: {tD_:g}e-3, tw: {tT_:g}e-3 }})" in SIM))
extra.append(("D1: the trap's K = 0.52 equals the measured fixed–fixed K rounded", abs(float(KV["Bff_K"].split("±")[0]) - 0.52) < 0.005 and "$K$ = 0.52 from Part B" in H))
# procedure, limits and data
def test(part, cfg, L=None, e=None):
    return [r for r in rows if r["part"] == part and r["config"] == cfg and (L is None or float(r["L_mm"]) == L) and (e is None or float(r["e_mm"]) == e)]


specs = [("A 300", test("A", "pinned", 300.0), 250, 0.50, 5.0), ("A 450", test("A", "pinned", 450.0), 100, 0.75, 7.5), ("A 600", test("A", "pinned", 600.0), 50, 1.00, 10.0),
         ("B fixed–fixed", test("B", "fixed-fixed"), 250, 1.00, 10.0), ("B fixed–pinned", test("B", "fixed-pinned"), 100, 1.07, 10.7),
         ("C e = 1", test("C", "eccentric", 450.0, 1.0), 100, 0.75, 7.5), ("C e = 2", test("C", "eccentric", 450.0, 2.0), 100, 0.75, 7.5)]
for name, rr, step, dstep, dmax in specs:
    P = [float(r["load_N"]) for r in rr]
    d = [float(r["defl_mm"]) for r in rr]
    nload = next(i for i in range(1, len(P)) if abs(P[i] - P[i - 1] - step) > 1e-6) if any(abs(P[i] - P[i - 1] - step) > 1e-6 for i in range(1, len(P))) else len(P)
    steps_ok = all(abs(P[i] - i * step) < 1e-6 for i in range(nload))
    tail = [round(d[i] - d[i - 1], 2) for i in range(nload + 1, len(d))]
    dsteps_ok = all(abs(x - dstep) <= 0.03 for x in tail[:-1]) if tail else True
    L_nom = float(rr[0]["L_mm"])
    extra.append((f"procedure = data, {name}: {step} N steps, then {dstep:.2f} mm steps, last reading {dmax} mm = L/60 to the dial step",
                  steps_ok and dsteps_ok and abs(d[-1] - dmax) < 1e-9 and abs(dmax - L_nom / 60) <= 0.5 * dstep and f"{dstep:.2f} mm" in H,
                  f"{nload} load steps, deflection steps {tail}"))
PD = [float(r["load_N"]) for r in test("D", "short")]
dD = [float(r["defl_mm"]) for r in test("D", "short")]
ipk = PD.index(max(PD))
extra.append(("procedure = data, Part D: 4 kN steps, then 0.05 mm steps through the maximum until the load falls by 15 %",
              all(abs(PD[i] - 4000 * i) < 1e-6 for i in range(1, 5)) and all(abs(round(dD[i] - dD[i - 1], 2) - 0.05) < 1e-9 for i in range(len(dD) - 5, len(dD)))
              and PD[-1] < 0.85 * max(PD) <= PD[-2] and "4 kN steps" in H and "every 0.05 mm" in H and "fallen by 15 %" in H))
strut = [float(r["load_N"]) for r in rows if r["part"] != "D"]
extra.append(("safety: the strut-frame loads stay below the 5 kN limit and the deflections stop at L/60",
              max(strut) < 5000 and "never above 5 kN" in H and "stop at a lateral deflection of $L/60$ (5.0, 7.5 and 10 mm for the 300, 450 and 600 mm bars)" in H, f"max {max(strut):.0f} N"))
extra.append(("safety: the key's largest stress in Parts A–C is under the handout's 55 % of σ_Y", float(KV["P6_true_pct"]) <= 55 and "below about 55 % of $\\sigma_Y$" in H,
              f"{KV['P6_true']} MPa = {KV['P6_true_pct']} %"))
for name, rr, load in (("A 300", specs[0][1], 2000), ("A 450", specs[1][1], 900), ("A 600", specs[2][1], 500), ("B fixed–fixed", specs[3][1], 2000),
                       ("B fixed–pinned", specs[4][1], 900), ("C e = 1", specs[5][1], 600), ("C e = 2", specs[6][1], 600)):
    extra.append((f"Table 4 spot load {load} N is a reading of {name}", any(float(r["load_N"]) == load for r in rr)))
d600 = {nm: [float(r["defl_mm"]) for r in rr if float(r["load_N"]) == 600][0] for nm, rr in (("A", specs[1][1]), ("C1", specs[5][1]), ("C2", specs[6][1]))}
extra.append(("procedure check, Part C at 600 N: about 0.9 / 1.5 mm against about 0.26 mm in Part A (data within 0.05 mm)",
              abs(d600["C1"] - 0.9) <= 0.05 and abs(d600["C2"] - 1.5) <= 0.05 and abs(d600["A"] - 0.26) <= 0.05
              and "at 600 N the dial reads about 0.9 mm (e = 1 mm) and 1.5 mm (e = 2 mm), against about 0.26 mm in Part A" in H, str(d600)))
extra.append(("the Southwell selection (P ≥ 0.5 P_pred) is the same in the handout, the analysis and the key",
              "readings above half your P1 load" in H and "frac=0.5" in ANA and "$P \\ge 0.5\\,P_{pred}$" in K))
extra.append(("effective-length factors: Beer's 1, 0.699, 0.5, 2 in the handout and the simulation",
              all(s in H for s in ("0.699", "0.5")) and "K_IDEAL" in SIM and re.search(r"'fixed-pinned': ?(PI|Math\.PI) ?/ ?4\.49340945790906|0\.699", SIM) is not None))
extra.append(("handout Eq. 11 agreement test is the one the key uses (2√(u1² + u2²))", "2\\sqrt{u_{meas}^2 + u_{pred}^2}" in H and "2\\sqrt{u_1^2 + u_2^2}" in K))
extra.append(("handout tables: nothing labeled Table 6 is missing (Tables 1–8 and A1, A2 captioned once each)",
              all(H.count(f": Table {n}.") == 1 for n in list(range(1, 9)) + ["A1", "A2"])))
# truth constants shared by the generator, the simulation and the figures
cfg = {
    "n": "09",
    "constants": {
        "bar 25.4 × 6.35 mm": [("handout", "25.4 × 6.35 mm"), ("sim", "b: 25.42e-3, t: 6.35e-3"), ("gen", "b=25.42e-3, t=6.350e-3"), ("figs", "b = 25.4 mm"), ("figs", "t = 6.35 mm")],
        "E 68.9 GPa (truth), σ_Y 273.7 MPa, m 17": [("sim", "E: 68.9e9, sY: 273.7e6, m: 17"), ("gen", "E=68.9e9"), ("gen", "m=17"), ("figs", "E_AL, SY_AL, M_RO = 68.9e9, 273.7e6, 17")],
        "lengths 300 / 450 / 600 / 640 / 90 mm": [("handout", "300, 450 and 600 mm"), ("handout", "640 mm"), ("handout", "90 mm bar"), ("sim", "L: 0.300"), ("sim", "L: 0.450"),
                                                  ("sim", "L: 0.6005"), ("sim", "L: 0.640"), ("sim", "L: 0.090"), ("figs", "0.640"), ("figs", "0.090")],
        "load cell 5 kN": [("handout", "5 kN load cell"), ("gen", "5 kN load cell")],
        "D1 strut 2.0 m, 12 kN, e 2 mm": [("handout", "service load of 12 kN"), ("sim", "Pabs: 12e3"), ("key", "12 kN")],
    },
    "symbols": ["P_{cr}", "\\sigma_{cr} = P_{cr}/A", "E_t", "r = \\sqrt{I/A}", "c$", "L$ length", "K$ effective-length", "L_e = KL", "L_e/r", "k$ rotational",
                "p = \\sqrt{P/EI}", "y_{max}", "\\delta_0", "\\delta$ change", "\\alpha = P/P_{cr}", "e$ eccentricity", "\\sigma_{max}", "\\sigma_Y", "m$ Ramberg", "U = 2u"],
    "csv_columns": ["part", "config", "L_mm", "e_mm", "step", "load_N", "defl_mm", "eps_front_ue", "eps_back_ue"],
    "sign_phrases": {"handout": ["The axial load $P$ is compressive and is reported as a positive magnitude", "$M = -Py$", "$M = -P(y + e)$",
                                 "the lever arm of the load at mid-length is $e + y_{max}$", "the **front** face is the convex one"],
                     "sim": ["P is the compressive load, reported as a positive magnitude", "M = −P y", "M = −P (y + e)", "lever arm at mid-length is e + y<sub>max</sub>",
                             "the front face is the convex one"],
                     "key": ["$M = -P(y + e)$", "front face convex"]},
    "extra": extra,
}
sys.exit(run(LAB, cfg))

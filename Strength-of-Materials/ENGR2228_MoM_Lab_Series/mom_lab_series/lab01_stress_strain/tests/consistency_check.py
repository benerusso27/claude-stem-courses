"""Cross-file consistency: units, symbols, sign convention, constants, references.

    python3 tests/consistency_check.py      (from lab01_stress_strain/)
"""
import csv
import json
import re
import sys
from pathlib import Path

LAB = Path(__file__).resolve().parents[1]
H = (LAB / "src" / "lab01_handout.md").read_text(encoding="utf-8")
K = (LAB / "src" / "lab01_instructor_key.md").read_text(encoding="utf-8")
SIM = (LAB / "lab01_simulation.html").read_text(encoding="utf-8")
GEN = (LAB / "src" / "generate_sample_data.py").read_text(encoding="utf-8")
FIGS = (LAB / "src" / "make_figures.py").read_text(encoding="utf-8")
ALT = (LAB / "figures" / "ALT_TEXT.md").read_text(encoding="utf-8")
MEAS = json.loads((LAB / "src" / "specimen_measurements.json").read_text())
checks = []


def ok(name, cond, detail=""):
    checks.append((name, bool(cond), detail))


# 1. specimen and test constants appear identically everywhere they are used
consts = {
    "d0 = 10.00 mm": [("handout", "$d_0$ = 10.00 mm" in H or "d_0 = 10.00$ mm" in H or "$d_0 = 10.00$" in H),
                      ("simulation default", "d0: 10e-3" in SIM), ("figures", "d₀ = 10.00 mm" in FIGS or "$d_0$ = 10.00 mm" in FIGS)],
    "gage / extensometer length 50.0 mm": [("handout", "50.0 mm" in H), ("generator", "L0 = 50.0e-3" in GEN),
                                           ("simulation default", "L0: 50e-3" in SIM), ("figures", "50.0 mm" in FIGS)],
    "reduced section 60 mm": [("handout", "$L_c$ = 60 mm" in H), ("generator", "LC = 60.0e-3" in GEN),
                              ("simulation (Lc = 1.2 L0)", "const Lc = 1.2 * p.L0" in SIM), ("figures", "= 60 mm" in FIGS)],
    "compliance 0.008 mm/kN": [("handout", "0.008" in H), ("generator", "C_M = 0.0080e-3 / 1e3" in GEN), ("simulation default", "Cm: 8e-9" in SIM)],
    "rates 1.0 then 5.0 mm/min, removal at 4.0 %": [("handout", "1.0 mm/min" in H and "5.0 mm/min" in H and "4.0 %" in H),
                                                   ("generator", "V1, V2 = 1.0e-3 / 60, 5.0e-3 / 60" in GEN and "EXT_OFF = 0.040" in GEN),
                                                   ("key", "1.0 mm/min" in K and "5.0 mm/min" in K)],
    "imperfection 0.3 %": [("handout", "0.3 %" in H), ("simulation default", "delta: 0.003" in SIM), ("generator", "delta=0.003" in GEN)],
}
for name, items in consts.items():
    for where, cond in items:
        ok(f"constant '{name}' in {where}", cond)

# 2. sign convention stated in handout and simulation, and consistent (tension positive)
ok("sign convention box in handout (tension positive)", "Sign convention (Beer 8e)." in H and "Tension is positive" in H)
ok("sign convention line in simulation (tension positive)", "Sign convention (Beer 8e):" in SIM and "tension positive" in SIM)
ok("no compression-positive statement anywhere", "compression positive" not in (H + K + SIM).lower())

# 3. units: simulation unit table matches the style guide
for q, si in (("stress", "MPa"), ("modulus", "GPa"), ("length", "mm"), ("force", "kN"), ("compliance", "mm/kN"), ("energy", "MJ/m³")):
    ok(f"simulation SI unit for {q} is {si}", re.search(rf"{q}:\s*\{{ SI: \[[^\]]*'{re.escape(si)}'\]", SIM) is not None)
ok("simulation US toggle present", "US customary" in SIM)

# 4. equation numbers: key and handout references point to equations that exist
eqs = set(int(n) for n in re.findall(r"\\qquad \((\d+)\)", H)) | set(int(n) for n in re.findall(r"\((\d+)\)\s*\$\$", H))
eqs |= set(int(n) for n in re.findall(r"\$ \((\d+)\)", H))
max_eq = max(eqs)
refs = set(int(n) for n in re.findall(r"Eqs?\. (\d+)", H + K)) | set(int(n) for n in re.findall(r"Eqs\. \d+–(\d+)", H + K))
missing = sorted(r for r in refs if r > max_eq or r not in eqs)
ok(f"every 'Eq. N' reference exists (equations 1–{max_eq})", not missing, f"missing {missing}")
ok("equations numbered consecutively", sorted(eqs) == list(range(1, max_eq + 1)), str(sorted(set(range(1, max_eq + 1)) - eqs)))

# 5. figures: referenced, files present (SVG + PNG), numbered in order of first appearance, alt text embedded
fig_refs = [int(n) for n in re.findall(r"Figure (\d)", H)]
first_seen = []
for n in fig_refs:
    if n not in first_seen:
        first_seen.append(n)
ok("figures first referenced in order 1, 2, 3, ...", first_seen == sorted(first_seen), str(first_seen))
for n in range(1, 6):
    svg = list((LAB / "figures").glob(f"fig{n}_*.svg"))
    png = list((LAB / "figures").glob(f"fig{n}_*.png"))
    ok(f"figure {n}: SVG and PNG present", len(svg) == 1 and len(png) == 1)
    if svg:
        t = svg[0].read_text(encoding="utf-8")
        ok(f"figure {n}: SVG has <title> and <desc>", "<title" in t and "<desc" in t)
        ok(f"figure {n}: alt text in ALT_TEXT.md", svg[0].stem in ALT)
        ok(f"figure {n}: embedded in handout", f"figures/{svg[0].stem}.png" in H)

# 6. question IDs used in the key exist in the handout
ids = sorted(set(re.findall(r"\*\*([PACMXD]\d)", K)))
missing_q = [q for q in ids if f"**{q}" not in H]
ok(f"all {len(ids)} question IDs in the key exist in the handout", not missing_q, str(missing_q))
hq = sorted(set(re.findall(r"\*\*([PACMXD]\d) ", H)) | set(re.findall(r"\*\*([PACMXD]\d) —", H)))
ok("every handout question answered in the key", all(f"**{q}" in K for q in hq), str([q for q in hq if f"**{q}" not in K]))

# 7. symbols defined in the handout nomenclature
for sym in ("E_{app}", "C_m", "\\Delta_{toe}", "\\varepsilon_u", "\\delta_A", "\\ell", "L_c", "L_e", "\\sigma_t", "\\varepsilon_t"):
    nom = H[H.index("**Nomenclature.**"): H.index("### 2.1")]
    ok(f"symbol ${sym}$ defined in nomenclature", sym in nom)
ok("strain-hardening n flagged as different from Beer's modular ratio", "not** Beer's modular ratio" in H)

# 8. sample data file matches the handout's description and appendix values
with open(LAB / "sample_data.csv", newline="") as f:
    header = next(csv.reader(f))
ok("CSV columns match handout Table A1", header == ["specimen", "time_s", "load_N", "crosshead_mm", "extensometer_mm"], str(header))
for key, col in (("steel_1018HR", 1), ("al_6061T6", 2)):
    m = MEAS[key]
    row = lambda label: [ln for ln in H.splitlines() if ln.startswith("| " + label)][0].split("|")[col + 1].strip()  # noqa: E731
    ok(f"{key}: d0 readings in Appendix A match", row("$d_0$ readings") == ", ".join(f"{v:.2f}" for v in m["d0_readings_mm"]))
    ok(f"{key}: L0, Lf in Appendix A match", row("$L_0$ (mm)") == f"{m['L0_mm']:.2f}" and row("$L_f$ (mm)") == f"{m['Lf_mm']:.2f}")
    ok(f"{key}: df readings in Appendix A match", row("$d_f$ readings") == ", ".join(f"{v:.2f}" for v in m["df_readings_mm"]))

# 9. textbook sections cited exist in Beer 8e's table of contents (Ch. 1, 2, 11 subsections used here)
valid = {"1.2A", "1.5", "2.1", "2.1A", "2.1B", "2.1C", "2.1D", "2.1E", "2.1G", "2.10", "2.12", "11.1B"}
cited = set(re.findall(r"§(\d+\.\d+[A-G]?)", H + K + SIM))
ok("every § citation is a real Beer 8e section", cited <= valid | {"2.1A–2.1E", "2.1A–E"}, str(sorted(cited - valid)))

lines = ["## Lab 1 — cross-file consistency (handout, simulation, figures, key, data)", "", "| Check | Result | Detail |", "|---|---|---|"]
lines += [f"| {n} | {'PASS' if c else '**FAIL**'} | {d} |" for n, c, d in checks]
nf = sum(not c for _, c, _ in checks)
lines += ["", f"{len(checks) - nf} of {len(checks)} passed."]
(Path(__file__).parent / "results_consistency.md").write_text("\n".join(lines) + "\n")
print("\n".join(lines))
sys.exit(1 if nf else 0)

"""Generic cross-file consistency checks for one lab (units, symbols, sign convention, references).

Each lab's tests/consistency_check.py builds a config and calls run(LAB, config):

config = {
  "n": "02",
  "constants": {"description": [("where", "substring that must appear"), ...]},   # where in handout/key/sim/gen/figs
  "symbols": ["E_{app}", ...],              # LaTeX fragments that must appear in the handout nomenclature box
  "csv_columns": ["part", "step", ...],     # header of sample_data.csv, also listed in handout Appendix A
  "sign_phrases": {"handout": [...], "sim": [...]},
  "extra": [(name, bool, detail), ...],     # lab-specific checks already evaluated
}
"""
import csv
import json
import re
from pathlib import Path

SHARED = Path(__file__).resolve().parent


def run(LAB, cfg):
    n = cfg["n"]
    src = LAB / "src"
    H = (src / f"lab{n}_handout.md").read_text(encoding="utf-8")
    K = (src / f"lab{n}_instructor_key.md").read_text(encoding="utf-8")
    SIM = (LAB / f"lab{n}_simulation.html").read_text(encoding="utf-8")
    texts = {"handout": H, "key": K, "sim": SIM,
             "gen": (src / "generate_sample_data.py").read_text(encoding="utf-8"),
             "figs": (src / "make_figures.py").read_text(encoding="utf-8")}
    ALT = (LAB / "figures" / "ALT_TEXT.md").read_text(encoding="utf-8")
    checks = []

    def ok(name, cond, detail=""):
        checks.append((name, bool(cond), detail))

    for desc, items in cfg.get("constants", {}).items():
        for where, sub in items:
            ok(f"constant '{desc}' in {where}", sub in texts[where], "" if sub in texts[where] else f"missing: {sub}")

    # sign convention
    ok("sign convention box in handout", "Sign convention (Beer 8e)." in H)
    ok("sign convention line in simulation", "Sign convention (Beer 8e):" in SIM)
    for where, phrases in cfg.get("sign_phrases", {}).items():
        for ph in phrases:
            ok(f"sign convention states '{ph}' in {where}", ph in texts[where])

    # spelling: Beer writes "gage" (strain gage, gage length)
    nG = sum(t.lower().count("gauge") for t in (H, K, SIM))
    ok('spelling "gage" (as in Beer 8e), never "gauge"', nG == 0, f"{nG} occurrences" if nG else "")

    # equations
    eqs = set(int(x) for x in re.findall(r"\\qquad \((\d+)\)", H)) | set(int(x) for x in re.findall(r"\$ \((\d+)\)", H))
    eqs |= set(int(x) for x in re.findall(r"\$\$\s*\((\d+)\)", H)) | set(int(x) for x in re.findall(r"\\quad \((\d+)\)", H))
    if eqs:
        mx = max(eqs)
        refs = set(int(x) for x in re.findall(r"Eqs?\. (\d+)", H + K)) | set(int(x) for x in re.findall(r"Eqs\. \d+[–-](\d+)", H + K))
        refs |= set(int(x) for x in re.findall(r"Eqs\. \d+, (\d+)", H + K))
        missing = sorted(r for r in refs if r not in eqs)
        ok(f"every 'Eq. N' reference exists (equations 1–{mx})", not missing, f"missing {missing}")
        ok("equations numbered consecutively", sorted(eqs) == list(range(1, mx + 1)), str(sorted(set(range(1, mx + 1)) - eqs)))

    # figures
    fig_refs = [int(x) for x in re.findall(r"Figure (\d)", H)]
    seen = []
    for x in fig_refs:
        if x not in seen:
            seen.append(x)
    ok("figures first referenced in order 1, 2, 3, ...", seen == list(range(1, len(seen) + 1)), str(seen))
    figs = sorted((LAB / "figures").glob("fig*_*.svg"))
    ok("3–5 figures", 3 <= len(figs) <= 5, str(len(figs)))
    for svg in figs:
        k = re.match(r"fig(\d+)_", svg.name).group(1)
        t = svg.read_text(encoding="utf-8")
        ok(f"figure {k}: PNG copy present", svg.with_suffix(".png").exists())
        ok(f"figure {k}: SVG has <title> and <desc>", "<title" in t and "<desc" in t)
        ok(f"figure {k}: alt text in ALT_TEXT.md", svg.stem in ALT)
        ok(f"figure {k}: embedded in handout", f"figures/{svg.stem}.png" in H)
        ok(f"figure {k}: referenced in the text", int(k) in fig_refs)

    # question IDs
    ids = sorted(set(re.findall(r"\*\*([PACMXD]\d+)\b", K)))
    miss = [q for q in ids if not re.search(rf"\*\*{q}\b", H)]
    ok(f"all {len(ids)} question IDs in the key exist in the handout", not miss, str(miss))
    hq = sorted(set(re.findall(r"\*\*([PACMXD]\d+) [\[—]", H)))
    ok(f"every handout question ({len(hq)}) answered in the key", all(re.search(rf"\*\*{q}\b", K) for q in hq),
       str([q for q in hq if not re.search(rf"\*\*{q}\b", K)]))

    # nomenclature
    if "**Nomenclature.**" in H:
        nom = H[H.index("**Nomenclature.**"):]
        nom = nom[:nom.index(":::")]
        for sym in cfg.get("symbols", []):
            ok(f"symbol ${sym}$ defined in nomenclature", sym in nom)
    else:
        ok("nomenclature box present", False)

    # data file
    with open(LAB / "sample_data.csv", newline="") as f:
        header = next(csv.reader(f))
    ok("sample_data.csv columns as configured", header == cfg["csv_columns"], str(header))
    ok("every CSV column described in handout Appendix A", all(f"`{c}`" in H for c in header),
       str([c for c in header if f"`{c}`" not in H]))

    # textbook sections
    valid = set(json.loads((SHARED / "beer8e_sections.json").read_text()))
    cited = set()
    for m in re.finditer(r"§\s?(\d+\.\d+[A-H]?)(?:[–-](\d+\.\d+[A-H]?|[A-H]))?", H + K + SIM):
        cited.add(m.group(1))
        if m.group(2) and re.match(r"\d", m.group(2)):
            cited.add(m.group(2))
    ok("every § citation is a real Beer 8e section", cited <= valid, str(sorted(cited - valid)))

    for item in cfg.get("extra", []):
        name, cond, detail = (tuple(item) + ("",))[:3]
        ok(name, cond, detail)

    lines = [f"## Lab {int(n)} — cross-file consistency (handout, simulation, figures, key, data)", "",
             "| Check | Result | Detail |", "|---|---|---|"]
    esc = lambda x: str(x).replace("|", "\\|")  # noqa: E731
    lines += [f"| {esc(a)} | {'PASS' if c else '**FAIL**'} | {esc(d)} |" for a, c, d in checks]
    nf = sum(not c for _, c, _ in checks)
    lines += ["", f"{len(checks) - nf} of {len(checks)} passed."]
    (LAB / "tests" / "results_consistency.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))
    return 1 if nf else 0

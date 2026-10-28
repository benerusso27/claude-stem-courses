"""Run every verification step for one lab and write tests/VERIFICATION.md.

    python3 shared/verify_lab.py lab01_stress_strain [--skip-browser]

Steps: rebuild the simulation page; Node model tests (exact page code, closed form vs independent
numerics); independent Python/scipy checks and data-pipeline closure; from-scratch re-solve of the
handout vs the key; cross-file consistency; browser check at 375 and 1280 px, light and dark.
"""
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

SERIES = Path(__file__).resolve().parent.parent


def run(cmd, cwd):
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


def md_cell(s):
    """Escape pipes so a name like |Δ| stays in one markdown table cell."""
    return str(s).replace("\\|", "|").replace("|", "\\|")


def table_rows(md):
    rows = []
    for ln in md.splitlines():
        if ln.startswith("| ") and not ln.startswith("| Test") and not ln.startswith("|---") and "Result" not in ln[:20]:
            cells = [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", ln.strip().strip("|"))]
            rows.append(cells)
    return rows


def main():
    lab = sys.argv[1]
    skip_browser = "--skip-browser" in sys.argv
    L = SERIES / lab
    n = re.search(r"lab(\d+)", lab).group(1)
    tests = L / "tests"
    steps = [
        ("Build simulation page", [sys.executable, str(SERIES / "shared" / "build_sim.py"), lab], SERIES, None),
        ("Model tests: closed form vs independent numerics (Node, exact page code)", ["node", f"tests/test_lab{n}_model.js"], L, "results_node.md"),
        ("Independent re-implementation (Python/scipy) and data-pipeline closure", [sys.executable, f"tests/test_lab{n}_independent.py"], L, "results_python.md"),
        ("Handout re-solved from scratch vs instructor key", [sys.executable, "tests/solve_from_scratch.py"], L, "results_from_scratch.md"),
        ("Cross-file consistency (units, symbols, sign convention, references)", [sys.executable, "tests/consistency_check.py"], L, "results_consistency.md"),
    ]
    if not skip_browser:
        steps.append(("Browser check, 375/1280 px, light/dark, every control", [sys.executable, str(SERIES / "shared" / "browser_check.py"),
                      str(L / f"lab{n}_simulation.html"), "--out", str(tests / "results_browser.md")], SERIES, "results_browser.md"))
    summary = []
    all_ok = True
    for name, cmd, cwd, res in steps:
        code, out = run(cmd, cwd)
        all_ok &= code == 0
        detail = ""
        if res and (tests / res).exists():
            txt = (tests / res).read_text()
            m = re.search(r"(\d+) of (\d+) (passed|agree)", txt)
            detail = f"{m.group(1)} of {m.group(2)} {m.group(3)}" if m else ("PASS" if "Result: PASS" in txt else "")
        summary.append((name, "PASS" if code == 0 else "**FAIL**", detail, res))
        print(f"[{'PASS' if code == 0 else 'FAIL'}] {name} {detail}")
        if code != 0:
            print(out[-2000:])

    # formula-vs-numerical agreement, worst case over presets, from the Node and Python tables
    worst = {}
    for res in ("results_node.md", "results_python.md"):
        p = tests / res
        if not p.exists():
            continue
        for cells in table_rows(p.read_text()):
            if len(cells) < 6 or not re.match(r"\d", cells[3] or ""):
                continue
            nm = re.sub(r"^\[[^\]]+\]\s*", "", cells[0]).split(" — ")[0]
            if "closure" in nm or "hand example" in nm or nm.startswith("units"):
                continue
            rel = float(cells[3])
            if nm not in worst or rel > worst[nm][0]:
                worst[nm] = (rel, cells[4], cells[5])
    lines = [f"# Verification record — {lab}", "",
             f"Run with `python3 shared/verify_lab.py {lab}` on {date.today().isoformat()}. "
             "Detailed tables are in the `results_*.md` files next to this one.", "",
             "| Step | Result | Detail | Record |", "|---|---|---|---|"]
    lines += [f"| {md_cell(a)} | {b} | {md_cell(c)} | {('`' + d + '`') if d else ''} |" for a, b, c, d in summary]
    lines += ["", "## Formula vs. independent numerical method (worst case over all material presets)", "",
              "| Comparison | Worst relative difference | Tolerance | Result |", "|---|---:|---:|---|"]
    for nm, (rel, tol, okk) in worst.items():
        lines.append(f"| {md_cell(nm)} | {rel:.1e} | {tol} | {okk} |")
    lines += ["", "Overall: " + ("**PASS**" if all_ok else "**FAIL**")]
    (tests / "VERIFICATION.md").write_text("\n".join(lines) + "\n")
    print("wrote", tests / "VERIFICATION.md")
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()

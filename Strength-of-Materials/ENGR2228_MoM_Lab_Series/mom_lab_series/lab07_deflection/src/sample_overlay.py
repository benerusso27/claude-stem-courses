"""Sample-data overlay embedded in lab07_simulation.html (built by shared/build_sim.py). SI units, downward deflection +."""
import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def overlay():
    rows = list(csv.DictReader(open(HERE.parent / "sample_data.csv")))
    res = json.loads((HERE / "results.json").read_text())
    m = json.loads((HERE / "specimen_measurements.json").read_text())
    f = lambda r, c: float(r[c]) * 1e-3  # noqa: E731
    a6 = [r for r in rows if r["part"] == "A" and r["config"] == "P600"][-1]
    ab = [r for r in rows if r["part"] == "A" and r["config"] == "both"][-1]
    b1 = [r for r in rows if r["part"] == "B" and r["config"] == "cantilever"][-1]
    b2 = [r for r in rows if r["part"] == "B" and r["config"] == "propped"][-1]
    cs = [r for r in rows if r["part"] == "C"]
    C = res["C"]
    return dict(
        A=dict(xg=[x * 1e-3 for x in m["A"]["gage_x_mm"]], P600=[f(a6, c) for c in ("d1_mm", "d2_mm", "d3_mm")], both=[f(ab, c) for c in ("d1_mm", "d2_mm", "d3_mm")]),
        B1=dict(xg=[x * 1e-3 for x in m["B"]["gage_x_mm"]], d=[f(b1, "d1_mm"), f(b1, "d2_mm")]),
        B2=dict(xg=m["B"]["gage_x_mm"][0] * 1e-3, d=f(b2, "d1_mm"), R=float(b2["R_N"])),
        C=dict(x=[f(r, "x_tip_mm") for r in cs], y=[f(r, "y_tip_mm") for r in cs], alpha=[p_["alpha"] for p_ in C["pts"]],
               dvL=[p_["dv"] / C["L"] for p_ in C["pts"]]),
    )


if __name__ == "__main__":
    print(json.dumps(overlay(), indent=1)[:800])

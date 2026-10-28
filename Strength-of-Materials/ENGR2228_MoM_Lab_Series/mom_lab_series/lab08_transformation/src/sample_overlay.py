"""Sample-data overlay embedded in lab08_simulation.html (built by shared/build_sim.py). SI units, strain dimensionless."""
import csv
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent


def overlay():
    rows = list(csv.DictReader(open(HERE.parent / "sample_data.csv")))
    res = json.loads((HERE / "results.json").read_text())
    m = json.loads((HERE / "specimen_measurements.json").read_text())
    r = res["res"]
    last = lambda part, cfg: [x for x in rows if x["part"] == part and x["config"] == cfg][-1]  # noqa: E731
    rd = {}
    for key, (part, cfg) in dict(A=("A", "axis"), B=("B", "lever"), C=("C", "pressure"), Cc=("C", "combined")).items():
        x = last(part, cfg)
        rd[key] = {g: [float(x[f"{g}{c}_ue"]) * 1e-6 for c in "abc"] for g in ("H", "K")}
    pre = dict(A="A", B="B", C="C", Cc="X")
    meas = {k: {g: dict(s1=r[f"{pre[k]}{g}_s1"], s2=r[f"{pre[k]}{g}_s2"]) for g in ("H", "K")} for k in pre}
    ref = m["reference"]
    return dict(rd=rd, meas=meas, betaH=math.radians(r["beta_H"]), betaK=math.radians(r["beta_K"]), Kt=m["rosette"]["Kt"],
                E2=ref["E_al_GPa"] * 1e9, nu2=ref["nu_al"])


if __name__ == "__main__":
    print(json.dumps(overlay(), indent=1)[:1500])

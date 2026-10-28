"""Sample-data overlay embedded in lab06_simulation.html (built by shared/build_sim.py). SI units."""
import csv
import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent


def overlay():
    res = json.loads((HERE / "results.json").read_text())
    m = json.loads((HERE / "specimen_measurements.json").read_text())
    rows = list(csv.DictReader(open(HERE.parent / "sample_data.csv")))
    E = res["E"] * 1e6                                    # Pa
    bm = m["bar"]
    out = {"partA": {}}
    for cfg in ("e0", "e1", "e2"):
        rr = [r for r in rows if r["part"] == "A" and r["config"] == cfg]
        top = max(rr, key=lambda r: float(r["load_N"]))
        g = [float(top[f"g{k:02d}_ue"]) * 1e-6 for k in range(1, 11)]
        f = 30e3 / float(top["load_N"])                     # scaled to the simulation's 30 kN
        out["partA"][cfg] = dict(e=bm["yP_mm"][cfg] * 1e-3, P=30e3,
                                 front=dict(y=[v * 1e-3 for v in bm["y_front_mm"]], sig=[E * v * f for v in g[:5]]),
                                 back=dict(y=[v * 1e-3 for v in bm["y_back_mm"]], sig=[E * v * f for v in g[5:10]]))
    am = m["angle"]
    B = res["B"]
    out["partB"] = dict(lz=am["load_z_mm"] * 1e-3, ly=am["load_y_mm"] * 1e-3,
                        gages=[dict(name=n, z=am["gages_mm"][n]["z"] * 1e-3, y=am["gages_mm"][n]["y"] * 1e-3, sig=B["meas"][i] * 1e6)
                               for i, n in enumerate(am["gages_mm"])])
    C = res["C"]
    out["partC"] = dict(e=C["e"] * 1e-3, P=C["P"], Cmid=C["Cmid_m"], Cend=C["Cend_m"], w=[v * 1e-3 for v in C["w"]])
    A2 = res["A"]["e2"]
    rr = [r for r in rows if r["part"] == "A" and r["config"] == "e2" and float(r["load_N"]) > 100]
    out["partAcol"] = dict(e=A2["e_hole"] * 1e-3, P=A2["P"], Cmid=[v / A2["e_hole"] for v in A2["e_eff"]],
                           w=[float(r["w_mid_mm"]) * 1e-3 for r in rr])
    return out


if __name__ == "__main__":
    print(json.dumps(overlay(), indent=1)[:1500])

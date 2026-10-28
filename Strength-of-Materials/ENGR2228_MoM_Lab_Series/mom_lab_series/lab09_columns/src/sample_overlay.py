"""Sample-data overlay embedded in lab09_simulation.html by shared/build_sim.py (SI base units)."""
import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
LAB = HERE.parent


def overlay():
    rows = list(csv.DictReader(open(LAB / "sample_data.csv", newline="")))
    res = json.loads((HERE / "results.json").read_text())
    tests = {}
    for r in rows:
        key = {"A": "A" + str(int(float(r["L_mm"]))), "B": "Bff" if r["config"] == "fixed-fixed" else "Bfp",
               "C": "C" + str(int(float(r["e_mm"]))), "D": "D"}[r["part"]]
        t = tests.setdefault(key, dict(P=[], d=[], ef=[], eb=[]))
        t["P"].append(float(r["load_N"]))
        t["d"].append(round(float(r["defl_mm"]) * 1e-3, 8))
        t["ef"].append(round(float(r["eps_front_ue"]) * 1e-6, 9) if r["eps_front_ue"] else None)
        t["eb"].append(round(float(r["eps_back_ue"]) * 1e-6, 9) if r["eps_back_ue"] else None)
    sw = {"A300": res["A"]["300"], "A450": res["A"]["450"], "A600": res["A"]["600"], "Bff": res["B"]["ff"], "Bfp": res["B"]["fp"]}
    for k, v in sw.items():
        tests[k]["PS"] = v["PS"]
        tests[k]["Pmin"] = v["Pmin"]
    cur = res["curve"]
    return dict(tests=tests, curve=dict(A=cur["A"], B=cur["B"], D=cur["D"]), Dmax=res["D"]["Pmax"],
                b=res["geom"]["b"] * 1e-3, t=res["geom"]["t"] * 1e-3, E2=68.46e9, sY=273.7e6, k=res["B"]["k"]["k"])


if __name__ == "__main__":
    print(json.dumps(overlay())[:600])

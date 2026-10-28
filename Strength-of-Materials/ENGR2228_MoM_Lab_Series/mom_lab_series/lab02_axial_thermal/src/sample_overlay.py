"""Sample data embedded in the Lab 2 simulation overlay: Part B tube force vs press load and
Part C bolt force vs temperature change, converted with the analysis script's measured values."""
import json
from pathlib import Path

import lab02_analysis as LA

HERE = Path(__file__).resolve().parent


def overlay():
    data = LA.load(LA.LAB / "sample_data.csv")
    m = json.loads((HERE / "specimen_measurements.json").read_text())
    r = LA.analyze(data, m)
    B, C = data["B"], data["C"]
    eps_t = (B["strain_tube_front_ue"] + B["strain_tube_back_ue"]) / 2 * 1e-6
    Ft = r["A"]["E"] * 1e9 * r["B"]["A_tube"] * 1e-6 * eps_t
    Fb = m["handbook"]["E_st_GPa"] * 1e9 * r["C"]["A_b"] * 1e-6 * C["strain_bolt_ue"] * 1e-6
    return {"B": {"P": [float(x) for x in B["load_N"]], "Ft": [round(float(x), 2) for x in Ft]},
            "C": {"dT": [round(float(x) - 20.0, 2) for x in C["temperature_C"]], "Fb": [round(float(x), 2) for x in Fb]}}

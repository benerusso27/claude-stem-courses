"""Sample data embedded in the Lab 3 simulation overlay: torque vs twist over the 50.8 mm gage.
Troptometer twist where it was attached; afterwards the head rotation corrected for compliance and backlash
(using the analysis script's fitted values) and scaled from the reduced length to the gage length."""
import json
import math
from pathlib import Path

import numpy as np

import lab03_analysis as LA

HERE = Path(__file__).resolve().parent


def overlay():
    data = LA.load(LA.LAB / "sample_data.csv")
    m = json.loads((HERE / "specimen_measurements.json").read_text())
    r = LA.analyze(data, m)
    L, Lr = m["L_gage_mm"], m["L_reduced_mm"]
    Cm = 0.5 * (r["steel"]["Cm_deg_per_Nm"] + r["al"]["Cm_deg_per_Nm"])
    toe = 0.5 * (r["steel"]["toe_deg"] + r["al"]["toe_deg"])
    out = {}
    for key in ("steel", "al", "ci"):
        D = data[key]
        T = D["T"][:-1]                                   # drop the post-fracture row
        tr = D["tr"][:-1] * 180 / math.pi
        hd = D["head"][:-1] * 180 / math.pi
        cmk = r[key].get("Cm_deg_per_Nm", Cm)
        tok = r[key].get("toe_deg", toe)
        phi = np.where(np.isnan(tr), (hd - cmk * T - tok) * L / Lr, tr)
        keep = np.r_[np.arange(0, len(T), 1 if len(T) < 200 else 2), len(T) - 1]
        out[key] = {"phi": [round(float(x), 4) for x in phi[keep]], "T": [round(float(x), 3) for x in T[keep]]}
    return out

"""Sample data embedded in the Lab 5 simulation overlay (all derived with the analysis script):
rectUp / rectFlat: shearing stress at the two faces on the neutral axis at the largest load (tau = G gamma);
ibeamWeb: web shearing stress at the three gage heights for V = 10 kN; spans: measured delta / (PL^3/48EI) vs L/h,
with E from the deflection fit; layered: end slip per newton for the three connections."""
import json
from pathlib import Path

import numpy as np

import lab05_analysis as LA

HERE = Path(__file__).resolve().parent


def overlay():
    rows = LA.load(LA.LAB / "sample_data.csv")
    m = json.loads((HERE / "specimen_measurements.json").read_text())
    r = LA.analyze(rows, m)
    G = m["reference"]["G_al_GPa"] * 1e9
    out = {}
    A = r["A"]["A"] * 1e-6
    for cfg, key in (("upright", "rectUp"), ("flat", "rectFlat")):
        rr = LA.loading(LA.sel(rows, "A", cfg))
        last = rr[-1]
        V = last["load_N"] / 2
        gF, gB = -LA.gamma(last, "gA"), -LA.gamma(last, "gB")
        elem = 1.5 * V / A
        Vp = 7500.0 if cfg == "upright" else 3750.0
        out[key] = {"V": Vp, "edge": {"tau": round(G * (gF + gB) / 2 * Vp / V, 1), "ratioFront": round(G * gF / elem, 5), "ratioBack": round(G * gB / elem, 5)}}
    H = r["B"]["H"]
    out["ibeamWeb"] = {"V": 10000.0, "web": {"y": [round((H / 2 + w["y"]) * 1e-3, 6) for w in r["B"]["web"]],
                                             "tau": [round(w["slope"] * 1e6 * 10000.0, 1) for w in r["B"]["web"]]}}
    d = r["B"]["defl"]
    out["spans"] = {"Lh": [round(row["L"] / H, 4) for row in d["rows"]], "ratio": [round(row["C"] / (d["a1"] * row["L"] ** 3), 5) for row in d["rows"]]}
    c = r["C"]
    out["layered"] = {"loose": {"slip_per_N": c["loose"]["slip"]}, "bolts": {"slip_per_N": c["bolted"]["slip"]}, "glue": {"slip_per_N": c["bonded"]["slip"]}}
    return out


if __name__ == "__main__":
    print(json.dumps(overlay(), indent=1, default=float))

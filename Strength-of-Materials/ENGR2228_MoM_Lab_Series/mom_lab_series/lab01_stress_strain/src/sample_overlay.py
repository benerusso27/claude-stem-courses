"""Decimated sample data embedded in the Lab 1 simulation for the 'Compare with sample data' overlay.
Stress uses each specimen's measured A0; strains are raw (extensometer / gage, crosshead / reduced length)."""
import csv
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent


def overlay():
    meas = json.loads((HERE / "specimen_measurements.json").read_text())
    rows = list(csv.DictReader(open(HERE.parent / "sample_data.csv", newline="")))
    out = {}
    for key, short in (("steel_1018HR", "steel"), ("al_6061T6", "al")):
        m = meas[key]
        d0 = sum(m["d0_readings_mm"]) / len(m["d0_readings_mm"])
        A0 = math.pi / 4 * d0 ** 2
        r = [x for x in rows if x["specimen"] == key]
        ext = [(float(x["extensometer_mm"]) / m["extensometer_gage_mm"], float(x["load_N"]) / A0)
               for x in r if x["extensometer_mm"].strip()]
        ch = [(float(x["crosshead_mm"]) / m["reduced_section_mm"], float(x["load_N"]) / A0) for x in r]
        # keep every point in the elastic/yield region, thin the rest
        ext_d = [p for i, p in enumerate(ext) if p[0] < 0.006 or i % 3 == 0]
        ch_d = ch[::4]
        out[short] = {"A0_mm2": round(A0, 3),
                      "ext": [[round(a, 6), round(b, 2)] for a, b in ext_d],
                      "ch": [[round(a, 5), round(b, 2)] for a, b in ch_d]}
    return out

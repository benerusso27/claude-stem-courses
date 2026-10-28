"""Generate realistic sample data for Lab 8 (stress and strain transformation) from a known truth model.

    python3 generate_sample_data.py   ->  ../sample_data.csv, truth.json, specimen_measurements.json

The 6061-T6 tube (38.1 x 3.175 mm nominal) is clamped at one end; a lever at the free end takes a load F at its axis
(Part A) or 200 mm to the side (Part B). Rectangular rosettes (0/45/90 deg) at the gage section, 250 mm from the load
line: H on top, K on the lever side at mid-height. Part C seals the tube and pressurizes it to 8 MPa, first alone and
then with the lever load. Readings in microstrain, zeroed with no load and no pressure at the start of each part.
Truth errors: dimensions, arms, a 0.4 mm offset of the "axis" hole, each rosette slightly off its nominal position on
the circumference and turned by a small angle, gage-factor errors (common and per grid), transverse sensitivity,
load-cell and pressure-transducer gain errors, 1.5 microstrain noise, 1 microstrain resolution.
"""
import json
import math
from pathlib import Path

import numpy as np

import lab08_model as LM

HERE = Path(__file__).resolve().parent
LAB = HERE.parent
rng = np.random.default_rng(20260513)
D = math.radians
TRUTH = dict(
    Do=38.13e-3, t=3.205e-3, E=68.9e9, nu=0.33,
    Lb=0.2506, aL=0.2002, axis_off=-0.4e-3,                       # axis hole 0.4 mm toward the back: T = F * axis_off
    H=dict(phi=D(1.2), beta=D(1.5)), K=dict(phi=D(90 - 0.8), beta=D(-1.0)),
    gf_common=0.003, gf_sd=0.003, Kt=0.012, nu0=0.285, noise=1.5e-6,
    load_gain=1.002, p_gain=0.997,
)
TRUTH["Di"] = TRUTH["Do"] - 2 * TRUTH["t"]
GF = {g: 1 + TRUTH["gf_common"] + TRUTH["gf_sd"] * rng.standard_normal(3) for g in ("H", "K")}
COLS = ["part", "config", "step", "load_N", "lever_mm", "p_MPa", "Ha_ue", "Hb_ue", "Hc_ue", "Ka_ue", "Kb_ue", "Kc_ue"]


def readings(F, arm, p):
    """True strains at H and K -> indicated readings (rosette turned, transverse sensitivity, gage factor), microstrain."""
    T = TRUTH
    out, states = {}, {}
    for g in ("H", "K"):
        s = LM.tube_state(T["Do"], T["Di"], F, arm, T["Lb"], p, T[g]["phi"])
        ex, ey, gxy = LM.state_strains(s["sx"], s["sy"], s["txy"], T["E"], T["nu"])
        r = LM.gage_readings(ex, ey, gxy, LM.RECT, T[g]["beta"], T["Kt"], T["nu0"], GF[g])
        out[g] = [x + rng.normal(0, T["noise"]) for x in r]
        states[g] = s
    return out, states


def main():
    T = TRUTH
    rows, rec = [], dict(A=[], B=[], C=[], Cc=[])

    def add(part, cfg, step, F_true, arm_true, p_true, F_show, lever_show, p_show, key):
        rd, stt = readings(F_true, arm_true, p_true)
        rows.append(dict(part=part, config=cfg, step=step, load_N=f"{F_show:.1f}", lever_mm=f"{lever_show:.0f}", p_MPa=f"{p_show:.2f}",
                         **{f"{g}{c}_ue": str(int(round(rd[g][i] * 1e6))) for g in ("H", "K") for i, c in enumerate("abc")}))
        rec[key].append(dict(F=F_true, arm=arm_true, p=p_true, sH={k: float(v) for k, v in stt["H"].items()}, sK={k: float(v) for k, v in stt["K"].items()}))
    loads = [0, 100, 200, 300, 400, 500, 600]
    for i, F in enumerate(loads):
        Ft = F / T["load_gain"]                                    # the load cell reads 0.2 % high
        add("A", "axis", i, Ft, T["axis_off"], 0.0, F, 0, 0.0, "A")
    for i, F in enumerate(loads):
        Ft = F / T["load_gain"]
        add("B", "lever", i, Ft, T["aL"], 0.0, F, 200, 0.0, "B")
    for i, p in enumerate([0, 2, 4, 6, 8]):
        add("C", "pressure", i, 0.0, T["aL"], p * 1e6 / T["p_gain"], 0, 200, p, "C")
    for i, F in enumerate([0, 200, 400, 600]):
        add("C", "combined", i, F / T["load_gain"], T["aL"], 8e6 / T["p_gain"], F, 200, 8.0, "Cc")
    lines = [",".join(COLS)] + [",".join(str(r[c]) for c in COLS) for r in rows]
    (LAB / "sample_data.csv").write_text("\n".join(lines) + "\n")
    truth = dict(T, GF={g: list(v) for g, v in GF.items()}, rec=rec)
    (HERE / "truth.json").write_text(json.dumps(truth, indent=1, default=float))
    meas = dict(
        tube=dict(Do_mm=[38.12, 38.14, 38.13, 38.13], t_mm=[3.20, 3.21, 3.20, 3.21], Lb_mm=250.0, aL_mm=200.0, axis_mm=0.0),
        rosette=dict(GF=2.10, GF_tol_pct=0.5, Kt=0.012, nu0=0.285, angles_deg=[0, 45, 90]),
        g=9.80665, micrometer_accuracy_mm=0.003, ball_micrometer_accuracy_mm=0.005, rule_accuracy_mm=0.5, loadcell_accuracy_pct=0.5,
        p_accuracy_MPa=0.05, strain_resolution_ue=1.0, strain_accuracy_pct=0.1,
        reference=dict(E_al_GPa=68.46, u_E_al_GPa=0.47, nu_al=0.3296, u_nu_al=0.0029, G_al_GPa=26.03, u_G_al_GPa=0.12, sY_al_MPa=273.7, u_sY_al_MPa=1.0),
    )
    (HERE / "specimen_measurements.json").write_text(json.dumps(meas, indent=1))
    print(len(rows), "rows; GF", {g: [round(x, 4) for x in v] for g, v in GF.items()})


if __name__ == "__main__":
    main()

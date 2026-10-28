"""Generate realistic sample data for Lab 6 (eccentric axial loading) from a known truth model.

    python3 generate_sample_data.py   ->  ../sample_data.csv, truth.json, specimen_measurements.json

One 6061-T6 bar, 50.8 x 12.7 mm, 250 mm free length between steel end blocks; the load line passes through a pin
25 mm beyond each end of the free length. The end blocks have four pin holes:
  Part A: in-plane offsets e = 0, h/6, h/3 (configs e0, e1, e2), to 30 kN;
  Part C: out-of-plane offset b/2 (config ez), to 25 kN: the bar bends about its weak axis and straightens visibly.
Twelve gages: five across the width on each broad face at mid-length, and a front/back pair near one end.
Part B: a 6061-T6 equal-leg angle 50.8 x 50.8 x 6.35 mm (root fillet r = 4.8 mm), 300 mm free length, loaded
through a gusset on one leg (load line in the gusset mid-plane, on the bolt line), to 30 kN; four gages.
Truth: superposition (Beer Eq. 4.58) in principal axes, with each principal eccentricity reduced by the
beam-column factor of a tension member with rigid end blocks (Appendix D of the handout); per-gage gage-factor
errors, 1.5 microstrain noise, load-cell and LVDT gain errors, small fixture misalignments.
"""
import json
import math
from pathlib import Path

import numpy as np

import lab06_model as LM

HERE = Path(__file__).resolve().parent
LAB = HERE.parent
rng = np.random.default_rng(20260429)

E = 68.9e9
TRUTH = dict(
    E=E, gf_common=0.003, gf_sd=0.003, noise_ue=1.5, load_gain=1.002, lvdt_gain=1.003,
    bar=dict(h=50.83e-3, b=12.68e-3, L=0.250, a=0.025, x_end=0.040,
             yP={"e0": 0.07e-3, "e1": 8.46e-3, "e2": 16.99e-3, "ez": 0.05e-3},
             zP={"e0": 0.15e-3, "e1": 0.15e-3, "e2": 0.15e-3, "ez": 6.38e-3},
             y_front=[-20.12e-3, -10.05e-3, 0.08e-3, 10.11e-3, 20.02e-3], y_back=[-20.03e-3, -10.12e-3, -0.02e-3, 9.93e-3, 20.09e-3],
             y_end=[0.05e-3, -0.04e-3]),
    angle=dict(bV=50.85e-3, bH=50.76e-3, t=6.33e-3, r=4.8e-3, L=0.300, a=0.025, load=(-28.55e-3, -4.78e-3),
               gages=[(0.0, 44.1e-3), (0.0, 12.05e-3), (-11.9e-3, 0.0), (-44.05e-3, 0.0)]),
)
COLS = ["part", "config", "step", "load_N", "w_mid_mm"] + [f"g{k:02d}_ue" for k in range(1, 13)]
GF = 1 + TRUTH["gf_common"] + rng.normal(0, TRUTH["gf_sd"], 16)   # gage-factor error of each physical gage


def q(x):
    return int(round(x))


def principal_stress_fn(pr, P, yP, zP, L, a, x):
    """sigma(y, z) at section x of the free length, and the lateral displacement vector of the centroid at mid-length,
    each principal eccentricity reduced by the beam-column factor (truth model)."""
    w, V = np.linalg.eigh(pr["S"])
    e = np.array([yP, zP])
    terms, disp = [], np.zeros(2)
    for k in range(2):
        d, lam = V[:, k], w[k]
        ek = float(d @ e)
        bc = LM.beam_column(P, E * lam, L, a, ek) if P > 0 else dict(Cmid=1.0, M=lambda xx: 1.0, wmid=0.0)
        Ck = float(bc["M"](x)) if P > 0 else 1.0
        terms.append((d, ek * Ck / lam))
        disp += d * ek * bc["wmid"]
    return (lambda y, z: P / pr["A"] + P * sum(c * float(d @ np.array([y, z])) for d, c in terms)), disp


def bar_runs(rows):
    t = TRUTH["bar"]
    sec = LM.rect(t["h"], t["b"])
    pr = LM.props(sec)
    info = dict(A=pr["A"], Iz=pr["Iz"], Iy=pr["Iy"], runs={})
    plan = (("A", "e0", [0, 5e3, 10e3, 15e3, 20e3, 25e3, 30e3, 0]), ("A", "e1", [0, 5e3, 10e3, 15e3, 20e3, 25e3, 30e3, 0]),
            ("A", "e2", [0, 5e3, 10e3, 15e3, 20e3, 25e3, 30e3, 0]), ("C", "ez", [0, 5e3, 10e3, 15e3, 20e3, 25e3, 0]))
    for part, cfg, loads in plan:
        yP, zP = t["yP"][cfg], t["zP"][cfg]
        run = []
        for i, P in enumerate(loads):
            fm, disp = principal_stress_fn(pr, P, yP, zP, t["L"], t["a"], t["L"] / 2)
            fe, _ = principal_stress_fn(pr, P, yP, zP, t["L"], t["a"], t["x_end"])
            pts = [(y, t["b"] / 2) for y in t["y_front"]] + [(y, -t["b"] / 2) for y in t["y_back"]]
            sig = [fm(y, z) for y, z in pts] + [fe(t["y_end"][0], t["b"] / 2), fe(t["y_end"][1], -t["b"] / 2)]
            g = [q(1e6 * s / E * GF[k] + rng.normal(0, TRUTH["noise_ue"])) for k, s in enumerate(sig)]
            wdir = disp[0] if part == "A" else disp[1]                  # LVDT along the eccentricity
            wm = wdir * TRUTH["lvdt_gain"] + rng.normal(0, 0.002e-3)
            Pm = P * TRUTH["load_gain"] + (rng.normal(0, 4) if P else rng.normal(0, 1))
            r = dict(part=part, config=cfg, step=i, load_N=q(Pm), w_mid_mm=f"{wm * 1e3:.3f}")
            r.update({f"g{k + 1:02d}_ue": g[k] for k in range(12)})
            rows.append(r)
            run.append(dict(P=P, sig=sig, w=wdir))
        info["runs"][cfg] = run
    return info


def angle_run(rows):
    t = TRUTH["angle"]
    sec = LM.angle(t["bV"], t["bH"], t["t"], t["r"])
    pr = LM.props(sec)
    zP, yP = t["load"][0] - pr["zc"], t["load"][1] - pr["yc"]
    info = dict(A=pr["A"], yc=pr["yc"], zc=pr["zc"], Iz=pr["Iz"], Iy=pr["Iy"], Iyz=pr["Iyz"], Imax=pr["Imax"], Imin=pr["Imin"], run=[])
    for i, P in enumerate([0, 5e3, 10e3, 15e3, 20e3, 25e3, 30e3, 0]):
        fm, disp = principal_stress_fn(pr, P, yP, zP, t["L"], t["a"], t["L"] / 2)
        sig = [fm(y - pr["yc"], z - pr["zc"]) for (z, y) in t["gages"]]
        g = [q(1e6 * s / E * GF[12 + k] + rng.normal(0, TRUTH["noise_ue"])) for k, s in enumerate(sig)]
        Pm = P * TRUTH["load_gain"] + (rng.normal(0, 4) if P else rng.normal(0, 1))
        r = dict(part="B", config="angle", step=i, load_N=q(Pm), w_mid_mm="")
        r.update({f"g{k + 1:02d}_ue": (g[k] if k < 4 else "") for k in range(12)})
        rows.append(r)
        info["run"].append(dict(P=P, sig=sig))
    return info


def main():
    rows = []
    a = bar_runs(rows)
    b = angle_run(rows)
    lines = [",".join(COLS)] + [",".join(str(r[c]) for c in COLS) for r in rows]
    (LAB / "sample_data.csv").write_text("\n".join(lines) + "\n")
    truth = dict(TRUTH, gf=list(GF), partAC=a, partB=b)
    (HERE / "truth.json").write_text(json.dumps(truth, indent=1, default=float))
    meas = dict(
        bar=dict(h_mm=[50.84, 50.82, 50.83], b_mm=[12.681, 12.678, 12.684], L_mm=250.0, a_mm=25.0,
                 yP_mm={"e0": 0.04, "e1": 8.49, "e2": 16.95, "ez": 0.04}, zP_mm={"e0": 0.0, "e1": 0.0, "e2": 0.0, "ez": 6.40},
                 y_front_mm=[-20.1, -10.0, 0.1, 10.1, 20.0], y_back_mm=[-20.0, -10.1, 0.0, 9.9, 20.1], x_end_mm=40.0),
        angle=dict(bV_mm=[50.86, 50.84, 50.85], bH_mm=[50.75, 50.77, 50.76], t_mm=[6.331, 6.334, 6.328, 6.331], r_mm=4.8,
                   L_mm=300.0, a_mm=25.0, load_z_mm=-28.58, load_y_mm=-4.76,
                   gages_mm=dict(G1=dict(z=0.0, y=44.0), G2=dict(z=0.0, y=12.0), G3=dict(z=-12.0, y=0.0), G4=dict(z=-44.0, y=0.0))),
        caliper_accuracy_mm=0.02, micrometer_accuracy_mm=0.003, rule_accuracy_mm=0.5, hole_position_accuracy_mm=0.05,
        gage_position_accuracy_mm=0.2, radius_gage_accuracy_mm=0.4, gage_factor_tolerance_pct=1.0, load_cell_accuracy_pct=0.5,
        lvdt_accuracy_pct=0.5, lvdt_resolution_mm=0.001,
        reference=dict(E_al_GPa=68.46, u_E_al_GPa=0.47, sY_al_MPa=273.7, u_sY_al_MPa=1.0),
    )
    (HERE / "specimen_measurements.json").write_text(json.dumps(meas, indent=1))
    print(len(rows), "rows")


if __name__ == "__main__":
    main()

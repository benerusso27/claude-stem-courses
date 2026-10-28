"""Generate realistic 'measured' data for Lab 2 (run without equipment).

    python3 generate_sample_data.py   ->  ../sample_data.csv, truth.json, specimen_measurements.json

Part A  6061-T6 flat bar in tension, axial and transverse gages on both faces (small load-train bending).
Part B  1018 steel rod inside a 6061-T6 tube between rigid caps on a press; the tube is 0.040 mm shorter,
        so the rod carries the load alone until the gap closes. Tube gages (both faces), dial gage on the caps.
Part C  Steel bolt clamping a 6061-T6 sleeve, preloaded at 20 C, heated in a water bath to 80 C and cooled.
        Self-temperature-compensated gage on the bolt (small residual apparent strain), thermocouple.
Imperfections the analysis must cope with: gage-factor error (systematic), bending (front/back differ),
gage noise and 1 ue resolution, load noise, fit-up gap, cap compliance in the dial reading,
temperature dependence of aluminum's modulus, residual thermal output of the bolt gage.
"""
import json
import math
from pathlib import Path

import numpy as np

from lab02_model import area_circle, area_tube, parallel

HERE = Path(__file__).resolve().parent
LAB = HERE.parent
rng = np.random.default_rng(20260204)

TRUTH = dict(
    E_al=68.9e9, nu_al=0.330, E_st=205e9, alpha_st=11.9e-6, alpha_al=23.4e-6,
    gf_error=+0.006,                 # actual gage factor 0.6 % above the value set on the indicator
    bend_A=0.055,                    # bending strain / axial strain in Part A (load-train misalignment)
    bend_B=0.03,
    gap=40e-6, C_cap=0.0015e-3 / 1e3, dial_seat=0.004e-3,
    preload=2.0e3, gage_thermal_ue_per_C=0.4, E_al_temp_coeff=-3.0e-4,   # per kelvin
)
GEOM = dict(
    A_b=25.40e-3, A_t=6.35e-3,
    B_rod_d=12.70e-3, B_tube_do=25.40e-3, B_tube_di=19.05e-3, B_L=150.00e-3,
    C_bolt_d=10.00e-3, C_sleeve_do=20.00e-3, C_sleeve_di=10.50e-3, C_L=100.0e-3,
)


def q(x, res=1.0):
    return np.round(np.asarray(x) / res) * res


def part_a():
    A = GEOM["A_b"] * GEOM["A_t"]
    loads = np.r_[np.arange(0, 18001, 2000), np.arange(16000, -1, -2000)].astype(float)
    rows = []
    for i, P in enumerate(loads):
        Pm = P + rng.normal(0, 5) if P > 0 else rng.normal(0, 3)
        ea = P / (A * TRUTH["E_al"])
        et = -TRUTH["nu_al"] * ea
        k = 1 + TRUTH["gf_error"]          # indicator reads strain * (GF_actual/GF_set)
        b = TRUTH["bend_A"]
        rows.append(dict(part="A", step=i, temperature_C=21.0, load_N=round(Pm),
                         strain_axial_front_ue=q(1e6 * ea * (1 + b) * k + rng.normal(0, 1.2)),
                         strain_axial_back_ue=q(1e6 * ea * (1 - b) * k + rng.normal(0, 1.2)),
                         strain_transverse_front_ue=q(1e6 * et * (1 + b) * k + rng.normal(0, 1.2)),
                         strain_transverse_back_ue=q(1e6 * et * (1 - b) * k + rng.normal(0, 1.2))))
    return rows


def part_b():
    rod = dict(E=TRUTH["E_st"], A=area_circle(GEOM["B_rod_d"]), L=GEOM["B_L"], alpha=TRUTH["alpha_st"])
    tube = dict(E=TRUTH["E_al"], A=area_tube(GEOM["B_tube_do"], GEOM["B_tube_di"]), L=GEOM["B_L"], alpha=TRUTH["alpha_al"])
    loads = np.r_[np.arange(0, 30001, 2000), np.arange(28000, -1, -4000)].astype(float)
    rows = []
    for i, P in enumerate(loads):
        F1, F2, e1 = parallel(P, 0.0, rod, tube, TRUTH["gap"], contact=True)
        eps_t = F2 / (tube["E"] * tube["A"])
        k = 1 + TRUTH["gf_error"]
        b = TRUTH["bend_B"]
        dial = -e1 + TRUTH["C_cap"] * P + TRUTH["dial_seat"] * (1 - math.exp(-P / 1500.0))
        rows.append(dict(part="B", step=i, temperature_C=21.0, load_N=round(P + (rng.normal(0, 8) if P else rng.normal(0, 3))),
                         strain_tube_front_ue=q(1e6 * eps_t * (1 + b) * k + rng.normal(0, 1.2)),
                         strain_tube_back_ue=q(1e6 * eps_t * (1 - b) * k + rng.normal(0, 1.2)),
                         dial_mm=f"{dial * 1e3 + rng.normal(0, 0.0007):.3f}".replace("-0.000", "0.000")))
    truth = dict(P_gap=rod["E"] * rod["A"] / rod["L"] * TRUTH["gap"],
                 share=tube["E"] * tube["A"] / (tube["E"] * tube["A"] + rod["E"] * rod["A"]),
                 rod_stress_at_30kN=-parallel(30e3, 0, rod, tube, TRUTH["gap"])[0] / rod["A"])
    return rows, truth


def part_c():
    Ab = area_circle(GEOM["C_bolt_d"])
    As = area_tube(GEOM["C_sleeve_do"], GEOM["C_sleeve_di"])
    L = GEOM["C_L"]
    temps = np.r_[np.arange(20, 81, 5), np.arange(70, 19, -10)].astype(float)
    rows = []
    kb = TRUTH["E_st"] * Ab / L
    for i, T in enumerate(temps):
        dT = T - 20.0
        Es = TRUTH["E_al"] * (1 + TRUTH["E_al_temp_coeff"] * dT)
        ks = Es * As / L
        # preload set at 20 C as an interference; thermal mismatch adds tension in the bolt
        interference = TRUTH["preload"] * (1 / kb + 1 / (TRUTH["E_al"] * As / L))
        F = (interference + (TRUTH["alpha_al"] - TRUTH["alpha_st"]) * dT * L) / (1 / kb + 1 / ks)
        eps_mech = F / (TRUTH["E_st"] * Ab)
        apparent = TRUTH["gage_thermal_ue_per_C"] * dT * 1e-6
        k = 1 + TRUTH["gf_error"]
        # the gage was zeroed on the bare bolt before assembly, so it reads the preload strain too
        rows.append(dict(part="C", step=i, temperature_C=round(T + rng.normal(0, 0.3), 1), load_N="",
                         strain_bolt_ue=q(1e6 * (eps_mech + apparent) * k + rng.normal(0, 1.5))))
    truth = dict(dF_dT_true=(TRUTH["alpha_al"] - TRUTH["alpha_st"]) * L / (1 / kb + 1 / (TRUTH["E_al"] * As / L)),
                 preload_strain_ue=1e6 * TRUTH["preload"] / (TRUTH["E_st"] * Ab))
    return rows, truth


COLS = ["part", "step", "temperature_C", "load_N", "strain_axial_front_ue", "strain_axial_back_ue",
        "strain_transverse_front_ue", "strain_transverse_back_ue", "strain_tube_front_ue", "strain_tube_back_ue",
        "dial_mm", "strain_bolt_ue"]


def main():
    ra = part_a()
    rb, tb = part_b()
    rc, tc = part_c()
    lines = [",".join(COLS)]
    for r in ra + rb + rc:
        vals = []
        for c in COLS:
            v = r.get(c, "")
            if isinstance(v, (float, np.floating)) and c not in ("temperature_C", "dial_mm"):
                v = int(v)
            vals.append(str(v))
        lines.append(",".join(vals))
    (LAB / "sample_data.csv").write_text("\n".join(lines) + "\n")
    truth = dict(TRUTH, **{f"B_{k}": v for k, v in tb.items()}, **{f"C_{k}": v for k, v in tc.items()})
    (HERE / "truth.json").write_text(json.dumps(truth, indent=1))
    meas = dict(
        A_width_mm=[25.41, 25.39, 25.40], A_thickness_mm=[6.36, 6.34, 6.35],
        B_rod_d_mm=[12.70, 12.71, 12.70], B_tube_do_mm=[25.41, 25.40, 25.40], B_tube_di_mm=[19.04, 19.06, 19.05],
        B_rod_L_mm=150.00, B_tube_L_mm=149.96,
        C_bolt_d_mm=[10.00, 10.01, 10.00], C_sleeve_do_mm=[20.00, 20.01, 20.00], C_sleeve_di_mm=[10.50, 10.51, 10.50],
        C_L_mm=100.0, C_preload_N=2000.0,
        gage_factor_set=2.10, gage_factor_tolerance_pct=1.0, gage_resolution_ue=1,
        load_cell_accuracy_pct=0.5, caliper_accuracy_mm=0.02, bore_gage_accuracy_mm=0.01, thermocouple_accuracy_C=1.0,
        height_gage_accuracy_mm=0.01, dial_resolution_mm=0.001, gage_residual_thermal_ue_per_C=0.5,
        handbook=dict(E_al_GPa=68.9, nu_al=0.33, E_st_GPa=205.0, alpha_al=23.6e-6, alpha_st=11.7e-6,
                      u_alpha=0.3e-6, u_E_st_GPa=3.0))
    (HERE / "specimen_measurements.json").write_text(json.dumps(meas, indent=1))
    print(len(lines) - 1, "rows;", json.dumps({k: (round(v, 4) if isinstance(v, float) else v) for k, v in truth.items()}))


if __name__ == "__main__":
    main()

"""Generate realistic 'measured' tension-test data for Lab 1 (run without equipment).

    python3 generate_sample_data.py          # writes ../sample_data.csv, truth.json, specimen_measurements.json

What makes the data realistic (and what students must deal with):
  * 1018 hot-rolled steel shows an upper/lower yield point and a serrated Luders plateau.
  * 6061-T6 aluminum yields gradually (Ramberg-Osgood), so it needs the 0.2 % offset method.
  * Necking localizes in a short zone (length 0.6 d0) at a 0.3 % area imperfection.
  * Crosshead displacement includes grip seating ("toe") and machine/grip compliance.
  * The clip-on extensometer (gage 50.0 mm) is removed at 4 % strain, as is common practice,
    so uniform elongation and the post-yield curve must come from compliance-corrected crosshead data.
  * Load-cell, extensometer and crosshead noise and quantization.
"""
import json
import math
from pathlib import Path

import numpy as np

from lab01_model import RambergOsgoodPlastic, SwiftAfterLuders, simulate_zone

HERE = Path(__file__).resolve().parent
LAB = HERE.parent
rng = np.random.default_rng(20260125)

L0 = 50.0e-3        # gage length between punch marks = extensometer gage length (m)
LC = 60.0e-3        # reduced-section length (m)
C_M = 0.0080e-3 / 1e3   # machine + grip + shoulder compliance (m/N) = 0.0080 mm/kN
TOE = 0.050e-3      # grip-seating slack taken up at low load (m)
TOE_P = 600.0       # load scale of seating (N)
EXT_OFF = 0.040     # extensometer removed at 4 % strain
DT = 0.2            # s (5 Hz)
V1, V2 = 1.0e-3 / 60, 5.0e-3 / 60   # crosshead rates before/after extensometer removal (m/s)

SPECIMENS = {
    "steel_1018HR": dict(
        label="AISI 1018 hot-rolled steel", E=205e9, d0=10.004e-3, delta=0.003, ell_over_d=0.6,
        RA=0.600, s_uy=322e6, s_ly=297e6, eps_L=0.017, n=0.19, K=758.3e6,
        d0_readings=[10.00, 10.01, 10.00, 10.01, 10.00, 10.01], L0_meas=50.01),
    "al_6061T6": dict(
        label="6061-T6 aluminum", E=68.9e9, d0=9.996e-3, delta=0.003, ell_over_d=0.6,
        RA=0.420, s02=274e6, m=17,
        d0_readings=[10.00, 9.99, 10.00, 9.99, 10.00, 9.99], L0_meas=49.99),
}


def truth_path(sp):
    E, d0, delta = sp["E"], sp["d0"], sp["delta"]
    A0 = math.pi / 4 * d0 ** 2
    ell = sp["ell_over_d"] * d0
    eps_f = math.log(1.0 / ((1.0 - sp["RA"]) / (1.0 - delta)))   # zone plastic strain at fracture
    if "s_uy" in sp:
        # Phase A: elastic to the upper yield point; Phase B: drop + Luders plateau; Phase C: hardening
        Puy, Ply = sp["s_uy"] * A0, sp["s_ly"] * A0 * (1.0 - delta)   # weakest section sets the plateau
        rows = []
        for P in np.linspace(0, Puy, 120):
            et = (P / A0) / E
            rows.append((P, 0.0, 0.0, et, et))
        # drop from upper to lower yield over a small plastic strain, then plateau at constant load
        for ep in np.linspace(0, 0.0006, 15)[1:]:
            P = Puy - (Puy - Ply) * (ep / 0.0006)
            rows.append((P, ep, ep, ep + (P / A0) / E, ep + (P / A0) / E))
        for ep in np.linspace(0.0006, sp["eps_L"], 160)[1:]:
            P = Ply
            s = P / (A0 * math.exp(-ep))
            rows.append((P, ep, ep, ep + s / E, ep + s / E))
        flow = SwiftAfterLuders(sp["K"], sp["n"], sp["s_ly"] * math.exp(sp["eps_L"]), sp["eps_L"])
        z = simulate_zone(flow, E, A0, L0, LC, ell, delta, eps_f, ep_start=sp["eps_L"], n_steps=2500,
                          grading=1.6, sigma_e=None)
        P = np.concatenate([[r[0] for r in rows], z["P"]])
        epz = np.concatenate([[r[1] for r in rows], z["ep_z"]])
        epr = np.concatenate([[r[2] for r in rows], z["ep_r"]])
        etz = np.concatenate([[r[3] for r in rows], z["et_z"]])
        etr = np.concatenate([[r[4] for r in rows], z["et_r"]])
        luders = np.concatenate([np.zeros(120), np.ones(14 + 159), np.zeros(len(z["P"]))]).astype(bool)
    else:
        flow = RambergOsgoodPlastic(sp["s02"], sp["m"])
        z = simulate_zone(flow, E, A0, L0, LC, ell, delta, eps_f, ep_start=0.0, n_steps=3000, grading=3.0)
        # low-load branch, resolved finely so grip seating (toe) is sampled correctly:
        # at these stresses the Ramberg-Osgood plastic strain is < 1e-9 but is kept for consistency
        Pl = np.linspace(0.0, z["P"][0], 150)[:-1]
        sz_l, sr_l = Pl / (A0 * (1 - delta)), Pl / A0
        epz_l = 0.002 * (sz_l / sp["s02"]) ** sp["m"]
        epr_l = 0.002 * (sr_l / sp["s02"]) ** sp["m"]
        P = np.concatenate([Pl, z["P"]])
        epz = np.concatenate([epz_l, z["ep_z"]])
        epr = np.concatenate([epr_l, z["ep_r"]])
        etz = np.concatenate([epz_l + sz_l / E, z["et_z"]])
        etr = np.concatenate([epr_l + sr_l / E, z["et_r"]])
        luders = np.zeros(len(P), bool)
    d_gage = ell * np.expm1(etz) + (L0 - ell) * np.expm1(etr)
    d_red = d_gage + (LC - L0) * np.expm1(etr)
    return dict(A0=A0, ell=ell, eps_f=eps_f, P=P, ep_z=epz, ep_r=epr, et_z=etz, et_r=etr,
                d_gage=d_gage, d_red=d_red, luders=luders)


def measured(sp, tp):
    P, d_gage, d_red = tp["P"], tp["d_gage"], tp["d_red"]
    xh = d_red + C_M * P + TOE * (1 - np.exp(-P / TOE_P))
    # crosshead must be monotonic for a displacement-controlled test
    assert np.all(np.diff(xh) > -1e-9), "crosshead path not monotonic"
    xh = np.maximum.accumulate(xh)
    # time from piecewise crosshead rate
    i_off = int(np.argmax(d_gage / L0 >= EXT_OFF))
    x_off = xh[i_off]
    t_of_x = np.where(xh <= x_off, xh / V1, x_off / V1 + (xh - x_off) / V2)
    t = np.arange(0.0, t_of_x[-1], DT)
    # resample (crosshead is the controlled variable)
    load = np.interp(t, t_of_x, P)
    gage = np.interp(t, t_of_x, d_gage)
    xhd = np.interp(t, t_of_x, xh)
    lud = np.interp(t, t_of_x, tp["luders"].astype(float)) > 0.5
    # Luders serrations: correlated fluctuations on the plateau (+/- ~1.5 MPa)
    A0 = tp["A0"]
    ser = np.convolve(rng.normal(0, 1, len(t)), np.ones(4) / 4, mode="same") * 1.2e6 * A0
    load = load + np.where(lud, ser, 0.0)
    # instrument noise and quantization
    load = load + rng.normal(0, 6.0, len(t)) + load * rng.normal(0, 5e-4, len(t))
    load = np.round(load, 0)
    ext = gage + rng.normal(0, 0.12e-6, len(t))
    ext = np.round(ext * 1e3, 4)                       # mm, 0.1 um resolution
    ext_str = [f"{v:.4f}" if g / L0 < EXT_OFF else "" for v, g in zip(ext, gage)]
    xhd = np.round((xhd + rng.normal(0, 0.4e-6, len(t))) * 1e3, 3)   # mm, 1 um resolution
    # fracture: a few samples after the final point with ~zero load
    n_post = 6
    t_post = t[-1] + DT * np.arange(1, n_post + 1)
    rows = [(f"{ti:.1f}", f"{int(li)}", f"{xi:.3f}", e) for ti, li, xi, e in zip(t, load, xhd, ext_str)]
    for k, tk in enumerate(t_post):
        rows.append((f"{tk:.1f}", f"{int(round(rng.normal(0, 6.0)))}", f"{xhd[-1] + V2 * DT * (k + 1) * 1e3:.3f}", ""))
    return rows, dict(t_ext_off=float(x_off / V1), n=len(rows))


def main():
    lines = ["specimen,time_s,load_N,crosshead_mm,extensometer_mm"]
    truth, meas = {}, {}
    for key, sp in SPECIMENS.items():
        tp = truth_path(sp)
        rows, info = measured(sp, tp)
        lines += [f"{key},{a},{b},{c},{d}" for a, b, c, d in rows]
        A0 = tp["A0"]
        s = tp["P"] / A0
        e = tp["d_gage"] / L0
        i_u = int(np.argmax(tp["P"]))
        # post-test measurements (elastic strain recovered)
        Lf = tp["ell"] * math.exp(tp["ep_z"][-1]) + (L0 - tp["ell"]) * math.exp(tp["ep_r"][-1])
        df = sp["d0"] * math.sqrt(1 - sp["delta"]) * math.exp(-tp["ep_z"][-1] / 2)
        Lf_meas = round(Lf * 1e3 + (sp["L0_meas"] - 50.0) + rng.normal(0, 0.04), 2)
        df_meas = [round(df * 1e3 + rng.normal(0, 0.02), 2) for _ in range(2)]
        truth[key] = dict(
            label=sp["label"], E_GPa=sp["E"] / 1e9, d0_mm=sp["d0"] * 1e3, A0_mm2=A0 * 1e6, delta=sp["delta"],
            neck_zone_mm=tp["ell"] * 1e3, compliance_mm_per_kN=C_M * 1e6, toe_mm=TOE * 1e3,
            sigma_U_MPa=float(s[i_u] / 1e6), e_at_max_load=float(e[i_u]), P_max_N=float(tp["P"][i_u]),
            P_fracture_N=float(tp["P"][-1]), e_fracture_gage=float(e[-1]),
            true_stress_neck_fracture_MPa=float(tp["P"][-1] / (A0 * (1 - sp["delta"]) * math.exp(-tp["ep_z"][-1])) / 1e6),
            Lf_mm=Lf * 1e3, df_mm=df * 1e3, eps_f_zone=tp["eps_f"],
            **({"sigma_uy_MPa": sp["s_uy"] / 1e6, "sigma_ly_MPa": sp["s_ly"] / 1e6, "eps_L": sp["eps_L"],
                "K_MPa": sp["K"] / 1e6, "n": sp["n"]} if "s_uy" in sp else
               {"sigma_02_true_MPa": sp["s02"] / 1e6, "RO_m": sp["m"]}),
            ext_removed_at_time_s=info["t_ext_off"], rows=info["n"])
        meas[key] = dict(label=sp["label"], d0_readings_mm=sp["d0_readings"], L0_mm=sp["L0_meas"],
                         Lf_mm=Lf_meas, df_readings_mm=df_meas, extensometer_gage_mm=50.0,
                         reduced_section_mm=LC * 1e3)
    (LAB / "sample_data.csv").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (HERE / "truth.json").write_text(json.dumps(truth, indent=2))
    (HERE / "specimen_measurements.json").write_text(json.dumps(meas, indent=2))
    print(json.dumps(truth, indent=1))
    print(json.dumps(meas, indent=1))


if __name__ == "__main__":
    main()

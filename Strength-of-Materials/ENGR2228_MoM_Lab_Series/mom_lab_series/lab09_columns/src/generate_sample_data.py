"""Generate realistic sample data for Lab 9 (columns) from a known truth model.

    python3 generate_sample_data.py   ->  ../sample_data.csv, truth.json, specimen_measurements.json

Specimens: 6061-T6 bar 25.4 x 6.35 mm (the Lab 2 stock), buckling about the weak axis.
  Part A: pinned ends (knife edges), lengths 300, 450 and 600 mm between pivots; load steps until the lateral
          deflection at mid-length reaches L/60.
  Part B: a 680 mm bar in clamp blocks (40 mm gripped at each end): fixed-fixed with 600 mm free length, then the top
          clamp replaced by a knife edge: fixed-pinned with 640 mm free length.
  Part C: the 450 mm bar from Part A with its ends in V-grooves offset 1 mm and then 2 mm from the axis (eccentric
          load, Beer Sec. 10.2).
  Part D: instructor demonstration in the 100 kN UTM: a 90 mm bar between hardened V-block pivots, loaded past its
          maximum load (inelastic buckling).
Truth model: Hermite finite elements (64 elements) with the stress-free bow (a half sine plus a small third harmonic),
end eccentricities on the -y side and, for the clamps, rotational springs; Part D by the fiber model with Lab 1's
Ramberg-Osgood curve. Instrument errors: load-cell gain, dial-gage resolution and noise, gage-factor errors and noise.
"""
import json
import math
from pathlib import Path

import numpy as np

import lab09_model as LM

HERE = Path(__file__).resolve().parent
LAB = HERE.parent
rng = np.random.default_rng(20260520)
NE = 64
TRUTH = dict(
    E=68.9e9, b=25.42e-3, t=6.350e-3, s02=274e6, m=17,
    load_gain=1.003,                     # the 5 kN load cell reads 0.3 % high (inside its +/-0.5 % specification)
    utm_gain=0.998,                      # the 100 kN UTM reads 0.2 % low
    e_knife=0.08e-3,                     # knife edges: the load line sits 0.08 mm off the bar's axis (same side at both ends)
    e_clamp=0.05e-3,
    k_clamp=(2450.0, 2580.0),            # rotational stiffness of the bottom and top clamp blocks, N m/rad
    gf_err=(0.004, -0.002),              # front and back gage-factor errors (indicated / true - 1)
    noise_ue=1.5e-6, dial_noise=0.003e-3,
    A={300: dict(L=0.3002, d0=0.28e-3, d3=0.03e-3), 450: dict(L=0.4498, d0=0.43e-3, d3=-0.04e-3), 600: dict(L=0.6003, d0=0.66e-3, d3=0.05e-3)},
    B=dict(Lff=0.6004, Lfp=0.6402, d0=0.52e-3, d3=0.02e-3),
    C={1: 1.01e-3, 2: 1.98e-3},          # true groove offsets for the nominal 1 and 2 mm
    D=dict(L=0.0901, d0=0.03e-3, e=0.05e-3),
)
COLS = ["part", "config", "L_mm", "e_mm", "step", "load_N", "defl_mm", "eps_front_ue", "eps_back_ue"]


def sec():
    return LM.rect(TRUTH["b"], TRUTH["t"])


def response(P, L, ends, d0, d3, e):
    """True mid-length deflection change and the front/back surface strains (tension +) at load P."""
    T = TRUTH
    s = sec()
    EI = T["E"] * s["I"]
    xn, v, w0 = LM.fe_imperfect(EI, L, NE, ends, P, d0, e, e, harmonics=((d3, 3),))
    dmid = float((v - w0)[NE])                       # node NE/2 sits at mid-length: index 2*(NE/2) = NE
    kap = LM.fe_curv_mid(v, w0, L, NE)
    ea = -P / (T["E"] * s["A"])
    return dmid, ea - kap * s["c"], ea + kap * s["c"], float(np.max(np.abs(v - w0)))


def predicted_pcr(L_show, K):
    """The pre-lab prediction that sets the switch from load steps to deflection steps: Euler with Lab 2's E, the
    nominal 25.4 x 6.35 mm section and Beer's ideal effective length."""
    s = LM.rect(25.4e-3, 6.35e-3)
    return LM.euler(68.46e9, s["I"], K * L_show / 1e3)


def run_test(part, cfg, L_show, e_show, L, ends, d0, d3, e, step, limit, K_ideal, rows, rec):
    """Load steps of `step` up to 75 % of the predicted P_cr, then (screw advanced) deflection steps of L/600 until the
    dial reads L/60. Stops early if the dial reaches L/60 during the load steps."""
    T = TRUTH
    s = sec()
    EI = T["E"] * s["I"]
    Pcr_true = LM.fe_pcr(EI, L, NE, ends)[0]
    i = 0

    def record(P_show, P):
        d, ef, eb, dmax = response(P, L, ends, d0, d3, e)
        dial = round((d + rng.normal(0, T["dial_noise"])) * 1e3, 2)
        gf, gb = (1 + T["gf_err"][0]) * ef + rng.normal(0, T["noise_ue"]), (1 + T["gf_err"][1]) * eb + rng.normal(0, T["noise_ue"])
        rows.append(dict(part=part, config=cfg, L_mm=f"{L_show:.1f}", e_mm=f"{e_show:.1f}", step=len([r for r in rows if r["part"] == part and r["config"] == cfg and r["L_mm"] == f"{L_show:.1f}" and r["e_mm"] == f"{e_show:.1f}"]),
                         load_N=f"{P_show:.0f}", defl_mm=f"{dial + 0.0:.2f}", eps_front_ue=str(int(round(gf * 1e6))), eps_back_ue=str(int(round(gb * 1e6)))))
        smax = P / s["A"] + abs(ef - eb) / 2 * T["E"]
        rec.append(dict(part=part, config=cfg, L=L, P=P, d=d, ef=ef, eb=eb, smax=smax, Pcr_true=Pcr_true))
        return dial
    switch = 0.75 * predicted_pcr(L_show, K_ideal)
    dial = 0.0
    while step * i <= switch:
        P_show = step * i
        dial = record(P_show, P_show / T["load_gain"])
        if dial >= limit * 1e3:
            return
        i += 1
    dstep = round(L_show / 600, 2)
    target = (math.floor(dial / dstep) + 1) * dstep
    while target <= limit * 1e3 + 1e-9:
        f = lambda P: response(P, L, ends, d0, d3, e)[0] * 1e3 - target   # noqa: E731
        P = brent(f, step * (i - 1) / T["load_gain"], Pcr_true * (1 - 1e-9))
        record(round(P * T["load_gain"]), P)
        target = round(target + dstep, 6)


def brent(f, a, b):
    from scipy import optimize
    return optimize.brentq(f, a, b, xtol=1e-6)


def part_d(rows, rec):
    T, D = TRUTH, TRUTH["D"]
    ds, Ps, Pm = LM.fiber_path(T["b"], T["t"], D["L"], T["E"], T["s02"], T["m"], D["d0"], D["e"], dmax=2.4e-3, nstep=480, nf=80)
    ipk = int(np.argmax(Ps))
    rec.append(dict(part="D", Pmax=Pm, d_at_Pmax=float(ds[ipk])))
    pts = []
    for Pshow in np.arange(4000, 0.93 * Pm * T["utm_gain"], 4000.0):        # rising branch, every 4 kN
        Pt = Pshow / T["utm_gain"]
        d = float(np.interp(Pt, Ps[:ipk + 1], ds[:ipk + 1]))
        pts.append((Pshow, d))
    d_start = float(np.interp(0.93 * Pm, Ps[:ipk + 1], ds[:ipk + 1]))
    d = math.ceil(d_start / 0.05e-3) * 0.05e-3
    while d <= ds[-1]:
        Pt = float(np.interp(d, ds, Ps))
        pts.append((Pt * T["utm_gain"], d))
        if d > ds[ipk] and Pt < 0.85 * Pm:
            break
        d += 0.05e-3
    rows.append(dict(part="D", config="short", L_mm="90.0", e_mm="0.0", step=0, load_N="0", defl_mm="0.00", eps_front_ue="", eps_back_ue=""))
    for i, (Pshow, d) in enumerate(pts, start=1):
        dial = round((d + rng.normal(0, T["dial_noise"])) * 1e3, 2)
        rows.append(dict(part="D", config="short", L_mm="90.0", e_mm="0.0", step=i, load_N=f"{Pshow:.0f}", defl_mm=f"{max(dial, 0):.2f}",
                         eps_front_ue="", eps_back_ue=""))


def main():
    T = TRUTH
    rows, rec = [], []
    pin = dict(v=True, k=0.0)
    for Ln, step in ((300, 250), (450, 100), (600, 50)):
        a = T["A"][Ln]
        run_test("A", "pinned", Ln, 0.0, a["L"], (pin, pin), a["d0"], a["d3"], T["e_knife"], step, Ln / 60e3, 1.0, rows, rec)
    kbot, ktop = T["k_clamp"]
    b = T["B"]
    run_test("B", "fixed-fixed", 600, 0.0, b["Lff"], (dict(v=True, k=ktop), dict(v=True, k=kbot)), b["d0"], b["d3"], T["e_clamp"], 250, 600 / 60e3, 0.5, rows, rec)
    run_test("B", "fixed-pinned", 640, 0.0, b["Lfp"], (dict(v=True, k=0.0), dict(v=True, k=kbot)), b["d0"], b["d3"], T["e_clamp"], 100, 10 * round(640 / 600, 2) / 1e3, LM.K_FACTORS["fixed-pinned"], rows, rec)  # ten 1.07 mm steps, = L/60 to the dial step
    a = T["A"][450]
    for en in (1, 2):
        run_test("C", "eccentric", 450, float(en), a["L"], (pin, pin), a["d0"], a["d3"], T["C"][en] + T["e_knife"], 100, 450 / 60e3, 1.0, rows, rec)
    part_d(rows, rec)
    lines = [",".join(COLS)] + [",".join(str(r[c]) for c in COLS) for r in rows]
    (LAB / "sample_data.csv").write_text("\n".join(lines) + "\n")
    (HERE / "truth.json").write_text(json.dumps(dict(T, rec=rec, A={str(k): v for k, v in T["A"].items()}, C={str(k): v for k, v in T["C"].items()}), indent=1, default=float))
    meas = dict(
        bar=dict(b_mm=[25.41, 25.43, 25.42, 25.42], t_mm=[6.35, 6.36, 6.34, 6.35], stock="6061-T6, 25.4 x 6.35 mm (the Lab 2 bar stock)"),
        lengths_mm={"A300": 300.0, "A450": 450.0, "A600": 600.5, "Bff": 600.5, "Bfp": 640.0, "D": 90.0},
        bow_mm={"A300": 0.26, "A450": 0.46, "A600": 0.62, "B": 0.50, "D": 0.03},
        offsets_mm={"C1": 1.0, "C2": 2.0, "tolerance": 0.02},
        clamp_grip_mm=40.0, bar_B_length_mm=680.0,
        gage=dict(GF=2.10, GF_tol_pct=0.5, location="mid-length, centered on both wide faces (front = convex side)"),
        micrometer_accuracy_mm=0.003, rule_accuracy_mm=0.5, dial_division_mm=0.01, dial_accuracy_mm=0.01,
        loadcell_capacity_N=5000, loadcell_accuracy_pct=0.5, utm_accuracy_pct=0.5, strain_resolution_ue=1.0,
        reference=dict(E_al_GPa=68.46, u_E_al_GPa=0.47, nu_al=0.3296, u_nu_al=0.0029, sY_al_MPa=273.7, u_sY_al_MPa=1.0, m_RO=17,
                       E_al_lab1_GPa=68.75, u_E_al_lab1_GPa=0.38),
    )
    (HERE / "specimen_measurements.json").write_text(json.dumps(meas, indent=1))
    by = {}
    for r in rows:
        by.setdefault((r["part"], r["config"], r["L_mm"], r["e_mm"]), []).append(r)
    for k, v in by.items():
        print(k, len(v), "rows, last", v[-1]["load_N"], "N", v[-1]["defl_mm"], "mm")
    print("max stress in A-C:", max(r["smax"] for r in rec if r.get("part") in "ABC" and "smax" in r) / 1e6, "MPa;",
          "Part D Pmax", [r for r in rec if r.get("part") == "D"][0]["Pmax"])


if __name__ == "__main__":
    main()

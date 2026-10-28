"""Generate realistic sample data for Lab 5 (transverse shear) from a known truth model.

    python3 generate_sample_data.py   ->  ../sample_data.csv, truth.json, specimen_measurements.json

Part A: the Lab 4 aluminum bar (25.4 x 50.8 mm) in three-point bending over 400 mm, upright and flat, with +-45 degree
gage pairs at the neutral axis on the faces, 100 mm from the left support. Truth: Saint-Venant flexure solution for a
rectangle (edge stress above VQ/Ib, depending on b/h and nu), a 0.3 mm load eccentricity (twist, opposite on the two
faces), gages slightly off the neutral axis, a common +0.4 % gage-factor error and 1 microstrain noise.
Part B: a 6061-T6 extruded I-beam: web gage pairs at three heights (900 mm span), and midspan deflection at five spans
(Timoshenko beam with the energy shear factor; LVDT gain +0.3 %, 0.5 micrometer noise).
Part C: two 50.8 x 12.7 mm bars over 600 mm: loose, six bolts (discrete springs, 40 kN/mm each) and bonded (epoxy
layer of finite shear stiffness); midspan deflection and end slip; Timoshenko shear term added.
"""
import json
import math
from pathlib import Path

import numpy as np

import lab05_model as LM

HERE = Path(__file__).resolve().parent
LAB = HERE.parent
rng = np.random.default_rng(20260415)

E, NU = 68.9e9, 0.330
G = E / (2 * (1 + NU))
TRUTH = dict(
    E=E, nu=NU, G=G, gf_error=0.004, lvdt_gain=1.003,
    barA=dict(b=25.42e-3, h=50.78e-3, L=0.400, xg=0.100, ecc=0.3e-3, dy_front=0.15e-3, dy_back=-0.10e-3),
    ibeam=dict(B=76.20e-3, H=101.60e-3, tf=6.35e-3, tw=4.80e-3, L_web=0.900, xg=0.225, yg=[0.2e-3, 22.4e-3, 41.1e-3],
               spans=[0.300, 0.450, 0.600, 0.900, 1.200]),
    layered=dict(b=50.82e-3, t1=12.71e-3, t2=12.69e-3, L=0.600, bolts=[0.05, 0.15, 0.25, 0.35, 0.45, 0.55], kb=40e6,
                 G_glue=1.2e9, t_glue=0.15e-3),
)
COLS = ["part", "config", "span_mm", "step", "load_N", "defl_mm", "slip_mm",
        "gA_p45_ue", "gA_m45_ue", "gB_p45_ue", "gB_m45_ue", "gC_p45_ue", "gC_m45_ue", "gD_p45_ue", "gD_m45_ue",
        "gE_p45_ue", "gE_m45_ue", "gF_p45_ue", "gF_m45_ue"]


def q(x):
    return int(round(x))


def reading(e):
    return q(1e6 * e * (1 + TRUTH["gf_error"]) + rng.normal(0, 1.0))


def pair(gxy, ex):
    """+-45 degree gage readings for in-plane shear strain gxy and axial strain ex (uniaxial stress: ey = -nu ex)."""
    ey = -NU * ex
    m = (ex + ey) / 2
    return reading(m + gxy / 2), reading(m - gxy / 2)


def blank_row(**kw):
    r = {c: "" for c in COLS}
    r.update(kw)
    return r


def part_a(rows):
    t = TRUTH["barA"]
    out = {}
    for cfg, b, h, loads in (("upright", t["b"], t["h"], [0, 2.5e3, 5e3, 7.5e3, 10e3, 12.5e3, 15e3, 0]),
                             ("flat", t["h"], t["b"], [0, 1.25e3, 2.5e3, 3.75e3, 5e3, 6.25e3, 7.5e3, 0])):
        A, I = b * h, b * h ** 3 / 12
        ratio = LM.rect_edge_ratio_xseries(b, h, NU)
        out[cfg] = dict(b=b, h=h, ratio=ratio)
        # twist from the load eccentricity: tau at the middle of the gaged face (long side a, short side s)
        a_, s_ = max(b, h), min(b, h)
        for i, P in enumerate(loads):
            V = P / 2
            tau = ratio * 1.5 * V / A                       # edge value on the neutral axis
            T = V * t["ecc"]
            tauT = T / (0.246 * a_ * s_ ** 2) * (1.0 if h >= b else 0.79)   # middle of a long side / of a short side
            M = V * t["xg"]
            gF = -(tau + tauT) / G                          # Beer's V > 0: tau_xy < 0 in the left shear span
            gB = -(tau - tauT) / G
            exF = -M * t["dy_front"] / (E * I)
            exB = -M * t["dy_back"] / (E * I)
            Pm = P + (rng.normal(0, 3) if P else rng.normal(0, 1))
            pA, mA = pair(gF, exF)
            pB, mB = pair(gB, exB)
            rows.append(blank_row(part="A", config=cfg, span_mm=f"{t['L'] * 1e3:.1f}", step=i, load_N=q(Pm),
                                  gA_p45_ue=pA, gA_m45_ue=mA, gB_p45_ue=pB, gB_m45_ue=mB))
    return out


def part_b(rows):
    t = TRUTH["ibeam"]
    lay = LM.ibeam(t["B"], t["H"], t["tf"], t["tw"])
    pr = LM.props(lay)
    fs = LM.form_factor(lay)
    info = dict(A=pr["A"], I=pr["I"], fs=fs, tau_per_V=[])
    for yg in t["yg"]:
        info["tau_per_V"].append(LM.Q_at(lay, pr["ybar"] + yg, pr["ybar"]) / (pr["I"] * t["tw"]))
    for i, P in enumerate([0, 5e3, 10e3, 15e3, 20e3, 0]):
        V = P / 2
        M = V * t["xg"]
        g = []
        for j, yg in enumerate(t["yg"]):
            tau = V * info["tau_per_V"][j]
            ex = -M * yg / (E * pr["I"])
            for side_tw in (1.0, -1.0):                     # web plate bending from a small out-of-plane load: +-1.5 % of tau
                g.append(pair(-tau * (1 + 0.015 * side_tw) / G, ex))
        Pm = P + (rng.normal(0, 4) if P else rng.normal(0, 1))
        rows.append(blank_row(part="B", config="web", span_mm=f"{t['L_web'] * 1e3:.1f}", step=i, load_N=q(Pm),
                              gA_p45_ue=g[0][0], gA_m45_ue=g[0][1], gB_p45_ue=g[1][0], gB_m45_ue=g[1][1],
                              gC_p45_ue=g[2][0], gC_m45_ue=g[2][1], gD_p45_ue=g[3][0], gD_m45_ue=g[3][1],
                              gE_p45_ue=g[4][0], gE_m45_ue=g[4][1], gF_p45_ue=g[5][0], gF_m45_ue=g[5][1]))
    info["defl"] = {}
    for L in t["spans"]:
        loads = [0, 5e3, 10e3, 15e3, 20e3] if L < 1.0 else [0, 5e3, 10e3, 15e3]
        db, ds = LM.timoshenko_delta(1.0, L, E, G, pr["I"], pr["A"], fs)
        info["defl"][f"{L * 1e3:.0f}"] = dict(bend=db, shear=ds)
        for i, P in enumerate(loads + [0]):
            d = P * (db + ds) * TRUTH["lvdt_gain"] + rng.normal(0, 0.5e-6)
            Pm = P + (rng.normal(0, 4) if P else rng.normal(0, 1))
            rows.append(blank_row(part="B", config="deflection", span_mm=f"{L * 1e3:.1f}", step=i, load_N=q(Pm),
                                  defl_mm=f"{max(d, -0.0005) * 1e3:.3f}"))
    return info


def part_c(rows):
    t = TRUTH["layered"]
    geom = LM.two_layer(t["b"], t["t1"], t["t2"], E)
    A = t["b"] * (t["t1"] + t["t2"])
    L = t["L"]
    info = dict(geom=geom)
    k_glue = t["G_glue"] * t["b"] / t["t_glue"]
    for cfg, loads in (("loose", [0, 500, 1000, 1500, 2000, 0]), ("bolted", [0, 500, 1000, 1500, 2000, 2500, 0]),
                       ("bonded", [0, 500, 1000, 1500, 2000, 2500, 3000, 3500, 4000, 0])):
        load = dict(kind="point", P=1.0)
        if cfg == "loose":
            d1, s1 = LM.loose_delta(geom, L, load), geom["r"] * load["P"] * L ** 2 / (16 * geom["EI0"])
        elif cfg == "bolted":
            sol = LM.bolts_shoot(geom, L, load, t["bolts"], t["kb"])
            d1, s1 = sol["delta"], sol["slip0"]
            info["bolt_forces_per_N"] = sol["forces"]
        else:
            sol = LM.smeared_bvp(geom, L, load, k_glue)
            d1, s1 = sol["delta"], sol["slip0"]
        dsh = 1.2 * L / (4 * G * A)                          # Timoshenko shear term (rectangle, whole section)
        info[cfg] = dict(delta_per_N=d1 + dsh, delta_bend_per_N=d1, slip_per_N=abs(s1))
        for i, P in enumerate(loads):
            d = P * (d1 + dsh) * TRUTH["lvdt_gain"] + rng.normal(0, 0.5e-6)
            sl = P * abs(s1) + rng.normal(0, 0.4e-6)          # dial gage reads the magnitude of the end slip
            Pm = P + (rng.normal(0, 2) if P else rng.normal(0, 0.5))
            rows.append(blank_row(part="C", config=cfg, span_mm=f"{L * 1e3:.1f}", step=i, load_N=q(Pm),
                                  defl_mm=f"{d * 1e3:.3f}", slip_mm=f"{sl * 1e3:.3f}"))
    info["k_glue"] = k_glue
    return info


def main():
    rows = []
    a = part_a(rows)
    b = part_b(rows)
    c = part_c(rows)
    lines = [",".join(COLS)] + [",".join(str(r[c_]) for c_ in COLS) for r in rows]
    (LAB / "sample_data.csv").write_text("\n".join(lines) + "\n")
    truth = dict(TRUTH, partA=a, partB=b, partC=c)
    (HERE / "truth.json").write_text(json.dumps(truth, indent=1, default=float))
    meas = dict(
        barA=dict(b_mm=[25.43, 25.41, 25.42], h_mm=[50.79, 50.77, 50.78], span_mm=400.0, x_gage_mm=100.0),
        ibeam=dict(H_mm=[101.62, 101.58, 101.60], B_mm=[76.19, 76.21, 76.22], tf_mm=[6.36, 6.34, 6.35, 6.36], tw_mm=[4.801, 4.797, 4.803],
                   gage_height_mm=[50.98, 73.17, 91.93], span_web_mm=900.0, x_gage_mm=225.0, spans_mm=[300.0, 450.0, 600.0, 900.0, 1200.0]),
        layered=dict(b_mm=[50.81, 50.83, 50.82], t_top_mm=[12.71, 12.70, 12.72], t_bot_mm=[12.69, 12.70, 12.68], span_mm=600.0,
                     bolts_mm=[50.0, 150.0, 250.0, 350.0, 450.0, 550.0]),
        caliper_accuracy_mm=0.02, micrometer_accuracy_mm=0.003, height_gage_accuracy_mm=0.05, span_accuracy_mm=0.5,
        gage_factor_tolerance_pct=1.0, load_cell_accuracy_pct=0.5, lvdt_accuracy_pct=0.5, lvdt_resolution_mm=0.001, slip_resolution_mm=0.001,
        reference=dict(E_al_GPa=68.46, u_E_al_GPa=0.47, nu_al=0.330, u_nu_al=0.003, G_al_GPa=26.03, u_G_al_GPa=0.12,
                       sY_al_MPa=273.7, u_sY_al_MPa=1.0, tauY_al_MPa=150.8, u_tauY_al_MPa=0.5),
    )
    (HERE / "specimen_measurements.json").write_text(json.dumps(meas, indent=1))
    print(len(rows), "rows; edge ratios", {k: round(v["ratio"], 4) for k, v in a.items()}, "I-beam fs", round(b["fs"], 4))


if __name__ == "__main__":
    main()

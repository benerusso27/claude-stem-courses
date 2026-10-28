"""Generate realistic sample data for Lab 7 (deflection of beams) from a known truth model.

    python3 generate_sample_data.py   ->  ../sample_data.csv, truth.json, specimen_measurements.json

Part A: the 1018 steel bar (25.4 x 6.35 mm) simply supported on knife edges 800 mm apart; hangers at 200 and 600 mm;
digital indicators at 200, 400 and 600 mm. Load at 600, then at 200, then both.
Part B: the same bar clamped at one end. B1 cantilever with a tip load at 700 mm (indicators at 350 and 700); B2 propped
on a load cell at 700 mm with a load at 350 mm; B3 the prop lowered 0.500 mm under load. Truth: the clamp has a finite
rotational stiffness k.
Part C: a blue-tempered spring-steel strip (12.7 x 0.79 mm) clamped in a vise, 250 mm to the load point, loaded by a
hanging mass at the tip until the deflection is large; tip position read on a grid board. Truth: the elastica with the
strip's own weight.
Truth errors: gage positions and spans off by a few tenths of a mm, mass tolerance, indicator and load-cell noise.
"""
import json
import math
from pathlib import Path

import numpy as np

import lab07_model as LM

HERE = Path(__file__).resolve().parent
LAB = HERE.parent
rng = np.random.default_rng(20260506)
G = 9.80665
TRUTH = dict(
    g=G, mass_err=0.0005,
    bar=dict(E=205e9, b=25.43e-3, h=6.362e-3, rho=7850.0),
    A=dict(L=0.8003, xP=[0.1996, 0.6004], xg=[0.2005, 0.3998, 0.6002], noise=1.5e-6),
    B=dict(L=0.7004, k=4500.0, xg=[0.3503, 0.6996], xP_tip=0.7000, xP_mid=0.3498, settle=0.502e-3, noise=1.5e-6, lc_noise=0.01, lc_gain=1.003),
    C=dict(E=203e9, b=12.70e-3, t=0.787e-3, L=0.2504, rho=7850.0, read_noise=0.25e-3),
)
COLS = ["part", "config", "step", "mass_kg", "load_pos_mm", "d1_mm", "d2_mm", "d3_mm", "R_N", "x_tip_mm", "y_tip_mm"]


def EIbar():
    t = TRUTH["bar"]
    return t["E"] * t["b"] * t["h"] ** 3 / 12


def blank(**kw):
    r = {c: "" for c in COLS}
    r.update(kw)
    return r


def mval(m):
    return m * (1 + TRUTH["mass_err"] * rng.uniform(-1, 1)) if m else 0.0


def part_a(rows):
    t = TRUTH["A"]
    EI = EIbar()
    out = {}
    plan = (("P600", [(0.6004, m) for m in (0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0)]),
            ("P200", [(0.1996, m) for m in (0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0)]),
            ("both", [None, (0.6004, 2.0, 0.1996, 1.0)]))
    for cfg, steps in plan:
        out[cfg] = []
        for i, st in enumerate(steps):
            if cfg == "both":
                if st is None:
                    loads, mass, pos = [], 0.0, "600+200"
                else:
                    loads = [(mval(st[1]) * G, st[0]), (mval(st[3]) * G, st[2])]
                    mass, pos = st[1] + st[3], "600+200"
            else:
                m = st[1]
                loads = [(mval(m) * G, st[0])] if m else []
                mass, pos = m, "600" if cfg == "P600" else "200"
            beam = dict(family="ss", L=t["L"], EI=EI, P=loads)
            d = -LM.closed_form(beam, np.array(t["xg"]))["y"]           # downward deflection
            d = d + rng.normal(0, t["noise"], 3)
            rows.append(blank(part="A", config=cfg, step=i, mass_kg=f"{mass:.2f}", load_pos_mm=pos,
                              d1_mm=f"{d[0] * 1e3:.3f}", d2_mm=f"{d[1] * 1e3:.3f}", d3_mm=f"{d[2] * 1e3:.3f}"))
            out[cfg].append(dict(loads=loads, d=list(d)))
    return out


def part_b(rows):
    t = TRUTH["B"]
    EI = EIbar()
    out = {}
    # B1 cantilever, tip load
    out["cant"] = []
    for i, m in enumerate((0, 0.2, 0.4, 0.6, 0.8, 1.0)):
        loads = [(mval(m) * G, t["xP_tip"])] if m else []
        beam = dict(family="cant", L=t["L"], EI=EI, P=loads, k=t["k"])
        d = -LM.closed_form(beam, np.array(t["xg"]))["y"] + rng.normal(0, t["noise"], 2)
        rows.append(blank(part="B", config="cantilever", step=i, mass_kg=f"{m:.2f}", load_pos_mm="700",
                          d1_mm=f"{d[0] * 1e3:.3f}", d2_mm=f"{d[1] * 1e3:.3f}"))
        out["cant"].append(dict(P=loads[0][0] if loads else 0.0, d=list(d)))
    # B2 propped, load at mid-length; B3 prop lowered at 3 kg
    out["prop"] = []
    for i, m in enumerate((0, 1.0, 2.0, 3.0, 4.0)):
        loads = [(mval(m) * G, t["xP_mid"])] if m else []
        beam = dict(family="propped", L=t["L"], EI=EI, P=loads, k=t["k"])
        cf = LM.closed_form(beam, np.array([t["xg"][0]]))
        d = -cf["y"][0] + rng.normal(0, t["noise"])
        R = cf["R"]["RB"] * t["lc_gain"] + rng.normal(0, t["lc_noise"])
        rows.append(blank(part="B", config="propped", step=i, mass_kg=f"{m:.2f}", load_pos_mm="350",
                          d1_mm=f"{d * 1e3:.3f}", R_N=f"{R:.2f}"))
        out["prop"].append(dict(P=loads[0][0] if loads else 0.0, R=cf["R"]["RB"], d=d))
    Pset = 3.0 * G * (1 + TRUTH["mass_err"] * 0.3)
    for i, s in enumerate((0.0, -t["settle"])):
        beam = dict(family="propped", L=t["L"], EI=EI, P=[(Pset, t["xP_mid"])], k=t["k"], s=s)
        cf = LM.closed_form(beam, np.array([t["xg"][0]]))
        d = -cf["y"][0] + rng.normal(0, t["noise"])
        R = cf["R"]["RB"] * t["lc_gain"] + rng.normal(0, t["lc_noise"])
        rows.append(blank(part="B", config="settlement", step=i, mass_kg="3.00", load_pos_mm="350",
                          d1_mm=f"{d * 1e3:.3f}", R_N=f"{R:.2f}"))
        out.setdefault("settle", []).append(dict(s=s, R=cf["R"]["RB"]))
    return out


def part_c(rows):
    t = TRUTH["C"]
    I = t["b"] * t["t"] ** 3 / 12
    EI = t["E"] * I
    w = t["rho"] * G * t["b"] * t["t"]
    beta = w * t["L"] ** 3 / EI
    out = dict(EI=EI, beta=beta, w=w, pts=[])
    for i, m in enumerate((0, 0.02, 0.04, 0.07, 0.12, 0.17, 0.22, 0.32, 0.42, 0.52, 0.62)):
        P = mval(m) * G
        alpha = P * t["L"] ** 2 / EI
        _, dv, xt, _ = LM.elastica_bvp(alpha, beta)
        x = xt * t["L"] + rng.normal(0, t["read_noise"])
        y = -dv * t["L"] + rng.normal(0, t["read_noise"])
        rows.append(blank(part="C", config="elastica", step=i, mass_kg=f"{m:.2f}", load_pos_mm="250",
                          x_tip_mm=f"{x * 1e3:.1f}", y_tip_mm=f"{y * 1e3:.1f}"))
        out["pts"].append(dict(P=P, alpha=alpha, dv=dv, xt=xt))
    return out


def main():
    rows = []
    a = part_a(rows)
    b = part_b(rows)
    c = part_c(rows)
    lines = [",".join(COLS)] + [",".join(str(r[c_]) for c_ in COLS) for r in rows]
    (LAB / "sample_data.csv").write_text("\n".join(lines) + "\n")
    truth = dict(TRUTH, EI_bar=EIbar(), partA=a, partB=b, partC=c)
    (HERE / "truth.json").write_text(json.dumps(truth, indent=1, default=float))
    meas = dict(
        bar=dict(b_mm=[25.42, 25.44, 25.43], h_mm=[6.361, 6.363, 6.362, 6.362]),
        A=dict(span_mm=800.0, load_x_mm=[200.0, 600.0], gage_x_mm=[200.0, 400.0, 600.0]),
        B=dict(L_mm=700.0, gage_x_mm=[350.0, 700.0], tip_load_x_mm=700.0, mid_load_x_mm=350.0, settle_mm=0.500),
        C=dict(b_mm=[12.70, 12.71, 12.69], t_mm=[0.787, 0.788, 0.786, 0.787], L_mm=250.0, rho_kg_m3=7850.0, hanger_kg=0.020),
        g=G, mass_tolerance_pct=0.1, caliper_accuracy_mm=0.02, micrometer_accuracy_mm=0.003, rule_accuracy_mm=0.5,
        indicator_accuracy_mm=0.003, indicator_resolution_mm=0.001, loadcell_accuracy_pct=0.5, loadcell_resolution_N=0.01,
        grid_reading_mm=0.5, prop_screw_accuracy_mm=0.005,
        reference=dict(E_st_GPa=205.2, u_E_st_GPa=1.2, sY_st_MPa=296.2, u_sY_st_MPa=1.1, E_al_GPa=68.46, u_E_al_GPa=0.47,
                       sY_al_MPa=273.7, u_sY_al_MPa=1.0, sY_spring_MPa_min=1300.0),
    )
    (HERE / "specimen_measurements.json").write_text(json.dumps(meas, indent=1))
    print(len(rows), "rows; EI bar", EIbar(), "strip EI", c["EI"], "beta", c["beta"])


if __name__ == "__main__":
    main()

"""Generate realistic sample data for Lab 4 (bending) from a known truth model.

    python3 generate_sample_data.py   ->  ../sample_data.csv, truth.json, specimen_measurements.json

Part A: 6061-T6 bar in 4-point bending, elastic (0-20 kN). Part B: the same section with a 1018 steel strip
bonded to its bottom face, elastic (0-15 kN). Part C: the Part A bar loaded beyond yield (to 40 kN) and unloaded.
Plane sections remain plane in the truth model; the stresses follow Lab 1's Ramberg-Osgood curve for 6061-T6.
Imperfections: gage heights differ slightly from nominal, a common +0.5 % gage-factor error, load points
0.4 mm off nominal, reading noise and 1 microstrain resolution.
"""
import json
import warnings
import math
from pathlib import Path

import numpy as np

from lab04_model import composite_props, section_moment

HERE = Path(__file__).resolve().parent
LAB = HERE.parent
rng = np.random.default_rng(20260401)
warnings.filterwarnings("ignore", message="The occurrence of roundoff")

TRUTH = dict(
    al=dict(law="ro", E=68.9e9, sY=274e6, m=17), steel=dict(law="epp", E=205e9, sY=370e6),
    nu_al=0.330, b=25.42e-3, h=50.78e-3, ts=6.36e-3, L=600.0e-3, a1=200.4e-3, a2=399.6e-3,
    gf_error=0.005,
    # true gage heights above the bottom of the aluminum bar (Part A/C) and of the strip (Part B), mm
    yA=[5.62, 15.21, 25.47, 35.18, 45.59], yB=[10.31, 20.18, 30.42, 40.06, 50.27],
    x_bottom=[100.0e-3, 150.0e-3],
)
COLS = ["part", "step", "load_N", "strain_side1_ue", "strain_side2_ue", "strain_side3_ue", "strain_side4_ue", "strain_side5_ue",
        "strain_top_ue", "strain_bottom_ue", "strain_transverse_top_ue", "strain_bottom_x100_ue", "strain_bottom_x150_ue"]


def q(x):
    return int(round(x))


def reading(e):
    return q(1e6 * e * (1 + TRUTH["gf_error"]) + rng.normal(0, 1.0))


def moment_mid(P):
    # reactions with slightly asymmetric load points; the middle segment carries M = R_A a1 - (P/2)(x - a1) ... at midspan
    a1, a2, L = TRUTH["a1"], TRUTH["a2"], TRUTH["L"]
    RA = P / 2 * ((L - a1) + (L - a2)) / L
    xm = L / 2
    return RA * xm - P / 2 * (xm - a1), RA


def part_a(rows):
    t = TRUTH
    I = t["b"] * t["h"] ** 3 / 12
    E = t["al"]["E"]
    loads = [0, 2.5e3, 5e3, 7.5e3, 10e3, 12.5e3, 15e3, 17.5e3, 20e3, 15e3, 10e3, 5e3, 0]
    for i, P in enumerate(loads):
        M, RA = moment_mid(P)
        k = M / (E * I)
        ys = np.array(t["yA"]) * 1e-3
        e = -k * (ys - t["h"] / 2)
        etop, ebot = -k * (t["h"] / 2), k * (t["h"] / 2)
        ex = [RA * x * (t["h"] / 2) / (E * I) for x in t["x_bottom"]]
        Pm = P + (rng.normal(0, 4) if P else rng.normal(0, 2))
        rows.append(dict(part="A", step=i, load_N=q(Pm), **{f"strain_side{j + 1}_ue": reading(e[j]) for j in range(5)},
                         strain_top_ue=reading(etop), strain_bottom_ue=reading(ebot), strain_transverse_top_ue=reading(-t["nu_al"] * etop),
                         strain_bottom_x100_ue=reading(ex[0]), strain_bottom_x150_ue=reading(ex[1])))


def part_b(rows):
    t = TRUTH
    cp = composite_props(t["b"], t["h"], t["ts"], t["al"]["E"], t["steel"]["E"])
    E = t["al"]["E"]
    H = t["h"] + t["ts"]
    loads = [0, 2.5e3, 5e3, 7.5e3, 10e3, 12.5e3, 15e3, 10e3, 5e3, 0]
    for i, P in enumerate(loads):
        M, RA = moment_mid(P)
        k = M / (E * cp["I"])
        ys = np.array(t["yB"]) * 1e-3
        e = -k * (ys - cp["ybar"])
        Pm = P + (rng.normal(0, 4) if P else rng.normal(0, 2))
        rows.append(dict(part="B", step=i, load_N=q(Pm), **{f"strain_side{j + 1}_ue": reading(e[j]) for j in range(5)},
                         strain_top_ue=reading(-k * (H - cp["ybar"])), strain_bottom_ue=reading(-k * (0 - cp["ybar"])),
                         strain_transverse_top_ue=reading(t["nu_al"] * k * (H - cp["ybar"])), strain_bottom_x100_ue="", strain_bottom_x150_ue=""))
    return cp


def kappa_for(M, layers, mats, lo=0.0, hi=1.0):
    """Curvature that gives moment M (bisection on the quadrature moment)."""
    while section_moment(layers, mats, hi)[0] < M:
        hi *= 2
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if section_moment(layers, mats, mid)[0] < M:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def part_c(rows):
    t = TRUTH
    E = t["al"]["E"]
    I = t["b"] * t["h"] ** 3 / 12
    layers = [(0.0, t["h"], t["b"], "al")]
    mats = {"al": t["al"]}
    loads_up = [0, 5e3, 10e3, 15e3, 20e3, 25e3, 28e3, 31e3, 34e3, 37e3, 40e3]
    loads_dn = [30e3, 20e3, 10e3, 0]
    kmax = Mmax = 0.0
    info = {}
    cache = {}
    for i, P in enumerate(loads_up + loads_dn):
        M, RA = moment_mid(P)
        if i < len(loads_up):
            k = kappa_for(M, layers, mats, hi=0.05) if M > 0 else 0.0
            kmax, Mmax = k, M
        else:
            k = kmax - (Mmax - M) / (E * I)               # elastic unloading
        cache[P if i < len(loads_up) else -P - 1] = k
        ys = np.array(t["yA"]) * 1e-3
        e = -k * (ys - t["h"] / 2)
        # outer-span bottom gages: the moment there is RA x; elastic below M_Y except near x = 150 mm at 40 kN (RO is mildly nonlinear)
        ex = []
        for x in t["x_bottom"]:
            Mx = RA * x
            if i < len(loads_up):
                kx = kappa_for(Mx, layers, mats, hi=0.05) if Mx > 0 else 0.0
                info.setdefault("kx_max", {})[f"{x * 1e3:.0f}"] = kx
            else:
                kxm = info["kx_max"][f"{x * 1e3:.0f}"]
                Mxm = moment_mid(40e3)[1] * x
                kx = kxm - (Mxm - Mx) / (E * I)
            ex.append(kx * t["h"] / 2)
        Pm = P + (rng.normal(0, 6) if P else rng.normal(0, 2))
        rows.append(dict(part="C", step=i, load_N=q(Pm), **{f"strain_side{j + 1}_ue": reading(e[j]) for j in range(5)},
                         strain_top_ue=reading(-k * t["h"] / 2), strain_bottom_ue=reading(k * t["h"] / 2),
                         strain_transverse_top_ue=reading(t["nu_al"] * k * t["h"] / 2 if k * t["h"] / 2 < 0.004 else 0.5 * k * t["h"] / 2 - 0.004 * (0.5 - t["nu_al"])),
                         strain_bottom_x100_ue=reading(ex[0]), strain_bottom_x150_ue=reading(ex[1])))
    info.update(kappa_max=kmax, M_max=Mmax, kappa_residual=kmax - Mmax / (E * I))
    return info


def straightedge_gap(P=40e3, bar_len=0.700, n=1401):
    """Gap at midspan under a straightedge laid on the top face after unloading from P (truth model).
    Permanent curvature kp(x) = kappa(M(x)) - M(x)/(EI) along the whole bar, integrated twice; the bar overhangs the
    supports equally. Uses symmetry of the rectangle (NA at mid-depth) for a fast M(kappa) table."""
    from scipy import integrate
    from lab04_model import sigma_of
    t = TRUTH
    E, b, h, L = t["al"]["E"], t["b"], t["h"], t["L"]
    I, c = b * h ** 3 / 12, h / 2
    ks = np.linspace(0, 0.4, 161)
    Ms = np.array([2 * b * integrate.quad(lambda y: y * sigma_of(t["al"], k * y), 0, c, epsrel=1e-10)[0] for k in ks])
    _, RA = moment_mid(P)
    a1, a2 = t["a1"], t["a2"]
    ov = (bar_len - L) / 2
    xs = np.linspace(-ov, L + ov, n)
    M = np.array([0.0 if (x < 0 or x > L) else RA * x - P / 2 * max(0.0, x - a1) - P / 2 * max(0.0, x - a2) for x in xs])
    kp = np.interp(M, Ms, ks) - M / (E * I)
    th = np.concatenate([[0], np.cumsum((kp[1:] + kp[:-1]) / 2 * np.diff(xs))])
    w = np.concatenate([[0], np.cumsum((th[1:] + th[:-1]) / 2 * np.diff(xs))])
    line = w[0] + (w[-1] - w[0]) * (xs - xs[0]) / (xs[-1] - xs[0])
    return float((line - w).max())


def main():
    rows = []
    part_a(rows)
    cp = part_b(rows)
    info = part_c(rows)
    lines = [",".join(COLS)] + [",".join(str(r[c]) for c in COLS) for r in rows]
    (LAB / "sample_data.csv").write_text("\n".join(lines) + "\n")
    t = TRUTH
    I = t["b"] * t["h"] ** 3 / 12
    info["straightedge_gap"] = straightedge_gap()
    truth = dict(t, I_A=I, composite=cp, partC=info, M_at_20kN=moment_mid(20e3)[0], M_at_40kN=moment_mid(40e3)[0])
    (HERE / "truth.json").write_text(json.dumps(truth, indent=1, default=float))
    meas = dict(
        b_mm=[25.43, 25.41, 25.42], h_mm=[50.79, 50.77, 50.78], ts_mm=[6.37, 6.35, 6.36],
        span_mm=600.0, a1_mm=200.0, a2_mm=400.0, x_bottom_mm=[100.0, 150.0],
        yA_mm=[5.65, 15.18, 25.49, 35.15, 45.62], yB_mm=[10.28, 20.21, 30.40, 40.09, 50.25],
        caliper_accuracy_mm=0.02, height_gage_accuracy_mm=0.05, load_position_accuracy_mm=0.5,
        gage_factor_tolerance_pct=1.0, load_cell_accuracy_pct=0.5, bar_length_mm=700.0,
        straightedge_gap_mm=round(info["straightedge_gap"] * 1e3 / 0.05) * 0.05, feeler_resolution_mm=0.05,
        reference=dict(E_al_GPa=68.46, u_E_al_GPa=0.47, nu_al=0.330, u_nu_al=0.003, E_st_GPa=205.0, u_E_st_GPa=3.0,
                       sY_al_MPa=273.7, u_sY_al_MPa=1.0, sY_st_MPa=296.2, u_sY_st_MPa=1.1, m_RO=17),
    )
    (HERE / "specimen_measurements.json").write_text(json.dumps(meas, indent=1))
    print(len(rows), "rows; part C kappa_max", round(info["kappa_max"], 5), "residual", round(info["kappa_residual"], 5))


if __name__ == "__main__":
    main()

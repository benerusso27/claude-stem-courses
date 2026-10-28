"""Generate realistic sample data for Lab 3 (torsion) from a known truth model.

    python3 generate_sample_data.py   ->  ../sample_data.csv, truth.json, specimen_measurements.json

Truth: each specimen is a fiber (ring) model of a circular shaft. Rings load along the material's monotonic
shear curve and unload elastically. The machine reads the torque (load cell with a small gain error and noise),
the troptometer reads the twist over the 50.80 mm gage (until it is removed), and the head encoder reads the
rotation of the grips, which includes the whole 76.2 mm reduced section, the shoulders and grips (compliance C_m)
and a little backlash taken up at low torque.
"""
import json
import math
from pathlib import Path

import numpy as np

from lab03_model import J_polar, tau_of

HERE = Path(__file__).resolve().parent
LAB = HERE.parent
rng = np.random.default_rng(20260318)

L_GAGE, L_RED = 50.80e-3, 76.20e-3
TRUTH = dict(
    steel=dict(law="plateau", G=80.0e9, tauY=171.5e6, gL=0.029, A=394.2e6, n=0.19, gf=1.60, d=6.3500e-3),
    al=dict(law="ro", G=25.9e9, tauY=158.2e6, g0=0.00346, m=17, gf=0.80, d=6.3520e-3),
    ci=dict(law="tanh", G=41.0e9, tauc=450e6, sigUT=214e6, d=6.3480e-3),
    C_m=6.0e-4,              # rad per N·m: shoulders, grips and drive train
    backlash=0.40 * math.pi / 180, backlash_T=0.30,
    torque_gain=1.003,       # load-cell gain error (+0.3 %)
    tropt_gain=0.998,        # troptometer calibration (−0.2 %)
)
RATE_SLOW, RATE_FAST = 0.25, 15.0        # head rate, deg/s
HZ_SLOW, HZ_FAST = 4.0, 2.0


class Shaft:
    """Ring model with loading/unloading memory; vectorized over Gauss–Legendre rings."""

    def __init__(self, m, nr=160):
        self.m = m
        c = m["d"] / 2
        xg, wg = np.polynomial.legendre.leggauss(nr)
        self.r = 0.5 * c * (xg + 1)
        self.w = 0.5 * c * wg
        self.gmax = np.zeros(nr)
        self.tmax = np.zeros(nr)
        # monotonic curve tabulated finely in log-strain for speed (exact laws evaluated at table nodes)
        g = np.r_[0.0, np.logspace(-7, math.log10(5.0), 6000)]
        self.gt, self.tt = g, np.array([tau_of(m, x) for x in g])

    def curve(self, g):
        return np.interp(g, self.gt, self.tt)

    def torque(self, theta, commit=False):
        g = self.r * theta
        load = g >= self.gmax
        tnew = self.curve(g)
        tau = np.where(load, tnew, np.maximum(self.tmax - self.m["G"] * (self.gmax - g), -self.tmax))
        if commit:
            self.gmax = np.where(load, g, self.gmax)
            self.tmax = np.where(load, tnew, self.tmax)
        return float(np.sum(2 * math.pi * self.r ** 2 * tau * self.w))


def head_of(theta, T):
    toe = TRUTH["backlash"] * (1 - math.exp(-abs(T) / TRUTH["backlash_T"]))
    return theta * L_RED + TRUTH["C_m"] * T + toe


def run(key, rows, cycle=False, tropt_off_deg=10.0, tropt=True):
    m = dict(TRUTH[key])
    sh = Shaft(m)
    c = m["d"] / 2
    t, head_prev = 0.0, 0.0
    info = {}

    def sample(theta, phase_rate, tropt_on, fail=False):
        nonlocal t, head_prev
        T = sh.torque(theta, commit=True)
        if fail:                      # specimen broken: torque gone, the head has simply moved on
            T = 0.0
            h = head_prev + math.radians(phase_rate / (HZ_SLOW if phase_rate == RATE_SLOW else HZ_FAST))
            t += 1 / (HZ_SLOW if phase_rate == RATE_SLOW else HZ_FAST)
        else:
            h = head_of(theta, T)
            t += abs(h - head_prev) * 180 / math.pi / phase_rate
        head_prev = h
        Tm = T * TRUTH["torque_gain"] + rng.normal(0, 0.006)
        row = dict(specimen=key, time_s=f"{t:.2f}", torque_Nm=f"{round(Tm / 0.01) * 0.01:.2f}",
                   troptometer_deg=(f"{round((theta * L_GAGE * TRUTH['tropt_gain'] * 180 / math.pi + rng.normal(0, 0.003)) / 0.01) * 0.01:.2f}" if tropt_on else ""),
                   head_deg=f"{round(h * 180 / math.pi / 0.1) * 0.1:.1f}")
        rows.append(row)
        return T

    def step_theta(dhead_deg, theta, T):
        # theta increment that advances the head by about dhead_deg (local tangent of head(theta))
        eps = 1e-7
        dT = (sh.torque(theta + eps) - sh.torque(theta)) / eps
        dh_dth = L_RED + TRUTH["C_m"] * dT
        return math.radians(dhead_deg) / dh_dth

    theta, T = 0.0, 0.0
    sample(0.0, RATE_SLOW, tropt)
    dh_slow = RATE_SLOW / HZ_SLOW
    target_off = math.radians(tropt_off_deg) / L_GAGE if tropt else None
    fracture_by_stress = m["law"] == "tanh"

    def broken(th):
        if fracture_by_stress:
            return tau_of(m, c * th) >= m["sigUT"]
        return c * th >= m["gf"]

    if cycle:
        th_A = 3 * m["tauY"] / (m["G"] * c) * 1.0
        while theta < th_A:
            theta = min(th_A, theta + step_theta(dh_slow, theta, T))
            T = sample(theta, RATE_SLOW, True)
        info["unload_start"] = dict(theta=theta, T=T)
        # unload until the torque is about zero
        while True:
            th_try = theta - step_theta(dh_slow, theta, T)
            if sh.torque(th_try) <= 0.02:
                break
            theta = th_try
            T = sample(theta, RATE_SLOW, True)
        # final unloading point at T = 0 (bisection on the unloading branch)
        lo, hi = 0.0, theta
        for _ in range(80):
            mid = 0.5 * (lo + hi)
            if sh.torque(mid) > 0:
                hi = mid
            else:
                lo = mid
        theta = 0.5 * (lo + hi)
        T = sample(theta, RATE_SLOW, True)
        info["residual_theta"] = theta
    while tropt and theta < target_off:
        theta = min(target_off, theta + step_theta(dh_slow, theta, T))
        if broken(theta):
            break
        T = sample(theta, RATE_SLOW, True)
    if fracture_by_stress or not tropt:
        while not broken(theta):
            theta += step_theta(dh_slow, theta, T)
            if broken(theta):
                break
            T = sample(theta, RATE_SLOW, False)
        info["T_fracture"] = T
        sample(theta, RATE_SLOW, False, fail=True)
        info["theta_fracture"] = theta
        return info
    info["tropt_removed_theta"] = theta
    dh_fast = RATE_FAST / HZ_FAST
    Tmax, th_Tmax = 0.0, 0.0
    while True:
        th_new = theta + step_theta(dh_fast, theta, T)
        if broken(th_new):
            break
        theta = th_new
        T = sample(theta, RATE_FAST, False)
        if T > Tmax:
            Tmax, th_Tmax = T, theta
    info.update(T_max=Tmax, theta_at_Tmax=th_Tmax, theta_fracture_last=theta, T_last=T)
    sample(theta + step_theta(dh_fast, theta, T) * 0.3, RATE_FAST, False, fail=True)
    return info


def main():
    rows = []
    info = dict(steel=run("steel", rows, cycle=True), al=run("al", rows), ci=run("ci", rows, tropt=False))
    cols = ["specimen", "time_s", "torque_Nm", "troptometer_deg", "head_deg"]
    (LAB / "sample_data.csv").write_text(",".join(cols) + "\n" + "\n".join(",".join(r[c] for c in cols) for r in rows) + "\n")
    truth = dict(TRUTH, L_gage=L_GAGE, L_reduced=L_RED, info=info)
    for k in ("steel", "al", "ci"):
        c = TRUTH[k]["d"] / 2
        truth[k]["J_mm4"] = J_polar(c) * 1e12
        if k != "ci":
            truth[k]["TY_Nm"] = TRUTH[k]["tauY"] * J_polar(c) / c
    (HERE / "truth.json").write_text(json.dumps(truth, indent=1, default=float))
    meas = dict(
        d_mm=dict(steel=[6.351, 6.349, 6.350, 6.352, 6.348, 6.350], al=[6.353, 6.351, 6.352, 6.354, 6.350, 6.352],
                  ci=[6.349, 6.347, 6.348, 6.350, 6.346, 6.348]),
        L_gage_mm=50.80, u_L_gage_mm=0.05, L_reduced_mm=76.20,
        micrometer_accuracy_mm=0.003, torque_accuracy_pct=0.5, troptometer_accuracy_pct=0.5,
        fracture=dict(steel="flat, perpendicular to the axis; smeared circular marks", al="flat, perpendicular to the axis",
                      ci="45° helix; granular grey surface"),
        reference=dict(E_steel_GPa=205.0, u_E_steel_GPa=3.0, nu_steel=0.29, u_nu_steel=0.01,
                       E_al_GPa=68.46, u_E_al_GPa=0.47, nu_al=0.330, u_nu_al=0.003,
                       sigUT_ci_MPa=214.0, u_sigUT_ci_MPa=15.0, G_ci_GPa=41.0, sigY_steel_MPa=297.0, sigY_al_MPa=274.0),
    )
    (HERE / "specimen_measurements.json").write_text(json.dumps(meas, indent=1))
    print(len(rows), "rows;", {k: (round(v["T_max"], 3) if "T_max" in v else round(v.get("T_fracture", 0), 3)) for k, v in info.items()})


if __name__ == "__main__":
    main()

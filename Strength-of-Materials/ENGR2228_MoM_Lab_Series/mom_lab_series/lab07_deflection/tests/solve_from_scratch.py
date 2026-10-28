"""Re-solve the handout's questions from scratch and compare with the instructor key.

    python3 tests/solve_from_scratch.py      (from lab07_deflection/)

Independent of src/lab07_analysis.py and src/lab07_model.py: plain csv + numpy/scipy, the handout's equations typed in
again, and deliberately different methods where one exists: E from one global least-squares fit of all twelve Part A
series at once (instead of six separate slopes averaged); EI and k from the closed-form P4 combinations (instead of a
2x2 solve); the propped-cantilever reactions from the stiffness method on a two-element model (instead of Eq. 8);
the elastica by scipy solve_ivp shooting with brentq (instead of elliptic integrals or collocation); D1 by numerical
integration of M/EI on a grid for every candidate. Compares with the numbers printed in the key (src/key_values.json).
"""
import csv
import json
import math
import re
import sys
from pathlib import Path

import numpy as np
from scipy import integrate, optimize

LAB = Path(__file__).resolve().parents[1]
KV = json.loads((LAB / "src" / "key_values.json").read_text())
meas = json.loads((LAB / "src" / "specimen_measurements.json").read_text())
rows = list(csv.DictReader(open(LAB / "sample_data.csv", newline="")))
g = 9.80665
out = []


def num(s, i=0):
    return float(re.findall(r"-?\d[\d ]*\.?\d*", s.replace("−", "-"))[i].replace(" ", ""))


def cmp(name, mine, key, tol):
    rel = abs(mine - key) / max(abs(key), 1e-12)
    out.append((name, mine, key, rel, tol, rel <= tol))


def get(part, config):
    return [r for r in rows if r["part"] == part and r["config"] == config]


def col(rr, c):
    return np.array([float(r[c]) for r in rr])


def ss_c(x, a, L):
    """Downward deflection at x per unit downward load at a, times EI (Eq. 2 and its mirror image)."""
    b = L - a
    if x <= a:
        return b * x * (L * L - b * b - x * x) / (6 * L)
    xr = L - x
    return a * xr * (L * L - a * a - xr * xr) / (6 * L)


# ---------------- dimensions ----------------
b = np.mean(meas["bar"]["b_mm"]) * 1e-3
h = np.mean(meas["bar"]["h_mm"]) * 1e-3
I = b * h ** 3 / 12

# ---------------- pre-lab (nominal) ----------------
In = 25.4e-3 * 6.35e-3 ** 3 / 12
EIn = 205.2e9 * In
cmp("P1(a) deflection at 200 mm, 3.0 kg at 600 mm (mm)", 3 * g * ss_c(0.2, 0.6, 0.8) / EIn * 1e3, num(KV["P1_dA"], 0), 1e-3)
cmp("P1(a) deflection at 400 mm (mm)", 3 * g * ss_c(0.4, 0.6, 0.8) / EIn * 1e3, num(KV["P1_dA"], 1), 1e-3)
cmp("P1(a) largest stress (MPa)", 3 * g * 0.6 * 0.2 / 0.8 * 6.35e-3 / 2 / In / 1e6, num(KV["P1_sA"]), 2e-3)
cmp("P1(d) α for 0.62 kg on the nominal strip", 0.62 * g * 0.25 ** 2 / (203e9 * 12.7e-3 * 0.79e-3 ** 3 / 12), num(KV["P1_alpha"]), 2e-3)
cmp("P3(b) R_B/P with λ = 0.04", (5 / 16 + 1.5 * 0.04) / (1 + 3 * 0.04), num(KV["P3_r"]), 1e-3)
cmp("P3(c) ΔR_B for 0.5 mm, rigid clamp (N)", -3 * EIn * 0.5e-3 / 0.7 ** 3, num(KV["P3_dR"]), 2e-3)

# ---------------- A1: one global fit of all Part A single-load data ----------------
L = meas["A"]["span_mm"] * 1e-3
xg = [v * 1e-3 for v in meas["A"]["gage_x_mm"]]
loads = {"P600": meas["A"]["load_x_mm"][1] * 1e-3, "P200": meas["A"]["load_x_mm"][0] * 1e-3}
Xcols, yv, blocks = [], [], 0
series = []
for cfg, a in loads.items():
    rr = get("A", cfg)
    P = col(rr, "mass_kg") * g
    for j, c_ in enumerate(("d1_mm", "d2_mm", "d3_mm")):
        series.append((P, col(rr, c_) * 1e-3, ss_c(xg[j], a, L)))
n_s = len(series)
A_rows, y_all = [], []
for k, (P, d, fct) in enumerate(series):
    for Pi, di in zip(P, d):
        r = np.zeros(n_s + 1)
        r[k] = 1.0                       # one zero offset per series
        r[-1] = fct * Pi                 # common unknown: 1/EI
        A_rows.append(r)
        y_all.append(di)
sol, *_ = np.linalg.lstsq(np.array(A_rows), np.array(y_all), rcond=None)
E_glob = 1 / sol[-1] / I / 1e9
cmp("A1 E from one global fit of twelve series (GPa)", E_glob, num(KV["A_E"]), 2e-3)

# ---------------- A2 ----------------
comp = {}
for cfg in loads:
    rr = get("A", cfg)
    P = col(rr, "mass_kg") * g
    for j, c_ in enumerate(("d1_mm", "d2_mm", "d3_mm")):
        comp[(cfg, j)] = np.polyfit(P, col(rr, c_) * 1e-3, 1)[0]
rb = get("A", "both")
for j, c_ in enumerate(("d1_mm", "d2_mm", "d3_mm")):
    pred = comp[("P600", j)] * 2 * g + comp[("P200", j)] * 1 * g
    cmp(f"A2 superposed deflection at {int(xg[j] * 1e3)} mm (mm)", pred * 1e3, num(KV["A2_pred"], j), 1e-3)
    cmp(f"A2 measured deflection with both loads at {int(xg[j] * 1e3)} mm (mm)", (float(rb[-1][c_]) - float(rb[0][c_])), num(KV["A2_meas"], j), 1e-3)
cmp("A2 c13 (µm/N)", comp[("P600", 0)] * 1e6, num(KV["A2_c13"]), 1e-4)
cmp("A2 c31 (µm/N)", comp[("P200", 2)] * 1e6, num(KV["A2_c31"]), 1e-4)

# ---------------- A3: P4 combinations ----------------
LB = meas["B"]["L_mm"] * 1e-3
rr = get("B", "cantilever")
P = col(rr, "mass_kg") * g
c1 = np.polyfit(P, col(rr, "d1_mm") * 1e-3, 1)[0]
c2 = np.polyfit(P, col(rr, "d2_mm") * 1e-3, 1)[0]
EI_B = LB ** 3 / (8 * (c2 - 2 * c1))
k_B = 3 * LB ** 2 / (16 * c1 - 5 * c2)
cmp("A3 EI from 8[c(L) − 2c(L/2)]/L³ (N·m²)", EI_B, num(KV["B1_EI"]), 1e-3)
cmp("A3 k from 3L²/[16c(L/2) − 5c(L)] (N·m/rad)", k_B, num(KV["B1_k"]), 3e-3)
cmp("A3 EI from the tip alone, rigid clamp (N·m²)", LB ** 3 / (3 * c2), num(KV["B1_EIrigid"]), 1e-3)

# ---------------- A4: stiffness method on two beam elements with a rotational spring ----------------


def propped_R(EI, k, L_, a, Delta=0.0):
    """Upward prop force per unit load (and the settlement effect) by the direct stiffness method: nodes at 0, a, L."""
    def ke(le):
        return EI / le ** 3 * np.array([[12, 6 * le, -12, 6 * le], [6 * le, 4 * le ** 2, -6 * le, 2 * le ** 2],
                                         [-12, -6 * le, 12, -6 * le], [6 * le, 2 * le ** 2, -6 * le, 4 * le ** 2]])
    K = np.zeros((6, 6))
    K[0:4, 0:4] += ke(a)
    K[2:6, 2:6] += ke(L_ - a)
    K[1, 1] += k                                   # clamp spring on the rotation at x = 0 (y up, theta ccw)
    F = np.zeros(6)
    F[2] = -1.0                                    # unit load down at x = a
    free = [1, 2, 3, 5]                            # y(0) = 0, y(L) = -Delta prescribed
    u = np.zeros(6)
    u[4] = -Delta
    rhs = F[free] - K[np.ix_(free, [4])] @ u[[4]]
    u[free] = np.linalg.solve(K[np.ix_(free, free)], rhs)
    return (K @ u - F)[4]                          # reaction at the prop, upward +


rr = get("B", "propped")
Pp = col(rr, "mass_kg") * g
r_meas = np.polyfit(Pp, col(rr, "R_N"), 1)[0]
cmp("A4 R_B/P from the load cell (slope)", r_meas, num(KV["B2_r"]), 1e-3)
cmp("A4 R_B/P, stiffness method with the A3 clamp", propped_R(EI_B, k_B, LB, LB / 2), num(KV["B2_rk"]), 1e-3)
cmp("A4 R_B/P, stiffness method with a rigid clamp (5/16)", propped_R(EI_B, 1e15, LB, LB / 2), 0.3125, 1e-9)
Delta = meas["B"]["settle_mm"] * 1e-3
dR_k = propped_R(EI_B, k_B, LB, LB / 2, Delta) - propped_R(EI_B, k_B, LB, LB / 2, 0.0)
rs = get("B", "settlement")
cmp("A4 ΔR_B measured (N)", float(rs[1]["R_N"]) - float(rs[0]["R_N"]), num(KV["B3_dR"]), 1e-3)
cmp("A4 ΔR_B for 0.5 mm, stiffness method with the clamp (N)", dR_k, num(KV["B3_k"]), 3e-3)

# ---------------- A5, C2: elastica by shooting with solve_ivp ----------------
Cm = meas["C"]
bs = np.mean(Cm["b_mm"]) * 1e-3
ts = np.mean(Cm["t_mm"]) * 1e-3
Is = bs * ts ** 3 / 12
ws = Cm["rho_kg_m3"] * g * bs * ts
rc = get("C", "elastica")
Pc = col(rc, "mass_kg") * g
xt_m = col(rc, "x_tip_mm") * 1e-3
dv_m = -col(rc, "y_tip_mm") * 1e-3
Lc = xt_m[0] / 0.99983
sl = np.polyfit(Pc[:4], dv_m[:4], 1)[0]
cmp("A5(a) EI from the first four points (N·m²)", Lc ** 3 / (3 * sl), num(KV["C_EIlin"]), 2e-3)


def shoot(alpha, beta):
    """theta'' = -(alpha + beta (1 - s)) cos theta; theta(0) = 0, theta'(1) = 0. Returns dv/L, x_tip/L."""
    def end(k0):
        s_ = integrate.solve_ivp(lambda s, Y: [Y[1], -(alpha + beta * (1 - s)) * math.cos(Y[0]), math.cos(Y[0]), -math.sin(Y[0])],
                                 (0, 1), [0, k0, 0, 0], rtol=1e-11, atol=1e-13)
        return s_.y[:, -1]
    if alpha + beta == 0:
        return 0.0, 1.0
    k0 = optimize.brentq(lambda k0_: end(k0_)[1], 0.0, alpha + beta / 2 + 1e-9, xtol=1e-13)
    Y = end(k0)
    return -Y[3], Y[2]


def resid(EI):
    beta = ws * Lc ** 3 / EI
    r = []
    for P_, d_, x_ in zip(Pc, dv_m, xt_m):
        dv, xt = shoot(P_ * Lc ** 2 / EI, beta)
        r += [dv * Lc - d_, xt * Lc - x_]
    return np.array(r)


EI_fit = optimize.minimize_scalar(lambda e: float(resid(e) @ resid(e)), bounds=(0.09, 0.12), method="bounded",
                                  options=dict(xatol=1e-8)).x
cmp("C2 EI from the whole curve with self-weight, solve_ivp shooting (N·m²)", EI_fit, num(KV["C_EIfit"]), 2e-3)
cmp("C2 E of the strip (GPa)", EI_fit / Is / 1e9, num(KV["C_Efit"]), 2e-3)
a5 = optimize.brentq(lambda a: (a / 3) / shoot(a, 0.0)[0] - 1.05, 0.2, 2.0, xtol=1e-12)
cmp("A5 α where Eq. 10 is 5 % high, shooting + brentq", a5, num(KV["C_a5"]), 1e-3)
al = Pc[-1] * Lc ** 2 / EI_fit
cmp("M1(a) factor by which Eq. 10 overstates δ_v at 0.62 kg (measured δ_v)", (al / 3 * Lc + shoot(0, ws * Lc ** 3 / EI_fit)[0] * Lc) / dv_m[-1], num(KV["C_factor"]), 3e-3)

# ---------------- C3 ----------------
flex = LB ** 3 / (3 * EI_B) + LB ** 2 / k_B
cmp("C3 prop error that changes R_B at 4.0 kg by 5 % (mm)", 0.05 * r_meas * Pp.max() * flex * 1e3, num(KV["C3_D"]), 3e-3)

# ---------------- D1: integrate M/EI numerically for every candidate ----------------
cat = [("I 76 × 51", 76.2, 50.8, 5.6, 4.3), ("I 102 × 64", 101.6, 63.5, 6.4, 4.8), ("I 102 × 76", 101.6, 76.2, 6.35, 4.8),
       ("I 127 × 76", 127.0, 76.2, 7.1, 5.1), ("I 152 × 102", 152.4, 101.6, 7.9, 5.8), ("I 178 × 102", 177.8, 101.6, 8.4, 6.1),
       ("I 203 × 127", 203.2, 127.0, 9.5, 6.4)]
E_al = meas["reference"]["E_al_GPa"] * 1e9
sa = 0.6 * meas["reference"]["sY_al_MPa"] * 1e6
Lt, w, Pt = 4.0, 2000.0, 1500.0


def check(H, B, tf, tw, Ls):
    hw = H - 2 * tf
    I_ = (B * H ** 3 - (B - tw) * hw ** 3) / 12 * 1e-12
    x = np.linspace(0, Lt, 16001)
    RB = (w * Lt ** 2 / 2 + Pt * Lt) / Ls
    RA = w * Lt + Pt - RB
    M = RA * x - w * x ** 2 / 2 + RB * np.maximum(x - Ls, 0)
    t = integrate.cumulative_trapezoid(M / (E_al * I_), x, initial=0)
    y = integrate.cumulative_trapezoid(t, x, initial=0)
    y = y - np.interp(Ls, x, y) / Ls * x
    span = x <= Ls + 1e-12
    s = np.max(np.abs(M)) * H / 2e3 / I_
    ys, yt = np.max(np.abs(y[span])), abs(y[-1])
    ok = s <= sa and ys <= Ls / 360 and yt <= 2 * (Lt - Ls) / 360
    return ok, s, ys, yt


found = None
for name, H, B, tf, tw in sorted(cat, key=lambda c: (2 * c[2] * c[3] + (c[1] - 2 * c[3]) * c[4])):
    feas = [Ls for Ls in np.round(np.arange(2.5, Lt + 1e-9, 0.05), 2) if check(H, B, tf, tw, Ls)[0]]
    if feas:
        found = (name, feas, check(H, B, tf, tw, float(num(KV["D_best_Ls"]))))
        break
out.append(("D1 lightest feasible section (name match)", 1.0 if found[0] == KV["D_best"] else 0.0, 1.0, 0.0 if found[0] == KV["D_best"] else 1.0, 0, found[0] == KV["D_best"]))
cmp("D1 first feasible roller position (m)", found[1][0], num(KV["D_best_Ls"]), 1e-9)
cmp("D1 last feasible roller position (m)", found[1][-1], num(KV["D_best_hi"]), 1e-9)
cmp("D1 largest stress at the reference design (MPa)", found[2][1] / 1e6, num(KV["D_s"]), 2e-3)
cmp("D1 largest span deflection (mm)", found[2][2] * 1e3, abs(num(KV["D_ys"])), 2e-3)
cmp("D1 tip deflection (mm)", found[2][3] * 1e3, abs(num(KV["D_yt"])), 3e-3)

lines = ["## Lab 7 — handout questions re-solved from scratch vs. the instructor key", "",
         "| Question / quantity | From scratch | Key | Rel. difference | Tolerance | Result |", "|---|---:|---:|---:|---:|---|"]
for name, a_, b_, rel, tol, okk in out:
    lines.append(f"| {name} | {a_:.6g} | {b_:.6g} | {rel:.1e} | {tol:.0e} | {'PASS' if okk else '**FAIL**'} |")
nf = sum(not o[-1] for o in out)
lines += ["", f"{len(out) - nf} of {len(out)} agree.",
          "Tolerances: about 1e-3 where the key prints a rounded value of the same quantity; 2e-3 to 3e-3 where a different "
          "estimator is used on purpose (one global fit instead of six slopes, unweighted shooting fit instead of the "
          "uncertainty-weighted collocation fit, trapezoidal integration instead of closed forms)."]
(Path(__file__).parent / "results_from_scratch.md").write_text("\n".join(lines) + "\n")
print("\n".join(lines))
sys.exit(1 if nf else 0)

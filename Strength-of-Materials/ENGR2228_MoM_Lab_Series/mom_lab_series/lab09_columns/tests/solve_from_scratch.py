"""Re-solve the handout's questions from scratch and compare with the instructor key.

    python3 tests/solve_from_scratch.py      (from lab09_columns/)

Independent of src/lab09_analysis.py and src/lab09_model.py: plain csv + numpy/scipy, the handout's equations typed in
again, and deliberately different methods where one exists:
  * Southwell lines from explicit normal equations, cross-checked by a nonlinear fit of delta = delta0 P/(P_cr - P)
    straight to the dial readings (a different estimator, so a looser tolerance);
  * spring-end and fixed-pinned critical loads from the zero of the 4 x 4 boundary-condition determinant of the general
    solution y = A sin px + B cos px + Cx + D (instead of Eqs. 3 and 4), and the clamp stiffness by root-finding on it;
  * sensitivities (C2) by central differences instead of the closed-form derivative;
  * the elastica (M1) from scipy.special.ellipk; the tangent- and reduced-modulus loads by brentq on the stress;
  * the secant first-yield loads by brentq on Eq. 8, and the D1 catalog searched again from the handout's numbers.
Each value is compared with the string printed in the key (src/key_values.json); the tolerance is half a unit in the
last printed digit (or the stated rounding) plus a small relative allowance.
"""
import csv
import json
import math
import re
import sys
from pathlib import Path

import numpy as np
from scipy import optimize, special

LAB = Path(__file__).resolve().parents[1]
KV = json.loads((LAB / "src" / "key_values.json").read_text())
H = (LAB / "src" / "lab09_handout.md").read_text(encoding="utf-8")
meas = json.loads((LAB / "src" / "specimen_measurements.json").read_text())
rows = list(csv.DictReader(open(LAB / "sample_data.csv", newline="")))
for r in rows:
    for k in ("L_mm", "e_mm", "load_N", "defl_mm"):
        r[k] = float(r[k])
    for k in ("eps_front_ue", "eps_back_ue"):
        r[k] = float(r[k]) if r[k] != "" else None
ref = meas["reference"]
E2, sY, mRO = ref["E_al_GPa"] * 1e9, ref["sY_al_MPa"] * 1e6, ref["m_RO"]
R3 = math.sqrt(3)
PI = math.pi
out = []


def parse(s, i=0):
    """i-th number in a key string and its number of decimals ('1 829 ± 11' -> 1829, 0)."""
    toks = re.findall(r"-?\d+(?: \d{3})*(?:\.\d+)?", s.replace("−", "-"))
    t = toks[i]
    dec = len(t.split(".")[1]) if "." in t else 0
    return float(t.replace(" ", "")), dec


def cmp(name, mine, key, i=0, rel=2e-4, absdig=None):
    """Compare with the key's printed value: |mine - key| <= half a unit of the last digit (or absdig) + rel*|key|."""
    kv, dec = parse(KV[key], i)
    tol = (absdig if absdig is not None else 0.5 * 10 ** -dec) * (1 + 1e-9) + rel * abs(kv)
    out.append((name, mine, kv, abs(mine - kv), tol, abs(mine - kv) <= tol))


def cmpx(name, mine, ref_, reltol):
    """Different estimator or Monte Carlo: relative agreement within reltol."""
    d = abs(mine - ref_) / abs(ref_)
    out.append((name, mine, ref_, d, reltol, d <= reltol))


def cmps(name, cond, mine="", key=""):
    out.append((name, mine, key, 0.0 if cond else 1.0, 0.0, bool(cond)))


def get(part, config, L=None, e=None):
    return [r for r in rows if r["part"] == part and r["config"] == config and (L is None or r["L_mm"] == L) and (e is None or r["e_mm"] == e)]


def southwell(d, P):
    """delta/P = delta/P_cr + delta0/P_cr by explicit normal equations; returns P_cr, delta0, u(P_cr) from the fit."""
    x, y = np.asarray(d, float), np.asarray(d, float) / np.asarray(P, float)
    n = len(x)
    Sx, Sy, Sxx, Sxy = x.sum(), y.sum(), (x * x).sum(), (x * y).sum()
    den = n * Sxx - Sx ** 2
    a1 = (n * Sxy - Sx * Sy) / den
    a0 = (Sy - a1 * Sx) / n
    s2 = ((y - a0 - a1 * x) ** 2).sum() / (n - 2)
    ua1 = math.sqrt(s2 * n / den)
    return 1 / a1, a0 / a1, ua1 / a1 ** 2


def nonlinear_pcr(d, P, P0):
    f = lambda p, d0, Pc: d0 * p / (Pc - p)  # noqa: E731
    popt, _ = optimize.curve_fit(f, P, d, p0=[1e-4, P0])
    return popt[1]


def bc_det(P, EI, L, k_top, k_bot):
    """Determinant of the boundary conditions for y = A sin px + B cos px + C x + D, x from the top end A.
    Ends cannot translate (y = 0); EI y'' = k y' at the top (x = 0) and EI y'' = -k y' at the bottom (x = L) for
    rotational springs that resist the end rotation (k = inf: y' = 0; k = 0: y'' = 0). Scaled rows."""
    p = math.sqrt(P / EI)
    def row_end(x, k, sgn):
        y = [math.sin(p * x), math.cos(p * x), x, 1.0]
        yp = [p * math.cos(p * x), -p * math.sin(p * x), 1.0, 0.0]
        ypp = [-p * p * math.sin(p * x), -p * p * math.cos(p * x), 0.0, 0.0]
        if k == math.inf:
            r2 = yp
        else:
            r2 = [EI * a - sgn * k * b for a, b in zip(ypp, yp)]
            r2 = [v / (EI * p * p + k * p) for v in r2]
        return y, r2
    y0, r0 = row_end(0.0, k_top, +1)
    yL, rL = row_end(L, k_bot, -1)
    return np.linalg.det(np.array([y0, [v * L for v in r0], yL, [v * L for v in rL]]))


def first_root(fun, Pmax, n=4000):
    """Smallest positive zero of fun(P) on (0, Pmax], found by scanning for a sign change, then brentq."""
    Ps = np.linspace(Pmax / n, Pmax, n)
    vals = [fun(P) for P in Ps]
    for i in range(1, n):
        if np.sign(vals[i]) != np.sign(vals[i - 1]):
            return optimize.brentq(fun, Ps[i - 1], Ps[i], xtol=1e-12, rtol=1e-14)
    raise ValueError("no root")


def euler(E, I, Le):
    return PI ** 2 * E * I / Le ** 2


def secant_ymax(e, P, Pcr):
    return e * (1 / math.cos(PI / 2 * math.sqrt(P / Pcr)) - 1)


def secant_smax(P, A, e, c, r, Pcr):
    return P / A * (1 + e * c / r ** 2 / math.cos(PI / 2 * math.sqrt(P / Pcr)))


def first_yield(sYv, A, e, c, r, Pcr):
    return optimize.brentq(lambda P: secant_smax(P, A, e, c, r, Pcr) - sYv, 1e-6 * Pcr, Pcr * (1 - 1e-12), xtol=1e-9)


def aa_6061(sl):     # Beer Eqs. 10.43b, 10.44b, 10.45b (MPa)
    if sl <= 17.8:
        return 146.3
    if sl < 66.0:
        return 173.9 - 1.602 * sl + 0.00323 * sl ** 2
    return 356e3 / sl ** 2


def inv_Et(s, E, sYv, m):    # Lab 1 Ramberg–Osgood: eps = s/E + 0.002 (s/sY)^m
    return 1 / E + 0.002 * m * (s / sYv) ** (m - 1) / sYv


def tangent_stress(sl, E, sYv, m, reduced=False):
    def Emod(s):
        Et = 1 / inv_Et(s, E, sYv, m)
        return 4 * E * Et / (math.sqrt(E) + math.sqrt(Et)) ** 2 if reduced else Et
    return optimize.brentq(lambda s: s - PI ** 2 * Emod(s) / sl ** 2, 1e3, 3 * sYv, xtol=1e-6)


# ------------------------------------------------------------------ pre-lab, nominal section and Table 1
bN, tN = 25.4e-3, 6.35e-3
AN, IN = bN * tN, bN * tN ** 3 / 12
rN, cN = math.sqrt(IN / AN), tN / 2
cmp("P: nominal area (mm²)", AN * 1e6, "P_A")
cmp("P: nominal I (mm⁴)", IN * 1e12, "P_I")
cmp("P: nominal r (mm)", rN * 1e3, "P_r")
cmp("P: nominal EI (N·m²)", E2 * IN, "P_EI")
for L in (300, 450, 600):
    P_ = euler(E2, IN, L / 1e3)
    cmp(f"P1(a) L/r, {L} mm", L / 1e3 / rN, f"P1_sl{L}")
    cmp(f"P1(a) P_cr, {L} mm (N)", P_, f"P1_P{L}")
    cmp(f"P1(a) σ_cr, {L} mm (MPa)", P_ / AN / 1e6, f"P1_s{L}")
# (b) fixed-fixed 600 and fixed-pinned 640 from the boundary-condition determinant (not Beer's K)
EIN = E2 * IN
Pff = first_root(lambda P: bc_det(P, EIN, 0.600, math.inf, math.inf), 5 * euler(E2, IN, 0.6))
Pfp = first_root(lambda P: bc_det(P, EIN, 0.640, 0.0, math.inf), 3 * euler(E2, IN, 0.64))
cmp("P1(b) fixed–fixed 600 mm (N), determinant", Pff, "P1_ff")
cmp("P1(b) fixed–pinned 640 mm (N), determinant", Pfp, "P1_fp", rel=5e-4)
P90 = euler(E2, IN, 0.090)
cmp("P1(c) L/r, 90 mm", 0.090 / rN, "P1_sl90")
cmp("P1(c) Euler P_cr, 90 mm (kN)", P90 / 1e3, "P1_90")
cmp("P1(c) Euler σ_cr, 90 mm (MPa)", P90 / AN / 1e6, "P1_s90")
cmp("P1(c) σ_Y A (kN)", sY * AN / 1e3, "P1_sYA")
cmp("P1(c) L/r below which Euler exceeds σ_Y", PI * math.sqrt(E2 / sY), "P1_slY")
for a, key in ((0.5, "P1_d50"), (0.75, "P1_d75"), (0.9, "P1_d90")):
    cmp(f"P1(d) dial at {a} P_cr (mm)", 0.5 * a / (1 - a), key)
# P3: readings typed in the handout
m3 = re.search(r"readings: (.*?)\. Plot", H).group(1)
pts = [(float(a), float(b)) for a, b in re.findall(r"(\d+) N, (\d+\.\d+) mm", m3)]
cmps("P3: four readings parsed from the handout", len(pts) == 4, str(pts))
P3c, d3c, _ = southwell([d * 1e-3 for _, d in pts], [P for P, _ in pts])
for i, (P, d) in enumerate(pts):
    cmp(f"P3: δ/P at {P:.0f} N (mm/kN)", d / P * 1e3, "P3_y", i=i)
cmp("P3: P_cr (N)", P3c, "P3_P")
cmp("P3: δ0 (mm)", d3c * 1e3, "P3_d0")
cmp("P3: slope (10⁻⁶ N⁻¹)", 1e6 / P3c, "P3_slope")
cmp("P3: intercept (10⁻⁶ m/N)", d3c / P3c * 1e6, "P3_icpt")
# P4: 450 mm, e = 2 mm, P = 0.5 P_cr (P1 value)
P4c = euler(E2, IN, 0.45)
P4 = round(P4c) / 2
y4 = secant_ymax(2e-3, P4, P4c)
cmp("P4: load (N)", P4, "P4_P", absdig=0.5)
cmp("P4: y_max (mm)", y4 * 1e3, "P4_y")
cmp("P4: moment at mid-length (N·m)", P4 * (2e-3 + y4), "P4_M")
cmp("P4: σ_max (MPa)", (P4 / AN + P4 * (2e-3 + y4) * cN / IN) / 1e6, "P4_s")
cmp("P4: σ_max by Eq. 8 (MPa)", secant_smax(P4, AN, 2e-3, cN, rN, P4c) / 1e6, "P4_secant")
cmp("P4: axial part (MPa)", P4 / AN / 1e6, "P4_ax")
cmp("P4: bending part (MPa)", P4 * (2e-3 + y4) * cN / IN / 1e6, "P4_sb")
cmp("P4: bending without deflection (MPa)", P4 * 2e-3 * cN / IN / 1e6, "P4_sb0")
cmp("P4: σ_max without deflection (MPa)", (P4 / AN + P4 * 2e-3 * cN / IN) / 1e6, "P4_s0")
cmp("P4: amplification sec(π/(2√2))", 1 / math.cos(PI / (2 * math.sqrt(2))), "P4_fac")
# P6: 300 mm bar near P_cr, bow 0.3 mm, at δ = 5 mm
P6 = euler(E2, IN, 0.3)
s6 = P6 / AN + P6 * (0.3e-3 + 5e-3) * cN / IN
cmp("P6: stress at the L/60 limit (MPa)", s6 / 1e6, "P6_s")
cmp("P6: stress / σ_Y (%)", 100 * s6 / sY, "P6_pct")
# P5: the page's closed forms at its own inputs (b 25.42, t 6.35, E 68.9 GPa, σ_Y 273.7, m 17)
Es, bS, tS = 68.9e9, 25.42e-3, 6.35e-3
AS, IS = bS * tS, bS * tS ** 3 / 12
rS, cS = math.sqrt(IS / AS), tS / 2
cmp("P5: page, pinned 450 mm (N)", euler(Es, IS, 0.45), "sim_A450")
Pspr = first_root(lambda P: bc_det(P, Es * IS, 0.6005, 2800.0, 2800.0), 4.5 * euler(Es, IS, 0.6005))
cmp("P5: page, springs k = 2800 N·m/rad, 600.5 mm (N), determinant", Pspr, "sim_sprP")
cmp("P5: page, K for the springs", PI / 0.6005 * math.sqrt(Es * IS / Pspr), "sim_sprK")
cmp("P5: page, ideal fixed ends 600.5 mm (N)", euler(Es, IS, 0.6005 / 2), "sim_sprI")
eC2 = 2e-3 + 4 / PI * 0.46e-3                                         # the page adds the bow as an offset (4/pi) delta0
cmp("P5: page, Eq. 10.37 for e = 2 mm plus the 0.46 mm bow as (4/π)δ0 (N)", sY * AS / (1 + eC2 * cS / rS ** 2), "sim_C2lin")
PcrS = euler(Es, IS, 0.45)
PYb = optimize.brentq(lambda P: P / AS + P * cS / IS * (2e-3 / math.cos(PI / 2 * math.sqrt(P / PcrS)) + 0.46e-3 / (1 - P / PcrS)) - sY, 1.0, PcrS * (1 - 1e-12))
cmp("P5: page, first yield with e = 2 mm and the bow (secant + bow amplification, closed form) (N)", PYb, "sim_C2PY", rel=1e-3)
cmp("P5: page, Part D Euler (kN)", euler(Es, IS, 0.09) / 1e3, "sim_DE")
cmp("P5: page, Part D tangent-modulus load (kN)", tangent_stress(0.09 / rS, Es, sY, mRO) * AS / 1e3, "sim_Dt")
cmp("P5: page, Part D reduced-modulus load (kN)", tangent_stress(0.09 / rS, Es, sY, mRO, True) * AS / 1e3, "sim_Dr")

# ------------------------------------------------------------------ measured section
bm, tm = np.mean(meas["bar"]["b_mm"]) * 1e-3, np.mean(meas["bar"]["t_mm"]) * 1e-3
A, I = bm * tm, bm * tm ** 3 / 12
r, c = math.sqrt(I / A), tm / 2
EI = E2 * I
cmp("section: b (mm)", bm * 1e3, "b")
cmp("section: t (mm)", tm * 1e3, "t")
cmp("section: A (mm²)", A * 1e6, "A")
cmp("section: I (mm⁴)", I * 1e12, "I")
cmp("section: r (mm)", r * 1e3, "r")
cmp("section: EI (N·m²)", EI, "EI")
ur_lc = meas["loadcell_accuracy_pct"] / 100 / R3

# ------------------------------------------------------------------ A1
Ls = meas["lengths_mm"]
PS = {}
for key, Lname in (("300", "A300"), ("450", "A450"), ("600", "A600")):
    L = Ls[Lname] * 1e-3
    Pe = euler(E2, I, L)
    use = [x for x in get("A", "pinned", float(key)) if x["load_N"] >= 0.5 * Pe and x["defl_mm"] > 0]
    d = np.array([x["defl_mm"] * 1e-3 for x in use]); P = np.array([x["load_N"] for x in use])
    Pc, d0, uP = southwell(d, P)
    PS[key] = (Pc, d0, L)
    cmp(f"A1 {key} mm: readings used", len(use), f"A{key}_n", absdig=0)
    cmp(f"A1 {key} mm: first load used (N)", P.min(), f"A{key}_Pmin")
    cmp(f"A1 {key} mm: Euler P_cr (N)", Pe, f"A{key}_Pe")
    cmp(f"A1 {key} mm: Southwell P_cr (N)", Pc, f"A{key}_PS")
    cmp(f"A1 {key} mm: U(P_cr) = 2 hypot(fit, load cell) (N)", 2 * math.hypot(uP, Pc * ur_lc), f"A{key}_PS", i=1)
    cmp(f"A1 {key} mm: difference from Euler (%)", 100 * (Pc / Pe - 1), f"A{key}_d")
    cmp(f"A1 {key} mm: Southwell δ0 (mm)", d0 * 1e3, f"A{key}_d0")
    cmp(f"A1 {key} mm: E from P_cr (GPa)", Pc * L ** 2 / (PI ** 2 * I) / 1e9, f"A{key}_ES")
    cmp(f"A1 {key} mm: offset equivalent (π/4)(δ0 − bow) (mm)", PI / 4 * (d0 * 1e3 - meas["bow_mm"][Lname]), f"A{key}_eeq")
    cmp(f"A1 {key} mm: last load / P_cr", max(x["load_N"] for x in get("A", "pinned", float(key))) / Pc, f"A{key}_last")
    cmpx(f"A1 {key} mm: P_cr by a nonlinear fit of δ = δ0 P/(P_cr − P) (different estimator)", nonlinear_pcr(d, P, Pe), Pc, 3e-3)
lx = np.log([PS[k][2] for k in PS]); ly = np.log([PS[k][0] for k in PS])
cmp("A1: slope of log P_cr against log L", np.polyfit(lx, ly, 1)[0], "A_slope")
cmp("A1: mean E from the Southwell loads (GPa)", np.mean([PS[k][0] * PS[k][2] ** 2 / (PI ** 2 * I) for k in PS]) / 1e9, "ES")
# A6: E from the axial strain, readings below half of each prediction, all three bars
xs, ys = [], []
for key, Lname in (("300", "A300"), ("450", "A450"), ("600", "A600")):
    Pe = euler(E2, I, Ls[Lname] * 1e-3)
    for x in get("A", "pinned", float(key)):
        if x["load_N"] <= 0.5 * Pe:
            xs.append(x["load_N"]); ys.append(-(x["eps_front_ue"] + x["eps_back_ue"]) / 2 * 1e-6)
sl_g, ic_g = np.polyfit(xs, ys, 1)
cmp("A6: readings used for the axial-strain E", len(xs), "Eg_n", absdig=0)
cmp("A6: E from the axial strain (GPa)", 1 / (A * sl_g) / 1e9, "Eg")
cmp("A6: intercept of the axial-strain line (µε)", ic_g * 1e6, "Eg_icpt")
# C1: strain Southwell for the 450 mm bar
Pe450 = euler(E2, I, Ls["A450"] * 1e-3)
use = [x for x in get("A", "pinned", 450.0) if x["load_N"] >= 0.5 * Pe450]
Pcs, e0s, _ = southwell([(x["eps_front_ue"] - x["eps_back_ue"]) / 2 * 1e-6 for x in use], [x["load_N"] for x in use])
cmp("C1: P_cr from the bending strain (N)", Pcs, "C1_PS")
cmp("C1: equivalent bending strain of the bow (µε)", e0s * 1e6, "C1_eps0")

# ------------------------------------------------------------------ A2: clamps
Lff, Lfp = Ls["Bff"] * 1e-3, Ls["Bfp"] * 1e-3
B = {}
for nm, cfg, Le0, L in (("ff", "fixed-fixed", 0.5 * Lff, Lff), ("fp", "fixed-pinned", Lfp * PI / optimize.brentq(lambda z: math.tan(z) - z, 4.0, 4.6), Lfp)):
    Pe = euler(E2, I, Le0)
    use = [x for x in get("B", cfg) if x["load_N"] >= 0.5 * Pe and x["defl_mm"] > 0]
    Pc, d0, uP = southwell([x["defl_mm"] * 1e-3 for x in use], [x["load_N"] for x in use])
    B[nm] = Pc
    tag = "Bff" if nm == "ff" else "Bfp"
    cmp(f"A2 {cfg}: readings used", len(use), f"{tag}_n", absdig=0)
    cmp(f"A2 {cfg}: Euler with Beer's K (N)", Pe, f"{tag}_Pe")
    cmp(f"A2 {cfg}: Southwell P_cr (N)", Pc, f"{tag}_PS")
    cmp(f"A2 {cfg}: K = (π/L)√(EI/P_cr)", PI / L * math.sqrt(EI / Pc), f"{tag}_K")
    cmp(f"A2 {cfg}: difference from Beer's ideal (%)", 100 * (Pc / Pe - 1), f"{tag}_d")
    cmp(f"A2 {cfg}: Southwell δ0 (mm)", d0 * 1e3, f"{tag}_d0")
# clamp stiffness: the k for which the symmetric-spring determinant vanishes at the measured fixed-fixed load
kk = optimize.brentq(lambda k: first_root(lambda P: bc_det(P, EI, Lff, k, k), 4.5 * euler(E2, I, Lff)) - B["ff"], 500.0, 50000.0, xtol=1e-6)
cmp("A2: clamp stiffness k (N·m/rad), determinant root (key rounds to 10)", kk, "B_k", absdig=5)
cmp("A2: kL/EI", kk * Lff / EI, "B_kLEI")
Pfp_pred = first_root(lambda P: bc_det(P, EI, Lfp, 0.0, kk), 3 * euler(E2, I, Lfp))
cmp("A2: fixed–pinned prediction with this k (N), determinant", Pfp_pred, "B_pred")
cmp("A2: K of the prediction", PI / Lfp * math.sqrt(EI / Pfp_pred), "B_predK")
cmp("A2: measured vs predicted fixed–pinned (%)", 100 * (B["fp"] / Pfp_pred - 1), "B_pred_d")
kfp = optimize.brentq(lambda k: first_root(lambda P: bc_det(P, EI, Lfp, 0.0, k), 3 * euler(E2, I, Lfp)) - B["fp"], 500.0, 50000.0, xtol=1e-6)
cmp("C2: k from the fixed–pinned test instead (key rounds to 10)", kfp, "k_fp", absdig=5)
# C2: sensitivities by central differences
def k_of_ff(P):
    return optimize.brentq(lambda k: first_root(lambda Q: bc_det(Q, EI, Lff, k, k), 4.5 * euler(E2, I, Lff)) - P, 300.0, 1e6, xtol=1e-8)
def k_of_fp(P):
    return optimize.brentq(lambda k: first_root(lambda Q: bc_det(Q, EI, Lfp, 0.0, k), 3 * euler(E2, I, Lfp)) - P, 300.0, 1e6, xtol=1e-8)
h = 1e-4
for nm, fun, key, rel in (("fixed–fixed", k_of_ff, "C2_sens", 1e-3), ("fixed–pinned", k_of_fp, "C2_fp", 1e-3)):
    P0 = B["ff"] if nm == "fixed–fixed" else B["fp"]
    sens = (fun(P0 * (1 + h)) - fun(P0 * (1 - h))) / (2 * h * fun(P0))
    cmp(f"C2: (dk/k)/(dP/P), {nm}, central difference", sens, key, rel=rel)
cmp("C2: x = (L/2)√(P_cr/EI) at the fixed–fixed result", Lff / 2 * math.sqrt(B["ff"] / EI), "C2_x")
# Monte Carlo of k (different seed and draws): U(k) within 10 %
rng = np.random.default_rng(12345)
ks = []
uE = ref["u_E_al_GPa"] * 1e9
ub, ut = parse(KV["b"], 1)[0] / 2, parse(KV["t"], 1)[0] / 2          # the key prints U = 2u for b and t
urI = math.sqrt((ub / (bm * 1e3)) ** 2 + (3 * ut / (tm * 1e3)) ** 2)
use = [x for x in get("B", "fixed-fixed") if x["load_N"] >= 0.5 * euler(E2, I, 0.5 * Lff) and x["defl_mm"] > 0]
_, _, uPff = southwell([x["defl_mm"] * 1e-3 for x in use], [x["load_N"] for x in use])
xff0 = Lff / 2 * math.sqrt(B["ff"] / EI)
for _ in range(3000):
    EIi = (E2 + uE * rng.standard_normal()) * I * (1 + urI * rng.standard_normal())
    Pi = (B["ff"] + uPff * rng.standard_normal()) / (1 + ur_lc * R3 * rng.uniform(-1, 1))
    Li = Lff + meas["rule_accuracy_mm"] / R3 * 1e-3 * rng.standard_normal()
    x = Li / 2 * math.sqrt(Pi / EIi)
    if x < PI:
        ks.append(-2 * x * EIi / (Li * math.tan(x)))   # Eq. 3 inverted, for speed in the Monte Carlo only
cmpx("A2: U(k) by an independent Monte Carlo (3000 draws, other seed)", 2 * float(np.std(ks)), parse(KV["B_k"], 1)[0], 0.10)

# ------------------------------------------------------------------ A3, C3: eccentric
Pc450 = PS["450"][0]
rA = {x["load_N"]: x for x in get("A", "pinned", 450.0)}
for en in (1.0, 2.0):
    rc = get("C", "eccentric", 450.0, en)
    com = [(x, rA[x["load_N"]]) for x in rc if x["load_N"] in rA and x["load_N"] > 0]
    P = np.array([a["load_N"] for a, _ in com])
    dd = np.array([(a["defl_mm"] - b_["defl_mm"]) * 1e-3 for a, b_ in com])
    sec = np.array([1 / math.cos(PI / 2 * math.sqrt(p / Pc450)) - 1 for p in P])
    e_fit = optimize.least_squares(lambda ee: ee[0] * sec - dd, [1e-3]).x[0]
    tag = f"C{int(en)}"
    cmp(f"A3 e = {en:.0f} mm: fitted eccentricity (mm)", e_fit * 1e3, f"{tag}_e")
    dbend = np.array([((a["eps_front_ue"] - a["eps_back_ue"]) - (b_["eps_front_ue"] - b_["eps_back_ue"])) / 2 * 1e-6 for a, b_ in com])
    arm = dbend * EI / (P * c)
    msk = P >= 400
    cmp(f"A3 e = {en:.0f} mm: lever arm from the gages minus the deflection change (mm)", float(np.mean((arm - dd)[msk])) * 1e3, f"{tag}_es")
    i6, i12 = list(P).index(600.0), list(P).index(1200.0)
    cmp(f"A3 e = {en:.0f} mm: deflection ratio 1200 N / 600 N", dd[i12] / dd[i6], f"{tag}_ratio")
    if en == 1.0:
        cmp("A3: theory ratio 1200 N / 600 N", sec[i12] / sec[i6], "C_ratio_th")
    # C3: Southwell on the raw readings; the raw-fit mistake
    use = [x for x in rc if x["load_N"] >= 0.5 * Pe450 and x["defl_mm"] > 0]
    Pr_, d0r, _ = southwell([x["defl_mm"] * 1e-3 for x in use], [x["load_N"] for x in use])
    cmp(f"C3 e = {en:.0f} mm: Southwell P_cr on the raw readings (N)", Pr_, f"{tag}_swP")
    cmp(f"C3 e = {en:.0f} mm: Southwell δ0 on the raw readings (mm)", d0r * 1e3, f"{tag}_swd0")
    cmp(f"C3 e = {en:.0f} mm: (π/4)(δ0 − Part A's δ0) (mm)", PI / 4 * (d0r - PS["450"][1]) * 1e3, f"{tag}_swe")
    Pr = np.array([x["load_N"] for x in rc if x["load_N"] > 0]); dr = np.array([x["defl_mm"] * 1e-3 for x in rc if x["load_N"] > 0])
    ok = Pr < 0.99 * Pc450
    fr = np.array([1 / math.cos(PI / 2 * math.sqrt(p / Pc450)) - 1 for p in Pr[ok]])
    cmp(f"mistake 4, e = {en:.0f} mm: Eq. 7 fitted to the raw readings (mm)", float(np.linalg.lstsq(fr[:, None], dr[ok], rcond=None)[0][0]) * 1e3, f"{tag}_raw")
# A4: first-yield loads with the measured P_cr
for en, tag in ((1.0, "1"), (2.0, "2")):
    PY = first_yield(sY, A, en * 1e-3, c, r, Pc450)
    PYl = sY * A / (1 + en * 1e-3 * c / r ** 2)
    cmp(f"A4 e = {en:.0f} mm: first-yield load, Eq. 8 (N)", PY, f"PY{tag}")
    cmp(f"A4 e = {en:.0f} mm: Eq. 10.37 (kN)", PYl / 1e3, f"PYl{tag}")
    cmp(f"A4 e = {en:.0f} mm: first-yield load / P_cr", PY / Pc450, f"PYr{tag}")
    if tag == "2":
        cmp("A4/M1(d): Eq. 10.37 overestimate, e = 2 mm (factor)", PYl / PY, "PYo2")
        cmp("A4: y_max at first yield, e = 2 mm (mm)", secant_ymax(2e-3, PY, Pc450) * 1e3, "PYy2")
rc2 = {x["load_N"]: x for x in get("C", "eccentric", 450.0, 2.0)}
Pl = max(p for p in rc2 if p in rA and p > 0)
cmp("A4: largest common load (N)", Pl, "st_P")
cmp("A4: measured back-face stress −Eε_B (MPa)", -rc2[Pl]["eps_back_ue"] * 1e-6 * E2 / 1e6, "st_meas")
s1035 = secant_smax(Pl, A, 2e-3, c, r, Pc450)
sA = -rA[Pl]["eps_back_ue"] * 1e-6 * E2
cmp("A4: Eq. 8 with the groove offset alone (MPa)", s1035 / 1e6, "st_1035")
cmp("A4: Part A stress at the same load (MPa)", sA / 1e6, "st_A")
cmp("A4: axial stress P/A (MPa)", Pl / A / 1e6, "st_ax")
cmp("A4: Eq. 8 + Part A − P/A (MPa)", (s1035 + sA - Pl / A) / 1e6, "st_sum")

# ------------------------------------------------------------------ A5: short column
rd = get("D", "short")
Pm = max(x["load_N"] for x in rd)
sl = Ls["D"] * 1e-3 / r
st = tangent_stress(sl, E2, sY, mRO)
sr = tangent_stress(sl, E2, sY, mRO, reduced=True)
PE = euler(E2, I, Ls["D"] * 1e-3)
cmp("A5: maximum load (kN)", Pm / 1e3, "D_P")
cmp("A5: maximum stress (MPa)", Pm / A / 1e6, "D_s")
cmp("A5: L/r", sl, "D_sl")
cmp("A5: Euler load (kN)", PE / 1e3, "D_PE")
cmp("A5: Euler stress (MPa)", PE / A / 1e6, "D_sE")
cmp("A5: σ_Y A (kN)", sY * A / 1e3, "D_PY")
cmp("A5: tangent-modulus stress (MPa)", st / 1e6, "D_st")
cmp("A5: tangent-modulus load (kN)", st * A / 1e3, "D_Pt")
cmp("A5: E_t at that stress (GPa)", 1 / inv_Et(st, E2, sY, mRO) / 1e9, "D_Et")
cmp("A5: reduced-modulus stress (MPa)", sr / 1e6, "D_sr")
cmp("A5: reduced-modulus load (kN)", sr * A / 1e3, "D_Pr")
cmp("A5: AA allowable stress, Eq. 10.44b (MPa)", aa_6061(sl), "D_aa")
cmp("A5: AA allowable load (kN)", aa_6061(sl) * 1e6 * A / 1e3, "D_Paa")
cmp("A5: 1.95 × AA allowable stress (MPa)", 1.95 * aa_6061(sl), "D_aa195")
cmp("A5: 1.95 × AA allowable load (kN)", 1.95 * aa_6061(sl) * 1e6 * A / 1e3, "D_Paa195")
cmp("A5: 1.95 × AA vs maximum (%)", 100 * (1.95 * aa_6061(sl) * 1e6 * A / Pm - 1), "D_aa_d")
cmp("M1(a): Euler overestimate (%)", 100 * (PE / Pm - 1), "D_Eo")
cmp("A5: σ_Y A overestimate (%)", 100 * (sY * A / Pm - 1), "D_Yo")
cmp("A5: tangent-modulus overestimate (%)", 100 * (st * A / Pm - 1), "D_to")
cmp("A5: deflection at the maximum (mm)", [x["defl_mm"] for x in rd if x["load_N"] == Pm][0], "D_dmax")

# ------------------------------------------------------------------ M1
def elastica_k(dL):
    return optimize.brentq(lambda k: k / special.ellipk(k * k) - dL, 1e-9, 0.9999)
for dL, key, nm in ((1 / 60, "M1_L60", "L/60"), (0.1, "M1_L10", "L/10")):
    k_ = elastica_k(dL)
    cmp(f"M1(c): elastica P/P_cr − 1 at δ = {nm} (%)", ((2 * special.ellipk(k_ * k_) / PI) ** 2 - 1) * 100, key, rel=1e-3)
cmp("M1(c): first-yield deflection of the perfect 450 mm bar (mm)", (sY - Pc450 / A) * I / (Pc450 * c) * 1e3, "M1_yd")
g1 = optimize.brentq(lambda g: PI / math.sqrt(first_root(lambda P: bc_det(P, 1.0, 1.0, g, g), 4.5 * PI ** 2)) - 0.505, 10.0, 1e5, xtol=1e-6)
cmp("M1(b): kL/EI for K within 1 % of 0.5 (determinant)", g1, "M1_k1")

# ------------------------------------------------------------------ D1: the catalog searched again
spec_ok = all(s in H for s in ("2.0 m long", "service load of 12 kN", "up to 2 mm off", "1.95 times the service load", "$D_o/t$ at most 40", "at most 76.2 mm"))
cmps("D1: requirements read from the handout (2.0 m, 12 kN, 2 mm, 1.95, D/t 40, 76.2 mm)", spec_ok)
cat_D = [float(x) for x in re.search(r"Outside diameter \$D_o\$ \(mm\) \| ([\d., ]+) \|", H).group(1).split(",")]
cat_t = [float(x) for x in re.search(r"Wall thickness \$t\$ \(mm\) \| ([\d., ]+) \|", H).group(1).split(",")]
cmps("D1: Table 6 parsed (5 diameters × 4 walls)", len(cat_D) == 5 and len(cat_t) == 4, f"{cat_D} × {cat_t}")


def tube(Do, tw):
    ro, ri = Do / 2e3, Do / 2e3 - tw / 1e3
    A_, I_ = PI * (ro ** 2 - ri ** 2), PI * (ro ** 4 - ri ** 4) / 4
    return A_, I_, math.sqrt(I_ / A_), ro


def check(Do, tw, K):
    A_, I_, r_, c_ = tube(Do, tw)
    Le = K * 2.0
    Pall = aa_6061(Le / r_) * 1e6 * A_
    PY_ = first_yield(sY, A_, 2e-3, c_, r_, euler(E2, I_, Le))
    return dict(ok=Pall >= 12e3 and PY_ >= 1.95 * 12e3 and Do / tw <= 40 and Do <= 76.2, Pall=Pall, PY=PY_, mass=2700 * A_, A=A_, I=I_, r=r_, c=c_, Le=Le)


for K, key in ((1.0, "D1_best"), (0.52, "D1_trap")):
    ok = sorted([(check(D, w, K)["mass"], D, w) for D in cat_D for w in cat_t if check(D, w, K)["ok"]])
    want = KV[key].replace(" ", "")
    got = f"{ok[0][1]:.2f}×{ok[0][2]:.2f}"
    cmps(f"D1: lightest tube with K = {K}", got == want, got, KV[key])
best = check(63.5, 1.65, 1.0)
Pcr_b = euler(E2, best["I"], 2.0)
cmp("D1 reference: mass (kg/m)", best["mass"], "D1_m")
cmp("D1 reference: A (mm²)", best["A"] * 1e6, "D1_A")
cmp("D1 reference: I (10³ mm⁴)", best["I"] * 1e9, "D1_I")
cmp("D1 reference: r (mm)", best["r"] * 1e3, "D1_r")
cmp("D1 reference: L/r", 2.0 / best["r"], "D1_sl")
cmp("D1 reference: σ_all (MPa)", aa_6061(2.0 / best["r"]), "D1_sall")
cmp("D1 reference: allowable load (kN)", best["Pall"] / 1e3, "D1_Pall")
cmp("D1 reference: P_cr (kN)", Pcr_b / 1e3, "D1_Pcr")
cmp("D1 reference: first-yield load, e = 2 mm (kN)", best["PY"] / 1e3, "D1_PY")
cmp("D1 reference: y_max at the service load (mm)", secant_ymax(2e-3, 12e3, Pcr_b) * 1e3, "D1_ymax")
cmp("D1 reference: σ_max at the service load (MPa)", secant_smax(12e3, best["A"], 2e-3, best["c"], best["r"], Pcr_b) / 1e6, "D1_smax")
cmp("D1 reference: F.S. wrongly applied to the stress (kN)", first_yield(sY / 1.95, best["A"], 2e-3, best["c"], best["r"], Pcr_b) / 1e3, "D1_PstFS")
cmp("D1 reference: first-yield load / F.S. (kN)", best["PY"] / 1.95e3, "D1_PYFS")
trap, trap_pin = check(44.45, 1.65, 0.52), check(44.45, 1.65, 1.0)
cmp("D1 trap: mass (kg/m)", trap["mass"], "D1_tm")
cmp("D1 trap: L_e/r with K = 0.52", 1.04 / trap["r"], "D1_tsl")
cmp("D1 trap: allowable load with K = 0.52 (kN)", trap["Pall"] / 1e3, "D1_tPall")
cmp("D1 trap: first-yield load with K = 0.52 (kN)", trap["PY"] / 1e3, "D1_tPY")
cmp("D1 trap: L/r if the gussets act as pins", 2.0 / trap_pin["r"], "D1_tpsl")
cmp("D1 trap: allowable load pinned (kN)", trap_pin["Pall"] / 1e3, "D1_tpPall")
cmp("D1 trap: Euler load pinned (kN)", euler(E2, trap_pin["I"], 2.0) / 1e3, "D1_tpPcr")
cmp("D1 trap: first-yield load pinned (kN)", trap_pin["PY"] / 1e3, "D1_tpPY")
cmp("D1 trap: mass saving (%)", 100 * (1 - trap["mass"] / best["mass"]), "D1_save")

# ------------------------------------------------------------------ report
esc = lambda s: str(s).replace("|", "\\|")  # noqa: E731
fmt = lambda v: f"{v:.6g}" if isinstance(v, (int, float, np.floating)) and not isinstance(v, bool) else esc(v)  # noqa: E731
lines = ["## Lab 9 — handout questions re-solved from scratch vs. the instructor key", "",
         "| Question / quantity | From scratch | Key | Abs. or rel. difference | Tolerance | Result |", "|---|---:|---:|---:|---:|---|"]
for name, a_, b_, dif, tol, okk in out:
    lines.append(f"| {esc(name)} | {fmt(a_)} | {fmt(b_)} | {dif:.2e} | {tol:.1e} | {'PASS' if okk else '**FAIL**'} |")
nf = sum(not o[-1] for o in out)
lines += ["", f"{len(out) - nf} of {len(out)} agree.",
          "Tolerances: half a unit in the key's last printed digit (absolute) plus 2e-4 relative; the key's stated rounding "
          "for values rounded to tens; relative tolerances (marked by a value below 1) for different estimators: 3e-3 for the "
          "nonlinear Southwell fit, 10 % for an independent Monte Carlo of U(k)."]
(Path(__file__).parent / "results_from_scratch.md").write_text("\n".join(lines) + "\n")
print("\n".join(lines))
sys.exit(1 if nf else 0)

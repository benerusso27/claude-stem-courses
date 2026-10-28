"""Re-solve the handout's questions from scratch and compare with the instructor key.

    python3 tests/solve_from_scratch.py      (from lab06_eccentric/)

Independent of src/lab06_analysis.py and src/lab06_model.py: plain csv + numpy/scipy, the handout's equations typed in
again, and deliberately different methods where one exists: the strain profile fitted to all ten gages at once with a
front/back offset term (instead of averaging pairs first); section properties of the angles as two rectangles by the
parallel-axis theorem (instead of Green's theorem); principal axes with explicit trigonometry from Eq. 7 (instead of an
eigen-solver); EI from scipy's curve_fit (instead of least_squares). Compares with the numbers printed in the key
(src/key_values.json).
"""
import csv
import json
import math
import re
import sys
from pathlib import Path

import numpy as np
from scipy import optimize

LAB = Path(__file__).resolve().parents[1]
KV = json.loads((LAB / "src" / "key_values.json").read_text())
meas = json.loads((LAB / "src" / "specimen_measurements.json").read_text())
rows = list(csv.DictReader(open(LAB / "sample_data.csv", newline="")))
E = meas["reference"]["E_al_GPa"] * 1e3                 # MPa
sY = meas["reference"]["sY_al_MPa"]
out = []


def num(s, i=0):
    return float(re.findall(r"-?\d[\d ]*\.?\d*", s.replace("−", "-"))[i].replace(" ", ""))


def cmp(name, mine, key, tol):
    rel = abs(mine - key) / max(abs(key), 1e-12)
    out.append((name, mine, key, rel, tol, rel <= tol))


def get(part, config):
    rr = [r for r in rows if r["part"] == part and r["config"] == config]
    P = np.array([float(r["load_N"]) for r in rr])
    imax = int(np.argmax(P))
    return [r for r in rr[: imax + 1] if float(r["load_N"]) > 100]


def g(r, k):
    return float(r[f"g{k:02d}_ue"])


def angle_props(bV, bH, t):
    """Heel at the origin, vertical leg along +y (z in [-t, 0]), horizontal leg along -z: two rectangles."""
    parts = [(bV * t, -t / 2, bV / 2, t * bV ** 3 / 12, bV * t ** 3 / 12),                       # (A, zc, yc, Iz_own, Iy_own)
             ((bH - t) * t, -(t + bH) / 2, t / 2, (bH - t) * t ** 3 / 12, t * (bH - t) ** 3 / 12)]
    A = sum(p[0] for p in parts)
    zc = sum(p[0] * p[1] for p in parts) / A
    yc = sum(p[0] * p[2] for p in parts) / A
    Iz = sum(p[3] + p[0] * (p[2] - yc) ** 2 for p in parts)
    Iy = sum(p[4] + p[0] * (p[1] - zc) ** 2 for p in parts)
    Iyz = sum(p[0] * (p[1] - zc) * (p[2] - yc) for p in parts)
    th = 0.5 * math.atan2(-2 * Iyz, Iz - Iy)                         # Eq. 7, root that gives I_u = I_max
    Iu = (Iz + Iy) / 2 + (Iz - Iy) / 2 * math.cos(2 * th) - Iyz * math.sin(2 * th)
    Iv = Iz + Iy - Iu
    return dict(A=A, zc=zc, yc=yc, Iz=Iz, Iy=Iy, Iyz=Iyz, th=th, Iu=Iu, Iv=Iv)


def sig8(pr, P, yP, zP, y, z):
    """Eq. 8: sigma = P/A + P vP v/Iu + P uP u/Iv; all coordinates from the centroid."""
    c, s = math.cos(pr["th"]), math.sin(pr["th"])
    uv = lambda yy, zz: (zz * c + yy * s, -zz * s + yy * c)  # noqa: E731
    uP, vP = uv(yP, zP)
    u, v = uv(y, z)
    return P / pr["A"] + P * vP * v / pr["Iu"] + P * uP * u / pr["Iv"]


def C_mid(P, EI, L, a):
    k = math.sqrt(P / EI)
    u = k * L / 2
    return 1 / (math.cosh(u) + k * a * math.sinh(u))


# ---------------- pre-lab (nominal) ----------------
h, b, L, a = 50.8, 12.7, 250.0, 25.0
A = h * b
PA = 30e3 / A
cmp("P1(a) σ_max at e = h/3 (MPa)", PA * (1 + 6 * (h / 3) / h), num(KV["P1_smax"]), 1e-3)
cmp("P1(a) strain at y = +20 mm (µε)", PA * (1 + 12 * (h / 3) * 20 / h ** 2) / E * 1e6, num(KV["P1_e20"]), 1e-3)
cmp("P1(b) back-face stress, Part C, Eq. 4 (MPa)", 25e3 / A * (1 - 6 * (b / 2) / b), num(KV["P1_sb"]), 1e-3)
cmp("P1(c) P_E through the thickness (kN)", math.pi ** 2 * E * h * b ** 3 / 12 / L ** 2 / 1e3, num(KV["P1_PEy"]), 1e-3)
an = angle_props(50.8, 50.8, 6.35)
cmp("P3 angle area, two rectangles (mm²)", an["A"], num(KV["P3_A"]), 1e-4)
cmp("P3 product of inertia, parallel-axis theorem (mm⁴)", an["Iyz"], num(KV["P3_Iyz"]), 1e-5)
cmp("P3 I_v = I_min (mm⁴)", an["Iv"], num(KV["P3_Iv"]), 1e-5)
yP, zP = -4.76 - an["yc"], -28.58 - an["zc"]
g1 = sig8(an, 30e3, yP, zP, 44.0 - an["yc"], 0 - an["zc"])
cmp("P3 σ at G1 from Eq. 8 (MPa)", g1, num(KV["P3_table"].split("|")[4]), 2e-3)

# ---------------- Part A: one fit to all ten gages, with a front/back offset term ----------------
bm = meas["bar"]
hm, bmw = np.mean(bm["h_mm"]), np.mean(bm["b_mm"])
yF, yB = np.array(bm["y_front_mm"]), np.array(bm["y_back_mm"])
for cfg in ("e0", "e1", "e2"):
    r = get("A", cfg)[-1]
    eps = np.array([g(r, k) for k in range(1, 11)])
    y = np.concatenate([yF, yB])
    s = np.concatenate([np.ones(5), -np.ones(5)])
    X = np.vstack([np.ones(10), y, s]).T
    e0, beta, dfb = np.linalg.lstsq(X, eps, rcond=None)[0]
    e_eff = hm * hm / 12 * beta / e0
    cmp(f"A1 e_eff at 30 kN, hole {cfg} (mm), ten-gage fit with offset term", e_eff, num(KV[f"A1_{cfg}_eff"]), 3e-3 if cfg != "e0" else 0.5)
    cmp(f"A3 out-of-plane bending, hole {cfg} (%)", 100 * dfb / e0, num(KV[f"A3_{cfg}_pb"]), 2e-3)
    if cfg != "e0":
        cmp(f"A2 neutral axis −ε₀/β, hole {cfg} (mm)", -e0 / beta, num(KV[f"A2_{cfg}_y0"]), 3e-3)
EIz = E * bmw * hm ** 3 / 12
cmp("A1 C_mid in-plane at 30 kN (Eq. 9)", C_mid(30e3, EIz, L, a), num(KV["A1_C"]), 1e-4)

# ---------------- Part B ----------------
am = meas["angle"]
pa = angle_props(np.mean(am["bV_mm"]), np.mean(am["bH_mm"]), np.mean(am["t_mm"]))
cmp("A4 measured angle: I_u (mm⁴)", pa["Iu"], num(KV["B_Iu"]), 1e-5)
cmp("A4 measured angle: θp (°)", math.degrees(pa["th"]), num(KV["B_th"]), 1e-3)
rb = get("B", "angle")
P = np.array([float(r["load_N"]) for r in rb])
gp = [(am["gages_mm"][k]["z"], am["gages_mm"][k]["y"]) for k in ("G1", "G2", "G3", "G4")]
yPm, zPm = am["load_y_mm"] - pa["yc"], am["load_z_mm"] - pa["zc"]
tab = KV["A4_table"].split("\n")
meas_s = []
for i in range(4):
    slope = np.polyfit(P, [g(r, i + 1) for r in rb], 1)[0]
    sm = E * slope * 1e-6 * 30e3
    meas_s.append(sm)
    cmp(f"A4 measured σ at G{i + 1}, 30 kN (MPa)", sm, num(tab[i].split("|")[2]), 2e-3)
    sp = sig8(pa, 30e3, yPm, zPm, gp[i][1] - pa["yc"], gp[i][0] - pa["zc"])
    cmp(f"A4 Eq. 8 at G{i + 1}, measured section (MPa)", sp, num(tab[i].split("|")[3]), 2e-3)
Gm = np.array([[1, y - pa["yc"], z - pa["zc"]] for z, y in gp])
cf = np.linalg.lstsq(Gm, np.array(meas_s), rcond=None)[0]
cmp("A4 neutral-axis direction from the four gages (°)", math.degrees(math.atan2(-cf[2], cf[1])), num(KV["B_phim"]), 2e-3)

# ---------------- Part C ----------------
rc = get("C", "ez")
ez = bm["zP_mm"]["ez"]
EIy = E * hm * bmw ** 3 / 12
r = rc[-1]
ax = np.mean([(g(r, k) + g(r, k + 5)) / 2 for k in range(1, 6)])
bd = np.mean([(g(r, k) - g(r, k + 5)) / 2 for k in range(1, 6)])
cmp("M1 C_mid at 25 kN from Eq. 12", bd / ax * bmw / (6 * ez), num(KV["M1_Cm"]), 1e-3)
cmp("M1 C_mid at 25 kN from Eq. 9", C_mid(float(r["load_N"]), EIy, L, a), num(KV["M1_Cp"]), 1e-3)
cmp("M1 C near the block from Eq. 12", (g(r, 11) - g(r, 12)) / (g(r, 11) + g(r, 12)) * bmw / (6 * ez), num(KV["M1_Em"]), 1e-3)
P5 = optimize.brentq(lambda p_: 1 / C_mid(p_, EIy, L, a) - 1.05, 10, 1e5)
cmp("M1 load where Eq. 4 is 5 % off, through the thickness (kN)", P5 / 1e3, num(KV["M1_P5w"]), 2e-3)
P5s = optimize.brentq(lambda p_: 1 / C_mid(p_, EIz, L, a) - 1.05, 10, 1e7)
cmp("M1 same, across the width (kN)", P5s / 1e3, num(KV["M1_P5s"]), 2e-3)
Pc = np.array([float(x["load_N"]) for x in rc])
wc = np.array([float(x["w_mid_mm"]) for x in rc])
popt, _ = optimize.curve_fit(lambda pp, EI: [ez * (1 - C_mid(p_, EI, L, a)) for p_ in pp], Pc, wc, p0=[EIy])
cmp("C2 EI from the LVDT readings, curve_fit (N·m²)", popt[0] / 1e9 * 1e3, num(KV["C2_EI"]), 2e-3)

# ---------------- X2: the Lab 8 tube ----------------
ro, ri, F, Lb, aL = 19.05, 15.875, 600.0, 250.0, 200.0
I = math.pi * (ro ** 4 - ri ** 4) / 4
cmp("X2 σ at the top, F L_b c/I (MPa)", F * Lb * ro / I, num(KV["X2_stop"]), 1e-3)
cmp("X2 τ at the side, Tc/J + VQ/(It) (MPa)", F * aL * ro / (2 * I) + F * (ro ** 3 - ri ** 3) / 3 / (I * (ro - ri)), num(KV["X2_tside"]), 1e-3)

# ---------------- D1 ----------------
cat = [("L38", 38.1, 38.1, 4.76, 22.2), ("L51a", 50.8, 50.8, 4.76, 28.6), ("L51b", 50.8, 50.8, 6.35, 28.6), ("L64", 63.5, 63.5, 6.35, 34.9),
       ("L76x51 long", 50.8, 76.2, 6.35, 44.5), ("L76x51 short", 76.2, 50.8, 6.35, 28.6), ("L76a", 76.2, 76.2, 6.35, 44.5), ("L76b", 76.2, 76.2, 9.53, 44.5)]
sa = 0.6 * sY
best = None
for name, bv, bh, t, gg in cat:
    pd = angle_props(bv, bh, t)
    corners = [(0, 0), (0, bv), (-t, bv), (-bh, t), (-bh, 0)]
    yl, zl = -9.53 / 2 - pd["yc"], -gg - pd["zc"]
    smax = max(sig8(pd, 40e3, yl, zl, y - pd["yc"], z - pd["zc"]) for z, y in corners)
    if smax <= sa and (best is None or pd["A"] < best[1] - 1e-9 or (abs(pd["A"] - best[1]) < 1e-9 and smax < best[2])):
        best = (name, pd["A"], smax)
cmp("D1 reference design: largest stress (MPa)", best[2], num(KV["D_best_s"]), 1e-3)
cmp("D1 allowable stress 0.6 σ_Y (MPa)", sa, num(KV["D_sa"]), 1e-3)

lines = ["## Lab 6 — handout questions re-solved from scratch vs. the instructor key", "",
         "| Question / quantity | From scratch | Key | Rel. difference | Tolerance | Result |", "|---|---:|---:|---:|---:|---|"]
for name, a_, b_, rel, tol, okk in out:
    lines.append(f"| {name} | {a_:.6g} | {b_:.6g} | {rel:.1e} | {tol:.0e} | {'PASS' if okk else '**FAIL**'} |")
nf = sum(not o[-1] for o in out)
lines += ["", f"{len(out) - nf} of {len(out)} agree.",
          "Tolerances: about 1e-3 where the key prints a rounded value of the same quantity; 2e-3 to 3e-3 where a different "
          "estimator is used on purpose (ten-gage fit with an offset term, curve_fit); 0.5 for the e = 0 eccentricity, which is "
          "near zero and dominated by noise."]
(Path(__file__).parent / "results_from_scratch.md").write_text("\n".join(lines) + "\n")
print("\n".join(lines))
sys.exit(1 if nf else 0)

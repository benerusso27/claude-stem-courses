"""Re-solve the handout's questions from scratch and compare with the instructor key.

    python3 tests/solve_from_scratch.py      (from lab02_axial_thermal/)

Independent of src/lab02_analysis.py: plain csv + numpy.polyfit, the handout's equations typed in again,
and deliberately different estimators where one exists (the knee located by intersecting the post-contact
line with F = 0 instead of a two-parameter scan; the three-member problem solved by bisection on the cap
displacement instead of event marching). Compares with src/results.json and with the numbers printed in
the key (src/key_values.json).
"""
import csv
import json
import math
import re
import sys
from pathlib import Path

import numpy as np

LAB = Path(__file__).resolve().parents[1]
res = json.loads((LAB / "src" / "results.json").read_text())
KV = json.loads((LAB / "src" / "key_values.json").read_text())
meas = json.loads((LAB / "src" / "specimen_measurements.json").read_text())
rows = list(csv.DictReader(open(LAB / "sample_data.csv", newline="")))
out = []


def num(s, i=0):
    """i-th number printed in a key string ('68.46 ± 0.93' -> 68.46)."""
    return float(re.findall(r"-?\d[\d ]*\.?\d*", s.replace("−", "-"))[i].replace(" ", ""))


def cmp(name, mine, key, tol):
    rel = abs(mine - key) / max(abs(key), 1e-12)
    out.append((name, mine, key, rel, tol, rel <= tol))


def col(part, c):
    return np.array([float(r[c]) if r[c].strip() else np.nan for r in rows if r["part"] == part])


PI = math.pi
E_al, E_st, nu_t, a_al, a_st = 68900.0, 205000.0, 0.33, 23.6e-6, 11.7e-6

# ---------------- pre-lab ----------------
A = 25.40 * 6.35
cmp("P1 stress at 18 kN (MPa)", 18000 / A, num(KV["P1_sig"]), 1e-3)
cmp("P1 axial strain (µε)", 18000 / A / E_al * 1e6, num(KV["P1_ex"]), 1e-3)
A1 = PI * 12.70 ** 2 / 4
A2 = PI * (25.40 ** 2 - 19.05 ** 2) / 4
k1 = E_st * A1 / 150
k2 = E_al * A2 / 149.96
Pg = k1 * 0.040
s = k2 / (k1 + k2)
cmp("P2 P_gap (kN)", Pg / 1e3, num(KV["Pgn"]), 1e-3)
cmp("P2 share s", s, num(KV["sn"]), 1e-3)
for P in (10, 20, 30):
    cmp(f"P2 F2 at {P} kN (kN)", -s * (P * 1e3 - Pg) / 1e3, num(KV[f"F2n_{P}"]), 1e-3)
Ab, As = PI * 10 ** 2 / 4, PI * (20 ** 2 - 10.5 ** 2) / 4
fl = 100 / (E_st * Ab) + 100 / (E_al * As)
cmp("P3 dF/dT (N/K)", (a_al - a_st) * 100 / fl, num(KV["dFdT_n"]), 1e-3)
cmp("P3 bolt stress at 80 °C (MPa)", (2000 + 60 * (a_al - a_st) * 100 / fl) / Ab, num(KV["sb80_n"]), 1e-3)
fl_sw = 100 / (E_al * Ab) + 100 / (E_st * As)
cmp("P3(b) separation ΔT, swapped materials (K)", 2000 / ((a_al - a_st) * 100 / fl_sw), num(KV["dTsep"]), 2e-3)
cmp("P4 offset for β = 5 % (mm)", 0.05 * 6.35 / 6, num(KV["P4_e"]), 1e-3)
# P6: march the load until the rod reaches 370 MPa (no closed form used)
P = 0.0
while True:
    F1 = -P if P < Pg else -(Pg + (1 - s) * (P - Pg))
    if -F1 >= 370 * A1:
        break
    P += 1.0
cmp("P6 press load at rod yield (kN), by marching", P / 1e3, num(KV["P6_Py"]), 2e-3)
cmp("handout worked example: δ of 20×5×300 mm bar at 10 kN (mm)", 10e3 * 300 / (68900 * 100), 0.435, 2e-3)
cmp("handout worked example: cone vs mean-diameter flexibility ratio", (4 * 300 / (PI * 68900 * 30 * 15)) / (300 / (68900 * PI * 22.5 ** 2 / 4)), 1.125, 1e-3)
kb = 97e3 * PI * 16 ** 2 / 4 / 200
kt = 205e3 * PI * (30 ** 2 - 24 ** 2) / 4 / 200
cmp("handout worked example: brass/steel P_gap (kN)", kb * 0.12 / 1e3, 11.7, 2e-3)
cmp("handout worked example: brass/steel share", kt / (kb + kt), 0.728, 1e-3)
cmp("handout worked example: restrained steel heated 50 K (MPa)", 205e3 * 11.7e-6 * 50, 120, 1e-3)
fl8 = 80 / (205e3 * PI * 64 / 4) + 80 / (68.9e3 * PI * (256 - 8.5 ** 2) / 4)
cmp("handout worked example: 8 mm bolt, ΔF for 40 K (kN)", 11.9e-6 * 80 * 40 / fl8 / 1e3, 2.41, 2e-3)
cmp("handout §2.2: β for e = 0.05 mm on 6.35 mm (printed as 4.7 %)", 6 * 0.05 / 6.35, 0.047, 1.1e-2)

# ---------------- Part A ----------------
b, t = np.mean(meas["A_width_mm"]), np.mean(meas["A_thickness_mm"])
P = col("A", "load_N")
ef, eb = col("A", "strain_axial_front_ue") * 1e-6, col("A", "strain_axial_back_ue") * 1e-6
tf, tb = col("A", "strain_transverse_front_ue") * 1e-6, col("A", "strain_transverse_back_ue") * 1e-6
sig = P / (b * t)
ex, ey = (ef + eb) / 2, (tf + tb) / 2
E = np.polyfit(ex, sig, 1)[0] / 1e3
cmp("A1 E (GPa)", E, res["A"]["E"], 1e-9)
cmp("A1 E printed in key", E, num(KV["E_A"]), 1e-3)
nu = -np.polyfit(ex, ey, 1)[0]
cmp("A1 ν", nu, num(KV["nu"]), 2e-3)
cmp("A1 G = E/2(1+ν) (GPa)", E / (2 * (1 + nu)), num(KV["G"]), 1e-3)
hi = P > 4000
beta = np.mean((ef[hi] - eb[hi]) / (ef[hi] + eb[hi]))
cmp("A2 β", beta, num(KV["beta"]), 1e-3)
cmp("A2 offset e = βt/6 (mm)", beta * t / 6, num(KV["e_mis"]), 5e-3)
Ef, Eb = np.polyfit(ef, sig, 1)[0] / 1e3, np.polyfit(eb, sig, 1)[0] / 1e3
cmp("A2 harmonic mean of single-gage E equals average-strain E", 2 / (1 / Ef + 1 / Eb), E, 2e-3)

# ---------------- Part B: knee by intersecting the post-contact line with F = 0 ----------------
P = col("B", "load_N")
up = np.arange(len(P)) <= np.argmax(P)
At = PI * (np.mean(meas["B_tube_do_mm"]) ** 2 - np.mean(meas["B_tube_di_mm"]) ** 2) / 4
Ar = PI * np.mean(meas["B_rod_d_mm"]) ** 2 / 4
Ft = E * 1e3 * At * (col("B", "strain_tube_front_ue") + col("B", "strain_tube_back_ue")) / 2 * 1e-6
post = up & (P > 9000)
m, c = np.polyfit(P[post], Ft[post], 1)
Pg_line = -c / m
cmp("A3 P_gap by line intersection vs key's two-parameter fit (kN)", Pg_line / 1e3, num(KV["Pg"]), 5e-3)
cmp("A3 share s = −slope above the knee", -m, num(KV["share"]), 5e-3)
cmp("A3 gap g = P_gap/k1 (mm)", Pg_line / (E_st * Ar / 150), num(KV["gap"]), 1e-2)
cmp("A3 theory share, Eq. 12 with measured E", E * At / (E * At + 205 * Ar), num(KV["share_th"]), 1e-3)
i30 = int(np.argmax(P))
cmp("A4 tube force at 30 kN (kN)", Ft[i30] / 1e3, num(KV["Ft30"]), 1e-3)
cmp("A4 rod stress at 30 kN (MPa)", -(P[i30] + Ft[i30]) / Ar, num(KV["srod30"]), 1e-3)
cmp("A4 no-gap overstatement (%)", 100 * (-(E * At / (E * At + 205 * Ar)) * P[i30] / Ft[i30] - 1), num(KV["nogap_err"]), 1e-2)
cmp("A4 tolerance for 5 % at 30 kN (µm)", 30e3 / 21 / (E_st * Ar / 150) * 1e3, num(KV["g5"]), 1e-2)
dial = col("B", "dial_mm")
post2 = up & (P > Pg_line + 2500)
sl = np.polyfit(P[post2] / 1e3, dial[post2], 1)[0]
Cboth = 150 / (E_st * Ar + E * 1e3 * At) * 1e3
cmp("A5 cap compliance above the knee (µm/kN)", (sl - Cboth) * 1e3, num(KV["C2"]), 2e-2)
i10, i20 = int(np.argmin(np.where(up, abs(P - 10e3), np.inf))), int(np.argmin(np.where(up, abs(P - 20e3), np.inf)))
cmp("M1(a) F2(20 kN)/F2(10 kN)", Ft[i20] / Ft[i10], num(KV["F_ratio"]), 2e-3)
cmp("M1(b) g_crit = σY L/E (mm)", 370 * 150 / 205e3, num(KV["gcrit"]), 2e-3)

# ---------------- Part C ----------------
T, eb_c = col("C", "temperature_C"), col("C", "strain_bolt_ue") * 1e-6
Ab_m = PI * np.mean(meas["C_bolt_d_mm"]) ** 2 / 4
As_m = PI * (np.mean(meas["C_sleeve_do_mm"]) ** 2 - np.mean(meas["C_sleeve_di_mm"]) ** 2) / 4
dFdT = np.polyfit(T, eb_c, 1)[0] * E_st * Ab_m
cmp("A6 dF/dT (N/K)", dFdT, num(KV["dFdT"]), 1e-3)
flm = 100 / (E_st * Ab_m) + 100 / (E * 1e3 * As_m)
cmp("A6 prediction, Eq. 16 (N/K)", (a_al - a_st) * 100 / flm, num(KV["dFdT_th"]), 1e-3)
F0 = E_st * Ab_m * np.mean(eb_c[np.abs(T - 20) < 1])
cmp("A6 preload (kN)", F0 / 1e3, num(KV["F0"]), 1e-3)
cmp("A6 bolt stress at 80 °C (MPa)", (F0 + 60 * dFdT) / Ab_m, num(KV["sb80"]), 1e-3)
cmp("C2 α of 6061-T6 (10⁻⁶/K)", (a_st + dFdT * flm / 100) * 1e6, num(KV["alpha_meas"]), 1e-3)
cmp("M1(c) separation ΔT, Al bolt in steel sleeve (K)", 2000 / ((a_al - a_st) * 100 / (100 / (E_al * PI * 25) + 100 / (E_st * PI * (400 - 110.25) / 4))), num(KV["sw_dTsep"]), 2e-3)
cmp("C3 dilatation at 18 kN (10⁻⁶)", (1 - 2 * nu) * 18011 / (b * t) / (E * 1e3) * 1e6, num(KV["C3_dil"]), 3e-3)
cmp("X1 critical L/d for 1018", PI / 2 * math.sqrt(205e3 / 370), num(KV["X1_Ld"]), 2e-3)

# ---------------- X3 by bisection on the cap displacement ----------------
ks = [E_st * Ar / 150, E * 1e3 * At / 150, 97e3 * PI * (32 ** 2 - 27 ** 2) / 4 / 150]
g1 = Pg_line / ks[0]
gaps = [0, res["B"]["gap_mm"], res["B"]["gap_mm"] + 0.040]
total = lambda D: sum(k * max(0, D - g) for k, g in zip(ks, gaps))  # noqa: E731
lo, hi_ = 0.0, 1.0
for _ in range(200):
    mid = (lo + hi_) / 2
    lo, hi_ = (mid, hi_) if total(mid) < 30e3 else (lo, mid)
D = (lo + hi_) / 2
cmp("X3 brass tube force at 30 kN (kN)", -ks[2] * max(0, D - gaps[2]) / 1e3, num(KV["X3_F3"]), 2e-3)
cmp("X3 second closing load (kN)", total(gaps[2]) / 1e3, num(KV["X3_P2"]), 2e-3)

# ---------------- D1 ----------------
aL = a_al * 3000
gmin = aL * (55 - 10) - 40 * 3000 / (E * 1e3)
gmax = 8.0 - aL * (20 + 25)
cmp("D1 minimum gap (mm)", gmin, num(KV["D_gmin"]), 5e-3)
cmp("D1 maximum gap (mm)", gmax, num(KV["D_gmax"]), 5e-3)
# brute force check: a 3.0 ± 1.0 mm specification satisfies both requirements over the whole envelope
okD = True
for g in (2.0, 3.0, 4.0):
    for Ti in np.linspace(10, 20, 11):
        for Ts in np.linspace(-25, 55, 81):
            closure = aL * (Ts - Ti) - g
            stress = E * 1e3 * max(0.0, closure) / 3000
            gap = g - aL * (Ts - Ti)
            okD &= stress <= 40 + 1e-9 and gap <= 8.0 + 1e-9
out.append(("D1 3.0 ± 1.0 mm meets both requirements over the full envelope (brute force)", 1.0, 1.0 if okD else 0.0, 0.0 if okD else 1.0, 0, okD))

lines = ["## Lab 2 — handout questions re-solved from scratch vs. the instructor key", "",
         "| Question / quantity | From scratch | Key | Rel. difference | Tolerance | Result |", "|---|---:|---:|---:|---:|---|"]
for name, a, b_, rel, tol, okk in out:
    lines.append(f"| {name} | {a:.6g} | {b_:.6g} | {rel:.1e} | {tol:.0e} | {'PASS' if okk else '**FAIL**'} |")
nf = sum(not o[-1] for o in out)
lines += ["", f"{len(out) - nf} of {len(out)} agree.",
          "Tolerances: 1e-3 where the key prints a rounded value of the same quantity; 5e-3 to 2e-2 where a different "
          "estimator is used on purpose (knee by line intersection vs. two-parameter fit; dial slope above a slightly different knee)."]
(Path(__file__).parent / "results_from_scratch.md").write_text("\n".join(lines) + "\n")
print("\n".join(lines))
sys.exit(1 if nf else 0)

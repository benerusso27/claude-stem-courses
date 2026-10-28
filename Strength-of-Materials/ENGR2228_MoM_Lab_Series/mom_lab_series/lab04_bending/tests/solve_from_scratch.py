"""Re-solve the handout's questions from scratch and compare with the instructor key.

    python3 tests/solve_from_scratch.py      (from lab04_bending/)

Independent of src/lab04_analysis.py and src/lab04_model.py: plain csv + numpy, the handout's equations typed in
again, and deliberately different methods where one exists (transformed section by fine strip integration instead
of the parallel-axis formula; Eq. 12 inverted by bisection instead of algebra; E as the mean of M/(κI) over the
steps instead of the slope; ν from a fit through the origin; the bimetal curvature from Timoshenko's closed-form
formula instead of a 2 × 2 equilibrium solve; catalog properties recomputed from the dimensions). Compares with the
numbers printed in the key (src/key_values.json).
"""
import csv
import json
import math
import re
import sys
from pathlib import Path

import numpy as np

LAB = Path(__file__).resolve().parents[1]
KV = json.loads((LAB / "src" / "key_values.json").read_text())
meas = json.loads((LAB / "src" / "specimen_measurements.json").read_text())
rows = list(csv.DictReader(open(LAB / "sample_data.csv", newline="")))
out = []


def num(s, i=0):
    return float(re.findall(r"-?\d[\d ]*\.?\d*", s.replace("−", "-"))[i].replace(" ", ""))


def cmp(name, mine, key, tol):
    rel = abs(mine - key) / max(abs(key), 1e-12)
    out.append((name, mine, key, rel, tol, rel <= tol))


def col(part, c):
    return np.array([float(r[c]) if r[c].strip() else np.nan for r in rows if r["part"] == part])


def bisect(f, lo, hi, n=200):
    flo = f(lo)
    for _ in range(n):
        mid = 0.5 * (lo + hi)
        if (f(mid) > 0) == (flo > 0):
            lo, flo = mid, f(mid)
        else:
            hi = mid
    return 0.5 * (lo + hi)


ref = meas["reference"]
E_al, E_st, sY = ref["E_al_GPa"] * 1e9, ref["E_st_GPa"] * 1e9, ref["sY_al_MPa"] * 1e6

# ---------------- worked examples and pre-lab (nominal section, Table 1) ----------------
cmp("§2.1 example: M under the load = 6 kN × 0.8 m (kN·m)", 6 * 0.8, 4.8, 1e-12)
Ie = 40 * 80 ** 3 / 12
cmp("§2.2 example: σ_m = Mc/I (MPa)", 3e6 * 40 / Ie, 70.3, 1e-3)
cmp("§2.2 example: κ = M/(EI) (1/m)", 3e3 / (205e9 * Ie * 1e-12), 0.00857, 1e-3)
b, h, a, L = 25.4e-3, 50.8e-3, 0.2, 0.6
I = b * h ** 3 / 12
cmp("P1 I (10⁵ mm⁴)", I * 1e12 / 1e5, num(KV["P1_I"]), 1e-4)
M20 = 10e3 * a
cmp("P1 σ at 20 kN (MPa)", M20 * (h / 2) / I / 1e6, num(KV["P1_sig"]), 1e-3)
cmp("P1 κ at 20 kN (1/m)", M20 / (E_al * I), num(KV["P1_k"]), 1e-3)
PY = 2 * sY * b * h ** 2 / 6 / a
cmp("P1 first-yield load P_Y (kN)", PY / 1e3, num(KV["P1_PY"]), 1e-3)
cmp("P1 fully plastic load from Z = bh²/4 (kN)", 2 * sY * b * h ** 2 / 4 / a / 1e3, num(KV["P1_Pp"]), 1e-3)
# P2(c): moments about the right support
a1, a2 = 0.2, 0.3996
RA = 0.5 * ((L - a1) + (L - a2)) / L
cmp("P2(c) R_A/P by moments about B", RA, num(KV["P2c_RA"]), 1e-5)
# P3 by fine strip integration of the transformed section
n = E_st / E_al
ts = 6.35e-3
N = 200000
y = (np.arange(N) + 0.5) * (h + ts) / N
w = np.where(y < ts, n * b, b)
dA = w * (h + ts) / N
yb = np.sum(y * dA) / np.sum(dA)
It = np.sum((y - yb) ** 2 * dA)
cmp("P3 transformed centroid by strip integration (mm)", yb * 1e3, num(KV["P3_ybar"]), 1e-4)
cmp("P3 I_t by strip integration (10⁵ mm⁴)", It * 1e12 / 1e5, num(KV["P3_It"]), 1e-4)
Mb = 7.5e3 * a
cmp("P3 steel bottom stress n M ȳ/I_t (MPa)", n * Mb * yb / It / 1e6, num(KV["P3_stbot"]), 1e-3)
cmp("P3 aluminum top stress (MPa)", -Mb * (h + ts - yb) / It / 1e6, num(KV["P3_altop"]), 1e-3)
# P4: invert Eq. 12 by bisection
MY = sY * b * h ** 2 / 6
kY = sY / (E_al * h / 2)
M40 = 20e3 * a
k40 = bisect(lambda k: 1.5 * MY * (1 - (kY / k) ** 2 / 3) - M40, kY, 100 * kY)
cmp("P4 κ at 40 kN by bisection on Eq. 12 (1/m)", k40, num(KV["P4_k"]), 1e-3)
cmp("P4 permanent curvature (1/m)", k40 - M40 / (E_al * I), num(KV["P4_kp"]), 2e-3)
cmp("P4 residual stress at the top (MPa)", (-sY + M40 * (h / 2) / I) / 1e6, num(KV["P4_res"]), 1e-3)

# ---------------- analysis ----------------
bm, hm, tsm = (np.mean(meas[k]) * 1e-3 for k in ("b_mm", "h_mm", "ts_mm"))
am = 0.5 * (meas["a1_mm"] + meas["span_mm"] - meas["a2_mm"]) * 1e-3
Im = bm * hm ** 3 / 12
SIDE = [f"strain_side{j}_ue" for j in range(1, 6)]


def profiles(part, ys_mm, H):
    yy = np.r_[ys_mm, H, 0.0] * 1e-3
    E = np.c_[np.column_stack([col(part, c) for c in SIDE]), col(part, "strain_top_ue"), col(part, "strain_bottom_ue")] * 1e-6
    res = []
    for e in E:
        s, c0 = np.polyfit(yy, e, 1)
        res.append((-s, -c0 / s if s else np.nan))
    return np.array(res)


PA = col("A", "load_N")
sel = PA > 1000
prA = profiles("A", meas["yA_mm"], hm * 1e3)
cmp("A2 mean neutral axis, bar A (mm)", np.mean(prA[sel, 1]) * 1e3, num(KV["A2_yNA"]), 1e-4)
cmp("A2 κ at 20 kN (1/m)", prA[int(np.argmax(PA)), 0], num(KV["A2_k20"]), 1e-4)
MA = PA / 2 * am
E_slope = np.polyfit(prA[sel, 0], MA[sel], 1)[0] / Im
cmp("A3 E from the slope of M vs κ (GPa)", E_slope / 1e9, num(KV["A3_E"]), 1e-3)
up = sel & (np.arange(len(PA)) <= int(np.argmax(PA)))
E_mean = np.mean(MA[up] / (prA[up, 0] * Im))
cmp("A3 E as the mean of M/(κI) over the loading steps instead (GPa)", E_mean / 1e9, num(KV["A3_E"]), 3e-3)
et, etr = col("A", "strain_top_ue")[sel], col("A", "strain_transverse_top_ue")[sel]
cmp("A4 ν from a fit through the origin", -np.sum(et * etr) / np.sum(et ** 2), num(KV["A4_nu"]), 5e-3)
S = Im / (hm / 2)
Mper = {}
for c, x in (("strain_bottom_x100_ue", 0.1), ("strain_bottom_x150_ue", 0.15)):
    Mper[x] = E_slope * S * np.polyfit(PA[sel], col("A", c)[sel] * 1e-6, 1)[0]
cmp("A1 V/P = ΔM/Δx between the shear-span gages", (Mper[0.15] - Mper[0.1]) / 0.05, num(KV["A1_V"]), 2e-3)
# Part B
PB = col("B", "load_N")
selB = PB > 1000
prB = profiles("B", meas["yB_mm"], (hm + tsm) * 1e3)
cmp("A5 measured neutral axis, bar B (mm)", np.mean(prB[selB, 1]) * 1e3, num(KV["A5_y"]), 1e-4)
cmp("A5 measured EI, bar B (N·m²)", np.polyfit(prB[selB, 0], PB[selB] / 2 * am, 1)[0], num(KV["A5_EI"]), 1e-3)
nB = E_st / E_slope
A1_, A2_ = bm * hm, nB * bm * tsm
ybB = (A1_ * (tsm + hm / 2) + A2_ * tsm / 2) / (A1_ + A2_)
cmp("A5 predicted neutral axis with measured E (mm)", ybB * 1e3, num(KV["A5_yp"]), 1e-3)
# Part C
PC, kC = col("C", "load_N"), profiles("C", meas["yA_mm"], hm * 1e3)[:, 0]
im = int(np.argmax(PC))
cmp("A6 κ at 40 kN (1/m)", kC[im], num(KV["A6_kmax"]), 2e-3)
cmp("A6 permanent curvature after unloading (1/m)", kC[-1], num(KV["A6_kres"]), 2e-3)
Mmax = PC[im] / 2 * am
cmp("A6 Eq. 14 predicted permanent curvature (1/m)", kC[im] - Mmax / (E_slope * Im), num(KV["A6_kresp"]), 2e-3)
MYm, kYm = sY * bm * hm ** 2 / 6, sY / (E_slope * hm / 2)
cmp("A6 EPP moment at the measured κ (N·m)", 1.5 * MYm * (1 - (kYm / kC[im]) ** 2 / 3), num(KV["A6_Mepp"]), 1e-3)
emax = kC[im] * hm / 2
s_act = bisect(lambda s: s / E_slope + 0.002 * (s / sY) ** ref["m_RO"] - emax, 0, 600e6)
cmp("A6 actual extreme-fiber stress from the Ramberg–Osgood curve by bisection (MPa)", s_act / 1e6, num(KV["A6_sact"]), 2e-3)
cmp("A6 flexure stress Mc/I (MPa)", Mmax * (hm / 2) / Im / 1e6, num(KV["A6_sflex"]), 1e-3)
half, mm_ = meas["bar_length_mm"] / 2e3, (meas["span_mm"] - 2 * am * 1e3) / 2e3
cmp("A6 straightedge gap, curvature confined to the middle (mm)", kC[-1] * mm_ * (half - mm_ / 2) * 1e3, num(KV["A6_gapmid"]), 3e-3)

# ---------------- challenge / extension ----------------
bI, hI, tf, tw = 0.100, 0.200, 0.010, 0.006
II = (bI * hI ** 3 - (bI - tw) * (hI - 2 * tf) ** 3) / 12
ZI = 2 * (bI * tf * (hI / 2 - tf / 2) + tw * (hI / 2 - tf) ** 2 / 2)
cmp("C1 I-section shape factor Z/S (first moments of the halves)", ZI / (II / (hI / 2)), num(KV["C1_k"]), 1e-4)
# X3: T-section, flange on top
Aw, Af = tw * (hI - tf), bI * tf
At = Aw + Af
yel = (Aw * (hI - tf) / 2 + Af * (hI - tf / 2)) / At
yp = (At / 2) / tw
cmp("X3 elastic neutral axis (mm)", yel * 1e3, num(KV["X3_ybar"]), 1e-4)
cmp("X3 plastic neutral axis (equal areas, mm)", yp * 1e3, num(KV["X3_yp"]), 1e-4)
IT = tw * (hI - tf) ** 3 / 12 + Aw * ((hI - tf) / 2 - yel) ** 2 + bI * tf ** 3 / 12 + Af * (hI - tf / 2 - yel) ** 2
ZT = tw * yp ** 2 / 2 + tw * (hI - tf - yp) ** 2 / 2 + Af * (hI - tf / 2 - yp)
cmp("X3 shape factor Z/S", ZT / (IT / max(yel, hI - yel)), num(KV["X3_k"]), 1e-3)
# X1: Timoshenko's bimetal formula (equal widths), layer 1 = steel, layer 2 = aluminum
t1, t2, a_1, a_2 = tsm, hm, 11.7e-6, 23.6e-6
m_, n_ = t1 / t2, E_st / E_slope
kT = 6 * (a_2 - a_1) * (1 + m_) ** 2 / ((t1 + t2) * (3 * (1 + m_) ** 2 + (1 + m_ * n_) * (m_ ** 2 + 1 / (m_ * n_))))
cmp("X1 |κ|/ΔT from Timoshenko's bimetal formula (10⁻³ 1/(m·K))", kT * 1e3, abs(num(KV["X1_k"])), 1e-3)
# D1: catalog properties from dimensions, lightest acceptable section
CAT = [("I-100", "I", 100, 55, 5.7, 4.1), ("I-120", "I", 120, 64, 6.3, 4.4), ("I-140", "I", 140, 73, 6.9, 4.7), ("I-160", "I", 160, 82, 7.4, 5.0),
       ("I-180", "I", 180, 91, 8.0, 5.3), ("I-200", "I", 200, 100, 8.5, 5.6), ("RT-100x50x4", "T", 100, 50, 4.0, 0), ("RT-120x60x5", "T", 120, 60, 5.0, 0),
       ("RT-150x100x5", "T", 150, 100, 5.0, 0), ("RT-200x100x6", "T", 200, 100, 6.0, 0)]
Ld, wd, Pd = 3.0, 3.0e3, 5.0e3
Md = wd * Ld ** 2 / 8 + Pd * Ld / 4
cmp("D1 maximum moment (kN·m)", Md / 1e3, num(KV["D_M"]), 1e-6)
for mat, E_, sy, rho, kk in (("steel", E_st, (ref["sY_st_MPa"] - 2 * ref["u_sY_st_MPa"]) * 1e6, 7870, "s"),
                             ("aluminum", E_slope, (ref["sY_al_MPa"] - 2 * ref["u_sY_al_MPa"]) * 1e6, 2700, "a")):
    best = None
    for name, kind, hh, bb, t, tw_ in CAT:
        hh, bb, t, tw_ = hh * 1e-3, bb * 1e-3, t * 1e-3, tw_ * 1e-3
        if kind == "I":
            Ix = (bb * hh ** 3 - (bb - tw_) * (hh - 2 * t) ** 3) / 12
            Ar = bb * hh - (bb - tw_) * (hh - 2 * t)
        else:
            Ix = (bb * hh ** 3 - (bb - 2 * t) * (hh - 2 * t) ** 3) / 12
            Ar = bb * hh - (bb - 2 * t) * (hh - 2 * t)
        ok = Md * (hh / 2) / Ix <= sy / 1.67 and 5 * wd * Ld ** 4 / (384 * E_ * Ix) + Pd * Ld ** 3 / (48 * E_ * Ix) <= Ld / 240
        if ok and (best is None or Ar * rho < best[1]):
            best = (name, Ar * rho)
    out.append((f"D1 lightest acceptable {mat} section: {best[0]} (key: {KV['D_best_' + kk]})", 1.0, 1.0 if best[0] == KV["D_best_" + kk] else 0.0,
                0.0 if best[0] == KV["D_best_" + kk] else 1.0, 0.0, best[0] == KV["D_best_" + kk]))
    cmp(f"D1 {mat}: mass per meter of the chosen section (kg/m)", best[1], num(KV["D_bm_" + kk]), 1e-3)
# handout Table 6 printed properties vs dimensions
H = (LAB / "src" / "lab04_handout.md").read_text(encoding="utf-8")
for name, kind, hh, bb, t, tw_ in CAT:
    if kind == "I":
        Ix = (bb * hh ** 3 - (bb - tw_) * (hh - 2 * t) ** 3) / 12
    else:
        Ix = (bb * hh ** 3 - (bb - 2 * t) * (hh - 2 * t) ** 3) / 12
    line = [ln for ln in H.splitlines() if ln.startswith(f"| {name} |")][0].split("|")
    cmp(f"Table 6 {name}: printed I (10⁶ mm⁴)", Ix / 1e6, float(line[6]), 6e-4)
    cmp(f"Table 6 {name}: printed S (10³ mm³)", Ix / (hh / 2) / 1e3, float(line[7]), 6e-4)

lines = ["## Lab 4 — handout questions re-solved from scratch vs. the instructor key", "",
         "| Question / quantity | From scratch | Key | Rel. difference | Tolerance | Result |", "|---|---:|---:|---:|---:|---|"]
for name, a_, b_, rel, tol, okk in out:
    lines.append(f"| {name} | {a_:.6g} | {b_:.6g} | {rel:.1e} | {tol:.0e} | {'PASS' if okk else '**FAIL**'} |")
nf = sum(not o[-1] for o in out)
lines += ["", f"{len(out) - nf} of {len(out)} agree.",
          "Tolerances: about 1e-3 where the key prints a rounded value of the same quantity; up to 5e-3 where a different "
          "estimator is used on purpose (mean of M/(κI), fit through the origin, middle-only gap); 6e-4 for the 4-figure catalog table."]
(Path(__file__).parent / "results_from_scratch.md").write_text("\n".join(lines) + "\n")
print("\n".join(lines))
sys.exit(1 if nf else 0)

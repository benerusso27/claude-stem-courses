"""Re-solve the handout's questions from scratch and compare with the instructor key.

    python3 tests/solve_from_scratch.py      (from lab03_torsion/)

Independent of src/lab03_analysis.py: plain csv + numpy, the handout's equations typed in again, and
deliberately different estimators where one exists (G from a fit through the origin of the same window;
tau_Y from a brute-force grid scan instead of a bounded minimizer; the permanent twist read where the
unloading branch crosses zero torque by linear interpolation; Nadai by central differences on a smoothed
curve instead of local log-log fits). Compares with the numbers printed in the key (src/key_values.json).
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
PI, DEG = math.pi, math.pi / 180


def num(s, i=0):
    return float(re.findall(r"-?\d[\d ]*\.?\d*", s.replace("−", "-"))[i].replace(" ", ""))


def cmp(name, mine, key, tol):
    rel = abs(mine - key) / max(abs(key), 1e-12)
    out.append((name, mine, key, rel, tol, rel <= tol))


def col(sp, c):
    return np.array([float(r[c]) if r[c].strip() else np.nan for r in rows if r["specimen"] == sp])


# ---------------- pre-lab ----------------
c = 6.35e-3 / 2
J = PI * c ** 4 / 2
tY = 297 / math.sqrt(3) * 1e6
G = 205e9 / 2.58
cmp("P1 steel T_Y (N·m)", tY * J / c, num(KV["P1_TY_s"]), 2e-3)
cmp("P1 steel φ_Y over 50.8 mm (°)", tY * 50.8e-3 / (G * c) / DEG, num(KV["P1_phiY_s"]), 1e-3)
cmp("P1 torque bound (2π/3)c³·430 MPa (N·m)", 2 * PI / 3 * c ** 3 * 430e6, num(KV["P1_Tmax"]), 2e-3)
cmp("P1 cast iron fracture torque σ_UT J/c (N·m)", 214e6 * J / c, num(KV["P1_Tci"]), 1e-3)
k = 0.6
Tp = 2 * PI / 3 * (1 - k ** 3)          # per unit tau_Y c^3
TY = PI * (1 - k ** 4) / 2
cmp("P2 hollow T_p/T_Y for c_i/c = 0.6 (direct integration)", Tp / TY, num(KV["P2_hollow"]), 1e-4)
rY = 1 / 3
T3 = 2 * PI / 3 * (1 - rY ** 3 / 4) / (PI / 2)   # T/T_Y at 3 phi_Y
cmp("P3 T_max/T_Y at 3φ_Y", T3, num(KV["P3_Tm"]), 1e-4)
cmp("P3 permanent twist φ_p/φ_Y", 3 - T3, num(KV["P3_phip"]), 1e-4)
cmp("P3 residual at ρ_Y (fraction of τ_Y)", 1 - T3 * rY, num(KV["P3_res_rY"]), 1e-4)
cmp("handout §2.1 worked example τ_max (MPa)", 100e3 * 10 / (PI * 10 ** 4 / 2), 63.7, 1e-3)
cmp("handout §2.1 worked example φ (°)", 100e3 * 800 / (PI * 10 ** 4 / 2 * 79.5e3) / DEG, 3.67, 2e-3)
cmp("handout §2.2 T at 2φ_Y = (4/3)(1 − 1/32) T_Y", 4 / 3 * (1 - 1 / 32), 1.292, 1e-3)

# ---------------- analysis ----------------
Lg, Lr = meas["L_gage_mm"] * 1e-3, meas["L_reduced_mm"] * 1e-3
res = {}
for sp, kk in (("steel", "s"), ("al", "a")):
    d = np.mean(meas["d_mm"][sp]) * 1e-3
    c = d / 2
    J = PI * c ** 4 / 2
    T, tr, hd = col(sp, "torque_Nm"), col(sp, "troptometer_deg") * DEG, col(sp, "head_deg") * DEG
    n_up = int(np.argmax(np.diff(np.nan_to_num(tr, nan=1e9)) < 0)) + 1 if sp == "steel" else int(np.nanargmax(tr)) + 1
    idx = np.arange(len(T))
    w = (idx < n_up) & (T > 0.3) & (T < 4.0)
    k_fit = np.polyfit(tr[w], T[w], 1)[0]
    G = k_fit * Lg / J
    cmp(f"[{kk}] A1 G (GPa)", G / 1e9, num(KV[f"G_{kk}"]), 1e-3)
    k0 = np.sum(tr[w] * T[w]) / np.sum(tr[w] ** 2)
    cmp(f"[{kk}] A1 G, fit through the origin instead (GPa)", k0 * Lg / J / 1e9, num(KV[f"G_{kk}"]), 3e-3)
    th = tr / Lg
    fit = (idx < n_up) & ~np.isnan(tr) & (th > 0.5 * 0.002 / c)
    grid = np.arange(100e6, 250e6, 0.01e6)
    thY = grid[:, None] / (G * c)
    Tm = np.where(th[fit][None, :] <= thY, grid[:, None] * PI * c ** 3 / 2 * th[fit][None, :] / thY,
                  4 / 3 * grid[:, None] * PI * c ** 3 / 2 * (1 - (thY / th[fit][None, :]) ** 3 / 4))
    sse = np.sum((T[fit][None, :] - Tm) ** 2, axis=1)
    tYs = grid[int(np.argmin(sse))]
    cmp(f"[{kk}] A2 τ_Y by grid scan (MPa)", tYs / 1e6, num(KV[f"tY_{kk}"]), 5e-4)
    cmp(f"[{kk}] A2 T_Y = τ_Y J/c (N·m)", tYs * J / c, num(KV[f"TY_{kk}"]), 5e-4)
    # compliance and fracture strain
    cm = (idx < n_up) & ~np.isnan(tr) & (T > 1.5) & (th < tYs / (G * c))
    Cm, toe = np.polyfit(T[cm], hd[cm] - Lr / Lg * tr[cm], 1)
    cmp(f"[{kk}] A4 C_m (°/N·m)", Cm / DEG, num(KV[f"Cm_{kk}"]), 2e-3)
    last = len(T) - 2
    gf = c * (hd[last] - Cm * T[last] - toe) / Lr
    cmp(f"[{kk}] A4 γ_f", gf, num(KV[f"gf_{kk}"]), 1e-3)
    TU = np.max(T)
    cmp(f"[{kk}] A5 R_T = T_U c/J (MPa)", TU * c / J / 1e6, num(KV[f"RT_{kk}"]), 2e-3)
    cmp(f"[{kk}] A5 fully plastic estimate (MPa)", 3 * TU / (2 * PI * c ** 3) / 1e6, num(KV[f"tpl_{kk}"]), 2e-3)
    # X3 plastic work by the trapezoid rule on the corrected twist of the reduced section
    phr = (hd[: last + 1] - Cm * T[: last + 1] - toe)
    W = float(np.sum(0.5 * (T[1: last + 1] + T[:last]) * np.diff(phr)))
    cmp(f"[{kk}] X3 plastic work (J)", W, num(KV[f"W_{kk}"]), 3e-3)
    res[sp] = dict(c=c, J=J, G=G, tY=tYs, T=T, tr=tr, hd=hd, Cm=Cm, toe=toe, last=last)
    if sp == "steel":
        iu = n_up - 1
        dn = np.arange(iu, len(T))
        j = dn[int(np.argmax(T[dn] < 0.25))]          # first sample below 0.25 N·m on the unloading branch
        # linear interpolation of the unloading line to T = 0 from the last two points above 0.25 N·m
        p = np.polyfit(T[j - 3:j], tr[j - 3:j], 1)
        cmp("[s] A3 permanent twist by extrapolating the unloading line to T = 0 (°; tolerance = 2 troptometer steps)", np.polyval(p, 0) / DEG, num(KV["phires_m"]), 0.02 / 3.29)
        cmp("[s] A3 predicted permanent twist φ_A − T_A L/(JG) (°)", (tr[iu] - T[iu] * Lg / (J * G)) / DEG, num(KV["phires_p"]), 2e-3)
        cmp("[s] A3 residual stress at the surface (MPa)", (tYs - T[iu] * c / J) / 1e6, num(KV["res_c"]), 3e-3)
        # Nadai at gamma = 0.5 by central differences of a moving-average-smoothed curve
        g = c * (hd - Cm * T - toe) / Lr
        sel = (np.arange(len(T)) <= last) & (g > 0.02)
        gs, Ts = g[sel], T[sel]
        o = np.argsort(gs)
        gs, Ts = gs[o], np.convolve(Ts[o], np.ones(9) / 9, mode="same")
        i5 = int(np.argmin(abs(gs - 0.5)))
        dTdg = (Ts[i5 + 6] - Ts[i5 - 6]) / (gs[i5 + 6] - gs[i5 - 6])
        cmp("[s] C1 Nadai τ at γ = 0.5 by central differences (MPa)", (3 * Ts[i5] + gs[i5] * dTdg) / (2 * PI * c ** 3) / 1e6,
            float(re.search(r"γ = 0.5: Nadai (\d+)", KV["nadai_rows"]).group(1)), 5e-3)
# cast iron
d = np.mean(meas["d_mm"]["ci"]) * 1e-3
c = d / 2
J = PI * c ** 4 / 2
Tci = col("ci", "torque_Nm")
cmp("[ci] A5 R_T (MPa)", np.max(Tci) * c / J / 1e6, num(KV["RT_ci"]), 1e-3)
# M1 square and X2 composite shaft
cmp("M1(c) circular formula on a 10 mm square: T(a/√2)/(a⁴/6) vs T/(0.2082 a³) (relative)", (math.sqrt(2) / 2 * 6) * 0.2082 - 1, num(KV["sq_pct"]) / 100, 5e-3)
Gs, Ga = res["steel"]["G"], res["al"]["G"]
Js, Ja = PI * 0.01 ** 4 / 2, PI * (0.015 ** 4 - 0.01 ** 4) / 2
cmp("X2 core share of torque", Js * Gs / (Js * Gs + Ja * Ga), num(KV["X2_share"]), 1e-3)
th1 = min(res["steel"]["tY"] / (Gs * 0.01), res["al"]["tY"] / (Ga * 0.015))
cmp("X2 torque at first yield (N·m)", th1 * (Js * Gs + Ja * Ga), num(KV["X2_T"]), 2e-3)
# D1: march diameters in whole mm for the steel tube d_i/d = 0.8
T = 15e3 / (2 * PI * 1200 / 60)
cmp("D1 torque (N·m)", T, num(KV["D_T"]), 1e-3)
tall = (res["steel"]["tY"] - 2 * 0.52e6) / 3.2
dd = 10
while True:
    Jd = PI * (dd * 1e-3) ** 4 * (1 - 0.8 ** 4) / 32
    if 1.6 * T * dd * 1e-3 / 2 / Jd <= tall and T * 1.5 / (Jd * Gs) <= 1.0 * DEG:
        break
    dd += 1
cmp("D1 smallest whole-mm steel tube (d_i/d = 0.8) by marching (mm)", dd, num(KV["D_s8_d"]), 1e-9)

lines = ["## Lab 3 — handout questions re-solved from scratch vs. the instructor key", "",
         "| Question / quantity | From scratch | Key | Rel. difference | Tolerance | Result |", "|---|---:|---:|---:|---:|---|"]
for name, a, b, rel, tol, okk in out:
    lines.append(f"| {name} | {a:.6g} | {b:.6g} | {rel:.1e} | {tol:.0e} | {'PASS' if okk else '**FAIL**'} |")
nf = sum(not o[-1] for o in out)
lines += ["", f"{len(out) - nf} of {len(out)} agree.",
          "Tolerances: about 1e-3 where the key prints a rounded value of the same quantity; up to 5e-3 where a different "
          "estimator is used on purpose (fit through the origin, grid scan, extrapolated unloading line, central differences)."]
(Path(__file__).parent / "results_from_scratch.md").write_text("\n".join(lines) + "\n")
print("\n".join(lines))
sys.exit(1 if nf else 0)

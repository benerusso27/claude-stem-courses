"""Re-solve the handout's questions from scratch and compare with the instructor key.

    python3 tests/solve_from_scratch.py      (from lab01_stress_strain/)

Independent of src/lab01_analysis.py: plain numpy (polyfit, interp, trapezoid), a different
peak estimate (moving average instead of a parabola), and the handout's own equations typed
in again. Compares with src/results.json and src/key_values.json (what the key prints).
"""
import csv
import json
import math
import sys
from pathlib import Path

import numpy as np

LAB = Path(__file__).resolve().parents[1]
res = json.loads((LAB / "src" / "results.json").read_text())
meas = json.loads((LAB / "src" / "specimen_measurements.json").read_text())
rows = list(csv.DictReader(open(LAB / "sample_data.csv", newline="")))
out = []


def cmp(name, mine, key, tol):
    rel = abs(mine - key) / max(abs(key), 1e-12)
    out.append((name, mine, key, rel, tol, rel <= tol))


# ---------------- pre-lab (handout equations, typed again) ----------------
A0n = math.pi * 10.0 ** 2 / 4
cmp("P1 steel P_U at 440 MPa (kN)", 440 * A0n / 1000, 34.56, 1e-3)
cmp("P1 steel gage elongation at yield, 295 MPa (mm)", 295 / 205000 * 50, 0.0720, 1e-3)
cmp("P1 criterion r ≤ √12·0.001·Δδw, steel (µm)", math.sqrt(12) * 0.001 * (135 / 205000 * 50) * 1000, 0.114, 5e-3)
x = 0.0201
cmp("P2 ln(1+ε)/ε = 0.99 near ε = 2.01 %", math.log1p(x) / x, 0.99, 1e-4)
k = A0n * 0.008 / 60
cmp("P3 E_app steel (GPa)", 1 / (1 / 205 + k), 65.15, 1e-3)
cmp("P3 E_app aluminum (GPa)", 1 / (1 / 68.9 + k), 40.02, 1e-3)
cmp("P4 εu for n = 0.20", math.exp(0.2) - 1, 0.2214, 1e-3)
cmp("P4 Δεt,u = 0.88·√(2·0.2·0.003)", 0.88 * math.sqrt(2 * 0.2 * 0.003), 0.0305, 2e-3)
cmp("P6 σb/σ = 8e/d for e = 0.1 mm", 8 * 0.1 / 10, 0.08, 1e-9)

# ---------------- analysis from the CSV ----------------
for key, short in (("steel_1018HR", "s"), ("al_6061T6", "a")):
    r = res[key]
    m = meas[key]
    d = [x for x in rows if x["specimen"] == key]
    P = np.array([float(x["load_N"]) for x in d])
    xh = np.array([float(x["crosshead_mm"]) for x in d])
    ext = np.array([float(x["extensometer_mm"]) if x["extensometer_mm"] else np.nan for x in d])
    d0 = float(np.mean(m["d0_readings_mm"]))
    A0 = math.pi * d0 ** 2 / 4
    cmp(f"[{short}] A0 (mm²)", A0, r["A0"], 1e-9)
    s = P / A0
    e = ext / 50.0
    ok = ~np.isnan(e)
    # initial loading branch: indices before the stress first exceeds 189 MPa
    n1 = int(np.argmax(s > 189))
    win = ok & (np.arange(len(s)) < n1) & (s >= 45) & (s <= 180)
    E = np.polyfit(e[win], s[win], 1)[0] / 1000
    cmp(f"[{short}] A2 E (GPa)", E, r["E"], 1e-6)
    # 0.2 % offset, linear interpolation at the first sign change
    g = s - E * 1000 * (e - 0.002)
    j = [i for i in range(len(g) - 1) if ok[i] and ok[i + 1] and e[i] > 0.001 and g[i] > 0 >= g[i + 1]][0]
    sy = s[j] + g[j] / (g[j] - g[j + 1]) * (s[j + 1] - s[j])
    cmp(f"[{short}] A3 0.2 % offset σY (MPa)", sy, r["sig_offset"], 1e-6)
    if short == "s":
        early = ok & (e < 0.004)
        cmp("[s] A3 upper yield point (MPa)", float(np.max(s[early])), r["sig_uy"], 1e-9)
        plat = ok & (e > 0.005) & (e < 0.017)
        cmp("[s] A3 lower yield point, plateau mean (MPa)", float(np.mean(s[plat])), r["sig_ly"], 2e-3)
    # sigma_U: 21-point moving average maximum (different estimator from the key's parabola)
    ma = np.convolve(P, np.ones(21) / 21, mode="valid")
    cmp(f"[{short}] A5 σU (MPa)", float(ma.max()) / A0, r["sigU"], 2e-3)
    # compliance, Eq. 9
    ov = ok & (P > 3000) & (np.arange(len(P)) < n1)
    Cm, toe = np.polyfit(P[ov] / 1000, xh[ov] - 60 / 50 * ext[ov], 1)
    cmp(f"[{short}] A4 Cm (mm/kN)", Cm, r["Cm"], 1e-6)
    wa = (np.arange(len(s)) < n1) & (s >= 45) & (s <= 180)
    Eapp = np.polyfit(xh[wa] / 60, s[wa], 1)[0] / 1000
    cmp(f"[{short}] A4 E_app from crosshead (GPa)", Eapp, r["E_app"], 1e-6)
    cmp(f"[{short}] A4 Eq. 8 prediction (GPa)", 1 / (1 / E + A0 * Cm / 60), r["E_app_pred"], 1e-6)
    ech = (xh - Cm * P / 1000 - toe) / 60
    eall = np.where(ok, e, ech)
    imax = int(np.argmax(P))
    cmp(f"[{short}] A5 εu (strain at the largest load sample)", float(eall[imax]), r["e_u"], 1e-9)
    pre = np.arange(len(P)) <= imax
    st_, et_ = s * (1 + eall), np.log1p(eall)
    lo = 0.03 if short == "s" else 0.01
    fm = pre & (et_ > lo) & (et_ < math.log1p(eall[imax]) * 0.97)
    n_fit = np.polyfit(np.log(et_[fm]), np.log(st_[fm]), 1)[0]
    cmp(f"[{short}] A6 Hollomon n", n_fit, r["n_hollomon"], 1e-6)
    cmp(f"[{short}] A7 energy to max load, engineering = true (MJ/m³)", float(np.trapezoid(s[pre], eall[pre])), float(np.trapezoid(st_[pre], et_[pre])), 1e-3)
    EL = (m["Lf_mm"] - m["L0_mm"]) / m["L0_mm"] * 100
    cmp(f"[{short}] A7 %EL", EL, r["EL"], 1e-9)
    df = float(np.mean(m["df_readings_mm"]))
    RA = (1 - (df / d0) ** 2) * 100
    cmp(f"[{short}] A7 %RA", RA, r["RA"], 1e-9)
    cmp(f"[{short}] A7 modulus of resilience σY²/2E (MJ/m³)", (r["sigY"]) ** 2 / (2 * E * 1000), r["u_res"], 1e-6)
    i_f = int(np.where(P > 0.2 * P.max())[0][-1])
    cmp(f"[{short}] M1 σf(1+εf) (MPa)", P[i_f] / A0 * (1 + EL / 100), r["sig_t_formula_f"], 1e-9)
    cmp(f"[{short}] M1 Pf/Af (MPa)", P[i_f] / (math.pi * df ** 2 / 4), r["sig_t_neck_f"], 1e-9)

# ---------------- design problem ----------------
for key, short, rho in (("steel_1018HR", "s", 7870), ("al_6061T6", "a", 2700)):
    r = res[key]
    sig_lo = r["sigY"] - 2 * r["uY"]
    A_req = max(2.0 * 12000 / (0.78 * sig_lo), 18000 / (0.78 * sig_lo), 12000 * 1800 / (r["E"] * 1000 * 1.20))
    dmin = math.sqrt(4 * A_req / math.pi)
    cmp(f"[{short}] D1 minimum diameter (mm)", dmin, res["_design"][key]["d_req"], 1e-9)
    dd = math.ceil(dmin)
    cmp(f"[{short}] D1 mass at d = {dd} mm (kg)", math.pi * dd ** 2 / 4 * 1e-6 * 1.80 * rho, res["_design"][key]["mass"], 1e-9)

lines = ["## Lab 1 — handout questions re-solved from scratch vs. the instructor key", "",
         "| Question / quantity | From scratch | Key | Rel. difference | Tolerance | Result |", "|---|---:|---:|---:|---:|---|"]
for name, a, b, rel, tol, okk in out:
    lines.append(f"| {name} | {a:.6g} | {b:.6g} | {rel:.1e} | {tol:.0e} | {'PASS' if okk else '**FAIL**'} |")
nf = sum(not o[-1] for o in out)
lines += ["", f"{len(out) - nf} of {len(out)} agree.",
          "Tolerances: 1e-9 where the same definition is recomputed; 1e-3 to 2e-3 where a different estimator is used on purpose "
          "(moving-average peak vs. parabola; plateau limits)."]
(Path(__file__).parent / "results_from_scratch.md").write_text("\n".join(lines) + "\n")
print("\n".join(lines))
sys.exit(1 if nf else 0)

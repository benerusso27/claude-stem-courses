"""Re-solve the handout's questions from scratch and compare with the instructor key.

    python3 tests/solve_from_scratch.py      (from lab08_transformation/)

Independent of src/lab08_analysis.py and src/lab08_model.py: plain csv + numpy/scipy, the handout's equations typed in
again, and deliberately different methods where one exists: E, nu and the rosette angle at H fitted all at once by
nonlinear least squares on every Part A reading (instead of slopes, then Eq. 6, then turning back); G and the
principal stresses from the invariants of the strain state (Mohr's circle radius and center, which do not depend on
how the rosette was turned) instead of turning the strains back; principal stresses of the D1 tubes from the roots of
the characteristic cubic (numpy.roots) instead of an eigen-solver. Compares with the numbers printed in the key
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
ref = meas["reference"]
E2, nu2 = ref["E_al_GPa"] * 1e9, ref["nu_al"]
Kt, nu0 = meas["rosette"]["Kt"], meas["rosette"]["nu0"]
out = []


def num(s, i=0):
    return float(re.findall(r"-?\d[\d ]*\.?\d*", s.replace("−", "-"))[i].replace(" ", ""))


def cmp(name, mine, key, tol):
    rel = abs(mine - key) / max(abs(key), 1e-12)
    out.append((name, mine, key, rel, tol, rel <= tol))


def get(part, config):
    return [r for r in rows if r["part"] == part and r["config"] == config]


def eps(th, ex, ey, g):
    return ex * math.cos(th) ** 2 + ey * math.sin(th) ** 2 + g * math.sin(th) * math.cos(th)


def indicated(ex, ey, g, th):
    return (eps(th, ex, ey, g) + Kt * eps(th + math.pi / 2, ex, ey, g)) / (1 - nu0 * Kt)


ANG = [0.0, math.pi / 4, math.pi / 2]
Do = np.mean(meas["tube"]["Do_mm"]) * 1e-3
tw = np.mean(meas["tube"]["t_mm"]) * 1e-3
ro, ri = Do / 2, Do / 2 - tw
I = math.pi * (ro ** 4 - ri ** 4) / 4
J = 2 * I
Lb, aL = meas["tube"]["Lb_mm"] * 1e-3, meas["tube"]["aL_mm"] * 1e-3

# ---------------- P1 (nominal) ----------------
ron, rin = 19.05e-3, 15.875e-3
In = math.pi * (ron ** 4 - rin ** 4) / 4
sx, t = 600 * 0.25 * ron / In, -600 * 0.2 * ron / (2 * In)
R = math.hypot(sx / 2, t)
cmp("P1(a) σmax at H (MPa)", (sx / 2 + R) / 1e6, num(KV["P1_s1"]), 1e-3)
cmp("P1(a) θp at H (°)", math.degrees(0.5 * math.atan2(t, sx / 2)), num(KV["P1_th"]), 1e-3)
cmp("P1(b) τxy at K (MPa)", -(600 * 0.2 * ron / (2 * In) + 600 * (2 / 3) * (ron ** 3 - rin ** 3) / (In * 2 * (ron - rin))) / 1e6, num(KV["P1_tK"]), 1e-3)
cmp("P1(d) Lamé hoop stress at 8 MPa (MPa)", 2 * 8 * rin ** 2 / (ron ** 2 - rin ** 2), num(KV["P1_th_lame"]), 1e-3)
sxp = sx + 8e6 * rin ** 2 / (ron ** 2 - rin ** 2)
syp = 2 * 8e6 * rin ** 2 / (ron ** 2 - rin ** 2)
Rp = math.hypot((sxp - syp) / 2, t)
cmp("P4 absolute τmax at H, 8 MPa + lever (MPa)", ((sxp + syp) / 2 + Rp) / 2 / 1e6, num(KV["P4_tabs"]), 1e-3)

# ---------------- A1: nonlinear least squares on all Part A readings at H ----------------
ra = get("A", "axis")
F = np.array([float(r["load_N"]) for r in ra])
Y = np.array([[float(r[f"H{c}_ue"]) for c in "abc"] for r in ra]) * 1e-6


def resA(v):
    exN, nu, beta, *z = v                                          # strain per newton along x; zero offsets per gage
    res = []
    for k, Fk in enumerate(F):
        ex = exN * Fk
        for i, th in enumerate(ANG):
            res.append(indicated(ex, -nu * ex, 0.0, th + beta) + z[i] - Y[k, i])
    return np.array(res) * 1e6


sol = optimize.least_squares(resA, [1.3e-6, 0.3, 0.01, 0, 0, 0], x_scale=[1e-6, 0.1, 0.01, 1e-6, 1e-6, 1e-6])
exN, nu_fit, beta_fit = sol.x[:3]
sigN = Lb * ro / I
cmp("A1 E by one nonlinear fit of all 21 Part A readings at H (GPa)", sigN / exN / 1e9, num(KV["E_A"]), 2e-3)
cmp("A1 ν by the same fit", nu_fit, num(KV["nu_A"]), 5e-3)
cmp("A1 β_H by the same fit (°)", math.degrees(beta_fit), num(KV["bH"]), 2e-2)


# ---------------- strain-state slopes, corrected for K_t by solving the 3x3 model ----------------
def slopes(part, cfg, g, xcol):
    rr = get(part, cfg)
    x = np.array([float(r[xcol]) for r in rr]) * (1e6 if xcol == "p_MPa" else 1.0)
    y = np.array([[float(r[f"{g}{c}_ue"]) for c in "abc"] for r in rr]) * 1e-6
    s = np.polyfit(x, y, 1)[0]
    A = np.array([[(math.cos(th) ** 2 + Kt * math.sin(th) ** 2), (math.sin(th) ** 2 + Kt * math.cos(th) ** 2), (1 - Kt) * math.sin(th) * math.cos(th)] for th in ANG]) / (1 - nu0 * Kt)
    return np.linalg.solve(A, s)                                   # ex, ey, g on the rosette's own axes


def mohr(ex, ey, g):
    return (ex + ey) / 2, math.hypot((ex - ey) / 2, g / 2)


# ---------------- A2: G from the radius of the torsion-only strain circle (independent of the rosette's turn) ----------------
G = []
for g in "HK":
    d = slopes("B", "lever", g, "load_N") - slopes("A", "axis", g, "load_N")
    _, Re = mohr(*d)
    G.append((aL * ro / J) / (2 * Re))
cmp("A2 G at H from the strain-circle radius (GPa)", G[0] / 1e9, num(KV["G_H"]), 2e-3)
cmp("A2 G at K from the strain-circle radius (GPa)", G[1] / 1e9, num(KV["G_K"]), 2e-3)


# ---------------- A3: principal stresses from principal strains (invariants) ----------------
def principal_stress(ex, ey, g):
    c, Re = mohr(ex, ey, g)
    e1, e2 = c + Re, c - Re
    k = E2 / (1 - nu2 ** 2)
    return k * (e1 + nu2 * e2), k * (e2 + nu2 * e1)


for g in "HK":
    s = slopes("B", "lever", g, "load_N") * 600
    s1, s2 = principal_stress(*s)
    cmp(f"A3 σmax at {g}, Part B, from principal strains (MPa)", s1 / 1e6, num(KV[f"B{g}_s1"]), 2e-3)
    cmp(f"A3 σmin at {g}, Part B, from principal strains (MPa)", s2 / 1e6, num(KV[f"B{g}_s2"]), 4e-3)
s = slopes("B", "lever", "H", "load_N")
thp_raw = 0.5 * math.atan2(s[2] / 2, (s[0] - s[1]) / 2)
cmp("A3 θp at H = angle on the rosette's axes + β_H from A1 (°)", math.degrees(thp_raw + beta_fit), num(KV["BH_th"]), 2e-2)

# ---------------- A4: pressure, from the principal strains ----------------
nus, sth = [], []
for g in "HK":
    s = slopes("C", "pressure", g, "p_MPa")
    c, Re = mohr(*s)
    e_hoop, e_ax = c + Re, c - Re
    r = e_ax / e_hoop
    nus.append((1 - 2 * r) / (2 - r))
    sth.append(E2 / (1 - nu2 ** 2) * (e_hoop + nu2 * e_ax) * 1e6)
cmp("A4 ν from the ratio of the principal strains under pressure", np.mean(nus), num(KV["C_nu"]), 3e-3)
cmp("A4 hoop stress per MPa (MPa/MPa)", np.mean(sth) / 1e6, num(KV["C_sth"]), 2e-3)

# ---------------- A5: Part C with the lever at H, from principal strains ----------------
for g in "HK":
    sp = slopes("C", "pressure", g, "p_MPa") * 8e6 + slopes("C", "combined", g, "load_N") * 600
    s1, s2 = principal_stress(*sp)
    cmp(f"A5 σmax at {g}, 8 MPa + 600 N (MPa)", s1 / 1e6, num(KV[f"X{g}_s1"]), 2e-3)
    if g == "H":
        cmp("A5 absolute τmax at H = σmax/2 (MPa)", s1 / 2 / 1e6, num(KV["XH_tabs"]), 2e-3)
        cmp("A5 in-plane τmax at H (MPa)", (s1 - s2) / 2 / 1e6, num(KV["XH_R"]), 2e-3)

# ---------------- D1: roots of the characteristic cubic ----------------
cat = [(31.75, 3.18), (31.75, 4.78), (38.1, 2.11), (38.1, 3.18), (38.1, 4.78), (44.45, 2.11), (44.45, 3.18), (44.45, 4.78), (50.8, 2.11), (50.8, 3.18), (50.8, 4.78)]
sY, G3 = ref["sY_al_MPa"] * 1e6, ref["G_al_GPa"] * 1e9
res = []
for OD, w in cat:
    ro_, ri_ = OD / 2e3, OD / 2e3 - w / 1e3
    I_ = math.pi * (ro_ ** 4 - ri_ ** 4) / 4
    A_ = 20e6 * ri_ ** 2 / (ro_ ** 2 - ri_ ** 2)
    worst = 0.0
    for r_ in (ro_, ri_):
        for sg in (1, -1):
            S = np.array([[A_ + sg * 300 * r_ / I_, 300 * r_ / (2 * I_), 0], [300 * r_ / (2 * I_), A_ + A_ * ro_ ** 2 / r_ ** 2, 0], [0, 0, A_ - A_ * ro_ ** 2 / r_ ** 2]])
            I1, I2, I3 = np.trace(S), 0.5 * (np.trace(S) ** 2 - np.trace(S @ S)), np.linalg.det(S)
            pr = np.sort(np.real(np.roots([1, -I1, I2, -I3])))
            worst = max(worst, (pr[-1] - pr[0]) / 2)
    twist = math.degrees(300 / (G3 * 2 * I_))
    res.append((f"{OD} × {w}", math.pi * (ro_ ** 2 - ri_ ** 2) * 2700, sY / (2 * worst), twist))
ok = sorted([x for x in res if x[2] >= 1.8 and x[3] <= 3.0], key=lambda x: x[1])
out.append(("D1 lightest tube (name match)", 1.0 if ok[0][0] == KV["D_best"] else 0.0, 1.0, 0.0 if ok[0][0] == KV["D_best"] else 1.0, 0, ok[0][0] == KV["D_best"]))
cmp("D1 Tresca factor of the reference tube", ok[0][2], num(KV["D_sf"]), 3e-3)
cmp("D1 twist of the reference tube (°/m)", ok[0][3], num(KV["D_tw"]), 3e-3)

lines = ["## Lab 8 — handout questions re-solved from scratch vs. the instructor key", "",
         "| Question / quantity | From scratch | Key | Rel. difference | Tolerance | Result |", "|---|---:|---:|---:|---:|---|"]
for name, a_, b_, rel, tol, okk in out:
    lines.append(f"| {name} | {a_:.6g} | {b_:.6g} | {rel:.1e} | {tol:.0e} | {'PASS' if okk else '**FAIL**'} |")
nf = sum(not o[-1] for o in out)
lines += ["", f"{len(out) - nf} of {len(out)} agree.",
          "Tolerances: about 1e-3 where the key prints a rounded value of the same quantity; 2e-3 to 5e-3 where a different "
          "estimator is used on purpose (one nonlinear fit of all readings instead of slopes; invariants instead of turning back); "
          "2e-2 for the angles, which the key rounds to 0.01° on values near 1°."]
(Path(__file__).parent / "results_from_scratch.md").write_text("\n".join(lines) + "\n")
print("\n".join(lines))
sys.exit(1 if nf else 0)

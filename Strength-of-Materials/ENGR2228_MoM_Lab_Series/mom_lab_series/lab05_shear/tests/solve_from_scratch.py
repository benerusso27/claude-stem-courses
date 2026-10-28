"""Re-solve the handout's questions from scratch and compare with the instructor key.

    python3 tests/solve_from_scratch.py      (from lab05_shear/)

Independent of src/lab05_analysis.py and src/lab05_model.py: plain csv + numpy/scipy, the handout's equations typed
in again, and deliberately different methods where one exists: section integrals on a fine strip grid; the wide-
rectangle factor R from a 2-D finite-difference solve with Richardson extrapolation; E and G from one nonlinear fit of
all (P, L, delta) points instead of per-span slopes; the bolted beam as a linear system for the bolt forces instead of
shooting. Compares with the numbers printed in the key (src/key_values.json).
"""
import csv
import json
import math
import re
import sys
from pathlib import Path

import numpy as np
from scipy import optimize, sparse
from scipy.sparse.linalg import spsolve

LAB = Path(__file__).resolve().parents[1]
KV = json.loads((LAB / "src" / "key_values.json").read_text())
meas = json.loads((LAB / "src" / "specimen_measurements.json").read_text())
rows = list(csv.DictReader(open(LAB / "sample_data.csv", newline="")))
ref = meas["reference"]
E, G, nu = ref["E_al_GPa"] * 1e3, ref["G_al_GPa"] * 1e3, ref["nu_al"]       # MPa
out = []


def num(s, i=0):
    return float(re.findall(r"-?\d[\d ]*\.?\d*", s.replace("−", "-"))[i].replace(" ", ""))


def cmp(name, mine, key, tol):
    rel = abs(mine - key) / max(abs(key), 1e-12)
    out.append((name, mine, key, rel, tol, rel <= tol))


def get(part, config, span=None):
    rr = [r for r in rows if r["part"] == part and r["config"] == config and (span is None or abs(float(r["span_mm"]) - span) < 1e-6)]
    P = np.array([float(r["load_N"]) for r in rr])
    imax = int(np.argmax(P))
    return [r for r in rr[: imax + 1] if float(r["load_N"]) > 100]


def fl(r, c):
    return float(r[c])


def strip_section(widths, H, n=200000):
    """widths(y) on y in [0, H]; returns A, ybar, I, and functions Q(y), t(y) on the grid (fine midpoint strips)."""
    y = (np.arange(n) + 0.5) * H / n
    t = widths(y)
    dA = t * H / n
    A = dA.sum()
    yb = (y * dA).sum() / A
    I = ((y - yb) ** 2 * dA).sum()
    Qcum = np.cumsum(((y - yb) * dA)[::-1])[::-1]       # first moment of the area above each strip (inclusive)
    return A, yb, I, y, t, Qcum


# ---------------- worked example and pre-lab ----------------
cmp("§2.1 example: τ_max of a 30 × 90 mm rectangle at V = 12 kN (MPa)", 1.5 * 12000 / 2700, 6.67, 1e-3)
cmp("§2.1 example: τ at 22.5 mm above the NA (MPa)", 1.5 * 12000 / 2700 * (1 - 0.25), 5.00, 1e-3)
A = 25.4 * 50.8
cmp("P1(a) τ = 3V/2A at V = 7.5 kN (MPa)", 1.5 * 7500 / A, num(KV["P1_tau"]), 1e-3)
cmp("P1(a) largest bending stress PL/4 ÷ bh²/6 (MPa)", 15000 * 400 / 4 / (25.4 * 50.8 ** 2 / 6), num(KV["P1_sig"]), 1e-3)
Bn, Hn, tfn, twn = 76.2, 101.6, 6.35, 4.76
wI = lambda y: np.where((y < tfn) | (y > Hn - tfn), Bn, twn)  # noqa: E731
AI, ybI, II, yI, tI, QI = strip_section(wI, Hn)
cmp("P2 I-beam I by fine strips (10⁶ mm⁴)", II / 1e6, num(KV["P2_I"]), 1e-4)
iNA = int(np.argmin(abs(yI - ybI)))
cmp("P2(a) τ at the NA = VQ/(It_w), strips (MPa)", 10000 * QI[iNA] / (II * twn), num(KV["P2_tNA"]), 2e-4)
ij = int(np.argmin(abs(yI - (Hn - tfn - 1e-4))))
cmp("P2(b) τ in the web at the junction (MPa)", 10000 * QI[ij] / (II * twn), num(KV["P2_tj"]), 1e-3)
cmp("P1(b)/P2 τ ≈ V/A_w (MPa)", 10000 / ((Hn - 2 * tfn) * twn), num(KV["P1_tweb"]), 1e-3)
fsA = AI / ((Hn - 2 * tfn) * twn)
for L in (300, 1200):
    db = 10000 * L ** 3 / (48 * E * II)
    ds = fsA * 10000 * L / (4 * G * AI)
    cmp(f"P1(c) bending part at {L} mm (mm)", db, num(KV[f"P1c_b{L}"]), 2e-3)
    cmp(f"P1(c) shear part at {L} mm (mm)", ds, num(KV[f"P1c_s{L}"]), 2e-3)
bc, tc, Lc = 50.8, 12.7, 600.0
EI0 = E * 2 * bc * tc ** 3 / 12
cmp("P1(d) loose deflection at 2 kN (mm)", 2000 * Lc ** 3 / (48 * EI0), num(KV["P1d_loose"]), 2e-3)
cmp("P1(d) loose end slip r θ_end at 2 kN (mm)", tc * 2000 * Lc ** 2 / (16 * EI0), num(KV["P1d_slip"]), 2e-3)
Q2 = bc * tc * (tc / 2)
I2 = bc * (2 * tc) ** 3 / 12
cmp("P3 q = VQ/I at the interface, V = 1.25 kN (N/mm)", 1250 * Q2 / I2, num(KV["P3_q"]), 1e-3)

# ---------------- A1: wide rectangle ----------------
def R_fd(b, h, nu_, n):
    """Face value of τ/(VQ/Ib) on the NA by 5-point finite differences on an n × m grid (sparse direct solve)."""
    m = max(4, 2 * round(n * h / b / 2))
    hx, hy = b / n, h / m
    nx, ny = n - 1, m - 1
    ex, ey = np.ones(nx), np.ones(ny)
    Dx = sparse.diags([ex[:-1], -2 * ex, ex[:-1]], [-1, 0, 1]) / hx ** 2
    Dy = sparse.diags([ey[:-1], -2 * ey, ey[:-1]], [-1, 0, 1]) / hy ** 2
    Lap = sparse.kron(sparse.identity(ny), Dx) + sparse.kron(Dy, sparse.identity(nx))
    x = -b / 2 + hx * np.arange(1, n)
    rhs = np.tile(x, ny)
    phi = spsolve(Lap.tocsc(), rhs).reshape(ny, nx)
    row = phi[m // 2 - 1]                                    # y = 0
    dphi = (3 * 0 - 4 * row[-1] + row[-2]) / (2 * hx)       # one-sided at x = b/2 (φ = 0 there)
    c = h / 2
    return 1 + (2 / c ** 2) * (nu_ / (1 + nu_)) * dphi


bA, hA = np.mean(meas["barA"]["b_mm"]), np.mean(meas["barA"]["h_mm"])
for cfg, b, h, key in (("upright", bA, hA, "up"), ("flat", hA, bA, "fl")):
    r1, r2 = R_fd(b, h, nu, 64), R_fd(b, h, nu, 128)
    cmp(f"A1 {cfg}: R from 2-D finite differences (64/128 cells, Richardson) vs key (series)", (4 * r2 - r1) / 3, num(KV[f"A1_P_{key}"]), 2e-4)
    rr = get("A", cfg)
    V = np.array([fl(r, "load_N") / 2 for r in rr])
    g = np.array([-(fl(r, "gA_p45_ue") - fl(r, "gA_m45_ue") + fl(r, "gB_p45_ue") - fl(r, "gB_m45_ue")) / 2 * 1e-6 for r in rr])
    slope = np.polyfit(V, G * g, 1)[0]
    cmp(f"A1 {cfg}: measured R (slope of τ against V) ÷ 3/(2A)", slope / (1.5 / (bA * hA)), num(KV[f"A1_R_{key}"]), 1e-3)
    cmp(f"A1 {cfg}: R from the largest load step only (different estimator)", G * g[-1] / V[-1] / (1.5 / (bA * hA)), num(KV[f"A1_R_{key}"]), 1.5e-2)

# ---------------- A2-A4: I-beam ----------------
ib = meas["ibeam"]
Bm, Hm, tfm, twm = (np.mean(ib[k]) for k in ("B_mm", "H_mm", "tf_mm", "tw_mm"))
wM = lambda y: np.where((y < tfm) | (y > Hm - tfm), Bm, twm)  # noqa: E731
AM, ybM, IM, yM, tM, QM = strip_section(wM, Hm)
cmp("A2 I of the measured section by strips (10⁶ mm⁴)", IM / 1e6, num(KV["B_I"]), 1e-4)
rr = get("B", "web")
V = np.array([fl(r, "load_N") / 2 for r in rr])
tab = KV["A2_table"].splitlines()
for j, (g1, g2) in enumerate((("gA", "gB"), ("gC", "gD"), ("gE", "gF"))):
    gam = np.array([-(fl(r, f"{g1}_p45_ue") - fl(r, f"{g1}_m45_ue") + fl(r, f"{g2}_p45_ue") - fl(r, f"{g2}_m45_ue")) / 2 * 1e-6 for r in rr])
    sl = np.polyfit(V, G * gam, 1)[0]
    y = ib["gage_height_mm"][j]
    i = int(np.argmin(abs(yM - y)))
    cells = [c.strip() for c in tab[j].split("|")[1:-1]]
    cmp(f"A2 web gage {j + 1}: measured τ/V (10⁻³ mm⁻²)", sl * 1e3, num(cells[2]), 1e-3)
    cmp(f"A2 web gage {j + 1}: Q/(I t_w) by strips (10⁻³ mm⁻²)", QM[i] / (IM * twm) * 1e3, num(cells[3]), 2e-4)
# f_s of the measured section on the fine grid: (A/I²) ∫ Q²/t dy
fsM = AM / IM ** 2 * np.sum(QM ** 2 / tM) * Hm / len(yM)
cmp("A3 shear form factor f_s of the measured I-beam (fine strips)", fsM, num(KV["B_fs"]), 2e-4)
P_, L_, d_ = [], [], []
for L in ib["spans_mm"]:
    for r in get("B", "deflection", L):
        P_.append(fl(r, "load_N")); L_.append(L); d_.append(fl(r, "defl_mm"))
P_, L_, d_ = map(np.array, (P_, L_, d_))


def model(X, Ei, Gi):
    P, L = X
    return P * (L ** 3 / (48 * Ei * 1e3 * IM) + fsM * L / (4 * Gi * 1e3 * AM))


popt, _ = optimize.curve_fit(model, (P_, L_), d_, p0=[68, 26], sigma=np.maximum(d_, 0.01), absolute_sigma=False)
cmp("A3 E from one nonlinear fit of all (P, L, δ) points (GPa)", popt[0], num(KV["A3_E"]), 4e-3)
cmp("A3 G from the same fit (GPa)", popt[1], num(KV["A3_G"]), 1e-2)
L5 = math.sqrt(19 * fsM * 48 * popt[0] * IM / (4 * popt[1] * AM))
cmp("A4 span with a 5 % shear part from the global fit (mm)", L5, num(KV["A4_L5f"]), 1e-2)
cmp("A4 the same from Eq. 9 with Table 1 values (mm)", math.sqrt(19 * fsM * 48 * E * IM / (4 * G * AM)), num(KV["A4_L5p"]), 1e-3)

# ---------------- A5-A6: layered beams ----------------
ly = meas["layered"]
bL, t1, t2 = np.mean(ly["b_mm"]), np.mean(ly["t_top_mm"]), np.mean(ly["t_bot_mm"])
Lc = ly["span_mm"]
EI0 = E * bL * (t1 ** 3 + t2 ** 3) / 12                              # N mm²
EAs = 1 / (1 / (E * bL * t1) + 1 / (E * bL * t2))
r_ = (t1 + t2) / 2
EIf = EI0 + EAs * r_ ** 2
dsh = 1.2 * Lc / (4 * G * bL * (t1 + t2))
EI = {}
for cfg in ("loose", "bolted", "bonded"):
    rr = get("C", cfg)
    P = np.array([fl(r, "load_N") for r in rr])
    C = np.polyfit(P, [fl(r, "defl_mm") for r in rr], 1)[0]
    EI[cfg] = Lc ** 3 / (48 * (C - dsh)) / 1e6                   # N m²
    cmp(f"A5 {cfg}: EI_eff (N·m²)", EI[cfg], num(KV[f"A5_EI_{cfg}"]), 1e-3)
cmp("A5 EI₀ from Eq. 11 (N·m²)", EI0 / 1e6, num(KV["A5_EI0"]), 1e-3)
cmp("A5 EI_full from Eq. 11 (N·m²)", EIf / 1e6, num(KV["A5_EIf"]), 1e-3)
rr = get("C", "loose")
sl = np.polyfit([fl(r, "load_N") for r in rr], [fl(r, "slip_mm") for r in rr], 1)[0]
cmp("A5 loose end slip per newton (10⁻⁹ m/N)", sl * 1e6, num(KV["A5_s_loose"]), 2e-3)
cmp("A5 r L²/(16 EI₀) (10⁻⁹ m/N)", r_ * Lc ** 2 / (16 * EI0) * 1e6, num(KV["A5_slipL"]), 1e-3)
xb = np.array(ly["bolts_mm"])
c1 = 1 / EAs + r_ ** 2 / EI0


def bolts_linear(kb, P=1.0):
    """Unknowns: end slip s0 and bolt forces F_j. s(x_i) = s0 + (r/EI0)∫0^xi M + c1 Σ_{j<i} F_j (x_i − x_j); F_i = kb s(x_i); Σ F = 0."""
    n = len(xb)
    Mint = lambda x: P / 4 * x ** 2 if x <= Lc / 2 else P / 4 * (Lc ** 2 / 2 - (Lc - x) ** 2)  # noqa: E731   ∫0^x M dx, M = P/2 min(x, L−x)
    Amat = np.zeros((n + 1, n + 1)); rhs = np.zeros(n + 1)
    for i in range(n):
        Amat[i, 0] = kb
        for j in range(i):
            Amat[i, 1 + j] = kb * c1 * (xb[i] - xb[j])
        Amat[i, 1 + i] = -1.0
        rhs[i] = -kb * r_ / EI0 * Mint(xb[i])
    Amat[n, 1:] = 1.0
    sol = np.linalg.solve(Amat, rhs)
    s0, F = sol[0], sol[1:]
    # deflection: ∫ (M + r Σ_{x_j<x} F_j)/EI0 · m dx, m = min(x, L−x)/2
    xs = np.linspace(0, Lc, 60001)
    M = P / 2 * np.minimum(xs, Lc - xs)
    Fsum = np.concatenate([[0.0], np.cumsum(F)])[np.searchsorted(xb, xs, side="left")]   # Σ F_j over bolts left of x
    kap = (M + r_ * Fsum) / EI0
    m = np.minimum(xs, Lc - xs) / 2
    return np.trapezoid(kap * m, xs), s0, F


rb = get("C", "bolted")
Cb = np.polyfit([fl(r, "load_N") for r in rb], [fl(r, "defl_mm") for r in rb], 1)[0] - dsh
kb = optimize.brentq(lambda k: bolts_linear(k)[0] - Cb, 1e3, 1e6, xtol=1e-6)
cmp("A6 bolt slip modulus from a linear system for the bolt forces (kN/mm)", kb / 1e3, num(KV["A6_kb"]), 2e-3)
d1, s0, F = bolts_linear(kb, 2500.0)
cmp("A6 predicted end slip per newton (10⁻⁹ m/N)", abs(s0) / 2500 * 1e6, num(KV["A6_sp"]), 3e-3)
cmp("A6 largest bolt force at 2.5 kN (kN)", np.max(np.abs(F)) / 1e3, num(KV["A6_Fmax"]), 3e-3)
ybar = (bL * t2 * t2 / 2 + bL * t1 * (t2 + t1 / 2)) / (bL * (t1 + t2))
Qint = bL * t1 * (t2 + t1 / 2 - ybar)
Iful = EIf / E
cmp("A6 Beer's F = (VQ/I) s at 2.5 kN (kN)", 1250 * Qint / Iful * 100 / 1e3, num(KV["A6_Fb"]), 1e-3)
cmp("A6 glue shearing stress VQ/(Ib) at 4 kN (MPa)", 2000 * Qint / (Iful * bL), num(KV["A6_tg"]), 3e-3)

# ---------------- D1 ----------------
w, Ld, bD, tD = 8.0, 2400.0, 100.0, 50.0                          # N/mm, mm
q0 = 3 * (w * Ld / 2) / (4 * tD)
cmp("D1 shear flow at the support 3V/(4t) (N/mm)", q0, num(KV["D_q0"]), 1e-6)
cmp("D1 spacing limit at the support 10 kN / q (mm)", 10000 / q0, num(KV["D_smax"]), 1e-3)
cmp("D1 fully composite deflection 5wL⁴/(384 E I) (mm)", 5 * w * Ld ** 4 / (384 * E * bD * (2 * tD) ** 3 / 12), num(KV["D_full"]), 2e-3)
s_u = 70.0
xs_u = np.arange(s_u / 2, Ld, s_u)
Fmax = max(3 * w * (Ld / 2 - min(x, Ld - x)) / (4 * tD) * s_u for x in xs_u)
cmp("D1 uniform 70 mm spacing: number of bolts", len(xs_u), num(KV["D_u_n"]), 1e-9)
cmp("D1 uniform 70 mm spacing: largest Eq. 5 force (kN)", Fmax / 1e3, num(KV["D_u_F"]), 1e-3)

lines = ["## Lab 5 — handout questions re-solved from scratch vs. the instructor key", "",
         "| Question / quantity | From scratch | Key | Rel. difference | Tolerance | Result |", "|---|---:|---:|---:|---:|---|"]
for name, a_, b_, rel, tol, okk in out:
    lines.append(f"| {name} | {a_:.6g} | {b_:.6g} | {rel:.1e} | {tol:.0e} | {'PASS' if okk else '**FAIL**'} |")
nf = sum(not o[-1] for o in out)
lines += ["", f"{len(out) - nf} of {len(out)} agree.",
          "Tolerances: about 1e-3 where the key prints a rounded value of the same quantity; up to 1e-2 where a different "
          "estimator is used on purpose (global nonlinear fit, finite-difference R); 1.5e-2 for the single-step ratio, which ignores the fit intercept."]
(Path(__file__).parent / "results_from_scratch.md").write_text("\n".join(lines) + "\n")
print("\n".join(lines))
sys.exit(1 if nf else 0)

"""Generate lab01_instructor_key.md from computed results (no hand-typed numbers).

    python3 lab01_analysis.py && python3 make_key.py

Inputs: results.json (lab01_analysis.py on sample_data.csv), sim_numbers.json (simulation presets),
specimen_measurements.json. Placeholders in the template are written «name».
"""
import json
import math
import re
from pathlib import Path

import numpy as np

import lab01_analysis as LA

HERE = Path(__file__).resolve().parent
R = json.loads((HERE / "results.json").read_text())
SIM = json.loads((HERE / "sim_numbers.json").read_text())
MEAS = json.loads((HERE / "specimen_measurements.json").read_text())
st, al, des = R["steel_1018HR"], R["al_6061T6"], R["_design"]
V = {}


def f(x, nd):
    return f"{x:,.{nd}f}".replace(",", " ")


def pm(x, U, nd):
    return f"{f(x, nd)} ± {f(U, nd)}"


# ------------------------------------------------------------------ pre-lab
A0n = math.pi / 4 * 10.0 ** 2
V["A0n"] = f(A0n, 2)
for key, sy, su, E in (("s", 295, 440, 205.0), ("a", 278, 310, 68.9)):
    V[f"PY_{key}"] = f(sy * A0n / 1e3, 1)
    V[f"PU_{key}"] = f(su * A0n / 1e3, 1)
    V[f"PUfrac_{key}"] = f(su * A0n / 1e3, 0)
    V[f"dY_{key}"] = f(sy / (E * 1e3) * 50, 4)
    dw = (180 - 45) / (E * 1e3) * 50
    V[f"dw_{key}"] = f(dw * 1e3, 1)          # um
    V[f"rmax_{key}"] = f(math.sqrt(12) * 1e-3 * dw * 1e3, 2)   # um
    V[f"xh_err_{key}"] = f(100 * (1 / math.sqrt(12)) / (dw * 1e3), 2)
eps_target = 0.99
# ln(1+e)/e = 0.99 -> solve
lo, hi = 1e-4, 0.2
for _ in range(80):
    m = 0.5 * (lo + hi)
    if math.log1p(m) / m > eps_target:
        lo = m
    else:
        hi = m
V["P2_eps"] = f(100 * m, 2)
k = A0n * 0.008 / 60
V["AC_L"] = f(k, 5)
V["Eapp_s"] = f(1 / (1 / 205 + k), 1)
V["Eapp_a"] = f(1 / (1 / 68.9 + k), 1)
V["Eapp_s_pct"] = f(100 / (1 + 205 * k), 1)
V["Eapp_a_pct"] = f(100 / (1 + 68.9 * k), 1)
V["Erigid"] = f(1 / k, 1)
V["P4_eu"] = f(math.expm1(0.2), 4)
dE = 0.88 * math.sqrt(2 * 0.2 * 0.003)
V["P4_d"] = f(dE, 4)
V["P4_etu"] = f(0.2 - dE, 4)
V["P4_eu2"] = f(math.expm1(0.2 - dE), 4)
for key, s in (("s", SIM["steel"]), ("a", SIM["al"])):
    V[f"sim_sY_{key}"] = f(s["sigY"], 1)
    V[f"sim_sU_{key}"] = f(s["sigU"], 1)
    V[f"sim_eu_{key}"] = f(100 * s["e_u"], 1)
    V[f"sim_EL_{key}"] = f(100 * s["EL"], 1)
    V[f"sim_Eapp_{key}"] = f(s["Eapp"], 1)
    V[f"cf_eu_{key}"] = f(100 * s["cf_e_u"], 1)

# ------------------------------------------------------------------ analysis (both materials)
for key, r in (("s", st), ("a", al)):
    V[f"d0_{key}"] = f(r["d0"], 3)
    V[f"ud0_{key}"] = f(r["u_d0"], 4)
    V[f"A0_{key}"] = f(r["A0"], 2)
    V[f"uA_{key}"] = f(100 * r["urel_A"], 2)
    V[f"E_{key}"] = pm(r["E"], 2 * r["uE"], 1)
    V[f"Ev_{key}"] = f(r["E"], 2)
    V[f"UE_{key}"] = f(2 * r["uE"], 2)
    V[f"Estat_{key}"] = f(100 * r["E_stat_rel"], 2)
    V[f"Eint_{key}"] = f(r["E_intercept_MPa"], 2)
    V[f"Enpts_{key}"] = str(r["E_npts"])
    V[f"Elow_{key}"] = f(r["E_low"], 1)
    V[f"Ehigh_{key}"] = f(r["E_high"], 1)
    V[f"Ehd_{key}"] = f(r["E_halves_diff"], 2)
    V[f"Ehs_{key}"] = f(r["E_halves_sig"], 2)
    V[f"Ewide_{key}"] = f(r["E_wide"], 1)
    V[f"Ewide_pct_{key}"] = f(100 * (r["E_wide"] / r["E"] - 1), 1)
    ref = r["ref"]
    V[f"Eagree_lim_{key}"] = f(2 * math.hypot(r["uE"], ref["uE"]), 2)
    V[f"Eagree_d_{key}"] = f(abs(r["E"] - ref["E"]), 2)
    V[f"sU_{key}"] = pm(r["sigU"], 2 * r["uU"], 1)
    V[f"Pmax_{key}"] = f(r["Pmax"] / 1e3, 2)
    V[f"off_{key}"] = pm(r["sig_offset"], 2 * r["u_offset"], 1)
    V[f"dsdE_{key}"] = f(r["dsig_dE"], 3)
    V[f"Cm_{key}"] = pm(r["Cm"], 2 * r["uCm"], 5)
    V[f"toe_{key}"] = pm(r["toe"], 2 * r["u_toe"], 4)
    V[f"Eapp_m_{key}"] = pm(r["E_app"], 2 * r["uE_app"], 2)
    V[f"Eapp_p_{key}"] = f(r["E_app_pred"], 2)
    V[f"splice_{key}"] = f(r["splice_mismatch"] * 1e6, 0)
    V[f"eu_{key}"] = pm(r["e_u"], 2 * r["u_eu"], 3)
    V[f"euspan_{key}"] = f(r["e_u_span"], 4)
    V[f"etu_{key}"] = pm(r["eps_t_u"], 2 * r["u_eps_t_u"], 3)
    V[f"K_{key}"] = f(r["K_hollomon"], 0)
    V[f"n_{key}"] = pm(r["n_hollomon"], 2 * r["u_n"], 4)
    V[f"nv_{key}"] = f(r["n_hollomon"], 3)
    V[f"cons_{key}"] = f(r["considere_direct"], 3)
    V[f"EL_{key}"] = pm(r["EL"], 2 * r["u_EL"], 1)
    V[f"RA_{key}"] = pm(r["RA"], 2 * r["u_RA"], 1)
    V[f"uY_{key}"] = f(r["u_res"], 3)
    V[f"uUe_{key}"] = f(r["uU_eng"], 2)
    V[f"uUt_{key}"] = f(r["uU_true"], 2)
    V[f"tough_{key}"] = f(r["toughness_ch"], 1)
    V[f"ech_f_{key}"] = f(100 * r["e_f_crosshead"], 1)
    V[f"Pf_{key}"] = f(r["P_f"] / 1e3, 2)
    V[f"sf_{key}"] = f(r["s_f"], 1)
    V[f"tform_{key}"] = f(r["sig_t_formula_f"], 1)
    V[f"tneck_{key}"] = pm(r["sig_t_neck_f"], 2 * r["u_sig_t_neck_f"], 1)
    V[f"tneckv_{key}"] = f(r["sig_t_neck_f"], 1)
    V[f"terr_{key}"] = f(r["formula_error_pct"], 0)
    V[f"df_{key}"] = f(r["df"], 3)
    V[f"etneck_{key}"] = f(r["eps_t_neck_f"], 3)
    # imperfection estimate from diameter readings: delta_A = 2 (d_max - d_min)/d_mean
    rd = MEAS["steel_1018HR" if key == "s" else "al_6061T6"]["d0_readings_mm"]
    dA = 2 * (max(rd) - min(rd)) / np.mean(rd)
    V[f"dA_{key}"] = f(100 * dA, 2)
    dEps = 0.88 * math.sqrt(2 * r["n_hollomon"] * dA)
    V[f"dEps_{key}"] = f(dEps, 4)
    V[f"npred_{key}"] = f(r["n_hollomon"] - dEps, 3)
    V[f"nres_{key}"] = f(r["n_hollomon"] - dEps - r["eps_t_u"], 3)
    V[f"ndisc_{key}"] = f(r["n_hollomon"] - r["eps_t_u"], 3)
    V[f"nU_{key}"] = f(2 * math.hypot(r["u_eps_t_u"], r["u_n"]), 3)
V["sly"] = pm(st["sig_ly"], 2 * st["u_ly"], 1)
V["suy"] = pm(st["sig_uy"], 2 * st["u_uy"], 1)
V["sY_a"] = pm(al["sigY"], 2 * al["uY"], 1)
V["plateau_end"] = f(st["e_plateau_end"], 4)
V["ELv_s"] = f(st["EL"], 1)
V["ELv_a"] = f(al["EL"], 1)

# ------------------------------------------------------------------ C2: Monte Carlo for Al offset yield
def mc_offset(n_draw=4000, seed=7):
    data = LA.load(LA.LAB / "sample_data.csv")["al_6061T6"]
    m = MEAS["al_6061T6"]
    rd = np.array(m["d0_readings_mm"])
    rng = np.random.default_rng(seed)
    P0, ext0 = data["P"], data["ext"]
    valid = ~np.isnan(ext0)
    res_E, res_Y = [], []
    for _ in range(n_draw):
        d0 = rd.mean() + rng.normal(0, rd.std(ddof=1) / math.sqrt(len(rd))) + rng.uniform(-LA.CAL_ACC, LA.CAL_ACC)
        A0 = math.pi / 4 * d0 ** 2
        P = P0 * (1 + rng.uniform(-LA.LOAD_REL, LA.LOAD_REL))
        Le = 50.0 * (1 + rng.uniform(-LA.EXT_GAGE_REL, LA.EXT_GAGE_REL))
        e = ext0 * (1 + rng.uniform(-LA.EXT_REL, LA.EXT_REL)) / Le
        s = P / A0
        first_hi = int(np.argmax(s > LA.E_WINDOW[1] * 1.05))
        w = (np.arange(len(s)) < first_hi) & valid & (s >= LA.E_WINDOW[0]) & (s <= LA.E_WINDOW[1])
        b = np.polyfit(e[w], s[w], 1)[0]
        fsel = s - b * (e - 0.002)
        ok = valid[:-1] & valid[1:] & (fsel[:-1] > 0) & (fsel[1:] <= 0) & (e[:-1] > 0.001)
        j = np.where(ok)[0][0]
        t = fsel[j] / (fsel[j] - fsel[j + 1])
        res_E.append(b / 1e3)
        res_Y.append(s[j] + t * (s[j + 1] - s[j]))
    return np.std(res_E, ddof=1), np.std(res_Y, ddof=1), np.mean(res_Y)


uE_mc, uY_mc, Y_mc = mc_offset()
V["mc_uE"] = f(uE_mc, 3)
V["mc_uY"] = f(uY_mc, 2)
V["mc_Y"] = f(Y_mc, 1)
V["lin_uE"] = f(al["uE"], 3)
V["lin_uY"] = f(al["uY"], 2)
V["mc_agree"] = f"within {max(abs(uE_mc / al['uE'] - 1), abs(uY_mc / al['uY'] - 1)) * 100:.0f} %"

# ------------------------------------------------------------------ C1, X1 from the simulation
for key, s in (("s", SIM["steel"]), ("a", SIM["al"])):
    rows = s["C1"]
    sl = np.polyfit(np.log([r["d"] for r in rows]), np.log([r["num"] for r in rows]), 1)[0]
    V[f"C1slope_{key}"] = f(sl, 2)
    V[f"C1tab_{key}"] = " | ".join(f"{100 * r['d']:.2f} % → {r['num']:.4f} vs {r['est']:.4f} ({100 * r['err']:+.0f} %)" for r in rows)
    X = {r["r"]: r for r in s["X1"]}
    V[f"X1_{key}"] = ", ".join(f"{r}d₀: {100 * X[r]['EL']:.1f} %" for r in (2, 3, 4, 5, 8))
    V[f"mesh_{key}"] = ", ".join(f"N = {n}: {100 * e:.1f} %" for n, e in s["mesh"] if n in (2, 5, 12, 32, 80, 200))
c_s = (st["EL"] / 100 - st["e_u"]) * 5
V["c_s"] = f(c_s, 2)
V["EL4_s"] = f(100 * (st["e_u"] + c_s / 4), 1)
epsL = st["e_plateau_end"] - st["sig_ly"] / (st["E"] * 1e3)
V["epsL"] = f(epsL, 4)
V["vfront"] = f(1.0 / epsL, 0)
V["plat_t"] = f(st["t_plateau"], 0)
for a_over_R in (0.5, 1.0):
    fac = (1 + 2 / a_over_R) * math.log(1 + a_over_R / 2)
    V[f"bridg_{str(a_over_R).replace('.', '')}"] = f(st["sig_t_neck_f"] / fac, 0)
    V[f"bfac_{str(a_over_R).replace('.', '')}"] = f(fac, 3)

# ------------------------------------------------------------------ design
for key, kk in (("s", "steel_1018HR"), ("a", "al_6061T6")):
    x = des[kk]
    for name in ("sigY_lo", "A_strength", "A_stiff", "A_over", "d_req", "A", "stress_service_thread", "FS_actual", "delta", "mass", "cost"):
        V[f"D_{name}_{key}"] = f(x[name], 2 if name not in ("A_strength", "A_stiff", "A_over", "A") else 1)
    V[f"D_d_{key}"] = str(x["d_pick"])
    V[f"D_gov_{key}"] = x["governs"]

tmpl = (HERE / "lab01_instructor_key.template.md").read_text(encoding="utf-8")
missing = sorted(set(re.findall(r"«(\w+)»", tmpl)) - set(V))
if missing:
    raise SystemExit(f"missing values: {missing}")
out = re.sub(r"«(\w+)»", lambda m: V[m.group(1)], tmpl)
(HERE / "lab01_instructor_key.md").write_text(out, encoding="utf-8")
(HERE / "key_values.json").write_text(json.dumps(V, indent=1, ensure_ascii=False))
print("wrote lab01_instructor_key.md;", len(V), "values")

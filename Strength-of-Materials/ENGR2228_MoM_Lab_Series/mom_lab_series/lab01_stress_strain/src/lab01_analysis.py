"""Lab 1 analysis: every number in the instructor key comes from this script.

    python3 lab01_analysis.py                      # sample data -> results.json + printed summary
    python3 lab01_analysis.py my_class.csv my_measurements.json   # your own class data

Works on any CSV with columns specimen,time_s,load_N,crosshead_mm,extensometer_mm
(blank extensometer cells after removal). Procedures match the handout exactly.
"""
import json
import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
LAB = HERE.parent

# Instrument specifications (handout Appendix A). Limits +/-a -> u = a/sqrt(3).
CAL_ACC = 0.02          # mm, caliper accuracy limit
LOAD_REL = 0.005        # load cell, fraction of reading
EXT_REL = 0.005         # extensometer, fraction of reading
EXT_GAGE_REL = 0.005    # extensometer gage length tolerance, fraction
R3 = math.sqrt(3.0)
E_WINDOW = (45.0, 180.0)   # MPa, fit window for E (about 15-60 % of yield for both materials)
REF = {   # reference ("theory") values: handbook-typical with spread treated as standard uncertainty
    "steel_1018HR": dict(E=205.0, uE=3.0, sigY_min=220.0, sigY_typ=(250, 340), sigU_typ=(400, 480), EL_typ=(25, 38)),
    "al_6061T6": dict(E=68.9, uE=1.0, sigY_min=240.0, sigY_typ=(255, 300), sigU_typ=(290, 330), EL_typ=(8, 17)),
}


def load(csv_path):
    import csv
    data = {}
    with open(csv_path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            d = data.setdefault(r["specimen"], {"t": [], "P": [], "xh": [], "ext": []})
            d["t"].append(float(r["time_s"]))
            d["P"].append(float(r["load_N"]))
            d["xh"].append(float(r["crosshead_mm"]))
            d["ext"].append(float(r["extensometer_mm"]) if r["extensometer_mm"].strip() else np.nan)
    return {k: {kk: np.array(vv) for kk, vv in v.items()} for k, v in data.items()}


def linfit(x, y):
    """Least squares y = a + b x with standard errors."""
    n = len(x)
    A = np.vstack([np.ones(n), x]).T
    coef, res, *_ = np.linalg.lstsq(A, y, rcond=None)
    yhat = A @ coef
    s2 = np.sum((y - yhat) ** 2) / (n - 2)
    cov = s2 * np.linalg.inv(A.T @ A)
    return coef[0], coef[1], math.sqrt(cov[0, 0]), math.sqrt(cov[1, 1]), math.sqrt(s2)


def analyze(key, d, m):
    out = {"label": m["label"]}
    # ---- geometry --------------------------------------------------------------------
    r = np.array(m["d0_readings_mm"])
    d0 = r.mean()
    u_d0 = math.sqrt((r.std(ddof=1) / math.sqrt(len(r))) ** 2 + (CAL_ACC / R3) ** 2)
    A0 = math.pi / 4 * d0 ** 2
    urel_A = 2 * u_d0 / d0
    L0, Le, Lc = m["L0_mm"], m["extensometer_gage_mm"], m["reduced_section_mm"]
    out.update(d0=d0, u_d0=u_d0, A0=A0, urel_A=urel_A)

    P, xh, ext = d["P"], d["xh"], d["ext"]
    s = P / A0                      # MPa (N/mm^2)
    e_ext = ext / Le
    valid = ~np.isnan(e_ext)
    i_max = int(np.argmax(P))
    # peak load: quadratic fit to the 21 points around the maximum (reduces noise bias)
    sl = slice(max(i_max - 10, 0), i_max + 11)
    c = np.polyfit(np.arange(len(P[sl])), P[sl], 2)
    Pmax = float(np.polyval(c, -c[1] / (2 * c[0]))) if c[0] < 0 else float(P[i_max])
    noise_P = float(np.std(np.diff(P[valid][5:60])) / math.sqrt(2))   # load noise from early increments
    out.update(Pmax=Pmax, noise_P=noise_P)

    # ---- elastic modulus (extensometer) -------------------------------------------------
    # initial loading branch only: up to the first point where s exceeds the window top
    first_hi = int(np.argmax(s > E_WINDOW[1] * 1.05))
    w = (np.arange(len(s)) < first_hi) & valid & (s >= E_WINDOW[0]) & (s <= E_WINDOW[1])
    a, b, ua, ub, sres = linfit(e_ext[w], s[w])
    E = b / 1e3                     # GPa
    urel_stat = ub / b
    # window linearity test (handout Sec. 2.11): fit the two halves of the window
    mid = 0.5 * (E_WINDOW[0] + E_WINDOW[1])
    wl, wh = w & (s <= mid), w & (s > mid)
    _, bl, _, ubl, _ = linfit(e_ext[wl], s[wl])
    _, bh, _, ubh, _ = linfit(e_ext[wh], s[wh])
    diff = abs(bl - bh) / 1e3
    sig_diff = math.hypot(ubl, ubh) / 1e3
    u_win = diff / 2 if diff > 2 * sig_diff else 0.0
    urel_E = math.sqrt(urel_stat ** 2 + urel_A ** 2 + (LOAD_REL / R3) ** 2 + (EXT_REL / R3) ** 2 + (EXT_GAGE_REL / R3) ** 2
                       + (u_win / E) ** 2)
    out.update(E=E, uE=E * urel_E, E_npts=int(w.sum()), E_stat_rel=urel_stat, E_intercept_MPa=a,
               E_low=bl / 1e3, E_high=bh / 1e3, E_halves_diff=diff, E_halves_sig=sig_diff, u_win=u_win)
    # wider window (A2 check): 45-260 MPa
    ww = (np.arange(len(s)) < int(np.argmax(s > 260 * 1.05))) & valid & (s >= 45) & (s <= 260)
    out["E_wide"] = linfit(e_ext[ww], s[ww])[1] / 1e3

    # ---- yield ---------------------------------------------------------------------------
    urel_s = math.sqrt(urel_A ** 2 + (LOAD_REL / R3) ** 2)
    early = valid & (e_ext < 0.03)
    if key.startswith("steel"):
        i_uy = int(np.argmax(np.where(early & (e_ext < 0.004), s, -1)))
        sig_uy = float(s[i_uy])
        # plateau: from 0.1 % past the upper-yield point until hardening lifts the stress clearly above
        # the plateau level (first estimate from the next 0.4 % of strain, then 5 MPa above it)
        after = early & (e_ext > e_ext[i_uy] + 0.001)
        lvl0 = float(np.median(s[after & (e_ext < e_ext[i_uy] + 0.005)]))
        idx = np.where(after)[0]
        above = idx[s[idx] > lvl0 + 5.0]
        e_end = float(e_ext[above[0]]) if len(above) else 0.015
        plateau = after & (e_ext < e_end - 0.001)
        sig_ly = float(np.mean(s[plateau]))
        t_plat = float(d["t"][plateau].max() - d["t"][np.where(after)[0][0]])
        u_ly_stat = float(np.std(s[plateau], ddof=1) / math.sqrt(plateau.sum() / 4))  # ~4-sample correlation
        out.update(sig_uy=sig_uy, u_uy=sig_uy * urel_s, sig_ly=sig_ly,
                   u_ly=math.sqrt((sig_ly * urel_s) ** 2 + u_ly_stat ** 2), sigY=sig_ly,
                   e_plateau_end=e_end, t_plateau=t_plat)
        out["uY"] = out["u_ly"]
    # 0.2 % offset (reported for both; for steel it lands on the plateau)
    def offset_yield(Eg):
        f = s - Eg * 1e3 * (e_ext - 0.002)
        ok = valid[:-1] & valid[1:]
        idx = np.where(ok & (f[:-1] > 0) & (f[1:] <= 0) & (e_ext[:-1] > 0.001))[0]
        j = idx[0]
        t = f[j] / (f[j] - f[j + 1])
        return float(s[j] + t * (s[j + 1] - s[j])), float(e_ext[j] + t * (e_ext[j + 1] - e_ext[j]))
    sig_off, e_off = offset_yield(E)
    dsdE = (offset_yield(E * 1.01)[0] - offset_yield(E * 0.99)[0]) / (0.02 * E)
    u_off = math.sqrt((sig_off * urel_s) ** 2 + (dsdE * out["uE"]) ** 2)
    out.update(sig_offset=sig_off, u_offset=u_off, e_offset=e_off, dsig_dE=dsdE)
    if not key.startswith("steel"):
        out.update(sigY=sig_off, uY=u_off)

    # ---- ultimate strength ----------------------------------------------------------------
    sigU = Pmax / A0
    out.update(sigU=sigU, uU=sigU * urel_s)

    # ---- machine compliance from the overlap of extensometer and crosshead ---------------
    ov = valid & (P > 3000) & (np.arange(len(P)) < first_hi)        # elastic loading, toe taken up
    yv = xh[ov] - (Lc / Le) * ext[ov]
    c0, Cm, uc0, uCm, _ = linfit(P[ov] / 1e3, yv)       # mm and mm/kN
    out.update(Cm=Cm, uCm=uCm, toe=c0, u_toe=uc0, Cm_npts=int(ov.sum()))
    # apparent modulus from raw crosshead (initial loading, same stress window)
    wa = (np.arange(len(s)) < first_hi) & (s >= E_WINDOW[0]) & (s <= E_WINDOW[1])
    _, bapp, _, ubapp, _ = linfit(xh[wa] / Lc, s[wa])
    E_app = bapp / 1e3
    E_app_pred = 1.0 / (1.0 / E + A0 * Cm / Lc)   # springs in series; mm^2*(mm/kN)/mm = 1/(kN/mm^2) = 1/GPa
    out.update(E_app=E_app, uE_app=ubapp / 1e3, E_app_pred=E_app_pred)

    # ---- corrected strain over the whole test --------------------------------------------
    e_ch = (xh - Cm * P / 1e3 - c0) / Lc                # uniform strain of the reduced section
    e_all = np.where(valid, e_ext, e_ch)               # extensometer while attached, then corrected crosshead
    # check the splice: mean mismatch over the last 50 extensometer points
    last = np.where(valid)[0][-50:]
    out["splice_mismatch"] = float(np.mean(e_ch[last] - e_ext[last]))
    # uniform elongation at max load; flatness: strain range where P is within 2 noise of Pmax
    e_u = float(np.interp(Pmax, [P[i_max]], [e_all[i_max]])) if False else float(e_all[i_max])
    near = np.where(P >= Pmax - 2 * noise_P * 1.0)[0]
    near = near[(near > i_max - 400) & (near < i_max + 400)]
    span = float(e_all[near].max() - e_all[near].min())
    u_eu = math.sqrt((span / 2 / R3) ** 2 + (0.003 * e_u) ** 2)
    out.update(e_u=e_u, u_eu=u_eu, e_u_span=span)

    # ---- true stress-strain to maximum load; hardening fit; Considere check ----------------
    pre = np.arange(len(P)) <= i_max
    sig_t = s * (1 + e_all)
    eps_t = np.log1p(e_all)
    lo = 0.03 if key.startswith("steel") else 0.010
    fitm = pre & (eps_t > lo) & (eps_t < math.log1p(e_u) * 0.97) & (sig_t > 0)
    bb, nn, ubb, unn, _ = linfit(np.log(eps_t[fitm]), np.log(sig_t[fitm]))
    K = math.exp(bb)
    out.update(K_hollomon=K, n_hollomon=nn, u_n=unn, eps_t_u=math.log1p(e_u), u_eps_t_u=u_eu / (1 + e_u),
               fit_range=(lo, math.log1p(e_u) * 0.97))
    # direct Considere: numerically differentiate a smoothed sigma_t(eps_t) and find d sigma/d eps = sigma
    sel = pre & (eps_t > lo)
    et, st = eps_t[sel], sig_t[sel]
    grid = np.linspace(et.min(), et.max(), 120)
    ss = np.interp(grid, *zip(*sorted(zip(et, st))))
    kern = np.ones(9) / 9
    ss = np.convolve(np.pad(ss, 4, mode="edge"), kern, mode="valid")
    dsde = np.gradient(ss, grid)
    cross = np.where((dsde[:-1] - ss[:-1] > 0) & (dsde[1:] - ss[1:] <= 0))[0]
    out["considere_direct"] = float(grid[cross[-1]]) if len(cross) else float("nan")

    # ---- energy densities (MJ/m^3 = MPa) ---------------------------------------------------
    order = pre & ~np.isnan(e_all)
    uU_eng = float(np.trapezoid(s[order], e_all[order]))
    uU_true = float(np.trapezoid(sig_t[order], eps_t[order]))
    # toughness to fracture: engineering curve with corrected-crosshead strain (gage-length dependent!)
    fr = P > 0.2 * Pmax
    i_f = int(np.where(fr)[0][-1])
    toughness = float(np.trapezoid(s[: i_f + 1], e_all[: i_f + 1]))
    out.update(uU_eng=uU_eng, uU_true=uU_true, toughness_ch=toughness, u_res=(out["sigY"] ** 2) / (2 * E * 1e3))

    # ---- ductility -----------------------------------------------------------------------
    Lf = m["Lf_mm"]
    EL = (Lf - L0) / L0 * 100
    u_L = math.sqrt(2) * CAL_ACC / R3
    u_EL = 100 * math.sqrt((u_L / L0) ** 2 + (Lf * u_L / L0 ** 2) ** 2)
    df = float(np.mean(m["df_readings_mm"]))
    u_df = math.sqrt((CAL_ACC / R3) ** 2 + 0.02 ** 2)   # neck is not a clean cylinder: add 0.02 mm form error
    RA = (1 - (df / d0) ** 2) * 100
    u_RA = 100 * 2 * (df / d0) ** 2 * math.sqrt((u_df / df) ** 2 + (u_d0 / d0) ** 2)
    out.update(Lf=Lf, EL=EL, u_EL=u_EL, df=df, u_df=u_df, RA=RA, u_RA=u_RA)
    # strain at fracture from corrected crosshead (reduced section 60 mm) vs marks (50 mm)
    out["e_f_crosshead"] = float(e_ch[i_f])

    # ---- true stress at fracture: formula vs neck --------------------------------------------
    Pf = float(P[i_f])
    sf = Pf / A0
    e_f_marks = EL / 100
    sig_formula = sf * (1 + e_f_marks)
    Af = math.pi / 4 * df ** 2
    sig_neck = Pf / Af
    eps_neck = math.log(A0 / Af)
    u_neck = sig_neck * math.sqrt((LOAD_REL / R3) ** 2 + (2 * u_df / df) ** 2)
    out.update(P_f=Pf, s_f=sf, sig_t_formula_f=sig_formula, sig_t_neck_f=sig_neck, u_sig_t_neck_f=u_neck,
               eps_t_neck_f=eps_neck, eps_t_formula_f=math.log1p(e_f_marks),
               formula_error_pct=(sig_formula - sig_neck) / sig_neck * 100)
    out["ref"] = REF.get(key, {})
    return out


def design(results, P_service=12.0e3, P_over=18.0e3, L=1.80, delta_max=1.2, FS=2.0, k_thread=0.78):
    """Reference solutions for the open-ended design problem D1 (handout Sec. 9)."""
    rho = {"steel_1018HR": 7870, "al_6061T6": 2700}
    cost = {"steel_1018HR": 2.20, "al_6061T6": 6.50}   # $/kg, bar stock
    sols = {}
    for key, r in results.items():
        sigY_lo = r["sigY"] - 2 * r["uY"]              # conservative: lower 95 % bound
        E = r["E"] * 1e3                                # MPa
        A_strength = P_service * FS / sigY_lo / k_thread   # gross area, mm^2 (stress on thread stress area)
        A_stiff = P_service * L * 1e3 / (E * delta_max)
        A_over = P_over / sigY_lo / k_thread
        A_req = max(A_strength, A_stiff, A_over)
        d_req = math.sqrt(4 * A_req / math.pi)
        d_pick = math.ceil(d_req)                      # 1 mm stock increments
        A = math.pi / 4 * d_pick ** 2
        mass = A * 1e-6 * L * rho[key]
        sols[key] = dict(sigY_lo=sigY_lo, A_strength=A_strength, A_stiff=A_stiff, A_over=A_over,
                         governs=["strength", "stiffness", "overload"][int(np.argmax([A_strength, A_stiff, A_over]))],
                         d_req=d_req, d_pick=d_pick, A=A, stress_service_thread=P_service / (k_thread * A),
                         FS_actual=sigY_lo / (P_service / (k_thread * A)), delta=P_service * L * 1e3 / (E * A),
                         mass=mass, cost=mass * cost[key])
    return sols


def main():
    csv_path = Path(sys.argv[1]) if len(sys.argv) > 1 else LAB / "sample_data.csv"
    meas_path = Path(sys.argv[2]) if len(sys.argv) > 2 else HERE / "specimen_measurements.json"
    data = load(csv_path)
    meas = json.loads(meas_path.read_text())
    results = {k: analyze(k, data[k], meas[k]) for k in data}
    results["_design"] = design({k: v for k, v in results.items()})
    (HERE / "results.json").write_text(json.dumps(results, indent=2, default=float))
    for k, r in results.items():
        if k.startswith("_"):
            continue
        print(f"\n=== {r['label']} ===")
        for name in ("d0", "u_d0", "A0", "E", "uE", "E_npts", "E_low", "E_high", "E_halves_diff", "E_halves_sig", "u_win", "E_wide", "sigY", "uY", "sig_uy", "sig_ly", "sig_offset", "u_offset",
                     "sigU", "uU", "Pmax", "Cm", "uCm", "toe", "E_app", "E_app_pred", "splice_mismatch", "e_u", "u_eu",
                     "e_u_span", "n_hollomon", "u_n", "K_hollomon", "eps_t_u", "considere_direct", "uU_eng", "uU_true",
                     "toughness_ch", "u_res", "EL", "u_EL", "RA", "u_RA", "e_f_crosshead", "P_f", "s_f", "sig_t_formula_f",
                     "sig_t_neck_f", "u_sig_t_neck_f", "eps_t_neck_f", "formula_error_pct"):
            if name in r:
                v = r[name]
                print(f"  {name:20s} {v:.6g}" if isinstance(v, float) else f"  {name:20s} {v}")
    print("\n=== design ===")
    for k, v in results["_design"].items():
        print(k, {kk: (round(vv, 3) if isinstance(vv, float) else vv) for kk, vv in v.items()})


if __name__ == "__main__":
    main()

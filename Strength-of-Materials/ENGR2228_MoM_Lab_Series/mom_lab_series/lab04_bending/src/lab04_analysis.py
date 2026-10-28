"""Lab 4 analysis: every number in the instructor key comes from this script.

    python3 lab04_analysis.py [data.csv] [measurements.json]   ->  results.json + printed summary
"""
import csv
import json
import math
import sys
import warnings
from pathlib import Path

import numpy as np

from lab04_model import composite_props, epp_rect_M, ibeam_props, section_moment, sigma_of

warnings.filterwarnings("ignore", message="The occurrence of roundoff")
HERE = Path(__file__).resolve().parent
LAB = HERE.parent
R3 = math.sqrt(3)
SIDE = [f"strain_side{j}_ue" for j in range(1, 6)]


def load(path):
    rows = list(csv.DictReader(open(path, newline="")))
    out = {}
    for part in "ABC":
        rr = [r for r in rows if r["part"] == part]
        out[part] = {c: np.array([float(r[c]) if r[c].strip() else np.nan for r in rr]) for c in rows[0] if c != "part"}
    return out


def linfit(x, y):
    n = len(x)
    A = np.vstack([np.ones(n), x]).T
    coef, *_ = np.linalg.lstsq(A, y, rcond=None)
    res = y - A @ coef
    s2 = res @ res / (n - 2)
    cov = s2 * np.linalg.inv(A.T @ A)
    return coef[0], coef[1], math.sqrt(cov[0, 0]), math.sqrt(cov[1, 1]), float(np.sqrt(np.mean(res ** 2)))


def mean_u(vals, acc):
    v = np.array(vals, float)
    return v.mean(), math.sqrt((v.std(ddof=1) / math.sqrt(len(v))) ** 2 + (acc / R3) ** 2)


def profile_fits(D, ys_mm, H_mm):
    """Per step: fit strain (all through-depth gages) vs height; returns kappa (1/m), NA height (mm), rms (µε)."""
    out = []
    for i in range(len(D["load_N"])):
        y = np.r_[ys_mm, H_mm, 0.0]
        e = np.r_[[D[c][i] for c in SIDE], D["strain_top_ue"][i], D["strain_bottom_ue"][i]]
        a, b, ua, ub, rms = linfit(y, e)          # e = a + b y   (µε, mm)
        kappa = -b * 1e-6 / 1e-3                  # 1/m
        yna = -a / b if abs(b) > 1e-9 else np.nan
        out.append(dict(P=float(D["load_N"][i]), kappa=kappa, u_kappa=ub * 1e-3, yNA=yna, rms=rms, a=a, b=b))
    return out


def analyze(data, m):
    ref = m["reference"]
    u_gf = m["gage_factor_tolerance_pct"] / 100 / R3
    u_load = m["load_cell_accuracy_pct"] / 100 / R3
    b, ub = mean_u(m["b_mm"], m["caliper_accuracy_mm"])
    h, uh = mean_u(m["h_mm"], m["caliper_accuracy_mm"])
    ts, uts = mean_u(m["ts_mm"], m["caliper_accuracy_mm"])
    L = m["span_mm"]
    a = 0.5 * (m["a1_mm"] + (L - m["a2_mm"]))                  # mm, mean shear-span length
    ua = m["load_position_accuracy_mm"] / R3 / math.sqrt(2)
    I = b * h ** 3 / 12                                        # mm^4
    uI_rel = math.sqrt((ub / b) ** 2 + (3 * uh / h) ** 2)
    out = {"geom": dict(b=b, ub=ub, h=h, uh=uh, ts=ts, uts=uts, a=a, ua=ua, I_mm4=I, uI_rel=uI_rel, L=L)}
    # ------------------------------------------------------------------ Part A
    A = data["A"]
    fits = profile_fits(A, m["yA_mm"], h)
    P = A["load_N"]
    Mm = P / 2 * a / 1e3                                       # N·m
    sel = P > 1000
    k = np.array([f["kappa"] for f in fits])
    _, slope, _, uslope, _ = linfit(k[sel], Mm[sel])          # dM/dkappa, N·m²
    E = slope / (I * 1e-12) / 1e9                              # GPa
    uE = E * math.sqrt((uslope / slope) ** 2 + uI_rel ** 2 + (ua / a) ** 2 + u_load ** 2 + u_gf ** 2)
    yna = np.array([f["yNA"] for f in fits])[sel]
    yna_mean, yna_s = float(np.mean(yna)), float(np.std(yna, ddof=1) / math.sqrt(sel.sum()))
    u_yna = math.sqrt(yna_s ** 2 + (m["height_gage_accuracy_mm"] / R3) ** 2 / 5)
    i20 = int(np.argmax(P))
    # transverse (anticlastic) strain on the top face
    _, sl_t, _, usl_t, _ = linfit(A["strain_top_ue"][sel], A["strain_transverse_top_ue"][sel])
    nu = -sl_t
    unu = math.sqrt(usl_t ** 2 + (0.005 / R3) ** 2)
    # moment diagram from the bottom gages: M = E S eps
    S = I / (h / 2)                                            # mm^3
    Ex = {}
    for col, x in (("strain_bottom_x100_ue", m["x_bottom_mm"][0]), ("strain_bottom_x150_ue", m["x_bottom_mm"][1]), ("strain_bottom_ue", L / 2)):
        _, sl, _, usl, _ = linfit(P[sel], A[col][sel])         # µε per N
        Mper = E * 1e3 * S * sl * 1e-6 / 1e3                   # N·m per N  (E in MPa, S mm³ -> N·mm -> N·m)
        Ex[f"{x:.0f}"] = dict(x=x, M_per_N=Mper, u_rel=math.sqrt((usl / sl) ** 2 + (uE / E) ** 2 + uI_rel ** 2 + (uh / h) ** 2))
    V_meas = (Ex["150"]["M_per_N"] - Ex["100"]["M_per_N"]) / ((m["x_bottom_mm"][1] - m["x_bottom_mm"][0]) / 1e3)   # per N of P
    uV = V_meas * math.hypot(Ex["150"]["u_rel"] * Ex["150"]["M_per_N"], Ex["100"]["u_rel"] * Ex["100"]["M_per_N"]) / (Ex["150"]["M_per_N"] - Ex["100"]["M_per_N"])
    out["A"] = dict(E=E, uE=uE, E_stat_rel=uslope / slope, n_steps=int(sel.sum()), yNA=yna_mean, u_yNA=u_yna, h_half=h / 2,
                    yNA_off=yna_mean - h / 2, rms20=fits[i20]["rms"], kappa20=fits[i20]["kappa"], M20=float(Mm[i20]),
                    eps_bot20=float(A["strain_bottom_ue"][i20]), sigma_bot20=float(E * 1e3 * A["strain_bottom_ue"][i20] * 1e-6),
                    sigma_flex20=float(Mm[i20] * 1e3 * (h / 2) / I), nu=nu, unu=unu, Ex=Ex, V_per_N=V_meas, uV_per_N=abs(uV),
                    E_ref=ref["E_al_GPa"], E_agree_lim=2 * math.hypot(uE, ref["u_E_al_GPa"]), nu_agree_lim=2 * math.hypot(unu, ref["u_nu_al"]),
                    I_mm4=I, S_mm3=S)
    # ------------------------------------------------------------------ Part B (composite)
    B = data["B"]
    H = h + ts
    fitsB = profile_fits(B, m["yB_mm"], H)
    PB = B["load_N"]
    selB = PB > 1000
    E_al = E
    E_st = ref["E_st_GPa"]
    cp = composite_props(b, h, ts, E_al, E_st)                 # mm-based (E ratio only matters)
    ynaB = np.array([f["yNA"] for f in fitsB])[selB]
    ynaB_mean, ynaB_s = float(np.mean(ynaB)), float(np.std(ynaB, ddof=1) / math.sqrt(selB.sum()))
    u_ynaB = math.sqrt(ynaB_s ** 2 + (m["height_gage_accuracy_mm"] / R3) ** 2 / 5)
    # prediction uncertainty: n = Est/Eal
    dn = 0.01
    cp2 = composite_props(b, h, ts, E_al, E_st * (1 + dn))
    dy_dn = (cp2["ybar"] - cp["ybar"]) / dn
    u_n_rel = math.hypot(ref["u_E_st_GPa"] / E_st, uE / E_al)
    dy_dts = (composite_props(b, h, ts + 0.01, E_al, E_st)["ybar"] - cp["ybar"]) / 0.01
    u_ybar_pred = math.sqrt((dy_dn * u_n_rel) ** 2 + (dy_dts * uts) ** 2)
    kB = np.array([f["kappa"] for f in fitsB])
    MmB = PB / 2 * a / 1e3
    _, slB, _, uslB, _ = linfit(kB[selB], MmB[selB])
    EI_meas = slB                                              # N·m²
    EI_pred = E_al * 1e9 * cp["I"] * 1e-12
    uEI_pred = EI_pred * math.sqrt((uE / E) ** 2 + (3 * uh / h) ** 2 + (0.5 * u_n_rel) ** 2)
    iB = int(np.argmax(PB))
    fB = fitsB[iB]
    eps_at = lambda y: (fB["a"] + fB["b"] * y) * 1e-6            # noqa: E731
    sig_st_bot = E_st * 1e3 * eps_at(0.0)
    sig_al_int = E_al * 1e3 * eps_at(ts)
    sig_st_int = E_st * 1e3 * eps_at(ts)
    sig_al_top = E_al * 1e3 * eps_at(H)
    MB = float(MmB[iB])
    pred = lambda y, n_: -n_ * MB * 1e3 * (y - cp["ybar"]) / cp["I"]   # noqa: E731  MPa (I mm^4)
    # equilibrium check with the measured strain fit: N = Σ E ∫ eps dA
    N_st = E_st * 1e3 * b * ts * eps_at(ts / 2)
    N_al = E_al * 1e3 * b * h * eps_at(ts + h / 2)
    C_al = E_al * 1e3 * b * 0.5 * max(0.0, H - fB["yNA"]) * eps_at(H)    # compressive resultant (triangle above NA)
    # homogeneous (no steel) prediction for comparison (M1c)
    ybar_hom = H / 2                                           # if the strip were aluminum too
    out["B"] = dict(H=H, yNA=ynaB_mean, u_yNA=u_ynaB, ybar_pred=cp["ybar"], u_ybar_pred=u_ybar_pred, n=cp["n"], I_t_mm4=cp["I"],
                    EI_meas=EI_meas, uEI_meas=uslB, EI_pred=EI_pred, uEI_pred=uEI_pred, P=float(PB[iB]), M=MB,
                    sig_st_bot=sig_st_bot, sig_al_int=sig_al_int, sig_st_int=sig_st_int, sig_al_top=sig_al_top,
                    pred_st_bot=pred(0.0, cp["n"]), pred_al_int=pred(ts, 1.0), pred_st_int=pred(ts, cp["n"]), pred_al_top=pred(H, 1.0),
                    N_resid_frac=(N_st + N_al) / abs(C_al), rms=fB["rms"], ybar_homog=ybar_hom, EI_alone=E_al * 1e9 * b * h ** 3 / 12 * 1e-12,
                    stiff_gain=EI_meas / (E_al * 1e9 * b * h ** 3 / 12 * 1e-12))
    # ------------------------------------------------------------------ Part C (plastic)
    C = data["C"]
    fitsC = profile_fits(C, m["yA_mm"], h)
    PC = C["load_N"]
    MC = PC / 2 * a / 1e3
    kC = np.array([f["kappa"] for f in fitsC])
    imax = int(np.argmax(PC))
    Emeas = E * 1e9
    sY = ref["sY_al_MPa"] * 1e6
    bm, hm = b * 1e-3, h * 1e-3
    MY = sY * bm * hm ** 2 / 6
    kY = sY / (Emeas * hm / 2)
    epp = [epp_rect_M(bm, hm, Emeas, sY, kk) for kk in kC[: imax + 1]]
    mats = {"al": dict(law="ro", E=Emeas, sY=sY, m=ref["m_RO"])}
    layers = [(0.0, hm, bm, "al")]
    ro = [section_moment(layers, mats, kk)[0] if kk > 0 else 0.0 for kk in kC[: imax + 1]]
    kmax, Mmax = float(kC[imax]), float(MC[imax])
    emax = kmax * hm / 2
    sig_actual = sigma_of(mats["al"], emax)
    sig_flex = Mmax * (hm / 2) / (bm * hm ** 3 / 12)
    k_res_meas = float(kC[-1])
    k_res_pred = kmax - Mmax / (Emeas * bm * hm ** 3 / 12)
    u_kres_pred = Mmax / (Emeas * bm * hm ** 3 / 12) * math.sqrt((uE / E) ** 2 + uI_rel ** 2 + (ua / a) ** 2)
    res_surf = sig_actual - sig_flex                           # tension side, after unloading (MPa*1e6)
    nu_eff = -(C["strain_transverse_top_ue"][imax] / C["strain_top_ue"][imax])
    # straightedge gap after Part C: (i) permanent curvature confined to the middle region; (ii) kappa_p(x) along the
    # whole bar from the measured loading curve kappa(M), integrated twice (Appendix D.9)
    half, m_mid = m["bar_length_mm"] / 2e3, (L - 2 * a) / 2e3                 # m
    gap_mid = k_res_meas * m_mid * (half - m_mid / 2)
    u_gap_mid = gap_mid * math.hypot(u_kres_pred / k_res_pred, 0.5 / (L - 2 * a))
    Mup, kup = np.r_[0.0, MC[1: imax + 1]], np.r_[0.0, kC[1: imax + 1]]
    xs = np.linspace(-(half - L / 2e3), half + L / 2e3, 1401)
    Lm, am = L / 1e3, a / 1e3
    Mx = np.array([0.0 if (x < 0 or x > Lm) else Mmax / am * min(x, am, Lm - x) for x in xs])
    kp = np.interp(Mx, Mup, kup) - Mx / (Emeas * bm * hm ** 3 / 12)
    th = np.concatenate([[0], np.cumsum((kp[1:] + kp[:-1]) / 2 * np.diff(xs))])
    w = np.concatenate([[0], np.cumsum((th[1:] + th[:-1]) / 2 * np.diff(xs))])
    gap_data = float((w[0] + (w[-1] - w[0]) * (xs - xs[0]) / (xs[-1] - xs[0]) - w).max())
    x_yield = 2 * MY / (Mmax / am * 2) if Mmax > MY else None
    out["C"] = dict(P=[float(x) for x in PC], M=[float(x) for x in MC], kappa=[float(x) for x in kC], yNA=[float(f["yNA"]) for f in fitsC],
                    rms=[float(f["rms"]) for f in fitsC], M_epp=[float(x) for x in epp], M_ro=[float(x) for x in ro],
                    MY=MY, Mp=1.5 * MY, kY=kY, kmax=kmax, Mmax=Mmax, eps_max=emax, sig_actual=sig_actual / 1e6, sig_flex=sig_flex / 1e6,
                    flex_over=(sig_flex / sig_actual - 1), k_res_meas=k_res_meas, k_res_pred=k_res_pred, u_k_res_pred=u_kres_pred,
                    M_epp_max=float(epp[-1]), M_ro_max=float(ro[-1]), res_surf=res_surf / 1e6, nu_eff=float(nu_eff),
                    rms_max=float(fitsC[imax]["rms"]), rms_A20=out["A"]["rms20"], eps_x150_max=float(C["strain_bottom_x150_ue"][imax]),
                    eps_x150_res=float(C["strain_bottom_x150_ue"][-1]), gap_meas=m["straightedge_gap_mm"],
                    u_gap_meas=math.hypot(m["feeler_resolution_mm"] / math.sqrt(12), 0.02), gap_mid=gap_mid * 1e3, u_gap_mid=u_gap_mid * 1e3,
                    gap_data=gap_data * 1e3, x_yield=x_yield * 1e3)
    out["D"] = design(E, ref)
    return out


CATALOG = [  # generic sections, mm: (name, kind, h, b, tf_or_t, tw)
    ("I-100", "I", 100, 55, 5.7, 4.1), ("I-120", "I", 120, 64, 6.3, 4.4), ("I-140", "I", 140, 73, 6.9, 4.7),
    ("I-160", "I", 160, 82, 7.4, 5.0), ("I-180", "I", 180, 91, 8.0, 5.3), ("I-200", "I", 200, 100, 8.5, 5.6),
    ("RT-100x50x4", "T", 100, 50, 4.0, None), ("RT-120x60x5", "T", 120, 60, 5.0, None), ("RT-150x100x5", "T", 150, 100, 5.0, None),
    ("RT-200x100x6", "T", 200, 100, 6.0, None),
]


def catalog_props():
    out = []
    for name, kind, h, b, t, tw in CATALOG:
        if kind == "I":
            pr = ibeam_props(b, h, t, tw)
            A = 2 * b * t + (h - 2 * t) * tw
        else:
            pr = dict(I=(b * h ** 3 - (b - 2 * t) * (h - 2 * t) ** 3) / 12)
            pr["S"] = pr["I"] / (h / 2)
            A = b * h - (b - 2 * t) * (h - 2 * t)
        out.append(dict(name=name, h=h, b=b, A=A, I=pr["I"], S=pr["S"]))
    return out


def design(E_al_meas, ref):
    """D1: 3.0 m simply supported; 3.0 kN/m + 5.0 kN at midspan; FS 1.67 on yield; deflection <= L/240."""
    L, w, P, FS = 3000.0, 3.0, 5.0e3, 1.67                     # mm, N/mm, N
    Mmax = w * L ** 2 / 8 + P * L / 4                          # N·mm
    mats = dict(steel=dict(E=ref["E_st_GPa"] * 1e3, sY=ref["sY_st_MPa"] - 2 * ref["u_sY_st_MPa"], rho=7870, price=2.20),
                al=dict(E=E_al_meas * 1e3, sY=ref["sY_al_MPa"] - 2 * ref["u_sY_al_MPa"], rho=2700, price=6.50))
    cat = catalog_props()
    res = dict(M_Nm=Mmax / 1e3, dmax_mm=L / 240, rows={})
    for k, mt in mats.items():
        sall = mt["sY"] / FS
        S_req = Mmax / sall
        I_req = (5 * w * L ** 4 / 384 + P * L ** 3 / 48) / (mt["E"] * L / 240)
        rows = []
        for c in cat:
            sig = Mmax / c["S"]
            d = 5 * w * L ** 4 / (384 * mt["E"] * c["I"]) + P * L ** 3 / (48 * mt["E"] * c["I"])
            mass = c["A"] * 1e-6 * mt["rho"]                         # kg/m
            rows.append(dict(name=c["name"], S=c["S"], I=c["I"], mass=mass, cost=mass * L / 1e3 * mt["price"], sigma=sig, defl=d,
                             ok=bool(sig <= sall and d <= L / 240)))
        okr = [r for r in rows if r["ok"]]
        best = min(okr, key=lambda r: r["mass"]) if okr else None
        res["rows"][k] = dict(sY_lo=mt["sY"], s_allow=sall, S_req=S_req, I_req=I_req, table=rows, best=best)
    return res


def main():
    data = load(Path(sys.argv[1]) if len(sys.argv) > 1 else LAB / "sample_data.csv")
    m = json.loads((Path(sys.argv[2]) if len(sys.argv) > 2 else HERE / "specimen_measurements.json").read_text())
    r = analyze(data, m)
    (HERE / "results.json").write_text(json.dumps(r, indent=1, default=float))
    for k in ("geom", "A", "B"):
        print(f"=== {k} ===")
        for kk, vv in r[k].items():
            if isinstance(vv, (int, float)):
                print(f"  {kk:16s} {vv:.6g}")
    c = r["C"]
    print("=== C ===", {k: round(v, 5) for k, v in c.items() if isinstance(v, float)})
    print("=== D ===", {k: (v["best"]["name"] if v["best"] else None, round(v["S_req"]), round(v["I_req"])) for k, v in r["D"]["rows"].items()})


if __name__ == "__main__":
    main()

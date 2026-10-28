"""Lab 5 analysis: every number in the instructor key comes from this script.

    python3 lab05_analysis.py [data.csv] [measurements.json]   ->  results.json + printed summary
"""
import csv
import json
import math
import sys
from pathlib import Path

import numpy as np
from scipy import optimize

import lab05_model as LM

HERE = Path(__file__).resolve().parent
LAB = HERE.parent
R3 = math.sqrt(3)


def load(path):
    rows = list(csv.DictReader(open(path, newline="")))
    f = lambda v: float(v) if v.strip() else np.nan  # noqa: E731
    return [{k: (v if k in ("part", "config") else f(v)) for k, v in r.items()} for r in rows]


def sel(rows, part, config, span=None):
    return [r for r in rows if r["part"] == part and r["config"] == config and (span is None or abs(r["span_mm"] - span) < 1e-6)]


def linfit(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    n = len(x)
    A = np.vstack([np.ones(n), x]).T
    coef, *_ = np.linalg.lstsq(A, y, rcond=None)
    res = y - A @ coef
    s2 = res @ res / max(n - 2, 1)
    cov = s2 * np.linalg.inv(A.T @ A)
    return coef[0], coef[1], math.sqrt(cov[0, 0]), math.sqrt(cov[1, 1]), cov


def mean_u(vals, acc):
    v = np.array(vals, float)
    return float(v.mean()), math.sqrt((v.std(ddof=1) / math.sqrt(len(v))) ** 2 + (acc / R3) ** 2)


def loading(rr):
    """Loading steps with load (exclude the final return to zero)."""
    Ps = [r["load_N"] for r in rr]
    imax = int(np.argmax(Ps))
    return [r for r in rr[: imax + 1] if r["load_N"] > 100]


def gamma(r, g):
    return (r[f"{g}_p45_ue"] - r[f"{g}_m45_ue"]) * 1e-6        # gamma_xy = eps(+45) - eps(-45)


def analyze(rows, m):
    ref = m["reference"]
    u_gf = m["gage_factor_tolerance_pct"] / 100 / R3
    u_P = m["load_cell_accuracy_pct"] / 100 / R3
    G = ref["G_al_GPa"] * 1e9
    uG = ref["u_G_al_GPa"] / ref["G_al_GPa"]
    E_ref, nu = ref["E_al_GPa"] * 1e9, ref["nu_al"]
    out = {}
    # ------------------------------------------------------------------ Part A: rectangle, upright and flat
    bA, ubA = mean_u(m["barA"]["b_mm"], m["caliper_accuracy_mm"])
    hA, uhA = mean_u(m["barA"]["h_mm"], m["caliper_accuracy_mm"])
    A_mm2 = bA * hA
    uA = math.hypot(ubA / bA, uhA / hA)
    out["A"] = dict(b=bA, ub=ubA, h=hA, uh=uhA, A=A_mm2)
    for cfg, b, h in (("upright", bA, hA), ("flat", hA, bA)):
        rr = loading(sel(rows, "A", cfg))
        V = np.array([r["load_N"] / 2 for r in rr])
        gF = np.array([-gamma(r, "gA") for r in rr])            # magnitudes (gamma_xy < 0 in the left shear span)
        gB = np.array([-gamma(r, "gB") for r in rr])
        tau = G * (gF + gB) / 2 / 1e6                            # MPa
        _, sl, _, usl, _ = linfit(V, tau)                        # MPa per N
        elem = 1.5 / A_mm2                                       # MPa per N
        ratio = sl / elem
        u_ratio = ratio * math.sqrt((usl / sl) ** 2 + uG ** 2 + u_gf ** 2 + u_P ** 2 + uA ** 2)
        pred = LM.rect_edge_ratio_xseries(b * 1e-3, h * 1e-3, nu)
        dpdnu = (LM.rect_edge_ratio_xseries(b * 1e-3, h * 1e-3, nu + 0.001) - pred) / 0.001
        u_pred = math.hypot(dpdnu * ref["u_nu_al"], (LM.rect_edge_ratio_xseries(b * 1e-3 * 1.001, h * 1e-3, nu) - pred) / 0.001 * ubA / bA)
        twist = float((gF[-1] - gB[-1]) / (gF[-1] + gB[-1]))
        out["A"][cfg] = dict(b=b, h=h, bh=b / h, slope=sl, u_slope_stat=usl, elem=elem, ratio=ratio, u_ratio=u_ratio, pred=pred, u_pred=u_pred,
                             agree_lim=2 * math.hypot(u_ratio, u_pred), V_max=float(V[-1]), tau_max=float(tau[-1]),
                             tau_elem_max=float(elem * V[-1]), gamma_max_ue=float((gF[-1] + gB[-1]) / 2 * 1e6), twist_frac=twist,
                             n=len(rr), err_elem=pred - 1)
    # ------------------------------------------------------------------ Part B: I-beam
    ib = m["ibeam"]
    H, uH = mean_u(ib["H_mm"], m["caliper_accuracy_mm"])
    B, uB = mean_u(ib["B_mm"], m["caliper_accuracy_mm"])
    tf, utf = mean_u(ib["tf_mm"], m["caliper_accuracy_mm"])
    tw, utw = mean_u(ib["tw_mm"], m["micrometer_accuracy_mm"])
    lay = LM.ibeam(B * 1e-3, H * 1e-3, tf * 1e-3, tw * 1e-3)
    pr = LM.props(lay)
    fs = LM.form_factor(lay)
    I_mm4, A_mm2 = pr["I"] * 1e12, pr["A"] * 1e6
    # sensitivity of I to the dimensions (finite differences)
    def Ifun(B_, H_, tf_, tw_):
        return LM.props(LM.ibeam(B_ * 1e-3, H_ * 1e-3, tf_ * 1e-3, tw_ * 1e-3))["I"] * 1e12
    dI = [(Ifun(B + d * (k == 0), H + d * (k == 1), tf + d * (k == 2), tw + d * (k == 3)) - I_mm4) / d for k, d in enumerate([1e-3] * 4)]
    uI = math.sqrt(sum((di * ui) ** 2 for di, ui in zip(dI, (uB, uH, utf, utw)))) / I_mm4
    out["B"] = dict(H=H, uH=uH, B=B, uB=uB, tf=tf, utf=utf, tw=tw, utw=utw, I=I_mm4, uI=uI, A=A_mm2, fs=fs, A_web=(H - 2 * tf) * tw,
                    fs_approx=A_mm2 / ((H - 2 * tf) * tw))
    rr = loading(sel(rows, "B", "web"))
    V = np.array([r["load_N"] / 2 for r in rr])
    web = []
    for j, (g1, g2) in enumerate((("gA", "gB"), ("gC", "gD"), ("gE", "gF"))):
        gm = np.array([-(gamma(r, g1) + gamma(r, g2)) / 2 for r in rr])
        tau = G * gm / 1e6
        _, sl, _, usl, _ = linfit(V, tau)
        y = ib["gage_height_mm"][j] - H / 2
        Q = LM.Q_at(lay, pr["ybar"] + y * 1e-3, pr["ybar"]) * 1e9           # mm^3
        pred = Q / (I_mm4 * tw)                                                # MPa per N
        u_pred = pred * math.hypot(uI, utw / tw)
        u_sl = sl * math.sqrt((usl / sl) ** 2 + uG ** 2 + u_gf ** 2 + u_P ** 2)
        diff_sides = float(np.mean([(gamma(r, g1) - gamma(r, g2)) / (gamma(r, g1) + gamma(r, g2)) for r in rr[-1:]]))
        web.append(dict(y=y, Q=Q, slope=sl, u_slope=u_sl, pred=pred, u_pred=u_pred, ratio=sl / pred, agree_lim=2 * math.hypot(u_sl, u_pred),
                        tau_max=float(tau[-1]), side_diff=diff_sides))
    out["B"]["web"] = web
    out["B"]["tau_Aweb_per_N"] = 1 / ((H - 2 * tf) * tw)
    # deflection vs span
    spans = ib["spans_mm"]
    C, uC = [], []
    for L in spans:
        rd = loading(sel(rows, "B", "deflection", L))
        _, sl, _, usl, _ = linfit([r["load_N"] for r in rd], [r["defl_mm"] for r in rd])
        C.append(sl)
        uC.append(usl)
    C = np.array(C)                                                   # mm/N
    Ls = np.array(spans)
    yv = C / Ls                                                       # 1/N
    a0, a1, ua0, ua1, cov = linfit(Ls ** 2, yv)                       # y = a0 + a1 L^2
    E_fit = 1 / (48 * I_mm4 * a1) / 1e3                               # GPa (N/mm^2 -> GPa)
    G_fit = fs / (4 * A_mm2 * a0) / 1e3
    u_gain = m["lvdt_accuracy_pct"] / 100 / R3
    uE_fit = E_fit * math.sqrt((ua1 / a1) ** 2 + uI ** 2 + u_gain ** 2 + u_P ** 2)
    ufs = 0.0
    uG_fit = G_fit * math.sqrt((ua0 / a0) ** 2 + (math.hypot(uB / B, uH / H) * 0.3) ** 2 + u_gain ** 2 + u_P ** 2 + ufs ** 2)
    # predicted compliances from reference E and G
    Cp = np.array([LM.timoshenko_delta(1.0, L * 1e-3, E_ref, G, pr["I"], pr["A"], fs) for L in spans])
    frac_meas = a0 * Ls / C
    frac_pred = Cp[:, 1] / Cp.sum(axis=1)
    L5_fit = math.sqrt(19 * a0 / a1)
    L5_pred = math.sqrt(19 * fs * 48 * E_ref * pr["I"] / (4 * G * pr["A"])) * 1e3
    rows_d = [dict(L=float(L), C=float(c), uC=float(u), C_pred=float(cp.sum() * 1e3), bend_pred=float(cp[0] * 1e3), frac_meas=float(fm), frac_pred=float(fp),
                   EB_err=float(1 - cp[0] / cp.sum())) for L, c, u, cp, fm, fp in zip(spans, C, uC, Cp, frac_meas, frac_pred)]
    out["B"]["defl"] = dict(rows=rows_d, a0=a0, a1=a1, ua0=ua0, ua1=ua1, E=E_fit, uE=uE_fit, G=G_fit, uG=uG_fit, L5_fit=L5_fit, L5_pred=L5_pred,
                            h_ratio_fit=L5_fit / H, h_ratio_pred=L5_pred / H, E_lim=2 * math.hypot(uE_fit, ref["u_E_al_GPa"]),
                            G_lim=2 * math.hypot(uG_fit, ref["u_G_al_GPa"]))
    # ------------------------------------------------------------------ Part C: layered beams
    ly = m["layered"]
    bL, ubL = mean_u(ly["b_mm"], m["caliper_accuracy_mm"])
    t1, ut1 = mean_u(ly["t_top_mm"], m["caliper_accuracy_mm"])
    t2, ut2 = mean_u(ly["t_bot_mm"], m["caliper_accuracy_mm"])
    Lc = ly["span_mm"] * 1e-3
    geom = LM.two_layer(bL * 1e-3, t1 * 1e-3, t2 * 1e-3, E_ref)
    Ac = bL * (t1 + t2) * 1e-6
    dsh = 1.2 * Lc / (4 * G * Ac)                                     # m/N, shear term (small)
    res = {}
    for cfg in ("loose", "bolted", "bonded"):
        rr = loading(sel(rows, "C", cfg))
        P = np.array([r["load_N"] for r in rr])
        _, sl, _, usl, _ = linfit(P, [r["defl_mm"] * 1e-3 for r in rr])
        _, ss, _, uss, _ = linfit(P, [r["slip_mm"] * 1e-3 for r in rr])
        Cb = sl - dsh
        EI = Lc ** 3 / (48 * Cb)
        uEI = EI * math.sqrt((usl / sl) ** 2 + u_gain ** 2 + u_P ** 2 + (3 * m["span_accuracy_mm"] / R3 / ly["span_mm"]) ** 2)
        res[cfg] = dict(C=sl, uC=usl, Cb=Cb, EI=EI, uEI=uEI, slip=ss, uslip=uss, Pmax=float(P[-1]), slip_max=float(rr[-1]["slip_mm"]), defl_max=float(rr[-1]["defl_mm"]))
    EI0, EIf = geom["EI0"], geom["EIfull"]
    uEI0 = math.sqrt((ubL / bL) ** 2 + (3 * ut1 / t1) ** 2 / 2 + (ref["u_E_al_GPa"] / ref["E_al_GPa"]) ** 2)
    res["pred"] = dict(EI0=EI0, EIfull=EIf, ratio_full=EIf / EI0, uEI_rel=uEI0, slip_loose=geom["r"] * Lc ** 2 / (16 * EI0), dsh=dsh)
    for cfg in ("loose", "bolted", "bonded"):
        res[cfg]["ratio"] = res[cfg]["EI"] / res["loose"]["EI"]
        res[cfg]["eta"] = (res[cfg]["EI"] - EI0) / (EIf - EI0)
    # fit kb (bolted): discrete springs, and the smeared closed form (k = kb/s)
    bolts = [x * 1e-3 for x in ly["bolts_mm"]]
    Cb_b = res["bolted"]["Cb"]
    ld1 = dict(kind="point", P=1.0)
    f_disc = lambda lk: LM.bolts_shoot(geom, Lc, ld1, bolts, 10 ** lk)["delta"] - Cb_b   # noqa: E731
    kb_disc = 10 ** optimize.brentq(f_disc, 5, 10, xtol=1e-10)
    sdisc = LM.bolts_shoot(geom, Lc, ld1, bolts, kb_disc)
    spacing = (bolts[1] - bolts[0])

    def smeared_delta(k):
        return newmark_point(geom, Lc, k)[0]
    kb_sm = 10 ** optimize.brentq(lambda lk: smeared_delta(10 ** lk / spacing) - Cb_b, 5, 10, xtol=1e-10)
    # uncertainty of kb from the deflection uncertainty (finite difference)
    dC = res["bolted"]["Cb"] * math.sqrt((res["bolted"]["uC"] / res["bolted"]["C"]) ** 2 + u_gain ** 2)
    kb_hi = 10 ** optimize.brentq(lambda lk: LM.bolts_shoot(geom, Lc, ld1, bolts, 10 ** lk)["delta"] - (Cb_b - dC), 5, 10, xtol=1e-10)
    u_kb = abs(kb_hi - kb_disc)
    slip_pred = abs(sdisc["slip0"])
    Pmax_b = res["bolted"]["Pmax"]
    Vb = Pmax_b / 2
    ybar = (bL * t2 * t2 / 2 + bL * t1 * (t2 + t1 / 2)) / (bL * (t1 + t2))
    Qint = bL * t1 * (t2 + t1 / 2 - ybar)                            # mm^3: top layer about the composite NA
    Icomp = EIf / E_ref * 1e12
    q_beer = Vb * Qint / Icomp                                      # N/mm
    res["kb"] = dict(kb_disc=kb_disc, kb_smeared=kb_sm, u_kb=u_kb, slip_pred_per_N=slip_pred, slip_meas_per_N=res["bolted"]["slip"],
                     u_slip_meas=res["bolted"]["uslip"], forces_max=[abs(f) * Pmax_b for f in sdisc["forces"]], F_beer=q_beer * spacing * 1e3,
                     q_beer=q_beer, spacing_mm=spacing * 1e3, smeared_vs_disc=kb_sm / kb_disc - 1)
    # bonded: glue shear stress at max load
    Pmax_g = res["bonded"]["Pmax"]
    res["bonded"]["tau_glue"] = (Pmax_g / 2) * Qint / (Icomp * bL)
    res["loose"]["slip_pred_per_N"] = res["pred"]["slip_loose"]
    out["C"] = dict(b=bL, ub=ubL, t1=t1, ut1=ut1, t2=t2, ut2=ut2, L=Lc * 1e3, **res)
    out["D"] = design(res["kb"]["kb_disc"], E_ref, G)
    return out


def newmark_point(geom, L, k):
    """Closed-form partial interaction, simple span, central point load P = 1 (retyped from the handout's Appendix D)."""
    EAs, EI0, r = geom["EAs"], geom["EI0"], geom["r"]
    a2 = k * (1 / EAs + r * r / EI0)
    a = math.sqrt(a2)
    be = k * r / EI0
    z = a * L / 2
    if z < 0.05:
        d = (L ** 3 / 48 - r * be / 2 * ((2 / 15) * (L / 2) ** 5 - (17 / 315) * (L / 2) ** 7 * a2)) / EI0
    else:
        d = ((1 - r * be / a2) * L ** 3 / 48 + r * be / 2 * (L / (2 * a2 * a2) - math.tanh(z) / (a2 * a2 * a))) / EI0
    s0 = r / (2 * EI0 * a2) * (1 - 1 / math.cosh(min(z, 700))) if z > 1e-8 else r * L ** 2 / (16 * EI0)
    return d, s0


def design(kb6, E, G):
    """D1: two 6061-T6 bars 100 wide x 50 deep, stacked; span 2.4 m; w = 8 kN/m; M10 bolts, F_allow = 10 kN each
    (Beer's q s); midspan deflection <= L/300 by the discrete-bolt model with kb(M10) = (10/6) kb(M6 measured)."""
    b, t, L, w, Fa = 0.100, 0.050, 2.4, 8.0e3, 10.0e3
    kb = kb6 * 10 / 6
    geom = LM.two_layer(b, t, t, E)
    Icomp = b * (2 * t) ** 3 / 12
    Q = b * t * t / 2
    d_full = 5 * w * L ** 4 / (384 * geom["EIfull"])
    d_loose = 5 * w * L ** 4 / (384 * geom["EI0"])
    V = lambda x: w * (L / 2 - x)  # noqa: E731
    load = dict(kind="udl", w=w)

    def pattern(s1, s2, e):
        xs, x = [], s1 / 2
        while x < L / 2 - 1e-9:
            xs.append(x)
            x += s1 if x + 1e-9 < e else s2
        half = list(xs)
        full = half + [L - x_ for x_ in reversed(half) if abs(L - x_ - x_) > 1e-9]
        return sorted(full), half

    def check(s1, s2, e):
        full, half = pattern(s1, s2, e)
        Fbeer = []
        for x_ in half:
            s_here = s1 if x_ + 1e-9 < e else s2
            Fbeer.append(abs(V(x_)) * Q / Icomp * s_here)
        sol = LM.bolts_shoot(geom, L, load, full, kb)
        return dict(n=len(full), Fbeer=max(Fbeer), Fmodel=max(abs(f) for f in sol["forces"]), delta=sol["delta"], ratio=sol["delta"] / d_full,
                    ok=bool(max(Fbeer) <= Fa and sol["delta"] <= L / 300), xs=full)
    best = {}
    for s in np.arange(300, 20, -5) / 1e3:                       # uniform: the largest spacing that passes
        c = check(s, s, L)
        if c["ok"]:
            best["uniform"] = dict(s1=float(s), **{k: v for k, v in c.items() if k != "xs"})
            break
    cand = None                                                   # stepped: end zones of length e at s1, middle at s2
    for e in (0.3, 0.45, 0.6, 0.8):
        for s1 in np.arange(150, 20, -5) / 1e3:
            if check(s1, s1, e)["Fbeer"] > Fa:
                continue
            for s2 in np.arange(500, 20, -5) / 1e3:
                if s2 < s1:
                    break
                c = check(s1, s2, e)
                if c["ok"]:
                    if cand is None or c["n"] < cand["n"] or (c["n"] == cand["n"] and c["delta"] < cand["delta"]):
                        cand = dict(e=e, s1=float(s1), s2=float(s2), **{k: v for k, v in c.items() if k != "xs"})
                    break
    best["stepped"] = cand
    q0 = V(0) * Q / Icomp
    return dict(kb_M10=kb, d_full=d_full, d_loose=d_loose, d_allow=L / 300, q0=q0, s_max_end=Fa / q0, Vmax=V(0), Mmax=w * L ** 2 / 8,
                sigma=w * L ** 2 / 8 * t / Icomp, tau_int=V(0) * Q / (Icomp * b), best=best)


def main():
    rows = load(Path(sys.argv[1]) if len(sys.argv) > 1 else LAB / "sample_data.csv")
    m = json.loads((Path(sys.argv[2]) if len(sys.argv) > 2 else HERE / "specimen_measurements.json").read_text())
    r = analyze(rows, m)
    (HERE / "results.json").write_text(json.dumps(r, indent=1, default=float))
    for cfg in ("upright", "flat"):
        a = r["A"][cfg]
        print(cfg, {k: round(a[k], 5) for k in ("bh", "ratio", "u_ratio", "pred", "agree_lim", "twist_frac")})
    for w_ in r["B"]["web"]:
        print("web", {k: round(w_[k], 6) for k in ("y", "slope", "pred", "ratio", "agree_lim", "side_diff")})
    d = r["B"]["defl"]
    print("defl", {k: round(d[k], 5) for k in ("E", "uE", "G", "uG", "L5_fit", "L5_pred")}, "fs", round(r["B"]["fs"], 4))
    for row in d["rows"]:
        print("  ", {k: round(v, 5) for k, v in row.items()})
    c = r["C"]
    for cfg in ("loose", "bolted", "bonded"):
        print(cfg, {k: round(v, 6) if isinstance(v, float) else v for k, v in c[cfg].items()})
    print("pred", c["pred"], "\nkb", c["kb"])
    print("D", json.dumps(r["D"], default=float)[:800])


if __name__ == "__main__":
    main()

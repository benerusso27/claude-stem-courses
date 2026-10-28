"""Lab 3 analysis: every number in the instructor key comes from this script.

    python3 lab03_analysis.py [data.csv] [measurements.json]   ->  results.json + printed summary
"""
import csv
import json
import math
import sys
from pathlib import Path

import numpy as np
from scipy import optimize

HERE = Path(__file__).resolve().parent
LAB = HERE.parent
R3 = math.sqrt(3)
DEG = math.pi / 180


def load(path):
    rows = list(csv.DictReader(open(path, newline="")))
    out = {}
    for key in ("steel", "al", "ci"):
        rr = [r for r in rows if r["specimen"] == key]
        f = lambda c: np.array([float(r[c]) if r[c].strip() else np.nan for r in rr])  # noqa: E731
        out[key] = dict(t=f("time_s"), T=f("torque_Nm"), tr=f("troptometer_deg") * DEG, head=f("head_deg") * DEG)
    return out


def linfit(x, y):
    n = len(x)
    A = np.vstack([np.ones(n), x]).T
    coef, *_ = np.linalg.lstsq(A, y, rcond=None)
    res = y - A @ coef
    s2 = res @ res / (n - 2)
    cov = s2 * np.linalg.inv(A.T @ A)
    return coef[0], coef[1], math.sqrt(cov[0, 0]), math.sqrt(cov[1, 1])


def epp_T(c, G, tauY, theta):
    """Elastic–perfectly plastic torque of a solid shaft (Beer Sec. 3.7), vectorized."""
    theta = np.asarray(theta, float)
    TY = tauY * math.pi * c ** 3 / 2
    thY = tauY / (G * c)
    x = np.clip(thY / np.maximum(theta, 1e-30), 0, 1)
    return np.where(theta <= thY, TY * theta / thY, 4 / 3 * TY * (1 - x ** 3 / 4))


def analyze(data, m):
    out = {}
    L = m["L_gage_mm"] * 1e-3
    Lr = m["L_reduced_mm"] * 1e-3
    uL = m["u_L_gage_mm"] / m["L_gage_mm"]
    u_T = m["torque_accuracy_pct"] / 100 / R3
    u_tr = m["troptometer_accuracy_pct"] / 100 / R3
    ref = m["reference"]
    for key in ("steel", "al", "ci"):
        D = data[key]
        dr = np.array(m["d_mm"][key])
        d = dr.mean() * 1e-3
        ud = math.hypot(dr.std(ddof=1) / math.sqrt(len(dr)), m["micrometer_accuracy_mm"] / R3) * 1e-3
        c = d / 2
        J = math.pi * c ** 4 / 2
        uJ = 4 * ud / d
        r = dict(d_mm=d * 1e3, ud_mm=ud * 1e3, J_mm4=J * 1e12, uJ_rel=uJ, c_mm=c * 1e3)
        T, tr, head = D["T"], D["tr"], D["head"]
        imax = int(np.argmax(T))
        if key != "ci":
            # ---------------- G from the troptometer, initial elastic loading
            first_unload = np.where(np.diff(tr) < 0)[0]
            n_up = first_unload[0] + 1 if len(first_unload) else int(np.nanargmax(tr)) + 1
            idx = np.arange(len(T))
            el = (idx < n_up) & (T > 0.3) & (T < 4.0) & ~np.isnan(tr)
            a0, k, _, uk = linfit(tr[el], T[el])          # N·m per rad over the gage
            G = k * L / J
            uG_rel = math.sqrt((uk / k) ** 2 + uJ ** 2 + uL ** 2 + u_T ** 2 + u_tr ** 2)
            E_ref, uE_ref = ref[f"E_{key}_GPa"], ref[f"u_E_{key}_GPa"]
            nu_ref, unu_ref = ref[f"nu_{key}"], ref[f"u_nu_{key}"]
            G_pred = E_ref / (2 * (1 + nu_ref))
            uG_pred = G_pred * math.hypot(uE_ref / E_ref, unu_ref / (1 + nu_ref))
            r.update(G_GPa=G / 1e9, uG_GPa=G / 1e9 * uG_rel, uG_rel=uG_rel, G_stat_rel=uk / k, n_G=int(el.sum()), G_int_Nm=a0,
                     G_pred_GPa=G_pred, uG_pred_GPa=uG_pred, G_agree_lim=2 * math.hypot(G / 1e9 * uG_rel, uG_pred))
            # ---------------- elastic–perfectly-plastic fit for tau_Y on the initial loading branch
            th = tr / L
            thY_guess = 0.002 / c
            fit = (idx < n_up) & ~np.isnan(tr) & (th > 0.5 * thY_guess)
            def sse(tauY):
                return float(np.sum((T[fit] - epp_T(c, G, tauY, th[fit])) ** 2))
            res = optimize.minimize_scalar(sse, bounds=(50e6, 400e6), method="bounded", options=dict(xatol=1e3))
            tauY = res.x
            resid = T[fit] - epp_T(c, G, tauY, th[fit])
            # uncertainty: statistical from curvature of SSE, plus area and torque calibration (tauY ∝ T/c³)
            h = 1e5
            curv = (sse(tauY + h) - 2 * sse(tauY) + sse(tauY - h)) / h ** 2
            s2 = res.fun / (fit.sum() - 1)
            u_stat = math.sqrt(2 * s2 / curv)
            u_tauY = tauY * math.sqrt((u_stat / tauY) ** 2 + (3 * ud / d) ** 2 + u_T ** 2)
            TY = tauY * J / c
            r.update(tauY_MPa=tauY / 1e6, u_tauY_MPa=u_tauY / 1e6, tauY_stat_MPa=u_stat / 1e6, TY_Nm=TY, Tp_Nm=4 / 3 * TY,
                     epp_rms_Nm=float(np.sqrt(np.mean(resid ** 2))), epp_maxdev_Nm=float(np.max(np.abs(resid))),
                     epp_maxdev_rel=float(np.max(np.abs(resid)) / TY), n_fit=int(fit.sum()),
                     tauY_from_tension_MPa=ref[f"sigY_{key}_MPa"] / R3, phiY_deg=tauY / (G * c) * L / DEG)
            # tauY from the 10° point only, assuming a flat plateau (fully plastic approximation)
            last_tr = int(np.where(~np.isnan(tr))[0][-1])
            th10 = th[last_tr]
            rY = tauY / (G * th10)
            r.update(T_at_tropt_off=float(T[last_tr]), phi_tropt_off_deg=float(tr[last_tr] / DEG),
                     T_epp_at_off=float(epp_T(c, G, tauY, th10)), rY_over_c_off=rY / c,
                     hardening_excess_rel=float(T[last_tr] / epp_T(c, G, tauY, th10) - 1))
            # ---------------- compliance from head vs troptometer (initial loading, toe taken up)
            cm = (idx < n_up) & ~np.isnan(tr) & (T > 1.5) & (th < tauY / (G * c))
            toe, Cm, utoe, uCm = linfit(T[cm], head[cm] - (Lr / L) * tr[cm])
            r.update(Cm_deg_per_Nm=Cm / DEG, uCm_deg_per_Nm=uCm / DEG, toe_deg=toe / DEG, utoe_deg=utoe / DEG,
                     head_slope_frac=float(Cm / (Cm + Lr / (J * G))))
            # ---------------- corrected twist from the head, ultimate and fracture
            th_head = (head - Cm * T - toe) / Lr
            gam = c * th_head
            last = len(T) - 2                                   # last row before the fracture row (torque ~ 0)
            TU = float(T[imax])
            RT = TU * c / J
            uRT = RT * math.sqrt(u_T ** 2 + (3 * ud / d) ** 2)
            tau_pl = 3 * TU / (2 * math.pi * c ** 3)
            r.update(TU_Nm=TU, RT_MPa=RT / 1e6, uRT_MPa=uRT / 1e6, tau_pl_MPa=tau_pl / 1e6, gamma_at_TU=float(gam[imax]),
                     gamma_f=float(gam[last]), phi_f_gage_rev=float(th_head[last] * L / (2 * math.pi)),
                     head_f_rev=float(head[last] / (2 * math.pi)), tauU_tension_MPa=None)
            # ---------------- Nadai: tau(gamma_s) = (3T + gamma dT/dgamma)/(2 pi c^3), on the head-corrected curve
            ok = (gam > 0.02) & (np.arange(len(T)) <= last) & (T > 0.5)
            g_ok, T_ok = gam[ok], T[ok]
            order = np.argsort(g_ok)
            g_ok, T_ok = g_ok[order], T_ok[order]
            lg, lT = np.log(g_ok), np.log(T_ok)
            nad = {}
            for gq in (0.05, 0.1, 0.2, 0.5, 1.0, 1.5):
                if gq > g_ok.max():
                    continue
                w = np.abs(lg - math.log(gq)) < 0.25
                if w.sum() < 4:
                    continue
                p = np.polyfit(lg[w] - math.log(gq), lT[w], 2)
                Tq, dlnT = math.exp(p[2]), p[1]                 # d lnT / d ln gamma at gq
                nad[str(gq)] = dict(T=Tq, slope=dlnT, tau_MPa=Tq * (3 + dlnT) / (2 * math.pi * c ** 3) / 1e6,
                                    tau_pl_MPa=3 * Tq / (2 * math.pi * c ** 3) / 1e6, tau_el_MPa=Tq * c / J / 1e6)
            r["nadai"] = nad
            # plastic work into the reduced section and the adiabatic temperature rise it could cause
            up_to = np.arange(len(T)) <= last
            phi_red = th_head[up_to] * Lr
            W = float(np.trapezoid(T[up_to], phi_red))
            rho_cp = dict(steel=(7870, 486), al=(2700, 896))[key]
            V = math.pi * c ** 2 * Lr
            r.update(W_J=W, V_mm3=V * 1e9, dT_adiabatic_K=W / (rho_cp[0] * rho_cp[1] * V), test_time_s=float(D["t"][last]))
            if key == "steel":
                # ---------------- unload–reload cycle
                iu = first_unload[0]
                thA, TA = th[iu], T[iu]
                dn = np.arange(iu, len(T))
                seg = dn[: int(np.argmax(np.diff(tr[dn]) > 0)) + 1]       # unloading branch
                i0 = seg[-1]
                phi_res_meas = tr[i0]
                phi_res_pred = thA * L - TA * L / (J * G)
                u_res_pred = math.hypot(TA * L / (J * G) * uG_rel, 0.01 * DEG / R3)
                ku = linfit(tr[seg][T[seg] > 1.0], T[seg][T[seg] > 1.0])[1]
                rY_A = tauY / (G * thA)
                res_surf = tauY - TA * c / J
                res_rY = tauY - TA * rY_A / J
                r.update(phiA_deg=thA * L / DEG, TA_Nm=TA, phi_res_meas_deg=phi_res_meas / DEG, phi_res_pred_deg=phi_res_pred / DEG,
                         u_phi_res_pred_deg=u_res_pred / DEG, phi_res_epp_ratio=float((thA * L - TA * L / (J * G)) / (tauY / (G * c) * L)),
                         unload_slope_rel=float(ku / k - 1), res_surf_MPa=res_surf / 1e6, res_rY_MPa=res_rY / 1e6, rY_A_mm=rY_A * 1e3)
        else:
            # ---------------- cast iron: brittle, no troptometer
            Tf = float(T[imax])
            RT = Tf * c / J
            uRT = RT * math.sqrt(u_T ** 2 + (3 * ud / d) ** 2)
            sig = ref["sigUT_ci_MPa"]
            r.update(Tf_Nm=Tf, RT_MPa=RT / 1e6, uRT_MPa=uRT / 1e6, sigUT_MPa=sig, u_sigUT_MPa=ref["u_sigUT_ci_MPa"],
                     RT_agree_lim=2 * math.hypot(uRT / 1e6, ref["u_sigUT_ci_MPa"]), head_f_deg=float(head[imax] / DEG))
        out[key] = r
    # compliance-corrected secant modulus for cast iron using the steel/aluminum mean compliance
    Cm = 0.5 * (out["steel"]["Cm_deg_per_Nm"] + out["al"]["Cm_deg_per_Nm"]) * DEG
    toe = 0.5 * (out["steel"]["toe_deg"] + out["al"]["toe_deg"]) * DEG
    D = data["ci"]
    c = out["ci"]["c_mm"] * 1e-3
    J = out["ci"]["J_mm4"] * 1e-12
    w = (D["T"] > 1.5) & (D["T"] < 5.0)
    k_head = linfit(D["T"][w], D["head"][w] - Cm * D["T"][w] - toe)[1]   # rad per N·m over the reduced length
    out["ci"]["G_secant_low_GPa"] = Lr / (J * k_head) / 1e9
    imax = int(np.argmax(D["T"]))
    thf = (D["head"][imax] - Cm * D["T"][imax] - toe) / Lr
    out["ci"]["gamma_f"] = c * thf
    out["ci"]["G_secant_f_GPa"] = out["ci"]["RT_MPa"] * 1e6 / (c * thf) / 1e9
    out["design"] = design(out)
    return out


def design(out):
    """D1 reference solutions: shaft transmitting P at n rpm, length Ls, fillet K, FS on shear yield, twist limit."""
    P, rpm, Ls, K, FS, phi_lim = 15e3, 1200.0, 1.50, 1.6, 2.0, 1.0 * DEG
    T = P / (2 * math.pi * rpm / 60)
    res = dict(T_Nm=T)
    for key, rho, cost in (("steel", 7870, 2.2), ("al", 2700, 6.5)):
        tau_lo = (out[key]["tauY_MPa"] - 2 * out[key]["u_tauY_MPa"]) * 1e6        # conservative: tau_Y - U
        tau_allow = tau_lo / FS / K
        G = out[key]["G_GPa"] * 1e9
        opts = {}
        for name, k_ratio in (("solid", 0.0), ("hollow_0.6", 0.6), ("hollow_0.8", 0.8)):
            fac = 1 - k_ratio ** 4
            d_str = (16 * T / (math.pi * tau_allow * fac)) ** (1 / 3)
            d_stiff = (32 * T * Ls / (math.pi * G * phi_lim * fac)) ** 0.25
            dreq = max(d_str, d_stiff)
            dpick = math.ceil(dreq * 1e3) / 1e3
            A = math.pi / 4 * dpick ** 2 * (1 - k_ratio ** 2)
            J = math.pi * dpick ** 4 * fac / 32
            opts[name] = dict(d_strength_mm=d_str * 1e3, d_stiffness_mm=d_stiff * 1e3, governs="twist" if d_stiff > d_str else "strength",
                              d_mm=dpick * 1e3, di_mm=dpick * k_ratio * 1e3, mass_kg=A * Ls * rho, cost=A * Ls * rho * cost,
                              tau_max_MPa=K * T * dpick / 2 / J / 1e6, phi_deg=T * Ls / (J * G) / DEG)
        res[key] = dict(tau_lo_MPa=tau_lo / 1e6, tau_allow_MPa=tau_allow / 1e6, opts=opts)
    return res


def main():
    data = load(Path(sys.argv[1]) if len(sys.argv) > 1 else LAB / "sample_data.csv")
    m = json.loads((Path(sys.argv[2]) if len(sys.argv) > 2 else HERE / "specimen_measurements.json").read_text())
    r = analyze(data, m)
    (HERE / "results.json").write_text(json.dumps(r, indent=1, default=float))
    for k, v in r.items():
        print(f"=== {k} ===")
        for kk, vv in v.items():
            if isinstance(vv, (int, float)):
                print(f"  {kk:22s} {vv:.6g}")
            elif isinstance(vv, dict) and k != "design":
                print(f"  {kk}: " + ", ".join(f"{a}: {b['tau_MPa']:.1f}" for a, b in vv.items()))


if __name__ == "__main__":
    main()

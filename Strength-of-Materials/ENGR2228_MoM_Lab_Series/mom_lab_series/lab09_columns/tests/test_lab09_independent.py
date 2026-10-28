"""Lab 9 independent verification (Python / numpy / scipy).

1. Cross-language, cross-method: the page's buckling loads (Euler, spring-end characteristic equations, finite elements
   by inverse iteration) vs scipy.linalg.eigh on the Python finite-element model and scipy brentq; the page's imperfect
   and eccentric column vs a scipy banded finite-difference solve; the page's elastica vs scipy.special and solve_bvp;
   the page's secant first-yield load, tangent-modulus curve and design formulas vs the Python model.
2. Closure: lab09_analysis.py on sample_data.csv recovers the generating (truth) values within its stated uncertainty.
3. D1: the page's design preset vs the analysis table.
"""
import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np

LAB = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(LAB / "src"))
sys.path.insert(0, str(LAB.parent / "shared"))
from checklib import Checks  # noqa: E402
import lab09_model as LM  # noqa: E402

C = Checks("Lab 9 — independent checks (Python/scipy) and data-pipeline closure")
PI = math.pi
E, SY, MRO = 68.9e9, 273.7e6, 17
SEC = LM.rect(25.42e-3, 6.35e-3)
EI = E * SEC["I"]
CASES = [("pinned", 0.45, 0.0), ("fixed-pinned", 0.64, 0.0), ("fixed-fixed", 0.6005, 0.0), ("free-fixed", 1.0, 0.0),
         ("springs", 0.6005, 2800.0), ("spring-pin", 0.64, 2800.0), ("springs", 0.3, 50.0), ("spring-pin", 1.2, 1e5)]
IMP = [(0.3, 0.4e-3, 0.0), (0.7, 0.46e-3, 1e-3), (0.9, 0.0, 2e-3), (0.95, 0.26e-3, 0.08e-3)]
EL = [1.01, 1.1, 1.5, 2.0]
SL = [35.0, 49.1, 60.0, 90.0, 150.0]
JS = r"""
const {loadModel}=require('%s'); const M=loadModel('%s'); const IN=%s; const o={pcr:[], imp:[], el:[], py:[], tan:[], aa:[], aisc:[], design:{}};
const sec=M.section({sec:'rect',b:25.42e-3,t:6.35e-3}), EI=IN.E*sec.I;
for (const [ends,L,k] of IN.cases) { const p={ends,L,k}; const cp=M.closedPcr(p,IN.E,sec.I); const fe=M.feBuckle(EI,L,64,M.endsOf(p)); o.pcr.push({ends,L,k,P:cp.P,K:cp.K,fe:fe.P}); }
for (const [a,d0,e] of IN.imp) { const L=0.45, Pcr=M.euler(IN.E,sec.I,L), P=a*Pcr; const xs=[0.1*L,0.25*L,0.5*L,0.8*L];
  o.imp.push({a,d0,e,cf:M.pinnedResponse(P,Pcr,L,xs,d0,e), fe:M.feMidDefl(M.feImperfect(EI,L,64,M.endsOf({ends:'pinned'}),P,d0,e,e)), smax:M.sigmaxSecant(P,sec.A,e,sec.c,sec.r,Pcr)}); }
for (const a of IN.el) { const c=M.elasticaClosed(a); o.el.push({a, dL:c.dL, alpha:c.alpha, k:c.k}); }
for (const e of [0.5e-3,1e-3,2e-3]) o.py.push({e, PY:M.secantPY(IN.sY,sec.A,e,sec.c,sec.r,IN.E,0.45)});
for (const sl of IN.sl) { o.tan.push({sl, t:M.tangentCurve(sl,IN.E,IN.sY,IN.m), r:M.tangentCurve(sl,IN.E,IN.sY,IN.m,true)}); o.aa.push(M.aa6061(sl)); o.aisc.push(M.aisc(sl,200e9,250e6).scr); }
const d=M.PRESETS.design, ds=M.section(d); o.design={A:ds.A, I:ds.I, r:ds.r, c:ds.c, Pcr:M.euler(68.46e9,ds.I,d.L), PY:M.secantPY(273.7e6,ds.A,d.e,ds.c,ds.r,68.46e9,d.L), aa:M.aa6061(d.L/ds.r)*ds.A, Do:d.Do, tw:d.tw, L:d.L, e:d.e, P:d.Pabs};
console.log(JSON.stringify(o));
"""
IN = dict(E=E, sY=SY, m=MRO, cases=CASES, imp=IMP, el=EL, sl=SL)
js = json.loads(subprocess.run(["node", "-e", JS % (LAB.parent / "shared" / "test_harness.js", LAB / "lab09_simulation.html", json.dumps(IN))],
                               capture_output=True, text=True, check=True).stdout)

# ---------------------------------------------------------------- 1. cross-language, cross-method
for r, (ends, L, k) in zip(js["pcr"], CASES):
    endsP = {"pinned": ({"v": True, "k": 0}, {"v": True, "k": 0}), "fixed-pinned": ({"v": True, "k": 0}, {"v": True, "k": math.inf}),
             "fixed-fixed": ({"v": True, "k": math.inf}, {"v": True, "k": math.inf}), "free-fixed": ({"v": False, "k": 0}, {"v": True, "k": math.inf}),
             "springs": ({"v": True, "k": k}, {"v": True, "k": k}), "spring-pin": ({"v": True, "k": 0}, {"v": True, "k": k})}[ends]
    P_eigh = LM.fe_pcr(EI, L, 128, endsP)[0]
    if ends == "springs":
        Pc, K = LM.spring_both(EI, L, k)
    elif ends == "spring-pin":
        Pc, K = LM.spring_pin(EI, L, k)
    else:
        K = LM.K_FACTORS[ends]
        Pc = LM.euler(E, SEC["I"], K * L)
    tag = f"{ends}, L = {L} m" + (f", k = {k:g} N·m/rad" if k else "")
    C.rel(f"{tag}: page closed form vs Python closed form (scipy brentq)", r["P"], Pc, 1e-12)
    C.rel(f"{tag}: page closed form vs scipy eigh on 128 Hermite elements", r["P"], P_eigh, 5e-8, note="eigh round-off at 128 elements")
    C.rel(f"{tag}: page inverse iteration (64 elements) vs scipy eigh (128 elements)", r["fe"], P_eigh, 2e-7)
for r in js["imp"]:
    L = 0.45
    Pcr = LM.euler(E, SEC["I"], L)
    P = r["a"] * Pcr
    xs = [0.1 * L, 0.25 * L, 0.5 * L, 0.8 * L]
    x1, w1 = LM.fd_pinned(EI, L, P, 4000, r["d0"], r["e"])
    x2, w2 = LM.fd_pinned(EI, L, P, 8000, r["d0"], r["e"])
    idx1 = [int(round(xx / L * 4000)) for xx in xs]; idx2 = [2 * i for i in idx1]
    fdv = [(4 * w2[j] - w1[i]) / 3 for i, j in zip(idx1, idx2)]          # Richardson: removes the h^2 error
    worst = max(abs(a - b) / max(abs(b), 1e-12) for a, b in zip(r["cf"], fdv))
    tag = f"P = {r['a']} P_cr, δ0 = {r['d0'] * 1e3:g} mm, e = {r['e'] * 1e3:g} mm"
    C.rel(f"{tag}: page closed form (bow + Eq. 10.26) vs scipy banded finite differences (N = 4000 and 8000, Richardson), worst of 4 points", 1 + worst, 1.0, 5e-8, note="round-off floor of the 8000-interval solve")
    _, v, w0 = LM.fe_imperfect(EI, L, 128, ({"v": True, "k": 0}, {"v": True, "k": 0}), P, r["d0"], r["e"], r["e"])
    C.rel(f"{tag}: page finite elements (64) vs Python finite elements (128, numpy solve), mid-length", r["fe"], float((v - w0)[128]), 5e-7, note="discretization, amplified near P_cr")
    if r["e"] > 0:
        ym = LM.ymax_secant(r["e"], P, Pcr)
        C.rel(f"{tag}: page Eq. 10.35 vs Python Eq. 10.33 with Eq. 10.31", r["smax"], P / SEC["A"] * (1 + (ym + r["e"]) * SEC["c"] / SEC["r"] ** 2), 1e-12)
for r in js["el"]:
    PoP, dL = LM.elastica_pinned(r["k"])
    C.rel(f"elastica at {r['a']} P_cr: page (Carlson R_F + bisection) vs scipy.special.ellipk, P/P_cr", PoP, r["a"], 1e-12)
    C.rel(f"elastica at {r['a']} P_cr: page δ/L vs scipy.special", r["dL"], dL, 1e-12)
    dbvp, a0 = LM.elastica_pinned_bvp(r["a"])
    C.rel(f"elastica at {r['a']} P_cr: page δ/L vs scipy solve_bvp (collocation)", r["dL"], dbvp, 2e-7)
    C.rel(f"elastica at {r['a']} P_cr: end slope, page vs solve_bvp", r["alpha"], a0, 2e-7)
for r in js["py"]:
    C.rel(f"secant first-yield load, e = {r['e'] * 1e3:g} mm: page bisection vs scipy brentq (Eq. 10.36)", r["PY"],
          LM.secant_P_yield(SY, SEC["A"], r["e"], SEC["c"], SEC["r"], E, 0.45), 1e-10)
for r, aa, ai in zip(js["tan"], js["aa"], js["aisc"]):
    sl = r["sl"]
    C.rel(f"tangent-modulus column curve at L/r = {sl:g}: page vs Python (brentq)", r["t"], LM.column_curve_tangent(sl, E, SY, MRO), 1e-9)
    C.rel(f"reduced-modulus curve at L/r = {sl:g}: page vs Python", r["r"], LM.column_curve_tangent(sl, E, SY, MRO, reduced=True), 1e-9)
    C.rel(f"Aluminum Association 6061-T6 at L/r = {sl:g}: page vs Python", aa, LM.aa_6061(sl), 1e-14)
    C.rel(f"AISC σ_cr at L/r = {sl:g} (E 200 GPa, σY 250 MPa): page vs Python", ai, LM.aisc(sl, 200e9, 250e6)[0], 1e-14)
# a second, independent integration of the inelastic short column: scipy brentq fiber model at a finer fiber count
dsF, PsF, PmF = LM.fiber_path(25.42e-3, 6.35e-3, 0.09, E, 274e6, 17, 0.03e-3, 0.05e-3, dmax=2.4e-3, nstep=480, nf=320)
T = json.loads((LAB / "src" / "truth.json").read_text())
PmT = [r for r in T["rec"] if r.get("part") == "D"][0]["Pmax"]
C.rel("Part D: fiber-model maximum with 320 fibers vs the 80 used for the data (section discretization)", PmF, PmT, 2e-3)

# ---------------------------------------------------------------- 2. closure: the analysis recovers the truth
subprocess.run([sys.executable, str(LAB / "src" / "lab09_analysis.py")], capture_output=True, check=True)
R = json.loads((LAB / "src" / "results.json").read_text())
Tsec = LM.rect(T["b"], T["t"])
EIt = T["E"] * Tsec["I"]


def clos(name, val, truth, uu, nd=3):
    k = abs(val - truth) / (2 * uu)
    C.abs(f"closure: {name} — |Δ| = {k:.2f} U", val, truth, 3 * uu, note="within 3u (99.7 %); students use 2u")


pin = ({"v": True, "k": 0.0}, {"v": True, "k": 0.0})
for key in ("300", "450", "600"):
    Lt = T["A"][key]["L"]
    Pt = LM.fe_pcr(EIt, Lt, 128, pin)[0]
    clos(f"Part A {key} mm: Southwell P_cr vs the truth eigenvalue (N)", R["A"][key]["PS"], Pt, R["A"][key]["uPS"])
clos("Part A: E from the three Southwell loads vs truth 68.9 GPa", R["A_E"]["ES"], T["E"] / 1e9, R["A_E"]["uES"])
clos("Part A: E from the axial strain vs truth 68.9 GPa", R["A_gage"]["E"], T["E"] / 1e9, R["A_gage"]["uE"])
C.abs("closure: Part A log-log slope of P_cr against L vs −2 (Euler)", R["A_slope"]["slope"], -2.0, 3 * R["A_slope"]["u"] + 0.002)
kbot, ktop = T["k_clamp"]
Pff_t = LM.fe_pcr(EIt, T["B"]["Lff"], 128, ({"v": True, "k": ktop}, {"v": True, "k": kbot}))[0]
Pfp_t = LM.fe_pcr(EIt, T["B"]["Lfp"], 128, ({"v": True, "k": 0.0}, {"v": True, "k": kbot}))[0]
clos("Part B fixed-fixed: Southwell P_cr vs truth eigenvalue with the real clamps (N)", R["B"]["ff"]["PS"], Pff_t, R["B"]["ff"]["uPS"])
clos("Part B fixed-pinned: Southwell P_cr vs truth eigenvalue (N)", R["B"]["fp"]["PS"], Pfp_t, R["B"]["fp"]["uPS"])
clos("Part B: clamp stiffness from the fixed-fixed test vs the truth (mean of the two clamps, N·m/rad)", R["B"]["k"]["k"], (kbot + ktop) / 2, R["B"]["k"]["uk"])
C.true(f"closure: Part B fixed-fixed disagrees with Euler for L_e = 0.5 L ({R['B']['ff']['diff_pct']:.1f} %, beyond U)", not R["B"]["ff"]["agree"] and R["B"]["ff"]["diff_pct"] < 0)
C.true("closure: the spring-end model predicts the fixed-pinned test within U", R["B"]["fp_pred"]["agree"])
for en in ("1", "2"):
    clos(f"Part C e = {en} mm: fitted eccentricity vs the true groove offset (mm)", R["C"][en]["e_fit"], T["C"][en] * 1e3, R["C"][en]["ue"])
Pm_t = PmT * T["utm_gain"]
C.rel("closure: Part D maximum load read from the data vs the truth model × UTM gain", R["D"]["Pmax"], Pm_t, 2e-3)
C.true(f"closure: Part D lies below the tangent-modulus load ({R['D']['t_over']:.1f} % under) and far below Euler ({R['D']['E_over']:.1f} %)",
       R["D"]["Pmax"] < R["D"]["Pt"] and R["D"]["E_over"] > 30)
for key in ("300", "450", "600"):
    a = T["A"][key]
    d0_eq = a["d0"] + 4 / PI * T["e_knife"]
    C.abs(f"closure: Part A {key} mm: Southwell δ0 vs the truth bow + (4/π) e_knife (mm)", R["A"][key]["d0S"], d0_eq * 1e3, 0.03)

# ---------------------------------------------------------------- 3. D1: page preset vs analysis table
D = js["design"]
row = next(r for r in R["D1"]["table"] if abs(r["Do"] - D["Do"] * 1e3) < 1e-9 and abs(r["t"] - D["tw"] * 1e3) < 1e-9)
C.rel("D1: page design preset, first-yield load (secant, Lab 2 E) vs analysis table", D["PY"], row["pin"]["PY"], 1e-10)
C.rel("D1: page design preset, AA allowable load vs analysis table", D["aa"], row["pin"]["Pall"], 1e-12)
C.true(f"D1: the preset tube {D['Do'] * 1e3:g} × {D['tw'] * 1e3:g} mm is the analysis's pinned answer {R['D1']['best']['pin']}", tuple(R["D1"]["best"]["pin"]) == (round(D["Do"] * 1e3, 2), round(D["tw"] * 1e3, 2)))
trap = next(r for r in R["D1"]["table"] if (r["Do"], r["t"]) == tuple(R["D1"]["best"]["clamp"]))
C.true(f"D1 trap: assuming clamped ends picks {R['D1']['best']['clamp']}, whose pinned allowable load is {trap['pin']['Pall'] / 1e3:.2f} kN < 12 kN",
       trap["pin"]["Pall"] < 12e3 and trap["mass"] < row["mass"])

sys.exit(C.write(LAB / "tests" / "results_python.md"))

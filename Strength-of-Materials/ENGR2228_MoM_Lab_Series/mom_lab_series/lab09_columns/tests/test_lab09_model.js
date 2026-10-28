/* Lab 9 verification: closed-form formulas vs independent numerical methods, exact page code.
   Run:  node tests/test_lab09_model.js   (from lab09_columns/) */
'use strict';
const path = require('path');
const fs = require('fs');
const { loadModel, loadSimCore, check, checkAbs, checkTrue, report } = require('../../shared/test_harness.js');
const HTML = path.join(__dirname, '..', 'lab09_simulation.html');
const M = loadModel(HTML);
const S = loadSimCore(HTML);
const SAMPLE = JSON.parse(fs.readFileSync(HTML, 'utf8').match(/<script id="sample-data" type="application\/json">([\s\S]*?)<\/script>/)[1]);
const RES = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'src', 'results.json'), 'utf8'));
const PI = Math.PI;
const AL = { E: 68.9e9, sY: 273.7e6, m: 17 };
const BAR = M.section({ sec: 'rect', b: 25.42e-3, t: 6.35e-3 });
const EI = AL.E * BAR.I;

// ---------------- sections: closed forms vs numerical integration ----------------
{
  const quad = (fn, a, b, n = 4000) => { let s = 0; const h = (b - a) / n; for (let i = 0; i < n; i++) s += fn(a + (i + 0.5) * h) * h; return s; };
  const r = M.section({ sec: 'rect', b: 25.42e-3, t: 6.35e-3 });
  check('rectangle: I = bt³/12 vs midpoint integration of z² b dz', r.I, quad((z) => 25.42e-3 * z * z, -3.175e-3, 3.175e-3), 1e-7);
  const tb = M.section({ sec: 'tube', Do: 63.5e-3, tw: 1.65e-3 }), Ro = 31.75e-3, Ri = Ro - 1.65e-3;
  check('tube: A = π(Do² − Di²)/4 vs polar integration', tb.A, quad((rr) => 2 * PI * rr, Ri, Ro), 1e-7);
  check('tube: I = π(Do⁴ − Di⁴)/64 vs polar integration of r² sin²θ', tb.I, quad((rr) => PI * rr ** 3, Ri, Ro), 1e-7);
  const rd = M.section({ sec: 'round', d: 12.7e-3 });
  check('solid round: r = d/4', rd.r, Math.sqrt(rd.I / rd.A), 1e-15);
}

// ---------------- Euler and effective lengths (Beer §10.1, Fig. 10.18) vs finite elements ----------------
check('Beer Eq. 10.20: tan z = z at z = 4.4934', Math.tan(M.Z_FP), M.Z_FP, 1e-13);
check('Beer Eq. 10.21: P_cr = 20.19 EI/L² for a fixed-pinned column (z² = 20.19)', M.Z_FP ** 2, 20.19, 2e-4);
check('Beer Fig. 10.18: K = π/4.4934 = 0.699 for fixed-pinned', M.K_IDEAL['fixed-pinned'], 0.699, 3e-4);
for (const ends of ['pinned', 'fixed-pinned', 'fixed-fixed', 'free-fixed']) {
  for (const L of [0.3, 0.6005, 1.7]) {
    const p = { ends, L }, cp = M.closedPcr(p, AL.E, BAR.I), fe = M.feBuckle(EI, L, 64, M.endsOf(p));
    check(`${ends}, L = ${L} m: Euler with K = ${cp.K.toFixed(4)} vs finite elements (N = 64)`, fe.P, cp.P, 2e-7);
  }
}
// rotational-spring ends: characteristic equations (Appendix D.3) vs finite elements
for (const k of [5, 300, 2800, 1e5, 1e8]) {
  for (const [ends, L] of [['springs', 0.6005], ['spring-pin', 0.640]]) {
    const p = { ends, L, k }, cp = M.closedPcr(p, AL.E, BAR.I), fe = M.feBuckle(EI, L, 64, M.endsOf(p));
    check(`${ends}, k = ${k} N·m/rad: characteristic equation vs finite elements (N = 64)`, fe.P, cp.P, 2e-7);
  }
}
{
  const L = 0.6005, sb = M.springBoth(EI, L, 2800), sp = M.springPin(EI, L, 2800);
  checkAbs('spring ends: residual of tan x + 2x EI/(kL) at the root', Math.tan(sb.x) + 2 * sb.x * EI / (2800 * L), 0, 1e-12);
  checkAbs('spring + pin: residual of tan z − z/(1 + z² EI/(kL)) at the root', Math.tan(sp.z) - sp.z / (1 + sp.z * sp.z * EI / (2800 * L)), 0, 1e-11);
  check('spring ends: k → 0 gives the pinned load', M.springBoth(EI, L, 1e-9).P, PI * PI * EI / L ** 2, 1e-9);
  check('spring ends: k = 10¹⁴ N·m/rad gives the fixed-fixed load', M.springBoth(EI, L, 1e14).P, 4 * PI * PI * EI / L ** 2, 1e-9);
  check('spring + pin: k = 10¹⁴ gives Beer Eq. 10.21', M.springPin(EI, L, 1e14).P, M.Z_FP ** 2 * EI / L ** 2, 1e-9);
  check('k from P (inverse of the symmetric characteristic equation)', M.kFromSym(EI, L, sb.P), 2800, 1e-10);
  checkTrue(`kL/EI = 1 already gives K = ${M.springBoth(EI, 1, EI).K.toFixed(3)} (between 0.5 and 1)`, M.springBoth(EI, 1, EI).K < 0.9 && M.springBoth(EI, 1, EI).K > 0.5);
}
// mode shapes: closed form vs eigenvector
for (const [ends, k] of [['pinned', 0], ['fixed-fixed', 0], ['fixed-pinned', 0], ['free-fixed', 0], ['springs', 2800], ['spring-pin', 2800]]) {
  const L = 0.6, p = { ends, L, k }, n = 64, fe = M.feBuckle(EI, L, n, M.endsOf(p));
  const xn = Array.from({ length: n + 1 }, (_, i) => i * L / n), yc = M.modeShape(p, AL.E, BAR.I, xn);
  let sfy = 0, sff = 0; for (let i = 0; i <= n; i++) { sfy += fe.v[2 * i] * yc[i]; sff += fe.v[2 * i] ** 2; }
  const al = sfy / sff;                           // scale the eigenvector onto the closed form (least squares)
  let worst = 0; for (let i = 0; i <= n; i++) worst = Math.max(worst, Math.abs(al * fe.v[2 * i] - yc[i]));
  checkAbs(`${ends}: closed-form mode shape vs finite-element eigenvector (least-squares scaled), max difference`, worst, 0, 1e-5);
}
// convergence order of the finite elements
{
  const p = { ends: 'pinned', L: 0.45 }, cp = M.closedPcr(p, AL.E, BAR.I);
  const ns = [4, 8, 16], err = ns.map((n) => Math.abs(M.feBuckle(EI, 0.45, n, M.endsOf(p)).P / cp.P - 1));
  check('Hermite elements: P_cr error falls as N⁻⁴ (fitted order, N = 4 to 16)', -S.logSlope(ns, err), 4, 0.03);
  const q = { ends: 'springs', L: 0.6, k: 2800 }, cq = M.closedPcr(q, AL.E, BAR.I), eq = [8, 16, 32].map((n) => Math.abs(M.feBuckle(EI, 0.6, n, M.endsOf(q)).P / cq.P - 1));
  check('Hermite elements with spring ends: order 4 too (N = 8 to 32)', -S.logSlope([8, 16, 32], eq), 4, 0.03);
  checkTrue(`one fixed-fixed element has no free DOF: P is NaN (the page asks for N ≥ 2)`, Number.isNaN(M.feBuckle(EI, 0.6, 1, M.endsOf({ ends: 'fixed-fixed' })).P));
}

// ---------------- imperfect and eccentric pinned column (Beer §10.2) ----------------
for (const [a, d0, e] of [[0.3, 0.4e-3, 0], [0.7, 0.4e-3, 1e-3], [0.9, 0, 2e-3], [0.95, 0.26e-3, 0.08e-3]]) {
  const L = 0.45, Pcr = M.euler(AL.E, BAR.I, L), P = a * Pcr, tag = `P = ${a} P_cr, δ0 = ${d0 * 1e3} mm, e = ${e * 1e3} mm`;
  const cf = M.pinnedResponse(P, Pcr, L, [L / 2], d0, e)[0];
  const fd = M.fdPinned(EI, L, P, 4000, d0, e)[2000];
  const fe = M.feMidDefl(M.feImperfect(EI, L, 64, M.endsOf({ ends: 'pinned' }), P, d0, e, e));
  check(`${tag}: mid-length deflection, closed form vs finite differences (N = 4000)`, fd, cf, 3e-6);
  check(`${tag}: mid-length deflection, closed form vs finite elements (N = 64)`, fe, cf, 3e-7);
  const kap = M.feCurvMid(M.feImperfect(EI, L, 64, M.endsOf({ ends: 'pinned' }), P, d0, e, e));
  check(`${tag}: curvature at mid-length × EI vs M = −P(e + δ0 + δ) (Beer Eq. 10.22)`, kap * EI, -P * (e + d0 + cf), 2e-3);
  const xs = [0.1 * L, 0.33 * L, 0.5 * L, 0.71 * L];
  const sum = M.pinnedResponse(P, Pcr, L, xs, d0, 0).map((v, i) => v + M.pinnedResponse(P, Pcr, L, xs, 0, e)[i]), both = M.pinnedResponse(P, Pcr, L, xs, d0, e);
  checkAbs(`${tag}: at a fixed load the responses to bow and eccentricity superpose (max |Δ|, m)`, Math.max(...both.map((v, i) => Math.abs(v - sum[i]))), 0, 1e-15);
}
{
  const L = 0.45, Pcr = M.euler(AL.E, BAR.I, L), e = 2e-3;
  for (const a of [0.2, 0.6, 0.9]) check(`Eq. 10.31 equals Eq. 10.26 at x = L/2 (P = ${a} P_cr)`, M.ymaxSecant(e, a * Pcr, Pcr), M.pinnedResponse(a * Pcr, Pcr, L, [L / 2], 0, e)[0], 1e-13);
  for (const a of [0.2, 0.6, 0.9]) { const P = a * Pcr, ym = M.ymaxSecant(e, P, Pcr); check(`Eq. 10.35 equals Eq. 10.33, P/A [1 + (y_max + e)c/r²] (P = ${a} P_cr)`, M.sigmaxSecant(P, BAR.A, e, BAR.c, BAR.r, Pcr), P / BAR.A * (1 + (ym + e) * BAR.c / BAR.r ** 2), 1e-13); }
  const r2 = M.ymaxSecant(e, 0.66 * Pcr, Pcr) / M.ymaxSecant(e, 0.33 * Pcr, Pcr);
  checkTrue(`superposition fails in P: doubling 0.33 → 0.66 P_cr multiplies y_max by ${r2.toFixed(3)} (> 2)`, r2 > 2.5);
  for (const ee of [0.5e-3, 1e-3, 2e-3]) {
    const PY = M.secantPY(AL.sY, BAR.A, ee, BAR.c, BAR.r, AL.E, L), PYn = M.secantPYnum(AL.E, BAR.I, BAR.A, BAR.c, L, AL.sY, ee, 4000);
    check(`first yield, e = ${ee * 1e3} mm: secant formula Eq. 10.36 vs finite differences (N = 4000)`, PYn, PY, 2e-6);
    check(`first yield, e = ${ee * 1e3} mm: σ_max(P_Y) = σ_Y`, M.sigmaxSecant(PY, BAR.A, ee, BAR.c, BAR.r, M.euler(AL.E, BAR.I, L)), AL.sY, 1e-10);
  }
  // order of the finite differences
  const ns = [16, 32, 64, 128], ex = M.pinnedResponse(0.7 * Pcr, Pcr, L, [L / 2], 0.4e-3, 1e-3)[0];
  const er = ns.map((n) => Math.abs(M.fdPinned(EI, L, 0.7 * Pcr, n, 0.4e-3, 1e-3)[n / 2] / ex - 1));
  check('finite differences: error falls as N⁻² (fitted order)', -S.logSlope(ns, er), 2, 0.02);
}
// Southwell
{
  const L = 0.45, Pcr = M.euler(AL.E, BAR.I, L), Ps = [0.5, 0.6, 0.7, 0.8, 0.9].map((a) => a * Pcr), d = Ps.map((P) => M.pinnedResponse(P, Pcr, L, [L / 2], 0.46e-3, 0)[0]);
  const sw = M.southwell(d, Ps);
  check('Southwell on an exact half-sine bow recovers P_cr', sw.Pcr, Pcr, 1e-12);
  check('Southwell on an exact half-sine bow recovers δ0', sw.d0, 0.46e-3, 1e-10);
  const de = Ps.map((P) => M.pinnedResponse(P, Pcr, L, [L / 2], 0, 1e-3)[0]), se = M.southwell(de, Ps);
  check('Southwell on a pure eccentric load: P_cr within 0.5 % (the secant curve is nearly a Southwell line)', se.Pcr, Pcr, 5e-3);
  check('Southwell on a pure eccentric load: the intercept is about (4/π) e', se.d0, 4 / PI * 1e-3, 0.03);
  for (const [ends, k] of [['fixed-fixed', 0], ['fixed-pinned', 0], ['springs', 2800]]) {
    const p = { ends, L: 0.6, k }, en = M.endsOf(p), Pc = M.feBuckle(EI, 0.6, 64, en).P, PP = [0.5, 0.6, 0.7, 0.8, 0.9].map((a) => a * Pc);
    const dd = PP.map((P) => M.feMidDefl(M.feImperfect(EI, 0.6, 64, en, P, 0.5e-3)));
    check(`${ends}: Southwell on mid-length readings (half-sine bow, clamps grip the initial slope) vs the eigenvalue`, M.southwell(dd, PP).Pcr, Pc, 5e-3, 'a half sine is not the clamped mode shape: higher modes bias the fit slightly');
  }
  // the sample data: the page's fit equals the analysis script's
  for (const [key, res] of [['A300', RES.A['300']], ['A450', RES.A['450']], ['A600', RES.A['600']], ['Bff', RES.B.ff], ['Bfp', RES.B.fp]]) {
    const t = SAMPLE.tests[key], use = t.P.map((P, i) => [P, t.d[i]]).filter(([P, dd]) => P >= t.Pmin && dd > 0);
    check(`sample data ${key}: page Southwell fit vs lab09_analysis.py`, M.southwell(use.map((u) => u[1]), use.map((u) => u[0])).Pcr, res.PS, 1e-9);
  }
}
// elastica
{
  check("Carlson R_F: K(m = 0.5) = 1.854074677301372", M.ellK(0.5), 1.854074677301372, 1e-14);
  check("Carlson R_F: K(0) = π/2", M.ellK(0), PI / 2, 1e-15);
  for (const a of [1.005, 1.02, 1.2, 1.5, 2.5]) {
    const c = M.elasticaClosed(a), s = M.elasticaShoot(a, 400);
    check(`elastica at ${a} P_cr: δ/L by elliptic integrals vs RK4 shooting (400 steps)`, s.dL, c.dL, 2e-9);
    check(`elastica at ${a} P_cr: end slope, elliptic vs shooting`, s.alpha, c.alpha, 2e-9);
  }
  const c = M.elasticaClosed(1.0001);
  check('elastica, small deflection: P/P_cr − 1 ≈ (π²/8)(δ/L)² (leading term, at 1.0001 P_cr)', 1e-4, PI * PI / 8 * c.dL ** 2, 5e-4);
}

// ---------------- material and short columns ----------------
{
  for (const s of [50e6, 200e6, 260e6, 300e6]) check(`Ramberg–Osgood: stress → strain → stress round trip at ${s / 1e6} MPa`, M.roStress(M.roStrain(s, AL.E, AL.sY, AL.m), AL.E, AL.sY, AL.m), s, 1e-12);
  for (const s of [100e6, 220e6, 270e6]) {
    const h = s * 1e-6, num = 2 * h / (M.roStrain(s + h, AL.E, AL.sY, AL.m) - M.roStrain(s - h, AL.E, AL.sY, AL.m));
    check(`tangent modulus at ${s / 1e6} MPa: formula vs central difference of the curve`, M.tangentModulus(s, AL.E, AL.sY, AL.m), num, 1e-7);
  }
  checkTrue('tangent modulus stays finite for a sharp knee (m = 60, steel): no overflow', Number.isFinite(M.tangentModulus(400e6, 200e9, 250e6, 60)));
  for (const sl of [35, 49.1, 60, 80]) {
    const st = M.tangentCurve(sl, AL.E, AL.sY, AL.m);
    check(`tangent-modulus column curve at L/r = ${sl}: σ = π²E_t/(L/r)² inverted by the closed form π√(E_t/σ)`, M.tangentSlender(st, AL.E, AL.sY, AL.m), sl, 1e-10);
    const sec = M.section({ sec: 'rect', b: 25.42e-3, t: 6.35e-3 }), L = sl * sec.r, fe = M.feBuckle(M.tangentModulus(st, AL.E, AL.sY, AL.m) * sec.I, L, 32, M.endsOf({ ends: 'pinned' }));
    check(`L/r = ${sl}: tangent-modulus load vs finite-element eigenvalue with E_t I`, fe.P, st * sec.A, 2e-6);
    checkTrue(`L/r = ${sl}: reduced-modulus stress ≥ tangent-modulus stress`, M.tangentCurve(sl, AL.E, AL.sY, AL.m, true) >= st);
  }
  check('tangent-modulus curve joins Euler for slender columns (L/r = 200)', M.tangentCurve(200, AL.E, AL.sY, AL.m), M.sigmaCr(AL.E, 200), 1e-9);
  for (const nf of [8, 40, 200]) check(`fiber section: Σ dA z² = I (1 − 1/n_f²) for n_f = ${nf} (midpoint rule)`, M.fiberI(25.42e-3, 6.35e-3, nf), BAR.I * (1 - 1 / nf ** 2), 1e-12);
  // fiber model, elastic material: equilibrium of the assumed mode gives delta = (d0 + e) a/(1 - a) with P_cr of the fiber section
  {
    const nf = 400, L = 0.45, d0 = 0.4e-3, e = 0.1e-3, fp = M.fiberPath({ b: 25.42e-3, t: 6.35e-3, L, E: AL.E, s02: 1e15, m: AL.m, d0, e, dmax: 4e-3, nstep: 8, nf });
    const Pf = PI * PI * AL.E * M.fiberI(25.42e-3, 6.35e-3, nf) / L ** 2;
    let worst = 0;
    fp.d.forEach((d, i) => { worst = Math.max(worst, Math.abs(fp.P[i] / (Pf * d / (d + d0 + e)) - 1)); });
    checkAbs('fiber model with an elastic material vs the assumed-mode closed form P = P_cr δ/(δ + δ0 + e), max relative difference', worst, 0, 1e-9);
  }
  {
    const L = 0.09, sec = M.section({ sec: 'rect', b: 25.42e-3, t: 6.35e-3 }), sl = L / sec.r, Pt = M.tangentCurve(sl, AL.E, AL.sY, AL.m) * sec.A, Pr = M.tangentCurve(sl, AL.E, AL.sY, AL.m, true) * sec.A;
    const fp0 = M.fiberPath({ b: 25.42e-3, t: 6.35e-3, L, E: AL.E, s02: AL.sY, m: AL.m, d0: 1e-8, e: 0, dmax: 1.2e-3, nstep: 160, nf: 160 });
    checkTrue(`nearly perfect inelastic column: tangent-modulus load ${(Pt / 1e3).toFixed(2)} kN ≤ fiber maximum ${(fp0.Pmax / 1e3).toFixed(2)} kN ≤ reduced-modulus load ${(Pr / 1e3).toFixed(2)} kN (Shanley)`, fp0.Pmax >= Pt * 0.995 && fp0.Pmax <= Pr * 1.005);
    const T = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'src', 'truth.json'), 'utf8')), TD = T.D, Pm = T.rec.find((r) => r.part === 'D').Pmax;
    const fp = M.fiberPath({ b: T.b, t: T.t, L: TD.L, E: T.E, s02: T.s02, m: T.m, d0: TD.d0, e: TD.e, dmax: 2.4e-3, nstep: 480, nf: 80 });
    check('Part D: page fiber model (JS) vs the truth model (Python, scipy brentq) with identical inputs, maximum load', fp.Pmax, Pm, 1e-7);
  }
  // design formulas, typed independently from Beer Eqs. 10.43b–10.45b and 10.38–10.42
  check('AA 6061-T6, L/r = 10: 146.3 MPa (Eq. 10.43b)', M.aa6061(10), 146.3e6, 1e-12);
  check('AA 6061-T6, L/r = 30: 173.9 − 1.602(30) + 0.00323(30)² MPa (Eq. 10.44b)', M.aa6061(30), (173.9 - 48.06 + 2.907) * 1e6, 1e-12);
  check('AA 6061-T6, L/r = 100: 356 000/100² MPa (Eq. 10.45b)', M.aa6061(100), 35.6e6, 1e-12);
  check('AA 6061-T6 Euler branch = Euler with E = 68.9 GPa divided by 1.91', PI * PI * 68.9e9 / M.aa6061(120) / 120 ** 2, 1.91, 2e-3);
  const E = 200e9, sY = 250e6, slj = 4.71 * Math.sqrt(E / sY);
  check('AISC junction (Eq. 10.41): Eqs. 10.38 and 10.40 meet within 0.5 %', M.aisc(slj * (1 - 1e-9), E, sY).scr, M.aisc(slj * (1 + 1e-9), E, sY).scr, 5e-3);
  check('AISC: σ_all = σ_cr/1.67 (Eq. 10.42)', M.aisc(80, E, sY).sall * 1.67, M.aisc(80, E, sY).scr, 1e-14);
}

// ---------------- presets and units ----------------
for (const [k, pr] of Object.entries(M.PRESETS)) {
  const sc = M.section(pr), cp = M.closedPcr(pr, pr.E, sc.I);
  checkTrue(`preset ${k}: finite P_cr (${(cp.P / 1e3).toFixed(3)} kN) and K (${cp.K.toFixed(4)})`, Number.isFinite(cp.P) && cp.P > 0 && cp.K > 0);
}
{
  const ff = M.endsOf({ ends: 'fixed-pinned' });
  checkTrue('end condition "fixed-pinned": top end A pinned, bottom end B fixed (as in Lab Part B)', ff[0].k === 0 && ff[1].k === Infinity);
  check('D1 preset: 12 kN on the 63.5 × 1.65 mm tube, pinned, 2.0 m', M.PRESETS.design.Pabs, 12e3, 0);
  S.setSystem('US');
  check('units: 1 N·m/rad in lb·in/rad', S.conv('rotstiff', 1), 8.850745791, 1e-9);
  check('units: 1000 N in lbf', S.conv('forceN', 1000), 224.8089431, 1e-9);
  S.setSystem('SI');
  check('units: 450 mm', S.conv('length', 0.45), 450, 1e-15);
}

const r = report('Lab 9 model tests (exact page code)');
fs.writeFileSync(path.join(__dirname, 'results_node.md'), r.text + '\n');
console.log(r.text.split('\n').filter((l) => l.includes('FAIL') || l.includes('passed')).join('\n'));
process.exit(r.nfail ? 1 : 0);

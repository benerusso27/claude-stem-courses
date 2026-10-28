/* Lab 2 verification: closed-form formulas vs independent numerical methods, exact page code.
   Run:  node tests/test_lab02_model.js   (from lab02_axial_thermal/) */
'use strict';
const path = require('path');
const fs = require('fs');
const { loadModel, loadSimCore, check, checkAbs, checkTrue, report } = require('../../shared/test_harness.js');
const HTML = path.join(__dirname, '..', 'lab02_simulation.html');
const M = loadModel(HTML);
const S = loadSimCore(HTML);

function simpson(f, a, b, n = 2000) { const h = (b - a) / n; let s = f(a) + f(b); for (let i = 1; i < n; i++) s += f(a + i * h) * (i % 2 ? 4 : 2); return s * h / 3; }
// independent dense linear solve (Gaussian elimination with partial pivoting)
function gauss(A, b) {
  const n = b.length; A = A.map((r) => r.slice()); b = b.slice();
  for (let k = 0; k < n; k++) {
    let p = k; for (let i = k + 1; i < n; i++) if (Math.abs(A[i][k]) > Math.abs(A[p][k])) p = i;
    [A[k], A[p]] = [A[p], A[k]]; [b[k], b[p]] = [b[p], b[k]];
    for (let i = k + 1; i < n; i++) { const m = A[i][k] / A[k][k]; for (let j = k; j < n; j++) A[i][j] -= m * A[k][j]; b[i] -= m * b[k]; }
  }
  const x = new Array(n).fill(0);
  for (let i = n - 1; i >= 0; i--) { let s = b[i]; for (let j = i + 1; j < n; j++) s -= A[i][j] * x[j]; x[i] = s / A[i][i]; }
  return x;
}

// ---------------- parallel members ----------------
const variants = [
  ['rod in tube, P = 30 kN', Object.assign({}, M.PRESETS.rodtube)],
  ['rod in tube, P = 5 kN (gap open)', Object.assign({}, M.PRESETS.rodtube, { P: 5e3 })],
  ['rod in tube, heated 40 K', Object.assign({}, M.PRESETS.rodtube, { dT: 40 })],
  ['rod in tube, interference −0.02 mm', Object.assign({}, M.PRESETS.rodtube, { g: -20e-6, P: 10e3 })],
  ['bolt and sleeve, ΔT = 60 K', Object.assign({}, M.PRESETS.bolt)],
  ['bolt and sleeve, cooled 40 K, P = 3 kN', Object.assign({}, M.PRESETS.bolt, { dT: -40, P: 3e3 })],
  ['brass bolt in steel sleeve', Object.assign({}, M.PRESETS.bolt, { mat1: 'brass', mat2: 'steel', dT: 80 })],
];
for (const [name, p] of variants) {
  const cf = M.parallelClosed(p);
  const pa = M.parallelPath(p);
  const n = pa.F1.length - 1;
  const scale = Math.max(Math.abs(cf.F1), Math.abs(cf.F2), 1);
  checkAbs(`[${name}] F1: closed form vs event-tracking load path`, pa.F1[n] / scale, cf.F1 / scale, 1e-10);
  checkAbs(`[${name}] F2: closed form vs event-tracking load path`, pa.F2[n] / scale, cf.F2 / scale, 1e-10);
  checkAbs(`[${name}] equilibrium F1 + F2 = −P (relative to the largest force)`, (cf.F1 + cf.F2 + p.P) / scale, 0, 1e-12);
  // independent: assemble the 2-equation system (equilibrium + compatibility) and solve by Gaussian elimination
  if (!cf.open) {
    const m1 = M.MATERIALS[p.mat1], m2 = M.MATERIALS[p.mat2];
    const A1 = M.A_circ(p.d1), A2 = M.A_tube(p.do, p.di);
    const L2 = p.L - (p.contact ? p.g : 0);
    const k1 = m1.E * A1 / p.L, k2 = m2.E * A2 / L2;
    const g = p.contact ? p.g : -p.F0 * (1 / k1 + 1 / k2);
    const x = gauss([[1, 1], [1 / k1, -1 / k2]], [-p.P, -g - p.dT * (m1.alpha * p.L - m2.alpha * L2)]);
    checkAbs(`[${name}] F1: closed form vs Gaussian elimination of equilibrium + compatibility`, x[0] / scale, cf.F1 / scale, 1e-12);
  }
}
{
  const p = Object.assign({}, M.PRESETS.rodtube);
  const pa = M.parallelPath(p, 37);
  const ev = pa.events.find((e) => e.closed);
  check('gap-closing load k1·g vs bisection-located contact event', ev.P, M.parallelClosed(p).Pgap, 1e-9);
  // share after contact: finite difference of the numerical solution between 20 and 30 kN
  const a = M.parallelPath(Object.assign({}, p, { P: 20e3 })), b = M.parallelPath(Object.assign({}, p, { P: 30e3 }));
  const share = -(b.F2[b.F2.length - 1] - a.F2[a.F2.length - 1]) / 10e3;
  check('load share E2A2/(E1A1 + E2A2) vs finite difference of numerical forces', share, M.parallelClosed(p).share, 3e-4, 'tube 0.040 mm shorter changes k2 by 0.03 %');
  // pre-lab P2 (key value, hand calculation): P = 30 kN, g = 0.040 mm -> F2 = -8.547 kN
  check('hand example (pre-lab P2): tube force at P = 30 kN with g = 0.040 mm (−8.547 kN)', M.parallelClosed(p).F2 / 1e3, -8.547, 1e-4);
  checkTrue('superposition fails while the gap is open: F2(20 kN) ≠ 2·F2(10 kN)', Math.abs(M.parallelClosed(Object.assign({}, p, { P: 20e3 })).F2 - 2 * M.parallelClosed(Object.assign({}, p, { P: 10e3 })).F2) > 1000);
}
{
  const p = Object.assign({}, M.PRESETS.bolt);
  const cf = M.parallelClosed(p);
  const a = M.parallelPath(Object.assign({}, p, { dT: 59 })), b = M.parallelPath(Object.assign({}, p, { dT: 61 }));
  check('dF/dT closed form vs central difference of the numerical solution', (b.F1[b.F1.length - 1] - a.F1[a.F1.length - 1]) / 2, cf.dFdT, 1e-9);
  check('hand example (pre-lab P3): bolt change per kelvin, steel bolt d = 10 mm, sleeve 20/10.5 mm (94.53 N/K)', cf.dFdT, 94.53, 1e-4);
  check('preload preserved at ΔT = 0', M.parallelClosed(Object.assign({}, p, { dT: 0 })).F1, 2000, 1e-12);
}

// ---------------- series bar ----------------
for (const [name, pv] of [['stepped, fixed–fixed, P_B = 40 kN', M.PRESETS.stepped], ['stepped, free end, heated', Object.assign({}, M.PRESETS.stepped, { support: 'free', dT: 50 })],
  ['stepped, gap 0.05 mm, P_B = 40 kN', Object.assign({}, M.PRESETS.stepped, { support: 'gap', g: 0.05e-3 })], ['stepped, gap 0.5 mm (stays open)', Object.assign({}, M.PRESETS.stepped, { support: 'gap', g: 0.5e-3 })]]) {
  const p = Object.assign({}, pv);
  const cf = M.seriesClosed(p), fe = M.seriesFE(p, 3);
  const sc = Math.max(Math.abs(cf.R), Math.abs(p.PB), 1);
  checkAbs(`[${name}] reaction: closed form vs FE (prismatic segments are exact)`, fe.R / sc, cf.R / sc, 1e-12);
  check(`[${name}] junction displacement: closed form vs FE`, fe.uB, cf.uB, 1e-9);
  // equilibrium of the whole bar: left reaction + PB - R = 0; left reaction from the first element force
  const Rleft = -fe.Ne[0];
  checkAbs(`[${name}] equilibrium of the whole bar (FE): R_left + P_B − R_right = 0`, (Rleft + p.PB - fe.R) / sc, 0, 1e-12);
}
{
  const p = Object.assign({}, M.PRESETS.stepped, { PB: 0, dT: 50, L2: 0.2, d2: 25e-3, smat2: 'steel' });
  const cf = M.seriesClosed(p);
  check('fully restrained prismatic steel bar heated 50 K: σ = −EαΔT', cf.sigma2, -205e9 * 11.7e-6 * 50, 1e-12);
}
{
  const p = Object.assign({}, M.PRESETS.taper, { support: 'fixed' });
  const m1 = M.MATERIALS[p.smat1];
  const f1 = simpson((x) => 1 / (m1.E * M.A_circ(p.da + (p.db - p.da) * x / p.L1)), 0, p.L1);
  check('taper flexibility 4L/(πE·da·db) vs Simpson quadrature of ∫dx/(EA)', M.seriesClosed(p).f1, f1, 1e-10);
  const c = M.seriesConvergence(p);
  checkTrue(`taper: FE converges at second order (observed ${c.slope.toFixed(3)})`, Math.abs(c.slope - 2) < 0.1);
  const fe = M.seriesFE(p, 256);
  check('taper: FE (N = 256) reaction vs closed form', fe.R, M.seriesClosed(p).R, 2e-5);
  // displacement field: closed form u(x) vs Simpson integration of strain N/(EA) + alpha dT
  const cf = M.seriesClosed(p);
  const x = 0.6 * p.L1;
  const ux = simpson((s) => cf.N1 / (m1.E * M.A_circ(p.da + (p.db - p.da) * s / p.L1)) + m1.alpha * p.dT, 0, x);
  check('taper: closed-form u(x) vs Simpson integration of the strain', cf.u(x), ux, 1e-9);
}
{
  const d = 10e-3, L = 0.5, al = 11.7e-6, E = 205e9;
  const dTc = M.bucklingDT(d, L, al);
  const Pcr = Math.PI ** 2 * E * Math.PI * d ** 4 / 64 / (0.5 * L) ** 2;
  check('thermal buckling ΔT_cr: E·α·ΔT_cr·A equals the fixed–fixed Euler load', E * al * dTc * M.A_circ(d), Pcr, 1e-12);
}
S.setSystem('US');
check('units: ΔT of 100 K = 180 °F', S.conv('temperature', 100), 180, 1e-12);
check('units: 1 kip = 4.448 kN', S.unconv('force', 1), 4448.2216, 1e-7);
S.setSystem('SI');

const { text, nfail } = report('Lab 2 — simulation model (Node, exact page code)');
fs.writeFileSync(path.join(__dirname, 'results_node.md'), text + '\n');
console.log(text);
process.exit(nfail ? 1 : 0);

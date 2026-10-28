/* Lab 4 verification: closed-form formulas vs independent numerical methods, exact page code.
   Run:  node tests/test_lab04_model.js   (from lab04_bending/) */
'use strict';
const path = require('path');
const fs = require('fs');
const { loadModel, loadSimCore, check, checkAbs, checkTrue, report } = require('../../shared/test_harness.js');
const HTML = path.join(__dirname, '..', 'lab04_simulation.html');
const M = loadModel(HTML);
const S = loadSimCore(HTML);
const P = M.PRESETS;

// ---------------- materials ----------------
for (const e of [1e-4, 3.9e-3, 8e-3, 0.03]) { const m = M.MATERIALS.al; const s = M.sigmaOf(m, e); check(`Ramberg–Osgood inverse ε(σ(ε)) = ε at ε = ${e}`, s / m.E + 0.002 * (s / m.sY) ** m.m, e, 1e-12); }
{ const m = M.MATERIALS.steel; check('steel law continuous at the end of the plateau', M.sigmaOf(m, m.eL + 1e-10), M.sigmaOf(m, m.eL - 1e-10), 1e-6); }

// ---------------- beams: closed form (statics) vs numerical integration ----------------
const beamCases = [
  ['4-point bending (preset)', Object.assign({}, P.fourpt)],
  ['cantilever, triangular load (preset)', Object.assign({}, P.cantilever)],
  ['overhang, point loads + uniform load (preset)', Object.assign({}, P.overhang)],
  ['cantilever, triangular + point load', Object.assign({}, P.cantilever, { P: 3e3, a: 0.7 })],
  ['3-point bending', Object.assign({}, P.fourpt, { load: 'center', P: 12e3 })],
  ['uniform load, simply supported', Object.assign({}, P.fourpt, { load: 'udl', w: 5e3, L: 2.5, s: 2.5 })],
];
for (const [name, p] of beamCases) {
  const c = M.beamClosed(p), n = M.beamNumeric(p, 512);
  const sc = Math.max(Math.abs(c.re.RA), Math.abs(c.re.RB), 1);
  checkAbs(`[${name}] R_A: statics vs shooting integration`, n.RA / sc, c.re.RA / sc, 1e-9);
  if (p.support === 'simple') checkAbs(`[${name}] R_B: statics vs shooting integration`, n.RB / sc, c.re.RB / sc, 1e-9);
  else check(`[${name}] fixed-end moment: statics vs integration from the free end`, n.MA, c.re.MA, 1e-5);
  let worst = 0;
  for (const q of n.prof) worst = Math.max(worst, Math.abs(q.M - c.M(q.x)));
  const tol = p.load === 'tri' ? 2e-5 : 1e-9;
  checkTrue(`[${name}] M(x) at every node: largest |error|/|M|max = ${(worst / Math.abs(c.Mmax)).toExponential(2)} (tolerance ${tol})`, worst / Math.abs(c.Mmax) < tol);
  // dM/dx = V and dV/dx = -w from the closed forms (central differences away from loads)
  const ld = c.ld, h = 1e-6;
  for (const x of [0.13, 0.31, 0.57, 0.83].map((f) => f * p.L)) {
    if (ld.points.some((q) => Math.abs(q[0] - x) < 1e-3) || Math.abs(x - p.s) < 1e-3) continue;
    checkAbs(`[${name}] dM/dx = V at x = ${x.toFixed(3)} m (relative to |V|max)`, ((c.M(x + h) - c.M(x - h)) / (2 * h) - c.V(x)) / sc, 0, 1e-6);
  }
}
check('hand value: 4-point bending, M = (P/2)a = 2000 N·m', M.beamClosed(P.fourpt).Mmax, 2000, 1e-12);
check('hand value: cantilever with triangular load, fixed-end moment w₀L²/3', M.beamClosed(P.cantilever).re.MA, 6e3 * 4 / 3, 1e-12);
check('hand value: overhang, M over the roller = −4 kN·m', M.beamClosed(P.overhang).M(3.0 - 1e-12), -4000, 1e-9);
{
  const cv = M.beamConvergence(Object.assign({}, P.cantilever));
  checkTrue(`triangular load: trapezoid integration converges at second order (observed ${cv.slope.toFixed(3)})`, Math.abs(cv.slope - 2) < 0.1);
}
// ---------------- sections ----------------
const el = { law: 'epp', sY: 1e30 };
{
  const p = Object.assign({}, P.fourpt), tr = M.transformed(p, 1);
  check('rectangle: I = bh³/12 (transformed routine)', tr.I, p.b * p.h ** 3 / 12, 1e-12);
  const kap = 0.1;
  const s = M.stripSolve(p, kap, 2000, el);
  check('rectangle, elastic: M = EIκ vs strip summation (N = 2000)', s.M, M.MATERIALS.al.E * tr.I * kap, 1e-6);
  checkAbs('rectangle, elastic: neutral axis at mid-depth (relative to h)', (s.yNA - p.h / 2) / p.h, 0, 1e-12);
}
{
  const p = Object.assign({}, P.composite), tr = M.transformed(p, 1);
  const n = M.MATERIALS.steel.E / M.MATERIALS.al.E, A1 = p.b * p.h, A2 = n * p.b * p.ts, y1 = p.ts + p.h / 2, y2 = p.ts / 2;
  const yb = (A1 * y1 + A2 * y2) / (A1 + A2);
  const I = p.b * p.h ** 3 / 12 + A1 * (y1 - yb) ** 2 + n * p.b * p.ts ** 3 / 12 + A2 * (y2 - yb) ** 2;
  check('composite: transformed-section centroid vs hand formula', tr.ybar, yb, 1e-12);
  check('composite: transformed I vs hand formula', tr.I, I, 1e-12);
  const s = M.stripSolve(p, 0.04, 2000, el);
  check('composite: neutral axis, transformed section vs strip equilibrium', s.yNA, tr.ybar, 1e-9);
  check('composite: M = E₁I_tκ vs strip summation', s.M, M.MATERIALS.al.E * tr.I * 0.04, 1e-6);
  const prof = s.prof.find((r) => r.y < p.ts);
  check('composite: steel stress = n × aluminum stress at the same strain', prof.s / (M.MATERIALS.al.E * prof.e), n, 1e-12);
}
{
  const p = Object.assign({}, P.plastic), al = M.MATERIALS.al;
  const kY = al.sY / (al.E * p.h / 2), MY = al.sY * p.b * p.h ** 2 / 6;
  for (const r of [0.5, 1, 1.5, 3, 10]) {
    check(`EPP rectangle at κ = ${r}κ_Y: §4.6 formula vs strip summation (N = 2000)`, M.stripSolve(p, r * kY, 2000, { law: 'epp' }).M, M.eppRectM(p.b, p.h, al.E, al.sY, r * kY), 2e-6);
  }
  for (const r of [1.5, 3]) {
    const yY = p.h / 2 / r;
    check(`Beer's form (3/2)M_Y[1 − ⅓(y_Y/c)²] at κ = ${r}κ_Y`, M.eppRectM(p.b, p.h, al.E, al.sY, r * kY), 1.5 * MY * (1 - (yY / (p.h / 2)) ** 2 / 3), 1e-14);
  }
  check('rectangle: plastic modulus Z = bh²/4 (equal-area routine)', M.plasticModulus(p).Z, p.b * p.h ** 2 / 4, 1e-12);
  check('rectangle: shape factor M_p/M_Y = 1.5', M.plasticModulus(p).Z / (p.b * p.h ** 2 / 6), 1.5, 1e-12);
  const cv = M.stripConvergence(p, 3 * kY, M.eppRectM(p.b, p.h, al.E, al.sY, 3 * kY), { law: 'epp' });
  checkTrue(`strip summation converges at second order (observed ${cv.slope.toFixed(3)})`, Math.abs(cv.slope - 2) < 0.15);
  // residual stresses after unloading carry no force and no moment
  const k = 3 * kY, s = M.stripSolve(p, k, 4000, { law: 'epp' }), I = p.b * p.h ** 3 / 12, h = p.h / 4000;
  let F = 0, Mr = 0;
  for (const r of s.prof) { const sr = r.s + s.M * (r.y - p.h / 2) / I; F += sr * p.b * h; Mr += (r.y - p.h / 2) * sr * p.b * h; }
  checkAbs('residual stresses: net force / (σ_Y A) = 0', F / (al.sY * p.b * p.h), 0, 1e-6);
  checkAbs('residual stresses: net moment / M_Y = 0', Mr / MY, 0, 1e-6);
  check('inverse: κ for M = 1.3 M_Y (bisection on strips) vs the §4.6 formula inverted', M.invertKappa(p, 1.3 * MY, 2000, { law: 'epp' }), kY / Math.sqrt(3 * (1 - 1.3 / 1.5)), 1e-5);
}
{
  const p = Object.assign({}, P.ibeam), hw = p.h - 2 * p.tf;
  const Z = p.b * p.tf * (p.h - p.tf) + p.tw * hw * hw / 4;
  check('I-section: plastic modulus vs hand formula b t_f(h − t_f) + t_w h_w²/4', M.plasticModulus(p).Z, Z, 1e-12);
  check('I-section: fully plastic moment σ_Y Z vs strip summation at κ = 10⁴κ_Y', M.stripSolve(p, 1e4 * 250e6 / (200e9 * p.h / 2), 4000, { law: 'epp' }).M, 250e6 * Z, 1e-5);
  const I = p.b * p.h ** 3 / 12 - (p.b - p.tw) * hw ** 3 / 12;
  check('I-section: I vs hand formula', M.transformed(p, 1).I, I, 1e-12);
  const pt = Object.assign({}, p, { shape: 'tee' });
  const zt = M.plasticModulus(pt);
  check('T-section: fully plastic moment σ_Y Z vs strip summation', M.stripSolve(pt, 1e4 * 250e6 / (200e9 * p.h / 2), 4000, { law: 'epp' }).M, 250e6 * zt.Z, 1e-4);
  const s = M.stripSolve(pt, 1e4 * 250e6 / (200e9 * p.h / 2), 4000, { law: 'epp' });
  check('T-section: plastic neutral axis divides the area equally (strip vs equal-area routine)', s.yNA, zt.yp, 1e-3);
}
// ---------------- units ----------------
S.setSystem('US');
check('units: 1 kN·m = 8850.7 lb·in', S.conv('moment', 1000), 8850.746, 1e-6);
check('units: 1 in³ = 16 387 mm³', S.unconv('volume3', 1) * 1e9, 16387.064, 1e-7);
S.setSystem('SI');

const { text, nfail } = report('Lab 4 — simulation model (Node, exact page code)');
fs.writeFileSync(path.join(__dirname, 'results_node.md'), text + '\n');
console.log(text);
process.exit(nfail ? 1 : 0);

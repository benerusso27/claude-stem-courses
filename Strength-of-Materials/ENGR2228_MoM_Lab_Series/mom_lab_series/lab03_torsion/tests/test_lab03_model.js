/* Lab 3 verification: closed-form formulas vs independent numerical methods, exact page code.
   Run:  node tests/test_lab03_model.js   (from lab03_torsion/) */
'use strict';
const path = require('path');
const fs = require('fs');
const { loadModel, loadSimCore, check, checkAbs, checkTrue, report } = require('../../shared/test_harness.js');
const HTML = path.join(__dirname, '..', 'lab03_simulation.html');
const M = loadModel(HTML);
const S = loadSimCore(HTML);

// independent quadrature: composite Simpson on [a, b] split at given break points
function simpson(f, a, b, n = 4000) { const h = (b - a) / n; let s = f(a) + f(b); for (let i = 1; i < n; i++) s += f(a + i * h) * (i % 2 ? 4 : 2); return s * h / 3; }
function torqueSimpson(mat, c, ci, th, breaks = []) {
  const pts = [ci, ...breaks.filter((r) => r > ci && r < c).sort((x, y) => x - y), c];
  let T = 0;
  for (let i = 0; i < pts.length - 1; i++) T += simpson((r) => 2 * Math.PI * r * r * M.tauOf(mat, r * th), pts[i], pts[i + 1]);
  return T;
}

// ---------------- stress–strain laws ----------------
const steel = M.MATERIALS.steel, al = M.MATERIALS.al, ci = M.MATERIALS.ci;
check('plateau law continuous at the end of the plateau (γ_L ± 1e−9)', M.tauOf(steel, steel.gL + 1e-9), M.tauOf(steel, steel.gL - 1e-9), 1e-6);
check('plateau law: τ = τ_Y on the plateau', M.tauOf(steel, 0.01), steel.tauY, 1e-14);
for (const g of [1e-4, 3e-3, 0.05, 0.5]) {
  const t = M.tauOf(al, g);
  check(`Ramberg–Osgood inverse: γ(τ(γ)) = γ at γ = ${g}`, t / al.G + al.g0 * (t / al.tauY) ** al.m, g, 1e-12);
}
check('odd symmetry τ(−γ) = −τ(γ)', M.tauOf(steel, -0.2), -M.tauOf(steel, 0.2), 1e-15);

// ---------------- circular shafts, EPP: closed form vs ring integration ----------------
const c = 3.175e-3, G = steel.G, tY = steel.tauY, epp = { law: 'epp', G, tauY: tY };
const thY = tY / (G * c);
for (const [label, cc, cci] of [['solid', c, 0], ['hollow d_i/d = 0.6', c, 0.6 * c]]) {
  for (const k of [0.5, 1.0, 1.5, 3, 10, 100]) {
    const th = k * thY;
    const cf = M.eppTorque(cc, cci, G, tY, th);
    check(`[${label}] EPP torque at θ = ${k}θ_Y: closed form vs rings (N = 4096)`, M.torqueRings(epp, cc, cci, th, 4096), cf, 2e-7);
    check(`[${label}] EPP torque at θ = ${k}θ_Y: closed form vs Simpson quadrature`, torqueSimpson(epp, cc, cci, th, [tY / (G * th)]), cf, 1e-10);
  }
}
{
  const TY = tY * Math.PI * c ** 3 / 2;
  for (const k of [1.5, 3, 10]) {
    const rY = c / k;
    check(`Beer §3.7 form (4/3)T_Y[1 − ¼(ρ_Y/c)³] at φ = ${k}φ_Y`, M.eppTorque(c, 0, G, tY, k * thY), 4 / 3 * TY * (1 - (rY / c) ** 3 / 4), 1e-14);
  }
  check('fully plastic limit T → (4/3)T_Y (solid)', M.eppTorque(c, 0, G, tY, 1e9 * thY) / TY, 4 / 3, 1e-12);
  check('elastic: T = JGφ/L (closed form) vs rings N = 4096', M.torqueRings(epp, c, 0, 0.5 * thY, 4096), M.Jp(c, 0) * G * 0.5 * thY, 1e-7);
  const cv = M.ringConvergence(epp, c, 0, 3 * thY, M.eppTorque(c, 0, G, tY, 3 * thY));
  checkTrue(`ring integration converges at second order (observed ${cv.slope.toFixed(3)})`, Math.abs(cv.slope - 2) < 0.15);
  // inverse problem
  for (const r of [1.05, 1.2, 1.3]) {
    const T = r * TY;
    check(`inverse: twist for T = ${r}T_Y, closed form vs bisection on rings (N = 2048)`, M.invertRings(epp, c, 0, T, 2048, 1), M.eppInverseSolid(c, G, tY, T), 1e-6);
  }
  // residual stresses after unloading from 3φ_Y
  const p = { d: 2 * c, di: 0, L: 50.8e-3, phi: 3 * thY * 50.8e-3 };
  const cf = M.circClosed(p, epp);
  const prof = M.ringProfile(epp, c, 0, cf.th, 4096);
  const h = c / 4096;
  let Tres = 0; prof.r.forEach((r, i) => { Tres += 2 * Math.PI * r * r * (prof.tau[i] - cf.T * r / cf.J) * h; });
  checkAbs('residual stresses carry zero net torque (rings, relative to T)', Tres / cf.T, 0, 1e-6);
  check('permanent twist ratio φ_p/φ_Y after unloading from 3φ_Y (EPP: 3 − 1.3210)', cf.phiP / cf.phiY, 3 - 4 / 3 * (1 - 1 / 108), 1e-12);
  check('surface residual stress τ_Y − T c/J (closed form) vs rings', cf.resSurf, M.tauOf(epp, c * cf.th) - M.torqueRings(epp, c, 0, cf.th, 4096) * c / cf.J, 1e-6);
}
// ---------------- hardening laws: ring integration vs independent Simpson quadrature ----------------
for (const [name, mat, ks] of [['1018 steel (plateau + hardening)', steel, [0.5, 2, 20, 500]], ['6061-T6 (Ramberg–Osgood)', al, [0.5, 2, 20, 150]], ['cast iron (tanh)', ci, [0.5, 1, 1.4]]]) {
  for (const k of ks) {
    const th = k * mat.tauY / (mat.G * c);
    const br = [mat.tauY / (mat.G * th)].concat(mat.gL ? [mat.gL / th] : []);
    check(`[${name}] torque at θ = ${k}θ_Y: rings (N = 4096) vs Simpson`, M.torqueRings(mat, c, 0, th, 4096), torqueSimpson(mat, c, 0, th, br), 3e-7);
  }
}
// ---------------- rectangle: series vs finite differences ----------------
for (const [ab, c1, c2] of [[1, 0.208, 0.1406], [2, 0.246, 0.229], [10, 0.312, 0.312]]) {
  const s = M.rectSeries(ab, 1);
  check(`hand value (3 s.f.): c₁ for a/b = ${ab}`, s.c1, c1, 2.5e-3);
  check(`hand value (3–4 s.f.): c₂ for a/b = ${ab}`, s.c2, c2, 2.5e-3);
}
check('thin strip: c₂ → (1/3)[1 − (192/π⁵)(31/32)ζ(5) b/a] for a/b = 1000', M.rectSeries(1000, 1).c2, (1 - 192 / Math.PI ** 5 * (31 / 32) * 1.0369277551433699 * 0.001) / 3, 1e-9);
for (const ab of [1, 2, 5]) {
  const s = M.rectSeries(ab, 1), f1 = M.rectFD(ab, 1, 16), f2 = M.rectFD(ab, 1, 32);
  const rc2 = (4 * f2.c2 - f1.c2) / 3, rk = (4 * f2.k - f1.k) / 3;
  check(`[a/b = ${ab}] c₂: Richardson-extrapolated finite differences (N = 16, 32) vs series`, rc2, s.c2, 5e-5);
  check(`[a/b = ${ab}] τ_max/(Gθb): Richardson-extrapolated finite differences vs series`, rk, s.k, 2e-4);
}
{
  const cv = M.rectConvergence(2, 1, [4, 8, 16, 32]);
  checkTrue(`finite differences converge at second order for c₂ (observed ${cv.slope.toFixed(3)})`, Math.abs(cv.slope - 2) < 0.15);
  const ys = [0.1, 0.25, 0.4], a = 2, b = 1, f = M.rectFD(a, b, 32);
  for (const y of ys) {
    const j = Math.round(y / (b / f.ny));
    check(`shear along the centre line at y = ${y}b: series vs finite differences (N = 32)`, f.ts[j], M.rectSeriesMidline(a, b, j * b / f.ny), 3e-3);
  }
}
// ---------------- thin-walled tube ----------------
{
  const T = 100, Gt = 80e9;
  const b1 = M.tubeBredt(50e-3, 0.05e-3, T, Gt), e1 = M.tubeExact(50e-3, 0.05e-3, T, Gt);
  check('Bredt → exact as t/r_m → 0 (stress, t/r_m = 0.002)', b1.tau, e1.tau, 1.5e-3);
  check('Bredt → exact as t/r_m → 0 (twist)', b1.theta, e1.theta, 1e-5);
  const ex = M.tubeExact(50e-3, 5e-3, T, Gt);
  check('tube: torque from ring integration of Tρ/J equals T', M.torqueRings({ law: 'epp', G: Gt, tauY: 1e30 }, 25e-3, 20e-3, ex.theta, 4096), T, 1e-7);
}
// ---------------- presets and units ----------------
{
  const cf = M.circClosed(Object.assign({}, M.PRESETS.steel), { law: 'epp', G: steel.G, tauY: steel.tauY });
  check('preset steel specimen d = 6.35 mm: T_Y = τ_Y πc³/2 (hand: 8.547 N·m)', cf.TY, 8.547, 1e-4);
  check('preset steel specimen: φ_Y over 50.8 mm (hand: 1.960°)', cf.phiY * 180 / Math.PI, 1.960, 2e-4);
}
S.setSystem('US');
check('units: 1 N·m = 8.8507 lb·in', S.conv('moment', 1), 8.850746, 1e-6);
check('units: angle in degrees in both systems', S.conv('angle', Math.PI), 180, 1e-14);
check('units: 1 in⁴ = 416 231 mm⁴', S.unconv('inertia', 1) * 1e12, 416231.4256, 1e-9);
S.setSystem('SI');

const { text, nfail } = report('Lab 3 — simulation model (Node, exact page code)');
fs.writeFileSync(path.join(__dirname, 'results_node.md'), text + '\n');
console.log(text);
process.exit(nfail ? 1 : 0);

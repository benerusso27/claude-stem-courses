/* Lab 5 verification: closed-form formulas vs independent numerical methods, exact page code.
   Run:  node tests/test_lab05_model.js   (from lab05_shear/) */
'use strict';
const path = require('path');
const fs = require('fs');
const { loadModel, loadSimCore, check, checkAbs, checkTrue, report } = require('../../shared/test_harness.js');
const HTML = path.join(__dirname, '..', 'lab05_simulation.html');
const M = loadModel(HTML);
const S = loadSimCore(HTML);
const P = M.PRESETS;

// ---------------- sections: closed form vs hand formulas vs strip integration ----------------
{
  const p = Object.assign({}, P.rectUp), c = M.sectionClosed(p), A = p.b * p.h;
  check('rectangle: I = bh³/12', c.I, p.b * p.h ** 3 / 12, 1e-13);
  check('rectangle: Q at the NA = bh²/8', c.QNA, p.b * p.h ** 2 / 8, 1e-13);
  check('rectangle: τ_max = 3V/(2A) (Beer §6.1C)', c.tauMax(p.V), 1.5 * p.V / A, 1e-13);
  check('rectangle: energy shear factor f_s = 6/5', c.fs, 1.2, 1e-13);
  const n = M.sectionNumeric(p, 2000);
  check('rectangle: f_s by strips (N_s = 2000) vs 6/5', n.fs, 1.2, 1e-6);
  check('rectangle: I by strips (N_s = 2000)', n.I, c.I, 1e-6);
  const cv = M.stripConvergence(p);
  checkTrue(`rectangle: strip error in I falls as N_s⁻² (observed ${cv.slope.toFixed(3)})`, Math.abs(cv.slope - 2) < 0.05);
}
{
  const p = Object.assign({}, P.ibeamWeb), c = M.sectionClosed(p), hw = p.H - 2 * p.tf;
  const I = (p.B * p.H ** 3 - (p.B - p.tw) * hw ** 3) / 12;
  const QNA = p.B * p.tf * (p.H - p.tf) / 2 + p.tw * hw * hw / 8;
  check('I-section: I vs hand formula', c.I, I, 1e-13);
  check('I-section: Q at the NA = B t_f (H − t_f)/2 + t_w h_w²/8', c.QNA, QNA, 1e-13);
  check('I-section: τ in the web at the NA = VQ/(I t_w)', c.tauNA(p.V), p.V * QNA / (I * p.tw), 1e-13);
  const yj = p.H - p.tf, Qj = p.B * p.tf * (p.H - p.tf) / 2;
  check('I-section: τ in the web at the junction = V B t_f (H − t_f)/(2 I t_w)', p.V * c.Q(yj - 1e-15) / (c.I * p.tw), p.V * Qj / (I * p.tw), 1e-9);
  check('I-section: shear flow is continuous at the junction (q = VQ/I either side)', c.Q(yj - 1e-12), c.Q(yj + 1e-12), 1e-6);
  const n = M.sectionNumeric(p, 4000);
  check('I-section: f_s exact layer integral vs strips (N_s = 4000)', n.fs, c.fs, 5e-6);
  checkTrue(`I-section: f_s = ${c.fs.toFixed(4)} lies between 1 and A/A_web = ${(c.A / (hw * p.tw)).toFixed(4)}`, c.fs > 1 && c.fs < c.A / (hw * p.tw));
}
for (const k of ['tee', 'box']) {
  const p = Object.assign({}, P[k]), c = M.sectionClosed(p), n = M.sectionNumeric(p, 4000);
  check(`${k}: neutral axis, layer sums vs strips`, n.ybar, c.ybar, 1e-12);
  check(`${k}: Q at the NA, layer formula vs strips`, n.QNA, c.QNA, 1e-9);
  check(`${k}: f_s, exact integral vs strips (N_s = 4000)`, n.fs, c.fs, 5e-6);
  // Q at the NA is the same from above and from below (first moment of the whole section about the NA is zero)
  let below = 0;
  for (const l of c.layers) { const hi = Math.min(l.y1, c.ybar); if (hi > l.y0) below += l.b * ((c.ybar - l.y0) ** 2 - (c.ybar - hi) ** 2) / 2; }
  check(`${k}: Q of the area above the NA = Q of the area below`, c.QNA, below, 1e-12);
}
{
  const p = Object.assign({}, P.circle), c = M.sectionClosed(p), A = Math.PI * p.d ** 2 / 4;
  check('circle: τ_max = 4V/(3A) (Beer §6.1C)', c.tauMax(p.V), 4 * p.V / (3 * A), 1e-13);
  check('circle: f_s = 10/9 vs strips (N_s = 20000)', M.sectionNumeric(p, 20000).fs, 10 / 9, 2e-5);
  const cv = M.stripConvergence(p);
  checkTrue(`circle: strip error in I converges at order 1.5 (width ∝ √distance at the poles; observed ${cv.slope.toFixed(3)})`, Math.abs(cv.slope - 1.5) < 0.1);
}
// ---------------- wide rectangle: series vs finite differences ----------------
for (const [k, bh] of [['rectUp', 0.5], ['rectFlat', 2]]) {
  const p = P[k];
  const ser = M.rectSeries(p.b, p.h, 0.33, 1), fd = M.rectFD(p.b, p.h, 0.33, 96);
  check(`b/h = ${bh}: face value τ/(VQ/Ib), series vs finite differences (96 cells)`, fd.edge, ser, 1e-3);
  check(`b/h = ${bh}: center value, series vs finite differences`, fd.center, M.rectSeries(p.b, p.h, 0.33, 0), 1e-3);
  // equilibrium: the average of τ across the width on the NA equals VQ/(Ib) exactly (Simpson on 401 points)
  const n = 400; let s = 0;
  for (let i = 0; i <= n; i++) { const xi = -1 + 2 * i / n, wgt = i === 0 || i === n ? 1 : i % 2 ? 4 : 2; s += wgt * M.rectSeries(p.b, p.h, 0.33, xi); }
  check(`b/h = ${bh}: width-average of the elasticity solution = VQ/(Ib) (∫τ dx = VQ/I)`, s / (3 * n) * 2 / 2, 1, 1e-6);
  const cv = M.fdConvergence(p.b, p.h, 0.33);
  checkTrue(`b/h = ${bh}: finite-difference error falls as N⁻² (observed ${cv.slope.toFixed(3)})`, Math.abs(cv.slope - 2) < 0.1);
}
check('ν = 0: the elasticity solution is the elementary one (b/h = 2)', M.rectSeries(2, 1, 0, 1), 1, 1e-14);
for (const [bh, v] of [[0.5, 1.033], [2, 1.396], [4, 1.988]]) check(`ν = 0.25, b/h = ${bh}: face value matches the value tabulated in Beer §6.1C (3 figures)`, M.rectSeries(bh, 1, 0.25, 1), v, 5e-4);
// ---------------- Timoshenko beam: closed form vs finite elements ----------------
for (const k of ['ibeamSpan', 'cantilever']) {
  const p = Object.assign({}, P[k]), t = M.timoClosed(p);
  check(`[${k}] deflection: closed form vs 256 reduced-integration elements`, M.timoFE(p, 256, 'reduced').delta, t.total, 2e-5);
  const cv = M.feConvergence(p, 'reduced');
  checkTrue(`[${k}] element error falls as N_e⁻² (observed ${cv.slope.toFixed(3)})`, Math.abs(cv.slope - 2) < 0.1);
  check(`[${k}] span with a 5 % shear part: closed form vs bisection on the elements`, M.feL5(p, 128), t.L5, 2e-3);
  const fe = M.timoFE(Object.assign({}, p, { L: 50 * M.depthOf(p) }), 64, 'reduced'), tl = M.timoClosed(Object.assign({}, p, { L: 50 * M.depthOf(p) }));
  check(`[${k}] slender limit (L/h = 50): elements → Euler–Bernoulli within the shear part`, fe.delta, tl.bend, 1.5 * tl.shear / tl.bend);
}
{
  const p = Object.assign({}, P.cantilever, { L: 1.0 }), t = M.timoClosed(p), full = M.timoFE(p, 4, 'full').delta;
  checkTrue(`shear locking: 4 fully integrated elements give ${(100 * full / t.total).toFixed(1)} % of the deflection (< 50 %)`, full / t.total < 0.5);
  check('rectangle: δ_shear/δ_bending = 3EI f_s/(GA L²) for a cantilever (closed form vs formula)', t.shear / t.bend, 3 * t.EI * 1.2 / (t.G * t.sec.A * p.L * p.L), 1e-12);
}
// ---------------- built-up beam: closed form vs finite differences vs discrete springs ----------------
const lcases = [['bolts, point load', Object.assign({}, P.layered)], ['glue, point load', Object.assign({}, P.layered, { conn: 'glue' })],
  ['bolts, uniform load', Object.assign({}, P.design, { s1: 0.1, s2: 0.1 })], ['loose, point load', Object.assign({}, P.layered, { conn: 'loose' })],
  ['loose, uniform load', Object.assign({}, P.design, { conn: 'loose' })], ['soft glue, uniform load', Object.assign({}, P.design, { conn: 'glue', Gg: 30e6, tg: 1e-3 })]];
for (const [name, p] of lcases) {
  const c = M.newmarkClosed(p), f = M.newmarkFD(p, 4000);
  check(`[${name}] midspan deflection: closed form vs finite differences (4000 intervals)`, f.delta, c.delta, 2e-6);
  check(`[${name}] end slip: closed form vs finite differences`, f.slip0, c.slip0, 2e-4);
  checkTrue(`[${name}] δ_full ≤ δ ≤ δ_loose`, c.delta >= c.deltaFull * (1 - 1e-12) && c.delta <= c.deltaLoose * (1 + 1e-12));
}
{
  const p = Object.assign({}, P.layered), g = M.layerGeom(p);
  check('loose limit: k → 0 gives PL³/(48EI₀)', M.newmarkClosed(p, 1e-6).delta, p.P * p.L ** 3 / (48 * g.EI0), 1e-9);
  check('bonded limit: k → ∞ gives PL³/(48EI_full)', M.newmarkClosed(p, 1e16).delta, p.P * p.L ** 3 / (48 * g.EIfull), 1e-6);
  check('two equal layers: EI_full = 4 EI₀', g.EIfull / g.EI0, 4, 1e-12);
  check('loose end slip = r θ_end = r PL²/(16EI₀)', M.newmarkClosed(Object.assign({}, p, { conn: 'loose' })).slip0, g.r * p.P * p.L ** 2 / (16 * g.EI0), 1e-12);
  const kz = (z) => (z / (p.L / 2)) ** 2 / (1 / g.EAs + g.r ** 2 / g.EI0);
  check('closed form: small-αL series and full formula join at αL/2 = 0.05 (point load)', M.newmarkClosed(p, kz(0.05 * (1 - 1e-9))).delta, M.newmarkClosed(p, kz(0.05 * (1 + 1e-9))).delta, 1e-9);
  const pu = Object.assign({}, P.design), gu = M.layerGeom(pu), kzu = (z) => (z / (pu.L / 2)) ** 2 / (1 / gu.EAs + gu.r ** 2 / gu.EI0);
  check('closed form: series and full formula join at αL/2 = 0.05 (uniform load)', M.newmarkClosed(pu, kzu(0.05 * (1 - 1e-9))).delta, M.newmarkClosed(pu, kzu(0.05 * (1 + 1e-9))).delta, 1e-9);
  const cv = M.layerConvergence(p);
  checkTrue(`finite-difference error falls as n⁻² (observed ${cv.slope.toFixed(3)})`, Math.abs(cv.slope - 2) < 0.1);
  // discrete springs → smeared connection as the spacing shrinks (same k per unit length)
  const kpl = p.kb / p.s1, fine = Object.assign({}, p, { s1: 0.005, s2: 0.005, kb: kpl * 0.005 });
  check('discrete springs at 5 mm spacing → smeared closed form', M.boltsDiscrete(fine).delta, M.newmarkClosed(p).delta, 2e-4);
  const d = M.boltsDiscrete(p);
  checkAbs('discrete springs: shooting leaves N(L) = 0 (relative to the largest bolt force)', d.residual / Math.max(...d.forces.map((x) => Math.abs(x.F))), 0, 1e-10);
  check('discrete springs: forces antisymmetric about midspan', d.forces[0].F, -d.forces[d.forces.length - 1].F, 1e-9);
  // Beer's q·s for a rigid connection: q = VQ/I with V = P/2, Q = b t² /2, I = b(2t)³/12 → q = 3V/(4t)
  check("Beer's q for two equal layers = 3V/(4t)", M.beerBoltForces(p)[0].F / p.s1, 3 * (p.P / 2) / (4 * p.t1), 1e-12);
}
// ---------------- units ----------------
S.setSystem('US');
check('units: 1 N/mm = 5.7101 lb/in', S.conv('shearflow', 1000), 5.710147, 1e-6);
check('units: 1 kN/mm = 5.7101 kip/in', S.conv('stiffness', 1e6), 5.710147, 1e-6);
check('units: 1 N·m² = 348.45 lb·in²', S.conv('rigidity', 1), 1 / (4.4482216152605 * 0.0254 ** 2), 1e-12);
S.setSystem('SI');

const { text, nfail } = report('Lab 5 — simulation model (Node, exact page code)');
fs.writeFileSync(path.join(__dirname, 'results_node.md'), text + '\n');
console.log(text);
process.exit(nfail ? 1 : 0);

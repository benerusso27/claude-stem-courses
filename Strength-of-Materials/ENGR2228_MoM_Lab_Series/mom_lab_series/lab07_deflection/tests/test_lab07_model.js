/* Lab 7 verification: closed-form formulas vs independent numerical methods, exact page code, plus a comparison of the
   page's port of the finite-element solver with the instructor's compiled beam_deflection.cpp.
   Run:  node tests/test_lab07_model.js   (from lab07_deflection/) */
'use strict';
const path = require('path');
const fs = require('fs');
const os = require('os');
const { execFileSync } = require('child_process');
const { loadModel, loadSimCore, check, checkAbs, checkTrue, report } = require('../../shared/test_harness.js');
const HTML = path.join(__dirname, '..', 'lab07_simulation.html');
const M = loadModel(HTML);
const S = loadSimCore(HTML);
const P = M.PRESETS;
const EIof = (p) => M.MATERIALS[p.mat].E * M.section(p).I;

// ---------------- Beer App. F, cases 1-7 (y up; values typed from the table's formulas) ----------------
{
  const p = P.F1, EI = EIof(p), c = M.closedForm(p), L = p.L, Pl = p.P1;
  check('App. F 1: y_max = −PL³/3EI', c.y(L), -Pl * L ** 3 / (3 * EI), 1e-13);
  check('App. F 1: slope at the end = −PL²/2EI', c.t(L), -Pl * L * L / (2 * EI), 1e-13);
  check('App. F 1: elastic curve y = P(x³ − 3Lx²)/6EI at x = 0.4L', c.y(0.4 * L), Pl * ((0.4 * L) ** 3 - 3 * L * (0.4 * L) ** 2) / (6 * EI), 1e-13);
}
{
  const p = P.F2, EI = EIof(p), c = M.closedForm(p), L = p.L, w = p.w;
  check('App. F 2: y_max = −wL⁴/8EI', c.y(L), -w * L ** 4 / (8 * EI), 1e-13);
  check('App. F 2: slope at the end = −wL³/6EI', c.t(L), -w * L ** 3 / (6 * EI), 1e-13);
}
{
  const p = P.F3, EI = EIof(p), c = M.closedForm(p), L = p.L, Mm = -p.C0;     // Beer's M drawn clockwise
  check('App. F 3: y_max = −ML²/2EI (clockwise end couple)', c.y(L), -Mm * L * L / (2 * EI), 1e-13);
  check('App. F 3: slope at the end = −ML/EI', c.t(L), -Mm * L / EI, 1e-13);
}
{
  const p = P.F4, EI = EIof(p), c = M.closedForm(p), L = p.L, Pl = p.P1;
  check('App. F 4: y_max = −PL³/48EI', c.y(L / 2), -Pl * L ** 3 / (48 * EI), 1e-13);
  check('App. F 4: slope at A = −PL²/16EI', c.t(0), -Pl * L * L / (16 * EI), 1e-13);
}
{
  const p = P.F5, EI = EIof(p), c = M.closedForm(p), L = p.L, Pl = p.P1, a = p.a1, b = L - a, xm = Math.sqrt((L * L - b * b) / 3);
  check('App. F 5: y_max = −Pb(L² − b²)^{3/2}/(9√3 EIL) at x_m = √((L² − b²)/3)', c.y(xm), -Pl * b * (L * L - b * b) ** 1.5 / (9 * Math.sqrt(3) * EI * L), 1e-12);
  checkAbs('App. F 5: slope is zero at x_m', c.t(xm) * EI / (Pl * L * L), 0, 1e-13);
  check('App. F 5: θ_A = −Pb(L² − b²)/6EIL', c.t(0), -Pl * b * (L * L - b * b) / (6 * EI * L), 1e-13);
  check('App. F 5: θ_B = +Pa(L² − a²)/6EIL', c.t(L), Pl * a * (L * L - a * a) / (6 * EI * L), 1e-13);
  check('App. F 5: y under the load = −Pa²b²/3EIL', c.y(a), -Pl * a * a * b * b / (3 * EI * L), 1e-13);
}
{
  const p = P.F6, EI = EIof(p), c = M.closedForm(p), L = p.L, w = p.w;
  check('App. F 6: y_max = −5wL⁴/384EI', c.y(L / 2), -5 * w * L ** 4 / (384 * EI), 1e-13);
  check('App. F 6: slope at A = −wL³/24EI', c.t(0), -w * L ** 3 / (24 * EI), 1e-13);
}
{
  const p = P.F7, EI = EIof(p), c = M.closedForm(p), L = p.L, Mm = -p.C0;     // Beer's M at B, drawn clockwise
  check('App. F 7: y_max = ML²/(9√3 EI) at x = L/√3 (bows upward)', c.y(L / Math.sqrt(3)), Mm * L * L / (9 * Math.sqrt(3) * EI), 1e-12);
  check('App. F 7: θ_A = +ML/6EI', c.t(0), Mm * L / (6 * EI), 1e-13);
  check('App. F 7: θ_B = −ML/3EI', c.t(L), -Mm * L / (3 * EI), 1e-13);
}
{
  const p = P.fixedw, EI = EIof(p), c = M.closedForm(p), L = p.L, w = p.w;
  check('fixed at both ends, uniform load: y_max = −wL⁴/384EI', c.y(L / 2), -w * L ** 4 / (384 * EI), 1e-11);
  check('fixed at both ends: end moments wL²/12', c.R.MA, w * L * L / 12, 1e-11);
  const q = Object.assign({}, P.F4, { family: 'fixed' }), cq = M.closedForm(q);
  check('fixed at both ends, central load: y_max = −PL³/192EI', cq.y(q.L / 2), -q.P1 * q.L ** 3 / (192 * EIof(q)), 1e-11);
}
{
  const p = Object.assign({}, P.partB2, { rigid: true }), c = M.closedForm(p);
  check('propped cantilever, central load, rigid clamp: R_B = 5P/16 (§9.2)', c.R.RB, 5 * p.P1 / 16, 1e-12);
  check('propped cantilever: wall moment 3PL/16', c.R.MA, 3 * p.P1 * p.L / 16, 1e-12);
  const pw = Object.assign({}, p, { P1: 0, w: 1000 }), cw = M.closedForm(pw);
  check('propped cantilever, uniform load: R_B = 3wL/8', cw.R.RB, 3 * 1000 * p.L / 8, 1e-12);
  const soft = M.closedForm(Object.assign({}, p, { rigid: false, k: 1e-6 }));
  check('propped cantilever with k → 0 becomes a simple span: R_B → P/2', soft.R.RB, p.P1 / 2, 1e-6);
  const EI = EIof(p), d = -0.5e-3, cs = M.closedForm(Object.assign({}, p, { s: d }));
  check('settlement Δ of the prop changes R_B by 3EIΔ/L³ (rigid clamp)', cs.R.RB - c.R.RB, 3 * EI * d / p.L ** 3, 1e-10);
  const k = 4400, ck = M.closedForm(Object.assign({}, p, { rigid: false, k })), cks = M.closedForm(Object.assign({}, p, { rigid: false, k, s: d }));
  check('settlement with a flexible clamp: ΔR_B = Δ/(L³/3EI + L²/k)', cks.R.RB - ck.R.RB, d / (p.L ** 3 / (3 * EI) + p.L ** 2 / k), 1e-10);
  const cb = M.closedForm(Object.assign({}, P.partB1, { rigid: false, k })), L = P.partB1.L, Pl = P.partB1.P1;
  check('cantilever with a flexible clamp: tip deflection PL³/3EI + PL²/k', -cb.y(L), Pl * L ** 3 / (3 * EI) + Pl * L * L / k, 1e-12);
}

// ---------------- finite elements (port of beam_deflection.cpp) vs closed forms, every beam preset ----------------
for (const k of Object.keys(P)) {
  const p = P[k];
  if (p.mode === 'elastica') continue;
  for (const variant of [{}, { rigid: false, k: 5 * EIof(p) / p.L }]) {
    if (variant.rigid === false && (p.family === 'ss' || !p.rigid)) continue;
    const q = Object.assign({}, p, variant), c = M.closedForm(q), f = M.feSolve(q), Lt = c.Lt;
    const xs = Array.from({ length: 241 }, (_, i) => Lt * i / 240);
    const ym = Math.max(...xs.map((x) => Math.abs(c.y(x))));
    const tm = Math.max(...xs.map((x) => Math.abs(c.t(x))));
    const tag = `[${k}${variant.k ? ', clamp k = 5EI/L' : ''}]`;
    checkAbs(`${tag} elastic curve: FE vs closed form, max |Δy|/|y|max`, Math.max(...xs.map((x) => Math.abs(f.y(x) - c.y(x)))) / ym, 0, 1e-7);
    checkAbs(`${tag} slope: FE vs closed form, max |Δθ|/|θ|max`, Math.max(...xs.map((x) => Math.abs(f.t(x) - c.t(x)))) / tm, 0, 1e-7);
    const W = Math.abs(q.P1) + Math.abs(q.P2) + q.w * Lt + Math.abs(q.C0) / Lt;
    checkAbs(`${tag} reaction at the left support: FE vs closed form (relative to the total load)`, (f.reactions[0].F_up - c.R.RA) / W, 0, 1e-7);
    if (f.reactions.length > 1) checkAbs(`${tag} reaction at the right support`, (f.reactions[1].F_up - c.R.RB) / W, 0, 1e-7);
    if (q.family !== 'ss') checkAbs(`${tag} reaction couple at the left: FE vs closed form (relative to W·L)`, (f.reactions[0].M_ccw - c.R.MA) / (W * Lt), 0, 1e-7);
    // equilibrium of the FE reactions
    let sF = -q.w * Lt, sM = 0;
    for (const [Pp, a] of M.pointLoads(q)) { sF -= Pp; sM -= Pp * a; }
    sM -= q.w * Lt * Lt / 2; sM += q.C0;
    for (const r of f.reactions) { sF += r.F_up; sM += r.F_up * r.x + r.M_ccw; }
    checkAbs(`${tag} FE reactions satisfy ΣF = 0 and ΣM = 0 (relative)`, Math.hypot(sF / W, sM / (W * Lt)), 0, 1e-7);
  }
}
{
  // superposition and reciprocity with the FE solver itself
  const a = Object.assign({}, P.partA, { P1: 10, a1: 0.6, P2: 0 }), b = Object.assign({}, P.partA, { P1: 10, a1: 0.2, P2: 0 }), ab = Object.assign({}, P.partA, { P1: 10, a1: 0.6, P2: 10, a2: 0.2 });
  const fa = M.feSolve(a), fb = M.feSolve(b), fab = M.feSolve(ab);
  checkAbs('superposition: FE(both loads) − FE(load 1) − FE(load 2) at 400 mm (relative)', (fab.y(0.4) - fa.y(0.4) - fb.y(0.4)) / fab.y(0.4), 0, 1e-9);
  check('Maxwell reciprocity: y at 200 mm under 10 N at 600 = y at 600 under 10 N at 200 (FE)', fa.y(0.2), fb.y(0.6), 1e-8);
}
{
  const p = Object.assign({}, P.F6), cv = M.beamConvergence(p);
  checkTrue(`uniform load: FE deflection between nodes converges as N⁻⁴ (observed ${cv.slope.toFixed(3)})`, Math.abs(cv.slope - 4) < 0.15);
  checkTrue(`uniform load: FE moment EI·y″ converges as N⁻² (observed ${cv.slopeM.toFixed(3)})`, Math.abs(cv.slopeM - 2) < 0.1);
  const f = M.feSolve(p, 2), c = M.closedForm(p);
  check('uniform load, 2 elements: nodal deflection already exact (superconvergence)', f.y(p.L / 2), c.y(p.L / 2), 1e-8);
  const pp = M.beamConvergence(P.F5);
  checkTrue(`point load: FE exact at every mesh (largest error ${Math.max(...pp.rows.map((r) => r.err)).toExponential(1)})`, Math.max(...pp.rows.map((r) => r.err)) < 1e-8);
}

// ---------------- the port vs the compiled C++ program ----------------
{
  const exe = path.join(os.tmpdir(), 'lab07_cpp_driver_' + process.pid);
  let ran = false;
  try {
    execFileSync('g++', ['-std=c++17', '-O2', '-o', exe, path.join(__dirname, 'cpp_driver.cpp')], { stdio: 'pipe' });
    const beams = ['partA', 'partAboth', 'partB2', 'design', 'F2', 'F3', 'F5', 'F7', 'fixedw'].map((k) => [k, Object.assign({}, P[k], { rigid: true, s: 0, Ne: 60 })]);
    beams.push(['triangle', { bm: { L: 3, E: 200e9, I: 8e-6, supports: [{ type: 'Pin', x: 0 }, { type: 'Roller', x: 2.2 }], loads: [{ type: 'D', a: 0.5, b: 3, q1: 0, q2: 4000 }, { type: 'P', a: 3, b: 3, q1: 1500, q2: 0 }, { type: 'C', a: 1.1, b: 1.1, q1: 800, q2: 0 }] } }]);
    const toTxt = (bm, Ne) => {
      const t = { Pin: 'P', Roller: 'R', Fixed: 'F' };
      return [`${bm.L} ${bm.E} ${bm.I} ${Ne}`, `${bm.supports.length}`, ...bm.supports.map((s) => `${t[s.type]} ${s.x}`), `${bm.loads.length}`, ...bm.loads.map((l) => `${l.type} ${l.a} ${l.b} ${l.q1} ${l.q2}`)].join('\n');
    };
    const list = beams.map(([k, p]) => [k, p.bm || M.cppBeam(p), p.Ne || 60]);
    const out = JSON.parse(execFileSync(exe, { input: list.map(([, bm, Ne]) => toTxt(bm, Ne)).join('\n') + '\n' }).toString());
    list.forEach(([k, bm, Ne], i) => {
      const js = M.solveBeam(bm, Ne), cc = out[i];
      checkTrue(`C++ reference [${k}]: same mesh (${cc.x.length} nodes)`, js.ok && cc.ok && cc.x.length === js.xn.length && cc.x.every((x, j) => Math.abs(x - js.xn[j]) < 1e-14 * bm.L));
      const ym = Math.max(...cc.y.map(Math.abs)), tm = Math.max(...cc.t.map(Math.abs));
      checkAbs(`C++ reference [${k}]: nodal deflections, JS port vs C++ (max |Δ|/|y|max)`, Math.max(...cc.y.map((v, j) => Math.abs(v - js.yn[j]))) / ym, 0, 1e-9);
      checkAbs(`C++ reference [${k}]: nodal slopes, JS port vs C++`, Math.max(...cc.t.map((v, j) => Math.abs(v - js.tn[j]))) / tm, 0, 1e-9);
      const Rm = Math.max(...cc.R.map((r) => Math.abs(r[1])));
      checkAbs(`C++ reference [${k}]: reactions (force and couple), JS port vs C++`, Math.max(...cc.R.map((r, j) => Math.max(Math.abs(r[1] - js.reactions[j].F_up) / Rm, Math.abs(r[2] - js.reactions[j].M_cw) / (Rm * bm.L)))), 0, 1e-9);
    });
    ran = true;
  } catch (e) { checkTrue('C++ reference: compiled and ran (g++ needed)', false, String(e).slice(0, 120)); }
  try { fs.unlinkSync(exe); } catch (e) { /* not created */ }
  if (ran) checkTrue('C++ reference: all beams compared', true);
}

// ---------------- elastica ----------------
{
  check('Carlson R_F: K(m = 0.5) = 1.8540746773013719', M.ellF(Math.PI / 2, 0.5), 1.8540746773013719, 1e-13);
  check('Carlson R_D: E(m = 0.5) = 1.3506438810476755', M.ellE(Math.PI / 2, 0.5), 1.3506438810476755, 1e-13);
  check('incomplete F(π/4, m = 0.3) = 0.80436 (series check)', M.ellF(Math.PI / 4, 0.3), (() => { let s = 0; const n = 20000; for (let i = 0; i < n; i++) { const ph = (i + 0.5) * (Math.PI / 4) / n; s += 1 / Math.sqrt(1 - 0.3 * Math.sin(ph) ** 2); } return s * (Math.PI / 4) / n; })(), 1e-8);
  for (const a of [0.05, 0.5, 1, 2, 3, 5]) {
    const c = M.elasticaClosed(a), n = M.elasticaShoot(a, 0, 400);
    check(`elastica α = ${a}: tip deflection, closed form vs RK4 shooting (N = 400)`, n.dv, c.dv, 1e-9);
    check(`elastica α = ${a}: tip angle`, n.th0, c.th0, 1e-9);
    check(`elastica α = ${a}: tip x-position`, n.xt, c.xt, 1e-9);
    const sh = c.shape(50), last = sh[sh.length - 1];
    check(`elastica α = ${a}: closed-form shape ends at the closed-form tip`, -last.y, c.dv, 1e-12);
    check(`elastica α = ${a}: arc length of the closed-form shape = L`, last.s, 1, 1e-12);
  }
  check('elastica, small load: δ_v/L → α/3 (α = 0.001)', M.elasticaClosed(0.001).dv, 0.001 / 3, 1e-6);
  check('elastica, small load: tip angle → α/2', M.elasticaClosed(0.001).th0, 0.0005, 1e-6);
  check('linear theory is 5 % high at α = 0.67564 (bisection)', M.alpha5(), 0.6756366713616627, 1e-9);
  const cv = M.elasticaConvergence(1.0);
  checkTrue(`RK4 shooting converges as N⁻⁴ (observed ${cv.slope.toFixed(3)})`, Math.abs(cv.slope - 4) < 0.15);
  const sw = M.elasticaShoot(0, 0.01, 400);
  check('self-weight only, small: tip deflection → βL/8', sw.dv, 0.01 / 8, 2e-3);
  const sp = M.stripProps(P.partC);
  checkTrue(`Part C preset reaches α = ${sp.alpha.toFixed(2)} > 3`, sp.alpha > 3);
}

// ---------------- units ----------------
{
  S.setSystem('US');
  check('units: 10 N in lbf', S.conv('forceN', 10), 10 / 4.4482216152605, 1e-12);
  check('units: 2 kN/m in kip/ft', S.conv('lineload', 2000), 2 * 0.3048 / 4.4482216152605, 1e-12);
  check('units: 4500 N·m/rad in lb·in/rad', S.conv('rotstiff', 4500), 4500 / (4.4482216152605 * 0.0254), 1e-12);
  S.setSystem('SI');
}

const r = report('Lab 7 model tests (exact page code, and the C++ reference)');
fs.writeFileSync(path.join(__dirname, 'results_node.md'), r.text + '\n');
console.log(r.text);
process.exit(r.nfail ? 1 : 0);

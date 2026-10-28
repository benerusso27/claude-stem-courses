/* Lab 6 verification: closed-form formulas vs independent numerical methods, exact page code.
   Run:  node tests/test_lab06_model.js   (from lab06_eccentric/) */
'use strict';
const path = require('path');
const fs = require('fs');
const { loadModel, loadSimCore, check, checkAbs, checkTrue, report } = require('../../shared/test_harness.js');
const HTML = path.join(__dirname, '..', 'lab06_simulation.html');
const M = loadModel(HTML);
const S = loadSimCore(HTML);
const PP = (k, o = {}) => Object.assign(M.presetParams(k), o);

// ---------------- sections: closed form vs hand formulas ----------------
{
  const p = PP('partA2'), c = M.sectionClosed(p), h = p.h, b = p.b, A = b * h;
  check('rectangle: A = bh', c.A, A, 1e-14);
  check('rectangle: I_z = bh³/12', c.Iz, b * h ** 3 / 12, 1e-13);
  check('rectangle: I_y = hb³/12', c.Iy, h * b ** 3 / 12, 1e-13);
  checkAbs('rectangle: I_yz = 0', c.Iyz, 0, 1e-20);
  checkAbs('rectangle (h > b): major axis along z, θp = 0', c.th, 0, 1e-12);
  const e = p.ey, P = p.P;
  check('rectangle, e = h/3 class: σ_max = (P/A)(1 + 6e/h) (Beer Eq. 4.50)', M.stressClosed(c, P, e, 0, h / 2, 0), P / A * (1 + 6 * e / h), 1e-13);
  check('rectangle: σ_min = (P/A)(1 − 6e/h)', M.stressClosed(c, P, e, 0, -h / 2, 0), P / A * (1 - 6 * e / h), 1e-12);
  const pl = M.planeClosed(c, P, e, 0);
  check('rectangle: neutral axis y₀ = −r²/e = −h²/(12e)', -pl.s0 / pl.By, -(h * h / 12) / e, 1e-12);
  const kc = M.kernClosed(p, c);
  const kmax = Math.max(...kc.map((v) => Math.abs(v[0]))), kzmax = Math.max(...kc.map((v) => Math.abs(v[1])));
  check('rectangle: kern half-diagonal along y = h/6', kmax, h / 6, 1e-12);
  check('rectangle: kern half-diagonal along z = b/6', kzmax, b / 6, 1e-12);
  check('rectangle: kern area = hb/18', M.polyArea(kc), h * b / 18, 1e-12);
  checkAbs('rectangle, load at the kern vertex (h/6, 0): σ at the far edge = 0 (in units of P/A)', M.stressClosed(c, P, h / 6, 0, -h / 2, 0) / (P / A), 0, 1e-12);
}
{
  // equal-leg angle: two rectangles and the parallel-axis theorem, typed independently
  const p = PP('partB'), c = M.sectionClosed(p), b = p.bV, t = p.t;
  const A1 = b * t, A2 = (b - t) * t, A = A1 + A2;
  const zbar = (A1 * (-t / 2) + A2 * (-(t + b) / 2)) / A, ybar = (A1 * (b / 2) + A2 * (t / 2)) / A;
  const Iz = t * b ** 3 / 12 + A1 * (b / 2 - ybar) ** 2 + (b - t) * t ** 3 / 12 + A2 * (t / 2 - ybar) ** 2;
  const Iyz = A1 * (-t / 2 - zbar) * (b / 2 - ybar) + A2 * (-(t + b) / 2 - zbar) * (t / 2 - ybar);
  check('angle: area', c.A, A, 1e-13);
  check('angle: centroid y', c.yc, ybar, 1e-12);
  check('angle: centroid z', c.zc, zbar, 1e-12);
  check('angle: I_z by parallel axes', c.Iz, Iz, 1e-12);
  check('equal-leg angle: I_y = I_z', c.Iy, c.Iz, 1e-12);
  check('angle: I_yz by parallel axes (own products zero)', c.Iyz, Iyz, 1e-12);
  check('equal-leg angle: θp = −45° (major axis along the line of symmetry)', c.th, -Math.PI / 4, 1e-12);
  check('equal-leg angle: I_max = I_z + |I_yz|', c.Imax, Iz + Math.abs(Iyz), 1e-12);
  check('equal-leg angle: I_min = I_z − |I_yz|', c.Imin, Iz - Math.abs(Iyz), 1e-12);
  // AA/AISC tabulated value for L2 × 2 × 1/4: r_min = 0.391 in
  check('angle L2 × 2 × 1/4: r_min = 0.391 in (handbook, 3 significant figures)', Math.sqrt(c.Imin / c.A) / 0.0254, 0.391, 2e-3);
}
{
  const r = 4.8e-3, q = M.partIntegrals({ kind: 'spandrel', zc: -6.35e-3, yc: 6.35e-3, r });
  check('fillet (spandrel): area = (1 − π/4) r²', q.A, (1 - Math.PI / 4) * r * r, 1e-12);
  check('fillet: centroid 0.2234 r from each straight edge = r(10 − 3π)/(3(4 − π))', -6.35e-3 - q.Sz / q.A, r * (10 - 3 * Math.PI) / (3 * (4 - Math.PI)), 1e-11);
  check('fillet: centroid height above the leg face, same distance (symmetry)', q.Sy / q.A - 6.35e-3, r * (10 - 3 * Math.PI) / (3 * (4 - Math.PI)), 1e-11);
}
{
  const p = PP('tube8', { mode: 'section' }), c = M.sectionClosed(p), ro = p.Do / 2, ri = p.Di / 2;
  check('tube: I = π(c₂⁴ − c₁⁴)/4', c.Iz, Math.PI * (ro ** 4 - ri ** 4) / 4, 1e-13);
  const kc = M.kernClosed(p, c);
  check('tube: kern radius = (c₂² + c₁²)/(4c₂)', Math.hypot(...kc[0]), (ro * ro + ri * ri) / (4 * ro), 1e-13);
}

// ---------------- sections: closed form vs grid integration, for every shape ----------------
const SHAPES = [['partA2', {}], ['partB', {}], ['partB', { r: 4.8e-3 }], ['tee', {}], ['zsec', {}], ['design', {}], ['partA2', { shape: 'channel', B: 60e-3, H: 120e-3, tf: 8e-3, tw: 6e-3, ey: 10e-3, ez: 15e-3 }], ['tube8', { mode: 'section', P: 20e3, ey: 5e-3, ez: -8e-3 }]];
for (const [k, o] of SHAPES) {
  const p = PP(k, o), c = M.sectionClosed(p), n = M.sectionNumeric(p, 512), tag = `${p.shape}${p.r ? ' with fillet' : ''} [${k}]`;
  check(`${tag}: A, exact parts vs grid (N_g = 512)`, n.A, c.A, 1e-9);
  check(`${tag}: I_z, exact parts vs grid`, n.Iz, c.Iz, 2e-5);
  check(`${tag}: I_y, exact parts vs grid`, n.Iy, c.Iy, 2e-5);
  if (Math.abs(c.Iyz) > 1e-6 * c.Imax) check(`${tag}: I_yz, exact parts vs grid`, n.Iyz, c.Iyz, 2e-5);
  check(`${tag}: I_min, Mohr formula vs grid`, n.Imin, c.Imin, 2e-5);
  // principal angle: product of inertia in the rotated axes must vanish (independent check of tan 2θp)
  const th = c.th, Iuv = (c.Iz - c.Iy) / 2 * Math.sin(2 * th) + c.Iyz * Math.cos(2 * th);
  checkAbs(`${tag}: product of inertia in the principal axes = 0`, Iuv / c.Imax, 0, 1e-12);
  const Iu = (c.Iz + c.Iy) / 2 + (c.Iz - c.Iy) / 2 * Math.cos(2 * th) - c.Iyz * Math.sin(2 * th);
  check(`${tag}: θp points to the MAJOR axis (I about u = I_max)`, Iu, c.Imax, 1e-12);
  // stresses: Eq. 4.58 (principal axes) vs grid + 3 × 3 equilibrium solve in the drawing axes
  const P = Math.abs(p.P) > 0 ? p.P : 1e4, pn = M.planeNumeric(n, P, c.zc + p.ez, c.yc + p.ey);
  const vc = c.hull.map(([z, y]) => M.stressClosed(c, P, p.ey, p.ez, y - c.yc, z - c.zc)), vn = c.hull.map(([z, y]) => pn.at(z, y));
  const sc = Math.max(...vc.map(Math.abs));
  checkAbs(`${tag}: corner stresses, Eq. 4.58 vs equilibrium solve (max |Δ|/σ_max)`, Math.max(...vc.map((v, i) => Math.abs(v - vn[i]))) / sc, 0, 2e-4);
  // equilibrium of the closed-form stress, integrated on the grid
  let F = 0, My = 0, Mz = 0;
  for (const [z, y, w] of (() => { const cells = []; const nn = M.sectionNumeric(p, 256); void nn; return cells; })()) { F += w; My += w * z; Mz += w * y; }
  const n2 = M.sectionNumeric(p, 256), pl = M.planeClosed(c, P, p.ey, p.ez);
  const S2 = n2.S, s0 = pl.s0 - pl.By * c.yc - pl.Bz * c.zc;        // σ = s0 + By y + Bz z in drawing axes
  check(`${tag}: ∫σ dA = P`, s0 * S2.A + pl.By * S2.Sy + pl.Bz * S2.Sz, P, 1e-4);
  check(`${tag}: ∫σ y dA = P y_P (moment of the load)`, s0 * S2.Sy + pl.By * S2.Jyy + pl.Bz * S2.Jzy, P * (c.yc + p.ey), 1e-4);
  if (Math.abs(c.zc + p.ez) > 1e-6) check(`${tag}: ∫σ z dA = P z_P`, s0 * S2.Sz + pl.By * S2.Jzy + pl.Bz * S2.Jzz, P * (c.zc + p.ez), 1e-4);
  // kern: closed form (antipoles) vs bisection along rays, and σ = 0 on the hull edge for each kern vertex
  const kc = M.kernClosed(p, c), kn = M.kernNumeric(p, n, c.hull, 720);
  check(`${tag}: kern area, antipoles vs 720-ray bisection`, M.polyArea(kn), M.polyArea(kc), 5e-4);
  if (p.shape !== 'tube') {
    let worst = 0;
    kc.forEach(([y, z], i) => { const a = c.hull[i], b2 = c.hull[(i + 1) % c.hull.length]; for (const [zz, yy] of [a, b2]) worst = Math.max(worst, Math.abs(M.stressClosed(c, 1, y, z, yy - c.yc, zz - c.zc)) * c.A); });
    checkAbs(`${tag}: load at each kern vertex puts σ = 0 along its hull edge`, worst, 0, 1e-10);
  }
  const cv = M.sectionConvergence(p);
  checkTrue(`${tag}: grid error in I_min falls as N_g⁻² (observed ${cv.slope.toFixed(3)})`, Math.abs(cv.slope - 2) < 0.1);
}
{
  const p = PP('partB'), c = M.sectionClosed(p);
  const worst = Math.max(...c.hull.map(([z, y]) => Math.abs(M.stressNaive(c, p.P, p.ey, p.ez, y - c.yc, z - c.zc) - M.stressClosed(c, p.P, p.ey, p.ez, y - c.yc, z - c.zc)))) / (p.P / c.A);
  checkTrue(`angle: ignoring I_yz changes a corner stress by ${worst.toFixed(2)} P/A (> 1)`, worst > 1);
  const q = PP('partA2'), cq = M.sectionClosed(q);
  checkAbs('rectangle: the "naive" formula is exact when I_yz = 0', M.stressNaive(cq, q.P, q.ey, 0.002, q.h / 2, q.b / 2) - M.stressClosed(cq, q.P, q.ey, 0.002, q.h / 2, q.b / 2), 0, 1e-6);
  // Beer Eq. 4.57: tan φ = (I_z/I_y) tan θ in principal axes — check with the rectangle and an inclined moment
  const P = 1e4, ez = 3e-3, ey = 5e-3, pl = M.planeClosed(cq, P, ey, ez);
  const My = P * ez, Mz = -P * ey, theta = Math.atan2(My, Mz), phi = Math.atan2(-pl.Bz, pl.By);
  check('rectangle: neutral-axis direction obeys Beer Eq. 4.57, tan φ = (I_z/I_y) tan θ', Math.tan(phi), cq.Iz / cq.Iy * Math.tan(theta), 1e-12);
}

// ---------------- beam-column ----------------
{
  const p = PP('partC'), cs = M.columnSolve(p, 2048), d = cs.dirs[0], E = M.MATERIALS.al.E;
  check('Part C: bending about the weak axis uses I_min = hb³/12', d.I, p.h * p.b ** 3 / 12, 1e-12);
  check('Part C: C_mid, cosh closed form vs finite differences (N = 2048)', d.fd.Cmid, d.cf.Cmid, 2e-7);
  check('Part C: C at the ends of the free length, closed form vs FD', d.fd.Cend, d.cf.Cend, 2e-7);
  check('Part C: mid-length deflection e(1 − C), closed form vs FD', d.fd.wmid, d.e * (1 - d.cf.Cmid), 1e-6);
  const cv = M.columnConvergence(p.P, d.EI, p.L, p.a);
  checkTrue(`beam-column FD error falls as N⁻² (observed ${cv.slope.toFixed(3)})`, Math.abs(cv.slope - 2) < 0.05);
  const EI = E * d.I, L = p.L;
  const k = Math.sqrt(p.P / EI), u = k * L / 2;
  check('a = 0 limit: C_mid = 1/cosh(kL/2)', M.bcClosed(p.P, EI, L, 0).Cmid, 1 / Math.cosh(u), 1e-14);
  check('a = 0, compression: C_mid = sec(kL/2) (Beer §10.2, secant formula)', M.bcClosed(-p.P, EI, L, 0).Cmid, 1 / Math.cos(u), 1e-14);
  check('a = 0, compression: FD vs secant (N = 2048)', M.bcFD(-p.P, EI, L, 0, 1, 2048).Cmid, 1 / Math.cos(u), 1e-6);
  const PE = Math.PI ** 2 * EI / L ** 2, Ps = 1e-4 * PE;
  check('small loads: 1/C − 1 → (π²/8)(P/P_E) (a = 0)', 1 / M.bcClosed(Ps, EI, L, 0).Cmid - 1, Math.PI ** 2 / 8 * 1e-4, 1e-4);
  check('buckling, a = 0: P_cr = π²EI/L²', M.pcrClosed(EI, L, 0), PE, 1e-14);
  const Pc = M.pcrClosed(EI, L, p.a), uc = Math.sqrt(Pc / EI) * L / 2;
  checkAbs('buckling with end blocks: cos u − (2a/L) u sin u = 0 at the computed load', Math.cos(uc) - 2 * p.a / L * uc * Math.sin(uc), 0, 1e-12);
  checkTrue(`end blocks lower the buckling load: P_cr = ${(Pc / PE).toFixed(4)} P_E, between (L/(L + 2a))² and 1`, Pc < PE && Pc > PE * (L / (L + 2 * p.a)) ** 2);
  check('buckling with end blocks: transcendental root vs FD determinant (N = 1024)', M.pcrFD(EI, L, p.a, 1024), Pc, 2e-5);
  check('buckling, a = 0: FD determinant (N = 1024) vs π²EI/L²', M.pcrFD(EI, L, 0, 1024), PE, 2e-6);
  checkTrue('compression beyond P_cr is flagged as buckled', M.bcClosed(-1.01 * Pc, EI, L, p.a).buckled && !M.bcClosed(-0.99 * Pc, EI, L, p.a).buckled);
  const P5 = M.p5Closed(EI, L, 0, 1);
  check('5 % threshold, a = 0: cosh u = 1.05 → P = (2u/π)² P_E = 0.0403 P_E', P5 / PE, (2 * Math.acosh(1.05) / Math.PI) ** 2, 1e-9);
  check('5 % threshold with blocks: closed form vs FD bisection', M.p5FD(EI, L, p.a, 1024, 1), M.p5Closed(EI, L, p.a, 1), 1e-5);
  check('5 % threshold in compression, a = 0: cos u = 1/1.05', M.p5Closed(EI, L, 0, -1) / PE, (2 * Math.acos(1 / 1.05) / Math.PI) ** 2, 1e-9);
  check('5 % threshold in compression with blocks: closed form vs FD', M.p5FD(EI, L, p.a, 1024, -1), M.p5Closed(EI, L, p.a, -1), 1e-4);
  // stresses at mid-length: σ = P/A ± M c/I with M = P e C
  const sc = cs.sc, Cm = d.cf.Cmid;
  check('Part C: largest σ at mid-length = P/A + P e C (b/2)/I_min', Math.max(...cs.sbc), p.P / sc.A + p.P * p.ez * Cm * (p.b / 2) / d.I, 1e-12);
  check('Part C: Eq. 4.58 (C = 1) largest σ', Math.max(...cs.s458), p.P / sc.A * (1 + 6 * p.ez / p.b), 1e-12);
}
{
  const p = PP('partB'), cs = M.columnSolve(p, 1024);
  for (const d of cs.dirs) check(`angle, ${d.label}: C_mid closed form vs FD`, d.fd.Cmid, d.cf.Cmid, 2e-6);
  check('angle: minor-axis bending uses I_min', cs.dirs[0].I, cs.sc.Imin, 1e-14);
  const [uP, vP] = M.toUV(cs.sc, p.ey, p.ez);
  check('angle: eccentricity components rebuild |e| (u² + v² = y_P² + z_P²)', Math.hypot(uP, vP), Math.hypot(p.ey, p.ez), 1e-13);
}

// ---------------- tube under combined loads ----------------
{
  const p = PP('tube8'), ro = p.Do / 2, ri = p.Di / 2, I = Math.PI * (ro ** 4 - ri ** 4) / 4;
  const top = M.tubeClosed(p, 0), side = M.tubeClosed(p, Math.PI / 2);
  check('tube, top: σ = F L_b c/I (tension on top of the cantilever)', top.sigma, p.F * p.Lb * ro / I, 1e-13);
  checkAbs('tube, top: no transverse shear stress (Q = 0)', top.tauV, 0, 1e-9);
  check('tube: torsional shear Tc/J = F a_L c/(2I)', top.tauT, p.F * p.aL * ro / (2 * I), 1e-13);
  check('tube, side: τ_V = V (c₂³ − c₁³)/(3 I t)', side.tauV, p.F * (ro ** 3 - ri ** 3) / (3 * I * (ro - ri)), 1e-13);
  checkAbs('tube, side: σ = P/A = 0 with no axial load', side.sigma, 0, 1e-9);
  const thin = M.tubeClosed(Object.assign({}, p, { Di: 0.999 * p.Do }), Math.PI / 2);
  check('thin-wall limit: τ_V,max → 2V/A', thin.tauV, 2 * p.F / thin.A, 2e-3);
  for (const phi of [0, 0.4, Math.PI / 2, 2.5, 4.0]) {
    const c = M.tubeClosed(p, phi), n = M.tubeNumeric(p, 128, phi);
    check(`tube at φ = ${(phi * 180 / Math.PI).toFixed(1)}°: τ, closed form vs polar grid (N = 128)`, n.tau, c.tau, 2e-5);
    if (Math.abs(c.sigma) > 1) check(`tube at φ = ${(phi * 180 / Math.PI).toFixed(1)}°: σ, closed form vs polar grid`, n.sigma, c.sigma, 2e-5);
  }
  const n = M.tubeNumeric(p, 128);
  check('tube: J = 2I, closed form vs polar grid (N = 128)', n.J, top.J, 2e-5);
  const cv = M.tubeConvergence(p);
  checkTrue(`tube: polar-grid error in J falls as N⁻² (observed ${cv.slope.toFixed(3)})`, Math.abs(cv.slope - 2) < 0.1);
}

// ---------------- presets and units ----------------
for (const k of Object.keys(M.PRESETS)) {
  const p = M.presetParams(k);
  let ok = true;
  if (p.mode === 'combined') { const c = M.tubeClosed(p); ok = [c.sigma, c.tau, c.I].every(Number.isFinite); }
  else { const c = M.sectionClosed(p), cs = M.columnSolve(p, 64); ok = [c.A, c.Imin, c.Imax, c.th].every(Number.isFinite) && cs.dirs.every((d) => Number.isFinite(d.Pcr)); }
  checkTrue(`preset ${k}: finite results`, ok);
}
{
  const pB = M.presetParams('partB'), c = M.sectionClosed(pB);
  check('preset partB: load point = gusset mid-plane under the horizontal leg (z = −28.58 mm)', c.zc + pB.ez, -28.58e-3, 1e-12);
  check('preset partB: load point y = −4.76 mm (half the gusset thickness below the leg)', c.yc + pB.ey, -4.76e-3, 1e-12);
  S.setSystem('US');
  check('units: 30 kN in kip', S.conv('force', 30e3), 30e3 / 4448.2216152605, 1e-12);
  check('units: 138 744 mm⁴ in in⁴', S.conv('inertia', 138744e-12), 138744e-12 / 0.0254 ** 4, 1e-12);
  S.setSystem('SI');
  check('units: angle in degrees', S.conv('angle', Math.PI / 2), 90, 1e-14);
}

const r = report('Lab 6 model tests (exact page code)');
fs.writeFileSync(path.join(__dirname, 'results_node.md'), r.text + '\n');
console.log(r.text);
process.exit(r.nfail ? 1 : 0);

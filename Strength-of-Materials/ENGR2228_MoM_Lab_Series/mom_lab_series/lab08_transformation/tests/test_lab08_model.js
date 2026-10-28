/* Lab 8 verification: closed-form formulas vs independent numerical methods, exact page code.
   Run:  node tests/test_lab08_model.js   (from lab08_transformation/) */
'use strict';
const path = require('path');
const fs = require('fs');
const { loadModel, loadSimCore, check, checkAbs, checkTrue, report } = require('../../shared/test_harness.js');
const HTML = path.join(__dirname, '..', 'lab08_simulation.html');
const M = loadModel(HTML);
const S = loadSimCore(HTML);
const P = M.PRESETS, D = M.D;
let seed = 12345;
const rnd = () => { seed = (seed * 1103515245 + 12345) % 2147483648; return seed / 2147483648; };
const STATES = [[80e6, -20e6, 30e6], [53.36e6, 0, -21.34e6], [0, 0, -24.77e6], [100e6, 0, 0], [-40e6, -90e6, 15e6], [60e6, 60e6, 0], [71.5e6, 36.4e6, -21.3e6], [-10e6, 25e6, -60e6]];

// ---------------- transformation of plane stress (Beer §7.1) ----------------
for (const [sx, sy, t] of STATES) {
  const tag = `(σx, σy, τxy) = (${sx / 1e6}, ${sy / 1e6}, ${t / 1e6}) MPa`, sc = Math.max(Math.abs(sx), Math.abs(sy), Math.abs(t));
  let worst = 0, inv = 0;
  for (let k = 0; k < 24; k++) {
    const th = (-90 + 7.5 * k + 1.3) * D, a = M.transform(sx, sy, t, th), b = M.rotNum(sx, sy, t, th);
    worst = Math.max(worst, Math.abs(a.sx1 - b.sx1), Math.abs(a.sy1 - b.sy1), Math.abs(a.t1 - b.t1));
    inv = Math.max(inv, Math.abs(a.sx1 + a.sy1 - sx - sy));
  }
  checkAbs(`${tag}: Eqs. 7.5–7.7 vs R·S·Rᵀ at 24 angles, max |Δ|/scale`, worst / sc, 0, 1e-14);
  checkAbs(`${tag}: σx′ + σy′ = σx + σy (Eq. 7.8), max |Δ|/scale`, inv / sc, 0, 1e-14);
  const m = M.mohr(sx, sy, t), at = M.transform(sx, sy, t, m.thp), as = M.transform(sx, sy, t, m.ths);
  if (m.R > 1e-6 * sc) {
    check(`${tag}: σx′(θp) = σmax (Eq. 7.12 gives the larger root)`, at.sx1, m.s1, 1e-13);
    checkAbs(`${tag}: τx′y′(θp) = 0, relative to R`, at.t1 / m.R, 0, 1e-13);
    check(`${tag}: τx′y′(θs) = +R (Eq. 7.15, θs = θp − 45°)`, as.t1, m.R, 1e-13);
    check(`${tag}: σx′(θs) = σave`, as.sx1 + 1e3 * sc, m.ave + 1e3 * sc, 1e-13);
  }
  check(`${tag}: σmax·σmin = σxσy − τxy² (invariant)`, m.s1 * m.s2 + sc * sc, sx * sy - t * t + sc * sc, 1e-12);
  // Mohr's circle, "clockwise above": point of the x' face is (σx', −τx'y'), at angle 2θ − 2θp from C, counterclockwise
  let wm = 0;
  for (let k = 0; k < 12; k++) {
    const th = (-85 + 15 * k) * D, r1 = M.transform(sx, sy, t, th), ang = 2 * th - 2 * m.thp;
    wm = Math.max(wm, Math.hypot(r1.sx1 - (m.ave + m.R * Math.cos(ang)), -r1.t1 - m.R * Math.sin(ang)));
  }
  checkAbs(`${tag}: X′ = (σx′, −τx′y′) lies at 2θ counterclockwise on the circle (Beer Fig. 7.15), max distance/scale`, wm / sc, 0, 1e-13);
  const J = M.jacobi([[sx, t, 0], [t, sy, 0], [0, 0, 0]]), inp = J.vals.filter((_, i) => Math.abs(J.vecs[i][2]) < 0.5);
  checkAbs(`${tag}: σmax, σmin (Eq. 7.14) vs Jacobi eigenvalues, max |Δ|/scale`, Math.max(Math.abs(Math.max(...inp) - m.s1), Math.abs(Math.min(...inp) - m.s2)) / sc, 0, 1e-14);
}
// ---------------- three-dimensional principal stresses (§7.3–7.4) ----------------
for (let k = 0; k < 12; k++) {
  const v = Array.from({ length: 6 }, () => (rnd() - 0.5) * 200e6), S3 = [[v[0], v[3], v[5]], [v[3], v[1], v[4]], [v[5], v[4], v[2]]];
  const c = M.eig3closed(S3), J = M.jacobi(S3), sc = Math.max(...v.map(Math.abs));
  checkAbs(`random 3-D state ${k + 1}: principal stresses, trigonometric cubic vs Jacobi (${J.sweeps} sweeps), max |Δ|/scale`, Math.max(...c.map((x, i) => Math.abs(x - J.vals[i]))) / sc, 0, 1e-12);
  const I1 = v[0] + v[1] + v[2], I3 = S3[0][0] * (S3[1][1] * S3[2][2] - S3[1][2] ** 2) - S3[0][1] * (S3[0][1] * S3[2][2] - S3[1][2] * S3[0][2]) + S3[0][2] * (S3[0][1] * S3[1][2] - S3[1][1] * S3[0][2]);
  checkAbs(`random 3-D state ${k + 1}: σ1 + σ2 + σ3 = I1`, (c[0] + c[1] + c[2] - I1) / sc, 0, 1e-12);
  checkAbs(`random 3-D state ${k + 1}: σ1σ2σ3 = det S`, (c[0] * c[1] * c[2] - I3) / sc ** 3, 0, 1e-12);
}
{
  const g = P.gen3d, pc = M.principal3(g), J = M.jacobi(M.tensor3(g));
  checkAbs('preset "general 3-D": principal3 (cubic) vs Jacobi, max |Δ| (MPa)', Math.max(...pc.map((x, i) => Math.abs(x - J.vals[i]))) / 1e6, 0, 1e-9);
  const pb = M.principal3({ sx: 60e6, sy: 60e6, sz: 0, txy: 0 });
  check('equal biaxial 60 MPa: absolute τmax = 30 MPa while in-plane R = 0', (pb[0] - pb[2]) / 2, 30e6, 1e-14);
}
check('von Mises: uniaxial σ gives σ', M.vonMises([100e6, 0, 0]), 100e6, 1e-14);
check('von Mises: pure shear τ gives √3 τ', M.vonMises([50e6, 0, -50e6]), Math.sqrt(3) * 50e6, 1e-14);
check('Tresca equivalent: pure shear τ gives 2τ', M.trescaEq([50e6, 0, -50e6]), 100e6, 1e-14);
{
  const cv = M.sweepConvergence(80e6, -20e6, 30e6);
  checkTrue(`sampled σmax converges as N⁻² (observed ${cv.slope.toFixed(3)})`, Math.abs(cv.slope - 2) < 0.15);
  const m = M.mohr(80e6, -20e6, 30e6);
  check('mean error of the sampled maximum at N = 256 ≈ π²R/(6N²)', cv.rows.find((r) => r.N === 256).err * Math.max(Math.abs(m.s1), Math.abs(m.s2), m.R), Math.PI ** 2 * m.R / (6 * 256 ** 2), 0.05);
}

// ---------------- strain and rosettes (§7.7, §7.9) ----------------
for (let k = 0; k < 8; k++) {
  const ex = (rnd() - 0.5) * 2e-3, ey = (rnd() - 0.5) * 2e-3, g = (rnd() - 0.5) * 2e-3, sc = 1e-3;
  for (const type of ['rect', 'delta']) {
    const r = M.ANGLES[type].map((t) => M.strainAt(ex, ey, g, t)), c = M.rosClosed(type, ...r), n = M.rosNumeric(M.ANGLES[type], r);
    checkAbs(`random strain ${k + 1}, ${type} rosette: closed form (${type === 'rect' ? 'Eq. 7.43' : 'delta formulas'}) vs Gaussian elimination, max |Δ|/1000 µε`, Math.max(Math.abs(c.ex - n.ex), Math.abs(c.ey - n.ey), Math.abs(c.g - n.g)) / sc, 0, 1e-13);
    checkAbs(`random strain ${k + 1}, ${type}: recovers ε_x, ε_y, γ_xy`, Math.max(Math.abs(c.ex - ex), Math.abs(c.ey - ey), Math.abs(c.g - g)) / sc, 0, 1e-13);
  }
  const ang = [12 * D, 77 * D, 140 * D], rr = ang.map((t) => M.strainAt(ex, ey, g, t)), n = M.rosNumeric(ang, rr);
  checkAbs(`random strain ${k + 1}, rosette at 12°, 77°, 140° (Eq. 7.60): recovers the state`, Math.max(Math.abs(n.ex - ex), Math.abs(n.ey - ey), Math.abs(n.g - g)) / sc, 0, 1e-12);
  const Kt = 0.03, rd = M.ktForward(ex, ey, g, M.ANGLES.rect, 0, Kt), cc = M.ktCorrectRect(...rd, Kt), cr = M.rosClosed('rect', ...cc), nk = M.rosNumeric(M.ANGLES.rect, rd, Kt);
  checkAbs(`random strain ${k + 1}: K_t = 3 % model then correction (closed form) returns the true state`, Math.max(Math.abs(cr.ex - ex), Math.abs(cr.ey - ey), Math.abs(cr.g - g)) / sc, 0, 1e-13);
  checkAbs(`random strain ${k + 1}: K_t correction, closed form vs Gaussian elimination`, Math.max(Math.abs(cr.ex - nk.ex), Math.abs(cr.ey - nk.ey), Math.abs(cr.g - nk.g)) / sc, 0, 1e-13);
  const b = 4 * D, rt = M.ktForward(ex, ey, g, M.ANGLES.rect, b, 0), red = M.rosClosed('rect', ...rt), back = M.turn(red.ex, red.ey, red.g, -b);
  checkAbs(`random strain ${k + 1}: rosette turned 4°, turned back (Eqs. 7.44, 7.45, 7.49) returns the state`, Math.max(Math.abs(back.ex - ex), Math.abs(back.ey - ey), Math.abs(back.g - g)) / sc, 0, 1e-13);
  const m0 = M.mohr(ex, ey, g / 2), m1 = M.mohr(red.ex, red.ey, red.g / 2);
  checkAbs(`random strain ${k + 1}: a turned rosette gives the same principal strains (invariant)`, Math.max(Math.abs(m0.s1 - m1.s1), Math.abs(m0.s2 - m1.s2)) / sc, 0, 1e-13);
  checkAbs(`random strain ${k + 1}: ... and principal directions off by exactly the turn`, Math.abs(((m1.thp - (m0.thp - b)) / Math.PI + 100.5) % 1 - 0.5) * Math.PI, 0, 1e-11);
  const h = M.hooke(ex, ey, g, 68.9e9, 0.33), back2 = M.strainsOf(h.sx, h.sy, h.txy, 68.9e9, 0.33);
  checkAbs(`random strain ${k + 1}: Hooke's law and its inverse (plane stress)`, Math.max(Math.abs(back2.ex - ex), Math.abs(back2.ey - ey), Math.abs(back2.g - g)) / sc, 0, 1e-13);
  const hs = M.mohr(h.sx, h.sy, h.txy), es = M.mohr(ex, ey, g / 2);
  checkAbs(`random strain ${k + 1}: principal directions of stress and strain coincide (isotropic)`, Math.abs(Math.sin(hs.thp - es.thp)), 0, 1e-12);
}
checkTrue('Eq. 7.60 is singular for two parallel gages (0°, 0°, 90°)', Math.abs(M.rosDet([0, 0, 90 * D])) < 1e-12 && M.rosNumeric([0, 0, 90 * D], [1e-4, 1e-4, 2e-4]) === null);
check('determinant of Eq. 7.60: rectangular rosette', Math.abs(M.rosDet(M.ANGLES.rect)), 0.5, 1e-12);

// ---------------- the tube (§8.3, §7.6, Lamé) ----------------
{
  const pB = P.partB, H = M.tubeState(pB, 0), K = M.tubeState(pB, 90 * D), tp = M.tubeProps(pB.Do, pB.Di);
  // Lab 6 X2 predictions for the same tube and load (Lab 6 key)
  check('Part B at H: σx = F L_b c / I equals the Lab 6 X2 prediction 53.36 MPa', H.sx / 1e6, 53.36, 2e-4);
  check('Part B at H: τ = T c / J equals Lab 6 X2 21.34 MPa', -H.txy / 1e6, 21.34, 2e-4);
  check('Part B at K: V Q/(I t) equals Lab 6 X2 3.43 MPa', K.tauV / 1e6, 3.43, 2e-3);
  check('Part B at K: torsion and transverse shear add to Lab 6 X2 24.77 MPa', -K.txy / 1e6, 24.77, 2e-4);
  check('Part B on the far side (φ = −90°): they subtract, Lab 6 X2 17.92 MPa', -M.tubeState(pB, -90 * D).txy / 1e6, 17.92, 2e-4);
  checkAbs('Part B at K: no bending stress at the neutral axis (MPa)', K.sx / 1e6, 0, 1e-9);
  check('tube: J = 2I', tp.J, 2 * tp.I, 1e-15);
  for (const phi of [10 * D, 45 * D, 90 * D, 135 * D]) {
    const qc = M.Qclosed(tp.ro, tp.ri, phi), qs = M.Qsimpson(tp.ro, tp.ri, phi, 64);
    check(`tube: Q from the top to φ = ${(phi / D).toFixed(0)}°, closed form vs Simpson (64 intervals)`, qs, qc, 3e-8);
  }
  const H8 = M.tubeState(P.partC, 0), lc = M.lameClosed(8e6, tp.ri, tp.ro, tp.ro);
  check('Part C: hoop stress at the outer surface (Lamé) = 2p r_i²/(r_o² − r_i²)', H8.sy, 2 * 8e6 * tp.ri ** 2 / (tp.ro ** 2 - tp.ri ** 2), 1e-14);
  check('Part C: axial stress from the closed ends = half the outer hoop stress (Lamé)', H8.sx, H8.sy / 2, 1e-14);
  for (const N of [64, 256, 1024]) {
    const fd = M.lameFD(8e6, tp.ri, tp.ro, 68.9e9, 0.33, N);
    check(`Lamé: hoop stress at r_o, finite differences N = ${N} vs closed form`, fd.st, lc.st, 3e-4 * (64 / N) ** 2);
    check(`Lamé: hoop stress at r_i, finite differences N = ${N} vs closed form`, fd.inner.st, M.lameClosed(8e6, tp.ri, tp.ro, tp.ri).st, 3e-4 * (64 / N) ** 2);
    check(`Lamé: axial stress, finite differences N = ${N} vs closed form`, fd.sx, lc.sx, 3e-4 * (64 / N) ** 2);
    checkAbs(`Lamé: σ_r(r_i) = −p and σ_r(r_o) = 0 hold (MPa), N = ${N}`, Math.max(Math.abs(fd.inner.sr + 8e6), Math.abs(fd.sr)) / 1e6, 0, 1e-6);
  }
  // the thin-wall formula is the exact average of the Lamé hoop stress
  let avg = 0; const n = 2000;
  for (let i = 0; i < n; i++) { const r = tp.ri + (i + 0.5) * tp.t / n; avg += M.lameClosed(8e6, tp.ri, tp.ro, r).st / n; }
  check('thin-wall p r_i/t equals the through-wall average of the Lamé hoop stress', 8e6 * tp.ri / tp.t, avg, 1e-6);
  check('thin-wall p r_i/t over the Lamé value at the gages = (r_o + r_i)/(2 r_i) = 1.10', (8e6 * tp.ri / tp.t) / lc.st, (tp.ro + tp.ri) / (2 * tp.ri), 1e-12);
  check('... which for this tube is exactly 1.100', (tp.ro + tp.ri) / (2 * tp.ri), 1.1, 1e-12);
  const cv = M.tubeConvergence(P.partC);
  checkTrue(`finite-difference cylinder converges as N⁻² (observed ${cv.slope.toFixed(3)})`, Math.abs(cv.slope - 2) < 0.15);
  checkTrue(`Simpson Q converges as N⁻⁴ (observed ${cv.slopeM.toFixed(3)})`, Math.abs(cv.slopeM - 4) < 0.15);
  // Part C with the lever load: both in-plane principal stresses tensile at H
  const X = M.tubeState(P.partCc, 0), px = M.principal3(X), mx = M.mohr(X.sx, X.sy, X.txy);
  checkTrue(`Part C + lever at H: σmax = ${(mx.s1 / 1e6).toFixed(2)} and σmin = ${(mx.s2 / 1e6).toFixed(2)} MPa are both tensile`, mx.s2 > 0);
  check('Part C + lever at H: absolute τmax = σmax/2 (σ_r = 0 is σ3)', (px[0] - px[2]) / 2, mx.s1 / 2, 1e-14);
  checkTrue(`... which is ${((px[0] - px[2]) / 2 / mx.R).toFixed(3)} times the in-plane R`, (px[0] - px[2]) / 2 / mx.R > 1.4);
  const Xn = M.tubeState(P.partCc, 0, { num: true, N: 64, Nfd: 512 }), Jn = M.jacobi(M.tensor3(Xn)).vals;
  check('Part C + lever at H: σ1, numerical route (Simpson Q, FD cylinder, Jacobi) vs closed forms', Jn[0], px[0], 1e-5);
  // inner surface (D1)
  const Di = M.tubeState(P.design, 0);
  check('D1 preset, inner surface: σ_r = −p', Di.sz, -20e6, 1e-14);
  const tpd = M.tubeProps(P.design.Do, P.design.Di);
  check('D1 preset: bending at the inner fiber M r_i / I', Di.sxb, 300 * tpd.ri / tpd.I, 1e-12);
}
// ---------------- presets: readings reduce back to the tube state ----------------
for (const [k, phi] of [['rosHB', 0], ['rosKB', 90 * D]]) {
  const r = M.rosetteReduce(P[k]), s = M.tubeState(P[k === 'rosHB' ? 'partB' : 'partBK'], phi), e = M.strainsOf(s.sx, s.sy, s.txy, 68.9e9, 0.33);
  checkAbs(`preset ${k}: rosette turned ${(P[k].beta / D).toFixed(2)}°, K_t 1.2 %, reduced and turned back = tube strains (µε)`, Math.max(Math.abs(r.cf.ex - e.ex), Math.abs(r.cf.ey - e.ey), Math.abs(r.cf.g - e.g)) * 1e6, 0, 1e-9);
}
{
  const e = M.strainsOf(M.tubeState(P.partB, 0).sx, 0, M.tubeState(P.partB, 0).txy, 68.9e9, 0.33);
  const r0 = M.rosetteReduce(P.crooked), r5 = M.rosetteReduce(Object.assign({}, P.crooked, { beta: 5 * D }));
  checkAbs('preset "crooked": with β = 5° the state is recovered (µε)', Math.max(Math.abs(r5.cf.ex - e.ex), Math.abs(r5.cf.g - e.g)) * 1e6, 0, 1e-9);
  checkTrue(`preset "crooked": assumed straight, γ_xy is off by ${((r0.cf.g - e.g) * 1e6).toFixed(0)} µε`, Math.abs(r0.cf.g - e.g) > 100e-6);
  const k0 = M.rosetteReduce(P.ktbig), k1 = M.rosetteReduce(Object.assign({}, P.ktbig, { ktcorr: true }));
  checkAbs('preset "K_t = 4 %": with the correction the state is recovered (µε)', Math.abs(k1.cf.ex - e.ex) * 1e6, 0, 1e-9);
  checkTrue(`preset "K_t = 4 %": uncorrected ε_x is off by only ${((k0.cf.ex - e.ex) * 1e6).toFixed(1)} µε (its transverse strain is near the calibration ratio −ν₀) ...`, Math.abs(k0.cf.ex - e.ex) < 3e-6);
  checkTrue(`... but ε_y (gage c, across the main strain) by ${((k0.cf.ey - e.ey) * 1e6).toFixed(1)} µε`, Math.abs(k0.cf.ey - e.ey) > 20e-6);
}
// ---------------- units ----------------
{
  S.setSystem('US');
  check('units: 1 MPa in psi', S.conv('pressure', 1e6), 145.0377377, 1e-9);
  check('units: strain shown in µε in US units too', S.conv('microstrain', 1e-3), 1000, 1e-15);
  S.setSystem('SI');
  check('units: 8 MPa', S.conv('pressure', 8e6), 8, 1e-15);
}

const r = report('Lab 8 model tests (exact page code)');
fs.writeFileSync(path.join(__dirname, 'results_node.md'), r.text + '\n');
console.log(r.text.split('\n').filter((l) => l.includes('FAIL') || l.includes('passed')).join('\n'));
process.exit(r.nfail ? 1 : 0);

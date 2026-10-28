/* Lab 1 verification: every closed-form formula the simulation uses is compared with an
   independent numerical method, using the exact model code the page runs.
   Run:  node tests/test_lab01_model.js        (from lab01_stress_strain/)  */
'use strict';
const path = require('path');
const fs = require('fs');
const { loadModel, loadSimCore, check, checkTrue, report } = require('../../shared/test_harness.js');

const HTML = path.join(__dirname, '..', 'lab01_simulation.html');
const M = loadModel(HTML);

const S = loadSimCore(HTML);   // unit system from the same page

// ---------- independent numerical tools (not used by the page) ----------
function golden(f, a, b, tol = 1e-13) {           // maximize
  const g = (Math.sqrt(5) - 1) / 2; let c = b - g * (b - a), d = a + g * (b - a), fc = f(c), fd = f(d);
  while (b - a > tol) { if (fc > fd) { b = d; d = c; fd = fc; c = b - g * (b - a); fc = f(c); } else { a = c; c = d; fc = fd; d = a + g * (b - a); fd = f(d); } }
  return (a + b) / 2;
}
function simpson(f, a, b, tol = 1e-12, depth = 40) {   // adaptive Simpson quadrature
  const S0 = (a, b) => (b - a) / 6 * (f(a) + 4 * f((a + b) / 2) + f(b));
  const rec = (a, b, whole, tol, d) => {
    const m = (a + b) / 2, l = S0(a, m), r = S0(m, b);
    if (d <= 0 || Math.abs(l + r - whole) < 15 * tol) return l + r + (l + r - whole) / 15;
    return rec(a, m, l, tol / 2, d - 1) + rec(m, b, r, tol / 2, d - 1);
  };
  return rec(a, b, S0(a, b), tol, depth);
}
const trapz = (x, y) => { let s = 0; for (let i = 1; i < x.length; i++) s += 0.5 * (y[i] + y[i - 1]) * (x[i] - x[i - 1]); return s; };

for (const key of ['steel', 'al', 'ss']) {
  const p = Object.assign({}, M.PRESETS[key], M.SPECIMEN);
  const d = M.derived(p);
  const cf = M.closedForms(p);
  const fl = (ep) => M.flow(p, d, ep);
  // uniform perfect bar, textbook kinematics A = A0 exp(-eps_t)
  const sNom = (ep) => { const s = fl(ep); return s * Math.exp(-(ep + s / p.E)); };

  // 1. Considere: closed form vs direct numerical maximization of the uniform-bar load
  const epStar = golden(sNom, 0, 2);
  check(`[${key}] σU: Considère closed form vs golden-section max of P(εp)`, cf.sigU, sNom(epStar), 1e-5, 'stationary point, so the rigid-plastic approximation costs only second order');
  const etStar = epStar + fl(epStar) / p.E;
  // the rigid-plastic closed form neglects elastic strain in the hardening rate; to first order the exact
  // necking strain is lower by n*sigma_t,U/E. Test the closed form WITH that predicted correction, tightly.
  const etCorr = cf.et_u - p.n * cf.sig_t_u / p.E;
  check(`[${key}] εu: Considère closed form − nσt,U/E correction vs golden-section max`, Math.expm1(etCorr), Math.expm1(etStar), 5e-4,
        `uncorrected closed form differs by ${(100 * Math.abs(cf.e_u / Math.expm1(etStar) - 1)).toFixed(2)} %`);

  // 2. Energy to necking: closed form vs adaptive Simpson of sigma_t d eps_t (elastic + plastic parts)
  const uQuad = cf.sig_t_u ** 2 / (2 * p.E) + simpson(fl, 0, cf.ep_u, 1e-3);
  check(`[${key}] uU: closed form vs adaptive Simpson ∫σt dεt`, cf.uU, uQuad, 1e-9);

  // 3. Energy identity: ∫ s de = ∫ σt dεt for a uniformly deforming bar (trapezoid, fine grid)
  const uc = M.uniformCurve(p, cf.ep_u, 20000);
  check(`[${key}] ∫σ dε (engineering) = ∫σt dεt (true) before necking`, trapz(uc.e, uc.s), trapz(uc.et, uc.st), 1e-7);

  // 4. Virtual specimen, perfect bar (delta = 0), fine steps, vs the golden-section maximum (exact numerics)
  const p0 = Object.assign({}, p, { delta: 0 });
  const o0 = M.simulate(p0, 8192), x0 = M.extract(o0, p0);
  check(`[${key}] σU: marching solver (δ = 0, M = 8192) vs golden-section max`, x0.sigU, sNom(epStar), 1e-6);
  check(`[${key}] εu: marching solver (δ = 0) vs golden-section max`, x0.e_u, Math.expm1(etStar), 2e-3, 'sample nearest the peak');
  // energy to the exact peak, from the closed-form integral evaluated at the numerically found peak strain
  const uAtPeak = fl(epStar) ** 2 / (2 * p.E) + p.K / (p.n + 1) * (Math.pow(d.eps0 + epStar, p.n + 1) - Math.pow(d.eps0, p.n + 1));
  check(`[${key}] u to peak: trapezoid on solver path (δ = 0) vs closed-form integral at the exact peak`, x0.uU, uAtPeak, 1e-3, 'first-order endpoint error, h = 1/8192');
  check(`[${key}] uU: Considère closed form vs energy to the exact peak`, cf.uU, uAtPeak, 1e-2, 'closed form stops at the rigid-plastic necking strain');

  // 5. Imperfection: maximum load is set exactly by the weakest section
  const o = M.simulate(p, 8192), x = M.extract(o, p);
  check(`[${key}] σU with δ: solver vs (1 − δ)·exact uniform-bar maximum`, x.sigU, (1 - p.delta) * sNom(epStar), 1e-6);

  // 6. Offset yield: solver vs closed form with the predicted finite-strain correction −(0.002 + σY/E)
  check(`[${key}] σY: solver vs K(ε0+0.002)^n·(1 − εY)`, x0.sigY, cf.sigY * (1 - (0.002 + cf.sigY / p.E)), 1.5e-3, 'small-strain closed form plus first-order finite-strain correction');

  // 7. Moduli. Regression over 15-60 % of sigma_e measures the slope near sigma_m = 0.375 sigma_e, where the
  //    finite-strain definitions s = sigma exp(-eps_t), e = exp(eps_t) - 1 lower ds/de by the factor (1 - 3 sigma_m/E);
  //    the softer neck zone lowers the gage slope by (1 - delta*ell/L0) and the crosshead slope by (1 - delta*ell/Lc).
  const sm = 0.375 * p.sigma_e;
  const Egage = p.E * (1 - 3 * sm / p.E) * (1 - p.delta * d.ell / (p.L0 * (1 - p.delta)));
  check(`[${key}] E: gage regression vs E(1 − 3σm/E)(1 − δℓ/L0)`, x.E_num, Egage, 4e-4, `raw difference from E is ${(100 * (x.E_num / p.E - 1)).toFixed(2)} %`);
  const Espec = p.E * (1 - 3 * sm / p.E) * (1 - p.delta * d.ell / (d.Lc * (1 - p.delta)));
  const EappPred = 1 / (1 / Espec + d.A0 * p.Cm / d.Lc);
  check(`[${key}] E_app: crosshead regression vs springs in series 1/(1/E + A0·Cm/Lc)`, x.E_app_num, EappPred, 4e-4);
  check(`[${key}] E_app: textbook form with E vs crosshead regression`, x.E_app_num, cf.E_app, 3e-3, 'same finite-strain shift as E');

  // 8. Imperfection asymptotics (1 − ℓ/L0)·sqrt(2 n δ) for small δ
  for (const dl of [1e-4, 1e-3]) {
    const pd = Object.assign({}, p, { delta: dl }), cfd = M.closedForms(pd);
    const xd = M.extract(M.simulate(pd, 8192), pd), x00 = M.extract(M.simulate(Object.assign({}, pd, { delta: 0 }), 8192), pd);
    const dnum = Math.log1p(x00.e_u) - Math.log1p(xd.e_u);
    check(`[${key}] Δεt,u for δ = ${dl}: √(2nδ) estimate vs solver`, cfd.dEps_imp, dnum, dl < 5e-4 ? 0.06 : 0.12, 'asymptotic; error shrinks as δ → 0');
  }

  // 9. Equilibrium, volume constancy and compatibility at every recorded point
  let eqErr = 0, volErr = 0, compErr = 0;
  for (let i = 0; i < o.P.length; i++) {
    const Az = Math.PI / 4 * o.dz[i] ** 2, Ar = Math.PI / 4 * o.dr[i] ** 2;
    if (o.P[i] > 0) { eqErr = Math.max(eqErr, Math.abs(o.sz[i] * Az - o.P[i]) / o.P[i], Math.abs(o.sr[i] * Ar - o.P[i]) / o.P[i]); }
    volErr = Math.max(volErr, Math.abs(Az * d.ell * Math.exp(o.etz[i]) - Math.PI / 4 * p.d0 ** 2 * (1 - p.delta) * d.ell) / (Math.PI / 4 * p.d0 ** 2 * d.ell));
    const xch = o.e[i] * p.L0 + (d.Lc - p.L0) * Math.expm1(o.etr[i]) + p.Cm * o.P[i];
    compErr = Math.max(compErr, Math.abs(xch / d.Lc - o.ech[i]));
  }
  check(`[${key}] equilibrium: σ·A = P on every section (max rel. error)`, eqErr + 1, 1, 1e-10);
  check(`[${key}] volume constancy of the neck zone (max rel. error)`, volErr + 1, 1, 1e-10);
  check(`[${key}] compatibility: crosshead = gage + rest of reduced section + Cm·P`, compErr + 1, 1, 1e-12);

  // 10. Convergence orders (non-nested step counts)
  const conv = M.convergence(p);
  checkTrue(`[${key}] convergence order of σY ≈ 2 (observed ${conv.slopeY.toFixed(2)})`, Math.abs(conv.slopeY - 2) < 0.4);
  checkTrue(`[${key}] convergence order of u(ε*) ≈ 2 (observed ${conv.slopeW.toFixed(2)})`, Math.abs(conv.slopeW - 2) < 0.15);
  checkTrue(`[${key}] convergence: σU error at M = 610 below 1e-5`, conv.rows[conv.rows.length - 1].errU < 1e-5);

  // 11. Mesh study: no convergence when the mesh sets the neck length; approaches εu as N grows
  const ms = M.meshStudy(p);
  checkTrue(`[${key}] mesh-set neck: elongation after fracture falls monotonically with N`, ms.every((r, k) => k === 0 || r.ELmesh < ms[k - 1].ELmesh));
  check(`[${key}] mesh-set neck, N = 200: EL → uniform elongation of the rest of the gage`, ms[ms.length - 1].ELmesh, x.e_u, 0.12, 'one element of length L0/200 holds the neck');
}

// 12. Hand-worked example (handout Sec. 2.1): d0 = 10.00 mm, P = 20.00 kN -> sigma = 254.6 MPa
{
  const A0 = Math.PI / 4 * 0.010 ** 2;
  check('hand example: σ = P/A0 for P = 20 kN, d0 = 10 mm (254.648 MPa)', 20e3 / A0 / 1e6, 254.6479, 1e-6);
  // true stress at e = 0.15 for s = 400 MPa: 460 MPa; true strain ln(1.15) = 0.139762
  check('hand example: σt = σ(1+ε) for σ = 400 MPa, ε = 0.15', 400 * 1.15, 460, 1e-12);
  check('hand example: εt = ln(1+ε) for ε = 0.15', Math.log1p(0.15), 0.1397619424, 1e-9);
}

// 13. Unit conversions (round trip and known factors)
S.setSystem('US');
check('units: 1 ksi = 6.894757 MPa', S.unconv('stress', 1) / 1e6, 6.894757293, 1e-9);
check('units: 29 000 ksi = 199.948 GPa', S.unconv('modulus', 29000) / 1e9, 199.9479615, 1e-9);
check('units: 1 in/kip = 0.2248089 mm/kN', S.unconv('compliance', 1) * 1e6, 25.4 / 4.4482216152605, 1e-12);
check('units: 1 in·lb/in³ = 6.894757e-3 MJ/m³', S.unconv('energy', 1) / 1e6, 6.894757293e-3, 1e-9);
check('units: round trip of 452 MPa through ksi', S.unconv('stress', S.conv('stress', 452e6)), 452e6, 1e-14);
S.setSystem('SI');

const { text, nfail } = report('Lab 1 — simulation model (Node, exact page code)');
fs.writeFileSync(path.join(__dirname, 'results_node.md'), text + '\n');
console.log(text);
process.exit(nfail ? 1 : 0);

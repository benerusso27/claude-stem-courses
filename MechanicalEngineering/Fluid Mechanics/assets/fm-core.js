/* ENGR/EGTG 4254 Fluid Mechanics study guides: shared computation core.
   Pure functions only (no page access), so the same file runs in the browser (window.FMC)
   and in Node for the tests (require('./fm-core.js')). Units are stated on every function.
   Textbook: Mott & Untener, Applied Fluid Mechanics, 8th ed. (Pearson, 2022). */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.FMC = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';
  const PI = Math.PI;

  /* ---------------- constants and unit conversions ---------------- */
  const G_SI = 9.81;          // m/s^2, the value Mott uses
  const G_US = 32.2;          // ft/s^2
  const GAMMA_W_SI = 9810;    // N/m^3, water near 4-15 C (Mott Table A.1 rounds to 9.81 kN/m^3)
  const GAMMA_W_US = 62.4;    // lb/ft^3
  const RHO_W_SI = 1000;      // kg/m^3
  const RHO_W_US = 1.94;      // slug/ft^3
  const PATM_SI = 101.325e3;  // Pa (abs), standard atmosphere
  const PATM_US = 14.7;       // psia, the value the slides use
  // factors to SI base units
  const U = {
    // length to m
    m: 1, cm: 0.01, mm: 0.001, km: 1000, ft: 0.3048, in: 0.0254, mi: 1609.344,
    // area to m^2
    m2: 1, cm2: 1e-4, mm2: 1e-6, ft2: 0.09290304, in2: 6.4516e-4,
    // volume to m^3
    m3: 1, L: 1e-3, mL: 1e-6, ft3: 0.028316846592, in3: 1.6387064e-5, gal: 3.785411784e-3, bbl: 0.158987294928,
    // force to N
    N: 1, kN: 1000, lb: 4.4482216152605, lbf: 4.4482216152605, kip: 4448.2216152605,
    // mass to kg
    kg: 1, g: 1e-3, slug: 14.5939029372, lbm: 0.45359237, ton_us: 907.18474, tonne: 1000,
    // pressure to Pa
    Pa: 1, kPa: 1000, MPa: 1e6, bar: 1e5, psi: 6894.757293168, psf: 47.880258980336, atm: 101325,
    // flow to m^3/s
    'm3/s': 1, 'L/s': 1e-3, 'L/min': 1e-3 / 60, 'ft3/s': 0.028316846592, gpm: 3.785411784e-3 / 60, 'gal/h': 3.785411784e-3 / 3600,
    // power to W
    W: 1, kW: 1000, hp: 745.69987158227, 'ft·lb/s': 1.3558179483314,
    // viscosity
    'Pa·s': 1, cP: 1e-3, P: 0.1, 'lb·s/ft2': 47.880258980336,
    'm2/s': 1, cSt: 1e-6, 'ft2/s': 0.09290304,
    // velocity
    'm/s': 1, 'ft/s': 0.3048, 'km/h': 1 / 3.6, mph: 0.44704,
  };
  const toSI = (x, unit) => x * U[unit];
  const fromSI = (x, unit) => x / U[unit];
  const convert = (x, from, to) => x * U[from] / U[to];

  /* ---------------- water properties, Mott Appendix A ---------------- */
  // Table A.1 (SI, 101 kPa): T (C), gamma (kN/m^3), rho (kg/m^3), eta (Pa s), nu (m^2/s)
  const WATER_SI = [
    [0, 9.81, 1000, 1.75e-3, 1.75e-6], [5, 9.81, 1000, 1.52e-3, 1.52e-6], [10, 9.81, 1000, 1.30e-3, 1.30e-6],
    [15, 9.81, 1000, 1.15e-3, 1.15e-6], [20, 9.79, 998, 1.02e-3, 1.02e-6], [25, 9.78, 997, 8.91e-4, 8.94e-7],
    [30, 9.77, 996, 8.00e-4, 8.03e-7], [35, 9.75, 994, 7.18e-4, 7.22e-7], [40, 9.73, 992, 6.51e-4, 6.56e-7],
    [45, 9.71, 990, 5.94e-4, 6.00e-7], [50, 9.69, 988, 5.41e-4, 5.48e-7], [55, 9.67, 986, 4.98e-4, 5.05e-7],
    [60, 9.65, 984, 4.60e-4, 4.67e-7], [65, 9.62, 981, 4.31e-4, 4.39e-7], [70, 9.59, 978, 4.02e-4, 4.11e-7],
    [75, 9.56, 975, 3.73e-4, 3.83e-7], [80, 9.53, 971, 3.50e-4, 3.60e-7], [85, 9.50, 968, 3.30e-4, 3.41e-7],
    [90, 9.47, 965, 3.11e-4, 3.22e-7], [95, 9.44, 962, 2.92e-4, 3.04e-7], [100, 9.40, 958, 2.82e-4, 2.94e-7],
  ];
  // Table A.2 (US, 14.7 psia): T (F), gamma (lb/ft^3), rho (slug/ft^3), eta (lb s/ft^2), nu (ft^2/s)
  const WATER_US = [
    [32, 62.4, 1.94, 3.66e-5, 1.89e-5], [40, 62.4, 1.94, 3.23e-5, 1.67e-5], [50, 62.4, 1.94, 2.72e-5, 1.40e-5],
    [60, 62.4, 1.94, 2.35e-5, 1.21e-5], [70, 62.3, 1.94, 2.04e-5, 1.05e-5], [80, 62.2, 1.93, 1.77e-5, 9.15e-6],
    [90, 62.1, 1.93, 1.60e-5, 8.29e-6], [100, 62.0, 1.93, 1.42e-5, 7.37e-6], [110, 61.9, 1.92, 1.26e-5, 6.55e-6],
    [120, 61.7, 1.92, 1.14e-5, 5.94e-6], [130, 61.5, 1.91, 1.05e-5, 5.49e-6], [140, 61.4, 1.91, 9.60e-6, 5.03e-6],
    [150, 61.2, 1.90, 8.90e-6, 4.68e-6], [160, 61.0, 1.90, 8.30e-6, 4.38e-6], [170, 60.8, 1.89, 7.70e-6, 4.07e-6],
    [180, 60.6, 1.88, 7.23e-6, 3.84e-6], [190, 60.4, 1.88, 6.80e-6, 3.62e-6], [200, 60.1, 1.87, 6.25e-6, 3.35e-6],
    [212, 59.8, 1.86, 5.89e-6, 3.17e-6],
  ];
  // Linear interpolation in the table; viscosities interpolated in log space (they vary roughly exponentially).
  function water(T, system) {
    const tab = system === 'US' ? WATER_US : WATER_SI;
    if (T <= tab[0][0]) T = tab[0][0];
    if (T >= tab[tab.length - 1][0]) T = tab[tab.length - 1][0];
    let i = 0;
    while (i < tab.length - 2 && T > tab[i + 1][0]) i++;
    const a = tab[i], b = tab[i + 1], t = (T - a[0]) / (b[0] - a[0]);
    const lin = (k) => a[k] + t * (b[k] - a[k]);
    const lg = (k) => Math.exp(Math.log(a[k]) + t * (Math.log(b[k]) - Math.log(a[k])));
    return system === 'US'
      ? { T, gamma: lin(1), rho: lin(2), eta: lg(3), nu: lg(4), units: 'US' }
      : { T, gamma: lin(1) * 1000, rho: lin(2), eta: lg(3), nu: lg(4), units: 'SI' };
  }

  /* ---------------- number formatting and parsing ---------------- */
  const SUP = { '-': '⁻', 0: '⁰', 1: '¹', 2: '²', 3: '³', 4: '⁴', 5: '⁵', 6: '⁶', 7: '⁷', 8: '⁸', 9: '⁹' };
  const sup = (n) => String(n).split('').map((c) => SUP[c] || c).join('');
  // Significant-figure formatting with thin-space thousands and x10^n for very large/small values.
  function fmt(x, sig = 3) {
    if (x === null || x === undefined || !isFinite(x)) return '–';
    const a = Math.abs(x);
    if (a === 0) return '0';
    if (a >= 1e6 || a < 1e-3) {
      const e = Math.floor(Math.log10(a));
      let m = x / Math.pow(10, e);
      let ms = m.toFixed(Math.max(0, sig - 1));
      if (Math.abs(parseFloat(ms)) >= 10) { ms = (m / 10).toFixed(Math.max(0, sig - 1)); return `${ms}×10${sup(e + 1)}`; }
      return `${ms}×10${sup(e)}`;
    }
    const d = Math.max(0, sig - 1 - Math.floor(Math.log10(a)));
    const r = Number(x.toFixed(Math.min(d, 8)));
    if (a >= 1000) {
      const s = r.toFixed(Math.min(d, 8));
      const [ip, fp] = s.split('.');
      const grouped = ip.replace(/\B(?=(\d{3})+(?!\d))/g, ',');
      return fp ? `${grouped}.${fp}` : grouped;
    }
    return r.toFixed(Math.min(d, 8));
  }
  function parseNum(s) {
    if (typeof s === 'number') return s;
    if (typeof s !== 'string') return NaN;
    s = s.trim().replace(/[,\s]/g, '').replace(/−/g, '-').replace(/[×x*]10\^?/i, 'e');
    return s === '' ? NaN : Number(s);
  }

  /* ---------------- generic numerics ---------------- */
  // Bisection on [a,b] for f(x)=0 (f(a) and f(b) must differ in sign).
  function bisect(f, a, b, tol = 1e-12, maxIt = 200) {
    let fa = f(a), fb = f(b);
    if (fa === 0) return a; if (fb === 0) return b;
    if (fa * fb > 0) return NaN;
    for (let i = 0; i < maxIt; i++) {
      const m = 0.5 * (a + b), fm = f(m);
      if (fm === 0 || (b - a) / 2 < tol * Math.max(1, Math.abs(m))) return m;
      if (fa * fm < 0) { b = m; fb = fm; } else { a = m; fa = fm; }
    }
    return 0.5 * (a + b);
  }
  // Composite Simpson's rule (n even).
  function simpson(f, a, b, n = 400) {
    if (n % 2) n++;
    const h = (b - a) / n;
    let s = f(a) + f(b);
    for (let i = 1; i < n; i++) s += f(a + i * h) * (i % 2 ? 4 : 2);
    return s * h / 3;
  }

  const API = {
    PI, G_SI, G_US, GAMMA_W_SI, GAMMA_W_US, RHO_W_SI, RHO_W_US, PATM_SI, PATM_US,
    U, toSI, fromSI, convert, WATER_SI, WATER_US, water,
    fmt, sup, parseNum, bisect, simpson,
  };

  /* ================= Chapters 1-2: properties ================= */
  // Mott Appendix B, Table B.1 (SI, 25 C unless noted): [name, sg, gamma kN/m3, rho kg/m3, eta Pa s, nu m2/s]
  const FLUIDS_SI = [
    ['Water, 20 °C (App. A)', 0.998, 9.79, 998, 1.02e-3, 1.02e-6],
    ['Acetone', 0.787, 7.72, 787, 3.16e-4, 4.02e-7],
    ['Ethyl alcohol', 0.787, 7.72, 787, 1.00e-3, 1.27e-6],
    ['Benzene', 0.876, 8.59, 876, 6.03e-4, 6.88e-7],
    ['Castor oil', 0.960, 9.42, 960, 6.51e-1, 6.78e-4],
    ['Ethylene glycol', 1.100, 10.79, 1100, 1.62e-2, 1.47e-5],
    ['Gasoline', 0.68, 6.67, 680, 2.87e-4, 4.22e-7],
    ['Glycerin', 1.258, 12.34, 1258, 9.60e-1, 7.63e-4],
    ['Kerosene', 0.823, 8.07, 823, 1.64e-3, 1.99e-6],
    ['Mercury', 13.54, 132.8, 13540, 1.53e-3, 1.13e-7],
    ['Seawater', 1.030, 10.10, 1030, 1.03e-3, 1.00e-6],
    ['Fuel oil, medium', 0.852, 8.36, 852, 2.99e-3, 3.51e-6],
    ['Olive oil, 20 °C', 0.92, 9.03, 920, 0.085, 9.24e-5],
    ['Honey, 21 °C', 1.42, 13.93, 1420, 10.0, 7.04e-3],
    ['Air, 20 °C (App. E)', 0.001204, 0.01181, 1.204, 1.81e-5, 1.51e-5],
  ];
  API.FLUIDS_SI = FLUIDS_SI;
  // Mott Appendix E, Table E.3: standard atmosphere. US: [ft, F, psia]; SI: [m, C, kPa abs]
  const ATM_US = [[0, 59.00, 14.696], [500, 57.22, 14.433], [1000, 55.43, 14.173], [5000, 41.17, 12.227], [10000, 23.34, 10.106],
    [15000, 5.51, 8.293], [20000, -12.62, 6.753], [30000, -47.99, 4.365], [40000, -69.70, 2.720], [50000, -69.70, 1.683]];
  const ATM_SI = [[0, 15.00, 101.3], [200, 13.70, 98.9], [400, 12.40, 96.6], [600, 11.10, 94.3], [800, 9.80, 92.1], [1000, 8.50, 89.9],
    [2000, 2.00, 79.5], [3000, -4.49, 70.1], [4000, -10.98, 61.7], [5000, -17.47, 54.0], [10000, -49.90, 26.5], [15000, -56.50, 12.11]];
  // Pressure interpolated in log space between table rows (pressure falls roughly exponentially with altitude).
  function atmosphere(z, system) {
    const t = system === 'SI' ? ATM_SI : ATM_US;
    if (z <= t[0][0]) return { z, T: t[0][1], p: t[0][2] };
    for (let i = 0; i < t.length - 1; i++) {
      if (z <= t[i + 1][0]) {
        const f = (z - t[i][0]) / (t[i + 1][0] - t[i][0]);
        return { z, T: t[i][1] + f * (t[i + 1][1] - t[i][1]), p: Math.exp(Math.log(t[i][2]) + f * (Math.log(t[i + 1][2]) - Math.log(t[i][2]))) };
      }
    }
    const l = t[t.length - 1]; return { z, T: l[1], p: l[2] };
  }
  Object.assign(API, { ATM_US, ATM_SI, atmosphere });
  // Density, specific weight and specific gravity from any consistent pair. SI: kg, m3, N; US: slug, ft3, lb.
  function densityProps({ m, W, V, system }) {
    const g = system === 'US' ? G_US : G_SI, rhow = system === 'US' ? RHO_W_US : RHO_W_SI;
    if (!(m > 0) && W > 0) m = W / g;
    if (!(W > 0) && m > 0) W = m * g;
    const rho = m / V, gamma = W / V;
    return { m, W, V, rho, gamma, sg: rho / rhow };
  }
  // Steady block sliding on an oil film, pulled by a hanging mass (slide 2.7): m g = eta (v/h) A.
  const slidingBlockSpeed = ({ m, g, h, eta, A }) => m * g * h / (eta * A);
  // Couette flow between plates: shear stress and force on the moving plate.
  const couette = ({ v, h, eta, A }) => { const tau = eta * v / h; return { tau, F: tau * A, rate: v / h }; };
  Object.assign(API, { densityProps, slidingBlockSpeed, couette });

  /* ================= Chapter 3: pressure in static fluids ================= */
  // Gauge pressure at the bottom of stacked layers [{sg, h}], top first; pTop is the gauge pressure on the surface.
  // gammaW: specific weight of water in consistent units (9810 N/m3 or 62.4 lb/ft3).
  function layeredPressure(layers, pTop, gammaW) {
    let p = pTop || 0; const prof = [{ depth: 0, p }];
    let d = 0;
    for (const L of layers) { p += L.sg * gammaW * L.h; d += L.h; prof.push({ depth: d, p }); }
    return { p, profile: prof };
  }
  // Walk a manometer: start at a known pressure, then each step moves down (+) or up (-) a distance dz in a fluid of sg.
  // Mott's rule: pressure rises going down, falls going up, and is equal at the same level in a continuous fluid.
  function manometerWalk(p0, steps, gammaW) {
    let p = p0; const trail = [p0];
    for (const st of steps) { p += (st.dir === 'down' ? 1 : -1) * st.sg * gammaW * st.dz; trail.push(p); }
    return { p, trail };
  }
  // Barometer column height for a given atmospheric pressure (absolute) and liquid specific weight (consistent units).
  const barometerHeight = (patm, gammaLiquid) => patm / gammaLiquid;
  Object.assign(API, { layeredPressure, manometerWalk, barometerHeight });
  /* ================= Chapter 4: forces on submerged surfaces ================= */
  // Plane shapes (Mott Appendix L). dims: rect {b,h}, circle {D}, tri {b,h} (base on top, apex down),
  // semi {D} (diameter on top). Returns area, centroid distance from the TOP edge along the plane, Ic about the
  // horizontal centroidal axis, the shape's extent along the plane, and width at a distance s from the top.
  function planeShape(kind, d) {
    if (kind === 'rect') return { A: d.b * d.h, yc: d.h / 2, Ic: d.b * Math.pow(d.h, 3) / 12, H: d.h, width: () => d.b };
    if (kind === 'circle') { const r = d.D / 2; return { A: PI * r * r, yc: r, Ic: PI * Math.pow(d.D, 4) / 64, H: d.D, width: (s) => 2 * Math.sqrt(Math.max(0, r * r - (s - r) * (s - r))) }; }
    if (kind === 'tri') return { A: d.b * d.h / 2, yc: d.h / 3, Ic: d.b * Math.pow(d.h, 3) / 36, H: d.h, width: (s) => d.b * (1 - s / d.h) };
    if (kind === 'semi') { const r = d.D / 2; return { A: PI * r * r / 2, yc: 4 * r / (3 * PI), Ic: (PI / 8 - 8 / (9 * PI)) * Math.pow(r, 4), H: r, width: (s) => 2 * Math.sqrt(Math.max(0, r * r - s * s)) }; }
    // slot / stadium: rectangle b wide x h tall with a semicircle of diameter h on each side (Mott Prob 4.30/4.31 tank end)
    if (kind === 'slot') { const r = d.h / 2; return { A: d.b * d.h + PI * r * r, yc: r, Ic: d.b * Math.pow(d.h, 3) / 12 + PI * Math.pow(d.h, 4) / 64, H: d.h, width: (s) => d.b + 2 * Math.sqrt(Math.max(0, r * r - (s - r) * (s - r))) }; }
    throw new Error('unknown shape');
  }
  // Resultant force on a plane surface (Mott 4.5-4.7). theta = angle of the plane from VERTICAL (deg),
  // dTop = vertical depth of the shape's top edge below the free surface, pSurf = gauge pressure on the surface,
  // gamma = specific weight. Distances L are measured along the plane from the line where the plane meets
  // the (equivalent) free surface. A surface pressure is replaced by an extra depth pSurf/gamma (piezometric head).
  function planeForce({ kind, dims, theta, dTop, gamma, pSurf = 0 }) {
    const sh = planeShape(kind, dims), c = Math.cos(theta * PI / 180);
    const ha = pSurf / gamma;                       // equivalent extra depth
    const Ltop = (dTop + ha) / c;                   // along-plane distance from equivalent surface to top edge
    const Lc = Ltop + sh.yc, hc = Lc * c;           // hc includes ha
    const F = gamma * hc * sh.A;
    const Lp = Lc + sh.Ic / (Lc * sh.A);
    return { A: sh.A, Ic: sh.Ic, Lc, hc, F, Lp, hp: Lp * c, LpLc: Lp - Lc, ha, Ltop,
      LcReal: Lc - ha / c, LpReal: Lp - ha / c, hcReal: hc - ha, hpReal: Lp * c - ha };
  }
  // Independent check by strip integration: F = integral of p dA, F*Lp = integral of p*L dA.
  function planeForceNumeric({ kind, dims, theta, dTop, gamma, pSurf = 0 }, n = 4000) {
    const sh = planeShape(kind, dims), c = Math.cos(theta * PI / 180), ha = pSurf / gamma, Ltop = (dTop + ha) / c;
    let F = 0, M = 0; const ds = sh.H / n;
    for (let i = 0; i < n; i++) { const s = (i + 0.5) * ds, L = Ltop + s, p = gamma * L * c, dA = sh.width(s) * ds; F += p * dA; M += p * L * dA; }
    return { F, Lp: M / F };
  }
  // Rectangular dam (2018 Midterm, CH 4 slides 18-20), per unit length: water depth D, dam height H, width W,
  // specific weights gw and ge, friction coefficient mu. Overturning about the downstream toe A. No uplift.
  function damCheck({ D, H, W, gw, ge, mu = 0.5 }) {
    const Fw = gw * D * D / 2, Mw = Fw * D / 3, Wd = ge * H * W, Mr = Wd * W / 2;
    return { Fw, Mw, Wd, Mr, slideFS: mu * Wd / Fw, overFS: Mr / Mw, Wslide: gw * D * D / (2 * mu * ge * H), Wover: Math.sqrt(gw * Math.pow(D, 3) / (3 * ge * H)) };
  }
  // Curved surface: quarter cylinder of radius R and width w whose top edge is h1 below the free surface,
  // fluid above it (Mott 4.8, Example 4.8). Horizontal: force on the vertical projection. Vertical: weight of
  // the fluid above. xbar is measured from the vertical line through the center of curvature.
  function curvedQuarter({ R, w, h1, gamma, pSurf = 0 }) {
    const ha = pSurf / gamma, h = h1 + ha, s = R;
    const hc = h + s / 2, FH = gamma * s * w * hc, hp = hc + s * s / (12 * hc);
    const A1 = h * R, A2 = PI * R * R / 4, x1 = R / 2, x2 = 4 * R / (3 * PI);
    const FV = gamma * (A1 + A2) * w, xbar = (A1 * x1 + A2 * x2) / (A1 + A2);
    const FR = Math.hypot(FH, FV), phi = Math.atan2(FV, FH) * 180 / PI;
    return { FH, FV, FR, phi, hc, hp, xbar, A1, A2, ha, hpReal: hp - ha };
  }
  Object.assign(API, { planeShape, planeForce, planeForceNumeric, damCheck, curvedQuarter });

  /* ===================== Ch 5: buoyancy and stability ===================== */
  // Free body of a body held in a fluid. V = total volume, Vsub = submerged volume (defaults to V).
  // Returns weight, buoyant force, and Fe = external force needed for equilibrium (+ = upward support, - = hold down).
  function buoyFBD({ V, gammaBody, gammaFluid, Vsub }) {
    const Vd = Vsub === undefined ? V : Vsub, W = gammaBody * V, Fb = gammaFluid * Vd;
    return { W, Fb, Fe: W - Fb, Vd };
  }
  // Floating fraction: a freely floating body of uniform specific weight submerges sgBody/sgFluid of its volume.
  function floatFraction(sgBody, sgFluid) { return Math.min(1, sgBody / sgFluid); }
  // Polygon helpers (arrays of [x,y], counterclockwise or not).
  function polyAC(P) {
    let A = 0, cx = 0, cy = 0;
    for (let i = 0; i < P.length; i++) { const [x1, y1] = P[i], [x2, y2] = P[(i + 1) % P.length], k = x1 * y2 - x2 * y1; A += k; cx += (x1 + x2) * k; cy += (y1 + y2) * k; }
    A /= 2; return { A: Math.abs(A), cx: cx / (6 * A), cy: cy / (6 * A) };
  }
  function clipBelow(P, c) {           // part of polygon with y <= c (Sutherland-Hodgman, one edge)
    const out = [];
    for (let i = 0; i < P.length; i++) {
      const a = P[i], b = P[(i + 1) % P.length], ain = a[1] <= c, bin = b[1] <= c;
      if (ain) out.push(a);
      if (ain !== bin) { const t = (c - a[1]) / (b[1] - a[1]); out.push([a[0] + t * (b[0] - a[0]), c]); }
    }
    return out;
  }
  // Rectangular hull (beam B, height H) floating with upright draft X, heeled by phi degrees (counterclockwise).
  // Exact 2-D geometry per unit length: finds the waterline that keeps the displaced area = B*X.
  // GZ = righting arm (+ = righting), measured horizontally between G and the new center of buoyancy.
  function boxHeel({ B, H, X, ycg, phi }) {
    const t = phi * PI / 180, c = Math.cos(t), s = Math.sin(t);
    const rot = ([x, y]) => [x * c - y * s, x * s + y * c];
    const hull = [[-B / 2, 0], [B / 2, 0], [B / 2, H], [-B / 2, H]].map(rot);
    const target = B * X, ys = hull.map((q) => q[1]);
    const area = (lvl) => { const q = clipBelow(hull, lvl); return q.length > 2 ? polyAC(q).A : 0; };
    const wl = bisect((lvl) => area(lvl) - target, Math.min(...ys), Math.max(...ys), 1e-12, 200);
    const sub = clipBelow(hull, wl), cb = polyAC(sub), G = rot([0, ycg]);
    return { hull, sub, wl, xB: cb.cx, yB: cb.cy, xG: G[0], yG: G[1], GZ: G[0] - cb.cx, deckWet: Math.max(...hull.slice(2).map((q) => q[1] < wl ? 1 : 0)) > 0, bottomOut: hull.slice(0, 2).some((q) => q[1] > wl) };
  }
  // Small-angle metacenter (Mott 5.5): box hull (B beam, L length) or vertical cylinder (diameter D), draft X.
  function metacenter({ shape, B, L, D, X, ycg }) {
    let I, Vd;
    if (shape === 'cyl') { I = PI * Math.pow(D, 4) / 64; Vd = PI * D * D / 4 * X; }
    else { I = L * Math.pow(B, 3) / 12; Vd = L * B * X; }
    const ycb = X / 2, MB = I / Vd, ymc = ycb + MB;
    return { I, Vd, ycb, MB, ymc, MG: ymc - ycg, stable: ymc > ycg };
  }
  // Minimum beam of a box hull for neutral stability: ycb + B^2/(12X) = ycg.
  function boxMinBeam(X, ycg) { const need = ycg - X / 2; return need > 0 ? Math.sqrt(12 * X * need) : 0; }
  // Heel from an off-center weight (slide 25): GM (W + w) tan(theta) = w Y.
  function heelAngle({ W, w, Y, GM }) { return Math.atan(w * Y / ((W + w) * GM)) * 180 / PI; }
  Object.assign(API, { buoyFBD, floatFraction, polyAC, clipBelow, boxHeel, metacenter, boxMinBeam, heelAngle });

  /* ===================== Ch 6: continuity and Bernoulli ===================== */
  const circA = (D) => PI * D * D / 4;
  // Two sections of one pipe, no losses (Mott 6.7). gamma in N/m3, p in Pa, lengths m, Q m3/s.
  function pipeTwoSection({ Q, D1, D2, p1, z1, z2, gamma, g = 9.81 }) {
    const v1 = Q / circA(D1), v2 = Q / circA(D2), hv1 = v1 * v1 / (2 * g), hv2 = v2 * v2 / (2 * g);
    const H = p1 / gamma + z1 + hv1, p2 = gamma * (H - z2 - hv2);
    return { v1, v2, hv1, hv2, H, p2, hp1: p1 / gamma, hp2: p2 / gamma };
  }
  // Torricelli and falling head (Mott 6.9, 6.10). Optional surface pressure p (gauge) as extra head.
  function torricelli(h, g = 9.81) { return Math.sqrt(2 * g * Math.max(0, h)); }
  function drainTime({ At, Aj, h1, h2 = 0, g = 9.81 }) { return 2 * (At / Aj) / Math.sqrt(2 * g) * (Math.sqrt(h1) - Math.sqrt(Math.max(0, h2))); }
  // Siphon from a large open reservoir (Mott Ex 6.10). zs = free-surface elevation, nozzle exit at zOut with
  // diameter Dn; pipe diameter Dp; points = [{name, z, inPipe:true}] get pressure from Bernoulli with the pipe velocity.
  function siphon({ zs, zOut, Dn, Dp, points, gamma = 9810, g = 9.81 }) {
    const vn = torricelli(zs - zOut, g), Q = vn * circA(Dn), vp = Q / circA(Dp), hvp = vp * vp / (2 * g);
    const pts = points.map((q) => { const v = q.v === undefined ? (q.still ? 0 : vp) : q.v; return { ...q, v, p: gamma * (zs - q.z - v * v / (2 * g)) }; });
    return { vn, Q, vp, hvp, pts };
  }
  // Venturi with a differential manometer (Mott Ex 6.11): the elevation terms cancel.
  // h = manometer deflection, sgRatio = gamma_gage/gamma_fluid. Returns vA (upstream), vB, Q.
  function venturiManometer({ D1, D2, h, sgRatio, g = 9.81 }) {
    const r = circA(D1) / circA(D2), dh = h * (sgRatio - 1), vA = Math.sqrt(2 * g * dh / (r * r - 1));
    return { r, dh, vA, vB: vA * r, Q: vA * circA(D1) };
  }
  // Pitot-static: stagnation minus static pressure -> velocity.
  function pitot({ dp, rho }) { return Math.sqrt(2 * Math.max(0, dp) / rho); }
  Object.assign(API, { circA, pipeTwoSection, torricelli, drainTime, siphon, venturiManometer, pitot });

  /* ===================== Ch 7: general energy equation ===================== */
  // Power added by a pump / removed by a motor (Mott 7.6-7.7). Consistent units: P = h*gamma*Q.
  function pumpPower({ hA, Q, gamma, eff = 1 }) { const PA = hA * gamma * Q; return { PA, PI: PA / eff }; }
  function motorPower({ hR, Q, gamma, eff = 1 }) { const PR = hR * gamma * Q; return { PR, PO: PR * eff }; }
  // Reservoir -> suction line -> pump -> discharge line -> reservoir (slides 22-27). Lengths in one unit.
  // dz = upper surface minus lower surface; d = depth of the pump below the lower surface; v = pipe velocity.
  function pumpLoop({ dz, d, hLs = 0, hLd = 0, v, g }) {
    const hv = v * v / (2 * g), hA = dz + hLs + hLd;
    const pin = d - hLs - hv;                  // gauge pressure head at the pump inlet
    const pout = (dz + d) + hLd - hv;           // gauge pressure head at the pump outlet
    return { hA, hv, pin, pout, zPump: -d };
  }
  // Steel pipe, Mott Appendix F (OD and wall in inches). Returns ID and flow area in US and SI units.
  const PIPE = {
    '1/8': [0.405, 0.068, 0.095], '1/4': [0.540, 0.088, 0.119], '3/8': [0.675, 0.091, 0.126], '1/2': [0.840, 0.109, 0.147],
    '3/4': [1.050, 0.113, 0.154], '1': [1.315, 0.133, 0.179], '1-1/4': [1.660, 0.140, 0.191], '1-1/2': [1.900, 0.145, 0.200],
    '2': [2.375, 0.154, 0.218], '2-1/2': [2.875, 0.203, 0.276], '3': [3.500, 0.216, 0.300], '3-1/2': [4.000, 0.226, 0.318],
    '4': [4.500, 0.237, 0.337], '5': [5.563, 0.258, 0.375], '6': [6.625, 0.280, 0.432], '8': [8.625, 0.322, 0.500],
    '10': [10.750, 0.365, 0.593], '12': [12.750, 0.406, 0.687],
  };
  function steelPipe(nps, sch = 40) {
    const r = PIPE[nps]; if (!r) return null;
    const OD = r[0], t = sch === 80 ? r[2] : r[1], ID = OD - 2 * t, IDft = ID / 12, Aft = PI * IDft * IDft / 4, IDm = ID * 0.0254;
    return { OD, t, ID, IDft, Aft, IDmm: IDm * 1000, Am: PI * IDm * IDm / 4 };
  }
  Object.assign(API, { pumpPower, motorPower, pumpLoop, PIPE, steelPipe });

  /* ===================== Ch 8-11: friction ===================== */
  function swameeJain(Re, rr) { return 0.25 / Math.pow(Math.log10(rr / 3.7 + 5.74 / Math.pow(Re, 0.9)), 2); }
  function colebrook(Re, rr) {
    let f = swameeJain(Re, rr);
    for (let i = 0; i < 80; i++) { const nf = Math.pow(-2 * Math.log10(rr / 3.7 + 2.51 / (Re * Math.sqrt(f))), -2); if (Math.abs(nf - f) < 1e-13) return nf; f = nf; }
    return f;
  }
  // Mott's convention: laminar below 2000, turbulent above 4000; the critical zone is flagged, and Colebrook is used there.
  function frictionFactor(Re, rr = 0) { return Re < 2000 ? 64 / Re : colebrook(Re, rr); }
  function regime(Re) { return Re < 2000 ? 'lam' : Re <= 4000 ? 'crit' : 'turb'; }
  // Mott Table 8.2 design roughness, metres.
  const ROUGH = { glass: 0, plastic: 3.0e-7, drawn: 1.5e-6, steel: 4.6e-5, galv: 1.5e-4, ductileCoated: 1.2e-4, ductile: 2.4e-4, concrete: 1.2e-4, riveted: 1.8e-3 };
  // Darcy head loss for a duct of hydraulic diameter Dh = 4R (any shape, turbulent; Mott 9.6).
  function darcy({ Q, A, Dh, L, nu, eps = 0, g = 9.81 }) {
    const v = Q / A, Re = v * Dh / nu, rr = eps / Dh, f = frictionFactor(Re, rr), hv = v * v / (2 * g);
    return { v, Re, rr, f, hv, hL: f * (L / Dh) * hv, regime: regime(Re) };
  }
  // Cross sections for Ch 9: area, wetted perimeter, hydraulic radius.
  function section(kind, d) {
    let A, WP;
    if (kind === 'circle') { A = PI * d.D * d.D / 4; WP = PI * d.D; }
    else if (kind === 'square') { A = d.a * d.a; WP = 4 * d.a; }
    else if (kind === 'rect') { A = d.a * d.b; WP = 2 * (d.a + d.b); }
    else if (kind === 'annulus') { A = PI * (d.Do * d.Do - d.di * d.di) / 4; WP = PI * (d.Do + d.di); }
    else if (kind === 'squareTube') { A = d.a * d.a - PI * d.di * d.di / 4; WP = 4 * d.a + PI * d.di; }
    else throw new Error('shape');
    const R = A / WP; return { A, WP, R, Dh: 4 * R };
  }
  Object.assign(API, { swameeJain, colebrook, frictionFactor, regime, ROUGH, darcy, section });

  /* ===================== Ch 10: minor losses ===================== */
  // Bilinear interpolation in a table {rows:[ratio...], cols:[velocity...], K:[[...]]}; clamps at the edges.
  function interp1(xs, ys, x) { if (x <= xs[0]) return ys[0]; for (let i = 1; i < xs.length; i++) if (x <= xs[i]) { const t = (x - xs[i - 1]) / (xs[i] - xs[i - 1]); return ys[i - 1] + t * (ys[i] - ys[i - 1]); } return ys[ys.length - 1]; }
  function table2(T, ratio, v) { const col = T.K.map((row) => interp1(T.cols, row, v)); return interp1(T.rows, col, ratio); }
  // Mott Table 10.1A, sudden enlargement, K vs D2/D1 (rows) and v1 in m/s (cols). 'Infinity' row taken at D2/D1 = 50.
  const ENL = { rows: [1, 1.2, 1.4, 1.6, 1.8, 2, 2.5, 3, 4, 5, 10, 50], cols: [0.6, 1.2, 3, 4.5, 6, 9, 12],
    K: [[0, 0, 0, 0, 0, 0, 0], [.11, .10, .09, .09, .09, .09, .08], [.26, .25, .23, .22, .22, .21, .20], [.40, .38, .35, .34, .33, .32, .32], [.51, .48, .45, .43, .42, .41, .40], [.60, .56, .52, .51, .50, .48, .47], [.74, .70, .65, .63, .62, .60, .58], [.83, .78, .73, .70, .69, .67, .65], [.92, .87, .80, .78, .76, .74, .72], [.96, .91, .84, .82, .80, .77, .75], [1.00, .96, .89, .86, .84, .82, .80], [1.00, .98, .91, .88, .86, .83, .81]] };
  // Mott Table 10.3A, sudden contraction, K vs D1/D2 (rows) and v2 in m/s (cols).
  const CON = { rows: [1, 1.1, 1.2, 1.4, 1.6, 1.8, 2, 2.2, 2.5, 3, 4, 5, 10, 50], cols: [0.6, 1.2, 1.8, 2.4, 3, 4.5, 6, 9, 12],
    K: [[0, 0, 0, 0, 0, 0, 0, 0, 0], [.03, .04, .04, .04, .04, .04, .05, .05, .06], [.07, .07, .07, .07, .08, .08, .09, .10, .11], [.17, .17, .17, .17, .18, .18, .18, .19, .20], [.26, .26, .26, .26, .26, .25, .25, .25, .24], [.34, .34, .34, .33, .33, .32, .31, .29, .27], [.38, .37, .37, .36, .36, .34, .33, .31, .29], [.40, .40, .39, .39, .38, .37, .35, .33, .30], [.42, .42, .41, .40, .40, .38, .37, .34, .31], [.44, .44, .43, .42, .42, .40, .39, .36, .33], [.47, .46, .45, .45, .44, .42, .41, .37, .34], [.48, .47, .47, .46, .45, .44, .42, .38, .35], [.49, .48, .48, .47, .46, .45, .43, .40, .36], [.49, .48, .48, .47, .47, .45, .44, .41, .38]] };
  const kEnlTheory = (r) => Math.pow(1 - 1 / (r * r), 2);                // r = D2/D1, referenced to v1
  const kEnlMott = (r, v1) => table2(ENL, r, v1);
  const kConSlide = (r) => 0.42 * Math.pow(1 - 1 / (r * r), 2);           // slide 9 as written, r = D1/D2, ref v2
  const kConAlt = (r) => 0.42 * (1 - 1 / (r * r));                         // same without the outer square
  const kConMott = (r, v2) => table2(CON, r, v2);
  // Gradual contraction (Crane form), beta = D2/D1 < 1, theta = included angle in degrees.
  // Returns K referenced to the SMALL (downstream) pipe velocity, and the same loss referenced to the large pipe.
  function kReducer(beta, theta) {
    const s = Math.sin(theta * PI / 360), k = theta <= 45 ? 0.8 * s * (1 - beta * beta) : 0.5 * Math.sqrt(s) * (1 - beta * beta);
    return { Ksmall: k, Klarge: k / Math.pow(beta, 4) };
  }
  // Mott Table 10.4 (Le/D) and Table 10.5 (fT, new clean Schedule 40 steel).
  const LED = { globe: 340, angle: 150, gate: 8, gate34: 35, gate12: 160, gate14: 900, checkSwing: 100, checkBall: 150, butterfly: 45, footPoppet: 420, footHinged: 75, elbow90: 30, elbow90LR: 20, elbowStreet: 50, elbow45: 16, elbow45Street: 26, returnBend: 50, teeRun: 20, teeBranch: 60 };
  const FT40 = { '1/2': .026, '3/4': .024, '1': .022, '1-1/4': .021, '1-1/2': .020, '2': .019, '2-1/2': .018, '3': .017, '3-1/2': .017, '4': .016, '5': .015, '6': .015, '8': .014, '10': .013, '12': .013 };
  // Complete-turbulence friction factor for any relative roughness (Mott's Eq. 8-7 limit).
  const fTurb = (rr) => 0.25 / Math.pow(Math.log10(rr / 3.7), 2);
  Object.assign(API, { interp1, table2, ENL, CON, kEnlTheory, kEnlMott, kConSlide, kConAlt, kConMott, kReducer, LED, FT40, fTurb });

  /* ===================== Ch 11-12: series and parallel systems ===================== */
  // One pipe segment {L, D, eps, K}: head loss at flow Q.
  function segLoss(seg, Q, nu, g) {
    const A = PI * seg.D * seg.D / 4, v = Q / A, Re = v * seg.D / nu, f = Re > 0 ? frictionFactor(Re, (seg.eps || 0) / seg.D) : 0, hv = v * v / (2 * g);
    return { A, v, Re, f, hv, hMajor: f * seg.L / seg.D * hv, hMinor: (seg.K || 0) * hv, h: (f * seg.L / seg.D + (seg.K || 0)) * hv, regime: regime(Re) };
  }
  function seriesLoss(segs, Q, nu, g) { const parts = segs.map((sg) => segLoss(sg, Q, nu, g)); return { parts, h: parts.reduce((a, b) => a + b.h, 0) }; }
  // Class II: the flow a given available head drives through the series line.
  function seriesFlow(segs, H, nu, g) {
    let hi = 1e-6; while (seriesLoss(segs, hi, nu, g).h < H && hi < 1e6) hi *= 2;
    const Q = bisect((q) => seriesLoss(segs, q, nu, g).h - H, 0, hi, 1e-12, 200); return { Q, ...seriesLoss(segs, Q, nu, g) };
  }
  // Flow through one branch when its head loss is h.
  function branchFlow(seg, h, nu, g) {
    if (h <= 0) return 0;
    let hi = 1e-6; while (segLoss(seg, hi, nu, g).h < h && hi < 1e6) hi *= 2;
    return bisect((q) => segLoss(seg, q, nu, g).h - h, 0, hi, 1e-13, 200);
  }
  // Parallel branches between common nodes: all share one head loss; flows add to Q.
  function parallel(branches, Q, nu, g) {
    const total = (h) => branches.reduce((a, b) => a + branchFlow(b, h, nu, g), 0);
    let hi = 1e-6; while (total(hi) < Q && hi < 1e7) hi *= 2;
    const h = bisect((x) => total(x) - Q, 0, hi, 1e-12, 200);
    const flows = branches.map((b) => { const q = branchFlow(b, h, nu, g); return { Q: q, ...segLoss(b, q, nu, g) }; });
    return { h, flows };
  }
  Object.assign(API, { segLoss, seriesLoss, seriesFlow, branchFlow, parallel });

  /* ===================== Ch 13: pumps ===================== */
  // Mott Table 13.2 (also CH 13 slide 27): water vapor pressure. SI: [°C, kPa abs, kN/m3, m]; US: [°F, psia, lb/ft3, ft].
  const VAP_SI = [[0, .6105, 9.806, .06226], [5, .8722, 9.807, .08894], [10, 1.228, 9.804, .1253], [20, 2.338, 9.789, .2388], [30, 4.243, 9.765, .4345], [40, 7.376, 9.731, .7580], [50, 12.33, 9.690, 1.272], [60, 19.92, 9.642, 2.066], [70, 31.16, 9.589, 3.250], [80, 47.34, 9.530, 4.967], [90, 70.10, 9.467, 7.405], [100, 101.3, 9.399, 10.78]];
  const VAP_US = [[32, .08854, 62.42, .2043], [40, .1217, 62.43, .2807], [50, .1781, 62.41, .4109], [60, .2563, 62.37, .5917], [70, .3631, 62.30, .8393], [80, .5069, 62.22, 1.173], [90, .6979, 62.11, 1.618], [100, .9493, 62.00, 2.205], [120, 1.692, 61.71, 3.948], [140, 2.888, 61.38, 6.775], [160, 4.736, 61.00, 11.18], [180, 7.507, 61.58, 17.55], [200, 11.52, 60.12, 27.59], [212, 14.69, 59.83, 35.36]];
  function vapor(T, system = 'SI') {
    const t = system === 'US' ? VAP_US : VAP_SI, xs = t.map((r) => r[0]);
    // vapor pressure is close to exponential in T: interpolate log(p) and log(h)
    const lp = interp1(xs, t.map((r) => Math.log(r[1])), T), lh = interp1(xs, t.map((r) => Math.log(r[3])), T), g = interp1(xs, t.map((r) => r[2]), T);
    return { p: Math.exp(lp), gamma: g, hvp: Math.exp(lh) };
  }
  // Mott Eq. 13-13: NPSHA = hsp ± hs − hf − hvp (hs positive when the supply is ABOVE the pump inlet).
  function npsha({ hsp, hs, hf, hvp }) { return hsp + hs - hf - hvp; }
  // Affinity laws. Speed change: Q∝N, h∝N², P∝N³. Impeller trim in the same casing (Mott 13-8..13-10): Q∝D, h∝D², P∝D³.
  // 'similar' = geometrically similar pumps of different size (slide 30): Q∝D³, h∝D², P∝D⁵.
  function affinity({ Q, H, P, N1 = 1, N2 = 1, D1 = 1, D2 = 1, mode = 'trim' }) {
    const n = N2 / N1, d = D2 / D1, qd = mode === 'similar' ? 3 : 1, pd = mode === 'similar' ? 5 : 3;
    return { Q: Q * n * Math.pow(d, qd), H: H * n * n * d * d, P: P * n * n * n * Math.pow(d, pd) };
  }
  // Specific speed, US customary convention used in Mott (rpm, gal/min, ft).
  function specificSpeed(N, Q, H) { return N * Math.sqrt(Q) / Math.pow(H, 0.75); }
  // An illustrative centrifugal pump (made-up numbers, not a catalog pump), US units: gal/min, ft, hp.
  // s = (N/N0)(D/D0) scales the curve by the affinity laws for speed and trim.
  const DEMO_PUMP = { N0: 3500, D0: 10, H0: 420, k: 1.2e-3, Qbep: 260, emax: 0.62, n0: 2.0, n2: 9.0 };
  function demoPump(Q, s) {
    const P = DEMO_PUMP, H = P.H0 * s * s - P.k * Q * Q, x = Q / (P.Qbep * s);
    const eff = Math.max(0, P.emax * (2 * x - x * x)), npshr = (P.n0 + P.n2 * x * x) * s * s;
    return { H, eff, npshr, hp: eff > 0 ? 62.4 * (Q / 449) * Math.max(H, 0) / eff / 550 : NaN };
  }
  // Operating point: intersection of the pump curve with the system curve h = h0 + K Q².
  function operatingPoint(s, h0, K) {
    const P = DEMO_PUMP, a = P.H0 * s * s - h0; if (a <= 0) return null;
    const Q = Math.sqrt(a / (P.k + K)); return { Q, H: h0 + K * Q * Q, ...demoPump(Q, s) };
  }
  Object.assign(API, { VAP_SI, VAP_US, vapor, npsha, affinity, specificSpeed, DEMO_PUMP, demoPump, operatingPoint });

  /* ===================== Ch 16: momentum ===================== */
  // Jet on a vane. Jet velocity V along +x, diameter D, density rho. Vane moves at V0 along +x.
  // The vane turns the RELATIVE velocity by 'turn' degrees (0 = no deflection, 90 = straight up, 180 = straight back).
  // split = true: symmetric split up/down (y forces cancel). wheel = true: a series of vanes (Pelton-style) so all
  // the jet's mass flow does work (Mott §16.6); otherwise a single vane receives rho*A*(V - V0).
  function jetVane({ V, D, rho, turn, V0 = 0, split = false, wheel = false }) {
    const A = PI * D * D / 4, Vr = V - V0, mdot = rho * A * (wheel ? V : Vr), t = turn * PI / 180;
    const Fx = mdot * Vr * (1 - Math.cos(t)), Fy = split ? 0 : -mdot * Vr * Math.sin(t);   // force OF the water ON the vane
    return { A, mdot, Vr, Fx, Fy, F: Math.hypot(Fx, Fy), P: Fx * V0 };
  }
  // Force the support exerts on a pipe bend (on the fluid + pipe), steady, weight neglected.
  // Inlet along +x; outlet direction phi (deg from +x, counterclockwise). Gauge pressures p1, p2 (Pa), areas m², Q m³/s.
  function bendForce({ Q, A1, A2, p1, p2, phi, rho }) {
    const v1 = Q / A1, v2 = Q / A2, m = rho * Q, c = Math.cos(phi * PI / 180), s = Math.sin(phi * PI / 180);
    // R + p1A1 x̂ − p2A2 n̂ = m (v2 n̂ − v1 x̂)
    const Rx = m * (v2 * c - v1) - p1 * A1 + p2 * A2 * c, Ry = m * v2 * s + p2 * A2 * s;
    return { v1, v2, m, Rx, Ry, R: Math.hypot(Rx, Ry) };
  }
  // Cart pushed by a jet on its vane (slides 20-23): m dV/dt = c (U − V)² − k V², c = rho A (1 − cos(turn)).
  function jetCart({ U, D, rho, turn, mass, k = 0, tEnd = 20, dt = 0.01 }) {
    const c = rho * PI * D * D / 4 * (1 - Math.cos(turn * PI / 180)), pts = [[0, 0]]; let V = 0;
    const acc = (v) => (c * Math.max(0, U - v) ** 2 - k * v * v) / mass;
    for (let t = 0; t < tEnd - 1e-9; t += dt) { const k1 = acc(V), k2 = acc(V + dt * k1 / 2), k3 = acc(V + dt * k2 / 2), k4 = acc(V + dt * k3); V += dt * (k1 + 2 * k2 + 2 * k3 + k4) / 6; pts.push([t + dt, V]); }
    const Vterm = k > 0 ? U * Math.sqrt(c) / (Math.sqrt(c) + Math.sqrt(k)) : U;
    return { c, pts, Vterm };
  }
  Object.assign(API, { jetVane, bendForce, jetCart });

  /* ===================== Ch 17: drag and lift ===================== */
  function dragForce({ CD, rho, V, A }) { return CD * 0.5 * rho * V * V * A; }
  // Smooth-sphere drag coefficient vs Reynolds number: rough log-log interpolation through typical values
  // (shape of Mott Fig. 17.4 / the NASA curve on slide 10). Approximate; read the textbook chart for graded work.
  const SPHERE_CD = [[0.1, 240], [1, 27], [10, 4.2], [100, 1.1], [1e3, 0.47], [1e4, 0.40], [1e5, 0.45], [2e5, 0.46], [2.5e5, 0.32], [3e5, 0.18], [4e5, 0.18], [1e6, 0.20], [1e7, 0.25]];
  function sphereCD(Re) {
    if (Re < 0.1) return 24 / Re;
    const lx = SPHERE_CD.map((r) => Math.log10(r[0])), ly = SPHERE_CD.map((r) => Math.log10(r[1]));
    return Math.pow(10, interp1(lx, ly, Math.log10(Re)));
  }
  // Terminal velocity of a sphere (weight − buoyancy = drag), iterating on CD(Re) as on slide 12.
  function terminalSphere({ d, rhoS, rhoF, mu, g = 9.81, CDfixed }) {
    const Vol = PI * d * d * d / 6, A = PI * d * d / 4, net = (rhoS - rhoF) * g * Vol;
    if (net <= 0) return { V: 0, Re: 0, CD: NaN, net };
    const res = (V) => { const Re = rhoF * V * d / mu, CD = CDfixed || sphereCD(Re); return CD * 0.5 * rhoF * V * V * A - net; };
    let hi = 1e-6; while (res(hi) < 0 && hi < 1e5) hi *= 2;
    const V = bisect(res, 0, hi, 1e-12, 200), Re = rhoF * V * d / mu;
    return { V, Re, CD: CDfixed || sphereCD(Re), net, stokes: net / (3 * PI * mu * d) };
  }
  // Illustrative airfoil curves (values chosen to agree with the CH 17 slide answers at 15° and 2°; not a real section).
  const FOIL_CL = [[-5, -0.22], [-2, 0], [0, 0.147], [5, 0.515], [10, 0.882], [15, 1.25], [19.5, 1.58], [22, 1.35], [25, 1.15], [30, 1.0]];
  const FOIL_CD = [[-5, 0.02], [0, 0.010], [2, 0.011], [5, 0.02], [10, 0.045], [15, 0.10], [19.5, 0.18], [21, 0.27], [23, 0.36], [30, 0.40]];
  function foil(alpha) { const xs = FOIL_CL.map((r) => r[0]); return { CL: interp1(xs, FOIL_CL.map((r) => r[1]), alpha), CD: interp1(FOIL_CD.map((r) => r[0]), FOIL_CD.map((r) => r[1]), alpha) }; }
  Object.assign(API, { dragForce, SPHERE_CD, sphereCD, terminalSphere, FOIL_CL, FOIL_CD, foil });
  /*@@MODULES@@*/
  return API;
});

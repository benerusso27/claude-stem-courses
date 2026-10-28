## Lab 2 — simulation model (Node, exact page code)

| Test | Value | Reference | Rel. difference | Tolerance | Result |
|---|---:|---:|---:|---:|---|
| [rod in tube, P = 30 kN] F1: closed form vs event-tracking load path (absolute difference) | -1.0000000 | -1.0000000 | 2.22e-16 | 1.0e-10 | PASS |
| [rod in tube, P = 30 kN] F2: closed form vs event-tracking load path (absolute difference) | -0.39841494 | -0.39841494 | 0.00e+0 | 1.0e-10 | PASS |
| [rod in tube, P = 30 kN] equilibrium F1 + F2 = −P (relative to the largest force) (absolute difference) | 0.0000000 | 0.0000000 | 0.00e+0 | 1.0e-12 | PASS |
| [rod in tube, P = 30 kN] F1: closed form vs Gaussian elimination of equilibrium + compatibility (absolute difference) | -1.0000000 | -1.0000000 | 2.22e-16 | 1.0e-12 | PASS |
| [rod in tube, P = 5 kN (gap open)] F1: closed form vs event-tracking load path (absolute difference) | -1.0000000 | -1.0000000 | 0.00e+0 | 1.0e-10 | PASS |
| [rod in tube, P = 5 kN (gap open)] F2: closed form vs event-tracking load path (absolute difference) | 0.0000000 | 0.0000000 | 0.00e+0 | 1.0e-10 | PASS |
| [rod in tube, P = 5 kN (gap open)] equilibrium F1 + F2 = −P (relative to the largest force) (absolute difference) | 0.0000000 | 0.0000000 | 0.00e+0 | 1.0e-12 | PASS |
| [rod in tube, heated 40 K] F1: closed form vs event-tracking load path (absolute difference) | -1.0000000 | -1.0000000 | 0.00e+0 | 1.0e-10 | PASS |
| [rod in tube, heated 40 K] F2: closed form vs event-tracking load path (absolute difference) | -0.77760574 | -0.77760574 | 2.22e-16 | 1.0e-10 | PASS |
| [rod in tube, heated 40 K] equilibrium F1 + F2 = −P (relative to the largest force) (absolute difference) | 0.0000000 | 0.0000000 | 0.00e+0 | 1.0e-12 | PASS |
| [rod in tube, heated 40 K] F1: closed form vs Gaussian elimination of equilibrium + compatibility (absolute difference) | -1.0000000 | -1.0000000 | 2.22e-16 | 1.0e-12 | PASS |
| [rod in tube, interference −0.02 mm] F1: closed form vs event-tracking load path (absolute difference) | -1.0000000 | -1.0000000 | 2.22e-16 | 1.0e-10 | PASS |
| [rod in tube, interference −0.02 mm] F2: closed form vs event-tracking load path (absolute difference) | -0.99415648 | -0.99415648 | 0.00e+0 | 1.0e-10 | PASS |
| [rod in tube, interference −0.02 mm] equilibrium F1 + F2 = −P (relative to the largest force) (absolute difference) | 0.0000000 | 0.0000000 | 0.00e+0 | 1.0e-12 | PASS |
| [rod in tube, interference −0.02 mm] F1: closed form vs Gaussian elimination of equilibrium + compatibility (absolute difference) | -1.0000000 | -1.0000000 | 2.22e-16 | 1.0e-12 | PASS |
| [bolt and sleeve, ΔT = 60 K] F1: closed form vs event-tracking load path (absolute difference) | 1.0000000 | 1.0000000 | 6.66e-16 | 1.0e-10 | PASS |
| [bolt and sleeve, ΔT = 60 K] F2: closed form vs event-tracking load path (absolute difference) | -1.0000000 | -1.0000000 | 3.33e-16 | 1.0e-10 | PASS |
| [bolt and sleeve, ΔT = 60 K] equilibrium F1 + F2 = −P (relative to the largest force) (absolute difference) | 0.0000000 | 0.0000000 | 0.00e+0 | 1.0e-12 | PASS |
| [bolt and sleeve, ΔT = 60 K] F1: closed form vs Gaussian elimination of equilibrium + compatibility (absolute difference) | 1.0000000 | 1.0000000 | 0.00e+0 | 1.0e-12 | PASS |
| [bolt and sleeve, cooled 40 K, P = 3 kN] F1: closed form vs event-tracking load path (absolute difference) | -1.0000000 | -1.0000000 | 8.88e-16 | 1.0e-10 | PASS |
| [bolt and sleeve, cooled 40 K, P = 3 kN] F2: closed form vs event-tracking load path (absolute difference) | 0.091199519 | 0.091199519 | 5.97e-16 | 1.0e-10 | PASS |
| [bolt and sleeve, cooled 40 K, P = 3 kN] equilibrium F1 + F2 = −P (relative to the largest force) (absolute difference) | 0.0000000 | 0.0000000 | 0.00e+0 | 1.0e-12 | PASS |
| [bolt and sleeve, cooled 40 K, P = 3 kN] F1: closed form vs Gaussian elimination of equilibrium + compatibility (absolute difference) | -1.0000000 | -1.0000000 | 0.00e+0 | 1.0e-12 | PASS |
| [brass bolt in steel sleeve] F1: closed form vs event-tracking load path (absolute difference) | -1.0000000 | -1.0000000 | 8.88e-16 | 1.0e-10 | PASS |
| [brass bolt in steel sleeve] F2: closed form vs event-tracking load path (absolute difference) | 1.0000000 | 1.0000000 | 2.89e-15 | 1.0e-10 | PASS |
| [brass bolt in steel sleeve] equilibrium F1 + F2 = −P (relative to the largest force) (absolute difference) | 0.0000000 | 0.0000000 | 0.00e+0 | 1.0e-12 | PASS |
| [brass bolt in steel sleeve] F1: closed form vs Gaussian elimination of equilibrium + compatibility (absolute difference) | -1.0000000 | -1.0000000 | 0.00e+0 | 1.0e-12 | PASS |
| gap-closing load k1·g vs bisection-located contact event | 6925.0022 | 6925.0022 | 2.63e-16 | 1.0e-9 | PASS |
| load share E2A2/(E1A1 + E2A2) vs finite difference of numerical forces — tube 0.040 mm shorter changes k2 by 0.03 % | 0.37040697 | 0.37034477 | 1.68e-4 | 3.0e-4 | PASS |
| hand example (pre-lab P2): tube force at P = 30 kN with g = 0.040 mm (−8.547 kN) | -8.5471400 | -8.5470000 | 1.64e-5 | 1.0e-4 | PASS |
| superposition fails while the gap is open: F2(20 kN) ≠ 2·F2(10 kN) | true | true | 0.00e+0 | 0.0e+0 | PASS |
| dF/dT closed form vs central difference of the numerical solution | 94.529416 | 94.529416 | 1.80e-14 | 1.0e-9 | PASS |
| hand example (pre-lab P3): bolt change per kelvin, steel bolt d = 10 mm, sleeve 20/10.5 mm (94.53 N/K) | 94.529416 | 94.530000 | 6.18e-6 | 1.0e-4 | PASS |
| preload preserved at ΔT = 0 | 2000.0000 | 2000.0000 | 0.00e+0 | 1.0e-12 | PASS |
| [stepped, fixed–fixed, P_B = 40 kN] reaction: closed form vs FE (prismatic segments are exact) (absolute difference) | 0.15361304 | 0.15361304 | 8.33e-17 | 1.0e-12 | PASS |
| [stepped, fixed–fixed, P_B = 40 kN] junction displacement: closed form vs FE | 0.00010093144 | 0.00010093144 | 1.34e-16 | 1.0e-9 | PASS |
| [stepped, fixed–fixed, P_B = 40 kN] equilibrium of the whole bar (FE): R_left + P_B − R_right = 0 (absolute difference) | 1.1368684e-16 | 0.0000000 | 1.14e-16 | 1.0e-12 | PASS |
| [stepped, free end, heated] reaction: closed form vs FE (prismatic segments are exact) (absolute difference) | -9.0949470e-17 | 0.0000000 | 9.09e-17 | 1.0e-12 | PASS |
| [stepped, free end, heated] junction displacement: closed form vs FE | 0.00029474975 | 0.00029474975 | 3.68e-16 | 1.0e-9 | PASS |
| [stepped, free end, heated] equilibrium of the whole bar (FE): R_left + P_B − R_right = 0 (absolute difference) | 1.1823431e-15 | 0.0000000 | 1.18e-15 | 1.0e-12 | PASS |
| [stepped, gap 0.05 mm, P_B = 40 kN] reaction: closed form vs FE (prismatic segments are exact) (absolute difference) | 0.089204923 | 0.089204923 | 1.39e-16 | 1.0e-12 | PASS |
| [stepped, gap 0.05 mm, P_B = 40 kN] junction displacement: closed form vs FE | 0.00010861209 | 0.00010861209 | 1.25e-16 | 1.0e-9 | PASS |
| [stepped, gap 0.05 mm, P_B = 40 kN] equilibrium of the whole bar (FE): R_left + P_B − R_right = 0 (absolute difference) | 2.2737368e-16 | 0.0000000 | 2.27e-16 | 1.0e-12 | PASS |
| [stepped, gap 0.5 mm (stays open)] reaction: closed form vs FE (prismatic segments are exact) (absolute difference) | -6.1878984e-17 | 0.0000000 | 6.19e-17 | 1.0e-12 | PASS |
| [stepped, gap 0.5 mm (stays open)] junction displacement: closed form vs FE | 0.00011924975 | 0.00011924975 | 0.00e+0 | 1.0e-9 | PASS |
| [stepped, gap 0.5 mm (stays open)] equilibrium of the whole bar (FE): R_left + P_B − R_right = 0 (absolute difference) | 2.4377792e-16 | 0.0000000 | 2.44e-16 | 1.0e-12 | PASS |
| fully restrained prismatic steel bar heated 50 K: σ = −EαΔT | -1.1992500e+8 | -1.1992500e+8 | 0.00e+0 | 1.0e-12 | PASS |
| taper flexibility 4L/(πE·da·db) vs Simpson quadrature of ∫dx/(EA) | 1.6426248e-8 | 1.6426248e-8 | 1.55e-14 | 1.0e-10 | PASS |
| taper: FE converges at second order (observed 1.970) | true | true | 0.00e+0 | 0.0e+0 | PASS |
| taper: FE (N = 256) reaction vs closed form | 28734.541 | 28734.499 | 1.48e-6 | 2.0e-5 | PASS |
| taper: closed-form u(x) vs Simpson integration of the strain | 0.00013755429 | 0.00013755429 | 5.91e-16 | 1.0e-9 | PASS |
| thermal buckling ΔT_cr: E·α·ΔT_cr·A equals the fixed–fixed Euler load | 15890.717 | 15890.717 | 4.58e-16 | 1.0e-12 | PASS |
| units: ΔT of 100 K = 180 °F | 180.00000 | 180.00000 | 0.00e+0 | 1.0e-12 | PASS |
| units: 1 kip = 4.448 kN | 4448.2216 | 4448.2216 | 3.43e-9 | 1.0e-7 | PASS |

54 of 54 passed.

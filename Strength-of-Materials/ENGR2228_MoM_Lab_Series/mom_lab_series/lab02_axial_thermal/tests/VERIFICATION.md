# Verification record — lab02_axial_thermal

Run with `python3 shared/verify_lab.py lab02_axial_thermal` on 2026-10-27. Detailed tables are in the `results_*.md` files next to this one.

| Step | Result | Detail | Record |
|---|---|---|---|
| Build simulation page | PASS |  |  |
| Model tests: closed form vs independent numerics (Node, exact page code) | PASS | 54 of 54 passed | `results_node.md` |
| Independent re-implementation (Python/scipy) and data-pipeline closure | PASS | 22 of 22 passed | `results_python.md` |
| Handout re-solved from scratch vs instructor key | PASS | 50 of 50 agree | `results_from_scratch.md` |
| Cross-file consistency (units, symbols, sign convention, references) | PASS | 100 of 100 passed | `results_consistency.md` |
| Browser check, 375/1280 px, light/dark, every control | PASS | PASS | `results_browser.md` |

## Formula vs. independent numerical method (worst case over all material presets)

| Comparison | Worst relative difference | Tolerance | Result |
|---|---:|---:|---|
| F1: closed form vs event-tracking load path (absolute difference) | 8.9e-16 | 1.0e-10 | PASS |
| F2: closed form vs event-tracking load path (absolute difference) | 2.9e-15 | 1.0e-10 | PASS |
| equilibrium F1 + F2 = −P (relative to the largest force) (absolute difference) | 0.0e+00 | 1.0e-12 | PASS |
| F1: closed form vs Gaussian elimination of equilibrium + compatibility (absolute difference) | 2.2e-16 | 1.0e-12 | PASS |
| gap-closing load k1·g vs bisection-located contact event | 2.6e-16 | 1.0e-9 | PASS |
| load share E2A2/(E1A1 + E2A2) vs finite difference of numerical forces | 1.7e-04 | 3.0e-4 | PASS |
| superposition fails while the gap is open: F2(20 kN) ≠ 2·F2(10 kN) | 0.0e+00 | 0.0e+0 | PASS |
| dF/dT closed form vs central difference of the numerical solution | 1.8e-14 | 1.0e-9 | PASS |
| preload preserved at ΔT = 0 | 0.0e+00 | 1.0e-12 | PASS |
| reaction: closed form vs FE (prismatic segments are exact) (absolute difference) | 1.4e-16 | 1.0e-12 | PASS |
| junction displacement: closed form vs FE | 3.7e-16 | 1.0e-9 | PASS |
| equilibrium of the whole bar (FE): R_left + P_B − R_right = 0 (absolute difference) | 1.2e-15 | 1.0e-12 | PASS |
| fully restrained prismatic steel bar heated 50 K: σ = −EαΔT | 0.0e+00 | 1.0e-12 | PASS |
| taper flexibility 4L/(πE·da·db) vs Simpson quadrature of ∫dx/(EA) | 1.6e-14 | 1.0e-10 | PASS |
| taper: FE converges at second order (observed 1.970) | 0.0e+00 | 0.0e+0 | PASS |
| taper: FE (N = 256) reaction vs closed form | 1.5e-06 | 2.0e-5 | PASS |
| taper: closed-form u(x) vs Simpson integration of the strain | 5.9e-16 | 1.0e-9 | PASS |
| thermal buckling ΔT_cr: E·α·ΔT_cr·A equals the fixed–fixed Euler load | 4.6e-16 | 1.0e-12 | PASS |
| F1: JavaScript vs Python closed form (relative to largest force) (absolute) | 0.0e+00 | 1.0e-12 | PASS |
| F2: JavaScript vs Python closed form (absolute) | 0.0e+00 | 1.0e-12 | PASS |
| F1: JavaScript closed form vs numpy.linalg.solve of the 2×2 system (absolute) | 2.2e-16 | 1.0e-12 | PASS |
| rod in tube: gap-closing load k1·g (Python) | 0.0e+00 | 1.0e-12 | PASS |
| bolt and sleeve: dF/dT JavaScript vs Python | 1.5e-16 | 1.0e-12 | PASS |
| segment-1 flexibility: closed form vs scipy.quad | 2.0e-16 | 1.0e-11 | PASS |
| wall reaction: JavaScript vs Python closed form | 0.0e+00 | 1.0e-12 | PASS |
| wall reaction: closed form vs FE with N = 512 | 3.7e-07 | 1.0e-05 | PASS |
| thermal buckling ΔT for d = 10 mm, L = 0.5 m steel (Python vs hand: π²r²/(α(L/2)²)) | 0.0e+00 | 1.0e-12 | PASS |

Overall: **PASS**

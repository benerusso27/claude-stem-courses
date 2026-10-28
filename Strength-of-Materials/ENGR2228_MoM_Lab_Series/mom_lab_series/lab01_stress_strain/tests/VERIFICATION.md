# Verification record — lab01_stress_strain

Run with `python3 shared/verify_lab.py lab01_stress_strain` on 2026-10-27. Detailed tables are in the `results_*.md` files next to this one.

| Step | Result | Detail | Record |
|---|---|---|---|
| Build simulation page | PASS |  |  |
| Model tests: closed form vs independent numerics (Node, exact page code) | PASS | 77 of 77 passed | `results_node.md` |
| Independent re-implementation (Python/scipy) and data-pipeline closure | PASS | 43 of 43 passed | `results_python.md` |
| Handout re-solved from scratch vs instructor key | PASS | 45 of 45 agree | `results_from_scratch.md` |
| Cross-file consistency (units, symbols, sign convention, references) | PASS | 74 of 74 passed | `results_consistency.md` |
| Browser check, 375/1280 px, light/dark, every control | PASS | PASS | `results_browser.md` |

## Formula vs. independent numerical method (worst case over all material presets)

| Comparison | Worst relative difference | Tolerance | Result |
|---|---:|---:|---|
| σU: Considère closed form vs golden-section max of P(εp) | 4.5e-06 | 1.0e-5 | PASS |
| εu: Considère closed form − nσt,U/E correction vs golden-section max | 2.2e-05 | 5.0e-4 | PASS |
| uU: closed form vs adaptive Simpson ∫σt dεt | 1.5e-14 | 1.0e-9 | PASS |
| ∫σ dε (engineering) = ∫σt dεt (true) before necking | 9.0e-08 | 1.0e-7 | PASS |
| σU: marching solver (δ = 0, M = 8192) vs golden-section max | 2.8e-09 | 1.0e-6 | PASS |
| εu: marching solver (δ = 0) vs golden-section max | 2.2e-04 | 2.0e-3 | PASS |
| u to peak: trapezoid on solver path (δ = 0) vs closed-form integral at the exact peak | 2.4e-04 | 1.0e-3 | PASS |
| uU: Considère closed form vs energy to the exact peak | 6.7e-03 | 1.0e-2 | PASS |
| σU with δ: solver vs (1 − δ)·exact uniform-bar maximum | 2.8e-09 | 1.0e-6 | PASS |
| σY: solver vs K(ε0+0.002)^n·(1 − εY) | 1.1e-03 | 1.5e-3 | PASS |
| E: gage regression vs E(1 − 3σm/E)(1 − δℓ/L0) | 2.4e-05 | 4.0e-4 | PASS |
| E_app: crosshead regression vs springs in series 1/(1/E + A0·Cm/Lc) | 1.4e-05 | 4.0e-4 | PASS |
| E_app: textbook form with E vs crosshead regression | 2.4e-03 | 3.0e-3 | PASS |
| Δεt,u for δ = 0.0001: √(2nδ) estimate vs solver | 2.3e-02 | 6.0e-2 | PASS |
| Δεt,u for δ = 0.001: √(2nδ) estimate vs solver | 6.3e-02 | 1.2e-1 | PASS |
| equilibrium: σ·A = P on every section (max rel. error) | 9.8e-14 | 1.0e-10 | PASS |
| volume constancy of the neck zone (max rel. error) | 6.7e-16 | 1.0e-10 | PASS |
| compatibility: crosshead = gage + rest of reduced section + Cm·P | 2.2e-16 | 1.0e-12 | PASS |
| convergence order of σY ≈ 2 (observed 1.99) | 0.0e+00 | 0.0e+0 | PASS |
| convergence order of u(ε*) ≈ 2 (observed 2.00) | 0.0e+00 | 0.0e+0 | PASS |
| convergence: σU error at M = 610 below 1e-5 | 0.0e+00 | 0.0e+0 | PASS |
| mesh-set neck: elongation after fracture falls monotonically with N | 0.0e+00 | 0.0e+0 | PASS |
| mesh-set neck, N = 200: EL → uniform elongation of the rest of the gage | 7.4e-02 | 1.2e-1 | PASS |
| convergence order of σY ≈ 2 (observed 2.22) | 0.0e+00 | 0.0e+0 | PASS |
| convergence order of u(ε*) ≈ 2 (observed 1.99) | 0.0e+00 | 0.0e+0 | PASS |
| convergence order of σY ≈ 2 (observed 2.13) | 0.0e+00 | 0.0e+0 | PASS |
| sigY: JavaScript closed form vs Python closed form | 2.0e-16 | 1.0e-12 | PASS |
| sigU: JavaScript closed form vs Python closed form | 0.0e+00 | 1.0e-12 | PASS |
| e_u: JavaScript closed form vs Python closed form | 0.0e+00 | 1.0e-12 | PASS |
| uU: JavaScript closed form vs Python closed form | 0.0e+00 | 1.0e-12 | PASS |
| σU: page solver (δ = 0) vs scipy bounded maximization | 2.8e-09 | 1.0e-06 | PASS |
| εu: page solver (δ = 0) vs scipy maximization | 2.2e-04 | 2.0e-03 | PASS |
| 0.2 % offset on engineering curve: page solver vs scipy brentq | 8.9e-08 | 5.0e-05 | PASS |
| energy to peak: page trapezoid vs scipy quad | 2.4e-04 | 1.0e-03 | PASS |
| Considère closed form σU vs scipy exact maximum | 4.5e-06 | 1.0e-05 | PASS |

Overall: **PASS**

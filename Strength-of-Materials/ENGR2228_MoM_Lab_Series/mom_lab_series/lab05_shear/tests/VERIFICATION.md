# Verification record — lab05_shear

Run with `python3 shared/verify_lab.py lab05_shear` on 2026-10-27. Detailed tables are in the `results_*.md` files next to this one.

| Step | Result | Detail | Record |
|---|---|---|---|
| Build simulation page | PASS |  |  |
| Model tests: closed form vs independent numerics (Node, exact page code) | PASS | 79 of 79 passed | `results_node.md` |
| Independent re-implementation (Python/scipy) and data-pipeline closure | PASS | 80 of 80 passed | `results_python.md` |
| Handout re-solved from scratch vs instructor key | PASS | 50 of 50 agree | `results_from_scratch.md` |
| Cross-file consistency (units, symbols, sign convention, references) | PASS | 103 of 103 passed | `results_consistency.md` |
| Browser check, 375/1280 px, light/dark, every control | PASS | PASS | `results_browser.md` |

## Formula vs. independent numerical method (worst case over all material presets)

| Comparison | Worst relative difference | Tolerance | Result |
|---|---:|---:|---|
| rectangle: I = bh³/12 | 0.0e+00 | 1.0e-13 | PASS |
| rectangle: Q at the NA = bh²/8 | 0.0e+00 | 1.0e-13 | PASS |
| rectangle: τ_max = 3V/(2A) (Beer §6.1C) | 0.0e+00 | 1.0e-13 | PASS |
| rectangle: energy shear factor f_s = 6/5 | 1.8e-16 | 1.0e-13 | PASS |
| rectangle: f_s by strips (N_s = 2000) vs 6/5 | 5.0e-07 | 1.0e-6 | PASS |
| rectangle: I by strips (N_s = 2000) | 2.5e-07 | 1.0e-6 | PASS |
| rectangle: strip error in I falls as N_s⁻² (observed 2.000) | 0.0e+00 | 0.0e+0 | PASS |
| I-section: I vs hand formula | 8.5e-16 | 1.0e-13 | PASS |
| I-section: Q at the NA = B t_f (H − t_f)/2 + t_w h_w²/8 | 7.3e-16 | 1.0e-13 | PASS |
| I-section: τ in the web at the NA = VQ/(I t_w) | 1.6e-16 | 1.0e-13 | PASS |
| I-section: τ in the web at the junction = V B t_f (H − t_f)/(2 I t_w) | 8.8e-15 | 1.0e-9 | PASS |
| I-section: shear flow is continuous at the junction (q = VQ/I either side) | 1.6e-10 | 1.0e-6 | PASS |
| I-section: f_s exact layer integral vs strips (N_s = 4000) | 6.1e-08 | 5.0e-6 | PASS |
| I-section: f_s = 2.9007 lies between 1 and A/A_web = 3.2679 | 0.0e+00 | 0.0e+0 | PASS |
| tee: neutral axis, layer sums vs strips | 2.0e-14 | 1.0e-12 | PASS |
| tee: Q at the NA, layer formula vs strips | 7.5e-14 | 1.0e-9 | PASS |
| tee: f_s, exact integral vs strips (N_s = 4000) | 1.2e-07 | 5.0e-6 | PASS |
| tee: Q of the area above the NA = Q of the area below | 2.1e-16 | 1.0e-12 | PASS |
| box: neutral axis, layer sums vs strips | 3.6e-14 | 1.0e-12 | PASS |
| box: Q at the NA, layer formula vs strips | 5.0e-14 | 1.0e-9 | PASS |
| box: f_s, exact integral vs strips (N_s = 4000) | 6.9e-08 | 5.0e-6 | PASS |
| box: Q of the area above the NA = Q of the area below | 3.5e-16 | 1.0e-12 | PASS |
| circle: τ_max = 4V/(3A) (Beer §6.1C) | 0.0e+00 | 1.0e-13 | PASS |
| circle: f_s = 10/9 vs strips (N_s = 20000) | 6.1e-08 | 2.0e-5 | PASS |
| circle: strip error in I converges at order 1.5 (width ∝ √distance at the poles; observed 1.430) | 0.0e+00 | 0.0e+0 | PASS |
| b/h = 0.5: face value τ/(VQ/Ib), series vs finite differences (96 cells) | 1.8e-05 | 1.0e-3 | PASS |
| b/h = 0.5: center value, series vs finite differences | 9.3e-06 | 1.0e-3 | PASS |
| b/h = 0.5: width-average of the elasticity solution = VQ/(Ib) (∫τ dx = VQ/I) | 2.4e-12 | 1.0e-6 | PASS |
| b/h = 0.5: finite-difference error falls as N⁻² (observed 2.001) | 0.0e+00 | 0.0e+0 | PASS |
| b/h = 2: face value τ/(VQ/Ib), series vs finite differences (96 cells) | 4.8e-04 | 1.0e-3 | PASS |
| b/h = 2: center value, series vs finite differences | 1.3e-04 | 1.0e-3 | PASS |
| b/h = 2: width-average of the elasticity solution = VQ/(Ib) (∫τ dx = VQ/I) | 1.0e-11 | 1.0e-6 | PASS |
| b/h = 2: finite-difference error falls as N⁻² (observed 1.943) | 0.0e+00 | 0.0e+0 | PASS |
| ν = 0: the elasticity solution is the elementary one (b/h = 2) | 0.0e+00 | 1.0e-14 | PASS |
| ν = 0.25, b/h = 0.5: face value matches the value tabulated in Beer §6.1C (3 figures) | 2.5e-04 | 5.0e-4 | PASS |
| ν = 0.25, b/h = 2: face value matches the value tabulated in Beer §6.1C (3 figures) | 2.8e-04 | 5.0e-4 | PASS |
| ν = 0.25, b/h = 4: face value matches the value tabulated in Beer §6.1C (3 figures) | 3.3e-05 | 5.0e-4 | PASS |
| deflection: closed form vs 256 reduced-integration elements | 1.3e-05 | 2.0e-5 | PASS |
| element error falls as N_e⁻² (observed 2.000) | 0.0e+00 | 0.0e+0 | PASS |
| span with a 5 % shear part: closed form vs bisection on the elements | 5.8e-04 | 2.0e-3 | PASS |
| slender limit (L/h = 50): elements → Euler–Bernoulli within the shear part | 6.1e-03 | 9.6e-3 | PASS |
| shear locking: 4 fully integrated elements give 11.6 % of the deflection (< 50 %) | 0.0e+00 | 0.0e+0 | PASS |
| rectangle: δ_shear/δ_bending = 3EI f_s/(GA L²) for a cantilever (closed form vs formula) | 2.1e-16 | 1.0e-12 | PASS |
| midspan deflection: closed form vs finite differences (4000 intervals) | 1.3e-07 | 2.0e-6 | PASS |
| end slip: closed form vs finite differences | 1.0e-06 | 2.0e-4 | PASS |
| δ_full ≤ δ ≤ δ_loose | 0.0e+00 | 0.0e+0 | PASS |
| loose limit: k → 0 gives PL³/(48EI₀) | 4.8e-15 | 1.0e-9 | PASS |
| bonded limit: k → ∞ gives PL³/(48EI_full) | 5.6e-08 | 1.0e-6 | PASS |
| two equal layers: EI_full = 4 EI₀ | 0.0e+00 | 1.0e-12 | PASS |
| loose end slip = r θ_end = r PL²/(16EI₀) | 0.0e+00 | 1.0e-12 | PASS |
| closed form: small-αL series and full formula join at αL/2 = 0.05 (point load) | 7.7e-10 | 1.0e-9 | PASS |
| closed form: series and full formula join at αL/2 = 0.05 (uniform load) | 8.6e-10 | 1.0e-9 | PASS |
| finite-difference error falls as n⁻² (observed 1.995) | 0.0e+00 | 0.0e+0 | PASS |
| discrete springs at 5 mm spacing → smeared closed form | 4.8e-05 | 2.0e-4 | PASS |
| discrete springs: shooting leaves N(L) = 0 (relative to the largest bolt force) (absolute difference) | 3.3e-14 | 1.0e-10 | PASS |
| discrete springs: forces antisymmetric about midspan | 1.9e-14 | 1.0e-9 | PASS |
| Beer's q for two equal layers = 3V/(4t) | 0.0e+00 | 1.0e-12 | PASS |
| rectUp: I, JavaScript layer sums vs Python quadrature | 1.9e-16 | 1.0e-11 | PASS |
| rectUp: neutral axis | 0.0e+00 | 1.0e-11 | PASS |
| rectUp: Q at the NA | 4.1e-16 | 1.0e-11 | PASS |
| rectUp: f_s, JavaScript exact antiderivative vs Python nested quadrature | 1.8e-16 | 1.0e-08 | PASS |
| rectUp: τ = VQ/(It) at y = 5.08 mm | 1.5e-16 | 1.0e-10 | PASS |
| rectUp: τ = VQ/(It) at y = 15.24 mm | 7.6e-16 | 1.0e-10 | PASS |
| rectUp: τ = VQ/(It) at y = 22.86 mm | 4.3e-16 | 1.0e-10 | PASS |
| ibeamWeb: I, JavaScript layer sums vs Python quadrature | 1.7e-16 | 1.0e-11 | PASS |
| ibeamWeb: neutral axis | 0.0e+00 | 1.0e-11 | PASS |
| ibeamWeb: Q at the NA | 3.7e-16 | 1.0e-11 | PASS |
| ibeamWeb: f_s, JavaScript exact antiderivative vs Python nested quadrature | 1.1e-15 | 1.0e-08 | PASS |
| ibeamWeb: τ = VQ/(It) at y = 10.16 mm | 3.7e-16 | 1.0e-10 | PASS |
| ibeamWeb: τ = VQ/(It) at y = 30.48 mm | 5.0e-16 | 1.0e-10 | PASS |
| ibeamWeb: τ = VQ/(It) at y = 45.72 mm | 4.8e-16 | 1.0e-10 | PASS |
| tee: I, JavaScript layer sums vs Python quadrature | 1.6e-16 | 1.0e-11 | PASS |
| tee: neutral axis | 0.0e+00 | 1.0e-11 | PASS |
| tee: Q at the NA | 4.3e-16 | 1.0e-11 | PASS |
| tee: f_s, JavaScript exact antiderivative vs Python nested quadrature | 5.5e-16 | 1.0e-08 | PASS |
| tee: τ = VQ/(It) at y = 12.00 mm | 1.0e-15 | 1.0e-10 | PASS |
| tee: τ = VQ/(It) at y = 36.00 mm | 7.8e-16 | 1.0e-10 | PASS |
| tee: τ = VQ/(It) at y = 54.00 mm | 3.0e-16 | 1.0e-10 | PASS |
| box: I, JavaScript layer sums vs Python quadrature | 2.1e-16 | 1.0e-11 | PASS |
| box: neutral axis | 2.3e-16 | 1.0e-11 | PASS |
| box: Q at the NA | 3.5e-16 | 1.0e-11 | PASS |
| box: f_s, JavaScript exact antiderivative vs Python nested quadrature | 1.7e-15 | 1.0e-08 | PASS |
| box: τ = VQ/(It) at y = 12.00 mm | 5.9e-16 | 1.0e-10 | PASS |
| box: τ = VQ/(It) at y = 36.00 mm | 8.0e-16 | 1.0e-10 | PASS |
| box: τ = VQ/(It) at y = 54.00 mm | 7.6e-16 | 1.0e-10 | PASS |
| circle: I = πc⁴/4, JavaScript vs Python | 0.0e+00 | 1.0e-13 | PASS |
| circle: f_s, JavaScript 10/9 vs Python adaptive quadrature | 1.6e-09 | 1.0e-08 | PASS |
| circle: τ_max, JavaScript vs Python | 2.7e-16 | 1.0e-12 | PASS |
| wide rectangle b = 25.4, h = 50.8 mm, ν = 0.33, x = 1·b/2: τ/(VQ/Ib), cosine series in y (JS) vs sine series in x (Python) | 1.5e-09 | 2.0e-07 | PASS |
| wide rectangle b = 25.4, h = 50.8 mm, ν = 0.33, x = 0·b/2: τ/(VQ/Ib), cosine series in y (JS) vs sine series in x (Python) | 6.5e-14 | 2.0e-07 | PASS |
| wide rectangle b = 25.4, h = 50.8 mm, ν = 0.33, x = 0.5·b/2: τ/(VQ/Ib), cosine series in y (JS) vs sine series in x (Python) | 6.4e-14 | 2.0e-07 | PASS |
| wide rectangle b = 50.8, h = 25.4 mm, ν = 0.33, x = 1·b/2: τ/(VQ/Ib), cosine series in y (JS) vs sine series in x (Python) | 4.2e-09 | 2.0e-07 | PASS |
| wide rectangle b = 50.8, h = 25.4 mm, ν = 0.33, x = 0·b/2: τ/(VQ/Ib), cosine series in y (JS) vs sine series in x (Python) | 5.8e-12 | 2.0e-07 | PASS |
| wide rectangle b = 50.8, h = 25.4 mm, ν = 0.33, x = 0.5·b/2: τ/(VQ/Ib), cosine series in y (JS) vs sine series in x (Python) | 5.2e-12 | 2.0e-07 | PASS |
| wide rectangle b = 40.0, h = 10.0 mm, ν = 0.25, x = 1·b/2: τ/(VQ/Ib), cosine series in y (JS) vs sine series in x (Python) | 5.1e-09 | 2.0e-07 | PASS |
| wide rectangle b = 40.0, h = 10.0 mm, ν = 0.25, x = 0·b/2: τ/(VQ/Ib), cosine series in y (JS) vs sine series in x (Python) | 2.0e-11 | 2.0e-07 | PASS |
| wide rectangle b = 40.0, h = 10.0 mm, ν = 0.25, x = 0.5·b/2: τ/(VQ/Ib), cosine series in y (JS) vs sine series in x (Python) | 1.9e-11 | 2.0e-07 | PASS |
| wide rectangle b = 10.0, h = 30.0 mm, ν = 0.3, x = 1·b/2: τ/(VQ/Ib), cosine series in y (JS) vs sine series in x (Python) | 9.6e-10 | 2.0e-07 | PASS |
| wide rectangle b = 10.0, h = 30.0 mm, ν = 0.3, x = 0·b/2: τ/(VQ/Ib), cosine series in y (JS) vs sine series in x (Python) | 1.0e-13 | 2.0e-07 | PASS |
| wide rectangle b = 10.0, h = 30.0 mm, ν = 0.3, x = 0.5·b/2: τ/(VQ/Ib), cosine series in y (JS) vs sine series in x (Python) | 1.0e-13 | 2.0e-07 | PASS |
| Timoshenko bending part, JavaScript vs Python | 0.0e+00 | 1.0e-13 | PASS |
| Timoshenko shear part | 1.3e-16 | 1.0e-13 | PASS |
| midspan deflection: JavaScript closed form vs scipy solve_bvp | 3.4e-14 | 2.0e-07 | PASS |
| end slip: closed form vs solve_bvp | 1.6e-15 | 2.0e-05 | PASS |
| discrete springs: midspan deflection, JavaScript vs Python | 8.7e-14 | 1.0e-10 | PASS |
| discrete springs: end slip | 2.1e-16 | 1.0e-09 | PASS |
| discrete springs: largest bolt force | 6.3e-13 | 1.0e-09 | PASS |

Overall: **PASS**

# Verification record — lab03_torsion

Run with `python3 shared/verify_lab.py lab03_torsion` on 2026-10-27. Detailed tables are in the `results_*.md` files next to this one.

| Step | Result | Detail | Record |
|---|---|---|---|
| Build simulation page | PASS |  |  |
| Model tests: closed form vs independent numerics (Node, exact page code) | PASS | 79 of 79 passed | `results_node.md` |
| Independent re-implementation (Python/scipy) and data-pipeline closure | PASS | 69 of 69 passed | `results_python.md` |
| Handout re-solved from scratch vs instructor key | PASS | 39 of 39 agree | `results_from_scratch.md` |
| Cross-file consistency (units, symbols, sign convention, references) | PASS | 95 of 95 passed | `results_consistency.md` |
| Browser check, 375/1280 px, light/dark, every control | PASS | PASS | `results_browser.md` |

## Formula vs. independent numerical method (worst case over all material presets)

| Comparison | Worst relative difference | Tolerance | Result |
|---|---:|---:|---|
| plateau law continuous at the end of the plateau (γ_L ± 1e−9) | 1.6e-08 | 1.0e-6 | PASS |
| plateau law: τ = τ_Y on the plateau | 0.0e+00 | 1.0e-14 | PASS |
| Ramberg–Osgood inverse: γ(τ(γ)) = γ at γ = 0.0001 | 0.0e+00 | 1.0e-12 | PASS |
| Ramberg–Osgood inverse: γ(τ(γ)) = γ at γ = 0.003 | 2.9e-16 | 1.0e-12 | PASS |
| Ramberg–Osgood inverse: γ(τ(γ)) = γ at γ = 0.05 | 1.1e-15 | 1.0e-12 | PASS |
| Ramberg–Osgood inverse: γ(τ(γ)) = γ at γ = 0.5 | 6.7e-16 | 1.0e-12 | PASS |
| odd symmetry τ(−γ) = −τ(γ) | 0.0e+00 | 1.0e-15 | PASS |
| EPP torque at θ = 0.5θ_Y: closed form vs rings (N = 4096) | 3.0e-08 | 2.0e-7 | PASS |
| EPP torque at θ = 0.5θ_Y: closed form vs Simpson quadrature | 1.9e-15 | 1.0e-10 | PASS |
| EPP torque at θ = 1θ_Y: closed form vs rings (N = 4096) | 3.0e-08 | 2.0e-7 | PASS |
| EPP torque at θ = 1θ_Y: closed form vs Simpson quadrature | 1.9e-15 | 1.0e-10 | PASS |
| EPP torque at θ = 1.5θ_Y: closed form vs rings (N = 4096) | 1.4e-08 | 2.0e-7 | PASS |
| EPP torque at θ = 1.5θ_Y: closed form vs Simpson quadrature | 1.7e-16 | 1.0e-10 | PASS |
| EPP torque at θ = 3θ_Y: closed form vs rings (N = 4096) | 1.4e-08 | 2.0e-7 | PASS |
| EPP torque at θ = 3θ_Y: closed form vs Simpson quadrature | 1.3e-15 | 1.0e-10 | PASS |
| EPP torque at θ = 10θ_Y: closed form vs rings (N = 4096) | 1.4e-08 | 2.0e-7 | PASS |
| EPP torque at θ = 10θ_Y: closed form vs Simpson quadrature | 1.2e-15 | 1.0e-10 | PASS |
| EPP torque at θ = 100θ_Y: closed form vs rings (N = 4096) | 1.5e-08 | 2.0e-7 | PASS |
| EPP torque at θ = 100θ_Y: closed form vs Simpson quadrature | 1.6e-15 | 1.0e-10 | PASS |
| Beer §3.7 form (4/3)T_Y[1 − ¼(ρ_Y/c)³] at φ = 1.5φ_Y | 0.0e+00 | 1.0e-14 | PASS |
| Beer §3.7 form (4/3)T_Y[1 − ¼(ρ_Y/c)³] at φ = 3φ_Y | 1.6e-16 | 1.0e-14 | PASS |
| Beer §3.7 form (4/3)T_Y[1 − ¼(ρ_Y/c)³] at φ = 10φ_Y | 0.0e+00 | 1.0e-14 | PASS |
| fully plastic limit T → (4/3)T_Y (solid) | 0.0e+00 | 1.0e-12 | PASS |
| elastic: T = JGφ/L (closed form) vs rings N = 4096 | 3.0e-08 | 1.0e-7 | PASS |
| ring integration converges at second order (observed 2.018) | 0.0e+00 | 0.0e+0 | PASS |
| inverse: twist for T = 1.05T_Y, closed form vs bisection on rings (N = 2048) | 1.4e-07 | 1.0e-6 | PASS |
| inverse: twist for T = 1.2T_Y, closed form vs bisection on rings (N = 2048) | 2.7e-07 | 1.0e-6 | PASS |
| inverse: twist for T = 1.3T_Y, closed form vs bisection on rings (N = 2048) | 6.2e-07 | 1.0e-6 | PASS |
| residual stresses carry zero net torque (rings, relative to T) (absolute difference) | 1.6e-08 | 1.0e-6 | PASS |
| permanent twist ratio φ_p/φ_Y after unloading from 3φ_Y (EPP: 3 − 1.3210) | 4.0e-16 | 1.0e-12 | PASS |
| surface residual stress τ_Y − T c/J (closed form) vs rings | 5.9e-08 | 1.0e-6 | PASS |
| torque at θ = 0.5θ_Y: rings (N = 4096) vs Simpson | 3.0e-08 | 3.0e-7 | PASS |
| torque at θ = 2θ_Y: rings (N = 4096) vs Simpson | 1.9e-08 | 3.0e-7 | PASS |
| torque at θ = 20θ_Y: rings (N = 4096) vs Simpson | 1.8e-08 | 3.0e-7 | PASS |
| torque at θ = 500θ_Y: rings (N = 4096) vs Simpson | 1.7e-08 | 3.0e-7 | PASS |
| torque at θ = 150θ_Y: rings (N = 4096) vs Simpson | 1.6e-08 | 3.0e-7 | PASS |
| torque at θ = 1θ_Y: rings (N = 4096) vs Simpson | 2.8e-08 | 3.0e-7 | PASS |
| torque at θ = 1.4θ_Y: rings (N = 4096) vs Simpson | 2.6e-08 | 3.0e-7 | PASS |
| hand value (3 s.f.): c₁ for a/b = 1 | 8.0e-04 | 2.5e-3 | PASS |
| hand value (3–4 s.f.): c₂ for a/b = 1 | 1.6e-04 | 2.5e-3 | PASS |
| hand value (3 s.f.): c₁ for a/b = 2 | 4.9e-04 | 2.5e-3 | PASS |
| hand value (3–4 s.f.): c₂ for a/b = 2 | 1.4e-03 | 2.5e-3 | PASS |
| hand value (3 s.f.): c₁ for a/b = 10 | 1.0e-03 | 2.5e-3 | PASS |
| hand value (3–4 s.f.): c₂ for a/b = 10 | 1.0e-03 | 2.5e-3 | PASS |
| thin strip: c₂ → (1/3)[1 − (192/π⁵)(31/32)ζ(5) b/a] for a/b = 1000 | 0.0e+00 | 1.0e-9 | PASS |
| c₂: Richardson-extrapolated finite differences (N = 16, 32) vs series | 3.3e-05 | 5.0e-5 | PASS |
| τ_max/(Gθb): Richardson-extrapolated finite differences vs series | 1.2e-05 | 2.0e-4 | PASS |
| finite differences converge at second order for c₂ (observed 1.970) | 0.0e+00 | 0.0e+0 | PASS |
| shear along the centre line at y = 0.1b: series vs finite differences (N = 32) | 8.2e-05 | 3.0e-3 | PASS |
| shear along the centre line at y = 0.25b: series vs finite differences (N = 32) | 9.8e-05 | 3.0e-3 | PASS |
| shear along the centre line at y = 0.4b: series vs finite differences (N = 32) | 1.1e-04 | 3.0e-3 | PASS |
| Bredt → exact as t/r_m → 0 (stress, t/r_m = 0.002) | 1.0e-03 | 1.5e-3 | PASS |
| Bredt → exact as t/r_m → 0 (twist) | 1.0e-06 | 1.0e-5 | PASS |
| tube: torque from ring integration of Tρ/J equals T | 7.3e-10 | 1.0e-7 | PASS |
| preset steel specimen d = 6.35 mm: T_Y = τ_Y πc³/2 (hand: 8.547 N·m) | 3.2e-05 | 1.0e-4 | PASS |
| preset steel specimen: φ_Y over 50.8 mm (hand: 1.960°) | 1.6e-04 | 2.0e-4 | PASS |
| EPP torque, c = 3.17 mm, c_i/c = 0, θ = 0.4715: JavaScript vs Python | 0.0e+00 | 1.0e-13 | PASS |
| … closed form vs scipy.quad of the EPP law | 4.0e-16 | 1.0e-10 | PASS |
| EPP torque, c = 3.17 mm, c_i/c = 0, θ = 1.01: JavaScript vs Python | 0.0e+00 | 1.0e-13 | PASS |
| EPP torque, c = 3.17 mm, c_i/c = 0, θ = 2.694: JavaScript vs Python | 0.0e+00 | 1.0e-13 | PASS |
| EPP torque, c = 3.17 mm, c_i/c = 0, θ = 33.68: JavaScript vs Python | 0.0e+00 | 1.0e-13 | PASS |
| EPP torque, c = 3.17 mm, c_i/c = 0.6, θ = 0.4715: JavaScript vs Python | 0.0e+00 | 1.0e-13 | PASS |
| EPP torque, c = 3.17 mm, c_i/c = 0.6, θ = 1.01: JavaScript vs Python | 0.0e+00 | 1.0e-13 | PASS |
| EPP torque, c = 3.17 mm, c_i/c = 0.6, θ = 2.694: JavaScript vs Python | 2.0e-16 | 1.0e-13 | PASS |
| EPP torque, c = 3.17 mm, c_i/c = 0.6, θ = 33.68: JavaScript vs Python | 2.0e-16 | 1.0e-13 | PASS |
| EPP torque, c = 25 mm, c_i/c = 0.6, θ = 0.05987: JavaScript vs Python | 0.0e+00 | 1.0e-13 | PASS |
| EPP torque, c = 25 mm, c_i/c = 0.6, θ = 0.1283: JavaScript vs Python | 0.0e+00 | 1.0e-13 | PASS |
| EPP torque, c = 25 mm, c_i/c = 0.6, θ = 0.3421: JavaScript vs Python | 0.0e+00 | 1.0e-13 | PASS |
| EPP torque, c = 25 mm, c_i/c = 0.6, θ = 4.277: JavaScript vs Python | 0.0e+00 | 1.0e-13 | PASS |
| ring integration (N = 2048) vs scipy.quad of the same law, θ = 0.5388 rad/m | 1.2e-07 | 1.0e-06 | PASS |
| ring integration (N = 2048) vs scipy.quad of the same law, θ = 2.021 rad/m | 5.7e-08 | 1.0e-06 | PASS |
| ring integration (N = 2048) vs scipy.quad of the same law, θ = 26.94 rad/m | 7.3e-08 | 1.0e-06 | PASS |
| ring integration (N = 2048) vs scipy.quad of the same law, θ = 1.531 rad/m | 1.1e-07 | 1.0e-06 | PASS |
| ring integration (N = 2048) vs scipy.quad of the same law, θ = 5.742 rad/m | 6.5e-08 | 1.0e-06 | PASS |
| ring integration (N = 2048) vs scipy.quad of the same law, θ = 76.56 rad/m | 6.3e-08 | 1.0e-06 | PASS |
| ring integration (N = 2048) vs scipy.quad of the same law, θ = 1.315 rad/m | 1.1e-07 | 1.0e-06 | PASS |
| rectangle a/b = 1: c₁ JavaScript vs Python series | 2.7e-16 | 1.0e-12 | PASS |
| rectangle a/b = 1: c₂ JavaScript vs Python series | 2.0e-16 | 1.0e-12 | PASS |
| rectangle a/b = 1.5: c₁ JavaScript vs Python series | 1.2e-16 | 1.0e-12 | PASS |
| rectangle a/b = 1.5: c₂ JavaScript vs Python series | 1.4e-16 | 1.0e-12 | PASS |
| rectangle a/b = 3: c₁ JavaScript vs Python series | 0.0e+00 | 1.0e-12 | PASS |
| rectangle a/b = 3: c₂ JavaScript vs Python series | 0.0e+00 | 1.0e-12 | PASS |
| rectangle a/b = 10: c₁ JavaScript vs Python series | 1.8e-16 | 1.0e-12 | PASS |
| rectangle a/b = 10: c₂ JavaScript vs Python series | 1.8e-16 | 1.0e-12 | PASS |
| rectangle FD a/b = 1, N = 8: conjugate gradients (page) vs sparse direct solve (scipy), c₂ | 4.1e-16 | 1.0e-09 | PASS |
| … same grid, τ_max coefficient k | 2.2e-14 | 1.0e-09 | PASS |
| rectangle FD a/b = 2, N = 16: conjugate gradients (page) vs sparse direct solve (scipy), c₂ | 3.4e-15 | 1.0e-09 | PASS |
| rectangle FD a/b = 4, N = 8: conjugate gradients (page) vs sparse direct solve (scipy), c₂ | 1.0e-15 | 1.0e-09 | PASS |
| rectangle a/b = 1.0: series c₂ vs Richardson-extrapolated scipy FD (N = 32, 64) | 2.4e-06 | 2.0e-05 | PASS |
| rectangle a/b = 2.0: series c₂ vs Richardson-extrapolated scipy FD (N = 32, 64) | 7.5e-07 | 2.0e-05 | PASS |
| rectangle a/b = 3.0: series c₂ vs Richardson-extrapolated scipy FD (N = 32, 64) | 4.4e-07 | 2.0e-05 | PASS |
| tube t = 1 mm: Bredt stress JavaScript vs Python | 0.0e+00 | 1.0e-13 | PASS |
| tube t = 1 mm: exact stress JavaScript vs Python | 0.0e+00 | 1.0e-13 | PASS |
| tube t = 5 mm: Bredt stress JavaScript vs Python | 0.0e+00 | 1.0e-13 | PASS |
| tube t = 5 mm: exact stress JavaScript vs Python | 0.0e+00 | 1.0e-13 | PASS |
| tube t = 15 mm: Bredt stress JavaScript vs Python | 0.0e+00 | 1.0e-13 | PASS |
| tube t = 15 mm: exact stress JavaScript vs Python | 0.0e+00 | 1.0e-13 | PASS |

Overall: **PASS**

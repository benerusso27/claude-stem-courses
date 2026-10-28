# Verification record — lab04_bending

Run with `python3 shared/verify_lab.py lab04_bending` on 2026-10-27. Detailed tables are in the `results_*.md` files next to this one.

| Step | Result | Detail | Record |
|---|---|---|---|
| Build simulation page | PASS |  |  |
| Model tests: closed form vs independent numerics (Node, exact page code) | PASS | 79 of 79 passed | `results_node.md` |
| Independent re-implementation (Python/scipy) and data-pipeline closure | PASS | 53 of 53 passed | `results_python.md` |
| Handout re-solved from scratch vs instructor key | PASS | 62 of 62 agree | `results_from_scratch.md` |
| Cross-file consistency (units, symbols, sign convention, references) | PASS | 101 of 101 passed | `results_consistency.md` |
| Browser check, 375/1280 px, light/dark, every control | PASS | PASS | `results_browser.md` |

## Formula vs. independent numerical method (worst case over all material presets)

| Comparison | Worst relative difference | Tolerance | Result |
|---|---:|---:|---|
| Ramberg–Osgood inverse ε(σ(ε)) = ε at ε = 0.0001 | 0.0e+00 | 1.0e-12 | PASS |
| Ramberg–Osgood inverse ε(σ(ε)) = ε at ε = 0.0039 | 1.1e-16 | 1.0e-12 | PASS |
| Ramberg–Osgood inverse ε(σ(ε)) = ε at ε = 0.008 | 6.5e-16 | 1.0e-12 | PASS |
| Ramberg–Osgood inverse ε(σ(ε)) = ε at ε = 0.03 | 1.0e-15 | 1.0e-12 | PASS |
| steel law continuous at the end of the plateau | 2.6e-09 | 1.0e-6 | PASS |
| R_A: statics vs shooting integration (absolute difference) | 6.7e-11 | 1.0e-9 | PASS |
| R_B: statics vs shooting integration (absolute difference) | 6.7e-11 | 1.0e-9 | PASS |
| M(x) at every node: largest \|error\|/\|M\|max = 2.02e-10 (tolerance 1e-9) | 0.0e+00 | 0.0e+0 | PASS |
| dM/dx = V at x = 0.078 m (relative to \|V\|max) (absolute difference) | 4.8e-12 | 1.0e-6 | PASS |
| dM/dx = V at x = 0.186 m (relative to \|V\|max) (absolute difference) | 1.4e-11 | 1.0e-6 | PASS |
| dM/dx = V at x = 0.342 m (relative to \|V\|max) (absolute difference) | 2.4e-11 | 1.0e-6 | PASS |
| dM/dx = V at x = 0.498 m (relative to \|V\|max) (absolute difference) | 4.6e-11 | 1.0e-6 | PASS |
| fixed-end moment: statics vs integration from the free end | 9.5e-07 | 1.0e-5 | PASS |
| M(x) at every node: largest \|error\|/\|M\|max = 9.54e-7 (tolerance 0.00002) | 0.0e+00 | 0.0e+0 | PASS |
| dM/dx = V at x = 0.260 m (relative to \|V\|max) (absolute difference) | 9.1e-11 | 1.0e-6 | PASS |
| dM/dx = V at x = 0.620 m (relative to \|V\|max) (absolute difference) | 6.4e-11 | 1.0e-6 | PASS |
| dM/dx = V at x = 1.140 m (relative to \|V\|max) (absolute difference) | 5.2e-11 | 1.0e-6 | PASS |
| dM/dx = V at x = 1.660 m (relative to \|V\|max) (absolute difference) | 1.4e-11 | 1.0e-6 | PASS |
| M(x) at every node: largest \|error\|/\|M\|max = 0.00e+0 (tolerance 1e-9) | 0.0e+00 | 0.0e+0 | PASS |
| dM/dx = V at x = 0.520 m (relative to \|V\|max) (absolute difference) | 1.7e-11 | 1.0e-6 | PASS |
| dM/dx = V at x = 1.240 m (relative to \|V\|max) (absolute difference) | 2.8e-11 | 1.0e-6 | PASS |
| dM/dx = V at x = 2.280 m (relative to \|V\|max) (absolute difference) | 4.7e-11 | 1.0e-6 | PASS |
| dM/dx = V at x = 3.320 m (relative to \|V\|max) (absolute difference) | 9.1e-11 | 1.0e-6 | PASS |
| M(x) at every node: largest \|error\|/\|M\|max = 7.55e-7 (tolerance 0.00002) | 0.0e+00 | 0.0e+0 | PASS |
| M(x) at every node: largest \|error\|/\|M\|max = 7.31e-11 (tolerance 1e-9) | 0.0e+00 | 0.0e+0 | PASS |
| dM/dx = V at x = 0.325 m (relative to \|V\|max) (absolute difference) | 3.1e-11 | 1.0e-6 | PASS |
| dM/dx = V at x = 0.775 m (relative to \|V\|max) (absolute difference) | 4.1e-11 | 1.0e-6 | PASS |
| dM/dx = V at x = 1.425 m (relative to \|V\|max) (absolute difference) | 1.2e-10 | 1.0e-6 | PASS |
| dM/dx = V at x = 2.075 m (relative to \|V\|max) (absolute difference) | 3.5e-10 | 1.0e-6 | PASS |
| hand value: 4-point bending, M = (P/2)a = 2000 N·m | 1.1e-16 | 1.0e-12 | PASS |
| hand value: cantilever with triangular load, fixed-end moment w₀L²/3 | 0.0e+00 | 1.0e-12 | PASS |
| hand value: overhang, M over the roller = −4 kN·m | 1.8e-12 | 1.0e-9 | PASS |
| triangular load: trapezoid integration converges at second order (observed 2.000) | 0.0e+00 | 0.0e+0 | PASS |
| rectangle: I = bh³/12 (transformed routine) | 0.0e+00 | 1.0e-12 | PASS |
| rectangle, elastic: M = EIκ vs strip summation (N = 2000) | 2.5e-07 | 1.0e-6 | PASS |
| rectangle, elastic: neutral axis at mid-depth (relative to h) (absolute difference) | 3.4e-16 | 1.0e-12 | PASS |
| composite: transformed-section centroid vs hand formula | 0.0e+00 | 1.0e-12 | PASS |
| composite: transformed I vs hand formula | 0.0e+00 | 1.0e-12 | PASS |
| composite: neutral axis, transformed section vs strip equilibrium | 1.4e-16 | 1.0e-9 | PASS |
| composite: M = E₁I_tκ vs strip summation | 2.1e-07 | 1.0e-6 | PASS |
| composite: steel stress = n × aluminum stress at the same strain | 0.0e+00 | 1.0e-12 | PASS |
| EPP rectangle at κ = 0.5κ_Y: §4.6 formula vs strip summation (N = 2000) | 2.5e-07 | 2.0e-6 | PASS |
| EPP rectangle at κ = 1κ_Y: §4.6 formula vs strip summation (N = 2000) | 2.5e-07 | 2.0e-6 | PASS |
| EPP rectangle at κ = 1.5κ_Y: §4.6 formula vs strip summation (N = 2000) | 6.5e-08 | 2.0e-6 | PASS |
| EPP rectangle at κ = 3κ_Y: §4.6 formula vs strip summation (N = 2000) | 5.8e-08 | 2.0e-6 | PASS |
| EPP rectangle at κ = 10κ_Y: §4.6 formula vs strip summation (N = 2000) | 1.7e-07 | 2.0e-6 | PASS |
| Beer's form (3/2)M_Y[1 − ⅓(y_Y/c)²] at κ = 1.5κ_Y | 0.0e+00 | 1.0e-14 | PASS |
| Beer's form (3/2)M_Y[1 − ⅓(y_Y/c)²] at κ = 3κ_Y | 0.0e+00 | 1.0e-14 | PASS |
| rectangle: plastic modulus Z = bh²/4 (equal-area routine) | 0.0e+00 | 1.0e-12 | PASS |
| rectangle: shape factor M_p/M_Y = 1.5 | 0.0e+00 | 1.0e-12 | PASS |
| strip summation converges at second order (observed 1.979) | 0.0e+00 | 0.0e+0 | PASS |
| residual stresses: net force / (σ_Y A) = 0 (absolute difference) | 1.7e-15 | 1.0e-6 | PASS |
| residual stresses: net moment / M_Y = 0 (absolute difference) | 9.0e-08 | 1.0e-6 | PASS |
| inverse: κ for M = 1.3 M_Y (bisection on strips) vs the §4.6 formula inverted | 1.5e-07 | 1.0e-5 | PASS |
| I-section: plastic modulus vs hand formula b t_f(h − t_f) + t_w h_w²/4 | 2.3e-16 | 1.0e-12 | PASS |
| I-section: fully plastic moment σ_Y Z vs strip summation at κ = 10⁴κ_Y | 4.0e-15 | 1.0e-5 | PASS |
| I-section: I vs hand formula | 4.8e-16 | 1.0e-12 | PASS |
| T-section: fully plastic moment σ_Y Z vs strip summation | 3.0e-08 | 1.0e-4 | PASS |
| T-section: plastic neutral axis divides the area equally (strip vs equal-area routine) | 2.8e-05 | 1.0e-3 | PASS |
| 4-point bending at x = 0.05 m: M, JavaScript vs Python (direct formula) | 0.0e+00 | 1.0e-12 | PASS |
| 4-point bending at x = 0.05 m: V/P (absolute) | 0.0e+00 | 1.0e-12 | PASS |
| 4-point bending at x = 0.2 m: M, JavaScript vs Python (direct formula) | 0.0e+00 | 1.0e-12 | PASS |
| 4-point bending at x = 0.2 m: V/P (absolute) | 0.0e+00 | 1.0e-12 | PASS |
| 4-point bending at x = 0.3 m: M, JavaScript vs Python (direct formula) | 1.1e-16 | 1.0e-12 | PASS |
| 4-point bending at x = 0.3 m: V/P (absolute) | 0.0e+00 | 1.0e-12 | PASS |
| 4-point bending at x = 0.45 m: M, JavaScript vs Python (direct formula) | 1.5e-16 | 1.0e-12 | PASS |
| 4-point bending at x = 0.45 m: V/P (absolute) | 0.0e+00 | 1.0e-12 | PASS |
| 4-point bending at x = 0.55 m: M, JavaScript vs Python (direct formula) | 9.1e-16 | 1.0e-12 | PASS |
| 4-point bending at x = 0.55 m: V/P (absolute) | 0.0e+00 | 1.0e-12 | PASS |
| cantilever, triangular load, x = 0.1 m: M, JavaScript vs scipy.quad (right free body) | 1.2e-16 | 1.0e-11 | PASS |
| cantilever, triangular load, x = 0.1 m: V | 0.0e+00 | 1.0e-11 | PASS |
| cantilever, triangular load, x = 0.5 m: M, JavaScript vs scipy.quad (right free body) | 1.8e-16 | 1.0e-11 | PASS |
| cantilever, triangular load, x = 0.5 m: V | 0.0e+00 | 1.0e-11 | PASS |
| cantilever, triangular load, x = 1 m: M, JavaScript vs scipy.quad (right free body) | 0.0e+00 | 1.0e-11 | PASS |
| cantilever, triangular load, x = 1 m: V | 2.0e-16 | 1.0e-11 | PASS |
| cantilever, triangular load, x = 1.5 m: M, JavaScript vs scipy.quad (right free body) | 0.0e+00 | 1.0e-11 | PASS |
| cantilever, triangular load, x = 1.5 m: V | 1.7e-16 | 1.0e-11 | PASS |
| cantilever, triangular load, x = 1.9 m: M, JavaScript vs scipy.quad (right free body) | 2.9e-14 | 1.0e-11 | PASS |
| cantilever, triangular load, x = 1.9 m: V | 9.7e-16 | 1.0e-11 | PASS |
| rectangle (own law), κ = 0.05: strip summation (N = 2000) vs scipy.quad + brentq | 2.5e-07 | 2.0e-06 | PASS |
| rectangle (own law), κ = 0.2: strip summation (N = 2000) vs scipy.quad + brentq | 1.3e-07 | 2.0e-06 | PASS |
| rectangle (own law), κ = 0.4: strip summation (N = 2000) vs scipy.quad + brentq | 1.0e-07 | 2.0e-06 | PASS |
| rectangle (epp law), κ = 0.05: strip summation (N = 2000) vs scipy.quad + brentq | 2.5e-07 | 2.0e-06 | PASS |
| … vs Python §4.6 formula | 2.5e-07 | 2.0e-06 | PASS |
| rectangle (epp law), κ = 0.2: strip summation (N = 2000) vs scipy.quad + brentq | 1.7e-07 | 2.0e-06 | PASS |
| rectangle (epp law), κ = 0.4: strip summation (N = 2000) vs scipy.quad + brentq | 6.1e-09 | 2.0e-06 | PASS |
| composite (elastic), κ = 0.02: M, strip vs quad | 2.1e-07 | 2.0e-06 | PASS |
| composite (elastic), κ = 0.02: neutral axis, strip vs brentq | 2.9e-16 | 1.0e-09 | PASS |
| composite (own curves, both yielding), κ = 0.4: M, strip vs quad | 9.8e-08 | 2.0e-05 | PASS |
| composite (own curves), κ = 0.4: neutral axis | 9.0e-10 | 2.0e-05 | PASS |
| composite (elastic), κ = 0.05: M, strip vs quad | 2.1e-07 | 2.0e-06 | PASS |
| composite (elastic), κ = 0.05: neutral axis, strip vs brentq | 2.9e-16 | 1.0e-09 | PASS |
| composite (own curves, both yielding), κ = 1: M, strip vs quad | 9.3e-08 | 2.0e-05 | PASS |
| composite (own curves), κ = 1: neutral axis | 2.2e-09 | 2.0e-05 | PASS |
| I-section (1018 curve), κ = 0.01: strip vs quad | 1.2e-07 | 2.0e-05 | PASS |
| I-section (1018 curve), κ = 0.03: strip vs quad | 4.1e-08 | 2.0e-05 | PASS |
| composite: transformed centroid, JavaScript vs Python | 0.0e+00 | 1.0e-12 | PASS |
| composite: transformed I, JavaScript vs Python | 0.0e+00 | 1.0e-12 | PASS |
| I-section: I, JavaScript vs Python | 4.8e-16 | 1.0e-12 | PASS |
| I-section: Z, JavaScript (equal-area routine) vs Python (formula) | 2.3e-16 | 1.0e-12 | PASS |

Overall: **PASS**

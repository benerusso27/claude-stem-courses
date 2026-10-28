# Verification record — lab07_deflection

Run with `python3 shared/verify_lab.py lab07_deflection` on 2026-10-27. Detailed tables are in the `results_*.md` files next to this one.

| Step | Result | Detail | Record |
|---|---|---|---|
| Build simulation page | PASS |  |  |
| Model tests: closed form vs independent numerics (Node, exact page code) | PASS | 212 of 212 passed | `results_node.md` |
| Independent re-implementation (Python/scipy) and data-pipeline closure | PASS | 288 of 288 passed | `results_python.md` |
| Handout re-solved from scratch vs instructor key | PASS | 35 of 35 agree | `results_from_scratch.md` |
| Cross-file consistency (units, symbols, sign convention, references) | PASS | 101 of 101 passed | `results_consistency.md` |
| Browser check, 375/1280 px, light/dark, every control | PASS | PASS | `results_browser.md` |

## Formula vs. independent numerical method (worst case over all material presets)

| Comparison | Worst relative difference | Tolerance | Result |
|---|---:|---:|---|
| App. F 1: y_max = −PL³/3EI | 0.0e+00 | 1.0e-13 | PASS |
| App. F 1: slope at the end = −PL²/2EI | 0.0e+00 | 1.0e-13 | PASS |
| App. F 1: elastic curve y = P(x³ − 3Lx²)/6EI at x = 0.4L | 1.7e-16 | 1.0e-13 | PASS |
| App. F 2: y_max = −wL⁴/8EI | 0.0e+00 | 1.0e-13 | PASS |
| App. F 2: slope at the end = −wL³/6EI | 0.0e+00 | 1.0e-13 | PASS |
| App. F 3: y_max = −ML²/2EI (clockwise end couple) | 0.0e+00 | 1.0e-13 | PASS |
| App. F 3: slope at the end = −ML/EI | 0.0e+00 | 1.0e-13 | PASS |
| App. F 4: y_max = −PL³/48EI | 1.3e-16 | 1.0e-13 | PASS |
| App. F 4: slope at A = −PL²/16EI | 1.3e-16 | 1.0e-13 | PASS |
| App. F 5: y_max = −Pb(L² − b²)^{3/2}/(9√3 EIL) at x_m = √((L² − b²)/3) | 0.0e+00 | 1.0e-12 | PASS |
| App. F 5: slope is zero at x_m (absolute difference) | 0.0e+00 | 1.0e-13 | PASS |
| App. F 5: θ_A = −Pb(L² − b²)/6EIL | 0.0e+00 | 1.0e-13 | PASS |
| App. F 5: θ_B = +Pa(L² − a²)/6EIL | 0.0e+00 | 1.0e-13 | PASS |
| App. F 5: y under the load = −Pa²b²/3EIL | 0.0e+00 | 1.0e-13 | PASS |
| App. F 6: y_max = −5wL⁴/384EI | 0.0e+00 | 1.0e-13 | PASS |
| App. F 6: slope at A = −wL³/24EI | 0.0e+00 | 1.0e-13 | PASS |
| App. F 7: y_max = ML²/(9√3 EI) at x = L/√3 (bows upward) | 2.1e-16 | 1.0e-12 | PASS |
| App. F 7: θ_A = +ML/6EI | 0.0e+00 | 1.0e-13 | PASS |
| App. F 7: θ_B = −ML/3EI | 0.0e+00 | 1.0e-13 | PASS |
| fixed at both ends, uniform load: y_max = −wL⁴/384EI | 8.6e-12 | 1.0e-11 | PASS |
| fixed at both ends: end moments wL²/12 | 3.0e-12 | 1.0e-11 | PASS |
| fixed at both ends, central load: y_max = −PL³/192EI | 3.6e-12 | 1.0e-11 | PASS |
| propped cantilever, central load, rigid clamp: R_B = 5P/16 (§9.2) | 4.4e-16 | 1.0e-12 | PASS |
| propped cantilever: wall moment 3PL/16 | 6.9e-16 | 1.0e-12 | PASS |
| propped cantilever, uniform load: R_B = 3wL/8 | 1.7e-14 | 1.0e-12 | PASS |
| propped cantilever with k → 0 becomes a simple span: R_B → P/2 | 7.9e-10 | 1.0e-6 | PASS |
| settlement Δ of the prop changes R_B by 3EIΔ/L³ (rigid clamp) | 5.7e-16 | 1.0e-10 | PASS |
| settlement with a flexible clamp: ΔR_B = Δ/(L³/3EI + L²/k) | 1.3e-16 | 1.0e-10 | PASS |
| cantilever with a flexible clamp: tip deflection PL³/3EI + PL²/k | 0.0e+00 | 1.0e-12 | PASS |
| elastic curve: FE vs closed form, max \|Δy\|/\|y\|max (absolute difference) | 1.2e-08 | 1.0e-7 | PASS |
| slope: FE vs closed form, max \|Δθ\|/\|θ\|max (absolute difference) | 1.2e-08 | 1.0e-7 | PASS |
| reaction at the left support: FE vs closed form (relative to the total load) (absolute difference) | 3.0e-08 | 1.0e-7 | PASS |
| reaction at the right support (absolute difference) | 7.9e-10 | 1.0e-7 | PASS |
| FE reactions satisfy ΣF = 0 and ΣM = 0 (relative) (absolute difference) | 3.4e-08 | 1.0e-7 | PASS |
| reaction couple at the left: FE vs closed form (relative to W·L) (absolute difference) | 1.6e-08 | 1.0e-7 | PASS |
| superposition: FE(both loads) − FE(load 1) − FE(load 2) at 400 mm (relative) (absolute difference) | 2.5e-14 | 1.0e-9 | PASS |
| Maxwell reciprocity: y at 200 mm under 10 N at 600 = y at 600 under 10 N at 200 (FE) | 1.1e-12 | 1.0e-8 | PASS |
| uniform load: FE deflection between nodes converges as N⁻⁴ (observed 4.000) | 0.0e+00 | 0.0e+0 | PASS |
| uniform load: FE moment EI·y″ converges as N⁻² (observed 2.000) | 0.0e+00 | 0.0e+0 | PASS |
| uniform load, 2 elements: nodal deflection already exact (superconvergence) | 2.3e-16 | 1.0e-8 | PASS |
| point load: FE exact at every mesh (largest error 2.2e-9) | 0.0e+00 | 0.0e+0 | PASS |
| C++ reference [partA]: same mesh (61 nodes) | 0.0e+00 | 0.0e+0 | PASS |
| C++ reference [partA]: nodal deflections, JS port vs C++ (max \|Δ\|/\|y\|max) (absolute difference) | 0.0e+00 | 1.0e-9 | PASS |
| C++ reference [partA]: nodal slopes, JS port vs C++ (absolute difference) | 0.0e+00 | 1.0e-9 | PASS |
| C++ reference [partA]: reactions (force and couple), JS port vs C++ (absolute difference) | 0.0e+00 | 1.0e-9 | PASS |
| C++ reference [partAboth]: same mesh (61 nodes) | 0.0e+00 | 0.0e+0 | PASS |
| C++ reference [partAboth]: nodal deflections, JS port vs C++ (max \|Δ\|/\|y\|max) (absolute difference) | 0.0e+00 | 1.0e-9 | PASS |
| C++ reference [partAboth]: nodal slopes, JS port vs C++ (absolute difference) | 0.0e+00 | 1.0e-9 | PASS |
| C++ reference [partAboth]: reactions (force and couple), JS port vs C++ (absolute difference) | 0.0e+00 | 1.0e-9 | PASS |
| C++ reference [partB2]: same mesh (61 nodes) | 0.0e+00 | 0.0e+0 | PASS |
| C++ reference [partB2]: nodal deflections, JS port vs C++ (max \|Δ\|/\|y\|max) (absolute difference) | 0.0e+00 | 1.0e-9 | PASS |
| C++ reference [partB2]: nodal slopes, JS port vs C++ (absolute difference) | 0.0e+00 | 1.0e-9 | PASS |
| C++ reference [partB2]: reactions (force and couple), JS port vs C++ (absolute difference) | 0.0e+00 | 1.0e-9 | PASS |
| C++ reference [design]: same mesh (62 nodes) | 0.0e+00 | 0.0e+0 | PASS |
| C++ reference [design]: nodal deflections, JS port vs C++ (max \|Δ\|/\|y\|max) (absolute difference) | 0.0e+00 | 1.0e-9 | PASS |
| C++ reference [design]: nodal slopes, JS port vs C++ (absolute difference) | 0.0e+00 | 1.0e-9 | PASS |
| C++ reference [design]: reactions (force and couple), JS port vs C++ (absolute difference) | 0.0e+00 | 1.0e-9 | PASS |
| C++ reference [F2]: same mesh (61 nodes) | 0.0e+00 | 0.0e+0 | PASS |
| C++ reference [F2]: nodal deflections, JS port vs C++ (max \|Δ\|/\|y\|max) (absolute difference) | 0.0e+00 | 1.0e-9 | PASS |
| C++ reference [F2]: nodal slopes, JS port vs C++ (absolute difference) | 0.0e+00 | 1.0e-9 | PASS |
| C++ reference [F2]: reactions (force and couple), JS port vs C++ (absolute difference) | 0.0e+00 | 1.0e-9 | PASS |
| C++ reference [F3]: same mesh (61 nodes) | 0.0e+00 | 0.0e+0 | PASS |
| C++ reference [F3]: nodal deflections, JS port vs C++ (max \|Δ\|/\|y\|max) (absolute difference) | 0.0e+00 | 1.0e-9 | PASS |
| C++ reference [F3]: nodal slopes, JS port vs C++ (absolute difference) | 0.0e+00 | 1.0e-9 | PASS |
| C++ reference [F3]: reactions (force and couple), JS port vs C++ (absolute difference) | 0.0e+00 | 1.0e-9 | PASS |
| C++ reference [F5]: same mesh (61 nodes) | 0.0e+00 | 0.0e+0 | PASS |
| C++ reference [F5]: nodal deflections, JS port vs C++ (max \|Δ\|/\|y\|max) (absolute difference) | 0.0e+00 | 1.0e-9 | PASS |
| C++ reference [F5]: nodal slopes, JS port vs C++ (absolute difference) | 0.0e+00 | 1.0e-9 | PASS |
| C++ reference [F5]: reactions (force and couple), JS port vs C++ (absolute difference) | 0.0e+00 | 1.0e-9 | PASS |
| C++ reference [F7]: same mesh (61 nodes) | 0.0e+00 | 0.0e+0 | PASS |
| C++ reference [F7]: nodal deflections, JS port vs C++ (max \|Δ\|/\|y\|max) (absolute difference) | 0.0e+00 | 1.0e-9 | PASS |
| C++ reference [F7]: nodal slopes, JS port vs C++ (absolute difference) | 0.0e+00 | 1.0e-9 | PASS |
| C++ reference [F7]: reactions (force and couple), JS port vs C++ (absolute difference) | 0.0e+00 | 1.0e-9 | PASS |
| C++ reference [fixedw]: same mesh (61 nodes) | 0.0e+00 | 0.0e+0 | PASS |
| C++ reference [fixedw]: nodal deflections, JS port vs C++ (max \|Δ\|/\|y\|max) (absolute difference) | 0.0e+00 | 1.0e-9 | PASS |
| C++ reference [fixedw]: nodal slopes, JS port vs C++ (absolute difference) | 0.0e+00 | 1.0e-9 | PASS |
| C++ reference [fixedw]: reactions (force and couple), JS port vs C++ (absolute difference) | 0.0e+00 | 1.0e-9 | PASS |
| C++ reference [triangle]: same mesh (61 nodes) | 0.0e+00 | 0.0e+0 | PASS |
| C++ reference [triangle]: nodal deflections, JS port vs C++ (max \|Δ\|/\|y\|max) (absolute difference) | 0.0e+00 | 1.0e-9 | PASS |
| C++ reference [triangle]: nodal slopes, JS port vs C++ (absolute difference) | 0.0e+00 | 1.0e-9 | PASS |
| C++ reference [triangle]: reactions (force and couple), JS port vs C++ (absolute difference) | 0.0e+00 | 1.0e-9 | PASS |
| C++ reference: all beams compared | 0.0e+00 | 0.0e+0 | PASS |
| Carlson R_F: K(m = 0.5) = 1.8540746773013719 | 1.2e-16 | 1.0e-13 | PASS |
| Carlson R_D: E(m = 0.5) = 1.3506438810476755 | 0.0e+00 | 1.0e-13 | PASS |
| incomplete F(π/4, m = 0.3) = 0.80436 (series check) | 1.5e-11 | 1.0e-8 | PASS |
| elastica α = 0.05: tip deflection, closed form vs RK4 shooting (N = 400) | 4.3e-13 | 1.0e-9 | PASS |
| elastica α = 0.05: tip angle | 2.2e-14 | 1.0e-9 | PASS |
| elastica α = 0.05: tip x-position | 1.2e-14 | 1.0e-9 | PASS |
| elastica α = 0.05: closed-form shape ends at the closed-form tip | 4.1e-13 | 1.0e-12 | PASS |
| elastica α = 0.05: arc length of the closed-form shape = L | 6.9e-15 | 1.0e-12 | PASS |
| elastica α = 0.5: tip deflection, closed form vs RK4 shooting (N = 400) | 3.2e-14 | 1.0e-9 | PASS |
| elastica α = 0.5: tip angle | 2.2e-14 | 1.0e-9 | PASS |
| elastica α = 0.5: tip x-position | 6.3e-14 | 1.0e-9 | PASS |
| elastica α = 0.5: closed-form shape ends at the closed-form tip | 2.7e-15 | 1.0e-12 | PASS |
| elastica α = 0.5: arc length of the closed-form shape = L | 4.4e-16 | 1.0e-12 | PASS |
| elastica α = 1: tip deflection, closed form vs RK4 shooting (N = 400) | 9.3e-14 | 1.0e-9 | PASS |
| elastica α = 1: tip angle | 1.2e-13 | 1.0e-9 | PASS |
| elastica α = 1: tip x-position | 2.6e-13 | 1.0e-9 | PASS |
| elastica α = 1: closed-form shape ends at the closed-form tip | 7.4e-16 | 1.0e-12 | PASS |
| elastica α = 1: arc length of the closed-form shape = L | 2.2e-16 | 1.0e-12 | PASS |
| elastica α = 2: tip deflection, closed form vs RK4 shooting (N = 400) | 8.9e-14 | 1.0e-9 | PASS |
| elastica α = 2: tip angle | 6.3e-13 | 1.0e-9 | PASS |
| elastica α = 2: tip x-position | 1.1e-12 | 1.0e-9 | PASS |
| elastica α = 2: closed-form shape ends at the closed-form tip | 6.8e-16 | 1.0e-12 | PASS |
| elastica α = 2: arc length of the closed-form shape = L | 3.3e-16 | 1.0e-12 | PASS |
| elastica α = 3: tip deflection, closed form vs RK4 shooting (N = 400) | 6.5e-14 | 1.0e-9 | PASS |
| elastica α = 3: tip angle | 1.4e-12 | 1.0e-9 | PASS |
| elastica α = 3: tip x-position | 2.4e-12 | 1.0e-9 | PASS |
| elastica α = 3: closed-form shape ends at the closed-form tip | 0.0e+00 | 1.0e-12 | PASS |
| elastica α = 3: arc length of the closed-form shape = L | 0.0e+00 | 1.0e-12 | PASS |
| elastica α = 5: tip deflection, closed form vs RK4 shooting (N = 400) | 4.4e-13 | 1.0e-9 | PASS |
| elastica α = 5: tip angle | 3.3e-12 | 1.0e-9 | PASS |
| elastica α = 5: tip x-position | 6.1e-12 | 1.0e-9 | PASS |
| elastica α = 5: closed-form shape ends at the closed-form tip | 4.7e-16 | 1.0e-12 | PASS |
| elastica α = 5: arc length of the closed-form shape = L | 4.4e-16 | 1.0e-12 | PASS |
| elastica, small load: δ_v/L → α/3 (α = 0.001) | 1.1e-07 | 1.0e-6 | PASS |
| elastica, small load: tip angle → α/2 | 9.2e-08 | 1.0e-6 | PASS |
| linear theory is 5 % high at α = 0.67564 (bisection) | 3.1e-14 | 1.0e-9 | PASS |
| RK4 shooting converges as N⁻⁴ (observed 3.945) | 0.0e+00 | 0.0e+0 | PASS |
| self-weight only, small: tip deflection → βL/8 | 1.3e-06 | 2.0e-3 | PASS |
| Part C preset reaches α = 3.63 > 3 | 0.0e+00 | 0.0e+0 | PASS |
| closed form y(x), JS vs Python, max \|Δ\|/\|y\|max (absolute) | 5.1e-11 | 1.0e-09 | PASS |
| closed form slope, JS vs Python, max \|Δ\|/\|θ\|max (absolute) | 2.0e-11 | 1.0e-09 | PASS |
| closed form y(x) (JS) vs double integration of M/EI (Python), max \|Δ\|/\|y\|max (absolute) | 4.6e-09 | 1.0e-07 | PASS |
| finite elements y(x) (JS port of the C++) vs double integration (Python), max \|Δ\|/\|y\|max (absolute) | 1.3e-08 | 1.0e-06 | PASS |
| finite elements slope vs double integration, max \|Δ\|/\|θ\|max (absolute) | 1.3e-08 | 1.0e-05 | PASS |
| reaction RA, JS vs Python closed form (relative to the largest reaction) (absolute) | 2.7e-12 | 1.0e-09 | PASS |
| reaction RB, JS vs Python closed form (relative to the largest reaction) (absolute) | 2.7e-12 | 1.0e-09 | PASS |
| finite-element reactions (Ku − F) vs double-integration reactions, worst relative to the largest (absolute) | 8.6e-09 | 1.0e-06 | PASS |
| M(x) from statics with the JS reactions vs Python, max \|Δ\|/\|M\|max (absolute) | 3.0e-10 | 1.0e-06 | PASS |
| reaction MA, JS vs Python closed form (relative to the largest reaction) (absolute) | 1.7e-12 | 1.0e-09 | PASS |
| reaction MB, JS vs Python closed form (relative to the largest reaction) (absolute) | 6.5e-12 | 1.0e-09 | PASS |
| elastica α = 0.05: tip angle, Carlson R_F (JS) vs scipy ellipkinc + brentq | 1.8e-14 | 1.0e-10 | PASS |
| elastica α = 0.05: δ_v/L, Carlson R_D (JS) vs scipy ellipeinc | 4.8e-13 | 1.0e-10 | PASS |
| elastica α = 0.05: x_tip/L, JS vs scipy | 8.9e-15 | 1.0e-10 | PASS |
| elastica α = 0.05: δ_v/L, RK4 shooting N = 400 (JS) vs collocation BVP (scipy) | 6.2e-16 | 1.0e-08 | PASS |
| elastica α = 0.05: x_tip/L, RK4 shooting vs BVP | 7.8e-16 | 1.0e-08 | PASS |
| elastica α = 0.05 with self-weight β = 0.1154: δ_v/L, RK4 shooting vs BVP | 1.3e-14 | 1.0e-07 | PASS |
| elastica α = 0.05 with self-weight: tip angle, RK4 shooting vs BVP | 8.5e-15 | 1.0e-07 | PASS |
| elastica α = 0.3: tip angle, Carlson R_F (JS) vs scipy ellipkinc + brentq | 7.5e-16 | 1.0e-10 | PASS |
| elastica α = 0.3: δ_v/L, Carlson R_D (JS) vs scipy ellipeinc | 1.7e-14 | 1.0e-10 | PASS |
| elastica α = 0.3: x_tip/L, JS vs scipy | 3.4e-16 | 1.0e-10 | PASS |
| elastica α = 0.3: δ_v/L, RK4 shooting N = 400 (JS) vs collocation BVP (scipy) | 1.3e-14 | 1.0e-08 | PASS |
| elastica α = 0.3: x_tip/L, RK4 shooting vs BVP | 2.3e-14 | 1.0e-08 | PASS |
| elastica α = 0.3 with self-weight β = 0.1154: δ_v/L, RK4 shooting vs BVP | 2.0e-14 | 1.0e-07 | PASS |
| elastica α = 0.3 with self-weight: tip angle, RK4 shooting vs BVP | 3.7e-14 | 1.0e-07 | PASS |
| elastica α = 1: tip angle, Carlson R_F (JS) vs scipy ellipkinc + brentq | 9.6e-16 | 1.0e-10 | PASS |
| elastica α = 1: δ_v/L, Carlson R_D (JS) vs scipy ellipeinc | 1.5e-15 | 1.0e-10 | PASS |
| elastica α = 1: x_tip/L, JS vs scipy | 3.5e-16 | 1.0e-10 | PASS |
| elastica α = 1: δ_v/L, RK4 shooting N = 400 (JS) vs collocation BVP (scipy) | 8.4e-14 | 1.0e-08 | PASS |
| elastica α = 1: x_tip/L, RK4 shooting vs BVP | 2.4e-13 | 1.0e-08 | PASS |
| elastica α = 1 with self-weight β = 0.1154: δ_v/L, RK4 shooting vs BVP | 7.6e-14 | 1.0e-07 | PASS |
| elastica α = 1 with self-weight: tip angle, RK4 shooting vs BVP | 1.5e-13 | 1.0e-07 | PASS |
| elastica α = 2: tip angle, Carlson R_F (JS) vs scipy ellipkinc + brentq | 4.3e-16 | 1.0e-10 | PASS |
| elastica α = 2: δ_v/L, Carlson R_D (JS) vs scipy ellipeinc | 2.3e-16 | 1.0e-10 | PASS |
| elastica α = 2: x_tip/L, JS vs scipy | 1.3e-16 | 1.0e-10 | PASS |
| elastica α = 2: δ_v/L, RK4 shooting N = 400 (JS) vs collocation BVP (scipy) | 7.3e-14 | 1.0e-08 | PASS |
| elastica α = 2: x_tip/L, RK4 shooting vs BVP | 1.1e-12 | 1.0e-08 | PASS |
| elastica α = 2 with self-weight β = 0.1154: δ_v/L, RK4 shooting vs BVP | 5.1e-14 | 1.0e-07 | PASS |
| elastica α = 2 with self-weight: tip angle, RK4 shooting vs BVP | 6.9e-13 | 1.0e-07 | PASS |
| elastica α = 3.641: tip angle, Carlson R_F (JS) vs scipy ellipkinc + brentq | 2.1e-16 | 1.0e-10 | PASS |
| elastica α = 3.641: δ_v/L, Carlson R_D (JS) vs scipy ellipeinc | 3.4e-16 | 1.0e-10 | PASS |
| elastica α = 3.641: x_tip/L, JS vs scipy | 1.6e-16 | 1.0e-10 | PASS |
| elastica α = 3.641: δ_v/L, RK4 shooting N = 400 (JS) vs collocation BVP (scipy) | 1.8e-13 | 1.0e-08 | PASS |
| elastica α = 3.641: x_tip/L, RK4 shooting vs BVP | 3.4e-12 | 1.0e-08 | PASS |
| elastica α = 3.641 with self-weight β = 0.1154: δ_v/L, RK4 shooting vs BVP | 2.1e-13 | 1.0e-07 | PASS |
| elastica α = 3.641 with self-weight: tip angle, RK4 shooting vs BVP | 2.1e-12 | 1.0e-07 | PASS |
| elastica α = 5: tip angle, Carlson R_F (JS) vs scipy ellipkinc + brentq | 3.7e-16 | 1.0e-10 | PASS |
| elastica α = 5: δ_v/L, Carlson R_D (JS) vs scipy ellipeinc | 1.2e-15 | 1.0e-10 | PASS |
| elastica α = 5: x_tip/L, JS vs scipy | 0.0e+00 | 1.0e-10 | PASS |
| elastica α = 5: δ_v/L, RK4 shooting N = 400 (JS) vs collocation BVP (scipy) | 4.3e-13 | 1.0e-08 | PASS |
| elastica α = 5: x_tip/L, RK4 shooting vs BVP | 6.1e-12 | 1.0e-08 | PASS |
| elastica α = 5 with self-weight β = 0.1154: δ_v/L, RK4 shooting vs BVP | 4.6e-13 | 1.0e-07 | PASS |
| elastica α = 5 with self-weight: tip angle, RK4 shooting vs BVP | 3.4e-12 | 1.0e-07 | PASS |
| elastica α = 1: elastic curve from the elliptic parameterization (JS) vs the BVP at the same arc length, max distance / L (absolute) | 6.3e-14 | 1.0e-07 | PASS |
| elastica α = 3.641: elastic curve from the elliptic parameterization (JS) vs the BVP at the same arc length, max distance / L (absolute) | 3.0e-14 | 1.0e-07 | PASS |
| α at which linear theory overstates δ_v by 5 %: JS bisection vs scipy brentq | 3.1e-14 | 1.0e-09 | PASS |
| handout Appendix E, 11 rows: every printed value vs scipy (largest error in the last printed digit) (absolute) | 4.7e-05 | 5.0e-05 | PASS |
| analysis α5 (scipy) vs the page's alpha5 (JS) | 3.1e-14 | 1.0e-09 | PASS |
| simulation Part C preset: β = wL³/EI with E = 203 GPa vs the analysis β | 5.2e-03 | 1.0e-02 | PASS |
| D1 reference design (I 102 × 64, L_s = 3.05 m): largest \|y\| on the span, page vs analysis (40 points vs 8000) | 1.5e-04 | 2.0e-03 | PASS |
| D1 reference design: tip deflection, page vs analysis | 6.5e-15 | 1.0e-09 | PASS |
| D1 reference design: roller reaction, page vs analysis | 0.0e+00 | 1.0e-12 | PASS |
| D1: the lightest feasible section is I 102 × 64; without an overhang it is I 152 × 102 | 0.0e+00 | 0.0e+00 | PASS |

Overall: **PASS**

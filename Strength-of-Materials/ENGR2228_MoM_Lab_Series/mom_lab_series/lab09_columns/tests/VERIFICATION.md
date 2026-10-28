# Verification record — lab09_columns

Run with `python3 shared/verify_lab.py lab09_columns` on 2026-10-26. Detailed tables are in the `results_*.md` files next to this one.

| Step | Result | Detail | Record |
|---|---|---|---|
| Build simulation page | PASS |  |  |
| Model tests: closed form vs independent numerics (Node, exact page code) | PASS | 154 of 154 passed | `results_node.md` |
| Independent re-implementation (Python/scipy) and data-pipeline closure | PASS | 97 of 97 passed | `results_python.md` |
| Handout re-solved from scratch vs instructor key | PASS | 200 of 200 agree | `results_from_scratch.md` |
| Cross-file consistency (units, symbols, sign convention, references) | PASS | 145 of 145 passed | `results_consistency.md` |
| Browser check, 375/1280 px, light/dark, every control | PASS | PASS | `results_browser.md` |

## Formula vs. independent numerical method (worst case over all material presets)

| Comparison | Worst relative difference | Tolerance | Result |
|---|---:|---:|---|
| rectangle: I = bt³/12 vs midpoint integration of z² b dz | 6.2e-08 | 1.0e-7 | PASS |
| tube: A = π(Do² − Di²)/4 vs polar integration | 5.1e-16 | 1.0e-7 | PASS |
| tube: I = π(Do⁴ − Di⁴)/64 vs polar integration of r² sin²θ | 4.5e-11 | 1.0e-7 | PASS |
| solid round: r = d/4 | 0.0e+00 | 1.0e-15 | PASS |
| Beer Eq. 10.20: tan z = z at z = 4.4934 | 2.0e-16 | 1.0e-13 | PASS |
| Beer Eq. 10.21: P_cr = 20.19 EI/L² for a fixed-pinned column (z² = 20.19) | 3.6e-05 | 2.0e-4 | PASS |
| Beer Fig. 10.18: K = π/4.4934 = 0.699 for fixed-pinned | 2.2e-04 | 3.0e-4 | PASS |
| pinned, L = 0.3 m: Euler with K = 1.0000 vs finite elements (N = 64) | 8.1e-09 | 2.0e-7 | PASS |
| pinned, L = 0.6005 m: Euler with K = 1.0000 vs finite elements (N = 64) | 8.1e-09 | 2.0e-7 | PASS |
| pinned, L = 1.7 m: Euler with K = 1.0000 vs finite elements (N = 64) | 8.1e-09 | 2.0e-7 | PASS |
| fixed-pinned, L = 0.3 m: Euler with K = 0.6992 vs finite elements (N = 64) | 3.4e-08 | 2.0e-7 | PASS |
| fixed-pinned, L = 0.6005 m: Euler with K = 0.6992 vs finite elements (N = 64) | 3.4e-08 | 2.0e-7 | PASS |
| fixed-pinned, L = 1.7 m: Euler with K = 0.6992 vs finite elements (N = 64) | 3.4e-08 | 2.0e-7 | PASS |
| fixed-fixed, L = 0.3 m: Euler with K = 0.5000 vs finite elements (N = 64) | 1.3e-07 | 2.0e-7 | PASS |
| fixed-fixed, L = 0.6005 m: Euler with K = 0.5000 vs finite elements (N = 64) | 1.3e-07 | 2.0e-7 | PASS |
| fixed-fixed, L = 1.7 m: Euler with K = 0.5000 vs finite elements (N = 64) | 1.3e-07 | 2.0e-7 | PASS |
| free-fixed, L = 0.3 m: Euler with K = 2.0000 vs finite elements (N = 64) | 5.1e-10 | 2.0e-7 | PASS |
| free-fixed, L = 0.6005 m: Euler with K = 2.0000 vs finite elements (N = 64) | 5.0e-10 | 2.0e-7 | PASS |
| free-fixed, L = 1.7 m: Euler with K = 2.0000 vs finite elements (N = 64) | 5.0e-10 | 2.0e-7 | PASS |
| springs, k = 5 N·m/rad: characteristic equation vs finite elements (N = 64) | 8.3e-09 | 2.0e-7 | PASS |
| spring-pin, k = 5 N·m/rad: characteristic equation vs finite elements (N = 64) | 8.2e-09 | 2.0e-7 | PASS |
| springs, k = 300 N·m/rad: characteristic equation vs finite elements (N = 64) | 2.7e-08 | 2.0e-7 | PASS |
| spring-pin, k = 300 N·m/rad: characteristic equation vs finite elements (N = 64) | 1.6e-08 | 2.0e-7 | PASS |
| springs, k = 2800 N·m/rad: characteristic equation vs finite elements (N = 64) | 9.9e-08 | 2.0e-7 | PASS |
| spring-pin, k = 2800 N·m/rad: characteristic equation vs finite elements (N = 64) | 3.0e-08 | 2.0e-7 | PASS |
| springs, k = 100000 N·m/rad: characteristic equation vs finite elements (N = 64) | 1.3e-07 | 2.0e-7 | PASS |
| spring-pin, k = 100000 N·m/rad: characteristic equation vs finite elements (N = 64) | 3.4e-08 | 2.0e-7 | PASS |
| springs, k = 100000000 N·m/rad: characteristic equation vs finite elements (N = 64) | 1.3e-07 | 2.0e-7 | PASS |
| spring-pin, k = 100000000 N·m/rad: characteristic equation vs finite elements (N = 64) | 3.4e-08 | 2.0e-7 | PASS |
| spring ends: residual of tan x + 2x EI/(kL) at the root (absolute difference) | 2.8e-16 | 1.0e-12 | PASS |
| spring + pin: residual of tan z − z/(1 + z² EI/(kL)) at the root (absolute difference) | 1.4e-14 | 1.0e-11 | PASS |
| spring ends: k → 0 gives the pinned load | 6.5e-12 | 1.0e-9 | PASS |
| spring ends: k = 10¹⁴ N·m/rad gives the fixed-fixed load | 2.5e-12 | 1.0e-9 | PASS |
| spring + pin: k = 10¹⁴ gives Beer Eq. 10.21 | 1.2e-12 | 1.0e-9 | PASS |
| k from P (inverse of the symmetric characteristic equation) | 2.0e-15 | 1.0e-10 | PASS |
| kL/EI = 1 already gives K = 0.855 (between 0.5 and 1) | 0.0e+00 | 0.0e+0 | PASS |
| pinned: closed-form mode shape vs finite-element eigenvector (least-squares scaled), max difference (absolute difference) | 1.6e-10 | 1.0e-5 | PASS |
| fixed-fixed: closed-form mode shape vs finite-element eigenvector (least-squares scaled), max difference (absolute difference) | 8.4e-08 | 1.0e-5 | PASS |
| fixed-pinned: closed-form mode shape vs finite-element eigenvector (least-squares scaled), max difference (absolute difference) | 9.7e-09 | 1.0e-5 | PASS |
| free-fixed: closed-form mode shape vs finite-element eigenvector (least-squares scaled), max difference (absolute difference) | 1.3e-10 | 1.0e-5 | PASS |
| springs: closed-form mode shape vs finite-element eigenvector (least-squares scaled), max difference (absolute difference) | 5.1e-08 | 1.0e-5 | PASS |
| spring-pin: closed-form mode shape vs finite-element eigenvector (least-squares scaled), max difference (absolute difference) | 2.1e-08 | 1.0e-5 | PASS |
| Hermite elements: P_cr error falls as N⁻⁴ (fitted order, N = 4 to 16) | 5.3e-03 | 3.0e-2 | PASS |
| Hermite elements with spring ends: order 4 too (N = 8 to 32) | 5.6e-03 | 3.0e-2 | PASS |
| one fixed-fixed element has no free DOF: P is NaN (the page asks for N ≥ 2) | 0.0e+00 | 0.0e+0 | PASS |
| P = 0.3 P_cr, δ0 = 0.4 mm, e = 0 mm: mid-length deflection, closed form vs finite differences (N = 4000) | 7.3e-08 | 3.0e-6 | PASS |
| P = 0.3 P_cr, δ0 = 0.4 mm, e = 0 mm: mid-length deflection, closed form vs finite elements (N = 64) | 1.2e-08 | 3.0e-7 | PASS |
| P = 0.3 P_cr, δ0 = 0.4 mm, e = 0 mm: curvature at mid-length × EI vs M = −P(e + δ0 + δ) (Beer Eq. 10.22) | 2.0e-04 | 2.0e-3 | PASS |
| P = 0.3 P_cr, δ0 = 0.4 mm, e = 0 mm: at a fixed load the responses to bow and eccentricity superpose (max \|Δ\|, m) (absolute difference) | 0.0e+00 | 1.0e-15 | PASS |
| P = 0.7 P_cr, δ0 = 0.4 mm, e = 1 mm: mid-length deflection, closed form vs finite differences (N = 4000) | 1.3e-07 | 3.0e-6 | PASS |
| P = 0.7 P_cr, δ0 = 0.4 mm, e = 1 mm: mid-length deflection, closed form vs finite elements (N = 64) | 1.6e-08 | 3.0e-7 | PASS |
| P = 0.7 P_cr, δ0 = 0.4 mm, e = 1 mm: curvature at mid-length × EI vs M = −P(e + δ0 + δ) (Beer Eq. 10.22) | 1.6e-04 | 2.0e-3 | PASS |
| P = 0.7 P_cr, δ0 = 0.4 mm, e = 1 mm: at a fixed load the responses to bow and eccentricity superpose (max \|Δ\|, m) (absolute difference) | 0.0e+00 | 1.0e-15 | PASS |
| P = 0.9 P_cr, δ0 = 0 mm, e = 2 mm: mid-length deflection, closed form vs finite differences (N = 4000) | 4.6e-07 | 3.0e-6 | PASS |
| P = 0.9 P_cr, δ0 = 0 mm, e = 2 mm: mid-length deflection, closed form vs finite elements (N = 64) | 6.6e-08 | 3.0e-7 | PASS |
| P = 0.9 P_cr, δ0 = 0 mm, e = 2 mm: curvature at mid-length × EI vs M = −P(e + δ0 + δ) (Beer Eq. 10.22) | 1.8e-04 | 2.0e-3 | PASS |
| P = 0.9 P_cr, δ0 = 0 mm, e = 2 mm: at a fixed load the responses to bow and eccentricity superpose (max \|Δ\|, m) (absolute difference) | 0.0e+00 | 1.0e-15 | PASS |
| P = 0.95 P_cr, δ0 = 0.25999999999999995 mm, e = 0.08 mm: mid-length deflection, closed form vs finite differences (N = 4000) | 1.0e-06 | 3.0e-6 | PASS |
| P = 0.95 P_cr, δ0 = 0.25999999999999995 mm, e = 0.08 mm: mid-length deflection, closed form vs finite elements (N = 64) | 1.6e-07 | 3.0e-7 | PASS |
| P = 0.95 P_cr, δ0 = 0.25999999999999995 mm, e = 0.08 mm: curvature at mid-length × EI vs M = −P(e + δ0 + δ) (Beer Eq. 10.22) | 2.0e-04 | 2.0e-3 | PASS |
| P = 0.95 P_cr, δ0 = 0.25999999999999995 mm, e = 0.08 mm: at a fixed load the responses to bow and eccentricity superpose (max \|Δ\|, m) (absolute difference) | 0.0e+00 | 1.0e-15 | PASS |
| Eq. 10.31 equals Eq. 10.26 at x = L/2 (P = 0.2 P_cr) | 0.0e+00 | 1.0e-13 | PASS |
| Eq. 10.31 equals Eq. 10.26 at x = L/2 (P = 0.6 P_cr) | 2.3e-16 | 1.0e-13 | PASS |
| Eq. 10.31 equals Eq. 10.26 at x = L/2 (P = 0.9 P_cr) | 1.5e-16 | 1.0e-13 | PASS |
| Eq. 10.35 equals Eq. 10.33, P/A [1 + (y_max + e)c/r²] (P = 0.2 P_cr) | 0.0e+00 | 1.0e-13 | PASS |
| Eq. 10.35 equals Eq. 10.33, P/A [1 + (y_max + e)c/r²] (P = 0.6 P_cr) | 0.0e+00 | 1.0e-13 | PASS |
| Eq. 10.35 equals Eq. 10.33, P/A [1 + (y_max + e)c/r²] (P = 0.9 P_cr) | 1.2e-16 | 1.0e-13 | PASS |
| superposition fails in P: doubling 0.33 → 0.66 P_cr multiplies y_max by 3.982 (> 2) | 0.0e+00 | 0.0e+0 | PASS |
| first yield, e = 0.5 mm: secant formula Eq. 10.36 vs finite differences (N = 4000) | 4.9e-08 | 2.0e-6 | PASS |
| first yield, e = 0.5 mm: σ_max(P_Y) = σ_Y | 1.9e-12 | 1.0e-10 | PASS |
| first yield, e = 1 mm: secant formula Eq. 10.36 vs finite differences (N = 4000) | 4.6e-08 | 2.0e-6 | PASS |
| first yield, e = 1 mm: σ_max(P_Y) = σ_Y | 9.8e-13 | 1.0e-10 | PASS |
| first yield, e = 2 mm: secant formula Eq. 10.36 vs finite differences (N = 4000) | 4.2e-08 | 2.0e-6 | PASS |
| first yield, e = 2 mm: σ_max(P_Y) = σ_Y | 5.9e-13 | 1.0e-10 | PASS |
| finite differences: error falls as N⁻² (fitted order) | 2.1e-03 | 2.0e-2 | PASS |
| Southwell on an exact half-sine bow recovers P_cr | 1.3e-16 | 1.0e-12 | PASS |
| Southwell on an exact half-sine bow recovers δ0 | 8.2e-16 | 1.0e-10 | PASS |
| Southwell on a pure eccentric load: P_cr within 0.5 % (the secant curve is nearly a Southwell line) | 1.4e-03 | 5.0e-3 | PASS |
| Southwell on a pure eccentric load: the intercept is about (4/π) e | 1.7e-02 | 3.0e-2 | PASS |
| fixed-fixed: Southwell on mid-length readings (half-sine bow, clamps grip the initial slope) vs the eigenvalue | 5.2e-04 | 5.0e-3 | PASS |
| fixed-pinned: Southwell on mid-length readings (half-sine bow, clamps grip the initial slope) vs the eigenvalue | 3.2e-03 | 5.0e-3 | PASS |
| springs: Southwell on mid-length readings (half-sine bow, clamps grip the initial slope) vs the eigenvalue | 3.9e-04 | 5.0e-3 | PASS |
| sample data A300: page Southwell fit vs lab09_analysis.py | 2.2e-16 | 1.0e-9 | PASS |
| sample data A450: page Southwell fit vs lab09_analysis.py | 2.5e-16 | 1.0e-9 | PASS |
| sample data A600: page Southwell fit vs lab09_analysis.py | 0.0e+00 | 1.0e-9 | PASS |
| sample data Bff: page Southwell fit vs lab09_analysis.py | 2.4e-16 | 1.0e-9 | PASS |
| sample data Bfp: page Southwell fit vs lab09_analysis.py | 6.4e-16 | 1.0e-9 | PASS |
| Carlson R_F: K(m = 0.5) = 1.854074677301372 | 2.4e-16 | 1.0e-14 | PASS |
| Carlson R_F: K(0) = π/2 | 0.0e+00 | 1.0e-15 | PASS |
| elastica at 1.005 P_cr: δ/L by elliptic integrals vs RK4 shooting (400 steps) | 3.9e-10 | 2.0e-9 | PASS |
| elastica at 1.005 P_cr: end slope, elliptic vs shooting | 3.9e-10 | 2.0e-9 | PASS |
| elastica at 1.02 P_cr: δ/L by elliptic integrals vs RK4 shooting (400 steps) | 9.6e-11 | 2.0e-9 | PASS |
| elastica at 1.02 P_cr: end slope, elliptic vs shooting | 9.7e-11 | 2.0e-9 | PASS |
| elastica at 1.2 P_cr: δ/L by elliptic integrals vs RK4 shooting (400 steps) | 7.6e-12 | 2.0e-9 | PASS |
| elastica at 1.2 P_cr: end slope, elliptic vs shooting | 9.0e-12 | 2.0e-9 | PASS |
| elastica at 1.5 P_cr: δ/L by elliptic integrals vs RK4 shooting (400 steps) | 2.5e-12 | 2.0e-9 | PASS |
| elastica at 1.5 P_cr: end slope, elliptic vs shooting | 4.4e-12 | 2.0e-9 | PASS |
| elastica at 2.5 P_cr: δ/L by elliptic integrals vs RK4 shooting (400 steps) | 4.3e-13 | 2.0e-9 | PASS |
| elastica at 2.5 P_cr: end slope, elliptic vs shooting | 5.4e-12 | 2.0e-9 | PASS |
| elastica, small deflection: P/P_cr − 1 ≈ (π²/8)(δ/L)² (leading term, at 1.0001 P_cr) | 2.4e-04 | 5.0e-4 | PASS |
| Ramberg–Osgood: stress → strain → stress round trip at 50 MPa | 0.0e+00 | 1.0e-12 | PASS |
| Ramberg–Osgood: stress → strain → stress round trip at 200 MPa | 0.0e+00 | 1.0e-12 | PASS |
| Ramberg–Osgood: stress → strain → stress round trip at 260 MPa | 0.0e+00 | 1.0e-12 | PASS |
| Ramberg–Osgood: stress → strain → stress round trip at 300 MPa | 2.0e-16 | 1.0e-12 | PASS |
| tangent modulus at 100 MPa: formula vs central difference of the curve | 7.9e-12 | 1.0e-7 | PASS |
| tangent modulus at 220 MPa: formula vs central difference of the curve | 1.3e-11 | 1.0e-7 | PASS |
| tangent modulus at 270 MPa: formula vs central difference of the curve | 6.1e-11 | 1.0e-7 | PASS |
| tangent modulus stays finite for a sharp knee (m = 60, steel): no overflow | 0.0e+00 | 0.0e+0 | PASS |
| tangent-modulus column curve at L/r = 35: σ = π²E_t/(L/r)² inverted by the closed form π√(E_t/σ) | 1.6e-14 | 1.0e-10 | PASS |
| L/r = 35: tangent-modulus load vs finite-element eigenvalue with E_t I | 1.3e-07 | 2.0e-6 | PASS |
| L/r = 35: reduced-modulus stress ≥ tangent-modulus stress | 0.0e+00 | 0.0e+0 | PASS |
| tangent-modulus column curve at L/r = 49.1: σ = π²E_t/(L/r)² inverted by the closed form π√(E_t/σ) | 1.2e-15 | 1.0e-10 | PASS |
| L/r = 49.1: tangent-modulus load vs finite-element eigenvalue with E_t I | 1.3e-07 | 2.0e-6 | PASS |
| L/r = 49.1: reduced-modulus stress ≥ tangent-modulus stress | 0.0e+00 | 0.0e+0 | PASS |
| tangent-modulus column curve at L/r = 60: σ = π²E_t/(L/r)² inverted by the closed form π√(E_t/σ) | 5.1e-15 | 1.0e-10 | PASS |
| L/r = 60: tangent-modulus load vs finite-element eigenvalue with E_t I | 1.3e-07 | 2.0e-6 | PASS |
| L/r = 60: reduced-modulus stress ≥ tangent-modulus stress | 0.0e+00 | 0.0e+0 | PASS |
| tangent-modulus column curve at L/r = 80: σ = π²E_t/(L/r)² inverted by the closed form π√(E_t/σ) | 3.2e-15 | 1.0e-10 | PASS |
| L/r = 80: tangent-modulus load vs finite-element eigenvalue with E_t I | 1.3e-07 | 2.0e-6 | PASS |
| L/r = 80: reduced-modulus stress ≥ tangent-modulus stress | 0.0e+00 | 0.0e+0 | PASS |
| tangent-modulus curve joins Euler for slender columns (L/r = 200) | 4.8e-15 | 1.0e-9 | PASS |
| fiber section: Σ dA z² = I (1 − 1/n_f²) for n_f = 8 (midpoint rule) | 0.0e+00 | 1.0e-12 | PASS |
| fiber section: Σ dA z² = I (1 − 1/n_f²) for n_f = 40 (midpoint rule) | 3.8e-16 | 1.0e-12 | PASS |
| fiber section: Σ dA z² = I (1 − 1/n_f²) for n_f = 200 (midpoint rule) | 1.9e-16 | 1.0e-12 | PASS |
| fiber model with an elastic material vs the assumed-mode closed form P = P_cr δ/(δ + δ0 + e), max relative difference (absolute difference) | 2.3e-15 | 1.0e-9 | PASS |
| nearly perfect inelastic column: tangent-modulus load 35.65 kN ≤ fiber maximum 35.98 kN ≤ reduced-modulus load 36.94 kN (Shanley) | 0.0e+00 | 0.0e+0 | PASS |
| Part D: page fiber model (JS) vs the truth model (Python, scipy brentq) with identical inputs, maximum load | 9.4e-16 | 1.0e-7 | PASS |
| AA 6061-T6, L/r = 10: 146.3 MPa (Eq. 10.43b) | 0.0e+00 | 1.0e-12 | PASS |
| AA 6061-T6, L/r = 30: 173.9 − 1.602(30) + 0.00323(30)² MPa (Eq. 10.44b) | 0.0e+00 | 1.0e-12 | PASS |
| AA 6061-T6, L/r = 100: 356 000/100² MPa (Eq. 10.45b) | 0.0e+00 | 1.0e-12 | PASS |
| AA 6061-T6 Euler branch = Euler with E = 68.9 GPa divided by 1.91 | 8.2e-05 | 2.0e-3 | PASS |
| AISC junction (Eq. 10.41): Eqs. 10.38 and 10.40 meet within 0.5 % | 3.8e-04 | 5.0e-3 | PASS |
| AISC: σ_all = σ_cr/1.67 (Eq. 10.42) | 0.0e+00 | 1.0e-14 | PASS |
| preset euler450: finite P_cr (1.821 kN) and K (1.0000) | 0.0e+00 | 0.0e+0 | PASS |
| preset endsFF: finite P_cr (4.091 kN) and K (0.5000) | 0.0e+00 | 0.0e+0 | PASS |
| preset springsB: finite P_cr (3.752 kN) and K (0.5221) | 0.0e+00 | 0.0e+0 | PASS |
| preset flagpole: finite P_cr (23.027 kN) and K (2.0000) | 0.0e+00 | 0.0e+0 | PASS |
| preset partA300: finite P_cr (4.098 kN) and K (1.0000) | 0.0e+00 | 0.0e+0 | PASS |
| preset partA450: finite P_cr (1.821 kN) and K (1.0000) | 0.0e+00 | 0.0e+0 | PASS |
| preset partA600: finite P_cr (1.023 kN) and K (1.0000) | 0.0e+00 | 0.0e+0 | PASS |
| preset partBff: finite P_cr (4.091 kN) and K (0.5000) | 0.0e+00 | 0.0e+0 | PASS |
| preset partBfp: finite P_cr (1.842 kN) and K (0.6992) | 0.0e+00 | 0.0e+0 | PASS |
| preset partC1: finite P_cr (1.821 kN) and K (1.0000) | 0.0e+00 | 0.0e+0 | PASS |
| preset partC2: finite P_cr (1.821 kN) and K (1.0000) | 0.0e+00 | 0.0e+0 | PASS |
| preset partD: finite P_cr (45.535 kN) and K (1.0000) | 0.0e+00 | 0.0e+0 | PASS |
| preset elastica: finite P_cr (1.821 kN) and K (1.0000) | 0.0e+00 | 0.0e+0 | PASS |
| preset steel: finite P_cr (47.584 kN) and K (1.0000) | 0.0e+00 | 0.0e+0 | PASS |
| preset design: finite P_cr (26.081 kN) and K (1.0000) | 0.0e+00 | 0.0e+0 | PASS |
| preset designTrap: finite P_cr (34.597 kN) and K (0.5000) | 0.0e+00 | 0.0e+0 | PASS |
| end condition "fixed-pinned": top end A pinned, bottom end B fixed (as in Lab Part B) | 0.0e+00 | 0.0e+0 | PASS |
| D1 preset: 12 kN on the 63.5 × 1.65 mm tube, pinned, 2.0 m | 0.0e+00 | 0.0e+0 | PASS |
| pinned, L = 0.45 m: page closed form vs Python closed form (scipy brentq) | 0.0e+00 | 1.0e-12 | PASS |
| pinned, L = 0.45 m: page closed form vs scipy eigh on 128 Hermite elements | 2.2e-09 | 5.0e-08 | PASS |
| pinned, L = 0.45 m: page inverse iteration (64 elements) vs scipy eigh (128 elements) | 5.9e-09 | 2.0e-07 | PASS |
| fixed-pinned, L = 0.64 m: page closed form vs Python closed form (scipy brentq) | 0.0e+00 | 1.0e-12 | PASS |
| fixed-pinned, L = 0.64 m: page closed form vs scipy eigh on 128 Hermite elements | 1.7e-09 | 5.0e-08 | PASS |
| fixed-pinned, L = 0.64 m: page inverse iteration (64 elements) vs scipy eigh (128 elements) | 3.2e-08 | 2.0e-07 | PASS |
| fixed-fixed, L = 0.6005 m: page closed form vs Python closed form (scipy brentq) | 0.0e+00 | 1.0e-12 | PASS |
| fixed-fixed, L = 0.6005 m: page closed form vs scipy eigh on 128 Hermite elements | 8.1e-09 | 5.0e-08 | PASS |
| fixed-fixed, L = 0.6005 m: page inverse iteration (64 elements) vs scipy eigh (128 elements) | 1.2e-07 | 2.0e-07 | PASS |
| free-fixed, L = 1.0 m: page closed form vs Python closed form (scipy brentq) | 0.0e+00 | 1.0e-12 | PASS |
| free-fixed, L = 1.0 m: page closed form vs scipy eigh on 128 Hermite elements | 2.0e-08 | 5.0e-08 | PASS |
| free-fixed, L = 1.0 m: page inverse iteration (64 elements) vs scipy eigh (128 elements) | 2.0e-08 | 2.0e-07 | PASS |
| springs, L = 0.6005 m, k = 2800 N·m/rad: page closed form vs Python closed form (scipy brentq) | 0.0e+00 | 1.0e-12 | PASS |
| springs, L = 0.6005 m, k = 2800 N·m/rad: page closed form vs scipy eigh on 128 Hermite elements | 6.7e-09 | 5.0e-08 | PASS |
| springs, L = 0.6005 m, k = 2800 N·m/rad: page inverse iteration (64 elements) vs scipy eigh (128 elements) | 9.3e-08 | 2.0e-07 | PASS |
| spring-pin, L = 0.64 m, k = 2800 N·m/rad: page closed form vs Python closed form (scipy brentq) | 1.3e-15 | 1.0e-12 | PASS |
| spring-pin, L = 0.64 m, k = 2800 N·m/rad: page closed form vs scipy eigh on 128 Hermite elements | 1.4e-09 | 5.0e-08 | PASS |
| spring-pin, L = 0.64 m, k = 2800 N·m/rad: page inverse iteration (64 elements) vs scipy eigh (128 elements) | 2.9e-08 | 2.0e-07 | PASS |
| springs, L = 0.3 m, k = 50 N·m/rad: page closed form vs Python closed form (scipy brentq) | 7.7e-16 | 1.0e-12 | PASS |
| springs, L = 0.3 m, k = 50 N·m/rad: page closed form vs scipy eigh on 128 Hermite elements | 1.4e-09 | 5.0e-08 | PASS |
| springs, L = 0.3 m, k = 50 N·m/rad: page inverse iteration (64 elements) vs scipy eigh (128 elements) | 8.1e-09 | 2.0e-07 | PASS |
| spring-pin, L = 1.2 m, k = 100000 N·m/rad: page closed form vs Python closed form (scipy brentq) | 2.2e-16 | 1.0e-12 | PASS |
| spring-pin, L = 1.2 m, k = 100000 N·m/rad: page closed form vs scipy eigh on 128 Hermite elements | 2.0e-09 | 5.0e-08 | PASS |
| spring-pin, L = 1.2 m, k = 100000 N·m/rad: page inverse iteration (64 elements) vs scipy eigh (128 elements) | 3.2e-08 | 2.0e-07 | PASS |
| P = 0.3 P_cr, δ0 = 0.4 mm, e = 0 mm: page closed form (bow + Eq. 10.26) vs scipy banded finite differences (N = 4000 and 8000, Richardson), worst of 4 points | 1.3e-09 | 5.0e-08 | PASS |
| P = 0.3 P_cr, δ0 = 0.4 mm, e = 0 mm: page finite elements (64) vs Python finite elements (128, numpy solve), mid-length | 1.3e-08 | 5.0e-07 | PASS |
| P = 0.7 P_cr, δ0 = 0.46 mm, e = 1 mm: page closed form (bow + Eq. 10.26) vs scipy banded finite differences (N = 4000 and 8000, Richardson), worst of 4 points | 2.1e-09 | 5.0e-08 | PASS |
| P = 0.7 P_cr, δ0 = 0.46 mm, e = 1 mm: page finite elements (64) vs Python finite elements (128, numpy solve), mid-length | 1.8e-08 | 5.0e-07 | PASS |
| P = 0.7 P_cr, δ0 = 0.46 mm, e = 1 mm: page Eq. 10.35 vs Python Eq. 10.33 with Eq. 10.31 | 2.0e-16 | 1.0e-12 | PASS |
| P = 0.9 P_cr, δ0 = 0 mm, e = 2 mm: page closed form (bow + Eq. 10.26) vs scipy banded finite differences (N = 4000 and 8000, Richardson), worst of 4 points | 3.9e-10 | 5.0e-08 | PASS |
| P = 0.9 P_cr, δ0 = 0 mm, e = 2 mm: page finite elements (64) vs Python finite elements (128, numpy solve), mid-length | 3.8e-08 | 5.0e-07 | PASS |
| P = 0.9 P_cr, δ0 = 0 mm, e = 2 mm: page Eq. 10.35 vs Python Eq. 10.33 with Eq. 10.31 | 2.4e-16 | 1.0e-12 | PASS |
| P = 0.95 P_cr, δ0 = 0.26 mm, e = 0.08 mm: page closed form (bow + Eq. 10.26) vs scipy banded finite differences (N = 4000 and 8000, Richardson), worst of 4 points | 2.5e-08 | 5.0e-08 | PASS |
| P = 0.95 P_cr, δ0 = 0.26 mm, e = 0.08 mm: page finite elements (64) vs Python finite elements (128, numpy solve), mid-length | 1.6e-07 | 5.0e-07 | PASS |
| P = 0.95 P_cr, δ0 = 0.26 mm, e = 0.08 mm: page Eq. 10.35 vs Python Eq. 10.33 with Eq. 10.31 | 1.2e-16 | 1.0e-12 | PASS |
| elastica at 1.01 P_cr: page (Carlson R_F + bisection) vs scipy.special.ellipk, P/P_cr | 2.2e-16 | 1.0e-12 | PASS |
| elastica at 1.01 P_cr: page δ/L vs scipy.special | 0.0e+00 | 1.0e-12 | PASS |
| elastica at 1.01 P_cr: page δ/L vs scipy solve_bvp (collocation) | 4.9e-13 | 2.0e-07 | PASS |
| elastica at 1.01 P_cr: end slope, page vs solve_bvp | 4.9e-13 | 2.0e-07 | PASS |
| elastica at 1.1 P_cr: page (Carlson R_F + bisection) vs scipy.special.ellipk, P/P_cr | 4.0e-16 | 1.0e-12 | PASS |
| elastica at 1.1 P_cr: page δ/L vs scipy.special | 2.2e-16 | 1.0e-12 | PASS |
| elastica at 1.1 P_cr: page δ/L vs scipy solve_bvp (collocation) | 1.0e-13 | 2.0e-07 | PASS |
| elastica at 1.1 P_cr: end slope, page vs solve_bvp | 9.9e-14 | 2.0e-07 | PASS |
| elastica at 1.5 P_cr: page (Carlson R_F + bisection) vs scipy.special.ellipk, P/P_cr | 1.5e-16 | 1.0e-12 | PASS |
| elastica at 1.5 P_cr: page δ/L vs scipy.special | 2.8e-16 | 1.0e-12 | PASS |
| elastica at 1.5 P_cr: page δ/L vs scipy solve_bvp (collocation) | 2.2e-15 | 2.0e-07 | PASS |
| elastica at 1.5 P_cr: end slope, page vs solve_bvp | 3.9e-15 | 2.0e-07 | PASS |
| elastica at 2 P_cr: page (Carlson R_F + bisection) vs scipy.special.ellipk, P/P_cr | 6.7e-16 | 1.0e-12 | PASS |
| elastica at 2 P_cr: page δ/L vs scipy.special | 0.0e+00 | 1.0e-12 | PASS |
| elastica at 2 P_cr: page δ/L vs scipy solve_bvp (collocation) | 1.2e-15 | 2.0e-07 | PASS |
| elastica at 2 P_cr: end slope, page vs solve_bvp | 1.2e-15 | 2.0e-07 | PASS |
| secant first-yield load, e = 0.5 mm: page bisection vs scipy brentq (Eq. 10.36) | 4.8e-14 | 1.0e-10 | PASS |
| secant first-yield load, e = 1 mm: page bisection vs scipy brentq (Eq. 10.36) | 4.9e-14 | 1.0e-10 | PASS |
| secant first-yield load, e = 2 mm: page bisection vs scipy brentq (Eq. 10.36) | 5.5e-14 | 1.0e-10 | PASS |
| tangent-modulus column curve at L/r = 35: page vs Python (brentq) | 3.2e-15 | 1.0e-09 | PASS |
| reduced-modulus curve at L/r = 35: page vs Python | 2.3e-16 | 1.0e-09 | PASS |
| Aluminum Association 6061-T6 at L/r = 35: page vs Python | 0.0e+00 | 1.0e-14 | PASS |
| AISC σ_cr at L/r = 35 (E 200 GPa, σY 250 MPa): page vs Python | 0.0e+00 | 1.0e-14 | PASS |
| tangent-modulus column curve at L/r = 49.1: page vs Python (brentq) | 4.1e-16 | 1.0e-09 | PASS |
| reduced-modulus curve at L/r = 49.1: page vs Python | 6.5e-16 | 1.0e-09 | PASS |
| Aluminum Association 6061-T6 at L/r = 49.1: page vs Python | 0.0e+00 | 1.0e-14 | PASS |
| AISC σ_cr at L/r = 49.1 (E 200 GPa, σY 250 MPa): page vs Python | 0.0e+00 | 1.0e-14 | PASS |
| tangent-modulus column curve at L/r = 60: page vs Python (brentq) | 6.8e-14 | 1.0e-09 | PASS |
| reduced-modulus curve at L/r = 60: page vs Python | 4.8e-15 | 1.0e-09 | PASS |
| Aluminum Association 6061-T6 at L/r = 60: page vs Python | 0.0e+00 | 1.0e-14 | PASS |
| AISC σ_cr at L/r = 60 (E 200 GPa, σY 250 MPa): page vs Python | 0.0e+00 | 1.0e-14 | PASS |
| tangent-modulus column curve at L/r = 90: page vs Python (brentq) | 2.0e-15 | 1.0e-09 | PASS |
| reduced-modulus curve at L/r = 90: page vs Python | 1.0e-14 | 1.0e-09 | PASS |
| Aluminum Association 6061-T6 at L/r = 90: page vs Python | 0.0e+00 | 1.0e-14 | PASS |
| AISC σ_cr at L/r = 90 (E 200 GPa, σY 250 MPa): page vs Python | 0.0e+00 | 1.0e-14 | PASS |
| tangent-modulus column curve at L/r = 150: page vs Python (brentq) | 1.2e-13 | 1.0e-09 | PASS |
| reduced-modulus curve at L/r = 150: page vs Python | 1.2e-13 | 1.0e-09 | PASS |
| Aluminum Association 6061-T6 at L/r = 150: page vs Python | 0.0e+00 | 1.0e-14 | PASS |
| AISC σ_cr at L/r = 150 (E 200 GPa, σY 250 MPa): page vs Python | 0.0e+00 | 1.0e-14 | PASS |
| Part D: fiber-model maximum with 320 fibers vs the 80 used for the data (section discretization) | 8.7e-04 | 2.0e-03 | PASS |
| D1: page design preset, first-yield load (secant, Lab 2 E) vs analysis table | 3.6e-14 | 1.0e-10 | PASS |
| D1: page design preset, AA allowable load vs analysis table | 0.0e+00 | 1.0e-12 | PASS |
| D1: the preset tube 63.5 × 1.65 mm is the analysis's pinned answer [63.5, 1.65] | 0.0e+00 | 0.0e+00 | PASS |
| D1 trap: assuming clamped ends picks [44.45, 1.65], whose pinned allowable load is 4.53 kN < 12 kN | 0.0e+00 | 0.0e+00 | PASS |

Overall: **PASS**

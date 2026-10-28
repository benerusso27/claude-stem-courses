# Verification record — lab08_transformation

Run with `python3 shared/verify_lab.py lab08_transformation` on 2026-10-27. Detailed tables are in the `results_*.md` files next to this one.

| Step | Result | Detail | Record |
|---|---|---|---|
| Build simulation page | PASS |  |  |
| Model tests: closed form vs independent numerics (Node, exact page code) | PASS | 255 of 255 passed | `results_node.md` |
| Independent re-implementation (Python/scipy) and data-pipeline closure | PASS | 156 of 156 passed | `results_python.md` |
| Handout re-solved from scratch vs instructor key | PASS | 24 of 24 agree | `results_from_scratch.md` |
| Cross-file consistency (units, symbols, sign convention, references) | PASS | 97 of 97 passed | `results_consistency.md` |
| Browser check, 375/1280 px, light/dark, every control | PASS | PASS | `results_browser.md` |

## Formula vs. independent numerical method (worst case over all material presets)

| Comparison | Worst relative difference | Tolerance | Result |
|---|---:|---:|---|
| (σx, σy, τxy) = (80, -20, 30) MPa: Eqs. 7.5–7.7 vs R·S·Rᵀ at 24 angles, max \|Δ\|/scale (absolute difference) | 1.9e-16 | 1.0e-14 | PASS |
| (σx, σy, τxy) = (80, -20, 30) MPa: σx′ + σy′ = σx + σy (Eq. 7.8), max \|Δ\|/scale (absolute difference) | 9.3e-17 | 1.0e-14 | PASS |
| (σx, σy, τxy) = (80, -20, 30) MPa: σx′(θp) = σmax (Eq. 7.12 gives the larger root) | 0.0e+00 | 1.0e-13 | PASS |
| (σx, σy, τxy) = (80, -20, 30) MPa: τx′y′(θp) = 0, relative to R (absolute difference) | 0.0e+00 | 1.0e-13 | PASS |
| (σx, σy, τxy) = (80, -20, 30) MPa: τx′y′(θs) = +R (Eq. 7.15, θs = θp − 45°) | 0.0e+00 | 1.0e-13 | PASS |
| (σx, σy, τxy) = (80, -20, 30) MPa: σx′(θs) = σave | 0.0e+00 | 1.0e-13 | PASS |
| (σx, σy, τxy) = (80, -20, 30) MPa: σmax·σmin = σxσy − τxy² (invariant) | 0.0e+00 | 1.0e-12 | PASS |
| (σx, σy, τxy) = (80, -20, 30) MPa: X′ = (σx′, −τx′y′) lies at 2θ counterclockwise on the circle (Beer Fig. 7.15), max distance/scale (absolute difference) | 1.3e-16 | 1.0e-13 | PASS |
| (σx, σy, τxy) = (80, -20, 30) MPa: σmax, σmin (Eq. 7.14) vs Jacobi eigenvalues, max \|Δ\|/scale (absolute difference) | 3.7e-16 | 1.0e-14 | PASS |
| (σx, σy, τxy) = (53.36, 0, -21.34) MPa: Eqs. 7.5–7.7 vs R·S·Rᵀ at 24 angles, max \|Δ\|/scale (absolute difference) | 2.8e-16 | 1.0e-14 | PASS |
| (σx, σy, τxy) = (53.36, 0, -21.34) MPa: σx′ + σy′ = σx + σy (Eq. 7.8), max \|Δ\|/scale (absolute difference) | 1.4e-16 | 1.0e-14 | PASS |
| (σx, σy, τxy) = (53.36, 0, -21.34) MPa: σx′(θp) = σmax (Eq. 7.12 gives the larger root) | 1.2e-16 | 1.0e-13 | PASS |
| (σx, σy, τxy) = (53.36, 0, -21.34) MPa: τx′y′(θp) = 0, relative to R (absolute difference) | 0.0e+00 | 1.0e-13 | PASS |
| (σx, σy, τxy) = (53.36, 0, -21.34) MPa: τx′y′(θs) = +R (Eq. 7.15, θs = θp − 45°) | 0.0e+00 | 1.0e-13 | PASS |
| (σx, σy, τxy) = (53.36, 0, -21.34) MPa: σx′(θs) = σave | 0.0e+00 | 1.0e-13 | PASS |
| (σx, σy, τxy) = (53.36, 0, -21.34) MPa: σmax·σmin = σxσy − τxy² (invariant) | 0.0e+00 | 1.0e-12 | PASS |
| (σx, σy, τxy) = (53.36, 0, -21.34) MPa: X′ = (σx′, −τx′y′) lies at 2θ counterclockwise on the circle (Beer Fig. 7.15), max distance/scale (absolute difference) | 3.0e-16 | 1.0e-13 | PASS |
| (σx, σy, τxy) = (53.36, 0, -21.34) MPa: σmax, σmin (Eq. 7.14) vs Jacobi eigenvalues, max \|Δ\|/scale (absolute difference) | 2.8e-16 | 1.0e-14 | PASS |
| (σx, σy, τxy) = (0, 0, -24.77) MPa: Eqs. 7.5–7.7 vs R·S·Rᵀ at 24 angles, max \|Δ\|/scale (absolute difference) | 1.9e-16 | 1.0e-14 | PASS |
| (σx, σy, τxy) = (0, 0, -24.77) MPa: σx′ + σy′ = σx + σy (Eq. 7.8), max \|Δ\|/scale (absolute difference) | 0.0e+00 | 1.0e-14 | PASS |
| (σx, σy, τxy) = (0, 0, -24.77) MPa: σx′(θp) = σmax (Eq. 7.12 gives the larger root) | 0.0e+00 | 1.0e-13 | PASS |
| (σx, σy, τxy) = (0, 0, -24.77) MPa: τx′y′(θp) = 0, relative to R (absolute difference) | 6.1e-17 | 1.0e-13 | PASS |
| (σx, σy, τxy) = (0, 0, -24.77) MPa: τx′y′(θs) = +R (Eq. 7.15, θs = θp − 45°) | 0.0e+00 | 1.0e-13 | PASS |
| (σx, σy, τxy) = (0, 0, -24.77) MPa: σx′(θs) = σave | 0.0e+00 | 1.0e-13 | PASS |
| (σx, σy, τxy) = (0, 0, -24.77) MPa: σmax·σmin = σxσy − τxy² (invariant) | 0.0e+00 | 1.0e-12 | PASS |
| (σx, σy, τxy) = (0, 0, -24.77) MPa: X′ = (σx′, −τx′y′) lies at 2θ counterclockwise on the circle (Beer Fig. 7.15), max distance/scale (absolute difference) | 4.1e-16 | 1.0e-13 | PASS |
| (σx, σy, τxy) = (0, 0, -24.77) MPa: σmax, σmin (Eq. 7.14) vs Jacobi eigenvalues, max \|Δ\|/scale (absolute difference) | 0.0e+00 | 1.0e-14 | PASS |
| (σx, σy, τxy) = (100, 0, 0) MPa: Eqs. 7.5–7.7 vs R·S·Rᵀ at 24 angles, max \|Δ\|/scale (absolute difference) | 1.5e-16 | 1.0e-14 | PASS |
| (σx, σy, τxy) = (100, 0, 0) MPa: σx′ + σy′ = σx + σy (Eq. 7.8), max \|Δ\|/scale (absolute difference) | 0.0e+00 | 1.0e-14 | PASS |
| (σx, σy, τxy) = (100, 0, 0) MPa: σx′(θp) = σmax (Eq. 7.12 gives the larger root) | 0.0e+00 | 1.0e-13 | PASS |
| (σx, σy, τxy) = (100, 0, 0) MPa: τx′y′(θp) = 0, relative to R (absolute difference) | 0.0e+00 | 1.0e-13 | PASS |
| (σx, σy, τxy) = (100, 0, 0) MPa: τx′y′(θs) = +R (Eq. 7.15, θs = θp − 45°) | 0.0e+00 | 1.0e-13 | PASS |
| (σx, σy, τxy) = (100, 0, 0) MPa: σx′(θs) = σave | 0.0e+00 | 1.0e-13 | PASS |
| (σx, σy, τxy) = (100, 0, 0) MPa: σmax·σmin = σxσy − τxy² (invariant) | 0.0e+00 | 1.0e-12 | PASS |
| (σx, σy, τxy) = (100, 0, 0) MPa: X′ = (σx′, −τx′y′) lies at 2θ counterclockwise on the circle (Beer Fig. 7.15), max distance/scale (absolute difference) | 0.0e+00 | 1.0e-13 | PASS |
| (σx, σy, τxy) = (100, 0, 0) MPa: σmax, σmin (Eq. 7.14) vs Jacobi eigenvalues, max \|Δ\|/scale (absolute difference) | 0.0e+00 | 1.0e-14 | PASS |
| (σx, σy, τxy) = (-40, -90, 15) MPa: Eqs. 7.5–7.7 vs R·S·Rᵀ at 24 angles, max \|Δ\|/scale (absolute difference) | 3.3e-16 | 1.0e-14 | PASS |
| (σx, σy, τxy) = (-40, -90, 15) MPa: σx′ + σy′ = σx + σy (Eq. 7.8), max \|Δ\|/scale (absolute difference) | 1.7e-16 | 1.0e-14 | PASS |
| (σx, σy, τxy) = (-40, -90, 15) MPa: σx′(θp) = σmax (Eq. 7.12 gives the larger root) | 0.0e+00 | 1.0e-13 | PASS |
| (σx, σy, τxy) = (-40, -90, 15) MPa: τx′y′(θp) = 0, relative to R (absolute difference) | 0.0e+00 | 1.0e-13 | PASS |
| (σx, σy, τxy) = (-40, -90, 15) MPa: τx′y′(θs) = +R (Eq. 7.15, θs = θp − 45°) | 0.0e+00 | 1.0e-13 | PASS |
| (σx, σy, τxy) = (-40, -90, 15) MPa: σx′(θs) = σave | 0.0e+00 | 1.0e-13 | PASS |
| (σx, σy, τxy) = (-40, -90, 15) MPa: σmax·σmin = σxσy − τxy² (invariant) | 0.0e+00 | 1.0e-12 | PASS |
| (σx, σy, τxy) = (-40, -90, 15) MPa: X′ = (σx′, −τx′y′) lies at 2θ counterclockwise on the circle (Beer Fig. 7.15), max distance/scale (absolute difference) | 9.3e-17 | 1.0e-13 | PASS |
| (σx, σy, τxy) = (-40, -90, 15) MPa: σmax, σmin (Eq. 7.14) vs Jacobi eigenvalues, max \|Δ\|/scale (absolute difference) | 1.7e-16 | 1.0e-14 | PASS |
| (σx, σy, τxy) = (60, 60, 0) MPa: Eqs. 7.5–7.7 vs R·S·Rᵀ at 24 angles, max \|Δ\|/scale (absolute difference) | 1.2e-16 | 1.0e-14 | PASS |
| (σx, σy, τxy) = (60, 60, 0) MPa: σx′ + σy′ = σx + σy (Eq. 7.8), max \|Δ\|/scale (absolute difference) | 0.0e+00 | 1.0e-14 | PASS |
| (σx, σy, τxy) = (60, 60, 0) MPa: σmax·σmin = σxσy − τxy² (invariant) | 0.0e+00 | 1.0e-12 | PASS |
| (σx, σy, τxy) = (60, 60, 0) MPa: X′ = (σx′, −τx′y′) lies at 2θ counterclockwise on the circle (Beer Fig. 7.15), max distance/scale (absolute difference) | 0.0e+00 | 1.0e-13 | PASS |
| (σx, σy, τxy) = (60, 60, 0) MPa: σmax, σmin (Eq. 7.14) vs Jacobi eigenvalues, max \|Δ\|/scale (absolute difference) | 0.0e+00 | 1.0e-14 | PASS |
| (σx, σy, τxy) = (71.5, 36.4, -21.3) MPa: Eqs. 7.5–7.7 vs R·S·Rᵀ at 24 angles, max \|Δ\|/scale (absolute difference) | 2.1e-16 | 1.0e-14 | PASS |
| (σx, σy, τxy) = (71.5, 36.4, -21.3) MPa: σx′ + σy′ = σx + σy (Eq. 7.8), max \|Δ\|/scale (absolute difference) | 0.0e+00 | 1.0e-14 | PASS |
| (σx, σy, τxy) = (71.5, 36.4, -21.3) MPa: σx′(θp) = σmax (Eq. 7.12 gives the larger root) | 0.0e+00 | 1.0e-13 | PASS |
| (σx, σy, τxy) = (71.5, 36.4, -21.3) MPa: τx′y′(θp) = 0, relative to R (absolute difference) | 6.7e-17 | 1.0e-13 | PASS |
| (σx, σy, τxy) = (71.5, 36.4, -21.3) MPa: τx′y′(θs) = +R (Eq. 7.15, θs = θp − 45°) | 1.3e-16 | 1.0e-13 | PASS |
| (σx, σy, τxy) = (71.5, 36.4, -21.3) MPa: σx′(θs) = σave | 0.0e+00 | 1.0e-13 | PASS |
| (σx, σy, τxy) = (71.5, 36.4, -21.3) MPa: σmax·σmin = σxσy − τxy² (invariant) | 0.0e+00 | 1.0e-12 | PASS |
| (σx, σy, τxy) = (71.5, 36.4, -21.3) MPa: X′ = (σx′, −τx′y′) lies at 2θ counterclockwise on the circle (Beer Fig. 7.15), max distance/scale (absolute difference) | 2.1e-16 | 1.0e-13 | PASS |
| (σx, σy, τxy) = (71.5, 36.4, -21.3) MPa: σmax, σmin (Eq. 7.14) vs Jacobi eigenvalues, max \|Δ\|/scale (absolute difference) | 2.1e-16 | 1.0e-14 | PASS |
| (σx, σy, τxy) = (-10, 25, -60) MPa: Eqs. 7.5–7.7 vs R·S·Rᵀ at 24 angles, max \|Δ\|/scale (absolute difference) | 5.0e-16 | 1.0e-14 | PASS |
| (σx, σy, τxy) = (-10, 25, -60) MPa: σx′ + σy′ = σx + σy (Eq. 7.8), max \|Δ\|/scale (absolute difference) | 1.2e-16 | 1.0e-14 | PASS |
| (σx, σy, τxy) = (-10, 25, -60) MPa: σx′(θp) = σmax (Eq. 7.12 gives the larger root) | 0.0e+00 | 1.0e-13 | PASS |
| (σx, σy, τxy) = (-10, 25, -60) MPa: τx′y′(θp) = 0, relative to R (absolute difference) | 1.2e-16 | 1.0e-13 | PASS |
| (σx, σy, τxy) = (-10, 25, -60) MPa: τx′y′(θs) = +R (Eq. 7.15, θs = θp − 45°) | 1.2e-16 | 1.0e-13 | PASS |
| (σx, σy, τxy) = (-10, 25, -60) MPa: σx′(θs) = σave | 0.0e+00 | 1.0e-13 | PASS |
| (σx, σy, τxy) = (-10, 25, -60) MPa: σmax·σmin = σxσy − τxy² (invariant) | 2.0e-15 | 1.0e-12 | PASS |
| (σx, σy, τxy) = (-10, 25, -60) MPa: X′ = (σx′, −τx′y′) lies at 2θ counterclockwise on the circle (Beer Fig. 7.15), max distance/scale (absolute difference) | 6.8e-16 | 1.0e-13 | PASS |
| (σx, σy, τxy) = (-10, 25, -60) MPa: σmax, σmin (Eq. 7.14) vs Jacobi eigenvalues, max \|Δ\|/scale (absolute difference) | 1.2e-16 | 1.0e-14 | PASS |
| random 3-D state 1: principal stresses, trigonometric cubic vs Jacobi (3 sweeps), max \|Δ\|/scale (absolute difference) | 3.0e-16 | 1.0e-12 | PASS |
| random 3-D state 1: σ1 + σ2 + σ3 = I1 (absolute difference) | 0.0e+00 | 1.0e-12 | PASS |
| random 3-D state 1: σ1σ2σ3 = det S (absolute difference) | 9.5e-17 | 1.0e-12 | PASS |
| random 3-D state 2: principal stresses, trigonometric cubic vs Jacobi (3 sweeps), max \|Δ\|/scale (absolute difference) | 7.8e-16 | 1.0e-12 | PASS |
| random 3-D state 2: σ1 + σ2 + σ3 = I1 (absolute difference) | 1.9e-16 | 1.0e-12 | PASS |
| random 3-D state 2: σ1σ2σ3 = det S (absolute difference) | 3.0e-16 | 1.0e-12 | PASS |
| random 3-D state 3: principal stresses, trigonometric cubic vs Jacobi (3 sweeps), max \|Δ\|/scale (absolute difference) | 7.3e-16 | 1.0e-12 | PASS |
| random 3-D state 3: σ1 + σ2 + σ3 = I1 (absolute difference) | 0.0e+00 | 1.0e-12 | PASS |
| random 3-D state 3: σ1σ2σ3 = det S (absolute difference) | 7.2e-16 | 1.0e-12 | PASS |
| random 3-D state 4: principal stresses, trigonometric cubic vs Jacobi (3 sweeps), max \|Δ\|/scale (absolute difference) | 5.7e-16 | 1.0e-12 | PASS |
| random 3-D state 4: σ1 + σ2 + σ3 = I1 (absolute difference) | 1.9e-16 | 1.0e-12 | PASS |
| random 3-D state 4: σ1σ2σ3 = det S (absolute difference) | 1.4e-16 | 1.0e-12 | PASS |
| random 3-D state 5: principal stresses, trigonometric cubic vs Jacobi (2 sweeps), max \|Δ\|/scale (absolute difference) | 3.6e-16 | 1.0e-12 | PASS |
| random 3-D state 5: σ1 + σ2 + σ3 = I1 (absolute difference) | 0.0e+00 | 1.0e-12 | PASS |
| random 3-D state 5: σ1σ2σ3 = det S (absolute difference) | 1.1e-16 | 1.0e-12 | PASS |
| random 3-D state 6: principal stresses, trigonometric cubic vs Jacobi (3 sweeps), max \|Δ\|/scale (absolute difference) | 6.5e-16 | 1.0e-12 | PASS |
| random 3-D state 6: σ1 + σ2 + σ3 = I1 (absolute difference) | 0.0e+00 | 1.0e-12 | PASS |
| random 3-D state 6: σ1σ2σ3 = det S (absolute difference) | 4.2e-16 | 1.0e-12 | PASS |
| random 3-D state 7: principal stresses, trigonometric cubic vs Jacobi (3 sweeps), max \|Δ\|/scale (absolute difference) | 6.3e-16 | 1.0e-12 | PASS |
| random 3-D state 7: σ1 + σ2 + σ3 = I1 (absolute difference) | 0.0e+00 | 1.0e-12 | PASS |
| random 3-D state 7: σ1σ2σ3 = det S (absolute difference) | 3.0e-17 | 1.0e-12 | PASS |
| random 3-D state 8: principal stresses, trigonometric cubic vs Jacobi (4 sweeps), max \|Δ\|/scale (absolute difference) | 5.7e-16 | 1.0e-12 | PASS |
| random 3-D state 8: σ1 + σ2 + σ3 = I1 (absolute difference) | 0.0e+00 | 1.0e-12 | PASS |
| random 3-D state 8: σ1σ2σ3 = det S (absolute difference) | 1.4e-16 | 1.0e-12 | PASS |
| random 3-D state 9: principal stresses, trigonometric cubic vs Jacobi (3 sweeps), max \|Δ\|/scale (absolute difference) | 9.1e-16 | 1.0e-12 | PASS |
| random 3-D state 9: σ1 + σ2 + σ3 = I1 (absolute difference) | 0.0e+00 | 1.0e-12 | PASS |
| random 3-D state 9: σ1σ2σ3 = det S (absolute difference) | 4.3e-16 | 1.0e-12 | PASS |
| random 3-D state 10: principal stresses, trigonometric cubic vs Jacobi (4 sweeps), max \|Δ\|/scale (absolute difference) | 9.0e-16 | 1.0e-12 | PASS |
| random 3-D state 10: σ1 + σ2 + σ3 = I1 (absolute difference) | 1.6e-16 | 1.0e-12 | PASS |
| random 3-D state 10: σ1σ2σ3 = det S (absolute difference) | 1.3e-15 | 1.0e-12 | PASS |
| random 3-D state 11: principal stresses, trigonometric cubic vs Jacobi (4 sweeps), max \|Δ\|/scale (absolute difference) | 9.0e-16 | 1.0e-12 | PASS |
| random 3-D state 11: σ1 + σ2 + σ3 = I1 (absolute difference) | 0.0e+00 | 1.0e-12 | PASS |
| random 3-D state 11: σ1σ2σ3 = det S (absolute difference) | 6.9e-17 | 1.0e-12 | PASS |
| random 3-D state 12: principal stresses, trigonometric cubic vs Jacobi (3 sweeps), max \|Δ\|/scale (absolute difference) | 9.6e-16 | 1.0e-12 | PASS |
| random 3-D state 12: σ1 + σ2 + σ3 = I1 (absolute difference) | 0.0e+00 | 1.0e-12 | PASS |
| random 3-D state 12: σ1σ2σ3 = det S (absolute difference) | 4.0e-16 | 1.0e-12 | PASS |
| preset "general 3-D": principal3 (cubic) vs Jacobi, max \|Δ\| (MPa) (absolute difference) | 3.0e-14 | 1.0e-9 | PASS |
| equal biaxial 60 MPa: absolute τmax = 30 MPa while in-plane R = 0 | 0.0e+00 | 1.0e-14 | PASS |
| von Mises: uniaxial σ gives σ | 0.0e+00 | 1.0e-14 | PASS |
| von Mises: pure shear τ gives √3 τ | 0.0e+00 | 1.0e-14 | PASS |
| Tresca equivalent: pure shear τ gives 2τ | 0.0e+00 | 1.0e-14 | PASS |
| sampled σmax converges as N⁻² (observed 1.997) | 0.0e+00 | 0.0e+0 | PASS |
| mean error of the sampled maximum at N = 256 ≈ π²R/(6N²) | 2.0e-03 | 5.0e-2 | PASS |
| random strain 1, rect rosette: closed form (Eq. 7.43) vs Gaussian elimination, max \|Δ\|/1000 µε (absolute difference) | 5.4e-17 | 1.0e-13 | PASS |
| random strain 1, rect: recovers ε_x, ε_y, γ_xy (absolute difference) | 5.4e-17 | 1.0e-13 | PASS |
| random strain 1, delta rosette: closed form (delta formulas) vs Gaussian elimination, max \|Δ\|/1000 µε (absolute difference) | 1.1e-16 | 1.0e-13 | PASS |
| random strain 1, delta: recovers ε_x, ε_y, γ_xy (absolute difference) | 2.2e-16 | 1.0e-13 | PASS |
| random strain 1, rosette at 12°, 77°, 140° (Eq. 7.60): recovers the state (absolute difference) | 3.3e-16 | 1.0e-12 | PASS |
| random strain 1: K_t = 3 % model then correction (closed form) returns the true state (absolute difference) | 5.4e-17 | 1.0e-13 | PASS |
| random strain 1: K_t correction, closed form vs Gaussian elimination (absolute difference) | 1.1e-16 | 1.0e-13 | PASS |
| random strain 1: rosette turned 4°, turned back (Eqs. 7.44, 7.45, 7.49) returns the state (absolute difference) | 1.1e-16 | 1.0e-13 | PASS |
| random strain 1: a turned rosette gives the same principal strains (invariant) (absolute difference) | 5.4e-17 | 1.0e-13 | PASS |
| random strain 1: ... and principal directions off by exactly the turn (absolute difference) | 0.0e+00 | 1.0e-11 | PASS |
| random strain 1: Hooke's law and its inverse (plane stress) (absolute difference) | 1.1e-16 | 1.0e-13 | PASS |
| random strain 1: principal directions of stress and strain coincide (isotropic) (absolute difference) | 1.1e-16 | 1.0e-12 | PASS |
| random strain 2, rect rosette: closed form (Eq. 7.43) vs Gaussian elimination, max \|Δ\|/1000 µε (absolute difference) | 5.1e-17 | 1.0e-13 | PASS |
| random strain 2, rect: recovers ε_x, ε_y, γ_xy (absolute difference) | 5.1e-17 | 1.0e-13 | PASS |
| random strain 2, delta rosette: closed form (delta formulas) vs Gaussian elimination, max \|Δ\|/1000 µε (absolute difference) | 6.4e-17 | 1.0e-13 | PASS |
| random strain 2, delta: recovers ε_x, ε_y, γ_xy (absolute difference) | 7.8e-17 | 1.0e-13 | PASS |
| random strain 2, rosette at 12°, 77°, 140° (Eq. 7.60): recovers the state (absolute difference) | 1.7e-17 | 1.0e-12 | PASS |
| random strain 2: K_t = 3 % model then correction (closed form) returns the true state (absolute difference) | 5.1e-17 | 1.0e-13 | PASS |
| random strain 2: K_t correction, closed form vs Gaussian elimination (absolute difference) | 8.8e-17 | 1.0e-13 | PASS |
| random strain 2: rosette turned 4°, turned back (Eqs. 7.44, 7.45, 7.49) returns the state (absolute difference) | 1.0e-17 | 1.0e-13 | PASS |
| random strain 2: a turned rosette gives the same principal strains (invariant) (absolute difference) | 1.4e-17 | 1.0e-13 | PASS |
| random strain 2: ... and principal directions off by exactly the turn (absolute difference) | 0.0e+00 | 1.0e-11 | PASS |
| random strain 2: Hooke's law and its inverse (plane stress) (absolute difference) | 1.4e-17 | 1.0e-13 | PASS |
| random strain 2: principal directions of stress and strain coincide (isotropic) (absolute difference) | 1.4e-17 | 1.0e-12 | PASS |
| random strain 3, rect rosette: closed form (Eq. 7.43) vs Gaussian elimination, max \|Δ\|/1000 µε (absolute difference) | 1.7e-16 | 1.0e-13 | PASS |
| random strain 3, rect: recovers ε_x, ε_y, γ_xy (absolute difference) | 1.8e-16 | 1.0e-13 | PASS |
| random strain 3, delta rosette: closed form (delta formulas) vs Gaussian elimination, max \|Δ\|/1000 µε (absolute difference) | 2.6e-16 | 1.0e-13 | PASS |
| random strain 3, delta: recovers ε_x, ε_y, γ_xy (absolute difference) | 2.1e-16 | 1.0e-13 | PASS |
| random strain 3, rosette at 12°, 77°, 140° (Eq. 7.60): recovers the state (absolute difference) | 5.4e-17 | 1.0e-12 | PASS |
| random strain 3: K_t = 3 % model then correction (closed form) returns the true state (absolute difference) | 1.2e-16 | 1.0e-13 | PASS |
| random strain 3: K_t correction, closed form vs Gaussian elimination (absolute difference) | 2.8e-16 | 1.0e-13 | PASS |
| random strain 3: rosette turned 4°, turned back (Eqs. 7.44, 7.45, 7.49) returns the state (absolute difference) | 5.4e-17 | 1.0e-13 | PASS |
| random strain 3: a turned rosette gives the same principal strains (invariant) (absolute difference) | 0.0e+00 | 1.0e-13 | PASS |
| random strain 3: ... and principal directions off by exactly the turn (absolute difference) | 0.0e+00 | 1.0e-11 | PASS |
| random strain 3: Hooke's law and its inverse (plane stress) (absolute difference) | 5.4e-17 | 1.0e-13 | PASS |
| random strain 3: principal directions of stress and strain coincide (isotropic) (absolute difference) | 0.0e+00 | 1.0e-12 | PASS |
| random strain 4, rect rosette: closed form (Eq. 7.43) vs Gaussian elimination, max \|Δ\|/1000 µε (absolute difference) | 3.2e-16 | 1.0e-13 | PASS |
| random strain 4, rect: recovers ε_x, ε_y, γ_xy (absolute difference) | 3.3e-16 | 1.0e-13 | PASS |
| random strain 4, delta rosette: closed form (delta formulas) vs Gaussian elimination, max \|Δ\|/1000 µε (absolute difference) | 5.8e-16 | 1.0e-13 | PASS |
| random strain 4, delta: recovers ε_x, ε_y, γ_xy (absolute difference) | 4.8e-16 | 1.0e-13 | PASS |
| random strain 4, rosette at 12°, 77°, 140° (Eq. 7.60): recovers the state (absolute difference) | 2.2e-16 | 1.0e-12 | PASS |
| random strain 4: K_t = 3 % model then correction (closed form) returns the true state (absolute difference) | 4.3e-16 | 1.0e-13 | PASS |
| random strain 4: K_t correction, closed form vs Gaussian elimination (absolute difference) | 5.8e-16 | 1.0e-13 | PASS |
| random strain 4: rosette turned 4°, turned back (Eqs. 7.44, 7.45, 7.49) returns the state (absolute difference) | 1.4e-16 | 1.0e-13 | PASS |
| random strain 4: a turned rosette gives the same principal strains (invariant) (absolute difference) | 1.1e-16 | 1.0e-13 | PASS |
| random strain 4: ... and principal directions off by exactly the turn (absolute difference) | 0.0e+00 | 1.0e-11 | PASS |
| random strain 4: Hooke's law and its inverse (plane stress) (absolute difference) | 2.2e-16 | 1.0e-13 | PASS |
| random strain 4: principal directions of stress and strain coincide (isotropic) (absolute difference) | 1.7e-18 | 1.0e-12 | PASS |
| random strain 5, rect rosette: closed form (Eq. 7.43) vs Gaussian elimination, max \|Δ\|/1000 µε (absolute difference) | 3.3e-16 | 1.0e-13 | PASS |
| random strain 5, rect: recovers ε_x, ε_y, γ_xy (absolute difference) | 3.3e-16 | 1.0e-13 | PASS |
| random strain 5, delta rosette: closed form (delta formulas) vs Gaussian elimination, max \|Δ\|/1000 µε (absolute difference) | 2.2e-16 | 1.0e-13 | PASS |
| random strain 5, delta: recovers ε_x, ε_y, γ_xy (absolute difference) | 2.2e-16 | 1.0e-13 | PASS |
| random strain 5, rosette at 12°, 77°, 140° (Eq. 7.60): recovers the state (absolute difference) | 3.3e-16 | 1.0e-12 | PASS |
| random strain 5: K_t = 3 % model then correction (closed form) returns the true state (absolute difference) | 1.1e-16 | 1.0e-13 | PASS |
| random strain 5: K_t correction, closed form vs Gaussian elimination (absolute difference) | 3.3e-16 | 1.0e-13 | PASS |
| random strain 5: rosette turned 4°, turned back (Eqs. 7.44, 7.45, 7.49) returns the state (absolute difference) | 2.2e-16 | 1.0e-13 | PASS |
| random strain 5: a turned rosette gives the same principal strains (invariant) (absolute difference) | 2.2e-16 | 1.0e-13 | PASS |
| random strain 5: ... and principal directions off by exactly the turn (absolute difference) | 0.0e+00 | 1.0e-11 | PASS |
| random strain 5: Hooke's law and its inverse (plane stress) (absolute difference) | 1.1e-16 | 1.0e-13 | PASS |
| random strain 5: principal directions of stress and strain coincide (isotropic) (absolute difference) | 0.0e+00 | 1.0e-12 | PASS |
| random strain 6, rect rosette: closed form (Eq. 7.43) vs Gaussian elimination, max \|Δ\|/1000 µε (absolute difference) | 2.7e-17 | 1.0e-13 | PASS |
| random strain 6, rect: recovers ε_x, ε_y, γ_xy (absolute difference) | 2.7e-17 | 1.0e-13 | PASS |
| random strain 6, delta rosette: closed form (delta formulas) vs Gaussian elimination, max \|Δ\|/1000 µε (absolute difference) | 5.4e-17 | 1.0e-13 | PASS |
| random strain 6, delta: recovers ε_x, ε_y, γ_xy (absolute difference) | 0.0e+00 | 1.0e-13 | PASS |
| random strain 6, rosette at 12°, 77°, 140° (Eq. 7.60): recovers the state (absolute difference) | 2.7e-17 | 1.0e-12 | PASS |
| random strain 6: K_t = 3 % model then correction (closed form) returns the true state (absolute difference) | 5.4e-17 | 1.0e-13 | PASS |
| random strain 6: K_t correction, closed form vs Gaussian elimination (absolute difference) | 1.6e-16 | 1.0e-13 | PASS |
| random strain 6: rosette turned 4°, turned back (Eqs. 7.44, 7.45, 7.49) returns the state (absolute difference) | 8.1e-17 | 1.0e-13 | PASS |
| random strain 6: a turned rosette gives the same principal strains (invariant) (absolute difference) | 5.4e-17 | 1.0e-13 | PASS |
| random strain 6: ... and principal directions off by exactly the turn (absolute difference) | 0.0e+00 | 1.0e-11 | PASS |
| random strain 6: Hooke's law and its inverse (plane stress) (absolute difference) | 0.0e+00 | 1.0e-13 | PASS |
| random strain 6: principal directions of stress and strain coincide (isotropic) (absolute difference) | 0.0e+00 | 1.0e-12 | PASS |
| random strain 7, rect rosette: closed form (Eq. 7.43) vs Gaussian elimination, max \|Δ\|/1000 µε (absolute difference) | 5.4e-17 | 1.0e-13 | PASS |
| random strain 7, rect: recovers ε_x, ε_y, γ_xy (absolute difference) | 1.6e-16 | 1.0e-13 | PASS |
| random strain 7, delta rosette: closed form (delta formulas) vs Gaussian elimination, max \|Δ\|/1000 µε (absolute difference) | 1.6e-16 | 1.0e-13 | PASS |
| random strain 7, delta: recovers ε_x, ε_y, γ_xy (absolute difference) | 1.6e-16 | 1.0e-13 | PASS |
| random strain 7, rosette at 12°, 77°, 140° (Eq. 7.60): recovers the state (absolute difference) | 1.6e-16 | 1.0e-12 | PASS |
| random strain 7: K_t = 3 % model then correction (closed form) returns the true state (absolute difference) | 1.1e-16 | 1.0e-13 | PASS |
| random strain 7: K_t correction, closed form vs Gaussian elimination (absolute difference) | 2.2e-16 | 1.0e-13 | PASS |
| random strain 7: rosette turned 4°, turned back (Eqs. 7.44, 7.45, 7.49) returns the state (absolute difference) | 1.6e-16 | 1.0e-13 | PASS |
| random strain 7: a turned rosette gives the same principal strains (invariant) (absolute difference) | 1.1e-16 | 1.0e-13 | PASS |
| random strain 7: ... and principal directions off by exactly the turn (absolute difference) | 0.0e+00 | 1.0e-11 | PASS |
| random strain 7: Hooke's law and its inverse (plane stress) (absolute difference) | 0.0e+00 | 1.0e-13 | PASS |
| random strain 7: principal directions of stress and strain coincide (isotropic) (absolute difference) | 0.0e+00 | 1.0e-12 | PASS |
| random strain 8, rect rosette: closed form (Eq. 7.43) vs Gaussian elimination, max \|Δ\|/1000 µε (absolute difference) | 1.1e-16 | 1.0e-13 | PASS |
| random strain 8, rect: recovers ε_x, ε_y, γ_xy (absolute difference) | 2.6e-16 | 1.0e-13 | PASS |
| random strain 8, delta rosette: closed form (delta formulas) vs Gaussian elimination, max \|Δ\|/1000 µε (absolute difference) | 3.4e-18 | 1.0e-13 | PASS |
| random strain 8, delta: recovers ε_x, ε_y, γ_xy (absolute difference) | 1.1e-16 | 1.0e-13 | PASS |
| random strain 8, rosette at 12°, 77°, 140° (Eq. 7.60): recovers the state (absolute difference) | 8.5e-18 | 1.0e-12 | PASS |
| random strain 8: K_t = 3 % model then correction (closed form) returns the true state (absolute difference) | 2.6e-16 | 1.0e-13 | PASS |
| random strain 8: K_t correction, closed form vs Gaussian elimination (absolute difference) | 4.3e-16 | 1.0e-13 | PASS |
| random strain 8: rosette turned 4°, turned back (Eqs. 7.44, 7.45, 7.49) returns the state (absolute difference) | 2.2e-16 | 1.0e-13 | PASS |
| random strain 8: a turned rosette gives the same principal strains (invariant) (absolute difference) | 1.1e-16 | 1.0e-13 | PASS |
| random strain 8: ... and principal directions off by exactly the turn (absolute difference) | 0.0e+00 | 1.0e-11 | PASS |
| random strain 8: Hooke's law and its inverse (plane stress) (absolute difference) | 1.1e-16 | 1.0e-13 | PASS |
| random strain 8: principal directions of stress and strain coincide (isotropic) (absolute difference) | 0.0e+00 | 1.0e-12 | PASS |
| Eq. 7.60 is singular for two parallel gages (0°, 0°, 90°) | 0.0e+00 | 0.0e+0 | PASS |
| determinant of Eq. 7.60: rectangular rosette | 1.1e-16 | 1.0e-12 | PASS |
| Part B at H: σx = F L_b c / I equals the Lab 6 X2 prediction 53.36 MPa | 3.9e-05 | 2.0e-4 | PASS |
| Part B at H: τ = T c / J equals Lab 6 X2 21.34 MPa | 1.5e-04 | 2.0e-4 | PASS |
| Part B at K: V Q/(I t) equals Lab 6 X2 3.43 MPa | 1.2e-03 | 2.0e-3 | PASS |
| Part B at K: torsion and transverse shear add to Lab 6 X2 24.77 MPa | 3.9e-05 | 2.0e-4 | PASS |
| Part B on the far side (φ = −90°): they subtract, Lab 6 X2 17.92 MPa | 1.5e-04 | 2.0e-4 | PASS |
| Part B at K: no bending stress at the neutral axis (MPa) (absolute difference) | 3.3e-15 | 1.0e-9 | PASS |
| tube: J = 2I | 0.0e+00 | 1.0e-15 | PASS |
| tube: Q from the top to φ = 10°, closed form vs Simpson (64 intervals) | 3.1e-13 | 3.0e-8 | PASS |
| tube: Q from the top to φ = 45°, closed form vs Simpson (64 intervals) | 1.3e-10 | 3.0e-8 | PASS |
| tube: Q from the top to φ = 90°, closed form vs Simpson (64 intervals) | 2.0e-09 | 3.0e-8 | PASS |
| tube: Q from the top to φ = 135°, closed form vs Simpson (64 intervals) | 1.0e-08 | 3.0e-8 | PASS |
| Part C: hoop stress at the outer surface (Lamé) = 2p r_i²/(r_o² − r_i²) | 2.1e-16 | 1.0e-14 | PASS |
| Part C: axial stress from the closed ends = half the outer hoop stress (Lamé) | 0.0e+00 | 1.0e-14 | PASS |
| Lamé: hoop stress at r_o, finite differences N = 64 vs closed form | 6.5e-05 | 3.0e-4 | PASS |
| Lamé: hoop stress at r_i, finite differences N = 64 vs closed form | 7.3e-05 | 3.0e-4 | PASS |
| Lamé: axial stress, finite differences N = 64 vs closed form | 2.2e-05 | 3.0e-4 | PASS |
| Lamé: σ_r(r_i) = −p and σ_r(r_o) = 0 hold (MPa), N = 64 (absolute difference) | 8.3e-12 | 1.0e-6 | PASS |
| Lamé: hoop stress at r_o, finite differences N = 256 vs closed form | 4.2e-06 | 1.9e-5 | PASS |
| Lamé: hoop stress at r_i, finite differences N = 256 vs closed form | 4.6e-06 | 1.9e-5 | PASS |
| Lamé: axial stress, finite differences N = 256 vs closed form | 1.4e-06 | 1.9e-5 | PASS |
| Lamé: σ_r(r_i) = −p and σ_r(r_o) = 0 hold (MPa), N = 256 (absolute difference) | 2.3e-11 | 1.0e-6 | PASS |
| Lamé: hoop stress at r_o, finite differences N = 1024 vs closed form | 2.6e-07 | 1.2e-6 | PASS |
| Lamé: hoop stress at r_i, finite differences N = 1024 vs closed form | 2.9e-07 | 1.2e-6 | PASS |
| Lamé: axial stress, finite differences N = 1024 vs closed form | 8.6e-08 | 1.2e-6 | PASS |
| Lamé: σ_r(r_i) = −p and σ_r(r_o) = 0 hold (MPa), N = 1024 (absolute difference) | 1.0e-10 | 1.0e-6 | PASS |
| thin-wall p r_i/t equals the through-wall average of the Lamé hoop stress | 1.1e-09 | 1.0e-6 | PASS |
| thin-wall p r_i/t over the Lamé value at the gages = (r_o + r_i)/(2 r_i) = 1.10 | 0.0e+00 | 1.0e-12 | PASS |
| ... which for this tube is exactly 1.100 | 2.0e-16 | 1.0e-12 | PASS |
| finite-difference cylinder converges as N⁻² (observed 1.918) | 0.0e+00 | 0.0e+0 | PASS |
| Simpson Q converges as N⁻⁴ (observed 4.002) | 0.0e+00 | 0.0e+0 | PASS |
| Part C + lever at H: σmax = 81.61 and σmin = 26.30 MPa are both tensile | 0.0e+00 | 0.0e+0 | PASS |
| Part C + lever at H: absolute τmax = σmax/2 (σ_r = 0 is σ3) | 0.0e+00 | 1.0e-14 | PASS |
| ... which is 1.475 times the in-plane R | 0.0e+00 | 0.0e+0 | PASS |
| Part C + lever at H: σ1, numerical route (Simpson Q, FD cylinder, Jacobi) vs closed forms | 1.5e-07 | 1.0e-5 | PASS |
| D1 preset, inner surface: σ_r = −p | 3.7e-16 | 1.0e-14 | PASS |
| D1 preset: bending at the inner fiber M r_i / I | 0.0e+00 | 1.0e-12 | PASS |
| preset rosHB: rosette turned 1.45°, K_t 1.2 %, reduced and turned back = tube strains (µε) (absolute difference) | 2.2e-13 | 1.0e-9 | PASS |
| preset rosKB: rosette turned -1.00°, K_t 1.2 %, reduced and turned back = tube strains (µε) (absolute difference) | 8.9e-14 | 1.0e-9 | PASS |
| preset "crooked": with β = 5° the state is recovered (µε) (absolute difference) | 0.0e+00 | 1.0e-9 | PASS |
| preset "crooked": assumed straight, γ_xy is off by -166 µε | 0.0e+00 | 0.0e+0 | PASS |
| preset "K_t = 4 %": with the correction the state is recovered (µε) (absolute difference) | 1.1e-13 | 1.0e-9 | PASS |
| preset "K_t = 4 %": uncorrected ε_x is off by only -1.4 µε (its transverse strain is near the calibration ratio −ν₀) ... | 0.0e+00 | 0.0e+0 | PASS |
| ... but ε_y (gage c, across the main strain) by 28.4 µε | 0.0e+00 | 0.0e+0 | PASS |
| state 1: Eqs. 7.5–7.7 (JS) vs R·S·Rᵀ (numpy), max \|Δ\|/scale (absolute) | 1.3e-16 | 1.0e-14 | PASS |
| state 1: Mohr σmax, σmin (JS) vs numpy eigh, max \|Δ\|/scale (absolute) | 0.0e+00 | 1.0e-14 | PASS |
| state 1: θp (JS, Eq. 7.12 with atan2) vs eigenvector of the larger eigenvalue (rad) (absolute) | 2.2e-16 | 1.0e-12 | PASS |
| state 1: 3-D principal stresses, trigonometric cubic (JS) vs numpy eigvalsh, max \|Δ\|/scale (absolute) | 9.2e-16 | 1.0e-12 | PASS |
| state 1: 3-D principal stresses, Jacobi (JS) vs numpy eigvalsh (absolute) | 1.0e-15 | 1.0e-12 | PASS |
| state 1: z principal: Mohr + σz (JS principal3) vs numpy (absolute) | 0.0e+00 | 1.0e-13 | PASS |
| state 2: Eqs. 7.5–7.7 (JS) vs R·S·Rᵀ (numpy), max \|Δ\|/scale (absolute) | 2.3e-16 | 1.0e-14 | PASS |
| state 2: Mohr σmax, σmin (JS) vs numpy eigh, max \|Δ\|/scale (absolute) | 2.8e-17 | 1.0e-14 | PASS |
| state 2: θp (JS, Eq. 7.12 with atan2) vs eigenvector of the larger eigenvalue (rad) (absolute) | 1.1e-16 | 1.0e-12 | PASS |
| state 2: 3-D principal stresses, trigonometric cubic (JS) vs numpy eigvalsh, max \|Δ\|/scale (absolute) | 1.4e-15 | 1.0e-12 | PASS |
| state 2: 3-D principal stresses, Jacobi (JS) vs numpy eigvalsh (absolute) | 6.8e-16 | 1.0e-12 | PASS |
| state 2: z principal: Mohr + σz (JS principal3) vs numpy (absolute) | 2.8e-17 | 1.0e-13 | PASS |
| state 3: Eqs. 7.5–7.7 (JS) vs R·S·Rᵀ (numpy), max \|Δ\|/scale (absolute) | 1.2e-16 | 1.0e-14 | PASS |
| state 3: Mohr σmax, σmin (JS) vs numpy eigh, max \|Δ\|/scale (absolute) | 0.0e+00 | 1.0e-14 | PASS |
| state 3: θp (JS, Eq. 7.12 with atan2) vs eigenvector of the larger eigenvalue (rad) (absolute) | 2.2e-16 | 1.0e-12 | PASS |
| state 3: 3-D principal stresses, trigonometric cubic (JS) vs numpy eigvalsh, max \|Δ\|/scale (absolute) | 7.2e-16 | 1.0e-12 | PASS |
| state 3: 3-D principal stresses, Jacobi (JS) vs numpy eigvalsh (absolute) | 8.4e-16 | 1.0e-12 | PASS |
| state 3: z principal: Mohr + σz (JS principal3) vs numpy (absolute) | 0.0e+00 | 1.0e-13 | PASS |
| state 4: Eqs. 7.5–7.7 (JS) vs R·S·Rᵀ (numpy), max \|Δ\|/scale (absolute) | 1.5e-16 | 1.0e-14 | PASS |
| state 4: Mohr σmax, σmin (JS) vs numpy eigh, max \|Δ\|/scale (absolute) | 0.0e+00 | 1.0e-14 | PASS |
| state 4: θp (JS, Eq. 7.12 with atan2) vs eigenvector of the larger eigenvalue (rad) (absolute) | 5.3e-16 | 1.0e-12 | PASS |
| state 4: 3-D principal stresses, trigonometric cubic (JS) vs numpy eigvalsh, max \|Δ\|/scale (absolute) | 3.0e-16 | 1.0e-12 | PASS |
| state 4: 3-D principal stresses, Jacobi (JS) vs numpy eigvalsh (absolute) | 8.0e-16 | 1.0e-12 | PASS |
| state 4: z principal: Mohr + σz (JS principal3) vs numpy (absolute) | 0.0e+00 | 1.0e-13 | PASS |
| state 5: Eqs. 7.5–7.7 (JS) vs R·S·Rᵀ (numpy), max \|Δ\|/scale (absolute) | 1.2e-16 | 1.0e-14 | PASS |
| state 5: Mohr σmax, σmin (JS) vs numpy eigh, max \|Δ\|/scale (absolute) | 0.0e+00 | 1.0e-14 | PASS |
| state 5: θp (JS, Eq. 7.12 with atan2) vs eigenvector of the larger eigenvalue (rad) (absolute) | 0.0e+00 | 1.0e-12 | PASS |
| state 5: 3-D principal stresses, trigonometric cubic (JS) vs numpy eigvalsh, max \|Δ\|/scale (absolute) | 6.7e-16 | 1.0e-12 | PASS |
| state 5: 3-D principal stresses, Jacobi (JS) vs numpy eigvalsh (absolute) | 1.2e-15 | 1.0e-12 | PASS |
| state 5: z principal: Mohr + σz (JS principal3) vs numpy (absolute) | 0.0e+00 | 1.0e-13 | PASS |
| state 6: Eqs. 7.5–7.7 (JS) vs R·S·Rᵀ (numpy), max \|Δ\|/scale (absolute) | 5.1e-17 | 1.0e-14 | PASS |
| state 6: Mohr σmax, σmin (JS) vs numpy eigh, max \|Δ\|/scale (absolute) | 2.6e-17 | 1.0e-14 | PASS |
| state 6: θp (JS, Eq. 7.12 with atan2) vs eigenvector of the larger eigenvalue (rad) (absolute) | 2.2e-16 | 1.0e-12 | PASS |
| state 6: 3-D principal stresses, trigonometric cubic (JS) vs numpy eigvalsh, max \|Δ\|/scale (absolute) | 2.1e-16 | 1.0e-12 | PASS |
| state 6: 3-D principal stresses, Jacobi (JS) vs numpy eigvalsh (absolute) | 4.1e-16 | 1.0e-12 | PASS |
| state 6: z principal: Mohr + σz (JS principal3) vs numpy (absolute) | 2.6e-17 | 1.0e-13 | PASS |
| state 7: Eqs. 7.5–7.7 (JS) vs R·S·Rᵀ (numpy), max \|Δ\|/scale (absolute) | 2.7e-16 | 1.0e-14 | PASS |
| state 7: Mohr σmax, σmin (JS) vs numpy eigh, max \|Δ\|/scale (absolute) | 1.0e-16 | 1.0e-14 | PASS |
| state 7: θp (JS, Eq. 7.12 with atan2) vs eigenvector of the larger eigenvalue (rad) (absolute) | 4.4e-16 | 1.0e-12 | PASS |
| state 7: 3-D principal stresses, trigonometric cubic (JS) vs numpy eigvalsh, max \|Δ\|/scale (absolute) | 6.6e-16 | 1.0e-12 | PASS |
| state 7: 3-D principal stresses, Jacobi (JS) vs numpy eigvalsh (absolute) | 8.2e-16 | 1.0e-12 | PASS |
| state 7: z principal: Mohr + σz (JS principal3) vs numpy (absolute) | 1.0e-16 | 1.0e-13 | PASS |
| state 8: Eqs. 7.5–7.7 (JS) vs R·S·Rᵀ (numpy), max \|Δ\|/scale (absolute) | 1.2e-16 | 1.0e-14 | PASS |
| state 8: Mohr σmax, σmin (JS) vs numpy eigh, max \|Δ\|/scale (absolute) | 1.2e-16 | 1.0e-14 | PASS |
| state 8: θp (JS, Eq. 7.12 with atan2) vs eigenvector of the larger eigenvalue (rad) (absolute) | 1.1e-16 | 1.0e-12 | PASS |
| state 8: 3-D principal stresses, trigonometric cubic (JS) vs numpy eigvalsh, max \|Δ\|/scale (absolute) | 6.1e-16 | 1.0e-12 | PASS |
| state 8: 3-D principal stresses, Jacobi (JS) vs numpy eigvalsh (absolute) | 1.2e-15 | 1.0e-12 | PASS |
| state 8: z principal: Mohr + σz (JS principal3) vs numpy (absolute) | 1.2e-16 | 1.0e-13 | PASS |
| state 9: Eqs. 7.5–7.7 (JS) vs R·S·Rᵀ (numpy), max \|Δ\|/scale (absolute) | 7.2e-18 | 1.0e-14 | PASS |
| state 9: Mohr σmax, σmin (JS) vs numpy eigh, max \|Δ\|/scale (absolute) | 5.8e-17 | 1.0e-14 | PASS |
| state 9: θp (JS, Eq. 7.12 with atan2) vs eigenvector of the larger eigenvalue (rad) (absolute) | 1.8e-16 | 1.0e-12 | PASS |
| state 9: 3-D principal stresses, trigonometric cubic (JS) vs numpy eigvalsh, max \|Δ\|/scale (absolute) | 2.3e-16 | 1.0e-12 | PASS |
| state 9: 3-D principal stresses, Jacobi (JS) vs numpy eigvalsh (absolute) | 2.3e-16 | 1.0e-12 | PASS |
| state 9: z principal: Mohr + σz (JS principal3) vs numpy (absolute) | 5.8e-17 | 1.0e-13 | PASS |
| state 10: Eqs. 7.5–7.7 (JS) vs R·S·Rᵀ (numpy), max \|Δ\|/scale (absolute) | 7.1e-17 | 1.0e-14 | PASS |
| state 10: Mohr σmax, σmin (JS) vs numpy eigh, max \|Δ\|/scale (absolute) | 0.0e+00 | 1.0e-14 | PASS |
| state 10: θp (JS, Eq. 7.12 with atan2) vs eigenvector of the larger eigenvalue (rad) (absolute) | 1.1e-16 | 1.0e-12 | PASS |
| state 10: 3-D principal stresses, trigonometric cubic (JS) vs numpy eigvalsh, max \|Δ\|/scale (absolute) | 4.3e-16 | 1.0e-12 | PASS |
| state 10: 3-D principal stresses, Jacobi (JS) vs numpy eigvalsh (absolute) | 5.7e-16 | 1.0e-12 | PASS |
| state 10: z principal: Mohr + σz (JS principal3) vs numpy (absolute) | 0.0e+00 | 1.0e-13 | PASS |
| strain 1: rectangular rosette Eq. 7.43 (JS) vs least squares (numpy), max \|Δ\| (µε) (absolute) | 8.7e-13 | 1.0e-09 | PASS |
| strain 1: delta rosette formulas (JS) vs least squares, max \|Δ\| (µε) (absolute) | 6.5e-13 | 1.0e-09 | PASS |
| strain 1: gages at 11.5°, 63.0°, 137.5°: Gaussian elimination (JS) vs least squares, max \|Δ\| (µε) (absolute) | 4.3e-13 | 1.0e-09 | PASS |
| strain 1: readings of a rosette turned 3° with K_t = 2 %, JS vs Python forward model (µε) (absolute) | 6.5e-13 | 1.0e-09 | PASS |
| strain 1: page's K_t correction and turn-back (closed form) vs Python least squares and tensor rotation (µε) (absolute) | 1.3e-12 | 1.0e-09 | PASS |
| strain 1: ... recovers the true strains (µε) (absolute) | 1.1e-12 | 1.0e-09 | PASS |
| strain 2: rectangular rosette Eq. 7.43 (JS) vs least squares (numpy), max \|Δ\| (µε) (absolute) | 4.3e-13 | 1.0e-09 | PASS |
| strain 2: delta rosette formulas (JS) vs least squares, max \|Δ\| (µε) (absolute) | 5.4e-13 | 1.0e-09 | PASS |
| strain 2: gages at 11.5°, 63.0°, 137.5°: Gaussian elimination (JS) vs least squares, max \|Δ\| (µε) (absolute) | 1.6e-13 | 1.0e-09 | PASS |
| strain 2: readings of a rosette turned 3° with K_t = 2 %, JS vs Python forward model (µε) (absolute) | 3.4e-15 | 1.0e-09 | PASS |
| strain 2: page's K_t correction and turn-back (closed form) vs Python least squares and tensor rotation (µε) (absolute) | 1.1e-13 | 1.0e-09 | PASS |
| strain 2: ... recovers the true strains (µε) (absolute) | 2.2e-13 | 1.0e-09 | PASS |
| strain 3: rectangular rosette Eq. 7.43 (JS) vs least squares (numpy), max \|Δ\| (µε) (absolute) | 2.2e-13 | 1.0e-09 | PASS |
| strain 3: delta rosette formulas (JS) vs least squares, max \|Δ\| (µε) (absolute) | 5.4e-13 | 1.0e-09 | PASS |
| strain 3: gages at 11.5°, 63.0°, 137.5°: Gaussian elimination (JS) vs least squares, max \|Δ\| (µε) (absolute) | 2.2e-13 | 1.0e-09 | PASS |
| strain 3: readings of a rosette turned 3° with K_t = 2 %, JS vs Python forward model (µε) (absolute) | 0.0e+00 | 1.0e-09 | PASS |
| strain 3: page's K_t correction and turn-back (closed form) vs Python least squares and tensor rotation (µε) (absolute) | 3.2e-13 | 1.0e-09 | PASS |
| strain 3: ... recovers the true strains (µε) (absolute) | 6.5e-13 | 1.0e-09 | PASS |
| strain 4: rectangular rosette Eq. 7.43 (JS) vs least squares (numpy), max \|Δ\| (µε) (absolute) | 2.2e-13 | 1.0e-09 | PASS |
| strain 4: delta rosette formulas (JS) vs least squares, max \|Δ\| (µε) (absolute) | 3.2e-13 | 1.0e-09 | PASS |
| strain 4: gages at 11.5°, 63.0°, 137.5°: Gaussian elimination (JS) vs least squares, max \|Δ\| (µε) (absolute) | 4.3e-13 | 1.0e-09 | PASS |
| strain 4: readings of a rosette turned 3° with K_t = 2 %, JS vs Python forward model (µε) (absolute) | 0.0e+00 | 1.0e-09 | PASS |
| strain 4: page's K_t correction and turn-back (closed form) vs Python least squares and tensor rotation (µε) (absolute) | 4.3e-13 | 1.0e-09 | PASS |
| strain 4: ... recovers the true strains (µε) (absolute) | 3.2e-13 | 1.0e-09 | PASS |
| strain 5: rectangular rosette Eq. 7.43 (JS) vs least squares (numpy), max \|Δ\| (µε) (absolute) | 7.6e-13 | 1.0e-09 | PASS |
| strain 5: delta rosette formulas (JS) vs least squares, max \|Δ\| (µε) (absolute) | 9.8e-13 | 1.0e-09 | PASS |
| strain 5: gages at 11.5°, 63.0°, 137.5°: Gaussian elimination (JS) vs least squares, max \|Δ\| (µε) (absolute) | 4.3e-13 | 1.0e-09 | PASS |
| strain 5: readings of a rosette turned 3° with K_t = 2 %, JS vs Python forward model (µε) (absolute) | 3.2e-13 | 1.0e-09 | PASS |
| strain 5: page's K_t correction and turn-back (closed form) vs Python least squares and tensor rotation (µε) (absolute) | 4.3e-13 | 1.0e-09 | PASS |
| strain 5: ... recovers the true strains (µε) (absolute) | 5.4e-13 | 1.0e-09 | PASS |
| strain 6: rectangular rosette Eq. 7.43 (JS) vs least squares (numpy), max \|Δ\| (µε) (absolute) | 5.4e-13 | 1.0e-09 | PASS |
| strain 6: delta rosette formulas (JS) vs least squares, max \|Δ\| (µε) (absolute) | 4.3e-13 | 1.0e-09 | PASS |
| strain 6: gages at 11.5°, 63.0°, 137.5°: Gaussian elimination (JS) vs least squares, max \|Δ\| (µε) (absolute) | 2.2e-13 | 1.0e-09 | PASS |
| strain 6: readings of a rosette turned 3° with K_t = 2 %, JS vs Python forward model (µε) (absolute) | 2.2e-13 | 1.0e-09 | PASS |
| strain 6: page's K_t correction and turn-back (closed form) vs Python least squares and tensor rotation (µε) (absolute) | 7.6e-13 | 1.0e-09 | PASS |
| strain 6: ... recovers the true strains (µε) (absolute) | 5.4e-13 | 1.0e-09 | PASS |
| strain 7: rectangular rosette Eq. 7.43 (JS) vs least squares (numpy), max \|Δ\| (µε) (absolute) | 2.2e-13 | 1.0e-09 | PASS |
| strain 7: delta rosette formulas (JS) vs least squares, max \|Δ\| (µε) (absolute) | 5.4e-13 | 1.0e-09 | PASS |
| strain 7: gages at 11.5°, 63.0°, 137.5°: Gaussian elimination (JS) vs least squares, max \|Δ\| (µε) (absolute) | 1.1e-13 | 1.0e-09 | PASS |
| strain 7: readings of a rosette turned 3° with K_t = 2 %, JS vs Python forward model (µε) (absolute) | 1.1e-13 | 1.0e-09 | PASS |
| strain 7: page's K_t correction and turn-back (closed form) vs Python least squares and tensor rotation (µε) (absolute) | 3.2e-13 | 1.0e-09 | PASS |
| strain 7: ... recovers the true strains (µε) (absolute) | 1.6e-13 | 1.0e-09 | PASS |
| strain 8: rectangular rosette Eq. 7.43 (JS) vs least squares (numpy), max \|Δ\| (µε) (absolute) | 1.6e-13 | 1.0e-09 | PASS |
| strain 8: delta rosette formulas (JS) vs least squares, max \|Δ\| (µε) (absolute) | 4.3e-13 | 1.0e-09 | PASS |
| strain 8: gages at 11.5°, 63.0°, 137.5°: Gaussian elimination (JS) vs least squares, max \|Δ\| (µε) (absolute) | 6.5e-13 | 1.0e-09 | PASS |
| strain 8: readings of a rosette turned 3° with K_t = 2 %, JS vs Python forward model (µε) (absolute) | 1.1e-13 | 1.0e-09 | PASS |
| strain 8: page's K_t correction and turn-back (closed form) vs Python least squares and tensor rotation (µε) (absolute) | 8.7e-13 | 1.0e-09 | PASS |
| strain 8: ... recovers the true strains (µε) (absolute) | 7.6e-13 | 1.0e-09 | PASS |
| σx, σθ, τxy: JS closed forms vs Python with Q by scipy dblquad, max \|Δ\|/scale (absolute) | 1.9e-16 | 1.0e-10 | PASS |
| Q of the wall from the top (JS closed form vs dblquad) | 3.6e-16 | 1.0e-10 | PASS |
| hoop stress at r_o: JS finite differences (1024) vs scipy solve_bvp | 5.1e-06 | 1.0e-05 | PASS |
| axial stress: JS finite differences vs scipy solve_bvp | 1.2e-06 | 1.0e-05 | PASS |
| hoop stress at r_o: JS Lamé closed form vs scipy solve_bvp | 6.2e-16 | 1.0e-08 | PASS |
| principal stresses at the inner surface (σr = −p): JS vs numpy, max \|Δ\| (MPa) (absolute) | 1.5e-14 | 1.0e-08 | PASS |
| D1: absolute τmax at the critical point of 44.45 × 4.78, page preset (inner surface, top) vs analysis | 7.3e-16 | 1.0e-12 | PASS |
| D1: the analysis's critical point for 44.45 × 4.78 is the inner surface, tension side | 0.0e+00 | 0.0e+00 | PASS |
| D1: the in-plane trap picks 50.8 × 3.18, lighter than 44.45 × 4.78 and unsafe by Tresca | 0.0e+00 | 0.0e+00 | PASS |

Overall: **PASS**

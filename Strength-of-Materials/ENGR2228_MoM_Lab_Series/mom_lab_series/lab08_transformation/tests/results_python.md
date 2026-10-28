## Lab 8 — independent checks (Python/scipy) and data-pipeline closure

| Test | Value | Reference | Rel. difference | Tolerance | Result |
|---|---:|---:|---:|---:|---|
| state 1: Eqs. 7.5–7.7 (JS) vs R·S·Rᵀ (numpy), max \|Δ\|/scale (absolute) | 1.3149321e-16 | 0 | 1.31e-16 | 1.0e-14 | PASS |
| state 1: Mohr σmax, σmin (JS) vs numpy eigh, max \|Δ\|/scale (absolute) | 0 | 0 | 0.00e+00 | 1.0e-14 | PASS |
| state 1: θp (JS, Eq. 7.12 with atan2) vs eigenvector of the larger eigenvalue (rad) (absolute) | 2.220446e-16 | 0 | 2.22e-16 | 1.0e-12 | PASS |
| state 1: 3-D principal stresses, trigonometric cubic (JS) vs numpy eigvalsh, max \|Δ\|/scale (absolute) | 9.2045244e-16 | 0 | 9.20e-16 | 1.0e-12 | PASS |
| state 1: 3-D principal stresses, Jacobi (JS) vs numpy eigvalsh (absolute) | 1.0519456e-15 | 0 | 1.05e-15 | 1.0e-12 | PASS |
| state 1: z principal: Mohr + σz (JS principal3) vs numpy (absolute) | 0 | 0 | 0.00e+00 | 1.0e-13 | PASS |
| state 2: Eqs. 7.5–7.7 (JS) vs R·S·Rᵀ (numpy), max \|Δ\|/scale (absolute) | 2.2607633e-16 | 0 | 2.26e-16 | 1.0e-14 | PASS |
| state 2: Mohr σmax, σmin (JS) vs numpy eigh, max \|Δ\|/scale (absolute) | 2.8259542e-17 | 0 | 2.83e-17 | 1.0e-14 | PASS |
| state 2: θp (JS, Eq. 7.12 with atan2) vs eigenvector of the larger eigenvalue (rad) (absolute) | 1.110223e-16 | 0 | 1.11e-16 | 1.0e-12 | PASS |
| state 2: 3-D principal stresses, trigonometric cubic (JS) vs numpy eigvalsh, max \|Δ\|/scale (absolute) | 1.356458e-15 | 0 | 1.36e-15 | 1.0e-12 | PASS |
| state 2: 3-D principal stresses, Jacobi (JS) vs numpy eigvalsh (absolute) | 6.78229e-16 | 0 | 6.78e-16 | 1.0e-12 | PASS |
| state 2: z principal: Mohr + σz (JS principal3) vs numpy (absolute) | 2.8259542e-17 | 0 | 2.83e-17 | 1.0e-13 | PASS |
| state 3: Eqs. 7.5–7.7 (JS) vs R·S·Rᵀ (numpy), max \|Δ\|/scale (absolute) | 1.2063202e-16 | 0 | 1.21e-16 | 1.0e-14 | PASS |
| state 3: Mohr σmax, σmin (JS) vs numpy eigh, max \|Δ\|/scale (absolute) | 0 | 0 | 0.00e+00 | 1.0e-14 | PASS |
| state 3: θp (JS, Eq. 7.12 with atan2) vs eigenvector of the larger eigenvalue (rad) (absolute) | 2.220446e-16 | 0 | 2.22e-16 | 1.0e-12 | PASS |
| state 3: 3-D principal stresses, trigonometric cubic (JS) vs numpy eigvalsh, max \|Δ\|/scale (absolute) | 7.2379214e-16 | 0 | 7.24e-16 | 1.0e-12 | PASS |
| state 3: 3-D principal stresses, Jacobi (JS) vs numpy eigvalsh (absolute) | 8.4442417e-16 | 0 | 8.44e-16 | 1.0e-12 | PASS |
| state 3: z principal: Mohr + σz (JS principal3) vs numpy (absolute) | 0 | 0 | 0.00e+00 | 1.0e-13 | PASS |
| state 4: Eqs. 7.5–7.7 (JS) vs R·S·Rᵀ (numpy), max \|Δ\|/scale (absolute) | 1.5064464e-16 | 0 | 1.51e-16 | 1.0e-14 | PASS |
| state 4: Mohr σmax, σmin (JS) vs numpy eigh, max \|Δ\|/scale (absolute) | 0 | 0 | 0.00e+00 | 1.0e-14 | PASS |
| state 4: θp (JS, Eq. 7.12 with atan2) vs eigenvector of the larger eigenvalue (rad) (absolute) | 5.2735594e-16 | 0 | 5.27e-16 | 1.0e-12 | PASS |
| state 4: 3-D principal stresses, trigonometric cubic (JS) vs numpy eigvalsh, max \|Δ\|/scale (absolute) | 3.0128927e-16 | 0 | 3.01e-16 | 1.0e-12 | PASS |
| state 4: 3-D principal stresses, Jacobi (JS) vs numpy eigvalsh (absolute) | 8.0343806e-16 | 0 | 8.03e-16 | 1.0e-12 | PASS |
| state 4: z principal: Mohr + σz (JS principal3) vs numpy (absolute) | 0 | 0 | 0.00e+00 | 1.0e-13 | PASS |
| state 5: Eqs. 7.5–7.7 (JS) vs R·S·Rᵀ (numpy), max \|Δ\|/scale (absolute) | 1.1712874e-16 | 0 | 1.17e-16 | 1.0e-14 | PASS |
| state 5: Mohr σmax, σmin (JS) vs numpy eigh, max \|Δ\|/scale (absolute) | 0 | 0 | 0.00e+00 | 1.0e-14 | PASS |
| state 5: θp (JS, Eq. 7.12 with atan2) vs eigenvector of the larger eigenvalue (rad) (absolute) | 0 | 0 | 0.00e+00 | 1.0e-12 | PASS |
| state 5: 3-D principal stresses, trigonometric cubic (JS) vs numpy eigvalsh, max \|Δ\|/scale (absolute) | 6.7349024e-16 | 0 | 6.73e-16 | 1.0e-12 | PASS |
| state 5: 3-D principal stresses, Jacobi (JS) vs numpy eigvalsh (absolute) | 1.1712874e-15 | 0 | 1.17e-15 | 1.0e-12 | PASS |
| state 5: z principal: Mohr + σz (JS principal3) vs numpy (absolute) | 0 | 0 | 0.00e+00 | 1.0e-13 | PASS |
| state 6: Eqs. 7.5–7.7 (JS) vs R·S·Rᵀ (numpy), max \|Δ\|/scale (absolute) | 5.1175146e-17 | 0 | 5.12e-17 | 1.0e-14 | PASS |
| state 6: Mohr σmax, σmin (JS) vs numpy eigh, max \|Δ\|/scale (absolute) | 2.5587573e-17 | 0 | 2.56e-17 | 1.0e-14 | PASS |
| state 6: θp (JS, Eq. 7.12 with atan2) vs eigenvector of the larger eigenvalue (rad) (absolute) | 2.220446e-16 | 0 | 2.22e-16 | 1.0e-12 | PASS |
| state 6: 3-D principal stresses, trigonometric cubic (JS) vs numpy eigvalsh, max \|Δ\|/scale (absolute) | 2.0470058e-16 | 0 | 2.05e-16 | 1.0e-12 | PASS |
| state 6: 3-D principal stresses, Jacobi (JS) vs numpy eigvalsh (absolute) | 4.0940117e-16 | 0 | 4.09e-16 | 1.0e-12 | PASS |
| state 6: z principal: Mohr + σz (JS principal3) vs numpy (absolute) | 2.5587573e-17 | 0 | 2.56e-17 | 1.0e-13 | PASS |
| state 7: Eqs. 7.5–7.7 (JS) vs R·S·Rᵀ (numpy), max \|Δ\|/scale (absolute) | 2.7256769e-16 | 0 | 2.73e-16 | 1.0e-14 | PASS |
| state 7: Mohr σmax, σmin (JS) vs numpy eigh, max \|Δ\|/scale (absolute) | 1.0221288e-16 | 0 | 1.02e-16 | 1.0e-14 | PASS |
| state 7: θp (JS, Eq. 7.12 with atan2) vs eigenvector of the larger eigenvalue (rad) (absolute) | 4.4408921e-16 | 0 | 4.44e-16 | 1.0e-12 | PASS |
| state 7: 3-D principal stresses, trigonometric cubic (JS) vs numpy eigvalsh, max \|Δ\|/scale (absolute) | 6.6438373e-16 | 0 | 6.64e-16 | 1.0e-12 | PASS |
| state 7: 3-D principal stresses, Jacobi (JS) vs numpy eigvalsh (absolute) | 8.1770306e-16 | 0 | 8.18e-16 | 1.0e-12 | PASS |
| state 7: z principal: Mohr + σz (JS principal3) vs numpy (absolute) | 1.0221288e-16 | 0 | 1.02e-16 | 1.0e-13 | PASS |
| state 8: Eqs. 7.5–7.7 (JS) vs R·S·Rᵀ (numpy), max \|Δ\|/scale (absolute) | 1.2255949e-16 | 0 | 1.23e-16 | 1.0e-14 | PASS |
| state 8: Mohr σmax, σmin (JS) vs numpy eigh, max \|Δ\|/scale (absolute) | 1.2255949e-16 | 0 | 1.23e-16 | 1.0e-14 | PASS |
| state 8: θp (JS, Eq. 7.12 with atan2) vs eigenvector of the larger eigenvalue (rad) (absolute) | 1.110223e-16 | 0 | 1.11e-16 | 1.0e-12 | PASS |
| state 8: 3-D principal stresses, trigonometric cubic (JS) vs numpy eigvalsh, max \|Δ\|/scale (absolute) | 6.1279743e-16 | 0 | 6.13e-16 | 1.0e-12 | PASS |
| state 8: 3-D principal stresses, Jacobi (JS) vs numpy eigvalsh (absolute) | 1.2255949e-15 | 0 | 1.23e-15 | 1.0e-12 | PASS |
| state 8: z principal: Mohr + σz (JS principal3) vs numpy (absolute) | 1.2255949e-16 | 0 | 1.23e-16 | 1.0e-13 | PASS |
| state 9: Eqs. 7.5–7.7 (JS) vs R·S·Rᵀ (numpy), max \|Δ\|/scale (absolute) | 7.1972638e-18 | 0 | 7.20e-18 | 1.0e-14 | PASS |
| state 9: Mohr σmax, σmin (JS) vs numpy eigh, max \|Δ\|/scale (absolute) | 5.757811e-17 | 0 | 5.76e-17 | 1.0e-14 | PASS |
| state 9: θp (JS, Eq. 7.12 with atan2) vs eigenvector of the larger eigenvalue (rad) (absolute) | 1.8041124e-16 | 0 | 1.80e-16 | 1.0e-12 | PASS |
| state 9: 3-D principal stresses, trigonometric cubic (JS) vs numpy eigvalsh, max \|Δ\|/scale (absolute) | 2.3031244e-16 | 0 | 2.30e-16 | 1.0e-12 | PASS |
| state 9: 3-D principal stresses, Jacobi (JS) vs numpy eigvalsh (absolute) | 2.3031244e-16 | 0 | 2.30e-16 | 1.0e-12 | PASS |
| state 9: z principal: Mohr + σz (JS principal3) vs numpy (absolute) | 5.757811e-17 | 0 | 5.76e-17 | 1.0e-13 | PASS |
| state 10: Eqs. 7.5–7.7 (JS) vs R·S·Rᵀ (numpy), max \|Δ\|/scale (absolute) | 7.0971839e-17 | 0 | 7.10e-17 | 1.0e-14 | PASS |
| state 10: Mohr σmax, σmin (JS) vs numpy eigh, max \|Δ\|/scale (absolute) | 0 | 0 | 0.00e+00 | 1.0e-14 | PASS |
| state 10: θp (JS, Eq. 7.12 with atan2) vs eigenvector of the larger eigenvalue (rad) (absolute) | 1.110223e-16 | 0 | 1.11e-16 | 1.0e-12 | PASS |
| state 10: 3-D principal stresses, trigonometric cubic (JS) vs numpy eigvalsh, max \|Δ\|/scale (absolute) | 4.2583104e-16 | 0 | 4.26e-16 | 1.0e-12 | PASS |
| state 10: 3-D principal stresses, Jacobi (JS) vs numpy eigvalsh (absolute) | 5.6777471e-16 | 0 | 5.68e-16 | 1.0e-12 | PASS |
| state 10: z principal: Mohr + σz (JS principal3) vs numpy (absolute) | 0 | 0 | 0.00e+00 | 1.0e-13 | PASS |
| strain 1: rectangular rosette Eq. 7.43 (JS) vs least squares (numpy), max \|Δ\| (µε) (absolute) | 8.6736174e-13 | 0 | 8.67e-13 | 1.0e-09 | PASS |
| strain 1: delta rosette formulas (JS) vs least squares, max \|Δ\| (µε) (absolute) | 6.505213e-13 | 0 | 6.51e-13 | 1.0e-09 | PASS |
| strain 1: gages at 11.5°, 63.0°, 137.5°: Gaussian elimination (JS) vs least squares, max \|Δ\| (µε) (absolute) | 4.3368087e-13 | 0 | 4.34e-13 | 1.0e-09 | PASS |
| strain 1: readings of a rosette turned 3° with K_t = 2 %, JS vs Python forward model (µε) (absolute) | 6.505213e-13 | 0 | 6.51e-13 | 1.0e-09 | PASS |
| strain 1: page's K_t correction and turn-back (closed form) vs Python least squares and tensor rotation (µε) (absolute) | 1.3010426e-12 | 0 | 1.30e-12 | 1.0e-09 | PASS |
| strain 1: ... recovers the true strains (µε) (absolute) | 1.0842022e-12 | 0 | 1.08e-12 | 1.0e-09 | PASS |
| strain 2: rectangular rosette Eq. 7.43 (JS) vs least squares (numpy), max \|Δ\| (µε) (absolute) | 4.3368087e-13 | 0 | 4.34e-13 | 1.0e-09 | PASS |
| strain 2: delta rosette formulas (JS) vs least squares, max \|Δ\| (µε) (absolute) | 5.4210109e-13 | 0 | 5.42e-13 | 1.0e-09 | PASS |
| strain 2: gages at 11.5°, 63.0°, 137.5°: Gaussian elimination (JS) vs least squares, max \|Δ\| (µε) (absolute) | 1.6263033e-13 | 0 | 1.63e-13 | 1.0e-09 | PASS |
| strain 2: readings of a rosette turned 3° with K_t = 2 %, JS vs Python forward model (µε) (absolute) | 3.3881318e-15 | 0 | 3.39e-15 | 1.0e-09 | PASS |
| strain 2: page's K_t correction and turn-back (closed form) vs Python least squares and tensor rotation (µε) (absolute) | 1.0842022e-13 | 0 | 1.08e-13 | 1.0e-09 | PASS |
| strain 2: ... recovers the true strains (µε) (absolute) | 2.1684043e-13 | 0 | 2.17e-13 | 1.0e-09 | PASS |
| strain 3: rectangular rosette Eq. 7.43 (JS) vs least squares (numpy), max \|Δ\| (µε) (absolute) | 2.1684043e-13 | 0 | 2.17e-13 | 1.0e-09 | PASS |
| strain 3: delta rosette formulas (JS) vs least squares, max \|Δ\| (µε) (absolute) | 5.4210109e-13 | 0 | 5.42e-13 | 1.0e-09 | PASS |
| strain 3: gages at 11.5°, 63.0°, 137.5°: Gaussian elimination (JS) vs least squares, max \|Δ\| (µε) (absolute) | 2.1684043e-13 | 0 | 2.17e-13 | 1.0e-09 | PASS |
| strain 3: readings of a rosette turned 3° with K_t = 2 %, JS vs Python forward model (µε) (absolute) | 0 | 0 | 0.00e+00 | 1.0e-09 | PASS |
| strain 3: page's K_t correction and turn-back (closed form) vs Python least squares and tensor rotation (µε) (absolute) | 3.2526065e-13 | 0 | 3.25e-13 | 1.0e-09 | PASS |
| strain 3: ... recovers the true strains (µε) (absolute) | 6.505213e-13 | 0 | 6.51e-13 | 1.0e-09 | PASS |
| strain 4: rectangular rosette Eq. 7.43 (JS) vs least squares (numpy), max \|Δ\| (µε) (absolute) | 2.1684043e-13 | 0 | 2.17e-13 | 1.0e-09 | PASS |
| strain 4: delta rosette formulas (JS) vs least squares, max \|Δ\| (µε) (absolute) | 3.2526065e-13 | 0 | 3.25e-13 | 1.0e-09 | PASS |
| strain 4: gages at 11.5°, 63.0°, 137.5°: Gaussian elimination (JS) vs least squares, max \|Δ\| (µε) (absolute) | 4.3368087e-13 | 0 | 4.34e-13 | 1.0e-09 | PASS |
| strain 4: readings of a rosette turned 3° with K_t = 2 %, JS vs Python forward model (µε) (absolute) | 0 | 0 | 0.00e+00 | 1.0e-09 | PASS |
| strain 4: page's K_t correction and turn-back (closed form) vs Python least squares and tensor rotation (µε) (absolute) | 4.3368087e-13 | 0 | 4.34e-13 | 1.0e-09 | PASS |
| strain 4: ... recovers the true strains (µε) (absolute) | 3.2526065e-13 | 0 | 3.25e-13 | 1.0e-09 | PASS |
| strain 5: rectangular rosette Eq. 7.43 (JS) vs least squares (numpy), max \|Δ\| (µε) (absolute) | 7.5894152e-13 | 0 | 7.59e-13 | 1.0e-09 | PASS |
| strain 5: delta rosette formulas (JS) vs least squares, max \|Δ\| (µε) (absolute) | 9.7578196e-13 | 0 | 9.76e-13 | 1.0e-09 | PASS |
| strain 5: gages at 11.5°, 63.0°, 137.5°: Gaussian elimination (JS) vs least squares, max \|Δ\| (µε) (absolute) | 4.3368087e-13 | 0 | 4.34e-13 | 1.0e-09 | PASS |
| strain 5: readings of a rosette turned 3° with K_t = 2 %, JS vs Python forward model (µε) (absolute) | 3.2526065e-13 | 0 | 3.25e-13 | 1.0e-09 | PASS |
| strain 5: page's K_t correction and turn-back (closed form) vs Python least squares and tensor rotation (µε) (absolute) | 4.3368087e-13 | 0 | 4.34e-13 | 1.0e-09 | PASS |
| strain 5: ... recovers the true strains (µε) (absolute) | 5.4210109e-13 | 0 | 5.42e-13 | 1.0e-09 | PASS |
| strain 6: rectangular rosette Eq. 7.43 (JS) vs least squares (numpy), max \|Δ\| (µε) (absolute) | 5.4210109e-13 | 0 | 5.42e-13 | 1.0e-09 | PASS |
| strain 6: delta rosette formulas (JS) vs least squares, max \|Δ\| (µε) (absolute) | 4.3368087e-13 | 0 | 4.34e-13 | 1.0e-09 | PASS |
| strain 6: gages at 11.5°, 63.0°, 137.5°: Gaussian elimination (JS) vs least squares, max \|Δ\| (µε) (absolute) | 2.1684043e-13 | 0 | 2.17e-13 | 1.0e-09 | PASS |
| strain 6: readings of a rosette turned 3° with K_t = 2 %, JS vs Python forward model (µε) (absolute) | 2.1684043e-13 | 0 | 2.17e-13 | 1.0e-09 | PASS |
| strain 6: page's K_t correction and turn-back (closed form) vs Python least squares and tensor rotation (µε) (absolute) | 7.5894152e-13 | 0 | 7.59e-13 | 1.0e-09 | PASS |
| strain 6: ... recovers the true strains (µε) (absolute) | 5.4210109e-13 | 0 | 5.42e-13 | 1.0e-09 | PASS |
| strain 7: rectangular rosette Eq. 7.43 (JS) vs least squares (numpy), max \|Δ\| (µε) (absolute) | 2.1684043e-13 | 0 | 2.17e-13 | 1.0e-09 | PASS |
| strain 7: delta rosette formulas (JS) vs least squares, max \|Δ\| (µε) (absolute) | 5.4210109e-13 | 0 | 5.42e-13 | 1.0e-09 | PASS |
| strain 7: gages at 11.5°, 63.0°, 137.5°: Gaussian elimination (JS) vs least squares, max \|Δ\| (µε) (absolute) | 1.0842022e-13 | 0 | 1.08e-13 | 1.0e-09 | PASS |
| strain 7: readings of a rosette turned 3° with K_t = 2 %, JS vs Python forward model (µε) (absolute) | 1.1180835e-13 | 0 | 1.12e-13 | 1.0e-09 | PASS |
| strain 7: page's K_t correction and turn-back (closed form) vs Python least squares and tensor rotation (µε) (absolute) | 3.2526065e-13 | 0 | 3.25e-13 | 1.0e-09 | PASS |
| strain 7: ... recovers the true strains (µε) (absolute) | 1.6263033e-13 | 0 | 1.63e-13 | 1.0e-09 | PASS |
| strain 8: rectangular rosette Eq. 7.43 (JS) vs least squares (numpy), max \|Δ\| (µε) (absolute) | 1.6263033e-13 | 0 | 1.63e-13 | 1.0e-09 | PASS |
| strain 8: delta rosette formulas (JS) vs least squares, max \|Δ\| (µε) (absolute) | 4.3368087e-13 | 0 | 4.34e-13 | 1.0e-09 | PASS |
| strain 8: gages at 11.5°, 63.0°, 137.5°: Gaussian elimination (JS) vs least squares, max \|Δ\| (µε) (absolute) | 6.505213e-13 | 0 | 6.51e-13 | 1.0e-09 | PASS |
| strain 8: readings of a rosette turned 3° with K_t = 2 %, JS vs Python forward model (µε) (absolute) | 1.0842022e-13 | 0 | 1.08e-13 | 1.0e-09 | PASS |
| strain 8: page's K_t correction and turn-back (closed form) vs Python least squares and tensor rotation (µε) (absolute) | 8.6736174e-13 | 0 | 8.67e-13 | 1.0e-09 | PASS |
| strain 8: ... recovers the true strains (µε) (absolute) | 7.5894152e-13 | 0 | 7.59e-13 | 1.0e-09 | PASS |
| [partB, φ = 0°] σx, σθ, τxy: JS closed forms vs Python with Q by scipy dblquad, max \|Δ\|/scale (absolute) | 0 | 0 | 0.00e+00 | 1.0e-10 | PASS |
| [partBK, φ = 90°] σx, σθ, τxy: JS closed forms vs Python with Q by scipy dblquad, max \|Δ\|/scale (absolute) | 0 | 0 | 0.00e+00 | 1.0e-10 | PASS |
| [partBK, φ = 90°] Q of the wall from the top (JS closed form vs dblquad) | 9.7084819e-07 | 9.7084819e-07 | 2.18e-16 | 1.0e-10 | PASS |
| [partB, φ = -90°] σx, σθ, τxy: JS closed forms vs Python with Q by scipy dblquad, max \|Δ\|/scale (absolute) | 0 | 0 | 0.00e+00 | 1.0e-10 | PASS |
| [partB, φ = -90°] Q of the wall from the top (JS closed form vs dblquad) | -9.7084819e-07 | -9.7084819e-07 | 2.18e-16 | 1.0e-10 | PASS |
| [partB, φ = 37°] σx, σθ, τxy: JS closed forms vs Python with Q by scipy dblquad, max \|Δ\|/scale (absolute) | 8.7420359e-17 | 0 | 8.74e-17 | 1.0e-10 | PASS |
| [partB, φ = 37°] Q of the wall from the top (JS closed form vs dblquad) | 5.8427103e-07 | 5.8427103e-07 | 3.62e-16 | 1.0e-10 | PASS |
| [partC, φ = 0°] σx, σθ, τxy: JS closed forms vs Python with Q by scipy dblquad, max \|Δ\|/scale (absolute) | 1.0244548e-16 | 0 | 1.02e-16 | 1.0e-10 | PASS |
| [partC, φ = 0°] hoop stress at r_o: JS finite differences (1024) vs scipy solve_bvp | 36363646 | 36363636 | 2.62e-07 | 1.0e-05 | PASS |
| [partC, φ = 0°] axial stress: JS finite differences vs scipy solve_bvp | 18181820 | 18181818 | 8.55e-08 | 1.0e-05 | PASS |
| [partC, φ = 0°] hoop stress at r_o: JS Lamé closed form vs scipy solve_bvp | 36363636 | 36363636 | 6.15e-16 | 1.0e-08 | PASS |
| [partCc, φ = 0°] σx, σθ, τxy: JS closed forms vs Python with Q by scipy dblquad, max \|Δ\|/scale (absolute) | 0 | 0 | 0.00e+00 | 1.0e-10 | PASS |
| [partCc, φ = 0°] hoop stress at r_o: JS finite differences (1024) vs scipy solve_bvp | 36363646 | 36363636 | 2.62e-07 | 1.0e-05 | PASS |
| [partCc, φ = 0°] axial stress: JS finite differences vs scipy solve_bvp | 18181820 | 18181818 | 8.55e-08 | 1.0e-05 | PASS |
| [partCc, φ = 0°] hoop stress at r_o: JS Lamé closed form vs scipy solve_bvp | 36363636 | 36363636 | 6.15e-16 | 1.0e-08 | PASS |
| [partCcK, φ = 90°] σx, σθ, τxy: JS closed forms vs Python with Q by scipy dblquad, max \|Δ\|/scale (absolute) | 1.0244548e-16 | 0 | 1.02e-16 | 1.0e-10 | PASS |
| [partCcK, φ = 90°] Q of the wall from the top (JS closed form vs dblquad) | 9.7084819e-07 | 9.7084819e-07 | 2.18e-16 | 1.0e-10 | PASS |
| [partCcK, φ = 90°] hoop stress at r_o: JS finite differences (1024) vs scipy solve_bvp | 36363646 | 36363636 | 2.62e-07 | 1.0e-05 | PASS |
| [partCcK, φ = 90°] axial stress: JS finite differences vs scipy solve_bvp | 18181820 | 18181818 | 8.55e-08 | 1.0e-05 | PASS |
| [partCcK, φ = 90°] hoop stress at r_o: JS Lamé closed form vs scipy solve_bvp | 36363636 | 36363636 | 6.15e-16 | 1.0e-08 | PASS |
| [design, φ = 0°, inner surface] hoop stress at r_o: JS finite differences (1024) vs scipy solve_bvp | 64196603 | 64196573 | 4.72e-07 | 1.0e-05 | PASS |
| [design, φ = 0°, inner surface] axial stress: JS finite differences vs scipy solve_bvp | 32098291 | 32098286 | 1.48e-07 | 1.0e-05 | PASS |
| [design, φ = 0°, inner surface] hoop stress at r_o: JS Lamé closed form vs scipy solve_bvp | 64196573 | 64196573 | 3.48e-16 | 1.0e-08 | PASS |
| [design, φ = 0°, inner surface] principal stresses at the inner surface (σr = −p): JS vs numpy, max \|Δ\| (MPa) (absolute) | 1.4901161e-14 | 0 | 1.49e-14 | 1.0e-08 | PASS |
| [thick, φ = 0°] σx, σθ, τxy: JS closed forms vs Python with Q by scipy dblquad, max \|Δ\|/scale (absolute) | 1.8626451e-16 | 0 | 1.86e-16 | 1.0e-10 | PASS |
| [thick, φ = 0°] hoop stress at r_o: JS finite differences (1024) vs scipy solve_bvp | 20000102 | 20000000 | 5.12e-06 | 1.0e-05 | PASS |
| [thick, φ = 0°] axial stress: JS finite differences vs scipy solve_bvp | 10000012 | 10000000 | 1.21e-06 | 1.0e-05 | PASS |
| [thick, φ = 0°] hoop stress at r_o: JS Lamé closed form vs scipy solve_bvp | 20000000 | 20000000 | 3.73e-16 | 1.0e-08 | PASS |
| closure: E from Part A vs truth 68.9 GPa — \|Δ\| = 0.58 U — within 3u (99.7 %); students use 2u (absolute) | 68.507285 | 68.9 | 3.93e-01 | 1.0e+00 | PASS |
| closure: ν from Part A vs truth 0.33 — \|Δ\| = 0.16 U — within 3u (99.7 %); students use 2u (absolute) | 0.32927062 | 0.33 | 7.29e-04 | 6.7e-03 | PASS |
| closure: β_H vs truth 1.5° — \|Δ\| = 0.24 U — within 3u (99.7 %); students use 2u (absolute) | 1.450534 | 1.5 | 4.95e-02 | 3.0e-01 | PASS |
| closure: β_K vs truth −1.0° — \|Δ\| = 0.08 U — within 3u (99.7 %); students use 2u (absolute) | -1.019202 | -1 | 1.92e-02 | 3.5e-01 | PASS |
| closure: G (mean of H and K) vs truth E/2(1+ν) — \|Δ\| = 0.71 U — within 3u (99.7 %); students use 2u (absolute) | 25.671882 | 25.902256 | 2.30e-01 | 4.8e-01 | PASS |
| closure: K above mid-height vs truth 0.8° — \|Δ\| = 1.06 U — within 3u (99.7 %); students use 2u (absolute) | 0.60107799 | 0.8 | 1.99e-01 | 2.8e-01 | PASS |
| closure: ν from the pressure strains vs truth — \|Δ\| = 0.70 U — within 3u (99.7 %); students use 2u (absolute) | 0.33492246 | 0.33 | 4.92e-03 | 1.1e-02 | PASS |
| closure: hoop stress per MPa vs Lamé with the true tube — \|Δ\| = 0.07 U — within 3u (99.7 %); students use 2u (absolute) | 4.4885062 | 4.494402 | 5.90e-03 | 1.2e-01 | PASS |
| closure: σmax, Part B at H, vs the truth state — \|Δ\| = 0.07 U — within 3u (99.7 %); students use 2u (absolute) | 60.285899 | 60.352851 | 6.70e-02 | 1.4e+00 | PASS |
| closure: σmin, Part B at H, vs the truth state — \|Δ\| = 0.21 U — within 3u (99.7 %); students use 2u (absolute) | -7.3614771 | -7.4514791 | 9.00e-02 | 6.4e-01 | PASS |
| closure: σmax, Part B at K, vs the truth state — \|Δ\| = 0.50 U — within 3u (99.7 %); students use 2u (absolute) | 24.608923 | 24.894156 | 2.85e-01 | 8.6e-01 | PASS |
| closure: σmin, Part B at K, vs the truth state — \|Δ\| = 0.20 U — within 3u (99.7 %); students use 2u (absolute) | -24.070197 | -24.155375 | 8.52e-02 | 6.4e-01 | PASS |
| closure: σmax, Part C + lever at H, vs the truth state — \|Δ\| = 0.19 U — within 3u (99.7 %); students use 2u (absolute) | 80.691301 | 80.951683 | 2.60e-01 | 2.0e+00 | PASS |
| closure: σmin, Part C + lever at H, vs the truth state — \|Δ\| = 0.44 U — within 3u (99.7 %); students use 2u (absolute) | 25.713509 | 26.044799 | 3.31e-01 | 1.1e+00 | PASS |
| closure: absolute τmax at H, Part C + lever, vs the truth state — \|Δ\| = 0.19 U — within 3u (99.7 %); students use 2u (absolute) | 40.34565 | 40.475841 | 1.30e-01 | 1.0e+00 | PASS |
| closure: at H with pressure and the lever both in-plane principal stresses are tensile (σmin = 25.71 MPa) | True | True | 0.00e+00 | 0.0e+00 | PASS |
| closure: thin-wall hoop stress is rejected by the data (\|Δ\| > U) | True | True | 0.00e+00 | 0.0e+00 | PASS |
| D1: absolute τmax at the critical point of 44.45 × 4.78, page preset (inner surface, top) vs analysis | 61267842 | 61267842 | 7.30e-16 | 1.0e-12 | PASS |
| D1: the analysis's critical point for 44.45 × 4.78 is the inner surface, tension side | True | True | 0.00e+00 | 0.0e+00 | PASS |
| D1: the in-plane trap picks 50.8 × 3.18, lighter than 44.45 × 4.78 and unsafe by Tresca | True | True | 0.00e+00 | 0.0e+00 | PASS |

156 of 156 passed.

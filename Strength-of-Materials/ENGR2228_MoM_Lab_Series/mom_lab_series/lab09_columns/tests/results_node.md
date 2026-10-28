## Lab 9 model tests (exact page code)

| Test | Value | Reference | Rel. difference | Tolerance | Result |
|---|---:|---:|---:|---:|---|
| rectangle: I = bt³/12 vs midpoint integration of z² b dz | 5.4239475e-10 | 5.4239471e-10 | 6.25e-8 | 1.0e-7 | PASS |
| tube: A = π(Do² − Di²)/4 vs polar integration | 0.00032060738 | 0.00032060738 | 5.07e-16 | 1.0e-7 | PASS |
| tube: I = π(Do⁴ − Di⁴)/64 vs polar integration of r² sin²θ | 1.5341644e-7 | 1.5341644e-7 | 4.45e-11 | 1.0e-7 | PASS |
| solid round: r = d/4 | 0.0031750000 | 0.0031750000 | 0.00e+0 | 1.0e-15 | PASS |
| Beer Eq. 10.20: tan z = z at z = 4.4934 | 4.4934095 | 4.4934095 | 1.98e-16 | 1.0e-13 | PASS |
| Beer Eq. 10.21: P_cr = 20.19 EI/L² for a fixed-pinned column (z² = 20.19) | 20.190729 | 20.190000 | 3.61e-5 | 2.0e-4 | PASS |
| Beer Fig. 10.18: K = π/4.4934 = 0.699 for fixed-pinned | 0.69915566 | 0.69900000 | 2.23e-4 | 3.0e-4 | PASS |
| pinned, L = 0.3 m: Euler with K = 1.0000 vs finite elements (N = 64) | 4098.1886 | 4098.1885 | 8.06e-9 | 2.0e-7 | PASS |
| pinned, L = 0.6005 m: Euler with K = 1.0000 vs finite elements (N = 64) | 1022.8417 | 1022.8417 | 8.12e-9 | 2.0e-7 | PASS |
| pinned, L = 1.7 m: Euler with K = 1.0000 vs finite elements (N = 64) | 127.62525 | 127.62525 | 8.06e-9 | 2.0e-7 | PASS |
| fixed-pinned, L = 0.3 m: Euler with K = 0.6992 vs finite elements (N = 64) | 8383.8634 | 8383.8631 | 3.37e-8 | 2.0e-7 | PASS |
| fixed-pinned, L = 0.6005 m: Euler with K = 0.6992 vs finite elements (N = 64) | 2092.4769 | 2092.4769 | 3.38e-8 | 2.0e-7 | PASS |
| fixed-pinned, L = 1.7 m: Euler with K = 0.6992 vs finite elements (N = 64) | 261.08917 | 261.08916 | 3.37e-8 | 2.0e-7 | PASS |
| fixed-fixed, L = 0.3 m: Euler with K = 0.5000 vs finite elements (N = 64) | 16392.756 | 16392.754 | 1.29e-7 | 2.0e-7 | PASS |
| fixed-fixed, L = 0.6005 m: Euler with K = 0.5000 vs finite elements (N = 64) | 4091.3673 | 4091.3667 | 1.29e-7 | 2.0e-7 | PASS |
| fixed-fixed, L = 1.7 m: Euler with K = 0.5000 vs finite elements (N = 64) | 510.50106 | 510.50099 | 1.29e-7 | 2.0e-7 | PASS |
| free-fixed, L = 0.3 m: Euler with K = 2.0000 vs finite elements (N = 64) | 1024.5471 | 1024.5471 | 5.07e-10 | 2.0e-7 | PASS |
| free-fixed, L = 0.6005 m: Euler with K = 2.0000 vs finite elements (N = 64) | 255.71042 | 255.71042 | 5.03e-10 | 2.0e-7 | PASS |
| free-fixed, L = 1.7 m: Euler with K = 2.0000 vs finite elements (N = 64) | 31.906312 | 31.906312 | 5.04e-10 | 2.0e-7 | PASS |
| springs, k = 5 N·m/rad: characteristic equation vs finite elements (N = 64) | 1055.8777 | 1055.8777 | 8.31e-9 | 2.0e-7 | PASS |
| spring-pin, k = 5 N·m/rad: characteristic equation vs finite elements (N = 64) | 915.90454 | 915.90454 | 8.20e-9 | 2.0e-7 | PASS |
| springs, k = 300 N·m/rad: characteristic equation vs finite elements (N = 64) | 2319.7262 | 2319.7262 | 2.70e-8 | 2.0e-7 | PASS |
| spring-pin, k = 300 N·m/rad: characteristic equation vs finite elements (N = 64) | 1400.6688 | 1400.6688 | 1.60e-8 | 2.0e-7 | PASS |
| springs, k = 2800 N·m/rad: characteristic equation vs finite elements (N = 64) | 3752.4022 | 3752.4018 | 9.94e-8 | 2.0e-7 | PASS |
| spring-pin, k = 2800 N·m/rad: characteristic equation vs finite elements (N = 64) | 1769.3089 | 1769.3089 | 2.99e-8 | 2.0e-7 | PASS |
| springs, k = 100000 N·m/rad: characteristic equation vs finite elements (N = 64) | 4081.2016 | 4081.2010 | 1.28e-7 | 2.0e-7 | PASS |
| spring-pin, k = 100000 N·m/rad: characteristic equation vs finite elements (N = 64) | 1840.0093 | 1840.0092 | 3.36e-8 | 2.0e-7 | PASS |
| springs, k = 100000000 N·m/rad: characteristic equation vs finite elements (N = 64) | 4091.3571 | 4091.3566 | 1.29e-7 | 2.0e-7 | PASS |
| spring-pin, k = 100000000 N·m/rad: characteristic equation vs finite elements (N = 64) | 1842.1553 | 1842.1553 | 3.37e-8 | 2.0e-7 | PASS |
| spring ends: residual of tan x + 2x EI/(kL) at the root (absolute difference) | 2.7755576e-16 | 0.0000000 | 2.78e-16 | 1.0e-12 | PASS |
| spring + pin: residual of tan z − z/(1 + z² EI/(kL)) at the root (absolute difference) | -1.3766766e-14 | 0.0000000 | 1.38e-14 | 1.0e-11 | PASS |
| spring ends: k → 0 gives the pinned load | 1022.8417 | 1022.8417 | 6.51e-12 | 1.0e-9 | PASS |
| spring ends: k = 10¹⁴ N·m/rad gives the fixed-fixed load | 4091.3667 | 4091.3667 | 2.49e-12 | 1.0e-9 | PASS |
| spring + pin: k = 10¹⁴ gives Beer Eq. 10.21 | 2092.4769 | 2092.4769 | 1.25e-12 | 1.0e-9 | PASS |
| k from P (inverse of the symmetric characteristic equation) | 2800.0000 | 2800.0000 | 1.95e-15 | 1.0e-10 | PASS |
| kL/EI = 1 already gives K = 0.855 (between 0.5 and 1) | true | true | 0.00e+0 | 0.0e+0 | PASS |
| pinned: closed-form mode shape vs finite-element eigenvector (least-squares scaled), max difference (absolute difference) | 1.6322532e-10 | 0.0000000 | 1.63e-10 | 1.0e-5 | PASS |
| fixed-fixed: closed-form mode shape vs finite-element eigenvector (least-squares scaled), max difference (absolute difference) | 8.3838992e-8 | 0.0000000 | 8.38e-8 | 1.0e-5 | PASS |
| fixed-pinned: closed-form mode shape vs finite-element eigenvector (least-squares scaled), max difference (absolute difference) | 9.6824768e-9 | 0.0000000 | 9.68e-9 | 1.0e-5 | PASS |
| free-fixed: closed-form mode shape vs finite-element eigenvector (least-squares scaled), max difference (absolute difference) | 1.2652590e-10 | 0.0000000 | 1.27e-10 | 1.0e-5 | PASS |
| springs: closed-form mode shape vs finite-element eigenvector (least-squares scaled), max difference (absolute difference) | 5.1286208e-8 | 0.0000000 | 5.13e-8 | 1.0e-5 | PASS |
| spring-pin: closed-form mode shape vs finite-element eigenvector (least-squares scaled), max difference (absolute difference) | 2.0661362e-8 | 0.0000000 | 2.07e-8 | 1.0e-5 | PASS |
| Hermite elements: P_cr error falls as N⁻⁴ (fitted order, N = 4 to 16) | 3.9788020 | 4.0000000 | 5.30e-3 | 3.0e-2 | PASS |
| Hermite elements with spring ends: order 4 too (N = 8 to 32) | 3.9775716 | 4.0000000 | 5.61e-3 | 3.0e-2 | PASS |
| one fixed-fixed element has no free DOF: P is NaN (the page asks for N ≥ 2) | true | true | 0.00e+0 | 0.0e+0 | PASS |
| P = 0.3 P_cr, δ0 = 0.4 mm, e = 0 mm: mid-length deflection, closed form vs finite differences (N = 4000) | 0.00017142858 | 0.00017142857 | 7.32e-8 | 3.0e-6 | PASS |
| P = 0.3 P_cr, δ0 = 0.4 mm, e = 0 mm: mid-length deflection, closed form vs finite elements (N = 64) | 0.00017142857 | 0.00017142857 | 1.16e-8 | 3.0e-7 | PASS |
| P = 0.3 P_cr, δ0 = 0.4 mm, e = 0 mm: curvature at mid-length × EI vs M = −P(e + δ0 + δ) (Beer Eq. 10.22) | -0.31230561 | -0.31224294 | 2.01e-4 | 2.0e-3 | PASS |
| P = 0.3 P_cr, δ0 = 0.4 mm, e = 0 mm: at a fixed load the responses to bow and eccentricity superpose (max \|Δ\|, m) (absolute difference) | 0.0000000 | 0.0000000 | 0.00e+0 | 1.0e-15 | PASS |
| P = 0.7 P_cr, δ0 = 0.4 mm, e = 1 mm: mid-length deflection, closed form vs finite differences (N = 4000) | 0.0038739405 | 0.0038739400 | 1.33e-7 | 3.0e-6 | PASS |
| P = 0.7 P_cr, δ0 = 0.4 mm, e = 1 mm: mid-length deflection, closed form vs finite elements (N = 64) | 0.0038739399 | 0.0038739400 | 1.65e-8 | 3.0e-7 | PASS |
| P = 0.7 P_cr, δ0 = 0.4 mm, e = 1 mm: curvature at mid-length × EI vs M = −P(e + δ0 + δ) (Beer Eq. 10.22) | -6.7252785 | -6.7242312 | 1.56e-4 | 2.0e-3 | PASS |
| P = 0.7 P_cr, δ0 = 0.4 mm, e = 1 mm: at a fixed load the responses to bow and eccentricity superpose (max \|Δ\|, m) (absolute difference) | 0.0000000 | 0.0000000 | 0.00e+0 | 1.0e-15 | PASS |
| P = 0.9 P_cr, δ0 = 0 mm, e = 2 mm: mid-length deflection, closed form vs finite differences (N = 4000) | 0.022838307 | 0.022838296 | 4.64e-7 | 3.0e-6 | PASS |
| P = 0.9 P_cr, δ0 = 0 mm, e = 2 mm: mid-length deflection, closed form vs finite elements (N = 64) | 0.022838295 | 0.022838296 | 6.57e-8 | 3.0e-7 | PASS |
| P = 0.9 P_cr, δ0 = 0 mm, e = 2 mm: curvature at mid-length × EI vs M = −P(e + δ0 + δ) (Beer Eq. 10.22) | -40.724162 | -40.716808 | 1.81e-4 | 2.0e-3 | PASS |
| P = 0.9 P_cr, δ0 = 0 mm, e = 2 mm: at a fixed load the responses to bow and eccentricity superpose (max \|Δ\|, m) (absolute difference) | 0.0000000 | 0.0000000 | 0.00e+0 | 1.0e-15 | PASS |
| P = 0.95 P_cr, δ0 = 0.25999999999999995 mm, e = 0.08 mm: mid-length deflection, closed form vs finite differences (N = 4000) | 0.0068719293 | 0.0068719224 | 1.01e-6 | 3.0e-6 | PASS |
| P = 0.95 P_cr, δ0 = 0.25999999999999995 mm, e = 0.08 mm: mid-length deflection, closed form vs finite elements (N = 64) | 0.0068719213 | 0.0068719224 | 1.57e-7 | 3.0e-7 | PASS |
| P = 0.95 P_cr, δ0 = 0.25999999999999995 mm, e = 0.08 mm: curvature at mid-length × EI vs M = −P(e + δ0 + δ) (Beer Eq. 10.22) | -12.481591 | -12.479123 | 1.98e-4 | 2.0e-3 | PASS |
| P = 0.95 P_cr, δ0 = 0.25999999999999995 mm, e = 0.08 mm: at a fixed load the responses to bow and eccentricity superpose (max \|Δ\|, m) (absolute difference) | 0.0000000 | 0.0000000 | 0.00e+0 | 1.0e-15 | PASS |
| Eq. 10.31 equals Eq. 10.26 at x = L/2 (P = 0.2 P_cr) | 0.00062040353 | 0.00062040353 | 0.00e+0 | 1.0e-13 | PASS |
| Eq. 10.31 equals Eq. 10.26 at x = L/2 (P = 0.6 P_cr) | 0.0037684868 | 0.0037684868 | 2.30e-16 | 1.0e-13 | PASS |
| Eq. 10.31 equals Eq. 10.26 at x = L/2 (P = 0.9 P_cr) | 0.022838296 | 0.022838296 | 1.52e-16 | 1.0e-13 | PASS |
| Eq. 10.35 equals Eq. 10.33, P/A [1 + (y_max + e)c/r²] (P = 0.2 P_cr) | 7844520.3 | 7844520.3 | 0.00e+0 | 1.0e-13 | PASS |
| Eq. 10.35 equals Eq. 10.33, P/A [1 + (y_max + e)c/r²] (P = 0.6 P_cr) | 43672432 | 43672432 | 0.00e+0 | 1.0e-13 | PASS |
| Eq. 10.35 equals Eq. 10.33, P/A [1 + (y_max + e)c/r²] (P = 0.9 P_cr) | 2.4849830e+8 | 2.4849830e+8 | 1.20e-16 | 1.0e-13 | PASS |
| superposition fails in P: doubling 0.33 → 0.66 P_cr multiplies y_max by 3.982 (> 2) | true | true | 0.00e+0 | 0.0e+0 | PASS |
| first yield, e = 0.5 mm: secant formula Eq. 10.36 vs finite differences (N = 4000) | 1775.8193 | 1775.8194 | 4.90e-8 | 2.0e-6 | PASS |
| first yield, e = 0.5 mm: σ_max(P_Y) = σ_Y | 2.7370000e+8 | 2.7370000e+8 | 1.87e-12 | 1.0e-10 | PASS |
| first yield, e = 1 mm: secant formula Eq. 10.36 vs finite differences (N = 4000) | 1733.0281 | 1733.0282 | 4.62e-8 | 2.0e-6 | PASS |
| first yield, e = 1 mm: σ_max(P_Y) = σ_Y | 2.7370000e+8 | 2.7370000e+8 | 9.85e-13 | 1.0e-10 | PASS |
| first yield, e = 2 mm: secant formula Eq. 10.36 vs finite differences (N = 4000) | 1654.7288 | 1654.7289 | 4.22e-8 | 2.0e-6 | PASS |
| first yield, e = 2 mm: σ_max(P_Y) = σ_Y | 2.7370000e+8 | 2.7370000e+8 | 5.93e-13 | 1.0e-10 | PASS |
| finite differences: error falls as N⁻² (fitted order) | 2.0041135 | 2.0000000 | 2.06e-3 | 2.0e-2 | PASS |
| Southwell on an exact half-sine bow recovers P_cr | 1821.4171 | 1821.4171 | 1.25e-16 | 1.0e-12 | PASS |
| Southwell on an exact half-sine bow recovers δ0 | 0.00046000000 | 0.00046000000 | 8.25e-16 | 1.0e-10 | PASS |
| Southwell on a pure eccentric load: P_cr within 0.5 % (the secant curve is nearly a Southwell line) | 1818.7861 | 1821.4171 | 1.44e-3 | 5.0e-3 | PASS |
| Southwell on a pure eccentric load: the intercept is about (4/π) e | 0.0012520350 | 0.0012732395 | 1.67e-2 | 3.0e-2 | PASS |
| fixed-fixed: Southwell on mid-length readings (half-sine bow, clamps grip the initial slope) vs the eigenvalue — a half sine is not the clamped mode shape: higher modes bias the fit slightly | 4100.3170 | 4098.1891 | 5.19e-4 | 5.0e-3 | PASS |
| fixed-pinned: Southwell on mid-length readings (half-sine bow, clamps grip the initial slope) vs the eigenvalue — a half sine is not the clamped mode shape: higher modes bias the fit slightly | 2102.7333 | 2095.9658 | 3.23e-3 | 5.0e-3 | PASS |
| springs: Southwell on mid-length readings (half-sine bow, clamps grip the initial slope) vs the eigenvalue — a half sine is not the clamped mode shape: higher modes bias the fit slightly | 3759.8601 | 3758.3967 | 3.89e-4 | 5.0e-3 | PASS |
| sample data A300: page Southwell fit vs lab09_analysis.py | 4103.3305 | 4103.3305 | 2.22e-16 | 1.0e-9 | PASS |
| sample data A450: page Southwell fit vs lab09_analysis.py | 1828.8061 | 1828.8061 | 2.49e-16 | 1.0e-9 | PASS |
| sample data A600: page Southwell fit vs lab09_analysis.py | 1026.1354 | 1026.1354 | 0.00e+0 | 1.0e-9 | PASS |
| sample data Bff: page Southwell fit vs lab09_analysis.py | 3730.0737 | 3730.0737 | 2.44e-16 | 1.0e-9 | PASS |
| sample data Bfp: page Southwell fit vs lab09_analysis.py | 1765.0465 | 1765.0465 | 6.44e-16 | 1.0e-9 | PASS |
| Carlson R_F: K(m = 0.5) = 1.854074677301372 | 1.8540747 | 1.8540747 | 2.40e-16 | 1.0e-14 | PASS |
| Carlson R_F: K(0) = π/2 | 1.5707963 | 1.5707963 | 0.00e+0 | 1.0e-15 | PASS |
| elastica at 1.005 P_cr: δ/L by elliptic integrals vs RK4 shooting (400 steps) | 0.063286059 | 0.063286059 | 3.93e-10 | 2.0e-9 | PASS |
| elastica at 1.005 P_cr: end slope, elliptic vs shooting | 0.19964685 | 0.19964685 | 3.95e-10 | 2.0e-9 | PASS |
| elastica at 1.02 P_cr: δ/L by elliptic integrals vs RK4 shooting (400 steps) | 0.12436536 | 0.12436536 | 9.60e-11 | 2.0e-9 | PASS |
| elastica at 1.02 P_cr: end slope, elliptic vs shooting | 0.39719891 | 0.39719891 | 9.73e-11 | 2.0e-9 | PASS |
| elastica at 1.2 P_cr: δ/L by elliptic integrals vs RK4 shooting (400 steps) | 0.32439181 | 0.32439181 | 7.64e-12 | 2.0e-9 | PASS |
| elastica at 1.2 P_cr: end slope, elliptic vs shooting | 1.1844002 | 1.1844002 | 9.04e-12 | 2.0e-9 | PASS |
| elastica at 1.5 P_cr: δ/L by elliptic integrals vs RK4 shooting (400 steps) | 0.39428790 | 0.39428790 | 2.49e-12 | 2.0e-9 | PASS |
| elastica at 1.5 P_cr: end slope, elliptic vs shooting | 1.7221418 | 1.7221418 | 4.45e-12 | 2.0e-9 | PASS |
| elastica at 2.5 P_cr: δ/L by elliptic integrals vs RK4 shooting (400 steps) | 0.37720270 | 0.37720270 | 4.26e-13 | 2.0e-9 | PASS |
| elastica at 2.5 P_cr: end slope, elliptic vs shooting | 2.4269573 | 2.4269573 | 5.38e-12 | 2.0e-9 | PASS |
| elastica, small deflection: P/P_cr − 1 ≈ (π²/8)(δ/L)² (leading term, at 1.0001 P_cr) | 0.00010000000 | 0.000099976254 | 2.38e-4 | 5.0e-4 | PASS |
| Ramberg–Osgood: stress → strain → stress round trip at 50 MPa | 50000000 | 50000000 | 0.00e+0 | 1.0e-12 | PASS |
| Ramberg–Osgood: stress → strain → stress round trip at 200 MPa | 2.0000000e+8 | 2.0000000e+8 | 0.00e+0 | 1.0e-12 | PASS |
| Ramberg–Osgood: stress → strain → stress round trip at 260 MPa | 2.6000000e+8 | 2.6000000e+8 | 0.00e+0 | 1.0e-12 | PASS |
| Ramberg–Osgood: stress → strain → stress round trip at 300 MPa | 3.0000000e+8 | 3.0000000e+8 | 1.99e-16 | 1.0e-12 | PASS |
| tangent modulus at 100 MPa: formula vs central difference of the curve | 6.8899941e+10 | 6.8899941e+10 | 7.89e-12 | 1.0e-7 | PASS |
| tangent modulus at 220 MPa: formula vs central difference of the curve | 5.4687316e+10 | 5.4687316e+10 | 1.31e-11 | 1.0e-7 | PASS |
| tangent modulus at 270 MPa: formula vs central difference of the curve | 8.7391142e+9 | 8.7391142e+9 | 6.13e-11 | 1.0e-7 | PASS |
| tangent modulus stays finite for a sharp knee (m = 60, steel): no overflow | true | true | 0.00e+0 | 0.0e+0 | PASS |
| tangent-modulus column curve at L/r = 35: σ = π²E_t/(L/r)² inverted by the closed form π√(E_t/σ) | 35.000000 | 35.000000 | 1.56e-14 | 1.0e-10 | PASS |
| L/r = 35: tangent-modulus load vs finite-element eigenvalue with E_t I | 39239.484 | 39239.479 | 1.29e-7 | 2.0e-6 | PASS |
| L/r = 35: reduced-modulus stress ≥ tangent-modulus stress | true | true | 0.00e+0 | 0.0e+0 | PASS |
| tangent-modulus column curve at L/r = 49.1: σ = π²E_t/(L/r)² inverted by the closed form π√(E_t/σ) | 49.100000 | 49.100000 | 1.16e-15 | 1.0e-10 | PASS |
| L/r = 49.1: tangent-modulus load vs finite-element eigenvalue with E_t I | 35653.756 | 35653.751 | 1.29e-7 | 2.0e-6 | PASS |
| L/r = 49.1: reduced-modulus stress ≥ tangent-modulus stress | true | true | 0.00e+0 | 0.0e+0 | PASS |
| tangent-modulus column curve at L/r = 60: σ = π²E_t/(L/r)² inverted by the closed form π√(E_t/σ) | 60.000000 | 60.000000 | 5.09e-15 | 1.0e-10 | PASS |
| L/r = 60: tangent-modulus load vs finite-element eigenvalue with E_t I | 29973.675 | 29973.671 | 1.29e-7 | 2.0e-6 | PASS |
| L/r = 60: reduced-modulus stress ≥ tangent-modulus stress | true | true | 0.00e+0 | 0.0e+0 | PASS |
| tangent-modulus column curve at L/r = 80: σ = π²E_t/(L/r)² inverted by the closed form π√(E_t/σ) | 80.000000 | 80.000000 | 3.20e-15 | 1.0e-10 | PASS |
| L/r = 80: tangent-modulus load vs finite-element eigenvalue with E_t I | 17150.916 | 17150.914 | 1.29e-7 | 2.0e-6 | PASS |
| L/r = 80: reduced-modulus stress ≥ tangent-modulus stress | true | true | 0.00e+0 | 0.0e+0 | PASS |
| tangent-modulus curve joins Euler for slender columns (L/r = 200) | 17000394 | 17000394 | 4.82e-15 | 1.0e-9 | PASS |
| fiber section: Σ dA z² = I (1 − 1/n_f²) for n_f = 8 (midpoint rule) | 5.3391983e-10 | 5.3391983e-10 | 0.00e+0 | 1.0e-12 | PASS |
| fiber section: Σ dA z² = I (1 − 1/n_f²) for n_f = 40 (midpoint rule) | 5.4205575e-10 | 5.4205575e-10 | 3.82e-16 | 1.0e-12 | PASS |
| fiber section: Σ dA z² = I (1 − 1/n_f²) for n_f = 200 (midpoint rule) | 5.4238119e-10 | 5.4238119e-10 | 1.91e-16 | 1.0e-12 | PASS |
| fiber model with an elastic material vs the assumed-mode closed form P = P_cr δ/(δ + δ0 + e), max relative difference (absolute difference) | 2.3314684e-15 | 0.0000000 | 2.33e-15 | 1.0e-9 | PASS |
| nearly perfect inelastic column: tangent-modulus load 35.65 kN ≤ fiber maximum 35.98 kN ≤ reduced-modulus load 36.94 kN (Shanley) | true | true | 0.00e+0 | 0.0e+0 | PASS |
| Part D: page fiber model (JS) vs the truth model (Python, scipy brentq) with identical inputs, maximum load | 31094.263 | 31094.263 | 9.36e-16 | 1.0e-7 | PASS |
| AA 6061-T6, L/r = 10: 146.3 MPa (Eq. 10.43b) | 1.4630000e+8 | 1.4630000e+8 | 0.00e+0 | 1.0e-12 | PASS |
| AA 6061-T6, L/r = 30: 173.9 − 1.602(30) + 0.00323(30)² MPa (Eq. 10.44b) | 1.2874700e+8 | 1.2874700e+8 | 0.00e+0 | 1.0e-12 | PASS |
| AA 6061-T6, L/r = 100: 356 000/100² MPa (Eq. 10.45b) | 35600000 | 35600000 | 0.00e+0 | 1.0e-12 | PASS |
| AA 6061-T6 Euler branch = Euler with E = 68.9 GPa divided by 1.91 | 1.9101566 | 1.9100000 | 8.20e-5 | 2.0e-3 | PASS |
| AISC junction (Eq. 10.41): Eqs. 10.38 and 10.40 meet within 0.5 % | 97580457 | 97543320 | 3.81e-4 | 5.0e-3 | PASS |
| AISC: σ_all = σ_cr/1.67 (Eq. 10.42) | 1.7807357e+8 | 1.7807357e+8 | 0.00e+0 | 1.0e-14 | PASS |
| preset euler450: finite P_cr (1.821 kN) and K (1.0000) | true | true | 0.00e+0 | 0.0e+0 | PASS |
| preset endsFF: finite P_cr (4.091 kN) and K (0.5000) | true | true | 0.00e+0 | 0.0e+0 | PASS |
| preset springsB: finite P_cr (3.752 kN) and K (0.5221) | true | true | 0.00e+0 | 0.0e+0 | PASS |
| preset flagpole: finite P_cr (23.027 kN) and K (2.0000) | true | true | 0.00e+0 | 0.0e+0 | PASS |
| preset partA300: finite P_cr (4.098 kN) and K (1.0000) | true | true | 0.00e+0 | 0.0e+0 | PASS |
| preset partA450: finite P_cr (1.821 kN) and K (1.0000) | true | true | 0.00e+0 | 0.0e+0 | PASS |
| preset partA600: finite P_cr (1.023 kN) and K (1.0000) | true | true | 0.00e+0 | 0.0e+0 | PASS |
| preset partBff: finite P_cr (4.091 kN) and K (0.5000) | true | true | 0.00e+0 | 0.0e+0 | PASS |
| preset partBfp: finite P_cr (1.842 kN) and K (0.6992) | true | true | 0.00e+0 | 0.0e+0 | PASS |
| preset partC1: finite P_cr (1.821 kN) and K (1.0000) | true | true | 0.00e+0 | 0.0e+0 | PASS |
| preset partC2: finite P_cr (1.821 kN) and K (1.0000) | true | true | 0.00e+0 | 0.0e+0 | PASS |
| preset partD: finite P_cr (45.535 kN) and K (1.0000) | true | true | 0.00e+0 | 0.0e+0 | PASS |
| preset elastica: finite P_cr (1.821 kN) and K (1.0000) | true | true | 0.00e+0 | 0.0e+0 | PASS |
| preset steel: finite P_cr (47.584 kN) and K (1.0000) | true | true | 0.00e+0 | 0.0e+0 | PASS |
| preset design: finite P_cr (26.081 kN) and K (1.0000) | true | true | 0.00e+0 | 0.0e+0 | PASS |
| preset designTrap: finite P_cr (34.597 kN) and K (0.5000) | true | true | 0.00e+0 | 0.0e+0 | PASS |
| end condition "fixed-pinned": top end A pinned, bottom end B fixed (as in Lab Part B) | true | true | 0.00e+0 | 0.0e+0 | PASS |
| D1 preset: 12 kN on the 63.5 × 1.65 mm tube, pinned, 2.0 m | 12000.000 | 12000.000 | 0.00e+0 | 0.0e+0 | PASS |
| units: 1 N·m/rad in lb·in/rad | 8.8507458 | 8.8507458 | 3.70e-11 | 1.0e-9 | PASS |
| units: 1000 N in lbf | 224.80894 | 224.80894 | 1.29e-12 | 1.0e-9 | PASS |
| units: 450 mm | 450.00000 | 450.00000 | 0.00e+0 | 1.0e-15 | PASS |

154 of 154 passed.

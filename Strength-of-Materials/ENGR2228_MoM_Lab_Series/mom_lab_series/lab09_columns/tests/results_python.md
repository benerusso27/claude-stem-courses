## Lab 9 — independent checks (Python/scipy) and data-pipeline closure

| Test | Value | Reference | Rel. difference | Tolerance | Result |
|---|---:|---:|---:|---:|---|
| pinned, L = 0.45 m: page closed form vs Python closed form (scipy brentq) | 1821.4171 | 1821.4171 | 0.00e+00 | 1.0e-12 | PASS |
| pinned, L = 0.45 m: page closed form vs scipy eigh on 128 Hermite elements — eigh round-off at 128 elements | 1821.4171 | 1821.4171 | 2.19e-09 | 5.0e-08 | PASS |
| pinned, L = 0.45 m: page inverse iteration (64 elements) vs scipy eigh (128 elements) | 1821.4171 | 1821.4171 | 5.92e-09 | 2.0e-07 | PASS |
| fixed-pinned, L = 0.64 m: page closed form vs Python closed form (scipy brentq) | 1842.1574 | 1842.1574 | 0.00e+00 | 1.0e-12 | PASS |
| fixed-pinned, L = 0.64 m: page closed form vs scipy eigh on 128 Hermite elements — eigh round-off at 128 elements | 1842.1574 | 1842.1574 | 1.69e-09 | 5.0e-08 | PASS |
| fixed-pinned, L = 0.64 m: page inverse iteration (64 elements) vs scipy eigh (128 elements) | 1842.1575 | 1842.1574 | 3.20e-08 | 2.0e-07 | PASS |
| fixed-fixed, L = 0.6005 m: page closed form vs Python closed form (scipy brentq) | 4091.3667 | 4091.3667 | 0.00e+00 | 1.0e-12 | PASS |
| fixed-fixed, L = 0.6005 m: page closed form vs scipy eigh on 128 Hermite elements — eigh round-off at 128 elements | 4091.3667 | 4091.3668 | 8.13e-09 | 5.0e-08 | PASS |
| fixed-fixed, L = 0.6005 m: page inverse iteration (64 elements) vs scipy eigh (128 elements) | 4091.3673 | 4091.3668 | 1.21e-07 | 2.0e-07 | PASS |
| free-fixed, L = 1.0 m: page closed form vs Python closed form (scipy brentq) | 92.209242 | 92.209242 | 0.00e+00 | 1.0e-12 | PASS |
| free-fixed, L = 1.0 m: page closed form vs scipy eigh on 128 Hermite elements — eigh round-off at 128 elements | 92.209242 | 92.20924 | 1.97e-08 | 5.0e-08 | PASS |
| free-fixed, L = 1.0 m: page inverse iteration (64 elements) vs scipy eigh (128 elements) | 92.209242 | 92.20924 | 2.02e-08 | 2.0e-07 | PASS |
| springs, L = 0.6005 m, k = 2800 N·m/rad: page closed form vs Python closed form (scipy brentq) | 3752.4018 | 3752.4018 | 0.00e+00 | 1.0e-12 | PASS |
| springs, L = 0.6005 m, k = 2800 N·m/rad: page closed form vs scipy eigh on 128 Hermite elements — eigh round-off at 128 elements | 3752.4018 | 3752.4019 | 6.70e-09 | 5.0e-08 | PASS |
| springs, L = 0.6005 m, k = 2800 N·m/rad: page inverse iteration (64 elements) vs scipy eigh (128 elements) | 3752.4022 | 3752.4019 | 9.27e-08 | 2.0e-07 | PASS |
| spring-pin, L = 0.64 m, k = 2800 N·m/rad: page closed form vs Python closed form (scipy brentq) | 1769.3089 | 1769.3089 | 1.29e-15 | 1.0e-12 | PASS |
| spring-pin, L = 0.64 m, k = 2800 N·m/rad: page closed form vs scipy eigh on 128 Hermite elements — eigh round-off at 128 elements | 1769.3089 | 1769.3089 | 1.42e-09 | 5.0e-08 | PASS |
| spring-pin, L = 0.64 m, k = 2800 N·m/rad: page inverse iteration (64 elements) vs scipy eigh (128 elements) | 1769.3089 | 1769.3089 | 2.85e-08 | 2.0e-07 | PASS |
| springs, L = 0.3 m, k = 50 N·m/rad: page closed form vs Python closed form (scipy brentq) | 4738.5141 | 4738.5141 | 7.68e-16 | 1.0e-12 | PASS |
| springs, L = 0.3 m, k = 50 N·m/rad: page closed form vs scipy eigh on 128 Hermite elements — eigh round-off at 128 elements | 4738.5141 | 4738.5141 | 1.38e-09 | 5.0e-08 | PASS |
| springs, L = 0.3 m, k = 50 N·m/rad: page inverse iteration (64 elements) vs scipy eigh (128 elements) | 4738.5141 | 4738.5141 | 8.06e-09 | 2.0e-07 | PASS |
| spring-pin, L = 1.2 m, k = 100000 N·m/rad: page closed form vs Python closed form (scipy brentq) | 523.66533 | 523.66533 | 2.17e-16 | 1.0e-12 | PASS |
| spring-pin, L = 1.2 m, k = 100000 N·m/rad: page closed form vs scipy eigh on 128 Hermite elements — eigh round-off at 128 elements | 523.66533 | 523.66533 | 2.00e-09 | 5.0e-08 | PASS |
| spring-pin, L = 1.2 m, k = 100000 N·m/rad: page inverse iteration (64 elements) vs scipy eigh (128 elements) | 523.66535 | 523.66533 | 3.17e-08 | 2.0e-07 | PASS |
| P = 0.3 P_cr, δ0 = 0.4 mm, e = 0 mm: page closed form (bow + Eq. 10.26) vs scipy banded finite differences (N = 4000 and 8000, Richardson), worst of 4 points — round-off floor of the 8000-interval solve | 1 | 1 | 1.26e-09 | 5.0e-08 | PASS |
| P = 0.3 P_cr, δ0 = 0.4 mm, e = 0 mm: page finite elements (64) vs Python finite elements (128, numpy solve), mid-length — discretization, amplified near P_cr | 0.00017142857 | 0.00017142857 | 1.33e-08 | 5.0e-07 | PASS |
| P = 0.7 P_cr, δ0 = 0.46 mm, e = 1 mm: page closed form (bow + Eq. 10.26) vs scipy banded finite differences (N = 4000 and 8000, Richardson), worst of 4 points — round-off floor of the 8000-interval solve | 1 | 1 | 2.10e-09 | 5.0e-08 | PASS |
| P = 0.7 P_cr, δ0 = 0.46 mm, e = 1 mm: page finite elements (64) vs Python finite elements (128, numpy solve), mid-length — discretization, amplified near P_cr | 0.0040139399 | 0.00401394 | 1.76e-08 | 5.0e-07 | PASS |
| P = 0.7 P_cr, δ0 = 0.46 mm, e = 1 mm: page Eq. 10.35 vs Python Eq. 10.33 with Eq. 10.31 | 37309002 | 37309002 | 2.00e-16 | 1.0e-12 | PASS |
| P = 0.9 P_cr, δ0 = 0 mm, e = 2 mm: page closed form (bow + Eq. 10.26) vs scipy banded finite differences (N = 4000 and 8000, Richardson), worst of 4 points — round-off floor of the 8000-interval solve | 1 | 1 | 3.93e-10 | 5.0e-08 | PASS |
| P = 0.9 P_cr, δ0 = 0 mm, e = 2 mm: page finite elements (64) vs Python finite elements (128, numpy solve), mid-length — discretization, amplified near P_cr | 0.022838295 | 0.022838295 | 3.76e-08 | 5.0e-07 | PASS |
| P = 0.9 P_cr, δ0 = 0 mm, e = 2 mm: page Eq. 10.35 vs Python Eq. 10.33 with Eq. 10.31 | 2.484983e+08 | 2.484983e+08 | 2.40e-16 | 1.0e-12 | PASS |
| P = 0.95 P_cr, δ0 = 0.26 mm, e = 0.08 mm: page closed form (bow + Eq. 10.26) vs scipy banded finite differences (N = 4000 and 8000, Richardson), worst of 4 points — round-off floor of the 8000-interval solve | 1 | 1 | 2.45e-08 | 5.0e-08 | PASS |
| P = 0.95 P_cr, δ0 = 0.26 mm, e = 0.08 mm: page finite elements (64) vs Python finite elements (128, numpy solve), mid-length — discretization, amplified near P_cr | 0.0068719213 | 0.0068719224 | 1.61e-07 | 5.0e-07 | PASS |
| P = 0.95 P_cr, δ0 = 0.26 mm, e = 0.08 mm: page Eq. 10.35 vs Python Eq. 10.33 with Eq. 10.31 | 31098241 | 31098241 | 1.20e-16 | 1.0e-12 | PASS |
| elastica at 1.01 P_cr: page (Carlson R_F + bisection) vs scipy.special.ellipk, P/P_cr | 1.01 | 1.01 | 2.20e-16 | 1.0e-12 | PASS |
| elastica at 1.01 P_cr: page δ/L vs scipy.special | 0.08897418 | 0.08897418 | 0.00e+00 | 1.0e-12 | PASS |
| elastica at 1.01 P_cr: page δ/L vs scipy solve_bvp (collocation) | 0.08897418 | 0.08897418 | 4.89e-13 | 2.0e-07 | PASS |
| elastica at 1.01 P_cr: end slope, page vs solve_bvp | 0.28184672 | 0.28184672 | 4.92e-13 | 2.0e-07 | PASS |
| elastica at 1.1 P_cr: page (Carlson R_F + bisection) vs scipy.special.ellipk, P/P_cr | 1.1 | 1.1 | 4.04e-16 | 1.0e-12 | PASS |
| elastica at 1.1 P_cr: page δ/L vs scipy.special | 0.25426708 | 0.25426708 | 2.18e-16 | 1.0e-12 | PASS |
| elastica at 1.1 P_cr: page δ/L vs scipy solve_bvp (collocation) | 0.25426708 | 0.25426708 | 9.96e-14 | 2.0e-07 | PASS |
| elastica at 1.1 P_cr: end slope, page vs solve_bvp | 0.86445863 | 0.86445863 | 9.88e-14 | 2.0e-07 | PASS |
| elastica at 1.5 P_cr: page (Carlson R_F + bisection) vs scipy.special.ellipk, P/P_cr | 1.5 | 1.5 | 1.48e-16 | 1.0e-12 | PASS |
| elastica at 1.5 P_cr: page δ/L vs scipy.special | 0.3942879 | 0.3942879 | 2.82e-16 | 1.0e-12 | PASS |
| elastica at 1.5 P_cr: page δ/L vs scipy solve_bvp (collocation) | 0.3942879 | 0.3942879 | 2.25e-15 | 2.0e-07 | PASS |
| elastica at 1.5 P_cr: end slope, page vs solve_bvp | 1.7221418 | 1.7221418 | 3.87e-15 | 2.0e-07 | PASS |
| elastica at 2 P_cr: page (Carlson R_F + bisection) vs scipy.special.ellipk, P/P_cr | 2 | 2 | 6.66e-16 | 1.0e-12 | PASS |
| elastica at 2 P_cr: page δ/L vs scipy.special | 0.39848071 | 0.39848071 | 0.00e+00 | 1.0e-12 | PASS |
| elastica at 2 P_cr: page δ/L vs scipy solve_bvp (collocation) | 0.39848071 | 0.39848071 | 1.25e-15 | 2.0e-07 | PASS |
| elastica at 2 P_cr: end slope, page vs solve_bvp | 2.1738542 | 2.1738542 | 1.23e-15 | 2.0e-07 | PASS |
| secant first-yield load, e = 0.5 mm: page bisection vs scipy brentq (Eq. 10.36) | 1775.8194 | 1775.8194 | 4.84e-14 | 1.0e-10 | PASS |
| secant first-yield load, e = 1 mm: page bisection vs scipy brentq (Eq. 10.36) | 1733.0282 | 1733.0282 | 4.89e-14 | 1.0e-10 | PASS |
| secant first-yield load, e = 2 mm: page bisection vs scipy brentq (Eq. 10.36) | 1654.7289 | 1654.7289 | 5.48e-14 | 1.0e-10 | PASS |
| tangent-modulus column curve at L/r = 35: page vs Python (brentq) | 2.4309384e+08 | 2.4309384e+08 | 3.19e-15 | 1.0e-09 | PASS |
| reduced-modulus curve at L/r = 35: page vs Python | 2.5524103e+08 | 2.5524103e+08 | 2.34e-16 | 1.0e-09 | PASS |
| Aluminum Association 6061-T6 at L/r = 35: page vs Python | 1.2178675e+08 | 1.2178675e+08 | 0.00e+00 | 1.0e-14 | PASS |
| AISC σ_cr at L/r = 35 (E 200 GPa, σY 250 MPa): page vs Python | 2.3428156e+08 | 2.3428156e+08 | 0.00e+00 | 1.0e-14 | PASS |
| tangent-modulus column curve at L/r = 49.1: page vs Python (brentq) | 2.2087978e+08 | 2.2087978e+08 | 4.05e-16 | 1.0e-09 | PASS |
| reduced-modulus curve at L/r = 49.1: page vs Python | 2.2886997e+08 | 2.2886997e+08 | 6.51e-16 | 1.0e-09 | PASS |
| Aluminum Association 6061-T6 at L/r = 49.1: page vs Python | 1.0302872e+08 | 1.0302872e+08 | 0.00e+00 | 1.0e-14 | PASS |
| AISC σ_cr at L/r = 49.1 (E 200 GPa, σY 250 MPa): page vs Python | 2.2000798e+08 | 2.2000798e+08 | 0.00e+00 | 1.0e-14 | PASS |
| tangent-modulus column curve at L/r = 60: page vs Python (brentq) | 1.8569092e+08 | 1.8569092e+08 | 6.79e-14 | 1.0e-09 | PASS |
| reduced-modulus curve at L/r = 60: page vs Python | 1.8708016e+08 | 1.8708016e+08 | 4.78e-15 | 1.0e-09 | PASS |
| Aluminum Association 6061-T6 at L/r = 60: page vs Python | 89408000 | 89408000 | 0.00e+00 | 1.0e-14 | PASS |
| AISC σ_cr at L/r = 60 (E 200 GPa, σY 250 MPa): page vs Python | 2.0656701e+08 | 2.0656701e+08 | 0.00e+00 | 1.0e-14 | PASS |
| tangent-modulus column curve at L/r = 90: page vs Python (brentq) | 83952556 | 83952556 | 1.95e-15 | 1.0e-09 | PASS |
| reduced-modulus curve at L/r = 90: page vs Python | 83952559 | 83952559 | 1.05e-14 | 1.0e-09 | PASS |
| Aluminum Association 6061-T6 at L/r = 90: page vs Python | 43950617 | 43950617 | 0.00e+00 | 1.0e-14 | PASS |
| AISC σ_cr at L/r = 90 (E 200 GPa, σY 250 MPa): page vs Python | 1.6272794e+08 | 1.6272794e+08 | 0.00e+00 | 1.0e-14 | PASS |
| tangent-modulus column curve at L/r = 150: page vs Python (brentq) | 30222922 | 30222922 | 1.20e-13 | 1.0e-09 | PASS |
| reduced-modulus curve at L/r = 150: page vs Python | 30222922 | 30222922 | 1.17e-13 | 1.0e-09 | PASS |
| Aluminum Association 6061-T6 at L/r = 150: page vs Python | 15822222 | 15822222 | 0.00e+00 | 1.0e-14 | PASS |
| AISC σ_cr at L/r = 150 (E 200 GPa, σY 250 MPa): page vs Python | 76939049 | 76939049 | 0.00e+00 | 1.0e-14 | PASS |
| Part D: fiber-model maximum with 320 fibers vs the 80 used for the data (section discretization) | 31121.224 | 31094.263 | 8.67e-04 | 2.0e-03 | PASS |
| closure: Part A 300 mm: Southwell P_cr vs the truth eigenvalue (N) — \|Δ\| = 0.45 U — within 3u (99.7 %); students use 2u (absolute) | 4103.3305 | 4092.7297 | 1.06e+01 | 3.6e+01 | PASS |
| closure: Part A 450 mm: Southwell P_cr vs the truth eigenvalue (N) — \|Δ\| = 0.54 U — within 3u (99.7 %); students use 2u (absolute) | 1828.8061 | 1823.0372 | 5.77e+00 | 1.6e+01 | PASS |
| closure: Part A 600 mm: Southwell P_cr vs the truth eigenvalue (N) — \|Δ\| = 0.44 U — within 3u (99.7 %); students use 2u (absolute) | 1026.1354 | 1023.5234 | 2.61e+00 | 8.9e+00 | PASS |
| closure: Part A: E from the three Southwell loads vs truth 68.9 GPa — \|Δ\| = 0.36 U — within 3u (99.7 %); students use 2u (absolute) | 69.095941 | 68.9 | 1.96e-01 | 8.1e-01 | PASS |
| closure: Part A: E from the axial strain vs truth 68.9 GPa — \|Δ\| = 0.55 U — within 3u (99.7 %); students use 2u (absolute) | 69.337406 | 68.9 | 4.37e-01 | 1.2e+00 | PASS |
| closure: Part A log-log slope of P_cr against L vs −2 (Euler) (absolute) | -1.9969098 | -2 | 3.09e-03 | 1.0e-02 | PASS |
| closure: Part B fixed-fixed: Southwell P_cr vs truth eigenvalue with the real clamps (N) — \|Δ\| = 0.56 U — within 3u (99.7 %); students use 2u (absolute) | 3730.0737 | 3718.0897 | 1.20e+01 | 3.2e+01 | PASS |
| closure: Part B fixed-pinned: Southwell P_cr vs truth eigenvalue (N) — \|Δ\| = 0.64 U — within 3u (99.7 %); students use 2u (absolute) | 1765.0465 | 1758.4696 | 6.58e+00 | 1.5e+01 | PASS |
| closure: Part B: clamp stiffness from the fixed-fixed test vs the truth (mean of the two clamps, N·m/rad) — \|Δ\| = 0.57 U — within 3u (99.7 %); students use 2u (absolute) | 2796.7674 | 2515 | 2.82e+02 | 7.5e+02 | PASS |
| closure: Part B fixed-fixed disagrees with Euler for L_e = 0.5 L (-8.2 %, beyond U) | True | True | 0.00e+00 | 0.0e+00 | PASS |
| closure: the spring-end model predicts the fixed-pinned test within U | True | True | 0.00e+00 | 0.0e+00 | PASS |
| closure: Part C e = 1 mm: fitted eccentricity vs the true groove offset (mm) — \|Δ\| = 0.04 U — within 3u (99.7 %); students use 2u (absolute) | 1.0093002 | 1.01 | 7.00e-04 | 2.5e-02 | PASS |
| closure: Part C e = 2 mm: fitted eccentricity vs the true groove offset (mm) — \|Δ\| = 0.02 U — within 3u (99.7 %); students use 2u (absolute) | 1.9793728 | 1.98 | 6.27e-04 | 4.9e-02 | PASS |
| closure: Part D maximum load read from the data vs the truth model × UTM gain | 31029 | 31032.074 | 9.91e-05 | 2.0e-03 | PASS |
| closure: Part D lies below the tangent-modulus load (14.8 % under) and far below Euler (45.8 %) | True | True | 0.00e+00 | 0.0e+00 | PASS |
| closure: Part A 300 mm: Southwell δ0 vs the truth bow + (4/π) e_knife (mm) (absolute) | 0.37959837 | 0.38185916 | 2.26e-03 | 3.0e-02 | PASS |
| closure: Part A 450 mm: Southwell δ0 vs the truth bow + (4/π) e_knife (mm) (absolute) | 0.5330611 | 0.53185916 | 1.20e-03 | 3.0e-02 | PASS |
| closure: Part A 600 mm: Southwell δ0 vs the truth bow + (4/π) e_knife (mm) (absolute) | 0.75680077 | 0.76185916 | 5.06e-03 | 3.0e-02 | PASS |
| D1: page design preset, first-yield load (secant, Lab 2 E) vs analysis table | 24267.385 | 24267.385 | 3.61e-14 | 1.0e-10 | PASS |
| D1: page design preset, AA allowable load vs analysis table | 13654.064 | 13654.064 | 0.00e+00 | 1.0e-12 | PASS |
| D1: the preset tube 63.5 × 1.65 mm is the analysis's pinned answer [63.5, 1.65] | True | True | 0.00e+00 | 0.0e+00 | PASS |
| D1 trap: assuming clamped ends picks [44.45, 1.65], whose pinned allowable load is 4.53 kN < 12 kN | True | True | 0.00e+00 | 0.0e+00 | PASS |

97 of 97 passed.

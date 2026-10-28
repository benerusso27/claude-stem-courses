## Lab 4 — independent checks (Python/scipy) and data-pipeline closure

| Test | Value | Reference | Rel. difference | Tolerance | Result |
|---|---:|---:|---:|---:|---|
| 4-point bending at x = 0.05 m: M, JavaScript vs Python (direct formula) | 500 | 500 | 0.00e+00 | 1.0e-12 | PASS |
| 4-point bending at x = 0.05 m: V/P (absolute) | 0.5 | 0.5 | 0.00e+00 | 1.0e-12 | PASS |
| 4-point bending at x = 0.2 m: M, JavaScript vs Python (direct formula) | 2000 | 2000 | 0.00e+00 | 1.0e-12 | PASS |
| 4-point bending at x = 0.2 m: V/P (absolute) | 0.5 | 0.5 | 0.00e+00 | 1.0e-12 | PASS |
| 4-point bending at x = 0.3 m: M, JavaScript vs Python (direct formula) | 2000 | 2000 | 1.14e-16 | 1.0e-12 | PASS |
| 4-point bending at x = 0.3 m: V/P (absolute) | 0 | 0 | 0.00e+00 | 1.0e-12 | PASS |
| 4-point bending at x = 0.45 m: M, JavaScript vs Python (direct formula) | 1500 | 1500 | 1.52e-16 | 1.0e-12 | PASS |
| 4-point bending at x = 0.45 m: V/P (absolute) | -0.5 | -0.5 | 0.00e+00 | 1.0e-12 | PASS |
| 4-point bending at x = 0.55 m: M, JavaScript vs Python (direct formula) | 500 | 500 | 9.09e-16 | 1.0e-12 | PASS |
| 4-point bending at x = 0.55 m: V/P (absolute) | -0.5 | -0.5 | 0.00e+00 | 1.0e-12 | PASS |
| cantilever, triangular load, x = 0.1 m: M, JavaScript vs scipy.quad (right free body) | -7400.5 | -7400.5 | 1.23e-16 | 1.0e-11 | PASS |
| cantilever, triangular load, x = 0.1 m: V | 5985 | 5985 | 0.00e+00 | 1.0e-11 | PASS |
| cantilever, triangular load, x = 0.5 m: M, JavaScript vs scipy.quad (right free body) | -5062.5 | -5062.5 | 1.80e-16 | 1.0e-11 | PASS |
| cantilever, triangular load, x = 0.5 m: V | 5625 | 5625 | 0.00e+00 | 1.0e-11 | PASS |
| cantilever, triangular load, x = 1 m: M, JavaScript vs scipy.quad (right free body) | -2500 | -2500 | 0.00e+00 | 1.0e-11 | PASS |
| cantilever, triangular load, x = 1 m: V | 4500 | 4500 | 2.02e-16 | 1.0e-11 | PASS |
| cantilever, triangular load, x = 1.5 m: M, JavaScript vs scipy.quad (right free body) | -687.5 | -687.5 | 0.00e+00 | 1.0e-11 | PASS |
| cantilever, triangular load, x = 1.5 m: V | 2625 | 2625 | 1.73e-16 | 1.0e-11 | PASS |
| cantilever, triangular load, x = 1.9 m: M, JavaScript vs scipy.quad (right free body) | -29.5 | -29.5 | 2.91e-14 | 1.0e-11 | PASS |
| cantilever, triangular load, x = 1.9 m: V | 585 | 585 | 9.72e-16 | 1.0e-11 | PASS |
| rectangle (own law), κ = 0.05: strip summation (N = 2000) vs scipy.quad + brentq — midpoint rule O(N⁻²) | 955.9446 | 955.94484 | 2.50e-07 | 2.0e-06 | PASS |
| rectangle (own law), κ = 0.2: strip summation (N = 2000) vs scipy.quad + brentq — midpoint rule O(N⁻²) | 3429.7698 | 3429.7703 | 1.28e-07 | 2.0e-06 | PASS |
| rectangle (own law), κ = 0.4: strip summation (N = 2000) vs scipy.quad + brentq — midpoint rule O(N⁻²) | 4339.4239 | 4339.4244 | 1.01e-07 | 2.0e-06 | PASS |
| rectangle (epp law), κ = 0.05: strip summation (N = 2000) vs scipy.quad + brentq — midpoint rule O(N⁻²) | 955.9446 | 955.94484 | 2.50e-07 | 2.0e-06 | PASS |
|     … vs Python §4.6 formula | 955.9446 | 955.94484 | 2.50e-07 | 2.0e-06 | PASS |
| rectangle (epp law), κ = 0.2: strip summation (N = 2000) vs scipy.quad + brentq — midpoint rule O(N⁻²) | 3572.8514 | 3572.852 | 1.73e-07 | 2.0e-06 | PASS |
|     … vs Python §4.6 formula | 3572.8514 | 3572.852 | 1.73e-07 | 2.0e-06 | PASS |
| rectangle (epp law), κ = 0.4: strip summation (N = 2000) vs scipy.quad + brentq — midpoint rule O(N⁻²) | 4260.7547 | 4260.7547 | 6.05e-09 | 2.0e-06 | PASS |
|     … vs Python §4.6 formula | 4260.7547 | 4260.7547 | 6.05e-09 | 2.0e-06 | PASS |
| composite (elastic), κ = 0.02: M, strip vs quad | 778.18282 | 778.18299 | 2.13e-07 | 2.0e-06 | PASS |
| composite (elastic), κ = 0.02: neutral axis, strip vs brentq | 0.024003537 | 0.024003537 | 2.89e-16 | 1.0e-09 | PASS |
| composite (own curves, both yielding), κ = 0.4: M, strip vs quad | 5638.4206 | 5638.4211 | 9.82e-08 | 2.0e-05 | PASS |
| composite (own curves), κ = 0.4: neutral axis | 0.028520074 | 0.028520074 | 8.96e-10 | 2.0e-05 | PASS |
| composite (elastic), κ = 0.05: M, strip vs quad | 1945.4571 | 1945.4575 | 2.13e-07 | 2.0e-06 | PASS |
| composite (elastic), κ = 0.05: neutral axis, strip vs brentq | 0.024003537 | 0.024003537 | 2.89e-16 | 1.0e-09 | PASS |
| composite (own curves, both yielding), κ = 1: M, strip vs quad | 6410.6619 | 6410.6625 | 9.33e-08 | 2.0e-05 | PASS |
| composite (own curves), κ = 1: neutral axis | 0.028293019 | 0.028293019 | 2.20e-09 | 2.0e-05 | PASS |
| I-section (1018 curve), κ = 0.01: strip vs quad | 43014.461 | 43014.467 | 1.22e-07 | 2.0e-05 | PASS |
| I-section (1018 curve), κ = 0.03: strip vs quad | 69478.88 | 69478.883 | 4.14e-08 | 2.0e-05 | PASS |
| composite: transformed centroid, JavaScript vs Python | 0.024003537 | 0.024003537 | 0.00e+00 | 1.0e-12 | PASS |
| composite: transformed I, JavaScript vs Python | 5.6471915e-07 | 5.6471915e-07 | 0.00e+00 | 1.0e-12 | PASS |
| I-section: I, JavaScript vs Python | 2.0982667e-05 | 2.0982667e-05 | 4.84e-16 | 1.0e-12 | PASS |
| I-section: Z, JavaScript (equal-area routine) vs Python (formula) | 0.0002386 | 0.0002386 | 2.27e-16 | 1.0e-12 | PASS |
| closure: E of 6061-T6 from M–κ (GPa) recovered within U = 0.904 (value 68.393, truth 68.557) — truth divided by the gage-factor error | True | True | 0.00e+00 | 0.0e+00 | PASS |
| closure: neutral axis height, Part A (mm) recovered within U = 0.0465 (value 25.392, truth 25.39) | True | True | 0.00e+00 | 0.0e+00 | PASS |
| closure: Poisson's ratio from anticlastic strain recovered within U = 0.00589 (value 0.32945, truth 0.33) | True | True | 0.00e+00 | 0.0e+00 | PASS |
| closure: shear V per unit load from the moment gradient recovered within U = 0.0242 (value 0.50052, truth 0.5) | True | True | 0.00e+00 | 0.0e+00 | PASS |
| closure: composite neutral axis (mm) recovered within U = 0.0885 (value 23.985, truth 23.994) | True | True | 0.00e+00 | 0.0e+00 | PASS |
| closure: composite EI (N·m²) recovered within U = 808 (value 38606, truth 38738) | True | True | 0.00e+00 | 0.0e+00 | PASS |
| closure: Part C maximum curvature (1/m) recovered within U = 0.00292 (value 0.29345, truth 0.29346) | True | True | 0.00e+00 | 0.0e+00 | PASS |
| closure: Part C residual curvature (1/m) recovered within U = 0.00385 (value 0.08266, truth 0.082692) | True | True | 0.00e+00 | 0.0e+00 | PASS |
| closure: straightedge gap, κ_p(x) integrated from the measured M–κ curve (mm) recovered within U = 0.0493 (value 2.8712, truth 2.8399) | True | True | 0.00e+00 | 0.0e+00 | PASS |
| closure: straightedge gap in the sample measurements (mm) recovered within U = 0.026 (value 2.85, truth 2.8399) — rounded to the 0.05 mm feeler step | True | True | 0.00e+00 | 0.0e+00 | PASS |

53 of 53 passed.

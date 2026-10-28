## Lab 7 — handout questions re-solved from scratch vs. the instructor key

| Question / quantity | From scratch | Key | Rel. difference | Tolerance | Result |
|---|---:|---:|---:|---:|---|
| P1(a) deflection at 200 mm, 3.0 kg at 600 mm (mm) | 1.23452 | 1.235 | 3.9e-04 | 1e-03 | PASS |
| P1(a) deflection at 400 mm (mm) | 1.93996 | 1.94 | 2.2e-05 | 1e-03 | PASS |
| P1(a) largest stress (MPa) | 25.8525 | 25.9 | 1.8e-03 | 2e-03 | PASS |
| P1(d) α for 0.62 kg on the nominal strip | 3.58751 | 3.59 | 6.9e-04 | 2e-03 | PASS |
| P3(b) R_B/P with λ = 0.04 | 0.332589 | 0.3326 | 3.2e-05 | 1e-03 | PASS |
| P3(c) ΔR_B for 0.5 mm, rigid clamp (N) | -0.486349 | -0.486 | 7.2e-04 | 2e-03 | PASS |
| A1 E from one global fit of twelve series (GPa) | 205.052 | 205.01 | 2.1e-04 | 2e-03 | PASS |
| A2 superposed deflection at 200 mm (mm) | 1.34521 | 1.345 | 1.6e-04 | 1e-03 | PASS |
| A2 measured deflection with both loads at 200 mm (mm) | 1.346 | 1.346 | 0.0e+00 | 1e-03 | PASS |
| A2 superposed deflection at 400 mm (mm) | 1.9275 | 1.928 | 2.6e-04 | 1e-03 | PASS |
| A2 measured deflection with both loads at 400 mm (mm) | 1.927 | 1.927 | 0.0e+00 | 1e-03 | PASS |
| A2 superposed deflection at 600 mm (mm) | 1.46136 | 1.461 | 2.4e-04 | 1e-03 | PASS |
| A2 measured deflection with both loads at 600 mm (mm) | 1.462 | 1.462 | 0.0e+00 | 1e-03 | PASS |
| A2 c13 (µm/N) | 41.7792 | 41.779 | 5.5e-06 | 1e-04 | PASS |
| A2 c31 (µm/N) | 41.7137 | 41.714 | 7.7e-06 | 1e-04 | PASS |
| A3 EI from 8[c(L) − 2c(L/2)]/L³ (N·m²) | 112.307 | 112.31 | 3.0e-05 | 1e-03 | PASS |
| A3 k from 3L²/[16c(L/2) − 5c(L)] (N·m/rad) | 4366.34 | 4370 | 8.4e-04 | 3e-03 | PASS |
| A3 EI from the tip alone, rigid clamp (N·m²) | 101.156 | 101.16 | 4.0e-05 | 1e-03 | PASS |
| A4 R_B/P from the load cell (slope) | 0.330796 | 0.3308 | 1.2e-05 | 1e-03 | PASS |
| A4 R_B/P, stiffness method with the A3 clamp | 0.331117 | 0.3311 | 5.0e-05 | 1e-03 | PASS |
| A4 R_B/P, stiffness method with a rigid clamp (5/16) | 0.3125 | 0.3125 | 2.9e-13 | 1e-09 | PASS |
| A4 ΔR_B measured (N) | -0.43 | -0.43 | 6.5e-16 | 1e-03 | PASS |
| A4 ΔR_B for 0.5 mm, stiffness method with the clamp (N) | -0.442373 | -0.442 | 8.4e-04 | 3e-03 | PASS |
| A5(a) EI from the first four points (N·m²) | 0.105012 | 0.105 | 1.2e-04 | 2e-03 | PASS |
| C2 EI from the whole curve with self-weight, solve_ivp shooting (N·m²) | 0.10473 | 0.1047 | 2.9e-04 | 2e-03 | PASS |
| C2 E of the strip (GPa) | 203.014 | 203 | 6.9e-05 | 2e-03 | PASS |
| A5 α where Eq. 10 is 5 % high, shooting + brentq | 0.675637 | 0.676 | 5.4e-04 | 1e-03 | PASS |
| M1(a) factor by which Eq. 10 overstates δ_v at 0.62 kg (measured δ_v) | 1.88475 | 1.88 | 2.5e-03 | 3e-03 | PASS |
| C3 prop error that changes R_B at 4.0 kg by 5 % (mm) | 0.733318 | 0.733 | 4.3e-04 | 3e-03 | PASS |
| D1 lightest feasible section (name match) | 1 | 1 | 0.0e+00 | 0e+00 | PASS |
| D1 first feasible roller position (m) | 3.05 | 3.05 | 0.0e+00 | 1e-09 | PASS |
| D1 last feasible roller position (m) | 3.1 | 3.1 | 0.0e+00 | 1e-09 | PASS |
| D1 largest stress at the reference design (MPa) | 55.6547 | 55.7 | 8.1e-04 | 2e-03 | PASS |
| D1 largest span deflection (mm) | 6.43817 | 6.44 | 2.8e-04 | 2e-03 | PASS |
| D1 tip deflection (mm) | 4.36 | 4.36 | 2.6e-07 | 3e-03 | PASS |

35 of 35 agree.
Tolerances: about 1e-3 where the key prints a rounded value of the same quantity; 2e-3 to 3e-3 where a different estimator is used on purpose (one global fit instead of six slopes, unweighted shooting fit instead of the uncertainty-weighted collocation fit, trapezoidal integration instead of closed forms).

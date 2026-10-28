## Lab 5 — handout questions re-solved from scratch vs. the instructor key

| Question / quantity | From scratch | Key | Rel. difference | Tolerance | Result |
|---|---:|---:|---:|---:|---|
| §2.1 example: τ_max of a 30 × 90 mm rectangle at V = 12 kN (MPa) | 6.66667 | 6.67 | 5.0e-04 | 1e-03 | PASS |
| §2.1 example: τ at 22.5 mm above the NA (MPa) | 5 | 5 | 0.0e+00 | 1e-03 | PASS |
| P1(a) τ = 3V/2A at V = 7.5 kN (MPa) | 8.71877 | 8.719 | 2.7e-05 | 1e-03 | PASS |
| P1(a) largest bending stress PL/4 ÷ bh²/6 (MPa) | 137.303 | 137.3 | 2.5e-05 | 1e-03 | PASS |
| P2 I-beam I by fine strips (10⁶ mm⁴) | 2.47692 | 2.4769 | 7.4e-06 | 1e-04 | PASS |
| P2(a) τ at the NA = VQ/(It_w), strips (MPa) | 23.5339 | 23.53 | 1.6e-04 | 2e-04 | PASS |
| P2(b) τ in the web at the junction (MPa) | 19.5455 | 19.55 | 2.3e-04 | 1e-03 | PASS |
| P1(b)/P2 τ ≈ V/A_w (MPa) | 23.6315 | 23.63 | 6.3e-05 | 1e-03 | PASS |
| P1(c) bending part at 300 mm (mm) | 0.0331722 | 0.0332 | 8.4e-04 | 2e-03 | PASS |
| P1(c) shear part at 300 mm (mm) | 0.0680892 | 0.0681 | 1.6e-04 | 2e-03 | PASS |
| P1(c) bending part at 1200 mm (mm) | 2.12302 | 2.123 | 9.0e-06 | 2e-03 | PASS |
| P1(c) shear part at 1200 mm (mm) | 0.272357 | 0.2724 | 1.6e-04 | 2e-03 | PASS |
| P1(d) loose deflection at 2 kN (mm) | 7.58022 | 7.58 | 2.9e-05 | 2e-03 | PASS |
| P1(d) loose end slip r θ_end at 2 kN (mm) | 0.481344 | 0.481 | 7.2e-04 | 2e-03 | PASS |
| P3 q = VQ/I at the interface, V = 1.25 kN (N/mm) | 73.8189 | 73.8 | 2.6e-04 | 1e-03 | PASS |
| A1 upright: R from 2-D finite differences (64/128 cells, Richardson) vs key (series) | 1.04136 | 1.0414 | 4.2e-05 | 2e-04 | PASS |
| A1 upright: measured R (slope of τ against V) ÷ 3/(2A) | 1.04234 | 1.042 | 3.2e-04 | 1e-03 | PASS |
| A1 upright: R from the largest load step only (different estimator) | 1.05131 | 1.042 | 8.9e-03 | 1e-02 | PASS |
| A1 flat: R from 2-D finite differences (64/128 cells, Richardson) vs key (series) | 1.49091 | 1.4909 | 6.9e-06 | 2e-04 | PASS |
| A1 flat: measured R (slope of τ against V) ÷ 3/(2A) | 1.51456 | 1.515 | 2.9e-04 | 1e-03 | PASS |
| A1 flat: R from the largest load step only (different estimator) | 1.50727 | 1.515 | 5.1e-03 | 1e-02 | PASS |
| A2 I of the measured section by strips (10⁶ mm⁴) | 2.48019 | 2.4802 | 4.5e-06 | 1e-04 | PASS |
| A2 web gage 1: measured τ/V (10⁻³ mm⁻²) | 2.35738 | 2.3574 | 9.8e-06 | 1e-03 | PASS |
| A2 web gage 1: Q/(I t_w) by strips (10⁻³ mm⁻²) | 2.33472 | 2.3347 | 8.9e-06 | 2e-04 | PASS |
| A2 web gage 2: measured τ/V (10⁻³ mm⁻²) | 2.24911 | 2.2491 | 2.4e-06 | 1e-03 | PASS |
| A2 web gage 2: Q/(I t_w) by strips (10⁻³ mm⁻²) | 2.23385 | 2.2338 | 2.1e-05 | 2e-04 | PASS |
| A2 web gage 3: measured τ/V (10⁻³ mm⁻²) | 2.01228 | 2.0123 | 1.1e-05 | 1e-03 | PASS |
| A2 web gage 3: Q/(I t_w) by strips (10⁻³ mm⁻²) | 1.99369 | 1.9937 | 2.9e-06 | 2e-04 | PASS |
| A3 shear form factor f_s of the measured I-beam (fine strips) | 2.90151 | 2.9015 | 4.8e-06 | 2e-04 | PASS |
| A3 E from one nonlinear fit of all (P, L, δ) points (GPa) | 68.754 | 68.66 | 1.4e-03 | 4e-03 | PASS |
| A3 G from the same fit (GPa) | 25.7178 | 25.84 | 4.7e-03 | 1e-02 | PASS |
| A4 span with a 5 % shear part from the global fit (mm) | 1773.28 | 1768 | 3.0e-03 | 1e-02 | PASS |
| A4 the same from Eq. 9 with Table 1 values (mm) | 1758.84 | 1759 | 9.1e-05 | 1e-03 | PASS |
| A5 loose: EI_eff (N·m²) | 1189.87 | 1190 | 1.1e-04 | 1e-03 | PASS |
| A5 bolted: EI_eff (N·m²) | 2529.52 | 2530 | 1.9e-04 | 1e-03 | PASS |
| A5 bonded: EI_eff (N·m²) | 4761.15 | 4761 | 3.1e-05 | 1e-03 | PASS |
| A5 EI₀ from Eq. 11 (N·m²) | 1187.77 | 1188 | 1.9e-04 | 1e-03 | PASS |
| A5 EI_full from Eq. 11 (N·m²) | 4751.07 | 4751 | 1.5e-05 | 1e-03 | PASS |
| A5 loose end slip per newton (10⁻⁹ m/N) | 239.535 | 239.535 | 5.1e-08 | 2e-03 | PASS |
| A5 r L²/(16 EI₀) (10⁻⁹ m/N) | 240.577 | 240.58 | 1.3e-05 | 1e-03 | PASS |
| A6 bolt slip modulus from a linear system for the bolt forces (kN/mm) | 40.1558 | 40.16 | 1.0e-04 | 2e-03 | PASS |
| A6 predicted end slip per newton (10⁻⁹ m/N) | 66.9557 | 66.956 | 5.1e-06 | 3e-03 | PASS |
| A6 largest bolt force at 2.5 kN (kN) | 6.05078 | 6.05 | 1.3e-04 | 3e-03 | PASS |
| A6 Beer's F = (VQ/I) s at 2.5 kN (kN) | 7.38189 | 7.38 | 2.6e-04 | 1e-03 | PASS |
| A6 glue shearing stress VQ/(Ib) at 4 kN (MPa) | 2.32409 | 2.32 | 1.8e-03 | 3e-03 | PASS |
| D1 shear flow at the support 3V/(4t) (N/mm) | 144 | 144 | 0.0e+00 | 1e-06 | PASS |
| D1 spacing limit at the support 10 kN / q (mm) | 69.4444 | 69.4 | 6.4e-04 | 1e-03 | PASS |
| D1 fully composite deflection 5wL⁴/(384 E I) (mm) | 6.05784 | 6.06 | 3.6e-04 | 2e-03 | PASS |
| D1 uniform 70 mm spacing: number of bolts | 34 | 34 | 0.0e+00 | 1e-09 | PASS |
| D1 uniform 70 mm spacing: largest Eq. 5 force (kN) | 9.786 | 9.79 | 4.1e-04 | 1e-03 | PASS |

50 of 50 agree.
Tolerances: about 1e-3 where the key prints a rounded value of the same quantity; up to 1e-2 where a different estimator is used on purpose (global nonlinear fit, finite-difference R); 1.5e-2 for the single-step ratio, which ignores the fit intercept.

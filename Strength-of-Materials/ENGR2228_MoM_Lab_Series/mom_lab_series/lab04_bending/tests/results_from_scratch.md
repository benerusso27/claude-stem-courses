## Lab 4 — handout questions re-solved from scratch vs. the instructor key

| Question / quantity | From scratch | Key | Rel. difference | Tolerance | Result |
|---|---:|---:|---:|---:|---|
| §2.1 example: M under the load = 6 kN × 0.8 m (kN·m) | 4.8 | 4.8 | 1.9e-16 | 1e-12 | PASS |
| §2.2 example: σ_m = Mc/I (MPa) | 70.3125 | 70.3 | 1.8e-04 | 1e-03 | PASS |
| §2.2 example: κ = M/(EI) (1/m) | 0.0085747 | 0.00857 | 5.5e-04 | 1e-03 | PASS |
| P1 I (10⁵ mm⁴) | 2.77488 | 2.7749 | 8.6e-06 | 1e-04 | PASS |
| P1 σ at 20 kN (MPa) | 183.071 | 183.1 | 1.6e-04 | 1e-03 | PASS |
| P1 κ at 20 kN (1/m) | 0.105281 | 0.1053 | 1.8e-04 | 1e-03 | PASS |
| P1 first-yield load P_Y (kN) | 29.9009 | 29.9 | 3.1e-05 | 1e-03 | PASS |
| P1 fully plastic load from Z = bh²/4 (kN) | 44.8514 | 44.85 | 3.1e-05 | 1e-03 | PASS |
| P2(c) R_A/P by moments about B | 0.500333 | 0.50033 | 6.7e-06 | 1e-05 | PASS |
| P3 transformed centroid by strip integration (mm) | 23.9673 | 23.967 | 1.4e-05 | 1e-04 | PASS |
| P3 I_t by strip integration (10⁵ mm⁴) | 5.66064 | 5.6607 | 1.0e-05 | 1e-04 | PASS |
| P3 steel bottom stress n M ȳ/I_t (MPa) | 190.179 | 190.2 | 1.1e-04 | 1e-03 | PASS |
| P3 aluminum top stress (MPa) | -87.9299 | -87.9 | 3.4e-04 | 1e-03 | PASS |
| P4 κ at 40 kN by bisection on Eq. 12 (1/m) | 0.276311 | 0.2763 | 4.0e-05 | 1e-03 | PASS |
| P4 permanent curvature (1/m) | 0.0657493 | 0.0657 | 7.5e-04 | 2e-03 | PASS |
| P4 residual stress at the top (MPa) | 92.4425 | 92.4 | 4.6e-04 | 1e-03 | PASS |
| A2 mean neutral axis, bar A (mm) | 25.3915 | 25.392 | 1.9e-05 | 1e-04 | PASS |
| A2 κ at 20 kN (1/m) | 0.105399 | 0.1054 | 1.1e-05 | 1e-04 | PASS |
| A3 E from the slope of M vs κ (GPa) | 68.3929 | 68.39 | 4.2e-05 | 1e-03 | PASS |
| A3 E as the mean of M/(κI) over the loading steps instead (GPa) | 68.4324 | 68.39 | 6.2e-04 | 3e-03 | PASS |
| A4 ν from a fit through the origin | 0.329818 | 0.3294 | 1.3e-03 | 5e-03 | PASS |
| A1 V/P = ΔM/Δx between the shear-span gages | 0.500525 | 0.5005 | 4.9e-05 | 2e-03 | PASS |
| A5 measured neutral axis, bar B (mm) | 23.9854 | 23.985 | 1.8e-05 | 1e-04 | PASS |
| A5 measured EI, bar B (N·m²) | 38605.7 | 38606 | 8.6e-06 | 1e-03 | PASS |
| A5 predicted neutral axis with measured E (mm) | 23.952 | 23.95 | 8.2e-05 | 1e-03 | PASS |
| A6 κ at 40 kN (1/m) | 0.293451 | 0.2935 | 1.7e-04 | 2e-03 | PASS |
| A6 permanent curvature after unloading (1/m) | 0.0826601 | 0.0827 | 4.8e-04 | 2e-03 | PASS |
| A6 Eq. 14 predicted permanent curvature (1/m) | 0.0825832 | 0.0826 | 2.0e-04 | 2e-03 | PASS |
| A6 EPP moment at the measured κ (N·m) | 4053.83 | 4054 | 4.2e-05 | 1e-03 | PASS |
| A6 actual extreme-fiber stress from the Ramberg–Osgood curve by bisection (MPa) | 282.019 | 282 | 6.6e-05 | 2e-03 | PASS |
| A6 flexure stress Mc/I (MPa) | 366.17 | 366.2 | 8.2e-05 | 1e-03 | PASS |
| A6 straightedge gap, curvature confined to the middle (mm) | 2.4798 | 2.48 | 7.9e-05 | 3e-03 | PASS |
| C1 I-section shape factor Z/S (first moments of the halves) | 1.13713 | 1.1371 | 2.6e-05 | 1e-04 | PASS |
| X3 elastic neutral axis (mm) | 141.729 | 141.73 | 7.3e-06 | 1e-04 | PASS |
| X3 plastic neutral axis (equal areas, mm) | 178.333 | 178.33 | 1.9e-05 | 1e-04 | PASS |
| X3 shape factor Z/S | 1.81885 | 1.819 | 8.0e-05 | 1e-03 | PASS |
| X1 |κ|/ΔT from Timoshenko's bimetal formula (10⁻³ 1/(m·K)) | 0.211411 | 0.2114 | 5.2e-05 | 1e-03 | PASS |
| D1 maximum moment (kN·m) | 7.125 | 7.125 | 0.0e+00 | 1e-06 | PASS |
| D1 lightest acceptable steel section: I-120 (key: I-120) | 1 | 1 | 0.0e+00 | 0e+00 | PASS |
| D1 steel: mass per meter of the chosen section (kg/m) | 10.0654 | 10.07 | 4.6e-04 | 1e-03 | PASS |
| D1 lightest acceptable aluminum section: I-160 (key: I-160) | 1 | 1 | 0.0e+00 | 0e+00 | PASS |
| D1 aluminum: mass per meter of the chosen section (kg/m) | 5.23692 | 5.24 | 5.9e-04 | 1e-03 | PASS |
| Table 6 I-100: printed I (10⁶ mm⁴) | 1.63323 | 1.633 | 1.4e-04 | 6e-04 | PASS |
| Table 6 I-100: printed S (10³ mm³) | 32.6645 | 32.66 | 1.4e-04 | 6e-04 | PASS |
| Table 6 I-120: printed I (10⁶ mm⁴) | 3.06313 | 3.063 | 4.2e-05 | 6e-04 | PASS |
| Table 6 I-120: printed S (10³ mm³) | 51.0521 | 51.05 | 4.2e-05 | 6e-04 | PASS |
| Table 6 I-140: printed I (10⁶ mm⁴) | 5.25289 | 5.253 | 2.1e-05 | 6e-04 | PASS |
| Table 6 I-140: printed S (10³ mm³) | 75.0413 | 75.04 | 1.7e-05 | 6e-04 | PASS |
| Table 6 I-160: printed I (10⁶ mm⁴) | 8.34626 | 8.346 | 3.2e-05 | 6e-04 | PASS |
| Table 6 I-160: printed S (10³ mm³) | 104.328 | 104.3 | 2.7e-04 | 6e-04 | PASS |
| Table 6 I-180: printed I (10⁶ mm⁴) | 12.7245 | 12.72 | 3.5e-04 | 6e-04 | PASS |
| Table 6 I-180: printed S (10³ mm³) | 141.383 | 141.4 | 1.2e-04 | 6e-04 | PASS |
| Table 6 I-200: printed I (10⁶ mm⁴) | 18.4559 | 18.46 | 2.2e-04 | 6e-04 | PASS |
| Table 6 I-200: printed S (10³ mm³) | 184.559 | 184.6 | 2.2e-04 | 6e-04 | PASS |
| Table 6 RT-100x50x4: printed I (10⁶ mm⁴) | 1.44126 | 1.441 | 1.8e-04 | 6e-04 | PASS |
| Table 6 RT-100x50x4: printed S (10³ mm³) | 28.8252 | 28.83 | 1.7e-04 | 6e-04 | PASS |
| Table 6 RT-120x60x5: printed I (10⁶ mm⁴) | 3.09417 | 3.094 | 5.4e-05 | 6e-04 | PASS |
| Table 6 RT-120x60x5: printed S (10³ mm³) | 51.5694 | 51.57 | 1.1e-05 | 6e-04 | PASS |
| Table 6 RT-150x100x5: printed I (10⁶ mm⁴) | 7.545 | 7.545 | 0.0e+00 | 6e-04 | PASS |
| Table 6 RT-150x100x5: printed S (10³ mm³) | 100.6 | 100.6 | 0.0e+00 | 6e-04 | PASS |
| Table 6 RT-200x100x6: printed I (10⁶ mm⁴) | 17.9391 | 17.94 | 5.2e-05 | 6e-04 | PASS |
| Table 6 RT-200x100x6: printed S (10³ mm³) | 179.391 | 179.4 | 5.2e-05 | 6e-04 | PASS |

62 of 62 agree.
Tolerances: about 1e-3 where the key prints a rounded value of the same quantity; up to 5e-3 where a different estimator is used on purpose (mean of M/(κI), fit through the origin, middle-only gap); 6e-4 for the 4-figure catalog table.

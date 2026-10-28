## Lab 2 — handout questions re-solved from scratch vs. the instructor key

| Question / quantity | From scratch | Key | Rel. difference | Tolerance | Result |
|---|---:|---:|---:|---:|---|
| P1 stress at 18 kN (MPa) | 111.6 | 111.6 | 2.0e-06 | 1e-03 | PASS |
| P1 axial strain (µε) | 1619.74 | 1620 | 1.6e-04 | 1e-03 | PASS |
| P2 P_gap (kN) | 6.925 | 6.925 | 3.2e-07 | 1e-03 | PASS |
| P2 share s | 0.370407 | 0.3704 | 1.9e-05 | 1e-03 | PASS |
| P2 F2 at 10 kN (kN) | -1.139 | -1.139 | 5.3e-07 | 1e-03 | PASS |
| P2 F2 at 20 kN (kN) | -4.84307 | -4.843 | 1.5e-05 | 1e-03 | PASS |
| P2 F2 at 30 kN (kN) | -8.54714 | -8.547 | 1.6e-05 | 1e-03 | PASS |
| P3 dF/dT (N/K) | 94.5294 | 94.53 | 6.2e-06 | 1e-03 | PASS |
| P3 bolt stress at 80 °C (MPa) | 97.6799 | 97.7 | 2.1e-04 | 1e-03 | PASS |
| P3(b) separation ΔT, swapped materials (K) | 34.6606 | 34.7 | 1.1e-03 | 2e-03 | PASS |
| P4 offset for β = 5 % (mm) | 0.0529167 | 0.0529 | 3.2e-04 | 1e-03 | PASS |
| P6 press load at rod yield (kN), by marching | 70.372 | 70.4 | 4.0e-04 | 2e-03 | PASS |
| handout worked example: δ of 20×5×300 mm bar at 10 kN (mm) | 0.435414 | 0.435 | 9.5e-04 | 2e-03 | PASS |
| handout worked example: cone vs mean-diameter flexibility ratio | 1.125 | 1.125 | 2.0e-16 | 1e-03 | PASS |
| handout worked example: brass/steel P_gap (kN) | 11.7018 | 11.7 | 1.5e-04 | 2e-03 | PASS |
| handout worked example: brass/steel share | 0.727874 | 0.728 | 1.7e-04 | 1e-03 | PASS |
| handout worked example: restrained steel heated 50 K (MPa) | 119.925 | 120 | 6.3e-04 | 1e-03 | PASS |
| handout worked example: 8 mm bolt, ΔF for 40 K (kN) | 2.40873 | 2.41 | 5.3e-04 | 2e-03 | PASS |
| handout §2.2: β for e = 0.05 mm on 6.35 mm (printed as 4.7 %) | 0.0472441 | 0.047 | 5.2e-03 | 1e-02 | PASS |
| A1 E (GPa) | 68.4593 | 68.4593 | 1.0e-15 | 1e-09 | PASS |
| A1 E printed in key | 68.4593 | 68.46 | 1.1e-05 | 1e-03 | PASS |
| A1 ν | 0.329619 | 0.33 | 1.2e-03 | 2e-03 | PASS |
| A1 G = E/2(1+ν) (GPa) | 25.7439 | 25.74 | 1.5e-04 | 1e-03 | PASS |
| A2 β | 0.054493 | 0.0545 | 1.3e-04 | 1e-03 | PASS |
| A2 offset e = βt/6 (mm) | 0.0576718 | 0.0577 | 4.9e-04 | 5e-03 | PASS |
| A2 harmonic mean of single-gage E equals average-strain E | 68.459 | 68.4593 | 4.1e-06 | 2e-03 | PASS |
| A3 P_gap by line intersection vs key's two-parameter fit (kN) | 6.93722 | 6.951 | 2.0e-03 | 5e-03 | PASS |
| A3 share s = −slope above the knee | 0.370926 | 0.3712 | 7.4e-04 | 5e-03 | PASS |
| A3 gap g = P_gap/k1 (mm) | 0.0400495 | 0.0401 | 1.3e-03 | 1e-02 | PASS |
| A3 theory share, Eq. 12 with measured E | 0.368867 | 0.3689 | 8.9e-05 | 1e-03 | PASS |
| A4 tube force at 30 kN (kN) | -8.52664 | -8.527 | 4.2e-05 | 1e-03 | PASS |
| A4 rod stress at 30 kN (MPa) | -169.519 | -169.5 | 1.1e-04 | 1e-03 | PASS |
| A4 no-gap overstatement (%) | 29.8335 | 29.8 | 1.1e-03 | 1e-02 | PASS |
| A4 tolerance for 5 % at 30 kN (µm) | 8.24734 | 8.2 | 5.8e-03 | 1e-02 | PASS |
| A5 cap compliance above the knee (µm/kN) | 1.43897 | 1.44 | 7.1e-04 | 2e-02 | PASS |
| M1(a) F2(20 kN)/F2(10 kN) | 4.28859 | 4.29 | 3.3e-04 | 2e-03 | PASS |
| M1(b) g_crit = σY L/E (mm) | 0.270732 | 0.271 | 9.9e-04 | 2e-03 | PASS |
| A6 dF/dT (N/K) | 97.6286 | 97.6 | 2.9e-04 | 1e-03 | PASS |
| A6 prediction, Eq. 16 (N/K) | 94.2635 | 94.3 | 3.9e-04 | 1e-03 | PASS |
| A6 preload (kN) | 1.99781 | 1.998 | 9.3e-05 | 1e-03 | PASS |
| A6 bolt stress at 80 °C (MPa) | 99.953 | 100 | 4.7e-04 | 1e-03 | PASS |
| C2 α of 6061-T6 (10⁻⁶/K) | 24.0248 | 24.02 | 2.0e-04 | 1e-03 | PASS |
| M1(c) separation ΔT, Al bolt in steel sleeve (K) | 34.6606 | 34.7 | 1.1e-03 | 2e-03 | PASS |
| C3 dilatation at 18 kN (10⁻⁶) | 555.84 | 556 | 2.9e-04 | 3e-03 | PASS |
| X1 critical L/d for 1018 | 36.974 | 37 | 7.0e-04 | 2e-03 | PASS |
| X3 brass tube force at 30 kN (kN) | -4.26273 | -4.26 | 6.4e-04 | 2e-03 | PASS |
| X3 second closing load (kN) | 17.9289 | 17.93 | 6.3e-05 | 2e-03 | PASS |
| D1 minimum gap (mm) | 1.43313 | 1.43 | 2.2e-03 | 5e-03 | PASS |
| D1 maximum gap (mm) | 4.814 | 4.81 | 8.3e-04 | 5e-03 | PASS |
| D1 3.0 ± 1.0 mm meets both requirements over the full envelope (brute force) | 1 | 1 | 0.0e+00 | 0e+00 | PASS |

50 of 50 agree.
Tolerances: 1e-3 where the key prints a rounded value of the same quantity; 5e-3 to 2e-2 where a different estimator is used on purpose (knee by line intersection vs. two-parameter fit; dial slope above a slightly different knee).

## Lab 8 — handout questions re-solved from scratch vs. the instructor key

| Question / quantity | From scratch | Key | Rel. difference | Tolerance | Result |
|---|---:|---:|---:|---:|---|
| P1(a) σmax at H (MPa) | 60.8447 | 60.84 | 7.7e-05 | 1e-03 | PASS |
| P1(a) θp at H (°) | -19.3299 | -19.33 | 5.0e-06 | 1e-03 | PASS |
| P1(b) τxy at K (MPa) | -24.769 | -24.77 | 3.9e-05 | 1e-03 | PASS |
| P1(d) Lamé hoop stress at 8 MPa (MPa) | 36.3636 | 36.36 | 1.0e-04 | 1e-03 | PASS |
| P4 absolute τmax at H, 8 MPa + lever (MPa) | 40.804 | 40.8 | 9.8e-05 | 1e-03 | PASS |
| A1 E by one nonlinear fit of all 21 Part A readings at H (GPa) | 68.5073 | 68.51 | 4.0e-05 | 2e-03 | PASS |
| A1 ν by the same fit | 0.329271 | 0.3293 | 8.9e-05 | 5e-03 | PASS |
| A1 β_H by the same fit (°) | 1.44868 | 1.45 | 9.1e-04 | 2e-02 | PASS |
| A2 G at H from the strain-circle radius (GPa) | 25.5536 | 25.55 | 1.4e-04 | 2e-03 | PASS |
| A2 G at K from the strain-circle radius (GPa) | 25.7895 | 25.79 | 2.0e-05 | 2e-03 | PASS |
| A3 σmax at H, Part B, from principal strains (MPa) | 60.2859 | 60.29 | 6.8e-05 | 2e-03 | PASS |
| A3 σmin at H, Part B, from principal strains (MPa) | -7.36148 | -7.36 | 2.0e-04 | 4e-03 | PASS |
| A3 σmax at K, Part B, from principal strains (MPa) | 24.6089 | 24.61 | 4.4e-05 | 2e-03 | PASS |
| A3 σmin at K, Part B, from principal strains (MPa) | -24.0702 | -24.07 | 8.2e-06 | 4e-03 | PASS |
| A3 θp at H = angle on the rosette's axes + β_H from A1 (°) | -19.5309 | -19.53 | 4.7e-05 | 2e-02 | PASS |
| A4 ν from the ratio of the principal strains under pressure | 0.33504 | 0.3349 | 4.2e-04 | 3e-03 | PASS |
| A4 hoop stress per MPa (MPa/MPa) | 4.48881 | 4.489 | 4.3e-05 | 2e-03 | PASS |
| A5 σmax at H, 8 MPa + 600 N (MPa) | 80.6913 | 80.69 | 1.6e-05 | 2e-03 | PASS |
| A5 absolute τmax at H = σmax/2 (MPa) | 40.3457 | 40.35 | 1.1e-04 | 2e-03 | PASS |
| A5 in-plane τmax at H (MPa) | 27.4889 | 27.49 | 4.0e-05 | 2e-03 | PASS |
| A5 σmax at K, 8 MPa + 600 N (MPa) | 52.6735 | 52.67 | 6.6e-05 | 2e-03 | PASS |
| D1 lightest tube (name match) | 1 | 1 | 0.0e+00 | 0e+00 | PASS |
| D1 Tresca factor of the reference tube | 2.23364 | 2.23 | 1.6e-03 | 3e-03 | PASS |
| D1 twist of the reference tube (°/m) | 2.77719 | 2.78 | 1.0e-03 | 3e-03 | PASS |

24 of 24 agree.
Tolerances: about 1e-3 where the key prints a rounded value of the same quantity; 2e-3 to 5e-3 where a different estimator is used on purpose (one nonlinear fit of all readings instead of slopes; invariants instead of turning back); 2e-2 for the angles, which the key rounds to 0.01° on values near 1°.

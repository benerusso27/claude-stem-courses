## Lab 2 — independent checks (Python/scipy) and data-pipeline closure

| Test | Value | Reference | Rel. difference | Tolerance | Result |
|---|---:|---:|---:|---:|---|
| [rodtube] F1: JavaScript vs Python closed form (relative to largest force) (absolute) | -1 | -1 | 0.00e+00 | 1.0e-12 | PASS |
| [rodtube] F2: JavaScript vs Python closed form (absolute) | -0.39841494 | -0.39841494 | 0.00e+00 | 1.0e-12 | PASS |
| [rodtube] F1: JavaScript closed form vs numpy.linalg.solve of the 2×2 system (absolute) | -1 | -1 | 2.22e-16 | 1.0e-12 | PASS |
| [bolt] F1: JavaScript vs Python closed form (relative to largest force) (absolute) | 1 | 1 | 0.00e+00 | 1.0e-12 | PASS |
| [bolt] F2: JavaScript vs Python closed form (absolute) | -1 | -1 | 0.00e+00 | 1.0e-12 | PASS |
| [bolt] F1: JavaScript closed form vs numpy.linalg.solve of the 2×2 system (absolute) | 1 | 1 | 0.00e+00 | 1.0e-12 | PASS |
| rod in tube: gap-closing load k1·g (Python) | 6925.0022 | 6925.0022 | 0.00e+00 | 1.0e-12 | PASS |
| bolt and sleeve: dF/dT JavaScript vs Python | 94.529416 | 94.529416 | 1.50e-16 | 1.0e-12 | PASS |
| [stepped] segment-1 flexibility: closed form vs scipy.quad | 2.9812438e-09 | 2.9812438e-09 | 1.39e-16 | 1.0e-11 | PASS |
| [stepped] wall reaction: JavaScript vs Python closed form | 6144.5216 | 6144.5216 | 0.00e+00 | 1.0e-12 | PASS |
| [stepped] wall reaction: closed form vs FE with N = 512 — taper: discretization; prismatic: round-off only | 6144.5216 | 6144.5216 | 1.45e-12 | 1.0e-10 | PASS |
| [taper] segment-1 flexibility: closed form vs scipy.quad | 1.6426248e-08 | 1.6426248e-08 | 2.01e-16 | 1.0e-11 | PASS |
| [taper] wall reaction: JavaScript vs Python closed form | 16558.864 | 16558.864 | 0.00e+00 | 1.0e-12 | PASS |
| [taper] wall reaction: closed form vs FE with N = 512 — taper: discretization; prismatic: round-off only | 16558.87 | 16558.864 | 3.71e-07 | 1.0e-05 | PASS |
| thermal buckling ΔT for d = 10 mm, L = 0.5 m steel (Python vs hand: π²r²/(α(L/2)²)) | 84.355593 | 84.355593 | 0.00e+00 | 1.0e-12 | PASS |
| closure: E of 6061-T6 (GPa) recovered within U = 0.931 (value 68.459, truth 68.9) — includes the +0.6 % gage-factor error | True | True | 0.00e+00 | 0.0e+00 | PASS |
| closure: Poisson's ratio recovered within U = 0.00581 (value 0.32962, truth 0.33) | True | True | 0.00e+00 | 0.0e+00 | PASS |
| closure: bending fraction front/back recovered within U = 0.005 (value 0.054493, truth 0.055) | True | True | 0.00e+00 | 0.0e+00 | PASS |
| closure: gap g (mm) recovered within U = 0.00121 (value 0.040128, truth 0.04) | True | True | 0.00e+00 | 0.0e+00 | PASS |
| closure: tube share after contact recovered within U = 0.00732 (value 0.37123, truth 0.37034) | True | True | 0.00e+00 | 0.0e+00 | PASS |
| closure: bolt dF/dT (N/K) recovered within U = 9.85 (value 97.629, truth 91.352) — residual thermal output of the gage biases it high | True | True | 0.00e+00 | 0.0e+00 | PASS |
| closure: bolt preload at 20 °C (N) recovered within U = 60 (value 1997.8, truth 2000) | True | True | 0.00e+00 | 0.0e+00 | PASS |

22 of 22 passed.

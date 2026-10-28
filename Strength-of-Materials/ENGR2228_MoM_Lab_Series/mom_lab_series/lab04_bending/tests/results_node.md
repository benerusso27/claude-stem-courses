## Lab 4 — simulation model (Node, exact page code)

| Test | Value | Reference | Rel. difference | Tolerance | Result |
|---|---:|---:|---:|---:|---|
| Ramberg–Osgood inverse ε(σ(ε)) = ε at ε = 0.0001 | 0.00010000000 | 0.00010000000 | 0.00e+0 | 1.0e-12 | PASS |
| Ramberg–Osgood inverse ε(σ(ε)) = ε at ε = 0.0039 | 0.0039000000 | 0.0039000000 | 1.11e-16 | 1.0e-12 | PASS |
| Ramberg–Osgood inverse ε(σ(ε)) = ε at ε = 0.008 | 0.0080000000 | 0.0080000000 | 6.51e-16 | 1.0e-12 | PASS |
| Ramberg–Osgood inverse ε(σ(ε)) = ε at ε = 0.03 | 0.030000000 | 0.030000000 | 1.04e-15 | 1.0e-12 | PASS |
| steel law continuous at the end of the plateau | 2.9700000e+8 | 2.9700000e+8 | 2.63e-9 | 1.0e-6 | PASS |
| [4-point bending (preset)] R_A: statics vs shooting integration (absolute difference) | 1.0000000 | 1.0000000 | 6.73e-11 | 1.0e-9 | PASS |
| [4-point bending (preset)] R_B: statics vs shooting integration (absolute difference) | 1.0000000 | 1.0000000 | 6.73e-11 | 1.0e-9 | PASS |
| [4-point bending (preset)] M(x) at every node: largest \|error\|/\|M\|max = 2.02e-10 (tolerance 1e-9) | true | true | 0.00e+0 | 0.0e+0 | PASS |
| [4-point bending (preset)] dM/dx = V at x = 0.078 m (relative to \|V\|max) (absolute difference) | -9.0949470e-13 | 0.0000000 | 9.09e-13 | 1.0e-6 | PASS |
| [4-point bending (preset)] dM/dx = V at x = 0.186 m (relative to \|V\|max) (absolute difference) | -9.0949470e-13 | 0.0000000 | 9.09e-13 | 1.0e-6 | PASS |
| [4-point bending (preset)] dM/dx = V at x = 0.342 m (relative to \|V\|max) (absolute difference) | 0.0000000 | 0.0000000 | 0.00e+0 | 1.0e-6 | PASS |
| [4-point bending (preset)] dM/dx = V at x = 0.498 m (relative to \|V\|max) (absolute difference) | 4.6384230e-11 | 0.0000000 | 4.64e-11 | 1.0e-6 | PASS |
| [cantilever, triangular load (preset)] R_A: statics vs shooting integration (absolute difference) | 1.0000000 | 1.0000000 | 0.00e+0 | 1.0e-9 | PASS |
| [cantilever, triangular load (preset)] fixed-end moment: statics vs integration from the free end | 7999.9924 | 8000.0000 | 9.54e-7 | 1.0e-5 | PASS |
| [cantilever, triangular load (preset)] M(x) at every node: largest \|error\|/\|M\|max = 9.54e-7 (tolerance 0.00002) | true | true | 0.00e+0 | 0.0e+0 | PASS |
| [cantilever, triangular load (preset)] dM/dx = V at x = 0.260 m (relative to \|V\|max) (absolute difference) | -9.0875801e-11 | 0.0000000 | 9.09e-11 | 1.0e-6 | PASS |
| [cantilever, triangular load (preset)] dM/dx = V at x = 0.620 m (relative to \|V\|max) (absolute difference) | 6.3610363e-11 | 0.0000000 | 6.36e-11 | 1.0e-6 | PASS |
| [cantilever, triangular load (preset)] dM/dx = V at x = 1.140 m (relative to \|V\|max) (absolute difference) | -5.2215000e-11 | 0.0000000 | 5.22e-11 | 1.0e-6 | PASS |
| [cantilever, triangular load (preset)] dM/dx = V at x = 1.660 m (relative to \|V\|max) (absolute difference) | 1.4145371e-11 | 0.0000000 | 1.41e-11 | 1.0e-6 | PASS |
| [overhang, point loads + uniform load (preset)] R_A: statics vs shooting integration (absolute difference) | 0.63636364 | 0.63636364 | 0.00e+0 | 1.0e-9 | PASS |
| [overhang, point loads + uniform load (preset)] R_B: statics vs shooting integration (absolute difference) | 1.0000000 | 1.0000000 | 0.00e+0 | 1.0e-9 | PASS |
| [overhang, point loads + uniform load (preset)] M(x) at every node: largest \|error\|/\|M\|max = 0.00e+0 (tolerance 1e-9) | true | true | 0.00e+0 | 0.0e+0 | PASS |
| [overhang, point loads + uniform load (preset)] dM/dx = V at x = 0.520 m (relative to \|V\|max) (absolute difference) | 1.6952981e-11 | 0.0000000 | 1.70e-11 | 1.0e-6 | PASS |
| [overhang, point loads + uniform load (preset)] dM/dx = V at x = 1.240 m (relative to \|V\|max) (absolute difference) | -2.8071967e-11 | 0.0000000 | 2.81e-11 | 1.0e-6 | PASS |
| [overhang, point loads + uniform load (preset)] dM/dx = V at x = 2.280 m (relative to \|V\|max) (absolute difference) | -4.6751335e-11 | 0.0000000 | 4.68e-11 | 1.0e-6 | PASS |
| [overhang, point loads + uniform load (preset)] dM/dx = V at x = 3.320 m (relative to \|V\|max) (absolute difference) | -9.1280196e-11 | 0.0000000 | 9.13e-11 | 1.0e-6 | PASS |
| [cantilever, triangular + point load] R_A: statics vs shooting integration (absolute difference) | 1.0000000 | 1.0000000 | 0.00e+0 | 1.0e-9 | PASS |
| [cantilever, triangular + point load] fixed-end moment: statics vs integration from the free end | 10099.992 | 10100.000 | 7.55e-7 | 1.0e-5 | PASS |
| [cantilever, triangular + point load] M(x) at every node: largest \|error\|/\|M\|max = 7.55e-7 (tolerance 0.00002) | true | true | 0.00e+0 | 0.0e+0 | PASS |
| [cantilever, triangular + point load] dM/dx = V at x = 0.260 m (relative to \|V\|max) (absolute difference) | 7.3250703e-12 | 0.0000000 | 7.33e-12 | 1.0e-6 | PASS |
| [cantilever, triangular + point load] dM/dx = V at x = 0.620 m (relative to \|V\|max) (absolute difference) | 9.2608793e-12 | 0.0000000 | 9.26e-12 | 1.0e-6 | PASS |
| [cantilever, triangular + point load] dM/dx = V at x = 1.140 m (relative to \|V\|max) (absolute difference) | -4.7441871e-11 | 0.0000000 | 4.74e-11 | 1.0e-6 | PASS |
| [cantilever, triangular + point load] dM/dx = V at x = 1.660 m (relative to \|V\|max) (absolute difference) | 9.4302474e-12 | 0.0000000 | 9.43e-12 | 1.0e-6 | PASS |
| [3-point bending] R_A: statics vs shooting integration (absolute difference) | 1.0000000 | 1.0000000 | 3.65e-11 | 1.0e-9 | PASS |
| [3-point bending] R_B: statics vs shooting integration (absolute difference) | 1.0000000 | 1.0000000 | 3.65e-11 | 1.0e-9 | PASS |
| [3-point bending] M(x) at every node: largest \|error\|/\|M\|max = 7.31e-11 (tolerance 1e-9) | true | true | 0.00e+0 | 0.0e+0 | PASS |
| [3-point bending] dM/dx = V at x = 0.078 m (relative to \|V\|max) (absolute difference) | 4.7748472e-12 | 0.0000000 | 4.77e-12 | 1.0e-6 | PASS |
| [3-point bending] dM/dx = V at x = 0.186 m (relative to \|V\|max) (absolute difference) | 1.4248750e-11 | 0.0000000 | 1.42e-11 | 1.0e-6 | PASS |
| [3-point bending] dM/dx = V at x = 0.342 m (relative to \|V\|max) (absolute difference) | 2.3646862e-11 | 0.0000000 | 2.36e-11 | 1.0e-6 | PASS |
| [3-point bending] dM/dx = V at x = 0.498 m (relative to \|V\|max) (absolute difference) | 2.3646862e-11 | 0.0000000 | 2.36e-11 | 1.0e-6 | PASS |
| [uniform load, simply supported] R_A: statics vs shooting integration (absolute difference) | 1.0000000 | 1.0000000 | 0.00e+0 | 1.0e-9 | PASS |
| [uniform load, simply supported] R_B: statics vs shooting integration (absolute difference) | 1.0000000 | 1.0000000 | 0.00e+0 | 1.0e-9 | PASS |
| [uniform load, simply supported] M(x) at every node: largest \|error\|/\|M\|max = 0.00e+0 (tolerance 1e-9) | true | true | 0.00e+0 | 0.0e+0 | PASS |
| [uniform load, simply supported] dM/dx = V at x = 0.325 m (relative to \|V\|max) (absolute difference) | -3.1141099e-11 | 0.0000000 | 3.11e-11 | 1.0e-6 | PASS |
| [uniform load, simply supported] dM/dx = V at x = 0.775 m (relative to \|V\|max) (absolute difference) | 4.1036401e-11 | 0.0000000 | 4.10e-11 | 1.0e-6 | PASS |
| [uniform load, simply supported] dM/dx = V at x = 1.425 m (relative to \|V\|max) (absolute difference) | 1.1699725e-10 | 0.0000000 | 1.17e-10 | 1.0e-6 | PASS |
| [uniform load, simply supported] dM/dx = V at x = 2.075 m (relative to \|V\|max) (absolute difference) | -3.5273872e-10 | 0.0000000 | 3.53e-10 | 1.0e-6 | PASS |
| hand value: 4-point bending, M = (P/2)a = 2000 N·m | 2000.0000 | 2000.0000 | 1.14e-16 | 1.0e-12 | PASS |
| hand value: cantilever with triangular load, fixed-end moment w₀L²/3 | 8000.0000 | 8000.0000 | 0.00e+0 | 1.0e-12 | PASS |
| hand value: overhang, M over the roller = −4 kN·m | -4000.0000 | -4000.0000 | 1.75e-12 | 1.0e-9 | PASS |
| triangular load: trapezoid integration converges at second order (observed 2.000) | true | true | 0.00e+0 | 0.0e+0 | PASS |
| rectangle: I = bh³/12 (transformed routine) | 2.7748762e-7 | 2.7748762e-7 | 0.00e+0 | 1.0e-12 | PASS |
| rectangle, elastic: M = EIκ vs strip summation (N = 2000) | 1911.8892 | 1911.8897 | 2.50e-7 | 1.0e-6 | PASS |
| rectangle, elastic: neutral axis at mid-depth (relative to h) (absolute difference) | 3.4148100e-16 | 0.0000000 | 3.41e-16 | 1.0e-12 | PASS |
| composite: transformed-section centroid vs hand formula | 0.024003537 | 0.024003537 | 0.00e+0 | 1.0e-12 | PASS |
| composite: transformed I vs hand formula | 5.6471915e-7 | 5.6471915e-7 | 0.00e+0 | 1.0e-12 | PASS |
| composite: neutral axis, transformed section vs strip equilibrium | 0.024003537 | 0.024003537 | 1.45e-16 | 1.0e-9 | PASS |
| composite: M = E₁I_tκ vs strip summation | 1556.3656 | 1556.3660 | 2.13e-7 | 1.0e-6 | PASS |
| composite: steel stress = n × aluminum stress at the same strain | 2.9753266 | 2.9753266 | 0.00e+0 | 1.0e-12 | PASS |
| EPP rectangle at κ = 0.5κ_Y: §4.6 formula vs strip summation (N = 2000) | 1496.6848 | 1496.6852 | 2.50e-7 | 2.0e-6 | PASS |
| EPP rectangle at κ = 1κ_Y: §4.6 formula vs strip summation (N = 2000) | 2993.3696 | 2993.3704 | 2.50e-7 | 2.0e-6 | PASS |
| EPP rectangle at κ = 1.5κ_Y: §4.6 formula vs strip summation (N = 2000) | 3824.8619 | 3824.8621 | 6.53e-8 | 2.0e-6 | PASS |
| EPP rectangle at κ = 3κ_Y: §4.6 formula vs strip summation (N = 2000) | 4323.7569 | 4323.7572 | 5.76e-8 | 2.0e-6 | PASS |
| EPP rectangle at κ = 10κ_Y: §4.6 formula vs strip summation (N = 2000) | 4475.0879 | 4475.0887 | 1.67e-7 | 2.0e-6 | PASS |
| Beer's form (3/2)M_Y[1 − ⅓(y_Y/c)²] at κ = 1.5κ_Y | 3824.8621 | 3824.8621 | 0.00e+0 | 1.0e-14 | PASS |
| Beer's form (3/2)M_Y[1 − ⅓(y_Y/c)²] at κ = 3κ_Y | 4323.7572 | 4323.7572 | 0.00e+0 | 1.0e-14 | PASS |
| rectangle: plastic modulus Z = bh²/4 (equal-area routine) | 0.000016387064 | 0.000016387064 | 0.00e+0 | 1.0e-12 | PASS |
| rectangle: shape factor M_p/M_Y = 1.5 | 1.5000000 | 1.5000000 | 0.00e+0 | 1.0e-12 | PASS |
| strip summation converges at second order (observed 1.979) | true | true | 0.00e+0 | 0.0e+0 | PASS |
| residual stresses: net force / (σ_Y A) = 0 (absolute difference) | 1.6895171e-15 | 0.0000000 | 1.69e-15 | 1.0e-6 | PASS |
| residual stresses: net moment / M_Y = 0 (absolute difference) | -9.0277778e-8 | 0.0000000 | 9.03e-8 | 1.0e-6 | PASS |
| inverse: κ for M = 1.3 M_Y (bisection on strips) vs the §4.6 formula inverted | 0.24755264 | 0.24755268 | 1.54e-7 | 1.0e-5 | PASS |
| I-section: plastic modulus vs hand formula b t_f(h − t_f) + t_w h_w²/4 | 0.00023860000 | 0.00023860000 | 2.27e-16 | 1.0e-12 | PASS |
| I-section: fully plastic moment σ_Y Z vs strip summation at κ = 10⁴κ_Y | 59650.000 | 59650.000 | 4.03e-15 | 1.0e-5 | PASS |
| I-section: I vs hand formula | 0.000020982667 | 0.000020982667 | 4.84e-16 | 1.0e-12 | PASS |
| T-section: fully plastic moment σ_Y Z vs strip summation | 28120.832 | 28120.833 | 2.96e-8 | 1.0e-4 | PASS |
| T-section: plastic neutral axis divides the area equally (strip vs equal-area routine) | 0.17832833 | 0.17833333 | 2.80e-5 | 1.0e-3 | PASS |
| units: 1 kN·m = 8850.7 lb·in | 8850.7458 | 8850.7460 | 2.36e-8 | 1.0e-6 | PASS |
| units: 1 in³ = 16 387 mm³ | 16387.064 | 16387.064 | 0.00e+0 | 1.0e-7 | PASS |

79 of 79 passed.

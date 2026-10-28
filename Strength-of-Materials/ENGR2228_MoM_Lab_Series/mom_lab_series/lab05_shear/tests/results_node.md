## Lab 5 — simulation model (Node, exact page code)

| Test | Value | Reference | Rel. difference | Tolerance | Result |
|---|---:|---:|---:|---:|---|
| rectangle: I = bh³/12 | 2.7748762e-7 | 2.7748762e-7 | 0.00e+0 | 1.0e-13 | PASS |
| rectangle: Q at the NA = bh²/8 | 0.0000081935320 | 0.0000081935320 | 0.00e+0 | 1.0e-13 | PASS |
| rectangle: τ_max = 3V/(2A) (Beer §6.1C) | 8718767.4 | 8718767.4 | 0.00e+0 | 1.0e-13 | PASS |
| rectangle: energy shear factor f_s = 6/5 | 1.2000000 | 1.2000000 | 1.85e-16 | 1.0e-13 | PASS |
| rectangle: f_s by strips (N_s = 2000) vs 6/5 | 1.2000006 | 1.2000000 | 5.00e-7 | 1.0e-6 | PASS |
| rectangle: I by strips (N_s = 2000) | 2.7748755e-7 | 2.7748762e-7 | 2.50e-7 | 1.0e-6 | PASS |
| rectangle: strip error in I falls as N_s⁻² (observed 2.000) | true | true | 0.00e+0 | 0.0e+0 | PASS |
| I-section: I vs hand formula | 0.0000024792604 | 0.0000024792604 | 8.54e-16 | 1.0e-13 | PASS |
| I-section: Q at the NA = B t_f (H − t_f)/2 + t_w h_w²/8 | 0.000027786235 | 0.000027786235 | 7.32e-16 | 1.0e-13 | PASS |
| I-section: τ in the web at the NA = VQ/(I t_w) | 23348895 | 23348895 | 1.60e-16 | 1.0e-13 | PASS |
| I-section: τ in the web at the junction = V B t_f (H − t_f)/(2 I t_w) | 19364233 | 19364233 | 8.85e-15 | 1.0e-9 | PASS |
| I-section: shear flow is continuous at the junction (q = VQ/I either side) | 0.000023044309 | 0.000023044309 | 1.56e-10 | 1.0e-6 | PASS |
| I-section: f_s exact layer integral vs strips (N_s = 4000) | 2.9007455 | 2.9007454 | 6.05e-8 | 5.0e-6 | PASS |
| I-section: f_s = 2.9007 lies between 1 and A/A_web = 3.2679 | true | true | 0.00e+0 | 0.0e+0 | PASS |
| tee: neutral axis, layer sums vs strips | 0.088883721 | 0.088883721 | 1.97e-14 | 1.0e-12 | PASS |
| tee: Q at the NA, layer formula vs strips | 0.000031601263 | 0.000031601263 | 7.48e-14 | 1.0e-9 | PASS |
| tee: f_s, exact integral vs strips (N_s = 4000) | 2.4083604 | 2.4083601 | 1.16e-7 | 5.0e-6 | PASS |
| tee: Q of the area above the NA = Q of the area below | 0.000031601263 | 0.000031601263 | 2.14e-16 | 1.0e-12 | PASS |
| box: neutral axis, layer sums vs strips | 0.060000000 | 0.060000000 | 3.63e-14 | 1.0e-12 | PASS |
| box: Q at the NA, layer formula vs strips | 0.000039024000 | 0.000039024000 | 5.05e-14 | 1.0e-9 | PASS |
| box: f_s, exact integral vs strips (N_s = 4000) | 1.9602791 | 1.9602790 | 6.91e-8 | 5.0e-6 | PASS |
| box: Q of the area above the NA = Q of the area below | 0.000039024000 | 0.000039024000 | 3.47e-16 | 1.0e-12 | PASS |
| circle: τ_max = 4V/(3A) (Beer §6.1C) | 13581222 | 13581222 | 0.00e+0 | 1.0e-13 | PASS |
| circle: f_s = 10/9 vs strips (N_s = 20000) | 1.1111110 | 1.1111111 | 6.08e-8 | 2.0e-5 | PASS |
| circle: strip error in I converges at order 1.5 (width ∝ √distance at the poles; observed 1.430) | true | true | 0.00e+0 | 0.0e+0 | PASS |
| b/h = 0.5: face value τ/(VQ/Ib), series vs finite differences (96 cells) | 1.0412412 | 1.0412594 | 1.76e-5 | 1.0e-3 | PASS |
| b/h = 0.5: center value, series vs finite differences | 0.97942628 | 0.97941716 | 9.31e-6 | 1.0e-3 | PASS |
| b/h = 0.5: width-average of the elasticity solution = VQ/(Ib) (∫τ dx = VQ/I) | 1.0000000 | 1.0000000 | 2.37e-12 | 1.0e-6 | PASS |
| b/h = 0.5: finite-difference error falls as N⁻² (observed 2.001) | true | true | 0.00e+0 | 0.0e+0 | PASS |
| b/h = 2: face value τ/(VQ/Ib), series vs finite differences (96 cells) | 1.4910450 | 1.4917613 | 4.80e-4 | 1.0e-3 | PASS |
| b/h = 2: center value, series vs finite differences | 0.82162718 | 0.82152440 | 1.25e-4 | 1.0e-3 | PASS |
| b/h = 2: width-average of the elasticity solution = VQ/(Ib) (∫τ dx = VQ/I) | 1.0000000 | 1.0000000 | 1.02e-11 | 1.0e-6 | PASS |
| b/h = 2: finite-difference error falls as N⁻² (observed 1.943) | true | true | 0.00e+0 | 0.0e+0 | PASS |
| ν = 0: the elasticity solution is the elementary one (b/h = 2) | 1.0000000 | 1.0000000 | 0.00e+0 | 1.0e-14 | PASS |
| ν = 0.25, b/h = 0.5: face value matches the value tabulated in Beer §6.1C (3 figures) | 1.0332576 | 1.0330000 | 2.49e-4 | 5.0e-4 | PASS |
| ν = 0.25, b/h = 2: face value matches the value tabulated in Beer §6.1C (3 figures) | 1.3963894 | 1.3960000 | 2.79e-4 | 5.0e-4 | PASS |
| ν = 0.25, b/h = 4: face value matches the value tabulated in Beer §6.1C (3 figures) | 1.9879350 | 1.9880000 | 3.27e-5 | 5.0e-4 | PASS |
| [ibeamSpan] deflection: closed form vs 256 reduced-integration elements | 0.0021395416 | 0.0021395687 | 1.27e-5 | 2.0e-5 | PASS |
| [ibeamSpan] element error falls as N_e⁻² (observed 2.000) | true | true | 0.00e+0 | 0.0e+0 | PASS |
| [ibeamSpan] span with a 5 % shear part: closed form vs bisection on the elements | 1.7675406 | 1.7685652 | 5.79e-4 | 2.0e-3 | PASS |
| [ibeamSpan] slender limit (L/h = 50): elements → Euler–Bernoulli within the shear part | 0.32173239 | 0.31977060 | 6.13e-3 | 9.6e-3 | PASS |
| [cantilever] deflection: closed form vs 256 reduced-integration elements | 0.00032113862 | 0.00032113975 | 3.49e-6 | 2.0e-5 | PASS |
| [cantilever] element error falls as N_e⁻² (observed 2.000) | true | true | 0.00e+0 | 0.0e+0 | PASS |
| [cantilever] span with a 5 % shear part: closed form vs bisection on the elements | 0.19777847 | 0.19780714 | 1.45e-4 | 2.0e-3 | PASS |
| [cantilever] slender limit (L/h = 50): elements → Euler–Bernoulli within the shear part | 1.4288912 | 1.4285225 | 2.58e-4 | 4.8e-4 | PASS |
| shear locking: 4 fully integrated elements give 11.6 % of the deflection (< 50 %) | true | true | 0.00e+0 | 0.0e+0 | PASS |
| rectangle: δ_shear/δ_bending = 3EI f_s/(GA L²) for a cantilever (closed form vs formula) | 0.0020593507 | 0.0020593507 | 2.11e-16 | 1.0e-12 | PASS |
| [bolts, point load] midspan deflection: closed form vs finite differences (4000 intervals) | 0.0043544438 | 0.0043544432 | 1.28e-7 | 2.0e-6 | PASS |
| [bolts, point load] end slip: closed form vs finite differences | 0.00015577141 | 0.00015577139 | 1.18e-7 | 2.0e-4 | PASS |
| [bolts, point load] δ_full ≤ δ ≤ δ_loose | true | true | 0.00e+0 | 0.0e+0 | PASS |
| [glue, point load] midspan deflection: closed form vs finite differences (4000 intervals) | 0.0023568710 | 0.0023568707 | 1.28e-7 | 2.0e-6 | PASS |
| [glue, point load] end slip: closed form vs finite differences | 1.8164099e-7 | 1.8164099e-7 | 1.89e-14 | 2.0e-4 | PASS |
| [glue, point load] δ_full ≤ δ ≤ δ_loose | true | true | 0.00e+0 | 0.0e+0 | PASS |
| [bolts, uniform load] midspan deflection: closed form vs finite differences (4000 intervals) | 0.0077862472 | 0.0077862468 | 3.92e-8 | 2.0e-6 | PASS |
| [bolts, uniform load] end slip: closed form vs finite differences | 0.00016974541 | 0.00016974532 | 5.61e-7 | 2.0e-4 | PASS |
| [bolts, uniform load] δ_full ≤ δ ≤ δ_loose | true | true | 0.00e+0 | 0.0e+0 | PASS |
| [loose, point load] midspan deflection: closed form vs finite differences (4000 intervals) | 0.0094147703 | 0.0094147692 | 1.25e-7 | 2.0e-6 | PASS |
| [loose, point load] end slip: closed form vs finite differences | 0.00059783784 | 0.00059783784 | 0.00e+0 | 2.0e-4 | PASS |
| [loose, point load] δ_full ≤ δ ≤ δ_loose | true | true | 0.00e+0 | 0.0e+0 | PASS |
| [loose, uniform load] midspan deflection: closed form vs finite differences (4000 intervals) | 0.024076634 | 0.024076633 | 5.00e-8 | 2.0e-6 | PASS |
| [loose, uniform load] end slip: closed form vs finite differences | 0.0016051088 | 0.0016051089 | 6.25e-8 | 2.0e-4 | PASS |
| [loose, uniform load] δ_full ≤ δ ≤ δ_loose | true | true | 0.00e+0 | 0.0e+0 | PASS |
| [soft glue, uniform load] midspan deflection: closed form vs finite differences (4000 intervals) | 0.0064425468 | 0.0064425465 | 4.67e-8 | 2.0e-6 | PASS |
| [soft glue, uniform load] end slip: closed form vs finite differences | 0.000043207690 | 0.000043207645 | 1.04e-6 | 2.0e-4 | PASS |
| [soft glue, uniform load] δ_full ≤ δ ≤ δ_loose | true | true | 0.00e+0 | 0.0e+0 | PASS |
| loose limit: k → 0 gives PL³/(48EI₀) | 0.0094147692 | 0.0094147692 | 4.79e-15 | 1.0e-9 | PASS |
| bonded limit: k → ∞ gives PL³/(48EI_full) | 0.0023536924 | 0.0023536923 | 5.56e-8 | 1.0e-6 | PASS |
| two equal layers: EI_full = 4 EI₀ | 4.0000000 | 4.0000000 | 0.00e+0 | 1.0e-12 | PASS |
| loose end slip = r θ_end = r PL²/(16EI₀) | 0.00059783784 | 0.00059783784 | 0.00e+0 | 1.0e-12 | PASS |
| closed form: small-αL series and full formula join at αL/2 = 0.05 (point load) | 0.0094077152 | 0.0094077152 | 7.72e-10 | 1.0e-9 | PASS |
| closed form: series and full formula join at αL/2 = 0.05 (uniform load) | 0.024058293 | 0.024058293 | 8.57e-10 | 1.0e-9 | PASS |
| finite-difference error falls as n⁻² (observed 1.995) | true | true | 0.00e+0 | 0.0e+0 | PASS |
| discrete springs at 5 mm spacing → smeared closed form | 0.0043546541 | 0.0043544432 | 4.84e-5 | 2.0e-4 | PASS |
| discrete springs: shooting leaves N(L) = 0 (relative to the largest bolt force) (absolute difference) | -3.2543609e-14 | 0.0000000 | 3.25e-14 | 1.0e-10 | PASS |
| discrete springs: forces antisymmetric about midspan | -6036.5418 | -6036.5418 | 1.85e-14 | 1.0e-9 | PASS |
| Beer's q for two equal layers = 3V/(4t) | 73818.898 | 73818.898 | 0.00e+0 | 1.0e-12 | PASS |
| units: 1 N/mm = 5.7101 lb/in | 5.7101472 | 5.7101470 | 2.71e-8 | 1.0e-6 | PASS |
| units: 1 kN/mm = 5.7101 kip/in | 5.7101472 | 5.7101470 | 2.71e-8 | 1.0e-6 | PASS |
| units: 1 N·m² = 348.45 lb·in² | 348.45456 | 348.45456 | 0.00e+0 | 1.0e-12 | PASS |

79 of 79 passed.

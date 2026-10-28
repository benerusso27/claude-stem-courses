## Lab 5 — independent checks (Python/scipy) and data-pipeline closure

| Test | Value | Reference | Rel. difference | Tolerance | Result |
|---|---:|---:|---:|---:|---|
| rectUp: I, JavaScript layer sums vs Python quadrature | 2.7748762e-07 | 2.7748762e-07 | 1.91e-16 | 1.0e-11 | PASS |
| rectUp: neutral axis | 0.0254 | 0.0254 | 0.00e+00 | 1.0e-11 | PASS |
| rectUp: Q at the NA | 8.193532e-06 | 8.193532e-06 | 4.14e-16 | 1.0e-11 | PASS |
| rectUp: f_s, JavaScript exact antiderivative vs Python nested quadrature | 1.2 | 1.2 | 1.85e-16 | 1.0e-08 | PASS |
| rectUp: τ = VQ/(It) at y = 5.08 mm | 3138756.3 | 3138756.3 | 1.48e-16 | 1.0e-10 | PASS |
| rectUp: τ = VQ/(It) at y = 15.24 mm | 7323764.6 | 7323764.6 | 7.63e-16 | 1.0e-10 | PASS |
| rectUp: τ = VQ/(It) at y = 22.86 mm | 8631579.8 | 8631579.8 | 4.32e-16 | 1.0e-10 | PASS |
| ibeamWeb: I, JavaScript layer sums vs Python quadrature | 2.4792604e-06 | 2.4792604e-06 | 1.71e-16 | 1.0e-11 | PASS |
| ibeamWeb: neutral axis | 0.0508 | 0.0508 | 0.00e+00 | 1.0e-11 | PASS |
| ibeamWeb: Q at the NA | 2.7786235e-05 | 2.7786235e-05 | 3.66e-16 | 1.0e-11 | PASS |
| ibeamWeb: f_s, JavaScript exact antiderivative vs Python nested quadrature | 2.9007454 | 2.9007454 | 1.07e-15 | 1.0e-08 | PASS |
| ibeamWeb: τ = VQ/(It) at y = 10.16 mm | 20018043 | 20018043 | 3.72e-16 | 1.0e-10 | PASS |
| ibeamWeb: τ = VQ/(It) at y = 30.48 mm | 22516182 | 22516182 | 4.96e-16 | 1.0e-10 | PASS |
| ibeamWeb: τ = VQ/(It) at y = 45.72 mm | 23296850 | 23296850 | 4.80e-16 | 1.0e-10 | PASS |
| tee: I, JavaScript layer sums vs Python quadrature | 2.6625801e-06 | 2.6625801e-06 | 1.59e-16 | 1.0e-11 | PASS |
| tee: neutral axis | 0.088883721 | 0.088883721 | 0.00e+00 | 1.0e-11 | PASS |
| tee: Q at the NA | 3.1601263e-05 | 3.1601263e-05 | 4.29e-16 | 1.0e-11 | PASS |
| tee: f_s, JavaScript exact antiderivative vs Python nested quadrature | 2.4083601 | 2.4083601 | 5.53e-16 | 1.0e-08 | PASS |
| tee: τ = VQ/(It) at y = 12.00 mm | 7470983.9 | 7470983.9 | 9.97e-16 | 1.0e-10 | PASS |
| tee: τ = VQ/(It) at y = 36.00 mm | 19167979 | 19167979 | 7.77e-16 | 1.0e-10 | PASS |
| tee: τ = VQ/(It) at y = 54.00 mm | 25101374 | 25101374 | 2.97e-16 | 1.0e-10 | PASS |
| box: I, JavaScript layer sums vs Python quadrature | 3.961728e-06 | 3.961728e-06 | 2.14e-16 | 1.0e-11 | PASS |
| box: neutral axis | 0.06 | 0.06 | 2.31e-16 | 1.0e-11 | PASS |
| box: Q at the NA | 3.9024e-05 | 3.9024e-05 | 3.47e-16 | 1.0e-11 | PASS |
| box: f_s, JavaScript exact antiderivative vs Python nested quadrature | 1.960279 | 1.960279 | 1.70e-15 | 1.0e-08 | PASS |
| box: τ = VQ/(It) at y = 12.00 mm | 18809974 | 18809974 | 5.94e-16 | 1.0e-10 | PASS |
| box: τ = VQ/(It) at y = 36.00 mm | 23171707 | 23171707 | 8.04e-16 | 1.0e-10 | PASS |
| box: τ = VQ/(It) at y = 54.00 mm | 24534748 | 24534748 | 7.59e-16 | 1.0e-10 | PASS |
| circle: I = πc⁴/4, JavaScript vs Python | 3.0679616e-07 | 3.0679616e-07 | 0.00e+00 | 1.0e-13 | PASS |
| circle: f_s, JavaScript 10/9 vs Python adaptive quadrature | 1.1111111 | 1.1111111 | 1.59e-09 | 1.0e-08 | PASS |
| circle: τ_max, JavaScript vs Python | 13581222 | 13581222 | 2.74e-16 | 1.0e-12 | PASS |
| wide rectangle b = 25.4, h = 50.8 mm, ν = 0.33, x = 1·b/2: τ/(VQ/Ib), cosine series in y (JS) vs sine series in x (Python) | 1.0412594 | 1.0412594 | 1.51e-09 | 2.0e-07 | PASS |
| wide rectangle b = 25.4, h = 50.8 mm, ν = 0.33, x = 0·b/2: τ/(VQ/Ib), cosine series in y (JS) vs sine series in x (Python) | 0.97941716 | 0.97941716 | 6.55e-14 | 2.0e-07 | PASS |
| wide rectangle b = 25.4, h = 50.8 mm, ν = 0.33, x = 0.5·b/2: τ/(VQ/Ib), cosine series in y (JS) vs sine series in x (Python) | 0.99483087 | 0.99483087 | 6.44e-14 | 2.0e-07 | PASS |
| wide rectangle b = 50.8, h = 25.4 mm, ν = 0.33, x = 1·b/2: τ/(VQ/Ib), cosine series in y (JS) vs sine series in x (Python) | 1.4917613 | 1.4917613 | 4.21e-09 | 2.0e-07 | PASS |
| wide rectangle b = 50.8, h = 25.4 mm, ν = 0.33, x = 0·b/2: τ/(VQ/Ib), cosine series in y (JS) vs sine series in x (Python) | 0.8215244 | 0.8215244 | 5.82e-12 | 2.0e-07 | PASS |
| wide rectangle b = 50.8, h = 25.4 mm, ν = 0.33, x = 0.5·b/2: τ/(VQ/Ib), cosine series in y (JS) vs sine series in x (Python) | 0.92587603 | 0.92587603 | 5.16e-12 | 2.0e-07 | PASS |
| wide rectangle b = 40.0, h = 10.0 mm, ν = 0.25, x = 1·b/2: τ/(VQ/Ib), cosine series in y (JS) vs sine series in x (Python) | 1.987935 | 1.987935 | 5.10e-09 | 2.0e-07 | PASS |
| wide rectangle b = 40.0, h = 10.0 mm, ν = 0.25, x = 0·b/2: τ/(VQ/Ib), cosine series in y (JS) vs sine series in x (Python) | 0.80484383 | 0.80484383 | 1.99e-11 | 2.0e-07 | PASS |
| wide rectangle b = 40.0, h = 10.0 mm, ν = 0.25, x = 0.5·b/2: τ/(VQ/Ib), cosine series in y (JS) vs sine series in x (Python) | 0.85613785 | 0.85613785 | 1.87e-11 | 2.0e-07 | PASS |
| wide rectangle b = 10.0, h = 30.0 mm, ν = 0.3, x = 1·b/2: τ/(VQ/Ib), cosine series in y (JS) vs sine series in x (Python) | 1.0170923 | 1.0170923 | 9.58e-10 | 2.0e-07 | PASS |
| wide rectangle b = 10.0, h = 30.0 mm, ν = 0.3, x = 0·b/2: τ/(VQ/Ib), cosine series in y (JS) vs sine series in x (Python) | 0.99145467 | 0.99145467 | 1.04e-13 | 2.0e-07 | PASS |
| wide rectangle b = 10.0, h = 30.0 mm, ν = 0.3, x = 0.5·b/2: τ/(VQ/Ib), cosine series in y (JS) vs sine series in x (Python) | 0.99786325 | 0.99786325 | 1.03e-13 | 2.0e-07 | PASS |
| [ibeamSpan] Timoshenko bending part, JavaScript vs Python | 0.0017781767 | 0.0017781767 | 0.00e+00 | 1.0e-13 | PASS |
| [ibeamSpan] Timoshenko shear part | 0.00036139195 | 0.00036139195 | 0.00e+00 | 1.0e-13 | PASS |
| [cantilever] Timoshenko bending part, JavaScript vs Python | 0.00029421154 | 0.00029421154 | 0.00e+00 | 1.0e-13 | PASS |
| [cantilever] Timoshenko shear part | 2.6928211e-05 | 2.6928211e-05 | 1.26e-16 | 1.0e-13 | PASS |
| [bolts, point, L = 0.6 m, s = 100/100 mm] midspan deflection: JavaScript closed form vs scipy solve_bvp | 0.0043544432 | 0.0043544432 | 5.98e-16 | 2.0e-07 | PASS |
| [bolts, point, L = 0.6 m, s = 100/100 mm] end slip: closed form vs solve_bvp | 0.00015577139 | 0.00015577139 | 1.57e-15 | 2.0e-05 | PASS |
| [bolts, point, L = 0.6 m, s = 100/100 mm] discrete springs: midspan deflection, JavaScript vs Python | 0.0044342683 | 0.0044342683 | 0.00e+00 | 1.0e-10 | PASS |
| [bolts, point, L = 0.6 m, s = 100/100 mm] discrete springs: end slip | 0.00016752015 | 0.00016752015 | 1.62e-16 | 1.0e-09 | PASS |
| [bolts, point, L = 0.6 m, s = 100/100 mm] discrete springs: largest bolt force | 6036.5418 | 6036.5418 | 0.00e+00 | 1.0e-09 | PASS |
| [glue, point, L = 0.6 m] midspan deflection: JavaScript closed form vs scipy solve_bvp | 0.0023568707 | 0.0023568707 | 3.44e-14 | 2.0e-07 | PASS |
| [glue, point, L = 0.6 m] end slip: closed form vs solve_bvp | 1.8164099e-07 | 1.8164099e-07 | 2.91e-16 | 2.0e-05 | PASS |
| [bolts, udl, L = 2.4 m, s = 100/100 mm] midspan deflection: JavaScript closed form vs scipy solve_bvp | 0.0077862468 | 0.0077862468 | 5.57e-16 | 2.0e-07 | PASS |
| [bolts, udl, L = 2.4 m, s = 100/100 mm] end slip: closed form vs solve_bvp | 0.00016974532 | 0.00016974532 | 0.00e+00 | 2.0e-05 | PASS |
| [bolts, udl, L = 2.4 m, s = 100/100 mm] discrete springs: midspan deflection, JavaScript vs Python | 0.007806996 | 0.007806996 | 3.16e-14 | 1.0e-10 | PASS |
| [bolts, udl, L = 2.4 m, s = 100/100 mm] discrete springs: end slip | 0.00017275034 | 0.00017275034 | 0.00e+00 | 1.0e-09 | PASS |
| [bolts, udl, L = 2.4 m, s = 100/100 mm] discrete springs: largest bolt force | 11281.242 | 11281.242 | 6.31e-13 | 1.0e-09 | PASS |
| [glue, udl, L = 2.4 m] midspan deflection: JavaScript closed form vs scipy solve_bvp | 0.0064425465 | 0.0064425465 | 4.04e-16 | 2.0e-07 | PASS |
| [glue, udl, L = 2.4 m] end slip: closed form vs solve_bvp | 4.3207645e-05 | 4.3207645e-05 | 0.00e+00 | 2.0e-05 | PASS |
| [bolts, point, L = 0.6 m, s = 300/300 mm] midspan deflection: JavaScript closed form vs scipy solve_bvp | 0.0061586621 | 0.0061586621 | 4.23e-16 | 2.0e-07 | PASS |
| [bolts, point, L = 0.6 m, s = 300/300 mm] end slip: closed form vs solve_bvp | 0.0003117404 | 0.0003117404 | 3.48e-16 | 2.0e-05 | PASS |
| [bolts, point, L = 0.6 m, s = 300/300 mm] discrete springs: midspan deflection, JavaScript vs Python | 0.0063215415 | 0.0063215415 | 1.37e-16 | 1.0e-10 | PASS |
| [bolts, point, L = 0.6 m, s = 300/300 mm] discrete springs: end slip | 0.00036504382 | 0.00036504382 | 1.49e-16 | 1.0e-09 | PASS |
| [bolts, point, L = 0.6 m, s = 300/300 mm] discrete springs: largest bolt force | 8623.3743 | 8623.3743 | 2.11e-16 | 1.0e-09 | PASS |
| [bolts, udl, L = 2.4 m, s = 70/210 mm] discrete springs: midspan deflection, JavaScript vs Python | 0.007391357 | 0.007391357 | 8.73e-14 | 1.0e-10 | PASS |
| [bolts, udl, L = 2.4 m, s = 70/210 mm] discrete springs: end slip | 0.00012606693 | 0.00012606693 | 2.15e-16 | 1.0e-09 | PASS |
| [bolts, udl, L = 2.4 m, s = 70/210 mm] discrete springs: largest bolt force | 8298.1859 | 8298.1859 | 2.19e-16 | 1.0e-09 | PASS |
| closure: Part A upright: face τ/(VQ/Ib) recovered within U = 0.0181 (value 1.04234, truth 1.05068) — truth × gage-factor and G biases | True | True | 0.00e+00 | 0.0e+00 | PASS |
| closure: Part A flat: face τ/(VQ/Ib) recovered within U = 0.0287 (value 1.51456, truth 1.50426) — truth × gage-factor and G biases | True | True | 0.00e+00 | 0.0e+00 | PASS |
| closure: Part B web gage 1: τ per newton of V (MPa/N) recovered within U = 3.98e-05 (value 0.00235738, truth 0.00235578) | True | True | 0.00e+00 | 0.0e+00 | PASS |
| closure: Part B web gage 2: τ per newton of V (MPa/N) recovered within U = 3.63e-05 (value 0.00224911, truth 0.00225369) | True | True | 0.00e+00 | 0.0e+00 | PASS |
| closure: Part B web gage 3: τ per newton of V (MPa/N) recovered within U = 3.25e-05 (value 0.00201228, truth 0.00201207) | True | True | 0.00e+00 | 0.0e+00 | PASS |
| closure: Part B: E from the deflection fit (GPa) recovered within U = 0.604 (value 68.6646, truth 68.6939) — truth / LVDT gain | True | True | 0.00e+00 | 0.0e+00 | PASS |
| closure: Part B: G from the deflection fit (GPa) recovered within U = 0.27 (value 25.8375, truth 25.8248) — truth / LVDT gain | True | True | 0.00e+00 | 0.0e+00 | PASS |
| closure: Part B: shear factor f_s of the measured section vs truth section recovered within U = 0.0058 (value 2.9015, truth 2.90075) | True | True | 0.00e+00 | 0.0e+00 | PASS |
| closure: Part C: bolt slip modulus from the bolted deflection (N/m) recovered within U = 1.2e+06 (value 4.01558e+07, truth 4e+07) — E from Lab 2, dimensions measured | True | True | 0.00e+00 | 0.0e+00 | PASS |
| closure: Part C: loose end slip per newton (m/N) recovered within U = 2.01e-09 (value 2.39535e-07, truth 2.39041e-07) | True | True | 0.00e+00 | 0.0e+00 | PASS |
| closure: Part C: bonded effective EI = full composite (N·m²) recovered within U = 89.3 (value 4761.15, truth 4767.3) | True | True | 0.00e+00 | 0.0e+00 | PASS |

80 of 80 passed.

## Lab 3 — independent checks (Python/scipy) and data-pipeline closure

| Test | Value | Reference | Rel. difference | Tolerance | Result |
|---|---:|---:|---:|---:|---|
| EPP torque, c = 3.17 mm, c_i/c = 0, θ = 0.4715: JavaScript vs Python | 5.982711 | 5.982711 | 0.00e+00 | 1.0e-13 | PASS |
|     … closed form vs scipy.quad of the EPP law | 5.982711 | 5.982711 | 1.48e-16 | 1.0e-10 | PASS |
| EPP torque, c = 3.17 mm, c_i/c = 0, θ = 1.01: JavaScript vs Python | 10.551519 | 10.551519 | 0.00e+00 | 1.0e-13 | PASS |
|     … closed form vs scipy.quad of the EPP law | 10.551519 | 10.551519 | 3.37e-16 | 1.0e-10 | PASS |
| EPP torque, c = 3.17 mm, c_i/c = 0, θ = 2.694: JavaScript vs Python | 11.351126 | 11.351126 | 0.00e+00 | 1.0e-13 | PASS |
|     … closed form vs scipy.quad of the EPP law | 11.351126 | 11.351126 | 0.00e+00 | 1.0e-10 | PASS |
| EPP torque, c = 3.17 mm, c_i/c = 0, θ = 33.68: JavaScript vs Python | 11.395617 | 11.395617 | 0.00e+00 | 1.0e-13 | PASS |
|     … closed form vs scipy.quad of the EPP law | 11.395617 | 11.395617 | 1.56e-16 | 1.0e-10 | PASS |
| EPP torque, c = 3.17 mm, c_i/c = 0.6, θ = 0.4715: JavaScript vs Python | 5.2073517 | 5.2073517 | 0.00e+00 | 1.0e-13 | PASS |
|     … closed form vs scipy.quad of the EPP law | 5.2073517 | 5.2073517 | 1.71e-16 | 1.0e-10 | PASS |
| EPP torque, c = 3.17 mm, c_i/c = 0.6, θ = 1.01: JavaScript vs Python | 8.8900343 | 8.8900343 | 0.00e+00 | 1.0e-13 | PASS |
|     … closed form vs scipy.quad of the EPP law | 8.8900343 | 8.8900343 | 4.00e-16 | 1.0e-10 | PASS |
| EPP torque, c = 3.17 mm, c_i/c = 0.6, θ = 2.694: JavaScript vs Python | 8.9341818 | 8.9341818 | 1.99e-16 | 1.0e-13 | PASS |
|     … closed form vs scipy.quad of the EPP law | 8.9341818 | 8.9341818 | 0.00e+00 | 1.0e-10 | PASS |
| EPP torque, c = 3.17 mm, c_i/c = 0.6, θ = 33.68: JavaScript vs Python | 8.9341818 | 8.9341818 | 1.99e-16 | 1.0e-13 | PASS |
|     … closed form vs scipy.quad of the EPP law | 8.9341818 | 8.9341818 | 0.00e+00 | 1.0e-10 | PASS |
| EPP torque, c = 25 mm, c_i/c = 0.6, θ = 0.05987: JavaScript vs Python | 2542.1768 | 2542.1768 | 0.00e+00 | 1.0e-13 | PASS |
|     … closed form vs scipy.quad of the EPP law | 2542.1768 | 2542.1768 | 0.00e+00 | 1.0e-10 | PASS |
| EPP torque, c = 25 mm, c_i/c = 0.6, θ = 0.1283: JavaScript vs Python | 4340.0254 | 4340.0254 | 0.00e+00 | 1.0e-13 | PASS |
|     … closed form vs scipy.quad of the EPP law | 4340.0254 | 4340.0254 | 0.00e+00 | 1.0e-10 | PASS |
| EPP torque, c = 25 mm, c_i/c = 0.6, θ = 0.3421: JavaScript vs Python | 4361.5778 | 4361.5778 | 0.00e+00 | 1.0e-13 | PASS |
|     … closed form vs scipy.quad of the EPP law | 4361.5778 | 4361.5778 | 0.00e+00 | 1.0e-10 | PASS |
| EPP torque, c = 25 mm, c_i/c = 0.6, θ = 4.277: JavaScript vs Python | 4361.5778 | 4361.5778 | 0.00e+00 | 1.0e-13 | PASS |
|     … closed form vs scipy.quad of the EPP law | 4361.5778 | 4361.5778 | 0.00e+00 | 1.0e-10 | PASS |
| [steel] ring integration (N = 2048) vs scipy.quad of the same law, θ = 0.5388 rad/m — midpoint rule O(N⁻²) | 6.8373832 | 6.837384 | 1.19e-07 | 1.0e-06 | PASS |
| [steel] ring integration (N = 2048) vs scipy.quad of the same law, θ = 2.021 rad/m — midpoint rule O(N⁻²) | 11.290124 | 11.290125 | 5.68e-08 | 1.0e-06 | PASS |
| [steel] ring integration (N = 2048) vs scipy.quad of the same law, θ = 26.94 rad/m — midpoint rule O(N⁻²) | 14.563255 | 14.563256 | 7.33e-08 | 1.0e-06 | PASS |
| [al] ring integration (N = 2048) vs scipy.quad of the same law, θ = 1.531 rad/m — midpoint rule O(N⁻²) | 6.3368234 | 6.3368241 | 1.11e-07 | 1.0e-06 | PASS |
| [al] ring integration (N = 2048) vs scipy.quad of the same law, θ = 5.742 rad/m — midpoint rule O(N⁻²) | 10.909365 | 10.909366 | 6.49e-08 | 1.0e-06 | PASS |
| [al] ring integration (N = 2048) vs scipy.quad of the same law, θ = 76.56 rad/m — midpoint rule O(N⁻²) | 13.302221 | 13.302222 | 6.27e-08 | 1.0e-06 | PASS |
| [ci] ring integration (N = 2048) vs scipy.quad of the same law, θ = 1.315 rad/m — midpoint rule O(N⁻²) | 8.341705 | 8.341706 | 1.14e-07 | 1.0e-06 | PASS |
| rectangle a/b = 1: c₁ JavaScript vs Python series | 0.20816526 | 0.20816526 | 2.67e-16 | 1.0e-12 | PASS |
| rectangle a/b = 1: c₂ JavaScript vs Python series | 0.14057701 | 0.14057701 | 1.97e-16 | 1.0e-12 | PASS |
| rectangle a/b = 1.5: c₁ JavaScript vs Python series | 0.23096913 | 0.23096913 | 1.20e-16 | 1.0e-12 | PASS |
| rectangle a/b = 1.5: c₂ JavaScript vs Python series | 0.19576071 | 0.19576071 | 1.42e-16 | 1.0e-12 | PASS |
| rectangle a/b = 3: c₁ JavaScript vs Python series | 0.26720805 | 0.26720805 | 0.00e+00 | 1.0e-12 | PASS |
| rectangle a/b = 3: c₂ JavaScript vs Python series | 0.26331693 | 0.26331693 | 0.00e+00 | 1.0e-12 | PASS |
| rectangle a/b = 10: c₁ JavaScript vs Python series | 0.31232511 | 0.31232511 | 1.78e-16 | 1.0e-12 | PASS |
| rectangle a/b = 10: c₂ JavaScript vs Python series | 0.31232504 | 0.31232504 | 1.78e-16 | 1.0e-12 | PASS |
| rectangle FD a/b = 1, N = 8: conjugate gradients (page) vs sparse direct solve (scipy), c₂ | 0.13369212 | 0.13369212 | 4.15e-16 | 1.0e-09 | PASS |
|     … same grid, τ_max coefficient k | 0.65165441 | 0.65165441 | 1.02e-15 | 1.0e-09 | PASS |
| rectangle FD a/b = 2, N = 16: conjugate gradients (page) vs sparse direct solve (scipy), c₂ | 0.22704527 | 0.22704527 | 3.42e-15 | 1.0e-09 | PASS |
|     … same grid, τ_max coefficient k | 0.92845572 | 0.92845572 | 2.22e-14 | 1.0e-09 | PASS |
| rectangle FD a/b = 4, N = 8: conjugate gradients (page) vs sparse direct solve (scipy), c₂ | 0.27496347 | 0.27496347 | 1.01e-15 | 1.0e-09 | PASS |
|     … same grid, τ_max coefficient k | 0.99656383 | 0.99656383 | 1.55e-14 | 1.0e-09 | PASS |
| rectangle a/b = 1.0: series c₂ vs Richardson-extrapolated scipy FD (N = 32, 64) | 0.14057701 | 0.14057668 | 2.41e-06 | 2.0e-05 | PASS |
| rectangle a/b = 2.0: series c₂ vs Richardson-extrapolated scipy FD (N = 32, 64) | 0.22868168 | 0.2286815 | 7.55e-07 | 2.0e-05 | PASS |
| rectangle a/b = 3.0: series c₂ vs Richardson-extrapolated scipy FD (N = 32, 64) | 0.26331693 | 0.26331682 | 4.35e-07 | 2.0e-05 | PASS |
| tube t = 1 mm: Bredt stress JavaScript vs Python | 26514776 | 26514776 | 0.00e+00 | 1.0e-13 | PASS |
| tube t = 1 mm: exact stress JavaScript vs Python | 27044630 | 27044630 | 0.00e+00 | 1.0e-13 | PASS |
| tube t = 5 mm: Bredt stress JavaScript vs Python | 6287602.7 | 6287602.7 | 0.00e+00 | 1.0e-13 | PASS |
| tube t = 5 mm: exact stress JavaScript vs Python | 6901027.3 | 6901027.3 | 0.00e+00 | 1.0e-13 | PASS |
| tube t = 15 mm: Bredt stress JavaScript vs Python | 3464597.4 | 3464597.4 | 0.00e+00 | 1.0e-13 | PASS |
| tube t = 15 mm: exact stress JavaScript vs Python | 4181410.7 | 4181410.7 | 0.00e+00 | 1.0e-13 | PASS |
| closure: [steel] G (GPa) recovered within U = 0.933 (value 80.252, truth 80.401) — truth includes the load-cell and troptometer gain errors | True | True | 0.00e+00 | 0.0e+00 | PASS |
| closure: [steel] compliance C_m (°/N·m) recovered within U = 0.00427 (value 0.035831, truth 0.034377) | True | True | 0.00e+00 | 0.0e+00 | PASS |
| closure: [steel] backlash (°) recovered within U = 0.03 (value 0.38807, truth 0.4) — toe not fully seated at 1.5 N·m | True | True | 0.00e+00 | 0.0e+00 | PASS |
| closure: [steel] fracture shear strain γ_f recovered within U = 0.032 (value 1.5977, truth 1.6) | True | True | 0.00e+00 | 0.0e+00 | PASS |
| closure: [al] G (GPa) recovered within U = 0.232 (value 26.032, truth 26.03) — truth includes the load-cell and troptometer gain errors | True | True | 0.00e+00 | 0.0e+00 | PASS |
| closure: [al] compliance C_m (°/N·m) recovered within U = 0.0034 (value 0.036899, truth 0.034377) | True | True | 0.00e+00 | 0.0e+00 | PASS |
| closure: [al] backlash (°) recovered within U = 0.03 (value 0.39245, truth 0.4) — toe not fully seated at 1.5 N·m | True | True | 0.00e+00 | 0.0e+00 | PASS |
| closure: [al] fracture shear strain γ_f recovered within U = 0.016 (value 0.7964, truth 0.8) | True | True | 0.00e+00 | 0.0e+00 | PASS |
| closure: [steel] τ_Y from the EPP fit (MPa) recovered within U = 1.04 (value 172.07, truth 172.01) | True | True | 0.00e+00 | 0.0e+00 | PASS |
| closure: [steel] permanent twist after unloading (°) recovered within U = 0.0523 (value 3.29, truth 3.2852) | True | True | 0.00e+00 | 0.0e+00 | PASS |
| closure: [steel] Nadai τ at γ = 0.1 (MPa) recovered within U = 3.7 (value 246.76, truth 246.69) | True | True | 0.00e+00 | 0.0e+00 | PASS |
| closure: [steel] Nadai τ at γ = 0.5 (MPa) recovered within U = 5.17 (value 344.41, truth 344.39) | True | True | 0.00e+00 | 0.0e+00 | PASS |
| closure: [steel] Nadai τ at γ = 1.0 (MPa) recovered within U = 5.91 (value 394.14, truth 394.14) | True | True | 0.00e+00 | 0.0e+00 | PASS |
| closure: [al] Nadai τ at γ = 0.5 (MPa) recovered within U = 3.18 (value 212.32, truth 212.39) | True | True | 0.00e+00 | 0.0e+00 | PASS |
| closure: [ci] secant G at low torque (GPa) recovered within U = 1.64 (value 40.744, truth 41) — nonlinearity lowers the secant slightly | True | True | 0.00e+00 | 0.0e+00 | PASS |

69 of 69 passed.

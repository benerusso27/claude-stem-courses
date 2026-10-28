## Lab 1 — independent checks (Python/scipy) and data-pipeline closure

| Test | Value | Reference | Rel. difference | Tolerance | Result |
|---|---:|---:|---:|---:|---|
| [steel] sigY: JavaScript closed form vs Python closed form | 2.9601788e+08 | 2.9601788e+08 | 2.01e-16 | 1.0e-12 | PASS |
| [steel] sigU: JavaScript closed form vs Python closed form | 4.5197629e+08 | 4.5197629e+08 | 0.00e+00 | 1.0e-12 | PASS |
| [steel] e_u: JavaScript closed form vs Python closed form | 0.211271 | 0.211271 | 0.00e+00 | 1.0e-12 | PASS |
| [steel] uU: JavaScript closed form vs Python closed form | 88716830 | 88716830 | 0.00e+00 | 1.0e-12 | PASS |
| [steel] σU: page solver (δ = 0) vs scipy bounded maximization | 4.519766e+08 | 4.519766e+08 | 3.39e-10 | 1.0e-06 | PASS |
| [steel] εu: page solver (δ = 0) vs scipy maximization — sample nearest the peak | 0.21062713 | 0.21063773 | 5.03e-05 | 2.0e-03 | PASS |
| [steel] 0.2 % offset on engineering curve: page solver vs scipy brentq | 2.9492899e+08 | 2.9492899e+08 | 9.56e-09 | 5.0e-05 | PASS |
| [steel] energy to peak: page trapezoid vs scipy quad — first-order endpoint, h = 1/8192 | 88425812 | 88430605 | 5.42e-05 | 1.0e-03 | PASS |
| [steel] Considère closed form σU vs scipy exact maximum — rigid-plastic approximation at a stationary point | 4.5197629e+08 | 4.519766e+08 | 6.97e-07 | 1.0e-05 | PASS |
| [al] sigY: JavaScript closed form vs Python closed form | 2.7396373e+08 | 2.7396373e+08 | 0.00e+00 | 1.0e-12 | PASS |
| [al] sigU: JavaScript closed form vs Python closed form | 3.1395759e+08 | 3.1395759e+08 | 0.00e+00 | 1.0e-12 | PASS |
| [al] e_u: JavaScript closed form vs Python closed form | 0.068084017 | 0.068084017 | 0.00e+00 | 1.0e-12 | PASS |
| [al] uU: JavaScript closed form vs Python closed form | 20113816 | 20113816 | 0.00e+00 | 1.0e-12 | PASS |
| [al] σU: page solver (δ = 0) vs scipy bounded maximization | 3.1395782e+08 | 3.1395782e+08 | 2.82e-09 | 1.0e-06 | PASS |
| [al] εu: page solver (δ = 0) vs scipy maximization — sample nearest the peak | 0.067749052 | 0.06776416 | 2.23e-04 | 2.0e-03 | PASS |
| [al] 0.2 % offset on engineering curve: page solver vs scipy brentq | 2.7203772e+08 | 2.7203774e+08 | 8.85e-08 | 5.0e-05 | PASS |
| [al] energy to peak: page trapezoid vs scipy quad — first-order endpoint, h = 1/8192 | 20008646 | 20013394 | 2.37e-04 | 1.0e-03 | PASS |
| [al] Considère closed form σU vs scipy exact maximum — rigid-plastic approximation at a stationary point | 3.1395759e+08 | 3.1395782e+08 | 7.27e-07 | 1.0e-05 | PASS |
| [ss] sigY: JavaScript closed form vs Python closed form | 2.4997939e+08 | 2.4997939e+08 | 0.00e+00 | 1.0e-12 | PASS |
| [ss] sigU: JavaScript closed form vs Python closed form | 6.0001381e+08 | 6.0001381e+08 | 0.00e+00 | 1.0e-12 | PASS |
| [ss] e_u: JavaScript closed form vs Python closed form | 0.49874282 | 0.49874282 | 0.00e+00 | 1.0e-12 | PASS |
| [ss] uU: JavaScript closed form vs Python closed form | 2.639753e+08 | 2.639753e+08 | 0.00e+00 | 1.0e-12 | PASS |
| [ss] σU: page solver (δ = 0) vs scipy bounded maximization | 6.0001652e+08 | 6.0001652e+08 | 3.18e-11 | 1.0e-06 | PASS |
| [ss] εu: page solver (δ = 0) vs scipy maximization — sample nearest the peak | 0.49581708 | 0.49582293 | 1.18e-05 | 2.0e-03 | PASS |
| [ss] 0.2 % offset on engineering curve: page solver vs scipy brentq | 2.4910782e+08 | 2.4910782e+08 | 1.18e-08 | 5.0e-05 | PASS |
| [ss] energy to peak: page trapezoid vs scipy quad — first-order endpoint, h = 1/8192 | 2.622198e+08 | 2.6222332e+08 | 1.34e-05 | 1.0e-03 | PASS |
| [ss] Considère closed form σU vs scipy exact maximum — rigid-plastic approximation at a stationary point | 6.0001381e+08 | 6.0001652e+08 | 4.53e-06 | 1.0e-05 | PASS |
| [steel_1018HR] closure: E (GPa) recovered within its expanded uncertainty U = 3.02 — plus 0.3 % finite-strain/neck-zone shift of the truth model | 205.21883 | 205 | 1.07e-03 | 1.5e-02 | PASS |
| [steel_1018HR] closure: σU (MPa) recovered within its expanded uncertainty U = 3.36 | 451.87933 | 451.87773 | 3.55e-06 | 7.4e-03 | PASS |
| [steel_1018HR] closure: machine compliance (mm/kN) recovered within its expanded uncertainty U = 5.46e-05 | 0.0080005466 | 0.008 | 6.83e-05 | 6.8e-03 | PASS |
| [steel_1018HR] closure: grip seating toe (mm) recovered within its expanded uncertainty U = 0.00143 | 0.050075484 | 0.05 | 1.51e-03 | 2.9e-02 | PASS |
| [steel_1018HR] closure: uniform elongation εu recovered within its expanded uncertainty U = 0.0142 | 0.19004095 | 0.1897962 | 1.29e-03 | 7.5e-02 | PASS |
| [steel_1018HR] closure: elongation after fracture (%) recovered within its expanded uncertainty U = 0.209 — mark-measurement scatter 0.04 mm | 33.873225 | 33.942609 | 2.04e-03 | 6.2e-03 | PASS |
| [steel_1018HR] closure: true stress in neck at fracture (MPa) recovered within its expanded uncertainty U = 11.7 | 743.65967 | 743.9228 | 3.54e-04 | 1.6e-02 | PASS |
| [steel_1018HR] closure: upper yield point (MPa) recovered within its expanded uncertainty U = 4.39 — serration/noise on the peak sample | 321.50244 | 322 | 1.55e-03 | 1.4e-02 | PASS |
| [steel_1018HR] closure: lower yield point (MPa) recovered within its expanded uncertainty U = 2.21 — plateau set by the weakest section | 296.1963 | 296.109 | 2.95e-04 | 7.5e-03 | PASS |
| [al_6061T6] closure: E (GPa) recovered within its expanded uncertainty U = 0.97 — plus 0.3 % finite-strain/neck-zone shift of the truth model | 68.751255 | 68.9 | 2.16e-03 | 1.4e-02 | PASS |
| [al_6061T6] closure: σU (MPa) recovered within its expanded uncertainty U = 2.34 | 314.25395 | 314.25528 | 4.21e-06 | 7.4e-03 | PASS |
| [al_6061T6] closure: machine compliance (mm/kN) recovered within its expanded uncertainty U = 5.26e-05 | 0.0080025123 | 0.008 | 3.14e-04 | 6.6e-03 | PASS |
| [al_6061T6] closure: grip seating toe (mm) recovered within its expanded uncertainty U = 0.00141 | 0.049992725 | 0.05 | 1.46e-04 | 2.8e-02 | PASS |
| [al_6061T6] closure: uniform elongation εu recovered within its expanded uncertainty U = 0.00594 | 0.048643622 | 0.049980092 | 2.67e-02 | 1.2e-01 | PASS |
| [al_6061T6] closure: elongation after fracture (%) recovered within its expanded uncertainty U = 0.198 — mark-measurement scatter 0.04 mm | 12.382476 | 12.396303 | 1.12e-03 | 1.6e-02 | PASS |
| [al_6061T6] closure: true stress in neck at fracture (MPa) recovered within its expanded uncertainty U = 5.14 | 382.30632 | 380.93715 | 3.59e-03 | 1.3e-02 | PASS |

43 of 43 passed.

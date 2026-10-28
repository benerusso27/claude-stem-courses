## Lab 1 — simulation model (Node, exact page code)

| Test | Value | Reference | Rel. difference | Tolerance | Result |
|---|---:|---:|---:|---:|---|
| [steel] σU: Considère closed form vs golden-section max of P(εp) — stationary point, so the rigid-plastic approximation costs only second order | 4.5197629e+8 | 4.5197660e+8 | 6.97e-7 | 1.0e-5 | PASS |
| [steel] εu: Considère closed form − nσt,U/E correction vs golden-section max — uncorrected closed form differs by 0.30 % | 0.21063909 | 0.21063774 | 6.43e-6 | 5.0e-4 | PASS |
| [steel] uU: closed form vs adaptive Simpson ∫σt dεt | 88716830 | 88716830 | 8.40e-16 | 1.0e-9 | PASS |
| [steel] ∫σ dε (engineering) = ∫σt dεt (true) before necking | 88716829 | 88716830 | 3.76e-9 | 1.0e-7 | PASS |
| [steel] σU: marching solver (δ = 0, M = 8192) vs golden-section max | 4.5197660e+8 | 4.5197660e+8 | 3.39e-10 | 1.0e-6 | PASS |
| [steel] εu: marching solver (δ = 0) vs golden-section max — sample nearest the peak | 0.21062713 | 0.21063774 | 5.04e-5 | 2.0e-3 | PASS |
| [steel] u to peak: trapezoid on solver path (δ = 0) vs closed-form integral at the exact peak — first-order endpoint error, h = 1/8192 | 88425812 | 88430609 | 5.42e-5 | 1.0e-3 | PASS |
| [steel] uU: Considère closed form vs energy to the exact peak — closed form stops at the rigid-plastic necking strain | 88716830 | 88430609 | 3.24e-3 | 1.0e-2 | PASS |
| [steel] σU with δ: solver vs (1 − δ)·exact uniform-bar maximum | 4.5062067e+8 | 4.5062067e+8 | 3.39e-10 | 1.0e-6 | PASS |
| [steel] σY: solver vs K(ε0+0.002)^n·(1 − εY) — small-strain closed form plus first-order finite-strain correction | 2.9492899e+8 | 2.9499839e+8 | 2.35e-4 | 1.5e-3 | PASS |
| [steel] E: gage regression vs E(1 − 3σm/E)(1 − δℓ/L0) — raw difference from E is -0.19 % | 2.0461160e+11 | 2.0461030e+11 | 6.33e-6 | 4.0e-4 | PASS |
| [steel] E_app: crosshead regression vs springs in series 1/(1/E + A0·Cm/Lc) | 6.5108451e+10 | 6.5108318e+10 | 2.05e-6 | 4.0e-4 | PASS |
| [steel] E_app: textbook form with E vs crosshead regression — same finite-strain shift as E | 6.5108451e+10 | 6.5146477e+10 | 5.84e-4 | 3.0e-3 | PASS |
| [steel] Δεt,u for δ = 0.0001: √(2nδ) estimate vs solver — asymptotic; error shrinks as δ → 0 | 0.0055012319 | 0.0054366549 | 1.19e-2 | 6.0e-2 | PASS |
| [steel] Δεt,u for δ = 0.001: √(2nδ) estimate vs solver — asymptotic; error shrinks as δ → 0 | 0.017396423 | 0.016808474 | 3.50e-2 | 1.2e-1 | PASS |
| [steel] equilibrium: σ·A = P on every section (max rel. error) | 1.0000000 | 1.0000000 | 9.55e-15 | 1.0e-10 | PASS |
| [steel] volume constancy of the neck zone (max rel. error) | 1.0000000 | 1.0000000 | 6.66e-16 | 1.0e-10 | PASS |
| [steel] compatibility: crosshead = gage + rest of reduced section + Cm·P | 1.0000000 | 1.0000000 | 0.00e+0 | 1.0e-12 | PASS |
| [steel] convergence order of σY ≈ 2 (observed 1.99) | true | true | 0.00e+0 | 0.0e+0 | PASS |
| [steel] convergence order of u(ε*) ≈ 2 (observed 2.00) | true | true | 0.00e+0 | 0.0e+0 | PASS |
| [steel] convergence: σU error at M = 610 below 1e-5 | true | true | 0.00e+0 | 0.0e+0 | PASS |
| [steel] mesh-set neck: elongation after fracture falls monotonically with N | true | true | 0.00e+0 | 0.0e+0 | PASS |
| [steel] mesh-set neck, N = 200: EL → uniform elongation of the rest of the gage — one element of length L0/200 holds the neck | 0.17578180 | 0.17674540 | 5.45e-3 | 1.2e-1 | PASS |
| [al] σU: Considère closed form vs golden-section max of P(εp) — stationary point, so the rigid-plastic approximation costs only second order | 3.1395759e+8 | 3.1395782e+8 | 7.27e-7 | 1.0e-5 | PASS |
| [al] εu: Considère closed form − nσt,U/E correction vs golden-section max — uncorrected closed form differs by 0.47 % | 0.067765616 | 0.067764162 | 2.15e-5 | 5.0e-4 | PASS |
| [al] uU: closed form vs adaptive Simpson ∫σt dεt | 20113816 | 20113816 | 1.46e-14 | 1.0e-9 | PASS |
| [al] ∫σ dε (engineering) = ∫σt dεt (true) before necking | 20113814 | 20113816 | 9.04e-8 | 1.0e-7 | PASS |
| [al] σU: marching solver (δ = 0, M = 8192) vs golden-section max | 3.1395782e+8 | 3.1395782e+8 | 2.82e-9 | 1.0e-6 | PASS |
| [al] εu: marching solver (δ = 0) vs golden-section max — sample nearest the peak | 0.067749052 | 0.067764162 | 2.23e-4 | 2.0e-3 | PASS |
| [al] u to peak: trapezoid on solver path (δ = 0) vs closed-form integral at the exact peak — first-order endpoint error, h = 1/8192 | 20008646 | 20013395 | 2.37e-4 | 1.0e-3 | PASS |
| [al] uU: Considère closed form vs energy to the exact peak — closed form stops at the rigid-plastic necking strain | 20113816 | 20013395 | 5.02e-3 | 1.0e-2 | PASS |
| [al] σU with δ: solver vs (1 − δ)·exact uniform-bar maximum | 3.1301594e+8 | 3.1301594e+8 | 2.82e-9 | 1.0e-6 | PASS |
| [al] σY: solver vs K(ε0+0.002)^n·(1 − εY) — small-strain closed form plus first-order finite-strain correction | 2.7203772e+8 | 2.7232646e+8 | 1.06e-3 | 1.5e-3 | PASS |
| [al] E: gage regression vs E(1 − 3σm/E)(1 − δℓ/L0) — raw difference from E is -0.43 % | 6.8606887e+10 | 6.8605219e+10 | 2.43e-5 | 4.0e-4 | PASS |
| [al] E_app: crosshead regression vs springs in series 1/(1/E + A0·Cm/Lc) | 3.9925118e+10 | 3.9924545e+10 | 1.44e-5 | 4.0e-4 | PASS |
| [al] E_app: textbook form with E vs crosshead regression — same finite-strain shift as E | 3.9925118e+10 | 4.0022791e+10 | 2.44e-3 | 3.0e-3 | PASS |
| [al] Δεt,u for δ = 0.0001: √(2nδ) estimate vs solver — asymptotic; error shrinks as δ → 0 | 0.0030802514 | 0.0030121543 | 2.26e-2 | 6.0e-2 | PASS |
| [al] Δεt,u for δ = 0.001: √(2nδ) estimate vs solver — asymptotic; error shrinks as δ → 0 | 0.0097406102 | 0.0091666242 | 6.26e-2 | 1.2e-1 | PASS |
| [al] equilibrium: σ·A = P on every section (max rel. error) | 1.0000000 | 1.0000000 | 9.75e-14 | 1.0e-10 | PASS |
| [al] volume constancy of the neck zone (max rel. error) | 1.0000000 | 1.0000000 | 6.66e-16 | 1.0e-10 | PASS |
| [al] compatibility: crosshead = gage + rest of reduced section + Cm·P | 1.0000000 | 1.0000000 | 0.00e+0 | 1.0e-12 | PASS |
| [al] convergence order of σY ≈ 2 (observed 2.22) | true | true | 0.00e+0 | 0.0e+0 | PASS |
| [al] convergence order of u(ε*) ≈ 2 (observed 1.99) | true | true | 0.00e+0 | 0.0e+0 | PASS |
| [al] convergence: σU error at M = 610 below 1e-5 | true | true | 0.00e+0 | 0.0e+0 | PASS |
| [al] mesh-set neck: elongation after fracture falls monotonically with N | true | true | 0.00e+0 | 0.0e+0 | PASS |
| [al] mesh-set neck, N = 200: EL → uniform elongation of the rest of the gage — one element of length L0/200 holds the neck | 0.047820242 | 0.051663303 | 7.44e-2 | 1.2e-1 | PASS |
| [ss] σU: Considère closed form vs golden-section max of P(εp) — stationary point, so the rigid-plastic approximation costs only second order | 6.0001381e+8 | 6.0001652e+8 | 4.53e-6 | 1.0e-5 | PASS |
| [ss] εu: Considère closed form − nσt,U/E correction vs golden-section max — uncorrected closed form differs by 0.59 % | 0.49583084 | 0.49582296 | 1.59e-5 | 5.0e-4 | PASS |
| [ss] uU: closed form vs adaptive Simpson ∫σt dεt | 2.6397530e+8 | 2.6397530e+8 | 4.52e-16 | 1.0e-9 | PASS |
| [ss] ∫σ dε (engineering) = ∫σt dεt (true) before necking | 2.6397530e+8 | 2.6397530e+8 | 1.09e-9 | 1.0e-7 | PASS |
| [ss] σU: marching solver (δ = 0, M = 8192) vs golden-section max | 6.0001652e+8 | 6.0001652e+8 | 3.18e-11 | 1.0e-6 | PASS |
| [ss] εu: marching solver (δ = 0) vs golden-section max — sample nearest the peak | 0.49581708 | 0.49582296 | 1.19e-5 | 2.0e-3 | PASS |
| [ss] u to peak: trapezoid on solver path (δ = 0) vs closed-form integral at the exact peak — first-order endpoint error, h = 1/8192 | 2.6221980e+8 | 2.6222334e+8 | 1.35e-5 | 1.0e-3 | PASS |
| [ss] uU: Considère closed form vs energy to the exact peak — closed form stops at the rigid-plastic necking strain | 2.6397530e+8 | 2.6222334e+8 | 6.68e-3 | 1.0e-2 | PASS |
| [ss] σU with δ: solver vs (1 − δ)·exact uniform-bar maximum | 5.9821647e+8 | 5.9821647e+8 | 3.18e-11 | 1.0e-6 | PASS |
| [ss] σY: solver vs K(ε0+0.002)^n·(1 − εY) — small-strain closed form plus first-order finite-strain correction | 2.4910782e+8 | 2.4915565e+8 | 1.92e-4 | 1.5e-3 | PASS |
| [ss] E: gage regression vs E(1 − 3σm/E)(1 − δℓ/L0) — raw difference from E is -0.17 % | 1.9266272e+11 | 1.9266165e+11 | 5.55e-6 | 4.0e-4 | PASS |
| [ss] E_app: crosshead regression vs springs in series 1/(1/E + A0·Cm/Lc) | 6.3848478e+10 | 6.3848359e+10 | 1.87e-6 | 4.0e-4 | PASS |
| [ss] E_app: textbook form with E vs crosshead regression — same finite-strain shift as E | 6.3848478e+10 | 6.3884200e+10 | 5.59e-4 | 3.0e-3 | PASS |
| [ss] Δεt,u for δ = 0.0001: √(2nδ) estimate vs solver — asymptotic; error shrinks as δ → 0 | 0.0080403303 | 0.0079840169 | 7.05e-3 | 6.0e-2 | PASS |
| [ss] Δεt,u for δ = 0.001: √(2nδ) estimate vs solver — asymptotic; error shrinks as δ → 0 | 0.025425757 | 0.024836483 | 2.37e-2 | 1.2e-1 | PASS |
| [ss] equilibrium: σ·A = P on every section (max rel. error) | 1.0000000 | 1.0000000 | 7.99e-15 | 1.0e-10 | PASS |
| [ss] volume constancy of the neck zone (max rel. error) | 1.0000000 | 1.0000000 | 6.66e-16 | 1.0e-10 | PASS |
| [ss] compatibility: crosshead = gage + rest of reduced section + Cm·P | 1.0000000 | 1.0000000 | 2.22e-16 | 1.0e-12 | PASS |
| [ss] convergence order of σY ≈ 2 (observed 2.13) | true | true | 0.00e+0 | 0.0e+0 | PASS |
| [ss] convergence order of u(ε*) ≈ 2 (observed 2.00) | true | true | 0.00e+0 | 0.0e+0 | PASS |
| [ss] convergence: σU error at M = 610 below 1e-5 | true | true | 0.00e+0 | 0.0e+0 | PASS |
| [ss] mesh-set neck: elongation after fracture falls monotonically with N | true | true | 0.00e+0 | 0.0e+0 | PASS |
| [ss] mesh-set neck, N = 200: EL → uniform elongation of the rest of the gage — one element of length L0/200 holds the neck | 0.42867814 | 0.43392136 | 1.21e-2 | 1.2e-1 | PASS |
| hand example: σ = P/A0 for P = 20 kN, d0 = 10 mm (254.648 MPa) | 254.64791 | 254.64790 | 3.51e-8 | 1.0e-6 | PASS |
| hand example: σt = σ(1+ε) for σ = 400 MPa, ε = 0.15 | 460.00000 | 460.00000 | 1.24e-16 | 1.0e-12 | PASS |
| hand example: εt = ln(1+ε) for ε = 0.15 | 0.13976194 | 0.13976194 | 1.78e-10 | 1.0e-9 | PASS |
| units: 1 ksi = 6.894757 MPa | 6.8947573 | 6.8947573 | 2.44e-11 | 1.0e-9 | PASS |
| units: 29 000 ksi = 199.948 GPa | 199.94796 | 199.94796 | 9.36e-12 | 1.0e-9 | PASS |
| units: 1 in/kip = 0.2248089 mm/kN | 5.7101472 | 5.7101472 | 0.00e+0 | 1.0e-12 | PASS |
| units: 1 in·lb/in³ = 6.894757e-3 MJ/m³ | 0.0068947573 | 0.0068947573 | 2.44e-11 | 1.0e-9 | PASS |
| units: round trip of 452 MPa through ksi | 4.5200000e+8 | 4.5200000e+8 | 0.00e+0 | 1.0e-14 | PASS |

77 of 77 passed.

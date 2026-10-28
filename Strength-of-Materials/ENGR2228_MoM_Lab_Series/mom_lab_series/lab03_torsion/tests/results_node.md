## Lab 3 — simulation model (Node, exact page code)

| Test | Value | Reference | Rel. difference | Tolerance | Result |
|---|---:|---:|---:|---:|---|
| plateau law continuous at the end of the plateau (γ_L ± 1e−9) | 1.7000000e+8 | 1.7000000e+8 | 1.59e-8 | 1.0e-6 | PASS |
| plateau law: τ = τ_Y on the plateau | 1.7000000e+8 | 1.7000000e+8 | 0.00e+0 | 1.0e-14 | PASS |
| Ramberg–Osgood inverse: γ(τ(γ)) = γ at γ = 0.0001 | 0.00010000000 | 0.00010000000 | 0.00e+0 | 1.0e-12 | PASS |
| Ramberg–Osgood inverse: γ(τ(γ)) = γ at γ = 0.003 | 0.0030000000 | 0.0030000000 | 2.89e-16 | 1.0e-12 | PASS |
| Ramberg–Osgood inverse: γ(τ(γ)) = γ at γ = 0.05 | 0.050000000 | 0.050000000 | 1.11e-15 | 1.0e-12 | PASS |
| Ramberg–Osgood inverse: γ(τ(γ)) = γ at γ = 0.5 | 0.50000000 | 0.50000000 | 6.66e-16 | 1.0e-12 | PASS |
| odd symmetry τ(−γ) = −τ(γ) | -2.8503864e+8 | -2.8503864e+8 | 0.00e+0 | 1.0e-15 | PASS |
| [solid] EPP torque at θ = 0.5θ_Y: closed form vs rings (N = 4096) | 4.2733649 | 4.2733650 | 2.98e-8 | 2.0e-7 | PASS |
| [solid] EPP torque at θ = 0.5θ_Y: closed form vs Simpson quadrature | 4.2733650 | 4.2733650 | 8.31e-16 | 1.0e-10 | PASS |
| [solid] EPP torque at θ = 1θ_Y: closed form vs rings (N = 4096) | 8.5467298 | 8.5467301 | 2.98e-8 | 2.0e-7 | PASS |
| [solid] EPP torque at θ = 1θ_Y: closed form vs Simpson quadrature | 8.5467301 | 8.5467301 | 8.31e-16 | 1.0e-10 | PASS |
| [solid] EPP torque at θ = 1.5θ_Y: closed form vs rings (N = 4096) | 10.551518 | 10.551519 | 1.43e-8 | 2.0e-7 | PASS |
| [solid] EPP torque at θ = 1.5θ_Y: closed form vs Simpson quadrature | 10.551519 | 10.551519 | 1.68e-16 | 1.0e-10 | PASS |
| [solid] EPP torque at θ = 3θ_Y: closed form vs rings (N = 4096) | 11.290125 | 11.290125 | 1.42e-8 | 2.0e-7 | PASS |
| [solid] EPP torque at θ = 3θ_Y: closed form vs Simpson quadrature | 11.290125 | 11.290125 | 1.26e-15 | 1.0e-10 | PASS |
| [solid] EPP torque at θ = 10θ_Y: closed form vs rings (N = 4096) | 11.392791 | 11.392791 | 1.42e-8 | 2.0e-7 | PASS |
| [solid] EPP torque at θ = 10θ_Y: closed form vs Simpson quadrature | 11.392791 | 11.392791 | 6.24e-16 | 1.0e-10 | PASS |
| [solid] EPP torque at θ = 100θ_Y: closed form vs rings (N = 4096) | 11.395637 | 11.395637 | 1.50e-8 | 2.0e-7 | PASS |
| [solid] EPP torque at θ = 100θ_Y: closed form vs Simpson quadrature | 11.395637 | 11.395637 | 1.56e-15 | 1.0e-10 | PASS |
| [hollow d_i/d = 0.6] EPP torque at θ = 0.5θ_Y: closed form vs rings (N = 4096) | 3.7195369 | 3.7195369 | 3.51e-9 | 2.0e-7 | PASS |
| [hollow d_i/d = 0.6] EPP torque at θ = 0.5θ_Y: closed form vs Simpson quadrature | 3.7195369 | 3.7195369 | 1.91e-15 | 1.0e-10 | PASS |
| [hollow d_i/d = 0.6] EPP torque at θ = 1θ_Y: closed form vs rings (N = 4096) | 7.4390738 | 7.4390738 | 3.51e-9 | 2.0e-7 | PASS |
| [hollow d_i/d = 0.6] EPP torque at θ = 1θ_Y: closed form vs Simpson quadrature | 7.4390738 | 7.4390738 | 1.91e-15 | 1.0e-10 | PASS |
| [hollow d_i/d = 0.6] EPP torque at θ = 1.5θ_Y: closed form vs rings (N = 4096) | 8.8900343 | 8.8900343 | 2.41e-10 | 2.0e-7 | PASS |
| [hollow d_i/d = 0.6] EPP torque at θ = 1.5θ_Y: closed form vs Simpson quadrature | 8.8900343 | 8.8900343 | 0.00e+0 | 1.0e-10 | PASS |
| [hollow d_i/d = 0.6] EPP torque at θ = 3θ_Y: closed form vs rings (N = 4096) | 8.9341818 | 8.9341818 | 1.22e-9 | 2.0e-7 | PASS |
| [hollow d_i/d = 0.6] EPP torque at θ = 3θ_Y: closed form vs Simpson quadrature | 8.9341818 | 8.9341818 | 1.19e-15 | 1.0e-10 | PASS |
| [hollow d_i/d = 0.6] EPP torque at θ = 10θ_Y: closed form vs rings (N = 4096) | 8.9341818 | 8.9341818 | 1.22e-9 | 2.0e-7 | PASS |
| [hollow d_i/d = 0.6] EPP torque at θ = 10θ_Y: closed form vs Simpson quadrature | 8.9341818 | 8.9341818 | 1.19e-15 | 1.0e-10 | PASS |
| [hollow d_i/d = 0.6] EPP torque at θ = 100θ_Y: closed form vs rings (N = 4096) | 8.9341818 | 8.9341818 | 1.22e-9 | 2.0e-7 | PASS |
| [hollow d_i/d = 0.6] EPP torque at θ = 100θ_Y: closed form vs Simpson quadrature | 8.9341818 | 8.9341818 | 1.19e-15 | 1.0e-10 | PASS |
| Beer §3.7 form (4/3)T_Y[1 − ¼(ρ_Y/c)³] at φ = 1.5φ_Y | 10.551519 | 10.551519 | 0.00e+0 | 1.0e-14 | PASS |
| Beer §3.7 form (4/3)T_Y[1 − ¼(ρ_Y/c)³] at φ = 3φ_Y | 11.290125 | 11.290125 | 1.57e-16 | 1.0e-14 | PASS |
| Beer §3.7 form (4/3)T_Y[1 − ¼(ρ_Y/c)³] at φ = 10φ_Y | 11.392791 | 11.392791 | 0.00e+0 | 1.0e-14 | PASS |
| fully plastic limit T → (4/3)T_Y (solid) | 1.3333333 | 1.3333333 | 0.00e+0 | 1.0e-12 | PASS |
| elastic: T = JGφ/L (closed form) vs rings N = 4096 | 4.2733649 | 4.2733650 | 2.98e-8 | 1.0e-7 | PASS |
| ring integration converges at second order (observed 2.018) | true | true | 0.00e+0 | 0.0e+0 | PASS |
| inverse: twist for T = 1.05T_Y, closed form vs bisection on rings (N = 2048) | 0.71099271 | 0.71099261 | 1.38e-7 | 1.0e-6 | PASS |
| inverse: twist for T = 1.2T_Y, closed form vs bisection on rings (N = 2048) | 0.91408136 | 0.91408111 | 2.71e-7 | 1.0e-6 | PASS |
| inverse: twist for T = 1.3T_Y, closed form vs bisection on rings (N = 2048) | 1.4510142 | 1.4510133 | 6.19e-7 | 1.0e-6 | PASS |
| residual stresses carry zero net torque (rings, relative to T) (absolute difference) | 1.5598837e-8 | 0.0000000 | 1.56e-8 | 1.0e-6 | PASS |
| permanent twist ratio φ_p/φ_Y after unloading from 3φ_Y (EPP: 3 − 1.3210) | 1.6790123 | 1.6790123 | 3.97e-16 | 1.0e-12 | PASS |
| surface residual stress τ_Y − T c/J (closed form) vs rings | -54567901 | -54567898 | 5.85e-8 | 1.0e-6 | PASS |
| [1018 steel (plateau + hardening)] torque at θ = 0.5θ_Y: rings (N = 4096) vs Simpson | 4.2733649 | 4.2733650 | 2.98e-8 | 3.0e-7 | PASS |
| [1018 steel (plateau + hardening)] torque at θ = 2θ_Y: rings (N = 4096) vs Simpson | 11.039526 | 11.039526 | 1.92e-8 | 3.0e-7 | PASS |
| [1018 steel (plateau + hardening)] torque at θ = 20θ_Y: rings (N = 4096) vs Simpson | 12.062763 | 12.062763 | 1.81e-8 | 3.0e-7 | PASS |
| [1018 steel (plateau + hardening)] torque at θ = 500θ_Y: rings (N = 4096) vs Simpson | 25.036919 | 25.036920 | 1.74e-8 | 3.0e-7 | PASS |
| [6061-T6 (Ramberg–Osgood)] torque at θ = 0.5θ_Y: rings (N = 4096) vs Simpson | 3.9717087 | 3.9717088 | 2.98e-8 | 3.0e-7 | PASS |
| [6061-T6 (Ramberg–Osgood)] torque at θ = 2θ_Y: rings (N = 4096) vs Simpson | 10.207130 | 10.207130 | 1.69e-8 | 3.0e-7 | PASS |
| [6061-T6 (Ramberg–Osgood)] torque at θ = 20θ_Y: rings (N = 4096) vs Simpson | 12.735941 | 12.735941 | 1.57e-8 | 3.0e-7 | PASS |
| [6061-T6 (Ramberg–Osgood)] torque at θ = 150θ_Y: rings (N = 4096) vs Simpson | 14.406675 | 14.406676 | 1.56e-8 | 3.0e-7 | PASS |
| [cast iron (tanh)] torque at θ = 0.5θ_Y: rings (N = 4096) vs Simpson | 5.3129508 | 5.3129510 | 2.93e-8 | 3.0e-7 | PASS |
| [cast iron (tanh)] torque at θ = 1θ_Y: rings (N = 4096) vs Simpson | 10.252315 | 10.252315 | 2.78e-8 | 3.0e-7 | PASS |
| [cast iron (tanh)] torque at θ = 1.4θ_Y: rings (N = 4096) vs Simpson | 13.751331 | 13.751332 | 2.62e-8 | 3.0e-7 | PASS |
| hand value (3 s.f.): c₁ for a/b = 1 | 0.20816526 | 0.20800000 | 7.95e-4 | 2.5e-3 | PASS |
| hand value (3–4 s.f.): c₂ for a/b = 1 | 0.14057701 | 0.14060000 | 1.63e-4 | 2.5e-3 | PASS |
| hand value (3 s.f.): c₁ for a/b = 2 | 0.24587834 | 0.24600000 | 4.95e-4 | 2.5e-3 | PASS |
| hand value (3–4 s.f.): c₂ for a/b = 2 | 0.22868168 | 0.22900000 | 1.39e-3 | 2.5e-3 | PASS |
| hand value (3 s.f.): c₁ for a/b = 10 | 0.31232511 | 0.31200000 | 1.04e-3 | 2.5e-3 | PASS |
| hand value (3–4 s.f.): c₂ for a/b = 10 | 0.31232504 | 0.31200000 | 1.04e-3 | 2.5e-3 | PASS |
| thin strip: c₂ → (1/3)[1 − (192/π⁵)(31/32)ζ(5) b/a] for a/b = 1000 | 0.33312325 | 0.33312325 | 0.00e+0 | 1.0e-9 | PASS |
| [a/b = 1] c₂: Richardson-extrapolated finite differences (N = 16, 32) vs series | 0.14057243 | 0.14057701 | 3.26e-5 | 5.0e-5 | PASS |
| [a/b = 1] τ_max/(Gθb): Richardson-extrapolated finite differences vs series | 0.67530644 | 0.67531448 | 1.19e-5 | 2.0e-4 | PASS |
| [a/b = 2] c₂: Richardson-extrapolated finite differences (N = 16, 32) vs series | 0.22867934 | 0.22868168 | 1.02e-5 | 5.0e-5 | PASS |
| [a/b = 2] τ_max/(Gθb): Richardson-extrapolated finite differences vs series | 0.93005955 | 0.93006027 | 7.72e-7 | 2.0e-4 | PASS |
| [a/b = 5] c₂: Richardson-extrapolated finite differences (N = 16, 32) vs series | 0.29131582 | 0.29131675 | 3.20e-6 | 5.0e-5 | PASS |
| [a/b = 5] τ_max/(Gθb): Richardson-extrapolated finite differences vs series | 0.99937072 | 0.99937067 | 5.36e-8 | 2.0e-4 | PASS |
| finite differences converge at second order for c₂ (observed 1.970) | true | true | 0.00e+0 | 0.0e+0 | PASS |
| shear along the centre line at y = 0.1b: series vs finite differences (N = 32) | 0.74551556 | 0.74557657 | 8.18e-5 | 3.0e-3 | PASS |
| shear along the centre line at y = 0.25b: series vs finite differences (N = 32) | 0.45052158 | 0.45056571 | 9.80e-5 | 3.0e-3 | PASS |
| shear along the centre line at y = 0.4b: series vs finite differences (N = 32) | 0.16719528 | 0.16721302 | 1.06e-4 | 3.0e-3 | PASS |
| Bredt → exact as t/r_m → 0 (stress, t/r_m = 0.002) | 5.1031594e+8 | 5.1082625e+8 | 9.99e-4 | 1.5e-3 | PASS |
| Bredt → exact as t/r_m → 0 (twist) | 0.25541338 | 0.25541313 | 1.00e-6 | 1.0e-5 | PASS |
| tube: torque from ring integration of Tρ/J equals T | 100.00000 | 100.00000 | 7.27e-10 | 1.0e-7 | PASS |
| preset steel specimen d = 6.35 mm: T_Y = τ_Y πc³/2 (hand: 8.547 N·m) | 8.5467301 | 8.5470000 | 3.16e-5 | 1.0e-4 | PASS |
| preset steel specimen: φ_Y over 50.8 mm (hand: 1.960°) | 1.9603084 | 1.9600000 | 1.57e-4 | 2.0e-4 | PASS |
| units: 1 N·m = 8.8507 lb·in | 8.8507458 | 8.8507460 | 2.36e-8 | 1.0e-6 | PASS |
| units: angle in degrees in both systems | 180.00000 | 180.00000 | 0.00e+0 | 1.0e-14 | PASS |
| units: 1 in⁴ = 416 231 mm⁴ | 416231.43 | 416231.43 | 1.40e-16 | 1.0e-9 | PASS |

79 of 79 passed.

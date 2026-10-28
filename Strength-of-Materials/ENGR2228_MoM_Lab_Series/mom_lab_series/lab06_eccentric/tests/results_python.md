## Lab 6 — independent checks (Python/scipy) and data-pipeline closure

| Test | Value | Reference | Rel. difference | Tolerance | Result |
|---|---:|---:|---:|---:|---|
| rect [partA2]: A, JavaScript part formulas vs Python Green's theorem / quadrature | 0.00064516 | 0.00064516 | 0.00e+00 | 1.0e-11 | PASS |
| rect [partA2]: centroid y (mm) (absolute) | 0 | 0 | 0.00e+00 | 1.0e-09 | PASS |
| rect [partA2]: centroid z (mm) (absolute) | 0 | 0 | 0.00e+00 | 1.0e-09 | PASS |
| rect [partA2]: I_z | 1.3874381e-07 | 1.3874381e-07 | 0.00e+00 | 1.0e-10 | PASS |
| rect [partA2]: I_y | 8.671488e-09 | 8.671488e-09 | 1.91e-16 | 1.0e-10 | PASS |
| rect [partA2]: I_yz / I_max (absolute) | 0 | -5.2516148e-18 | 5.25e-18 | 1.0e-10 | PASS |
| rect [partA2]: I_max, Mohr formula (JS) vs eigenvalue (numpy) | 1.3874381e-07 | 1.3874381e-07 | 0.00e+00 | 1.0e-10 | PASS |
| rect [partA2]: I_min, Mohr formula (JS) vs eigenvalue (numpy) | 8.671488e-09 | 8.671488e-09 | 1.34e-15 | 1.0e-10 | PASS |
| rect [partA2]: corner stresses, Eq. 4.58 in principal axes (JS) vs general S⁻¹ form (Python), max \|Δ\|/σ_max (absolute) | 0 | 0 | 0.00e+00 | 1.0e-10 | PASS |
| rect [partA2]: kern area, antipoles (JS) vs half-plane intersection (scipy) | 3.5842222e-05 | 3.5842222e-05 | 1.51e-15 | 1.0e-09 | PASS |
| rect [partA2]: every kern vertex found by both methods (largest distance, mm) (absolute) | 3.0357661e-15 | 0 | 3.04e-15 | 1.0e-09 | PASS |
| angle [partB]: A, JavaScript part formulas vs Python Green's theorem / quadrature | 0.0006048375 | 0.0006048375 | 0.00e+00 | 1.0e-11 | PASS |
| angle [partB]: centroid y (mm) (absolute) | 15.028333 | 15.028333 | 1.78e-15 | 1.0e-09 | PASS |
| angle [partB]: centroid z (mm) (absolute) | -15.028333 | -15.028333 | 0.00e+00 | 1.0e-09 | PASS |
| angle [partB]: I_z | 1.4467836e-07 | 1.4467836e-07 | 1.83e-16 | 1.0e-10 | PASS |
| angle [partB]: I_y | 1.4467836e-07 | 1.4467836e-07 | 0.00e+00 | 1.0e-10 | PASS |
| angle [partB]: I_yz / I_max (absolute) | 0.3700295 | 0.3700295 | 5.55e-17 | 1.0e-10 | PASS |
| angle [partB]: I_max, Mohr formula (JS) vs eigenvalue (numpy) | 2.2965894e-07 | 2.2965894e-07 | 0.00e+00 | 1.0e-10 | PASS |
| angle [partB]: I_min, Mohr formula (JS) vs eigenvalue (numpy) | 5.9697775e-08 | 5.9697775e-08 | 0.00e+00 | 1.0e-10 | PASS |
| angle [partB]: corner stresses, Eq. 4.58 in principal axes (JS) vs general S⁻¹ form (Python), max \|Δ\|/σ_max (absolute) | 4.6670059e-16 | 0 | 4.67e-16 | 1.0e-10 | PASS |
| angle [partB]: kern area, antipoles (JS) vs half-plane intersection (scipy) | 0.00019135036 | 0.00019135036 | 8.50e-16 | 1.0e-09 | PASS |
| angle [partB]: every kern vertex found by both methods (largest distance, mm) (absolute) | 5.553825e-15 | 0 | 5.55e-15 | 1.0e-09 | PASS |
| angle with fillet [partB]: A, JavaScript part formulas vs Python Green's theorem / quadrature | 0.00060978193 | 0.00060978193 | 0.00e+00 | 1.0e-11 | PASS |
| angle with fillet [partB]: centroid y (mm) (absolute) | 14.966659 | 14.966659 | 3.55e-15 | 1.0e-09 | PASS |
| angle with fillet [partB]: centroid z (mm) (absolute) | -14.966659 | -14.966659 | 0.00e+00 | 1.0e-09 | PASS |
| angle with fillet [partB]: I_z | 1.449661e-07 | 1.449661e-07 | 0.00e+00 | 1.0e-10 | PASS |
| angle with fillet [partB]: I_y | 1.449661e-07 | 1.449661e-07 | 0.00e+00 | 1.0e-10 | PASS |
| angle with fillet [partB]: I_yz / I_max (absolute) | 0.36879408 | 0.36879408 | 1.11e-16 | 1.0e-10 | PASS |
| angle with fillet [partB]: I_max, Mohr formula (JS) vs eigenvalue (numpy) | 2.296653e-07 | 2.296653e-07 | 1.15e-16 | 1.0e-10 | PASS |
| angle with fillet [partB]: I_min, Mohr formula (JS) vs eigenvalue (numpy) | 6.0266893e-08 | 6.0266893e-08 | 4.39e-16 | 1.0e-10 | PASS |
| angle with fillet [partB]: corner stresses, Eq. 4.58 in principal axes (JS) vs general S⁻¹ form (Python), max \|Δ\|/σ_max (absolute) | 3.5082137e-16 | 0 | 3.51e-16 | 1.0e-10 | PASS |
| angle with fillet [partB]: kern area, antipoles (JS) vs half-plane intersection (scipy) | 0.00019066618 | 0.00019066618 | 1.14e-15 | 1.0e-09 | PASS |
| angle with fillet [partB]: every kern vertex found by both methods (largest distance, mm) (absolute) | 1.0971355e-14 | 0 | 1.10e-14 | 1.0e-09 | PASS |
| tee [tee]: A, JavaScript part formulas vs Python Green's theorem / quadrature | 0.00228 | 0.00228 | 3.80e-16 | 1.0e-11 | PASS |
| tee [tee]: centroid y (mm) (absolute) | 85.578947 | 85.578947 | 1.42e-14 | 1.0e-09 | PASS |
| tee [tee]: centroid z (mm) (absolute) | 0 | -1.9813636e-15 | 1.98e-15 | 1.0e-09 | PASS |
| tee [tee]: I_z | 3.1104758e-06 | 3.1104758e-06 | 2.18e-15 | 1.0e-10 | PASS |
| tee [tee]: I_y | 1.009e-06 | 1.009e-06 | 2.10e-16 | 1.0e-10 | PASS |
| tee [tee]: I_yz / I_max (absolute) | 0 | 1.2429085e-16 | 1.24e-16 | 1.0e-10 | PASS |
| tee [tee]: I_max, Mohr formula (JS) vs eigenvalue (numpy) | 3.1104758e-06 | 3.1104758e-06 | 2.18e-15 | 1.0e-10 | PASS |
| tee [tee]: I_min, Mohr formula (JS) vs eigenvalue (numpy) | 1.009e-06 | 1.009e-06 | 2.10e-16 | 1.0e-10 | PASS |
| tee [tee]: corner stresses, Eq. 4.58 in principal axes (JS) vs general S⁻¹ form (Python), max \|Δ\|/σ_max (absolute) | 2.2135572e-15 | 0 | 2.21e-15 | 1.0e-10 | PASS |
| tee [tee]: kern area, antipoles (JS) vs half-plane intersection (scipy) | 0.00064805382 | 0.00064805382 | 2.68e-15 | 1.0e-09 | PASS |
| tee [tee]: every kern vertex found by both methods (largest distance, mm) (absolute) | 1.1113417e-13 | 0 | 1.11e-13 | 1.0e-09 | PASS |
| zsec [zsec]: A, JavaScript part formulas vs Python Green's theorem / quadrature | 0.0024 | 0.0024 | 0.00e+00 | 1.0e-11 | PASS |
| zsec [zsec]: centroid y (mm) (absolute) | 60 | 60 | 0.00e+00 | 1.0e-09 | PASS |
| zsec [zsec]: centroid z (mm) (absolute) | -5.6468863e-15 | -7.5291818e-15 | 1.88e-15 | 1.0e-09 | PASS |
| zsec [zsec]: I_z | 5.52e-06 | 5.52e-06 | 2.76e-15 | 1.0e-10 | PASS |
| zsec [zsec]: I_y | 2.9312e-06 | 2.9312e-06 | 2.89e-16 | 1.0e-10 | PASS |
| zsec [zsec]: I_yz / I_max (absolute) | 0.41423485 | 0.41423485 | 6.66e-16 | 1.0e-10 | PASS |
| zsec [zsec]: I_max, Mohr formula (JS) vs eigenvalue (numpy) | 7.6478354e-06 | 7.6478354e-06 | 1.33e-15 | 1.0e-10 | PASS |
| zsec [zsec]: I_min, Mohr formula (JS) vs eigenvalue (numpy) | 8.0336457e-07 | 8.0336457e-07 | 7.12e-15 | 1.0e-10 | PASS |
| zsec [zsec]: corner stresses, Eq. 4.58 in principal axes (JS) vs general S⁻¹ form (Python), max \|Δ\|/σ_max (absolute) | 5.7942512e-15 | 0 | 5.79e-15 | 1.0e-10 | PASS |
| zsec [zsec]: kern area, antipoles (JS) vs half-plane intersection (scipy) | 0.00085704457 | 0.00085704457 | 8.60e-15 | 1.0e-09 | PASS |
| zsec [zsec]: every kern vertex found by both methods (largest distance, mm) (absolute) | 1.2490009e-13 | 0 | 1.25e-13 | 1.0e-09 | PASS |
| angle [design]: A, JavaScript part formulas vs Python Green's theorem / quadrature | 0.0007661275 | 0.0007661275 | 1.42e-16 | 1.0e-11 | PASS |
| angle [design]: centroid y (mm) (absolute) | 12.532895 | 12.532895 | 1.78e-15 | 1.0e-09 | PASS |
| angle [design]: centroid z (mm) (absolute) | -25.232895 | -25.232895 | 1.07e-14 | 1.0e-09 | PASS |
| angle [design]: I_z | 1.6311098e-07 | 1.6311098e-07 | 1.62e-16 | 1.0e-10 | PASS |
| angle [design]: I_y | 4.5252189e-07 | 4.5252189e-07 | 7.02e-16 | 1.0e-10 | PASS |
| angle [design]: I_yz / I_max (absolute) | 0.30285175 | 0.30285175 | 2.22e-16 | 1.0e-10 | PASS |
| angle [design]: I_max, Mohr formula (JS) vs eigenvalue (numpy) | 5.2217152e-07 | 5.2217152e-07 | 4.06e-16 | 1.0e-10 | PASS |
| angle [design]: I_min, Mohr formula (JS) vs eigenvalue (numpy) | 9.346134e-08 | 9.346134e-08 | 8.50e-16 | 1.0e-10 | PASS |
| angle [design]: corner stresses, Eq. 4.58 in principal axes (JS) vs general S⁻¹ form (Python), max \|Δ\|/σ_max (absolute) | 1.259296e-16 | 0 | 1.26e-16 | 1.0e-10 | PASS |
| angle [design]: kern area, antipoles (JS) vs half-plane intersection (scipy) | 0.00029700763 | 0.00029700763 | 1.10e-15 | 1.0e-09 | PASS |
| angle [design]: every kern vertex found by both methods (largest distance, mm) (absolute) | 3.1417178e-14 | 0 | 3.14e-14 | 1.0e-09 | PASS |
| channel [partA2]: A, JavaScript part formulas vs Python Green's theorem / quadrature | 0.001584 | 0.001584 | 1.37e-16 | 1.0e-11 | PASS |
| channel [partA2]: centroid y (mm) (absolute) | 60 | 60 | 2.13e-14 | 1.0e-09 | PASS |
| channel [partA2]: centroid z (mm) (absolute) | 19.363636 | 19.363636 | 7.11e-15 | 1.0e-09 | PASS |
| channel [partA2]: I_z | 3.578112e-06 | 3.578112e-06 | 2.37e-15 | 1.0e-10 | PASS |
| channel [partA2]: I_y | 5.6556655e-07 | 5.6556655e-07 | 2.06e-15 | 1.0e-10 | PASS |
| channel [partA2]: I_yz / I_max (absolute) | 5.9181556e-17 | 4.7345245e-16 | 4.14e-16 | 1.0e-10 | PASS |
| channel [partA2]: I_max, Mohr formula (JS) vs eigenvalue (numpy) | 3.578112e-06 | 3.578112e-06 | 2.37e-15 | 1.0e-10 | PASS |
| channel [partA2]: I_min, Mohr formula (JS) vs eigenvalue (numpy) | 5.6556655e-07 | 5.6556655e-07 | 1.87e-15 | 1.0e-10 | PASS |
| channel [partA2]: corner stresses, Eq. 4.58 in principal axes (JS) vs general S⁻¹ form (Python), max \|Δ\|/σ_max (absolute) | 1.5879665e-15 | 0 | 1.59e-15 | 1.0e-10 | PASS |
| channel [partA2]: kern area, antipoles (JS) vs half-plane intersection (scipy) | 0.0010250039 | 0.0010250039 | 4.02e-15 | 1.0e-09 | PASS |
| channel [partA2]: every kern vertex found by both methods (largest distance, mm) (absolute) | 9.1422134e-14 | 0 | 9.14e-14 | 1.0e-09 | PASS |
| tube [tube8]: A, JavaScript part formulas vs Python Green's theorem / quadrature | 0.00034836139 | 0.00034836139 | 0.00e+00 | 1.0e-11 | PASS |
| tube [tube8]: centroid y (mm) (absolute) | 0 | 6.9500466e-16 | 6.95e-16 | 1.0e-09 | PASS |
| tube [tube8]: centroid z (mm) (absolute) | 0 | 1.4322586e-15 | 1.43e-15 | 1.0e-09 | PASS |
| tube [tube8]: I_z | 5.3553433e-08 | 5.3553433e-08 | 3.71e-16 | 1.0e-10 | PASS |
| tube [tube8]: I_y | 5.3553433e-08 | 5.3553433e-08 | 4.94e-16 | 1.0e-10 | PASS |
| tube [tube8]: I_yz / I_max (absolute) | 0 | -3.5309385e-17 | 3.53e-17 | 1.0e-10 | PASS |
| tube [tube8]: I_max, Mohr formula (JS) vs eigenvalue (numpy) | 5.3553433e-08 | 5.3553433e-08 | 3.71e-16 | 1.0e-10 | PASS |
| tube [tube8]: I_min, Mohr formula (JS) vs eigenvalue (numpy) | 5.3553433e-08 | 5.3553433e-08 | 4.94e-16 | 1.0e-10 | PASS |
| tube [tube8]: corner stresses, Eq. 4.58 in principal axes (JS) vs general S⁻¹ form (Python), max \|Δ\|/σ_max (absolute) | 4.7864198e-16 | 0 | 4.79e-16 | 1.0e-10 | PASS |
| tube [tube8]: kern area vs π r_k², r_k = (c₂² + c₁²)/(4c₂) (360-gon) | 0.00020457496 | 0.00020458534 | 5.08e-05 | 2.0e-04 | PASS |
| beam-column P = 25 kN, EI = 590 N·m², L = 0.25 m, a = 25 mm: C_mid, JS closed form vs scipy solve_bvp | 0.66790071 | 0.66790071 | 9.81e-15 | 1.0e-07 | PASS |
| beam-column P = 25 kN, EI = 590 N·m², L = 0.25 m, a = 25 mm: C at the ends of the free length | 0.90147253 | 0.90147253 | 1.11e-15 | 1.0e-07 | PASS |
| beam-column P = 25 kN, EI = 590 N·m², L = 0.25 m, a = 25 mm: buckling load with end blocks, JS bisection vs scipy brentq | 65180.162 | 65180.162 | 0.00e+00 | 1.0e-09 | PASS |
| beam-column P = -25 kN, EI = 590 N·m², L = 0.25 m, a = 25 mm: C_mid, JS closed form vs scipy solve_bvp | 1.7588665 | 1.7588665 | 1.59e-14 | 1.0e-07 | PASS |
| beam-column P = -25 kN, EI = 590 N·m², L = 0.25 m, a = 25 mm: C at the ends of the free length | 1.2080385 | 1.2080385 | 4.60e-15 | 1.0e-07 | PASS |
| beam-column P = -25 kN, EI = 590 N·m², L = 0.25 m, a = 25 mm: buckling load with end blocks, JS bisection vs scipy brentq | 65180.162 | 65180.162 | 0.00e+00 | 1.0e-09 | PASS |
| beam-column P = 30 kN, EI = 9500 N·m², L = 0.25 m, a = 25 mm: C_mid, JS closed form vs scipy solve_bvp | 0.96644275 | 0.96644275 | 0.00e+00 | 1.0e-07 | PASS |
| beam-column P = 30 kN, EI = 9500 N·m², L = 0.25 m, a = 25 mm: C at the ends of the free length | 0.99038411 | 0.99038411 | 1.12e-16 | 1.0e-07 | PASS |
| beam-column P = 30 kN, EI = 9500 N·m², L = 0.25 m, a = 25 mm: buckling load with end blocks, JS bisection vs scipy brentq | 1049511.1 | 1049511.1 | 0.00e+00 | 1.0e-09 | PASS |
| beam-column P = -40 kN, EI = 590 N·m², L = 0.25 m, a = 0 mm: C_mid, JS closed form vs scipy solve_bvp | 1.9399559 | 1.9399559 | 6.07e-15 | 1.0e-07 | PASS |
| beam-column P = -40 kN, EI = 590 N·m², L = 0.25 m, a = 0 mm: C at the ends of the free length | 1 | 1 | 0.00e+00 | 1.0e-07 | PASS |
| beam-column P = -40 kN, EI = 590 N·m², L = 0.25 m, a = 0 mm: buckling load with end blocks, JS bisection vs scipy brentq | 93169.066 | 93169.066 | 0.00e+00 | 1.0e-09 | PASS |
| beam-column P = 40 kN, EI = 4113 N·m², L = 1.5 m, a = 75 mm: C_mid, JS closed form vs scipy solve_bvp | 0.1554108 | 0.1554108 | 1.07e-13 | 1.0e-07 | PASS |
| beam-column P = 40 kN, EI = 4113 N·m², L = 1.5 m, a = 75 mm: C at the ends of the free length | 0.81328575 | 0.81328575 | 8.19e-16 | 1.0e-07 | PASS |
| beam-column P = 40 kN, EI = 4113 N·m², L = 1.5 m, a = 75 mm: buckling load with end blocks, JS bisection vs scipy brentq | 14928.687 | 14928.687 | 4.63e-15 | 1.0e-09 | PASS |
| beam-column P = 5 kN, EI = 590 N·m², L = 0.25 m, a = 100 mm: C_mid, JS closed form vs scipy solve_bvp | 0.85089944 | 0.85089944 | 3.00e-15 | 1.0e-07 | PASS |
| beam-column P = 5 kN, EI = 590 N·m², L = 0.25 m, a = 100 mm: C at the ends of the free length | 0.90785987 | 0.90785987 | 1.22e-15 | 1.0e-07 | PASS |
| beam-column P = 5 kN, EI = 590 N·m², L = 0.25 m, a = 100 mm: buckling load with end blocks, JS bisection vs scipy brentq | 32711.793 | 32711.793 | 0.00e+00 | 1.0e-09 | PASS |
| tube: A, JS vs Python quadrature | 0.00034836139 | 0.00034836139 | 0.00e+00 | 1.0e-10 | PASS |
| tube: I, JS vs Python quadrature | 5.3553433e-08 | 5.3553433e-08 | 6.18e-16 | 1.0e-10 | PASS |
| tube: J, JS vs Python quadrature | 1.0710687e-07 | 1.0710687e-07 | 2.47e-16 | 1.0e-10 | PASS |
| tube at φ = 0.0°: σ_x, JS vs Python | 53357923 | 53357923 | 0.00e+00 | 1.0e-12 | PASS |
| tube at φ = 0.0°: τ = Tc/J + VQ/(It), JS vs Python | 21343169 | 21343169 | 0.00e+00 | 1.0e-12 | PASS |
| tube at φ = 34.4°: Q of the wall from the top, JS closed form vs quadrature | 5.4818212e-07 | 5.4818212e-07 | 3.86e-16 | 1.0e-09 | PASS |
| tube at φ = 34.4°: σ_x, JS vs Python | 44038194 | 44038194 | 0.00e+00 | 1.0e-12 | PASS |
| tube at φ = 34.4°: τ = Tc/J + VQ/(It), JS vs Python | 23277564 | 23277564 | 0.00e+00 | 1.0e-12 | PASS |
| tube at φ = 90.0°: Q of the wall from the top, JS closed form vs quadrature | 9.7084819e-07 | 9.7084819e-07 | 2.18e-16 | 1.0e-09 | PASS |
| tube at φ = 90.0°: τ = Tc/J + VQ/(It), JS vs Python | 24769044 | 24769044 | 0.00e+00 | 1.0e-12 | PASS |
| tube at φ = 137.5°: Q of the wall from the top, JS closed form vs quadrature | 6.5577221e-07 | 6.5577221e-07 | 3.23e-16 | 1.0e-09 | PASS |
| tube at φ = 137.5°: σ_x, JS vs Python | -39345797 | -39345797 | 0.00e+00 | 1.0e-12 | PASS |
| tube at φ = 137.5°: τ = Tc/J + VQ/(It), JS vs Python | 23657222 | 23657222 | 0.00e+00 | 1.0e-12 | PASS |
| tube at φ = 223.5°: Q of the wall from the top, JS closed form vs quadrature | -6.6771653e-07 | -6.6771653e-07 | 3.17e-16 | 1.0e-09 | PASS |
| tube at φ = 223.5°: σ_x, JS vs Python | -38734240 | -38734240 | 0.00e+00 | 1.0e-12 | PASS |
| tube at φ = 223.5°: τ = Tc/J + VQ/(It), JS vs Python | 18986968 | 18986968 | 0.00e+00 | 1.0e-12 | PASS |
| closure Part A e0: e_eff vs truth e·C_mid (mm), within 2u (absolute) | 0.044336841 | 0.06766563 | 2.33e-02 | 4.2e-02 | PASS |
| closure Part A e0: out-of-plane e_z vs truth (mm), within 0.02 mm (absolute) | 0.09361947 | 0.09377694 | 1.57e-04 | 2.0e-02 | PASS |
| closure Part A e0: σ₀ = Eε₀ vs P/A (truth E, truth A) | 46.65908 | 46.639041 | 4.30e-04 | 1.8e-02 | PASS |
| closure Part A e1: e_eff vs truth e·C_mid (mm), within 2u (absolute) | 8.1683008 | 8.1778747 | 9.57e-03 | 5.4e-02 | PASS |
| closure Part A e1: out-of-plane e_z vs truth (mm), within 0.02 mm (absolute) | 0.095942521 | 0.09377694 | 2.17e-03 | 2.0e-02 | PASS |
| closure Part A e1: σ₀ = Eε₀ vs P/A (truth E, truth A) | 46.5764 | 46.639041 | 1.34e-03 | 1.8e-02 | PASS |
| closure Part A e2: e_eff vs truth e·C_mid (mm), within 2u (absolute) | 16.465385 | 16.423415 | 4.20e-02 | 1.1e-01 | PASS |
| closure Part A e2: out-of-plane e_z vs truth (mm), within 0.02 mm (absolute) | 0.093120026 | 0.09377694 | 6.57e-04 | 2.0e-02 | PASS |
| closure Part A e2: σ₀ = Eε₀ vs P/A (truth E, truth A) | 46.54884 | 46.639041 | 1.93e-03 | 1.8e-02 | PASS |
| closure Part C at the largest load: C_mid vs truth, within 2u (absolute) | 0.66867479 | 0.66992723 | 1.25e-03 | 7.8e-03 | PASS |
| closure Part C at the largest load: C near the block vs truth, within 2u (absolute) | 0.76919028 | 0.77419866 | 5.01e-03 | 1.4e-02 | PASS |
| closure Part C at the largest load: w_mid vs truth (mm), within 2u (absolute) | 2.11 | 2.1121819 | 2.18e-03 | 1.2e-02 | PASS |
| closure Part C: EI from the LVDT fit vs truth E·hb³/12 (N·mm²), within 2u (absolute) | 5.9674997e+08 | 5.9499847e+08 | 1.75e+06 | 9.3e+06 | PASS |
| closure Part B G1: measured σ (bias removed) vs truth (MPa), within 2u (absolute) | -62.536219 | -63.596003 | 1.06e+00 | 1.7e+00 | PASS |
| closure Part B G2: measured σ (bias removed) vs truth (MPa), within 2u (absolute) | 48.174446 | 48.374079 | 2.00e-01 | 1.0e+00 | PASS |
| closure Part B G3: measured σ (bias removed) vs truth (MPa), within 2u (absolute) | 98.182411 | 99.401034 | 1.22e+00 | 1.9e+00 | PASS |
| closure Part B G4: measured σ (bias removed) vs truth (MPa), within 2u (absolute) | 124.00311 | 123.52434 | 4.79e-01 | 2.4e+00 | PASS |
| D1: largest stress of the reference design, simulation preset (JS) vs analysis (Python) | 118.3293 | 118.3293 | 2.40e-16 | 1.0e-09 | PASS |
| D1: P/A alone picks L38 × 38 × 4.8, which is overstressed | True | True | 0.00e+00 | 0.0e+00 | PASS |

140 of 140 passed.

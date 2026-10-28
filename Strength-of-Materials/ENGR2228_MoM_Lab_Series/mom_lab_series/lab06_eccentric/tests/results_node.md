## Lab 6 model tests (exact page code)

| Test | Value | Reference | Rel. difference | Tolerance | Result |
|---|---:|---:|---:|---:|---|
| rectangle: A = bh | 0.00064516000 | 0.00064516000 | 0.00e+0 | 1.0e-14 | PASS |
| rectangle: I_z = bh³/12 | 1.3874381e-7 | 1.3874381e-7 | 0.00e+0 | 1.0e-13 | PASS |
| rectangle: I_y = hb³/12 | 8.6714880e-9 | 8.6714880e-9 | 0.00e+0 | 1.0e-13 | PASS |
| rectangle: I_yz = 0 (absolute difference) | 0.0000000 | 0.0000000 | 0.00e+0 | 1.0e-20 | PASS |
| rectangle (h > b): major axis along z, θp = 0 (absolute difference) | 0.0000000 | 0.0000000 | 0.00e+0 | 1.0e-12 | PASS |
| rectangle, e = h/3 class: σ_max = (P/A)(1 + 6e/h) (Beer Eq. 4.50) | 1.3959181e+8 | 1.3959181e+8 | 0.00e+0 | 1.0e-13 | PASS |
| rectangle: σ_min = (P/A)(1 − 6e/h) | -46591629 | -46591629 | 1.60e-16 | 1.0e-12 | PASS |
| rectangle: neutral axis y₀ = −r²/e = −h²/(12e) | -0.012687512 | -0.012687512 | 0.00e+0 | 1.0e-12 | PASS |
| rectangle: kern half-diagonal along y = h/6 | 0.0084666667 | 0.0084666667 | 2.05e-16 | 1.0e-12 | PASS |
| rectangle: kern half-diagonal along z = b/6 | 0.0021166667 | 0.0021166667 | 1.02e-15 | 1.0e-12 | PASS |
| rectangle: kern area = hb/18 | 0.000035842222 | 0.000035842222 | 9.45e-16 | 1.0e-12 | PASS |
| rectangle, load at the kern vertex (h/6, 0): σ at the far edge = 0 (in units of P/A) (absolute difference) | 1.6022722e-16 | 0.0000000 | 1.60e-16 | 1.0e-12 | PASS |
| angle: area | 0.00060483750 | 0.00060483750 | 0.00e+0 | 1.0e-13 | PASS |
| angle: centroid y | 0.015028333 | 0.015028333 | 0.00e+0 | 1.0e-12 | PASS |
| angle: centroid z | -0.015028333 | -0.015028333 | 0.00e+0 | 1.0e-12 | PASS |
| angle: I_z by parallel axes | 1.4467836e-7 | 1.4467836e-7 | 0.00e+0 | 1.0e-12 | PASS |
| equal-leg angle: I_y = I_z | 1.4467836e-7 | 1.4467836e-7 | 3.66e-16 | 1.0e-12 | PASS |
| angle: I_yz by parallel axes (own products zero) | 8.4980583e-8 | 8.4980583e-8 | 1.56e-16 | 1.0e-12 | PASS |
| equal-leg angle: θp = −45° (major axis along the line of symmetry) | -0.78539816 | -0.78539816 | 2.83e-16 | 1.0e-12 | PASS |
| equal-leg angle: I_max = I_z + \|I_yz\| | 2.2965894e-7 | 2.2965894e-7 | 1.15e-16 | 1.0e-12 | PASS |
| equal-leg angle: I_min = I_z − \|I_yz\| | 5.9697775e-8 | 5.9697775e-8 | 6.65e-16 | 1.0e-12 | PASS |
| angle L2 × 2 × 1/4: r_min = 0.391 in (handbook, 3 significant figures) | 0.39113439 | 0.39100000 | 3.44e-4 | 2.0e-3 | PASS |
| fillet (spandrel): area = (1 − π/4) r² | 0.0000049444263 | 0.0000049444263 | 1.54e-15 | 1.0e-12 | PASS |
| fillet: centroid 0.2234 r from each straight edge = r(10 − 3π)/(3(4 − π)) | 0.0010721661 | 0.0010721661 | 4.85e-15 | 1.0e-11 | PASS |
| fillet: centroid height above the leg face, same distance (symmetry) | 0.0010721661 | 0.0010721661 | 4.85e-15 | 1.0e-11 | PASS |
| tube: I = π(c₂⁴ − c₁⁴)/4 | 5.3553433e-8 | 5.3553433e-8 | 0.00e+0 | 1.0e-13 | PASS |
| tube: kern radius = (c₂² + c₁²)/(4c₂) | 0.0080697917 | 0.0080697917 | 0.00e+0 | 1.0e-13 | PASS |
| rect [partA2]: A, exact parts vs grid (N_g = 512) | 0.00064516000 | 0.00064516000 | 4.11e-12 | 1.0e-9 | PASS |
| rect [partA2]: I_z, exact parts vs grid | 1.3874328e-7 | 1.3874381e-7 | 3.81e-6 | 2.0e-5 | PASS |
| rect [partA2]: I_y, exact parts vs grid | 8.6714550e-9 | 8.6714880e-9 | 3.81e-6 | 2.0e-5 | PASS |
| rect [partA2]: I_min, Mohr formula vs grid | 8.6714550e-9 | 8.6714880e-9 | 3.81e-6 | 2.0e-5 | PASS |
| rect [partA2]: product of inertia in the principal axes = 0 (absolute difference) | 0.0000000 | 0.0000000 | 0.00e+0 | 1.0e-12 | PASS |
| rect [partA2]: θp points to the MAJOR axis (I about u = I_max) | 1.3874381e-7 | 1.3874381e-7 | 0.00e+0 | 1.0e-12 | PASS |
| rect [partA2]: corner stresses, Eq. 4.58 vs equilibrium solve (max \|Δ\|/σ_max) (absolute difference) | 0.0000025439764 | 0.0000000 | 2.54e-6 | 2.0e-4 | PASS |
| rect [partA2]: ∫σ dA = P | 30000.000 | 30000.000 | 2.37e-13 | 1.0e-4 | PASS |
| rect [partA2]: ∫σ y dA = P y_P (moment of the load) | 508.49224 | 508.50000 | 1.53e-5 | 1.0e-4 | PASS |
| rect [partA2]: kern area, antipoles vs 720-ray bisection | 0.000035841949 | 0.000035842222 | 7.63e-6 | 5.0e-4 | PASS |
| rect [partA2]: load at each kern vertex puts σ = 0 along its hull edge (absolute difference) | 0.0000000 | 0.0000000 | 0.00e+0 | 1.0e-10 | PASS |
| rect [partA2]: grid error in I_min falls as N_g⁻² (observed 2.000) | true | true | 0.00e+0 | 0.0e+0 | PASS |
| angle [partB]: A, exact parts vs grid (N_g = 512) | 0.00060483750 | 0.00060483750 | 8.61e-12 | 1.0e-9 | PASS |
| angle [partB]: I_z, exact parts vs grid | 1.4467809e-7 | 1.4467836e-7 | 1.85e-6 | 2.0e-5 | PASS |
| angle [partB]: I_y, exact parts vs grid | 1.4467818e-7 | 1.4467836e-7 | 1.25e-6 | 2.0e-5 | PASS |
| angle [partB]: I_yz, exact parts vs grid | 8.4980583e-8 | 8.4980583e-8 | 1.34e-11 | 2.0e-5 | PASS |
| angle [partB]: I_min, Mohr formula vs grid | 5.9697551e-8 | 5.9697775e-8 | 3.77e-6 | 2.0e-5 | PASS |
| angle [partB]: product of inertia in the principal axes = 0 (absolute difference) | -2.6411427e-17 | 0.0000000 | 2.64e-17 | 1.0e-12 | PASS |
| angle [partB]: θp points to the MAJOR axis (I about u = I_max) | 2.2965894e-7 | 2.2965894e-7 | 0.00e+0 | 1.0e-12 | PASS |
| angle [partB]: corner stresses, Eq. 4.58 vs equilibrium solve (max \|Δ\|/σ_max) (absolute difference) | 0.0000024330406 | 0.0000000 | 2.43e-6 | 2.0e-4 | PASS |
| angle [partB]: ∫σ dA = P | 30000.000 | 30000.000 | 4.00e-12 | 1.0e-4 | PASS |
| angle [partB]: ∫σ y dA = P y_P (moment of the load) | -142.79598 | -142.80000 | 2.81e-5 | 1.0e-4 | PASS |
| angle [partB]: ∫σ z dA = P z_P | -857.39956 | -857.40000 | 5.17e-7 | 1.0e-4 | PASS |
| angle [partB]: kern area, antipoles vs 720-ray bisection | 0.00019132800 | 0.00019135036 | 1.17e-4 | 5.0e-4 | PASS |
| angle [partB]: load at each kern vertex puts σ = 0 along its hull edge (absolute difference) | 5.5009650e-16 | 0.0000000 | 5.50e-16 | 1.0e-10 | PASS |
| angle [partB]: grid error in I_min falls as N_g⁻² (observed 2.000) | true | true | 0.00e+0 | 0.0e+0 | PASS |
| angle with fillet [partB]: A, exact parts vs grid (N_g = 512) | 0.00060978193 | 0.00060978193 | 1.23e-11 | 1.0e-9 | PASS |
| angle with fillet [partB]: I_z, exact parts vs grid | 1.4496583e-7 | 1.4496610e-7 | 1.85e-6 | 2.0e-5 | PASS |
| angle with fillet [partB]: I_y, exact parts vs grid | 1.4496592e-7 | 1.4496610e-7 | 1.25e-6 | 2.0e-5 | PASS |
| angle with fillet [partB]: I_yz, exact parts vs grid | 8.4699204e-8 | 8.4699205e-8 | 2.15e-9 | 2.0e-5 | PASS |
| angle with fillet [partB]: I_min, Mohr formula vs grid | 6.0266669e-8 | 6.0266893e-8 | 3.72e-6 | 2.0e-5 | PASS |
| angle with fillet [partB]: product of inertia in the principal axes = 0 (absolute difference) | -2.5941632e-17 | 0.0000000 | 2.59e-17 | 1.0e-12 | PASS |
| angle with fillet [partB]: θp points to the MAJOR axis (I about u = I_max) | 2.2966530e-7 | 2.2966530e-7 | 0.00e+0 | 1.0e-12 | PASS |
| angle with fillet [partB]: corner stresses, Eq. 4.58 vs equilibrium solve (max \|Δ\|/σ_max) (absolute difference) | 0.0000024130558 | 0.0000000 | 2.41e-6 | 2.0e-4 | PASS |
| angle with fillet [partB]: ∫σ dA = P | 30000.000 | 30000.000 | 8.57e-9 | 1.0e-4 | PASS |
| angle with fillet [partB]: ∫σ y dA = P y_P (moment of the load) | -144.64624 | -144.65024 | 2.76e-5 | 1.0e-4 | PASS |
| angle with fillet [partB]: ∫σ z dA = P z_P | -855.54930 | -855.54976 | 5.33e-7 | 1.0e-4 | PASS |
| angle with fillet [partB]: kern area, antipoles vs 720-ray bisection | 0.00019062318 | 0.00019066618 | 2.26e-4 | 5.0e-4 | PASS |
| angle with fillet [partB]: load at each kern vertex puts σ = 0 along its hull edge (absolute difference) | 5.5459343e-16 | 0.0000000 | 5.55e-16 | 1.0e-10 | PASS |
| angle with fillet [partB]: grid error in I_min falls as N_g⁻² (observed 2.000) | true | true | 0.00e+0 | 0.0e+0 | PASS |
| tee [tee]: A, exact parts vs grid (N_g = 512) | 0.0022800000 | 0.0022800000 | 5.36e-14 | 1.0e-9 | PASS |
| tee [tee]: I_z, exact parts vs grid | 0.0000031104717 | 0.0000031104758 | 1.31e-6 | 2.0e-5 | PASS |
| tee [tee]: I_y, exact parts vs grid | 0.0000010089962 | 0.0000010090000 | 3.81e-6 | 2.0e-5 | PASS |
| tee [tee]: I_min, Mohr formula vs grid | 0.0000010089962 | 0.0000010090000 | 3.81e-6 | 2.0e-5 | PASS |
| tee [tee]: product of inertia in the principal axes = 0 (absolute difference) | 0.0000000 | 0.0000000 | 0.00e+0 | 1.0e-12 | PASS |
| tee [tee]: θp points to the MAJOR axis (I about u = I_max) | 0.0000031104758 | 0.0000031104758 | 0.00e+0 | 1.0e-12 | PASS |
| tee [tee]: corner stresses, Eq. 4.58 vs equilibrium solve (max \|Δ\|/σ_max) (absolute difference) | 0.0000012550546 | 0.0000000 | 1.26e-6 | 2.0e-4 | PASS |
| tee [tee]: ∫σ dA = P | -40000.000 | -40000.000 | 5.62e-13 | 1.0e-4 | PASS |
| tee [tee]: ∫σ y dA = P y_P (moment of the load) | -4423.1527 | -4423.1579 | 1.18e-6 | 1.0e-4 | PASS |
| tee [tee]: kern area, antipoles vs 720-ray bisection | 0.00064804194 | 0.00064805382 | 1.83e-5 | 5.0e-4 | PASS |
| tee [tee]: load at each kern vertex puts σ = 0 along its hull edge (absolute difference) | 3.0780711e-16 | 0.0000000 | 3.08e-16 | 1.0e-10 | PASS |
| tee [tee]: grid error in I_min falls as N_g⁻² (observed 2.000) | true | true | 0.00e+0 | 0.0e+0 | PASS |
| zsec [zsec]: A, exact parts vs grid (N_g = 512) | 0.0024000000 | 0.0024000000 | 1.89e-11 | 1.0e-9 | PASS |
| zsec [zsec]: I_z, exact parts vs grid | 0.0000055199974 | 0.0000055200000 | 4.70e-7 | 2.0e-5 | PASS |
| zsec [zsec]: I_y, exact parts vs grid | 0.0000029311967 | 0.0000029312000 | 1.12e-6 | 2.0e-5 | PASS |
| zsec [zsec]: I_yz, exact parts vs grid | 0.0000031680000 | 0.0000031680000 | 1.18e-13 | 2.0e-5 | PASS |
| zsec [zsec]: I_min, Mohr formula vs grid | 8.0336151e-7 | 8.0336457e-7 | 3.81e-6 | 2.0e-5 | PASS |
| zsec [zsec]: product of inertia in the principal axes = 0 (absolute difference) | -2.7688650e-17 | 0.0000000 | 2.77e-17 | 1.0e-12 | PASS |
| zsec [zsec]: θp points to the MAJOR axis (I about u = I_max) | 0.0000076478354 | 0.0000076478354 | 2.22e-16 | 1.0e-12 | PASS |
| zsec [zsec]: corner stresses, Eq. 4.58 vs equilibrium solve (max \|Δ\|/σ_max) (absolute difference) | 0.0000021586813 | 0.0000000 | 2.16e-6 | 2.0e-4 | PASS |
| zsec [zsec]: ∫σ dA = P | 50000.000 | 50000.000 | 1.62e-12 | 1.0e-4 | PASS |
| zsec [zsec]: ∫σ y dA = P y_P (moment of the load) | 4499.9926 | 4500.0000 | 1.65e-6 | 1.0e-4 | PASS |
| zsec [zsec]: kern area, antipoles vs 720-ray bisection | 0.00085677456 | 0.00085704457 | 3.15e-4 | 5.0e-4 | PASS |
| zsec [zsec]: load at each kern vertex puts σ = 0 along its hull edge (absolute difference) | 8.1854523e-16 | 0.0000000 | 8.19e-16 | 1.0e-10 | PASS |
| zsec [zsec]: grid error in I_min falls as N_g⁻² (observed 2.000) | true | true | 0.00e+0 | 0.0e+0 | PASS |
| angle [design]: A, exact parts vs grid (N_g = 512) | 0.00076612750 | 0.00076612750 | 9.09e-13 | 1.0e-9 | PASS |
| angle [design]: I_z, exact parts vs grid | 1.6311070e-7 | 1.6311098e-7 | 1.66e-6 | 2.0e-5 | PASS |
| angle [design]: I_y, exact parts vs grid | 4.5252120e-7 | 4.5252189e-7 | 1.53e-6 | 2.0e-5 | PASS |
| angle [design]: I_yz, exact parts vs grid | 1.5814056e-7 | 1.5814056e-7 | 1.61e-12 | 2.0e-5 | PASS |
| angle [design]: I_min, Mohr formula vs grid | 9.3461001e-8 | 9.3461340e-8 | 3.63e-6 | 2.0e-5 | PASS |
| angle [design]: product of inertia in the principal axes = 0 (absolute difference) | 5.0691733e-17 | 0.0000000 | 5.07e-17 | 1.0e-12 | PASS |
| angle [design]: θp points to the MAJOR axis (I about u = I_max) | 5.2217152e-7 | 5.2217152e-7 | 0.00e+0 | 1.0e-12 | PASS |
| angle [design]: corner stresses, Eq. 4.58 vs equilibrium solve (max \|Δ\|/σ_max) (absolute difference) | 0.0000025096895 | 0.0000000 | 2.51e-6 | 2.0e-4 | PASS |
| angle [design]: ∫σ dA = P | 40000.000 | 40000.000 | 1.78e-12 | 1.0e-4 | PASS |
| angle [design]: ∫σ y dA = P y_P (moment of the load) | -190.59576 | -190.60000 | 2.22e-5 | 1.0e-4 | PASS |
| angle [design]: ∫σ z dA = P z_P | -1779.9991 | -1780.0000 | 5.19e-7 | 1.0e-4 | PASS |
| angle [design]: kern area, antipoles vs 720-ray bisection | 0.00029692813 | 0.00029700763 | 2.68e-4 | 5.0e-4 | PASS |
| angle [design]: load at each kern vertex puts σ = 0 along its hull edge (absolute difference) | 3.4839445e-16 | 0.0000000 | 3.48e-16 | 1.0e-10 | PASS |
| angle [design]: grid error in I_min falls as N_g⁻² (observed 2.002) | true | true | 0.00e+0 | 0.0e+0 | PASS |
| channel [partA2]: A, exact parts vs grid (N_g = 512) | 0.0015840000 | 0.0015840000 | 1.28e-11 | 1.0e-9 | PASS |
| channel [partA2]: I_z, exact parts vs grid | 0.0000035781087 | 0.0000035781120 | 9.26e-7 | 2.0e-5 | PASS |
| channel [partA2]: I_y, exact parts vs grid | 5.6556574e-7 | 5.6556655e-7 | 1.43e-6 | 2.0e-5 | PASS |
| channel [partA2]: I_min, Mohr formula vs grid | 5.6556574e-7 | 5.6556655e-7 | 1.43e-6 | 2.0e-5 | PASS |
| channel [partA2]: product of inertia in the principal axes = 0 (absolute difference) | 0.0000000 | 0.0000000 | 0.00e+0 | 1.0e-12 | PASS |
| channel [partA2]: θp points to the MAJOR axis (I about u = I_max) | 0.0000035781120 | 0.0000035781120 | 0.00e+0 | 1.0e-12 | PASS |
| channel [partA2]: corner stresses, Eq. 4.58 vs equilibrium solve (max \|Δ\|/σ_max) (absolute difference) | 9.0433331e-7 | 0.0000000 | 9.04e-7 | 2.0e-4 | PASS |
| channel [partA2]: ∫σ dA = P | 30000.000 | 30000.000 | 4.54e-13 | 1.0e-4 | PASS |
| channel [partA2]: ∫σ y dA = P y_P (moment of the load) | 2099.9989 | 2100.0000 | 5.29e-7 | 1.0e-4 | PASS |
| channel [partA2]: ∫σ z dA = P z_P | 1030.9065 | 1030.9091 | 2.50e-6 | 1.0e-4 | PASS |
| channel [partA2]: kern area, antipoles vs 720-ray bisection | 0.0010250015 | 0.0010250039 | 2.36e-6 | 5.0e-4 | PASS |
| channel [partA2]: load at each kern vertex puts σ = 0 along its hull edge (absolute difference) | 1.8007995e-16 | 0.0000000 | 1.80e-16 | 1.0e-10 | PASS |
| channel [partA2]: grid error in I_min falls as N_g⁻² (observed 2.000) | true | true | 0.00e+0 | 0.0e+0 | PASS |
| tube [tube8]: A, exact parts vs grid (N_g = 512) | 0.00034836139 | 0.00034836139 | 3.02e-13 | 1.0e-9 | PASS |
| tube [tube8]: I_z, exact parts vs grid | 5.3553432e-8 | 5.3553433e-8 | 3.13e-8 | 2.0e-5 | PASS |
| tube [tube8]: I_y, exact parts vs grid | 5.3553432e-8 | 5.3553433e-8 | 3.13e-8 | 2.0e-5 | PASS |
| tube [tube8]: I_min, Mohr formula vs grid | 5.3553432e-8 | 5.3553433e-8 | 3.13e-8 | 2.0e-5 | PASS |
| tube [tube8]: product of inertia in the principal axes = 0 (absolute difference) | 0.0000000 | 0.0000000 | 0.00e+0 | 1.0e-12 | PASS |
| tube [tube8]: θp points to the MAJOR axis (I about u = I_max) | 5.3553433e-8 | 5.3553433e-8 | 0.00e+0 | 1.0e-12 | PASS |
| tube [tube8]: corner stresses, Eq. 4.58 vs equilibrium solve (max \|Δ\|/σ_max) (absolute difference) | 1.6852605e-8 | 0.0000000 | 1.69e-8 | 2.0e-4 | PASS |
| tube [tube8]: ∫σ dA = P | 20000.000 | 20000.000 | 4.40e-14 | 1.0e-4 | PASS |
| tube [tube8]: ∫σ y dA = P y_P (moment of the load) | 99.999987 | 100.00000 | 1.25e-7 | 1.0e-4 | PASS |
| tube [tube8]: ∫σ z dA = P z_P | -159.99998 | -160.00000 | 1.25e-7 | 1.0e-4 | PASS |
| tube [tube8]: kern area, antipoles vs 720-ray bisection | 0.00020459052 | 0.00020457496 | 7.61e-5 | 5.0e-4 | PASS |
| tube [tube8]: grid error in I_min falls as N_g⁻² (observed 2.000) | true | true | 0.00e+0 | 0.0e+0 | PASS |
| angle: ignoring I_yz changes a corner stress by 1.69 P/A (> 1) | true | true | 0.00e+0 | 0.0e+0 | PASS |
| rectangle: the "naive" formula is exact when I_yz = 0 (absolute difference) | -5.9604645e-8 | 0.0000000 | 5.96e-8 | 1.0e-6 | PASS |
| rectangle: neutral-axis direction obeys Beer Eq. 4.57, tan φ = (I_z/I_y) tan θ | -9.6000000 | -9.6000000 | 1.11e-15 | 1.0e-12 | PASS |
| Part C: bending about the weak axis uses I_min = hb³/12 | 8.6714880e-9 | 8.6714880e-9 | 1.14e-15 | 1.0e-12 | PASS |
| Part C: C_mid, cosh closed form vs finite differences (N = 2048) | 0.67087636 | 0.67087635 | 8.14e-9 | 2.0e-7 | PASS |
| Part C: C at the ends of the free length, closed form vs FD | 0.90239928 | 0.90239928 | 5.91e-9 | 2.0e-7 | PASS |
| Part C: mid-length deflection e(1 − C), closed form vs FD | 0.0021063913 | 0.0021063913 | 1.66e-8 | 1.0e-6 | PASS |
| beam-column FD error falls as N⁻² (observed 1.999) | true | true | 0.00e+0 | 0.0e+0 | PASS |
| a = 0 limit: C_mid = 1/cosh(kL/2) | 0.74343627 | 0.74343627 | 0.00e+0 | 1.0e-14 | PASS |
| a = 0, compression: C_mid = sec(kL/2) (Beer §10.2, secant formula) | 1.4481726 | 1.4481726 | 0.00e+0 | 1.0e-14 | PASS |
| a = 0, compression: FD vs secant (N = 2048) | 1.4481726 | 1.4481726 | 2.20e-8 | 1.0e-6 | PASS |
| small loads: 1/C − 1 → (π²/8)(P/P_E) (a = 0) | 0.00012337259 | 0.00012337006 | 2.06e-5 | 1.0e-4 | PASS |
| buckling, a = 0: P_cr = π²EI/L² | 94347.974 | 94347.974 | 0.00e+0 | 1.0e-14 | PASS |
| buckling with end blocks: cos u − (2a/L) u sin u = 0 at the computed load (absolute difference) | 1.1102230e-16 | 0.0000000 | 1.11e-16 | 1.0e-12 | PASS |
| end blocks lower the buckling load: P_cr = 0.6996 P_E, between (L/(L + 2a))² and 1 | true | true | 0.00e+0 | 0.0e+0 | PASS |
| buckling with end blocks: transcendental root vs FD determinant (N = 1024) | 66004.901 | 66004.915 | 2.03e-7 | 2.0e-5 | PASS |
| buckling, a = 0: FD determinant (N = 1024) vs π²EI/L² | 94347.900 | 94347.974 | 7.84e-7 | 2.0e-6 | PASS |
| compression beyond P_cr is flagged as buckled | true | true | 0.00e+0 | 0.0e+0 | PASS |
| 5 % threshold, a = 0: cosh u = 1.05 → P = (2u/π)² P_E = 0.0403 P_E | 0.040195168 | 0.040195168 | 1.90e-15 | 1.0e-9 | PASS |
| 5 % threshold with blocks: closed form vs FD bisection | 2710.6237 | 2710.6237 | 9.69e-9 | 1.0e-5 | PASS |
| 5 % threshold in compression, a = 0: cos u = 1/1.05 | 0.038908834 | 0.038908834 | 3.57e-15 | 1.0e-9 | PASS |
| 5 % threshold in compression with blocks: closed form vs FD | 2620.3968 | 2620.3968 | 9.29e-9 | 1.0e-4 | PASS |
| Part C: largest σ at mid-length = P/A + P e C (b/2)/I_min | 1.1735370e+8 | 1.1735370e+8 | 0.00e+0 | 1.0e-12 | PASS |
| Part C: Eq. 4.58 (C = 1) largest σ | 1.5591567e+8 | 1.5591567e+8 | 9.56e-16 | 1.0e-12 | PASS |
| angle, minor axis: C_mid closed form vs FD | 0.89985754 | 0.89985754 | 2.67e-9 | 2.0e-6 | PASS |
| angle, major axis: C_mid closed form vs FD | 0.97222802 | 0.97222802 | 1.89e-10 | 2.0e-6 | PASS |
| angle: minor-axis bending uses I_min | 5.9697775e-8 | 5.9697775e-8 | 0.00e+0 | 1.0e-14 | PASS |
| angle: eccentricity components rebuild \|e\| (u² + v² = y_P² + z_P²) | 0.023983866 | 0.023983866 | 0.00e+0 | 1.0e-13 | PASS |
| tube, top: σ = F L_b c/I (tension on top of the cantilever) | 53357923 | 53357923 | 0.00e+0 | 1.0e-13 | PASS |
| tube, top: no transverse shear stress (Q = 0) (absolute difference) | 0.0000000 | 0.0000000 | 0.00e+0 | 1.0e-9 | PASS |
| tube: torsional shear Tc/J = F a_L c/(2I) | 21343169 | 21343169 | 0.00e+0 | 1.0e-13 | PASS |
| tube, side: τ_V = V (c₂³ − c₁³)/(3 I t) | 3425875.1 | 3425875.1 | 1.36e-16 | 1.0e-13 | PASS |
| tube, side: σ = P/A = 0 with no axial load (absolute difference) | 0.0000000 | 0.0000000 | 0.00e+0 | 1.0e-9 | PASS |
| thin-wall limit: τ_V,max → 2V/A | 5.2653658e+8 | 5.2653667e+8 | 1.67e-7 | 2.0e-3 | PASS |
| tube at φ = 0.0°: τ, closed form vs polar grid (N = 128) | 21343180 | 21343169 | 5.00e-7 | 2.0e-5 | PASS |
| tube at φ = 0.0°: σ, closed form vs polar grid | 53357950 | 53357923 | 5.00e-7 | 2.0e-5 | PASS |
| tube at φ = 22.9°: τ, closed form vs polar grid (N = 128) | 22677280 | 22677268 | 5.14e-7 | 2.0e-5 | PASS |
| tube at φ = 22.9°: σ, closed form vs polar grid | 49145927 | 49145902 | 5.00e-7 | 2.0e-5 | PASS |
| tube at φ = 90.0°: τ, closed form vs polar grid (N = 128) | 24769078 | 24769044 | 1.35e-6 | 2.0e-5 | PASS |
| tube at φ = 143.2°: τ, closed form vs polar grid (N = 128) | 23393504 | 23393460 | 1.88e-6 | 2.0e-5 | PASS |
| tube at φ = 143.2°: σ, closed form vs polar grid | -42747381 | -42747360 | 5.00e-7 | 2.0e-5 | PASS |
| tube at φ = 229.2°: τ, closed form vs polar grid (N = 128) | 18750363 | 18750459 | 5.10e-6 | 2.0e-5 | PASS |
| tube at φ = 229.2°: σ, closed form vs polar grid | -34877084 | -34877066 | 5.00e-7 | 2.0e-5 | PASS |
| tube: J = 2I, closed form vs polar grid (N = 128) | 1.0710681e-7 | 1.0710687e-7 | 5.00e-7 | 2.0e-5 | PASS |
| tube: polar-grid error in J falls as N⁻² (observed 2.000) | true | true | 0.00e+0 | 0.0e+0 | PASS |
| preset partA0: finite results | true | true | 0.00e+0 | 0.0e+0 | PASS |
| preset partA1: finite results | true | true | 0.00e+0 | 0.0e+0 | PASS |
| preset partA2: finite results | true | true | 0.00e+0 | 0.0e+0 | PASS |
| preset partB: finite results | true | true | 0.00e+0 | 0.0e+0 | PASS |
| preset partC: finite results | true | true | 0.00e+0 | 0.0e+0 | PASS |
| preset partAcol: finite results | true | true | 0.00e+0 | 0.0e+0 | PASS |
| preset design: finite results | true | true | 0.00e+0 | 0.0e+0 | PASS |
| preset zsec: finite results | true | true | 0.00e+0 | 0.0e+0 | PASS |
| preset tee: finite results | true | true | 0.00e+0 | 0.0e+0 | PASS |
| preset compression: finite results | true | true | 0.00e+0 | 0.0e+0 | PASS |
| preset tube8: finite results | true | true | 0.00e+0 | 0.0e+0 | PASS |
| preset partB: load point = gusset mid-plane under the horizontal leg (z = −28.58 mm) | -0.028580000 | -0.028580000 | 0.00e+0 | 1.0e-12 | PASS |
| preset partB: load point y = −4.76 mm (half the gusset thickness below the leg) | -0.0047600000 | -0.0047600000 | 3.64e-16 | 1.0e-12 | PASS |
| units: 30 kN in kip | 6.7442683 | 6.7442683 | 0.00e+0 | 1.0e-12 | PASS |
| units: 138 744 mm⁴ in in⁴ | 0.33333379 | 0.33333379 | 1.67e-16 | 1.0e-12 | PASS |
| units: angle in degrees | 90.000000 | 90.000000 | 0.00e+0 | 1.0e-14 | PASS |

192 of 192 passed.

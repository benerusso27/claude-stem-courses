# Verification record — lab06_eccentric

Run with `python3 shared/verify_lab.py lab06_eccentric` on 2026-10-27. Detailed tables are in the `results_*.md` files next to this one.

| Step | Result | Detail | Record |
|---|---|---|---|
| Build simulation page | PASS |  |  |
| Model tests: closed form vs independent numerics (Node, exact page code) | PASS | 192 of 192 passed | `results_node.md` |
| Independent re-implementation (Python/scipy) and data-pipeline closure | PASS | 140 of 140 passed | `results_python.md` |
| Handout re-solved from scratch vs instructor key | PASS | 38 of 38 agree | `results_from_scratch.md` |
| Cross-file consistency (units, symbols, sign convention, references) | PASS | 97 of 97 passed | `results_consistency.md` |
| Browser check, 375/1280 px, light/dark, every control | PASS | PASS | `results_browser.md` |

## Formula vs. independent numerical method (worst case over all material presets)

| Comparison | Worst relative difference | Tolerance | Result |
|---|---:|---:|---|
| rectangle: A = bh | 0.0e+00 | 1.0e-14 | PASS |
| rectangle: I_z = bh³/12 | 0.0e+00 | 1.0e-13 | PASS |
| rectangle: I_y = hb³/12 | 0.0e+00 | 1.0e-13 | PASS |
| rectangle: I_yz = 0 (absolute difference) | 0.0e+00 | 1.0e-20 | PASS |
| rectangle (h > b): major axis along z, θp = 0 (absolute difference) | 0.0e+00 | 1.0e-12 | PASS |
| rectangle, e = h/3 class: σ_max = (P/A)(1 + 6e/h) (Beer Eq. 4.50) | 0.0e+00 | 1.0e-13 | PASS |
| rectangle: σ_min = (P/A)(1 − 6e/h) | 1.6e-16 | 1.0e-12 | PASS |
| rectangle: neutral axis y₀ = −r²/e = −h²/(12e) | 0.0e+00 | 1.0e-12 | PASS |
| rectangle: kern half-diagonal along y = h/6 | 2.1e-16 | 1.0e-12 | PASS |
| rectangle: kern half-diagonal along z = b/6 | 1.0e-15 | 1.0e-12 | PASS |
| rectangle: kern area = hb/18 | 9.4e-16 | 1.0e-12 | PASS |
| rectangle, load at the kern vertex (h/6, 0): σ at the far edge = 0 (in units of P/A) (absolute difference) | 1.6e-16 | 1.0e-12 | PASS |
| angle: area | 0.0e+00 | 1.0e-13 | PASS |
| angle: centroid y | 0.0e+00 | 1.0e-12 | PASS |
| angle: centroid z | 0.0e+00 | 1.0e-12 | PASS |
| angle: I_z by parallel axes | 0.0e+00 | 1.0e-12 | PASS |
| equal-leg angle: I_y = I_z | 3.7e-16 | 1.0e-12 | PASS |
| angle: I_yz by parallel axes (own products zero) | 1.6e-16 | 1.0e-12 | PASS |
| equal-leg angle: θp = −45° (major axis along the line of symmetry) | 2.8e-16 | 1.0e-12 | PASS |
| equal-leg angle: I_max = I_z + \|I_yz\| | 1.1e-16 | 1.0e-12 | PASS |
| equal-leg angle: I_min = I_z − \|I_yz\| | 6.6e-16 | 1.0e-12 | PASS |
| angle L2 × 2 × 1/4: r_min = 0.391 in (handbook, 3 significant figures) | 3.4e-04 | 2.0e-3 | PASS |
| fillet (spandrel): area = (1 − π/4) r² | 1.5e-15 | 1.0e-12 | PASS |
| fillet: centroid 0.2234 r from each straight edge = r(10 − 3π)/(3(4 − π)) | 4.9e-15 | 1.0e-11 | PASS |
| fillet: centroid height above the leg face, same distance (symmetry) | 4.9e-15 | 1.0e-11 | PASS |
| tube: I = π(c₂⁴ − c₁⁴)/4 | 0.0e+00 | 1.0e-13 | PASS |
| tube: kern radius = (c₂² + c₁²)/(4c₂) | 0.0e+00 | 1.0e-13 | PASS |
| rect [partA2]: A, exact parts vs grid (N_g = 512) | 4.1e-12 | 1.0e-9 | PASS |
| rect [partA2]: I_z, exact parts vs grid | 3.8e-06 | 2.0e-5 | PASS |
| rect [partA2]: I_y, exact parts vs grid | 3.8e-06 | 2.0e-5 | PASS |
| rect [partA2]: I_min, Mohr formula vs grid | 3.8e-06 | 2.0e-5 | PASS |
| rect [partA2]: product of inertia in the principal axes = 0 (absolute difference) | 0.0e+00 | 1.0e-12 | PASS |
| rect [partA2]: θp points to the MAJOR axis (I about u = I_max) | 0.0e+00 | 1.0e-12 | PASS |
| rect [partA2]: corner stresses, Eq. 4.58 vs equilibrium solve (max \|Δ\|/σ_max) (absolute difference) | 2.5e-06 | 2.0e-4 | PASS |
| rect [partA2]: ∫σ dA = P | 2.4e-13 | 1.0e-4 | PASS |
| rect [partA2]: ∫σ y dA = P y_P (moment of the load) | 1.5e-05 | 1.0e-4 | PASS |
| rect [partA2]: kern area, antipoles vs 720-ray bisection | 7.6e-06 | 5.0e-4 | PASS |
| rect [partA2]: load at each kern vertex puts σ = 0 along its hull edge (absolute difference) | 0.0e+00 | 1.0e-10 | PASS |
| rect [partA2]: grid error in I_min falls as N_g⁻² (observed 2.000) | 0.0e+00 | 0.0e+0 | PASS |
| angle [partB]: A, exact parts vs grid (N_g = 512) | 8.6e-12 | 1.0e-9 | PASS |
| angle [partB]: I_z, exact parts vs grid | 1.9e-06 | 2.0e-5 | PASS |
| angle [partB]: I_y, exact parts vs grid | 1.3e-06 | 2.0e-5 | PASS |
| angle [partB]: I_yz, exact parts vs grid | 1.3e-11 | 2.0e-5 | PASS |
| angle [partB]: I_min, Mohr formula vs grid | 3.8e-06 | 2.0e-5 | PASS |
| angle [partB]: product of inertia in the principal axes = 0 (absolute difference) | 2.6e-17 | 1.0e-12 | PASS |
| angle [partB]: θp points to the MAJOR axis (I about u = I_max) | 0.0e+00 | 1.0e-12 | PASS |
| angle [partB]: corner stresses, Eq. 4.58 vs equilibrium solve (max \|Δ\|/σ_max) (absolute difference) | 2.4e-06 | 2.0e-4 | PASS |
| angle [partB]: ∫σ dA = P | 4.0e-12 | 1.0e-4 | PASS |
| angle [partB]: ∫σ y dA = P y_P (moment of the load) | 2.8e-05 | 1.0e-4 | PASS |
| angle [partB]: ∫σ z dA = P z_P | 5.2e-07 | 1.0e-4 | PASS |
| angle [partB]: kern area, antipoles vs 720-ray bisection | 1.2e-04 | 5.0e-4 | PASS |
| angle [partB]: load at each kern vertex puts σ = 0 along its hull edge (absolute difference) | 5.5e-16 | 1.0e-10 | PASS |
| angle [partB]: grid error in I_min falls as N_g⁻² (observed 2.000) | 0.0e+00 | 0.0e+0 | PASS |
| angle with fillet [partB]: A, exact parts vs grid (N_g = 512) | 1.2e-11 | 1.0e-9 | PASS |
| angle with fillet [partB]: I_z, exact parts vs grid | 1.9e-06 | 2.0e-5 | PASS |
| angle with fillet [partB]: I_y, exact parts vs grid | 1.3e-06 | 2.0e-5 | PASS |
| angle with fillet [partB]: I_yz, exact parts vs grid | 2.1e-09 | 2.0e-5 | PASS |
| angle with fillet [partB]: I_min, Mohr formula vs grid | 3.7e-06 | 2.0e-5 | PASS |
| angle with fillet [partB]: product of inertia in the principal axes = 0 (absolute difference) | 2.6e-17 | 1.0e-12 | PASS |
| angle with fillet [partB]: θp points to the MAJOR axis (I about u = I_max) | 0.0e+00 | 1.0e-12 | PASS |
| angle with fillet [partB]: corner stresses, Eq. 4.58 vs equilibrium solve (max \|Δ\|/σ_max) (absolute difference) | 2.4e-06 | 2.0e-4 | PASS |
| angle with fillet [partB]: ∫σ dA = P | 8.6e-09 | 1.0e-4 | PASS |
| angle with fillet [partB]: ∫σ y dA = P y_P (moment of the load) | 2.8e-05 | 1.0e-4 | PASS |
| angle with fillet [partB]: ∫σ z dA = P z_P | 5.3e-07 | 1.0e-4 | PASS |
| angle with fillet [partB]: kern area, antipoles vs 720-ray bisection | 2.3e-04 | 5.0e-4 | PASS |
| angle with fillet [partB]: load at each kern vertex puts σ = 0 along its hull edge (absolute difference) | 5.6e-16 | 1.0e-10 | PASS |
| angle with fillet [partB]: grid error in I_min falls as N_g⁻² (observed 2.000) | 0.0e+00 | 0.0e+0 | PASS |
| tee [tee]: A, exact parts vs grid (N_g = 512) | 5.4e-14 | 1.0e-9 | PASS |
| tee [tee]: I_z, exact parts vs grid | 1.3e-06 | 2.0e-5 | PASS |
| tee [tee]: I_y, exact parts vs grid | 3.8e-06 | 2.0e-5 | PASS |
| tee [tee]: I_min, Mohr formula vs grid | 3.8e-06 | 2.0e-5 | PASS |
| tee [tee]: product of inertia in the principal axes = 0 (absolute difference) | 0.0e+00 | 1.0e-12 | PASS |
| tee [tee]: θp points to the MAJOR axis (I about u = I_max) | 0.0e+00 | 1.0e-12 | PASS |
| tee [tee]: corner stresses, Eq. 4.58 vs equilibrium solve (max \|Δ\|/σ_max) (absolute difference) | 1.3e-06 | 2.0e-4 | PASS |
| tee [tee]: ∫σ dA = P | 5.6e-13 | 1.0e-4 | PASS |
| tee [tee]: ∫σ y dA = P y_P (moment of the load) | 1.2e-06 | 1.0e-4 | PASS |
| tee [tee]: kern area, antipoles vs 720-ray bisection | 1.8e-05 | 5.0e-4 | PASS |
| tee [tee]: load at each kern vertex puts σ = 0 along its hull edge (absolute difference) | 3.1e-16 | 1.0e-10 | PASS |
| tee [tee]: grid error in I_min falls as N_g⁻² (observed 2.000) | 0.0e+00 | 0.0e+0 | PASS |
| zsec [zsec]: A, exact parts vs grid (N_g = 512) | 1.9e-11 | 1.0e-9 | PASS |
| zsec [zsec]: I_z, exact parts vs grid | 4.7e-07 | 2.0e-5 | PASS |
| zsec [zsec]: I_y, exact parts vs grid | 1.1e-06 | 2.0e-5 | PASS |
| zsec [zsec]: I_yz, exact parts vs grid | 1.2e-13 | 2.0e-5 | PASS |
| zsec [zsec]: I_min, Mohr formula vs grid | 3.8e-06 | 2.0e-5 | PASS |
| zsec [zsec]: product of inertia in the principal axes = 0 (absolute difference) | 2.8e-17 | 1.0e-12 | PASS |
| zsec [zsec]: θp points to the MAJOR axis (I about u = I_max) | 2.2e-16 | 1.0e-12 | PASS |
| zsec [zsec]: corner stresses, Eq. 4.58 vs equilibrium solve (max \|Δ\|/σ_max) (absolute difference) | 2.2e-06 | 2.0e-4 | PASS |
| zsec [zsec]: ∫σ dA = P | 1.6e-12 | 1.0e-4 | PASS |
| zsec [zsec]: ∫σ y dA = P y_P (moment of the load) | 1.7e-06 | 1.0e-4 | PASS |
| zsec [zsec]: kern area, antipoles vs 720-ray bisection | 3.2e-04 | 5.0e-4 | PASS |
| zsec [zsec]: load at each kern vertex puts σ = 0 along its hull edge (absolute difference) | 8.2e-16 | 1.0e-10 | PASS |
| zsec [zsec]: grid error in I_min falls as N_g⁻² (observed 2.000) | 0.0e+00 | 0.0e+0 | PASS |
| angle [design]: A, exact parts vs grid (N_g = 512) | 9.1e-13 | 1.0e-9 | PASS |
| angle [design]: I_z, exact parts vs grid | 1.7e-06 | 2.0e-5 | PASS |
| angle [design]: I_y, exact parts vs grid | 1.5e-06 | 2.0e-5 | PASS |
| angle [design]: I_yz, exact parts vs grid | 1.6e-12 | 2.0e-5 | PASS |
| angle [design]: I_min, Mohr formula vs grid | 3.6e-06 | 2.0e-5 | PASS |
| angle [design]: product of inertia in the principal axes = 0 (absolute difference) | 5.1e-17 | 1.0e-12 | PASS |
| angle [design]: θp points to the MAJOR axis (I about u = I_max) | 0.0e+00 | 1.0e-12 | PASS |
| angle [design]: corner stresses, Eq. 4.58 vs equilibrium solve (max \|Δ\|/σ_max) (absolute difference) | 2.5e-06 | 2.0e-4 | PASS |
| angle [design]: ∫σ dA = P | 1.8e-12 | 1.0e-4 | PASS |
| angle [design]: ∫σ y dA = P y_P (moment of the load) | 2.2e-05 | 1.0e-4 | PASS |
| angle [design]: ∫σ z dA = P z_P | 5.2e-07 | 1.0e-4 | PASS |
| angle [design]: kern area, antipoles vs 720-ray bisection | 2.7e-04 | 5.0e-4 | PASS |
| angle [design]: load at each kern vertex puts σ = 0 along its hull edge (absolute difference) | 3.5e-16 | 1.0e-10 | PASS |
| angle [design]: grid error in I_min falls as N_g⁻² (observed 2.002) | 0.0e+00 | 0.0e+0 | PASS |
| channel [partA2]: A, exact parts vs grid (N_g = 512) | 1.3e-11 | 1.0e-9 | PASS |
| channel [partA2]: I_z, exact parts vs grid | 9.3e-07 | 2.0e-5 | PASS |
| channel [partA2]: I_y, exact parts vs grid | 1.4e-06 | 2.0e-5 | PASS |
| channel [partA2]: I_min, Mohr formula vs grid | 1.4e-06 | 2.0e-5 | PASS |
| channel [partA2]: product of inertia in the principal axes = 0 (absolute difference) | 0.0e+00 | 1.0e-12 | PASS |
| channel [partA2]: θp points to the MAJOR axis (I about u = I_max) | 0.0e+00 | 1.0e-12 | PASS |
| channel [partA2]: corner stresses, Eq. 4.58 vs equilibrium solve (max \|Δ\|/σ_max) (absolute difference) | 9.0e-07 | 2.0e-4 | PASS |
| channel [partA2]: ∫σ dA = P | 4.5e-13 | 1.0e-4 | PASS |
| channel [partA2]: ∫σ y dA = P y_P (moment of the load) | 5.3e-07 | 1.0e-4 | PASS |
| channel [partA2]: ∫σ z dA = P z_P | 2.5e-06 | 1.0e-4 | PASS |
| channel [partA2]: kern area, antipoles vs 720-ray bisection | 2.4e-06 | 5.0e-4 | PASS |
| channel [partA2]: load at each kern vertex puts σ = 0 along its hull edge (absolute difference) | 1.8e-16 | 1.0e-10 | PASS |
| channel [partA2]: grid error in I_min falls as N_g⁻² (observed 2.000) | 0.0e+00 | 0.0e+0 | PASS |
| tube [tube8]: A, exact parts vs grid (N_g = 512) | 3.0e-13 | 1.0e-9 | PASS |
| tube [tube8]: I_z, exact parts vs grid | 3.1e-08 | 2.0e-5 | PASS |
| tube [tube8]: I_y, exact parts vs grid | 3.1e-08 | 2.0e-5 | PASS |
| tube [tube8]: I_min, Mohr formula vs grid | 3.1e-08 | 2.0e-5 | PASS |
| tube [tube8]: product of inertia in the principal axes = 0 (absolute difference) | 0.0e+00 | 1.0e-12 | PASS |
| tube [tube8]: θp points to the MAJOR axis (I about u = I_max) | 0.0e+00 | 1.0e-12 | PASS |
| tube [tube8]: corner stresses, Eq. 4.58 vs equilibrium solve (max \|Δ\|/σ_max) (absolute difference) | 1.7e-08 | 2.0e-4 | PASS |
| tube [tube8]: ∫σ dA = P | 4.4e-14 | 1.0e-4 | PASS |
| tube [tube8]: ∫σ y dA = P y_P (moment of the load) | 1.2e-07 | 1.0e-4 | PASS |
| tube [tube8]: ∫σ z dA = P z_P | 1.2e-07 | 1.0e-4 | PASS |
| tube [tube8]: kern area, antipoles vs 720-ray bisection | 7.6e-05 | 5.0e-4 | PASS |
| tube [tube8]: grid error in I_min falls as N_g⁻² (observed 2.000) | 0.0e+00 | 0.0e+0 | PASS |
| angle: ignoring I_yz changes a corner stress by 1.69 P/A (> 1) | 0.0e+00 | 0.0e+0 | PASS |
| rectangle: the "naive" formula is exact when I_yz = 0 (absolute difference) | 6.0e-08 | 1.0e-6 | PASS |
| rectangle: neutral-axis direction obeys Beer Eq. 4.57, tan φ = (I_z/I_y) tan θ | 1.1e-15 | 1.0e-12 | PASS |
| Part C: bending about the weak axis uses I_min = hb³/12 | 1.1e-15 | 1.0e-12 | PASS |
| Part C: C_mid, cosh closed form vs finite differences (N = 2048) | 8.1e-09 | 2.0e-7 | PASS |
| Part C: C at the ends of the free length, closed form vs FD | 5.9e-09 | 2.0e-7 | PASS |
| Part C: mid-length deflection e(1 − C), closed form vs FD | 1.7e-08 | 1.0e-6 | PASS |
| beam-column FD error falls as N⁻² (observed 1.999) | 0.0e+00 | 0.0e+0 | PASS |
| a = 0 limit: C_mid = 1/cosh(kL/2) | 0.0e+00 | 1.0e-14 | PASS |
| a = 0, compression: C_mid = sec(kL/2) (Beer §10.2, secant formula) | 0.0e+00 | 1.0e-14 | PASS |
| a = 0, compression: FD vs secant (N = 2048) | 2.2e-08 | 1.0e-6 | PASS |
| small loads: 1/C − 1 → (π²/8)(P/P_E) (a = 0) | 2.1e-05 | 1.0e-4 | PASS |
| buckling, a = 0: P_cr = π²EI/L² | 0.0e+00 | 1.0e-14 | PASS |
| buckling with end blocks: cos u − (2a/L) u sin u = 0 at the computed load (absolute difference) | 1.1e-16 | 1.0e-12 | PASS |
| end blocks lower the buckling load: P_cr = 0.6996 P_E, between (L/(L + 2a))² and 1 | 0.0e+00 | 0.0e+0 | PASS |
| buckling with end blocks: transcendental root vs FD determinant (N = 1024) | 2.0e-07 | 2.0e-5 | PASS |
| buckling, a = 0: FD determinant (N = 1024) vs π²EI/L² | 7.8e-07 | 2.0e-6 | PASS |
| compression beyond P_cr is flagged as buckled | 0.0e+00 | 0.0e+0 | PASS |
| 5 % threshold, a = 0: cosh u = 1.05 → P = (2u/π)² P_E = 0.0403 P_E | 1.9e-15 | 1.0e-9 | PASS |
| 5 % threshold with blocks: closed form vs FD bisection | 9.7e-09 | 1.0e-5 | PASS |
| 5 % threshold in compression, a = 0: cos u = 1/1.05 | 3.6e-15 | 1.0e-9 | PASS |
| 5 % threshold in compression with blocks: closed form vs FD | 9.3e-09 | 1.0e-4 | PASS |
| Part C: largest σ at mid-length = P/A + P e C (b/2)/I_min | 0.0e+00 | 1.0e-12 | PASS |
| Part C: Eq. 4.58 (C = 1) largest σ | 9.6e-16 | 1.0e-12 | PASS |
| angle, minor axis: C_mid closed form vs FD | 2.7e-09 | 2.0e-6 | PASS |
| angle, major axis: C_mid closed form vs FD | 1.9e-10 | 2.0e-6 | PASS |
| angle: minor-axis bending uses I_min | 0.0e+00 | 1.0e-14 | PASS |
| angle: eccentricity components rebuild \|e\| (u² + v² = y_P² + z_P²) | 0.0e+00 | 1.0e-13 | PASS |
| tube, top: σ = F L_b c/I (tension on top of the cantilever) | 0.0e+00 | 1.0e-13 | PASS |
| tube, top: no transverse shear stress (Q = 0) (absolute difference) | 0.0e+00 | 1.0e-9 | PASS |
| tube: torsional shear Tc/J = F a_L c/(2I) | 0.0e+00 | 1.0e-13 | PASS |
| tube, side: τ_V = V (c₂³ − c₁³)/(3 I t) | 1.4e-16 | 1.0e-13 | PASS |
| tube, side: σ = P/A = 0 with no axial load (absolute difference) | 0.0e+00 | 1.0e-9 | PASS |
| thin-wall limit: τ_V,max → 2V/A | 1.7e-07 | 2.0e-3 | PASS |
| tube at φ = 0.0°: τ, closed form vs polar grid (N = 128) | 5.0e-07 | 2.0e-5 | PASS |
| tube at φ = 0.0°: σ, closed form vs polar grid | 5.0e-07 | 2.0e-5 | PASS |
| tube at φ = 22.9°: τ, closed form vs polar grid (N = 128) | 5.1e-07 | 2.0e-5 | PASS |
| tube at φ = 22.9°: σ, closed form vs polar grid | 5.0e-07 | 2.0e-5 | PASS |
| tube at φ = 90.0°: τ, closed form vs polar grid (N = 128) | 1.3e-06 | 2.0e-5 | PASS |
| tube at φ = 143.2°: τ, closed form vs polar grid (N = 128) | 1.9e-06 | 2.0e-5 | PASS |
| tube at φ = 143.2°: σ, closed form vs polar grid | 5.0e-07 | 2.0e-5 | PASS |
| tube at φ = 229.2°: τ, closed form vs polar grid (N = 128) | 5.1e-06 | 2.0e-5 | PASS |
| tube at φ = 229.2°: σ, closed form vs polar grid | 5.0e-07 | 2.0e-5 | PASS |
| tube: J = 2I, closed form vs polar grid (N = 128) | 5.0e-07 | 2.0e-5 | PASS |
| tube: polar-grid error in J falls as N⁻² (observed 2.000) | 0.0e+00 | 0.0e+0 | PASS |
| preset partA0: finite results | 0.0e+00 | 0.0e+0 | PASS |
| preset partA1: finite results | 0.0e+00 | 0.0e+0 | PASS |
| preset partA2: finite results | 0.0e+00 | 0.0e+0 | PASS |
| preset partB: finite results | 0.0e+00 | 0.0e+0 | PASS |
| preset partC: finite results | 0.0e+00 | 0.0e+0 | PASS |
| preset partAcol: finite results | 0.0e+00 | 0.0e+0 | PASS |
| preset design: finite results | 0.0e+00 | 0.0e+0 | PASS |
| preset zsec: finite results | 0.0e+00 | 0.0e+0 | PASS |
| preset tee: finite results | 0.0e+00 | 0.0e+0 | PASS |
| preset compression: finite results | 0.0e+00 | 0.0e+0 | PASS |
| preset tube8: finite results | 0.0e+00 | 0.0e+0 | PASS |
| preset partB: load point = gusset mid-plane under the horizontal leg (z = −28.58 mm) | 0.0e+00 | 1.0e-12 | PASS |
| preset partB: load point y = −4.76 mm (half the gusset thickness below the leg) | 3.6e-16 | 1.0e-12 | PASS |
| rect [partA2]: A, JavaScript part formulas vs Python Green's theorem / quadrature | 0.0e+00 | 1.0e-11 | PASS |
| rect [partA2]: centroid y (mm) (absolute) | 0.0e+00 | 1.0e-09 | PASS |
| rect [partA2]: centroid z (mm) (absolute) | 0.0e+00 | 1.0e-09 | PASS |
| rect [partA2]: I_z | 0.0e+00 | 1.0e-10 | PASS |
| rect [partA2]: I_y | 1.9e-16 | 1.0e-10 | PASS |
| rect [partA2]: I_yz / I_max (absolute) | 5.2e-18 | 1.0e-10 | PASS |
| rect [partA2]: I_max, Mohr formula (JS) vs eigenvalue (numpy) | 0.0e+00 | 1.0e-10 | PASS |
| rect [partA2]: I_min, Mohr formula (JS) vs eigenvalue (numpy) | 1.3e-15 | 1.0e-10 | PASS |
| rect [partA2]: corner stresses, Eq. 4.58 in principal axes (JS) vs general S⁻¹ form (Python), max \|Δ\|/σ_max (absolute) | 0.0e+00 | 1.0e-10 | PASS |
| rect [partA2]: kern area, antipoles (JS) vs half-plane intersection (scipy) | 1.5e-15 | 1.0e-09 | PASS |
| rect [partA2]: every kern vertex found by both methods (largest distance, mm) (absolute) | 3.0e-15 | 1.0e-09 | PASS |
| angle [partB]: A, JavaScript part formulas vs Python Green's theorem / quadrature | 0.0e+00 | 1.0e-11 | PASS |
| angle [partB]: centroid y (mm) (absolute) | 1.8e-15 | 1.0e-09 | PASS |
| angle [partB]: centroid z (mm) (absolute) | 0.0e+00 | 1.0e-09 | PASS |
| angle [partB]: I_z | 1.8e-16 | 1.0e-10 | PASS |
| angle [partB]: I_y | 0.0e+00 | 1.0e-10 | PASS |
| angle [partB]: I_yz / I_max (absolute) | 5.6e-17 | 1.0e-10 | PASS |
| angle [partB]: I_max, Mohr formula (JS) vs eigenvalue (numpy) | 0.0e+00 | 1.0e-10 | PASS |
| angle [partB]: I_min, Mohr formula (JS) vs eigenvalue (numpy) | 0.0e+00 | 1.0e-10 | PASS |
| angle [partB]: corner stresses, Eq. 4.58 in principal axes (JS) vs general S⁻¹ form (Python), max \|Δ\|/σ_max (absolute) | 4.7e-16 | 1.0e-10 | PASS |
| angle [partB]: kern area, antipoles (JS) vs half-plane intersection (scipy) | 8.5e-16 | 1.0e-09 | PASS |
| angle [partB]: every kern vertex found by both methods (largest distance, mm) (absolute) | 5.5e-15 | 1.0e-09 | PASS |
| angle with fillet [partB]: A, JavaScript part formulas vs Python Green's theorem / quadrature | 0.0e+00 | 1.0e-11 | PASS |
| angle with fillet [partB]: centroid y (mm) (absolute) | 3.6e-15 | 1.0e-09 | PASS |
| angle with fillet [partB]: centroid z (mm) (absolute) | 0.0e+00 | 1.0e-09 | PASS |
| angle with fillet [partB]: I_z | 0.0e+00 | 1.0e-10 | PASS |
| angle with fillet [partB]: I_y | 0.0e+00 | 1.0e-10 | PASS |
| angle with fillet [partB]: I_yz / I_max (absolute) | 1.1e-16 | 1.0e-10 | PASS |
| angle with fillet [partB]: I_max, Mohr formula (JS) vs eigenvalue (numpy) | 1.1e-16 | 1.0e-10 | PASS |
| angle with fillet [partB]: I_min, Mohr formula (JS) vs eigenvalue (numpy) | 4.4e-16 | 1.0e-10 | PASS |
| angle with fillet [partB]: corner stresses, Eq. 4.58 in principal axes (JS) vs general S⁻¹ form (Python), max \|Δ\|/σ_max (absolute) | 3.5e-16 | 1.0e-10 | PASS |
| angle with fillet [partB]: kern area, antipoles (JS) vs half-plane intersection (scipy) | 1.1e-15 | 1.0e-09 | PASS |
| angle with fillet [partB]: every kern vertex found by both methods (largest distance, mm) (absolute) | 1.1e-14 | 1.0e-09 | PASS |
| tee [tee]: A, JavaScript part formulas vs Python Green's theorem / quadrature | 3.8e-16 | 1.0e-11 | PASS |
| tee [tee]: centroid y (mm) (absolute) | 1.4e-14 | 1.0e-09 | PASS |
| tee [tee]: centroid z (mm) (absolute) | 2.0e-15 | 1.0e-09 | PASS |
| tee [tee]: I_z | 2.2e-15 | 1.0e-10 | PASS |
| tee [tee]: I_y | 2.1e-16 | 1.0e-10 | PASS |
| tee [tee]: I_yz / I_max (absolute) | 1.2e-16 | 1.0e-10 | PASS |
| tee [tee]: I_max, Mohr formula (JS) vs eigenvalue (numpy) | 2.2e-15 | 1.0e-10 | PASS |
| tee [tee]: I_min, Mohr formula (JS) vs eigenvalue (numpy) | 2.1e-16 | 1.0e-10 | PASS |
| tee [tee]: corner stresses, Eq. 4.58 in principal axes (JS) vs general S⁻¹ form (Python), max \|Δ\|/σ_max (absolute) | 2.2e-15 | 1.0e-10 | PASS |
| tee [tee]: kern area, antipoles (JS) vs half-plane intersection (scipy) | 2.7e-15 | 1.0e-09 | PASS |
| tee [tee]: every kern vertex found by both methods (largest distance, mm) (absolute) | 1.1e-13 | 1.0e-09 | PASS |
| zsec [zsec]: A, JavaScript part formulas vs Python Green's theorem / quadrature | 0.0e+00 | 1.0e-11 | PASS |
| zsec [zsec]: centroid y (mm) (absolute) | 0.0e+00 | 1.0e-09 | PASS |
| zsec [zsec]: centroid z (mm) (absolute) | 1.9e-15 | 1.0e-09 | PASS |
| zsec [zsec]: I_z | 2.8e-15 | 1.0e-10 | PASS |
| zsec [zsec]: I_y | 2.9e-16 | 1.0e-10 | PASS |
| zsec [zsec]: I_yz / I_max (absolute) | 6.7e-16 | 1.0e-10 | PASS |
| zsec [zsec]: I_max, Mohr formula (JS) vs eigenvalue (numpy) | 1.3e-15 | 1.0e-10 | PASS |
| zsec [zsec]: I_min, Mohr formula (JS) vs eigenvalue (numpy) | 7.1e-15 | 1.0e-10 | PASS |
| zsec [zsec]: corner stresses, Eq. 4.58 in principal axes (JS) vs general S⁻¹ form (Python), max \|Δ\|/σ_max (absolute) | 5.8e-15 | 1.0e-10 | PASS |
| zsec [zsec]: kern area, antipoles (JS) vs half-plane intersection (scipy) | 8.6e-15 | 1.0e-09 | PASS |
| zsec [zsec]: every kern vertex found by both methods (largest distance, mm) (absolute) | 1.2e-13 | 1.0e-09 | PASS |
| angle [design]: A, JavaScript part formulas vs Python Green's theorem / quadrature | 1.4e-16 | 1.0e-11 | PASS |
| angle [design]: centroid y (mm) (absolute) | 1.8e-15 | 1.0e-09 | PASS |
| angle [design]: centroid z (mm) (absolute) | 1.1e-14 | 1.0e-09 | PASS |
| angle [design]: I_z | 1.6e-16 | 1.0e-10 | PASS |
| angle [design]: I_y | 7.0e-16 | 1.0e-10 | PASS |
| angle [design]: I_yz / I_max (absolute) | 2.2e-16 | 1.0e-10 | PASS |
| angle [design]: I_max, Mohr formula (JS) vs eigenvalue (numpy) | 4.1e-16 | 1.0e-10 | PASS |
| angle [design]: I_min, Mohr formula (JS) vs eigenvalue (numpy) | 8.5e-16 | 1.0e-10 | PASS |
| angle [design]: corner stresses, Eq. 4.58 in principal axes (JS) vs general S⁻¹ form (Python), max \|Δ\|/σ_max (absolute) | 1.3e-16 | 1.0e-10 | PASS |
| angle [design]: kern area, antipoles (JS) vs half-plane intersection (scipy) | 1.1e-15 | 1.0e-09 | PASS |
| angle [design]: every kern vertex found by both methods (largest distance, mm) (absolute) | 3.1e-14 | 1.0e-09 | PASS |
| channel [partA2]: A, JavaScript part formulas vs Python Green's theorem / quadrature | 1.4e-16 | 1.0e-11 | PASS |
| channel [partA2]: centroid y (mm) (absolute) | 2.1e-14 | 1.0e-09 | PASS |
| channel [partA2]: centroid z (mm) (absolute) | 7.1e-15 | 1.0e-09 | PASS |
| channel [partA2]: I_z | 2.4e-15 | 1.0e-10 | PASS |
| channel [partA2]: I_y | 2.1e-15 | 1.0e-10 | PASS |
| channel [partA2]: I_yz / I_max (absolute) | 4.1e-16 | 1.0e-10 | PASS |
| channel [partA2]: I_max, Mohr formula (JS) vs eigenvalue (numpy) | 2.4e-15 | 1.0e-10 | PASS |
| channel [partA2]: I_min, Mohr formula (JS) vs eigenvalue (numpy) | 1.9e-15 | 1.0e-10 | PASS |
| channel [partA2]: corner stresses, Eq. 4.58 in principal axes (JS) vs general S⁻¹ form (Python), max \|Δ\|/σ_max (absolute) | 1.6e-15 | 1.0e-10 | PASS |
| channel [partA2]: kern area, antipoles (JS) vs half-plane intersection (scipy) | 4.0e-15 | 1.0e-09 | PASS |
| channel [partA2]: every kern vertex found by both methods (largest distance, mm) (absolute) | 9.1e-14 | 1.0e-09 | PASS |
| tube [tube8]: A, JavaScript part formulas vs Python Green's theorem / quadrature | 0.0e+00 | 1.0e-11 | PASS |
| tube [tube8]: centroid y (mm) (absolute) | 6.9e-16 | 1.0e-09 | PASS |
| tube [tube8]: centroid z (mm) (absolute) | 1.4e-15 | 1.0e-09 | PASS |
| tube [tube8]: I_z | 3.7e-16 | 1.0e-10 | PASS |
| tube [tube8]: I_y | 4.9e-16 | 1.0e-10 | PASS |
| tube [tube8]: I_yz / I_max (absolute) | 3.5e-17 | 1.0e-10 | PASS |
| tube [tube8]: I_max, Mohr formula (JS) vs eigenvalue (numpy) | 3.7e-16 | 1.0e-10 | PASS |
| tube [tube8]: I_min, Mohr formula (JS) vs eigenvalue (numpy) | 4.9e-16 | 1.0e-10 | PASS |
| tube [tube8]: corner stresses, Eq. 4.58 in principal axes (JS) vs general S⁻¹ form (Python), max \|Δ\|/σ_max (absolute) | 4.8e-16 | 1.0e-10 | PASS |
| tube [tube8]: kern area vs π r_k², r_k = (c₂² + c₁²)/(4c₂) (360-gon) | 5.1e-05 | 2.0e-04 | PASS |
| beam-column P = 25 kN, EI = 590 N·m², L = 0.25 m, a = 25 mm: C_mid, JS closed form vs scipy solve_bvp | 9.8e-15 | 1.0e-07 | PASS |
| beam-column P = 25 kN, EI = 590 N·m², L = 0.25 m, a = 25 mm: C at the ends of the free length | 1.1e-15 | 1.0e-07 | PASS |
| beam-column P = 25 kN, EI = 590 N·m², L = 0.25 m, a = 25 mm: buckling load with end blocks, JS bisection vs scipy brentq | 0.0e+00 | 1.0e-09 | PASS |
| beam-column P = -25 kN, EI = 590 N·m², L = 0.25 m, a = 25 mm: C_mid, JS closed form vs scipy solve_bvp | 1.6e-14 | 1.0e-07 | PASS |
| beam-column P = -25 kN, EI = 590 N·m², L = 0.25 m, a = 25 mm: C at the ends of the free length | 4.6e-15 | 1.0e-07 | PASS |
| beam-column P = -25 kN, EI = 590 N·m², L = 0.25 m, a = 25 mm: buckling load with end blocks, JS bisection vs scipy brentq | 0.0e+00 | 1.0e-09 | PASS |
| beam-column P = 30 kN, EI = 9500 N·m², L = 0.25 m, a = 25 mm: C_mid, JS closed form vs scipy solve_bvp | 0.0e+00 | 1.0e-07 | PASS |
| beam-column P = 30 kN, EI = 9500 N·m², L = 0.25 m, a = 25 mm: C at the ends of the free length | 1.1e-16 | 1.0e-07 | PASS |
| beam-column P = 30 kN, EI = 9500 N·m², L = 0.25 m, a = 25 mm: buckling load with end blocks, JS bisection vs scipy brentq | 0.0e+00 | 1.0e-09 | PASS |
| beam-column P = -40 kN, EI = 590 N·m², L = 0.25 m, a = 0 mm: C_mid, JS closed form vs scipy solve_bvp | 6.1e-15 | 1.0e-07 | PASS |
| beam-column P = -40 kN, EI = 590 N·m², L = 0.25 m, a = 0 mm: C at the ends of the free length | 0.0e+00 | 1.0e-07 | PASS |
| beam-column P = -40 kN, EI = 590 N·m², L = 0.25 m, a = 0 mm: buckling load with end blocks, JS bisection vs scipy brentq | 0.0e+00 | 1.0e-09 | PASS |
| beam-column P = 40 kN, EI = 4113 N·m², L = 1.5 m, a = 75 mm: C_mid, JS closed form vs scipy solve_bvp | 1.1e-13 | 1.0e-07 | PASS |
| beam-column P = 40 kN, EI = 4113 N·m², L = 1.5 m, a = 75 mm: C at the ends of the free length | 8.2e-16 | 1.0e-07 | PASS |
| beam-column P = 40 kN, EI = 4113 N·m², L = 1.5 m, a = 75 mm: buckling load with end blocks, JS bisection vs scipy brentq | 4.6e-15 | 1.0e-09 | PASS |
| beam-column P = 5 kN, EI = 590 N·m², L = 0.25 m, a = 100 mm: C_mid, JS closed form vs scipy solve_bvp | 3.0e-15 | 1.0e-07 | PASS |
| beam-column P = 5 kN, EI = 590 N·m², L = 0.25 m, a = 100 mm: C at the ends of the free length | 1.2e-15 | 1.0e-07 | PASS |
| beam-column P = 5 kN, EI = 590 N·m², L = 0.25 m, a = 100 mm: buckling load with end blocks, JS bisection vs scipy brentq | 0.0e+00 | 1.0e-09 | PASS |
| tube: A, JS vs Python quadrature | 0.0e+00 | 1.0e-10 | PASS |
| tube: I, JS vs Python quadrature | 6.2e-16 | 1.0e-10 | PASS |
| tube: J, JS vs Python quadrature | 2.5e-16 | 1.0e-10 | PASS |
| tube at φ = 0.0°: σ_x, JS vs Python | 0.0e+00 | 1.0e-12 | PASS |
| tube at φ = 0.0°: τ = Tc/J + VQ/(It), JS vs Python | 0.0e+00 | 1.0e-12 | PASS |
| tube at φ = 34.4°: Q of the wall from the top, JS closed form vs quadrature | 3.9e-16 | 1.0e-09 | PASS |
| tube at φ = 34.4°: σ_x, JS vs Python | 0.0e+00 | 1.0e-12 | PASS |
| tube at φ = 34.4°: τ = Tc/J + VQ/(It), JS vs Python | 0.0e+00 | 1.0e-12 | PASS |
| tube at φ = 90.0°: Q of the wall from the top, JS closed form vs quadrature | 2.2e-16 | 1.0e-09 | PASS |
| tube at φ = 90.0°: τ = Tc/J + VQ/(It), JS vs Python | 0.0e+00 | 1.0e-12 | PASS |
| tube at φ = 137.5°: Q of the wall from the top, JS closed form vs quadrature | 3.2e-16 | 1.0e-09 | PASS |
| tube at φ = 137.5°: σ_x, JS vs Python | 0.0e+00 | 1.0e-12 | PASS |
| tube at φ = 137.5°: τ = Tc/J + VQ/(It), JS vs Python | 0.0e+00 | 1.0e-12 | PASS |
| tube at φ = 223.5°: Q of the wall from the top, JS closed form vs quadrature | 3.2e-16 | 1.0e-09 | PASS |
| tube at φ = 223.5°: σ_x, JS vs Python | 0.0e+00 | 1.0e-12 | PASS |
| tube at φ = 223.5°: τ = Tc/J + VQ/(It), JS vs Python | 0.0e+00 | 1.0e-12 | PASS |
| D1: largest stress of the reference design, simulation preset (JS) vs analysis (Python) | 2.4e-16 | 1.0e-09 | PASS |
| D1: P/A alone picks L38 × 38 × 4.8, which is overstressed | 0.0e+00 | 0.0e+00 | PASS |

Overall: **PASS**

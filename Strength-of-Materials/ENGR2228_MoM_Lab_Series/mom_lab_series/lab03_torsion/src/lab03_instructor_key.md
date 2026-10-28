# Lab 3 — Instructor Key: Torsion

::: {custom-style="Instructor"}
**For instructors only. Do not distribute to students.** Every number in this key is computed by `src/lab03_analysis.py` (and `src/make_key.py`) from `sample_data.csv` and `src/specimen_measurements.json`, from Lab 1's analysis results, or by the simulation's own model code run in Node. To build a key for your own class data, put your CSV and measurements in the same format and run `python3 src/lab03_analysis.py your.csv your_measurements.json`, then `python3 src/make_key.py`. Uncertainties are expanded ($U = 2u$) unless marked $u$. Sign convention as in the handout (Beer 8e): torque and twist by the right-hand rule, all positive in this test.
:::

## 1. Results at a glance (sample data)

| Quantity | 1018 steel | 6061-T6 aluminum | Gray cast iron | Reference |
|---|---|---|---|---|
| Mean $d$ (mm), $u_d$ | 6.3500, 0.0018 | 6.3520, 0.0018 | 6.3480 | 6.35 nominal |
| $J$ (mm⁴); $4u_d/d$ | 159.62; 0.12 % | 159.82; 0.11 % | — | — |
| $G$ (GPa) | 80.25 ± 0.93 | 26.03 ± 0.23 | secant 40.7 | Eq. 7: 79.46 ± 2.63 / 25.74 ± 0.37 |
| $\tau_Y$ from the Eq. 10 fit (MPa) | 172.1 ± 1.0 | 150.8 ± 1.1 | — | $\sigma_Y/\sqrt{3}$: 171.5 / 158.2 |
| RMS / largest residual of the fit (N·m) | 0.013 / 0.044 | 0.130 / 0.272 | — | — |
| $T$ at 10° on the gage: measured / Eq. 10 (N·m) | 11.51 / 11.512 | 9.99 / 9.736 | — | — |
| Permanent twist after unloading from 5.88° (°) | 3.29 (Eq. 12: 3.285 ± 0.032) | — | — | — |
| $C_m$ (°/N·m); backlash (°) | 0.0358 ± 0.0021; 0.388 ± 0.012 ($u$) | 0.0369 ± 0.0017; 0.392 ± 0.008 ($u$) | — | true 0.0344; 0.40 |
| $T_U$ (N·m) | 27.17 | 14.36 | 11.07 | — |
| $R_T = T_Uc/J$ (MPa) | 540 ± 3 | 285 ± 2 | 220.4 ± 1.3 | cast iron $\sigma_{UT}$ = 214 ± 30 |
| Fully plastic estimate $3T_U/(2\pi c^3)$ (MPa) | 405 | 214 | — | — |
| $\gamma_f$; revolutions over the gage | 1.598; 4.07 | 0.796; 2.03 | 0.00568 | true 1.60; 0.80 |
| Plastic work (J); adiabatic $\Delta T$ (K) | 869; 94 | 257; 44 | — | — |

: Table K1. Results from the sample data.

The sample data were generated from a known "truth" model (`src/generate_sample_data.py`, values in `src/truth.json`): a ring model of each specimen with the material's shear curve, elastic unloading, a +0.3 % load-cell gain error, a −0.2 % troptometer calibration error, the compliance and backlash of the load train, and reading noise. The steel curve is consistent with Lab 1's truth model through the von Mises relation. The closure test in `tests/test_lab03_independent.py` confirms that the analysis recovers the truth values within their stated uncertainty.

## 2. Pre-lab solutions

**P1.** (a) $c$ = 3.175 mm, $c^3$ = 32.01 mm³, $J$ = 159.6 mm⁴, $J/c$ = 50.27 mm³. Steel: $\tau_Y$ = 297/√3 = 171.5 MPa, $G$ = 205/(2 × 1.29) = 79.46 GPa, $T_Y$ = 8.62 N·m, $T_p$ = 11.49 N·m, $\varphi_Y$ = 1.978°. Aluminum: 158.2 MPa, $G$ = 25.74 GPa, $T_Y$ = 7.95 N·m, $T_p$ = 10.60 N·m, $\varphi_Y$ = 5.635°. (b) 0.01° is 0.51 % of $\varphi_Y$ for steel and 0.18 % for aluminum. (c) $(2\pi/3)c^3 \times$ 430 MPa = 28.8 N·m, half the capacity. (d) $T \approx \sigma_{UT}J/c$ = 10.76 N·m. Units: MPa × mm³ = N·mm.

**P2.** (a) Appendix D.3. (b) At $\varphi = \varphi_Y$: $\frac{4}{3}T_Y(1 - \frac{1}{4}) = T_Y$, continuous with the elastic line. As $\varphi \to \infty$: $T \to \frac{4}{3}T_Y$. The slope $dT/d\varphi$ at $\varphi_Y^+$ is $\frac{4}{3}T_Y \cdot \frac{3}{4}\varphi_Y^3/\varphi^4 = T_Y/\varphi_Y$, so the slope is continuous too. (c) $T_p/T_Y = \frac{4}{3}(1 - k^3)/(1 - k^4)$ = 1.2010 for $k$ = 0.6. The material that a tube lacks near the axis is the low-stress material that gains the most when it yields.

**P3.** (a) $T_{max}/T_Y = \frac{4}{3}(1 - \frac{1}{4 \cdot 27})$ = 1.3210. (b) $\varphi_p/\varphi_Y$ = 3 − 1.3210 = 1.6790. (c) Surface: $\tau_Y - T_{max}c/J$ = (1 − 1.3210) $\tau_Y$ = −0.3210 $\tau_Y$. At $\rho_Y = c/3$: (1 − 1.3210/3) $\tau_Y$ = 0.5597 $\tau_Y$. (d) $\int\rho\tau\,dA = T_{max}$ and $\int\rho(T_{max}\rho/J)\,dA = T_{max}$; their difference is zero.

**P4.** (a) $4 \times 0.02/6.35$ = 1.26 % in $J$ and in $G$. (b) $u_d \le$ 0.25 % × 6.35/4 ≈ 4.0 µm: a micrometer, not calipers. (c) The head slope is $L_c/(JG) + C_m$ (Eq. 15): it includes the 25.4 mm of reduced section outside the gage and the load train's compliance. Using it as $L/(JG)$ gives a $G$ that is too low.

**P5.** Simulation, presets as shipped. Steel: $T_Y$ = 8.547 N·m, $T_p$ = 11.396 N·m, $T$(10°) = 11.374 N·m with the material curve and 11.374 N·m with the EPP law (−0.01 %). Aluminum: $T_Y$ = 7.943, $T_p$ = 10.591, $T$(10°) = 9.956 (material) vs 10.133 N·m (EPP), −1.8 %. The law matters for aluminum, whose curve rounds off gradually, and hardly at all for steel at 10°, which is still on its yield plateau. "Overload, then unload" ($\varphi$ = 5.881°): permanent twist 3.291°.

**P6.** (a) The rotating drive head (entanglement): hands clear, motor disabled when adjusting, hair tied back. Overload of the machine: overload stop at 40 N·m, stop at 35 N·m. Fragments from the brittle cast iron: guard closed, stand aside. Credit sharp fracture surfaces (gloves). (b) Beyond about 10° the troptometer's arms would wind into the specimen and be damaged. On cast iron the fracture is sudden and energetic, and a clamped instrument would be thrown or damaged.

## 3. Analysis solutions

**A1.** Steel: 23 points, $k L/J$ gives **$G$ = 80.25 ± 0.93 GPa** (statistical part 0.38 %, intercept 0.003 N·m). Aluminum: 64 points, **26.03 ± 0.23 GPa** (0.10 %, intercept 0.001 N·m). Eq. 7 with Table 1: steel 79.46 ± 2.63, aluminum 25.74 ± 0.37 GPa. Agreement: steel $|\Delta|$ = 0.80 ≤ 2.79 GPa, agree; aluminum 0.29 ≤ 0.44 GPa, agree. For steel the reference dominates ($E$ contributes 1.5 % and $\nu$ 0.8 %); for aluminum the measurement and the reference have similar uncertainty. The diameter term is only 0.12 % with a micrometer; with calipers ($u_d$ ≈ 0.012 mm) it would be 0.75 % and would dominate. *Common error:* using the head rotation, which gives a $G$ about 10 % low for steel even with $L_c$ (A4), and 40 % low with $L$.

**A2.** Steel: 124 points from about $0.5\varphi_Y$ to the start of unloading. **$\tau_Y$ = 172.1 ± 1.0 MPa**, $T_Y$ = 8.651 N·m, $\varphi_Y$ = 1.966°. RMS residual 0.013 N·m and largest 0.044 N·m (0.5 % of $T_Y$): at the noise level. $\sigma_Y/\sqrt{3}$ = 171.5 MPa from Lab 1; ratio 1.003: von Mises holds, and the two agree within $U$. Aluminum: 224 points up to 10°. $\tau_Y$ = 150.8 ± 1.1 MPa, but the RMS residual is 0.130 N·m and the largest 0.272 N·m (3.6 % of $T_Y$), ten times the steel's. The fitted $\tau_Y$ is −7.4 MPa (−4.7 %) below the offset value 158.2 MPa, because a single flat plateau must split the difference between the early rounding and the later hardening. *Interpret:* hot-rolled steel has a yield plateau (Lüders behavior), so the EPP model is physical; aluminum hardens continuously, so its $\tau_Y$ from Eq. 10 depends on the fitting range.

**A3.** Unloading started at 5.88°, 11.42 N·m. **Permanent twist measured 3.29°, predicted 3.285 ± 0.032°** (Eq. 12 with the measured $G$): agree. In units of $\varphi_Y$: 1.671 (ideal EPP from $3\varphi_Y$: 1.6790). The unloading slope differs from the loading slope by 0.24 %: unloading is elastic. Residual stresses (Eq. 12, EPP): elastic-core radius at unloading $\rho_Y$ = 1.061 mm; $\tau_{res}$ = **−55.1 MPa at the surface** and **+96.1 MPa at $\rho_Y$**, linear in between and to zero at the axis. *Check:* $\int\rho\tau_{res}\,dA = 0$ by construction (D.4). *Interpret:* the plastic shell was stretched in shear and cannot return; the elastic core is held twisted by it, so the shaft keeps a permanent twist, with forward shear inside and reverse shear outside. Torsion springs are deliberately overstrained this way (presetting) to raise their elastic range in the working direction.

**A4.** Steel: $C_m$ = 0.0358 ± 0.0021 °/N·m, backlash 0.388 ± 0.012°. Aluminum: 0.0369 ± 0.0017, 0.392 ± 0.008°. In the elastic range the machine is 9.5 % of the head rotation for steel and 3.4 % for aluminum (aluminum's specimen is three times more compliant). Fracture: **steel $\gamma_f$ = 1.598** (4.07 revolutions over the gage; the head turned 6.11 revolutions); **aluminum $\gamma_f$ = 0.796** (2.03 revolutions; head 3.04). *Check:* the corrected head twist joins the troptometer at 10° within the noise. *Interpret:* at fracture the specimen has twisted thousands of degrees, so a few tenths of a degree from the machine are negligible; in the elastic range the machine is a 10 % error for steel.

**A5.** Steel: $T_U$ = 27.17 N·m, **$R_T$ = 540 ± 3 MPa**, fully plastic estimate 405 MPa. Aluminum: $T_U$ = 14.36 N·m, **$R_T$ = 285 ± 2 MPa**, 214 MPa. The true surface stress at fracture lies between them: Nadai (C1) gives about 426 MPa for steel at $\gamma$ = 1.5, so $R_T$ is 27 % high. Cast iron: $T_f$ = 11.07 N·m, **$R_T$ = 220.4 ± 1.3 MPa** vs. $\sigma_{UT}$ = 214 MPa: $|\Delta|$ = 6.4 ≤ 30.0 MPa, agree. The cast iron's 45° helix is the plane normal to $\sigma = +\tau$ (Eq. 14): it failed in tension. The metals failed in shear on the transverse plane, the plane of maximum shear. *Check:* $R_T/(3T_U/2\pi c^3) = 4/3$ identically, since both are $T_U$ times a geometric factor. For the cast iron, which stays nearly elastic, only $R_T$ is meaningful (secant modulus at fracture 38.8 GPa vs 40.7 at low torque: mildly nonlinear, which makes $R_T$ slightly exceed the true surface stress).

**A6.** Use Table K1. Expected verdicts: $G$ agrees for both metals; steel $\tau_Y$ agrees with $\sigma_Y/\sqrt{3}$; aluminum $\tau_Y$ from the EPP fit sits about 5 % below the offset value (a model-form discrepancy, A2 and M1); $T$ at 10° agrees with Eq. 10 for steel and exceeds it by 2.61 % for aluminum; the permanent twist agrees; the cast iron $R_T$ agrees with $\sigma_{UT}$. Full credit needs each discrepancy above $U$ explained with a named, quantified cause.

**M1.** (a) The aluminum residuals are at the noise level in the elastic range, negative through the transition around $\varphi_Y$ (the material rounds off before a sharp yield would), with the largest, 3.6 % of $T_Y$, near 5–6°, and positive beyond about 8° (hardening), reaching 2.61 % at 10°. In the simulation at 10°: material curve 9.956 N·m vs EPP 10.133 N·m (−1.7 %, with the offset $\tau_Y$). (b) At 120° ($\gamma_c$ = 0.131): $Tc/J$ = 322 MPa vs. the actual surface stress 260 MPa, 24 % high. For the steel at fracture, $R_T$ is 27 % above Nadai's stress: same cause, a stress profile flatter than linear. (c) Square 10 mm × 10 mm, 50 N·m: exact $\tau_{max}$ = $T/(c_1a^3)$ with $c_1$ = 0.2082: 240.2 MPa at the middle of each side. The circular formula with the polar moment and the half diagonal gives 212.1 MPa (−11.7 %) and places it at the corners, where the stress is actually zero. A circle looks the same after any rotation about its axis, so its sections have no reason to warp. A square's corners would have to carry shear across a free surface, so its sections warp to relieve them.

## 4. Challenge and Extension solutions

**C1.** Derivation in Appendix D.6 of the handout. Steel, from the corrected head rotation (local quadratic fit of $\ln T$ against $\ln\gamma_c$ over ±0.25 in $\ln\gamma$): γ = 0.1: Nadai 247 MPa (fully plastic estimate 228, elastic formula 304); Lab 1 Hollomon converted 243 MPa; γ = 0.5: Nadai 344 MPa (fully plastic estimate 323, elastic formula 431); Lab 1 Hollomon converted 352 MPa; γ = 1.0: Nadai 394 MPa (fully plastic estimate 370, elastic formula 493); Lab 1 Hollomon converted 413 MPa; γ = 1.5: Nadai 426 MPa (fully plastic estimate 400, elastic formula 534); Lab 1 Hollomon converted 453 MPa. Lab 1's Hollomon fit ($K$ = 811 MPa, $n$ = 0.230, fitted below necking, $\varepsilon_t \le$ 0.17) matches to within 3 % up to $\gamma$ ≈ 0.5 ($\varepsilon_t$ ≈ 0.29), then overshoots by 5–6 %: extrapolating a power law far beyond its fitting range is unsafe. Lab 1's neck at fracture gives $\sigma_t/\sqrt{3}$ = 429 MPa at $\gamma$ = 1.59, consistent with Nadai's 426 MPa at 1.5. Aluminum: 193 MPa at 0.1 and 212 MPa at 0.5. Torsion reaches strains that a tension test can only reach inside a neck.

**C2.** $T_p/T_Y = \frac{4}{3}(1 - k^3)/(1 - k^4)$: 4/3 for $k$ = 0, 1.2010 for 0.6 and 1.0507 for 0.9. The "Hollow shaft" preset ($k$ = 0.6) gives 1.2010. A thin tube is already nearly uniformly stressed when its outer fiber yields, so there is little left to gain.

**C3.** FD for $a/b$ = 2: N = 8: 0.22223, N = 16: 0.22705, N = 32: 0.22827. Successive differences shrink by 3.93 (4 for second order). Richardson: 0.22868 vs series 0.22868. Membrane: the film's slope is the stress, and it is steepest where the boundary is closest to the center (mid-side) and flat in a corner, where two fixed edges meet.

**X1.** Equilibrium of a wall element between two longitudinal cuts gives $q = \tau t$ constant; its moment is $2A_mq = T$; energy gives the twist (Appendix D.8). Exactly, $\tau_{Bredt}/\tau_{max} = (1 + x^2/4)/(1 + x/2)$ with $x = t/r_m$, i.e. $1 - x/2$ to first order. For $t/r_m$ = 0.5: first order −25 %, exact −15.0 % (simulation: 19.9 vs 23.4 MPa).

**X2.** Same twist rate in both parts. $J_{core}$ = 15 708 mm⁴, $J_{sleeve}$ = 63 814 mm⁴; the core carries $J_sG_s/(J_sG_s + J_aG_a)$ = 0.4315 of the torque. First yield of the core at $\theta = \tau_{Y,s}/(G_s \cdot 10\ \text{mm})$ = 0.2144 rad/m; of the sleeve at $\tau_{Y,a}/(G_a \cdot 15\ \text{mm})$ = 0.3861 rad/m. So **the steel core yields first**, at $T$ = 626 N·m. Students should note that the higher-strength part yields first because it is three times stiffer.

**X3.** Plastic work into the reduced section ($V$ ≈ 2 413 mm³): steel 869 J, aluminum 257 J. If adiabatic, the temperature would rise by 94 K (steel) and 44 K (aluminum). The tests took 246 s and 135 s; a 6 mm bar loses heat to the grips and air on a time scale of tens of seconds, so the real rise is a fraction of this, but the specimen is noticeably warm. A ten-times-faster test would be nearly adiabatic, and the softening would lower the measured hardening.

## 5. Design problem D1: reference solution

**D1.** $T = P/\omega$ = 15 000/(2π × 1200/60) = **119.4 N·m**. Allowable stress at the fillet: steel $(\tau_Y - U)/(2.0 \times 1.6)$ = 171.0/3.2 = 53.4 MPa; aluminum 149.7/3.2 = 46.8 MPa. Required outer diameter $d$ (mm) and resulting design:

| Option | $d$ for strength | $d$ for twist | Chosen $d$ × $d_i$ | Mass (kg) | Cost (\$) | $K\tau_{max}$ (MPa) | $\varphi$ (°) |
|---|---:|---:|---|---:|---:|---:|---:|
| Steel, solid | 22.5 | 33.8 | 34 | 10.72 | 23.58 | 24.7 | 0.974 |
| Steel, $d_i/d$ = 0.6 | 23.6 | 35.0 | 35 × 21.0 | 7.27 | 15.99 | 26.1 | 0.997 |
| Steel, $d_i/d$ = 0.8 | 26.8 | 38.5 | 39 × 31.2 | 5.08 | 11.17 | 27.8 | 0.953 |
| Aluminum, solid | 23.5 | 44.8 | 45 | 6.44 | 41.87 | 10.7 | 0.979 |
| Aluminum, $d_i/d$ = 0.6 | 24.6 | 46.3 | 47 × 28.2 | 4.50 | 29.23 | 10.8 | 0.945 |
| Aluminum, $d_i/d$ = 0.8 | 28.0 | 51.1 | 52 × 41.6 | 3.10 | 20.13 | 11.7 | 0.930 |

: Table K2. Reference designs (twist governs every option).

The twist limit governs every option by a wide margin. The strength requirement alone would allow shafts 30–50 % smaller in diameter, so the stresses in the final designs are far below the allowable. That is the main lesson: students who size for strength first and "check" twist afterwards usually fail the check. Cheapest: the steel tube with $d_i/d$ = 0.8. Lightest: the aluminum tube with $d_i/d$ = 0.8 (about 60 % of the steel tube's mass, at about twice the cost). Either is acceptable if justified. *Assumptions that could invalidate a design:* the 1.6 concentration factor at the fillet (check the actual $r/d$ and $D/d$ against §3.5); a thin tube's local buckling (check $d/t$; at 0.8 it is 10, which is safe here); the coupling and bearing stiffness, which adds twist (check the drive's allowable windup).

**Rubric detail (15 points total in the report).** Torque from power (3). Strength basis (3.75): $\tau_Y - U$ from the student's data, $K$ at the fillet. Every requirement checked, governing one named (3). Trade-off between at least two options with numbers (3.75). Presentation and assumption (1.5). Typical partial credit: power in hp or rpm not converted to rad/s (−2); $K$ omitted (−2); twist not checked (−4, because it governs); handbook $G$ (−1).

## 6. Expected ranges for real class data

| Quantity | Steel (1018 HR) | Aluminum (6061-T6) | If outside, suspect |
|---|---|---|---|
| $G$ from the troptometer (GPa) | 77–82 | 25–27 | troptometer seating, wrong $L$, diameter error |
| $G$ from the head rotation (GPa) | 65–75 | 23–26 | not a fault: compliance (A4) |
| $\tau_Y$ from Eq. 10 (MPa) | 150–200 | 135–165 | fitting range |
| $T_U$ (N·m), $d$ = 6.35 mm | 22–30 | 13–16 | — |
| $\gamma_f$ | 1.0–2.5 | 0.4–1.0 | fracture at a fillet (retest) |
| Cast iron $R_T$ (MPa) | — | — | 180–300 (class 25–35) |

: Table K3. Expected data ranges.

## 7. Common student mistakes

1. Computing $G$ from the head rotation, or from the head rotation divided by $L$ instead of $L_c$.
2. Using degrees in $\varphi = TL/(JG)$, or $\pi d^4/64$ (the second moment $I$) for $J$.
3. Using calipers for $d$ and not noticing that the $d^4$ term then dominates $u_G$.
4. Fitting $\tau_Y$ to the unloading or reloading segment of the steel data.
5. Reporting $R_T$ as the shear strength of a ductile metal.
6. Taking the permanent twist as $\varphi_{max} - \varphi_Y$ instead of $\varphi_{max} - T_{max}L/(JG)$.
7. Saying the cast iron "failed in shear because it was in torsion".
8. Converting tension to shear with $\tau = \sigma/2$ (Tresca) without saying so; the handout uses von Mises ($\sigma/\sqrt{3}$). Either is acceptable if stated, and the 15 % difference should be noted.
9. In D1, sizing for strength and forgetting the twist limit, or applying $K$ to the twist.
10. Using the elastic formulas past yield in M1 without saying why they fail.

## 8. Grading rubric

| Part | Points | Full credit | Common deductions |
|---|---:|---|---|
| Pre-lab | 15 | P1–P6 correct with units; P1 an estimate made before measuring | P2 limits missing (−1); P4(c) wrong (−2) |
| Data & procedure | 10 | Tables 3–4 complete; checks in steps 1, 2 and 4 recorded | diameters with calipers (−2) |
| A1 | 9 | $G$ for both with budgets; Eq. 7 prediction with $U$; agreement | head rotation used (−4) |
| A2 | 9 | fits, residuals, comparison with $\sigma_Y/\sqrt3$, why aluminum misfits | no residual analysis (−3) |
| A3 | 8 | permanent twist vs Eq. 12 with $U$; unloading slope; residual distribution | residual stresses not plotted (−2) |
| A4 | 6 | $C_m$, backlash, correction, $\gamma_f$ | no join check (−1) |
| A5 | 8 | $R_T$, plastic estimate, bracket, cast iron comparison, fracture explanation | $R_T$ called the shear strength (−2) |
| A6 | 5 | complete table, normalized figure, every discrepancy explained | unexplained discrepancy (−1 each) |
| M1 | 10 | (a) residual pattern, (b) overstatement, (c) square with warping explanation | no simulation numbers (−2 each) |
| D1 | 15 | see Sec. 5 | see Sec. 5 |
| Communication | 5 | labeled axes, units, $x \pm U$ format | each unlabeled axis (−1) |
| Challenge | +10 | C1 (4), C2 (3), C3 (3) | — |

: Table K4. Grading rubric (100 points plus up to 10 Challenge points). Core analysis A1–A6 totals 45.

Every Core answer must include the required check and interpretation; deduct 1 point per question where either is missing.

## 9. Instructor notes

**Before the lab.** Specimens: 6.35 mm reduced section 76.2 mm long with generous fillets ($r \ge$ 3 mm) and 12.7 mm hexagonal ends, ground to ±0.01 mm; one each of 1018 HR (from the same bar as Lab 1, if possible), 6061-T6, and class 30 gray cast iron. Check the troptometer's gage-length setting bar and that its collars clamp without marking the specimen. Set the machine's overload stop at 40 N·m. Fit a polycarbonate guard for the cast iron test.

**Timing (2 h).** 0:00–0:10 safety and pre-lab collection; 0:10–0:20 diameters; 0:20–0:55 steel, including the unloading cycle; 0:55–1:20 aluminum; 1:20–1:35 cast iron; 1:35–1:45 fracture surfaces side by side; 1:45–2:00 simulation (step 11). The steel's fast phase lasts about 2.5 minutes at 15°/s.

**Safety.** Demonstrate troptometer removal with the motor disabled. The steel absorbs nearly 1 kJ of plastic work and is warm after the test (X3). Do not let students hold the specimen to "feel the twist".

**Running without equipment.** Give students `sample_data.csv` and Appendix A of the handout; everything in this key applies unchanged. A good hybrid is to break one cast iron specimen live, which takes 40 s and shows the helix, and to use the sample data for the analysis.

**Your own class data.** Export the columns specimen, time_s, torque_Nm, troptometer_deg and head_deg; fill a measurements JSON like `src/specimen_measurements.json`, with each team's Lab 1 and Lab 2 values in `reference`; run `src/lab03_analysis.py` and `src/make_key.py`.

**The simulation.** Students use it in P5, step 11, A6, M1, C2, C3 and X1. Its readout separates verification rows (closed form vs. ring integration or finite differences, "agree") from model-comparison rows ("different models"); the tests are in `tests/` and summarized in `tests/VERIFICATION.md`.

## 10. Self-critique and revisions

Before release, the lab was reviewed as a demanding instructor at a top program would review it. The three biggest weaknesses found, and the fixes made:

1. **$G$ was going to be taken from the machine's head rotation,** as many torsion labs do. The load train's compliance makes that about 10 % low for steel (9.5 % of the elastic head rotation is the machine), which would have produced a "discrepancy" blamed on the material. *Fix:* the troptometer measures $\varphi$ over a known gage length. Eq. 15 and A4 make students measure the machine's compliance and use it only where it is harmless (at fracture). P4(c) asks why the head slope cannot give $G$.
2. **The elastic–perfectly plastic model was presented as "the" theory,** with no way for students to see the material's real shear curve, and the modulus of rupture was easy to mistake for a stress. *Fix:* Eq. 18 (Nadai) recovers $\tau(\gamma)$ from the data (C1, cross-checked against Lab 1). A5 brackets the true stress between $R_T$ and the fully plastic estimate. M1 quantifies the EPP misfit for aluminum and the overstatement of $Tc/J$.
3. **No test of the unloading theory (§3.8).** Residual stress was purely a derivation. *Fix:* the steel is unloaded from about $3\varphi_Y$ and reloaded (procedure step 5). A3 compares the measured permanent twist with Eq. 12 (agreement to 3.29° vs 3.285 ± 0.032°) and checks that unloading is elastic.

**Known limitations (not fixed).** The steel model has no upper yield point or Lüders band, which in a real hot-rolled bar can give a small torque drop near $T_Y$. End effects at the fillets and grips are ignored, which is acceptable because the troptometer reads the middle 50.8 mm. The sample data assume isothermal behavior although X3 shows the steel can heat significantly. The cast iron is modeled with a smooth softening law; real gray iron is also weaker in tension than in compression, which torsion does not test.

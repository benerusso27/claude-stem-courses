# Lab 3 — Instructor Key: Torsion

::: {custom-style="Instructor"}
**For instructors only. Do not distribute to students.** Every number in this key is computed by `src/lab03_analysis.py` (and `src/make_key.py`) from `sample_data.csv` and `src/specimen_measurements.json`, from Lab 1's analysis results, or by the simulation's own model code run in Node. To build a key for your own class data, put your CSV and measurements in the same format and run `python3 src/lab03_analysis.py your.csv your_measurements.json`, then `python3 src/make_key.py`. Uncertainties are expanded ($U = 2u$) unless marked $u$. Sign convention as in the handout (Beer 8e): torque and twist by the right-hand rule, all positive in this test.
:::

## 1. Results at a glance (sample data)

| Quantity | 1018 steel | 6061-T6 aluminum | Gray cast iron | Reference |
|---|---|---|---|---|
| Mean $d$ (mm), $u_d$ | «d_s», «ud_s» | «d_a», «ud_a» | «d_ci» | 6.35 nominal |
| $J$ (mm⁴); $4u_d/d$ | «J_s»; «uJ_s» % | «J_a»; «uJ_a» % | — | — |
| $G$ (GPa) | «G_s» | «G_a» | secant «Gsl_ci» | Eq. 7: «Gp_s» / «Gp_a» |
| $\tau_Y$ from the Eq. 10 fit (MPa) | «tY_s» | «tY_a» | — | $\sigma_Y/\sqrt{3}$: «tYten_s» / «tYten_a» |
| RMS / largest residual of the fit (N·m) | «rms_s» / «maxdev_s» | «rms_a» / «maxdev_a» | — | — |
| $T$ at 10° on the gage: measured / Eq. 10 (N·m) | «T10_s» / «T10epp_s» | «T10_a» / «T10epp_a» | — | — |
| Permanent twist after unloading from «phiA»° (°) | «phires_m» (Eq. 12: «phires_p») | — | — | — |
| $C_m$ (°/N·m); backlash (°) | «Cm_s»; «toe_s» ($u$) | «Cm_a»; «toe_a» ($u$) | — | true 0.0344; 0.40 |
| $T_U$ (N·m) | «TU_s» | «TU_a» | «Tf_ci» | — |
| $R_T = T_Uc/J$ (MPa) | «RT_s» | «RT_a» | «RT_ci» | cast iron $\sigma_{UT}$ = 214 ± 30 |
| Fully plastic estimate $3T_U/(2\pi c^3)$ (MPa) | «tpl_s» | «tpl_a» | — | — |
| $\gamma_f$; revolutions over the gage | «gf_s»; «rev_s» | «gf_a»; «rev_a» | «gf_ci» | true 1.60; 0.80 |
| Plastic work (J); adiabatic $\Delta T$ (K) | «W_s»; «dT_s» | «W_a»; «dT_a» | — | — |

: Table K1. Results from the sample data.

The sample data were generated from a known "truth" model (`src/generate_sample_data.py`, values in `src/truth.json`): a ring model of each specimen with the material's shear curve, elastic unloading, a +0.3 % load-cell gain error, a −0.2 % troptometer calibration error, the compliance and backlash of the load train, and reading noise. The steel curve is consistent with Lab 1's truth model through the von Mises relation. The closure test in `tests/test_lab03_independent.py` confirms that the analysis recovers the truth values within their stated uncertainty.

## 2. Pre-lab solutions

**P1.** (a) $c$ = 3.175 mm, $c^3$ = «P1_c3» mm³, $J$ = «P1_J» mm⁴, $J/c$ = «P1_Jc» mm³. Steel: $\tau_Y$ = 297/√3 = «P1_tY_s» MPa, $G$ = 205/(2 × 1.29) = «P1_G_s» GPa, $T_Y$ = «P1_TY_s» N·m, $T_p$ = «P1_Tp_s» N·m, $\varphi_Y$ = «P1_phiY_s»°. Aluminum: «P1_tY_a» MPa, $G$ = «P1_G_a» GPa, $T_Y$ = «P1_TY_a» N·m, $T_p$ = «P1_Tp_a» N·m, $\varphi_Y$ = «P1_phiY_a»°. (b) 0.01° is «P1_res_s» % of $\varphi_Y$ for steel and «P1_res_a» % for aluminum. (c) $(2\pi/3)c^3 \times$ 430 MPa = «P1_Tmax» N·m, half the capacity. (d) $T \approx \sigma_{UT}J/c$ = «P1_Tci» N·m. Units: MPa × mm³ = N·mm.

**P2.** (a) Appendix D.3. (b) At $\varphi = \varphi_Y$: $\frac{4}{3}T_Y(1 - \frac{1}{4}) = T_Y$, continuous with the elastic line. As $\varphi \to \infty$: $T \to \frac{4}{3}T_Y$. The slope $dT/d\varphi$ at $\varphi_Y^+$ is $\frac{4}{3}T_Y \cdot \frac{3}{4}\varphi_Y^3/\varphi^4 = T_Y/\varphi_Y$, so the slope is continuous too. (c) $T_p/T_Y = \frac{4}{3}(1 - k^3)/(1 - k^4)$ = «P2_hollow» for $k$ = 0.6. The material that a tube lacks near the axis is the low-stress material that gains the most when it yields.

**P3.** (a) $T_{max}/T_Y = \frac{4}{3}(1 - \frac{1}{4 \cdot 27})$ = «P3_Tm». (b) $\varphi_p/\varphi_Y$ = 3 − «P3_Tm» = «P3_phip». (c) Surface: $\tau_Y - T_{max}c/J$ = (1 − «P3_Tm») $\tau_Y$ = «P3_res_c» $\tau_Y$. At $\rho_Y = c/3$: (1 − «P3_Tm»/3) $\tau_Y$ = «P3_res_rY» $\tau_Y$. (d) $\int\rho\tau\,dA = T_{max}$ and $\int\rho(T_{max}\rho/J)\,dA = T_{max}$; their difference is zero.

**P4.** (a) $4 \times 0.02/6.35$ = «P4_pct» % in $J$ and in $G$. (b) $u_d \le$ 0.25 % × 6.35/4 ≈ «P4_ud» µm: a micrometer, not calipers. (c) The head slope is $L_c/(JG) + C_m$ (Eq. 15): it includes the 25.4 mm of reduced section outside the gage and the load train's compliance. Using it as $L/(JG)$ gives a $G$ that is too low.

**P5.** Simulation, presets as shipped. Steel: $T_Y$ = «sim_TY_s» N·m, $T_p$ = «sim_Tp_s» N·m, $T$(10°) = «sim_Tmat_s» N·m with the material curve and «sim_Tepp_s» N·m with the EPP law («sim_st_diff» %). Aluminum: $T_Y$ = «sim_TY_a», $T_p$ = «sim_Tp_a», $T$(10°) = «sim_Tmat_a» (material) vs «sim_Tepp_a» N·m (EPP), «sim_al_diff» %. The law matters for aluminum, whose curve rounds off gradually, and hardly at all for steel at 10°, which is still on its yield plateau. "Overload, then unload" ($\varphi$ = «sim_phiA»°): permanent twist «sim_phiP»°.

**P6.** (a) The rotating drive head (entanglement): hands clear, motor disabled when adjusting, hair tied back. Overload of the machine: overload stop at 40 N·m, stop at 35 N·m. Fragments from the brittle cast iron: guard closed, stand aside. Credit sharp fracture surfaces (gloves). (b) Beyond about 10° the troptometer's arms would wind into the specimen and be damaged. On cast iron the fracture is sudden and energetic, and a clamped instrument would be thrown or damaged.

## 3. Analysis solutions

**A1.** Steel: «nG_s» points, $k L/J$ gives **$G$ = «G_s» GPa** (statistical part «Gst_s» %, intercept «Gint_s» N·m). Aluminum: «nG_a» points, **«G_a» GPa** («Gst_a» %, intercept «Gint_a» N·m). Eq. 7 with Table 1: steel «Gp_s», aluminum «Gp_a» GPa. Agreement: steel $|\Delta|$ = «Gd_s» ≤ «Glim_s» GPa, «Gagree_s»; aluminum «Gd_a» ≤ «Glim_a» GPa, «Gagree_a». For steel the reference dominates ($E$ contributes 1.5 % and $\nu$ 0.8 %); for aluminum the measurement and the reference have similar uncertainty. The diameter term is only «uJ_s» % with a micrometer; with calipers ($u_d$ ≈ 0.012 mm) it would be 0.75 % and would dominate. *Common error:* using the head rotation, which gives a $G$ about 10 % low for steel even with $L_c$ (A4), and 40 % low with $L$.

**A2.** Steel: «nfit_s» points from about $0.5\varphi_Y$ to the start of unloading. **$\tau_Y$ = «tY_s» MPa**, $T_Y$ = «TY_s» N·m, $\varphi_Y$ = «phiY_s»°. RMS residual «rms_s» N·m and largest «maxdev_s» N·m («maxdevrel_s» % of $T_Y$): at the noise level. $\sigma_Y/\sqrt{3}$ = «tYten_s» MPa from Lab 1; ratio «tYten_ratio_s»: von Mises holds, and the two agree within $U$. Aluminum: «nfit_a» points up to 10°. $\tau_Y$ = «tY_a» MPa, but the RMS residual is «rms_a» N·m and the largest «maxdev_a» N·m («maxdevrel_a» % of $T_Y$), ten times the steel's. The fitted $\tau_Y$ is «tYd_a» MPa («tYd_a_pct» %) below the offset value «tYten_a» MPa, because a single flat plateau must split the difference between the early rounding and the later hardening. *Interpret:* hot-rolled steel has a yield plateau (Lüders behavior), so the EPP model is physical; aluminum hardens continuously, so its $\tau_Y$ from Eq. 10 depends on the fitting range.

**A3.** Unloading started at «phiA»°, «TA» N·m. **Permanent twist measured «phires_m»°, predicted «phires_p»°** (Eq. 12 with the measured $G$): agree. In units of $\varphi_Y$: «phires_ratio» (ideal EPP from $3\varphi_Y$: «P3_phip»). The unloading slope differs from the loading slope by «unl_slope» %: unloading is elastic. Residual stresses (Eq. 12, EPP): elastic-core radius at unloading $\rho_Y$ = «rY_A» mm; $\tau_{res}$ = **«res_c» MPa at the surface** and **+«res_rY» MPa at $\rho_Y$**, linear in between and to zero at the axis. *Check:* $\int\rho\tau_{res}\,dA = 0$ by construction (D.4). *Interpret:* the plastic shell was stretched in shear and cannot return; the elastic core is held twisted by it, so the shaft keeps a permanent twist, with forward shear inside and reverse shear outside. Torsion springs are deliberately overstrained this way (presetting) to raise their elastic range in the working direction.

**A4.** Steel: $C_m$ = «Cm_s» °/N·m, backlash «toe_s»°. Aluminum: «Cm_a», «toe_a»°. In the elastic range the machine is «hfrac_s» % of the head rotation for steel and «hfrac_a» % for aluminum (aluminum's specimen is three times more compliant). Fracture: **steel $\gamma_f$ = «gf_s»** («rev_s» revolutions over the gage; the head turned «hrev_s» revolutions); **aluminum $\gamma_f$ = «gf_a»** («rev_a» revolutions; head «hrev_a»). *Check:* the corrected head twist joins the troptometer at 10° within the noise. *Interpret:* at fracture the specimen has twisted thousands of degrees, so a few tenths of a degree from the machine are negligible; in the elastic range the machine is a 10 % error for steel.

**A5.** Steel: $T_U$ = «TU_s» N·m, **$R_T$ = «RT_s» MPa**, fully plastic estimate «tpl_s» MPa. Aluminum: $T_U$ = «TU_a» N·m, **$R_T$ = «RT_a» MPa**, «tpl_a» MPa. The true surface stress at fracture lies between them: Nadai (C1) gives about «nad15» MPa for steel at $\gamma$ = 1.5, so $R_T$ is «RT_over_nad» % high. Cast iron: $T_f$ = «Tf_ci» N·m, **$R_T$ = «RT_ci» MPa** vs. $\sigma_{UT}$ = 214 MPa: $|\Delta|$ = «RTd_ci» ≤ «RTlim_ci» MPa, agree. The cast iron's 45° helix is the plane normal to $\sigma = +\tau$ (Eq. 14): it failed in tension. The metals failed in shear on the transverse plane, the plane of maximum shear. *Check:* $R_T/(3T_U/2\pi c^3) = 4/3$ identically, since both are $T_U$ times a geometric factor. For the cast iron, which stays nearly elastic, only $R_T$ is meaningful (secant modulus at fracture «Gsf_ci» GPa vs «Gsl_ci» at low torque: mildly nonlinear, which makes $R_T$ slightly exceed the true surface stress).

**A6.** Use Table K1. Expected verdicts: $G$ agrees for both metals; steel $\tau_Y$ agrees with $\sigma_Y/\sqrt{3}$; aluminum $\tau_Y$ from the EPP fit sits about 5 % below the offset value (a model-form discrepancy, A2 and M1); $T$ at 10° agrees with Eq. 10 for steel and exceeds it by «T10ex_a» % for aluminum; the permanent twist agrees; the cast iron $R_T$ agrees with $\sigma_{UT}$. Full credit needs each discrepancy above $U$ explained with a named, quantified cause.

**M1.** (a) The aluminum residuals are at the noise level in the elastic range, negative through the transition around $\varphi_Y$ (the material rounds off before a sharp yield would), with the largest, «maxdevrel_a» % of $T_Y$, near 5–6°, and positive beyond about 8° (hardening), reaching «T10ex_a» % at 10°. In the simulation at 10°: material curve «M1_al_mat» N·m vs EPP «M1_al_epp» N·m («M1_al_pct» %, with the offset $\tau_Y$). (b) At 120° ($\gamma_c$ = «M1_g»): $Tc/J$ = «M1_el» MPa vs. the actual surface stress «M1_surf» MPa, «M1_pct» % high. For the steel at fracture, $R_T$ is «RT_over_nad» % above Nadai's stress: same cause, a stress profile flatter than linear. (c) Square 10 mm × 10 mm, 50 N·m: exact $\tau_{max}$ = $T/(c_1a^3)$ with $c_1$ = «sq_c1»: «sq_tau» MPa at the middle of each side. The circular formula with the polar moment and the half diagonal gives «sq_mis» MPa («sq_pct» %) and places it at the corners, where the stress is actually zero. A circle looks the same after any rotation about its axis, so its sections have no reason to warp. A square's corners would have to carry shear across a free surface, so its sections warp to relieve them.

## 4. Challenge and Extension solutions

**C1.** Derivation in Appendix D.6 of the handout. Steel, from the corrected head rotation (local quadratic fit of $\ln T$ against $\ln\gamma_c$ over ±0.25 in $\ln\gamma$): «nadai_rows». Lab 1's Hollomon fit ($K$ = «L1_K» MPa, $n$ = «L1_n», fitted below necking, $\varepsilon_t \le$ 0.17) matches to within 3 % up to $\gamma$ ≈ 0.5 ($\varepsilon_t$ ≈ 0.29), then overshoots by 5–6 %: extrapolating a power law far beyond its fitting range is unsafe. Lab 1's neck at fracture gives $\sigma_t/\sqrt{3}$ = «L1_neck_tau» MPa at $\gamma$ = «L1_neck_g», consistent with Nadai's «nad15» MPa at 1.5. Aluminum: «nad01_a» MPa at 0.1 and «nad05_a» MPa at 0.5. Torsion reaches strains that a tension test can only reach inside a neck.

**C2.** $T_p/T_Y = \frac{4}{3}(1 - k^3)/(1 - k^4)$: 4/3 for $k$ = 0, «C2_06» for 0.6 and «C2_09» for 0.9. The "Hollow shaft" preset ($k$ = 0.6) gives «C2_sim». A thin tube is already nearly uniformly stressed when its outer fiber yields, so there is little left to gain.

**C3.** FD for $a/b$ = 2: «C3_rows». Successive differences shrink by «C3_ratio» (4 for second order). Richardson: «C3_rich» vs series «C3_series». Membrane: the film's slope is the stress, and it is steepest where the boundary is closest to the center (mid-side) and flat in a corner, where two fixed edges meet.

**X1.** Equilibrium of a wall element between two longitudinal cuts gives $q = \tau t$ constant; its moment is $2A_mq = T$; energy gives the twist (Appendix D.8). Exactly, $\tau_{Bredt}/\tau_{max} = (1 + x^2/4)/(1 + x/2)$ with $x = t/r_m$, i.e. $1 - x/2$ to first order. For $t/r_m$ = 0.5: first order «X1_lead» %, exact «X1_pct» % (simulation: «X1_bt» vs «X1_et» MPa).

**X2.** Same twist rate in both parts. $J_{core}$ = «X2_Js» mm⁴, $J_{sleeve}$ = «X2_Ja» mm⁴; the core carries $J_sG_s/(J_sG_s + J_aG_a)$ = «X2_share» of the torque. First yield of the core at $\theta = \tau_{Y,s}/(G_s \cdot 10\ \text{mm})$ = «X2_ths» rad/m; of the sleeve at $\tau_{Y,a}/(G_a \cdot 15\ \text{mm})$ = «X2_tha» rad/m. So **«X2_first» yields first**, at $T$ = «X2_T» N·m. Students should note that the higher-strength part yields first because it is three times stiffer.

**X3.** Plastic work into the reduced section ($V$ ≈ «V_s» mm³): steel «W_s» J, aluminum «W_a» J. If adiabatic, the temperature would rise by «dT_s» K (steel) and «dT_a» K (aluminum). The tests took «ttest_s» s and «ttest_a» s; a 6 mm bar loses heat to the grips and air on a time scale of tens of seconds, so the real rise is a fraction of this, but the specimen is noticeably warm. A ten-times-faster test would be nearly adiabatic, and the softening would lower the measured hardening.

## 5. Design problem D1: reference solution

**D1.** $T = P/\omega$ = 15 000/(2π × 1200/60) = **«D_T» N·m**. Allowable stress at the fillet: steel $(\tau_Y - U)/(2.0 \times 1.6)$ = «D_tlo_s»/3.2 = «D_tall_s» MPa; aluminum «D_tlo_a»/3.2 = «D_tall_a» MPa. Required outer diameter $d$ (mm) and resulting design:

| Option | $d$ for strength | $d$ for twist | Chosen $d$ × $d_i$ | Mass (kg) | Cost (\$) | $K\tau_{max}$ (MPa) | $\varphi$ (°) |
|---|---:|---:|---|---:|---:|---:|---:|
| Steel, solid | «D_s0_ds» | «D_s0_dk» | «D_s0_d» | «D_s0_m» | «D_s0_cost» | «D_s0_tau» | «D_s0_phi» |
| Steel, $d_i/d$ = 0.6 | «D_s6_ds» | «D_s6_dk» | «D_s6_d» × «D_s6_di» | «D_s6_m» | «D_s6_cost» | «D_s6_tau» | «D_s6_phi» |
| Steel, $d_i/d$ = 0.8 | «D_s8_ds» | «D_s8_dk» | «D_s8_d» × «D_s8_di» | «D_s8_m» | «D_s8_cost» | «D_s8_tau» | «D_s8_phi» |
| Aluminum, solid | «D_a0_ds» | «D_a0_dk» | «D_a0_d» | «D_a0_m» | «D_a0_cost» | «D_a0_tau» | «D_a0_phi» |
| Aluminum, $d_i/d$ = 0.6 | «D_a6_ds» | «D_a6_dk» | «D_a6_d» × «D_a6_di» | «D_a6_m» | «D_a6_cost» | «D_a6_tau» | «D_a6_phi» |
| Aluminum, $d_i/d$ = 0.8 | «D_a8_ds» | «D_a8_dk» | «D_a8_d» × «D_a8_di» | «D_a8_m» | «D_a8_cost» | «D_a8_tau» | «D_a8_phi» |

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

1. **$G$ was going to be taken from the machine's head rotation,** as many torsion labs do. The load train's compliance makes that about 10 % low for steel («hfrac_s» % of the elastic head rotation is the machine), which would have produced a "discrepancy" blamed on the material. *Fix:* the troptometer measures $\varphi$ over a known gage length. Eq. 15 and A4 make students measure the machine's compliance and use it only where it is harmless (at fracture). P4(c) asks why the head slope cannot give $G$.
2. **The elastic–perfectly plastic model was presented as "the" theory,** with no way for students to see the material's real shear curve, and the modulus of rupture was easy to mistake for a stress. *Fix:* Eq. 18 (Nadai) recovers $\tau(\gamma)$ from the data (C1, cross-checked against Lab 1). A5 brackets the true stress between $R_T$ and the fully plastic estimate. M1 quantifies the EPP misfit for aluminum and the overstatement of $Tc/J$.
3. **No test of the unloading theory (§3.8).** Residual stress was purely a derivation. *Fix:* the steel is unloaded from about $3\varphi_Y$ and reloaded (procedure step 5). A3 compares the measured permanent twist with Eq. 12 (agreement to «phires_m»° vs «phires_p»°) and checks that unloading is elastic.

**Known limitations (not fixed).** The steel model has no upper yield point or Lüders band, which in a real hot-rolled bar can give a small torque drop near $T_Y$. End effects at the fillets and grips are ignored, which is acceptable because the troptometer reads the middle 50.8 mm. The sample data assume isothermal behavior although X3 shows the steel can heat significantly. The cast iron is modeled with a smooth softening law; real gray iron is also weaker in tension than in compression, which torsion does not test.

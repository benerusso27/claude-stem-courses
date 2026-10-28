# Lab 2 — Instructor Key: Axial Deformation, Redundant Members and Thermal Stress

::: {custom-style="Instructor"}
**For instructors only. Do not distribute to students.** Every number in this key is computed by `src/lab02_analysis.py` (and `src/make_key.py`) from `sample_data.csv` and `src/specimen_measurements.json`, or by the simulation's own model code run in Node. To build a key for your own class data, put your CSV and measurements in the same format and run `python3 src/lab02_analysis.py your.csv your_measurements.json`, then `python3 src/make_key.py`. Uncertainties are expanded ($U = 2u$) unless marked $u$. Sign convention as in the handout (Beer 8e): tension positive; $P$ on the caps is a compressive magnitude.
:::

## 1. Results at a glance (sample data)

| Quantity | Result | Reference / theory |
|---|---|---|
| Part A area $bt$ (mm²) | «A_A» ($u_A/A$ = «uA_rel» %) | 161.29 nominal |
| $E$ of 6061-T6 (GPa) | «E_A» | 68.9 ± 2.0 |
| $\nu$ | «nu» | 0.33 ± 0.02 |
| $G = E/2(1+\nu)$ (GPa) | «G» | about 26 |
| Bending fraction $\beta$; offset $e$ | «beta» ; «e_mis» mm | — |
| $E$ front gage only / back only (GPa) | «E_front» / «E_back» | — |
| $P_{gap}$ (kN) | «Pg» | Eq. 10 with height-gage $g$: «Pg_hg» |
| Gap $g$ from the knee / height gage (mm) | «gap» / «gap_direct» | true value 0.0400 |
| Share $s$ after contact | «share» | Eq. 12: «share_th» |
| Tube force at 30 kN (kN) | «Ft30» | Eq. 11: «Ft_eq11»; no-gap formula: «Ft_nogap» |
| Rod / tube stress at 30 kN (MPa) | «srod30» / «stube30» | yield 370 / 276 |
| Cap compliance $C$ (mm/kN), below / above knee | «C1» / «C2» ($u$) | true value 1.50 |
| $dF_b/dT$ (N/K) | «dFdT» | Eq. 16: «dFdT_th» |
| Preload at 20 °C (kN) | «F0» | 2.0 set |
| Bolt / sleeve stress at 80 °C (MPa) | «sb80» / «ss80» | — |
| $\alpha$ of 6061-T6 inferred from Part C (10⁻⁶/K) | «alpha_meas» | 23.6 ± 0.6 |
| D1 acceptable fixed gap (mm) | «D_gmin» to «D_gmax» | — |

: Table K1. Results from the sample data.

The sample data were generated from a known "truth" model (`src/generate_sample_data.py`, values in `src/truth.json`). It includes a 5.5 % bending fraction in Part A, a +0.6 % gage-factor error, a cap compliance and a seating toe in Part B, and a residual thermal output of +0.4 µε/K and a temperature-dependent sleeve modulus in Part C. The closure test in `tests/test_lab02_independent.py` confirms that the analysis recovers every truth value within its stated uncertainty.

## 2. Pre-lab solutions

**P1.** (a) $A = 25.40 \times 6.35 = «P1_A»$ mm²; $\sigma = 18\,000/«P1_A» = «P1_sig»$ MPa, «P1_frac» % of the 276 MPa yield strength. $\varepsilon_x = \sigma/E = «P1_ex»$ µε; $\varepsilon_y = -\nu\varepsilon_x = «P1_ey»$ µε. A 1 µε resolution is «P1_res2» % of the axial strain at 2 kN and «P1_res18» % at 18 kN. (b) $A_1 = «A1n»$ mm², $k_1 = E_1A_1/L = «k1n»$ kN/mm, $P_{gap} = k_1g ≈ 7$ kN. With $s ≈ 0.4$: $F_2 ≈ -0.4(30 - 7) ≈ «P1_Ft_est»$ kN, so the rod carries about 21 kN, $\sigma_{rod} ≈ «P1_srod_est»$ MPa. (c) Free mismatch $(23.6 - 11.7) \times 10^{-6} \times 60 \times 100 = «mis_n»$ mm. The bolt and sleeve stiffnesses are similar («kb_n» and «ks_n» kN/mm), so each takes about half of the mismatch strain of 714 µε: the bolt strain rises by about 350 µε (exact: «deb_n» µε). Units: K⁻¹ × K × mm = mm.

**P2.** (a) Appendix D.4 of the handout. (b) $A_2 = «A2n»$ mm², $k_2 = E_2A_2/(L - g) = «k2n»$ kN/mm, $P_{gap} = «Pgn»$ kN, $s = «sn»$. $F_2$(10 kN) = «F2n_10» kN, $F_2$(20 kN) = «F2n_20» kN, $F_2$(30 kN) = «F2n_30» kN. Twice $F_2$(10 kN) is «F2n_2x10» kN, not «F2n_20» kN: the first 6.9 kN of every load case goes to the rod alone, so the tube's force is proportional to $P - P_{gap}$, not to $P$. (c) $g \to 0$: $F_2 = -sP$, the textbook result. $k_2 \to 0$: $F_2 = 0$. $k_2 \to \infty$: $s \to 1$, $F_2 = -(P - P_{gap})$.

**P3.** (a) $A_b = «Ab_n»$ mm², $A_s = «As_n»$ mm²; $L/(E_bA_b) + L/(E_sA_s) = «flex_n» \times 10^{-6}$ mm/N; $dF_b/dT = (11.9 \times 10^{-6})(100)/(«flex_n» \times 10^{-6}) = «dFdT_n»$ N/K. At 80 °C: $F_b = 2000 + 60(«dFdT_n») = «F80_n»$ kN; $\sigma_b = «sb80_n»$ MPa, $\sigma_s = «ss80_n»$ MPa. (b) Swapped: $L/(E_{al}A_b) + L/(E_{st}A_s)$ gives $dF_b/dT = «dFdT_sw»$ N/K, so the preload is gone after $2000/«dFdT_sw» ≈ «dTsep»$ K of heating.

**P4.** (a) $e = \beta t/6 = 0.05 \times 6.35/6 = «P4_e»$ mm. (b) The front gage reads $\varepsilon_x(1 + \beta)$, so $E_{front} = E/(1 + \beta)$: «P4_front» % (too low); the back gage gives «P4_back» % (too high). (c) $[\varepsilon_x(1+\beta) + \varepsilon_x(1-\beta)]/2 = \varepsilon_x$ for any $\beta$, because the bending strain is linear through the thickness and the gages are symmetric about the mid-plane.

**P5.** Simulation, presets as shipped: $P_{gap}$ = «sim_Pgap» kN, $s$ = «sim_share» %, $F_2$(30 kN) = «sim_F2» kN; bolt $dF_b/dT$ = «sim_dFdT» N/K, $F_b$ at $\Delta T$ = 60 K = «sim_F1_60» kN. These match P2 and P3 exactly. "Superposition fails with a gap" sets $P$ = 20 kN: the tube carries «sim_F2_20» kN at 20 kN against «sim_F2_10» kN at 10 kN, more than four times as much for twice the load.

**P6.** (a) The rod yields at $F_1 = 370 \times «A1n» = «P6_Fy»$ kN. Before contact, $F_1 = -P$; after, $F_1 = -P_{gap} - (1 - s)(P - P_{gap})$. Setting $|F_1| = «P6_Fy»$ kN gives $P ≈ «P6_Py»$ kN, «P6_fac» times the 30 kN limit (the tube is then at «P6_stube» MPa, still elastic). (b) Scalding (80 °C water): the hook, gloves, and lifting out only below 40 °C. Electric shock (mains heater and water): GFCI outlet, indicator and leads away from the water. Credit also a wet gage giving false readings (sealed gage; the step-4 check).

## 3. Analysis solutions

**A1.** $b$ = «b» mm, $t$ = «t» mm, $A$ = «A_A» mm². Least-squares slope of $\sigma$ against the average axial strain (loading and unloading, 19 points): $E$ = **«E_A» GPa**, intercept «Eint» MPa. Budget (relative $u$): slope statistics «Estat» %, area «uA_rel» %, load cell «load_rel» %, gage factor «gf_rel» %. The gage factor dominates. Transverse vs axial slope: $\nu$ = **«nu»**, intercept «nuint» µε. Agreement (Eq. 21): $|\Delta E|$ = «Eagree_d» ≤ «Eagree_lim» GPa; $|\Delta\nu|$ = «nuagree_d» ≤ «nuagree_lim»; both agree. $G$ = «G» GPa, close to the handbook 26 GPa. Largest loading–unloading difference «hyst» µε, at the noise level: no yielding or slip. *Interpret:* a fitted slope uses every point and ignores a zero offset; a ratio of single readings is biased by any offset and has the noise of one reading. To reduce $u_E$, calibrate the gage factor (shunt calibration), not the calipers.

**A2.** $\beta$ = «beta» («beta_pct» %), nearly constant above 4 kN, so the offset is geometric: $e = \beta t/6$ = **«e_mis» mm**. Single-gage moduli: front «E_front» GPa («E_front_err» %), back «E_back» GPa («E_back_err» %). Harmonic mean $2/(1/E_f + 1/E_b)$ = «E_harm» GPa, identical to the average-strain $E$; the arithmetic mean «E_arith» GPa is biased high by about $\beta^2$. *Interpret:* a one-gage test would have been wrong by about 5 %, «oneg_ratio» times the expanded uncertainty ($U/E$ = «E1U» %), with no warning in the data: a perfectly straight $\sigma$–$\varepsilon$ line can hide a 5 % error.

**A3.** Areas: rod «A_rod» mm², tube «A_tube» ± «uA_tube» mm² ($u$). Two-parameter fit to the loading branch: **$P_{gap}$ = «Pg» kN, $s$ = «share»**, residual scatter «sres» N. With $k_1$ = «k1» kN/mm (Table 1 $E$ for steel), **$g$ = «gap» mm**. The height gage gives «gap_direct» mm; $|\Delta|$ = «gap_d» ≤ «gap_lim» mm, agree. The knee is «gap_ratio» times more precise: it measures the gap through the stiffness of a 150 mm rod, which turns 0.04 mm into 7 kN, while the height gage must resolve the 0.04 mm length difference directly with ±0.01 mm on each length. Theory, Eq. 12 with the measured $E$ and areas: $s$ = «share_th»; $|\Delta|$ = «share_d» ≤ «share_lim», agree. *Check:* $k$ in N/mm = MPa × mm²/mm. A line forced through the origin ($g$ = 0) misses the data by up to «origin_res» kN below 10 kN. *Common error:* reading $P_{gap}$ as "the first load where the tube strain is non-zero" («P_first» kN), which overstates $g$ by «first_err» %.

**A4.** At 30 kN: tube **«Ft30» kN** (measured), rod by equilibrium «Frod30» kN; stresses **«srod30» MPa** (rod) and **«stube30» MPa** (tube), both well below yield. Eq. 11 with the fitted $P_{gap}$ and $s$: «Ft_eq11» kN («Ft_eq11_d» % from the measurement). The textbook no-gap result $-sP$ = «Ft_nogap» kN overstates the tube force by **«nogap_err» %**. Apparent share $F_2/(-P)$: «app_tab»; theory at 30 kN $s(1 - P_{gap}/P)$ = «app_th». It approaches $s$ only as $P \to \infty$. *Check:* the unloading branch gives $s$ = «s_unload», the same line as loading; tube gages differ by «beta_B» % (bending), removed by averaging. *Interpret:* for the no-gap formula to be within 5 % at 30 kN, $P_{gap}/(P - P_{gap}) \le 0.05$, so $P_{gap} \le$ «Pg5» kN and $g \le$ «g5» µm: a tolerance tighter than ordinary machining. Fit-up controls load sharing in short, stiff assemblies.

**A5.** Below the knee (2–6 kN): slope «sl_pre» ± «usl_pre» µm/kN ($u$); $1/k_1$ = «C_rod» µm/kN, so $C$ = **«C1» µm/kN**. Above the knee: slope «sl_post» ± «usl_post» µm/kN; $1/(k_1 + k_2)$ = «C_both» µm/kN, so $C$ = **«C2» µm/kN**. The two estimates differ by «Cdiff_sig» combined standard uncertainties: they disagree. Cause: the low-load points include the seating of the caps and the dial (a toe, as in Lab 1), which adds apparent compliance between 2 and 6 kN. The above-knee estimate is the reliable one (true value 1.50 µm/kN). *Check:* units µm/kN = mm/MN. *Interpret:* the dial reads members, caps and seating in series, and $C$ is about «C_frac» % of the post-contact slope, so it cannot isolate the members. The gages measure the tube's own strain, independent of $C$.

**A6.** $A_b$ = «A_b» mm², $A_s$ = «A_s» mm². Preload at 20 °C: «eps0» µε → **«F0» kN**. Fit of $F_b$ against $T$ (all 19 points): slope «slope» µε/K → **$dF_b/dT$ = «dFdT» N/K** (relative $u$ «u_dFdT_rel» %, dominated by the residual-thermal-output allowance, «u_app_rel» %). Heating alone «dFdT_heat», cooling alone «dFdT_cool» N/K: no slip. Prediction, Eq. 16, with $E_s$ from A1: flexibility sum «flex» × 10⁻⁶ mm/N, **«dFdT_th» N/K** (dominated by the uncertainty in $\alpha_s - \alpha_b$). $|\Delta|$ = «dFdT_d» ≤ «dFdT_lim» N/K: agree. At 80 °C: $F_b$ = «F80» kN, $\sigma_b$ = «sb80» MPa, $\sigma_s$ = «ss80» MPa. *Two effects:* (1) residual thermal output: ±0.5 µε/K × $E_bA_b$ = ±«resid05» N/K, either sign; the truth model's +0.4 µε/K adds +«resid» N/K. (2) The sleeve's modulus falls 1.8 % over 60 K, which changes the average slope by «ET_pct» % (from «slope_noET» to «slope_ET» N/K). The measured excess of «dFdT_d» N/K is consistent with a small positive residual output; the modulus effect alone would push the slope the other way. *Check:* $F_b > 0$ throughout, so the joint never separated.

**A7.** Table K1 supplies the entries; simulation values are in P5. Expected verdicts: $E$, $\nu$, $P_{gap}$ (vs. Eq. 10 with the height-gage $g$, whose large $U$ makes agreement easy), $s$ and $dF_b/dT$ all agree; $F_2$ at 30 kN agrees with Eq. 11 but not with the no-gap formula. The normalized plot should show the knee-based $P_{gap}$ with a much smaller error bar than the height-gage prediction. Full credit requires students to state that the agreement for $P_{gap}$ is weak evidence, because the reference is imprecise.

**M1.** (a) Measured $F_2$(20 kN)/$F_2$(10 kN) = «F20»/«F10» = **«F_ratio»**, not 2. Superposition requires a linear system with a fixed set of active constraints; the tube's contact is a one-sided constraint that switches on at $P_{gap}$, so the response is only piecewise linear. (b) The rod yields before the tube engages if $k_1g > \sigma_YA_1$, i.e. $g > \sigma_Y L/E_1$ = 370 × 150/205 000 = **«gcrit» mm**. In "Gap never closes" ($g$ = 0.4 mm), $P_{gap}$ = «gn_Pgap» kN while the rod is already at «gn_sig» MPa at 60 kN, and the yield warning shows. With $g$ = 0.27 mm and $P$ just above $P_{gap}$, the warning appears as the tube engages. (c) Aluminum bolt in steel sleeve: $dF_b/dT$ = «sw_dFdT» N/K, so $\Delta T_{sep}$ = 2000/«sw_dFdT» ≈ **«sw_dTsep» K**. At 120 K the bonded formula gives $F_b$ = «sw_F120» kN (a bolt in compression), which is impossible: the head lifts off the sleeve, the joint is loose, and both forces are zero. Eq. 16 assumed the members stay in contact.

## 4. Challenge and Extension solutions

**C1.** "Refine a taper" (aluminum cone 30 → 15 mm over 400 mm plus a 100 mm segment of 15 mm diameter, fixed at both ends, heated 60 K; $R$ = «C1_R» kN). Relative error in $R$: «C1_tab». Log–log slope «C1_slope» (theory 2). The finite element with the midpoint area integrates $\int dx/A$ by the midpoint rule, whose error per element is $(h^3/24)(1/A)''$, summing to $O(h^2)$ over the length. On a prismatic segment $1/A$ is constant, the midpoint rule is exact, and so is the element for any $N$.

**C2.** From Eq. 16: $\alpha_s = \alpha_b + (dF_b/dT)(f_b + f_s)/L$ = **«alpha_meas» × 10⁻⁶/K**. Handbook 23.6; $|\Delta|$ = «alpha_d» ≤ «alpha_lim» × 10⁻⁶/K: agree. The dominant term is $u(dF_b/dT)$, itself dominated by the gage's residual thermal output. The truth model used 23.4 × 10⁻⁶/K: this measurement is «alpha_high» % high, consistent with the +0.4 µε/K residual.

**C3.** At 18 kN: $\varepsilon_x$ = «C3_ex» µε, $\varepsilon_y = \varepsilon_z$ = «C3_ey» µε. Width change «C3_db» µm, thickness change «C3_dt» µm. Dilatation $(1 - 2\nu)\varepsilon_x$ = «C3_dil» × 10⁻⁶. The caliper's $u$ is about «C3_ucal» µm, so the width change is about one standard uncertainty: not measurable. Bulk modulus $E/[3(1 - 2\nu)]$ = «C3_K» GPa. $\nu = 0.5$ means zero volume change (incompressible, infinite bulk modulus): the limit approached in plastic flow (Lab 1's constant-volume assumption), not in elastic metals.

**X1.** $E\alpha\Delta T A = 4\pi^2EI/L^2$ with $I/A = d^2/16$ gives $\Delta T_{cr} = \pi^2d^2/(4\alpha L^2)$; $E$ cancels. Example: 10 mm × 0.5 m steel bar, 84.4 K. Yield occurs at $\Delta T_Y = \sigma_Y/(E\alpha)$ = «X1_dTy» K. Buckling comes first when $\pi^2d^2/(4\alpha L^2) < \sigma_Y/(E\alpha)$, i.e. $L/d > (\pi/2)\sqrt{E/\sigma_Y}$ = **«X1_Ld»** for 1018 steel. The simulation experiment (8 mm and 6 mm segments, 1.2 m long, heated 120 K) reports a compressive force of «X1_N» kN against a fixed–fixed Euler load of «X1_Pcr» kN for the thinnest section; by the formula above, that bar buckles after about «X1_dTcr» K.

**X2.** With $E_s$ falling 0.03 %/K, Eq. 16 predicts a quadratic coefficient of about «c2_pred» N/K² and a largest departure from a straight line of «dev_ET» N («dev_ET_ue» µε) over 60 K. The quadratic fit to the data gives «c2» N/K² ($u$): the standard error is about twice the predicted effect, so it is not detectable. A larger range (to 150 °C in oil), averaging several readings per step, or a full-bridge bolt gage (2.6 times the signal) would be needed. The effect on the mean slope, «ET_pct» %, is also well below $u$.

**X3.** Brass tube $A_3$ = «X3_A3» mm², $k_3$ = «X3_k3» kN/mm, shorter than the rod by $g$ + 0.040 mm. Events: aluminum tube engages at **«X3_P1» kN**; brass tube engages when the caps have moved a further 0.040 mm, at **«X3_P2» kN** ($P = P_1 + 0.040(k_1 + k_2)$). At 30 kN: rod «X3_F1» kN, aluminum tube «X3_F2» kN, brass tube «X3_F3» kN (sum «X3_sum» kN = $-P$). Grade the program on event detection (sorted gaps, or a check on each member's contact at each step) and on the equilibrium check.

## 5. Design problem D1: reference solution

**D1.** $\alpha L$ = «D_aL» mm/K for a 3.00 m segment. **Hot requirement** (worst case: installed at the coldest, 10 °C; hottest service, 55 °C): free growth $\alpha(55 - 10)L$ = «D_hot» mm. The allowed restrained shortening is $\sigma_{allow}L/E$ = 40 × 3000/«Ev_MPa» = «D_sigL_E» mm, so $g \ge$ «D_hot» − «D_sigL_E» = **«D_gmin» mm**. (With $g$ = 0 and installation at 15 °C the stress would reach «D_sig0» MPa.) **Cold requirement** (worst case: installed at 20 °C; −25 °C service): the gap grows by «D_hot» mm, so $g \le$ 8.0 − «D_hot» = **«D_gmax» mm**.

*Design 1 (fixed gap):* $g$ = «D_mid» ± «D_tol» mm satisfies both requirements for any installation temperature in 10–20 °C. A specification of 3.0 ± 1.0 mm is easy for a crew to hold with feeler gages and leaves margins of about 0.6 mm and 0.8 mm on the two bounds. *Design 2 (temperature rule):* set $g(T_{inst}) = «D_rule_g15» - «D_rule_slope»(T_{inst} - 15\,°\text{C})$ mm, which keeps the full band width of «D_rule_width» mm (tolerance ±«D_rule_tol» mm) at any installation temperature: more tolerance, at the cost of measuring the rail temperature at installation. *Uncertainty:* $U(\alpha)$ moves each bound by ±«D_ua» mm; $U(E)$ moves the hot bound by ±«D_dE» mm. Both are small compared with the band. A robust answer shrinks the band by these amounts. *Assumptions that could invalidate the design:* the rail's temperature in sun can exceed the air temperature by 20–30 K (check with a contact thermometer on a summer day); the posts are not rigid, so restrained stress is overestimated (conservative); buckling between posts governs the 40 MPa limit (check with Lab 9's Euler formula for the post spacing).

**Rubric detail (15 points total in the report).** Requirements (3): both translated, including that the hot case allows closure plus restrained stress. Worst cases (3.75): opposite installation-temperature extremes for the two requirements. $E$ and $\alpha$ (2.25): uses measured $E$; mentions $U(\alpha)$. Specification and trade-off (4.5): a nominal value and a tolerance, or a rule, checked against both bounds, compared with an alternative. Presentation and assumption (1.5). Typical partial credit: using 15 °C for both bounds (−3); requiring $g \ge$ the full free expansion, ignoring the allowed stress (−2, the design still works but is over-constrained); using the textbook $E$ instead of the measured one (−1).

## 6. Expected ranges for real class data

| Quantity | Expected | If outside, suspect |
|---|---|---|
| $E$ of 6061-T6 from Part A (GPa) | 66–71 | gage factor setting, single-gage use, area from nominal |
| $\nu$ | 0.31–0.35 | transverse gage misaligned; ratio of single readings |
| $\beta$ in Part A | below 0.10 | grips not seated; re-grip |
| Gap from the knee (mm) | as machined, typically 0.02–0.08 | caps not flat; rod or tube ends not square |
| $s$ after contact | 0.35–0.39 | wrong tube area (gross instead of annulus); $E$ of steel used for the tube |
| $C$ above the knee (µm/kN) | 1–4 | fit range includes the knee or the toe |
| $dF_b/dT$ (N/K) | 85–105 | uncompensated gage (reads total strain: about 6 times too large); temperature not settled |
| Preload (kN) | 1.9–2.1 | gage not zeroed with the nut finger-tight |

: Table K2. Expected data ranges.

## 7. Common student mistakes

1. Using one gage of a pair, or averaging the two single-gage moduli instead of the strains.
2. Taking $\nu$ as $-\varepsilon_y/\varepsilon_x$ at one load instead of fitting a slope.
3. Writing equilibrium as $F_1 + F_2 = P$ with tension-positive member forces, which gives tension in a squeezed assembly.
4. Computing the share as $F_2/P$ at the largest load (A4) and calling it $s$.
5. Using the outer-diameter area for the tube, or the steel modulus for the aluminum tube.
6. Picking $P_{gap}$ as the first non-zero tube reading instead of fitting the knee.
7. Subtracting $\alpha_b\Delta T$ from the compensated bolt gage, which the gage has already done.
8. Measuring $\Delta T$ from 0 °C instead of from the preload temperature.
9. Adding stiffnesses instead of flexibilities in the denominator of Eq. 16 (members in series around the loop of the joint).
10. In D1, using one installation temperature for both requirements, or ignoring that the hot case allows the gap to close.
11. Mixing µε and mε, or α per °F and per K.

## 8. Grading rubric

| Part | Points | Full credit | Common deductions |
|---|---:|---|---|
| Pre-lab | 15 | P1–P6 correct with units; P1 an estimate made before measuring | P2 without the superposition explanation (−2); P2(c) limits missing (−1) |
| Data & procedure | 10 | Tables 3–6 complete; checks in steps 2, 4, 8 and 12 recorded | Part C readings before the temperature settled (−3) |
| A1 | 8 | $E$, $\nu$, $G$ with budgets and agreement tests | no budget (−3); ratio instead of slope for $\nu$ (−2) |
| A2 | 5 | $\beta$, $e$, single-gage moduli, harmonic-mean check | arithmetic mean claimed equal (−1) |
| A3 | 8 | two-parameter fit, $g$ with $U$, comparison with height gage, $s$ vs. Eq. 12 | knee by eye (−3) |
| A4 | 7 | stresses, Eq. 11 vs. no-gap comparison, apparent share, tolerance | no tolerance answer (−2) |
| A5 | 5 | both $C$ estimates, disagreement found and explained | disagreement not noticed (−2) |
| A6 | 8 | slope, preload, prediction with $U$, stresses, two effects quantified | uncompensated-strain error (−4) |
| A7 | 4 | complete table, normalized error-bar figure, every discrepancy explained | unexplained discrepancy (−1 each) |
| M1 | 10 | ratio from data; $g_{crit}$ derived and checked; separation temperature and why Eq. 16 fails | no simulation confirmation (−2 each) |
| D1 | 15 | see Sec. 5 | see Sec. 5 |
| Communication | 5 | labeled axes, units, $x \pm U$ format | each unlabeled axis (−1) |
| Challenge | +10 | C1 (4), C2 (3), C3 (3) | — |

: Table K3. Grading rubric (100 points plus up to 10 Challenge points).

Every Core answer must include the required check and interpretation; deduct 1 point per question where either is missing.

## 9. Instructor notes

**Before the lab.** Part A: a 300 mm 6061-T6 flat bar with a 0°/90° gage pair (axial and transverse) on each wide face at mid-length. Part B: face the rod and the tube in the same lathe setup so that the tube ends up 0.03–0.06 mm shorter and both ends are square; harden or use tool-steel caps at least 40 mm thick so that $C$ stays small; bond two axial gages on opposite sides of the tube at mid-length (75 mm from each end, more than ten wall thicknesses from the caps). Part C: bond a steel-compensated (STC 06) gage on the bolt shank, coat it for immersion (nitrile or polysulfide coating), run the leads along the shank and out through a 2 mm notch at the nut end of the sleeve, and test it in warm water the day before. Check the bath's GFCI.

**Timing (2 h).** 0:00–0:10 safety briefing, collect P1–P6; 0:10–0:20 Part C preload and into the bath, heater on; 0:20–0:50 Part A while one partner records Part C every 5 °C; 0:50–1:25 Part B; 1:25–1:45 Part C cooling readings and dimensions; 1:45–2:00 simulation (step 13). With more than four teams, run Part C as one shared station with a single bath and post its readings for everyone.

**Safety.** Demonstrate the hook and the lift-out before anyone heats water. Never let a team open the shield during Part B loading: a cap that is not centred can eject the stack sideways at 30 kN. The 30 kN limit leaves a factor of 2.35 on rod yield.

**Running without equipment.** Give students `sample_data.csv` and Appendix A of the handout; everything in this key applies unchanged. A good hybrid is to run Part B live (the knee is striking to watch) and use the sample data for Parts A and C.

**Your own class data.** Export each part in the column layout of Table A1, fill a measurements JSON like `src/specimen_measurements.json` (including the height-gage lengths), and run `src/lab02_analysis.py` and `src/make_key.py`.

**The simulation.** Students use it in P5, step 13, A7, M1, C1 and X1. Its readout shows closed form vs. numerical agreement for every quantity; the Node and Python tests in `tests/` and the record in `tests/VERIFICATION.md` show that the two agree to round-off for prismatic members and converge as $N^{-2}$ for the taper.

## 10. Self-critique and revisions

Before release, the lab was reviewed as a demanding instructor at a top program would review it. The three biggest weaknesses found, and the fixes made:

1. **The gap in Part B was going to be read off the first non-zero tube reading.** With 2 kN steps this locates $P_{gap}$ only to ±1 kN (15 % of its value), so the comparison with theory was meaningless. *Fix:* the handout now fits the two-parameter model of Eq. 11 by least squares (Appendix D.7), and A3 asks for the gap with its uncertainty and a comparison with an independent height-gage measurement. The fit is «gap_ratio» times more precise than the height gage.
2. **An ordinary gage on the bolt would read total strain**, about $\alpha_b\Delta T$ = 700 µε of free expansion on top of the 350 µε mechanical signal. Students would have had to subtract a large, uncertain number. *Fix:* Part C specifies a gage compensated for steel, the handout explains what it reads (Sec. 2.4), Table 2 states its residual thermal output, the uncertainty budget includes it, and A6 asks students to quantify its effect against the modulus drift.
3. **Three experiments did not fit in two hours,** mainly because heating a bath takes 30–45 minutes with settling time at each step. *Fix:* the procedure starts Part C first and runs Parts A and B on the machine while it heats, and the instructor notes give a minute-by-minute plan and a shared-station option for large sections.

**Known limitations (not fixed).** The simulation treats the caps as rigid ($C$ = 0) and the moduli as independent of temperature; A5 and X2 address both from the data. The sample data have no temperature lag between bath and bolt, so heating and cooling slopes agree better than a live test will show. Saint-Venant end zones at the caps are outside the 1-D model; the gages are placed far enough away (75 mm, more than ten wall thicknesses) that this does not matter here.

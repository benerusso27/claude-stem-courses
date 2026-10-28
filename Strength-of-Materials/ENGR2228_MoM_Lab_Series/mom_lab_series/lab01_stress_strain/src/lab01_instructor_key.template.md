# Lab 1 — Instructor Key: Tension Test and the Stress–Strain Diagram

::: {custom-style="Instructor"}
**For instructors only. Do not distribute to students.** Every number in this key is computed by `src/lab01_analysis.py` (and `src/make_key.py`) from `sample_data.csv` and `src/specimen_measurements.json`, or by the simulation's own model code. To build a key for your own class data, put your CSV and measurements in the same format and run `python3 src/lab01_analysis.py your.csv your_measurements.json`. Uncertainties are expanded ($U = 2u$) unless marked $u$.
:::

## 1. Results at a glance (sample data)

| Quantity | 1018 steel | 6061-T6 aluminum | Reference |
|---|---|---|---|
| $d_0$ (mm), $u_d$ | «d0_s», «ud0_s» | «d0_a», «ud0_a» | nominal 10.00 |
| $A_0$ (mm²), $u_A/A$ | «A0_s», «uA_s» % | «A0_a», «uA_a» % | 78.54 |
| $E$ (GPa) | «E_s» | «E_a» | 205 ± 6 / 68.9 ± 2.0 |
| Upper / lower yield (MPa) | «suy» / «sly» | — | 250–340 |
| 0.2 % offset $\sigma_Y$ (MPa) | «off_s» (on the plateau) | «off_a» | 255–300 (Al) |
| $\sigma_U$ (MPa) | «sU_s» | «sU_a» | 400–480 / 290–330 |
| $\varepsilon_u$ (corrected crosshead) | «eu_s» | «eu_a» | — |
| Hollomon $K$ (MPa), $n$ | «K_s», «n_s» | «K_a», «n_a» | — |
| $C_m$ (mm/kN) | «Cm_s» | «Cm_a» | true value 0.00800 |
| $\Delta_{toe}$ (mm) | «toe_s» | «toe_a» | true value 0.0500 |
| $E_{app}$ measured / Eq. 8 (GPa) | «Eapp_m_s» / «Eapp_p_s» | «Eapp_m_a» / «Eapp_p_a» | — |
| %EL / %RA | «EL_s» / «RA_s» | «EL_a» / «RA_a» | 25–38 / 8–17 %EL |
| True stress at fracture: formula / neck (MPa) | «tform_s» / «tneck_s» | «tform_a» / «tneck_a» | — |

: Table K1. Results from the sample data.

The sample data were generated from a known "truth" model (`src/generate_sample_data.py`, values in `src/truth.json`). The closure test in `tests/test_lab01_independent.py` confirms that the analysis recovers every truth value within its stated uncertainty.

## 2. Pre-lab solutions

**P1.** $A_0 = \pi(10.00)^2/4 = «A0n»$ mm².

(a) Using mid-range reference values (steel $\sigma_Y \approx 295$, $\sigma_U \approx 440$ MPa; aluminum $\sigma_Y \approx 278$, $\sigma_U \approx 310$ MPa): steel $P_Y \approx «PY_s»$ kN, $P_U \approx «PU_s»$ kN (about «PUfrac_s» % of 100 kN); aluminum $P_Y \approx «PY_a»$ kN, $P_U \approx «PU_a»$ kN (about «PUfrac_a» %). Both lie well inside the machine's range; the 50 kN overload stop leaves margin.

(b) Elastic elongation at yield over 50 mm: steel $295/205\,000 \times 50 = «dY_s»$ mm; aluminum $278/68\,900 \times 50 = «dY_a»$ mm. Elongation across the 45–180 MPa window: steel $\Delta\delta_w = 135/205\,000 \times 50 = «dw_s»$ µm; aluminum «dw_a» µm. The criterion $r/\sqrt{12} \le 0.001\,\Delta\delta_w$ gives $r \le «rmax_s»$ µm for steel («rmax_a» µm for aluminum). The crosshead's 1 µm resolution gives a rounding error of «xh_err_s» % of the steel window, about nine times the criterion, even before compliance (P3) is considered. Only the extensometer can measure $E$.

(c) Crosshead travel at fracture ≈ $\varepsilon_f L_c$ + machine stretch: steel ≈ 0.3 × 60 ≈ 20 mm, aluminum ≈ 0.12 × 60 ≈ 7 mm. Phase 1 (to 4 % strain at 1.0 mm/min) needs about 0.04 × 60 + $C_mP$ + toe ≈ 2.7 mm, about 2.7 min. Phase 2 at 5.0 mm/min: steel (20 − 2.7)/5 ≈ 3.5 min, aluminum (7 − 2.7)/5 ≈ 0.9 min. Totals are about 6 min and 3.5 min (the sample data run 360 s and 213 s). Units: mm ÷ (mm/min) = min.

**P2.** (a) $\varepsilon_t = \int_{L_0}^{L} dL/L = \ln(L/L_0) = \ln(1+\varepsilon)$. Then $d\varepsilon_t = d\varepsilon/(1+\varepsilon)$, and with $\sigma_t = \sigma(1+\varepsilon)$, $\sigma_t\,d\varepsilon_t = \sigma\,d\varepsilon$. (b) $\ln(1+\varepsilon)/\varepsilon = 0.99$ at $\varepsilon = «P2_eps»$ %. The series $\ln(1+\varepsilon) \approx \varepsilon - \varepsilon^2/2$ gives the same estimate, $\varepsilon/2 = 0.01$.

**P3.** $A_0C_m/L_c = 78.54 \times 0.008/60 = «AC_L»$ 1/GPa. Steel: $E_{app} = 1/(1/205 + «AC_L») = «Eapp_s»$ GPa («Eapp_s_pct» % of $E$). Aluminum: «Eapp_a» GPa («Eapp_a_pct» %). The steel curve misleads more: the machine term is the same for both, but it is a larger share of the total compliance when the specimen is stiff. Limits: $C_m \to 0$ gives $E$; $E \to \infty$ gives $L_c/(A_0C_m) = «Erigid»$ GPa, the stiffness of the machine itself.

**P4.** $\varepsilon_{t,U} = n = 0.20$, $\varepsilon_u = e^{0.2} - 1 = «P4_eu»$. Eq. 16: $\Delta\varepsilon_{t,u} = 0.88\sqrt{2(0.2)(0.003)} = «P4_d»$, so $\varepsilon_{t,u} \approx «P4_etu»$ and $\varepsilon_u \approx «P4_eu2»$. The maximum load drops by only $\delta_A$ = 0.3 %.

**P5.** Simulation, default settings ($\delta_A$ = 0.3 %, $M$ = 400):

| Preset | $\sigma_Y$ (MPa) | $\sigma_U$ (MPa) | $\varepsilon_u$ (%) | Elongation after fracture (%) | $E_{app}$ (GPa) |
|---|---:|---:|---:|---:|---:|
| Steel | «sim_sY_s» | «sim_sU_s» | «sim_eu_s» (closed form «cf_eu_s») | «sim_EL_s» | «sim_Eapp_s» |
| Aluminum | «sim_sY_a» | «sim_sU_a» | «sim_eu_a» (closed form «cf_eu_a») | «sim_EL_a» | «sim_Eapp_a» |

: Table K2. Simulation predictions.

Aluminum necks at the smaller strain because its hardening exponent is much smaller (0.06 vs. 0.20): by Considère, the hardening rate falls to the true stress sooner.

**P6.** (a) $\sigma_b/\sigma = 8e/d = 8(0.1)/10 = 0.08$, i.e. 8 %. Bending adds $+\varepsilon_b$ on one side and $-\varepsilon_b$ on the opposite side, so the average of two diametrically opposite readings removes it to first order, and the slope of $\sigma$ against the average strain is $E$. (b) Hands stay out while the grips close (pinch point) and whenever the crosshead can move: during the test and especially near fracture. The extensometer is removed only with the crosshead on hold.

## 3. Analysis solutions

**A1.** Steel: linear elastic line, a sharp upper yield point (≈ «suy» MPa), a drop to a serrated plateau near «sly» MPa that ends at about «plateau_end» strain, strain hardening to the maximum, then necking (in the crosshead record) and fracture. Aluminum: linear to about 200 MPa, gradual yielding with no plateau, little hardening, an early maximum, necking, fracture. *Check:* $\sigma = 0$ at $P = 0$ within the load noise (intercepts in A2 are below 0.2 MPa); the elastic slopes are in the ratio $205/68.9 \approx 3.0$, as the moduli are. *Common error:* plotting crosshead strain on the zoomed graph, which makes steel look three times softer than it is.

**A2.** Fit window 45–180 MPa: steel «Enpts_s» points, $E$ = «Ev_s» GPa, intercept «Eint_s» MPa, statistical part «Estat_s» %. Aluminum: «Enpts_a» points, «Ev_a» GPa, intercept «Eint_a» MPa, statistical part «Estat_a» %. Window halves: steel «Elow_s» vs. «Ehigh_s» GPa (difference «Ehd_s» GPa, $2\times$ combined s.e. «Ehs_s» GPa, so linear: $u_{win} = 0$). Aluminum: «Elow_a» vs. «Ehigh_a» GPa (difference «Ehd_a», limit «Ehs_a»: linear). The budget per Eq. 22, in relative standard uncertainty: diameter $2u_d/d$ = «uA_s» %; load cell, extensometer and gage length 0.5 %/√3 = 0.29 % each; statistics as above. Result: **steel $E$ = «E_s» GPa, aluminum $E$ = «E_a» GPa** ($U$, $k = 2$). Agreement (Eq. 23): steel $|\Delta|$ = «Eagree_d_s» ≤ «Eagree_lim_s» GPa, agrees; aluminum «Eagree_d_a» ≤ «Eagree_lim_a» GPa, agrees.
*Check (wider window, 45–260 MPa):* steel «Ewide_s» GPa («Ewide_pct_s» %), essentially unchanged because steel is linear up to its yield point. Aluminum «Ewide_a» GPa («Ewide_pct_a» %): the fit now includes gradual yielding and is biased low. *Interpret:* the three calibration terms dominate equally, then the diameter. A micrometer (±0.002 mm) would cut the area term about tenfold; better calibration certificates (smaller ±a) for the extensometer and load cell would cut the rest. More data points would help almost nothing.

**A3.** Steel: upper yield **«suy» MPa**, lower yield **«sly» MPa**. The offset method on steel gives «off_s» MPa, landing on the plateau as it should. Aluminum 0.2 % offset: **«sY_a» MPa**. Sensitivity to $E$: $\partial\sigma_Y/\partial E$ = «dsdE_a» MPa/GPa for aluminum (the offset line cuts a curve that is flattening, so the sensitivity is small) and «dsdE_s» for steel (cuts a flat plateau). *Check:* aluminum's linear region ends near 200 MPa < «sY_a» < $\sigma_U$. *Interpret:* the upper yield point depends on alignment, loading rate, machine stiffness and specimen finish; the lower yield point is what the material sustains while yielding spreads, so it is reproducible and conservative.

**A4.** (a) Raw crosshead, same window: steel $E_{app}$ = «Eapp_m_s» GPa, aluminum «Eapp_m_a» GPa. (b) Eq. 9 fit above 3 kN: $C_m$ = «Cm_s» mm/kN (steel), «Cm_a» (aluminum); toe «toe_s» mm and «toe_a» mm. (c) Eq. 8 predicts «Eapp_p_s» and «Eapp_p_a» GPa, matching (a) within uncertainty. (d) Corrected crosshead strain minus extensometer strain over the last 50 extensometer points: steel «splice_s» $\times 10^{-6}$, aluminum «splice_a» $\times 10^{-6}$; the splice is seamless. *Check:* $A_0C_m/L_c$ in mm²/kN = 1/GPa; as $C_m \to 0$, $E_{app} \to E$. *Interpret:* the machine and grips are about twice as compliant as the steel specimen, so crosshead strain mostly measures the machine.

**A5.** $\sigma_U$: steel **«sU_s» MPa** ($P_{max}$ = «Pmax_s» kN from a parabola through the peak region), aluminum **«sU_a» MPa**. $\varepsilon_u$ (corrected crosshead): steel **«eu_s»**, aluminum **«eu_a»**. Strain span over which $P > P_{max} - 2u_P$: steel «euspan_s», aluminum «euspan_a»; half of it, divided by √3, dominates $u(\varepsilon_u)$. *Check:* for aluminum the extensometer came off at 4.0 % strain, before $\varepsilon_u$, so the corrected crosshead strain is required. *Interpret:* at a flat maximum, a small change in load corresponds to a large change in strain, so $\varepsilon_u$ is ill-conditioned while $\sigma_U$ is well-conditioned.

**A6.** Hollomon fits: steel $K$ = «K_s» MPa, $n$ = «n_s»; aluminum $K$ = «K_a» MPa, $n$ = «n_a». Measured $\varepsilon_{t,U} = \ln(1+\varepsilon_u)$: steel «etu_s», aluminum «etu_a». Discrepancy $n - \varepsilon_{t,U}$: steel «ndisc_s», aluminum «ndisc_a», both larger than the combined $U$ (steel «nU_s», aluminum «nU_a»): **disagree**. *Check (direct Considère):* on the smoothed data the slope $d\sigma_t/d\varepsilon_t$ equals $\sigma_t$ at $\varepsilon_t$ = «cons_s» (steel) and «cons_a» (aluminum), matching the measured necking strains. Considère's criterion itself holds; the disagreement comes from the Hollomon prediction. Two quantified reasons:
(i) *Imperfection.* The diameter readings span 0.01 mm, so $\delta_A \approx 2(0.01)/10 = «dA_s»$ %. Eq. 16 gives a shortfall of «dEps_s» (steel) and «dEps_a» (aluminum), so the predictions become «npred_s» and «npred_a».
(ii) *Fit form.* The remaining gaps («nres_s» steel, «nres_a» aluminum) arise because the hardening is not a single power law. Steel's hardening restarts after the Lüders plateau (its curve is shifted, like Swift's $\varepsilon_0$), and aluminum's exponent varies with strain. A global $n$ then overstates the local exponent $d\ln\sigma_t/d\ln\varepsilon_t$ at necking, which by Considère must equal $\varepsilon_{t,U}$.
Full credit requires the direct check and at least one quantified cause.

**A7.** %EL: steel **«EL_s»**, aluminum **«EL_a»**. %RA: steel **«RA_s»**, aluminum **«RA_a»**. Modulus of resilience: steel «uY_s» MJ/m³, aluminum «uY_a» MJ/m³ (aluminum stores more elastic energy per volume because its $E$ is low). Energy to maximum load: steel «uUe_s» MJ/m³ (engineering) = «uUt_s» (true); aluminum «uUe_a» = «uUt_a». Area to fracture with corrected crosshead strain: steel «tough_s», aluminum «tough_a» MJ/m³. Corrected crosshead strain at fracture: steel «ech_f_s» %, aluminum «ech_f_a» %, both lower than %EL. The neck's extra length is divided by $L_c$ = 60 mm instead of $L_0$ = 50 mm, and %EL is measured after elastic recovery. *Interpret:* for absorbing an overload without breaking, choose steel: about five times the energy to maximum load and four times the area to fracture.

**A8.** Use Table K1 and the simulation values in Table K2. Expected verdicts: $E$ agrees for both materials; $E_{app}$ agrees with Eq. 8; $\sigma_U$ from the simulation preset agrees within a few percent (the preset is a smooth fit); $\varepsilon_u$ disagrees with the Hollomon/Considère prediction (A6) and is matched by the simulation only when $\delta_A$ is set from the diameter readings; for steel the yield plateau is absent from the simulation (X3). Full credit needs each discrepancy above $U$ explained with a named, quantified cause.

**M1.** Steel: $\sigma_f(1+\varepsilon_f)$ = «sf_s» × (1 + «ELv_s»/100) ≈ **«tform_s» MPa**, versus $P_f/A_f$ = «Pf_s» kN / (π «df_s»²/4) = **«tneck_s» MPa**; the formula is off by «terr_s» %. Aluminum: **«tform_a»** vs. **«tneck_a» MPa** («terr_a» %). (b) The failed assumption is uniform deformation: Eq. 12 uses the gage-average strain, but after the maximum load the neck strains far more than the average ($\varepsilon_t$ in the neck is «etneck_s» for steel, against $\ln(1+\varepsilon_f) \approx 0.29$). In the simulation (default settings), the "σ(1+ε)" and "neck σt" readings first differ by more than 2 % right at the maximum load. For steel this happens slightly *before* it (ε ≈ 17.2 % vs. ε_u = 17.7 %), because the weaker neck site starts to strain ahead of the rest of the gage; for aluminum it happens just after (ε ≈ 5.20 % vs. 5.16 %). Credit either description if it is tied to the maximum load and explained. (c) The curved neck profile creates radial and hoop tensile stresses (a triaxial state). The axial stress peaks at the center, and the uniaxial flow stress is lower than $P/A$ by a factor of 1.1–1.25 (Bridgman, X2).

## 4. Challenge and Extension solutions

**C1.** Algebra as in Appendix D.5 of the handout. Simulation (steel preset; drop in $\varepsilon_{t,u}$, numerical vs. Eq. 16): «C1tab_s». Log–log slope «C1slope_s» (theory 0.5). Eq. 16 is off by 20 % near $\delta_A$ ≈ 3 % for steel. For aluminum («C1tab_a», slope «C1slope_a») it is off by 20 % already at $\delta_A$ ≈ 1 %, consistent with the validity condition $\delta_A \ll n/2$ (aluminum's $n/2 \approx 0.03$).

**C2.** 4000 Monte Carlo draws: $u(E)$ = «mc_uE» GPa (first-order «lin_uE»), $u(\sigma_Y)$ = «mc_uY» MPa (first-order «lin_uY»), mean $\sigma_Y$ = «mc_Y» MPa. The two methods agree to «mc_agree», as expected for a measurement model that is nearly linear over input changes of a fraction of a percent. Students who find a large difference have usually drawn a ±a limit as a normal distribution with standard deviation a.

**C3.** The largest sample has error $\sigma_U - \sigma(t_i) \approx \tfrac12|\sigma''|(t_i - t^*)^2 \le \tfrac18|\sigma''|h^2$. That bound has slope 2, but the actual error depends on where the nearest sample happens to fall, hence the scatter. Integrating to the largest sample moves the upper limit by up to one step, $O(h)$, while the integrand there is $\sigma_U \neq 0$, so the missing area is $\sigma_U \cdot O(h)$: first order. Integrating to a fixed strain leaves only the trapezoid error, $O(h^2)$.

**X1.** With the neck length set by the mesh, elongation after fracture keeps falling (steel: «mesh_s»; aluminum: «mesh_a») toward $\varepsilon_u$, because softening localizes into one element of length $L_0/N$. The model has no physical neck length: real necks scale with $d_0$ through three-dimensional effects (necking geometry, triaxiality). Simulation, steel, varying $L_0/d_0$: «X1_s». From the sample data, $c = (\%EL/100 - \varepsilon_u)\,L_0/d_0$ = «c_s», so a $4d_0$ gage would give about «EL4_s» %.

**X2.** With $a/R$ = 1: factor $(1 + 2R/a)\ln(1 + a/2R)$ = «bfac_10», corrected stress ≈ «bridg_10» MPa. With $a/R$ = 0.5: factor «bfac_05», ≈ «bridg_05» MPa. A twofold uncertainty in $R$ moves the answer by about 10 %, so a photograph with a scale bar is needed.

**X3.** The plateau ends where hardening lifts the stress clearly above the plateau, at a total strain of «plateau_end». Subtracting the elastic strain $\sigma_Y/E$ gives a Lüders strain $\varepsilon_L$ ≈ «epsL» (the truth model uses 0.017). During the plateau the load is constant, so the machine's stretch does not change and all of the crosshead motion goes into new Lüders strain: $v_{front}\,\varepsilon_L = v_{ch}$, giving $v_{front} \approx v_{ch}/\varepsilon_L$ ≈ «vfront» mm/min ≈ 1 mm/s. The band therefore crosses the 60 mm reduced section in about 60 s; the sample data's plateau lasts «plat_t» s (from the load drop to the start of hardening). A smooth law with $d\sigma/d\varepsilon_p > 0$ everywhere has no locally softening branch, so it cannot nucleate and propagate a band. The simulation's steel preset therefore goes straight from elastic to hardening.

## 5. Design problem D1: reference solutions

**D1.** Conservative strength $\sigma_Y - U$: steel «D_sigY_lo_s» MPa, aluminum «D_sigY_lo_a» MPa. Required gross areas (mm²):

| Requirement | Equation | Steel | Aluminum |
|---|---|---:|---:|
| FS ≥ 2.0 at service, thread | $A \ge 2.0\,P_s/(0.78\,\sigma_{Y,lo})$ | «D_A_strength_s» | «D_A_strength_a» |
| No yield at overload, thread | $A \ge P_o/(0.78\,\sigma_{Y,lo})$ | «D_A_over_s» | «D_A_over_a» |
| Stretch ≤ 1.20 mm, gross | $A \ge P_sL/(E\,\delta_{max})$ | «D_A_stiff_s» | «D_A_stiff_a» |
| Governs | | «D_gov_s» | «D_gov_a» |
| Minimum $d$ (mm) → chosen | | «D_d_req_s» → **«D_d_s»** | «D_d_req_a» → **«D_d_a»** |
| Thread stress at service (MPa), FS | | «D_stress_service_thread_s», «D_FS_actual_s» | «D_stress_service_thread_a», «D_FS_actual_a» |
| Stretch at service (mm) | | «D_delta_s» | «D_delta_a» |
| Mass (kg), cost ($) | | «D_mass_s», «D_cost_s» | «D_mass_a», «D_cost_a» |

: Table K3. Reference designs for D1.

Both are acceptable. Steel at 12 mm is the cheapest; aluminum at 19 mm is the lightest, governed by stiffness. Other defensible answers: steel at 13 mm for more stiffness margin; a steel rod with upset (enlarged) threaded ends; an aluminum tube. Any design that meets all three requirements with the student's own conservative strength and justifies the choice quantitatively earns full marks. A critical assumption students might name: static load only. Thread roots are stress concentrations ($K_t \approx 3$), so fatigue under walkway traffic, corrosion of steel, or galvanic contact for aluminum could govern. Check by a fatigue estimate or a code provision for tension rods.

**Rubric detail (15 points total in the report).** Requirements (3): all three translated, including that strength uses the stress area and stretch the gross area. Strength basis (4.5): uses $\sigma_Y - U$ from the student's own data; full credit only if $U$ is from their analysis. Calculations (4.5 combined with the above): correct areas, rounding up to available stock. Every check shown (3). Trade-off between two alternatives with numbers (3). Presentation and critical assumption (1.5). Typical partial credit: using a typical handbook $\sigma_Y$ (−2), using gross area at the threads (−3), forgetting the overload case when it does not govern (−0.5), forgetting stiffness for aluminum (−3, because it governs).

## 6. Expected ranges for real class data

| Quantity | Steel (1018 HR) | Aluminum (6061-T6) | If outside, suspect |
|---|---|---|---|
| $E$ from extensometer (GPa) | 195–212 | 66–71 | extensometer seating, wrong $L_e$, fit window |
| $E_{app}$ from crosshead (GPa) | 20–90 | 15–55 | not a fault: machine-specific |
| $C_m$ (mm/kN) | 0.003–0.02 | same | toe not excluded |
| Lower yield / offset $\sigma_Y$ (MPa) | 250–340 | 255–300 | specimen heat-treat or mix-up |
| $\sigma_U$ (MPa) | 400–480 | 290–330 | area error (diameter) |
| $\varepsilon_u$ | 0.15–0.24 | 0.04–0.09 | crosshead not corrected |
| Hollomon $n$ | 0.18–0.26 | 0.05–0.10 | fit range includes plateau or elastic part |
| %EL in $5d_0$ / %RA | 25–38 / 50–65 | 8–17 / 30–50 | fracture outside gage marks (retest) |

: Table K4. Expected data ranges.

## 7. Common student mistakes

1. Taking $E$ from crosshead travel, or from a stress–strain plot whose strain axis is crosshead strain.
2. Using the nominal 10.00 mm instead of the measured diameter, or using radius in $\pi d^2/4$.
3. Placing the offset line at 0.2 (not 0.002) or mixing percent and fraction in the same equation.
4. Reporting the upper yield point as $\sigma_Y$.
5. Converting to true stress past the maximum load and calling it "the true stress–strain curve."
6. Fitting the Hollomon law over a range that includes the elastic part or the Lüders plateau.
7. Adding stiffnesses instead of compliances in Eq. 8 (springs in series add compliance).
8. Treating a manufacturer's ±a as a standard uncertainty, or adding relative uncertainties linearly.
9. Dividing crosshead travel by $L_0$ instead of $L_c$, which mixes gage lengths.
10. Excess significant figures (e.g. "E = 205.21883 GPa ± 2.4").
11. In D1, using the gross area at the threads, or a handbook yield strength instead of the measured lower bound.

## 8. Grading rubric

| Part | Points | Full credit | Common deductions |
|---|---:|---|---|
| Pre-lab | 15 | P1–P6 correct with units; estimate before measuring | P1 without units (−2); P3 limits missing (−1) |
| Data & procedure | 10 | Tables 3–5 complete; checks in steps 2, 4 and 7 recorded | missing $d_0$ repeats (−3) |
| A1 | 4 | both curves, zoomed plot, stages named | crosshead strain on the zoom (−2) |
| A2 | 7 | E ± U with budget, window test, agreement test, wide-window check | no budget (−3) |
| A3 | 5 | upper and lower yield, offset with sensitivity to E | upper yield as $\sigma_Y$ (−2) |
| A4 | 7 | $E_{app}$, $C_m$ fit, Eq. 8 comparison, splice shown | stiffnesses added (−3) |
| A5 | 5 | $\sigma_U$, $\varepsilon_u$ with flat-peak uncertainty | $\varepsilon_u$ from uncorrected crosshead (−2) |
| A6 | 7 | fit, direct Considère check, two quantified reasons | reasons not quantified (−3) |
| A7 | 5 | %EL, %RA, energies, identity check, gage-length explanation | — |
| A8 | 5 | complete tables, normalized error-bar figure, every discrepancy explained | unexplained discrepancy (−1 each) |
| M1 | 10 | both values, failed assumption with timing, triaxiality | no timing from simulation (−3) |
| D1 | 15 | see Sec. 5 | see Sec. 5 |
| Communication | 5 | labeled axes, units, $x \pm U$ format | each unlabeled axis (−1) |
| Challenge | +10 | C1 (4), C2 (3), C3 (3) | — |

: Table K5. Grading rubric (100 points plus up to 10 Challenge points).

Every Core answer must include the required check and interpretation; deduct 1 point per question where either is missing.

## 9. Instructor notes

**Before the lab.** Order specimens with $d_0$ = 10.00 mm, a 60 mm reduced section and gage marks 50.0 mm apart. If your machine's capacity is below 100 kN, use 6.0 mm specimens instead (loads scale with $d_0^2$: about 13 kN for steel) and scale $L_0$ to 30 mm so that $L_0 = 5d_0$ still holds. Verify the extensometer's calibration date and gage length. Pre-set two test methods (steel and aluminum) with the rate change at 4 % extensometer strain. Print Tables 3–6b.

**Timing (2 h).** 0:00–0:10 safety briefing and pre-lab check (collect P1–P6); 0:10–0:25 diameter measurements; 0:25–0:55 steel test; 0:55–1:20 aluminum test; 1:20–1:35 post-test measurements and fracture surfaces; 1:35–2:00 simulation comparison (procedure step 13). If time is short, run aluminum while steel's post-test measurements are made.

**Safety.** Demonstrate the hold, extensometer removal and shield before the first test. The steel specimen absorbs about 0.6 kJ of plastic work (the neck is warm to the touch), and at fracture the specimen and machine release about 3 J of stored elastic energy, enough to throw a fragment: keep the shield closed. Do not let students remove grip pieces until the load reads near zero.

**Running without equipment.** Give students `sample_data.csv` and Appendix A of the handout; everything in this key applies unchanged. A hybrid works well: run one live test (steel) for the experience, and use the sample data for the analysis so all teams have identical numbers to compare.

**Your own class data.** Export each test as CSV with the columns specimen, time_s, load_N, crosshead_mm and extensometer_mm, fill a measurements JSON like `src/specimen_measurements.json`, and run `src/lab01_analysis.py`. It prints every key quantity and writes `results.json`.

**The simulation.** Students use it in P5, step 13, A8, M1, C1, C3 and X1. Its readout explains every closed-form vs. numerical gap; its tests are in `tests/` and summarized in `tests/VERIFICATION.md`.

## 10. Self-critique and revisions

Before release, the lab was reviewed as a demanding instructor at a top program would review it. The three biggest weaknesses found, and the fixes made:

1. **Eq. 16 (imperfection sensitivity) was asserted, not derived, and its range of validity was not stated.** A student could not reproduce the $\sqrt{2n\delta_A}$ step. *Fix:* the handout now states the result with its validity limit in Sec. 2.6 and gives the equilibrium argument and the quadratic expansion step by step in Appendix D.5, states the validity condition $\delta_A \ll n/2$, and Challenge C1 makes students find where it fails (20 % error at $\delta_A$ ≈ 3 % for steel, 1 % for aluminum).
2. **The uncertainty budget for $E$ ignored the choice of fitting window,** a model-form error that can exceed every instrument term for a material that yields gradually. A wider window lowers the aluminum modulus by «Ewide_pct_a» %. *Fix:* Eq. 22 now includes $u_{win}$ with an objective test (fit the two halves; include the term only if their slopes differ by more than twice their combined standard error). A2 requires the test, and `lab01_analysis.py` implements it.
3. **Pre-lab P1(b) asked for a "tolerable" resolution without a criterion,** so answers could not be graded consistently. *Fix:* it now specifies the criterion (rounding error $r/\sqrt{12}$ below 0.1 % of the elongation across the fitting window), which yields a definite number («rmax_s» µm for steel) and shows quantitatively why the crosshead cannot measure $E$.

**Known limitations (not fixed).** The sample data contain no load-train misalignment, so P6(a) cannot be demonstrated with them; a live test with an intentionally offset grip shows it. The steel preset in the simulation has no Lüders plateau (X3 turns this into a question). Eq. 16 uses a uniform-zone neck; real necks have a strain gradient, so the coefficient $1 - \ell/L_0$ is approximate.

# Lab 9 — Instructor Key: Columns

::: {custom-style="Instructor"}
**For instructors only. Do not distribute to students.** Every number in this key is computed by `src/lab09_analysis.py` (and `src/make_key.py`) from `sample_data.csv` and `src/specimen_measurements.json`, or by the simulation's own model code run in Node. To build a key for your own class data, put your CSV and measurements in the same format and run `python3 src/lab09_analysis.py your.csv your_measurements.json`, then `python3 src/make_key.py`. Uncertainties are expanded ($U = 2u$) unless marked $u$; the clamp stiffness and the prediction that uses it come from a Monte Carlo propagation (GUM Supplement 1) in which the load-cell calibration is common to both clamped tests. Sign convention as in the handout (Beer 8e §10.1–10.2): $P$ compressive and positive, $x$ down the column from end A, $y$ lateral, $M = -P(y + e)$; the column bows away from the load line; tension positive; front face convex.
:::

## 1. Results at a glance (sample data)

| Quantity | Measured | Reference or prediction | Verdict (Eq. 11) |
|------------------------------|----------------|------------------------------|--------------------|
| Bar: $b$, $t$ (mm) | «b», «t» | 25.40 × 6.35 nominal | — |
| $P_{cr}$, pinned 300 mm (N) | «A300_PS» | Euler «A300_Pe» | «A300_ag» |
| $P_{cr}$, pinned 450 mm (N) | «A450_PS» | Euler «A450_Pe» | «A450_ag» |
| $P_{cr}$, pinned 600 mm (N) | «A600_PS» | Euler «A600_Pe» | «A600_ag» |
| Slope of $\log P_{cr}$ against $\log L$ | «A_slope» | −2 | agree |
| $E$ from the Southwell loads (GPa) | «ES» | Lab 2: «ref_E» | «ES_ag» |
| $E$ from the axial strain (GPa) | «Eg» | Lab 2: «ref_E» | «Eg_ag» |
| $P_{cr}$, fixed–fixed 600 mm (N); $K$ | «Bff_PS»; «Bff_K» | Euler, $K$ = 0.5: «Bff_Pe» | «Bff_ag» (8 % low) |
| Clamp stiffness $k$ (N·m/rad) | «B_k» | — | — |
| $P_{cr}$, fixed–pinned 640 mm (N); $K$ | «Bfp_PS»; «Bfp_K» | $K$ = 0.699: «Bfp_Pe»; Eq. 4 with $k$: «B_pred» | «Bfp_ag» with 0.699; «B_pred_ag» with Eq. 4 |
| Groove offsets from Part C (mm) | «C1_e», «C2_e» | 1.00, 2.00 (±0.02) | «C1_ag», «C2_ag» |
| Part D maximum load (kN) | «D_P» | Euler «D_PE»; tangent modulus «D_Pt» | Euler «D_Eo» % high; tangent «D_to» % high |
| D1 lightest tube | «D1_best» | with $K$ = 0.52 from Part B: «D1_trap» (buckles at «D1_tpPcr» kN) | — |

: Table K1. Results from the sample data.

The sample data were generated from a known "truth" model (`src/generate_sample_data.py`, values in `src/truth.json`): $E$ = «T_E» GPa; bar «T_b» × «T_t» mm; half-sine bows of «T_d0» mm (300, 450, 600 mm) plus a small third harmonic; the knife edges put the load line «T_ek» mm off the axis; clamps of «T_k» N·m/rad (bottom, top); groove offsets «T_C» mm; load cell «T_gain» % high, UTM «T_utm» %; dial noise 0.003 mm and 0.01 mm resolution; gage-factor errors +0.4 % (front) and −0.2 % (back) and 1.5 µε noise. The response is a Hermite finite-element model with the stress-free bow, the end offsets and the clamp springs; Part D is the fiber model with Lab 1's Ramberg–Osgood curve ($\sigma_{0.2}$ = «T_s02» MPa, $m$ = «T_m»), maximum «T_DPm» kN. The closure tests in `tests/test_lab09_independent.py` confirm that the analysis recovers every truth value within its stated uncertainty.

## 2. Pre-lab solutions

Nominal section: $A$ = «P_A» mm², $I$ = «P_I» mm⁴, $r$ = «P_r» mm; with Table 1's $E$, $EI$ = «P_EI» N·m².

**P1.** (a) $L/r$ = «P1_sl300», «P1_sl450», «P1_sl600»; $P_{cr}$ = «P1_P300», «P1_P450», «P1_P600» N; $\sigma_{cr}$ = «P1_s300», «P1_s450», «P1_s600» MPa, far below $\sigma_Y$. (b) Fixed–fixed 600 mm ($L_e$ = 300 mm): «P1_ff» N; fixed–pinned 640 mm ($L_e$ = 0.699 × 640 mm): «P1_fp» N. (c) 90 mm: $L/r$ = «P1_sl90», Euler gives «P1_90» kN, $\sigma_{cr}$ = «P1_s90» MPa, above $\sigma_Y$; $\sigma_YA$ = «P1_sYA» kN. Euler's formula stops applying below $L/r = \pi\sqrt{E/\sigma_Y}$ = «P1_slY», so the bar reaches the yield region first (and, as Part D shows, fails well below both). (d) $\delta$ = «P1_d50», «P1_d75» and «P1_d90» mm. Units: GPa × mm⁴/mm² = (10³ N/mm²)(mm²) = kN, so keep $E$ in N/mm² (MPa) to get newtons.

**P2.** Both have $L_e$ = 300 mm, so the same ideal $P_{cr}$ («P1_P300» N). The clamped bar buckles lower, because no real clamp is rigid: Part B measures «Bff_PS» N against «A300_PS» N for the 300 mm pinned bar.

**P3.** $\delta/P$ = «P3_y» mm/kN. The line has slope «P3_slope» × 10⁻⁶ N⁻¹ and intercept «P3_icpt» × 10⁻⁶ m/N: $P_{cr}$ = «P3_P» N and $\delta_0$ = «P3_d0» mm. The 900 N reading is the least reliable: its deflection is small, so the dial's ±0.01 mm and the seating of the knife edges matter most, and higher buckling modes still contribute below about $0.5P_{cr}$. The method needs no reading near $P_{cr}$ because Eq. 6 is a straight line at every load.

**P4.** $P$ = «P4_P» N: $y_{max}$ = «P4_y» mm, $M = P(e + y_{max})$ = «P4_M» N·m, $\sigma_{max}$ = «P4_ax» + «P4_sb» = «P4_s» MPa (Eq. 8 gives «P4_secant» MPa). Without deflection the bending stress would be «P4_sb0» MPa and $\sigma_{max}$ = «P4_s0» MPa: the deflection multiplies the bending stress by «P4_fac» $= \sec(\pi/(2\sqrt2))$.

**P5.** (Simulation, exact page code.) "Lab Part A: pinned, 450 mm": «sim_A450» N closed form and «sim_A450fe» N by finite elements (E = 68.9 GPa, the series' truth value in the page's material table). Springs, $k$ = 2800 N·m/rad, 600.5 mm: $P_{cr}$ = «sim_sprP» N, $K$ = «sim_sprK» (ideal fixed ends: «sim_sprI» N). "Lab Part C, e = 2 mm": first-yield load «sim_C2PY» N, against «sim_C2lin» N from Eq. 10.37 (both treat the 0.46 mm bow as an extra offset $(4/\pi)\delta_0$ = 0.59 mm). "Lab Part D": Euler «sim_DE» kN, tangent modulus «sim_Dt» kN, reduced modulus «sim_Dr» kN, fiber model «sim_Dfib» kN.

**P6.** (a) A column kicking sideways if a knife edge slips (seat both ends, guard, hands out); the screw loader (turn by hand, back off before touching); Part D's large load and possible fragments (shield, distance). (b) $\sigma$ = «P6_s» MPa = «P6_pct» % of $\sigma_Y$ at $\delta$ = 5 mm on the 300 mm bar, the worst of the three. The limit keeps every bar elastic so it can be reused and the Southwell analysis stays valid; in the sample data the largest stress in Parts A–C is «P6_true» MPa («P6_true_pct» % of $\sigma_Y$).

::: {.needspace lines="12"}
:::

## 3. Analysis solutions

| $L$ (mm) | $L/r$ | Euler $P_{cr}$ (N) | Southwell $P_{cr}$ (N) | Difference (%) | Limit (%) | Southwell $\delta_0$ (mm) | Bow (mm) | $E$ from $P_{cr}$ (GPa) |
|----|-----:|---------:|---------:|------:|-----:|---------:|-----:|---------:|
«A_table»

: Table K2. Part A: Southwell fits (readings with $P \ge 0.5\,P_{pred}$) and Euler predictions with Lab 2's $E$, the measured section and lengths. Limit = $2\sqrt{u_1^2 + u_2^2}$ (Eq. 11).

**A1.** Southwell fits use «A300_n», «A450_n» and «A600_n» readings (from «A300_Pmin», «A450_Pmin» and «A600_Pmin» N up). All three critical loads agree with Euler (Table K2); the Southwell loads run about 1 % above Euler, which A6 traces to $E$. Slope of $\log P_{cr}$ against $\log L$: «A_slope», as Eq. 1 requires. $E$ from the three loads: «ES» GPa, against Lab 2's «ref_E» GPa: «ES_ag» ($|\Delta|$ = «ES_d» % of $E$, limit «ES_lim» %). *Interpret:* Southwell's $\delta_0$ exceeds the surface-plate bow by «bowx_lo»–«bowx_hi» mm because the knife edges put the load slightly off the axis; an offset $e$ acts like a bow of $(4/\pi)e$, so $e \approx (\pi/4)(\delta_{0,S} - \text{bow})$ = «A300_eeq», «A450_eeq» and «A600_eeq» mm, about «eeq_mean» mm (truth «T_ek» mm). The last readings reach only «last_lo»–«last_hi» of $P_{cr}$, yet the fits find $P_{cr}$ to a fraction of a percent.

**A2.** Fixed–fixed: $P_{cr}$ = «Bff_PS» N, $K$ = «Bff_K», against 0.5: «Bff_ag»; Euler with $K$ = 0.5 is «Bff_over» % above the measurement. Fixed–pinned: «Bfp_PS» N, $K$ = «Bfp_K» against 0.699: «Bfp_ag» (Euler «Bfp_over» % high). From Eq. 3 with the fixed–fixed result ($x = pL/2$ = «C2_x»): $k$ = «B_k» N·m/rad (95 % interval «B_klo»–«B_khi»; $kL/EI$ = «B_kLEI»; truth mean «k_true»). Eq. 4 with this $k$ predicts «B_pred» N for the fixed–pinned test ($K$ = «B_predK»), against «Bfp_PS» N measured: «B_pred_ag» ($|\Delta|$ = «B_pred_d» %, limit «B_pred_lim» %; the common load-cell error cancels). *Check:* Eq. 3 with $k \to \infty$ gives $\tan x = 0$, $x = \pi$, $K$ = 0.5. *Interpret:* assuming fixed ends overstates this column's capacity by «Bff_over» %, a margin a designer would not see; a clamp with $kL/EI$ ≈ 45 is "fixed" only to within 9 % in load.

| Load (N) | Part A δ (mm) | e = 1: δ (mm) | Difference (mm) | Eq. 7, e = 1 mm (mm) | e = 2: δ (mm) | Difference (mm) | Eq. 7, e = 2 mm (mm) |
|------:|------:|------:|------:|------:|------:|------:|------:|
«C_table»

: Table K3. Part C minus Part A at the same loads (every second load shown), with Eq. 7 for the nominal offsets and $P_{cr}$ from A1.

**A3.** Fitting Eq. 7 to the differences: $e$ = «C1_e» mm and «C2_e» mm, both «C1_ag» with the grooves (1.00 and 2.00 ± 0.02 mm). From the gages, the change of the lever arm minus the change of deflection gives $e$ = «C1_es» and «C2_es» mm, the same within a few hundredths of a millimeter: the gages see the moment $P(e + y_{max})$ of Beer Fig. 10.23. *Check:* at 200 N the difference is close to $(\pi^2/8)e\,P/P_{cr}$. *Interpret:* from 600 to 1200 N the eccentric deflection grows by a factor «C1_ratio» (e = 1 mm) and «C2_ratio» (e = 2 mm), against «C_ratio_th» from Eq. 7 and 2 for a linear response: the effects of several loads cannot be added, although at one load the responses to the bow and to the offset do add (which is why the subtraction works).

**A4.** With $P_{cr}$ from A1 and $\sigma_Y$ = 273.7 MPa, Eq. 8 gives first yield at «PY1» N ($e$ = 1 mm) and «PY2» N ($e$ = 2 mm), that is «PYr1» and «PYr2» of $P_{cr}$; Eq. 10.37 gives «PYl1» kN and «PYl2» kN, «PYo2» times too high for $e$ = 2 mm, because it ignores the deflection, which reaches «PYy2» mm at first yield. At «st_P» N with $e$ = 2 mm the back gage gives «st_meas» MPa; Eq. 8 with the 2 mm offset alone gives «st_1035» MPa («st_low» % low), and adding the Part A stress at the same load («st_A» MPa, minus the axial «st_ax» MPa counted twice) gives «st_sum» MPa, within «st_pct» %. *Check:* $e \to 0$ gives $P_Y \to P_{cr}$ here, because $P_{cr} < \sigma_YA$. *Interpret:* $\sigma_{max}$ grows faster than $P$, so dividing the stress by F.S. leaves a much smaller margin on the load than F.S.; the factor must divide the load at first yield (Beer §10.2).

**A5.** Part D: maximum «D_P» kN ($\sigma$ = «D_s» MPa) at $L/r$ = «D_sl», reached at a lateral deflection of «D_dmax» mm. Euler: «D_PE» kN ($\sigma_{cr}$ = «D_sE» MPa > $\sigma_Y$), «D_Eo» % high; $\sigma_YA$ = «D_PY» kN, «D_Yo» % high; tangent modulus (Eq. 9): «D_Pt» kN ($\sigma_t$ = «D_st» MPa, $E_t$ = «D_Et» GPa), «D_to» % high; reduced modulus «D_Pr» kN; 1.95 × the AA allowable ($\sigma_{all}$ = «D_aa» MPa by Eq. 10.44b): «D_Paa195» kN, «D_aa_d» % from the measurement. On the column curve the pinned tests sit on Euler's hyperbola, the clamped tests sit on it at their measured $K$ (not at Beer's ideal), and Part D sits below the tangent-modulus curve. *Check:* at $L/r$ = 245 the tangent-modulus and Euler curves coincide. *Interpret:* only the tangent-modulus load, from the material's own curve, comes within 15 %; the bar's small bow and offset, amplified near the knee of the stress–strain curve, take the rest. The AA formula times its factor of safety lands near the measurement, as a design curve calibrated on real columns should.

**A6.** Table 5 rows are in Table K1. $E$ from the axial strain, «Eg_n» readings below half of each $P_{cr}$: «Eg» GPa («Eg_ag» with Lab 2; difference «Eg_d» GPa, limit «Eg_lim» GPa; intercept «Eg_icpt» µε). *Named causes for the systematic differences:* the Southwell loads and the strain-based $E$ both run high because the load cell reads 0.3 % high (inside its ±0.5 % specification) and Lab 2's $E$ is itself 0.6 % below the series' truth value; Part B's disagreement with Beer's $K$ is the clamps' finite stiffness, quantified by $k$.

**M1.** (a) Euler overstates the Part D load by «D_Eo» %; it predicts more than $\sigma_Y$ below $L/r$ = «D_slY». (b) Fixed ends are unconservative by «Bff_over» % (fixed–fixed) and «Bfp_over» % (fixed–pinned); $K$ comes within 1 % of 0.5 only for $kL/EI$ of about «M1_k1» or more, more than four times these clamps. (c) At $\delta = L/60$ a perfect pinned column carries only «M1_L60» % more than $P_{cr}$ (and 1.3 % at $L/10$); the 450 mm bar would first yield at $\delta$ ≈ «M1_yd» mm. (d) Eq. 10.37 overstates the first-yield load for $e$ = 2 mm by a factor of «PYo2». (e) The knife edges are about «eeq_mean» mm off the axis. *Ranking:* (d) and (a) are gross errors for the cases they touch; (b) is a 4–9 % unconservative error hidden in every design that assumes fixed ends; (e) is a 0.1 mm imperfection that Southwell absorbs; (c) is negligible in this lab's range.

## 4. Challenge and Extension solutions

**C1.** Bending-strain Southwell for the 450 mm bar: $P_{cr}$ = «C1_PS» N, «C1_d» % from the dial-gage fit; the intercept, «C1_eps0» µε, is the bending strain of the equivalent bow. Strain gages work on columns too stiff or too short for a dial gage, and on structures where the deflection cannot be reached.

**C2.** $k = -2xEI/(L\tan x)$ with $x \propto \sqrt{P}$ gives $(dk/k)/(dP/P) = \tfrac12[1 - x/(\sin x\cos x)]$ = «C2_sens» at $x$ = «C2_x»: a 1 % error in $P_{cr}$ is a «C2_sens» % error in $k$. The fixed–pinned test is even more sensitive (about «C2_fp»; its own $k$ would be «k_fp» N·m/rad). Better: a shorter fixed–fixed bar (smaller $kL/EI$, $x$ further from $\pi$), or a direct moment–rotation test of the clamp, as in Lab 7.

**C3.** A constant moment $M_0$ on $0 < x < L$ has the first sine coefficient $(4/\pi)M_0$; with $M_0 = Pe$ it acts on the first mode like a bow of $(4/\pi)e$. Southwell on the raw Part C data gives $\delta_0$ = «C1_swd0» and «C2_swd0» mm ($P_{cr}$ = «C1_swP» and «C2_swP» N); subtracting Part A's 450 mm intercept and multiplying by $\pi/4$ gives «C1_swe» and «C2_swe» mm, close to the grooves.

**X1.** Appendix D.3. Limits: $k \to 0$ in Eq. 3 gives $\tan(pL/2) \to \infty$, $pL = \pi$ (Eq. 10.11a); $k \to \infty$ in Eq. 4 gives $\tan pL = pL$ (Eq. 10.19).

**X2.** With $\theta$ the slope, $EI\theta'' + P\sin\theta = 0$; integrating once with zero moment at the pins and once more over the half length gives $\sqrt{P/EI}\,L/2 = K(k)$ with $k = \sin(\theta_0/2)$, so $P/P_{cr} = (2K/\pi)^2$; the lateral deflection is $\delta = 2k/p$, so $\delta/L = k/K(k)$. For small $k$, $K \approx (\pi/2)(1 + k^2/4)$, giving $P/P_{cr} - 1 \approx k^2/2 \approx (\pi^2/8)(\delta/L)^2$. A deflection of $L/10$ raises the load only «M1_L10» %: the column has essentially no reserve after buckling, unlike a plate, whose membrane stresses stiffen it.

**X3.** In the simulation the nearly perfect 90 mm bar stays straight up to the tangent-modulus load, then bends while the load still rises a little toward the reduced-modulus load; at the tangent-modulus load no fiber has to unload, which is why bending starts there (Shanley). Any imperfection makes the column bend earlier, and the maximum falls below $P_t$ (A5).

## 5. Design problem D1: reference solution

| Tube | Mass (kg/m) | $D_o/t$ | $L/r$ (pinned) | Allowable load, pinned (kN) | First yield, $e$ = 2 mm, pinned (kN) | OK, pinned? | Allowable load, $K$ = 0.52 (kN) | OK with $K$ = 0.52? |
|------------------|-------:|------:|------:|------:|------:|-----|------:|-----|
«D1_table»

: Table K4. D1 candidates, lightest first. Requirements: allowable load ≥ 12 kN; first yield ≥ «D1_req» kN (1.95 × 12 kN); $D_o/t$ ≤ 40. Lab 2 $E$ and Lab 1 $\sigma_Y$.

**D1 — reference design: «D1_best»**, «D1_m» kg/m, pinned ends ($K$ = 1, gussets bolted, free to rotate in their plane). $A$ = «D1_A» mm², $I$ = «D1_I» × 10³ mm⁴, $r$ = «D1_r» mm, $L/r$ = «D1_sl» (Euler branch, Eq. 10.45b): $\sigma_{all}$ = «D1_sall» MPa, allowable load «D1_Pall» kN ≥ 12 kN. $P_{cr}$ = «D1_Pcr» kN; secant first yield with $e$ = 2 mm: «D1_PY» kN ≥ «D1_req» kN (this governs, with a 4 % margin); at the service load $y_{max}$ = «D1_ymax» mm and $\sigma_{max}$ = «D1_smax» MPa. $D_o/t$ = «D1_Dt». **The trap:** with $K$ = 0.52 taken from Part B's clamps, the lightest tube that passes is «D1_trap» («D1_tm» kg/m, «D1_save» % lighter: $L_e/r$ = «D1_tsl», allowable «D1_tPall» kN). With the gussets' true pinned behavior its $L/r$ is «D1_tpsl», its allowable load «D1_tpPall» kN and its Euler load **«D1_tpPcr» kN, below the 12 kN service load: it would buckle.** A student who applies F.S. to the stress instead of the load (solving $\sigma_{max} = \sigma_Y/1.95$) gets «D1_PstFS» kN for the reference tube instead of «D1_PYFS» kN, a large unconservative error. *Assumptions that could invalidate a design:* bolted gussets with in-plane fixity (would justify $K < 1$, but only with a measured stiffness); out-of-straightness larger than the 2 mm allowance (rule of thumb $L/1000$ = 2 mm here); local buckling or crushing at the bolt holes; welding near the ends (heat-affected 6061 loses roughly half its yield strength).

**Rubric detail (15 points in the report).** Section properties, $L/r$, allowable load (3); secant first-yield load solved correctly with F.S. on the load (4); $K$ chosen and justified from the end detail and Part B (3); comparison of alternatives including the $K$ = 0.52 trap (4); presentation and one assumption with a check (1). Typical partial credit: Euler with $L_e = L$ but no design formula (−2); F.S. applied to the stress (−3); $K$ = 0.5 or 0.52 for bolted gussets without justification (−3 and the design fails); $D_o/t$ not checked (−1).

## 6. Expected ranges for real class data

| Quantity | Expected | If outside, suspect |
|------------------------------|--------------|------------------------------------------------------|
| Southwell / Euler, pinned | 0.97–1.04 | wrong axis of $I$ (×16); lengths measured to the bar ends instead of the pivots; low readings included in the fit |
| Southwell $\delta_0$ (mm) | 0.2–1.0 | dial not zeroed at no load; bar seated off the groove center |
| Slope, $\log P_{cr}$ vs $\log L$ | −1.9 to −2.1 | one bar's lengths or bow mis-recorded |
| $K$, fixed–fixed | 0.51–0.60 | clamp bolts loose (K → 0.6 or more); bar not bottomed in the clamp |
| Clamp stiffness $k$ (N·m/rad) | 1500–6000 | very sensitive to $P_{cr}$ (C2); compare the fixed–pinned prediction |
| Fitted eccentricity (mm) | 0.9–1.1, 1.9–2.1 | raw readings fitted without subtracting Part A (A3) |
| Part D maximum / tangent-modulus load | 0.80–0.95 | seat misalignment (lower); bar ends not square |
| $E$ from the axial strain (GPa) | 67–70 | gages off mid-length or not opposite each other; gage factor set wrong |

: Table K5. Expected data ranges.

## 7. Common student mistakes

1. Using the strong-axis $I = tb^3/12$: $P_{cr}$ 16 times too large.
2. Calling the last load recorded the "buckling load": the readings stop at «last_lo»–«last_hi» of $P_{cr}$ by design.
3. Fitting the Southwell line through every reading: the low-load points (seating, zero offsets, higher modes) bend the plot; use $P \ge 0.5P_{cr}$.
4. Comparing the raw Part C deflections with Eq. 7: the bow and the knife-edge offset are still in them, and the fitted $e$ comes out «C1_raw» and «C2_raw» mm instead of about 1 and 2 mm.
5. Applying the factor of safety to the stress in the secant formula (D1: «D1_PstFS» kN instead of «D1_PYFS» kN).
6. Taking $K$ = 0.5 for any "fixed" end: Part B's clamps give «Bff_K», and bolted gussets are closer to pinned.
7. Using Euler's formula for Part D ($\sigma_{cr}$ = «D_sE» MPa > $\sigma_Y$).
8. Adding the bow twice in the strain check of A3, or forgetting that the dial reads the change of deflection, not the total.
9. Reading the front gage's sign change (it turns tensile once the bow plus the deflection exceeds $t/6$) as a faulty gage.

## 8. Grading rubric

| Part | Points | Full credit | Common deductions |
|-------------|------:|------------------------------------------------|------------------------------------|
| Pre-lab | 15 | P1–P6 correct with units; P3 fitted, P4 compared with no deflection | weak-axis $I$ wrong (−4); P6 without a number (−2) |
| Data & procedure | 10 | Tables 3–4 complete; checks recorded | bows not measured (−2); front face not marked (−1) |
| A1 | 9 | Southwell fits with $U$; Euler compared; slope and $E$ | no uncertainty (−3); fit includes low loads (−2) |
| A2 | 8 | $K$ for both tests; $k$ from Eq. 3; Eq. 4 prediction compared | $k$ not found (−4); no prediction (−3) |
| A3 | 8 | Part A subtracted; $e$ fitted; lever-arm check; superposition ratio | raw data fitted (−4) |
| A4 | 7 | first-yield loads by Eq. 8 and Eq. 10.37; stress check at the last common load | F.S. on stress in the interpretation (−3) |
| A5 | 7 | Part D vs four predictions; all tests on the column curve | Euler only (−4) |
| A6 | 6 | Table 5 complete; normalized plot; every discrepancy explained | unexplained discrepancy (−2 each) |
| M1 | 10 | (a)–(e) with numbers and a ranking | no ranking (−2) |
| D1 | 15 | see Section 5 | |
| Communication | 5 | labeled axes, units, $x \pm U$ format | |
| Challenge | +10 | C1, C2, C3 (about 3 each) | |

: Table K6. Grading rubric (100 points plus up to 10 Challenge points). Core analysis A1–A6 totals 45.

Every Core answer must include the required check and interpretation; deduct 1 point per question where either is missing.

## 9. Instructor notes

**Before the lab.** Cut the bars from the Lab 2 stock: 300, 450 and 600 mm between pivot lines (the knife-edge seats are at the bar ends), 680 mm for Part B and 90 mm for Part D; square the ends. Bond a gage at mid-length on each wide face of the A and B bars, centered across the width, and wire quarter bridges. Check that the V-grooves at 1.00 and 2.00 mm are on the side opposite the dial gage. Torque the clamp bolts to the same value every session; $k$ depends on it.

**Timing (2 h).** 0:00–0:10 safety and measurements; 0:10–0:55 Part A (about 15 min per bar); 0:55–1:20 Part B; 1:20–1:45 Part C; 1:45–1:55 Part D demonstration (one per session, in the UTM); 1:55–2:00 simulation predictions. If time is short, run only the 450 mm bar in Part A (it is reused in Part C) and use the sample data for the others.

**Safety.** The bars are elastic throughout (largest stress about «P6_true_pct» % of $\sigma_Y$) and are reused; Part D destroys one 90 mm bar per session. A bar that slips from a knife edge springs sideways: keep the guard on and hands out of the frame under load.

**Running without equipment.** Give students `sample_data.csv` and Appendix A; Sections 3–5 of this key apply unchanged. **Your own class data:** export the columns listed in Table A1, fill in `src/specimen_measurements.json` with the class's dimensions, lengths and bows, and run `src/lab09_analysis.py` and `src/make_key.py`.

**The simulation** (P5, A5, D1) checks each closed form against an independent numerical method; its tests are in `tests/` and summarized in `tests/VERIFICATION.md`.

## 10. Self-critique and revisions

Before release, the lab was reviewed as a demanding instructor at a top program would review it. The three biggest weaknesses found, and the fixes made:

1. **The original procedure loaded in fixed steps of load, past the critical load.** A real bar cannot carry a load step above $P_{cr}$, and the first draft of the sample data recorded nonsense there. *Fix:* load steps up to 75 % of the predicted $P_{cr}$, then deflection steps of $L/600$ to $L/60$ (how a screw-loaded strut test is actually run); the data, the safety limits and the Southwell selection all follow this.
2. **Clamped ends were modeled as forcing a bowed bar straight at the clamp.** The fixed–pinned Southwell estimate came out 6 % low as a result. *Fix:* the finite-element model now solves for the change of deflection, so a clamp grips the bar at its initial slope and a spring resists only the change; the Southwell bias for clamped ends dropped below 0.3 %, and the generator, the page and the tests use the same formulation.
3. **The page's eigenvalue solver could converge to the wrong mode.** A symmetric start vector trapped inverse iteration in the second mode with one element (500 % error), and round-off in the stiffness quadratic form stalled the iteration at large $N$. *Fix:* a non-symmetric start vector and the quotient $x^TGx/x^TGz$; convergence is now a clean $N^{-4}$ for all ends.

**Known limitations (not fixed).** Both clamps are treated as equal (the truth model's differ by 5 %); knife edges are frictionless; Part D's half-sine fiber model slightly overstates the maximum load; the elastica correction at $L/60$ (negligible) and residual stresses are ignored; D1 checks local buckling only by $D_o/t$.

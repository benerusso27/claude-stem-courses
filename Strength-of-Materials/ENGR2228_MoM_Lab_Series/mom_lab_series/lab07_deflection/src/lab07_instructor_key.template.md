# Lab 7 — Instructor Key: Deflection of Beams

::: {custom-style="Instructor"}
**For instructors only. Do not distribute to students.** Every number in this key is computed by `src/lab07_analysis.py` (and `src/make_key.py`) from `sample_data.csv` and `src/specimen_measurements.json`, or by the simulation's own model code run in Node. To build a key for your own class data, put your CSV and measurements in the same format and run `python3 src/lab07_analysis.py your.csv your_measurements.json`, then `python3 src/make_key.py`. Uncertainties are expanded ($U = 2u$) unless marked $u$. Sign convention as in the handout (Beer 8e): $y$ up, $EI\,y'' = M$, $M > 0$ sags, loads down, couples and reaction couples counterclockwise positive; $\delta = -y$ is the downward deflection.
:::

## 1. Results at a glance (sample data)

| Quantity | Measured | Reference or prediction | Verdict (Eq. 12) |
|------------------------------|----------------|------------------------------|--------------------|
| Bar: $b$, $h$ (mm) | «bar_b», «bar_h» | 25.4 × 6.35 nominal | — |
| $E$ from six Part A compliances (GPa) | «A_E» | Lab 1: «ref_E» | «A_E_ag» |
| Both loads: $\delta$ at 200, 400, 600 mm (mm) | «A2_meas» | Eq. 3 from single-load data: «A2_pred» | «A2_ag» |
| $c_{13}$ vs $c_{31}$ (µm/N) | «A2_c13» | «A2_c31» | «A2_rec_ag» |
| B1: $EI$ (N·m²) | «B1_EI» | Part A: «A_EI» | «B1_EI_ag» |
| B1: clamp stiffness $k$ (N·m/rad) | «B1_k» | — | — |
| B2: $R_B/P$ | «B2_r» | 5/16 = 0.3125 (Eq. 5); «B2_rk» (Eq. 8 with $k$) | «B2_ag_rigid» with Eq. 5; «B2_ag_k» with Eq. 8 |
| B3: $\Delta R_B$ for 0.500 mm (N) | «B3_dR» | «B3_rigid» (Eq. 6); «B3_k» (Eq. 8) | «B3_ag_rigid» with Eq. 6; «B3_ag_k» with Eq. 8 |
| Strip $EI$, whole-curve fit (N·m²) | «C_EIfit» | linear, four points: «C_EIlin» | consistent |
| Strip $E$ (GPa) | «C_Efit» | 203 nominal | — |
| $\delta_v$ at 0.62 kg (mm) | «C_dv_last» | Eq. 10: «C_lin_last»; Eq. 9: «C_tip_last»; with weight: «C_w_last» | agrees only with the weight included |
| $\alpha$ where Eq. 10 is 5 % high | «C_a5m» (data, interpolated) | «C_a5» (Eq. 9) | — |
| D1 lightest section | «D_best» at $L_s$ = «D_best_Ls» m | without an overhang: «D_noover» | — |

: Table K1. Results from the sample data.

The sample data were generated from a known "truth" model (`src/generate_sample_data.py`, values in `src/truth.json`): $E$ = 205 GPa for the bar and 203 GPa for the strip; a clamp of rotational stiffness 4500 N·m/rad in Part B; supports, hangers and indicators a few tenths of a millimeter from their nominal positions; a prop lowered by 0.502 mm instead of 0.500; mass tolerance ±0.05 %; indicator noise 1.5 µm; load-cell noise 0.01 N and a +0.3 % gain error; grid-reading noise 0.25 mm; and the exact elastica with the strip's own weight. The closure tests in `tests/test_lab07_independent.py` confirm that the analysis recovers the truth values within their stated uncertainty.

## 2. Pre-lab solutions

Nominal values: bar 25.4 × 6.35 mm, $I$ = «P1_I» mm⁴, $E$ = 205.2 GPa, $EI$ = «P1_EI» N·m²; strip 12.7 × 0.79 mm, $I$ = «P1_Is» mm⁴, $E$ = 203 GPa, $EI$ = «P1_EIs» N·m².

**P1.** (a) $P$ = 3.0 × 9.807 = «P1_PA» N at $a$ = 0.6 m ($b$ = 0.2 m). Eq. 2 at $x$ = 0.2 and 0.4 m and its mirror image at 0.6 m: $\delta$ = «P1_dA» mm. Largest moment, under the load: $Pab/L$ = «P1_MA» N·m; $\sigma = Mc/I$ = «P1_sA» MPa, «P1_sAr» of $\sigma_Y$. (b) $\delta = PL^3/(3EI)$ = «P1_dB1» mm. (c) $R_B = 5P/16$ = «P1_RB» N for $P$ = «P1_PB2» N. (d) $\alpha$ = «P1_PC» × 0.25²/«P1_EIs» = «P1_alpha»; Eq. 10 gives $\delta_v$ = «P1_dC» mm, more than the strip's length of 250 mm: impossible, so Eq. 10 cannot apply at this load. Units: N·m²/(N·m²) for $\alpha$; N·m³/(N·m²) = m for $\delta$.

**P2.** Eq. 2 for 2.0 kg at 600 mm gives «P2_y1» mm at 400 mm; for 1.0 kg at 200 mm, «P2_y2» mm; Eq. 3: $\delta(400)$ = «P2_y» mm. For the pair 200/600 mm, $c_{12}$ (indicator 200, load 600) $= bx(L^2 - b^2 - x^2)/(6EIL)$ with $b = x$ = 0.2 m, and $c_{21}$ (indicator 600, load 200) is the mirror image with $a = L - x$ = 0.2 m: both equal $0.2 \cdot 0.2 \cdot 0.56/(6 \cdot 0.8\,EI)$ = «P2_c» µm/N.

**P3.** (a) Appendix D.2. (b) $R_B/P = (5/16 + 0.06)/1.12$ = «P3_r», above 5/16: a flexible clamp sheds moment to the prop. (c) $\Delta R_B = -3EI\Delta/L^3$ = «P3_dR» N with $L$ = 0.7 m and $\Delta$ = 0.5 mm.

**P4.** With $e = 1/EI$ and $f = 1/k$: $c(L/2) = \frac{5L^3}{48}e + \frac{L^2}{2}f$ and $c(L) = \frac{L^3}{3}e + L^2 f$. Then $c(L) - 2c(L/2) = L^3 e/8$, so $1/EI = 8[c(L) - 2c(L/2)]/L^3$ (the clamp term cancels), and $1/k = [16\,c(L/2) - 5\,c(L)]/(3L^2)$. The combination $16c(L/2) - 5c(L)$ is zero for a rigid clamp and isolates the clamp. It is a small difference of two large numbers (in the sample data «P4_frac» % of $16c(L/2)$), so $k$ needs both indicators read to the micrometer; this is why $k$ comes out with a «P4_uk» % uncertainty while $EI$ is good to «P4_uEI» %.

**P5.** Simulation, presets as shipped: "Part A: both loads": $\delta$ = «sim_A_both» mm at 200, 400 and 600 mm; the parts are «sim_A_600» mm (2.0 kg at 600 mm) and «sim_A_200» mm (1.0 kg at 200 mm). "Part B2": $R_B$ = «sim_B2_k» N with $k$ = 4400 N·m/rad and «sim_B2_rigid» N with a rigid clamp (5/16 of «sim_B2_P» N). "Part C" at 0.62 kg: $\delta_v$ = «sim_C_dv_w» mm and $\delta_h$ = «sim_C_dh_w» mm with the strip's weight, «sim_C_dv» and «sim_C_dh» mm without; linear theory is 5 % off at $\alpha$ = «sim_C_a5», i.e. at «sim_C_m5» kg.

**P6.** (a) A strip or clamp springing back under load (glasses; clamp and vise tightened before loading; weight lifted off before release; face out of the strip's plane); falling masses (add one at a time, feet clear); pinch points at the hangers and the prop (indicators set at zero load, no reaching across a loaded hanger). (b) The bar: 3.0 kg on each hanger gives at most «P6_sA» MPa in Part A, and the Part B limits «P6_sB1» MPa (B1) and «P6_sB2» MPa (B2), all below about one sixth of $\sigma_Y$ = 296 MPa, so the bar stays linear-elastic with a wide margin and the indicators stay within their travel. The strip: at 0.62 kg the root moment is «C_Mroot» N·m and the bending stress «C_sroot» MPa, «C_sroot_r» of the 1300 MPa minimum; heavier weights would approach yield at the clamp, where the strip would take a permanent set.

::: {.needspace lines="14"}
:::

## 3. Analysis solutions

| Load at | Indicator at | Compliance $c$ (µm/N) | App. F factor $f$ (×10⁻³ m³) | $E = f/(cI)$ (GPa) |
|-------:|-------:|----------------:|----------------:|----------------:|
«A1_table»

: Table K2. Part A compliances ($I$ = «A_I» mm⁴ from the measured $b$ and $h$).

**A1.** Table K2. The six values combine to **$E$ = «A_E» GPa** (mean; the spread of the six, «A_spread» GPa, is consistent with their uncertainties; the position and $I$ terms are common to all six and are kept in full). Lab 1: «ref_E» GPa: $|\Delta|$ = «A_dE» ≤ «A_lim», «A_E_ag». *Check:* $f$ is in m³ and $c$ in m/N, so $f/(cI)$ has units m³/(m/N · m⁴) = N/m². *Interpret:* the relative standard uncertainties of each coefficient are: positions set with the steel rule (span, hanger, indicator) «A1_uf» % through $f$, the compliance fit «A1_uc» %, $h$ «A1_uh» % (as $3u_h/h$) and $b$ «A1_ub» %. The positions limit the accuracy, mainly the span; $h$ is a minor term only because it was measured with a micrometer. With calipers (±0.02 mm), $3u_h/h$ would be «A1_hcal» % and would dominate. $h$ enters as $h^3$ in $I$; a tension test needs only $A = bh$ (Lab 1), so the same error in $h$ costs three times less there.

**A2.** Measured with both loads: «A2_meas» mm; superposed from the single-load compliances: «A2_pred» mm; differences «A2_diff» µm against limits «A2_lims» µm (Eq. 12): «A2_ag». App. F with $E$ from A1 gives «A2_theory» mm. Reciprocity: $c_{13}$ = «A2_c13» µm/N and $c_{31}$ = «A2_c31» µm/N; $|\Delta|$ = «A2_rec_d» ≤ «A2_rec_lim», «A2_rec_ag» (0.16 %). The two "middle" compliances, $c_{12}$ = «A2_c12» and $c_{32}$ = «A2_c32» µm/N, agree by the symmetry of the span, a different property. *Check:* past yield the moment–curvature relation is no longer linear (Lab 4), so neither superposition nor reciprocity holds: the deflection under both loads would exceed the sum. *Interpret:* reciprocity holds for any linear-elastic structure, whatever its supports; so an influence line can be measured by moving the indicator and keeping the load fixed (or the reverse), whichever is more convenient.

**A3.** From the B1 compliances $c(350)$ = «B1_cmid» µm/N and $c(700)$ = «B1_ctip» µm/N, P4 gives **$EI$ = «B1_EI» N·m²** and **$k$ = «B1_k» N·m/rad**. Part A gave «A_EI» N·m²: $|\Delta|$ = «B1_dEI» ≤ «B1_EI_lim», «B1_EI_ag». From the tip indicator alone with a rigid clamp: $EI$ = «B1_EIrigid» N·m², «B1_EIrigid_err» % low. *Check:* as $k \to \infty$ the second term of Eq. 7 vanishes and $\delta(L) = PL^3/(3EI)$, App. F case 1. *Interpret:* the clamp contributes «B1_share» % of the tip deflection; an unsuspecting student would report $E$ about «B1_Eunsusp» GPa and blame the material. In this test the clamp is a spring in series with the bar.

**A4.** Fit of $R_B$ against $P$: **$R_B/P$ = «B2_r»**. Rigid clamp (Eq. 5): 0.3125, $|\Delta|$ = «B2_drig», «B2_xU» times $U$: «B2_ag_rigid». Eq. 8 with $\lambda = EI/(kL)$ = «B2_lam» from A3: «B2_rk», $|\Delta|$ = «B2_dk» ≤ «B2_limk», «B2_ag_k». Mid-length deflection per newton: measured «B2_dslope» µm/N; rigid clamp «B2_drigid» µm/N; with $k$ «B2_dk_pred» µm/N ($|\Delta|$ = «B2_ddd» ≤ «B2_dlim», agree with $k$). Turned around, $R_B/P$ alone implies $k$ = «B2_kR» N·m/rad, consistent with A3. B3: **$\Delta R_B$ = «B3_dR» N**; Eq. 6 (rigid): «B3_rigid» N («B3_ag_rigid»); Eq. 8: «B3_k» N, $|\Delta|$ = «B3_dd» ≤ «B3_lim», «B3_ag_k». The indicator at 350 mm moved by «B3_ind» mm when the prop was lowered. *Check:* at $\lambda = 0$, Eq. 8 gives $(5/16)/1 = 5/16$; as $\lambda \to \infty$, $(3\lambda/2)/(3\lambda) = 1/2$, the value for a pin at A. *Interpret:* the beam is neither fixed nor pinned at A: the clamp is a rotational spring, and with it one parameter measured in B1 predicts two different quantities in B2 and B3. A 0.5 mm settlement changes $R_B$ by «B3_pct» % here; in a simple span (determinate) the reactions follow from statics alone and a settlement only tilts the beam.

| Mass (kg) | $\alpha$ | $\delta_v$ measured (mm) | Eq. 10 (mm) | Eq. 9 (mm) | With weight (mm) | $x_{tip}$ measured (mm) | With weight (mm) | Eq. 10 error (%) |
|------:|------:|------:|------:|------:|------:|------:|------:|------:|
«C_table»

: Table K3. Part C. $EI$ from the whole-curve fit; Eq. 10 and Eq. 9 columns include the zero-load sag «C_sag0» mm as an offset. Grid readings ±«C_Ugrid» mm ($U$).

**A5.** (a) First four points (0 to 0.07 kg): slope «C_slope» mm/N, **$EI$ = «C_EIlin» N·m²** ($L$ = «C_L» mm from the zero-load reading). (b) Table K3. Eq. 10 is 5 % high at $\alpha$ ≈ «C_a5m» in the data (Eq. 9: «C_a5»), and «C_lin_last_err» % high at 0.62 kg. Eq. 9 without the weight is within «C_tip_ok» mm of the data up to $\alpha \approx 1$, then «C_tip_last_d» mm high at 0.62 kg; the model with the weight matches every point within the grid uncertainty (χ² = «C_chi2» for «C_dof» degrees of freedom). The tip moves inward by «C_dh_last» mm at 0.62 kg. *Check:* at $\alpha$ = 0.25, Appendix E gives 0.0827 against $\alpha/3$ = 0.0833: Eq. 9 approaches Eq. 10. *Interpret:* as the strip rotates, the load's lever arm $x_{tip}$ shrinks, so the root moment grows less than in proportion to $P$ and the strip stiffens; at large $\alpha$ part of the load is carried by the strip in tension along its length, not in bending.

**A6.** Use Table K1. Expected verdicts: $E$, superposition and reciprocity agree; $R_B/P$ and $\Delta R_B$ disagree with the rigid-clamp formulas and agree with Eq. 8 using the measured $k$; $\delta_v$ at 0.62 kg disagrees with Eq. 10 by a factor of «C_factor», and with Eq. 9 without the weight by «C_tip_last_d» mm. Full credit needs Table 5 complete, a normalized figure with error bars, and each discrepancy explained with a named, quantified cause (the clamp's flexibility, large deflection, self-weight).

**M1.** (a) At 0.62 kg ($\alpha$ = «C_amax»), Eq. 10 overstates $\delta_v$ by a factor of «C_factor»; the tip slope is «C_th0» (exact model), where $(dy/dx)^2$ ≈ «C_slope2» rather than $\ll 1$. (b) Assuming a rigid clamp: $R_B$ «B2_rigid_pct» % low (5/16 vs «B2_r»), $\Delta R_B$ «B3_rigid_pct» % too large, $EI$ from the tip «B1_EIrigid_err» % low. (c) The weight adds «C_w12» mm to $\delta_v$ at 0.12 kg and «C_w62» mm at 0.62 kg, against «C_sag0» mm with no load: as the strip hangs more steeply, the weight's lever arms shrink. Adding the zero-load sag to the tip-load elastica would be «C_tip_last_d» mm wrong at 0.62 kg. The data resolve it: the differences exceed the grid $U$ of «C_Ugrid» mm (barely at 0.62 kg). (d) With the simulation's shear term $12 f_s EI/(GAL^2)$ for a central load, shear deformation adds 5 % at a span of «M1_Lsh_bar» mm for the Part A bar (span/depth «M1_Lsh_bar_r») and «M1_Lsh_D1» m for the D1 section; at the actual spans it adds «M1_sh_bar» % (Part A) and «M1_sh_D1» % (D1 at 3.05 m). *Rule:* Part A is limited by nothing in the model (the bar is long, stiff and lightly stressed); Part B by the support model; Part C by small slopes, with self-weight second.

## 4. Challenge and Extension solutions

**C1.** "App. F case 5": the error is at round-off level («C1_F5_err») for every mesh, because the exact solution is piecewise cubic and the mesh has a node under the load; $EI\,y''$ is exact too. "App. F case 6": the nodal deflections are exact for every $N$; the largest error between nodes falls as $N^{-«C1_F6_sy»}$ and the moment from $EI\,y''$ at element midpoints as $N^{-«C1_F6_sM»}$. Reason (Appendix D.6): the Hermite element reproduces any cubic, which is the exact solution of $EIy'''' = 0$, and the consistent load vector makes the nodal values exact; between nodes the cubic misses the quartic part of the uniform-load solution, an error of order $h^4$ in $y$, and differentiating twice costs $h^2$.

**C2.** Whole-curve fit with the weight: **$EI$ = «C_EIfit» N·m²**, $E$ = «C_Efit» GPa; the four-point linear value «C_EIlin» N·m² is «C_linbias» % higher, within the uncertainties. Linear theory overstates the deflection already at 0.07 kg ($\alpha$ = «C_a4»), so the fitted slope is too small and $EI$ too large. The strip's thickness dominates the uncertainty of $E$ ($3u_t/t$ = «C_t_pct» %).

**C3.** At 4.0 kg, $R_B$ = «C3_R» N, so 5 % is «C3_dR» N. With the A3 values, $L^3/(3EI) + L^2/k$ = «C3_flex» mm/N, and the prop height error that changes $R_B$ by 5 % is «C3_D» mm, about «C3_ratio» times the 0.002 mm criterion of step 4. The criterion is conservative for this flexible bar; it matters for stiff beams (Eq. 6 scales with $EI/L^3$), and for the "just touching" condition itself, which defines the zero of the load cell.

**X1.** Appendix D.5. For small $\alpha$, expanding the elliptic integrals (or perturbing $\theta = \alpha\theta_1 + \alpha^3\theta_3$ in $EI\theta'' = -P\cos\theta$) gives $\theta_0 = \alpha/2 - 11\alpha^3/240$, $\delta_v/L = \alpha/3 - 4\alpha^3/105$ and $\delta_h/L = \alpha^2/15$ (confirmed numerically by `make_key.py`: «X1_c3», «X1_t3» and «X1_h2» at $\alpha$ = 0.01). The leading terms are Eq. 10 and the App. F slope $PL^2/(2EI)$. The inward motion is of second order in $\alpha$, which is why linear theory has none; the first correction to $\delta_v$ is of third order, so Eq. 10 stays good to 1 % up to $\alpha$ = «X1_a1».

**X2.** Appendix D.3. From Eq. 7 extended to a load at $a$: $\delta(x = L) = Pa^2(3L - a)/(6EI) + Pa L/k$ for $a$ = 0.35 m, and $\delta(x = 0.35) = Px^2(3L - x)/(6EI) + PLx/k$ for the tip load: the two expressions are identical term by term, so with the B1 values both give «X2_c» µm/N, the measured $c(350)$. The clamp term is symmetric in $a$ and $x$ ($PaL/k$ vs $PLx/k$), so reciprocity survives the spring.

**X3.** In `solveBeam()`, where a fixed support locks its rotation, replace the lock by a spring when $k$ is finite: `if (std::isfinite(s.k)) K(2*n+1, 2*n+1) += s.k; else lock(2*n+1);`, and report the spring moment as `-s.k * u[2*n+1]`. With the B1 values ($EI$ = «B1_EI» N·m², $k$ = «B1_k» N·m/rad) the extended program gives «X3_tip» mm at the tip and «X3_mid» mm at 350 mm under 1.0 kg, the measured «X3_meas» and «X3_mid_meas» mm. That agreement is exact by construction ($EI$ and $k$ were found from these two readings); the real test is Part B2, where the same $k$ predicts $R_B/P$ = «B2_rk» against «B2_r» measured. The simulation contains exactly this extension (marked `[extension]` in its source).

## 5. Design problem D1: reference solution

**D1.** $\sigma_{allow}$ = 0.6 × 273.7 = «D_sa» MPa; $E$ = 68.46 GPa (Lab 2). For each section, $L_s$ from 2.50 to 4.00 m in 0.05 m steps; largest $|M|$ from statics, span deflection from App. F cases 6 and 7, tip from the end slope plus cases 1 and 2 for the overhang (Table K4).

**Reference design: «D_best», roller at $L_s$ = «D_best_Ls» m** (overhang «D_best_a» m), «D_best_m» kg/m. Reactions $R_A$ = «D_RA» N, $R_B$ = «D_RB» N (check: sum «D_sum» N = 2.0 × 4.0 + 1.5 kN). Moment: largest hogging at the roller, $M_B = -(wa^2/2 + Pa)$ = «D_MB» N·m; largest sagging «D_Mpos» N·m at $x = R_A/w$ = «D_xpos» m. Stress «D_s» MPa («D_rs» of the allowable). Span deflection by superposing case 6 ($w$ on $L_s$: «D_y6» mm at the location of the largest deflection) and case 7 (end couple $M_B$: «D_y7» mm): «D_ys» mm (limit «D_ys_lim» mm). Tip: end slope «D_thB» × 10⁻³ rad × $a$ = «D_tip_rot» mm (almost zero: at this roller position the overhang's moment nearly balances the span's load), plus case 1 «D_tip_P» mm and case 2 «D_tip_w» mm: «D_yt» mm (limit «D_yt_lim» mm). The feasible window is narrow: below «D_best_Ls» m the tip deflection governs, above «D_best_hi» m the span deflection. The simulation's preset uses $E$ = 68.9 GPa, so its deflections are 0.6 % smaller; accept either if stated. Without an overhang the lightest section is «D_noover» («D_noover_m» kg/m, «D_noover_ratio» times the mass): the overhang's hogging moment relieves the span. *Assumptions that could invalidate a design:* the railing post at the very tip (a post inboard changes the balance); load patterns (live load on the span only, or on the overhang only, can lift the tip or raise the span deflection: a full design checks them); lateral-torsional buckling of the compression flange over the roller, where the bottom flange is in compression and unbraced (Lab 9 territory).

| Section | $I$ (10⁶ mm⁴) | Mass (kg/m) | Feasible $L_s$ (m) | Stress ratio | Span deflection ratio | Tip deflection ratio |
|------------------|-------:|-------:|--------------------|--------:|----------:|----------:|
«D_table»

: Table K4. D1 candidates. Ratios: $\sigma/\sigma_{allow}$, $\delta_{span}/(L_s/360)$ and $\delta_{tip}/(2a/360)$, at the best roller position for each section (all ratios ≤ 1 there if feasible; otherwise at the position that minimizes the largest ratio).

**Rubric detail (15 points total in the report).** Reactions, moment diagram and section properties (3). Hand superposition matching the simulation within 1 % (3.75). All three checks with the student's own $E$ and $\sigma_Y$ and the governing one named (3). At least three sections or roller positions compared quantitatively (3.75). Presentation and assumption (1.5). Typical partial credit: tip deflection not checked (−3); stress taken at the span's sagging maximum instead of the roller (−2); the overhang's moment at the roller entered with the wrong sign in case 7 (−2).

::: {.needspace lines="16"}
:::

## 6. Expected ranges for real class data

| Quantity | Expected | If outside, suspect |
|------------------------------|--------------|------------------------------------------------|
| $E$ from Part A (GPa) | 200–210 | $h$ by calipers; span measured to the wrong edge of the knife edges; indicator not over the bar's centerline |
| $c_{13}/c_{31}$ | 0.99–1.01 | hanger or indicator position error; bar not centered |
| Clamp share of the B1 tip deflection | 5–20 % | loose clamp (> 25 %); clamp edge not where $L$ is measured from |
| $R_B/P$ in B2 | 0.32–0.35 | prop not "just touching" at zero load; load cell not tared |
| $\Delta R_B$ for 0.5 mm (N) | −0.40 to −0.47 | prop screw backlash; reading taken before the load cell settled |
| Strip $E$ (GPa) | 195–210 | thickness by calipers; length from the rule instead of the grid |
| $\alpha$ where Eq. 10 is 5 % high | 0.6–0.8 | parallax in the grid readings; strip twisted in the vise |

: Table K5. Expected data ranges.

## 7. Common student mistakes

1. Taking the deflection positive downward without saying so, then writing $EI\,y'' = -M$ in one place and $+M$ in another.
2. Using the total mass on the hanger instead of the mass added after zeroing (Part A and B), or forgetting the 0.020 kg hanger in Part C.
3. Using the $x \le a$ branch of Eq. 2 for an indicator beyond the load.
4. Treating the clamp as rigid in B1, which gives $E$ about 10 % low, and calling it "experimental error".
5. Comparing $R_B$ with 5P/16 only, without asking why the gap exceeds $U$.
6. Mixing units in Eq. 6 ($\Delta$ in mm with $EI$ in N·m²), giving an answer 1000 times too large.
7. Applying $\alpha/3$ at every Part C load, or measuring the strip's length with the rule after it has deflected.
8. Measuring the strip's thickness with calipers: ±0.02 mm on 0.79 mm is 7.6 % in $E$.
9. In D1, checking only the span (not the tip, which can deflect upward for long overhangs), or taking the stress at the span's sagging maximum instead of over the roller.
10. Adding the zero-load sag to the large-deflection tip deflection, as if self-weight superposed.

::: {.needspace lines="24"}
:::

## 8. Grading rubric

| Part | Points | Full credit | Common deductions |
|----------------|------:|----------------------------------------------------------|------------------------------|
| Pre-lab | 15 | P1–P6 correct with units; P1 an estimate made before measuring | P1(d) not compared with $L$ (−2) |
| Data & procedure | 10 | Tables 3–4 complete; checks recorded | $h$ not by micrometer (−3) |
| A1 | 9 | six values of $E$ with $U$, combined, compared with Lab 1 | no position uncertainty (−2) |
| A2 | 7 | superposition at three points and reciprocity, plot | no plot (−2) |
| A3 | 8 | $EI$ and $k$ with $U$; rigid-clamp comparison | rigid clamp assumed (−5) |
| A4 | 9 | $R_B/P$ and $\Delta R_B$ against both models | only Eq. 5 (−4) |
| A5 | 7 | $EI$ from the slope; three models plotted against $\alpha$ | no $x_{tip}$ comparison (−2) |
| A6 | 5 | complete table, normalized figure, every discrepancy explained | unexplained discrepancy (−1 each) |
| M1 | 10 | (a)–(d) with numbers and a stated rule | (d) missing (−2) |
| D1 | 15 | see Sec. 5 | see Sec. 5 |
| Communication | 5 | labeled axes, units, $x \pm U$ format | each unlabeled axis (−1) |
| Challenge | +10 | C1 (3), C2 (3), C3 (4) | — |

: Table K6. Grading rubric (100 points plus up to 10 Challenge points). Core analysis A1–A6 totals 45.

Every Core answer must include the required check and interpretation; deduct 1 point per question where either is missing.

## 9. Instructor notes

**Before the lab.** The bar: 1018 hot-rolled flat (the Lab 1 material, so that Table 1 applies), 25.4 × 6.35 × 1000 mm, straight to 0.5 mm over its length and free of loose scale where the indicators bear (a cold-drawn bar also works, but its yield strength is higher than Table 1); mark 200, 400, 600 mm from one end with a scribe. The frame: two knife edges on a rail, a bench clamp with a hardened jaw edge (the edge defines $x$ = 0 in Part B), and a roller prop on a 50 N load cell with a micrometer screw (or a fine-thread bolt with a dial indicator). Three 0.001 mm digital indicators on magnetic stands. The strip: blue-tempered spring steel shim 12.7 × 0.79 mm (0.031 in), 300 mm long, with a 3 mm hole drilled 250 mm from the vise jaws (drill it before hardening, or use an S-hook over the end); a grid board with 10 mm squares behind it, and a square to sight across.

**Timing (2 h).** 0:00–0:10 safety and pre-lab; 0:10–0:20 dimensions; 0:20–0:50 Part A; 0:50–1:25 Part B (clamping, B1, prop, B2, B3); 1:25–1:50 Part C; 1:50–2:00 simulation (step 7). If time is short, skip the 200 mm single-load run in Part A (reciprocity then uses the both-loads run and P2), or use the sample data for Part C.

**Safety.** The strip stores energy: the most likely injury is a strip slipping out of the vise. Inspect the vise jaws, and have students lift the weight before touching the vise. The prop must never carry load while being adjusted beyond the B3 step.

**Running without equipment.** Give students `sample_data.csv` and Appendix A; everything in this key applies unchanged. A good hybrid is to run Parts A and B live and use the sample data for Part C.

**Your own class data.** Export the columns listed in Table A1; fill a measurements JSON like `src/specimen_measurements.json`, with the class's Lab 1 and Lab 2 values in `reference`; run `src/lab07_analysis.py` and `src/make_key.py`.

**The simulation and the C++ program.** Students use the simulation in P5, step 7, A5, M1, C1 and D1. Its finite-element solver is the instructor's `beam_deflection.cpp` (in `reference/`), ported line by line and extended with a clamp spring and a settlement; `tests/test_lab07_model.js` compiles the C++ and compares the two at every node for ten beams (bit-identical). The readout separates verification rows ("agree") from model comparisons ("different models"); all tests are summarized in `tests/VERIFICATION.md`.

## 10. Self-critique and revisions

Before release, the lab was reviewed as a demanding instructor at a top program would review it. The three biggest weaknesses found, and the fixes made:

1. **A simple-span deflection test only re-confirms App. F,** a verification with nothing at stake. *Fix:* Part B makes the beam indeterminate with a real bench clamp. The textbook value 5P/16 is then measurably wrong («B2_rigid_pct» % low), two indicators in B1 measure the clamp as a rotational spring, and that one measured $k$ predicts two other quantities ($R_B/P$ and $\Delta R_B$) within their uncertainty: a model refined from data and tested on independent measurements.
2. **Small-deflection theory was never pushed to failure.** *Fix:* Part C bends a spring-steel strip until Eq. 10 is «C_lin_last_err» % high. The exact elastica, tabulated in Appendix E and computed two ways in the simulation, matches the data only when the strip's weight is included, and M1 shows that the weight does not superpose at large deflection. The measured 5 % point («C_a5m») is close to the theoretical «C_a5».
3. **The simulation's "independent" numerical method would be meaningless if the instructor's C++ program were only paraphrased.** *Fix:* the page ports the C++ solver line by line; the Node tests compile the original and compare the two at every node for ten beams (identical to the last bit); the two extensions (clamp spring, settlement) are tested against the closed forms and against an independent double integration in Python.

**Known limitations (not fixed).** The indicators push on the bar with about 1 N; zeroing at no load removes it from the increments, but in B2 it slightly preloads the prop. The clamp is modeled as a linear spring; a real clamp can have a small dead zone before it grips, which would show up as a nonzero intercept in B1. Knife-edge friction and the bar's initial curvature are ignored. The strip is 16 times as wide as it is thick: at the root at 0.62 kg, $b^2/(\rho t)$ reaches about «C_searle», where the anticlastic curvature starts to be restrained and the strip stiffens toward the plate value $EI/(1 - \nu^2)$, up to 9 %; the truth model ignores it, and real data may show $E$ a few percent high from the largest loads.

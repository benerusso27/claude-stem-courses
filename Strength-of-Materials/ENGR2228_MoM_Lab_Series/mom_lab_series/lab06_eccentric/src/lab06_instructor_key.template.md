# Lab 6 — Instructor Key: Eccentric Axial Loading

::: {custom-style="Instructor"}
**For instructors only. Do not distribute to students.** Every number in this key is computed by `src/lab06_analysis.py` (and `src/make_key.py`) from `sample_data.csv` and `src/specimen_measurements.json`, or by the simulation's own model code run in Node. To build a key for your own class data, put your CSV and measurements in the same format and run `python3 src/lab06_analysis.py your.csv your_measurements.json`, then `python3 src/make_key.py`. Uncertainties are expanded ($U = 2u$) unless marked $u$. Sign convention as in the handout (Beer 8e): $y$ up, $z$ to the left in section views, tension positive, Eq. 4.58 in principal axes with $M_y = Pz_P$, $M_z = -Py_P$; beam-column deflection measured toward the load line.
:::

## 1. Results at a glance (sample data)

| Quantity | Measured | Reference or prediction | Verdict (Eq. 15) |
|------------------------------|----------------|------------------------------|--------------------|
| Bar: $h$, $b$ (mm) | «bar_h», «bar_b» | 50.8 × 12.7 nominal | — |
| $e_{eff}$ at 30 kN, hole $h/3$ (mm) | «A1_e2_eff» | hole «A1_e2_hole» (Eq. 1); $eC_{mid}$ «A1_e2_bc» (Eq. 9) | «A1_e2_a450» with Eq. 1; «A1_e2_abc» with Eq. 9 |
| $e_{eff}$ at 30 kN, hole $h/6$ (mm) | «A1_e1_eff» | hole «A1_e1_hole»; $eC_{mid}$ «A1_e1_bc» | «A1_e1_a450» with Eq. 1; «A1_e1_abc» with Eq. 9 |
| $E\varepsilon_0$ at 30 kN, hole $h/3$ (MPa) | «A1_e2_sig0» | $P/A$ = «A1_e2_PA» | «A1_e2_sig0_ag» |
| Out-of-plane bending, $e$ = 0 run | «A3_e0_pb» % ($e_z$ = «A3_e0_ez» mm) | — | — |
| Angle: G1, G2, G3, G4 at 30 kN | Table K4 | Eq. 8 | «B_nagree» of 4 agree with Eq. 8 alone; «B_nagree_bc» of 4 with fillet and Eq. 9 |
| Part C at 25 kN: $C_{mid}$ | «M1_Cm» | Eq. 9: «M1_Cp» | «M1_Ca» |
| Part C at 25 kN: $C_{end}$ (40 mm from the block) | «M1_Em» | Eq. 9: «M1_Ep» | «M1_Ea» |
| Part C at 25 kN: $w_{mid}$ (mm) | «M1_wm» | Eq. 9: «M1_wp» | «M1_wa» |
| $EI$ through the thickness from $w_{mid}$ (N·m²) | «C2_EI» | $E\,hb^3/12$: «C2_EIr» | «C2_a» |
| D1 lightest angle | «D_best» | $P/A$ alone would pick «D_naive» | — |

: Table K1. Results from the sample data.

The sample data were generated from a known "truth" model (`src/generate_sample_data.py`, values in `src/truth.json`): Eq. 4.58 in principal axes with every principal eccentricity reduced by the beam-column factor of Eq. 9 (rigid end blocks, $E$ = 68.9 GPa), a root fillet of 4.8 mm on the angle, hole positions within ±0.05 mm of the reported values, an out-of-plane misalignment of 0.15 mm in the Part A runs, a common +0.3 % and a random ±0.3 % gage-factor error, 1.5 µε noise, +0.2 % load-cell and +0.3 % LVDT gain errors. The closure test in `tests/test_lab06_independent.py` confirms that the analysis recovers the truth values within their stated uncertainty. Because Eqs. 11 and 12 are ratios, the common gage-factor, load and $E$ errors cancel in $e_{eff}$ and $C$.

## 2. Pre-lab solutions

**P1.** (a) $A$ = «P1_A» mm², $P/A$ = «P1_PA» MPa; with $e = h/3$, $6e/h = 2$: $\sigma_{max}$ = «P1_smax» MPa at $y = +h/2$, $\sigma_{min}$ = «P1_smin» MPa at $y = -h/2$. Neutral axis $y_0 = -(h^2/12)/(h/3) = -h/4$ = «P1_y0» mm. At $y$ = +20 mm, $\sigma$ = «P1_s20» MPa (≈ «P1_e20» µε); at −20 mm, «P1_sm20» MPa (≈ «P1_em20» µε). (b) $P/A$ = «P1_PAc» MPa and $6e/b = 3$: front «P1_sf» MPa («P1_ef» µε), back «P1_sb» MPa («P1_eb» µε). (c) $I_z$ = «P1_Iz» mm⁴, $I_y$ = «P1_Iy» mm⁴; $P_{cr}$ = «P1_PEz» kN across the width and «P1_PEy» kN through the thickness. $P/P_{cr}$ = «P1_rz» (Part A, 30 kN) and «P1_ry» (Part C, 25 kN): Eq. 10 says Part A is safe (about «P1_ez» %), Part C is not (about «P1_ey» % by the small-load estimate; Eq. 9 gives more, see M1). Units: N·mm²/mm² = N.

**P2.** At the edge $y = -h/2$, Eq. 2 gives $\sigma = (P/A)(1 - 6e/h)$, which is zero when $e = h/6$. Hole $e$ = 0: inside the kern, uniform stress. $h/6$: on its boundary, the neutral axis touches the far edge (stress zero there, $2P/A$ at the near edge). $h/3$: outside, the neutral axis is inside the bar at $-h/4$, with compression beyond it.

**P3.** Two rectangles (vertical leg $50.8 \times 6.35$, horizontal leg $44.45 \times 6.35$): $A$ = «P3_A» mm², centroid «P3_c» mm from both outer faces, $I_y = I_z$ = «P3_I» mm⁴, $I_{yz}$ = «P3_Iyz» mm⁴ (positive for the "L" of Figure 1: both legs' centroids lie in quadrants where $y$ and $z$ have the same sign). $I_u = I + |I_{yz}|$ = «P3_Iu» mm⁴, $I_v = I - |I_{yz}|$ = «P3_Iv» mm⁴, $\theta_p$ = «P3_th»° (the major axis runs through the heel and the centroid). Load point from the centroid: $y_P$ = «P3_yP», $z_P$ = «P3_zP» mm, so $u_P$ = «P3_uP» and $v_P$ = «P3_vP» mm. At 30 kN, $P/A$ = «P3_PA» MPa, and:

| Gage | $y$, $z$ from C (mm) | $u$, $v$ (mm) | Eq. 8 (MPa) | $I_{yz}$ ignored (MPa) |
|------|----------------|----------------|----------:|----------:|
«P3_table»

: Table K2. Pre-lab P3 (nominal angle).

Ignoring $I_{yz}$ moves the neutral axis and gets G2 and G4 badly wrong (and overstates G1's compression); G3 is nearly right by coincidence, because it sits close to where the two stress planes cross.

**P4.** Eq. 2: $E\varepsilon = (P/A)(1 + ey/r_z^2)$ is linear in $y$ with intercept $P/(EA)$ and slope $Pe/(EAr_z^2)$; their ratio times $r_z^2$ is $e$, and $E$, a common gage-factor error and the load scale both terms equally (Appendix D.5). A front-minus-back difference that is the same at all heights is bending through the thickness, an out-of-plane offset of the load line. A difference that varies with $y$ would mean twisting of the bar (or a gage-position error), which the out-of-plane offset alone cannot produce.

**P5.** Simulation, presets as shipped ($E$ = 68.9 GPa in the page): Part A, $h/3$: $\sigma_{max}$ = «sim_A2_smax» MPa, $\sigma_{min}$ = «sim_A2_smin» MPa, neutral axis at «sim_A2_y0» mm. Part B: G1–G4 = «sim_B» MPa from Eq. 8; the largest stress is «sim_Bmax» MPa with principal axes and «sim_Bn» MPa with $I_{yz}$ ignored. Part C at 25 kN: $C_{mid}$ = «sim_C_Cmid», $C_{end}$ = «sim_C_Cend», $w_{mid}$ = «sim_C_w» mm; Eq. 4 is 5 % off at «sim_C_P5» kN (the buckling load with the end blocks is «sim_C_Pcr» kN).

**P6.** (a) Pins walking out of the clevises (retaining clips, full insertion); pinch points at the grips and blocks (hands clear, jog with both hands); overload (overload stop); reaching past a loaded specimen to adjust the LVDT (set at zero load). (b) In tension Eq. 4 overstates the bending (Section 2.4), so a limit set with it is conservative. In compression the same offsets amplify the bending; the Part C bar would reach yield well below 25 kN, and the out-of-plane configuration would buckle at about «sim_C_Pcr» kN.

## 3. Analysis solutions

| Hole | $e_{eff}$ (mm) | Hole offset (mm) | Eq. 1 | $eC_{mid}$, Eq. 9 (mm) | Eq. 9 | $E\varepsilon_0$ (MPa) | $y_0$ (mm) | Bending out of plane (%) |
|------|----------------:|-------------:|----------|----------------:|----------|-------------:|----------:|--------:|
«A1_table»

: Table K3. Part A at 30 kN ($P/A$ = «A1_e2_PA» MPa).

**A1.** Table K3. $E\varepsilon_0$ agrees with $P/A$ in every run (the centric part is unaffected by the offset). For $h/3$: **$e_{eff}$ = «A1_e2_eff» mm** vs the hole «A1_e2_hole» mm: $|\Delta|$ = «A1_e2_d450» > «A1_e2_l450», «A1_e2_a450»; vs $eC_{mid}$ = «A1_e2_bc» mm: $|\Delta|$ = «A1_e2_dbc» ≤ «A1_e2_lbc», «A1_e2_abc». For $h/6$: «A1_e1_eff» vs hole «A1_e1_hole» («A1_e1_a450») and vs «A1_e1_bc» («A1_e1_abc»). At 30 kN Eq. 9 gives $C_{mid}$ = «A1_C» (in-plane, $P_{cr}$ = «bar_PEbs» kN with the blocks): the bar has straightened enough to cut the in-plane bending by «A1_drop» %, and the ratio method resolves it. In stress terms, Eq. 2 predicts «A1_sig_max450» and «A1_sig_min450» MPa at the edges; the fit gives «A1_sig_max» and «A1_sig_min» MPa. *Check:* for $e$ = 0, $e_{eff}$ = «A1_e0_eff» mm, consistent with the hole offset «A1_e0_hole» mm; $e_{eff} = r_z^2\beta/\varepsilon_0$ has units mm² × (1/mm) = mm. *Interpret:* the comparison tests the assumption that the deformation leaves the eccentricity unchanged. For this stocky bar the effect is a few percent, small but measurable, and it makes Eq. 1 slightly conservative.

**A2.** Table K3. With the hole offset (Eq. 3): $y_0$ = «A2_e2_p» mm ($h/3$) and «A2_e1_p» mm ($h/6$, at the edge «A2_edge» mm); with $eC_{mid}$: «A2_e2_pbc» and «A2_e1_pbc» mm. Measured: «A2_e2_y0» and «A2_e1_y0» mm. *Check:* $y_0\,e_{eff}$ = «A2_e2_prod» mm² ($h/3$) and «A2_e1_prod» mm² ($h/6$), both equal to $-r_z^2$ = «A2_r2» mm² as Eq. 3 requires. *Interpret:* for $h/6$ the measured neutral axis lies just **outside** the bar, because the straightening reduced the effective eccentricity below $h/6$: the load is effectively inside the kern and the whole section stays in tension. Unreinforced masonry has almost no tensile strength, so a compressive load must stay within the middle third of a rectangular pier (the kern) or the pier cracks on the far side.

**A3.** Out-of-plane bending at 30 kN: «A3_e0_pb» % ($e$ = 0), «A3_e1_pb» % ($h/6$), «A3_e2_pb» % ($h/3$), corresponding to $e_z$ = «A3_e0_ez», «A3_e1_ez», «A3_e2_ez» mm. *Check:* in the $e$ = 0 run the half-difference is the same at the five heights within «A3_e0_spr» µε, as an offset through the thickness predicts. In the $h/3$ run the raw half-differences spread over «A3_e2_sprr» µε, because each back gage sits up to 0.2 mm from its front partner and the steep in-plane gradient leaks in; correcting each pair by $\beta(y_F - y_B)/2$ brings the spread down to «A3_e2_spr» µε and the percent bending from «A3_e2_raw» % to «A3_e2_pb» %. *Interpret:* using the front gages alone in the $e$ = 0 run would overstate the strain by the bending fraction, about «A3_e0_pb» %, and $E$ would come out low by the same amount; the back gages alone would err the other way. Standards for tension testing limit the percent bending because it biases modulus and yield measurements in exactly this way.

| Gage | Measured (MPa) | Eq. 8 (MPa) | Difference | Limit (Eq. 15) | Verdict | $I_{yz}$ ignored | + fillet | + fillet and Eq. 9 |
|-----|--------------:|--------------:|-------:|-------:|----------|-------:|-------:|---------:|
«A4_table»

: Table K4. Part B at 30 kN. Measured section: legs «B_bV» and «B_bH» mm, $t$ = «B_t» mm.

**A4.** Measured section (legs as rectangles): $A$ = «B_A» mm², centroid at $y$ = «B_yc», $z$ = «B_zc» mm from the heel; $I_z$ = «B_Iz», $I_y$ = «B_Iy», $I_{yz}$ = «B_Iyz» mm⁴; $\theta_p$ = «B_th»°, $I_u$ = «B_Iu», $I_v$ = «B_Iv» mm⁴. Load point: $y_P$ = «B_yP», $z_P$ = «B_zP» mm; $u_P$ = «B_uP», $v_P$ = «B_vP» mm. Table K4: Eq. 8 reproduces the pattern (signs and magnitudes, G1 in compression at «B_G1_ratio» $P/A$), but only «B_nagree» of the 4 gages agree within Eq. 15: the residuals are «B_res» MPa. Ignoring $I_{yz}$ is off by up to «B_naive_err» % of the true value. The plane through the four measured stresses has its neutral axis at «B_phim»° from $z$, against «B_phip»° from Eq. 8. *Check:* $I_u + I_v$ = «B_sum» mm⁴ = $I_y + I_z$ = «B_sum2» mm⁴; $I_y \approx I_z$ (equal legs, measured legs differ by 0.1 mm). *Interpret:* the load acts far below the horizontal leg and well to one side, so the minor-axis couple bends the vertical leg's tip back toward compression: a tension member with compression in its outstanding leg. A thin outstanding leg in compression can buckle locally, and a brittle material could crack there. The residuals are explained in C3.

**A5.** Use Table K1. Expected verdicts: $E\varepsilon_0$ with $P/A$, $e_{eff}$ with $eC_{mid}$ (not with the hole offset), the Part C values with Eq. 9, and the angle with Eq. 8 only after the fillet and Eq. 9 are included. Full credit needs Table 5 complete, a normalized figure with error bars, and each discrepancy above $U$ explained with a named, quantified cause (the straightening, the fillet, misalignment).

| $P$ (kN) | $C_{mid}$ measured | Eq. 9 | $C_{end}$ measured | Eq. 9 | $w_{mid}$ measured (mm) | Eq. 9 (mm) |
|-------:|----------:|--------:|----------:|--------:|----------:|---------:|
«M1_table»

: Table K5. Part C: bending-moment factors from Eq. 12 and the LVDT deflection against Eq. 9 ($e$ = 6.40 mm, $EI$ from Table 1 and the measured $b$).

**M1.** (a) Table K5. At 25 kN: **$C_{mid}$ = «M1_Cm»** vs Eq. 9 «M1_Cp» ($|\Delta|$ = «M1_Cd» ≤ «M1_Cl», «M1_Ca»); $C_{end}$ = «M1_Em» vs «M1_Ep» («M1_Ea»); $w_{mid}$ = «M1_wm» mm vs «M1_wp» mm («M1_wa»). Eq. 4 assumes $C = 1$: it overstates the mid-length bending moment by «M1_err» % (Eq. 9: «M1_errp» %), and the largest stress at mid-length (front face) by «M1_sover» %: «M1_sf450» MPa by Eq. 4 against «M1_sfmid» MPa measured. Near the block the measured front-face stress is «M1_sfend» MPa, still «M1_send_over» % below Eq. 4. The axial strain gives $E\varepsilon_0$ = «M1_sax» MPa vs $P/A$ = «M1_PA» MPa: the centric part is unaffected. (b) Eq. 4 is 5 % off at **«M1_P5w» kN** through the thickness ($P/P_{cr}$ = «M1_P5wr») and at **«M1_P5s» kN** across the width ($P/P_{cr}$ = «M1_P5sr»): the same fraction of each buckling load, as Eq. 10 predicts. Part A at 30 kN is inside the 5 % band; Part C is far outside it from about 3 kN on. (c) In compression $C$ grows: «M1_Cc25» at 25 kN and «M1_Cc40» at 40 kN for the Part C configuration, without bound at $P_{cr}$ = «M1_Pcr» kN; Eq. 4 is already 5 % low at «M1_P5c» kN. The deformation adds to the eccentricity, so Eq. 4 underestimates the stress: unconservative. *Interpret:* Eq. 4 may be used when $|P|$ is below about 4 % of the buckling load of the member in the plane of the offset; above that, use Eq. 9 (or the secant formula in compression, §10.2). In tension Eq. 4 errs on the safe side; in compression it does not.

## 4. Challenge and Extension solutions

**C1.** Slope of $e_{eff}$ against $P$: $h/6$, «C1_e1_s» µm/N against «C1_e1_sp» µm/N from Eq. 9; $h/3$, «C1_e2_s» against «C1_e2_sp» µm/N. They are resolved at «C1_e1_sig» and «C1_e2_sig» standard uncertainties, both consistent with Eq. 9, and the measured drop over the test is «C1_e1_drop» % and «C1_e2_drop» %. Extrapolated to $P = 0$: «C1_e1_e0» and «C1_e2_e0» mm, against holes «A1_e1_hole» and «A1_e2_hole» mm. The trend is the straightening of Section 2.4, seen in a member where it is only a few percent.

**C2.** Least-squares fit of $w_{mid}(P)$ with $EI$ as the only unknown: **$EI$ = «C2_EI» N·m²** (statistical scatter, hole offset, LVDT gain and end-block length combined) vs $E\,hb^3/12$ = «C2_EIr» N·m²: $|\Delta|$ = «C2_d» ≤ «C2_l», «C2_a» («C2_pct» %). The uncertainty of the offset $e$ (±0.05 mm on 6.4 mm) and of the block length $a$ dominate; $EI$ from the LVDT is an independent check of $E$ through a stiffness, not a strain.

**C3.** For the measured angle, Eq. 9 gives $C_{mid}$ = «B_Cmin» for the minor-axis component of the offset and «B_Cmaj» for the major-axis component at 30 kN. Including the 4.8 mm fillet changes the predictions by «B_res_fil» MPa (area +«B_dA» %); adding the straightening changes them by a further «B_res_bc» MPa. Against the residuals «B_res» MPa of A4, the straightening explains most of the misfit and the fillet a little; with both, «B_nagree_bc» of the 4 gages agree (Table K4, last column). Remaining differences come from the truth model's slightly different load point and dimensions, within the stated uncertainties.

**X1.** Appendix D.4. With $a$ = 0 the compression solution gives $M_{max} = Pe\sec(kL/2)$ and $y_{max} = e[\sec(kL/2) - 1]$, Beer's secant formula (§10.2). With blocks, $P_{cr}$ is the root of $\cos u = ka\sin u$; for $a/L$ = 0.1 it is «X1_ratio» of $\pi^2EI/L^2$ (the blocks lengthen the effective member). The small-load expansion is in Appendix D.4.

**X2.** At the section: $M$ = «X2_M» N·m (Beer sign; tension on top), $T$ = «X2_T» N·m, $V$ = «X2_V» N. $I$ = «X2_I» mm⁴, $J$ = «X2_J» mm⁴. Top (H): $\sigma_x$ = «X2_stop» MPa, $\tau = Tc/J$ = «X2_tT» MPa. Side where they add (K): $\sigma_x$ = 0, $\tau$ = «X2_tT» + «X2_tV» = «X2_tside» MPa; on the opposite side «X2_tother» MPa. To measure the torque alone, put a ±45° pair at the top or bottom, where $VQ/(It)$ = 0 and the bending strain cancels in $\varepsilon(+45°) - \varepsilon(-45°)$; or average the two sides. These are the Lab 8 predictions.

**X3.** The kern of the nominal angle has «X3_nv» vertices (one per edge of the convex outline) and an area of «X3_area» mm² (simulation: «X3_sim» mm²). The Part B load point is «X3_dP» mm from the centroid; along that direction the kern ends «X3_dk» mm from it. No position of a gusset on one leg can bring the load inside the kern; connecting both legs, or using a pair of angles back to back, is the way to load an angle concentrically.

## 5. Design problem D1: reference solution

**D1.** $\sigma_{allow}$ = 0.6 × 273.7 = «D_sa» MPa. Load point: in the gusset mid-plane, 4.765 mm below the connected leg, on its bolt line at $g$ from the heel. Table K6 evaluates Eq. 8 at every corner of the convex outline (the largest stress is always at a corner) for each candidate, with $T$ = 40 kN, and adds the beam-column values (Eq. 9, $L$ = 1.50 m, $a$ = 75 mm).

| Angle | $A$ (mm²) | Mass (kg/m) | $P/A$ (MPa) | Largest $\sigma$, Eq. 8 (MPa) | Smallest $\sigma$ (MPa) | Eq. 9, ends (MPa) | Eq. 9, mid (MPa) | OK? |
|--------------------------------------------|-------:|-------:|-------:|---------:|---------:|--------:|--------:|-----|
«D_table»

: Table K6. D1 candidates (6061-T6, root fillets ignored; Eq. 9 columns at the ends of the free length and at mid-length).

**Reference design: «D_best»**, «D_best_m» kg/m, largest stress «D_best_s» MPa = «D_best_r» $\sigma_{allow}$ (simulation preset "D1": «D_sim» MPa). The equal-leg L64 × 64 × 6.4 has the same mass and also passes («D_64_s» MPa), so either earns full credit if justified; the unequal angle is better because the connected long leg puts the gage line close to the centroid's projection. Connecting the **short** leg of the same angle fails («D_short_s» MPa): the choice of leg is part of the design. $P/A \le \sigma_{allow}$ alone would choose «D_naive» ($P/A$ = «D_naive_PA» MPa), whose true largest stress is «D_naive_s» MPa, «D_naive_r» times the allowable. The L51 × 51 × 6.4 fails narrowly («D_51_s» MPa with Eq. 8; «D_51_end» MPa even with Eq. 9 at the ends). The straightening helps little where it matters: the governing stress is at the ends of the free length, where Eq. 9 gives «D_best_end» MPa for the chosen angle (mid-length «D_best_mid» MPa), so relying on it would not change the choice. The compression side reaches «D_best_min» MPa in the outstanding leg, far below local-buckling concern for $b/t$ = 8. *Assumptions that could invalidate a design:* the rigid-block model of the gusset (a flexible gusset rotates and changes the end moments; check with a strain-gaged prototype); stress concentration and shear lag at the bolts (the net-section check required by design codes); load reversal under wind, which would make this slender brace buckle (Lab 9).

**Rubric detail (15 points total in the report).** Section properties, principal axes and load point (3.75). Largest stress at the right corner with Eq. 8 and the student's own $\sigma_Y$ (3.75). Three or more candidates including the connected-leg choice (3). Comparison with $P/A$ and a reasoned decision on Eq. 9 (3). Presentation and assumption (1.5). Typical partial credit: load point at the leg's mid-thickness instead of the gusset mid-plane (−2); $I_{yz}$ ignored (−4); stress at the centroid's distance instead of the extreme corner (−2).

## 6. Expected ranges for real class data

| Quantity | Expected | If outside, suspect |
|------------------------------|--------------|------------------------------------------------|
| $E\varepsilon_0 / (P/A)$ | 0.98–1.02 | $E$ value; gage factor; misread load |
| $e_{eff}$ / hole offset at 30 kN ($h/3$) | 0.95–0.99 | hole offset measured from the wrong edge; pin clearance; grips not self-aligning |
| Out-of-plane bending | < 6 % | grips binding; end blocks clamped crooked; bar bowed |
| Angle stresses vs Eq. 8 | within 12 % | load point measured to the leg instead of the gusset mid-plane; gage on the wrong face |
| Part C $C_{mid}$ at 25 kN | 0.63–0.71 | wrong hole; $a$ or $L$ misread; bar bowed out of plane |
| Part C $w_{mid}$ at 25 kN (mm) | 1.9–2.3 | LVDT not square to the face; stand on the moving crosshead |

: Table K7. Expected data ranges.

## 7. Common student mistakes

1. Taking $z$ to the right in section views, which flips the sign of $I_{yz}$ and of every $z$ term.
2. Writing $M = +Pe$ in Eq. 1 for a load above the centroid, so that the tension side comes out in compression.
3. Using Eq. 4 in the drawing axes for the angle, with $I_{yz}$ ignored.
4. Measuring the angle's load point to the leg's mid-thickness instead of the gusset mid-plane.
5. Fitting the front gages only, then reporting the out-of-plane misalignment as an error in $E$ or $e$.
6. Comparing $e_{eff}$ with the hole offset and calling the 3 % gap "experimental error" without testing it against Eq. 9.
7. Using $I_z$ instead of $I_y$ in Eq. 9 for Part C, which gives $C_{mid}$ close to 1.
8. Applying Eq. 10 with the pinned-end $\pi^2EI/L^2$ when the end blocks lower the buckling load.
9. In D1, checking only $P/A$, or checking the stress at the centroidal distance instead of at the outline's corners.
10. Concluding from Part C that Eq. 4 is "wrong" rather than stating its condition of validity.

## 8. Grading rubric

| Part | Points | Full credit | Common deductions |
|----------------|------:|----------------------------------------------------------|------------------------------|
| Pre-lab | 15 | P1–P6 correct with units; P1 an estimate made before measuring | P3 with $I_{yz}$ sign wrong (−2) |
| Data & procedure | 10 | Tables 3–4 complete; checks recorded | hole offsets not measured (−3) |
| A1 | 10 | $e_{eff}$ with $U$ for each hole, compared with Eq. 1 and Eq. 9 | only one comparison (−3) |
| A2 | 8 | $y_0$ for each run, plot with kern, product check | no plot (−3) |
| A3 | 6 | percent bending and $e_z$, constancy check, interpretation | — |
| A4 | 15 | measured vs Eq. 8 with $U$, $I_{yz}$-ignored comparison, neutral-axis direction | load point wrong (−4) |
| A5 | 6 | complete table, normalized figure, every discrepancy explained | unexplained discrepancy (−1 each) |
| M1 | 10 | (a)–(c) with numbers and a stated rule | no simulation numbers in (c) (−2) |
| D1 | 15 | see Sec. 5 | see Sec. 5 |
| Communication | 5 | labeled axes, units, $x \pm U$ format | each unlabeled axis (−1) |
| Challenge | +10 | C1 (3), C2 (3), C3 (4) | — |

: Table K8. Grading rubric (100 points plus up to 10 Challenge points). Core analysis A1–A5 totals 45.

Every Core answer must include the required check and interpretation; deduct 1 point per question where either is missing.

## 9. Instructor notes

**Before the lab.** The bar: 6061-T6 flat, 50.8 × 12.7 × 400 mm. Bond five gages across the width at mid-length on each broad face (front and back at the same heights, ±0.2 mm), and one pair at $y$ = 0 40 mm from where the lower block will end. End blocks: two steel blocks per end (or one slotted block) clamped with four M10 bolts each; drill and ream the four pin holes as one set so that the two ends match, and mark the reference edge from which students measure the offsets. Self-aligning (spherical-seat) clevises are essential: rigid grips would add end moments and invalidate Eq. 9. The angle: 450 mm of 50.8 × 50.8 × 6.35 mm extruded 6061-T6; two 9.53 mm steel gusset plates bolted to the outer face of one leg on its 28.6 mm gage line. Measure the root fillet with a radius gage.

**Timing (2 h).** 0:00–0:10 safety and pre-lab; 0:10–0:25 dimensions and hole offsets; 0:25–1:05 Part A (three holes, 10–12 min each including the pin change); 1:05–1:25 Part C with the LVDT; 1:25–1:50 Part B (specimen change); 1:50–2:00 simulation (step 6). If time is short, run only $e$ = 0 and $h/3$ in Part A; A1–A3 still work.

**Safety.** The pins are the weak point: use hardened pins with retaining clips and check them before every run. Never load these fixtures in compression (P6).

**Running without equipment.** Give students `sample_data.csv` and Appendix A; everything in this key applies unchanged. A good hybrid is to run Part A live and use the sample data for Parts B and C.

**Your own class data.** Export the columns listed in Table A1; fill a measurements JSON like `src/specimen_measurements.json`, with the class's Lab 1 and Lab 2 values in `reference`; run `src/lab06_analysis.py` and `src/make_key.py`.

**The simulation.** Students use it in P5, step 6, A4, M1, C3, X2, X3 and D1. Its readout separates verification rows ("agree") from model comparisons ("different models"); the tests are in `tests/` and summarized in `tests/VERIFICATION.md`.

## 10. Self-critique and revisions

Before release, the lab was reviewed as a demanding instructor at a top program would review it. The three biggest weaknesses found, and the fixes made:

1. **Eccentric tension of a stocky bar only confirms Eq. 4.50 to a few percent,** a verification with nothing at stake. *Fix:* Part C puts the same bar's offset through its thickness, where the deformation changes the eccentricity enough to make Eq. 4 «M1_err» % high at mid-length; it is measured two independent ways (strain ratio and LVDT) against Eq. 9, and M1 turns it into a rule ($|P| \lesssim 0.04\,P_{cr}$) that also warns about compression (Lab 9). The ratio estimator of Eq. 11, in which $E$ and gage-factor errors cancel, is precise enough to detect the «A1_drop» % straightening even in Part A.
2. **Only doubly symmetric sections,** so principal axes and $I_{yz}$ were never tested. *Fix:* Part B is a real one-leg-connected angle, the way bracing is built. Eq. 8 in principal axes predicts a compressive gage in a tension member, and ignoring $I_{yz}$ errs by up to «B_naive_err» %. D1 turns the same physics into a member choice where $P/A$ alone picks an angle that is «D_naive_r» times overstressed.
3. **Fixture misalignment would contaminate the measured eccentricity unnoticed.** *Fix:* gages at five heights on both faces separate in-plane bending from out-of-plane misalignment (A3), the $e$ = 0 run measures the fixture's own bending, and every estimator is a ratio of front/back averages.

**Known limitations (not fixed).** The end blocks are modeled as rigid and the clevises as frictionless pins; real spherical seats have friction, which adds a small end moment. The angle is treated as bending about two principal axes with no coupling to twist (its shear center is at the heel); in tension this coupling is stabilizing and small. Shear lag and the stress concentration at the bolt holes are outside the model (the gages are far from the connections). The truth model has no initial crookedness of the bar, which in a real Part C test would add to or subtract from the offset.

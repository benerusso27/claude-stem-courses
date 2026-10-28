# Lab 8 — Instructor Key: Transformation of Stress and Strain

::: {custom-style="Instructor"}
**For instructors only. Do not distribute to students.** Every number in this key is computed by `src/lab08_analysis.py` (and `src/make_key.py`) from `sample_data.csv` and `src/specimen_measurements.json`, or by the simulation's own model code run in Node. To build a key for your own class data, put your CSV and measurements in the same format and run `python3 src/lab08_analysis.py your.csv your_measurements.json`, then `python3 src/make_key.py`. Uncertainties are expanded ($U = 2u$) unless marked $u$; they come from a Monte Carlo propagation of every input (GUM Supplement 1), so quantities that share inputs keep their correlation. Sign convention as in the handout (Beer 8e): tension positive, $\tau_{xy} > 0$ on the $+x$ face in $+y$, $\theta$ counterclockwise, Mohr's circle "clockwise above"; on the tube $x$ along the tube and $y$ 90° counterclockwise from $x$ seen from outside.
:::

## 1. Results at a glance (sample data)

| Quantity | Measured | Reference or prediction | Verdict (Eq. 13) |
|------------------------------|----------------|------------------------------|--------------------|
| Tube: $D_o$, wall (mm) | «Do», «tw» | 38.10 × 3.18 nominal | — |
| Rosette H, rosette K bonded at $\beta$ (°) | «bH», «bK» | 0 intended | — |
| $E$ (GPa), Part A | «E_A» | Lab 2: «ref_E» | «E_ag» |
| $\nu$, Part A | «nu_A» | Lab 2: «ref_nu» | «nu_ag» |
| $G$ (GPa), Part B − Part A, mean of H and K | «G_mean» | Lab 3: «ref_G»; $E/2(1+\nu)$: «G_A» | «G_ag3» with Lab 3; «G_agA» with $E$, $\nu$ |
| H, Part B: $\sigma_{max}$, $\sigma_{min}$ (MPa) | «BH_s1», «BH_s2» | Eq. 9: «BH_s1_p», «BH_s2_p» | «BH_ag» |
| H, Part B: $\theta_p$ (°) | «BH_th» | «BH_th_p» | «BH_th_ag» |
| K, Part B: $\sigma_{max}$, $\sigma_{min}$ (MPa) | «BK_s1», «BK_s2» | Eq. 9: «BK_s1_p», «BK_s2_p» | «BK_ag» |
| $\sigma_\theta$ per MPa, Part C | «C_sth» | Lamé «C_sth_lame»; thin wall «C_sth_thin» | «C_ag_lame» with Lamé; «C_ag_thin» with thin wall |
| $\nu$ from the pressure strains | «C_nu» | Lab 2: «ref_nu» | «C_nu_ag» |
| H, Part C with the lever: $\sigma_{max}$, $\sigma_{min}$ (MPa) | «XH_s1», «XH_s2» | «XH_s1_p», «XH_s2_p» | both tensile, as predicted |
| H, Part C with the lever: absolute / in-plane $\tau_{max}$ (MPa) | «XH_tabs» / «XH_R» | absolute predicted «XH_tabs_p» | «XH_ag» |
| D1 lightest tube | «D_best» | with the in-plane $\tau_{max}$: «D_inplane» (unsafe) | — |

: Table K1. Results from the sample data.

The sample data were generated from a known "truth" model (`src/generate_sample_data.py`, values in `src/truth.json`): $E$ = 68.9 GPa, $\nu$ = 0.33; tube 38.13 × 3.205 mm; arms 250.6 and 200.2 mm; the "axis" load point 0.4 mm off the axis; rosette H 1.2° from the top toward K and bonded at +1.5°; rosette K 0.8° above mid-height and bonded at −1.0°; gage factor +0.3 % common and ±0.3 % per grid; $K_t$ = 1.2 % with $\nu_0$ = 0.285; load cell +0.2 %, pressure transducer −0.3 %; 1.5 µε noise and 1 µε resolution; beam theory for bending, torsion and transverse shear and the exact Lamé solution for pressure. The closure tests in `tests/test_lab08_independent.py` confirm that the analysis recovers the truth values within their stated uncertainty.

## 2. Pre-lab solutions

Nominal tube: $r_o$ = 19.05 mm, $r_i$ = 15.875 mm, $I$ = «P_I» mm⁴, $J$ = «P_J» mm⁴, $Q$ = «P_Q» mm³; Table 1: $E$ = 68.46 GPa, $\nu$ = 0.3296, $G$ = «P_G» GPa.

**P1.** (a) $M$ = 150 N·m, $T$ = 120 N·m: $\sigma_x$ = «P1_sx» MPa, $\tau_{xy}$ = «P1_t» MPa. $\sigma_{ave}$ = «P1_ave», $R$ = «P1_R» MPa: $\sigma_{max}$ = «P1_s1» MPa, $\sigma_{min}$ = «P1_s2» MPa, $\theta_p$ = «P1_th»° (clockwise from $x$, seen from above), in-plane $\tau_{max}$ = «P1_R» MPa. (b) $Tc/J$ = «P1_tT» and $VQ/(It)$ = «P1_tV» MPa: $\tau_{xy}$ = «P1_tK» MPa at K. (c) $\varepsilon_x$ = «P1_ex», $\varepsilon_y$ = «P1_ey», $\gamma_{xy}$ = «P1_g» µε; readings a, b, c = «P1_rd» µε. (d) Eq. 10: $\sigma_\theta$ = «P1_th_thin», $\sigma_x$ = «P1_x_thin» MPa; Eq. 11: «P1_th_lame» and «P1_x_lame» MPa. Units: N·m × m/m⁴ = N/m².

**P2.** X is at (σ_x, −τ_xy) = («P1_sx», «P1_mt») MPa, above the axis (the negative τ_xy turns the element clockwise); Y at (0, «P1_t»). The circle crosses the axis at «P1_s1» and «P1_s2» MPa. From X, turning **clockwise** by $2\theta_p$ = «P1_2th»° reaches A, so the largest tensile stress acts «P1_thabs»° clockwise from the tube axis as seen from above, which is toward the lever side (the local $y$ at H points away from it).

**P3.** Eqs. 6–8 return P1(a) exactly. Bonded at 2°: readings a, b, c = «P3_rd» µε. Eq. 6 then gives $\varepsilon_x$ = «P3_ex» and $\gamma_{xy}$ = «P3_g» µε (wrong by «P3_dex» and «P3_dg» µε), and $\theta_p$ wrong by 2°; $\varepsilon_{max}$ = «P3_e1» µε, unchanged.

**P4.** $\sigma_x$ = «P4_sx», $\sigma_y$ = «P4_sy», $\tau_{xy}$ = «P1_t» MPa: $\sigma_{max}$ = «P4_s1», $\sigma_{min}$ = «P4_s2» MPa, both tensile. In-plane $\tau_{max}$ = «P4_R» MPa; with $\sigma_3$ = 0, the absolute $\tau_{max}$ = $\sigma_{max}/2$ = «P4_tabs» MPa. Tresca uses the absolute value.

**P5.** Simulation, presets as shipped (page material $E$ = 68.9 GPa, $\nu$ = 0.33): H: $\sigma_{max}$ = «sim_H_s1», $\sigma_{min}$ = «sim_H_s2» MPa, $\theta_p$ = «sim_H_th»°, readings «sim_H_rd» µε. K: «sim_K_s1» and «sim_K_s2» MPa at «sim_K_th»°, readings «sim_K_rd» µε. Part C with the lever at H: in-plane «sim_X_R», absolute «sim_X_tabs» MPa. "Rosette turned 5°": with $\beta$ = 0, $\sigma_x$ = «sim_cr_sx0» and $\tau_{xy}$ = «sim_cr_t0» MPa; with $\beta$ = 5°, «sim_cr_sx5» and «sim_cr_t5» MPa; $\sigma_{max}$ = «sim_cr_s1» MPa in both.

**P6.** (a) Oil under pressure (bleeding, relief valve, shield, no work on fittings under pressure); the lever and screw loader (hands clear, load by hand); a tube slipping in the clamp. (b) At 600 N with 8 MPa the largest von Mises stress is «P6_vm» MPa at H on the outer surface and «P6_vm_in» MPa at the inner surface: «P6_pct» % of $\sigma_Y$, so the tube stays far inside the elastic range (Hooke's law and Eq. 8 require it), with margin for a misplaced load point.

::: {.needspace lines="16"}
:::

## 3. Analysis solutions

| | Gage a | Gage b | Gage c | $\varepsilon_x$ | $\varepsilon_y$ | $\gamma_{xy}$ |
|---|------:|------:|------:|------:|------:|------:|
«A_table»

: Table K2. Slopes of the readings ($K_t$-corrected) and of the reduced components, µε per 100 N (Parts A, B) or per MPa (Part C), before turning back.

**A1.** Table K2. At H in Part A, $\gamma''/(\varepsilon_x'' - \varepsilon_y'')$ = «A1_ratio», so **$\beta_H$ = «bH»°**. Turned back, $\varepsilon_x$ = «A1_ex» µε/N; with $\sigma_x$ = $FL_bc/I$ = «A1_sxN» kPa per newton, **$E$ = «E_A» GPa** and **$\nu$ = «nu_A»**. Lab 2: $E$ «ref_E», $|\Delta|$ = «E_d» ≤ «E_lim», «E_ag»; $\nu$ «ref_nu», «nu_ag». *Check:* $\sigma/\varepsilon$ has units of stress; with $\beta$ = 0 the apparent shear $-(\varepsilon_x - \varepsilon_y)\sin 2\beta$ vanishes. *Interpret:* turning the rosette slides its three points around the same circle (Figure 2b), so the principal strains do not change. In Part A the turn changes $\varepsilon_x$ and $\varepsilon_y$ only to second order ($\cos 2\beta$ = «A1_cos»), so $E$ and $\nu$ would hardly change; the turn spoils the shear strain, which is first order in $\beta$: «A1_gapp» µε of apparent shear at 600 N. The $K_t$ correction matters more for $\nu$: without it $\nu$ = «nu_noKt» («nu_noKt_pct» %), while $E$ moves only «E_noKt_pct» % (C3).

**A2.** Torsion only (Part B − Part A): at K, $(\varepsilon_x'' - \varepsilon_y'')/\gamma''$ gives **$\beta_K$ = «bK»°**. Turned back: **$G$ = «G_H» GPa at H and «G_K» GPa at K**, mean «G_mean» GPa. From A1, $E/2(1+\nu)$ = «G_A» GPa («G_agA»); Lab 3: «ref_G» GPa, $|\Delta|$ = «G_d3» against a limit of «G_lim3» («G_ag3»). *Check:* the torsion-only state at H, turned back by $\beta_H$ from Part A (an independent angle), has $\varepsilon_x - \varepsilon_y$ = «A2_dexy» µε per 100 N against $\gamma_{xy}$ = «A2_g» µε, a residual turn of «A2_res»°, within the uncertainty of $\beta_H$: pure shear, as it must be. *Interpret:* bending and transverse shear depend only on $F$ and the section, which are the same in Parts A and B; only the torque changes, so the difference isolates it. A torsion test of a thin solid bar (Lab 3) and a tube in combined loading give the same $G$ within about «G_pct» %.

| Point | $\sigma_x$ (MPa) | $\tau_{xy}$ (MPa) | $\sigma_{max}$ (MPa) | $\sigma_{min}$ (MPa) | $\theta_p$ (°) | Eq. 9: $\sigma_{max}$, $\sigma_{min}$ | Eq. 9: $\theta_p$ |
|------|------:|------:|------:|------:|------:|------:|------:|
«B_table»

: Table K3. Part B at 600 N, stresses from the turned-back strains with Lab 2's $E$ and $\nu$.

**A3.** Table K3. At H: **$\sigma_{max}$ = «BH_s1» MPa**, $\sigma_{min}$ = «BH_s2» MPa, $\theta_p$ = «BH_th»°, against «BH_s1_p», «BH_s2_p» MPa and «BH_th_p»°: «BH_ag» (differences «BH_d1», «BH_d2» MPa within «BH_l1», «BH_l2»). At K: «BK_s1» and «BK_s2» MPa at «BK_th»°, against ±«BK_s1_p» MPa at −45°. $\sigma_{max}$ agrees; $\sigma_{min}$ differs by «BK_d2» MPa against a limit of «BK_l2»: rosette K sits slightly above mid-height (M1(e)), where the bending stress adds «BK_sx» MPa to $\sigma_x$ and raises both principal stresses by half of that. With K at the measured height, the prediction becomes «BK_s1_c» and «BK_s2_c» MPa, and both agree. *Check:* $\sigma_{max} + \sigma_{min}$ = «BH_I1» MPa = $\sigma_x + \sigma_y$ at H. *Interpret:* at H the bending tension dominates and the largest tension runs «BH_thabs»° from the tube axis; at K there is no bending, the state is nearly pure shear, and the largest tension runs at 45°: the helix along which a brittle tube would crack in torsion.

**A4.** Pressure slopes (turned back), per MPa: H: $\varepsilon_x$ = «CH_ex», $\varepsilon_y$ = «CH_ey» µε; K: «CK_ex», «CK_ey» µε. (a) **$\nu$ = «C_nu»** (mean of H and K), against Lab 2 «ref_nu»: «C_nu_ag». (b) **$\sigma_\theta$ = «C_sth» MPa per MPa** and $\sigma_x$ = «C_sx»: Lamé (Eq. 11) gives «C_sth_lame» and «C_sx_lame» («C_ag_lame»); the thin-wall Eq. 10 gives «C_sth_thin» and «C_sx_thin» («C_ag_thin», «C_thin_pct» % high). *Check:* $\sigma_x/\sigma_\theta$ = «C_ratio». *Interpret:* the gages agree with Lamé. Equation 10 is the average hoop stress through the wall, which is exact, but the hoop stress falls from the inner to the outer surface (Figure 4), and the gages see only the outer value.

**A5.** With 8 MPa and 600 N on the lever: at H, **$\sigma_{max}$ = «XH_s1» and $\sigma_{min}$ = «XH_s2» MPa, both tensile** (predicted «XH_s1_p» and «XH_s2_p»). In-plane $\tau_{max}$ = «XH_R» MPa; **absolute $\tau_{max}$ = «XH_tabs» MPa** = $\sigma_{max}/2$, predicted «XH_tabs_p» («XH_ag»), «XH_ratio» times the in-plane value. At K: «XK_s1» and «XK_s2» MPa; $\sigma_{min}$ is only just tensile, so the absolute «XK_tabs» MPa barely exceeds the in-plane «XK_R» MPa. *Check:* the absolute value is never less than the in-plane one. *Interpret:* Tresca must use the absolute value: at H, the in-plane value understates the largest shear by «XH_pct» %. At the inner surface $\sigma_r = -p$ is the smallest principal stress, which makes the largest circle bigger still (D1).

**A6.** Use Table K1. Expected verdicts: $E$, $\nu$ and $G$ agree with Labs 2 and 3; the principal stresses at H and K agree with Eq. 9 once the rosettes' turns are corrected (and K's height is accounted for); the pressure stresses agree with Lamé, not with the thin-wall formula; the absolute $\tau_{max}$ under pressure agrees with Eq. 4 and is about 1.5 times the in-plane value. Full credit needs Table 5 complete, a normalized figure with error bars, and each discrepancy explained with a named, quantified cause.

**M1.** (a) Eq. 10 is «C_thin_pct» % high at the gages: the ratio is $(r_o + r_i)/(2r_i)$ = «M1_ratio»; 5 % needs $r_o/r_i$ = 1.10, i.e. $r_i/t_w$ ≈ 10. (b) With the lever load at H the in-plane value is «XH_pct» % low; with pressure alone ($\sigma_\theta$ = 2$\sigma_x$, both tensile) the absolute $\tau_{max}$ = $\sigma_\theta/2$ is twice the in-plane $(\sigma_\theta - \sigma_x)/2$, so the in-plane value is 50 % low (Beer Eqs. 7.33, 7.34). (c) Ignoring the turns at H in Part B: $\tau_{xy}$ = «M1_tu» MPa instead of «BH_txy» («M1_tu_pct» % high) and $\theta_p$ = «M1_thu»° instead of «BH_th»°; $\sigma_{max}$ unchanged. (d) Ignoring $K_t$: $E$ changes «E_noKt_pct» %, $\nu$ «nu_noKt_pct» %, the Part C hoop strain «C_ey_noKt_pct» % and the Part C axial strain «C_ex_noKt_pct» %; the gage most affected is the one across the larger strain (gage c in Part A, gage a in Part C). (e) Part A, K: the turned-back $\varepsilon_x$ at K is «M1_ratioK» of that at H, so **K is «phiK»° above mid-height** (truth 0.8°). *Rank:* thin wall (10 %) and in-plane vs absolute shear («XH_pct» % low here, 50 % under pressure alone) are model errors that change a design decision; the rosette turn (6 % on $\tau$) and $K_t$ (3 % on $\nu$, 6 % on the Part C axial strain) are measurement errors that a careful experimenter corrects; K's height matters only for $\sigma_{min}$ at K.

## 4. Challenge and Extension solutions

**C1.** A delta rosette at K aligned with $x$ would read «C1_rd» µε in Part B at 600 N. With 1.5 µε on each reading, $u(\gamma_{xy})$ = $1.5\sqrt{6}$ = «C1_urect» µε for the rectangular rosette (Eq. 6) and $1.5 \times 2\sqrt{2}/\sqrt{3}$ = «C1_udelta» µε for the delta rosette; $u(\varepsilon_x)$ is 1.5 µε for both. The delta rosette is better conditioned for shear (its three directions are spread evenly), which is what K measures.

**C2.** From Part B alone: $\sigma_x$ at H gives $FL_b$ = «C2_FLb» N·m (150 by the load cell and rule), $\tau$ at H gives $Fa_L$ = «C2_FaL» N·m (120). The shear force comes from the difference of the shear stresses at K and H, $VQ/(It)$: **$F$ = «C2_F» N**, against 600 N, and then $a_L$ = «C2_aL» mm and $L_b$ = «C2_Lb» mm. The moments are good to 1.6 %, but $F$ is the small difference of two large stresses (about 24 and 21 MPa), so 0.3 MPa of error in either is 10 % in $F$; the truth model's 1.2° offset of H adds a 2 % bias. A strain-gage load cell should measure bending at two sections instead.

**C3.** Appendix D.4. A gage reads $(\varepsilon_\parallel + K_t\varepsilon_\perp)/(1 - \nu_0K_t)$; this equals $\varepsilon_\parallel$ when $\varepsilon_\perp = -\nu_0\varepsilon_\parallel$, the strain field of the gage-factor calibration. In Part A, gage a sees $\varepsilon_\perp/\varepsilon_\parallel = -\nu$ = −0.33, close to −0.285, so its error is tiny; gage c sees $\varepsilon_\perp/\varepsilon_\parallel = -1/\nu \approx -3$, far from −0.285, so its error is «C3_c_pct» % of its reading (which is why $\nu$ moves). In Part C gage a lies across the hoop strain, 4.6 times its own, and errs by «C_ex_noKt_pct» %.

**X1.** Appendix D.6. The integral $\int_{r_i}^{r_o}(A + B/r^2)\,dr = A t_w + B(1/r_i - 1/r_o) = A t_w + A r_o t_w/r_i = p r_i$, so the average is $pr_i/t_w$.

**X2.** Hooke's law gives $\sigma_x - \sigma_y = 2G(\varepsilon_x - \varepsilon_y)$ and $\tau_{xy} = 2G(\gamma_{xy}/2)$, so Eq. 3 for stress and Eq. 7 for strain give the same $2\theta_p$, and $R_\sigma = 2G\,R_\varepsilon$. For Part B at H: $R_\sigma$ = «BH_R» MPa, $2G R_\varepsilon$ = «X2_R» MPa.

**X3.** Two gages at ±45° to the axis on the top and two on the bottom (or on opposite sides), wired as a full bridge with the +45° gages in opposite arms: torsion strains the +45° gages in tension and the −45° gages in compression, and the bridge adds them. Bending gives equal strains at ±45° (Eq. 5 with $\gamma$ = 0 and $\varepsilon(45°) = \varepsilon(-45°)$), so it cancels within each pair; top and bottom cancel the bending sign too. Pressure gives equal ±45° strains (cancels), transverse shear is zero at top and bottom, and temperature strains all four gages equally (cancels in a full bridge).

## 5. Design problem D1: reference solution

**D1.** Tresca allowable shear $\sigma_Y/(2 \times 1.8)$ = «D_tall» MPa; twist limit 3.0°/m with $G$ = 26.03 GPa. For each tube: Lamé stresses at $r_o$ and $r_i$ ($A = pr_i^2/(r_o^2 - r_i^2)$, $\sigma_\theta = A + Ar_o^2/r^2$, $\sigma_r = A - Ar_o^2/r^2$, $\sigma_x = A \pm Mr/I$), $\tau = Tr/J$, principal stresses with $\sigma_r$ as the third, on the tension and compression sides.

::: {.needspace lines="22"}
:::

| Tube | Mass (kg/m) | Tresca factor (absolute $\tau_{max}$) | With in-plane $\tau_{max}$ | Von Mises factor | Twist (°/m) | Critical point | OK? |
|------------------|-------:|-------:|-------:|-------:|-------:|----------------------|-----|
«D_table»

: Table K4. D1 candidates (factors are $\sigma_Y/(2\tau)$ or $\sigma_Y/\sigma_{vM}$; required 1.8).

**Reference design: «D_best»**, «D_best_m» kg/m. Critical point: «D_crit». There $\sigma_x$ = «D_sx», $\sigma_\theta$ = «D_st», $\sigma_r$ = «D_sr» and $\tau$ = «D_tau» MPa; principal stresses «D_p» MPa; absolute $\tau_{max}$ = «D_tabs» MPa (Tresca factor «D_sf»), while the in-plane circle has radius only «D_tin» MPa. Von Mises factor «D_vm». Twist «D_tw»°/m. The lighter **«D_stress»** passes the stress requirement (factor «D_stress_sf») but twists «D_stress_tw»°/m: the twist limit governs it out. A student who uses the in-plane $\tau_{max}$ picks **«D_inplane»** («D_inplane_m» kg/m, in-plane factor «D_inplane_sfin»), whose true Tresca factor is «D_inplane_sf»: unsafe, because pressure makes both in-plane principal stresses tensile at the inner surface and $\sigma_r = -p$ is the third principal stress. Von Mises gives the same choice as Tresca here. *Assumptions that could invalidate a design:* the closed-end axial stress (an open-ended swivel with a sliding seal carries no $pA$ end force); pressure surges above 20 MPa (relief valve setting); stress concentrations at ports and fittings; fatigue under cyclic pressure and torque, which governs most real hydraulic parts.

**Rubric detail (15 points total in the report).** Stresses at the four points, with $\sigma_r$ at the inner surface (3). Principal stresses and the absolute $\tau_{max}$ at the critical point, by hand and against the simulation (3.75). All requirements checked with the student's own $\sigma_Y$ and $G$ (3). At least three tubes compared, with the in-plane trap named (3.75). Presentation and assumption (1.5). Typical partial credit: thin-wall formulas instead of Lamé (−2); in-plane $\tau_{max}$ only (−4); inner surface not checked (−3); twist not checked (−2).

::: {.needspace lines="16"}
:::

## 6. Expected ranges for real class data

| Quantity | Expected | If outside, suspect |
|------------------------------|--------------|------------------------------------------------|
| $\beta$ of a rosette (°) | −3 to 3 | rosette bonded crooked; gages connected to the wrong channels (a and c swapped gives about 90°) |
| $E$ from Part A (GPa) | 67–70 | $L_b$ measured to the wrong point; load not on the axis; gage factor setting |
| $\nu$ from Part A | 0.31–0.35 | $K_t$ not corrected; rosette H not on top |
| $G$ from Part B − A (GPa) | 25–27 | lever arm misread; load point slipped |
| $\theta_p$ at H, Part B (°) | −22 to −17 | rosette turn not corrected; sign of $\gamma$ (b and the others swapped) |
| $\sigma_\theta$ per MPa, Part C | 4.3–4.7 | air in the oil (pressure lagging); transducer zero |
| Absolute/in-plane $\tau_{max}$ at H, Part C with the lever | 1.4–1.55 | pressure released before loading; wrong zero |

: Table K5. Expected data ranges.

## 7. Common student mistakes

1. Plotting X at $(\sigma_x, +\tau_{xy})$, which mirrors the circle and puts the principal directions on the wrong side.
2. Taking the angle on Mohr's circle as $\theta$ instead of $2\theta$, or turning the element the opposite way to the point.
3. Using Eq. 3's first root without checking whether it gives $\sigma_{max}$ or $\sigma_{min}$.
4. Using $\sigma = E\varepsilon$ component by component instead of Eq. 8: at H it invents a hoop stress of «M7_sy» MPa where there is none, and in Part C it understates the hoop stress by about «M7_pct» %.
5. Treating the in-plane $\tau_{max}$ as the maximum when both principal stresses have the same sign.
6. Using the thin-wall formula with the mean or outer radius instead of the inner radius, or comparing it with surface strains without noting that it is an average.
7. Forgetting that the "combined" readings include the pressure strains (they were not re-zeroed).
8. Ignoring the rosette's turn and reporting the apparent shear in Part A as a real stress.
9. Sign of $\tau_{xy}$ at H and K: the local $y$ axes point in different directions at H and K (Figure 1c); both give $\tau_{xy} < 0$ for this loading.
10. In D1, checking only the outer surface, or leaving out $\sigma_r = -p$ at the inner surface.

::: {.needspace lines="24"}
:::

## 8. Grading rubric

| Part | Points | Full credit | Common deductions |
|----------------|------:|----------------------------------------------------------|------------------------------|
| Pre-lab | 15 | P1–P6 correct with units; P1 an estimate made before measuring | X plotted on the wrong side (−2) |
| Data & procedure | 10 | Tables 3–4 complete; checks recorded | pressure steps not recorded (−3) |
| A1 | 9 | $\beta_H$, $E$ and $\nu$ with $U$, compared with Lab 2 | no $K_t$ correction (−2) |
| A2 | 7 | $\beta_K$, $G$ at H and K, compared | torsion not isolated (−3) |
| A3 | 9 | principal stresses and directions at H and K, circles to scale | turns not corrected (−3) |
| A4 | 8 | $\nu$ from the ratio; Lamé vs thin wall | only one model (−3) |
| A5 | 7 | in-plane and absolute values, three circles | absolute missing (−4) |
| A6 | 5 | complete table, normalized figure, every discrepancy explained | unexplained discrepancy (−1 each) |
| M1 | 10 | (a)–(e) with numbers and a ranking | ranking missing (−2) |
| D1 | 15 | see Sec. 5 | see Sec. 5 |
| Communication | 5 | labeled axes, units, $x \pm U$ format | each unlabeled axis (−1) |
| Challenge | +10 | C1 (3), C2 (4), C3 (3) | — |

: Table K6. Grading rubric (100 points plus up to 10 Challenge points). Core analysis A1–A6 totals 45.

Every Core answer must include the required check and interpretation; deduct 1 point per question where either is missing.

## 9. Instructor notes

**Before the lab.** The tube: 6061-T6, 38.1 × 3.18 mm, 500 mm long; the clamp grips 60 mm and the gage section is 125 mm from the clamp face (more than three diameters), 250 mm from the load line. Bond the rosettes with gage a along the tube's axis (scribe a line with a height gage) and record their positions; the analysis measures and corrects small turns anyway. End plugs with O-rings and a bleed screw; a hand pump with a relief valve set at 10 MPa and a 0–20 MPa transducer. The lever: a steel arm clamped to the free-end plug, with a load hole on the tube's axis and one 200 mm to the side; a screw loader pulling down through a 1 kN load cell.

**Timing (2 h).** 0:00–0:10 safety and pre-lab; 0:10–0:20 dimensions, wiring, zero; 0:20–0:40 Part A; 0:40–1:00 Part B; 1:00–1:35 Part C, including filling and bleeding (the longest step: have the tube filled beforehand if possible); 1:35–1:50 Part C with the lever; 1:50–2:00 simulation (step 7). If time is short, skip Part C with the lever and use the sample data for it.

**Safety.** The pressure is the main hazard: insist on bleeding and the shield, and check the relief valve before each session. The tube is far from yield at the limits (P6).

**Running without equipment.** Give students `sample_data.csv` and Appendix A; everything in this key applies unchanged. A good hybrid is to run Parts A and B live and use the sample data for Part C.

**Your own class data.** Export the columns listed in Table A1; fill a measurements JSON like `src/specimen_measurements.json`, with the class's Lab 1–3 values in `reference`; run `src/lab08_analysis.py` and `src/make_key.py`.

**The simulation.** Students use it in P5, step 7, A3, A5, M1 and D1. Its readout separates verification rows ("agree") from model comparisons ("different models"); the tests are in `tests/` and summarized in `tests/VERIFICATION.md`.

## 10. Self-critique and revisions

Before release, the lab was reviewed as a demanding instructor at a top program would review it. The three biggest weaknesses found, and the fixes made:

1. **A rosette lab easily becomes a calculator exercise:** three readings in, Eq. 6 and Mohr's circle, a match, done. *Fix:* the lab measures its own imperfections. Part A's uniaxial state reveals how rosette H was bonded («bH»°), the torsion-only difference reveals rosette K's («bK»°), and Part A's bending leak locates K on the circumference; A1–A3 then show that the corrections move $\tau_{xy}$ by «M1_tu_pct» % and $\theta_p$ by «bH»° while leaving the principal values alone, which is the content of Eq. 1.
2. **Only the in-plane maximum shear was ever computed,** so §7.4 stayed abstract. *Fix:* Part C pressurizes the same tube, making both in-plane principal stresses tensile at H; the measured absolute $\tau_{max}$ is «XH_ratio» times the in-plane value, and D1 turns that into a design trap (the in-plane value picks a tube that is unsafe by Tresca).
3. **The thin-wall formula was taken on faith.** *Fix:* the gages on the outer surface resolve the 10 % difference between Eq. 10 and Lamé (A4), the key explains why Eq. 10 is nevertheless exact on average, and Poisson's ratio is measured from the pressure strains independently of $E$.

**Known limitations (not fixed).** The transverse shear uses $VQ/(It)$ averaged through the wall; for $t_w/r_o$ = 0.17 the exact elasticity distribution differs by a few percent at the surface, and the truth model uses the beam formula too. The clamp is assumed rigid and far enough away (Saint-Venant); end-plug restraint near the clamp is not modeled. Temperature changes during the pressure test (the oil warms slightly when pumped) are ignored; self-temperature-compensated gages make this small. The truth model has no residual stresses from tube manufacture, which would not affect the increments measured here.

# Lab 4 — Instructor Key: Bending

::: {custom-style="Instructor"}
**For instructors only. Do not distribute to students.** Every number in this key is computed by `src/lab04_analysis.py` (and `src/make_key.py`) from `sample_data.csv` and `src/specimen_measurements.json`, or by the simulation's own model code run in Node. To build a key for your own class data, put your CSV and measurements in the same format and run `python3 src/lab04_analysis.py your.csv your_measurements.json`, then `python3 src/make_key.py`. Uncertainties are expanded ($U = 2u$) unless marked $u$. Sign convention as in the handout (Beer 8e): $V$ and $M$ as in Fig. 5.6, $M > 0$ sagging, $\sigma_x = -My/I$ with $y$ up from the neutral axis, tension positive.
:::

## 1. Results at a glance (sample data)

| Quantity | Measured | Reference or prediction | Verdict (Eq. 18) |
|---|---|---|---|
| Bar A: $b$, $h$ (mm); $I$ (10⁵ mm⁴) | «b», «h»; «I» ($u_I$ = «uI» %) | 25.4 × 50.8 nominal | — |
| Shear span $a$ (mm) | «a» | 200 | — |
| $V/P$ in the left shear span (A1) | «A1_V» | 0.5 (Eq. 2) | «A1_agree» |
| Neutral axis, bar A (mm above bottom) | «A2_yNA» | $h/2$ = «A2_h2» | agree |
| $E$ of 6061-T6 from $M$–$\kappa$ (GPa) | «A3_E» | Lab 2: «A3_Eref» | «A3_agree» |
| $\nu$ from anticlastic strain | «A4_nu» | Lab 2: 0.330 ± 0.006 | «A4_agree» |
| Neutral axis, bar B (mm above bottom) | «A5_y» | Eq. 9: «A5_yp» | «A5_yagree» |
| $EI$, bar B (N·m²) | «A5_EI» | $E_1I_t$: «A5_EIp» | «A5_EIagree» |
| $M$ at 40 kN and $\kappa$ = «A6_kmax» m⁻¹ (N·m) | «A6_Mmax» | EPP «A6_Mepp»; material curve «A6_Mro» | EPP +«A6_eppct» %; curve +«A6_ropct» % |
| Flexure stress vs actual at 40 kN (MPa) | actual «A6_sact» | $Mc/I$ = «A6_sflex» | overstated «A6_over» % |
| Permanent curvature (m⁻¹) | «A6_kres» | Eq. 14: «A6_kresp» | «A6_kresagree» |
| Straightedge gap after Part C (mm) | «A6_gap» | middle 200 mm only: «A6_gapmid»; whole bar from the measured $M$–$\kappa$: «A6_gapdata» | gap «A6_gappct» % larger: shear spans yielded too |
| D1 lightest acceptable section | steel «D_best_s», aluminum «D_best_a» | — | — |

: Table K1. Results from the sample data.

The sample data were generated from a known "truth" model (`src/generate_sample_data.py`, values in `src/truth.json`): plane sections, 6061-T6 following Lab 1's Ramberg–Osgood curve ($E$ = 68.9 GPa), the steel strip elastic, a common +0.5 % gage-factor error, true gage heights that differ from the recorded ones by a few hundredths of a millimeter, load points 0.4 mm inside their nominal positions, and 1 µε reading noise. Because every strain reads 0.5 % high, the measured $E$ is 0.5 % low: correct for the gages, invisible to the student, and inside the stated uncertainty. The closure test in `tests/test_lab04_independent.py` confirms that the analysis recovers the truth values within their stated uncertainty.

## 2. Pre-lab solutions

**P1.** (a) $I = bh^3/12$ = «P1_I» × 10⁵ mm⁴, $S$ = «P1_S» mm³. At 20 kN, $M = (P/2)a$ = «P1_M» N·m, $\sigma_m = M/S$ = «P1_sig» MPa, $\varepsilon = \sigma/E$ = «P1_eps» µε, $\kappa = M/(EI)$ = «P1_k» m⁻¹, $\rho$ = «P1_rho» m. (b) $M_Y = \sigma_Y S$ = «P1_MY» N·m, so $P_Y = 2M_Y/a$ = «P1_PY» kN; $M_p = 1.5M_Y$ gives «P1_Pp» kN. Part C's 40 kN is «P1_40Y» $P_Y$ and «P1_40p» $P_p$: well into the plastic range but short of collapse. (c) At 2.5 kN the bottom strain is about «P1_e25» µε, so 1 µε is «P1_res» %. (d) $V/(bh)$ = «P1_tau» MPa, «P1_tau_pct» % of the bending stress (the parabolic maximum, «P1_tau_max» MPa, is Lab 5's subject). Units: N·m/mm³ → MPa after ×10³; µε = 10⁻⁶.

**P2.** (a) Figure 2: $V = P/2$, 0, $-P/2$; integrating, $M$ rises to $Pa/2$, stays flat, and falls by $Pa/2$ to zero at $L$. (b) $a_1 + a_2 = L$, so the loads are still symmetric: $R_A = R_B = P/2$, and $M = (P/2)a_1$ = «P2b_M» × 10⁻³ $P$ (m), «P2b_pct» % above Eq. 2. The middle is still in pure bending. (c) $R_A$ = «P2c_RA» $P$ and $R_B$ = «P2c_RB» $P$ (Appendix D.1); between the loads $V = R_A - P/2$ = «P2c_V» $P$, so $M$ changes by «P2c_dM» % across the middle third. Strictly not pure bending, but far below anything the gages can see. *Lesson:* the measurement is insensitive to small load-point errors because the moment in the middle depends on $a$ only to first order.

**P3.** $n = 205/68.46$ = «P3_n». With $y$ from the bottom of the strip, transformed areas $n b t_s$ at $t_s/2$ and $bh$ at $t_s + h/2$: $\bar y$ = «P3_ybar» mm and $I_t$ = «P3_It» × 10⁵ mm⁴ (bar alone: «P3_Ibar» × 10⁵ mm⁴; ratio «P3_gain»). At 15 kN, $M$ = «P3_Mb» N·m: steel bottom +«P3_stbot» MPa; interface aluminum +«P3_alint» MPa and steel +«P3_stint» MPa (ratio $n$); aluminum top «P3_altop» MPa. (b) $t_s \to 0$: $\bar y \to h/2$ and $I_t \to bh^3/12$. $n = 1$: a homogeneous bar of depth $h + t_s$, with $\bar y = (h + t_s)/2$.

**P4.** (a) $M_Y$ = «P4_MY» N·m, $\kappa_Y = \sigma_Y/(Ec)$ = «P4_kY» m⁻¹, $M_p$ = «P4_Mp» N·m. (b) $M/M_Y$ = «P4_r»; Eq. 12 gives $(\kappa_Y/\kappa)^2 = 3(1 - M/1.5M_Y)$, so $\kappa_Y/\kappa = y_Y/c$ = «P4_yy», $\kappa$ = «P4_k» m⁻¹, and the elastic core is ±«P4_yY» mm. (c) Elastic recovery $M/(EI)$ = «P4_kel» m⁻¹, so $\kappa_p$ = «P4_kp» m⁻¹. Residual stress: top $-\sigma_Y + Mc/I$ = −273.7 + «P4_flex» = +«P4_res» MPa (tension), bottom −«P4_res» MPa. (d) $-\int y\sigma_{res}\,dA = M - M = 0$ (Appendix D.7); students may also integrate the piecewise-linear residual distribution numerically.

**P5.** Simulation, presets as shipped (nominal section, $E$ = 68.9 GPa). Part A: $M$ = «sim_MA» N·m, largest $|\sigma|$ = «sim_sA» MPa. Part B: elastic NA «sim_ybB» mm, $I_t$ = «sim_IB» × 10⁵ mm⁴ (slightly different from P3 because the page uses $E$ = 68.9 GPa). Part C at $\kappa$ = «sim_kC» m⁻¹: material curve «sim_Cmat» N·m, EPP «sim_Cepp» N·m (+«sim_Cpct» %). The EPP law is larger: aluminum's curve bends over before $\sigma_Y$ (the 0.2 % offset point), so the outer fibers carry less than $\sigma_Y$ just past yield, and Part C's strains are not yet large enough for the hardening to make it up. "Overload, then unload" ($\kappa = 3\kappa_Y$ = «sim_unl_k» m⁻¹, $M$ = «sim_unl_M» $M_Y$): permanent curvature «sim_unl_kp» m⁻¹.

**P6.** (a) Pinch points at the rollers and spreader (hands clear when the crosshead can move); stored elastic energy if the bar shifts or a roller slips (bar centered and square, stop on a load drop); overloading the bar or fixture (overload stop set per part); manual handling of 2.5 kg bars. (b) Part C bends the bar permanently, so it must come after Part A, which needs an undamaged bar; an overload stop set before the plastic part is the only protection against running past 40 kN toward collapse at about «P1_Pp» kN, where the deflection would grow quickly.

## 3. Analysis solutions

**A1.** Slopes of bottom strain against $P$ converted with $M = ES\varepsilon$ ($E$ from A3): $M/P$ = «A1_M100» mm at $x$ = 100 mm (statics «A1_S100», «A1_d100» %), «A1_M150» mm at 150 mm («A1_S150», «A1_d150» %) and «A1_M300» mm at midspan («A1_S300», «A1_d300» %); each ±«A1_uM» % ($u$, mostly from $E$). **$V/P$ = «A1_V»**, $|\Delta|$ = «A1_Vd» ≤ «A1_Vlim»: «A1_agree». *Check:* the line through the two shear-span points meets $M = 0$ at $x$ = «A1_icpt_mm» mm, at the support, as a pin must require. *Interpret:* the slope of the moment diagram is the reaction ($V = R_A$ in the shear span); between the loads both load points' halves cancel, so the slope, $V$, is zero. The shear is a difference of two nearly equal moments, which is why its relative uncertainty (about 2.4 %, $u$) is several times that of $M$.

**A2.** «A2_n» steps above 1 kN. Curvature: «A2_k5» m⁻¹ at 5 kN, «A2_k10» at 10 kN, «A2_k20» at 20 kN (linear in load). RMS residuals «A2_rmsmin»–«A2_rmsmax» µε («A2_rms20» at 20 kN). At 20 kN, top «A2_et» µε and bottom «A2_eb» µε. **$y_{NA}$ = «A2_yNA» mm** vs $h/2$ = «A2_h2» mm: difference «A2_off» mm, within «A2_lim». *Check:* residuals at the 1–3 µε level with no curvature in the profile; equal and opposite extreme strains. *Interpret:* a curved profile would mean sections warp (or a gage is misplaced); residuals growing with load in the same pattern would mean gage-height errors (C3), not physics.

**A3.** «A3_n» loading steps; slope $EI$ = «A3_EI» N·m². **$E$ = «A3_E» GPa** vs Lab 2 «A3_Eref»: $|\Delta|$ = «A3_d» ≤ «A3_lim», «A3_agree». Budget ($u$, %): fit «A3_t_slope», $b$ «A3_t_b», $3u_h/h$ «A3_t_h», $a$ «A3_t_a», load cell «A3_t_P», gage factor «A3_t_GF»; total «A3_urel» %. At 20 kN: flexure formula «A3_sflex» MPa vs $E\varepsilon$ = «A3_sEe» MPa ($\varepsilon$ = «A3_eb» µε). *Check:* slope units N·m/(m⁻¹) = N·m²; $I \propto h^3$ so 1 % in $h$ is 3 % in $E$. *Interpret:* the gage factor dominates. A common gage-factor error scales every strain, so it scales $\kappa$ and biases $E$, but it cancels in $y_{NA} = -A_0/A_1$ (C3).

**A4.** **$\nu$ = «A4_nu»** vs 0.330 ± 0.006: «A4_agree». At 20 kN $\rho$ = «A4_rho» m, so $\rho' = \rho/\nu$ = «A4_rhop» m. *Check:* the compressed top widens, so the transverse gage there reads positive («A4_ttop» µε at 20 kN). *Interpret:* the anticlastic curvature makes the top face slightly saddle-shaped; near the edges the transverse strain is affected by the free edges and the gage's finite length, so a centered gage is best (§4.3 assumes the section is free to deform).

**A5.** Measured **NA «A5_y» mm** vs Eq. 9 with measured dimensions and $n$ = «A5_n»: **«A5_yp» mm**; $|\Delta|$ = «A5_yd» ≤ «A5_ylim», «A5_yagree» (the prediction's uncertainty is dominated by $E_{steel}$). All-aluminum bar of the same depth: «A5_hom» mm. **$EI$ = «A5_EI» N·m²** vs $E_1I_t$ = **«A5_EIp»** («A5_EIpct» %), «A5_EIagree». At «A5_P» kN ($M$ = «A5_M» N·m), from the fitted strain line (RMS «A5_rms» µε): steel bottom «A5_m_st_bot» MPa (predicted «A5_p_st_bot», «A5_d_st_bot» %), aluminum interface «A5_m_al_int» («A5_p_al_int»), steel interface «A5_m_st_int» («A5_p_st_int»), aluminum top «A5_m_al_top» («A5_p_al_top»). $\int\sigma\,dA$ = «A5_N» % of the compressive resultant. *Check:* it must vanish in pure bending (first of Eqs. 4); the small remainder is the strain-line fit and the 0.5 % gage-factor bias, which cancels in ratios. *Interpret:* the composite is «A5_gain» times as stiff as bar A («A5_EIal» N·m²); the steel's bottom fiber is the most highly stressed point, about twice the aluminum's top.

**A6.** Table K2 lists the Part C steps. $M_Y$ = «A6_MY» N·m, $M_p$ = «A6_Mp» N·m, $\kappa_Y$ = «A6_kY» m⁻¹ (measured $E$, Lab 1 $\sigma_Y$).

| $P$ (kN) | $M$ (N·m) | $\kappa$ (m⁻¹) | EPP, Eq. 12 (N·m) | Material curve, strips (N·m) | $y_{NA}$ (mm) | RMS (µε) |
|---:|---:|---:|---:|---:|---:|---:|
«A6_table»

: Table K2. Part C (loading branch and unloading); model moments at the measured curvature.

At 40 kN ($M/M_Y$ = «A6_ratio»): measured $\kappa$ = «A6_kmax» m⁻¹, extreme strain «A6_emax» %. EPP predicts «A6_Mepp» N·m (+«A6_eppct» %), the strip summation with Lab 1's curve «A6_Mro» N·m (+«A6_ropct» %). **Flexure stress «A6_sflex» MPa vs actual «A6_sact» MPa: «A6_over» % too high.** **Permanent curvature: measured «A6_kres» m⁻¹, Eq. 14 «A6_kresp»: «A6_kresagree»** (elastic recovery «A6_kel» m⁻¹). The zero-load surface strains, ±«A6_eres» µε, are $\kappa_pc$. **Straightedge gap: measured «A6_gap» mm; Appendix D.9 with $\kappa_p$ confined to the middle 200 mm gives «A6_gapmid» mm.** The difference, «A6_gapdiff» mm (limit «A6_gaplim»), is real: the moment exceeds $M_Y$ in the shear spans beyond $x = M_Ya/M_{max}$ = «A6_xY» mm, so the bar also yielded near the load points. Integrating $\kappa_p(x) = \kappa(M(x)) - M(x)/(EI)$ along the whole bar, with $\kappa(M)$ interpolated from the measured loading curve, gives «A6_gapdata» mm, in agreement. (Expect only the first estimate from most students; the second is worth credit as an interpretation.) Surface residual stress on the tension side (strip summation, material curve): **«A6_res» MPa**. *Check:* $y_{NA}$ = «A6_yNA40» mm at 40 kN and the RMS residual «A6_rms40» µε vs «A6_rms20» at 20 kN in Part A. Per unit curvature, «A6_rmsk40» vs «A6_rmsk20» µε·m: the residual grows with $\kappa$ in the same pattern, the signature of gage-height errors (C3), so plane sections still hold. *Interpret:* aluminum's curve bends over before the 0.2 % offset point, so near yield the outer fibers carry less than $\sigma_Y$ and EPP overpredicts $M$. The same gradual yielding means the measured curvature at 4000 N·m is larger than EPP's «A6_kepp» m⁻¹, so the permanent set («A6_kres») is «A6_kp_ratio» times the bilinear EPP estimate («A6_kpepp» m⁻¹). Also worth credit: the transverse-to-longitudinal strain ratio on the top face rose to «A6_nueff» at 40 kN (plastic flow is incompressible, so the ratio heads toward 0.5); the bottom gage at $x$ = 150 mm, where $M \approx M_Y$ at 40 kN, kept «A6_x150r» µε of «A6_x150» µε: the plastic zone reached just to it, consistent with the gap.

**A7.** Use Table K1. Expected verdicts: every Table 5 row agrees except two model-form discrepancies. The moment at 40 kN: EPP is +«A6_eppct» % (the comparison's $U$ is about 1 %), and the material curve removes it. The straightedge gap: the middle-only estimate of D.9 is «A6_gappct» % low because the shear spans yielded too (A6). Full credit needs each discrepancy above $U$ explained with a named, quantified cause.

**M1.** (a) Flexure formula vs actual extreme-fiber stress (simulation, material curve): «M1_grow». At the preset curvature: «M1_flex» vs «M1_act» MPa, «M1_pct» % high (the readout's Difference column shows «M1_ro» % because it divides by the flexure value; accept either if the base is stated). The error grows quickly beyond $P_Y$ because $M$ keeps rising while the outer-fiber stress barely does. (b) At 40 kN's curvature, EPP is «A6_eppct» % above the material curve; the data follow the material curve («A6_ropct» %). (c) With the strip made of aluminum the neutral axis moves from «M1_true_y» to «M1_ign_y» mm (+«M1_dy» mm), and at $M$ = 1500 N·m the bottom stress would be predicted as «M1_sb_ign» MPa instead of «M1_sb_true» MPa: ignoring the strip underestimates the steel's stress by a factor of «M1_sb_ratio». (d) The RMS residual scales with $\kappa$ (A6), so compatibility (Eq. 3) holds through Part C. What failed is Hooke's law: Eqs. 5–6 assume a linear $\sigma$–$\varepsilon$ relation, and Eq. 12 assumes a flat plateau.

## 4. Challenge and Extension solutions

**C1.** Appendix D.6: $Z = bt_f(h - t_f) + t_wh_w^2/4$ = «C1_Z» × 10³ mm³, $S$ = «C1_S» × 10³ mm³, **$k$ = «C1_k»** (rectangle 1.5). The experiment ($\kappa$ = «C1_kk» $\kappa_Y$) gives $M/M_Y$ = «C1_M02», essentially fully plastic. $M_Y$ = «C1_MY» kN·m, $M_p$ = «C1_Mp» kN·m. In an I-section most of the material is already near $\pm\sigma_Y$ at first yield, so there is little left to mobilize; a rectangle's lightly stressed core can still pick up a lot. Design against collapse (plastic design) therefore gains 50 % for a rectangle but only about 14 % for an I-section; the I-section is still far more efficient per unit mass.

**C2.** Part B (elastic): errors «C2B_rows»; successive ratios «C2B_ratio» (4 for second order). Richardson from 20 and 40: relative error «C2B_rich». Part C with EPP: «C2_rows», ratios «C2_ratio»; the least-squares slope over $N_s$ = 2–256 on the plot is «C2_slopeAll». The midpoint rule is second order for a smooth integrand; the EPP stress has a kink at $\pm y_Y$, and the error contributed by the strip containing the kink depends on where in that strip the kink falls, so the error oscillates about an $N_s^{-2}$ trend. Triangular load: «C2_cant» (slope «C2_slope»). Four-point bending: the shear is piecewise constant and the load points are nodes, so the trapezoid rule integrates it exactly at any $N$ (largest error «C2_four»).

**C3.** (a) Every strain scales by $(1 + \delta)$, so $A_0$ and $A_1$ both scale and $y_{NA} = -A_0/A_1$ is unchanged while $\kappa$ scales. (b) Replacing $y_h$ by $y_h + d$ changes $A_0$ by $-A_1d$ and leaves $A_1$ unchanged. (c) For one gage, $\delta A_1/A_1 = -\delta y_j(y_j - \bar y)/\sum(y_i - \bar y)^2$ to first order; with $\sum(y_i - \bar y)^2$ = «C3_Sxx» mm², a 0.1 mm error changes $\kappa$ by at most «C3_dk» %. At 20 kN it is equivalent to a «C3_eps» µε strain error at that gage, which is how A2's residuals (1–3 µε) bound the gage-height errors to a few hundredths of a millimeter. None of these explains a discrepancy here; the gage factor (a) is the largest term in A3.

**X1.** Strains $\varepsilon = \varepsilon_0 - \kappa y_h$ in both layers (compatibility, perfect bond); stresses $E(\varepsilon - \alpha\Delta T)$; $N = 0$ and $M = 0$ give two linear equations for $\varepsilon_0$ and $\kappa$. With measured dimensions and $E$: **$\kappa/\Delta T$ = «X1_k» × 10⁻³ m⁻¹/K**, «X1_sense» because the aluminum on top expands more. At 50 K: $\kappa$ = «X1_k50» m⁻¹ (radius «X1_rho» m); interface stresses steel +«X1_st_i» MPa and aluminum «X1_al_i» MPa; steel bottom «X1_st_b» MPa; aluminum top «X1_al_t» MPa. *Check:* equal coefficients give $\kappa = 0$ and no stress. The interface shear needed to transfer these forces is concentrated near the ends, which is where bimetal bonds fail.

**X2.** Unloading from $M_{max}$ leaves $\sigma_{res}(c) = -\sigma_Y + M_{max}c/I = \sigma_Y(M_{max}/M_Y - 1)$ on the compression side (tension), and the opposite on the tension side. On reverse loading by $\Delta M$, the extreme fiber reaches $-\sigma_Y$ again (on the original tension side) when $\sigma_Y(1 - M_{max}/M_Y) - \Delta M c/I = -\sigma_Y$, i.e. after a total change of $2M_Y$ from $M_{max}$: reverse yield at $M = M_{max} - 2M_Y$. Since $M_{max} \le M_p = 1.5M_Y < 2M_Y$, unloading to zero never reverse-yields (the residual is at most 0.5 $\sigma_Y$). Reloading in the original direction is elastic up to $M_{max}$ (shakedown; the same idea as the autofrettage of gun barrels and the presetting of springs).

**X3.** T-section from the I-beam preset (flange 100 × 10 mm, web 6 mm, depth 200 mm, area «X3_A» mm²): elastic NA «X3_ybar» mm above the bottom; plastic NA «X3_yp» mm (equal areas, in the web just below the flange); strip summation at $10^4\kappa_Y$ puts it at «X3_ypS» mm with $M/M_p$ = «X3_MpS». $Z$ = «X3_Z» × 10³ mm³, $S$ (to the extreme fiber, at the bottom of the web) = «X3_S» × 10³ mm³, **$k$ = «X3_k»**. The elastic axis balances first moments of area; the plastic axis balances areas. They coincide only for a section symmetric about the neutral axis.

## 5. Design problem D1: reference solution

**D1.** $M_{max} = wL^2/8 + PL/4$ = **«D_M» kN·m** at midspan; $\delta_{allow}$ = $L/240$ = «D_dmax» mm. Steel: $\sigma_Y - U$ = «D_sY_s» MPa, allowable «D_sall_s» MPa, $S_{req}$ = «D_Sreq_s» × 10³ mm³, $I_{req}$ = «D_Ireq_s» × 10⁶ mm⁴ ($E$ = 205 GPa). Aluminum: «D_sY_a» MPa, «D_sall_a» MPa, $S_{req}$ = «D_Sreq_a» × 10³ mm³, $I_{req}$ = «D_Ireq_a» × 10⁶ mm⁴ ($E$ = «D_Eal» GPa, measured).

| Section | Mass (kg/m) | $\sigma_{max}$ (MPa) | $\delta$, steel (mm) | Acceptable |
|---|---:|---:|---:|---|
«D_table_s»

: Table K3. Steel candidates (stress is the same for both materials).

| Section | Mass (kg/m) | $\sigma_{max}$ (MPa) | $\delta$, aluminum (mm) | Acceptable |
|---|---:|---:|---:|---|
«D_table_a»

: Table K4. Aluminum candidates.

**Steel: «D_best_s»**, «D_bm_s» kg/m («D_bM_s» kg, about \$«D_bc_s»); utilization «D_bus_s» in stress and «D_bud_s» in deflection, so the two requirements are nearly balanced. **Aluminum: «D_best_a»**, «D_bm_a» kg/m («D_bM_a» kg, about \$«D_bc_a»); utilization «D_bus_a» in stress and «D_bud_a» in deflection: deflection governs, because aluminum's $E$ is a third of steel's while its strength is similar. The aluminum beam is about half the mass at about 1.5 times the cost; either is acceptable if justified. *Assumptions that could invalidate a design:* lateral–torsional buckling of the unbraced compression flange over 3 m (check bracing, or a buckling check that comes later in the course); local buckling of thin flanges (the catalog proportions are compact); load placement other than at midspan; long-term creep is not an issue for these metals at room temperature.

**Rubric detail (15 points total in the report).** Moment and requirements (3). Strength basis (3.75): $\sigma_Y - U$ from the student's Lab 1 data and measured $E$ for aluminum. Every requirement checked, governing one named for each material (3). Trade-off between at least two options with numbers (3.75). Presentation and assumption (1.5). Typical partial credit: $w$ in kN/m mixed with mm (−2); deflection not checked (−4, it governs aluminum); handbook values instead of measured (−1); $S$ and $I$ swapped (−2).

## 6. Expected ranges for real class data

| Quantity | Expected | If outside, suspect |
|---|---|---|
| RMS residual of the profile fit, Part A | 1–5 µε | a gage misplaced or debonded; wrong height recorded |
| $y_{NA}$, bar A | $h/2$ ± 0.3 mm | gage heights measured from the wrong face; bar not seated (twist) |
| $E$ of 6061-T6 (GPa) | 67–71 | gage factor setting; $h$ measured at the wrong place; $a$ wrong |
| $\nu$ from the top-transverse gage | 0.31–0.35 | gage not centered or not transverse |
| $V/P$ from the bottom gages | 0.45–0.55 | gage $x$ positions; local effect of the load roller at $x$ = 150 mm |
| Bar B NA (mm above bottom) | 23.5–24.5 | adhesive layer thickness; strip not 1018 |
| Permanent curvature after Part C (m⁻¹) | 0.06–0.10 | plateau of the particular bar; load overshoot |

: Table K5. Expected data ranges.

## 7. Common student mistakes

1. Measuring gage heights from the top instead of the bottom, or mixing $y$ (from the neutral axis) with $y_h$ (from the bottom).
2. Using $\sigma = Mc/I$ with $c$ measured to the far fiber of the composite instead of using the transformed section and the factor $n$.
3. Forgetting that $\kappa = -A_1$: a positive slope of strain against height means hogging.
4. Fitting $M$ against $\kappa$ through the unloading steps or the zero step, or forcing the line through the origin without saying so.
5. Using $P$ instead of $P/2$ in $M = (P/2)a$.
6. Computing $E$ from a single bottom gage with the handbook neutral axis, which hides the plane-sections test.
7. Applying Eq. 6 in Part C and calling 366 MPa the stress in an aluminum bar whose tensile strength is about 314 MPa.
8. Taking the permanent curvature as $\kappa_{max} - \kappa_Y$.
9. In A5, comparing the steel stress with $-My/I_t$ without the factor $n$.
10. In D1, checking stress only, or using the steel modulus for the aluminum beam.

## 8. Grading rubric

| Part | Points | Full credit | Common deductions |
|----------------|------:|----------------------------------------------------------|------------------------------|
| Pre-lab | 15 | P1–P6 correct with units; P1 an estimate made before measuring | P2(c) missing (−1); P4 inversion wrong (−2) |
| Data & procedure | 10 | Tables 3–4 complete; checks in steps 1–6 recorded | gage heights not measured (−3) |
| A1 | 6 | $M(x)$ from gages vs statics, $V/P$ with $U$, intercept check | $P/2$ error (−2) |
| A2 | 7 | profiles, $\kappa$, $y_{NA}$ with $U$, residual discussion | no residuals (−3) |
| A3 | 7 | $E$ with budget, comparison with Lab 2, flexure check | no budget (−3) |
| A4 | 5 | $\nu$ with $U$, $\rho'$, sign check | — |
| A5 | 8 | NA, $EI$, four stresses vs prediction, $\int\sigma\,dA$ check | factor $n$ missing (−3) |
| A6 | 8 | $M$–$\kappa$ with both models, flexure overstatement, permanent curvature, residual stress | elastic formula past yield (−3) |
| A7 | 4 | complete table, normalized figure, every discrepancy explained | unexplained discrepancy (−1 each) |
| M1 | 10 | (a)–(d) with simulation numbers and the plane-sections argument | no simulation numbers (−2 each) |
| D1 | 15 | see Sec. 5 | see Sec. 5 |
| Communication | 5 | labeled axes, units, $x \pm U$ format | each unlabeled axis (−1) |
| Challenge | +10 | C1 (3), C2 (4), C3 (3) | — |

: Table K6. Grading rubric (100 points plus up to 10 Challenge points). Core analysis A1–A7 totals 45.

Every Core answer must include the required check and interpretation; deduct 1 point per question where either is missing.

## 9. Instructor notes

**Before the lab.** Bars: 6061-T6, 25.4 × 50.8 mm (1 × 2 in) bar stock, 700 mm long. Bar A gets ten gages (five on one side face at 5, 15, 25.4, 35 and 45 mm, top, bottom and top-transverse at midspan, and two bottom gages at 100 and 150 mm from the left support); bar B gets eight. Bond the 6.35 mm 1018 strip to bar B with a structural epoxy (thin, uniform bond line; clamp while curing). Part C consumes one bar A per section run: either give each team its own bar (about 2.5 kg of 6061 bar per team) or run Part C once as a demonstration and share the data. Check the fixture's rollers turn freely; seized rollers add axial force and spoil the neutral axis.

**Timing (2 h).** 0:00–0:10 safety and pre-lab collection; 0:10–0:25 dimensions and gage heights; 0:25–0:55 Part A (eleven steps with holds); 0:55–1:20 Part B; 1:20–1:45 Part C; 1:45–2:00 straightedge check and simulation (step 8).

**Safety.** Demonstrate the overload stop and a controlled stop. Under 40 kN the 6061 bar deflects only a few millimeters, but a spreader that tips releases the load suddenly; insist on the centering check.

**Running without equipment.** Give students `sample_data.csv` and Appendix A of the handout; everything in this key applies unchanged. A good hybrid is to run Part A live (it is non-destructive) and use the sample data for Parts B and C.

**Your own class data.** Export the columns listed in Table A1 of the handout, one row per load step; fill a measurements JSON like `src/specimen_measurements.json`, with the class's Lab 1 and Lab 2 values in `reference`; run `src/lab04_analysis.py` and `src/make_key.py`.

**The simulation.** Students use it in P5, step 8, A6, M1, C1, C2 and X3. Its readout separates verification rows (closed form vs. integration or strip summation, "agree") from model-comparison rows ("different models"); the tests are in `tests/` and summarized in `tests/VERIFICATION.md`.

## 10. Self-critique and revisions

Before release, the lab was reviewed as a demanding instructor at a top program would review it. The three biggest weaknesses found, and the fixes made:

1. **The planned lab verified the flexure formula with a handbook modulus and an assumed neutral axis,** which is circular: it can only "confirm" what it assumes. *Fix:* seven gages through the depth measure the strain profile, so the neutral axis and curvature come from the data without assuming the material is elastic (Eq. 15). $E$ is measured from moment and curvature and compared with Lab 2, a transverse gage measures $\nu$ (A4), and the residuals test plane sections directly (A2, M1(d)).
2. **Shear and moment diagrams (§5.1–5.2) were drawn but never measured.** *Fix:* two bottom gages in the shear span turn strain into $M(x)$ and the moment gradient into $V$ (Eq. 16, A1), with an intercept check at the support. P2 adds the sensitivity to load-point placement.
3. **No test of where the formulas fail.** *Fix:* Part B tests the transformed section on a real two-material beam, including the equilibrium check $\int\sigma\,dA = 0$ from measured strains (A5). Part C loads past first yield and compares the measured moment–curvature curve with the EPP formula and with the material's own curve, quantifies the «A6_over» % overstatement of $Mc/I$, and predicts the permanent curvature (agreement: «A6_kres» vs «A6_kresp» m⁻¹).

**Known limitations (not fixed).** The truth model assumes a perfect bond and an elastic steel strip. It ignores the local contact stresses under the rollers, which affect the bottom gage at $x$ = 150 mm (50 mm from a load roller) in a real test; extrusion residual stresses, which make the onset of yield in a real bar less sharp; and the gages' transverse sensitivity (about 1 %). Part C consumes a bar.

# Lab 5 — Instructor Key: Transverse Shear

::: {custom-style="Instructor"}
**For instructors only. Do not distribute to students.** Every number in this key is computed by `src/lab05_analysis.py` (and `src/make_key.py`) from `sample_data.csv` and `src/specimen_measurements.json`, or by the simulation's own model code run in Node. To build a key for your own class data, put your CSV and measurements in the same format and run `python3 src/lab05_analysis.py your.csv your_measurements.json`, then `python3 src/make_key.py`. Uncertainties are expanded ($U = 2u$) unless marked $u$. Sign convention as in the handout (Beer 8e): $V$ and $M$ as in Fig. 5.6; $\tau_{xy} < 0$ for $V > 0$, reported as the magnitude $\tau = VQ/(It)$; deflection $y$ up, $\delta = -y$ reported.
:::

## 1. Results at a glance (sample data)

| Quantity | Measured | Reference or prediction | Verdict (Eq. 16) |
|---|---|---|---|
| Bar A: $b$, $h$ (mm) | «bA», «hA» | 25.4 × 50.8 nominal | — |
| $R$ at the faces, upright ($b/h$ = «A1_bh_up») | «A1_R_up» | Eq. 7: «A1_P_up» | «A1_ag_up» |
| $R$ at the faces, flat ($b/h$ = «A1_bh_fl») | «A1_R_fl» | Eq. 7: «A1_P_fl» | «A1_ag_fl» |
| I-beam web $\tau/V$ at the NA (10⁻³ mm⁻²) | see Table K2 | $Q/(It_w)$ | agree at all three heights |
| $E$ from the span series (GPa) | «A3_E» | Lab 2: 68.46 ± 0.94 | «A3_Eag» |
| $G$ from the span series (GPa) | «A3_G» | Lab 3: 26.03 ± 0.24 | «A3_Gag» |
| Span with a 5 % shear part (mm; $L/H$) | «A4_L5f» («A4_hf») | Eq. 9: «A4_L5p» («A4_hp») | agree |
| $EI_{eff}$ loose / bolted / bonded (N·m²) | «A5_EI_loose» / «A5_EI_bolted» / «A5_EI_bonded» | Eq. 11: «A5_EI0» / — / «A5_EIf» | loose and bonded agree |
| Bolt slip modulus $k_b$ (kN/mm) | «A6_kb» (discrete); «A6_kbs» (smeared) | — | — |
| Bolted end slip (10⁻⁹ m/N) | «A6_sm» | model with fitted $k_b$: «A6_sp» | agree («A6_sd» %) |
| D1 fewest bolts | stepped: «D_s_n»; uniform: «D_u_n» | — | — |

: Table K1. Results from the sample data.

The sample data were generated from a known "truth" model (`src/generate_sample_data.py`, values in `src/truth.json`). Part A: the Saint-Venant flexure solution for each orientation ($\nu$ = 0.330), a 0.3 mm load eccentricity (twist, opposite on the two faces), gages slightly off the neutral axis. Part B: $VQ/(It)$ in the web with ±1.5 % plate bending between the two sides; Timoshenko deflection with the energy shear factor. Part C: six discrete bolts of 40 kN/mm, an epoxy layer of finite stiffness, plus the shear deflection. Instrument errors: +0.4 % common gage-factor error, +0.3 % LVDT gain, reading noise. Because the gages read high and Lab 3's $G$ is 0.5 % above the truth, every measured shearing stress is about «A1_bias» % high, inside its uncertainty. The closure test in `tests/test_lab05_independent.py` confirms that the analysis recovers the truth values within their stated uncertainty.

## 2. Pre-lab solutions

**P1.** (a) $V$ = 7.5 kN, $A$ = «P1_A» mm², $\tau = 3V/2A$ = «P1_tau» MPa, $\gamma = \tau/G$ = «P1_g» µε, so $\varepsilon(+45°) - \varepsilon(-45°)$ = −«P1_g» µε (negative in the left half, P4). Largest bending stress under the load: $M = PL/4$ = «P1_M» N·m, $S$ = «P1_S» mm³, $\sigma$ = «P1_sig» MPa, top in compression and bottom in tension. (b) $A_w$ = «P1_Aw» mm²; $V$ = 10 kN gives $\tau \approx$ «P1_tweb» MPa and a pair difference of about «P1_gweb» µε. (c) Nominal I-beam: $I$ = «P1_I» × 10⁶ mm⁴, $A$ = «P1_AI» mm², $f_s \approx A/A_w$ = «P1_fsA». At 10 kN on 300 mm: bending «P1c_b300» mm, shear «P1c_s300» mm (shear «P1c_f300» % of the total); on 1200 mm: «P1c_b1200» mm and «P1c_s1200» mm («P1c_f1200» %). Shear dominates the short span; bending dominates the long one. (d) $EI_0$ = «P1d_EI0» N·m²; at 2 kN, loose «P1d_loose» mm, bonded «P1d_bond» mm (one quarter), loose end slip $rPL^2/(16EI_0)$ = «P1d_slip» mm. Units: N·mm³/(N/mm² × mm⁴) = mm.

**P2.** $I$ = «P2_I» × 10⁶ mm⁴. (a) $Q_{NA}$ = «P2_QNA» mm³, $\tau$ = «P2_tNA» MPa. (b) Web just below the flange: $Q = Bt_f(H - t_f)/2$ = «P2_Qf» mm³, $\tau$ = «P2_tj» MPa. (c) Flange just above: same $Q$, width $B$: «P2_tf» MPa. The shear flow $q = VQ/I$ is the same on both sides of the junction (Eq. 1); dividing by widths in the ratio «P2_ratio» gives the jump. Eq. 4: «P2_Aw» MPa, close to (a).

**P3.** For two equal layers, $Q = bt^2/2$ and $I = 2bt^3/3$, so $q = 3V/(4t)$ = «P3_q» N/mm at $V$ = 1.25 kN. At 100 mm spacing each bolt carries «P3_F» kN, an average shank stress of «P3_tb» MPa (high-strength shoulder bolts are needed). The loose interface carries no shear (apart from friction): each bar bends about its own axis, so $EI = 2 \times bt^3/12$ instead of $b(2t)^3/12$, a factor of 4.

**P4.** (a) Appendix D.2 of the handout: $\varepsilon(\pm45°) = \frac{1}{2}(\varepsilon_x + \varepsilon_y) \pm \frac{1}{2}\gamma$, with $\varepsilon_y = -\nu\varepsilon_x$, so the axial part is $\varepsilon_x(1 - \nu)/2$ on both gages. (b) In the left half, $V = +P/2$ (Beer), so $\tau_{xy} < 0$, $\gamma_{xy} < 0$ and the difference is negative; the sample data confirm it. (c) A slightly eccentric load twists the bar; torsion adds shear of opposite sign on opposite faces, which the average cancels (A1 reports the difference).

**P5.** Simulation, presets as shipped ($\nu$ = 0.33): upright $R$ = «sim_Rup», flat $R$ = «sim_Rflat» (center of the flat bar «sim_Rflat0»). I-beam: shear part «sim_f300» % at 300 mm and «sim_f1200» % at 1200 mm; 5 % at «sim_L5» mm; $f_s$ = «sim_fsI». Part C at 2.5 kN with six bolts: δ = «sim_dlay» mm (discrete springs), end slip «sim_slay» mm; loose «sim_dloose» mm and «sim_sloose» mm; glue «sim_dglue» mm.

**P6.** (a) Pinch points at rollers, load nose and yoke; specimens rolling or shifting sideways (flat bar, stacked bars); overload of the specimens, bolts or fixture (overload stops per test); handling the 5 kg I-beam. (b) The limits keep the bending stress below about half of $\sigma_Y$ in every test and the bolt forces below their rating. The flat bar's section modulus is half the upright one ($bh^2/6$ with $b$ and $h$ swapped), so the same bending stress is reached at half the load.

## 3. Analysis solutions

**A1.** Upright ($V$ to «A1_V_up» kN): **$R$ = «A1_R_up»** vs Eq. 7 «A1_P_up»: $|\Delta|$ = «A1_d_up» ≤ «A1_lim_up», «A1_ag_up». At the largest load, $\tau$ = «A1_tm_up» MPa vs $VQ/(Ib)$ = «A1_te_up» MPa ($\gamma$ = «A1_g_up» µε). Flat ($V$ to «A1_V_fl» kN): **$R$ = «A1_R_fl»** vs «A1_P_fl»: $|\Delta|$ = «A1_d_fl» ≤ «A1_lim_fl», «A1_ag_fl»; $\tau$ = «A1_tm_fl» vs «A1_te_fl» MPa. The two faces differ by ±«A1_tw_up» % (upright) and ±«A1_tw_fl» % (flat) about their mean: the twist from a slightly eccentric load, cancelled by averaging. *Check:* upright $b/h$ = 0.5 gives $R$ close to 1, as Eq. 7 requires as $b/h \to 0$. *Interpret:* for the flat bar, $VQ/(Ib)$ underestimates the largest shearing stress by «A1_under_fl» % (the elasticity value is «A1_err_fl» % above it). The section, $V$ and the average stress are the same in both orientations; only the shape of the stress distribution across the width changes, through Poisson's ratio.

| Height above mid-depth (mm) | $Q$ (mm³) | Measured $\tau/V$ (10⁻³ mm⁻²) | $Q/(It_w)$ (10⁻³ mm⁻²) | Difference (%) | Eq. 16 | Sides differ by (%) |
|---:|---:|---:|---:|---:|---|---:|
«A2_table»

: Table K2. Web shearing stress per newton of shear (I-beam: $I$ = «B_I» × 10⁶ mm⁴, $t_w$ = «B_tw» mm).

**A2.** Table K2. Measured section: $H$ = «B_H», $B$ = «B_B», $t_f$ = «B_tf», $t_w$ = «B_tw» mm; $u_I$ = «B_uI» %. All three heights agree with $Q/(It_w)$; the common +«A2_bias» % is the gage-factor and $G$ bias above. $1/A_w$ = «B_Awinv» × 10⁻³ mm⁻², within «A2_NA_Aw» % of the neutral-axis value. *Check:* $q$ at the junction is $VQ/I$ = «A2_qj» N/mm at $V$ = 10 kN on both sides; in the flange that is an average vertical stress of only «A2_tfl» MPa over the full width $B$. *Interpret:* the web carries «A2_web_share» % of $V$ (integral of $\tau t$ over the web), so it is nearly uniformly stressed: $V/A_w$ is a good design value, and the flanges carry the bending.

| Span (mm) | $L/H$ | Measured $\delta/P$ (µm/N) | Eq. 9 (µm/N) | Shear part, measured (%) | Shear part, Eq. 9 (%) |
|---:|---:|---:|---:|---:|---:|
«A4_table»

: Table K3. Compliance and shear part of the deflection (Eq. 9 with Table 1 values and $f_s$ = «B_fs»).

**A3.** Fit of $\delta/(PL)$ against $L^2$: slope «A3_a1» × 10⁻¹² N⁻¹mm⁻² (±«A3_ua1» %, $u$), intercept «A3_a0» × 10⁻⁹ N⁻¹ (±«A3_ua0» %). With $I$ = «B_I» × 10⁶ mm⁴ and $f_s$ = «B_fs» (energy integral for the measured section; $A/A_w$ = «B_fsA»): **$E$ = «A3_E» GPa** vs Lab 2: $|\Delta|$ = «A3_Ed» ≤ «A3_Elim», «A3_Eag». **$G$ = «A3_G» GPa** vs Lab 3: $|\Delta|$ = «A3_Gd» ≤ «A3_Glim», «A3_Gag». Both are about 0.3 % low because of the LVDT gain error, which scales slope and intercept equally. *Check:* slope units 1/(N·mm²) → $1/(48EI)$; intercept units 1/N → $f_s/(4GA)$. *Interpret:* the short spans fix the intercept (shear is 65 % of $\delta$ at 300 mm); the long spans alone have almost no shear and give $G$ with a large uncertainty. Using $f_s = A/A_w$ would have given $G$ = «A3_Gapprox» GPa («A3_Gapprox_pct» % high): the choice of $f_s$ matters as much as the measurement.

**A4.** Table K3. The 5 % span is **«A4_L5f» mm** from the fit ($L/H$ = «A4_hf») and «A4_L5p» mm from Eq. 9 ($L/H$ = «A4_hp»). On the 300 mm span, shear is «A4_EB300» % of the deflection: Euler–Bernoulli would underestimate it by a factor of «A4_EBx». *Check:* the shear fraction falls by about $(L_1/L_2)^2$ between spans at long spans. *Interpret:* the I-section puts its material in the flanges, which raises $I$ but leaves a thin web to carry $V$, so $EI/(GA_w)$ is large; a solid rectangle of the same depth reaches 5 % at about $L/H$ = «A4_rect».

**A5.** After removing the shear term (about «A5_dsh» % of the bonded compliance): loose **«A5_EI_loose»** N·m² vs $EI_0$ = «A5_EI0» («A5_loose_vs» %); bolted **«A5_EI_bolted»** ($EI/EI_0$ = «A5_r_bolted», $\eta$ = «A5_eta_bolted»); bonded **«A5_EI_bonded»** vs $EI_{full}$ = «A5_EIf» («A5_bond_vs» %, $\eta$ = «A5_eta_bonded»). Bonded/loose = «A5_ratio_lb». Loose end slip «A5_s_loose» × 10⁻⁹ m/N vs $rL^2/(16EI_0)$ = «A5_slipL»: «A5_slip_ag». *Check:* $b(2t)^3/12 \div (2 \times bt^3/12) = 4$. *Interpret:* bonding moves the material of each bar away from its own neutral axis to a distance $t/2$ from the common one; the parallel-axis terms triple the stiffness of the separate bars.

**A6.** Fitting the bolted deflection with the discrete-spring model gives **$k_b$ = «A6_kb» kN/mm**; the smeared closed form needs «A6_kbs» kN/mm («A6_kbd» %), because spreading six bolts uniformly misplaces their stiffness. **Predicted end slip «A6_sp» × 10⁻⁹ m/N vs measured «A6_sm»** («A6_sd» %): the model, fitted to deflection only, predicts the slip, which validates it. At «A6_Pb» kN the bolt forces from the springs are «A6_Flist» kN (outer to inner, each half); Eq. 5 with a rigid connection ($q$ = «A6_q» N/mm) gives «A6_Fb» kN for every bolt in the shear span, «A6_Fover» % above the largest spring value. Largest shank stress «A6_tb» MPa. Glue: $\tau = VQ/(Ib)$ = «A6_tg» MPa at «A6_Pg» kN. *Check:* the predicted slip lies between 0 and the loose value. *Interpret:* the bolts slip, so the layers carry part of the moment separately and the interface force is lower than for a rigid bond; the force is largest at the outer bolt, where the slip is largest, and smallest near midspan, where the slip vanishes by symmetry.

**A7.** Use Table K1. Expected verdicts: every row agrees. Full credit needs Table 5 complete, a normalized figure with error bars, and each discrepancy above $U$ explained with a named, quantified cause.

**M1.** (a) Flat bar ($b/h$ = 2, $\nu$ = 0.33): the face stress is «M1_flat» % above $VQ/(Ib)$, matching A1. (b) 300 mm span: $\delta/\delta_{bending}$ = «M1_short»: Euler–Bernoulli underestimates the deflection by that factor. (c) Part C at 2.5 kN: largest bolt force «M1_Fd» kN (springs) vs «M1_Fb» kN (Eq. 5). "Few bolts" ($s$ = 300 mm, «M1_few_n» bolts): deflection smeared «M1_few_sm» mm vs discrete «M1_few_d» mm («M1_few_pct» %), but the end slip differs by «M1_few_s» %, and Eq. 5 gives «M1_few_Fb» kN per bolt against «M1_few_Fd» kN from the springs. Smearing is acceptable when the spacing is well below $1/\alpha$ («M1_ia» mm for the lab's six bolts; «M1_ia_few» mm with 300 mm spacing). (d) With $G_g$ = 50 MPa and a 1 mm layer, $\eta$ = «M1_soft_eta». For a 0.15 mm layer, $\eta$ falls below 0.95 only when $G_g$ < «M1_G95» MPa; a structural epoxy (about 1 GPa) gives $\eta$ = «M1_etaLab», so the lab's bonded pair is effectively rigid.

## 4. Challenge and Extension solutions

**C1.** Appendix D.4: $f_s$ = 6/5. For the measured I-beam, $f_s$ = «B_fs» (flanges and web; the simulation agrees), while $A/A_w$ = «B_fsA». Using $A/A_w$ in A3 raises $G$ by «A3_Gapprox_pct» %. The energy factor is the consistent choice with Eq. 9; the difference shows that "shear area" approximations are good to only about 10 % for I-sections.

**C2.** Flat bar: «C2_rows». Successive differences shrink by «C2_ratio» (4 for second order). Richardson from 32 and 64: «C2_rich» vs series «sim_Rflat». With $\nu = 0$ the right-hand side of the stress-function equation vanishes, $\phi = 0$, and $VQ/(Ib)$ is exact.

**C3.** Slender cantilever (1 m): «C3_rows» (percent of the closed-form deflection). With full integration the element enforces $w' = \theta$ at two points, which a linear $w$ and linear $\theta$ can satisfy only with no bending: the element "locks". Reduced integration enforces it on average, and the error is $O(N^{-2})$. Locking worsens as $L/h$ grows because the shear stiffness $GA/L$ dominates the bending stiffness $EI/L^3$ by $(L/h)^2$.

**X1.** Appendix D.5. Loose: $k \to 0$ gives $N = 0$, $\delta = PL^3/(48EI_0)$, and $s_0 = r\int_0^{L/2}\kappa\,dx = r\theta_{end}$. Rigid: $k \to \infty$ gives $\delta = PL^3/(48EI_{full})$ and $s_0 \to 0$.

**X2.** In a flange the horizontal shear flow at distance $s$ from the tip is $q = Vt_fs\,d/I$ with $d = (H - t_f)/2$, linear in $s$. At the web face each half delivers «X2_qh» N/mm for $V$ = 10 kN; the part of the flange directly above the web adds «X2_qw» N/mm; the total, «X2_qj» N/mm, equals $VQ/I$ in the web at the junction (A2).

**X3.** From the simulation, $\eta$ = 0.95 needs $G_g$ ≈ «M1_G95» MPa for a 0.15 mm layer. Hot-cured epoxies drop by an order of magnitude in modulus above their glass transition and creep under sustained load, so a bonded beam under a permanent load in a hot environment slowly loses composite action (more deflection, and stress moves from the bond into the layers).

## 5. Design problem D1: reference solution

**D1.** $V_{max} = wL/2$ = «D_V» kN, $M_{max} = wL^2/8$ = «D_M» kN·m ($\sigma$ = «D_sig» MPa, $\tau$ at the interface «D_tau» MPa: both far below the limits). At the support $q = 3V/(4t)$ = «D_q0» N/mm, so the spacing there must not exceed «D_smax» mm. With $k_b$(M10) = «D_kb» kN/mm (from the A6 fit), $\delta_{full}$ = «D_full» mm, $\delta_{loose}$ = «D_loose» mm, limit $L/300$ = «D_allow» mm.

| Pattern | Bolts | Largest $F$, Eq. 5 (kN) | Largest $F$, springs (kN) | δ (mm) |
|---|---:|---:|---:|---:|
| Uniform, $s$ = «D_u_s» mm | «D_u_n» | «D_u_F» | «D_u_Fm» | «D_u_d» |
| Stepped, $s_1$ = «D_s_s1» mm over «D_s_e» mm at each end, $s_2$ = «D_s_s2» mm | «D_s_n» | «D_s_F» | «D_s_Fm» | «D_s_d» |

: Table K4. Reference designs (search in 5 mm steps; the stepped pattern is the fewest-bolt solution found).

The bolt-force requirement governs both patterns: the shear flow falls linearly toward midspan, so wider spacing in the middle saves «D_s_save» bolts. Both patterns meet the deflection limit with some margin. The spring model's largest force is about 15 % below Eq. 5, so Eq. 5 is conservative here. *Assumptions that could invalidate a design:* the linear scaling of $k_b$ with bolt diameter (check with a single-bolt push-out test); hole clearance, which adds slip before the bolts bear (use fitted bolts or check the slip at service load); bearing stress on the aluminum around the holes; fatigue of the bolts under repeated walkway loads.

**Rubric detail (15 points total in the report).** V, M, q and the spacing limit (3). Measured $k_b$ and $E$ in the deflection check (3.75). Both requirements checked, governing one named (3). At least two patterns compared with numbers (3.75). Presentation and assumption (1.5). Typical partial credit: $Q$ of the whole section instead of one bar (−2); deflection with a rigid bond (−3); spacing from $V$ at midspan (−2).

## 6. Expected ranges for real class data

| Quantity | Expected | If outside, suspect |
|---|---|---|
| $R$ upright / flat | 1.02–1.07 / 1.42–1.58 | gage pair not at mid-height; wrong orientation; $G$ value |
| Two faces differ by | < 10 % | load nose off center (twist) |
| Web $\tau/V$ vs $Q/(It_w)$ | ±3 % | $t_w$ measured with calipers; gage not on the web centerline |
| $E$ from the span series (GPa) | 67–71 | yoke seated badly; span error |
| $G$ from the span series (GPa) | 24–28 | short-span local effects; wrong $f_s$ |
| $EI$ bonded / loose | 3.8–4.0 | glue line too thick, or bars not flat |
| $k_b$ for an M6 bolt (kN/mm) | 20–80 | hole clearance (lower), friction from over-tightened bolts (higher) |

: Table K5. Expected data ranges.

## 7. Common student mistakes

1. Using $Q$ of the whole section, or the area below the neutral axis with the wrong sign.
2. Using the full width $B$ instead of $t_w$ in the web, or the reverse in the flange.
3. Converting $\gamma$ to $\tau$ with $E$ instead of $G$, or taking one gage's reading as $\gamma$ (a factor of 2).
4. Forgetting to average the two faces, then reporting the twist as a model error.
5. Fitting $\delta$ against $L^3$ and attributing the short-span excess to "machine compliance".
6. Using $A/A_w$ for $f_s$ without saying so.
7. In A5, comparing the bonded pair with the loose one without removing the small shear term, or using $b(2t)^3/12$ with $t$ the total depth.
8. Computing bolt forces with $V$ at midspan, or spacing bolts uniformly at the midspan requirement.
9. In A6, treating the end slip as a fitted quantity instead of an independent check.
10. Calling the flat-bar discrepancy "experimental error" instead of a known limitation of Eq. 2.

## 8. Grading rubric

| Part | Points | Full credit | Common deductions |
|----------------|------:|----------------------------------------------------------|------------------------------|
| Pre-lab | 15 | P1–P6 correct with units; P1 an estimate made before measuring | P4(b) sign missing (−1) |
| Data & procedure | 10 | Tables 3–4 complete; checks recorded | $t_w$ with calipers (−2) |
| A1 | 7 | $R$ in both orientations with $U$, comparison with Eq. 7, faces | single face only (−2) |
| A2 | 6 | three heights vs $Q/(It_w)$ and $V/A_w$, continuity check | width wrong (−3) |
| A3 | 7 | linearized fit, $E$ and $G$ with $U$, comparison with Labs 2–3 | $f_s$ unstated (−2) |
| A4 | 6 | shear fraction per span, 5 % span, Euler–Bernoulli error | — |
| A5 | 7 | three $EI_{eff}$, ratios, $\eta$, loose slip | shear term ignored without comment (−1) |
| A6 | 8 | $k_b$ fit, slip prediction vs measurement, bolt forces vs Eq. 5, glue stress | slip fitted, not predicted (−3) |
| A7 | 4 | complete table, normalized figure, every discrepancy explained | unexplained discrepancy (−1 each) |
| M1 | 10 | (a)–(d) with simulation numbers | no simulation numbers (−2 each) |
| D1 | 15 | see Sec. 5 | see Sec. 5 |
| Communication | 5 | labeled axes, units, $x \pm U$ format | each unlabeled axis (−1) |
| Challenge | +10 | C1 (3), C2 (3), C3 (4) | — |

: Table K6. Grading rubric (100 points plus up to 10 Challenge points). Core analysis A1–A7 totals 45.

Every Core answer must include the required check and interpretation; deduct 1 point per question where either is missing.

## 9. Instructor notes

**Before the lab.** Bar A is the Lab 4 bar (Part A or B of Lab 4, not the Part C bar, which has a permanent set): add a ±45° pair at the middle of each long face at one station. I-beam: any 6061-T6 extruded I-section about 100 mm deep works; enter its dimensions. Bond the web gage pairs on both sides at the same heights. Part C: three pairs of 50.8 × 12.7 mm bars; drill and ream the bolted pair together (six holes, 100 mm pitch, symmetric) and use shoulder bolts, snug-tight; bond the third pair with a structural epoxy under clamping pressure and let it cure fully. Put a PTFE sheet between the loose pair.

**Timing (2 h).** 0:00–0:10 safety and pre-lab; 0:10–0:20 dimensions; 0:20–0:40 Part A (two orientations); 0:40–1:20 Part B (web, then five spans; changing spans takes most of the time); 1:20–1:50 Part C (three pairs); 1:50–2:00 simulation (step 7). If time is short, run three spans (300, 600, 1200 mm) in Part B; A3 still works.

**Safety.** The flat bar and the stacked bars can slide sideways on the rollers; use roller cradles or side stops. Check the bolt torque before the bolted test.

**Running without equipment.** Give students `sample_data.csv` and Appendix A; everything in this key applies unchanged. A good hybrid is to run Part A live (both orientations take 15 minutes) and use the sample data for Parts B and C.

**Your own class data.** Export the columns listed in Table A1; fill a measurements JSON like `src/specimen_measurements.json`, with the class's Lab 2 and Lab 3 values in `reference`; run `src/lab05_analysis.py` and `src/make_key.py`.

**The simulation.** Students use it in P5, step 7, A1, A3, A6, M1, C1–C3, X3 and D1. Its readout separates verification rows ("agree") from model comparisons ("different models"); the tests are in `tests/` and summarized in `tests/VERIFICATION.md`.

## 10. Self-critique and revisions

Before release, the lab was reviewed as a demanding instructor at a top program would review it. The three biggest weaknesses found, and the fixes made:

1. **τ = VQ/It was to be "verified" on a narrow section with a handbook G,** where it is right by construction. *Fix:* the same bar is tested upright and flat, with $G$ carried over from Lab 3, so the measurement shows where the formula fails (A1: «A1_under_fl» % under-estimate at $b/h$ = 2). The elasticity correction is computed two independent ways in the simulation, and the I-beam web profile tests $Q/(It)$ at three heights.
2. **The planned loose/bolted/bonded stack was a qualitative demonstration,** and Eq. 5 assumes a rigid connection that bolts do not provide. *Fix:* a partial-interaction model (closed form, finite differences, discrete springs) with the bolt stiffness fitted to the deflection and then checked against the independently measured end slip (A6: «A6_sd» %). Eq. 5 is compared with the spring forces, and D1 uses the measured $k_b$.
3. **Shear deformation was to be shown in the simulation only,** and a real short-span test mixes it with fixture compliance. *Fix:* a yoke referenced to the supports and five spans; Eq. 10 separates bending and shear, giving $E$ and $G$ from one beam for comparison with Labs 2 and 3 (A3).

**Known limitations (not fixed).** The truth model uses Timoshenko beam theory with the energy shear factor; at $L/H$ ≈ 3 the real elastic field near the load differs by a few percent, which the sample data do not contain. The bolts are modeled as linear springs with no hole clearance or friction. The glue is linear elastic. The web gage pairs are assumed to sit exactly at mid-thickness of the web plate; real pairs on a 4.8 mm web pick up some web bending, which averaging the two sides removes.

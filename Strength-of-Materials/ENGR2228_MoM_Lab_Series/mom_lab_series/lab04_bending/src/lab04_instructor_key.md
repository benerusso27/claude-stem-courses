# Lab 4 — Instructor Key: Bending

::: {custom-style="Instructor"}
**For instructors only. Do not distribute to students.** Every number in this key is computed by `src/lab04_analysis.py` (and `src/make_key.py`) from `sample_data.csv` and `src/specimen_measurements.json`, or by the simulation's own model code run in Node. To build a key for your own class data, put your CSV and measurements in the same format and run `python3 src/lab04_analysis.py your.csv your_measurements.json`, then `python3 src/make_key.py`. Uncertainties are expanded ($U = 2u$) unless marked $u$. Sign convention as in the handout (Beer 8e): $V$ and $M$ as in Fig. 5.6, $M > 0$ sagging, $\sigma_x = -My/I$ with $y$ up from the neutral axis, tension positive.
:::

## 1. Results at a glance (sample data)

| Quantity | Measured | Reference or prediction | Verdict (Eq. 18) |
|---|---|---|---|
| Bar A: $b$, $h$ (mm); $I$ (10⁵ mm⁴) | 25.420 ± 0.026, 50.780 ± 0.026; 2.7738 ($u_I$ = 0.092 %) | 25.4 × 50.8 nominal | — |
| Shear span $a$ (mm) | 200.00 ± 0.41 | 200 | — |
| $V/P$ in the left shear span (A1) | 0.5005 ± 0.0242 | 0.5 (Eq. 2) | agree |
| Neutral axis, bar A (mm above bottom) | 25.392 ± 0.026 | $h/2$ = 25.390 | agree |
| $E$ of 6061-T6 from $M$–$\kappa$ (GPa) | 68.39 ± 0.90 | Lab 2: 68.46 ± 0.94 | agree |
| $\nu$ from anticlastic strain | 0.3294 ± 0.0059 | Lab 2: 0.330 ± 0.006 | agree |
| Neutral axis, bar B (mm above bottom) | 23.985 ± 0.039 | Eq. 9: 23.95 ± 0.18 | agree |
| $EI$, bar B (N·m²) | 38 606 ± 64 | $E_1I_t$: 38 751 ± 808 | agree |
| $M$ at 40 kN and $\kappa$ = 0.2935 m⁻¹ (N·m) | 4 000 | EPP 4 054; material curve 4 003 | EPP +1.34 %; curve +0.07 % |
| Flexure stress vs actual at 40 kN (MPa) | actual 282.0 | $Mc/I$ = 366.2 | overstated 29.8 % |
| Permanent curvature (m⁻¹) | 0.0827 | Eq. 14: 0.0826 ± 0.0028 | agree |
| Straightedge gap after Part C (mm) | 2.85 ± 0.05 | middle 200 mm only: 2.48 ± 0.09; whole bar from the measured $M$–$\kappa$: 2.87 | gap 15 % larger: shear spans yielded too |
| D1 lightest acceptable section | steel I-120, aluminum I-160 | — | — |

: Table K1. Results from the sample data.

The sample data were generated from a known "truth" model (`src/generate_sample_data.py`, values in `src/truth.json`): plane sections, 6061-T6 following Lab 1's Ramberg–Osgood curve ($E$ = 68.9 GPa), the steel strip elastic, a common +0.5 % gage-factor error, true gage heights that differ from the recorded ones by a few hundredths of a millimeter, load points 0.4 mm inside their nominal positions, and 1 µε reading noise. Because every strain reads 0.5 % high, the measured $E$ is 0.5 % low: correct for the gages, invisible to the student, and inside the stated uncertainty. The closure test in `tests/test_lab04_independent.py` confirms that the analysis recovers the truth values within their stated uncertainty.

## 2. Pre-lab solutions

**P1.** (a) $I = bh^3/12$ = 2.7749 × 10⁵ mm⁴, $S$ = 10 925 mm³. At 20 kN, $M = (P/2)a$ = 2 000 N·m, $\sigma_m = M/S$ = 183.1 MPa, $\varepsilon = \sigma/E$ = 2 674 µε, $\kappa = M/(EI)$ = 0.1053 m⁻¹, $\rho$ = 9.50 m. (b) $M_Y = \sigma_Y S$ = 2 990 N·m, so $P_Y = 2M_Y/a$ = 29.90 kN; $M_p = 1.5M_Y$ gives 44.85 kN. Part C's 40 kN is 1.338 $P_Y$ and 0.892 $P_p$: well into the plastic range but short of collapse. (c) At 2.5 kN the bottom strain is about 334 µε, so 1 µε is 0.30 %. (d) $V/(bh)$ = 7.75 MPa, 4.2 % of the bending stress (the parabolic maximum, 11.6 MPa, is Lab 5's subject). Units: N·m/mm³ → MPa after ×10³; µε = 10⁻⁶.

**P2.** (a) Figure 2: $V = P/2$, 0, $-P/2$; integrating, $M$ rises to $Pa/2$, stays flat, and falls by $Pa/2$ to zero at $L$. (b) $a_1 + a_2 = L$, so the loads are still symmetric: $R_A = R_B = P/2$, and $M = (P/2)a_1$ = 100.200 × 10⁻³ $P$ (m), 0.200 % above Eq. 2. The middle is still in pure bending. (c) $R_A$ = 0.50033 $P$ and $R_B$ = 0.49967 $P$ (Appendix D.1); between the loads $V = R_A - P/2$ = 0.000333 $P$, so $M$ changes by 0.067 % across the middle third. Strictly not pure bending, but far below anything the gages can see. *Lesson:* the measurement is insensitive to small load-point errors because the moment in the middle depends on $a$ only to first order.

**P3.** $n = 205/68.46$ = 2.9944. With $y$ from the bottom of the strip, transformed areas $n b t_s$ at $t_s/2$ and $bh$ at $t_s + h/2$: $\bar y$ = 23.967 mm and $I_t$ = 5.6607 × 10⁵ mm⁴ (bar alone: 2.7749 × 10⁵ mm⁴; ratio 2.040). At 15 kN, $M$ = 1 500 N·m: steel bottom +190.2 MPa; interface aluminum +46.68 MPa and steel +139.8 MPa (ratio $n$); aluminum top −87.9 MPa. (b) $t_s \to 0$: $\bar y \to h/2$ and $I_t \to bh^3/12$. $n = 1$: a homogeneous bar of depth $h + t_s$, with $\bar y = (h + t_s)/2$.

**P4.** (a) $M_Y$ = 2 990 N·m, $\kappa_Y = \sigma_Y/(Ec)$ = 0.1574 m⁻¹, $M_p$ = 4 485 N·m. (b) $M/M_Y$ = 1.3378; Eq. 12 gives $(\kappa_Y/\kappa)^2 = 3(1 - M/1.5M_Y)$, so $\kappa_Y/\kappa = y_Y/c$ = 0.5696, $\kappa$ = 0.2763 m⁻¹, and the elastic core is ±14.47 mm. (c) Elastic recovery $M/(EI)$ = 0.2106 m⁻¹, so $\kappa_p$ = 0.0657 m⁻¹. Residual stress: top $-\sigma_Y + Mc/I$ = −273.7 + 366.1 = +92.4 MPa (tension), bottom −92.4 MPa. (d) $-\int y\sigma_{res}\,dA = M - M = 0$ (Appendix D.7); students may also integrate the piecewise-linear residual distribution numerically.

**P5.** Simulation, presets as shipped (nominal section, $E$ = 68.9 GPa). Part A: $M$ = 2 000 N·m, largest $|\sigma|$ = 183.1 MPa. Part B: elastic NA 24.004 mm, $I_t$ = 5.6472 × 10⁵ mm⁴ (slightly different from P3 because the page uses $E$ = 68.9 GPa). Part C at $\kappa$ = 0.292 m⁻¹: material curve 4 008 N·m, EPP 4 060 N·m (+1.28 %). The EPP law is larger: aluminum's curve bends over before $\sigma_Y$ (the 0.2 % offset point), so the outer fibers carry less than $\sigma_Y$ just past yield, and Part C's strains are not yet large enough for the hardening to make it up. "Overload, then unload" ($\kappa = 3\kappa_Y$ = 0.4697 m⁻¹, $M$ = 1.4444 $M_Y$): permanent curvature 0.2435 m⁻¹.

**P6.** (a) Pinch points at the rollers and spreader (hands clear when the crosshead can move); stored elastic energy if the bar shifts or a roller slips (bar centered and square, stop on a load drop); overloading the bar or fixture (overload stop set per part); manual handling of 2.5 kg bars. (b) Part C bends the bar permanently, so it must come after Part A, which needs an undamaged bar; an overload stop set before the plastic part is the only protection against running past 40 kN toward collapse at about 44.85 kN, where the deflection would grow quickly.

## 3. Analysis solutions

**A1.** Slopes of bottom strain against $P$ converted with $M = ES\varepsilon$ ($E$ from A3): $M/P$ = 49.91 mm at $x$ = 100 mm (statics 50.0, −0.18 %), 74.94 mm at 150 mm (75.0, −0.08 %) and 100.06 mm at midspan (100.0, 0.06 %); each ±0.67 % ($u$, mostly from $E$). **$V/P$ = 0.5005 ± 0.0242**, $|\Delta|$ = 0.0005 ≤ 0.0242: agree. *Check:* the line through the two shear-span points meets $M = 0$ at $x$ = 0.28 mm, at the support, as a pin must require. *Interpret:* the slope of the moment diagram is the reaction ($V = R_A$ in the shear span); between the loads both load points' halves cancel, so the slope, $V$, is zero. The shear is a difference of two nearly equal moments, which is why its relative uncertainty (about 2.4 %, $u$) is several times that of $M$.

**A2.** 11 steps above 1 kN. Curvature: 0.02637 m⁻¹ at 5 kN, 0.05268 at 10 kN, 0.10540 at 20 kN (linear in load). RMS residuals 0.79–3.10 µε (1.81 at 20 kN). At 20 kN, top −2 675 µε and bottom 2 677 µε. **$y_{NA}$ = 25.392 ± 0.026 mm** vs $h/2$ = 25.390 mm: difference 0.002 mm, within 0.026. *Check:* residuals at the 1–3 µε level with no curvature in the profile; equal and opposite extreme strains. *Interpret:* a curved profile would mean sections warp (or a gage is misplaced); residuals growing with load in the same pattern would mean gage-height errors (C3), not physics.

**A3.** 11 loading steps; slope $EI$ = 18 971 N·m². **$E$ = 68.39 ± 0.90 GPa** vs Lab 2 68.46 ± 0.94: $|\Delta|$ = 0.07 ≤ 1.30, agree. Budget ($u$, %): fit 0.031, $b$ 0.051, $3u_h/h$ 0.076, $a$ 0.102, load cell 0.289, gage factor 0.577; total 0.661 %. At 20 kN: flexure formula 183.0 MPa vs $E\varepsilon$ = 183.1 MPa ($\varepsilon$ = 2 677 µε). *Check:* slope units N·m/(m⁻¹) = N·m²; $I \propto h^3$ so 1 % in $h$ is 3 % in $E$. *Interpret:* the gage factor dominates. A common gage-factor error scales every strain, so it scales $\kappa$ and biases $E$, but it cancels in $y_{NA} = -A_0/A_1$ (C3).

**A4.** **$\nu$ = 0.3294 ± 0.0059** vs 0.330 ± 0.006: agree. At 20 kN $\rho$ = 9.49 m, so $\rho' = \rho/\nu$ = 28.8 m. *Check:* the compressed top widens, so the transverse gage there reads positive (882 µε at 20 kN). *Interpret:* the anticlastic curvature makes the top face slightly saddle-shaped; near the edges the transverse strain is affected by the free edges and the gage's finite length, so a centered gage is best (§4.3 assumes the section is free to deform).

**A5.** Measured **NA 23.985 ± 0.039 mm** vs Eq. 9 with measured dimensions and $n$ = 2.9974: **23.95 ± 0.18 mm**; $|\Delta|$ = 0.033 ≤ 0.186, agree (the prediction's uncertainty is dominated by $E_{steel}$). All-aluminum bar of the same depth: 28.57 mm. **$EI$ = 38 606 ± 64 N·m²** vs $E_1I_t$ = **38 751 ± 808** (−0.38 %), agree. At 14.993 kN ($M$ = 1 499.3 N·m), from the fitted strain line (RMS 1.36 µε): steel bottom 190.8 MPa (predicted 190.0, 0.41 %), aluminum interface 46.8 (46.6), steel interface 140.1 (139.5), aluminum top −88.1 (−87.8). $\int\sigma\,dA$ = 0.17 % of the compressive resultant. *Check:* it must vanish in pure bending (first of Eqs. 4); the small remainder is the strain-line fit and the 0.5 % gage-factor bias, which cancels in ratios. *Interpret:* the composite is 2.035 times as stiff as bar A (18 971 N·m²); the steel's bottom fiber is the most highly stressed point, about twice the aluminum's top.

**A6.** Table K2 lists the Part C steps. $M_Y$ = 2 990 N·m, $M_p$ = 4 485 N·m, $\kappa_Y$ = 0.1576 m⁻¹ (measured $E$, Lab 1 $\sigma_Y$).

| $P$ (kN) | $M$ (N·m) | $\kappa$ (m⁻¹) | EPP, Eq. 12 (N·m) | Material curve, strips (N·m) | $y_{NA}$ (mm) | RMS (µε) |
|---:|---:|---:|---:|---:|---:|---:|
| 5.0 | 501 | 0.0264 | 500 | 500 | 25.40 | 0.3 |
| 10.0 | 1 000 | 0.0526 | 999 | 999 | 25.40 | 2.0 |
| 15.0 | 1 501 | 0.0791 | 1 500 | 1 500 | 25.40 | 2.2 |
| 20.0 | 2 000 | 0.1054 | 1 999 | 1 999 | 25.40 | 2.3 |
| 25.0 | 2 501 | 0.1323 | 2 509 | 2 499 | 25.39 | 3.9 |
| 28.0 | 2 801 | 0.1500 | 2 846 | 2 800 | 25.39 | 4.1 |
| 31.0 | 3 100 | 0.1712 | 3 218 | 3 100 | 25.39 | 4.5 |
| 34.0 | 3 400 | 0.1986 | 3 544 | 3 401 | 25.39 | 4.8 |
| 37.0 | 3 700 | 0.2365 | 3 821 | 3 702 | 25.39 | 5.7 |
| 40.0 | 4 000 | 0.2935 | 4 054 | 4 003 | 25.39 | 6.6 |

: Table K2. Part C (loading branch and unloading); model moments at the measured curvature.

At 40 kN ($M/M_Y$ = 1.338): measured $\kappa$ = 0.2935 m⁻¹, extreme strain 0.745 %. EPP predicts 4 054 N·m (+1.34 %), the strip summation with Lab 1's curve 4 003 N·m (+0.07 %). **Flexure stress 366.2 MPa vs actual 282.0 MPa: 29.8 % too high.** **Permanent curvature: measured 0.0827 m⁻¹, Eq. 14 0.0826 ± 0.0028: agree** (elastic recovery 0.2109 m⁻¹). The zero-load surface strains, ±2 099 µε, are $\kappa_pc$. **Straightedge gap: measured 2.85 ± 0.05 mm; Appendix D.9 with $\kappa_p$ confined to the middle 200 mm gives 2.48 ± 0.09 mm.** The difference, 0.37 mm (limit 0.10), is real: the moment exceeds $M_Y$ in the shear spans beyond $x = M_Ya/M_{max}$ = 149.5 mm, so the bar also yielded near the load points. Integrating $\kappa_p(x) = \kappa(M(x)) - M(x)/(EI)$ along the whole bar, with $\kappa(M)$ interpolated from the measured loading curve, gives 2.87 mm, in agreement. (Expect only the first estimate from most students; the second is worth credit as an interpretation.) Surface residual stress on the tension side (strip summation, material curve): **−84.2 MPa**. *Check:* $y_{NA}$ = 25.39 mm at 40 kN and the RMS residual 6.58 µε vs 1.81 at 20 kN in Part A. Per unit curvature, 22.4 vs 17.2 µε·m: the residual grows with $\kappa$ in the same pattern, the signature of gage-height errors (C3), so plane sections still hold. *Interpret:* aluminum's curve bends over before the 0.2 % offset point, so near yield the outer fibers carry less than $\sigma_Y$ and EPP overpredicts $M$. The same gradual yielding means the measured curvature at 4000 N·m is larger than EPP's 0.2768 m⁻¹, so the permanent set (0.0827) is 1.25 times the bilinear EPP estimate (0.0659 m⁻¹). Also worth credit: the transverse-to-longitudinal strain ratio on the top face rose to 0.408 at 40 kN (plastic flow is incompressible, so the ratio heads toward 0.5); the bottom gage at $x$ = 150 mm, where $M \approx M_Y$ at 40 kN, kept 138 µε of 4 144 µε: the plastic zone reached just to it, consistent with the gap.

**A7.** Use Table K1. Expected verdicts: every Table 5 row agrees except two model-form discrepancies. The moment at 40 kN: EPP is +1.34 % (the comparison's $U$ is about 1 %), and the material curve removes it. The straightedge gap: the middle-only estimate of D.9 is 15 % low because the shear spans yielded too (A6). Full credit needs each discrepancy above $U$ explained with a named, quantified cause.

**M1.** (a) Flexure formula vs actual extreme-fiber stress (simulation, material curve): 30 kN: 275 vs 252 MPa (9 %); 35 kN: 320 vs 268 MPa (19 %); 40 kN: 366 vs 282 MPa (30 %). At the preset curvature: 366.9 vs 282.3 MPa, 30.0 % high (the readout's Difference column shows 23 % because it divides by the flexure value; accept either if the base is stated). The error grows quickly beyond $P_Y$ because $M$ keeps rising while the outer-fiber stress barely does. (b) At 40 kN's curvature, EPP is 1.34 % above the material curve; the data follow the material curve (0.07 %). (c) With the strip made of aluminum the neutral axis moves from 24.00 to 28.58 mm (+4.57 mm), and at $M$ = 1500 N·m the bottom stress would be predicted as 108.5 MPa instead of 189.7 MPa: ignoring the strip underestimates the steel's stress by a factor of 1.75. (d) The RMS residual scales with $\kappa$ (A6), so compatibility (Eq. 3) holds through Part C. What failed is Hooke's law: Eqs. 5–6 assume a linear $\sigma$–$\varepsilon$ relation, and Eq. 12 assumes a flat plateau.

## 4. Challenge and Extension solutions

**C1.** Appendix D.6: $Z = bt_f(h - t_f) + t_wh_w^2/4$ = 238.6 × 10³ mm³, $S$ = 209.8 × 10³ mm³, **$k$ = 1.1371** (rectangle 1.5). The experiment ($\kappa$ = 16.0 $\kappa_Y$) gives $M/M_Y$ = 1.1368, essentially fully plastic. $M_Y$ = 52.5 kN·m, $M_p$ = 59.7 kN·m. In an I-section most of the material is already near $\pm\sigma_Y$ at first yield, so there is little left to mobilize; a rectangle's lightly stressed core can still pick up a lot. Design against collapse (plastic design) therefore gains 50 % for a rectangle but only about 14 % for an I-section; the I-section is still far more efficient per unit mass.

**C2.** Part B (elastic): errors $N_s$ = 10: −8.17 × 10⁻³, $N_s$ = 20: −2.05 × 10⁻³, $N_s$ = 40: −5.17 × 10⁻⁴; successive ratios 3.985 and 3.964 (4 for second order). Richardson from 20 and 40: relative error −6.21 × 10⁻⁶. Part C with EPP: $N_s$ = 10: −3.39 × 10⁻³, $N_s$ = 20: −3.36 × 10⁻⁴, $N_s$ = 40: −2.58 × 10⁻⁴, ratios 10.1 and 1.3; the least-squares slope over $N_s$ = 2–256 on the plot is 2.09. The midpoint rule is second order for a smooth integrand; the EPP stress has a kink at $\pm y_Y$, and the error contributed by the strip containing the kink depends on where in that strip the kink falls, so the error oscillates about an $N_s^{-2}$ trend. Triangular load: N = 2: 6.25 × 10⁻², N = 4: 1.56 × 10⁻², N = 8: 3.91 × 10⁻³, N = 16: 9.77 × 10⁻⁴, N = 32: 2.44 × 10⁻⁴ (slope 2.00). Four-point bending: the shear is piecewise constant and the load points are nodes, so the trapezoid rule integrates it exactly at any $N$ (largest error 0.0).

**C3.** (a) Every strain scales by $(1 + \delta)$, so $A_0$ and $A_1$ both scale and $y_{NA} = -A_0/A_1$ is unchanged while $\kappa$ scales. (b) Replacing $y_h$ by $y_h + d$ changes $A_0$ by $-A_1d$ and leaves $A_1$ unchanged. (c) For one gage, $\delta A_1/A_1 = -\delta y_j(y_j - \bar y)/\sum(y_i - \bar y)^2$ to first order; with $\sum(y_i - \bar y)^2$ = 2 288 mm², a 0.1 mm error changes $\kappa$ by at most 0.089 %. At 20 kN it is equivalent to a 10.5 µε strain error at that gage, which is how A2's residuals (1–3 µε) bound the gage-height errors to a few hundredths of a millimeter. None of these explains a discrepancy here; the gage factor (a) is the largest term in A3.

**X1.** Strains $\varepsilon = \varepsilon_0 - \kappa y_h$ in both layers (compatibility, perfect bond); stresses $E(\varepsilon - \alpha\Delta T)$; $N = 0$ and $M = 0$ give two linear equations for $\varepsilon_0$ and $\kappa$. With measured dimensions and $E$: **$\kappa/\Delta T$ = −0.2114 × 10⁻³ m⁻¹/K**, hogging (concave down) because the aluminum on top expands more. At 50 K: $\kappa$ = −0.0106 m⁻¹ (radius 94.6 m); interface stresses steel +50.6 MPa and aluminum −23.8 MPa; steel bottom 36.8 MPa; aluminum top 12.9 MPa. *Check:* equal coefficients give $\kappa = 0$ and no stress. The interface shear needed to transfer these forces is concentrated near the ends, which is where bimetal bonds fail.

**X2.** Unloading from $M_{max}$ leaves $\sigma_{res}(c) = -\sigma_Y + M_{max}c/I = \sigma_Y(M_{max}/M_Y - 1)$ on the compression side (tension), and the opposite on the tension side. On reverse loading by $\Delta M$, the extreme fiber reaches $-\sigma_Y$ again (on the original tension side) when $\sigma_Y(1 - M_{max}/M_Y) - \Delta M c/I = -\sigma_Y$, i.e. after a total change of $2M_Y$ from $M_{max}$: reverse yield at $M = M_{max} - 2M_Y$. Since $M_{max} \le M_p = 1.5M_Y < 2M_Y$, unloading to zero never reverse-yields (the residual is at most 0.5 $\sigma_Y$). Reloading in the original direction is elastic up to $M_{max}$ (shakedown; the same idea as the autofrettage of gun barrels and the presetting of springs).

**X3.** T-section from the I-beam preset (flange 100 × 10 mm, web 6 mm, depth 200 mm, area 2 140 mm²): elastic NA 141.73 mm above the bottom; plastic NA 178.33 mm (equal areas, in the web just below the flange); strip summation at $10^4\kappa_Y$ puts it at 178.33 mm with $M/M_p$ = 1.00000. $Z$ = 112.5 × 10³ mm³, $S$ (to the extreme fiber, at the bottom of the web) = 61.8 × 10³ mm³, **$k$ = 1.819**. The elastic axis balances first moments of area; the plastic axis balances areas. They coincide only for a section symmetric about the neutral axis.

## 5. Design problem D1: reference solution

**D1.** $M_{max} = wL^2/8 + PL/4$ = **7.125 kN·m** at midspan; $\delta_{allow}$ = $L/240$ = 12.5 mm. Steel: $\sigma_Y - U$ = 294.0 MPa, allowable 176.0 MPa, $S_{req}$ = 40.47 × 10³ mm³, $I_{req}$ = 2.332 × 10⁶ mm⁴ ($E$ = 205 GPa). Aluminum: 271.7 MPa, 162.7 MPa, $S_{req}$ = 43.79 × 10³ mm³, $I_{req}$ = 6.991 × 10⁶ mm⁴ ($E$ = 68.39 GPa, measured).

| Section | Mass (kg/m) | $\sigma_{max}$ (MPa) | $\delta$, steel (mm) | Acceptable |
|---|---:|---:|---:|---|
| I-100 | 7.79 | 218.1 | 17.85 | no |
| I-120 | 10.07 | 139.6 | 9.52 | yes |
| I-140 | 12.60 | 94.9 | 5.55 | yes |
| I-160 | 15.26 | 68.3 | 3.49 | yes |
| I-180 | 18.30 | 50.4 | 2.29 | yes |
| I-200 | 21.44 | 38.6 | 1.58 | yes |
| RT-100x50x4 | 8.94 | 247.2 | 20.23 | no |
| RT-120x60x5 | 13.38 | 138.2 | 9.42 | yes |
| RT-150x100x5 | 18.89 | 70.8 | 3.86 | yes |
| RT-200x100x6 | 27.20 | 39.7 | 1.63 | yes |

: Table K3. Steel candidates (stress is the same for both materials).

| Section | Mass (kg/m) | $\sigma_{max}$ (MPa) | $\delta$, aluminum (mm) | Acceptable |
|---|---:|---:|---:|---|
| I-100 | 2.67 | 218.1 | 53.50 | no |
| I-120 | 3.45 | 139.6 | 28.53 | no |
| I-140 | 4.32 | 94.9 | 16.64 | no |
| I-160 | 5.24 | 68.3 | 10.47 | yes |
| I-180 | 6.28 | 50.4 | 6.87 | yes |
| I-200 | 7.36 | 38.6 | 4.73 | yes |
| RT-100x50x4 | 3.07 | 247.2 | 60.63 | no |
| RT-120x60x5 | 4.59 | 138.2 | 28.24 | no |
| RT-150x100x5 | 6.48 | 70.8 | 11.58 | yes |
| RT-200x100x6 | 9.33 | 39.7 | 4.87 | yes |

: Table K4. Aluminum candidates.

**Steel: I-120**, 10.07 kg/m (30.2 kg, about \$66); utilization 0.79 in stress and 0.76 in deflection, so the two requirements are nearly balanced. **Aluminum: I-160**, 5.24 kg/m (15.7 kg, about \$102); utilization 0.42 in stress and 0.84 in deflection: deflection governs, because aluminum's $E$ is a third of steel's while its strength is similar. The aluminum beam is about half the mass at about 1.5 times the cost; either is acceptable if justified. *Assumptions that could invalidate a design:* lateral–torsional buckling of the unbraced compression flange over 3 m (check bracing, or a buckling check that comes later in the course); local buckling of thin flanges (the catalog proportions are compact); load placement other than at midspan; long-term creep is not an issue for these metals at room temperature.

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
3. **No test of where the formulas fail.** *Fix:* Part B tests the transformed section on a real two-material beam, including the equilibrium check $\int\sigma\,dA = 0$ from measured strains (A5). Part C loads past first yield and compares the measured moment–curvature curve with the EPP formula and with the material's own curve, quantifies the 29.8 % overstatement of $Mc/I$, and predicts the permanent curvature (agreement: 0.0827 vs 0.0826 ± 0.0028 m⁻¹).

**Known limitations (not fixed).** The truth model assumes a perfect bond and an elastic steel strip. It ignores the local contact stresses under the rollers, which affect the bottom gage at $x$ = 150 mm (50 mm from a load roller) in a real test; extrusion residual stresses, which make the onset of yield in a real bar less sharp; and the gages' transverse sensitivity (about 1 %). Part C consumes a bar.

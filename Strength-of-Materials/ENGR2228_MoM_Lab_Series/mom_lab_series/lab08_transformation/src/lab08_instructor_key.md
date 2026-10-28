# Lab 8 — Instructor Key: Transformation of Stress and Strain

::: {custom-style="Instructor"}
**For instructors only. Do not distribute to students.** Every number in this key is computed by `src/lab08_analysis.py` (and `src/make_key.py`) from `sample_data.csv` and `src/specimen_measurements.json`, or by the simulation's own model code run in Node. To build a key for your own class data, put your CSV and measurements in the same format and run `python3 src/lab08_analysis.py your.csv your_measurements.json`, then `python3 src/make_key.py`. Uncertainties are expanded ($U = 2u$) unless marked $u$; they come from a Monte Carlo propagation of every input (GUM Supplement 1), so quantities that share inputs keep their correlation. Sign convention as in the handout (Beer 8e): tension positive, $\tau_{xy} > 0$ on the $+x$ face in $+y$, $\theta$ counterclockwise, Mohr's circle "clockwise above"; on the tube $x$ along the tube and $y$ 90° counterclockwise from $x$ seen from outside.
:::

## 1. Results at a glance (sample data)

| Quantity | Measured | Reference or prediction | Verdict (Eq. 13) |
|------------------------------|----------------|------------------------------|--------------------|
| Tube: $D_o$, wall (mm) | 38.130 ± 0.009, 3.205 ± 0.008 | 38.10 × 3.18 nominal | — |
| Rosette H, rosette K bonded at $\beta$ (°) | 1.45 ± 0.20, −1.02 ± 0.23 | 0 intended | — |
| $E$ (GPa), Part A | 68.51 ± 0.68 | Lab 2: 68.46 ± 0.94 | agree |
| $\nu$, Part A | 0.3293 ± 0.0044 | Lab 2: 0.3296 ± 0.0058 | agree |
| $G$ (GPa), Part B − Part A, mean of H and K | 25.67 ± 0.32 | Lab 3: 26.03 ± 0.24; $E/2(1+\nu)$: 25.77 ± 0.26 | agree with Lab 3; agree with $E$, $\nu$ |
| H, Part B: $\sigma_{max}$, $\sigma_{min}$ (MPa) | 60.29 ± 0.95, −7.36 ± 0.43 | Eq. 9: 60.31, −7.42 | both agree |
| H, Part B: $\theta_p$ (°) | −19.53 ± 0.23 | −19.33 | agree |
| K, Part B: $\sigma_{max}$, $\sigma_{min}$ (MPa) | 24.61 ± 0.57, −24.07 ± 0.43 | Eq. 9: 24.55, −24.55 | σ_max agrees; σ_min does not |
| $\sigma_\theta$ per MPa, Part C | 4.489 ± 0.083 | Lamé 4.494; thin wall 4.949 | agree with Lamé; disagree with thin wall |
| $\nu$ from the pressure strains | 0.3349 ± 0.0070 | Lab 2: 0.3296 ± 0.0058 | agree |
| H, Part C with the lever: $\sigma_{max}$, $\sigma_{min}$ (MPa) | 80.69 ± 1.37, 25.71 ± 0.75 | 80.84, 25.98 | both tensile, as predicted |
| H, Part C with the lever: absolute / in-plane $\tau_{max}$ (MPa) | 40.35 ± 0.68 / 27.49 ± 0.50 | absolute predicted 40.42 | agree |
| D1 lightest tube | 44.45 × 4.78 | with the in-plane $\tau_{max}$: 50.8 × 3.18 (unsafe) | — |

: Table K1. Results from the sample data.

The sample data were generated from a known "truth" model (`src/generate_sample_data.py`, values in `src/truth.json`): $E$ = 68.9 GPa, $\nu$ = 0.33; tube 38.13 × 3.205 mm; arms 250.6 and 200.2 mm; the "axis" load point 0.4 mm off the axis; rosette H 1.2° from the top toward K and bonded at +1.5°; rosette K 0.8° above mid-height and bonded at −1.0°; gage factor +0.3 % common and ±0.3 % per grid; $K_t$ = 1.2 % with $\nu_0$ = 0.285; load cell +0.2 %, pressure transducer −0.3 %; 1.5 µε noise and 1 µε resolution; beam theory for bending, torsion and transverse shear and the exact Lamé solution for pressure. The closure tests in `tests/test_lab08_independent.py` confirm that the analysis recovers the truth values within their stated uncertainty.

## 2. Pre-lab solutions

Nominal tube: $r_o$ = 19.05 mm, $r_i$ = 15.875 mm, $I$ = 53 553 mm⁴, $J$ = 107 107 mm⁴, $Q$ = 1 942 mm³; Table 1: $E$ = 68.46 GPa, $\nu$ = 0.3296, $G$ = 25.74 GPa.

**P1.** (a) $M$ = 150 N·m, $T$ = 120 N·m: $\sigma_x$ = 53.36 MPa, $\tau_{xy}$ = −21.34 MPa. $\sigma_{ave}$ = 26.68, $R$ = 34.17 MPa: $\sigma_{max}$ = 60.84 MPa, $\sigma_{min}$ = −7.49 MPa, $\theta_p$ = −19.33° (clockwise from $x$, seen from above), in-plane $\tau_{max}$ = 34.17 MPa. (b) $Tc/J$ = 21.34 and $VQ/(It)$ = 3.43 MPa: $\tau_{xy}$ = −24.77 MPa at K. (c) $\varepsilon_x$ = 779.4, $\varepsilon_y$ = −256.9, $\gamma_{xy}$ = −829.0 µε; readings a, b, c = 779.4, −153.3, −256.9 µε. (d) Eq. 10: $\sigma_\theta$ = 40.00, $\sigma_x$ = 20.00 MPa; Eq. 11: 36.36 and 18.18 MPa. Units: N·m × m/m⁴ = N/m².

**P2.** X is at (σ_x, −τ_xy) = (53.36, 21.34) MPa, above the axis (the negative τ_xy turns the element clockwise); Y at (0, −21.34). The circle crosses the axis at 60.84 and −7.49 MPa. From X, turning **clockwise** by $2\theta_p$ = 38.7° reaches A, so the largest tensile stress acts 19.3° clockwise from the tube axis as seen from above, which is toward the lever side (the local $y$ at H points away from it).

**P3.** Eqs. 6–8 return P1(a) exactly. Bonded at 2°: readings a, b, c = 749.2, −188.4, −226.7 µε. Eq. 6 then gives $\varepsilon_x$ = 749.2 and $\gamma_{xy}$ = −899.3 µε (wrong by −30.2 and −70.3 µε), and $\theta_p$ wrong by 2°; $\varepsilon_{max}$ = 924.8 µε, unchanged.

**P4.** $\sigma_x$ = 71.54, $\sigma_y$ = 36.36, $\tau_{xy}$ = −21.34 MPa: $\sigma_{max}$ = 81.61, $\sigma_{min}$ = 26.30 MPa, both tensile. In-plane $\tau_{max}$ = 27.66 MPa; with $\sigma_3$ = 0, the absolute $\tau_{max}$ = $\sigma_{max}/2$ = 40.80 MPa. Tresca uses the absolute value.

**P5.** Simulation, presets as shipped (page material $E$ = 68.9 GPa, $\nu$ = 0.33): H: $\sigma_{max}$ = 60.84, $\sigma_{min}$ = −7.49 MPa, $\theta_p$ = −19.33°, readings 774.4, −152.6, −255.6 µε. K: 24.77 and −24.77 MPa at −45.0°, readings 0.0, −478.1, 0.0 µε. Part C with the lever at H: in-plane 27.66, absolute 40.80 MPa. "Rosette turned 5°": with $\beta$ = 0, $\sigma_x$ = 48.92 and $\tau_{xy}$ = −25.50 MPa; with $\beta$ = 5°, 53.01 and −21.21 MPa; $\sigma_{max}$ = 60.45 MPa in both.

**P6.** (a) Oil under pressure (bleeding, relief valve, shield, no work on fittings under pressure); the lever and screw loader (hands clear, load by hand); a tube slipping in the clamp. (b) At 600 N with 8 MPa the largest von Mises stress is 72.1 MPa at H on the outer surface and 70.6 MPa at the inner surface: 26 % of $\sigma_Y$, so the tube stays far inside the elastic range (Hooke's law and Eq. 8 require it), with margin for a misplaced load point.

::: {.needspace lines="16"}
:::

## 3. Analysis solutions

| | Gage a | Gage b | Gage c | $\varepsilon_x$ | $\varepsilon_y$ | $\gamma_{xy}$ |
|---|------:|------:|------:|------:|------:|------:|
| Part A, H | 128.57 | 38.83 | −42.26 | 128.57 | −42.26 | −8.65 |
| Part A, K | 1.72 | −9.99 | −0.95 | 1.72 | −0.95 | −20.75 |
| Part B, H | 124.60 | −30.01 | −38.23 | 124.60 | −38.23 | −146.40 |
| Part B, K | 4.20 | −78.26 | −3.32 | 4.20 | −3.32 | −157.39 |
| Part C, H | 11.15 | 33.75 | 54.88 | 11.15 | 54.88 | 1.46 |
| Part C, K | 10.60 | 32.54 | 54.83 | 10.60 | 54.83 | −0.35 |

: Table K2. Slopes of the readings ($K_t$-corrected) and of the reduced components, µε per 100 N (Parts A, B) or per MPa (Part C), before turning back.

**A1.** Table K2. At H in Part A, $\gamma''/(\varepsilon_x'' - \varepsilon_y'')$ = −0.0506, so **$\beta_H$ = 1.45 ± 0.20°**. Turned back, $\varepsilon_x$ = 1.2868 µε/N; with $\sigma_x$ = $FL_bc/I$ = 88.153 kPa per newton, **$E$ = 68.51 ± 0.68 GPa** and **$\nu$ = 0.3293 ± 0.0044**. Lab 2: $E$ 68.46 ± 0.94, $|\Delta|$ = 0.05 ≤ 1.16, agree; $\nu$ 0.3296 ± 0.0058, agree. *Check:* $\sigma/\varepsilon$ has units of stress; with $\beta$ = 0 the apparent shear $-(\varepsilon_x - \varepsilon_y)\sin 2\beta$ vanishes. *Interpret:* turning the rosette slides its three points around the same circle (Figure 2b), so the principal strains do not change. In Part A the turn changes $\varepsilon_x$ and $\varepsilon_y$ only to second order ($\cos 2\beta$ = 0.99872), so $E$ and $\nu$ would hardly change; the turn spoils the shear strain, which is first order in $\beta$: −52 µε of apparent shear at 600 N. The $K_t$ correction matters more for $\nu$: without it $\nu$ = 0.3185 (−3.3 %), while $E$ moves only 0.05 % (C3).

**A2.** Torsion only (Part B − Part A): at K, $(\varepsilon_x'' - \varepsilon_y'')/\gamma''$ gives **$\beta_K$ = −1.02 ± 0.23°**. Turned back: **$G$ = 25.55 ± 0.39 GPa at H and 25.79 ± 0.41 GPa at K**, mean 25.67 ± 0.32 GPa. From A1, $E/2(1+\nu)$ = 25.77 ± 0.26 GPa (agree); Lab 3: 26.03 ± 0.24 GPa, $|\Delta|$ = 0.36 against a limit of 0.40 (agree). *Check:* the torsion-only state at H, turned back by $\beta_H$ from Part A (an independent angle), has $\varepsilon_x - \varepsilon_y$ = −1.02 µε per 100 N against $\gamma_{xy}$ = −138.0 µε, a residual turn of 0.21°, within the uncertainty of $\beta_H$: pure shear, as it must be. *Interpret:* bending and transverse shear depend only on $F$ and the section, which are the same in Parts A and B; only the torque changes, so the difference isolates it. A torsion test of a thin solid bar (Lab 3) and a tube in combined loading give the same $G$ within about 1.4 %.

| Point | $\sigma_x$ (MPa) | $\tau_{xy}$ (MPa) | $\sigma_{max}$ (MPa) | $\sigma_{min}$ (MPa) | $\theta_p$ (°) | Eq. 9: $\sigma_{max}$, $\sigma_{min}$ | Eq. 9: $\theta_p$ |
|------|------:|------:|------:|------:|------:|------:|------:|
| H | 52.73 | −21.31 | 60.29 ± 0.95 | −7.36 ± 0.43 | −19.53 ± 0.23 | 60.31, −7.42 | −19.33 |
| K | 0.57 | −24.34 | 24.61 ± 0.57 | −24.07 ± 0.43 | −44.65 ± 0.14 | 24.55, −24.55 | −45.00 |

: Table K3. Part B at 600 N, stresses from the turned-back strains with Lab 2's $E$ and $\nu$.

**A3.** Table K3. At H: **$\sigma_{max}$ = 60.29 ± 0.95 MPa**, $\sigma_{min}$ = −7.36 ± 0.43 MPa, $\theta_p$ = −19.53 ± 0.23°, against 60.31, −7.42 MPa and −19.33°: both agree (differences 0.03, 0.06 MPa within 1.03, 0.43). At K: 24.61 ± 0.57 and −24.07 ± 0.43 MPa at −44.65 ± 0.14°, against ±24.55 MPa at −45°. $\sigma_{max}$ agrees; $\sigma_{min}$ differs by 0.48 MPa against a limit of 0.46: rosette K sits slightly above mid-height (M1(e)), where the bending stress adds 0.57 MPa to $\sigma_x$ and raises both principal stresses by half of that. With K at the measured height, the prediction becomes 24.83 and −24.27 MPa, and both agree. *Check:* $\sigma_{max} + \sigma_{min}$ = 52.92 MPa = $\sigma_x + \sigma_y$ at H. *Interpret:* at H the bending tension dominates and the largest tension runs 19.5° from the tube axis; at K there is no bending, the state is nearly pure shear, and the largest tension runs at 45°: the helix along which a brittle tube would crack in torsion.

**A4.** Pressure slopes (turned back), per MPa: H: $\varepsilon_x$ = 11.14, $\varepsilon_y$ = 54.89 µε; K: 10.61, 54.83 µε. (a) **$\nu$ = 0.3349 ± 0.0070** (mean of H and K), against Lab 2 0.3296 ± 0.0058: agree. (b) **$\sigma_\theta$ = 4.489 ± 0.083 MPa per MPa** and $\sigma_x$ = 2.224 ± 0.059: Lamé (Eq. 11) gives 4.494 and 2.247 (agree); the thin-wall Eq. 10 gives 4.949 and 2.474 (disagree, 10.1 % high). *Check:* $\sigma_x/\sigma_\theta$ = 0.495. *Interpret:* the gages agree with Lamé. Equation 10 is the average hoop stress through the wall, which is exact, but the hoop stress falls from the inner to the outer surface (Figure 4), and the gages see only the outer value.

**A5.** With 8 MPa and 600 N on the lever: at H, **$\sigma_{max}$ = 80.69 ± 1.37 and $\sigma_{min}$ = 25.71 ± 0.75 MPa, both tensile** (predicted 80.84 and 25.98). In-plane $\tau_{max}$ = 27.49 ± 0.50 MPa; **absolute $\tau_{max}$ = 40.35 ± 0.68 MPa** = $\sigma_{max}/2$, predicted 40.42 (agree), 1.47 times the in-plane value. At K: 52.67 ± 0.99 and 1.42 ± 0.46 MPa; $\sigma_{min}$ is only just tensile, so the absolute 26.34 ± 0.49 MPa barely exceeds the in-plane 25.63 ± 0.51 MPa. *Check:* the absolute value is never less than the in-plane one. *Interpret:* Tresca must use the absolute value: at H, the in-plane value understates the largest shear by 32 %. At the inner surface $\sigma_r = -p$ is the smallest principal stress, which makes the largest circle bigger still (D1).

**A6.** Use Table K1. Expected verdicts: $E$, $\nu$ and $G$ agree with Labs 2 and 3; the principal stresses at H and K agree with Eq. 9 once the rosettes' turns are corrected (and K's height is accounted for); the pressure stresses agree with Lamé, not with the thin-wall formula; the absolute $\tau_{max}$ under pressure agrees with Eq. 4 and is about 1.5 times the in-plane value. Full credit needs Table 5 complete, a normalized figure with error bars, and each discrepancy explained with a named, quantified cause.

**M1.** (a) Eq. 10 is 10.1 % high at the gages: the ratio is $(r_o + r_i)/(2r_i)$ = 1.101; 5 % needs $r_o/r_i$ = 1.10, i.e. $r_i/t_w$ ≈ 10. (b) With the lever load at H the in-plane value is 32 % low; with pressure alone ($\sigma_\theta$ = 2$\sigma_x$, both tensile) the absolute $\tau_{max}$ = $\sigma_\theta/2$ is twice the in-plane $(\sigma_\theta - \sigma_x)/2$, so the in-plane value is 50 % low (Beer Eqs. 7.33, 7.34). (c) Ignoring the turns at H in Part B: $\tau_{xy}$ = −22.61 MPa instead of −21.31 (6.1 % high) and $\theta_p$ = −20.98° instead of −19.53 ± 0.23°; $\sigma_{max}$ unchanged. (d) Ignoring $K_t$: $E$ changes 0.05 %, $\nu$ −3.3 %, the Part C hoop strain 0.6 % and the Part C axial strain 6.3 %; the gage most affected is the one across the larger strain (gage c in Part A, gage a in Part C). (e) Part A, K: the turned-back $\varepsilon_x$ at K is 0.0105 of that at H, so **K is 0.60 ± 0.19° above mid-height** (truth 0.8°). *Rank:* thin wall (10 %) and in-plane vs absolute shear (32 % low here, 50 % under pressure alone) are model errors that change a design decision; the rosette turn (6 % on $\tau$) and $K_t$ (3 % on $\nu$, 6 % on the Part C axial strain) are measurement errors that a careful experimenter corrects; K's height matters only for $\sigma_{min}$ at K.

## 4. Challenge and Extension solutions

**C1.** A delta rosette at K aligned with $x$ would read 8.4, −409.6, 409.1 µε in Part B at 600 N. With 1.5 µε on each reading, $u(\gamma_{xy})$ = $1.5\sqrt{6}$ = 3.67 µε for the rectangular rosette (Eq. 6) and $1.5 \times 2\sqrt{2}/\sqrt{3}$ = 2.45 µε for the delta rosette; $u(\varepsilon_x)$ is 1.5 µε for both. The delta rosette is better conditioned for shear (its three directions are spread evenly), which is what K measures.

**C2.** From Part B alone: $\sigma_x$ at H gives $FL_b$ = 149.5 ± 2.4 N·m (150 by the load cell and rule), $\tau$ at H gives $Fa_L$ = 120.9 ± 2.4 N·m (120). The shear force comes from the difference of the shear stresses at K and H, $VQ/(It)$: **$F$ = 535 ± 59 N**, against 600 N, and then $a_L$ = 226 ± 28 mm and $L_b$ = 280 ± 31 mm. The moments are good to 1.6 %, but $F$ is the small difference of two large stresses (about 24 and 21 MPa), so 0.3 MPa of error in either is 10 % in $F$; the truth model's 1.2° offset of H adds a 2 % bias. A strain-gage load cell should measure bending at two sections instead.

**C3.** Appendix D.4. A gage reads $(\varepsilon_\parallel + K_t\varepsilon_\perp)/(1 - \nu_0K_t)$; this equals $\varepsilon_\parallel$ when $\varepsilon_\perp = -\nu_0\varepsilon_\parallel$, the strain field of the gage-factor calibration. In Part A, gage a sees $\varepsilon_\perp/\varepsilon_\parallel = -\nu$ = −0.33, close to −0.285, so its error is tiny; gage c sees $\varepsilon_\perp/\varepsilon_\parallel = -1/\nu \approx -3$, far from −0.285, so its error is 3.3 % of its reading (which is why $\nu$ moves). In Part C gage a lies across the hoop strain, 4.6 times its own, and errs by 6.3 %.

**X1.** Appendix D.6. The integral $\int_{r_i}^{r_o}(A + B/r^2)\,dr = A t_w + B(1/r_i - 1/r_o) = A t_w + A r_o t_w/r_i = p r_i$, so the average is $pr_i/t_w$.

**X2.** Hooke's law gives $\sigma_x - \sigma_y = 2G(\varepsilon_x - \varepsilon_y)$ and $\tau_{xy} = 2G(\gamma_{xy}/2)$, so Eq. 3 for stress and Eq. 7 for strain give the same $2\theta_p$, and $R_\sigma = 2G\,R_\varepsilon$. For Part B at H: $R_\sigma$ = 33.82 MPa, $2G R_\varepsilon$ = 33.82 MPa.

**X3.** Two gages at ±45° to the axis on the top and two on the bottom (or on opposite sides), wired as a full bridge with the +45° gages in opposite arms: torsion strains the +45° gages in tension and the −45° gages in compression, and the bridge adds them. Bending gives equal strains at ±45° (Eq. 5 with $\gamma$ = 0 and $\varepsilon(45°) = \varepsilon(-45°)$), so it cancels within each pair; top and bottom cancel the bending sign too. Pressure gives equal ±45° strains (cancels), transverse shear is zero at top and bottom, and temperature strains all four gages equally (cancels in a full bridge).

## 5. Design problem D1: reference solution

**D1.** Tresca allowable shear $\sigma_Y/(2 \times 1.8)$ = 76.0 MPa; twist limit 3.0°/m with $G$ = 26.03 GPa. For each tube: Lamé stresses at $r_o$ and $r_i$ ($A = pr_i^2/(r_o^2 - r_i^2)$, $\sigma_\theta = A + Ar_o^2/r^2$, $\sigma_r = A - Ar_o^2/r^2$, $\sigma_x = A \pm Mr/I$), $\tau = Tr/J$, principal stresses with $\sigma_r$ as the third, on the tension and compression sides.

::: {.needspace lines="22"}
:::

| Tube | Mass (kg/m) | Tresca factor (absolute $\tau_{max}$) | With in-plane $\tau_{max}$ | Von Mises factor | Twist (°/m) | Critical point | OK? |
|------------------|-------:|-------:|-------:|-------:|-------:|----------------------|-----|
| 38.1 × 2.11 | 0.644 | 0.99 | 1.02 | 1.14 | 8.52 | inner, tension side | no |
| 44.45 × 2.11 | 0.758 | 1.04 | 1.20 | 1.19 | 5.24 | inner, tension side | no |
| 31.75 × 3.18 | 0.771 | 1.07 | 1.07 | 1.23 | 11.20 | outer, compression side | no |
| 50.8 × 2.11 | 0.871 | 1.01 | 1.29 | 1.15 | 3.45 | inner, tension side | no |
| 38.1 × 3.18 | 0.942 | 1.45 | 1.47 | 1.68 | 6.16 | inner, tension side | no |
| 31.75 × 4.78 | 1.094 | 1.43 | 1.43 | 1.62 | 8.69 | outer, compression side | no |
| 44.45 × 3.18 | 1.113 | 1.54 | 1.77 | 1.75 | 3.74 | inner, tension side | no |
| 50.8 × 3.18 | 1.284 | 1.50 | 1.91 | 1.70 | 2.44 | inner, tension side | no |
| 38.1 × 4.78 | 1.351 | 2.05 | 2.05 | 2.37 | 4.66 | outer, compression side | no |
| 44.45 × 4.78 | 1.608 | 2.23 | 2.59 | 2.55 | 2.78 | inner, tension side | yes |
| 50.8 × 4.78 | 1.866 | 2.18 | 2.79 | 2.47 | 1.79 | inner, tension side | yes |

: Table K4. D1 candidates (factors are $\sigma_Y/(2\tau)$ or $\sigma_Y/\sigma_{vM}$; required 1.8).

**Reference design: 44.45 × 4.78**, 1.608 kg/m. Critical point: inner surface, tension side. There $\sigma_x$ = 76.1, $\sigma_\theta$ = 84.2, $\sigma_r$ = −20.0 and $\tau$ = 22.0 MPa; principal stresses 102.5, 57.8, −20.0 MPa; absolute $\tau_{max}$ = 61.3 MPa (Tresca factor 2.23), while the in-plane circle has radius only 22.4 MPa. Von Mises factor 2.55. Twist 2.78°/m. The lighter **38.1 × 4.78** passes the stress requirement (factor 2.05) but twists 4.66°/m: the twist limit governs it out. A student who uses the in-plane $\tau_{max}$ picks **50.8 × 3.18** (1.284 kg/m, in-plane factor 1.91), whose true Tresca factor is 1.50: unsafe, because pressure makes both in-plane principal stresses tensile at the inner surface and $\sigma_r = -p$ is the third principal stress. Von Mises gives the same choice as Tresca here. *Assumptions that could invalidate a design:* the closed-end axial stress (an open-ended swivel with a sliding seal carries no $pA$ end force); pressure surges above 20 MPa (relief valve setting); stress concentrations at ports and fittings; fatigue under cyclic pressure and torque, which governs most real hydraulic parts.

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
4. Using $\sigma = E\varepsilon$ component by component instead of Eq. 8: at H it invents a hoop stress of −17.2 MPa where there is none, and in Part C it understates the hoop stress by about 100 %.
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

1. **A rosette lab easily becomes a calculator exercise:** three readings in, Eq. 6 and Mohr's circle, a match, done. *Fix:* the lab measures its own imperfections. Part A's uniaxial state reveals how rosette H was bonded (1.45 ± 0.20°), the torsion-only difference reveals rosette K's (−1.02 ± 0.23°), and Part A's bending leak locates K on the circumference; A1–A3 then show that the corrections move $\tau_{xy}$ by 6.1 % and $\theta_p$ by 1.45 ± 0.20° while leaving the principal values alone, which is the content of Eq. 1.
2. **Only the in-plane maximum shear was ever computed,** so §7.4 stayed abstract. *Fix:* Part C pressurizes the same tube, making both in-plane principal stresses tensile at H; the measured absolute $\tau_{max}$ is 1.47 times the in-plane value, and D1 turns that into a design trap (the in-plane value picks a tube that is unsafe by Tresca).
3. **The thin-wall formula was taken on faith.** *Fix:* the gages on the outer surface resolve the 10 % difference between Eq. 10 and Lamé (A4), the key explains why Eq. 10 is nevertheless exact on average, and Poisson's ratio is measured from the pressure strains independently of $E$.

**Known limitations (not fixed).** The transverse shear uses $VQ/(It)$ averaged through the wall; for $t_w/r_o$ = 0.17 the exact elasticity distribution differs by a few percent at the surface, and the truth model uses the beam formula too. The clamp is assumed rigid and far enough away (Saint-Venant); end-plug restraint near the clamp is not modeled. Temperature changes during the pressure test (the oil warms slightly when pumped) are ignored; self-temperature-compensated gages make this small. The truth model has no residual stresses from tube manufacture, which would not affect the increments measured here.

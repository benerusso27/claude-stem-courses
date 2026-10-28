# Lab 5 — Instructor Key: Transverse Shear

::: {custom-style="Instructor"}
**For instructors only. Do not distribute to students.** Every number in this key is computed by `src/lab05_analysis.py` (and `src/make_key.py`) from `sample_data.csv` and `src/specimen_measurements.json`, or by the simulation's own model code run in Node. To build a key for your own class data, put your CSV and measurements in the same format and run `python3 src/lab05_analysis.py your.csv your_measurements.json`, then `python3 src/make_key.py`. Uncertainties are expanded ($U = 2u$) unless marked $u$. Sign convention as in the handout (Beer 8e): $V$ and $M$ as in Fig. 5.6; $\tau_{xy} < 0$ for $V > 0$, reported as the magnitude $\tau = VQ/(It)$; deflection $y$ up, $\delta = -y$ reported.
:::

## 1. Results at a glance (sample data)

| Quantity | Measured | Reference or prediction | Verdict (Eq. 16) |
|---|---|---|---|
| Bar A: $b$, $h$ (mm) | 25.420 ± 0.026, 50.780 ± 0.026 | 25.4 × 50.8 nominal | — |
| $R$ at the faces, upright ($b/h$ = 0.5006) | 1.042 ± 0.018 | Eq. 7: 1.0414 ± 0.0006 | agree |
| $R$ at the faces, flat ($b/h$ = 1.9976) | 1.515 ± 0.029 | Eq. 7: 1.4909 ± 0.0067 | agree |
| I-beam web $\tau/V$ at the NA (10⁻³ mm⁻²) | see Table K2 | $Q/(It_w)$ | agree at all three heights |
| $E$ from the span series (GPa) | 68.66 ± 0.60 | Lab 2: 68.46 ± 0.94 | agree |
| $G$ from the span series (GPa) | 25.84 ± 0.27 | Lab 3: 26.03 ± 0.24 | agree |
| Span with a 5 % shear part (mm; $L/H$) | 1 768 (17.4) | Eq. 9: 1 759 (17.3) | agree |
| $EI_{eff}$ loose / bolted / bonded (N·m²) | 1 190 ± 11 / 2 530 ± 23 / 4 761 ± 42 | Eq. 11: 1 188 / — / 4 751 | loose and bonded agree |
| Bolt slip modulus $k_b$ (kN/mm) | 40.16 ± 0.83 (discrete); 37.94 (smeared) | — | — |
| Bolted end slip (10⁻⁹ m/N) | 67.212 ± 0.890 | model with fitted $k_b$: 66.956 | agree (0.38 %) |
| D1 fewest bolts | stepped: 26; uniform: 34 | — | — |

: Table K1. Results from the sample data.

The sample data were generated from a known "truth" model (`src/generate_sample_data.py`, values in `src/truth.json`). Part A: the Saint-Venant flexure solution for each orientation ($\nu$ = 0.330), a 0.3 mm load eccentricity (twist, opposite on the two faces), gages slightly off the neutral axis. Part B: $VQ/(It)$ in the web with ±1.5 % plate bending between the two sides; Timoshenko deflection with the energy shear factor. Part C: six discrete bolts of 40 kN/mm, an epoxy layer of finite stiffness, plus the shear deflection. Instrument errors: +0.4 % common gage-factor error, +0.3 % LVDT gain, reading noise. Because the gages read high and Lab 3's $G$ is 0.5 % above the truth, every measured shearing stress is about 0.9 % high, inside its uncertainty. The closure test in `tests/test_lab05_independent.py` confirms that the analysis recovers the truth values within their stated uncertainty.

## 2. Pre-lab solutions

**P1.** (a) $V$ = 7.5 kN, $A$ = 1 290.3 mm², $\tau = 3V/2A$ = 8.719 MPa, $\gamma = \tau/G$ = 335 µε, so $\varepsilon(+45°) - \varepsilon(-45°)$ = −335 µε (negative in the left half, P4). Largest bending stress under the load: $M = PL/4$ = 1 500 N·m, $S$ = 10 925 mm³, $\sigma$ = 137.3 MPa, top in compression and bottom in tension. (b) $A_w$ = 423.2 mm²; $V$ = 10 kN gives $\tau \approx$ 23.63 MPa and a pair difference of about 908 µε. (c) Nominal I-beam: $I$ = 2.4769 × 10⁶ mm⁴, $A$ = 1 390.9 mm², $f_s \approx A/A_w$ = 3.287. At 10 kN on 300 mm: bending 0.0332 mm, shear 0.0681 mm (shear 67 % of the total); on 1200 mm: 2.1230 mm and 0.2724 mm (11 %). Shear dominates the short span; bending dominates the long one. (d) $EI_0$ = 1.2 N·m²; at 2 kN, loose 7.58 mm, bonded 1.895 mm (one quarter), loose end slip $rPL^2/(16EI_0)$ = 0.481 mm. Units: N·mm³/(N/mm² × mm⁴) = mm.

**P2.** $I$ = 2.4769 × 10⁶ mm⁴. (a) $Q_{NA}$ = 27 747 mm³, $\tau$ = 23.53 MPa. (b) Web just below the flange: $Q = Bt_f(H - t_f)/2$ = 23 044 mm³, $\tau$ = 19.55 MPa. (c) Flange just above: same $Q$, width $B$: 1.221 MPa. The shear flow $q = VQ/I$ is the same on both sides of the junction (Eq. 1); dividing by widths in the ratio 16.01 gives the jump. Eq. 4: 23.63 MPa, close to (a).

**P3.** For two equal layers, $Q = bt^2/2$ and $I = 2bt^3/3$, so $q = 3V/(4t)$ = 73.8 N/mm at $V$ = 1.25 kN. At 100 mm spacing each bolt carries 7.38 kN, an average shank stress of 261 MPa (high-strength shoulder bolts are needed). The loose interface carries no shear (apart from friction): each bar bends about its own axis, so $EI = 2 \times bt^3/12$ instead of $b(2t)^3/12$, a factor of 4.

**P4.** (a) Appendix D.2 of the handout: $\varepsilon(\pm45°) = \frac{1}{2}(\varepsilon_x + \varepsilon_y) \pm \frac{1}{2}\gamma$, with $\varepsilon_y = -\nu\varepsilon_x$, so the axial part is $\varepsilon_x(1 - \nu)/2$ on both gages. (b) In the left half, $V = +P/2$ (Beer), so $\tau_{xy} < 0$, $\gamma_{xy} < 0$ and the difference is negative; the sample data confirm it. (c) A slightly eccentric load twists the bar; torsion adds shear of opposite sign on opposite faces, which the average cancels (A1 reports the difference).

**P5.** Simulation, presets as shipped ($\nu$ = 0.33): upright $R$ = 1.0413, flat $R$ = 1.4918 (center of the flat bar 0.8215). I-beam: shear part 64.7 % at 300 mm and 10.3 % at 1200 mm; 5 % at 1 769 mm; $f_s$ = 2.9007. Part C at 2.5 kN with six bolts: δ = 4.434 mm (discrete springs), end slip 0.1675 mm; loose 9.415 mm and 0.598 mm; glue 2.357 mm.

**P6.** (a) Pinch points at rollers, load nose and yoke; specimens rolling or shifting sideways (flat bar, stacked bars); overload of the specimens, bolts or fixture (overload stops per test); handling the 5 kg I-beam. (b) The limits keep the bending stress below about half of $\sigma_Y$ in every test and the bolt forces below their rating. The flat bar's section modulus is half the upright one ($bh^2/6$ with $b$ and $h$ swapped), so the same bending stress is reached at half the load.

## 3. Analysis solutions

**A1.** Upright ($V$ to 7.500 kN): **$R$ = 1.042 ± 0.018** vs Eq. 7 1.0414 ± 0.0006: $|\Delta|$ = 0.0010 ≤ 0.0181, agree. At the largest load, $\tau$ = 9.16 MPa vs $VQ/(Ib)$ = 8.72 MPa ($\gamma$ = 352 µε). Flat ($V$ to 3.752 kN): **$R$ = 1.515 ± 0.029** vs 1.4909 ± 0.0067: $|\Delta|$ = 0.0237 ≤ 0.0294, agree; $\tau$ = 6.57 vs 4.36 MPa. The two faces differ by ±3.1 % (upright) and ±2.2 % (flat) about their mean: the twist from a slightly eccentric load, cancelled by averaging. *Check:* upright $b/h$ = 0.5 gives $R$ close to 1, as Eq. 7 requires as $b/h \to 0$. *Interpret:* for the flat bar, $VQ/(Ib)$ underestimates the largest shearing stress by 34.0 % (the elasticity value is 49.1 % above it). The section, $V$ and the average stress are the same in both orientations; only the shape of the stress distribution across the width changes, through Poisson's ratio.

| Height above mid-depth (mm) | $Q$ (mm³) | Measured $\tau/V$ (10⁻³ mm⁻²) | $Q/(It_w)$ (10⁻³ mm⁻²) | Difference (%) | Eq. 16 | Sides differ by (%) |
|---:|---:|---:|---:|---:|---|---:|
| 0.18 | 27 796 | 2.3574 ± 0.0398 | 2.3347 ± 0.0073 | 0.97 | agree | 1.5 |
| 22.37 | 26 595 | 2.2491 ± 0.0363 | 2.2338 ± 0.0070 | 0.68 | agree | 1.8 |
| 41.13 | 23 736 | 2.0123 ± 0.0325 | 1.9937 ± 0.0062 | 0.93 | agree | 1.4 |

: Table K2. Web shearing stress per newton of shear (I-beam: $I$ = 2.4802 × 10⁶ mm⁴, $t_w$ = 4.8003 ± 0.0049 mm).

**A2.** Table K2. Measured section: $H$ = 101.600 ± 0.033, $B$ = 76.207 ± 0.029, $t_f$ = 6.352 ± 0.025, $t_w$ = 4.8003 ± 0.0049 mm; $u_I$ = 0.15 %. All three heights agree with $Q/(It_w)$; the common +1.0 % is the gage-factor and $G$ bias above. $1/A_w$ = 2.3434 × 10⁻³ mm⁻², within −0.37 % of the neutral-axis value. *Check:* $q$ at the junction is $VQ/I$ = 93.0 N/mm at $V$ = 10 kN on both sides; in the flange that is an average vertical stress of only 1.220 MPa over the full width $B$. *Interpret:* the web carries 94.0 % of $V$ (integral of $\tau t$ over the web), so it is nearly uniformly stressed: $V/A_w$ is a good design value, and the flanges carry the bending.

| Span (mm) | $L/H$ | Measured $\delta/P$ (µm/N) | Eq. 9 (µm/N) | Shear part, measured (%) | Shear part, Eq. 9 (%) |
|---:|---:|---:|---:|---:|---:|
| 300 | 2.95 | 0.00932 | 0.00931 | 64.8 | 64.4 |
| 450 | 4.43 | 0.02025 | 0.02017 | 44.7 | 44.6 |
| 600 | 5.91 | 0.03846 | 0.03849 | 31.4 | 31.1 |
| 900 | 8.86 | 0.10735 | 0.10743 | 16.9 | 16.7 |
| 1 200 | 11.81 | 0.23551 | 0.23600 | 10.3 | 10.2 |

: Table K3. Compliance and shear part of the deflection (Eq. 9 with Table 1 values and $f_s$ = 2.9015).

**A3.** Fit of $\delta/(PL)$ against $L^2$: slope 0.1223 × 10⁻¹² N⁻¹mm⁻² (±0.07 %, $u$), intercept 20.126 × 10⁻⁹ N⁻¹ (±0.32 %). With $I$ = 2.4802 × 10⁶ mm⁴ and $f_s$ = 2.9015 (energy integral for the measured section; $A/A_w$ = 3.2689): **$E$ = 68.66 ± 0.60 GPa** vs Lab 2: $|\Delta|$ = 0.20 ≤ 1.12, agree. **$G$ = 25.84 ± 0.27 GPa** vs Lab 3: $|\Delta|$ = 0.19 ≤ 0.36, agree. Both are about 0.3 % low because of the LVDT gain error, which scales slope and intercept equally. *Check:* slope units 1/(N·mm²) → $1/(48EI)$; intercept units 1/N → $f_s/(4GA)$. *Interpret:* the short spans fix the intercept (shear is 65 % of $\delta$ at 300 mm); the long spans alone have almost no shear and give $G$ with a large uncertainty. Using $f_s = A/A_w$ would have given $G$ = 29.11 GPa (12.7 % high): the choice of $f_s$ matters as much as the measurement.

**A4.** Table K3. The 5 % span is **1 768 mm** from the fit ($L/H$ = 17.4) and 1 759 mm from Eq. 9 ($L/H$ = 17.3). On the 300 mm span, shear is 65 % of the deflection: Euler–Bernoulli would underestimate it by a factor of 2.84. *Check:* the shear fraction falls by about $(L_1/L_2)^2$ between spans at long spans. *Interpret:* the I-section puts its material in the flanges, which raises $I$ but leaves a thin web to carry $V$, so $EI/(GA_w)$ is large; a solid rectangle of the same depth reaches 5 % at about $L/H$ = 7.7.

**A5.** After removing the shear term (about 0.56 % of the bonded compliance): loose **1 190 ± 11** N·m² vs $EI_0$ = 1 188 (0.18 %); bolted **2 530 ± 23** ($EI/EI_0$ = 2.126, $\eta$ = 0.377); bonded **4 761 ± 42** vs $EI_{full}$ = 4 751 (0.21 %, $\eta$ = 1.003). Bonded/loose = 4.001. Loose end slip 239.535 ± 0.675 × 10⁻⁹ m/N vs $rL^2/(16EI_0)$ = 240.58: agree. *Check:* $b(2t)^3/12 \div (2 \times bt^3/12) = 4$. *Interpret:* bonding moves the material of each bar away from its own neutral axis to a distance $t/2$ from the common one; the parallel-axis terms triple the stiffness of the separate bars.

**A6.** Fitting the bolted deflection with the discrete-spring model gives **$k_b$ = 40.16 ± 0.83 kN/mm**; the smeared closed form needs 37.94 kN/mm (−5.5 %), because spreading six bolts uniformly misplaces their stiffness. **Predicted end slip 66.956 × 10⁻⁹ m/N vs measured 67.212 ± 0.890** (0.38 %): the model, fitted to deflection only, predicts the slip, which validates it. At 2.5 kN the bolt forces from the springs are 6.05, 5.08, 2.44 kN (outer to inner, each half); Eq. 5 with a rigid connection ($q$ = 73.8 N/mm) gives 7.38 kN for every bolt in the shear span, 22 % above the largest spring value. Largest shank stress 214 MPa. Glue: $\tau = VQ/(Ib)$ = 2.32 MPa at 4.0 kN. *Check:* the predicted slip lies between 0 and the loose value. *Interpret:* the bolts slip, so the layers carry part of the moment separately and the interface force is lower than for a rigid bond; the force is largest at the outer bolt, where the slip is largest, and smallest near midspan, where the slip vanishes by symmetry.

**A7.** Use Table K1. Expected verdicts: every row agrees. Full credit needs Table 5 complete, a normalized figure with error bars, and each discrepancy above $U$ explained with a named, quantified cause.

**M1.** (a) Flat bar ($b/h$ = 2, $\nu$ = 0.33): the face stress is 49.2 % above $VQ/(Ib)$, matching A1. (b) 300 mm span: $\delta/\delta_{bending}$ = 2.83: Euler–Bernoulli underestimates the deflection by that factor. (c) Part C at 2.5 kN: largest bolt force 6.04 kN (springs) vs 7.38 kN (Eq. 5). "Few bolts" ($s$ = 300 mm, 2 bolts): deflection smeared 6.159 mm vs discrete 6.322 mm (2.6 %), but the end slip differs by 17 %, and Eq. 5 gives 22.1 kN per bolt against 8.62 kN from the springs. Smearing is acceptable when the spacing is well below $1/\alpha$ (118 mm for the lab's six bolts; 204 mm with 300 mm spacing). (d) With $G_g$ = 50 MPa and a 1 mm layer, $\eta$ = 0.792. For a 0.15 mm layer, $\eta$ falls below 0.95 only when $G_g$ < 39.2 MPa; a structural epoxy (about 1 GPa) gives $\eta$ = 0.9982, so the lab's bonded pair is effectively rigid.

## 4. Challenge and Extension solutions

**C1.** Appendix D.4: $f_s$ = 6/5. For the measured I-beam, $f_s$ = 2.9015 (flanges and web; the simulation agrees), while $A/A_w$ = 3.2689. Using $A/A_w$ in A3 raises $G$ by 12.7 %. The energy factor is the consistent choice with Eq. 9; the difference shows that "shear area" approximations are good to only about 10 % for I-sections.

**C2.** Flat bar: N = 8: 1.40098, N = 16: 1.46641, N = 32: 1.48533, N = 64: 1.49015. Successive differences shrink by 3.46 and 3.93 (4 for second order). Richardson from 32 and 64: 1.49176 vs series 1.4918. With $\nu = 0$ the right-hand side of the stress-function equation vanishes, $\phi = 0$, and $VQ/(Ib)$ is exact.

**C3.** Slender cantilever (1 m): 4 elements: full 11.6 %, reduced 98.44 %; 16 elements: full 67.8 %, reduced 99.90 %; 64 elements: full 97.1 %, reduced 99.99 % (percent of the closed-form deflection). With full integration the element enforces $w' = \theta$ at two points, which a linear $w$ and linear $\theta$ can satisfy only with no bending: the element "locks". Reduced integration enforces it on average, and the error is $O(N^{-2})$. Locking worsens as $L/h$ grows because the shear stiffness $GA/L$ dominates the bending stiffness $EI/L^3$ by $(L/h)^2$.

**X1.** Appendix D.5. Loose: $k \to 0$ gives $N = 0$, $\delta = PL^3/(48EI_0)$, and $s_0 = r\int_0^{L/2}\kappa\,dx = r\theta_{end}$. Rigid: $k \to \infty$ gives $\delta = PL^3/(48EI_{full})$ and $s_0 \to 0$.

**X2.** In a flange the horizontal shear flow at distance $s$ from the tip is $q = Vt_fs\,d/I$ with $d = (H - t_f)/2$, linear in $s$. At the web face each half delivers 43.6 N/mm for $V$ = 10 kN; the part of the flange directly above the web adds 5.9 N/mm; the total, 93.0 N/mm, equals $VQ/I$ in the web at the junction (A2).

**X3.** From the simulation, $\eta$ = 0.95 needs $G_g$ ≈ 39.2 MPa for a 0.15 mm layer. Hot-cured epoxies drop by an order of magnitude in modulus above their glass transition and creep under sustained load, so a bonded beam under a permanent load in a hot environment slowly loses composite action (more deflection, and stress moves from the bond into the layers).

## 5. Design problem D1: reference solution

**D1.** $V_{max} = wL/2$ = 9.6 kN, $M_{max} = wL^2/8$ = 5.76 kN·m ($\sigma$ = 34.6 MPa, $\tau$ at the interface 1.44 MPa: both far below the limits). At the support $q = 3V/(4t)$ = 144 N/mm, so the spacing there must not exceed 69.4 mm. With $k_b$(M10) = 66.9 kN/mm (from the A6 fit), $\delta_{full}$ = 6.06 mm, $\delta_{loose}$ = 24.23 mm, limit $L/300$ = 8.0 mm.

| Pattern | Bolts | Largest $F$, Eq. 5 (kN) | Largest $F$, springs (kN) | δ (mm) |
|---|---:|---:|---:|---:|
| Uniform, $s$ = 70 mm | 34 | 9.79 | 8.27 | 7.34 |
| Stepped, $s_1$ = 70 mm over 800 mm at each end, $s_2$ = 210 mm | 26 | 9.95 | 8.30 | 7.43 |

: Table K4. Reference designs (search in 5 mm steps; the stepped pattern is the fewest-bolt solution found).

The bolt-force requirement governs both patterns: the shear flow falls linearly toward midspan, so wider spacing in the middle saves 8 bolts. Both patterns meet the deflection limit with some margin. The spring model's largest force is about 15 % below Eq. 5, so Eq. 5 is conservative here. *Assumptions that could invalidate a design:* the linear scaling of $k_b$ with bolt diameter (check with a single-bolt push-out test); hole clearance, which adds slip before the bolts bear (use fitted bolts or check the slip at service load); bearing stress on the aluminum around the holes; fatigue of the bolts under repeated walkway loads.

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

1. **τ = VQ/It was to be "verified" on a narrow section with a handbook G,** where it is right by construction. *Fix:* the same bar is tested upright and flat, with $G$ carried over from Lab 3, so the measurement shows where the formula fails (A1: 34.0 % under-estimate at $b/h$ = 2). The elasticity correction is computed two independent ways in the simulation, and the I-beam web profile tests $Q/(It)$ at three heights.
2. **The planned loose/bolted/bonded stack was a qualitative demonstration,** and Eq. 5 assumes a rigid connection that bolts do not provide. *Fix:* a partial-interaction model (closed form, finite differences, discrete springs) with the bolt stiffness fitted to the deflection and then checked against the independently measured end slip (A6: 0.38 %). Eq. 5 is compared with the spring forces, and D1 uses the measured $k_b$.
3. **Shear deformation was to be shown in the simulation only,** and a real short-span test mixes it with fixture compliance. *Fix:* a yoke referenced to the supports and five spans; Eq. 10 separates bending and shear, giving $E$ and $G$ from one beam for comparison with Labs 2 and 3 (A3).

**Known limitations (not fixed).** The truth model uses Timoshenko beam theory with the energy shear factor; at $L/H$ ≈ 3 the real elastic field near the load differs by a few percent, which the sample data do not contain. The bolts are modeled as linear springs with no hole clearance or friction. The glue is linear elastic. The web gage pairs are assumed to sit exactly at mid-thickness of the web plate; real pairs on a 4.8 mm web pick up some web bending, which averaging the two sides removes.

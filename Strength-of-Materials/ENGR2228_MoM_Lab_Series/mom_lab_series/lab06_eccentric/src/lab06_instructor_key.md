# Lab 6 — Instructor Key: Eccentric Axial Loading

::: {custom-style="Instructor"}
**For instructors only. Do not distribute to students.** Every number in this key is computed by `src/lab06_analysis.py` (and `src/make_key.py`) from `sample_data.csv` and `src/specimen_measurements.json`, or by the simulation's own model code run in Node. To build a key for your own class data, put your CSV and measurements in the same format and run `python3 src/lab06_analysis.py your.csv your_measurements.json`, then `python3 src/make_key.py`. Uncertainties are expanded ($U = 2u$) unless marked $u$. Sign convention as in the handout (Beer 8e): $y$ up, $z$ to the left in section views, tension positive, Eq. 4.58 in principal axes with $M_y = Pz_P$, $M_z = -Py_P$; beam-column deflection measured toward the load line.
:::

## 1. Results at a glance (sample data)

| Quantity | Measured | Reference or prediction | Verdict (Eq. 15) |
|------------------------------|----------------|------------------------------|--------------------|
| Bar: $h$, $b$ (mm) | 50.830 ± 0.026, 12.6810 ± 0.0049 | 50.8 × 12.7 nominal | — |
| $e_{eff}$ at 30 kN, hole $h/3$ (mm) | 16.465 ± 0.109 | hole 16.950 ± 0.058 (Eq. 1); $eC_{mid}$ 16.380 ± 0.056 (Eq. 9) | disagree with Eq. 1; agree with Eq. 9 |
| $e_{eff}$ at 30 kN, hole $h/6$ (mm) | 8.168 ± 0.054 | hole 8.490 ± 0.058; $eC_{mid}$ 8.205 ± 0.056 | disagree with Eq. 1; agree with Eq. 9 |
| $E\varepsilon_0$ at 30 kN, hole $h/3$ (MPa) | 46.25 ± 0.84 | $P/A$ = 46.63 ± 0.27 | agree |
| Out-of-plane bending, $e$ = 0 run | 4.43 % ($e_z$ = 0.094 mm) | — | — |
| Angle: G1, G2, G3, G4 at 30 kN | Table K4 | Eq. 8 | 1 of 4 agree with Eq. 8 alone; 4 of 4 with fillet and Eq. 9 |
| Part C at 25 kN: $C_{mid}$ | 0.6687 ± 0.0078 | Eq. 9: 0.6680 ± 0.0040 | agree |
| Part C at 25 kN: $C_{end}$ (40 mm from the block) | 0.7692 ± 0.0144 | Eq. 9: 0.7728 ± 0.0031 | agree |
| Part C at 25 kN: $w_{mid}$ (mm) | 2.110 ± 0.012 | Eq. 9: 2.125 ± 0.032 | agree |
| $EI$ through the thickness from $w_{mid}$ (N·m²) | 596.7 ± 9.3 | $E\,hb^3/12$: 591.3 ± 8.1 | agree |
| D1 lightest angle | L76 × 51 × 6.4, long leg connected | $P/A$ alone would pick L38 × 38 × 4.8 | — |

: Table K1. Results from the sample data.

The sample data were generated from a known "truth" model (`src/generate_sample_data.py`, values in `src/truth.json`): Eq. 4.58 in principal axes with every principal eccentricity reduced by the beam-column factor of Eq. 9 (rigid end blocks, $E$ = 68.9 GPa), a root fillet of 4.8 mm on the angle, hole positions within ±0.05 mm of the reported values, an out-of-plane misalignment of 0.15 mm in the Part A runs, a common +0.3 % and a random ±0.3 % gage-factor error, 1.5 µε noise, +0.2 % load-cell and +0.3 % LVDT gain errors. The closure test in `tests/test_lab06_independent.py` confirms that the analysis recovers the truth values within their stated uncertainty. Because Eqs. 11 and 12 are ratios, the common gage-factor, load and $E$ errors cancel in $e_{eff}$ and $C$.

## 2. Pre-lab solutions

**P1.** (a) $A$ = 645.16 mm², $P/A$ = 46.50 MPa; with $e = h/3$, $6e/h = 2$: $\sigma_{max}$ = 139.5 MPa at $y = +h/2$, $\sigma_{min}$ = −46.5 MPa at $y = -h/2$. Neutral axis $y_0 = -(h^2/12)/(h/3) = -h/4$ = −12.7 mm. At $y$ = +20 mm, $\sigma$ = 119.7 MPa (≈ 1 749 µε); at −20 mm, −26.7 MPa (≈ −390 µε). (b) $P/A$ = 38.75 MPa and $6e/b = 3$: front 155.0 MPa (2 264 µε), back −77.5 MPa (−1 132 µε). (c) $I_z$ = 138 744 mm⁴, $I_y$ = 8 671.5 mm⁴; $P_{cr}$ = 1 500 kN across the width and 93.7 kN through the thickness. $P/P_{cr}$ = 0.020 (Part A, 30 kN) and 0.267 (Part C, 25 kN): Eq. 10 says Part A is safe (about 2.5 %), Part C is not (about 33 % by the small-load estimate; Eq. 9 gives more, see M1). Units: N·mm²/mm² = N.

**P2.** At the edge $y = -h/2$, Eq. 2 gives $\sigma = (P/A)(1 - 6e/h)$, which is zero when $e = h/6$. Hole $e$ = 0: inside the kern, uniform stress. $h/6$: on its boundary, the neutral axis touches the far edge (stress zero there, $2P/A$ at the near edge). $h/3$: outside, the neutral axis is inside the bar at $-h/4$, with compression beyond it.

**P3.** Two rectangles (vertical leg $50.8 \times 6.35$, horizontal leg $44.45 \times 6.35$): $A$ = 604.8 mm², centroid 15.03 mm from both outer faces, $I_y = I_z$ = 144 678 mm⁴, $I_{yz}$ = 84 981 mm⁴ (positive for the "L" of Figure 1: both legs' centroids lie in quadrants where $y$ and $z$ have the same sign). $I_u = I + |I_{yz}|$ = 229 659 mm⁴, $I_v = I - |I_{yz}|$ = 59 698 mm⁴, $\theta_p$ = −45° (the major axis runs through the heel and the centroid). Load point from the centroid: $y_P$ = −19.79, $z_P$ = −13.55 mm, so $u_P$ = 4.41 and $v_P$ = −23.57 mm. At 30 kN, $P/A$ = 49.60 MPa, and:

| Gage | $y$, $z$ from C (mm) | $u$, $v$ (mm) | Eq. 8 (MPa) | $I_{yz}$ ignored (MPa) |
|------|----------------|----------------|----------:|----------:|
| G1 | 28.97, 15.03 | −9.86, 31.11 | −68.1 | −111.5 |
| G2 | −3.03, 15.03 | 12.77, 8.49 | 51.8 | 19.8 |
| G3 | −15.03, 3.03 | 12.77, −8.49 | 104.0 | 102.8 |
| G4 | −15.03, −28.97 | −9.86, −31.11 | 123.6 | 192.7 |

: Table K2. Pre-lab P3 (nominal angle).

Ignoring $I_{yz}$ moves the neutral axis and gets G2 and G4 badly wrong (and overstates G1's compression); G3 is nearly right by coincidence, because it sits close to where the two stress planes cross.

**P4.** Eq. 2: $E\varepsilon = (P/A)(1 + ey/r_z^2)$ is linear in $y$ with intercept $P/(EA)$ and slope $Pe/(EAr_z^2)$; their ratio times $r_z^2$ is $e$, and $E$, a common gage-factor error and the load scale both terms equally (Appendix D.5). A front-minus-back difference that is the same at all heights is bending through the thickness, an out-of-plane offset of the load line. A difference that varies with $y$ would mean twisting of the bar (or a gage-position error), which the out-of-plane offset alone cannot produce.

**P5.** Simulation, presets as shipped ($E$ = 68.9 GPa in the page): Part A, $h/3$: $\sigma_{max}$ = 139.6 MPa, $\sigma_{min}$ = −46.59 MPa, neutral axis at −12.69 mm. Part B: G1–G4 = −68.1, 51.8, 104.0, 123.6 MPa from Eq. 8; the largest stress is 127.7 MPa with principal axes and 211.8 MPa with $I_{yz}$ ignored. Part C at 25 kN: $C_{mid}$ = 0.6709, $C_{end}$ = 0.9024, $w_{mid}$ = 2.106 mm; Eq. 4 is 5 % off at 2.71 kN (the buckling load with the end blocks is 66.0 kN).

**P6.** (a) Pins walking out of the clevises (retaining clips, full insertion); pinch points at the grips and blocks (hands clear, jog with both hands); overload (overload stop); reaching past a loaded specimen to adjust the LVDT (set at zero load). (b) In tension Eq. 4 overstates the bending (Section 2.4), so a limit set with it is conservative. In compression the same offsets amplify the bending; the Part C bar would reach yield well below 25 kN, and the out-of-plane configuration would buckle at about 66.0 kN.

## 3. Analysis solutions

| Hole | $e_{eff}$ (mm) | Hole offset (mm) | Eq. 1 | $eC_{mid}$, Eq. 9 (mm) | Eq. 9 | $E\varepsilon_0$ (MPa) | $y_0$ (mm) | Bending out of plane (%) |
|------|----------------:|-------------:|----------|----------------:|----------|-------------:|----------:|--------:|
| 0 | 0.044 ± 0.042 | 0.04 ± 0.06 | agree | 0.039 ± 0.056 | agree | 46.36 ± 0.84 | far outside | 4.43 |
| h/6 | 8.168 ± 0.054 | 8.49 ± 0.06 | disagree | 8.205 ± 0.056 | agree | 46.28 ± 0.83 | −26.36 | 4.54 |
| h/3 | 16.465 ± 0.109 | 16.95 ± 0.06 | disagree | 16.380 ± 0.056 | agree | 46.25 ± 0.84 | −13.08 | 4.41 |

: Table K3. Part A at 30 kN ($P/A$ = 46.63 ± 0.27 MPa).

**A1.** Table K3. $E\varepsilon_0$ agrees with $P/A$ in every run (the centric part is unaffected by the offset). For $h/3$: **$e_{eff}$ = 16.465 ± 0.109 mm** vs the hole 16.950 ± 0.058 mm: $|\Delta|$ = 0.485 > 0.123, disagree; vs $eC_{mid}$ = 16.380 ± 0.056 mm: $|\Delta|$ = 0.085 ≤ 0.123, agree. For $h/6$: 8.168 ± 0.054 vs hole 8.490 ± 0.058 (disagree) and vs 8.205 ± 0.056 (agree). At 30 kN Eq. 9 gives $C_{mid}$ = 0.9664 (in-plane, $P_{cr}$ = 1 050 kN with the blocks): the bar has straightened enough to cut the in-plane bending by 3.4 %, and the ratio method resolves it. In stress terms, Eq. 2 predicts 139.9 and −46.7 MPa at the edges; the fit gives 136.1 and −43.6 MPa. *Check:* for $e$ = 0, $e_{eff}$ = 0.044 ± 0.042 mm, consistent with the hole offset 0.040 ± 0.058 mm; $e_{eff} = r_z^2\beta/\varepsilon_0$ has units mm² × (1/mm) = mm. *Interpret:* the comparison tests the assumption that the deformation leaves the eccentricity unchanged. For this stocky bar the effect is a few percent, small but measurable, and it makes Eq. 1 slightly conservative.

**A2.** Table K3. With the hole offset (Eq. 3): $y_0$ = −12.70 mm ($h/3$) and −25.36 mm ($h/6$, at the edge −25.42 mm); with $eC_{mid}$: −13.14 and −26.24 mm. Measured: −13.08 and −26.36 mm. *Check:* $y_0\,e_{eff}$ = −215.3 mm² ($h/3$) and −215.3 mm² ($h/6$), both equal to $-r_z^2$ = −215.3 mm² as Eq. 3 requires. *Interpret:* for $h/6$ the measured neutral axis lies just **outside** the bar, because the straightening reduced the effective eccentricity below $h/6$: the load is effectively inside the kern and the whole section stays in tension. Unreinforced masonry has almost no tensile strength, so a compressive load must stay within the middle third of a rectangular pier (the kern) or the pier cracks on the far side.

**A3.** Out-of-plane bending at 30 kN: 4.43 % ($e$ = 0), 4.54 % ($h/6$), 4.41 % ($h/3$), corresponding to $e_z$ = 0.094, 0.096, 0.093 mm. *Check:* in the $e$ = 0 run the half-difference is the same at the five heights within 4 µε, as an offset through the thickness predicts. In the $h/3$ run the raw half-differences spread over 11 µε, because each back gage sits up to 0.2 mm from its front partner and the steep in-plane gradient leaks in; correcting each pair by $\beta(y_F - y_B)/2$ brings the spread down to 4 µε and the percent bending from 4.56 % to 4.41 %. *Interpret:* using the front gages alone in the $e$ = 0 run would overstate the strain by the bending fraction, about 4.43 %, and $E$ would come out low by the same amount; the back gages alone would err the other way. Standards for tension testing limit the percent bending because it biases modulus and yield measurements in exactly this way.

| Gage | Measured (MPa) | Eq. 8 (MPa) | Difference | Limit (Eq. 15) | Verdict | $I_{yz}$ ignored | + fillet | + fillet and Eq. 9 |
|-----|--------------:|--------------:|-------:|-------:|----------|-------:|-------:|---------:|
| G1 | −62.3 ± 1.7 | −67.9 ± 0.9 | 5.6 | 1.9 | disagree | −111.6 | −67.9 | −63.1 |
| G2 | 48.0 ± 1.0 | 51.7 ± 0.9 | −3.7 | 1.4 | disagree | 19.8 | 50.3 | 48.3 |
| G3 | 97.8 ± 1.9 | 104.1 ± 0.4 | −6.3 | 2.0 | disagree | 103.0 | 102.7 | 99.3 |
| G4 | 123.6 ± 2.4 | 124.2 ± 0.4 | −0.6 | 2.4 | agree | 193.5 | 124.2 | 123.7 |

: Table K4. Part B at 30 kN. Measured section: legs 50.85 ± 0.03 and 50.76 ± 0.03 mm, $t$ = 6.331 ± 0.004 mm.

**A4.** Measured section (legs as rectangles): $A$ = 603.2 mm², centroid at $y$ = 15.05, $z$ = −15.00 mm from the heel; $I_z$ = 144 690, $I_y$ = 144 042, $I_{yz}$ = 84 809 mm⁴; $\theta_p$ = −44.89°, $I_u$ = 229 175, $I_v$ = 59 557 mm⁴. Load point: $y_P$ = −19.81, $z_P$ = −13.58 mm; $u_P$ = 4.36, $v_P$ = −23.62 mm. Table K4: Eq. 8 reproduces the pattern (signs and magnitudes, G1 in compression at −1.25 $P/A$), but only 1 of the 4 gages agree within Eq. 15: the residuals are 5.6, −3.7, −6.3, −0.6 MPa. Ignoring $I_{yz}$ is off by up to 64 % of the true value. The plane through the four measured stresses has its neutral axis at 167.1° from $z$, against 170.5° from Eq. 8. *Check:* $I_u + I_v$ = 288 732 mm⁴ = $I_y + I_z$ = 288 732 mm⁴; $I_y \approx I_z$ (equal legs, measured legs differ by 0.1 mm). *Interpret:* the load acts far below the horizontal leg and well to one side, so the minor-axis couple bends the vertical leg's tip back toward compression: a tension member with compression in its outstanding leg. A thin outstanding leg in compression can buckle locally, and a brittle material could crack there. The residuals are explained in C3.

**A5.** Use Table K1. Expected verdicts: $E\varepsilon_0$ with $P/A$, $e_{eff}$ with $eC_{mid}$ (not with the hole offset), the Part C values with Eq. 9, and the angle with Eq. 8 only after the fillet and Eq. 9 are included. Full credit needs Table 5 complete, a normalized figure with error bars, and each discrepancy above $U$ explained with a named, quantified cause (the straightening, the fillet, misalignment).

| $P$ (kN) | $C_{mid}$ measured | Eq. 9 | $C_{end}$ measured | Eq. 9 | $w_{mid}$ measured (mm) | Eq. 9 (mm) |
|-------:|----------:|--------:|----------:|--------:|----------:|---------:|
| 5.01 | 0.9074 | 0.9141 | 0.9522 | 0.9422 | 0.541 | 0.550 |
| 10.02 | 0.8400 | 0.8399 | 0.8926 | 0.8918 | 1.018 | 1.025 |
| 15.03 | 0.7756 | 0.7751 | 0.8428 | 0.8474 | 1.427 | 1.439 |
| 20.05 | 0.7179 | 0.7182 | 0.8063 | 0.8080 | 1.794 | 1.803 |
| 25.05 | 0.6687 | 0.6680 | 0.7692 | 0.7728 | 2.110 | 2.125 |

: Table K5. Part C: bending-moment factors from Eq. 12 and the LVDT deflection against Eq. 9 ($e$ = 6.40 mm, $EI$ from Table 1 and the measured $b$).

**M1.** (a) Table K5. At 25 kN: **$C_{mid}$ = 0.6687 ± 0.0078** vs Eq. 9 0.6680 ± 0.0040 ($|\Delta|$ = 0.0007 ≤ 0.0087, agree); $C_{end}$ = 0.7692 ± 0.0144 vs 0.7728 ± 0.0031 (agree); $w_{mid}$ = 2.110 ± 0.012 mm vs 2.125 ± 0.032 mm (agree). Eq. 4 assumes $C = 1$: it overstates the mid-length bending moment by 49.5 % (Eq. 9: 49.7 %), and the largest stress at mid-length (front face) by 34 %: 156.5 MPa by Eq. 4 against 116.7 MPa measured. Near the block the measured front-face stress is 129.5 MPa, still 21 % below Eq. 4. The axial strain gives $E\varepsilon_0$ = 38.57 MPa vs $P/A$ = 38.86 MPa: the centric part is unaffected. (b) Eq. 4 is 5 % off at **2.68 kN** through the thickness ($P/P_{cr}$ = 0.0411) and at **43.1 kN** across the width ($P/P_{cr}$ = 0.0411): the same fraction of each buckling load, as Eq. 10 predicts. Part A at 30 kN is inside the 5 % band; Part C is far outside it from about 3 kN on. (c) In compression $C$ grows: 1.744 at 25 kN and 2.89 at 40 kN for the Part C configuration, without bound at $P_{cr}$ = 66.0 kN; Eq. 4 is already 5 % low at 2.62 kN. The deformation adds to the eccentricity, so Eq. 4 underestimates the stress: unconservative. *Interpret:* Eq. 4 may be used when $|P|$ is below about 4 % of the buckling load of the member in the plane of the offset; above that, use Eq. 9 (or the secant formula in compression, §10.2). In tension Eq. 4 errs on the safe side; in compression it does not.

## 4. Challenge and Extension solutions

**C1.** Slope of $e_{eff}$ against $P$: $h/6$, −8.32 ± 1.29 µm/N against −9.45 µm/N from Eq. 9; $h/3$, −20.41 ± 1.86 against −18.86 µm/N. They are resolved at 13 and 22 standard uncertainties, both consistent with Eq. 9, and the measured drop over the test is 3.0 % and 3.6 %. Extrapolated to $P = 0$: 8.432 ± 0.025 and 17.073 ± 0.036 mm, against holes 8.490 ± 0.058 and 16.950 ± 0.058 mm. The trend is the straightening of Section 2.4, seen in a member where it is only a few percent.

**C2.** Least-squares fit of $w_{mid}(P)$ with $EI$ as the only unknown: **$EI$ = 596.7 ± 9.3 N·m²** (statistical scatter, hole offset, LVDT gain and end-block length combined) vs $E\,hb^3/12$ = 591.3 ± 8.1 N·m²: $|\Delta|$ = 5.4 ≤ 12.3, agree (0.92 %). The uncertainty of the offset $e$ (±0.05 mm on 6.4 mm) and of the block length $a$ dominate; $EI$ from the LVDT is an independent check of $E$ through a stiffness, not a strain.

**C3.** For the measured angle, Eq. 9 gives $C_{mid}$ = 0.899 for the minor-axis component of the offset and 0.972 for the major-axis component at 30 kN. Including the 4.8 mm fillet changes the predictions by 0.0, −1.4, −1.4, 0.0 MPa (area +0.82 %); adding the straightening changes them by a further 4.8, −2.0, −3.4, −0.6 MPa. Against the residuals 5.6, −3.7, −6.3, −0.6 MPa of A4, the straightening explains most of the misfit and the fillet a little; with both, 4 of the 4 gages agree (Table K4, last column). Remaining differences come from the truth model's slightly different load point and dimensions, within the stated uncertainties.

**X1.** Appendix D.4. With $a$ = 0 the compression solution gives $M_{max} = Pe\sec(kL/2)$ and $y_{max} = e[\sec(kL/2) - 1]$, Beer's secant formula (§10.2). With blocks, $P_{cr}$ is the root of $\cos u = ka\sin u$; for $a/L$ = 0.1 it is 0.70 of $\pi^2EI/L^2$ (the blocks lengthen the effective member). The small-load expansion is in Appendix D.4.

**X2.** At the section: $M$ = −150.0 N·m (Beer sign; tension on top), $T$ = 120.0 N·m, $V$ = 600 N. $I$ = 53 553 mm⁴, $J$ = 107 107 mm⁴. Top (H): $\sigma_x$ = 53.36 MPa, $\tau = Tc/J$ = 21.34 MPa. Side where they add (K): $\sigma_x$ = 0, $\tau$ = 21.34 + 3.43 = 24.77 MPa; on the opposite side 17.92 MPa. To measure the torque alone, put a ±45° pair at the top or bottom, where $VQ/(It)$ = 0 and the bending strain cancels in $\varepsilon(+45°) - \varepsilon(-45°)$; or average the two sides. These are the Lab 8 predictions.

**X3.** The kern of the nominal angle has 5 vertices (one per edge of the convex outline) and an area of 191.4 mm² (simulation: 191.4 mm²). The Part B load point is 23.98 mm from the centroid; along that direction the kern ends 8.31 mm from it. No position of a gusset on one leg can bring the load inside the kern; connecting both legs, or using a pair of angles back to back, is the way to load an angle concentrically.

## 5. Design problem D1: reference solution

**D1.** $\sigma_{allow}$ = 0.6 × 273.7 = 164.2 MPa. Load point: in the gusset mid-plane, 4.765 mm below the connected leg, on its bolt line at $g$ from the heel. Table K6 evaluates Eq. 8 at every corner of the convex outline (the largest stress is always at a corner) for each candidate, with $T$ = 40 kN, and adds the beam-column values (Eq. 9, $L$ = 1.50 m, $a$ = 75 mm).

| Angle | $A$ (mm²) | Mass (kg/m) | $P/A$ (MPa) | Largest $\sigma$, Eq. 8 (MPa) | Smallest $\sigma$ (MPa) | Eq. 9, ends (MPa) | Eq. 9, mid (MPa) | OK? |
|--------------------------------------------|-------:|-------:|-------:|---------:|---------:|--------:|--------:|-----|
| L38 × 38 × 4.8 | 340 | 0.92 | 117.6 | 316.4 | −249.4 | 292.7 | 170.9 | no |
| L51 × 51 × 4.8 | 461 | 1.24 | 86.8 | 226.3 | −149.2 | 216.6 | 163.2 | no |
| L51 × 51 × 6.4 | 605 | 1.63 | 66.1 | 170.5 | −124.7 | 165.2 | 133.8 | no |
| L64 × 64 × 6.4 | 766 | 2.07 | 52.2 | 131.8 | −84.4 | 129.7 | 117.5 | yes |
| L76 × 51 × 6.4, long leg connected | 766 | 2.07 | 52.2 | 118.3 | −106.2 | 118.2 | 113.8 | yes |
| L76 × 51 × 6.4, short leg connected | 766 | 2.07 | 52.2 | 180.1 | −72.0 | 170.9 | 130.7 | no |
| L76 × 76 × 6.4 | 927 | 2.50 | 43.1 | 124.3 | −57.5 | 122.2 | 111.3 | yes |
| L76 × 76 × 9.5 | 1 362 | 3.68 | 29.4 | 82.9 | −46.2 | 82.1 | 78.0 | yes |

: Table K6. D1 candidates (6061-T6, root fillets ignored; Eq. 9 columns at the ends of the free length and at mid-length).

**Reference design: L76 × 51 × 6.4, long leg connected**, 2.07 kg/m, largest stress 118.3 MPa = 0.72 $\sigma_{allow}$ (simulation preset "D1": 118.3 MPa). The equal-leg L64 × 64 × 6.4 has the same mass and also passes (131.8 MPa), so either earns full credit if justified; the unequal angle is better because the connected long leg puts the gage line close to the centroid's projection. Connecting the **short** leg of the same angle fails (180.1 MPa): the choice of leg is part of the design. $P/A \le \sigma_{allow}$ alone would choose L38 × 38 × 4.8 ($P/A$ = 117.6 MPa), whose true largest stress is 316 MPa, 1.93 times the allowable. The L51 × 51 × 6.4 fails narrowly (170.5 MPa with Eq. 8; 165.2 MPa even with Eq. 9 at the ends). The straightening helps little where it matters: the governing stress is at the ends of the free length, where Eq. 9 gives 118.2 MPa for the chosen angle (mid-length 113.8 MPa), so relying on it would not change the choice. The compression side reaches −106.2 MPa in the outstanding leg, far below local-buckling concern for $b/t$ = 8. *Assumptions that could invalidate a design:* the rigid-block model of the gusset (a flexible gusset rotates and changes the end moments; check with a strain-gaged prototype); stress concentration and shear lag at the bolts (the net-section check required by design codes); load reversal under wind, which would make this slender brace buckle (Lab 9).

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

1. **Eccentric tension of a stocky bar only confirms Eq. 4.50 to a few percent,** a verification with nothing at stake. *Fix:* Part C puts the same bar's offset through its thickness, where the deformation changes the eccentricity enough to make Eq. 4 49.5 % high at mid-length; it is measured two independent ways (strain ratio and LVDT) against Eq. 9, and M1 turns it into a rule ($|P| \lesssim 0.04\,P_{cr}$) that also warns about compression (Lab 9). The ratio estimator of Eq. 11, in which $E$ and gage-factor errors cancel, is precise enough to detect the 3.4 % straightening even in Part A.
2. **Only doubly symmetric sections,** so principal axes and $I_{yz}$ were never tested. *Fix:* Part B is a real one-leg-connected angle, the way bracing is built. Eq. 8 in principal axes predicts a compressive gage in a tension member, and ignoring $I_{yz}$ errs by up to 64 %. D1 turns the same physics into a member choice where $P/A$ alone picks an angle that is 1.93 times overstressed.
3. **Fixture misalignment would contaminate the measured eccentricity unnoticed.** *Fix:* gages at five heights on both faces separate in-plane bending from out-of-plane misalignment (A3), the $e$ = 0 run measures the fixture's own bending, and every estimator is a ratio of front/back averages.

**Known limitations (not fixed).** The end blocks are modeled as rigid and the clevises as frictionless pins; real spherical seats have friction, which adds a small end moment. The angle is treated as bending about two principal axes with no coupling to twist (its shear center is at the heel); in tension this coupling is stabilizing and small. Shear lag and the stress concentration at the bolt holes are outside the model (the gages are far from the connections). The truth model has no initial crookedness of the bar, which in a real Part C test would add to or subtract from the offset.

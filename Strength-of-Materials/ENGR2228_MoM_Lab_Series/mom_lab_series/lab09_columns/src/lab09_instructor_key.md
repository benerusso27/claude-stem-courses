# Lab 9 — Instructor Key: Columns

::: {custom-style="Instructor"}
**For instructors only. Do not distribute to students.** Every number in this key is computed by `src/lab09_analysis.py` (and `src/make_key.py`) from `sample_data.csv` and `src/specimen_measurements.json`, or by the simulation's own model code run in Node. To build a key for your own class data, put your CSV and measurements in the same format and run `python3 src/lab09_analysis.py your.csv your_measurements.json`, then `python3 src/make_key.py`. Uncertainties are expanded ($U = 2u$) unless marked $u$; the clamp stiffness and the prediction that uses it come from a Monte Carlo propagation (GUM Supplement 1) in which the load-cell calibration is common to both clamped tests. Sign convention as in the handout (Beer 8e §10.1–10.2): $P$ compressive and positive, $x$ down the column from end A, $y$ lateral, $M = -P(y + e)$; the column bows away from the load line; tension positive; front face convex.
:::

## 1. Results at a glance (sample data)

| Quantity | Measured | Reference or prediction | Verdict (Eq. 11) |
|------------------------------|----------------|------------------------------|--------------------|
| Bar: $b$, $t$ (mm) | 25.420 ± 0.011, 6.350 ± 0.011 | 25.40 × 6.35 nominal | — |
| $P_{cr}$, pinned 300 mm (N) | 4 103 ± 24 | Euler 4 072 ± 62 | agree |
| $P_{cr}$, pinned 450 mm (N) | 1 829 ± 11 | Euler 1 810 ± 27 | agree |
| $P_{cr}$, pinned 600 mm (N) | 1 026 ± 6 | Euler 1 016 ± 15 | agree |
| Slope of $\log P_{cr}$ against $\log L$ | −1.997 ± 0.005 | −2 | agree |
| $E$ from the Southwell loads (GPa) | 69.10 ± 0.54 | Lab 2: 68.46 ± 0.94 | agree |
| $E$ from the axial strain (GPa) | 69.34 ± 0.80 | Lab 2: 68.46 ± 0.94 | agree |
| $P_{cr}$, fixed–fixed 600 mm (N); $K$ | 3 730 ± 22; 0.5220 ± 0.0041 | Euler, $K$ = 0.5: 4 065 ± 60 | disagree (8 % low) |
| Clamp stiffness $k$ (N·m/rad) | 2 800 ± 500 | — | — |
| $P_{cr}$, fixed–pinned 640 mm (N); $K$ | 1 765 ± 10; 0.7120 ± 0.0056 | $K$ = 0.699: 1 830 ± 27; Eq. 4 with $k$: 1 758 ± 15 | disagree with 0.699; agree with Eq. 4 |
| Groove offsets from Part C (mm) | 1.009 ± 0.017, 1.979 ± 0.033 | 1.00, 2.00 (±0.02) | agree, agree |
| Part D maximum load (kN) | 31.03 ± 0.18 | Euler 45.24; tangent modulus 35.61 | Euler 46 % high; tangent 14.8 % high |
| D1 lightest tube | 63.50 × 1.65 | with $K$ = 0.52 from Part B: 44.45 × 1.65 (buckles at 8.59 kN) | — |

: Table K1. Results from the sample data.

The sample data were generated from a known "truth" model (`src/generate_sample_data.py`, values in `src/truth.json`): $E$ = 68.9 GPa; bar 25.42 × 6.350 mm; half-sine bows of 0.28, 0.43, 0.66 mm (300, 450, 600 mm) plus a small third harmonic; the knife edges put the load line 0.08 mm off the axis; clamps of 2 450, 2 580 N·m/rad (bottom, top); groove offsets 1.01, 1.98 mm; load cell 0.3 % high, UTM −0.2 %; dial noise 0.003 mm and 0.01 mm resolution; gage-factor errors +0.4 % (front) and −0.2 % (back) and 1.5 µε noise. The response is a Hermite finite-element model with the stress-free bow, the end offsets and the clamp springs; Part D is the fiber model with Lab 1's Ramberg–Osgood curve ($\sigma_{0.2}$ = 274 MPa, $m$ = 17), maximum 31.09 kN. The closure tests in `tests/test_lab09_independent.py` confirm that the analysis recovers every truth value within its stated uncertainty.

## 2. Pre-lab solutions

Nominal section: $A$ = 161.29 mm², $I$ = 542.0 mm⁴, $r$ = 1.833 mm; with Table 1's $E$, $EI$ = 37.10 N·m².

**P1.** (a) $L/r$ = 163.7, 245.5, 327.3; $P_{cr}$ = 4 069, 1 808, 1 017 N; $\sigma_{cr}$ = 25.23, 11.21, 6.31 MPa, far below $\sigma_Y$. (b) Fixed–fixed 600 mm ($L_e$ = 300 mm): 4 069 N; fixed–pinned 640 mm ($L_e$ = 0.699 × 640 mm): 1 829 N. (c) 90 mm: $L/r$ = 49.1, Euler gives 45.2 kN, $\sigma_{cr}$ = 280 MPa, above $\sigma_Y$; $\sigma_YA$ = 44.1 kN. Euler's formula stops applying below $L/r = \pi\sqrt{E/\sigma_Y}$ = 49.7, so the bar reaches the yield region first (and, as Part D shows, fails well below both). (d) $\delta$ = 0.50, 1.50 and 4.50 mm. Units: GPa × mm⁴/mm² = (10³ N/mm²)(mm²) = kN, so keep $E$ in N/mm² (MPa) to get newtons.

**P2.** Both have $L_e$ = 300 mm, so the same ideal $P_{cr}$ (4 069 N). The clamped bar buckles lower, because no real clamp is rigid: Part B measures 3 730 ± 22 N against 4 103 ± 24 N for the 300 mm pinned bar.

**P3.** $\delta/P$ = 0.556, 0.833, 1.667, 3.333 mm/kN. The line has slope 555.6 × 10⁻⁶ N⁻¹ and intercept 0.278 × 10⁻⁶ m/N: $P_{cr}$ = 1 800 N and $\delta_0$ = 0.50 mm. The 900 N reading is the least reliable: its deflection is small, so the dial's ±0.01 mm and the seating of the knife edges matter most, and higher buckling modes still contribute below about $0.5P_{cr}$. The method needs no reading near $P_{cr}$ because Eq. 6 is a straight line at every load.

**P4.** $P$ = 904 N: $y_{max}$ = 2.50 mm, $M = P(e + y_{max})$ = 4.07 N·m, $\sigma_{max}$ = 5.61 + 23.9 = 29.5 MPa (Eq. 8 gives 29.5 MPa). Without deflection the bending stress would be 10.6 MPa and $\sigma_{max}$ = 16.2 MPa: the deflection multiplies the bending stress by 2.25 $= \sec(\pi/(2\sqrt2))$.

**P5.** (Simulation, exact page code.) "Lab Part A: pinned, 450 mm": 1 821.4 N closed form and 1 821.4 N by finite elements (E = 68.9 GPa, the series' truth value in the page's material table). Springs, $k$ = 2800 N·m/rad, 600.5 mm: $P_{cr}$ = 3 752 N, $K$ = 0.5221 (ideal fixed ends: 4 091 N). "Lab Part C, e = 2 mm": first-yield load 1 628 N, against 12 831 N from Eq. 10.37 (both treat the 0.46 mm bow as an extra offset $(4/\pi)\delta_0$ = 0.59 mm). "Lab Part D": Euler 45.54 kN, tangent modulus 35.65 kN, reduced modulus 36.94 kN, fiber model 33.31 kN.

**P6.** (a) A column kicking sideways if a knife edge slips (seat both ends, guard, hands out); the screw loader (turn by hand, back off before touching); Part D's large load and possible fragments (shield, distance). (b) $\sigma$ = 152 MPa = 55 % of $\sigma_Y$ at $\delta$ = 5 mm on the 300 mm bar, the worst of the three. The limit keeps every bar elastic so it can be reused and the Southwell analysis stays valid; in the sample data the largest stress in Parts A–C is 142 MPa (52 % of $\sigma_Y$).

::: {.needspace lines="12"}
:::

## 3. Analysis solutions

| $L$ (mm) | $L/r$ | Euler $P_{cr}$ (N) | Southwell $P_{cr}$ (N) | Difference (%) | Limit (%) | Southwell $\delta_0$ (mm) | Bow (mm) | $E$ from $P_{cr}$ (GPa) |
|----|-----:|---------:|---------:|------:|-----:|---------:|-----:|---------:|
| 300 | 163.7 | 4 072 ± 62 | 4 103 ± 24 | 0.77 | 1.62 | 0.380 ± 0.001 | 0.26 | 68.99 ± 0.59 |
| 450 | 245.5 | 1 810 ± 27 | 1 829 ± 11 | 1.05 | 1.60 | 0.533 ± 0.002 | 0.46 | 69.18 ± 0.56 |
| 600 | 327.6 | 1 016 ± 15 | 1 026 ± 6 | 0.97 | 1.59 | 0.757 ± 0.003 | 0.62 | 69.12 ± 0.55 |

: Table K2. Part A: Southwell fits (readings with $P \ge 0.5\,P_{pred}$) and Euler predictions with Lab 2's $E$, the measured section and lengths. Limit = $2\sqrt{u_1^2 + u_2^2}$ (Eq. 11).

**A1.** Southwell fits use 12, 13 and 13 readings (from 2 250, 1 000 and 550 N up). All three critical loads agree with Euler (Table K2); the Southwell loads run about 1 % above Euler, which A6 traces to $E$. Slope of $\log P_{cr}$ against $\log L$: −1.997 ± 0.005, as Eq. 1 requires. $E$ from the three loads: 69.10 ± 0.54 GPa, against Lab 2's 68.46 ± 0.94 GPa: agree ($|\Delta|$ = 0.93 % of $E$, limit 1.58 %). *Interpret:* Southwell's $\delta_0$ exceeds the surface-plate bow by 0.07–0.14 mm because the knife edges put the load slightly off the axis; an offset $e$ acts like a bow of $(4/\pi)e$, so $e \approx (\pi/4)(\delta_{0,S} - \text{bow})$ = 0.094, 0.057 and 0.107 mm, about 0.09 mm (truth 0.08 mm). The last readings reach only 0.929–0.933 of $P_{cr}$, yet the fits find $P_{cr}$ to a fraction of a percent.

**A2.** Fixed–fixed: $P_{cr}$ = 3 730 ± 22 N, $K$ = 0.5220 ± 0.0041, against 0.5: disagree; Euler with $K$ = 0.5 is 9.0 % above the measurement. Fixed–pinned: 1 765 ± 10 N, $K$ = 0.7120 ± 0.0056 against 0.699: disagree (Euler 3.7 % high). From Eq. 3 with the fixed–fixed result ($x = pL/2$ = 3.0093): $k$ = 2 800 ± 500 N·m/rad (95 % interval 2 400–3 370; $kL/EI$ = 45.2; truth mean 2 515). Eq. 4 with this $k$ predicts 1 758 ± 15 N for the fixed–pinned test ($K$ = 0.7133), against 1 765 ± 10 N measured: agree ($|\Delta|$ = 0.38 %, limit 0.84 %; the common load-cell error cancels). *Check:* Eq. 3 with $k \to \infty$ gives $\tan x = 0$, $x = \pi$, $K$ = 0.5. *Interpret:* assuming fixed ends overstates this column's capacity by 9.0 %, a margin a designer would not see; a clamp with $kL/EI$ ≈ 45 is "fixed" only to within 9 % in load.

| Load (N) | Part A δ (mm) | e = 1: δ (mm) | Difference (mm) | Eq. 7, e = 1 mm (mm) | e = 2: δ (mm) | Difference (mm) | Eq. 7, e = 2 mm (mm) |
|------:|------:|------:|------:|------:|------:|------:|------:|
| 200 | 0.07 | 0.22 | 0.15 | 0.15 | 0.37 | 0.30 | 0.30 |
| 400 | 0.15 | 0.51 | 0.36 | 0.35 | 0.84 | 0.69 | 0.70 |
| 600 | 0.26 | 0.87 | 0.61 | 0.61 | 1.46 | 1.20 | 1.22 |
| 800 | 0.42 | 1.40 | 0.98 | 0.97 | 2.33 | 1.91 | 1.94 |
| 1 000 | 0.64 | 2.18 | 1.54 | 1.51 | 3.64 | 3.00 | 3.03 |
| 1 200 | 1.02 | 3.44 | 2.42 | 2.40 | 5.77 | 4.75 | 4.80 |

: Table K3. Part C minus Part A at the same loads (every second load shown), with Eq. 7 for the nominal offsets and $P_{cr}$ from A1.

**A3.** Fitting Eq. 7 to the differences: $e$ = 1.009 ± 0.017 mm and 1.979 ± 0.033 mm, both agree with the grooves (1.00 and 2.00 ± 0.02 mm). From the gages, the change of the lever arm minus the change of deflection gives $e$ = 1.002 ± 0.015 and 1.951 ± 0.018 mm, the same within a few hundredths of a millimeter: the gages see the moment $P(e + y_{max})$ of Beer Fig. 10.23. *Check:* at 200 N the difference is close to $(\pi^2/8)e\,P/P_{cr}$. *Interpret:* from 600 to 1200 N the eccentric deflection grows by a factor 3.97 (e = 1 mm) and 3.96 (e = 2 mm), against 3.95 from Eq. 7 and 2 for a linear response: the effects of several loads cannot be added, although at one load the responses to the bow and to the offset do add (which is why the subtraction works).

**A4.** With $P_{cr}$ from A1 and $\sigma_Y$ = 273.7 MPa, Eq. 8 gives first yield at 1 740 N ($e$ = 1 mm) and 1 661 N ($e$ = 2 mm), that is 0.951 and 0.908 of $P_{cr}$; Eq. 10.37 gives 22.7 kN and 15.3 kN, 9.2 times too high for $e$ = 2 mm, because it ignores the deflection, which reaches 25.1 mm at first yield. At 1 300 N with $e$ = 2 mm the back gage gives 83.0 MPa; Eq. 8 with the 2 mm offset alone gives 70.4 MPa (15 % low), and adding the Part A stress at the same load (22.0 MPa, minus the axial 8.05 MPa counted twice) gives 84.4 MPa, within 1.6 %. *Check:* $e \to 0$ gives $P_Y \to P_{cr}$ here, because $P_{cr} < \sigma_YA$. *Interpret:* $\sigma_{max}$ grows faster than $P$, so dividing the stress by F.S. leaves a much smaller margin on the load than F.S.; the factor must divide the load at first yield (Beer §10.2).

**A5.** Part D: maximum 31.03 ± 0.18 kN ($\sigma$ = 192 MPa) at $L/r$ = 49.1, reached at a lateral deflection of 0.30 mm. Euler: 45.24 kN ($\sigma_{cr}$ = 280 MPa > $\sigma_Y$), 46 % high; $\sigma_YA$ = 44.18 kN, 42 % high; tangent modulus (Eq. 9): 35.61 kN ($\sigma_t$ = 221 MPa, $E_t$ = 53.9 GPa), 14.8 % high; reduced modulus 36.89 kN; 1.95 × the AA allowable ($\sigma_{all}$ = 103.0 MPa by Eq. 10.44b): 32.43 kN, 4.5 % from the measurement. On the column curve the pinned tests sit on Euler's hyperbola, the clamped tests sit on it at their measured $K$ (not at Beer's ideal), and Part D sits below the tangent-modulus curve. *Check:* at $L/r$ = 245 the tangent-modulus and Euler curves coincide. *Interpret:* only the tangent-modulus load, from the material's own curve, comes within 15 %; the bar's small bow and offset, amplified near the knee of the stress–strain curve, take the rest. The AA formula times its factor of safety lands near the measurement, as a design curve calibrated on real columns should.

**A6.** Table 5 rows are in Table K1. $E$ from the axial strain, 30 readings below half of each $P_{cr}$: 69.34 ± 0.80 GPa (agree with Lab 2; difference 0.88 GPa, limit 1.23 GPa; intercept 0.3 µε). *Named causes for the systematic differences:* the Southwell loads and the strain-based $E$ both run high because the load cell reads 0.3 % high (inside its ±0.5 % specification) and Lab 2's $E$ is itself 0.6 % below the series' truth value; Part B's disagreement with Beer's $K$ is the clamps' finite stiffness, quantified by $k$.

**M1.** (a) Euler overstates the Part D load by 46 %; it predicts more than $\sigma_Y$ below $L/r$ = 49.7. (b) Fixed ends are unconservative by 9.0 % (fixed–fixed) and 3.7 % (fixed–pinned); $K$ comes within 1 % of 0.5 only for $kL/EI$ of about 200 or more, more than four times these clamps. (c) At $\delta = L/60$ a perfect pinned column carries only 0.034 % more than $P_{cr}$ (and 1.3 % at $L/10$); the 450 mm bar would first yield at $\delta$ ≈ 24.5 mm. (d) Eq. 10.37 overstates the first-yield load for $e$ = 2 mm by a factor of 9.2. (e) The knife edges are about 0.09 mm off the axis. *Ranking:* (d) and (a) are gross errors for the cases they touch; (b) is a 4–9 % unconservative error hidden in every design that assumes fixed ends; (e) is a 0.1 mm imperfection that Southwell absorbs; (c) is negligible in this lab's range.

## 4. Challenge and Extension solutions

**C1.** Bending-strain Southwell for the 450 mm bar: $P_{cr}$ = 1 829 ± 11 N, 0.03 % from the dial-gage fit; the intercept, 83 µε, is the bending strain of the equivalent bow. Strain gages work on columns too stiff or too short for a dial gage, and on structures where the deflection cannot be reached.

**C2.** $k = -2xEI/(L\tan x)$ with $x \propto \sqrt{P}$ gives $(dk/k)/(dP/P) = \tfrac12[1 - x/(\sin x\cos x)]$ = 12.0 at $x$ = 3.0093: a 1 % error in $P_{cr}$ is a 12.0 % error in $k$. The fixed–pinned test is even more sensitive (about 28; its own $k$ would be 3 100 N·m/rad). Better: a shorter fixed–fixed bar (smaller $kL/EI$, $x$ further from $\pi$), or a direct moment–rotation test of the clamp, as in Lab 7.

**C3.** A constant moment $M_0$ on $0 < x < L$ has the first sine coefficient $(4/\pi)M_0$; with $M_0 = Pe$ it acts on the first mode like a bow of $(4/\pi)e$. Southwell on the raw Part C data gives $\delta_0$ = 1.797 and 2.999 mm ($P_{cr}$ = 1 826 and 1 824 N); subtracting Part A's 450 mm intercept and multiplying by $\pi/4$ gives 0.99 and 1.94 mm, close to the grooves.

**X1.** Appendix D.3. Limits: $k \to 0$ in Eq. 3 gives $\tan(pL/2) \to \infty$, $pL = \pi$ (Eq. 10.11a); $k \to \infty$ in Eq. 4 gives $\tan pL = pL$ (Eq. 10.19).

**X2.** With $\theta$ the slope, $EI\theta'' + P\sin\theta = 0$; integrating once with zero moment at the pins and once more over the half length gives $\sqrt{P/EI}\,L/2 = K(k)$ with $k = \sin(\theta_0/2)$, so $P/P_{cr} = (2K/\pi)^2$; the lateral deflection is $\delta = 2k/p$, so $\delta/L = k/K(k)$. For small $k$, $K \approx (\pi/2)(1 + k^2/4)$, giving $P/P_{cr} - 1 \approx k^2/2 \approx (\pi^2/8)(\delta/L)^2$. A deflection of $L/10$ raises the load only 1.27 %: the column has essentially no reserve after buckling, unlike a plate, whose membrane stresses stiffen it.

**X3.** In the simulation the nearly perfect 90 mm bar stays straight up to the tangent-modulus load, then bends while the load still rises a little toward the reduced-modulus load; at the tangent-modulus load no fiber has to unload, which is why bending starts there (Shanley). Any imperfection makes the column bend earlier, and the maximum falls below $P_t$ (A5).

## 5. Design problem D1: reference solution

| Tube | Mass (kg/m) | $D_o/t$ | $L/r$ (pinned) | Allowable load, pinned (kN) | First yield, $e$ = 2 mm, pinned (kN) | OK, pinned? | Allowable load, $K$ = 0.52 (kN) | OK with $K$ = 0.52? |
|------------------|-------:|------:|------:|------:|------:|-----|------:|-----|
| 44.45 × 1.65 | 0.599 | 26.9 | 132.1 | 4.53 | 8.26 | no | 16.75 | yes |
| 50.80 × 1.65 | 0.688 | 30.8 | 115.0 | 6.85 | 12.41 | no | 22.84 | yes |
| 44.45 × 2.11 | 0.758 | 21.1 | 133.4 | 5.61 | 10.24 | no | 20.75 | yes |
| 57.15 × 1.65 | 0.777 | 34.6 | 101.9 | 9.87 | 17.71 | no | 28.22 | yes |
| 63.50 × 1.65 | 0.866 | 38.5 | 91.4 | 13.65 | 24.27 | yes | 33.68 | yes |
| 50.80 × 2.11 | 0.871 | 24.1 | 116.1 | 8.53 | 15.45 | no | 28.72 | yes |
| 57.15 × 2.11 | 0.985 | 27.1 | 102.7 | 12.31 | 22.11 | no | 35.59 | yes |
| 76.20 × 1.65 | 1.043 | 46.2 | 75.9 | 23.91 | 41.39 | no | 44.72 | no |
| 63.50 × 2.11 | 1.099 | 30.1 | 92.1 | 17.08 | 30.37 | yes | 42.56 | yes |
| 44.45 × 3.18 | 1.113 | 14.0 | 136.7 | 7.86 | 14.35 | no | 29.06 | yes |
| 50.80 × 3.18 | 1.284 | 16.0 | 118.5 | 12.06 | 21.84 | no | 41.59 | yes |
| 76.20 × 2.11 | 1.326 | 36.1 | 76.3 | 30.02 | 52.00 | yes | 56.68 | yes |
| 57.15 × 3.18 | 1.456 | 18.0 | 104.6 | 17.53 | 31.50 | yes | 51.92 | yes |
| 44.45 × 4.78 | 1.608 | 9.3 | 141.6 | 10.58 | 19.32 | no | 39.13 | yes |
| 63.50 × 3.18 | 1.627 | 20.0 | 93.7 | 24.46 | 43.52 | yes | 62.40 | yes |
| 50.80 × 4.78 | 1.866 | 10.6 | 122.3 | 16.46 | 29.84 | yes | 58.81 | yes |
| 76.20 × 3.18 | 1.970 | 24.0 | 77.4 | 43.35 | 75.21 | yes | 83.64 | yes |
| 57.15 × 4.78 | 2.123 | 12.0 | 107.6 | 24.20 | 43.50 | yes | 74.24 | yes |
| 63.50 × 4.78 | 2.381 | 13.3 | 96.0 | 34.05 | 60.64 | yes | 89.91 | yes |
| 76.20 × 4.78 | 2.896 | 15.9 | 79.0 | 61.13 | 106.26 | yes | 121.75 | yes |

: Table K4. D1 candidates, lightest first. Requirements: allowable load ≥ 12 kN; first yield ≥ 23.4 kN (1.95 × 12 kN); $D_o/t$ ≤ 40. Lab 2 $E$ and Lab 1 $\sigma_Y$.

**D1 — reference design: 63.50 × 1.65**, 0.866 kg/m, pinned ends ($K$ = 1, gussets bolted, free to rotate in their plane). $A$ = 320.6 mm², $I$ = 153.4 × 10³ mm⁴, $r$ = 21.88 mm, $L/r$ = 91.4 (Euler branch, Eq. 10.45b): $\sigma_{all}$ = 42.6 MPa, allowable load 13.65 kN ≥ 12 kN. $P_{cr}$ = 25.91 kN; secant first yield with $e$ = 2 mm: 24.27 kN ≥ 23.4 kN (this governs, with a 4 % margin); at the service load $y_{max}$ = 2.16 mm and $\sigma_{max}$ = 47.8 MPa. $D_o/t$ = 38.5. **The trap:** with $K$ = 0.52 taken from Part B's clamps, the lightest tube that passes is 44.45 × 1.65 (0.599 kg/m, 31 % lighter: $L_e/r$ = 68.7, allowable 16.75 kN). With the gussets' true pinned behavior its $L/r$ is 132.1, its allowable load 4.53 kN and its Euler load **8.59 kN, below the 12 kN service load: it would buckle.** A student who applies F.S. to the stress instead of the load (solving $\sigma_{max} = \sigma_Y/1.95$) gets 21.9 kN for the reference tube instead of 12.44 kN, a large unconservative error. *Assumptions that could invalidate a design:* bolted gussets with in-plane fixity (would justify $K < 1$, but only with a measured stiffness); out-of-straightness larger than the 2 mm allowance (rule of thumb $L/1000$ = 2 mm here); local buckling or crushing at the bolt holes; welding near the ends (heat-affected 6061 loses roughly half its yield strength).

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
2. Calling the last load recorded the "buckling load": the readings stop at 0.929–0.933 of $P_{cr}$ by design.
3. Fitting the Southwell line through every reading: the low-load points (seating, zero offsets, higher modes) bend the plot; use $P \ge 0.5P_{cr}$.
4. Comparing the raw Part C deflections with Eq. 7: the bow and the knife-edge offset are still in them, and the fitted $e$ comes out 1.43 and 2.40 mm instead of about 1 and 2 mm.
5. Applying the factor of safety to the stress in the secant formula (D1: 21.9 kN instead of 12.44 kN).
6. Taking $K$ = 0.5 for any "fixed" end: Part B's clamps give 0.5220 ± 0.0041, and bolted gussets are closer to pinned.
7. Using Euler's formula for Part D ($\sigma_{cr}$ = 280 MPa > $\sigma_Y$).
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

**Safety.** The bars are elastic throughout (largest stress about 52 % of $\sigma_Y$) and are reused; Part D destroys one 90 mm bar per session. A bar that slips from a knife edge springs sideways: keep the guard on and hands out of the frame under load.

**Running without equipment.** Give students `sample_data.csv` and Appendix A; Sections 3–5 of this key apply unchanged. **Your own class data:** export the columns listed in Table A1, fill in `src/specimen_measurements.json` with the class's dimensions, lengths and bows, and run `src/lab09_analysis.py` and `src/make_key.py`.

**The simulation** (P5, A5, D1) checks each closed form against an independent numerical method; its tests are in `tests/` and summarized in `tests/VERIFICATION.md`.

## 10. Self-critique and revisions

Before release, the lab was reviewed as a demanding instructor at a top program would review it. The three biggest weaknesses found, and the fixes made:

1. **The original procedure loaded in fixed steps of load, past the critical load.** A real bar cannot carry a load step above $P_{cr}$, and the first draft of the sample data recorded nonsense there. *Fix:* load steps up to 75 % of the predicted $P_{cr}$, then deflection steps of $L/600$ to $L/60$ (how a screw-loaded strut test is actually run); the data, the safety limits and the Southwell selection all follow this.
2. **Clamped ends were modeled as forcing a bowed bar straight at the clamp.** The fixed–pinned Southwell estimate came out 6 % low as a result. *Fix:* the finite-element model now solves for the change of deflection, so a clamp grips the bar at its initial slope and a spring resists only the change; the Southwell bias for clamped ends dropped below 0.3 %, and the generator, the page and the tests use the same formulation.
3. **The page's eigenvalue solver could converge to the wrong mode.** A symmetric start vector trapped inverse iteration in the second mode with one element (500 % error), and round-off in the stiffness quadratic form stalled the iteration at large $N$. *Fix:* a non-symmetric start vector and the quotient $x^TGx/x^TGz$; convergence is now a clean $N^{-4}$ for all ends.

**Known limitations (not fixed).** Both clamps are treated as equal (the truth model's differ by 5 %); knife edges are frictionless; Part D's half-sine fiber model slightly overstates the maximum load; the elastica correction at $L/60$ (negligible) and residual stresses are ignored; D1 checks local buckling only by $D_o/t$.

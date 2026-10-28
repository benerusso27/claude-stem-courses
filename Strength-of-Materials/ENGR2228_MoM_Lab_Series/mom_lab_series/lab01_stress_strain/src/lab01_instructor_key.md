# Lab 1 — Instructor Key: Tension Test and the Stress–Strain Diagram

::: {custom-style="Instructor"}
**For instructors only. Do not distribute to students.** Every number in this key is computed by `src/lab01_analysis.py` (and `src/make_key.py`) from `sample_data.csv` and `src/specimen_measurements.json`, or by the simulation's own model code. To build a key for your own class data, put your CSV and measurements in the same format and run `python3 src/lab01_analysis.py your.csv your_measurements.json`. Uncertainties are expanded ($U = 2u$) unless marked $u$.
:::

## 1. Results at a glance (sample data)

| Quantity | 1018 steel | 6061-T6 aluminum | Reference |
|---|---|---|---|
| $d_0$ (mm), $u_d$ | 10.005, 0.0118 | 9.995, 0.0118 | nominal 10.00 |
| $A_0$ (mm²), $u_A/A$ | 78.62, 0.24 % | 78.46, 0.24 % | 78.54 |
| $E$ (GPa) | 205.2 ± 2.4 | 68.8 ± 0.8 | 205 ± 6 / 68.9 ± 2.0 |
| Upper / lower yield (MPa) | 321.5 ± 2.4 / 296.2 ± 2.2 | — | 250–340 |
| 0.2 % offset $\sigma_Y$ (MPa) | 296.1 ± 2.2 (on the plateau) | 273.7 ± 2.1 | 255–300 (Al) |
| $\sigma_U$ (MPa) | 451.9 ± 3.4 | 314.3 ± 2.3 | 400–480 / 290–330 |
| $\varepsilon_u$ (corrected crosshead) | 0.190 ± 0.014 | 0.049 ± 0.006 | — |
| Hollomon $K$ (MPa), $n$ | 811, 0.2298 ± 0.0007 | 415, 0.0747 ± 0.0003 | — |
| $C_m$ (mm/kN) | 0.00800 ± 0.00004 | 0.00800 ± 0.00004 | true value 0.00800 |
| $\Delta_{toe}$ (mm) | 0.0501 ± 0.0004 | 0.0500 ± 0.0004 | true value 0.0500 |
| $E_{app}$ measured / Eq. 8 (GPa) | 65.04 ± 0.28 / 65.12 | 40.01 ± 0.11 / 39.98 | — |
| %EL / %RA | 33.9 ± 0.1 / 60.0 ± 0.6 | 12.4 ± 0.1 / 42.1 ± 0.8 | 25–38 / 8–17 %EL |
| True stress at fracture: formula / neck (MPa) | 398.5 / 743.7 ± 11.7 | 248.7 / 382.3 ± 5.1 | — |

: Table K1. Results from the sample data.

The sample data were generated from a known "truth" model (`src/generate_sample_data.py`, values in `src/truth.json`). The closure test in `tests/test_lab01_independent.py` confirms that the analysis recovers every truth value within its stated uncertainty.

## 2. Pre-lab solutions

**P1.** $A_0 = \pi(10.00)^2/4 = 78.54$ mm².

(a) Using mid-range reference values (steel $\sigma_Y \approx 295$, $\sigma_U \approx 440$ MPa; aluminum $\sigma_Y \approx 278$, $\sigma_U \approx 310$ MPa): steel $P_Y \approx 23.2$ kN, $P_U \approx 34.6$ kN (about 35 % of 100 kN); aluminum $P_Y \approx 21.8$ kN, $P_U \approx 24.3$ kN (about 24 %). Both lie well inside the machine's range; the 50 kN overload stop leaves margin.

(b) Elastic elongation at yield over 50 mm: steel $295/205\,000 \times 50 = 0.0720$ mm; aluminum $278/68\,900 \times 50 = 0.2017$ mm. Elongation across the 45–180 MPa window: steel $\Delta\delta_w = 135/205\,000 \times 50 = 32.9$ µm; aluminum 98.0 µm. The criterion $r/\sqrt{12} \le 0.001\,\Delta\delta_w$ gives $r \le 0.11$ µm for steel (0.34 µm for aluminum). The crosshead's 1 µm resolution gives a rounding error of 0.88 % of the steel window, about nine times the criterion, even before compliance (P3) is considered. Only the extensometer can measure $E$.

(c) Crosshead travel at fracture ≈ $\varepsilon_f L_c$ + machine stretch: steel ≈ 0.3 × 60 ≈ 20 mm, aluminum ≈ 0.12 × 60 ≈ 7 mm. Phase 1 (to 4 % strain at 1.0 mm/min) needs about 0.04 × 60 + $C_mP$ + toe ≈ 2.7 mm, about 2.7 min. Phase 2 at 5.0 mm/min: steel (20 − 2.7)/5 ≈ 3.5 min, aluminum (7 − 2.7)/5 ≈ 0.9 min. Totals are about 6 min and 3.5 min (the sample data run 360 s and 213 s). Units: mm ÷ (mm/min) = min.

**P2.** (a) $\varepsilon_t = \int_{L_0}^{L} dL/L = \ln(L/L_0) = \ln(1+\varepsilon)$. Then $d\varepsilon_t = d\varepsilon/(1+\varepsilon)$, and with $\sigma_t = \sigma(1+\varepsilon)$, $\sigma_t\,d\varepsilon_t = \sigma\,d\varepsilon$. (b) $\ln(1+\varepsilon)/\varepsilon = 0.99$ at $\varepsilon = 2.03$ %. The series $\ln(1+\varepsilon) \approx \varepsilon - \varepsilon^2/2$ gives the same estimate, $\varepsilon/2 = 0.01$.

**P3.** $A_0C_m/L_c = 78.54 \times 0.008/60 = 0.01047$ 1/GPa. Steel: $E_{app} = 1/(1/205 + 0.01047) = 65.1$ GPa (31.8 % of $E$). Aluminum: 40.0 GPa (58.1 %). The steel curve misleads more: the machine term is the same for both, but it is a larger share of the total compliance when the specimen is stiff. Limits: $C_m \to 0$ gives $E$; $E \to \infty$ gives $L_c/(A_0C_m) = 95.5$ GPa, the stiffness of the machine itself.

**P4.** $\varepsilon_{t,U} = n = 0.20$, $\varepsilon_u = e^{0.2} - 1 = 0.2214$. Eq. 16: $\Delta\varepsilon_{t,u} = 0.88\sqrt{2(0.2)(0.003)} = 0.0305$, so $\varepsilon_{t,u} \approx 0.1695$ and $\varepsilon_u \approx 0.1847$. The maximum load drops by only $\delta_A$ = 0.3 %.

**P5.** Simulation, default settings ($\delta_A$ = 0.3 %, $M$ = 400):

| Preset | $\sigma_Y$ (MPa) | $\sigma_U$ (MPa) | $\varepsilon_u$ (%) | Elongation after fracture (%) | $E_{app}$ (GPa) |
|---|---:|---:|---:|---:|---:|
| Steel | 294.8 | 450.6 | 17.7 (closed form 21.1) | 33.0 | 65.1 |
| Aluminum | 271.9 | 313.0 | 5.2 (closed form 6.8) | 12.5 | 39.9 |

: Table K2. Simulation predictions.

Aluminum necks at the smaller strain because its hardening exponent is much smaller (0.06 vs. 0.20): by Considère, the hardening rate falls to the true stress sooner.

**P6.** (a) $\sigma_b/\sigma = 8e/d = 8(0.1)/10 = 0.08$, i.e. 8 %. Bending adds $+\varepsilon_b$ on one side and $-\varepsilon_b$ on the opposite side, so the average of two diametrically opposite readings removes it to first order, and the slope of $\sigma$ against the average strain is $E$. (b) Hands stay out while the grips close (pinch point) and whenever the crosshead can move: during the test and especially near fracture. The extensometer is removed only with the crosshead on hold.

## 3. Analysis solutions

**A1.** Steel: linear elastic line, a sharp upper yield point (≈ 321.5 ± 2.4 MPa), a drop to a serrated plateau near 296.2 ± 2.2 MPa that ends at about 0.0193 strain, strain hardening to the maximum, then necking (in the crosshead record) and fracture. Aluminum: linear to about 200 MPa, gradual yielding with no plateau, little hardening, an early maximum, necking, fracture. *Check:* $\sigma = 0$ at $P = 0$ within the load noise (intercepts in A2 are below 0.2 MPa); the elastic slopes are in the ratio $205/68.9 \approx 3.0$, as the moduli are. *Common error:* plotting crosshead strain on the zoomed graph, which makes steel look three times softer than it is.

**A2.** Fit window 45–180 MPa: steel 37 points, $E$ = 205.22 GPa, intercept -0.01 MPa, statistical part 0.19 %. Aluminum: 61 points, 68.75 GPa, intercept 0.11 MPa, statistical part 0.05 %. Window halves: steel 205.5 vs. 206.2 GPa (difference 0.73 GPa, $2\times$ combined s.e. 1.61 GPa, so linear: $u_{win} = 0$). Aluminum: 68.7 vs. 68.6 GPa (difference 0.13, limit 0.15: linear). The budget per Eq. 22, in relative standard uncertainty: diameter $2u_d/d$ = 0.24 %; load cell, extensometer and gage length 0.5 %/√3 = 0.29 % each; statistics as above. Result: **steel $E$ = 205.2 ± 2.4 GPa, aluminum $E$ = 68.8 ± 0.8 GPa** ($U$, $k = 2$). Agreement (Eq. 23): steel $|\Delta|$ = 0.22 ≤ 6.46 GPa, agrees; aluminum 0.15 ≤ 2.14 GPa, agrees.
*Check (wider window, 45–260 MPa):* steel 204.8 GPa (-0.2 %), essentially unchanged because steel is linear up to its yield point. Aluminum 58.9 GPa (-14.3 %): the fit now includes gradual yielding and is biased low. *Interpret:* the three calibration terms dominate equally, then the diameter. A micrometer (±0.002 mm) would cut the area term about tenfold; better calibration certificates (smaller ±a) for the extensometer and load cell would cut the rest. More data points would help almost nothing.

**A3.** Steel: upper yield **321.5 ± 2.4 MPa**, lower yield **296.2 ± 2.2 MPa**. The offset method on steel gives 296.1 ± 2.2 MPa, landing on the plateau as it should. Aluminum 0.2 % offset: **273.7 ± 2.1 MPa**. Sensitivity to $E$: $\partial\sigma_Y/\partial E$ = -0.485 MPa/GPa for aluminum (the offset line cuts a curve that is flattening, so the sensitivity is small) and -0.004 for steel (cuts a flat plateau). *Check:* aluminum's linear region ends near 200 MPa < 273.7 ± 2.1 < $\sigma_U$. *Interpret:* the upper yield point depends on alignment, loading rate, machine stiffness and specimen finish; the lower yield point is what the material sustains while yielding spreads, so it is reproducible and conservative.

**A4.** (a) Raw crosshead, same window: steel $E_{app}$ = 65.04 ± 0.28 GPa, aluminum 40.01 ± 0.11 GPa. (b) Eq. 9 fit above 3 kN: $C_m$ = 0.00800 ± 0.00004 mm/kN (steel), 0.00800 ± 0.00004 (aluminum); toe 0.0501 ± 0.0004 mm and 0.0500 ± 0.0004 mm. (c) Eq. 8 predicts 65.12 and 39.98 GPa, matching (a) within uncertainty. (d) Corrected crosshead strain minus extensometer strain over the last 50 extensometer points: steel -12 $\times 10^{-6}$, aluminum -93 $\times 10^{-6}$; the splice is seamless. *Check:* $A_0C_m/L_c$ in mm²/kN = 1/GPa; as $C_m \to 0$, $E_{app} \to E$. *Interpret:* the machine and grips are about twice as compliant as the steel specimen, so crosshead strain mostly measures the machine.

**A5.** $\sigma_U$: steel **451.9 ± 3.4 MPa** ($P_{max}$ = 35.53 kN from a parabola through the peak region), aluminum **314.3 ± 2.3 MPa**. $\varepsilon_u$ (corrected crosshead): steel **0.190 ± 0.014**, aluminum **0.049 ± 0.006**. Strain span over which $P > P_{max} - 2u_P$: steel 0.0244, aluminum 0.0103; half of it, divided by √3, dominates $u(\varepsilon_u)$. *Check:* for aluminum the extensometer came off at 4.0 % strain, before $\varepsilon_u$, so the corrected crosshead strain is required. *Interpret:* at a flat maximum, a small change in load corresponds to a large change in strain, so $\varepsilon_u$ is ill-conditioned while $\sigma_U$ is well-conditioned.

**A6.** Hollomon fits: steel $K$ = 811 MPa, $n$ = 0.2298 ± 0.0007; aluminum $K$ = 415 MPa, $n$ = 0.0747 ± 0.0003. Measured $\varepsilon_{t,U} = \ln(1+\varepsilon_u)$: steel 0.174 ± 0.012, aluminum 0.047 ± 0.006. Discrepancy $n - \varepsilon_{t,U}$: steel 0.056, aluminum 0.027, both larger than the combined $U$ (steel 0.012, aluminum 0.006): **disagree**. *Check (direct Considère):* on the smoothed data the slope $d\sigma_t/d\varepsilon_t$ equals $\sigma_t$ at $\varepsilon_t$ = 0.170 (steel) and 0.047 (aluminum), matching the measured necking strains. Considère's criterion itself holds; the disagreement comes from the Hollomon prediction. Two quantified reasons:
(i) *Imperfection.* The diameter readings span 0.01 mm, so $\delta_A \approx 2(0.01)/10 = 0.20$ %. Eq. 16 gives a shortfall of 0.0267 (steel) and 0.0152 (aluminum), so the predictions become 0.203 and 0.059.
(ii) *Fit form.* The remaining gaps (0.029 steel, 0.012 aluminum) arise because the hardening is not a single power law. Steel's hardening restarts after the Lüders plateau (its curve is shifted, like Swift's $\varepsilon_0$), and aluminum's exponent varies with strain. A global $n$ then overstates the local exponent $d\ln\sigma_t/d\ln\varepsilon_t$ at necking, which by Considère must equal $\varepsilon_{t,U}$.
Full credit requires the direct check and at least one quantified cause.

**A7.** %EL: steel **33.9 ± 0.1**, aluminum **12.4 ± 0.1**. %RA: steel **60.0 ± 0.6**, aluminum **42.1 ± 0.8**. Modulus of resilience: steel 0.214 MJ/m³, aluminum 0.545 MJ/m³ (aluminum stores more elastic energy per volume because its $E$ is low). Energy to maximum load: steel 77.10 MJ/m³ (engineering) = 77.10 (true); aluminum 14.08 = 14.08. Area to fracture with corrected crosshead strain: steel 124.0, aluminum 31.7 MJ/m³. Corrected crosshead strain at fracture: steel 31.6 %, aluminum 11.4 %, both lower than %EL. The neck's extra length is divided by $L_c$ = 60 mm instead of $L_0$ = 50 mm, and %EL is measured after elastic recovery. *Interpret:* for absorbing an overload without breaking, choose steel: about five times the energy to maximum load and four times the area to fracture.

**A8.** Use Table K1 and the simulation values in Table K2. Expected verdicts: $E$ agrees for both materials; $E_{app}$ agrees with Eq. 8; $\sigma_U$ from the simulation preset agrees within a few percent (the preset is a smooth fit); $\varepsilon_u$ disagrees with the Hollomon/Considère prediction (A6) and is matched by the simulation only when $\delta_A$ is set from the diameter readings; for steel the yield plateau is absent from the simulation (X3). Full credit needs each discrepancy above $U$ explained with a named, quantified cause.

**M1.** Steel: $\sigma_f(1+\varepsilon_f)$ = 297.7 × (1 + 33.9/100) ≈ **398.5 MPa**, versus $P_f/A_f$ = 23.40 kN / (π 6.330²/4) = **743.7 ± 11.7 MPa**; the formula is off by -46 %. Aluminum: **248.7** vs. **382.3 ± 5.1 MPa** (-35 %). (b) The failed assumption is uniform deformation: Eq. 12 uses the gage-average strain, but after the maximum load the neck strains far more than the average ($\varepsilon_t$ in the neck is 0.916 for steel, against $\ln(1+\varepsilon_f) \approx 0.29$). In the simulation (default settings), the "σ(1+ε)" and "neck σt" readings first differ by more than 2 % right at the maximum load. For steel this happens slightly *before* it (ε ≈ 17.2 % vs. ε_u = 17.7 %), because the weaker neck site starts to strain ahead of the rest of the gage; for aluminum it happens just after (ε ≈ 5.20 % vs. 5.16 %). Credit either description if it is tied to the maximum load and explained. (c) The curved neck profile creates radial and hoop tensile stresses (a triaxial state). The axial stress peaks at the center, and the uniaxial flow stress is lower than $P/A$ by a factor of 1.1–1.25 (Bridgman, X2).

## 4. Challenge and Extension solutions

**C1.** Algebra as in Appendix D.5 of the handout. Simulation (steel preset; drop in $\varepsilon_{t,u}$, numerical vs. Eq. 16): 0.05 % → 0.0120 vs 0.0123 (+2 %) | 0.10 % → 0.0168 vs 0.0174 (+3 %) | 0.30 % → 0.0284 vs 0.0301 (+6 %) | 1.00 % → 0.0493 vs 0.0550 (+12 %) | 3.00 % → 0.0787 vs 0.0953 (+21 %). Log–log slope 0.46 (theory 0.5). Eq. 16 is off by 20 % near $\delta_A$ ≈ 3 % for steel. For aluminum (0.05 % → 0.0066 vs 0.0069 (+5 %) | 0.10 % → 0.0092 vs 0.0097 (+6 %) | 0.30 % → 0.0152 vs 0.0169 (+11 %) | 1.00 % → 0.0253 vs 0.0308 (+22 %) | 3.00 % → 0.0376 vs 0.0534 (+42 %), slope 0.43) it is off by 20 % already at $\delta_A$ ≈ 1 %, consistent with the validity condition $\delta_A \ll n/2$ (aluminum's $n/2 \approx 0.03$).

**C2.** 4000 Monte Carlo draws: $u(E)$ = 0.378 GPa (first-order 0.382), $u(\sigma_Y)$ = 1.01 MPa (first-order 1.04), mean $\sigma_Y$ = 273.7 MPa. The two methods agree to within 2 %, as expected for a measurement model that is nearly linear over input changes of a fraction of a percent. Students who find a large difference have usually drawn a ±a limit as a normal distribution with standard deviation a.

**C3.** The largest sample has error $\sigma_U - \sigma(t_i) \approx \tfrac12|\sigma''|(t_i - t^*)^2 \le \tfrac18|\sigma''|h^2$. That bound has slope 2, but the actual error depends on where the nearest sample happens to fall, hence the scatter. Integrating to the largest sample moves the upper limit by up to one step, $O(h)$, while the integrand there is $\sigma_U \neq 0$, so the missing area is $\sigma_U \cdot O(h)$: first order. Integrating to a fixed strain leaves only the trapezoid error, $O(h^2)$.

**X1.** With the neck length set by the mesh, elongation after fracture keeps falling (steel: N = 2: 83.9 %, N = 5: 43.7 %, N = 12: 28.1 %, N = 32: 21.1 %, N = 80: 18.6 %, N = 200: 17.6 %; aluminum: N = 2: 38.0 %, N = 5: 17.9 %, N = 12: 10.0 %, N = 32: 6.5 %, N = 80: 5.3 %, N = 200: 4.8 %) toward $\varepsilon_u$, because softening localizes into one element of length $L_0/N$. The model has no physical neck length: real necks scale with $d_0$ through three-dimensional effects (necking geometry, triaxiality). Simulation, steel, varying $L_0/d_0$: 2d₀: 57.1 %, 3d₀: 43.7 %, 4d₀: 37.0 %, 5d₀: 33.0 %, 8d₀: 27.0 %. From the sample data, $c = (\%EL/100 - \varepsilon_u)\,L_0/d_0$ = 0.74, so a $4d_0$ gage would give about 37.6 %.

**X2.** With $a/R$ = 1: factor $(1 + 2R/a)\ln(1 + a/2R)$ = 1.216, corrected stress ≈ 611 MPa. With $a/R$ = 0.5: factor 1.116, ≈ 667 MPa. A twofold uncertainty in $R$ moves the answer by about 10 %, so a photograph with a scale bar is needed.

**X3.** The plateau ends where hardening lifts the stress clearly above the plateau, at a total strain of 0.0193. Subtracting the elastic strain $\sigma_Y/E$ gives a Lüders strain $\varepsilon_L$ ≈ 0.0179 (the truth model uses 0.017). During the plateau the load is constant, so the machine's stretch does not change and all of the crosshead motion goes into new Lüders strain: $v_{front}\,\varepsilon_L = v_{ch}$, giving $v_{front} \approx v_{ch}/\varepsilon_L$ ≈ 56 mm/min ≈ 1 mm/s. The band therefore crosses the 60 mm reduced section in about 60 s; the sample data's plateau lasts 57 s (from the load drop to the start of hardening). A smooth law with $d\sigma/d\varepsilon_p > 0$ everywhere has no locally softening branch, so it cannot nucleate and propagate a band. The simulation's steel preset therefore goes straight from elastic to hardening.

## 5. Design problem D1: reference solutions

**D1.** Conservative strength $\sigma_Y - U$: steel 293.99 MPa, aluminum 271.61 MPa. Required gross areas (mm²):

| Requirement | Equation | Steel | Aluminum |
|---|---|---:|---:|
| FS ≥ 2.0 at service, thread | $A \ge 2.0\,P_s/(0.78\,\sigma_{Y,lo})$ | 104.7 | 113.3 |
| No yield at overload, thread | $A \ge P_o/(0.78\,\sigma_{Y,lo})$ | 78.5 | 85.0 |
| Stretch ≤ 1.20 mm, gross | $A \ge P_sL/(E\,\delta_{max})$ | 87.7 | 261.8 |
| Governs | | strength | stiffness |
| Minimum $d$ (mm) → chosen | | 11.54 → **12** | 18.26 → **19** |
| Thread stress at service (MPa), FS | | 136.03, 2.16 | 54.26, 5.01 |
| Stretch at service (mm) | | 0.93 | 1.11 |
| Mass (kg), cost ($) | | 1.60, 3.52 | 1.38, 8.96 |

: Table K3. Reference designs for D1.

Both are acceptable. Steel at 12 mm is the cheapest; aluminum at 19 mm is the lightest, governed by stiffness. Other defensible answers: steel at 13 mm for more stiffness margin; a steel rod with upset (enlarged) threaded ends; an aluminum tube. Any design that meets all three requirements with the student's own conservative strength and justifies the choice quantitatively earns full marks. A critical assumption students might name: static load only. Thread roots are stress concentrations ($K_t \approx 3$), so fatigue under walkway traffic, corrosion of steel, or galvanic contact for aluminum could govern. Check by a fatigue estimate or a code provision for tension rods.

**Rubric detail (15 points total in the report).** Requirements (3): all three translated, including that strength uses the stress area and stretch the gross area. Strength basis (4.5): uses $\sigma_Y - U$ from the student's own data; full credit only if $U$ is from their analysis. Calculations (4.5 combined with the above): correct areas, rounding up to available stock. Every check shown (3). Trade-off between two alternatives with numbers (3). Presentation and critical assumption (1.5). Typical partial credit: using a typical handbook $\sigma_Y$ (−2), using gross area at the threads (−3), forgetting the overload case when it does not govern (−0.5), forgetting stiffness for aluminum (−3, because it governs).

## 6. Expected ranges for real class data

| Quantity | Steel (1018 HR) | Aluminum (6061-T6) | If outside, suspect |
|---|---|---|---|
| $E$ from extensometer (GPa) | 195–212 | 66–71 | extensometer seating, wrong $L_e$, fit window |
| $E_{app}$ from crosshead (GPa) | 20–90 | 15–55 | not a fault: machine-specific |
| $C_m$ (mm/kN) | 0.003–0.02 | same | toe not excluded |
| Lower yield / offset $\sigma_Y$ (MPa) | 250–340 | 255–300 | specimen heat-treat or mix-up |
| $\sigma_U$ (MPa) | 400–480 | 290–330 | area error (diameter) |
| $\varepsilon_u$ | 0.15–0.24 | 0.04–0.09 | crosshead not corrected |
| Hollomon $n$ | 0.18–0.26 | 0.05–0.10 | fit range includes plateau or elastic part |
| %EL in $5d_0$ / %RA | 25–38 / 50–65 | 8–17 / 30–50 | fracture outside gage marks (retest) |

: Table K4. Expected data ranges.

## 7. Common student mistakes

1. Taking $E$ from crosshead travel, or from a stress–strain plot whose strain axis is crosshead strain.
2. Using the nominal 10.00 mm instead of the measured diameter, or using radius in $\pi d^2/4$.
3. Placing the offset line at 0.2 (not 0.002) or mixing percent and fraction in the same equation.
4. Reporting the upper yield point as $\sigma_Y$.
5. Converting to true stress past the maximum load and calling it "the true stress–strain curve."
6. Fitting the Hollomon law over a range that includes the elastic part or the Lüders plateau.
7. Adding stiffnesses instead of compliances in Eq. 8 (springs in series add compliance).
8. Treating a manufacturer's ±a as a standard uncertainty, or adding relative uncertainties linearly.
9. Dividing crosshead travel by $L_0$ instead of $L_c$, which mixes gage lengths.
10. Excess significant figures (e.g. "E = 205.21883 GPa ± 2.4").
11. In D1, using the gross area at the threads, or a handbook yield strength instead of the measured lower bound.

## 8. Grading rubric

| Part | Points | Full credit | Common deductions |
|---|---:|---|---|
| Pre-lab | 15 | P1–P6 correct with units; estimate before measuring | P1 without units (−2); P3 limits missing (−1) |
| Data & procedure | 10 | Tables 3–5 complete; checks in steps 2, 4 and 7 recorded | missing $d_0$ repeats (−3) |
| A1 | 4 | both curves, zoomed plot, stages named | crosshead strain on the zoom (−2) |
| A2 | 7 | E ± U with budget, window test, agreement test, wide-window check | no budget (−3) |
| A3 | 5 | upper and lower yield, offset with sensitivity to E | upper yield as $\sigma_Y$ (−2) |
| A4 | 7 | $E_{app}$, $C_m$ fit, Eq. 8 comparison, splice shown | stiffnesses added (−3) |
| A5 | 5 | $\sigma_U$, $\varepsilon_u$ with flat-peak uncertainty | $\varepsilon_u$ from uncorrected crosshead (−2) |
| A6 | 7 | fit, direct Considère check, two quantified reasons | reasons not quantified (−3) |
| A7 | 5 | %EL, %RA, energies, identity check, gage-length explanation | — |
| A8 | 5 | complete tables, normalized error-bar figure, every discrepancy explained | unexplained discrepancy (−1 each) |
| M1 | 10 | both values, failed assumption with timing, triaxiality | no timing from simulation (−3) |
| D1 | 15 | see Sec. 5 | see Sec. 5 |
| Communication | 5 | labeled axes, units, $x \pm U$ format | each unlabeled axis (−1) |
| Challenge | +10 | C1 (4), C2 (3), C3 (3) | — |

: Table K5. Grading rubric (100 points plus up to 10 Challenge points).

Every Core answer must include the required check and interpretation; deduct 1 point per question where either is missing.

## 9. Instructor notes

**Before the lab.** Order specimens with $d_0$ = 10.00 mm, a 60 mm reduced section and gage marks 50.0 mm apart. If your machine's capacity is below 100 kN, use 6.0 mm specimens instead (loads scale with $d_0^2$: about 13 kN for steel) and scale $L_0$ to 30 mm so that $L_0 = 5d_0$ still holds. Verify the extensometer's calibration date and gage length. Pre-set two test methods (steel and aluminum) with the rate change at 4 % extensometer strain. Print Tables 3–6b.

**Timing (2 h).** 0:00–0:10 safety briefing and pre-lab check (collect P1–P6); 0:10–0:25 diameter measurements; 0:25–0:55 steel test; 0:55–1:20 aluminum test; 1:20–1:35 post-test measurements and fracture surfaces; 1:35–2:00 simulation comparison (procedure step 13). If time is short, run aluminum while steel's post-test measurements are made.

**Safety.** Demonstrate the hold, extensometer removal and shield before the first test. The steel specimen absorbs about 0.6 kJ of plastic work (the neck is warm to the touch), and at fracture the specimen and machine release about 3 J of stored elastic energy, enough to throw a fragment: keep the shield closed. Do not let students remove grip pieces until the load reads near zero.

**Running without equipment.** Give students `sample_data.csv` and Appendix A of the handout; everything in this key applies unchanged. A hybrid works well: run one live test (steel) for the experience, and use the sample data for the analysis so all teams have identical numbers to compare.

**Your own class data.** Export each test as CSV with the columns specimen, time_s, load_N, crosshead_mm and extensometer_mm, fill a measurements JSON like `src/specimen_measurements.json`, and run `src/lab01_analysis.py`. It prints every key quantity and writes `results.json`.

**The simulation.** Students use it in P5, step 13, A8, M1, C1, C3 and X1. Its readout explains every closed-form vs. numerical gap; its tests are in `tests/` and summarized in `tests/VERIFICATION.md`.

## 10. Self-critique and revisions

Before release, the lab was reviewed as a demanding instructor at a top program would review it. The three biggest weaknesses found, and the fixes made:

1. **Eq. 16 (imperfection sensitivity) was asserted, not derived, and its range of validity was not stated.** A student could not reproduce the $\sqrt{2n\delta_A}$ step. *Fix:* the handout now states the result with its validity limit in Sec. 2.6 and gives the equilibrium argument and the quadratic expansion step by step in Appendix D.5, states the validity condition $\delta_A \ll n/2$, and Challenge C1 makes students find where it fails (20 % error at $\delta_A$ ≈ 3 % for steel, 1 % for aluminum).
2. **The uncertainty budget for $E$ ignored the choice of fitting window,** a model-form error that can exceed every instrument term for a material that yields gradually. A wider window lowers the aluminum modulus by -14.3 %. *Fix:* Eq. 22 now includes $u_{win}$ with an objective test (fit the two halves; include the term only if their slopes differ by more than twice their combined standard error). A2 requires the test, and `lab01_analysis.py` implements it.
3. **Pre-lab P1(b) asked for a "tolerable" resolution without a criterion,** so answers could not be graded consistently. *Fix:* it now specifies the criterion (rounding error $r/\sqrt{12}$ below 0.1 % of the elongation across the fitting window), which yields a definite number (0.11 µm for steel) and shows quantitatively why the crosshead cannot measure $E$.

**Known limitations (not fixed).** The sample data contain no load-train misalignment, so P6(a) cannot be demonstrated with them; a live test with an intentionally offset grip shows it. The steel preset in the simulation has no Lüders plateau (X3 turns this into a question). Eq. 16 uses a uniform-zone neck; real necks have a strain gradient, so the coefficient $1 - \ell/L_0$ is approximate.

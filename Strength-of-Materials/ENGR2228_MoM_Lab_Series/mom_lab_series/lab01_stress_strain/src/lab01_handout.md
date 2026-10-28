# Lab 1 — Tension Test and the Stress–Strain Diagram

| | |
|---|---|
| **Course** | ENGR 2228 Mechanics of Materials |
| **When** | Week 3, after lectures on Beer 8e Ch. 1 and §2.1 |
| **Textbook** | Beer, Johnston, DeWolf, Mazurek, *Mechanics of Materials*, 8th ed. (Beer 8e): §1.2A, §1.5, §2.1A–2.1E, §2.10, §2.12; §11.1B for energy density |
| **Session** | 2 hours in the lab, teams of two; report due one week later |
| **Equipment** | Universal testing machine (capacity ≥ 100 kN), 50.0 mm clip-on extensometer, digital calipers, one 1018 hot-rolled steel and one 6061-T6 aluminum specimen |
| **Files** | `lab01_simulation.html` (open in any browser, works offline), `sample_data.csv` |

## 1. Learning objectives

After this lab you will be able to:

1. Derive the engineering stress $\sigma = P/A_0$ from equilibrium and the engineering strain $\varepsilon = \delta/L_0$ from geometry, and state with numbers when each one describes the material (§1.2A, §2.1A, §2.10).
2. Extract the modulus of elasticity, the yield strength (yield point or 0.2 % offset), the ultimate strength, the percent elongation and the percent reduction of area from load–deformation data, each with a propagated uncertainty (§2.1B, §2.1D, §2.1E).
3. Explain why strain computed from crosshead travel misrepresents the elastic modulus, and correct it with a springs-in-series model (§2.1A, §2.1D).
4. Convert to true stress and true strain, derive Considère's condition for the onset of necking, and test it against your data (§2.1C, §2.12).
5. Use measured strengths, with their uncertainty, to size a member against both a strength and a stiffness requirement (§1.5).

## 2. Theory

In a tension test a universal testing machine (Figure 1) stretches a round specimen at a controlled rate while a load cell measures the force $P$ and an extensometer measures the elongation of a marked gage length. Every formula you will use follows from equilibrium, geometry (compatibility) and the material's constitutive law.

![Figure 1. Tension-test setup (schematic, not to scale): the crosshead moves up, the load cell reads P, the extensometer reads the stretch of the 50.0 mm gage.](figures/fig1_setup.png){width=4.6in}

::: {custom-style="Callout"}
**Sign convention (Beer 8e).** Tension is positive. The load $P$, the normal stress $\sigma$ and the normal strain $\varepsilon$ are positive when the specimen is pulled and stretched. Lengths are measured along the specimen axis.
:::

::: {custom-style="Callout"}
**Nomenclature.** $P$ axial load (N); $A_0$, $d_0$ original cross-sectional area and diameter; $A$, $d$ current area and diameter; $L_0$ original gage length (distance between the gage marks); $L$ current gage length; $\delta = L - L_0$ elongation; $\sigma$ engineering stress; $\varepsilon$ engineering strain; $E$ modulus of elasticity; $\sigma_Y$ yield strength; $\sigma_U$ ultimate strength; $\sigma_t$, $\varepsilon_t$ true stress and true strain; $\varepsilon_u$ uniform elongation (engineering strain at maximum load); $K$, $n$ strength coefficient and strain-hardening exponent (Lab 1 only; this $n$ is **not** Beer's modular ratio $n$ of Ch. 4); $\Delta$ crosshead travel; $\Delta_{toe}$ slack taken up as the grips seat; $C_m$ compliance of machine, grips and specimen shoulders (mm/kN); $E_{app}$ apparent modulus read from crosshead travel; $L_c$ reduced-section length; $L_e$ extensometer gage length; $\delta_{ext}$ extensometer reading; $\ell$ neck length; $\delta_A$ fractional area deficit of the weakest section; $u$ standard uncertainty; $U = 2u$ expanded uncertainty.
:::

Full derivations of the results below are in **Appendix D**; this section states each result, what it means, and when it stops applying.

### 2.1 Stress and strain

![Figure 2. (a) Specimen geometry: gage marks 50.0 mm apart on a 60 mm reduced section of diameter 10.00 mm; shaded zones next to the fillets are where the stress is not yet uniform. (b) Free body of the gage below a cut: equilibrium gives σA₀ = P.](figures/fig2_specimen_fbd.png){width=6.3in}

Cutting the gage and writing equilibrium of the lower free body (Figure 2b) gives

$$\int_{A} \sigma \, dA - P = 0 \qquad (1)$$

If the stress is uniform over the cut, the **engineering stress** is

$$\sigma = \frac{P}{A_0} \qquad (2)$$

and the **engineering strain** of the gage length is

$$\varepsilon = \frac{\delta}{L_0} \qquad (3)$$

*Worked example.* $P = 20.00$ kN on $d_0 = 10.00$ mm: $A_0 = 78.54$ mm², $\sigma = 254.6$ MPa (N/mm² = MPa).

*When Eqs. 2–3 describe the material:* the load must be centric, because an offset $e$ adds a bending stress $\sigma_b/\sigma = 8e/d$ (8 % for $e$ = 0.1 mm on 10 mm; Appendix D.1). The section must lie about one diameter away from fillets and grips (Saint-Venant, §2.10; shaded in Figure 2a). And the deformation must be uniform: Eq. 3 is an *average*, equal to the local strain only until a neck forms.

### 2.2 Hooke's law and the modulus of elasticity

Below the proportional limit the material obeys the constitutive law

$$\sigma = E\,\varepsilon \qquad (4)$$

Estimate $E$ as the least-squares slope through $N$ points in the linear region:

$$E = \frac{\sum_{i}(\varepsilon_i - \bar{\varepsilon})(\sigma_i - \bar{\sigma})}{\sum_{i}(\varepsilon_i - \bar{\varepsilon})^2} \qquad (5)$$

Use the window **45–180 MPa** (about 15–60 % of the yield strength of both materials). Below it the extensometer and grips are still seating; above it the aluminum curve bends and biases the slope low. A fitted intercept near zero is a quick check that the window is linear.

### 2.3 Yield strength

![Figure 3. Anatomy of the stress–strain diagram for an illustrative material (not your specimens). (a) Mild steel with a yield point and Lüders plateau; the true-stress curve is shown only up to maximum load. (b) Gradual yielding and the 0.2 % offset construction.](figures/fig3_stress_strain.png){width=6.4in}

Hot-rolled low-carbon steel shows an **upper yield point**, then a drop to a nearly constant **lower yield point** while a Lüders band sweeps along the gage. Report the lower yield point as $\sigma_Y$; the upper one depends on alignment, rate and machine stiffness. For materials that yield gradually, $\sigma_Y$ is the **0.2 % offset** intersection of the curve with

$$\sigma = E\,(\varepsilon - 0.002) \qquad (6)$$

the stress at which the specimen, if unloaded along a line of slope $E$ (§2.1E), would keep a permanent strain of 0.2 %.

### 2.4 What the crosshead measures

![Figure 4. The machine, grips and shoulders act as a spring in series with the specimen, so crosshead travel overstates the specimen's elastic strain. Curves are for an illustrative steel.](figures/fig4_compliance.png){width=6.3in}

The crosshead travel $\Delta$ includes the stretch of the frame, grips and shoulders, which carry the same load as the specimen (equilibrium) and whose stretches add to the specimen's (compatibility). Lumping them into a compliance $C_m$:

$$\Delta = \frac{P L_c}{E A_0} + C_m P + \Delta_{toe} \qquad (7)$$

so a stress versus crosshead-strain plot has the apparent slope

$$\frac{1}{E_{app}} = \frac{1}{E} + \frac{A_0 C_m}{L_c} \qquad (8)$$

With $A_0 = 78.5$ mm², $C_m = 0.008$ mm/kN and $L_c = 60$ mm, the machine term (0.0105 per GPa) is twice the steel term ($1/E$ = 0.0049 per GPa): the crosshead "modulus" of steel is about one third of $E$. Where both instruments record, the difference

$$\Delta - \frac{L_c}{L_e}\,\delta_{ext} = C_m P + \Delta_{toe} \qquad (9)$$

is a straight line in $P$ (above about 3 kN, once the toe is taken up), giving $C_m$ and $\Delta_{toe}$. After the extensometer comes off, the corrected crosshead strain is

$$\varepsilon_{ch} = \frac{\Delta - C_m P - \Delta_{toe}}{L_c} \qquad (10)$$

valid until the maximum load, while the reduced section still stretches uniformly. Derivation: Appendix D.2.

### 2.5 True stress and true strain

Measured against the current length and area,

$$\varepsilon_t = \ln(1+\varepsilon) \qquad (11)$$

$$\sigma_t = \sigma\,(1+\varepsilon) \qquad (12)$$

Eq. 12 assumes plastic flow at constant volume. *Limits:* elastic volume change is negligible (about 0.06 % at yield for steel); true and engineering strain differ by about $\varepsilon/2$ in relative terms (1 % at $\varepsilon$ = 2 %); and both equations assume uniform deformation, so after the maximum load they describe a fictitious uniform bar, not the neck. Before necking, $\sigma\,d\varepsilon = \sigma_t\,d\varepsilon_t$: the areas under the two curves are equal. Derivations: Appendix D.3.

### 2.6 Strain hardening and necking (Considère)

![Figure 5. Considère construction for an illustrative power-law material (n = 0.22): the load per original area peaks exactly where the hardening rate falls to the true stress.](figures/fig5_considere.png){width=6.2in}

After yielding, metals harden; a common fit is the Hollomon law

$$\sigma_t = K\,\varepsilon_t^{\,n} \qquad (13)$$

The load $P = \sigma_t A$ rises while hardening outpaces the loss of area and reaches its maximum when

$$\frac{d\sigma_t}{d\varepsilon_t} = \sigma_t \qquad (14)$$

(Considère's criterion, Figure 5). Past this point a slightly more strained section is weaker than its neighbors and keeps straining: a neck forms. For the Hollomon law,

$$\varepsilon_{t,U} = n, \qquad \sigma_U = K\,n^n e^{-n} \qquad (15)$$

*Check:* $K$ = 800 MPa, $n$ = 0.20 gives $\varepsilon_u = e^{0.2} - 1 = 0.221$ and $\sigma_U$ = 475 MPa.

**Imperfections shorten the uniform stretch.** If the weakest section's area is smaller by the fraction $\delta_A$ (0.3 % for a 0.015 mm diameter error on 10 mm), it peaks first, and the rest of the gage stops stretching early by about

$$\Delta\varepsilon_{t,u} \approx \left(1 - \frac{\ell}{L_0}\right)\sqrt{2\,n\,\delta_A} \qquad (16)$$

where $\ell$ is the neck length. This holds for $\delta_A \ll n/2$. For $n$ = 0.2, $\delta_A$ = 0.003 and $\ell/L_0$ = 0.12, the uniform strain falls from 0.20 to 0.17 while the maximum load falls only 0.3 %. Derivations of Eqs. 14–16: Appendix D.4–D.5.

### 2.7 Energy and ductility

The work per unit volume to strain the material to $\varepsilon$ is the area under the curve (§11.1B):

$$u = \int_0^{\varepsilon} \sigma\, d\varepsilon \qquad (17)$$

To yield it is the modulus of resilience, $u_Y = \sigma_Y^2/(2E)$ (18). To maximum load it is $u_U$, the same on the engineering and true curves. Ductility after fracture:

$$\%EL = 100\,\frac{L_f - L_0}{L_0} \qquad (19) \qquad\qquad \%RA = 100\left[1 - \left(\frac{d_f}{d_0}\right)^2\right] \qquad (20)$$

%EL depends on $L_0/d_0$, because after necking the extra elongation comes from a neck about one diameter long (Appendix D.6). %RA does not.

### 2.8 The model in the simulation

`lab01_simulation.html` uses the Swift law $\sigma_t = K(\varepsilon_0 + \varepsilon_p)^n$, where $\varepsilon_0 = (\sigma_e/K)^{1/n}$ makes the curve continuous at the elastic limit $\sigma_e$. Its **closed forms** describe a perfect, uniformly deforming bar: at necking $\varepsilon_0 + \varepsilon_p = n$. Its **independent numerical solution** is a virtual specimen: a neck zone of length $\ell$ with area smaller by $\delta_A$, in series with the rest of the bar. The program enforces equilibrium (the same $P$ on every section), volume constancy and compatibility (elongations add; the crosshead adds $C_mP$) step by step, and finds the maximum load by marching, without using Eq. 14.

### 2.9 Uncertainty

Use standard uncertainties $u$; convert a limit $\pm a$ to $u = a/\sqrt{3}$; propagate to first order (Appendix B):

$$\left(\frac{u_\sigma}{\sigma}\right)^2 = \left(\frac{u_P}{P}\right)^2 + \left(\frac{2u_d}{d}\right)^2, \qquad u_d^2 = \frac{s_d^2}{N} + \left(\frac{a_{cal}}{\sqrt{3}}\right)^2 \qquad (21)$$

$$\left(\frac{u_E}{E}\right)^2 = \left(\frac{s_E}{E}\right)^2 + \left(\frac{2u_d}{d}\right)^2 + \left(\frac{u_P}{P}\right)^2 + \left(\frac{u_{ext}}{\delta_{ext}}\right)^2 + \left(\frac{u_{L_e}}{L_e}\right)^2 + \left(\frac{u_{win}}{E}\right)^2 \qquad (22)$$

Here $s_d$ is the standard deviation of $N$ diameter readings, $a_{cal}$ the caliper accuracy and $s_E$ the slope's standard error. The term $u_{win}$ covers the choice of fitting window: fit the two halves (45–112 and 112–180 MPa) separately. If their slopes differ by more than twice their combined standard error, $u_{win} = |E_{low} - E_{high}|/2$; otherwise $u_{win} = 0$. Report $x \pm U$ with $U = 2u$ and draw error bars at $\pm U$. A measurement and a reference **agree** when

$$|x_{meas} - x_{ref}| \le 2\sqrt{u_{meas}^2 + u_{ref}^2} \qquad (23)$$

Any larger discrepancy needs a physical or procedural explanation, quantified where possible.

## 3. Pre-lab (due at the start of the session)

Answer on paper or in a short document. Show every step, units included.

**P1 — Estimate before you measure.** Use the reference values in Table 1 and the nominal diameter $d_0 = 10.00$ mm.
(a) Estimate the load at yield and at maximum for each specimen, and the fraction of the 100 kN machine capacity each represents.
(b) Estimate the elastic elongation of the 50.0 mm gage at yield, and the elongation $\Delta\delta_w$ that occurs across the 45–180 MPa fitting window, for each material. A reading with resolution $r$ carries a rounding error $r/\sqrt{12}$. What is the coarsest resolution that keeps this error below 0.1 % of $\Delta\delta_w$ for steel? Would the crosshead, with 1 µm resolution, meet that criterion even if the machine were rigid?
(c) Estimate the crosshead travel at fracture and the test duration for each specimen at the rates in the procedure. Check that your answers have the right units.

**P2 — True and engineering measures.** (a) Starting from $d\varepsilon_t = dL/L$, derive Eq. 11 and show that $\sigma\,d\varepsilon = \sigma_t\,d\varepsilon_t$. (b) At what engineering strain do $\ln(1+\varepsilon)$ and $\varepsilon$ differ by 1 %?

**P3 — The machine is a spring.** With $C_m = 0.008$ mm/kN, $L_c = 60$ mm and $A_0 = 78.54$ mm², use Eq. 8 to predict $E_{app}$ for steel and for aluminum. Which material's crosshead curve misleads you more, and why? Check both limiting cases of Eq. 8.

**P4 — Considère and imperfections.** For a Hollomon material with $n = 0.20$, find $\varepsilon_{t,U}$ and $\varepsilon_u$. Then use Eq. 16 with $\delta_A = 0.3$ % and $\ell/L_0 = 0.12$ to estimate how much uniform strain an imperfect specimen loses, and by how much its maximum load drops.

**P5 — Predict with the simulation.** Open `lab01_simulation.html`. For each material preset, record from the readout: the numerical $\sigma_Y$, $\sigma_U$, $\varepsilon_u$ and elongation after fracture, and the apparent crosshead modulus. Which material will neck at the smaller strain? Explain using $n$.

**P6 — Alignment and safety.** (a) Compute $\sigma_b/\sigma$ for a misalignment $e = 0.1$ mm on $d_0 = 10.00$ mm. Explain why averaging the strain on two opposite sides of the specimen removes most of this error from $E$. (b) List the two moments in this test when you must keep your hands out of the machine, and why.

| Material | $E$ (GPa) | $\sigma_Y$ typical (MPa) | $\sigma_U$ typical (MPa) | %EL in 5$d_0$ typical |
|---|---:|---:|---:|---:|
| 1018 steel, hot rolled | 205 ± 3 | 250–340 | 400–480 | 25–38 |
| 6061-T6 aluminum | 68.9 ± 1.0 | 255–300 | 290–330 | 8–17 |

: Table 1. Reference values. The modulus uncertainty is a standard uncertainty for alloy-to-alloy and lot-to-lot spread. Strengths depend on processing, so only typical ranges are given.

## 4. Equipment and safety

| Item | Specification used in this handout |
|---|---|
| Universal testing machine | Capacity ≥ 100 kN; load cell accuracy ±0.5 % of reading; crosshead resolution 1 µm |
| Clip-on extensometer | Gage length $L_e$ = 50.0 mm ± 0.5 %; accuracy ±0.5 % of reading; resolution 0.1 µm |
| Digital calipers | Resolution 0.01 mm; accuracy ±0.02 mm |
| Specimens | Round, $d_0$ = 10.00 mm nominal, reduced section $L_c$ = 60 mm, gage marks $L_0$ = 50.0 mm ($5d_0$), threaded or shouldered grip ends |

: Table 2. Equipment. If your machine or specimens differ, record their values and use them throughout.

::: {custom-style="Safety"}
**Safety.** Wear safety glasses with side shields from the moment a specimen is in the grips until both pieces are out. Close the polycarbonate shield before loading; stand to the side, not in line with the specimen. **Pinch points:** keep fingers away from the wedge grips while they close and from the crosshead while it moves; use the jog control at low speed when positioning. **Load limit:** the expected peak load is below 37 kN. Set the machine's overload stop at 50 kN, and stop the test if the load exceeds 45 kN or rises with no visible stretching. **Extensometer:** remove it only after the crosshead is put on *hold*, with the shield open only as long as needed; it must be off before necking because the energy released at fracture can destroy it. **At fracture** the two pieces can whip and fracture surfaces are sharp. Handle them with gloves. Know where the emergency stop is before you start.
:::

## 5. Procedure

1. **Check the machine.** Confirm the load cell range, set the overload stop (50 kN), and zero the load with the upper grip hanging free.
2. **Measure the diameter.** Measure $d_0$ at the top, middle and bottom of the gage section, twice at each location (rotate 90°). Record all six readings in Table 3. **Check:** the readings should span no more than 0.02 mm; a larger spread means a taper, and the smallest section is where the specimen will neck.
3. **Check the gage marks.** Measure the distance between the punch marks, $L_0$, to 0.01 mm.
4. **Mount the specimen.** Clamp it in the upper grip, zero the load, then close the lower grip. **Check:** the load after clamping should be within ±0.3 kN. Grips can squeeze a specimen into compression; if they do, back off and re-clamp.
5. **Attach the extensometer** with its knife edges on the gage marks, remove its setting pin, and zero it.
6. **Set the test.** Crosshead rate 1.0 mm/min; record load, crosshead and extensometer at 5 Hz.
7. **Start the steel test.** **Check at about 10 kN:** the stress divided by the extensometer strain should be within 10 % of the reference $E$. If not, stop and re-seat the extensometer.
8. Watch for the **upper yield point and the load drop**, then the plateau. When the extensometer reads 4.0 % strain, put the crosshead on **hold**, remove the extensometer, close the shield and resume at **5.0 mm/min**.
9. Note the **maximum load** and where the neck forms. Stay clear until **fracture**. Stop the test and save the data as CSV.
10. Remove the pieces, fit them together, and measure $L_f$. Measure $d_f$ at the smallest section in two directions at 90°.
11. **Sketch or photograph both fracture surfaces.** Note the cup-and-cone shape, any shear lip, and the surface texture.
12. Repeat steps 2–11 for the aluminum specimen. Note when the extensometer comes off relative to the maximum load.
13. **In the lab, before you leave:** open the simulation, choose the matching preset, and set the overlay to the sample data or plot your own data. Record in Tables 6a and 6b the predicted $\sigma_Y$, $\sigma_U$, $\varepsilon_u$ and $E_{app}$ next to your raw readings of maximum load and yield.

## 6. Data tables

```{=latex}
\renewcommand{\arraystretch}{2.0}
```

| Reading | Top, 0° | Top, 90° | Middle, 0° | Middle, 90° | Bottom, 0° | Bottom, 90° | Mean | Std. dev. |
|---|---|---|---|---|---|---|---|---|
| Steel $d_0$ (mm) | | | | | | | | |
| Aluminum $d_0$ (mm) | | | | | | | | |

: Table 3. Initial diameter.

| Quantity | Steel | Aluminum |
|---|---|---|
| Gage length $L_0$ (mm) | | |
| Final gage length $L_f$ (mm) | | |
| Final diameter $d_f$, 0° (mm) | | |
| Final diameter $d_f$, 90° (mm) | | |
| Fracture surface description | | |

: Table 4. Gage marks and post-test measurements.

| Quantity | Steel | Aluminum |
|---|---|---|
| Upper yield load (kN) | | — |
| Plateau load (kN) | | — |
| Maximum load (kN) | | |
| Load at fracture (kN) | | |
| Extensometer removed at strain (%) / time (s) | | |
| Where the neck formed (distance from a gage mark, mm) | | |

: Table 5. Test record.

| Quantity | Reference / theory | Simulation (preset) | Measured ± U | Agree (Eq. 23)? |
|---|---|---|---|---|
| $E$ (GPa) | | | | |
| $E_{app}$ from crosshead (GPa) | Eq. 8 | | | |
| $\sigma_Y$ (MPa) | | | | |
| $\sigma_U$ (MPa) | | | | |
| $\varepsilon_u$ | Eq. 15 with your $n$ | | | |
| %EL | | | | |

: Table 6a. Theory vs. simulation vs. measurement: steel.

| Quantity | Reference / theory | Simulation (preset) | Measured ± U | Agree (Eq. 23)? |
|---|---|---|---|---|
| $E$ (GPa) | | | | |
| $E_{app}$ from crosshead (GPa) | Eq. 8 | | | |
| $\sigma_Y$ (MPa) | | | | |
| $\sigma_U$ (MPa) | | | | |
| $\varepsilon_u$ | Eq. 15 with your $n$ | | | |
| %EL | | | | |

: Table 6b. Theory vs. simulation vs. measurement: aluminum.

```{=latex}
\renewcommand{\arraystretch}{1.15}
```

## 7. Analysis

Every answer must (i) show at least two reasoning steps, (ii) include a dimensional check or a limiting-case check, and (iii) end with one to three sentences interpreting the result in words. Questions marked **[Core]** are required of everyone. **[Challenge]** questions are for students who want more. **[Extension]** questions are for honors and independent study.

**A1 [Core] — Curves.** Compute $\sigma$ and the extensometer strain $\varepsilon$ for both specimens and plot the engineering stress–strain curves on one graph, plus a second graph zoomed to $\varepsilon \le 1.5$ %. *Check:* $\sigma = 0$ at $P = 0$, and the elastic slopes differ by about the ratio of the reference moduli. *Interpret:* describe each stage of each curve, using the terms in Figure 3.

**A2 [Core] — Modulus with uncertainty.** Fit $E$ by Eq. 5 in the 45–180 MPa window and report the fitted intercept. Test the window's linearity by fitting its two halves (Sec. 2.9), then combine the slope's standard error, the window term, and the diameter, load-cell and extensometer terms (Eq. 22) to get $u_E$. Report $E \pm U$. Compare with Table 1 using Eq. 23. *Check:* refit with the window raised to 45–260 MPa and explain the change for each material. *Interpret:* which uncertainty term dominates, and what would you buy to reduce it?

**A3 [Core] — Yield strength.** For steel, report the upper and lower yield points. For aluminum, construct the 0.2 % offset (Eq. 6), interpolating between data points, and also apply the offset method to the steel curve. Propagate the uncertainty, including the effect of $u_E$ on the offset intersection (recompute with $E \pm u_E$). *Check:* $\sigma_Y$ must lie above the end of the linear region and below $\sigma_U$. *Interpret:* why is the lower yield point, not the upper, the useful design value?

**A4 [Core] — The machine as a spring.** (a) From the raw crosshead data, find the apparent modulus $E_{app}$ in the same stress window. (b) Fit Eq. 9 for loads above 3 kN on the initial loading branch to obtain $C_m$ and $\Delta_{toe}$, with their standard errors. (c) Predict $E_{app}$ from Eq. 8 with your $E$ and $C_m$, and compare with (a). (d) Apply Eq. 10 and show that the corrected crosshead strain joins the extensometer strain where the extensometer was removed. *Check:* units of $A_0C_m/L_c$; the limit $C_m \to 0$. *Interpret:* why must $E$ never be taken from crosshead travel?

**A5 [Core] — Ultimate strength and uniform elongation.** Report $\sigma_U$ and $\varepsilon_u$ with uncertainties, using the corrected crosshead strain for $\varepsilon_u$. Near a flat maximum, many points lie within the load noise of $P_{max}$. Estimate $u(\varepsilon_u)$ from the range of strain over which $P > P_{max} - 2u_P$. *Check:* for aluminum, was the extensometer still attached at maximum load? *Interpret:* why is $\varepsilon_u$ known much less precisely than $\sigma_U$?

**A6 [Core] — True stress and Considère.** Convert both curves to true stress and true strain up to the maximum load (Eqs. 11–12). Fit the Hollomon law (Eq. 13) on log–log axes over the hardening range (steel: from $\varepsilon_t = 0.03$; aluminum: from $\varepsilon_t = 0.01$) to obtain $K$ and $n$. Compare the Considère prediction $\varepsilon_{t,U} = n$ with your measured $\ln(1+\varepsilon_u)$ using Eq. 23. *Check:* the slope of your true curve at $\varepsilon_{t,U}$ should equal $\sigma_{t,U}$; verify numerically. *Interpret:* if the prediction and the measurement disagree, give two quantified reasons (consider the form of the fit and Eq. 16 with $\delta_A$ estimated from your diameter readings).

**A7 [Core] — Ductility and energy.** Compute %EL and %RA (Eqs. 19–20) with uncertainties, the modulus of resilience (Eq. 18), and $u_U$ (Eq. 17) by the trapezoid rule. Compare %EL with the corrected crosshead strain at fracture and explain the difference. *Check:* show numerically that the areas under the engineering and true curves to maximum load agree. *Interpret:* which material would you choose for a part that must absorb a large overload without breaking, and which number supports the choice?

**A8 [Core] — Theory vs. simulation vs. measurement.** Complete Tables 6a and 6b. Make one figure with error bars at $\pm U$ for $E$, $E_{app}$, $\sigma_U$ and $\varepsilon_u$, normalized by the theory value so that both materials fit on one plot. Explain **every** discrepancy larger than the expanded uncertainty with a named cause, quantified where you can.

**M1 [Core] — Where does the model break?** (a) Compute the true stress at fracture two ways: from the formula $\sigma_f(1+\varepsilon_f)$ with $\varepsilon_f$ from %EL, and from the neck, $P_f/A_f$ with $A_f$ from $d_f$. (b) Which assumption behind Eq. 12 failed, and when? Use the simulation's progress slider and formula cards to find the point in the test at which the two first differ by more than 2 %. (c) Even $P_f/A_f$ overstates the stress the material can carry in uniaxial tension. Explain in two sentences what the neck's curved shape adds to the stress state.

**C1 [Challenge] — Imperfection sensitivity.** Derive Eq. 16, then test it with the simulation: set $\delta_A$ = 0.05 %, 0.1 %, 0.3 %, 1 % and 3 % and plot the drop in uniform true strain against $\delta_A$ on log–log axes. Report the slope and the $\delta_A$ at which Eq. 16 is off by more than 20 %.

**C2 [Challenge] — Monte Carlo uncertainty.** For the aluminum offset yield strength, draw 10 000 random sets of ($d_0$, load calibration, extensometer calibration) from their distributions, recompute $E$ and $\sigma_Y$ for each, and compare the standard deviation with your first-order result from A3.

**C3 [Challenge] — Convergence.** Export the convergence CSV from the simulation. Explain why the error in $\sigma_U$ taken as the largest sample scatters yet stays below a line of slope 2, and show by a one-line argument why integrating the energy up to the largest sample, rather than to a fixed strain, is only first-order accurate.

**X1 [Extension] — The missing length scale.** In the simulation, set the neck length by the mesh and refine $N$ from 5 to 200. Explain why the elongation after fracture never converges, and what physical length a one-dimensional model is missing. Then use the "short gage length" experiment and your data to estimate $c$ in $\%EL \approx 100(\varepsilon_u + c\,d_0/L_0)$, and predict the %EL your steel would show on a $4d_0$ gage.

**X2 [Extension] — Bridgman's correction.** Photograph the neck profile of the steel specimen just before fracture (or from the broken piece), estimate the neck radius of curvature $R$ at the minimum section of radius $a$, and apply $\bar{\sigma} = \dfrac{P/A}{(1 + 2R/a)\ln(1 + a/2R)}$ to correct the fracture stress from M1. Discuss how sensitive the correction is to your estimate of $R$.

**X3 [Extension] — The Lüders band.** From the steel plateau, estimate the Lüders strain $\varepsilon_L$ and the speed at which the band front travels along the gage (hint: the crosshead feeds length into the specimen only where the band passes). Explain why a smooth hardening law such as Eq. 13 cannot produce a plateau, and how the simulation's steel preset differs from your data because of it.

## 8. Design problem

**D1 — Size a tie rod.** A tie rod 1.80 m long hangs a walkway segment. It carries a service tension of 12.0 kN and an occasional overload of 18.0 kN. Its ends are threaded; the tensile stress area of the thread is 0.78 times the gross area of the rod. Bar stock is available in whole-millimeter diameters. Requirements:

* factor of safety against yield of at least 2.0 at the service load, at the threaded section, using a **conservative** yield strength taken from **your** measurement ($\sigma_Y - U$);
* no yielding at the overload;
* elastic elongation of the rod at the service load no more than 1.20 mm.

Choose a material (either one you tested) and a diameter. Material data: density 7870 kg/m³ for steel and 2700 kg/m³ for aluminum; bar stock costs about \$2.20/kg for steel and \$6.50/kg for aluminum. More than one design is acceptable. Justify yours with a quantitative trade-off (mass, cost, stiffness margin, or another criterion you define). Submit at most one page: a requirements table, the governing calculation for each requirement, the chosen design with every requirement checked, and one assumption that could invalidate your design, with how you would check it.

| Criterion | Weight |
|---|---:|
| Requirements identified and translated into equations, units correct | 20 % |
| Conservative strength from **your** data with its uncertainty; correct calculations | 30 % |
| Every requirement checked for the final design (stress area for strength, gross area for stretch) | 20 % |
| Choice justified by a quantitative comparison of at least two alternatives | 20 % |
| Clear one-page presentation; one critical assumption named and a check proposed | 10 % |

: Table 7. How D1 will be graded.

## 9. Report

Write a technical report of at most eight pages plus appendices, one per team. Include the pre-lab, Tables 3–6b, all plots with labeled axes and units, every Core answer, M1 and D1. Challenge and Extension answers go in a clearly marked section. State every number as value ± $U$ with units, rounded per the style rules (uncertainty to one or two significant figures, value to the same decimal place). Put your analysis code or spreadsheet in an appendix.

| Part | Points |
|---|---:|
| Pre-lab P1–P6 | 15 |
| Data quality and procedure (Tables 3–5, checks performed) | 10 |
| Core analysis A1–A8 | 45 |
| M1 — Where does the model break? | 10 |
| D1 — Design problem | 15 |
| Communication: figures, units, uncertainty format | 5 |
| **Total** | **100** |
| Challenge (C1–C3) | up to +10 |

: Table 8. Report grading. Extension questions are graded separately for honors and independent-study credit.

::: pagebreak
:::

## Appendix A — Running the lab without equipment

If the machine is unavailable, use `sample_data.csv`. It holds one row per sample at 5 Hz for both specimens:

| Column | Meaning |
|---|---|
| `specimen` | `steel_1018HR` or `al_6061T6` |
| `time_s` | time from the start of the test (s) |
| `load_N` | load (N), resolution 1 N |
| `crosshead_mm` | crosshead travel from the start (mm), resolution 0.001 mm |
| `extensometer_mm` | extensometer elongation over $L_e$ = 50.0 mm (mm), resolution 0.0001 mm; blank after removal at 4.0 % strain |

: Table A1. Columns of `sample_data.csv`.

The tests ran at 1.0 mm/min until the extensometer was removed (steel at about 161 s, aluminum at about 159 s), then at 5.0 mm/min until fracture. Use these measurements:

| Quantity | Steel | Aluminum |
|---|---|---|
| $d_0$ readings (mm): top 0°, top 90°, middle 0°, middle 90°, bottom 0°, bottom 90° | 10.00, 10.01, 10.00, 10.01, 10.00, 10.01 | 10.00, 9.99, 10.00, 9.99, 10.00, 9.99 |
| $L_0$ (mm) | 50.01 | 49.99 |
| $L_f$ (mm) | 66.95 | 56.18 |
| $d_f$ readings (mm): 0°, 90° | 6.33, 6.33 | 7.60, 7.61 |
| Fracture surface | cup-and-cone, fibrous center, shear lip all around | cup-and-cone with a smaller, flatter cup; finer texture |

: Table A2. Specimen measurements for the sample data.

## Appendix B — Uncertainty quick reference

* Limit $\pm a$ (calibration, accuracy): $u = a/\sqrt{3}$. Reading resolution $r$: $u = r/\sqrt{12}$ (already included when you use the scatter of repeated readings).
* Sum or difference: $u_{x \pm y}^2 = u_x^2 + u_y^2$. Product or quotient: $(u_{xy}/xy)^2 = (u_x/x)^2 + (u_y/y)^2$. Power: $u_{x^k}/x^k = |k|\,u_x/x$.
* Mean of $N$ readings: $u = s/\sqrt{N}$ for the scatter, combined with any calibration term.
* *Example.* Six diameter readings with $s_d = 0.0055$ mm and caliper accuracy ±0.02 mm: $u_d = \sqrt{0.0055^2/6 + 0.02^2/3} = 0.012$ mm, so $u_A/A = 2(0.012)/10.00 = 0.24$ %.
* Report $x \pm U$ with $U = 2u$. Round $U$ to one or two significant figures, and $x$ to the same decimal place.

## Appendix C — Using the simulation

Open `lab01_simulation.html` in any browser; it needs no internet connection. Choose a material preset, then move the sliders. The **readout table** compares each closed-form (textbook) result with the independent numerical solution and says why they differ. The **progress slider** steps through the test; the formula cards report whether each textbook formula still applies at that point. **Push the model past its assumptions** runs prepared experiments. **Export (CSV)** saves the curve, the readout or the convergence study. If your browser blocks the download, the data appears in a box you can copy. The **SI / US customary** toggle converts every input and output.

## Appendix D — Derivations

**D.1 Equilibrium of a cut, and misalignment.** On the cut a–a (Figure 2b) each area element $dA$ carries $\sigma\,dA$. Axial equilibrium of the lower piece gives Eq. 1. Equilibrium fixes only the resultant; if $\sigma$ is uniform it leaves the integral and $\sigma A_0 = P$ (Eq. 2). If the load line is offset by $e$ from the centroid, the cut must also resist a moment $M = Pe$. For a solid circle, $I = \pi d^4/64$ and $c = d/2$, so the bending stress at the surface is $Mc/I = 32Pe/(\pi d^3)$ (bending is derived in Lab 4). Dividing by $P/A_0 = 4P/(\pi d^2)$ gives $\sigma_b/\sigma = 8e/d$. The bending strain is $+\varepsilon_b$ on one side and $-\varepsilon_b$ on the opposite side, so averaging two opposite readings removes it to first order.

**D.2 Springs in series (Eqs. 7–10).** The reduced section (length $L_c$, area $A_0$) stretches $PL_c/(EA_0)$ while it is elastic. Every other part of the load path carries the same $P$ (equilibrium along the load train) and stretches in proportion to $P$; their sum is $C_mP$. Grip seating adds a slack $\Delta_{toe}$ that is taken up at low load. Lengths add (compatibility), giving Eq. 7. Divide by $L_c$ and substitute $P = \sigma A_0$: $\Delta/L_c = \sigma\,[1/E + A_0C_m/L_c] + \Delta_{toe}/L_c$. The slope is $E_{app}$ of Eq. 8. Units: mm² × (mm/kN) / mm = mm²/kN = 1/(kN/mm²) = 1/GPa. Limits: $C_m \to 0$ gives $E_{app} \to E$; $E \to \infty$ gives $E_{app} \to L_c/(A_0C_m)$, the machine alone. While deformation is uniform, the reduced section stretches $(L_c/L_e)\,\delta_{ext}$; subtracting that from Eq. 7 gives Eq. 9, and solving Eq. 7 for the specimen's stretch gives Eq. 10.

**D.3 True strain and true stress (Eqs. 11–12).** An increment of stretch measured against the current length is $d\varepsilon_t = dL/L$. Integrating from $L_0$ to $L$ gives $\varepsilon_t = \ln(L/L_0) = \ln(1+\varepsilon)$. Plastic flow conserves volume, $AL = A_0L_0$, so $A = A_0/(1+\varepsilon)$ and $\sigma_t = P/A = \sigma(1+\varepsilon)$. Elastic strain changes volume by $(1-2\nu)\varepsilon_e \approx 0.4 \times 0.0015 = 0.0006$ for steel at yield. The series $\ln(1+\varepsilon) = \varepsilon - \varepsilon^2/2 + \dots$ shows a relative difference of about $\varepsilon/2$. Since $d\varepsilon = (1+\varepsilon)\,d\varepsilon_t$, we get $\sigma\,d\varepsilon = \sigma(1+\varepsilon)\,d\varepsilon_t = \sigma_t\,d\varepsilon_t$.

**D.4 Considère's criterion (Eqs. 14–15).** $P = \sigma_t A$, so $dP = A\,d\sigma_t + \sigma_t\,dA$. Volume constancy gives $dA/A = -dL/L = -d\varepsilon_t$, hence $dP = A\,(d\sigma_t - \sigma_t\,d\varepsilon_t)$. The load is stationary ($dP = 0$) when $d\sigma_t/d\varepsilon_t = \sigma_t$. Beyond that point $dP < 0$: a section that strains a little more needs less load, so it keeps straining while its neighbors unload, and deformation localizes. For $\sigma_t = K\varepsilon_t^{\,n}$, $nK\varepsilon_t^{\,n-1} = K\varepsilon_t^{\,n}$ gives $\varepsilon_{t,U} = n$. Then $\sigma_U = \sigma_{t,U}/(1+\varepsilon_u) = Kn^n/e^{n}$.

**D.5 Imperfection sensitivity (Eq. 16).** For the Hollomon law, $\ln P = \ln(K A_0) + n\ln\varepsilon_t - \varepsilon_t$. Its second derivative is $-n/\varepsilon_t^2 = -1/n$ at the peak $\varepsilon_t = n$, so near the peak $P \approx P_{max}[1 - (\varepsilon_t - n)^2/(2n)]$. The weak section (area smaller by $\delta_A$) has the same curve scaled by $(1 - \delta_A)$, so it peaks first, at load $(1-\delta_A)P_{max}$; after that the load falls. The rest of the gage carries the same load (equilibrium), so it stops stretching at the strain where its own capacity equals $(1-\delta_A)P_{max}$: $(\varepsilon_t - n)^2/(2n) = \delta_A$, or $n - \varepsilon_t = \sqrt{2n\delta_A}$. The neck (length $\ell$) is at $\varepsilon_t = n$, and the remaining $L_0 - \ell$ falls short by $\sqrt{2n\delta_A}$. The length-weighted average gives Eq. 16. The quadratic expansion requires the shortfall to be small compared with $n$, i.e. $\delta_A \ll n/2$.

**D.6 Gage-length dependence of %EL.** Up to the maximum load the whole gage stretches uniformly by $\varepsilon_u L_0$. After it, extra stretch occurs only in a neck whose length scales with $d_0$, adding $c\,d_0$ with $c$ a material constant. So $L_f - L_0 \approx \varepsilon_u L_0 + c\,d_0$, and $\%EL \approx 100(\varepsilon_u + c\,d_0/L_0)$. This is why standards fix $L_0/d_0$, and why the simulation's one-dimensional model, which has no length scale for the neck, cannot predict %EL unless the neck length is supplied (Challenge X1).

**D.7 Least squares and its standard error (Eq. 5).** Minimizing $\sum(\sigma_i - a - E\varepsilon_i)^2$ over $a$ and $E$ gives Eq. 5. The slope's standard error is $s_E = s\,/\sqrt{\sum(\varepsilon_i - \bar\varepsilon)^2}$, where $s^2 = \sum(\sigma_i - a - E\varepsilon_i)^2/(N-2)$. Spreadsheet functions (LINEST, SLOPE with STEYX) report both.


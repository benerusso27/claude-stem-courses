# Lab 4 — Bending: Shear and Moment Diagrams, the Flexure Formula, Composite and Plastic Beams

| | |
|---|---|
| **Course** | ENGR 2228 Mechanics of Materials |
| **When** | Week 8, after lectures on Beer 8e Ch. 4 and §5.1–5.3 |
| **Textbook** | Beer, Johnston, DeWolf, Mazurek, *Mechanics of Materials*, 8th ed. (Beer 8e): §4.1A–4.1B, §4.2, §4.3, §4.4, §4.6A–4.6C, §5.1, §5.2, §5.3 |
| **Session** | 2 hours in the lab, teams of two; report due one week later |
| **Equipment** | Universal testing machine (capacity ≥ 50 kN) with a four-point bending fixture, 12-channel strain-gage amplifier, calipers, height gage, 1 m straightedge and feeler gages; a 6061-T6 aluminum bar 25.4 × 50.8 mm with ten strain gages, and a second bar with a 6.35 mm 1018 steel strip bonded to its bottom face, with eight gages |
| **Files** | `lab04_simulation.html` (open in any browser, works offline), `sample_data.csv` |

## 1. Learning objectives

After this lab you will be able to:

1. Draw shear and bending-moment diagrams from free bodies and from the load–shear–moment relations, using Beer's sign convention, and measure the moment and shear in a real beam with strain gages (§5.1–5.2).
2. Derive the flexure formula from compatibility (plane sections remain plane), Hooke's law and equilibrium, test each step against a measured strain profile, and measure $E$ and $\nu$ in bending (§4.1–4.3).
3. Locate the neutral axis of a beam made of two materials with the transformed section, and check the prediction against measured strains (§4.4).
4. Predict the moment–curvature curve, permanent curvature and residual stresses of a beam loaded past first yield, and show by how much the flexure formula overstates the stress there (§4.6A–4.6C).
5. Select a beam from a catalog against strength and deflection requirements, using your own measured properties (§5.3).

## 2. Theory

The beam rests on two supports 600 mm apart, and the testing machine pushes a spreader beam that applies $P/2$ at each of two load points 200 mm from the supports (Figure 1). Between the load points the beam carries a constant moment and no shear: it is in **pure bending**. Strain gages up the side face at midspan measure how the strain varies through the depth; gages on the bottom face in the left outer span measure how the moment varies along the beam.

![Figure 1. Four-point bending set-up (schematic, not to scale). Midspan gages: five on the side face, one on the top face, one on the bottom face and one transverse gage on the top face. Two bottom gages at x = 100 and 150 mm sample the left outer span.](figures/fig1_setup.png){width=6.4in}

::: {custom-style="Callout"}
**Sign convention (Beer 8e).** Shear $V$ and bending moment $M$ follow Fig. 5.6 of the text: on the **left** part of a cut beam, $V$ acts **downward** on the cut face and $M$ acts **counterclockwise** (on the right part both are reversed). A positive $M$ bends the beam concave upward (sagging), with the bottom in tension. A distributed load $w$ is positive downward, so $dV/dx = -w$ and $dM/dx = V$. The coordinate $y$ is measured **upward from the neutral axis**, so the normal stress is $\sigma_x = -My/I$; tension is positive. The curvature $\kappa = 1/\rho$ is positive for sagging. Gage locations are given as heights $y_h$ above the **bottom** of the section; convert with $y = y_h - y_{NA}$.
:::

::: {custom-style="Callout"}
**Nomenclature.** $P$ total load on the spreader; $L$ span; $a$ distance from a support to the nearer load point (shear span); $x$ position from the left support; $V$ shear; $M$ bending moment; $w$ distributed load; $b$ width; $h$ depth; $c = h/2$; $I$ moment of inertia about the neutral axis; $S = I/c$ elastic section modulus; $Z$ plastic section modulus; $\rho$ radius of curvature; $\kappa = 1/\rho$ curvature; $y$ distance above the neutral axis; $y_h$ height above the bottom; $y_{NA}$ height of the neutral axis; $\varepsilon_x$, $\sigma_x$ longitudinal strain and stress; $\varepsilon_z$ transverse strain; $E$ modulus of elasticity; $\nu$ Poisson's ratio; $\rho'$ radius of the anticlastic curvature; $E_1$, $E_2$ moduli of the two materials in a composite beam; $n = E_2/E_1$; $t_s$ strip thickness; $H = h + t_s$; $\bar y$ centroid height of the transformed section; $I_t$ its moment of inertia; $\sigma_Y$ yield strength; $M_Y$, $\kappa_Y$ moment and curvature at first yield; $y_Y$ half-thickness of the elastic core; $M_p$ fully plastic moment; $k = M_p/M_Y$ shape factor; $\kappa_p$ permanent curvature; $\sigma_{res}$ residual stress; $u$ standard uncertainty; $U = 2u$ expanded uncertainty.
:::

Full derivations are in **Appendix D**; this section states each result, what it means, and when it stops applying.

### 2.1 Shear and bending-moment diagrams

Cut the beam at $x$ and write equilibrium of either part: the internal $V$ and $M$ balance everything on that side (§5.1). Doing the same for a short slice of length $dx$ gives the load–shear–moment relations (§5.2):

$$\frac{dV}{dx} = -w, \qquad \frac{dM}{dx} = V \qquad (1)$$

so the moment diagram's slope is the shear, and the change in $M$ between two points is the area under the shear diagram. A concentrated load makes $V$ jump by the load; a concentrated couple makes $M$ jump. For the four-point set-up with load points at $a$ and $L - a$ the reactions are $P/2$, and

$$M = \frac{P}{2}\,x \ \ (0 \le x \le a), \qquad M = \frac{P}{2}\,a \ \ (a \le x \le L - a) \qquad (2)$$

with $V = P/2$ in the left shear span, $V = 0$ between the load points, and $V = -P/2$ in the right shear span (Figure 2).

![Figure 2. (a) Positive shear and moment in Beer's convention, on the left part of the beam. (b) Shear and (c) bending moment for four-point bending with a = L/3; the shaded region carries a constant moment with no shear.](figures/fig2_vm.png){width=6.4in}

*Worked example.* A 2.4 m simply supported beam carries 6 kN at 0.8 m from each support. Each reaction is 6 kN, $V$ = 6 kN in the left third, and $M$ rises at 6 kN·m per meter to 4.8 kN·m at $x$ = 0.8 m, where it stays until the second load.

### 2.2 Stresses and deformations in the elastic range

![Figure 3. (a) Strain varies linearly through the depth and vanishes at the neutral axis. (b) In the elastic range the stress is linear too; its resultant force is zero and its moment is M. (c) A stiffer strip at the bottom: the strain stays continuous and linear, but the stress jumps by the factor n at the interface and the neutral axis moves toward the strip.](figures/fig3_flexure.png){width=6.4in}

**Compatibility.** A symmetric member in pure bending deforms symmetrically, so plane cross-sections stay plane and rotate about a line in the section, the **neutral axis** (§4.1B). The longitudinal strain is then linear in $y$, whatever the material:

$$\varepsilon_x = -\frac{y}{\rho} = -\kappa\,y \qquad (3)$$

**Equilibrium.** In pure bending the stresses on a cut carry no net force and a moment equal to $M$ (§4.1A):

$$\int_A \sigma_x\,dA = 0, \qquad -\int_A y\,\sigma_x\,dA = M \qquad (4)$$

**Hooke's law** $\sigma_x = E\varepsilon_x$ makes the stress linear too. The first of Eqs. 4 then puts the neutral axis through the centroid, and the second gives (§4.2)

$$\kappa = \frac{1}{\rho} = \frac{M}{EI} \qquad (5)$$

$$\sigma_x = -\frac{My}{I}, \qquad \sigma_m = \frac{Mc}{I} = \frac{M}{S} \qquad (6)$$

$$I = \frac{bh^3}{12}, \qquad S = \frac{bh^2}{6} \quad \text{(rectangle)} \qquad (7)$$

*Worked example.* A steel bar 40 mm wide and 80 mm deep ($E$ = 205 GPa) carries $M$ = 3.0 kN·m. Then $I$ = 1.707 × 10⁶ mm⁴, $\sigma_m$ = 70.3 MPa (compression on top), and $\kappa$ = 0.00857 m⁻¹, a radius of 117 m.

*When Eqs. 5–7 apply:* linear elastic, homogeneous material; a section symmetric about the plane of loading; and points at least about one depth away from load points and supports (Saint-Venant). In the shear spans $V \ne 0$ adds shear stresses (Lab 5), but for a slender beam they change $\sigma_x$ by much less than 1 %.

**Anticlastic curvature.** Poisson's effect acts across the width too: the compressed top widens and the stretched bottom narrows (Figure 4a). The transverse strain is (§4.3)

$$\varepsilon_z = -\nu\,\varepsilon_x, \qquad \rho' = \frac{\rho}{\nu} \qquad (8)$$

so the cross-section curves the other way, with radius $\rho'$. A transverse gage on the top face measures $\nu$ directly.

![Figure 4. (a) Anticlastic curvature: the compressed top widens and the stretched bottom narrows, so the section curves with radius ρ/ν. (b) Fully plastic stress blocks: the shape factor is 1.5 for a rectangle and about 1.1–1.2 for an I-section.](figures/fig4_details.png){width=6.0in}

### 2.3 Beams made of two materials

Compatibility does not care what the beam is made of, so Eq. 3 still holds across the interface; the stress is $E_1\varepsilon_x$ in one material and $E_2\varepsilon_x$ in the other. The **transformed section** (§4.4) replaces material 2 with material 1 by multiplying its width by

$$n = \frac{E_2}{E_1} \qquad (9)$$

The neutral axis passes through the centroid $\bar y$ of the transformed section, whose moment of inertia about that axis is $I_t$, and

$$\sigma_1 = -\frac{My}{I_t}, \qquad \sigma_2 = -\frac{nMy}{I_t} \qquad (10)$$

For the steel strip on aluminum, $n \approx 3$: the strip pulls the neutral axis toward itself and roughly doubles the bending stiffness (Figure 3c).

*When Eqs. 9–10 apply:* both materials elastic; a perfect bond (no slip at the interface); each layer's width uniform.

### 2.4 Plastic bending

![Figure 5. Plastic bending of a rectangle (normalized, elastic–perfectly plastic). (a) Plastic zones at ±σ_Y grow inward as the curvature increases. (b) Moment–curvature: the curve approaches 1.5 M_Y; unloading follows the elastic slope and leaves a permanent curvature. (c) Residual stress after unloading from 3κ_Y.](figures/fig5_plastic.png){width=6.4in}

Equation 3 still holds after yield, so the strain stays linear while the stress follows the material's curve. For an **elastic–perfectly plastic** (EPP) material, yield starts at the extreme fibers when (§4.6A)

$$M_Y = \sigma_Y S, \qquad \kappa_Y = \frac{\sigma_Y}{Ec} \qquad (11)$$

At larger curvature an elastic core of half-thickness $y_Y = c\,\kappa_Y/\kappa$ is sandwiched between plastic zones at $\pm\sigma_Y$ (Figure 5a), and Eqs. 4 give, for a rectangle,

$$M = \frac{3}{2}M_Y\left[1 - \frac{1}{3}\left(\frac{\kappa_Y}{\kappa}\right)^2\right], \qquad \kappa \ge \kappa_Y \qquad (12)$$

which approaches the **fully plastic moment**

$$M_p = \sigma_Y Z, \qquad Z = \frac{bh^2}{4} \ \text{(rectangle)}, \qquad k = \frac{M_p}{M_Y} = \frac{Z}{S} \qquad (13)$$

For any section, the plastic neutral axis divides the area into two equal halves, and $Z$ is the sum of the first moments of the two halves about it (§4.6B). The **shape factor** $k$ is 1.5 for a rectangle but only about 1.1–1.2 for an I-section, whose material is already concentrated far from the neutral axis (Figure 4b).

**Unloading and residual stresses.** Unloading is elastic, so it subtracts the elastic solution for the moment removed (§4.6C). After loading to $(\kappa_{max}, M_{max})$ and releasing,

$$\sigma_{res}(y) = \sigma(y) + \frac{M_{max}\,y}{I}, \qquad \kappa_p = \kappa_{max} - \frac{M_{max}}{EI} \qquad (14)$$

The residual stresses carry no net force or moment: the extreme fibers on the compression side are left in tension, and those on the tension side in compression (Figure 5c).

*When Eqs. 11–14 apply:* the material has a flat yield plateau. 6061-T6 does not: it yields gradually and keeps hardening, so Eq. 12 is only an approximation for it. Beyond yield, Eq. 6 is no longer the stress; the value $M_{max}c/I$ (the "flexure stress") overstates the real extreme-fiber stress.

### 2.5 What the gages measure

Each gage reads the longitudinal strain at its height. Fitting a straight line through the seven gages at midspan (five on the side, top and bottom),

$$\varepsilon_x = A_0 + A_1 y_h \quad \Rightarrow \quad \kappa = -A_1, \qquad y_{NA} = -\frac{A_0}{A_1} \qquad (15)$$

tests compatibility (are the residuals at the level of the gage noise?) and measures the curvature and the neutral axis without assuming the material is elastic. In the elastic range a bottom-face gage at position $x$ also measures the moment there, and two of them measure the shear between them (Eq. 1):

$$M(x) = E\,S\,\varepsilon_{bottom}(x), \qquad V \approx \frac{M(x_2) - M(x_1)}{x_2 - x_1} \qquad (16)$$

### 2.6 The model in the simulation

`lab04_simulation.html` has two configurations. **Beam & diagrams** builds $V$ and $M$ from statics for point loads, uniform and triangular loads on a simply supported, overhanging or cantilever beam, and compares them with an **independent numerical solution** that integrates Eqs. 1 step by step from one end, finding the unknown reaction by shooting. **Section & stress** takes a curvature and evaluates Eqs. 6, 10 and 12 in closed form, and compares them with a **strip summation** that slices the section into $N_s$ strips, applies Eq. 3 and the chosen stress–strain law to each, finds the neutral axis from the first of Eqs. 4 by bisection, and adds up the moment. It never uses Eqs. 6–14. The law can be EPP (to check the formulas) or the material's own curve from Lab 1 (to see where the formulas fail).

### 2.7 Uncertainty

Use standard uncertainties $u$; convert a limit $\pm a$ to $u = a/\sqrt{3}$; propagate to first order (Appendix B). In Part A you will fit $M = (P/2)a$ against the measured $\kappa$; the slope is $EI$, so $E = \text{slope}/I$ with $I = bh^3/12$:

$$\left(\frac{u_E}{E}\right)^2 = \left(\frac{s_k}{k}\right)^2 + \left(\frac{u_b}{b}\right)^2 + \left(\frac{3u_h}{h}\right)^2 + \left(\frac{u_a}{a}\right)^2 + \left(\frac{u_P}{P}\right)^2 + u_{GF}^2 \qquad (17)$$

where $k$ is the fitted slope with standard error $s_k$ and $u_{GF}$ is the relative uncertainty of the gage factor (every strain, and so $\kappa$, scales with it). Report $x \pm U$ with $U = 2u$ and draw error bars at $\pm U$. A measurement and a reference **agree** when

$$|x_{meas} - x_{ref}| \le 2\sqrt{u_{meas}^2 + u_{ref}^2} \qquad (18)$$

Any larger discrepancy needs a physical or procedural explanation, quantified where possible.

## 3. Pre-lab (due at the start of the session)

Answer on paper or in a short document. Show every step, units included. Use Table 1 and the nominal section $b$ = 25.4 mm, $h$ = 50.8 mm, span $L$ = 600 mm, $a$ = 200 mm.

**P1 — Estimate before you measure.** (a) For the aluminum bar find $I$ and $S$, and at $P$ = 20 kN the midspan moment, the extreme-fiber stress and strain, and the curvature and its radius. (b) At what load $P_Y$ does the bar first yield, and at what load would it become fully plastic (EPP model)? How far past $P_Y$ does Part C's 40 kN go? (c) The amplifier resolves 1 µε. What fraction of the bottom strain at the first load step (2.5 kN) is that? (d) In the shear spans $V = P/2$. Estimate the average shear stress $V/(bh)$ at 20 kN and compare it with the bending stress from (a). Check the units of every answer.

**P2 — Diagrams.** (a) Draw $V$ and $M$ for the four-point set-up from free bodies, then confirm them with Eqs. 1: integrate $V$ from $x = 0$ and show that $M$ returns to zero at $x = L$. (b) The load points are measured to ±0.5 mm. Suppose they are actually at $a_1$ = 200.4 mm and $a_2$ = 399.6 mm from the left support. Find the reactions and the midspan moment, and the percentage change from Eq. 2. (c) Repeat with only the second point off ($a_1$ = 200.0 mm, $a_2$ = 399.6 mm). Is the middle region still in pure bending? Give the shear there as a fraction of $P$.

**P3 — Composite section.** For the Part B section (aluminum bar on a 6.35 mm steel strip, $E_2/E_1$ from Table 1), find $n$, $\bar y$ above the bottom of the strip, and $I_t$. At $P$ = 15 kN find the stress at the bottom of the steel, on each side of the interface, and at the top of the aluminum. (b) Check two limits: $t_s \to 0$ and $n = 1$.

**P4 — Beyond yield.** Treat the aluminum as EPP with $\sigma_Y$ from Table 1. (a) Find $M_Y$, $\kappa_Y$ and $M_p$. (b) At $P$ = 40 kN, invert Eq. 12 to find $\kappa$ and the half-thickness of the elastic core. (c) Find the permanent curvature after unloading (Eq. 14) and the residual stress at the top and bottom surfaces. (d) Check that the residual stresses carry no net moment.

**P5 — Predict with the simulation.** Open `lab04_simulation.html`. For the preset "Lab Part A", record $M$ at midspan and the extreme-fiber stress. Switch to "Lab Part B" and record the neutral-axis height and $I_t$. For "Lab Part C", record the moment at $\kappa$ = 0.292 m⁻¹ with the material's own curve and with **Elastic–perfectly plastic**: which is larger, and why? Run "Overload, then unload" and record the permanent curvature.

**P6 — Safety.** (a) List the hazards in this lab and how the procedure controls each. (b) Why is Part C run last, and why must the overload stop be set before it starts?

| Material | $E$ (GPa) | $\nu$ | $\sigma_Y$ (MPa) |
|---|---:|---:|---:|
| 6061-T6 aluminum | 68.46 ± 0.47 (your Lab 2) | 0.330 ± 0.003 (your Lab 2) | 273.7 ± 1.0 (0.2 % offset, your Lab 1) |
| 1018 steel, hot rolled | 205 ± 3 | 0.29 ± 0.01 | 296.2 ± 1.1 (lower yield point, your Lab 1) |

: Table 1. Reference values. The ± values are standard uncertainties. Replace them with your own team's results where you have them.

## 4. Equipment and safety

| Item | Specification used in this handout |
|---|---|
| Testing machine | Capacity ≥ 50 kN; load accuracy ±0.5 % of reading |
| Four-point fixture | Rollers 600 mm apart; spreader with load rollers 200 mm apart, centered; roller diameter 25 mm |
| Strain gages and amplifier | 120 Ω foil gages, 3 mm grid, gage factor ±1 %; resolution 1 µε |
| Calipers / height gage | Accuracy ±0.02 mm / ±0.05 mm |
| Straightedge / feeler gages | 1 m, flat to 0.02 mm / 0.05 mm steps |
| Bar A (Parts A and C) | 6061-T6, 25.4 × 50.8 × 700 mm; five side gages at about 5, 15, 25, 35 and 45 mm above the bottom at midspan; top, bottom and top-transverse gages at midspan; bottom gages at $x$ = 100 and 150 mm |
| Bar B (Part B) | The same bar with a 1018 steel strip, 25.4 × 6.35 mm, bonded to its bottom face; five side gages at about 10, 20, 30, 40 and 50 mm above the bottom of the strip; top, bottom and top-transverse gages at midspan |

: Table 2. Equipment. If your equipment differs, record its values and use them throughout.

::: {custom-style="Safety"}
**Safety.** Wear safety glasses while any load is on the fixture. **Load limits:** set the machine's overload stop before each part, at 22 kN for Part A, 17 kN for Part B and 42 kN for Part C; do not exceed 20, 15 and 40 kN. **Pinch points:** keep fingers out from between the rollers and the bar and from under the spreader whenever the crosshead can move; jog the crosshead only with both hands on the controller. **Stored energy:** a beam that rolls off a support or a spreader that tips can release the load suddenly; check that the bar is centered and square on both supports before every part, and stop at once if the load drops or the bar shifts. **Part C** bends the bar permanently; it is run last so that Parts A and B use an undamaged bar, and it is never run past 40 kN, close to the fully plastic load. The bars weigh about 2.5 kg; lift them with two hands and keep feet clear.
:::

## 5. Procedure

1. **Measure the section.** Measure $b$ and $h$ of bar A at three places along the middle 200 mm with the calipers, and $t_s$ of bar B's strip. Measure the height of every side gage's center above the bottom of its bar with the height gage. Record everything in Table 3. **Check:** the three readings of each dimension should span no more than 0.03 mm.
2. **Set the fixture.** Set the supports 600.0 mm apart and center the spreader. Measure the distance from the left support to each load roller. **Check:** both should be within 0.5 mm of 200 and 400 mm.
3. **Connect and zero the gages.** Place bar A on the supports with the side gages facing you, connect the ten channels and zero them with no load on the spreader. Shunt-calibrate one channel. **Check:** the shunt reading is within 1 % of its nominal value.
4. **Part A — elastic bending.** Preload to 1 kN, unload and re-zero. Load in 2.5 kN steps to 20 kN at about 2 kN/s, holding 10 s at each step before recording all channels; then unload in 5 kN steps to zero. **Check at 5 kN:** the top and bottom strains should be equal and opposite within 3 %, and close to your P1 estimate; if not, check the bar's seating and the gage connections.
5. **Part B — composite bar.** Replace bar A with bar B, steel strip down, and repeat steps 3–4 to 15 kN. **Check at 5 kN:** the top strain should be larger in size than the bottom strain. Why?
6. **Part C — beyond yield.** Replace bar A, re-zero, and load in 5 kN steps to 25 kN, then in 3 kN steps to 40 kN, recording at each step. Unload in 10 kN steps to zero and record the strains at zero load. **Check:** above about 28 kN the top and bottom strains should start to grow faster than the load.
7. **Measure the permanent set.** Lay the straightedge along the top face of bar A, resting on its two ends, and measure the gap at midspan with feeler gages.
8. **Before you leave:** open the simulation, enter your measured dimensions in each Lab preset, and record its predictions in Table 5 next to your raw readings.

## 6. Data tables

```{=latex}
\renewcommand{\arraystretch}{1.9}
```

| Quantity | Readings | Mean |
|----------------------------------|------------------------------------------------|----------|
| Bar A width $b$ (mm) | | |
| Bar A depth $h$ (mm) | | |
| Bar B strip thickness $t_s$ (mm) | | |
| Load rollers from left support (mm) | | — |
| Bar A side gages $y_h$ (mm) | | — |
| Bar B side gages $y_h$ (mm) | | — |

: Table 3. Dimensions and gage heights.

| $P$ (kN) | S1 | S2 | S3 | S4 | S5 | Top | Bot. | Tr. | B100 | B150 |
|--------------|------|------|------|------|------|------|------|------|------|------|
| 5 | | | | | | | | | | |
| 10 | | | | | | | | | | |
| 20 | | | | | | | | | | |
| 15, Part B | | | | | | | | | — | — |
| 40, Part C | | | | | | | | | | |
| 0 after Part C | | | | | | | | | | |

: Table 4. Spot readings (µε) for the checks in the procedure; the data system records every step. S1–S5: side gages from the lowest; Tr.: top transverse; B100, B150: bottom gages at $x$ = 100 and 150 mm.

| Quantity | Theory (equation) | Simulation | Measured ± U | Agree (Eq. 18)? |
|----------------------------------------|------------|------------|--------------|-----------|
| Shear $V/P$ in the left shear span | Eq. 2 | | | |
| Neutral axis, bar A (mm above bottom) | $h/2$ | | | |
| $E$ of 6061-T6 (GPa) | Lab 2 | — | | |
| $\nu$ of 6061-T6 | Lab 2 | — | | |
| Neutral axis, bar B (mm above bottom) | Eq. 9 | | | |
| $EI$, bar B (N·m²) | Eq. 10 | | | |
| Moment at 40 kN, measured $\kappa$ (N·m) | Eq. 12 | | | |
| Permanent curvature (m⁻¹) | Eq. 14 | | | |
| Straightedge gap after Part C (mm) | App. D.9 | — | | |

: Table 5. Theory vs. simulation vs. measurement.

```{=latex}
\renewcommand{\arraystretch}{1.15}
```

## 7. Analysis

Every answer must (i) show at least two reasoning steps, (ii) include a dimensional check or a limiting-case check, and (iii) end with one to three sentences interpreting the result in words. Questions marked **[Core]** are required of everyone. **[Challenge]** questions are for students who want more. **[Extension]** questions are for honors and independent study.

**A1 [Core] — Shear and moment from the gages.** Use the Part A loading steps above 1 kN. For the bottom gages at $x$ = 100 mm, 150 mm and midspan, fit strain against $P$ and convert each slope to moment per unit load with Eq. 16, using your $E$ from A3. Plot $M/P$ against $x$ with the statics line of Eq. 2 and find $V/P$ from the two shear-span gages. Compare it with 1/2 using Eq. 18. *Check:* extrapolate your line to $x = 0$; what should $M$ be there, and is it? *Interpret:* what does the measured slope tell you about the reaction, and why does the gradient between the load points vanish?

**A2 [Core] — The strain profile and plane sections.** For every Part A step, fit Eq. 15 to the seven midspan gages and report $\kappa$, $y_{NA}$ and the RMS residual. Plot the strain profiles at 5, 10 and 20 kN with their fitted lines. Report the mean $y_{NA}$ with its uncertainty and compare it with $h/2$. *Check:* the residuals should be comparable to the reading noise (about 1–2 µε), and the top and bottom strains equal and opposite. *Interpret:* what would a curved profile or a residual growing with load have meant physically?

**A3 [Core] — E from moment and curvature.** Fit $M = (P/2)a$ against $\kappa$ from A2 for the loading steps, and compute $E$ from the slope and $I$, with its uncertainty from Eq. 17. Compare it with your Lab 2 value. Then at 20 kN compare the bottom-fiber stress from the flexure formula (Eq. 6) with $E$ times the measured strain. *Check:* units of the slope; show that a 1 % error in $h$ gives a 3 % error in $E$. *Interpret:* which uncertainty term dominates, and why does a common gage-factor error bias $E$ but not $y_{NA}$?

**A4 [Core] — Poisson's ratio from anticlastic curvature.** Fit the top-transverse strain against the top longitudinal strain for the Part A loading steps and report $\nu$ from Eq. 8 with its uncertainty. Compare with Lab 2. Find the anticlastic radius $\rho'$ at 20 kN. *Check:* the sign of the transverse strain on the compressed face. *Interpret:* why is a transverse gage near the edge of the top face slightly less reliable than one at its center?

**A5 [Core] — The composite beam.** From the Part B profile fits, find the neutral-axis height and compare it with your P3 prediction recomputed with measured dimensions and your $E$, propagating the uncertainty in $n$. Fit $M$ against $\kappa$ to get the measured $EI$ and compare it with $E_1 I_t$. At 15 kN, use the fitted strain line and each material's $E$ to find the stresses at the four points of P3, and compare. Finally, evaluate $\int\sigma_x\,dA$ from your fitted strain line as a fraction of the compressive resultant. *Check:* that fraction should be near zero; why? *Interpret:* how much stiffer is the composite bar than bar A alone, and where is it most highly stressed?

**A6 [Core] — Beyond first yield.** Plot the Part C moment against measured curvature, with the elastic line, the EPP curve of Eq. 12 and the curve from the simulation's strip summation with the material's own law (Section & stress, preset "Lab Part C", one point per measured $\kappa$; export the CSV). At 40 kN, report the flexure stress $M_{max}c/I$, the actual extreme-fiber stress (Lab 1's curve at the measured extreme strain) and the percentage by which the flexure formula overstates it. Predict the permanent curvature with Eq. 14 and compare it with the curvature measured after unloading. Report the strip-summation surface residual stress on the tension side. Finally, predict the straightedge gap from your permanent curvature, assuming it is confined to the middle 200 mm (Appendix D.9), and compare it with the measured gap. *Check:* the neutral axis and the RMS residual of the profile fit at 40 kN: do plane sections still hold? *Interpret:* why does the EPP model overpredict the moment at moderate curvature, why is the permanent set larger than a simple bilinear picture suggests, and what does the gap tell you about where else the bar yielded?

**A7 [Core] — Theory vs. simulation vs. measurement.** Complete Table 5. Make one figure with error bars at $\pm U$ for each row, normalized by its theory value. Explain **every** discrepancy larger than the expanded uncertainty with a named cause, quantified where you can.

**M1 [Core] — Where does the model break?** (a) Run "Flexure formula beyond yield": by what percentage does $Mc/I$ overstate the real extreme-fiber stress at 40 kN, and how does the error grow with load? (b) Run "Aluminum is not elastic–perfectly plastic": at the measured 40 kN curvature, how far apart are the two laws, and which one your data follow? (c) Run "Ignore the steel strip": how far does the neutral axis move, and by what factor would you misjudge the stress in the strip? (d) Plane sections: compare the profile-fit RMS residual at 20 kN (Part A) and 40 kN (Part C). Do your data show any departure from Eq. 3, and if not, which of Eqs. 3–6 failed in Part C?

**C1 [Challenge] — Shape factor.** Derive $Z$ and $k$ for the simulation's I-section preset (Appendix D.6) and run "An I-beam has little plastic reserve". Explain the difference from the rectangle with the stress blocks of Figure 4b. What does it mean for design against collapse rather than first yield?

**C2 [Challenge] — Convergence.** In **Section & stress**, preset "Lab Part B" (elastic, so the transformed section is exact), record the error in the strip-summation moment at $N_s$ = 10, 20 and 40. Show that it falls as $N_s^{-2}$ and Richardson-extrapolate ($M \approx (4M_{2N} - M_N)/3$). Repeat with preset "Lab Part C" and the law set to Elastic–perfectly plastic: on the convergence plot the error still falls roughly as $N_s^{-2}$, but not smoothly. Explain why from where the elastic–plastic boundary falls among the strips. Then run "Refine the load integration" and show the same order for the triangular load. Why is the four-point case exact at any $N$?

**C3 [Challenge] — How errors propagate.** Show from Eq. 15 that (a) a common gage-factor error scales $\kappa$ but leaves $y_{NA}$ unchanged; (b) a common offset in all gage heights shifts $y_{NA}$ but leaves $\kappa$ unchanged; (c) a 0.1 mm error in one gage's height changes the fitted $\kappa$ by an amount you estimate. Which of these could explain any discrepancy in A2 or A3?

**X1 [Extension] — A bimetal strip.** Bar B is heated uniformly by $\Delta T$ with no load. Using compatibility at the interface ($\alpha$ = 23.6 × 10⁻⁶ /K for 6061-T6 and 11.7 × 10⁻⁶ /K for 1018 steel) and the equilibrium conditions of Eqs. 4, find the curvature per kelvin and the interface stresses for $\Delta T$ = 50 K. Check the limit of equal coefficients.

**X2 [Extension] — Reverse loading.** For an EPP rectangle unloaded from $M_{max}$, find the residual stress at the extreme fibers and the reverse moment at which the beam yields again. Show that unloading from any $M_{max} \le M_p$ never causes reverse yield.

**X3 [Extension] — An unsymmetric section.** For the simulation's T-section (Section & stress, shape T-section), find the elastic neutral axis, the plastic neutral axis (equal areas) and the shape factor, and check them against the simulation at a large curvature. Why do the two axes differ?

## 8. Design problem

**D1 — A floor beam.** A simply supported beam spans 3.0 m and carries a uniform load of 3.0 kN/m (self-weight included) and a 5.0 kN point load at midspan. Requirements:

* factor of safety of at least 1.67 against first yield, using a **conservative** yield strength from **your** Lab 1 measurement ($\sigma_Y - U$);
* midspan deflection no more than $L/240$, using $\delta = \dfrac{5wL^4}{384EI} + \dfrac{PL^3}{48EI}$ (you will derive both terms in Lab 7) and **your** measured $E$ for aluminum;
* a section from Table 6, in 1018 steel or 6061-T6 aluminum.

Choose a material and a section. Densities: 7870 kg/m³ (steel), 2700 kg/m³ (aluminum); stock prices about \$2.20/kg (steel) and \$6.50/kg (aluminum). More than one design is acceptable. Justify yours with a quantitative trade-off (mass, cost or another criterion you define), and say which requirement governs for each material. Submit at most one page: the moment and the required $S$ and $I$ for each material, a table of the candidates you checked, the chosen design with every requirement checked, and one assumption that could invalidate your design (for example, lateral support of the compression flange), with how you would check it.

| Section | $h$ × $b$ (mm) | Flange $t_f$ / wall $t$ (mm) | Web $t_w$ (mm) | Area (mm²) | $I$ (10⁶ mm⁴) | $S$ (10³ mm³) |
|-------------------|-------------|--------------|----------:|----------:|-----------:|-----------:|
| I-100 | 100 × 55 | 5.7 | 4.1 | 990 | 1.633 | 32.66 |
| I-120 | 120 × 64 | 6.3 | 4.4 | 1279 | 3.063 | 51.05 |
| I-140 | 140 × 73 | 6.9 | 4.7 | 1601 | 5.253 | 75.04 |
| I-160 | 160 × 82 | 7.4 | 5.0 | 1940 | 8.346 | 104.3 |
| I-180 | 180 × 91 | 8.0 | 5.3 | 2325 | 12.72 | 141.4 |
| I-200 | 200 × 100 | 8.5 | 5.6 | 2725 | 18.46 | 184.6 |
| RT-100x50x4 | 100 × 50 | 4.0 | — | 1136 | 1.441 | 28.83 |
| RT-120x60x5 | 120 × 60 | 5.0 | — | 1700 | 3.094 | 51.57 |
| RT-150x100x5 | 150 × 100 | 5.0 | — | 2400 | 7.545 | 100.6 |
| RT-200x100x6 | 200 × 100 | 6.0 | — | 3456 | 17.94 | 179.4 |

: Table 6. Generic catalog (I: wide-flange I-section; RT: rectangular tube with sharp corners). Properties are about the strong axis.

| Criterion | Weight |
|------------------------------------------------------------------------------|-------:|
| Moment diagram and maximum moment correct; requirements translated into required $S$ and $I$, units correct | 20 % |
| Conservative strength and measured $E$ from **your** data, applied to the right material | 25 % |
| Every requirement checked for the final design; governing requirement identified for each material | 20 % |
| Choice justified by a quantitative comparison of at least two alternatives | 25 % |
| Clear one-page presentation; one critical assumption named and a check proposed | 10 % |

: Table 7. How D1 will be graded.

## 9. Report

Write a technical report of at most eight pages plus appendices, one per team. Include the pre-lab, Tables 3–5, all plots with labeled axes and units, every Core answer, M1 and D1. Challenge and Extension answers go in a clearly marked section. State every number as value ± $U$ with units, rounded per the style rules (uncertainty to one or two significant figures, value to the same decimal place). Put your analysis code or spreadsheet in an appendix.

| Part | Points |
|---|---:|
| Pre-lab P1–P6 | 15 |
| Data quality and procedure (Tables 3–4, checks performed) | 10 |
| Core analysis A1–A7 | 45 |
| M1 — Where does the model break? | 10 |
| D1 — Design problem | 15 |
| Communication: figures, units, uncertainty format | 5 |
| **Total** | **100** |
| Challenge (C1–C3) | up to +10 |

: Table 8. Report grading. Extension questions are graded separately for honors and independent-study credit.

::: pagebreak
:::

## Appendix A — Running the lab without equipment

If the machine is unavailable, use `sample_data.csv`. It holds one row per load step for the three parts:

| Column | Meaning |
|---|---|
| `part` | `A` (bar A, elastic), `B` (bar B, composite) or `C` (bar A beyond yield) |
| `step` | load step number within the part, from 0 |
| `load_N` | total load $P$ on the spreader (N), resolution 1 N |
| `strain_side1_ue`, `strain_side2_ue`, `strain_side3_ue`, `strain_side4_ue`, `strain_side5_ue` | side gages at midspan, from the lowest (1) to the highest (5) (µε) |
| `strain_top_ue`, `strain_bottom_ue` | top-face and bottom-face gages at midspan (µε) |
| `strain_transverse_top_ue` | transverse gage on the top face at midspan (µε) |
| `strain_bottom_x100_ue`, `strain_bottom_x150_ue` | bottom-face gages at $x$ = 100 and 150 mm (µε); blank for Part B |

: Table A1. Columns of `sample_data.csv`. All strains are zeroed at the start of each part, resolution 1 µε.

Part A was loaded in 2.5 kN steps to 20 kN and unloaded in 5 kN steps; Part B in 2.5 kN steps to 15 kN and back; Part C in 5 kN steps to 25 kN, 3 kN steps to 40 kN, and unloaded in 10 kN steps. Use these measurements:

| Quantity | Readings |
|---|---|
| Bar A width $b$ (mm) | 25.43, 25.41, 25.42 |
| Bar A depth $h$ (mm) | 50.79, 50.77, 50.78 |
| Bar B strip thickness $t_s$ (mm) | 6.37, 6.35, 6.36 |
| Span / load rollers from left support (mm) | 600.0 / 200.0, 400.0 |
| Bar A side gages $y_h$ (mm) | 5.65, 15.18, 25.49, 35.15, 45.62 |
| Bar B side gages $y_h$ (mm) | 10.28, 20.21, 30.40, 40.09, 50.25 |
| Straightedge gap at midspan after Part C, bar resting on its ends (mm) | 2.85 |
| Bar A length (mm) | 700 |

: Table A2. Measurements for the sample data. Instrument accuracies are those of Table 2; the load-roller positions are good to ±0.5 mm.

## Appendix B — Uncertainty quick reference

* Limit $\pm a$ (calibration, accuracy): $u = a/\sqrt{3}$. Reading resolution $r$: $u = r/\sqrt{12}$ (already included when you use the scatter of repeated readings).
* Sum or difference: $u_{x \pm y}^2 = u_x^2 + u_y^2$. Product or quotient: $(u_{xy}/xy)^2 = (u_x/x)^2 + (u_y/y)^2$. Power: $u_{x^k}/x^k = |k|\,u_x/x$.
* Mean of $N$ readings: $u = s/\sqrt{N}$ for the scatter, combined with any calibration term.
* Least-squares line $y = A_0 + A_1x$ through $N$ points: $s_{A_1} = s/\sqrt{\sum(x_i - \bar x)^2}$, with $s^2 = \sum(y_i - A_0 - A_1x_i)^2/(N-2)$ (LINEST in a spreadsheet).
* *Neutral axis from a fit.* $y_{NA} = -A_0/A_1$ is a ratio of correlated fit parameters; for one step, use the scatter of $y_{NA}$ over all the steps above 1 kN instead ($u = s/\sqrt{N}$), and add the height-gage term $0.05/\sqrt{3}$ mm divided by $\sqrt{5}$ for the five side gages.
* *A quantity from an inverted formula (P4, A6).* Perturb each input by its $u$, recompute, and add the changes in quadrature.
* *Example.* Three caliper readings of $h$ with $s$ = 0.010 mm and accuracy ±0.02 mm: $u_h = \sqrt{0.010^2/3 + 0.02^2/3}$ = 0.013 mm, so $3u_h/h$ = 0.08 %.
* Report $x \pm U$ with $U = 2u$. Round $U$ to one or two significant figures, and $x$ to the same decimal place.

## Appendix C — Using the simulation

Open `lab04_simulation.html` in any browser; it needs no internet connection. Choose a configuration and a preset, then move the sliders. In **Beam & diagrams** mode, choose the supports and the loads; the plots show $V$ and $M$ from statics (solid) and from step-by-step integration of Eqs. 1 (markers), with the sample data's moments when the set-up matches Part A. In **Section & stress** mode, choose the shape and materials and set the curvature; the **law** toggle switches the strip summation between the material's own stress–strain curve and the EPP model, and **Stress state** switches between the loaded state and the state after unloading. The **readout table** compares each closed-form result with the independent numerical solution: "agree" rows check the formulas, and "different models" rows show how far a formula is from a more realistic model. **Push the model past its assumptions** runs prepared experiments. **Export (CSV)** saves the curves, the readout or the convergence study; if your browser blocks the download, the data appears in a box you can copy. The **SI / US customary** toggle converts every input and output.

## Appendix D — Derivations

**D.1 Load, shear and moment (Eqs. 1–2).** Take a slice between $x$ and $x + dx$ carrying the downward load $w\,dx$. With $V$ and $M$ positive as in the sign-convention box, vertical equilibrium gives $V - (V + dV) - w\,dx = 0$, so $dV/dx = -w$. Moments about the right face give $(M + dM) - M - V\,dx + w\,dx\,(dx/2) = 0$, so $dM/dx = V$ as $dx \to 0$. For four-point bending, symmetry gives reactions $P/2$; the left free body at $x < a$ carries $M = (P/2)x$, and at $a < x < L - a$ it carries $M = (P/2)x - (P/2)(x - a) = Pa/2$, independent of $x$, so $V = 0$ there. If the load points are at $a_1$ and $a_2$ instead, $R_A = (P/2)(2L - a_1 - a_2)/L$ and $M = R_Ax - (P/2)(x - a_1)$ between the loads, whose slope $R_A - P/2$ vanishes only when $a_1 + a_2 = L$.

**D.2 Flexure formula (Eqs. 3–7).** By symmetry, a cross-section of a symmetric member bent by equal and opposite end couples cannot warp: a bulge toward one end would look different from the other end, which the loading cannot tell apart. So sections stay plane, and a fiber at distance $y$ from the surface that keeps its length (the neutral surface) has length $(\rho - y)\theta$ where the neutral surface has $\rho\theta$; its strain is $-y/\rho$ (Eq. 3). With $\sigma_x = E\varepsilon_x = -E\kappa y$, the first of Eqs. 4 gives $-E\kappa\int y\,dA = 0$: the neutral axis is at the centroid. The second gives $E\kappa\int y^2\,dA = EI\kappa = M$ (Eq. 5), and eliminating $E\kappa$ gives Eq. 6. For a rectangle, $\int y^2\,dA = \int_{-h/2}^{h/2} b\,y^2\,dy = bh^3/12$ (Eq. 7). Units: N·m / (N/m² × m⁴) = m⁻¹.

**D.3 Anticlastic curvature (Eq. 8).** The stress is uniaxial ($\sigma_y = \sigma_z = 0$), so Hooke's law gives $\varepsilon_z = -\nu\sigma_x/E = -\nu\varepsilon_x = \nu y/\rho$. A transverse strain linear in $y$ is a curvature in the $y$–$z$ plane of magnitude $\nu/\rho$, of opposite sense to the longitudinal one.

**D.4 Transformed section (Eqs. 9–10).** With $\varepsilon_x = -\kappa y$ in both materials, $\sigma_1 = -E_1\kappa y$ and $\sigma_2 = -E_2\kappa y = -nE_1\kappa y$. The force on an element $dA$ of material 2 is the same as on an element $n\,dA$ of material 1, so Eqs. 4 become the homogeneous-beam conditions for a section whose material-2 parts are $n$ times as wide: $\int y\,dA_t = 0$ (the neutral axis is the transformed centroid) and $E_1\kappa I_t = M$. Substituting back gives Eq. 10. If $t_s \to 0$ or $n = 1$, the result reduces to Eqs. 6–7.

**D.5 Elastoplastic rectangle (Eqs. 11–12).** Yield begins at $|y| = c$ when $E\kappa c = \sigma_Y$ (Eq. 11). For $\kappa > \kappa_Y$ the fibers with $|y| < y_Y = \sigma_Y/(E\kappa)$ are elastic and the rest are at $\mp\sigma_Y$. Then $M = 2b\left[\int_0^{y_Y}\frac{\sigma_Y}{y_Y}y^2\,dy + \int_{y_Y}^{c}\sigma_Y y\,dy\right] = 2b\sigma_Y\left[\frac{y_Y^2}{3} + \frac{c^2 - y_Y^2}{2}\right] = b c^2\sigma_Y\left[1 - \frac{y_Y^2}{3c^2}\right]$. With $M_Y = \sigma_Y bh^2/6 = \frac{2}{3}bc^2\sigma_Y$ and $y_Y/c = \kappa_Y/\kappa$, this is Eq. 12.

**D.6 Fully plastic moment (Eq. 13).** When every fiber is at $\pm\sigma_Y$, the first of Eqs. 4 says the areas in tension and compression are equal, so the plastic neutral axis bisects the area. The moment is $\sigma_Y$ times the sum of the first moments of the two halves about that axis, which defines $Z$. For a rectangle, $Z = 2 \times (bh/2)(h/4) = bh^2/4$, and $k = Z/S = 1.5$. For an I-section of depth $h$, flange width $b$, flange thickness $t_f$ and web thickness $t_w$, with web height $h_w = h - 2t_f$: $Z = bt_f(h - t_f) + t_w h_w^2/4$.

**D.7 Unloading (Eq. 14).** Removing $M_{max}$ changes every fiber's strain by $\Delta\varepsilon = \Delta\kappa\,y$ in reverse. If no fiber reverse-yields, the stress change is elastic everywhere, so it is the elastic solution for $-M_{max}$: $\Delta\sigma = +M_{max}y/I$ and $\Delta\kappa = -M_{max}/(EI)$. The residuals carry $\int\sigma_{res}\,dA = 0 + 0$ and $-\int y\sigma_{res}\,dA = M_{max} - M_{max} = 0$.

**D.8 Gage fit (Eqs. 15–16).** With heights from the bottom, Eq. 3 reads $\varepsilon_x = -\kappa(y_h - y_{NA}) = \kappa y_{NA} - \kappa y_h$, a straight line with slope $-\kappa$ and intercept $\kappa y_{NA}$. In the elastic range the bottom fiber has $\sigma = Mc/I = M/S$ and $\sigma = E\varepsilon$, so $M = ES\varepsilon_{bottom}$; with Eq. 1, the slope of $M$ along the beam is $V$.

**D.9 Straightedge gap.** Suppose the permanent curvature $\kappa_p$ is uniform over the middle region of half-length $m$ (here 100 mm) and zero elsewhere, and the bar's half-length is $\ell$ (350 mm). Measured from the tangent at midspan, the top face rises by $\kappa_p m^2/2$ over the curved part and then by $\kappa_p m$ per unit length along the straight remainder, so each end is higher by $\kappa_p m^2/2 + \kappa_p m(\ell - m) = \kappa_p m(\ell - m/2)$. A straightedge resting on the two ends therefore stands that far above the top face at midspan. If the shear spans also yielded near the load points, they add their own permanent curvature, and the gap is larger.

# Lab 7 — Deflection of Beams: Superposition, Redundant Supports and Large Deflection

| | |
|---|---|
| **Course** | ENGR 2228 Mechanics of Materials |
| **When** | Week 13, after lectures on Beer 8e Ch. 9 |
| **Textbook** | Beer, Johnston, DeWolf, Mazurek, *Mechanics of Materials*, 8th ed. (Beer 8e): §9.1A, §9.2, §9.4A–9.4B and Appendix F; §11.6 for Maxwell's reciprocal theorem; §10.1 for the exact curvature |
| **Session** | 2 hours in the lab, teams of two; report due one week later |
| **Equipment** | Beam-deflection frame with knife-edge supports, a bench clamp and an adjustable roller prop on a load cell; three digital indicators on magnetic stands; load hangers and slotted masses; micrometer and calipers; a 1018 steel bar 25.4 × 6.35 × 1000 mm; a blue-tempered spring-steel strip 12.7 × 0.79 mm in a bench vise, in front of a grid board |
| **Files** | `lab07_simulation.html` (open in any browser, works offline), `sample_data.csv`, and `beam_deflection.cpp` (the C++ program whose solver the simulation uses) |

## 1. Learning objectives

After this lab you will be able to:

1. Measure the elastic curve of a beam and recover E from it with Beer's App. F formulas (§9.1, App. F).
2. Show by measurement that deflections superpose and that the deflection at one point under a load at another equals the reverse (§9.4, §11.6).
3. Solve a statically indeterminate beam by superposition, measure its redundant reaction, and explain why a real clamp makes the measured reaction differ from the textbook value (§9.2, §9.4B).
4. Predict how a support settlement changes the reactions of an indeterminate beam.
5. Recognize when the small-slope equation EI y″ = M stops applying, and compare linear theory with the exact large-deflection solution (§9.1A, §10.1).
6. Design a beam with an overhang for strength and deflection, choosing both the section and the support position.

## 2. Theory

The three set-ups are shown in Figure 1. Part A loads the steel bar on a simple span, Part B clamps the same bar at one end and props it at the other, and Part C bends a thin spring-steel strip until its tip has moved more than half its length.

![Figure 1. Test set-ups (schematic). (a) The bar on knife edges 800 mm apart, with indicators at 200, 400 and 600 mm and hangers at 200 and 600 mm. (b) The bar clamped at one end, with a roller prop on a load cell 700 mm from the clamp and indicators at 350 and 700 mm. (c) The spring-steel strip in a vise, loaded by a hanging weight; the tip position is read on a grid board.](figures/fig1_setup.png){width=6.4in}

::: {.needspace lines="12"}
:::

::: {custom-style="Callout"}
**Sign convention (Beer 8e).** $x$ is measured from the left end of the beam. Deflection $y$ is positive **upward**, so a beam under downward loads has $y < 0$; we report the downward deflection $\delta = -y$ where that is clearer. The slope is $\theta = dy/dx$. $V$ and $M$ follow Fig. 5.6 ($M > 0$ sags), and $EI\,d^2y/dx^2 = M$ (Eq. 9.4). Loads $P$ and $w$ act downward; an applied couple is positive counterclockwise. Reaction forces are positive upward, reaction couples positive counterclockwise. Tension is positive. The C++ program `beam_deflection.cpp` takes $y$ positive downward internally; the simulation converts all of its output to the convention above.
:::

::: {custom-style="Callout"}
**Nomenclature.** $x$ position along the beam; $y$ deflection (up +); $\delta$ downward deflection; $\theta$ slope; $L$ span or free length; $a$, $b = L - a$ load position from the left and right supports; $P$ point load; $w$ load per unit length; $M$ bending moment; $E$ modulus of elasticity; $I$ moment of inertia; $EI$ flexural rigidity; $c$ compliance (deflection per unit load); $R_A$, $R_B$ reactions; $M_A$ reaction couple at the clamp; $k$ rotational stiffness of the clamp; $\lambda = EI/(kL)$ clamp flexibility; $\Delta$ settlement of a support; $s$ arc length; $\alpha = PL^2/EI$ load parameter; $\beta = wL^3/EI$ self-weight parameter; $\theta_0$ tip angle; $\delta_v$, $\delta_h$ vertical and horizontal tip displacement; $K$, $F$, $E(\cdot)$ elliptic integrals; $u$ standard uncertainty; $U = 2u$ expanded uncertainty.
:::

Full derivations are in **Appendix D**; this section states each result, what it means, and when it stops applying.

### 2.1 The elastic curve

A beam bends with curvature $1/\rho = M/EI$ (Ch. 4). For small slopes the curvature of the curve $y(x)$ is $d^2y/dx^2$, so (§9.1A)

$$EI\,\frac{d^2y}{dx^2} = M(x) \qquad (1)$$

Integrating twice gives the slope and the deflection, with two constants fixed by the supports: $y = 0$ at a pin or a roller, and $y = 0$ and $dy/dx = 0$ at a fixed end. Beer's App. F lists the results for the common cases. For a simple span with a load $P$ at distance $a$ from the left support ($b = L - a$),

$$y = -\frac{Pbx}{6EIL}\left(L^2 - b^2 - x^2\right) \quad (0 \le x \le a) \qquad (2)$$

and the mirror-image expression for $x \ge a$. Every App. F deflection has the form (number) × load × $L^n/EI$, so a measured deflection gives $EI$ directly.

*Worked example.* A 2.0 m simple span with $EI$ = 50 kN·m² carries 1.2 kN at $a$ = 1.5 m ($b$ = 0.5 m). At midspan ($x$ = 1.0 m ≤ $a$): $y = -(1200)(0.5)(1.0)(4 - 0.25 - 1)/(6 \times 50\,000 \times 2) = -2.75$ mm.

### 2.2 Superposition and reciprocity

Equation 1 is linear in $M$, and $M$ is linear in the loads. The deflection under several loads is therefore the sum of the deflections under each load alone (§9.4A, Figure 2a):

$$y(x) = \sum_i y_i(x) \qquad (3)$$

A consequence (Maxwell's reciprocal theorem, §11.6): the deflection at point 1 caused by a unit load at point 2 equals the deflection at point 2 caused by a unit load at point 1,

$$c_{12} = c_{21} \qquad (4)$$

![Figure 2. (a) On a simple span, the elastic curves of two separate loads add to the curve of both together. (b) A propped cantilever as superposition: the cantilever deflects down under the load and up under the prop force R; R is the force that makes the sum zero at the prop.](figures/fig2_superposition.png){width=6.4in}

### 2.3 Statically indeterminate beams

A propped cantilever has one reaction more than statics can find. Remove the prop and treat its reaction $R_B$ as an unknown load (§9.4B, Figure 2b). The cantilever deflects at the prop by an amount from the load and by $R_B L^3/(3EI)$ from the prop force; the prop requires their sum to be zero. For a central load,

$$R_B = \frac{5P}{16}, \qquad M_A = \frac{3PL}{16} \qquad (5)$$

If the prop **settles** by $\Delta$ (downward), the condition becomes $y(L) = -\Delta$, and the reaction drops by

$$\Delta R_B = -\frac{3EI}{L^3}\,\Delta \qquad (6)$$

In a determinate beam a settlement just tilts the beam; in an indeterminate beam it changes the reactions and the moments.

### 2.4 A clamp is a spring

Equations 5 and 6 assume a perfectly fixed end. A bench clamp lets the bar rotate a little, roughly in proportion to the moment it carries: $\theta_A = M_A/k$, with $k$ the clamp's **rotational stiffness** (Figure 3a). For a cantilever with a load $P$ at $x = L$, the extra rotation tilts the whole bar,

$$\delta(x) = \frac{Px^2(3L - x)}{6EI} + \frac{PLx}{k} \qquad (7)$$

so the clamp can be measured with two indicators. In the propped cantilever it moves load from the clamp to the prop (Figure 3b). With $\lambda = EI/(kL)$ and a central load,

$$\frac{R_B}{P} = \frac{5/16 + 3\lambda/2}{1 + 3\lambda}, \qquad \Delta R_B = -\frac{\Delta}{L^3/(3EI) + L^2/k} \qquad (8)$$

which runs from 5/16 for a rigid clamp to 1/2 when the clamp becomes a pin.

![Figure 3. (a) A clamp modeled as a rotational spring of stiffness k: the clamp turns by M_A/k and the beam tilts with it. (b) The prop reaction of a propped cantilever rises as the clamp flexibility EI/(kL) grows.](figures/fig3_clamp.png){width=6.4in}

*When Eqs. 1–8 apply:* elastic material; slopes small enough that $(dy/dx)^2 \ll 1$ (about 0.1 rad gives a 1.5 % curvature error); a beam long compared with its depth, so that shear deformation is negligible (Lab 5); supports and loads as modeled. The next section is about the second condition.

### 2.5 Large deflection: the elastica

When the slope is no longer small, the exact curvature must be used: $EI\,d\theta/ds = M$, with $\theta$ the angle of the tangent and $s$ the arc length. For a cantilever with a vertical load $P$ at its tip, $M = P(x_{tip} - x)$, which depends on where the tip has moved to. In terms of the **load parameter** $\alpha = PL^2/EI$, the solution is the elastica (Appendix D.5):

$$\sqrt{\alpha} = K(k) - F(\varphi_1, k), \qquad \frac{\delta_v}{L} = 1 - \frac{2}{\sqrt{\alpha}}\left[E(k) - E(\varphi_1, k)\right], \qquad \frac{x_{tip}}{L} = \sqrt{\frac{2\sin\theta_0}{\alpha}} \qquad (9)$$

where $k^2 = (1 + \sin\theta_0)/2$, $\sin\varphi_1 = 1/(k\sqrt{2})$, and $F$, $E$ are elliptic integrals of the first and second kind (Appendix E tabulates the result). Linear theory gives

$$\frac{\delta_v}{L} = \frac{\alpha}{3}, \qquad \delta_h = 0 \qquad (10)$$

It is the tangent of Eq. 9 at $\alpha = 0$. It overstates $\delta_v$ by 5 % at $\alpha \approx 0.68$, and it misses the inward movement $\delta_h$ of the tip altogether (Figure 4). The strip's own weight, $\beta = wL^3/EI$, adds a small extra deflection that the simulation can include.

![Figure 4. (a) Shapes of a tip-loaded cantilever at increasing load: the exact shape (solid) keeps the strip's length, so the tip swings inward; linear theory (dotted) does not. (b) Tip displacements against α: linear theory is accurate only at small α.](figures/fig4_elastica.png){width=6.4in}

### 2.6 The model in the simulation

`lab07_simulation.html` has two configurations. **Beam** evaluates the closed forms of Sections 2.1–2.4 by superposing App. F cases, finding redundant reactions from the extra support conditions. It checks them against a **finite-element** solution: the solver of `beam_deflection.cpp`, ported line by line, which divides the beam into Hermite cubic elements and solves $\mathbf{K}\mathbf{u} = \mathbf{F}$ (Appendix D.6). The page adds two features to the C++ solver: a rotational spring at a clamp and a prescribed support settlement. **Large deflection** compares Eq. 9 with a numerical **RK4 integration** of the exact equation, with or without the strip's weight. The test files compare the ported solver with the compiled C++ program at every node.

### 2.7 Uncertainty

Use standard uncertainties $u$; convert a limit $\pm a$ to $u = a/\sqrt{3}$; propagate to first order (Appendix B). In Part A, each fitted compliance $c$ (deflection per newton) gives $E = f/(cI)$, where $f$ is the App. F factor ($c = f/EI$). With $I = bh^3/12$:

$$\left(\frac{u_E}{E}\right)^2 = \left(\frac{u_c}{c}\right)^2 + \left(\frac{u_b}{b}\right)^2 + \left(\frac{3u_h}{h}\right)^2 + \left(\frac{u_f}{f}\right)^2 \qquad (11)$$

where $u_f$ comes from the positions of the supports, the hanger and the indicator. Report $x \pm U$ with $U = 2u$ and draw error bars at $\pm U$. A measurement and a prediction **agree** when

$$|x_{meas} - x_{pred}| \le 2\sqrt{u_{meas}^2 + u_{pred}^2} \qquad (12)$$

Any larger discrepancy needs a physical or procedural explanation, quantified where possible.

## 3. Pre-lab (due at the start of the session)

Answer on paper or in a short document. Show every step, units included. Use Table 1 and the nominal dimensions in Table 2.

**P1 — Estimate before you measure.** (a) Part A: with 3.0 kg at 600 mm, find the deflection at 200, 400 and 600 mm from Eq. 2, and the largest bending stress. (b) Part B1: tip deflection under 1.0 kg at 700 mm for a rigid clamp. (c) Part B2: the prop reaction under 4.0 kg at mid-length (Eq. 5). (d) Part C: $\alpha$ for 0.62 kg on the 250 mm strip, and the tip deflection predicted by Eq. 10. Compare that number with the strip's length. Check the units of every answer.

**P2 — Superposition by hand.** For 2.0 kg at 600 mm and 1.0 kg at 200 mm together, predict the deflection at 400 mm from Eq. 2 twice and Eq. 3. Show that $c_{12} = c_{21}$ for the pair of points 200 mm and 600 mm (Eq. 4).

**P3 — The redundant reaction.** (a) Derive Eq. 5 by superposing the cantilever cases (Appendix D.2 outlines the steps). (b) With $\lambda = EI/(kL)$ = 0.04, find $R_B/P$ from Eq. 8. Will the measured reaction be above or below 5P/16? (c) Find the change in $R_B$ when the prop is lowered by 0.5 mm, for a rigid clamp (Eq. 6).

**P4 — Two indicators, two unknowns.** Using Eq. 7 with indicators at $L/2$ and $L$, write the two compliances in terms of $1/EI$ and $1/k$, and solve for both. Which combination is most sensitive to the clamp?

**P5 — Predict with the simulation.** Open `lab07_simulation.html`. For "Lab Part A: both loads", record the deflections at 200, 400 and 600 mm and the two parts that add up to them. For "Lab Part B2" (it opens with a flexible clamp, $k$ = 4400 N·m/rad), record $R_B$; then tick "Rigid clamp" and record it again. For "Lab Part C", record $\delta_v$ and $\delta_h$ at 0.62 kg with and without the strip's weight, and the load at which linear theory is 5 % off.

**P6 — Safety.** (a) List the hazards in this lab and how the procedure controls each. (b) Why is the bar in Part A limited to 3.0 kg per hanger, and the strip in Part C to 0.62 kg?

| Material | $E$ (GPa) | Yield strength $\sigma_Y$ (MPa) |
|---|---:|---:|
| 1018 steel bar (hot rolled) | 205.2 ± 1.2 (your Lab 1) | 296.2 ± 1.1 (your Lab 1) |
| Spring steel strip | 203 (supplier nominal); measure it in Part C | ≥ 1300 (supplier minimum) |
| 6061-T6 aluminum (D1) | 68.46 ± 0.47 (your Lab 2) | 273.7 ± 1.0 (your Lab 1) |

: Table 1. Reference values. The ± values are standard uncertainties. Replace them with your own team's results where you have them.

## 4. Equipment and safety

| Item | Specification used in this handout |
|---|---|
| Frame and supports | Knife edges, span adjustable, positions set with a steel rule (±0.5 mm); bench clamp with two 12 mm bolts; roller prop with a 0.01 mm micrometer screw, on a 50 N load cell (±0.5 % of reading, resolution 0.01 N) |
| Digital indicators | Resolution 0.001 mm, accuracy ±0.003 mm, plunger force about 1 N (constant over the stroke) |
| Masses and hangers | Hanger 0.50 kg (steel bar) or 0.020 kg (strip); slotted masses 0.5 kg and 0.05 kg, tolerance ±0.1 % |
| Calipers / micrometer | Accuracy ±0.02 mm / ±0.003 mm |
| Steel bar (Parts A and B) | 1018 hot rolled, 25.4 × 6.35 × 1000 mm (nominal) |
| Spring-steel strip (Part C) | Blue-tempered, 12.7 × 0.79 mm (nominal), clamped with 250 mm free to the load hole; grid board with 10 mm squares |

: Table 2. Equipment. If your equipment differs, record its values and use them throughout.

::: {custom-style="Safety"}
**Safety.** Wear safety glasses throughout: a slipping clamp or a strip released under load can spring back. **Load limits:** Part A 3.0 kg on each hanger; Part B 1.0 kg at the tip without the prop and 4.0 kg at mid-length with the prop; Part C 0.62 kg. These keep the steel bar below about one sixth of its yield strength and the strip's root stress below about 0.65 of its supplier minimum. **Masses:** add and remove them by hand, one at a time, without dropping; keep feet clear of the hangers. **Clamp and vise:** tighten them before loading and never adjust them under load. **Strip:** the strip stores energy; lift the weight off before you release it, and keep your face out of its plane. **Indicators:** set them with no load on the beam; never reach across a loaded hanger.
:::

## 5. Procedure

1. **Measure.** Record $b$ and $h$ of the bar (micrometer for $h$, at four places), the span and the positions of the indicators and hangers in Part A, the free length and indicator positions in Part B, and $b$ and $t$ of the strip. Write everything in Table 3. **Check:** repeated readings should span no more than 0.03 mm (0.005 mm with the micrometer).
2. **Part A.** Set the knife edges 800.0 mm apart and the bar centered on them. Hang the empty hangers at 200 and 600 mm and zero the indicators: from here on, "mass" means the mass added to a hanger. Add 0.5 kg at a time at 600 mm up to 3.0 kg, reading all three indicators at each step; unload. Repeat at 200 mm. Then load 2.0 kg at 600 mm and 1.0 kg at 200 mm together. **Check at 1.0 kg:** the middle indicator should read close to your P1 value scaled to 1.0 kg.
3. **Part B1.** Clamp the bar with 700 mm free to the tip hanger and set the indicators at 350 and 700 mm. Zero with the empty hanger. Load to 1.0 kg in 0.2 kg steps, reading both indicators. **Check:** the tip deflection at 1.0 kg should be about 10 % more than your rigid-clamp estimate; if it is much more, tighten the clamp and repeat.
4. **Part B2.** Move the hanger to 350 mm. Raise the prop at 700 mm until it just touches the bar (the 700 mm indicator moves by no more than 0.002 mm), then tare the load cell. Load to 4.0 kg in 1.0 kg steps, reading the load cell and the 350 mm indicator.
5. **Part B3.** At 3.0 kg, read the load cell and the indicator, lower the prop by 0.500 mm with its micrometer screw, and read them again.
6. **Part C.** Clamp the strip with 250 mm free, flat side horizontal, in front of the grid board. Read the position of the load hole with no load (the strip sags a little under its own weight). Hang the 0.020 kg hanger, then add masses so that the total hanging mass is 0.04, 0.07, 0.12, 0.17, 0.22, 0.32, 0.42, 0.52 and 0.62 kg, reading the hole's horizontal and vertical position on the grid each time, sighting square to the board. **Check:** at 0.22 kg the tip should already be clearly (more than 10 mm) above where Eq. 10 puts it.
7. **Before you leave:** open the simulation, enter your measured dimensions in each Lab preset, and record its predictions in Table 5 next to your raw readings.

## 6. Data tables

```{=latex}
\renewcommand{\arraystretch}{1.9}
```

| Quantity | Readings | Mean |
|----------------------------------|------------------------------------------------|----------|
| Bar $b$, $h$ (mm) | | |
| Part A: span; indicator and hanger positions (mm) | | — |
| Part B: free length; indicator positions (mm) | | — |
| Strip $b$, $t$ (mm); free length (mm) | | |

: Table 3. Dimensions.

::: {.needspace lines="12"}
:::

| Test | Load | Readings |
|------------------------------|----------|--------------------------------------------------------------|
| Part A: three indicators, load at 600 mm (mm) | 1.0 kg | |
| Part B1: indicators at 350 and 700 mm (mm) | 1.0 kg | |
| Part B2: load cell (N), indicator at 350 mm (mm) | 2.0 kg | |
| Part C: tip $x$, $y$ on the grid (mm) | 0.22 kg | |

: Table 4. Spot readings for the checks in the procedure; record every step on a separate sheet.

| Quantity | Theory (equation) | Simulation | Measured ± U | Agree (Eq. 12)? |
|----------------------------------------|------------|------------|--------------|-----------|
| $E$ of the bar (GPa) | Lab 1 | — | | |
| Deflections at 200, 400, 600 mm, both loads (mm) | Eq. 3 | | | |
| $c_{12}$ vs $c_{21}$ (µm/N) | Eq. 4 | | | |
| $EI$ (N·m²) and $k$ (N·m/rad), Part B1 | Eq. 7 | — | | |
| $R_B/P$, Part B2 | Eqs. 5, 8 | | | |
| $\Delta R_B$ for 0.5 mm, Part B3 (N) | Eqs. 6, 8 | | | |
| $\delta_v$ at 0.62 kg, Part C (mm) | Eqs. 9, 10 | | | |

: Table 5. Theory vs. simulation vs. measurement.

```{=latex}
\renewcommand{\arraystretch}{1.15}
```

## 7. Analysis

Every answer must (i) show at least two reasoning steps, (ii) include a dimensional check or a limiting-case check, and (iii) end with one to three sentences interpreting the result in words. Questions marked **[Core]** are required of everyone. **[Challenge]** questions are for students who want more. **[Extension]** questions are for honors and independent study.

**A1 [Core] — E from the elastic curve.** For each Part A load position and each indicator, fit the deflection against $P = mg$ to get the compliance $c$ (µm/N). From Eq. 2 and your measured positions, compute $E = f/(cI)$ for each of the six coefficients, with its uncertainty (Eq. 11), and combine them. Compare with Lab 1 (Eq. 12). *Check:* show that $f/(cI)$ has units of pressure. *Interpret:* which measured dimension limits the accuracy of $E$, and why does a bending test need it so much more precisely than a tension test?

**A2 [Core] — Superposition and reciprocity.** Predict the three deflections under both loads from the single-load compliances (Eq. 3) and compare them with the measured ones. Compare $c_{12}$ (indicator at 200 mm, load at 600 mm) with $c_{21}$ (indicator at 600 mm, load at 200 mm). Plot the measured elastic curves with the App. F curves. *Check:* what would superposition predict if the bar were loaded past yield? *Interpret:* reciprocity holds whatever the beam's supports; why is that useful when an indicator cannot be placed where a load acts?

**A3 [Core] — The clamp.** From the Part B1 compliances at 350 and 700 mm, solve Eq. 7 for $EI$ and $k$ (P4), with uncertainties. Compare $EI$ with A1. Then compute the $EI$ you would have reported from the tip indicator alone, assuming a rigid clamp. *Check:* as $k \to \infty$, Eq. 7 must reduce to App. F case 1. *Interpret:* what fraction of the tip deflection comes from the clamp, and how would that error show up in an unsuspecting student's $E$?

**A4 [Core] — The redundant reaction and settlement.** Fit $R_B$ against $P$ in Part B2 and compare the slope with 5/16 (Eq. 5) and with Eq. 8 using your $k$. Compare the mid-length deflection per newton with both models. From Part B3, compare the measured $\Delta R_B$ with Eq. 6 and with Eq. 8. *Check:* Eq. 8 must give 5/16 at $\lambda = 0$ and 1/2 as $\lambda \to \infty$. *Interpret:* which support condition does the propped cantilever really have, and why does a settlement of half a millimeter matter in an indeterminate beam but not in a simple span?

**A5 [Core] — Large deflection.** (a) From the first four Part C points, zero load included (Eq. 10 holds within about 2 % up to 0.07 kg), find the strip's $EI$ from the slope of $\delta_v$ against $P$, which Eq. 10 says is $L^3/(3EI)$ (the intercept is the sag under the strip's own weight). Use the zero-load grid reading of the tip as $L$ (the sag under the strip's weight shortens it by less than 0.05 mm). (b) For every load, compute $\alpha$ and compare the measured $\delta_v$ and $x_{tip}$ with Eq. 10, with Eq. 9 (Appendix E or the simulation), and with the simulation including the strip's weight. Plot all three with your data and error bars against $\alpha$. *Check:* as $\alpha \to 0$, Eq. 9 must approach Eq. 10. *Interpret:* at what $\alpha$ does linear theory become 5 % wrong in your data, and what does the inward motion of the tip tell you about how the strip carries the load?

**A6 [Core] — Theory vs. simulation vs. measurement.** Complete Table 5. Make one figure with each row normalized by its theory value, with error bars at $\pm U$. Explain **every** discrepancy larger than the expanded uncertainty with a named cause, quantified where you can.

**M1 [Core] — Where does the model break?** (a) At the largest Part C load, by what factor does Eq. 10 overstate $\delta_v$, and what is the largest slope? (b) By how much would assuming a rigid clamp misstate $R_B$ and $EI$ in Part B? (c) How much does the strip's weight change $\delta_v$ at 0.12 kg and at 0.62 kg? Can your data resolve it? (d) Using the simulation, find the span at which shear deformation (shown in the warnings) would add 5 % to the central-load deflection of the Part A bar and of the D1 beam. Which of these assumptions matters most for each part of this lab?

**C1 [Challenge] — Why the finite elements are exact.** In the simulation, run "App. F case 5" and "App. F case 6" and record the convergence study for each. Explain why the nodal values are exact for any mesh (Appendix D.6), why the deflection between nodes converges as $N^{-4}$ under a uniform load, and why $EI\,y''$ converges only as $N^{-2}$.

**C2 [Challenge] — EI from the whole curve.** Fit $EI$ to all the Part C points with the large-deflection model including the strip's weight (adjust $E$ in the simulation, or use Appendix E and a correction for the weight). Compare it with A5(a) and explain the difference.

**C3 [Challenge] — How precisely must the prop be set?** Using Eq. 8, find the error in the prop height that would change $R_B$ at 4.0 kg by 5 %. Compare it with the 0.002 mm "just touching" criterion of step 4.

**X1 [Extension] — The elastica.** Derive Eq. 9 from $EI\,d\theta/ds = P(x_{tip} - x)$ (Appendix D.5), and show that it reduces to Eq. 10 for small $\alpha$.

**X2 [Extension] — Reciprocity from energy.** Prove Eq. 4 from the work done by two loads applied in either order (§11.6). Then show it for your measured data in Part B1 by computing the deflection at 700 mm due to a load at 350 mm from Eq. 7.

**X3 [Extension] — Extend the C++ program.** `beam_deflection.cpp` locks a fixed end completely. Following Appendix D.6, add a rotational spring to its `solveBeam()` (about five lines), rebuild it, and reproduce your Part B1 result.

## 8. Design problem

**D1 — An overhanging deck beam.** A 4.0 m long 6061-T6 aluminum beam supports a deck. It rests on a pin at its left end and on a roller at a position $L_s$ that you choose, so it overhangs the roller by $a = 4.0 - L_s$. It carries a uniform load of 2.0 kN/m over its whole length (self-weight included) and a 1.5 kN railing post at the free end of the overhang. Requirements:

* largest bending stress at no more than $0.6\,\sigma_Y$, with **your** Lab 1 yield strength;
* deflection between the supports no more than $L_s/360$, and at the tip of the overhang no more than $2a/360$ (up or down), with **your** Lab 2 $E$;
* the lightest section from Table 6, with the roller position to the nearest 0.05 m.

| Section | $H$ (mm) | $B$ (mm) | $t_f$ (mm) | $t_w$ (mm) |
|------------------|------:|------:|------:|------:|
| I 76 × 51 | 76.2 | 50.8 | 5.6 | 4.3 |
| I 102 × 64 | 101.6 | 63.5 | 6.4 | 4.8 |
| I 102 × 76 | 101.6 | 76.2 | 6.35 | 4.8 |
| I 127 × 76 | 127.0 | 76.2 | 7.1 | 5.1 |
| I 152 × 102 | 152.4 | 101.6 | 7.9 | 5.8 |
| I 178 × 102 | 177.8 | 101.6 | 8.4 | 6.1 |
| I 203 × 127 | 203.2 | 127.0 | 9.5 | 6.4 |

: Table 6. Catalog for D1 (6061-T6 I-sections, dimensions idealized without fillets; compute $I$ and the mass yourself, density 2700 kg/m³).

Use the simulation (preset "D1") to explore, then verify your final design by hand: the span deflection by superposing App. F cases 6 and 7 (the overhang's load acts on the span as an end couple), and the tip deflection as the span's end slope times $a$ plus the cantilever cases for the overhang. Compare your choice with the lightest section that works without an overhang. Submit at most one page: the reactions and moment diagram of your design, the three checks with numbers, a table of the sections and roller positions you tried, and one assumption that could invalidate your design, with how you would check it.

| Criterion | Weight |
|------------------------------------------------------------------------------|-------:|
| Reactions, moment diagram and section properties correct; units correct | 20 % |
| Deflections verified by hand superposition and matching the simulation | 25 % |
| All three requirements checked with **your** $E$ and $\sigma_Y$; governing one identified | 20 % |
| Section and roller position justified by a quantitative comparison of alternatives | 25 % |
| Clear one-page presentation; one critical assumption named and a check proposed | 10 % |

: Table 7. How D1 will be graded.

::: {.needspace lines="26"}
:::

## 9. Report

Write a technical report of at most eight pages plus appendices, one per team. Include the pre-lab, Tables 3–5, all plots with labeled axes and units, every Core answer, M1 and D1. Challenge and Extension answers go in a clearly marked section. State every number as value ± $U$ with units, rounded per the style rules (uncertainty to one or two significant figures, value to the same decimal place). Put your analysis code or spreadsheet in an appendix.

| Part | Points |
|---|---:|
| Pre-lab P1–P6 | 15 |
| Data quality and procedure (Tables 3–4, checks performed) | 10 |
| Core analysis A1–A6 | 45 |
| M1 — Where does the model break? | 10 |
| D1 — Design problem | 15 |
| Communication: figures, units, uncertainty format | 5 |
| **Total** | **100** |
| Challenge (C1–C3) | up to +10 |

: Table 8. Report grading. Extension questions are graded separately for honors and independent-study credit.

## Appendix A — Running the lab without equipment

If the equipment is unavailable, use `sample_data.csv`. It holds one row per load step:

| Column | Meaning |
|---|---|
| `part` | `A`, `B` or `C` |
| `config` | Part A: `P600`, `P200` (hanger used) or `both`; Part B: `cantilever`, `propped` or `settlement`; Part C: `elastica` |
| `step` | load step number within the test, from 0 |
| `mass_kg` | Parts A and B: mass added after zeroing with the empty hangers in place (kg); in Part A `both`, the sum of 2.0 kg at 600 mm and 1.0 kg at 200 mm. Part C: total hanging mass including the 0.020 kg hanger |
| `load_pos_mm` | nominal position of the load (mm) |
| `d1_mm`, `d2_mm`, `d3_mm` | indicator readings, downward deflection positive (mm). Part A: at 200, 400 and 600 mm. Part B1: `d1_mm` at 350 mm, `d2_mm` at 700 mm. Parts B2, B3: `d1_mm` at 350 mm |
| `R_N` | prop load cell, tared with the prop just touching (N) |
| `x_tip_mm`, `y_tip_mm` | Part C: position of the load hole on the grid, from the clamp edge; $x$ along the strip, $y$ up (mm) |

: Table A1. Columns of `sample_data.csv`. Indicators were zeroed with the empty hangers in place; in Part B3, the second row is after the prop was lowered by 0.500 mm.

::: {.needspace lines="16"}
:::

Use these measurements:

| Quantity | Readings |
|---|---|
| Bar $b$ (mm) | 25.42, 25.44, 25.43 |
| Bar $h$ (mm) | 6.361, 6.363, 6.362, 6.362 |
| Part A span / indicators / hangers (mm) | 800.0 / 200.0, 400.0, 600.0 / 200.0, 600.0 |
| Part B free length / indicators (mm) | 700.0 / 350.0, 700.0 |
| Part B3 prop lowered by (mm) | 0.500 |
| Strip $b$ (mm) | 12.70, 12.71, 12.69 |
| Strip $t$ (mm) | 0.787, 0.788, 0.786, 0.787 |
| Strip free length by rule (mm) | 250.0 |

: Table A2. Measurements for the sample data. Positions set with the rule are good to ±0.5 mm; the prop screw to ±0.005 mm; grid readings to ±0.5 mm. Use $g$ = 9.80665 m/s² and a steel density of 7850 kg/m³.

## Appendix B — Uncertainty quick reference

* Limit $\pm a$ (calibration, accuracy): $u = a/\sqrt{3}$. Reading resolution $r$: $u = r/\sqrt{12}$ (already included when you use the scatter of repeated readings).
* Sum or difference: $u_{x \pm y}^2 = u_x^2 + u_y^2$. Product or quotient: $(u_{xy}/xy)^2 = (u_x/x)^2 + (u_y/y)^2$. Power: $u_{x^k}/x^k = |k|\,u_x/x$.
* Mean of $N$ readings: $u = s/\sqrt{N}$ for the scatter, combined with any calibration term.
* Least-squares line $y = A_0 + A_1x$ through $N$ points: $s_{A_1} = s/\sqrt{\sum(x_i - \bar x)^2}$, with $s^2 = \sum(y_i - A_0 - A_1x_i)^2/(N-2)$ (LINEST in a spreadsheet).
* *Positions.* A position error $u_x$ changes an App. F factor $f$ by $(\partial f/\partial x)\,u_x$; evaluate the derivative numerically by changing $x$ by 0.1 mm.
* *A quantity from two equations (A3).* Solve with each input changed by its $u$ in turn and add the changes in quadrature.
* *Example.* Four micrometer readings of $h$ with $s$ = 0.0008 mm and accuracy ±0.003 mm: $u = \sqrt{0.0008^2/4 + 0.003^2/3}$ = 0.0018 mm, 0.03 % of 6.36 mm, and $3u_h/h$ = 0.09 % in $E$.
* Report $x \pm U$ with $U = 2u$. Round $U$ to one or two significant figures, and $x$ to the same decimal place.

## Appendix C — Using the simulation

Open `lab07_simulation.html` in any browser; it needs no internet connection. In **Beam**, choose the supports (pin and roller with an optional overhang, cantilever, propped cantilever, or fixed at both ends), the section and up to two point loads, a uniform load and an end couple. For a clamp, untick "Rigid clamp" to give it a rotational stiffness $k$; for the propped cantilever, set a settlement of the prop. The plots show the elastic curve (closed form, finite elements, and the App. F parts that add up to it) and the moment diagram. In **Large deflection**, set the strip and the tip load; tick "Include the strip's own weight" to add $\beta$. The **readout table** compares each closed-form result with the independent numerical solution: "agree" rows check the formulas, and "different models" rows show how far a formula is from a more complete model. **Push the model past its assumptions** runs prepared experiments. **Export (CSV)** saves the curves, the readout or the convergence study; if your browser blocks the download, the data appears in a box you can copy. The **SI / US customary** toggle converts every input and output.

## Appendix D — Derivations

**D.1 The elastic curve (Eqs. 1, 2).** Integrating Eq. 1 once gives $EI\,\theta = \int M\,dx + C_1$ and again $EI\,y = \iint M\,dx\,dx + C_1x + C_2$ (Beer Eqs. 9.5, 9.6). For a simple span with $P$ at $a$: $R_A = Pb/L$, and for $x \le a$, $M = Pbx/L$, so $EIy = Pbx^3/(6L) + C_1x + C_2$. $y(0) = 0$ gives $C_2 = 0$. In $a \le x \le L$, $M = Pbx/L - P(x - a)$; matching $y$ and $\theta$ at $x = a$ and setting $y(L) = 0$ gives $C_1 = -Pb(L^2 - b^2)/(6L)$, which is Eq. 2. Setting $dy/dx = 0$ gives the position of the largest deflection, $x_m = \sqrt{(L^2 - b^2)/3}$.

**D.2 Superposition and redundants (Eqs. 3, 5, 6).** If $y_1$ satisfies $EIy_1'' = M_1$ and $y_2$ satisfies $EIy_2'' = M_2$ with the same support conditions, $y_1 + y_2$ satisfies $EIy'' = M_1 + M_2$: Eq. 3. For the propped cantilever, remove the prop: under $P$ at $L/2$, App. F case 1 applied to the loaded half gives the tip deflection $-P(L/2)^2(3L - L/2)/(6EI) = -5PL^3/(48EI)$; an upward force $R_B$ at the tip gives $+R_BL^3/(3EI)$. Their sum is zero at the prop: $R_B = 5P/16$; then $M_A = PL/2 - R_BL = 3PL/16$. With the prop at $y = -\Delta$ instead, $R_BL^3/(3EI)$ must make up the difference, which gives Eq. 6.

**D.3 Reciprocity (Eq. 4).** Apply $P_1$ at point 1 and then $P_2$ at point 2. The work done is $\frac{1}{2}c_{11}P_1^2 + \frac{1}{2}c_{22}P_2^2 + c_{12}P_1P_2$, the last term being $P_1$ riding through the deflection that $P_2$ causes at point 1. In the reverse order the cross term is $c_{21}P_1P_2$. The stored energy cannot depend on the order, so $c_{12} = c_{21}$ (§11.6).

**D.4 The flexible clamp (Eqs. 7, 8).** The clamp carries $M_A$ and turns by $\theta_A = M_A/k$; the bar beyond it bends as a rigidly clamped cantilever and also turns rigidly by $\theta_A$, adding $\theta_Ax$ to the deflection. For a tip load, $M_A = PL$, which gives Eq. 7. With indicators at $x_1$, $x_2$, Eq. 7 is linear in $1/EI$ and $1/k$:
$c(x_i) = \frac{x_i^2(3L - x_i)}{6}\cdot\frac{1}{EI} + Lx_i\cdot\frac{1}{k}$, two equations for two unknowns. In the propped cantilever, $M_A = PL/2 - R_BL$ for a central load, and the tip condition becomes $-\frac{5PL^3}{48EI} + \frac{R_BL^3}{3EI} - \left(\frac{PL}{2} - R_BL\right)\frac{L}{k} = -\Delta$. Solving for $R_B$ with $\lambda = EI/(kL)$ gives Eq. 8.

**D.5 The elastica (Eq. 9).** With $\theta$ measured from the horizontal and $s$ from the clamp, $x' = \cos\theta$ and $y' = -\sin\theta$ (prime: $d/ds$). The moment of the tip load at $s$ is $P(x_{tip} - x)$, so $EI\theta' = P(x_{tip} - x)$ and, differentiating, $EI\theta'' = -P\cos\theta$, with $\theta(0) = 0$ and $\theta'(L) = 0$. Multiply by $\theta'$ and integrate: $\frac{1}{2}\theta'^2 = \frac{P}{EI}(\sin\theta_0 - \sin\theta)$. Substitute $1 + \sin\theta = 2k^2\sin^2\varphi$ with $2k^2 = 1 + \sin\theta_0$. Then $ds = (L/\sqrt{\alpha})\,d\varphi/\sqrt{1 - k^2\sin^2\varphi}$, and integrating from $\theta = 0$ ($\sin\varphi_1 = 1/(k\sqrt{2})$) to $\theta_0$ ($\varphi = \pi/2$) gives $L$ on the left and $(L/\sqrt\alpha)[K(k) - F(\varphi_1, k)]$ on the right: the first of Eqs. 9. Integrating $\sin\theta\,ds$ and $\cos\theta\,ds$ the same way gives $\delta_v$ and $x_{tip}$. For small $\alpha$, $\theta_0 \approx \alpha/2$ and $\delta_v/L \approx \alpha/3$ (Eq. 10). The strip's weight adds $w(L - s)\cos\theta$ to $EI\theta''$; there is no closed form, and the simulation integrates it numerically.

**D.6 The finite-element solver (`beam_deflection.cpp`).** Each element of length $h$ carries a cubic $y(x)$ fixed by the deflections and slopes at its two nodes (Hermite interpolation). An unloaded uniform beam segment bends exactly as a cubic ($EI\,y'''' = 0$), so the element stiffness $\frac{EI}{h^3}\begin{bmatrix}12 & 6h & -12 & 6h\\ 6h & 4h^2 & -6h & 2h^2\\ -12 & -6h & 12 & -6h\\ 6h & 2h^2 & -6h & 4h^2\end{bmatrix}$ is exact, and a distributed load becomes "consistent" nodal forces. Assembling $\mathbf{K}\mathbf{u} = \mathbf{F}$, locking $y$ at pins and rollers and $y$ and $\theta$ at fixed ends, and solving gives nodal values that are exact for a uniform beam. Between nodes, the cubic misses the quartic part of a distributed-load solution, an error of order $h^4$ in $y$ and $h^2$ in $y''$. The reactions are $(\mathbf{K}\mathbf{u} - \mathbf{F})$ in the equations of the locked unknowns. The simulation adds two things: a clamp with stiffness $k$ adds $k$ to the diagonal of its rotation unknown instead of locking it, and a settlement is a locked deflection with a nonzero value, moved to the right-hand side before solving.

## Appendix E — The elastica in numbers

| $\alpha = PL^2/EI$ | $\delta_v/L$ | $x_{tip}/L$ | $\theta_0$ (°) | Linear theory $\alpha/3$ |
|---:|---:|---:|---:|---:|
| 0.25 | 0.0827 | 0.9959 | 7.12 | 0.0833 |
| 0.5 | 0.1621 | 0.9841 | 14.01 | 0.1667 |
| 0.75 | 0.2356 | 0.9660 | 20.48 | 0.2500 |
| 1 | 0.3017 | 0.9436 | 26.43 | 0.3333 |
| 1.5 | 0.4110 | 0.8921 | 36.64 | 0.5000 |
| 2 | 0.4935 | 0.8394 | 44.79 | 0.6667 |
| 2.5 | 0.5557 | 0.7900 | 51.28 | 0.8333 |
| 3 | 0.6033 | 0.7456 | 56.49 | 1.0000 |
| 3.5 | 0.6404 | 0.7061 | 60.74 | 1.1667 |
| 4 | 0.6700 | 0.6711 | 64.24 | 1.3333 |
| 5 | 0.7138 | 0.6124 | 69.64 | 1.6667 |

: Table E1. Tip-loaded cantilever, large deflection (Eq. 9), without self-weight. Interpolate linearly between rows.

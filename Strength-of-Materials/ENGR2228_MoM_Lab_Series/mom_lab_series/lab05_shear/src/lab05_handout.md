# Lab 5 — Transverse Shear: Shearing Stress, Shear Deformation and Built-Up Beams

| | |
|---|---|
| **Course** | ENGR 2228 Mechanics of Materials |
| **When** | Week 10, after lectures on Beer 8e Ch. 6 |
| **Textbook** | Beer, Johnston, DeWolf, Mazurek, *Mechanics of Materials*, 8th ed. (Beer 8e): §6.1A–6.1C, §6.2, §6.3, §6.4; §2.8 for the relation among E, ν and G; §4.4 for composite sections |
| **Session** | 2 hours in the lab, teams of two; report due one week later |
| **Equipment** | Universal testing machine (capacity ≥ 50 kN) with a three-point bending fixture (span adjustable from 300 to 1200 mm), 12-channel strain-gage amplifier, displacement transducer (LVDT) on a deflection yoke, dial gage, calipers, micrometer, height gage; the Lab 4 aluminum bar with ±45° gage pairs, a 6061-T6 I-beam with web gage pairs, and three pairs of 50.8 × 12.7 mm 6061-T6 bars (loose, bolted, bonded) |
| **Files** | `lab05_simulation.html` (open in any browser, works offline), `sample_data.csv` |

## 1. Learning objectives

After this lab you will be able to:

1. Derive the shearing stress τ = VQ/(It) from equilibrium of part of a beam element, compute Q for common sections, and measure τ with ±45° strain-gage pairs (§6.1–6.2).
2. State when the elementary formula fails across a wide section, and quantify the error with the elasticity solution (§6.1C).
3. Measure the shear deformation of a short beam, separate it from bending, and recover both E and G from the same test (§2.8, §6.2).
4. Explain how the connection between the layers of a built-up beam controls its stiffness, predict the slip and the fastener forces, and compare the rigid-connection estimate F = qs with a model of flexible fasteners (§6.1A, §6.3).
5. Design the fastener spacing of a built-up beam against strength and deflection requirements using your own measured properties.

## 2. Theory

All three set-ups are three-point bending tests (Figure 1). Between a support and the central load the shear force is constant, V = P/2, and the bending moment grows linearly from zero; the gages sit in that region, at least two depths away from the load and the supports.

![Figure 1. The three test set-ups (schematic, not to scale). (a) The Lab 4 bar over 400 mm, upright and flat, with ±45° gage pairs at mid-height on its faces. (b) The I-beam, with web gage pairs at three heights and a deflection yoke; the span is changed from 300 to 1200 mm. (c) Two 50.8 × 12.7 mm bars over 600 mm, tested loose, bolted and bonded, with a dial gage for the slip at one end.](figures/fig1_setup.png){width=6.4in}

::: {custom-style="Callout"}
**Sign convention (Beer 8e).** Shear $V$ and moment $M$ follow Fig. 5.6 of the text: on the left part of a cut beam, $V$ acts downward on the cut face and $M$ acts counterclockwise; $M > 0$ sags the beam. On a cross-section, the shearing stress $\tau_{xy}$ is positive when it acts in $+y$ on a face whose outward normal is $+x$ (§1.4), so $V = -\int \tau_{xy}\,dA$: a positive $V$ produces $\tau_{xy} < 0$. Like Beer, we work with the magnitude $\tau = VQ/(It)$ and keep the sign only for the gage readings. Deflection $y$ is positive upward (Beer Ch. 9); we report the downward deflection $\delta = -y > 0$. Tension is positive.
:::

::: {custom-style="Callout"}
**Nomenclature.** $P$ central load; $L$ span; $V$ shear force; $M$ bending moment; $I$ moment of inertia about the neutral axis (NA); $A$ area; $Q$ first moment about the NA of the area above the level considered ($Q = A'\bar y'$); $t$ width of the section at that level; $q$ shear flow (force per unit length); $\tau$ shearing stress; $\gamma$ shear strain; $b$, $h$ width and depth of a rectangle; $c = h/2$; $B$, $H$, $t_f$, $t_w$ flange width, overall depth, flange and web thickness of the I-beam; $A_w = (H - 2t_f)t_w$ web area; $E$, $G$, $\nu$ elastic constants; $R$ ratio of the shearing stress at the faces of a rectangle to $VQ/(Ib)$; $f_s$ shear form factor; $\delta$ deflection; $s$ fastener spacing; $F$ fastener force; $k_b$ slip modulus of one bolt; $k$ connection stiffness per unit length; $t_1$, $t_2$ layer thicknesses; $r$ distance between the layer centroids; $EI_0$, $EI_{full}$ bending stiffness of the loose and fully composite beam; $EA^*$ combined axial stiffness of the two layers; $N$ axial force in a layer; $\alpha$, $\beta$ partial-interaction constants; $\eta$ degree of composite action; $u$ standard uncertainty; $U = 2u$ expanded uncertainty.
:::

Full derivations are in **Appendix D**; this section states each result, what it means, and when it stops applying.

### 2.1 Shear flow and shearing stress

Cut a short length $\Delta x$ of a beam along a plane parallel to the neutral surface (Figure 2a). The part above the cut carries the normal stresses from $M$ on one face and from $M + \Delta M$ on the other; they do not balance, so the cut must carry a horizontal force $\Delta H$. Per unit length of beam, this is the **shear flow** (§6.1A)

$$q = \frac{VQ}{I} \qquad (1)$$

where $Q$ is the first moment about the neutral axis of the area above the cut. Dividing by the width $t$ of the cut gives the average **shearing stress** on it, which by symmetry of stresses equals the average vertical shearing stress across the section at that level (§6.1B):

$$\tau = \frac{VQ}{It} \qquad (2)$$

![Figure 2. (a) The normal stresses on the part above a horizontal cut are unbalanced when the moment changes, so the cut carries a shear flow q. (b) In a rectangle τ is parabolic through the depth. (c) In an I-section τ is nearly uniform in the web and small in the flanges.](figures/fig2_shearflow.png){width=6.4in}

For a rectangle, $Q = \frac{b}{2}(c^2 - y^2)$ and

$$\tau = \frac{3V}{2A}\left(1 - \frac{y^2}{c^2}\right), \qquad \tau_{max} = \frac{3V}{2A} \qquad (3)$$

For a solid circle $\tau_{max} = 4V/(3A)$; in the web of an I-section the stress varies little, and $\tau \approx V/A_w$ (§6.1C):

$$\tau_{web} \approx \frac{V}{A_w}, \qquad A_w = (H - 2t_f)\,t_w \qquad (4)$$

A beam built from parts joined by bolts, nails or glue must transmit the shear flow across each joint (§6.1A). With fasteners at spacing $s$, each one carries

$$F = q\,s = \frac{VQ}{I}\,s \qquad (5)$$

where $Q$ is the first moment of the part that the joint connects to the rest of the section.

*Worked example.* A 30 mm × 90 mm rectangle carries $V$ = 12 kN: $A$ = 2700 mm², $\tau_{max}$ = 6.67 MPa at the neutral axis, 5.00 MPa at 22.5 mm above it.

*When Eqs. 1–5 apply:* elastic material; the section is symmetric about the plane of loading; the beam is prismatic; and the point is at least about one depth from a load or support. Equation 2 is an average across the width $t$; it is accurate when $t$ is small compared with the depth (§6.1C and Section 2.3).

### 2.2 Measuring shear strain

A shearing stress distorts a square element into a rhombus (Figure 3a): the diagonal at +45° lengthens and the one at −45° shortens, by half the shear strain each. A pair of gages at ±45° to the beam axis therefore measures (§2.8; Lab 8 derives it from the strain transformation)

$$\gamma_{xy} = \varepsilon(+45°) - \varepsilon(-45°), \qquad \tau = G\,|\gamma_{xy}| \qquad (6)$$

and any axial strain from bending, which both gages see equally, cancels. Averaging the pairs on opposite faces also cancels any twist from a slightly eccentric load.

![Figure 3. (a) Shear distorts a square: the +45° diagonal lengthens and the −45° one shortens, so their difference is the shear strain. (b) Across a wide rectangle the shearing stress on the neutral axis is not uniform: it is largest at the faces (curves for ν = 0.3).](figures/fig3_measure.png){width=6.2in}

### 2.3 Wide sections

Equation 2 averages the stress across the width. In a narrow rectangle the stress is nearly uniform, but the elasticity solution of the same problem shows that Poisson's effect makes it vary across the width: on the neutral axis it is largest at the faces and smallest at the center (Figure 3b; §6.1C, derivation in Appendix D.3):

$$\tau_{face} = R\left(\frac{b}{h}, \nu\right)\frac{VQ}{Ib} \qquad (7)$$

$R$ is within 1 % of 1 for $b/h \le 1/4$ and grows quickly beyond $b/h \approx 1$. The simulation computes $R$ in two independent ways.

### 2.4 Shear deformation

Shear strains also deflect the beam: they make adjacent cross-sections slide, tilting the axis without bending it (Figure 4a). Averaged over the section in the energy sense, the shear strain is $\gamma = f_sV/(GA)$, with the **shear form factor** (Appendix D.4)

$$f_s = \frac{A}{I^2}\int \frac{Q^2}{t}\,dy \qquad (8)$$

which is 6/5 for a rectangle, 10/9 for a circle, and roughly $A/A_w$ for an I-section. For a simple span with a central load (Timoshenko beam),

$$\delta = \frac{PL^3}{48EI} + \frac{f_s P L}{4GA} \qquad (9)$$

The first term is the familiar bending deflection (Ch. 9, Lab 7). The ratio of the two terms is $12f_sEI/(GAL^2)$: shear matters for short, deep beams and for sections with thin webs. Dividing Eq. 9 by $PL$ gives a straight line in $L^2$,

$$\frac{\delta}{PL} = \frac{L^2}{48EI} + \frac{f_s}{4GA} \qquad (10)$$

so tests at several spans give $E$ from the slope and $G$ from the intercept.

![Figure 4. (a) A beam deflects by bending, which rotates cross-sections, and by shear, which slides them. (b) Total deflection over bending deflection against span-to-depth ratio for a rectangle and a typical I-section (simple span, central load).](figures/fig4_timoshenko.png){width=6.2in}

*When Eqs. 8–10 apply:* elastic beam; the load and supports spread over at least a few millimeters, so that local indentation is negligible; span-to-depth ratio above about 3 (below that, the deformation near the load is not beam-like).

### 2.5 Built-up beams

Two equal layers that slide freely on each other (loose) bend independently: their stiffness is just the sum $EI_0 = E\sum b t_i^3/12$. Bonded rigidly, they act as one section of twice the depth: $EI_{full}$ is four times $EI_0$ (Figure 5). In general (Appendix D.5),

$$EI_0 = E\,\frac{b(t_1^3 + t_2^3)}{12}, \qquad EI_{full} = EI_0 + EA^* r^2, \qquad \frac{1}{EA^*} = \frac{1}{Ebt_1} + \frac{1}{Ebt_2} \qquad (11)$$

with $r = (t_1 + t_2)/2$ between the layer centroids. Real bolts deform a little under load, so the layers slip slightly at each bolt: a **partial interaction**. If the bolts (slip modulus $k_b$ each, spacing $s$) are smeared into a continuous connection of stiffness $k = k_b/s$ per unit length, the axial force $N$ that the connection builds up in each layer satisfies (Appendix D.5)

$$N'' - \alpha^2 N = -\beta M, \qquad \alpha^2 = k\left(\frac{1}{EA^*} + \frac{r^2}{EI_0}\right), \qquad \beta = \frac{kr}{EI_0} \qquad (12)$$

with $N = 0$ at the ends; the curvature is $(M - rN)/EI_0$. For a simple span with a central load, the solution gives the midspan deflection and the slip at the ends:

$$\delta = \frac{1}{EI_0}\left[\left(1 - \frac{r\beta}{\alpha^2}\right)\frac{PL^3}{48} + \frac{r\beta P}{2}\left(\frac{L}{2\alpha^4} - \frac{\tanh(\alpha L/2)}{\alpha^5}\right)\right], \qquad s_0 = \frac{rP}{2EI_0\alpha^2}\left[1 - \operatorname{sech}\frac{\alpha L}{2}\right] \qquad (13)$$

For a loose stack, $s_0 = rPL^2/(16EI_0)$; for a rigid bond, $s_0 = 0$ and $\delta = PL^3/(48EI_{full})$. The degree of composite action is

$$\eta = \frac{EI_{eff} - EI_0}{EI_{full} - EI_0} \qquad (14)$$

where $EI_{eff} = PL^3/(48\delta)$; it runs from 0 (loose) to 1 (rigid).

![Figure 5. Two equal layers. (a) Strain through the depth at midspan: loose layers slip at the interface, bonded layers do not. (b) Slip along the beam, relative to the loose end slip. (c) Effective stiffness against the connection parameter αL.](figures/fig5_layered.png){width=6.4in}

*When Eqs. 11–14 apply:* elastic layers that stay in contact (no uplift); for Eqs. 12–13, a connection that is uniform along the span or bolts close enough together to be smeared (spacing below about $1/\alpha$). Equation 5 assumes a rigid connection; with flexible bolts each bolt's force depends on the slip there, which the simulation's discrete-spring model computes.

### 2.6 The model in the simulation

`lab05_simulation.html` has three configurations. **Section** evaluates Eqs. 1–4 and 8 with exact layer formulas and checks them against a **strip integration** that slices the section into $N_s$ strips and adds up $A$, $I$ and $Q$; for a rectangle it computes $R$ of Eq. 7 from a series solution and from an independent **finite-difference** solution of the elasticity problem. **Shear deformation** compares Eq. 9 with a **finite-element** Timoshenko beam. **Built-up beam** compares Eqs. 12–13 with a **finite-difference** solution of Eq. 12, and with a model of **discrete bolts** in which each bolt is a spring of stiffness $k_b$. None of the numerical solutions uses the closed forms.

### 2.7 Uncertainty

Use standard uncertainties $u$; convert a limit $\pm a$ to $u = a/\sqrt{3}$; propagate to first order (Appendix B). In Part A you will fit $\tau = G|\gamma|$ against $V$; the ratio of the slope to the elementary value $3/(2A)$ is the measured $R$:

$$\left(\frac{u_R}{R}\right)^2 = \left(\frac{s_k}{k}\right)^2 + \left(\frac{u_G}{G}\right)^2 + u_{GF}^2 + \left(\frac{u_P}{P}\right)^2 + \left(\frac{u_b}{b}\right)^2 + \left(\frac{u_h}{h}\right)^2 \qquad (15)$$

where $k$ is the fitted slope with standard error $s_k$ and $u_{GF}$ is the relative uncertainty of the gage factor. Report $x \pm U$ with $U = 2u$ and draw error bars at $\pm U$. A measurement and a reference **agree** when

$$|x_{meas} - x_{ref}| \le 2\sqrt{u_{meas}^2 + u_{ref}^2} \qquad (16)$$

Any larger discrepancy needs a physical or procedural explanation, quantified where possible.

## 3. Pre-lab (due at the start of the session)

Answer on paper or in a short document. Show every step, units included. Use Table 1 and the nominal dimensions in Table 2.

**P1 — Estimate before you measure.** (a) Part A, bar upright at $P$ = 15 kN: find $V$, $\tau$ at the neutral axis from Eq. 3, the shear strain, and the expected difference $\varepsilon(+45°) - \varepsilon(-45°)$ in µε. What is the largest bending stress, and where? (b) Part B at $P$ = 20 kN on the 900 mm span: estimate $\tau$ in the web with Eq. 4 and the corresponding gage-pair difference. (c) Estimate the bending and shear parts of the midspan deflection of the I-beam at $P$ = 10 kN on the 300 mm and 1200 mm spans, taking $f_s \approx A/A_w$. Which term dominates at each span? (d) Part C at $P$ = 2 kN: the midspan deflection of the loose and of the bonded pair, and the loose end slip. Check the units of every answer.

**P2 — Q for the I-beam.** For the nominal I-beam, find $I$, then $Q$ and $\tau$ for $V$ = 10 kN (a) at the neutral axis, (b) in the web just below the flange, and (c) in the flange just above the web. Explain the jump between (b) and (c) with Eq. 1, and compare (a) with Eq. 4.

**P3 — Shear flow and bolts.** For the two bars bonded rigidly, find $q$ at the interface for $P$ = 2.5 kN (Eq. 1), the force per bolt at 100 mm spacing (Eq. 5), and the average shearing stress in a 6 mm bolt shank. For the loose pair, what force does the interface carry, and why is the pair four times less stiff?

**P4 — Gage pairs.** (a) Show with Figure 3a that a pure shear strain $\gamma$ lengthens the +45° diagonal by $\gamma/2$ and shortens the −45° one by the same amount, and that an axial strain $\varepsilon_x$ adds $\varepsilon_x(1 - \nu)/2$ to both. (b) In the left half of the span, what sign do you expect for $\varepsilon(+45°) - \varepsilon(-45°)$ with Beer's convention? (c) Why are the readings on opposite faces averaged?

**P5 — Predict with the simulation.** Open `lab05_simulation.html`. Record $R$ at the faces for the presets "Lab Part A: bar upright" and "Lab Part A: bar flat". For "Lab Part B: I-beam deflection", record the shear part of the deflection at spans of 300 and 1200 mm and the span at which it is 5 %. For "Lab Part C: two bars, six bolts", record the midspan deflection and end slip at 2.5 kN, then switch the connection to loose and to glue.

**P6 — Safety.** (a) List the hazards in this lab and how the procedure controls each. (b) Why are the load limits different for each part, and why is the flat bar loaded to only half the upright load?

| Material | $E$ (GPa) | $\nu$ | $G$ (GPa) | Strength (MPa) |
|---|---:|---:|---:|---:|
| 6061-T6 aluminum | 68.46 ± 0.47 (your Lab 2) | 0.330 ± 0.003 (your Lab 2) | 26.03 ± 0.12 (your Lab 3) | $\sigma_Y$ = 273.7 ± 1.0 (Lab 1); $\tau_Y$ = 150.8 ± 0.5 (Lab 3) |

: Table 1. Reference values. The ± values are standard uncertainties. Replace them with your own team's results where you have them.

## 4. Equipment and safety

| Item | Specification used in this handout |
|---|---|
| Testing machine | Capacity ≥ 50 kN; load accuracy ±0.5 % of reading |
| Three-point fixture | Rollers 25 mm in diameter; support span adjustable 300–1200 mm; central load nose with a 25 mm wide bearing plate |
| Strain gages and amplifier | 120 Ω foil gages, ±45° pairs (3 mm grids); gage factor ±1 %; resolution 1 µε |
| Deflection yoke and LVDT | Yoke resting on the bottom face over the supports; LVDT at midspan, resolution 0.001 mm, accuracy ±0.5 % of reading |
| Dial gage | Resolution 0.001 mm, for the end slip in Part C |
| Calipers / micrometer / height gage | Accuracy ±0.02 mm / ±0.003 mm / ±0.05 mm |
| Bar A (Part A) | The Lab 4 bar, 6061-T6, 25.4 × 50.8 × 700 mm, with a ±45° gage pair at the middle of each long face, all at one station |
| I-beam (Part B) | 6061-T6 extrusion, $H$ = 101.6 mm, $B$ = 76.2 mm, $t_f$ = 6.35 mm, $t_w$ = 4.76 mm (nominal), 1300 mm long; ±45° pairs on both sides of the web at 0, 22 and 41 mm above mid-depth |
| Bar pairs (Part C) | 6061-T6, 50.8 × 12.7 × 700 mm each: one pair loose (PTFE film between), one pair with six M6 shoulder bolts in reamed holes at 100 mm spacing, one pair bonded with structural epoxy |

: Table 2. Equipment. If your equipment differs, record its values and use them throughout.

::: {custom-style="Safety"}
**Safety.** Wear safety glasses while any load is on the fixture. **Load limits:** Part A upright 15 kN, flat 7.5 kN; Part B 20 kN on spans up to 900 mm and 15 kN on the 1200 mm span; Part C 2.0 kN loose, 2.5 kN bolted, 4.0 kN bonded. Set the overload stop about 10 % above each limit before every test. These limits keep the bending stress below about half the yield strength, and the bolt forces below the bolts' rated shear. **Pinch points:** keep fingers away from the rollers, the load nose and the yoke whenever the crosshead can move; jog it only with both hands on the controller. **Stability:** the flat bar and the stacked bars can roll or shift sideways on the rollers; center them and check that they sit square before loading, and stop at once if the load drops. **Instruments:** mount the yoke and the dial gage with the load at zero and the crosshead locked; never reach across a loaded specimen to adjust them. The I-beam weighs about 5 kg: carry it with two people.
:::

## 5. Procedure

1. **Measure.** Record $b$ and $h$ of bar A; $H$, $B$, $t_f$ (both flanges) and $t_w$ (with the micrometer) of the I-beam; $b$ and the thickness of each Part C bar; and the height of each web gage pair above the bottom of the I-beam. Write everything in Table 3. **Check:** repeated readings of each dimension should span no more than 0.03 mm (0.005 mm for $t_w$).
2. **Part A, upright.** Set the span to 400.0 mm with the bar upright and its gage station 100 mm from the left support. Zero the gages with no load. Load in 2.5 kN steps to 15 kN, holding 10 s at each step, then unload. **Check at 5 kN:** each gage pair should read nearly equal and opposite strains (difference near your P1 value), and the two faces should agree within about 10 %.
3. **Part A, flat.** Turn the bar onto its wide face, same span and station, and repeat in 1.25 kN steps to 7.5 kN, using the gage pairs on the narrow faces.
4. **Part B, web.** Set the span to 900 mm with the web gage station 225 mm from the left support. Load in 5 kN steps to 20 kN and unload. **Check at 10 kN:** the three heights should read within about 20 % of each other.
5. **Part B, spans.** Fit the yoke and LVDT. For spans of 300, 450, 600, 900 and 1200 mm, load in 5 kN steps to the limit and unload, recording the deflection at each step. **Check:** the deflection should return to zero within 0.002 mm.
6. **Part C.** Set the span to 600 mm. For the loose, bolted and bonded pairs in turn, fit the yoke and the dial gage at one end, load in 0.5 kN steps to the limit, and unload, recording the deflection and the end slip at each step. **Check:** the loose pair's slip at 1 kN should be close to your P1 estimate.
7. **Before you leave:** open the simulation, enter your measured dimensions in each Lab preset, and record its predictions in Table 5 next to your raw readings.

## 6. Data tables

```{=latex}
\renewcommand{\arraystretch}{1.9}
```

| Quantity | Readings | Mean |
|----------------------------------|------------------------------------------------|----------|
| Bar A $b$, $h$ (mm) | | |
| I-beam $H$, $B$ (mm) | | |
| I-beam $t_f$ (both flanges), $t_w$ (mm) | | |
| Web gage heights above the bottom (mm) | | — |
| Part C bars: $b$, $t$ of each bar (mm) | | |

: Table 3. Dimensions.

| Test | Load | Readings |
|------------------------------|----------|--------------------------------------------------------------|
| Part A upright: pairs on both faces (µε) | 7.5 kN | |
| Part A flat: pairs on both faces (µε) | 3.75 kN | |
| Part B web: three heights, both sides (µε) | 10 kN | |
| Part B: deflection at each span (mm) | 10 kN | |
| Part C: deflection / slip, loose, bolted, bonded (mm) | 2 kN | |

: Table 4. Spot readings for the checks in the procedure; the data system records every step.

| Quantity | Theory (equation) | Simulation | Measured ± U | Agree (Eq. 16)? |
|----------------------------------------|------------|------------|--------------|-----------|
| $R$, bar upright | Eq. 7 | | | |
| $R$, bar flat | Eq. 7 | | | |
| Web $\tau/V$ at the NA (1/mm²) | Eq. 2 | | | |
| $E$ from the span series (GPa) | Lab 2 | — | | |
| $G$ from the span series (GPa) | Lab 3 | — | | |
| Span with a 5 % shear part (mm) | Eq. 9 | | | |
| $EI_{eff}$, bonded / loose | Eq. 11 | | | |
| End slip, bolted (mm/kN) | Eq. 13 | | | |

: Table 5. Theory vs. simulation vs. measurement.

```{=latex}
\renewcommand{\arraystretch}{1.15}
```

## 7. Analysis

Every answer must (i) show at least two reasoning steps, (ii) include a dimensional check or a limiting-case check, and (iii) end with one to three sentences interpreting the result in words. Questions marked **[Core]** are required of everyone. **[Challenge]** questions are for students who want more. **[Extension]** questions are for honors and independent study.

**A1 [Core] — Shearing stress in a rectangle, narrow and wide.** For each orientation of bar A, compute $\gamma$ from each face's gage pair (Eq. 6), average the two faces, convert to $\tau$ with $G$ from Table 1, and fit $\tau$ against $V = P/2$ for the loading steps. Divide the slope by $3/(2A)$ to get the measured $R$, with its uncertainty from Eq. 15. Compare with the simulation's $R$ for your measured $b/h$ and $\nu$, using Eq. 16. Report the difference between the two faces as a fraction of their mean. *Check:* $R$ must approach 1 as $b/h \to 0$; is your upright value consistent with that? *Interpret:* by how much does $VQ/(Ib)$ underestimate the largest shearing stress in the flat bar, and why does the same bar give different answers in the two orientations?

**A2 [Core] — Shearing stress in the I-beam web.** For each of the three gage heights, average the two sides of the web, convert to $\tau$, and fit against $V$. Compare each slope with $Q/(It_w)$ for your measured section and with the approximation $1/A_w$ (Eq. 4). Plot the measured $\tau$ against height with the predicted profile. *Check:* the shear flow $q = \tau t$ must be continuous where the web meets the flange; use it to predict the (unmeasured) average vertical shearing stress in the flange. *Interpret:* why is the web stress so nearly uniform, and what fraction of $V$ does the web carry?

**A3 [Core] — E and G from the span series.** For each span, fit $\delta$ against $P$ to get the compliance $\delta/P$. Plot $\delta/(PL)$ against $L^2$ and fit a line (Eq. 10). From the slope find $E$, and from the intercept find $G$, using $f_s$ for your measured section from the simulation (Section mode, I-section). Propagate the uncertainties and compare $E$ with Lab 2 and $G$ with Lab 3. *Check:* units of slope and intercept. *Interpret:* which measurement constrains $G$ most, and why could you not get $G$ from the long spans alone?

**A4 [Core] — When does shear deformation matter?** For each span, report the shear part of the deflection as a fraction of the total, measured (intercept × $L$ over the compliance) and predicted (Eq. 9 with Table 1). Find the span at which the shear part is 5 %, from your fit and from Eq. 9, and express it as $L/H$. *Check:* the fraction must fall as $1/L^2$ at long spans. *Interpret:* by how much would Euler–Bernoulli theory ($PL^3/48EI$) have underestimated the deflection on the 300 mm span, and why is the I-beam affected more than a rectangle of the same depth?

**A5 [Core] — Loose, bolted and bonded.** For each Part C pair, fit $\delta$ against $P$, subtract the small shear term of Eq. 9 ($f_s$ = 6/5 for the whole section), and compute $EI_{eff} = L^3/(48\,\delta_{bend}/P)$. Report $EI_{eff}/EI_0$ for each pair and $\eta$ (Eq. 14), and compare the loose and bonded values with Eq. 11. For the loose pair, compare the measured end slip per newton with $rL^2/(16EI_0)$. *Check:* the bonded-to-loose ratio for two equal layers must be 4; derive it. *Interpret:* where does the factor of 4 come from physically?

**A6 [Core] — Bolts: slip modulus, slip and forces.** Using the simulation's discrete-bolt model (preset "Lab Part C", connection Bolts) with your measured dimensions and $E$, find the bolt slip modulus $k_b$ that reproduces your measured bolted deflection. With that $k_b$, predict the end slip and compare it with your measurement: this is an independent check of the model. Then report the largest bolt force at the largest load from the model and from Eq. 5 (rigid connection), and the shearing stress in the bonded pair's glue at its largest load. Repeat the fit with the smeared closed form (Eq. 13, $k = k_b/s$) and compare the two values of $k_b$. *Check:* the predicted end slip must lie between 0 and the loose value. *Interpret:* why does Eq. 5 overestimate the force in the bolt nearest the support, and which bolts carry the least?

**A7 [Core] — Theory vs. simulation vs. measurement.** Complete Table 5. Make one figure with error bars at $\pm U$ for each row, normalized by its theory value. Explain **every** discrepancy larger than the expanded uncertainty with a named cause, quantified where you can.

**M1 [Core] — Where does the model break?** (a) Run "A wide rectangle": how far above $VQ/(Ib)$ is the stress at the faces, and how does it compare with your A1 result? (b) Run "A deep, short I-beam": by what factor does Euler–Bernoulli theory underestimate the deflection? (c) In "Lab Part C", compare the largest bolt force from Eq. 5 with the discrete-spring value; then run "Few bolts" and compare the smeared and discrete deflections. When is smearing the bolts acceptable? (d) Run "Glue is not rigid": what glue stiffness would make the bonded pair noticeably less stiff than a rigid bond, and is your bonded pair in that range?

**C1 [Challenge] — The shear form factor.** Derive $f_s$ = 6/5 for a rectangle from Eq. 8. Compute $f_s$ for your I-beam by hand (Appendix D.4 gives the integrals) and compare it with the simulation and with $A/A_w$. Which approximation would you use, and how much would using $A/A_w$ instead change your $G$ in A3?

**C2 [Challenge] — Convergence.** For "Lab Part A: bar flat", record the finite-difference value of $R$ at 8, 16, 32 and 64 cells across the width. Show that the error falls as $N^{-2}$, Richardson-extrapolate, and compare with the series value. Then explain from the elasticity solution (Appendix D.3) why the effect vanishes when $\nu = 0$.

**C3 [Challenge] — Shear locking.** Run "Shear locking" and compare the finite-element deflection with the closed form for 4, 16 and 64 elements with full and with reduced integration. Explain why fully integrated linear elements are too stiff for slender beams, and why the error grows as the beam gets more slender.

**X1 [Extension] — Partial interaction.** Derive Eq. 12 from equilibrium of each layer and compatibility of the slip (Appendix D.5), and show that Eq. 13 reduces to the loose and rigid limits. Then show that $s_0$ for the loose case is $r$ times the end rotation.

**X2 [Extension] — Shear flow in the flanges.** In the I-beam's flange, the shear flow runs horizontally (§6.4). Show that it grows linearly from the flange tip to the web, find its value at the junction for $V$ = 10 kN, and show that the two flange halves together deliver to the web exactly the shear flow that Eq. 1 gives in the web there.

**X3 [Extension] — Adhesives.** Using the simulation, find the glue shear modulus at which the Part C bonded pair reaches $\eta$ = 0.95 for a 0.15 mm layer. Structural epoxies lose stiffness above about 60 °C and creep under sustained load. What does this mean for a bonded beam carrying a permanent load in a hot environment?

## 8. Design problem

**D1 — A bolted beam.** A walkway beam spanning 2.4 m (simply supported) is built from two 6061-T6 bars, 100 mm wide and 50 mm deep each, stacked to make a 100 × 100 mm section, and joined by M10 bolts in a single line along the middle of the width. It carries a uniform load of 8.0 kN/m (self-weight included). Requirements:

* every bolt's force from Eq. 5, $F = q\,s$, at no more than 10 kN, with $q$ evaluated at the bolt and $s$ the spacing in the zone where the bolt sits (the 10 kN already includes the factor of safety);
* midspan deflection no more than $L/300$, computed with the simulation's discrete-bolt model (preset "D1") using $k_b$ for an M10 bolt of $(10/6)$ times **your** M6 value from A6, and **your** measured $E$;
* bolts placed symmetrically, the first one at $s_1/2$ from each support; spacing $s_1$ within end zones of length $e$ and $s_2$ in the middle (a uniform spacing is the case $s_1 = s_2$).

Find the pattern with the fewest bolts. Compare it with the best uniform spacing, say which requirement governs, and compare the largest bolt force from Eq. 5 with the model's. Submit at most one page: the moment, shear and $q$ at the support, the required spacing near the supports, a table of the patterns you tried, the chosen pattern with both requirements checked, and one assumption that could invalidate your design (for example, the scaling of $k_b$ with bolt diameter), with how you would check it.

| Criterion | Weight |
|------------------------------------------------------------------------------|-------:|
| V, M and q correct; requirements translated into a spacing limit, units correct | 20 % |
| Measured $k_b$ and $E$ from **your** data used in the deflection check | 25 % |
| Every requirement checked for the final pattern; governing requirement identified | 20 % |
| Choice justified by a quantitative comparison of at least two patterns | 25 % |
| Clear one-page presentation; one critical assumption named and a check proposed | 10 % |

: Table 6. How D1 will be graded.

::: {.needspace lines="26"}
:::

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

: Table 7. Report grading. Extension questions are graded separately for honors and independent-study credit.

::: pagebreak
:::

## Appendix A — Running the lab without equipment

If the machine is unavailable, use `sample_data.csv`. It holds one row per load step:

| Column | Meaning |
|---|---|
| `part` | `A`, `B` or `C` |
| `config` | Part A: `upright` or `flat`; Part B: `web` or `deflection`; Part C: `loose`, `bolted` or `bonded` |
| `span_mm` | support span (mm) |
| `step` | load step number within the test, from 0 |
| `load_N` | central load $P$ (N), resolution 1 N |
| `defl_mm` | midspan deflection from the yoke, positive downward (mm), resolution 0.001 mm; blank where not measured |
| `slip_mm` | end slip between the Part C bars, magnitude (mm), resolution 0.001 mm |
| `gA_p45_ue`, `gA_m45_ue`, `gB_p45_ue`, `gB_m45_ue` | gage pairs, +45° and −45° (µε). Part A: front face (A) and back face (B). Part B web: at the neutral axis, front (A) and back (B) |
| `gC_p45_ue`, `gC_m45_ue`, `gD_p45_ue`, `gD_m45_ue` | Part B web, middle height, front (C) and back (D) |
| `gE_p45_ue`, `gE_m45_ue`, `gF_p45_ue`, `gF_m45_ue` | Part B web, highest pair, front (E) and back (F) |

: Table A1. Columns of `sample_data.csv`. The +45° gage of every pair points 45° counterclockwise from the beam axis as seen from the front; the back-face gages are mounted to measure the same two directions. Strains are zeroed at the start of each test.

The last row of each test is the return to zero load. Use these measurements:

| Quantity | Readings |
|---|---|
| Bar A $b$ / $h$ (mm) | 25.43, 25.41, 25.42 / 50.79, 50.77, 50.78 |
| Part A span / gage station from the left support (mm) | 400.0 / 100.0 |
| I-beam $H$ (mm) | 101.62, 101.58, 101.60 |
| I-beam $B$ (mm) | 76.19, 76.21, 76.22 |
| I-beam $t_f$ (mm) | 6.36, 6.34, 6.35, 6.36 |
| I-beam $t_w$ (mm) | 4.801, 4.797, 4.803 |
| Web gage heights above the bottom (mm) | 50.98, 73.17, 91.93 |
| Part B web span / gage station (mm) | 900.0 / 225.0 |
| Part C bars $b$ (mm) | 50.81, 50.83, 50.82 |
| Part C top bar / bottom bar $t$ (mm) | 12.71, 12.70, 12.72 / 12.69, 12.70, 12.68 |
| Part C span / bolt positions from the left support (mm) | 600.0 / 50, 150, 250, 350, 450, 550 |

: Table A2. Measurements for the sample data. Instrument accuracies are those of Table 2; spans are good to ±0.5 mm.

## Appendix B — Uncertainty quick reference

* Limit $\pm a$ (calibration, accuracy): $u = a/\sqrt{3}$. Reading resolution $r$: $u = r/\sqrt{12}$ (already included when you use the scatter of repeated readings).
* Sum or difference: $u_{x \pm y}^2 = u_x^2 + u_y^2$. Product or quotient: $(u_{xy}/xy)^2 = (u_x/x)^2 + (u_y/y)^2$. Power: $u_{x^k}/x^k = |k|\,u_x/x$.
* Mean of $N$ readings: $u = s/\sqrt{N}$ for the scatter, combined with any calibration term.
* Least-squares line $y = A_0 + A_1x$ through $N$ points: $s_{A_1} = s/\sqrt{\sum(x_i - \bar x)^2}$, $s_{A_0} = s\sqrt{\sum x_i^2/(N\sum(x_i - \bar x)^2)}$, with $s^2 = \sum(y_i - A_0 - A_1x_i)^2/(N-2)$ (LINEST in a spreadsheet).
* *A quantity from a fitted model (A6).* Change the measured input by its $u$, refit, and take the change in the output as its $u$.
* *Example.* Three micrometer readings of $t_w$ with $s$ = 0.003 mm and accuracy ±0.003 mm: $u = \sqrt{0.003^2/3 + 0.003^2/3}$ = 0.0024 mm, or 0.05 % of 4.80 mm.
* Report $x \pm U$ with $U = 2u$. Round $U$ to one or two significant figures, and $x$ to the same decimal place.

## Appendix C — Using the simulation

Open `lab05_simulation.html` in any browser; it needs no internet connection. Choose a configuration and a preset, then move the sliders. **Section** shows $\tau$ through the depth and, for a rectangle, across the width on the neutral axis; the number of strips and of finite-difference cells set the numerical resolution. **Shear deformation** shows how much shear adds to the deflection at every span and the deflected shape; the **shear term** toggle switches the elements between reduced and full integration. **Built-up beam** shows the slip along the beam and the stress through the depth at midspan; choose loose, bolts or glue, and for bolts set $k_b$, the two spacings and the end-zone length. The **readout table** compares each closed-form result with the independent numerical solution: "agree" rows check the formulas, and "different models" rows show how far a formula is from a more realistic model. **Push the model past its assumptions** runs prepared experiments. **Export (CSV)** saves the curves, the readout or the convergence study; if your browser blocks the download, the data appears in a box you can copy. The **SI / US customary** toggle converts every input and output.

## Appendix D — Derivations

**D.1 Shear flow and shearing stress (Eqs. 1–4).** Take the part of a beam element of length $\Delta x$ above a horizontal cut (Figure 2a). On its left face the normal stress is $\sigma = -My/I$, on its right face $-(M + \Delta M)y/I$. Horizontal equilibrium: $\Delta H = \int_{A'} \frac{\Delta M\,y}{I}\,dA = \frac{\Delta M}{I}Q$, where $Q = \int_{A'} y\,dA = A'\bar y'$. Dividing by $\Delta x$ and using $dM/dx = V$ gives $q = VQ/I$ (Eq. 1). The force $\Delta H$ acts on an area $t\,\Delta x$, so its average stress is $VQ/(It)$; because the shearing stresses on perpendicular planes are equal (§1.4), this is also the average of $\tau_{xy}$ across the width at that level (Eq. 2). For a rectangle, $Q = b(c - y)(c + y)/2$ and $I = bh^3/12 = 2bc^3/3$, which gives Eq. 3; $\tau_{max} = Vbc^2/(2It) = 3V/(2A)$. For a circle, $Q = \frac{2}{3}(c^2 - y^2)^{3/2}$ and $t = 2\sqrt{c^2 - y^2}$, so $\tau = V(c^2 - y^2)/(3I)$ and $\tau_{max} = 4V/(3A)$. In an I-section web, $Q$ changes only from $Bt_f(H - t_f)/2$ at the junction to that plus $t_w h_w^2/8$ at the neutral axis, with $h_w = H - 2t_f$, so $\tau$ is nearly constant and close to $V/A_w$ (Eq. 4).

**D.2 Gage pairs (Eq. 6).** A square element of side $a$ sheared by $\gamma$ has diagonals of length $a\sqrt{2}(1 \pm \gamma/2)$ to first order: the +45° diagonal stretches by $\gamma/2$ and the −45° one shortens by $\gamma/2$ (for $\gamma > 0$). An axial strain $\varepsilon_x$, with $\varepsilon_y = -\nu\varepsilon_x$, stretches both diagonals by $(\varepsilon_x + \varepsilon_y)/2$. So $\varepsilon(\pm45°) = \frac{1}{2}(\varepsilon_x + \varepsilon_y) \pm \frac{1}{2}\gamma$, and the difference is $\gamma$. A small twist adds equal and opposite shear strains on the two faces; the mean cancels it.

**D.3 The elasticity solution for a rectangle (Eq. 7).** Saint-Venant's solution for a prismatic bar bent by a constant shear force (Timoshenko and Goodier, *Theory of Elasticity*) keeps $\sigma_x = -My/I$ and adds shearing stresses that satisfy equilibrium and compatibility exactly. Writing them with a stress function $\phi$, the stress at height $y$ and position $z$ across the width is the elementary value plus $\partial\phi/\partial z$, where $\nabla^2\phi = \frac{\nu}{1+\nu}\frac{V}{I}z$ in the section and $\phi = 0$ on its edge. The right-hand side vanishes when $\nu = 0$: then the elementary formula is exact. A Fourier series for $\phi$ gives, on the neutral axis, $R = 1 + \frac{2}{c^2}\frac{\nu}{1+\nu}\sum_n \frac{c_n}{\alpha_n^2}\left[\frac{\alpha_n b}{2}\frac{\cosh(\alpha_n z)}{\sinh(\alpha_n b/2)} - 1\right]$ with $\alpha_n = (2n+1)\pi/h$ and $c_n = 4(-1)^n/[(2n+1)\pi]$. Integrated across the width, the correction is zero, so the width-average is always $VQ/(Ib)$.

**D.4 Shear deflection (Eqs. 8–10).** The strain energy of the shearing stresses per unit length of beam is $\int \frac{\tau^2}{2G}\,dA = \frac{V^2}{2GI^2}\int \frac{Q^2}{t}\,dy$, using $\tau = VQ/(It)$ and $dA = t\,dy$. Writing it as $\frac{1}{2}V\gamma$ with an average shear strain $\gamma = f_sV/(GA)$ defines Eq. 8. For a rectangle, $\int_{-c}^{c}\frac{b}{4}(c^2 - y^2)^2\,dy = \frac{4bc^5}{15}$, so $f_s = \frac{2bc}{(2bc^3/3)^2}\cdot\frac{4bc^5}{15} = \frac{6}{5}$. The shear strain tilts the axis: $dy_s/dx = -f_sV/(GA)$. For a simple span with a central load, $V = P/2$ over each half, so the midspan shear deflection is $f_s(P/2)(L/2)/(GA) = f_sPL/(4GA)$. Adding the bending deflection gives Eq. 9, and dividing by $PL$ gives Eq. 10. For an I-section, $\int Q^2/t\,dy$ is a sum of polynomial integrals over the flanges and the web.

**D.5 Partial interaction (Eqs. 11–14).** Let the bottom layer carry a tension $N$ and the top layer an equal compression, and let both have the curvature $\kappa$ (they stay in contact). Moment equilibrium of a section: $M = EI_0\kappa + Nr$, so $\kappa = (M - rN)/EI_0$. The slip $s$ is the difference between the longitudinal displacements of the two surfaces in contact; its rate is the difference of their strains, $s' = -N/EA^* + r\kappa$. The connection resists the slip with a shear flow $ks$, which changes the axial force in the bottom layer: $N' = -ks$. Differentiating and substituting gives $N'' = k(N/EA^* - r\kappa) = \alpha^2N - \beta M$ (Eq. 12). At free ends $N = 0$. For a central load, $M = Px/2$ on the left half, and by symmetry $N'(L/2) = 0$; the solution is $N = \frac{\beta}{\alpha^2}\frac{Px}{2} - \frac{\beta P}{2\alpha^3}\frac{\sinh\alpha x}{\cosh(\alpha L/2)}$. The midspan deflection is $\int_0^{L/2}\kappa\,x\,dx$ (unit-load method, or twice integrating $\kappa$), which gives Eq. 13; the end slip is $s_0 = -N'(0)/k$. With $k = 0$, $N = 0$ and $\kappa = M/EI_0$; with $k \to \infty$, $s \to 0$ and $N = r\kappa EA^*$, so $M = (EI_0 + EA^*r^2)\kappa$, which is Eq. 11.

**D.6 Bolts as springs.** Between two bolts there is no connection, so $N$ is constant and $s' = -N/EA^* + r(M - rN)/EI_0$ can be integrated directly. At a bolt, $N$ drops by the bolt force $k_b s$. Starting at $x = 0$ with $N = 0$ and an unknown slip, and requiring $N = 0$ again at $x = L$, fixes that slip. This is the simulation's discrete-bolt model; it reduces to Eq. 12 as the spacing shrinks with $k_b/s$ held fixed.

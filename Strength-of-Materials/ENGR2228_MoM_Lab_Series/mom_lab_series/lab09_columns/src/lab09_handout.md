# Lab 9 — Columns: Euler Buckling, End Conditions, Imperfections and the Secant Formula

| | |
|---|---|
| **Course** | ENGR 2228 Mechanics of Materials |
| **When** | Week 15, after lectures on Beer 8e Ch. 10 |
| **Textbook** | Beer, Johnston, DeWolf, Mazurek, *Mechanics of Materials*, 8th ed. (Beer 8e): §10.1 (stability, Euler's formula, effective length), §10.2 (eccentric loading, the secant formula), §10.3–10.4 (design of columns) |
| **Session** | 2 hours in the lab, teams of two; report due one week later |
| **Equipment** | Strut frame with a loading screw and a 5 kN load cell; knife-edge holders (V-grooves at 0, 1 and 2 mm offsets) and clamp blocks; dial gage; two strain gages per bar and an indicator; 6061-T6 bars 25.4 × 6.35 mm (the Lab 2 stock); 100 kN UTM for the Part D demonstration; micrometer, steel rule, surface plate |
| **Files** | `lab09_simulation.html` (open in any browser, works offline) and `sample_data.csv` |

```{=latex}
\renewcommand{\floatpagefraction}{0.8}\renewcommand{\topfraction}{0.85}\renewcommand{\textfraction}{0.1}
```

## 1. Learning objectives

After this lab you will be able to:

1. Predict the critical load of a column with Euler's formula and the effective length of its end conditions, and measure it (§10.1).
2. Extract the critical load and the initial imperfection of a real, crooked column from readings taken well below buckling, with a Southwell plot.
3. Measure how far real clamps are from "fixed", express it as a rotational stiffness, and use it to predict another test (§10.1B).
4. Predict the deflection and the maximum stress of an eccentrically loaded column with the secant formula, and show why superposition fails (§10.2).
5. Find where Euler's formula stops applying for short columns, and compare a short column's failure load with the tangent-modulus load and the design formulas (§10.3).
6. Design a strut for centric and eccentric loads, applying the factor of safety to the load (§10.2–10.4).

## 2. Theory

The set-up is shown in Figure 1. A screw pushes down on a bar standing between two supports; a load cell under the bottom support reads the load $P$, a dial gage reads the lateral deflection at mid-length, and two strain gages, one on each wide face at mid-length, read the bending. In Parts A and C the bar's ends sit in knife-edge V-grooves (pinned ends); in Part B they are gripped in clamp blocks.

![Figure 1. Test set-up (schematic). (a) The strut frame with pinned ends: knife edges in V-blocks under the loading screw and on the load cell; the dial gage and the front and back strain gages at mid-length; Beer's axes, x down the column from end A and y lateral. (b) The end fixtures: a knife-edge holder with V-grooves at 0, 1 and 2 mm from the axis, and a clamp block that grips 40 mm of the bar. (c) The 25.4 × 6.35 mm section, which bends across its thickness t; the front gage F is on the convex face.](figures/fig1_setup.png){width=6.4in}

::: {.needspace lines="12"}
:::

::: {custom-style="Callout"}
**Sign convention (Beer 8e).** The axial load $P$ is compressive and is reported as a positive magnitude. Following Beer (§10.1A, Fig. 10.7), $x$ runs along the column from the top end A and $y$ is the lateral deflection; the elastic curve obeys $EI\,y'' = M$ with $M = -Py$ for a centric load (Eq. 10.4) and $M = -P(y + e)$ for a load applied at distance $e$ from the axis (Eq. 10.22). The column bows away from the line of the load, so the lever arm of the load at mid-length is $e + y_{max}$ (Fig. 10.23). We measure the initial bow $\delta_0$ in the same direction as the bowing, and $\delta$ is the **change** of the mid-length deflection from the no-load reading, which is what the dial gage reads. Strains are positive in tension; the **front** face is the convex one, where bending adds tension.
:::

::: {.needspace lines="12"}
:::

::: {custom-style="Callout"}
**Nomenclature.** $P$ axial load (compression, magnitude); $P_{cr}$ critical load; $\sigma_{cr} = P_{cr}/A$ critical stress; $E$ modulus of elasticity; $E_t$ tangent modulus; $I$ smaller moment of inertia of the section; $A$ area; $r = \sqrt{I/A}$ radius of gyration; $c$ distance from the neutral axis to the extreme fiber; $b$, $t$ width and thickness of the bar; $L$ length between the supports; $K$ effective-length factor; $L_e = KL$ effective length; $L_e/r$ effective slenderness ratio; $k$ rotational stiffness of an end (moment per unit rotation); $p = \sqrt{P/EI}$; $y$ lateral deflection; $y_{max}$ its value at mid-length; $\delta_0$ initial bow at mid-length; $\delta$ change of mid-length deflection; $\alpha = P/P_{cr}$ load ratio; $e$ eccentricity of the load; $\sigma_{max}$ largest compressive stress; $\sigma_Y$ yield strength; $m$ Ramberg–Osgood exponent (fitted to the Lab 1 curve); F.S. factor of safety; $u$ standard uncertainty; $U = 2u$ expanded uncertainty.
:::

Full derivations are in **Appendix D**; this section states each result, what it means, and when it stops applying.

### 2.1 Euler's formula and the effective length

A straight, centrally loaded, elastic column stays straight until the load reaches the value at which a bent shape is also in equilibrium (§10.1A). For a column of length $L$ pinned at both ends this is Euler's formula; for other end conditions $L$ is replaced by the effective length $L_e = KL$, the length of the equivalent pinned column (Beer Eqs. 10.11b, 10.13b, Fig. 10.18):

$$P_{cr} = \frac{\pi^2EI}{L_e^2} \qquad (1)$$

$$\sigma_{cr} = \frac{P_{cr}}{A} = \frac{\pi^2E}{(L_e/r)^2} \qquad (2)$$

Use the smaller moment of inertia: the bar of Figure 1c buckles across its 6.35 mm thickness, with $r = t/\sqrt{12}$. The effective length runs between points of zero bending moment (Figure 2): $K = 1$ for pinned ends, 0.699 for one pinned and one fixed end (Beer Eqs. 10.19–10.21), 0.5 for two fixed ends and 2 for a free top on a fixed base.

![Figure 2. The first buckling mode for five sets of end conditions, from this lab's closed-form solutions. Purple dots: points of zero moment; purple brackets: the effective length. The last column has clamps of finite stiffness, kL/EI = 45, as found in Part B: its K lies between the pinned and fixed values.](figures/fig2_ends.png){width=5.2in}

**Real clamps.** A clamp is not infinitely stiff: it lets the end turn a little under the end moment, $M = k\theta$. For two equal clamps of stiffness $k$ (each end laterally held), the buckled column satisfies (Appendix D.3)

$$\tan\frac{pL}{2} = -\frac{2EI}{kL}\,\frac{pL}{2}, \qquad p^2 = \frac{P_{cr}}{EI} \qquad (3)$$

and with a clamp at one end and a pin at the other,

$$\tan pL = \frac{pL}{1 + (pL)^2\,EI/(kL)} \qquad (4)$$

Equation 3 gives $K = \pi/(pL)$ between 0.5 ($kL/EI \to \infty$) and 1 ($k = 0$); Eq. 4 gives $K$ between 0.699 and 1. Solve them numerically (a few steps of bisection) or with the simulation. From a measured $P_{cr}$, Eq. 3 can be solved for $k$ directly (Appendix D.3).

### 2.2 Imperfect columns and the Southwell plot

No real column is straight. If the bar has an initial bow $\delta_0 \sin(\pi x/L)$, it deflects from the start of loading, and the change of the mid-length deflection is (Appendix D.4)

$$\delta = \delta_0\,\frac{\alpha}{1 - \alpha}, \qquad \alpha = \frac{P}{P_{cr}} \qquad (5)$$

The deflection grows without limit as $P$ approaches $P_{cr}$ (Figure 3a): a real column never shows a sharp buckling load, so we do not load it to $P_{cr}$. Rearranging Eq. 5 gives a straight line (Southwell's construction, Appendix D.5):

$$\frac{\delta}{P} = \frac{\delta}{P_{cr}} + \frac{\delta_0}{P_{cr}} \qquad (6)$$

Plot $\delta/P$ against $\delta$ for readings above about half the critical load: the inverse of the slope is $P_{cr}$ and the intercept on the $\delta/P$ axis is $\delta_0/P_{cr}$ (Figure 3b). A small offset $e$ of the load line at the knife edges acts like an extra bow of about $(4/\pi)e$, so Southwell's $\delta_0$ is the bow **plus** the knife edges' offset.

![Figure 3. Imperfect columns, in nondimensional form. (a) Load ratio against deflection for a bowed column (Eq. 5), for a column loaded at an offset e (Eq. 7) and for the perfect column. (b) The bowed column's readings plotted as δ/P against δ fall on a straight line: slope 1/P_cr, intercept δ0/P_cr.](figures/fig3_southwell.png){width=6.4in}

### 2.3 Eccentric loads and the secant formula

A load applied at distance $e$ from the axis (Part C) bends the column from the start. The maximum deflection and the largest compressive stress are (Beer Eqs. 10.31 and 10.36, Appendix D.6)

$$y_{max} = e\left[\sec\left(\frac{\pi}{2}\sqrt{\frac{P}{P_{cr}}}\right) - 1\right] \qquad (7)$$

$$\sigma_{max} = \frac{P}{A}\left[1 + \frac{ec}{r^2}\sec\left(\frac{1}{2}\sqrt{\frac{P}{EA}}\,\frac{L_e}{r}\right)\right] \qquad (8)$$

Equation 8 is the **secant formula**. The moment at mid-length is $P(e + y_{max})$, and $y_{max}$ itself grows with $P$, so $\sigma_{max}$ is not proportional to $P$ (Figure 4a). Superposition therefore fails: you cannot add the stresses of several loads, and a factor of safety must be applied to the **load** (find the load that makes $\sigma_{max} = \sigma_Y$, then divide by F.S.), not to the stress. Setting the secant to 1 recovers Beer's Eq. 10.37, $P/A = \sigma_Y/(1 + ec/r^2)$, the eccentric-load result of §4.7 with no deflection, which is acceptable only for short columns (Figure 4b).

![Figure 4. (a) The lever arm of an eccentric load at mid-length, divided by e, against P/P_cr: the secant result, the simpler amplification 1/(1 − α), and the constant value that superposition without deflection assumes. (b) For 6061-T6, the load at first yield divided by P_cr against the eccentricity ratio ec/r², from the secant formula (thick) and from Eq. 10.37 (thin), for L_e/r = 50, 100 and 250.](figures/fig4_eccentric.png){width=6.4in}

### 2.4 Short columns

Equation 2 has no upper limit: below $L_e/r = \pi\sqrt{E/\sigma_Y}$ (about 50 for 6061-T6) it predicts a critical stress above the yield strength. A short column starts to yield before it buckles elastically, and once the material is on the curved part of its stress–strain curve it is less stiff than $E$. Engesser's **tangent-modulus** load replaces $E$ in Eq. 2 by the slope $E_t = d\sigma/d\varepsilon$ of the stress–strain curve at the critical stress (Appendix D.7). With a Ramberg–Osgood fit to the Lab 1 curve, $\varepsilon = \sigma/E + 0.002(\sigma/\sigma_Y)^m$ ($m$ in Table 1; the same appendix shows how to fit it):

$$\sigma_t = \frac{\pi^2E_t(\sigma_t)}{(L_e/r)^2}, \qquad \frac{1}{E_t} = \frac{1}{E} + \frac{0.002\,m}{\sigma_Y}\left(\frac{\sigma}{\sigma_Y}\right)^{m-1} \qquad (9)$$

Equation 9 is implicit in $\sigma_t$: solve it by trial, or pick $\sigma$ and compute the slenderness at which it is critical, $L_e/r = \pi\sqrt{E_t/\sigma}$. Real columns, with small imperfections, fail somewhat below the tangent-modulus load. The design formulas of §10.3 (for 6061-T6, Beer Eqs. 10.43b–10.45b) follow this column curve with a factor of safety built in; their long-column branch is Euler's curve divided by about 1.9 (Figure 5).

![Figure 5. Column curve for 6061-T6: Euler's hyperbola, the tangent- and reduced-modulus curves from Lab 1's stress–strain curve, and the Aluminum Association allowable stress. Ticks along the bottom mark the slenderness of this lab's tests (the clamped tests at their ideal effective lengths).](figures/fig5_curve.png){width=6.4in}

*When Eqs. 1–9 apply:* Eqs. 1–4 need a straight, centrally loaded, linear-elastic column with $\sigma_{cr} < \sigma_Y$, and Eqs. 1 and 3–4 assume the ends are held laterally; Eqs. 5–8 add small deflections ($y''$ for the curvature) and the first buckling mode for the bow; all of them hold only below the proportional limit. The Southwell plot needs readings in which the first mode dominates (above about $0.5P_{cr}$).

### 2.5 The model in the simulation

`lab09_simulation.html` has three configurations. **Buckling load** computes $P_{cr}$ and the buckled shape for any end condition, including rotational springs, and places the column on the column curve. **Imperfect and eccentric** draws the load–deflection curve for a bow $\delta_0$ and an offset $e$, the elastica past $P_{cr}$, and a Southwell plot of simulated readings and of the sample data. **Short columns** compares Euler, the tangent- and reduced-modulus loads and an imperfect inelastic column. Each closed form is checked against an independent numerical method: Hermite finite elements solved by inverse iteration for $P_{cr}$, the same elements loaded with the bow and the end offsets, a finite-difference beam-column, RK4 shooting for the elastica, and a fiber model of the section.

### 2.6 Uncertainty

Use standard uncertainties $u$; convert a limit $\pm a$ to $u = a/\sqrt{3}$; propagate to first order (Appendix B). For the Euler prediction of a rectangular bar ($I = bt^3/12$),

$$\left(\frac{u_P}{P_{cr}}\right)^2 = \left(\frac{u_E}{E}\right)^2 + \left(\frac{3u_t}{t}\right)^2 + \left(\frac{u_b}{b}\right)^2 + \left(\frac{2u_L}{L}\right)^2 \qquad (10)$$

The Southwell $P_{cr}$ is the inverse slope of a least-squares line; combine the slope's statistical uncertainty with the load-cell calibration. Report $x \pm U$ with $U = 2u$ and draw error bars at $\pm U$. A measurement and a prediction **agree** when

$$|x_{meas} - x_{pred}| \le 2\sqrt{u_{meas}^2 + u_{pred}^2} \qquad (11)$$

Any larger discrepancy needs a physical or procedural explanation, quantified where possible.

## 3. Pre-lab (due at the start of the session)

Answer on paper or in a short document. Show every step, units included. Use Table 1 and the nominal 25.4 × 6.35 mm section.

**P1 — Estimate before you measure.** (a) Find $A$, $I$ and $r$, and then $L/r$, $P_{cr}$ (Eq. 1) and $\sigma_{cr}$ for the pinned bars of 300, 450 and 600 mm. (b) Find $P_{cr}$ for the 600 mm bar with both ends fixed and for the 640 mm bar with one end fixed and one pinned (Beer's ideal $K$). (c) For the 90 mm bar of Part D, pinned, find Euler's $P_{cr}$ and $\sigma_{cr}$ and the load $\sigma_YA$. Which does the bar reach first? (d) A 450 mm bar has a bow of 0.5 mm: what will the dial read at $0.5P_{cr}$, $0.75P_{cr}$ and $0.9P_{cr}$ (Eq. 5)? Check the units of every answer.

**P2 — Same load, different columns.** Show that the 300 mm pinned bar and the 600 mm fixed–fixed bar have the same ideal $P_{cr}$. Which do you expect to buckle at the lower load in the lab, and why?

**P3 — A Southwell plot by hand.** A bowed pinned bar gives these readings: 900 N, 0.50 mm; 1200 N, 1.00 mm; 1500 N, 2.50 mm; 1650 N, 5.50 mm. Plot $\delta/P$ against $\delta$, fit a line, and find $P_{cr}$ and $\delta_0$ (Eq. 6). Which reading would you trust least, and why does the method not need a reading near $P_{cr}$?

**P4 — An eccentric load.** For the 450 mm bar with $e$ = 2 mm at $P = 0.5P_{cr}$ (your P1 value), find $y_{max}$ (Eq. 7), the moment at mid-length and $\sigma_{max}$ (Eq. 8). Compare $\sigma_{max}$ with the value you would get if the bar did not deflect ($y_{max} = 0$). By what factor has the deflection increased the bending stress?

**P5 — Predict with the simulation.** Open `lab09_simulation.html`. For "Lab Part A: pinned, 450 mm", record the closed-form and finite-element $P_{cr}$. Switch the ends to "rotational springs" with $k$ = 2800 N·m/rad and $L$ = 600.5 mm and record $P_{cr}$ and $K$. For "Lab Part C: eccentric, e = 2 mm", record the first-yield load from the readout. For "Lab Part D", record the Euler, tangent-modulus and fiber-model loads.

**P6 — Safety.** (a) List the hazards in this lab and how the procedure controls each. (b) Why do we stop at a lateral deflection of $L/60$? For the 300 mm bar near $P_{cr}$ with a bow of 0.3 mm, find the largest stress at $\delta$ = 5 mm, $\sigma = P/A + P(\delta_0 + \delta)c/I$, and compare it with $\sigma_Y$.

| Property of the 6061-T6 bar | Value |
|---|---:|
| $E$ (GPa) | 68.46 ± 0.47 (your Lab 2) |
| Yield strength $\sigma_Y$ (MPa) | 273.7 ± 1.0 (your Lab 1) |
| Ramberg–Osgood exponent $m$ | 17 (fit to the Lab 1 curve, Appendix D.7) |

: Table 1. Reference values. The ± values are standard uncertainties. Replace them with your own team's results where you have them; Lab 2 measured this same bar stock.

```{=latex}
\clearpage
```

## 4. Equipment and safety

| Item | Specification used in this handout |
|---|---|
| Bars | 6061-T6, 25.4 × 6.35 mm (1 × 0.25 in): pinned bars 300, 450 and 600 mm between pivots, each with a strain gage on both wide faces at mid-length; one 680 mm bar with gages for Part B; one 90 mm bar for Part D |
| Strut frame | Loading screw turned by hand; 5 kN load cell (±0.5 % of reading) under the bottom support |
| End fixtures | Knife-edge holders with V-grooves on the axis and at 1.00 and 2.00 mm from it (±0.02 mm); clamp blocks gripping 40 mm of the bar, bolts torqued to 20 N·m |
| Deflection | Dial gage at mid-length, 0.01 mm divisions, ±0.01 mm |
| Strain gages | Gage factor 2.10 ± 0.5 %, quarter bridge, indicator resolution 1 µε |
| Part D | 100 kN UTM (±0.5 % of reading) with hardened V-block seats, a polycarbonate shield and a dial gage at mid-length |
| Instruments | Micrometer ±0.003 mm; steel rule ±0.5 mm; surface plate and dial gage for the initial bow |

: Table 2. Equipment. If your equipment differs, record its values and use them throughout.

::: {custom-style="Safety"}
**Safety.** Wear safety glasses throughout. **Limits:** in the strut frame, stop at a lateral deflection of $L/60$ (5.0, 7.5 and 10 mm for the 300, 450 and 600 mm bars) and never above 5 kN; these keep the largest stress below about 55 % of $\sigma_Y$, so every bar is reused. **Stored energy:** a loaded column can kick sideways if it slips off a knife edge; seat both ends before loading, keep the guard in place, and keep hands out of the frame while it carries load. Unload by backing off the screw before touching the bar or the dial gage. **Part D** is an instructor demonstration in the UTM behind the shield; stand back at least 1 m.
:::

## 5. Procedure

1. **Measure.** Record $b$ and $t$ of each bar (micrometer, four places), the distance between pivots or clamp faces (rule), and the initial bow: set the bar on two equal blocks near its ends on the surface plate and read the dial gage at mid-length relative to the ends, then turn the bar over and repeat; the bow is half the difference. Mark the convex face "F" (front). Write everything in Table 3. **Check:** the four readings of $t$ should span no more than 0.01 mm; bows of a few tenths of a millimeter are normal.
2. **Connect and zero.** Connect the front and back gages, set the gage factor to 2.10 and zero with the bar unloaded.
3. **Part A.** Seat the 300 mm bar in the central V-grooves with its front face toward the dial gage. Zero the dial. Load in 250 N steps, recording load, dial and both gages, up to 75 % of your P1 load; then turn the screw in steps that move the dial by $L/600$ (0.50 mm) and record the load at each, until the dial reads $L/60$ (5.0 mm). Unload. Repeat for the 450 mm bar (100 N steps, then 0.75 mm steps to 7.5 mm) and the 600 mm bar (50 N steps, then 1.00 mm steps to 10.0 mm). **Check:** at half your P1 load the dial should read roughly the measured bow, or a little more (Eq. 5 with $\alpha$ = 0.5), and in the last steps the load should hardly rise. The front gage turns from compression to tension when the bow plus the dial reading reaches about $r^2/c = t/6$ = 1.06 mm, the edge of the section's kern (Lab 6).
4. **Part B.** Grip the 680 mm bar in the clamp blocks, 40 mm at each end (600 mm free length), front face toward the dial. Load in 250 N steps up to 3000 N, then in 1.00 mm deflection steps to 10.0 mm. Then replace the top clamp by a knife edge (640 mm from the bottom clamp face to the pivot) and repeat with 100 N steps up to 1300 N and 1.07 mm deflection steps to 10.7 mm. **Check:** the fixed–fixed load levels off **below** your P1(b) value.
5. **Part C.** Seat the 450 mm bar in the grooves 1.00 mm off the axis at both ends, on the side opposite the front face, so that the offset and the bow add. Load in 100 N steps, at the same loads as in Part A, until the dial reads 7.5 mm (switch to 0.75 mm deflection steps above 1300 N if you get there). Repeat with the 2.00 mm grooves. **Check:** at 600 N the dial reads about 0.9 mm (e = 1 mm) and 1.5 mm (e = 2 mm), against about 0.26 mm in Part A.
6. **Part D (instructor demonstration).** The 90 mm bar is loaded in the UTM between V-block seats at 0.5 mm/min with a dial gage at mid-length. Record the load at 4 kN steps, then the load at every 0.05 mm of lateral deflection, through the maximum and until the load has fallen by 15 %. Record the maximum load.
7. **Before you leave:** open the simulation, enter your measured dimensions and lengths in the Lab presets, and record its predictions in Table 5 next to your raw readings.

::: {.needspace lines="18"}
:::

## 6. Data tables

```{=latex}
\renewcommand{\arraystretch}{1.9}
```

| Quantity | Readings | Mean |
|----------------------------------|------------------------------------------------|----------|
| $b$ (mm) | | |
| $t$ (mm) | | |
| Lengths (mm): A 300, 450, 600; B 600, 640; D 90 | | — |
| Initial bows (mm): A 300, 450, 600; B; D | | — |

: Table 3. Dimensions.

::: {.needspace lines="14"}
:::

| Test | Load | Dial (mm), front and back strains (µε) |
|------------------------------|--------------|--------------------------------------------------------------|
| Part A, 300 mm | 2000 N | |
| Part A, 450 mm | 900 N | |
| Part A, 600 mm | 500 N | |
| Part B, fixed–fixed | 2000 N | |
| Part B, fixed–pinned | 900 N | |
| Part C, e = 1 mm and 2 mm | 600 N | |
| Part D | maximum | |

: Table 4. Spot readings for the checks in the procedure; record every step on a separate sheet.

::: {.needspace lines="24"}
:::

| Quantity | Theory (equation) | Simulation | Measured ± U | Agree (Eq. 11)? |
|----------------------------------------|------------|------------|--------------|-----------|
| $P_{cr}$, pinned, 300 / 450 / 600 mm (N) | Eq. 1 | | | |
| $E$ from the Southwell loads (GPa) | Lab 2 | — | | |
| $E$ from the axial strain (GPa) | Lab 2 | — | | |
| $K$, fixed–fixed, 600 mm | 0.5 (Fig. 10.18) | | | |
| $P_{cr}$, fixed–pinned, 640 mm (N) | Eq. 4 with your $k$ | | | |
| Eccentricity from Part C (mm) | 1.00, 2.00 | — | | |
| Maximum load, Part D (kN) | Eq. 9 | | | |

: Table 5. Theory vs. simulation vs. measurement.

```{=latex}
\renewcommand{\arraystretch}{1.15}
```

## 7. Analysis

Every answer must (i) show at least two reasoning steps, (ii) include a dimensional check or a limiting-case check, and (iii) end with one to three sentences interpreting the result in words. Questions marked **[Core]** are required of everyone. **[Challenge]** questions are for students who want more. **[Extension]** questions are for honors and independent study.

**A1 [Core] — Euler's formula, measured without buckling the bar.** For each Part A bar, make a Southwell plot (Eq. 6) from the readings above half your P1 load and find $P_{cr}$ and $\delta_0$ with uncertainties. Compare $P_{cr}$ with Eq. 1 using Table 1's $E$, your section and your lengths (Eqs. 10, 11). Plot $\log P_{cr}$ against $\log L$ and find the slope. From each $P_{cr}$ find $E = P_{cr}L^2/(\pi^2I)$ and compare the mean with Lab 2. *Check:* Euler's formula predicts a slope of exactly −2. *Interpret:* why is Southwell's $\delta_0$ larger than the bow you measured on the surface plate, and what does the difference tell you about the knife edges?

**A2 [Core] — How fixed is a clamp?** From the Part B readings find $P_{cr}$ for the fixed–fixed and the fixed–pinned tests (Southwell) and their effective-length factors $K = (\pi/L)\sqrt{EI/P_{cr}}$. Compare each with Beer's ideal value (Eq. 11). Find the clamp stiffness $k$ from the fixed–fixed result (Eq. 3, Appendix D.3), then use it in Eq. 4 to predict the fixed–pinned $P_{cr}$, and compare with the measurement. *Check:* Eq. 3 must return $K$ = 0.5 for $k \to \infty$. *Interpret:* by how much would a designer who assumed fixed ends overestimate the capacity of this column?

**A3 [Core] — Eccentric load.** At each Part C load, subtract the Part A reading of the 450 mm bar at the same load: the difference is the deflection caused by the groove offset alone (at a fixed load the response is linear in the imperfections, Appendix D.4). Fit $e$ in Eq. 7, with $P_{cr}$ from A1, and compare it with the groove offsets. From the change of bending strain, $(\varepsilon_F - \varepsilon_B)/2$, find the change of the moment at mid-length and divide by $P$ to get the change of the lever arm; compare it with $e$ plus the change of deflection (Beer Fig. 10.23). *Check:* for small $P$, Eq. 7 gives $y_{max} \approx (\pi^2/8)e\,P/P_{cr}$. *Interpret:* compare the deflection at 1200 N with twice that at 600 N. What does this say about adding the effects of several loads?

**A4 [Core] — The secant formula as a design tool.** With $P_{cr}$ from A1 (in Eq. 8, $\pi^2EA/(L_e/r)^2 = P_{cr}$) and your Lab 1 $\sigma_Y$, find the load that first yields the 450 mm bar for $e$ = 1 mm and 2 mm, and the load Eq. 10.37 gives if deflection is ignored. At the largest Part C load common to both tests, compare the measured stress at the back face, $-E\varepsilon_B$, with Eq. 8 for the groove offset alone and with Eq. 8 plus the Part A stress at the same load. *Check:* as $e \to 0$ the first-yield load must approach the smaller of $P_{cr}$ and $\sigma_YA$. *Interpret:* why must a factor of safety divide the load, not the stress?

**A5 [Core] — The short column and the column curve.** For Part D, compare the maximum load with Euler's $P_{cr}$, with $\sigma_YA$, with the tangent-modulus load (Eq. 9) and with 1.95 times the Aluminum Association allowable load (Beer Eq. 10.44b). Then plot every test of this lab on the column curve, $\sigma_{cr}$ against $L_e/r$, with error bars, over Euler's curve and the tangent-modulus curve. *Check:* the tangent-modulus curve joins Euler's curve for slender columns. *Interpret:* which of the predictions would you have trusted before the test, and why does even the tangent-modulus load overestimate the real column?

**A6 [Core] — Theory vs. simulation vs. measurement.** Complete Table 5, including $E$ from the axial strain: average the front and back gages, $(\varepsilon_F + \varepsilon_B)/2 = -P/(EA)$, over the readings below half of each $P_{cr}$. Make one figure with each row normalized by its theory value, with error bars at $\pm U$. Explain **every** discrepancy larger than the expanded uncertainty with a named cause, quantified where you can.

**M1 [Core] — Where does the model break?** (a) By how much does Euler's formula overestimate the Part D maximum load, and below what $L/r$ does it predict more than $\sigma_Y$? (b) By how much is "fixed ends" unconservative for your clamped tests, and what $kL/EI$ would bring $K$ within 1 % of 0.5? (c) Linear theory says $\delta \to \infty$ at $P_{cr}$; the exact (elastica) solution of a perfect pinned column has $P/P_{cr} - 1 \approx (\pi^2/8)(\delta/L)^2$. How far above $P_{cr}$ is a perfect bar at your $L/60$ limit, and at what $\delta$ would your 450 mm bar first yield? (d) By how much does Eq. 10.37 overestimate the first-yield load for $e$ = 2 mm? (e) How large an offset of the knife edges does your A1 result imply? Rank these effects.

**C1 [Challenge] — Southwell from strains.** Repeat the Southwell construction for the 450 mm bar with the bending strain $(\varepsilon_F - \varepsilon_B)/2$ in place of $\delta$ (Appendix D.5) and compare $P_{cr}$. Why can a strain-gage Southwell plot be used on a column whose deflection you cannot reach with a dial gage?

**C2 [Challenge] — How well can a stiff clamp be measured?** From Eq. 3, find $(dk/k)/(dP_{cr}/P_{cr})$ at your fixed–fixed result, and explain why a 1 % uncertainty in $P_{cr}$ becomes more than 10 % in $k$. Propose a test that would measure $k$ more precisely.

**C3 [Challenge] — The offset as a bow.** Show that equal end moments $Pe$ on a pinned column act on the first buckling mode like an initial bow $(4/\pi)e$ (expand the constant moment in a sine series), and check the result against your Part C data.

**X1 [Extension] — Spring ends.** Derive Eqs. 3 and 4 (Appendix D.3), and show that they reduce to Beer's Eqs. 10.11a and 10.19 in the limits $k \to 0$ and $k \to \infty$.

**X2 [Extension] — After buckling.** Derive the elastica of the pinned column, $P/P_{cr} = (2K(k)/\pi)^2$ and $\delta/L = k/K(k)$, where $K(k)$ is the complete elliptic integral of the first kind and $k = \sin(\theta_0/2)$, and expand it for small $\delta$. Use it to explain why a column, unlike a plate, has almost no strength beyond $P_{cr}$.

**X3 [Extension] — Tangent or reduced modulus?** With the simulation's short-column model, load a nearly perfect 90 mm bar ($\delta_0 = L/10^7$) and explain, after Shanley, why bending starts at the tangent-modulus load while the load can still rise toward the reduced-modulus load.

## 8. Design problem

**D1 — An aluminum strut.** A 6061-T6 round tube, 2.0 m long between the bolts of its end gussets, carries a compressive service load of 12 kN. The load may act up to 2 mm off the tube's axis. Requirements:

* centric load: $P \le \sigma_{all}A$ with the Aluminum Association formulas for 6061-T6 (Beer Eqs. 10.43b–10.45b, which include a factor of safety);
* eccentric load: the load that first yields the tube with $e$ = 2 mm (secant formula, Eq. 8, with **your** Lab 1 $\sigma_Y$ and Lab 2 $E$) at least 1.95 times the service load, the factor the Aluminum Association formulas build in;
* wall slenderness $D_o/t$ at most 40 (local buckling of thin walls is outside Beer's scope) and outside diameter at most 76.2 mm; the lightest tube from Table 6.

Choose the effective length and justify it: the gusset plates are bolted, not clamped like Part B's blocks.

::: {.needspace lines="8"}
:::

| Dimension | Sizes available (every combination, 20 tubes) |
|---|---|
| Outside diameter $D_o$ (mm) | 44.45, 50.80, 57.15, 63.50, 76.20 |
| Wall thickness $t$ (mm) | 1.65, 2.11, 3.18, 4.78 |

: Table 6. Catalog for D1: 6061-T6 round tubes, named $D_o$ × wall (for example 50.8 × 3.18). Compute the mass yourself (density 2700 kg/m³).

Use the simulation (preset "D1") to explore, then verify your final choice by hand: $L_e/r$, the allowable load, the first-yield load from Eq. 8 (solved by trial) and the lateral deflection at the service load (Eq. 7). Then show what a designer who took $K$ = 0.52 from Part B would have chosen, and check that tube with pinned ends. Submit at most one page: a table of the tubes you checked, the calculations for your choice, and one assumption that could invalidate your design, with how you would check it.

| Criterion | Weight |
|------------------------------------------------------------------------------|-------:|
| Section properties, $L_e/r$ and the allowable load correct; units correct | 20 % |
| First-yield load from the secant formula solved correctly; factor of safety applied to the load | 25 % |
| Effective length chosen and justified from the end details and from Part B | 20 % |
| Choice justified by a quantitative comparison of alternatives, including the fixed-end trap | 25 % |
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

If the equipment is unavailable, use `sample_data.csv`. It holds one row per reading:

| Column | Meaning |
|---|---|
| `part` | `A`, `B`, `C` or `D` |
| `config` | `pinned` (Part A), `fixed-fixed` or `fixed-pinned` (Part B), `eccentric` (Part C), `short` (Part D) |
| `L_mm` | nominal length between the supports (mm) |
| `e_mm` | nominal offset of the V-grooves (mm): 0, 1 or 2 |
| `step` | reading number within the test, from 0 |
| `load_N` | load-cell reading (N); the UTM's reading in Part D |
| `defl_mm` | dial-gage reading at mid-length (mm), zeroed with no load |
| `eps_front_ue`, `eps_back_ue` | front (convex) and back gages at mid-length, in microstrain, zeroed with no load; blank in Part D |

: Table A1. Columns of `sample_data.csv`. In each test the readings switch from load steps to deflection steps at about 75 % of the predicted critical load (step 3 of the procedure).

::: {.needspace lines="16"}
:::

Use these measurements:

| Quantity | Readings |
|---|---|
| $b$ (mm) | 25.41, 25.43, 25.42, 25.42 |
| $t$ (mm) | 6.35, 6.36, 6.34, 6.35 |
| Lengths (mm) | A: 300.0, 450.0, 600.5; B: 600.5 (fixed–fixed), 640.0 (fixed–pinned); D: 90.0 |
| Initial bows (mm) | A: 0.26, 0.46, 0.62; B: 0.50; D: 0.03 |
| Groove offsets (mm) | 1.00 and 2.00, ±0.02 |

: Table A2. Measurements for the sample data. The micrometer is good to ±0.003 mm, the rule to ±0.5 mm, the dial gage to ±0.01 mm, the load cell and the UTM to ±0.5 % of reading, and the gage factor to ±0.5 %.

## Appendix B — Uncertainty quick reference

* Limit $\pm a$ (calibration, accuracy): $u = a/\sqrt{3}$. Reading resolution $r$: $u = r/\sqrt{12}$ (already included when you use the scatter of repeated readings).
* Sum or difference: $u_{x \pm y}^2 = u_x^2 + u_y^2$. Product or quotient: $(u_{xy}/xy)^2 = (u_x/x)^2 + (u_y/y)^2$. Power: $u_{x^k}/x^k = |k|\,u_x/x$.
* Mean of $N$ readings: $u = s/\sqrt{N}$ for the scatter, combined with any calibration term.
* Least-squares line $y = A_0 + A_1x$ through $N$ points: $s_{A_1} = s/\sqrt{\sum(x_i - \bar x)^2}$, with $s^2 = \sum(y_i - A_0 - A_1x_i)^2/(N-2)$ (LINEST in a spreadsheet).
* *Southwell.* $P_{cr} = 1/A_1$, so $u_P/P_{cr} = s_{A_1}/A_1$ from the fit; add the load-cell calibration, $0.5\,\%/\sqrt{3}$, in quadrature. $\delta_0 = A_0/A_1$.
* *Euler prediction.* Eq. 10: the thickness enters cubed, so a 0.005 mm uncertainty in $t$ gives 0.24 % in $I$.
* *Monte Carlo (for the clamp stiffness and the fixed–pinned prediction).* Draw every input ($P_{cr}$ of each test, $E$, $I$, the lengths, the load-cell calibration, common to both tests) from its distribution, repeat the whole calculation a few thousand times, and take the standard deviation of the results as $u$. It keeps the correlations between quantities that share inputs.
* *Example.* A slope of $5.47 \times 10^{-4}$ N⁻¹ with $s_{A_1} = 1.2 \times 10^{-7}$ N⁻¹: $P_{cr}$ = 1829 N with $u$ = 0.4 N from the fit and 5.3 N from the load cell, so $u$ = 5.3 N and $P_{cr}$ = 1829 ± 11 N ($U$). The calibration, not the scatter, dominates.
* Report $x \pm U$ with $U = 2u$. Round $U$ to one or two significant figures, and $x$ to the same decimal place.

## Appendix C — Using the simulation

Open `lab09_simulation.html` in any browser; it needs no internet connection. Choose a configuration at the top. In **Buckling load**, set the end conditions (including rotational springs of stiffness $k$), the length, the section and the material; the diagram shows the buckled shape and the effective length, and the column curve places your column on it. In **Imperfect and eccentric**, set the initial bow $\delta_0$, the offset $e$ and the load as a fraction of $P_{cr}$ (above 1 the page switches to the elastica); the Southwell plot fits the simulated readings and, for the Lab presets, the sample data. In **Short columns**, set the length, the material curve ($E$, $\sigma_Y$, $m$), the bow and the offset; a fiber model of the bar's section traces the load–deflection path through the maximum load. The **readout table** compares each closed form with an independent numerical method: "agree" rows check the formulas, and "different models" rows show how far a formula is from a more complete model. **Push the model past its assumptions** runs prepared experiments. **Export (CSV)** saves the curves, the readout or the convergence study; if your browser blocks the download, the data appears in a box you can copy. The **SI / US customary** toggle converts every input and output.

## Appendix D — Derivations

**D.1 Euler's formula (Eq. 1).** For the pinned column of Beer Fig. 10.7 the moment at a section is $M = -Py$, so $EIy'' = -Py$, or $y'' + p^2y = 0$ with $p^2 = P/EI$ (Beer Eqs. 10.4–10.7). The solution $y = A\sin px + B\cos px$ satisfies $y(0) = 0$ only if $B = 0$, and $y(L) = 0$ requires $A\sin pL = 0$. A bent shape ($A \ne 0$) needs $pL = n\pi$; the smallest load is $n = 1$, $P_{cr} = \pi^2EI/L^2$, with the shape $y = A\sin(\pi x/L)$ of undetermined amplitude (Beer Eqs. 10.8–10.12).

**D.2 Effective length.** A segment between two points of zero moment behaves as a pinned column, so $P_{cr} = \pi^2EI/L_e^2$ with $L_e$ the distance between those points (Beer §10.1B). With one end pinned and one fixed, the moment includes the lateral reaction $V$: $y = A\sin px - (V/P)x$, and the conditions at the fixed end give $\tan pL = pL$, so $pL = 4.4934$ and $K = \pi/4.4934 = 0.699$ (Beer Eqs. 10.14–10.21).

**D.3 Rotational-spring ends (Eqs. 3, 4).** Let each end resist rotation with a moment $M = k\theta$. *Two equal springs.* By symmetry there is no lateral reaction, and the end moment $M_e$ is the same at both ends: $EIy'' = -Py + M_e$, so $y = A\sin px + B\cos px + M_e/P$. The conditions $y(0) = y(L) = 0$ give $B = -M_e/P$ and $A = -(M_e/P)\tan(pL/2)$. At the end, $EIy''(0) = M_e$ must equal $ky'(0) = kAp$: $1 = -(kp/P)\tan(pL/2)$, which with $P = p^2EI$ is Eq. 3. *Spring at one end, pin at the other.* With $\xi$ measured from the spring end, a lateral reaction $M_0/L$ keeps the column in equilibrium: $EIy'' = -Py + M_0(1 - \xi/L)$, so $y = A\sin p\xi + B\cos p\xi + (M_0/P)(1 - \xi/L)$. The conditions give $B = -M_0/P$ and $A = (M_0/P)\cot pL$; equating $M_0$ to $ky'(0)$ gives $PL/k = pL\cot pL - 1$, which is Eq. 4. *Inverting Eq. 3.* With $x = (L/2)\sqrt{P_{cr}/EI}$ from a measured $P_{cr}$, $k = -2xEI/(L\tan x)$; as $x \to \pi$ (fixed ends) $\tan x \to 0$ and $k$ becomes very sensitive to $P_{cr}$.

**D.4 Bow amplification (Eq. 5).** With a stress-free initial shape $y_0 = \delta_0\sin(\pi x/L)$, the bending moment is set by the change of curvature: $EI(y - y_0)'' = -Py$. Trying $y = Y\sin(\pi x/L)$ gives $EI(\pi/L)^2(Y - \delta_0) = PY$, so $Y = \delta_0/(1 - P/P_{cr})$ and the dial reads $\delta = Y - \delta_0 = \delta_0\alpha/(1 - \alpha)$. A general bow is a sine series; its $n$th term is amplified by $1/(1 - \alpha/n^2)$, so near $P_{cr}$ the first term dominates. For a fixed load the equation is linear in $y_0$ and in the end offsets, so the responses to a bow and to an eccentricity add at the same load, even though neither is proportional to $P$.

**D.5 Southwell (Eq. 6).** Multiply Eq. 5 by $(1 - \alpha)/P$: $\delta/P - \delta/P_{cr} = \delta_0/P_{cr}$, which is Eq. 6. *An offset load as a bow:* end moments $Pe$ produce a constant moment, whose sine-series coefficient for the first mode is $(4/\pi)Pe$, the same as a bow of $(4/\pi)e$. *With strains:* the bending strain at mid-length is $\varepsilon_b = Mc/EI$ with $M = P(\delta_0 + \delta + e)$ for the pinned bar, which is proportional to $\delta$ plus a constant, so $\varepsilon_b/P$ against $\varepsilon_b$ is also a straight line of slope $1/P_{cr}$.

**D.6 The secant formula (Eqs. 7, 8).** For the eccentric pinned column $M = -P(y + e)$ (Beer Eq. 10.22), so $y'' + p^2y = -p^2e$, with solution $y = e[\tan(pL/2)\sin px + \cos px - 1]$ (Eq. 10.26). At mid-length $y_{max} = e[\sec(pL/2) - 1]$, and $pL/2 = (\pi/2)\sqrt{P/P_{cr}}$ (Eqs. 10.27–10.31). The largest compressive stress is $P/A + P(y_{max} + e)c/I$; with $I = Ar^2$ this is Eq. 8 (Eqs. 10.32–10.36). For other end conditions use $L_e$.

**D.7 Short columns (Eq. 9).** Engesser assumed that a column which starts to bend at a stress $\sigma$ does so while every fiber is still loading, so its bending stiffness is $E_tI$ and $P_t = \pi^2E_tI/L_e^2$. Differentiating the Ramberg–Osgood fit, $d\varepsilon/d\sigma = 1/E + 0.002m\sigma^{m-1}/\sigma_Y^m$, gives $1/E_t$ in Eq. 9. If instead the convex side unloads at the slope $E$ while the concave side loads at $E_t$, the stiffness is the reduced modulus, $E_r = 4EE_t/(\sqrt{E} + \sqrt{E_t})^2$ for a rectangle (von Kármán). Shanley showed that a perfect column starts to bend at the tangent-modulus load and that the load can then rise only toward the reduced-modulus load; with imperfections, the maximum load lies below $P_t$. *Fitting $m$:* from your Lab 1 aluminum curve, take the plastic strain $\varepsilon_p = \varepsilon - \sigma/E$ for stresses between about $0.7\sigma_Y$ and $\sigma_Y$ and fit a line to $\log\varepsilon_p$ against $\log(\sigma/\sigma_Y)$: the slope is $m$, and the line should pass near $\varepsilon_p$ = 0.002 at $\sigma_Y$. The Lab 1 sample data give $m \approx$ 17.

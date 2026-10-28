# Lab 8 — Transformation of Stress and Strain: Mohr's Circle, Strain Rosettes and a Tube Under Combined Loads

| | |
|---|---|
| **Course** | ENGR 2228 Mechanics of Materials |
| **When** | Week 14, after lectures on Beer 8e Ch. 7 |
| **Textbook** | Beer, Johnston, DeWolf, Mazurek, *Mechanics of Materials*, 8th ed. (Beer 8e): §7.1–7.4 (plane stress, Mohr's circle, three-dimensional stress), §7.5 (yield criteria), §7.6 (pressure vessels), §7.7 and §7.9 (strain, rosettes), §8.3 (combined loads) |
| **Session** | 2 hours in the lab, teams of two; report due one week later |
| **Equipment** | Combined-loading frame: a 6061-T6 tube 38.1 × 3.18 mm clamped at one end, with a lever at the free end and a screw loader on a 1 kN load cell; two rectangular strain-gage rosettes; six-channel strain indicator; sealed end plugs, hand pump and pressure transducer; micrometer, ball micrometer, steel rule |
| **Files** | `lab08_simulation.html` (open in any browser, works offline) and `sample_data.csv` |

## 1. Learning objectives

After this lab you will be able to:

1. Transform a plane state of stress to any axes and find the principal stresses, the principal planes and the maximum shearing stress, both from the equations and with Mohr's circle (§7.1–7.2).
2. Reduce strain-rosette readings to strain components, principal strains and principal directions, and convert them to stresses (§7.7, §7.9, §2.5).
3. Predict the stresses at points of a tube under bending, torsion, transverse shear and internal pressure, and test the prediction with rosettes (§8.3, §7.6).
4. Tell the in-plane from the absolute maximum shearing stress, and show by measurement when they differ (§7.4).
5. Measure and correct two real imperfections of strain-gage work: a rosette bonded at a small angle, and the gages' transverse sensitivity.
6. Choose a tube for combined loads and internal pressure with a yield criterion (§7.5).

## 2. Theory

The set-up is shown in Figure 1. A load $F$ on the lever bends and twists the tube; with the load moved onto the tube's axis it only bends it. Rosette H on top sees bending and torsion; rosette K on the lever side, at mid-height, sees torsion and transverse shear. In Part C the tube is sealed and pressurized.

![Figure 1. Test set-up (schematic). (a) The tube, clamped at the left, with the lever at the free end pointing toward the viewer and the load F at its tip; rosettes H (top) and K (lever side) at the gage section, L_b = 250 mm from the load line. (b) The section seen from the free end: the lever arm a_L = 200 mm and the torque T. (c) The rectangular rosette and the local axes: x along the tube, y 90° counterclockwise from x as seen from outside the tube.](figures/fig1_setup.png){width=6.4in}

::: {.needspace lines="12"}
:::

::: {custom-style="Callout"}
**Sign convention (Beer 8e).** Tension is positive. The shearing stress $\tau_{xy}$ is positive on the $+x$ face in the $+y$ direction (Fig. 7.2), and the angle $\theta$ is measured counterclockwise from $x$. **Mohr's circle:** a face whose shearing stress tends to turn the element clockwise is plotted above the $\sigma$ axis (Fig. 7.15), so point X, for the $x$ face, is plotted at $(\sigma_x, -\tau_{xy})$; turning the element by $\theta$ moves the point by $2\theta$ in the same sense. Strain follows the same rules with $\sigma \to \varepsilon$ and $\tau \to \gamma/2$. **On the tube:** $x$ runs along the tube toward the free end, and $y$ is 90° counterclockwise from $x$ as seen from outside the tube; gage a of each rosette is along $x$, b at 45° and c at 90° (Figure 1c). With these axes a downward load on the lever gives $\tau_{xy} < 0$ at both H and K.
:::

::: {custom-style="Callout"}
**Nomenclature.** $\sigma_x, \sigma_y, \tau_{xy}$ plane-stress components; $\sigma_{x'}, \tau_{x'y'}$ components on axes turned by $\theta$; $\sigma_{ave}$, $R$ center and radius of Mohr's circle; $\sigma_{max}, \sigma_{min}$ in-plane principal stresses; $\theta_p$ principal angle; $\sigma_1 \ge \sigma_2 \ge \sigma_3$ principal stresses in three dimensions; $\tau_{max}$ maximum shearing stress; $\varepsilon_x, \varepsilon_y, \gamma_{xy}$ strain components; $\varepsilon_a, \varepsilon_b, \varepsilon_c$ gage readings; $\beta$ angle at which a rosette is bonded, counterclockwise from $x$; $K_t$ transverse sensitivity; $E$, $\nu$, $G$ elastic constants; $D_o$, $D_i$, $r_o$, $r_i$ outside and inside diameters and radii; $t_w = r_o - r_i$ wall thickness; $t$ total width of the cut in $VQ/(It)$; $I$, $J$ moments of inertia; $Q$ first moment; $F$ load; $a_L$ lever arm; $L_b$ distance from the gage section to the load line; $M$, $T$, $V$ bending moment, torque and shear force; $p$ internal pressure; $\sigma_\theta$, $\sigma_r$ hoop and radial stress; $u$ standard uncertainty; $U = 2u$ expanded uncertainty.
:::

Full derivations are in **Appendix D**; this section states each result, what it means, and when it stops applying.

### 2.1 Transformation of plane stress and Mohr's circle

Cutting a small element at an angle $\theta$ and writing its equilibrium gives the stresses on the turned faces (§7.1A):

$$\sigma_{x'} = \sigma_{ave} + \frac{\sigma_x - \sigma_y}{2}\cos 2\theta + \tau_{xy}\sin 2\theta, \qquad \tau_{x'y'} = -\frac{\sigma_x - \sigma_y}{2}\sin 2\theta + \tau_{xy}\cos 2\theta \qquad (1)$$

with $\sigma_{ave} = (\sigma_x + \sigma_y)/2$. As $\theta$ varies, the point $(\sigma_{x'}, -\tau_{x'y'})$ runs around a circle of center $\sigma_{ave}$ and radius $R$, Mohr's circle (§7.2; Figure 2a shows it for point H). Its ends on the $\sigma$ axis are the **principal stresses**, on faces with no shearing stress,

$$\sigma_{max,\,min} = \sigma_{ave} \pm R, \qquad R = \sqrt{\left(\frac{\sigma_x - \sigma_y}{2}\right)^2 + \tau_{xy}^2} \qquad (2)$$

$$\tan 2\theta_p = \frac{2\tau_{xy}}{\sigma_x - \sigma_y} \qquad (3)$$

and its top and bottom are the largest **in-plane** shearing stress, $R$, on faces at 45° to the principal faces. Equation 3 has two roots 90° apart; substitute one into Eq. 1, or read Mohr's circle, to see which face carries $\sigma_{max}$.

*Worked example.* $\sigma_x$ = 40 MPa, $\sigma_y$ = −10 MPa, $\tau_{xy}$ = 15 MPa: $\sigma_{ave}$ = 15 MPa, $R = \sqrt{25^2 + 15^2}$ = 29.2 MPa, so $\sigma_{max}$ = 44.2 MPa and $\sigma_{min}$ = −14.2 MPa. X is at (40, −15), below the axis; turning counterclockwise by $2\theta_p$ = 31.0° brings it to A, so $\theta_p$ = 15.5° counterclockwise from $x$.

![Figure 2. Mohr's circles at the top of the tube (H), load on the lever, drawn without numbers. (a) Stress: X for the face normal to the tube axis is above the σ axis (its shearing stress turns the element clockwise); A and B are the principal stresses. (b) Strain: the three gage readings are the abscissas of three points on the circle at twice their angles from x; squares show the same rosette turned by 8°, whose points slide around the same circle.](figures/fig2_mohr.png){width=6.4in}

### 2.2 Three dimensions: the absolute maximum shearing stress

At a free surface the stress normal to the surface is zero, so it is a third principal stress (§7.4). The three principal stresses $\sigma_1 \ge \sigma_2 \ge \sigma_3$, zero among them, define three Mohr's circles (Figure 3), and the largest shearing stress on **any** plane is

$$\tau_{max} = \frac{\sigma_1 - \sigma_3}{2} \qquad (4)$$

If $\sigma_{max}$ and $\sigma_{min}$ have opposite signs, the in-plane circle is the largest and $\tau_{max} = R$. If they have the same sign, the largest circle passes through zero and $\tau_{max}$ is half the larger principal stress, on planes at 45° to the surface. A thin pressure vessel is the classic case (Beer Eqs. 7.33, 7.34).

### 2.3 Strain and strain rosettes

The normal strain in a direction $\theta$ follows from the strain components exactly as Eq. 1 follows from the stresses, with $\tau$ replaced by $\gamma/2$ (§7.7):

$$\varepsilon(\theta) = \varepsilon_x\cos^2\theta + \varepsilon_y\sin^2\theta + \gamma_{xy}\sin\theta\cos\theta \qquad (5)$$

A gage measures $\varepsilon$ in one direction only, so three gages are needed for the three components (§7.9). For the rectangular rosette of Figure 1c (gages at 0°, 45° and 90°), Eq. 5 gives Beer's Eq. 7.43:

$$\varepsilon_x = \varepsilon_a, \qquad \varepsilon_y = \varepsilon_c, \qquad \gamma_{xy} = 2\varepsilon_b - (\varepsilon_a + \varepsilon_c) \qquad (6)$$

The principal strains and their directions follow from Mohr's circle for strain, which plots $(\varepsilon, \gamma/2)$ by the same "clockwise above" rule (Beer Eqs. 7.50–7.52):

$$\varepsilon_{max,\,min} = \varepsilon_{ave} \pm \sqrt{\left(\frac{\varepsilon_x - \varepsilon_y}{2}\right)^2 + \left(\frac{\gamma_{xy}}{2}\right)^2}, \qquad \tan 2\theta_p = \frac{\gamma_{xy}}{\varepsilon_x - \varepsilon_y} \qquad (7)$$

At a free surface ($\sigma_z = 0$), Hooke's law for an isotropic material gives the stresses (§2.5, §2.7):

$$\sigma_x = \frac{E}{1 - \nu^2}(\varepsilon_x + \nu\varepsilon_y), \qquad \sigma_y = \frac{E}{1 - \nu^2}(\varepsilon_y + \nu\varepsilon_x), \qquad \tau_{xy} = G\gamma_{xy}, \qquad G = \frac{E}{2(1 + \nu)} \qquad (8)$$

and the principal directions of stress and strain coincide.

**Two imperfections.** *A turned rosette:* if the rosette is bonded at a small angle $\beta$ (counterclockwise) from $x$, Eq. 6 returns the strains on axes turned by $\beta$. Its readings move around the same Mohr's circle (Figure 2b), so the principal strains are still right, but the components on $x$ and $y$, and the principal directions, are wrong until the strains are turned back by $-\beta$ with Eq. 1. *Transverse sensitivity:* a gage also responds, weakly, to strain across its grid. The indicated reading is $\hat\varepsilon = (\varepsilon_\parallel + K_t\varepsilon_\perp)/(1 - \nu_0K_t)$, with $K_t$ from the gage package and $\nu_0$ = 0.285 the Poisson's ratio of the gage-factor calibration; Appendix D.4 inverts it for a rectangular rosette.

### 2.4 The tube under combined loads

At the gage section the load $F$ produces a bending moment $M = FL_b$, a torque $T = Fa_L$ and a shear force $V = F$ (§8.3). With $c = r_o$, $I = \pi(r_o^4 - r_i^4)/4$ and $J = 2I$:

$$\text{H:}\;\; \sigma_x = \frac{Mc}{I},\;\; \tau_{xy} = -\frac{Tc}{J}; \qquad \text{K:}\;\; \sigma_x = 0,\;\; \tau_{xy} = -\left(\frac{Tc}{J} + \frac{VQ}{It}\right) \qquad (9)$$

with $\sigma_y = 0$ at both, $Q = \tfrac{2}{3}(r_o^3 - r_i^3)$ the first moment of the half-section above the neutral axis, and $t = 2(r_o - r_i)$ the width of the cut through both walls. The transverse shear adds to the torsion at K, on the lever side, and subtracts on the opposite side.

Internal pressure $p$ in the closed tube adds a hoop stress $\sigma_\theta$ (along the local $y$) and an axial stress (along $x$). Treating the wall as thin (§7.6, with $r$ the inner radius),

$$\sigma_\theta = \frac{pr_i}{t_w}, \qquad \sigma_x = \frac{pr_i}{2t_w} \qquad (10)$$

where $t_w = r_o - r_i$ is the wall thickness. Equation 10 is exact for the **average** hoop stress across the wall, but the gages sit on the outer surface, where the thick-wall (Lamé) solution of Appendix D.6 gives

$$\sigma_\theta(r_o) = \frac{2pr_i^2}{r_o^2 - r_i^2}, \qquad \sigma_x = \frac{pr_i^2}{r_o^2 - r_i^2}, \qquad \sigma_r(r_o) = 0 \qquad (11)$$

For the lab tube, $r_i/t_w \approx 5$ and Eq. 10 is 10 % above Eq. 11 at the gages (Figure 4). At the inner surface the hoop stress is larger and $\sigma_r = -p$.

![Figure 3. Three-dimensional Mohr's circles at H, without numbers. The solid circle is the in-plane circle; the dashed circles join A and B to the origin O, the zero radial stress at the surface. (a) Lever load only: A tensile, B slightly compressive, so the in-plane maximum shear is the absolute maximum. (b) With internal pressure: A and B both tensile, the largest circle runs from O to A, and the absolute maximum shear is about 1.5 times the in-plane value.](figures/fig3_threeD.png){width=6.4in}

*When Eqs. 1–11 apply:* Eqs. 1–7 are geometry and equilibrium and hold for any material; Eq. 8 needs a linear-elastic isotropic material at a free surface; Eq. 9 needs the gage section at least about two diameters from the clamp and from the load (Saint-Venant), and $VQ/It$ is the shear averaged through the wall; Eq. 10 needs $r_i/t_w \gtrsim 10$ for 5 % accuracy at a surface.

![Figure 4. (a) Hoop and radial stress through the wall of the lab tube, divided by the pressure (Lamé), with the thin-wall value p r_i/t; the open circle marks the outer surface, where the gages are. (b) The error of p r_i/t against the radius ratio r_o/r_i, relative to the Lamé hoop stress at the outer surface and at the inner surface.](figures/fig4_thick.png){width=6.4in}

### 2.5 The model in the simulation

`lab08_simulation.html` has three configurations. **Stress at a point** draws Mohr's circle with a turning element; drag the point X′ around the circle and the element turns by half the angle. **Strain rosette** reduces three readings (rectangular, delta or any three angles), corrects for a turned rosette and for $K_t$, and marks the readings on Mohr's circle for strain. **Tube, combined loads** applies Eqs. 9–11 at any point of the circumference, on the outer or the inner surface. Each closed form is checked against an independent numerical method: the stress tensor rotated by matrix products, eigenvalues by Jacobi rotations, a sweep over all directions, Gaussian elimination of Eq. 5, Simpson quadrature for $Q$ and a finite-difference solution of the thick cylinder.

### 2.6 Uncertainty

Use standard uncertainties $u$; convert a limit $\pm a$ to $u = a/\sqrt{3}$; propagate to first order (Appendix B). In Part A, $E = \sigma_x/\varepsilon_x$ with $\sigma_x = FL_bc/I$ per newton and $\varepsilon_x$ the fitted slope $s$, so

$$\left(\frac{u_E}{E}\right)^2 = \left(\frac{u_s}{s}\right)^2 + \left(\frac{u_{L_b}}{L_b}\right)^2 + \left(\frac{u_I}{I}\right)^2 + \left(\frac{u_c}{c}\right)^2 + \left(\frac{u_F}{F}\right)^2 + \left(\frac{u_{GF}}{GF}\right)^2 \qquad (12)$$

where the last two terms are the load-cell and gage-factor calibrations. Principal stresses come from three readings through several nonlinear steps; propagate them by the Monte Carlo method of Appendix B. Report $x \pm U$ with $U = 2u$ and draw error bars at $\pm U$. A measurement and a prediction **agree** when

$$|x_{meas} - x_{pred}| \le 2\sqrt{u_{meas}^2 + u_{pred}^2} \qquad (13)$$

Any larger discrepancy needs a physical or procedural explanation, quantified where possible.

## 3. Pre-lab (due at the start of the session)

Answer on paper or in a short document. Show every step, units included. Use Table 1 and the nominal dimensions in Table 2.

**P1 — Estimate before you measure.** For $F$ = 600 N: (a) at H with the load on the lever, find $\sigma_x$ and $\tau_{xy}$ (Eq. 9), then $\sigma_{max}$, $\sigma_{min}$, $\theta_p$ and the in-plane $\tau_{max}$ (Eqs. 2, 3). (b) At K, find $\tau_{xy}$. (c) At H, find $\varepsilon_x$, $\varepsilon_y$ and $\gamma_{xy}$ (Eq. 8), and the readings of gages a, b and c (Eq. 5). (d) For $p$ = 8 MPa alone, find $\sigma_\theta$ and $\sigma_x$ at the gages from Eq. 10 and from Eq. 11. Check the units of every answer.

**P2 — Mohr's circle by hand.** Draw Mohr's circle for P1(a) to scale on graph paper. Plot X and Y by the "clockwise above" rule, read off $\sigma_{max}$, $\sigma_{min}$ and $2\theta_p$, and compare with Eqs. 2 and 3. Sketch the element at H, seen from above, turned to its principal directions.

**P3 — A rosette by hand.** Reduce your P1(c) readings with Eqs. 6–8 and confirm that they return P1(a). Then suppose the rosette had been bonded 2° counterclockwise from $x$: what would the three gages read, and which of $\varepsilon_x$, $\gamma_{xy}$, $\varepsilon_{max}$ and $\theta_p$ would come out wrong if you ignored the turn?

**P4 — In-plane or absolute?** Superpose P1(a) and the Eq. 11 stresses of P1(d) to get the state at H with 8 MPa and the lever load. Find the principal stresses, the in-plane $\tau_{max}$ and the absolute $\tau_{max}$ (Eq. 4). Which one does the maximum-shearing-stress (Tresca) criterion use?

**P5 — Predict with the simulation.** Open `lab08_simulation.html`. For "Lab Part B: load on the lever, rosette H" and "rosette K", record $\sigma_{max}$, $\sigma_{min}$, $\theta_p$ and the ideal rosette readings. For "Lab Part C: 8 MPa and the lever load, H", record the in-plane and the absolute $\tau_{max}$. For "Rosette turned 5°", record $\sigma_x$, $\tau_{xy}$ and $\sigma_{max}$ with $\beta$ = 0 and with $\beta$ = 5°.

**P6 — Safety.** (a) List the hazards in this lab and how the procedure controls each. (b) Why are the limits 600 N and 8 MPa? Support your answer with the largest von Mises stress in the tube and the margin to $\sigma_Y$.

| Property of the 6061-T6 tube | Value |
|---|---:|
| $E$ (GPa) | 68.46 ± 0.47 (your Lab 2) |
| $\nu$ | 0.3296 ± 0.0029 (your Lab 2) |
| $G$ (GPa) | 26.03 ± 0.12 (your Lab 3) |
| Yield strength $\sigma_Y$ (MPa) | 273.7 ± 1.0 (your Lab 1) |

: Table 1. Reference values. The ± values are standard uncertainties. Replace them with your own team's results where you have them.

::: {.needspace lines="14"}
:::

## 4. Equipment and safety

| Item | Specification used in this handout |
|---|---|
| Tube | 6061-T6, 38.1 × 3.18 mm (1.5 × 0.125 in) nominal, clamped over 60 mm at one end, sealed with O-ring end plugs |
| Lever and loader | Load points on the tube's axis and 200 mm to the side; screw loader on a 1 kN load cell (±0.5 % of reading) |
| Rosettes | Two stacked rectangular rosettes, 3 mm grids, gage factor 2.10 ± 0.5 %, transverse sensitivity $K_t$ = +1.2 % (from the package; calibrated with $\nu_0$ = 0.285), self-temperature-compensated for aluminum |
| Strain indicator | Six channels, quarter bridge, three-wire; resolution 1 µε, accuracy ±0.1 % |
| Pressure | Hand pump with hydraulic oil, relief valve set at 10 MPa, transducer 0–20 MPa (±0.05 MPa), bleed screw in the far end plug |
| Instruments | Micrometer ±0.003 mm; ball micrometer for the wall ±0.005 mm; steel rule ±0.5 mm |

: Table 2. Equipment. If your equipment differs, record its values and use them throughout.

::: {custom-style="Safety"}
**Safety.** Wear safety glasses throughout. **Limits:** load 600 N; pressure 8 MPa; both together at most 600 N with 8 MPa. These keep the largest von Mises stress below about 30 % of $\sigma_Y$. **Pressure:** bleed every bubble of air before you pressurize (oil stores almost no energy; trapped air does), keep the shield in place, never tighten or loosen a fitting under pressure, and release the pressure before you touch the plugs. **Loading:** turn the screw loader by hand only; keep fingers away from the lever and the clamp while loaded; unload the lever before releasing the pressure.
:::

## 5. Procedure

1. **Measure.** Record $D_o$ (micrometer, four places), the wall thickness (ball micrometer, four places), $L_b$ and $a_L$ (rule), and the rosette data. Write everything in Table 3. **Check:** the four readings of each should span no more than 0.01 mm.
2. **Connect and zero.** Connect the six grids (Ha, Hb, Hc, Ka, Kb, Kc), set the gage factor to 2.10 and zero with no load and no pressure. **Check:** no reading drifts more than 2 µε in two minutes.
3. **Part A.** Attach the loader at the load point on the tube's axis. Load from 0 to 600 N in 100 N steps, recording all six readings at each step; unload. **Check:** at 600 N, Ha should be near your P1(c) value of $\varepsilon_x$ (about 770 µε) and Kb small (about −60 µε); after unloading, every reading returns to within 3 µε of zero.
4. **Part B.** Move the loader to the lever point, 200 mm from the axis, and repeat step 3. **Check:** Kb about −480 µε at 600 N.
5. **Part C.** Unload. Fill the tube with oil, bleed the air, close the bleed screw and re-zero the indicator at zero pressure. Raise the pressure to 2, 4, 6 and 8 MPa, recording all six readings at each step. **Check:** Hc/Ha and Kc/Ka should both lie between 4.4 and 5.0.
6. **Part C with the lever load.** Hold 8 MPa and load the lever to 200, 400 and 600 N, recording the readings (do not re-zero). Unload the lever first, then release the pressure.
7. **Before you leave:** open the simulation, enter your measured dimensions in the Lab presets, and record its predictions in Table 5 next to your raw readings.

## 6. Data tables

```{=latex}
\renewcommand{\arraystretch}{1.9}
```

| Quantity | Readings | Mean |
|----------------------------------|------------------------------------------------|----------|
| $D_o$ (mm) | | |
| Wall thickness (mm) | | |
| $L_b$, $a_L$ (mm) | | — |
| Gage factor, $K_t$ (from the package) | | — |

: Table 3. Dimensions.

::: {.needspace lines="12"}
:::

| Test | Load | Readings Ha, Hb, Hc, Ka, Kb, Kc (µε) |
|------------------------------|--------------|--------------------------------------------------------------|
| Part A (load on the axis) | 600 N | |
| Part B (load on the lever) | 600 N | |
| Part C (pressure) | 8 MPa | |
| Part C (pressure and lever) | 8 MPa, 600 N | |

: Table 4. Spot readings for the checks in the procedure; record every step on a separate sheet.

```{=latex}
\clearpage
```

| Quantity | Theory (equation) | Simulation | Measured ± U | Agree (Eq. 13)? |
|----------------------------------------|------------|------------|--------------|-----------|
| $E$ (GPa), $\nu$, Part A | Labs 1–2 | — | | |
| $G$ (GPa), Part B − Part A | Lab 3 | — | | |
| $\sigma_{max}$, $\sigma_{min}$ at H, Part B (MPa) | Eqs. 2, 9 | | | |
| $\theta_p$ at H, Part B (°) | Eqs. 3, 9 | | | |
| $\sigma_{max}$, $\sigma_{min}$ at K, Part B (MPa) | Eqs. 2, 9 | | | |
| $\sigma_\theta$ per MPa, Part C | Eqs. 10, 11 | | | |
| Absolute $\tau_{max}$ at H, Part C with the lever (MPa) | Eq. 4 | | | |

: Table 5. Theory vs. simulation vs. measurement.

```{=latex}
\renewcommand{\arraystretch}{1.15}
```

## 7. Analysis

Every answer must (i) show at least two reasoning steps, (ii) include a dimensional check or a limiting-case check, and (iii) end with one to three sentences interpreting the result in words. Questions marked **[Core]** are required of everyone. **[Challenge]** questions are for students who want more. **[Extension]** questions are for honors and independent study.

**A1 [Core] — How was each rosette bonded? E and ν.** Correct the Part A readings for transverse sensitivity (Appendix D.4), reduce them with Eq. 6 and fit each component against $F$. At H the stress is uniaxial, so any shear strain is apparent: find the angle $\beta_H$ at which rosette H was bonded (Appendix D.3), turn the strains back by $-\beta_H$, and find $E = \sigma_x/\varepsilon_x$ (with $\sigma_x$ from Eq. 9) and $\nu = -\varepsilon_y/\varepsilon_x$, with uncertainties (Eq. 12). Compare with Table 1 (Eq. 13). *Check:* with $\beta$ = 0 the apparent $\gamma_{xy}$ must vanish. *Interpret:* why does a turned rosette not change the principal strains, and which of your Part A results would the turn have spoiled had you ignored it?

**A2 [Core] — Torsion alone: G.** Subtract the Part A slopes from the Part B slopes: at both rosettes the difference is pure torsion. From the torsion-only state at K find the angle $\beta_K$ at which rosette K was bonded (Appendix D.3). Turn both differences back, and find $G = \tau/\gamma$ at H and at K with $\tau = Tc/J$. Compare with $E/(2(1+\nu))$ from A1 and with Table 1. *Check:* in pure shear $\varepsilon_x = \varepsilon_y$ after turning back. *Interpret:* why does the subtraction remove bending and transverse shear exactly?

**A3 [Core] — Principal stresses at H and K.** For Part B at 600 N, turn the strains back by $\beta$, convert them to stresses with Table 1's $E$ and $\nu$ (Eq. 8), and find $\sigma_{max}$, $\sigma_{min}$, $\theta_p$ and the in-plane $\tau_{max}$ at H and at K. Draw both Mohr's circles to scale. Compare with Eq. 9 using your measured dimensions (Eq. 13). *Check:* $\sigma_{max} + \sigma_{min} = \sigma_x + \sigma_y$. *Interpret:* sketch the tube with the direction of the largest tensile stress at H and at K, and explain why the two directions differ.

**A4 [Core] — Thin wall or thick?** From Part C, fit $\varepsilon_x$ and $\varepsilon_y$ (hoop) against $p$ at H and at K. (a) Find $\nu$ from their ratio, which does not involve $E$ (Appendix D.5). (b) Convert to $\sigma_\theta$ and $\sigma_x$ per MPa (Eq. 8) and compare with Eqs. 10 and 11. *Check:* both models give $\sigma_x/\sigma_\theta$ = 1/2. *Interpret:* which model agrees with your gages, and how can Eq. 10 be exact and still wrong at the surface?

**A5 [Core] — When is the in-plane shear not the maximum?** For Part C with the lever load (8 MPa and 600 N), find the principal stresses at H and at K, the in-plane $\tau_{max}$ and the absolute $\tau_{max}$ (Eq. 4), and compare with the prediction (Eqs. 9 and 11). Draw the three Mohr's circles at H. *Check:* the absolute $\tau_{max}$ can never be smaller than the in-plane one. *Interpret:* which value would the Tresca criterion use at H, and at K? What changes at the inner surface, where $\sigma_r = -p$?

**A6 [Core] — Theory vs. simulation vs. measurement.** Complete Table 5. Make one figure with each row normalized by its theory value, with error bars at $\pm U$. Explain **every** discrepancy larger than the expanded uncertainty with a named cause, quantified where you can.

**M1 [Core] — Where does the model break?** (a) By how much does Eq. 10 overstate the hoop stress at your gages, and at what $r_o/r_i$ would the error reach 5 %? (b) By how much does the in-plane $\tau_{max}$ understate the absolute one at H in Part C with the lever load, and with pressure alone? (c) If the rosettes' turns were ignored, how wrong would $\tau_{xy}$ and $\theta_p$ at H be in Part B? (d) If $K_t$ were ignored, how would $E$, $\nu$ and the Part C hoop strain change, and which gage of a rectangular rosette is affected most? (e) From the bending strain that leaks into rosette K in Part A, how far from mid-height is K? Rank these effects.

**C1 [Challenge] — Which rosette is better?** If K were a delta rosette (0°, 60°, 120° from $x$), what would its gages read in Part B at 600 N? With 1.5 µε of noise on every reading, compare the uncertainty of $\gamma_{xy}$ from the rectangular and the delta rosette.

**C2 [Challenge] — The tube as a load cell.** Using only the Part B readings of H and K (and $E$, $\nu$), find the load $F$, the torque arm $a_L$ and the bending arm $L_b$. Compare with the load cell and the rule.

**C3 [Challenge] — Transverse sensitivity.** Derive the correction of Appendix D.4. Show that a single gage reads correctly, whatever $K_t$, when the strain across it is $-\nu_0$ times the strain along it, and explain why gage a at H in Part A is nearly unaffected while gage c in Part C is not.

**X1 [Extension] — Lamé.** Derive Eq. 11 (Appendix D.6) and show that the hoop stress averaged through the wall is exactly Eq. 10.

**X2 [Extension] — Stress and strain circles.** Show that in an isotropic material the principal directions of stress and strain coincide, and that the radius of Mohr's circle for stress is $2G$ times the radius of the circle for strain (with $\gamma/2$ plotted).

**X3 [Extension] — A torque meter.** Design a strain-gage arrangement (gages and a full bridge) on this tube that reads the torque alone, rejecting bending, transverse shear, pressure and temperature. Explain each rejection with Eq. 5.

## 8. Design problem

**D1 — A pressurized swivel arm.** A 6061-T6 tube carries hydraulic oil at 20 MPa (closed ends) and, at its critical section, a bending moment of 300 N·m and a torque of 300 N·m. Requirements:

* at every point of the critical section (outer and inner surfaces, tension and compression sides), the absolute maximum shearing stress (Eq. 4) at most $\sigma_Y/(2 \times 1.8)$, with **your** Lab 1 yield strength (Tresca, §7.5); also report the factor of safety by von Mises;
* angle of twist at most 3.0° per meter, with **your** Lab 3 $G$;
* outside diameter at most 50.8 mm; the lightest tube from Table 6.

::: {.needspace lines="18"}
:::

| Tube | $D_o$ (mm) | Wall (mm) |
|------------------|------:|------:|
| 31.75 × 3.18 | 31.75 | 3.18 |
| 31.75 × 4.78 | 31.75 | 4.78 |
| 38.1 × 2.11 | 38.10 | 2.11 |
| 38.1 × 3.18 | 38.10 | 3.18 |
| 38.1 × 4.78 | 38.10 | 4.78 |
| 44.45 × 2.11 | 44.45 | 2.11 |
| 44.45 × 3.18 | 44.45 | 3.18 |
| 44.45 × 4.78 | 44.45 | 4.78 |
| 50.8 × 2.11 | 50.80 | 2.11 |
| 50.8 × 3.18 | 50.80 | 3.18 |
| 50.8 × 4.78 | 50.80 | 4.78 |

: Table 6. Catalog for D1 (6061-T6 tubes; compute the mass yourself, density 2700 kg/m³).

These tubes are thick for their diameter, so use the Lamé stresses (Eq. 11 and Appendix D.6) at both surfaces. Use the simulation (preset "D1", which opens at the inner surface) to explore, then verify your final choice by hand: the stresses at the four points, the three principal stresses at the critical point, and its Mohr's circles. Compare your choice with the tube you would have chosen with the in-plane $\tau_{max}$. Submit at most one page: the stresses at the four points, the principal stresses and Mohr's circles at the critical point, a table of the tubes you tried, and one assumption that could invalidate your design, with how you would check it.

| Criterion | Weight |
|------------------------------------------------------------------------------|-------:|
| Section properties and stresses at all four points correct; units correct | 20 % |
| Principal stresses and absolute maximum shear at the critical point, verified by hand and against the simulation | 25 % |
| All requirements checked with **your** $\sigma_Y$ and $G$; governing requirement identified | 20 % |
| Choice justified by a quantitative comparison of alternatives, including the in-plane trap | 25 % |
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
| `config` | Part A: `axis` (load on the tube's axis); Part B: `lever` (load 200 mm to the side); Part C: `pressure` (no load) or `combined` (8 MPa held, load on the lever) |
| `step` | load or pressure step number within the test, from 0 |
| `load_N` | load-cell reading (N) |
| `lever_mm` | nominal lever arm of the load point in use (mm): 0 or 200 |
| `p_MPa` | pressure-transducer reading (MPa) |
| `Ha_ue`, `Hb_ue`, `Hc_ue` | rosette H readings, gages a (along $x$), b (45°) and c (90°), in microstrain, gage factor 2.10, not corrected for $K_t$ |
| `Ka_ue`, `Kb_ue`, `Kc_ue` | rosette K readings, as for H |

: Table A1. Columns of `sample_data.csv`. The indicator was zeroed with no load and no pressure before Parts A, B and C; the `combined` rows continue from the `pressure` rows without re-zeroing.

::: {.needspace lines="16"}
:::

Use these measurements:

| Quantity | Readings |
|---|---|
| $D_o$ (mm) | 38.12, 38.14, 38.13, 38.13 |
| Wall thickness (mm) | 3.20, 3.21, 3.20, 3.21 |
| $L_b$ / $a_L$ (mm) | 250.0 / 200.0 |
| Rosettes | gage factor 2.10 ± 0.5 %, $K_t$ = 1.2 %, $\nu_0$ = 0.285 |

: Table A2. Measurements for the sample data. The micrometer is good to ±0.003 mm, the ball micrometer to ±0.005 mm, the rule to ±0.5 mm, the load cell to ±0.5 % and the pressure transducer to ±0.05 MPa. Take $K_t$ as uncertain by ±0.2 % (absolute).

## Appendix B — Uncertainty quick reference

* Limit $\pm a$ (calibration, accuracy): $u = a/\sqrt{3}$. Reading resolution $r$: $u = r/\sqrt{12}$ (already included when you use the scatter of repeated readings).
* Sum or difference: $u_{x \pm y}^2 = u_x^2 + u_y^2$. Product or quotient: $(u_{xy}/xy)^2 = (u_x/x)^2 + (u_y/y)^2$. Power: $u_{x^k}/x^k = |k|\,u_x/x$.
* Mean of $N$ readings: $u = s/\sqrt{N}$ for the scatter, combined with any calibration term.
* Least-squares line $y = A_0 + A_1x$ through $N$ points: $s_{A_1} = s/\sqrt{\sum(x_i - \bar x)^2}$, with $s^2 = \sum(y_i - A_0 - A_1x_i)^2/(N-2)$ (LINEST in a spreadsheet).
* *Tube properties.* $I = \pi(D_o^4 - D_i^4)/64$ with $D_i = D_o - 2t_w$: change $D_o$ and $t_w$ by their $u$ in turn and add the changes in $I$ in quadrature.
* *Monte Carlo (for principal stresses and angles).* Draw every input (slopes, dimensions, $E$, $\nu$, gage factor, load and pressure calibration, $K_t$) from a normal distribution with its mean and $u$; repeat the whole calculation a few thousand times; the standard deviation of the results is $u$. It keeps the correlations between quantities that share inputs.
* *Example.* A slope of 1.283 µε/N with $u_s$ = 0.005 µε/N, $u_{L_b}/L_b$ = 0.12 %, $u_I/I$ = 0.2 %, load cell 0.29 % and gage factor 0.29 % ($u_c/c$ is negligible): $u_E/E = \sqrt{0.39^2 + 0.12^2 + 0.2^2 + 0.29^2 + 0.29^2}$ % = 0.6 %.
* Report $x \pm U$ with $U = 2u$. Round $U$ to one or two significant figures, and $x$ to the same decimal place.

## Appendix C — Using the simulation

Open `lab08_simulation.html` in any browser; it needs no internet connection. Choose a configuration at the top. In **Stress at a point**, set $\sigma_x$, $\sigma_y$, $\tau_{xy}$ and, for a three-dimensional state, $\sigma_z$, $\tau_{yz}$ and $\tau_{zx}$; drag X′ around Mohr's circle (or use the θ slider) to turn the element. In **Strain rosette**, enter three readings, the rosette type, $E$, $\nu$, $K_t$ and the angle $\beta$ at which the rosette was bonded; the readings appear as points on Mohr's circle for strain. In **Tube, combined loads**, set the tube, the load, its arms, the pressure and the point (angle $\varphi$ from H toward K), on the outer or inner surface, with thin-wall or Lamé pressure stresses; the stats show the readings an ideal rosette would give there. The **readout table** compares each closed form with an independent numerical method: "agree" rows check the formulas, and "different models" rows show how far a formula is from a more complete model. **Push the model past its assumptions** runs prepared experiments. **Export (CSV)** saves the curves, the readout or the convergence study; if your browser blocks the download, the data appears in a box you can copy. The **SI / US customary** toggle converts every input and output.

## Appendix D — Derivations

**D.1 Transformation and Mohr's circle (Eqs. 1–3).** A wedge with faces normal to $x$, $y$ and $x'$ (area $\Delta A$ on the slanted face) is in equilibrium in the $x'$ and $y'$ directions: $\sigma_{x'}\Delta A = \sigma_x\Delta A\cos^2\theta + \sigma_y\Delta A\sin^2\theta + 2\tau_{xy}\Delta A\sin\theta\cos\theta$, and similarly for $\tau_{x'y'}$ (Beer §7.1A). Double-angle identities give Eq. 1. Writing $(\sigma_x - \sigma_y)/2 = R\cos 2\theta_p$ and $\tau_{xy} = R\sin 2\theta_p$ turns Eq. 1 into $\sigma_{x'} = \sigma_{ave} + R\cos(2\theta - 2\theta_p)$ and $-\tau_{x'y'} = R\sin(2\theta - 2\theta_p)$: the point $(\sigma_{x'}, -\tau_{x'y'})$ runs counterclockwise around a circle of radius $R$ as $\theta$ increases (Eqs. 2, 3). This is why X is plotted at $(\sigma_x, -\tau_{xy})$.

**D.2 The absolute maximum (Eq. 4).** For principal axes 1, 2, 3, the normal and shearing stresses on any plane lie inside the largest of the three circles drawn on the pairs of principal stresses and outside the other two (Beer §7.3–7.4); the largest shearing stress is the radius of the largest circle, $(\sigma_1 - \sigma_3)/2$, on planes that bisect axes 1 and 3.

**D.3 Strain, a turned rosette (Eqs. 5–7).** A segment along $\theta$ stretches by $\varepsilon_x\cos^2\theta + \varepsilon_y\sin^2\theta + \gamma_{xy}\sin\theta\cos\theta$ (Beer §7.7A); at 0°, 45° and 90° this gives Eq. 6. If the rosette is bonded at $\beta$, its gages read $\varepsilon(\beta)$, $\varepsilon(45° + \beta)$, $\varepsilon(90° + \beta)$, and Eq. 6 returns the components $\varepsilon_x''$, $\varepsilon_y''$, $\gamma''$ on axes turned by $\beta$: $\varepsilon_x'' - \varepsilon_y'' = (\varepsilon_x - \varepsilon_y)\cos 2\beta + \gamma_{xy}\sin 2\beta$ and $\gamma'' = -(\varepsilon_x - \varepsilon_y)\sin 2\beta + \gamma_{xy}\cos 2\beta$. Two cases measure $\beta$. Under uniaxial stress ($\gamma_{xy} = 0$): $\sin 2\beta = -\gamma''/(\varepsilon_x'' - \varepsilon_y'')$, approximately. Under pure shear ($\varepsilon_x = \varepsilon_y$): $\tan 2\beta = (\varepsilon_x'' - \varepsilon_y'')/\gamma''$ exactly. Turning back is Eq. 1 for strain with $\theta = -\beta$.

**D.4 Transverse sensitivity.** A gage at angle $\theta$ indicates $\hat\varepsilon(\theta) = [\varepsilon(\theta) + K_t\varepsilon(\theta + 90°)]/(1 - \nu_0K_t)$. For a rectangular rosette, gages a and c are transverse to each other: with $k = 1 - \nu_0K_t$, $\varepsilon_a = k(\hat\varepsilon_a - K_t\hat\varepsilon_c)/(1 - K_t^2)$ and $\varepsilon_c = k(\hat\varepsilon_c - K_t\hat\varepsilon_a)/(1 - K_t^2)$. Gage b's transverse direction is 135°, where $\varepsilon(135°) = \varepsilon_a + \varepsilon_c - \varepsilon_b$, so $\varepsilon_b = (k\hat\varepsilon_b - K_t(\varepsilon_a + \varepsilon_c))/(1 - K_t)$. If $\varepsilon(\theta + 90°) = -\nu_0\,\varepsilon(\theta)$, the reading is exact whatever $K_t$.

**D.5 Hooke's law and ν from pressure (Eq. 8).** With $\sigma_z = 0$: $\varepsilon_x = (\sigma_x - \nu\sigma_y)/E$, $\varepsilon_y = (\sigma_y - \nu\sigma_x)/E$, $\gamma_{xy} = \tau_{xy}/G$; solving for the stresses gives Eq. 8 (§2.5). Under pressure alone $\sigma_x/\sigma_\theta = 1/2$ in both Eq. 10 and Eq. 11, so $r = \varepsilon_x/\varepsilon_\theta = (1 - 2\nu)/(2 - \nu)$ and $\nu = (1 - 2r)/(2 - r)$, independent of $E$, the pressure calibration and the gage factor.

**D.6 The thick cylinder (Eq. 11).** A ring element of radius $r$ is in equilibrium if $d\sigma_r/dr + (\sigma_r - \sigma_\theta)/r = 0$. With the radial displacement $u(r)$, $\varepsilon_r = du/dr$ and $\varepsilon_\theta = u/r$; Hooke's law and equilibrium give $u'' + u'/r - u/r^2 = 0$, so $u = C_1r + C_2/r$, and $\sigma_r = A - B/r^2$, $\sigma_\theta = A + B/r^2$. The conditions $\sigma_r(r_i) = -p$ and $\sigma_r(r_o) = 0$ give $A = pr_i^2/(r_o^2 - r_i^2)$ and $B = Ar_o^2$; the closed ends add a uniform $\sigma_x = A$ (the end force $p\pi r_i^2$ over the wall area). At $r_o$ this is Eq. 11; at $r_i$, $\sigma_\theta = p(r_o^2 + r_i^2)/(r_o^2 - r_i^2)$ and $\sigma_r = -p$. Integrating $\sigma_\theta$ from $r_i$ to $r_o$ gives $pr_i$, so the average hoop stress is exactly $pr_i/t_w$ (Eq. 10). The ratio of Eq. 10 to Eq. 11 is $(r_o + r_i)/(2r_i)$.

**D.7 The tube (Eq. 9).** $M = FL_b$ gives $\sigma_x = Mc/I$ at the top (§4.2); $T = Fa_L$ gives $\tau = Tc/J$ everywhere on the surface (§3.1). The shear force $V = F$ produces a shear flow $q = VQ/I$ around the wall, where $Q$ is the first moment of the wall between the top and the point; at mid-height $Q = \tfrac{2}{3}(r_o^3 - r_i^3)$ for the upper half, carried by two walls of total thickness $2(r_o - r_i)$ (§6.1). In the local axes of Figure 1c the torsion and the transverse shear both act in $-y$ on the $+x$ face at K for a downward load on the lever side; on the far side they oppose.

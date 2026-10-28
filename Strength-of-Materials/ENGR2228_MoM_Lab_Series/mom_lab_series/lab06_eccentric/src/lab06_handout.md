# Lab 6 — Eccentric Axial Loading: Superposition, Principal Axes and the Kern

| | |
|---|---|
| **Course** | ENGR 2228 Mechanics of Materials |
| **When** | Week 12, after lectures on Beer 8e §4.7–4.9 and §8.3 |
| **Textbook** | Beer, Johnston, DeWolf, Mazurek, *Mechanics of Materials*, 8th ed. (Beer 8e): §4.7, §4.8, §4.9, §8.3; §2.5 and §2.10 for the conditions of superposition and Saint-Venant's principle; §10.2 for eccentric compression |
| **Session** | 2 hours in the lab, teams of two; report due one week later |
| **Equipment** | Universal testing machine (capacity ≥ 50 kN) with self-aligning clevis grips, steel end blocks with offset pin holes, a gusset end fixture for the angle, 12-channel strain-gage amplifier, displacement transducer (LVDT) on a magnetic stand, calipers, micrometer, radius gage; a 6061-T6 bar 50.8 × 12.7 mm with twelve gages and a 6061-T6 angle 50.8 × 50.8 × 6.35 mm with four gages |
| **Files** | `lab06_simulation.html` (open in any browser, works offline), `sample_data.csv` |

## 1. Learning objectives

After this lab you will be able to:

1. Replace an eccentric axial load by a centric load and two couples, and superpose the stresses to find the normal stress anywhere in the section (§4.7, §4.9).
2. Locate the neutral axis of an eccentrically loaded section, construct its kern, and say where a load can act without producing stress of the opposite sign.
3. Find the principal centroidal axes of an unsymmetric section, explain why Eq. 4.58 must be used in those axes, and quantify the error of ignoring the product of inertia (§4.8).
4. Measure the eccentricity of a load from a strain profile, and separate in-plane bending from out-of-plane misalignment.
5. Recognize when the deformation changes the eccentricity, so that superposition no longer applies, and predict how large the effect is in tension and in compression (§2.5, §10.2).
6. Choose a tension member connected through one leg, using the stresses from eccentricity rather than the average stress.

## 2. Theory

All three tests load a member in axial tension through pins whose line of action is offset from the centroid of the cross-section (Figure 1). The bar of Parts A and C is clamped between steel end blocks; each block has four pin holes, three offset within the plane of the bar's width and one offset through its thickness. The angle of Part B is bolted through one leg to a gusset plate at each end, the way bracing angles are usually connected, so the load acts in the mid-plane of the gusset.

![Figure 1. Test set-ups (schematic, not to scale). (a) The bar between end blocks, front view: three in-plane hole positions, five gages across the width on each face at mid-length, and a pair of gages near one block. (b) Edge view: the out-of-plane hole of Part C and the LVDT. (c) The angle of Part B in section, with the load point in the gusset mid-plane and gages G1–G4.](figures/fig1_setup.png){width=6.4in}

::: {custom-style="Callout"}
**Sign convention (Beer 8e).** The $x$ axis runs along the member, $y$ is up and $z$ completes a right-handed set. Cross-sections are drawn looking along $-x$, so $z$ points to the **left**, as in Beer's Fig. 4.50. Tension is positive. Couple vectors follow the right-hand rule; Eq. 4.58 is written for principal centroidal axes, and a force $P$ (tension positive) through the point $(y_P, z_P)$ is equivalent to $P$ at the centroid plus the couples $M_y = P z_P$ and $M_z = -P y_P$. In the beam-column analysis of Section 2.4, the deflection $w$ is measured from the original centerline **toward the load line**.
:::

::: {custom-style="Callout"}
**Nomenclature.** $P$ axial load; $A$ area; $y$, $z$ coordinates from the centroid $C$; $y_P$, $z_P$ coordinates of the load point; $e$ eccentricity (distance from the centroid to the load line); $M_y$, $M_z$ couple components; $I_y = \int z^2\,dA$, $I_z = \int y^2\,dA$ centroidal moments of inertia; $I_{yz} = \int yz\,dA$ product of inertia; $u$, $v$ principal centroidal axes ($u$ major, $v$ minor), $\theta_p$ angle from $z$ to $u$; $I_u = I_{max}$, $I_v = I_{min}$; $r_z^2 = I_z/A$, $r_y^2 = I_y/A$ squared radii of gyration; $y_0$ position of the neutral axis (N.A.); $h$, $b$ depth (along $y$) and width (along $z$) of the bar; $L$ free length between the end blocks; $a$ distance from a pin to the end of the free length; $k = \sqrt{P/EI}$; $C = M/(Pe)$ bending-moment factor; $w$ deflection toward the load line; $P_{cr}$ buckling load of the member with its end blocks; $\varepsilon_0$, $\beta$ intercept and slope of the strain profile; $e_{eff}$ effective eccentricity; $\varepsilon_b$ bending strain; $T$ torque; $V$ shear force; $J$ polar moment of inertia; $Q$ first moment of area; $E$ modulus of elasticity; $\sigma_Y$ yield strength; $u_x$ standard uncertainty of $x$; $U = 2u$ expanded uncertainty.
:::

Full derivations are in **Appendix D**; this section states each result, what it means, and when it stops applying.

### 2.1 Load in a plane of symmetry

Cut the member at a section away from the ends. Equilibrium of the part on one side requires an internal force $F = P$ at the centroid and a couple $M = Pe$ (§4.7). Superposing the uniform stress of the centric load and the linear stress of the couple (Figure 2a) gives Beer's Eq. 4.50:

$$\sigma_x = \frac{P}{A} - \frac{My}{I}, \qquad M = -Pe \;\text{ for a load at } y_P = e \qquad (1)$$

so that, for a rectangle of depth $h$ loaded at $y_P = e$,

$$\sigma_x = \frac{P}{A}\left(1 + \frac{12\,e\,y}{h^2}\right), \qquad \sigma_{max,min} = \frac{P}{A}\left(1 \pm \frac{6e}{h}\right) \qquad (2)$$

The stress is linear but not uniform, and it vanishes along the **neutral axis**

$$y_0 = -\frac{r_z^2}{e}, \qquad r_z^2 = \frac{I_z}{A} \quad \left(= \frac{h^2}{12} \text{ for a rectangle}\right) \qquad (3)$$

on the side of the centroid away from the load. The farther the load moves out, the closer the neutral axis comes in.

*Worked example.* A 20 × 60 mm rectangle (depth 60 mm) carries $P$ = 24 kN at $e$ = 15 mm: $P/A$ = 20 MPa, $\sigma$ = 20(1 ± 1.5) = 50 MPa and −10 MPa, and the neutral axis is at $y_0 = -300/15 = -20$ mm.

![Figure 2. (a) A load in a plane of symmetry: the uniform stress P/A plus the linear bending stress gives a linear distribution whose neutral axis lies on the far side of the centroid. (b) The kern of a rectangle: a load inside it leaves the whole section in tension; on its boundary the neutral axis touches an edge; outside it the neutral axis enters the section.](figures/fig2_kern.png){width=6.4in}

### 2.2 General eccentric load and the kern

When the load point is off both axes, the force is equivalent to $P$ at the centroid plus two couples. In **principal** centroidal axes, each couple bends the member in its own plane and the three stress fields superpose (§4.9, Eq. 4.58):

$$\sigma_x = \frac{P}{A} - \frac{M_z y}{I_z} + \frac{M_y z}{I_y}, \qquad M_y = P z_P,\quad M_z = -P y_P \qquad (4)$$

or, in terms of the load point,

$$\sigma_x = \frac{P}{A}\left(1 + \frac{y_P\,y}{r_z^2} + \frac{z_P\,z}{r_y^2}\right) \qquad (5)$$

Setting $\sigma_x = 0$ gives a straight neutral axis that crosses the $y$ axis at $-r_z^2/y_P$ and the $z$ axis at $-r_y^2/z_P$; it does not depend on the size of $P$. The **kern** (core) is the region of load points for which the neutral axis does not cut the section, so that the whole section carries stress of one sign. Its boundary is traced by placing the neutral axis along each edge of the section's convex outline. For a rectangle (Figure 2b),

$$\frac{|y_P|}{h/6} + \frac{|z_P|}{b/6} \le 1 \qquad (6)$$

a diamond with half-diagonals $h/6$ and $b/6$. For a solid circle the kern is a circle of radius $c/4$.

### 2.3 Unsymmetric sections: principal axes

Equations 4 and 5 hold only in the principal centroidal axes, those for which the product of inertia vanishes (§4.8, Eq. 4.51). For axes $y$, $z$ that are not principal, rotate them by $\theta_p$ from $z$ toward $y$, where

$$\tan 2\theta_p = \frac{-2I_{yz}}{I_z - I_y}, \qquad I_{max,min} = \frac{I_y + I_z}{2} \pm \sqrt{\left(\frac{I_z - I_y}{2}\right)^2 + I_{yz}^2} \qquad (7)$$

and choose the root for which the second moment about the rotated $z$ axis, called $u$, is $I_{max}$ (Figure 3b). In the principal axes $u$ (major) and $v$ (minor), Eq. 5 reads

$$\sigma_x = \frac{P}{A} + \frac{P\,v_P\,v}{I_u} + \frac{P\,u_P\,u}{I_v} \qquad (8)$$

where $v$ is the distance from the $u$ axis and $u$ the distance from the $v$ axis. For an **equal-leg angle**, symmetry makes the principal axes the line through the heel and the centroid ($u$, major) and the line across it ($v$, minor), and $I_y = I_z$, so $I_{u,v} = I_z \pm |I_{yz}|$. The neutral axis is not parallel to the moment vector unless the moment acts along a principal axis; it always lies between the moment vector and the minor axis (Beer Eq. 4.57). Using Eq. 4 in the axes of the drawing while ignoring $I_{yz}$ is a common and large error (Figure 3a).

![Figure 3. (a) A generic unequal angle in eccentric tension, shaded by stress: the principal axes u and v are tilted from the legs, and ignoring the product of inertia puts the neutral axis in the wrong place. The grey quadrilateral is the kern. (b) The second moment about an axis at angle θ from z is largest where the product of inertia in those axes is zero.](figures/fig3_principal.png){width=6.4in}

*When Eqs. 1–8 apply:* elastic material (superposition, §2.5); a section far enough from the end blocks for the load to have spread (Saint-Venant, §2.10: a few section depths); and **a deformation small enough not to change the eccentricity**. The last condition is the subject of Part C.

### 2.4 When the deformation changes the eccentricity

A member under an eccentric load bends, and its centerline moves sideways. In tension it moves **toward** the load line, so the lever arm of $P$, and with it the bending moment, shrinks; in compression it moves away and the moment grows (Figure 4a). For a member of free length $L$ between rigid end blocks, pinned on the load line a distance $a$ beyond each end, the moment at a distance $x$ along the free length is $M(x) = P\,e\,C(x)$, with (Appendix D.4)

$$C_{mid} = \frac{1}{\cosh u + ka\,\sinh u}, \qquad C_{end} = \frac{\cosh u}{\cosh u + ka\,\sinh u}, \qquad k = \sqrt{\frac{P}{EI}},\quad u = \frac{kL}{2} \qquad (9)$$

in tension. The mid-length deflection toward the load line is $w_{mid} = e\,(1 - C_{mid})$. Here $I$ is the moment of inertia about the axis of bending: for an offset across the width it is $I_z$, for an offset through the thickness it is $I_y$, and for an unsymmetric section each principal component of the offset is reduced by its own factor. In compression, $\cosh$ and $\sinh$ become $\cos$ and $\sin$, the denominator becomes $\cos u - ka\sin u$, and $C$ grows without bound at the buckling load $P_{cr}$, the root of $\cos u = ka\sin u$ ($P_{cr} = \pi^2EI/L^2$ when $a = 0$; this is Beer's secant formula, §10.2). For small loads, Eq. 4 is within 5 % when

$$|P| \lesssim 0.04\,P_{cr} \qquad (10)$$

Figure 4b shows $C$ against $P/P_{cr}$. Note that Eq. 4 is **conservative** in tension (it overstates the bending) and **unconservative** in compression.

![Figure 4. (a) A member between rigid end blocks: tension straightens it toward the load line, compression bows it away. (b) The bending-moment factor C = M/(Pe) against P/P_cr: Eq. 4 assumes C = 1, which holds within 5 % only in a narrow band of loads.](figures/fig4_beamcolumn.png){width=6.4in}

### 2.5 Measuring the eccentricity

The gages on the bar read strain $\varepsilon = \sigma/E$. Average each front gage with the back gage at the same $y$; the average removes any bending through the thickness. Fit the averages with a line, $\varepsilon = \varepsilon_0 + \beta y$. By Eq. 2, $\varepsilon_0 = P/(EA)$ and $\beta = P e/(E I_z)$, so

$$e_{eff} = r_z^2\,\frac{\beta}{\varepsilon_0} \qquad (11)$$

in which $E$, the gage factor and the load all cancel. Half the front-minus-back difference, $\varepsilon_b$, is the strain from bending through the thickness; the **percent bending** $100\,\varepsilon_b/\varepsilon_0$ and the out-of-plane eccentricity $e_z = (b/6)(\varepsilon_b/\varepsilon_0)$ measure how well the load is aligned. In Part C, where the offset is through the thickness, the same ratio gives the bending-moment factor directly:

$$C = \frac{M}{Pe} = \frac{\varepsilon_b}{\varepsilon_0}\,\frac{b}{6e} \qquad (12)$$

### 2.6 Combined loads

Section 8.3 of Beer extends superposition to sections that also carry a torque and shear forces: the internal force-couple system at the section gives the normal stress from $P$ and the two bending couples (Eq. 4), and the shearing stress from the torque and the shear force. For a circular tube of radii $c_1 < c_2$, at a point on the outer surface an angle $\varphi$ from the top (Figure 5),

$$\sigma_x = \frac{P}{A} - \frac{M\,c_2\cos\varphi}{I}, \qquad \tau = \frac{T c_2}{J} \pm \frac{V Q}{I t}, \qquad Q = \frac{(c_2^3 - c_1^3)\sin\varphi}{3}, \quad t = c_2 - c_1 \qquad (13)$$

with the sign of the second term depending on whether the shearing stresses from $T$ and $V$ act in the same direction on that side. Lab 8 measures these components with a strain rosette on such a tube; Extension X2 predicts them.

![Figure 5. (a) A tube cantilever loaded through a lever arm, with a section at distance L_b from the lever. (b) The stress components at the top (H) and at the side (K) of that section.](figures/fig5_combined.png){width=6.4in}

### 2.7 The model in the simulation

`lab06_simulation.html` has three configurations. **Section** evaluates Eqs. 4–8 with exact formulas for each part of the section and draws the stress map, the neutral axis and the kern. It checks them against an independent **numerical solution** that divides the section into $N_g \times N_g$ cells per part, adds up the integrals, and solves the three equilibrium equations $\int\sigma\,dA = P$, $\int\sigma y\,dA = P y_P$, $\int\sigma z\,dA = P z_P$ directly in the drawing axes, without principal axes or Eq. 4.58; the kern is checked by bisection along 180 rays. **Beam-column** compares Eq. 9 with a **finite-difference** solution of the bending equation, and the buckling load with the root of the finite-difference determinant. **Combined loads** compares Eq. 13 with integration over a polar grid.

### 2.8 Uncertainty

Use standard uncertainties $u$; convert a limit $\pm a$ to $u = a/\sqrt{3}$; propagate to first order (Appendix B). For Eq. 11, with $s_{\beta}$ and $s_{\varepsilon_0}$ the standard errors of the fitted slope and intercept,

$$\left(\frac{u_{e_{eff}}}{e_{eff}}\right)^2 = \left(\frac{s_\beta}{\beta}\right)^2 + \left(\frac{s_{\varepsilon_0}}{\varepsilon_0}\right)^2 + \left(\frac{2u_h}{h}\right)^2 + \left(\frac{u_{y}}{\sqrt{2\sum(y_i - \bar y)^2}}\right)^2 \qquad (14)$$

where the last term comes from the uncertainty $u_y$ of each gage position (the front and back positions are averaged). Report $x \pm U$ with $U = 2u$ and draw error bars at $\pm U$. A measurement and a prediction **agree** when

$$|x_{meas} - x_{pred}| \le 2\sqrt{u_{meas}^2 + u_{pred}^2} \qquad (15)$$

Any larger discrepancy needs a physical or procedural explanation, quantified where possible.

## 3. Pre-lab (due at the start of the session)

Answer on paper or in a short document. Show every step, units included. Use Table 1 and the nominal dimensions in Table 2.

**P1 — Estimate before you measure.** (a) Part A, load at $e = h/3$ and $P$ = 30 kN: find $P/A$, $\sigma_{max}$ and $\sigma_{min}$ from Eq. 2, the neutral axis from Eq. 3, and the strains you expect at the gages at $y$ = ±20 mm. (b) Part C at 25 kN, offset $b/2$ through the thickness: the front- and back-face stresses from Eq. 4. (c) For the bar with $a = 0$, compute $P_{cr} = \pi^2EI/L^2$ for bending in the plane of the width and through the thickness, and $P/P_{cr}$ at the largest load of each part. Using Eq. 10, in which part do you expect Eq. 4 to fail, and by roughly how much ($1/C - 1 \approx (\pi^2/8)P/P_{cr}$)? Check the units of every answer.

**P2 — The kern of the bar.** Derive the $h/6$ limit of Eq. 6 from Eq. 2. For the three in-plane holes ($e$ = 0, $h/6$, $h/3$), say whether the load is inside, on or outside the kern, and sketch the stress distribution and the neutral axis for each.

**P3 — The angle.** For the nominal angle of Table 2 (ignore the root fillet), treat the section as two rectangles and find $A$, the centroid, $I_y$, $I_z$ and $I_{yz}$ (parallel-axis theorem; each rectangle's own product of inertia is zero). Find $I_u$ and $I_v$, and the coordinates $(u, v)$ of the load point and of gages G1–G4. Predict $\sigma_x$ at each gage at 30 kN with Eq. 8. Then repeat with Eq. 4 in the $y$, $z$ axes as if $I_{yz}$ were zero, and compare.

**P4 — Reading a strain profile.** Show that Eq. 11 follows from Eq. 2, and that a common error in $E$ or in the gage factor cancels. What does a front-minus-back difference that is the same at all five heights tell you, and what would a difference that varies with $y$ mean?

**P5 — Predict with the simulation.** Open `lab06_simulation.html`. For "Lab Part A: bar, e = h/3", record $\sigma_{max}$, $\sigma_{min}$ and the neutral axis. For "Lab Part B", record the stress at G1–G4 from the plot of stress around the outline (corner A is the tip of the vertical leg; G1 and G2 lie on segment A→B, G3 and G4 on B→C), and the largest stress with $I_{yz}$ ignored. For "Lab Part C", record $C_{mid}$, $C_{end}$ and the mid-length deflection at 25 kN, and the load at which Eq. 4 is 5 % off.

**P6 — Safety.** (a) List the hazards in this lab and how the procedure controls each. (b) The load limits in Section 4 are set with Eq. 4. Why is that safe for Parts A and C, and would it be safe if the same members were loaded in compression?

| Material | $E$ (GPa) | Yield strength $\sigma_Y$ (MPa) |
|---|---:|---:|
| 6061-T6 aluminum | 68.46 ± 0.47 (your Lab 2) | 273.7 ± 1.0 (your Lab 1) |

: Table 1. Reference values. The ± values are standard uncertainties. Replace them with your own team's results where you have them.

## 4. Equipment and safety

| Item | Specification used in this handout |
|---|---|
| Testing machine | Capacity ≥ 50 kN; load accuracy ±0.5 % of reading; self-aligning clevis grips with spherical seats |
| End blocks (bar) | Steel, clamped to each end of the bar; the free length between them is 250 mm. Four reamed 12.75 mm holes for a 12.70 mm pin, 25 mm beyond the block face: in-plane offsets 0, 8.47 and 16.93 mm ($h/6$, $h/3$), and one offset 6.35 mm ($b/2$) through the thickness |
| Gusset fixture (angle) | 9.53 mm steel plate at each end, bolted to the outside of the horizontal leg with two M10 bolts on the leg's gage line (28.6 mm from the heel); pin hole on the bolt line, 25 mm beyond the end of the 300 mm free length |
| Strain gages and amplifier | 120 Ω foil gages, 3 mm grids, aligned with the member axis; gage factor ±1 %; resolution 1 µε |
| LVDT | On a magnetic stand on the machine column, touching the bar at mid-length; resolution 0.001 mm, accuracy ±0.5 % of reading |
| Calipers / micrometer / radius gage / steel rule | Accuracy ±0.02 mm / ±0.003 mm / ±0.4 mm / ±0.5 mm |
| Bar (Parts A and C) | 6061-T6, 50.8 × 12.7 mm ($h \times b$), 400 mm long. Gages at mid-length at $y$ = −20, −10, 0, 10 and 20 mm on the front face ($z = +b/2$) and at the same heights on the back face; one more pair (front and back, $y$ = 0) 40 mm from the lower block |
| Angle (Part B) | 6061-T6 extruded angle, 50.8 × 50.8 × 6.35 mm, 450 mm long. Gages at mid-length on the outer faces: G1 and G2 on the vertical leg, 44 and 12 mm above the heel; G3 and G4 on the horizontal leg, 12 and 44 mm from the heel |

: Table 2. Equipment. If your equipment differs, record its values and use them throughout.

::: {custom-style="Safety"}
**Safety.** Wear safety glasses while any load is applied. **Load limits:** Part A 30 kN in every hole; Part B 30 kN; Part C 25 kN. Set the overload stop about 10 % above each limit before every test. With Eq. 4 these limits keep the largest stress at or below about 0.6 $\sigma_Y$; in tension the true stress is lower still, because the member straightens (Section 2.4). **Never load these set-ups in compression:** the same offsets would amplify the bending instead (Lab 9). **Pins and grips:** insert each pin fully and fit its retaining clip before loading; a pin that walks out releases the specimen suddenly. Keep hands out of the grips and away from the end blocks whenever the crosshead can move, and jog it only with both hands on the controller. **Instruments:** set the LVDT with the load at zero and the crosshead locked; never reach past a loaded specimen to adjust it. Stop at once and unload if the load drops, a pin shifts, or you hear a crack.
:::

## 5. Procedure

1. **Measure.** Record $h$ and $b$ of the bar at three places; the offset of each hole from the block's reference edge, converted to $e$ from the bar's centerline; the free length $L$ and the pin distance $a$; the position of every gage; the legs, thickness and root-fillet radius of the angle; the load point of the gusset fixture (distance from the heel along the leg, and below its outer face); and the positions of G1–G4. Write everything in Table 3. **Check:** repeated readings of each dimension should span no more than 0.03 mm (0.005 mm with the micrometer).
2. **Part A, $e$ = 0.** Pin the bar through the centre holes of both blocks. With a small seating load (about 0.2 kN), zero all gages. Load in 5 kN steps to 30 kN, holding 10 s at each step, then unload. **Check at 10 kN:** the ten mid-length gages should read within about 10 % of $P/(EA)$, and the front and back averages within a few percent of each other.
3. **Part A, $e$ = $h/6$ and $h/3$.** Move both pins to the next holes on the **same** side and repeat. **Check at 10 kN:** with $h/6$, the gages at $y$ = −20 mm should read close to zero; with $h/3$, they should read compression.
4. **Part C.** Move both pins to the out-of-plane holes and bring the LVDT up to the back face at mid-length. Zero, then load in 5 kN steps to 25 kN and unload, recording the LVDT at each step. **Check at 10 kN:** the back-face gages read compression and the LVDT shows the bar moving toward the load line; the deflection returns to within 0.005 mm of zero on unloading.
5. **Part B.** Mount the angle with its gusset fixtures. Zero, then load in 5 kN steps to 30 kN and unload. **Check at 10 kN:** G1, at the tip of the leg that is not connected, should read compression although the member is in tension.
6. **Before you leave:** open the simulation, enter your measured dimensions and load points in each Lab preset, and record its predictions in Table 5 next to your raw readings.

## 6. Data tables

```{=latex}
\renewcommand{\arraystretch}{1.9}
```

| Quantity | Readings | Mean |
|----------------------------------|------------------------------------------------|----------|
| Bar $h$, $b$ (mm) | | |
| Hole offsets $e$: three in-plane, one through the thickness (mm) | | — |
| $L$, $a$ (mm) | | — |
| Gage positions $y$, front / back (mm) | | — |
| Angle legs, thickness, fillet radius (mm) | | |
| Angle load point; G1–G4 positions (mm) | | — |

: Table 3. Dimensions.

| Test | Load | Readings |
|------------------------------|----------|--------------------------------------------------------------|
| Part A, $e$ = 0: ten mid-length gages (µε) | 10 kN | |
| Part A, $h/6$ and $h/3$: gages at $y$ = ±20 mm (µε) | 10 kN | |
| Part C: front, back (µε); LVDT (mm) | 10 kN | |
| Part B: G1–G4 (µε) | 10 kN | |

: Table 4. Spot readings for the checks in the procedure; the data system records every step.

| Quantity | Theory (equation) | Simulation | Measured ± U | Agree (Eq. 15)? |
|----------------------------------------|------------|------------|--------------|-----------|
| $\varepsilon_0$ as $P/A$, $e = h/3$, 30 kN (MPa) | Eq. 2 | | | |
| $e_{eff}$, $e = h/3$, 30 kN (mm) | Eqs. 1, 9 | | | |
| Neutral axis $y_0$, $e = h/3$ (mm) | Eq. 3 | | | |
| Percent bending, $e$ = 0 | — | — | | — |
| $\sigma$ at G1, G2, G3, G4, 30 kN (MPa) | Eq. 8 | | | |
| $C_{mid}$ and $C_{end}$, Part C, 25 kN | Eq. 9 | | | |
| $w_{mid}$, Part C, 25 kN (mm) | Eq. 9 | | | |

: Table 5. Theory vs. simulation vs. measurement.

```{=latex}
\renewcommand{\arraystretch}{1.15}
```

## 7. Analysis

Every answer must (i) show at least two reasoning steps, (ii) include a dimensional check or a limiting-case check, and (iii) end with one to three sentences interpreting the result in words. Questions marked **[Core]** are required of everyone. **[Challenge]** questions are for students who want more. **[Extension]** questions are for honors and independent study.

**A1 [Core] — Strain profile and effective eccentricity.** For each Part A run, average the front and back gages at each height, and at every load step fit $\varepsilon = \varepsilon_0 + \beta y$. Compare $E\varepsilon_0$ with $P/A$. At 30 kN compute $e_{eff}$ (Eq. 11) with its uncertainty (Eq. 14), and compare it with the measured hole offset (what Eqs. 1–2 assume) and with $e\,C_{mid}$ from Eq. 9, both by Eq. 15. *Check:* for $e$ = 0 the slope must vanish within its uncertainty; show that $e_{eff}$ has units of length. *Interpret:* which assumption of Eq. 1 does the comparison test, and how large is its effect on this stocky bar?

**A2 [Core] — Neutral axis and kern.** For each run find the neutral axis from the fit, $y_0 = -\varepsilon_0/\beta$, and compare with Eq. 3 using the hole offset and using $e\,C_{mid}$. Plot the measured stress profiles ($\sigma = E\varepsilon$, with error bars) with the predicted lines, and mark the kern. *Check:* the product $y_0\,e$ should be the same for every run; what is it? *Interpret:* for the $h/6$ hole, is the neutral axis inside or outside the bar, and why does it matter which? Where must a compressive load act on an unreinforced masonry pier so that no part of it cracks in tension?

**A3 [Core] — Alignment.** For each Part A run, compute the percent bending at 30 kN and the out-of-plane eccentricity $e_z$ (Section 2.5), pairing each front gage with the back gage at the same height and allowing for the small difference in their measured positions. *Check:* compare the front-minus-back difference at the five heights; is it constant, as an offset through the thickness predicts? *Interpret:* what would you have concluded about $E$ if you had used only the front gages in the $e$ = 0 run, and why do testing standards limit the percent bending of tension tests?

**A4 [Core] — The angle.** Fit each gage's strain against load and report $\sigma = E \times$ slope × 30 kN with its uncertainty. Predict the four stresses with Eq. 8 from **your** measured dimensions and load point (legs as rectangles), and again with $I_{yz}$ ignored. Tabulate measured, predicted and the difference, and apply Eq. 15. Fit a plane $\sigma = a_0 + a_1y + a_2z$ through the four measured stresses and compare the direction of its neutral axis with Eq. 8. *Check:* verify $I_u + I_v = I_y + I_z$ and that $I_y = I_z$ for an equal-leg angle. *Interpret:* why does G1 read compression in a tension member, and what does that imply for an outstanding leg that is thin?

**A5 [Core] — Theory vs. simulation vs. measurement.** Complete Table 5. Make one figure with each row normalized by its theory value, with error bars at $\pm U$. Explain **every** discrepancy larger than the expanded uncertainty with a named cause, quantified where you can.

**M1 [Core] — Where does the model break?** (a) For Part C, compute $C$ at mid-length and near the block from Eq. 12 at every load step, and plot them against $P$ with error bars, together with Eq. 9 and with $C = 1$ (Eq. 4). Plot the LVDT deflection against $e\,(1 - C_{mid})$. By how much does Eq. 4 overstate the mid-length stress at 25 kN? (b) Find the load at which Eq. 4 is 5 % off for this bar for bending through the thickness and across the width, and express each as $P/P_{cr}$. Is Part A inside the 5 % band? (c) Run "Reverse the load" and describe what happens to $C$ as the compressive load grows. Why is Eq. 4 unconservative there? *Interpret:* state a rule for when an eccentrically loaded member may be designed with Eq. 4.

**C1 [Challenge] — Seeing the straightening in Part A.** Plot $e_{eff}$ against $P$ for the $h/6$ and $h/3$ runs and fit lines. Compare the slopes with those predicted by Eq. 9, and extrapolate to $P = 0$ to compare with the hole offsets. Is the trend resolved by your uncertainties?

**C2 [Challenge] — $EI$ from the deflection.** Fit the Part C LVDT readings with $w_{mid} = e(1 - C_{mid})$, treating $EI$ as the only unknown. Estimate its uncertainty (vary each input by its $u$ and refit) and compare with $E$ from Table 1 times $hb^3/12$. Which input limits the accuracy?

**C3 [Challenge] — What is left over in Part B?** Use the simulation to estimate how much (a) the root fillet (radius from Table 3) and (b) the straightening of Section 2.4, with each principal direction reduced by its own $C_{mid}$, change the predicted stresses at G1–G4. Do they account for the residuals of A4?

**X1 [Extension] — The beam-column equation.** Derive Eq. 9 and its compression counterpart from $EIw'' = P(w - e)$ with the end-block conditions of Appendix D.4. Show that with $a$ = 0 it reduces to Beer's secant formula (§10.2), find the buckling load with end blocks, and show that $1/C_{mid} - 1 \approx (\pi^2/8)P/P_{cr}$ for small loads when $a$ = 0.

**X2 [Extension] — Combined loads: your Lab 8 predictions.** The Lab 8 specimen is a 6061-T6 tube with $D_o$ = 38.10 mm and $D_i$ = 31.75 mm, loaded by $F$ = 600 N at the end of a 200 mm lever arm, with the gage section 250 mm from the lever. Find $M$, $T$ and $V$ at that section, and $\sigma_x$ and $\tau$ at the top and at the side where the two shearing stresses add (Eq. 13). Check your numbers with the simulation's **Combined loads** tab, and say which point you would choose for a rosette that is to measure the torque alone.

**X3 [Extension] — The kern of the angle.** Construct the kern of the nominal angle from the antipoles of the five edges of its convex outline (Appendix D.2), and compare its area and vertices with the simulation. Is the Part B load point inside it? How far would the gusset have to move for the whole section to stay in tension?

## 8. Design problem

**D1 — A single-angle tension brace.** A diagonal brace in an aluminum frame is a single 6061-T6 angle, connected at each end by bolts through one leg to a 9.53 mm gusset plate, the same way as the Part B specimen. It carries a service tension $T$ = 40 kN. The free length between the end connections is 1.50 m, and each connection acts as a rigid block 75 mm long. The load acts in the mid-plane of the gusset, on the bolt line of the connected leg (gage $g$ in Table 6). Requirements:

* the largest normal stress anywhere in the free length, from Eq. 8 with **your** principal-axis analysis, at no more than $\sigma_{allow} = 0.6\,\sigma_Y$ with **your** Lab 1 yield strength;
* the lightest angle from Table 6; for an unequal angle, you choose which leg to connect;
* bolt bearing, the net section at the holes and block shear are checked separately and are not part of this problem.

| Angle (mm) | Connected leg | $t$ (mm) | Gage $g$ (mm) | Mass (kg/m) |
|----------------------|----------|------:|------:|------:|
| L38 × 38 × 4.8 | 38 | 4.76 | 22.2 | 0.92 |
| L51 × 51 × 4.8 | 51 | 4.76 | 28.6 | 1.24 |
| L51 × 51 × 6.4 | 51 | 6.35 | 28.6 | 1.63 |
| L64 × 64 × 6.4 | 64 | 6.35 | 34.9 | 2.07 |
| L76 × 51 × 6.4 | 76 or 51 | 6.35 | 44.5 or 28.6 | 2.07 |
| L76 × 76 × 6.4 | 76 | 6.35 | 44.5 | 2.50 |
| L76 × 76 × 9.5 | 76 | 9.53 | 44.5 | 3.68 |

: Table 6. Catalog for D1 (6061-T6 angles; legs and thickness in mm, root fillets ignored).

Compare your choice with the angle that $P/A \le \sigma_{allow}$ alone would select, and say how much Eq. 9 would let you save if you relied on the straightening of the brace, and why you might not. Submit at most one page: the section properties and load point of your choice in principal axes, the stress check at the governing corner, a table of the candidates you checked, and one assumption that could invalidate your design, with how you would check it.

| Criterion | Weight |
|------------------------------------------------------------------------------|-------:|
| Section properties, principal axes and load point correct for the chosen angle | 25 % |
| Largest stress found at the right corner with Eq. 8; **your** $\sigma_Y$ used | 25 % |
| At least three candidates compared quantitatively, including the connected-leg choice | 20 % |
| Comparison with the $P/A$ design and a reasoned decision about Eq. 9 | 20 % |
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
| Core analysis A1–A5 | 45 |
| M1 — Where does the model break? | 10 |
| D1 — Design problem | 15 |
| Communication: figures, units, uncertainty format | 5 |
| **Total** | **100** |
| Challenge (C1–C3) | up to +10 |

: Table 8. Report grading. Extension questions are graded separately for honors and independent-study credit.

::: pagebreak
:::

## Appendix A — Running the lab without equipment

If the machine is unavailable, use `sample_data.csv`. It holds one row per load step:

| Column | Meaning |
|---|---|
| `part` | `A`, `B` or `C` |
| `config` | Part A: `e0`, `e1`, `e2` for the holes at $e$ = 0, $h/6$, $h/3$; Part C: `ez`; Part B: `angle` |
| `step` | load step number within the test, from 0 |
| `load_N` | axial load $P$ (N), resolution 1 N |
| `w_mid_mm` | LVDT at mid-length, positive toward the load line (mm), resolution 0.001 mm; in-plane for Part A, through the thickness for Part C; blank for Part B |
| `g01_ue` … `g05_ue` | bar: front face ($z = +b/2$) at mid-length, at the five heights of Table A2 (µε). Angle: `g01_ue` to `g04_ue` are G1–G4 |
| `g06_ue` … `g10_ue` | bar: back face ($z = -b/2$) at mid-length, same order (µε) |
| `g11_ue`, `g12_ue` | bar: front and back gages 40 mm from the lower block, $y$ = 0 (µε) |

: Table A1. Columns of `sample_data.csv` (`g02_ue`, `g03_ue`, `g04_ue` and `g07_ue`, `g08_ue`, `g09_ue` are the heights in between). Strains are zeroed at the start of each test, and the last row of each test is the return to zero load.

Use these measurements:

| Quantity | Readings |
|---|---|
| Bar $h$ / $b$ (mm) | 50.84, 50.82, 50.83 / 12.681, 12.678, 12.684 |
| Bar $L$ / $a$ (mm) | 250.0 / 25.0 |
| Hole offsets $e$: e0, e1, e2 / ez (mm) | 0.04, 8.49, 16.95 / 6.40 (through the thickness) |
| Gage heights $y$, front (mm) | −20.1, −10.0, 0.1, 10.1, 20.0 |
| Gage heights $y$, back (mm) | −20.0, −10.1, 0.0, 9.9, 20.1 |
| End pair, distance from the block face (mm) | 40.0 |
| Angle legs $b_V$ / $b_H$ (mm) | 50.86, 50.84, 50.85 / 50.75, 50.77, 50.76 |
| Angle thickness $t$ (mm) | 6.331, 6.334, 6.328, 6.331 |
| Angle root-fillet radius (mm) | 4.8 |
| Angle $L$ / $a$ (mm) | 300.0 / 25.0 |
| Angle load point from the heel, $z$ / $y$ (mm) | −28.58 / −4.76 |
| G1, G2 ($z$ = 0) heights $y$ / G3, G4 ($y$ = 0) positions $z$ (mm) | 44.0, 12.0 / −12.0, −44.0 |

: Table A2. Measurements for the sample data, in the coordinates of Figure 1 (angle: origin at the heel, $y$ up the vertical leg, $z$ to the left, so the horizontal leg lies at negative $z$). Hole offsets and the load point are good to ±0.05 mm, gage positions to ±0.2 mm; other accuracies are those of Table 2.

## Appendix B — Uncertainty quick reference

* Limit $\pm a$ (calibration, accuracy): $u = a/\sqrt{3}$. Reading resolution $r$: $u = r/\sqrt{12}$ (already included when you use the scatter of repeated readings).
* Sum or difference: $u_{x \pm y}^2 = u_x^2 + u_y^2$. Product or quotient: $(u_{xy}/xy)^2 = (u_x/x)^2 + (u_y/y)^2$. Power: $u_{x^k}/x^k = |k|\,u_x/x$.
* Mean of $N$ readings: $u = s/\sqrt{N}$ for the scatter, combined with any calibration term.
* Least-squares line $y = A_0 + A_1x$ through $N$ points: $s_{A_1} = s/\sqrt{\sum(x_i - \bar x)^2}$, $s_{A_0} = s\sqrt{\sum x_i^2/(N\sum(x_i - \bar x)^2)}$, with $s^2 = \sum(y_i - A_0 - A_1x_i)^2/(N-2)$ (LINEST in a spreadsheet).
* *Ratios cancel common errors.* In Eqs. 11 and 12, $E$, the load and any gage-factor error shared by all gages cancel; only the scatter between gages remains.
* *A quantity from a fitted model (C2).* Change the measured input by its $u$, refit, and take the change in the output as its $u$.
* *Example.* Three micrometer readings of $b$ with $s$ = 0.003 mm and accuracy ±0.003 mm: $u = \sqrt{0.003^2/3 + 0.003^2/3}$ = 0.0024 mm, or 0.02 % of 12.68 mm; in $I_y = hb^3/12$ it becomes 0.06 %.
* Report $x \pm U$ with $U = 2u$. Round $U$ to one or two significant figures, and $x$ to the same decimal place.

## Appendix C — Using the simulation

Open `lab06_simulation.html` in any browser; it needs no internet connection. Choose a configuration and a preset, then move the sliders. In **Section**, drag the black diamond (or use the arrow keys when the drawing has focus, or the sliders) to move the load point; the drawing shows the stress map, the neutral axis, the kern and the principal axes, and the plots show the stress around the outline and the extreme stresses as the load point moves out from the centroid. The purple curve appears whenever $I_{yz} \neq 0$ and shows the result of ignoring it. **Beam-column** shows how the bending-moment factor and the mid-length deflection change with the load in tension and in compression, for the free length and end blocks you set. **Combined loads** shows the stress components around a tube loaded through a lever arm. The **readout table** compares each closed-form result with the independent numerical solution: "agree" rows check the formulas, and "different models" rows show how far a formula is from a more complete model. **Push the model past its assumptions** runs prepared experiments. **Export (CSV)** saves the curves, the readout or the convergence study; if your browser blocks the download, the data appears in a box you can copy. The **SI / US customary** toggle converts every input and output.

## Appendix D — Derivations

**D.1 Superposition (Eqs. 1, 2, 4, 5).** A force $P$ along a line through the point $(y_P, z_P)$ of the section, parallel to $x$, has moments $M_y = P z_P$ and $M_z = -P y_P$ about the centroidal axes (the moment of a force $P\mathbf{i}$ at $y_P\mathbf{j} + z_P\mathbf{k}$ is $(y_P\mathbf{j} + z_P\mathbf{k}) \times P\mathbf{i} = P z_P\mathbf{j} - P y_P\mathbf{k}$). Away from the ends, the stress is linear, $\sigma_x = \sigma_0 + B_y y + B_z z$, because plane sections remain plane and the material is elastic. Equilibrium with the force and couples requires $\int\sigma_x\,dA = P$, $\int y\,\sigma_x\,dA = P y_P$ and $\int z\,\sigma_x\,dA = P z_P$. With centroidal axes, $\int y\,dA = \int z\,dA = 0$, so $\sigma_0 = P/A$, $I_zB_y + I_{yz}B_z = Py_P$ and $I_{yz}B_y + I_yB_z = Pz_P$. In principal axes $I_{yz} = 0$, so $B_y = P y_P/I_z$ and $B_z = P z_P/I_y$, which is Eq. 5, and Eq. 4 after substituting $M_y$ and $M_z$. In other axes, ignoring $I_{yz}$ solves the wrong equations. Eqs. 1–2 are the case $z_P = 0$ with $I = bh^3/12$. The simulation's numerical solution solves these three equations directly in the drawing axes.

**D.2 Neutral axis and kern (Eqs. 3, 6).** Setting Eq. 5 to zero gives the line $1 + y_P y/r_z^2 + z_P z/r_y^2 = 0$, with intercepts $-r_z^2/y_P$ and $-r_y^2/z_P$; it does not depend on $P$. Conversely, a neutral axis along a given line $\alpha y + \gamma z = 1$ (in principal axes) requires the load at $y_P = -\alpha r_z^2$, $z_P = -\gamma r_y^2$: the **antipole** of the line. Placing the neutral axis along each edge of the convex outline gives one kern vertex per edge; the kern is the polygon through them. For the rectangle, the edge $y = -h/2$ ($\alpha = -2/h$) gives $y_P = 2r_z^2/h = h/6$, which is Eq. 6. For a circle of radius $c$, $r^2 = c^2/4$ and a tangent at distance $c$ gives a kern radius $c/4$.

**D.3 Principal axes (Eq. 7).** Rotate the axes by $\theta$ from $z$ toward $y$: $u = z\cos\theta + y\sin\theta$, $v = -z\sin\theta + y\cos\theta$. Then $I_u = \int v^2\,dA = \frac{I_z + I_y}{2} + \frac{I_z - I_y}{2}\cos 2\theta - I_{yz}\sin 2\theta$ and $I_{uv} = \int uv\,dA = \frac{I_z - I_y}{2}\sin 2\theta + I_{yz}\cos 2\theta$. $I_u$ is extreme where $dI_u/d\theta = -2I_{uv} = 0$, which gives Eq. 7; of the two roots, the one with $I_u = I_{max}$ defines the major axis. For an equal-leg angle with legs $b$ and thickness $t$, the line through the heel and the centroid is an axis of symmetry and therefore principal. For each leg as a rectangle, the product of inertia about its own centroid is zero, so $I_{yz} = \sum A_i\,\bar y_i\,\bar z_i$ with $\bar y_i$, $\bar z_i$ the distances of each leg's centroid from the section's centroid.

**D.4 The member with end blocks (Eqs. 9, 10).** Let $w(x)$ be the deflection of the centerline toward the load line, so that the lever arm of $P$ at $x$ is $e - w$ and the bending moment is $M = P(e - w)$. With Beer's convention ($y$ up, $EI\,y'' = M$, Ch. 9) and the load line on the positive side, $EI\,w'' = P(w - e)$, that is $w'' - k^2w = -k^2e$ with $k^2 = P/EI$. Each end block is rigid and pinned on the load line a distance $a$ beyond the free length, so $w(0) - a\,w'(0) = 0$ and $w(L) + a\,w'(L) = 0$. The symmetric solution is $w = e\,[1 - C\cosh k(x - L/2)]$; the boundary condition gives $C = 1/(\cosh u + ka\sinh u)$ with $u = kL/2$, and $M(x) = PeC\cosh k(x - L/2)$, which is Eq. 9. For compression, $k^2 = |P|/EI$ and the equation becomes $w'' + k^2w = k^2e$, with $w = e[1 - C\cos k(x - L/2)]$ and $C = 1/(\cos u - ka\sin u)$; $C$ is unbounded when $\cos u = ka\sin u$, which defines $P_{cr}$ ($u = \pi/2$ when $a$ = 0). For small loads and $a$ = 0, $1/C - 1 = \cosh u - 1 \approx u^2/2 = (\pi^2/8)(P/P_{cr})$, which is 0.05 at $P/P_{cr} \approx 0.04$ (Eq. 10); short end blocks change the coefficient only slightly when $P$ is scaled by their own $P_{cr}$. An unsymmetric section bends about both principal axes; to this order each principal component of the offset obeys Eq. 9 with its own $EI$, and twisting is neglected.

**D.5 Measured quantities (Eqs. 11, 12).** By Eq. 2, $E\varepsilon = (P/A)(1 + ey/r_z^2)$, so $\varepsilon_0 = P/(EA)$ and $\beta = Pe/(EAr_z^2)$, and $r_z^2\beta/\varepsilon_0 = e$: Eq. 11. For an offset $e$ through the thickness, the bending strain at the faces is $\varepsilon_b = M(b/2)/(EI_y)$ and $\varepsilon_0 = P/(EA)$, so $\varepsilon_b/\varepsilon_0 = M(b/2)A/(PI_y) = 6M/(Pb)$ and $M/(Pe) = (\varepsilon_b/\varepsilon_0)\,b/(6e)$: Eq. 12. The gage positions enter the slope through $\sum(y_i - \bar y)^2$, which gives the last term of Eq. 14.

**D.6 The tube (Eq. 13).** For a cantilever loaded through a lever, a free body of the part beyond the section gives a bending moment $M = -FL_b$ (hogging, so the top is in tension), a torque $T = Fa_L$ and a shear force $V = F$. On the outer surface, $y = c_2\cos\varphi$, which gives $\sigma_x$. The torsional shearing stress is $Tc_2/J$ everywhere on the surface (§3.1). For the shearing stress from $V$, cut the wall radially at $\varphi$; the part of the wall between the top and the cut has $Q = \int_0^{\varphi}\int_{c_1}^{c_2}(r\cos\theta)\,r\,dr\,d\theta = (c_2^3 - c_1^3)\sin\varphi/3$, and the cut has length $t = c_2 - c_1$, so $\tau = VQ/(It)$ (§6.4). At the side ($\varphi$ = 90°) this equals the full-section value $VQ_{NA}/(I\cdot 2t)$, and for a thin wall it approaches $2V/A$.

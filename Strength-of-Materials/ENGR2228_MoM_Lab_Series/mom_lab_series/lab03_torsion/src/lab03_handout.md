# Lab 3 — Torsion: Elastic, Elastoplastic and Noncircular Shafts

| | |
|---|---|
| **Course** | ENGR 2228 Mechanics of Materials |
| **When** | Week 7, after lectures on Beer 8e Ch. 3 |
| **Textbook** | Beer, Johnston, DeWolf, Mazurek, *Mechanics of Materials*, 8th ed. (Beer 8e): §3.1A–3.1C, §3.2, §3.3, §3.4, §3.5, §3.6, §3.7, §3.8, §3.9, §3.10; §2.8 for the relation among E, ν and G |
| **Session** | 2 hours in the lab, teams of two; report due one week later |
| **Equipment** | Torsion testing machine (capacity ≥ 60 N·m) with torque cell and head-rotation encoder, troptometer (twist gage) with 50.8 mm gage length, micrometer, three specimens: 1018 steel, 6061-T6 aluminum and gray cast iron |
| **Files** | `lab03_simulation.html` (open in any browser, works offline), `sample_data.csv` |

## 1. Learning objectives

After this lab you will be able to:

1. Derive the shear strain, shear stress and angle of twist of a circular shaft from compatibility (plane sections rotate), Hooke's law in shear and equilibrium, and state with numbers when each result applies (§3.1–3.2).
2. Measure the modulus of rigidity $G$ with a propagated uncertainty, and test it against $E/[2(1+\nu)]$ from your Lab 1 and Lab 2 measurements (§2.8).
3. Extract a shear yield strength from the torque–twist curve with the elastic–perfectly plastic model, predict the permanent twist and residual stresses after unloading, and show where the model fails (§3.6–3.8).
4. Explain the fracture surfaces of ductile and brittle shafts from the stresses on inclined planes, and compare the torsional modulus of rupture with the tensile strength (§3.1C, §3.6).
5. Apply the corrections for noncircular and thin-walled sections, and size a transmission shaft against strength and stiffness requirements (§3.4, §3.5, §3.9, §3.10).

## 2. Theory

A torsion tester (Figure 1) twists a round specimen between a fixed head, which holds the torque cell, and a drive head, which turns. A troptometer clamped to the reduced section measures the angle of twist $\varphi$ over a gage length $L$; the drive head's encoder measures the total rotation of the grips. Every formula you will use follows from compatibility (how the cross-sections move), the material's shear stress–strain law, and equilibrium (the stresses on a cut must add up to the torque).

![Figure 1. Torsion test set-up (schematic, not to scale): the troptometer measures the twist φ over the 50.8 mm gage length; the drive head's encoder measures the rotation of the grips.](figures/fig1_setup.png){width=6.3in}

::: {custom-style="Callout"}
**Sign convention (Beer 8e).** Torque and angle of twist follow the right-hand rule: an internal torque $T$ is positive when its vector, drawn as a double arrow, points out of the cut section (along the outward normal), and $\varphi$ is positive in the same sense. In this lab every torque and twist is positive. The shear stress $\tau$ and shear strain $\gamma$ on a cross-section are reported as magnitudes; their direction is perpendicular to the radius, in the sense of $T$.
:::

::: {custom-style="Callout"}
**Nomenclature.** $T$ torque; $\varphi$ angle of twist over the gage length $L$; $\theta = \varphi/L$ twist per unit length; $c$ outer radius ($d = 2c$); $c_i$ inner radius of a hollow shaft; $\rho$ radial distance from the axis; $J$ polar moment of inertia; $\gamma$ shear strain; $\tau$ shear stress; $G$ modulus of rigidity; $\tau_Y$ shear yield strength; $T_Y$, $\varphi_Y$ torque and twist at first yield; $\rho_Y$ radius of the elastic core; $T_p$ fully plastic torque; $T_U$ maximum torque; $R_T$ modulus of rupture in torsion; $\varphi_p$ permanent twist after unloading; $\tau_{res}$ residual shear stress; $L_c$ reduced-section length; $C_m$ torsional compliance of the shoulders, grips and drive (°/N·m); $\Delta_{head}$ drive-head rotation; $\Delta_{toe}$ backlash taken up at low torque; $a$, $b$ long and short sides of a rectangle; $c_1$, $c_2$ rectangle coefficients; $t$ wall thickness; $A_m$ area enclosed by the wall's mid-line; $\sigma_{UT}$ tensile strength; $u$ standard uncertainty; $U = 2u$ expanded uncertainty.
:::

Full derivations of the results below are in **Appendix D**; this section states each result, what it means, and when it stops applying.

### 2.1 Elastic torsion of a circular shaft

![Figure 2. (a) A line on the surface becomes a helix: plane cross-sections rotate rigidly, so γ grows linearly with ρ. (b) Elastic shear stress across a section. (c) At the surface the material is in pure shear; on planes at 45° the same state is a tension σ = +τ and a compression σ = −τ.](figures/fig2_kinematics.png){width=6.4in}

Because a circular shaft is axisymmetric, its cross-sections stay plane and rotate rigidly (§3.1B). A fiber at radius $\rho$ is sheared by

$$\gamma = \frac{\rho\,\varphi}{L} \qquad (1)$$

which holds whatever the material does. In the elastic range Hooke's law in shear,

$$\tau = G\gamma \qquad (2)$$

makes the stress linear in $\rho$, and equilibrium of a cut requires

$$T = \int_A \rho\,\tau\,dA \qquad (3)$$

Together they give the elastic torsion formulas (§3.1C, §3.2)

$$\tau = \frac{T\rho}{J}, \qquad \tau_{max} = \frac{Tc}{J} \qquad (4)$$

$$J = \frac{\pi c^4}{2} \ \text{(solid)}, \qquad J = \frac{\pi (c^4 - c_i^4)}{2} \ \text{(hollow)} \qquad (5)$$

$$\varphi = \frac{TL}{JG} \qquad (6)$$

*Worked example.* A solid steel shaft, $d$ = 20 mm, $L$ = 0.80 m, $G$ = 79.5 GPa, carrying 100 N·m: $J$ = 15 708 mm⁴, $\tau_{max}$ = 63.7 MPa and $\varphi$ = 0.0641 rad = 3.67°.

For an isotropic material $G$ is not independent of $E$ and $\nu$ (§2.8; derived in Lab 2, Appendix D.2):

$$G = \frac{E}{2(1+\nu)} \qquad (7)$$

*When Eqs. 4–6 apply:* elastic material; circular section (solid or hollow) that does not change along $L$; and points at least about one diameter away from the grips, shoulders and any change of section (Saint-Venant). Near a shoulder fillet the stress is raised by a concentration factor $K$ (§3.5).

### 2.2 Elastoplastic torsion

Equation 1 still holds after yielding, so the strain stays linear in $\rho$ while the stress follows the material's curve. For an **elastic–perfectly plastic** material (Beer's model, §3.7), yield starts at the surface when

$$T_Y = \frac{\tau_Y J}{c}, \qquad \varphi_Y = \frac{\tau_Y L}{Gc} \qquad (8)$$

Beyond that, a plastic shell at $\tau = \tau_Y$ surrounds an elastic core of radius

$$\rho_Y = c\,\frac{\varphi_Y}{\varphi} \qquad (9)$$

(Figure 3a), and integrating Eq. 3 over the core and the shell gives, for a solid shaft,

$$T = \frac{4}{3}T_Y\left[1 - \frac{1}{4}\left(\frac{\varphi_Y}{\varphi}\right)^3\right], \qquad \varphi \ge \varphi_Y \qquad (10)$$

which approaches the **fully plastic torque**

$$T_p = \frac{4}{3}T_Y = \frac{2\pi}{3}c^3\tau_Y \qquad (11)$$

At $\varphi = 2\varphi_Y$, $T = 1.292\,T_Y$: twice the twist buys only 29 % more torque. Derivation and the hollow-shaft version: Appendix D.3.

![Figure 3. Elastoplastic torsion of a solid shaft, normalized. (a) The plastic shell grows inward as φ increases. (b) Torque–twist: the elastic–perfectly plastic curve approaches (4/3)T_Y; unloading follows the elastic slope. (c) Residual stress after unloading from 3φ_Y.](figures/fig3_elastoplastic.png){width=6.4in}

**Unloading and residual stresses.** Unloading is elastic, so it subtracts the elastic solution for the torque removed (§3.8). After loading to $(\varphi_{max}, T_{max})$ and releasing,

$$\tau_{res}(\rho) = \tau(\rho) - \frac{T_{max}\,\rho}{J}, \qquad \varphi_p = \varphi_{max} - \frac{T_{max}L}{JG} \qquad (12)$$

The residual stresses carry zero net torque: the surface is left in reverse shear and the interior in forward shear (Figure 3c). Derivation: Appendix D.4.

*When Eqs. 8–12 apply:* the material must really have a flat yield plateau. Hot-rolled steel comes close at small plastic strains; aluminum and work-hardened metals do not (their torque keeps rising), and Eq. 10 then describes them only approximately. Eq. 12 also assumes that unloading does not cause reverse yielding.

### 2.3 Strength, fracture and the modulus of rupture

Applying the elastic formula at the maximum torque defines the **modulus of rupture in torsion** (§3.6)

$$R_T = \frac{T_U\,c}{J} \qquad (13)$$

It is a convenient index, not a stress: for a ductile shaft the outer fibers are not carrying $T_Uc/J$. For a flat plateau, $T_U = T_p$ and $R_T = \frac{4}{3}\tau_Y$, so $R_T$ overstates the shear strength by up to 33 %. The fully plastic estimate $3T_U/(2\pi c^3)$ errs the other way.

![Figure 4. (a) A ductile shaft fails in shear on a plane perpendicular to its axis. (b) A brittle shaft fails in tension on a 45° helix.](figures/fig4_fracture.png){width=6.0in}

**Fracture surfaces.** In pure shear, the planes at 45° to the axis carry normal stresses and no shear (Figure 2c; §3.1C):

$$\sigma_{45°} = \pm\tau \qquad (14)$$

A ductile metal yields and fails in shear, on the transverse plane where $\tau$ is largest. A brittle material such as gray cast iron is weaker in tension than in shear, so it fails when $\tau$ at the surface reaches its tensile strength $\sigma_{UT}$, on the 45° helix perpendicular to $\sigma = +\tau$ (Figure 4). Derivation: Appendix D.5.

### 2.4 What the drive head measures

The drive head's rotation includes the twist of the whole reduced section ($L_c$ = 76.2 mm, not just the gage), the shoulders, grips and drive train, and a backlash $\Delta_{toe}$ taken up at low torque:

$$\Delta_{head} = \frac{L_c}{L}\,\varphi + C_m T + \Delta_{toe} \qquad (15)$$

After the troptometer is removed, solve Eq. 15 for $\varphi$ to get the twist from the head reading. The surface shear strain is then $\gamma_c = c\varphi/L$ (Eq. 1). Derivation: Appendix D.7.

### 2.5 Noncircular and thin-walled sections

![Figure 5. (a) In a rectangle the shear stress is largest at the middle of the long sides and zero at the corners. (b) The coefficients of Eq. 16 approach 1/3 for a thin strip. (c) In a thin-walled tube the shear flow q = τt is constant around the wall.](figures/fig5_noncircular.png){width=6.4in}

A noncircular section **warps**: its cross-sections do not stay plane, so Eqs. 1 and 4 do not apply. For a rectangle with long side $a$ and short side $b$, the elasticity solution gives (§3.9)

$$\tau_{max} = \frac{T}{c_1 a b^2}, \qquad \varphi = \frac{TL}{c_2 a b^3 G} \qquad (16)$$

with $c_1$ and $c_2$ depending only on $a/b$ (Figure 5b; $c_1$ = 0.208 and $c_2$ = 0.141 for a square). For a thin-walled closed tube with wall thickness $t$ around a mid-line enclosing the area $A_m$ (§3.10),

$$\tau = \frac{T}{2tA_m}, \qquad \varphi = \frac{TL}{4A_m^2G}\oint\frac{ds}{t} \qquad (17)$$

*When Eqs. 16–17 apply:* elastic material, ends free to warp. Eq. 17 also assumes that $\tau$ is uniform through the wall, which for a circular tube is off by about $t/(2r_m)$, where $r_m$ is the mid-wall radius.

### 2.6 Recovering the shear stress–strain curve

The torque is an integral of $\tau$ over the section, so the torque–twist curve hides the material's $\tau$–$\gamma$ curve. Differentiating Eq. 3 with Eq. 1 recovers it (Nadai's method; Appendix D.6):

$$\tau(\gamma_c) = \frac{1}{2\pi c^3}\left[3T + \gamma_c\frac{dT}{d\gamma_c}\right] \qquad (18)$$

where $\gamma_c = c\varphi/L$ is the surface shear strain. For a flat plateau ($dT/d\gamma_c = 0$) Eq. 18 gives $3T_p/(2\pi c^3) = \tau_Y$, consistent with Eq. 11.

### 2.7 The model in the simulation

`lab03_simulation.html` has two configurations. **Circular shaft** evaluates Eqs. 4–12 in closed form and compares them with an **independent numerical solution** that divides the section into $N$ rings, evaluates $\tau(\rho\varphi/L)$ from the chosen stress–strain law in each ring, and adds up Eq. 3. It never uses Eqs. 10–12. The law can be elastic–perfectly plastic (to check the formulas) or the material's own curve (to see where the formulas fail). **Noncircular / thin wall** compares Eq. 16, with $c_1$ and $c_2$ from the elasticity series, with a **finite-difference** solution for the Prandtl stress function on a grid, and compares Eq. 17 with the exact hollow-circle solution.

### 2.8 Uncertainty

Use standard uncertainties $u$; convert a limit $\pm a$ to $u = a/\sqrt{3}$; propagate to first order (Appendix B). From Eq. 6, $G = kL/J$, where $k$ is the fitted slope of $T$ against $\varphi$, and $J \propto d^4$:

$$\left(\frac{u_G}{G}\right)^2 = \left(\frac{s_k}{k}\right)^2 + \left(\frac{4u_d}{d}\right)^2 + \left(\frac{u_L}{L}\right)^2 + \left(\frac{u_T}{T}\right)^2 + \left(\frac{u_\varphi}{\varphi}\right)^2 \qquad (19)$$

The factor 4 is why the diameter is measured with a micrometer, not calipers. Report $x \pm U$ with $U = 2u$ and draw error bars at $\pm U$. A measurement and a reference **agree** when

$$|x_{meas} - x_{ref}| \le 2\sqrt{u_{meas}^2 + u_{ref}^2} \qquad (20)$$

Any larger discrepancy needs a physical or procedural explanation, quantified where possible.

## 3. Pre-lab (due at the start of the session)

Answer on paper or in a short document. Show every step, units included. Use Table 1 and the nominal diameter $d$ = 6.35 mm.

**P1 — Estimate before you measure.** (a) Estimate $\tau_Y \approx \sigma_Y/\sqrt{3}$ (the von Mises relation between tension and shear) for the steel and the aluminum, and from it $T_Y$, $T_p$ and $\varphi_Y$ over the 50.8 mm gage. (b) The troptometer resolves 0.01°. What fraction of $\varphi_Y$ is that? (c) An upper bound on the steel's maximum torque comes from letting the whole section carry Lab 1's true fracture stress divided by $\sqrt{3}$, about 430 MPa. Use Eq. 11 with $\tau$ = 430 MPa. Is the 60 N·m machine large enough? (d) Estimate the cast iron's fracture torque from Eq. 4 with $\tau_{max} = \sigma_{UT}$. Check the units of every answer.

**P2 — Elastoplastic torque.** (a) Starting from Eqs. 1, 3 and the elastic–perfectly plastic law, derive Eq. 10. (b) Check it at $\varphi = \varphi_Y$ and as $\varphi \to \infty$. (c) For a hollow shaft with $c_i/c$ = 0.6, find $T_p/T_Y$ and explain why it is smaller than 4/3.

**P3 — Unloading.** A solid steel shaft is twisted to $3\varphi_Y$ and released. Using Eqs. 10 and 12, find (a) $T_{max}/T_Y$, (b) the permanent twist $\varphi_p/\varphi_Y$, and (c) the residual stress at the surface and at $\rho_Y$, as fractions of $\tau_Y$. (d) Check that the residual stresses produce no net torque.

**P4 — Sensitivity.** (a) A 0.02 mm error in $d$ = 6.35 mm: by what percentage does it change $J$, and therefore $G$ from Eq. 6? (b) What diameter uncertainty would keep that term below 0.25 %? (c) Why does the slope of torque against **head rotation** not give $G$? Use Eq. 15.

**P5 — Predict with the simulation.** Open `lab03_simulation.html`. For the presets "Lab specimen: 1018 steel" and "Lab specimen: 6061-T6 aluminum", record $T_Y$, $T_p$ and the numerical torque at 10° over the gage. Switch the law to **Elastic–perfectly plastic** and back: for which material does the choice matter, and why? Run "Overload, then unload" and record the permanent twist.

**P6 — Safety.** (a) List the three hazards in this lab and how the procedure controls each. (b) Why must the troptometer come off before the steel enters large plastic twist, and why is it not used at all on the cast iron?

| Material | $E$ (GPa) | $\nu$ | $\sigma_Y$ (MPa) | Other |
|---|---:|---:|---:|---|
| 1018 steel, hot rolled | 205 ± 3 | 0.29 ± 0.01 | 297 (your Lab 1 lower yield point) | Lab 1 true fracture stress about 745 MPa |
| 6061-T6 aluminum | 68.46 ± 0.47 (your Lab 2) | 0.330 ± 0.003 (your Lab 2) | 274 (0.2 % offset, Lab 1) | — |
| Gray cast iron, class 30 | about 100 | about 0.26 | — | $\sigma_{UT}$ = 214 ± 15 MPa |

: Table 1. Reference values. The ± values are standard uncertainties. Replace the Lab 1 and Lab 2 values with your own team's results where you have them.

## 4. Equipment and safety

| Item | Specification used in this handout |
|---|---|
| Torsion testing machine | Capacity ≥ 60 N·m; torque accuracy ±0.5 % of reading; drive-head encoder resolution 0.1° |
| Troptometer | Gage length $L$ = 50.80 ± 0.05 mm; resolution 0.01°; accuracy ±0.5 % of reading |
| Micrometer | Resolution 0.001 mm; accuracy ±0.003 mm |
| Specimens | Round, $d$ = 6.35 mm (0.250 in) reduced section, $L_c$ = 76.2 mm (3.00 in), hexagonal ends; 1018 steel, 6061-T6 aluminum, gray cast iron |

: Table 2. Equipment. If your equipment differs, record its values and use them throughout.

::: {custom-style="Safety"}
**Safety.** Wear safety glasses from the moment a specimen is in the grips until it is out. **Rotating head:** keep hands, sleeves, hair and lanyards clear of the drive head whenever the motor is enabled; tie back long hair. **Load limit:** the machine's capacity is 60 N·m; set its overload stop at 40 N·m. The expected maxima are about 28 N·m (steel), 15 N·m (aluminum) and 11 N·m (cast iron). Stop the test if the torque exceeds 35 N·m. **Troptometer:** remove it at 10° of twist on the gage, with the motor stopped and disabled; large twist would wind its arms into the specimen. **Cast iron:** brittle fracture releases stored energy and can throw fragments; close the guard, do not fit the troptometer, and stand to the side. Fracture surfaces of all three specimens are sharp; handle them with gloves.
:::

## 5. Procedure

1. **Measure the diameters.** Measure $d$ of each specimen with the micrometer at three places along the reduced section, twice at each place (rotate 90°), and record the six readings in Table 3. **Check:** the readings should span no more than 0.005 mm.
2. **Zero the torque** with the steel specimen held in the fixed head only. Then engage the drive head's hex and **check** that the torque stays within ±0.05 N·m.
3. **Fit the troptometer** to the steel specimen with its collars 50.80 mm apart, centered on the reduced section, and zero it.
4. **Load the steel elastically.** Run the drive at 0.25°/s, recording torque, troptometer and head rotation at 4 Hz. **Check at about 4 N·m:** $T/\varphi$ (in N·m per radian) times $L/J$ should be within 10 % of your P1 estimate of $G$; if not, re-seat the troptometer.
5. **Unload and reload.** At a troptometer reading of about 6° (about $3\varphi_Y$), reverse the drive at the same rate until the torque returns to zero. Record the permanent twist on the troptometer, then reload.
6. **Remove the troptometer** at 10° on the gage: stop and disable the motor, unclamp the troptometer, and step clear.
7. **Twist to fracture** at 15°/s, recording at 2 Hz. Note the maximum torque, the head rotation at fracture and the number of revolutions.
8. **Inspect the fracture surface.** Sketch or photograph it. Note whether it is flat or helical and whether there are circular smear marks.
9. Repeat steps 2–8 for the aluminum. Omit the unloading in step 5.
10. **Cast iron:** close the guard and do not fit the troptometer. Twist at 0.25°/s, recording at 4 Hz, until it fractures. Photograph the fracture surface next to the steel's.
11. **Before you leave:** open the simulation, choose each specimen preset, enter your measured diameter, and record its predictions in Table 5 next to your raw readings.

## 6. Data tables

```{=latex}
\renewcommand{\arraystretch}{1.9}
```

| Specimen | $d$ readings, 0° and 90°, at three places (mm) | Mean $d$ (mm) | Std. dev. (mm) |
|---|---|---|---|
| 1018 steel | | | |
| 6061-T6 aluminum | | | |
| Gray cast iron | | | |

: Table 3. Specimen diameters.

| Quantity | 1018 steel | 6061-T6 aluminum | Gray cast iron |
|---|---|---|---|
| Torque at 1° on the troptometer (N·m) | | | — |
| Torque at 2° (N·m) | | | — |
| Torque at 5° (N·m) | | | — |
| Torque at 10°, troptometer removed (N·m) | | | — |
| Unloaded from (°, N·m) / permanent twist (°) | | — | — |
| Maximum torque (N·m) | | | |
| Head rotation at fracture (°) and revolutions | | | |
| Fracture surface: flat or helical; texture | | | |

: Table 4. Test record.

| Quantity | Theory (equation) | Simulation | Measured ± U | Agree (Eq. 20)? |
|---|---|---|---|---|
| $G$, steel (GPa) | Eq. 7 | — | | |
| $G$, aluminum (GPa) | Eq. 7 | — | | |
| $\tau_Y$, steel (MPa) | $\sigma_Y/\sqrt{3}$ | | | |
| $T$ at 10°, steel (N·m) | Eq. 10 | | | |
| $T$ at 10°, aluminum (N·m) | Eq. 10 | | | |
| Permanent twist, steel (°) | Eq. 12 | | | |
| $R_T$, cast iron (MPa) | $\sigma_{UT}$ | | | |

: Table 5. Theory vs. simulation vs. measurement.

```{=latex}
\renewcommand{\arraystretch}{1.15}
```

## 7. Analysis

Every answer must (i) show at least two reasoning steps, (ii) include a dimensional check or a limiting-case check, and (iii) end with one to three sentences interpreting the result in words. Questions marked **[Core]** are required of everyone. **[Challenge]** questions are for students who want more. **[Extension]** questions are for honors and independent study.

**A1 [Core] — Modulus of rigidity.** For steel and aluminum, plot $T$ against the troptometer twist $\varphi$ (in radians) on the initial loading and fit a line for 0.3 N·m < $T$ < 4 N·m. Compute $G = kL/J$ from the slope $k$ and its uncertainty from Eq. 19. Predict $G$ from Eq. 7 with the values in Table 1, propagate that uncertainty too, and compare using Eq. 20. *Check:* the fitted intercept should be near zero; units of $kL/J$. *Interpret:* which uncertainty term dominates, and how would the answer change if you had measured $d$ with calipers?

**A2 [Core] — Yield and the elastic–perfectly plastic model.** For each metal, fit $\tau_Y$ by least squares to the initial loading data using Eq. 10 (steel: up to the start of unloading; aluminum: up to 10°), with your $G$ from A1 (one free parameter; a spreadsheet solver or a scan over $\tau_Y$ works). Report $\tau_Y \pm U$, $T_Y$ and $\varphi_Y$, the RMS and largest residuals, and compare $\tau_Y$ with $\sigma_Y/\sqrt{3}$ from Table 1. *Check:* the residuals for steel should be at the level of the torque noise. *Interpret:* why does the model fit one metal and not the other, and what does the misfit do to the fitted $\tau_Y$?

**A3 [Core] — Unloading, permanent set and residual stress.** For the steel, find the twist and torque at which you started unloading and the permanent twist when the torque returned to zero. Predict the permanent twist from Eq. 12 with your $G$, with its uncertainty, and compare. Fit the slope of the unloading branch and compare it with the loading slope of A1. Then compute and plot the residual stress distribution from Eq. 12 with your $\tau_Y$. *Check:* the residual torque $\int\rho\tau_{res}\,dA$ must vanish. *Interpret:* why did the shaft not spring back to zero, and where in the section is the residual stress largest?

**A4 [Core] — What the drive head measures.** On the initial elastic loading of each metal, fit $\Delta_{head} - (L_c/L)\varphi$ against $T$ for 1.5 N·m < $T$ < $T_Y$ to obtain $C_m$ and $\Delta_{toe}$ (Eq. 15). What fraction of the elastic head rotation is the machine? Then use Eq. 15 to convert the head rotation after the troptometer came off into twist over the gage, and report the surface shear strain at fracture $\gamma_f$ and the number of revolutions over the gage. *Check:* the corrected head twist must join the troptometer curve at 10° without a step. *Interpret:* why is the correction small for steel at fracture but essential for $G$?

**A5 [Core] — Strength and fracture.** For steel and aluminum, report $T_U$, the modulus of rupture $R_T$ (Eq. 13) with its uncertainty, and the fully plastic estimate $3T_U/(2\pi c^3)$. Explain which one is closer to the true shear stress at the surface and why the two bracket it. For cast iron, compare $R_T$ with $\sigma_{UT}$ using Eq. 20 and explain the 45° helical fracture with Eq. 14. *Check:* the ratio of the two estimates is exactly 4/3 whatever the data; explain why, and why only one of them is meaningful for the cast iron. *Interpret:* why do the ductile and brittle surfaces look so different, given that all three specimens carried the same stress state?

**A6 [Core] — Theory vs. simulation vs. measurement.** Complete Table 5. Make one figure with error bars at $\pm U$ for $G$ (both metals), $\tau_Y$ (steel), the torque at 10° (both metals), the permanent twist and the cast iron's $R_T$, each normalized by its theory value. Explain **every** discrepancy larger than the expanded uncertainty with a named cause, quantified where you can.

**M1 [Core] — Where does the model break?** (a) For aluminum, plot the residual of the Eq. 10 fit against twist, say where it is largest, and give its size as a fraction of $T_Y$. In the simulation, run "Aluminum is not elastic–perfectly plastic" and compare the two laws at 10°. (b) Run "Elastic formula beyond yield": by what percentage does $Tc/J$ overstate the actual surface stress at 120°, and how does that compare with your $R_T$ for steel? (c) Run "Circular formula on a square bar": how wrong is $\tau = Tc/J$, and where does it put the maximum stress? Explain in two sentences why plane sections stay plane for a circle but not for a square.

**C1 [Challenge] — Recover τ(γ) with Nadai's method.** Derive Eq. 18. Apply it to the steel data, with the twist from the corrected head rotation (Eq. 15) throughout, at $\gamma_c$ = 0.1, 0.5, 1.0 and 1.5, estimating $dT/d\gamma_c$ from a local fit of $\ln T$ against $\ln\gamma_c$. Compare with your Lab 1 tension results converted by $\tau = \sigma_t/\sqrt{3}$, $\gamma = \sqrt{3}\,\varepsilon_t$, and comment on how far the Lab 1 Hollomon fit can be extrapolated.

**C2 [Challenge] — Hollow shafts have little plastic reserve.** Derive $T_p/T_Y$ for a hollow shaft as a function of $c_i/c$, evaluate it at 0, 0.6 and 0.9, and confirm two of the values with the simulation's "Hollow shaft" preset. Explain the trend from the stress distribution.

**C3 [Challenge] — Check the rectangle coefficients.** In the simulation's rectangle mode with $a/b$ = 2, record the finite-difference $c_2$ at $N$ = 8, 16 and 32. Show that the error falls as $N^{-2}$, Richardson-extrapolate ($c_2 \approx (4c_{2,2N} - c_{2,N})/3$), and compare with the series value. Then use the membrane analogy to explain why the maximum stress in a square is at the middle of a side and zero at the corners.

**X1 [Extension] — Thin walls.** Derive Eq. 17 from equilibrium of a wall element (constant shear flow). For a circular tube, show that Bredt's stress is lower than the exact $Tc/J$ by about $t/(2r_m)$ to first order, and check it with the simulation's "Thin wall gets thick" experiment.

**X2 [Extension] — A composite shaft.** A 20 mm steel core is bonded inside a 6061-T6 sleeve with 30 mm outside diameter, and the pair is twisted as one (§3.3). Using your measured $G$ and $\tau_Y$ values, find how the torque divides between core and sleeve, which part yields first, and the torque at which it does.

**X3 [Extension] — Where does the work go?** Integrate $T$ against the twist of the reduced section up to fracture to find the plastic work done on the steel and the aluminum, and the temperature rise if none of it escaped (steel: $\rho$ = 7870 kg/m³, $c_p$ = 486 J/(kg·K); aluminum: 2700 kg/m³, 896 J/(kg·K)). Was the test isothermal? What would this mean for a test run ten times faster?

## 8. Design problem

**D1 — A transmission shaft.** A conveyor drive transmits 15 kW at 1200 rpm through a shaft 1.50 m long between its couplings. At one end it has a shoulder whose fillet raises the stress by $K$ = 1.6 (§3.5). Requirements:

* factor of safety of at least 2.0 against shear yield at the fillet, using a **conservative** shear yield strength from **your** measurement ($\tau_Y - U$);
* angle of twist over the 1.50 m length of no more than 1.0°, using **your** measured $G$;
* outer diameter a whole number of millimeters; a hollow shaft may have $d_i/d$ up to 0.8.

Choose a material (1018 steel or 6061-T6), a section (solid or hollow) and a diameter. Material data: density 7870 kg/m³ for steel and 2700 kg/m³ for aluminum; bar and tube stock cost about \$2.20/kg for steel and \$6.50/kg for aluminum. More than one design is acceptable. Justify yours with a quantitative trade-off (mass, cost, margin, or another criterion you define), and say which requirement governs. Submit at most one page: a requirements table, the governing calculation for each requirement, the chosen design with every requirement checked, and one assumption that could invalidate your design, with how you would check it.

| Criterion | Weight |
|---|---:|
| Torque from power and speed; requirements translated into equations, units correct | 20 % |
| Conservative strength and measured $G$ from **your** data, with the concentration factor at the right place | 25 % |
| Every requirement checked for the final design; governing requirement identified | 20 % |
| Choice justified by a quantitative comparison of at least two alternatives | 25 % |
| Clear one-page presentation; one critical assumption named and a check proposed | 10 % |

: Table 6. How D1 will be graded.

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

: Table 7. Report grading. Extension questions are graded separately for honors and independent-study credit.

::: pagebreak
:::

## Appendix A — Running the lab without equipment

If the machine is unavailable, use `sample_data.csv`. It holds one row per sample for the three specimens:

| Column | Meaning |
|---|---|
| `specimen` | `steel`, `al` or `ci` |
| `time_s` | time from the start of the test (s) |
| `torque_Nm` | torque (N·m), resolution 0.01 N·m |
| `troptometer_deg` | twist over the 50.80 mm gage (°), resolution 0.01°; blank after removal and for the cast iron |
| `head_deg` | drive-head rotation from the start (°), resolution 0.1° |

: Table A1. Columns of `sample_data.csv`. The last row of each specimen is the first sample after fracture.

The steel was loaded at 0.25°/s to about 5.9° on the troptometer, unloaded to zero torque, reloaded to 10.0°, and then twisted at 15°/s to fracture; the aluminum the same without the unloading; the cast iron at 0.25°/s to fracture. Use these measurements:

| Quantity | Readings |
|---|---|
| Steel $d$ (mm) | 6.351, 6.349, 6.350, 6.352, 6.348, 6.350 |
| Aluminum $d$ (mm) | 6.353, 6.351, 6.352, 6.354, 6.350, 6.352 |
| Cast iron $d$ (mm) | 6.349, 6.347, 6.348, 6.350, 6.346, 6.348 |
| Gage length $L$ / reduced length $L_c$ (mm) | 50.80 / 76.20 |
| Fracture surfaces | steel and aluminum flat, perpendicular to the axis, with circular smear marks; cast iron a 45° helix, granular grey |

: Table A2. Specimen measurements for the sample data.

## Appendix B — Uncertainty quick reference

* Limit $\pm a$ (calibration, accuracy): $u = a/\sqrt{3}$. Reading resolution $r$: $u = r/\sqrt{12}$ (already included when you use the scatter of repeated readings).
* Sum or difference: $u_{x \pm y}^2 = u_x^2 + u_y^2$. Product or quotient: $(u_{xy}/xy)^2 = (u_x/x)^2 + (u_y/y)^2$. Power: $u_{x^k}/x^k = |k|\,u_x/x$.
* Mean of $N$ readings: $u = s/\sqrt{N}$ for the scatter, combined with any calibration term.
* Least-squares line $y = a + mx$ through $N$ points: $s_m = s/\sqrt{\sum(x_i - \bar x)^2}$, with $s^2 = \sum(y_i - a - mx_i)^2/(N-2)$ (LINEST in a spreadsheet).
* *One-parameter fit (A2).* Scan $\tau_Y$, compute the sum of squared residuals $S(\tau_Y)$, and take the minimum. Its standard error is $\sqrt{2s^2/S''}$, with $s^2 = S_{min}/(N-1)$ and $S''$ the curvature of $S$ at the minimum (a finite difference). Then add the calibration terms: $\tau_Y \propto T/d^3$, so $(u/\tau_Y)^2$ gains $(3u_d/d)^2 + (u_T/T)^2$.
* *Example.* Six micrometer readings with $s_d$ = 0.0014 mm and accuracy ±0.003 mm: $u_d = \sqrt{0.0014^2/6 + 0.003^2/3}$ = 0.0018 mm, so $4u_d/d$ = 0.11 %.
* Report $x \pm U$ with $U = 2u$. Round $U$ to one or two significant figures, and $x$ to the same decimal place.

## Appendix C — Using the simulation

Open `lab03_simulation.html` in any browser; it needs no internet connection. Choose a configuration and a preset, then move the sliders. In **Circular shaft** mode the **law** toggle switches the numerical solution between the material's own stress–strain curve and the elastic–perfectly plastic model of §3.7; **Stress state shown** switches between the loaded state and the state after unloading. The **readout table** compares each closed-form result with the independent numerical solution: "agree" rows check the formulas, and "different models" rows show how far a formula is from a more realistic model. The **formula cards** state where each equation comes from and whether it applies at the current settings. **Push the model past its assumptions** runs prepared experiments. **Export (CSV)** saves the curves, the readout or the convergence study. If your browser blocks the download, the data appears in a box you can copy. The **SI / US customary** toggle converts every input and output.

## Appendix D — Derivations

**D.1 Elastic torsion (Eqs. 1–6).** Symmetry forbids a circular cross-section from warping or distorting: any out-of-plane bulge would look different when the shaft is turned end for end, which a circular shaft cannot tell apart. So each section rotates rigidly, and a section at distance $x$ turns by $\varphi(x)$. A fiber at radius $\rho$ between two sections $dx$ apart is sheared by $\gamma = \rho\,d\varphi/dx$, which is $\rho\varphi/L$ for a uniform shaft (Eq. 1). With $\tau = G\gamma$, $\tau = G\rho\varphi/L$. Substituting into Eq. 3, $T = (G\varphi/L)\int\rho^2\,dA = JG\varphi/L$, which gives Eq. 6, and eliminating $G\varphi/L$ gives Eq. 4. For a solid circle $\int\rho^2\,dA = \int_0^c \rho^2\,2\pi\rho\,d\rho = \pi c^4/2$; a hollow circle subtracts the hole (Eq. 5). Limits: $\varphi \propto L$ and $\varphi \propto 1/d^4$. Units: N·m × m / (m⁴ × N/m²) = rad.

**D.2 E, ν and G.** See Lab 2, Appendix D.2: pure shear $\tau$ is equivalent to principal stresses $\pm\tau$ at 45°, and Hooke's law along the diagonals gives Eq. 7.

**D.3 Elastoplastic torque (Eqs. 8–11).** Yield starts where $\gamma$ is largest, at $\rho = c$, when $G c\varphi/L = \tau_Y$: Eq. 8. For larger $\varphi$, the fibers with $\rho\varphi/L > \tau_Y/G$ are at $\tau_Y$; the boundary is at $\rho_Y = \tau_Y L/(G\varphi) = c\varphi_Y/\varphi$ (Eq. 9). Then $T = \int_0^{\rho_Y} \frac{\tau_Y\rho}{\rho_Y}\,2\pi\rho^2\,d\rho + \int_{\rho_Y}^{c}\tau_Y\,2\pi\rho^2\,d\rho = \frac{\pi}{2}\tau_Y\rho_Y^3 + \frac{2\pi}{3}\tau_Y(c^3 - \rho_Y^3) = \frac{2\pi}{3}\tau_Y c^3\left[1 - \frac{1}{4}\frac{\rho_Y^3}{c^3}\right]$. With $T_Y = \tau_Y\pi c^3/2$, this is Eq. 10. As $\rho_Y \to 0$, $T \to \frac{2\pi}{3}c^3\tau_Y = \frac{4}{3}T_Y$ (Eq. 11). For a hollow shaft the core starts at $c_i$: $T_p = \frac{2\pi}{3}\tau_Y(c^3 - c_i^3)$ and $T_Y = \tau_Y\pi(c^4 - c_i^4)/(2c)$, so $T_p/T_Y = \frac{4}{3}\frac{1 - k^3}{1 - k^4}$ with $k = c_i/c$, which falls toward 1 as $k \to 1$, because the stress in a thin tube is already nearly uniform at first yield.

**D.4 Unloading (Eq. 12).** Reducing the torque by $\Delta T$ changes every fiber's strain by $\Delta\gamma = \rho\Delta\varphi/L$ in the reverse direction. Fibers that are unloading obey $\Delta\tau = G\Delta\gamma$, so the change is the elastic solution: $\Delta\tau = \Delta T\rho/J$ and $\Delta\varphi = \Delta TL/(JG)$. Removing all of $T_{max}$ gives Eq. 12. The residual torque is $\int\rho\tau\,dA - (T_{max}/J)\int\rho^2\,dA = T_{max} - T_{max} = 0$. For an elastic–perfectly plastic solid shaft, $T_{max} \le \frac{4}{3}T_Y$, so the surface residual is at least $\tau_Y - \frac{4}{3}\tau_Y = -\frac{1}{3}\tau_Y$: unloading never causes reverse yielding.

**D.5 Stresses at 45° (Eq. 14).** Cut a small element with faces along and across the axis; it carries $\tau$ on all four faces. Cut it along a diagonal and write equilibrium of the triangle normal to the diagonal: the two shear forces $\tau\,dA\cos 45°$ add up to $\sigma\,dA$, so $\sigma = \tau$ on one diagonal, and by the same argument $\sigma = -\tau$ on the other, with no shear on either (Lab 8 generalizes this with Mohr's circle).

**D.6 Nadai's method (Eq. 18).** With $\rho = \gamma c/\gamma_c$ in Eq. 3, $T = 2\pi\int_0^c \tau\rho^2\,d\rho = \frac{2\pi c^3}{\gamma_c^3}\int_0^{\gamma_c}\tau(\gamma)\gamma^2\,d\gamma$. Multiply by $\gamma_c^3$ and differentiate with respect to $\gamma_c$: $\frac{d}{d\gamma_c}(T\gamma_c^3) = 2\pi c^3\tau(\gamma_c)\gamma_c^2$, so $\tau(\gamma_c) = \frac{1}{2\pi c^3}\left(3T + \gamma_c\frac{dT}{d\gamma_c}\right)$. In logarithmic form, $\gamma_c\,dT/d\gamma_c = T\,d\ln T/d\ln\gamma_c$, which is easier to estimate from noisy data.

**D.7 Head rotation (Eq. 15).** The torque is the same in every part of the load train (equilibrium of each piece). The reduced section is uniform, so its twist is $(L_c/L)\varphi$ whether it is elastic or plastic. The shoulders, hex ends, grips and drive train stay elastic and twist by an amount proportional to $T$: $C_mT$. Seating of the hex in its socket adds a backlash taken up at low torque. The twists add along the train (compatibility), which gives Eq. 15. In the elastic range the head slope is $L_c/(JG) + C_m$, so it does not give $G$ unless $C_m$ is known.

**D.8 Noncircular and thin-walled sections (Eqs. 16–17).** Prandtl showed that the shear stresses in a twisted prism derive from a stress function $\psi$ that satisfies $\nabla^2\psi = -2G\theta$ inside the section and $\psi = 0$ on its boundary. The stresses are the slopes of $\psi$, and $T = 2\int\psi\,dA$. The same equation describes a soap film stretched over a hole of the section's shape and inflated: the film is steepest where the boundary is closest to the center (the middle of the long sides) and flat at the corners. Solving it for a rectangle as a Fourier series gives $c_1$ and $c_2$ of Eq. 16; for $a/b \to \infty$ the film is a parabola across $b$, and both coefficients tend to 1/3. For a thin closed wall, equilibrium of a wall element cut by two longitudinal planes shows that the shear flow $q = \tau t$ is the same everywhere around the wall. Its moment about the axis is $\oint q\,r\,ds = q\cdot 2A_m = T$, which gives the first of Eqs. 17. Equating the work done per unit length, $T\theta/2$, to the strain energy per unit length, $\oint \frac{q^2}{2Gt}\,ds$, gives the second.

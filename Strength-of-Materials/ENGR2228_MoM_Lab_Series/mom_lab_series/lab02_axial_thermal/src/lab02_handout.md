# Lab 2 — Axial Deformation, Redundant Members and Thermal Stress

| | |
|---|---|
| **Course** | ENGR 2228 Mechanics of Materials |
| **When** | Week 5, after lectures on Beer 8e §2.1G–2.5 and §2.8 |
| **Textbook** | Beer, Johnston, DeWolf, Mazurek, *Mechanics of Materials*, 8th ed. (Beer 8e): §2.1G, §2.2, §2.3, §2.4, §2.5, §2.6, §2.8, §2.10; §10.1B for the Extension on buckling |
| **Session** | 2 hours in the lab, teams of two; report due one week later |
| **Equipment** | Universal testing machine (capacity ≥ 100 kN) with compression platens; four-channel strain indicator; dial gage (0.001 mm); calipers, bore gage and height gage; stirred water bath to 80 °C with thermocouple; three test articles (Parts A–C, Table 2) |
| **Files** | `lab02_simulation.html` (open in any browser, works offline), `sample_data.csv` |

## 1. Learning objectives

After this lab you will be able to:

1. Predict the elongation of prismatic, stepped and tapered members from Hooke's law, and measure the modulus of elasticity and Poisson's ratio with strain gages, each with a propagated uncertainty (§2.1G, §2.4, §2.8).
2. Detect and remove bending caused by an off-center load, and say how large the error would be with one gage (§2.10).
3. Solve a statically indeterminate assembly from equilibrium, compatibility and the force–deformation law, including a fit-up gap, and show from your own data when superposition fails (§2.2).
4. Predict and measure the thermal stress in a bolted joint made of two materials, and use the measurement to infer a coefficient of thermal expansion (§2.3).
5. Size an expansion gap that satisfies a strength limit and a geometric limit across a temperature range, with uncertainty (§2.3).

## 2. Theory

You will test three assemblies (Figure 1). Part A is a flat aluminum bar pulled in tension, with axial and transverse gages on both wide faces. Part B is a steel rod standing inside a slightly shorter aluminum tube, squeezed between two rigid caps. Part C is a steel bolt clamping an aluminum sleeve, heated in a water bath. Every result below comes from three ingredients: **equilibrium** (forces), **compatibility** (how the deformations fit together) and the **force–deformation law** of each member (Hooke's law plus thermal expansion).

![Figure 1. The three parts of Lab 2 (schematic, not to scale): (a) flat bar in tension with gage pairs on both faces; (b) steel rod in a shorter aluminum tube between rigid caps; (c) steel bolt and aluminum sleeve in a water bath.](figures/fig1_setups.png){width=6.4in}

::: {custom-style="Callout"}
**Sign convention (Beer 8e).** Tension is positive: internal axial forces $F$ and $N$, normal stresses $\sigma$ and normal strains $\varepsilon$ are positive when a member is stretched. An elongation $\delta$ is positive; a temperature rise $\Delta T$ is positive. The press load $P$ on the caps of Part B is entered as a positive **magnitude** that pushes the caps together, so it puts the members in compression ($F < 0$). In a bar between supports, $x$ points to the right; a load $P_B$ and a displacement $u$ are positive toward $+x$, and the wall reaction $R$ is positive when the right wall pushes the bar toward $-x$ (compressing it). A gap $g > 0$ is a clearance; $g < 0$ is an interference.
:::

::: {custom-style="Callout"}
**Nomenclature.** $P$ press or test load; $F_1$, $F_2$ member forces (member 1 = rod or bolt, member 2 = tube or sleeve); $E$ modulus of elasticity; $\nu$ Poisson's ratio; $G$ modulus of rigidity; $A$ cross-sectional area; $b$, $t$ width and thickness of the Part A bar; $L$ length; $\delta$ elongation; $k_i = E_iA_i/L_i$ axial stiffness and $f_i = L_i/(E_iA_i)$ flexibility of member $i$; $g$ fit-up gap; $P_{gap}$ load at which the gap closes; $s$ share of load carried by member 2 after contact; $\Delta$ approach of the caps measured by the dial gage; $C$ compliance of the caps and fixtures (mm/kN); $\varepsilon_x$ axial and $\varepsilon_y$ transverse strain; $\beta$ bending fraction (bending strain divided by axial strain); $e$ load offset; $\alpha$ coefficient of thermal expansion; $\Delta T$ temperature change; $F_b$ bolt force; $F_0$ bolt preload at the starting temperature; $\alpha_b$, $\alpha_s$ and $E_bA_b$, $E_sA_s$ bolt and sleeve properties; $P_B$ load applied at the junction B of a two-segment bar; $R$ wall reaction; $d_a$, $d_b$ end diameters of a tapered segment; $GF$ gage factor; $u$ standard uncertainty; $U = 2u$ expanded uncertainty.
:::

Full derivations of the results below are in **Appendix D**; this section states each result, what it means, and when it stops applying.

### 2.1 Deformation of a member under axial load

For a prismatic member of length $L$ carrying a force $P$, Hooke's law $\sigma = E\varepsilon$ with $\sigma = P/A$ and $\varepsilon = \delta/L$ gives (§2.1G)

$$\delta = \frac{PL}{EA} \qquad (1)$$

If the area or the force varies along the member, apply Eq. 1 to a slice $dx$ and add:

$$\delta = \int_0^L \frac{P(x)\,dx}{E\,A(x)} \qquad (2)$$

and for a member made of prismatic segments

$$\delta = \sum_i \frac{P_i L_i}{E_i A_i} \qquad (3)$$

*Worked example.* A 6061-T6 bar 20 mm × 5 mm × 300 mm carrying 10 kN: $\delta = (10\,000)(300)/[(68\,900)(100)] = 0.435$ mm (N, mm and MPa = N/mm² are a consistent set). A cone of the same material, 300 mm long, tapering from 30 mm to 15 mm diameter, has a flexibility $\delta/P = 4L/(\pi E d_a d_b)$ (Appendix D.1) that is 11 % larger than that of a cylinder with the mean diameter, 22.5 mm.

*When Eqs. 1–3 apply:* the material must be linear elastic; the stress must be uniform over each cross-section, which fails within about one width of a load application point, a support or a change of section (Saint-Venant, §2.10); and the taper must be gentle (half-angle below about 10°) for Eq. 2 to describe a three-dimensional body.

### 2.2 Poisson's ratio, the modulus of rigidity and stray bending

In uniaxial stress the bar shortens laterally in proportion to its axial strain (§2.4):

$$\varepsilon_y = -\nu\,\varepsilon_x \qquad (4)$$

For an isotropic material, $E$, $\nu$ and the modulus of rigidity are linked (§2.8; Appendix D.2):

$$G = \frac{E}{2(1+\nu)} \qquad (5)$$

**Bending from an off-center load.** If the load line in Part A is offset by $e$ through the thickness $t$, the bar also bends. A gage on one wide face reads more strain than the average and the gage on the other face reads less:

$$\varepsilon_{front} = \varepsilon_x(1+\beta), \qquad \varepsilon_{back} = \varepsilon_x(1-\beta), \qquad \beta = \frac{6e}{t} \qquad (6)$$

so an offset of only 0.05 mm on a 6.35 mm bar gives $\beta$ = 4.7 %. The **average** of the two readings is $\varepsilon_x$ exactly, which is why every gage in this lab comes in a pair on opposite faces. Derivation: Appendix D.3.

### 2.3 Two members between rigid caps (statically indeterminate)

![Figure 2. Two members between rigid caps. (a) Before loading, member 2 is shorter by a gap g. (b) Equilibrium of the cap. (c) Compatibility: after loading both members end at the same cap position.](figures/fig2_compatibility.png){width=6.4in}

In Part B the press pushes the top cap down with a force $P$. The cap is in equilibrium under $P$ and the two member forces (Figure 2b):

$$F_1 + F_2 = -P \qquad (7)$$

That is one equation for two unknowns: the assembly is **statically indeterminate** (§2.2). The second equation comes from geometry. Both members end at the same cap, so their deformed lengths match (Figure 2c):

$$L + \delta_1 = (L - g) + \delta_2 \qquad (8)$$

and each member obeys its own force–deformation law, with thermal expansion included (§2.3):

$$\delta_i = \frac{F_i L_i}{E_i A_i} + \alpha_i\,\Delta T\,L_i \qquad (9)$$

Solving Eqs. 7–9 at constant temperature (Appendix D.4): member 2 carries nothing until the cap has moved through the gap, which takes the load

$$P_{gap} = k_1\,g \qquad (10)$$

after which each additional newton of load is split in proportion to the stiffnesses:

$$F_2 = \begin{cases} 0, & P < P_{gap} \\ -s\,(P - P_{gap}), & P \ge P_{gap} \end{cases} \qquad (11)$$

$$s = \frac{k_2}{k_1 + k_2} = \frac{E_2A_2}{E_1A_1 + E_2A_2} \quad (L_1 \approx L_2) \qquad (12)$$

*Worked example.* A brass rod ($E$ = 97 GPa, $d$ = 16 mm) inside a steel tube ($E$ = 205 GPa, 30 mm × 24 mm), both 200 mm long with $g$ = 0.12 mm: $k_1$ = 97.5 kN/mm, $P_{gap}$ = 11.7 kN and $s$ = 0.728 (Figure 3). The stiff tube takes 73 % of each increment once it is engaged, but only from 11.7 kN on.

![Figure 3. Load sharing with a fit-up gap, for the illustrative brass rod in a steel tube. Left: member forces. Right: the approach of the caps that a dial gage would read.](figures/fig3_sharing.png){width=6.3in}

**Superposition fails while the gap is open.** Eq. 11 is linear in $P$ only on each side of $P_{gap}$. Doubling the load does not double $F_2$, because the set of members carrying load changes at $P_{gap}$. The textbook method of adding load cases (§2.2) is valid only for loads that leave the contact state unchanged.

**What the dial gage reads.** A dial gage between the caps measures the members' shortening plus the compliance $C$ of the caps and their seats, which carry the full load $P$ in series with the members:

$$\Delta = \begin{cases} P/k_1 + C\,P, & P < P_{gap} \\ g + (P - P_{gap})/(k_1 + k_2) + C\,P, & P \ge P_{gap} \end{cases} \qquad (13)$$

The knee in $\Delta$ locates $P_{gap}$, but the slopes alone cannot separate $k$ from $C$. The tube gages measure $F_2$ directly and are not affected by $C$.

### 2.4 Thermal stress

The total strain of a heated member is its elastic strain plus its free thermal strain (§2.3):

$$\varepsilon = \frac{\sigma}{E} + \alpha\,\Delta T \qquad (14)$$

A prismatic bar held between rigid walls cannot change length, so $\varepsilon = 0$ and

$$\sigma = -E\,\alpha\,\Delta T \qquad (15)$$

independent of its length and area: a steel bar heated 50 K is stressed to −120 MPa.

![Figure 4. Thermal stress in a bolted joint. (a) Heated freely, the aluminum sleeve would grow more than the steel bolt. (b) Clamped, both reach the same length: the bolt is stretched, the sleeve squeezed. (c) Compatibility.](figures/fig4_thermal.png){width=6.3in}

**Bolt and sleeve (Part C).** The bolt (member 1) and the sleeve (member 2) have the same length $L$ and are clamped together by the head and the nut with a preload $F_0$ at the starting temperature. The bolt force is $F_b$ and the sleeve force is $-F_b$ (equilibrium of the nut). Compatibility requires their elongations to match (Figure 4c), which gives (Appendix D.5)

$$F_b = F_0 + \Delta T\,\frac{(\alpha_s - \alpha_b)\,L}{L/(E_bA_b) + L/(E_sA_s)} \qquad (16)$$

*Worked example.* A steel bolt of 8 mm diameter clamping an aluminum sleeve 16 mm × 8.5 mm, both 80 mm long, heated 40 K: $L/(E_bA_b) + L/(E_sA_s)$ = 1.581 × 10⁻⁵ mm/N, so the bolt force rises by 2.41 kN. *Check:* if $\alpha_s = \alpha_b$ nothing happens; if the sleeve were rigid, the bolt alone would absorb the mismatch, $\Delta F_b = E_bA_b(\alpha_s - \alpha_b)\Delta T$.

The bolt gage in Part C is **self-temperature-compensated for steel**: it reads the bolt's mechanical strain $F_b/(E_bA_b)$, not its total strain, apart from a small residual thermal output (Table 2).

*When Eqs. 14–16 apply:* both members stay elastic; the joint stays closed ($F_b > 0$; a bolt with a *larger* $\alpha$ than its sleeve loses preload when heated); $E$ and $\alpha$ are constant over the temperature range (6061-T6 loses about 2 % of its modulus between 20 and 80 °C); and each member has a uniform temperature.

### 2.5 Superposition with a redundant reaction

![Figure 5. A bar fixed at both ends solved by superposition: remove the right wall, let the load and the temperature change act, then push the end back with the unknown reaction R.](figures/fig5_superposition.png){width=6.3in}

The simulation also solves a two-segment bar between walls (Figure 5). Remove the right wall (the **redundant** support): the free end moves by $\delta_{free} = P_B f_1 + \Delta T(\alpha_1L_1 + \alpha_2L_2)$. Then apply the unknown reaction $R$, which moves the end back by $R(f_1 + f_2)$. Compatibility at the wall (zero displacement, or a gap $g$ that has closed) gives

$$R = \frac{\delta_{free} - g}{f_1 + f_2}, \qquad R \ge 0 \qquad (17)$$

where each flexibility is $f = \int dx/(EA)$. For a cone with end diameters $d_a$ and $d_b$,

$$f = \frac{4L}{\pi E\,d_a\,d_b} \qquad (18)$$

*When Eqs. 17–18 apply:* while the gap stays closed (if $R$ comes out negative, the bar has left the wall and $R = 0$), while all segments are elastic, and while the compressed bar stays straight. A slender bar heated between walls buckles sideways when its thermal force reaches the Euler load (§10.1B; Lab 9), long before the stress of Eq. 15 reaches yield.

### 2.6 The model in the simulation

`lab02_simulation.html` has two configurations. **Rod & tube / bolt & sleeve** evaluates Eqs. 10–12 and 16 in closed form and compares them with an **independent numerical solution** that marches the load and temperature from zero in $M$ increments, solves the cap's equilibrium with whichever members are in contact, and locates each contact event (gap closing or opening) by bisection. It does not use Eqs. 10–12. **Bar between supports** evaluates Eqs. 17–18 and compares them with a one-dimensional **finite-element** solution with $N$ elements per segment, each with the area at its midpoint. For prismatic segments the finite elements are exact for any $N$; for a taper their error falls as $N^{-2}$, which the convergence study shows.

### 2.7 Uncertainty and the measured quantities

The gages give strain; you convert strain to force with Hooke's law. The tube force in Part B and the bolt force in Part C are

$$F_2 = E_2A_2\,\bar{\varepsilon}_2, \qquad F_b = E_bA_b\,\varepsilon_b \qquad (19)$$

where $\bar{\varepsilon}_2$ is the average of the two tube gages. Use $E_2$ from your Part A measurement (the tube is 6061-T6 too) and $E_b$ from Table 1. Use standard uncertainties $u$; convert a limit $\pm a$ to $u = a/\sqrt{3}$; propagate to first order (Appendix B). For the modulus from Part A:

$$\left(\frac{u_E}{E}\right)^2 = \left(\frac{s_E}{E}\right)^2 + \left(\frac{u_A}{A}\right)^2 + \left(\frac{u_P}{P}\right)^2 + \left(\frac{u_{GF}}{GF}\right)^2 \qquad (20)$$

where $s_E$ is the standard error of the fitted slope, $u_A/A$ combines the width and thickness ($\sqrt{(u_b/b)^2 + (u_t/t)^2}$), and $u_{GF}/GF$ is the gage-factor tolerance (±1 % → 0.58 %). Report $x \pm U$ with $U = 2u$ and draw error bars at $\pm U$. A measurement and a reference **agree** when

$$|x_{meas} - x_{ref}| \le 2\sqrt{u_{meas}^2 + u_{ref}^2} \qquad (21)$$

Any larger discrepancy needs a physical or procedural explanation, quantified where possible.

## 3. Pre-lab (due at the start of the session)

Answer on paper or in a short document. Show every step, units included. Use Table 1 and the nominal dimensions in Table 2.

**P1 — Estimate before you measure.** (a) Part A at its maximum load of 18 kN: estimate the stress, the axial and transverse strains in microstrain (µε), and the fraction of the yield strength used. With a 1 µε indicator resolution, what is the relative resolution of the axial strain at 2 kN and at 18 kN? (b) Part B at 30 kN: estimate $P_{gap}$ for $g$ = 0.040 mm, the tube force and the rod stress (one significant figure is enough; use $s \approx 0.4$). (c) Part C between 20 and 80 °C: estimate the free length mismatch $(\alpha_s - \alpha_b)\Delta T\,L$, and the bolt's change in strain in µε. Check that each answer has the right units.

**P2 — Gap and superposition.** (a) Starting from Eqs. 7–9 with $\Delta T = 0$, derive Eqs. 10–12. (b) For the Part B assembly (rod $d$ = 12.70 mm; tube 25.40 mm × 19.05 mm; $L$ = 150 mm; $g$ = 0.040 mm), compute $P_{gap}$, $s$ and $F_2$ at 10, 20 and 30 kN. Show that $F_2(20\ \text{kN}) \ne 2F_2(10\ \text{kN})$ and explain why in one sentence. (c) Check the limiting cases $g \to 0$, $k_2 \to 0$ and $k_2 \to \infty$.

**P3 — Thermal clamp.** (a) Compute the change in bolt force per kelvin, $dF_b/dT$, for Part C from Eq. 16 (bolt $d$ = 10.00 mm; sleeve 20.00 mm × 10.50 mm; $L$ = 100 mm), and the bolt and sleeve stresses at 80 °C with $F_0$ = 2.0 kN. (b) If the materials were swapped (aluminum bolt, steel sleeve), at what temperature rise would the 2.0 kN preload be lost?

**P4 — Alignment.** (a) Use Eq. 6 to find the offset $e$ that gives $\beta$ = 5 % on the 6.35 mm bar. (b) If you used only the front gage with that offset, by what percentage would your $E$ be wrong, and in which direction? (c) Show that the average of the front and back readings removes the bending exactly, not just to first order.

**P5 — Predict with the simulation.** Open `lab02_simulation.html`. With the preset "Part B: steel rod in aluminum tube (gap)", record $P_{gap}$, the share $s$ and $F_2$ at 30 kN from the readout. With the preset "Part C: steel bolt clamping aluminum sleeve (heated)", record $dF_b/dT$ and $F_b$ at $\Delta T$ = 60 K. Run the experiment "Superposition fails with a gap" and describe in one sentence what the plot shows. Do the simulation's numbers match yours from P2–P3?

**P6 — Safety and load limits.** (a) At what press load would the Part B rod reach its yield strength (Table 1)? By what factor does the 30 kN test limit stay below it? (b) What are the two hazards in Part C, and how does the procedure control each?

| Material | $E$ (GPa) | $\nu$ | $\alpha$ (10⁻⁶/K) | $\sigma_Y$ typical (MPa) |
|---|---:|---:|---:|---:|
| 1018 steel, cold drawn (rod, bolt) | 205 ± 3 | 0.29 | 11.7 ± 0.3 | 370 |
| 6061-T6 aluminum (bar, tube, sleeve) | 68.9 ± 1.0 | 0.33 ± 0.01 | 23.6 ± 0.3 | 276 |

: Table 1. Reference values. The ± values are standard uncertainties for alloy-to-alloy and lot-to-lot spread. $G$ for 6061-T6 is about 26 GPa.

## 4. Equipment and safety

| Item | Specification used in this handout |
|---|---|
| Universal testing machine | Capacity ≥ 100 kN; load cell accuracy ±0.5 % of reading; flat compression platens, upper one on a spherical seat |
| Strain gages and indicator | 350 Ω foil gages, gage factor 2.10 ± 1 %; quarter bridge; indicator resolution 1 µε. Bolt gage self-temperature-compensated for steel, residual thermal output within ±0.5 µε/K, sealed for immersion |
| Dial gage | Resolution 0.001 mm, mounted on the lower cap with its plunger on the upper cap |
| Calipers / bore gage / height gage | Accuracy ±0.02 mm / ±0.01 mm / ±0.01 mm |
| Water bath | Stirred, 20–80 °C, thermocouple accuracy ±1.0 °C |
| Part A | 6061-T6 flat bar 25.40 mm × 6.35 mm × 300 mm; axial and transverse gages at mid-length on both wide faces |
| Part B | 1018 rod, $d$ = 12.70 mm, $L$ = 150.00 mm, inside a 6061-T6 tube 25.40 mm × 19.05 mm that is about 0.04 mm shorter; hardened steel caps; two axial gages on opposite sides of the tube at mid-length |
| Part C | M10 1018 bolt with a plain 10.00 mm shank and a gage at mid-length (leads out through a 2 mm notch in the sleeve end); 6061-T6 sleeve 20.00 mm × 10.50 mm; clamped length $L$ = 100.0 mm; preload 2.0 kN |

: Table 2. Equipment. If your equipment differs, record its values and use them throughout.

::: {custom-style="Safety"}
**Safety.** Wear safety glasses throughout. **Load limits:** Part A at most 18 kN (overload stop 22 kN; the bar would yield near 44 kN). Part B at most 30 kN (overload stop 35 kN; the rod would yield near 70 kN, P6). **Compression of a short assembly (Part B):** centre the caps on the platens, use the spherical seat, close the shield, and keep hands out while the crosshead moves; an off-center stack can kick out sideways. **Pinch points:** wedge grips (Part A) and the platens (Part B); position with the jog control at low speed. **Hot water (Part C):** water at 80 °C scalds in seconds. Lower and lift the assembly with the wire hook, never by hand; wear heat-resistant gloves; keep the bath on a stable bench away from the machine; do not exceed 80 °C. **Electrical:** the bath heater must be on a GFCI outlet; keep the strain-indicator leads and the indicator itself away from the water. Know where the emergency stop is before you start.
:::

## 5. Procedure

Start Part C first: the bath takes 30–45 minutes to heat from 20 to 80 °C, plus a few minutes of settling at each step. One partner records Part C while the other runs Parts A and B on the machine.

**Part C — Bolt and sleeve (start of the session, then at each temperature step).**

1. Measure the bolt shank diameter and the sleeve's outer and inner diameters three times each (Table 3).
2. Connect the bolt gage, balance it with the joint loose (nut finger-tight), then tighten the nut until the gage reads $F_0/(E_bA_b)$ = **124 µε** (2.0 kN). **Check:** the reading should stay within ±2 µε for one minute; a drifting reading means the nut or a washer is still seating.
3. Lower the assembly into the bath at about 20 °C with the hook. Wait until the thermocouple is steady to ±0.2 °C for two minutes, then record the temperature and the bolt strain (Table 6).
4. Heat in steps of about 5 °C up to 80 °C. At each step, wait for a steady temperature before recording. **Check:** the strain should rise by roughly 6 µε per kelvin (your P1c estimate); a jump or a fall means a lead is wet or the joint has slipped.
5. Switch the heater off and record on cooling at about 70, 60, 50, 40, 30 and 20 °C (add cold water to speed it up). Lift the assembly out with the hook only when the bath is below 40 °C.

**Part A — Flat bar in tension.**

6. Measure the width $b$ and thickness $t$ at the gage location, three times each (Table 3).
7. Grip the bar, connect the four gages, and balance all channels at zero load.
8. Load in steps of 2 kN to 18 kN, then unload in steps of 2 kN to zero, recording the load and all four strains at each step (Table 4). **Check at 6 kN:** the average axial strain should be within 10 % of $P/(Ebt)$ (your P1 estimate); the front and back axial readings should differ by less than 15 %. A larger difference means the bar is badly seated in the grips: unload, re-grip, repeat.

**Part B — Rod in tube.**

9. Measure the rod diameter, the tube's outer and inner diameters, and the lengths of the rod and the tube with the height gage (Table 3). Compute the gap $g = L_{rod} - L_{tube}$.
10. Stand the tube and the rod on the lower cap, centre the stack on the lower platen, place the upper cap, and mount the dial gage. Connect the two tube gages and balance them.
11. Bring the platen down until the load reads about 0.05 kN; zero the dial gage.
12. Load in steps of 2 kN to 30 kN, then unload in steps of 4 kN, recording the load, both tube strains and the dial reading at each step (Table 5). **Check:** the tube strain should stay near zero until about 7 kN (your P2 estimate of $P_{gap}$), then grow steadily; the dial reading should show a knee at the same load.
13. **Before you leave:** open the simulation, choose each Part B and Part C preset, enter your measured dimensions and gap, and record its predictions in Table 7 next to your raw readings at 30 kN and at 80 °C.

## 6. Data tables

```{=latex}
\renewcommand{\arraystretch}{1.9}
```

| Dimension (mm) | Reading 1 | Reading 2 | Reading 3 | Mean |
|---|---|---|---|---|
| Part A width $b$ | | | | |
| Part A thickness $t$ | | | | |
| Part B rod diameter | | | | |
| Part B tube outer diameter | | | | |
| Part B tube inner diameter (bore gage) | | | | |
| Part B rod length / tube length (height gage) | | | | |
| Part C bolt shank diameter | | | | |
| Part C sleeve outer diameter | | | | |
| Part C sleeve inner diameter | | | | |

: Table 3. Dimensions.

```{=latex}
\renewcommand{\arraystretch}{1.45}
```

| Load (kN) | Axial front (µε) | Axial back (µε) | Transverse front (µε) | Transverse back (µε) |
|---|---|---|---|---|
| 0 | | | | |
| 2 | | | | |
| 4 | | | | |
| 6 | | | | |
| 8 | | | | |
| 10 | | | | |
| 12 | | | | |
| 14 | | | | |
| 16 | | | | |
| 18 | | | | |
| 16 (unloading) | | | | |
| 12 | | | | |
| 8 | | | | |
| 4 | | | | |
| 0 | | | | |

: Table 4. Part A record. Record every 2 kN on unloading if time allows.

| Load (kN) | Tube front (µε) | Tube back (µε) | Dial (mm) | Load (kN) | Tube front (µε) | Tube back (µε) | Dial (mm) |
|---|---|---|---|---|---|---|---|
| 0 | | | | 18 | | | |
| 2 | | | | 20 | | | |
| 4 | | | | 22 | | | |
| 6 | | | | 24 | | | |
| 8 | | | | 26 | | | |
| 10 | | | | 28 | | | |
| 12 | | | | 30 | | | |
| 14 | | | | 20 (unloading) | | | |
| 16 | | | | 8 (unloading) | | | |

: Table 5. Part B record. Unload in 4 kN steps; record at least 20 and 8 kN on the way down.

| Temperature (°C) | Bolt (µε) | Temperature (°C) | Bolt (µε) | Temperature (°C) | Bolt (µε) |
|---|---|---|---|---|---|
| | | | | | |
| | | | | | |
| | | | | | |
| | | | | | |
| | | | | | |
| | | | | | |
| | | | | | |

: Table 6. Part C record (heating, then cooling; mark the cooling readings).

```{=latex}
\renewcommand{\arraystretch}{1.9}
```

| Quantity | Theory (equation) | Simulation | Measured ± U | Agree (Eq. 21)? |
|---|---|---|---|---|
| $E$ of 6061-T6 (GPa) | Table 1 | — | | |
| $\nu$ | Table 1 | — | | |
| $P_{gap}$ (kN) | Eq. 10 with measured $g$ | | | |
| Share $s$ after contact | Eq. 12 | | | |
| $F_2$ at 30 kN (kN) | Eq. 11 | | | |
| $dF_b/dT$ (N/K) | Eq. 16 | | | |
| $F_b$ at 80 °C (kN) | Eq. 16 | | | |

: Table 7. Theory vs. simulation vs. measurement.

```{=latex}
\renewcommand{\arraystretch}{1.15}
```

## 7. Analysis

Every answer must (i) show at least two reasoning steps, (ii) include a dimensional check or a limiting-case check, and (iii) end with one to three sentences interpreting the result in words. Questions marked **[Core]** are required of everyone. **[Challenge]** questions are for students who want more. **[Extension]** questions are for honors and independent study.

**A1 [Core] — Modulus and Poisson's ratio.** Compute $\sigma = P/(bt)$ and the average axial strain $\varepsilon_x = (\varepsilon_{front} + \varepsilon_{back})/2$ at each step. Plot $\sigma$ against $\varepsilon_x$ for loading and unloading and fit $E$ by least squares (Appendix B). Plot the average transverse strain against $\varepsilon_x$ and take $\nu$ as minus the slope (Eq. 4). Combine the slope's standard error with the area, load-cell and gage-factor terms (Eq. 20) to get $u_E$; for $\nu$, add an allowance of ±0.005 for the gages' transverse sensitivity. Report $E \pm U$ and $\nu \pm U$ and compare with Table 1 using Eq. 21. Compute $G$ from Eq. 5 with its uncertainty. *Check:* both fitted intercepts should be near zero; the largest difference between the loading and unloading strains at equal load should be a few µε. *Interpret:* why fit a slope instead of dividing single readings, and which term dominates $u_E$?

**A2 [Core] — Bending in an "axial" test.** For loads above 4 kN, compute $\beta$ (Eq. 6) at each step and its mean, and infer the load offset $e$. Fit $E$ from the front gage alone and from the back gage alone. *Check:* $\beta$ should be the same at every load if the offset is geometric; show that $E$ from the average strain is the harmonic mean of the two single-gage values, $2/(1/E_{front} + 1/E_{back})$, not their arithmetic mean. *Interpret:* how large an error would a one-gage test have made, compared with your $U$?

**A3 [Core] — Find the gap from the knee.** Compute the tube force $F_2$ (Eq. 19) at each step, using your $E$ from A1 and the measured tube area, and plot it against $P$ for loading and unloading. Fit the two-parameter model of Eq. 11 ($P_{gap}$ and $s$) to the loading branch by least squares (Appendix D.7). Infer $g = P_{gap}/k_1$ (Eq. 10) with its uncertainty, and compare it with the gap from the height gage (Table 3) using Eq. 21. Compare $s$ with Eq. 12. *Check:* units of $k_1$; if $g = 0$ the fitted line must pass through the origin. *Interpret:* which measurement of $g$ is more precise, by what factor, and why?

**A4 [Core] — Load path, stresses and the no-gap formula.** Use equilibrium (Eq. 7) to find the rod force at every step, and give the rod and tube stresses at 30 kN. Compare the measured $F_2$ at 30 kN with Eq. 11 using your $P_{gap}$, and with the textbook no-gap result $F_2 = -sP$; state the percentage by which the no-gap formula is wrong. Plot the apparent share $F_2/(-P)$ against $P$. *Check:* the unloading points must fall on the loading line (no slip, no yielding); both stresses must be below yield. *Interpret:* why does $F_2/(-P)$ never reach $s$ during the test? What fit-up tolerance on $g$ would keep the no-gap formula within 5 % at 30 kN?

**A5 [Core] — What the dial gage measures.** Fit straight lines to the dial reading against $P$ below the knee (2 to 6 kN) and well above it (above $P_{gap}$ + 2.5 kN). From Eq. 13, compare the two slopes with $1/k_1$ and $1/(k_1 + k_2)$, and deduce the cap compliance $C$ from each one, with standard errors. *Check:* units (mm/kN); the two estimates of $C$ should agree within their uncertainty. If they do not, find the cause in the low-load data (compare with Lab 1's toe region). *Interpret:* why are the gages, not the dial, the right instrument for the load share?

**A6 [Core] — Thermal stress in the joint.** Convert the bolt strain to force (Eq. 19) and plot $F_b$ against temperature, marking heating and cooling. Fit a line to obtain $dF_b/dT$ and the preload at 20 °C. Compare $dF_b/dT$ with Eq. 16, using the reference $\alpha$ and $E$ values with their uncertainties and your $E$ for the sleeve, and propagate the uncertainty of the prediction (Appendix B). Give the bolt and sleeve stresses at 80 °C. *Check:* heating and cooling slopes should agree (no slip, elastic); the joint must never have separated. *Interpret:* estimate the size and sign of two effects that make the measured slope differ from Eq. 16: the gage's residual thermal output (Table 2) and the 2 % drop in the sleeve's modulus over the range. Which one can explain your discrepancy?

**A7 [Core] — Theory vs. simulation vs. measurement.** Complete Table 7. Make one figure with error bars at $\pm U$ for $E$, $\nu$, $P_{gap}$, $s$ and $dF_b/dT$, each normalized by its theory value. Explain **every** discrepancy larger than the expanded uncertainty with a named cause, quantified where you can.

**M1 [Core] — Where does the model break?** (a) From your Part B data, compare $F_2$ at 20 kN with twice $F_2$ at 10 kN, and explain which assumption of the superposition method failed. (b) In the simulation, run "Gap never closes". Derive the largest gap for which the tube engages before the rod yields, and confirm it with the simulation: set $g$ to your value and $P$ just above $P_{gap}$, and watch for the yield warning. (c) Run "Heat the joint until it separates". Use Eq. 16 to find the temperature rise at which the joint loses its preload, compare with the simulation, and explain why Eq. 16 gives the wrong force beyond that point.

**C1 [Challenge] — Convergence of the bar model.** Run "Refine a taper" and export the convergence study. Plot the relative error in $R$ against $N$ on log–log axes and report the slope. Show, from the midpoint rule applied to $\int dx/A(x)$, why the error falls as $N^{-2}$, and why the finite elements are exact for any $N$ on a prismatic segment.

**C2 [Challenge] — Measure α of aluminum.** Turn Eq. 16 around: use your measured $dF_b/dT$ and the reference $\alpha_b$ to infer $\alpha_s$ for 6061-T6, with uncertainty. Compare with Table 1 using Eq. 21, and name the dominant uncertainty term.

**C3 [Challenge] — Generalized Hooke's law and volume change.** For Part A at 18 kN, compute the changes in width and thickness and the change in volume per unit volume (dilatation, §2.5–2.6). Could you have measured the width change with the calipers? Compute the bulk modulus $E/[3(1-2\nu)]$ and explain what $\nu = 0.5$ would mean.

**X1 [Extension] — Thermal buckling of a restrained bar.** For a straight round bar of diameter $d$ and length $L$, fixed at both ends, the Euler load is $P_{cr} = 4\pi^2EI/L^2$ (§10.1B). Derive the temperature rise at which the thermal force of Eq. 15 reaches $P_{cr}$, and find the slenderness $L/d$ above which a restrained 1018 steel bar buckles before it yields. Check your formula against the simulation's "Heat a restrained bar until it buckles" experiment.

**X2 [Extension] — Is the temperature dependence of E visible?** Model the sleeve modulus as $E_s(T) = E_s(20\,°\text{C})[1 - 3 \times 10^{-4}(T - 20)]$. Predict the curvature this produces in $F_b(T)$ over your range, then fit a quadratic to your Part C data and compare its quadratic coefficient with its standard error. Is the effect detectable? What change to the experiment would make it so?

**X3 [Extension] — More than two members.** Add a third member to Part B: a C360 brass tube ($E$ = 97 GPa) 32.0 mm × 27.0 mm outside the aluminum tube, 0.080 mm shorter than the rod. Write a short program (any language) that finds every contact event and the three member forces as $P$ rises to 30 kN, using only equilibrium and compatibility. Report the two closing loads and the forces at 30 kN, and plot the three forces against $P$.

## 8. Design problem

**D1 — Expansion gap for a handrail.** A handrail along an outdoor ramp is made of 6061-T6 tube segments 3.00 m long, joined end to end by internal sleeves that let the segments slide but transmit compression once the ends touch. Each segment is anchored at its middle. The rail is installed at a temperature between 10 °C and 20 °C (the day is not known in advance), and in service its temperature ranges from −25 °C (winter night) to +55 °C (summer sun). Requirements:

* when hot, the gap may close, but the compressive stress in the rail must not exceed **40 MPa** (a limit set by buckling between the posts); treat the rail as fully restrained once the ends touch;
* when cold, the gap must not exceed **8.0 mm**, so that a cane tip or a finger cannot be caught.

Use $E$ from **your** Part A measurement and $\alpha$ from Table 1. Specify the installation gap (a nominal value and a tolerance, or a rule that depends on the installation temperature) and show that every requirement holds at the worst combination of installation and service temperatures. More than one design is acceptable. Justify yours with a quantitative trade-off (tolerance a crew can hold, margin on each requirement, or another criterion you define). Submit at most one page: a requirements table, the governing calculation for each requirement, the chosen specification with every requirement checked, and one assumption that could invalidate your design, with how you would check it.

| Criterion | Weight |
|---|---:|
| Requirements identified and translated into equations, units correct | 20 % |
| Worst-case temperature combinations identified for each requirement | 25 % |
| Correct use of your measured $E$ and of the uncertainty in $\alpha$ | 15 % |
| Specification checked against every requirement; choice justified by a quantitative comparison of at least two options | 30 % |
| Clear one-page presentation; one critical assumption named and a check proposed | 10 % |

: Table 8. How D1 will be graded.

## 9. Report

Write a technical report of at most eight pages plus appendices, one per team. Include the pre-lab, Tables 3–7, all plots with labeled axes and units, every Core answer, M1 and D1. Challenge and Extension answers go in a clearly marked section. State every number as value ± $U$ with units, rounded per the style rules (uncertainty to one or two significant figures, value to the same decimal place). Put your analysis code or spreadsheet in an appendix.

| Part | Points |
|---|---:|
| Pre-lab P1–P6 | 15 |
| Data quality and procedure (Tables 3–6, checks performed) | 10 |
| Core analysis A1–A7 | 45 |
| M1 — Where does the model break? | 10 |
| D1 — Design problem | 15 |
| Communication: figures, units, uncertainty format | 5 |
| **Total** | **100** |
| Challenge (C1–C3) | up to +10 |

: Table 9. Report grading. Extension questions are graded separately for honors and independent-study credit.

::: pagebreak
:::

## Appendix A — Running the lab without equipment

If the equipment is unavailable, use `sample_data.csv`. It holds one row per recorded step for all three parts:

| Column | Meaning |
|---|---|
| `part` | `A` (flat bar), `B` (rod in tube) or `C` (bolt and sleeve) |
| `step` | reading number within the part, in the order taken |
| `temperature_C` | bath temperature (°C) in Part C; room temperature in Parts A and B |
| `load_N` | machine load (N); blank in Part C |
| `strain_axial_front_ue`, `strain_axial_back_ue` | Part A axial gages, front and back faces (µε) |
| `strain_transverse_front_ue`, `strain_transverse_back_ue` | Part A transverse gages (µε) |
| `strain_tube_front_ue`, `strain_tube_back_ue` | Part B tube gages on opposite sides (µε) |
| `dial_mm` | Part B dial gage, approach of the caps (mm) |
| `strain_bolt_ue` | Part C bolt gage, mechanical strain (µε) |

: Table A1. Columns of `sample_data.csv`. Strains are zeroed at the start of each part, except the bolt gage, which was zeroed with the nut finger-tight.

Use these measurements with the sample data:

| Quantity | Readings |
|---|---|
| Part A width $b$ (mm) | 25.41, 25.39, 25.40 |
| Part A thickness $t$ (mm) | 6.36, 6.34, 6.35 |
| Part B rod diameter (mm) | 12.70, 12.71, 12.70 |
| Part B tube outer diameter (mm) | 25.41, 25.40, 25.40 |
| Part B tube inner diameter (mm) | 19.04, 19.06, 19.05 |
| Part B rod length / tube length (mm) | 150.00 / 149.96 |
| Part C bolt shank diameter (mm) | 10.00, 10.01, 10.00 |
| Part C sleeve outer diameter (mm) | 20.00, 20.01, 20.00 |
| Part C sleeve inner diameter (mm) | 10.50, 10.51, 10.50 |

: Table A2. Specimen measurements for the sample data. Part C clamped length 100.0 mm; preload set to 2.0 kN.

## Appendix B — Uncertainty quick reference

* Limit $\pm a$ (calibration, accuracy): $u = a/\sqrt{3}$. Reading resolution $r$: $u = r/\sqrt{12}$ (already included when you use the scatter of repeated readings).
* Sum or difference: $u_{x \pm y}^2 = u_x^2 + u_y^2$. Product or quotient: $(u_{xy}/xy)^2 = (u_x/x)^2 + (u_y/y)^2$. Power: $u_{x^k}/x^k = |k|\,u_x/x$.
* Mean of $N$ readings: $u = s/\sqrt{N}$ for the scatter, combined with any calibration term.
* Least-squares line $y = a + mx$ through $N$ points: $m = \sum(x_i - \bar x)(y_i - \bar y)/\sum(x_i - \bar x)^2$, with standard error $s_m = s/\sqrt{\sum(x_i - \bar x)^2}$, where $s^2 = \sum(y_i - a - mx_i)^2/(N-2)$. Spreadsheet functions (LINEST, or SLOPE with STEYX) report both.
* *Example (tube area).* $A_2 = \pi(D_o^2 - D_i^2)/4$, so $u_{A_2}^2 = (\pi D_o u_{D_o}/2)^2 + (\pi D_i u_{D_i}/2)^2$. With $u_{D_o}$ = 0.012 mm and $u_{D_i}$ = 0.008 mm: $u_{A_2}$ = 0.54 mm², 0.24 % of the area.
* *Example (Eq. 16).* The prediction depends on $\alpha_s - \alpha_b$. With $u$ = 0.3 × 10⁻⁶/K on each, $u(\alpha_s - \alpha_b) = 0.42 \times 10^{-6}$/K, which is 3.6 % of the difference: the dominant term.
* Report $x \pm U$ with $U = 2u$. Round $U$ to one or two significant figures, and $x$ to the same decimal place.

## Appendix C — Using the simulation

Open `lab02_simulation.html` in any browser; it needs no internet connection. Choose a configuration and a preset, then move the sliders. **Ends of member 2** switches between *contact only* (a press squeezing two loose members; member 2 can only push) and *bonded* (a bolted joint with a preload). The **readout table** compares each closed-form (textbook) result with the independent numerical solution and says why they differ. The **formula cards** state where each equation comes from and whether it applies at the current settings. **Push the model past its assumptions** runs prepared experiments. **Compare with sample data** overlays the Part B tube force or the Part C bolt force from `sample_data.csv`. **Export (CSV)** saves the curves, the readout or the convergence study. If your browser blocks the download, the data appears in a box you can copy. The **SI / US customary** toggle converts every input and output.

## Appendix D — Derivations

**D.1 Elongation of a member (Eqs. 1–3, 18).** A slice $dx$ carries the internal force $P(x)$ (equilibrium of the part on one side of the cut). If the stress is uniform on the slice, $\sigma = P/A$, and Hooke's law gives the slice's strain $d\delta/dx = P/(EA)$. Integrating gives Eq. 2; with $P$, $E$, $A$ constant it gives Eq. 1, and with piecewise-constant values it gives Eq. 3. For a cone, $d(x) = d_a + (d_b - d_a)x/L$, so $dd = (d_b - d_a)\,dx/L$ and
$\int_0^L \frac{4\,dx}{\pi E d^2} = \frac{4L}{\pi E (d_b - d_a)}\left[\frac{1}{d_a} - \frac{1}{d_b}\right] = \frac{4L}{\pi E d_a d_b}$.
Limit: $d_b \to d_a$ gives $L/(EA)$. Units: mm/(MPa·mm²) = mm/N. For the cone in Sec. 2.1, $d_a d_b$ = 450 mm² while $(d_a + d_b)^2/4$ = 506 mm², so the cone is $506/450$ = 1.125 times as flexible as the mean-diameter cylinder.

**D.2 Relation among E, ν and G (Eq. 5).** Take a small square element whose sides carry a pure shear stress $\tau$ (§2.8). Its diagonals are the directions of the principal stresses $+\tau$ and $-\tau$. By the generalized Hooke's law (§2.5), one diagonal stretches by the strain $(\tau + \nu\tau)/E$ and the other shortens by the same amount. For small strains, the right angle between the sides then changes by the difference of the two diagonal strains, $\gamma = 2(1+\nu)\tau/E$. Since $\gamma = \tau/G$ by definition of $G$, Eq. 5 follows.

**D.3 Bending from an offset load (Eq. 6).** An offset $e$ through the thickness adds a bending moment $M = Pe$ about the bar's wide axis (the bending stress formula is derived in Lab 4). With $I = bt^3/12$ and the faces at $\pm t/2$, the bending stress on the faces is $\pm M(t/2)/I = \pm 6Pe/(bt^2)$, while the axial stress is $P/(bt)$. Their ratio is $\beta = 6e/t$, and the strains are in the same ratio. The front reads $\varepsilon_x(1+\beta)$, the back $\varepsilon_x(1-\beta)$, and their average is $\varepsilon_x$ for any $\beta$: the cancellation is exact because bending strain is linear through the thickness and the gages sit at equal distances on opposite sides. A single-gage modulus is $E/(1 \pm \beta)$. Averaging the two single-gage *moduli* gives $E/(1-\beta^2)$, which is biased; averaging the *strains* gives $E$, which is the harmonic mean of the two single-gage moduli.

**D.4 Two members between caps (Eqs. 10–13).** Take $\Delta T = 0$ and member 2 shorter by $g > 0$. Let the cap move down by $\Delta$ (members shorten). Member 1 shortens by $\Delta$, so $F_1 = -k_1\Delta$. Member 2 is untouched until $\Delta = g$, then $F_2 = -k_2(\Delta - g)$. Equilibrium (Eq. 7): before contact, $k_1\Delta = P$; contact occurs when $\Delta = g$, i.e. at $P = k_1g$ (Eq. 10). After contact, $k_1\Delta + k_2(\Delta - g) = P$, so $\Delta = (P + k_2g)/(k_1 + k_2)$ and $F_2 = -k_2(P - k_1g)/(k_1 + k_2)$, which is Eq. 11 with $s = k_2/(k_1 + k_2)$. Member 2 is actually $L - g$ long, so $k_2 = E_2A_2/(L - g)$; with $g/L = 0.0003$ this changes $s$ by 0.02 %. The dial adds $CP$ because the caps carry $P$ in series with the members. Limits: $g \to 0$ gives the textbook $F_2 = -sP$; $k_2 \to 0$ gives $F_2 = 0$; $k_2 \to \infty$ gives $F_2 = -(P - P_{gap})$, a rigid tube that takes everything above $P_{gap}$. The same algebra with the thermal terms of Eq. 9 shows that heating shifts the gap by $(\alpha_2 - \alpha_1)\Delta T\,L$, so a temperature change can close or open it.

**D.5 Bolt and sleeve (Eq. 16).** Cut through the nut: the bolt force $F_b$ and the sleeve force $F_s$ are the only forces on it, so $F_s = -F_b$. At the start the bolt is stretched and the sleeve squeezed by the preload; the combined elastic misfit is $F_0(f_b + f_s)$ with $f = L/(EA)$. Heating adds free elongations $\alpha_b\Delta T L$ and $\alpha_s\Delta T L$. Compatibility (equal final lengths): $\alpha_b\Delta T L + F_b f_b = \alpha_s\Delta T L + F_s f_s + F_0(f_b + f_s)$, where the last term restores the initial misfit. With $F_s = -F_b$: $F_b(f_b + f_s) = F_0(f_b + f_s) + (\alpha_s - \alpha_b)\Delta T L$, which is Eq. 16. For a single bar between rigid walls, $f_s \to 0$ and $F_0 = 0$ give $F_b = E_bA_b(\alpha_s - \alpha_b)\Delta T$; with "sleeve" replaced by a wall that does not expand ($\alpha_s = 0$), $\sigma = -E\alpha\Delta T$, Eq. 15. The joint separates when $F_b$ reaches zero: $\Delta T_{sep} = -F_0(f_b + f_s)/[(\alpha_s - \alpha_b)L]$, which is positive only if $\alpha_b > \alpha_s$.

**D.6 Superposition with a redundant reaction (Eq. 17).** With the right wall removed, the bar is statically determinate: segment 1 carries $P_B$ (equilibrium of a cut between the left wall and B with no right reaction), segment 2 carries nothing, and the free end moves by $\delta_{free} = P_Bf_1 + \Delta T(\alpha_1L_1 + \alpha_2L_2)$ (Eq. 3 plus thermal strain). A force $R$ pushing the end toward $-x$ compresses both segments and moves the end by $-R(f_1 + f_2)$. Because the bar is linear, the two motions add. Compatibility with a wall at distance $g$ requires $\delta_{free} - R(f_1 + f_2) = g$, which is Eq. 17. Superposition is valid only while the set of active supports is fixed: if Eq. 17 returns $R < 0$, the wall would have to pull, which it cannot, so the bar is free and $R = 0$.

**D.7 Fitting a knee (Eq. 11).** For a trial $P_{gap}$, Eq. 11 is linear in $s$, so the least-squares $s$ is $s = -\sum x_iF_i/\sum x_i^2$ with $x_i = \max(0, P_i - P_{gap})$. Scan $P_{gap}$ over a fine grid and keep the value with the smallest sum of squared residuals. The standard errors follow from the residual scatter and the sensitivity of the model to each parameter (the analysis script does this; a spreadsheet can scan $P_{gap}$ in a column). Do not pick the knee by eye from the first non-zero tube reading: the readings are 2 kN apart, so that would locate $P_{gap}$ only to within ±1 kN ($u \approx$ 0.6 kN), while the fit uses every point above the knee and is more than twenty times more precise.

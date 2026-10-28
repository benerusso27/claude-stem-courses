# Style Guide — ENGR 2228 Mechanics of Materials Lab Series

Every handout, simulation, figure, instructor key and data file in this series follows this guide. When a lab needs something this guide does not cover, decide once, add the decision here, and apply it to every lab.

Textbook: F. Beer, E. R. Johnston, J. DeWolf, D. Mazurek, *Mechanics of Materials*, 8th ed. (McGraw-Hill, 2020) — cited as **Beer 8e**. We follow its chapter numbering, notation and sign conventions. We do not reproduce its text, figures or problems.

---

## 1. Units

| Rule | SI (primary) | US customary (toggle / parentheses) |
|---|---|---|
| Stress, strength | MPa | ksi |
| Modulus E, G | GPa | ksi (e.g. 29 000 ksi) |
| Force | N, kN | lb, kip |
| Length (specimens, sections) | mm | in |
| Length (spans, members) | m (mm if < 1 m in a lab setup) | in or ft |
| Moment, torque | N·m, kN·m | lb·in, kip·in |
| Area, second moment | mm², mm⁴ | in², in⁴ |
| Energy density | MJ/m³ (= MPa) | in·lb/in³ (= psi) |
| Temperature change | °C (= K for ΔT) | °F |
| Angle | rad in equations, degrees in readouts | same |

* A space separates a number and its unit (200 GPa); the product dot is used in compound units (N·m).
* Handouts state values in SI with the US value in parentheses only where students meet hardware specified in US units (specimen diameters, machine capacities).
* Simulations open in SI. The **SI / US** toggle converts every input, readout, axis label and CSV column; the model computes internally in SI base units (N, m, Pa) only.
* Conversion constants (exact or to 7 significant figures) live in one place in each simulation (`UNITS` object) and in `shared/units.py`: 1 in = 25.4 mm, 1 lbf = 4.448222 N, 1 ksi = 6.894757 MPa.
* Significant figures: round the uncertainty to 1–2 significant figures, then round the value to the same decimal place (E = 203 ± 4 GPa, not 202.71 ± 3.8 GPa).

## 2. Sign conventions (Beer 8e)

State the conventions that apply **in every handout (a boxed "Sign convention" callout in the Theory section) and in every simulation (a line under the title)**.

| Quantity | Convention | Beer 8e reference |
|---|---|---|
| Normal stress σ, axial force P | Tension positive | 1.2A |
| Normal strain ε | Elongation positive | 2.1A |
| Shear stress τ_xy | Positive on a positive face acting in a positive coordinate direction | 1.4 |
| Shear strain γ_xy | Positive when the angle between the +x and +y faces decreases | 2.7 |
| Torque T, angle of twist φ | Right-hand rule; positive when the vector points out of the cut section (along the outward normal) | 3.1–3.3 |
| Shear V, bending moment M | Positive as in Beer Fig. 5.6: on the left free body V acts downward and M counterclockwise (M > 0 sags). With w > 0 downward: dV/dx = −w, dM/dx = V | 5.1–5.2 |
| Bending stress | σ_x = −My/I, with y measured upward from the neutral axis | 4.2 |
| Beam deflection | y positive **upward**; slope θ = dy/dx; EI d²y/dx² = M(x) | 9.1A |
| Mohr's circle | σ plotted to the right; a face whose shear tends to rotate the element clockwise plots **above** the σ axis (point X at (σ_x, −τ_xy)); a rotation θ of the element is 2θ on the circle in the same sense | 7.2 |
| Temperature change ΔT | Positive for heating | 2.3 |
| Columns | Axial load P reported as a positive compressive magnitude; x down the column from the top end A, y lateral, EI y″ = M with M = −Py (centric) and M = −P(y + e) (eccentric); the column bows away from the load line, so the lever arm at mid-length is e + y_max; the initial bow δ₀ is measured in the bowing direction and δ is the change from the no-load reading | 10.1A (Fig. 10.7), 10.2 (Eq. 10.22, Fig. 10.23) |

## 3. Notation

* Use Beer 8e symbols (its *List of Symbols*): P, A₀, L₀ (gage length), δ, σ, ε, E, ν, G, σ_Y, σ_U, σ_B, σ_t, ε_t, T, J, φ, V, M, I, Q, q, y (deflection in Ch. 9), P_cr, L_e, F.S.
* Spell it "gage", as Beer does.
* Symbols that Beer does not define (strain-hardening exponent n, machine compliance C_m, Swift constant ε₀…) are defined where they first appear and listed in the handout's nomenclature box. If such a symbol clashes with a Beer symbol used later in the course, the handout says so (e.g., Lab 1's n is not Beer's modular ratio n of Ch. 4).
* Every symbol is defined in words at its first appearance in each handout.

## 4. Color, line and marker semantics (color-blind safe)

Palette: Okabe–Ito. Color is never the only carrier of meaning — every color pairs with a distinct line style, marker or label.

### Plots

| Meaning | Light background | Dark background | Line / marker |
|---|---|---|---|
| Closed-form theory (textbook formula) | Blue `#0072B2` | Sky blue `#56B4E9` | solid, 2 px |
| Independent numerical solution (simulation) | Vermillion `#D55E00` | Vermillion `#E8743B` | dashed (6-4), 2 px |
| Measured / sample data | Near-black `#1A1A1A` | Light gray `#E6E6E6` | open circles, 3–4 px |
| Uncertainty (error bars, bands) | Gray `#8C8C8C`, 30 % opacity band | Gray `#A6A6A6` | bars with caps |
| Third series | Reddish purple `#B8478F` (Okabe–Ito `#CC79A7` darkened to ≥ 3 : 1 on white) | `#E08AC0` | dash-dot |
| Fourth series | Bluish green `#00845F` (Okabe–Ito `#009E73` darkened to ≥ 3 : 1 on white) | `#3CC59A` | dotted |
| Region where a model assumption fails | Orange `#E69F00` band, 18 % opacity | same | hatched edge + text label |

### Diagrams (setup sketches, free-body diagrams)

| Element | Style |
|---|---|
| Member / specimen | Fill `#E6E6E6`, outline `#1A1A1A` 1.5 px |
| Applied loads | Vermillion `#D55E00`, solid filled arrowheads |
| Reactions | `#4D4D4D`, open (hollow) arrowheads |
| Stress distributions | Sky-blue fill `#56B4E9` at 45 % opacity, outline `#0072B2` |
| Dimensions | Gray `#666666`, thin lines with ticks |
| Fixed supports / machine parts | Hatching `#666666` |

## 5. Typography

| Medium | Font |
|---|---|
| Handouts and keys (.docx) | Arial (LibreOffice substitutes metric-identical Liberation Sans); equations in Cambria Math (Word's equation font) |
| Figures (SVG, PNG) | Arial / Liberation Sans, 9 pt labels, 8 pt tick labels at print size |
| Simulations | System UI stack: `system-ui, -apple-system, "Segoe UI", Roboto, Arial, sans-serif`; numbers use tabular figures |

Body text 11 pt, headings bold in blue `#0072B2` (contrast 5.0 : 1 on white). Page: US Letter, 1-inch margins.

## 6. Figures

* Each lab has 3–5 figures in `figures/`: SVG master plus 300-dpi PNG copy, same basename (`fig1_setup.svg`, `fig1_setup.png`).
* Full-width figures are 6.5 in wide; half-width are 3.2 in.
* Axis labels read "Quantity, symbol (unit)" — e.g. "Engineering stress, σ (MPa)". Ticks outward, light gridlines, no chart titles inside the image (the caption carries the title).
* Plots of model curves are generated from the series' own models, never traced from the textbook.
* Every figure has alt text in `figures/ALT_TEXT.md`; the same text is embedded in the SVG `<title>`/`<desc>` and in the Word file's image description.

## 7. Handout structure (every lab, in this order)

1. Header block: lab number, title, week, Beer 8e sections, session length, team size.
2. Learning objectives — each tagged with Beer 8e sections.
3. Theory — every key result stated with its equation number, what it means, and the condition (quantified) under which it fails; each result traced to equilibrium, compatibility (geometry) and the constitutive law. Step-by-step derivations go in **Appendix D — Derivations** so the main text stays short. Includes the boxed **Sign convention** and **Nomenclature**.
4. Pre-lab (due at the start of the session) — always begins with an **order-of-magnitude estimate** of what will be measured, and includes a simulation prediction.
5. Equipment and **Safety** (boxed) — load limits stated as numbers.
6. Procedure — numbered steps with checkpoints ("✔ Check: …").
7. Data tables.
8. Analysis — tiered **[Core]**, **[Challenge]**, **[Extension]**; includes uncertainty propagation, a theory-vs-simulation-vs-measurement table with expanded uncertainties, and one question labeled **Where does the model break?**
9. Design problem (open-ended, more than one acceptable answer) with the grading criteria students will be judged on.
10. Report requirements.
11. Appendices: A — data for running the lab without equipment (matching `sample_data.csv`); B — uncertainty quick reference; C — using the simulation; D — derivations.

Question numbering: P1… (pre-lab), A1… (analysis, Core), C1… (Challenge), X1… (Extension), M1 (model break), D1 (design). Equations numbered (1), (2)… within each handout.

Every analysis question requires at least two reasoning steps, a limiting-case or dimensional check, and a one-to-three-sentence interpretation in words.

## 8. Uncertainty conventions

* Standard uncertainty *u* (k = 1). Manufacturer limits ±a convert to *u* = a/√3 (rectangular distribution); a reading resolution r contributes r/√12.
* Combined uncertainty by first-order propagation (root-sum-square of sensitivity-weighted contributions); Challenge tier verifies by Monte Carlo.
* Error bars and agreement tests use the expanded uncertainty **U = 2u_c (≈ 95 %)**.
* Theory and data **agree** when |x_meas − x_theory| ≤ 2·√(u_meas² + u_theory²). A larger discrepancy must be explained by a named physical or procedural cause, quantified where possible.
* Report as `x = 203 ± 8 GPa (U, k = 2)`.

## 9. Simulations

* One self-contained HTML file per lab: no network requests, no external libraries; works offline in any current browser and at phone width (≥ 360 px).
* Layout: title + sign-convention line + SI/US toggle → controls → plots → readout table → convergence study → "push past the assumptions" panel → formula cards → export buttons.
* Required features: sliders for governing parameters (each with typed numeric readout and units), live plots, a readout table comparing **closed-form (textbook)** and **independent numerical** results with % difference and an explanation line, a convergence study (error vs. mesh/step size, log–log with fitted slope), at least one control that pushes the model past its assumptions with a visible warning, and CSV export.
* The physics lives in a single `<script id="model">` block of pure functions (no DOM access) so the Node test harness can load exactly the code the page runs.
* Accessibility: native `<input type="range">` with labels (keyboard operable), visible focus rings, text contrast ≥ 4.5 : 1, plots drawn as SVG with `role="img"` and a text description, status not conveyed by color alone.
* Light and dark themes via CSS custom properties (`prefers-color-scheme`), using the dark-background colors in §4.
* In-plot labels on reference lines are offset in pixels (`dy`), never by a fraction of the value, so they clear the line at phone width; a failure band's label goes at the bottom (`labelPos: 'bottom'`) when curves cross its top.

## 10. Data files

* `sample_data.csv`: UTF-8, comma-separated, one header row, no comment lines, tidy (one observation per row). Column names are `quantity_unit` in snake_case (`load_N`, `extensometer_mm`). Blank cell = not recorded.
* Metadata (specimen dimensions, instrument specifications, post-test measurements) live in the handout appendix and the instructor key, not in the CSV.
* CSV exported from simulations uses the same naming rule with the active unit system (`stress_MPa` or `stress_ksi`).

## 11. Verification (every lab)

* `tests/` contains: a Node test that loads the simulation's model block and compares every closed-form formula against an independent numerical method; an independent Python re-implementation; a browser check at 375 px and 1280 px widths that exercises every slider and button; and `VERIFICATION.md` recording the measured agreement.
* The instructor key's numbers are produced by `src/labNN_analysis.py` from `sample_data.csv`; a separate from-scratch solve of every handout question is compared against the key before release.

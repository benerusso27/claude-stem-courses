## Lab 7 — cross-file consistency (handout, simulation, figures, key, data)

| Check | Result | Detail |
|---|---|---|
| constant 'Part A: span 800, hangers 200/600, indicators 200/400/600' in handout | PASS |  |
| constant 'Part A: span 800, hangers 200/600, indicators 200/400/600' in handout | PASS |  |
| constant 'Part A: span 800, hangers 200/600, indicators 200/400/600' in gen | PASS |  |
| constant 'Part A: span 800, hangers 200/600, indicators 200/400/600' in sim | PASS |  |
| constant 'Part A: span 800, hangers 200/600, indicators 200/400/600' in figs | PASS |  |
| constant 'Part B: free length 700, indicators 350/700, prop 0.5 mm' in handout | PASS |  |
| constant 'Part B: free length 700, indicators 350/700, prop 0.5 mm' in handout | PASS |  |
| constant 'Part B: free length 700, indicators 350/700, prop 0.5 mm' in handout | PASS |  |
| constant 'Part B: free length 700, indicators 350/700, prop 0.5 mm' in gen | PASS |  |
| constant 'Part B: free length 700, indicators 350/700, prop 0.5 mm' in sim | PASS |  |
| constant 'Part B: free length 700, indicators 350/700, prop 0.5 mm' in figs | PASS |  |
| constant 'Part C: strip 12.7 × 0.79, 250 mm, 0.62 kg' in handout | PASS |  |
| constant 'Part C: strip 12.7 × 0.79, 250 mm, 0.62 kg' in handout | PASS |  |
| constant 'Part C: strip 12.7 × 0.79, 250 mm, 0.62 kg' in gen | PASS |  |
| constant 'Part C: strip 12.7 × 0.79, 250 mm, 0.62 kg' in sim | PASS |  |
| constant 'bar 25.4 × 6.35' in handout | PASS |  |
| constant 'bar 25.4 × 6.35' in sim | PASS |  |
| constant 'bar 25.4 × 6.35' in gen | PASS |  |
| constant 'D1: 0.6 σ_Y' in handout | PASS |  |
| constant 'D1: 0.6 σ_Y' in key | PASS |  |
| sign convention box in handout | PASS |  |
| sign convention line in simulation | PASS |  |
| sign convention states 'Deflection $y$ is positive **upward**' in handout | PASS |  |
| sign convention states '$EI\,d^2y/dx^2 = M$ (Eq. 9.4)' in handout | PASS |  |
| sign convention states 'an applied couple is positive counterclockwise' in handout | PASS |  |
| sign convention states 'Reaction forces are positive upward, reaction couples positive counterclockwise' in handout | PASS |  |
| sign convention states 'Tension is positive' in handout | PASS |  |
| sign convention states 'deflection y is positive upward and EI y″ = M (Eq. 9.4)' in sim | PASS |  |
| sign convention states 'an applied couple C is positive counterclockwise' in sim | PASS |  |
| sign convention states 'Reactions: forces positive upward, couples positive counterclockwise' in sim | PASS |  |
| sign convention states '$y$ up, $EI\,y'' = M$, $M > 0$ sags' in key | PASS |  |
| spelling "gage" (as in Beer 8e), never "gauge" | PASS |  |
| every 'Eq. N' reference exists (equations 1–12) | PASS | missing [] |
| equations numbered consecutively | PASS | [] |
| figures first referenced in order 1, 2, 3, ... | PASS | [1, 2, 3, 4] |
| 3–5 figures | PASS | 4 |
| figure 1: PNG copy present | PASS |  |
| figure 1: SVG has <title> and <desc> | PASS |  |
| figure 1: alt text in ALT_TEXT.md | PASS |  |
| figure 1: embedded in handout | PASS |  |
| figure 1: referenced in the text | PASS |  |
| figure 2: PNG copy present | PASS |  |
| figure 2: SVG has <title> and <desc> | PASS |  |
| figure 2: alt text in ALT_TEXT.md | PASS |  |
| figure 2: embedded in handout | PASS |  |
| figure 2: referenced in the text | PASS |  |
| figure 3: PNG copy present | PASS |  |
| figure 3: SVG has <title> and <desc> | PASS |  |
| figure 3: alt text in ALT_TEXT.md | PASS |  |
| figure 3: embedded in handout | PASS |  |
| figure 3: referenced in the text | PASS |  |
| figure 4: PNG copy present | PASS |  |
| figure 4: SVG has <title> and <desc> | PASS |  |
| figure 4: alt text in ALT_TEXT.md | PASS |  |
| figure 4: embedded in handout | PASS |  |
| figure 4: referenced in the text | PASS |  |
| all 20 question IDs in the key exist in the handout | PASS | [] |
| every handout question (20) answered in the key | PASS | [] |
| symbol $\delta$ defined in nomenclature | PASS |  |
| symbol $\theta$ defined in nomenclature | PASS |  |
| symbol $EI$ defined in nomenclature | PASS |  |
| symbol $R_A$ defined in nomenclature | PASS |  |
| symbol $M_A$ defined in nomenclature | PASS |  |
| symbol $\lambda = EI/(kL)$ defined in nomenclature | PASS |  |
| symbol $\Delta$ defined in nomenclature | PASS |  |
| symbol $\alpha = PL^2/EI$ defined in nomenclature | PASS |  |
| symbol $\beta = wL^3/EI$ defined in nomenclature | PASS |  |
| symbol $\theta_0$ defined in nomenclature | PASS |  |
| symbol $\delta_v$ defined in nomenclature | PASS |  |
| symbol $\delta_h$ defined in nomenclature | PASS |  |
| symbol $K$ defined in nomenclature | PASS |  |
| symbol $F$ defined in nomenclature | PASS |  |
| symbol $E(\cdot)$ defined in nomenclature | PASS |  |
| symbol $c$ defined in nomenclature | PASS |  |
| sample_data.csv columns as configured | PASS | ['part', 'config', 'step', 'mass_kg', 'load_pos_mm', 'd1_mm', 'd2_mm', 'd3_mm', 'R_N', 'x_tip_mm', 'y_tip_mm'] |
| every CSV column described in handout Appendix A | PASS | [] |
| every § citation is a real Beer 8e section | PASS | [] |
| Appendix A matches measurements JSON: Bar $b$ (mm) | PASS | 25.42, 25.44, 25.43 vs 25.42, 25.44, 25.43 |
| Appendix A matches measurements JSON: Bar $h$ (mm) | PASS | 6.361, 6.363, 6.362, 6.362 vs 6.361, 6.363, 6.362, 6.362 |
| Appendix A matches measurements JSON: Part A span / indicators / hangers (mm) | PASS | 800.0 / 200.0, 400.0, 600.0 / 200.0, 600.0 vs 800.0 / 200.0, 400.0, 600.0 / 200.0, 600.0 |
| Appendix A matches measurements JSON: Part B free length / indicators (mm) | PASS | 700.0 / 350.0, 700.0 vs 700.0 / 350.0, 700.0 |
| Appendix A matches measurements JSON: Part B3 prop lowered by (mm) | PASS | 0.500 vs 0.500 |
| Appendix A matches measurements JSON: Strip $b$ (mm) | PASS | 12.70, 12.71, 12.69 vs 12.70, 12.71, 12.69 |
| Appendix A matches measurements JSON: Strip $t$ (mm) | PASS | 0.787, 0.788, 0.786, 0.787 vs 0.787, 0.788, 0.786, 0.787 |
| Appendix A matches measurements JSON: Strip free length by rule (mm) | PASS | 250.0 vs 250.0 |
| Table A2 caption accuracy matches measurements JSON: rule | PASS | rule are good to ±0.5 mm |
| Table A2 caption accuracy matches measurements JSON: prop screw | PASS | prop screw to ±0.005 mm |
| Table A2 caption accuracy matches measurements JSON: grid | PASS | grid readings to ±0.5 mm |
| Table 1 steel E and σ_Y equal the Lab 1 measured values | PASS |  |
| Table 1 aluminum E (Lab 2) and σ_Y (Lab 1) equal the earlier labs' values | PASS |  |
| simulation materials: steel 205 GPa / 296.2 MPa, 6061-T6 68.9 GPa / 273.7 MPa, spring steel 203 GPa / 1300 MPa | PASS |  |
| D1 catalog: handout Table 6 equals the analysis catalog (7 sections) | PASS | 7 sections in the analysis |
| D1 load case in handout matches the analysis (4.0 m, 2.0 kN/m, 1.5 kN, 0.6 σ_Y, L/360, 2a/360) | PASS |  |
| D1 simulation preset is the I 102 × 64 geometry on a 4.0 m beam (not the answer's roller position) | PASS |  |
| safety load limits equal the largest loads in the procedure and data (3.0, 1.0, 4.0, 0.62 kg) | PASS |  |
| Part C masses in the procedure equal the data's | PASS |  |
| instructor's beam_deflection.cpp is shipped in reference/ and included verbatim by the test driver | PASS |  |
| the C++ program's y-down convention is stated in the handout and the simulation | PASS |  |
| α where Eq. 10 is 5 % high: handout '0.68' and the key's value agree to two decimals | PASS | 0.676 |
| procedure step 3 'about 10 % more' matches the key's clamp share of the tip deflection | PASS | 9.9 % |
| P5 tells students the B2 preset opens with a flexible clamp, as the simulation does | PASS |  |

101 of 101 passed.

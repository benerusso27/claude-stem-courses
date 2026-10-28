## Lab 9 — cross-file consistency (handout, simulation, figures, key, data)

| Check | Result | Detail |
|---|---|---|
| constant 'bar 25.4 × 6.35 mm' in handout | PASS |  |
| constant 'bar 25.4 × 6.35 mm' in sim | PASS |  |
| constant 'bar 25.4 × 6.35 mm' in gen | PASS |  |
| constant 'bar 25.4 × 6.35 mm' in figs | PASS |  |
| constant 'bar 25.4 × 6.35 mm' in figs | PASS |  |
| constant 'E 68.9 GPa (truth), σ_Y 273.7 MPa, m 17' in sim | PASS |  |
| constant 'E 68.9 GPa (truth), σ_Y 273.7 MPa, m 17' in gen | PASS |  |
| constant 'E 68.9 GPa (truth), σ_Y 273.7 MPa, m 17' in gen | PASS |  |
| constant 'E 68.9 GPa (truth), σ_Y 273.7 MPa, m 17' in figs | PASS |  |
| constant 'lengths 300 / 450 / 600 / 640 / 90 mm' in handout | PASS |  |
| constant 'lengths 300 / 450 / 600 / 640 / 90 mm' in handout | PASS |  |
| constant 'lengths 300 / 450 / 600 / 640 / 90 mm' in handout | PASS |  |
| constant 'lengths 300 / 450 / 600 / 640 / 90 mm' in sim | PASS |  |
| constant 'lengths 300 / 450 / 600 / 640 / 90 mm' in sim | PASS |  |
| constant 'lengths 300 / 450 / 600 / 640 / 90 mm' in sim | PASS |  |
| constant 'lengths 300 / 450 / 600 / 640 / 90 mm' in sim | PASS |  |
| constant 'lengths 300 / 450 / 600 / 640 / 90 mm' in sim | PASS |  |
| constant 'lengths 300 / 450 / 600 / 640 / 90 mm' in figs | PASS |  |
| constant 'lengths 300 / 450 / 600 / 640 / 90 mm' in figs | PASS |  |
| constant 'load cell 5 kN' in handout | PASS |  |
| constant 'load cell 5 kN' in gen | PASS |  |
| constant 'D1 strut 2.0 m, 12 kN, e 2 mm' in handout | PASS |  |
| constant 'D1 strut 2.0 m, 12 kN, e 2 mm' in sim | PASS |  |
| constant 'D1 strut 2.0 m, 12 kN, e 2 mm' in key | PASS |  |
| sign convention box in handout | PASS |  |
| sign convention line in simulation | PASS |  |
| sign convention states 'The axial load $P$ is compressive and is reported as a positive magnitude' in handout | PASS |  |
| sign convention states '$M = -Py$' in handout | PASS |  |
| sign convention states '$M = -P(y + e)$' in handout | PASS |  |
| sign convention states 'the lever arm of the load at mid-length is $e + y_{max}$' in handout | PASS |  |
| sign convention states 'the **front** face is the convex one' in handout | PASS |  |
| sign convention states 'P is the compressive load, reported as a positive magnitude' in sim | PASS |  |
| sign convention states 'M = −P y' in sim | PASS |  |
| sign convention states 'M = −P (y + e)' in sim | PASS |  |
| sign convention states 'lever arm at mid-length is e + y<sub>max</sub>' in sim | PASS |  |
| sign convention states 'the front face is the convex one' in sim | PASS |  |
| sign convention states '$M = -P(y + e)$' in key | PASS |  |
| sign convention states 'front face convex' in key | PASS |  |
| spelling "gage" (as in Beer 8e), never "gauge" | PASS |  |
| every 'Eq. N' reference exists (equations 1–11) | PASS | missing [] |
| equations numbered consecutively | PASS | [] |
| figures first referenced in order 1, 2, 3, ... | PASS | [1, 2, 3, 4, 5] |
| 3–5 figures | PASS | 5 |
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
| figure 5: PNG copy present | PASS |  |
| figure 5: SVG has <title> and <desc> | PASS |  |
| figure 5: alt text in ALT_TEXT.md | PASS |  |
| figure 5: embedded in handout | PASS |  |
| figure 5: referenced in the text | PASS |  |
| all 20 question IDs in the key exist in the handout | PASS | [] |
| every handout question (20) answered in the key | PASS | [] |
| symbol $P_{cr}$ defined in nomenclature | PASS |  |
| symbol $\sigma_{cr} = P_{cr}/A$ defined in nomenclature | PASS |  |
| symbol $E_t$ defined in nomenclature | PASS |  |
| symbol $r = \sqrt{I/A}$ defined in nomenclature | PASS |  |
| symbol $c$$ defined in nomenclature | PASS |  |
| symbol $L$ length$ defined in nomenclature | PASS |  |
| symbol $K$ effective-length$ defined in nomenclature | PASS |  |
| symbol $L_e = KL$ defined in nomenclature | PASS |  |
| symbol $L_e/r$ defined in nomenclature | PASS |  |
| symbol $k$ rotational$ defined in nomenclature | PASS |  |
| symbol $p = \sqrt{P/EI}$ defined in nomenclature | PASS |  |
| symbol $y_{max}$ defined in nomenclature | PASS |  |
| symbol $\delta_0$ defined in nomenclature | PASS |  |
| symbol $\delta$ change$ defined in nomenclature | PASS |  |
| symbol $\alpha = P/P_{cr}$ defined in nomenclature | PASS |  |
| symbol $e$ eccentricity$ defined in nomenclature | PASS |  |
| symbol $\sigma_{max}$ defined in nomenclature | PASS |  |
| symbol $\sigma_Y$ defined in nomenclature | PASS |  |
| symbol $m$ Ramberg$ defined in nomenclature | PASS |  |
| symbol $U = 2u$ defined in nomenclature | PASS |  |
| sample_data.csv columns as configured | PASS | ['part', 'config', 'L_mm', 'e_mm', 'step', 'load_N', 'defl_mm', 'eps_front_ue', 'eps_back_ue'] |
| every CSV column described in handout Appendix A | PASS | [] |
| every § citation is a real Beer 8e section | PASS | [] |
| Table A2 matches the measurements JSON: $b$ (mm) | PASS | 25.41, 25.43, 25.42, 25.42 vs 25.41, 25.43, 25.42, 25.42 |
| Table A2 matches the measurements JSON: $t$ (mm) | PASS | 6.35, 6.36, 6.34, 6.35 vs 6.35, 6.36, 6.34, 6.35 |
| Table A2 matches the measurements JSON: Lengths (mm) | PASS | A: 300.0, 450.0, 600.5; B: 600.5 (fixed–fixed), 640.0 (fixed–pinned); D: 90.0 vs A: 300.0, 450.0, 600.5; B: 600.5 (fixed–fixed), 640.0 (fixed–pinned); D: 90.0 |
| Table A2 matches the measurements JSON: Initial bows (mm) | PASS | A: 0.26, 0.46, 0.62; B: 0.50; D: 0.03 vs A: 0.26, 0.46, 0.62; B: 0.50; D: 0.03 |
| Table A2 matches the measurements JSON: Groove offsets (mm) | PASS | 1.00 and 2.00, ±0.02 vs 1.00 and 2.00, ±0.02 |
| Table A2 caption accuracy matches the measurements JSON: micrometer | PASS | micrometer is good to ±0.003 mm |
| Table A2 caption accuracy matches the measurements JSON: rule | PASS | the rule to ±0.5 mm |
| Table A2 caption accuracy matches the measurements JSON: dial gage | PASS | the dial gage to ±0.01 mm |
| Table A2 caption accuracy matches the measurements JSON: load cell and UTM | PASS | the load cell and the UTM to ±0.5 % of reading |
| Table A2 caption accuracy matches the measurements JSON: gage factor | PASS | the gage factor to ±0.5 % |
| Table 2 (equipment) matches the measurements JSON: gage factor | PASS | Gage factor 2.10 ± 0.5 % |
| Table 2 (equipment) matches the measurements JSON: load cell | PASS | 5 kN load cell (±0.5 % of reading) |
| Table 2 (equipment) matches the measurements JSON: UTM | PASS | 100 kN UTM (±0.5 % of reading) |
| Table 2 (equipment) matches the measurements JSON: grooves | PASS | at 1.00 and 2.00 mm from it (±0.02 mm) |
| Table 2 (equipment) matches the measurements JSON: clamp grip | PASS | clamp blocks gripping 40 mm of the bar |
| Table 2 (equipment) matches the measurements JSON: Part B bar | PASS | one 680 mm bar with gages for Part B |
| Table 2 (equipment) matches the measurements JSON: dial | PASS | Dial gage at mid-length, 0.01 mm divisions, ±0.01 mm |
| Table 2 (equipment) matches the measurements JSON: micrometer and rule | PASS | Micrometer ±0.003 mm; steel rule ±0.5 mm |
| Part B geometry: 680 mm bar − 2 × 40 mm grip = 600 mm free length (procedure, JSON, data) | PASS |  |
| Table 1: E equals the Lab 2 result (68.46 ± 0.47 GPa) | PASS |  |
| Table 1: σ_Y equals the Lab 1 result for 6061-T6 (273.7 ± 1.0 MPa) | PASS |  |
| Table 1: m = 17 is a fit to the Lab 1 curve, and D.7 says how to fit it | PASS |  |
| bar stock: 25.4 × 6.35 mm 6061-T6, the Lab 2 bar (Lab 2 measured b 25.40, t 6.35) | PASS |  |
| kern t/6 = 1.06 mm (Lab 6 reference) | PASS |  |
| simulation 6061-T6: E = 68.9 GPa (series truth), σ_Y and m equal Table 1; steel σ_Y = Lab 1 | PASS |  |
| D1 catalog: handout Table 6 equals the analysis catalog (5 diameters × 4 walls = 20 tubes) | PASS | [44.45, 50.8, 57.15, 63.5, 76.2] × [1.65, 2.11, 3.18, 4.78] |
| D1 requirements in the handout match the analysis (2.0 m, 12 kN, e 2 mm, 1.95, D/t 40, 76.2 mm) | PASS |  |
| D1 simulation preset 'design' is the key's reference tube 63.50 × 1.65 (pinned, 2.0 m, e 2 mm, 12 kN) | PASS |  |
| D1 simulation preset 'designTrap' is the key's fixed-end trap 44.45 × 1.65 | PASS |  |
| D1: the trap's K = 0.52 equals the measured fixed–fixed K rounded | PASS |  |
| procedure = data, A 300: 250 N steps, then 0.50 mm steps, last reading 5.0 mm = L/60 to the dial step | PASS | 13 load steps, deflection steps [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5] |
| procedure = data, A 450: 100 N steps, then 0.75 mm steps, last reading 7.5 mm = L/60 to the dial step | PASS | 14 load steps, deflection steps [0.75, 0.75, 0.75, 0.74, 0.76, 0.75, 0.74, 0.76] |
| procedure = data, A 600: 50 N steps, then 1.00 mm steps, last reading 10.0 mm = L/60 to the dial step | PASS | 16 load steps, deflection steps [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0] |
| procedure = data, B fixed–fixed: 250 N steps, then 1.00 mm steps, last reading 10.0 mm = L/60 to the dial step | PASS | 13 load steps, deflection steps [0.99, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0] |
| procedure = data, B fixed–pinned: 100 N steps, then 1.07 mm steps, last reading 10.7 mm = L/60 to the dial step | PASS | 14 load steps, deflection steps [1.07, 1.07, 1.07, 1.07, 1.06, 1.08, 1.07, 1.07] |
| procedure = data, C e = 1: 100 N steps, then 0.75 mm steps, last reading 7.5 mm = L/60 to the dial step | PASS | 14 load steps, deflection steps [0.75, 0.75, 0.75, 0.75] |
| procedure = data, C e = 2: 100 N steps, then 0.75 mm steps, last reading 7.5 mm = L/60 to the dial step | PASS | 14 load steps, deflection steps [] |
| procedure = data, Part D: 4 kN steps, then 0.05 mm steps through the maximum until the load falls by 15 % | PASS |  |
| safety: the strut-frame loads stay below the 5 kN limit and the deflections stop at L/60 | PASS | max 3814 N |
| safety: the key's largest stress in Parts A–C is under the handout's 55 % of σ_Y | PASS | 142 MPa = 52 % |
| Table 4 spot load 2000 N is a reading of A 300 | PASS |  |
| Table 4 spot load 900 N is a reading of A 450 | PASS |  |
| Table 4 spot load 500 N is a reading of A 600 | PASS |  |
| Table 4 spot load 2000 N is a reading of B fixed–fixed | PASS |  |
| Table 4 spot load 900 N is a reading of B fixed–pinned | PASS |  |
| Table 4 spot load 600 N is a reading of C e = 1 | PASS |  |
| Table 4 spot load 600 N is a reading of C e = 2 | PASS |  |
| procedure check, Part C at 600 N: about 0.9 / 1.5 mm against about 0.26 mm in Part A (data within 0.05 mm) | PASS | {'A': 0.26, 'C1': 0.87, 'C2': 1.46} |
| the Southwell selection (P ≥ 0.5 P_pred) is the same in the handout, the analysis and the key | PASS |  |
| effective-length factors: Beer's 1, 0.699, 0.5, 2 in the handout and the simulation | PASS |  |
| handout Eq. 11 agreement test is the one the key uses (2√(u1² + u2²)) | PASS |  |
| handout tables: nothing labeled Table 6 is missing (Tables 1–8 and A1, A2 captioned once each) | PASS |  |

145 of 145 passed.

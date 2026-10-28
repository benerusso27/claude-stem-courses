## Lab 6 — cross-file consistency (handout, simulation, figures, key, data)

| Check | Result | Detail |
|---|---|---|
| constant 'bar 50.8 × 12.7, L = 250, a = 25' in handout | PASS |  |
| constant 'bar 50.8 × 12.7, L = 250, a = 25' in handout | PASS |  |
| constant 'bar 50.8 × 12.7, L = 250, a = 25' in gen | PASS |  |
| constant 'bar 50.8 × 12.7, L = 250, a = 25' in sim | PASS |  |
| constant 'bar 50.8 × 12.7, L = 250, a = 25' in figs | PASS |  |
| constant 'holes 0, h/6, h/3, b/2' in handout | PASS |  |
| constant 'holes 0, h/6, h/3, b/2' in handout | PASS |  |
| constant 'holes 0, h/6, h/3, b/2' in sim | PASS |  |
| constant 'holes 0, h/6, h/3, b/2' in sim | PASS |  |
| constant 'load limits 30 / 30 / 25 kN' in handout | PASS |  |
| constant 'load limits 30 / 30 / 25 kN' in gen | PASS |  |
| constant 'load limits 30 / 30 / 25 kN' in gen | PASS |  |
| constant 'angle 50.8 × 50.8 × 6.35, gusset 9.53, gage 28.6, L 300' in handout | PASS |  |
| constant 'angle 50.8 × 50.8 × 6.35, gusset 9.53, gage 28.6, L 300' in handout | PASS |  |
| constant 'angle 50.8 × 50.8 × 6.35, gusset 9.53, gage 28.6, L 300' in handout | PASS |  |
| constant 'angle 50.8 × 50.8 × 6.35, gusset 9.53, gage 28.6, L 300' in sim | PASS |  |
| constant 'angle 50.8 × 50.8 × 6.35, gusset 9.53, gage 28.6, L 300' in figs | PASS |  |
| constant 'angle 50.8 × 50.8 × 6.35, gusset 9.53, gage 28.6, L 300' in figs | PASS |  |
| constant 'D1: 40 kN, 1.50 m, 75 mm, 0.6 σ_Y' in handout | PASS |  |
| constant 'D1: 40 kN, 1.50 m, 75 mm, 0.6 σ_Y' in handout | PASS |  |
| constant 'D1: 40 kN, 1.50 m, 75 mm, 0.6 σ_Y' in handout | PASS |  |
| constant 'D1: 40 kN, 1.50 m, 75 mm, 0.6 σ_Y' in handout | PASS |  |
| constant 'D1: 40 kN, 1.50 m, 75 mm, 0.6 σ_Y' in sim | PASS |  |
| sign convention box in handout | PASS |  |
| sign convention line in simulation | PASS |  |
| sign convention states '$M_y = P z_P$ and $M_z = -P y_P$' in handout | PASS |  |
| sign convention states 'Tension is positive' in handout | PASS |  |
| sign convention states '**toward the load line**' in handout | PASS |  |
| sign convention states 'M<sub>y</sub> = P z<sub>P</sub> and M<sub>z</sub> = −P y<sub>P</sub>' in sim | PASS |  |
| sign convention states 'Tension positive' in sim | PASS |  |
| sign convention states 'toward the load line' in sim | PASS |  |
| spelling "gage" (as in Beer 8e), never "gauge" | PASS |  |
| every 'Eq. N' reference exists (equations 1–15) | PASS | missing [] |
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
| all 19 question IDs in the key exist in the handout | PASS | [] |
| every handout question (19) answered in the key | PASS | [] |
| symbol $y_P$ defined in nomenclature | PASS |  |
| symbol $z_P$ defined in nomenclature | PASS |  |
| symbol $M_y$ defined in nomenclature | PASS |  |
| symbol $M_z$ defined in nomenclature | PASS |  |
| symbol $I_{yz}$ defined in nomenclature | PASS |  |
| symbol $\theta_p$ defined in nomenclature | PASS |  |
| symbol $r_z^2$ defined in nomenclature | PASS |  |
| symbol $y_0$ defined in nomenclature | PASS |  |
| symbol $C = M/(Pe)$ defined in nomenclature | PASS |  |
| symbol $P_{cr}$ defined in nomenclature | PASS |  |
| symbol $e_{eff}$ defined in nomenclature | PASS |  |
| symbol $\varepsilon_b$ defined in nomenclature | PASS |  |
| symbol $k = \sqrt{P/EI}$ defined in nomenclature | PASS |  |
| sample_data.csv columns as configured | PASS | ['part', 'config', 'step', 'load_N', 'w_mid_mm', 'g01_ue', 'g02_ue', 'g03_ue', 'g04_ue', 'g05_ue', 'g06_ue', 'g07_ue', 'g08_ue', 'g09_ue', 'g10_ue', 'g11_ue', 'g12_ue'] |
| every CSV column described in handout Appendix A | PASS | [] |
| every § citation is a real Beer 8e section | PASS | [] |
| Appendix A matches measurements JSON: Bar $h$ / $b$ (mm) | PASS | 50.84, 50.82, 50.83 / 12.681, 12.678, 12.684 vs 50.84, 50.82, 50.83 / 12.681, 12.678, 12.684 |
| Appendix A matches measurements JSON: Bar $L$ / $a$ (mm) | PASS | 250.0 / 25.0 vs 250.0 / 25.0 |
| Appendix A matches measurements JSON: Hole offsets $e$: e0, e1, e2 / ez (mm) | PASS | 0.04, 8.49, 16.95 / 6.40 (through the thickness) vs 0.04, 8.49, 16.95 / 6.40 (through the thickness) |
| Appendix A matches measurements JSON: Gage heights $y$, front (mm) | PASS | −20.1, −10.0, 0.1, 10.1, 20.0 vs −20.1, −10.0, 0.1, 10.1, 20.0 |
| Appendix A matches measurements JSON: Gage heights $y$, back (mm) | PASS | −20.0, −10.1, 0.0, 9.9, 20.1 vs −20.0, −10.1, 0.0, 9.9, 20.1 |
| Appendix A matches measurements JSON: End pair, distance from the block face (mm) | PASS | 40.0 vs 40.0 |
| Appendix A matches measurements JSON: Angle legs $b_V$ / $b_H$ (mm) | PASS | 50.86, 50.84, 50.85 / 50.75, 50.77, 50.76 vs 50.86, 50.84, 50.85 / 50.75, 50.77, 50.76 |
| Appendix A matches measurements JSON: Angle thickness $t$ (mm) | PASS | 6.331, 6.334, 6.328, 6.331 vs 6.331, 6.334, 6.328, 6.331 |
| Appendix A matches measurements JSON: Angle root-fillet radius (mm) | PASS | 4.8 vs 4.8 |
| Appendix A matches measurements JSON: Angle $L$ / $a$ (mm) | PASS | 300.0 / 25.0 vs 300.0 / 25.0 |
| Appendix A matches measurements JSON: Angle load point from the heel, $z$ / $y$ (mm) | PASS | −28.58 / −4.76 vs −28.58 / −4.76 |
| Appendix A matches measurements JSON: G1, G2 ($z$ = 0) heights $y$ / G3, G4 ($y$ = 0) positions $z$ (mm) | PASS | 44.0, 12.0 / −12.0, −44.0 vs 44.0, 12.0 / −12.0, −44.0 |
| Table 1 E equals the Lab 2 measured value | PASS |  |
| Table 1 σ_Y equals the Lab 1 measured value | PASS |  |
| simulation 6061-T6: E = 68.9 GPa (series truth value), σ_Y = Lab 1 value | PASS |  |
| Lab 8 tube in X2 matches the simulation preset (D_o 38.1, D_i 31.75, F 600 N, L_b 250, a_L 200) | PASS |  |
| D1 catalog: gage and thickness in the handout match the analysis catalog | PASS |  |
| z points left in section views: stated in handout, simulation and figures | PASS |  |

97 of 97 passed.

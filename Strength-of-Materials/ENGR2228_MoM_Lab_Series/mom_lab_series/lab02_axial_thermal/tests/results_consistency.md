## Lab 2 — cross-file consistency (handout, simulation, figures, key, data)

| Check | Result | Detail |
|---|---|---|
| constant 'Part A bar 25.40 mm × 6.35 mm' in handout | PASS |  |
| constant 'Part A bar 25.40 mm × 6.35 mm' in gen | PASS |  |
| constant 'Part B rod d = 12.70 mm, L = 150 mm' in handout | PASS |  |
| constant 'Part B rod d = 12.70 mm, L = 150 mm' in handout | PASS |  |
| constant 'Part B rod d = 12.70 mm, L = 150 mm' in sim | PASS |  |
| constant 'Part B rod d = 12.70 mm, L = 150 mm' in sim | PASS |  |
| constant 'Part B rod d = 12.70 mm, L = 150 mm' in gen | PASS |  |
| constant 'Part B rod d = 12.70 mm, L = 150 mm' in gen | PASS |  |
| constant 'Part B tube 25.40 × 19.05 mm' in handout | PASS |  |
| constant 'Part B tube 25.40 × 19.05 mm' in sim | PASS |  |
| constant 'Part B tube 25.40 × 19.05 mm' in gen | PASS |  |
| constant 'Part B gap 0.040 mm' in handout | PASS |  |
| constant 'Part B gap 0.040 mm' in sim | PASS |  |
| constant 'Part B gap 0.040 mm' in gen | PASS |  |
| constant 'Part C bolt 10.00 mm, sleeve 20.00 × 10.50 mm, L = 100 mm' in handout | PASS |  |
| constant 'Part C bolt 10.00 mm, sleeve 20.00 × 10.50 mm, L = 100 mm' in sim | PASS |  |
| constant 'Part C bolt 10.00 mm, sleeve 20.00 × 10.50 mm, L = 100 mm' in gen | PASS |  |
| constant 'Part C preload 2.0 kN (124 µε)' in handout | PASS |  |
| constant 'Part C preload 2.0 kN (124 µε)' in handout | PASS |  |
| constant 'Part C preload 2.0 kN (124 µε)' in sim | PASS |  |
| constant 'Part C preload 2.0 kN (124 µε)' in gen | PASS |  |
| constant 'Part C preload 2.0 kN (124 µε)' in key | PASS |  |
| constant 'load limits 18 kN and 30 kN' in handout | PASS |  |
| constant 'load limits 18 kN and 30 kN' in handout | PASS |  |
| constant 'load limits 18 kN and 30 kN' in gen | PASS |  |
| constant 'load limits 18 kN and 30 kN' in gen | PASS |  |
| constant 'bath 20 → 80 °C' in handout | PASS |  |
| constant 'bath 20 → 80 °C' in gen | PASS |  |
| constant 'bath 20 → 80 °C' in figs | PASS |  |
| constant 'gage factor 2.10 ± 1 %' in handout | PASS |  |
| sign convention box in handout | PASS |  |
| sign convention line in simulation | PASS |  |
| sign convention states 'Tension is positive' in handout | PASS |  |
| sign convention states 'positive **magnitude**' in handout | PASS |  |
| sign convention states '$g < 0$ is an interference' in handout | PASS |  |
| sign convention states 'tension positive' in sim | PASS |  |
| sign convention states 'compressive magnitude' in sim | PASS |  |
| spelling "gage" (as in Beer 8e), never "gauge" | PASS |  |
| every 'Eq. N' reference exists (equations 1–21) | PASS | missing [] |
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
| all 21 question IDs in the key exist in the handout | PASS | [] |
| every handout question (21) answered in the key | PASS | [] |
| symbol $k_i$ defined in nomenclature | PASS |  |
| symbol $f_i$ defined in nomenclature | PASS |  |
| symbol $P_{gap}$ defined in nomenclature | PASS |  |
| symbol $\beta$ defined in nomenclature | PASS |  |
| symbol $C$$ defined in nomenclature | PASS |  |
| symbol $\Delta$$ defined in nomenclature | PASS |  |
| symbol $F_0$ defined in nomenclature | PASS |  |
| symbol $GF$ defined in nomenclature | PASS |  |
| symbol $P_B$ defined in nomenclature | PASS |  |
| symbol $d_a$ defined in nomenclature | PASS |  |
| symbol $\varepsilon_y$ defined in nomenclature | PASS |  |
| symbol $\alpha_b$ defined in nomenclature | PASS |  |
| symbol $s$$ defined in nomenclature | PASS |  |
| symbol $G$$ defined in nomenclature | PASS |  |
| symbol $\nu$ defined in nomenclature | PASS |  |
| sample_data.csv columns as configured | PASS | ['part', 'step', 'temperature_C', 'load_N', 'strain_axial_front_ue', 'strain_axial_back_ue', 'strain_transverse_front_ue', 'strain_transverse_back_ue', 'strain_tube_front_ue', 'strain_tube_back_ue', 'dial_mm', 'strain_bolt_ue'] |
| every CSV column described in handout Appendix A | PASS | [] |
| every § citation is a real Beer 8e section | PASS | [] |
| Appendix A readings match measurements JSON: Part A width | PASS | 25.41, 25.39, 25.40 vs 25.41, 25.39, 25.40 |
| Appendix A readings match measurements JSON: Part A thickness | PASS | 6.36, 6.34, 6.35 vs 6.36, 6.34, 6.35 |
| Appendix A readings match measurements JSON: Part B rod diameter (mm) | PASS | 12.70, 12.71, 12.70 vs 12.70, 12.71, 12.70 |
| Appendix A readings match measurements JSON: Part B tube outer diameter (mm) | PASS | 25.41, 25.40, 25.40 vs 25.41, 25.40, 25.40 |
| Appendix A readings match measurements JSON: Part B tube inner diameter (mm) | PASS | 19.04, 19.06, 19.05 vs 19.04, 19.06, 19.05 |
| Appendix A readings match measurements JSON: Part C bolt shank diameter (mm) | PASS | 10.00, 10.01, 10.00 vs 10.00, 10.01, 10.00 |
| Appendix A readings match measurements JSON: Part C sleeve outer diameter (mm) | PASS | 20.00, 20.01, 20.00 vs 20.00, 20.01, 20.00 |
| Appendix A readings match measurements JSON: Part C sleeve inner diameter (mm) | PASS | 10.50, 10.51, 10.50 vs 10.50, 10.51, 10.50 |
| Appendix A rod/tube lengths match JSON | PASS | 150.00 / 149.96 |
| Figure 3 example (brass rod 16 mm, steel tube 30×24 mm, g = 0.12 mm) matches handout text | PASS |  |
| material E and α identical in handout Table 1, simulation and analysis reference values | PASS |  |
| steel modulus matches Lab 1 (205 GPa) across the series | PASS |  |
| no compression-positive statement anywhere | PASS |  |

100 of 100 passed.

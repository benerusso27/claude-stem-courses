## Lab 4 — cross-file consistency (handout, simulation, figures, key, data)

| Check | Result | Detail |
|---|---|---|
| constant 'span 600 mm' in handout | PASS |  |
| constant 'span 600 mm' in sim | PASS |  |
| constant 'span 600 mm' in gen | PASS |  |
| constant 'span 600 mm' in figs | PASS |  |
| constant 'shear span a = 200 mm' in handout | PASS |  |
| constant 'shear span a = 200 mm' in sim | PASS |  |
| constant 'shear span a = 200 mm' in figs | PASS |  |
| constant 'bar 25.4 × 50.8 mm' in handout | PASS |  |
| constant 'bar 25.4 × 50.8 mm' in sim | PASS |  |
| constant 'bar 25.4 × 50.8 mm' in figs | PASS |  |
| constant 'steel strip 6.35 mm' in handout | PASS |  |
| constant 'steel strip 6.35 mm' in sim | PASS |  |
| constant 'steel strip 6.35 mm' in figs | PASS |  |
| constant 'bottom gages at x = 100, 150 mm' in handout | PASS |  |
| constant 'bottom gages at x = 100, 150 mm' in gen | PASS |  |
| constant 'bottom gages at x = 100, 150 mm' in figs | PASS |  |
| constant 'load limits 20/15/40 kN, stops 22/17/42 kN' in handout | PASS |  |
| constant 'load limits 20/15/40 kN, stops 22/17/42 kN' in handout | PASS |  |
| constant 'load limits 20/15/40 kN, stops 22/17/42 kN' in gen | PASS |  |
| constant 'load limits 20/15/40 kN, stops 22/17/42 kN' in sim | PASS |  |
| constant 'D1: 3.0 m, 3.0 kN/m, 5.0 kN, FS 1.67, L/240' in handout | PASS |  |
| constant 'D1: 3.0 m, 3.0 kN/m, 5.0 kN, FS 1.67, L/240' in handout | PASS |  |
| constant 'D1: 3.0 m, 3.0 kN/m, 5.0 kN, FS 1.67, L/240' in handout | PASS |  |
| constant 'D1: 3.0 m, 3.0 kN/m, 5.0 kN, FS 1.67, L/240' in handout | PASS |  |
| constant 'D1: 3.0 m, 3.0 kN/m, 5.0 kN, FS 1.67, L/240' in handout | PASS |  |
| sign convention box in handout | PASS |  |
| sign convention line in simulation | PASS |  |
| sign convention states '$dV/dx = -w$' in handout | PASS |  |
| sign convention states '**counterclockwise**' in handout | PASS |  |
| sign convention states '$\sigma_x = -My/I$' in handout | PASS |  |
| sign convention states 'dV/dx = −w' in sim | PASS |  |
| sign convention states 'counterclockwise' in sim | PASS |  |
| sign convention states 'σ<sub>x</sub> = −My/I' in sim | PASS |  |
| spelling "gage" (as in Beer 8e), never "gauge" | PASS |  |
| every 'Eq. N' reference exists (equations 1–18) | PASS | missing [] |
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
| symbol $\kappa$ defined in nomenclature | PASS |  |
| symbol $y_{NA}$ defined in nomenclature | PASS |  |
| symbol $y_h$ defined in nomenclature | PASS |  |
| symbol $I_t$ defined in nomenclature | PASS |  |
| symbol $\bar y$ defined in nomenclature | PASS |  |
| symbol $M_Y$ defined in nomenclature | PASS |  |
| symbol $\kappa_Y$ defined in nomenclature | PASS |  |
| symbol $M_p$ defined in nomenclature | PASS |  |
| symbol $Z$$ defined in nomenclature | PASS |  |
| symbol $S = I/c$ defined in nomenclature | PASS |  |
| symbol $\kappa_p$ defined in nomenclature | PASS |  |
| symbol $\sigma_{res}$ defined in nomenclature | PASS |  |
| symbol $\rho'$ defined in nomenclature | PASS |  |
| symbol $n = E_2/E_1$ defined in nomenclature | PASS |  |
| symbol $t_s$ defined in nomenclature | PASS |  |
| symbol $y_Y$ defined in nomenclature | PASS |  |
| symbol $\varepsilon_z$ defined in nomenclature | PASS |  |
| symbol $\nu$ defined in nomenclature | PASS |  |
| sample_data.csv columns as configured | PASS | ['part', 'step', 'load_N', 'strain_side1_ue', 'strain_side2_ue', 'strain_side3_ue', 'strain_side4_ue', 'strain_side5_ue', 'strain_top_ue', 'strain_bottom_ue', 'strain_transverse_top_ue', 'strain_bottom_x100_ue', 'strain_bottom_x150_ue'] |
| every CSV column described in handout Appendix A | PASS | [] |
| every § citation is a real Beer 8e section | PASS | [] |
| Appendix A readings match measurements JSON: b_mm | PASS | 25.43, 25.41, 25.42 vs 25.43, 25.41, 25.42 |
| Appendix A readings match measurements JSON: h_mm | PASS | 50.79, 50.77, 50.78 vs 50.79, 50.77, 50.78 |
| Appendix A readings match measurements JSON: ts_mm | PASS | 6.37, 6.35, 6.36 vs 6.37, 6.35, 6.36 |
| Appendix A readings match measurements JSON: yA_mm | PASS | 5.65, 15.18, 25.49, 35.15, 45.62 vs 5.65, 15.18, 25.49, 35.15, 45.62 |
| Appendix A readings match measurements JSON: yB_mm | PASS | 10.28, 20.21, 30.40, 40.09, 50.25 vs 10.28, 20.21, 30.40, 40.09, 50.25 |
| Appendix A span and load rollers match JSON | PASS |  |
| Appendix A straightedge gap matches JSON | PASS |  |
| Appendix A bar length matches JSON | PASS |  |
| Table 1 aluminum E and ν equal the Lab 2 measured values (carried forward) | PASS | Lab 2: E = 68.459, ν = 0.3296 |
| Table 1 yield strengths equal the Lab 1 measured values (carried forward) | PASS |  |
| steel E = 205 GPa as in Labs 1–3 | PASS |  |
| simulation 6061-T6 curve = Lab 1 truth family (E 68.9 GPa, σ_Y 274 MPa, m 17) | PASS |  |
| Table 6 catalog dimensions match the analysis catalog | PASS | [True, True, True, True, True, True, True, True, True, True] |
| no hogging-positive or compression-positive statement | PASS |  |
| sign of the flexure formula: σ = −My/I in handout, key and simulation | PASS |  |

101 of 101 passed.

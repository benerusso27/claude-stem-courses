## Lab 3 — cross-file consistency (handout, simulation, figures, key, data)

| Check | Result | Detail |
|---|---|---|
| constant 'specimen d = 6.35 mm' in handout | PASS |  |
| constant 'specimen d = 6.35 mm' in sim | PASS |  |
| constant 'specimen d = 6.35 mm' in figs | PASS |  |
| constant 'gage length 50.8 mm' in handout | PASS |  |
| constant 'gage length 50.8 mm' in sim | PASS |  |
| constant 'gage length 50.8 mm' in gen | PASS |  |
| constant 'gage length 50.8 mm' in figs | PASS |  |
| constant 'reduced length 76.2 mm' in handout | PASS |  |
| constant 'reduced length 76.2 mm' in figs | PASS |  |
| constant 'troptometer removed at 10°' in handout | PASS |  |
| constant 'troptometer removed at 10°' in gen | PASS |  |
| constant 'troptometer removed at 10°' in sim | PASS |  |
| constant 'head rates 0.25°/s and 15°/s' in handout | PASS |  |
| constant 'head rates 0.25°/s and 15°/s' in handout | PASS |  |
| constant 'head rates 0.25°/s and 15°/s' in gen | PASS |  |
| constant 'machine capacity 60 N·m, stop 40 N·m' in handout | PASS |  |
| constant 'machine capacity 60 N·m, stop 40 N·m' in handout | PASS |  |
| constant 'machine capacity 60 N·m, stop 40 N·m' in key | PASS |  |
| constant 'cast iron σ_UT 214 MPa' in handout | PASS |  |
| constant 'cast iron σ_UT 214 MPa' in sim | PASS |  |
| constant 'cast iron σ_UT 214 MPa' in gen | PASS |  |
| constant 'D1: 15 kW, 1200 rpm, 1.50 m, K = 1.6, FS 2.0, 1.0°' in handout | PASS |  |
| constant 'D1: 15 kW, 1200 rpm, 1.50 m, K = 1.6, FS 2.0, 1.0°' in handout | PASS |  |
| constant 'D1: 15 kW, 1200 rpm, 1.50 m, K = 1.6, FS 2.0, 1.0°' in handout | PASS |  |
| constant 'D1: 15 kW, 1200 rpm, 1.50 m, K = 1.6, FS 2.0, 1.0°' in handout | PASS |  |
| constant 'D1: 15 kW, 1200 rpm, 1.50 m, K = 1.6, FS 2.0, 1.0°' in handout | PASS |  |
| sign convention box in handout | PASS |  |
| sign convention line in simulation | PASS |  |
| sign convention states 'right-hand rule' in handout | PASS |  |
| sign convention states 'points out of the cut section' in handout | PASS |  |
| sign convention states 'right-hand rule' in sim | PASS |  |
| sign convention states 'points out of the cut section' in sim | PASS |  |
| spelling "gage" (as in Beer 8e), never "gauge" | PASS |  |
| every 'Eq. N' reference exists (equations 1–20) | PASS | missing [] |
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
| symbol $\varphi$ defined in nomenclature | PASS |  |
| symbol $\theta$ defined in nomenclature | PASS |  |
| symbol $J$$ defined in nomenclature | PASS |  |
| symbol $G$$ defined in nomenclature | PASS |  |
| symbol $\tau_Y$ defined in nomenclature | PASS |  |
| symbol $T_Y$ defined in nomenclature | PASS |  |
| symbol $\rho_Y$ defined in nomenclature | PASS |  |
| symbol $T_p$ defined in nomenclature | PASS |  |
| symbol $T_U$ defined in nomenclature | PASS |  |
| symbol $R_T$ defined in nomenclature | PASS |  |
| symbol $\varphi_p$ defined in nomenclature | PASS |  |
| symbol $\tau_{res}$ defined in nomenclature | PASS |  |
| symbol $L_c$ defined in nomenclature | PASS |  |
| symbol $C_m$ defined in nomenclature | PASS |  |
| symbol $\Delta_{head}$ defined in nomenclature | PASS |  |
| symbol $\Delta_{toe}$ defined in nomenclature | PASS |  |
| symbol $c_1$ defined in nomenclature | PASS |  |
| symbol $A_m$ defined in nomenclature | PASS |  |
| symbol $\sigma_{UT}$ defined in nomenclature | PASS |  |
| sample_data.csv columns as configured | PASS | ['specimen', 'time_s', 'torque_Nm', 'troptometer_deg', 'head_deg'] |
| every CSV column described in handout Appendix A | PASS | [] |
| every § citation is a real Beer 8e section | PASS | [] |
| Appendix A readings match measurements JSON: steel | PASS | 6.351, 6.349, 6.350, 6.352, 6.348, 6.350 vs 6.351, 6.349, 6.350, 6.352, 6.348, 6.350 |
| Appendix A readings match measurements JSON: al | PASS | 6.353, 6.351, 6.352, 6.354, 6.350, 6.352 vs 6.353, 6.351, 6.352, 6.354, 6.350, 6.352 |
| Appendix A readings match measurements JSON: ci | PASS | 6.349, 6.347, 6.348, 6.350, 6.346, 6.348 vs 6.349, 6.347, 6.348, 6.350, 6.346, 6.348 |
| Appendix A gage and reduced lengths match JSON | PASS |  |
| Table 1 aluminum E and ν equal the Lab 2 measured values (carried forward) | PASS | Lab 2: E = 68.459, ν = 0.3296 |
| Table 1 aluminum uncertainties equal Lab 2's standard uncertainties | PASS |  |
| steel E = 205 GPa as in Labs 1 and 2 | PASS |  |
| simulation steel G ≈ E/(2(1 + ν)) with series values (79.5 GPa) | PASS |  |
| no compression-positive or clockwise-positive torque statement | PASS |  |

95 of 95 passed.

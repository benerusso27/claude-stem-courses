## Lab 8 — cross-file consistency (handout, simulation, figures, key, data)

| Check | Result | Detail |
|---|---|---|
| constant 'tube 38.1 × 3.18' in handout | PASS |  |
| constant 'tube 38.1 × 3.18' in sim | PASS |  |
| constant 'tube 38.1 × 3.18' in gen | PASS |  |
| constant 'tube 38.1 × 3.18' in figs | PASS |  |
| constant 'arms 250 / 200 mm' in handout | PASS |  |
| constant 'arms 250 / 200 mm' in handout | PASS |  |
| constant 'arms 250 / 200 mm' in sim | PASS |  |
| constant 'arms 250 / 200 mm' in gen | PASS |  |
| constant 'arms 250 / 200 mm' in figs | PASS |  |
| constant 'arms 250 / 200 mm' in figs | PASS |  |
| constant '8 MPa' in handout | PASS |  |
| constant '8 MPa' in sim | PASS |  |
| constant '8 MPa' in gen | PASS |  |
| constant 'K_t 1.2 %, ν0 0.285' in handout | PASS |  |
| constant 'K_t 1.2 %, ν0 0.285' in handout | PASS |  |
| constant 'K_t 1.2 %, ν0 0.285' in gen | PASS |  |
| constant 'K_t 1.2 %, ν0 0.285' in sim | PASS |  |
| sign convention box in handout | PASS |  |
| sign convention line in simulation | PASS |  |
| sign convention states 'Tension is positive' in handout | PASS |  |
| sign convention states 'plotted above the $\sigma$ axis (Fig. 7.15)' in handout | PASS |  |
| sign convention states '$(\sigma_x, -\tau_{xy})$' in handout | PASS |  |
| sign convention states 'counterclockwise from $x$' in handout | PASS |  |
| sign convention states 'tension positive' in sim | PASS |  |
| sign convention states 'plotted above the σ axis (Fig. 7.15)' in sim | PASS |  |
| sign convention states 'X = (σ<sub>x</sub>, −τ<sub>xy</sub>)' in sim | PASS |  |
| sign convention states 'Mohr's circle "clockwise above"' in key | PASS |  |
| spelling "gage" (as in Beer 8e), never "gauge" | PASS |  |
| every 'Eq. N' reference exists (equations 1–13) | PASS | missing [] |
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
| symbol $\sigma_{ave}$ defined in nomenclature | PASS |  |
| symbol $R$ defined in nomenclature | PASS |  |
| symbol $\theta_p$ defined in nomenclature | PASS |  |
| symbol $\sigma_1 \ge \sigma_2 \ge \sigma_3$ defined in nomenclature | PASS |  |
| symbol $\tau_{max}$ defined in nomenclature | PASS |  |
| symbol $\gamma_{xy}$ defined in nomenclature | PASS |  |
| symbol $\beta$ defined in nomenclature | PASS |  |
| symbol $K_t$ defined in nomenclature | PASS |  |
| symbol $G$ defined in nomenclature | PASS |  |
| symbol $t_w = r_o - r_i$ defined in nomenclature | PASS |  |
| symbol $Q$ defined in nomenclature | PASS |  |
| symbol $a_L$ defined in nomenclature | PASS |  |
| symbol $L_b$ defined in nomenclature | PASS |  |
| symbol $\sigma_\theta$ defined in nomenclature | PASS |  |
| symbol $\sigma_r$ defined in nomenclature | PASS |  |
| symbol $U = 2u$ defined in nomenclature | PASS |  |
| sample_data.csv columns as configured | PASS | ['part', 'config', 'step', 'load_N', 'lever_mm', 'p_MPa', 'Ha_ue', 'Hb_ue', 'Hc_ue', 'Ka_ue', 'Kb_ue', 'Kc_ue'] |
| every CSV column described in handout Appendix A | PASS | [] |
| every § citation is a real Beer 8e section | PASS | [] |
| Appendix A matches measurements JSON: $D_o$ (mm) | PASS | 38.12, 38.14, 38.13, 38.13 vs 38.12, 38.14, 38.13, 38.13 |
| Appendix A matches measurements JSON: Wall thickness (mm) | PASS | 3.20, 3.21, 3.20, 3.21 vs 3.20, 3.21, 3.20, 3.21 |
| Appendix A matches measurements JSON: $L_b$ / $a_L$ (mm) | PASS | 250.0 / 200.0 vs 250.0 / 200.0 |
| Appendix A matches measurements JSON: Rosettes | PASS | gage factor 2.10 ± 0.5 %, $K_t$ = 1.2 %, $\nu_0$ = 0.285 vs gage factor 2.10 ± 0.5 %, $K_t$ = 1.2 %, $\nu_0$ = 0.285 |
| Table A2 caption accuracy matches measurements JSON: micrometer | PASS | micrometer is good to ±0.003 mm |
| Table A2 caption accuracy matches measurements JSON: ball micrometer | PASS | ball micrometer to ±0.005 mm |
| Table A2 caption accuracy matches measurements JSON: rule | PASS | the rule to ±0.5 mm |
| Table A2 caption accuracy matches measurements JSON: load cell | PASS | load cell to ±0.5 % |
| Table A2 caption accuracy matches measurements JSON: pressure | PASS | pressure transducer to ±0.05 MPa |
| Table 1: E and ν equal the Lab 2 results | PASS |  |
| Table 1: G equals the Lab 3 result for 6061-T6 | PASS |  |
| Table 1: σ_Y equals the Lab 1 result for 6061-T6 | PASS |  |
| simulation 6061-T6: E = 68.9 GPa (series truth value), σ_Y = Lab 1 value | PASS |  |
| Lab 6 X2 prediction carried into Lab 8 P1: σ at the top | PASS | Lab 6 53.36 |
| Lab 6 X2 prediction carried into Lab 8 P1: Tc/J | PASS | Lab 6 21.34 |
| Lab 6 X2 prediction carried into Lab 8 P1: VQ/It | PASS | Lab 6 3.43 |
| Lab 6 X2 prediction carried into Lab 8 P1: τ at K | PASS | Lab 6 24.77 |
| D1 catalog: handout Table 6 equals the analysis catalog (11 tubes) | PASS | 11 tubes |
| D1 requirements in the handout match the analysis (20 MPa, 300 N·m, 300 N·m, 1.8, 3.0°/m, 50.8 mm) | PASS |  |
| D1 simulation preset: M = T = 300 N·m (F 1000 N on 0.3 m arms), 20 MPa, 44.45 × 4.78, inner surface | PASS |  |
| safety limits equal the largest load and pressure in the data (600 N, 8 MPa) | PASS |  |
| procedure steps equal the data's (100 N steps; 2, 4, 6, 8 MPa; 200, 400, 600 N at 8 MPa) | PASS |  |
| the local-axis convention is stated in the handout, the simulation and Figure 1 | PASS |  |
| thin-wall radius: Beer's inner radius used in the handout, the model and the page | PASS |  |

97 of 97 passed.

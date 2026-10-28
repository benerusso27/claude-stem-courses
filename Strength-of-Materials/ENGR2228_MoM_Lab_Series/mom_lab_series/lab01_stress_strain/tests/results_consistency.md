## Lab 1 — cross-file consistency (handout, simulation, figures, key, data)

| Check | Result | Detail |
|---|---|---|
| constant 'd0 = 10.00 mm' in handout | PASS |  |
| constant 'd0 = 10.00 mm' in simulation default | PASS |  |
| constant 'd0 = 10.00 mm' in figures | PASS |  |
| constant 'gage / extensometer length 50.0 mm' in handout | PASS |  |
| constant 'gage / extensometer length 50.0 mm' in generator | PASS |  |
| constant 'gage / extensometer length 50.0 mm' in simulation default | PASS |  |
| constant 'gage / extensometer length 50.0 mm' in figures | PASS |  |
| constant 'reduced section 60 mm' in handout | PASS |  |
| constant 'reduced section 60 mm' in generator | PASS |  |
| constant 'reduced section 60 mm' in simulation (Lc = 1.2 L0) | PASS |  |
| constant 'reduced section 60 mm' in figures | PASS |  |
| constant 'compliance 0.008 mm/kN' in handout | PASS |  |
| constant 'compliance 0.008 mm/kN' in generator | PASS |  |
| constant 'compliance 0.008 mm/kN' in simulation default | PASS |  |
| constant 'rates 1.0 then 5.0 mm/min, removal at 4.0 %' in handout | PASS |  |
| constant 'rates 1.0 then 5.0 mm/min, removal at 4.0 %' in generator | PASS |  |
| constant 'rates 1.0 then 5.0 mm/min, removal at 4.0 %' in key | PASS |  |
| constant 'imperfection 0.3 %' in handout | PASS |  |
| constant 'imperfection 0.3 %' in simulation default | PASS |  |
| constant 'imperfection 0.3 %' in generator | PASS |  |
| sign convention box in handout (tension positive) | PASS |  |
| sign convention line in simulation (tension positive) | PASS |  |
| no compression-positive statement anywhere | PASS |  |
| simulation SI unit for stress is MPa | PASS |  |
| simulation SI unit for modulus is GPa | PASS |  |
| simulation SI unit for length is mm | PASS |  |
| simulation SI unit for force is kN | PASS |  |
| simulation SI unit for compliance is mm/kN | PASS |  |
| simulation SI unit for energy is MJ/m³ | PASS |  |
| simulation US toggle present | PASS |  |
| every 'Eq. N' reference exists (equations 1–23) | PASS | missing [] |
| equations numbered consecutively | PASS | [] |
| figures first referenced in order 1, 2, 3, ... | PASS | [1, 2, 3, 4, 5] |
| figure 1: SVG and PNG present | PASS |  |
| figure 1: SVG has <title> and <desc> | PASS |  |
| figure 1: alt text in ALT_TEXT.md | PASS |  |
| figure 1: embedded in handout | PASS |  |
| figure 2: SVG and PNG present | PASS |  |
| figure 2: SVG has <title> and <desc> | PASS |  |
| figure 2: alt text in ALT_TEXT.md | PASS |  |
| figure 2: embedded in handout | PASS |  |
| figure 3: SVG and PNG present | PASS |  |
| figure 3: SVG has <title> and <desc> | PASS |  |
| figure 3: alt text in ALT_TEXT.md | PASS |  |
| figure 3: embedded in handout | PASS |  |
| figure 4: SVG and PNG present | PASS |  |
| figure 4: SVG has <title> and <desc> | PASS |  |
| figure 4: alt text in ALT_TEXT.md | PASS |  |
| figure 4: embedded in handout | PASS |  |
| figure 5: SVG and PNG present | PASS |  |
| figure 5: SVG has <title> and <desc> | PASS |  |
| figure 5: alt text in ALT_TEXT.md | PASS |  |
| figure 5: embedded in handout | PASS |  |
| all 22 question IDs in the key exist in the handout | PASS | [] |
| every handout question answered in the key | PASS | [] |
| symbol $E_{app}$ defined in nomenclature | PASS |  |
| symbol $C_m$ defined in nomenclature | PASS |  |
| symbol $\Delta_{toe}$ defined in nomenclature | PASS |  |
| symbol $\varepsilon_u$ defined in nomenclature | PASS |  |
| symbol $\delta_A$ defined in nomenclature | PASS |  |
| symbol $\ell$ defined in nomenclature | PASS |  |
| symbol $L_c$ defined in nomenclature | PASS |  |
| symbol $L_e$ defined in nomenclature | PASS |  |
| symbol $\sigma_t$ defined in nomenclature | PASS |  |
| symbol $\varepsilon_t$ defined in nomenclature | PASS |  |
| strain-hardening n flagged as different from Beer's modular ratio | PASS |  |
| CSV columns match handout Table A1 | PASS | ['specimen', 'time_s', 'load_N', 'crosshead_mm', 'extensometer_mm'] |
| steel_1018HR: d0 readings in Appendix A match | PASS |  |
| steel_1018HR: L0, Lf in Appendix A match | PASS |  |
| steel_1018HR: df readings in Appendix A match | PASS |  |
| al_6061T6: d0 readings in Appendix A match | PASS |  |
| al_6061T6: L0, Lf in Appendix A match | PASS |  |
| al_6061T6: df readings in Appendix A match | PASS |  |
| every § citation is a real Beer 8e section | PASS | [] |

74 of 74 passed.

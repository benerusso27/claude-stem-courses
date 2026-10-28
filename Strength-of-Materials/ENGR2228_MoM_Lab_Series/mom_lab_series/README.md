# ENGR 2228 Mechanics of Materials — Lab Series

A classroom-ready series of nine labs for a sophomore Mechanics of Materials course using Beer, Johnston, DeWolf and Mazurek, *Mechanics of Materials*, 8th ed. (Beer 8e). Each lab pairs a hands-on test with an interactive simulation. Students estimate with theory before measuring, run the test (or use the sample data) and explain every difference between theory, simulation and measurement.

**Status:** all nine labs are built and verified (table below). `lab_map.md` gives each lab's week, Beer 8e sections, concepts, equipment and simulation. `style_guide.md` holds the conventions every file follows.

<!--STATUS-->
| Lab | Topic | Week | Handout / key (pages) | Figures | Node: formula vs numerics | Python: independent + closure | From-scratch re-solve vs key | Consistency | Browser 375/1280 px | Verified |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | [Tension test and the stress–strain diagram](lab01_stress_strain/) | 3 | 17 / 8 | 5 | PASS (77/77) | PASS (43/43) | PASS (45/45) | PASS (74/74) | PASS | 2026-10-27 |
| 2 | [Axial members: E, ν, indeterminate and thermal](lab02_axial_thermal/) | 5 | 19 / 8 | 5 | PASS (54/54) | PASS (22/22) | PASS (50/50) | PASS (100/100) | PASS | 2026-10-27 |
| 3 | [Torsion](lab03_torsion/) | 7 | 16 / 8 | 5 | PASS (79/79) | PASS (69/69) | PASS (39/39) | PASS (95/95) | PASS | 2026-10-27 |
| 4 | [Pure bending, composite sections, beyond yield](lab04_bending/) | 8 | 17 / 9 | 5 | PASS (79/79) | PASS (53/53) | PASS (62/62) | PASS (101/101) | PASS | 2026-10-27 |
| 5 | [Transverse shear and shear flow](lab05_shear/) | 10 | 17 / 8 | 5 | PASS (79/79) | PASS (80/80) | PASS (50/50) | PASS (103/103) | PASS | 2026-10-27 |
| 6 | [Eccentric axial loading](lab06_eccentric/) | 12 | 17 / 9 | 5 | PASS (192/192) | PASS (140/140) | PASS (38/38) | PASS (97/97) | PASS | 2026-10-27 |
| 7 | [Beam deflection, indeterminate beams, elastica](lab07_deflection/) | 13 | 15 / 9 | 4 | PASS (212/212) | PASS (288/288) | PASS (35/35) | PASS (101/101) | PASS | 2026-10-27 |
| 8 | [Stress and strain transformation, rosettes, pressure vessels](lab08_transformation/) | 14 | 15 / 9 | 4 | PASS (255/255) | PASS (156/156) | PASS (24/24) | PASS (97/97) | PASS | 2026-10-27 |
| 9 | [Columns: buckling, imperfections, secant formula](lab09_columns/) | 15 | 17 / 8 | 5 | PASS (154/154) | PASS (97/97) | PASS (200/200) | PASS (145/145) | PASS | 2026-10-26 |
<!--/STATUS-->

## What is in the package

```
README.md                  this file
lab_map.md                 lab -> week -> Beer 8e sections -> concepts -> equipment -> simulation -> status
style_guide.md             units, sign conventions, notation, colors, figures, handout structure, uncertainty, verification
labNN_<topic>/             one folder per lab, all with the same layout:
  labNN_handout.docx/.pdf          student handout (edit the .docx; the .pdf is typeset from the same source)
  labNN_instructor_key.docx/.pdf   worked solutions, expected ranges, common mistakes, rubric, instructor notes, self-critique
  labNN_simulation.html            interactive simulation (one file, offline, any browser, phones included)
  sample_data.csv                  realistic "measured" data, so the lab can run without equipment
  figures/                         4–5 figures as SVG + 300-dpi PNG, with ALT_TEXT.md
  tests/                           verification scripts and their results (VERIFICATION.md)
  src/                             sources: handout and key Markdown, model, data generator, analysis, figure script
lab07_deflection/reference/  the supplied beam_deflection.cpp (the Lab 7 page runs a line-by-line port of it)
shared/                    build tools, shared simulation core, test harness, Word and PDF templates
```

## Every handout has the same structure

Header table → learning objectives (with Beer 8e sections) → concise theory with numbered equations, a **Sign convention (Beer 8e)** box and a nomenclature box → pre-lab (P1 is always an estimate before measuring; one question predicts with the simulation) → equipment and a **Safety** box with load limits → procedure with **Check:** steps → data tables → analysis questions tiered **[Core]**, **[Challenge]** and **[Extension]**, each asking for at least two reasoning steps, a dimensional or limiting-case check and an interpretation, plus an M1 question on where the model breaks → an open-ended design problem (D1) with its grading table → report requirements and points → appendices: A sample data, B uncertainty, C the simulation, D derivations.

The instructor key follows one pattern too: results at a glance, worked solutions for every question, the D1 reference design and rubric detail, expected ranges for real class data, common mistakes, the grading rubric, instructor notes (preparation, timing, safety) and a self-critique (the three biggest weaknesses found before release and how each was fixed, plus known limitations).

## Opening and running

* **Handouts and keys.** Open the `.docx` in Word, LibreOffice or Google Docs to edit (equations are native, editable Word equations). The `.pdf` is ready to print or post. Keep the instructor keys away from students.
* **Simulations.** Double-click `labNN_simulation.html`. Each needs no internet connection, no installation and no server, and works in any current browser, on phones too. Every simulation has presets matching the lab's parts, a readout table comparing each textbook closed form with an independent numerical method, a convergence study, a "Push the model past its assumptions" panel, an SI / US customary toggle that converts every input, readout and export, and **Export (CSV)**. If a browser blocks the download, the data appears in a box with a Copy button.
* **Sample data.** `sample_data.csv` holds every part of the lab; its columns are described in Appendix A of the handout. The specimen measurements that go with it are in Appendix A and in `src/specimen_measurements.json`.
* **Your own class data.** Export the machine's data with the columns listed in Appendix A, write a measurements JSON like `src/specimen_measurements.json`, then run `python3 src/labNN_analysis.py your.csv your.json`; with no arguments it reads the sample files. It writes `results.json` and prints every quantity in the key with its uncertainty; `python3 src/make_key.py` then rebuilds the key from those results.

## Rebuilding and verifying (optional)

Requirements: Python 3.11+ with numpy, scipy, matplotlib, python-docx and playwright; Node 18+; pandoc 3; XeLaTeX (for the PDFs); Chromium for the browser check (`playwright install chromium` if not present).

```bash
python3 shared/build_docs.py make-reference                       # Word template (once)
cd lab09_columns/src                                              # any lab: labNN_<topic>/src
python3 generate_sample_data.py      # sample_data.csv, truth.json, specimen_measurements.json
python3 lab09_analysis.py            # results.json (every number in the key)
python3 make_figures.py              # figures/*.svg, *.png, ALT_TEXT.md
python3 make_key.py                  # lab09_instructor_key.md and key_values.json
cd ../..
python3 shared/build_sim.py lab09_columns
python3 shared/build_docs.py build lab09_columns/src/lab09_handout.md --out lab09_columns/lab09_handout.docx \
        --header "Lab 9 · Columns" --alt lab09_columns/figures/ALT_TEXT.md
python3 shared/build_docs.py build lab09_columns/src/lab09_instructor_key.md --out lab09_columns/lab09_instructor_key.docx \
        --header "Lab 9 · Instructor Key"
python3 shared/verify_lab.py lab09_columns                        # all verification; writes tests/VERIFICATION.md
```

Verification for each lab covers six things:
* Every closed-form formula the simulation uses is checked against an independent numerical method, running the page's own code in Node (`tests/test_labNN_model.js`).
* A second implementation in Python/scipy cross-checks the page's results, and a closure test confirms the analysis recovers the values that generated the sample data (`tests/test_labNN_independent.py`).
* Every handout question is re-solved from scratch, without the lab's analysis or model code, and compared with the number printed in the key (`tests/solve_from_scratch.py`).
* Units, symbols, sign conventions, constants, tables, procedure steps against the data, and references to other labs are checked across all files (`tests/consistency_check.py`).
* A browser test drives every control at 375 and 1280 px in light and dark mode, checking for errors, horizontal scrolling and blank values.
* Each lab's results are recorded in `tests/VERIFICATION.md`.

## Defaults chosen (cheap to change; listed so you can check them)

| Decision | Default | Where to change |
|---|---|---|
| Handout format | .docx (editable, native equations) + PDF typeset from the same Markdown; long derivations in Appendix D | `src/*.md`, `shared/build_docs.py` |
| Units | SI primary; US customary through the simulation toggle and in parentheses for hardware specs | `style_guide.md` §1 |
| Uncertainty | Standard u; error bars and agreement at U = 2u; ±a limits → a/√3 | `style_guide.md` §8 |
| Sign conventions | Beer 8e throughout (tension positive; V, M per Fig. 5.6; y up in deflection; Mohr "clockwise above"; columns per Fig. 10.7 and Eq. 10.22) | `style_guide.md` §2 |
| Materials carried forward | 1018 HR steel and 6061-T6: E, ν, σ_Y and the stress–strain curve measured in Labs 1–2 are the reference values of later labs (Table 1 of each handout) | each handout, Table 1 |
| Language | Python for analysis, figures and tests; JavaScript in the pages; Lab 7 keeps the supplied C++ solver as a reference test | `src/`, `tests/` |
| Equipment | Listed per lab in `lab_map.md` and Table 2 of each handout; every lab can also run from the simulation and the sample data alone | per lab |

## Notes

* Problems, numbers, figures and text are original; the series follows Beer 8e's chapters, notation and sign conventions without reproducing its content.
* Accessibility: color-blind-safe Okabe–Ito palette with line styles and markers, so color is never the only cue; labeled axes with units; alt text for every figure (in the SVG, in `figures/ALT_TEXT.md` and in the Word files); keyboard-operable simulation controls; light and dark themes.

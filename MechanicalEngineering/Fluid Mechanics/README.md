# Fluid Mechanics lecture companions (ENGR/EGTG 4254, FDU)

Interactive pages that follow the instructor's slide decks for Mott & Untener, *Applied Fluid Mechanics*, 8th ed.
One page per lecture topic in syllabus order, plus a final-exam review. Each page can be projected in class
(press **Present** in the top bar, or Alt+P) and reread afterward as a study guide.

Plain HTML, CSS and JavaScript. No build step is needed to view or host the site.

## Contents

| File | Topic |
| --- | --- |
| `index.html` | Home page, week by week |
| `ch01-02-properties.html` | Ch 1–2 Fluid properties and viscosity |
| `ch03-pressure.html` | Ch 3 Pressure in static fluids, manometers |
| `ch04-static-forces.html` | Ch 4 Forces on submerged plane and curved surfaces |
| `ch05-buoyancy.html` | Ch 5 Buoyancy and stability |
| `ch06-bernoulli.html` | Ch 6 Continuity and Bernoulli |
| `ch07-energy.html` | Ch 7 General energy equation, pump power |
| `ch08-reynolds-friction.html` | Ch 8 Reynolds number, Darcy, Moody |
| `ch09-noncircular.html` | Ch 9 Flow visualization, velocity profiles, hydraulic radius |
| `ch10-minor-losses.html` | Ch 10 Minor losses and equivalent length |
| `ch11-pipe-systems.html` | Ch 11–12 Series and parallel pipes |
| `ch13-pumps.html` | Ch 13 Pump selection, NPSH, affinity laws |
| `ch16-momentum.html` | Ch 16 Forces due to fluids in motion |
| `ch17-drag-lift.html` | Ch 17 Drag and lift |
| `review.html` | Final exam review |
| `assets/` | Shared stylesheet, calculation library (`fm-core.js`), page helpers (`fm-ui.js`), MathJax 3.2.2 (bundled so equations work offline) |
| `tests/` | `core.test.js` checks the calculations against textbook and slide answers; `browser_check.js` loads every page in a headless browser |
| `_build/` | Page sources and the script that assembles them (only needed if you edit pages) |

## Put it on GitHub

1. Unzip the folder.
2. In GitHub Desktop: **File → Add local repository**, choose the folder, and accept the offer to create a repository.
3. Write a summary such as "Add fluid mechanics pages" and click **Commit to main**.
4. Click **Publish repository**. Untick "Keep this code private" only if you intend the site to be public (see the note below).
5. On github.com, open the repository, then **Settings → Pages**. Under "Build and deployment", choose **Deploy from a branch**, branch **main**, folder **/ (root)**, and **Save**.
6. After a minute or two the address appears at the top of the Pages screen (`https://<your-user>.github.io/<repo-name>/`).

GitHub Pages sites are public even when made from a private repository on most plans.

## Editing a page

Edit the matching file in `_build/pages/`, then run `python3 _build/build.py` to regenerate the top-level HTML files.
Run `node tests/core.test.js` after changing anything in `assets/fm-core.js`.

## Notes on use

- Textbook problem statements are paraphrased, and all figures are drawn for this site; no text or figures are copied from
  the textbook or slides. Worked solutions to textbook problems are still homework solutions: ask the instructor before
  posting them publicly, and check the course's academic-integrity rules.
- Property values come from Mott's appendices. Where the pages read numbers from a chart, they say so; use the textbook's
  charts and tables on graded work.
- The pump curve on the Ch 13 page and the airfoil curves on the Ch 17 page are illustrative models, not catalog data.

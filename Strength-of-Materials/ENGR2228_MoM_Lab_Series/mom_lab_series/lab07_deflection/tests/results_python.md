## Lab 7 — independent checks (Python/scipy) and data-pipeline closure

| Test | Value | Reference | Rel. difference | Tolerance | Result |
|---|---:|---:|---:|---:|---|
| [partA] closed form y(x), JS vs Python, max \|Δ\|/\|y\|max (absolute) | 0 | 0 | 0.00e+00 | 1.0e-12 | PASS |
| [partA] closed form slope, JS vs Python, max \|Δ\|/\|θ\|max (absolute) | 1.8717498e-16 | 0 | 1.87e-16 | 1.0e-12 | PASS |
| [partA] closed form y(x) (JS) vs double integration of M/EI (Python), max \|Δ\|/\|y\|max (absolute) | 7.1440431e-15 | 0 | 7.14e-15 | 1.0e-07 | PASS |
| [partA] finite elements y(x) (JS port of the C++) vs double integration (Python), max \|Δ\|/\|y\|max (absolute) | 7.6365381e-10 | 0 | 7.64e-10 | 1.0e-06 | PASS |
| [partA] finite elements slope vs double integration, max \|Δ\|/\|θ\|max (absolute) | 7.5257958e-10 | 0 | 7.53e-10 | 1.0e-05 | PASS |
| [partA] reaction RA, JS vs Python closed form (relative to the largest reaction) (absolute) | 0 | 0 | 0.00e+00 | 1.0e-12 | PASS |
| [partA] reaction RB, JS vs Python closed form (relative to the largest reaction) (absolute) | 0 | 0 | 0.00e+00 | 1.0e-12 | PASS |
| [partA] finite-element reactions (Ku − F) vs double-integration reactions, worst relative to the largest (absolute) | 8.2426108e-10 | 0 | 8.24e-10 | 1.0e-06 | PASS |
| [partA] M(x) from statics with the JS reactions vs Python, max \|Δ\|/\|M\|max (absolute) | 8.0505772e-16 | 0 | 8.05e-16 | 1.0e-06 | PASS |
| [partAboth] closed form y(x), JS vs Python, max \|Δ\|/\|y\|max (absolute) | 0 | 0 | 0.00e+00 | 1.0e-12 | PASS |
| [partAboth] closed form slope, JS vs Python, max \|Δ\|/\|θ\|max (absolute) | 2.0687761e-16 | 0 | 2.07e-16 | 1.0e-12 | PASS |
| [partAboth] closed form y(x) (JS) vs double integration of M/EI (Python), max \|Δ\|/\|y\|max (absolute) | 6.7994207e-15 | 0 | 6.80e-15 | 1.0e-07 | PASS |
| [partAboth] finite elements y(x) (JS port of the C++) vs double integration (Python), max \|Δ\|/\|y\|max (absolute) | 8.1753994e-10 | 0 | 8.18e-10 | 1.0e-06 | PASS |
| [partAboth] finite elements slope vs double integration, max \|Δ\|/\|θ\|max (absolute) | 8.9041094e-10 | 0 | 8.90e-10 | 1.0e-05 | PASS |
| [partAboth] reaction RA, JS vs Python closed form (relative to the largest reaction) (absolute) | 0 | 0 | 0.00e+00 | 1.0e-12 | PASS |
| [partAboth] reaction RB, JS vs Python closed form (relative to the largest reaction) (absolute) | 0 | 0 | 0.00e+00 | 1.0e-12 | PASS |
| [partAboth] finite-element reactions (Ku − F) vs double-integration reactions, worst relative to the largest (absolute) | 1.1568925e-09 | 0 | 1.16e-09 | 1.0e-06 | PASS |
| [partAboth] M(x) from statics with the JS reactions vs Python, max \|Δ\|/\|M\|max (absolute) | 5.8222924e-16 | 0 | 5.82e-16 | 1.0e-06 | PASS |
| [partB1] closed form y(x), JS vs Python, max \|Δ\|/\|y\|max (absolute) | 1.5510977e-16 | 0 | 1.55e-16 | 1.0e-12 | PASS |
| [partB1] closed form slope, JS vs Python, max \|Δ\|/\|θ\|max (absolute) | 0 | 0 | 0.00e+00 | 1.0e-12 | PASS |
| [partB1] closed form y(x) (JS) vs double integration of M/EI (Python), max \|Δ\|/\|y\|max (absolute) | 6.204391e-15 | 0 | 6.20e-15 | 1.0e-07 | PASS |
| [partB1] finite elements y(x) (JS port of the C++) vs double integration (Python), max \|Δ\|/\|y\|max (absolute) | 3.6040133e-09 | 0 | 3.60e-09 | 1.0e-06 | PASS |
| [partB1] finite elements slope vs double integration, max \|Δ\|/\|θ\|max (absolute) | 3.4272148e-09 | 0 | 3.43e-09 | 1.0e-05 | PASS |
| [partB1] reaction RA, JS vs Python closed form (relative to the largest reaction) (absolute) | 0 | 0 | 0.00e+00 | 1.0e-12 | PASS |
| [partB1] reaction RB, JS vs Python closed form (relative to the largest reaction) (absolute) | 0 | 0 | 0.00e+00 | 1.0e-12 | PASS |
| [partB1] reaction MA, JS vs Python closed form (relative to the largest reaction) (absolute) | 0 | 0 | 0.00e+00 | 1.0e-12 | PASS |
| [partB1] reaction MB, JS vs Python closed form (relative to the largest reaction) (absolute) | 0 | 0 | 0.00e+00 | 1.0e-12 | PASS |
| [partB1] finite-element reactions (Ku − F) vs double-integration reactions, worst relative to the largest (absolute) | 5.1889967e-09 | 0 | 5.19e-09 | 1.0e-06 | PASS |
| [partB1] M(x) from statics with the JS reactions vs Python, max \|Δ\|/\|M\|max (absolute) | 1.2938428e-16 | 0 | 1.29e-16 | 1.0e-06 | PASS |
| [partB1 rigid=True] closed form y(x), JS vs Python, max \|Δ\|/\|y\|max (absolute) | 1.7189539e-16 | 0 | 1.72e-16 | 1.0e-12 | PASS |
| [partB1 rigid=True] closed form slope, JS vs Python, max \|Δ\|/\|θ\|max (absolute) | 0 | 0 | 0.00e+00 | 1.0e-12 | PASS |
| [partB1 rigid=True] closed form y(x) (JS) vs double integration of M/EI (Python), max \|Δ\|/\|y\|max (absolute) | 7.0477109e-15 | 0 | 7.05e-15 | 1.0e-07 | PASS |
| [partB1 rigid=True] finite elements y(x) (JS port of the C++) vs double integration (Python), max \|Δ\|/\|y\|max (absolute) | 3.1967265e-10 | 0 | 3.20e-10 | 1.0e-06 | PASS |
| [partB1 rigid=True] finite elements slope vs double integration, max \|Δ\|/\|θ\|max (absolute) | 4.0227197e-10 | 0 | 4.02e-10 | 1.0e-05 | PASS |
| [partB1 rigid=True] reaction RA, JS vs Python closed form (relative to the largest reaction) (absolute) | 0 | 0 | 0.00e+00 | 1.0e-12 | PASS |
| [partB1 rigid=True] reaction RB, JS vs Python closed form (relative to the largest reaction) (absolute) | 0 | 0 | 0.00e+00 | 1.0e-12 | PASS |
| [partB1 rigid=True] reaction MA, JS vs Python closed form (relative to the largest reaction) (absolute) | 0 | 0 | 0.00e+00 | 1.0e-12 | PASS |
| [partB1 rigid=True] reaction MB, JS vs Python closed form (relative to the largest reaction) (absolute) | 0 | 0 | 0.00e+00 | 1.0e-12 | PASS |
| [partB1 rigid=True] finite-element reactions (Ku − F) vs double-integration reactions, worst relative to the largest (absolute) | 1.4835569e-09 | 0 | 1.48e-09 | 1.0e-06 | PASS |
| [partB1 rigid=True] M(x) from statics with the JS reactions vs Python, max \|Δ\|/\|M\|max (absolute) | 1.2938428e-16 | 0 | 1.29e-16 | 1.0e-06 | PASS |
| [partB2] closed form y(x), JS vs Python, max \|Δ\|/\|y\|max (absolute) | 2.7516811e-15 | 0 | 2.75e-15 | 1.0e-09 | PASS |
| [partB2] closed form slope, JS vs Python, max \|Δ\|/\|θ\|max (absolute) | 0 | 0 | 0.00e+00 | 1.0e-09 | PASS |
| [partB2] closed form y(x) (JS) vs double integration of M/EI (Python), max \|Δ\|/\|y\|max (absolute) | 2.6410463e-11 | 0 | 2.64e-11 | 1.0e-07 | PASS |
| [partB2] finite elements y(x) (JS port of the C++) vs double integration (Python), max \|Δ\|/\|y\|max (absolute) | 4.0806571e-11 | 0 | 4.08e-11 | 1.0e-06 | PASS |
| [partB2] finite elements slope vs double integration, max \|Δ\|/\|θ\|max (absolute) | 4.8768117e-11 | 0 | 4.88e-11 | 1.0e-05 | PASS |
| [partB2] reaction RA, JS vs Python closed form (relative to the largest reaction) (absolute) | 0 | 0 | 0.00e+00 | 1.0e-09 | PASS |
| [partB2] reaction RB, JS vs Python closed form (relative to the largest reaction) (absolute) | 0 | 0 | 0.00e+00 | 1.0e-09 | PASS |
| [partB2] reaction MA, JS vs Python closed form (relative to the largest reaction) (absolute) | 0 | 0 | 0.00e+00 | 1.0e-09 | PASS |
| [partB2] reaction MB, JS vs Python closed form (relative to the largest reaction) (absolute) | 0 | 0 | 0.00e+00 | 1.0e-09 | PASS |
| [partB2] finite-element reactions (Ku − F) vs double-integration reactions, worst relative to the largest (absolute) | 2.2933767e-10 | 0 | 2.29e-10 | 1.0e-06 | PASS |
| [partB2] M(x) from statics with the JS reactions vs Python, max \|Δ\|/\|M\|max (absolute) | 4.3986982e-12 | 0 | 4.40e-12 | 1.0e-06 | PASS |
| [partB2 rigid=True] closed form y(x), JS vs Python, max \|Δ\|/\|y\|max (absolute) | 1.5375688e-15 | 0 | 1.54e-15 | 1.0e-09 | PASS |
| [partB2 rigid=True] closed form slope, JS vs Python, max \|Δ\|/\|θ\|max (absolute) | 0 | 0 | 0.00e+00 | 1.0e-09 | PASS |
| [partB2 rigid=True] closed form y(x) (JS) vs double integration of M/EI (Python), max \|Δ\|/\|y\|max (absolute) | 2.7742822e-11 | 0 | 2.77e-11 | 1.0e-07 | PASS |
| [partB2 rigid=True] finite elements y(x) (JS port of the C++) vs double integration (Python), max \|Δ\|/\|y\|max (absolute) | 2.1988425e-10 | 0 | 2.20e-10 | 1.0e-06 | PASS |
| [partB2 rigid=True] finite elements slope vs double integration, max \|Δ\|/\|θ\|max (absolute) | 1.8416574e-10 | 0 | 1.84e-10 | 1.0e-05 | PASS |
| [partB2 rigid=True] reaction RA, JS vs Python closed form (relative to the largest reaction) (absolute) | 0 | 0 | 0.00e+00 | 1.0e-09 | PASS |
| [partB2 rigid=True] reaction RB, JS vs Python closed form (relative to the largest reaction) (absolute) | 0 | 0 | 0.00e+00 | 1.0e-09 | PASS |
| [partB2 rigid=True] reaction MA, JS vs Python closed form (relative to the largest reaction) (absolute) | 0 | 0 | 0.00e+00 | 1.0e-09 | PASS |
| [partB2 rigid=True] reaction MB, JS vs Python closed form (relative to the largest reaction) (absolute) | 0 | 0 | 0.00e+00 | 1.0e-09 | PASS |
| [partB2 rigid=True] finite-element reactions (Ku − F) vs double-integration reactions, worst relative to the largest (absolute) | 3.1206321e-10 | 0 | 3.12e-10 | 1.0e-06 | PASS |
| [partB2 rigid=True] M(x) from statics with the JS reactions vs Python, max \|Δ\|/\|M\|max (absolute) | 4.1347764e-12 | 0 | 4.13e-12 | 1.0e-06 | PASS |
| [partB3] closed form y(x), JS vs Python, max \|Δ\|/\|y\|max (absolute) | 1.5085902e-15 | 0 | 1.51e-15 | 1.0e-09 | PASS |
| [partB3] closed form slope, JS vs Python, max \|Δ\|/\|θ\|max (absolute) | 0 | 0 | 0.00e+00 | 1.0e-09 | PASS |
| [partB3] closed form y(x) (JS) vs double integration of M/EI (Python), max \|Δ\|/\|y\|max (absolute) | 7.5416309e-12 | 0 | 7.54e-12 | 1.0e-07 | PASS |
| [partB3] finite elements y(x) (JS port of the C++) vs double integration (Python), max \|Δ\|/\|y\|max (absolute) | 4.2417313e-11 | 0 | 4.24e-11 | 1.0e-06 | PASS |
| [partB3] finite elements slope vs double integration, max \|Δ\|/\|θ\|max (absolute) | 7.9270174e-11 | 0 | 7.93e-11 | 1.0e-05 | PASS |
| [partB3] reaction RA, JS vs Python closed form (relative to the largest reaction) (absolute) | 0 | 0 | 0.00e+00 | 1.0e-09 | PASS |
| [partB3] reaction RB, JS vs Python closed form (relative to the largest reaction) (absolute) | 0 | 0 | 0.00e+00 | 1.0e-09 | PASS |
| [partB3] reaction MA, JS vs Python closed form (relative to the largest reaction) (absolute) | 0 | 0 | 0.00e+00 | 1.0e-09 | PASS |
| [partB3] reaction MB, JS vs Python closed form (relative to the largest reaction) (absolute) | 0 | 0 | 0.00e+00 | 1.0e-09 | PASS |
| [partB3] finite-element reactions (Ku − F) vs double-integration reactions, worst relative to the largest (absolute) | 2.5717601e-10 | 0 | 2.57e-10 | 1.0e-06 | PASS |
| [partB3] M(x) from statics with the JS reactions vs Python, max \|Δ\|/\|M\|max (absolute) | 1.4037659e-12 | 0 | 1.40e-12 | 1.0e-06 | PASS |
| [partB3 rigid=True] closed form y(x), JS vs Python, max \|Δ\|/\|y\|max (absolute) | 1.654373e-15 | 0 | 1.65e-15 | 1.0e-09 | PASS |
| [partB3 rigid=True] closed form slope, JS vs Python, max \|Δ\|/\|θ\|max (absolute) | 0 | 0 | 0.00e+00 | 1.0e-09 | PASS |
| [partB3 rigid=True] closed form y(x) (JS) vs double integration of M/EI (Python), max \|Δ\|/\|y\|max (absolute) | 7.6923176e-12 | 0 | 7.69e-12 | 1.0e-07 | PASS |
| [partB3 rigid=True] finite elements y(x) (JS port of the C++) vs double integration (Python), max \|Δ\|/\|y\|max (absolute) | 1.889871e-10 | 0 | 1.89e-10 | 1.0e-06 | PASS |
| [partB3 rigid=True] finite elements slope vs double integration, max \|Δ\|/\|θ\|max (absolute) | 2.3449022e-10 | 0 | 2.34e-10 | 1.0e-05 | PASS |
| [partB3 rigid=True] reaction RA, JS vs Python closed form (relative to the largest reaction) (absolute) | 0 | 0 | 0.00e+00 | 1.0e-09 | PASS |
| [partB3 rigid=True] reaction RB, JS vs Python closed form (relative to the largest reaction) (absolute) | 0 | 0 | 0.00e+00 | 1.0e-09 | PASS |
| [partB3 rigid=True] reaction MA, JS vs Python closed form (relative to the largest reaction) (absolute) | 0 | 0 | 0.00e+00 | 1.0e-09 | PASS |
| [partB3 rigid=True] reaction MB, JS vs Python closed form (relative to the largest reaction) (absolute) | 0 | 0 | 0.00e+00 | 1.0e-09 | PASS |
| [partB3 rigid=True] finite-element reactions (Ku − F) vs double-integration reactions, worst relative to the largest (absolute) | 3.453613e-10 | 0 | 3.45e-10 | 1.0e-06 | PASS |
| [partB3 rigid=True] M(x) from statics with the JS reactions vs Python, max \|Δ\|/\|M\|max (absolute) | 1.3041051e-12 | 0 | 1.30e-12 | 1.0e-06 | PASS |
| [design] closed form y(x), JS vs Python, max \|Δ\|/\|y\|max (absolute) | 1.2912669e-15 | 0 | 1.29e-15 | 1.0e-12 | PASS |
| [design] closed form slope, JS vs Python, max \|Δ\|/\|θ\|max (absolute) | 8.493573e-16 | 0 | 8.49e-16 | 1.0e-12 | PASS |
| [design] closed form y(x) (JS) vs double integration of M/EI (Python), max \|Δ\|/\|y\|max (absolute) | 2.3727029e-14 | 0 | 2.37e-14 | 1.0e-07 | PASS |
| [design] finite elements y(x) (JS port of the C++) vs double integration (Python), max \|Δ\|/\|y\|max (absolute) | 1.3906842e-09 | 0 | 1.39e-09 | 1.0e-06 | PASS |
| [design] finite elements slope vs double integration, max \|Δ\|/\|θ\|max (absolute) | 1.4684909e-09 | 0 | 1.47e-09 | 1.0e-05 | PASS |
| [design] reaction RA, JS vs Python closed form (relative to the largest reaction) (absolute) | 0 | 0 | 0.00e+00 | 1.0e-12 | PASS |
| [design] reaction RB, JS vs Python closed form (relative to the largest reaction) (absolute) | 0 | 0 | 0.00e+00 | 1.0e-12 | PASS |
| [design] finite-element reactions (Ku − F) vs double-integration reactions, worst relative to the largest (absolute) | 6.2669537e-10 | 0 | 6.27e-10 | 1.0e-06 | PASS |
| [design] M(x) from statics with the JS reactions vs Python, max \|Δ\|/\|M\|max (absolute) | 8.8031843e-16 | 0 | 8.80e-16 | 1.0e-06 | PASS |
| [design L=3.05, aov=0.95] closed form y(x), JS vs Python, max \|Δ\|/\|y\|max (absolute) | 2.7121551e-15 | 0 | 2.71e-15 | 1.0e-12 | PASS |
| [design L=3.05, aov=0.95] closed form slope, JS vs Python, max \|Δ\|/\|θ\|max (absolute) | 2.2571083e-15 | 0 | 2.26e-15 | 1.0e-12 | PASS |
| [design L=3.05, aov=0.95] closed form y(x) (JS) vs double integration of M/EI (Python), max \|Δ\|/\|y\|max (absolute) | 1.6950969e-14 | 0 | 1.70e-14 | 1.0e-07 | PASS |
| [design L=3.05, aov=0.95] finite elements y(x) (JS port of the C++) vs double integration (Python), max \|Δ\|/\|y\|max (absolute) | 1.5605495e-09 | 0 | 1.56e-09 | 1.0e-06 | PASS |
| [design L=3.05, aov=0.95] finite elements slope vs double integration, max \|Δ\|/\|θ\|max (absolute) | 1.2808719e-09 | 0 | 1.28e-09 | 1.0e-05 | PASS |
| [design L=3.05, aov=0.95] reaction RA, JS vs Python closed form (relative to the largest reaction) (absolute) | 0 | 0 | 0.00e+00 | 1.0e-12 | PASS |
| [design L=3.05, aov=0.95] reaction RB, JS vs Python closed form (relative to the largest reaction) (absolute) | 0 | 0 | 0.00e+00 | 1.0e-12 | PASS |
| [design L=3.05, aov=0.95] finite-element reactions (Ku − F) vs double-integration reactions, worst relative to the largest (absolute) | 1.9404536e-10 | 0 | 1.94e-10 | 1.0e-06 | PASS |
| [design L=3.05, aov=0.95] M(x) from statics with the JS reactions vs Python, max \|Δ\|/\|M\|max (absolute) | 1.3289781e-15 | 0 | 1.33e-15 | 1.0e-06 | PASS |
| [F1] closed form y(x), JS vs Python, max \|Δ\|/\|y\|max (absolute) | 1.389134e-16 | 0 | 1.39e-16 | 1.0e-12 | PASS |
| [F1] closed form slope, JS vs Python, max \|Δ\|/\|θ\|max (absolute) | 0 | 0 | 0.00e+00 | 1.0e-12 | PASS |
| [F1] closed form y(x) (JS) vs double integration of M/EI (Python), max \|Δ\|/\|y\|max (absolute) | 2.3615279e-15 | 0 | 2.36e-15 | 1.0e-07 | PASS |
| [F1] finite elements y(x) (JS port of the C++) vs double integration (Python), max \|Δ\|/\|y\|max (absolute) | 3.8141841e-09 | 0 | 3.81e-09 | 1.0e-06 | PASS |
| [F1] finite elements slope vs double integration, max \|Δ\|/\|θ\|max (absolute) | 3.9526292e-09 | 0 | 3.95e-09 | 1.0e-05 | PASS |
| [F1] reaction RA, JS vs Python closed form (relative to the largest reaction) (absolute) | 0 | 0 | 0.00e+00 | 1.0e-12 | PASS |
| [F1] reaction RB, JS vs Python closed form (relative to the largest reaction) (absolute) | 0 | 0 | 0.00e+00 | 1.0e-12 | PASS |
| [F1] reaction MA, JS vs Python closed form (relative to the largest reaction) (absolute) | 0 | 0 | 0.00e+00 | 1.0e-12 | PASS |
| [F1] reaction MB, JS vs Python closed form (relative to the largest reaction) (absolute) | 0 | 0 | 0.00e+00 | 1.0e-12 | PASS |
| [F1] finite-element reactions (Ku − F) vs double-integration reactions, worst relative to the largest (absolute) | 3.2337766e-09 | 0 | 3.23e-09 | 1.0e-06 | PASS |
| [F1] M(x) from statics with the JS reactions vs Python, max \|Δ\|/\|M\|max (absolute) | 3.5527137e-18 | 0 | 3.55e-18 | 1.0e-06 | PASS |
| [F2] closed form y(x), JS vs Python, max \|Δ\|/\|y\|max (absolute) | 1.8521787e-16 | 0 | 1.85e-16 | 1.0e-12 | PASS |
| [F2] closed form slope, JS vs Python, max \|Δ\|/\|θ\|max (absolute) | 0 | 0 | 0.00e+00 | 1.0e-12 | PASS |
| [F2] closed form y(x) (JS) vs double integration of M/EI (Python), max \|Δ\|/\|y\|max (absolute) | 4.8156646e-15 | 0 | 4.82e-15 | 1.0e-07 | PASS |
| [F2] finite elements y(x) (JS port of the C++) vs double integration (Python), max \|Δ\|/\|y\|max (absolute) | 3.6876217e-09 | 0 | 3.69e-09 | 1.0e-06 | PASS |
| [F2] finite elements slope vs double integration, max \|Δ\|/\|θ\|max (absolute) | 4.341818e-09 | 0 | 4.34e-09 | 1.0e-05 | PASS |
| [F2] reaction RA, JS vs Python closed form (relative to the largest reaction) (absolute) | 0 | 0 | 0.00e+00 | 1.0e-12 | PASS |
| [F2] reaction RB, JS vs Python closed form (relative to the largest reaction) (absolute) | 0 | 0 | 0.00e+00 | 1.0e-12 | PASS |
| [F2] reaction MA, JS vs Python closed form (relative to the largest reaction) (absolute) | 0 | 0 | 0.00e+00 | 1.0e-12 | PASS |
| [F2] reaction MB, JS vs Python closed form (relative to the largest reaction) (absolute) | 0 | 0 | 0.00e+00 | 1.0e-12 | PASS |
| [F2] finite-element reactions (Ku − F) vs double-integration reactions, worst relative to the largest (absolute) | 2.2674394e-09 | 0 | 2.27e-09 | 1.0e-06 | PASS |
| [F2] M(x) from statics with the JS reactions vs Python, max \|Δ\|/\|M\|max (absolute) | 1.1368684e-16 | 0 | 1.14e-16 | 1.0e-06 | PASS |
| [F3] closed form y(x), JS vs Python, max \|Δ\|/\|y\|max (absolute) | 1.8521787e-16 | 0 | 1.85e-16 | 1.0e-12 | PASS |
| [F3] closed form slope, JS vs Python, max \|Δ\|/\|θ\|max (absolute) | 0 | 0 | 0.00e+00 | 1.0e-12 | PASS |
| [F3] closed form y(x) (JS) vs double integration of M/EI (Python), max \|Δ\|/\|y\|max (absolute) | 1.0742637e-13 | 0 | 1.07e-13 | 1.0e-07 | PASS |
| [F3] finite elements y(x) (JS port of the C++) vs double integration (Python), max \|Δ\|/\|y\|max (absolute) | 3.9438113e-09 | 0 | 3.94e-09 | 1.0e-06 | PASS |
| [F3] finite elements slope vs double integration, max \|Δ\|/\|θ\|max (absolute) | 3.0247614e-09 | 0 | 3.02e-09 | 1.0e-05 | PASS |
| [F3] reaction RA, JS vs Python closed form (relative to the largest reaction) (absolute) | 0 | 0 | 0.00e+00 | 1.0e-12 | PASS |
| [F3] reaction RB, JS vs Python closed form (relative to the largest reaction) (absolute) | 0 | 0 | 0.00e+00 | 1.0e-12 | PASS |
| [F3] reaction MA, JS vs Python closed form (relative to the largest reaction) (absolute) | 0 | 0 | 0.00e+00 | 1.0e-12 | PASS |
| [F3] reaction MB, JS vs Python closed form (relative to the largest reaction) (absolute) | 0 | 0 | 0.00e+00 | 1.0e-12 | PASS |
| [F3] finite-element reactions (Ku − F) vs double-integration reactions, worst relative to the largest (absolute) | 5.2444352e-09 | 0 | 5.24e-09 | 1.0e-06 | PASS |
| [F3] M(x) from statics with the JS reactions vs Python, max \|Δ\|/\|M\|max (absolute) | 0 | 0 | 0.00e+00 | 1.0e-06 | PASS |
| [F4] closed form y(x), JS vs Python, max \|Δ\|/\|y\|max (absolute) | 0 | 0 | 0.00e+00 | 1.0e-12 | PASS |
| [F4] closed form slope, JS vs Python, max \|Δ\|/\|θ\|max (absolute) | 1.481743e-16 | 0 | 1.48e-16 | 1.0e-12 | PASS |
| [F4] closed form y(x) (JS) vs double integration of M/EI (Python), max \|Δ\|/\|y\|max (absolute) | 1.620039e-14 | 0 | 1.62e-14 | 1.0e-07 | PASS |
| [F4] finite elements y(x) (JS port of the C++) vs double integration (Python), max \|Δ\|/\|y\|max (absolute) | 5.1421723e-10 | 0 | 5.14e-10 | 1.0e-06 | PASS |
| [F4] finite elements slope vs double integration, max \|Δ\|/\|θ\|max (absolute) | 9.549653e-10 | 0 | 9.55e-10 | 1.0e-05 | PASS |
| [F4] reaction RA, JS vs Python closed form (relative to the largest reaction) (absolute) | 0 | 0 | 0.00e+00 | 1.0e-12 | PASS |
| [F4] reaction RB, JS vs Python closed form (relative to the largest reaction) (absolute) | 0 | 0 | 0.00e+00 | 1.0e-12 | PASS |
| [F4] finite-element reactions (Ku − F) vs double-integration reactions, worst relative to the largest (absolute) | 3.8444996e-09 | 0 | 3.84e-09 | 1.0e-06 | PASS |
| [F4] M(x) from statics with the JS reactions vs Python, max \|Δ\|/\|M\|max (absolute) | 2.4253192e-16 | 0 | 2.43e-16 | 1.0e-06 | PASS |
| [F5] closed form y(x), JS vs Python, max \|Δ\|/\|y\|max (absolute) | 0 | 0 | 0.00e+00 | 1.0e-12 | PASS |
| [F5] closed form slope, JS vs Python, max \|Δ\|/\|θ\|max (absolute) | 1.6429223e-16 | 0 | 1.64e-16 | 1.0e-12 | PASS |
| [F5] closed form y(x) (JS) vs double integration of M/EI (Python), max \|Δ\|/\|y\|max (absolute) | 1.1661609e-14 | 0 | 1.17e-14 | 1.0e-07 | PASS |
| [F5] finite elements y(x) (JS port of the C++) vs double integration (Python), max \|Δ\|/\|y\|max (absolute) | 8.2947762e-10 | 0 | 8.29e-10 | 1.0e-06 | PASS |
| [F5] finite elements slope vs double integration, max \|Δ\|/\|θ\|max (absolute) | 1.165557e-09 | 0 | 1.17e-09 | 1.0e-05 | PASS |
| [F5] reaction RA, JS vs Python closed form (relative to the largest reaction) (absolute) | 0 | 0 | 0.00e+00 | 1.0e-12 | PASS |
| [F5] reaction RB, JS vs Python closed form (relative to the largest reaction) (absolute) | 0 | 0 | 0.00e+00 | 1.0e-12 | PASS |
| [F5] finite-element reactions (Ku − F) vs double-integration reactions, worst relative to the largest (absolute) | 2.6715653e-09 | 0 | 2.67e-09 | 1.0e-06 | PASS |
| [F5] M(x) from statics with the JS reactions vs Python, max \|Δ\|/\|M\|max (absolute) | 5.7745695e-16 | 0 | 5.77e-16 | 1.0e-06 | PASS |
| [F6] closed form y(x), JS vs Python, max \|Δ\|/\|y\|max (absolute) | 1.2292979e-15 | 0 | 1.23e-15 | 1.0e-12 | PASS |
| [F6] closed form slope, JS vs Python, max \|Δ\|/\|θ\|max (absolute) | 1.0975874e-15 | 0 | 1.10e-15 | 1.0e-12 | PASS |
| [F6] closed form y(x) (JS) vs double integration of M/EI (Python), max \|Δ\|/\|y\|max (absolute) | 8.0782431e-15 | 0 | 8.08e-15 | 1.0e-07 | PASS |
| [F6] finite elements y(x) (JS port of the C++) vs double integration (Python), max \|Δ\|/\|y\|max (absolute) | 5.3766492e-10 | 0 | 5.38e-10 | 1.0e-06 | PASS |
| [F6] finite elements slope vs double integration, max \|Δ\|/\|θ\|max (absolute) | 9.3551785e-10 | 0 | 9.36e-10 | 1.0e-05 | PASS |
| [F6] reaction RA, JS vs Python closed form (relative to the largest reaction) (absolute) | 0 | 0 | 0.00e+00 | 1.0e-12 | PASS |
| [F6] reaction RB, JS vs Python closed form (relative to the largest reaction) (absolute) | 0 | 0 | 0.00e+00 | 1.0e-12 | PASS |
| [F6] finite-element reactions (Ku − F) vs double-integration reactions, worst relative to the largest (absolute) | 2.5116735e-09 | 0 | 2.51e-09 | 1.0e-06 | PASS |
| [F6] M(x) from statics with the JS reactions vs Python, max \|Δ\|/\|M\|max (absolute) | 5.3895982e-16 | 0 | 5.39e-16 | 1.0e-06 | PASS |
| [F7] closed form y(x), JS vs Python, max \|Δ\|/\|y\|max (absolute) | 0 | 0 | 0.00e+00 | 1.0e-12 | PASS |
| [F7] closed form slope, JS vs Python, max \|Δ\|/\|θ\|max (absolute) | 2.4695716e-16 | 0 | 2.47e-16 | 1.0e-12 | PASS |
| [F7] closed form y(x) (JS) vs double integration of M/EI (Python), max \|Δ\|/\|y\|max (absolute) | 7.057924e-15 | 0 | 7.06e-15 | 1.0e-07 | PASS |
| [F7] finite elements y(x) (JS port of the C++) vs double integration (Python), max \|Δ\|/\|y\|max (absolute) | 1.1010755e-09 | 0 | 1.10e-09 | 1.0e-06 | PASS |
| [F7] finite elements slope vs double integration, max \|Δ\|/\|θ\|max (absolute) | 1.0138967e-09 | 0 | 1.01e-09 | 1.0e-05 | PASS |
| [F7] reaction RA, JS vs Python closed form (relative to the largest reaction) (absolute) | 0 | 0 | 0.00e+00 | 1.0e-12 | PASS |
| [F7] reaction RB, JS vs Python closed form (relative to the largest reaction) (absolute) | 0 | 0 | 0.00e+00 | 1.0e-12 | PASS |
| [F7] finite-element reactions (Ku − F) vs double-integration reactions, worst relative to the largest (absolute) | 8.6128712e-09 | 0 | 8.61e-09 | 1.0e-06 | PASS |
| [F7] M(x) from statics with the JS reactions vs Python, max \|Δ\|/\|M\|max (absolute) | 0 | 0 | 0.00e+00 | 1.0e-06 | PASS |
| [fixedw] closed form y(x), JS vs Python, max \|Δ\|/\|y\|max (absolute) | 3.5122796e-14 | 0 | 3.51e-14 | 1.0e-09 | PASS |
| [fixedw] closed form slope, JS vs Python, max \|Δ\|/\|θ\|max (absolute) | 2.1723084e-14 | 0 | 2.17e-14 | 1.0e-09 | PASS |
| [fixedw] closed form y(x) (JS) vs double integration of M/EI (Python), max \|Δ\|/\|y\|max (absolute) | 2.6403723e-10 | 0 | 2.64e-10 | 1.0e-07 | PASS |
| [fixedw] finite elements y(x) (JS port of the C++) vs double integration (Python), max \|Δ\|/\|y\|max (absolute) | 3.1550793e-10 | 0 | 3.16e-10 | 1.0e-06 | PASS |
| [fixedw] finite elements slope vs double integration, max \|Δ\|/\|θ\|max (absolute) | 8.7878272e-10 | 0 | 8.79e-10 | 1.0e-05 | PASS |
| [fixedw] reaction RA, JS vs Python closed form (relative to the largest reaction) (absolute) | -6.063298e-16 | 0 | 6.06e-16 | 1.0e-09 | PASS |
| [fixedw] reaction RB, JS vs Python closed form (relative to the largest reaction) (absolute) | 6.063298e-16 | 0 | 6.06e-16 | 1.0e-09 | PASS |
| [fixedw] reaction MA, JS vs Python closed form (relative to the largest reaction) (absolute) | -1.9200444e-15 | 0 | 1.92e-15 | 1.0e-09 | PASS |
| [fixedw] reaction MB, JS vs Python closed form (relative to the largest reaction) (absolute) | -1.0105497e-16 | 0 | 1.01e-16 | 1.0e-09 | PASS |
| [fixedw] finite-element reactions (Ku − F) vs double-integration reactions, worst relative to the largest (absolute) | 4.0245727e-10 | 0 | 4.02e-10 | 1.0e-06 | PASS |
| [fixedw] M(x) from statics with the JS reactions vs Python, max \|Δ\|/\|M\|max (absolute) | 3.0027149e-10 | 0 | 3.00e-10 | 1.0e-06 | PASS |
| [fixedw rigid=False, k=200000, P1=4000, a1=1.1, w=1500] closed form y(x), JS vs Python, max \|Δ\|/\|y\|max (absolute) | 5.1365935e-11 | 0 | 5.14e-11 | 1.0e-09 | PASS |
| [fixedw rigid=False, k=200000, P1=4000, a1=1.1, w=1500] closed form slope, JS vs Python, max \|Δ\|/\|θ\|max (absolute) | 1.9555627e-11 | 0 | 1.96e-11 | 1.0e-09 | PASS |
| [fixedw rigid=False, k=200000, P1=4000, a1=1.1, w=1500] closed form y(x) (JS) vs double integration of M/EI (Python), max \|Δ\|/\|y\|max (absolute) | 4.4885059e-11 | 0 | 4.49e-11 | 1.0e-07 | PASS |
| [fixedw rigid=False, k=200000, P1=4000, a1=1.1, w=1500] finite elements y(x) (JS port of the C++) vs double integration (Python), max \|Δ\|/\|y\|max (absolute) | 1.7636321e-09 | 0 | 1.76e-09 | 1.0e-06 | PASS |
| [fixedw rigid=False, k=200000, P1=4000, a1=1.1, w=1500] finite elements slope vs double integration, max \|Δ\|/\|θ\|max (absolute) | 1.5476784e-09 | 0 | 1.55e-09 | 1.0e-05 | PASS |
| [fixedw rigid=False, k=200000, P1=4000, a1=1.1, w=1500] reaction RA, JS vs Python closed form (relative to the largest reaction) (absolute) | -2.7396745e-12 | 0 | 2.74e-12 | 1.0e-09 | PASS |
| [fixedw rigid=False, k=200000, P1=4000, a1=1.1, w=1500] reaction RB, JS vs Python closed form (relative to the largest reaction) (absolute) | 2.7396745e-12 | 0 | 2.74e-12 | 1.0e-09 | PASS |
| [fixedw rigid=False, k=200000, P1=4000, a1=1.1, w=1500] reaction MA, JS vs Python closed form (relative to the largest reaction) (absolute) | -1.6962286e-12 | 0 | 1.70e-12 | 1.0e-09 | PASS |
| [fixedw rigid=False, k=200000, P1=4000, a1=1.1, w=1500] reaction MB, JS vs Python closed form (relative to the largest reaction) (absolute) | -6.5227948e-12 | 0 | 6.52e-12 | 1.0e-09 | PASS |
| [fixedw rigid=False, k=200000, P1=4000, a1=1.1, w=1500] finite-element reactions (Ku − F) vs double-integration reactions, worst relative to the largest (absolute) | 1.9242568e-09 | 0 | 1.92e-09 | 1.0e-06 | PASS |
| [fixedw rigid=False, k=200000, P1=4000, a1=1.1, w=1500] M(x) from statics with the JS reactions vs Python, max \|Δ\|/\|M\|max (absolute) | 3.5843879e-11 | 0 | 3.58e-11 | 1.0e-06 | PASS |
| [partB2 w=300, P2=20, a2=0.6, C0=3] closed form y(x), JS vs Python, max \|Δ\|/\|y\|max (absolute) | 4.5893328e-15 | 0 | 4.59e-15 | 1.0e-09 | PASS |
| [partB2 w=300, P2=20, a2=0.6, C0=3] closed form slope, JS vs Python, max \|Δ\|/\|θ\|max (absolute) | 1.6133449e-15 | 0 | 1.61e-15 | 1.0e-09 | PASS |
| [partB2 w=300, P2=20, a2=0.6, C0=3] closed form y(x) (JS) vs double integration of M/EI (Python), max \|Δ\|/\|y\|max (absolute) | 3.4403288e-11 | 0 | 3.44e-11 | 1.0e-07 | PASS |
| [partB2 w=300, P2=20, a2=0.6, C0=3] finite elements y(x) (JS port of the C++) vs double integration (Python), max \|Δ\|/\|y\|max (absolute) | 9.6684765e-11 | 0 | 9.67e-11 | 1.0e-06 | PASS |
| [partB2 w=300, P2=20, a2=0.6, C0=3] finite elements slope vs double integration, max \|Δ\|/\|θ\|max (absolute) | 1.6453778e-10 | 0 | 1.65e-10 | 1.0e-05 | PASS |
| [partB2 w=300, P2=20, a2=0.6, C0=3] reaction RA, JS vs Python closed form (relative to the largest reaction) (absolute) | 0 | 0 | 0.00e+00 | 1.0e-09 | PASS |
| [partB2 w=300, P2=20, a2=0.6, C0=3] reaction RB, JS vs Python closed form (relative to the largest reaction) (absolute) | 8.5982576e-17 | 0 | 8.60e-17 | 1.0e-09 | PASS |
| [partB2 w=300, P2=20, a2=0.6, C0=3] reaction MA, JS vs Python closed form (relative to the largest reaction) (absolute) | 0 | 0 | 0.00e+00 | 1.0e-09 | PASS |
| [partB2 w=300, P2=20, a2=0.6, C0=3] reaction MB, JS vs Python closed form (relative to the largest reaction) (absolute) | 0 | 0 | 0.00e+00 | 1.0e-09 | PASS |
| [partB2 w=300, P2=20, a2=0.6, C0=3] finite-element reactions (Ku − F) vs double-integration reactions, worst relative to the largest (absolute) | 2.0211116e-10 | 0 | 2.02e-10 | 1.0e-06 | PASS |
| [partB2 w=300, P2=20, a2=0.6, C0=3] M(x) from statics with the JS reactions vs Python, max \|Δ\|/\|M\|max (absolute) | 6.9455733e-12 | 0 | 6.95e-12 | 1.0e-06 | PASS |
| [F5 aov=0.8, P2=2000, a2=3.6, C0=-1500, w=800] closed form y(x), JS vs Python, max \|Δ\|/\|y\|max (absolute) | 5.2619651e-16 | 0 | 5.26e-16 | 1.0e-12 | PASS |
| [F5 aov=0.8, P2=2000, a2=3.6, C0=-1500, w=800] closed form slope, JS vs Python, max \|Δ\|/\|θ\|max (absolute) | 1.2604142e-15 | 0 | 1.26e-15 | 1.0e-12 | PASS |
| [F5 aov=0.8, P2=2000, a2=3.6, C0=-1500, w=800] closed form y(x) (JS) vs double integration of M/EI (Python), max \|Δ\|/\|y\|max (absolute) | 4.5474154e-09 | 0 | 4.55e-09 | 1.0e-07 | PASS |
| [F5 aov=0.8, P2=2000, a2=3.6, C0=-1500, w=800] finite elements y(x) (JS port of the C++) vs double integration (Python), max \|Δ\|/\|y\|max (absolute) | 3.927131e-09 | 0 | 3.93e-09 | 1.0e-06 | PASS |
| [F5 aov=0.8, P2=2000, a2=3.6, C0=-1500, w=800] finite elements slope vs double integration, max \|Δ\|/\|θ\|max (absolute) | 5.3534974e-09 | 0 | 5.35e-09 | 1.0e-05 | PASS |
| [F5 aov=0.8, P2=2000, a2=3.6, C0=-1500, w=800] reaction RA, JS vs Python closed form (relative to the largest reaction) (absolute) | 0 | 0 | 0.00e+00 | 1.0e-12 | PASS |
| [F5 aov=0.8, P2=2000, a2=3.6, C0=-1500, w=800] reaction RB, JS vs Python closed form (relative to the largest reaction) (absolute) | 0 | 0 | 0.00e+00 | 1.0e-12 | PASS |
| [F5 aov=0.8, P2=2000, a2=3.6, C0=-1500, w=800] finite-element reactions (Ku − F) vs double-integration reactions, worst relative to the largest (absolute) | 3.07781e-10 | 0 | 3.08e-10 | 1.0e-06 | PASS |
| [F5 aov=0.8, P2=2000, a2=3.6, C0=-1500, w=800] M(x) from statics with the JS reactions vs Python, max \|Δ\|/\|M\|max (absolute) | 4.7850681e-16 | 0 | 4.79e-16 | 1.0e-06 | PASS |
| [partB1 w=120, C0=-2, P2=15, a2=0.2] closed form y(x), JS vs Python, max \|Δ\|/\|y\|max (absolute) | 2.5144231e-16 | 0 | 2.51e-16 | 1.0e-12 | PASS |
| [partB1 w=120, C0=-2, P2=15, a2=0.2] closed form slope, JS vs Python, max \|Δ\|/\|θ\|max (absolute) | 6.4219996e-17 | 0 | 6.42e-17 | 1.0e-12 | PASS |
| [partB1 w=120, C0=-2, P2=15, a2=0.2] closed form y(x) (JS) vs double integration of M/EI (Python), max \|Δ\|/\|y\|max (absolute) | 1.0190454e-11 | 0 | 1.02e-11 | 1.0e-07 | PASS |
| [partB1 w=120, C0=-2, P2=15, a2=0.2] finite elements y(x) (JS port of the C++) vs double integration (Python), max \|Δ\|/\|y\|max (absolute) | 1.2821509e-08 | 0 | 1.28e-08 | 1.0e-06 | PASS |
| [partB1 w=120, C0=-2, P2=15, a2=0.2] finite elements slope vs double integration, max \|Δ\|/\|θ\|max (absolute) | 1.2795765e-08 | 0 | 1.28e-08 | 1.0e-05 | PASS |
| [partB1 w=120, C0=-2, P2=15, a2=0.2] reaction RA, JS vs Python closed form (relative to the largest reaction) (absolute) | 0 | 0 | 0.00e+00 | 1.0e-12 | PASS |
| [partB1 w=120, C0=-2, P2=15, a2=0.2] reaction RB, JS vs Python closed form (relative to the largest reaction) (absolute) | 0 | 0 | 0.00e+00 | 1.0e-12 | PASS |
| [partB1 w=120, C0=-2, P2=15, a2=0.2] reaction MA, JS vs Python closed form (relative to the largest reaction) (absolute) | 6.5303245e-17 | 0 | 6.53e-17 | 1.0e-12 | PASS |
| [partB1 w=120, C0=-2, P2=15, a2=0.2] reaction MB, JS vs Python closed form (relative to the largest reaction) (absolute) | 0 | 0 | 0.00e+00 | 1.0e-12 | PASS |
| [partB1 w=120, C0=-2, P2=15, a2=0.2] finite-element reactions (Ku − F) vs double-integration reactions, worst relative to the largest (absolute) | 7.4626041e-09 | 0 | 7.46e-09 | 1.0e-06 | PASS |
| [partB1 w=120, C0=-2, P2=15, a2=0.2] M(x) from statics with the JS reactions vs Python, max \|Δ\|/\|M\|max (absolute) | 3.4438322e-16 | 0 | 3.44e-16 | 1.0e-06 | PASS |
| elastica α = 0.05: tip angle, Carlson R_F (JS) vs scipy ellipkinc + brentq | 0.024994274 | 0.024994274 | 1.76e-14 | 1.0e-10 | PASS |
| elastica α = 0.05: δ_v/L, Carlson R_D (JS) vs scipy ellipeinc | 0.016661907 | 0.016661907 | 4.80e-13 | 1.0e-10 | PASS |
| elastica α = 0.05: x_tip/L, JS vs scipy | 0.99983341 | 0.99983341 | 8.88e-15 | 1.0e-10 | PASS |
| elastica α = 0.05: δ_v/L, RK4 shooting N = 400 (JS) vs collocation BVP (scipy) | 0.016661907 | 0.016661907 | 6.25e-16 | 1.0e-08 | PASS |
| elastica α = 0.05: x_tip/L, RK4 shooting vs BVP | 0.99983341 | 0.99983341 | 7.77e-16 | 1.0e-08 | PASS |
| elastica α = 0.05 with self-weight β = 0.1154: δ_v/L, RK4 shooting vs BVP | 0.03106459 | 0.03106459 | 1.27e-14 | 1.0e-07 | PASS |
| elastica α = 0.05 with self-weight: tip angle, RK4 shooting vs BVP | 0.044203087 | 0.044203087 | 8.48e-15 | 1.0e-07 | PASS |
| elastica α = 0.3: tip angle, Carlson R_F (JS) vs scipy ellipkinc + brentq | 0.14878373 | 0.14878373 | 7.46e-16 | 1.0e-10 | PASS |
| elastica α = 0.3: δ_v/L, Carlson R_D (JS) vs scipy ellipeinc | 0.098990751 | 0.098990751 | 1.68e-14 | 1.0e-10 | PASS |
| elastica α = 0.3: x_tip/L, JS vs scipy | 0.99410062 | 0.99410062 | 3.35e-16 | 1.0e-10 | PASS |
| elastica α = 0.3: δ_v/L, RK4 shooting N = 400 (JS) vs collocation BVP (scipy) | 0.098990751 | 0.098990751 | 1.33e-14 | 1.0e-08 | PASS |
| elastica α = 0.3: x_tip/L, RK4 shooting vs BVP | 0.99410062 | 0.99410062 | 2.31e-14 | 1.0e-08 | PASS |
| elastica α = 0.3 with self-weight β = 0.1154: δ_v/L, RK4 shooting vs BVP | 0.1129755 | 0.1129755 | 1.99e-14 | 1.0e-07 | PASS |
| elastica α = 0.3 with self-weight: tip angle, RK4 shooting vs BVP | 0.16751854 | 0.16751854 | 3.71e-14 | 1.0e-07 | PASS |
| elastica α = 1: tip angle, Carlson R_F (JS) vs scipy ellipkinc + brentq | 0.46135195 | 0.46135195 | 9.63e-16 | 1.0e-10 | PASS |
| elastica α = 1: δ_v/L, Carlson R_D (JS) vs scipy ellipeinc | 0.30172077 | 0.30172077 | 1.47e-15 | 1.0e-10 | PASS |
| elastica α = 1: x_tip/L, JS vs scipy | 0.94356676 | 0.94356676 | 3.53e-16 | 1.0e-10 | PASS |
| elastica α = 1: δ_v/L, RK4 shooting N = 400 (JS) vs collocation BVP (scipy) | 0.30172077 | 0.30172077 | 8.37e-14 | 1.0e-08 | PASS |
| elastica α = 1: x_tip/L, RK4 shooting vs BVP | 0.94356676 | 0.94356676 | 2.36e-13 | 1.0e-08 | PASS |
| elastica α = 1 with self-weight β = 0.1154: δ_v/L, RK4 shooting vs BVP | 0.31272709 | 0.31272709 | 7.56e-14 | 1.0e-07 | PASS |
| elastica α = 1 with self-weight: tip angle, RK4 shooting vs BVP | 0.47662 | 0.47662 | 1.55e-13 | 1.0e-07 | PASS |
| elastica α = 2: tip angle, Carlson R_F (JS) vs scipy ellipkinc + brentq | 0.78174983 | 0.78174983 | 4.26e-16 | 1.0e-10 | PASS |
| elastica α = 2: δ_v/L, Carlson R_D (JS) vs scipy ellipeinc | 0.49345748 | 0.49345748 | 2.25e-16 | 1.0e-10 | PASS |
| elastica α = 2: x_tip/L, JS vs scipy | 0.83935828 | 0.83935828 | 1.32e-16 | 1.0e-10 | PASS |
| elastica α = 2: δ_v/L, RK4 shooting N = 400 (JS) vs collocation BVP (scipy) | 0.49345748 | 0.49345748 | 7.29e-14 | 1.0e-08 | PASS |
| elastica α = 2: x_tip/L, RK4 shooting vs BVP | 0.83935828 | 0.83935828 | 1.07e-12 | 1.0e-08 | PASS |
| elastica α = 2 with self-weight β = 0.1154: δ_v/L, RK4 shooting vs BVP | 0.5001882 | 0.5001882 | 5.13e-14 | 1.0e-07 | PASS |
| elastica α = 2 with self-weight: tip angle, RK4 shooting vs BVP | 0.79171199 | 0.79171199 | 6.90e-13 | 1.0e-07 | PASS |
| elastica α = 3.641: tip angle, Carlson R_F (JS) vs scipy ellipkinc + brentq | 1.0785253 | 1.0785253 | 2.06e-16 | 1.0e-10 | PASS |
| elastica α = 3.641: δ_v/L, Carlson R_D (JS) vs scipy ellipeinc | 0.64939694 | 0.64939694 | 3.42e-16 | 1.0e-10 | PASS |
| elastica α = 3.641: x_tip/L, JS vs scipy | 0.69575627 | 0.69575627 | 1.60e-16 | 1.0e-10 | PASS |
| elastica α = 3.641: δ_v/L, RK4 shooting N = 400 (JS) vs collocation BVP (scipy) | 0.64939694 | 0.64939694 | 1.82e-13 | 1.0e-08 | PASS |
| elastica α = 3.641: x_tip/L, RK4 shooting vs BVP | 0.69575627 | 0.69575627 | 3.40e-12 | 1.0e-08 | PASS |
| elastica α = 3.641 with self-weight β = 0.1154: δ_v/L, RK4 shooting vs BVP | 0.6526971 | 0.6526971 | 2.08e-13 | 1.0e-07 | PASS |
| elastica α = 3.641 with self-weight: tip angle, RK4 shooting vs BVP | 1.0837131 | 1.0837131 | 2.07e-12 | 1.0e-07 | PASS |
| elastica α = 5: tip angle, Carlson R_F (JS) vs scipy ellipkinc + brentq | 1.2153681 | 1.2153681 | 3.65e-16 | 1.0e-10 | PASS |
| elastica α = 5: δ_v/L, Carlson R_D (JS) vs scipy ellipeinc | 0.71379152 | 0.71379152 | 1.24e-15 | 1.0e-10 | PASS |
| elastica α = 5: x_tip/L, JS vs scipy | 0.61237164 | 0.61237164 | 0.00e+00 | 1.0e-10 | PASS |
| elastica α = 5: δ_v/L, RK4 shooting N = 400 (JS) vs collocation BVP (scipy) | 0.71379152 | 0.71379152 | 4.34e-13 | 1.0e-08 | PASS |
| elastica α = 5: x_tip/L, RK4 shooting vs BVP | 0.61237164 | 0.61237164 | 6.11e-12 | 1.0e-08 | PASS |
| elastica α = 5 with self-weight β = 0.1154: δ_v/L, RK4 shooting vs BVP | 0.71590315 | 0.71590315 | 4.56e-13 | 1.0e-07 | PASS |
| elastica α = 5 with self-weight: tip angle, RK4 shooting vs BVP | 1.2186897 | 1.2186897 | 3.36e-12 | 1.0e-07 | PASS |
| elastica α = 1: elastic curve from the elliptic parameterization (JS) vs the BVP at the same arc length, max distance / L (absolute) | 6.3488548e-14 | 0 | 6.35e-14 | 1.0e-07 | PASS |
| elastica α = 3.641: elastic curve from the elliptic parameterization (JS) vs the BVP at the same arc length, max distance / L (absolute) | 3.032511e-14 | 0 | 3.03e-14 | 1.0e-07 | PASS |
| α at which linear theory overstates δ_v by 5 %: JS bisection vs scipy brentq | 0.67563667 | 0.67563667 | 3.11e-14 | 1.0e-09 | PASS |
| handout Appendix E, 11 rows: every printed value vs scipy (largest error in the last printed digit) (absolute) | 4.7404302e-05 | 0 | 4.74e-05 | 5.0e-05 | PASS |
| closure Part A: E from six compliances vs truth 205 GPa, within 2u (absolute) | 205.00775 | 205 | 7.75e-03 | 9.9e-01 | PASS |
| closure Part A: EI vs truth (N·m²), within 2u (absolute) | 111.87071 | 111.86648 | 4.23e-03 | 5.4e-01 | PASS |
| closure Part A: reciprocity c13 − c31 (µm/N), within its limit (absolute) | 0.065553185 | 0 | 6.56e-02 | 2.4e-01 | PASS |
| closure Part B1: EI from two indicators vs truth (N·m²), within 2u (absolute) | 112.30667 | 111.86648 | 4.40e-01 | 1.0e+00 | PASS |
| closure Part B1: clamp stiffness k vs truth 4500 N·m/rad, within 2u (absolute) | 4366.3376 | 4500 | 1.34e+02 | 3.1e+02 | PASS |
| closure Part B2: R_B/P (load-cell gain included) vs truth model with the spring clamp, within 2u (absolute) | 0.33079594 | 0.33089783 | 1.02e-04 | 2.0e-03 | PASS |
| closure Part B2: rigid-clamp 5/16 is rejected by the data (\|r − 5/16\| > 2u) | True | True | 0.00e+00 | 0.0e+00 | PASS |
| closure Part B3: ΔR_B (N) vs truth (spring clamp, 0.502 mm, load-cell gain), within 2u (absolute) | -0.43 | -0.44447201 | 1.45e-02 | 2.1e-02 | PASS |
| closure Part C: strip EI from the large-deflection fit vs truth (N·m²), within 2u (absolute) | 0.10473042 | 0.10472315 | 7.26e-06 | 7.8e-04 | PASS |
| closure Part C: strip E (GPa) vs truth 203, within 2u (absolute) | 203.01408 | 203 | 1.41e-02 | 3.2e+00 | PASS |
| closure Part C: free length from the zero-load grid reading vs truth (m) | 0.25044258 | 0.2504 | 1.70e-04 | 5.0e-03 | PASS |
| closure Part C: χ² of the fit consistent with the reading noise (χ² = 18.1 for 21 degrees of freedom) | True | True | 0.00e+00 | 0.0e+00 | PASS |
| analysis α5 (scipy) vs the page's alpha5 (JS) | 0.67563667 | 0.67563667 | 3.11e-14 | 1.0e-09 | PASS |
| simulation Part C preset: β = wL³/EI with E = 203 GPa vs the analysis β | 0.11480111 | 0.11540389 | 5.22e-03 | 1.0e-02 | PASS |
| D1 reference design (I 102 × 64, L_s = 3.05 m): largest \|y\| on the span, page vs analysis (40 points vs 8000) — page deflections scaled by 68.9/68.46 | 6.4372157 | 6.4381661 | 1.48e-04 | 2.0e-03 | PASS |
| D1 reference design: tip deflection, page vs analysis — scaled by 68.9/68.46 | 4.3599988 | 4.3599988 | 6.52e-15 | 1.0e-09 | PASS |
| D1 reference design: roller reaction, page vs analysis | 7213.1148 | 7213.1148 | 0.00e+00 | 1.0e-12 | PASS |
| D1: the lightest feasible section is I 102 × 64; without an overhang it is I 152 × 102 | True | True | 0.00e+00 | 0.0e+00 | PASS |

288 of 288 passed.

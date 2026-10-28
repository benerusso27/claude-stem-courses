## Lab 7 model tests (exact page code, and the C++ reference)

| Test | Value | Reference | Rel. difference | Tolerance | Result |
|---|---:|---:|---:|---:|---|
| App. F 1: y_max = −PL³/3EI | -0.0062439024 | -0.0062439024 | 0.00e+0 | 1.0e-13 | PASS |
| App. F 1: slope at the end = −PL²/2EI | -0.0046829268 | -0.0046829268 | 0.00e+0 | 1.0e-13 | PASS |
| App. F 1: elastic curve y = P(x³ − 3Lx²)/6EI at x = 0.4L | -0.0012987317 | -0.0012987317 | 1.67e-16 | 1.0e-13 | PASS |
| App. F 2: y_max = −wL⁴/8EI | -0.0046829268 | -0.0046829268 | 0.00e+0 | 1.0e-13 | PASS |
| App. F 2: slope at the end = −wL³/6EI | -0.0031219512 | -0.0031219512 | 0.00e+0 | 1.0e-13 | PASS |
| App. F 3: y_max = −ML²/2EI (clockwise end couple) | -0.0046829268 | -0.0046829268 | 0.00e+0 | 1.0e-13 | PASS |
| App. F 3: slope at the end = −ML/EI | -0.0046829268 | -0.0046829268 | 0.00e+0 | 1.0e-13 | PASS |
| App. F 4: y_max = −PL³/48EI | -0.0032926829 | -0.0032926829 | 1.32e-16 | 1.0e-13 | PASS |
| App. F 4: slope at A = −PL²/16EI | -0.0032926829 | -0.0032926829 | 1.32e-16 | 1.0e-13 | PASS |
| App. F 5: y_max = −Pb(L² − b²)^{3/2}/(9√3 EIL) at x_m = √((L² − b²)/3) | -0.0026404099 | -0.0026404099 | 0.00e+0 | 1.0e-12 | PASS |
| App. F 5: slope is zero at x_m (absolute difference) | 0.0000000 | 0.0000000 | 0.00e+0 | 1.0e-13 | PASS |
| App. F 5: θ_A = −Pb(L² − b²)/6EIL | -0.0023970732 | -0.0023970732 | 0.00e+0 | 1.0e-13 | PASS |
| App. F 5: θ_B = +Pa(L² − a²)/6EIL | 0.0031346341 | 0.0031346341 | 0.00e+0 | 1.0e-13 | PASS |
| App. F 5: y under the load = −Pa²b²/3EIL | -0.0023233171 | -0.0023233171 | 0.00e+0 | 1.0e-13 | PASS |
| App. F 6: y_max = −5wL⁴/384EI | -0.0037042683 | -0.0037042683 | 0.00e+0 | 1.0e-13 | PASS |
| App. F 6: slope at A = −wL³/24EI | -0.0039512195 | -0.0039512195 | 0.00e+0 | 1.0e-13 | PASS |
| App. F 7: y_max = ML²/(9√3 EI) at x = L/√3 (bows upward) | 0.0020277668 | 0.0020277668 | 2.14e-16 | 1.0e-12 | PASS |
| App. F 7: θ_A = +ML/6EI | 0.0017560976 | 0.0017560976 | 0.00e+0 | 1.0e-13 | PASS |
| App. F 7: θ_B = −ML/3EI | -0.0035121951 | -0.0035121951 | 0.00e+0 | 1.0e-13 | PASS |
| fixed at both ends, uniform load: y_max = −wL⁴/384EI | -0.00074085366 | -0.00074085366 | 8.55e-12 | 1.0e-11 | PASS |
| fixed at both ends: end moments wL²/12 | 2250.0000 | 2250.0000 | 3.00e-12 | 1.0e-11 | PASS |
| fixed at both ends, central load: y_max = −PL³/192EI | -0.00082317073 | -0.00082317073 | 3.59e-12 | 1.0e-11 | PASS |
| propped cantilever, central load, rigid clamp: R_B = 5P/16 (§9.2) | 12.258312 | 12.258312 | 4.35e-16 | 1.0e-12 | PASS |
| propped cantilever: wall moment 3PL/16 | 5.1484913 | 5.1484912 | 6.90e-16 | 1.0e-12 | PASS |
| propped cantilever, uniform load: R_B = 3wL/8 | 262.50000 | 262.50000 | 1.71e-14 | 1.0e-12 | PASS |
| propped cantilever with k → 0 becomes a simple span: R_B → P/2 | 19.613300 | 19.613300 | 7.88e-10 | 1.0e-6 | PASS |
| settlement Δ of the prop changes R_B by 3EIΔ/L³ (rigid clamp) | -0.48587510 | -0.48587510 | 5.71e-16 | 1.0e-10 | PASS |
| settlement with a flexible clamp: ΔR_B = Δ/(L³/3EI + L²/k) | -0.43842932 | -0.43842932 | 1.27e-16 | 1.0e-10 | PASS |
| cantilever with a flexible clamp: tip deflection PL³/3EI + PL²/k | 0.011183844 | 0.011183844 | 0.00e+0 | 1.0e-12 | PASS |
| [partA] elastic curve: FE vs closed form, max \|Δy\|/\|y\|max (absolute difference) | 1.1534153e-9 | 0.0000000 | 1.15e-9 | 1.0e-7 | PASS |
| [partA] slope: FE vs closed form, max \|Δθ\|/\|θ\|max (absolute difference) | 9.4097344e-10 | 0.0000000 | 9.41e-10 | 1.0e-7 | PASS |
| [partA] reaction at the left support: FE vs closed form (relative to the total load) (absolute difference) | -4.3271051e-10 | 0.0000000 | 4.33e-10 | 1.0e-7 | PASS |
| [partA] reaction at the right support (absolute difference) | -3.9147892e-10 | 0.0000000 | 3.91e-10 | 1.0e-7 | PASS |
| [partA] FE reactions satisfy ΣF = 0 and ΣM = 0 (relative) (absolute difference) | 9.1243846e-10 | 0.0000000 | 9.12e-10 | 1.0e-7 | PASS |
| [partAboth] elastic curve: FE vs closed form, max \|Δy\|/\|y\|max (absolute difference) | 1.1798636e-9 | 0.0000000 | 1.18e-9 | 1.0e-7 | PASS |
| [partAboth] slope: FE vs closed form, max \|Δθ\|/\|θ\|max (absolute difference) | 1.0497393e-9 | 0.0000000 | 1.05e-9 | 1.0e-7 | PASS |
| [partAboth] reaction at the left support: FE vs closed form (relative to the total load) (absolute difference) | -4.3842204e-10 | 0.0000000 | 4.38e-10 | 1.0e-7 | PASS |
| [partAboth] reaction at the right support (absolute difference) | -3.9516532e-10 | 0.0000000 | 3.95e-10 | 1.0e-7 | PASS |
| [partAboth] FE reactions satisfy ΣF = 0 and ΣM = 0 (relative) (absolute difference) | 9.2250937e-10 | 0.0000000 | 9.23e-10 | 1.0e-7 | PASS |
| [partB1] elastic curve: FE vs closed form, max \|Δy\|/\|y\|max (absolute difference) | 2.4213289e-9 | 0.0000000 | 2.42e-9 | 1.0e-7 | PASS |
| [partB1] slope: FE vs closed form, max \|Δθ\|/\|θ\|max (absolute difference) | 2.2554023e-9 | 0.0000000 | 2.26e-9 | 1.0e-7 | PASS |
| [partB1] reaction at the left support: FE vs closed form (relative to the total load) (absolute difference) | 4.5004753e-9 | 0.0000000 | 4.50e-9 | 1.0e-7 | PASS |
| [partB1] reaction couple at the left: FE vs closed form (relative to W·L) (absolute difference) | 2.8593238e-9 | 0.0000000 | 2.86e-9 | 1.0e-7 | PASS |
| [partB1] FE reactions satisfy ΣF = 0 and ΣM = 0 (relative) (absolute difference) | 5.3319800e-9 | 0.0000000 | 5.33e-9 | 1.0e-7 | PASS |
| [partB2] elastic curve: FE vs closed form, max \|Δy\|/\|y\|max (absolute difference) | 1.7909975e-10 | 0.0000000 | 1.79e-10 | 1.0e-7 | PASS |
| [partB2] slope: FE vs closed form, max \|Δθ\|/\|θ\|max (absolute difference) | 1.8072059e-10 | 0.0000000 | 1.81e-10 | 1.0e-7 | PASS |
| [partB2] reaction at the left support: FE vs closed form (relative to the total load) (absolute difference) | 2.1189621e-10 | 0.0000000 | 2.12e-10 | 1.0e-7 | PASS |
| [partB2] reaction at the right support (absolute difference) | 6.5264288e-11 | 0.0000000 | 6.53e-11 | 1.0e-7 | PASS |
| [partB2] reaction couple at the left: FE vs closed form (relative to W·L) (absolute difference) | 3.9213916e-11 | 0.0000000 | 3.92e-11 | 1.0e-7 | PASS |
| [partB2] FE reactions satisfy ΣF = 0 and ΣM = 0 (relative) (absolute difference) | 2.9619864e-10 | 0.0000000 | 2.96e-10 | 1.0e-7 | PASS |
| [partB3] elastic curve: FE vs closed form, max \|Δy\|/\|y\|max (absolute difference) | 1.7621206e-10 | 0.0000000 | 1.76e-10 | 1.0e-7 | PASS |
| [partB3] slope: FE vs closed form, max \|Δθ\|/\|θ\|max (absolute difference) | 2.4104239e-10 | 0.0000000 | 2.41e-10 | 1.0e-7 | PASS |
| [partB3] reaction at the left support: FE vs closed form (relative to the total load) (absolute difference) | 2.4296545e-10 | 0.0000000 | 2.43e-10 | 1.0e-7 | PASS |
| [partB3] reaction at the right support (absolute difference) | 1.3281134e-10 | 0.0000000 | 1.33e-10 | 1.0e-7 | PASS |
| [partB3] reaction couple at the left: FE vs closed form (relative to W·L) (absolute difference) | 4.5823490e-11 | 0.0000000 | 4.58e-11 | 1.0e-7 | PASS |
| [partB3] FE reactions satisfy ΣF = 0 and ΣM = 0 (relative) (absolute difference) | 4.1607522e-10 | 0.0000000 | 4.16e-10 | 1.0e-7 | PASS |
| [design] elastic curve: FE vs closed form, max \|Δy\|/\|y\|max (absolute difference) | 2.1305756e-9 | 0.0000000 | 2.13e-9 | 1.0e-7 | PASS |
| [design] slope: FE vs closed form, max \|Δθ\|/\|θ\|max (absolute difference) | 1.8976545e-10 | 0.0000000 | 1.90e-10 | 1.0e-7 | PASS |
| [design] reaction at the left support: FE vs closed form (relative to the total load) (absolute difference) | 5.4282760e-11 | 0.0000000 | 5.43e-11 | 1.0e-7 | PASS |
| [design] reaction at the right support (absolute difference) | 4.0810176e-11 | 0.0000000 | 4.08e-11 | 1.0e-7 | PASS |
| [design] FE reactions satisfy ΣF = 0 and ΣM = 0 (relative) (absolute difference) | 1.0157652e-10 | 0.0000000 | 1.02e-10 | 1.0e-7 | PASS |
| [F1] elastic curve: FE vs closed form, max \|Δy\|/\|y\|max (absolute difference) | 1.3792902e-9 | 0.0000000 | 1.38e-9 | 1.0e-7 | PASS |
| [F1] slope: FE vs closed form, max \|Δθ\|/\|θ\|max (absolute difference) | 1.1042637e-9 | 0.0000000 | 1.10e-9 | 1.0e-7 | PASS |
| [F1] reaction at the left support: FE vs closed form (relative to the total load) (absolute difference) | 6.9839880e-9 | 0.0000000 | 6.98e-9 | 1.0e-7 | PASS |
| [F1] reaction couple at the left: FE vs closed form (relative to W·L) (absolute difference) | 2.7514329e-9 | 0.0000000 | 2.75e-9 | 1.0e-7 | PASS |
| [F1] FE reactions satisfy ΣF = 0 and ΣM = 0 (relative) (absolute difference) | 7.5064287e-9 | 0.0000000 | 7.51e-9 | 1.0e-7 | PASS |
| [F1, clamp k = 5EI/L] elastic curve: FE vs closed form, max \|Δy\|/\|y\|max (absolute difference) | 1.1481503e-8 | 0.0000000 | 1.15e-8 | 1.0e-7 | PASS |
| [F1, clamp k = 5EI/L] slope: FE vs closed form, max \|Δθ\|/\|θ\|max (absolute difference) | 1.0171535e-8 | 0.0000000 | 1.02e-8 | 1.0e-7 | PASS |
| [F1, clamp k = 5EI/L] reaction at the left support: FE vs closed form (relative to the total load) (absolute difference) | 2.6769936e-8 | 0.0000000 | 2.68e-8 | 1.0e-7 | PASS |
| [F1, clamp k = 5EI/L] reaction couple at the left: FE vs closed form (relative to W·L) (absolute difference) | 1.4116266e-8 | 0.0000000 | 1.41e-8 | 1.0e-7 | PASS |
| [F1, clamp k = 5EI/L] FE reactions satisfy ΣF = 0 and ΣM = 0 (relative) (absolute difference) | 3.0263814e-8 | 0.0000000 | 3.03e-8 | 1.0e-7 | PASS |
| [F2] elastic curve: FE vs closed form, max \|Δy\|/\|y\|max (absolute difference) | 1.6407647e-9 | 0.0000000 | 1.64e-9 | 1.0e-7 | PASS |
| [F2] slope: FE vs closed form, max \|Δθ\|/\|θ\|max (absolute difference) | 1.4715989e-9 | 0.0000000 | 1.47e-9 | 1.0e-7 | PASS |
| [F2] reaction at the left support: FE vs closed form (relative to the total load) (absolute difference) | 3.0630617e-9 | 0.0000000 | 3.06e-9 | 1.0e-7 | PASS |
| [F2] reaction couple at the left: FE vs closed form (relative to W·L) (absolute difference) | 1.2133280e-9 | 0.0000000 | 1.21e-9 | 1.0e-7 | PASS |
| [F2] FE reactions satisfy ΣF = 0 and ΣM = 0 (relative) (absolute difference) | 3.2946187e-9 | 0.0000000 | 3.29e-9 | 1.0e-7 | PASS |
| [F2, clamp k = 5EI/L] elastic curve: FE vs closed form, max \|Δy\|/\|y\|max (absolute difference) | 1.2254012e-8 | 0.0000000 | 1.23e-8 | 1.0e-7 | PASS |
| [F2, clamp k = 5EI/L] slope: FE vs closed form, max \|Δθ\|/\|θ\|max (absolute difference) | 1.1981396e-8 | 0.0000000 | 1.20e-8 | 1.0e-7 | PASS |
| [F2, clamp k = 5EI/L] reaction at the left support: FE vs closed form (relative to the total load) (absolute difference) | 1.2315810e-8 | 0.0000000 | 1.23e-8 | 1.0e-7 | PASS |
| [F2, clamp k = 5EI/L] reaction couple at the left: FE vs closed form (relative to W·L) (absolute difference) | 6.3975424e-9 | 0.0000000 | 6.40e-9 | 1.0e-7 | PASS |
| [F2, clamp k = 5EI/L] FE reactions satisfy ΣF = 0 and ΣM = 0 (relative) (absolute difference) | 1.3878318e-8 | 0.0000000 | 1.39e-8 | 1.0e-7 | PASS |
| [F3] elastic curve: FE vs closed form, max \|Δy\|/\|y\|max (absolute difference) | 1.0258955e-9 | 0.0000000 | 1.03e-9 | 1.0e-7 | PASS |
| [F3] slope: FE vs closed form, max \|Δθ\|/\|θ\|max (absolute difference) | 6.1989162e-10 | 0.0000000 | 6.20e-10 | 1.0e-7 | PASS |
| [F3] reaction at the left support: FE vs closed form (relative to the total load) (absolute difference) | 8.0303289e-9 | 0.0000000 | 8.03e-9 | 1.0e-7 | PASS |
| [F3] reaction couple at the left: FE vs closed form (relative to W·L) (absolute difference) | 3.1300597e-9 | 0.0000000 | 3.13e-9 | 1.0e-7 | PASS |
| [F3] FE reactions satisfy ΣF = 0 and ΣM = 0 (relative) (absolute difference) | 8.6187851e-9 | 0.0000000 | 8.62e-9 | 1.0e-7 | PASS |
| [F3, clamp k = 5EI/L] elastic curve: FE vs closed form, max \|Δy\|/\|y\|max (absolute difference) | 1.0160123e-8 | 0.0000000 | 1.02e-8 | 1.0e-7 | PASS |
| [F3, clamp k = 5EI/L] slope: FE vs closed form, max \|Δθ\|/\|θ\|max (absolute difference) | 6.9324876e-9 | 0.0000000 | 6.93e-9 | 1.0e-7 | PASS |
| [F3, clamp k = 5EI/L] reaction at the left support: FE vs closed form (relative to the total load) (absolute difference) | 2.9943883e-8 | 0.0000000 | 2.99e-8 | 1.0e-7 | PASS |
| [F3, clamp k = 5EI/L] reaction couple at the left: FE vs closed form (relative to W·L) (absolute difference) | 1.6213497e-8 | 0.0000000 | 1.62e-8 | 1.0e-7 | PASS |
| [F3, clamp k = 5EI/L] FE reactions satisfy ΣF = 0 and ΣM = 0 (relative) (absolute difference) | 3.4051632e-8 | 0.0000000 | 3.41e-8 | 1.0e-7 | PASS |
| [F4] elastic curve: FE vs closed form, max \|Δy\|/\|y\|max (absolute difference) | 6.7784235e-10 | 0.0000000 | 6.78e-10 | 1.0e-7 | PASS |
| [F4] slope: FE vs closed form, max \|Δθ\|/\|θ\|max (absolute difference) | 8.0952781e-10 | 0.0000000 | 8.10e-10 | 1.0e-7 | PASS |
| [F4] reaction at the left support: FE vs closed form (relative to the total load) (absolute difference) | 6.8843365e-10 | 0.0000000 | 6.88e-10 | 1.0e-7 | PASS |
| [F4] reaction at the right support (absolute difference) | 2.8014183e-10 | 0.0000000 | 2.80e-10 | 1.0e-7 | PASS |
| [F4] FE reactions satisfy ΣF = 0 and ΣM = 0 (relative) (absolute difference) | 1.0082747e-9 | 0.0000000 | 1.01e-9 | 1.0e-7 | PASS |
| [F5] elastic curve: FE vs closed form, max \|Δy\|/\|y\|max (absolute difference) | 6.4219694e-10 | 0.0000000 | 6.42e-10 | 1.0e-7 | PASS |
| [F5] slope: FE vs closed form, max \|Δθ\|/\|θ\|max (absolute difference) | 6.4272919e-10 | 0.0000000 | 6.43e-10 | 1.0e-7 | PASS |
| [F5] reaction at the left support: FE vs closed form (relative to the total load) (absolute difference) | 5.1334500e-10 | 0.0000000 | 5.13e-10 | 1.0e-7 | PASS |
| [F5] reaction at the right support (absolute difference) | 2.1383166e-10 | 0.0000000 | 2.14e-10 | 1.0e-7 | PASS |
| [F5] FE reactions satisfy ΣF = 0 and ΣM = 0 (relative) (absolute difference) | 7.5796430e-10 | 0.0000000 | 7.58e-10 | 1.0e-7 | PASS |
| [F6] elastic curve: FE vs closed form, max \|Δy\|/\|y\|max (absolute difference) | 9.5631695e-10 | 0.0000000 | 9.56e-10 | 1.0e-7 | PASS |
| [F6] slope: FE vs closed form, max \|Δθ\|/\|θ\|max (absolute difference) | 7.8205230e-10 | 0.0000000 | 7.82e-10 | 1.0e-7 | PASS |
| [F6] reaction at the left support: FE vs closed form (relative to the total load) (absolute difference) | 4.4662091e-10 | 0.0000000 | 4.47e-10 | 1.0e-7 | PASS |
| [F6] reaction at the right support (absolute difference) | 1.7840001e-10 | 0.0000000 | 1.78e-10 | 1.0e-7 | PASS |
| [F6] FE reactions satisfy ΣF = 0 and ΣM = 0 (relative) (absolute difference) | 6.4998287e-10 | 0.0000000 | 6.50e-10 | 1.0e-7 | PASS |
| [F7] elastic curve: FE vs closed form, max \|Δy\|/\|y\|max (absolute difference) | 6.2420653e-10 | 0.0000000 | 6.24e-10 | 1.0e-7 | PASS |
| [F7] slope: FE vs closed form, max \|Δθ\|/\|θ\|max (absolute difference) | 4.2720755e-10 | 0.0000000 | 4.27e-10 | 1.0e-7 | PASS |
| [F7] reaction at the left support: FE vs closed form (relative to the total load) (absolute difference) | -1.9036233e-9 | 0.0000000 | 1.90e-9 | 1.0e-7 | PASS |
| [F7] reaction at the right support (absolute difference) | -7.8976154e-10 | 0.0000000 | 7.90e-10 | 1.0e-7 | PASS |
| [F7] FE reactions satisfy ΣF = 0 and ΣM = 0 (relative) (absolute difference) | 2.8067856e-9 | 0.0000000 | 2.81e-9 | 1.0e-7 | PASS |
| [fixedw] elastic curve: FE vs closed form, max \|Δy\|/\|y\|max (absolute difference) | 4.8581407e-9 | 0.0000000 | 4.86e-9 | 1.0e-7 | PASS |
| [fixedw] slope: FE vs closed form, max \|Δθ\|/\|θ\|max (absolute difference) | 6.1838393e-11 | 0.0000000 | 6.18e-11 | 1.0e-7 | PASS |
| [fixedw] reaction at the left support: FE vs closed form (relative to the total load) (absolute difference) | 2.1904068e-11 | 0.0000000 | 2.19e-11 | 1.0e-7 | PASS |
| [fixedw] reaction at the right support (absolute difference) | -2.4180635e-11 | 0.0000000 | 2.42e-11 | 1.0e-7 | PASS |
| [fixedw] reaction couple at the left: FE vs closed form (relative to W·L) (absolute difference) | 1.3956533e-12 | 0.0000000 | 1.40e-12 | 1.0e-7 | PASS |
| [fixedw] FE reactions satisfy ΣF = 0 and ΣM = 0 (relative) (absolute difference) | 1.8192499e-11 | 0.0000000 | 1.82e-11 | 1.0e-7 | PASS |
| [fixedw, clamp k = 5EI/L] elastic curve: FE vs closed form, max \|Δy\|/\|y\|max (absolute difference) | 3.2921147e-9 | 0.0000000 | 3.29e-9 | 1.0e-7 | PASS |
| [fixedw, clamp k = 5EI/L] slope: FE vs closed form, max \|Δθ\|/\|θ\|max (absolute difference) | 1.0219095e-10 | 0.0000000 | 1.02e-10 | 1.0e-7 | PASS |
| [fixedw, clamp k = 5EI/L] reaction at the left support: FE vs closed form (relative to the total load) (absolute difference) | 6.3926361e-11 | 0.0000000 | 6.39e-11 | 1.0e-7 | PASS |
| [fixedw, clamp k = 5EI/L] reaction at the right support (absolute difference) | 5.8969615e-12 | 0.0000000 | 5.90e-12 | 1.0e-7 | PASS |
| [fixedw, clamp k = 5EI/L] reaction couple at the left: FE vs closed form (relative to W·L) (absolute difference) | 5.0914777e-12 | 0.0000000 | 5.09e-12 | 1.0e-7 | PASS |
| [fixedw, clamp k = 5EI/L] FE reactions satisfy ΣF = 0 and ΣM = 0 (relative) (absolute difference) | 7.0443417e-11 | 0.0000000 | 7.04e-11 | 1.0e-7 | PASS |
| superposition: FE(both loads) − FE(load 1) − FE(load 2) at 400 mm (relative) (absolute difference) | -2.4885650e-14 | 0.0000000 | 2.49e-14 | 1.0e-9 | PASS |
| Maxwell reciprocity: y at 200 mm under 10 N at 600 = y at 600 under 10 N at 200 (FE) | -0.00042002900 | -0.00042002900 | 1.12e-12 | 1.0e-8 | PASS |
| uniform load: FE deflection between nodes converges as N⁻⁴ (observed 4.000) | true | true | 0.00e+0 | 0.0e+0 | PASS |
| uniform load: FE moment EI·y″ converges as N⁻² (observed 2.000) | true | true | 0.00e+0 | 0.0e+0 | PASS |
| uniform load, 2 elements: nodal deflection already exact (superconvergence) | -0.0037042683 | -0.0037042683 | 2.34e-16 | 1.0e-8 | PASS |
| point load: FE exact at every mesh (largest error 2.2e-9) | true | true | 0.00e+0 | 0.0e+0 | PASS |
| C++ reference [partA]: same mesh (61 nodes) | true | true | 0.00e+0 | 0.0e+0 | PASS |
| C++ reference [partA]: nodal deflections, JS port vs C++ (max \|Δ\|/\|y\|max) (absolute difference) | 0.0000000 | 0.0000000 | 0.00e+0 | 1.0e-9 | PASS |
| C++ reference [partA]: nodal slopes, JS port vs C++ (absolute difference) | 0.0000000 | 0.0000000 | 0.00e+0 | 1.0e-9 | PASS |
| C++ reference [partA]: reactions (force and couple), JS port vs C++ (absolute difference) | 0.0000000 | 0.0000000 | 0.00e+0 | 1.0e-9 | PASS |
| C++ reference [partAboth]: same mesh (61 nodes) | true | true | 0.00e+0 | 0.0e+0 | PASS |
| C++ reference [partAboth]: nodal deflections, JS port vs C++ (max \|Δ\|/\|y\|max) (absolute difference) | 0.0000000 | 0.0000000 | 0.00e+0 | 1.0e-9 | PASS |
| C++ reference [partAboth]: nodal slopes, JS port vs C++ (absolute difference) | 0.0000000 | 0.0000000 | 0.00e+0 | 1.0e-9 | PASS |
| C++ reference [partAboth]: reactions (force and couple), JS port vs C++ (absolute difference) | 0.0000000 | 0.0000000 | 0.00e+0 | 1.0e-9 | PASS |
| C++ reference [partB2]: same mesh (61 nodes) | true | true | 0.00e+0 | 0.0e+0 | PASS |
| C++ reference [partB2]: nodal deflections, JS port vs C++ (max \|Δ\|/\|y\|max) (absolute difference) | 0.0000000 | 0.0000000 | 0.00e+0 | 1.0e-9 | PASS |
| C++ reference [partB2]: nodal slopes, JS port vs C++ (absolute difference) | 0.0000000 | 0.0000000 | 0.00e+0 | 1.0e-9 | PASS |
| C++ reference [partB2]: reactions (force and couple), JS port vs C++ (absolute difference) | 0.0000000 | 0.0000000 | 0.00e+0 | 1.0e-9 | PASS |
| C++ reference [design]: same mesh (62 nodes) | true | true | 0.00e+0 | 0.0e+0 | PASS |
| C++ reference [design]: nodal deflections, JS port vs C++ (max \|Δ\|/\|y\|max) (absolute difference) | 0.0000000 | 0.0000000 | 0.00e+0 | 1.0e-9 | PASS |
| C++ reference [design]: nodal slopes, JS port vs C++ (absolute difference) | 0.0000000 | 0.0000000 | 0.00e+0 | 1.0e-9 | PASS |
| C++ reference [design]: reactions (force and couple), JS port vs C++ (absolute difference) | 0.0000000 | 0.0000000 | 0.00e+0 | 1.0e-9 | PASS |
| C++ reference [F2]: same mesh (61 nodes) | true | true | 0.00e+0 | 0.0e+0 | PASS |
| C++ reference [F2]: nodal deflections, JS port vs C++ (max \|Δ\|/\|y\|max) (absolute difference) | 0.0000000 | 0.0000000 | 0.00e+0 | 1.0e-9 | PASS |
| C++ reference [F2]: nodal slopes, JS port vs C++ (absolute difference) | 0.0000000 | 0.0000000 | 0.00e+0 | 1.0e-9 | PASS |
| C++ reference [F2]: reactions (force and couple), JS port vs C++ (absolute difference) | 0.0000000 | 0.0000000 | 0.00e+0 | 1.0e-9 | PASS |
| C++ reference [F3]: same mesh (61 nodes) | true | true | 0.00e+0 | 0.0e+0 | PASS |
| C++ reference [F3]: nodal deflections, JS port vs C++ (max \|Δ\|/\|y\|max) (absolute difference) | 0.0000000 | 0.0000000 | 0.00e+0 | 1.0e-9 | PASS |
| C++ reference [F3]: nodal slopes, JS port vs C++ (absolute difference) | 0.0000000 | 0.0000000 | 0.00e+0 | 1.0e-9 | PASS |
| C++ reference [F3]: reactions (force and couple), JS port vs C++ (absolute difference) | 0.0000000 | 0.0000000 | 0.00e+0 | 1.0e-9 | PASS |
| C++ reference [F5]: same mesh (61 nodes) | true | true | 0.00e+0 | 0.0e+0 | PASS |
| C++ reference [F5]: nodal deflections, JS port vs C++ (max \|Δ\|/\|y\|max) (absolute difference) | 0.0000000 | 0.0000000 | 0.00e+0 | 1.0e-9 | PASS |
| C++ reference [F5]: nodal slopes, JS port vs C++ (absolute difference) | 0.0000000 | 0.0000000 | 0.00e+0 | 1.0e-9 | PASS |
| C++ reference [F5]: reactions (force and couple), JS port vs C++ (absolute difference) | 0.0000000 | 0.0000000 | 0.00e+0 | 1.0e-9 | PASS |
| C++ reference [F7]: same mesh (61 nodes) | true | true | 0.00e+0 | 0.0e+0 | PASS |
| C++ reference [F7]: nodal deflections, JS port vs C++ (max \|Δ\|/\|y\|max) (absolute difference) | 0.0000000 | 0.0000000 | 0.00e+0 | 1.0e-9 | PASS |
| C++ reference [F7]: nodal slopes, JS port vs C++ (absolute difference) | 0.0000000 | 0.0000000 | 0.00e+0 | 1.0e-9 | PASS |
| C++ reference [F7]: reactions (force and couple), JS port vs C++ (absolute difference) | 0.0000000 | 0.0000000 | 0.00e+0 | 1.0e-9 | PASS |
| C++ reference [fixedw]: same mesh (61 nodes) | true | true | 0.00e+0 | 0.0e+0 | PASS |
| C++ reference [fixedw]: nodal deflections, JS port vs C++ (max \|Δ\|/\|y\|max) (absolute difference) | 0.0000000 | 0.0000000 | 0.00e+0 | 1.0e-9 | PASS |
| C++ reference [fixedw]: nodal slopes, JS port vs C++ (absolute difference) | 0.0000000 | 0.0000000 | 0.00e+0 | 1.0e-9 | PASS |
| C++ reference [fixedw]: reactions (force and couple), JS port vs C++ (absolute difference) | 0.0000000 | 0.0000000 | 0.00e+0 | 1.0e-9 | PASS |
| C++ reference [triangle]: same mesh (61 nodes) | true | true | 0.00e+0 | 0.0e+0 | PASS |
| C++ reference [triangle]: nodal deflections, JS port vs C++ (max \|Δ\|/\|y\|max) (absolute difference) | 0.0000000 | 0.0000000 | 0.00e+0 | 1.0e-9 | PASS |
| C++ reference [triangle]: nodal slopes, JS port vs C++ (absolute difference) | 0.0000000 | 0.0000000 | 0.00e+0 | 1.0e-9 | PASS |
| C++ reference [triangle]: reactions (force and couple), JS port vs C++ (absolute difference) | 0.0000000 | 0.0000000 | 0.00e+0 | 1.0e-9 | PASS |
| C++ reference: all beams compared | true | true | 0.00e+0 | 0.0e+0 | PASS |
| Carlson R_F: K(m = 0.5) = 1.8540746773013719 | 1.8540747 | 1.8540747 | 1.20e-16 | 1.0e-13 | PASS |
| Carlson R_D: E(m = 0.5) = 1.3506438810476755 | 1.3506439 | 1.3506439 | 0.00e+0 | 1.0e-13 | PASS |
| incomplete F(π/4, m = 0.3) = 0.80436 (series check) | 0.80845903 | 0.80845903 | 1.52e-11 | 1.0e-8 | PASS |
| elastica α = 0.05: tip deflection, closed form vs RK4 shooting (N = 400) | 0.016661907 | 0.016661907 | 4.27e-13 | 1.0e-9 | PASS |
| elastica α = 0.05: tip angle | 0.024994274 | 0.024994274 | 2.21e-14 | 1.0e-9 | PASS |
| elastica α = 0.05: tip x-position | 0.99983341 | 0.99983341 | 1.17e-14 | 1.0e-9 | PASS |
| elastica α = 0.05: closed-form shape ends at the closed-form tip | 0.016661907 | 0.016661907 | 4.14e-13 | 1.0e-12 | PASS |
| elastica α = 0.05: arc length of the closed-form shape = L | 1.0000000 | 1.0000000 | 6.88e-15 | 1.0e-12 | PASS |
| elastica α = 0.5: tip deflection, closed form vs RK4 shooting (N = 400) | 0.16214358 | 0.16214358 | 3.20e-14 | 1.0e-9 | PASS |
| elastica α = 0.5: tip angle | 0.24453365 | 0.24453365 | 2.21e-14 | 1.0e-9 | PASS |
| elastica α = 0.5: tip x-position | 0.98408104 | 0.98408104 | 6.35e-14 | 1.0e-9 | PASS |
| elastica α = 0.5: closed-form shape ends at the closed-form tip | 0.16214358 | 0.16214358 | 2.74e-15 | 1.0e-12 | PASS |
| elastica α = 0.5: arc length of the closed-form shape = L | 1.0000000 | 1.0000000 | 4.44e-16 | 1.0e-12 | PASS |
| elastica α = 1: tip deflection, closed form vs RK4 shooting (N = 400) | 0.30172077 | 0.30172077 | 9.33e-14 | 1.0e-9 | PASS |
| elastica α = 1: tip angle | 0.46135195 | 0.46135195 | 1.23e-13 | 1.0e-9 | PASS |
| elastica α = 1: tip x-position | 0.94356676 | 0.94356676 | 2.63e-13 | 1.0e-9 | PASS |
| elastica α = 1: closed-form shape ends at the closed-form tip | 0.30172077 | 0.30172077 | 7.36e-16 | 1.0e-12 | PASS |
| elastica α = 1: arc length of the closed-form shape = L | 1.0000000 | 1.0000000 | 2.22e-16 | 1.0e-12 | PASS |
| elastica α = 2: tip deflection, closed form vs RK4 shooting (N = 400) | 0.49345748 | 0.49345748 | 8.94e-14 | 1.0e-9 | PASS |
| elastica α = 2: tip angle | 0.78174983 | 0.78174983 | 6.27e-13 | 1.0e-9 | PASS |
| elastica α = 2: tip x-position | 0.83935828 | 0.83935828 | 1.09e-12 | 1.0e-9 | PASS |
| elastica α = 2: closed-form shape ends at the closed-form tip | 0.49345748 | 0.49345748 | 6.75e-16 | 1.0e-12 | PASS |
| elastica α = 2: arc length of the closed-form shape = L | 1.0000000 | 1.0000000 | 3.33e-16 | 1.0e-12 | PASS |
| elastica α = 3: tip deflection, closed form vs RK4 shooting (N = 400) | 0.60325344 | 0.60325344 | 6.48e-14 | 1.0e-9 | PASS |
| elastica α = 3: tip angle | 0.98601695 | 0.98601695 | 1.43e-12 | 1.0e-9 | PASS |
| elastica α = 3: tip x-position | 0.74557982 | 0.74557982 | 2.38e-12 | 1.0e-9 | PASS |
| elastica α = 3: closed-form shape ends at the closed-form tip | 0.60325344 | 0.60325344 | 0.00e+0 | 1.0e-12 | PASS |
| elastica α = 3: arc length of the closed-form shape = L | 1.0000000 | 1.0000000 | 0.00e+0 | 1.0e-12 | PASS |
| elastica α = 5: tip deflection, closed form vs RK4 shooting (N = 400) | 0.71379152 | 0.71379152 | 4.41e-13 | 1.0e-9 | PASS |
| elastica α = 5: tip angle | 1.2153681 | 1.2153681 | 3.32e-12 | 1.0e-9 | PASS |
| elastica α = 5: tip x-position | 0.61237164 | 0.61237164 | 6.13e-12 | 1.0e-9 | PASS |
| elastica α = 5: closed-form shape ends at the closed-form tip | 0.71379152 | 0.71379152 | 4.67e-16 | 1.0e-12 | PASS |
| elastica α = 5: arc length of the closed-form shape = L | 1.0000000 | 1.0000000 | 4.44e-16 | 1.0e-12 | PASS |
| elastica, small load: δ_v/L → α/3 (α = 0.001) | 0.00033333329 | 0.00033333333 | 1.15e-7 | 1.0e-6 | PASS |
| elastica, small load: tip angle → α/2 | 0.00049999995 | 0.00050000000 | 9.17e-8 | 1.0e-6 | PASS |
| linear theory is 5 % high at α = 0.67564 (bisection) | 0.67563667 | 0.67563667 | 3.11e-14 | 1.0e-9 | PASS |
| RK4 shooting converges as N⁻⁴ (observed 3.945) | true | true | 0.00e+0 | 0.0e+0 | PASS |
| self-weight only, small: tip deflection → βL/8 | 0.0012499984 | 0.0012500000 | 1.25e-6 | 2.0e-3 | PASS |
| Part C preset reaches α = 3.63 > 3 | true | true | 0.00e+0 | 0.0e+0 | PASS |
| units: 10 N in lbf | 2.2480894 | 2.2480894 | 0.00e+0 | 1.0e-12 | PASS |
| units: 2 kN/m in kip/ft | 0.13704353 | 0.13704353 | 0.00e+0 | 1.0e-12 | PASS |
| units: 4500 N·m/rad in lb·in/rad | 39828.356 | 39828.356 | 0.00e+0 | 1.0e-12 | PASS |

212 of 212 passed.

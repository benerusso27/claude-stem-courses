"""Sample data embedded in the Lab 4 simulation overlay (all converted with the analysis script's measured values):
beam: bending moment at the three bottom gages at 20 kN (Part A), M = E S eps;
profiles: gage stresses through the depth (Part A at 20 kN, Part B at 15 kN, Part C at 40 kN via Lab 1's curve);
mk: applied moment vs gage curvature through the Part C load cycle."""
import json
from pathlib import Path

import lab04_analysis as LA
from lab04_model import sigma_of

HERE = Path(__file__).resolve().parent


def overlay():
    data = LA.load(LA.LAB / "sample_data.csv")
    m = json.loads((HERE / "specimen_measurements.json").read_text())
    r = LA.analyze(data, m)
    E = r["A"]["E"] * 1e9
    Est = m["reference"]["E_st_GPa"] * 1e9
    h, ts = r["geom"]["h"], r["geom"]["ts"]
    A, B, C = data["A"], data["B"], data["C"]
    iA, iB, iC = int(A["load_N"].argmax()), int(B["load_N"].argmax()), int(C["load_N"].argmax())
    S = r["A"]["S_mm3"] * 1e-9
    beam = {"P": 20000.0, "x": [0.100, 0.150, 0.300],
            "M": [round(E * S * A[c][iA] * 1e-6 * 20000.0 / A["load_N"][iA], 3) for c in ("strain_bottom_x100_ue", "strain_bottom_x150_ue", "strain_bottom_ue")]}
    side = [f"strain_side{j}_ue" for j in range(1, 6)]

    def prof(D, i, ys, H, Ebot, law=None):
        y = [v * 1e-3 for v in ys] + [H * 1e-3, 0.0]
        e = [D[c][i] * 1e-6 for c in side] + [D["strain_top_ue"][i] * 1e-6, D["strain_bottom_ue"][i] * 1e-6]
        Es = [E] * 6 + [Ebot]
        s = [sigma_of(law, ee) if law else EE * ee for ee, EE in zip(e, Es)]
        return {"y": [round(v, 6) for v in y], "s": [round(v, 0) for v in s]}
    ro = dict(law="ro", E=E, sY=m["reference"]["sY_al_MPa"] * 1e6, m=m["reference"]["m_RO"])
    profiles = {"fourpt": prof(A, iA, m["yA_mm"], h, E), "composite": prof(B, iB, m["yB_mm"], h + ts, Est), "plastic": prof(C, iC, m["yA_mm"], h, E, ro)}
    mk = {"k": [round(x, 6) for x in r["C"]["kappa"]], "M": [round(x, 2) for x in r["C"]["M"]]}
    return {"beam": beam, "profiles": profiles, "mk": mk}

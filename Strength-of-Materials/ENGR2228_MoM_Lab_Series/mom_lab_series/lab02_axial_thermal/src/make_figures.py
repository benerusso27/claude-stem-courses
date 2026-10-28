"""Lab 2 figures (series style). Writes ../figures/*.svg, *.png and ALT_TEXT.md.
Plots use ILLUSTRATIVE numbers (not the lab specimens) so the handout does not give away results."""
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "shared"))
from figstyle import (DASH, DIM, FAIL, INK, LOAD, MEMBER_FILL, REACT, STRESS_EDGE, THEORY, THIRD, arrow,  # noqa: E402
                      dim_line, new_fig, save, sketch_axes, write_alt_text)
from matplotlib.patches import Circle, Polygon, Rectangle  # noqa: E402

FIG = HERE.parent / "figures"


def fig1_setups():
    fig, ax = sketch_axes("full", 3.4, xlim=(0, 19.5), ylim=(0, 10.1))
    # (a) flat bar with gages
    ax.text(0.2, 9.65, "(a) Part A: flat bar", fontsize=8.5, fontweight="bold")
    ax.add_patch(Rectangle((2.2, 1.0), 1.4, 1.2, fc="#BFBFBF", ec=INK, hatch="////", lw=0.8))
    ax.add_patch(Rectangle((2.2, 7.0), 1.4, 1.2, fc="#BFBFBF", ec=INK, hatch="////", lw=0.8))
    ax.add_patch(Rectangle((2.45, 1.6), 0.9, 6.0, fc=MEMBER_FILL, ec=INK, lw=1.2))
    ax.add_patch(Rectangle((2.7, 4.2), 0.4, 0.9, fc=THEORY, alpha=0.6, ec=THEORY))      # axial gage
    ax.add_patch(Rectangle((2.55, 3.5), 0.7, 0.35, fc=THIRD, alpha=0.6, ec=THIRD))      # transverse gage
    arrow(ax, 2.9, 8.25, 2.9, 9.2, color=LOAD); arrow(ax, 2.9, 0.9, 2.9, 0.2, color=LOAD)
    ax.text(3.6, 4.65, "axial gage\n(front and back)", fontsize=7.2, color=THEORY, va="center")
    ax.text(3.6, 3.4, "transverse gage\n(front and back)", fontsize=7.2, color=THIRD, va="center")
    ax.text(3.15, 8.35, "P", fontsize=9, color=LOAD, fontstyle="italic")
    # (b) rod in tube
    ax.text(6.9, 9.65, "(b) Part B: rod in tube", fontsize=8.5, fontweight="bold")
    ax.add_patch(Rectangle((7.4, 7.3), 4.6, 0.5, fc="#D9D9D9", ec=INK))
    ax.add_patch(Rectangle((7.4, 1.0), 4.6, 0.5, fc="#D9D9D9", ec=INK))
    ax.add_patch(Rectangle((8.2, 1.5), 0.55, 5.55, fc="none", ec=THIRD, lw=1.5))         # tube walls
    ax.add_patch(Rectangle((10.65, 1.5), 0.55, 5.55, fc="none", ec=THIRD, lw=1.5))
    ax.add_patch(Rectangle((9.25, 1.5), 0.9, 5.8, fc=MEMBER_FILL, ec=THEORY, lw=1.5))    # rod
    ax.annotate("gap g\n(exaggerated)", xy=(10.9, 7.15), xytext=(12.3, 6.4), fontsize=7.2, color="#8A5300",
                arrowprops=dict(arrowstyle="-", color=DIM, lw=0.6))
    ax.add_patch(Rectangle((10.67, 4.0), 0.5, 0.8, fc=THIRD, alpha=0.6, ec=THIRD))
    ax.text(12.3, 4.4, "tube gages", fontsize=7.2, color=THIRD, va="center")
    ax.text(9.7, 4.4, "steel\nrod", fontsize=7, color=THEORY, ha="center", va="center")
    ax.text(8.0, 3.0, "Al\ntube", fontsize=7, color=THIRD, ha="right", va="center")
    arrow(ax, 9.7, 9.25, 9.7, 7.85, color=LOAD); ax.text(9.95, 8.55, "P", fontsize=9, color=LOAD, fontstyle="italic")
    ax.add_patch(Rectangle((11.2, 8.0), 0.5, 0.5, fc="white", ec=INK)); ax.plot([11.45, 11.45], [7.8, 8.0], color=INK, lw=1); ax.text(11.85, 8.25, "dial gage", fontsize=7.2, va="center")
    # (c) bolt and sleeve in a bath
    ax.text(14.3, 9.65, "(c) Part C: bolt + sleeve", fontsize=8.5, fontweight="bold")
    ax.add_patch(Rectangle((14.6, 0.6), 4.6, 6.4, fc="#EAF4FB", ec=DIM, lw=0.8))            # bath
    ax.add_patch(Rectangle((16.0, 1.6), 0.5, 4.6, fc="none", ec=THIRD, lw=1.5))
    ax.add_patch(Rectangle((17.4, 1.6), 0.5, 4.6, fc="none", ec=THIRD, lw=1.5))
    ax.add_patch(Rectangle((16.6, 1.0), 0.7, 5.8, fc=MEMBER_FILL, ec=THEORY, lw=1.5))
    ax.add_patch(Rectangle((15.7, 6.2), 2.5, 0.45, fc="#BFBFBF", ec=INK))                 # head
    ax.add_patch(Rectangle((15.7, 1.15), 2.5, 0.45, fc="#BFBFBF", ec=INK))               # nut
    ax.add_patch(Rectangle((16.78, 3.5), 0.34, 0.8, fc=THEORY, alpha=0.6, ec=THEORY))
    ax.text(16.95, 7.25, "steel bolt, Al sleeve", fontsize=7.2, ha="center")
    ax.plot([18.6, 18.6], [1.2, 7.9], color=FAIL, lw=1.6); ax.text(19.4, 8.15, "thermocouple", fontsize=7.2, color="#8A5300", ha="right")
    ax.text(15.0, 0.25, "water bath 20 → 80 °C", fontsize=7.2, color=DIM)
    return save(fig, FIG / "fig1_setups", title="Figure 1. The three parts of Lab 2",
                alt=("Three schematics. (a) A flat aluminum bar held in wedge grips and pulled by a load P, with an axial and a "
                     "transverse strain gage on the front face and the same pair on the back face. (b) A steel rod inside an "
                     "aluminum tube between two rigid caps on a press; the tube is slightly shorter, leaving a small gap under "
                     "the top cap, drawn exaggerated. Gages are on the tube and a dial gage measures the caps' approach. (c) A "
                     "steel bolt with head and nut clamping an aluminum sleeve, submerged in a water bath heated from 20 to "
                     "80 degrees Celsius, with a strain gage on the bolt shank and a thermocouple in the water."))


def fig2_compatibility():
    fig, ax = sketch_axes("full", 2.9, xlim=(0, 16), ylim=(0, 6.6))
    ax.text(0.2, 6.2, "(a) Before loading", fontsize=8.5, fontweight="bold")
    ax.add_patch(Rectangle((0.6, 1.0), 0.6, 4.4, fc=MEMBER_FILL, ec=THEORY, lw=1.5))
    ax.add_patch(Rectangle((1.7, 1.0), 0.6, 4.0, fc=MEMBER_FILL, ec=THIRD, lw=1.5))
    ax.plot([0.3, 2.9], [1.0, 1.0], color=INK, lw=2)
    dim_line(ax, 3.1, 1.0, 3.1, 5.4, "L", offset=(0.25, 0))
    dim_line(ax, 2.5, 5.0, 2.5, 5.4, "", offset=(0, 0))
    ax.text(2.7, 5.55, "g", fontsize=8.5, color=DIM)
    ax.text(0.9, 0.55, "1", fontsize=8.5, color=THEORY, ha="center"); ax.text(2.0, 0.55, "2", fontsize=8.5, color=THIRD, ha="center")
    ax.text(5.0, 6.2, "(b) Free body of the cap", fontsize=8.5, fontweight="bold")
    ax.add_patch(Rectangle((5.6, 3.2), 3.2, 0.5, fc="#D9D9D9", ec=INK))
    arrow(ax, 7.2, 5.3, 7.2, 3.75, color=LOAD); ax.text(7.4, 4.9, "P", fontsize=9, color=LOAD, fontstyle="italic")
    arrow(ax, 6.2, 1.6, 6.2, 3.15, color=REACT, hollow=True); ax.text(5.75, 1.25, r"$-F_1$", fontsize=8.5, color=THEORY)
    arrow(ax, 8.2, 1.6, 8.2, 3.15, color=REACT, hollow=True); ax.text(7.95, 1.25, r"$-F_2$", fontsize=8.5, color=THIRD)
    ax.text(5.6, 0.45, r"$\Sigma F = 0$:  $F_1 + F_2 = -P$" + "\n(member forces tension +)", fontsize=8, color=INK)
    ax.text(10.4, 6.2, "(c) After loading: one cap position", fontsize=8.5, fontweight="bold")
    ax.add_patch(Rectangle((10.8, 1.0), 0.6, 3.7, fc=MEMBER_FILL, ec=THEORY, lw=1.5))
    ax.add_patch(Rectangle((11.9, 1.0), 0.6, 3.7, fc=MEMBER_FILL, ec=THIRD, lw=1.5))
    ax.plot([10.5, 13.1], [1.0, 1.0], color=INK, lw=2); ax.plot([10.5, 13.1], [4.7, 4.7], color=INK, lw=2, ls=DASH)
    ax.text(13.3, 3.4, r"$L + \delta_1 = (L - g) + \delta_2$" + "\n" + r"$\delta_i = \dfrac{F_i L_i}{E_i A_i} + \alpha_i \Delta T L_i$",
            fontsize=8.2, color=INK, va="center")
    return save(fig, FIG / "fig2_compatibility", title="Figure 2. Equilibrium and compatibility for two members between caps",
                alt=("Three sketches. (a) Two members standing on a base before loading: member 1 has length L, member 2 is "
                     "shorter by a gap g. (b) Free-body diagram of the rigid cap: the press load P acts down, and the two members "
                     "push up with forces minus F1 and minus F2, so equilibrium gives F1 plus F2 equals minus P with tension "
                     "positive. (c) After loading both members end at the same cap position, so L plus delta 1 equals L minus g "
                     "plus delta 2, where each delta is F L over E A plus alpha delta T L."))


def fig3_sharing():
    # illustrative: brass rod d = 16 mm in steel tube 30/24 mm, gap 0.12 mm, L = 200 mm
    E1, A1, E2, A2, L, g = 97e3, np.pi / 4 * 16 ** 2, 205e3, np.pi / 4 * (30 ** 2 - 24 ** 2), 200.0, 0.12
    k1, k2 = E1 * A1 / L, E2 * A2 / L          # N/mm
    Pg = k1 * g / 1e3                          # kN
    P = np.linspace(0, 60, 601)
    F2 = np.where(P < Pg, 0, -(P - Pg) * k2 / (k1 + k2))
    F2_nogap = -P * k2 / (k1 + k2)
    fig, axs = new_fig("full", 2.8, ncols=2, gridspec_kw=dict(wspace=0.38))
    ax = axs[0]
    ax.axvspan(0, Pg, color=FAIL, alpha=0.14, lw=0)
    ax.plot(P, F2_nogap, color=THEORY, lw=1.2, ls=DASH, label="member 2, no gap (constant share)")
    ax.plot(P, F2, color=THEORY, lw=1.8, label="member 2, gap g (engages late)")
    ax.plot(P, -P - F2, color=THIRD, lw=1.6, ls=(0, (6, 3, 1.5, 3)), label="member 1, gap g")
    ax.axvline(Pg, color=DIM, lw=0.8, ls=DASH)
    ax.annotate(r"gap closes at $P = k_1 g$", xy=(Pg, -2), xytext=(Pg + 6, -4), fontsize=7.6, color=DIM,
                arrowprops=dict(arrowstyle="-", color=DIM, lw=0.6))
    ax.annotate("superposition\nfails in the\nshaded range", xy=(Pg * 0.5, -30), xytext=(Pg + 4, -31), fontsize=7.4, color="#8A5300",
                va="center", arrowprops=dict(arrowstyle="-", color="#8A5300", lw=0.6))
    ax.set_xlabel("Press load, P (kN)"); ax.set_ylabel("Member force, tension + (kN)")
    ax.legend(fontsize=6.8, loc="lower left", bbox_to_anchor=(0.0, 0.0))
    ax.set_ylim(-62, 3)
    ax = axs[1]
    Cc = 0.002   # mm/kN cap compliance
    dial = lambda p: np.where(p < Pg, p / k1 * 1e3, g + (p - Pg) / (k1 + k2) * 1e3) + Cc * p
    ax.axvline(Pg, color=DIM, lw=0.8, ls=DASH)
    ax.plot(P, dial(P), color=THEORY, lw=1.8)
    ax.text(Pg + 1.5, 0.45 * g, r"slope $1/k_1 + C$", fontsize=7.8)
    ax.text(32, float(dial(32)) - 0.045, r"slope $1/(k_1 + k_2) + C$", fontsize=7.8)
    ax.set_xlabel("Press load, P (kN)"); ax.set_ylabel("Cap approach, Δ (mm)")
    return save(fig, FIG / "fig3_sharing", title="Figure 3. Load sharing with a fit-up gap (illustrative)",
                alt=("Two plots for an illustrative brass rod in a steel tube with a 0.12 millimeter gap, press load 0 to 60 kN. "
                     "Left: member 2's force stays at zero in a shaded region up to the load k1 times g, about 12 kN, then "
                     "becomes increasingly compressive along a straight line; a dashed line through the origin shows the "
                     "no-gap prediction with a constant share; member 1's force is the dash-dot line and carries all the load "
                     "until the gap closes. The shaded region is labeled superposition fails in the shaded range. Right: the "
                     "caps' approach rises steeply with slope 1 over k1 plus C until the gap closes, then more gently with slope "
                     "1 over k1 plus k2, plus C, where C is the compliance of the caps and fixtures."))


def fig4_thermal():
    fig, ax = sketch_axes("full", 2.9, xlim=(0, 17), ylim=(-0.6, 7.0))
    def bar(x, y0, h, col, lab):
        ax.add_patch(Rectangle((x, y0), 0.7, h, fc=MEMBER_FILL, ec=col, lw=1.5)); ax.text(x + 0.35, y0 - 0.45, lab, fontsize=8, color=col, ha="center")
    ax.text(0.2, 6.6, "(a) Free expansion", fontsize=8.5, fontweight="bold")
    bar(0.8, 1.0, 3.6, THEORY, "bolt"); bar(2.2, 1.0, 4.2, THIRD, "sleeve")
    ax.plot([0.5, 3.4], [4.0, 4.0], color=DIM, lw=0.8, ls=DASH)
    ax.text(0.3, -0.35, r"$\alpha_s \Delta T L > \alpha_b \Delta T L$", fontsize=8, color=INK)
    ax.text(5.2, 6.6, "(b) Clamped", fontsize=8.5, fontweight="bold")
    bar(6.0, 1.0, 3.9, THEORY, "bolt"); bar(7.6, 1.0, 3.9, THIRD, "sleeve")
    ax.plot([5.7, 8.6], [4.9, 4.9], color=INK, lw=2)
    arrow(ax, 6.35, 5.0, 6.35, 5.9, color=LOAD, ms=9); ax.text(6.0, 6.0, r"$F$", fontsize=8.5, color=LOAD)
    arrow(ax, 7.95, 5.9, 7.95, 5.0, color=LOAD, ms=9); ax.text(8.15, 5.6, r"$-F$", fontsize=8.5, color=LOAD)
    ax.text(5.3, -0.35, "bolt: tension F;  sleeve: compression", fontsize=7.6, color=INK)
    ax.text(10.6, 6.6, "(c) Compatibility", fontsize=8.5, fontweight="bold")
    ax.text(10.6, 3.3, r"$\alpha_b \Delta T L + \dfrac{F L}{E_b A_b} = \alpha_s \Delta T L - \dfrac{F L}{E_s A_s}$" + "\n\n" +
            r"$\dfrac{\Delta F}{\Delta T} = \dfrac{(\alpha_s - \alpha_b) L}{L/(E_bA_b) + L/(E_sA_s)}$", fontsize=8.3, va="center")
    return save(fig, FIG / "fig4_thermal", title="Figure 4. Thermal stress in a bolted joint",
                alt=("Three panels. (a) Unconstrained, a heated aluminum sleeve would grow more than the steel bolt, since its "
                     "coefficient of expansion is larger. (b) Clamped by the head and nut, both end at the same length: the bolt "
                     "is stretched into tension F and the sleeve squeezed into compression minus F. (c) Compatibility: the bolt's "
                     "thermal plus mechanical elongation equals the sleeve's, which gives the change in bolt force per degree as "
                     "alpha sleeve minus alpha bolt times L, divided by the sum of the two flexibilities L over E A."))


def fig5_superposition():
    fig, ax = sketch_axes("full", 2.6, xlim=(0, 18), ylim=(0, 6.0))
    def bar(x0, y, lab, wall_right=True, load=False, react=False, title=""):
        ax.add_patch(Rectangle((x0 - 0.3, y - 0.9), 0.3, 1.8, fc="white", ec=DIM, hatch="////", lw=0.8))
        ax.add_patch(Rectangle((x0, y - 0.35), 2.4, 0.7, fc=MEMBER_FILL, ec=INK, lw=1.2))
        ax.add_patch(Rectangle((x0 + 2.4, y - 0.22), 1.6, 0.44, fc=MEMBER_FILL, ec=INK, lw=1.2))
        if wall_right:
            ax.add_patch(Rectangle((x0 + 4.0, y - 0.9), 0.3, 1.8, fc="white", ec=DIM, hatch="////", lw=0.8))
        if load:
            arrow(ax, x0 + 2.4, y + 0.9, x0 + 3.3, y + 0.9, color=LOAD, ms=9); ax.text(x0 + 2.4, y + 1.15, r"$P_B$", fontsize=8, color=LOAD)
        if react:
            arrow(ax, x0 + 5.3, y, x0 + 4.05, y, color=REACT, hollow=True, ms=9); ax.text(x0 + 4.6, y + 0.3, "R", fontsize=8.5, color=REACT, fontstyle="italic")
        ax.text(x0 + 1.9, y - 1.4, lab, fontsize=7.8, ha="center")
        if title:
            ax.text(x0 - 0.3, y + 1.9, title, fontsize=8.5, fontweight="bold")
    bar(0.6, 3.0, "both ends fixed: R unknown", True, True, False, "(a) Redundant bar")
    ax.text(5.6, 3.0, "=", fontsize=14)
    bar(6.6, 3.0, r"remove the right wall: $\delta_P + \delta_T$", False, True, False, "(b) Load and ΔT")
    ax.text(11.6, 3.0, "+", fontsize=14)
    bar(12.4, 3.0, r"apply R alone: $\delta_R = -R(f_1 + f_2)$", False, False, True, "(c) Redundant force")
    ax.text(0.3, 0.3, r"Compatibility: $\delta_P + \delta_T + \delta_R = 0$ (fixed) or $= g$ (gap closed);  $f_i = L_i/(E_iA_i)$", fontsize=8.5, color=INK)
    return save(fig, FIG / "fig5_superposition", title="Figure 5. Solving a redundant bar by superposition",
                alt=("A stepped bar fixed between two walls with a load P B at the step equals the same bar with the right wall "
                     "removed, loaded by P B and heated, plus the bar loaded only by the unknown wall reaction R at its right end. "
                     "The free elongations add: delta P plus delta T plus delta R equals zero for a fixed wall, or equals the gap g "
                     "once it closes, where delta R equals minus R times the sum of the segment flexibilities L over E A."))


if __name__ == "__main__":
    entries = [f() for f in (fig1_setups, fig2_compatibility, fig3_sharing, fig4_thermal, fig5_superposition)]
    write_alt_text(entries, FIG / "ALT_TEXT.md", "Lab 2: Axial deformation, statically indeterminate members and thermal stress")
    print("wrote", [e["file"] for e in entries])

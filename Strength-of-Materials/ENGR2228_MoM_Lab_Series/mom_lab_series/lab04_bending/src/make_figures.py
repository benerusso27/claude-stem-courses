"""Lab 4 figures (series style). Writes ../figures/*.svg, *.png and ALT_TEXT.md.
Plots are normalized or illustrative so the handout does not give away results."""
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "shared"))
from figstyle import (DASH, DASHDOT, DIM, FAIL, FOURTH, INK, LOAD, MEMBER_FILL, NUMERIC, REACT, THEORY, THIRD, arrow,  # noqa: E402
                      dim_line, new_fig, save, sketch_axes, write_alt_text)
from matplotlib.patches import Arc, Circle, FancyArrowPatch, Polygon, Rectangle  # noqa: E402

FIG = HERE.parent / "figures"


def fig1_setup():
    fig, ax = sketch_axes("full", 3.0, xlim=(0, 21), ylim=(0, 8))
    ax.add_patch(Rectangle((1.0, 3.0), 13.0, 1.0, fc=MEMBER_FILL, ec=INK, lw=1.2))
    for x in (1.5, 13.5):
        ax.add_patch(Polygon([[x, 3.0], [x - 0.4, 2.3], [x + 0.4, 2.3]], fc="#BFBFBF", ec=INK))
    ax.add_patch(Circle((13.5, 2.55), 0.0, fc="none"))
    ax.add_patch(Rectangle((5.0, 5.0), 5.0, 0.5, fc="#D9D9D9", ec=INK))          # spreader beam
    for x in (5.5, 9.5):
        ax.plot([x, x], [4.0, 5.0], color=INK, lw=1.0)
        ax.add_patch(Circle((x, 4.15), 0.15, fc="white", ec=INK))
    arrow(ax, 7.5, 6.6, 7.5, 5.55, color=LOAD); ax.text(7.75, 6.3, "P", color=LOAD, fontstyle="italic", fontsize=9)
    dim_line(ax, 1.5, 0.9, 13.5, 0.9, "span L = 600 mm", offset=(0, -0.35), fs=7.5)
    dim_line(ax, 1.5, 6.0, 5.5, 6.0, "a = 200 mm", offset=(0, 0.3), fs=7.5)
    ax.text(7.5, 4.55, "P/2      P/2", ha="center", fontsize=7.5, color=LOAD)
    # gages at midspan on the side face and outer-span bottom gages
    for yy in np.linspace(3.1, 3.9, 5):
        ax.add_patch(Rectangle((7.3, yy - 0.05), 0.4, 0.1, fc=THEORY, ec=THEORY))
    ax.add_patch(Rectangle((7.3, 2.82), 0.4, 0.12, fc=THIRD, ec=THIRD))
    ax.add_patch(Rectangle((3.3, 2.82), 0.4, 0.12, fc=THIRD, ec=THIRD)); ax.add_patch(Rectangle((4.3, 2.82), 0.4, 0.12, fc=THIRD, ec=THIRD))
    ax.text(4.0, 2.3, "x = 100, 150 mm", fontsize=7, color=THIRD, ha="center", va="center")
    ax.text(9.2, 2.1, "midspan: 5 side gages,\n1 top, 1 bottom, 1 transverse", fontsize=7, color=THEORY, ha="center", va="center")
    # cross-sections
    ax.text(16.0, 7.4, "Parts A, C", fontsize=8, fontweight="bold", ha="center")
    ax.add_patch(Rectangle((15.4, 4.0), 1.2, 2.4, fc=MEMBER_FILL, ec=INK)); ax.text(16.0, 3.6, "25.4 × 50.8 mm", ha="center", fontsize=7)
    ax.text(19.2, 7.4, "Part B", fontsize=8, fontweight="bold", ha="center")
    ax.add_patch(Rectangle((18.6, 4.3), 1.2, 2.4, fc=MEMBER_FILL, ec=INK))
    ax.add_patch(Rectangle((18.6, 4.0), 1.2, 0.3, fc=THEORY, alpha=0.5, ec=INK)); ax.text(19.2, 3.6, "+ 6.35 mm steel", ha="center", fontsize=7)
    ax.text(17.6, 2.9, "aluminum 6061-T6", ha="center", fontsize=7, color=DIM)
    return save(fig, FIG / "fig1_setup", title="Figure 1. Four-point bending set-up",
                alt=("A beam rests on two supports 600 millimeters apart. A spreader beam on top applies two equal loads P over 2 at "
                     "200 millimeters from each support, so the middle 200 millimeters carry a constant moment. At midspan five strain "
                     "gages run up the side face, with one more on the top face and one on the bottom face; two bottom gages sit in "
                     "the left outer span at 100 and 150 millimeters from the support. Insets show the cross-sections: a 25.4 by 50.8 "
                     "millimeter 6061-T6 bar for Parts A and C, and the same bar with a steel strip bonded to its bottom for Part B."))


def fig2_vm():
    fig, axs = new_fig("full", 2.6, ncols=3, gridspec_kw=dict(wspace=0.5, width_ratios=[1.05, 1, 1]))
    ax = axs[0]
    ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off")
    ax.add_patch(Rectangle((0.6, 4.4), 5.4, 1.6, fc=MEMBER_FILL, ec=INK))
    arrow(ax, 1.3, 2.9, 1.3, 4.35, color=REACT, hollow=True, ms=9); ax.text(1.7, 3.1, r"$R_A$", fontsize=8.5, color=REACT)
    arrow(ax, 6.35, 7.3, 6.35, 3.4, color=LOAD, ms=9); ax.text(5.6, 7.0, r"$V$", fontsize=9.5, color=LOAD)
    a = FancyArrowPatch((7.2, 3.6), (7.2, 6.8), connectionstyle="arc3,rad=0.55", arrowstyle="-|>", mutation_scale=11, color=THEORY, lw=1.5)
    ax.add_patch(a); ax.text(9.0, 5.0, r"$M$", fontsize=9.5, color=THEORY, va="center")
    ax.text(0.2, 0.3, "Left part of the beam:\nV acts down on the cut\nface; M turns counter-\nclockwise.", fontsize=6.6, color=DIM)
    ax.set_title("(a) Positive V and M (Beer)", fontsize=8.5, loc="left")
    x = np.linspace(0, 1, 401)
    a_ = 1 / 3
    V = np.where(x < a_, 0.5, np.where(x < 1 - a_, 0.0, -0.5))
    Mx = np.where(x < a_, 0.5 * x, np.where(x < 1 - a_, 0.5 * a_, 0.5 * (1 - x)))
    ax = axs[1]
    ax.plot(x, V, color=THEORY, lw=1.8); ax.axhline(0, color=INK, lw=0.6)
    ax.set_xlabel("Position, x/L"); ax.set_ylabel("Shear, V/P"); ax.set_ylim(-0.7, 0.7)
    ax.set_title("(b) Shear", fontsize=8.5, loc="left")
    ax.text(0.85, 0.3, "middle third:\nV = 0", ha="center", fontsize=7, color=DIM)
    ax = axs[2]
    ax.plot(x, Mx, color=THEORY, lw=1.8); ax.axhline(0, color=INK, lw=0.6)
    ax.fill_between(x, 0, Mx, where=(x >= a_) & (x <= 1 - a_), color=FAIL, alpha=0.15, lw=0)
    ax.set_xlabel("Position, x/L"); ax.set_ylabel("Moment, M/(PL)"); ax.set_ylim(0, 0.24)
    ax.text(0.5, 0.177, "M = Pa/2", ha="center", fontsize=7.5)
    ax.annotate("slope = V", xy=(0.2, 0.1), xytext=(0.03, 0.2), fontsize=7, color=DIM, arrowprops=dict(arrowstyle="-", color=DIM, lw=0.6))
    ax.set_title("(c) Bending moment", fontsize=8.5, loc="left")
    return save(fig, FIG / "fig2_vm", title="Figure 2. Sign convention and diagrams for four-point bending",
                alt=("Three panels. (a) Beer's positive internal forces on a left free body: the shear V acts downward on the cut "
                     "face and the bending moment M acts counterclockwise; the support reaction R A pushes up. (b) Shear diagram for "
                     "four-point bending with loads at one third and two thirds of the span: V equals plus P over 2 in the left "
                     "third, zero in the middle third and minus P over 2 in the right third. (c) Bending-moment diagram: M rises "
                     "linearly with slope V to P a over 2, stays constant over the middle third, which is shaded as the region of "
                     "pure bending, and falls back to zero at the right support."))


def fig3_flexure():
    fig, axs = new_fig("full", 2.7, ncols=3, gridspec_kw=dict(wspace=0.5))
    y = np.linspace(-1, 1, 201)
    ax = axs[0]
    ax.plot(-y, y, color=THEORY, lw=1.8)
    ax.axvline(0, color=INK, lw=0.6); ax.axhline(0, color=DIM, lw=0.8, ls=DASH)
    ax.set_xlabel(r"Strain, $\varepsilon_x$ (×$c\kappa$)"); ax.set_ylabel("Height, y/c")
    ax.text(0.05, 0.08, "neutral axis", fontsize=7, color=DIM)
    ax.text(0.08, 0.8, "top: compression", fontsize=7); ax.text(-0.95, -0.8, "bottom: tension", fontsize=7)
    ax.set_title(r"(a) $\varepsilon_x = -y/\rho$", fontsize=8.5, loc="left")
    ax = axs[1]
    ax.fill_betweenx(y, 0, -y, color=THEORY, alpha=0.15, lw=0)
    ax.plot(-y, y, color=THEORY, lw=1.8)
    ax.axvline(0, color=INK, lw=0.6); ax.axhline(0, color=DIM, lw=0.8, ls=DASH)
    ax.set_xlabel(r"Stress, $\sigma_x$ (×$Mc/I$)"); ax.set_ylabel("Height, y/c")
    ax.text(0.08, 0.55, r"$\int\sigma\,dA = 0$" + "\n" + r"$-\int y\sigma\,dA = M$", fontsize=7.5)
    ax.set_title(r"(b) $\sigma_x = -My/I$", fontsize=8.5, loc="left")
    ax = axs[2]
    n, ts, h = 3.0, 0.25, 2.0
    yb = (h * (ts + h / 2) + n * ts * ts / 2) / (h + n * ts)
    yy = np.linspace(0, ts + h, 400)
    eps = -(yy - yb)
    sig = np.where(yy < ts, n * eps, eps)
    ax.plot(eps / (ts + h), yy, color=DIM, lw=1.0, ls=DASH, label="strain (continuous)")
    ax.plot(sig / (ts + h), yy, color=THEORY, lw=1.8, label="stress (jumps by n)")
    ax.axhline(ts, color=THIRD, lw=0.8, ls=DASHDOT); ax.text(1.85, ts + 0.06, "interface", fontsize=6.8, color=THIRD, ha="right")
    ax.axhline(yb, color=NUMERIC, lw=0.8, ls=DASH); ax.text(0.1, yb + 0.06, "neutral axis", fontsize=6.8, color=NUMERIC)
    ax.axvline(0, color=INK, lw=0.6)
    ax.set_xlabel("Strain or stress (scaled)"); ax.set_ylabel("Height above bottom")
    ax.set_xlim(-0.75, 1.9); ax.set_ylim(-0.05, 3.0)
    ax.legend(fontsize=6.5, loc="upper right")
    ax.set_title("(c) Stiff strip at the bottom", fontsize=8.5, loc="left")
    return save(fig, FIG / "fig3_flexure", title="Figure 3. Strain and stress in elastic bending",
                alt=("Three panels through the depth of a beam under positive moment. (a) The strain varies linearly from compression "
                     "at the top to tension at the bottom and is zero at the neutral axis. (b) The elastic stress has the same linear "
                     "shape; equilibrium requires its resultant force to vanish and its moment to equal M. (c) A beam with a stiffer "
                     "strip at the bottom: the strain is still linear and continuous, but the stress in the strip is n times larger "
                     "at the same strain, so it jumps at the interface, and the neutral axis moves below mid-depth."))


def fig5_plastic():
    fig, axs = new_fig("full", 2.7, ncols=3, gridspec_kw=dict(wspace=0.45))
    y = np.linspace(-1, 1, 401)
    ax = axs[0]
    for k, col, ls, lab in ((1, THEORY, "-", r"$\kappa = \kappa_Y$"), (2, THIRD, DASHDOT, r"$\kappa = 2\kappa_Y$"), (8, FOURTH, (0, (1.2, 2.4)), r"$\kappa = 8\kappa_Y$")):
        ax.plot(np.clip(-k * y, -1, 1), y, color=col, ls=ls, lw=1.8, label=lab)
    ax.axvline(0, color=INK, lw=0.6)
    ax.set_xlabel(r"Stress, $\sigma/\sigma_Y$"); ax.set_ylabel("Height, y/c")
    ax.legend(fontsize=6.5, loc="lower left"); ax.set_xlim(-1.25, 1.25)
    ax.set_title("(a) Plastic zones grow inward", fontsize=8.5, loc="left")
    ax = axs[1]
    k = np.linspace(0, 8, 400)
    Mm = np.where(k <= 1, k, 1.5 * (1 - 1 / (3 * np.maximum(k, 1) ** 2)))
    ax.plot(k, Mm, color=THEORY, lw=1.8, label="EPP rectangle")
    ax.plot(k, k, color=DIM, ls=DASH, lw=0.9, label=r"elastic, $M = EI\kappa$")
    ax.axhline(1.5, color=DIM, lw=0.8, ls=(0, (1, 2))); ax.text(3.8, 1.57, r"$M_p = 1.5M_Y$", fontsize=7.5, color=DIM)
    k0 = 3.0; M0 = 1.5 * (1 - 1 / 27)
    ax.plot([k0, k0 - M0], [M0, 0], color=NUMERIC, ls=DASH, lw=1.2); ax.text(2.5, 0.6, "unloading", fontsize=7, color=NUMERIC)
    ax.set_xlim(0, 8); ax.set_ylim(0, 1.8)
    ax.set_xlabel(r"Curvature, $\kappa/\kappa_Y$"); ax.set_ylabel(r"Moment, $M/M_Y$")
    ax.legend(fontsize=6.3, loc="lower right")
    ax.set_title("(b) Moment–curvature", fontsize=8.5, loc="left")
    ax = axs[2]
    load = np.clip(-3 * y, -1, 1)
    res = load + M0 * y
    ax.plot(load, y, color=THEORY, lw=1.6)
    ax.plot(M0 * y, y, color=DIM, ls=DASH, lw=1.0)
    ax.plot(res, y, color=FOURTH, ls=(0, (1.2, 2.4)), lw=1.8)
    ax.text(-1.07, 0.65, "loaded", fontsize=6.8, color=THEORY, ha="right")
    ax.text(0.62, -0.05, "residual", fontsize=6.8, color=FOURTH)
    ax.text(1.0, 0.45, "unloading", fontsize=6.8, color=DIM)
    ax.axvline(0, color=INK, lw=0.6)
    ax.set_xlabel(r"$\sigma/\sigma_Y$"); ax.set_ylabel("Height, y/c")
    ax.set_xlim(-2.0, 2.0)
    ax.set_title(r"(c) Residual stress, from $3\kappa_Y$", fontsize=8.5, loc="left")
    return save(fig, FIG / "fig5_plastic", title="Figure 5. Plastic bending of a rectangular section (normalized)",
                alt=("Three normalized plots for an elastic–perfectly plastic rectangle. (a) Stress through the depth at curvatures of "
                     "one, two and eight times the yield curvature: linear in an elastic core and flat at plus or minus the yield "
                     "stress in outer plastic zones that grow toward the neutral axis. (b) Moment over yield moment versus curvature "
                     "over yield curvature: linear up to one, then curving toward 1.5, the fully plastic moment; an unloading line "
                     "from three times the yield curvature has the elastic slope and leaves a permanent curvature. (c) Residual stress "
                     "after unloading from three times the yield curvature: the loaded stress plus the elastic unloading stress, "
                     "which leaves tension near the top, compression just inside it, and the reverse below the neutral axis."))


def fig4_details():
    fig, axs = new_fig("full", 2.5, ncols=2, gridspec_kw=dict(wspace=0.35))
    ax = axs[0]
    ax.set_xlim(-1.6, 1.6); ax.set_ylim(-1.3, 1.5); ax.set_aspect("equal"); ax.axis("off")
    xs = np.linspace(-1, 1, 50)
    top = 0.76 - 0.12 * xs ** 2
    bot = -0.64 - 0.12 * xs ** 2
    ax.add_patch(Polygon(np.c_[np.r_[xs * 1.08, xs[::-1] * 0.92], np.r_[top, bot[::-1]]], fc=MEMBER_FILL, ec=INK))
    ax.plot([-1, 1, 1, -1, -1], [0.7, 0.7, -0.7, -0.7, 0.7], color=DIM, ls=DASH, lw=0.8)
    arrow(ax, 0.6, 1.05, 1.2, 1.05, color=THIRD, lw=1.0, ms=6); arrow(ax, -0.6, 1.05, -1.2, 1.05, color=THIRD, lw=1.0, ms=6)
    ax.text(0, 1.2, "top (compressed) widens", ha="center", fontsize=7, color=THIRD)
    ax.text(0, -1.15, "bottom (stretched) narrows", ha="center", fontsize=7, color=THIRD)
    ax.text(0, 0.0, r"transverse radius $\rho/\nu$", ha="center", fontsize=7.5)
    ax.set_title("(a) Anticlastic curvature (§4.3)", fontsize=8.5, loc="left")
    ax = axs[1]
    ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis("off")
    ax.add_patch(Rectangle((0.8, 1.0), 1.4, 4.0, fc=MEMBER_FILL, ec=INK))
    ax.add_patch(Rectangle((2.6, 3.0), 1.2, 2.0, fc=THEORY, alpha=0.25, ec=THEORY)); ax.add_patch(Rectangle((2.6, 1.0), 1.2, 2.0, fc=NUMERIC, alpha=0.25, ec=NUMERIC))
    ax.text(2.3, 0.4, "rectangle: Z/S = 1.5", ha="center", fontsize=7.5)
    ax.add_patch(Rectangle((5.6, 4.6), 2.2, 0.4, fc=MEMBER_FILL, ec=INK)); ax.add_patch(Rectangle((5.6, 1.0), 2.2, 0.4, fc=MEMBER_FILL, ec=INK))
    ax.add_patch(Rectangle((6.55, 1.4), 0.3, 3.2, fc=MEMBER_FILL, ec=INK))
    ax.add_patch(Rectangle((8.2, 3.0), 1.2, 2.0, fc=THEORY, alpha=0.25, ec=THEORY)); ax.add_patch(Rectangle((8.2, 1.0), 1.2, 2.0, fc=NUMERIC, alpha=0.25, ec=NUMERIC))
    ax.text(7.5, 0.4, "I-section: Z/S ≈ 1.1–1.2", ha="center", fontsize=7.5)
    ax.text(5.0, 5.6, r"fully plastic stress blocks, $\pm\sigma_Y$", ha="center", fontsize=7.5, color=DIM)
    ax.set_title("(b) Shape factor", fontsize=8.5, loc="left")
    return save(fig, FIG / "fig4_details", title="Figure 4. Anticlastic curvature and the shape factor",
                alt=("Two panels. (a) A rectangular cross-section of a beam bent with positive moment: the compressed top widens and "
                     "the stretched bottom narrows because of Poisson's effect, so the section curves the other way with a transverse "
                     "radius of rho over nu. (b) Fully plastic stress blocks of plus and minus the yield stress next to a rectangle and "
                     "an I-section: the rectangle's plastic moment is 1.5 times its yield moment, while the I-section, whose material "
                     "is already concentrated in the flanges, gains only about 10 to 20 percent."))


if __name__ == "__main__":
    entries = [f() for f in (fig1_setup, fig2_vm, fig3_flexure, fig4_details, fig5_plastic)]
    write_alt_text(entries, FIG / "ALT_TEXT.md", "Lab 4: Bending")
    print("wrote", [e["file"] for e in entries])

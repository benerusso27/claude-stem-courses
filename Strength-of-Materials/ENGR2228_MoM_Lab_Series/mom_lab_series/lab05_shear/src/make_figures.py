"""Lab 5 figures (series style). Writes ../figures/*.svg, *.png and ALT_TEXT.md.
Plots are normalized or use generic sections so the handout does not give away results."""
import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "shared"))
sys.path.insert(0, str(HERE))
from figstyle import (DASH, DASHDOT, DIM, DOT, FAIL, FOURTH, INK, LOAD, MEMBER_FILL, NUMERIC, REACT, THEORY, THIRD, arrow,  # noqa: E402
                      dim_line, new_fig, save, write_alt_text)
from matplotlib.patches import Circle, Polygon, Rectangle  # noqa: E402

import lab05_model as LM  # noqa: E402
from lab05_analysis import newmark_point  # noqa: E402

FIG = HERE.parent / "figures"


def _sketch(ax, xlim, ylim):
    ax.set_xlim(*xlim); ax.set_ylim(*ylim); ax.set_aspect("equal"); ax.axis("off"); ax.grid(False)


def _supports(ax, x1, x2, y):
    ax.add_patch(Polygon([[x1, y], [x1 - 0.35, y - 0.6], [x1 + 0.35, y - 0.6]], fc="#BFBFBF", ec=INK, lw=0.8))
    ax.add_patch(Circle((x2, y - 0.3), 0.3, fc="#BFBFBF", ec=INK, lw=0.8))


def _chevron(ax, x, y, s=0.32, color=THEORY):
    ax.plot([x - s, x + s], [y - s, y + s], color=color, lw=1.6)
    ax.plot([x - s, x + s], [y + s, y - s], color=color, lw=1.6)


def fig1_setup():
    fig, axs = new_fig("full", 2.6, ncols=3, gridspec_kw=dict(wspace=0.05))
    # (a) Part A
    ax = axs[0]; _sketch(ax, (0, 10), (-1.5, 7))
    ax.add_patch(Rectangle((0.6, 2.0), 8.8, 1.6, fc=MEMBER_FILL, ec=INK, lw=1.1))
    _supports(ax, 1.0, 9.0, 2.0)
    arrow(ax, 5.0, 5.0, 5.0, 3.65, color=LOAD, ms=10); ax.text(5.25, 4.6, "P", color=LOAD, fontstyle="italic", fontsize=9)
    _chevron(ax, 3.0, 2.8)
    ax.text(2.4, 4.5, "±45° pair\nat mid-height", ha="center", fontsize=6.8, color=THEORY)
    dim_line(ax, 1.0, 0.6, 9.0, 0.6, "400 mm", offset=(0, -0.45), fs=7)
    dim_line(ax, 1.0, 1.35, 3.0, 1.35, "100", offset=(0, -0.35), fs=6.5)
    ax.add_patch(Rectangle((6.6, 4.9), 0.6, 1.2, fc=MEMBER_FILL, ec=INK)); ax.plot([6.6, 7.2], [5.5, 5.5], "o", color=THEORY, ms=3)
    ax.add_patch(Rectangle((8.0, 5.2), 1.2, 0.6, fc=MEMBER_FILL, ec=INK)); ax.plot([8.0, 9.2], [5.5, 5.5], "o", color=THEORY, ms=3)
    ax.text(6.9, 4.35, "upright", ha="center", fontsize=6.5); ax.text(8.6, 4.35, "flat", ha="center", fontsize=6.5)
    ax.set_title("(a) Part A: bar, two orientations", fontsize=8.5, loc="left")
    # (b) Part B
    ax = axs[1]; _sketch(ax, (0, 10), (-1.5, 7))
    ax.add_patch(Rectangle((0.6, 1.8), 8.8, 2.2, fc=MEMBER_FILL, ec=INK, lw=1.1))
    ax.plot([0.6, 9.4], [3.65, 3.65], color=INK, lw=0.7); ax.plot([0.6, 9.4], [2.15, 2.15], color=INK, lw=0.7)
    _supports(ax, 1.0, 9.0, 1.8)
    arrow(ax, 5.0, 5.4, 5.0, 4.05, color=LOAD, ms=10); ax.text(5.25, 5.0, "P", color=LOAD, fontstyle="italic", fontsize=9)
    for yy in (2.9, 3.25, 3.5):
        _chevron(ax, 2.6, yy, s=0.13)
    ax.text(2.4, 4.7, "web pairs at\nthree heights", ha="center", fontsize=6.8, color=THEORY)
    ax.plot([1.0, 9.0], [1.2, 1.2], color=THIRD, lw=1.2); ax.plot([1.0, 1.0], [1.2, 1.8], color=THIRD, lw=1.0); ax.plot([9.0, 9.0], [1.2, 1.8], color=THIRD, lw=1.0)
    ax.add_patch(Rectangle((4.75, 1.25), 0.5, 0.5, fc="white", ec=THIRD))
    ax.text(5.0, 0.55, "LVDT on a yoke", ha="center", fontsize=6.8, color=THIRD)
    dim_line(ax, 1.0, -0.2, 9.0, -0.2, "span L = 300–1200 mm", offset=(0, -0.45), fs=7)
    ax.set_title("(b) Part B: I-beam", fontsize=8.5, loc="left")
    # (c) Part C
    ax = axs[2]; _sketch(ax, (0, 10.1), (-1.6, 7))
    ax.add_patch(Rectangle((0.6, 2.6), 8.8, 0.8, fc=MEMBER_FILL, ec=INK, lw=1.1))
    ax.add_patch(Rectangle((0.6, 1.8), 8.8, 0.8, fc=MEMBER_FILL, ec=INK, lw=1.1))
    for x in np.linspace(1.67, 8.33, 6):
        ax.plot([x, x], [1.7, 3.5], color=THIRD, lw=1.4)
    _supports(ax, 1.0, 9.0, 1.8)
    arrow(ax, 5.0, 5.0, 5.0, 3.45, color=LOAD, ms=10); ax.text(5.25, 4.6, "P", color=LOAD, fontstyle="italic", fontsize=9)
    ax.add_patch(Rectangle((9.55, 2.75), 0.45, 0.5, fc="white", ec=FOURTH)); ax.plot([9.4, 9.55], [3.0, 3.0], color=FOURTH, lw=1.2)
    ax.text(8.6, 4.4, "end-slip\ndial gage", ha="center", fontsize=6.8, color=FOURTH)
    ax.text(5.0, 0.5, "loose · six bolts · bonded", ha="center", fontsize=7)
    dim_line(ax, 1.0, -0.6, 9.0, -0.6, "600 mm", offset=(0, -0.45), fs=7)
    ax.set_title("(c) Part C: two bars", fontsize=8.5, loc="left")
    return save(fig, FIG / "fig1_setup", title="Figure 1. The three test set-ups",
                alt=("Three schematic panels. (a) Part A: the 25.4 by 50.8 millimeter aluminum bar on supports 400 millimeters apart "
                     "with a central load P; a plus-and-minus 45 degree gage pair sits at mid-height on the face, 100 millimeters from "
                     "the left support. Small insets show the bar upright and flat, with the gage pairs at the middle of the two side "
                     "faces in each orientation. (b) Part B: an aluminum I-beam with a central load over spans from 300 to 1200 "
                     "millimeters; gage pairs on the web at three heights, and a displacement transducer on a yoke that spans the "
                     "supports and reads the midspan deflection of the bottom flange. (c) Part C: two 50.8 by 12.7 millimeter bars "
                     "stacked, over a 600 millimeter span with a central load, tested loose, joined by six bolts, and bonded; a dial "
                     "gage at the left end reads the slip between the bars."))


def fig2_shearflow():
    fig, axs = new_fig("full", 2.7, ncols=3, gridspec_kw=dict(wspace=0.45, width_ratios=[1.5, 1, 1]))
    ax = axs[0]; _sketch(ax, (-0.5, 10.5), (0, 8))
    ax.add_patch(Rectangle((2.8, 1.0), 4.4, 5.6, fc=MEMBER_FILL, ec=INK, lw=1.0))
    ax.add_patch(Rectangle((2.8, 5.0), 4.4, 1.6, fc=THEORY, alpha=0.15, ec="none"))
    ax.plot([2.8, 7.2], [5.0, 5.0], color=INK, lw=1.0, ls=DASH)
    ax.plot([2.8, 7.2], [3.8, 3.8], color=DIM, lw=0.6, ls=DOT); ax.text(7.35, 3.7, "NA", fontsize=6.8, color=DIM)
    for yy in (5.25, 5.8, 6.35):
        L1 = 0.35 + 0.55 * (yy - 3.8) / 2.8; L2 = L1 * 1.5
        arrow(ax, 2.8, yy, 2.8 - L1 * 1.4, yy, color=THIRD, lw=1.0, ms=6)
        arrow(ax, 7.2, yy, 7.2 + L2 * 1.4, yy, color=THIRD, lw=1.0, ms=6)
    arrow(ax, 6.4, 5.0, 3.6, 5.0, color=LOAD, lw=1.4, ms=8)
    ax.text(2.65, 4.45, r"$\Delta H = q\,\Delta x$", ha="right", fontsize=7, color=LOAD)
    ax.text(0.3, 7.0, r"$M$", fontsize=8, color=THIRD); ax.text(8.6, 7.0, r"$M + \Delta M$", fontsize=8, color=THIRD)
    ax.text(5.0, 5.7, r"$A'$, $\bar y'$", ha="center", fontsize=8, color=THEORY)
    dim_line(ax, 2.8, 0.5, 7.2, 0.5, r"$\Delta x$", offset=(0, -0.35), fs=8)
    ax.set_title("(a) Part above a cut", fontsize=8.5, loc="left")
    u = np.linspace(-1, 1, 201)
    ax = axs[1]
    ax.plot(1 - u ** 2, u, color=THEORY, lw=1.8)
    ax.axvline(0, color=INK, lw=0.6); ax.axhline(0, color=DIM, lw=0.6, ls=DASH)
    ax.set_xlabel(r"$\tau\,/\,\tau_{max}$"); ax.set_ylabel("Height, y/c"); ax.set_xlim(-0.05, 1.2)
    ax.text(0.06, 0.25, r"$\tau_{max} = 3V/2A$", fontsize=7.5)
    ax.set_title("(b) Rectangle", fontsize=8.5, loc="left")
    ax = axs[2]
    H, B, tf, tw = 1.0, 0.75, 0.0625, 0.047
    lay = LM.ibeam(B, H, tf, tw); pr = LM.props(lay)
    ys = np.r_[np.linspace(0, tf, 30), np.linspace(tf, H - tf, 120), np.linspace(H - tf, H, 30)]
    bs = np.r_[np.full(30, B), np.full(120, tw), np.full(30, B)]
    Qs = np.array([LM.Q_at(lay, y, pr["ybar"]) for y in ys])
    tau = Qs / bs
    tau /= tau.max()
    ax.plot(tau, (ys - H / 2) / (H / 2), color=THEORY, lw=1.8)
    ax.axhline((H / 2 - tf) / (H / 2), color=DIM, lw=0.6, ls=DOT); ax.axhline(-(H / 2 - tf) / (H / 2), color=DIM, lw=0.6, ls=DOT)
    ax.axvline(0, color=INK, lw=0.6)
    ax.text(0.05, 0.93, "flange", fontsize=6.8, color=DIM); ax.text(0.25, 0.25, "web: nearly\nuniform", fontsize=6.8, color=DIM)
    ax.set_xlabel(r"$\tau\,/\,\tau_{max}$"); ax.set_ylabel("Height, y/c"); ax.set_xlim(-0.05, 1.2)
    ax.set_title("(c) I-section", fontsize=8.5, loc="left")
    return save(fig, FIG / "fig2_shearflow", title="Figure 2. Horizontal shear and the shearing-stress distribution",
                alt=("Three panels. (a) A short length delta x of a beam, cut horizontally above the neutral axis. The normal stresses "
                     "on the part above the cut are larger on the right face, where the moment is M plus delta M, than on the left, so "
                     "a horizontal force delta H equal to q times delta x must act on the cut; the shaded area above the cut is A prime "
                     "with its centroid at y bar prime. (b) In a rectangle the shearing stress varies as a parabola through the depth, "
                     "zero at the top and bottom and largest, 3V over 2A, at the neutral axis. (c) In an I-section the stress is small "
                     "in the flanges, jumps up where the width drops to the web thickness, and is nearly uniform across the web."))


def fig3_measure():
    fig, axs = new_fig("full", 2.6, ncols=2, gridspec_kw=dict(wspace=0.35, width_ratios=[1, 1.3]))
    ax = axs[0]; _sketch(ax, (-3, 3), (-2.4, 2.6))
    sq = np.array([[-1, -1], [1, -1], [1, 1], [-1, 1], [-1, -1]])
    ax.plot(sq[:, 0], sq[:, 1], color=DIM, lw=0.9, ls=DASH)
    g = 0.35
    rh = np.array([[-1 - g, -1], [1 - g, -1], [1 + g, 1], [-1 + g, 1], [-1 - g, -1]])
    ax.add_patch(Polygon(rh[:-1], fc=MEMBER_FILL, ec=INK, lw=1.0))
    ax.plot([-1 - g, 1 + g], [-1, 1], color=THEORY, lw=1.6); ax.plot([1 - g, -1 + g], [-1, 1], color=NUMERIC, lw=1.6, ls=DASH)
    ax.text(1.45, 0.3, "+45°:\nlonger", fontsize=7, color=THEORY); ax.text(-2.95, 0.3, "−45°:\nshorter", fontsize=7, color=NUMERIC)
    arrow(ax, -1.2, 1.35, 1.2, 1.35, color=LOAD, lw=1.0, ms=7); arrow(ax, 1.2, -1.35, -1.2, -1.35, color=LOAD, lw=1.0, ms=7)
    ax.text(0, 1.65, r"$\tau_{xy} > 0$ shown", ha="center", fontsize=7, color=LOAD)
    ax.text(0, -2.1, r"$\gamma_{xy} = \varepsilon(+45°) - \varepsilon(-45°)$", ha="center", fontsize=8)
    ax.set_title("(a) A gage pair measures γ", fontsize=8.5, loc="left")
    ax = axs[1]
    xi = np.linspace(-1, 1, 81)
    for bh, col, ls in ((0.25, FOURTH, DOT), (0.5, THEORY, "-"), (1.0, THIRD, DASHDOT), (2.0, NUMERIC, DASH)):
        r = [LM.rect_edge_ratio_xseries(bh, 1.0, 0.3, x_over_b=x / 2, M=20000) for x in xi]
        ax.plot(xi, r, color=col, ls=ls, lw=1.7, label=f"b/h = {bh:g}")
    ax.axhline(1.0, color=INK, lw=0.6)
    ax.set_xlabel("Position across the width, z/(b/2)"); ax.set_ylabel(r"$\tau\,/\,(VQ/Ib)$ on the NA")
    ax.legend(fontsize=6.8, loc="upper center", ncol=2); ax.set_ylim(0.7, 1.75)
    ax.text(0.0, 0.76, "ν = 0.3", ha="center", fontsize=7, color=DIM)
    ax.set_title("(b) Wide sections: τ is not uniform", fontsize=8.5, loc="left")
    return save(fig, FIG / "fig3_measure", title="Figure 3. Measuring shear strain, and shearing stress across the width",
                alt=("Two panels. (a) A square element in pure shear distorts into a rhombus; one diagonal lengthens and the other "
                     "shortens by half the shear strain, so a pair of gages at plus and minus 45 degrees measures the shear strain as "
                     "the difference of their readings, and the axial strain from bending cancels. (b) Shearing stress on the neutral "
                     "axis divided by the elementary value VQ over Ib, plotted across the width of rectangles with b over h of 0.25, 0.5, "
                     "1 and 2 for Poisson's ratio 0.3: narrow sections are nearly uniform, but as the section gets wider the stress "
                     "rises at the faces and falls at the center while its average stays equal to the elementary value."))


def fig4_timoshenko():
    fig, axs = new_fig("full", 2.6, ncols=2, gridspec_kw=dict(wspace=0.32, width_ratios=[1, 1.3]))
    ax = axs[0]; _sketch(ax, (0, 10), (0, 8))
    ax.add_patch(Rectangle((0.5, 3.8), 3.4, 1.6, fc=MEMBER_FILL, ec=INK)); ax.text(2.2, 5.9, "bending", ha="center", fontsize=7.5)
    th = 0.25
    ax.add_patch(Polygon([[5.4, 3.8], [8.6, 3.8 - 3.2 * th], [8.6, 5.4 - 3.2 * th], [5.4, 5.4]], fc=MEMBER_FILL, ec=INK))
    ax.plot([5.4, 8.6], [4.6, 4.6], color=DIM, lw=0.6, ls=DASH)
    ax.annotate("", xy=(8.6, 4.6 - 3.2 * th), xytext=(8.6, 4.6), arrowprops=dict(arrowstyle="->", color=LOAD, lw=1.0))
    ax.text(8.8, 4.1, "γ", fontsize=9, color=LOAD); ax.text(7.0, 5.9, "shear", ha="center", fontsize=7.5)
    ax.text(5.0, 2.3, r"shear strain $\gamma = f_s V/(GA)$ tilts the axis", ha="center", fontsize=7)
    ax.text(5.0, 1.3, r"$\delta = \delta_{bending} + \delta_{shear}$", ha="center", fontsize=8)
    ax.set_title("(a) Two ways a beam deflects", fontsize=8.5, loc="left")
    ax = axs[1]
    Lh = np.logspace(0, np.log10(50), 200)
    nu = 0.3
    for name, f, col, ls in (("rectangle", 12 * 1.2 * 2 * (1 + nu) / 12, THEORY, "-"), ("typical I-section", None, NUMERIC, DASH)):
        if f is None:
            lay = LM.ibeam(0.75, 1.0, 0.0625, 0.047); pr = LM.props(lay); fs = LM.form_factor(lay)
            f = 12 * fs * 2 * (1 + nu) * pr["I"] / pr["A"]          # 12 f_s E I/(G A h^2), h = 1
        ax.plot(Lh, 1 + f / Lh ** 2, color=col, ls=ls, lw=1.8, label=name)
    ax.axhline(1 / 0.95, color=DIM, lw=0.8, ls=DOT); ax.text(1.1, 1.1, "shear = 5 % of δ", fontsize=7, color=DIM, ha="left")
    ax.set_xscale("log"); ax.set_yscale("log"); ax.set_ylim(0.95, 30); ax.set_xlim(1, 50)
    ax.set_xlabel("Span-to-depth ratio, L/h"); ax.set_ylabel(r"$\delta\,/\,\delta_{bending}$")
    ax.legend(fontsize=7, loc="upper right")
    ax.set_title("(b) Simple span, central load", fontsize=8.5, loc="left")
    return save(fig, FIG / "fig4_timoshenko", title="Figure 4. Shear deformation",
                alt=("Two panels. (a) A beam segment deforms in two ways: in bending its cross-sections rotate but stay normal to the "
                     "axis; in shear they slide past each other, so the axis tilts by the shear strain gamma equal to f s V over GA. The "
                     "deflection is the sum of the two. (b) Log-log plot of the total deflection divided by the bending-only deflection "
                     "against span-to-depth ratio for a simply supported beam with a central load, for a rectangle and for a typical "
                     "I-section, Poisson's ratio 0.3. Both curves approach 1 for long spans and rise steeply for short ones; the "
                     "I-section's curve lies well above the rectangle's, so it needs a longer span before shear falls below 5 percent of "
                     "the deflection, marked by a horizontal line."))


def fig5_layered():
    fig, axs = new_fig("full", 2.7, ncols=3, gridspec_kw=dict(wspace=0.5))
    ax = axs[0]
    y = np.linspace(0, 2, 201)
    loose = np.where(y < 1, -(y - 0.5), -(y - 1.5))
    bonded = -(y - 1.0) / 2 * 1
    ax.plot(loose, y, color=THIRD, ls=DASHDOT, lw=1.6, label="loose")
    ax.plot(bonded, y, color=THEORY, lw=1.8, label="bonded")
    part = np.where(y < 1, 0.18 - 0.8 * (y - 0.5), -0.18 - 0.8 * (y - 1.5))
    ax.plot(part, y, color=NUMERIC, ls=DASH, lw=1.6, label="partial")
    ax.axhline(1, color=DIM, lw=0.6, ls=DOT); ax.axvline(0, color=INK, lw=0.6)
    ax.set_xlabel(r"Strain $\varepsilon_x$ at midspan (scaled)"); ax.set_ylabel("Height (layer thicknesses)")
    ax.legend(fontsize=6.5, loc="upper right"); ax.set_xlim(-0.75, 0.75)
    ax.text(-0.72, 1.04, "interface", fontsize=6.5, color=DIM)
    ax.set_title("(a) Strain: slip at the interface", fontsize=8.5, loc="left")
    ax = axs[1]
    x = np.linspace(0, 1, 201)
    for aL, col, ls, lab in ((0.0, THIRD, DASHDOT, "loose"), (5.0, NUMERIC, DASH, "αL = 5"), (20.0, FOURTH, DOT, "αL = 20")):
        if aL == 0:
            s = (0.25 - np.minimum(x, 1 - x) ** 2) * np.where(x < 0.5, -1, 1)
        else:
            u = np.minimum(x, 1 - x)
            s = (1 - np.cosh(aL * u) / np.cosh(aL / 2)) * np.where(x < 0.5, -1, 1) * 2 / aL ** 2
        ax.plot(x, s / 0.25, color=col, ls=ls, lw=1.7, label=lab)
    ax.axhline(0, color=INK, lw=0.6)
    ax.set_xlabel("Position, x/L"); ax.set_ylabel("Slip / loose end slip")
    ax.legend(fontsize=6.5, loc="upper left")
    ax.set_title("(b) Slip along the beam", fontsize=8.5, loc="left")
    ax = axs[2]
    geom = LM.two_layer(1.0, 0.5, 0.5, 1.0)
    c1 = 1 / geom["EAs"] + geom["r"] ** 2 / geom["EI0"]
    aLs = np.logspace(-1, 2.3, 200)
    ratio = []
    for aL in aLs:
        k = (aL / 1.0) ** 2 / c1
        d, _ = newmark_point(geom, 1.0, k)
        ratio.append((1 / 48) / (d * geom["EI0"]))
    ax.plot(aLs, ratio, color=THEORY, lw=1.8)
    ax.axhline(4, color=DIM, lw=0.6, ls=DOT); ax.axhline(1, color=DIM, lw=0.6, ls=DOT)
    ax.text(0.12, 3.75, "bonded: 4", fontsize=7, color=DIM); ax.text(15, 1.1, "loose: 1", fontsize=7, color=DIM)
    ax.set_xscale("log"); ax.set_xlabel(r"Connection parameter, $\alpha L$"); ax.set_ylabel(r"$EI_{eff}\,/\,EI_0$")
    ax.set_ylim(0.8, 4.3)
    ax.set_title("(c) Two equal layers", fontsize=8.5, loc="left")
    return save(fig, FIG / "fig5_layered", title="Figure 5. Built-up beams: loose, partially connected and bonded",
                alt=("Three panels for a beam made of two equal layers with a central load. (a) Strain through the depth at midspan: "
                     "loose layers bend separately, each with its own neutral axis, so the strain jumps at the interface; a bonded beam "
                     "has one straight strain line through the whole depth; a partially connected beam lies in between, with a smaller "
                     "jump. (b) Slip between the layers along the span, divided by the loose end slip: largest at the supports and zero "
                     "at midspan, and much smaller and confined near the supports as the connection parameter alpha L grows. (c) "
                     "Effective bending stiffness divided by the loose value against alpha L on a log scale: it rises from 1 for a "
                     "loose stack to 4 for a fully bonded one, with most of the gain between alpha L of about 1 and 30."))


if __name__ == "__main__":
    entries = [f() for f in (fig1_setup, fig2_shearflow, fig3_measure, fig4_timoshenko, fig5_layered)]
    write_alt_text(entries, FIG / "ALT_TEXT.md", "Lab 5: Transverse Shear")
    print("wrote", [e["file"] for e in entries])

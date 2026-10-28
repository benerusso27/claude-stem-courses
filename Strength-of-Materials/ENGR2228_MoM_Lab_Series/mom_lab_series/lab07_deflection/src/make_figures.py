"""Lab 7 figures (series style). Writes ../figures/*.svg, *.png and ALT_TEXT.md.
Beer's convention: y up, deflections drawn downward for downward loads. Plots are normalized so that the handout does
not give away the results."""
import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "shared"))
sys.path.insert(0, str(HERE))
from figstyle import (DASH, DASHDOT, DIM, DOT, FAIL, FOURTH, INK, LOAD, MEMBER_FILL, NUMERIC, THEORY, THIRD, arrow,  # noqa: E402
                      dim_line, new_fig, save, write_alt_text)
from matplotlib.patches import Circle, Polygon, Rectangle  # noqa: E402

import lab07_model as LM  # noqa: E402

FIG = HERE.parent / "figures"


def _sketch(ax, xlim, ylim):
    ax.set_xlim(*xlim); ax.set_ylim(*ylim); ax.set_aspect("equal"); ax.axis("off"); ax.grid(False)


def _knife(ax, x, y, s=0.35):
    ax.add_patch(Polygon([[x, y], [x - s, y - 1.6 * s], [x + s, y - 1.6 * s]], closed=True, fc="#BFBFBF", ec=INK, lw=0.8))


def _indicator(ax, x, y, h=0.9):
    ax.add_patch(Rectangle((x - 0.32, y + 0.25), 0.64, h, fc="white", ec=THIRD, lw=1.0, zorder=6))
    ax.plot([x, x], [y, y + 0.25], color=THIRD, lw=1.2, zorder=6)


def _hanger(ax, x, y, n=2, color=LOAD):
    ax.plot([x, x], [y, y - 0.9], color=color, lw=1.0)
    for i in range(n):
        ax.add_patch(Rectangle((x - 0.35, y - 1.15 - 0.3 * i), 0.7, 0.26, fc=color, ec=INK, lw=0.5, alpha=0.85))


def fig1_setup():
    fig, axs = new_fig("full", 2.7, ncols=3, gridspec_kw=dict(width_ratios=[1.15, 1.0, 0.95], wspace=0.06))
    # (a) Part A
    ax = axs[0]; _sketch(ax, (-0.6, 10.6), (-3.3, 4.2))
    ax.add_patch(Rectangle((0, 0), 10, 0.35, fc=MEMBER_FILL, ec=INK, lw=1.0))
    _knife(ax, 0.5, 0); _knife(ax, 9.5, 0)
    for xg in (2.75, 5.0, 7.25):
        _indicator(ax, xg, 0.35)
    _hanger(ax, 2.75, 0.0, 2); _hanger(ax, 7.25, 0.0, 3)
    ax.text(5.0, 1.75, "digital indicators", ha="center", fontsize=6.8, color=THIRD)
    ax.text(5.0, -2.2, "hangers at 200 and 600 mm", ha="center", fontsize=6.8, color=LOAD)
    dim_line(ax, 0.5, -2.9, 9.5, -2.9, "800 mm", offset=(0, 0.3), fs=7)
    ax.set_title("(a) Part A: simple span", fontsize=8.5, loc="left")
    # (b) Part B
    ax = axs[1]; _sketch(ax, (-1.2, 10.2), (-3.6, 4.2))
    ax.add_patch(Rectangle((-1.0, -1.0), 1.0, 2.4, fc="white", ec=DIM, hatch="////", lw=0.8))
    ax.add_patch(Rectangle((-0.2, 0.35), 1.2, 0.5, fc="#BFBFBF", ec=INK, lw=0.8))
    ax.add_patch(Rectangle((-0.2, -0.5), 1.2, 0.5, fc="#BFBFBF", ec=INK, lw=0.8))
    ax.add_patch(Rectangle((0, 0), 8.6, 0.35, fc=MEMBER_FILL, ec=INK, lw=1.0))
    ax.add_patch(Circle((8.3, -0.3), 0.3, fc="#BFBFBF", ec=INK, lw=0.8))
    ax.add_patch(Rectangle((7.85, -1.6), 0.9, 1.0, fc="white", ec=FOURTH, lw=1.0))
    ax.text(8.9, -1.1, "load\ncell", ha="left", va="center", fontsize=6.6, color=FOURTH)
    _indicator(ax, 4.6, 0.35); _indicator(ax, 8.3, 0.35)
    _hanger(ax, 4.6, 0.0, 3)
    ax.text(0.4, 1.6, "clamp", fontsize=6.8, ha="center")
    dim_line(ax, 0.6, 2.8, 8.3, 2.8, "700 mm", offset=(0, 0.3), fs=7)
    ax.text(3.6, -2.9, "B1: no prop, load at 700 mm\nB2, B3: prop, load at 350 mm", ha="center", fontsize=6.3)
    ax.set_title("(b) Part B: clamp and prop", fontsize=8.5, loc="left")
    # (c) Part C
    ax = axs[2]; _sketch(ax, (-1.4, 8.6), (-6.4, 2.0))
    for gx in np.arange(0, 8.01, 1.0):
        ax.plot([gx, gx], [-6.2, 1.2], color="#D9D9D9", lw=0.5)
    for gy in np.arange(-6, 1.01, 1.0):
        ax.plot([-0.2, 8.2], [gy, gy], color="#D9D9D9", lw=0.5)
    ax.add_patch(Rectangle((-1.2, -0.6), 1.2, 1.2, fc="#BFBFBF", ec=INK, lw=0.8))
    a = 3.0
    th, dv, xt, sol = LM.elastica_bvp(a, 0.0)
    s = np.linspace(0, 1, 60)
    xy = sol.sol(s)
    Lp = 7.0
    ax.plot(xy[2] * Lp, xy[3] * Lp, color=INK, lw=2.4)
    ax.plot([0, Lp], [0, 0], color=DIM, lw=0.8, ls=DASH)
    xtp, ytp = xy[2][-1] * Lp, xy[3][-1] * Lp
    ax.plot([xtp, xtp], [ytp, ytp - 0.9], color=LOAD, lw=1.0)
    ax.add_patch(Rectangle((xtp - 0.3, ytp - 1.4), 0.6, 0.5, fc=LOAD, ec=INK, lw=0.5))
    ax.annotate("", xy=(xtp, 0.0), xytext=(xtp, ytp), arrowprops=dict(arrowstyle="<|-|>", color=THEORY, lw=0.8, mutation_scale=7))
    ax.text(xtp + 0.15, ytp / 2, "δv", color=THEORY, fontsize=7)
    ax.annotate("", xy=(xtp, 0.6), xytext=(Lp, 0.6), arrowprops=dict(arrowstyle="<|-|>", color=THEORY, lw=0.8, mutation_scale=7))
    ax.text((xtp + Lp) / 2, 0.9, "δh", color=THEORY, fontsize=7, ha="center")
    ax.text(4.0, -6.0, "grid board behind the strip", ha="center", fontsize=6.6, color=DIM)
    ax.set_title("(c) Part C: thin strip, large deflection", fontsize=8.5, loc="left")
    return save(fig, FIG / "fig1_setup", title="Figure 1. Test set-ups for Lab 7",
                alt=("Three schematic panels. (a) Part A: a steel bar resting on two knife edges 800 millimeters apart, with three digital "
                     "indicators touching its top at 200, 400 and 600 millimeters, and load hangers at 200 and 600 millimeters. (b) Part B: "
                     "the same bar clamped at its left end; a roller prop sitting on a load cell supports it 700 millimeters from the clamp; "
                     "indicators read the deflection at 350 and 700 millimeters; a hanger at 350 millimeters loads it. Without the prop, "
                     "the hanger is moved to 700 millimeters and the bar is a cantilever. (c) Part C: a thin spring-steel strip clamped in a "
                     "vise and bent far down by a weight hanging from its tip, in front of a grid board; the vertical deflection delta v and "
                     "the inward movement of the tip delta h are marked."))


def fig2_superposition():
    fig, axs = new_fig("full", 2.6, ncols=2, gridspec_kw=dict(wspace=0.28))
    ax = axs[0]
    L, EI = 1.0, 1.0
    x = np.linspace(0, L, 301)
    b = dict(family="ss", L=L, EI=EI, P=[(1.0, 0.75), (0.5, 0.25)])
    cf = LM.closed_form(b, x)
    s = 48 / (1.0 * L ** 3)
    for (lab, yy), col, ls in zip(cf["comps"], (THIRD, FOURTH), (DASHDOT, DOT)):
        ax.plot(x, yy * s, color=col, ls=ls, lw=1.4, label=f"load {'P at 0.75L' if '0.75' in lab else 'P/2 at 0.25L'} alone")
    ax.plot(x, cf["y"] * s, color=THEORY, lw=2, label="both loads: the sum")
    ax.axhline(0, color=DIM, lw=0.6)
    ax.set_xlabel("x / L"); ax.set_ylabel("y · 48EI / (PL³)")
    ax.legend(fontsize=6.6, loc="lower left")
    ax.set_title("(a) Simple span: deflections add", fontsize=8.5, loc="left")
    ax = axs[1]
    b = dict(family="propped", L=L, EI=EI, P=[(1.0, 0.5)])
    cf = LM.closed_form(b, x)
    s = 48 / (1.0 * L ** 3)
    yP = LM.cant_point(1.0, 0.5, EI, x)[0]
    R = cf["R"]["RB"]
    yR = R * x ** 2 * (3 * L - x) / (6 * EI)
    ax.plot(x, yP * s, color=THIRD, ls=DASHDOT, lw=1.4, label="cantilever with the load")
    ax.plot(x, yR * s, color=FOURTH, ls=DOT, lw=1.4, label="cantilever with the prop force R")
    ax.plot(x, cf["y"] * s, color=THEORY, lw=2, label="sum: y = 0 at the prop")
    ax.axhline(0, color=DIM, lw=0.6)
    ax.plot([1.0], [0.0], "o", mfc="white", mec=INK, ms=6)
    ax.set_xlabel("x / L"); ax.set_ylabel("y · 48EI / (PL³)")
    ax.legend(fontsize=6.6, loc="lower left")
    ax.set_title("(b) Propped cantilever: the redundant R", fontsize=8.5, loc="left")
    return save(fig, FIG / "fig2_superposition", title="Figure 2. Superposition of elastic curves",
                alt=("Two plots of nondimensional deflection along a beam. (a) A simple span with a load P at three quarters of the span "
                     "and a load P over 2 at one quarter: the two single-load elastic curves, dash-dot and dotted, add up to the solid "
                     "curve for both loads. (b) A propped cantilever with a central load: the cantilever bends down under the load alone "
                     "and up under the prop force alone; the prop force is the value that makes the sum zero at the prop."))


def fig3_clamp():
    fig, axs = new_fig("full", 2.6, ncols=2, gridspec_kw=dict(width_ratios=[0.9, 1.1], wspace=0.25))
    ax = axs[0]; _sketch(ax, (-1.6, 10.0), (-3.2, 2.6))
    ax.add_patch(Rectangle((-1.4, -1.4), 1.0, 2.8, fc="white", ec=DIM, hatch="////", lw=0.8))
    th = np.linspace(-1.2, 1.2, 40)
    ax.plot(-0.4 + 0.55 * np.cos(th * 1.3), 0.55 * np.sin(th * 1.3), color=THIRD, lw=1.6)
    ax.text(0.15, 0.85, "k", color=THIRD, fontsize=9, fontstyle="italic")
    x = np.linspace(0, 8, 50)
    k_rot = 0.04
    yb = -0.06 * x ** 2 * (24 - x) / 48 * 1.0
    ax.plot(x, np.zeros_like(x), color=DIM, lw=0.8, ls=DASH)
    ax.plot(x, yb, color=THEORY, lw=2.2)
    ax.plot(x, yb - k_rot * x, color=NUMERIC, lw=2.0, ls=DASH)
    ax.text(8.2, yb[-1] + 0.05, "rigid", color=THEORY, fontsize=6.8, va="center")
    ax.text(8.2, yb[-1] - k_rot * 8 - 0.2, "flexible", color=NUMERIC, fontsize=6.8, va="center")
    arrow(ax, 8.0, 1.6, 8.0, 0.25, color=LOAD, ms=9)
    ax.text(8.15, 1.2, "P", color=LOAD, fontstyle="italic", fontsize=8.5)
    ax.annotate("", xy=(3.2, -k_rot * 3.2), xytext=(3.2, 0.0), arrowprops=dict(arrowstyle="-", color=DIM, lw=0.6))
    ax.text(-1.4, -2.7, "M$_A$ = k θ$_A$: the clamp turns by θ$_A$\nand the whole beam tilts with it", fontsize=6.6)
    ax.set_title("(a) A clamp as a rotational spring", fontsize=8.5, loc="left")
    ax = axs[1]
    lam = np.logspace(-3, 1.5, 200)                      # EI / (k L)
    rP = [LM.closed_form(dict(family="propped", L=1.0, EI=1.0, P=[(1.0, 0.5)], k=1.0 / l), [0.5])["R"]["RB"] for l in lam]
    rW = [LM.closed_form(dict(family="propped", L=1.0, EI=1.0, w=1.0, k=1.0 / l), [0.5])["R"]["RB"] for l in lam]
    ax.semilogx(lam, rP, color=THEORY, label="central load P: R$_B$ / P")
    ax.semilogx(lam, rW, color=NUMERIC, ls=DASH, label="uniform load w: R$_B$ / (wL)")
    for v, t in ((5 / 16, "5/16"), (3 / 8, "3/8"), (0.5, "1/2 (clamp → pin)")):
        ax.axhline(v, color=DIM, lw=0.7, ls=DOT)
        ax.text(1.3e-3, v + 0.006, t, fontsize=6.4, color=DIM)
    ax.set_xlabel("Clamp flexibility EI / (kL)"); ax.set_ylabel("Prop reaction, normalized")
    ax.set_ylim(0.28, 0.54)
    ax.legend(fontsize=6.6, loc="lower right")
    ax.set_title("(b) Propped cantilever: the prop takes more", fontsize=8.5, loc="left")
    return save(fig, FIG / "fig3_clamp", title="Figure 3. A real clamp is not perfectly fixed",
                alt=("Two panels. (a) A cantilever held by a clamp drawn as a rotational spring of stiffness k. With a rigid clamp the beam "
                     "leaves the wall horizontally; with a flexible clamp the wall end rotates by an angle equal to the wall moment divided "
                     "by k, and the whole beam tilts further down. (b) The prop reaction of a propped cantilever against the clamp flexibility "
                     "EI over k L on a logarithmic axis: with a central load it rises from five sixteenths of P for a "
                     "rigid clamp to one half of P when the clamp becomes a pin; under a uniform load it rises from three eighths of w L to "
                     "one half."))


def fig4_elastica():
    fig, axs = new_fig("full", 2.7, ncols=2, gridspec_kw=dict(wspace=0.28))
    ax = axs[0]
    for a, col in ((0.5, THEORY), (1.5, NUMERIC), (3.0, THIRD), (6.0, FOURTH)):
        _, _, _, sol = LM.elastica_bvp(a, 0.0)
        s = np.linspace(0, 1, 80)
        xy = sol.sol(s)
        ax.plot(xy[2], xy[3], color=col, lw=1.8, label=f"α = {a:g}")
        xl = np.linspace(0, 1, 40)
        yl = -a * xl ** 2 * (3 - xl) / 6
        m = yl > -1.2
        ax.plot(xl[m], yl[m], color=col, lw=0.9, ls=DOT)
    ax.set_aspect("equal")
    ax.set_xlim(-0.02, 1.08); ax.set_ylim(-1.05, 0.08)
    ax.set_xlabel("x / L"); ax.set_ylabel("y / L")
    ax.legend(fontsize=6.6, loc="lower left", title="solid: elastica; dotted: linear", title_fontsize=6.4)
    ax.set_title("(a) Shapes at increasing load", fontsize=8.5, loc="left")
    ax = axs[1]
    al = np.linspace(0.01, 8, 200)
    dv = np.array([LM.elastica_closed(a)[1] for a in al])
    dh = np.array([1 - LM.elastica_closed(a)[2] for a in al])
    a5 = LM.elastica_p5()
    ax.axvspan(a5, 8, color=FAIL, alpha=0.15, lw=0)
    ax.text(a5 + 0.15, 1.02, "linear theory off by > 5 %", fontsize=6.6, color="#8A5300")
    ax.plot(al, dv, color=THEORY, label="δ_v / L, elastica")
    ax.plot(al, dh, color=THEORY, ls=DASH, lw=1.4, label="δ_h / L (tip moves inward)")
    ax.plot([0, 3.3], [0, 1.1], color=THIRD, ls=DASHDOT, label="linear theory, α/3")
    ax.set_xlim(0, 8); ax.set_ylim(0, 1.1)
    ax.set_xlabel("α = PL² / EI"); ax.set_ylabel("Tip displacement / L")
    ax.legend(fontsize=6.6, loc="lower right")
    ax.set_title("(b) Tip displacement", fontsize=8.5, loc="left")
    return save(fig, FIG / "fig4_elastica", title="Figure 4. Large deflection of a cantilever (the elastica)",
                alt=("Two panels. (a) The deflected shape of a cantilever with a vertical tip load for load parameters alpha of 0.5, 1.5, "
                     "3 and 6, drawn to equal scales: solid curves are the exact large-deflection shape, which keeps the strip's length so "
                     "the tip swings inward, and dotted curves are linear theory, which keeps every point at its original x and runs far "
                     "below the exact curves at the larger loads. (b) The vertical tip deflection over L and the inward tip movement over L "
                     "against alpha: the vertical deflection follows the linear-theory line alpha over 3 at first and then bends over, "
                     "approaching L slowly; a shaded band marks loads above about alpha = 0.68, where linear theory overstates the "
                     "deflection by more than 5 percent."))


def main():
    entries = [fig1_setup(), fig2_superposition(), fig3_clamp(), fig4_elastica()]
    write_alt_text(entries, FIG / "ALT_TEXT.md", "Lab 7: Deflection of Beams")
    print("wrote", [e["file"] for e in entries])


if __name__ == "__main__":
    main()

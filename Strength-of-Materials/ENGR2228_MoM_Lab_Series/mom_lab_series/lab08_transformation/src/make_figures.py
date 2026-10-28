"""Lab 8 figures (series style). Writes ../figures/*.svg, *.png and ALT_TEXT.md.
Beer's conventions: tension positive; Mohr's circle "clockwise above" (X plotted at (sigma_x, -tau_xy)); theta
counterclockwise. Mohr's circles are drawn without numbers so that the handout does not give away the results."""
import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "shared"))
sys.path.insert(0, str(HERE))
from figstyle import (DASH, DASHDOT, DIM, DOT, FAIL, FOURTH, INK, LOAD, MEMBER_FILL, NUMERIC, THEORY, THIRD, arrow,  # noqa: E402
                      dim_line, new_fig, save, write_alt_text)
from matplotlib.patches import Arc, Circle, Ellipse, Polygon, Rectangle  # noqa: E402

import lab08_model as LM  # noqa: E402

FIG = HERE.parent / "figures"
DO, DI = 38.1e-3, 31.75e-3


def _sketch(ax, xlim, ylim):
    ax.set_xlim(*xlim); ax.set_ylim(*ylim); ax.set_aspect("equal"); ax.axis("off"); ax.grid(False)


def _rosette(ax, x, y, s, rot=0.0, color=INK, lab=True, fs=6.5):
    """Rectangular rosette at (x, y): grids a (along local x), b (45 deg), c (90 deg); local x drawn at angle rot."""
    for k, (ang, name) in enumerate(((0, "a"), (45, "b"), (90, "c"))):
        t = math.radians(ang) + rot
        ux, uy = math.cos(t), math.sin(t)
        nx, ny = -uy, ux
        a0, a1, w = 0.25 * s, 0.95 * s, 0.11 * s
        ax.add_patch(Polygon([[x + ux * a0 + nx * w, y + uy * a0 + ny * w], [x + ux * a1 + nx * w, y + uy * a1 + ny * w],
                              [x + ux * a1 - nx * w, y + uy * a1 - ny * w], [x + ux * a0 - nx * w, y + uy * a0 - ny * w]],
                             closed=True, fc="white", ec=color, lw=0.8, zorder=7))
        if lab:
            ax.text(x + ux * (a1 + 0.22 * s), y + uy * (a1 + 0.22 * s), name, fontsize=fs, ha="center", va="center", color=color, zorder=8)


def fig1_setup():
    fig, axs = new_fig("full", 2.9, ncols=3, gridspec_kw=dict(width_ratios=[1.55, 0.95, 0.85], wspace=0.12))
    # (a) elevation seen from the lever side
    ax = axs[0]; _sketch(ax, (-1.4, 11.2), (-3.7, 3.4))
    ax.add_patch(Rectangle((-1.0, -1.6), 1.0, 3.2, fc="white", ec=DIM, lw=0.8, hatch="////"))
    ax.text(-0.5, 1.9, "clamp", fontsize=7, ha="center")
    ax.add_patch(Rectangle((0, -0.55), 9.0, 1.1, fc=MEMBER_FILL, ec=INK, lw=1.0))
    ax.plot([0, 9], [0, 0], color=DIM, lw=0.6, ls=(0, (8, 3, 1.5, 3)))
    ax.add_patch(Rectangle((9.0, -0.75), 0.35, 1.5, fc="#BFBFBF", ec=INK, lw=0.8))           # end plug and lever hub
    ax.add_patch(Circle((9.6, 0), 0.32, fc="white", ec=INK, lw=1.0, zorder=5))                # lever seen end-on (toward viewer)
    ax.plot([9.6], [0], "o", color=INK, ms=2.2, zorder=6)
    arrow(ax, 9.6, -0.35, 9.6, -2.1, color=LOAD, lw=1.6)
    ax.text(9.85, -1.6, "F", color=LOAD, fontsize=8, fontweight="bold")
    ax.text(9.7, 1.0, "lever (toward\nthe viewer)", fontsize=6.2, ha="center", va="bottom", color=DIM)
    xg = 3.2
    ax.plot([xg, xg], [-1.25, 0.55], color=DIM, lw=0.6, ls=(0, (2, 2)))
    _rosette(ax, xg - 0.15, -0.42, 0.62, rot=0, color=THIRD, lab=False)
    ax.text(xg + 0.75, -0.35, "K", color=THIRD, fontsize=8, fontweight="bold")
    ax.add_patch(Rectangle((xg - 0.25, 0.55), 0.5, 0.14, fc=THIRD, ec=THIRD))
    ax.text(xg, 0.95, "H (on top)", color=THIRD, fontsize=7, ha="center")
    dim_line(ax, xg, -2.75, 9.6, -2.75, "$L_b$ = 250 mm", offset=(0, -0.38), fs=7)
    # pump
    ax.add_patch(Rectangle((-1.25, -3.5), 1.6, 0.65, fc="white", ec=FOURTH, lw=0.9))
    ax.text(-0.45, -3.17, "pump", fontsize=6.2, ha="center", va="center", color=FOURTH)
    ax.plot([0.35, 1.0, 1.0], [-3.17, -3.17, -0.55], color=FOURTH, lw=0.9)
    ax.text(1.1, -2.2, "p (Part C)", fontsize=6.4, color=FOURTH)
    ax.set_title("(a) Side view, from the lever side", fontsize=8, loc="left")
    # (b) section at the gage section, seen from the free end
    ax = axs[1]; _sketch(ax, (-3.4, 2.0), (-3.4, 2.6))
    ro, ri = 1.25, 1.25 * DI / DO
    ax.add_patch(Circle((0, 0), ro, fc=MEMBER_FILL, ec=INK, lw=1.0)); ax.add_patch(Circle((0, 0), ri, fc="white", ec=INK, lw=0.8))
    ax.plot([0, -2.9], [0, 0], color=INK, lw=2.2)                                             # lever toward +Z = left in this view
    arrow(ax, -2.9, -0.1, -2.9, -1.9, color=LOAD, lw=1.6)
    ax.text(-2.75, -1.6, "F", color=LOAD, fontsize=8, fontweight="bold")
    dim_line(ax, 0, 1.75, -2.9, 1.75, "$a_L$ = 200 mm", offset=(0, 0.3), fs=6.8)
    ax.plot([0, 0], [1.3, 1.85], color=DIM, lw=0.5); ax.plot([-2.9, -2.9], [0.1, 1.85], color=DIM, lw=0.5)
    ax.plot([0], [ro], "s", color=THIRD, ms=4); ax.text(0.15, ro + 0.18, "H", color=THIRD, fontsize=7.5, fontweight="bold")
    ax.plot([-ro], [-0.0], "s", color=THIRD, ms=4); ax.text(-ro - 0.1, -0.42, "K", color=THIRD, fontsize=7.5, fontweight="bold", ha="right")
    ax.annotate("", xy=(1.55 * math.cos(math.radians(200)), 1.55 * math.sin(math.radians(200))), xytext=(1.55 * math.cos(math.radians(330)), 1.55 * math.sin(math.radians(330))),
                arrowprops=dict(arrowstyle="-|>", color=THEORY, lw=0.9, connectionstyle="arc3,rad=-0.55", mutation_scale=8))
    ax.text(1.05, -1.75, "T", color=THEORY, fontsize=8, fontweight="bold")
    ax.text(-0.4, -3.2, "φ from H toward K", fontsize=6.4, color=DIM, ha="center")
    ax.set_title("(b) Section from the free end", fontsize=8, loc="left")
    # (c) rosette and local axes at H, seen from above (outside)
    ax = axs[2]; _sketch(ax, (-1.9, 2.4), (-2.2, 2.6))
    arrow(ax, -1.2, -1.2, 1.9, -1.2, color=DIM, lw=0.9, ms=8); ax.text(1.95, -1.42, "x (along the tube)", fontsize=6.2, color=DIM, ha="right", va="top")
    arrow(ax, -1.2, -1.2, -1.2, 1.9, color=DIM, lw=0.9, ms=8); ax.text(-1.1, 2.0, "y (90° ccw from x,\nseen from outside)", fontsize=6.2, color=DIM, va="bottom")
    _rosette(ax, -0.55, -0.55, 1.75, rot=0, color=INK, fs=8)
    ax.add_patch(Arc((-0.55, -0.55), 1.4, 1.4, theta1=0, theta2=45, color=DIM, lw=0.7))
    ax.text(0.35, -0.08, "45°", fontsize=6.4, color=DIM)
    ax.set_title("(c) Rosette", fontsize=8, loc="left")
    return save(fig, FIG / "fig1_setup", title="Figure 1. Test set-up",
                alt=("Three panels. (a) Side view of the 6061-T6 tube clamped at its left end, with a lever at the free end pointing toward "
                     "the viewer and a downward load F at the lever's tip; the gage section is 250 mm (L_b) from the load line, with "
                     "rosette K on the near side at mid-height and rosette H on top; a hand pump connects to the end plug for Part C. "
                     "(b) The cross-section seen from the free end: the lever extends 200 mm (a_L) to the left, which is the K side, the "
                     "load F hangs from its tip, and the torque T acts about the tube's axis; H is at the top, K at the left, and the "
                     "angle phi is measured from H toward K. (c) The rectangular rosette: gage a along the tube axis x, gage b at 45 "
                     "degrees and gage c at 90 degrees counterclockwise from x, with the local y axis 90 degrees counterclockwise from x "
                     "as seen from outside the tube."))


def _mohr(ax, sx, sy, t, s3=None, label=("σ", "τ"), pts=None, show_xy=True, title=None, thetaS=None):
    m = LM.principal2(sx, sy, t)
    ave, R = (sx + sy) / 2, math.hypot((sx - sy) / 2, t)
    s1, s2 = ave + R, ave - R
    lo, hi = min(s2, 0 if s3 is None else s3, 0), max(s1, 0 if s3 is None else s3, 0)
    if s3 is not None:
        for u, v in ((s1, s3), (s2, s3)):
            ax.add_patch(Circle(((u + v) / 2, 0), abs(u - v) / 2, fill=False, ec=DIM, lw=0.8, ls=DASH))
    ax.add_patch(Circle((ave, 0), R, fill=False, ec=THEORY, lw=1.6))
    span = hi - lo
    ax.axhline(0, color=INK, lw=0.6); ax.axvline(0, color=INK, lw=0.6)
    ax.set_xlim(lo - 0.12 * span, hi + 0.12 * span)
    big = max(R, (hi - lo) / 2)
    ax.set_ylim(-1.18 * big, 1.25 * big); ax.set_aspect("equal"); ax.axis("off")
    ax.text(hi + 0.11 * span, 0.06 * big, label[0], fontsize=8, ha="right", va="bottom")
    ax.text(0.03 * span, 1.18 * big, f"{label[1]}, clockwise ↑", fontsize=6.8, va="top")
    if show_xy:
        X, Y = (sx, -t), (sy, t)
        ax.plot(*zip(X, Y), color=DIM, lw=0.8)
        ax.plot(*X, "o", color=INK, ms=3.5); ax.plot(*Y, "o", color=INK, ms=3.5)
        ax.text(X[0] + 0.03 * span, X[1] + 0.04 * big, "X", fontsize=7.5, fontweight="bold")
        ax.text(Y[0] + 0.03 * span, Y[1] + 0.04 * big, "Y", fontsize=7.5, fontweight="bold")
        th0 = math.degrees(math.atan2(-t, sx - ave))
        ax.add_patch(Arc((ave, 0), 0.5 * R, 0.5 * R, theta1=min(0, th0), theta2=max(0, th0), color=NUMERIC, lw=0.9))
        ax.text(ave + 0.3 * R * math.cos(math.radians(th0 / 2)), 0.3 * R * math.sin(math.radians(th0 / 2)) + (0.05 * big if th0 > 0 else -0.12 * big), "2θ$_p$", fontsize=6.6, color=NUMERIC)
    ax.plot([s1, s2], [0, 0], "o", color=THEORY, ms=3)
    ax.text(s1 + 0.02 * span, -0.14 * big, "A (σ$_{max}$)", fontsize=6.4, color=THEORY)
    ax.text(s2 - 0.02 * span, -0.14 * big, "B", fontsize=6.4, color=THEORY, ha="right")
    ax.plot([ave], [R], "o", color=THEORY, ms=2.5); ax.text(ave + 0.02 * span, R + 0.04 * big, "D", fontsize=6.4, color=THEORY)
    for (x, y, name) in pts or []:
        ax.plot(x, y, "o", mfc="white", mec=INK, ms=5, mew=1.1, zorder=6)
        ax.plot([x, x], [0, y], color=INK, lw=0.6, ls=(0, (2, 2)))
        ax.text(x + 0.025 * span, y + 0.05 * big, name, fontsize=7, fontweight="bold")
    if title:
        ax.set_title(title, fontsize=8, loc="left")


def fig2_mohr():
    fig, axs = new_fig("full", 2.7, ncols=2, gridspec_kw=dict(wspace=0.08))
    s = LM.tube_state(DO, DI, 600, 0.2, 0.25, 0, 0.0)
    _mohr(axs[0], s["sx"], s["sy"], s["txy"], title="(a) Stress at H, load on the lever")
    E, nu = 68.9e9, 0.33
    ex, ey, g = LM.state_strains(s["sx"], s["sy"], s["txy"], E, nu)
    ave, R = (ex + ey) / 2, math.hypot((ex - ey) / 2, g / 2)
    thp = 0.5 * math.atan2(g / 2, (ex - ey) / 2)
    pts = []
    for ang, nm in ((0, "a"), (45, "b"), (90, "c")):
        a2 = 2 * math.radians(ang) - 2 * thp
        pts.append((ave + R * math.cos(a2), R * math.sin(a2), nm))
    _mohr(axs[1], ex, ey, g / 2, label=("ε", "γ/2"), pts=pts, show_xy=False, title="(b) Strain at H: the three gage readings")
    b = math.radians(8)
    for ang, nm in ((0, "a′"), (45, "b′"), (90, "c′")):
        a2 = 2 * (math.radians(ang) + b) - 2 * thp
        x, y = ave + R * math.cos(a2), R * math.sin(a2)
        axs[1].plot(x, y, "s", mfc="white", mec=NUMERIC, ms=4.2, mew=1.0, zorder=6)
        axs[1].text(x - 0.06 * R, y - 0.22 * R, nm, fontsize=6.6, color=NUMERIC)
    return save(fig, FIG / "fig2_mohr", title="Figure 2. Mohr's circles at the top of the tube",
                alt=("Two Mohr's circles drawn to equal scales, without numbers. (a) Stress at point H with the load on the lever: point X, "
                     "for the face normal to the tube axis, lies to the right of the origin and above the sigma axis because its shear "
                     "stress turns the element clockwise; point Y lies at the origin's abscissa, below the axis; the circle crosses the "
                     "sigma axis at A (sigma max, tensile) and B (slightly compressive), and the angle 2 theta p from CX to CA is marked. "
                     "(b) The corresponding Mohr's circle for strain (epsilon against gamma over 2): the readings of gages a, b and c are "
                     "the abscissas of three points on the circle at twice their angles from the x axis; squares a-prime, b-prime and "
                     "c-prime show the same rosette turned by 8 degrees, whose points slide around the same circle, so the principal "
                     "strains do not change but each reading does."))


def fig3_threeD():
    fig, axs = new_fig("full", 2.6, ncols=2, gridspec_kw=dict(wspace=0.08))
    s = LM.tube_state(DO, DI, 600, 0.2, 0.25, 0, 0.0)
    _mohr(axs[0], s["sx"], s["sy"], s["txy"], s3=0.0, show_xy=False, title="(a) Lever load only: σ$_{max}$ > 0 > σ$_{min}$")
    s = LM.tube_state(DO, DI, 600, 0.2, 0.25, 8e6, 0.0)
    _mohr(axs[1], s["sx"], s["sy"], s["txy"], s3=0.0, show_xy=False, title="(b) With internal pressure: both tensile")
    for ax, st in zip(axs, (LM.tube_state(DO, DI, 600, 0.2, 0.25, 0, 0.0), LM.tube_state(DO, DI, 600, 0.2, 0.25, 8e6, 0.0))):
        ave, R = (st["sx"] + st["sy"]) / 2, math.hypot((st["sx"] - st["sy"]) / 2, st["txy"])
        s1, s2 = ave + R, ave - R
        top = max(s1, 0) / 2 + min(s2, 0) / 2
        rabs = (max(s1, 0) - min(s2, 0)) / 2
        ax.annotate("", xy=(ave, R), xytext=(ave, 0), arrowprops=dict(arrowstyle="-|>", color=THEORY, lw=0.8, mutation_scale=7))
        ax.text(ave + 0.03 * rabs, 0.45 * R, "in-plane\nτ$_{max}$", fontsize=6.2, color=THEORY)
        if rabs > R * 1.01:
            ax.annotate("", xy=(top, rabs), xytext=(top, 0), arrowprops=dict(arrowstyle="-|>", color=THIRD, lw=0.9, mutation_scale=7))
            ax.text(top - 0.05 * rabs, 0.62 * rabs, "absolute\nτ$_{max}$", fontsize=6.2, color=THIRD, ha="right")
        ax.text(0, -0.2 * rabs, "O (σ$_r$ = 0)", fontsize=6.2, color=DIM, ha="center", va="top")
    return save(fig, FIG / "fig3_threeD", title="Figure 3. Three-dimensional Mohr's circles at H",
                alt=("Two sets of three Mohr's circles for point H, without numbers. In each, the solid circle is the in-plane circle "
                     "through A and B, and the two dashed circles join A and B to the origin O, which represents the zero radial stress at "
                     "the free surface. (a) Lever load only: A is tensile and B is slightly compressive, so the origin lies inside the "
                     "in-plane circle and the in-plane maximum shear is also the absolute maximum. (b) With internal pressure added: both A "
                     "and B are tensile, the origin lies outside the in-plane circle, and the largest circle runs from O to A; the absolute "
                     "maximum shear (its radius, sigma max over 2) is about one and a half times the in-plane value."))


def fig4_thick():
    fig, axs = new_fig("full", 2.45, ncols=2, gridspec_kw=dict(wspace=0.32))
    ax = axs[0]
    ro, ri = DO / 2, DI / 2
    r = np.linspace(ri, ro, 200)
    st = np.array([LM.lame_closed(1.0, ri, ro, x)[1] for x in r])
    sr = np.array([LM.lame_closed(1.0, ri, ro, x)[0] for x in r])
    ax.plot((r - ri) / (ro - ri), st, color=THEORY, label="σ$_θ$/p, Lamé")
    ax.plot((r - ri) / (ro - ri), sr, color=THEORY, ls=DASH, lw=1.3, label="σ$_r$/p, Lamé")
    ax.plot([0, 1], [ri / (ro - ri)] * 2, color=THIRD, ls=DASHDOT, label="p r$_i$/t (thin wall)")
    ax.plot([1], [st[-1]], "o", mfc="white", mec=INK, ms=5, label="gage (outer surface)")
    ax.set_xlabel("Position through the wall, (r − r$_i$)/t"); ax.set_ylabel("Stress / p")
    ax.set_xlim(-0.03, 1.03); ax.legend(fontsize=6.4, loc="center right")
    ax.set_title("(a) Through the wall of the lab tube", fontsize=8, loc="left")
    ax = axs[1]
    k = np.linspace(1.02, 2.0, 200)
    err = (k + 1) / 2 - 1                                           # (ro + ri)/(2 ri) - 1 with k = ro/ri
    ax.axhspan(0.05, 1.0, color=FAIL, alpha=0.15, lw=0)
    ax.text(1.03, 0.4, "thin wall off by > 5 % at the gages", fontsize=6.4, color="#8A5300")
    ax.plot(k, err, color=THEORY, label="p r$_i$/t vs Lamé at r$_o$")
    ax.plot(k, (k + 1) / (k ** 2 + 1) - 1, color=THEORY, ls=DASH, lw=1.3, label="vs Lamé at r$_i$")
    ax.set_xlabel("r$_o$/r$_i$"); ax.set_ylabel("Relative error of p r$_i$/t")
    ax.set_xlim(1.0, 2.0); ax.set_ylim(-0.45, 0.55)
    ax.legend(fontsize=6.4, loc="lower left")
    ax.set_title("(b) Error of the thin-wall formula", fontsize=8, loc="left")
    return save(fig, FIG / "fig4_thick", title="Figure 4. Thin-wall and thick-wall hoop stress",
                alt=("Two panels. (a) Hoop and radial stress divided by the pressure across the wall of the lab tube: the Lame hoop stress "
                     "falls from about 5.5 at the inner surface to about 4.5 at the outer surface, the radial stress rises from minus 1 to "
                     "zero, and the thin-wall value p r_i/t is a horizontal line at 5.0, equal to the average of the hoop stress; an open "
                     "circle marks the outer surface, where the gages are. (b) The relative error of p r_i/t against the radius ratio "
                     "r_o/r_i from 1 to 2: compared with the Lame value at the outer surface the thin-wall formula is high by half of "
                     "(r_o/r_i minus 1), 10 percent for the lab tube; compared with the inner surface it is low; a shaded band marks errors "
                     "above 5 percent."))


def main():
    entries = [fig1_setup(), fig2_mohr(), fig3_threeD(), fig4_thick()]
    write_alt_text(entries, FIG / "ALT_TEXT.md", "Lab 8: Transformation of Stress and Strain")
    print("wrote", [e["file"] for e in entries])


if __name__ == "__main__":
    main()

"""Lab 9 figures (series style). Writes ../figures/*.svg, *.png and ALT_TEXT.md.
Beer's column conventions (Sec. 10.1, Fig. 10.7): x runs down the column from the top end A, y is the lateral
deflection; P is a compressive magnitude. Curves come from lab09_model.py; plots that would give away the students'
results are drawn in nondimensional form."""
import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "shared"))
sys.path.insert(0, str(HERE))
from figstyle import (DASH, DASHDOT, DIM, DOT, FAIL, FOURTH, INK, LOAD, MEMBER_FILL, THEORY, THIRD, arrow,  # noqa: E402
                      dim_line, new_fig, save, write_alt_text)
from matplotlib.patches import Circle, Polygon, Rectangle  # noqa: E402

import lab09_model as LM  # noqa: E402

FIG = HERE.parent / "figures"
PI = math.pi
E_AL, SY_AL, M_RO = 68.9e9, 273.7e6, 17


def _sketch(ax, xlim, ylim):
    ax.set_xlim(*xlim); ax.set_ylim(*ylim); ax.set_aspect("equal"); ax.axis("off"); ax.grid(False)


def _hatch(ax, x, y, w, h):
    ax.add_patch(Rectangle((x, y), w, h, fc="white", ec=DIM, lw=0.8, hatch="////", zorder=1))


def _pin(ax, x, y, up=True, s=0.32):
    """Knife edge / pin: a small circle on a triangle (pointing toward the column)."""
    d = -1 if up else 1
    ax.add_patch(Polygon([[x, y], [x - s, y + d * 1.4 * s], [x + s, y + d * 1.4 * s]], closed=True, fc="white", ec=INK, lw=0.9, zorder=4))
    ax.add_patch(Circle((x, y), 0.09, fc="white", ec=INK, lw=0.9, zorder=5))


def fig1_setup():
    fig, axs = new_fig("full", 3.6, ncols=3, gridspec_kw=dict(width_ratios=[1.25, 1.0, 0.8], wspace=0.08))
    # (a) elevation of the strut frame, pinned ends
    ax = axs[0]; _sketch(ax, (-3.6, 4.6), (-1.6, 12.6))
    _hatch(ax, -2.2, 11.3, 4.4, 0.7)
    ax.add_patch(Rectangle((-0.22, 10.55), 0.44, 0.75, fc="#BFBFBF", ec=INK, lw=0.8))                # screw
    ax.text(0.45, 11.0, "loading screw", fontsize=6.2, ha="left", va="center")
    _hatch(ax, -2.2, -1.2, 4.4, 0.6)
    ax.add_patch(Rectangle((-0.8, -0.6), 1.6, 0.75, fc="white", ec=INK, lw=0.9)); ax.text(0, -0.24, "load cell", fontsize=6, ha="center", va="center")
    # V-block seats and knife edges
    ax.add_patch(Polygon([[-0.6, 10.55], [0.6, 10.55], [0, 10.0]], closed=True, fc="#D9D9D9", ec=INK, lw=0.8))
    ax.add_patch(Polygon([[-0.6, 0.15], [0.6, 0.15], [0, 0.7]], closed=True, fc="#D9D9D9", ec=INK, lw=0.8))
    # bowed bar (exaggerated), bowing to +y (right)
    xs = np.linspace(0, 1, 60)
    yb = 0.55 * np.sin(PI * xs)
    top, bot = 10.0, 0.7
    Y = top - xs * (top - bot)
    w = 0.16
    ax.fill_betweenx(Y, yb - w, yb + w, color=MEMBER_FILL, ec=INK, lw=0.9, zorder=3)
    ax.plot([0, 0], [bot - 0.1, top + 0.1], color=DIM, lw=0.6, ls=(0, (8, 3, 1.5, 3)), zorder=2)
    arrow(ax, -1.0, 11.1, -1.0, 10.25, color=LOAD, lw=1.6); ax.text(-1.2, 10.7, "P", color=LOAD, fontsize=8, fontweight="bold", ha="right")
    ax.text(-0.45, top - 0.1, "A", fontsize=8, ha="right", va="center"); ax.text(-0.45, bot + 0.1, "B", fontsize=8, ha="right", va="center")
    # dial gage at mid-length on the convex (front) side
    ym = (top + bot) / 2
    ax.plot([0.55 + w, 1.6], [ym, ym], color=INK, lw=1.0)
    ax.add_patch(Circle((2.35, ym), 0.75, fc="white", ec=INK, lw=1.0)); ax.plot([2.35, 2.75], [ym, ym + 0.35], color=INK, lw=0.8)
    ax.text(2.35, ym - 1.15, "dial gage\n(mid-length)", fontsize=6.3, ha="center", va="top")
    # strain gages front/back
    for sx, lab in ((0.55 + w, "F"), (0.55 - w, "B")):
        ax.add_patch(Rectangle((sx - 0.07, ym + 0.35), 0.14, 0.7, fc=THIRD, ec=THIRD, zorder=6))
    ax.text(0.55 + w + 0.15, ym + 0.95, "front gage", fontsize=6.0, color=THIRD, ha="left", va="bottom")
    ax.text(0.55 - w - 0.15, ym + 0.95, "back gage", fontsize=6.0, color=THIRD, ha="right", va="bottom")
    dim_line(ax, -2.5, bot, -2.5, top, "L (pivot to pivot)", offset=(-0.42, 0), rotation=90, fs=6.6)
    # Beer's axes
    arrow(ax, 3.1, 10.2, 3.1, 8.9, color=INK, lw=0.9, ms=8); ax.text(3.25, 9.0, "x", fontsize=8, style="italic")
    arrow(ax, 3.1, 10.2, 4.3, 10.2, color=INK, lw=0.9, ms=8); ax.text(4.2, 10.4, "y", fontsize=8, style="italic")
    ax.set_title("(a) Strut frame, pinned ends", fontsize=8, loc="left"); ax.set_anchor("N")
    # (b) end fixtures
    ax = axs[1]; _sketch(ax, (-0.4, 7.6), (-1.0, 9.2))
    # knife-edge holder with three grooves (seen from the side, exaggerated offsets)
    ax.add_patch(Rectangle((0.2, 6.2), 3.2, 1.0, fc="#D9D9D9", ec=INK, lw=0.9))
    for i, gx in enumerate((1.3, 1.8, 2.3)):
        ax.add_patch(Polygon([[gx - 0.18, 6.2], [gx + 0.18, 6.2], [gx, 5.9]], closed=True, fc="white", ec=INK, lw=0.7))
    ax.add_patch(Rectangle((1.3 - 0.16, 3.6), 0.32, 2.3, fc=MEMBER_FILL, ec=INK, lw=0.9))
    ax.plot([1.3, 1.3], [3.4, 6.5], color=DIM, lw=0.5, ls=(0, (8, 3, 1.5, 3)))
    ax.text(1.8, 7.55, "V-grooves at e = 0, 1, 2 mm", fontsize=6.4, ha="center")
    ax.text(1.3, 3.3, "bar end in the\ncentral groove", fontsize=6.0, ha="center", va="top", color=DIM)
    dim_line(ax, 1.3, 7.0, 2.3, 7.0, "", fs=6)
    ax.text(3.55, 6.7, "knife-edge\nholder\n(Parts A, C)", fontsize=6.3, ha="left", va="center")
    # clamp block
    ax.add_patch(Rectangle((4.6, 0.0), 0.65, 2.6, fc="#D9D9D9", ec=INK, lw=0.9))
    ax.add_patch(Rectangle((5.62, 0.0), 0.65, 2.6, fc="#D9D9D9", ec=INK, lw=0.9))
    ax.add_patch(Rectangle((5.25, 0.0), 0.37, 5.2, fc=MEMBER_FILL, ec=INK, lw=0.9, zorder=3))
    for by in (0.6, 2.0):
        ax.plot([4.45, 6.42], [by, by], color=INK, lw=1.2)
    _hatch(ax, 4.2, -0.6, 2.5, 0.6)
    dim_line(ax, 6.7, 0.0, 6.7, 2.6, "40 mm grip", offset=(0.42, 0), rotation=90, fs=6.3)
    ax.text(4.4, 1.2, "clamp block\n(Parts B, D)", fontsize=6.3, ha="right", va="center")
    ax.set_title("(b) End fixtures", fontsize=8, loc="left"); ax.set_anchor("N")
    # (c) section seen along x
    ax = axs[2]; _sketch(ax, (-3.0, 3.6), (-3.6, 4.6))
    tt, bb = 0.9, 3.6
    ax.add_patch(Rectangle((-tt / 2, -bb / 2), tt, bb, fc=MEMBER_FILL, ec=INK, lw=1.0))
    ax.plot([-1.9, 1.9], [0, 0], color=DIM, lw=0.6, ls=(0, (8, 3, 1.5, 3)))
    ax.plot([0, 0], [-2.3, 2.3], color=DIM, lw=0.6, ls=(0, (8, 3, 1.5, 3)))
    ax.add_patch(Rectangle((tt / 2, -0.4), 0.12, 0.8, fc=THIRD, ec=THIRD)); ax.text(tt / 2 + 0.25, -0.75, "F", color=THIRD, fontsize=7, fontweight="bold")
    ax.add_patch(Rectangle((-tt / 2 - 0.12, -0.4), 0.12, 0.8, fc=THIRD, ec=THIRD)); ax.text(-tt / 2 - 0.45, -0.75, "B", color=THIRD, fontsize=7, fontweight="bold")
    arrow(ax, 0.2, 3.25, 2.1, 3.25, color=INK, lw=0.9, ms=8); ax.text(2.2, 3.25, "y", fontsize=8, style="italic", va="center")
    ax.text(0, 3.65, "bows this way", fontsize=6.2, ha="center", va="bottom")
    dim_line(ax, -tt / 2, -2.3, tt / 2, -2.3, "t = 6.35 mm", offset=(0, -0.45), fs=6.4)
    dim_line(ax, -1.5, -bb / 2, -1.5, bb / 2, "b = 25.4 mm", offset=(-0.62, 0), rotation=90, fs=6.4)
    ax.text(0, -3.45, "r = t/√12 (buckles across t)", fontsize=6.2, ha="center")
    ax.set_title("(c) Section, seen along x", fontsize=8, loc="left"); ax.set_anchor("N")
    return save(fig, FIG / "fig1_setup", title="Figure 1. Test set-up",
                alt=("Three panels. (a) The strut frame: a bar stands vertically between two knife edges seated in V-blocks, the upper one under a "
                     "loading screw in the crosshead and the lower one on a load cell. The bar is drawn bowed to the right (exaggerated). "
                     "The load P acts downward at the top end A; B is the bottom end; L is the distance between the pivots. A dial gage "
                     "touches the bar at mid-length on the right (convex, front) side, and strain gages are bonded at mid-length on the "
                     "front and back faces. Beer's axes are shown: x pointing down the column from A and y pointing to the right. "
                     "(b) The end fixtures: a knife-edge holder with three V-grooves at offsets of 0, 1 and 2 mm from the axis, used for "
                     "Parts A and C, and a clamp block that grips 40 mm of the bar between two jaws, used for Part B and Part D. "
                     "(c) The 25.4 by 6.35 mm cross-section seen along the column: it bends across the 6.35 mm thickness t, in the y "
                     "direction, with the front gage F on the convex face and the back gage B on the opposite face; the radius of "
                     "gyration is t over the square root of 12."))


def _shape(ends, k_over=None, n=161):
    """Closed-form first mode on x in [0, 1] (x down from A), scaled to a peak of 1, and the effective-length factor."""
    x = np.linspace(0, 1, n)
    if ends == "pinned":
        y, K = np.sin(PI * x), 1.0
    elif ends == "fixed-pinned":           # top pinned, bottom fixed (Beer Eq. 10.16 with B = 0)
        z = LM.Z_FP
        y, K = np.sin(z * x) - math.sin(z) * x, PI / z
    elif ends == "fixed-fixed":
        y, K = 1 - np.cos(2 * PI * x), 0.5
    elif ends == "free-fixed":
        y, K = 1 - np.sin(PI * x / 2), 2.0
    else:                                  # equal rotational springs, kL/EI = k_over
        P, K = LM.spring_both(1.0, 1.0, k_over)
        p = math.sqrt(P)
        y = 1 - np.cos(p * x) - math.tan(p / 2) * np.sin(p * x)
    y = y / np.max(np.abs(y))
    return x, y, K


def fig2_ends():
    fig, ax = new_fig("full", 3.5)
    _sketch(ax, (-0.6, 15.4), (-4.5, 8.4))
    H, amp = 6.0, 0.62
    cases = [("pinned", "Pinned–pinned", None), ("fixed-pinned", "Pinned top,\nfixed bottom", None), ("fixed-fixed", "Fixed–fixed", None),
             ("free-fixed", "Free top,\nfixed bottom", None), ("springs", "Clamps with\nkL/EI = 45", 45.0)]
    for i, (ends, name, kk) in enumerate(cases):
        x0 = 0.9 + i * 3.05
        x, y, K = _shape(ends, kk)
        Y = H - x * H
        ax.plot([x0, x0], [-0.2, H + 0.2], color=DIM, lw=0.6, ls=(0, (8, 3, 1.5, 3)), zorder=1)
        ax.plot(x0 + amp * y, Y, color=THEORY, lw=1.8, zorder=3)
        # ends
        if ends in ("pinned", "fixed-pinned"):
            _pin(ax, x0, H, up=False)
        if ends in ("fixed-fixed",):
            _hatch(ax, x0 - 0.45, H, 0.9, 0.28)
        if ends == "springs":
            for yy, d in ((H, 1), (0, -1)):
                ax.add_patch(Rectangle((x0 - 0.45, yy if d > 0 else yy - 0.28), 0.9, 0.28, fc="white", ec=FOURTH, lw=0.9, hatch="....", zorder=1))
        if ends == "pinned":
            _pin(ax, x0, 0, up=True)
        if ends in ("fixed-pinned", "fixed-fixed", "free-fixed"):
            _hatch(ax, x0 - 0.45, -0.28, 0.9, 0.28)
        arrow(ax, x0 + (amp * y[0] if ends == "free-fixed" else 0), H + 1.25, x0 + (amp * y[0] if ends == "free-fixed" else 0), H + 0.42, color=LOAD, lw=1.4, ms=9)
        # inflection points (zero moment) and the effective length
        curv = np.gradient(np.gradient(y, x), x)
        infl = [x[j] for j in range(5, len(x) - 5) if curv[j - 1] * curv[j] < 0]
        for xi in infl:
            yi = np.interp(xi, x, y)
            ax.plot([x0 + amp * yi], [H - xi * H], "o", color=THIRD, ms=4, zorder=5)
        xe = x0 + 1.15
        if ends == "free-fixed":
            xm = np.linspace(1, 1.12, 20)
            ym = 1 - np.sin(PI * xm / 2)
            ax.plot(x0 + amp * ym, H - xm * H, color=THEORY, lw=1.1, ls=DASH, zorder=2)
            ax.text(x0 + 0.3, -2.8, "L$_e$ = 2L: with its mirror image\nbelow the base it is a pinned\ncolumn of length 2L", fontsize=6.0, color=THIRD, ha="center", va="top")
        elif ends == "springs":
            pass
        else:
            ends_e = {"pinned": (0, 1), "fixed-pinned": (0, K), "fixed-fixed": (0.25, 0.75)}[ends]
            ya, yb = H - ends_e[0] * H, H - ends_e[1] * H
            ax.plot([xe, xe], [ya, yb], color=THIRD, lw=1.4)
            for yy in (ya, yb):
                ax.plot([xe - 0.12, xe + 0.12], [yy, yy], color=THIRD, lw=1.4)
            ax.text(xe + 0.15, (ya + yb) / 2, "L$_e$", color=THIRD, fontsize=8, va="center")
        ax.text(x0 + 0.3, -1.05, f"{name}\nK = {K:.3g}" if ends != "springs" else f"{name}\nK = {K:.2f}",
                fontsize=7, ha="center", va="top", linespacing=1.2)
    dim_line(ax, -0.35, 0, -0.35, H, "L", offset=(-0.18, 0), fs=7.5)
    ax.text(-0.5, 8.3, "purple dots: zero moment (inflection points); purple brackets: L$_e$", fontsize=6.3, color=THIRD, ha="left", va="top")
    return save(fig, FIG / "fig2_ends", title="Figure 2. End conditions and effective lengths",
                alt=("Five columns of equal length L, each drawn with its first buckling mode computed from this lab's closed-form solutions "
                     "and loaded by P at the top. Purple dots mark points of zero bending moment (inflection points) and purple brackets "
                     "mark the effective length L_e, the length of an equivalent pinned column. Pinned at both ends: a half sine, K = 1. "
                     "Pinned top, fixed bottom: the inflection point lies 0.699 L below the pin, K = 0.699. Fixed at both ends: inflection "
                     "points at the quarter points, K = 0.5. Free top, fixed bottom: the shape continued as its mirror image below the "
                     "base forms a pinned column of length 2 L, K = 2. Clamps of finite stiffness, with k L over EI equal to 45 as in Part B: "
                     "the shape is between the pinned and fixed cases and K = 0.52."))


def fig3_southwell():
    fig, axs = new_fig("full", 2.7, ncols=2, gridspec_kw=dict(wspace=0.32))
    ax = axs[0]
    a = np.linspace(0, 0.985, 400)
    bow = a / (1 - a)                                    # delta / delta0
    ecc = 1 / np.cos(PI / 2 * np.sqrt(a)) - 1           # y_max / e
    ax.plot(bow, a, color=THEORY, label="initial bow δ$_0$: δ/δ$_0$ = α/(1 − α)")
    ax.plot(ecc, a, color=THIRD, ls=DASHDOT, label="load offset e: y$_{max}$/e (Eq. 10.31)")
    ax.plot([0, 0, 20], [0, 1, 1], color=DIM, ls=DASH, lw=1.2, label="perfect column (Euler)")
    ax.set_xlim(0, 20); ax.set_ylim(0, 1.08)
    ax.set_xlabel("Deflection at mid-length ÷ imperfection"); ax.set_ylabel("Load ratio, α = P/P$_{cr}$")
    ax.legend(loc="lower right", fontsize=6.6)
    ax.set_title("(a) Imperfect columns approach P$_{cr}$ but never reach it", fontsize=8, loc="left")
    ax = axs[1]
    al = np.array([0.5, 0.6, 0.7, 0.75, 0.8, 0.85, 0.9, 0.93])
    d = al / (1 - al)                                    # delta/delta0
    yv = d / al                                          # (delta/P) in units of delta0/Pcr
    ax.plot(d, yv, "o", mfc="white", mec=INK, ms=4.5, label="readings (P from 0.5 to 0.93 P$_{cr}$)")
    xx = np.linspace(0, 15, 50)
    ax.plot(xx, xx + 1, color=THEORY, lw=1.4, label="fit: slope 1/P$_{cr}$, intercept δ$_0$/P$_{cr}$")
    ax.annotate("intercept = δ$_0$/P$_{cr}$", xy=(0, 1), xytext=(1.2, 0.25), fontsize=6.8, va="center", arrowprops=dict(arrowstyle="->", color=DIM, lw=0.7))
    ax.annotate("slope = 1/P$_{cr}$", xy=(9, 10), xytext=(9.6, 6.6), fontsize=6.8, arrowprops=dict(arrowstyle="->", color=DIM, lw=0.7))
    ax.set_xlim(0, 15); ax.set_ylim(0, 16)
    ax.set_xlabel("Deflection δ (units of δ$_0$)"); ax.set_ylabel("δ/P (units of δ$_0$/P$_{cr}$)")
    ax.legend(loc="upper left", fontsize=6.6)
    ax.set_title("(b) Southwell plot: a straight line", fontsize=8, loc="left")
    return save(fig, FIG / "fig3_southwell", title="Figure 3. Imperfect columns and the Southwell plot",
                alt=("Two panels in nondimensional form. (a) Load ratio P over P_cr against the mid-length deflection divided by the "
                     "imperfection. A column with an initial bow delta_0 follows alpha over (1 minus alpha), and a column with a load offset "
                     "e follows the secant result (Eq. 10.31); both rise steeply at first and then flatten, approaching P over P_cr = 1 "
                     "without reaching it. The perfect column stays straight up to P_cr and then deflects at constant load (dashed). "
                     "(b) The same bowed-column readings plotted as deflection over load against deflection fall on a straight line whose "
                     "slope is 1 over P_cr and whose intercept is delta_0 over P_cr, so P_cr and the equivalent bow follow from readings "
                     "taken well below the critical load."))


def fig4_eccentric():
    fig, axs = new_fig("full", 2.7, ncols=2, gridspec_kw=dict(wspace=0.32))
    ax = axs[0]
    a = np.linspace(0, 0.95, 300)
    sec = 1 / np.cos(PI / 2 * np.sqrt(a))
    ax.plot(a, sec, color=THEORY, label="secant: (e + y$_{max}$)/e = sec(½π√α)")
    ax.plot(a, 1 / (1 - a), color=FOURTH, ls=DOT, lw=1.8, label="amplification 1/(1 − α)")
    ax.plot(a, np.ones_like(a), color=DIM, ls=DASH, lw=1.2, label="no deflection (Eq. 4.58, Eq. 10.37)")
    ax.set_xlim(0, 1); ax.set_ylim(0, 12)
    ax.set_xlabel("Load ratio, α = P/P$_{cr}$"); ax.set_ylabel("Lever arm at mid-length ÷ e")
    ax.legend(loc="upper left", fontsize=6.6)
    ax.set_title("(a) The moment P(e + y$_{max}$) grows faster than P", fontsize=8, loc="left")
    ax = axs[1]
    r = 1.0
    ecr = np.linspace(0.0, 2.0, 120)
    for sl, col, ls in ((50, THEORY, "-"), (100, THIRD, DASHDOT), (250, FOURTH, DOT)):
        Pcr_A = PI ** 2 * E_AL / sl ** 2                  # P_cr/A
        ratio = []
        for v in ecr:
            e = v * r * r / 1.0                            # ec/r^2 = v with c = 1, r = 1 (nondimensional)
            f = lambda s: s * (1 + v / math.cos(0.5 * math.sqrt(s / E_AL) * sl)) - SY_AL   # noqa: E731
            hi = min(Pcr_A * (1 - 1e-12), SY_AL)
            from scipy import optimize
            s = optimize.brentq(f, 1e-6, hi) if f(hi) > 0 else hi
            ratio.append(s / Pcr_A)
        lin = [min(SY_AL / (1 + v), 5 * Pcr_A) / Pcr_A for v in ecr]
        ax.plot(ecr, ratio, color=col, ls=ls, label=f"L$_e$/r = {sl}: secant (Eq. 10.36)")
        ax.plot(ecr, lin, color=col, ls=ls, lw=0.8, alpha=0.55)
    ax.text(1.05, 1.45, "thin lines: σ$_Y$A/(1 + ec/r²), Eq. 10.37,\nno amplification", fontsize=6.2, color=DIM)
    ax.axhline(1.0, color=DIM, lw=0.8, ls=DASH)
    ax.text(1.98, 1.04, "P = P$_{cr}$", fontsize=6.4, color=DIM, ha="right", va="bottom")
    ax.set_xlim(0, 2); ax.set_ylim(0, 2.6)
    ax.set_xlabel("Eccentricity ratio, ec/r²"); ax.set_ylabel("Load at first yield ÷ P$_{cr}$")
    ax.legend(loc="upper right", fontsize=6.4)
    ax.set_title("(b) 6061-T6: first yield vs eccentricity", fontsize=8, loc="left")
    return save(fig, FIG / "fig4_eccentric", title="Figure 4. Eccentric loads and the secant formula",
                alt=("Two panels. (a) The lever arm of the load about the mid-length section, divided by the eccentricity e, against P over "
                     "P_cr: the secant result rises from 1 at no load to about 2 at half the critical load and without bound as P "
                     "approaches P_cr; the simpler amplification factor 1 over (1 minus alpha) is close to it; the dashed line at 1 is what "
                     "superposition without deflection (Eq. 4.58 or Eq. 10.37) assumes. (b) For 6061-T6, the load at first yield divided "
                     "by P_cr against the eccentricity ratio e c over r squared, for slenderness ratios of 50, 100 and 250. For the slender "
                     "column (250) the first-yield load stays just below P_cr however small the eccentricity, while the linear estimate "
                     "(thin lines) runs far above P_cr; for the stocky column (50) eccentricity lowers the load strongly and the two "
                     "estimates are close."))


def fig5_curve():
    fig, ax = new_fig("full", 3.0)
    sl = np.linspace(4, 350, 500)
    euler = PI ** 2 * E_AL / sl ** 2 / 1e6
    tang = np.array([LM.column_curve_tangent(s, E_AL, SY_AL, M_RO) for s in sl]) / 1e6
    red = np.array([LM.column_curve_tangent(s, E_AL, SY_AL, M_RO, reduced=True) for s in sl]) / 1e6
    aa = np.array([LM.aa_6061(s) for s in sl]) / 1e6
    slY = PI * math.sqrt(E_AL / SY_AL)
    ax.axvspan(0, slY, color=FAIL, alpha=0.16, lw=0)
    ax.text(3, 395, "Euler's\nσ$_{cr}$ > σ$_Y$", fontsize=6.6, color="#8A5300", va="top")
    ax.plot(sl, np.minimum(euler, 1e4), color=THEORY, label="Euler, π²E/(L$_e$/r)²  (Eq. 10.13b)")
    ax.plot(sl, tang, color=THIRD, ls=DASHDOT, label="tangent modulus (Lab 1 curve, m = 17)")
    ax.plot(sl, red, color=FOURTH, ls=DOT, lw=1.8, label="reduced modulus (rectangle)")
    ax.plot(sl, aa, color=DIM, ls=DASH, lw=1.2, label="Aluminum Association allowable (Eqs. 10.43b–10.45b)")
    ax.axhline(SY_AL / 1e6, color=INK, lw=0.7, ls=(0, (3, 2)))
    ax.text(345, SY_AL / 1e6 + 8, "σ$_Y$", fontsize=7.5, ha="right")
    r = 6.35e-3 / math.sqrt(12)
    marks = [(0.090 / r, "D\n90 mm"), (0.300 / r, "A 300 mm;\nB fixed–fixed\n(ideal)"), (0.450 / r, "A 450, C;\nB fixed–pinned\n(ideal, just left)"), (0.600 / r, "A 600")]
    for xv, lab in marks:
        ax.plot([xv, xv], [0, 22], color=INK, lw=1.0)
        ax.text(xv, 26, lab, fontsize=5.9, ha="center", va="bottom", linespacing=1.05)
    xfp = LM.K_FACTORS["fixed-pinned"] * 0.640 / r
    ax.plot([xfp, xfp], [0, 14], color=INK, lw=1.0)
    ax.set_xlim(0, 350); ax.set_ylim(0, 500)
    ax.set_xlabel("Effective slenderness ratio, L$_e$/r"); ax.set_ylabel("Critical stress, σ$_{cr}$ (MPa)")
    ax.legend(loc="upper right", fontsize=6.6)
    return save(fig, FIG / "fig5_curve", title="Figure 5. Column curve for 6061-T6",
                alt=("Critical stress against effective slenderness ratio for 6061-T6 aluminum, from 0 to 350. Euler's hyperbola rises without "
                     "limit as the slenderness falls and crosses the yield strength (a horizontal line at about 274 MPa) near L_e/r = 50; the "
                     "region to the left is shaded because there Euler predicts a stress the material cannot carry. The tangent-modulus "
                     "curve, from Lab 1's stress-strain curve, leaves Euler's hyperbola below about L_e/r = 60 and stays under the yield "
                     "strength until very short columns; the reduced-modulus curve lies slightly above it. The Aluminum Association "
                     "allowable-stress curve (with its factor of safety) runs well below both. Tick marks along the bottom show the "
                     "slenderness of this lab's tests: Part D at about 49, the 300 mm pinned bar and the ideal fixed-fixed 600 mm bar at "
                     "about 164, the ideal fixed-pinned 640 mm bar near 244, the 450 mm bar of Parts A and C at about 245, and the 600 mm "
                     "pinned bar at about 327."))


def main():
    entries = [fig1_setup(), fig2_ends(), fig3_southwell(), fig4_eccentric(), fig5_curve()]
    write_alt_text(entries, FIG / "ALT_TEXT.md", "Lab 9: Columns")
    print("wrote", [e["file"] for e in entries])


if __name__ == "__main__":
    main()

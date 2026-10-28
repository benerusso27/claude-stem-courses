"""Lab 6 figures (series style). Writes ../figures/*.svg, *.png and ALT_TEXT.md.
Section views follow Beer: looking along -x, y up, z to the LEFT (drawn as screen x = -z).
Plots are normalized or use generic sections so the handout does not give away results."""
import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "shared"))
sys.path.insert(0, str(HERE))
from figstyle import (DASH, DASHDOT, DIM, DOT, FAIL, FOURTH, INK, LOAD, MEMBER_FILL, NUMERIC, THEORY, THIRD, arrow,  # noqa: E402
                      dim_line, new_fig, save, write_alt_text)
from matplotlib.colors import LinearSegmentedColormap  # noqa: E402
from matplotlib.patches import Circle, Polygon, Rectangle  # noqa: E402
from matplotlib.path import Path as MPath  # noqa: E402

import lab06_model as LM  # noqa: E402

FIG = HERE.parent / "figures"
CMAP = LinearSegmentedColormap.from_list("ct", ["#0072B2", "#FFFFFF", "#D55E00"])


def _sketch(ax, xlim, ylim):
    ax.set_xlim(*xlim); ax.set_ylim(*ylim); ax.set_aspect("equal"); ax.axis("off"); ax.grid(False)


def _axes_key(ax, x, y, s=0.9, fs=7):
    """Beer section-view axes: y up, z to the left."""
    arrow(ax, x, y, x, y + s, color=INK, lw=0.9, ms=7)
    arrow(ax, x, y, x - s, y, color=INK, lw=0.9, ms=7)
    ax.text(x + 0.15 * s, y + s, "y", fontsize=fs, fontstyle="italic", va="top")
    ax.text(x - s - 0.15 * s, y, "z", fontsize=fs, fontstyle="italic", ha="right", va="center")


def _key2(ax, x, y, up, side, sdir, s=0.8, fs=6.5):
    """Axes key for a side view: `up` axis upward, `side` axis toward sdir (+1 right, -1 left)."""
    arrow(ax, x, y, x, y + s, color=INK, lw=0.9, ms=7)
    arrow(ax, x, y, x + sdir * s, y, color=INK, lw=0.9, ms=7)
    ax.text(x - sdir * 0.15, y + s + 0.05, up, fontsize=fs, fontstyle="italic", va="bottom", ha="center")
    ax.text(x + sdir * (s + 0.25), y, side, fontsize=fs, fontstyle="italic", ha="center", va="center")


def _gage(ax, x, y, w=0.36, h=0.22, color=THEORY, rot=False):
    if rot:
        w, h = h, w
    ax.add_patch(Rectangle((x - w / 2, y - h / 2), w, h, fc="white", ec=color, lw=1.0, zorder=6))


def fig1_setup():
    fig, axs = new_fig("full", 3.6, ncols=3, gridspec_kw=dict(width_ratios=[1.15, 0.65, 1.2], wspace=0.05))
    # (a) bar, front view (loading vertical, width h horizontal); units: 10 mm per unit
    ax = axs[0]; _sketch(ax, (-4.6, 4.6), (-1.2, 16.6))
    h, L, a = 5.08, 10.0, 2.5            # scaled: width 50.8 mm -> 5.08; free length 250 -> 10.0 (factor 1/25 along the length)
    y0 = 2.6
    ax.add_patch(Rectangle((-h / 2, y0), h, L, fc=MEMBER_FILL, ec=INK, lw=1.0))
    for yb in (y0 - 1.9, y0 + L):
        ax.add_patch(Rectangle((-3.4, yb), 6.8, 1.9, fc="#BFBFBF", ec=INK, lw=0.9, hatch="////"))
    offs = [0.0, 0.847, 1.693]          # e = 0, h/6, h/3 (scaled to the drawing width)
    for yp in (y0 - 1.0, y0 + L + 1.0):
        for k, e in enumerate(offs):
            ax.add_patch(Circle((-e, yp), 0.27, fc="white", ec=INK, lw=0.8, zorder=4))
    ax.add_patch(Circle((-offs[2], y0 + L + 1.0), 0.27, fc=LOAD, ec=INK, lw=0.8, zorder=5))
    ax.add_patch(Circle((-offs[2], y0 - 1.0), 0.27, fc=LOAD, ec=INK, lw=0.8, zorder=5))
    arrow(ax, -offs[2], y0 + L + 1.3, -offs[2], y0 + L + 2.9, color=LOAD, ms=10)
    arrow(ax, -offs[2], y0 - 1.3, -offs[2], y0 - 2.9 + 0.2, color=LOAD, ms=10)
    ax.text(-offs[2] + 0.25, y0 + L + 2.55, "P", color=LOAD, fontstyle="italic", fontsize=9)
    ax.plot([-offs[2]] * 2, [y0 - 1.0, y0 + L + 1.0], color=LOAD, lw=0.8, ls=DASH)
    ax.text(-offs[2] - 0.15, y0 + L * 0.82, "load line", color=LOAD, fontsize=6.3, rotation=90, ha="right", va="center")
    ym = y0 + L / 2
    for yy in (-2.0, -1.0, 0.0, 1.0, 2.0):
        _gage(ax, -yy, ym, rot=True)
    _gage(ax, 0.0, y0 + 1.6, rot=True)
    ax.text(h / 2 + 0.25, ym, "5 gages across\nthe width, each\nface, mid-length", fontsize=6.3, va="center", color=THEORY)
    ax.text(h / 2 + 0.25, y0 + 1.6, "end pair\n(40 mm)", fontsize=6.3, va="center", color=THEORY)
    dim_line(ax, -3.9, y0, -3.9, y0 + L, "L = 250 mm", offset=(-0.35, 0), fs=6.8, rotation=90)
    dim_line(ax, -3.9, y0 + L, -3.9, y0 + L + 1.0, "a", offset=(-0.35, 0), fs=6.8)
    ax.text(3.55, y0 + L + 0.95, "holes at\ne = 0, h/6, h/3", ha="left", va="center", fontsize=6.3)
    ax.text(0, -1.0, "front face (z = +b/2)", ha="center", fontsize=6.5)
    _key2(ax, 4.1, -0.7, "x", "y", -1, s=0.9)
    ax.set_title("(a) Bar, Parts A and C: front view", fontsize=8.5, loc="left")
    # (b) side view: out-of-plane hole and LVDT
    ax = axs[1]; _sketch(ax, (-3.0, 3.2), (-1.2, 16.6))
    b = 1.27
    ax.add_patch(Rectangle((-b / 2, y0), b, L, fc=MEMBER_FILL, ec=INK, lw=1.0))
    for yb in (y0 - 1.9, y0 + L):
        ax.add_patch(Rectangle((-1.9, yb), 3.8, 1.9, fc="#BFBFBF", ec=INK, lw=0.9, hatch="////"))
    ez = b / 2
    for yp in (y0 - 1.0, y0 + L + 1.0):
        ax.add_patch(Circle((ez, yp), 0.27, fc=LOAD, ec=INK, lw=0.8, zorder=5))
    arrow(ax, ez, y0 + L + 1.3, ez, y0 + L + 2.9, color=LOAD, ms=10)
    arrow(ax, ez, y0 - 1.3, ez, y0 - 2.7, color=LOAD, ms=10)
    ax.plot([ez] * 2, [y0 - 1.0, y0 + L + 1.0], color=LOAD, lw=0.8, ls=DASH)
    # straightened shape (exaggerated) in tension: the centroid moves toward the load line
    xs = np.linspace(0, 1, 50)
    ax.plot(0.45 * np.sin(np.pi * xs), y0 + L * xs, color=THEORY, lw=1.0, ls=DASH)
    ax.add_patch(Rectangle((-2.3, ym - 0.35), 1.1, 0.7, fc="white", ec=THIRD, lw=1.0)); ax.plot([-1.2, -b / 2], [ym, ym], color=THIRD, lw=1.2)
    ax.text(-1.75, ym - 0.9, "LVDT", ha="center", fontsize=6.3, color=THIRD)
    dim_line(ax, 0.0, y0 + L + 3.3, ez, y0 + L + 3.3, "", fs=6)
    ax.text(0.3, y0 + L + 3.65, "b/2", ha="center", fontsize=6.3)
    ax.text(0.0, -1.0, "edge view", ha="center", fontsize=6.5)
    ax.text(1.0, ym + 2.9, "bar bows\ntoward the\nload line", fontsize=6.0, color=THEORY, va="center")
    _key2(ax, 1.5, -0.7, "x", "z", 1, s=0.8)
    ax.set_title("(b) Part C hole", fontsize=8.5, loc="left")
    # (c) angle section with gusset load point and gages
    ax = axs[2]; _sketch(ax, (-1.5, 7.8), (-2.6, 7.0))
    bv, bh, t = 5.08, 5.08, 0.635
    P = [(0, 0), (0, bv), (-t, bv), (-t, t), (-bh, t), (-bh, 0)]
    ax.add_patch(Polygon([(-z, y) for z, y in P], closed=True, fc=MEMBER_FILL, ec=INK, lw=1.1))
    ax.add_patch(Rectangle((1.6, -0.953), 4.6, 0.953, fc="none", ec=DIM, lw=0.8, ls=DASH))
    ax.text(5.95, -1.45, "gusset (at the ends only)", ha="right", fontsize=6.2, color=DIM)
    zl, yl = -2.858, -0.476
    ax.plot([-zl], [yl], marker="D", ms=6, color=INK, zorder=7)
    ax.text(-zl + 0.25, yl - 0.2, "P", fontsize=8.5, fontstyle="italic", va="top")
    for name, (z, y), (dx, dy) in (("G1", (0, 4.4), (-0.75, 0)), ("G2", (0, 1.2), (-0.75, 0)), ("G3", (-1.2, 0), (0, -0.55)), ("G4", (-4.4, 0), (0, -0.55))):
        _gage(ax, -z + (-0.12 if z == 0 else 0), y + (-0.12 if y == 0 else 0), rot=(z == 0))
        ax.text(-z + dx, y + dy, name, fontsize=6.8, ha="center", va="center", color=THEORY)
    dim_line(ax, 0, -2.15, -zl, -2.15, "g = 28.6", offset=(0, -0.3), fs=6.5)
    dim_line(ax, 6.6, 0, 6.6, yl, "", fs=6)
    ax.text(6.75, yl / 2, "4.76", fontsize=6.3, va="center")
    ax.text(3.4, 3.4, "50.8 × 50.8 × 6.35 mm\n6061-T6 angle", fontsize=6.6, ha="center")
    _axes_key(ax, 7.3, 5.4, s=0.7, fs=6.5)
    ax.set_title("(c) Part B: angle section", fontsize=8.5, loc="left")
    return save(fig, FIG / "fig1_setup", title="Figure 1. Test set-ups for Lab 6",
                alt=("Three schematic panels. (a) Front view of the 50.8 by 12.7 millimeter aluminum bar held between two steel end blocks; "
                     "the free length between the blocks is 250 millimeters, and the loading pins sit a distance a beyond each end of the free "
                     "length. Each block has holes at in-plane offsets of zero, one sixth and one third of the width (x up the bar, y across it); here the pins are in the h/3 "
                     "holes and the load line runs parallel to the bar, off its centerline. Five gages run across the width at mid-length on each "
                     "face, and a further pair sits 40 millimeters from one block. (b) Edge view of the same bar with the pins in the fourth hole, "
                     "offset half the thickness out of plane; a displacement transducer touches the face at mid-length, and a dashed curve shows "
                     "the bar bowing toward the load line under tension. (c) Section view of the 50.8 by 50.8 by 6.35 millimeter angle, drawn with "
                     "y up and z to the left: the load acts at a point 28.6 millimeters from the heel along the horizontal leg and 4.76 millimeters "
                     "below it, in the mid-plane of the gusset that is bolted to the leg at the ends. Gages G1 and G2 are on the outer face of the "
                     "vertical leg near its tip and near the heel; G3 and G4 are on the underside of the horizontal leg near the heel and near its tip."))


def fig2_kern():
    fig, axs = new_fig("full", 2.7, ncols=2, gridspec_kw=dict(width_ratios=[1.35, 1], wspace=0.15))
    # (a) superposition across the depth for e = 0.25 h (generic)
    ax = axs[0]; _sketch(ax, (-0.3, 12.2), (-2.8, 3.0))
    h = 4.0
    e = 0.25
    blocks = [("$P/A$", lambda y: 1.0), ("$-M_z\\,y/I_z$", lambda y: 6 * e * (2 * y / h) * 1.0), ("$\\sigma_x$", lambda y: 1 + 6 * e * (2 * y / h))]
    xs0 = [0.6, 4.6, 8.8]
    sc = 0.55
    ys = np.linspace(-h / 2, h / 2, 60)
    for (lab, f), x0 in zip(blocks, xs0):
        ax.plot([x0, x0], [-h / 2, h / 2], color=INK, lw=1.0)
        v = np.array([f(y) for y in ys])
        ax.fill_betweenx(ys, x0, x0 + sc * v, where=v >= 0, color=NUMERIC, alpha=0.25, lw=0)
        ax.fill_betweenx(ys, x0, x0 + sc * v, where=v < 0, color=THEORY, alpha=0.30, lw=0)
        ax.plot(x0 + sc * v, ys, color=INK, lw=1.0)
        ax.text(x0 + 0.7, -h / 2 - 0.55, lab, ha="center", fontsize=8)
    ax.text(3.1, 0, "+", fontsize=14, ha="center", va="center"); ax.text(7.3, 0, "=", fontsize=14, ha="center", va="center")
    y_na = -(h * h / 12) / (e * h)
    ax.plot([8.4, 10.6], [y_na, y_na], color=INK, lw=1.4)
    ax.text(10.7, y_na, "N.A.", fontsize=7.5, va="center")
    ax.plot([0.2, 1.6], [0, 0], color=DIM, lw=0.6, ls=DOT); ax.text(0.15, 0.12, "C", fontsize=7, color=DIM, ha="right")
    ax.text(10.4, 1.25, "tension", fontsize=6.8, color=NUMERIC); ax.text(9.2, -2.1, "compression", fontsize=6.8, color=THEORY)
    ax.set_title("(a) Load at e = h/4 in the plane of symmetry: superposition", fontsize=8.5, loc="left")
    # (b) kern of a rectangle and the antipole relation
    ax = axs[1]; _sketch(ax, (-3.0, 5.6), (-3.8, 3.2))
    H, B = 5.0, 2.0
    ax.add_patch(Rectangle((-B / 2, -H / 2), B, H, fc=MEMBER_FILL, ec=INK, lw=1.1))
    kern = [(0, H / 6), (B / 6, 0), (0, -H / 6), (-B / 6, 0)]
    ax.add_patch(Polygon([(-z, y) for y, z in [(H / 6, 0), (0, B / 6), (-H / 6, 0), (0, -B / 6)]], closed=True, fc="#BFBFBF", ec=INK, lw=1.2))
    void = kern
    r2 = H * H / 12
    for e_, col, lab in ((H / 8, FOURTH, "load inside the kern"), (H / 6, THIRD, "load on its boundary"), (H / 3.2, LOAD, "load outside the kern")):
        ax.plot([0.0], [e_], marker="D", ms=5, color=col, zorder=6)
        y0 = -r2 / e_
        ax.plot([-1.5, 1.5], [y0, y0], color=col, lw=1.3, ls=DASH if y0 < -H / 2 else "-")
        ax.text(1.6, y0, f"N.A., {lab}", fontsize=6.3, color=col, va="center")
    ax.annotate("h/6", xy=(0, H / 6), xytext=(-1.6, H / 6 + 0.5), fontsize=6.6, arrowprops=dict(arrowstyle="-", lw=0.6, color=DIM))
    ax.annotate("b/6", xy=(B / 6 * -1 * -1, 0), xytext=(1.3, 0.9), fontsize=6.6, arrowprops=dict(arrowstyle="-", lw=0.6, color=DIM))
    ax.plot([0, 0], [-H / 2 - 0.3, H / 2 + 0.3], color=DIM, lw=0.6, ls=DOT)
    _axes_key(ax, -2.0, -3.5, s=0.7, fs=6.5)
    ax.set_title("(b) Kern of a rectangle", fontsize=8.5, loc="left")
    del void
    return save(fig, FIG / "fig2_kern", title="Figure 2. Eccentric load in a plane of symmetry, and the kern",
                alt=("Two panels. (a) Stress across the depth of a rectangular section loaded at a quarter of the depth above the centroid: "
                     "a uniform block P over A plus a linear bending distribution, minus M z y over I z, gives a combined distribution that is "
                     "tension over most of the depth and compression near the bottom; the neutral axis, where the combined stress is zero, "
                     "lies below the centroid, on the side away from the load. (b) A rectangle with its kern, a diamond whose half-diagonals "
                     "are h over 6 along y and b over 6 along z. Three load points on the y axis are shown with their neutral axes: a load inside "
                     "the kern puts the neutral axis outside the section, a load on the kern boundary puts it exactly on the bottom edge, and a "
                     "load outside the kern brings it into the section. The farther the load moves out, the closer the neutral axis comes to the centroid."))


def fig3_principal():
    """Generic unequal angle 60 x 40 x 5 mm, load at the outside corner of the long-leg tip."""
    fig, axs = new_fig("full", 3.3, ncols=2, gridspec_kw=dict(width_ratios=[1.1, 1], wspace=0.35))
    bv, bh, t = 60e-3, 40e-3, 5e-3
    sec = LM.angle(bv, bh, t)
    pr = LM.props(sec)
    zL, yL = 0.0, bv                                    # load at the outer corner of the vertical leg tip
    yP, zP = yL - pr["yc"], zL - pr["zc"]
    P = 1.0
    a0, b0, c0 = LM.stress_coeffs(pr, P, yP, zP)
    an, bn, cn = LM.stress_coeffs(pr, P, yP, zP, naive=True)
    ax = axs[0]; _sketch(ax, (-0.012, 0.062), (-0.012, 0.072))
    # stress map clipped to the section
    Z, Y = np.meshgrid(np.linspace(-bh, 0, 260), np.linspace(0, bv, 380))
    S = (a0 + b0 * (Y - pr["yc"]) + c0 * (Z - pr["zc"])) * pr["A"] / P
    poly = [(-z, y) for z, y in sec["polys"][0]]
    smax = np.abs(S).max()
    im = ax.pcolormesh(-Z, Y, S, cmap=CMAP, vmin=-smax, vmax=smax, shading="auto", rasterized=True)
    patch = Polygon(poly, closed=True, fc="none", ec=INK, lw=1.1)
    ax.add_patch(patch); im.set_clip_path(patch)
    # principal axes
    th = 0.5 * math.atan2(-2 * pr["Iyz"], pr["Iz"] - pr["Iy"])
    cz, cy = pr["zc"], pr["yc"]
    for ang, lab in ((th, "u (major)"), (th + math.pi / 2, "v (minor)")):
        dz, dy = math.cos(ang) * 0.036, math.sin(ang) * 0.036
        ax.plot([-(cz - dz), -(cz + dz)], [cy - dy, cy + dy], color=DIM, lw=0.8, ls=DASHDOT)
        ax.text(-(cz + dz * 1.0), cy + dy * 1.0, lab, fontsize=6.6, color=DIM, ha="center", va="center", fontstyle="italic", bbox=dict(fc="white", ec="none", pad=0.5))
    ax.plot([-cz], [cy], marker="o", ms=5, mfc="white", mec=INK, zorder=7); ax.text(-cz + 0.0015, cy - 0.004, "C", fontsize=7)
    ax.plot([-zL], [yL], marker="D", ms=6, color=INK, zorder=8); ax.text(-zL + 0.0016, yL + 0.001, "P", fontsize=8, fontstyle="italic")

    def na(aa, bb, cc, **kw):
        # aa + bb (y - yc) + cc (z - zc) = 0, drawn across the view
        zz = np.linspace(-0.07, 0.02, 2)
        yy = cy - (aa + cc * (zz - cz)) / bb
        ax.plot(-zz, yy, **kw)
    na(a0, b0, c0, color=INK, lw=1.6)
    na(an, bn, cn, color=THIRD, lw=1.3, ls=DASHDOT)
    ax.text(0.054, cy - (a0 + c0 * (-0.054 - cz)) / b0 + 0.002, "N.A.", fontsize=7)
    ax.text(0.040, cy - (an + cn * (-0.040 - cz)) / bn - 0.006, "I$_{yz}$ ignored\n(wrong)", fontsize=6.3, color=THIRD)
    K, _ = LM.kern(pr, LM.to_centroidal(pr, sec["hull"]))
    ax.add_patch(Polygon([(-(z + cz), y + cy) for y, z in K], closed=True, fc="#BFBFBF", ec=INK, lw=0.9, alpha=0.8))
    ax.set_xlim(-0.012, 0.062); ax.set_ylim(-0.012, 0.072)
    _axes_key(ax, 0.058, 0.060, s=0.007, fs=6.5)
    cb = fig.colorbar(im, ax=ax, orientation="horizontal", fraction=0.045, pad=0.02, aspect=30)
    cb.set_label("$\\sigma_x/(P/A)$", fontsize=7); cb.ax.tick_params(labelsize=6.5)
    ax.set_title("(a) Unequal angle in eccentric tension", fontsize=8.5, loc="left")
    # (b) moment of inertia vs axis angle (Mohr): I(θ) and I_yz(θ)
    ax = axs[1]
    ths = np.linspace(-90, 90, 361)
    Iz, Iy, Iyz = pr["Iz"], pr["Iy"], pr["Iyz"]
    Iu = (Iz + Iy) / 2 + (Iz - Iy) / 2 * np.cos(2 * np.radians(ths)) - Iyz * np.sin(2 * np.radians(ths))
    Puv = (Iz - Iy) / 2 * np.sin(2 * np.radians(ths)) + Iyz * np.cos(2 * np.radians(ths))
    s = pr["Imax"]
    ax.plot(ths, Iu / s, color=THEORY, label="I about an axis at θ from z")
    ax.plot(ths, Puv / s, color=THIRD, ls=DASHDOT, label="product of inertia in those axes")
    ax.axvline(math.degrees(th), color=DIM, lw=0.8, ls=DOT)
    ax.axhline(0, color=DIM, lw=0.6)
    ax.text(math.degrees(th) + 3, 0.62, "θ$_p$: product = 0,\nI = I$_{max}$", fontsize=6.6)
    ax.set_xlabel("Axis angle θ from z toward y (°)"); ax.set_ylabel("Second moment / I$_{max}$")
    ax.set_xlim(-90, 90); ax.set_xticks([-90, -45, 0, 45, 90])
    ax.legend(loc="lower center", fontsize=6.4, bbox_to_anchor=(0.5, -0.30), ncol=1)
    ax.set_title("(b) Principal axes", fontsize=8.5, loc="left")
    return save(fig, FIG / "fig3_principal", title="Figure 3. Unsymmetric section: principal axes and the neutral axis",
                alt=("Two panels. (a) A generic unequal-leg angle, 60 by 40 by 5 millimeters, drawn with y up and z to the left, loaded in "
                     "tension at the outside corner of the tip of its long leg. The section is shaded by normal stress, orange for tension "
                     "and blue for compression. Dash-dot lines mark the principal axes u (major) and v (minor), which are tilted from the "
                     "legs. A solid line marks the true neutral axis, which crosses the short leg; a purple dash-dot line, labelled wrong, "
                     "shows where the neutral axis would be if the product of inertia were ignored. A grey quadrilateral near the centroid "
                     "is the kern. (b) The second moment of area about an axis at angle theta from z, and the product of inertia in the "
                     "rotated axes, plotted against theta from minus 90 to 90 degrees: the second moment is largest exactly where the "
                     "product of inertia is zero, which defines the principal angle theta p."))


def fig4_beamcolumn():
    fig, axs = new_fig("full", 2.9, ncols=2, gridspec_kw=dict(width_ratios=[1.1, 1], wspace=0.22))
    ax = axs[0]; _sketch(ax, (-0.8, 12.6), (-4.6, 4.4))
    L, a, e = 9.0, 1.2, 1.2
    x0 = 1.6
    for sgn, yb, lab, col in ((1, 1.4, "tension: the bar straightens toward the load line", THEORY),
                              (-1, -2.6, "compression: the bar bows away from it", NUMERIC)):
        yline = yb + e
        ax.plot([x0 - a - 0.4, x0 + L + a + 0.4], [yline, yline], color=DIM, lw=0.7, ls=DASH)
        ax.plot([x0, x0 + L], [yb, yb], color=DIM, lw=0.8, ls=DOT)
        xs = np.linspace(0, L, 80)
        w = (0.55 if sgn > 0 else -0.55) * np.sin(np.pi * xs / L) * e
        ax.plot(x0 + xs, yb + w, color=col, lw=4.0, solid_capstyle="round")
        ax.plot([x0 - a, x0], [yline, yb], color=INK, lw=6, alpha=0.5, solid_capstyle="butt")
        ax.plot([x0 + L, x0 + L + a], [yb, yline], color=INK, lw=6, alpha=0.5, solid_capstyle="butt")
        for xp in (x0 - a, x0 + L + a):
            ax.add_patch(Circle((xp, yline), 0.2, fc="white", ec=INK, lw=0.9, zorder=6))
        d = 1 if sgn > 0 else -1
        xr, xl = x0 + L + a + 0.3, x0 - a - 0.3
        if d > 0:
            arrow(ax, xr, yline, xr + 1.0, yline, color=LOAD, ms=9); arrow(ax, xl, yline, xl - 1.0, yline, color=LOAD, ms=9)
        else:
            arrow(ax, xr + 1.0, yline, xr, yline, color=LOAD, ms=9); arrow(ax, xl - 1.0, yline, xl, yline, color=LOAD, ms=9)
        ax.text(x0 + L + a + 0.8, yline + 0.35, "P", color=LOAD, fontstyle="italic", fontsize=8)
        ax.text(x0 + L / 2, yb - 1.25, lab, ha="center", fontsize=6.9, color=col)
    dim_line(ax, x0 + L * 0.12, 1.4, x0 + L * 0.12, 1.4 + e, "", fs=7)
    ax.text(x0 + L * 0.12 + 0.2, 1.4 + e / 2, "e", fontsize=7.5, fontstyle="italic", va="center")
    dim_line(ax, x0 - a, 3.6, x0, 3.6, "a", offset=(0, 0.35), fs=7)
    dim_line(ax, x0, 3.6, x0 + L, 3.6, "L", offset=(0, 0.35), fs=7)
    ax.text(x0 + L - 0.2, 1.4 + e + 0.3, "load line", fontsize=6.5, color=DIM, ha="right")
    ax.set_title("(a) Member between rigid end blocks (exaggerated)", fontsize=8.5, loc="left")
    ax = axs[1]
    r = np.linspace(-0.92, 1.0, 400)
    curves = (("mid", 0.0, THEORY, "-", "mid-length, a/L = 0"), ("mid", 0.1, NUMERIC, DASH, "mid-length, a/L = 0.1"),
              ("end", 0.1, THIRD, DASHDOT, "ends of the free length, a/L = 0.1"))
    for where, aL, col, ls, lab in curves:
        Pcr = LM.euler_load_blocks(1.0, 1.0, aL)
        vals = [LM.beam_column(rr * Pcr, 1.0, 1.0, aL, 1.0)["Cmid" if where == "mid" else "Cend"] for rr in r]
        ax.plot(r, vals, color=col, ls=ls, label=lab)
    ax.axhline(1, color=DIM, lw=0.8, ls=DOT)
    ax.axhspan(1 / 1.05, 1.05, color=FOURTH, alpha=0.12, lw=0)
    ax.text(0.98, 1.10, "Eq. 4.58 within 5 %", fontsize=6.6, color=FOURTH, ha="right")
    ax.set_xlabel("P / P$_{cr}$  (compression < 0 < tension)"); ax.set_ylabel("C = M / (P e)")
    ax.set_ylim(0, 3.0); ax.set_xlim(-0.92, 1.0)
    ax.legend(loc="upper right", fontsize=6.6, title="C at", title_fontsize=6.6)
    ax.set_title("(b) Bending moment factor vs load", fontsize=8.5, loc="left")
    return save(fig, FIG / "fig4_beamcolumn", title="Figure 4. When the deformation changes the eccentricity",
                alt=("Two panels. (a) A bar between two rigid end blocks that are pinned on the load line, a distance a beyond each end of the "
                     "free length L; the bar's centerline starts a distance e from the load line. Under tension the bar bends toward the load "
                     "line and the eccentricity at mid-length shrinks; under compression the bar bows away from the load line and the "
                     "eccentricity grows. (b) The bending moment divided by P times e, plotted against the axial load as a fraction of the "
                     "buckling load of the member with its end blocks. At mid-length the curves for end blocks of zero length and of one tenth "
                     "of the free length nearly coincide: the factor is 1 at zero load, falls below 1 in tension and rises without bound as the "
                     "compressive load approaches buckling. At the ends of the free length the factor changes much less. A narrow band around "
                     "1 marks where the superposition formula, which assumes the factor is 1, is within 5 percent."))


def fig5_combined():
    fig, axs = new_fig("full", 2.5, ncols=3, gridspec_kw=dict(width_ratios=[1.45, 0.55, 1.1], wspace=0.06))
    ax = axs[0]; _sketch(ax, (-0.8, 11.2), (-3.2, 3.6))
    ax.add_patch(Rectangle((-0.6, -1.9), 0.6, 3.8, fc="white", ec=DIM, hatch="////", lw=0.8))
    ax.add_patch(Rectangle((0, -0.8), 9.6, 1.6, fc=MEMBER_FILL, ec=INK, lw=1.0))
    ax.add_patch(Circle((9.6, 0.0), 0.32, fc="white", ec=INK, lw=1.0, zorder=5))
    ax.plot([9.6], [0.0], marker="o", ms=2.5, color=INK, zorder=6)
    ax.text(9.25, 1.15, "lever a$_L$ comes\ntoward you (+z)", fontsize=6.2, ha="center")
    arrow(ax, 10.5, 0.4, 10.5, -1.9, color=LOAD, ms=10); ax.text(10.65, -1.5, "F at the\nlever tip", color=LOAD, fontsize=6.6)
    xs = 3.4
    ax.plot([xs, xs], [-1.2, 1.2], color=THIRD, lw=1.2, ls=DASH)
    ax.plot([xs], [0.8], marker="o", ms=5, color=THEORY, zorder=6); ax.text(xs, 1.35, "H", fontsize=7.5, ha="center", color=THEORY)
    dim_line(ax, xs, -2.3, 9.6, -2.3, "L$_b$", offset=(0, -0.4), fs=7)
    ax.text(xs - 0.2, -1.55, "section", fontsize=6.4, color=THIRD, ha="right")
    _key2(ax, 0.6, 2.3, "y", "x", 1, s=0.8)
    ax.set_title("(a) Tube cantilever with a lever arm", fontsize=8.5, loc="left")
    ax = axs[1]; _sketch(ax, (-2.0, 2.0), (-2.6, 2.4))
    ax.add_patch(Circle((0, 0), 1.2, fc=MEMBER_FILL, ec=INK, lw=1.0)); ax.add_patch(Circle((0, 0), 0.95, fc="white", ec=INK, lw=0.9))
    ax.plot([0], [1.075], marker="o", ms=5, color=THEORY, zorder=6); ax.text(0, 1.45, "H", fontsize=7.5, ha="center", color=THEORY)
    ax.plot([-1.075], [0], marker="s", ms=5, color=FOURTH, zorder=6); ax.text(-1.5, 0, "K", fontsize=7.5, ha="center", va="center", color=FOURTH)
    _axes_key(ax, 1.5, -2.2, s=0.6, fs=6.5)
    ax.set_title("section", fontsize=8, loc="left")
    ax = axs[2]; _sketch(ax, (-0.4, 9.6), (-3.2, 3.6))
    for x0, lab, sig, col in ((2.2, "H: σ$_x$ = Mc/I\nτ = Tc/J", True, THEORY), (7.0, "K: σ$_x$ = P/A\nτ = Tc/J ± VQ/(It)", False, FOURTH)):
        ax.add_patch(Rectangle((x0 - 0.9, -0.4), 1.8, 1.8, fc="#F2F2F2", ec=INK, lw=1.0))
        if sig:
            arrow(ax, x0 + 1.0, 0.5, x0 + 2.0, 0.5, color=THEORY, ms=8); arrow(ax, x0 - 1.0, 0.5, x0 - 2.0, 0.5, color=THEORY, ms=8)
        c2 = THIRD if sig else FOURTH
        arrow(ax, x0 - 0.7, 1.55, x0 + 0.7, 1.55, color=c2, ms=8)
        arrow(ax, x0 + 0.7, -0.55, x0 - 0.7, -0.55, color=c2, ms=8)
        arrow(ax, x0 + 1.05, -0.2, x0 + 1.05, 1.2, color=c2, ms=8)
        arrow(ax, x0 - 1.05, 1.2, x0 - 1.05, -0.2, color=c2, ms=8)
        ax.text(x0, -1.6, lab, ha="center", va="top", fontsize=6.8)
    ax.text(4.6, 2.6, "surface elements, x along the tube", ha="center", fontsize=6.6)
    ax.set_title("(b) Stress components", fontsize=8.5, loc="left")
    return save(fig, FIG / "fig5_combined", title="Figure 5. Combined loads on a tube (Beer §8.3, preview of Lab 8)",
                alt=("Three parts. (a) Side view of a tube fixed to a wall at the left. A lever arm at the free end points toward the viewer, "
                     "and a downward force F at its tip bends and twists the tube. A section is cut a distance L b from the lever; point H is "
                     "at the top of that section. (b, left) The section seen end-on, with H at the top and K at the side, on the neutral axis. "
                     "(b, right) Two square stress elements on the tube surface. At H there is a normal stress from bending, M c over I, along "
                     "the tube, plus a shearing stress from torsion, T c over J. At K the bending stress is zero and only the axial stress P "
                     "over A remains, while the shearing stress is the torsional stress plus or minus the transverse-shear stress V Q over I t."))


def main():
    entries = [fig1_setup(), fig2_kern(), fig3_principal(), fig4_beamcolumn(), fig5_combined()]
    write_alt_text(entries, FIG / "ALT_TEXT.md", "Lab 6: Eccentric Axial Loading")
    print("wrote", [e["file"] for e in entries])


if __name__ == "__main__":
    main()

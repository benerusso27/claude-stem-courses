"""Lab 3 figures (series style). Writes ../figures/*.svg, *.png and ALT_TEXT.md.
Plots use ILLUSTRATIVE numbers in normalized form so the handout does not give away results."""
import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "shared"))
from figstyle import (DASH, DASHDOT, DIM, FAIL, FOURTH, INK, LOAD, MEMBER_FILL, NUMERIC, REACT, THEORY, THIRD, arrow,  # noqa: E402
                      dim_line, new_fig, save, sketch_axes, write_alt_text)
from matplotlib.patches import Arc, Ellipse, FancyArrowPatch, Polygon, Rectangle  # noqa: E402

FIG = HERE.parent / "figures"


def torque_arrow(ax, x, y, w, h, color=LOAD, ccw=True, lw=1.8):
    """Curved arrow around a shaft axis drawn as an elliptical arc (right-hand rule shown by the label)."""
    a = FancyArrowPatch((x - w / 2, y - h * 0.15), (x + w / 2, y - h * 0.15) if ccw else (x - w / 2 - 0.01, y - h * 0.15),
                        connectionstyle=f"arc3,rad={0.9 if ccw else -0.9}", arrowstyle="-|>", mutation_scale=11, color=color, lw=lw)
    ax.add_patch(a)


def cylinder(ax, x0, x1, y, r, fill=MEMBER_FILL, ec=INK, lw=1.2, z=1):
    ax.add_patch(Rectangle((x0, y - r), x1 - x0, 2 * r, fc=fill, ec="none", zorder=z))
    ax.plot([x0, x1], [y + r, y + r], color=ec, lw=lw, zorder=z + 1)
    ax.plot([x0, x1], [y - r, y - r], color=ec, lw=lw, zorder=z + 1)
    ax.add_patch(Ellipse((x1, y), 0.35 * r, 2 * r, fc=fill, ec=ec, lw=lw, zorder=z + 1))
    ax.add_patch(Arc((x0, y), 0.35 * r, 2 * r, theta1=90, theta2=270, ec=ec, lw=lw, zorder=z + 1))


def fig1_setup():
    fig, ax = sketch_axes("full", 2.9, xlim=(0, 18), ylim=(0, 7.2))
    # fixed head with torque cell (left), drive head (right)
    ax.add_patch(Rectangle((0.4, 1.6), 2.0, 3.6, fc="#D9D9D9", ec=INK))
    ax.text(1.4, 1.2, "fixed head +\ntorque cell", ha="center", va="top", fontsize=7.5)
    ax.add_patch(Rectangle((15.6, 1.6), 2.0, 3.6, fc="#D9D9D9", ec=INK))
    ax.text(16.6, 1.2, "drive head\n(rotation encoder)", ha="center", va="top", fontsize=7.5)
    # hex grip ends and shoulders
    for x0 in (2.4, 13.6):
        ax.add_patch(Rectangle((x0, 2.55), 2.0, 1.7, fc="#BFBFBF", ec=INK, hatch="////", lw=0.8))
    ax.add_patch(Polygon([[4.4, 2.75], [5.1, 3.05], [5.1, 3.75], [4.4, 4.05]], fc=MEMBER_FILL, ec=INK))
    ax.add_patch(Polygon([[13.6, 2.75], [12.9, 3.05], [12.9, 3.75], [13.6, 4.05]], fc=MEMBER_FILL, ec=INK))
    cylinder(ax, 5.1, 12.9, 3.4, 0.35)
    # troptometer collars
    for x in (6.3, 11.7):
        ax.add_patch(Rectangle((x - 0.15, 2.6), 0.3, 1.6, fc=THEORY, alpha=0.75, ec=THEORY))
    ax.plot([6.3, 6.3], [4.2, 5.4], color=THEORY, lw=1.2)
    ax.plot([11.7, 11.7], [4.2, 5.0], color=THEORY, lw=1.2)
    ax.add_patch(Arc((11.7, 5.0), 0.9, 0.9, theta1=20, theta2=160, ec=THEORY, lw=1.2))
    ax.plot([6.3, 11.6], [5.4, 5.4], color=THEORY, lw=1.0)
    ax.text(9.0, 5.65, "troptometer: twist φ over the gage length L", ha="center", fontsize=7.5, color=THEORY)
    dim_line(ax, 6.3, 1.9, 11.7, 1.9, "L = 50.8 mm", offset=(0, -0.35), fs=7.5)
    dim_line(ax, 5.1, 0.7, 12.9, 0.7, "reduced section 76.2 mm", offset=(0, -0.35), fs=7.5)
    ax.text(9.0, 3.4, "d = 6.35 mm", ha="center", va="center", fontsize=7.5)
    # torque vectors (right-hand rule): double-headed arrows along the axis
    arrow(ax, 16.0, 6.4, 17.6, 6.4, color=LOAD); arrow(ax, 16.3, 6.4, 17.3, 6.4, color=LOAD)
    ax.text(16.8, 6.75, "T", color=LOAD, fontsize=9, fontstyle="italic", ha="center")
    arrow(ax, 2.0, 6.4, 0.4, 6.4, color=REACT, hollow=True); arrow(ax, 1.7, 6.4, 0.7, 6.4, color=REACT, hollow=True)
    ax.text(1.2, 6.75, "T′", color=REACT, fontsize=9, fontstyle="italic", ha="center")
    ax.text(9.0, 6.6, "torque vectors by the right-hand rule (double arrows)", ha="center", fontsize=7.5, color=DIM)
    return save(fig, FIG / "fig1_setup", title="Figure 1. Torsion test set-up",
                alt=("Schematic of a torsion tester. A round specimen with hexagonal ends is held between a fixed head that contains "
                     "the torque cell on the left and a drive head with a rotation encoder on the right. Its reduced section is "
                     "6.35 millimeters in diameter and 76.2 millimeters long. Two collars of a troptometer are clamped 50.8 "
                     "millimeters apart on the reduced section and measure the angle of twist phi over that gage length. Torque "
                     "vectors drawn as double-headed arrows along the axis show the applied torque T at the drive head and the "
                     "reaction T prime at the fixed head."))


def fig2_kinematics():
    fig, ax = sketch_axes("full", 2.8, xlim=(0, 19), ylim=(0, 7))
    ax.text(0.2, 6.6, "(a) Plane sections rotate", fontsize=8.5, fontweight="bold")
    cylinder(ax, 0.8, 6.2, 3.3, 1.6)
    ax.plot([0.8, 6.2], [4.9, 4.9], color=INK, lw=1.2)
    ax.plot([0.8, 6.2], [4.9, 3.9], color=THEORY, lw=1.6, ls=DASH)
    ax.plot([0.8, 6.2], [4.9, 4.9], color=DIM, lw=0.8, ls=DASH)
    ax.add_patch(Arc((0.8, 4.9), 3.0, 3.0, theta1=-12, theta2=0, ec=THEORY, lw=1.0))
    ax.text(2.6, 4.95, "γ", color=THEORY, fontsize=9)
    ax.text(6.55, 3.85, "φ", color=THEORY, fontsize=9)
    dim_line(ax, 0.8, 1.1, 6.2, 1.1, "L", offset=(0, -0.3), fs=8)
    ax.text(3.5, 0.2, r"$\gamma = \rho\varphi/L$  (linear in ρ)", ha="center", fontsize=8.2)
    ax.text(7.4, 6.6, "(b) Elastic stress", fontsize=8.5, fontweight="bold")
    ax.add_patch(Ellipse((10.0, 3.3), 4.0, 4.0, fc=MEMBER_FILL, ec=INK, lw=1.2))
    for rr in np.linspace(0.25, 2.0, 7):
        L = 0.9 * rr
        arrow(ax, 10.0 - L / 2, 3.3 + rr, 10.0 + L / 2, 3.3 + rr, color=THEORY, lw=1.0, ms=6)
    ax.plot([10.0, 10.0], [3.3, 5.3], color=DIM, lw=0.6, ls=DASH)
    ax.text(10.0, 0.6, r"$\tau = T\rho/J$" + "\n" + r"$\tau_{max} = Tc/J$", ha="center", fontsize=8.2)
    ax.text(13.2, 6.6, "(c) Pure shear at the surface", fontsize=8.5, fontweight="bold")
    s = 1.4
    ax.add_patch(Rectangle((13.6, 2.7), s, s, fc=MEMBER_FILL, ec=INK))
    arrow(ax, 13.6, 2.7 + s + 0.15, 13.6 + s, 2.7 + s + 0.15, color=THEORY, lw=1.2, ms=7)
    arrow(ax, 13.6 + s, 2.55, 13.6, 2.55, color=THEORY, lw=1.2, ms=7)
    arrow(ax, 13.45, 2.7, 13.45, 2.7 + s, color=THEORY, lw=1.2, ms=7)
    arrow(ax, 13.75 + s, 2.7 + s, 13.75 + s, 2.7, color=THEORY, lw=1.2, ms=7)
    ax.text(14.3, 4.45, "τ", color=THEORY, fontsize=9)
    cx, cy, h = 17.3, 3.4, 0.75
    ax.add_patch(Polygon([[cx, cy - h], [cx + h, cy], [cx, cy + h], [cx - h, cy]], fc=MEMBER_FILL, ec=INK))
    arrow(ax, cx + 0.45, cy + 0.45, cx + 1.05, cy + 1.05, color=LOAD, lw=1.2, ms=7)
    arrow(ax, cx - 0.45, cy - 0.45, cx - 1.05, cy - 1.05, color=LOAD, lw=1.2, ms=7)
    arrow(ax, cx - 1.05, cy + 1.05, cx - 0.5, cy + 0.5, color=REACT, lw=1.2, ms=7)
    arrow(ax, cx + 1.05, cy - 1.05, cx + 0.5, cy - 0.5, color=REACT, lw=1.2, ms=7)
    ax.text(cx + 0.85, cy + 1.25, "σ = +τ", color=LOAD, fontsize=8)
    ax.text(cx - 1.95, cy + 1.25, "σ = −τ", color=REACT, fontsize=8)
    ax.text(16.2, 1.0, "planes at 45° carry\nσ = ±τ, no shear", ha="center", fontsize=8)
    return save(fig, FIG / "fig2_kinematics", title="Figure 2. Kinematics and stresses in a twisted circular shaft",
                alt=("Three sketches. (a) A circular shaft of length L: a straight line on its surface becomes a helix when one end "
                     "rotates by phi, so the surface shear strain is gamma; in general gamma equals rho times phi over L, linear "
                     "in the radius rho. (b) Elastic shear stress on the cross-section, drawn as arrows that grow linearly from zero "
                     "at the center to the maximum Tc over J at the surface. (c) A small element on the surface is in pure shear "
                     "tau; the same element rotated 45 degrees carries a tensile normal stress plus tau on one diagonal and a "
                     "compressive normal stress minus tau on the other, with no shear."))


def fig3_elastoplastic():
    fig, axs = new_fig("full", 2.75, ncols=3, gridspec_kw=dict(wspace=0.42))
    x = np.linspace(0, 1, 201)
    ax = axs[0]
    for k, col, ls, lab in ((1, THEORY, "-", r"$\varphi = \varphi_Y$"), (2, THIRD, DASHDOT, r"$\varphi = 2\varphi_Y$"), (4, FOURTH, (0, (1.2, 2.4)), r"$\varphi = 4\varphi_Y$")):
        ax.plot(x, np.minimum(k * x, 1), color=col, ls=ls, lw=1.8, label=lab)
    ax.set_xlabel(r"Radius, $\rho/c$"); ax.set_ylabel(r"Shear stress, $\tau/\tau_Y$")
    ax.set_ylim(0, 1.25); ax.legend(fontsize=7, loc="lower right")
    ax.set_title("(a) Plastic shell grows inward", fontsize=8.5, loc="left")
    ax = axs[1]
    f = np.linspace(0, 8, 400)
    T = np.where(f <= 1, f, 4 / 3 * (1 - 1 / (4 * np.maximum(f, 1) ** 3)))
    ax.plot(f, T, color=THEORY, lw=1.8, label="elastic–perfectly plastic")
    ax.plot(f, np.where(f <= 1, f, 4 / 3 * (1 - 1 / (4 * np.maximum(f, 1) ** 3)) * (1 + 0.012 * (f - 1))), color=THIRD, ls=DASHDOT, lw=1.6, label="with hardening (illustrative)")
    ax.plot(f, f, color=DIM, ls=DASH, lw=0.9, label="elastic formula")
    ax.axhline(4 / 3, color=DIM, lw=0.8, ls=(0, (1, 2)))
    ax.text(6.6, 1.24, "4/3", fontsize=8, color=DIM)
    ax.plot([3, 3 - 4 / 3 * (1 - 1 / 108)], [4 / 3 * (1 - 1 / 108), 0], color=NUMERIC, ls=DASH, lw=1.2)
    ax.text(2.75, 0.55, "unloading\n(elastic slope)", fontsize=6.5, color=NUMERIC)
    ax.set_xlim(0, 8); ax.set_ylim(0, 1.7)
    ax.set_xlabel(r"Twist, $\varphi/\varphi_Y$"); ax.set_ylabel(r"Torque, $T/T_Y$")
    ax.legend(fontsize=6.3, loc="lower right", bbox_to_anchor=(1.0, 0.02))
    ax.set_title("(b) Torque–twist", fontsize=8.5, loc="left")
    ax = axs[2]
    Tm = 4 / 3 * (1 - 1 / 108)
    res = np.minimum(3 * x, 1) - Tm * x
    ax.plot(x, np.minimum(3 * x, 1), color=THEORY, lw=1.6, label=r"loaded to $3\varphi_Y$")
    ax.plot(x, -Tm * x, color=DIM, ls=DASH, lw=1.0, label=r"unloading, $-T_{max}\rho/J$")
    ax.plot(x, res, color=FOURTH, lw=1.8, ls=(0, (1.2, 2.4)), label="residual")
    ax.axhline(0, color=INK, lw=0.6)
    ax.set_xlabel(r"Radius, $\rho/c$"); ax.set_ylabel(r"$\tau/\tau_Y$")
    ax.set_ylim(-1.75, 1.25)
    ax.legend(fontsize=6.3, loc="lower left")
    ax.set_title("(c) Residual stress", fontsize=8.5, loc="left")
    return save(fig, FIG / "fig3_elastoplastic", title="Figure 3. Elastoplastic torsion of a solid shaft (normalized)",
                alt=("Three normalized plots for an elastic–perfectly plastic solid shaft. (a) Shear stress over yield stress "
                     "versus radius over c for twists of one, two and four times the yield twist: the stress rises linearly from "
                     "the center and is capped at the yield stress in an outer plastic shell that grows inward. (b) Torque over the "
                     "yield torque versus twist over the yield twist: linear up to one, then curving toward the horizontal "
                     "asymptote 4/3; a hardening material keeps rising slowly; an unloading line from three times the yield twist "
                     "has the elastic slope and reaches zero torque at a permanent twist of about 1.68. (c) Residual stress after "
                     "unloading from three times the yield twist: the loaded stress minus the elastic unloading stress, positive "
                     "inside, negative near the surface."))


def fig4_fracture():
    fig, ax = sketch_axes("full", 2.4, xlim=(0, 17), ylim=(0, 6))
    ax.text(0.2, 5.6, "(a) Ductile: shear on a cross-section", fontsize=8.5, fontweight="bold")
    cylinder(ax, 0.8, 3.6, 3.0, 1.2)
    cylinder(ax, 4.0, 6.8, 3.0, 1.2)
    ax.text(3.8, 0.9, "flat fracture, perpendicular to the axis\n(plane of maximum shear)", ha="center", fontsize=7.8)
    ax.text(8.6, 5.6, "(b) Brittle: tension on a 45° helix", fontsize=8.5, fontweight="bold")
    cylinder(ax, 9.0, 15.8, 3.0, 1.2)
    xs = np.linspace(9.6, 15.2, 200)
    ys = 3.0 + 1.2 * np.sin((xs - 9.6) / 1.2 * 1.0)
    ax.plot(xs, ys, color=FAIL, lw=2.0)
    ax.text(12.4, 0.9, "fracture surface along a helix at 45°\n(normal to σ₁ = τ)", ha="center", fontsize=7.8)
    ax.annotate("45°", xy=(10.2, 3.6), xytext=(9.6, 4.8), fontsize=8, color="#8A5300", arrowprops=dict(arrowstyle="-", color="#8A5300", lw=0.6))
    return save(fig, FIG / "fig4_fracture", title="Figure 4. Fracture modes in torsion",
                alt=("Two sketches. (a) A ductile shaft breaks on a flat plane perpendicular to its axis, the plane of maximum shear "
                     "stress. (b) A brittle shaft such as gray cast iron breaks along a helical surface at 45 degrees to the axis, "
                     "perpendicular to the maximum tensile stress, which in pure shear equals tau."))


def fig5_noncircular():
    fig = None
    fig, axs = new_fig("full", 2.7, ncols=3, gridspec_kw=dict(wspace=0.5, width_ratios=[1.15, 1.2, 0.9]))
    ax = axs[0]
    ax.set_xlim(-0.3, 2.3); ax.set_ylim(-0.6, 1.7); ax.set_aspect("equal"); ax.axis("off")
    ax.add_patch(Rectangle((0, 0), 2, 1, fc=MEMBER_FILL, ec=INK, lw=1.2))
    xs = np.linspace(0.05, 1.95, 13)
    for xx in xs:
        mag = 0.25 * (1 - ((xx - 1) / 1.05) ** 6)
        arrow(ax, xx - mag / 2, 1.08, xx + mag / 2, 1.08, color=THEORY, lw=1.0, ms=5)
        arrow(ax, xx + mag / 2, -0.08, xx - mag / 2, -0.08, color=THEORY, lw=1.0, ms=5)
    ax.text(1.0, 0.5, "a × b", ha="center", va="center", fontsize=8)
    ax.text(1.0, 1.24, "largest τ at mid-side", ha="center", fontsize=7, color=THEORY)
    ax.plot([0], [1], "o", color=FOURTH, ms=4); ax.text(0.0, -0.45, "corners: τ = 0", fontsize=7, color=FOURTH)
    ax.set_title("(a) Rectangle", fontsize=8.5, loc="left")
    ax = axs[1]
    ab = np.linspace(1, 10, 200)
    c1, c2 = [], []
    for r in ab:
        n = np.arange(1, 400, 2.0)
        z = n * math.pi * r / 2
        s2 = np.sum(np.tanh(z) / n ** 5)
        with np.errstate(over="ignore"):
            sk = np.sum(np.where(z > 700, 0, 1 / (n * n * np.cosh(np.minimum(z, 700)))))
        cc2 = (1 - 192 / math.pi ** 5 / r * s2) / 3
        c2.append(cc2); c1.append(cc2 / (1 - 8 / math.pi ** 2 * sk))
    ax.plot(ab, c1, color=THEORY, lw=1.8, label=r"$c_1$: $\tau_{max} = T/(c_1ab^2)$")
    ax.plot(ab, c2, color=THIRD, lw=1.6, ls=DASHDOT, label=r"$c_2$: $\varphi = TL/(c_2ab^3G)$")
    ax.axhline(1 / 3, color=DIM, ls=DASH, lw=0.9); ax.text(6.5, 0.338, "thin strip: 1/3", fontsize=7, color=DIM)
    ax.set_xlabel("Aspect ratio, a/b"); ax.set_ylabel("Coefficient")
    ax.set_ylim(0.12, 0.36); ax.legend(fontsize=6.8, loc="lower right")
    ax.set_title("(b) Coefficients", fontsize=8.5, loc="left")
    ax = axs[2]
    ax.set_xlim(-1.4, 1.4); ax.set_ylim(-1.4, 1.4); ax.set_aspect("equal"); ax.axis("off")
    ax.add_patch(Ellipse((0, 0), 2.2, 2.2, fc=MEMBER_FILL, ec=INK, lw=1.2))
    ax.add_patch(Ellipse((0, 0), 1.9, 1.9, fc="white", ec=INK, lw=1.2))
    for ang in np.linspace(0, 2 * math.pi, 9)[:-1]:
        x0, y0 = 1.025 * math.cos(ang), 1.025 * math.sin(ang)
        dx, dy = -math.sin(ang) * 0.35, math.cos(ang) * 0.35
        arrow(ax, x0 - dx / 2, y0 - dy / 2, x0 + dx / 2, y0 + dy / 2, color=THEORY, lw=1.0, ms=5)
    ax.text(0, 0.05, "q = τt\nconstant", ha="center", va="center", fontsize=7.5, color=THEORY)
    ax.set_title("(c) Thin wall", fontsize=8.5, loc="left")
    return save(fig, FIG / "fig5_noncircular", title="Figure 5. Noncircular and thin-walled sections",
                alt=("Three panels. (a) A rectangle of sides a and b in torsion: shear stress arrows along the long edges are largest "
                     "at the middle of each long side and fall to zero at the corners. (b) The coefficients c1 and c2 in the formulas "
                     "tau max equals T over c1 a b squared and phi equals T L over c2 a b cubed G, plotted against the aspect ratio "
                     "a over b from 1 to 10: c1 rises from about 0.21 and c2 from about 0.14, and both approach one third, the "
                     "thin-strip limit. (c) A thin-walled tube carries a constant shear flow q equal to tau times t around the wall."))


if __name__ == "__main__":
    entries = [f() for f in (fig1_setup, fig2_kinematics, fig3_elastoplastic, fig4_fracture, fig5_noncircular)]
    write_alt_text(entries, FIG / "ALT_TEXT.md", "Lab 3: Torsion")
    print("wrote", [e["file"] for e in entries])

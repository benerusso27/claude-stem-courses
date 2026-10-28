"""Lab 1 figures (series style, shared/figstyle.py). Writes ../figures/*.svg, *.png and ALT_TEXT.md.

    python3 make_figures.py

Curves come from the series' own models with an ILLUSTRATIVE material (not the lab specimens),
so the handout does not give away the values students will measure.
"""
import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "shared"))
from figstyle import (DASH, DASHDOT, DIM, DOT, FAIL, FOURTH, INK, LOAD, MEASURED, MEMBER_FILL, NUMERIC,  # noqa: E402
                      REACT, SKY, STRESS_EDGE, STRESS_FILL, THEORY, THIRD, arrow, dim_line, new_fig, save,
                      sketch_axes, write_alt_text)
from matplotlib.patches import Circle, FancyBboxPatch, Polygon, Rectangle  # noqa: E402

FIG = HERE.parent / "figures"
entries = []


# ------------------------------------------------------------------------------------------------
def fig1_setup():
    fig, ax = sketch_axes("full", 4.6, xlim=(-1.4, 13), ylim=(0, 9.2))
    # frame
    ax.add_patch(Rectangle((1.2, 0.3), 5.6, 0.7, fc="#D9D9D9", ec=INK, lw=1.2))           # base
    for x in (1.5, 6.0):
        ax.add_patch(Rectangle((x, 1.0), 0.5, 7.6, fc="#EFEFEF", ec=INK, lw=1.2))           # columns (screws)
    ax.add_patch(Rectangle((1.2, 8.6), 5.6, 0.45, fc="#D9D9D9", ec=INK, lw=1.2))           # top
    ax.add_patch(Rectangle((1.2, 6.55), 5.6, 0.7, fc="#CFE3F0", ec=INK, lw=1.2))           # moving crosshead
    ax.add_patch(Rectangle((3.55, 6.0), 0.9, 0.55, fc="#FFFFFF", ec=INK, lw=1.2))          # load cell
    # grips
    for y0, h in ((5.05, 0.95), (1.55, 0.95)):
        ax.add_patch(Polygon([[3.35, y0], [4.65, y0], [4.45, y0 + h], [3.55, y0 + h]] if y0 < 3 else
                             [[3.55, y0], [4.45, y0], [4.65, y0 + h], [3.35, y0 + h]], closed=True, fc="#BFBFBF", ec=INK, lw=1.0, hatch="////"))
    ax.add_patch(Rectangle((3.6, 1.0), 0.8, 0.55, fc="#D9D9D9", ec=INK, lw=1.0))           # lower fixture
    # specimen: ends in grips, reduced section between
    ax.add_patch(Rectangle((3.78, 4.35), 0.44, 1.2, fc=MEMBER_FILL, ec=INK, lw=1.0))
    ax.add_patch(Rectangle((3.78, 2.1), 0.44, 1.25, fc=MEMBER_FILL, ec=INK, lw=1.0))
    ax.add_patch(Rectangle((3.87, 3.3), 0.26, 1.1, fc=MEMBER_FILL, ec=INK, lw=1.0))
    # extensometer (clip-on), knife edges at gage marks
    ax.add_patch(Rectangle((4.18, 3.42), 0.55, 0.86, fc="none", ec=THEORY, lw=1.6))
    for y in (3.45, 4.25):
        ax.plot([4.13, 4.2], [y, y], color=THEORY, lw=2.2)
    # motion and load arrows
    arrow(ax, 7.4, 6.9, 7.4, 8.1, color=LOAD, lw=1.6)
    ax.text(7.6, 7.5, "crosshead moves up\nat a set rate", fontsize=8, va="center", color=INK)
    arrow(ax, 4.0, 7.4, 4.0, 8.15, color=LOAD, lw=2.0)
    ax.text(4.15, 7.8, "P", fontsize=10, color=LOAD, fontstyle="italic", va="center")
    # labels with leaders
    def lab(x, y, tx, ty, text):
        ax.annotate(text, xy=(x, y), xytext=(tx, ty), fontsize=8, color=INK, va="center",
                    arrowprops=dict(arrowstyle="-", color=DIM, lw=0.6))
    lab(4.45, 6.28, 8.0, 6.2, "load cell: measures P")
    lab(4.6, 5.5, 8.0, 5.35, "upper wedge grip")
    lab(4.73, 3.85, 8.0, 4.25, "clip-on extensometer\n(gage length 50.0 mm)")
    lab(4.13, 3.1, 8.0, 3.2, "specimen, reduced section\nd₀ = 10.00 mm")
    lab(4.6, 2.0, 8.0, 2.1, "lower wedge grip")
    lab(6.8, 0.65, 8.0, 0.9, "fixed base")
    ax.text(1.1, 4.6, "frame\n(columns,\nscrews)", fontsize=8, color=DIM, ha="right", va="center")
    ax.text(10.6, 8.7, "Universal testing machine\n(schematic, not to scale)", fontsize=8, color=DIM, ha="center")
    return save(fig, FIG / "fig1_setup",
                title="Figure 1. Tension-test setup",
                alt=("Schematic of a universal testing machine. A moving crosshead at the top, carrying a load cell, "
                     "travels upward along two screw columns at a set rate while the base stays fixed. Wedge grips "
                     "hold the threaded or shouldered ends of a round specimen. A clip-on extensometer with a 50.0 mm "
                     "gage length is attached to the narrow reduced section, whose initial diameter is 10.00 mm. "
                     "An arrow labeled P shows the tensile load measured by the load cell."))


# ------------------------------------------------------------------------------------------------
def fig2_specimen_fbd():
    fig, ax = sketch_axes("full", 3.4, xlim=(0, 16), ylim=(-0.4, 6.6))
    yc, s = 4.0, 0.066   # drawing scale: 1 mm = 0.066 units
    L_red, d0, D_end, L_end = 60, 10, 16, 25
    x0 = 0.5
    xs = [x0, x0 + L_end * s, x0 + (L_end + 8) * s, x0 + (L_end + 8 + L_red) * s, x0 + (L_end + 16 + L_red) * s, x0 + (2 * L_end + 16 + L_red) * s]
    top = [(xs[0], yc + D_end / 2 * s), (xs[1], yc + D_end / 2 * s), (xs[2], yc + d0 / 2 * s), (xs[3], yc + d0 / 2 * s),
           (xs[4], yc + D_end / 2 * s), (xs[5], yc + D_end / 2 * s)]
    bot = [(x, 2 * yc - y) for x, y in top][::-1]
    ax.add_patch(Polygon(top + bot, closed=True, fc=MEMBER_FILL, ec=INK, lw=1.2))
    xm = (xs[2] + xs[3]) / 2
    # Saint-Venant zones near the fillets (about one diameter long)
    for xa in (xs[2], xs[3] - 10 * s):
        ax.add_patch(Rectangle((xa, yc - d0 / 2 * s), 10 * s, d0 * s, fc=FAIL, alpha=0.30, ec="none"))
    for dx in (-25, 25):   # gage marks
        ax.plot([xm + dx * s] * 2, [yc - d0 / 2 * s - 0.12, yc + d0 / 2 * s + 0.12], color=INK, lw=1.4)
    dim_line(ax, xm - 25 * s, yc - 0.75, xm + 25 * s, yc - 0.75, r"gage length $L_0$ = 50.0 mm", offset=(0.95, -0.32))
    for dx in (-25, 25):   # extension lines from the marks to the dimension line
        ax.plot([xm + dx * s] * 2, [yc - d0 / 2 * s - 0.15, yc - 0.82], color=DIM, lw=0.5)
    dim_line(ax, xs[2], yc + 1.2, xs[3], yc + 1.2, r"reduced section $L_\mathrm{c}$ = 60 mm", offset=(0, 0.3))
    for xx in (xs[2], xs[3]):
        ax.plot([xx, xx], [yc + d0 / 2 * s + 0.1, yc + 1.27], color=DIM, lw=0.5)
    dim_line(ax, xm - 12 * s, yc - d0 / 2 * s, xm - 12 * s, yc + d0 / 2 * s, "")
    ax.text(xm - 12 * s + 0.12, yc + 0.6, r"$d_0$ = 10.00 mm", fontsize=8, color=DIM, va="center")
    ax.text(xs[0] + 0.05, yc + D_end / 2 * s + 0.15, "grip end", fontsize=8, color=DIM)
    ax.text(x0, 6.25, "(a) Specimen", fontsize=9, fontweight="bold", color=INK)
    ax.annotate("shaded: fillet transition, stress not yet uniform\n(Saint-Venant zone, about one diameter long)",
                xy=(xs[2] + 5 * s, yc - d0 / 2 * s), xytext=(x0, 1.45), fontsize=7.5, color=INK, ha="left",
                arrowprops=dict(arrowstyle="-", color=DIM, lw=0.6))

    # (b) free-body diagram of the lower part of the gage, cut at section a-a
    bx, by, w, h = 12.3, 1.2, 1.4, 3.1
    ax.text(10.7, 6.25, "(b) Free body below a cut", fontsize=9, fontweight="bold", color=INK)
    ax.add_patch(Rectangle((bx, by), w, h, fc=MEMBER_FILL, ec=INK, lw=1.2))
    ax.plot([bx - 0.25, bx + w + 0.25], [by + h, by + h], color=INK, lw=0.8, ls=(0, (4, 2)))
    ax.text(bx + w + 0.35, by + h, "cut a–a", fontsize=8, color=DIM, va="center")
    # uniform stress on the cut face (pointing up = tension on the lower free body)
    ax.add_patch(Rectangle((bx, by + h), w, 0.55, fc=STRESS_FILL, alpha=0.45, ec=STRESS_EDGE, lw=1.0))
    for k in range(6):
        xk = bx + 0.12 + k * (w - 0.24) / 5
        arrow(ax, xk, by + h + 0.02, xk, by + h + 0.55, color=STRESS_EDGE, lw=1.0, ms=7)
    ax.text(bx + w / 2, by + h + 0.85, r"$\sigma = P/A_0$ (uniform)", fontsize=8.5, color=STRESS_EDGE, ha="center")
    # applied load at bottom (pulling down)
    arrow(ax, bx + w / 2, by, bx + w / 2, by - 0.95, color=LOAD, lw=2.0)
    ax.text(bx + w / 2 + 0.2, by - 0.65, r"$P$ (from the grip)", fontsize=8.5, color=LOAD, va="center")
    ax.text(bx - 0.25, by + h / 2, r"$\Sigma F_y = 0$:" + "\n" + r"$\sigma A_0 - P = 0$", fontsize=8.5, color=INK, ha="right", va="center")
    return save(fig, FIG / "fig2_specimen_fbd",
                title="Figure 2. Specimen geometry and free-body diagram",
                alt=("Part a: side view of a round tension specimen with wider grip ends, fillets, and a reduced section "
                     "60 mm long and 10.00 mm in diameter. Two gage marks 50.0 mm apart are centered on the reduced "
                     "section. Shaded zones about one diameter long next to each fillet are labeled as regions of "
                     "non-uniform stress. Part b: free-body diagram of the lower piece of the gage section below a cut "
                     "a–a. The grip pulls down with force P; on the cut face a uniform tensile stress sigma acts upward "
                     "over the original area A0. Equilibrium of vertical forces gives sigma times A0 minus P equals zero, "
                     "so sigma equals P over A0."))


# ------------------------------------------------------------------------------------------------
def illustrative_steel(n_pts=1400):
    """Illustrative mild steel (not the lab specimen): yield point, Luders plateau, Swift hardening, neck."""
    E = 200e3   # MPa
    s_uy, s_ly, eL = 360.0, 338.0, 0.020
    K, n = 820.0, 0.20
    st0 = s_ly * math.exp(eL)
    eps0 = (st0 / K) ** (1 / n)
    e, s = [0.0], [0.0]
    for sg in np.linspace(0, s_uy, 40)[1:]:
        e.append(sg / E); s.append(sg)
    e.append(s_uy / E + 0.0006); s.append(s_ly)
    for ep in np.linspace(0.0006, eL, 40)[1:]:
        e.append(math.expm1(ep + s_ly / E)); s.append(s_ly)
    eps = np.linspace(eL, 0.6, 3000)
    et = eps + K * (eps0 + eps - eL) ** n / E
    sig_t = K * (eps0 + eps - eL) ** n
    s_nom = sig_t * np.exp(-et)
    i_u = int(np.argmax(s_nom))
    for k in range(1, i_u + 1):
        e.append(math.expm1(et[k])); s.append(s_nom[k])
    e_u, s_u = e[-1], s[-1]
    # post-necking (gage average): smooth decline to fracture at e_f
    e_f, s_f = 0.32, 0.80 * s_u
    t = np.linspace(0, 1, 60)[1:]
    for tk in t:
        e.append(e_u + (e_f - e_u) * tk); s.append(s_u - (s_u - s_f) * tk ** 1.6)
    return dict(E=E, e=np.array(e), s=np.array(s), e_u=e_u, s_u=s_u, e_f=e_f, s_f=s_f, s_uy=s_uy, s_ly=s_ly, eL=eL, K=K, n=n, eps0=eps0)


def fig3_stress_strain():
    st = illustrative_steel()
    fig, axs = new_fig("full", 3.3, ncols=2, gridspec_kw=dict(width_ratios=[1.65, 1], wspace=0.32))
    ax = axs[0]
    e, s = st["e"], st["s"]
    pre = e <= st["e_u"] + 1e-12
    ax.plot(100 * e[pre], s[pre], color=THEORY, lw=1.8, label=r"engineering, $\sigma = P/A_0$")
    ax.plot(100 * e[~pre], s[~pre], color=THEORY, lw=1.8)
    # true stress up to necking (uniform), via sigma(1+e)
    ax.plot(100 * np.log1p(e[pre]), s[pre] * (1 + e[pre]), color=THIRD, ls=DASHDOT, lw=1.6,
            label=r"true, $\sigma_t = \sigma(1+\varepsilon)$ vs $\varepsilon_t = \ln(1+\varepsilon)$, to max load")
    ax.axvspan(100 * st["e_u"], 100 * 0.34, color=FAIL, alpha=0.16, lw=0)
    ax.text(100 * st["e_u"] + 0.6, 230, "necking:\ndeformation\nlocalizes", fontsize=7.5, color="#8A5300")
    ann = dict(fontsize=7.5, color=INK, arrowprops=dict(arrowstyle="-", color=DIM, lw=0.6))
    ax.annotate("upper yield point", xy=(100 * st["s_uy"] / st["E"], st["s_uy"]), xytext=(3.0, 205), **ann)
    ax.annotate("lower yield point,\nLüders plateau", xy=(1.2, st["s_ly"]), xytext=(5.5, 285), **ann)
    ax.annotate("strain hardening", xy=(8.0, s[np.searchsorted(e, 0.08)]), xytext=(9.5, 360), **ann)
    ax.plot([100 * st["e_u"]], [st["s_u"]], "o", mfc="white", mec=THEORY, ms=5, mew=1.5)
    ax.annotate(r"$\sigma_U$ at maximum load", xy=(100 * st["e_u"], st["s_u"]), xytext=(9.0, 560), **ann)
    ax.plot([100 * st["e_f"]], [st["s_f"]], "x", color=THEORY, ms=6, mew=1.8)
    ax.annotate("fracture", xy=(100 * st["e_f"], st["s_f"]), xytext=(27, 330), **ann)
    ax.set_xlim(0, 34); ax.set_ylim(0, 650)
    ax.set_xlabel(r"Engineering strain, $\varepsilon$ (%) — true strain for the dash-dot curve"); ax.set_ylabel("Stress (MPa)")
    ax.legend(loc="lower right", fontsize=7.2)
    ax.text(0.5, 625, "(a) Illustrative mild steel", fontsize=8, fontweight="bold")
    # (b) aluminum-like gradual yielding and 0.2 % offset construction
    ax = axs[1]
    E, s02, m = 70e3, 250.0, 14
    sg = np.linspace(0, 300, 600)
    ee = sg / E + 0.002 * (sg / s02) ** m
    ax.plot(100 * ee, sg, color=THEORY, lw=1.8)
    ax.plot(100 * (0.002 + sg / E), sg, color=DIM, ls=DASH, lw=1.0)
    ax.plot(100 * sg / E, sg, color=THEORY, lw=0.8, ls=DOT)
    ax.plot([100 * (0.002 + s02 / E)], [s02], "D", mfc="white", mec=NUMERIC, ms=5, mew=1.5)
    ax.annotate(r"$\sigma_Y$ (0.2 % offset)", xy=(100 * (0.002 + s02 / E), s02), xytext=(0.75, 175), fontsize=7.5,
                arrowprops=dict(arrowstyle="-", color=DIM, lw=0.6))
    ax.annotate(r"slope $E$", xy=(0.27, 0.27 * E / 100), xytext=(0.03, 255), fontsize=7.5,
                arrowprops=dict(arrowstyle="-", color=DIM, lw=0.6))
    ax.text(0.24, 8, "0.2 %", fontsize=7.5, color=DIM)
    ax.set_xlim(0, 1.2); ax.set_ylim(0, 320)
    ax.set_xlabel("Engineering strain, ε (%)"); ax.set_ylabel("Engineering stress, σ (MPa)")
    ax.text(0.03, 300, "(b) No yield point:\noffset method", fontsize=8, fontweight="bold", va="top")
    return save(fig, FIG / "fig3_stress_strain",
                title="Figure 3. Anatomy of the stress-strain diagram",
                alt=("Two plots of an illustrative material, not the lab specimens. Part a, engineering stress in MPa "
                     "versus engineering strain in percent from 0 to 34 percent for a mild steel: a steep linear elastic "
                     "line up to an upper yield point near 360 MPa, a drop to a flat lower-yield Luders plateau near "
                     "340 MPa extending to about 2 percent strain, a rising strain-hardening curve to a maximum of about "
                     "500 MPa near 18 percent strain, then a shaded necking region where engineering stress falls to "
                     "fracture at 32 percent. A dash-dot true-stress curve, plotted up to the maximum load only, lies "
                     "above the engineering curve and keeps rising. Part b, aluminum-like curve with gradual yielding "
                     "over 0 to 1.2 percent strain: a dashed line of slope E starting at 0.2 percent strain cuts the "
                     "curve at the 0.2 percent offset yield strength, marked by a diamond near 250 MPa."))


def fig4_considere():
    K, n, E = 800.0, 0.22, 200e3
    et = np.linspace(0.003, 0.45, 600)
    sig = K * et ** n
    dsig = n * K * et ** (n - 1)
    P_over = sig * np.exp(-et)             # P/A0 for a uniform bar: sigma_t * A/A0
    fig, axs = new_fig("full", 3.6, nrows=2, sharex=True, gridspec_kw=dict(height_ratios=[1, 1.35], hspace=0.12))
    ax = axs[0]
    ax.plot(et, P_over, color=THEORY, lw=1.8)
    ax.axvline(n, color=DIM, lw=0.8, ls=DASH)
    ax.plot([n], [K * n ** n * math.exp(-n)], "o", mfc="white", mec=THEORY, ms=5, mew=1.5)
    ax.set_ylabel(r"$P/A_0$ (MPa)")
    ax.set_ylim(300, 520)
    ax.text(0.012, 492, r"load $P = \sigma_t A$ falls once area loss outpaces hardening", fontsize=7.5)
    ax = axs[1]
    ax.plot(et, sig, color=THEORY, lw=1.8, label=r"true stress $\sigma_t = K\varepsilon_t^{\,n}$")
    ax.plot(et, dsig, color=FOURTH, ls=DOT, lw=1.8, label=r"hardening rate $d\sigma_t/d\varepsilon_t$")
    ax.axvline(n, color=DIM, lw=0.8, ls=DASH)
    ax.axvspan(n, 0.45, color=FAIL, alpha=0.14, lw=0)
    ax.plot([n], [K * n ** n], "o", mfc="white", mec=INK, ms=6, mew=1.6)
    ax.annotate("Considère: " + r"$d\sigma_t/d\varepsilon_t = \sigma_t$" + "\nso " + r"$\varepsilon_{t,U} = n$" + " (Hollomon law)", xy=(n, K * n ** n), xytext=(0.285, 760),
                fontsize=7.5, arrowprops=dict(arrowstyle="-", color=DIM, lw=0.6))
    ax.text(0.36, 120, "unstable:\nneck grows", fontsize=7.5, color="#8A5300")
    ax.text(0.04, 230, "stable: uniform stretching", fontsize=7.5, color=INK)
    ax.set_ylim(0, 1400)
    ax.set_xlim(0, 0.45)
    ax.set_xlabel(r"True strain, $\varepsilon_t$"); ax.set_ylabel("Stress (MPa)")
    ax.legend(loc="upper right", fontsize=7.2)
    return save(fig, FIG / "fig5_considere",
                title="Figure 5. Considère construction for the onset of necking",
                alt=("Two stacked plots sharing a true-strain axis from 0 to 0.45, for an illustrative power-law material "
                     "with n = 0.22. Top: load per original area rises, peaks at true strain 0.22, then falls. Bottom: the "
                     "true-stress curve rises with decreasing slope while the dotted hardening-rate curve falls steeply "
                     "from high values; they cross at true strain 0.22, marked with a circle and labeled Considère: "
                     "d sigma t over d epsilon t equals sigma t, so the necking strain equals n. A dashed vertical line "
                     "links the crossing to the load maximum. To the left the region is labeled stable uniform "
                     "stretching; to the right a shaded region is labeled unstable, neck grows."))


def fig5_compliance():
    fig = __import__("matplotlib.pyplot", fromlist=["figure"]).figure(figsize=(6.5, 2.9))
    axL = fig.add_axes([0.0, 0.02, 0.36, 0.96]); axL.axis("off"); axL.set_xlim(0, 6); axL.set_ylim(0, 8.2); axL.set_aspect("equal")
    axR = fig.add_axes([0.47, 0.17, 0.51, 0.78])
    # springs in series schematic (vertical): ground, machine spring, specimen spring, crosshead
    def spring(ax, x, y0, y1, color, label, nturn=6):
        ys = np.linspace(y0 + 0.3, y1 - 0.3, 2 * nturn + 1)
        xs = [x + (0.35 if k % 2 else -0.35) for k in range(len(ys))]
        xs[0] = xs[-1] = x
        ax.plot([x, x], [y0, y0 + 0.3], color=color, lw=1.6); ax.plot(xs, ys, color=color, lw=1.6); ax.plot([x, x], [y1 - 0.3, y1], color=color, lw=1.6)
        ax.text(x + 0.6, (y0 + y1) / 2, label, fontsize=8, va="center", color=color)
    axL.add_patch(Rectangle((1.0, 0.2), 2.0, 0.35, fc="white", ec=DIM, hatch="////", lw=0.8))
    spring(axL, 2.0, 0.55, 3.3, REACT, "frame, grips,\nshoulders: " + r"$C_\mathrm{m}$")
    axL.add_patch(Rectangle((1.6, 3.3), 0.8, 0.3, fc="#D9D9D9", ec=INK, lw=0.8))
    spring(axL, 2.0, 3.6, 6.6, THEORY, "specimen:\n" + r"$L_\mathrm{c}/(EA_0)$")
    axL.add_patch(Rectangle((1.0, 6.6), 2.0, 0.35, fc="#CFE3F0", ec=INK, lw=1.0))
    arrow(axL, 2.0, 7.0, 2.0, 7.9, color=LOAD, lw=1.8)
    axL.text(2.2, 7.6, r"$\Delta$ (crosshead travel)", fontsize=8, color=LOAD, va="center")
    axL.text(0.1, 4.7, "same " + r"$P$" + "\nin both", fontsize=8, color=INK, ha="left", va="center")
    # plot: stress vs strain from extensometer and from crosshead (with toe)
    E, A0, Lc, Cm, toe = 200e3, 78.54, 60.0, 0.008, 0.05   # MPa, mm^2, mm, mm/kN, mm
    sg = np.linspace(0, 280, 200)
    P = sg * A0 / 1e3   # kN
    e_ext = sg / E
    e_ch = (Lc * sg / E + Cm * P + toe * (1 - np.exp(-P / 0.6))) / Lc
    axR.plot(100 * e_ext, sg, color=THEORY, lw=1.8)
    axR.plot(100 * e_ch, sg, color=THIRD, ls=DASHDOT, lw=1.8)
    axR.text(0.16, 255, r"extensometer on the gage: slope $E$", fontsize=7.8, color=THEORY)
    axR.text(0.33, 110, "crosshead travel / " + r"$L_\mathrm{c}$: slope $E_\mathrm{app}$", fontsize=7.8, color=THIRD)
    axR.annotate("toe: grips seating", xy=(100 * e_ch[10], sg[10]), xytext=(0.22, 12), fontsize=7.5,
                 arrowprops=dict(arrowstyle="-", color=DIM, lw=0.6))
    axR.set_xlim(0, 0.7); axR.set_ylim(0, 300)
    axR.set_xlabel(r"Engineering strain, $\varepsilon$ (%)"); axR.set_ylabel(r"Engineering stress, $\sigma$ (MPa)")
    axR.text(0.47, 52, r"$1/E_\mathrm{app} = 1/E + A_0 C_\mathrm{m}/L_\mathrm{c}$", fontsize=8.5, color=INK)
    return save(fig, FIG / "fig4_compliance",
                title="Figure 4. Why crosshead travel overstates strain",
                alt=("Left: schematic of two springs in series between a fixed base and the moving crosshead. The lower "
                     "spring represents the frame, grips and specimen shoulders with compliance C m; the upper spring "
                     "represents the specimen reduced section with compliance L c over E A0. Both carry the same load P, "
                     "and the crosshead travel Delta is the sum of their stretches. Right: engineering stress up to "
                     "280 MPa versus strain up to 0.6 percent for an illustrative steel. The extensometer curve rises "
                     "steeply with slope E; the crosshead-based curve starts with a curved toe from grip seating and "
                     "then rises with a much smaller slope E app, given by 1 over E app equals 1 over E plus A0 C m over L c."))


if __name__ == "__main__":
    for f in (fig1_setup, fig2_specimen_fbd, fig3_stress_strain, fig5_compliance, fig4_considere):
        entries.append(f())
    write_alt_text(entries, FIG / "ALT_TEXT.md", "Lab 1: Tension test and the stress-strain diagram")
    print("wrote", [e["file"] for e in entries])

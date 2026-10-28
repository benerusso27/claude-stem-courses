"""Shared figure style for the ENGR 2228 lab series (see style_guide.md, sections 4-6).

Usage:
    import sys; sys.path.insert(0, "<series>/shared")
    from figstyle import *
    fig, ax = new_fig("full")          # 6.5 in wide
    ...
    save(fig, "figures/fig3_curve", alt="Alt text ...", title="Short title")

Every figure is saved as SVG (text kept as text) and as a 300-dpi PNG, and the alt
text is embedded in the SVG <title>/<desc>.
"""
import re
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyArrowPatch, Polygon, Rectangle  # noqa: E402,F401

# ---- palette (Okabe-Ito, semantic roles) -----------------------------------
THEORY = "#0072B2"      # closed-form theory, solid
NUMERIC = "#D55E00"     # independent numerical solution, dashed
MEASURED = "#1A1A1A"    # measured / sample data, open circles
UNCERT = "#8C8C8C"      # error bars, bands
THIRD = "#B8478F"       # third series, dash-dot (Okabe-Ito reddish purple, darkened to 3:1 on white)
FOURTH = "#00845F"      # fourth series, dotted (Okabe-Ito bluish green, darkened to 3:1 on white)
FAIL = "#E69F00"        # region where an assumption fails
SKY = "#56B4E9"
LOAD = "#D55E00"        # applied loads in diagrams
REACT = "#4D4D4D"       # reactions (hollow heads)
MEMBER_FILL = "#E6E6E6"
INK = "#1A1A1A"
DIM = "#666666"
STRESS_FILL = "#56B4E9"
STRESS_EDGE = "#0072B2"

DASH = (0, (6, 4))
DASHDOT = (0, (6, 3, 1.5, 3))
DOT = (0, (1.2, 2.4))

FULL_W, HALF_W = 6.5, 3.2

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Liberation Sans", "Helvetica", "DejaVu Sans"],
    "font.size": 9,
    "axes.labelsize": 9,
    "axes.titlesize": 9,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "legend.fontsize": 8,
    "legend.frameon": False,
    "axes.edgecolor": INK,
    "axes.labelcolor": INK,
    "axes.linewidth": 0.8,
    "xtick.color": INK,
    "ytick.color": INK,
    "xtick.direction": "out",
    "ytick.direction": "out",
    "axes.grid": True,
    "grid.color": "#D9D9D9",
    "grid.linewidth": 0.5,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "lines.linewidth": 1.6,
    "svg.fonttype": "none",          # keep text as text in SVG (selectable, accessible)
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.04,
    "mathtext.fontset": "dejavusans",
})


def new_fig(width="full", height=None, **kw):
    w = FULL_W if width == "full" else HALF_W if width == "half" else float(width)
    h = height if height is not None else w * 0.55
    return plt.subplots(figsize=(w, h), **kw)


def sketch_axes(width="full", height=None, xlim=(0, 10), ylim=(0, 6)):
    """Axes for diagrams: equal aspect, no ticks/grid/spines."""
    fig, ax = new_fig(width, height)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.grid(False)
    return fig, ax


def arrow(ax, x0, y0, x1, y1, color=LOAD, lw=1.8, hollow=False, ms=12, z=5):
    style = "-|>" if not hollow else "-|>"
    a = FancyArrowPatch((x0, y0), (x1, y1), arrowstyle=style, mutation_scale=ms,
                        color=color, lw=lw, zorder=z,
                        fc=("white" if hollow else color))
    ax.add_patch(a)
    return a


def dim_line(ax, x0, y0, x1, y1, text, offset=(0, 0), fs=8, color=DIM, rotation=0, ha="center", va="center"):
    """Dimension line with arrowheads at both ends; label placed at the midpoint + offset (no mask)."""
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="<|-|>", color=color, lw=0.7, mutation_scale=7, shrinkA=0, shrinkB=0))
    if text:
        xm, ym = (x0 + x1) / 2 + offset[0], (y0 + y1) / 2 + offset[1]
        ax.text(xm, ym, text, ha=ha, va=va, fontsize=fs, color=color, rotation=rotation)


def hatch_block(ax, x, y, w, h, angle_up=True):
    ax.add_patch(Rectangle((x, y), w, h, fc="white", ec=DIM, lw=0.8, hatch="////", zorder=1))


def _embed_alt(svg_path, title, alt):
    s = Path(svg_path).read_text(encoding="utf-8")
    esc = lambda t: (t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))  # noqa: E731
    s = re.sub(r"<svg ", '<svg role="img" aria-labelledby="fig-title fig-desc" ', s, count=1)
    s = re.sub(r"(<svg[^>]*>)", r"\1\n <title id=\"fig-title\">" + esc(title) +
               "</title>\n <desc id=\"fig-desc\">" + esc(alt) + "</desc>", s, count=1)
    # strip the matplotlib date stamp so rebuilt figures diff cleanly
    s = re.sub(r"<dc:date>.*?</dc:date>", "", s)
    Path(svg_path).write_text(s, encoding="utf-8")


def save(fig, basename, alt, title):
    base = Path(basename)
    base.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(base.with_suffix(".svg"), metadata={"Date": None})
    fig.savefig(base.with_suffix(".png"), dpi=300)
    plt.close(fig)
    _embed_alt(base.with_suffix(".svg"), title, alt)
    return {"file": base.name, "title": title, "alt": alt}


def write_alt_text(entries, path, lab_title):
    lines = [f"# Alt text — {lab_title}", "",
             "Each entry is embedded in the SVG `<title>`/`<desc>` and in the Word file's image description.", ""]
    for e in entries:
        lines += [f"## {e['file']} (.svg / .png)", f"**{e['title']}**", "", e["alt"], ""]
    Path(path).write_text("\n".join(lines), encoding="utf-8")

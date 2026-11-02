"""Assemble the study-guide pages.

Each page body lives in _build/pages/<file>.html. The first lines of a body are front matter:
    <!--title: Pressure in Static Fluids-->
    <!--short: Pressure-->
    <!--eyebrow: Week 2 · Chapter 3-->
    <!--desc: one sentence for search engines and link previews-->
The rest is the page content (hero, layout, sections, and the page's own <script>).
This script wraps every body in the same head, top bar and footer, and writes <file>.html
to the site root. Run: python3 _build/build.py
"""
import html, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = ROOT / "_build" / "pages"

# Reading order (also the prev/next order). Index is separate.
ORDER = [
    "ch01-02-properties", "ch03-pressure", "ch04-static-forces", "ch05-buoyancy",
    "ch06-bernoulli", "ch07-energy", "ch08-reynolds-friction", "ch09-noncircular", "ch10-minor-losses",
    "ch11-pipe-systems", "ch13-pumps", "ch16-momentum", "ch17-drag-lift",
    "review",
]

HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="claude:viewport-fit-sides" content="cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,500..800&family=Source+Serif+4:ital,opsz,wght@0,8..60,400..700;1,8..60,400..600&family=JetBrains+Mono:wght@400..600&display=swap">
<link rel="stylesheet" href="assets/fm.css">
<script>window.MathJax={{tex:{{inlineMath:[['\\\\(','\\\\)']],displayMath:[['\\\\[','\\\\]']],packages:{{'[+]':['html']}}}},svg:{{fontCache:'global'}},options:{{skipHtmlTags:['script','noscript','style','textarea','pre','code']}}}};</script>
<script defer src="assets/mathjax/tex-svg-full.js"></script>
<script src="assets/fm-core.js"></script>
<script src="assets/fm-ui.js"></script>
</head>
<body>
<div class="wrap">
<nav class="topbar" aria-label="Site">
  <a class="home" href="index.html">Fluid Mechanics · ENGR 4254</a>
  <span class="pn">{prev}{next}<button type="button" class="themebtn presbtn" aria-pressed="false" title="Larger type for projecting in lecture">Present</button><button type="button" class="themebtn" id="themebtn" aria-label="Color theme">Auto</button></span>
</nav>
"""

FOOT = """
<footer>
  <div class="pager">{prev_big}{next_big}</div>
  <p>Lecture companion for ENGR/EGTG 4254 Fluid Mechanics (FDU), keyed to the instructor's slide numbers and to Mott &amp; Untener, <i>Applied Fluid Mechanics</i>, 8th ed. (Pearson, 2022). Usable as in-class lecture material (press Present for projector-sized type) and as a study guide afterward. Figures are drawn for this site. Check numbers against your textbook's tables on graded work.</p>
</footer>
</div>
</body>
</html>
"""


def meta(body):
    m = {}
    for k in ("title", "short", "eyebrow", "desc"):
        r = re.search(rf"<!--{k}:\s*(.*?)-->", body)
        m[k] = r.group(1).strip() if r else ""
    body = re.sub(r"<!--(title|short|eyebrow|desc):.*?-->\n?", "", body)
    return m, body


def build():
    metas = {}
    bodies = {}
    for name in ORDER:
        f = PAGES / f"{name}.html"
        if not f.exists():
            continue
        metas[name], bodies[name] = meta(f.read_text(encoding="utf-8"))
    built = [n for n in ORDER if n in bodies]
    for i, name in enumerate(built):
        m = metas[name]
        prv = built[i - 1] if i > 0 else None
        nxt = built[i + 1] if i + 1 < len(built) else None
        lk = lambda n, arrow_left: (f'<a href="{n}.html">{"← " if arrow_left else ""}{html.escape(metas[n]["short"])}{"" if arrow_left else " →"}</a>') if n else ""
        page = HEAD.format(title=html.escape(m["title"]), desc=html.escape(m["desc"]), prev=lk(prv, True), next=lk(nxt, False))
        page += bodies[name]
        page += FOOT.format(prev_big=lk(prv, True) or "<span></span>", next_big=lk(nxt, False) or '<a href="index.html">All guides →</a>')
        (ROOT / f"{name}.html").write_text(page, encoding="utf-8")
    # index
    idx = PAGES / "index.html"
    if idx.exists():
        m, body = meta(idx.read_text(encoding="utf-8"))
        page = HEAD.format(title=html.escape(m["title"]), desc=html.escape(m["desc"]), prev="", next="").replace(
            '<a class="home" href="index.html">Fluid Mechanics · ENGR 4254</a>', '<span class="home">ENGR/EGTG 4254 · FDU</span>')
        page += body + FOOT.format(prev_big="<span></span>", next_big=f'<a href="{built[0]}.html">Start: {html.escape(metas[built[0]]["short"])} →</a>' if built else "")
        (ROOT / "index.html").write_text(page, encoding="utf-8")
    print("built:", ", ".join(built), "+ index" if idx.exists() else "")


if __name__ == "__main__":
    build()

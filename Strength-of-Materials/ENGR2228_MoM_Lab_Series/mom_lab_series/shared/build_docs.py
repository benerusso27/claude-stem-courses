"""Markdown -> editable .docx (native Word equations) -> PDF, in the series style.

    python3 shared/build_docs.py make-reference
    python3 shared/build_docs.py build lab01_stress_strain/src/lab01_handout.md \
        --out lab01_stress_strain/lab01_handout.docx --header "Lab 1 - Tension Test" \
        --alt lab01_stress_strain/figures/ALT_TEXT.md

Pipeline: pandoc (with shared/reference.docx) -> python-docx post-processing (table
styling, header text, figure alt text, keep-with-next) -> LibreOffice -> PDF.
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

HERE = Path(__file__).resolve().parent
REF = HERE / "reference.docx"
BLUE = RGBColor(0x00, 0x72, 0xB2)
INK = RGBColor(0x1A, 0x1A, 0x1A)
FONT = "Arial"


# ----------------------------------------------------------------------------- helpers
def _shade(ppr_or_tcpr, fill):
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill)
    ppr_or_tcpr.append(shd)


def _pborder(ppr, side, color, sz=12, space=4):
    bdr = ppr.find(qn("w:pBdr"))
    if bdr is None:
        bdr = OxmlElement("w:pBdr")
        ppr.append(bdr)
    el = OxmlElement(f"w:{side}")
    el.set(qn("w:val"), "single")
    el.set(qn("w:sz"), str(sz))
    el.set(qn("w:space"), str(space))
    el.set(qn("w:color"), color)
    bdr.append(el)


def _set_font(style, size=None, bold=None, color=None, italic=None, name=FONT):
    f = style.font
    f.name = name
    rpr = style.element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.append(rfonts)
    for a in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
        rfonts.set(qn(a), name)
    for a in ("w:asciiTheme", "w:hAnsiTheme", "w:cstheme", "w:eastAsiaTheme"):
        if rfonts.get(qn(a)) is not None:
            del rfonts.attrib[qn(a)]
    if size:
        f.size = Pt(size)
    if bold is not None:
        f.bold = bold
    if italic is not None:
        f.italic = italic
    if color is not None:
        f.color.rgb = color


def _box_style(doc, name, fill, edge):
    styles = doc.styles
    existing = [s for s in styles if s.name == name]
    st = existing[0] if existing else styles.add_style(name, WD_STYLE_TYPE.PARAGRAPH)
    st.base_style = _Styles(doc)["Body Text"]
    _set_font(st, size=10.5)
    pf = st.paragraph_format
    pf.space_before = Pt(2)
    pf.space_after = Pt(2)
    pf.left_indent = Inches(0.12)
    pf.right_indent = Inches(0.12)
    ppr = st.element.get_or_add_pPr()
    for side in ("top", "left", "bottom", "right"):
        _pborder(ppr, side, edge, sz=8 if side != "left" else 24, space=4)
    _shade(ppr, fill)
    return st


# ----------------------------------------------------------------------------- reference
class _Styles:
    """Look styles up by display name without python-docx's built-in name translation."""
    def __init__(self, doc):
        self.doc = doc

    def __getitem__(self, name):
        for s in self.doc.styles:
            if s.name == name or s.style_id == name.replace(" ", ""):
                return s
        raise KeyError(name)


def make_reference():
    tmp = HERE / "_ref_default.docx"
    subprocess.run(["pandoc", "-o", str(tmp), "--print-default-data-file", "reference.docx"], check=True)
    doc = Document(str(tmp))
    st = _Styles(doc)
    _set_font(st["Normal"], size=11, color=INK)
    for name in ("Body Text", "First Paragraph", "Compact"):
        _set_font(st[name], size=11, color=INK)
        st[name].paragraph_format.space_after = Pt(6)
        st[name].paragraph_format.line_spacing = 1.12
    st["Compact"].paragraph_format.space_after = Pt(2)
    _set_font(st["Title"], size=20, bold=True, color=INK)
    _set_font(st["Subtitle"], size=12, color=BLUE)
    for lvl, size in ((1, 15), (2, 12.5), (3, 11.5), (4, 11)):
        h = st[f"Heading {lvl}"]
        _set_font(h, size=size, bold=True, color=BLUE)
        h.font.italic = False
        h.paragraph_format.space_before = Pt(14 if lvl == 1 else 10)
        h.paragraph_format.space_after = Pt(4)
        h.paragraph_format.keep_with_next = True
    for name in ("Image Caption", "Table Caption"):
        _set_font(st[name], size=9.5, italic=True, color=INK)
        st[name].paragraph_format.space_after = Pt(8)
    st["Table Caption"].paragraph_format.keep_with_next = True
    _set_font(st["Block Text"], size=10.5, color=INK)
    for name in ("Footnote Text", "Author", "Date", "Abstract"):
        try:
            _set_font(st[name], size=10, color=INK)
        except KeyError:
            pass
    _box_style(doc, "Callout", "EAF4FB", "0072B2")
    _box_style(doc, "Safety", "FFF4DC", "E69F00")
    _box_style(doc, "Answer", "F2F2F2", "8C8C8C")
    _box_style(doc, "Instructor", "F7EAF2", "CC79A7")
    # page: US Letter, 1-inch margins, footer with page number
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Inches(8.5), Inches(11)
    for m in ("left_margin", "right_margin", "top_margin", "bottom_margin"):
        setattr(sec, m, Inches(1))
    sec.header_distance = Inches(0.45)
    sec.footer_distance = Inches(0.45)
    fp = sec.footer.paragraphs[0]
    fp.text = ""
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = fp.add_run("ENGR 2228 Mechanics of Materials Lab Series  ·  page ")
    r.font.size = Pt(8.5)
    r.font.name = FONT
    _field(fp, "PAGE")
    hp = sec.header.paragraphs[0]
    hp.text = "HEADER_PLACEHOLDER"
    hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    for run in hp.runs:
        run.font.size = Pt(8.5)
        run.font.name = FONT
        run.font.color.rgb = RGBColor(0x66, 0x66, 0x66)
    doc.save(str(REF))
    tmp.unlink()
    print("wrote", REF)


def _field(paragraph, code):
    run = paragraph.add_run()
    run.font.size = Pt(8.5)
    for tag, text in (("begin", None), ("instr", code), ("separate", None), ("text", "1"), ("end", None)):
        if tag == "instr":
            el = OxmlElement("w:instrText")
            el.set(qn("xml:space"), "preserve")
            el.text = f" {text} "
        elif tag == "text":
            el = OxmlElement("w:t")
            el.text = text
        else:
            el = OxmlElement("w:fldChar")
            el.set(qn("w:fldCharType"), tag)
        run._r.append(el)


# ----------------------------------------------------------------------------- post-processing
def _parse_alt(path):
    """ALT_TEXT.md -> {figure number: alt text}, keyed by the 'figN_' file prefix."""
    alts = {}
    if not path or not Path(path).exists():
        return alts
    cur = None
    for block in Path(path).read_text(encoding="utf-8").split("\n## ")[1:]:
        head, *rest = block.split("\n")
        m = re.match(r"fig(\d+)_", head.strip())
        if not m:
            continue
        body = [ln for ln in rest if ln.strip() and not ln.startswith("**")]
        alts[int(m.group(1))] = " ".join(body).strip()
    return alts


def _style_table(tbl):
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tblPr = tbl._tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for side in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement(f"w:{side}")
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), "4")
        el.set(qn("w:space"), "0")
        el.set(qn("w:color"), "8C8C8C")
        borders.append(el)
    old = tblPr.find(qn("w:tblBorders"))
    if old is not None:
        tblPr.remove(old)
    tblPr.append(borders)
    mar = OxmlElement("w:tblCellMar")
    for side, w in (("top", 30), ("bottom", 30), ("left", 80), ("right", 80)):
        el = OxmlElement(f"w:{side}")
        el.set(qn("w:w"), str(w))
        el.set(qn("w:type"), "dxa")
        mar.append(el)
    tblPr.append(mar)
    for i, row in enumerate(tbl.rows):
        trPr = row._tr.get_or_add_trPr()
        cant = OxmlElement("w:cantSplit")
        trPr.append(cant)
        if i == 0:
            hdr = OxmlElement("w:tblHeader")
            trPr.append(hdr)
        for cell in row.cells:
            tcPr = cell._tc.get_or_add_tcPr()
            old_b = tcPr.find(qn("w:tcBorders"))
            if old_b is not None:
                tcPr.remove(old_b)
            tcb = OxmlElement("w:tcBorders")
            for side in ("top", "left", "bottom", "right"):
                el = OxmlElement(f"w:{side}")
                el.set(qn("w:val"), "single")
                el.set(qn("w:sz"), "4")
                el.set(qn("w:space"), "0")
                el.set(qn("w:color"), "8C8C8C")
                tcb.append(el)
            tcPr.append(tcb)
            if i == 0:
                _shade(tcPr, "DCEBF5")
            for p in cell.paragraphs:
                p.paragraph_format.space_after = Pt(1)
                p.paragraph_format.space_before = Pt(1)
                for r in p.runs:
                    r.font.size = Pt(9.5)
                    if i == 0:
                        r.font.bold = True


def postprocess(docx_path, header_text, alt_path):
    doc = Document(str(docx_path))
    for sec in doc.sections:
        for p in sec.header.paragraphs:
            if "HEADER_PLACEHOLDER" in p.text:
                for r in p.runs:
                    r.text = r.text.replace("HEADER_PLACEHOLDER", header_text)
    for tbl in doc.tables:
        _style_table(tbl)
        # tables mostly left blank for students: give rows room for handwriting
        body = [c.text.strip() for r in tbl.rows[1:] for c in r.cells[1:]]
        if body and sum(1 for t in body if not t) / len(body) >= 0.4:
            from docx.enum.table import WD_ROW_HEIGHT_RULE
            for r in tbl.rows[1:]:
                r.height = Inches(0.36)
                r.height_rule = WD_ROW_HEIGHT_RULE.AT_LEAST
    # alt text: caption starts with "Figure N." -> description from ALT_TEXT.md
    alts = _parse_alt(alt_path)
    missing = []
    for docpr in doc.element.body.iter(qn("wp:docPr")):
        cap = docpr.get("descr", "")
        m = re.match(r"Figure\s+(\d+)", cap)
        if m and int(m.group(1)) in alts:
            docpr.set("descr", alts[int(m.group(1))])
            docpr.set("title", cap.split(".")[0])
        elif m:
            missing.append(cap[:40])
    # keep figure paragraphs with their captions
    for p in doc.paragraphs:
        if p.style.name in ("Captioned Figure", "Figure"):
            p.paragraph_format.keep_with_next = True
    doc.save(str(docx_path))
    if missing:
        print("WARNING: no alt text for:", missing, file=sys.stderr)


def to_pdf_latex(md, pdf_out, header, resource):
    """Typeset the same Markdown source with XeLaTeX (high-quality math)."""
    hdr = Path(pdf_out).with_suffix(".hdr.tex")
    esc = header.replace("&", "\\&").replace("%", "\\%").replace("#", "\\#")
    hdr.write_text("\\newcommand{\\seriesheader}{" + esc + "}\n" + (HERE / "latex" / "header.tex").read_text())
    cmd = ["pandoc", str(md), "-f", MD_FORMAT, "-o", str(pdf_out), "--pdf-engine=xelatex",
           f"--include-in-header={hdr}", f"--lua-filter={HERE / 'latex' / 'boxes.lua'}", f"--lua-filter={HERE / 'latex' / 'supers.lua'}",
           f"--resource-path={resource}",
           "-V", "fontfamily=fontspec", "-V", "mainfont=Liberation Sans", "-V", "mathfont=Latin Modern Math",
           "-V", "geometry:letterpaper,margin=1in", "-V", "fontsize=11pt", "-V", "colorlinks=true",
           "-V", "linkcolor=seriesblue", "-V", "urlcolor=seriesblue"]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True)
    finally:
        hdr.unlink(missing_ok=True)
    if r.returncode != 0:
        sys.stderr.write(r.stderr)
        raise SystemExit(f"pandoc/xelatex failed for {md}")
    missing = sorted(set(re.findall(r"Missing character: There is no (\S+)", r.stderr)))
    if missing:   # a glyph the font lacks would silently vanish from the PDF
        raise SystemExit(f"{md}: characters missing from the PDF fonts: {missing} (often math split by a space before a closing $)")
    return Path(pdf_out)


MD_FORMAT = "markdown+pipe_tables+grid_tables+fenced_divs+tex_math_dollars"


def build(md, out, header, alt=None, pdf=True):
    md, out = Path(md), Path(out)
    resource = f"{md.parent}:{md.parent.parent}"
    cmd = ["pandoc", str(md), "-f", MD_FORMAT, "-o", str(out), f"--reference-doc={REF}",
           f"--resource-path={resource}", f"--lua-filter={HERE / 'latex' / 'boxes.lua'}", f"--lua-filter={HERE / 'latex' / 'supers.lua'}"]
    subprocess.run(cmd, check=True)
    postprocess(out, header, alt)
    if pdf:
        p = to_pdf_latex(md, out.with_suffix(".pdf"), header, resource)
        print("wrote", out, "and", p)
    else:
        print("wrote", out)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("make-reference")
    b = sub.add_parser("build")
    b.add_argument("md")
    b.add_argument("--out", required=True)
    b.add_argument("--header", required=True)
    b.add_argument("--alt")
    b.add_argument("--no-pdf", action="store_true")
    a = ap.parse_args()
    if a.cmd == "make-reference":
        make_reference()
    else:
        build(a.md, a.out, a.header, a.alt, pdf=not a.no_pdf)

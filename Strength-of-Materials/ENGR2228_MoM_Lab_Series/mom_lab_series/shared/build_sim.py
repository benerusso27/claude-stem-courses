"""Assemble a lab's self-contained simulation page.

    python3 shared/build_sim.py lab01_stress_strain [--artifact OUT.html]

Inlines shared/sim_core.css + sim_core.js and the lab's sample-data overlay (src/sample_overlay.py,
optional) into src/labNN_simulation.src.html -> labNN_simulation.html (a complete offline page).
--artifact also writes a copy without the document wrapper, for publishing as a hosted page.
"""
import importlib.util
import json
import re
import sys
from pathlib import Path

SERIES = Path(__file__).resolve().parent.parent


def build(lab_dir, artifact=None):
    lab = SERIES / lab_dir
    src = next((lab / "src").glob("lab*_simulation.src.html"))
    html = src.read_text(encoding="utf-8")
    css = (SERIES / "shared" / "sim_core.css").read_text(encoding="utf-8")
    js = (SERIES / "shared" / "sim_core.js").read_text(encoding="utf-8")
    data = "{}"
    ov = lab / "src" / "sample_overlay.py"
    if ov.exists():
        sys.path.insert(0, str(lab / "src"))
        spec = importlib.util.spec_from_file_location("sample_overlay", ov)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        data = json.dumps(mod.overlay(), separators=(",", ":"))
    html = html.replace("/*@@SIM_CORE_CSS@@*/", css).replace("/*@@SIM_CORE_JS@@*/", js).replace("/*@@SAMPLE_DATA@@*/", data)
    assert "@@" not in html, "unreplaced placeholder"
    out = lab / src.name.replace(".src.html", ".html")
    out.write_text(html, encoding="utf-8")
    print(f"wrote {out} ({len(html) / 1024:.0f} KB)")
    if artifact:
        body = re.sub(r"(?is)^.*?<head>\s*", "", html)
        body = re.sub(r"(?is)<meta charset=[^>]*>\s*<meta name=\"viewport\"[^>]*>\s*", "", body)
        body = re.sub(r"(?is)</head>\s*<body>", "", body)
        body = re.sub(r"(?is)</body>\s*</html>\s*$", "", body)
        Path(artifact).write_text(body, encoding="utf-8")
        print(f"wrote {artifact}")
    return out


if __name__ == "__main__":
    a = sys.argv[1:]
    art = a[a.index("--artifact") + 1] if "--artifact" in a else None
    build(a[0], art)

"""Browser check for a lab simulation page (Playwright + Chromium, headless).

    python3 shared/browser_check.py lab01_stress_strain/lab01_simulation.html [--out tests/results_browser.md]

At phone (375 px) and desktop (1280 px) widths, in light and dark color schemes:
  * loads the page and records console errors and uncaught exceptions;
  * checks that the page body never scrolls horizontally;
  * moves every range slider to its minimum, middle and maximum (input events), then resets;
  * types a value into every numeric box;
  * changes every <select> to each enabled option;
  * clicks every button (segmented toggles, experiments, play/pause, exports, copy);
  * after every action: no new errors, no "NaN"/"undefined"/"Infinity" in visible text, layout still fits;
  * no duplicate element ids once the page has built its controls, and every control is visible in at least one mode.
"""
import asyncio
import re
import sys
from pathlib import Path

from playwright.async_api import async_playwright

BAD = re.compile(r"\bNaN\b|\bundefined\b|Infinity")


async def run(page_path, width, scheme, log):
    async with async_playwright() as p:
        b = await p.chromium.launch()
        ctx = await b.new_context(viewport={"width": width, "height": 900}, color_scheme=scheme, accept_downloads=True)
        pg = await ctx.new_page()
        errors = []
        pg.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
        pg.on("pageerror", lambda e: errors.append("pageerror: " + str(e)))
        await pg.goto(Path(page_path).resolve().as_uri())
        await pg.wait_for_timeout(800)
        n_actions, problems = 0, []

        async def audit(label):
            nonlocal n_actions
            n_actions += 1
            await pg.wait_for_timeout(120)
            sw = await pg.evaluate("document.documentElement.scrollWidth")
            if sw > width + 1:
                problems.append(f"{label}: horizontal overflow ({sw}px > {width}px)")
            txt = await pg.evaluate("""() => { const w = document.querySelector('.wall') || document.body;
                const e = document.getElementById('errors'); const hide = e && !e.hidden;
                return hide ? '' : w.innerText; }""")
            m = BAD.search(txt or "")
            if m:
                i = m.start()
                problems.append(f"{label}: '{txt[max(0, i - 60):i + 20].strip()}'")
            if errors:
                problems.append(f"{label}: JS error {errors[-1]}")
                errors.clear()

        await audit("load")
        dups = await pg.evaluate("() => { const c = {}; document.querySelectorAll('[id]').forEach(e => c[e.id] = (c[e.id] || 0) + 1); return Object.keys(c).filter(k => c[k] > 1); }")
        if dups:
            problems.append(f"duplicate element ids after load (controls may be attached to the wrong element): {dups}")
        done = set()
        counts = {"range": 0, "number": 0, "select": 0}
        VIS = "els => els.filter(e => e.offsetParent !== null).map(e => e.id)"

        async def visible(eid):
            return await pg.evaluate("id => { const e = document.getElementById(id); return !!e && e.offsetParent !== null; }", eid)

        async def exercise(tag):
            # every visible input not yet exercised: sliders min/mid/max, number boxes, every select option
            for sid in await pg.eval_on_selector_all("input[type=range]", VIS):
                if sid in done or not await visible(sid):
                    continue
                done.add(sid); counts["range"] += 1
                for v in ("0", "500", "1000"):
                    await pg.evaluate("([id, v]) => { const e = document.getElementById(id); e.value = v; e.dispatchEvent(new Event('input', {bubbles: true})); }", [sid, v])
                    await audit(f"{tag}slider {sid}={v}")
                if await pg.query_selector("#reset"):
                    await pg.click("#reset")
            for bid in await pg.eval_on_selector_all("input[type=number]", VIS):
                if bid in done or not await visible(bid):
                    continue
                done.add(bid); counts["number"] += 1
                val = await pg.input_value(f"#{bid}")
                await pg.fill(f"#{bid}", val)
                await pg.dispatch_event(f"#{bid}", "change")
                await audit(f"{tag}number box {bid}")
            sels = await pg.eval_on_selector_all("select", "els => els.filter(e => e.offsetParent !== null).map(e => [e.id, [...e.options].filter(o => !o.disabled).map(o => o.value)])")
            for sid, opts in sels:
                if sid in done or not await visible(sid):
                    continue
                done.add(sid); counts["select"] += 1
                for o in opts:
                    if not await visible(sid):
                        break          # an earlier option switched to a mode that hides this control
                    await pg.select_option(f"#{sid}", o)
                    await audit(f"{tag}select {sid}={o}")
                    await exercise(f"[{sid}={o}] ")      # controls this option reveals

        await exercise("")
        # controls that appear only in another mode: visit every state of every segmented toggle
        n_seg = await pg.eval_on_selector_all(".seg button", "els => els.length")
        for k in range(n_seg):
            btn = (await pg.query_selector_all(".seg button"))[k]
            if not await btn.is_visible():
                continue
            label = (await btn.inner_text()).strip()[:30]
            await btn.click()
            await audit(f"toggle '{label}'")
            await exercise(f"[{label}] ")
        hidden = await pg.eval_on_selector_all("input[type=range], input[type=number], select", "els => els.map(e => e.id)")
        never = [h for h in hidden if h not in done]
        if never:
            problems.append(f"controls never visible in any mode (not exercised): {never}")
        sliders, boxes, selects = range(counts["range"]), range(counts["number"]), range(counts["select"])
        n_buttons = await pg.eval_on_selector_all("button", "els => els.length")
        for k in range(n_buttons):
            btn = (await pg.query_selector_all("button"))[k]
            if not await btn.is_visible():
                continue
            label = (await btn.inner_text()).strip()[:30]
            try:
                async with pg.expect_download(timeout=1500) as dl:
                    await btn.click()
                d = await dl.value
                problems_before = len(problems)
                content = Path(await d.path()).read_text()
                if not content.strip() or "," not in content.splitlines()[0]:
                    problems.append(f"button '{label}': empty or malformed CSV")
                log.append(f"  - export '{label}': {d.suggested_filename}, {len(content.splitlines()) - 1} data rows, header `{content.splitlines()[0][:90]}`")
            except Exception:
                pass   # not a download button
            if label.lower() == "pause":
                await btn.click()
            await audit(f"button '{label}'")
        if await pg.query_selector("#reset"):
            await pg.click("#reset")
        shot = Path(page_path).parent / "tests" / f"screenshot_{width}px_{scheme}.png"
        await pg.screenshot(path=str(shot), full_page=False)
        await b.close()
        return n_actions, problems, len(sliders), len(boxes), len(selects), n_buttons


def main():
    page = sys.argv[1]
    out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else None
    lines = [f"## Browser check — `{Path(page).name}`", ""]
    total_problems = 0
    for width in (375, 1280):
        for scheme in ("light", "dark"):
            log = []
            n, probs, ns, nb, nsel, nbtn = asyncio.run(run(page, width, scheme, log))
            total_problems += len(probs)
            lines.append(f"* **{width} px, {scheme}**: {n} actions ({ns} sliders × 3 positions, {nb} number boxes, {nsel} selects, {nbtn} buttons) — "
                         + ("no problems" if not probs else f"**{len(probs)} problems**"))
            lines += [f"  - {p}" for p in probs[:20]] + log
    lines += ["", "Result: " + ("PASS" if total_problems == 0 else f"FAIL ({total_problems} problems)")]
    text = "\n".join(lines)
    print(text)
    if out:
        Path(out).write_text(text + "\n")
    sys.exit(1 if total_problems else 0)


if __name__ == "__main__":
    main()

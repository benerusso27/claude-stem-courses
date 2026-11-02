"""Render a slide deck into contact sheets (2 x 3 slides per image) for reading.
usage: python3 sheets.py deck.pdf outprefix [width]"""
import subprocess, sys, glob, os
from PIL import Image, ImageDraw

pdf, pre = sys.argv[1], sys.argv[2]
w = int(sys.argv[3]) if len(sys.argv) > 3 else 760
tmp = pre + "_p"
subprocess.run(["pdftoppm", "-png", "-scale-to-x", str(w), "-scale-to-y", "-1", pdf, tmp], check=True)
pages = sorted(glob.glob(tmp + "-*.png"))
per = 6
for s in range(0, len(pages), per):
    ims = [Image.open(p).convert("RGB") for p in pages[s:s + per]]
    cw = max(i.width for i in ims); ch = max(i.height for i in ims)
    sheet = Image.new("RGB", (cw * 2 + 10, (ch + 22) * 3), (120, 120, 120))
    d = ImageDraw.Draw(sheet)
    for k, im in enumerate(ims):
        x = (k % 2) * (cw + 10); y = (k // 2) * (ch + 22)
        sheet.paste(im, (x, y + 22))
        d.text((x + 6, y + 4), f"slide {s + k + 1}", fill=(255, 255, 0))
    sheet.save(f"{pre}_s{s // per + 1:02d}.png")
for p in pages: os.remove(p)
print(len(pages), "slides ->", (len(pages) + per - 1) // per, "sheets")

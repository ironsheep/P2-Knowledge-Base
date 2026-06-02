#!/usr/bin/env python3
# bmp2png.py — convert captured window .bmp files to .png figures for the manual.
# Run in the doc container (which has Pillow: pip install --user Pillow).
#   captures/screenshots/*.bmp  ->  ../assets/*.png
# Skips empty files and reports each image's size + flat-color warning (a single-color
# image means the capture rendered blank — fix the example's timing and recapture).
import glob, os, sys
from PIL import Image

here = os.path.dirname(os.path.abspath(__file__))
src  = os.path.join(here, "captures", "screenshots")
dst  = os.path.join(here, "..", "assets")
os.makedirs(dst, exist_ok=True)

n = 0
for bmp in sorted(glob.glob(os.path.join(src, "*.bmp"))):
    name = os.path.splitext(os.path.basename(bmp))[0]
    if os.path.getsize(bmp) == 0:
        print(f"  skip  {name}  (0 bytes — recapture)"); continue
    try:
        im = Image.open(bmp).convert("RGB")
    except Exception as e:
        print(f"  FAIL  {name}  ({e})"); continue
    out = os.path.join(dst, name + ".png")
    im.save(out, "PNG")
    flat = len(im.getcolors(maxcolors=2) or [1, 2]) == 1
    warn = "  <-- WARNING: flat single-color image, capture is blank" if flat else ""
    print(f"  ok    {name}  {im.size[0]}x{im.size[1]} -> assets/{name}.png{warn}")
    n += 1

print(f"{n} png written to assets/")

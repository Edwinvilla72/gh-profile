#!/usr/bin/env python3
"""
Converts a photo into the ASCII portrait used on the left panel of the card.

Run this ONLY when you want to change the photo:
    pip install pillow
    python photo_to_ascii.py my_photo.jpg

It writes portrait.txt, which generate_profile.py reads. (The daily GitHub Action never runs this — it needs no dependencies.)
"""
import sys
from pathlib import Path
from PIL import Image, ImageEnhance, ImageOps

SRC = sys.argv[1] if len(sys.argv) > 1 else "photo.jpg"

# crop box on the source image (left, top, right, bottom) — head + torso
CROP = (186, 238, 600, 902)

COLS = 64            # characters across
CELL_ASPECT = 1.72   # svg line-height / char-width
CONTRAST = 1.35

# darkest -> lightest
RAMP = "@%#*+=-:. "


def build(gray):
    w, h = gray.size
    rows = max(1, int(COLS * (h / w) / CELL_ASPECT))
    small = gray.resize((COLS, rows), Image.LANCZOS)
    px = small.load()
    n = len(RAMP) - 1
    lines = []
    for y in range(rows):
        line = []
        for x in range(COLS):
            v = 255 - px[x, y]          # dark pixels -> dense glyphs (ink)
            line.append(RAMP[round((255 - v) / 255 * n)])
        lines.append("".join(line).rstrip())
    return "\n".join(lines)


def main():
    im = Image.open(SRC).convert("RGB").crop(CROP)
    gray = ImageOps.autocontrast(im.convert("L"), cutoff=2)
    gray = ImageEnhance.Contrast(gray).enhance(CONTRAST)

    out = Path(__file__).parent
    (out / "portrait.txt").write_text(build(gray), encoding="utf-8")
    print("wrote portrait.txt")


if __name__ == "__main__":
    main()

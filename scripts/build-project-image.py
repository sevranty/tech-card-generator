#!/usr/bin/env python3
"""Build deterministic project image and GitHub social preview assets."""

from __future__ import annotations

import hashlib
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
SIZES = {
    "project-image.png": (1600, 800),
    "social-preview.png": (1280, 640),
}


def get_font(size: int, bold: bool = False):
    candidates = [
        "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/Library/Fonts/Arial Bold.ttf" if bold else "/Library/Fonts/Arial.ttf",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            pass
    return ImageFont.load_default()


def ln(draw, points, width=3, fill=20):
    draw.line(points, fill=fill, width=width, joint="curve")


def machine(draw, box):
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0

    # Distant, middle and foreground planes.
    ln(draw, [(x0, y0+h*.30), (x0+w*.22, y0+h*.22),
              (x0+w*.42, y0+h*.29), (x1, y0+h*.24)], 2, 190)
    ln(draw, [(x0, y0+h*.50), (x0+w*.28, y0+h*.44),
              (x0+w*.58, y0+h*.49), (x1, y0+h*.43)], 2, 160)
    ln(draw, [(x0, y0+h*.78), (x0+w*.30, y0+h*.73),
              (x0+w*.68, y0+h*.79), (x1, y0+h*.72)], 3, 125)

    # Local white paper zone.
    draw.ellipse((x0+w*.13, y0+h*.24, x0+w*.87, y0+h*.80), fill=255)

    # Tracks, body and cab.
    track = (x0+w*.18, y0+h*.55, x0+w*.76, y0+h*.78)
    draw.rounded_rectangle(track, radius=int(h*.10), fill=250, outline=15, width=7)
    draw.rounded_rectangle((track[0]+20, track[1]+16, track[2]-18, track[3]-16),
                           radius=int(h*.07), outline=35, width=4)
    for cx in (.29, .45, .61):
        r = int(h*.055)
        x, y = x0+w*cx, y0+h*.665
        draw.ellipse((x-r, y-r, x+r, y+r), fill=255, outline=20, width=4)

    body = [(x0+w*.31, y0+h*.54), (x0+w*.38, y0+h*.37),
            (x0+w*.63, y0+h*.37), (x0+w*.69, y0+h*.56)]
    draw.polygon(body, fill=255)
    ln(draw, body+[body[0]], 6, 15)
    cab = [(x0+w*.41, y0+h*.37), (x0+w*.45, y0+h*.25),
           (x0+w*.60, y0+h*.25), (x0+w*.64, y0+h*.37)]
    draw.polygon(cab, fill=255)
    ln(draw, cab+[cab[0]], 6, 15)
    draw.rectangle((x0+w*.465, y0+h*.275, x0+w*.515, y0+h*.345),
                   outline=20, width=3)
    draw.rectangle((x0+w*.53, y0+h*.275, x0+w*.585, y0+h*.345),
                   outline=20, width=3)

    # Mechanically connected blade in contact with soil.
    ln(draw, [(x0+w*.66, y0+h*.48), (x0+w*.80, y0+h*.56)], 6, 15)
    ln(draw, [(x0+w*.66, y0+h*.60), (x0+w*.80, y0+h*.62)], 6, 15)
    blade = [(x0+w*.79, y0+h*.48), (x0+w*.91, y0+h*.51),
             (x0+w*.90, y0+h*.72), (x0+w*.80, y0+h*.70)]
    draw.polygon(blade, fill=255)
    ln(draw, blade+[blade[0]], 7, 15)
    ln(draw, [(blade[0][0]+5, blade[0][1]+35),
              (blade[1][0]-4, blade[1][1]+35)], 3, 30)

    soil = [(x0+w*.79, y0+h*.70), (x0+w*.84, y0+h*.66),
            (x0+w*.91, y0+h*.70), (x0+w*.96, y0+h*.76),
            (x0+w*.80, y0+h*.76)]
    draw.polygon(soil, fill=245)
    ln(draw, soil+[soil[0]], 3, 90)

    for offset in range(0, 70, 14):
        ln(draw, [(x0+w*.35+offset, y0+h*.43),
                  (x0+w*.38+offset, y0+h*.48)], 2, 45)


def detail(draw, box):
    x0, y0, x1, y1 = box
    w, h = x1-x0, y1-y0
    blade = [(x0+w*.18, y0+h*.24), (x0+w*.82, y0+h*.24),
             (x0+w*.76, y0+h*.70), (x0+w*.24, y0+h*.70)]
    draw.polygon(blade, fill=255)
    ln(draw, blade+[blade[0]], 7, 15)
    ln(draw, [(x0+w*.20, y0+h*.45), (x0+w*.80, y0+h*.45)], 4, 30)
    ln(draw, [(x0+w*.23, y0+h*.61), (x0+w*.77, y0+h*.61)], 3, 30)
    for pos in (.30, .45, .60, .72):
        x = x0+w*pos
        ln(draw, [(x, y0+h*.25), (x-8, y0+h*.69)], 2, 50)


def build(size):
    width, height = size
    image = Image.new("L", size, 255)
    draw = ImageDraw.Draw(image)
    margin = int(min(size) * .10)
    draw.rounded_rectangle((margin, margin, width-margin, height-margin),
                           radius=int(height*.035), fill=255, outline=20, width=3)

    left = margin + int(width*.035)
    draw.text((left, margin+height*.05), "machinery-card-generator",
              font=get_font(int(height*.035), True), fill=20)
    draw.text((left, margin+height*.15), "ONE REAL MACHINE",
              font=get_font(int(height*.052), True), fill=10)
    draw.text((left, margin+height*.24), "ANALYZE • GENERATE • VERIFY",
              font=get_font(int(height*.032)), fill=25)

    x, y = left, margin+height*.34
    for chip in ("2×1 CARD", "B/W", "SAFE 10%", "NO BRANDS"):
        f = get_font(int(height*.024), True)
        box = draw.textbbox((0, 0), chip, font=f)
        cw, ch = box[2]-box[0]+int(width*.025), int(height*.065)
        draw.rounded_rectangle((x, y, x+cw, y+ch), radius=ch//2,
                               outline=25, width=2)
        draw.text((x+int(width*.012), y+int(height*.016)), chip, font=f, fill=20)
        x += cw + int(width*.012)

    card_x = int(width*.50)
    card_y = margin + int(height*.07)
    square = min(height-2*margin-int(height*.14),
                 (width-margin-int(width*.02)-card_x)//2)
    card_bottom = card_y + square
    draw.rounded_rectangle((card_x, card_y, card_x+2*square, card_bottom),
                           radius=int(height*.025), fill=255, outline=20, width=3)
    draw.line((card_x+square, card_y, card_x+square, card_bottom),
              fill=20, width=3)

    machine(draw, (card_x+10, card_y+10, card_x+square-10, card_bottom-80))
    detail(draw, (card_x+square+25, card_y+100,
                  card_x+2*square-25, card_bottom-105))

    draw.text((card_x+square//2, card_bottom-50), "BULLDOZER MOVES SOIL",
              anchor="mm", font=get_font(int(height*.024), True), fill=20)
    draw.text((card_x+square+square//2, card_y+50), "BULLDOZER",
              anchor="mm", font=get_font(int(height*.044), True), fill=15)
    draw.text((card_x+square+square//2, card_bottom-50), "WIDE BLADE",
              anchor="mm", font=get_font(int(height*.029), True), fill=20)
    draw.text((left, height-margin-int(height*.04)),
              "One subject • real mechanics • visible action",
              font=get_font(int(height*.024)), fill=70)
    return image.convert("1")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    ASSETS.mkdir(parents=True, exist_ok=True)
    for name, size in SIZES.items():
        path = ASSETS / name
        build(size).save(path, optimize=True)
        with Image.open(path) as image:
            assert image.size == size
        assert path.stat().st_size < 1_000_000
        print(f"{path.relative_to(ROOT)} {size[0]}x{size[1]} sha256={digest(path)}")
    print("Project image validation passed")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Build deterministic project image and GitHub social preview assets."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"

PROJECT_SIZE = (1600, 800)
SOCIAL_SIZE = (1280, 640)
SAFE_MARGIN = 0.08


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    names = [
        "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/Library/Fonts/Arial Bold.ttf" if bold else "/Library/Fonts/Arial.ttf",
    ]
    for name in names:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def line(draw: ImageDraw.ImageDraw, points, width=3, fill=20):
    draw.line(points, fill=fill, width=width, joint="curve")


def draw_bulldozer(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int]) -> None:
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0

    # Three environment levels, intentionally lighter than the machine.
    line(draw, [(x0, y0 + int(h * .30)), (x0 + int(w * .20), y0 + int(h * .22)),
                (x0 + int(w * .38), y0 + int(h * .29)), (x1, y0 + int(h * .24))], 2, 190)
    line(draw, [(x0, y0 + int(h * .50)), (x0 + int(w * .25), y0 + int(h * .45)),
                (x0 + int(w * .55), y0 + int(h * .49)), (x1, y0 + int(h * .43))], 2, 160)
    line(draw, [(x0, y0 + int(h * .78)), (x0 + int(w * .28), y0 + int(h * .73)),
                (x0 + int(w * .65), y0 + int(h * .79)), (x1, y0 + int(h * .72))], 3, 125)

    # Local white separation zone behind the machine.
    halo = (x0 + int(w * .13), y0 + int(h * .24), x0 + int(w * .86), y0 + int(h * .79))
    draw.ellipse(halo, fill=255)

    # Tracks.
    track = (x0 + int(w * .18), y0 + int(h * .55), x0 + int(w * .76), y0 + int(h * .78))
    draw.rounded_rectangle(track, radius=int(h * .10), fill=250, outline=15, width=7)
    inner = (track[0] + 20, track[1] + 16, track[2] - 18, track[3] - 16)
    draw.rounded_rectangle(inner, radius=int(h * .07), outline=35, width=4)
    for cx in (0.29, 0.45, 0.61):
        r = int(h * .055)
        c = x0 + int(w * cx)
        cy = y0 + int(h * .665)
        draw.ellipse((c-r, cy-r, c+r, cy+r), fill=255, outline=20, width=4)

    # Body and cab.
    body = [
        (x0 + int(w * .31), y0 + int(h * .54)),
        (x0 + int(w * .38), y0 + int(h * .37)),
        (x0 + int(w * .63), y0 + int(h * .37)),
        (x0 + int(w * .69), y0 + int(h * .56)),
    ]
    draw.polygon(body, fill=255, outline=15)
    line(draw, body + [body[0]], 6, 15)
    cab = [
        (x0 + int(w * .41), y0 + int(h * .37)),
        (x0 + int(w * .45), y0 + int(h * .25)),
        (x0 + int(w * .60), y0 + int(h * .25)),
        (x0 + int(w * .64), y0 + int(h * .37)),
    ]
    draw.polygon(cab, fill=255, outline=15)
    line(draw, cab + [cab[0]], 6, 15)
    draw.rectangle((x0 + int(w * .465), y0 + int(h * .275),
                    x0 + int(w * .515), y0 + int(h * .345)), outline=20, width=3)
    draw.rectangle((x0 + int(w * .53), y0 + int(h * .275),
                    x0 + int(w * .585), y0 + int(h * .345)), outline=20, width=3)

    # Blade arms and working blade in contact with soil.
    line(draw, [(x0 + int(w * .66), y0 + int(h * .48)),
                (x0 + int(w * .80), y0 + int(h * .56))], 6, 15)
    line(draw, [(x0 + int(w * .66), y0 + int(h * .60)),
                (x0 + int(w * .80), y0 + int(h * .62))], 6, 15)
    blade = [
        (x0 + int(w * .79), y0 + int(h * .48)),
        (x0 + int(w * .91), y0 + int(h * .51)),
        (x0 + int(w * .90), y0 + int(h * .72)),
        (x0 + int(w * .80), y0 + int(h * .70)),
    ]
    draw.polygon(blade, fill=255, outline=15)
    line(draw, blade + [blade[0]], 7, 15)
    line(draw, [(blade[0][0]+5, blade[0][1]+35), (blade[1][0]-4, blade[1][1]+35)], 3, 30)
    line(draw, [(blade[3][0]+4, blade[3][1]-18), (blade[2][0]-4, blade[2][1]-18)], 3, 30)

    # Material interaction and visible action result.
    soil = [
        (x0 + int(w * .79), y0 + int(h * .70)),
        (x0 + int(w * .84), y0 + int(h * .66)),
        (x0 + int(w * .91), y0 + int(h * .70)),
        (x0 + int(w * .96), y0 + int(h * .76)),
        (x0 + int(w * .80), y0 + int(h * .76)),
    ]
    draw.polygon(soil, fill=245, outline=90)
    line(draw, soil + [soil[0]], 3, 90)
    for i in range(5):
        sx = x0 + int(w * (.82 + i * .025))
        line(draw, [(sx, y0 + int(h * .70)), (sx + 8, y0 + int(h * .74))], 2, 120)

    # Hatching on the machine.
    for offset in range(0, 70, 14):
        line(draw, [(x0 + int(w * .35) + offset, y0 + int(h * .43)),
                    (x0 + int(w * .38) + offset, y0 + int(h * .48))], 2, 45)


def draw_detail(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int]) -> None:
    x0, y0, x1, y1 = box
    w, h = x1-x0, y1-y0
    blade = [
        (x0 + int(w*.18), y0 + int(h*.24)),
        (x0 + int(w*.82), y0 + int(h*.24)),
        (x0 + int(w*.76), y0 + int(h*.70)),
        (x0 + int(w*.24), y0 + int(h*.70)),
    ]
    draw.polygon(blade, fill=255, outline=15)
    line(draw, blade + [blade[0]], 7, 15)
    line(draw, [(x0 + int(w*.20), y0 + int(h*.45)), (x0 + int(w*.80), y0 + int(h*.45))], 4, 30)
    line(draw, [(x0 + int(w*.23), y0 + int(h*.61)), (x0 + int(w*.77), y0 + int(h*.61))], 3, 30)
    for pos in (.30, .45, .60, .72):
        xx = x0 + int(w*pos)
        line(draw, [(xx, y0 + int(h*.25)), (xx-8, y0 + int(h*.69))], 2, 50)


def build(size: tuple[int, int]) -> Image.Image:
    width, height = size
    img = Image.new("L", size, 255)
    d = ImageDraw.Draw(img)
    margin = int(min(width, height) * SAFE_MARGIN)
    d.rounded_rectangle((margin, margin, width-margin, height-margin),
                        radius=int(height*.035), fill="white", outline=20, width=3)

    # Left product message.
    lx = margin + int(width*.035)
    d.text((lx, margin + int(height*.06)), "machinery-card-generator",
           font=font(int(height*.035), True), fill=20)
    d.text((lx, margin + int(height*.16)), "ONE REAL MACHINE",
           font=font(int(height*.052), True), fill=10)
    d.text((lx, margin + int(height*.25)), "ANALYZE • GENERATE • VERIFY",
           font=font(int(height*.032), False), fill=25)

    chips = ["2×1 CARD", "B/W", "SAFE 10%", "NO BRANDS"]
    cx = lx
    cy = margin + int(height*.35)
    for chip in chips:
        f = font(int(height*.024), True)
        bb = d.textbbox((0, 0), chip, font=f)
        cw = bb[2]-bb[0] + int(width*.025)
        ch = int(height*.065)
        d.rounded_rectangle((cx, cy, cx+cw, cy+ch), radius=ch//2, outline=25, width=2)
        d.text((cx + int(width*.012), cy + int(height*.016)), chip, font=f, fill=20)
        cx += cw + int(width*.012)

    # Right educational card: two equal square panels.
    card_x0 = int(width*.50)
    card_y0 = margin + int(height*.08)
    card_h = height - 2*margin - int(height*.16)
    square = card_h
    card_w = square*2
    card_x1 = min(width-margin-int(width*.02), card_x0+card_w)
    square = (card_x1-card_x0)//2
    card_y1 = card_y0 + square
    d.rounded_rectangle((card_x0, card_y0, card_x0+2*square, card_y1),
                        radius=int(height*.025), fill="white", outline=20, width=3)
    d.line((card_x0+square, card_y0, card_x0+square, card_y1), fill=20, width=3)

    draw_bulldozer(d, (card_x0+10, card_y0+10, card_x0+square-10, card_y1-80))
    draw_detail(d, (card_x0+square+25, card_y0+110, card_x0+2*square-25, card_y1-110))

    # ASCII-only labels keep rendering portable.
    d.text((card_x0+square//2, card_y1-55), "BULLDOZER MOVES SOIL",
           anchor="mm", font=font(int(height*.025), True), fill=20)
    d.text((card_x0+square+square//2, card_y0+55), "BULLDOZER",
           anchor="mm", font=font(int(height*.046), True), fill=15)
    d.text((card_x0+square+square//2, card_y1-55), "WIDE BLADE",
           anchor="mm", font=font(int(height*.030), True), fill=20)

    d.text((lx, height-margin-int(height*.045)),
           "One subject • real mechanics • visible action",
           font=font(int(height*.026), False), fill=70)
    return img.convert("RGB")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.parse_args()
    ASSETS.mkdir(parents=True, exist_ok=True)

    outputs = {
        ASSETS / "project-image.png": PROJECT_SIZE,
        ASSETS / "social-preview.png": SOCIAL_SIZE,
    }
    for path, size in outputs.items():
        image = build(size)
        image.save(path, optimize=True)
        if Image.open(path).size != size:
            raise SystemExit(f"unexpected dimensions: {path}")
        if path.stat().st_size >= 1_000_000:
            raise SystemExit(f"file exceeds 1 MB: {path}")
        print(f"{path.relative_to(ROOT)} {size[0]}x{size[1]} sha256={sha256(path)}")

    print("Project image validation passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

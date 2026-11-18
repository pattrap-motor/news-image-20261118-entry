#!/usr/bin/env python3
"""Draw the 18 November 2026 world-news front page (1024x1024, deterministic).

Run: python3 draw.py  -> writes entry.png next to this file.
Only Pillow is used; no network, no randomness, no clock.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
M = 30  # page margin
PAPER = (246, 241, 229)
INK = (17, 17, 17)
RED = (176, 30, 36)
GREY = (90, 86, 76)
RULE = (40, 40, 40)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_I = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def text_w(d, s, f):
    """Width of s in font f."""
    return d.textbbox((0, 0), s, font=f)[2]


def wrap(d, s, f, width):
    """Greedy word wrap; returns list of lines that fit in width."""
    lines, cur = [], ""
    for word in s.split():
        trial = (cur + " " + word).strip()
        if text_w(d, trial, f) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(d, x, y, lines, f, fill, leading):
    for line in lines:
        d.text((x, y), line, font=f, fill=fill)
        y += leading
    return y


def fit_size(d, s, path, start, width, minimum=10):
    """Largest font size (<= start) that fits s on one line."""
    size = start
    while size > minimum and text_w(d, s, font(path, size)) > width:
        size -= 1
    return size


def hline(d, y, x0=None, x1=None, fill=RULE, width=2):
    d.line([(x0 if x0 is not None else M, y), (x1 if x1 is not None else W - M, y)],
           fill=fill, width=width)


def star(d, cx, cy, r_out, r_in, fill, points=5):
    import math
    pts = []
    for i in range(points * 2):
        r = r_out if i % 2 == 0 else r_in
        a = math.pi * i / points - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=fill)


def burst(d, cx, cy, r, fill):
    star(d, cx, cy, r, r * 0.45, fill, points=8)


# ---------------------------------------------------------------- lead art
def draw_lead_art(d, x0, y0, x1, y1):
    """Night strait: bridge with a collapsed road span in the water."""
    d.rectangle([x0, y0, x1, y1], fill=(27, 42, 74))
    # moon + stars
    d.ellipse([x1 - 70, y0 + 14, x1 - 34, y0 + 50], fill=(238, 232, 200))
    for sx, sy in [(x0 + 40, y0 + 22), (x0 + 120, y0 + 12), (x0 + 200, y0 + 30),
                   (x0 + 300, y0 + 16), (x0 + 420, y0 + 26), (x0 + 560, y0 + 14)]:
        d.ellipse([sx, sy, sx + 3, sy + 3], fill=(220, 220, 220))
    # sea
    sea_y = y0 + int((y1 - y0) * 0.55)
    d.rectangle([x0, sea_y, x1, y1], fill=(38, 84, 110))
    for wx in range(x0 + 30, x1 - 60, 90):
        d.line([(wx, sea_y + 18), (wx + 34, sea_y + 18)], fill=(120, 170, 195), width=2)
        d.line([(wx + 12, sea_y + 44), (wx + 46, sea_y + 44)], fill=(120, 170, 195), width=2)
    # bridge towers (two pylons) and intact deck
    deck_y = y0 + int((y1 - y0) * 0.42)
    for tx in (x0 + 150, x0 + 700):
        d.rectangle([tx, y0 + 18, tx + 16, deck_y + 6], fill=(200, 198, 190))
        d.rectangle([tx - 6, y0 + 10, tx + 22, y0 + 20], fill=(200, 198, 190))
    d.rectangle([x0, deck_y, x0 + 400, deck_y + 10], fill=(214, 210, 198))
    d.rectangle([x0 + 640, deck_y, x1, deck_y + 10], fill=(214, 210, 198))
    # collapsed span: tilted deck sliding into the water (the gap)
    d.polygon([(x0 + 400, deck_y), (x0 + 640, deck_y + 10),
               (x0 + 620, deck_y + 34), (x0 + 396, deck_y + 26)], fill=(150, 146, 134))
    d.polygon([(x0 + 470, deck_y + 22), (x0 + 560, deck_y + 30),
               (x0 + 540, y1 - 12), (x0 + 480, y1 - 8)], fill=(120, 116, 106))
    # splash where the span hit the water
    for sx, sy, sr in [(x0 + 500, y1 - 26, 12), (x0 + 530, y1 - 18, 9),
                       (x0 + 470, y1 - 16, 8)]:
        d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(190, 220, 235))
    # explosion + smoke over the gap
    burst(d, x0 + 520, deck_y - 6, 34, (240, 140, 40))
    burst(d, x0 + 520, deck_y - 6, 18, (250, 200, 90))
    for cx, cy, cr in [(x0 + 470, deck_y - 34, 16), (x0 + 500, deck_y - 52, 20),
                       (x0 + 540, deck_y - 40, 14)]:
        d.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=(110, 110, 112))
    # caption strip
    d.rectangle([x0, y1 - 26, x1, y1], fill=(0, 0, 0))
    cap = "THE KERCH ROAD SPAN, DOWN IN THE STRAIT — UKRAINE"
    d.text((x0 + 10, y1 - 22), cap, font=font(SANS_B, 15), fill=(255, 255, 255))


# ---------------------------------------------------------------- grid art
def draw_bahrain(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(24, 34, 58))
    for sx, sy in [(x0 + 18, y0 + 12), (x0 + 60, y0 + 8), (x0 + 140, y0 + 14),
                   (x0 + 180, y0 + 10)]:
        d.ellipse([sx, sy, sx + 2, sy + 2], fill=(220, 220, 220))
    # radar dome + sweeping beam
    d.pieslice([x0 + 55, y1 - 62, x0 + 145, y1 + 28], 180, 360, fill=(210, 208, 200))
    d.rectangle([x0 + 52, y1 - 14, x0 + 148, y1 - 6], fill=(160, 158, 150))
    d.line([(x0 + 100, y1 - 60), (x0 + 168, y0 + 34)], fill=(120, 200, 120), width=3)
    # drone silhouette (light grey so it reads on the night sky)
    dx, dy = x0 + 52, y0 + 34
    d.ellipse([dx - 12, dy - 6, dx + 12, dy + 6], fill=(170, 170, 170))
    for rx in (dx - 22, dx + 22):
        d.line([(rx - 12, dy - 12), (rx + 12, dy - 12)], fill=(170, 170, 170), width=3)
    d.line([(dx - 22, dy - 12), (dx - 12, dy - 4)], fill=(170, 170, 170), width=2)
    d.line([(dx + 22, dy - 12), (dx + 12, dy - 4)], fill=(170, 170, 170), width=2)
    # intercept burst + label (top-right, clear of the dome)
    burst(d, x0 + 168, y0 + 52, 16, (250, 200, 60))
    d.text((x1 - 108, y0 + 8), "INTERCEPTED", font=font(SANS_B, 13), fill=(250, 200, 60))


def mini_flag_us(d, x0, y0, w, h):
    for i in range(7):
        d.rectangle([x0, y0 + i * h // 7, x0 + w, y0 + (i + 1) * h // 7],
                    fill=(178, 34, 52) if i % 2 == 0 else (255, 255, 255))
    d.rectangle([x0, y0, x0 + w * 0.45, y0 + h * 0.55], fill=(40, 60, 120))
    for r in range(3):
        for c in range(4):
            d.ellipse([x0 + 5 + c * 11, y0 + 5 + r * 10, x0 + 9 + c * 11, y0 + 9 + r * 10],
                      fill=(255, 255, 255))


def mini_flag_in(d, x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h // 3], fill=(255, 153, 51))
    d.rectangle([x0, y0 + h // 3, x0 + w, y0 + 2 * h // 3], fill=(255, 255, 255))
    d.rectangle([x0, y0 + 2 * h // 3, x0 + w, y0 + h], fill=(19, 136, 8))
    cx, cy, r = x0 + w // 2, y0 + h // 2, h // 6
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(0, 0, 128), width=2)


def mini_flag_jp(d, x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(255, 255, 255))
    d.ellipse([x0 + w // 2 - h // 5, y0 + h // 2 - h // 5,
               x0 + w // 2 + h // 5, y0 + h // 2 + h // 5], fill=(188, 0, 45))


def mini_flag_au(d, x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(0, 40, 104))
    d.rectangle([x0, y0, x0 + w * 0.45, y0 + h * 0.5], fill=(200, 200, 210))
    d.line([(x0, y0), (x0 + w * 0.45, y0 + h * 0.5)], fill=(188, 0, 45), width=3)
    d.line([(x0 + w * 0.45, y0), (x0, y0 + h * 0.5)], fill=(188, 0, 45), width=3)
    for sx, sy in [(x0 + w * 0.75, y0 + h * 0.3), (x0 + w * 0.85, y0 + h * 0.6),
                   (x0 + w * 0.6, y0 + h * 0.7)]:
        star(d, sx, sy, 6, 2.5, (255, 255, 255))


def draw_manila(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(232, 226, 205))
    fw, fh = (x1 - x0 - 24) // 2, (y1 - y0 - 24) // 2
    mini_flag_us(d, x0 + 8, y0 + 8, fw, fh)
    mini_flag_in(d, x0 + 16 + fw, y0 + 8, fw, fh)
    mini_flag_jp(d, x0 + 8, y0 + 16 + fh, fw, fh)
    mini_flag_au(d, x0 + 16 + fw, y0 + 16 + fh, fw, fh)


def mini_flag_cn(d, x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(222, 41, 16))
    star(d, x0 + w * 0.18, y0 + h * 0.25, 12, 5, (255, 222, 0))
    for sx, sy in [(x0 + w * 0.4, y0 + h * 0.16), (x0 + w * 0.48, y0 + h * 0.32),
                   (x0 + w * 0.4, y0 + h * 0.48), (x0 + w * 0.28, y0 + h * 0.42)]:
        star(d, sx, sy, 5, 2, (255, 222, 0))


def mini_flag_ca(d, x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w * 0.25, y0 + h], fill=(255, 0, 0))
    d.rectangle([x0 + w * 0.25, y0, x0 + w * 0.75, y0 + h], fill=(255, 255, 255))
    d.rectangle([x0 + w * 0.75, y0, x0 + w, y0 + h], fill=(255, 0, 0))
    cx, cy = x0 + w // 2, y0 + h // 2
    leaf = [(cx, cy - 20), (cx + 6, cy - 8), (cx + 16, cy - 12), (cx + 12, cy - 2),
            (cx + 20, cy + 2), (cx + 9, cy + 8), (cx + 8, cy + 18), (cx + 3, cy + 12),
            (cx, cy + 20), (cx - 3, cy + 12), (cx - 8, cy + 18), (cx - 9, cy + 8),
            (cx - 20, cy + 2), (cx - 12, cy - 2), (cx - 16, cy - 12), (cx - 6, cy - 8)]
    d.polygon(leaf, fill=(255, 0, 0))


def draw_shenzhen(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(232, 226, 205))
    fw = (x1 - x0 - 24) // 2
    fh = (y1 - y0) - 16
    mini_flag_cn(d, x0 + 8, y0 + 8, fw, fh)
    mini_flag_ca(d, x0 + 16 + fw, y0 + 8, fw, fh)


def draw_london(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(232, 226, 205))
    # settlement houses
    for hx, hw in [(x0 + 14, 44), (x0 + 66, 52), (x0 + 126, 40)]:
        d.rectangle([hx, y1 - 66, hx + hw, y1 - 22], fill=(150, 120, 90))
        d.polygon([(hx - 4, y1 - 66), (hx + hw // 2, y1 - 88), (hx + hw + 4, y1 - 66)],
                  fill=(120, 60, 50))
    d.rectangle([x0 + 14, y1 - 22, x1 - 14, y1 - 14], fill=(120, 110, 95))
    # prohibition stamp
    cx, cy, r = (x0 + x1) // 2, (y0 + y1) // 2 - 6, 52
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=RED, width=7)
    d.line([(cx - r * 0.7, cy + r * 0.7), (cx + r * 0.7, cy - r * 0.7)],
           fill=RED, width=7)
    d.text((cx - 34, cy - 8), "NO", font=font(SANS_B, 26), fill=RED)


# ---------------------------------------------------------------- page
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # masthead
    title = "THE WORLD IN ONE DAY"
    size = fit_size(d, title, SERIF_B, 66, W - 2 * M)
    tf = font(SERIF_B, size)
    tw = text_w(d, title, tf)
    d.text(((W - tw) // 2, 26), title, font=tf, fill=INK)
    hline(d, 104, width=3)
    hline(d, 110, width=1)
    date = "WEDNESDAY  ·  18 NOVEMBER 2026"
    df = font(SANS_B, 34)
    dw = text_w(d, date, df)
    d.text(((W - dw) // 2, 122), date, font=df, fill=RED)
    sub = "ONE DAY  ·  FIVE STORIES  ·  THE WORLD"
    sf = font(SANS, 18)
    sw = text_w(d, sub, sf)
    d.text(((W - sw) // 2, 168), sub, font=sf, fill=GREY)

    # ---- lead story
    y = 196
    kf = font(SANS_B, 21)
    d.text((M, y), "UKRAINE  ·  KERCH STRAIT", font=kf, fill=RED)
    y += 30
    head = "THE BRIDGE FALLS"
    hf = font(SERIF_B, fit_size(d, head, SERIF_B, 82, W - 2 * M))
    d.text((M, y), head, font=hf, fill=INK)
    y += 96
    subhead = ("Ukraine's second strike in two days brings down the Kerch road span — "
               "rail reopens on one track as Moscow vows to rebuild.")
    shf = font(SANS, 25)
    y = draw_lines(d, M, y, wrap(d, subhead, shf, W - 2 * M), shf, INK, 32)
    y += 8
    art_h = 140
    draw_lead_art(d, M, y, W - M, y + art_h)
    y += art_h + 12
    hline(d, y, width=2)

    # ---- 2x2 grid
    y += 14
    cell_w = (W - 2 * M - 20) // 2
    cell_h = 168
    stories = [
        ("BAHRAIN  ·  GULF",
         "THIRD DRONE ATTACK IN FIVE DAYS",
         "Iran claims it hit a US radar at Isa Air Base; Bahrain and the US say the drones were intercepted — no damage.",
         draw_bahrain),
        ("MANILA  ·  ASEAN",
         "QUAD'S MINERALS PACT",
         "Trump, Modi, Takaichi and Albanese strike minerals deals; ASEAN closes as Trump flies to Shenzhen for Thursday's Xi–Putin talks.",
         draw_manila),
        ("SHENZHEN  ·  APEC",
         "CANADA–CHINA THAW",
         "Xi meets Carney in Shenzhen; China cuts tariffs on C$400m of Canadian pork and seafood as the two sides extend trade relief.",
         draw_shenzhen),
        ("LONDON  ·  WEST BANK",
         "UK SANCTIONS SETTLERS",
         "Britain sanctions eight Israeli settlement firms and a group that blocks Gaza aid, in a push to protect the two-state solution.",
         draw_london),
    ]
    for i, (kick, headline, body, art) in enumerate(stories):
        cx = M + (i % 2) * (cell_w + 20)
        cy = y + (i // 2) * (cell_h + 12)
        d.text((cx, cy), kick, font=font(SANS_B, 16), fill=RED)
        hf2 = font(SERIF_B, 25)
        hl = wrap(d, headline, hf2, cell_w)
        ty = draw_lines(d, cx, cy + 24, hl, hf2, INK, 29)
        # text column left, art panel right
        art_x0 = cx + cell_w - 196
        art_y0 = ty + 4
        art_y1 = cy + cell_h
        if art_y1 - art_y0 < 60:  # headline took 2 lines; shrink art, keep text clear
            art_y0 = cy + cell_h - 62
        bf = font(SANS, 17)
        bl = wrap(d, body, bf, art_x0 - cx - 10)
        draw_lines(d, cx, ty + 2, bl, bf, INK, 21)
        art(d, art_x0, art_y0, cx + cell_w, art_y1)
        if i % 2 == 0:
            d.line([(cx + cell_w + 10, cy), (cx + cell_w + 10, cy + cell_h)],
                   fill=(200, 194, 178), width=1)
    y += 2 * cell_h + 12 + 12

    # ---- ticker
    ty0 = y
    d.rectangle([M, ty0, W - M, ty0 + 50], fill=(17, 17, 17))
    tick = ("ALSO TODAY:  Eisenkot ally elected Knesset Speaker  •  Cyclone Akvan strengthens  •  "
            "Trump hints at Kim meeting  •  Pope Leo hit by rosary in Peru")
    tf2 = font(SANS_B, 17)
    tl = wrap(d, tick, tf2, W - 2 * M - 20)
    draw_lines(d, M + 10, ty0 + 6, tl[:2], tf2, (255, 255, 255), 19)

    # ---- footer
    fy = ty0 + 62
    foot = "Sources: Reuters · Al Jazeera · AFP · The Guardian · Bloomberg · AP — reported 18 November 2026"
    ff = font(SANS_I, 15)
    fw = text_w(d, foot, ff)
    d.text(((W - fw) // 2, fy), foot, font=ff, fill=GREY)

    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()

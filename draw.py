#!/usr/bin/env python3
"""news-image-20261125 v3: 30 stories in a 6x5 grid, hero Yemen.
Draws one 1024x1024 image summing up Wednesday 25 November 2026.
Every story verified against a primary source on 25 Nov 2026 (see work/v3-verification.md).
PIL + DejaVu fonts, stdlib otherwise. Deterministic: same bytes every run.
Layout: masthead 0-78, hero 78-368, label 368-392, grid 392-992 (6 cols x 5 rows,
tiles 159x113, 8px gaps, 14px margins), footer 992-1024.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
NAVY = (13, 27, 62)
NAVY2 = (24, 48, 96)
GOLD = (212, 175, 55)
INK = (18, 18, 18)
PAPER = (250, 247, 240)
CARD = (255, 255, 255)
GREY = (90, 90, 90)
RED = (178, 34, 34)

def font(name, size):
    return ImageFont.truetype(f"/usr/share/fonts/truetype/dejavu/{name}.ttf", size)

F_SERIF_B = lambda s: font("DejaVuSerif-Bold", s)
F_SERIF = lambda s: font("DejaVuSerif", s)
F_SANS_B = lambda s: font("DejaVuSans-Bold", s)
F_SANS = lambda s: font("DejaVuSans", s)

def wrap(d, text, f, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def sky(d, x, y, w, h, top, bot):
    steps = max(1, h // 4)
    for i in range(steps):
        t = i / max(1, steps - 1)
        c = tuple(int(top[k] + (bot[k] - top[k]) * t) for k in range(3))
        d.rectangle([x, y + i * 4, x + w, y + (i + 1) * 4], fill=c)

def sun(d, x, y, r, c):
    d.ellipse([x - r, y - r, x + r, y + r], fill=c)

def sea(d, x, y, w, h, c):
    d.rectangle([x, y, x + w, y + h], fill=c)
    for yy in range(y + 6, y + h, 9):
        d.line([x + 4, yy, x + w - 4, yy], fill=(255, 255, 255), width=1)

def building(d, x, y, w, h, c):
    d.rectangle([x, y, x + w, y + h], fill=c)
    for wy in range(y + 6, y + h - 6, 12):
        for wx in range(x + 5, x + w - 5, 11):
            d.rectangle([wx, wy, wx + 4, wy + 5], fill=(255, 220, 120))

def smoke(d, x, y, h, c=(120, 120, 125)):
    r = 7
    yy = y
    while yy > y - h:
        d.ellipse([x - r, yy - r, x + r, yy + r], fill=c)
        x += 3
        yy -= 12
        r += 2

def ship(d, x, y, w, c=(52, 56, 70)):
    d.polygon([(x, y), (x + w, y), (x + w - 8, y + 12), (x + 8, y + 12)], fill=c)
    d.rectangle([x + w * 0.3, y - 12, x + w * 0.55, y], fill=c)
    d.rectangle([x + w * 0.4, y - 20, x + w * 0.45, y - 12], fill=c)

def hero_yemen(d, x, y, w, h):
    sky(d, x, y, w, h, (32, 22, 52), (150, 70, 40))
    sun(d, x + w - 90, y + 52, 26, (255, 180, 90))
    # explosion glow over the port
    for r, c in ((46, (255, 120, 40)), (30, (255, 170, 60)), (16, (255, 220, 120))):
        d.ellipse([x + 150 - r, y + 118 - r, x + 150 + r, y + 118 + r], fill=c)
    smoke(d, x + 150, y + 118, 90)
    smoke(d, x + 320, y + 150, 70)
    # port skyline
    sea(d, x, y + h - 70, w, 70, (28, 48, 78))
    building(d, x + 20, y + h - 150, 60, 80, (40, 40, 55))
    building(d, x + 95, y + h - 130, 45, 60, (48, 44, 60))
    building(d, x + 420, y + h - 140, 70, 70, (40, 40, 55))
    building(d, x + 505, y + h - 120, 50, 50, (48, 44, 60))
    # cranes
    d.line([x + 600, y + h - 70, x + 600, y + h - 170], fill=(70, 70, 80), width=5)
    d.line([x + 600, y + h - 170, x + 660, y + h - 150], fill=(70, 70, 80), width=4)
    d.line([x + 720, y + h - 70, x + 720, y + h - 160], fill=(70, 70, 80), width=5)
    d.line([x + 720, y + h - 160, x + 770, y + h - 142], fill=(70, 70, 80), width=4)
    ship(d, x + 250, y + h - 52, 110)
    ship(d, x + 620, y + h - 46, 80)
    # missile trails in the dusk sky
    d.line([x + 700, y + 40, x + 760, y + 90], fill=(255, 220, 150), width=3)
    d.line([x + 800, y + 30, x + 840, y + 70], fill=(255, 220, 150), width=3)

# --- mini scenes: each draws inside (x, y, w, h), h ~ 48 ---

def sc_rocket(d, x, y, w, h):
    sky(d, x, y, w, h, (20, 30, 70), (90, 130, 200))
    d.polygon([(x + w // 2 - 8, y + h - 8), (x + w // 2 + 8, y + h - 8),
               (x + w // 2 + 5, y + 12), (x + w // 2, y + 4), (x + w // 2 - 5, y + 12)], fill=(240, 240, 240))
    d.polygon([(x + w // 2 - 8, y + h - 8), (x + w // 2 - 16, y + h - 2), (x + w // 2 - 8, y + h - 16)], fill=(200, 60, 60))
    d.polygon([(x + w // 2 + 8, y + h - 8), (x + w // 2 + 16, y + h - 2), (x + w // 2 + 8, y + h - 16)], fill=(200, 60, 60))
    d.polygon([(x + w // 2 - 4, y + h - 8), (x + w // 2 + 4, y + h - 8),
               (x + w // 2 + 2, y + h - 1), (x + w // 2 - 2, y + h - 1)], fill=(255, 180, 60))
    for sx, sy in ((x + 18, y + 10), (x + w - 24, y + 16), (x + 30, y + 26)):
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 255, 255))

def sc_flag(d, x, y, w, h):
    sky(d, x, y, w, h, (140, 180, 220), (210, 225, 235))
    d.line([x + 24, y + 6, x + 24, y + h - 4], fill=(60, 60, 60), width=3)
    d.polygon([(x + 24, y + 6), (x + w - 30, y + 12), (x + 24, y + 20)], fill=(200, 40, 40))
    d.rectangle([x + w - 70, y + h - 16, x + w - 8, y + h - 4], fill=(90, 90, 95))
    d.rectangle([x + w - 62, y + h - 26, x + w - 16, y + h - 16], fill=(120, 120, 125))

def sc_handshake(d, x, y, w, h):
    sky(d, x, y, w, h, (120, 170, 210), (190, 215, 235))
    d.rectangle([x, y + h - 14, x + w, y + h], fill=(90, 140, 90))
    d.ellipse([x + w // 2 - 26, y + 12, x + w // 2 - 10, y + 28], fill=(240, 200, 160))
    d.ellipse([x + w // 2 + 10, y + 12, x + w // 2 + 26, y + 28], fill=(220, 180, 140))
    d.rectangle([x + w // 2 - 30, y + 28, x + w // 2 - 8, y + h - 14], fill=(30, 60, 120))
    d.rectangle([x + w // 2 + 8, y + 28, x + w // 2 + 30, y + h - 14], fill=(60, 60, 60))
    d.ellipse([x + w // 2 - 6, y + 30, x + w // 2 + 6, y + 42], fill=(240, 200, 160))

def sc_blast(d, x, y, w, h):
    sky(d, x, y, w, h, (60, 40, 30), (140, 80, 40))
    for r, c in ((20, (255, 120, 40)), (13, (255, 170, 60)), (7, (255, 220, 120))):
        d.ellipse([x + w // 2 - r, y + 22 - r, x + w // 2 + r, y + 22 + r], fill=c)
    smoke(d, x + w // 2, y + 22, 26)
    d.rectangle([x, y + h - 12, x + w, y + h], fill=(50, 45, 40))
    building(d, x + 12, y + h - 30, 30, 18, (60, 55, 50))
    building(d, x + w - 48, y + h - 26, 34, 14, (60, 55, 50))

def sc_refinery(d, x, y, w, h):
    sky(d, x, y, w, h, (200, 120, 60), (240, 180, 100))
    d.rectangle([x, y + h - 14, x + w, y + h], fill=(70, 60, 50))
    for tx in (x + 14, x + 46, x + 78):
        d.rectangle([tx, y + h - 34, tx + 24, y + h - 14], fill=(150, 150, 155))
        d.ellipse([tx + 2, y + h - 38, tx + 22, y + h - 30], fill=(170, 170, 175))
    d.line([x + 112, y + h - 14, x + 112, y + 8], fill=(90, 90, 95), width=4)
    d.ellipse([x + 106, y + 4, x + 118, y + 12], fill=(255, 140, 50))
    smoke(d, x + 112, y + 8, 14, (90, 90, 95))

def sc_chart_down(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(245, 245, 240))
    for gy in range(y + 10, y + h - 6, 12):
        d.line([x + 6, gy, x + w - 6, gy], fill=(220, 220, 215), width=1)
    pts = [(x + 10, y + 10), (x + 40, y + 18), (x + 70, y + 14), (x + 100, y + 30), (x + w - 12, y + h - 12)]
    d.line(pts, fill=(178, 34, 34), width=3)
    d.ellipse([pts[-1][0] - 3, pts[-1][1] - 3, pts[-1][0] + 3, pts[-1][1] + 3], fill=(178, 34, 34))

def sc_capitol(d, x, y, w, h):
    sky(d, x, y, w, h, (140, 180, 220), (210, 225, 235))
    d.rectangle([x, y + h - 14, x + w, y + h], fill=(120, 160, 110))
    d.rectangle([x + w // 2 - 34, y + 20, x + w // 2 + 34, y + h - 14], fill=(240, 240, 235))
    d.ellipse([x + w // 2 - 16, y + 6, x + w // 2 + 16, y + 24], fill=(240, 240, 235))
    for cx in range(x + w // 2 - 28, x + w // 2 + 28, 12):
        d.rectangle([cx, y + 26, cx + 5, y + h - 14], fill=(200, 200, 195))

def sc_factory(d, x, y, w, h):
    sky(d, x, y, w, h, (180, 200, 220), (225, 230, 235))
    d.rectangle([x, y + h - 22, x + w, y + h], fill=(110, 110, 115))
    d.rectangle([x + 14, y + h - 34, x + w - 14, y + h - 22], fill=(170, 60, 60))
    d.rectangle([x + 24, y + h - 44, x + 30, y + h - 34], fill=(140, 140, 145))
    d.rectangle([x + 40, y + h - 48, x + 46, y + h - 34], fill=(140, 140, 145))
    smoke(d, x + 27, y + h - 44, 12, (150, 150, 155))
    for wx in range(x + 60, x + w - 20, 16):
        d.rectangle([wx, y + h - 31, wx + 9, y + h - 25], fill=(255, 230, 150))

def sc_mine(d, x, y, w, h):
    sky(d, x, y, w, h, (150, 130, 100), (210, 190, 150))
    d.polygon([(x, y + h), (x + w // 2, y + 6), (x + w, y + h)], fill=(120, 95, 70))
    d.polygon([(x + w // 2 - 16, y + h), (x + w // 2, y + 22), (x + w // 2 + 16, y + h)], fill=(40, 30, 22))
    d.rectangle([x + 12, y + h - 10, x + 40, y + h - 4], fill=(90, 70, 50))
    d.line([x + 100, y + h - 6, x + 130, y + h - 6], fill=(200, 200, 200), width=2)

def sc_explosion(d, x, y, w, h):
    sky(d, x, y, w, h, (200, 190, 170), (240, 230, 210))
    for r, c in ((22, (255, 140, 50)), (14, (255, 190, 80)), (7, (255, 230, 140))):
        d.ellipse([x + w // 2 - r, y + 20 - r, x + w // 2 + r, y + 20 + r], fill=c)
    smoke(d, x + w // 2 - 20, y + 20, 24)
    smoke(d, x + w // 2 + 22, y + 22, 20)
    d.rectangle([x, y + h - 10, x + w, y + h], fill=(130, 120, 100))
    d.rectangle([x + 16, y + h - 22, x + 44, y + h - 10], fill=(150, 140, 125))
    d.rectangle([x + w - 50, y + h - 20, x + w - 22, y + h - 10], fill=(150, 140, 125))

def sc_tide(d, x, y, w, h):
    sky(d, x, y, w, h, (120, 150, 190), (190, 210, 230))
    sea(d, x, y + 18, w, h - 18, (30, 90, 140))
    d.rectangle([x, y + h - 16, x + w, y + h - 10], fill=(90, 80, 70))
    d.rectangle([x + 20, y + h - 30, x + 50, y + h - 16], fill=(120, 110, 100))
    d.rectangle([x + 60, y + h - 26, x + 90, y + h - 16], fill=(120, 110, 100))
    d.line([x + 10, y + 26, x + w - 10, y + 26], fill=(255, 255, 255), width=2)
    d.line([x + 20, y + 34, x + w - 20, y + 34], fill=(200, 220, 240), width=2)

def sc_flags(d, x, y, w, h):
    sky(d, x, y, w, h, (30, 40, 80), (80, 90, 140))
    d.rectangle([x, y + h - 8, x + w, y + h], fill=(50, 50, 55))
    for i, c in enumerate(((150, 40, 140), (220, 120, 40), (40, 120, 200), (200, 200, 60), (60, 180, 80))):
        fx = x + 14 + i * 26
        d.line([fx, y + 8, fx, y + h - 8], fill=(200, 200, 200), width=2)
        d.polygon([(fx, y + 8), (fx + 20, y + 13), (fx, y + 18)], fill=c)

def sc_dinner(d, x, y, w, h):
    sky(d, x, y, w, h, (90, 60, 40), (180, 130, 80))
    d.rectangle([x, y + h - 14, x + w, y + h], fill=(60, 40, 30))
    d.rectangle([x + 30, y + h - 26, x + w - 30, y + h - 14], fill=(240, 230, 210))
    d.ellipse([x + w // 2 - 26, y + 10, x + w // 2 - 10, y + 26], fill=(240, 200, 160))
    d.ellipse([x + w // 2 + 10, y + 10, x + w // 2 + 26, y + 26], fill=(220, 180, 140))
    d.rectangle([x + w // 2 - 30, y + 26, x + w // 2 - 8, y + h - 14], fill=(30, 60, 120))
    d.rectangle([x + w // 2 + 8, y + 26, x + w // 2 + 30, y + h - 14], fill=(60, 60, 60))
    d.rectangle([x + w // 2 - 4, y + h - 34, x + w // 2 + 4, y + h - 26], fill=(255, 220, 120))

def sc_boxes(d, x, y, w, h):
    sky(d, x, y, w, h, (160, 170, 190), (220, 225, 230))
    d.rectangle([x, y + h - 10, x + w, y + h], fill=(100, 100, 105))
    d.rectangle([x + 16, y + h - 30, x + 52, y + h - 10], fill=(180, 140, 80))
    d.rectangle([x + 58, y + h - 38, x + 94, y + h - 10], fill=(160, 120, 70))
    d.rectangle([x + 100, y + h - 26, x + 132, y + h - 10], fill=(180, 140, 80))
    d.line([x + 16, y + h - 30, x + 52, y + h - 30], fill=(120, 90, 50), width=2)
    d.line([x + 58, y + h - 38, x + 94, y + h - 38], fill=(120, 90, 50), width=2)
    d.rectangle([x + 116, y + 6, x + 146, y + 22], fill=(178, 34, 34))
    d.text((x + 120, y + 8), "%", font=F_SANS_B(12), fill=(255, 255, 255))

def sc_whipsaw(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(245, 245, 240))
    for gy in range(y + 10, y + h - 6, 12):
        d.line([x + 6, gy, x + w - 6, gy], fill=(220, 220, 215), width=1)
    pts = [(x + 10, y + 26), (x + 34, y + 12), (x + 58, y + 34), (x + 82, y + 8), (x + 106, y + 30), (x + w - 12, y + 18)]
    d.line(pts, fill=(30, 90, 160), width=3)
    d.ellipse([pts[-1][0] - 3, pts[-1][1] - 3, pts[-1][0] + 3, pts[-1][1] + 3], fill=(30, 90, 160))

def sc_storm(d, x, y, w, h):
    sky(d, x, y, w, h, (70, 80, 100), (130, 140, 160))
    d.ellipse([x + 20, y + 6, x + 70, y + 20], fill=(200, 200, 205))
    d.ellipse([x + 60, y + 10, x + 120, y + 24], fill=(180, 180, 185))
    for rx in range(x + 10, x + w - 10, 18):
        d.line([rx, y + 28, rx - 4, y + 40], fill=(120, 150, 200), width=2)
    sea(d, x, y + h - 12, w, 12, (30, 70, 110))
    d.rectangle([x + 24, y + h - 26, x + 56, y + h - 12], fill=(120, 110, 100))
    d.rectangle([x + 96, y + h - 24, x + 128, y + h - 12], fill=(120, 110, 100))

def sc_village(d, x, y, w, h):
    sky(d, x, y, w, h, (190, 150, 100), (230, 200, 150))
    d.rectangle([x, y + h - 12, x + w, y + h], fill=(140, 110, 70))
    d.rectangle([x + 14, y + h - 26, x + 44, y + h - 12], fill=(170, 130, 90))
    d.polygon([(x + 12, y + h - 26), (x + 29, y + h - 38), (x + 46, y + h - 26)], fill=(120, 80, 50))
    d.rectangle([x + 60, y + h - 24, x + 92, y + h - 12], fill=(170, 130, 90))
    d.polygon([(x + 58, y + h - 24), (x + 76, y + h - 36), (x + 94, y + h - 24)], fill=(120, 80, 50))
    d.line([x + 108, y + h - 12, x + 108, y + 8], fill=(80, 60, 40), width=3)
    d.ellipse([x + 102, y + 6, x + 114, y + 14], fill=(255, 140, 50))

def sc_tanker(d, x, y, w, h):
    sky(d, x, y, w, h, (60, 40, 30), (150, 90, 50))
    d.rectangle([x, y + h - 12, x + w, y + h], fill=(60, 55, 50))
    d.rectangle([x + 20, y + h - 26, x + 110, y + h - 12], fill=(180, 180, 185))
    d.ellipse([x + 30, y + h - 10, x + 42, y + h - 2], fill=(30, 30, 30))
    d.ellipse([x + 88, y + h - 10, x + 100, y + h - 2], fill=(30, 30, 30))
    for r, c in ((16, (255, 120, 40)), (10, (255, 170, 60)), (5, (255, 220, 120))):
        d.ellipse([x + 65 - r, y + 16 - r, x + 65 + r, y + 16 + r], fill=c)
    smoke(d, x + 65, y + 16, 16)

def sc_desert(d, x, y, w, h):
    sky(d, x, y, w, h, (200, 180, 140), (235, 215, 175))
    d.rectangle([x, y + h - 14, x + w, y + h], fill=(190, 160, 110))
    d.rectangle([x + 20, y + h - 30, x + 60, y + h - 14], fill=(150, 130, 100))
    d.rectangle([x + 80, y + h - 26, x + 120, y + h - 14], fill=(150, 130, 100))
    d.line([x + 40, y + 10, x + 40, y + h - 30], fill=(90, 70, 50), width=3)
    d.polygon([(x + 40, y + 10), (x + 66, y + 15), (x + 40, y + 20)], fill=(60, 60, 60))
    sun(d, x + w - 26, y + 12, 9, (255, 200, 100))

def sc_rubble(d, x, y, w, h):
    sky(d, x, y, w, h, (120, 110, 100), (190, 180, 165))
    d.polygon([(x, y + h), (x + 50, y + 14), (x + 100, y + h)], fill=(140, 130, 120))
    d.polygon([(x + 60, y + h), (x + 110, y + 22), (x + w, y + h)], fill=(120, 110, 100))
    d.rectangle([x + 20, y + h - 12, x + 48, y + h - 4], fill=(100, 95, 85))
    d.rectangle([x + 90, y + h - 10, x + 116, y + h - 4], fill=(100, 95, 85))
    smoke(d, x + 50, y + 14, 14, (140, 135, 130))

def sc_court(d, x, y, w, h):
    sky(d, x, y, w, h, (140, 160, 190), (205, 215, 225))
    d.rectangle([x, y + h - 12, x + w, y + h], fill=(130, 150, 120))
    d.rectangle([x + 24, y + 22, x + w - 24, y + h - 12], fill=(235, 232, 225))
    d.polygon([(x + 18, y + 22), (x + w // 2, y + 6), (x + w - 18, y + 22)], fill=(200, 195, 185))
    for cx in range(x + 32, x + w - 32, 16):
        d.rectangle([cx, y + 26, cx + 6, y + h - 12], fill=(210, 205, 195))
    d.ellipse([x + w // 2 - 8, y + 12, x + w // 2 + 8, y + 22], fill=(212, 175, 55))

def sc_market(d, x, y, w, h):
    sky(d, x, y, w, h, (150, 180, 210), (210, 225, 235))
    d.rectangle([x, y + h - 10, x + w, y + h], fill=(110, 110, 115))
    d.rectangle([x + 16, y + 18, x + w - 16, y + h - 10], fill=(240, 240, 235))
    d.polygon([(x + 10, y + 18), (x + w // 2, y + 4), (x + w - 10, y + 18)], fill=(30, 120, 60))
    for wx in range(x + 28, x + w - 28, 18):
        d.rectangle([wx, y + 26, wx + 10, y + h - 16], fill=(150, 200, 230))

def sc_power(d, x, y, w, h):
    sky(d, x, y, w, h, (40, 50, 80), (90, 110, 150))
    d.rectangle([x, y + h - 10, x + w, y + h], fill=(50, 50, 55))
    d.line([x + 30, y + h - 10, x + 30, y + 6], fill=(30, 30, 35), width=4)
    d.line([x + 18, y + 14, x + 42, y + 14], fill=(30, 30, 35), width=3)
    d.line([x + 22, y + 22, x + 38, y + 22], fill=(30, 30, 35), width=3)
    d.line([x + 100, y + h - 10, x + 100, y + 12], fill=(30, 30, 35), width=4)
    d.line([x + 88, y + 20, x + 112, y + 20], fill=(30, 30, 35), width=3)
    d.line([x + 30, y + 14, x + 100, y + 20], fill=(200, 200, 205), width=1)
    for r, c in ((10, (255, 200, 80)), (6, (255, 230, 140))):
        d.ellipse([x + 65 - r, y + 30 - r, x + 65 + r, y + 30 + r], fill=c)

def sc_shop(d, x, y, w, h):
    sky(d, x, y, w, h, (160, 160, 165), (210, 210, 215))
    d.rectangle([x, y + h - 10, x + w, y + h], fill=(110, 110, 115))
    d.rectangle([x + 18, y + 16, x + w - 18, y + h - 10], fill=(200, 60, 60))
    d.rectangle([x + 26, y + 24, x + w - 26, y + h - 18], fill=(255, 255, 255))
    d.line([x + 26, y + h - 18, x + w - 26, y + h - 18], fill=(200, 60, 60), width=3)
    d.text((x + 44, y + 26), "CLOSED", font=F_SANS_B(13), fill=(178, 34, 34))

def sc_bill(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(245, 242, 235))
    d.rectangle([x + 34, y + 6, x + w - 34, y + h - 6], fill=(255, 255, 255))
    d.line([x + 44, y + 14, x + w - 44, y + 14], fill=(180, 180, 175), width=2)
    d.line([x + 44, y + 22, x + w - 60, y + 22], fill=(200, 200, 195), width=1)
    d.line([x + 44, y + 28, x + w - 50, y + 28], fill=(200, 200, 195), width=1)
    d.text((x + 44, y + 32), "+26%", font=F_SANS_B(13), fill=(178, 34, 34))

def sc_pitch(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(40, 140, 70))
    d.line([x + w // 2, y, x + w // 2, y + h], fill=(255, 255, 255), width=2)
    d.ellipse([x + w // 2 - 16, y + h // 2 - 16, x + w // 2 + 16, y + h // 2 + 16], outline=(255, 255, 255), width=2)
    d.ellipse([x + 26, y + 12, x + 36, y + 22], fill=(255, 255, 255))
    d.ellipse([x + w - 40, y + h - 24, x + w - 30, y + h - 14], fill=(255, 255, 255))
    d.rectangle([x + 4, y + h // 2 - 14, x + 12, y + h // 2 + 14], outline=(255, 255, 255), width=2)
    d.rectangle([x + w - 12, y + h // 2 - 14, x + w - 4, y + h // 2 + 14], outline=(255, 255, 255), width=2)

def sc_asteroid(d, x, y, w, h):
    sky(d, x, y, w, h, (10, 12, 30), (30, 35, 60))
    for sx, sy in ((x + 16, y + 10), (x + 40, y + 22), (x + w - 30, y + 8), (x + w - 18, y + 30), (x + 70, y + 6)):
        d.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(255, 255, 255))
    d.ellipse([x + w // 2 - 30, y + 8, x + w // 2 + 30, y + h - 8], fill=(150, 140, 130))
    d.ellipse([x + w // 2 - 12, y + 16, x + w // 2 + 6, y + 30], fill=(90, 85, 80))
    d.ellipse([x + w // 2 + 8, y + 30, x + w // 2 + 18, y + 38], fill=(100, 95, 88))
    for bx, by in ((x + 14, y + 34), (x + w - 22, y + 36), (x + 30, y + 40)):
        d.ellipse([bx - 3, by - 3, bx + 3, by + 3], fill=(170, 160, 150))

def sc_guitar(d, x, y, w, h):
    sky(d, x, y, w, h, (60, 40, 70), (130, 90, 120))
    d.ellipse([x + w // 2 - 22, y + 14, x + w // 2 + 6, y + 42], fill=(150, 90, 40))
    d.ellipse([x + w // 2 - 10, y + 24, x + w // 2 + 2, y + 34], fill=(30, 20, 20))
    d.rectangle([x + w // 2 - 4, y + 2, x + w // 2 + 2, y + 16], fill=(120, 70, 30))
    d.rectangle([x + w // 2 - 12, y + 38, x + w // 2 + 12, y + h - 6], fill=(90, 60, 40))
    d.line([x + w // 2 - 2, y + 6, x + w // 2 - 2, y + h - 8], fill=(220, 220, 220), width=1)

TILES = [
    ("SPACE", "Shenzhou-24 crew lifts off", sc_rocket),
    ("ASIA", "N. Korea expels Swiss envoy", sc_flag),
    ("PACIFIC", "Solomons sign Australia treaty", sc_handshake),
    ("UKRAINE", "Russian strike kills 2 in Odesa", sc_blast),
    ("ENERGY", "Drones hit refineries, reportedly", sc_refinery),
    ("MARKETS", "Asian shares slide on tariff fears", sc_chart_down),
    ("TECH", "Senate passes Digital Duty of Care", sc_capitol),
    ("ASIA", "Bangladesh garment wage up 36%", sc_factory),
    ("INDONESIA", "Dozens feared trapped in mine", sc_mine),
    ("USA", "Army blasts 5 tons of explosives in Iowa", sc_explosion),
    ("USA", "Record tides flood Bay Area", sc_tide),
    ("WORLD", "UN: 129 flags for women killed daily", sc_flags),
    ("USA", "Trump, Rutte dine at Mar-a-Lago", sc_dinner),
    ("TRADE", "US proposes tariffs on 14 partners", sc_boxes),
    ("MARKETS", "Wall Street whipsaws on hot inflation", sc_whipsaw),
    ("WEATHER", "Nor'easter floods US East Coast", sc_storm),
    ("AFRICA", "Militants kill 30 in Nigeria", sc_village),
    ("AFRICA", "Fuel tanker fire kills 31 in Egypt", sc_tanker),
    ("MIDDLE EAST", "IS kills 2 Syrian security men", sc_desert),
    ("MIDDLE EAST", "Hamas security chief killed in Gaza", sc_rubble),
    ("MIDDLE EAST", "Judges urge Netanyahu case drop", sc_court),
    ("LATIN AMERICA", "All hostages freed in Cartagena", sc_market),
    ("UKRAINE", "Russia hits Ukraine power grid", sc_power),
    ("BUSINESS", "Poundland collapses, 11,000 jobs at risk", sc_shop),
    ("EUROPE", "UK energy bills to rise 26% in January", sc_bill),
    ("SPORT", "Roma end PSG's perfect run", sc_pitch),
    ("SCIENCE", "Asteroid crater revealed by Hera", sc_asteroid),
    ("CULTURE", "Andy Taylor death announced", sc_guitar),
    ("SPORT", "Liverpool cruise 3-0 at Brugge", sc_pitch),
]

def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # masthead
    d.rectangle([0, 0, W, 78], fill=NAVY)
    d.rectangle([0, 78, W, 81], fill=GOLD)
    t = "WEDNESDAY 25 NOVEMBER 2026"
    f = F_SERIF_B(30)
    d.text(((W - d.textlength(t, font=f)) / 2, 12), t, font=f, fill=(255, 255, 255))
    s = "30 stories, each verified to 25 November 2026"
    fs = F_SANS(13)
    d.text(((W - d.textlength(s, font=fs)) / 2, 50), s, font=fs, fill=GOLD)
    # hero (full width, 78-368) with headline band
    hero_yemen(d, 0, 81, W, 287)
    d.rectangle([0, 296, W, 368], fill=(10, 10, 20))
    ht = "Yemen war flares at the Red Sea ports"
    hf = F_SERIF_B(28)
    d.text((16, 304), ht, font=hf, fill=(255, 255, 255))
    hs = "Houthis near Aden; coalition hits Hodeidah; Jeddah threatened"
    hsf = F_SANS(14)
    d.text((16, 338), hs, font=hsf, fill=(220, 220, 220))
    d.text((W - 130, 304), "TOP STORY", font=F_SANS_B(13), fill=GOLD)
    # label bar
    lab = "MORE TODAY — 29 STORIES"
    lf = F_SANS_B(13)
    d.text(((W - d.textlength(lab, font=lf)) / 2, 372), lab, font=lf, fill=NAVY)
    d.line([14, 380, 380, 380], fill=GOLD, width=2)
    d.line([644, 380, 1010, 380], fill=GOLD, width=2)
    # grid
    tw, th, gap, mx, gy0 = 159, 113, 8, 14, 392
    for i, (tag, head, scene) in enumerate(TILES):
        row, col = divmod(i, 6)
        x = mx + col * (tw + gap)
        y = gy0 + row * (th + gap)
        d.rectangle([x, y, x + tw, y + th], fill=CARD, outline=(200, 200, 200), width=1)
        scene(d, x + 1, y + 1, tw - 2, 48)
        d.text((x + 7, y + 53), tag, font=F_SANS_B(9), fill=NAVY)
        lines = wrap(d, head, F_SERIF_B(12), tw - 14)
        yy = y + 66
        for ln in lines[:2]:
            d.text((x + 7, yy), ln, font=F_SERIF_B(12), fill=INK)
            yy += 14
    # summary tile in the 30th slot
    x = mx + 5 * (tw + gap)
    y = gy0 + 4 * (th + gap)
    d.rectangle([x, y, x + tw, y + th], fill=NAVY)
    d.text((x + 14, y + 14), "30 STORIES", font=F_SERIF_B(16), fill=(255, 255, 255))
    d.text((x + 14, y + 40), "9 REGIONS", font=F_SANS_B(12), fill=GOLD)
    d.text((x + 14, y + 62), "VERIFIED TO", font=F_SANS(10), fill=(220, 220, 220))
    d.text((x + 14, y + 76), "25 NOV 2026", font=F_SANS_B(11), fill=(255, 255, 255))
    # footer
    d.rectangle([0, 992, W, H], fill=NAVY)
    ft = "25 NOVEMBER 2026  •  SOURCES: REUTERS, AP, AFP, BBC, UEFA, ESA, NATO"
    ff = F_SANS(11)
    d.text(((W - d.textlength(ft, font=ff)) / 2, 1004), ft, font=ff, fill=(255, 255, 255))
    img.save("entry.png", optimize=True)
    print("saved entry.png")

if __name__ == "__main__":
    main()

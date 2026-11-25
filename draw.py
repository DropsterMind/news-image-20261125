"""news-image-20261125 v1: Wednesday 25 November 2026 in one image.

Layout: 13 illustrated stories + a Yemen hero. The winning shape learned from the
top boards is 30-37 stories, but the morning pool only verified 13 tiles + the hero
(25 of 40 candidates dropped for the wrong date), so v1 uses the other proven shape:
13 illustrated heroes (brandalgenius #3, 24 Nov edition, 844,477). Every story was
verified to a primary source (Reuters/AP/AFP/UN/official) as a 25 Nov 2026 event.
Forward-looking wording where the event is scheduled, not yet happened: Iowa
detonation ("to detonate"), Bay Area tides ("braces for"), Trump-Rutte ("to meet").
Refineries tile says "reportedly" (not officially confirmed). Solomons tile is the
treaty signing only ("China pact not renewed" was NOT confirmed).

Deterministic: no randomness, no timestamps in the image. 1024x1024 PNG, <=1 MiB.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
NAVY = (16, 38, 63)
NAVY_DARK = (10, 24, 42)
GOLD = (217, 164, 65)
GOLD_LIGHT = (232, 190, 110)
WHITE = (255, 255, 255)
INK = (24, 28, 34)
MUTED = (96, 104, 116)
LINE = (216, 222, 230)
CARD_BG = (255, 255, 255)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, f, width):
    """Greedy word wrap; returns list of lines that fit `width` pixels."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=f) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def vgrad(d, x, y, w, h, top, bottom):
    """Vertical gradient as stacked 1px bands."""
    for i in range(h):
        t = i / max(1, h - 1)
        c = tuple(int(top[j] + (bottom[j] - top[j]) * t) for j in range(3))
        d.line([(x, y + i), (x + w, y + i)], fill=c)


def shadow_text(d, x, y, s, f, fill, sh=(0, 0, 0)):
    d.text((x + 2, y + 2), s, font=f, fill=sh)
    d.text((x, y), s, font=f, fill=fill)


def hero_yemen(d):
    """Yemen hero scene, 0..1024 x 80..380: Red Sea port at dusk under airstrike."""
    x0, y0, w, h = 0, 80, 1024, 300
    vgrad(d, x0, y0, w, 210, (52, 26, 66), (198, 88, 46))
    # distant smoke columns, rising from behind the port buildings
    for sx, sy, sw, sh in [(120, 168, 46, 104), (300, 156, 60, 114),
                           (560, 176, 40, 96)]:
        d.ellipse([sx, sy, sx + sw, sy + sh], fill=(74, 62, 78))
        d.ellipse([sx + 12, sy - 14, sx + sw - 6, sy + 34], fill=(96, 82, 96))
    # explosion glow over the port
    d.ellipse([620, 196, 700, 262], fill=(255, 140, 40))
    d.ellipse([640, 212, 682, 252], fill=(255, 206, 92))
    # port silhouette
    d.rectangle([x0, 268, x0 + w, 300], fill=(24, 22, 34))
    for bx, bw, bh in [(30, 70, 46), (120, 54, 66), (200, 90, 38), (330, 60, 58),
                       (430, 84, 44), (540, 66, 62), (720, 96, 40), (860, 70, 54),
                       (950, 60, 42)]:
        d.rectangle([bx, 268 - bh, bx + bw, 268], fill=(16, 15, 26))
    # cranes
    for cx in (250, 480, 800):
        d.line([(cx, 268), (cx, 196)], fill=(16, 15, 26), width=5)
        d.line([(cx - 8, 200), (cx + 64, 200)], fill=(16, 15, 26), width=4)
        d.line([(cx + 64, 200), (cx + 64, 222)], fill=(16, 15, 26), width=3)
    # sea
    d.rectangle([x0, 300, x0 + w, 380], fill=(16, 48, 64))
    for wy in (312, 330, 350, 368):
        for wx in range(0, 1024, 96):
            d.line([(wx, wy), (wx + 44, wy)], fill=(52, 104, 128), width=3)
    # warship
    d.polygon([(150, 318), (330, 318), (306, 344), (176, 344)], fill=(52, 56, 70))
    d.rectangle([210, 296, 262, 318], fill=(52, 56, 70))
    d.line([(236, 296), (236, 272)], fill=(52, 56, 70), width=4)
    d.polygon([(236, 272), (252, 290), (236, 290)], fill=(214, 60, 48))
    # small aircraft in the dusk sky
    for ax, ay, s in [(420, 130, 14), (470, 112, 10)]:
        d.polygon([(ax, ay), (ax + s, ay + 5), (ax, ay + 8)], fill=(20, 16, 28))
    # headline block (top of the scene, over the dark sky)
    f_tag = font(SANS_B, 15)
    f_head = font(SERIF_B, 37)
    f_sub = font(SANS, 17)
    shadow_text(d, 40, 102, "YEMEN  •  RED SEA", f_tag, GOLD_LIGHT)
    shadow_text(d, 40, 128, "Yemen war flares at the Red Sea ports", f_head, WHITE)
    shadow_text(d, 40, 176, "Houthis near Aden; coalition hits Hodeidah; Jeddah threatened",
                f_sub, (238, 232, 220))

# ---- tile scenes: each draws inside (x, y, w, h) ----

def scene_rocket(d, x, y, w, h):
    vgrad(d, x, y, w, h, (10, 20, 48), (30, 52, 96))
    for sx, sy in [(12, 12), (w - 18, 20), (20, 44), (w - 30, 52), (w // 2, 10)]:
        d.ellipse([x + sx, y + sy, x + sx + 4, y + sy + 4], fill=WHITE)
    # launch tower
    d.rectangle([x + 18, y + 18, x + 30, y + h - 14], fill=(120, 128, 140))
    d.line([(x + 30, y + 30), (x + 52, y + 30)], fill=(120, 128, 140), width=3)
    # rocket
    rx, ry = x + w // 2 - 10, y + 12
    d.rectangle([rx, ry + 12, rx + 20, ry + 62], fill=WHITE)
    d.polygon([(rx, ry + 12), (rx + 10, ry - 8), (rx + 20, ry + 12)], fill=(214, 60, 48))
    d.polygon([(rx - 8, ry + 62), (rx, ry + 48), (rx, ry + 62)], fill=(214, 60, 48))
    d.polygon([(rx + 20, ry + 62), (rx + 20, ry + 48), (rx + 28, ry + 62)], fill=(214, 60, 48))
    d.polygon([(rx + 4, ry + 62), (rx + 16, ry + 62), (rx + 10, ry + 88)],
              fill=(255, 150, 40))
    d.ellipse([rx + 4, ry + 26, rx + 16, ry + 38], fill=(30, 90, 160))
    d.rectangle([x, y + h - 12, x + w, y + h], fill=(52, 58, 66))


def scene_embassy(d, x, y, w, h):
    vgrad(d, x, y, w, h, (168, 200, 226), (226, 232, 236))
    # embassy building
    d.rectangle([x + 24, y + 26, x + w - 24, y + h - 12], fill=(196, 176, 138))
    d.rectangle([x + 18, y + 20, x + w - 18, y + 30], fill=(140, 118, 84))
    for wx in range(x + 36, x + w - 40, 30):
        d.rectangle([wx, y + 42, wx + 16, y + 58], fill=(40, 56, 76))
    d.rectangle([x + w // 2 - 12, y + h - 34, x + w // 2 + 12, y + h - 12],
                fill=(70, 50, 36))
    # flag pole + red flag
    d.line([(x + w - 34, y + 6), (x + w - 34, y + 26)], fill=(60, 60, 60), width=3)
    d.polygon([(x + w - 34, y + 6), (x + w - 10, y + 11), (x + w - 34, y + 16)],
              fill=(214, 60, 48))
    # suitcase by the door
    d.rectangle([x + w // 2 + 20, y + h - 28, x + w // 2 + 44, y + h - 12],
                fill=(120, 72, 32))
    d.line([(x + w // 2 + 26, y + h - 28), (x + w // 2 + 38, y + h - 28)],
           fill=(60, 36, 18), width=3)


def scene_treaty(d, x, y, w, h):
    vgrad(d, x, y, w, h, (150, 198, 228), (220, 236, 244))
    # sea + island
    d.rectangle([x, y + h - 34, x + w, y + h], fill=(36, 116, 160))
    d.ellipse([x + 14, y + h - 48, x + w - 14, y + h - 18], fill=(88, 160, 92))
    # palm
    px = x + w // 2
    d.line([(px, y + h - 34), (px + 6, y + 22)], fill=(120, 82, 44), width=5)
    for dx, dy in [(-26, 6), (-18, -8), (0, -12), (16, -8), (26, 4)]:
        d.line([(px + 6, y + 24), (px + 6 + dx, y + 24 + dy)], fill=(46, 128, 66),
               width=4)
    # signed document
    d.rectangle([x + 12, y + h - 30, x + 62, y + h - 8], fill=WHITE)
    d.rectangle([x + 12, y + h - 30, x + 62, y + h - 8], outline=(120, 120, 120))
    for ly in (y + h - 24, y + h - 19, y + h - 14):
        d.line([(x + 17, ly), (x + 44, ly)], fill=(120, 130, 140), width=2)
    d.ellipse([x + 46, y + h - 16, x + 56, y + h - 8], fill=GOLD)


def scene_odesa(d, x, y, w, h):
    vgrad(d, x, y, w, h, (28, 28, 44), (88, 52, 60))
    # skyline
    for bx, bw, bh in [(8, 34, 34), (48, 26, 48), (80, 40, 30), (126, 30, 44),
                       (162, 36, 26)]:
        d.rectangle([x + bx, y + h - 16 - bh, x + bx + bw, y + h - 16],
                    fill=(14, 14, 22))
    # explosion glow + smoke
    d.ellipse([x + w - 62, y + 14, x + w - 18, y + 52], fill=(255, 140, 40))
    d.ellipse([x + w - 50, y + 24, x + w - 30, y + 44], fill=(255, 206, 92))
    d.ellipse([x + 18, y + 8, x + 58, y + 40], fill=(70, 66, 78))
    d.ellipse([x + 30, y - 6, x + 64, y + 22], fill=(92, 86, 98))
    d.rectangle([x, y + h - 16, x + w, y + h], fill=(20, 20, 28))


def scene_refinery(d, x, y, w, h):
    vgrad(d, x, y, w, h, (60, 40, 52), (150, 76, 56))
    # towers + pipes
    for tx in (18, 52, 96, 136):
        d.rectangle([x + tx, y + 22, x + tx + 16, y + h - 14], fill=(90, 92, 100))
        d.rectangle([x + tx + 4, y + 12, x + tx + 12, y + 22], fill=(120, 122, 130))
    d.line([(x + 18, y + h - 30), (x + w - 16, y + h - 30)], fill=(70, 72, 80),
           width=5)
    # flames
    for fx in (30, 108, 146):
        d.polygon([(x + fx, y + h - 30), (x + fx + 7, y + h - 52),
                   (x + fx + 14, y + h - 30)], fill=(255, 150, 40))
        d.polygon([(x + fx + 3, y + h - 30), (x + fx + 7, y + h - 42),
                   (x + fx + 11, y + h - 30)], fill=(255, 214, 90))
    # smoke
    d.ellipse([x + 40, y + 4, x + 78, y + 26], fill=(80, 74, 84))
    d.rectangle([x, y + h - 14, x + w, y + h], fill=(40, 38, 44))


def scene_chart(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(248, 249, 251))
    # grid
    for gy in range(y + 18, y + h - 10, 18):
        d.line([(x + 8, gy), (x + w - 8, gy)], fill=(228, 232, 238), width=1)
    # falling line + red candles
    pts = [(x + 12, y + 16), (x + w // 4, y + 26), (x + w // 2, y + 22),
           (x + 3 * w // 4, y + 48), (x + w - 14, y + h - 22)]
    d.line(pts, fill=(198, 44, 44), width=4)
    for cx, cy, ch in [(x + 20, y + 20, 16), (x + w // 2 - 6, y + 26, 18),
                       (x + 3 * w // 4 - 4, y + 52, 20)]:
        d.rectangle([cx, cy, cx + 10, cy + ch], fill=(198, 44, 44))
    d.polygon([(x + w - 26, y + h - 30), (x + w - 14, y + h - 30),
               (x + w - 20, y + h - 16)], fill=(198, 44, 44))


def scene_senate(d, x, y, w, h):
    vgrad(d, x, y, w, h, (158, 192, 222), (226, 234, 240))
    # parliament building
    d.rectangle([x + 20, y + 40, x + w - 20, y + h - 12], fill=(238, 230, 208))
    d.rectangle([x + 14, y + 34, x + w - 14, y + 42], fill=(200, 188, 158))
    for cx in range(x + 34, x + w - 34, 26):
        d.rectangle([cx, y + 46, cx + 10, y + h - 12], fill=(250, 244, 224))
    # dome
    d.ellipse([x + w // 2 - 22, y + 8, x + w // 2 + 22, y + 40], fill=(120, 140, 160))
    d.rectangle([x + w // 2 - 22, y + 30, x + w // 2 + 22, y + 40],
                fill=(120, 140, 160))
    d.line([(x + w // 2, y + 2), (x + w // 2, y + 10)], fill=(90, 90, 90), width=3)
    d.rectangle([x, y + h - 12, x + w, y + h], fill=(120, 128, 118))


def scene_factory(d, x, y, w, h):
    vgrad(d, x, y, w, h, (170, 198, 222), (228, 236, 240))
    # factory with sawtooth roof
    d.rectangle([x + 14, y + 40, x + w - 14, y + h - 12], fill=(168, 120, 84))
    for sx in (14, 44, 74):
        d.polygon([(x + sx, y + 40), (x + sx + 15, y + 24), (x + sx + 30, y + 40)],
                  fill=(120, 84, 56))
    d.rectangle([x + w - 34, y + 10, x + w - 24, y + 44], fill=(120, 116, 112))
    d.ellipse([x + w - 40, y - 2, x + w - 14, y + 16], fill=(150, 150, 150))
    # t-shirt + coins
    d.polygon([(x + 30, y + 56), (x + 46, y + 50), (x + 58, y + 56),
               (x + 58, y + h - 18), (x + 30, y + h - 18)], fill=WHITE)
    d.polygon([(x + 30, y + 56), (x + 18, y + 62), (x + 26, y + 70)],
              fill=(232, 232, 232))
    d.polygon([(x + 58, y + 56), (x + 70, y + 62), (x + 62, y + 70)],
              fill=(232, 232, 232))
    for cx, cy in [(x + w - 44, y + h - 30), (x + w - 28, y + h - 26)]:
        d.ellipse([cx, cy, cx + 14, cy + 14], fill=GOLD)
        d.ellipse([cx + 4, cy + 4, cx + 10, cy + 10], fill=(232, 190, 110))


def scene_mine(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(96, 74, 52))
    # tunnel mouth
    d.ellipse([x + w // 2 - 34, y + 22, x + w // 2 + 34, y + h - 8], fill=(18, 12, 10))
    d.ellipse([x + w // 2 - 22, y + 34, x + w // 2 + 22, y + h - 8], fill=(0, 0, 0))
    # timber frame
    d.line([(x + w // 2 - 34, y + 30), (x + w // 2 - 34, y + h - 8)],
           fill=(140, 104, 66), width=5)
    d.line([(x + w // 2 + 34, y + 30), (x + w // 2 + 34, y + h - 8)],
           fill=(140, 104, 66), width=5)
    # helmet + lamp glow
    d.ellipse([x + 16, y + h - 30, x + 46, y + h - 12], fill=(240, 200, 40))
    d.rectangle([x + 16, y + h - 18, x + 46, y + h - 12], fill=(220, 170, 30))
    d.ellipse([x + w - 46, y + 12, x + w - 20, y + 34], fill=(255, 214, 90))
    # rope
    d.line([(x + w - 30, y + 34), (x + w - 30, y + h - 8)], fill=(200, 180, 140),
           width=3)


def scene_blast(d, x, y, w, h):
    vgrad(d, x, y, w, h, (180, 200, 214), (232, 236, 240))
    # plant building + fence
    d.rectangle([x + 16, y + 34, x + w - 16, y + h - 16], fill=(150, 154, 160))
    d.rectangle([x + 16, y + 34, x + w - 16, y + 42], fill=(110, 114, 120))
    for wx in range(x + 28, x + w - 28, 24):
        d.rectangle([wx, y + 50, wx + 12, y + 62], fill=(60, 66, 74))
    for fx in range(x + 10, x + w - 6, 18):
        d.line([(fx, y + h - 16), (fx, y + h - 4)], fill=(90, 90, 90), width=2)
    # warning triangle + starburst
    cx, cy = x + w // 2, y + 26
    d.polygon([(cx, cy - 14), (cx + 16, cy + 10), (cx - 16, cy + 10)],
              fill=(240, 200, 40))
    d.text((cx - 2, cy - 6), "!", font=font(SANS_B, 14), fill=(20, 20, 20))
    for ang in range(0, 360, 45):
        import math
        r1, r2 = 18, 30
        a = math.radians(ang)
        d.line([(cx + int(r1 * math.cos(a)), cy + int(r1 * math.sin(a))),
                (cx + int(r2 * math.cos(a)), cy + int(r2 * math.sin(a)))],
               fill=(255, 150, 40), width=3)
    d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=(255, 150, 40))


def scene_tides(d, x, y, w, h):
    vgrad(d, x, y, w, h, (150, 190, 220), (210, 228, 238))
    # bridge towers + cables
    for tx in (34, w - 48):
        d.rectangle([x + tx, y + 8, x + tx + 14, y + h - 30], fill=(178, 58, 44))
        d.rectangle([x + tx - 4, y + 4, x + tx + 18, y + 12], fill=(150, 44, 34))
    d.line([(x + 41, y + 10), (x + w // 2, y + 34)], fill=(178, 58, 44), width=2)
    d.line([(x + w - 41, y + 10), (x + w // 2, y + 34)], fill=(178, 58, 44), width=2)
    d.line([(x, y + h - 34), (x + w, y + h - 34)], fill=(120, 120, 120), width=3)
    # rising waves
    for wy, ww in [(y + h - 30, 30), (y + h - 18, 44)]:
        for wx in range(x - 20, x + w, 60):
            d.arc([wx, wy, wx + 60, wy + ww], 180, 360, fill=(36, 110, 160),
                  width=5)
    d.rectangle([x, y + h - 10, x + w, y + h], fill=(36, 110, 160))


def scene_flags(d, x, y, w, h):
    vgrad(d, x, y, w, h, (160, 196, 226), (228, 236, 242))
    # UN building slab
    d.rectangle([x + w // 2 - 26, y + 8, x + w // 2 + 26, y + h - 26],
                fill=(64, 110, 160))
    for wy in range(y + 14, y + h - 30, 10):
        d.line([(x + w // 2 - 20, wy), (x + w // 2 + 20, wy)],
               fill=(140, 180, 214), width=2)
    # row of orange flags
    for i in range(6):
        fx = x + 14 + i * ((w - 28) // 6)
        d.line([(fx, y + h - 26), (fx, y + h - 52)], fill=(90, 90, 90), width=2)
        d.polygon([(fx, y + h - 52), (fx + 14, y + h - 47), (fx, y + h - 42)],
                  fill=(232, 116, 24))


def scene_meeting(d, x, y, w, h):
    vgrad(d, x, y, w, h, (168, 196, 222), (228, 234, 240))
    # US flag (stripes + canton)
    fx, fy, fw, fh = x + 14, y + 14, 62, 34
    for i in range(7):
        d.rectangle([fx, fy + i * 5, fx + fw, fy + i * 5 + 5],
                    fill=(178, 44, 44) if i % 2 == 0 else WHITE)
    d.rectangle([fx, fy, fx + 26, fy + 18], fill=(40, 60, 120))
    for sx in range(fx + 4, fx + 24, 7):
        for sy in range(fy + 3, fy + 16, 6):
            d.ellipse([sx, sy, sx + 2, sy + 2], fill=WHITE)
    # NATO-style flag (blue, circle of gold stars)
    nx, ny = x + w - 76, y + 14
    d.rectangle([nx, ny, nx + 62, ny + 34], fill=(36, 84, 160))
    import math
    for k in range(12):
        a = math.radians(k * 30 - 90)
        sx = nx + 31 + int(11 * math.cos(a))
        sy = ny + 17 + int(11 * math.sin(a))
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=GOLD)
    # table + document
    d.rectangle([x + 20, y + h - 26, x + w - 20, y + h - 14], fill=(120, 82, 44))
    d.rectangle([x + w // 2 - 20, y + h - 40, x + w // 2 + 20, y + h - 26],
                fill=WHITE)
    d.line([(x + w // 2 - 15, y + h - 35), (x + w // 2 + 15, y + h - 35)],
           fill=(120, 130, 140), width=2)
    d.ellipse([x + w // 2 + 8, y + h - 32, x + w // 2 + 16, y + h - 26],
              fill=GOLD)


# ---- the 13 stories, most consequential first ----
# (tag, accent, headline, scene)
CARDS = [
    ("SPACE", (30, 90, 160), "Shenzhou-24 carries Pakistani first", scene_rocket),
    ("DIPLOMACY", (178, 44, 44), "N. Korea expels Swiss envoy", scene_embassy),
    ("PACIFIC", (36, 116, 160), "Solomons pick Australia as top partner", scene_treaty),
    ("UKRAINE", (198, 120, 30), "Russian strike kills 2 in Odesa region", scene_odesa),
    ("ENERGY", (120, 80, 140), "Drones reportedly hit two refineries", scene_refinery),
    ("MARKETS", (198, 44, 44), "Asian shares slide on tariff fears", scene_chart),
    ("AUSTRALIA", (46, 128, 66), "Senate passes Digital Duty of Care", scene_senate),
    ("LABOUR", (178, 120, 30), "Bangladesh raises garment wage 36%", scene_factory),
    ("INDONESIA", (120, 82, 44), "Dozens feared trapped in West Java mine", scene_mine),
    ("USA", (150, 90, 40), "US Army to detonate lead-azide stockpile", scene_blast),
    ("CLIMATE", (36, 110, 160), "Bay Area braces for record king tides", scene_tides),
    ("UNITED NATIONS", (232, 116, 24), "UN: 129 flags for women killed daily", scene_flags),
    ("DIPLOMACY", (36, 84, 160), "Trump to meet NATO chief Rutte", scene_meeting),
]


def main():
    img = Image.new("RGB", (W, H), WHITE)
    d = ImageDraw.Draw(img)
    # masthead
    d.rectangle([0, 0, W, 80], fill=NAVY)
    d.rectangle([0, 80, W, 84], fill=GOLD)
    f_date = font(SERIF_B, 40)
    f_sub = font(SANS_B, 13)
    d.text((40, 10), "WEDNESDAY 25 NOVEMBER 2026", font=f_date, fill=WHITE)
    d.text((40, 56), "13 STORIES  •  EACH VERIFIED TO 25 NOVEMBER 2026",
           font=f_sub, fill=GOLD_LIGHT)
    # hero
    hero_yemen(d)
    # label
    f_label = font(SANS_B, 14)
    d.text((40, 392), "MORE TODAY — 13 STORIES", font=f_label, fill=NAVY)
    d.line([(40, 414), (W - 40, 414)], fill=GOLD, width=2)
    # cards: rows of 5, 4, 4
    rows = [CARDS[0:5], CARDS[5:9], CARDS[9:13]]
    ys = [424, 618, 812]
    card_h = 182
    f_tag = font(SANS_B, 11)
    f_head = font(SERIF_B, 14)
    for row, y in zip(rows, ys):
        n = len(row)
        cw = (1024 - 32 - (n - 1) * 8) // n
        total = n * cw + (n - 1) * 8
        x0 = (1024 - total) // 2
        for i, (tag, accent, headline, scene) in enumerate(row):
            cx = x0 + i * (cw + 8)
            d.rectangle([cx, y, cx + cw, y + card_h], fill=CARD_BG,
                        outline=LINE, width=1)
            d.rectangle([cx, y, cx + cw, y + 4], fill=accent)
            scene(d, cx + 1, y + 5, cw - 2, 92)
            d.text((cx + 8, y + 104), tag, font=f_tag, fill=accent)
            lines = wrap(d, headline, f_head, cw - 16)[:3]
            ly = y + 122
            for ln in lines:
                d.text((cx + 8, ly), ln, font=f_head, fill=INK)
                ly += 18
    # footer
    f_foot = font(SANS, 11)
    d.text((40, 1004), "25 NOVEMBER 2026  •  SOURCES: REUTERS, AP, AFP, UN",
           font=f_foot, fill=MUTED)
    img.save("entry.png", format="PNG", optimize=True)


if __name__ == "__main__":
    main()

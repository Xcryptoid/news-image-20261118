"""Draw the front page of THE WORLD TODAY for Wednesday 18 November 2026.

A newspaper-style summary of the day's world news, drawn with Pillow and
DejaVu fonts. Lead story: the Gulf escalation (Iranian drone strikes on US
bases in Kuwait and Bahrain after US jets hit a missile site on Qeshm
Island). Below it a 3x2 grid of six more stories from the same day.
Saves entry.png (1024x1024) next to this file.
"""

import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

W, H = 1024, 1024
PAPER = (248, 245, 236)
INK = (18, 18, 18)
RED = (178, 24, 24)
BLUE = (24, 64, 128)
SEA = (168, 205, 225)
SAND = (232, 214, 170)
PANEL_BG = (255, 255, 255)
RULE = (60, 60, 60)

_fonts = {}


def font(name, size):
    key = (name, size)
    if key not in _fonts:
        _fonts[key] = ImageFont.truetype(os.path.join(FONT_DIR, name), size)
    return _fonts[key]


def wrap(draw, text, fnt, max_w):
    """Split text into lines that fit max_w pixels."""
    lines = []
    for chunk in text.split("\n"):
        words = chunk.split()
        if not words:
            lines.append("")
            continue
        line = words[0]
        for word in words[1:]:
            trial = line + " " + word
            if draw.textlength(trial, font=fnt) <= max_w:
                line = trial
            else:
                lines.append(line)
                line = word
        lines.append(line)
    return lines


def draw_lines(draw, lines, fnt, x, y, color, spacing=4, align="left", width=None):
    """Draw lines of text; returns the y just below the last line."""
    for line in lines:
        if align == "center":
            lx = x + (width - draw.textlength(line, font=fnt)) / 2
        else:
            lx = x
        draw.text((lx, y), line, font=fnt, fill=color)
        y += fnt.size + spacing
    return y


def label(draw, x, y, text, fnt, fg=(20, 20, 20), bg=(255, 255, 255)):
    """Small map label: black text on a white box so it stays readable."""
    w = draw.textlength(text, font=fnt) + 8
    h = fnt.size + 4
    draw.rectangle([x, y, x + w, y + h], fill=bg, outline=(120, 120, 120))
    draw.text((x + 4, y + 2), text, font=fnt, fill=fg)
    return w


def flag_china(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
    cx, cy = x + w * 0.22, y + h * 0.28
    for dx, dy in [(0, 0), (14, 4), (10, 12), (2, 12), (16, 10)]:
        draw.ellipse([cx + dx - 2, cy + dy - 2, cx + dx + 2, cy + dy + 2],
                     fill=(255, 222, 0))


def flag_russia(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h / 3], fill=(255, 255, 255))
    draw.rectangle([x, y + h / 3, x + w, y + 2 * h / 3], fill=(0, 57, 166))
    draw.rectangle([x, y + 2 * h / 3, x + w, y + h], fill=(213, 0, 50))
    draw.rectangle([x, y, x + w, y + h], outline=(120, 120, 120))


def flag_usa(draw, x, y, w, h):
    for i in range(7):
        draw.rectangle([x, y + i * h / 7, x + w, y + (i + 1) * h / 7],
                       fill=(178, 34, 52) if i % 2 == 0 else (255, 255, 255))
    draw.rectangle([x, y, x + w * 0.4, y + h * 0.55], fill=(60, 59, 110))
    for r in range(3):
        for c in range(4):
            draw.ellipse([x + 4 + c * 9, y + 4 + r * 9,
                          x + 8 + c * 9, y + 8 + r * 9], fill=(255, 255, 255))
    draw.rectangle([x, y, x + w, y + h], outline=(120, 120, 120))


def flag_japan(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
    draw.ellipse([x + w / 2 - h * 0.28, y + h / 2 - h * 0.28,
                  x + w / 2 + h * 0.28, y + h / 2 + h * 0.28],
                 fill=(188, 0, 45))
    draw.rectangle([x, y, x + w, y + h], outline=(120, 120, 120))


def flag_india(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h / 3], fill=(255, 153, 51))
    draw.rectangle([x, y + h / 3, x + w, y + 2 * h / 3], fill=(255, 255, 255))
    draw.rectangle([x, y + 2 * h / 3, x + w, y + h], fill=(19, 136, 8))
    draw.ellipse([x + w / 2 - 7, y + h / 2 - 7, x + w / 2 + 7, y + h / 2 + 7],
                 outline=(0, 0, 128), width=2)
    draw.rectangle([x, y, x + w, y + h], outline=(120, 120, 120))


def flag_australia(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(0, 0, 139))
    for sx, sy in [(0.62, 0.25), (0.78, 0.45), (0.60, 0.68), (0.85, 0.72)]:
        draw.ellipse([x + w * sx - 3, y + h * sy - 3,
                      x + w * sx + 3, y + h * sy + 3], fill=(255, 255, 255))
    draw.rectangle([x, y, x + w, y + h], outline=(120, 120, 120))


def art_gulf(draw, x, y, w, h):
    """Simplified Persian Gulf: sea, land, a burning tanker, drones."""
    draw.rectangle([x, y, x + w, y + h], fill=SEA)
    # Land masses: Arabia (bottom), Iran (top right), Kuwait corner (top left).
    draw.polygon([(x, y + h), (x, y + h * 0.72), (x + w * 0.30, y + h * 0.80),
                  (x + w * 0.55, y + h * 0.86), (x + w, y + h * 0.94),
                  (x + w, y + h)], fill=SAND)
    draw.polygon([(x + w * 0.55, y), (x + w, y), (x + w, y + h * 0.30),
                  (x + w * 0.78, y + h * 0.22), (x + w * 0.62, y + h * 0.12)],
                 fill=SAND)
    draw.polygon([(x, y), (x + w * 0.22, y), (x + w * 0.16, y + h * 0.18),
                  (x, y + h * 0.22)], fill=SAND)
    # Strait of Hormuz: narrow gap bottom right.
    draw.polygon([(x + w * 0.86, y + h * 0.86), (x + w, y + h * 0.80),
                  (x + w, y + h), (x + w * 0.92, y + h)], fill=SEA)
    # Tanker with fire mid-sea.
    tx, ty = x + w * 0.42, y + h * 0.52
    draw.rectangle([tx, ty, tx + 150, ty + 26], fill=(40, 40, 40))
    draw.rectangle([tx + 110, ty - 16, tx + 140, ty], fill=(200, 60, 30))
    for i, (fx, fy, fr) in enumerate([(8, -14, 12), (26, -22, 15), (46, -12, 11),
                                      (66, -20, 13), (86, -10, 10)]):
        draw.ellipse([tx + fx - fr, ty + fy - fr, tx + fx + fr, ty + fy + fr],
                     fill=(255, 140, 0) if i % 2 == 0 else (255, 60, 0))
    for sx, sy, sr in [(30, -48, 12), (55, -60, 15), (80, -46, 11)]:
        draw.ellipse([tx + sx - sr, ty + sy - sr, tx + sx + sr, ty + sy + sr],
                     fill=(90, 90, 90))
    # Drones: small black crosses with dotted trails.
    for dx, dy in [(0.16, 0.30), (0.30, 0.18), (0.72, 0.30)]:
        px, py = x + w * dx, y + h * dy
        draw.line([px - 60, py + 26, px - 8, py + 4], fill=(60, 60, 60),
                  width=2)
        draw.line([px - 9, py - 9, px + 9, py + 9], fill=(15, 15, 15), width=3)
        draw.line([px - 9, py + 9, px + 9, py - 9], fill=(15, 15, 15), width=3)
    small = font("DejaVuSans-Bold.ttf", 15)
    label(draw, x + 10, y + 8, "KUWAIT", small)
    label(draw, x + 8, y + h * 0.55, "BAHRAIN", small)
    label(draw, x + w - 150, y + 8, "QESHM ISLAND", small)
    label(draw, x + w - 210, y + h - 26, "STRAIT OF HORMUZ", small)


def art_summit(draw, x, y, w, h):
    """Three flags (China, Russia, US) with a location line below."""
    fw, fh = (w - 40) / 3, 64
    flag_china(draw, x + 10, y + 6, fw, fh)
    flag_russia(draw, x + 20 + fw, y + 6, fw, fh)
    flag_usa(draw, x + 30 + 2 * fw, y + 6, fw, fh)
    draw.line([x + 10, y + fh + 14, x + w - 10, y + fh + 14],
              fill=(150, 120, 60), width=3)
    small = font("DejaVuSans-Bold.ttf", 17)
    draw.text((x + 10, y + fh + 22), "SHENZHEN  •  THURSDAY",
              font=small, fill=INK)


def art_quad(draw, x, y, w, h):
    """Four Quad flags in a row."""
    fw, fh = (w - 50) / 4, 56
    flag_usa(draw, x + 10, y + 10, fw, fh)
    flag_japan(draw, x + 20 + fw, y + 10, fw, fh)
    flag_india(draw, x + 30 + 2 * fw, y + 10, fw, fh)
    flag_australia(draw, x + 40 + 3 * fw, y + 10, fw, fh)
    small = font("DejaVuSans-Bold.ttf", 17)
    draw.text((x + 10, y + h - 32), "MANILA  •  FIRST IN 2 YEARS",
              font=small, fill=INK)


def art_bridge(draw, x, y, w, h):
    """A bridge with its middle span collapsed into the water."""
    draw.rectangle([x, y, x + w, y + h], fill=(214, 228, 240))
    # Water at the bottom.
    draw.rectangle([x, y + h - 34, x + w, y + h], fill=(120, 170, 210))
    for wy in range(3):
        yy = y + h - 28 + wy * 9
        draw.line([(x + 8 + wy * 30, yy), (x + 60 + wy * 30, yy)],
                  fill=(255, 255, 255), width=2)
    # Deck: left part intact, middle span broken and tilted, right part intact.
    mid = x + w / 2
    draw.rectangle([x + 8, y + 46, mid - 52, y + 58], fill=(70, 70, 70))
    draw.rectangle([mid + 52, y + 46, x + w - 8, y + 58], fill=(70, 70, 70))
    draw.polygon([(mid - 52, y + 58), (mid - 8, y + 96), (mid + 6, y + 96),
                  (mid - 34, y + 58)], fill=(90, 90, 90))
    # Towers.
    for tx in (x + 60, x + w - 76):
        draw.rectangle([tx, y + 12, tx + 14, y + 58], fill=(50, 50, 50))
    # Smoke over the break (coordinates are relative to the panel art).
    for sx, sy, sr in [(mid - 18, 26, 12), (mid + 4, 16, 15), (mid + 24, 28, 11)]:
        draw.ellipse([sx - sr, y + sy - sr, sx + sr, y + sy + sr],
                     fill=(110, 110, 110))
    # Flames at the break.
    draw.ellipse([mid - 14, y + 62, mid + 2, y + 78], fill=(255, 120, 0))
    draw.ellipse([mid + 2, y + 66, mid + 16, y + 80], fill=(255, 60, 0))


def art_ballot(draw, x, y, w, h):
    """A ballot box with a big 56-44 score."""
    draw.rectangle([x + 18, y + 30, x + 130, y + h - 12], fill=(200, 40, 40),
                   outline=INK, width=2)
    draw.rectangle([x + 30, y + 18, x + 118, y + 30], fill=(255, 255, 255),
                   outline=INK, width=2)
    draw.line([x + 58, y + 22, x + 88, y + 22], fill=INK, width=3)
    big = font("DejaVuSans-Bold.ttf", 44)
    draw.text((x + 150, y + 22), "56–44", font=big, fill=BLUE)
    small = font("DejaVuSans-Bold.ttf", 16)
    draw.text((x + 150, y + 78), "DEMOCRATS", font=small, fill=INK)


def art_virus(draw, x, y, w, h):
    """Red measles virus: spiked circles."""
    cx, cy = x + 62, y + h / 2 + 4
    for ang in range(0, 360, 30):
        import math
        rad = math.radians(ang)
        x1 = cx + 26 * math.cos(rad)
        y1 = cy + 26 * math.sin(rad)
        x2 = cx + 40 * math.cos(rad)
        y2 = cy + 40 * math.sin(rad)
        draw.line([x1, y1, x2, y2], fill=(178, 24, 24), width=5)
        draw.ellipse([x2 - 6, y2 - 6, x2 + 6, y2 + 6], fill=(178, 24, 24))
    draw.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], fill=(214, 48, 48))
    # Small viruses along the bottom edge, clear of the text.
    for sx, sy, sr in [(x + 190, y + h - 16, 10), (x + 250, y + h - 14, 8),
                       (x + 285, y + h - 22, 6)]:
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(214, 48, 48))
    big = font("DejaVuSans-Bold.ttf", 40)
    draw.text((x + 150, y + 14), "5,400+", font=big, fill=RED)
    small = font("DejaVuSans-Bold.ttf", 16)
    draw.text((x + 152, y + 66), "CASES", font=small, fill=INK)


def art_parliament(draw, x, y, w, h):
    """A parliament building with columns and a dome."""
    bx, by = x + 16, y + 34
    bw, bh = w - 32, h - 72
    draw.rectangle([bx, by + 26, bx + bw, by + bh], fill=(226, 216, 190),
                   outline=INK, width=2)
    draw.polygon([(bx + bw / 2 - 46, by), (bx + bw / 2 + 46, by),
                  (bx + bw / 2, by - 18)], fill=(178, 24, 24))
    for i in range(5):
        cx = bx + 24 + i * (bw - 48) / 4
        draw.rectangle([cx - 7, by + 34, cx + 7, by + bh - 10],
                       fill=(255, 255, 255), outline=INK)
    small = font("DejaVuSans-Bold.ttf", 16)
    draw.text((x + 16, y + h - 24), "JERUSALEM", font=small, fill=INK)


def panel(draw, x, y, w, h, headline, caption, art):
    draw.rectangle([x, y, x + w, y + h], fill=PANEL_BG, outline=INK, width=2)
    head_f = font("DejaVuSans-Bold.ttf", 24)
    cap_f = font("DejaVuSans.ttf", 15)
    lines = wrap(draw, headline, head_f, w - 20)
    ty = draw_lines(draw, lines[:2], head_f, x + 10, y + 8, INK, spacing=2)
    art(draw, x + 4, ty + 2, w - 8, h - (ty - y) - 52)
    cap_lines = wrap(draw, caption, cap_f, w - 20)
    draw_lines(draw, cap_lines[:2], cap_f, x + 10, y + h - 44, (40, 40, 40),
               spacing=1)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([10, 10, W - 10, H - 10], outline=INK, width=3)

    # Masthead.
    mast = font("DejaVuSerif-Bold.ttf", 64)
    title = "THE WORLD TODAY"
    d.text(((W - d.textlength(title, font=mast)) / 2, 26), title,
           font=mast, fill=INK)
    d.line([24, 106, W - 24, 106], fill=RULE, width=2)

    # Date line in red.
    date_f = font("DejaVuSans-Bold.ttf", 28)
    date = "WEDNESDAY, 18 NOVEMBER 2026"
    d.text(((W - d.textlength(date, font=date_f)) / 2, 116), date,
           font=date_f, fill=RED)
    d.line([24, 152, W - 24, 152], fill=RULE, width=2)

    # Lead story.
    lead_f = font("DejaVuSans-Bold.ttf", 40)
    lead = "IRAN STRIKES US BASES\nIN KUWAIT AND BAHRAIN"
    ly = 166
    for line in lead.split("\n"):
        d.text(((W - d.textlength(line, font=lead_f)) / 2, ly), line,
               font=lead_f, fill=INK)
        ly += 48
    art_gulf(d, 24, 268, W - 48, 128)
    cap_f = font("DejaVuSans.ttf", 18)
    cap = ("Drones hit Ali Al Salem Air Base in Kuwait and US sites in Bahrain, "
           "after US jets struck a missile site on Qeshm Island in the Strait of Hormuz.")
    cap_lines = wrap(d, cap, cap_f, W - 48)
    draw_lines(d, cap_lines[:2], cap_f, 24, 404, (40, 40, 40), spacing=2)
    d.line([24, 452, W - 24, 452], fill=RULE, width=2)

    # Six panels, 3 x 2.
    pw, ph = 317, 232
    gx, gy = 24, 466
    stories = [
        ("XI AND PUTIN MEET;\nTRUMP SUMMIT THURSDAY",
         "Xi and Putin talk in Shenzhen; first three-way summit set for Thursday.",
         art_summit),
        ("QUAD LEADERS MEET\nIN MANILA",
         "First leader-level Quad in over two years; Trump hails a Philippines trade deal.",
         art_quad),
        ("UKRAINE HITS CRIMEA\nBRIDGE AGAIN",
         "A span partly collapses; Russian drones over Dnipro injure six.",
         art_bridge),
        ("PELTOLA WINS\nALASKA SENATE SEAT",
         "Peltola wins; Democrats take a 56–44 majority.",
         art_ballot),
        ("US LOSES MEASLES-\nFREE STATUS",
         "Elimination status lost after 26 years, with 5,400+ cases reported.",
         art_virus),
        ("KAHANA ELECTED\nKNESSET SPEAKER",
         "Israel's parliament picks Matan Kahana — a blow for Netanyahu.",
         art_parliament),
    ]
    for i, (head, cap_text, art) in enumerate(stories):
        px = gx + (i % 3) * (pw + 12)
        py = gy + (i // 3) * (ph + 12)
        panel(d, px, py, pw, ph, head, cap_text, art)

    # Footer.
    foot_f = font("DejaVuSans-Bold.ttf", 16)
    foot = "18 NOVEMBER 2026  —  THE WORLD IN ONE IMAGE"
    d.text(((W - d.textlength(foot, font=foot_f)) / 2, 962), foot,
           font=foot_f, fill=INK)

    out = os.path.join(HERE, "entry.png")
    img.save(out, "PNG")
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    build()

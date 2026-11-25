#!/usr/bin/env python3
"""Build entry.png: a newspaper front page summing up the world news of
Tuesday 24 November 2026. Run locally with Pillow; the graded program
(main.py) only copies the finished entry.png, so it needs no libraries.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BG = (248, 244, 236)
INK = (18, 18, 18)
GREY = (92, 88, 80)
RED = (178, 30, 40)
GREEN = (8, 118, 62)
RULE = (18, 18, 18)

SERIF_B = "/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc"
SANS_B = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
SANS_R = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)
M = 44                      # page margin
CW = W - 2 * M              # content width


def font(path, size):
    return ImageFont.truetype(path, size, index=0)


def fit(path, text, max_w, start, floor=10):
    """Largest font size <= start whose text fits max_w."""
    s = start
    while s > floor:
        f = font(path, s)
        if d.textlength(text, font=f) <= max_w:
            return f
        s -= 2
    return font(path, floor)


def centered(text, y, f, fill=INK):
    w = d.textlength(text, font=f)
    d.text(((W - w) / 2, y), text, font=f, fill=fill)
    return y + f.size


def wrap(text, f, max_w):
    words, lines, cur = text.split(), [], ""
    for wd in words:
        t = wd if not cur else cur + " " + wd
        if d.textlength(t, font=f) <= max_w:
            cur = t
        else:
            lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def para(x, y, text, f, max_w, leading, fill=INK):
    for ln in wrap(text, f, max_w):
        d.text((x, y), ln, font=f, fill=fill)
        y += leading
    return y


def hrule(y, thick=3):
    d.line([(M, y), (W - M, y)], fill=RULE, width=thick)
    return y + thick


# ---------------------------------------------------------------- masthead
hrule(28, 4)
hrule(38, 1)
centered("THE WORLD TODAY", 48, fit(SERIF_B, "THE WORLD TODAY", CW, 100))
y = 164
d.rectangle([M, y, W - M, y + 42], fill=INK)
centered("TUESDAY · 24 NOVEMBER 2026 · THE DAY IN ONE PICTURE", y + 5,
         fit(SANS_B, "TUESDAY · 24 NOVEMBER 2026 · THE DAY IN ONE PICTURE",
             CW - 30, 29), fill=(255, 255, 255))
hrule(y + 52, 2)

# ---------------------------------------------------------------- lead story
y = 232
d.text((M, y), "TECH · MARKETS — THE DAY'S BIG STORY", font=font(SANS_B, 24),
       fill=RED)
y += 34
f = fit(SERIF_B, "HUANG RETURNS TO NVIDIA", CW, 58)
d.text((M, y), "HUANG RETURNS TO NVIDIA", font=f, fill=INK)
y += f.size + 2
f = fit(SERIF_B, "IN BOOMERANG-CEO SHOCKER", CW, 58)
d.text((M, y), "IN BOOMERANG-CEO SHOCKER", font=f, fill=INK)
y += f.size + 8
y = para(M, y,
         "Eleven days after resigning in scandal, Jensen Huang is back as "
         "Nvidia's chief executive after President Trump intervened — and "
         "Wall Street erupts.",
         font(SANS_R, 25), CW, 33)
y += 8

# ---------------------------------------------------------------- chart strip
box_t, box_b = y, y + 118
d.rectangle([M, box_t, W - M, box_b], outline=RULE, width=2)
d.text((M + 18, box_t + 9), "MONDAY'S MARKET ERUPTION", font=font(SANS_B, 20),
       fill=GREY)
stats = [("NVDA", "+31%"), ("NASDAQ", "+6.5%"), ("S&P 500", "+4.7%")]
sx = M + 18
for name, val in stats:
    d.text((sx, box_t + 38), name, font=font(SANS_B, 22), fill=INK)
    d.text((sx, box_t + 64), val, font=font(SANS_B, 40), fill=GREEN)
    sx += 205
# rising line chart, right side of the box
cx0, cy0, cx1, cy1 = W - M - 250, box_t + 88, W - M - 22, box_t + 30
pts = [(cx0, cy1 + 50), (cx0 + 55, cy1 + 42), (cx0 + 105, cy1 + 47),
       (cx0 + 155, cy1 + 20), (cx1, cy1 - 4)]
d.line([(cx0, cy0), (cx1, cy0)], fill=GREY, width=2)
d.line(pts, fill=GREEN, width=6, joint="curve")
for px, py in pts:
    d.ellipse([px - 5, py - 5, px + 5, py + 5], fill=GREEN)
d.polygon([(cx1, cy1 - 12), (cx1 - 2, cy1 + 7), (cx1 - 19, cy1 - 1)],
          fill=GREEN)
y = box_b + 10

# ---------------------------------------------------------------- two columns
hrule(y, 2)
y += 12
col_w = (CW - 36) // 2
col2_x = M + col_w + 36
body_f = font(SANS_R, 20)

d.text((M, y), "SPACE · DEFENCE", font=font(SANS_B, 20), fill=RED)
y1 = para(M, y + 29,
          "RUSSIA EYES NUCLEAR SPACE WEAPON, ALLIES WARN",
          fit(SERIF_B, "RUSSIA EYES NUCLEAR", col_w, 31), col_w, 36)
y1 = para(M, y1 + 4,
          "German reports say Moscow could launch a satellite-killing "
          "nuclear device within weeks; NATO vows a space-defence answer.",
          body_f, col_w, 26, fill=(40, 40, 40))

d.text((col2_x, y), "UKRAINE WAR", font=font(SANS_B, 20), fill=RED)
y2 = para(col2_x, y + 29,
          "UKRAINE SINKS RUSSIAN WARSHIP OFF LIBYA",
          fit(SERIF_B, "UKRAINE SINKS RUSSIAN", col_w, 31), col_w, 36)
y2 = para(col2_x, y2 + 4,
          "Kyiv's strike far from home shows a widening reach, as leaked "
          "data puts Russia's death toll near 500,000.",
          body_f, col_w, 26, fill=(40, 40, 40))
y = max(y1, y2) + 12

# ---------------------------------------------------------------- briefs row
hrule(y, 2)
y += 12
d.text((M, y), "HASINA'S HOMECOMING", font=font(SANS_B, 22), fill=INK)
para(M, y + 31,
     "Ousted Bangladeshi PM Sheikh Hasina says she will fly home on "
     "16 December — despite facing a death sentence.",
     body_f, col_w, 26, fill=(40, 40, 40))
d.text((col2_x, y), "STATES SUE OVER GROK", font=font(SANS_B, 22), fill=INK)
para(col2_x, y + 31,
     "U.S. states sue Elon Musk's firms over sexualised images from "
     "the Grok chatbot; UN chief wants AI risk rules within a year.",
     body_f, col_w, 26, fill=(40, 40, 40))

# ---------------------------------------------------------------- footer
hrule(H - 50, 2)
centered("As reported on 24 November 2026 · Reuters · AP · SCMP · "
         "The Japan Times", H - 38, font(SANS_R, 17), fill=GREY)

img.save("entry.png", optimize=True)
print("wrote entry.png", img.size)

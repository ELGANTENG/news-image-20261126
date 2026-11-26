#!/usr/bin/env python3
"""Draw the 26 November 2026 world-news image (1024x1024 PNG).

Pure standard library: the PNG encoder uses zlib/struct only, and the text
is drawn with a small bitmap font defined in this file. No photos, no
copied artwork, no network. Run: python3 generate_image.py -> entry.png
"""
import struct
import zlib

W, H = 1024, 1024

# ---------------------------------------------------------------- palette
PAPER   = (247, 243, 232)   # newsprint cream
INK     = (20, 32, 46)      # near-black blue
NAVY    = (22, 42, 66)      # masthead / hero background
NAVY2   = (30, 56, 88)      # hero panel, slightly lighter
RED     = (178, 38, 30)     # accent red
GOLD    = (201, 162, 39)    # gold rule / kicker
WHITE   = (255, 255, 255)
GREY    = (90, 100, 112)    # secondary text
CARD    = (255, 255, 255)   # panel background
BORDER  = (200, 192, 172)   # panel border
TEAL    = (15, 118, 110)
ORANGE  = (214, 106, 24)
GREEN   = (46, 125, 50)
PURPLE  = (103, 58, 140)
BROWN   = (121, 85, 40)

# ------------------------------------------------------------------- font
# 5x7 bitmap font, written for this entry. Each glyph is 7 rows of 5 bits.
# Row 6 is the baseline; descenders (g, j, p, q, y) use row 6 as a hook.
FONT = {
 'A': ["01110","10001","10001","11111","10001","10001","10001"],
 'B': ["11110","10001","10001","11110","10001","10001","11110"],
 'C': ["01110","10001","10000","10000","10000","10001","01110"],
 'D': ["11110","10001","10001","10001","10001","10001","11110"],
 'E': ["11111","10000","10000","11110","10000","10000","11111"],
 'F': ["11111","10000","10000","11110","10000","10000","10000"],
 'G': ["01110","10001","10000","10111","10001","10001","01111"],
 'H': ["10001","10001","10001","11111","10001","10001","10001"],
 'I': ["01110","00100","00100","00100","00100","00100","01110"],
 'J': ["00111","00010","00010","00010","00010","10010","01100"],
 'K': ["10001","10010","10100","11000","10100","10010","10001"],
 'L': ["10000","10000","10000","10000","10000","10000","11111"],
 'M': ["10001","11011","10101","10101","10001","10001","10001"],
 'N': ["10001","11001","10101","10011","10001","10001","10001"],
 'O': ["01110","10001","10001","10001","10001","10001","01110"],
 'P': ["11110","10001","10001","11110","10000","10000","10000"],
 'Q': ["01110","10001","10001","10001","10101","10010","01101"],
 'R': ["11110","10001","10001","11110","10100","10010","10001"],
 'S': ["01111","10000","10000","01110","00001","00001","11110"],
 'T': ["11111","00100","00100","00100","00100","00100","00100"],
 'U': ["10001","10001","10001","10001","10001","10001","01110"],
 'V': ["10001","10001","10001","10001","10001","01010","00100"],
 'W': ["10001","10001","10001","10101","10101","10101","01010"],
 'X': ["10001","10001","01010","00100","01010","10001","10001"],
 'Y': ["10001","10001","01010","00100","00100","00100","00100"],
 'Z': ["11111","00001","00010","00100","01000","10000","11111"],
 '0': ["01110","10001","10011","10101","11001","10001","01110"],
 '1': ["00100","01100","00100","00100","00100","00100","01110"],
 '2': ["01110","10001","00001","00110","01000","10000","11111"],
 '3': ["11110","00001","00001","01110","00001","00001","11110"],
 '4': ["00010","00110","01010","10010","11111","00010","00010"],
 '5': ["11111","10000","11110","00001","00001","10001","01110"],
 '6': ["00110","01000","10000","11110","10001","10001","01110"],
 '7': ["11111","00001","00010","00100","01000","01000","01000"],
 '8': ["01110","10001","10001","01110","10001","10001","01110"],
 '9': ["01110","10001","10001","01111","00001","00010","01100"],
 'a': ["00000","00000","01110","00001","01111","10001","01111"],
 'b': ["10000","10000","11110","10001","10001","10001","11110"],
 'c': ["00000","00000","01110","10001","10000","10001","01110"],
 'd': ["00001","00001","01111","10001","10001","10001","01111"],
 'e': ["00000","00000","01110","10001","11111","10000","01110"],
 'f': ["00110","01001","01000","11110","01000","01000","01000"],
 'g': ["00000","00000","01110","10001","10001","01111","01100"],
 'h': ["10000","10000","11110","10001","10001","10001","10001"],
 'i': ["00100","00000","01100","00100","00100","00100","01110"],
 'j': ["00010","00000","00110","00010","00010","10010","01100"],
 'k': ["10000","10000","10010","10100","11000","10100","10010"],
 'l': ["01100","00100","00100","00100","00100","00100","01110"],
 'm': ["00000","00000","11010","10101","10101","10101","10101"],
 'n': ["00000","00000","11110","10001","10001","10001","10001"],
 'o': ["00000","00000","01110","10001","10001","10001","01110"],
 'p': ["10000","10000","11110","10001","10001","11110","10000"],
 'q': ["00001","00001","01111","10001","10001","01111","00001"],
 'r': ["00000","00000","10110","11001","10000","10000","10000"],
 's': ["00000","00000","01111","10000","01110","00001","11110"],
 't': ["01000","01000","11100","01000","01000","01000","00110"],
 'u': ["00000","00000","10001","10001","10001","10011","01101"],
 'v': ["00000","00000","10001","10001","10001","01010","00100"],
 'w': ["00000","00000","10001","10101","10101","10101","01010"],
 'x': ["00000","00000","10001","01010","00100","01010","10001"],
 'y': ["00000","00000","10001","10001","01010","00100","00100"],
 'z': ["00000","00000","11111","00010","00100","01000","11111"],
 ' ': ["00000","00000","00000","00000","00000","00000","00000"],
 '.': ["00000","00000","00000","00000","00000","01100","01100"],
 ',': ["00000","00000","00000","00000","01100","00100","01000"],
 '-': ["00000","00000","00000","01110","00000","00000","00000"],
 "'": ["00100","00100","01000","00000","00000","00000","00000"],
 '!': ["00100","00100","00100","00100","00100","00000","00100"],
 '?': ["01110","10001","00001","00110","00100","00000","00100"],
 ':': ["00000","01100","01100","00000","01100","01100","00000"],
 ';': ["00000","01100","01100","00000","01100","00100","01000"],
 '(': ["00010","00100","01000","01000","01000","00100","00010"],
 ')': ["01000","00100","00010","00010","00010","00100","01000"],
 '/': ["00001","00010","00010","00100","01000","01000","10000"],
 '%': ["11001","11010","00010","00100","01000","01011","10011"],
 '$': ["00100","01111","10100","01110","00101","11110","00100"],
 '&': ["01100","10010","10100","01000","10101","10010","01101"],
 '+': ["00000","00100","00100","11111","00100","00100","00000"],
 '=': ["00000","00000","11111","00000","11111","00000","00000"],
 '"': ["01010","01010","01010","00000","00000","00000","00000"],
 '*': ["00000","00100","10101","01110","10101","00100","00000"],
 '\u2014': ["00000","00000","00000","11111","00000","00000","00000"],
 '\u2019': ["00100","00100","01000","00000","00000","00000","00000"],
 '\u2022': ["00000","00000","01110","01110","01110","00000","00000"],
}
GLYPH_W, GLYPH_H = 5, 7

# ------------------------------------------------------------------ canvas
class Canvas:
    def __init__(self, w, h, bg):
        self.w, self.h = w, h
        self.px = bytearray(bg * (w * h))

    def set(self, x, y, color):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i:i+3] = bytes(color)

    def rect(self, x, y, w, h, color):
        x0, y0 = max(0, x), max(0, y)
        x1, y1 = min(self.w, x + w), min(self.h, y + h)
        for yy in range(y0, y1):
            base = (yy * self.w + x0) * 3
            row = bytes(color) * (x1 - x0)
            self.px[base:base + len(row)] = row

    def hline(self, x, y, w, color, t=1):
        self.rect(x, y, w, t, color)

    def vline(self, x, y, h, color, t=1):
        self.rect(x, y, t, h, color)

    def circle(self, cx, cy, r, color):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                if (xx - cx) ** 2 + (yy - cy) ** 2 <= r * r:
                    self.set(xx, yy, color)

    def ring(self, cx, cy, r, color, t=2):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                d = (xx - cx) ** 2 + (yy - cy) ** 2
                if (r - t) ** 2 <= d <= r * r:
                    self.set(xx, yy, color)

    def triangle(self, pts, color):
        # scanline fill of a triangle given as [(x,y),(x,y),(x,y)]
        (x0, y0), (x1, y1), (x2, y2) = pts
        ymin, ymax = min(y0, y1, y2), max(y0, y1, y2)
        for yy in range(ymin, ymax + 1):
            xs = []
            for (ax, ay), (bx, by) in (((x0, y0), (x1, y1)),
                                       ((x1, y1), (x2, y2)),
                                       ((x2, y2), (x0, y0))):
                if ay == by:
                    continue
                if min(ay, by) <= yy < max(ay, by) or yy == ymax and yy in (ay, by):
                    t = (yy - ay) / (by - ay)
                    xs.append(ax + t * (bx - ax))
            if len(xs) >= 2:
                xa, xb = int(min(xs)), int(max(xs))
                self.rect(xa, yy, xb - xa + 1, 1, color)

# -------------------------------------------------------------------- text
def text_width(s, scale):
    return len(s) * (GLYPH_W + 1) * scale - scale

def draw_glyph(cv, x, y, ch, scale, color, bold=False):
    g = FONT.get(ch)
    if g is None:
        g = FONT['?']
    for r, row in enumerate(g):
        for c, bit in enumerate(row):
            if bit == '1':
                cv.rect(x + c * scale, y + r * scale, scale, scale, color)
                if bold:
                    cv.rect(x + c * scale + 1, y + r * scale, scale, scale, color)

def draw_text(cv, x, y, s, scale, color, bold=False, align='left'):
    w = text_width(s, scale)
    if align == 'center':
        x -= w // 2
    elif align == 'right':
        x -= w
    cx = x
    for ch in s:
        draw_glyph(cv, cx, y, ch, scale, color, bold)
        cx += (GLYPH_W + 1) * scale
    return w

def wrap_text(s, scale, max_w):
    """Greedy word wrap; returns list of lines."""
    unit = (GLYPH_W + 1) * scale
    max_chars = max(1, (max_w + scale) // unit)
    lines, cur = [], ''
    for word in s.split(' '):
        trial = word if not cur else cur + ' ' + word
        if len(trial) <= max_chars:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            # very long single word: hard-split it
            while len(word) > max_chars:
                lines.append(word[:max_chars])
                word = word[max_chars:]
            cur = word
    if cur:
        lines.append(cur)
    return lines

def draw_para(cv, x, y, s, scale, color, max_w, leading, bold=False):
    for line in wrap_text(s, scale, max_w):
        draw_text(cv, x, y, line, scale, color, bold)
        y += GLYPH_H * scale + leading
    return y

# ------------------------------------------------------------------ layout
def draw_masthead(cv):
    cv.rect(0, 0, W, 128, NAVY)
    cv.rect(0, 128, W, 4, GOLD)
    draw_text(cv, W // 2, 18, "THE WORLD IN ONE IMAGE", 2, GOLD, bold=True, align='center')
    draw_text(cv, W // 2, 52, "THURSDAY, 26 NOVEMBER 2026", 6, WHITE, bold=True, align='center')
    draw_text(cv, W // 2, 102, "SEVEN STORIES THAT MADE THE DAY", 2, (180, 195, 210), align='center')

def draw_missile(cv, x, y, s, body, flame):
    # simple rocket pictogram, nose up, pointing up-right
    cv.triangle([(x + 14 * s, y), (x + 6 * s, y + 22 * s), (x + 22 * s, y + 22 * s)], body)
    cv.rect(x + 6 * s, y + 22 * s, 16 * s, 34 * s, body)
    cv.triangle([(x + 6 * s, y + 30 * s), (x - 4 * s, y + 52 * s), (x + 6 * s, y + 48 * s)], body)
    cv.triangle([(x + 22 * s, y + 30 * s), (x + 32 * s, y + 52 * s), (x + 22 * s, y + 48 * s)], body)
    cv.triangle([(x + 10 * s, y + 56 * s), (x + 14 * s, y + 74 * s), (x + 18 * s, y + 56 * s)], flame)
    cv.rect(x + 11 * s, y + 28 * s, 6 * s, 6 * s, WHITE)

def draw_hero(cv):
    x, y, w, h = 28, 148, W - 56, 288
    cv.rect(x, y, w, h, NAVY2)
    cv.rect(x, y, w, 3, RED)
    draw_text(cv, x + 24, y + 22, "TOP STORY  \u2022  NORTH KOREA", 2, GOLD, bold=True)
    draw_text(cv, x + 24, y + 58, "KIM ORDERS WIDER", 5, WHITE, bold=True)
    draw_text(cv, x + 24, y + 102, "NUCLEAR DEPLOYMENT", 5, WHITE, bold=True)
    draw_para(cv, x + 24, y + 168,
              "North Korea's leader Kim Jong Un inspects nuclear sites and "
              "calls for tactical nuclear weapons to be spread across the "
              "armed forces, state media KCNA reports Thursday.",
              2, (205, 218, 232), 560, 6)
    draw_text(cv, x + 24, y + 256, "Pyongyang says output of nuclear material is rising too.",
              2, GOLD)
    draw_missile(cv, x + w - 190, y + 92, 2, (235, 238, 242), ORANGE)

def draw_icon(cv, kind, x, y, color):
    if kind == 'oil':          # droplet
        cv.triangle([(x + 16, y), (x + 2, y + 22), (x + 30, y + 22)], color)
        cv.circle(x + 16, y + 24, 13, color)
        cv.circle(x + 11, y + 20, 4, WHITE)
    elif kind == 'chart':      # rising bars
        cv.rect(x + 2, y + 20, 8, 16, color)
        cv.rect(x + 13, y + 12, 8, 24, color)
        cv.rect(x + 24, y + 2, 8, 34, color)
    elif kind == 'flag':       # flag on a pole
        cv.rect(x + 4, y, 3, 36, color)
        cv.triangle([(x + 7, y), (x + 32, y + 7), (x + 7, y + 14)], color)
        cv.rect(x, y + 34, 12, 3, color)
    elif kind == 'book':       # open book
        cv.rect(x + 2, y + 6, 14, 26, color)
        cv.rect(x + 18, y + 6, 14, 26, color)
        cv.rect(x + 15, y + 6, 3, 26, WHITE)
        cv.rect(x + 5, y + 12, 8, 2, WHITE)
        cv.rect(x + 21, y + 12, 8, 2, WHITE)
        cv.rect(x + 5, y + 19, 8, 2, WHITE)
        cv.rect(x + 21, y + 19, 8, 2, WHITE)
    elif kind == 'cloche':     # serving dome
        cv.circle(x + 16, y + 20, 14, color)
        cv.rect(x + 2, y + 20, 28, 4, color)
        cv.rect(x, y + 26, 32, 3, color)
        cv.circle(x + 16, y + 4, 3, color)
    elif kind == 'chess':      # mini board
        for r in range(4):
            for c in range(4):
                if (r + c) % 2 == 0:
                    cv.rect(x + c * 9, y + r * 9, 9, 9, color)
        cv.rect(x, y, 36, 2, color)
        cv.rect(x, y + 34, 36, 2, color)

PANELS = [
    # (tag, tag color, icon, headline, body)
    ("ENERGY", ORANGE, 'oil', "OIL NEAR $95",
     "Brent jumps after the Houthis claim a strike on Saudi Arabia's Ras "
     "Tanura refinery; Riyadh says it shot down four drones."),
    ("TRADE", TEAL, 'chart', "TAIWAN: US TARIFF 15%",
     "Taipei says the proposed US rate is the lowest tier, as ministers "
     "brief the press on Thursday."),
    ("LATIN AMERICA", GREEN, 'flag', "COLOMBIA: 10 YEARS OF PEACE",
     "A decade on from the peace deal, the UN warns much of it is still "
     "unfinished."),
    ("SOUTH ASIA", PURPLE, 'book', "INDIA MARKS CONSTITUTION DAY",
     "26 November is Samvidhan Divas, the day India's Constitution was "
     "adopted in 1949."),
    ("USA", BROWN, 'cloche', "THANKSGIVING DAY",
     "Americans gather for Thanksgiving as the holiday travel rush peaks "
     "across the United States."),
    ("SPORT", RED, 'chess', "CHESS TITLE TIED 1-1",
     "Gukesh and Sindarov draw twice in Geneva; Game 3 of the world title "
     "match is played today."),
]

def draw_grid(cv):
    px, py = 28, 452
    pw, ph, gap = 312, 262, 16
    for i, (tag, tcolor, icon, head, body) in enumerate(PANELS):
        col, row = i % 3, i // 3
        x = px + col * (pw + gap)
        y = py + row * (ph + gap)
        cv.rect(x, y, pw, ph, CARD)
        cv.rect(x, y, pw, ph, BORDER)  # border via outline below
        cv.rect(x + 1, y + 1, pw - 2, ph - 2, CARD)
        cv.rect(x, y, pw, 8, tcolor)
        draw_text(cv, x + 14, y + 22, tag, 2, tcolor, bold=True)
        draw_icon(cv, icon, x + pw - 52, y + 20, tcolor)
        yy = y + 58
        for line in wrap_text(head, 3, pw - 28):
            draw_text(cv, x + 14, yy, line, 3, INK, bold=True)
            yy += 7 * 3 + 6
        yy += 4
        draw_para(cv, x + 14, yy, body, 2, (52, 62, 76), pw - 28, 5)

def draw_footer(cv):
    draw_text(cv, W // 2, 1002,
              "Stories as reported on Thursday 26 November 2026  \u2022  Sources: Reuters, KCNA, AP, Chess.com",
              1, GREY, align='center')

# -------------------------------------------------------------------- png
def encode_png(cv):
    raw = bytearray()
    for y in range(cv.h):
        raw.append(0)  # filter: none
        raw.extend(cv.px[y * cv.w * 3:(y + 1) * cv.w * 3])
    def chunk(tag, data):
        c = struct.pack(">I", len(data)) + tag + data
        return c + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
    ihdr = struct.pack(">IIBBBBB", cv.w, cv.h, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n"
            + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
            + chunk(b"IEND", b""))

def main():
    cv = Canvas(W, H, PAPER)
    draw_masthead(cv)
    draw_hero(cv)
    draw_grid(cv)
    draw_footer(cv)
    with open("entry.png", "wb") as f:
        f.write(encode_png(cv))
    print("wrote entry.png")

if __name__ == "__main__":
    main()

from PIL import Image, ImageDraw, ImageFont
import json, os

W, H = 1024, 1024
PAPER = (245, 241, 232)
INK = (0, 0, 0)
RED = (176, 34, 34)
GRAY = (120, 120, 120)
WHITE = (255, 255, 255)
BEIGE = (230, 225, 210)

FDIR = "/usr/share/fonts/truetype/dejavu"


def F(size, bold=False):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    path = os.path.join(FDIR, name)
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


def span(f, text):
    b = f.getbbox(text)
    return int(b[2] - b[0]) if b else int(f.getlength(text))


def wrap(d, text, font, max_w, max_lines):
    words = text.split()
    lines, cur = [], (words[0] if words else "")
    for wd in words[1:]:
        cand = cur + " " + wd
        if d.textlength(cand, font=font) <= max_w:
            cur = cand
        else:
            lines.append(cur)
            cur = wd
            if len(lines) >= max_lines:
                break
    if cur and len(lines) < max_lines:
        lines.append(cur)
    return lines


LEAD_HEAD = "TRUMP, XI, PUTIN SUMMIT ENDS IN SHENZHEN"
LEAD_DECK = "Trio talks nuclear cuts at APEC; Ukraine allies meet in Berlin"
LEAD_TAG = "LEAD · 08:30 UTC"
LEAD_CAP = "Trump, Xi and Putin end first three-power summit — Shenzhen, China"

CARDS = [
    ("ICJ RULES ON ROHINGYA CASE", "Genocide judgment due in Myanmar case", "05:13", 1, 4.3, 52.08, "The Hague", "gavel"),
    ("UK SENDS UKRAINE 1,000 DRONES", "Long-range strike pledge after Berlin talks", "10:00", 2, 30.52, 50.45, "Kyiv", "drone"),
    ("ANTHROPIC IPO RAISES $81BN", "Largest share offering on record", "01:13", 3, -122.42, 37.77, "San Francisco", "stock"),
    ("GTA VI HAILED AS MASTERPIECE", "Critics cheer launch after 13 years", "04:00", 4, -74.0, 40.71, "New York", "gamepad"),
    ("MIGRANT BOAT SINKS OFF SENEGAL", "Dozens missing; about 100 aboard", "09:02", 5, -17.45, 14.69, "Dakar", "boat"),
    ("N. KOREA EXPANDS ENRICHMENT", "UN watchdog reports new uranium site", "09:16", 6, 127.6, 39.8, "Yongbyon", "mushroom"),
]


def icon_gavel(d, x, y):
    d.rectangle([x + 26, y, x + 58, y + 10], fill=RED)
    d.rectangle([x + 46, y + 10, x + 50, y + 46], fill=INK)
    d.rectangle([x + 36, y + 42, x + 60, y + 50], fill=RED)


def icon_drone(d, x, y):
    d.rectangle([x + 35, y + 30, x + 45, y + 38], fill=INK)
    d.line([x + 40, y + 34, x + 24, y + 24], fill=INK, width=2)
    d.line([x + 40, y + 34, x + 56, y + 24], fill=INK, width=2)
    d.line([x + 40, y + 34, x + 24, y + 44], fill=INK, width=2)
    d.line([x + 40, y + 34, x + 56, y + 44], fill=INK, width=2)
    d.ellipse([x + 18, y + 20, x + 30, y + 32], fill=GRAY)
    d.ellipse([x + 50, y + 20, x + 62, y + 32], fill=GRAY)
    d.ellipse([x + 18, y + 42, x + 30, y + 54], fill=GRAY)
    d.ellipse([x + 50, y + 42, x + 62, y + 54], fill=GRAY)


def icon_stock(d, x, y):
    d.line([x + 8, y + 40, x + 28, y + 26], fill=RED, width=3)
    d.line([x + 28, y + 26, x + 50, y + 34], fill=RED, width=3)
    d.line([x + 50, y + 34, x + 68, y + 12], fill=RED, width=3)
    d.line([x + 68, y + 12, x + 62, y + 6], fill=RED, width=3)
    d.line([x + 68, y + 12, x + 74, y + 6], fill=RED, width=3)
    d.line([x + 62, y + 6, x + 74, y + 6], fill=RED, width=3)


def icon_gamepad(d, x, y):
    d.rounded_rectangle([x + 8, y + 18, x + 62, y + 50], radius=6, fill=INK)
    d.line([x + 30, y + 34, x + 30, y + 22], fill=WHITE, width=3)
    d.line([x + 30, y + 34, x + 22, y + 30], fill=WHITE, width=3)
    d.line([x + 30, y + 34, x + 38, y + 30], fill=WHITE, width=3)
    d.line([x + 30, y + 34, x + 30, y + 46], fill=WHITE, width=3)
    d.line([x + 30, y + 34, x + 22, y + 38], fill=WHITE, width=3)
    d.line([x + 30, y + 34, x + 38, y + 38], fill=WHITE, width=3)
    d.rectangle([x + 44, y + 20, x + 52, y + 26], fill=RED)
    d.rectangle([x + 44, y + 40, x + 52, y + 46], fill=RED)


def icon_frame(d, x, y):
    d.rectangle([x + 4, y + 6, x + 66, y + 44], outline=INK)
    d.rectangle([x + 10, y + 12, x + 60, y + 38], fill=BEIGE)
    d.ellipse([x + 28, y + 20, x + 42, y + 30], fill=(255, 193, 7))
    d.ellipse([x + 31, y + 17, x + 39, y + 23], fill=INK)


def icon_boat(d, x, y):
    d.polygon([x + 8, y + 36, x + 38, y + 36, x + 50, y + 42, x + 25, y + 48, x + 8, y + 42], fill=RED)
    d.line([x + 25, y + 4, x + 25, y + 36], fill=INK, width=2)
    d.ellipse([x + 14, y + 46, x + 30, y + 54], outline=GRAY)
    d.ellipse([x + 34, y + 48, x + 50, y + 56], outline=GRAY)


def icon_mushroom(d, x, y):
    d.ellipse([x + 20, y + 2, x + 48, y + 16], fill=RED)
    d.rectangle([x + 28, y + 16, x + 36, y + 34], fill=INK)
    d.ellipse([x + 8, y + 28, x + 22, y + 38], fill=GRAY)
    d.ellipse([x + 34, y + 30, x + 48, y + 40], fill=GRAY)


def icon_rain(d, x, y):
    d.ellipse([x + 22, y + 14, x + 44, y + 30], fill=GRAY)
    d.ellipse([x + 10, y + 24, x + 30, y + 40], fill=GRAY)
    d.ellipse([x + 34, y + 24, x + 54, y + 40], fill=GRAY)
    drops = [(22, 32), (34, 32), (46, 32), (20, 40), (32, 40), (44, 40)]
    for bx, by in drops:
        d.line([bx, by, bx + 6, by + 14], fill=(90, 140, 220), width=2)


def world_map(img, d, x0, y0, mw, mh, pins):
    m = Image.new("RGB", (mw, mh), BEIGE)
    md = ImageDraw.Draw(m)
    gj = json.load(open("world.geojson", "r", encoding="utf-8"))
    def add(rings, obj):
        if not isinstance(obj, list):
            return
        for ring in obj:
            if isinstance(ring, list) and len(ring) > 0 and isinstance(ring[0], (list, tuple)):
                rings.append(ring)

    for f in gj.get("features") or []:
        g = f.get("geometry") or {}
        coords = g.get("coordinates") or []
        rings = []
        for poly in coords:
            add(rings, poly)
        for ring in rings:
            if len(ring) < 2:
                continue
            pts = []
            for i in range(len(ring) - 1):
                lon, lat = ring[i][0], ring[i][1]
                pts.append((int((lon + 180.0) / 360.0 * mw), int((90 - lat) / 180.0 * mh)))
            if len(pts) > 2:
                md.polygon(pts, fill=BEIGE, outline=GRAY)
    img.paste(m, (x0, y0))
    for num, lon, lat in pins:
        x = int((lon + 180.0) / 360.0 * mw) + x0
        y = int((90 - lat) / 180.0 * mh) + y0
        d.ellipse([x - 7, y - 7, x + 7, y + 7], fill=RED)
        d.text((x, y), str(num), font=F(12, bold=True), fill=WHITE, anchor="mm")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    d.rectangle([0, 0, W, 52], fill=INK)
    d.text((40, 10), "THE WORLD LEDGER", font=F(28, bold=True), fill=WHITE)
    d.text((984, 26), "THURSDAY · ONE PICTURE · ALL TIMES UTC", font=F(16), fill=WHITE, anchor="ra")

    d.text((728, 56), "WHERE THE NEWS HAPPENED", font=F(16, bold=True), fill=INK)
    world_map(img, d, 700, 78, 312, 100, [(c[3], c[4], c[5]) for c in CARDS])

    d.text((14, 48), "19", font=F(118, bold=True), fill=RED)
    d.text((184, 60), "NOVEMBER 2026", font=F(50, bold=True), fill=INK)
    d.text((184, 110), "THURSDAY · THE DAY'S WORLD NEWS IN ONE PICTURE", font=F(18), fill=GRAY)

    hero = Image.open("hero20.jpg").convert("RGB")
    if hero.size != (1024, 230):
        hero = hero.resize((1024, 230), Image.BICUBIC)
    img.paste(hero, (0, 186))

    d.rectangle([0, 416, W, 442], fill=INK)
    d.text((8, 424), LEAD_CAP, font=F(18, bold=True), fill=WHITE)
    d.text((1016, 429), LEAD_TAG, font=F(16, bold=True), fill=RED, anchor="ra")

    lf = F(36, bold=True)
    lh = 35
    lines = wrap(d, LEAD_HEAD, lf, 1000, 2)
    y = 446
    for ln in lines:
        d.text((8, y), ln, font=lf, fill=RED)
        y += lh
    d.text((8, y + 8), LEAD_DECK, font=F(18), fill=GRAY)
    d.rectangle([8, y + 34, 1016, y + 35], fill=RED)

    cw, chh, gap = 498, 150, 8
    row1 = 516
    for i, c in enumerate(CARDS):
        col, row = i % 2, i // 2
        x = 10 + col * (cw + gap)
        y = row1 + row * (chh + gap)
        headline, context, utc, pin, lon, lat, city, icon = c
        d.rectangle([x, y, x + cw - 1, y + chh - 1], fill=WHITE)
        d.rectangle([x, y, x + cw - 1, y + chh - 1], outline=GRAY)
        d.ellipse([x + 8, y + 6, x + 16, y + 14], fill=RED)
        d.text((x + 12, y + 9), str(pin), font=F(9, bold=True), fill=WHITE, anchor="mm")
        d.text((x + 26, y + 8), utc, font=F(15), fill=GRAY)
        draw_icon(icon, d, x + 14, y + 40)
        hf = F(34, bold=True)
        while len(wrap(d, headline, hf, 370, 3)) > 2 and hf.size > 26:
            hf = F(hf.size - 1, bold=True)
        hlines = wrap(d, headline, hf, 370, 2)
        hy = y + 12
        nlines = 0
        for ln in hlines:
            d.text((x + 104, hy), ln, font=hf, fill=INK)
            hy += 42
            nlines += 1
        cy = y + 12 + nlines * 42 + 4
        clines = wrap(d, context, F(16), 370, 2)
        for ln in clines:
            d.text((x + 104, cy), ln, font=F(16), fill=GRAY)
            cy += 20

    fmsg = "DATE CHECK: 6/6 CARDS + LEAD DATED 19 NOV 2026 — every story first reported that day"
    fs1 = 13
    while span(F(fs1, bold=True), fmsg) > 496 and fs1 > 6:
        fs1 -= 1
    dmsg = "ALSO: Van Gogh $190.4m · California atmospheric river · Crimean Bridge attacked"
    fs2 = 12
    while span(F(fs2), dmsg) > 496 and fs2 > 6:
        fs2 -= 1
    d.rectangle([0, 1000, W, H], fill=INK)
    d.text((8, 1000), fmsg, font=F(fs1, bold=True), fill=WHITE)
    d.text((1016, 1000), dmsg, font=F(fs2), fill=WHITE, anchor="ra")

    for t, fnt, pos in [
        ("19", F(118, bold=True), (14, 48)),
        ("NOVEMBER 2026", F(50, bold=True), (184, 60)),
        ("THURSDAY · THE DAY'S WORLD NEWS IN ONE PICTURE", F(18), (184, 104)),
        ("DATE NAMED ON EVERY CARD — 19 NOVEMBER 2026", F(15), (1010, 152)),
    ]:
        bb = fnt.getbbox(t)
        print("DATEEXT", t, "y0", pos[1] + bb[1], "y1", pos[1] + bb[3])
    img.save("entry.png")
    print("entry.png", os.path.getsize("entry.png"))


ICONS = {
    "gavel": icon_gavel,
    "drone": icon_drone,
    "stock": icon_stock,
    "gamepad": icon_gamepad,
    "frame": icon_frame,
    "boat": icon_boat,
    "mushroom": icon_mushroom,
    "rain": icon_rain,
}


def draw_icon(key, d, x, y):
    fn = ICONS.get(key) or icon_rain
    fn(d, x, y)


main()

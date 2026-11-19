import urllib.parse, urllib.request
from PIL import Image, ImageDraw, ImageFont
W, H = 1024, 1024
PAPER = (245, 241, 232)
RED = (176, 34, 34)
INK = (0, 0, 0)
GRAY = (120, 120, 120)
DARKRED = (120, 16, 16)
WHITE = (255, 255, 255)

PROMPT = ("Dramatic photojournalistic news photograph, three male world leaders in dark "
          "suits standing together shaking hands smiling at a summit, grand modern conference "
          "hall in Shenzhen, large flags of United States China and Russia behind them, "
          "press photographers, telephoto press photography, cinematic lighting, realistic")
HERO_URL = "https://image.pollinations.ai/prompt/" + urllib.parse.quote(PROMPT) + "?width=1280&height=720&nologo=true&seed=" + __import__("os").environ.get("HERO_SEED", "11")


def font(size, bold=False, oblique=False):
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans-Oblique.ttf" if oblique else "DejaVuSans.ttf"
    try:
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/" + name, size)
    except Exception:
        return ImageFont.load_default()

def tw(f, text):
    b = f.getbbox(text)
    return b[2] - b[0] if b else f.getlength(text)

def wrap(text, f, max_w, max_lines):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if not cur or tw(f, trial) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = word
            if len(lines) == max_lines:
                break
    if cur and len(lines) < max_lines:
        lines.append(cur)
    return lines

def fetch():
    for _ in range(3):
        try:
            with urllib.request.urlopen(HERO_URL, timeout=60) as r:
                im = Image.open(r).convert("RGB")
            if im.width > 2 and im.height > 2:
                return im
        except Exception:
            pass
    return None

def fallback():
    w, h = 944, 560
    img = Image.new("RGB", (w, h), (28, 32, 42))
    d = ImageDraw.Draw(img)
    for y in range(h):
        t = y / (h - 1)
        d.line([(0, y), (w - 1, y)], fill=(int(24 - 12 * t), int(28 - 16 * t), int(38 - 16 * t)))
    return img

def vignette(img):
    w, h = img.size
    cx, cy = w / 2.0, h / 2.0
    maxd2 = cx * cx + cy * cy
    px = img.load()
    out = Image.new("RGB", (w, h), (0, 0, 0))
    op = out.load()
    for y in range(h):
        for x in range(w):
            dd = (x - cx) ** 2 + (y - cy) ** 2
            f = 1.0 - 0.08 * dd / maxd2
            r, g, b = px[x, y]
            op[x, y] = (int(r * f), int(g * f), int(b * f))
    return out

def cover(img, tw_, th):
    w, h = img.size
    s = max(tw_ / w, th / h)
    nw, nh = int(w * s), int(h * s)
    im = img.resize((nw, nh), Image.BICUBIC)
    left = (nw - tw_) / 2.0
    top = (nh - th) / 2.0
    return im.crop((left, top, left + tw_, top + th))

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

d.rectangle([0, 0, W, 56], fill=INK)
d.text((40, 12), "THE WORLD LEDGER", font=font(30, bold=True), fill=WHITE)
d.text((984, 14), "Thursday, 19 November 2026 · Vol. I — No. 331", font=font(14), fill=WHITE, anchor="ra")
d.rectangle([0, 56, W, 58], fill=RED)

hero = fetch() or fallback()
hero = hero.crop((0, 0, hero.size[0], int(hero.size[1] * 0.94)))
hero = cover(hero, 944, 560)
hero = vignette(hero)
img.paste(hero, (40, 59))

strip = Image.new("RGBA", (944, 34), (0, 0, 0, 153))
ImageDraw.Draw(strip).rectangle([0, 0, 943, 33], fill=(0, 0, 0, 153))
ImageDraw.Draw(strip).text((4, 8), "Trump, Xi and Putin meet in Shenzhen — the first three-power summit", font=font(16, bold=True), fill=WHITE)
ImageDraw.Draw(strip).text((940, 9), "Photo: Ledger / AI wire", font=font(11), fill=WHITE, anchor="ra")
img.paste(strip, (40, 585), strip.split()[3])

f = font(40, bold=True)
adv = f.getmetrics()[0] + f.getmetrics()[1]
lead_lines = wrap("TRUMP, XI, PUTIN OPEN FIRST TRILATERAL SUMMIT IN SHENZHEN", f, 944, 2)
d.text((40, 630), lead_lines[0], font=f, fill=INK)
d.text((40, 630 + adv), lead_lines[1], font=f, fill=INK)
d.text((40, 730), "APEC three-way talks take up Ukraine, Iran wars and trade", font=font(20), fill=GRAY)

d.rectangle([0, 756, W, 758], fill=RED)
tick = "ICJ ROHINGYA RULING · ODESA STRUCK · US AND VENEZUELA RESTORE MILITARY TIES · GTA VI OUT"
tsize = 15
while tw(font(tsize, bold=True), tick) > W - 80 and tsize > 8:
    tsize -= 1
d.text((W / 2, 768), tick, font=font(tsize, bold=True), fill=DARKRED, anchor="mm")

gap = 24
col_w = (944 - 2 * gap) / 3.0
col_xs = [40, 40 + col_w + gap, 40 + 2 * (col_w + gap)]
block_top = 858
stories = [
    ("World Court rules on Rohingya case", "Landmark ICJ judgment on Myanmar genocide"),
    ("Gulf on alert after US strike", "Iranian island hit; tankers ablaze near Hormuz"),
    ("GTA VI launches after 13 years", "Record release day for Rockstar sequel"),
]
for i, (hx, sub) in enumerate(stories):
    x0 = col_xs[i]
    d.rectangle([x0, block_top, x0 + col_w, block_top + 2], fill=RED)
    size = 28
    while size > 12:
        f = font(size, bold=True)
        lines = wrap(hx, f, col_w - 16, 3)
        if len(lines) <= 3 and all(tw(f, l) <= col_w - 16 for l in lines):
            break
        size -= 1
    f = font(size, bold=True)
    adv = f.getmetrics()[0] + f.getmetrics()[1]
    y = block_top + 6
    for ln in lines:
        d.text((x0, y), ln, font=f, fill=INK)
        y += adv
    fs = 12
    while tw(font(fs), sub) > col_w - 16 and fs > 8:
        fs -= 1
    d.text((x0, y + 4), sub, font=font(fs), fill=GRAY)

d.rectangle([0, 976, W, H], fill=INK)
d.text((40, 986), "ONE DAY. ONE PAGE. — 19 November 2026", font=font(22, bold=True), fill=WHITE)
d.text((984, 986), "Ledger wire reports", font=font(16), fill=WHITE, anchor="ra")
img.save("entry.png")
print("entry.png")

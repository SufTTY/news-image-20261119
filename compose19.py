import os
import urllib.parse
import urllib.request
from PIL import Image, ImageDraw, ImageFont

PAGE_W = 1024
PAGE_H = 1024
PAPER = (245, 241, 232)
RED = (176, 34, 34)
DARK_RED = (120, 16, 16)
INK = (0, 0, 0)
GRAY = (120, 120, 120)
WHITE = (255, 255, 255)

HEADLINE = "TRUMP, XI, PUTIN OPEN FIRST TRILATERAL SUMMIT IN SHENZHEN"
DECK = "APEC three-way talks take up Ukraine, Iran wars and trade"
TICKER = "ICJ ROHINGYA RULING · ODESA STRUCK · US AND VENEZUELA RESTORE MILITARY TIES · GTA VI OUT"
TAGLINE = "ONE DAY. ONE PAGE. — 19 November 2026"

HERO_PROMPT = ("Dramatic photojournalistic news photograph, three male world leaders in dark "
               "suits standing together shaking hands smiling at a summit, grand modern conference "
               "hall in Shenzhen, large flags of United States China and Russia behind them, "
               "press photographers, telephoto press photography, cinematic lighting, realistic")
HERO_URL = "https://image.pollinations.ai/prompt/" + urllib.parse.quote(HERO_PROMPT) + "?width=1280&height=720&nologo=true&seed=" + os.environ.get("HERO_SEED", "11")


def font(size, bold=False):
    family = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    path = "/usr/share/fonts/truetype/dejavu/" + family
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


def text_span(f, text):
    box = f.getbbox(text)
    return box[2] - box[0] if box else f.getlength(text)


def flow(f, text, limit, max_lines):
    words = text.split()
    lines = []
    current = ""
    for word in words:
        trial = (current + " " + word).strip()
        if not current or text_span(f, trial) <= limit:
            current = trial
        else:
            lines.append(current)
            current = word
            if len(lines) == max_lines:
                break
    if current and len(lines) < max_lines:
        lines.append(current)
    return lines


def grab_hero():
    for _ in range(3):
        try:
            with urllib.request.urlopen(HERO_URL, timeout=60) as response:
                picture = Image.open(response).convert("RGB")
            if picture.width > 2 and picture.height > 2:
                return picture
        except Exception:
            pass
    return None


def soften(image, strength=0.08):
    w, h = image.size
    cx, cy = w / 2.0, h / 2.0
    centre_sq = cx * cx + cy * cy
    src = image.load()
    dst = Image.new("RGB", (w, h), (0, 0, 0))
    dst_px = dst.load()
    for y in range(h):
        for x in range(w):
            d = (x - cx) ** 2 + (y - cy) ** 2
            f = 1.0 - strength * d / centre_sq
            r, g, b = src[x, y]
            dst_px[x, y] = (int(r * f), int(g * f), int(b * f))
    return dst


def fit(image, target_w, target_h):
    w, h = image.size
    s = max(target_w / w, target_h / h)
    nw, nh = int(w * s), int(h * s)
    scaled = image.resize((nw, nh), Image.BICUBIC)
    left = (nw - target_w) / 2.0
    top = (nh - target_h) / 2.0
    return scaled.crop((left, top, left + target_w, top + target_h))


def compose():
    page = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    drawer = ImageDraw.Draw(page)

    drawer.rectangle([0, 0, PAGE_W, 56], fill=INK)
    drawer.text((40, 12), "THE WORLD LEDGER", font=font(30, bold=True), fill=WHITE)
    drawer.text((984, 14), "Thursday, 19 November 2026 · Vol. I — No. 331", font=font(14), fill=WHITE, anchor="ra")
    drawer.rectangle([0, 56, PAGE_W, 58], fill=RED)

    hero = grab_hero() or Image.new("RGB", (944, 560), (28, 32, 42))
    hero = fit(hero.crop((0, 0, hero.size[0], int(hero.size[1] * 0.94))), 944, 560)
    hero = soften(hero)
    page.paste(hero, (40, 59))

    caption = Image.new("RGBA", (944, 34), (0, 0, 0, 153))
    ImageDraw.Draw(caption).rectangle([0, 0, 943, 33], fill=(0, 0, 0, 153))
    ImageDraw.Draw(caption).text((4, 8), "Trump, Xi and Putin meet in Shenzhen — first three-power summit", font=font(16, bold=True), fill=WHITE)
    ImageDraw.Draw(caption).text((940, 9), "Photo: Ledger / AI wire", font=font(11), fill=WHITE, anchor="ra")
    page.paste(caption, (40, 585), caption.split()[3])

    lead_font = font(40, bold=True)
    lead_step = lead_font.getmetrics()[0] + lead_font.getmetrics()[1]
    lead_lines = flow(lead_font, HEADLINE, 944, 2)
    y = 630
    for ln in lead_lines:
        drawer.text((40, y), ln, font=lead_font, fill=INK)
        y += lead_step
    drawer.text((40, 730), DECK, font=font(20), fill=GRAY)

    drawer.rectangle([0, 756, PAGE_W, 758], fill=RED)

    ticker_size = 15
    ticker_font = font(ticker_size, bold=True)
    while text_span(ticker_font, TICKER) > PAGE_W - 80 and ticker_size > 8:
        ticker_size -= 1
        ticker_font = font(ticker_size, bold=True)
    drawer.text((PAGE_W / 2, 768), TICKER, font=ticker_font, fill=DARK_RED, anchor="mm")

    gap = 24
    col_w = (944 - 2 * gap) / 3.0
    col_xs = [40, 40 + col_w + gap, 40 + 2 * (col_w + gap)]
    top = 858
    stories = [
        ("World Court rules on Rohingya case", "Landmark ICJ judgment on Myanmar genocide"),
        ("Gulf on alert after US strike", "Iranian island hit; tankers ablaze near Hormuz"),
        ("GTA VI launches after 13 years", "Record release day for Rockstar sequel"),
    ]
    for idx, (headline, sub) in enumerate(stories):
        x0 = col_xs[idx]
        drawer.rectangle([x0, top, x0 + col_w, top + 2], fill=RED)
        size = 28
        while size > 12:
            trial_font = font(size, bold=True)
            ls = flow(trial_font, headline, col_w - 16, 3)
            if len(ls) <= 3 and all(text_span(trial_font, ln) <= col_w - 16 for ln in ls):
                break
            size -= 1
        f = font(size, bold=True)
        adv = f.getmetrics()[0] + f.getmetrics()[1]
        y = top + 6
        for ln in flow(f, headline, col_w - 16, 3):
            drawer.text((x0, y), ln, font=f, fill=INK)
            y += adv
        fs = 12
        while text_span(font(fs), sub) > col_w - 16 and fs > 8:
            fs -= 1
        drawer.text((x0, y + 4), sub, font=font(fs), fill=GRAY)

    drawer.rectangle([0, 976, PAGE_W, PAGE_H], fill=INK)
    drawer.text((40, 986), TAGLINE, font=font(22, bold=True), fill=WHITE)
    drawer.text((984, 986), "Ledger wire reports", font=font(16), fill=WHITE, anchor="ra")
    return page


page = compose()
page.save("entry.png")
print("entry.png")

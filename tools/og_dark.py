# Dark Monergism-style og images (1200x630 JPEG) for hand-built root pages.
# v2 (2026-11-19): PICTURE-FIRST — each page gets its own full-bleed classical
# oil painting (AI-generated, no text in the art) under a dark gradient, so the
# card reads as a painting with words on it, like the Monergism reference grid —
# not a dark empty panel with a small faded engraving (v1 mistake, Duc 19/11).
# Text stays PIL + DejaVu (exact Vietnamese, diacritics correct).
# Sig files use the same formula as tools/og_images.py so a future regen skips them:
#   md5("v4|" + path + "|" + title + "|" + desc)[:12]  (title/desc HTML-UNESCAPED)
# NOTE: the sig covers path+title+desc only, NOT the art — after changing art,
# delete the old og/<slug>.jpg first or the script will skip as "unchanged".
# Usage: python3 tools/og_dark.py   (run from repo root)
import hashlib, html, os, re
from PIL import Image, ImageDraw, ImageFont

_OGFD = "/usr/share/fonts/truetype/dejavu/"
_GOLD = (198, 162, 96)      # gold accent
_GOLD_DIM = (188, 176, 152) # muted gold-grey (lighter than v1: reads over paintings)
_CREAM = (242, 236, 220)    # cream title
_BAND = (46, 38, 26)        # bottom band

def _f(n, s):
    return ImageFont.truetype(_OGFD + n, s)

def _wrap(d, t, font, w):
    out, cur = [], ""
    for wd in t.split():
        x = (cur + " " + wd).strip()
        if d.textlength(x, font=font) <= w or not cur:
            cur = x
        else:
            out.append(cur)
            cur = wd
    if cur:
        out.append(cur)
    return out

def _cover(path, w, h):
    """Cover-crop an image to w x h, centred."""
    im = Image.open(path).convert("RGB")
    iw, ih = im.size
    s = max(w / iw, h / ih)
    im = im.resize((int(iw * s + 0.5), int(ih * s + 0.5)))
    x = (im.size[0] - w) // 2
    y = (im.size[1] - h) // 2
    return im.crop((x, y, x + w, y + h))

def _shade(im):
    """Darken the painting so cream/gold text reads: overall dim + a strong
    left-to-right gradient (dark where the text sits, clear where the picture
    shows) + extra darkening at the bottom band."""
    w, h = im.size
    base = Image.blend(im, Image.new("RGB", (w, h), (0, 0, 0)), 0.30)
    mask = Image.new("L", (w, h), 0)
    px = mask.load()
    for x in range(w):
        a = max(0, 205 - int(205 * x / 820)) if x < 820 else 0
        for y in range(h):
            v = a
            if y > 500:
                v = max(v, int(150 * (y - 500) / 130))
            px[x, y] = v
    return Image.composite(Image.new("RGB", (w, h), (0, 0, 0)), base, mask)

# (page path, art file, kicker, og:title, og:description) — titles/descs HTML-UNESCAPED
PAGES = [
    ("bat-dau-tu-dau.html", "tools/og-art-src/og-painting-bat-dau.jpg", "NGƯỜI MỚI BẮT ĐẦU",
     "Bắt đầu từ đâu với Thần học Cải chánh? | Reformed Vietnam",
     "Người mới tìm hiểu thần học Cải chánh bắt đầu từ đâu? Năm Sola, Năm điểm TULIP, lộ trình 10 cuốn sách miễn phí và kế hoạch đọc 30 ngày."),
    ("su-menh-cam-ket.html", "tools/og-art-src/og-painting-su-menh.jpg", "SỨ MỆNH & CAM KẾT",
     "Sứ mệnh & Cam kết | Reformed Vietnam",
     "Sứ mệnh và cam kết của Reformed Vietnam: thư viện Cải Chánh tiếng Việt miễn phí, dự án cá nhân của David — đây là gì, và không phải là gì."),
    ("lo-trinh-nhom.html", "tools/og-art-src/og-painting-lo-trinh-nhom.jpg", "LỘ TRÌNH THEO NHÓM",
     "Lộ trình theo nhóm — 8 nhóm độc giả | Reformed Vietnam",
     "Lộ trình học Kinh Thánh theo 8 nhóm độc giả: trẻ em, thiếu niên, thanh niên, nam giới, phụ nữ, người đi làm, tân tín hữu và cha mẹ. Chủ đề tháng 12/2026 là Giáng Sinh."),
    ("quiz.html", "tools/og-art-src/og-painting-quiz.jpg", "TRẮC NGHIỆM & THẺ GHI NHỚ",
     "Trắc nghiệm & Thẻ ghi nhớ Giáo Lý | Reformed Vietnam",
     "Trắc nghiệm 10 câu Kinh Thánh và thần học Cải Chánh, cùng 19 thẻ ghi nhớ Giáo Lý Vắn Tắt Westminster (Câu 1–19)."),
]

def render(path, art, kicker, title, desc):
    name = re.sub(r"[^a-z0-9]+", "-", path.lower().replace(".html", "")).strip("-")
    out = f"og/{name}.jpg"
    sig = hashlib.md5(f"v4|{path}|{title}|{desc}".encode("utf-8")).hexdigest()[:12]
    sigf = out + ".sig"
    try:
        if os.path.exists(out) and open(sigf).read().strip() == sig:
            print(out, "unchanged, skipped")
            return out
    except OSError:
        pass
    t = re.split(r"\s+[|–]\s+", title)[0].strip()
    im = _shade(_cover(art, 1200, 630))
    d = ImageDraw.Draw(im)
    # thin gold frame
    d.rectangle([24, 24, 1175, 605], outline=_GOLD, width=2)
    # gold bar, left edge (echoes the rust bar on the light og images)
    d.rectangle([0, 0, 10, 630], fill=_GOLD)
    d.text((72, 66), kicker, font=_f("DejaVuSans-Bold.ttf", 26), fill=_GOLD)
    W = 690
    for sz in (72, 62, 54, 46, 40):
        fo = _f("DejaVuSerif-Bold.ttf", sz)
        L = _wrap(d, t, fo, W)
        if len(L) <= (3 if sz > 54 else 4):
            break
    L = L[:4]
    y = 118
    for ln in L:
        d.text((72, y), ln, font=fo, fill=_CREAM)
        y += int(sz * 1.22)
    ds = re.sub(r"\s+", " ", desc).strip()
    if ds and y < 400:
        fs = _f("DejaVuSerif.ttf", 28)
        DL = _wrap(d, ds, fs, W)[:3 if y < 330 else 2]
        if len(DL) and _wrap(d, ds, fs, W)[len(DL):]:
            DL[-1] = DL[-1].rstrip(" ,.;:") + "…"
        y += 18
        for ln in DL:
            d.text((72, y), ln, font=fs, fill=_GOLD_DIM)
            y += 40
    d.rectangle([0, 548, 1200, 630], fill=_BAND)
    d.text((72, 570), "Reformed Vietnam", font=_f("DejaVuSerif-Bold.ttf", 32), fill=_GOLD)
    d.text((1128, 576), "Sách Cải Chánh miễn phí · reformedvietnam.com",
           font=_f("DejaVuSans.ttf", 20), fill=_GOLD_DIM, anchor="ra")
    os.makedirs("og", exist_ok=True)
    im.save(out, "JPEG", quality=82, optimize=True, progressive=True)
    open(sigf, "w").write(sig)
    print(out, "rendered, sig", sig)
    return out

if __name__ == "__main__":
    for p in PAGES:
        render(*p)

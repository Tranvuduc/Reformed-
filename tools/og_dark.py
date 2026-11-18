# Dark Monergism-style og images (1200x630 JPEG) for hand-built root pages.
# Style: dark warm black-green background, gold frame + kicker, cream serif title,
# faded Dore engraving on the right, dark-gold bottom band. Rendered with PIL
# (exact Vietnamese text, DejaVu fonts) — never AI-generated, so diacritics stay correct.
# Sig files use the same formula as tools/og_images.py so a future regen skips them:
#   md5("v4|" + path + "|" + title + "|" + desc)[:12]  (title/desc HTML-UNESCAPED)
# Usage: python3 tools/og_dark.py   (run from repo root)
import hashlib, html, os, re
from PIL import Image, ImageDraw, ImageFont

_OGFD = "/usr/share/fonts/truetype/dejavu/"
_BG = (20, 24, 20)          # near-black green
_GOLD = (198, 162, 96)      # gold accent
_GOLD_DIM = (168, 158, 138) # muted gold-grey
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

def _art():
    if not os.path.exists("img/dore-sermon.jpg"):
        return None
    a = Image.open("img/dore-sermon.jpg").convert("L").resize((420, 560))
    # darken toward the background so it reads as a faint engraving, not a photo
    a = Image.blend(Image.new("L", a.size, 28), a, 0.42).convert("RGB")
    m = Image.new("L", a.size, 255)
    md = ImageDraw.Draw(m)
    for x in range(160):
        md.line([(x, 0), (x, 560)], fill=int(255 * x / 160))
    return (a, m)

# (page path, kicker, og:title, og:description) — titles/descs HTML-UNESCAPED
PAGES = [
    ("bat-dau-tu-dau.html", "NGƯỜI MỚI BẮT ĐẦU",
     "Bắt đầu từ đâu với Thần học Cải chánh? | Reformed Vietnam",
     "Người mới tìm hiểu thần học Cải chánh bắt đầu từ đâu? Năm Sola, Năm điểm TULIP, lộ trình 10 cuốn sách miễn phí và kế hoạch đọc 30 ngày."),
    ("su-menh-cam-ket.html", "SỨ MỆNH & CAM KẾT",
     "Sứ mệnh & Cam kết | Reformed Vietnam",
     "Sứ mệnh và cam kết của Reformed Vietnam: thư viện Cải Chánh tiếng Việt miễn phí, dự án cá nhân của David — đây là gì, và không phải là gì."),
    ("lo-trinh-nhom.html", "LỘ TRÌNH THEO NHÓM",
     "Lộ trình theo nhóm — 8 nhóm độc giả | Reformed Vietnam",
     "Lộ trình học Kinh Thánh theo 8 nhóm độc giả: trẻ em, thiếu niên, thanh niên, nam giới, phụ nữ, người đi làm, tân tín hữu và cha mẹ. Chủ đề tháng 12/2026 là Giáng Sinh."),
    ("quiz.html", "TRẮC NGHIỆM & THẺ GHI NHỚ",
     "Trắc nghiệm & Thẻ ghi nhớ Giáo Lý | Reformed Vietnam",
     "Trắc nghiệm 10 câu Kinh Thánh và thần học Cải Chánh, cùng 19 thẻ ghi nhớ Giáo Lý Vắn Tắt Westminster (Câu 1–19)."),
]

def render(path, kicker, title, desc):
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
    im = Image.new("RGB", (1200, 630), _BG)
    a = _art()
    if a:
        im.paste(a[0], (780, 0), a[1])
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

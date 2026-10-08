# Per-page social share images (1200x630 JPEG) rendered with PIL. exec'd by build-pages.py.
import hashlib, os, re
from PIL import Image, ImageDraw, ImageFont
_OGFD = "/usr/share/fonts/truetype/dejavu/"
def _ogf(n, s): return ImageFont.truetype(_OGFD + n, s)
_OGBG = (244, 239, 228); _OGINK = (38, 33, 26); _OGRUST = (154, 52, 18); _OGMUT = (111, 102, 90)
_OGART = None
def _ogart():
    global _OGART
    if _OGART is None and os.path.exists("img/dore-sermon.jpg"):
        a = Image.open("img/dore-sermon.jpg").convert("L").resize((420, 560))
        a = Image.blend(Image.new("L", a.size, 244), a, 0.2).convert("RGB")
        m = Image.new("L", a.size, 255); md = ImageDraw.Draw(m)
        for x in range(160): md.line([(x, 0), (x, 560)], fill=int(255 * x / 160))
        _OGART = (a, m)
    return _OGART
def _ogwrap(d, t, font, w):
    out, cur = [], ""
    for wd in t.split():
        x = (cur + " " + wd).strip()
        if d.textlength(x, font=font) <= w or not cur: cur = x
        else: out.append(cur); cur = wd
    if cur: out.append(cur)
    return out
def _ogkick(path):
    for p, k in (("a/", "TÁC GIẢ"), ("b/", "SÁCH · ĐỌC MIỄN PHÍ"), ("bai-giang", "BÀI GIẢNG"), ("ban-dich", "BẢN DỊCH TIẾNG VIỆT"),
                 ("chu-de", "CHỦ ĐỀ"), ("video", "VIDEO"), ("moi-tin", "NGƯỜI MỚI TIN CHÚA"), ("phuc-am", "TÌM HIỂU")):
        if path.startswith(p): return k
    return "THƯ VIỆN CẢI CHÁNH"
def og_image(path, title, desc=""):
    name = re.sub(r"[^a-z0-9]+", "-", path.lower().replace(".html", "")).strip("-") or "home"
    out = f"og/{name}.jpg"
    # skip regeneration if inputs unchanged (hash of path+title+desc)
    sig = hashlib.md5(f"{path}|{title}|{desc}".encode("utf-8")).hexdigest()[:12]
    sigf = out + ".sig"
    try:
        if os.path.exists(out) and open(sigf).read().strip() == sig:
            return out
    except OSError:
        pass
    _p = [x.strip() for x in re.split(r"\s+[|–]\s+", title)]; t = _p[0]; by = _p[1] if len(_p) > 2 or (len(_p) == 2 and path.startswith("b/")) else ""
    im = Image.new("RGB", (1200, 630), _OGBG); a = _ogart()
    if a and not path.startswith("a/"): im.paste(a[0], (780, 0), a[1])
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 22, 630], fill=_OGRUST)
    d.text((80, 70), _ogkick(path), font=_ogf("DejaVuSans-Bold.ttf", 26), fill=_OGRUST)
    W = 690
    for sz in (74, 64, 56, 48, 42):
        fo = _ogf("DejaVuSerif-Bold.ttf", sz); L = _ogwrap(d, t, fo, W)
        if len(L) <= (3 if sz > 56 else 4): break
    L = L[:4]; y = 125
    for ln in L: d.text((80, y), ln, font=fo, fill=_OGINK); y += int(sz * 1.22)
    if by:
        d.text((80, y + 6), by, font=_ogf("DejaVuSans-Bold.ttf", 30), fill=_OGRUST); y += 56
    ds = re.sub(r"\s+", " ", desc).strip()
    if ds and y < 400:
        fs = _ogf("DejaVuSerif.ttf", 28); DL = _ogwrap(d, ds, fs, W)[:3 if y < 330 else 2]
        if len(DL) and _ogwrap(d, ds, fs, W)[len(DL):]: DL[-1] = DL[-1].rstrip(" ,.;:") + "…"
        y += 18
        for ln in DL: d.text((80, y), ln, font=fs, fill=_OGMUT); y += 40
    d.rectangle([0, 548, 1200, 630], fill=_OGRUST)
    d.text((80, 570), "Reformed Vietnam", font=_ogf("DejaVuSerif-Bold.ttf", 32), fill=(255, 255, 255))
    d.text((1120, 576), "Sách Cải Chánh miễn phí · reformed-vietnam.vercel.app", font=_ogf("DejaVuSans.ttf", 20), fill=(255, 235, 220), anchor="ra")
    os.makedirs("og", exist_ok=True)
    im.save(out, "JPEG", quality=62, optimize=True, progressive=True)
    try:
        open(sigf, "w").write(sig)
    except OSError:
        pass
    return out

#!/usr/bin/env python3
"""Tạo sách nói giọng tự nhiên (Azure Speech) theo từng đoạn của trình đọc.

Có khóa Azure thì dùng Azure; không có khóa thì tự dùng edge-tts (pip install edge-tts).
Chạy trên máy bạn hoặc GitHub Actions (không đưa khóa vào mã):
  export AZURE_SPEECH_KEY=...   AZURE_SPEECH_REGION=southeastasia
  python3 tools/tts_gen.py <slug> [--voice vi-VN-HoaiMyNeural] [--limit N] [--dry-run]

Đầu ra: tts_out/<slug>/<k>.mp3   (k = số thứ tự đoạn, khớp với reader.html)
Sau đó tải thư mục lên nơi lưu trữ (R2, GitHub Pages repo riêng...) và thêm vào tts/index.json:
  {"base": "https://.../", "books": {"<slug>": <số đoạn>}}
Tính lại mỗi đoạn: nếu file đã có thì bỏ qua (chạy lại được).
"""
import os, re, sys, json, time, argparse, urllib.request, urllib.error
from xml.sax.saxutils import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTFMT = "audio-24khz-48kbitrate-mono-mp3"
MAXC = 2800


def paragraphs(text):
    """Giống build() trong reader.html: cùng cách tách đoạn, cùng chỉ số k."""
    t = text.replace("\r", "")
    out = []
    for r in re.split(r"\n[ \t]*\n", t):
        lines = [x.rstrip() for x in r.split("\n")]
        lines = [x for x in lines if x.strip()]
        if not lines:
            continue
        verse = len(lines) >= 3 and all(len(x.strip()) < 52 for x in lines)
        s = "\n".join(x.strip() for x in lines) if verse else re.sub(r"\s{2,}", " ", " ".join(x.strip() for x in lines))
        one = lines[0].strip() if len(lines) == 1 else ""
        heading = bool(one) and len(one) <= 80 and re.search(r"[A-Z]{3}", one) and one == one.upper()
        if not heading and len(s) < 2:
            continue
        out.append(s)
    return out


def pron_table():
    src = open(os.path.join(ROOT, "reader.html"), encoding="utf-8").read()
    m = re.search(r"^var PRON=(\[.*?\]);?\s*$", src, re.M)
    pairs = re.findall(r'\["([^"]+)","([^"]+)"\]', m.group(1)) if m else []
    return pairs


def speakable(s, pairs):
    for a, b in pairs:
        s = s.replace(a, b)
    s = re.sub(r"\bChrist\b", "Cơ Đốc", s)
    s = re.sub(r"[#*_`]+", "", s)
    return s.strip()


def split(s):
    if len(s) <= MAXC:
        return [s]
    out, buf = [], ""
    for x in re.split(r"(?<=[.!?])\s+", s):
        while len(x) > MAXC:
            k = x.rfind(" ", 0, MAXC)
            out.append(x[:k]); x = x[k + 1:]
        if buf and len(buf) + len(x) + 1 > MAXC:
            out.append(buf); buf = x
        else:
            buf = (buf + " " + x).strip()
    if buf:
        out.append(buf)
    return out


def synth(text, voice, key, region, rate):
    ssml = ('<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="vi-VN">'
            '<voice name="%s"><prosody rate="%s">%s</prosody></voice></speak>') % (voice, rate, escape(text))
    req = urllib.request.Request(
        "https://%s.tts.speech.microsoft.com/cognitiveservices/v1" % region,
        data=ssml.encode("utf-8"),
        headers={"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/ssml+xml",
                 "X-Microsoft-OutputFormat": OUTFMT, "User-Agent": "reformed-vietnam-tts"})
    for a in range(5):
        try:
            return urllib.request.urlopen(req, timeout=60).read()
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503):
                time.sleep(2 ** a * 2); continue
            raise SystemExit("Azure trả lỗi %s: %s" % (e.code, e.read()[:200]))
        except Exception:
            time.sleep(2 ** a)
    raise SystemExit("Azure không phản hồi")


def synth_edge(text, voice, rate):
    """Không cần tài khoản/khóa: dùng giọng Microsoft Edge (cùng giọng thần kinh vi-VN)."""
    import asyncio, tempfile, edge_tts
    r = rate if rate[0] in "+-" else "+" + rate
    async def go():
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as f:
            name = f.name
        await edge_tts.Communicate(text, voice, rate=r).save(name)
        b = open(name, "rb").read(); os.remove(name); return b
    for a in range(4):
        try:
            b = asyncio.run(go())
            if len(b) > 200:
                return b
        except Exception as e:
            err = e
        time.sleep(2 ** a * 2)
    raise SystemExit("Edge TTS lỗi: %s" % err)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    ap.add_argument("--voice", default="vi-VN-HoaiMyNeural")
    ap.add_argument("--rate", default="0%", help="vd -5%% cho chậm hơn")
    ap.add_argument("--limit", type=int, default=0, help="chỉ làm N đoạn đầu (để thử)")
    ap.add_argument("--dry-run", action="store_true", help="chỉ đếm ký tự, không gọi Azure")
    ap.add_argument("--out", default=os.path.join(ROOT, "tts_out"))
    a = ap.parse_args()
    src = os.path.join(ROOT, "txt", a.slug + ".txt")
    if not os.path.exists(src):
        raise SystemExit("Không thấy " + src)
    pairs = pron_table()
    paras = paragraphs(open(src, encoding="utf-8").read())
    if a.limit:
        paras = paras[:a.limit]
    chars = sum(len(speakable(p, pairs)) for p in paras)
    print("%s: %d đoạn, %d ký tự (≈%.1f%% hạn mức 500K/tháng)" % (a.slug, len(paras), chars, chars / 5000))
    if a.dry_run:
        return
    key, region = os.environ.get("AZURE_SPEECH_KEY"), os.environ.get("AZURE_SPEECH_REGION", "southeastasia")
    if not key:
        print("Không có AZURE_SPEECH_KEY → dùng edge-tts (miễn phí, không cần tài khoản)")
    od = os.path.join(a.out, a.slug)
    os.makedirs(od, exist_ok=True)
    for k, p in enumerate(paras):
        fn = os.path.join(od, "%d.mp3" % k)
        if os.path.exists(fn) and os.path.getsize(fn) > 200:
            continue
        txt = speakable(p, pairs)
        if not re.search(r"\w", txt):
            continue
        data = b"".join((synth(c, a.voice, key, region, a.rate) if key else synth_edge(c, a.voice, a.rate)) for c in split(txt))
        open(fn, "wb").write(data)
        if k % 20 == 0:
            print("  %d/%d" % (k, len(paras)), flush=True)
    print("Xong →", od)


if __name__ == "__main__":
    main()

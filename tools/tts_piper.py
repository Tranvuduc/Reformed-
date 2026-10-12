#!/usr/bin/env python3
"""Tạo giọng Piper (mã nguồn mở, chạy trên máy/CI, không cần tài khoản).
Dùng: python3 tools/tts_piper.py <slug> --voice vi_VN-vais1000-medium --limit 3 --out tts/test/<slug>-<voice>"""
import argparse, os, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(__file__))
import tts_gen as g

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug"); ap.add_argument("--voice", required=True)
    ap.add_argument("--limit", type=int, default=0); ap.add_argument("--out", required=True)
    ap.add_argument("--kbps", default="48k")
    a = ap.parse_args()
    pairs = g.pron_table()
    paras = g.paragraphs(open(os.path.join(g.ROOT, "txt", a.slug + ".txt"), encoding="utf-8").read())
    if a.limit: paras = paras[:a.limit]
    os.makedirs(a.out, exist_ok=True)
    for k, p in enumerate(paras):
        fn = os.path.join(a.out, "%d.mp3" % k)
        if os.path.exists(fn) and os.path.getsize(fn) > 200: continue
        txt = g.speakable(p, pairs)
        if not any(c.isalnum() for c in txt): continue
        wav = tempfile.mktemp(suffix=".wav")
        subprocess.run([sys.executable, "-m", "piper", "-m", a.voice, "-f", wav], input=txt.encode(), check=True)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wav, "-ac", "1", "-b:a", a.kbps, fn], check=True)
        os.remove(wav)
    print("Xong →", a.out)

if __name__ == "__main__":
    main()

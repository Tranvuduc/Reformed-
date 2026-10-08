# Executed from build-pages.py (after vi_books). Writes txt/<slug>.txt (plain text) for doc/*.html and ban-dich/*.html so reader.html?id=vn/<slug> can open them.
import os as _o, re as _re
from html.parser import HTMLParser as _HP
class _X(_HP):
    SKIP = {"nav", "script", "style", "footer", "ol", "button"}
    def __init__(s):
        super().__init__(convert_charrefs=True); s.out = []; s.buf = []; s.tag = None; s.inmain = False; s.skip = 0; s.skipcls = 0
    def handle_starttag(s, t, a):
        a = dict(a); c = a.get("class", "") or ""
        if t == "main": s.inmain = True
        if not s.inmain: return
        if t in s.SKIP: s.skip += 1
        if t == "div" and ("acts" in c or "toc" in c or "hero" in c): s.skipcls += 1; return
        if t == "br": s.buf.append(" ")
        if t in ("h1", "h2", "h3", "p", "li", "blockquote"): s.flush(); s.tag = t; s.cls = c
    def handle_endtag(s, t):
        if not s.inmain: return
        if t in s.SKIP and s.skip: s.skip -= 1
        if t == "div" and s.skipcls: s.skipcls -= 1
        if t in ("h1", "h2", "h3", "p", "li", "blockquote"): s.flush()
    def handle_data(s, d):
        if s.inmain and not s.skip and not s.skipcls and s.tag: s.buf.append(d)
    def flush(s):
        t = _re.sub(r"\s+", " ", "".join(s.buf)).strip(); tg = s.tag; s.buf = []; s.tag = None
        if not t: return
        if tg in ("h1", "h2", "h3"):
            if t.lower() in ("mục lục", "tải về", "sách liên quan"): return
            t = t.upper()
            if s.out and t == s.out[0]: return
        elif _re.match(r"^(Tải EPUB|Đọc ngay|Về thư viện)", t): return
        if _re.match(r"^[=_\-]{5,}$", t): return
        s.out.append(t)
_o.makedirs("txt", exist_ok=True)
for _d in ("doc", "ban-dich"):
    for _f in sorted(_o.listdir(_d)):
        if not _f.endswith(".html") or _f == "index.html": continue
        _src = f"{_d}/{_f}"; _dst = f"txt/{_f[:-5]}.txt"
        try:
            if _o.path.exists(_dst) and _o.path.getmtime(_dst) >= _o.path.getmtime(_src):
                continue
        except OSError:
            pass
        _x = _X(); _x.feed(open(_src, encoding="utf-8").read()); _x.flush()
        if len(" ".join(_x.out)) < 800: continue
        open(_dst, "w", encoding="utf-8").write("\n\n".join(_x.out) + "\n")

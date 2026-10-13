# Executed after nang_cap4.py. Full-text search index (s/*.bin + search-meta.json), plus static-JS pages:
# tim-kiem, doc-kinh-thanh, hoc-thuoc-long, gia-dinh-tho-phuong, hoi-thanh-nha, lich-su-hom-nay, so-hoc.
import unicodedata as _ud5, collections as _c5

def _fold5(s):
    s = s.lower().replace("đ", "d")
    return "".join(ch for ch in _ud5.normalize("NFD", s) if _ud5.category(ch) != "Mn")
_tok5 = _r3.compile(r"[^\W_]+")
def _nl5(s): return _ud5.normalize("NFC", s).lower()
def _key5(w): return "-".join(format(ord(c), "x") for c in w[:2])
def _vi5(n):
    o = bytearray()
    while n >= 128: o.append((n & 127) | 128); n >>= 7
    o.append(n); return bytes(o)

# ---- sections ----
_SEC5, _post5, _bi5 = [], _c5.defaultdict(list), _c5.defaultdict(list)
_stems5 = _stems3  # same order as kt tables
for _si, _s in enumerate(_stems5):
    _d = _B3[_s]; _bl = _d["blocks"]; _acc = 0; _st = None; _words = set()
    _rawt = open("txt/" + _s + ".txt", encoding="utf-8").read(); _bp = [0, 0]
    def _b8(off):
        if off < _bp[0]: _bp[0] = 0; _bp[1] = 0
        _bp[1] += len(_rawt[_bp[0]:off].encode("utf-8")); _bp[0] = off; return _bp[1]
    _bg = set()
    def _flush(end):
        global _words, _bg
        sid = len(_SEC5); _SEC5.append([_si, _b8(_st), _b8(end)])
        for w in _words: _post5[w].append(sid)
        for w in _bg: _bi5[w].append(sid)
        _words = set(); _bg = set()
    for _t, _off in _bl:
        if _st is None: _st = _off
        _acc += len(_t); _tk = _tok5.findall(_nl5(_t)); _words.update(w for w in _tk if len(w) >= 2); _bg.update(a + ' ' + b for a, b in zip(_tk, _tk[1:]))
        if _acc >= 6000:
            _flush(_off + len(_t)); _st = None; _acc = 0
    if _st is not None and _words: _flush(_bl[-1][1] + len(_bl[-1][0]))
_N5 = len(_SEC5)
_stop5 = sorted(w for w, p in _post5.items() if len(p) > _N5 * 0.45)
_shards = _c5.defaultdict(bytearray)
for w, pl in _post5.items():
    if len(pl) > _N5 * 0.45: continue
    wb = w.encode(); b = bytearray([len(wb)]) + wb + _vi5(len(pl)); prev = 0
    for x in pl: b += _vi5(x - prev); prev = x
    _shards[_key5(w)] += b
_o3.makedirs("s", exist_ok=True)
for _f in _o3.listdir("s"): _o3.remove("s/" + _f)
for k, v in _shards.items(): open(f"s/{k}.bin", "wb").write(bytes(v))
_o3.makedirs("s2", exist_ok=True)
for _f in _o3.listdir("s2"): _o3.remove("s2/" + _f)
_sh2 = _c5.defaultdict(bytearray)
for w, pl in _bi5.items():
    if len(pl) > _N5 * 0.08 or len(pl) < 2: continue
    wb = w.encode(); b = bytearray([len(wb)]) + wb + _vi5(len(pl)); prev = 0
    for x in pl: b += _vi5(x - prev); prev = x
    _sh2[_key5(w)] += b
for k, v in _sh2.items(): open(f"s2/{k}.bin", "wb").write(bytes(v))
open("search-meta.json", "w", encoding="utf-8").write(_j3.dumps({"b": _tbl3, "s": _SEC5, "stop": _stop5}, ensure_ascii=False, separators=(",", ":")))
_b = _NC3 + '''<h1>Tìm trong toàn văn các sách</h1>
<p>Gõ một cụm từ tiếng Việt (có hoặc không dấu) để tìm trong tất cả các bản dịch của thư viện. Kết quả hiện đoạn văn và mở đúng chỗ trong trình đọc.</p>
<form id="f" class="sel"><input id="q" type="search" placeholder="Ví dụ: xưng công bình, sự tái sinh, giết chết tội lỗi" autocomplete="off" style="flex:1"><button class="btn" type="submit">Tìm</button></form>
<p class="m" id="st" role="status"></p><ol class="rs" id="rs" style="padding-left:1.2em"></ol>
<p class="m">Tìm trong các đoạn lớn khoảng 6.000 chữ. Từ quá phổ biến (như “và”, “của”) được bỏ qua. Bản dịch do AI hỗ trợ, chưa được mục sư duyệt.</p>
<script src="/tim-kiem.js" defer></script>'''
open("tim-kiem.html", "w", encoding="utf-8").write(page("Tìm trong toàn văn các sách | Reformed Vietnam", "Tìm một cụm từ trong tất cả các bản dịch tiếng Việt của thư viện Cải Chánh và mở đúng đoạn trong trình đọc.", "tim-kiem.html", _b)); urls.append("tim-kiem.html")
print("bigram shards:", len(_sh2), sum(len(v) for v in _sh2.values()) // 1024, "KB"); print("search index:", _N5, "sections,", len(_shards), "shards,", sum(len(v) for v in _shards.values()) // 1024, "KB,", len(_stop5), "stopwords")

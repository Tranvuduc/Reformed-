# Executed from build-pages.py (uses: page, E, bcard, bkgrid, urls).
# Builds kinh-thanh-index.html — browse translated books by Bible passage (Monergism-style Scripture index).
import json as _js, os as _os, re as _re, unicodedata as _ud


def _sl(s):
    s = _ud.normalize("NFKD", s.replace("đ", "d").replace("Đ", "D"))
    s = "".join(c for c in s if not _ud.combining(c)).lower()
    return _re.sub(r"[^a-z0-9]+", "-", s).strip("-")[:70]

_SI = _js.load(open("tools/scripture-index.json", encoding="utf-8"))
_TI = {x["id"]: x for x in _js.load(open("translations/index.json", encoding="utf-8"))}

# 66 books of the Bible, Vietnamese (1934) names, canonical order
BIBLE_BOOKS = [
    ("Sáng Thế Ký", "ot"), ("Xuất Ê-díp-tô Ký", "ot"), ("Lê-vi Ký", "ot"), ("Dân Số Ký", "ot"),
    ("Phục Truyền Luật Lệ Ký", "ot"), ("Giô-suê", "ot"), ("Các Quan Xét", "ot"), ("Ru-tơ", "ot"),
    ("1 Sa-mu-ên", "ot"), ("2 Sa-mu-ên", "ot"), ("1 Các Vua", "ot"), ("2 Các Vua", "ot"),
    ("1 Sử Ký", "ot"), ("2 Sử Ký", "ot"), ("E-xơ-ra", "ot"), ("Nê-hê-mi", "ot"), ("Ê-xơ-tê", "ot"),
    ("Gióp", "ot"), ("Thi Thiên", "ot"), ("Châm Ngôn", "ot"), ("Truyền Đạo", "ot"), ("Nhã Ca", "ot"),
    ("Ê-sai", "ot"), ("Giê-rê-mi", "ot"), ("Ca Thương", "ot"), ("Ê-xê-chi-ên", "ot"), ("Đa-ni-ên", "ot"),
    ("Ô-sê", "ot"), ("Giô-ên", "ot"), ("A-mốt", "ot"), ("Áp-đia", "ot"), ("Giô-na", "ot"),
    ("Mi-chê", "ot"), ("Na-hum", "ot"), ("Ha-ba-cúc", "ot"), ("Sô-phô-ni", "ot"), ("A-ghê", "ot"),
    ("Xa-cha-ri", "ot"), ("Ma-la-chi", "ot"),
    ("Ma-thi-ơ", "nt"), ("Mác", "nt"), ("Lu-ca", "nt"), ("Giăng", "nt"), ("Công vụ", "nt"),
    ("Rô-ma", "nt"), ("1 Cô-rinh-tô", "nt"), ("2 Cô-rinh-tô", "nt"), ("Ga-la-ti", "nt"),
    ("Ê-phê-sô", "nt"), ("Phi-líp", "nt"), ("Cô-lô-se", "nt"),
    ("1 Tê-sa-lô-ni-ca", "nt"), ("2 Tê-sa-lô-ni-ca", "nt"),
    ("1 Ti-mô-thê", "nt"), ("2 Ti-mô-thê", "nt"), ("Tít", "nt"), ("Phi-lê-môn", "nt"),
    ("Hê-bơ-rơ", "nt"), ("Gia-cơ", "nt"), ("1 Phi-e-rơ", "nt"), ("2 Phi-e-rơ", "nt"),
    ("1 Giăng", "nt"), ("2 Giăng", "nt"), ("3 Giăng", "nt"), ("Giu-đe", "nt"), ("Khải Huyền", "nt"),
]
_BB = {n for n, _ in BIBLE_BOOKS}


def _ref_book(ref):
    m = _re.match(r"^(.+?)\s+\d+", ref.strip())
    return m.group(1) if m else ref.strip()


def _ref_key(ref):
    m = _re.match(r"^(.+?)\s+(\d+)(?::(\d+))?", ref.strip())
    if not m:
        return (0, 0)
    return (int(m.group(2)), int(m.group(3) or 0))


# reverse index: bible book -> ref -> [translation entries]; validate ids + files
_by_book, _skipped = {}, []
for _b in _SI["books"]:
    _e = _TI.get(_b["id"])
    if not _e or not _os.path.exists("translations/" + _e.get("file", "")):
        _skipped.append(_b["id"])
        continue
    for _ref in _b["refs"]:
        _bk = _ref_book(_ref)
        if _bk not in _BB:
            _skipped.append(f"{_b['id']}:{_ref}")
            continue
        _by_book.setdefault(_bk, {}).setdefault(_ref, []).append(_e)
if _skipped:
    print("scripture-index skipped:", _skipped)

_n_mapped = sum(len(v) for refs in _by_book.values() for v in refs.values())
_n_books = len(_by_book)

_CSS = ("<style>.sc-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:8px;margin:10px 0}"
        ".sc{display:block;border:1px solid var(--line);border-radius:10px;padding:8px 10px;text-decoration:none;background:var(--card)}"
        ".sc b{display:block;font-size:.92rem}.sc span{font:12px system-ui,sans-serif;color:var(--mut)}"
        ".sc.dis{opacity:.42}.sc:hover{border-color:var(--acc)}"
        ".sc-sel{width:100%;padding:10px 14px;border:1px solid var(--line);border-radius:999px;background:var(--card);color:var(--fg);font:15px system-ui,sans-serif;margin:8px 0}"
        ".sc-ref{margin:1.2em 0 .4em;font-size:1.05rem}</style>")
_JS = ("<script>(function(){var s=document.getElementById('scjump');if(!s)return;"
       "s.addEventListener('change',function(){if(s.value)location.hash=s.value})})()</script>")


def _cell(name):
    c = sum(len(v) for v in _by_book.get(name, {}).values())
    cls = "" if c else " dis"
    href = f"#s-{_sl(name)}" if c else "#s-top"
    return f'<a class="sc{cls}" href="{href}"><b>{E(name)}</b><span>{c} sách</span></a>'


def _grid(test):
    return '<div class="sc-grid">' + "".join(_cell(n) for n, t in BIBLE_BOOKS if t == test) + "</div>"


_opts = "".join(
    f'<option value="s-{_sl(n)}"{"" if sum(len(v) for v in _by_book.get(n, {}).values()) else " disabled"}>'
    f"{E(n)} ({sum(len(v) for v in _by_book.get(n, {}).values())})</option>"
    for n, _ in BIBLE_BOOKS)

_secs = []
for _n, _t in BIBLE_BOOKS:
    _refs = _by_book.get(_n)
    if not _refs:
        continue
    _h = ""
    for _ref in sorted(_refs, key=_ref_key):
        _cards = "".join(
            bcard(_e["title"], _e["author"],
                  f"/ban-dich/{_os.path.splitext(_e['file'])[0]}.html",
                  kicker="Bản dịch", badge="AI, chưa duyệt")
            for _e in _refs[_ref])
        _h += f'<h3 class="sc-ref">{E(_ref)}</h3><div class="bk-grid">{_cards}</div>'
    _secs.append(f'<h2 id="s-{_sl(_n)}">{E(_n)}</h2>{_h}')

_body = (_CSS +
         '<p class="m"><a href="/">← Thư viện</a> · <a href="/chu-de/kinh-thanh.html">Chủ đề Kinh Thánh</a></p>\n'
         f'<h1 id="s-top">Tìm sách theo phân đoạn Kinh Thánh</h1>\n'
         f'<p>Chọn một sách trong Kinh Thánh để xem các tác phẩm Cải Chánh giảng giải phân đoạn đó. '
         f'Hiện có <b>{_n_mapped} lượt gắn</b> trên <b>{_n_books}/66</b> sách Kinh Thánh — danh sách do biên tập viên chọn tay và đang bổ sung dần.</p>\n'
         f'<select id="scjump" class="sc-sel" aria-label="Chọn sách Kinh Thánh"><option value="">— Chọn nhanh một sách Kinh Thánh —</option>{_opts}</select>\n'
         '<h2>Cựu Ước</h2>\n' + _grid("ot") +
         '<h2>Tân Ước</h2>\n' + _grid("nt") +
         '<hr>' + "\n".join(_secs) + _JS)

open("kinh-thanh-index.html", "w", encoding="utf-8").write(page(
    "Tìm sách theo phân đoạn Kinh Thánh | Reformed Vietnam",
    "Tìm sách Cải Chánh theo phân đoạn Kinh Thánh: chọn một sách trong 66 sách Kinh Thánh để xem các tác phẩm giảng giải phân đoạn đó, đọc miễn phí tiếng Việt.",
    "kinh-thanh-index.html", _body))
urls.append("kinh-thanh-index.html")
print(f"scripture-index: {_n_mapped} mappings across {_n_books} bible books")

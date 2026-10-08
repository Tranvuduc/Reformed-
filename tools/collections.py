# Executed from build-pages.py AFTER vi_books.py (uses: page, E, urls, bcard, bcolor, SITE).
# Builds suu-tap/ curated collection hub pages. Draft: AI-assisted, not pastor-reviewed.
import json as _j, os as _o
_o.makedirs("suu-tap", exist_ok=True)
_books = _j.load(open("books.json", encoding="utf-8"))
_vib = _j.load(open("vi-books.json", encoding="utf-8"))
_T = {}
for _a in _books["authors"]:
    for _b in _a["books"]:
        _T[_a["id"] + "/" + _b[0]] = (_a["name"], _b[1])
_vi_t = _books.get("vi", {})
_vn_titles = {}
for _e in _j.load(open("translations/index.json", encoding="utf-8")):
    if not _e.get("hold"):
        _vn_titles[_e["id"]] = _e.get("title", "")
def _centry(bid):
    if bid not in _T: return None
    au, en = _T[bid]
    v = _vib.get(bid)
    if v:
        return (_vn_titles.get(bid) or _vi_t.get(bid) or en, au, v["u"], "Bản dịch tiếng Việt")
    return (_vi_t.get(bid) or en, au, f"/reader.html?id={bid}", "Đọc trong thư viện")
_COLS = [
 ("nguoi-moi", "Sách cho người mới tin Chúa",
  "Bắt đầu từ Phúc Âm: những cuốn sách ngắn gọn, rõ ràng và đầy an ủi cho người mới tin Chúa hoặc mới tìm hiểu đức tin Cơ Đốc. Ưu tiên bản dịch tiếng Việt.",
  ["spurgeon/grace", "bonar/peace", "ryle/holiness", "bunyan/pilgrim", "flavel/lovely", "baxter/saints_rest", "boston/crook", "watson/beatitudes", "ryle/matthew"]),
 ("kinh-dien", "Kinh điển Cải Chánh nên đọc",
  "Những tác phẩm nền tảng đã định hình thần học Cải Chánh qua các thế kỷ — từ Calvin, Owen đến Edwards và Spurgeon.",
  ["calvin/institutes", "owen/mort", "edwards/affections", "edwards/will", "bunyan/pilgrim", "baxter/saints_rest", "spurgeon/grace", "owen/just", "owen/communion", "flavel/lovely"]),
 ("cau-nguyen", "Sách cầu nguyện & đời sống thuộc linh",
  "Học cầu nguyện và lớn lên trong đời sống với Chúa qua các tác phẩm linh tu kinh điển của Knox, Calvin, Watson và Ryle.",
  ["knox/prayer", "calvin/prayer", "watson/prayer", "ryle/holiness", "owen/mort", "boston/crook", "owen/glory", "edwards/sermons"]),
 ("than-hoc", "Thần học hệ thống nhập môn",
  "Muốn hiểu thần học Cải Chánh một cách có hệ thống? Bắt đầu với những bộ giáo trình kinh điển này — đọc từng phần, không cần hết cuốn.",
  ["berkhof/systematictheology", "hodge/theology1", "bavinck/revelation", "calvin/institutes", "owen/just", "edwards/affections", "charnock/cleansing", "baxter/pastor"]),
]
for _slug, _name, _intro, _ids in _COLS:
    _cards = []
    for _bid in _ids:
        _ce = _centry(_bid)
        if not _ce: continue
        _t, _a, _u, _k = _ce
        _cards.append(bcard(_t, _a, _u, kicker=_k))
    _body = (f'<p class="m"><a href="/suu-tap/">← Tất cả bộ sưu tập</a> · <a href="/">Thư viện</a></p>'
             f'<h1>{E(_name)}</h1><p>{E(_intro)}</p>'
             '<div class="bk-grid">' + "".join(_cards) + '</div>')
    _p = f"suu-tap/{_slug}.html"
    open(_p, "w", encoding="utf-8").write(page(f"{_name} | Reformed Vietnam", _intro, _p, _body))
    urls.append(_p)
_hub_cards = []
for _s, _n, _d, _i in _COLS:
    _hub_cards.append(
        f'<article class="bk-card"><a class="bk-main" href="/suu-tap/{_s}.html">'
        f'<span class="bk-spine" style="background-color:{bcolor(_n)}"><i>{E(_n)}</i></span>'
        f'<span class="bk-body"><span class="bk-by">{len(_i)} cuốn sách</span><span class="bk-d">{E(_d)}</span></span>'
        '</a></article>')
open("suu-tap/index.html", "w", encoding="utf-8").write(page(
    "Bộ sưu tập sách | Reformed Vietnam",
    "Các bộ sưu tập sách Cải Chánh được chọn lọc: cho người mới tin Chúa, kinh điển, cầu nguyện và thần học hệ thống.",
    "suu-tap/index.html",
    '<h1>Bộ sưu tập sách</h1><p>Những tuyển chọn theo nhu cầu để bạn dễ bắt đầu — mỗi bộ sưu tập ưu tiên bản dịch tiếng Việt khi có.</p>'
    '<div class="bk-grid">' + "".join(_hub_cards) + '</div>'))
urls.append("suu-tap/index.html")

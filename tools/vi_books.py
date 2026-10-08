# Executed from build-pages.py. Builds ban-dich/*.html from translations/*.txt (hand/AI translations pasted from chats).
import urllib.parse as _ul, json as _j, os as _o, re as _r, shutil as _s
_TD = "translations"
_idx = _j.load(open(f"{_TD}/index.json", encoding="utf-8")) if _o.path.exists(f"{_TD}/index.json") else []
_s.rmtree("ban-dich", ignore_errors=True)
_CH = _r.compile(r"^((Chương|CHƯƠNG|Phần|PHẦN)\s+(\d+|[IVX]+)\b|Mục \d+\.?$|Lời nói đầu|LỜI NÓI ĐẦU|LỜI TỰA|[IVX]{1,5}\. [A-ZÀ-Ỹ]{3}|BẢNG ĐỐI CHIẾU|ĐỐI CHIẾU GIÁO LÝ|ĐỌC THÊM)")
_TAIL = _r.compile(r"^(BẢNG ĐỐI CHIẾU|ĐỐI CHIẾU GIÁO LÝ|ĐỌC THÊM)")
_NOTE = _r.compile(r"^(THUẬT NGỮ MỚI|CẦN DUYỆT)\s*:", _r.I)
VIBOOKS = {}
_hub = []
_o.makedirs("ban-dich", exist_ok=True); _o.makedirs(f"{_TD}/review", exist_ok=True)
open("ban-dich/.gitkeep", "w").close()
# related-books lookup: (slug, title, author, url, orig) for all published translations
_vn_rel = []
for _b2 in _idx:
    if _b2.get("hold") or not _o.path.exists(f"{_TD}/{_b2['file']}"): continue
    _s2 = _o.path.splitext(_b2["file"])[0]
    _vn_rel.append((_s2, _b2.get("title", ""), _b2.get("author", ""), f"/ban-dich/{_s2}.html", _b2.get("orig", "")))
def _vn_related(slug, author, orig):
    _okw = set(_r.findall(r"[a-zA-Z]{4,}", orig or ""))
    _rel = [x for x in _vn_rel if x[2] == author and x[0] != slug][:6]
    if len(_rel) < 6:
        _rest = [x for x in _vn_rel if x[0] != slug and x not in _rel]
        _rest.sort(key=lambda x: (-len(_okw & set(_r.findall(r"[a-zA-Z]{4,}", x[4] or ""))), x[1]))
        _rel += _rest[:6 - len(_rel)]
    if not _rel: return ""
    _cards = "".join(bcard(t, a2, u2, kicker="Bản dịch") for _, t, a2, u2, _ in _rel)
    return '<h2>Sách liên quan</h2><div class="bk-grid">' + _cards + '</div>'
for _b in _idx:
    _f = f"{_TD}/{_b['file']}"
    if _b.get("hold") or not _o.path.exists(_f): continue
    _slug = _o.path.splitext(_b["file"])[0]
    _lines = open(_f, encoding="utf-8").read().replace("\r", "").split("\n")
    _secs, _cur, _notes, _in_note, _tail = [], None, [], False, False
    for _ln in _lines:
        _t = _ln.strip()
        if _CH.match(_t) and (not _tail or _TAIL.match(_t)):
            if _TAIL.match(_t): _tail = True
            _cur = [_t, []]; _secs.append(_cur); _in_note = False; continue
        if _NOTE.match(_t): _in_note = True
        if _in_note:
            if _t: _notes.append(_t)
            continue
        if _cur is None: _cur = [_b.get("title", ""), []]; _secs.append(_cur)
        _cur[1].append(_ln)
    if _notes: open(f"{_TD}/review/{_slug}.txt", "w", encoding="utf-8").write("\n".join(_notes) + "\n")
    _rev = bool(_b.get("reviewed"))
    _by = _b.get("by", "AI")
    _orig_book = bool(_b.get("original"))
    _label = ((f'<p class="dr">Bản nháp do AI ({E(_by)}) hỗ trợ soạn, chưa được mục sư duyệt giáo lý. Nhiều câu Kinh Thánh được dịch lại từ tiếng Anh nên có thể khác chữ bản 1934; trong trình đọc, chạm vào địa chỉ câu để xem đúng bản 1934. Hãy đọc với tinh thần Bê-rê và hỏi mục sư của bạn.</p>' if not _rev else '<p class="dr">Sách đã được mục sư xem lại.</p>') if _orig_book else'<p class="dr">Bản dịch đã được mục sư xem lại. Hãy luôn đối chiếu Kinh Thánh và hỏi mục sư của bạn.</p>' if _rev else
              f'<p class="dr">Bản dịch do AI ({E(_by)}) hỗ trợ, chưa được mục sư duyệt giáo lý. Thuật ngữ có thể chưa chính xác; hãy đối chiếu với bản gốc và Kinh Thánh, đồng thời hỏi mục sư của bạn.</p>')
    _toc = "".join(f'<li><a href="#c{i+1}">{E(s[0])}</a></li>' for i, s in enumerate(_secs))
    _body_secs = ""
    for i, (h, ps) in enumerate(_secs):
        _paras = [p.strip() for p in "\n".join(ps).split("\n\n") if p.strip()]
        _body_secs += f'<h2 id="c{i+1}">{E(h)}</h2>' + "".join(f"<p>{E(p).replace(chr(10), '<br>')}</p>" for p in _paras)
    _orig = _b.get("orig", ""); _au = _b.get("author", "")
    _rd = f'/reader.html?id=vn/{_slug}&pid=' + _ul.quote(_b["id"], safe="")
    _body = (f'<style>.dr{{padding:.6em .9em;border-radius:8px;background:#d9a41e22}}.bt{{columns:1}}main h2{{margin-top:1.8em}}.rd-top{{margin:14px 0}}</style>'
             f'<h1>{E(_b["title"])}</h1><p>{E(_au)}' + (f' · <i>{E(_orig)}</i>' if _orig else '') + f'</p>{_label}' +
             f'<p class="rd-top"><a class="btn" href="{_rd}">📖 Đọc trong trình đọc</a></p>' +
             (f'<p class="dr">{E(_b["note"])}</p>' if _b.get("note") else '') + ('<p>Sách mới, miễn phí, không thương mại. Tác giả (bút danh): ' + E(_au) + '.</p>' if _orig_book else '<p>Nguyên tác thuộc phạm vi công cộng. Bản dịch tiếng Việt miễn phí, không thương mại.</p>') +
             f'<h2>Mục lục</h2><ol>{_toc}</ol>{_body_secs}' + _vn_related(_slug, _au, _orig) +
             f'<p><a class="btn" href="{_rd}">Mở trong trình đọc</a> <a class="btn s" href="/">Về thư viện</a></p>')
    _path = f"ban-dich/{_slug}.html"
    _ld = {"@context": "https://schema.org", "@type": "Book", "name": _b["title"],
           "author": {"@type": "Person", "name": _au},
           "inLanguage": "vi", "url": f"{SITE}/{_path}",
           "translator": {"@type": "Organization", "name": "Reformed Vietnam",
                          "url": SITE},
           "bookFormat": "https://schema.org/EBook", "isAccessibleForFree": True}
    if _orig: _ld["alternateName"] = _orig
    open(_path, "w", encoding="utf-8").write(page(f'{_b["title"]} · bản dịch tiếng Việt | Reformed Vietnam', f'Bản dịch tiếng Việt "{_b["title"]}" của {_au}. Miễn phí.', _path, _body, _ld))
    urls.append(_path)
    VIBOOKS[_b["id"]] = {"u": "/" + _path, "by": _by, "r": _rev, "rd": f"reader.html?id=vn/{_slug}&pid=" + _ul.quote(_b["id"], safe="")}
    _hub.append((_b["title"], _au, _b.get("orig", ""), "/" + _path, _rev, _orig_book))
open("vi-books.json", "w", encoding="utf-8").write(_j.dumps(VIBOOKS, ensure_ascii=False))

_li = lambda x: bcard(x[0], x[1], x[3], badge=("đã duyệt" if x[4] else "AI, chưa duyệt"), kicker=x[2] or "Bản dịch")
_tr = "".join(_li(x) for x in _hub if not x[5]); _nw = "".join(_li(x) for x in _hub if x[5])
_hb = ('<h1>Bản dịch và sách mới</h1><p class="dr" style="padding:.6em .9em;border-radius:8px;background:#d9a41e22">Các sách dưới đây do AI hỗ trợ dịch hoặc soạn và <b>chưa được mục sư duyệt giáo lý</b>. Hãy đối chiếu Kinh Thánh và hỏi mục sư của bạn.</p>'
       + (f'<h2>Bản dịch tiếng Việt</h2>' + bkgrid(_tr) if _tr else '') + (f'<h2>Sách mới (tác giả David)</h2>' + bkgrid(_nw) if _nw else '') + '<p><a class="btn" href="/">Về thư viện</a></p>')
if _hub:
    open("ban-dich/index.html", "w", encoding="utf-8").write(page("Bản dịch và sách mới | Reformed Vietnam", "Các bản dịch tiếng Việt và sách mới do AI hỗ trợ, chưa duyệt giáo lý. Miễn phí.", "ban-dich/index.html", _hb))
    urls.append("ban-dich/index.html")

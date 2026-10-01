# Executed from build-pages.py. Builds ban-dich/*.html from translations/*.txt (hand/AI translations pasted from chats).
import json as _j, os as _o, re as _r, shutil as _s
_TD = "translations"
_idx = _j.load(open(f"{_TD}/index.json", encoding="utf-8")) if _o.path.exists(f"{_TD}/index.json") else []
_s.rmtree("ban-dich", ignore_errors=True)
_CH = _r.compile(r"^(Chương|CHƯƠNG|Phần|PHẦN|Lời nói đầu|LỜI NÓI ĐẦU)\b")
_NOTE = _r.compile(r"^(THUẬT NGỮ MỚI|CẦN DUYỆT)\s*:", _r.I)
VIBOOKS = {}
_o.makedirs("ban-dich", exist_ok=True); _o.makedirs(f"{_TD}/review", exist_ok=True)
open("ban-dich/.gitkeep", "w").close()
for _b in _idx:
    _f = f"{_TD}/{_b['file']}"
    if _b.get("hold") or not _o.path.exists(_f): continue
    _slug = _o.path.splitext(_b["file"])[0]
    _lines = open(_f, encoding="utf-8").read().replace("\r", "").split("\n")
    _secs, _cur, _notes, _in_note = [], None, [], False
    for _ln in _lines:
        _t = _ln.strip()
        if _CH.match(_t):
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
    _label = ('<p class="dr">Bản dịch đã được mục sư xem lại. Hãy luôn đối chiếu Kinh Thánh và hỏi mục sư của bạn.</p>' if _rev else
              f'<p class="dr">Bản dịch do AI ({E(_by)}) hỗ trợ, chưa được mục sư duyệt giáo lý. Thuật ngữ có thể sai; hãy đối chiếu bản gốc và Kinh Thánh, và hỏi mục sư của bạn.</p>')
    _toc = "".join(f'<li><a href="#c{i+1}">{E(s[0])}</a></li>' for i, s in enumerate(_secs))
    _body_secs = ""
    for i, (h, ps) in enumerate(_secs):
        _paras = [p.strip() for p in "\n".join(ps).split("\n\n") if p.strip()]
        _body_secs += f'<h2 id="c{i+1}">{E(h)}</h2>' + "".join(f"<p>{E(p).replace(chr(10), '<br>')}</p>" for p in _paras)
    _orig = _b.get("orig", ""); _au = _b.get("author", "")
    _body = (f'<style>.dr{{padding:.6em .9em;border-radius:8px;background:#d9a41e22}}.bt{{columns:1}}main h2{{margin-top:1.8em}}</style>'
             f'<h1>{E(_b["title"])}</h1><p>{E(_au)}' + (f' · <i>{E(_orig)}</i>' if _orig else '') + f'</p>{_label}'
             f'<p>Nguyên tác thuộc phạm vi công cộng. Bản dịch tiếng Việt miễn phí, không thương mại.</p>'
             f'<h2>Mục lục</h2><ol>{_toc}</ol>{_body_secs}'
             f'<p><a class="btn" href="/">Về thư viện</a></p>')
    _path = f"ban-dich/{_slug}.html"
    open(_path, "w", encoding="utf-8").write(page(f'{_b["title"]} · bản dịch tiếng Việt | Reformed Vietnam', f'Bản dịch tiếng Việt "{_b["title"]}" của {_au}. Miễn phí.', _path, _body))
    urls.append(_path)
    VIBOOKS[_b["id"]] = {"u": "/" + _path, "by": _by, "r": _rev}
open("vi-books.json", "w", encoding="utf-8").write(_j.dumps(VIBOOKS, ensure_ascii=False))

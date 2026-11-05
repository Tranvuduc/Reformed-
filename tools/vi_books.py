# Executed from build-pages.py. Builds ban-dich/*.html from translations/*.txt (hand/AI translations pasted from chats).
import urllib.parse as _ul, json as _j, os as _o, re as _r, shutil as _s
_TD = "translations"
_idx = _j.load(open(f"{_TD}/index.json", encoding="utf-8")) if _o.path.exists(f"{_TD}/index.json") else []
# Batch C: chunked regen (see regen-runbook.md) sets VI_BOOKS_KEEP_BANDICH=1
# for chunks after the first, so a resume never wipes already-built pages.
# Default behaviour (env unset) is unchanged: wipe and rebuild ban-dich/.
if not _o.environ.get("VI_BOOKS_KEEP_BANDICH"):
    _s.rmtree("ban-dich", ignore_errors=True)

_CH = _r.compile(r"^((Chương|CHƯƠNG|Phần|PHẦN)\s+(\d+|[IVX]+)\b|Mục \d+\.?$|Lời nói đầu|LỜI NÓI ĐẦU|LỜI TỰA|[IVX]{1,5}\. [A-ZÀ-Ỹ]{3}|BẢNG ĐỐI CHIẾU|ĐỐI CHIẾU GIÁO LÝ|ĐỌC THÊM)")
_TAIL = _r.compile(r"^(BẢNG ĐỐI CHIẾU|ĐỐI CHIẾU GIÁO LÝ|ĐỌC THÊM)")
_NOTE = _r.compile(r"^(THUẬT NGỮ MỚI|CẦN DUYỆT)\s*:", _r.I)
# --- Batch C patch (2026-11-05, site design-consistency fix) ---
# H2: raw Markdown in translations/*.txt leaked as visible text (<p># ...,
# <p>**...**, <p>---</p>) + the "TRANSLATION STATUS: COMPLETE /
# TERMINOLOGY ISSUES:" footer block printed at the end of pages.
# H9: giant pages had no in-page navigation (Bavinck: 3 <h2>, 1 TOC link).
# M7: ALL-CAPS titles wrapped to 3+ lines at 1.9rem.
# Rendering-only changes: translations/*.txt and index.json are NEVER edited.
_MD_H = _r.compile(r"^(#{1,6})\s+(.*)$")            # Markdown heading line (Wave 2: was {1,3}; corpus has #### / ##### too)
_MD_SEP = _r.compile(r"^(---|\*\*\*|___)\s*$")      # horizontal-rule line: drop
_MD_FOOT = _r.compile(r"^(TRANSLATION STATUS|TERMINOLOGY ISSUES)\s*:")  # footer-block trigger
_MD_MARK = _r.compile(r"^\x00MDH\x00(md-\d+)\x00(.*)$")  # stored md sub-heading marker
_BOLD = _r.compile(r"\*\*(.+?)\*\*|__(.+?)__")      # **bold** / __bold__
_EMPH = _r.compile(r"(?<!\w)\*([\(\[A-Za-zÀ-ỹ][^*\n]*?)\*(?!\w)")  # *emphasis*
def _md_inline(s):
    """Strip Markdown emphasis markers, keep inner text (H2).
    Paired **bold** / __bold__ / *emphasis* first; any unpaired leftover
    ** or __ is also dropped (e.g. the bibliography line '** Smend, ...'
    in Bavinck, whose closing marker never existed). A lone single '*'
    is left alone: it is usually a footnote marker, not emphasis."""
    s = _BOLD.sub(lambda m: m.group(1) if m.group(1) is not None else m.group(2), s)
    s = _EMPH.sub(r"\1", s)
    return s.replace("**", "").replace("__", "")
_ACRONYMS = {"WSC", "KJV", "NKJV", "ESV", "NASB", "NIV", "BDM", "CCEL", "EPUB",
             "PDF", "MP3", "URL", "HTML", "AI", "DVD", "CD", "BD", "NT", "OT"}
_ROMAN = _r.compile(r"^[IVXLCDM]+$")
def _is_vowel(ch):
    """Vietnamese vowel test without unicodedata: ASCII vowels, plus any
    non-ASCII letter except Đ (every other non-ASCII Vietnamese letter is
    a vowel: à á â ã ả ạ ă ắ ... ơ ư ỳ ý ...)."""
    if ch in "AEIOUY":
        return True
    if ch == "Đ":
        return False
    return not ch.isascii()
def _keep_caps(core):
    """True when an all-caps word is probably an acronym / numeral, not a
    Vietnamese word: explicit allowlist, Roman numerals (I..VIII), a single
    ASCII letter, or a word with no vowel at all (WSC, KJV, BDM).
    NOTE: a length rule does NOT work here — most Vietnamese words are
    2-4 letters ('ĐÁ', 'CHO', 'LÝ' would all be wrongly kept)."""
    if not core or not core.isupper():
        return False
    if core in _ACRONYMS:
        return True
    if _ROMAN.match(core) and len(core) <= 5:
        return True
    if len(core) == 1 and core.isascii():
        return True
    return not any(_is_vowel(ch) for ch in core)
def _titlecase_vi(t):
    """Render-time Title Case for ALL-CAPS titles (M7). Display only.
    Rule: transform only when every cased char is uppercase (str.isupper()).
    Word-by-word titlecase, except words _keep_caps() identifies as probable
    acronyms/numerals, which stay verbatim. Mixed-case titles pass through
    untouched."""
    if not t or not t.isupper():
        return t
    _out = []
    for _w in t.split(" "):
        _core = _w.strip(".,;:!?()\"'«»—–-")
        if _keep_caps(_core):
            _out.append(_w)
        else:
            _out.append(_w.capitalize())
    return " ".join(_out)
_TOTOP_CSS = ".totop{position:fixed;right:16px;bottom:18px;z-index:50;background:var(--accbtn,#9a3412);color:#fff;padding:8px 14px;border-radius:999px;text-decoration:none;font:600 14px system-ui,sans-serif;box-shadow:0 2px 10px rgba(0,0,0,.25)}"
_TOTOP_MIN = 50 * 1024  # H9: back-to-top only on pages over ~50 KB of body HTML
def _normfile(f):
    """Normalise an index 'file' value to a translations/ slug (no dir, no ext).
    Tolerates the 'translations/' prefix found on 589 live index entries
    (e.g. 'translations/calvin-isaiah-vol1.txt'), which the old code silently
    skipped (path translations/translations/... never exists). Returns None
    when the entry has no file at all (3 live entries)."""
    if not f:
        return None
    if f.startswith("translations/"):
        f = f[len("translations/"):]
    return _o.path.splitext(f)[0]
def _resolve(b):
    """Resolve title/author/orig for an index entry (Wave 2). The standard
    schema has 'title'/'author'/'orig', but 43 live MG-3 entries use
    'short'/'a'/'vi':{'t'}/'en':{'t'} instead (no 'title' key at all — the
    old code crashed with KeyError: 'title' on them). 'short' first for the
    title: live pages show the short title (e.g. 'Sống Hay Chết?'), which is
    already Title Case, so _titlecase_vi leaves it unchanged."""
    _t = b.get("title") or b.get("short") or (b.get("vi") or {}).get("t") or ""
    _a = b.get("author") or b.get("a") or ""
    _o = b.get("orig") or (b.get("en") or {}).get("t") or ""
    return _t, _a, _o
def _is_footer_trigger(t):
    """True when a source line opens the translator's footer block (H2, Wave 2).
    Attested forms: 'TRANSLATION STATUS: ...', '**TRANSLATION STATUS:** ...',
    '## TRANSLATION STATUS', '## TERMINOLOGY ISSUES' (53 + 40 files). A
    Markdown heading prefix and emphasis markers are stripped before testing,
    so the bold / heading variants are caught too. Exact-phrase match only,
    so a content heading merely mentioning the words does not trigger."""
    _u = t
    _mh = _MD_H.match(_u)
    if _mh:
        _u = _mh.group(2).strip()
    _u = _u.strip("*_ ").strip()
    if _MD_FOOT.match(_u):
        return True
    return _u.rstrip(":").strip().upper() in ("TRANSLATION STATUS", "TERMINOLOGY ISSUES")
VIBOOKS = {}
_hub = []; _nofile = []  # Batch C: _nofile = index entries with no 'file' key (3 in live index.json)
# Batch C: chunked regen (see regen-runbook.md) sets VI_BOOKS_ONLY to a comma
# separated slug list; only those books are (re)built, while _vn_rel above
# still uses the FULL index, so "Sách liên quan" stays correct. Unset = all.
_ONLY = set(_o.environ["VI_BOOKS_ONLY"].split(",")) if _o.environ.get("VI_BOOKS_ONLY") else None
_o.makedirs("ban-dich", exist_ok=True); _o.makedirs(f"{_TD}/review", exist_ok=True)
open("ban-dich/.gitkeep", "w").close()
# related-books lookup: (slug, title, author, url, orig) for all published translations
_vn_rel = []
for _b2 in _idx:
    _s2 = _normfile(_b2.get("file"))  # Batch C: tolerate 'translations/' prefix; skip file-less entries
    if _b2.get("hold") or not _s2 or not _o.path.exists(f"{_TD}/{_s2}.txt"): continue
    _rt, _ra, _ro = _resolve(_b2)  # Wave 2: MG-3 entries have no 'title'/'author'/'orig'
    _vn_rel.append((_s2, _rt, _ra, f"/ban-dich/{_s2}.html", _ro))
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
    _slug = _normfile(_b.get("file"))  # Batch C: tolerate 'translations/' prefix; skip file-less entries
    if _slug is None:
        _nofile.append(_b.get("id", "?")); continue
    if _ONLY is not None and _slug not in _ONLY: continue  # Batch C: chunked regen filter
    _f = f"{_TD}/{_slug}.txt"
    if _b.get("hold") or not _o.path.exists(_f): continue
    _lines = open(_f, encoding="utf-8").read().replace("\r", "").split("\n")
    _bt, _au, _orig = _resolve(_b)  # Wave 2: MG-3 entries have no 'title'/'author'/'orig'
    _dt = _titlecase_vi(_bt)  # Batch C (M7): display title
    _secs, _cur, _notes, _in_note, _tail, _in_footer, _md_n = [], None, [], False, False, False, 0
    for _ln in _lines:
        _t = _ln.strip()
        # Batch C (H2): translation-footer block. Detected BEFORE section
        # assembly and BEFORE the _NOTE diversion, so it never reaches the
        # rendered page nor translations/review/*.txt. Skipped to end of file,
        # unless a real content heading resumes (footer pasted mid-file).
        if _in_footer:
            if _is_footer_trigger(_t):
                continue  # Wave 2: another status/terminology heading inside the footer: stay in footer mode
            if _CH.match(_t) or _MD_H.match(_t):
                _in_footer = False  # fall through: process this heading normally
            else:
                continue
        elif _is_footer_trigger(_t):
            _in_footer = True
            continue
        # Batch C (H2): Markdown headings. "# " starts a new chapter section
        # (real <h2 id="cN"> + TOC entry, like _CH); "## " and deeper become
        # <h3 id="md-N"> sub-headings inside the current section (+ TOC).
        # Wave 2: depth extended to 6 (corpus has 135 '####' + 35 '#####' lines).
        _mh = _MD_H.match(_t)
        if _mh:
            _ht = _md_inline(_mh.group(2).strip())
            if not _ht:
                continue
            if len(_mh.group(1)) == 1 and (not _tail or _TAIL.match(_ht)):
                if _TAIL.match(_ht): _tail = True
                # a level-1 heading identical to the book title repeats the <h1>
                if _ht.lower() == _dt.strip().lower():
                    _in_note = False; continue
                _cur = [_ht, []]; _secs.append(_cur); _in_note = False; continue
            if _cur is None: _cur = [_dt, []]; _secs.append(_cur)
            _md_n += 1
            _cur[1].append("\x00MDH\x00md-%d\x00%s" % (_md_n, _ht))
            _in_note = False; continue
        # Batch C (H2): drop horizontal-rule lines (--- / *** / ___).
        if _MD_SEP.match(_t):
            continue
        if _CH.match(_t) and (not _tail or _TAIL.match(_t)):
            if _TAIL.match(_t): _tail = True
            _cur = [_md_inline(_t), []]; _secs.append(_cur); _in_note = False; continue
        if _NOTE.match(_t): _in_note = True
        if _in_note:
            if _t: _notes.append(_t)
            continue
        # Wave 2 (H2): stray '#' marker on a content line (list numbers '#9.',
        # leaked anchors '#comment-...', refs '#II ...'): drop the single marker
        # and keep the text, so no '<p>#' leak remains. Heading lines were
        # already consumed by _MD_H above; a '#' reaching here has no space
        # after it, so it is not a heading.
        if _t.startswith("#"):
            _ln = _t[1:]
        if _cur is None: _cur = [_dt, []]; _secs.append(_cur)
        _cur[1].append(_ln)
    if _notes: open(f"{_TD}/review/{_slug}.txt", "w", encoding="utf-8").write("\n".join(_notes) + "\n")
    _rev = bool(_b.get("reviewed"))
    _by = _b.get("by", "AI")
    _orig_book = bool(_b.get("original"))
    _label = ((f'<p class="dr">Bản nháp do AI ({E(_by)}) hỗ trợ soạn, chưa được mục sư duyệt giáo lý. Nhiều câu Kinh Thánh được dịch lại từ tiếng Anh nên có thể khác chữ bản 1934; trong trình đọc, chạm vào địa chỉ câu để xem đúng bản 1934. Hãy đọc với tinh thần Bê-rê và hỏi mục sư của bạn.</p>' if not _rev else '<p class="dr">Sách đã được mục sư xem lại.</p>') if _orig_book else'<p class="dr">Bản dịch đã được mục sư xem lại. Hãy luôn đối chiếu Kinh Thánh và hỏi mục sư của bạn.</p>' if _rev else
              f'<p class="dr">Bản dịch do AI ({E(_by)}) hỗ trợ, chưa được mục sư duyệt giáo lý. Thuật ngữ có thể chưa chính xác; hãy đối chiếu với bản gốc và Kinh Thánh, đồng thời hỏi mục sư của bạn.</p>')
    # Batch C (H2/H9): TOC includes the Markdown sub-headings (id md-N).
    _toc_ps = []
    for i, s in enumerate(_secs):
        _toc_ps.append(f'<li><a href="#c{i+1}">{E(s[0])}</a></li>')
        for _ln in s[1]:
            _mm = _MD_MARK.match(_ln)
            if _mm:
                _toc_ps.append(f'<li class="toc-sub"><a href="#{_mm.group(1)}">{E(_mm.group(2))}</a></li>')
    _toc = "".join(_toc_ps)
    _body_secs = ""
    for i, (h, ps) in enumerate(_secs):
        _paras = [p.strip() for p in "\n".join(ps).split("\n\n") if p.strip()]
        _sec_html = f'<h2 id="c{i+1}">{E(h)}</h2>'
        for p in _paras:
            # Batch C (H2): split out md sub-heading markers (whole lines);
            # remaining lines form one <p> with <br> joins, as before.
            # Batch C (H2): strip ** / * emphasis markers inside paragraphs.
            _buf = []
            for _line in p.split("\n"):
                _mm = _MD_MARK.match(_line)
                if _mm:
                    if _buf:
                        _sec_html += f"<p>{E(_md_inline(chr(10).join(_buf).strip())).replace(chr(10), '<br>')}</p>"; _buf = []
                    _sec_html += f'<h3 id="{_mm.group(1)}">{E(_mm.group(2))}</h3>'
                else:
                    _buf.append(_line)
            if _buf:
                _sec_html += f"<p>{E(_md_inline(chr(10).join(_buf).strip())).replace(chr(10), '<br>')}</p>"
        _body_secs += _sec_html
    # _au / _orig resolved above via _resolve (Wave 2)
    _rd = f'/reader.html?id=vn/{_slug}&pid=' + _ul.quote(_b["id"], safe="")
    _toc_css = ".toc-sub{margin-left:1.2em}" if "toc-sub" in _toc else ""  # Batch C: only when md sub-headings exist
    _body = (f'<style>.bt{{columns:1}}main h2{{margin-top:1.8em}}.rd-top{{margin:14px 0}}{_toc_css}</style>'
             f'<h1>{E(_dt)}</h1><p>{E(_au)}' + (f' · <i>{E(_orig)}</i>' if _orig else '') + f'</p>{_label}' +
             f'<p class="rd-top"><a class="btn primary" href="{_rd}">📖 Đọc trong trình đọc</a></p>' +
             (f'<p class="dr">{E(_b["note"])}</p>' if _b.get("note") else '') + ('<p>Sách mới, miễn phí, không thương mại. Tác giả (bút danh): ' + E(_au) + '.</p>' if _orig_book else '<p>Nguyên tác thuộc phạm vi công cộng. Bản dịch tiếng Việt miễn phí, không thương mại.</p>') +
             f'<h2>Mục lục</h2><ol>{_toc}</ol>{_body_secs}' + _vn_related(_slug, _au, _orig) +
             f'<p><a class="btn primary" href="{_rd}">Mở trong trình đọc</a> <a class="btn s" href="/">Về thư viện</a></p>')
    # Batch C (H9): back-to-top button on long pages (>~50 KB of body HTML).
    # href="#top" scrolls to top per the HTML fragment rule; the h1 anchor
    # makes it explicit. Small pages are untouched (no chrome diff).
    if len(_body) > _TOTOP_MIN:
        _body = _body.replace("</style>", _TOTOP_CSS + "</style>", 1)
        _body = _body.replace("<h1>", '<h1 id="top">', 1)
        _body += '<a href="#top" class="totop">↑ Đầu trang</a>'
    _path = f"ban-dich/{_slug}.html"
    _ld = {"@context": "https://schema.org", "@type": "Book", "name": _dt,
           "author": {"@type": "Person", "name": _au},
           "inLanguage": "vi", "url": f"{SITE}/{_path}",
           "translator": {"@type": "Organization", "name": "Reformed Vietnam",
                          "url": SITE},
           "bookFormat": "https://schema.org/EBook", "isAccessibleForFree": True}
    if _orig: _ld["alternateName"] = _orig
    open(_path, "w", encoding="utf-8").write(page(f'{_dt} · bản dịch tiếng Việt | Reformed Vietnam', f'Bản dịch tiếng Việt "{_dt}" của {_au}. Miễn phí.', _path, _body, _ld))
    urls.append(_path)
    VIBOOKS[_b["id"]] = {"u": "/" + _path, "by": _by, "r": _rev, "rd": f"reader.html?id=vn/{_slug}&pid=" + _ul.quote(_b["id"], safe="")}
    _hub.append((_bt, _au, _orig, "/" + _path, _rev, _orig_book))
open("vi-books.json", "w", encoding="utf-8").write(_j.dumps(VIBOOKS, ensure_ascii=False))
# Batch C: the live index has entries with no 'file' key; they are skipped, not fatal.
if _nofile:
    print("vi_books: skipped %d index entries without 'file': %s" % (len(_nofile), ", ".join(_nofile[:10])))

_li = lambda x: bcard(x[0], x[1], x[3], badge=("đã duyệt" if x[4] else "AI, chưa duyệt"), kicker=x[2] or "Bản dịch")
_tr = "".join(_li(x) for x in _hub if not x[5]); _nw = "".join(_li(x) for x in _hub if x[5])
_hb = ('<h1>Bản dịch và sách mới</h1><p class="dr" style="padding:.6em .9em;border-radius:8px;background:#d9a41e22">Các sách dưới đây do AI hỗ trợ dịch hoặc soạn và <b>chưa được mục sư duyệt giáo lý</b>. Hãy đối chiếu Kinh Thánh và hỏi mục sư của bạn.</p>'
       + (f'<h2>Bản dịch tiếng Việt</h2>' + bkgrid(_tr) if _tr else '') + (f'<h2>Sách mới (tác giả David)</h2>' + bkgrid(_nw) if _nw else '') + '<p><a class="btn primary" href="/">Về thư viện</a></p>')
if _hub:
    open("ban-dich/index.html", "w", encoding="utf-8").write(page("Bản dịch và sách mới | Reformed Vietnam", "Các bản dịch tiếng Việt và sách mới do AI hỗ trợ, chưa duyệt giáo lý. Miễn phí.", "ban-dich/index.html", _hb))
    urls.append("ban-dich/index.html")

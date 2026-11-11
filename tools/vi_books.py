# Executed from build-pages.py. Builds ban-dich/*.html from translations/*.txt (hand/AI translations pasted from chats).
import urllib.parse as _ul, json as _j, os as _o, re as _r, shutil as _s
_TD = "translations"
_idx = _j.load(open(f"{_TD}/index.json", encoding="utf-8")) if _o.path.exists(f"{_TD}/index.json") else []
# Phase 1.6: tier-2 title overrides — shortened display titles (<=38 chars,
# so the full <title> stays <=60). tools/ban-dich-titles-tier2.json, built
# from the verified worklist; absent file = no overrides (safe default).
_OVR = _j.load(open("tools/ban-dich-titles-tier2.json", encoding="utf-8")) if _o.path.exists("tools/ban-dich-titles-tier2.json") else {}
# Phase 1.3: author bio map — catalogue author string -> /a/<slug> slug.
# tools/author-slug-map.json; absent file or null value = plain author text.
_AMAP = _j.load(open("tools/author-slug-map.json", encoding="utf-8")) if _o.path.exists("tools/author-slug-map.json") else {}
# Phase 1.3: author aliases — catalogue spellings that are the same person as
# an existing bio page (verified 2026-11-11, phase1-1.3-analysis.md §2).
# Tier A: middle initial/name dropped. Tier B: full-name / spelling variants,
# "Mục sư" prefix, embedded dates, and surname-only spellings verified
# per-book (Whitefield/Burroughs/Warfield/Thornwell/Berridge/Watson/Keach/
# Baxter/T. Watson/Bridge). NOT aliased: "Thomas, Jun Watson" (the son, 1785
# — not the elder Thomas Watson), the three Jonathan Edwardses, the two
# non-Haddington John Browns, J. Ligon Duncan, "David" (pen name), Monergism,
# A. A. Hodge, multi-person strings, "D.D." — see the analysis.
_AUTHOR_ALIASES = {
    "William S. Plumer": "william-plumer",
    "Benjamin B. Warfield": "benjamin-warfield",
    "Robert Lewis Dabney": "robert-dabney",
    "James Henley Thornwell": "james-thornwell",
    "Andrew A. Bonar": "andrew-bonar",
    "Robert S. Candlish": "robert-candlish",
    "Robert Smith Candlish": "robert-candlish",
    "James P. Boyce": "james-boyce",
    "James H. Thornwell": "james-thornwell",
    "Charles R. Hodge": "charles-hodge",
    "Andrew R. Bonar": "andrew-bonar",
    "Augustus H. Strong": "augustus-strong",
    "John A. Broadus": "john-broadus",
    "John L. Girardeau": "john-girardeau",
    "Edward D. Griffin": "edward-griffin",
    "A. W. Pink": "arthur-pink",
    "Benjamin Breckinridge Warfield": "benjamin-warfield",
    "Peter Martyr Vermigli": "pietro-martire-vermigli",
    "Henry Bullinger": "heinrich-bullinger",
    "William G. T. Shedd": "william-shedd",
    "W. G. T. Shedd": "william-shedd",
    "John Brown (of Haddington)": "john-brown",
    "John Brown of Haddington": "john-brown",
    "Nathanael Vincent": "nathaniel-vincent",
    "Whitefield": "george-whitefield",
    "A.M James Hervey": "james-hervey",
    "Thomas Goodwin of Pinner": "thomas-goodwin",
    "Alexander (1836-1921) Whyte": "alexander-whyte",
    "Augustus Montague Toplady": "augustus-toplady",
    "Burroughs": "jeremiah-burroughs",
    "Athanasius": "athanasius-of-alexandria",
    "Zacharius Ursinus": "zacharias-ursinus",
    "Arthur Hildersham": "arthur-hildersam",
    "Thomas McCrie": "thomas-m-crie",
    "J. H. Merle D'Aubigné": "j-h-jean-henri-merle-d-aubigne",
    "William B. Sprague": "william-buell-sprague",
    "James W. Alexander": "j-w-alexander",
    "Mục sư Thomas M. Chalmers": "thomas-chalmers",
    "Mục sư Benjamin Morgan Palmer": "benjamin-morgan-palmer",
    "Charles, 1797-1878 Hodge": "charles-hodge",
    "John Gill (1697-1771)": "john-gill",
    "Westminster Assembly": "westminster-assembly-1643-1652",
    "Warfield": "benjamin-warfield",
    "Thornwell": "james-thornwell",
    "Berridge": "john-berridge",
    "Watson": "thomas-watson",
    "Keach": "benjamin-keach",
    "Baxter": "richard-baxter",
    "T. Watson": "thomas-watson",
    "Bridge": "william-bridge",
}
# Phase 1.3: original-source links — tools/source-urls.json lists LIVE-VERIFIED
# IA identifiers ("ia") and CCEL ids ("ccel"), checked 2026-11-11. Absent
# file = no source links (safe default). Only these verified ids are linked;
# nothing is derived from an unverified pattern.
_SRC = _j.load(open("tools/source-urls.json", encoding="utf-8")) if _o.path.exists("tools/source-urls.json") else {"ia": [], "ccel": []}
_SRC_IA = set(_SRC.get("ia", [])); _SRC_CCEL = set(_SRC.get("ccel", []))
# The one catalogue src (djvu.txt) that returns a persistent 500
# (2026-11-11); its details page is the fallback, no djvu link is shown.
_SRC_BROKEN_DJVU = "arch/faithfulnarrativ00edwa"
# Phase 1.2: graduated review badges. States: ai-draft (default) / in-review /
# reviewed. No reviewer is ever invented: "reviewed" requires review_status
# "reviewed" (or the legacy reviewed=true) in the catalogue entry.
_RSTATUS = {"ai-draft": "Bản dịch AI, chưa duyệt", "in-review": "Đang được duyệt", "reviewed": "Đã được mục sư duyệt"}
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
_TOTOP_CSS = ".totop{position:fixed;right:16px;bottom:18px;z-index:50;background:var(--accbtn,#7c2128);color:#fff;padding:8px 14px;border-radius:999px;text-decoration:none;font:600 14px system-ui,sans-serif;box-shadow:0 2px 10px rgba(0,0,0,.25)}"
_TOTOP_MIN = 50 * 1024  # H9: back-to-top only on pages over ~50 KB of body HTML
# Phase 3.4: reading-time estimate. 175 words/min = the speed reader.html
# uses for its remaining-time estimate, so the book-page figure and the
# in-reader ETA agree. Rounded to the nearest 5 minutes: an estimate, not
# a promise. Returns (display text, rounded minutes).
def _read_time(words, wpm=175):
    mins = max(5, round(max(1, round(words / wpm)) / 5) * 5)
    if mins < 60:
        return f"khoảng {mins} phút", mins
    h, m = divmod(mins, 60)
    return (f"khoảng {h} giờ {m} phút" if m else f"khoảng {h} giờ"), mins
def _words_fmt(n):
    return f"{n:,}".replace(",", ".")  # Vietnamese thousands separator
def _vn_date(iso):
    y, m, d = iso.split("-")
    return f"{int(d)}/{int(m)}/{y}"
_MD_MARK_PFX = _r.compile(r"^\x00MDH\x00md-\d+\x00")  # strip md sub-heading marker, keep the heading text
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
    _rstat = _b.get("review_status") or ("reviewed" if _rev else "ai-draft")  # Phase 1.2
    _rbadge = _RSTATUS.get(_rstat, _RSTATUS["ai-draft"])
    _by = _b.get("by", "AI")
    _orig_book = bool(_b.get("original"))
    _label = ((f'<p class="dr">Bản nháp do AI ({E(_by)}) hỗ trợ soạn, chưa được mục sư duyệt giáo lý. Nhiều câu Kinh Thánh được dịch lại từ tiếng Anh nên có thể khác chữ bản 1934; trong trình đọc, chạm vào địa chỉ câu để xem đúng bản 1934. Hãy đọc với tinh thần Bê-rê và hỏi mục sư của bạn.</p>' if not _rev else '<p class="dr">Sách đã được mục sư xem lại.</p>') if _orig_book else'<p class="dr">Bản dịch đã được mục sư xem lại. Hãy luôn đối chiếu Kinh Thánh và hỏi mục sư của bạn.</p>' if _rev else
              f'<p class="dr">Bản dịch do AI ({E(_by)}) hỗ trợ, chưa được mục sư duyệt giáo lý. Thuật ngữ có thể chưa chính xác; hãy đối chiếu với bản gốc và Kinh Thánh, đồng thời hỏi mục sư của bạn.</p>')
    # Phase 3.4: word count over the rendered text (headings + paragraphs;
    # translator footer + review notes are excluded — they never render).
    _words = 0
    for _h, _ps in _secs:
        _words += len(_h.split())
        for _ln2 in _ps:
            _words += len(_MD_MARK_PFX.sub("", _ln2).split())
    _rt, _mins = _read_time(_words)
    # Phase 3.2/3.3: reader URL (also used by the per-chapter deep links).
    _rd = f'/reader.html?id=vn/{_slug}&pid=' + _ul.quote(_b["id"], safe="")
    # Batch C (H2/H9): TOC includes the Markdown sub-headings (id md-N).
    # Phase 3.3: each top-level chapter also gets a "Đọc →" deep link into
    # the reader (?at=<heading>); the reader matches it against the chapter
    # heading text (reader.html normalises leading "# " / "**" markers).
    _toc_ps = []
    for i, s in enumerate(_secs):
        _at = _ul.quote(s[0], safe="")
        _toc_ps.append(f'<li><a href="#c{i+1}">{E(s[0])}</a> <a class="toc-rd" href="{_rd}&at={_at}">Đọc →</a></li>')
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
    _toc_css = ".toc-rd{font:600 12px 'Be Vietnam Pro',system-ui,sans-serif;color:var(--mut);margin-left:6px;text-decoration:none;white-space:nowrap}" + (".toc-sub{margin-left:1.2em}" if "toc-sub" in _toc else "")  # Batch C: only when md sub-headings exist
    _au_slug = _AMAP.get(_au) or _AUTHOR_ALIASES.get(_au)  # Phase 1.3: exact map, then alias
    _au_html = f'<a href="/a/{_au_slug}.html">{E(_au)}</a>' if _au_slug else E(_au)  # Phase 1.3: author bio link when mapped
    _au_line = f'<p>{_au_html}' + (f' · <i>{E(_orig)}</i>' if _orig else '') + f' <span class="rv-badge rv-{_rstat}">{_rbadge}</span></p>'
    _rt_line = f'<p class="m">⏱ Thời gian đọc ước tính: {_rt} · {_words_fmt(_words)} từ (tốc độ 175 từ/phút)</p>'  # Phase 3.4
    # Phase 3.2: resume button. Hidden unless this device has a saved
    # position for the book (reader.html stores rv.pos.vn/<slug> +
    # rv.prog[<pid>]); the script unhides it and points it at the saved page.
    _resume_js = ('<script>(function(){try{var id=' + _j.dumps("vn/" + _slug) + ',pid=' + _j.dumps(_b["id"]) +
                  ',pos=+localStorage.getItem("rv.pos."+id)||0;if(!pos)return;'
                  'var b=document.getElementById("rv-resume");if(!b)return;'
                  'var pr=null;try{pr=JSON.parse(localStorage.getItem("rv.prog")||"{}")[pid]}catch(e){}'
                  'b.hidden=false;b.href="/reader.html?id="+id+"&pid="+encodeURIComponent(pid)+"&p="+pos;'
                  'b.textContent="▶ Tiếp tục đọc — trang "+(pos+1)+(pr&&pr.p?" · "+pr.p+"%":"");}catch(e){}})()</script>')
    _rep = "mailto:reformedvn@gmail.com?subject=" + _ul.quote(f"Báo lỗi bản dịch: {_dt} — {_au}")  # Phase 1.1: page context in subject
    _rep_line = f'<p class="m">Thấy lỗi trong bản dịch? <a href="{_rep}">Báo lỗi bản dịch</a>.</p>'
    # Phase 1.3: original-source link(s) — only live-verified ids (see _SRC).
    # IA details page ("bản gốc") and, for the 26 catalogue src entries, the
    # djvu.txt text that was actually translated ("văn bản nguồn đã dịch").
    _id = _b.get("id", "")
    _src_links = []
    if _id.startswith("arch/") and _id[5:] in _SRC_IA:
        _src_links.append(f'<a href="https://archive.org/details/{_id[5:]}">Xem bản gốc tại Internet Archive</a>')
    elif _id.startswith("arch-") and _id[5:] in _SRC_IA:
        _src_links.append(f'<a href="https://archive.org/details/{_id[5:]}">Xem bản gốc tại Internet Archive</a>')
    elif "/" in _id and _id in _SRC_CCEL:
        _src_links.append(f'<a href="https://ccel.org/ccel/{_id}">Đọc bản gốc tại CCEL</a>')
    _djvu = _b.get("src")
    if _djvu and _id != _SRC_BROKEN_DJVU:
        _src_links.append(f'<a href="{E(_ul.quote(_djvu, safe="/:"))}">Văn bản nguồn đã dịch</a>')
    _src_line = ('<p class="m">Nguồn: ' + " · ".join(_src_links) + ".</p>") if _src_links else ""
    _body = (f'<style>.bt{{columns:1}}main h2{{margin-top:1.8em}}.rd-top{{margin:14px 0}}{_toc_css}.rv-badge{{display:inline-block;font:600 12px \'Be Vietnam Pro\',system-ui,sans-serif;padding:3px 10px;border-radius:999px;background:#d9a41e22;color:var(--mut);border:1px solid var(--line);vertical-align:middle}}.rv-badge.rv-reviewed{{background:#2e7d3222;color:#2e7d32}}.rv-badge.rv-in-review{{background:#7c212822;color:var(--acc)}}</style>'
             f'<h1>{E(_dt)}</h1>{_au_line}{_rt_line}{_label}{_rep_line}{_src_line}' +
             f'<p class="rd-top"><a class="btn primary" href="{_rd}">📖 Đọc trong trình đọc</a> <a class="btn s" id="rv-resume" href="{_rd}" hidden>▶ Tiếp tục đọc</a></p>{_resume_js}' +
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
    _ttl_dt = _OVR.get(_slug, _dt)  # Phase 1.6: tier-2 shortened title (title tag only; the h1 keeps the full title)
    _ttl = f'{_ttl_dt} · bản dịch tiếng Việt | Reformed Vietnam'
    if len(_ttl) > 60:  # tier-1 (2026-11-10): drop the site suffix when it alone brings the title to <=60 chars
        _ttl = f'{_ttl_dt} · bản dịch tiếng Việt'
    open(_path, "w", encoding="utf-8").write(page(_ttl, f'Bản dịch tiếng Việt "{_dt}" của {_au}. Miễn phí.', _path, _body, _ld))
    urls.append(_path)
    VIBOOKS[_b["id"]] = {"u": "/" + _path, "by": _by, "r": _rev, "rs": _rstat, "words": _words, "mins": _mins, "rd": f"reader.html?id=vn/{_slug}&pid=" + _ul.quote(_b["id"], safe="")}
    _hub.append((_bt, _au, _orig, "/" + _path, _rev, _orig_book, _rstat))
open("vi-books.json", "w", encoding="utf-8").write(_j.dumps(VIBOOKS, ensure_ascii=False))
# Batch C: the live index has entries with no 'file' key; they are skipped, not fatal.
if _nofile:
    print("vi_books: skipped %d index entries without 'file': %s" % (len(_nofile), ", ".join(_nofile[:10])))

_li = lambda x: bcard(x[0], x[1], x[3], badge=_RSTATUS.get(x[6], _RSTATUS["ai-draft"]), kicker=x[2] or "Bản dịch")
_tr = "".join(_li(x) for x in _hub if not x[5]); _nw = "".join(_li(x) for x in _hub if x[5])
# Phase 3.6: "Moi them gan day" from tools/recent-books.json (git-derived
# dates; absent file = no block, safe default). Top 8, newest first.
_RECENT = _j.load(open("tools/recent-books.json", encoding="utf-8"))["books"][:8] if _o.path.exists("tools/recent-books.json") else []
_recent_html = ""
if _RECENT:
    _recent_html = ('<h2>Mới thêm gần đây</h2><p class="m">Ngày thêm là ngày sách xuất hiện trong thư viện (theo lịch sử kho mã). '
                    'Xem <a href="/moi-cap-nhat.html">Mới cập nhật</a> để biết các thay đổi khác của trang.</p><ul>' +
                    "".join(f'<li><a href="/ban-dich/{b["slug"]}.html">{E(b["title"])}</a> — {E(b["author"])} <span class="m">· thêm ngày {_vn_date(b["date"])}</span></li>' for b in _RECENT) + '</ul>')
_hb = ('<h1>Bản dịch và sách mới</h1><p class="dr" style="padding:.6em .9em;border-radius:8px;background:#d9a41e22">Các sách dưới đây do AI hỗ trợ dịch hoặc soạn và <b>chưa được mục sư duyệt giáo lý</b>. Hãy đối chiếu Kinh Thánh và hỏi mục sư của bạn.</p>' + _recent_html
       + (f'<h2>Bản dịch tiếng Việt</h2>' + bkgrid(_tr) if _tr else '') + (f'<h2>Sách mới (tác giả David)</h2>' + bkgrid(_nw) if _nw else '') + '<p><a class="btn primary" href="/">Về thư viện</a></p>')
if _hub:
    open("ban-dich/index.html", "w", encoding="utf-8").write(page("Bản dịch và sách mới | Reformed Vietnam", "Các bản dịch tiếng Việt và sách mới do AI hỗ trợ, chưa duyệt giáo lý. Miễn phí.", "ban-dich/index.html", _hb))
    urls.append("ban-dich/index.html")

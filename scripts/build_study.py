#!/usr/bin/env python3
"""Phase 4 — Study depth (Nghiên cứu Kinh Thánh).

Builds, from data already in the repo (no invented content):

  4.1  /nhan-vat/<id>.html x50 + /nhan-vat/ index
       from data/nhanvat.json (copy of the Bible app's data/nhanvat.json).
       Bio + verse notes are used VERBATIM; each verse also shows the
       1934 verse text (from the Bible app's data/bible/*.json) and links
       to /kinh-thanh/<bid>/<ch>.html#v<v>.
  4.2  /chu-de-kinh-thanh/<id>.html x20 + /chu-de-kinh-thanh/ index
       from data/topics.json (copy of the Bible app's data/topics.json).
       Same pattern: intro + verses verbatim, 1934 text embedded.
       NOTE: /chu-de/ is the LEGACY book-topic index (13 book lists) and
       must not be touched — hence the separate -kinh-thanh namespace.
       Where a topic id matches a legacy book-topic slug (cau-nguyen),
       the topic page links to the legacy book list as well.
  4.3  /kinh-thanh/gioi-thieu/<bid>.html x66 + index
       Derived ONLY from data already in the repo: chapter counts and
       verse counts from the Bible app's books.json, per-chapter summaries
       and themes from data/chapter-summaries.json (labelled AI-drafted),
       plus character/topic cross-links derived from their verse keys.
       No authorship/date scholarship is asserted anywhere.
  4.4  /dong-thoi-gian-kinh-thanh.html — Bible timeline from
       scripts/helper-data/bible-timeline.json: only dates with a solid
       scholarly consensus; every pre-1000 TCN date is marked "khoảng";
       Creation, the Flood, Babel and Paul's conversion date are omitted
       (no absolute dates), and the Exodus-date debate is footnoted.
       /ban-do-kinh-thanh.html — the Bible app's 5 watercolour maps
       (img/ban-do/*.jpg, copied from the Bible app), with the app's
       titles/descriptions verbatim and 1934 verse texts. The maps are
       artistic illustrations, not scale-accurate charts (stated on page).
  Hub  /nghien-cuu-kinh-thanh.html — links the four sections above to
       each other and to the existing study tools (reader, devotions,
       catechism, reading plans, answers, encyclopedia, Academy).

All AI-drafted prose carries "Nội dung AI soạn, chưa duyệt". Verse text
is the 1934 text verbatim. Follows the hub_page.py builder pattern
(Phase 2): head/header/footer from hub.html, check_links on every
page, sitemap_add at the end. Search entries are added by
scripts/build_search.py (Phase 4 section) — re-run it after this.
"""
import html
import json
import pathlib
import re
import sys
from collections import Counter

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from hub_page import (BASE, ROOT, head, header, footer, MINI_JS, share_row,
                      report_mailto, write_if_changed, check_links, sitemap_add)

APP = ROOT.parent / "bible-app"

BOOKS = json.loads((APP / "data/books.json").read_text(encoding="utf-8"))
NAMES = {b["id"]: b["name"] for b in BOOKS}
NAMES_REV = {b["name"]: b["id"] for b in BOOKS}
TESTAMENT = {b["id"]: ("Cựu Ước" if b["t"] == "old" else "Tân Ước") for b in BOOKS}
NCH = {b["id"]: len(b["nc"]) for b in BOOKS}
NVER = {b["id"]: sum(b["nc"]) for b in BOOKS}
ORDER = [b["id"] for b in BOOKS]

NV = json.loads((ROOT / "data/nhanvat.json").read_text(encoding="utf-8"))
TP = json.loads((ROOT / "data/topics.json").read_text(encoding="utf-8"))
SUMS = json.loads((ROOT / "data/chapter-summaries.json").read_text(encoding="utf-8"))["entries"]
TIMELINE = json.loads((ROOT / "scripts/helper-data/bible-timeline.json").read_text(encoding="utf-8"))

LEGACY_BOOK_TOPICS = ["an-dien-tin-lanh", "ba-ngoi", "cau-nguyen", "chua-christ",
                      "duc-thanh-linh", "giao-uoc", "hoi-thanh", "kinh-thanh",
                      "lich-su-cai-chanh", "muc-vu-giang-dao", "nen-thanh",
                      "tien-dinh", "xung-cong-binh"]

MAPS = [
    {"id": "exodus", "title": "Hành trình Xuất Hành",
     "desc": "Từ Ai Cập qua Biển Đỏ, lang thang 40 năm trong đồng vắng Si-nai, đến bờ sông Giô-đanh trước Đất Hứa.",
     "verses": ["exo:14:21", "exo:14:22", "num:33:1"]},
    {"id": "conquest", "title": "Đất Ca-na-an",
     "desc": "Mười hai chi phái nhận phần đất thừa hưởng — từ sông Giô-đanh đến Địa Trung Hải, từ đồng bằng đến đồi núi.",
     "verses": ["jos:1:3", "jos:21:43"]},
    {"id": "galilee", "title": "Chức vụ tại Ga-li-lê",
     "desc": "Biển Ga-li-lê, Ca-bê-na-um, Na-xa-rét — nơi Chúa Giê-xu giảng dạy, chữa lành và kêu gọi môn đồ.",
     "verses": ["mat:4:23", "luk:5:1"]},
    {"id": "paul", "title": "Các hành trình của Phao-lô",
     "desc": "Từ An-ti-ốt qua Tiểu Á, Ma-xê-đoan, Hy Lạp đến Rô-ma — Phúc Âm lan ra khắp thế giới ngoại giáo.",
     "verses": ["act:13:2", "act:16:9", "rom:15:24"]},
    {"id": "jerusalem", "title": "Giê-ru-sa-lem thời Chúa Giê-xu",
     "desc": "Thành thánh trên đồi, đền thờ nguy nga, thung lũng Xết-rôn — bối cảnh tuần lễ thương khó và sự phục sinh.",
     "verses": ["luk:19:41", "mat:21:12"]},
]

_bible_cache = {}
PAGES = []  # (path, html, label) — written first, link-checked last


def queue_page(path, html_text, label):
    PAGES.append((pathlib.Path(path), html_text, label))


def esc(s):
    return html.escape(str(s or ""), quote=True)


def verse_text(key):
    """1934 verse text for a 'bid:ch:v' key; fails loudly if it is missing."""
    bid, ch, v = key.split(":")
    ch, v = int(ch), int(v)
    if bid not in _bible_cache:
        _bible_cache[bid] = json.loads((APP / f"data/bible/{bid}.json").read_text(encoding="utf-8"))["ch"]
    chs = _bible_cache[bid]
    assert 1 <= ch <= len(chs), f"chapter out of range: {key}"
    assert 1 <= v <= len(chs[ch - 1]), f"verse out of range: {key}"
    return chs[ch - 1][v - 1]


def verse_url(key):
    bid, ch, v = key.split(":")
    return f"/kinh-thanh/{bid}/{ch}.html#v{v}"


def verse_block(v):
    """One verse: linked ref + 1934 text + the data file's note (verbatim)."""
    note = f'<p class="v-note">{esc(v.get("note", ""))}</p>' if v.get("note") else ""
    return (f'<div class="verse"><a class="v-ref" href="{verse_url(v["key"])}">{esc(v["ref"])}</a>'
            f'<p class="v-text">“{esc(verse_text(v["key"]))}”</p>{note}</div>')


def book_links(keys):
    """Distinct book-intro links for a list of verse keys, in first-seen order."""
    seen = []
    for k in keys:
        bid = k.split(":")[0]
        if bid not in seen:
            seen.append(bid)
    return "".join(f'<a class="btn" href="/kinh-thanh/gioi-thieu/{b}.html">{esc(NAMES[b])}</a> ' for b in seen)


def prev_next(items, i, base, label):
    out = ""
    if i > 0:
        p = items[i - 1]
        out += f'<a class="btn" href="{base}/{p["id"]}.html">← {esc(p.get("name") or p.get("title"))}</a> '
    if i < len(items) - 1:
        n = items[i + 1]
        out += f'<a class="btn" href="{base}/{n["id"]}.html">{esc(n.get("name") or n.get("title"))} →</a>'
    return f'<p style="text-align:center;margin-top:26px">{out}</p>' if out else ""


def page(title, desc, url, body, extra_css=""):
    p = f"""{head(title, desc, url, extra_css)}
<body id="top">
{header}
<main class="wrap">
{body}
</main>
{footer}
{MINI_JS}
</body>
</html>"""
    return p


CSS = """
      .verse { border-bottom: 1px solid var(--line); padding: 12px 2px; }
      .verse .v-ref { color: var(--gold-text); font-weight: 700; }
      .verse .v-text { font-family: "Noto Serif", serif; margin: 6px 0; line-height: 1.65; }
      .verse .v-note { color: var(--ink-soft); font-size: 14px; margin: 0; line-height: 1.6; }
      .idx-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 12px; max-width: 900px; margin: 20px auto; }
      .idx-card { display: block; background: var(--surface); border: 1px solid var(--line); border-radius: var(--radius); padding: 14px 18px; box-shadow: var(--shadow); text-decoration: none; }
      .idx-card h3 { font-family: "Noto Serif", serif; font-size: 16.5px; margin: 0 0 4px; color: var(--ink); line-height: 1.45; }
      .idx-card p { margin: 0; color: var(--ink-soft); font-size: 13.5px; line-height: 1.55; }
      .idx-card:hover h3 { color: var(--burgundy); }
      .ch-table { width: 100%; border-collapse: collapse; max-width: 900px; margin: 18px auto; font-size: 14.5px; }
      .ch-table th, .ch-table td { text-align: left; padding: 8px 10px; border-bottom: 1px solid var(--line); vertical-align: top; line-height: 1.55; }
      .ch-table th { font-size: 12.5px; letter-spacing: .06em; text-transform: uppercase; color: var(--gold-text); }
      .ch-table td.cnum { font-family: "Playfair Display", serif; font-weight: 700; white-space: nowrap; }
      .ch-table td a { color: var(--gold-text); }
      .map-img { width: 100%; border-radius: 12px; border: 1px solid var(--line); display: block; }
      .map-card { max-width: 860px; margin: 28px auto 0; }
      .map-card h2 { font-family: "Playfair Display", serif; font-size: 23px; margin: 0 0 8px; }
      .map-card p { color: var(--ink-soft); }
      .era { max-width: 860px; margin: 28px auto 0; }
      .era h2 { font-family: "Playfair Display", serif; font-size: 23px; margin: 0 0 4px; border-bottom: 2px solid var(--gold-soft); padding-bottom: 6px; }
      .tl-item { display: flex; gap: 16px; padding: 14px 0; border-bottom: 1px solid var(--line); }
      .tl-year { flex: 0 0 110px; font-family: "Playfair Display", serif; font-weight: 700; font-size: 16px; color: var(--gold-text); }
      .tl-item h3 { font-size: 16.5px; margin: 0 0 4px; }
      .tl-item p { margin: 0 0 6px; color: var(--ink-soft); }
      .tl-item ul { margin: 0; padding-left: 18px; }
      .tl-item li { margin: 3px 0; }
      .tl-item li a { color: var(--gold-text); }
      @media (max-width: 640px) { .tl-year { flex-basis: 88px; font-size: 14px; } }
      .hub-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 14px; max-width: 900px; margin: 20px auto; }
"""

AI_NOTE = ('<p style="text-align:center;margin-top:14px"><span class="ai-label">'
           'Nội dung AI soạn, chưa duyệt</span></p>')


def top_themes(bid):
    c = Counter()
    for ch in range(1, NCH[bid] + 1):
        c.update(SUMS[f"{bid}:{ch}"].get("themes") or [])
    return [t for t, _ in sorted(c.items(), key=lambda kv: (-kv[1], kv[0]))[:5]]


def key_verse_url(ref):
    """'Sáng Thế Ký 1:27' -> /kinh-thanh/gen/1.html#v27 (chapter page if unparsable)."""
    m = re.match(r"^(.+?) (\d+):(\d+)$", ref.strip())
    if not m:
        return None
    bid = NAMES_REV.get(m.group(1))
    if not bid:
        return None
    return f"/kinh-thanh/{bid}/{m.group(2)}.html#v{m.group(3)}"


def build_characters():
    assert len(NV) == 50, f"expected 50 characters, got {len(NV)}"
    urls = []
    for i, e in enumerate(NV):
        verses = "".join(verse_block(v) for v in e["verses"])
        books = book_links([v["key"] for v in e["verses"]])
        url = f"{BASE}/nhan-vat/{e['id']}.html"
        body = f"""  <p class="crumb"><a href="/">Trang chủ</a> · <a href="/nhan-vat/">Nhân vật Kinh Thánh</a></p>
  <div class="cat-head">
    <div class="kicker">Nhân vật Kinh Thánh</div>
    <h1>{esc(e['name'])}</h1>
  </div>
{AI_NOTE}
  <div class="cat-band"><p style="color:var(--ink);font-size:16.5px;line-height:1.75">{esc(e['bio'])}</p></div>
  <div class="cat-band"><div class="cat-band-head"><h3>Các câu Kinh Thánh</h3><span class="rng">{len(e['verses'])} câu · Bản 1934</span></div>
{verses}</div>
  <div class="cat-band"><div class="cat-band-head"><h3>Xuất hiện trong các sách</h3></div>
  <p>{books}</p></div>
{prev_next(NV, i, "/nhan-vat", "name")}
  <p style="text-align:center;margin-top:26px"><a class="btn" href="/nhan-vat/">Tất cả 50 nhân vật</a> <a class="btn" href="/nghien-cuu-kinh-thanh.html">Nghiên cứu Kinh Thánh</a></p>
  {share_row(url)}
  {report_mailto(e['name'] + " — Nhân vật Kinh Thánh")}"""
        p = page(f"{e['name']} — Nhân vật Kinh Thánh | Reformed Vietnam",
                 f"{e['name']}: {e['bio'][:140]}", url, body, CSS)
        queue_page(ROOT / f"nhan-vat/{e['id']}.html", p, f"/nhan-vat/{e['id']}.html")
        urls.append(f"/nhan-vat/{e['id']}.html")
    cards = "".join(
        f'<a class="idx-card" href="/nhan-vat/{e["id"]}.html"><h3>{esc(e["name"])}</h3>'
        f'<p>{esc(e["bio"][:120])}…</p></a>' for e in NV)
    url = f"{BASE}/nhan-vat/"
    body = f"""  <p class="crumb"><a href="/">Trang chủ</a> · <a href="/nghien-cuu-kinh-thanh.html">Nghiên cứu Kinh Thánh</a></p>
  <div class="cat-head">
    <div class="kicker">Nghiên cứu Kinh Thánh</div>
    <h1>Nhân vật Kinh Thánh</h1>
    <p style="max-width:640px;margin:0 auto;color:var(--ink-soft)">50 nhân vật — từ A-đam đến Giu-đa — mỗi người với tiểu sử ngắn và những câu Kinh Thánh then chốt, trích bản 1934. Thứ tự theo dòng thời gian Kinh Thánh.</p>
  </div>
{AI_NOTE}
  <div class="idx-grid">{cards}</div>
  <p style="text-align:center;margin-top:26px"><a class="btn" href="/nghien-cuu-kinh-thanh.html">Nghiên cứu Kinh Thánh</a></p>
  {share_row(url)}
  {report_mailto("Nhân vật Kinh Thánh")}"""
    p = page("Nhân vật Kinh Thánh — 50 nhân vật | Reformed Vietnam",
             "50 nhân vật Kinh Thánh, từ A-đam đến Giu-đa: tiểu sử ngắn và những câu Kinh Thánh then chốt theo bản 1934.", url, body, CSS)
    queue_page(ROOT / "nhan-vat/index.html", p, "/nhan-vat/")
    urls.append("/nhan-vat/")
    print(f"  characters: {len(NV)} pages + index")
    return urls


def build_topics():
    assert len(TP) == 20, f"expected 20 topics, got {len(TP)}"
    urls = []
    for i, e in enumerate(TP):
        verses = "".join(verse_block(v) for v in e["verses"])
        books = book_links([v["key"] for v in e["verses"]])
        legacy = (f'<p><a class="btn" href="/chu-de/{e["id"]}.html">Sách về {esc(e["title"])} →</a></p>'
                  if e["id"] in LEGACY_BOOK_TOPICS else "")
        url = f"{BASE}/chu-de-kinh-thanh/{e['id']}.html"
        body = f"""  <p class="crumb"><a href="/">Trang chủ</a> · <a href="/chu-de-kinh-thanh/">Chủ đề Kinh Thánh</a></p>
  <div class="cat-head">
    <div class="kicker">Chủ đề Kinh Thánh</div>
    <h1>{esc(e['title'])}</h1>
  </div>
{AI_NOTE}
  <div class="cat-band"><p style="color:var(--ink);font-size:16.5px;line-height:1.75">{esc(e['intro'])}</p></div>
  <div class="cat-band"><div class="cat-band-head"><h3>Các câu Kinh Thánh</h3><span class="rng">{len(e['verses'])} câu · Bản 1934</span></div>
{verses}</div>
  <div class="cat-band"><div class="cat-band-head"><h3>Các sách liên quan</h3></div>
  <p>{books}</p>{legacy}</div>
{prev_next(TP, i, "/chu-de-kinh-thanh", "title")}
  <p style="text-align:center;margin-top:26px"><a class="btn" href="/chu-de-kinh-thanh/">Tất cả 20 chủ đề</a> <a class="btn" href="/nghien-cuu-kinh-thanh.html">Nghiên cứu Kinh Thánh</a></p>
  {share_row(url)}
  {report_mailto(e['title'] + " — Chủ đề Kinh Thánh")}"""
        p = page(f"{e['title']} — Chủ đề Kinh Thánh | Reformed Vietnam",
                 f"{e['title']}: {e['intro'][:140]}", url, body, CSS)
        queue_page(ROOT / f"chu-de-kinh-thanh/{e['id']}.html", p, f"/chu-de-kinh-thanh/{e['id']}.html")
        urls.append(f"/chu-de-kinh-thanh/{e['id']}.html")
    # Groups are derived from the id prefix: sola-* (Five Solas),
    # tulip-* (Five Points), the rest are Christian-life topics.
    groups = [("Năm Sola", [e for e in TP if e["id"].startswith("sola")]),
              ("Năm Điểm TULIP", [e for e in TP if e["id"].startswith("tulip-")]),
              ("Đời sống Cơ Đốc", [e for e in TP if not e["id"].startswith(("sola", "tulip-"))])]
    sections = ""
    for gtitle, items in groups:
        cards = "".join(
            f'<a class="idx-card" href="/chu-de-kinh-thanh/{e["id"]}.html"><h3>{esc(e["title"])}</h3>'
            f'<p>{esc(e["intro"][:120])}…</p></a>' for e in items)
        sections += (f'<div class="cat-band"><div class="cat-band-head"><h3>{gtitle}</h3>'
                     f'<span class="rng">{len(items)} chủ đề</span></div></div>'
                     f'<div class="idx-grid">{cards}</div>')
    url = f"{BASE}/chu-de-kinh-thanh/"
    body = f"""  <p class="crumb"><a href="/">Trang chủ</a> · <a href="/nghien-cuu-kinh-thanh.html">Nghiên cứu Kinh Thánh</a></p>
  <div class="cat-head">
    <div class="kicker">Nghiên cứu Kinh Thánh</div>
    <h1>Chủ đề Kinh Thánh</h1>
    <p style="max-width:640px;margin:0 auto;color:var(--ink-soft)">20 chủ đề — Năm Sola, Năm Điểm TULIP và đời sống Cơ Đốc — mỗi chủ đề với phần giới thiệu ngắn và các câu Kinh Thánh then chốt, trích bản 1934.</p>
  </div>
{AI_NOTE}
{sections}
  <div class="band-tint"><h2 class="bt-head">Sách theo chủ đề</h2>
  <p style="color:var(--ink-soft);margin:0">Muốn đọc sách về một chủ đề? Thư viện có 13 chuyên mục sách theo chủ đề — ân điển, Ba Ngôi, cầu nguyện, Hội Thánh và nhiều hơn — tại <a href="/chu-de/">Học theo chủ đề</a>.</p></div>
  <p style="text-align:center;margin-top:26px"><a class="btn" href="/nghien-cuu-kinh-thanh.html">Nghiên cứu Kinh Thánh</a></p>
  {share_row(url)}
  {report_mailto("Chủ đề Kinh Thánh")}"""
    p = page("Chủ đề Kinh Thánh — 20 chủ đề | Reformed Vietnam",
             "20 chủ đề Kinh Thánh: Năm Sola, Năm Điểm TULIP và đời sống Cơ Đốc, với các câu Kinh Thánh then chốt theo bản 1934.", url, body, CSS)
    queue_page(ROOT / "chu-de-kinh-thanh/index.html", p, "/chu-de-kinh-thanh/")
    urls.append("/chu-de-kinh-thanh/")
    print(f"  topics: {len(TP)} pages + index")
    return urls


def build_book_intros():
    urls = []
    for idx, bid in enumerate(ORDER):
        name = NAMES[bid]
        themes = top_themes(bid)
        rows = ""
        for ch in range(1, NCH[bid] + 1):
            s = SUMS[f"{bid}:{ch}"]
            kv = s.get("key_verse_ref", "")
            kv_url = key_verse_url(kv)
            kv_html = (f'<a href="{kv_url}">{esc(kv)}</a>' if kv_url else esc(kv))
            rows += (f'<tr><td class="cnum"><a href="/kinh-thanh/{bid}/{ch}.html">Chương {ch}</a></td>'
                     f'<td>{esc(s.get("summary_vi", ""))}</td><td>{kv_html}</td></tr>')
        chars_here = [e for e in NV if any(v["key"].split(":")[0] == bid for v in e["verses"])]
        topics_here = [e for e in TP if any(v["key"].split(":")[0] == bid for v in e["verses"])]
        char_links = "".join(f'<a class="btn" href="/nhan-vat/{e["id"]}.html">{esc(e["name"])}</a> ' for e in chars_here)
        topic_links = "".join(f'<a class="btn" href="/chu-de-kinh-thanh/{e["id"]}.html">{esc(e["title"])}</a> ' for e in topics_here)
        prev_b = f'<a class="btn" href="/kinh-thanh/gioi-thieu/{ORDER[idx - 1]}.html">← {esc(NAMES[ORDER[idx - 1]])}</a> ' if idx > 0 else ""
        next_b = f'<a class="btn" href="/kinh-thanh/gioi-thieu/{ORDER[idx + 1]}.html">{esc(NAMES[ORDER[idx + 1]])} →</a>' if idx < len(ORDER) - 1 else ""
        url = f"{BASE}/kinh-thanh/gioi-thieu/{bid}.html"
        body = f"""  <p class="crumb"><a href="/">Trang chủ</a> · <a href="/kinh-thanh/gioi-thieu/">Giới thiệu các sách Kinh Thánh</a> · <a href="/kinh-thanh/{bid}/1.html">Đọc {esc(name)}</a></p>
  <div class="cat-head">
    <div class="kicker">Giới thiệu sách · {TESTAMENT[bid]}</div>
    <h1>{esc(name)}</h1>
    <p style="max-width:640px;margin:0 auto;color:var(--ink-soft)">{NCH[bid]} chương · {NVER[bid]} câu · Chủ đề chính: {esc(" · ".join(themes))}</p>
  </div>
{AI_NOTE}
  <p style="text-align:center;margin-top:16px"><a class="btn solid" href="/kinh-thanh/{bid}/1.html">Đọc {esc(name)} 1 →</a></p>
  <div class="cat-band"><div class="cat-band-head"><h3>Tóm tắt từng chương</h3><span class="rng">{NCH[bid]} chương</span></div>
  <p>Tóm tắt ngắn từng chương và câu then chốt — giúp nắm toàn cảnh sách trước khi đọc. Câu then chốt dẫn tới đúng câu trong bản 1934.</p></div>
  <table class="ch-table"><tr><th>Chương</th><th>Tóm tắt</th><th>Câu then chốt</th></tr>
{rows}</table>
  <div class="cat-band"><div class="cat-band-head"><h3>Nhân vật trong sách này</h3></div>
  <p>{char_links or "—"}</p></div>
  <div class="cat-band"><div class="cat-band-head"><h3>Chủ đề liên quan</h3></div>
  <p>{topic_links or "—"}</p></div>
  <p style="text-align:center;margin-top:26px">{prev_b}{next_b}</p>
  <p style="text-align:center;margin-top:26px"><a class="btn" href="/kinh-thanh/gioi-thieu/">Tất cả 66 sách</a> <a class="btn" href="/nghien-cuu-kinh-thanh.html">Nghiên cứu Kinh Thánh</a></p>
  {share_row(url)}
  {report_mailto("Giới thiệu sách " + name)}"""
        p = page(f"Giới thiệu sách {name} — {NCH[bid]} chương | Reformed Vietnam",
                 f"Giới thiệu sách {name} ({TESTAMENT[bid]}): {NCH[bid]} chương, {NVER[bid]} câu, tóm tắt từng chương và câu then chốt theo bản 1934.", url, body, CSS)
        queue_page(ROOT / f"kinh-thanh/gioi-thieu/{bid}.html", p, f"/kinh-thanh/gioi-thieu/{bid}.html")
        urls.append(f"/kinh-thanh/gioi-thieu/{bid}.html")
    # index
    sections = ""
    for tname, bids in [("Cựu Ước", [b for b in ORDER if TESTAMENT[b] == "Cựu Ước"]),
                        ("Tân Ước", [b for b in ORDER if TESTAMENT[b] == "Tân Ước"])]:
        cards = "".join(
            f'<a class="idx-card" href="/kinh-thanh/gioi-thieu/{b}.html"><h3>{esc(NAMES[b])}</h3>'
            f'<p>{NCH[b]} chương · {NVER[b]} câu · {esc(" · ".join(top_themes(b)[:3]))}</p></a>' for b in bids)
        sections += (f'<div class="cat-band"><div class="cat-band-head"><h3>{tname}</h3>'
                     f'<span class="rng">{len(bids)} sách</span></div></div>'
                     f'<div class="idx-grid">{cards}</div>')
    url = f"{BASE}/kinh-thanh/gioi-thieu/"
    body = f"""  <p class="crumb"><a href="/">Trang chủ</a> · <a href="/nghien-cuu-kinh-thanh.html">Nghiên cứu Kinh Thánh</a></p>
  <div class="cat-head">
    <div class="kicker">Nghiên cứu Kinh Thánh</div>
    <h1>Giới thiệu các sách Kinh Thánh</h1>
    <p style="max-width:640px;margin:0 auto;color:var(--ink-soft)">66 sách, mỗi sách một trang giới thiệu: số chương, số câu, chủ đề chính, tóm tắt từng chương và câu then chốt — tất cả dẫn tới bản Kinh Thánh 1934.</p>
  </div>
{AI_NOTE}
{sections}
  <p style="text-align:center;margin-top:26px"><a class="btn" href="/nghien-cuu-kinh-thanh.html">Nghiên cứu Kinh Thánh</a></p>
  {share_row(url)}
  {report_mailto("Giới thiệu các sách Kinh Thánh")}"""
    p = page("Giới thiệu các sách Kinh Thánh — 66 sách | Reformed Vietnam",
             "Giới thiệu 66 sách Kinh Thánh: số chương, số câu, chủ đề chính, tóm tắt từng chương và câu then chốt theo bản 1934.", url, body, CSS)
    queue_page(ROOT / "kinh-thanh/gioi-thieu/index.html", p, "/kinh-thanh/gioi-thieu/")
    urls.append("/kinh-thanh/gioi-thieu/")
    print(f"  book intros: {len(ORDER)} pages + index")
    return urls


def build_timeline():
    n = 0
    eras = ""
    for era in TIMELINE["eras"]:
        items = ""
        for e in era["entries"]:
            n += 1
            links = ""
            if e.get("links"):
                lis = "".join(f'<li><a href="{l["url"]}">{esc(l["label"])}</a></li>' for l in e["links"])
                links = f"<ul>{lis}</ul>"
            items += (f'<div class="tl-item"><div class="tl-year">{esc(e["year"])}</div>'
                      f'<div><h3>{esc(e["title"])}</h3><p>{esc(e["note"])}</p>{links}</div></div>')
        eras += f'<section class="era"><h2>{esc(era["title"])}</h2>{items}</section>'
    url = f"{BASE}/dong-thoi-gian-kinh-thanh.html"
    body = f"""  <p class="crumb"><a href="/">Trang chủ</a> · <a href="/nghien-cuu-kinh-thanh.html">Nghiên cứu Kinh Thánh</a></p>
  <div class="cat-head">
    <div class="kicker">Nghiên cứu Kinh Thánh</div>
    <h1>Dòng thời gian Kinh Thánh</h1>
    <p style="max-width:640px;margin:0 auto;color:var(--ink-soft)">Từ lời kêu gọi Áp-ra-ham đến sách Khải Huyền — những mốc lớn của lịch sử cứu rỗi, mỗi mốc đều dẫn tới đúng chương Kinh Thánh 1934. Niên đại ghi 'khoảng' là ước tính theo niên đại truyền thống, không phải ngày chính xác tuyệt đối.</p>
  </div>
{AI_NOTE}
{eras}
  <div class="band-tint"><h2 class="bt-head">Về độ chính xác</h2>
  <p style="color:var(--ink-soft);margin:0">{esc(TIMELINE['note'])} Nếu bạn phát hiện sai sót, xin báo cho chúng tôi.</p></div>
  <p style="text-align:center;margin-top:26px"><a class="btn" href="/ban-do-kinh-thanh.html">Bản đồ &amp; hành trình →</a> <a class="btn" href="/nghien-cuu-kinh-thanh.html">Nghiên cứu Kinh Thánh</a></p>
  {share_row(url)}
  {report_mailto("Dòng thời gian Kinh Thánh")}"""
    p = page("Dòng thời gian Kinh Thánh | Reformed Vietnam",
             "Dòng thời gian Kinh Thánh: từ Áp-ra-ham đến Khải Huyền — các mốc lớn của lịch sử cứu rỗi, dẫn tới Kinh Thánh 1934.", url, body, CSS)
    queue_page(ROOT / "dong-thoi-gian-kinh-thanh.html", p, "/dong-thoi-gian-kinh-thanh.html")
    print(f"  bible timeline: {n} entries")
    return ["/dong-thoi-gian-kinh-thanh.html"]


def build_maps():
    sections = ""
    for m in MAPS:
        verses = "".join(verse_block({"key": k, "ref": _ref_for(k), "note": ""}) for k in m["verses"])
        sections += (f'<section class="map-card"><h2>{esc(m["title"])}</h2>'
                     f'<img class="map-img" src="/img/ban-do/{m["id"]}.jpg" alt="{esc(m["title"])}" loading="lazy">'
                     f'<p>{esc(m["desc"])}</p>{verses}</section>')
    url = f"{BASE}/ban-do-kinh-thanh.html"
    body = f"""  <p class="crumb"><a href="/">Trang chủ</a> · <a href="/nghien-cuu-kinh-thanh.html">Nghiên cứu Kinh Thánh</a></p>
  <div class="cat-head">
    <div class="kicker">Nghiên cứu Kinh Thánh</div>
    <h1>Bản đồ &amp; hành trình Kinh Thánh</h1>
    <p style="max-width:640px;margin:0 auto;color:var(--ink-soft)">Địa lý Kinh Thánh qua tranh màu nước: hành trình Xuất Hành, Đất Ca-na-an, chức vụ tại Ga-li-lê, các hành trình của Phao-lô và Giê-ru-sa-lem thời Chúa Giê-xu — mỗi bản đồ kèm những câu Kinh Thánh 1934 liên quan.</p>
  </div>
{AI_NOTE}
{sections}
  <div class="band-tint"><h2 class="bt-head">Lưu ý về các bản đồ</h2>
  <p style="color:var(--ink-soft);margin:0">Các hình trên đây là tranh minh họa theo phong cách màu nước, vẽ lại hành trình và địa danh một cách ước lệ — không phải bản đồ đo đạc theo tỷ lệ. Vị trí tương đối giữa các địa danh là đúng đại thể; để tra cứu chính xác, xin đối chiếu với một atlas Kinh Thánh.</p></div>
  <p style="text-align:center;margin-top:26px"><a class="btn" href="/dong-thoi-gian-kinh-thanh.html">Dòng thời gian Kinh Thánh →</a> <a class="btn" href="/nghien-cuu-kinh-thanh.html">Nghiên cứu Kinh Thánh</a></p>
  {share_row(url)}
  {report_mailto("Bản đồ Kinh Thánh")}"""
    p = page("Bản đồ & hành trình Kinh Thánh | Reformed Vietnam",
             "Bản đồ Kinh Thánh qua tranh màu nước: Xuất Hành, Đất Ca-na-an, Ga-li-lê, các hành trình của Phao-lô và Giê-ru-sa-lem — kèm câu Kinh Thánh 1934.", url, body, CSS)
    queue_page(ROOT / "ban-do-kinh-thanh.html", p, "/ban-do-kinh-thanh.html")
    print("  maps: 5 maps on 1 page")
    return ["/ban-do-kinh-thanh.html"]


def _ref_for(key):
    bid, ch, v = key.split(":")
    return f"{NAMES[bid]} {ch}:{v}"


def build_hub():
    url = f"{BASE}/nghien-cuu-kinh-thanh.html"
    cards = [
        ("/nhan-vat/", "Nhân vật Kinh Thánh", "50 nhân vật, từ A-đam đến Giu-đa — tiểu sử ngắn và các câu Kinh Thánh then chốt."),
        ("/chu-de-kinh-thanh/", "Chủ đề Kinh Thánh", "20 chủ đề: Năm Sola, Năm Điểm TULIP và đời sống Cơ Đốc, với các câu Kinh Thánh then chốt."),
        ("/kinh-thanh/gioi-thieu/", "Giới thiệu các sách", "66 sách: số chương, số câu, chủ đề chính, tóm tắt từng chương và câu then chốt."),
        ("/dong-thoi-gian-kinh-thanh.html", "Dòng thời gian", "Từ Áp-ra-ham đến Khải Huyền — các mốc lớn của lịch sử cứu rỗi, dẫn tới Kinh Thánh 1934."),
        ("/ban-do-kinh-thanh.html", "Bản đồ & hành trình", "Địa lý Kinh Thánh qua tranh màu nước: Xuất Hành, Ca-na-an, Ga-li-lê, Phao-lô, Giê-ru-sa-lem."),
    ]
    grid = "".join(
        f'<a class="idx-card" href="{u}"><h3>{t}</h3><p>{d}</p></a>' for u, t, d in cards)
    tools = [
        ("/kinh-thanh/", "Đọc Kinh Thánh 1934", "Trọn 66 sách, 31.102 câu, tham chiếu chéo."),
        ("/suy-ngam/", "Tĩnh nguyện mỗi ngày", "366 bài của Spurgeon — Ân Điển Mỗi Ngày."),
        ("/giao-ly/", "Giáo lý vấn đáp", "107 câu hỏi đáp Westminster ngắn, kèm câu Kinh Thánh."),
        ("/ke-hoach-doc.html", "Kế hoạch đọc Kinh Thánh", "Đọc trọn Kinh Thánh theo kế hoạch cả năm."),
        ("/hoi-dap/", "Hỏi Đáp", "95 câu hỏi về đức tin và đời sống, trả lời có căn cứ Kinh Thánh."),
        ("/bach-khoa/", "Bách Khoa Thần Học", "201 thuật ngữ thần học và Kinh Thánh, giải nghĩa rõ ràng."),
        ("/hoc-vien/", "Học Viện Cải Chánh", "Lộ trình học từ nền tảng đến thần học hệ thống (Thirdmill)."),
        ("/tra-kinh-thanh.html", "Tra cứu Kinh Thánh", "Tìm từ, cụm từ trong toàn bộ bản 1934."),
        ("/bang-doc-sach.html", "Bảng đọc của tôi", "Sách đang đọc, đã đọc xong, đã lưu và dấu trang — chỉ lưu trên thiết bị này."),
        ("/chu-de/", "Sách theo chủ đề", "13 chuyên mục sách Cải Chánh theo chủ đề: ân điển, Ba Ngôi, cầu nguyện…"),
    ]
    tgrid = "".join(
        f'<a class="idx-card" href="{u}"><h3>{t}</h3><p>{d}</p></a>' for u, t, d in tools)
    body = f"""  <p class="crumb"><a href="/">Trang chủ</a></p>
  <div class="cat-head">
    <div class="kicker">Học Kinh Thánh sâu hơn</div>
    <h1>Nghiên cứu Kinh Thánh</h1>
    <p style="max-width:640px;margin:0 auto;color:var(--ink-soft)">Nhân vật, chủ đề, giới thiệu từng sách, dòng thời gian và bản đồ — tất cả dẫn về bản Kinh Thánh 1934 và các công cụ học tập của trang.</p>
  </div>
  <div class="hub-grid">{grid}</div>
  <div class="cat-band"><div class="cat-band-head"><h3>Công cụ học Kinh Thánh khác</h3></div></div>
  <div class="hub-grid">{tgrid}</div>
  <p style="text-align:center;color:var(--ink-soft);font-size:13.5px">Tiểu sử nhân vật, phần giới thiệu chủ đề, tóm tắt chương và dòng thời gian là nội dung AI soạn, chưa duyệt — xin đối chiếu với Kinh Thánh. Câu Kinh Thánh trích dẫn là bản Truyền Thống 1934, nguyên văn.</p>
  {share_row(url)}
  {report_mailto("Nghiên cứu Kinh Thánh")}"""
    p = page("Nghiên cứu Kinh Thánh — Nhân vật, chủ đề, giới thiệu sách, dòng thời gian, bản đồ | Reformed Vietnam",
             "Nghiên cứu Kinh Thánh: 50 nhân vật, 20 chủ đề, giới thiệu 66 sách, dòng thời gian và bản đồ — tất cả dẫn về Kinh Thánh 1934.", url, body, CSS)
    queue_page(ROOT / "nghien-cuu-kinh-thanh.html", p, "/nghien-cuu-kinh-thanh.html")
    print("  hub: /nghien-cuu-kinh-thanh.html")
    return ["/nghien-cuu-kinh-thanh.html"]


def main():
    # Validate every verse key in the data resolves to a real 1934 verse.
    for src, rows in (("nhanvat", NV), ("topics", TP)):
        for e in rows:
            for v in e["verses"]:
                verse_text(v["key"])
    for m in MAPS:
        for k in m["verses"]:
            verse_text(k)
    # Validate every chapter summary exists.
    for bid in ORDER:
        for ch in range(1, NCH[bid] + 1):
            assert f"{bid}:{ch}" in SUMS, f"missing chapter summary {bid}:{ch}"
    print("validation: all verse keys + chapter summaries resolve")
    urls = []
    urls += build_characters()
    urls += build_topics()
    urls += build_book_intros()
    urls += build_timeline()
    urls += build_maps()
    urls += build_hub()
    # Write everything first, then link-check: the pages link to each
    # other (characters -> book intros + hub, indexes -> pages), so no
    # single page can be checked before the rest exist.
    n_written = 0
    for path, html_text, _label in PAGES:
        if write_if_changed(path, html_text):
            n_written += 1
    print(f"pages written: {n_written} changed, {len(PAGES) - n_written} unchanged (of {len(PAGES)})")
    for path, html_text, label in PAGES:
        check_links(html_text, label)
    print(f"link check: {len(PAGES)} pages, all internal links resolve")
    added = sitemap_add(urls)
    print(f"sitemap: {added} URLs added (of {len(urls)} new pages)")
    print("DONE")


if __name__ == "__main__":
    main()

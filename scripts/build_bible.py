#!/usr/bin/env python3
"""Build the Bible Study module (Kinh Thánh 1934 reader) for Reformed Vietnam.

Sources (Kinh Thánh Mỗi Ngày app data, integrated under the owner's override
of 2026-11-06):
  - data/books.json  — 66 books, canonical order, chapter verse counts
  - data/bible/*.json — the full 1934 Vietnamese Bible (31,102 verses)
  - data/xref/*.json  — ~34k cross-references, keyed "chapter:verse"
  - data/notes.json   — 100 chapter study notes (context/exegesis/application/
                        prayer), each already marked "AI soạn, chưa được
                        mục sư duyệt" at the source; pages carry the site label
  - data/kehoach.json, plan-nt90.json, plan-prov31.json — reading plans

Outputs: kinh-thanh/index.html, kinh-thanh/<book>/<chapter>.html x1,189,
kinh-thanh/ke-hoach-doc/<plan>.html x3, sitemap.xml updates.
"""
import json, re, html, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
APP = ROOT.parent / "bible-app" / "data"
BASE = "https://reformed-vietnam.vercel.app"

books_meta = json.loads((APP / "books.json").read_text(encoding="utf-8"))
assert len(books_meta) == 66
notes = json.loads((APP / "notes.json").read_text(encoding="utf-8"))
summ_path = ROOT / "data/chapter-summaries.json"
summaries = json.loads(summ_path.read_text(encoding="utf-8"))["entries"] if summ_path.exists() else {}
id2name = {b["id"]: b["name"] for b in books_meta}
order = [b["id"] for b in books_meta]

def key_to_ref(key):
    parts = key.split(":")
    if len(parts) != 3: return None
    bid, ch, vs = parts
    if bid not in id2name: return None
    return (f"{id2name[bid]} {ch}:{vs}", f"/kinh-thanh/{bid}/{ch}.html#v{vs.split('-')[0]}")

hub = (ROOT / "hub.html").read_text(encoding="utf-8")
font_link = re.search(r'<link rel="stylesheet" href="data:text/css;base64,[^>]+>', hub).group(0)
style = re.search(r"<style>(.*?)</style>", hub, re.S).group(1)
header = re.search(r"<header.*?</header>", hub, re.S).group(0)
footer = re.search(r"<footer.*?</footer>", hub, re.S).group(0)

def rebase(block):
    block = block.replace('href="#top"', 'href="/"')
    return re.sub(r'href="#([a-z-]+)"', r'href="/#\1"', block)
header, footer = rebase(header), rebase(footer)

EXTRA_CSS = """
      /* nav-offset fallback: builders extract <main id=top> from hub.html;
         if a rebuild ever drops that wrapper, anchored sections still clear the fixed header */
      section[id] { scroll-margin-top: 76px; }

      /* ---------- bible reader ---------- */
      .crumb { font-size: 13.5px; color: var(--ink-soft); margin: 26px 0 6px; }
      .crumb a { color: var(--burgundy); text-decoration: none; }
      .cat-head { text-align: center; padding: 18px 0 6px; }
      .cat-head .kicker { color: var(--gold-text); font-weight: 700; letter-spacing: .08em; text-transform: uppercase; font-size: 12.5px; }
      .cat-head h1 { font-family: "Playfair Display", serif; font-size: clamp(26px, 4.6vw, 38px); margin: 8px 0 10px; }
      .cat-panel { max-width: 720px; margin: 18px auto 8px; background: var(--surface); border: 1px solid var(--line); border-radius: var(--radius); padding: 26px 26px 20px; box-shadow: var(--shadow); }
      .ai-label { display: inline-block; font-size: 12px; font-weight: 600; color: var(--burgundy); background: color-mix(in srgb, var(--burgundy) 9%, transparent); border: 1px solid color-mix(in srgb, var(--burgundy) 35%, transparent); padding: 2px 9px; border-radius: 999px; }
      .verse { font-family: "Noto Serif", serif; font-size: 17px; line-height: 1.8; margin: 0 0 10px; scroll-margin-top: 90px; }
      .verse .vn { font-family: "Be Vietnam Pro", sans-serif; font-size: 11.5px; font-weight: 700; color: var(--gold-text); vertical-align: super; margin-right: 5px; }
      .xref { margin: -4px 0 12px; font-size: 13.5px; }
      .xref summary { cursor: pointer; color: var(--burgundy); font-weight: 600; }
      .xref div { padding: 6px 0 2px; line-height: 2; overflow-wrap: break-word; }
      .xref a { color: var(--ink); margin-right: 10px; white-space: nowrap; }
      .chips { display: flex; flex-wrap: wrap; gap: 6px; margin: 10px 0; }
      .chips a { min-width: 38px; text-align: center; padding: 6px 8px; border: 1px solid var(--line); border-radius: 8px; text-decoration: none; color: var(--ink); font-size: 14px; background: var(--surface); }
      .chips a.cur { background: var(--burgundy); color: #fff; border-color: var(--burgundy); }
      .books-details { max-width: 720px; margin: 0 auto 6px; }
      .books-details summary { cursor: pointer; font-weight: 600; color: var(--burgundy); padding: 8px 0; }
      .book-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(168px, 1fr)); gap: 9px; }
      .book-card { display: block; background: var(--surface); border: 1px solid var(--line); border-radius: 10px; padding: 12px 14px; text-decoration: none; }
      .book-card .bn { font-family: "Noto Serif", serif; font-weight: 700; color: var(--ink); font-size: 16px; }
      .book-card .bc { display: block; font-size: 13px; color: var(--ink-soft); margin-top: 2px; }
      .book-card:hover { border-color: var(--burgundy); }
      .qnav { display: flex; justify-content: space-between; gap: 10px; max-width: 720px; margin: 20px auto 6px; }
      .share-row { display: flex; gap: 10px; justify-content: center; margin: 18px 0 4px; flex-wrap: wrap; }
      .note-panel h3 { margin: 14px 0 6px; }
      .note-panel p, .note-panel li { font-family: "Noto Serif", serif; font-size: 15.5px; line-height: 1.75; }
      .plan-row { display: flex; justify-content: space-between; gap: 10px; padding: 9px 2px; border-bottom: 1px solid var(--line); font-size: 15px; }
      .plan-row a { color: var(--burgundy); text-decoration: none; font-weight: 600; }
      /* ---------- design pass 2026-11: pull quote + section rhythm ---------- */
      .pull-quote { font-family: "Playfair Display", serif; font-style: italic; font-size: 20px; color: var(--burgundy); border-left: 4px solid var(--gold-soft); }
      .testament-h { border-bottom: 2px solid var(--gold-soft); padding-bottom: 6px; }
      .band-tint { background: color-mix(in srgb, var(--burgundy) 6%, var(--bg)); border-top: 2px solid var(--gold-soft); border-radius: var(--radius); padding: 16px 20px 20px; margin-top: 26px; }
      .band-tint h2 { margin-top: 0 !important; }
"""

MINI_JS = """
<script>
  (function () {
    var b = document.getElementById("menuBtn"), n = document.querySelector("nav.main");
    if (b && n) b.addEventListener("click", function () {
      var open = n.style.display === "flex";
      n.style.display = open ? "" : "flex";
      b.setAttribute("aria-expanded", String(!open));
    });
    var top = document.getElementById("toTop");
    if (top) top.addEventListener("click", function () { window.scrollTo({ top: 0, behavior: "smooth" }); });
  })();
</script>
"""

def esc(s): return html.escape(s, quote=True)

def head(title, desc, url):
    return f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}" />
<link rel="canonical" href="{url}" />
<meta property="og:type" content="article" />
<meta property="og:title" content="{esc(title)}" />
<meta property="og:description" content="{esc(desc)}" />
<meta property="og:url" content="{url}" />
<meta property="og:image" content="{BASE}/og.jpg" />
<link rel="icon" href="/favicon.svg" type="image/svg+xml" />
{font_link}
<style>{style}{EXTRA_CSS}</style>
</head>"""

def share_row(url):
    return (f'<div class="share-row">'
            f'<a class="btn solid" target="_blank" rel="noopener" href="https://www.facebook.com/sharer/sharer.php?u={url}">Chia sẻ Facebook</a>'
            f'<a class="btn" target="_blank" rel="noopener" href="https://sp.zalo.me/share_inline?url={url}">Chia sẻ Zalo</a></div>')

from text_corrections import fix_verse, merge_split

OUT = ROOT / "kinh-thanh"
OUT.mkdir(exist_ok=True)

book_links = "".join(
    f'<a href="/kinh-thanh/{b["id"]}/1.html">{esc(b["name"])}</a>'
    for b in books_meta)
book_links = "<span style='line-height:2.1'>" + " · ".join(
    f'<a href="/kinh-thanh/{b["id"]}/1.html" style="color:var(--ink);white-space:nowrap">{esc(b["name"])}</a>'
    for b in books_meta) + "</span>"

# flat chapter sequence for prev/next across books
flat = []
for b in books_meta:
    for c in range(1, len(b["nc"]) + 1):
        flat.append((b["id"], c))
flatpos = {bc: i for i, bc in enumerate(flat)}
total_verses = 0
xref_total = 0

for b in books_meta:
    bid, bname = b["id"], b["name"]
    data = json.loads((APP / "bible" / f"{bid}.json").read_text(encoding="utf-8"))
    xref_path = APP / "xref" / f"{bid}.json"
    xref = json.loads(xref_path.read_text(encoding="utf-8")) if xref_path.exists() else {}
    bdir = OUT / bid
    bdir.mkdir(exist_ok=True)
    nch = len(data["ch"])
    chips = "".join(
        f'<a href="/kinh-thanh/{bid}/{c}.html" data-c="{c}">{c}</a>' for c in range(1, nch + 1))
    for ci, verses in enumerate(data["ch"], start=1):
        total_verses += len(verses)
        i = flatpos[(bid, ci)]
        prev_bc = flat[i - 1] if i > 0 else None
        next_bc = flat[i + 1] if i < len(flat) - 1 else None
        vhtml = []
        for vi, vtext in enumerate(verses, start=1):
            vtext = fix_verse(bid, ci, vi, vtext)
            vhtml.append(f'<p class="verse" id="v{vi}"><span class="vn">{vi}</span>{esc(vtext)}</p>')
            refs = xref.get(f"{ci}:{vi}")
            if refs:
                links = []
                for key in refs:
                    r = key_to_ref(key)
                    if r: links.append(f'<a href="{r[1]}">{esc(r[0])}</a>')
                if links:
                    xref_total += len(links)
                    vhtml.append(f'<details class="xref"><summary>Tham chiếu ({len(links)})</summary><div>{" ".join(links)}</div></details>')
        note = notes.get(f"{bid}:{ci}")
        note_html = ""
        if note:
            exeg = "".join(f"<li>{esc(merge_split(x))}</li>" for x in note.get("exegesis", []))
            appl = "".join(f"<li>{esc(merge_split(x))}</li>" for x in note.get("application", []))
            note_html = f"""
  <article class="cat-panel note-panel">
    <div class="kicker" style="color:var(--gold-text);font-weight:700;font-size:12.5px;letter-spacing:.08em">GHI CHÚ HỌC KINH THÁNH</div>
    <p style="margin-top:8px"><span class="ai-label">Nội dung AI soạn, chưa duyệt</span></p>
    <h3>Bối cảnh</h3><p>{esc(merge_split(note.get('context', '')))}</p>
    <h3>Giải nghĩa</h3><ul style="margin:0;padding-left:20px">{exeg}</ul>
    <h3>Áp dụng</h3><ul style="margin:0;padding-left:20px">{appl}</ul>
    <h3>Cầu nguyện</h3><p>{esc(merge_split(note.get('prayer', '')))}</p>
  </article>"""
        intro_html = ""
        sm = summaries.get(f"{bid}:{ci}")
        if sm:
            theme_chips = "".join(f'<span class="btn" style="pointer-events:none">{esc(t)}</span>' for t in sm.get("themes", []))
            intro_html = f"""
  <article class="cat-panel" style="margin-bottom:18px">
    <div class="kicker" style="color:var(--gold-text);font-weight:700;font-size:12.5px;letter-spacing:.08em">TÓM TẮT CHƯƠNG</div>
    <p style="margin-top:8px"><span class="ai-label">Nội dung AI soạn, chưa duyệt</span></p>
    <p style="margin-top:8px">{esc(sm['summary_vi'])}</p>
    <blockquote class="dev-verse-lg pull-quote" style="margin:12px 0 4px">“{esc(sm['key_verse_text'])}”</blockquote>
    <p style="color:var(--ink-soft);font-size:14px;margin:0 0 10px">— {esc(sm['key_verse_ref'])}</p>
    <div style="display:flex;flex-wrap:wrap;gap:8px">{theme_chips}</div>
  </article>"""
        nav = '<nav class="qnav">'
        if prev_bc:
            nav += f'<a class="btn" href="/kinh-thanh/{prev_bc[0]}/{prev_bc[1]}.html">← {esc(id2name[prev_bc[0]])} {prev_bc[1]}</a>'
        else:
            nav += "<span></span>"
        if next_bc:
            nav += f'<a class="btn" href="/kinh-thanh/{next_bc[0]}/{next_bc[1]}.html">{esc(id2name[next_bc[0]])} {next_bc[1]} →</a>'
        nav += "</nav>"
        url = f"{BASE}/kinh-thanh/{bid}/{ci}.html"
        title = f"{bname} {ci} — Kinh Thánh 1934 | Reformed Vietnam"
        desc = sm["summary_vi"] if sm else ((verses[0][:150] + "…") if verses else title)
        page = f"""{head(title, desc, url)}
<body id="top">
{header}
<main class="wrap">
  <p class="crumb"><a href="/">Trang chủ</a> · <a href="/kinh-thanh/">Kinh Thánh</a> · {esc(bname)}</p>
  <div class="cat-head">
    <div class="kicker">Kinh Thánh 1934</div>
    <h1>{esc(bname)} {ci}</h1>
  </div>
  <details class="books-details"><summary>Đổi sách — tất cả 66 sách</summary><div style="padding:4px 0 8px">{book_links}</div></details>
  <div class="chips" style="max-width:720px;margin:6px auto">{chips.replace(f'data-c="{ci}"', f'data-c="{ci}" class="cur"')}</div>
  {intro_html}
  <article class="cat-panel">
    {''.join(vhtml)}
  </article>
  {note_html}
  {nav}
  {share_row(url)}
  <p style="text-align:center;color:var(--ink-soft);font-size:13px;margin-bottom:34px">Bản Kinh Thánh Truyền Thống 1934. Ghi chú học tập (nếu có) do AI soạn, chưa qua duyệt.</p>
</main>
{footer}
{MINI_JS}
</body>
</html>"""
        (bdir / f"{ci}.html").write_text(page, encoding="utf-8")
print(f"chapter pages written: {len(flat)} | verses: {total_verses} | xref links: {xref_total}")

# ---- reading plans ----
PLANS = [
    ("doc-tron-kinh-thanh-mot-nam", "Đọc trọn Kinh Thánh trong một năm", "kehoach.json",
     "Mỗi ngày một đoạn theo thứ tự các sách — trọn bộ 66 sách trong 365 ngày."),
    ("tan-uoc-90-ngay", "Tân Ước trong 90 ngày", "plan-nt90.json",
     "Đọc trọn 27 sách Tân Ước trong 90 ngày, mỗi ngày một đoạn ngắn."),
    ("cham-ngon-31-ngay", "Châm Ngôn trong 31 ngày", "plan-prov31.json",
     "Mỗi ngày một chương Châm Ngôn — trọn sách trong một tháng."),
]
plan_dir = OUT / "ke-hoach-doc"
plan_dir.mkdir(exist_ok=True)
plan_cards = ""
for slug, pname, fname, pdesc in PLANS:
    plan = json.loads((APP / fname).read_text(encoding="utf-8"))
    rows = ""
    for di, day in enumerate(plan, start=1):
        segs = []
        for d in day:
            bk = books_meta[d["b"]]
            rng = f'{d["c1"]}' if d["c1"] == d["c2"] else f'{d["c1"]}–{d["c2"]}'
            segs.append(f'<a href="/kinh-thanh/{bk["id"]}/{d["c1"]}.html">{esc(bk["name"])} {rng}</a>')
        rows += (f'<div class="plan-row"><span>Ngày {di}</span>'
                 f'<span>{" · ".join(segs)}</span></div>')
    url = f"{BASE}/kinh-thanh/ke-hoach-doc/{slug}.html"
    page = f"""{head(pname + " | Kế Hoạch Đọc Kinh Thánh", pdesc, url)}
<body id="top">
{header}
<main class="wrap">
  <p class="crumb"><a href="/">Trang chủ</a> · <a href="/kinh-thanh/">Kinh Thánh</a> · Kế hoạch đọc</p>
  <div class="cat-head">
    <div class="kicker">Kế Hoạch Đọc Kinh Thánh</div>
    <h1>{esc(pname)}</h1>
    <p style="max-width:620px;margin:0 auto;color:var(--ink-soft)">{esc(pdesc)} Bấm vào từng ngày để mở chương đầu tiên của đoạn đọc.</p>
  </div>
  <article class="cat-panel">
    {rows}
  </article>
  <p style="text-align:center;margin:16px 0 34px"><a class="btn" href="/kinh-thanh/">← Tất cả 66 sách</a></p>
</main>
{footer}
{MINI_JS}
</body>
</html>"""
    (plan_dir / f"{slug}.html").write_text(page, encoding="utf-8")
    plan_cards += (f'<a class="book-card" href="/kinh-thanh/ke-hoach-doc/{slug}.html">'
                   f'<span class="bn">{esc(pname)}</span><span class="bc">{esc(pdesc)}</span></a>')
print("3 reading plan pages written")

# ---- landing ----
ot = "".join(f'<a class="book-card" href="/kinh-thanh/{b["id"]}/1.html"><span class="bn">{esc(b["name"])}</span><span class="bc">{len(b["nc"])} chương</span></a>' for b in books_meta if b["t"] == "old")
nt = "".join(f'<a class="book-card" href="/kinh-thanh/{b["id"]}/1.html"><span class="bn">{esc(b["name"])}</span><span class="bc">{len(b["nc"])} chương</span></a>' for b in books_meta if b["t"] == "new")
landing = f"""{head("Đọc Kinh Thánh 1934 — Trọn bộ 66 sách | Reformed Vietnam",
                     "Đọc trọn bộ Kinh Thánh bản Truyền Thống 1934: 66 sách, 31.102 câu, tham chiếu chéo và ghi chú học tập, hoàn toàn miễn phí.", BASE + "/kinh-thanh/")}
<body id="top">
{header}
<main class="wrap">
  <p class="crumb"><a href="/">Trang chủ</a> · Kinh Thánh</p>
  <div class="cat-head">
    <div class="kicker">Học Kinh Thánh</div>
    <h1>Kinh Thánh 1934 — trọn bộ 66 sách</h1>
    <p style="max-width:640px;margin:0 auto;color:var(--ink-soft)">Bản Truyền Thống 1934, 31.102 câu. Mỗi câu có tham chiếu chéo đến các đoạn liên quan; 100 chương có thêm ghi chú học tập (bối cảnh, giải nghĩa, áp dụng, cầu nguyện). Chọn một sách để bắt đầu đọc.</p>
  </div>
  <h2 class="testament-h" style="font-family:'Playfair Display',serif;color:var(--gold-text);margin:22px 0 10px">Cựu Ước</h2>
  <div class="book-grid">{ot}</div>
  <h2 class="testament-h" style="font-family:'Playfair Display',serif;color:var(--gold-text);margin:26px 0 10px">Tân Ước</h2>
  <div class="book-grid">{nt}</div>
  <section class="band-tint">
  <h2 style="font-family:'Playfair Display',serif;color:var(--gold-text);margin:26px 0 10px">Kế hoạch đọc</h2>
  <div class="book-grid">{plan_cards}</div>
  </section>
  <p style="text-align:center;color:var(--ink-soft);font-size:13px;margin:26px 0 34px">Ghi chú học tập do AI soạn, chưa qua duyệt. Bản dịch 1934 được dùng rộng rãi trong các Hội Thánh Việt Nam.</p>
</main>
{footer}
{MINI_JS}
</body>
</html>"""
(OUT / "index.html").write_text(landing, encoding="utf-8")
print("landing page written")

sm_path = ROOT / "sitemap.xml"
sm = sm_path.read_text(encoding="utf-8")
new_urls = ["/kinh-thanh/"] + [f"/kinh-thanh/ke-hoach-doc/{s}.html" for s, _, _, _ in PLANS] + \
           [f"/kinh-thanh/{bid}/{c}.html" for bid, c in flat]
added = 0
parts = []
for u in new_urls:
    loc = f"<loc>{BASE}{u}</loc>"
    if loc not in sm:
        parts.append(f"<url>{loc}</url>"); added += 1
if parts:
    sm = sm.replace("</urlset>", "".join(parts) + "</urlset>")
    sm_path.write_text(sm, encoding="utf-8")
print(f"sitemap: {added} URLs added")
print("DONE")

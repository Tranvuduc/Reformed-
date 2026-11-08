#!/usr/bin/env python3
"""Build the Theology Encyclopedia module for Reformed Vietnam (Phase B).

Sources (all integrated under the module's "Nội dung AI soạn, chưa duyệt" label):
  - Kinh-thanh-moi-ngay/data/glossary.json — 200 terms; definition_short_vi is
    always the glossary's own text, verbatim.
  - scripts/helper-data/encyclopedia-batch-*.json — helper-AI expansions
    (body, misunderstandings, English names, extra Scripture refs, related
    catechism/books), verified by the integrator 2026-11-06: schemas exact,
    all 569 verse instances exist in the 1934 text, locked terms enforced
    (one "Tin mừng" slip in the wrath entry is corrected to "Phúc Âm" below).
  - The hub homepage's 8 curated terms supply related-term links.
  - Verse texts: the Bible app repo's data/bible/*.json (1934 Vietnamese Bible).

Outputs: data/encyclopedia.json (Guide §10 shape), bach-khoa/index.html,
bach-khoa/<slug>.html x200, sitemap.xml updates.
"""
import json, re, sys, html, pathlib, unicodedata
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from booklinks import resolve as resolve_books

ROOT = pathlib.Path(__file__).resolve().parent.parent
APP = ROOT.parent / "bible-app"
BASE = "https://reformed-vietnam.vercel.app"

glossary = json.loads((APP / "data/glossary.json").read_text(encoding="utf-8"))
assert len(glossary) == 200, len(glossary)

books = {}
name2id = {}
for f in (APP / "data" / "bible").glob("*.json"):
    d = json.loads(f.read_text(encoding="utf-8"))
    books[f.stem] = d
    name2id[d["name"].strip().lower()] = f.stem

from text_corrections import fix_verse

def verse_text(key):
    book, ch, vs = key.split(":")
    return fix_verse(book, int(ch), int(vs),
                     books[book]["ch"][int(ch) - 1][int(vs) - 1]).strip()

def resolve_ref(ref):
    """Vietnamese ref string ('Rô-ma 8:29–30') -> {ref_vi, text_vi} using 1934 texts."""
    m = re.match(r"^(.+?)\s+(\d+):(\d+)(?:\s*[–—-]\s*(\d+))?$", ref.strip())
    if not m: return None
    name, ch, v1, v2 = m.groups()
    bid = name2id.get(name.strip().lower())
    if not bid: return None
    chs = books[bid]["ch"]
    verses = list(range(int(v1), int(v2) + 1)) if v2 else [int(v1)]
    texts = [fix_verse(bid, int(ch), v, chs[int(ch) - 1][v - 1]).strip() for v in verses]
    return {"ref_vi": ref, "text_vi": " ".join(texts)}

def slugify(s):
    s = s.replace("Đ", "d").replace("đ", "d")
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

def norm(s):
    return slugify(s).replace("-", " ")

# ---- hub's 8 curated terms (related links only) ----
hub = (ROOT / "hub.html").read_text(encoding="utf-8")
hub_terms = {}
for m in re.finditer(r'\{\s*name:\s*"([^"]+)",\s*en:\s*"([^"]+)",\s*def:\s*"((?:[^"\\]|\\.)*)",\s*verse:\s*"[^"]*",\s*related:\s*\[([^\]]*)\]\s*\}', hub):
    name, en, defn, rel = m.groups()
    hub_terms[slugify(name)] = {"related": [slugify(x) for x in re.findall(r'"([^"]+)"', rel)]}
ALIASES = {"tien-dinh": "su-tien-dinh", "tuyen-chon": "su-tuyen-chon",
           "chuoc-toi": "su-chuoc-toi", "nen-thanh": "su-nen-thanh"}
hub_terms = {ALIASES.get(k, k): {"related": [ALIASES.get(r, r) for r in v["related"]]}
             for k, v in hub_terms.items()}

# ---- helper-AI expansions (verified) ----
helper = {}
for i in range(1, 9):
    for e in json.loads((ROOT / "scripts/helper-data" / f"encyclopedia-batch-{i:02d}.json").read_text(encoding="utf-8")):
        helper[e["slug"]] = e
assert len(helper) == 200, len(helper)
# locked-term fix: exactly one "Tin mừng" slip exists in the delivery (wrath entry)
blob = json.dumps(helper, ensure_ascii=False)
assert blob.count("Tin mừng") == 1
helper = json.loads(blob.replace("Tin mừng", "Phúc Âm"))
print("helper expansions loaded: 200 | locked-term fix applied: Tin mừng -> Phúc Âm (x1)")

# ---- build merged entries ----
entries, missing = [], []
for e in glossary:
    slug = slugify(e["term"])
    h = helper[slug]
    refs, seen_refs = [], set()
    for v in e.get("verses", []):
        try: txt = verse_text(v["key"])
        except Exception: missing.append(v["key"]); txt = ""
        refs.append({"ref_vi": v["ref"], "text_vi": txt, "key": v["key"]}); seen_refs.add(v["ref"])
    for r in h["scripture_refs_vi"]:
        if r in seen_refs: continue
        rr = resolve_ref(r)
        if rr is None: missing.append("ref:" + r); continue
        refs.append(rr); seen_refs.add(r)
    hubrel = hub_terms.get(slug, {}).get("related", [])
    entries.append({
        "slug": slug,
        "term_vi": e["term"],
        "term_en": h["term_en"],
        "definition_short_vi": e["def"],
        "body_vi": h["body_vi"],
        "scripture_refs": refs,
        "misunderstandings_vi": h["misunderstandings_vi"],
        "related_books": h["related_books"],
        "related_books_resolved": resolve_books(h["related_books"]),
        "related_catechism": h["related_catechism"],
        "related_terms": hubrel,
        "review_status": "ai-unreviewed",
        "copyright": h["copyright"],
    })
if missing:
    print("UNRESOLVED:", missing); sys.exit(1)
print(f"verse texts resolved: {sum(len(e['scripture_refs']) for e in entries)} refs across 200 entries")

# ---- integrator extra entries (terms missing from the app glossary, e.g.
# justification — added 2026-11-07; full entries in the output schema with
# scripture texts pre-resolved verbatim from the 1934 Bible) ----
_extra_path = ROOT / "scripts/helper-data/encyclopedia-extra.json"
if _extra_path.exists():
    _extras = json.loads(_extra_path.read_text(encoding="utf-8"))
    for _x in _extras:
        _x["related_books_resolved"] = resolve_books(_x["related_books"])
        entries.append(_x)
    print(f"extra entries appended: {len(_extras)}")

# ---- locked-term decision 2026-11-07 (owner): Kingdom of God =
# "Vương quốc Đức Chúa Trời" in the site's own voice. The app glossary
# term and helper expansions say "Nước Đức Chúa Trời" (the 1934 form);
# rename the term in own-voice fields only. The slug stays
# nuoc-duc-chua-troi so existing links and sitemap entries do not
# break, and 1934 verse quotations keep "nước Đức Chúa Trời" verbatim.
for _e in entries:
    if _e["term_vi"] == "Nước Đức Chúa Trời":
        _e["term_vi"] = "Vương quốc Đức Chúa Trời"
    _e["body_vi"] = [p.replace("Nước Đức Chúa Trời", "Vương quốc Đức Chúa Trời") for p in _e["body_vi"]]
    _e["misunderstandings_vi"] = [p.replace("Nước Đức Chúa Trời", "Vương quốc Đức Chúa Trời") for p in _e["misunderstandings_vi"]]
print("locked-term fix applied: Nước -> Vương quốc Đức Chúa Trời (own voice)")

# ---- locked-term fix 2026-11-08 (Round 10 spot-check): the Phúc Âm
# glossary definition opens "Tin mừng:" — the locked term for the gospel
# in the site's own voice is "Phúc Âm" (owner lock 2026-11-07). The app
# glossary stays untouched; rename in the hub's own-voice field only.
for _e in entries:
    if _e["slug"] == "phuc-am" and _e["definition_short_vi"].startswith("Tin mừng:"):
        _e["definition_short_vi"] = "Phúc Âm:" + _e["definition_short_vi"][len("Tin mừng:"):]
print("locked-term fix applied: Phúc Âm definition Tin mừng -> Phúc Âm (own voice)")

# ---- locked-term fix 2026-11-08 (Round 12 spot-check): troi-moi-dat-moi
# uses "công bình" twice in its own voice (definition + first body
# paragraph) — a paraphrase of 2 Phi-e-rơ 3:13, which the entry does not
# quote. The locked term for righteousness in the site's own voice is
# "sự công chính" (owner lock 2026-11-07); "công bình" stays only inside
# verbatim 1934 quotations.
for _e in entries:
    if _e["slug"] == "troi-moi-dat-moi":
        _e["definition_short_vi"] = _e["definition_short_vi"].replace("Nơi công bình ở,", "Nơi sự công chính ở,")
        _e["body_vi"] = [p.replace("nơi sự công bình ngự trị", "nơi sự công chính ngự trị") for p in _e["body_vi"]]
print("locked-term fix applied: troi-moi-dat-moi công bình -> sự công chính (own voice)")

# ---- locked-term fix 2026-11-08 (Round 14 spot-check, Hana batch 6):
# duy-an-dien body paragraph 3 uses "tin mừng" in its own voice —
# "duy ân điển là tin mừng lớn". The locked term for the gospel in the
# site's own voice is "Phúc Âm" (owner lock 2026-11-07); "tin mừng" is
# the same defect class as phuc-am (Round 10) and troi-moi-dat-moi
# (Round 12). The app glossary stays untouched; fix in the hub's
# own-voice field only.
for _e in entries:
    if _e["slug"] == "duy-an-dien":
        _e["body_vi"] = [p.replace("duy ân điển là tin mừng lớn", "duy ân điển là Phúc Âm lớn") for p in _e["body_vi"]]
print("locked-term fix applied: duy-an-dien tin mừng -> Phúc Âm (own voice)")

by_slug = {e["slug"]: e for e in entries}
for e in entries:
    if e["related_terms"]: continue
    rel = []
    my_def = norm(e["definition_short_vi"])
    for o in entries:
        if o["slug"] == e["slug"]: continue
        tname = norm(o["term_vi"])
        if len(tname) >= 4 and (tname in my_def or norm(e["term_vi"]) in norm(o["definition_short_vi"])):
            rel.append(o["slug"])
    e["related_terms"] = rel[:5]

(ROOT / "data/encyclopedia.json").write_text(json.dumps({
    "module": "encyclopedia",
    "source": "Kinh Thánh Mỗi Ngày — 200-term glossary, expanded by helper-AI drafts (integrator-verified 2026-11-06)",
    "label": "Nội dung AI soạn, chưa duyệt",
    "count": len(entries),
    "entries": entries,
}, ensure_ascii=False, indent=1), encoding="utf-8")
print("data/encyclopedia.json written (merged)")

# ---- template parts ----
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

      /* ---------- encyclopedia module ---------- */
      .crumb { font-size: 13.5px; color: var(--ink-soft); margin: 26px 0 6px; }
      .crumb a { color: var(--burgundy); text-decoration: none; }
      .cat-head { text-align: center; padding: 18px 0 6px; }
      .cat-head .kicker { color: var(--gold-text); font-weight: 700; letter-spacing: .08em; text-transform: uppercase; font-size: 12.5px; }
      .cat-head h1 { font-family: "Playfair Display", serif; font-size: clamp(26px, 4.6vw, 38px); margin: 8px 0 10px; }
      .cat-panel { max-width: 680px; margin: 18px auto 8px; background: var(--surface); border: 1px solid var(--line); border-radius: var(--radius); padding: 26px 26px 20px; box-shadow: var(--shadow); }
      .term-def { font-family: "Noto Serif", serif; font-size: 18.5px; line-height: 1.75; }
      .term-body p { font-family: "Noto Serif", serif; font-size: 16.5px; line-height: 1.75; }
      .ai-label { display: inline-block; font-size: 12px; font-weight: 600; color: var(--burgundy); background: color-mix(in srgb, var(--burgundy) 9%, transparent); border: 1px solid color-mix(in srgb, var(--burgundy) 35%, transparent); padding: 2px 9px; border-radius: 999px; }
      .proof { border-top: 1px solid var(--line); padding: 9px 0; }
      .proof summary { cursor: pointer; font-weight: 600; color: var(--burgundy); font-size: 15px; }
      .proof p { font-family: "Noto Serif", serif; font-size: 15.5px; line-height: 1.7; margin: 8px 0 4px; }
      .mis-list li { font-family: "Noto Serif", serif; font-size: 15.5px; line-height: 1.7; margin-bottom: 8px; }
      .share-row { display: flex; gap: 10px; justify-content: center; margin: 18px 0 4px; flex-wrap: wrap; }
      .rel-links a { display: inline-block; margin: 0 8px 8px 0; }
      .letter { font-family: "Playfair Display", serif; font-size: 22px; color: var(--gold-text); margin: 22px 0 8px; }
      .term-index { list-style: none; padding: 0; columns: 2; column-gap: 34px; max-width: 860px; margin: 0 auto; }
      @media (max-width: 720px) { .term-index { columns: 1; } }
      .term-index li { margin: 0 0 7px; break-inside: avoid; }
      .term-index a { color: var(--ink); text-decoration: none; }
      .term-index a:hover { color: var(--burgundy); text-decoration: underline; }
      .term-search { max-width: 560px; margin: 14px auto 4px; display: flex; gap: 8px; }
      .term-search input { flex: 1; padding: 12px 16px; border: 1px solid var(--line); border-radius: 999px; font: inherit; font-size: 15.5px; background: var(--surface); color: var(--ink); }
      /* ---------- design pass 2026-11: title band + term cards ---------- */
      .title-band { max-width: 860px; margin: 16px auto 6px; background: linear-gradient(120deg, var(--burgundy-deep), var(--burgundy)); border-radius: var(--radius); box-shadow: var(--shadow); padding: 26px 28px; display: flex; gap: 22px; align-items: center; }
      .title-band .tb-kicker { color: #eccf8f; font-weight: 700; letter-spacing: .09em; text-transform: uppercase; font-size: 12.5px; }
      .title-band h1 { font-family: "Playfair Display", serif; font-size: clamp(25px, 4.4vw, 36px); line-height: 1.28; margin: 6px 0 4px; color: #fdf6e9; }
      .title-band .tb-sub { color: #efdfc2; font-size: 15px; margin: 2px 0 0; font-style: italic; }
      .title-band .ai-label { background: rgba(255,255,255,.14); border-color: rgba(255,255,255,.45); color: #fdf6e9; font-style: normal; }
      .medallion { flex: 0 0 auto; width: 84px; height: 84px; border-radius: 50%; border: 2px solid #eccf8f; display: flex; flex-direction: column; align-items: center; justify-content: center; font-family: "Playfair Display", serif; color: #fdf6e9; text-align: center; padding: 4px; }
      .medallion .m-big { font-size: 32px; font-weight: 700; line-height: 1; }
      .medallion .m-small { font-size: 10.5px; letter-spacing: .08em; text-transform: uppercase; font-family: "Be Vietnam Pro", sans-serif; margin-top: 3px; color: #eccf8f; }
      @media (max-width: 560px) { .title-band { flex-direction: column; text-align: center; padding: 22px 18px; } .medallion { width: 70px; height: 70px; } .medallion .m-big { font-size: 26px; } }
      @media (prefers-color-scheme: dark) { .title-band { background: linear-gradient(120deg, #241611, #571d22); } }
      .band-tint { max-width: 860px; margin: 26px auto 0; background: color-mix(in srgb, var(--burgundy) 6%, var(--bg)); border-top: 2px solid var(--gold-soft); border-radius: var(--radius); padding: 16px 20px 6px; }
      .band-tint .bt-head { font-family: "Playfair Display", serif; font-size: 21px; margin: 0 0 12px; }
      .term-index { columns: unset; display: grid; grid-template-columns: 1fr 1fr; gap: 10px; max-width: 860px; }
      @media (max-width: 720px) { .term-index { grid-template-columns: 1fr; } }
      .term-index li { margin: 0; }
      .term-card { display: block; background: var(--surface); border: 1px solid var(--line); border-radius: 10px; padding: 13px 15px; box-shadow: var(--shadow); height: 100%; box-sizing: border-box; }
      .term-card:hover { border-color: var(--burgundy); text-decoration: none; }
      .term-card .tc-term { font-family: "Noto Serif", serif; font-weight: 700; font-size: 16.5px; color: var(--ink); display: block; }
      .term-card:hover .tc-term { color: var(--burgundy); }
      .term-card .tc-en { font-size: 12.5px; font-style: italic; color: var(--gold-text); display: block; margin-top: 1px; }
      .term-card .tc-def { font-size: 14px; line-height: 1.55; color: var(--ink-soft); display: block; margin-top: 5px; }
      .core-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; list-style: none; padding: 0; margin: 0; }
      @media (max-width: 720px) { .core-grid { grid-template-columns: 1fr; } }
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

def chips(title, pairs):
    if not pairs: return ""
    links = "".join(f'<a class="btn" href="{u}">{esc(label)}</a>' for label, u in pairs)
    return f'<div style="margin-top:18px"><h3 style="margin:0 0 10px">{title}</h3><div class="rel-links">{links}</div></div>'

OUT = ROOT / "bach-khoa"
OUT.mkdir(exist_ok=True)

for e in entries:
    url = f"{BASE}/bach-khoa/{e['slug']}.html"
    title = f"{e['term_vi']} là gì? | Bách Khoa Thần Học Cải Chánh"
    desc = e["definition_short_vi"][:155]
    en_line = f'<p style="color:var(--ink-soft);font-style:italic;margin:2px 0 0">{esc(e["term_en"])}</p>' if e["term_en"] else ""
    body = '<div class="term-body" style="margin-top:14px">' + "".join(f"<p>{esc(p)}</p>" for p in e["body_vi"]) + "</div>"
    proofs = "".join(
        f'<details class="proof"><summary>{esc(p["ref_vi"])}</summary><p>{esc(p["text_vi"])}</p></details>'
        for p in e["scripture_refs"])
    mis = ""
    if e["misunderstandings_vi"]:
        items = "".join(f"<li>{esc(m)}</li>" for m in e["misunderstandings_vi"])
        mis = f'<div style="margin-top:16px"><h3 style="margin:0 0 8px">Hiểu lầm thường gặp</h3><ul class="mis-list" style="margin:0;padding-left:20px">{items}</ul></div>'
    cat = chips("Trong Tín Lý Yếu Lược Westminster",
                [(f"Câu {n}", f"/giao-ly/cau-{n}.html") for n in e["related_catechism"]])
    bks = chips("Sách liên quan trong thư viện",
                [(label, u) for label, u in e["related_books_resolved"]])
    rel = chips("Thuật ngữ liên quan",
                [(by_slug[s]["term_vi"], f"/bach-khoa/{s}.html") for s in e["related_terms"] if s in by_slug])
    page = f"""{head(title, desc, url)}
<body id="top">
{header}
<main class="wrap">
  <p class="crumb"><a href="/">Trang chủ</a> · <a href="/bach-khoa/">Bách Khoa</a> · {esc(e['term_vi'])}</p>
  <div class="title-band">
    <div class="medallion"><span class="m-big">{esc(e['term_vi'].strip()[:1])}</span><span class="m-small">Thuật ngữ</span></div>
    <div>
      <div class="tb-kicker">Bách Khoa Thần Học</div>
      <h1>{esc(e['term_vi'])}</h1>
      <p class="tb-sub">{esc(e["term_en"])} &nbsp;<span class="ai-label">Nội dung AI soạn, chưa duyệt</span></p>
    </div>
  </div>
  <article class="cat-panel">
    <div class="term-def">{esc(e['definition_short_vi'])}</div>
    {body}
    {mis}
    <div style="margin-top:16px"><h3 style="margin:0 0 4px">Căn cứ Kinh Thánh <span style="font-weight:400;font-size:13.5px;color:var(--ink-soft)">(bấm để đọc câu gốc — bản 1934)</span></h3>{proofs}</div>
    {cat}
    {bks}
    {rel}
  </article>
  <p style="text-align:center;margin-top:16px"><a class="btn" href="/bach-khoa/">← Tất cả {len(entries)} thuật ngữ</a></p>
  {share_row(url)}
  <p style="text-align:center;color:var(--ink-soft);font-size:13px;margin-bottom:34px">Nguồn thuật ngữ: Kinh Thánh Mỗi Ngày; phần giải thích do AI soạn, chưa qua duyệt.</p>
</main>
{footer}
{MINI_JS}
</body>
</html>"""
    (OUT / f"{e['slug']}.html").write_text(page, encoding="utf-8")
print(f"{len(entries)} entry pages written (full entries)")

def term_card(e):
    en = f'<span class="tc-en">{esc(e["term_en"])}</span>' if e["term_en"] else ""
    return (f'<li data-name="{esc(norm(e["term_vi"]))}"><a class="term-card" href="/bach-khoa/{e["slug"]}.html">'
            f'<span class="tc-term">{esc(e["term_vi"])}</span>{en}'
            f'<span class="tc-def">{esc(e["definition_short_vi"])}</span></a></li>')

groups = {}
for e in sorted(entries, key=lambda x: x["slug"]):
    groups.setdefault(e["slug"][0].upper(), []).append(e)
index_html = ""
for letter in sorted(groups):
    items = "".join(term_card(e) for e in groups[letter])
    index_html += f'<h2 class="letter">{letter}</h2><ul class="term-index">{items}</ul>'

# featured core-terms row (design pass 2026-11): slugs verified against the data
CORE_SLUGS = ["an-dien", "duc-tin", "xung-cong-chinh", "su-chuoc-toi", "su-nen-thanh", "dang-christ"]
assert all(s in by_slug for s in CORE_SLUGS)
featured_html = ('<div class="band-tint"><h2 class="bt-head">Thuật ngữ cốt lõi</h2><ul class="core-grid">'
                 + "".join(term_card(by_slug[s]) for s in CORE_SLUGS) + "</ul></div>")
landing = f"""{head(f"Bách Khoa Thần Học Cải Chánh — {len(entries)} thuật ngữ | Reformed Vietnam",
                     f"Tra cứu {len(entries)} thuật ngữ thần học Cải Chánh bằng tiếng Việt dễ hiểu: định nghĩa, giải thích, căn cứ Kinh Thánh và thuật ngữ liên quan.", BASE + "/bach-khoa/")}
<body id="top">
{header}
<main class="wrap">
  <p class="crumb"><a href="/">Trang chủ</a> · Bách Khoa</p>
  <div class="cat-head">
    <div class="kicker">Bách Khoa Thần Học</div>
    <h1>{len(entries)} thuật ngữ, giải nghĩa dễ hiểu</h1>
    <p style="max-width:620px;margin:0 auto;color:var(--ink-soft)">Gặp một từ khó trong Kinh Thánh hay sách thần học — như "tiền định", "giao ước", "chuộc tội" — hãy tra ở đây: mỗi thuật ngữ có định nghĩa tóm tắt, phần giải thích dễ hiểu, các hiểu lầm thường gặp và câu Kinh Thánh căn cứ đọc ngay tại chỗ.</p>
    <p style="margin-top:10px"><span class="ai-label">Nội dung AI soạn, chưa duyệt</span></p>
  </div>
  <div class="term-search">
    <input type="search" id="termSearch" placeholder="Tìm thuật ngữ… (gõ không dấu cũng được)" aria-label="Tìm thuật ngữ" />
  </div>
  <p id="termCount" style="text-align:center;color:var(--ink-soft);font-size:13.5px">{len(entries)} thuật ngữ</p>
  {featured_html}
  <div id="termIndex">
{index_html}
  </div>
  <p style="text-align:center;color:var(--ink-soft);font-size:13px;margin:26px 0 34px">Nguồn thuật ngữ: Kinh Thánh Mỗi Ngày; phần giải thích do AI soạn, chưa qua duyệt.</p>
</main>
{footer}
{MINI_JS}
<script>
  (function () {{
    function norm(s) {{ return s.toLowerCase().normalize("NFD").replace(/[\\u0300-\\u036f]/g, "").replace(/đ/g, "d").replace(/Đ/g, "d"); }}
    var input = document.getElementById("termSearch"), items = document.querySelectorAll("#termIndex li"), count = document.getElementById("termCount");
    input.addEventListener("input", function () {{
      var q = norm(input.value.trim()), shown = 0;
      items.forEach(function (li) {{
        var hit = !q || norm(li.getAttribute("data-name") + " " + li.textContent).indexOf(q) >= 0;
        li.style.display = hit ? "" : "none"; if (hit) shown++;
      }});
      document.querySelectorAll("#termIndex .letter").forEach(function (h) {{
        var ul = h.nextElementSibling, any = false;
        ul.querySelectorAll("li").forEach(function (li) {{ if (li.style.display !== "none") any = true; }});
        h.style.display = any ? "" : "none"; ul.style.display = any ? "" : "none";
      }});
      count.textContent = q ? ("Tìm thấy " + shown + " thuật ngữ") : "{len(entries)} thuật ngữ";
    }});
  }})();
</script>
</body>
</html>"""
(OUT / "index.html").write_text(landing, encoding="utf-8")
print("landing page written")

sm_path = ROOT / "sitemap.xml"
sm = sm_path.read_text(encoding="utf-8")
sm = sm.replace("<url><loc>https://reformed-vietnam.vercel.app/thuat-ngu.html</loc></url>", "")
new_urls = ["/bach-khoa/"] + [f"/bach-khoa/{e['slug']}.html" for e in entries]
added = 0
for u in new_urls:
    loc = f"<loc>{BASE}{u}</loc>"
    if loc not in sm:
        sm = sm.replace("</urlset>", f"<url>{loc}</url></urlset>"); added += 1
sm_path.write_text(sm, encoding="utf-8")
print(f"sitemap: {added} URLs added")
print("DONE")

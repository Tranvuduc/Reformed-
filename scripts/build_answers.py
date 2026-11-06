#!/usr/bin/env python3
"""Build the Reformed Answers module for Reformed Vietnam (Phase B, part 3).

Source: scripts/helper-data/answers-starters.json — 5 helper-AI starter answers,
verified by the integrator 2026-11-06 (schemas exact, all Scripture refs exist
in the 1934 text, both-sides doctrine confirmed on Q1–Q3, short answers warm
and concrete on Q4–Q5). One fix applied below: the answers link the
predestination entry as "tien-dinh" (the guide's example slug) while the live
encyclopedia uses the glossary slug "su-tien-dinh" — rewritten here.

Outputs: data/answers.json (Guide §10 Q&A shape), hoi-dap/index.html,
hoi-dap/<slug>.html x5, sitemap.xml updates. The old hoi-dap.html stub is
redirected to /hoi-dap/ in vercel.json.
"""
import json, re, sys, html, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from booklinks import resolve as resolve_books

ROOT = pathlib.Path(__file__).resolve().parent.parent
APP = ROOT.parent / "bible-app"
BASE = "https://reformed-vietnam.vercel.app"

books, name2id = {}, {}
for f in (APP / "data" / "bible").glob("*.json"):
    d = json.loads(f.read_text(encoding="utf-8"))
    books[f.stem] = d
    name2id[d["name"].strip().lower()] = f.stem

def resolve_ref(ref):
    m = re.match(r"^(.+?)\s+(\d+):(\d+)(?:\s*[–—-]\s*(\d+))?$", ref.strip())
    if not m: return None
    name, ch, v1, v2 = m.groups()
    bid = name2id.get(name.strip().lower())
    if not bid: return None
    chs = books[bid]["ch"]
    verses = list(range(int(v1), int(v2) + 1)) if v2 else [int(v1)]
    return {"ref_vi": ref, "text_vi": " ".join(chs[int(ch) - 1][v - 1].strip() for v in verses)}

raw = json.loads((ROOT / "scripts/helper-data/answers-starters.json").read_text(encoding="utf-8"))
blob = json.dumps(raw, ensure_ascii=False)
assert blob.count('"tien-dinh"') == 2
raw = json.loads(blob.replace('"tien-dinh"', '"su-tien-dinh"'))
print("answers loaded: 5 | encyclopedia slug fix applied: tien-dinh -> su-tien-dinh (x2)")

enc = {e["slug"]: e for e in json.loads((ROOT / "data/encyclopedia.json").read_text(encoding="utf-8"))["entries"]}

entries = []
for a in raw:
    refs = []
    for r in a["scripture_refs_vi"]:
        rr = resolve_ref(r)
        assert rr is not None, r
        refs.append(rr)
    for s in a["related_encyclopedia"]:
        assert s in enc, f"encyclopedia slug missing: {s}"
    entries.append({
        "slug": a["slug"],
        "question_vi": a["question_vi"],
        "answer_short_vi": a["answer_short_vi"],
        "body_vi": a["body_vi"],
        "scripture_refs": refs,
        "related_encyclopedia": a["related_encyclopedia"],
        "related_catechism": a["related_catechism"],
        "related_books": a["related_books"],
        "related_books_resolved": resolve_books(a["related_books"]),
        "review_status": "ai-unreviewed",
    })
print("all refs resolved; all encyclopedia links valid")

(ROOT / "data/answers.json").write_text(json.dumps({
    "module": "reformed-answers",
    "source": "Helper-AI starter drafts (integrator-verified 2026-11-06)",
    "label": "Nội dung AI soạn, chưa duyệt",
    "count": len(entries),
    "entries": entries,
}, ensure_ascii=False, indent=1), encoding="utf-8")
print("data/answers.json written")

# ---- template parts ----
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
      /* ---------- answers module ---------- */
      .crumb { font-size: 13.5px; color: var(--ink-soft); margin: 26px 0 6px; }
      .crumb a { color: var(--burgundy); text-decoration: none; }
      .cat-head { text-align: center; padding: 18px 0 6px; }
      .cat-head .kicker { color: var(--gold-text); font-weight: 700; letter-spacing: .08em; text-transform: uppercase; font-size: 12.5px; }
      .cat-head h1 { font-family: "Playfair Display", serif; font-size: clamp(25px, 4.4vw, 36px); margin: 8px 0 10px; line-height: 1.3; }
      .cat-panel { max-width: 680px; margin: 18px auto 8px; background: var(--surface); border: 1px solid var(--line); border-radius: var(--radius); padding: 26px 26px 20px; box-shadow: var(--shadow); }
      .ans-short { font-family: "Noto Serif", serif; font-size: 18px; line-height: 1.75; }
      .ans-body p { font-family: "Noto Serif", serif; font-size: 16.5px; line-height: 1.75; }
      .ai-label { display: inline-block; font-size: 12px; font-weight: 600; color: var(--burgundy); background: color-mix(in srgb, var(--burgundy) 9%, transparent); border: 1px solid color-mix(in srgb, var(--burgundy) 35%, transparent); padding: 2px 9px; border-radius: 999px; }
      .proof { border-top: 1px solid var(--line); padding: 9px 0; }
      .proof summary { cursor: pointer; font-weight: 600; color: var(--burgundy); font-size: 15px; }
      .proof p { font-family: "Noto Serif", serif; font-size: 15.5px; line-height: 1.7; margin: 8px 0 4px; }
      .share-row { display: flex; gap: 10px; justify-content: center; margin: 18px 0 4px; flex-wrap: wrap; }
      .rel-links a { display: inline-block; margin: 0 8px 8px 0; }
      .qa-cards { display: grid; gap: 14px; max-width: 760px; margin: 18px auto 8px; }
      .qa-card { display: block; background: var(--surface); border: 1px solid var(--line); border-radius: var(--radius); padding: 20px 22px; box-shadow: var(--shadow); text-decoration: none; }
      .qa-card h3 { font-family: "Noto Serif", serif; font-size: 18.5px; margin: 0 0 6px; color: var(--ink); line-height: 1.45; }
      .qa-card p { margin: 0; color: var(--ink-soft); font-size: 15px; line-height: 1.6; }
      .qa-card:hover h3 { color: var(--burgundy); }
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

OUT = ROOT / "hoi-dap"
OUT.mkdir(exist_ok=True)

for e in entries:
    url = f"{BASE}/hoi-dap/{e['slug']}.html"
    q = e["question_vi"]
    title = f"{q} | Hỏi Đáp Cải Chánh"
    desc = e["answer_short_vi"][:155]
    body = '<div class="ans-body" style="margin-top:14px">' + "".join(f"<p>{esc(p)}</p>" for p in e["body_vi"]) + "</div>"
    proofs = "".join(
        f'<details class="proof"><summary>{esc(p["ref_vi"])}</summary><p>{esc(p["text_vi"])}</p></details>'
        for p in e["scripture_refs"])
    enc_chips = chips("Đọc thêm trong Bách Khoa",
                      [(enc[s]["term_vi"], f"/bach-khoa/{s}.html") for s in e["related_encyclopedia"]])
    cat_chips = chips("Trong Tín Lý Yếu Lược Westminster",
                      [(f"Câu {n}", f"/giao-ly/cau-{n}.html") for n in e["related_catechism"]])
    bks = chips("Sách liên quan trong thư viện", [(label, u) for label, u in e["related_books_resolved"]])
    page = f"""{head(title, desc, url)}
<body id="top">
{header}
<main class="wrap">
  <p class="crumb"><a href="/">Trang chủ</a> · <a href="/hoi-dap/">Hỏi Đáp</a></p>
  <div class="cat-head">
    <div class="kicker">Hỏi Đáp Cải Chánh</div>
    <h1>{esc(q)}</h1>
    <p style="margin-top:10px"><span class="ai-label">Nội dung AI soạn, chưa duyệt</span></p>
  </div>
  <article class="cat-panel">
    <div class="ans-short">{esc(e['answer_short_vi'])}</div>
    {body}
    <div style="margin-top:16px"><h3 style="margin:0 0 4px">Căn cứ Kinh Thánh <span style="font-weight:400;font-size:13.5px;color:var(--ink-soft)">(bấm để đọc câu gốc — bản 1934)</span></h3>{proofs}</div>
    {enc_chips}
    {cat_chips}
    {bks}
  </article>
  <p style="text-align:center;margin-top:16px"><a class="btn" href="/hoi-dap/">← Tất cả câu hỏi</a></p>
  {share_row(url)}
  <p style="text-align:center;color:var(--ink-soft);font-size:13px;margin-bottom:34px">Câu trả lời do AI soạn theo thần học Cải Chánh, chưa qua duyệt.</p>
</main>
{footer}
{MINI_JS}
</body>
</html>"""
    (OUT / f"{e['slug']}.html").write_text(page, encoding="utf-8")
print("5 answer pages written")

cards = "".join(
    f'<a class="qa-card" href="/hoi-dap/{e["slug"]}.html"><h3>{esc(e["question_vi"])}</h3><p>{esc(e["answer_short_vi"][:150])}…</p></a>'
    for e in entries)
landing = f"""{head("Hỏi Đáp Cải Chánh — Giải đáp thắc mắc đức tin | Reformed Vietnam",
                     "Những câu hỏi thường gặp về đức tin Cải Chánh — tiền định, cầu nguyện, xưng công chính — được trả lời ngắn gọn, dễ hiểu, có căn cứ Kinh Thánh.", BASE + "/hoi-dap/")}
<body id="top">
{header}
<main class="wrap">
  <p class="crumb"><a href="/">Trang chủ</a> · Hỏi Đáp</p>
  <div class="cat-head">
    <div class="kicker">Hỏi Đáp Cải Chánh</div>
    <h1>Thắc mắc về đức tin, trả lời dễ hiểu</h1>
    <p style="max-width:620px;margin:0 auto;color:var(--ink-soft)">Mỗi câu hỏi có một câu trả lời ngắn đọc ngay được, phần giải thích đầy đủ hơn, và các câu Kinh Thánh căn cứ. Danh sách câu hỏi sẽ tiếp tục được bổ sung.</p>
    <p style="margin-top:10px"><span class="ai-label">Nội dung AI soạn, chưa duyệt</span></p>
  </div>
  <div class="qa-cards">
{cards}
  </div>
  <p style="text-align:center;color:var(--ink-soft);font-size:13px;margin:26px 0 34px">Bạn có câu hỏi khác? Gửi về <a href="mailto:reformedvn@gmail.com">reformedvn@gmail.com</a> — những câu hỏi hay sẽ được bổ sung vào trang này.</p>
</main>
{footer}
{MINI_JS}
</body>
</html>"""
(OUT / "index.html").write_text(landing, encoding="utf-8")
print("landing page written")

sm_path = ROOT / "sitemap.xml"
sm = sm_path.read_text(encoding="utf-8")
sm = sm.replace("<url><loc>https://reformed-vietnam.vercel.app/hoi-dap.html</loc></url>", "")
new_urls = ["/hoi-dap/"] + [f"/hoi-dap/{e['slug']}.html" for e in entries]
added = 0
for u in new_urls:
    loc = f"<loc>{BASE}{u}</loc>"
    if loc not in sm:
        sm = sm.replace("</urlset>", f"<url>{loc}</url></urlset>"); added += 1
sm_path.write_text(sm, encoding="utf-8")
print(f"sitemap: {added} URLs added, hoi-dap.html entry removed")
print("DONE")

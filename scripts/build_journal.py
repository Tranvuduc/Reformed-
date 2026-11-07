#!/usr/bin/env python3
"""Build the Reformed Journal for Reformed Vietnam (Guide Phase D, §7.9).

Launch format (owner decision 2026-11-07: proceed without a separate
reviewer for now): the journal curates chapters from public-domain classics
already hosted in the library. AI-written introductions carry the label
"Nội dung AI soạn, chưa duyệt"; excerpts reproduce the library translation
verbatim and keep its label "Bản dịch AI, chưa duyệt". Nothing is presented
as reviewed editorial content. Source of truth: data/journal.json.
Outputs: tap-chi/index.html, tap-chi/<slug>.html, sitemap additions.
"""
import json, re, html, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = "https://reformed-vietnam.vercel.app"
data = json.loads((ROOT / "data/journal.json").read_text(encoding="utf-8"))
articles = data["articles"]

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
      /* ---------- journal module ---------- */
      .crumb { font-size: 13.5px; color: var(--ink-soft); margin: 26px 0 6px; }
      .crumb a { color: var(--burgundy); text-decoration: none; }
      .cat-head { text-align: center; padding: 18px 0 6px; }
      .cat-head .kicker { color: var(--gold-text); font-weight: 700; letter-spacing: .08em; text-transform: uppercase; font-size: 12.5px; }
      .cat-head h1 { font-family: "Playfair Display", serif; font-size: clamp(25px, 4.4vw, 36px); margin: 8px 0 10px; line-height: 1.3; }
      .cat-panel { max-width: 680px; margin: 18px auto 8px; background: var(--surface); border: 1px solid var(--line); border-radius: var(--radius); padding: 26px 26px 20px; box-shadow: var(--shadow); }
      .ans-body p { font-family: "Noto Serif", serif; font-size: 16.5px; line-height: 1.75; }
      .excerpt { font-family: "Noto Serif", serif; font-size: 16.5px; line-height: 1.8; }
      .excerpt p { margin: 0 0 14px; }
      .excerpt-mark { font-family: "Be Vietnam Pro", sans-serif; font-size: 12.5px; font-weight: 700; color: var(--gold-text); letter-spacing: .06em; margin: 20px 0 10px; }
      .ai-label { display: inline-block; font-size: 12px; font-weight: 600; color: var(--burgundy); background: color-mix(in srgb, var(--burgundy) 9%, transparent); border: 1px solid color-mix(in srgb, var(--burgundy) 35%, transparent); padding: 2px 9px; border-radius: 999px; }
      .share-row { display: flex; gap: 10px; justify-content: center; margin: 18px 0 4px; flex-wrap: wrap; }
      .basis { font-size: 13px; color: var(--ink-soft); border-top: 1px solid var(--line); padding-top: 10px; margin-top: 16px; line-height: 1.6; }
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

def esc(s): return html.escape(str(s), quote=True)

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

OUT = ROOT / "tap-chi"
OUT.mkdir(exist_ok=True)
sitemap_urls = ["/tap-chi/"]

for a in articles:
    url = f"{BASE}/tap-chi/{a['slug']}.html"
    sitemap_urls.append(f"/tap-chi/{a['slug']}.html")
    intro = "".join(f"<p>{esc(p)}</p>" for p in a["intro_vi"])
    excerpt = "".join(f"<p>{esc(p)}</p>" for p in a["excerpt_vi"])
    page = f"""{head(a["title_vi"] + " — " + a["author"] + " | Tạp Chí Cải Chánh", a["intro_vi"][0][:150], url)}
<body id="top">
{header}
<main class="wrap">
  <p class="crumb"><a href="/">Trang chủ</a> · <a href="/tap-chi/">Tạp Chí</a> · {esc(a["author"])}</p>
  <div class="cat-head">
    <div class="kicker">Tạp Chí Cải Chánh</div>
    <h1>{esc(a["title_vi"])}</h1>
    <p style="color:var(--ink-soft)">{esc(a["author"])} ({esc(a["author_years"])})</p>
    <p style="margin-top:10px"><span class="ai-label">Nội dung AI soạn, chưa duyệt</span></p>
  </div>
  <article class="cat-panel">
    <div class="ans-body">{intro}</div>
    <p class="excerpt-mark">TRÍCH ĐĂNG — BẢN DỊCH AI, CHƯA DUYỆT</p>
    <div class="excerpt">{excerpt}</div>
    <p style="margin-top:18px"><a class="btn solid" href="{esc(a["source_url"])}">Đọc trọn cuốn {esc(a["source_book_vi"])} trong thư viện →</a></p>
    <p class="basis">{esc(a["source_note"])} Nguyên tác thuộc phạm vi công cộng; phần trích đăng giữ nguyên văn bản dịch của thư viện.</p>
    {share_row(url)}
  </article>
  <p style="text-align:center;margin-top:16px"><a class="btn" href="/tap-chi/">← Tất cả bài viết</a></p>
</main>
{footer}
{MINI_JS}
</body>
</html>"""
    (OUT / f"{a['slug']}.html").write_text(page, encoding="utf-8")

cards = "".join(
    f'<a class="qa-card" href="/tap-chi/{a["slug"]}.html"><h3>{esc(a["title_vi"])}</h3>'
    f'<p>{esc(a["author"])} — {esc(a["intro_vi"][0][:130])}…</p></a>'
    for a in articles)
index = f"""{head("Tạp Chí Cải Chánh | Reformed Vietnam",
                   "Tạp chí trích đăng những chương tiêu biểu từ các tác phẩm thần học kinh điển thuộc phạm vi công cộng, kèm lời giới thiệu tiếng Việt.", BASE + "/tap-chi/")}
<body id="top">
{header}
<main class="wrap">
  <p class="crumb"><a href="/">Trang chủ</a> · Tạp Chí</p>
  <div class="cat-head">
    <div class="kicker">Tạp Chí Cải Chánh</div>
    <h1>Đọc Sâu, Nghĩ Sâu</h1>
    <p style="color:var(--ink-soft);max-width:640px;margin:0 auto">Tạp chí trích đăng những chương tiêu biểu nhất từ các tác phẩm kinh điển đã có trong thư viện — Spurgeon, Pink, Ryle và nhiều tác giả khác — kèm lời giới thiệu ngắn để bạn đọc có bối cảnh trước khi vào bài. Mỗi bài đều ghi rõ nguồn và tình trạng duyệt.</p>
    <p style="margin-top:10px"><span class="ai-label">Nội dung AI soạn, chưa duyệt</span></p>
  </div>
  <div class="qa-cards">{cards}</div>
</main>
{footer}
{MINI_JS}
</body>
</html>"""
(OUT / "index.html").write_text(index, encoding="utf-8")

sm = ROOT / "sitemap.xml"
t = sm.read_text(encoding="utf-8")
added = 0
for u in sitemap_urls:
    loc = f"<loc>{BASE}{u}</loc>"
    if loc not in t:
        t = t.replace("</urlset>", f"<url>{loc}<changefreq>monthly</changefreq></url></urlset>")
        added += 1
sm.write_text(t, encoding="utf-8")
print(f"journal articles: {len(articles)} | sitemap: {added} URLs added")
print("DONE")

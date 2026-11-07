#!/usr/bin/env python3
"""Build the Hymns & Worship module for Reformed Vietnam (Guide Phase D, §7.8).

Rule from the Guide: only hymns public domain in BOTH words and music, with
the basis recorded per hymn (data/hymns.json). The Vietnamese lyrics are the
project's own new translations, written to each hymn's exact meter so they
can be sung to the original tune, labelled "Bản dịch AI, chưa duyệt". No
sheet music or audio is hosted. Outputs: thanh-ca/index.html,
thanh-ca/<slug>.html, sitemap additions.
"""
import json, re, html, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = "https://reformed-vietnam.vercel.app"
data = json.loads((ROOT / "data/hymns.json").read_text(encoding="utf-8"))
entries = data["entries"]

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
      /* ---------- hymns module ---------- */
      .crumb { font-size: 13.5px; color: var(--ink-soft); margin: 26px 0 6px; }
      .crumb a { color: var(--burgundy); text-decoration: none; }
      .cat-head { text-align: center; padding: 18px 0 6px; }
      .cat-head .kicker { color: var(--gold-text); font-weight: 700; letter-spacing: .08em; text-transform: uppercase; font-size: 12.5px; }
      .cat-head h1 { font-family: "Playfair Display", serif; font-size: clamp(25px, 4.4vw, 36px); margin: 8px 0 10px; line-height: 1.3; }
      .cat-panel { max-width: 680px; margin: 18px auto 8px; background: var(--surface); border: 1px solid var(--line); border-radius: var(--radius); padding: 26px 26px 20px; box-shadow: var(--shadow); }
      .ai-label { display: inline-block; font-size: 12px; font-weight: 600; color: var(--burgundy); background: color-mix(in srgb, var(--burgundy) 9%, transparent); border: 1px solid color-mix(in srgb, var(--burgundy) 35%, transparent); padding: 2px 9px; border-radius: 999px; }
      .meta-table { width: 100%; border-collapse: collapse; margin: 4px 0 14px; font-size: 15px; }
      .meta-table th { text-align: left; color: var(--ink-soft); font-weight: 600; padding: 6px 10px 6px 0; white-space: nowrap; vertical-align: top; }
      .meta-table td { padding: 6px 0; }
      .meta-table a { color: var(--burgundy); }
      .lyrics { font-family: "Noto Serif", serif; font-size: 17.5px; line-height: 1.85; margin: 10px 0 4px; }
      .lyrics .verse { margin: 0 0 18px; }
      .lyrics .verse-num { font-family: "Be Vietnam Pro", sans-serif; font-size: 12.5px; font-weight: 700; color: var(--gold-text); letter-spacing: .06em; }
      .lyrics p { margin: 2px 0; }
      .refrain { border-left: 3px solid var(--gold-text); padding-left: 14px; }
      .orig { border-top: 1px solid var(--line); margin-top: 14px; padding-top: 10px; }
      .orig summary { cursor: pointer; font-weight: 600; color: var(--burgundy); font-size: 15px; }
      .orig .lyrics { font-size: 15.5px; color: var(--ink-soft); }
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

def verses_html(verses, refrain=None, refrain_label="Điệp khúc"):
    out = []
    for i, v in enumerate(verses, 1):
        lines = "".join(f"<p>{esc(l)}</p>" for l in v)
        out.append(f'<div class="verse"><span class="verse-num">CÂU {i}</span>{lines}</div>')
        if refrain and i == 1:
            rl = "".join(f"<p>{esc(l)}</p>" for l in refrain)
            out.append(f'<div class="verse refrain"><span class="verse-num">{refrain_label.upper()}</span>{rl}</div>')
    return "".join(out)

OUT = ROOT / "thanh-ca"
OUT.mkdir(exist_ok=True)
sitemap_urls = ["/thanh-ca/"]

for e in entries:
    url = f"{BASE}/thanh-ca/{e['slug']}.html"
    sitemap_urls.append(f"/thanh-ca/{e['slug']}.html")
    rows = [
        ("Lời", f"{esc(e['words_by'])} ({esc(e['words_years'])}), {e['words_year']}"),
        ("Giai điệu", f"{esc(e['tune'])} — {esc(e['tune_by'])}, {e['tune_year']}"),
        ("Thể điệu", esc(e["meter"]) + " — bản dịch giữ đúng số âm tiết từng dòng để hát theo giai điệu gốc"),
    ]
    if e.get("scripture"):
        bid, ch = e["scripture_passage"].split(":")
        rows.append(("Kinh Thánh", f'<a href="/kinh-thanh/{bid}/{ch}.html">{esc(e["scripture"])}</a>'))
    meta = "".join(f"<tr><th>{k}</th><td>{v}</td></tr>" for k, v in rows)
    orig = (f'<details class="orig"><summary>Nguyên bản tiếng Anh (thuộc phạm vi công cộng)</summary>'
            f'<div class="lyrics">{verses_html(e["en"], e.get("refrain_en"))}</div></details>')
    page = f"""{head(e["title_vi"] + " — Thánh Ca | Reformed Vietnam",
                     f"Thánh ca {e['title_en']} ({e['words_by']}, {e['words_year']}) với bản dịch tiếng Việt mới hát được theo giai điệu {e['tune']}.", url)}
<body id="top">
{header}
<main class="wrap">
  <p class="crumb"><a href="/">Trang chủ</a> · <a href="/thanh-ca/">Thánh Ca</a></p>
  <div class="cat-head">
    <div class="kicker">Thánh Ca &amp; Thờ Phượng</div>
    <h1>{esc(e["title_vi"])}</h1>
    <p style="color:var(--ink-soft)">{esc(e["title_en"])} · {esc(e["words_by"])}, {e["words_year"]}</p>
    <p style="margin-top:10px"><span class="ai-label">Bản dịch AI, chưa duyệt</span></p>
  </div>
  <article class="cat-panel">
    <table class="meta-table">{meta}</table>
    <div class="lyrics">{verses_html(e["vi"], e.get("refrain_vi"))}</div>
    {orig}
    <p class="basis">Cơ sở đăng tải: {esc(e["basis"])}. Bản dịch tiếng Việt trên đây là bản dịch mới của dự án (AI dịch, chưa duyệt), không sao chép bất kỳ bản dịch thánh ca hiện có nào.</p>
    {share_row(url)}
  </article>
  <p style="text-align:center;margin-top:16px"><a class="btn" href="/thanh-ca/">← Tất cả thánh ca</a></p>
</main>
{footer}
{MINI_JS}
</body>
</html>"""
    (OUT / f"{e['slug']}.html").write_text(page, encoding="utf-8")

cards = "".join(
    f'<a class="qa-card" href="/thanh-ca/{e["slug"]}.html"><h3>{esc(e["title_vi"])}</h3>'
    f'<p>{esc(e["title_en"])} · {esc(e["words_by"])} ({e["words_year"]}) · Giai điệu {esc(e["tune"])}</p></a>'
    for e in entries)
index = f"""{head("Thánh Ca & Thờ Phượng | Reformed Vietnam",
                   "Những thánh ca truyền thống thuộc phạm vi công cộng cả lời và nhạc, với bản dịch tiếng Việt mới hát được theo đúng giai điệu gốc.", BASE + "/thanh-ca/")}
<body id="top">
{header}
<main class="wrap">
  <p class="crumb"><a href="/">Trang chủ</a> · Thánh Ca</p>
  <div class="cat-head">
    <div class="kicker">Thánh Ca &amp; Thờ Phượng</div>
    <h1>Thánh Ca Truyền Thống</h1>
    <p style="color:var(--ink-soft);max-width:640px;margin:0 auto">Những thánh ca đã nuôi dưỡng Hội Thánh qua nhiều thế kỷ, được chọn theo nguyên tắc: cả lời và nhạc đều thuộc phạm vi công cộng, và cơ sở được ghi rõ cho từng bài. Mỗi bài có bản dịch tiếng Việt mới, dịch theo đúng thể điệu để hát được theo giai điệu gốc, cùng nguyên bản tiếng Anh để đối chiếu.</p>
    <p style="margin-top:10px"><span class="ai-label">Bản dịch AI, chưa duyệt</span></p>
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
print(f"hymn pages: {len(entries)} | sitemap: {added} URLs added")
print("DONE")

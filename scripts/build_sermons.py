#!/usr/bin/env python3
"""Build the Sermon Library for Reformed Vietnam (Guide Phase D, §7.7).

Rule from the Guide: metadata and links to the original sermon source only.
No sermon transcript is hosted here; where our own library already hosts a
Vietnamese translation (Edwards), the sermon page links to it. Source of
truth: data/sermons.json (each entry records its public-domain basis).
Outputs: bai-giang/index.html, bai-giang/<slug>.html, sitemap additions.
"""
import json, re, html, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = "https://reformedvietnam.com"
data = json.loads((ROOT / "data/sermons.json").read_text(encoding="utf-8"))
entries, collections = data["entries"], data["collections"]

# ---- template parts (same pattern as the other module builders) ----
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

      /* ---------- sermons module ---------- */
      .crumb { font-size: 13.5px; color: var(--ink-soft); margin: 26px 0 6px; }
      .crumb a { color: var(--burgundy); text-decoration: none; }
      .cat-head { text-align: center; padding: 18px 0 6px; }
      .cat-head .kicker { color: var(--gold-text); font-weight: 700; letter-spacing: .08em; text-transform: uppercase; font-size: 12.5px; }
      .cat-head h1 { font-family: "Playfair Display", serif; font-size: clamp(25px, 4.4vw, 36px); margin: 8px 0 10px; line-height: 1.3; }
      .cat-panel { max-width: 680px; margin: 18px auto 8px; background: var(--surface); border: 1px solid var(--line); border-radius: var(--radius); padding: 26px 26px 20px; box-shadow: var(--shadow); }
      .ans-body p { font-family: "Noto Serif", serif; font-size: 16.5px; line-height: 1.75; }
      .ai-label { display: inline-block; font-size: 12px; font-weight: 600; color: var(--burgundy); background: color-mix(in srgb, var(--burgundy) 9%, transparent); border: 1px solid color-mix(in srgb, var(--burgundy) 35%, transparent); padding: 2px 9px; border-radius: 999px; }
      .meta-table { width: 100%; border-collapse: collapse; margin: 4px 0 14px; font-size: 15px; }
      .meta-table th { text-align: left; color: var(--ink-soft); font-weight: 600; padding: 6px 10px 6px 0; white-space: nowrap; vertical-align: top; }
      .meta-table td { padding: 6px 0; }
      .meta-table a { color: var(--burgundy); }
      .share-row { display: flex; gap: 10px; justify-content: center; margin: 18px 0 4px; flex-wrap: wrap; }
      .rel-links a { display: inline-block; margin: 0 8px 8px 0; }
      .qa-cards { display: grid; gap: 14px; max-width: 760px; margin: 18px auto 8px; }
      .qa-card { display: block; background: var(--surface); border: 1px solid var(--line); border-radius: var(--radius); padding: 20px 22px; box-shadow: var(--shadow); text-decoration: none; }
      .qa-card h3 { font-family: "Noto Serif", serif; font-size: 18.5px; margin: 0 0 6px; color: var(--ink); line-height: 1.45; }
      .qa-card p { margin: 0; color: var(--ink-soft); font-size: 15px; line-height: 1.6; }
      .qa-card:hover h3 { color: var(--burgundy); }
      .basis { font-size: 13px; color: var(--ink-soft); border-top: 1px solid var(--line); padding-top: 10px; margin-top: 16px; line-height: 1.6; }
      /* ---------- design pass 2026-11: title band / monogram cards / rhythm ---------- */
      .title-band { max-width: 860px; margin: 16px auto 6px; background: linear-gradient(120deg, var(--burgundy-deep), var(--burgundy)); border-radius: var(--radius); box-shadow: var(--shadow); padding: 26px 28px; display: flex; gap: 22px; align-items: center; }
      .title-band .tb-kicker { color: #eccf8f; font-weight: 700; letter-spacing: .09em; text-transform: uppercase; font-size: 12.5px; }
      .title-band h1 { font-family: "Playfair Display", serif; font-size: clamp(24px, 4.2vw, 34px); line-height: 1.32; margin: 6px 0 4px; color: #fdf6e9; }
      .title-band .tb-sub { color: #efdfc2; font-size: 15px; margin: 4px 0 0; }
      .title-band .ai-label { background: rgba(255,255,255,.14); border-color: rgba(255,255,255,.45); color: #fdf6e9; }
      .medallion { flex: 0 0 auto; width: 84px; height: 84px; border-radius: 50%; border: 2px solid #eccf8f; display: flex; flex-direction: column; align-items: center; justify-content: center; font-family: "Playfair Display", serif; color: #fdf6e9; text-align: center; padding: 4px; }
      .medallion .m-big { font-size: 27px; font-weight: 700; line-height: 1; letter-spacing: .04em; }
      .medallion .m-small { font-size: 10.5px; letter-spacing: .08em; text-transform: uppercase; font-family: "Be Vietnam Pro", sans-serif; margin-top: 3px; color: #eccf8f; }
      @media (max-width: 560px) { .title-band { flex-direction: column; text-align: center; padding: 22px 18px; } .medallion { width: 70px; height: 70px; } .medallion .m-big { font-size: 22px; } }
      @media (prefers-color-scheme: dark) { .title-band { background: linear-gradient(120deg, #241611, #571d22); } }
      .qa-card { display: flex; gap: 16px; align-items: flex-start; }
      .monogram { flex: 0 0 auto; width: 52px; height: 52px; border-radius: 50%; background: var(--burgundy); color: #fdf6e9; font-family: "Playfair Display", serif; font-weight: 700; font-size: 19px; letter-spacing: .03em; display: flex; align-items: center; justify-content: center; margin-top: 2px; box-shadow: var(--shadow); }
      .band-tint { max-width: 860px; margin: 34px auto 8px; background: color-mix(in srgb, var(--burgundy) 6%, var(--bg)); border-top: 2px solid var(--gold-soft); border-radius: var(--radius); padding: 6px 18px 20px; }
      .band-tint .qa-cards { margin-top: 10px; }
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

def initials(name):
    """Monogram initials from an existing preacher/author name: first + last word."""
    words = [w for w in re.split(r"\s+", str(name).strip()) if w]
    return (words[0][0] + words[-1][0]).upper() if words else ""

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

OUT = ROOT / "bai-giang"
OUT.mkdir(exist_ok=True)
sitemap_urls = ["/bai-giang/"]

for e in entries:
    url = f"{BASE}/bai-giang/{e['slug']}.html"
    sitemap_urls.append(f"/bai-giang/{e['slug']}.html")
    bid, ch = e["text_passage"].split(":")
    rows = [
        ("Người giảng", f"{esc(e['preacher'])} ({esc(e['preacher_years'])})"),
        ("Ngày giảng", esc(e["date_vi"])),
        ("Nơi giảng", esc(e["venue"])),
        ("Câu gốc", f'<a href="/kinh-thanh/{bid}/{ch}.html">{esc(e["text_ref_vi"])}</a>'),
    ]
    if e.get("sermon_no"):
        rows.append(("Số hiệu", esc(e["sermon_no"]) + " trong tuyển tập bài giảng của tác giả"))
    meta = "".join(f"<tr><th>{k}</th><td>{v}</td></tr>" for k, v in rows)
    intro = "".join(f"<p>{esc(p)}</p>" for p in e["intro_vi"])
    vi_btn = (f'<a class="btn solid" href="{esc(e["read_vi_url"])}">Đọc bản dịch tiếng Việt trong thư viện →</a> '
              if e.get("read_vi_url") else "")
    page = f"""{head(e["title_vi"] + " — " + e["preacher"] + " | Thư Viện Bài Giảng", e["intro_vi"][0][:150], url)}
<body id="top">
{header}
<main class="wrap">
  <p class="crumb"><a href="/">Trang chủ</a> · <a href="/bai-giang/">Bài Giảng</a> · {esc(e["preacher"])}</p>
  <div class="title-band">
    <div class="medallion"><span class="m-big">{esc(initials(e["preacher"]))}</span><span class="m-small">Bài giảng</span></div>
    <div>
      <div class="tb-kicker">Thư Viện Bài Giảng</div>
      <h1>{esc(e["title_vi"])}</h1>
      <p class="tb-sub">{esc(e["title_en"])} · {esc(e["preacher"])} &nbsp;<span class="ai-label">Nội dung AI soạn, chưa duyệt</span></p>
    </div>
  </div>
  <article class="cat-panel">
    <table class="meta-table">{meta}</table>
    <div class="ans-body">{intro}</div>
    <div class="rel-links" style="margin-top:16px">{vi_btn}<a class="btn{' solid' if not e.get('read_vi_url') else ''}" target="_blank" rel="noopener" href="{esc(e["source_url"])}">Đọc toàn văn tiếng Anh tại nguồn →</a> <a class="btn" href="/kinh-thanh/{bid}/{ch}.html">Đọc phân đoạn Kinh Thánh →</a></div>
    <p class="basis">Cơ sở đăng tải: {esc(e["basis"])}. Trang này chỉ giới thiệu và liên kết đến nguồn gốc; toàn văn bài giảng không được sao chép về máy chủ của chúng ta.</p>
    {share_row(url)}
  </article>
  <p style="text-align:center;margin-top:16px"><a class="btn" href="/bai-giang/">← Tất cả bài giảng</a></p>
</main>
{footer}
{MINI_JS}
</body>
</html>"""
    (OUT / f"{e['slug']}.html").write_text(page, encoding="utf-8")

vi_cards = "".join(
    f'<a class="qa-card" href="{esc(v["local_url"])}"><span class="monogram">{esc(initials(v["preacher"]))}</span><span><h3>{esc(v["title_vi"])}</h3>'
    f'<p>{esc(v["preacher"])}' + (f' · {esc(v["text_ref_vi"])}' if v.get("text_ref_vi") else "") +
    f' — {esc(v["blurb_vi"])}</p></span></a>'
    for v in data.get("vi_sermons", []))
cards = "".join(
    f'<a class="qa-card" href="/bai-giang/{e["slug"]}.html"><span class="monogram">{esc(initials(e["preacher"]))}</span><span><h3>{esc(e["title_vi"])}</h3>'
    f'<p>{esc(e["preacher"])} · {esc(e["date_vi"])} · Câu gốc: {esc(e["text_ref_vi"])}</p></span></a>'
    for e in entries)
col_cards = "".join(
    f'<a class="qa-card" href="{esc(c["url"])}"><span class="monogram">{esc(initials(c["author"]))}</span><span><h3>{esc(c["title_vi"])}</h3>'
    f'<p>{esc(c["author"])} — {esc(c["note_vi"])}</p></span></a>'
    for c in collections)
index = f"""{head("Thư Viện Bài Giảng Cải Chánh | Reformed Vietnam",
                   "Những bài giảng kinh điển của Spurgeon, Edwards và các mục sư Cải Chánh — giới thiệu tiếng Việt, sắp xếp theo phân đoạn Kinh Thánh, liên kết toàn văn tại nguồn gốc.", BASE + "/bai-giang/")}
<body id="top">
{header}
<main class="wrap">
  <p class="crumb"><a href="/">Trang chủ</a> · Bài Giảng</p>
  <div class="cat-head">
    <div class="kicker">Thư Viện Bài Giảng</div>
    <h1>Bài Giảng Kinh Điển</h1>
    <p style="color:var(--ink-soft);max-width:640px;margin:0 auto">Những bài giảng đã được thời gian thử thách của các mục sư Cải Chánh và Thanh Giáo, sắp xếp theo phân đoạn Kinh Thánh. Một số bài đã có trọn bản dịch tiếng Việt; các bài còn lại được giới thiệu bằng tiếng Việt và liên kết đến toàn văn tại nguồn gốc — chúng tôi không sao chép toàn văn khi chưa có phép của người giữ bản quyền.</p>
    <p style="margin-top:10px"><span class="ai-label">Nội dung AI soạn, chưa duyệt</span></p>
  </div>
  <div class="cat-head" style="margin-top:26px">
    <div class="kicker">Đã Có Tiếng Việt</div>
    <h1 style="font-size:clamp(22px,3.6vw,29px)">Bài Giảng Có Bản Dịch Tiếng Việt</h1>
  </div>
  <div class="qa-cards">{vi_cards}</div>
  <section class="band-tint">
  <div class="cat-head" style="margin-top:20px">
    <div class="kicker">Toàn Văn Tại Nguồn</div>
    <h1 style="font-size:clamp(22px,3.6vw,29px)">Bài Giảng Kinh Điển Của Spurgeon</h1>
    <p style="color:var(--ink-soft);max-width:640px;margin:0 auto">Giới thiệu và dữ kiện bằng tiếng Việt; toàn văn tiếng Anh tại The Spurgeon Library.</p>
  </div>
  <div class="qa-cards">{cards}</div>
  </section>
  <div class="cat-head" style="margin-top:34px">
    <div class="kicker">Trong Thư Viện Sách</div>
    <h1 style="font-size:clamp(22px,3.6vw,29px)">Tuyển Tập Bài Giảng Tiếng Việt</h1>
    <p style="color:var(--ink-soft);max-width:640px;margin:0 auto">Các tuyển tập bài giảng trọn bộ đã có bản dịch tiếng Việt ngay trong thư viện sách của chúng tôi.</p>
  </div>
  <div class="qa-cards">{col_cards}</div>
</main>
{footer}
{MINI_JS}
</body>
</html>"""
(OUT / "index.html").write_text(index, encoding="utf-8")

# sitemap: append missing entries (bounded, no pattern spans)
sm = ROOT / "sitemap.xml"
t = sm.read_text(encoding="utf-8")
added = 0
for u in sitemap_urls:
    loc = f"<loc>{BASE}{u}</loc>"
    if loc not in t:
        t = t.replace("</urlset>", f"<url>{loc}<changefreq>monthly</changefreq></url></urlset>")
        added += 1
sm.write_text(t, encoding="utf-8")
print(f"sermon pages: {len(entries)} | sitemap: {added} URLs added")
print("DONE")

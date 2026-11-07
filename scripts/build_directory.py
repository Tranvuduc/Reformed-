#!/usr/bin/env python3
"""Build the Church Directory for Reformed Vietnam (Guide Phase D, §7.10).

Launch format (owner decision 2026-11-07: proceed without waiting for a
consent round): the directory lists only information a church itself
submits — submission IS the consent — and every listing carries the
correction/removal process from day one. No scraping, no bulk import, no
invented entries. Source of truth: data/churches.json (entries grouped by
region). Outputs: danh-ba/index.html, sitemap addition.
"""
import json, re, html, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
BASE = "https://reformed-vietnam.vercel.app"
data = json.loads((ROOT / "data/churches.json").read_text(encoding="utf-8"))
entries, regions = data["entries"], data["regions"]
EMAIL = "reformedvn@gmail.com"

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
      /* ---------- directory module ---------- */
      .crumb { font-size: 13.5px; color: var(--ink-soft); margin: 26px 0 6px; }
      .crumb a { color: var(--burgundy); text-decoration: none; }
      .cat-head { text-align: center; padding: 18px 0 6px; }
      .cat-head .kicker { color: var(--gold-text); font-weight: 700; letter-spacing: .08em; text-transform: uppercase; font-size: 12.5px; }
      .cat-head h1 { font-family: "Playfair Display", serif; font-size: clamp(25px, 4.4vw, 36px); margin: 8px 0 10px; line-height: 1.3; }
      .cat-panel { max-width: 680px; margin: 18px auto 8px; background: var(--surface); border: 1px solid var(--line); border-radius: var(--radius); padding: 26px 26px 20px; box-shadow: var(--shadow); }
      .cat-panel p, .cat-panel li { font-size: 15.5px; line-height: 1.7; }
      .cat-panel h2 { font-family: "Playfair Display", serif; font-size: 21px; margin: 20px 0 8px; }
      .cat-panel h2:first-child { margin-top: 0; }
      .qa-cards { display: grid; gap: 14px; max-width: 760px; margin: 18px auto 8px; }
      .qa-card { display: block; background: var(--surface); border: 1px solid var(--line); border-radius: var(--radius); padding: 20px 22px; box-shadow: var(--shadow); text-decoration: none; }
      .qa-card h3 { font-family: "Noto Serif", serif; font-size: 18.5px; margin: 0 0 6px; color: var(--ink); line-height: 1.45; }
      .qa-card p { margin: 0; color: var(--ink-soft); font-size: 15px; line-height: 1.6; }
      .empty { text-align: center; color: var(--ink-soft); font-size: 15px; padding: 10px 0 2px; }
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

region_html = []
for r in regions:
    items = [e for e in entries if e.get("region") == r]
    if items:
        def card(e):
            lines = [esc(e.get(k, "")) for k in ("address", "service_times", "contact", "confession") if e.get(k)]
            src = ""
            if e.get("source_url"):
                src = (f'<p style="margin-top:8px;font-size:13px">Nguồn: <a href="{esc(e["source_url"])}" '
                       f'target="_blank" rel="noopener">{esc(e.get("source_name", "nguồn công khai"))}</a>'
                       f' · Thông tin công khai, chưa xác nhận trực tiếp với Hội Thánh — Hội Thánh có thể yêu cầu sửa hoặc gỡ bất cứ lúc nào.</p>')
            return (f'<div class="qa-card"><h3>{esc(e["name"])}</h3>'
                    f'<p>{"<br>".join(lines)}</p>{src}</div>')
        cards = "".join(card(e) for e in items)
        region_html.append(f'<div class="cat-head" style="margin-top:30px"><div class="kicker">{esc(r)}</div></div><div class="qa-cards">{cards}</div>')
    else:
        region_html.append(f'<div class="cat-head" style="margin-top:30px"><div class="kicker">{esc(r)}</div></div><p class="empty">Chưa có Hội Thánh nào đăng ký trong khu vực này.</p>')

mailto = ("mailto:" + EMAIL + "?subject=" + "Đăng ký Hội Thánh vào Danh Bạ" +
          "&body=" + "Tên Hội Thánh:%0AĐịa chỉ:%0AGiờ nhóm:%0AĐiện thoại / email liên hệ:%0AHệ phái / tín ngưỡng tuyên xưng:%0A")
page = f"""{head("Danh Bạ Hội Thánh Cải Chánh | Reformed Vietnam",
                 "Tìm Hội Thánh Cải Chánh gần nơi bạn ở — thông tin do chính các Hội Thánh gửi đăng ký, kèm quy trình sửa và gỡ minh bạch.", BASE + "/danh-ba/")}
<body id="top">
{header}
<main class="wrap">
  <p class="crumb"><a href="/">Trang chủ</a> · Danh Bạ Hội Thánh</p>
  <div class="cat-head">
    <div class="kicker">Danh Bạ Hội Thánh</div>
    <h1>Hội Thánh Cải Chánh Gần Bạn</h1>
    <p style="color:var(--ink-soft);max-width:640px;margin:0 auto">Danh bạ được biên soạn từ các danh bạ và nguồn thông tin công khai — nguồn được ghi rõ dưới mỗi mục — và tiếp nhận đăng ký trực tiếp từ các Hội Thánh. Nếu thông tin của Hội Thánh bạn chưa đúng, chỉ cần liên hệ để chúng tôi sửa hoặc gỡ ngay.</p>
  </div>
  <article class="cat-panel">
    <h2>Đăng ký Hội Thánh của bạn</h2>
    <p>Gửi email đến <a href="{mailto}">{EMAIL}</a> với các thông tin sau:</p>
    <ul>
      <li>Tên Hội Thánh và địa chỉ nhóm họp</li>
      <li>Giờ nhóm chính và các buổi nhóm khác (nếu có)</li>
      <li>Điện thoại hoặc email liên hệ của Hội Thánh</li>
      <li>Tín ngưỡng tuyên xưng của Hội Thánh (ví dụ: Tín Lý Westminster)</li>
    </ul>
    <p><a class="btn solid" href="{mailto}">Gửi đăng ký →</a></p>
    <h2>Sửa hoặc gỡ thông tin</h2>
    <p>Nếu thông tin của Hội Thánh bạn thay đổi hoặc bạn muốn gỡ khỏi danh bạ, chỉ cần email đến {EMAIL} — chúng tôi sẽ sửa trong lần cập nhật gần nhất và gỡ ngay khi người đại diện Hội Thánh yêu cầu, không cần giải thích lý do.</p>
    <h2>Nguyên tắc đăng</h2>
    <p>Danh bạ chỉ gồm các Hội Thánh thuộc truyền thống Cải chính (Trưởng lão, Cải chánh, Báp-tít Cải chánh…) có thông tin công khai có thể kiểm chứng. Mỗi mục đều ghi nguồn; thông tin từ danh bạ công khai được đánh dấu là chưa xác nhận trực tiếp với Hội Thánh. Khi Hội Thánh đăng ký hoặc liên hệ trực tiếp, thông tin của Hội Thánh sẽ được cập nhật theo dữ liệu Hội Thánh cung cấp và bỏ đánh dấu chưa xác nhận.</p>
  </article>
  {''.join(region_html)}
</main>
{footer}
{MINI_JS}
</body>
</html>"""
OUT = ROOT / "danh-ba"
OUT.mkdir(exist_ok=True)
(OUT / "index.html").write_text(page, encoding="utf-8")

sm = ROOT / "sitemap.xml"
t = sm.read_text(encoding="utf-8")
loc = f"<loc>{BASE}/danh-ba/</loc>"
if loc not in t:
    t = t.replace("</urlset>", f"<url>{loc}<changefreq>monthly</changefreq></url></urlset>")
    sm.write_text(t, encoding="utf-8")
    print("sitemap: 1 URL added")
print(f"directory entries rendered: {len(entries)}")
print("DONE")

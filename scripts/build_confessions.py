#!/usr/bin/env python3
"""Phase 2, item 2.2 — Confessions library (Thư viện Tuyên Xưng).

Builds /tuyen-xung/ (index) and /tuyen-xung/<id>.html for each AVAILABLE
confession in scripts/helper-data/confessions.json. Texts that are NOT in
the library yet (Westminster Confession full text, 1689 London Baptist
Confession, Westminster Larger Catechism) appear on the index ONLY, marked
'Sắp ra mắt — cần dịch', with links to what IS available meanwhile. No
confession text is written or invented here — detail pages link to the
existing Vietnamese translations in /ban-dich/.

Every link is checked against the repo (hub_page.check_links).
"""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from hub_page import (BASE, ROOT, head, header, footer, MINI_JS, share_row,
                      report_mailto, write_if_changed, check_links, sitemap_add)

OUT = ROOT / "tuyen-xung"

CONF_CSS = """
      .conf-card { max-width: 860px; margin: 16px auto 0; padding: 20px; border: 1px solid var(--line); border-radius: 12px; background: rgba(255,255,255,.35); }
      .conf-card h2, .conf-card h3 { font-family: "Playfair Display", serif; margin: 0 0 6px; }
      .conf-card h2 { font-size: 21px; }
      .conf-card .meta { color: var(--gold-text); font-weight: 700; font-size: 13px; letter-spacing: .04em; margin-bottom: 8px; }
      .conf-card p { color: var(--ink-soft); margin: 0 0 10px; }
      .conf-card ul { margin: 0; padding-left: 20px; }
      .conf-card li { margin: 4px 0; }
      .conf-card li a { color: var(--gold-text); }
      .planned { opacity: .92; border-style: dashed; }
      .detail { max-width: 860px; margin: 20px auto 0; }
      .detail p { color: var(--ink-soft); }
      .detail h2 { font-family: "Playfair Display", serif; font-size: 21px; margin: 22px 0 8px; }
      .detail ul { padding-left: 20px; }
      .detail li { margin: 5px 0; }
      .detail li a { color: var(--gold-text); }
"""

def card(c, link=True):
    badge = ('<span class="ai-label">Bản dịch AI, chưa duyệt</span>'
             if c["status"] == "available"
             else '<span class="ai-label">Sắp ra mắt — cần dịch</span>')
    title = (f'<a href="/tuyen-xung/{c["id"]}.html" style="color:inherit">{c["title"]}</a>'
             if link and c["status"] == "available" else c["title"])
    read = (f'<p><a class="btn solid" href="/ban-dich/{c["ban_dich"]}.html">Đọc toàn văn →</a></p>'
            if c["status"] == "available" else "")
    links = ""
    if c.get("links"):
        lis = "".join(f'<li><a href="{l["url"]}">{l["label"]}</a></li>' for l in c["links"])
        links = f"<ul>{lis}</ul>"
    cls = "conf-card" + (" planned" if c["status"] == "planned" else "")
    return (f'<article class="{cls}"><h2>{title}</h2>'
            f'<div class="meta">{c["author"]} · {c["year"]} · {c["title_en"]}</div>'
            f'<p>{c["desc"]}</p>{read}<p style="margin-top:6px">{badge}</p>{links}</article>')

def build_detail(c):
    url = f"{BASE}/tuyen-xung/{c['id']}.html"
    links = "".join(f'<li><a href="{l["url"]}">{l["label"]}</a></li>' for l in c["links"])
    page = f"""{head(c["title"] + " | Thư viện Tuyên Xưng | Reformed Vietnam",
                     c["desc"], url, CONF_CSS)}
<body id="top">
{header}
<main class="wrap">
  <p class="crumb"><a href="/">Trang chủ</a> · <a href="/tuyen-xung/">Thư viện Tuyên Xưng</a></p>
  <div class="cat-head">
    <div class="kicker">Thư viện Tuyên Xưng</div>
    <h1>{c["title"]}</h1>
    <p style="color:var(--gold-text);font-weight:700">{c["author"]} · {c["year"]} · {c["title_en"]}</p>
    <p style="margin-top:10px"><span class="ai-label">Bản dịch AI, chưa duyệt</span></p>
  </div>
  <div class="detail">
    <p>{c["intro"]}</p>
    <h2>Cấu trúc</h2>
    <p>{c["structure"]}</p>
    <p><a class="btn solid" href="/ban-dich/{c["ban_dich"]}.html">Đọc toàn văn trong thư viện →</a></p>
    <h2>Đọc thêm</h2>
    <ul>{links}</ul>
  </div>
  <p style="text-align:center;margin-top:26px"><a class="btn" href="/tuyen-xung/">← Tất cả bản tuyên xưng</a></p>
  {share_row(url)}
  {report_mailto(c["title"])}
</main>
{footer}
{MINI_JS}
</body>
</html>"""
    changed = write_if_changed(OUT / f"{c['id']}.html", page)
    print(f"  /tuyen-xung/{c['id']}.html — {'written' if changed else 'unchanged'}")
    return page

def main():
    data = json.loads((ROOT / "scripts/helper-data/confessions.json").read_text(encoding="utf-8"))
    confs = data["confessions"]
    available = [c for c in confs if c["status"] == "available"]
    planned = [c for c in confs if c["status"] == "planned"]
    assert len(available) == 7 and len(planned) == 3, f"expected 7+3, got {len(available)}+{len(planned)}"
    for c in available:
        assert (ROOT / "ban-dich" / f"{c['ban_dich']}.html").exists(), f"missing translation: {c['ban_dich']}"
    pages = []
    for c in available:
        pages.append((c, build_detail(c)))
    avail_cards = "".join(card(c) for c in available)
    planned_cards = "".join(card(c, link=False) for c in planned)
    url = f"{BASE}/tuyen-xung/"
    index = f"""{head("Thư viện Tuyên Xưng — Các bản tuyên xưng đức tin Cải Chánh | Reformed Vietnam",
                     "Các bản tuyên xưng và giáo lý vấn đáp của truyền thống Cải Chánh bằng tiếng Việt: Westminster, Heidelberg, Belgic, Helvetic, Keach và Spurgeon.", url, CONF_CSS)}
<body id="top">
{header}
<main class="wrap">
  <p class="crumb"><a href="/">Trang chủ</a></p>
  <div class="cat-head">
    <div class="kicker">Thư viện Tuyên Xưng</div>
    <h1>Các bản tuyên xưng đức tin</h1>
    <p style="max-width:640px;margin:0 auto;color:var(--ink-soft)">Tuyên xưng đức tin là cách Hội Thánh nói lại những gì Kinh Thánh dạy — ngắn gọn, chính xác, và được cả Hội Thánh cùng xưng nhận. Dưới đây là các bản tuyên xưng và giáo lý vấn đáp của truyền thống Cải Chánh đã có bản dịch tiếng Việt trong thư viện, cùng ba bản lớn đang chờ dịch.</p>
  </div>
  <div class="cat-band"><div class="cat-band-head"><h3>Đã có bản dịch tiếng Việt ({len(available)})</h3></div></div>
{avail_cards}
  <div class="cat-band"><div class="cat-band-head"><h3>Sắp ra mắt — đang chờ dịch ({len(planned)})</h3><span class="rng">dự kiến giao cho vòng dịch sắp tới</span></div>
  <p style="color:var(--ink-soft)">Ba bản tuyên xưng lớn dưới đây chưa có bản dịch tiếng Việt trong thư viện. Trong khi chờ, mỗi mục đều dẫn tới những gì đã có: sách bình luận và bản tuyên xưng gần nhất.</p></div>
{planned_cards}
  <p style="text-align:center;margin-top:26px"><a class="btn" href="/giao-ly/">Giáo Lý Vấn Đáp Ngắn — 107 câu</a> <a class="btn" href="/bach-khoa/tin-dieu.html">Bách Khoa: Tín điều</a></p>
  {share_row(url)}
  {report_mailto("Thư viện Tuyên Xưng")}
</main>
{footer}
{MINI_JS}
</body>
</html>"""
    pages.append(({"id": "index"}, index))
    # Write the index BEFORE the link check: detail pages link back to it.
    changed = write_if_changed(OUT / "index.html", index)
    print(f"  /tuyen-xung/ — {'written' if changed else 'unchanged'}")
    for c, page in pages:
        check_links(page, f"/tuyen-xung/{c['id']}.html")
    print("all links verified")
    added = sitemap_add(["/tuyen-xung/"] + [f"/tuyen-xung/{c['id']}.html" for c in available])
    print(f"sitemap: {added} URLs added")
    print("DONE")

if __name__ == "__main__":
    main()

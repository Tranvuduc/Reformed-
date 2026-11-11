#!/usr/bin/env python3
"""Phase 2, item 2.3 — Doctrinal hubs (Trung tâm giáo lý).

Builds /trung-tam-giao-ly/<id>.html for each hub in scripts/helper-data/
doctrine-hubs.json: Five Solas, TULIP, Covenant theology. Assembly only —
encyclopedia entries + books + WSC questions + Bible passages + Hoi Dap
questions that already exist. Every link is checked against the repo
(hub_page.check_links) before the page is written.

URL note: the hubs live under /trung-tam-giao-ly/, NOT /bach-khoa/, because
the encyclopedia already has entries at /bach-khoa/nam-sola.html,
/bach-khoa/tulip.html and /bach-khoa/than-hoc-giao-uoc.html — those entry
pages must not be overwritten.
"""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from hub_page import (BASE, ROOT, head, header, footer, MINI_JS, share_row,
                      report_mailto, write_if_changed, check_links, sitemap_add)

OUT = ROOT / "trung-tam-giao-ly"

HUB_CSS = """
      .hub-sec { max-width: 860px; margin: 26px auto 0; padding: 20px; border: 1px solid var(--line); border-radius: 12px; background: rgba(255,255,255,.35); }
      .hub-sec h2 { font-family: "Playfair Display", serif; font-size: 21px; margin: 0 0 8px; }
      .hub-sec .note { color: var(--ink-soft); margin: 0 0 12px; }
      .hub-sec h3 { font-size: 15px; margin: 14px 0 4px; color: var(--gold-text); }
      .hub-sec ul { margin: 0; padding-left: 20px; }
      .hub-sec li { margin: 5px 0; }
      .hub-sec li a { color: var(--gold-text); }
"""

def group_html(title, items):
    if not items:
        return ""
    lis = "".join(f'<li><a href="{it["url"]}">{it["label"]}</a></li>' for it in items)
    return f"<h3>{title}</h3><ul>{lis}</ul>"

def build_hub(h):
    url = f"{BASE}/trung-tam-giao-ly/{h['id']}.html"
    title = f"{h['title']} | Trung tâm giáo lý | Reformed Vietnam"
    secs = ""
    for s in h["sections"]:
        secs += (f'<section class="hub-sec"><h2>{s["title"]}</h2>'
                 f'<p class="note">{s["note"]}</p>'
                 + group_html("Thuật ngữ Bách Khoa", s.get("enc", []))
                 + group_html("Giáo Lý Vấn Đáp Ngắn", s.get("wsc", []))
                 + group_html("Sách trong thư viện", s.get("books", []))
                 + group_html("Câu Kinh Thánh", s.get("passages", []))
                 + group_html("Hỏi Đáp", s.get("questions", []))
                 + "</section>")
    page = f"""{head(title, h["desc"], url, HUB_CSS)}
<body id="top">
{header}
<main class="wrap">
  <p class="crumb"><a href="/">Trang chủ</a> · <a href="/bach-khoa/">Bách Khoa</a> · Trung tâm giáo lý</p>
  <div class="cat-head">
    <div class="kicker">Trung tâm giáo lý</div>
    <h1>{h["title"]}</h1>
    <p style="max-width:640px;margin:0 auto;color:var(--ink-soft)">{h["intro"]}</p>
  </div>
{secs}
  <p style="text-align:center;margin-top:26px"><a class="btn" href="/bach-khoa/">← Bách Khoa</a> <a class="btn" href="/bach-khoa/theo-chu-de.html">Học theo 10 lĩnh vực</a></p>
  {share_row(url)}
  {report_mailto(h["title"])}
</main>
{footer}
{MINI_JS}
</body>
</html>"""
    changed = write_if_changed(OUT / f"{h['id']}.html", page)
    print(f"  /trung-tam-giao-ly/{h['id']}.html — {len(h['sections'])} sections, {'written' if changed else 'unchanged'}")
    return page

def main():
    data = json.loads((ROOT / "scripts/helper-data/doctrine-hubs.json").read_text(encoding="utf-8"))
    pages = [(h, build_hub(h)) for h in data["hubs"]]
    for h, page in pages:
        check_links(page, f"/trung-tam-giao-ly/{h['id']}.html")
    print("all links verified")
    added = sitemap_add([f"/trung-tam-giao-ly/{h['id']}.html" for h in data["hubs"]])
    print(f"sitemap: {added} URLs added")
    print("DONE")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Phase 2, item 2.1 — Learning paths (Lộ trình học).

Builds /lo-trinh/<id>.html for each path in scripts/helper-data/
learning-paths.json. Assembly ONLY: every step links to a page that
already exists on the site (encyclopedia, WSC, book, Hoi Dap, Academy,
sermon, hymn, Bible passage, devotion). The 30-day new-believer path is
NOT rebuilt here — it already exists in full at /moi-tin-chua.html and
the paths index links to it.

Every link is checked against the repo (hub_page.check_links) before the
page is written; a dead link fails the build.
"""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from hub_page import (BASE, ROOT, head, header, footer, MINI_JS, share_row,
                      report_mailto, write_if_changed, check_links, sitemap_add)

OUT = ROOT / "lo-trinh"

PATHS_CSS = """
      .step { max-width: 860px; margin: 26px auto 0; padding: 20px; border: 1px solid var(--line); border-radius: 12px; background: rgba(255,255,255,.35); }
      .step h2 { font-family: "Playfair Display", serif; font-size: 21px; margin: 0 0 8px; }
      .step .note { color: var(--ink-soft); margin: 0 0 12px; }
      .step ul { margin: 0; padding-left: 20px; }
      .step li { margin: 5px 0; }
      .step li a { color: var(--gold-text); }
      .path-nav { display: flex; gap: 8px; flex-wrap: wrap; justify-content: center; max-width: 860px; margin: 18px auto 6px; }
"""

def build_path(p):
    url = f"{BASE}/lo-trinh/{p['id']}.html"
    title = f"{p['title']} | Lộ trình học | Reformed Vietnam"
    steps = ""
    for s in p["steps"]:
        links = "".join(
            f'<li><a href="{l["url"]}">{l["label"]}</a></li>' for l in s["links"])
        steps += (f'<section class="step"><h2>{s["title"]}</h2>'
                  f'<p class="note">{s["note"]}</p><ul>{links}</ul></section>')
    page = f"""{head(title, p["desc"], url, PATHS_CSS)}
<body id="top">
{header}
<main class="wrap">
  <p class="crumb"><a href="/">Trang chủ</a> · <a href="/lo-trinh.html">Lộ trình học</a></p>
  <div class="cat-head">
    <div class="kicker">Lộ trình học</div>
    <h1>{p["title"]}</h1>
    <p style="max-width:640px;margin:0 auto;color:var(--ink-soft)">{p["intro"]}</p>
  </div>
  <div class="path-nav"><a class="btn" href="/moi-tin-chua.html">Tôi mới tin Chúa — 30 ngày đầu tiên</a> <a class="btn" href="/lo-trinh/nam-sola.html">Năm Sola</a> <a class="btn" href="/lo-trinh/su-thanh-khiet.html">Sự nên thánh</a> <a class="btn" href="/lo-trinh/chuan-bi-giang-day.html">Chuẩn bị giảng dạy</a></div>
{steps}
  <p style="text-align:center;margin-top:26px"><a class="btn solid" href="/lo-trinh.html">← Tất cả lộ trình</a></p>
  {share_row(url)}
  {report_mailto(p["title"])}
</main>
{footer}
{MINI_JS}
</body>
</html>"""
    check_links_note = None  # checked after all pages exist (nav links siblings)
    changed = write_if_changed(OUT / f"{p['id']}.html", page)
    print(f"  /lo-trinh/{p['id']}.html — {len(p['steps'])} steps, {'written' if changed else 'unchanged'}")
    return page

def main():
    data = json.loads((ROOT / "scripts/helper-data/learning-paths.json").read_text(encoding="utf-8"))
    OUT.mkdir(exist_ok=True)
    pages = [(p, build_path(p)) for p in data["paths"]]
    # Link check AFTER all pages exist: each page's nav links its siblings.
    for p, page in pages:
        check_links(page, f"/lo-trinh/{p['id']}.html")
    print("all links verified")
    added = sitemap_add([f"/lo-trinh/{p['id']}.html" for p in data["paths"]])
    print(f"sitemap: {added} URLs added")
    print("DONE")

if __name__ == "__main__":
    main()

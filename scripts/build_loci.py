#!/usr/bin/env python3
"""Phase 2, item 2.4 — Loci index (Học theo lĩnh vực thần học).

Builds /bach-khoa/theo-chu-de.html from data/encyclopedia.json (which
carries the 'loci' tags applied by scripts/build_encyclopedia.py) and the
locus metadata in scripts/helper-data/encyclopedia-loci.json. Each locus
section lists its encyclopedia entries plus a few verified library books
whose catalogue 'topics' match the locus (book URLs verified to exist).

Asserts: every one of the 201 entries appears in exactly one locus.
"""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from hub_page import (BASE, ROOT, head, header, footer, MINI_JS, share_row,
                      report_mailto, write_if_changed, check_links, sitemap_add)
from topic_map import LOCI

# A few verified library books per locus, chosen from the catalogue's own
# 'topics' field (ids below were checked against translations/index.json
# and their /ban-dich/ pages exist). Kept small on purpose: the locus
# page is an index, not a bibliography.
LOCI_BOOKS = {
    "kinh-thanh": [("mg1-122-institutes-1541-calvin", "Calvin — Giáo Huấn Cơ Đốc Giáo (1541)"),
                   ("spurgeon-grace", "Spurgeon — Tất Cả Bởi Ân Điển")],
    "duc-chua-troi": [("mg1-121-institutes-of-the-christian-religion-reformed-theo-calvin", "Calvin — Giáo Lý Cơ Đốc Giáo"),
                      ("watson-bodyofdivinity", "Watson — Thân Thể Thần Học")],
    "chua-gie-xu": [("flavel-fountainoflife", "Flavel — Nguồn Sống Mở Ra"),
                    ("bunyan-grace", "Bunyan — Ân Điển Dư Dật Cho Kẻ Tội Lỗi Đầu Sỏ")],
    "duc-thanh-linh": [("owen-mort", "Owen — Giết Chết Tội Lỗi"),
                       ("edwards-affections", "Edwards — Các Cảm Xúc Thuộc Linh")],
    "con-nguoi": [("arch-humannaturein00bost", "Boston — Bản Chất Con Người Trong Bốn Trạng Thái"),
                  ("001-pilgrims-progress-bunyan", "Bunyan — Hành Trình Của Người Lữ Hành")],
    "su-cuu-roi": [("spurgeon-grace", "Spurgeon — Tất Cả Bởi Ân Điển"),
                   ("bonar-followlamb", "Bonar — Theo Chiên Con")],
    "hoi-thanh": [("baxter-pastor", "Baxter — Người Chăn Bầy Cải Chánh"),
                  ("spurgeon-lectures-to-my-students", "Spurgeon — Các Bài Giảng Cho Sinh Viên")],
    "tan-the": [("001-pilgrims-progress-bunyan", "Bunyan — Hành Trình Của Người Lữ Hành"),
                ("ryle-holiness", "Ryle — Sự Nên Thánh")],
    "doi-song": [("ryle-holiness", "Ryle — Sự Nên Thánh"),
                 ("sibbes-bruisedreed", "Sibbes — Cây Sậy Dập")],
    "lich-su": [("mg1-122-institutes-1541-calvin", "Calvin — Giáo Huấn Cơ Đốc Giáo (1541)"),
                ("westminster-shorter", "Giáo Lý Vấn Đáp Ngắn Westminster")],
}

LOCI_CSS = """
      .locus { max-width: 860px; margin: 26px auto 0; padding: 20px; border: 1px solid var(--line); border-radius: 12px; background: rgba(255,255,255,.35); }
      .locus h2 { font-family: "Playfair Display", serif; font-size: 21px; margin: 0 0 6px; }
      .locus .desc { color: var(--ink-soft); margin: 0 0 12px; }
      .locus h3 { font-size: 15px; margin: 14px 0 4px; color: var(--gold-text); }
      .locus ul { margin: 0; padding-left: 20px; columns: 2; column-gap: 28px; }
      .locus li { margin: 4px 0; break-inside: avoid; }
      .locus li a { color: var(--gold-text); }
      @media (max-width: 640px) { .locus ul { columns: 1; } }
"""

def main():
    enc = json.loads((ROOT / "data/encyclopedia.json").read_text(encoding="utf-8"))["entries"]
    by_locus = {lid: [] for lid in LOCI}
    for e in enc:
        assert e.get("loci") and len(e["loci"]) == 1, f"entry {e['slug']} lacks exactly one locus"
        by_locus[e["loci"][0]].append(e)
    total = sum(len(v) for v in by_locus.values())
    assert total == len(enc) == 201, f"loci coverage {total} != 201"
    for lid, books in LOCI_BOOKS.items():
        for slug, _label in books:
            assert (ROOT / "ban-dich" / f"{slug}.html").exists(), f"locus book missing: {slug}"
    print(f"loci coverage: {total} entries across {len(LOCI)} loci")

    nav = "".join(
        f'<a class="btn" href="#locus-{lid}">{LOCI[lid]["name_vi"]} ({len(by_locus[lid])})</a>'
        for lid in LOCI)
    secs = ""
    for lid in LOCI:
        entries = sorted(by_locus[lid], key=lambda e: e["term_vi"])
        lis = "".join(
            f'<li><a href="/bach-khoa/{e["slug"]}.html">{e["term_vi"]}</a></li>' for e in entries)
        books = "".join(
            f'<li><a href="/ban-dich/{slug}.html">{label}</a></li>' for slug, label in LOCI_BOOKS.get(lid, []))
        secs += (f'<section class="locus" id="locus-{lid}"><h2>{LOCI[lid]["name_vi"]}</h2>'
                 f'<p class="desc">{LOCI[lid]["desc_vi"]}</p>'
                 f'<h3>Thuật ngữ ({len(entries)})</h3><ul>{lis}</ul>'
                 f'<h3>Sách liên quan</h3><ul>{books}</ul></section>')
    url = f"{BASE}/bach-khoa/theo-chu-de.html"
    page = f"""{head("Học theo lĩnh vực thần học — Bách Khoa | Reformed Vietnam",
                     "201 thuật ngữ Bách Khoa được xếp vào 10 lĩnh vực thần học: Kinh Thánh, Đức Chúa Trời, Chúa Giê-xu Christ, Đức Thánh Linh, con người, sự cứu rỗi, Hội Thánh, tận thế, đời sống Cơ Đốc và lịch sử Hội Thánh.", url, LOCI_CSS)}
<body id="top">
{header}
<main class="wrap">
  <p class="crumb"><a href="/">Trang chủ</a> · <a href="/bach-khoa/">Bách Khoa</a></p>
  <div class="cat-head">
    <div class="kicker">Bách Khoa · Theo lĩnh vực</div>
    <h1>Học theo lĩnh vực thần học</h1>
    <p style="max-width:640px;margin:0 auto;color:var(--ink-soft)">201 thuật ngữ được xếp vào 10 lĩnh vực thần học cổ điển (loci). Mỗi lĩnh vực liệt kê các thuật ngữ và vài cuốn sách liên quan trong thư viện — chọn một lĩnh vực để bắt đầu học có hệ thống.</p>
  </div>
  <div style="display:flex;gap:8px;flex-wrap:wrap;justify-content:center;max-width:860px;margin:18px auto 6px">{nav}</div>
{secs}
  <p style="text-align:center;margin-top:26px"><a class="btn" href="/bach-khoa/">← Bách Khoa</a> <a class="btn" href="/trung-tam-giao-ly/nam-sola.html">Trung tâm giáo lý: Năm Sola</a></p>
  {share_row(url)}
  {report_mailto("Học theo lĩnh vực thần học")}
</main>
{footer}
{MINI_JS}
</body>
</html>"""
    check_links(page, "/bach-khoa/theo-chu-de.html")
    changed = write_if_changed(ROOT / "bach-khoa/theo-chu-de.html", page)
    print(f"  /bach-khoa/theo-chu-de.html — {'written' if changed else 'unchanged'}")
    added = sitemap_add(["/bach-khoa/theo-chu-de.html"])
    print(f"sitemap: {added} URLs added")
    print("DONE")

if __name__ == "__main__":
    main()

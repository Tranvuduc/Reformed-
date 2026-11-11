#!/usr/bin/env python3
"""Phase 2, item 2.6 — Church history timeline (Lịch sử Hội Thánh).

Builds /lich-su-hoi-thanh.html from scripts/helper-data/timeline.json.
Only well-established dates are included; uncertain ones were left out
entirely (see the note in the data file) rather than guessed.
"""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from hub_page import (BASE, ROOT, head, header, footer, MINI_JS, share_row,
                      report_mailto, write_if_changed, check_links, sitemap_add)

TL_CSS = """
      .era { max-width: 860px; margin: 28px auto 0; }
      .era h2 { font-family: "Playfair Display", serif; font-size: 23px; margin: 0 0 4px; border-bottom: 2px solid var(--gold-soft); padding-bottom: 6px; }
      .tl-item { display: flex; gap: 16px; padding: 14px 0; border-bottom: 1px solid var(--line); }
      .tl-year { flex: 0 0 92px; font-family: "Playfair Display", serif; font-weight: 700; font-size: 17px; color: var(--gold-text); }
      .tl-item h3 { font-size: 16.5px; margin: 0 0 4px; }
      .tl-item p { margin: 0 0 6px; color: var(--ink-soft); }
      .tl-item ul { margin: 0; padding-left: 18px; }
      .tl-item li { margin: 3px 0; }
      .tl-item li a { color: var(--gold-text); }
      @media (max-width: 640px) { .tl-year { flex-basis: 72px; font-size: 15px; } }
"""

def main():
    data = json.loads((ROOT / "scripts/helper-data/timeline.json").read_text(encoding="utf-8"))
    n = 0
    eras = ""
    for era in data["eras"]:
        items = ""
        for e in era["entries"]:
            n += 1
            links = ""
            if e.get("links"):
                lis = "".join(f'<li><a href="{l["url"]}">{l["label"]}</a></li>' for l in e["links"])
                links = f"<ul>{lis}</ul>"
            items += (f'<div class="tl-item"><div class="tl-year">{e["year"]}</div>'
                      f'<div><h3>{e["title"]}</h3><p>{e["note"]}</p>{links}</div></div>')
        eras += f'<section class="era"><h2>{era["title"]}</h2>{items}</section>'
    url = f"{BASE}/lich-su-hoi-thanh.html"
    page = f"""{head("Lịch sử Hội Thánh — Từ Lễ Ngũ Tuần đến Việt Nam | Reformed Vietnam",
                     "Dòng thời gian lịch sử Hội Thánh: từ Lễ Ngũ Tuần, các công đồng, cuộc Cải Chánh, đến khi Tin Lành đến Việt Nam năm 1911.", url, TL_CSS)}
<body id="top">
{header}
<main class="wrap">
  <p class="crumb"><a href="/">Trang chủ</a></p>
  <div class="cat-head">
    <div class="kicker">Lịch sử Hội Thánh</div>
    <h1>Hai ngàn năm của Hội Thánh</h1>
    <p style="max-width:640px;margin:0 auto;color:var(--ink-soft)">Từ ngày Lễ Ngũ Tuần đến khi Tin Lành đến Việt Nam — những mốc lớn đã định hình đức tin chúng ta hôm nay. Mỗi mốc đều dẫn tới tài liệu liên quan trong thư viện. Ngày ghi 'khoảng' là ngày được giới sử học ước tính, không phải ngày chính xác tuyệt đối.</p>
  </div>
{eras}
  <div class="band-tint"><h2 class="bt-head">Về độ chính xác</h2>
  <p style="color:var(--ink-soft);margin:0">Dòng thời gian này chỉ ghi những mốc đã được xác lập rõ ràng trong lịch sử Hội Thánh. Các mốc chưa chắc chắn — ví dụ năm thành lập chính thức của Hội Thánh Tin Lành Việt Nam, hay ngày trở lại chính xác của Phao-lô — được bỏ qua cho đến khi có nguồn xác thực, thay vì đoán mò. Nếu bạn phát hiện sai sót, xin báo cho chúng tôi.</p></div>
  <p style="text-align:center;margin-top:26px"><a class="btn" href="/bach-khoa/cai-chanh.html">Bách Khoa: Cuộc Cải Chánh</a> <a class="btn" href="/trung-tam-giao-ly/nam-sola.html">Năm Sola</a></p>
  {share_row(url)}
  {report_mailto("Lịch sử Hội Thánh")}
</main>
{footer}
{MINI_JS}
</body>
</html>"""
    check_links(page, "/lich-su-hoi-thanh.html")
    changed = write_if_changed(ROOT / "lich-su-hoi-thanh.html", page)
    print(f"  /lich-su-hoi-thanh.html — {n} entries, {'written' if changed else 'unchanged'}")
    added = sitemap_add(["/lich-su-hoi-thanh.html"])
    print(f"sitemap: {added} URLs added")
    print("DONE")

if __name__ == "__main__":
    main()

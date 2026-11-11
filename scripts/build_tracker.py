#!/usr/bin/env python3
"""Phase 5.3 — Public translation-project tracker (Theo dõi dự án dịch thuật).

Builds /theo-doi-dich-thuat.html from real numbers only:

  * library size — counted live from translations/index.json
  * remaining queue — data/translation-programme.json (V24 verified
    baseline minus rounds completed since; every number carries its
    source on the page)
  * last completed round + current round (null = none running; the page
    says so plainly instead of inventing a date)
  * quality snapshot — data/quality-report.json (written by
    scripts/check_translations.py); if the file is absent the section
    is omitted rather than faked

No reviewer names, no dates and no completion estimates are invented.
Re-run after each translation round (update the JSON first).
"""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from hub_page import (BASE, ROOT, head, header, footer, MINI_JS, share_row,
                      report_mailto, write_if_changed, check_links, sitemap_add)

PROG = json.loads((ROOT / "data/translation-programme.json").read_text(encoding="utf-8"))
IDX = json.loads((ROOT / "translations/index.json").read_text(encoding="utf-8"))
LIBRARY_TOTAL = len(IDX)
try:
    QC = json.loads((ROOT / "data/quality-report.json").read_text(encoding="utf-8"))
except FileNotFoundError:
    QC = None

CSS = """
      .stat-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:14px;margin:22px 0}
      .stat{border:1px solid var(--line);border-radius:12px;padding:16px;text-align:center;background:rgba(255,255,255,.35)}
      .stat b{display:block;font-family:"Playfair Display",serif;font-size:34px;color:var(--burgundy)}
      .stat span{font-size:13.5px;color:var(--ink-soft)}
      .qbar{height:10px;border-radius:5px;background:var(--line);overflow:hidden;margin:8px 0 4px}
      .qbar i{display:block;height:100%;background:#2e7d32}
      .note{font-size:13.5px;color:var(--ink-soft)}
      .round-card{border:1px solid var(--line);border-radius:12px;padding:18px 20px;margin:16px 0;background:rgba(255,255,255,.35)}
      .round-card h3{margin:0 0 6px;font-family:"Playfair Display",serif}
      .phase5-nav{text-align:center;margin:26px 0 6px;font-size:14px;color:var(--ink-soft)}
      .phase5-nav a{color:var(--gold-text);font-weight:700}
"""


def fmt(n):
    return f"{n:,}".replace(",", ".")


def main():
    q = PROG["queue"]
    lr = PROG["last_round"]
    url = f"{BASE}/theo-doi-dich-thuat.html"

    if PROG["current_round"]:
        cr = PROG["current_round"]
        current_html = (f'<div class="round-card"><h3>Vòng {cr["round"]} — đang dịch</h3>'
                        f'<p><b>{cr["title_vi"]}</b> — {cr["author"]} '
                        f'(<i>{cr["orig"]}</i>)</p></div>')
    else:
        current_html = ('<div class="round-card"><h3>Chưa có vòng dịch đang chạy</h3>'
                        f'<p>{PROG["current_round_note"]}</p></div>')

    if lr["page_status"] == "live":
        page_line = (f'Trang đọc: <a href="{lr["page_url"]}">đọc bản dịch</a>.')
    else:
        page_line = lr["page_note"]
    last_html = (f'<div class="round-card"><h3>Vòng {lr["round"]} — mới hoàn tất ({lr["date"]})</h3>'
                 f'<p><b>{lr["title_vi"]}</b> — {lr["author"]} '
                 f'(<i>{lr["orig"]}</i>): {fmt(lr["chars"])} ký tự · '
                 f'{fmt(lr["words"])} từ · {lr["chapters"]} chương.</p>'
                 f'<p class="note">{page_line}</p></div>')

    done_pct = round(q["already_in_library"] / q["already_in_library_total"] * 100)
    queue_html = f"""
  <div class="stat-grid">
    <div class="stat"><b>{fmt(LIBRARY_TOTAL)}</b><span>bản dịch tiếng Việt trong thư viện</span></div>
    <div class="stat"><b>{fmt(q["remaining_total"])}</b><span>cuốn còn trong hàng đợi dịch</span></div>
    <div class="stat"><b>{fmt(q["ai2_pending"])}</b><span>cuốn còn lại trong danh sách AI-2 (dịch trước)</span></div>
    <div class="stat"><b>{PROG["audiobooks"]["books"]}</b><span>sách nói đã hoàn tất ({PROG["audiobooks"]["episodes"]} tập)</span></div>
  </div>
  <h2>Hàng đợi dịch còn lại: {fmt(q["remaining_total"])} cuốn</h2>
  <p>Trong {fmt(q["already_in_library_total"])} đầu sách đã đối chiếu, {fmt(q["already_in_library"])} cuốn đã có
  bản tiếng Việt trong thư viện ({done_pct}%). Số còn lại gồm {fmt(q["remaining_untranslated"])} cuốn chưa dịch và
  {fmt(q["remaining_other_volume"])} cuốn thuộc tập khác của tác phẩm đã dịch (ví dụ: tập 2 của một bộ đã có tập 1).
  Tối đa {fmt(q["remaining_max"])} cuốn nếu cả {q["baseline_unclear"]} dòng CHƯA RÕ đều hóa ra chưa dịch.</p>
  <div class="qbar"><i style="width:{done_pct}%"></i></div>
  <p class="note">{done_pct}% đầu sách đã đối chiếu đã có bản dịch · Nguồn: {q["baseline_source"]}
  Trừ 1 cuốn đã xong ở Vòng 32 (Burroughs, 11/11/2026) — còn {fmt(q["remaining_total"])} cuốn.</p>
  <p class="note">Chúng tôi không hứa ngày hoàn thành cho từng cuốn hay cho toàn bộ hàng đợi: mỗi vòng dịch một cuốn,
  và chất lượng bản dịch quan trọng hơn tốc độ. Mọi bản dịch đều ghi rõ “Bản dịch AI, chưa duyệt”.</p>"""

    if QC:
        qc_html = f"""
  <h2>Chất lượng bản dịch — kiểm tra ngày {QC["date"]}</h2>
  <p>Chương trình kiểm tra tự động quét toàn bộ {fmt(QC["files_total"])} tệp bản dịch và báo cáo các dấu hiệu cần rà soát.
  Đây là thống kê, không phải kết luận duyệt — mỗi mục đều cần người đọc lại trước khi sửa.</p>
  <ul>
    <li>{fmt(QC["footer_status_missing"])} tệp thiếu chân trang trạng thái dịch (TRANSLATION STATUS).</li>
    <li>{fmt(QC["needs_review_total"])} dấu [NEEDS REVIEW] trong {fmt(QC["needs_review_files"])} tệp — ghi chú chỗ chưa chắc, phần lớn là phục dựng lỗi OCR.</li>
    <li>{fmt(QC["english_flagged_files"])} tệp còn đoạn tiếng Anh dài chưa dịch (trên ngưỡng &gt;10 dòng).</li>
    <li>{fmt(QC["cong_binh_files"])} tệp chứa “công bình” và {fmt(QC["nuoc_dct_files"])} tệp chứa “nước Đức Chúa Trời” — hai cụm này đúng khi nằm trong trích dẫn Kinh Thánh 1934 nguyên văn, nên cần rà soát thủ công từng chỗ.</li>
    <li>“Kinh Lạy Cha”: {fmt(QC["kinh_lay_cha"])} lượt · “Kinh Tin Kính”: {fmt(QC["kinh_tin_kinh"])} lượt — đối chiếu mẫu cho thấy phần lớn là tên gọi quen thuộc của bài cầu nguyện / tín điều bên trong văn bản được dịch, không phải giọng văn riêng của trang; có sửa hay không là quyết định duyệt theo ngữ cảnh. Thuật ngữ khóa của trang là “Bài Cầu Nguyện Chung” và “Tín Điều Các Sứ Đồ”.</li>
  </ul>
  <p class="note">Báo cáo đầy đủ lưu trong kho mã nguồn (<code>scripts/quality-report-{QC["date"]}.md</code>); script kiểm tra ở <code>scripts/check_translations.py</code> — chạy lại sau mỗi đợt dịch.</p>"""
    else:
        qc_html = ""

    steps = "".join(f"<li>{s}</li>" for s in PROG["process"])
    body = f"""  <p class="crumb"><a href="/">Trang chủ</a> · <a href="/ve-chung-toi.html">Về chúng tôi</a></p>
  <div class="cat-head">
    <div class="kicker">Dự án dịch thuật</div>
    <h1>Theo dõi dự án dịch thuật</h1>
    <p style="max-width:640px;margin:0 auto;color:var(--ink-soft)">Thư viện đang dịch các tác phẩm Cải Chánh sang tiếng Việt — từng cuốn một, kiểm chứng với bản gốc, ghi rõ “Bản dịch AI, chưa duyệt”. Trang này cho thấy chương trình đang ở đâu, bằng số liệu thật.</p>
  </div>
{queue_html}
  <h2>Vòng dịch</h2>
{current_html}
{last_html}
  <h2>Cách một cuốn sách được dịch</h2>
  <ol>{steps}</ol>
  <p>Xem <a href="/trang-thai-ban-dich.html">trạng thái duyệt từng bản dịch</a> và
  <a href="/lo-trinh-phat-trien.html">lộ trình phát triển của trang</a>.</p>
{qc_html}
  <p class="note">Cập nhật lần cuối: {PROG["last_updated"]}. Số liệu trên trang này được cập nhật thủ công sau mỗi vòng dịch — nếu một vòng vừa xong mà trang chưa đổi, đó là vì chưa kịp cập nhật, không phải vì chương trình dừng lại.</p>
  <p class="phase5-nav"><a href="/bang-doc-sach.html">Bảng đọc của tôi</a> · <a href="/lo-trinh-phat-trien.html">Lộ trình phát triển</a></p>
  {share_row(url)}
  {report_mailto("Theo dõi dự án dịch thuật")}"""
    p = (head("Theo dõi dự án dịch thuật — còn bao nhiêu sách chưa dịch? | Reformed Vietnam",
              f"Chương trình dịch thuật Reformed Vietnam: {fmt(LIBRARY_TOTAL)} bản dịch trong thư viện, "
              f"{fmt(q['remaining_total'])} cuốn còn trong hàng đợi, vòng dịch mới nhất và cách một cuốn sách được dịch.",
              url, CSS)
         + "<body><main>" + header + body + "</main>" + footer + MINI_JS + "</body></html>")
    changed = write_if_changed(ROOT / "theo-doi-dich-thuat.html", p)
    check_links(p, "/theo-doi-dich-thuat.html")
    print(f"tracker: {'written' if changed else 'unchanged'}; "
          f"library={LIBRARY_TOTAL}, queue={q['remaining_total']}")
    print(f"sitemap: {sitemap_add(['/theo-doi-dich-thuat.html'])} URLs added")
    print("DONE")


if __name__ == "__main__":
    main()

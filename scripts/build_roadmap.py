#!/usr/bin/env python3
"""Phase 5.4 — Publish the roadmap (Lộ trình phát triển).

Builds /lo-trinh-phat-trien.html: the public edition of the site roadmap
(~/workspace/your_files/site-roadmap-2026-11-11.md), adapted for visitors:
phases with honest statuses, what is blocked on people/decisions, and the
ongoing programmes. Internal effort estimates and working notes are left
out; nothing is presented as done before it is live.

Statuses are hand-maintained in this file — update them when a phase lands.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from hub_page import (BASE, ROOT, head, header, footer, MINI_JS, share_row,
                      report_mailto, write_if_changed, check_links, sitemap_add)

UPDATED = "11/11/2026"

CSS = """
      .ph{border:1px solid var(--line);border-radius:12px;padding:18px 20px;margin:16px 0;background:rgba(255,255,255,.35)}
      .ph h3{margin:0 0 4px;font-family:"Playfair Display",serif}
      .pill{display:inline-block;font-size:12px;font-weight:700;padding:3px 10px;border-radius:999px;margin-left:8px;vertical-align:middle}
      .pill.done{background:#2e7d3222;color:#2e7d32;border:1px solid #2e7d3255}
      .pill.doing{background:#d9a41e22;color:#6b4423;border:1px solid #d9a41e55}
      .pill.wait{background:#7c212822;color:var(--burgundy);border:1px solid #7c212855}
      .note{font-size:13.5px;color:var(--ink-soft)}
      .phase5-nav{text-align:center;margin:26px 0 6px;font-size:14px;color:var(--ink-soft)}
      .phase5-nav a{color:var(--gold-text);font-weight:700}
"""

PHASES = [
    ("Giai đoạn 1 — Tin cậy &amp; tìm kiếm", "done", "Hoàn tất 11/11/2026",
     "Nút báo lỗi trên mọi trang sách; huy hiệu cho biết mỗi bản dịch đang ở trạng thái nào; "
     "bộ lọc tìm kiếm theo chủ đề, tác giả, độ khó; liên kết tác giả và nguồn gốc tiếng Anh cho từng cuốn."),
    ("Giai đoạn 2 — Học", "done", "Hoàn tất 11/11/2026",
     "Lộ trình học cho người mới tin Chúa, Năm Sola, sự nên thánh và chuẩn bị giảng dạy; "
     "thư viện các bản tuyên xưng đức tin; trung tâm giáo lý (Năm Sola, TULIP, Giao Ước); "
     "dòng thời gian lịch sử Hội Thánh; Hỏi Đáp nhóm theo chủ đề."),
    ("Giai đoạn 3 — Đọc", "done", "Hoàn tất 11/11/2026",
     "Trình đọc với cỡ chữ, giãn dòng, phông chữ và chế độ sáng/tối; lưu vị trí đọc dở và nút “Tiếp tục đọc”; "
     "thời gian đọc ước tính cho từng cuốn; mục “Sách mới thêm”; chế độ tập trung khi đọc."),
    ("Giai đoạn 4 — Chiều sâu học Kinh Thánh", "done", "Hoàn tất 11/11/2026",
     "50 nhân vật Kinh Thánh, 20 chủ đề, giới thiệu 66 sách Kinh Thánh với tóm tắt từng chương; "
     "dòng thời gian Kinh Thánh và bản đồ hành trình — tất cả dẫn về bản Kinh Thánh 1934."),
    ("Giai đoạn 5 — Tương tác &amp; chất lượng", "done", "Hoàn tất 11/11/2026",
     "Bảng đọc cá nhân; chương trình kiểm tra chất lượng bản dịch tự động; "
     "trang theo dõi dự án dịch thuật công khai; và chính trang lộ trình này."),
    ("Giai đoạn 6 — Đổi mới", "doing", "Hỏi xong · chờ bật bình luận",
     "Hỏi Thư Viện đã mở: tìm đoạn văn có trích dẫn, không tự soạn câu trả lời — hỏi toàn thư viện hoặc hỏi riêng một sách, từ link “Hỏi sách này” trên mọi trang sách. "
     "Bình luận bằng Giscus đã chuẩn bị sẵn trên mọi trang sách, đang chờ cài ứng dụng Giscus trên kho GitHub (một bước của quản trị viên); quản trị viên kiểm duyệt bình luận."),
]

BLOCKED = [
    ("Người duyệt bản dịch (mục sư, chủng sinh)", "Mọi bản dịch AI đều cần người có chuyên môn duyệt giáo lý. Đây là giới hạn lớn nhất của trang: không có người duyệt thì huy hiệu vẫn mãi ở “chưa duyệt”."),
    ("Người viết bản tin email", "Bản tin tuần chỉ mở khi có người viết đều đặn — hiện chưa có."),
    ("Nộp podcast lên Apple/Spotify", "Kênh “Sách Nói Cải Chánh” đã có nguồn cấp dữ liệu đầy đủ; việc nộp lên các cửa hàng podcast cần tài khoản của người quản lý trang."),
    ("Kết nối Facebook", "Trang Facebook cần được kết nối trước khi đăng bài hay kiểm tra nhóm — hiện chưa xong."),
]


def main():
    url = f"{BASE}/lo-trinh-phat-trien.html"
    ph_html = ""
    for title, cls, status, desc in PHASES:
        pill = {"done": "done", "doing": "doing", "wait": "wait"}[cls]
        ph_html += (f'<div class="ph"><h3>{title}<span class="pill {pill}">{status}</span></h3>'
                    f'<p>{desc}</p></div>')
    bl_html = "".join(f"<li><b>{t}:</b> {d}</li>" for t, d in BLOCKED)
    body = f"""  <p class="crumb"><a href="/">Trang chủ</a> · <a href="/ve-chung-toi.html">Về chúng tôi</a></p>
  <div class="cat-head">
    <div class="kicker">Reformed Vietnam đang đi tới đâu</div>
    <h1>Lộ trình phát triển</h1>
    <p style="max-width:640px;margin:0 auto;color:var(--ink-soft)">Trang này ghi lại những gì đã làm xong, đang làm và còn chờ — để bạn biết trang đang ở đâu và điều gì cần người giúp. Không hứa ngày hoàn thành cho những việc chưa có người làm.</p>
  </div>
{ph_html}
  <h2>Việc đang chạy song song</h2>
  <ul>
    <li><b>Dịch thuật:</b> còn 556 cuốn trong hàng đợi (xem <a href="/theo-doi-dich-thuat.html">theo dõi dự án dịch thuật</a>) — mỗi vòng dịch một cuốn, ngắn nhất trước.</li>
    <li><b>Sách nói:</b> 15 cuốn đã hoàn tất, 152 tập podcast “Sách Nói Cải Chánh”.</li>
    <li><b>Mạng xã hội:</b> Threads và Instagram đã đăng bài; TikTok, Pinterest, LinkedIn cần đăng nhập thêm.</li>
  </ul>
  <h2>Những việc cần người — chưa phải việc xây dựng</h2>
  <ul>{bl_html}</ul>
  <p class="note">Nếu bạn là mục sư hay người có chuyên môn thần học và muốn giúp duyệt bản dịch, xin xem
  <a href="/cho-muc-su.html">trang dành cho mục sư</a> hoặc viết thư về reformedvn@gmail.com.</p>
  <p class="note">Cập nhật lần cuối: {UPDATED}. Trang này do người quản lý cập nhật thủ công sau mỗi giai đoạn — trạng thái ghi ở đây là trạng thái thật tại thời điểm cập nhật.</p>
  <p class="phase5-nav"><a href="/bang-doc-sach.html">Bảng đọc của tôi</a> · <a href="/theo-doi-dich-thuat.html">Theo dõi dự án dịch thuật</a></p>
  {share_row(url)}
  {report_mailto("Lộ trình phát triển")}"""
    p = (head("Lộ trình phát triển | Reformed Vietnam",
              "Lộ trình phát triển của Reformed Vietnam: những giai đoạn đã hoàn tất, đang làm và còn chờ — "
              "ghi rõ việc nào cần người giúp trước khi mở.",
              url, CSS)
         + "<body><main>" + header + body + "</main>" + footer + MINI_JS + "</body></html>")
    changed = write_if_changed(ROOT / "lo-trinh-phat-trien.html", p)
    check_links(p, "/lo-trinh-phat-trien.html")
    print(f"roadmap: {'written' if changed else 'unchanged'}")
    print(f"sitemap: {sitemap_add(['/lo-trinh-phat-trien.html'])} URLs added")
    print("DONE")


if __name__ == "__main__":
    main()

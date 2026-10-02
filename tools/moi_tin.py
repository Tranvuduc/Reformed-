# Executed from build-pages.py (after vi_books.py). Builds moi-tin-chua.html: a 30-day path for new believers.
import re as _r2
def _anch(slug, pat):
    try: h = open(f"ban-dich/{slug}.html", encoding="utf-8").read()
    except OSError: return None
    m = _r2.search(r'<h2 id="(c\d+)">([^<]*%s[^<]*)</h2>' % pat, h)
    return f"/ban-dich/{slug}.html#{m.group(1)}" if m else (f"/ban-dich/{slug}.html" if True else None)
def _bk(slug, label, pat=None):
    u = _anch(slug, pat) if pat else f"/ban-dich/{slug}.html"
    return (u, label) if u and _o.path.exists(f"ban-dich/{slug}.html") else None
_B = "bonar-followlamb"; _S = "spurgeon-puritan-catechism"; _C = "calvin-chr-life"
_D = [
 ("Tin Lành là gì?", "1 Cô-rinh-tô 15:1-4", _bk(_B, "Bonar, Theo Chiên Con, mở đầu", "THEO")),
 ("Chúa Giê-xu là ai?", "Giăng 1:1-18", _bk(_S, "Giáo lý Thanh giáo, câu 19-21")),
 ("Tội lỗi là gì?", "Rô-ma 3:9-26", _bk(_S, "Giáo lý Thanh giáo, câu 14-18")),
 ("Ân điển là gì?", "Ê-phê-sô 2:1-10", _bk(_B, "Bonar, chương I: hãy mạnh mẽ trong ân điển", "I\\. HÃY MẠNH")),
 ("Ăn năn và đức tin", "Mác 1:14-15; Công Vụ 20:21", _bk(_S, "Giáo lý Thanh giáo, câu 67-69")),
 ("Được xưng công bình", "Rô-ma 5:1-11", _bk(_S, "Giáo lý Thanh giáo, câu 31")),
 ("Làm con của Đức Chúa Trời", "Rô-ma 8:14-17; 1 Giăng 3:1-3", _bk(_S, "Giáo lý Thanh giáo, câu 32")),
 ("Đức Thánh Linh", "Giăng 14:15-27", _bk(_S, "Giáo lý Thanh giáo, câu 28-29")),
 ("Kinh Thánh là gì?", "2 Ti-mô-thê 3:14-17", _bk(_S, "Giáo lý Thanh giáo, câu 2-3")),
 ("Cách đọc Kinh Thánh mỗi ngày", "Thi Thiên 119:9-16; Công Vụ 17:10-12", _bk(_B, "Bonar, chương VI: nghiên cứu Kinh Thánh", "VI\\. HÃY NGHIÊN")),
 ("Cầu nguyện là gì?", "Ma-thi-ơ 6:5-8", ("/doc/do-you-pray.html", "Ryle, Bạn có cầu nguyện không?")),
 ("Lời Chúa dạy cầu nguyện", "Ma-thi-ơ 6:9-13", _bk("calvin-prayer", "Calvin, Về sự cầu nguyện")),
 ("Biết mình đã được cứu", "1 Giăng 5:11-13", _bk(_B, "Bonar, chương IV: hãy thành thật với chính mình", "IV\\. HÃY THÀNH")),
 ("Chiến đấu với tội lỗi", "Rô-ma 6:1-14", _bk(_B, "Bonar, chương IX: canh chừng Sa-tan", "IX\\. HÃY CANH")),
 ("Nên thánh mỗi ngày", "Phi-líp 2:12-13", _bk(_S, "Giáo lý Thanh giáo, câu 33")),
 ("Hội Thánh là gì?", "1 Phi-e-rơ 2:4-10", _bk(_B, "Bonar, chương V: kết thân với dân sự Chúa", "V\\. HÃY KẾT")),
 ("Báp-têm", "Ma-thi-ơ 28:18-20; Rô-ma 6:3-4", _bk(_S, "Giáo lý Thanh giáo, câu 75-80 (lập trường Báp-tít)")),
 ("Tiệc Thánh", "1 Cô-rinh-tô 11:23-28", _bk(_S, "Giáo lý Thanh giáo, câu 81-83")),
 ("Nhóm lại thờ phượng", "Hê-bơ-rơ 10:24-25", None),
 ("Hiếu thảo với cha mẹ", "Ê-phê-sô 6:1-4", _bk("sach-04-hieu-thao-theo-kinh-thanh", "David, Hiếu thảo theo Kinh Thánh")),
 ("Gia đình còn thờ cúng tổ tiên", "Xuất Ê-díp-tô Ký 20:3-6; Rô-ma 13:7", _bk("sach-05-nguoi-moi-tin-trong-gia-dinh-tho-cung", "David, Người mới tin trong nhà có bàn thờ")),
 ("Khi đau khổ và bệnh tật", "Rô-ma 8:28-39", _bk("sach-02-giop-giua-con-bao", "David, Gióp giữa cơn bão")),
 ("Sợ hãi, lo lắng và bình an", "Phi-líp 4:6-7; Giăng 14:27", _bk("sach-09-so-hai-va-binh-an-duc-tin-so-voi-bua-chu", "David, Sợ hãi và bình an")),
 ("Tiền bạc và Tin Lành thịnh vượng", "Ma-thi-ơ 6:19-24; 1 Ti-mô-thê 6:6-10", _bk("sach-01-chua-khong-hua-giau-co", "David, Chúa không hứa giàu có")),
 ("Làm chứng cho người thân", "Ma-thi-ơ 5:13-16; 1 Phi-e-rơ 3:15", ("/doc/compel-them-to-come-in.html", "Spurgeon, Hãy ép người ta phải vào")),
 ("Phục vụ trong Hội Thánh", "Rô-ma 12:3-8", None),
 ("Làm việc cho Chúa", "Cô-lô-se 3:23-24", _bk("sach-21-kinh-thanh-va-nghe-nghiep", "David, Kinh Thánh và nghề nghiệp")),
 ("Sống cho vinh hiển Đức Chúa Trời", "1 Cô-rinh-tô 10:31", _bk(_S, "Giáo lý Thanh giáo, câu 1")),
 ("Chúa gìn giữ đến cùng", "Giăng 10:27-30; Phi-líp 1:6", _bk(_C, "Calvin, Đời sống Cơ Đốc")),
 ("Bước tiếp theo", "Hê-bơ-rơ 13:7, 17", ("/lo-trinh.html", "Lộ trình đọc đầy đủ")),
]
_rows = "".join(
    f'<li><b>Ngày {i+1}: {E(t)}</b><br><span class="m">Kinh Thánh: {E(s)}</span>' + (f'<br><a href="{E(r[0])}">Đọc thêm: {E(r[1])}</a>' if r else "") + "</li>"
    for i, (t, s, r) in enumerate(_D))
_body = ('<style>.dp li{margin:0 0 1em;line-height:1.5}.dp{padding-left:1.2em}.dr{padding:.6em .9em;border-radius:8px;background:#d9a41e22}</style>'
 '<h1>Tôi mới tin Chúa: 30 ngày đầu tiên</h1>'
 '<p>Mỗi ngày chỉ khoảng 10 phút: đọc đoạn Kinh Thánh, rồi đọc phần gợi ý (nếu có), và cầu nguyện ngắn. Bạn không cần hiểu hết. Hãy đi chậm và hỏi mục sư hoặc người hướng dẫn của bạn khi có thắc mắc.</p>'
 '<p class="dr">Phần "Đọc thêm" gồm nhiều bản dịch và sách do AI hỗ trợ, <b>chưa được mục sư duyệt giáo lý</b>. Kinh Thánh là thẩm quyền tối hậu. Hãy đọc Kinh Thánh trong bản bạn quen dùng, và đối chiếu mọi điều bạn đọc với Kinh Thánh. Thư viện này hỗ trợ việc học, nhưng không thay thế Hội Thánh địa phương.</p>'
 f'<ol class="dp">{_rows}</ol>'
 '<p><a class="btn" href="/">Về thư viện</a> · <a class="btn" href="/lo-trinh.html">Lộ trình đọc đầy đủ</a></p>')
open("moi-tin-chua.html", "w", encoding="utf-8").write(page("Tôi mới tin Chúa: 30 ngày đầu tiên | Reformed Vietnam", "Lộ trình 30 ngày cho người mới tin Chúa: mỗi ngày một đoạn Kinh Thánh và một bài đọc ngắn. Miễn phí.", "moi-tin-chua.html", _body))
urls.append("moi-tin-chua.html")

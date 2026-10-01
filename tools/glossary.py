# Executed from build-pages.py. Builds thuat-ngu.html: intro to Reformed theology + plain-language glossary.
_G = [
 ("Ân điển", "Sự ban cho không xứng đáng. Đức Chúa Trời cứu chúng ta không vì việc làm của chúng ta, nhưng vì lòng thương xót của Ngài.", "Ê-phê-sô 2:8-9"),
 ("Xưng công bình", "Đức Chúa Trời tuyên bố người tin là công bình, vì công đức của Đấng Christ được kể cho họ.", "Rô-ma 3:23-24; 5:1"),
 ("Nên thánh", "Công việc Đức Thánh Linh làm cho người tin ngày càng giống Đấng Christ trong đời sống.", "Phi-líp 2:12-13; 1 Tê-sa-lô-ni-ca 5:23"),
 ("Giao ước", "Mối quan hệ Đức Chúa Trời lập với con người bằng lời hứa của Ngài. Kinh Thánh được đọc như câu chuyện của các giao ước, đỉnh cao là Đấng Christ.", "Sáng thế ký 17:7; Hê-bơ-rơ 8:6"),
 ("Sự chọn lựa (tiền định)", "Đức Chúa Trời chọn những người thuộc về Ngài từ trước khi sáng thế, vì lòng nhân từ của Ngài.", "Ê-phê-sô 1:4-5; Rô-ma 8:29-30"),
 ("Sự tái sinh", "Đức Thánh Linh ban sự sống mới cho người chết về thuộc linh, để họ có thể tin và vâng phục.", "Giăng 3:3-8; Ê-phê-sô 2:1-5"),
 ("Đức tin và ăn năn", "Tin cậy Đấng Christ và quay khỏi tội lỗi. Hai điều này đi cùng nhau.", "Mác 1:15; Công vụ 20:21"),
 ("Sự bền đỗ", "Những người Chúa thật sự cứu sẽ được Ngài gìn giữ đến cuối cùng.", "Giăng 10:28-29; Phi-líp 1:6"),
 ("Năm Solas", "Năm câu khẩu hiệu của Cải Chánh: Chỉ Kinh Thánh, chỉ bởi ân điển, chỉ bởi đức tin, chỉ trong Đấng Christ, chỉ vinh hiển Đức Chúa Trời.", "2 Ti-mô-thê 3:16-17; Ê-phê-sô 2:8-9"),
 ("Tín điều và giáo lý vấn đáp", "Bản tóm tắt đức tin của Hội Thánh qua nhiều thế kỷ, và các câu hỏi đáp để dạy dỗ. Chúng phục vụ Kinh Thánh, không thay thế Kinh Thánh.", "Giu-đe 3; 2 Ti-mô-thê 1:13"),
 ("Thanh giáo", "Các mục sư và tín hữu Anh thế kỷ 16-17 muốn đời sống và Hội Thánh thuận theo Kinh Thánh. Owen, Baxter, Bunyan, Watson thuộc nhóm này.", ""),
]
_li = "".join(f'<div class="g"><h3>{E(t)}</h3><p>{E(d)}</p>' + (f'<p class="m"><small>Kinh Thánh: {E(r)}</small></p>' if r else '') + '</div>' for t, d, r in _G)
_body = f'''<style>.g{{margin:14px 0;padding:12px 16px;border-left:3px solid #8a3b1f;background:#8881;border-radius:6px}}.g h3{{margin:0 0 .2em;font-size:1.05rem}}.g p{{margin:.2em 0}}.dr{{padding:.6em .9em;border-radius:8px;background:#d9a20022;font-size:.9rem}}</style>
<h1>Thần học Cải Chánh là gì?</h1>
<p class="dr"><b>Bản nháp, chờ mục sư duyệt.</b> Trang này do người quản trị soạn bằng ngôn ngữ đơn giản. Hãy đối chiếu Kinh Thánh và hỏi mục sư của bạn.</p>
<p>Thần học Cải Chánh là truyền thống đức tin của những người theo cuộc Cải Chánh thế kỷ 16 (Calvin, Knox và những người khác). Truyền thống này nhấn mạnh rằng Kinh Thánh là thẩm quyền tối hậu, và sự cứu rỗi hoàn toàn là việc của Đức Chúa Trời, từ đầu đến cuối.</p>
<p>Trong truyền thống này có những khác biệt về một số vấn đề như báp-têm hay thể chế Hội Thánh (Trưởng Lão, Báp-tít Cải Chánh). Thư viện này có sách của cả hai nhánh.</p>
<h2>Thuật ngữ thường gặp</h2>{_li}
<p><a class="btn" href="/lo-trinh.html">Theo lộ trình đọc</a> <a class="btn s" href="/chu-de/">Xem theo chủ đề</a></p>'''
open("thuat-ngu.html", "w", encoding="utf-8").write(page("Thần học Cải Chánh là gì? Thuật ngữ cho người mới | Reformed Vietnam", "Giới thiệu ngắn thần học Cải Chánh và giải thích các thuật ngữ như ân điển, xưng công bình, giao ước, sự chọn lựa.", "thuat-ngu.html", _body))
urls.append("thuat-ngu.html")

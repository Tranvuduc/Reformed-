# Executed from build-pages.py. Builds cai-chanh-la-gi.html (Reformed 101) and cho-muc-su.html (groups/leaders). Draft, pending pastor review.
_S = [
 ("Chỉ Kinh Thánh (Sola Scriptura)", "Kinh Thánh là thẩm quyền tối hậu cho đức tin và đời sống. Các tín điều và sách thần học giúp ta hiểu Kinh Thánh, nhưng không đứng trên Kinh Thánh.", "2 Ti-mô-thê 3:16-17; Công vụ 17:11"),
 ("Chỉ bởi ân điển (Sola Gratia)", "Sự cứu rỗi là món quà của Đức Chúa Trời. Chúng ta không tự cứu mình bằng việc lành.", "Ê-phê-sô 2:8-9; Tít 3:4-7"),
 ("Chỉ bởi đức tin (Sola Fide)", "Chúng ta được xưng công bình trước mặt Đức Chúa Trời bởi đức tin nơi Chúa Giê-xu, không bởi công đức riêng.", "Rô-ma 3:21-28; Ga-la-ti 2:16"),
 ("Chỉ một mình Đấng Christ (Solus Christus)", "Chỉ có Chúa Giê-xu là Đấng trung gian giữa Đức Chúa Trời và loài người.", "1 Ti-mô-thê 2:5; Công vụ 4:12"),
 ("Chỉ vinh hiển Đức Chúa Trời (Soli Deo Gloria)", "Mọi sự là vì sự vinh hiển của Ngài, kể cả đời sống thường ngày của ta.", "Rô-ma 11:36; 1 Cô-rinh-tô 10:31"),
]
_T = [
 ("Mọi người đều có tội", "Tội lỗi ảnh hưởng đến toàn thể con người: tâm trí, ý chí và tình cảm. Chúng ta cần Đức Chúa Trời làm công việc đầu tiên.", "Rô-ma 3:10-12, 23; Ê-phê-sô 2:1-3"),
 ("Đức Chúa Trời chọn lựa", "Đức Chúa Trời đã chọn một dân cho Ngài trước khi sáng thế, vì lòng yêu thương của Ngài, không vì điều gì nơi chúng ta.", "Ê-phê-sô 1:4-6; Rô-ma 9:11-16"),
 ("Đấng Christ chết thay cho dân Ngài", "Sự chết của Chúa Giê-xu thật sự cứu người, không chỉ làm cho sự cứu rỗi có thể xảy ra.", "Ga 10:11, 15; Ê-phê-sô 5:25"),
 ("Ân điển có sức cảm hóa", "Khi Đức Chúa Trời kêu gọi, Thánh Linh làm cho lòng người đáp lại bằng đức tin.", "Giăng 6:37, 44; Công vụ 16:14"),
 ("Đức Chúa Trời gìn giữ", "Những người thật sự thuộc về Chúa sẽ được Ngài giữ vững đến cùng, vì Ngài trung tín.", "Giăng 10:27-29; Phi-líp 1:6"),
]
_G = [
 ("Giao ước", "Đức Chúa Trời đến với con người bằng lời hứa. Từ Áp-ra-ham đến Đấng Christ, Kinh Thánh là câu chuyện về giao ước của Ngài.", "Sáng thế ký 17:7; Hê-bơ-rơ 8:6-13"),
 ("Hội Thánh", "Đời sống Cơ Đốc không đơn độc. Chúng ta thờ phượng, học Lời Chúa, dự Tiệc Thánh và nâng đỡ nhau trong Hội Thánh địa phương.", "Công vụ 2:42; Hê-bơ-rơ 10:24-25"),
 ("Tín điều và giáo lý", "Hội Thánh qua các thời đại đã tóm tắt giáo huấn Kinh Thánh trong các tín điều: Sứ đồ, Nicene, Heidelberg, Westminster, Báp-tít 1689.", "Giu-đe 3; 2 Ti-mô-thê 1:13"),
]
def _blk(L): return "".join(f'<div class="g"><h3>{E(t)}</h3><p>{E(d)}</p><p class="m"><small>Kinh Thánh: {E(r)}</small></p></div>' for t, d, r in L)
_css = '<style>.g{margin:14px 0;padding:12px 16px;border-left:3px solid #8a3b1f;background:#8881;border-radius:6px}.g h3{margin:0 0 .2em;font-size:1.05rem}.g p{margin:.2em 0}.dr{padding:.6em .9em;border-radius:8px;background:#d9a20022;font-size:.9rem}</style>'
_b1 = f'''{_css}<h1>Cải Chánh là gì?</h1>
<p class="dr">Bản nháp do AI hỗ trợ soạn, chưa được mục sư duyệt giáo lý. Kinh Thánh là thẩm quyền tối hậu. Hãy đối chiếu với Kinh Thánh và hỏi mục sư của bạn.</p>
<p>“Cải Chánh” (Reformed) là truyền thống Tin Lành bắt nguồn từ cuộc Cải cách thế kỷ XVI, với những người như Calvin, Zwingli, Knox. Truyền thống này nhấn mạnh Kinh Thánh, ân điển của Đức Chúa Trời và sự vinh hiển của Ngài. Bạn không cần hiểu hết mọi điều ấy mới theo Chúa được. Hãy bắt đầu với <a href="/moi-tin-chua.html">lộ trình 30 ngày</a>.</p>
<h2>Năm điều “Chỉ” (Năm Solas)</h2>{_blk(_S)}
<h2>Ân điển trong sự cứu rỗi (thường gọi là TULIP)</h2><p>Đây là năm điểm do Hội nghị Dort (1619) đưa ra để trả lời những tranh luận thời đó. Người Cải Chánh xem đó là cách tóm tắt việc Đức Chúa Trời cứu con người, chứ không phải cái nhãn để tranh cãi.</p>{_blk(_T)}
<h2>Những điều khác bạn sẽ gặp</h2>{_blk(_G)}
<h2>Các nhánh trong truyền thống</h2>
<p>Trưởng Lão (Presbyterian), Báp-tít Cải Chánh và các Hội Thánh khác có chung nhiều điều nhưng khác nhau về báp-têm (trẻ em hay người tin), thể chế Hội Thánh và một số điểm cánh chung. Mỗi sách trong thư viện có thể thuộc một nhánh khác nhau. Sách có mặt trong thư viện không có nghĩa là chúng tôi đồng ý với mọi điều tác giả viết.</p>
<p><a class="btn" href="/moi-tin-chua.html">Tôi mới tin Chúa</a> <a class="btn s" href="/thuat-ngu.html">Thuật ngữ</a> <a class="btn s" href="/lo-trinh.html">Lộ trình đọc</a></p>'''
open("cai-chanh-la-gi.html", "w", encoding="utf-8").write(page("Cải Chánh là gì? Năm Solas và giáo lý ân điển | Reformed Vietnam", "Giới thiệu truyền thống Cải Chánh bằng tiếng Việt đơn giản: Năm Solas, ân điển, giao ước, Hội Thánh và tín điều, kèm Kinh Thánh.", "cai-chanh-la-gi.html", _b1))
urls.append("cai-chanh-la-gi.html")
_Q = ["Đoạn Kinh Thánh hôm nay nói gì về Đức Chúa Trời?", "Đoạn này nói gì về con người và tội lỗi?", "Đoạn này chỉ về Chúa Giê-xu như thế nào?", "Tuần này tôi sẽ vâng theo điều gì?", "Tôi sẽ cầu nguyện cho ai và điều gì?"]
_b2 = f'''{_css}<h1>Cho mục sư và nhóm nhỏ</h1>
<p class="dr">Gợi ý cách dùng trang này trong Hội Thánh. Các bản dịch và sách mới do AI hỗ trợ soạn, chưa được mục sư duyệt, nên người hướng dẫn cần đọc trước.</p>
<h2>Cách dùng lộ trình 30 ngày cho nhóm</h2>
<p>Mỗi tuần nhóm gặp một lần và cùng xem lại bốn đến năm ngày đọc trong <a href="/moi-tin-chua.html">lộ trình “Tôi mới tin Chúa”</a>. Mỗi người đọc trước ở nhà, mỗi buổi khoảng 45 phút.</p>
<h2>Năm câu hỏi thảo luận cho mỗi buổi</h2><ol>{"".join(f"<li>{E(q)}</li>" for q in _Q)}</ol>
<h2>Gợi ý cho người hướng dẫn</h2>
<ul><li>Đọc trước và đối chiếu với Kinh Thánh. Dùng sách để hiểu Kinh Thánh, không thay cho Kinh Thánh.</li>
<li>Chọn tài liệu theo mức độ của nhóm. Người mới nên tránh các sách tranh luận.</li>
<li>Hãy để người mới thoải mái hỏi bất cứ điều gì, và đừng vội kéo họ vào những tranh luận sâu.</li>
<li>Nếu thấy lỗi trong bản dịch máy hoặc bản AI, xin báo để chúng tôi sửa: reformedvn@gmail.com.</li></ul>
<h2>Cho lãnh đạo Hội Thánh</h2>
<p>Các tín điều dùng trong thư viện: Giáo lý Heidelberg, Tín điều Bỉ, Các Điều luật Dort, Westminster và Tín điều Báp-tít 1689. Xem <a href="/tieng-viet.html">tài liệu tiếng Việt</a> và <a href="/doi-song-viet-nam.html">đời sống Việt Nam</a>.</p>'''
open("cho-muc-su.html", "w", encoding="utf-8").write(page("Cho mục sư và nhóm nhỏ: cách dùng lộ trình và câu hỏi thảo luận | Reformed Vietnam", "Gợi ý dùng thư viện cho nhóm nhỏ và lãnh đạo Hội Thánh: lộ trình 30 ngày, câu hỏi thảo luận, tài liệu tín điều.", "cho-muc-su.html", _b2))
urls.append("cho-muc-su.html")

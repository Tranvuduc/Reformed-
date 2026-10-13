# Executed at the end of nang_cap3.py. Content pages (AI-drafted, labelled unreviewed): so-sanh, dong-thoi-gian, hoi-dap, cong-cu-muc-vu, cong-cu-hoc.
def _bk3(stem):
    return f"/ban-dich/{stem}.html" if stem in _B3 else None
def _lks3(stems):
    return " · ".join(f'<a href="{_bk3(s)}">{E(_B3[s]["title"])}</a>' for s in stems if s in _B3)
_DRAFT3 = '<p class="m">Nội dung do AI hỗ trợ soạn dựa trên các bản tuyên xưng đức tin, chưa được mục sư duyệt. Hãy đối chiếu với Kinh Thánh và hỏi mục sư của bạn.</p>'

# ---- 4. So sanh cac truyen thong ----
_CMP = [
 ("Báp-têm", "Cho cả trẻ em; là phương tiện ân điển, Chúa dùng để củng cố và ban đức tin.", "Cho tín hữu và con cái họ; là dấu hiệu và con dấu của giao ước ân điển.", "Chỉ cho người đã tin; thường làm bằng cách dầm mình; là dấu hiệu của đức tin đã có.", "Bản Tuyên xưng Augsburg, đ. 9; Westminster, ch. 28; Tuyên xưng Báp-tít 1689, ch. 29"),
 ("Tiệc Thánh", "Thân và huyết Đấng Christ thật sự hiện diện “trong, cùng với và dưới” bánh và chén.", "Đấng Christ hiện diện thiêng liêng; tín hữu nhận Ngài bởi đức tin nhờ Đức Thánh Linh (Calvin).", "Chủ yếu là kỷ niệm và thông công; Đấng Christ hiện diện thiêng liêng với đức tin.", "Augsburg, đ. 10; Heidelberg, hỏi 75–82; Westminster, ch. 29; Báp-tít 1689, ch. 30"),
 ("Sự chọn lựa", "Chọn trong Đấng Christ để cứu rỗi; thận trọng không dạy rằng Chúa định trước sự hư mất.", "Chọn lựa vô điều kiện: Chúa chọn người thuộc về Ngài không vì điều Ngài thấy trước nơi họ.", "Cùng quan điểm Cải Chánh về sự chọn lựa vô điều kiện.", "Công thức Hòa hiệp, đ. 11; Các Quy tắc Dort; Westminster, ch. 3; Báp-tít 1689, ch. 3"),
 ("Sự bền đỗ của tín hữu", "Tín hữu có thể rơi khỏi đức tin; Chúa vẫn kêu gọi trở lại.", "Những người Chúa thật cứu sẽ được gìn giữ đến cùng.", "Cùng quan điểm Cải Chánh: sự bền đỗ của các thánh.", "Augsburg, đ. 12; Westminster, ch. 17; Báp-tít 1689, ch. 17"),
 ("Thể chế Hội Thánh", "Tùy từng nước: có nơi theo giám mục, có nơi theo hội đồng.", "Trưởng Lão: các trưởng lão cai quản, họp theo hội đồng nhiều tầng.", "Hội chúng tự trị: mỗi Hội Thánh địa phương tự điều hành, có trưởng lão và chấp sự.", "Westminster, ch. 25–31; Báp-tít 1689, ch. 26"),
 ("Luật pháp và ngày Chúa nhật", "Phân biệt rõ luật pháp và Phúc Âm; ngày Chúa nhật là ngày nhóm lại, không là luật Sa-bát.", "Ngày Chúa nhật là ngày Sa-bát Cơ Đốc, dành cho sự thờ phượng.", "Phần lớn giống Westminster: ngày thứ nhất trong tuần dành cho thờ phượng.", "Westminster, ch. 19, 21; Báp-tít 1689, ch. 19, 22"),
]
_rows = "".join(f'<tr><th scope="row">{E(t)}</th><td>{E(a)}</td><td>{E(b)}</td><td>{E(c)}</td></tr><tr><td colspan="4" class="stt">Tham khảo: {E(s)}</td></tr>' for t, a, b, c, s in _CMP)
_b4 = _NC3 + f'''<style>.cmp th,.cmp td{{vertical-align:top;font-size:.9rem}}.cmp thead th{{position:sticky;top:0;background:var(--bg,#fff)}}.cmpw{{overflow-x:auto}}</style><h1>So sánh các truyền thống</h1>
<p>Cải Chánh có nhiều nhánh. Bảng này so sánh cách ba dòng nhìn một số vấn đề thường gặp: <b>Luther</b> (Lutheran), <b>Calvin</b> (Cải Chánh và Trưởng Lão) và <b>Báp-tít Cải Chánh</b> (như Spurgeon và Bunyan). Cả ba cùng nhận Kinh Thánh là thẩm quyền tối hậu, Ba Ngôi, Đấng Christ là Đức Chúa Trời thật và người thật, và cứu rỗi chỉ bởi ân điển qua đức tin. Chỗ khác nhau là những vấn đề mà các Cơ Đốc nhân nghiêm túc vẫn bàn luận với nhau trong tình yêu thương.</p>
<div class="cmpw"><table class="tb cmp"><thead><tr><th></th><th>Luther</th><th>Calvin</th><th>Báp-tít Cải Chánh</th></tr></thead><tbody>{_rows}</tbody></table></div>
<section class="nc"><h2>Đọc thêm trong thư viện</h2><ul><li>Sự chọn lựa: {_lks3(["boettner-predestination", "owen-display", "edwards-will"])}</li><li>Tiệc Thánh: {_lks3(["owen-discourses", "heidelberg"])}</li><li>Giáo lý vấn đáp: {_lks3(["heidelberg", "westminster-shorter", "spurgeon-puritan-catechism"])}</li><li>Thờ phượng: {_lks3(["owen-worship"])}</li></ul></section>
<p class="m">Đây là bản tóm tắt ngắn. Mỗi hệ phái có những khác biệt nhỏ riêng, nên hãy đọc tuyên xưng đức tin của chính Hội Thánh bạn. Bản này không thay thế sự hướng dẫn của mục sư.</p>''' + _DRAFT3
open("so-sanh.html", "w", encoding="utf-8").write(page("So sánh Luther, Calvin và Báp-tít Cải Chánh | Reformed Vietnam", "Bảng so sánh ngắn cách ba dòng Cải Chánh nhìn báp-têm, Tiệc Thánh, sự chọn lựa, sự bền đỗ và thể chế Hội Thánh.", "so-sanh.html", _b4)); urls.append("so-sanh.html")

# ---- 5. Dong thoi gian ----
_TL = [
 (1517, "Luther đóng 95 luận đề tại Wittenberg", "Thường được xem là khởi đầu của cuộc Cải Chánh.", None),
 (1523, "Zwingli bắt đầu cải cách ở Zurich", "Cuộc Cải Chánh lan sang Thụy Sĩ.", None),
 (1536, "Calvin xuất bản bản đầu của Cơ Đốc Giáo Cương Yếu", "Calvin đến Geneva và về sau nhiều lần soạn lại tác phẩm này.", "calvin-chr-life"),
 (1553, "Mary I lên ngôi ở Anh", "Nhiều tín hữu Tin Lành bị bắt bớ; John Foxe ghi lại tên các người tử đạo.", None),
 (1559, "Bản cuối của Cơ Đốc Giáo Cương Yếu (tiếng Latin)", "Calvin hoàn tất bản mà Hội Thánh Cải Chánh dùng rộng rãi.", "calvin-prayer"),
 (1560, "Bản Tuyên xưng Đức tin Scotland", "John Knox cùng các bạn đồng công soạn bản tuyên xưng của Hội Thánh Scotland.", "knox-history"),
 (1563, "Giáo lý Vấn đáp Heidelberg", "Bản giáo lý dùng để dạy dân sự ở Palatinate, ngày nay vẫn dùng tại nhiều Hội Thánh.", "heidelberg"),
 (1618, "Hội nghị Dort (1618–1619)", "Hội nghị xử lý bất đồng với Arminius và để lại Các Quy tắc Dort.", None),
 (1643, "Hội đồng Westminster họp (1643–1653)", "Hội đồng soạn Tuyên xưng Đức tin, Giáo lý Lớn và Giáo lý Vắn tắt (1647).", "westminster-shorter"),
 (1678, "Bunyan xuất bản Thiên Lộ Lịch Trình", "Sách được dịch ra rất nhiều thứ tiếng, trong đó có tiếng Việt.", None),
 (1689, "Bản Tuyên xưng Đức tin Báp-tít (London)", "Các Hội Thánh Báp-tít Cải Chánh công bố bản tuyên xưng theo mô hình Westminster.", None),
 (1741, "Edwards giảng “Tội nhân trong tay Đức Chúa Trời thịnh nộ”", "Thời kỳ Đại Phấn Hưng ở Mỹ.", "edwards-sermons"),
 (1792, "William Carey và hội truyền giáo Báp-tít", "Andrew Fuller cổ vũ phong trào truyền giáo hiện đại.", None),
 (1834, "Spurgeon chào đời", "Về sau ông mục sư tại London và là “hoàng tử của các nhà giảng đạo”.", "spurgeon-grace"),
 (1911, "Tin Lành đến Việt Nam", "Hội truyền giáo đến Đà Nẵng; nhiều nguồn ghi nhận mốc này.", None),
 (1927, "Hội Thánh Tin Lành Việt Nam chính thức thành lập", "Nhiều nguồn ghi nhận mốc này.", None),
]
_tl = "".join(f'<li style="margin:.9em 0"><b>{y}</b> · <b>{E(t)}</b><br><span class="stt" style="opacity:.9">{E(d)}</span>' + (f' <a href="{_bk3(s)}">Đọc trong thư viện</a>' if s and _bk3(s) else "") + "</li>" for y, t, d, s in _TL)
_b5 = _NC3 + f'<h1>Dòng thời gian Cải Chánh</h1><p>Một số mốc lớn của cuộc Cải Chánh và truyền thống Cải Chánh, kèm sách liên quan trong thư viện. Không phải danh sách đầy đủ.</p><ol style="list-style:none;padding:0">{_tl}</ol><p class="m">Đây là bản tóm lược do AI soạn, chưa được mục sư hoặc nhà sử học duyệt. Một số năm ghi theo cách phổ biến; hãy kiểm tra trước khi trích dẫn.</p>'
open("dong-thoi-gian.html", "w", encoding="utf-8").write(page("Dòng thời gian Cải Chánh | Reformed Vietnam", "Các mốc lớn của Cải Chánh từ Luther và Calvin đến Heidelberg, Westminster, Spurgeon và Tin Lành Việt Nam, kèm sách liên quan.", "dong-thoi-gian.html", _b5)); urls.append("dong-thoi-gian.html")

# ---- 9. Hoi dap tan tin huu ----
_FQ = [
 ("Tin Chúa là gì?", "Là tin cậy Chúa Giê-xu: Ngài là Đức Chúa Trời làm người, chết thế cho tội ta và sống lại. Người tin được tha tội và có sự sống đời đời, không do việc làm nhưng do ân điển.", "Giăng 3:16; Rô-ma 10:9; Ê-phê-sô 2:8-9", ["sach-18-duc-tin-cai-chanh-trong-15-phut"]),
 ("Tôi có cần làm việc lành để được cứu không?", "Không. Việc lành là kết quả của sự cứu rỗi, không phải điều kiện để được cứu. Chúa dựng chúng ta để làm việc lành sau khi đã cứu.", "Ê-phê-sô 2:8-10; Tít 3:5", ["sach-07-an-dien-va-cong-duc", "spurgeon-grace"]),
 ("Tôi nên cầu nguyện thế nào?", "Cầu nguyện là nói chuyện với Cha trên trời. Có thể bắt đầu bằng Kinh Lạy Cha: tôn vinh Chúa, xin điều cần, xưng tội và xin tha.", "Ma-thi-ơ 6:5-13; Phi-líp 4:6", ["watson-lordsprayer", "do-you-pray"]),
 ("Nên bắt đầu đọc Kinh Thánh từ đâu?", "Hãy đọc Phúc Âm Giăng hoặc Mác trước, rồi Công Vụ và Rô-ma. Đọc mỗi ngày một ít, và cầu xin Chúa soi sáng.", "Giăng 20:31; Thi Thiên 119:105", []),
 ("Tại sao tôi cần Hội Thánh?", "Hội Thánh là gia đình của Chúa. Ở đó ta được dạy dỗ, được nâng đỡ, dự Tiệc Thánh và phục vụ nhau. Đức tin không được dành cho một mình.", "Công Vụ 2:42; Hê-bơ-rơ 10:24-25", ["sach-11-dan-dat-va-ky-luat-hoi-thanh"]),
 ("Báp-têm là gì?", "Là dấu hiệu bên ngoài cho thấy tôi thuộc về Đấng Christ, theo lệnh của Chúa. Các Hội Thánh Cải Chánh hiểu khác nhau về việc báp-têm cho trẻ em; hãy hỏi mục sư của bạn.", "Ma-thi-ơ 28:19; Rô-ma 6:3-4", []),
 ("Tại sao Tin Lành có nhiều hệ phái?", "Các Hội Thánh thống nhất về điều căn bản của Phúc Âm nhưng khác nhau ở một số vấn đề như báp-têm hay thể chế. Sự đa dạng không có nghĩa là Phúc Âm khác nhau.", "Ê-phê-sô 4:4-6", []),
 ("Gia đình tôi thờ cúng tổ tiên, tôi nên làm gì?", "Chúa dạy hiếu kính cha mẹ, và đồng thời chỉ thờ một mình Ngài. Hãy tôn trọng người thân bằng yêu thương, nhưng đừng cúng bái hay thờ lạy. Hãy hỏi mục sư để được hướng dẫn cụ thể.", "Xuất Ê-díp-tô Ký 20:3-5, 12; Ê-phê-sô 6:1-3", ["sach-05-nguoi-moi-tin-trong-gia-dinh-tho-cung", "sach-06-tang-le-gio-tet-song-lam-chung", "sach-04-hieu-thao-theo-kinh-thanh"]),
 ("Tôi vẫn phạm tội sau khi tin, vậy có mất ơn cứu rỗi không?", "Người thật sự thuộc về Chúa vẫn còn tội, nhưng được kêu gọi xưng tội và ăn năn. Truyền thống Cải Chánh dạy rằng Chúa gìn giữ người Ngài đã cứu.", "1 Giăng 1:9; Rô-ma 8:1; Phi-líp 1:6", ["owen-indwellingsin"]),
 ("Tại sao Chúa cho phép đau khổ?", "Kinh Thánh không cho biết mọi lý do, nhưng hứa rằng Chúa ở cùng và dùng mọi sự cho điều ích của người yêu mến Ngài. Gióp học tin Chúa khi chưa hiểu.", "Rô-ma 8:28; Gióp 42:1-6", ["sach-02-giop-giua-con-bao", "boston-crook"]),
 ("Chúa có hứa cho tôi giàu có không?", "Kinh Thánh hứa Chúa lo cho nhu cầu của chúng ta, không hứa sự giàu có. Sự thỏa lòng trong Chúa quý hơn của cải.", "Phi-líp 4:11-13; 1 Ti-mô-thê 6:6-10", ["sach-01-chua-khong-hua-giau-co", "watson-contentment"]),
 ("Làm sao tôi biết mình đã được cứu?", "Nhìn vào Đấng Christ chứ không nhìn vào cảm xúc. Dấu hiệu của đức tin thật là lòng ăn năn, yêu mến Lời Chúa và muốn vâng lời Ngài, dù còn yếu đuối.", "1 Giăng 5:13; Rô-ma 8:16", ["bonar-peace"]),
]
_fq = "".join(f'<section class="nc"><h2>{E(q)}</h2><p>{E(a)}</p><p class="stt">Kinh Thánh: {E(r)}' + (f'<br>Đọc thêm: {_lks3(ls)}' if _lks3(ls) else "") + '</p></section>' for q, a, r, ls in _FQ)
_ld5 = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a, r, ls in _FQ]}
_b9 = _NC3 + '<h1>Hỏi đáp cho người mới tin</h1><p>Những câu hỏi thường gặp khi mới tin Chúa. Câu trả lời ngắn, có câu Kinh Thánh và sách để đọc thêm.</p>' + _fq + _DRAFT3 + '<p><a class="btn" href="/moi-tin-chua.html">Lộ trình 30 ngày</a></p>'
open("hoi-dap.html", "w", encoding="utf-8").write(page("Hỏi đáp cho người mới tin Chúa | Reformed Vietnam", "Mười hai câu hỏi thường gặp của người mới tin Chúa, trả lời ngắn gọn theo Kinh Thánh, kèm sách để đọc thêm.", "hoi-dap.html", _b9, _ld5)); urls.append("hoi-dap.html")

# ---- 10. Cong cu muc vu ----
_b10 = _NC3 + f'''<h1>Công cụ cho mục sư và người dẫn nhóm</h1>
<p>Trang này gom những gì thư viện có để chuẩn bị bài giảng, dạy giáo lý và dẫn nhóm nhỏ. Xem thêm <a href="/cho-muc-su.html">hướng dẫn dành cho mục sư</a> và cách <a href="/duyet.html">giúp duyệt bản dịch</a>.</p>
<section class="nc"><h2>Chuẩn bị bài giảng từ một đoạn Kinh Thánh</h2><ol>
<li><b>Quan sát.</b> Đọc cả đoạn vài lần. Ai nói với ai? Điều gì lặp lại? Động từ chính là gì?</li>
<li><b>Bối cảnh.</b> Đoạn nằm ở đâu trong sách và trong câu chuyện cứu chuộc?</li>
<li><b>Xem người xưa giảng giải.</b> Dùng <a href="/tra-kinh-thanh.html">Tra cứu theo Kinh Thánh</a> để thấy các tác giả Cải Chánh đã trích hoặc giảng đoạn này.</li>
<li><b>Đấng Christ.</b> Đoạn chỉ về Ngài như thế nào?</li>
<li><b>Giáo lý.</b> Đối chiếu với <a href="/giao-ly-hang-ngay.html">giáo lý Heidelberg và Westminster</a> và <a href="/so-sanh.html">sự khác nhau giữa các dòng</a>.</li>
<li><b>Ứng dụng.</b> Điều gì cho người trong Hội Thánh bạn, ở nơi và hoàn cảnh của họ?</li></ol>
<p>Xem sách của chúng tôi: {_lks3(["sach-10-soan-bai-giang-giai-kinh"])}</p></section>
<section class="nc"><h2>Dạy và dẫn nhóm</h2><ul><li><a href="/nhom-nho.html">Kế hoạch nhóm nhỏ cho từng sách</a> (có thể in)</li><li><a href="/doc-chung.html">Kế hoạch đọc chung 4 tuần</a></li><li><a href="/ke-hoach-doc.html">Kế hoạch đọc cá nhân</a></li><li><a href="/thuat-ngu.html">Từ điển thuật ngữ</a></li><li>Sách của chúng tôi: {_lks3(["sach-12-giao-ly-van-dap-cho-lop-nhom-nho", "sach-14-day-giao-ly-o-nha", "sach-11-dan-dat-va-ky-luat-hoi-thanh", "sach-13-cham-soc-tin-huu-trong-khung-hoang"])}</li></ul></section>
<section class="nc"><h2>Giúp chúng tôi</h2><p>Nếu bạn là mục sư hoặc người có chuyên môn thần học, các bản dịch và tiểu sử còn đang chờ duyệt. Xem <a href="/trang-thai-ban-dich.html">trạng thái duyệt</a>.</p></section>''' + _DRAFT3
open("cong-cu-muc-vu.html", "w", encoding="utf-8").write(page("Công cụ cho mục sư và người dẫn nhóm | Reformed Vietnam", "Chuẩn bị bài giảng từ một đoạn Kinh Thánh, dạy giáo lý và dẫn nhóm nhỏ với các công cụ của thư viện Reformed Vietnam.", "cong-cu-muc-vu.html", _b10)); urls.append("cong-cu-muc-vu.html")

# ---- Hub: cong cu hoc ----
_HUB = [("Tra cứu theo Kinh Thánh", "/tra-kinh-thanh.html", "Chọn chương Kinh Thánh để thấy sách nào giảng giải."),
        ("Giáo lý mỗi ngày", "/giao-ly-hang-ngay.html", "Một câu hỏi Heidelberg và một câu Westminster mỗi ngày."),
        ("Kế hoạch đọc cá nhân", "/ke-hoach-doc.html", "Chia một sách thành các phần theo ngày."),
        ("Sách cho nhóm nhỏ", "/nhom-nho.html", "Buổi học, Kinh Thánh cùng đọc và câu hỏi thảo luận."),
        ("Hỏi đáp cho người mới tin", "/hoi-dap.html", "Mười hai câu hỏi thường gặp."),
        ("So sánh các truyền thống", "/so-sanh.html", "Luther, Calvin và Báp-tít Cải Chánh."),
        ("Dòng thời gian Cải Chánh", "/dong-thoi-gian.html", "Những mốc lớn từ 1517 đến Việt Nam."),
        ("Thuật ngữ", "/thuat-ngu.html", "Từ ngữ thần học bằng lời đơn giản."),
        ("Công cụ cho mục sư", "/cong-cu-muc-vu.html", "Chuẩn bị bài giảng và dạy giáo lý.")]
_b11 = _NC3 + '<h1>Công cụ học</h1><p>Những cách khác nhau để đọc và học thư viện này. Tất cả miễn phí, không cần tài khoản.</p>' + "".join(f'<section class="nc"><h2><a href="{u}">{E(t)}</a></h2><p>{E(d)}</p></section>' for t, u, d in _HUB)
open("cong-cu-hoc.html", "w", encoding="utf-8").write(page("Công cụ học | Reformed Vietnam", "Tra cứu theo Kinh Thánh, giáo lý mỗi ngày, kế hoạch đọc, sách cho nhóm nhỏ, hỏi đáp và dòng thời gian Cải Chánh.", "cong-cu-hoc.html", _b11)); urls.append("cong-cu-hoc.html")

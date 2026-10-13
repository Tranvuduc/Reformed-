# Executed after nang_cap5.py. Pages: doc-kinh-thanh, hoc-thuoc-long, gia-dinh-tho-phuong, hoi-thanh-nha, lich-su-hom-nay, so-hoc (+ giao-ly.json).
_open6 = lambda p, t: open(p, "w", encoding="utf-8").write(t)
_open6("giao-ly.json", _j3.dumps({"h": _hd3, "w": _wsc3}, ensure_ascii=False, separators=(",", ":")))
_nm_opts = "".join(f'<option value="{i+1}">{E(n)}</option>' for i, n in enumerate(_VN66))

# --- Doc Kinh Thanh kem giang giai ---
_b = _NC3 + f'''<style>.vs{{margin:.5em 0;line-height:1.65}}.vn{{font-size:.75rem;vertical-align:super;text-decoration:none;margin-right:2px;font-weight:700}}.vn.ci{{color:var(--acc,#8b5a2b)}}</style><h1>Đọc Kinh Thánh kèm giảng giải</h1>
<p>Đọc một chương Kinh Thánh (bản Việt ngữ 1934). Câu nào có dấu • nghĩa là có sách trong thư viện đã trích dẫn câu đó. Nhấn vào số câu để xem sách nào.</p>
<div class="sel noprint"><select id="bk" aria-label="Sách">{_nm_opts}</select><select id="ch" aria-label="Chương"></select><button class="btn s" id="pv" type="button">←</button><button class="btn s" id="nx" type="button">→</button></div>
<p class="m" id="st" role="status"></p><div id="tx"></div><div id="who"></div>
<p class="m">Nội dung Kinh Thánh lấy từ getBible (bản 1934) khi bạn đọc, cần có mạng. Danh sách sách trích dẫn dựa trên bản dịch AI chưa duyệt; một số trích dẫn có thể chưa chính xác.</p>
<script src="/doc-kinh-thanh.js" defer></script>'''
_open6("doc-kinh-thanh.html", page("Đọc Kinh Thánh kèm giảng giải | Reformed Vietnam", "Đọc từng chương Kinh Thánh bản 1934 và xem sách Cải Chánh nào trong thư viện đã trích dẫn từng câu.", "doc-kinh-thanh.html", _b)); urls.append("doc-kinh-thanh.html")

# --- Hoc thuoc long ---
_VS = [("Giăng 3:16",43,3,16,16),("Rô-ma 3:23",45,3,23,23),("Rô-ma 5:8",45,5,8,8),("Rô-ma 6:23",45,6,23,23),("Ê-phê-sô 2:8-9",49,2,8,9),("Giăng 14:6",43,14,6,6),("Rô-ma 8:1",45,8,1,1),("Rô-ma 8:28",45,8,28,28),("Phi-líp 4:6-7",50,4,6,7),("Phi-líp 4:13",50,4,13,13),("Thi Thiên 23:1",19,23,1,1),("Thi Thiên 46:1",19,46,1,1),("Thi Thiên 119:105",19,119,105,105),("Châm Ngôn 3:5-6",20,3,5,6),("Ê-sai 41:10",23,41,10,10),("Ê-sai 53:5",23,53,5,5),("Ma-thi-ơ 6:33",40,6,33,33),("Ma-thi-ơ 11:28",40,11,28,28),("Ma-thi-ơ 28:19-20",40,28,19,20),("Giăng 1:12",43,1,12,12),("Giăng 10:27-28",43,10,27,28),("1 Giăng 1:9",62,1,9,9),("2 Ti-mô-thê 3:16-17",55,3,16,17),("Hê-bơ-rơ 11:6",58,11,6,6),("Gia-cơ 1:5",59,1,5,5),("1 Phi-e-rơ 5:7",60,5,7,7),("Rô-ma 12:1-2",45,12,1,2),("Ga-la-ti 2:20",48,2,20,20),("Phi-líp 1:6",50,1,6,6),("Ê-phê-sô 6:1-3",49,6,1,3)]
_vj = _j3.dumps([{"r": r, "b": b, "c": c, "v": [v1, v2]} for r, b, c, v1, v2 in _VS], ensure_ascii=False)
_b = _NC3 + f'''<h1>Luyện thuộc lòng Kinh Thánh</h1>
<p>Ôn mỗi ngày vài câu. Câu nào nhớ được sẽ hiện lại sau nhiều ngày hơn; câu quên sẽ hiện lại sớm. Tiến độ lưu trong điện thoại của bạn.</p>
<p class="m" id="sum"></p>
<section class="nc" id="card"><h2 id="ref"></h2><p id="tv" style="font-size:1.15rem;line-height:1.6"></p>
<p><label>Chế độ: <select id="md"><option value="first">Chữ đầu mỗi từ</option><option value="half">Che một nửa</option><option value="full">Xem đủ</option></select></label></p>
<p><button class="btn" id="rt" type="button">Hiện cả câu</button></p><div id="lv"><p>Bạn nhớ được không?</p><button class="btn" id="ok" type="button">Nhớ rồi</button> <button class="btn s" id="no" type="button">Chưa nhớ</button></div></section>
<p id="done" class="nc" hidden></p><p><button class="btn s" id="add" type="button">Thêm câu mới</button></p>
<details class="nc"><summary>Danh sách {len(_VS)} câu</summary><ul id="ls"></ul></details>
<p class="m">Nội dung câu lấy từ bản Việt ngữ 1934 (getBible), cần có mạng. Hãy đối chiếu với Kinh Thánh của bạn.</p>
<script>window.RV_VERSES={_vj};</script><script src="/hoc-thuoc-long.js" defer></script>'''
_open6("hoc-thuoc-long.html", page("Luyện thuộc lòng Kinh Thánh | Reformed Vietnam", "Học thuộc lòng 30 câu Kinh Thánh quan trọng với lịch ôn lặp lại: câu nhớ được hiện thưa hơn, câu quên hiện sớm hơn.", "hoc-thuoc-long.html", _b)); urls.append("hoc-thuoc-long.html")

# --- Gia dinh tho phuong ---
_b = _NC3 + '''<h1>Thờ phượng gia đình 10 phút</h1>
<p>Mỗi ngày cả nhà quây quần khoảng 10 phút: nghe Lời Chúa, một câu giáo lý, một câu hỏi cho các em và cầu nguyện. Có thể làm vào bữa cơm hoặc buổi tối.</p>
<p class="noprint"><button class="btn s" id="pv" type="button">← Hôm qua</button> <button class="btn s" id="td" type="button">Hôm nay</button> <button class="btn s" id="nx" type="button">Ngày mai →</button> <span class="stt" id="dt"></span></p>
<section class="nc"><h2>1. Đọc Lời Chúa: <span id="rd"></span></h2><div id="tx"></div><p class="m">Một người đọc to, cả nhà lắng nghe. Hỏi: Đoạn này nói về ai? Có điều gì lạ?</p></section>
<section class="nc"><h2>2. Một câu giáo lý (Heidelberg)</h2><p><b id="hq"></b></p><p id="ha"></p></section>
<section class="nc"><h2>3. Câu hỏi cho các em</h2><p id="kq"></p></section>
<section class="nc"><h2>4. Cầu nguyện</h2><ul><li><b>Ngợi khen:</b> một điều con thấy Chúa tốt lành.</li><li><b>Tạ ơn:</b> một điều con cảm ơn Chúa hôm nay.</li><li><b>Xưng tội:</b> một điều con muốn Chúa tha thứ.</li><li><b>Cầu xin:</b> cho gia đình, người bệnh, người chưa tin.</li></ul><p>Kết thúc bằng Kinh Lạy Cha (Ma-thi-ơ 6:9-13).</p></section>
<p class="m">Kế hoạch đọc luân phiên các sách Mác, Giăng, vài Thi Thiên và thư tín. Giáo lý Heidelberg do AI hỗ trợ dịch, chưa được mục sư duyệt. Xem thêm <a href="/hoi-dap.html">hỏi đáp cho người mới tin</a> và <a href="/giao-ly-hang-ngay.html">giáo lý mỗi ngày</a>. Có thể in trang này (nút in của trình duyệt).</p>
<script src="/gia-dinh.js" defer></script>'''
_open6("gia-dinh-tho-phuong.html", page("Thờ phượng gia đình 10 phút mỗi ngày | Reformed Vietnam", "Gói thờ phượng gia đình 10 phút: đọc Lời Chúa, một câu giáo lý, câu hỏi cho các em và cầu nguyện, thay đổi mỗi ngày.", "gia-dinh-tho-phuong.html", _b)); urls.append("gia-dinh-tho-phuong.html")

# --- Hoi Thanh nha ---
_b = _NC3 + f'''<h1>Gói khởi sự Hội Thánh nhà</h1>
<p>Dành cho người dẫn một nhóm nhỏ hoặc Hội Thánh nhà mới bắt đầu. Có thể in và chỉnh cho phù hợp hoàn cảnh của bạn. Nên cộng tác với một mục sư hoặc Hội Thánh đã có kinh nghiệm.</p>
<section class="nc"><h2>1. Trình tự nhóm nhóm (khoảng 75 phút)</h2><ol><li>Chào đón và cầu nguyện mở đầu (5 phút)</li><li>Hát ngợi khen hoặc đọc một Thi Thiên chung (10 phút)</li><li>Đọc Kinh Thánh (5 phút)</li><li>Giảng hoặc học Lời Chúa (25 phút)</li><li>Thảo luận ba câu hỏi: Đoạn này nói gì về Chúa? Về tôi? Tôi sẽ vâng giữ điều gì? (15 phút)</li><li>Cầu thay và chia sẻ nhu cầu (10 phút)</li><li>Dâng hiến, thông báo, ban phước (5 phút)</li></ol><p class="m">Tiệc Thánh và báp-têm nên do người được Hội Thánh ủy nhiệm thực hiện. Hãy hỏi mục sư của bạn.</p></section>
<section class="nc"><h2>2. Lớp tín hữu mới (8 buổi)</h2><ol><li>Phúc Âm là gì: <a href="/phuc-am.html">Phúc Âm</a></li><li>Ân điển: <a href="/an-dien.html">Ân điển</a></li><li>Đức tin và xưng công bình: <a href="/xung-cong-binh.html">Xưng công bình</a></li><li>Cầu nguyện: {_lks3(["do-you-pray", "watson-lordsprayer"]) or "Cầu nguyện"}</li><li>Đọc và hiểu Kinh Thánh: <a href="/doc-kinh-thanh.html">Đọc Kinh Thánh kèm giảng giải</a></li><li>Hội Thánh và Tiệc Thánh: {_lks3(["heidelberg"]) or "Giáo lý Heidelberg"}</li><li>Sống thánh khiết: {_lks3(["ryle-holiness"]) or "Sự nên thánh"}</li><li>Làm chứng và phục vụ: <a href="/moi-tin-chua.html">Lộ trình 30 ngày</a></li></ol><p>Mỗi buổi có thể dùng <a href="/nhom-nho.html">kế hoạch nhóm nhỏ</a> làm khung thảo luận.</p></section>
<section class="nc"><h2>3. Giao ước mẫu (8 cam kết)</h2><ol><li>Chúng tôi tin Kinh Thánh là Lời Đức Chúa Trời, thẩm quyền tối hậu của đức tin và đời sống.</li><li>Chúng tôi tin Đức Chúa Trời Ba Ngôi và được cứu chỉ bởi ân điển qua đức tin nơi Chúa Giê-xu Christ.</li><li>Chúng tôi cam kết nhóm lại thờ phượng và học Lời Chúa đều đặn.</li><li>Chúng tôi cầu nguyện cho nhau và nâng đỡ nhau trong khó khăn.</li><li>Chúng tôi giữ lời nói chân thật, tránh nói xấu và hòa thuận với nhau.</li><li>Chúng tôi dâng hiến cách minh bạch và dùng tiền của cho công việc Chúa.</li><li>Chúng tôi tôn trọng gia đình, cha mẹ, và làm chứng bằng đời sống.</li><li>Chúng tôi chịu sự hướng dẫn của người lãnh đạo, và sẵn sàng sửa dạy nhau trong tình yêu thương.</li></ol></section>
<section class="nc"><h2>4. Danh sách kiểm tra cho người dẫn nhóm</h2><ul><li>Luôn có ít nhất hai người lớn khi có trẻ em; không để một người lớn ở một mình với một em.</li><li>Ghi sổ thu chi đơn giản, có người thứ hai kiểm tra.</li><li>Chuẩn bị trước bài học và đọc đoạn Kinh Thánh nhiều lần.</li><li>Có người hướng dẫn thuộc linh (mục sư hoặc người lớn tuổi trong đức tin) mà bạn báo cáo và xin lời khuyên.</li><li>Tìm hiểu các quy định hiện hành về sinh hoạt tôn giáo tại nơi bạn ở, và hỏi người có kinh nghiệm. Trang này không phải là tư vấn pháp lý.</li><li>Nếu có người cần bác sĩ hoặc giúp đỡ khẩn cấp, hãy giúp họ liên hệ ngay: xem sách {_lks3(["sach-23-khi-nao-can-gap-bac-si-va-vai-tro-cua-hoi-thanh", "sach-13-cham-soc-tin-huu-trong-khung-hoang"]) or "chăm sóc tín hữu"}.</li></ul></section>
<section class="nc"><h2>5. Sách giúp ích</h2><ul><li>{_lks3(["sach-11-dan-dat-va-ky-luat-hoi-thanh", "sach-12-giao-ly-van-dap-cho-lop-nhom-nho", "sach-14-day-giao-ly-o-nha", "sach-10-soan-bai-giang-giai-kinh", "baxter-pastor"])}</li></ul></section>''' + _DRAFT3
_open6("hoi-thanh-nha.html", page("Gói khởi sự Hội Thánh nhà | Reformed Vietnam", "Trình tự nhóm nhóm, lớp tín hữu mới 8 buổi, giao ước mẫu và danh sách kiểm tra cho người dẫn một Hội Thánh nhà hoặc nhóm nhỏ.", "hoi-thanh-nha.html", _b)); urls.append("hoi-thanh-nha.html")

# --- Lich su hom nay ---
_EV = [
 (1,1,1484,"Ulrich Zwingli chào đời tại Thụy Sĩ.",None),(2,18,1546,"Martin Luther qua đời tại Eisleben.",None),(3,17,1676,"Thomas Boston chào đời.","Thomas Boston"),(3,20,1661,"Samuel Rutherford qua đời.","Samuel Rutherford"),
 (3,22,1758,"Jonathan Edwards qua đời.","Jonathan Edwards"),(3,25,1843,"Robert Murray M'Cheyne qua đời, mới 29 tuổi.","Robert Murray M'Cheyne"),(5,10,1816,"J. C. Ryle chào đời.","J. C. Ryle"),(5,20,1732,"Thomas Boston qua đời.","Thomas Boston"),
 (5,21,1813,"Robert Murray M'Cheyne chào đời.","Robert Murray M'Cheyne"),(5,27,1564,"John Calvin qua đời tại Geneva.","John Calvin"),(6,9,1834,"William Carey qua đời.",None),(6,10,1900,"J. C. Ryle qua đời.","J. C. Ryle"),
 (6,19,1834,"Charles Haddon Spurgeon chào đời.","Charles Spurgeon"),(6,19,1878,"Charles Hodge qua đời.","Charles Hodge"),(7,1,1643,"Hội đồng Westminster họp lần đầu tại Tu viện Westminster.",None),(7,6,1415,"Jan Hus bị thiêu vì đức tin.",None),
 (7,10,1509,"John Calvin chào đời tại Noyon, Pháp.","John Calvin"),(7,29,1921,"Herman Bavinck qua đời.","Herman Bavinck"),(7,31,1889,"Horatius Bonar qua đời.","Horatius Bonar"),(8,24,1683,"John Owen qua đời.","John Owen"),
 (8,31,1688,"John Bunyan qua đời.","John Bunyan"),(9,30,1770,"George Whitefield qua đời.",None),(10,5,1703,"Jonathan Edwards chào đời.","Jonathan Edwards"),(10,6,1536,"William Tyndale bị xử tử vì dịch Kinh Thánh sang tiếng Anh.",None),
 (10,11,1531,"Ulrich Zwingli tử trận tại Kappel.",None),(10,26,1751,"Philip Doddridge qua đời.","Philip Doddridge"),(10,29,1837,"Abraham Kuyper chào đời.","Abraham Kuyper"),(10,31,1517,"Martin Luther đóng 95 luận đề tại Wittenberg.",None),
 (11,8,1920,"Abraham Kuyper qua đời.","Abraham Kuyper"),(11,10,1483,"Martin Luther chào đời.",None),(11,13,1618,"Hội nghị Dort khai mạc.",None),(11,24,1572,"John Knox qua đời tại Edinburgh.","John Knox"),
 (12,8,1691,"Richard Baxter qua đời.","Richard Baxter"),(12,13,1854,"Herman Bavinck chào đời.","Herman Bavinck"),(12,16,1714,"George Whitefield chào đời.",None),(12,19,1808,"Horatius Bonar chào đời.","Horatius Bonar"),
 (12,21,1807,"John Newton qua đời.","John Newton"),(12,28,1797,"Charles Hodge chào đời.","Charles Hodge"),(1,31,1892,"Charles Spurgeon qua đời tại Menton, Pháp.","Charles Spurgeon"),
]
def _auth6(n):
    if not n: return ""
    try: s = slug(n)
    except Exception: return ""
    return f"/a/{s}.html" if _o3.path.exists(f"a/{s}.html") else ""
_evj = _j3.dumps([[m, d, y, t, _auth6(a)] for m, d, y, t, a in _EV], ensure_ascii=False)
_b = _NC3 + f'''<h1>Hôm nay trong lịch sử Cải Chánh</h1><p class="m" id="dt"></p>
<section class="nc"><h2>Hôm nay</h2><ul id="td"></ul></section><section class="nc"><h2>30 ngày tới</h2><ul id="up"></ul></section>
<details class="nc"><summary>Toàn bộ danh sách ({len(_EV)} mốc)</summary><ul id="all"></ul></details>
<p class="m">Các ngày do AI tổng hợp từ tư liệu lịch sử phổ biến, chưa được duyệt. Một số ngày có thể khác nhau tùy lịch (cũ và mới); hãy kiểm tra trước khi trích dẫn.</p>
<script>window.RV_EV={_evj};</script><script src="/lich-su.js" defer></script>'''
_open6("lich-su-hom-nay.html", page("Hôm nay trong lịch sử Cải Chánh | Reformed Vietnam", "Mỗi ngày một mốc lịch sử Cải Chánh: ngày sinh, ngày mất của các nhà cải chánh, mục sư Thanh giáo và những văn kiện đức tin.", "lich-su-hom-nay.html", _b)); urls.append("lich-su-hom-nay.html")

# --- So hoc ---
_b = _NC3 + '''<h1>Sổ học của tôi</h1>
<p>Tất cả đoạn bạn đã tô màu hoặc ghi chú trong trình đọc, gom về một chỗ. Dữ liệu nằm trên thiết bị này; hãy xuất ra tệp để lưu hoặc chuyển sang thiết bị khác.</p>
<p class="noprint"><button class="btn" id="ex" type="button">Tải về (.txt)</button> <button class="btn s" id="cp" type="button">Sao chép</button></p>
<p class="m" id="st" role="status"></p><div id="ls"></div>
<p class="m">Khi đọc, chạm vào một đoạn trong trình đọc để tô màu hoặc ghi chú. Nếu bạn dùng đồng bộ, các đoạn đã đồng bộ cũng hiện ở đây sau khi tải lại trình đọc.</p>
<script src="/so-hoc.js" defer></script>'''
_open6("so-hoc.html", page("Sổ học của tôi: đoạn đã đánh dấu và ghi chú | Reformed Vietnam", "Xem và xuất các đoạn bạn đã tô màu hoặc ghi chú khi đọc sách Cải Chánh trên Reformed Vietnam.", "so-hoc.html", _b)); urls.append("so-hoc.html")

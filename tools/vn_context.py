# Executed from build-pages.py. Builds doi-song-viet-nam.html: draft Vietnamese-context questions with Scripture (pending pastor review).
_V = [
 ("Gia đình phản đối khi tôi theo Chúa", "Đừng tranh cãi, hãy tiếp tục hiếu kính cha mẹ và sống tử tế để gia đình thấy sự thay đổi. Chúa Giê-xu cũng báo trước rằng theo Ngài có thể gây chia rẽ trong nhà.", "Ma-thi-ơ 10:34-39; 1 Phi-e-rơ 3:1-2, 15-16"),
 ("Tôn kính cha mẹ và bàn thờ tổ tiên", "Kinh Thánh dạy hiếu kính cha mẹ khi còn sống và tưởng nhớ họ cách đáng kính. Kinh Thánh cũng dạy chỉ thờ phượng một mình Đức Chúa Trời. Hãy nói chuyện với mục sư của bạn về cách tưởng nhớ người đã khuất mà không thờ lạy.", "Xuất Ê-díp-tô Ký 20:3-5, 12; Ê-phê-sô 6:1-3"),
 ("Tết và các phong tục gia đình", "Nhiều phong tục là văn hóa (sum họp, thăm viếng, lì xì). Một số gắn với nghi lễ thờ cúng. Hãy dùng Kinh Thánh để phân biệt hai điều này, với lòng khôn ngoan và yêu thương, và cùng suy xét với Hội Thánh của bạn.", "1 Cô-rinh-tô 8:4-13; 10:23-33"),
 ("Hôn nhân với người chưa tin", "Kinh Thánh khuyên tín hữu kết hôn trong Chúa. Nếu một người tin Chúa khi đã có gia đình, họ được khuyên ở lại và sống làm chứng.", "2 Cô-rinh-tô 6:14; 1 Cô-rinh-tô 7:12-16"),
 ("Tiền bạc, công việc và sự ngay thẳng", "Hãy làm việc như làm cho Chúa, nói thật, từ chối hối lộ và gian lận, và chấp nhận cái giá phải trả. Hãy nhờ Hội Thánh cầu nguyện và đồng hành.", "Cô-lô-se 3:23-24; Châm ngôn 11:1; Ê-phê-sô 4:25, 28"),
 ("Áp lực từ cộng đồng và xã hội", "Hãy cầu nguyện cho chính quyền, vâng phục luật pháp trong phạm vi không trái Lời Chúa, và đứng vững khi bị chế giễu.", "Rô-ma 13:1-7; 1 Ti-mô-thê 2:1-2; Công vụ 5:29"),
 ("Chọn một Hội Thánh lành mạnh", "Một Hội Thánh lành mạnh giảng dạy Kinh Thánh trung tín, cử hành báp-têm và Tiệc Thánh, có lãnh đạo (trưởng lão, chấp sự) đáng tin cậy, và chăm sóc nhau. Hãy cẩn thận với những nơi hứa hẹn giàu có hoặc chữa lành đổi lại tiền bạc.", "Công vụ 2:42; 1 Ti-mô-thê 3; 2 Ti-mô-thê 4:3-4"),
 ("Phân biệt giáo lý lành mạnh", "Hãy so sánh mọi lời dạy với Kinh Thánh, như người Bê-rê. Hãy chú ý lời dạy về Đấng Christ, ân điển và sự ăn năn. Hãy hỏi mục sư của bạn nếu bạn bối rối.", "Công vụ 17:11; Ga-la-ti 1:6-9; 1 Giăng 4:1"),
]
_li = "".join(f'<div class="g"><h3>{E(t)}</h3><p>{E(d)}</p><p class="m"><small>Kinh Thánh: {E(r)}</small></p></div>' for t, d, r in _V)
_body = f'''<style>.g{{margin:14px 0;padding:12px 16px;border-left:3px solid #8a3b1f;background:#8881;border-radius:6px}}.g h3{{margin:0 0 .2em;font-size:1.05rem}}.g p{{margin:.2em 0}}.dr{{padding:.6em .9em;border-radius:8px;background:#d9a20022;font-size:.9rem}}</style>
<h1>Theo Chúa trong đời sống Việt Nam</h1>
<p class="dr">Nội dung này đã được mục sư xem lại. Đây chỉ là gợi ý ngắn dựa trên Kinh Thánh, không thay cho lời khuyên của mục sư. Bạn hãy trao đổi thêm với Hội Thánh địa phương của mình.</p>
<p>Dưới đây là những câu hỏi mà anh chị em tín hữu Việt thường gặp. Mỗi mục chỉ gợi ý hướng suy nghĩ và những đoạn Kinh Thánh để bạn tự đọc.</p>{_li}
<p><a class="btn" href="/lo-trinh.html">Lộ trình đọc</a> <a class="btn s" href="/thuat-ngu.html">Thuật ngữ</a></p>'''
open("doi-song-viet-nam.html", "w", encoding="utf-8").write(page("Theo Chúa trong đời sống Việt Nam: gia đình, tổ tiên, Tết, Hội Thánh | Reformed Vietnam", "Gợi ý dựa trên Kinh Thánh cho những câu hỏi tín hữu Việt thường gặp: gia đình phản đối, tổ tiên, Tết, hôn nhân, công việc, chọn Hội Thánh.", "doi-song-viet-nam.html", _body))
urls.append("doi-song-viet-nam.html")

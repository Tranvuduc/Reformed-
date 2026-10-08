# Executed from build-pages.py after sermon_pages.py. 4-week plan for a small reading group (doc-chung.html).
_GW = [
 ("Tuần 1: Phúc Âm", "phuc-am.html", "Phúc Âm là gì?", "compel-them-to-come-in"),
 ("Tuần 2: Ân điển", "an-dien.html", "Ân điển là gì?", "whitefield-con-duong-cua-an-dien"),
 ("Tuần 3: Chạy đến cùng Đấng Christ", "xung-cong-binh.html", "Xưng công bình là gì?", "mccheyne-cac-con-hay-chay-den-cung-dang-christ"),
 ("Tuần 4: Cầu nguyện", "moi-tin-chua.html", "Lộ trình 30 ngày cho người mới tin", "do-you-pray"),
]
_gb = ('<style>.gw{margin:18px 0;padding:14px 16px;border-radius:10px;background:#8881}.gw h2{margin:.1em 0 .4em;font-size:1.2rem}.gw ol{margin:.4em 0}</style>'
       '<h1>Nhóm đọc chung 4 tuần</h1><p>Dành cho nhóm nhỏ 3 đến 10 người, mỗi tuần gặp khoảng 60 phút. Mỗi buổi gồm một bài đọc nền tảng, một bài giảng và ba câu hỏi thảo luận. Xem thêm hướng dẫn tại <a href="/cho-muc-su.html">trang dành cho mục sư và nhóm nhỏ</a>.</p>'
       '<p class="m">Nội dung do AI hỗ trợ soạn, chưa được mục sư duyệt. Người hướng dẫn nên đọc trước và đối chiếu Kinh Thánh.</p>')
for _t, _pg, _pgt, _sl in _GW:
    _gq = _SP.get(_sl)
    _gqs = "".join(f"<li>{E(x)}</li>" for x in _gq[2]) if _gq else ""
    _gvs = (f'<p><b>Câu Kinh Thánh:</b> {E(_gq[0])}' + (f' – “{E(_gq[1])}”' if _gq[1] else "") + "</p>") if (_gq and _gq[0]) else ""
    _gb += (f'<section class="gw"><h2>{E(_t)}</h2><p>1. Đọc trước buổi họp: <a href="/{_pg}">{E(_pgt)}</a><br>2. Nghe hoặc đọc bài giảng: <a href="/bai-giang/{_sl}.html">trang bài giảng</a></p>{_gvs}'
            f'<p><b>Thảo luận:</b></p><ol>{_gqs}</ol><p><small>Gợi ý buổi họp: 10 phút cầu nguyện và chia sẻ, 15 phút đọc Kinh Thánh, 25 phút thảo luận, 10 phút cầu nguyện kết thúc.</small></p></section>')
open("doc-chung.html", "w", encoding="utf-8").write(page("Nhóm đọc chung 4 tuần: Phúc Âm, ân điển, đức tin, cầu nguyện | Reformed Vietnam",
    "Kế hoạch 4 tuần cho nhóm nhỏ: bài đọc, bài giảng Cải Chánh và câu hỏi thảo luận mỗi tuần.", "doc-chung.html", _gb)); urls.append("doc-chung.html")

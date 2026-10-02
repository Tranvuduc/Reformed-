# Executed from build-pages.py. Pillar pages (Phúc Âm, Ân điển, Xưng công bình). Draft, pending pastor review. Scripture = Vietnamese 1934.
_PC = '<style>.q{margin:12px 0;padding:10px 16px;border-left:3px solid #8a3b1f;background:#8881;border-radius:6px}.q p{margin:.2em 0}.q small{opacity:.75}.dr{padding:.6em .9em;border-radius:8px;background:#d9a20022;font-size:.9rem}.rl a{display:block;margin:.3em 0}.bc{font-size:.85rem;opacity:.8}</style>'
_DR = '<p class="dr">Bản nháp do AI hỗ trợ soạn, chưa được mục sư duyệt giáo lý. Kinh Thánh là thẩm quyền tối hậu. Hãy đối chiếu với Kinh Thánh và hỏi mục sư của bạn.</p>'
def _v(ref, txt): return f'<blockquote class="q"><p>{E(txt)}</p><p><small>{E(ref)} (Kinh Thánh Tiếng Việt 1934)</small></p></blockquote>'
def _rel(L): return '<div class="rl">' + "".join(f'<a href="{u}">{E(t)}</a>' for u, t in L) + '</div>'
_PILLARS = [
 ("phuc-am.html", "Phúc Âm là gì? Hướng dẫn Kinh Thánh cho người mới",
  "Phúc Âm (Tin Lành) là tin vui: Chúa Giê-xu chịu chết vì tội chúng ta và sống lại. Giải thích đơn giản từ Kinh Thánh, kèm sách đọc thêm miễn phí.",
  "Phúc Âm là gì?", "Phúc Âm (còn gọi là Tin Lành) là tin vui rằng Đức Chúa Trời cứu tội nhân qua Chúa Giê-xu Christ.",
  [("Định nghĩa ngắn", "Phúc Âm không phải trước hết là lời khuyên cách sống, mà là tin tức về điều Đức Chúa Trời đã làm: Chúa Giê-xu chịu chết vì tội chúng ta, được chôn, sống lại ngày thứ ba. Ai ăn năn và tin Ngài thì được tha tội và nhận sự sống đời đời."),
   ("Điều thường bị hiểu sai", "Nhiều người nghĩ Phúc Âm là “cố sống tốt để được Chúa thương”. Kinh Thánh nói ngược lại: chúng ta được cứu không phải nhờ việc làm của mình, mà nhờ điều Đấng Christ đã làm thay cho chúng ta. Việc lành là kết quả của sự cứu, không phải điều kiện để được cứu."),
   ("Góc nhìn Cải Chánh", "Truyền thống Cải Chánh nhấn mạnh rằng sự cứu rỗi trọn vẹn là công việc của Đức Chúa Trời, từ đầu đến cuối: Ngài kêu gọi, Đấng Christ chuộc tội, Thánh Linh đổi mới lòng người. Vì thế người tin có thể bình an, không dựa vào công trạng mình. Các truyền thống Cơ Đốc khác cũng giữ Phúc Âm làm trung tâm, nhưng giải thích khác nhau về vai trò của ý chí con người; bạn nên nghe cả mục sư của mình.")],
  [("1 Cô-rinh-tô 15:3-4", "Vả trước hết tôi đã dạy dỗ anh em điều mà chính tôi đã nhận lãnh, ấy là Đấng Christ chịu chết vì tội chúng ta theo lời Kinh Thánh; Ngài đã bị chôn, đến ngày thứ ba, Ngài sống lại, theo lời Kinh Thánh;"),
   ("Rô-ma 1:16", "Thật vậy, tôi không hổ thẹn về Tin Lành đâu, vì là quyền phép của Đức Chúa Trời để cứu mọi kẻ tin, trước là người Giu-đa, sau là người Gờ-réc;"),
   ("Mác 1:15", "mà rằng: Kỳ đã trọn, nước Đức Chúa Trời đã đến gần; các ngươi hãy ăn năn và tin đạo Tin Lành."),
   ("Giăng 3:16", "Vì Đức Chúa Trời yêu thương thế gian, đến nỗi đã ban Con một của Ngài, hầu cho hễ ai tin Con ấy không bị hư mất mà được sự sống đời đời.")],
  [("/moi-tin-chua.html", "Lộ trình 30 ngày cho người mới tin Chúa"), ("/ban-dich/sach-18-duc-tin-cai-chanh-trong-15-phut.html", "Đức tin Cải Chánh trong 15 phút"), ("/an-dien.html", "Ân điển là gì?"), ("/xung-cong-binh.html", "Xưng công bình là gì?")]),
 ("an-dien.html", "Ân điển là gì? Giải thích đơn giản từ Kinh Thánh",
  "Ân điển là ơn Đức Chúa Trời ban nhưng không cho người không xứng đáng. Định nghĩa, câu Kinh Thánh chính, hiểu lầm thường gặp và sách đọc thêm miễn phí.",
  "Ân điển là gì?", "Ân điển là ơn Đức Chúa Trời ban nhưng không, cho những người không xứng đáng.",
  [("Định nghĩa ngắn", "Ân điển là sự tốt lành Đức Chúa Trời bày tỏ cho tội nhân mà không đòi hỏi họ phải xứng đáng. Chúng ta không mua, không kiếm, không đổi được. Chúng ta chỉ nhận lấy bằng đức tin."),
   ("Điều thường bị hiểu sai", "Có người cho rằng ân điển là “Chúa bỏ qua cho, muốn sống sao cũng được”. Kinh Thánh dạy ân điển cứu chúng ta và cũng dạy chúng ta sống khác đi: ân điển không chỉ tha tội, mà còn thay đổi lòng. Cũng có người nghĩ mình phải làm đủ việc tốt thì ân điển mới đến; đó là điều Phao-lô bác bỏ."),
   ("Góc nhìn Cải Chánh", "Truyền thống Cải Chánh nói “chỉ bởi ân điển” (Sola Gratia): từ khởi đầu đến kết thúc, sự cứu là món quà. Các truyền thống khác cũng nói về ân điển, nhưng giải thích khác nhau về việc ân điển hợp tác với ý chí con người thế nào. Hãy xem Kinh Thánh và hỏi mục sư của bạn.")],
  [("Ê-phê-sô 2:8-9", "Vả, ấy là nhờ ân điển, bởi đức tin, mà anh em được cứu, điều đó không phải đến từ anh em, bèn là sự ban cho của Đức Chúa Trời. Ấy chẳng phải bởi việc làm đâu, hầu cho không ai khoe mình;"),
   ("Rô-ma 3:23-24", "vì mọi người đều đã phạm tội, thiếu mất sự vinh hiển của Đức Chúa Trời, và họ nhờ ân điển Ngài mà được xưng công bình nhưng không, bởi sự chuộc tội đã làm trọn trong Đức Chúa Jêsus Christ,"),
   ("Tít 2:11-12", "Vả, ân điển Đức Chúa Trời hay cứu mọi người, đã được bày tỏ ra rồi. Ân ấy dạy chúng ta chừa bỏ sự không tôn kính và tài đức thế gian, phải sống ở đời nầy theo tiết độ, công bình, nhân đức,"),
   ("2 Cô-rinh-tô 12:9", "Nhưng Chúa phán rằng: Ân điển ta đủ cho ngươi rồi, vì sức mạnh của ta nên trọn vẹn trong sự yếu đuối. Vậy, tôi sẽ rất vui lòng khoe mình về sự yếu đuối tôi, hầu cho sức mạnh của Đấng Christ ở trong tôi.")],
  [("/ban-dich/sach-07-an-dien-va-cong-duc.html", "Ân điển và “công đức” (sách Việt)"), ("/ban-dich/sach-03-an-dien-trong-nuoc-mat.html", "Ân điển trong nước mắt (sách Việt)"), ("/phuc-am.html", "Phúc Âm là gì?"), ("/xung-cong-binh.html", "Xưng công bình là gì?"), ("/cai-chanh-la-gi.html", "Cải Chánh là gì?")]),
 ("xung-cong-binh.html", "Xưng công bình là gì? Giải thích đơn giản từ Kinh Thánh",
  "Xưng công bình là Đức Chúa Trời tuyên bố người tin là công bình nhờ Đấng Christ, không nhờ việc làm. Giải thích, Kinh Thánh, hiểu lầm và sách đọc thêm.",
  "Xưng công bình là gì?", "Xưng công bình là việc Đức Chúa Trời tuyên bố người có tội là công bình trước mặt Ngài, vì Đấng Christ, bởi đức tin.",
  [("Định nghĩa ngắn", "Xưng công bình là lời tuyên bố của quan tòa: tội của người tin đã được tha, và họ được kể là công bình nhờ công việc của Đấng Christ. Đó là một lời tuyên bố một lần, chứ không phải một quá trình làm cho ta tốt dần lên."),
   ("Điều thường bị hiểu sai", "Hai hiểu lầm hay gặp: (1) xưng công bình nghĩa là Chúa làm cho ta hết tội ngay lập tức trong đời sống; (2) đức tin là một việc làm để “đổi lấy” sự cứu. Kinh Thánh nói đức tin chỉ là bàn tay đón nhận; điều cứu chúng ta là Đấng Christ. Việc nên thánh (đời sống được đổi mới dần) đi theo sau, và cần được phân biệt với xưng công bình."),
   ("Góc nhìn Cải Chánh và các góc nhìn khác", "Cải Chánh nhấn mạnh “chỉ bởi đức tin” (Sola Fide): sự công bình của Đấng Christ được kể cho người tin. Truyền thống Công giáo La Mã hiểu xưng công bình gồm cả việc được làm cho công bình bên trong, và đây là một điểm khác biệt chính của thời Cải cách. Có thêm các cuộc thảo luận về cách hiểu của Phao-lô, và bạn nên đọc Kinh Thánh cùng mục sư của mình.")],
  [("Rô-ma 3:23-24", "vì mọi người đều đã phạm tội, thiếu mất sự vinh hiển của Đức Chúa Trời, và họ nhờ ân điển Ngài mà được xưng công bình nhưng không, bởi sự chuộc tội đã làm trọn trong Đức Chúa Jêsus Christ,"),
   ("Rô-ma 3:28", "vì chúng ta kể rằng người ta được xưng công bình bởi đức tin, chớ không bởi việc làm theo luật pháp."),
   ("Rô-ma 5:1", "Vậy chúng ta đã được xưng công bình bởi đức tin, thì được hòa thuận với Đức Chúa Trời, bởi Đức Chúa Jêsus Christ chúng ta,"),
   ("Ga-la-ti 2:16", "Dầu vậy, đã biết rằng người ta được xưng công bình, chẳng phải bởi các việc luật pháp đâu, bèn là cậy đức tin trong Đức Chúa Jêsus Christ, nên chính chúng tôi đã tin Đức Chúa Jêsus Christ, để được xưng công bình bởi đức tin trong Đấng Christ, chớ chẳng bởi các việc luật pháp; vì chẳng có ai được xưng công bình bởi các việc luật pháp."),
   ("Rô-ma 4:5", "còn kẻ chẳng làm việc chi hết, nhưng tin Đấng xưng người có tội là công bình, thì đức tin của kẻ ấy kể là công bình cho mình.")],
  [("/ban-dich/sach-07-an-dien-va-cong-duc.html", "Ân điển và “công đức” (sách Việt)"), ("/ban-dich/sach-18-duc-tin-cai-chanh-trong-15-phut.html", "Đức tin Cải Chánh trong 15 phút"), ("/phuc-am.html", "Phúc Âm là gì?"), ("/an-dien.html", "Ân điển là gì?"), ("/thuat-ngu.html", "Thuật ngữ thần học")]),
]
for _p, _t, _d, _h, _ans, _secs, _ver, _rl in _PILLARS:
    _body = (_PC + f'<p class="bc"><a href="/">Trang chủ</a> → <a href="/cai-chanh-la-gi.html">Tìm hiểu</a> → {E(_h)}</p><h1>{E(_h)}</h1>' + _DR
             + f'<p><b>{E(_ans)}</b></p>' + "".join(f'<h2>{E(a)}</h2><p>{E(b)}</p>' for a, b in _secs)
             + '<h2>Kinh Thánh cần đọc</h2>' + "".join(_v(r, t) for r, t in _ver)
             + '<h2>Đọc thêm</h2>' + _rel(_rl))
    _ld = {"@context": "https://schema.org", "@type": "Article", "headline": _h, "inLanguage": "vi", "url": f"{SITE}/{_p}", "description": _d}
    open(_p, "w", encoding="utf-8").write(page(f"{_t} | Reformed Vietnam", _d, _p, _body, _ld)); urls.append(_p)

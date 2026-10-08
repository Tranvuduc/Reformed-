# Executed from build-pages.py. One page per hosted sermon (bai-giang/<slug>.html) + video page (only when tools/videos.json has items). Draft, AI-assisted, not pastor-reviewed.
import json as _j2
_SP = {
 "compel-them-to-come-in": ("Lu-ca 14:23", "Chủ nhà lại biểu rằng: Hãy ra ngoài đường và dọc hàng rào, gặp ai thì ép mời vào, cho được đầy nhà ta.",
   ["Trong dụ ngôn tiệc lớn, những người được mời đầu tiên đã từ chối. Bạn nghĩ vì sao con người từ chối lời mời của Phúc Âm?", "“Ép mời vào” nghĩa là gì trong lời kêu gọi người khác đến với Chúa? Điều gì khác với việc cưỡng ép?", "Bạn có thể mời ai đến với Chúa tuần này, và sẽ nói gì với họ?"]),
 "whitefield-con-duong-cua-an-dien": ("Giê-rê-mi 8:11", "Chúng nó rịt vết thương cho con gái dân ta cách sơ sài, nói rằng: Bình an, bình an! mà không bình an chi hết.",
   ["Thế nào là “bình an giả”? Những điều gì dễ làm ta tưởng mình bình an với Chúa mà thật ra chưa phải vậy?", "Whitefield nói về cách Chúa đem tội nhân đến với Đấng Christ. Điều gì trong lời giảng làm bạn suy nghĩ nhất?", "Bạn nhận ra nơi mình có chỗ nào đang “rịt vết thương cách sơ sài” không?"]),
 "edwards-toi-nhan-trong-tay-duc-chua-troi-thanh-no": ("Phục-truyền 32:35", "Khi chân chúng nó xiêu tó, Sự báo thù sẽ thuộc về ta, phần đối trả sẽ qui về ta. Vì ngày bại hoại của chúng nó hầu gần, Và những tai họa buộc phải xảy ra cho chúng nó đến mau.",
   ["Bài giảng này nhấn mạnh sự nghiêm trọng của tội. Bài giảng nói gì về sự nhịn nhục của Đức Chúa Trời?", "Hãy đọc bài giảng cùng Giăng 3:16 và Rô-ma 5:8. Phúc Âm làm gì để đáp lại sự phán xét?", "Vì sao một số người ngày nay thấy khó nghe loại bài giảng này? Bạn nghĩ sao?"]),
 "chalmers-quyen-nang-cua-mot-tinh-yeu-moi": ("1 Giăng 2:15", "Chớ yêu thế gian, cũng đừng yêu các vật ở thế gian nữa; nếu ai yêu thế gian, thì sự kính mến Đức Chúa Cha chẳng ở trong người ấy.",
   ["Chalmers cho rằng chỉ ra lệnh “đừng yêu thế gian” thì chưa đủ. Vì sao một tình yêu mới mới có sức thay thế?", "Điều gì đang chiếm chỗ lớn trong lòng bạn? Làm sao chiêm ngưỡng Đấng Christ thay đổi điều đó?", "Bạn thấy thế nào về ý “sức mạnh đẩy ra” của một tình yêu mới?"]),
 "newton-cay-non-bong-lua-hot-chac": ("Mác 4:28", "Vì đất tự sanh ra hoa lợi: ban đầu là cây, kế đến bông, đoạn bông kết thành hột.",
   ["Newton so sánh đời sống thuộc linh với cây non, bông lúa và hột chắc. Bạn thấy mình đang ở giai đoạn nào?", "Điều gì giúp một tín hữu lớn lên từ giai đoạn này sang giai đoạn sau?", "Bạn có thể khích lệ người mới tin hoặc người đang yếu đuối thế nào?"]),
 "spurgeon-y-chi-tu-do-mot-ke-no-le": (None, None,
   ["Spurgeon nói ý chí con người bị ràng buộc bởi tội. Hãy đọc bài và tóm lại lập luận chính của ông.", "Điều gì trong bài làm bạn đồng ý, và điều gì bạn muốn hỏi thêm mục sư?", "Hãy đối chiếu bài giảng với Kinh Thánh. Các Hội Thánh khác nhau thế nào về chủ đề này?"]),
 "spurgeon-loi-benh-vuc-thuyet-calvin": (None, None,
   ["Spurgeon gọi các giáo lý ân điển là Phúc Âm. Ông dùng lập luận nào?", "Điều gì bạn thấy dễ hiểu và điều gì còn khó trong bài?", "Các truyền thống Cơ Đốc khác trả lời thế nào về các câu hỏi này? Hãy trò chuyện với mục sư của bạn."]),
 "mccheyne-cac-con-hay-chay-den-cung-dang-christ": (None, None,
   ["M’Cheyne viết cho trẻ em. Điều gì trong lời lẽ ông đơn giản mà sâu?", "Bạn dạy hay chia sẻ Phúc Âm với trẻ em như thế nào?", "Vì sao đến với Đấng Christ sớm là điều quan trọng?"]),
 "do-you-pray": (None, None,
   ["Bạn cầu nguyện riêng mỗi ngày không? Điều gì cản trở bạn?", "Trong bảy lý do của bài, lý do nào làm bạn suy nghĩ nhất?", "Bạn sẽ dành thời gian nào trong ngày để cầu nguyện, bắt đầu từ tuần này?"]),
}
_scss = '<style>.q{margin:12px 0;padding:10px 16px;border-left:3px solid var(--acc);background:#8881;border-radius:6px}.q p{margin:.2em 0}.dr{padding:.6em .9em;border-radius:8px;background:#d9a20022;font-size:.9rem}.bc{font-size:.85rem;opacity:.8}</style>'
_sdesc = {s: d for g, L in _SG for s, a, d in L}
_sauth = {s: a for g, L in _SG for s, a, d in L}
os.makedirs("bai-giang", exist_ok=True)
for _s, (_ref, _vt, _qs) in _SP.items():
    if _s not in _VT: continue
    _title = _VT[_s][0]
    _b = (_scss + f'<p class="bc"><a href="/">Trang chủ</a> → <a href="/bai-giang.html">Bài giảng</a> → {E(_title)}</p><h1>{E(_title)}</h1><p class="m">{E(_sauth.get(_s, ""))} · khoảng {_min(_s)} phút đọc</p>'
          '<p class="dr">Bản tiếng Việt do AI hỗ trợ dịch, chưa được mục sư duyệt. Phần câu hỏi là gợi ý của AI. Hãy đọc với tinh thần Bê-rê và đối chiếu Kinh Thánh.</p>'
          f'<p>{E(_sdesc.get(_s, ""))}</p>'
          + (f'<h2>Kinh Thánh chính</h2><blockquote class="q"><p>{E(_vt)}</p><p><small>{E(_ref)} (Kinh Thánh Tiếng Việt 1934)</small></p></blockquote>' if _ref else '')
          + f'<p><a class="btn" href="/reader.html?id=vn/{_s}">Đọc bài giảng</a></p>'
          '<h2>Câu hỏi thảo luận cho nhóm nhỏ</h2><ol>' + "".join(f'<li>{E(q)}</li>' for q in _qs) + '</ol>'
          '<p><a href="/bai-giang.html">← Tất cả bài giảng</a> · <a href="/cho-muc-su.html">Cách dùng cho nhóm nhỏ</a></p>')
    _pp = f"bai-giang/{_s}.html"
    open(_pp, "w", encoding="utf-8").write(page(f"{_title} | Bài giảng | Reformed Vietnam", f"{_sauth.get(_s, '')}: {_sdesc.get(_s, '')}", _pp, _b, {"@context": "https://schema.org", "@type": "Article", "headline": _title, "inLanguage": "vi", "url": f"{SITE}/{_pp}"})); urls.append(_pp)
# link each sermon on the compilation page to its own page
_ph = open("bai-giang.html", encoding="utf-8").read()
for _s in _SP:
    _ph = _ph.replace(f'<h3><a href="/reader.html?id=vn/{_s}">', f'<h3><a href="/bai-giang/{_s}.html">')
open("bai-giang.html", "w", encoding="utf-8").write(_ph)
# video page: only when the curated list has items
_vp = "tools/videos.json"
_vl = _j2.load(open(_vp, encoding="utf-8")) if os.path.exists(_vp) else []
if _vl:
    _by = {}
    for _v in _vl: _by.setdefault(_v.get("topic", "Khác"), []).append(_v)
    _vb = ('<style>.vd{margin:14px 0}.vd iframe{width:100%;aspect-ratio:16/9;border:0;border-radius:8px}.dr{padding:.6em .9em;border-radius:8px;background:#d9a20022;font-size:.9rem}</style><h1>Video chọn lọc</h1><p class="dr">Các video do chủ sở hữu đăng trên YouTube. Thư viện chỉ nhúng hoặc dẫn link, không lưu lại. Nội dung do người dạy chịu trách nhiệm; hãy đối chiếu Kinh Thánh.</p>'
           + "".join(f'<h2>{E(t)}</h2>' + "".join(f'<div class="vd"><h3>{E(v["title"])}</h3><p><small>{E(v.get("by", ""))}</small></p><p>{E(v.get("note", ""))}</p><iframe src="https://www.youtube-nocookie.com/embed/{E(v["id"])}" title="{E(v["title"])}" loading="lazy" allowfullscreen></iframe></div>' for v in L) for t, L in _by.items()))
    _CH = [("BibleProject – Tiếng Việt (YouTube)", "https://www.youtube.com/@BibleProjectVietnamese", "Video hoạt hình tổng quan từng sách Kinh Thánh. Đây là kênh giải nghĩa Kinh Thánh chung, không phải kênh riêng của Cải Chánh."),
           ("Reformed Resources – God's Sovereignty in Vietnam", "https://godssovereigntyinvietnam.com/page-where-am-i/", "Trang tổng hợp tài liệu Cải Chánh tiếng Việt, gồm các bản tín điều và sách giáo lý."),
           ("Ligonier Ministries Tiếng Việt", "https://vi.ligonier.org", "Bài viết và tài liệu của Ligonier đã dịch sang tiếng Việt.")]
    _vb += '<h2>Kênh và nguồn tiếng Việt</h2><p class="m">Chỉ liệt kê các nguồn đã xác nhận có thật. Hãy tự đối chiếu giáo lý với Kinh Thánh.</p><ul>' + "".join(f'<li><a href="{E(u)}" rel="noopener" target="_blank">{E(t)}</a><br><small>{E(d)}</small></li>' for t, u, d in _CH) + '</ul>'
    open("video.html", "w", encoding="utf-8").write(page("Video giảng dạy Cơ Đốc chọn lọc bằng tiếng Việt | Reformed Vietnam", "Video giảng dạy và bài giảng chọn lọc về Kinh Thánh và giáo lý Cải Chánh, nhúng từ YouTube.", "video.html", _vb)); urls.append("video.html")

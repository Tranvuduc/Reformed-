# Executed from build-pages.py after reformed101.py. Pages: bat-dau, ve-chung-toi, trang-thai-ban-dich, moi-cap-nhat (+cap-nhat.xml), kinh-thanh.
import json as _j9, re as _r9, os as _o9
_NC = '<style>.nc{margin:16px 0;padding:14px 16px;border-radius:10px;background:#8881}.nc h2{margin:.1em 0 .4em;font-size:1.15rem}.nc ul,.nc ol{margin:.4em 0 .4em 1.2em;padding:0}.nc li{margin:.25em 0}.stt{font-size:.85rem;opacity:.75}.tb{width:100%;border-collapse:collapse;font-size:.92rem}.tb td,.tb th{padding:6px 8px;border-bottom:1px solid #8883;text-align:left;vertical-align:top}</style>'
_DRAFT = '<p class="m">Nội dung do AI hỗ trợ soạn, chưa được mục sư duyệt. Hãy đối chiếu với Kinh Thánh và hỏi mục sư của bạn.</p>'
_idx9 = _j9.load(open("translations/index.json", encoding="utf-8"))
_pub9 = [b for b in _idx9 if not b.get("hold") and _o9.path.exists("translations/" + b["file"])]

# 1. Bat dau o day
_b1 = _NC + '<h1>Bắt đầu ở đây</h1><p>Reformed Vietnam là thư viện miễn phí gồm sách, bài giảng và bản dịch Cải Chánh bằng tiếng Việt. Không bán gì, không cần tài khoản. Chọn một lối đi dưới đây tùy bạn đang ở đâu.</p>'
for _t, _p, _d in [
    ("Tôi mới tin Chúa", "/moi-tin-chua.html", "Lộ trình 30 ngày, mỗi ngày khoảng 10 phút: một đoạn Kinh Thánh, một phần đọc thêm và một lời cầu nguyện."),
    ("Tôi muốn hiểu Phúc Âm", "/phuc-am.html", "Phúc Âm là gì, ân điển là gì, xưng công bình là gì, bằng lời đơn giản."),
    ("Cải Chánh là gì?", "/cai-chanh-la-gi.html", "Giới thiệu ngắn về đức tin Cải Chánh và các bản tuyên xưng."),
    ("Tôi muốn nghe thay vì đọc", "/sach-noi.html", "Nghe sách nói. Một số sách có giọng tự nhiên tạo sẵn."),
    ("Tôi muốn đọc một cuốn sách ngắn", "/tieng-viet.html", "Sách đã dịch sang tiếng Việt, nhiều cuốn chỉ đọc vài chục phút."),
    ("Tôi dẫn nhóm nhỏ", "/doc-chung.html", "Kế hoạch đọc chung 4 tuần cho nhóm 3 đến 10 người."),
    ("Tôi là mục sư hoặc người hướng dẫn", "/cho-muc-su.html", "Hướng dẫn dùng thư viện cho Hội Thánh, và nơi để góp ý duyệt bản dịch."),
]:
    _b1 += f'<section class="nc"><h2><a href="{_p}">{E(_t)}</a></h2><p>{E(_d)}</p></section>'
_b1 += '<section class="nc"><h2>Nên đọc kèm</h2><ul><li><a href="/ve-chung-toi.html">Về chúng tôi và cách chọn sách</a></li><li><a href="/trang-thai-ban-dich.html">Trạng thái duyệt của từng bản dịch</a></li><li><a href="/moi-cap-nhat.html">Mới cập nhật</a></li></ul></section>' + _DRAFT
open("bat-dau.html", "w", encoding="utf-8").write(page("Bắt đầu ở đây | Reformed Vietnam", "Chọn lối đi phù hợp: mới tin Chúa, tìm hiểu Phúc Âm, nghe sách nói, đọc sách ngắn hoặc dẫn nhóm nhỏ.", "bat-dau.html", _b1)); urls.append("bat-dau.html")

# 2. Ve chung toi
_b2 = _NC + '<h1>Về chúng tôi</h1><p>Reformed Vietnam là một thư viện miễn phí, không thương mại, nhằm giúp người Việt đọc và nghe những tác phẩm Cải Chánh xưa nay bằng tiếng Việt tự nhiên của Hội Thánh.</p>' \
 '<section class="nc"><h2>Chúng tôi chọn sách như thế nào</h2><ul>' \
 '<li>Sách thuộc phạm vi công cộng, hoặc bản dịch do chính chúng tôi thực hiện, thì được lưu trên web này.</li>' \
 '<li>Sách tiếng Việt của nơi khác còn bản quyền chỉ được dẫn liên kết, không sao chép về đây.</li>' \
 '<li>Chúng tôi ưu tiên tác giả và tác phẩm có truyền thống Cải Chánh lâu đời, thuộc dòng Thanh giáo, Trưởng Lão, Báp-tít Cải Chánh và các bản tuyên xưng đức tin.</li>' \
 '<li>Kinh Thánh trích dẫn theo bản Việt ngữ 1934.</li></ul></section>' \
 '<section class="nc"><h2>Về bản dịch</h2><p>Phần lớn bản dịch có sự hỗ trợ của AI và được đánh dấu rõ là <b>chưa được mục sư duyệt giáo lý</b>. Chúng tôi xem Kinh Thánh là thẩm quyền tối hậu. Mỗi bản dịch chỉ giúp bạn học, và không thay thế Hội Thánh địa phương. Xem <a href="/trang-thai-ban-dich.html">trạng thái từng bản dịch</a>.</p></section>' \
 '<section class="nc"><h2>Góp ý và duyệt</h2><p>Nếu bạn là mục sư hoặc người có chuyên môn thần học và muốn giúp duyệt bản dịch, xem <a href="/cho-muc-su.html">trang dành cho mục sư</a>.</p></section>' \
 '<p class="m">Trang này là bản nháp về cách chúng tôi làm việc và chưa được mục sư duyệt.</p>'
open("ve-chung-toi.html", "w", encoding="utf-8").write(page("Về chúng tôi và cách chọn sách | Reformed Vietnam", "Reformed Vietnam là thư viện Cải Chánh miễn phí bằng tiếng Việt: cách chọn sách, bản quyền và cách đánh dấu bản dịch.", "ve-chung-toi.html", _b2)); urls.append("ve-chung-toi.html")

# 3. Trang thai ban dich
_rv9 = [b for b in _pub9 if b.get("reviewed")]
_rows = "".join(f'<tr><td><a href="/ban-dich/{E(_o9.path.splitext(b["file"])[0])}.html">{E(b.get("title", ""))}</a></td><td>{E(b.get("author", ""))}</td><td>{"Đã duyệt" if b.get("reviewed") else "Chưa duyệt"}</td></tr>' for b in sorted(_pub9, key=lambda x: (x.get("author", ""), x.get("title", ""))))
_b3 = _NC + f'<h1>Trạng thái bản dịch</h1><p>Hiện có <b>{len(_pub9)}</b> bản dịch tiếng Việt. Đã được mục sư duyệt: <b>{len(_rv9)}</b>. Chưa duyệt: <b>{len(_pub9) - len(_rv9)}</b>.</p><p>“Chưa duyệt” nghĩa là bản dịch có AI hỗ trợ và chưa có mục sư đọc lại giáo lý. Hãy đối chiếu với Kinh Thánh. Mục sư muốn giúp duyệt: <a href="/cho-muc-su.html">xem hướng dẫn</a>.</p>' \
 f'<table class="tb"><tr><th>Sách</th><th>Tác giả</th><th>Trạng thái</th></tr>{_rows}</table>'
open("trang-thai-ban-dich.html", "w", encoding="utf-8").write(page("Trạng thái duyệt các bản dịch | Reformed Vietnam", "Danh sách các bản dịch tiếng Việt và trạng thái duyệt giáo lý của từng bản.", "trang-thai-ban-dich.html", _b3)); urls.append("trang-thai-ban-dich.html")

# 4. Moi cap nhat + RSS
_cn = _j9.load(open("tools/cap_nhat.json", encoding="utf-8"))
_li = "".join(f'<li><b>{E(x["d"])}</b> · <a href="{E(x["u"])}">{E(x["t"])}</a></li>' for x in _cn)
_b4 = _NC + f'<h1>Mới cập nhật</h1><ul class="nc">{_li}</ul><p><a class="btn s" href="/cap-nhat.xml">RSS</a></p>'
open("moi-cap-nhat.html", "w", encoding="utf-8").write(page("Mới cập nhật | Reformed Vietnam", "Những thay đổi và nội dung mới gần đây của thư viện Reformed Vietnam.", "moi-cap-nhat.html", _b4)); urls.append("moi-cap-nhat.html")
import email.utils as _eu, datetime as _dt9
_it = "".join(f'<item><title>{E(x["t"])}</title><link>{SITE}{E(x["u"])}</link><guid>{SITE}/moi-cap-nhat.html#{x["d"]}-{i}</guid><pubDate>{_eu.format_datetime(_dt9.datetime.fromisoformat(x["d"]+"T06:00:00+07:00"))}</pubDate></item>' for i, x in enumerate(_cn))
open("cap-nhat.xml", "w", encoding="utf-8").write(f'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>Reformed Vietnam · Mới cập nhật</title><link>{SITE}/moi-cap-nhat.html</link><description>Nội dung và thay đổi mới của thư viện Cải Chánh</description><language>vi</language>{_it}</channel></rss>')

# 5. Doc theo sach Kinh Thanh
_BK = [("Sáng Thế Ký","Genesis"),("Xuất Ê-díp-tô Ký","Exodus"),("Lê-vi Ký","Leviticus"),("Dân Số Ký","Numbers"),("Phục Truyền Luật Lệ Ký","Deuteronomy"),("Giô-suê","Joshua"),("Các Quan Xét","Judges"),("Ru-tơ","Ruth"),("1 Sa-mu-ên",""),("2 Sa-mu-ên",""),("1 Các Vua",""),("2 Các Vua",""),("1 Sử Ký",""),("2 Sử Ký",""),("Ê-xơ-ra","Ezra"),("Nê-hê-mi","Nehemiah"),("Ê-xơ-tê","Esther"),("Gióp","Job"),("Thi Thiên","Psalm"),("Châm Ngôn","Proverbs"),("Truyền Đạo","Ecclesiastes"),("Nhã Ca","Song of Solomon"),("Ê-sai","Isaiah"),("Giê-rê-mi","Jeremiah"),("Ca Thương","Lamentations"),("Ê-xê-chi-ên","Ezekiel"),("Đa-ni-ên","Daniel"),("Ô-sê","Hosea"),("Giô-ên","Joel"),("A-mốt","Amos"),("Áp-đia","Obadiah"),("Giô-na","Jonah"),("Mi-chê","Micah"),("Na-hum","Nahum"),("Ha-ba-cúc","Habakkuk"),("Sô-phô-ni","Zephaniah"),("Ha-ghê","Haggai"),("Xa-cha-ri","Zechariah"),("Ma-la-chi","Malachi"),
 ("Ma-thi-ơ","Matthew"),("Mác","Mark"),("Lu-ca","Luke"),("Giăng","John"),("Công Vụ","Acts"),("Rô-ma","Romans"),("1 Cô-rinh-tô",""),("2 Cô-rinh-tô",""),("Ga-la-ti","Galatians"),("Ê-phê-sô","Ephesians"),("Phi-líp","Philippians"),("Cô-lô-se","Colossians"),("1 Tê-sa-lô-ni-ca",""),("2 Tê-sa-lô-ni-ca",""),("1 Ti-mô-thê",""),("2 Ti-mô-thê",""),("Tít","Titus"),("Phi-lê-môn","Philemon"),("Hê-bơ-rơ","Hebrews"),("Gia-cơ","James"),("1 Phi-e-rơ",""),("2 Phi-e-rơ",""),("1 Giăng",""),("2 Giăng",""),("3 Giăng",""),("Giu-đe","Jude"),("Khải Huyền","Book of Revelation")]
_AMB = {"Mark", "Luke", "John", "Matthew", "James", "Jude", "Jonah", "Job", "Ruth", "Esther", "Joshua", "Daniel", "Jeremiah", "Titus", "Ezra", "Amos", "Joel"}
_ALIAS = {"Phục Truyền Luật Lệ Ký": ["Phục-truyền", "Phục truyền"], "Xuất Ê-díp-tô Ký": ["Xuất Ê-díp-tô"], "Thi Thiên": ["Thi-thiên"]}
def _bible_hits(vi, en):
    _h = []
    for _sl, (_v, _q, _qs) in _SP.items():
        if any((_v or "").startswith(x + " ") or _v == x for x in [vi] + _ALIAS.get(vi, [])):
            _h.append(("Bài giảng", (_VT.get(_sl) or [_sl])[0], f"/bai-giang/{_sl}.html", _v))
    if en:
        _pat = (r"(Gospel (of|according to) |Epistles? (of |to )?(St\.? |Saint )?|\bon (the )?(Book of )?(the )?(Epistle )?(of |to )?)" + en + r"\b") if en in _AMB else (r"\b" + en + r"\b")
        for b in _pub9:
            if _r9.search(_pat, b.get("orig", "") or ""):
                _h.append(("Bản dịch", b.get("title", ""), "/ban-dich/" + _o9.path.splitext(b["file"])[0] + ".html", b.get("author", "")))
    if len(vi) >= 6 and not vi[0].isdigit():
        for b in _pub9:
            _u = "/ban-dich/" + _o9.path.splitext(b["file"])[0] + ".html"
            if _r9.search(r"\b" + _r9.escape(vi) + r"\b", b.get("title", "")) and not any(h[2] == _u for h in _h):
                _h.append(("Bản dịch", b.get("title", ""), _u, b.get("author", "")))
    return _h
_ot, _nt, _got = "", "", 0
for _i, (_vi, _en) in enumerate(_BK):
    _hs = _bible_hits(_vi, _en)
    _got += 1 if _hs else 0
    _body = "".join(f'<li>{k}: <a href="{E(u)}">{E(t)}</a> <span class="stt">({E(x)})</span></li>' for k, t, u, x in _hs) if _hs else '<li class="stt">Chưa có tài liệu. Sẽ bổ sung dần.</li>'
    _blk = f'<section class="nc"><h2>{E(_vi)}</h2><ul>{_body}</ul></section>'
    if _i < 39: _ot += _blk
    else: _nt += _blk
_b5 = _NC + f'<h1>Đọc theo sách Kinh Thánh</h1><p>Tìm bài giảng và bản dịch liên quan đến từng sách Kinh Thánh. Hiện có tài liệu cho <b>{_got}</b> trong 66 sách. Danh sách sẽ đầy dần khi thư viện thêm bài.</p><h2>Cựu Ước</h2>{_ot}<h2>Tân Ước</h2>{_nt}{_DRAFT}'
open("kinh-thanh.html", "w", encoding="utf-8").write(page("Đọc theo sách Kinh Thánh | Reformed Vietnam", "Tìm bài giảng và sách Cải Chánh tiếng Việt theo từng sách Kinh Thánh.", "kinh-thanh.html", _b5)); urls.append("kinh-thanh.html")

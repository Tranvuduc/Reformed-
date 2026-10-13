# Executed after nang_cap3.py: tai-sach.html (+ tai-sach.json). Client script: /tai-sach.js (hand-written, not generated).
_ix4 = {b["file"][:-4]: b for b in _idx3}
_L4 = []
for _f in sorted(_o3.listdir("txt")):
    if not _f.endswith(".txt"): continue
    _s = _f[:-4]; _txt = open("txt/" + _f, encoding="utf-8").read()
    if _s in _ix4 and not _ix4[_s].get("hold"):
        _b = _ix4[_s]; _t, _a, _o = _b.get("title", _s), _b.get("author", ""), _b.get("orig", "")
        _k = "goc" if _a == "David" else "dich"
    else:
        _ls = [l.strip() for l in _txt.split("\n", 12)[:10] if l.strip()]
        _t = _ls[0].title() if _ls else _s
        _a = next((l.split(" · ")[0] for l in _ls[1:] if " · " in l and len(l) < 200), "")
        if not _a: _a = _s.split("-")[0].title()
        _o = ""; _k = "dich"
    _L4.append({"s": _s, "t": _t, "a": _a, "o": _o, "k": _k, "n": len(_txt)})
_L4.sort(key=lambda x: (x["a"], x["t"]))
open("tai-sach.json", "w", encoding="utf-8").write(_j3.dumps(_L4, ensure_ascii=False, separators=(",", ":")))
_b4x = _NC3 + f'''<h1>Tải sách về máy</h1>
<p>Tải sách của thư viện về điện thoại hoặc máy tính để đọc khi không có mạng. Mỗi sách là một tệp <b>EPUB</b> có bìa, mục lục theo chương, trang bản quyền và ghi chú bản dịch. Mở bằng Google Play Sách, Moon+ Reader, Apple Books, Kobo hoặc bất kỳ ứng dụng đọc EPUB nào. Tệp được tạo ngay trên thiết bị của bạn, không gửi dữ liệu đi đâu.</p>
<section class="nc"><h2>Tải tất cả ({len(_L4)} sách)</h2><p>Chia thành vài tệp ZIP để điện thoại không bị quá tải. Bấm từng phần; mỗi phần mất vài phút. Hãy giữ màn hình mở cho đến khi xong.</p><p id="parts"></p></section>
<section class="nc"><h2>Hoặc chọn từng sách</h2><div class="sel"><input id="q" type="search" placeholder="Tìm theo tên sách hoặc tác giả" aria-label="Tìm"></div>
<p><button type="button" class="btn s" id="all">Chọn tất cả</button> <button type="button" class="btn s" id="none">Bỏ chọn</button> <button type="button" class="btn" id="dl">Tải các sách đã chọn (ZIP)</button> <span class="stt" id="cnt"></span></p>
<progress id="pg" max="1" value="0" hidden style="width:100%"></progress><p class="m" id="st" role="status"></p><ul class="rs" id="ls" style="list-style:none;padding:0"></ul></section>
<p class="m">Sách thuộc phạm vi công cộng hoặc do chúng tôi dịch/soạn. Bản dịch do AI hỗ trợ và chưa được mục sư duyệt; mỗi sách có ghi chú này ở trang bản quyền. Sách tiếng Việt của nơi khác còn bản quyền không được đưa lên đây. Cần trình duyệt Chrome, Edge, Safari hoặc Firefox bản mới.</p>
<script src="/tai-sach.js" defer></script>'''
open("tai-sach.html", "w", encoding="utf-8").write(page("Tải sách về máy (EPUB) | Reformed Vietnam", "Tải về điện thoại hoặc máy tính các sách Cải Chánh tiếng Việt dưới dạng EPUB có bìa, mục lục và ghi chú bản dịch, đọc offline miễn phí.", "tai-sach.html", _b4x)); urls.append("tai-sach.html")

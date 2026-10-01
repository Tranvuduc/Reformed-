# Executed from build-pages.py (uses: page, E, urls, books, mg, desc). Builds lo-trinh.html
T = {}
for _a in books["authors"]:
    for _b in _a["books"]:
        T[_a["id"] + "/" + _b[0]] = (_a["name"], _b[1])
X = {x["id"]: x for x in books["extra"]}
M = {x["id"]: x for x in mg["vn"]}
VI = books["vi"]

def item(kind, key, why):
    if kind == "c":
        nm, en = T.get(key, ("", key))
        title = VI.get(key) or (desc.get(key, ["", ""])[1][:0]) or en
        vt = VI.get(key)
        t = f'{E(vt)} <small>({E(en)})</small>' if vt else E(en)
        href = f"/reader.html?id={key}"
        tag = "EN · có nút 🌐 dịch sang tiếng Việt"
        who = nm
    elif kind == "x":
        x = X[key]; t = E(x["vi"]["t"]); who = x["a"]
        if x.get("url"): href = x["url"]; tag = "Tiếng Việt · trang ngoài"
        else: href = "/?q=" + key; tag = "Mở trong thư viện"
    else:
        x = M[key]; t = E(x["vi"]["t"]); who = x["a"]; href = x["url"]
        tag = "Tiếng Việt · trang ngoài" if x.get("au") not in ("dg", "lig") else "Miễn phí · trang ngoài (EN→VI tên)"
        if x.get("au") in ("dg", "lig"): tag = "Sách tiếng Anh miễn phí · bấm 🌐 trong trình đọc nếu mở trong thư viện"
    ext = ' target="_blank" rel="noopener"' if href.startswith("http") else ""
    return (f'<li><label class="ck"><input type="checkbox" data-k="{E(key)}"></label>'
            f'<div><a href="{E(href)}"{ext}><b>{t}</b></a> <small>· {E(who)} · {tag}</small><br><span class="why">{E(why)}</span></div></li>')

STAGES = [
 ("Giai đoạn 0 · Tuần 1–2 · Nền tảng cho người mới", "Nếu bạn mới tin Chúa hoặc mới nghe về thần học Cải Chánh, hãy bắt đầu ở đây. Mỗi ngày 15–20 phút.", [
   ("x","vn-apostles","Bản tín điều ngắn nhất của đức tin Cơ Đốc. Đọc chậm, đối chiếu với Kinh Thánh."),
   ("m","9m-what-is-the-gospel-t","Tin Lành là gì, nói ngắn gọn và rõ ràng (tiếng Việt)."),
   ("m","9m-who-is-jesus-chua-je","Chúa Jesus là ai? Cơ sở của mọi giáo lý khác (tiếng Việt)."),
   ("m","tp-ba-thanh-phan-thiet-yeu-de-doc-kinh-than","Cách đọc Kinh Thánh mỗi ngày (tiếng Việt)."),
   ("c","spurgeon/grace","Spurgeon giải thích ân điển cho người tìm hiểu; ấm áp, dễ đọc."),
   ("c","bonar/peace","Làm sao có bình an với Đức Chúa Trời, giải thích Tin Lành rõ ràng.")]),
 ("Giai đoạn 1 · Tuần 3–10 · Giáo lý căn bản", "Học theo dạng hỏi–đáp: mỗi tuần 3–5 câu, đọc phân đoạn Kinh Thánh kèm theo.", [
   ("x","vn-newcity","Giáo lý vấn đáp hiện đại 52 câu, thích hợp cho gia đình và nhóm nhỏ."),
   ("x","vn-wsc","Giáo lý Vắn tắt Westminster: 107 câu hỏi, cô đọng nhất của truyền thống Cải Chánh."),
   ("x","vn-heidelberg","Giáo lý Heidelberg: ấm áp, cá nhân, chia theo ba phần: tội, cứu chuộc, biết ơn (Anh–Việt)."),
   ("m","lig-what-is-faith","Sproul: đức tin là gì (sách ngắn, tiếng Anh)."),
   ("m","lig-what-is-the-trinity","Sproul: giáo lý Ba Ngôi (sách ngắn, tiếng Anh)."),
   ("m","tp-than-hoc-de-hieu-bitesize-theology","Thần học dễ hiểu (tiếng Việt)."),
   ("m","lig-what-does-it-mean-to-be-born-again","Sproul về sự tái sanh (sách ngắn, tiếng Anh)."),
   ("x","vn-nicene","Tín điều Nicene: giáo lý về Ba Ngôi và thân vị Đấng Christ.")]),
 ("Giai đoạn 2 · Tháng 3–5 · Đời sống Cơ Đốc", "Sách thuộc linh để nuôi đức tin: mỗi tuần một chương, ghi lại một điều áp dụng.", [
   ("c","bunyan/pilgrim","Hành trình của người hành hương: truyện ngụ ngôn về đời sống đức tin."),
   ("c","ryle/holiness","Ryle viết thẳng thắn về sự nên thánh và cuộc chiến thuộc linh."),
   ("c","watson/contentment","Học sự bằng lòng trong mọi hoàn cảnh."),
   ("c","flavel/lovely","Chiêm ngưỡng vẻ đẹp của Đấng Christ."),
   ("c","calvin/chr_life","Calvin về sự từ bỏ mình và vác thập tự."),
   ("c","calvin/prayer","Calvin về sự cầu nguyện."),
   ("m","dg-god-is-the-gospel","Piper: chính Đức Chúa Trời là món quà lớn nhất của Tin Lành (tiếng Anh)."),
   ("c","owen/mort","Owen về việc chiến đấu với tội lỗi (khó hơn, đọc sau cùng trong giai đoạn này).")]),
 ("Giai đoạn 3 · Tháng 5–7 · Hội Thánh, báp-têm và Tiệc Thánh", "Học sống trong cộng đồng đức tin. Rất hợp để học cùng nhóm.", [
   ("m","9m-nine-marks-of-a-heal","Chín dấu hiệu của một Hội thánh vững mạnh (tiếng Việt)."),
   ("m","9m-church-membership-va","Tư cách thành viên Hội thánh (tiếng Việt)."),
   ("m","9m-expositional-preachi","Vì sao giảng giải Kinh Thánh là trung tâm (tiếng Việt)."),
   ("m","lig-what-is-the-church","Sproul: Hội Thánh là gì (tiếng Anh)."),
   ("m","lig-what-is-baptism","Sproul: báp-têm (tiếng Anh)."),
   ("m","lig-what-is-the-lords-supper","Sproul: Tiệc Thánh (tiếng Anh)."),
   ("c","baxter/pastor","Dành cho người hầu việc Chúa: chăm sóc từng con chiên.")]),
 ("Giai đoạn 4 · Tháng 8–12 · Giáo lý Cải Chánh sâu hơn", "Bây giờ đọc các tuyên xưng đức tin và những lập luận kinh điển.", [
   ("x","westminster","Tuyên xưng đức tin Westminster (1646): sách tham khảo chính."),
   ("x","vn-dordt","Giáo luật Dordt (1619): nguồn gốc của năm điểm Calvin, bằng tiếng Việt."),
   ("x","vn-belgic","Xưng nhận đức tin Belgic (tiếng Việt)."),
   ("x","vn-baptist1689","Giáo lý Baptist 1689 (tiếng Việt), dành cho truyền thống Báp-tít Cải Chánh."),
   ("x","vn-philadelphia","Tuyên xưng Philadelphia 1742 (tiếng Việt)."),
   ("c","berkhof/summary","Tóm lược giáo lý Cải Chánh của Berkhof; đọc cạnh các tuyên xưng."),
   ("c","owen/deathofdeath","Owen về sự chuộc tội (khó)."),
   ("c","edwards/will","Edwards về ý chí con người (khó)."),
   ("x","bondage-of-the-will","Luther về ý chí bị trói buộc (khó).")]),
 ("Giai đoạn 5 · Năm thứ hai · Thần học hệ thống và kinh điển", "Đọc từng phần, không cần hết cuốn. Dùng mục lục và ô tìm kiếm trong trình đọc.", [
   ("c","calvin/institutes","Cơ Đốc Giáo Yếu Lý: kinh điển nền tảng của thần học Cải Chánh."),
   ("c","berkhof/systematictheology","Thần học hệ thống Berkhof: sách giáo khoa tiêu chuẩn."),
   ("c","hodge/theology1","Thần học hệ thống Hodge, tập 1."),
   ("c","kuyper/lecture","Kuyper: thuyết Calvin như một lối sống."),
   ("c","edwards/affections","Edwards: phân biệt cảm xúc thuộc linh thật và giả."),
   ("c","owen/communion","Owen về sự thông công với Cha, Con và Thánh Linh."),
   ("c","owen/just","Owen về sự xưng công chính bởi đức tin.")]),
 ("Song song · Lịch sử Hội Thánh và Cải Chánh", "Đọc xen kẽ bất cứ lúc nào để hiểu bối cảnh.", [
   ("m","tp-thien-tai-cua-geneva","Tiên Phong: Calvin (tiếng Việt)."),
   ("m","tp-ngon-nen-cua-nuoc-anh","Tiên Phong: Tyndale (tiếng Việt)."),
   ("m","tp-ngoi-sao-mai-cua-phong-trao-cai-chanh","Tiên Phong: Wycliffe (tiếng Việt)."),
   ("m","dg-martin-luther","Piper về Luther (tiếng Anh)."),
   ("m","dg-portrait-of-calvin--2","Piper về Calvin (tiếng Anh)."),
   ("c","foxe/martyrs","Sách các thánh tử đạo."),
   ("c","knox/history_reformation","Cải Chánh ở Scotland do chính Knox kể.")]),
]

TRACKS = [
 ("Năm Sola của Cải Chánh", "Chỉ bởi Kinh Thánh, chỉ bởi ân điển, chỉ bởi đức tin, chỉ trong Đấng Christ, chỉ vì vinh hiển Đức Chúa Trời.", [("x","vn-cambridge","Tuyên ngôn Cambridge (tiếng Việt)"),("x","vn-wsc","Giáo lý Vắn tắt Westminster")]),
 ("Giáo lý ân điển (năm điểm Calvin)", "Đọc Giáo luật Dordt trước, rồi các sách giải thích. Hãy luôn đối chiếu với Kinh Thánh.", [("x","vn-dordt","Giáo luật Dordt"),("c","owen/deathofdeath","Owen"),("c","boettner/predest","Boettner")]),
 ("Giao ước và Kinh Thánh", "Xem Tuyên xưng Westminster (chương về giao ước) và Calvin phần Cựu–Tân Ước.", [("x","westminster","Westminster"),("c","calvin/institutes","Calvin")]),
 ("Cầu nguyện và đời sống thuộc linh", "Calvin, Knox, Watson và sách nói.", [("c","calvin/prayer","Calvin"),("c","watson/prayer","Watson: Kinh Lạy Cha"),("c","knox/prayer","Knox"),("m","9m-prayer-su-cau-nguyen","9Marks: Sự cầu nguyện")]),
 ("Chức vụ và Hội Thánh", "Dành cho mục sư, trưởng lão, người hầu việc.", [("c","baxter/pastor","Baxter"),("m","9m-church-elders","Trưởng lão của Hội thánh"),("m","9m-church-discipline-ky","Kỷ luật Hội thánh")]),
]

def sect(i, h, intro, items):
    lis = "".join(item(k, key, why) for k, key, why in items)
    return f'<section><h2>{E(h)}</h2><p class="m">{E(intro)}</p><ul class="plan">{lis}</ul></section>'

def tracks():
    out = ""
    for h, intro, its in TRACKS:
        ls = []
        for k, key, label in its:
            if k == "c":
                href = f"/reader.html?id={key}"; ext = ""
            elif k == "x":
                x = X[key]; href = x.get("url") or "/?q=" + key; ext = ' target="_blank" rel="noopener"' if href.startswith("http") else ""
            else:
                href = M[key]["url"]; ext = ' target="_blank" rel="noopener"'
            ls.append(f'<a href="{E(href)}"{ext}>{E(label)}</a>')
        out += f'<details><summary>{E(h)}</summary><p>{E(intro)}</p><p>{" · ".join(ls)}</p></details>'
    return out

body = f'''<h1>Lộ trình đọc sách Cải Chánh cho người mới</h1>
<p class="m">Một con đường từ dễ đến khó, dùng sách miễn phí trong thư viện này. Bạn không cần đọc hết: hãy đi từng giai đoạn, đánh dấu ô bên trái khi đọc xong (lưu trên thiết bị của bạn).</p>
<div class="note"><b>Nên nhớ:</b> (1) Sách tiếng Anh trong thư viện có nút 🌐 dịch sang tiếng Việt bằng máy, có thể sai sót. (2) Với bản dịch máy, luôn đối chiếu Kinh Thánh và hỏi mục sư hoặc người hướng dẫn. (3) Thần học Cải Chánh có nhiều nhánh (Trưởng Lão, Báp-tít Cải Chánh, Anh giáo...) nên hãy đọc cùng một Hội Thánh nếu có thể.</div>
<div class="pace"><b>Nhịp đọc gợi ý:</b> 15–20 phút mỗi ngày; mỗi tuần một chương hoặc 3–5 câu giáo lý; mỗi tháng ghi 3 dòng điều học được. Cứ 2–3 tháng nghỉ một tuần để ôn lại.</div>
<p><span id="pg" class="m"></span></p>
{"".join(sect(i, *s) for i, s in enumerate(STAGES))}
<h2>Học theo chủ đề</h2>
{tracks()}
<h2>Nghe thay vì đọc</h2>
<p>Xem trang <a href="/sach-noi.html">Sách nói và bài giảng miễn phí</a>: LibriVox, CCEL MP3, Ligonier, Desiring God.</p>
<h2>Cần thêm sách tiếng Việt?</h2>
<p>Mở <a href="/tieng-viet.html">thư viện tiếng Việt</a>, hoặc gửi đường link sách Việt hợp pháp về reformedvn@gmail.com để chúng tôi thêm vào.</p>
<style>.plan{{list-style:none;padding:0}}.plan li{{display:flex;gap:10px;margin:.7em 0}}.ck input{{width:20px;height:20px;margin-top:4px}}.why{{color:#4b4338;font-size:15px}}.note,.pace{{background:#fff8ec;border:1px solid #e3d3b6;border-radius:10px;padding:10px 14px;margin:14px 0;font:15px/1.5 system-ui,sans-serif}}details{{margin:.5em 0;padding:8px 12px;background:#fffdf7;border:1px solid #e3d3b6;border-radius:8px}}summary{{cursor:pointer;font-weight:600}}</style>
<script>(function(){{var K="rv.plan",s={{}};try{{s=JSON.parse(localStorage.getItem(K)||"{{}}")}}catch(e){{}}
var bx=document.querySelectorAll("input[data-k]");function upd(){{var d=0;bx.forEach(function(b){{if(b.checked)d++}});document.getElementById("pg").textContent="Đã đọc "+d+" / "+bx.length}}
bx.forEach(function(b){{b.checked=!!s[b.dataset.k];b.onchange=function(){{s[b.dataset.k]=b.checked?1:0;try{{localStorage.setItem(K,JSON.stringify(s))}}catch(e){{}}upd()}}}});upd()}})()</script>'''
open("lo-trinh.html", "w", encoding="utf-8").write(page("Lộ trình đọc sách Cải Chánh cho người mới | Reformed Vietnam",
    "Lộ trình đọc sách thần học Cải Chánh miễn phí cho người mới: từ giáo lý căn bản, đời sống Cơ Đốc, Hội Thánh đến Calvin, Owen và Edwards. Có liên kết sách.", "lo-trinh.html", body))
urls.append("lo-trinh.html")

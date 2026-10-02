# Executed from build-pages.py (after vi_books.py). Builds moi-tin-chua.html: a 30-day path for new believers.
import re as _r2
def _anch(slug, pat):
    try: h = open(f"ban-dich/{slug}.html", encoding="utf-8").read()
    except OSError: return None
    m = _r2.search(r'<h2 id="(c\d+)">([^<]*%s[^<]*)</h2>' % pat, h)
    return f"/ban-dich/{slug}.html#{m.group(1)}" if m else (f"/ban-dich/{slug}.html" if True else None)
def _bk(slug, label, pat=None):
    u = _anch(slug, pat) if pat else f"/ban-dich/{slug}.html"
    return (u, label) if u and _o.path.exists(f"ban-dich/{slug}.html") else None
_B = "bonar-followlamb"; _S = "spurgeon-puritan-catechism"; _C = "calvin-chr-life"
_D = [
 ("Tin Lành là gì?", "1 Cô-rinh-tô 15:1-4", _bk(_B, "Bonar, Theo Chiên Con, mở đầu", "THEO")),
 ("Chúa Giê-xu là ai?", "Giăng 1:1-18", _bk(_S, "Giáo lý Thanh giáo, câu 19-21")),
 ("Tội lỗi là gì?", "Rô-ma 3:9-26", _bk(_S, "Giáo lý Thanh giáo, câu 14-18")),
 ("Ân điển là gì?", "Ê-phê-sô 2:1-10", _bk(_B, "Bonar, chương I: hãy mạnh mẽ trong ân điển", "I\\. HÃY MẠNH")),
 ("Ăn năn và đức tin", "Mác 1:14-15; Công Vụ 20:21", _bk(_S, "Giáo lý Thanh giáo, câu 67-69")),
 ("Được xưng công bình", "Rô-ma 5:1-11", _bk(_S, "Giáo lý Thanh giáo, câu 31")),
 ("Làm con của Đức Chúa Trời", "Rô-ma 8:14-17; 1 Giăng 3:1-3", _bk(_S, "Giáo lý Thanh giáo, câu 32")),
 ("Đức Thánh Linh", "Giăng 14:15-27", _bk(_S, "Giáo lý Thanh giáo, câu 28-29")),
 ("Kinh Thánh là gì?", "2 Ti-mô-thê 3:14-17", _bk(_S, "Giáo lý Thanh giáo, câu 2-3")),
 ("Cách đọc Kinh Thánh mỗi ngày", "Thi Thiên 119:9-16; Công Vụ 17:10-12", _bk(_B, "Bonar, chương VI: nghiên cứu Kinh Thánh", "VI\\. HÃY NGHIÊN")),
 ("Cầu nguyện là gì?", "Ma-thi-ơ 6:5-8", ("/doc/do-you-pray.html", "Ryle, Bạn có cầu nguyện không?")),
 ("Lời Chúa dạy cầu nguyện", "Ma-thi-ơ 6:9-13", _bk("calvin-prayer", "Calvin, Về sự cầu nguyện")),
 ("Biết mình đã được cứu", "1 Giăng 5:11-13", _bk(_B, "Bonar, chương IV: hãy thành thật với chính mình", "IV\\. HÃY THÀNH")),
 ("Chiến đấu với tội lỗi", "Rô-ma 6:1-14", _bk(_B, "Bonar, chương IX: canh chừng Sa-tan", "IX\\. HÃY CANH")),
 ("Nên thánh mỗi ngày", "Phi-líp 2:12-13", _bk(_S, "Giáo lý Thanh giáo, câu 33")),
 ("Hội Thánh là gì?", "1 Phi-e-rơ 2:4-10", _bk(_B, "Bonar, chương V: kết thân với dân sự Chúa", "V\\. HÃY KẾT")),
 ("Báp-têm", "Ma-thi-ơ 28:18-20; Rô-ma 6:3-4", _bk(_S, "Giáo lý Thanh giáo, câu 75-80 (lập trường Báp-tít)")),
 ("Tiệc Thánh", "1 Cô-rinh-tô 11:23-28", _bk(_S, "Giáo lý Thanh giáo, câu 81-83")),
 ("Nhóm lại thờ phượng", "Hê-bơ-rơ 10:24-25", None),
 ("Hiếu thảo với cha mẹ", "Ê-phê-sô 6:1-4", _bk("sach-04-hieu-thao-theo-kinh-thanh", "David, Hiếu thảo theo Kinh Thánh")),
 ("Gia đình còn thờ cúng tổ tiên", "Xuất Ê-díp-tô Ký 20:3-6; Rô-ma 13:7", _bk("sach-05-nguoi-moi-tin-trong-gia-dinh-tho-cung", "David, Người mới tin trong nhà có bàn thờ")),
 ("Khi đau khổ và bệnh tật", "Rô-ma 8:28-39", _bk("sach-02-giop-giua-con-bao", "David, Gióp giữa cơn bão")),
 ("Sợ hãi, lo lắng và bình an", "Phi-líp 4:6-7; Giăng 14:27", _bk("sach-09-so-hai-va-binh-an-duc-tin-so-voi-bua-chu", "David, Sợ hãi và bình an")),
 ("Tiền bạc và Tin Lành thịnh vượng", "Ma-thi-ơ 6:19-24; 1 Ti-mô-thê 6:6-10", _bk("sach-01-chua-khong-hua-giau-co", "David, Chúa không hứa giàu có")),
 ("Làm chứng cho người thân", "Ma-thi-ơ 5:13-16; 1 Phi-e-rơ 3:15", ("/doc/compel-them-to-come-in.html", "Spurgeon, Hãy ép người ta phải vào")),
 ("Phục vụ trong Hội Thánh", "Rô-ma 12:3-8", None),
 ("Làm việc cho Chúa", "Cô-lô-se 3:23-24", _bk("sach-21-kinh-thanh-va-nghe-nghiep", "David, Kinh Thánh và nghề nghiệp")),
 ("Sống cho vinh hiển Đức Chúa Trời", "1 Cô-rinh-tô 10:31", _bk(_S, "Giáo lý Thanh giáo, câu 1")),
 ("Chúa gìn giữ đến cùng", "Giăng 10:27-30; Phi-líp 1:6", _bk(_C, "Calvin, Đời sống Cơ Đốc")),
 ("Bước tiếp theo", "Hê-bơ-rơ 13:7, 17", ("/lo-trinh.html", "Lộ trình đọc đầy đủ")),
]
_W = [("Tuần 1: Phúc Âm", 0, 8), ("Tuần 2: Kinh Thánh, cầu nguyện và đời sống mới", 8, 15), ("Tuần 3: Hội Thánh và gia đình", 15, 22), ("Tuần 4: Sống như môn đồ", 22, 30)]
def _day(i, t, s_, r):
    return (f'<li class="dy" data-d="{i+1}"><label><input type="checkbox" data-d="{i+1}"> <b>Ngày {i+1}: {E(t)}</b></label><br><span class="m">Kinh Thánh: {E(s_)}</span>'
            + (f'<br><a href="{E(r[0])}">Đọc thêm: {E(r[1])}</a>' if r else "") + '</li>')
_rows = "".join(f'<section class="wk"><h2>{E(n)}</h2><ol class="dp" start="{a_+1}">' + "".join(_day(i, *_D[i]) for i in range(a_, b_)) + '</ol></section>' for n, a_, b_ in _W)
_js = """<script>(function(){var K="rv.mt",d={};try{d=JSON.parse(localStorage.getItem(K)||"{}")}catch(e){}
var bx=document.querySelectorAll('input[data-d]'),bar=document.getElementById("pb"),tx=document.getElementById("pt"),nx=document.getElementById("nx");
function upd(){var n=0,first=0;bx.forEach(function(c){var k=c.dataset.d;c.checked=!!d[k];c.closest("li").classList.toggle("ok",c.checked);if(c.checked)n++;else if(!first)first=+k});
bar.style.width=Math.round(n/bx.length*100)+"%";tx.textContent=n+" / "+bx.length+" ngày";
if(first){nx.hidden=false;nx.textContent="Tiếp tục: Ngày "+first;nx.href="#d"+first}else{nx.hidden=true;tx.textContent+=" · Chúc mừng bạn đã hoàn thành!"}}
bx.forEach(function(c){c.closest("li").id="d"+c.dataset.d;c.addEventListener("change",function(){if(c.checked)d[c.dataset.d]=1;else delete d[c.dataset.d];try{localStorage.setItem(K,JSON.stringify(d))}catch(e){}upd()})});upd()})()</script>"""
_body = ('<style>.dp li{margin:0 0 1em;line-height:1.5}.dp{padding-left:1.4em}.dp li.ok b{opacity:.55;text-decoration:line-through}.wk h2{margin:1.6em 0 .6em;font-size:1.15rem}.pbar{height:8px;border-radius:8px;background:#8882;overflow:hidden;margin:6px 0}.pbar i{display:block;height:100%;width:0;background:var(--accent,#9a3412)}.pg{position:sticky;top:0;background:var(--bg,#fff);padding:8px 0;z-index:2}.rf{padding:.6em .9em;border-left:3px solid #9a3412;background:#8881;border-radius:6px}input[type=checkbox]{width:20px;height:20px;vertical-align:-4px}.dr{padding:.6em .9em;border-radius:8px;background:#d9a41e22}</style>'
 '<h1>Tôi mới tin Chúa: 30 ngày đầu tiên</h1>'
 '<p>Mỗi ngày chỉ khoảng 10 phút: đọc đoạn Kinh Thánh, rồi đọc phần gợi ý (nếu có), và cầu nguyện ngắn. Bạn không cần hiểu hết. Hãy đi chậm và hỏi mục sư hoặc người hướng dẫn của bạn khi có thắc mắc.</p>'
 '<p class="dr">Phần "Đọc thêm" gồm nhiều bản dịch và sách do AI hỗ trợ, <b>chưa được mục sư duyệt giáo lý</b>. Kinh Thánh là thẩm quyền tối hậu. Hãy đọc Kinh Thánh trong bản bạn quen dùng, và đối chiếu mọi điều bạn đọc với Kinh Thánh. Thư viện này hỗ trợ việc học, nhưng không thay thế Hội Thánh địa phương.</p>'
 '<div class="pg"><div class="pbar"><i id="pb"></i></div><span id="pt"></span> <a class="btn" id="nx" href="#" hidden></a></div>'
 '<p class="rf"><b>Mỗi ngày, hãy tự hỏi:</b> Đoạn này nói gì về Đức Chúa Trời? Tôi sẽ vâng theo điều gì hôm nay? Tôi cầu nguyện cho ai và điều gì?</p>'
 f'{_rows}{_js}'
 '<p><a class="btn" href="/">Về thư viện</a> · <a class="btn" href="/lo-trinh.html">Lộ trình đọc đầy đủ</a></p>')
open("moi-tin-chua.html", "w", encoding="utf-8").write(page("Tôi mới tin Chúa: 30 ngày đầu tiên | Reformed Vietnam", "Lộ trình 30 ngày cho người mới tin Chúa: mỗi ngày một đoạn Kinh Thánh và một bài đọc ngắn. Miễn phí.", "moi-tin-chua.html", _body))
urls.append("moi-tin-chua.html")

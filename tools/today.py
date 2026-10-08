# Executed from build-pages.py. Builds hom-nay.html and feed.xml
import datetime as _dt
_X = {x["id"]: x for x in books["extra"]}
_hd = _X["vn-heidelberg"]["url"]; _wsc = _X["vn-wsc"]["url"]
_body = f'''<h1>Hôm nay</h1>
<p class="m" id="dt"></p>
<div class="card" id="me"></div>
<div class="card"><h2>Giáo lý hôm nay</h2>
<p><b>Giáo lý Vắn tắt Westminster:</b> câu hỏi số <b id="wq"></b>/107. Hãy đọc câu hỏi, câu trả lời và các câu Kinh Thánh kèm theo. <a href="{E(_wsc)}" target="_blank" rel="noopener">Mở bản tiếng Việt</a></p>
<p><b>Giáo lý Heidelberg:</b> tuần này là <b>Ngày Chúa nhật thứ <span id="hd"></span></b> (giáo lý chia làm 52 phần, mỗi tuần một phần). <a href="{E(_hd)}" target="_blank" rel="noopener">Mở bản Anh–Việt</a></p></div>
<div class="card" id="cont" hidden><h2>Đọc tiếp nơi bạn dừng lại</h2><p id="contp"></p></div>
<div class="card"><h2>Chia sẻ</h2><p><a class="btn" id="fb" target="_blank" rel="noopener" href="https://www.facebook.com/sharer/sharer.php?u={SITE}/hom-nay.html">Chia sẻ lên Facebook</a> <a class="btn s" href="/feed.xml">RSS</a></p>
<p class="m">Bản dịch tiếng Việt trong trình đọc là bản dịch máy nên có thể còn sai sót. Hãy đối chiếu với Kinh Thánh.</p></div>
<style>.card{{background:var(--card,#fffdf7);border:1px solid var(--line,#e3d3b6);border-radius:12px;padding:6px 16px 10px;margin:14px 0}}.card h2{{font-size:1.15rem;margin:.6em 0 .3em}}</style>
<script>(function(){{var M=["January","February","March","April","May","June","July","August","September","October","November","December"],VM=["tháng 1","tháng 2","tháng 3","tháng 4","tháng 5","tháng 6","tháng 7","tháng 8","tháng 9","tháng 10","tháng 11","tháng 12"];
var d=new Date(),doy=Math.floor((d-new Date(d.getFullYear(),0,0))/864e5);
document.getElementById("dt").textContent="Ngày "+d.getDate()+" "+VM[d.getMonth()]+" "+d.getFullYear();
var lbl=M[d.getMonth()]+" "+d.getDate(),base="/reader.html?id=spurgeon/morneve";
function lk(w){{return base+"&find="+encodeURIComponent(w+", "+lbl)}}
document.getElementById("me").innerHTML='<h2>Spurgeon: Sáng và Tối</h2><p>Bài suy niệm hôm nay (<i>Morning and Evening</i>, tiếng Anh, có nút 🌐 dịch sang tiếng Việt).</p><p><a class="btn" href="'+lk("Morning")+'">Buổi sáng</a> <a class="btn" href="'+lk("Evening")+'">Buổi tối</a> <a class="btn s" href="'+lk("Morning")+'&tr=1">Sáng (dịch tiếng Việt)</a> <a class="btn s" href="'+lk("Evening")+'&tr=1">Tối (dịch tiếng Việt)</a></p>';
document.getElementById("wq").textContent=(doy-1)%107+1;document.getElementById("hd").textContent=Math.min(52,Math.floor((doy-1)/7)+1);
try{{var p=JSON.parse(localStorage.getItem("rv.prog")||"{{}}"),best=null;for(var id in p)if(p[id].s==="reading"&&(!best||p[id].t>p[best].t))best=id;
if(best){{document.getElementById("cont").hidden=false;document.getElementById("contp").innerHTML='<a href="/reader.html?id='+best+'">'+best.split("/")[1]+' ('+p[best].p+'%)</a>'}}}}catch(e){{}}}})()</script>'''
open("hom-nay.html", "w", encoding="utf-8").write(page("Hôm nay: bài suy niệm và giáo lý mỗi ngày | Reformed Vietnam",
    "Bài suy niệm Spurgeon, câu hỏi giáo lý Westminster và Heidelberg mỗi ngày, miễn phí, có dịch tiếng Việt.", "hom-nay.html", _body))
urls.append("hom-nay.html")
# RSS: next 30 days of Morning and Evening
_M = ["January","February","March","April","May","June","July","August","September","October","November","December"]
_t0 = _dt.date.today(); _items = ""
for _i in range(30):
    _d = _t0 + _dt.timedelta(days=_i); _lbl = f"{_M[_d.month-1]} {_d.day}"
    for _w, _hr in (("Morning", 6), ("Evening", 18)):
        _u = f"{SITE}/reader.html?id=spurgeon/morneve&amp;find={_w}%2C%20{_lbl.replace(' ', '%20')}"
        _pub = _dt.datetime(_d.year, _d.month, _d.day, _hr, 0).strftime("%a, %d %b %Y %H:%M:%S +0700")
        _items += f"<item><title>Spurgeon · {_w}, {_lbl}</title><link>{_u}</link><guid isPermaLink=\"false\">morneve-{_d.isoformat()}-{_w}</guid><pubDate>{_pub}</pubDate><description>Bài suy niệm {'sáng' if _w=='Morning' else 'tối'} ngày {_d.day}/{_d.month} (Morning and Evening, Spurgeon).</description></item>"
open("feed.xml", "w", encoding="utf-8").write(f'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>Reformed Vietnam · Hôm nay</title><link>{SITE}/hom-nay.html</link><description>Suy niệm hằng ngày từ thư viện Cải Chánh</description><language>vi</language>{_items}</channel></rss>')

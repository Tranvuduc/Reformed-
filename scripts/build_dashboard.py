#!/usr/bin/env python3
"""Phase 5.1 — Reading dashboard (Bảng đọc của tôi).

Builds /bang-doc-sach.html: a personal reading-progress page that reads
ONLY this device/browser's localStorage — the same keys the Phase 3
reader already writes:

  * rv.prog        — {pid: {s: "reading"|"done", p: percent, t: time}}
  * rv.pos.vn/<slug> — last page index per book (resume)
  * rv.bm.vn/<slug>  — bookmarks [{p, g, s, t}]
  * rv.saved       — saved library book ids (homepage ☆)
  * rv-academy-done — completed Academy lessons (of 122)

Titles/authors come from /translations/index-lite.json and reader URLs
from /vi-books.json, fetched client-side. No accounts, no backend, no
data leaves the device — the page says so plainly, and offers a button
that wipes exactly these keys.

The page shell is static; all progress renders in the browser. If the
visitor has never read anything here, every section shows an honest
empty state instead of fake content.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from hub_page import (BASE, ROOT, head, header, footer, MINI_JS, share_row,
                      report_mailto, write_if_changed, check_links, sitemap_add)

CSS = """
      .stat-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:14px;margin:22px 0}
      .stat{border:1px solid var(--line);border-radius:12px;padding:16px;text-align:center;background:rgba(255,255,255,.35)}
      .stat b{display:block;font-family:"Playfair Display",serif;font-size:32px;color:var(--burgundy)}
      .stat span{font-size:13.5px;color:var(--ink-soft)}
      .bk-row{border-bottom:1px solid var(--line);padding:12px 2px}
      .bk-row h3{margin:0 0 2px;font-size:17px}
      .bk-row h3 a{color:var(--ink)}
      .bk-row .au{font-size:13.5px;color:var(--ink-soft)}
      .bar{height:8px;border-radius:4px;background:var(--line);overflow:hidden;margin:8px 0 4px;max-width:420px}
      .bar i{display:block;height:100%;background:#2e7d32}
      .bk-meta{font-size:13px;color:var(--ink-soft)}
      .bk-acts{margin-top:6px;display:flex;gap:10px;flex-wrap:wrap;font-size:14px}
      .bk-acts a{color:var(--gold-text);font-weight:700}
      .empty{color:var(--ink-soft);font-style:italic}
      .bm-snip{display:block;font-size:13.5px;color:var(--ink-soft);margin:3px 0}
      .note{font-size:13.5px;color:var(--ink-soft)}
      .danger{margin-top:8px}
      .phase5-nav{text-align:center;margin:26px 0 6px;font-size:14px;color:var(--ink-soft)}
      .phase5-nav a{color:var(--gold-text);font-weight:700}
"""

JS = """
<script>
(function(){
function ls(k){try{return localStorage.getItem(k)}catch(e){return null}}
function lsKeys(pref){var out=[];try{for(var i=0;i<localStorage.length;i++){var k=localStorage.key(i);if(k&&k.indexOf(pref)===0)out.push(k)}}catch(e){}return out}
function jparse(s,fb){try{return JSON.parse(s||"")}catch(e){return fb}}
function esc(s){return String(s==null?"":s).replace(/[&<>"]/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]})}
function dstr(t){try{return new Date(t).toLocaleDateString("vi-VN",{day:"numeric",month:"numeric",year:"numeric"})}catch(e){return""}}
var prog=jparse(ls("rv.prog"),{}), saved=jparse(ls("rv.saved"),[]), acad=jparse(ls("rv-academy-done"),[]);
if(!Array.isArray(saved))saved=[]; if(!Array.isArray(acad))acad=[];
var posKeys=lsKeys("rv.pos.vn/"), bmKeys=lsKeys("rv.bm.vn/");
var pos={}, bms={};
posKeys.forEach(function(k){var v=parseInt(ls(k)||"0",10);if(!isNaN(v))pos[k.slice(7)]=v});
bmKeys.forEach(function(k){var v=jparse(ls(k),[]);if(Array.isArray(v)&&v.length)bms[k.slice(7)]=v});
var reading=[],done=[];
Object.keys(prog).forEach(function(pid){var p=prog[pid];if(!p)return;
  (p.s==="done"?done:reading).push({pid:pid,p:p.p||0,t:p.t||0})});
reading.sort(function(a,b){return b.t-a.t}); done.sort(function(a,b){return b.t-a.t});
var bmTotal=0; Object.keys(bms).forEach(function(k){bmTotal+=bms[k].length});
function setTxt(id,t){var e=document.getElementById(id);if(e)e.textContent=t}
setTxt("st-reading",reading.length); setTxt("st-done",done.length);
setTxt("st-saved",saved.length); setTxt("st-bm",bmTotal);
setTxt("st-acad",acad.length+" / 122");
function fetchJ(u){return fetch(u).then(function(r){if(!r.ok)throw 0;return r.json()}).catch(function(){return null})}
Promise.all([fetchJ("/translations/index-lite.json"),fetchJ("/vi-books.json")]).then(function(xs){
  var lite=xs[0]||[], vib=xs[1]||{};
  var byId={},bySlug={};
  lite.forEach(function(e){if(e.id)byId[e.id]=e; if(e.slug)bySlug[e.slug]=e});
  function bookFor(pid){
    var e=byId[pid], v=vib[pid];
    if(e)return{title:e.short||pid,author:e.author||"",slug:e.slug,url:"/ban-dich/"+e.slug+".html",
      rd:v&&v.rd?v.rd:"/reader.html?id=vn/"+e.slug+"&pid="+encodeURIComponent(pid),mins:v?v.mins:0};
    if(v)return{title:pid,author:"",slug:null,url:v.u||"/",rd:v.rd||"/",mins:v.mins||0};
    return{title:pid,author:"",slug:null,url:"/",rd:"/",mins:0};
  }
  function row(it,verb){
    var b=bookFor(it.pid), pct=Math.max(0,Math.min(100,Math.round(it.p)||0));
    var posPage=(b.slug&&pos["vn/"+b.slug]!=null)?pos["vn/"+b.slug]:null;
    var cont=b.rd;
    if(posPage!=null)cont+=(cont.indexOf("?")>=0?"&":"?")+"p="+posPage;
    var h='<div class="bk-row"><h3><a href="'+esc(b.url)+'">'+esc(b.title)+"</a></h3>";
    if(b.author)h+='<div class="au">'+esc(b.author)+"</div>";
    h+='<div class="bar"><i style="width:'+pct+'%"></i></div>';
    h+='<div class="bk-meta">'+pct+"% · "+(it.t?("lần đọc gần nhất: "+dstr(it.t)):"")
      +(b.mins?(" · khoảng "+b.mins+" phút đọc"):"")+"</div>";
    h+='<div class="bk-acts"><a href="'+esc(cont)+'">'+verb+(posPage!=null?(" — trang "+(posPage+1)):"")
      +'</a><a href="'+esc(b.url)+'">Trang sách</a></div></div>';
    return h;
  }
  var rh=document.getElementById("sec-reading"), dh=document.getElementById("sec-done");
  rh.innerHTML=reading.length?reading.map(function(it){return row(it,"▶ Tiếp tục đọc")}).join("")
    :'<p class="empty">Bạn chưa đọc dở cuốn nào trên thiết bị này. Mở một cuốn sách trong <a href="/">thư viện</a> để bắt đầu — tiến độ sẽ hiện ở đây.</p>';
  dh.innerHTML=done.length?done.map(function(it){return row(it,"↺ Đọc lại")}).join("")
    :'<p class="empty">Chưa có cuốn nào đọc xong trên thiết bị này.</p>';
  var bh=document.getElementById("sec-bm"), bhtml="";
  Object.keys(bms).sort().forEach(function(slug){
    var e=bySlug[slug], v=vib[Object.keys(vib).find(function(k){return vib[k]&&vib[k].u&&vib[k].u.indexOf("/"+slug+".html")>=0})||""];
    var title=e?(e.short||slug):slug, rd=e?("/reader.html?id=vn/"+slug+"&pid="+encodeURIComponent(e.id)):(v&&v.rd?v.rd:"/");
    bhtml+='<div class="bk-row"><h3><a href="'+esc(e?("/ban-dich/"+slug+".html"):"/")+'">'+esc(title)+"</a></h3>";
    bms[slug].slice(0,20).forEach(function(b){
      var link=rd+(rd.indexOf("?")>=0?"&":"?")+"p="+(b.p||0);
      bhtml+='<a class="bm-snip" href="'+esc(link)+'">🔖 Trang '+((b.p||0)+1)+" — "+esc((b.s||"").slice(0,90))+"</a>";
    });
    if(bms[slug].length>20)bhtml+='<div class="bk-meta">…và '+(bms[slug].length-20)+" dấu trang nữa.</div>";
    bhtml+="</div>";
  });
  bh.innerHTML=bhtml||'<p class="empty">Chưa có dấu trang nào. Trong trình đọc, bấm nút dấu trang ở đoạn đang đọc để lưu lại.</p>';
  var sh=document.getElementById("sec-saved"), shtml="";
  saved.forEach(function(id){
    var e=byId[id], v=vib[id];
    if(e){shtml+='<div class="bk-row"><h3><a href="/ban-dich/'+esc(e.slug)+'.html">'+esc(e.short||id)+"</a></h3>"
      +'<div class="au">'+esc(e.author||"")+"</div></div>"}
    else if(v){shtml+='<div class="bk-row"><h3><a href="'+esc(v.u||("/"))+'">'+esc(id)+"</a></h3></div>"}
    else{shtml+='<div class="bk-row"><h3><a href="/?b='+encodeURIComponent(id)+'">'+esc(id)+"</a></h3>"
      +'<div class="au">Mở trong thư viện</div></div>'}
  });
  sh.innerHTML=shtml||'<p class="empty">Bạn chưa lưu cuốn nào. Bấm ☆ Lưu trên một cuốn sách trong <a href="/">thư viện</a> để xem lại ở đây.</p>';
  var ah=document.getElementById("sec-acad");
  ah.innerHTML=acad.length?('<p>Bạn đã đánh dấu hoàn thành <b>'+acad.length+' / 122</b> bài học trong Học Viện. '
    +'<a href="/hoc-vien/">Mở Học Viện →</a></p>')
    :'<p class="empty">Chưa có bài học nào được đánh dấu hoàn thành. <a href="/hoc-vien/">Mở Học Viện →</a></p>';
});
var clr=document.getElementById("clear-data");
if(clr)clr.addEventListener("click",function(){
  if(!confirm("Xóa toàn bộ tiến độ đọc trên thiết bị này?\\n\\nSẽ xóa: tiến độ đọc (rv.prog), vị trí đọc dở (rv.pos.*), dấu trang (rv.bm.*), sách đã lưu (rv.saved) và bài học Học Viện đã đánh dấu (rv-academy-done).\\n\\nKhông thể hoàn tác."))return;
  try{localStorage.removeItem("rv.prog");localStorage.removeItem("rv.saved");localStorage.removeItem("rv-academy-done");
    lsKeys("rv.pos.").forEach(function(k){localStorage.removeItem(k)});
    lsKeys("rv.bm.").forEach(function(k){localStorage.removeItem(k)})}catch(e){}
  location.reload();
});
})();
</script>
"""


def main():
    url = f"{BASE}/bang-doc-sach.html"
    body = f"""  <p class="crumb"><a href="/">Trang chủ</a></p>
  <div class="cat-head">
    <div class="kicker">Của riêng bạn, trên thiết bị này</div>
    <h1>Bảng đọc của tôi</h1>
    <p style="max-width:640px;margin:0 auto;color:var(--ink-soft)">Sách bạn đang đọc, đã đọc xong, đã lưu và dấu trang — tất cả chỉ lưu trên thiết bị và trình duyệt này. Không có tài khoản, không đồng bộ, không dữ liệu nào rời khỏi máy bạn.</p>
  </div>
  <div class="stat-grid">
    <div class="stat"><b id="st-reading">–</b><span>đang đọc</span></div>
    <div class="stat"><b id="st-done">–</b><span>đã đọc xong</span></div>
    <div class="stat"><b id="st-saved">–</b><span>đã lưu</span></div>
    <div class="stat"><b id="st-bm">–</b><span>dấu trang</span></div>
    <div class="stat"><b id="st-acad">–</b><span>bài học Học Viện</span></div>
  </div>
  <h2>Đang đọc</h2>
  <div id="sec-reading"><p class="empty">Đang tải…</p></div>
  <h2>Đã đọc xong</h2>
  <div id="sec-done"><p class="empty">Đang tải…</p></div>
  <h2>Dấu trang</h2>
  <div id="sec-bm"><p class="empty">Đang tải…</p></div>
  <h2>Đã lưu</h2>
  <div id="sec-saved"><p class="empty">Đang tải…</p></div>
  <h2>Học Viện</h2>
  <div id="sec-acad"><p class="empty">Đang tải…</p></div>
  <h2>Quyền riêng tư</h2>
  <p>Tiến độ đọc được trình đọc lưu vào bộ nhớ của trình duyệt (localStorage) khi bạn đọc sách trên trang này — cùng cơ chế với nút “Tiếp tục đọc” trên trang sách. Đổi trình duyệt, đổi máy, hay xóa dữ liệu trình duyệt thì tiến độ sẽ mất. Trang này không gửi tiến độ của bạn đi đâu cả.</p>
  <p class="danger"><button type="button" id="clear-data" class="btn">Xóa dữ liệu đọc trên thiết bị này</button></p>
  <p class="note">Tìm sách để đọc tiếp: <a href="/">thư viện</a> · <a href="/lo-trinh.html">lộ trình đọc</a> · <a href="/nghien-cuu-kinh-thanh.html">nghiên cứu Kinh Thánh</a></p>
  <p class="phase5-nav"><a href="/theo-doi-dich-thuat.html">Theo dõi dự án dịch thuật</a> · <a href="/lo-trinh-phat-trien.html">Lộ trình phát triển</a></p>
  {share_row(url)}
  {report_mailto("Bảng đọc của tôi")}"""
    p = (head("Bảng đọc của tôi — tiến độ đọc trên thiết bị này | Reformed Vietnam",
              "Bảng đọc cá nhân: sách đang đọc, đã đọc xong, đã lưu và dấu trang — "
              "chỉ lưu trên thiết bị này, không tài khoản, không đồng bộ.",
              url, CSS)
         + "<body><main>" + header + body + "</main>" + footer + MINI_JS + JS + "</body></html>")
    changed = write_if_changed(ROOT / "bang-doc-sach.html", p)
    check_links(p, "/bang-doc-sach.html")
    print(f"dashboard: {'written' if changed else 'unchanged'}")
    print(f"sitemap: {sitemap_add(['/bang-doc-sach.html'])} URLs added")
    print("DONE")


if __name__ == "__main__":
    main()

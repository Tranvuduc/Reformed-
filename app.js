var RV = window.RV_CONFIG || {};
var T={
 vi:{allTypes:"Mọi thể loại",allEras:"Mọi thời kỳ",clear:"Xóa bộ lọc",sort0:"Mặc định",sort1:"Tên sách A–Z",sort2:"Tên tác giả A–Z",sort3:"Xưa nhất trước",sort4:"Mới nhất trước",
   ty_systematic:"Thần học hệ thống",ty_commentary:"Bình giải",ty_sermons:"Bài giảng",ty_devotional:"Suy niệm và cầu nguyện",ty_doctrine:"Giáo lý và luận thuyết",ty_catechism:"Kinh Thánh, tín điều",ty_history:"Lịch sử và nhân vật",ty_collected:"Tuyển tập",ty_bible:"Kinh Thánh",ty_classic:"Cổ điển",
   er_anc:"Trước năm 1500",er_ref:"Cải Chánh (thế kỷ 16)",er_pur:"Thời Thanh giáo (thế kỷ 17)",er_aw:"Thời Phục hưng (thế kỷ 18)",er_mod:"Thế kỷ 19",er_c20:"Từ năm 1900",
   sync:"Đồng bộ",about:"Giới thiệu",sh:"Đồng bộ giữa các thiết bị",sp:"Mã này giống như chìa khóa riêng của bạn: ai biết mã đều xem và sửa được tiến độ của bạn. Hãy dùng cùng một mã trên các thiết bị.",snew:"Tạo mã mới",suse:"Dùng mã này",soff:"Tắt đồng bộ",sclose:"Đóng",sbad:"Mã không hợp lệ. Chỉ dùng chữ và số, 20–40 ký tự.",sok:"Đã đồng bộ xong.",serr:"Không đồng bộ được lúc này.",
   search:"Tìm sách, tác giả, chủ đề…",read:"Đọc",listen:"Nghe",archive:"Lưu trữ",more:"Xem thêm",of:"trong",titles:"tiêu đề",none:"Chưa có sách nào phù hợp.",noreading:"Chưa có mục nào đang đọc.",nosaved:"Chưa lưu sách nào.",cont:"Tiếp tục đọc",cont2:"Tiếp tục",home:"Trang chủ",browse:"Duyệt tất cả",reading:"Đang đọc",done:"Đã xong",saved:"Đã lưu",start:"Bắt đầu",all:"Tất cả",sr_cur:"Chọn lọc (không gồm bản scan)",sr_ccel:"CCEL (đọc tại đây)",sr_vn:"Tiếng Việt",sr_mg:"Monergism",sr_ia:"Internet Archive",sr_pg:"Project Gutenberg",sr_lv:"LibriVox",sr_dg:"Desiring God",sr_lig:"Ligonier",sr_other:"Khác",
   md_read:"Đọc tại đây",md_pdf:"Có PDF",md_epub:"Có EPUB",md_audio:"Có sách nói",authorPh:"Tìm tác giả…",
   h1:"Sách Cải Chánh, <span>miễn phí</span>",lede:"Sách và tài liệu miễn phí, đọc và nghe đọc trên điện thoại. Phần lớn là tác phẩm thuộc phạm vi công cộng; mỗi thẻ ghi rõ nguồn, mức độ, và bản quyền.",
   foot:"Thư viện sách Cải Chánh miễn phí. Dành cho đọc, học và suy ngẫm.",
   menu:"Menu",lang:"Cài đặt ngôn ngữ",theme:"Chuyển giao diện",sync:"Đồng bộ",about:"Giới thiệu",
   "s-h":"Đồng bộ giữa các thiết bị","s-p":"Mã này giống như chìa khóa riêng của bạn: ai biết mã đều xem và sửa được tiến độ của bạn. Hãy dùng cùng một mã trên các thiết bị.","s-new":"Tạo mã mới","s-use":"Dùng mã này","s-off":"Tắt đồng bộ","s-x":"Đóng",
   "s-st":""},
  en:{allTypes:"All types",allEras:"All eras",clear:"Clear filters",sort0:"Default order",sort1:"Title A–Z",sort2:"Author A–Z",sort3:"Oldest first",sort4:"Newest first",
   ty_systematic:"Systematic theology",ty_commentary:"Commentary",ty_sermons:"Sermons",ty_devotional:"Devotional and prayer",ty_doctrine:"Doctrine and treatises",ty_catechism:"Creeds and catechisms",ty_history:"History and biography",ty_collected:"Collected works",ty_bible:"Bible",ty_classic:"Classics",
   er_anc:"Before 1500",er_ref:"Reformation (1500s)",er_pur:"Puritan age (1600s)",er_aw:"Awakening era (1700s)",er_mod:"1800s",er_c20:"1900 and later",
   sync:"Sync",about:"About",sh:"Sync across devices",sp:"The sync code is your secret: anyone with it can read and write your progress. Enter the same code on another device.",snew:"Create new code",suse:"Use this code",soff:"Turn sync off",sclose:"Close",sbad:"Invalid code. Use only letters and numbers, 20–40 characters.",sok:"Sync complete.",serr:"Sync failed right now.",
   search:"Search books, authors, topics…",read:"Read",listen:"Listen",archive:"Archive",more:"More",of:"of",titles:"titles",none:"No books match the current filters.",noreading:"No books are marked as reading.",nosaved:"No books saved yet.",cont:"Continue reading",cont2:"Continue",home:"Home",browse:"Browse all",reading:"Reading",done:"Done",saved:"Saved",start:"Start",all:"All",sr_cur:"Curated (no raw scans)",sr_ccel:"CCEL (read here)",sr_vn:"Vietnamese",sr_mg:"Monergism",sr_ia:"Internet Archive",sr_pg:"Project Gutenberg",sr_lv:"LibriVox",sr_dg:"Desiring God",sr_lig:"Ligonier",sr_other:"Other",
   md_read:"Read here",md_pdf:"Has PDF",md_epub:"Has EPUB",md_audio:"Has audiobook",authorPh:"Author…",
   h1:"Free Reformed <span>Books</span>",lede:"Free books and resources for reading and listening on your phone. Many works are public domain; every card includes source, level, and copyright status.",
   foot:"Free Reformed library. For reading, study, and reflection.",
   menu:"Menu",lang:"Language",theme:"Theme",sync:"Sync",about:"About",
   "s-h":"Sync across devices","s-p":"The sync code is your secret: anyone with it can read and write your progress. Enter the same code on another device.","s-new":"Create new code","s-use":"Use this code","s-off":"Turn sync off","s-x":"Close",
   "s-st":""}
};
T.vi.allSources="Mọi nguồn";T.en.allSources="All sources";T.vi.allMedia="Mọi định dạng";T.en.allMedia="All formats";T.vi.authorPh="Tìm tác giả…";T.en.authorPh="Author…";
T.vi.md_read="Đọc tại đây";T.en.md_read="Read here";T.vi.md_pdf="Có PDF";T.en.md_pdf="Has PDF";T.vi.md_epub="Có EPUB";T.en.md_epub="Has EPUB";T.vi.md_audio="Có sách nói";T.en.md_audio="Has audiobook";
T.vi.sr_cur="Chọn lọc (không gồm bản scan)";T.en.sr_cur="Curated (no raw scans)";T.vi.sr_ccel="CCEL (đọc tại đây)";T.en.sr_ccel="CCEL (read here)";T.vi.sr_vn="Tiếng Việt";T.en.sr_vn="Vietnamese";T.vi.sr_mg="Monergism";T.en.sr_mg="Monergism";T.vi.sr_ia="Internet Archive";T.en.sr_ia="Internet Archive";T.vi.sr_pg="Project Gutenberg";T.en.sr_pg="Project Gutenberg";T.vi.sr_lv="LibriVox";T.en.sr_lv="LibriVox";T.vi.sr_dg="Desiring God";T.en.sr_dg="Desiring God";T.vi.sr_lig="Ligonier";T.en.sr_lig="Ligonier";T.vi.sr_other="Khác";T.en.sr_other="Other";
var SRCS = RV.SRCS || ["ccel","vn","mg","ia","pg","lv","dg","lig","other"],
    MEDIA = RV.MEDIA || ["read","pdf","epub","audio"],
    AUDIO = {};
function srcOf(b){return b.read?"ccel":(b.au||"other")}
function hasM(b,m){if(m==="read")return!!b.read||!!rdr(b);if(m==="pdf")return!!b.pdf||!!(b.dl&&(b.dl.PDF||b.dl.pdf));if(m==="epub")return!!b.epub||!!(b.dl&&(b.dl.EPUB||b.dl.epub));if(m==="audio")return!!(b.listen||b.audio||b.au==="lv"||(b.dl&&(b.dl.audio||b.dl.AUDIO)));return false}
function typeOf(title,key,over){
  if(over&&over[key])return over[key];
  var t=title.toLowerCase();
  if(/catechism|confession of faith|creeds/.test(t))return"catechism";
  if(/commentar|exposition|expository|harmony of|annotations|treasury of david/.test(t))return"commentary";
  if(/sermon/.test(t))return"sermons";
  if(/systematic theology|institutes|institutio|dogmatic|body of divinity|body of practical divinity|doctrinal divinity|summary of christian doctrine|reformed doctrine of predestination/.test(t))return"systematic";
  if(/^works of|practical works|miscellaneous/.test(t))return"collected";
  if(/history|martyrs|life of|christian church|philosophy of revelation|person of christ/.test(t))return"history";
  if(/morning and evening|checkbook|daily readings|everlasting rest|prayer|meditation|letters|contentment|holiness|crook|cordial|lovely|armour|saint indeed/.test(t))return"devotional";
  return"doctrine";
}
function eraOf(y){return y<1500?"anc":y<1600?"ref":y<1700?"pur":y<1800?"aw":y<1900?"mod":"c20"}
var $=function(i){return document.getElementById(i)};
var PAGE=48;
var DESC={},START=[];
var BOOKS=[],AUTHORS=[],st={f:"all",q:"",an:"",sr:"all",md:"all",ty:"all",er:"all",so:"0",limit:PAGE,saved:[],prog:{},lang:"vi"};
var TYPES = RV.TYPES || ["systematic","commentary","sermons","devotional","doctrine","catechism","history","collected","bible","classic"];
var ERAS = RV.ERAS || ["anc","ref","pur","aw","mod","c20"];
var ERAMID={anc:1000,ref:1550,pur:1650,aw:1750,mod:1850,c20:1950};
try{
  st.saved=JSON.parse(localStorage.getItem("rv.saved")||"[]");
  st.prog=JSON.parse(localStorage.getItem("rv.prog")||"{}");
  var l=localStorage.getItem("rv.lang");
  if(l)st.lang=l;
}catch(e){}
function saveLS(k,v){try{localStorage.setItem(k,JSON.stringify(v))}catch(e){}}
function esc(s){return String(s).replace(/[&<>\"]/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;"}[c]})}
function tx(k){return T[st.lang][k]}
function G(q){return"https://www.gutenberg.org/ebooks/search/?query="+encodeURIComponent(q)}
function L(q){return"https://librivox.org/search?primary_key=0&search_category=title&search_page=1&search_form=get_results&q="+encodeURIComponent(q)}
function A(q){return"https://archive.org/search?query="+encodeURIComponent(q)+"&and[]=mediatype%3A%22texts%22"}
function hue(s){var h=0;for(var i=0;i<s.length;i++)h=(h*31+s.charCodeAt(i))%360;return h}
function spurgeonYear(n){return n===8||n===9?1863:1854+n}
function lvl(b){var n=LVL_ID[b.id]||RVL[b.id]||LVL_T[b.ty]||(String(b.id).indexOf("rv-")===0?2:0);return n}
function lvlTxt(n){var vi=st.lang==="vi";return n===1?(vi?"🟢 Dễ đọc":"🟢 Beginner"):n===2?(vi?"🟡 Vừa":"🟡 Intermediate"):n===3?(vi?"🔴 Chuyên sâu":"🔴 Advanced"):""}
var RVT={"Charles Spurgeon":["Báp-tít Cải Chánh","Reformed Baptist"],"J.C. Ryle":["Anh giáo, Tin Lành","Anglican evangelical"],"Jonathan Edwards":["Cải Chánh, Hội Chúng","Reformed Congregational"],"John Owen":["Thanh giáo (Độc lập)","Puritan (Independent)"]};
var RVL={"rv-compel-them-to-come-in":1,"rv-do-you-pray":1,"rv-mccheyne-banh-hang-ngay":1,"rv-newton-cay-non-bong-lua-hot-chac":1,"rv-whitefield-con-duong-cua-an-dien":1};
var TRAD={calvin:["Cải Chánh thế kỷ 16","Sixteenth-century Reformed"],knox:["Trưởng Lão Scotland","Scottish Presbyterian"],owen:["Thanh giáo (Độc lập)","Puritan (Independent)"],baxter:["Thanh giáo (Cải Chánh)","Puritan (Reformed)"],edwards:["Cải Chánh, Hội Chúng","Reformed Congregational"],spurgeon:["Báp-tít Cải Chánh","Reformed Baptist"],ryle:["Anh giáo, Tin Lành","Anglican evangelical"]};
function trad(b){var t=TRAD[b.au]||(String(b.id).indexOf("rv-")===0&&RVT[b.a]);return t?t[st.lang==="vi"?0:1]:""}
var POL=/\b(popery|popish|papist|papism|papal|pope|jesuit|romish|rome|antichrist|wesley|arminian|unitarian|quaker)/i;
function badges(b){
  var o=[];if(b.au==="vn")o.push(["VI","vi"]);
  if(String(b.id).indexOf("rv-")===0)o.push([st.lang==="vi"?"AI, chưa duyệt":"AI, unreviewed",""]);
  if(b.read||rdr(b))o.push([st.lang==="vi"?"Đọc":"Read","r"]);
  if(hasM(b,"pdf"))o.push(["PDF",""]);if(hasM(b,"epub"))o.push(["EPUB",""]);
  if(hasM(b,"audio"))o.push([st.lang==="vi"?"🎧 Nghe":"🎧 Audio",""]);
  if(!b.read&&b.url&&!hasM(b,"pdf")&&!hasM(b,"epub")&&!hasM(b,"audio"))o.push(["Web",""]);
  if(!b.read&&!b.url)o.push(["Web",""]);if(b.au==="ia"&&b.y&&b.y<1700)o.push([st.lang==="vi"?"Văn cổ":"Early English","old"]);
  if(POL.test((b.en&&b.en.t)||""))o.unshift([st.lang==="vi"?"Tranh luận":"Polemic","pol"]);
  var L=lvl(b);if(L&&b.au!=="ia"&&b.au!=="pg"&&b.au!=="lv")o.unshift([lvlTxt(L),"lv"+L]);
  return o.map(function(x){return'<span class="bd '+x[1]+'">'+x[0]+'</span>'}).join("");
}
var CTX={
"bunyan/pilgrim":["Truyện ngụ ngôn Thanh giáo thế kỷ 17, phần đầu được viết khi Bunyan ở tù. Hãy đọc như câu chuyện về đời sống đức tin, không phải sách triết học.","Rô-ma 5:1-2","Tôi nhận ra sự an toàn trong Đấng Christ không phải từ sự hoàn hảo của tôi."]
};
function ctxBox(b){var c=CTX[b.id];
  if(!c&&b.er==="pur")c=["Tác phẩm Thanh giáo thế kỷ 16-17. Các ví dụ về xã hội và gia đình phản ánh thời của tác giả, không nên áp dụng máy móc cho ngày nay.","Mác 10:45","Tôi đặt sự lớn lao của Đức Chúa Trời lên trước những muốn cầu của mình."];
  if(!c)return"";
  return'<div class="ctx"><b>Đọc trong bối cảnh</b><p>'+esc(c[0])+'</p>'+(c[1]?'<p><b>Đọc Kinh Thánh:</b> '+esc(c[1])+'</p><p><b>Suy ngẫm:</b> '+esc(c[2])+'</p>':'')+'<small>Ghi chú: nội dung này giúp đặt sách vào bối cảnh lịch sử và thần học.</small></div>';
}
function infoBox(b){
  var vi=st.lang==="vi",rv=String(b.id).indexOf("rv-")===0,vb=window.VIB&&VIB[b.id],pd=b.read||b.au==="ia"||b.au==="pg"||b.au==="lv"||/ccel\.org/.test(b.url||"")||rv||vb;
  var L=lvl(b),T=trad(b),R=[];
  var src=rv?(vi?"Reformed Vietnam (dịch từ nguyên tác phạm vi công cộng)":"Reformed Vietnam (from public-domain original)"):vb?"Reformed Vietnam":b.read||/ccel\.org/.test(b.url||"")?"CCEL":b.au==="vn"?(vi?"Bản tiếng Việt của nhà xuất bản":"Publisher's Vietnamese edition"):b.au==="mg"?(vi?"Monergism / 9Marks":"Monergism / 9Marks"):b.au==="ia"?(vi?"Internet Archive":"Internet Archive"):b.au==="pg"?(vi?"Project Gutenberg":"Project Gutenberg"):b.au==="lv"?(vi?"LibriVox":"LibriVox"):b.au==="dg"?(vi?"Desiring God":"Desiring God"):b.au==="lig"?(vi?"Ligonier":"Ligonier"):vi?"Nguồn khác":"Other source";
  var st2=rv||vb?(vi?"AI hỗ trợ dịch, chưa được mục sư duyệt":"AI-assisted, not pastor-reviewed"):b.au==="vn"?(vi?"Bản tiếng Việt của nhà xuất bản":"Publisher's Vietnamese edition"):b.au==="mg"?(vi?"Tự do, không phải bản dịch chính thức":"Free reference / public access"):vi?"Bản gốc hoặc kết nối ra trang gốc":"Original or linked source";
  R.push([vi?"Nguồn":"Source",src],[vi?"Tình trạng bản dịch":"Translation",st2]);
  if(T)R.unshift([vi?"Truyền thống":"Tradition",T]);
  if(L)R.push([vi?"Mức độ":"Level",lvlTxt(L)]);
  R.push([vi?"Bản quyền":"Copyright",pd?(vi?"🟢 Phạm vi công cộng":"🟢 Public domain"):vi?"🟡 Thuộc tác giả hoặc nhà xuất bản":"🟡 Author or publisher"]);
  return'<dl class="inf">'+R.map(function(r){return'<dt>'+r[0]+'</dt><dd>'+esc(r[1])+'</dd>'}).join("")+'</dl>';
}
function lic(b){
  var vi=st.lang==="vi",pd=b.read||b.au==="ia"||b.au==="pg"||b.au==="lv"||/ccel\.org/.test(b.url||"");
  return pd?'<p class="lic pd">🟢 '+(vi?"Phạm vi công cộng. Bạn được đọc, tải và chia sẻ tự do.":"Public domain. Free to read, download and share.")+'</p>'
   :'<p class="lic ex">🟡 '+(vi?"Liên kết ra trang gốc. Bản quyền thuộc tác giả hoặc nhà xuất bản, chúng tôi không lưu bản sao.":"Link to the original site. Copyright belongs to the author or publisher; we do not host a copy.")+'</p>';
}
function card(b){
  var lg=st.lang,d=b[lg]||b.en,y=b.y?" · "+(b.y<0?Math.abs(b.y)+" BC":b.y):"";
  return'<article class="book" tabindex="0" role="button" data-open="'+esc(b.id)+'"><div class="spine" style="background-color:'+b.col+'"><b>'+tx("ty_"+b.ty)+y+'</b><i>'+esc(d.t)+'</i></div><div class="meta"><h3>'+esc(d.t)+'</h3><div class="by">'+esc(b.a)+(trad(b)?' · <i>'+esc(trad(b))+'</i>':'')+'</div><div class="badges">'+badges(b)+'</div></div></article>';
}
function rdr(b){var m=/^\/doc\/([a-z0-9_-]+)\.html$/i.exec(b.url||"");return m?"reader.html?id=vn/"+m[1]+"&pid="+encodeURIComponent(b.id):""}
function sheetActs(b){
  var lg=st.lang,vi=lg==="vi",x="",id=encodeURIComponent(b.id),ext=' target="_blank" rel="noopener"';
  if(window.VIB&&VIB[b.id])x+='<a class="p" href="'+(VIB[b.id].rd||VIB[b.id].u)+'">📖 '+(vi?"Đọc bản dịch tiếng Việt":"Read Vietnamese translation")+' <small>('+(VIB[b.id].r?(vi?"đã duyệt":"reviewed"):vi?"chưa duyệt":"unreviewed")+')</small></a>';
  if(b.read){
    x+='<a class="p" href="reader.html?id='+id+'">'+(vi?"Đọc tại đây":"Read here")+'</a>';
    if(b.au!=="vn")x+='<a class="s2" href="reader.html?id='+id+'&tr=1">🌐 '+(vi?"Đọc bản dịch tiếng Việt (dịch máy)":"Read Vietnamese translation (machine)")+'</a>';
    for(var f in b.dl)x+='<a class="s2" href="'+b.dl[f]+'"'+ext+'>⬇ '+f+'</a>';
    x+='<a class="s2" href="'+b.read+'"'+ext+'>CCEL ↗</a>';
    if(b.lv)x+='<a class="s2" href="'+b.lv+'"'+ext+'>🎧 LibriVox</a>';
    if(AUDIO[b.id])x+='<a class="s2" href="'+b.read+'"'+ext+'>🎧 CCEL audio</a>';
  }else if(rdr(b)){
    x+='<a class="p" href="'+rdr(b)+'">'+(vi?"Đọc tại đây":"Read here")+' <small>('+(vi?"AI, chưa duyệt":"AI, not yet reviewed")+')</small></a>';
    if(b.epub)x+='<a class="s2" href="'+b.epub+'" download>⬇ EPUB</a>';
    x+='<a class="s2" href="'+b.url+'">'+(vi?"Trang sách":"Book page")+'</a>';
  }else if(b.url){
    x+='<a class="p" href="'+b.url+'"'+ext+'>'+(b.au==="lv"?"🎧 "+tx("listen"):(vi?"Mở trang sách":"Open book page"))+' ↗</a>';
    if(b.pdf)x+='<a class="s2" href="'+b.pdf+'"'+ext+'>⬇ PDF</a>';
    if(b.epub)x+='<a class="s2" href="'+b.epub+'"'+ext+'>⬇ EPUB</a>';
  }else{
    var ks=b.q||b.en.t;
    x+='<a class="p" href="'+G(ks)+'"'+ext+'>'+tx("read")+' ↗</a><a class="s2" href="'+L(b.en.t)+'"'+ext+'>🎧 '+tx("listen")+'</a><a class="s2" href="'+A(ks)+'"'+ext+'>'+tx("archive")+'</a>';
  }
  x+='<button class="s2" type="button" data-share="'+esc(b.id)+'">↗ '+(vi?"Chia sẻ":"Share")+'</button><a class="s2" href="mailto:reformedvn@gmail.com?subject='+encodeURIComponent((vi?"Báo lỗi / Gợi ý sách":"Report issue / Suggest a book"))+'&body='+encodeURIComponent((vi?"Sách: ":"Book: ")+b.en.t)+'">✉ '+(vi?"Góp ý":"Feedback")+'</a>';
  return x;
}
var curBk=null,deepDone=false;
function deepLink(){if(deepDone)return;var id=new URLSearchParams(location.search).get("b");if(!id){deepDone=true;return}if(BOOKS.some(function(z){return z.id===id})){deepDone=true;openBook(id)}}
function openBook(id){
  var b=BOOKS.filter(function(z){return z.id===id})[0];if(!b)return;curBk=id;sheet(b);var dl=$("bk");if(!dl.open)dl.showModal();
}
function sheet(b){
  var lg=st.lang,d=b[lg]||b.en,o=b[lg==="vi"?"en":"vi"]||{},p=prog(b.id),s=st.saved.indexOf(b.id)>=0;
  var y=b.y?" · "+(b.y<0?Math.abs(b.y)+" BC":b.y):"";
  var alt=(lg==="vi"&&o.t&&o.t!==d.t)?'<p class="alt">'+esc(o.t)+'</p>':"";
  var sel='<select data-pid="'+esc(b.id)+'" aria-label="'+tx("reading")+'">'+["todo","reading","done"].map(function(v){return'<option value="'+v+'"'+(p.s===v?" selected":"")+'>'+tx(v)+'</option>'}).join("")+'</select>';
  var rng=p.s==="reading"?'<div class="pr"><input type="range" min="0" max="100" step="5" value="'+p.p+'" data-rid="'+esc(b.id)+'" aria-label="%"><output>'+p.p+'%</output></div>':"";
  $("bk-c").innerHTML='<button class="bk-x" type="button" aria-label="Close">×</button><p class="k">'+tx("ty_"+b.ty)+y+'</p><h2>'+esc(d.t)+'</h2>'+alt+'<p class="by">'+esc(b.a)+(trad(b)?' · <i>'+esc(trad(b))+'</i>':'')+'</p>'+ctxBox(b)+'<div class="acts">'+sheetActs(b)+'</div>'+infoBox(b)+lic(b)+'<div class="sheet-row"><button type="button" class="fav'+(s?" on":"")+'" data-id="'+esc(b.id)+'">'+(vi?"☆":"☆")+'</button>'+sel+rng+'</div>';
}
function renderCont(){
  var r=BOOKS.filter(function(b){return prog(b.id).s==="reading"}).sort(function(a,b){return(prog(b.id).t||0)-(prog(a.id).t||0)}).slice(0,4);
  var el=$("cont");
  if(!r.length){el.hidden=true;return}
  el.hidden=false;
  el.innerHTML='<h2>'+tx("cont")+'</h2><div class="controw">'+r.map(function(b){
    var d=b[st.lang]||b.en,p=prog(b.id),href=b.read?"reader.html?id="+encodeURIComponent(b.id):(rdr(b)||b.url||G(b.q||b.en.t));
    return'<div class="ci"><b>'+esc(d.t)+'</b><div class="meter"><i style="width:'+p.p+'%"></i></div><a href="'+href+'">'+tx("cont2")+' · '+p.p+'%</a></div>';
  }).join("")+'</div>';
}
function yr(b){return b.y||ERAMID[b.er]}
function sorted(list){
  var s=st.so,lg=st.lang;
  if(s==="0"){
    if(st.f==="start")return list.slice().sort(function(a,b){return START.indexOf(a.id)-START.indexOf(b.id)});
    var sc=function(b){return b.au==="vn"?0:(DESC[b.id]||(b.vi&&b.vi.t&&b.vi.t!==b.en.t))?1:b.au==="ia"?(b.y&&b.y<1700?5:b.y&&b.y<1800?4:3):2};
    return list.map(function(b,i){return[b,i]}).sort(function(x,y){return sc(x[0])-sc(y[0])||x[1]-y[1]}).map(function(x){return x[0]});
  }
  var n=function(b){return(b[lg]||b.en).t.toLowerCase()};
  var cmp={"1":function(a,b){return n(a)<n(b)?-1:n(a)>n(b)?1:0},
           "2":function(a,b){return a.a<b.a?-1:a.a>b.a?1:(n(a)<n(b)?-1:1)},
           "3":function(a,b){return yr(a)-yr(b)},
           "4":function(a,b){return yr(b)-yr(a)}}[s];
  return list.slice().sort(cmp);
}
function nAct(){return(st.sr!=="all")+(!!st.an)+(st.md!=="all")+(st.ty!=="all")+(st.er!=="all")+(st.so!=="0")}
function filtersOn(){return st.sr!=="all"||!!st.an||st.md!=="all"||st.ty!=="all"||st.er!=="all"||st.so!=="0"||st.q!==""||st.f!=="all"}
var VIEW=(function(){try{return localStorage.getItem("rv.view")||"grid"}catch(e){return"grid"}})();
function home(){return st.f==="all"&&!st.q&&st.sr==="all"&&!st.an&&st.md==="all"&&st.ty==="all"&&st.er==="all"&&st.so==="0"&&!st.br}
function render(){
  document.body.classList.toggle("home",home());
  var bar=document.querySelector(".bar");bar.classList.toggle("open",filtersOn()&&st.f==="all"||bar.dataset.o==="1");$("ftog").textContent=(st.lang==="vi"?"Bộ lọc":"Filters")+(nAct()?" · "+nAct():"");
  var all=sorted(BOOKS.filter(passes)),show=all.slice(0,st.limit);
  $("clear").hidden=!(filtersOn()||st.br);$("clear").textContent=filtersOn()?tx("clear"):(st.lang==="vi"?"‹ Trang chủ":"‹ Home");
  $("grid").className="grid"+(VIEW==="list"?" list":"");$("view").textContent=VIEW==="list"?"▦":"☰";
  $("grid").innerHTML=show.length?show.map(card).join(""):'<div class="empty">'+(st.f==="saved"?tx("nosaved"):(st.f==="reading"||st.f==="done")?tx("noreading"):tx("none"))+'</div>';
  $("count").textContent=all.length+" "+tx("of")+" "+BOOKS.length+" "+tx("titles");
  var m=$("more"),left=all.length-show.length;
  m.hidden=left<=0;m.textContent=tx("more")+" ("+left+")";
  renderCont();renderShelves();
}
var LEVELS = RV.LEVELS || [
  {k:"new",t:["Mới tin Chúa","New believer"],d:["Đọc nhẹ, dễ vào","Gentle and clear"],ids:["bunyan/pilgrim","bonar/peace","ryle/holiness","flavel/lovely","spurgeon/grace"]},
  {k:"grow",t:["Đang lớn lên","Growing"],d:["Đời sống thuộc linh","Deeper devotion"],ids:["owen/mort","watson/contentment","baxter/saints_rest","boston/crook","edwards/affections"]},
  {k:"deep",t:["Học sâu","Studying"],d:["Thần học hệ thống","Systematic theology"],ids:["calvin/institutes","edwards/will","hodge/theology1","berkhof/systematictheology","kuyper/holy_spirit"]}
];
var lvSel="";try{lvSel=localStorage.getItem("rv.lv")||""}catch(e){}
function renderLevels(){
  var el=$("lv"),on=home();el.hidden=!on;if(!on)return;
  var i=st.lang==="vi"?0:1;
  var h='<h2>'+(i?"Not sure what to read? Pick your level":"Chưa biết nên đọc gì? Chọn mức của bạn")+'</h2><div class="lvb">'+LEVELS.map(function(l){return'<button type="button" data-lv="'+l.k+'" class="'+(lvSel===l.k?"sel":"")+'"><b>'+l.t[i]+'</b><small>'+l.d[i]+'</small></button>'}).join("")+'</div>';
  var L=LEVELS.filter(function(l){return l.k===lvSel})[0];
  if(L){var l5=L.ids.map(function(id){return BOOKS.filter(function(b){return b.id===id})[0]}).filter(Boolean);
    h+='<div class="srow lvr">'+l5.map(card).join("")+'</div><a class="lvp" href="lo-trinh.html">'+(i?"Follow the full reading plan →":"Theo lộ trình đọc đầy đủ →")+'</a>'}
  el.innerHTML=h;
}
$("lv").addEventListener("click",function(e){
  var oc=e.target.closest("[data-open]");if(oc&&!e.target.closest(".fav")){openBook(oc.dataset.open);return}
  var b=e.target.closest("button[data-lv]");if(!b)return;lvSel=lvSel===b.dataset.lv?"":b.dataset.lv;try{localStorage.setItem("rv.lv",lvSel)}catch(x){}renderLevels();
});
var SHELVES = RV.SHELVES || [
  {k:"vn",sr:"vn",t:["Tiếng Việt","Vietnamese readings"],p:function(b){return b.au==="vn"},o:function(a,b){return(a.id.indexOf("vn-")===0?1:0)-(b.id.indexOf("vn-")===0?1:0)}},
  {k:"aud",md:"audio",t:["Sách nói","Audiobooks"],p:function(b){return hasM(b,"audio")},o:function(a,b){return(a.au==="lv"?1:0)-(b.au==="lv"?1:0)}}
];
function renderShelves(){
  var el=$("shelves"),on=home();renderLevels();
  $("allh").hidden=true;$("bw").hidden=!on;$("browse").textContent=(st.lang==="vi"?"Đã biết mình cần gì? Duyệt toàn bộ thư viện":"Know what you want? Browse the whole library");
  if(!on||1){el.innerHTML="";return}
  var i=st.lang==="vi"?0:1;
  el.innerHTML=SHELVES.map(function(s){
    var l=BOOKS.filter(s.p);if(s.o)l.sort(s.o);else l.sort(function(a,b){return(DESC[b.id]?1:0)-(DESC[a.id]?1:0)});
    l=l.slice(0,8);if(l.length<3)return"";
    return'<section class="shelf"><div class="shelfh"><h2>'+s.t[i]+'</h2><button type="button" data-sh="'+s.k+'">'+(i?"See all":"Xem tất cả")+' →</button></div><div class="srow">'+l.map(card).join("")+'</div></section>';
  }).join("");
}
$("shelves").addEventListener("click",function(e){
  if(e.target.closest("button[data-sh]")===null){var oc=e.target.closest("[data-open]");if(oc){openBook(oc.dataset.open);return}}
  var f=e.target.closest(".fav");
  if(f){var k=st.saved.indexOf(f.dataset.id);if(k<0)st.saved.push(f.dataset.id);else st.saved.splice(k,1);saveLS("rv.saved",st.saved);render();return}
  var b=e.target.closest("button[data-sh]");if(!b)return;
  var s=SHELVES.filter(function(x){return x.k===b.dataset.sh})[0];
  st.f=s.f||"all";st.sr=s.sr||"all";st.md=s.md||"all";st.an="";st.ty=s.ty||"all";st.er=s.er||"all";st.limit=PAGE;
  [].forEach.call($("fmt").children,function(c){c.setAttribute("aria-pressed",c.dataset.f===st.f)});
  buildAuthors();render();window.scrollTo(0,0);
});
var TILES = RV.TILES || [
  ["tieng-viet.html","Đọc sách tiếng Việt","Read in Vietnamese","Đọc ngay, không cần dịch","Ready to read, no translation needed"],
  ["chu-de/","Tìm hiểu một chủ đề","Explore a topic","Ân điển, Hội Thánh, cầu nguyện…","Grace, church, prayer…"],
  ["sach-noi.html","Nghe sách nói","Listen","Nghe khi đi đường","Listen on the go"],
  ["hom-nay.html","Bài đọc hôm nay","Today's reading","Mỗi ngày một đoạn ngắn","One short passage a day"]
];
function renderTiles(){var i=st.lang==="vi"?0:1;
  var ic=function(k){return'<svg class="ti" viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 19a2 2 0 100-4 2 2 0 000 4zM19 9a2 2 0 100-4 2 2 0 000 4zM7 17h6a3 3 0 000-6h-2a3 3 0 010-6h6"/></svg>'};
  $("tiles").innerHTML='<h2 class="gh">'+(i?"Where would you like to start?":"Bạn muốn bắt đầu từ đâu?")+'</h2>'+'<a class="tile first" href="moi-tin-chua.html">'+ic("moi-tin-chua.html")+'<span class="step">'+(i?"Step 1":"Bước 1")+'</span><b>'+(i?"I’m new to faith":"Tôi mới tin Chúa")+'</b><span>'+(i?"A gentle path with clear teaching.":"Lộ trình nhẹ, dạy rõ và dễ theo.")+'</span></a>' + TILES.map(function(t){return'<a class="tile" href="'+t[0]+'">'+ic(t[0])+'<b>'+t[1+i]+'</b><span>'+t[3+i]+'</span></a>'}).join("");
  var P=[["moi-tin-chua.html","Mới tin Chúa","New believer"],["lo-trinh.html","Lộ trình đọc","Reading path"],["tieng-viet.html","Sách tiếng Việt","Vietnamese"],["sach-noi.html","Sách nói","Audiobooks"]];
  $("nl").innerHTML=P.map(function(m){return'<a href="'+m[0]+'">'+m[1+i]+'</a>'}).join("");
  var M=[["hom-nay.html","Hôm nay","Today"],["khoa-hoc.html","Học trực tuyến","Online study"],["trich-dan.html","Trích dẫn","Quotes"],["thuat-ngu.html","Thuật ngữ","Glossary"],["cai-chanh-la-gi.html","Cải Chánh là gì?","What is Reformed?"]];
  $("mx").innerHTML=M.map(function(m){return'<a class="btn" href="'+m[0]+'">'+m[1+i]+'</a>'}).join("");
}
$("browse").addEventListener("click",function(){st.br=1;st.limit=PAGE;render();window.scrollTo(0,0)});
$("grid").addEventListener("click",function(e){if(e.target.closest(".fav"))return;var oc=e.target.closest("[data-open]");if(oc)openBook(oc.dataset.open)});
document.addEventListener("keydown",function(e){if((e.key==="Enter"||e.key===" ")&&e.target.matches&&e.target.matches(".book[data-open]")){e.preventDefault();openBook(e.target.dataset.open)}});
$("bk").addEventListener("click",function(e){
  var sb=e.target.closest("[data-share]");if(sb){var sbk=BOOKS.filter(function(z){return z.id===sb.dataset.share})[0],su=location.origin+"/?b="+encodeURIComponent(sb.dataset.share),stt=sbk?(sbk[st.lang]||sbk.en).t:sb.dataset.share;navigator.clipboard&&navigator.clipboard.writeText(su).catch(function(){});alert(st.lang==="vi"?"Liên kết đã được sao chép: "+su:"Link copied: "+su);return}
  if(e.target===$("bk")||e.target.closest(".bk-x")){$("bk").close();return}
  var f=e.target.closest(".fav");
  if(f){var k=st.saved.indexOf(f.dataset.id);if(k<0)st.saved.push(f.dataset.id);else st.saved.splice(k,1);saveLS("rv.saved",st.saved);openBook(curBk);render()}
});
$("bk").addEventListener("change",function(e){
  var s=e.target.closest("select[data-pid]");
  if(s){var id=s.dataset.pid,v=s.value,cur=prog(id);st.prog[id]={s:v,p:v==="done"?100:v==="todo"?0:(cur.p||0),t:Date.now()};if(v==="todo")delete st.prog[id];saveLS("rv.prog",st.prog);openBook(curBk);render();return}
  var r=e.target.closest("input[data-rid]");if(r)render();
});
$("bk").addEventListener("input",function(e){
  var r=e.target.closest("input[data-rid]");if(!r)return;
  var id=r.dataset.rid,p=+r.value;st.prog[id]={s:p>=100?"done":"reading",p:p,t:Date.now()};r.nextElementSibling.textContent=p+"%";saveLS("rv.prog",st.prog);
});
(function(){var br=document.querySelector(".brand");br.style.cursor="pointer";br.addEventListener("click",function(){$("clear").click();window.scrollTo(0,0)})})();

;fetch("subscribe.json").then(function(r){return r.json()}).then(function(j){var e=document.getElementById("sub");if(j&&/^https:\/\//.test(j.url)&&e){e.href=j.url;e.hidden=false}}).catch(function(){})

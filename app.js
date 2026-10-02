var util = window.RV_UTILS || {};
var stateUtil = window.RV_STATE_UTILS || window.RV_UTILS || {};
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
var SRCS = (window.RV_CONFIG && RV_CONFIG.SRCS) || ["ccel","vn","mg","ia","pg","lv","dg","lig","other"],
    MEDIA = (window.RV_CONFIG && RV_CONFIG.MEDIA) || ["read","pdf","epub","audio"],
    AUDIO = {};
var $=function(i){return document.getElementById(i)};
var PAGE=48;
var DESC={},START=[];
var BOOKS=[],AUTHORS=[];
var st = (stateUtil.getInitialState ? stateUtil.getInitialState() : {
  f:"all",q:"",an:"",sr:"all",md:"all",ty:"all",er:"all",so:"0",limit:PAGE,saved:[],prog:{},lang:"vi"
});
var TYPES = (window.RV_CONFIG && RV_CONFIG.TYPES) || ["systematic","commentary","sermons","devotional","doctrine","catechism","history","collected","bible","classic"];
var ERAS = (window.RV_CONFIG && RV_CONFIG.ERAS) || ["anc","ref","pur","aw","mod","c20"];
var ERAMID={anc:1000,ref:1550,pur:1650,aw:1750,mod:1850,c20:1950};
function saveLS(k,v){
  if(util.saveLS){return util.saveLS(k,v);} 
  try{localStorage.setItem(k,JSON.stringify(v))}catch(e){}
}
function esc(s){
  if(util.esc){return util.esc(s);} 
  return String(s).replace(/[&<>\"]/g,function(c){return{"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;"}[c]});
}
function tx(k){return T[st.lang][k]}
function srcOf(b){ return util.srcOf ? util.srcOf(b) : (b.read?"ccel":(b.au||"other")); }
function hasM(b,m){
  if(util.hasM){return util.hasM(b,m);} 
  if(m==="read")return!!b.read||!!rdr(b);if(m==="pdf")return!!b.pdf||!!(b.dl&&(b.dl.PDF||b.dl.pdf));if(m==="epub")return!!b.epub||!!(b.dl&&(b.dl.EPUB||b.dl.epub));if(m==="audio")return!!(b.listen||b.audio||b.au==="lv"||(b.dl&&(b.dl.audio||b.dl.AUDIO)));return false;
}
function typeOf(title,key,over){
  if(util.typeOf){return util.typeOf(title,key,over);} 
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
function eraOf(y){
  if(util.eraOf){return util.eraOf(y);} 
  return y<1500?"anc":y<1600?"ref":y<1700?"pur":y<1800?"aw":y<1900?"mod":"c20";
}

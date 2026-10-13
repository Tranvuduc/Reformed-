(function () {
  "use strict";
  var $ = function (i) { return document.getElementById(i); };
  var PL = [[41,1],[41,2],[41,3],[41,4],[41,5],[41,6],[41,8],[41,9],[41,10],[41,12],[41,14],[41,15],[41,16],[43,1],[43,3],[43,4],[43,6],[43,10],[43,11],[43,13],[43,14],[43,15],[43,17],[43,19],[43,20],[19,23],[19,1],[19,100],[19,121],[45,3],[45,5],[45,8],[49,2],[50,4],[48,2],[56,3]];
  var NM = ["","Sáng Thế Ký","Xuất Ê-díp-tô Ký","Lê-vi Ký","Dân Số Ký","Phục Truyền","Giô-suê","Các Quan Xét","Ru-tơ","1 Sa-mu-ên","2 Sa-mu-ên","1 Các Vua","2 Các Vua","1 Sử Ký","2 Sử Ký","Ê-xơ-ra","Nê-hê-mi","Ê-xơ-tê","Gióp","Thi Thiên","Châm Ngôn","Truyền Đạo","Nhã Ca","Ê-sai","Giê-rê-mi","Ca Thương","Ê-xê-chi-ên","Đa-ni-ên","Ô-sê","Giô-ên","A-mốt","Áp-đia","Giô-na","Mi-chê","Na-hum","Ha-ba-cúc","Sô-phô-ni","A-ghê","Xa-cha-ri","Ma-la-chi","Ma-thi-ơ","Mác","Lu-ca","Giăng","Công Vụ","Rô-ma","1 Cô-rinh-tô","2 Cô-rinh-tô","Ga-la-ti","Ê-phê-sô","Phi-líp","Cô-lô-se","1 Tê-sa-lô-ni-ca","2 Tê-sa-lô-ni-ca","1 Ti-mô-thê","2 Ti-mô-thê","Tít","Phi-lê-môn","Hê-bơ-rơ","Gia-cơ","1 Phi-e-rơ","2 Phi-e-rơ","1 Giăng","2 Giăng","3 Giăng","Giu-đe","Khải Huyền"];
  var KIDS = ["Hôm nay có điều gì làm con vui? Chúa muốn con cảm ơn Ngài về điều gì?", "Trong đoạn vừa đọc, ai là người làm con ngạc nhiên nhất? Vì sao?", "Chúa Giê-xu đã làm gì cho chúng ta trong đoạn này?", "Có điều nào con chưa hiểu? Cả nhà cùng hỏi mục sư hoặc tìm trong Kinh Thánh nhé.", "Con muốn xin Chúa giúp gì cho bạn bè hoặc người thân?", "Có việc nào hôm nay con làm chưa đúng? Chúa sẵn sàng tha thứ khi con xưng tội.", "Con có thể nói điều tốt gì với một người trong nhà hôm nay?"];
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  var d = new Date(), doy = Math.floor((d - new Date(d.getFullYear(), 0, 0)) / 864e5), off = 0;
  function day() { return doy + off; }
  async function render() {
    var n = day(), p = PL[(n - 1 + PL.length * 100) % PL.length], H = window.RV_G;
    $("dt").textContent = off === 0 ? "Hôm nay" : off === 1 ? "Ngày mai" : off === -1 ? "Hôm qua" : "Ngày " + (off > 0 ? "+" : "") + off;
    $("rd").textContent = NM[p[0]] + " " + p[1]; $("tx").textContent = "Đang tải…";
    try {
      var r = await fetch("https://api.getbible.net/v2/vietnamese/" + p[0] + "/" + p[1] + ".json"), j = await r.json(), vs = (j.verses || []).map(function (v) { return v.verse + " " + (v.text || "").replace(/Ð/g, "Đ").replace(/ð/g, "đ").trim(); });
      $("tx").innerHTML = vs.slice(0, 22).map(function (v) { return "<p style='margin:.35em 0'>" + esc(v) + "</p>"; }).join("") + (vs.length > 22 ? "<p class='m'>… (đọc tiếp trong Kinh Thánh của bạn, " + vs.length + " câu)</p>" : "");
    } catch (e) { $("tx").textContent = "Không tải được. Hãy mở Kinh Thánh của bạn đến " + NM[p[0]] + " " + p[1] + "."; }
    var q = H[(n - 1 + H.length * 100) % H.length]; $("hq").textContent = "Hỏi " + q[0] + ". " + q[1]; $("ha").textContent = q[2];
    $("kq").textContent = KIDS[(n - 1 + 700) % KIDS.length];
  }
  $("pv").onclick = function () { off--; render(); }; $("nx").onclick = function () { off++; render(); }; $("td").onclick = function () { off = 0; render(); };
  fetch("/giao-ly.json").then(function (r) { return r.json(); }).then(function (j) { window.RV_G = j.h; render(); }).catch(function () { $("tx").textContent = "Không tải được dữ liệu."; });
})();

(function () {
  "use strict";
  var $ = function (i) { return document.getElementById(i); }, E = window.RV_EV, MN = ["", "tháng 1", "tháng 2", "tháng 3", "tháng 4", "tháng 5", "tháng 6", "tháng 7", "tháng 8", "tháng 9", "tháng 10", "tháng 11", "tháng 12"];
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function li(e) { return "<li><b>" + e[1] + " " + MN[e[0]] + " " + e[2] + "</b> · " + esc(e[3]) + (e[4] ? ' <a href="' + e[4] + '">Xem thêm</a>' : "") + "</li>"; }
  var n = new Date(), m = n.getMonth() + 1, d = n.getDate(), t = E.filter(function (e) { return e[0] === m && e[1] === d; });
  $("dt").textContent = "Ngày " + d + " " + MN[m] + " " + n.getFullYear();
  $("td").innerHTML = t.length ? t.map(li).join("") : "<li class='m'>Chưa có mốc nào cho hôm nay trong danh sách của chúng tôi. Xem các ngày sắp tới bên dưới.</li>";
  var up = []; for (var k = 1; k <= 30; k++) { var x = new Date(n.getFullYear(), n.getMonth(), n.getDate() + k); E.forEach(function (e) { if (e[0] === x.getMonth() + 1 && e[1] === x.getDate()) up.push(e); }); }
  $("up").innerHTML = up.length ? up.map(li).join("") : "<li class='m'>Không có mốc nào trong 30 ngày tới.</li>";
  $("all").innerHTML = E.slice().sort(function (a, b) { return a[0] - b[0] || a[1] - b[1]; }).map(li).join("");
})();

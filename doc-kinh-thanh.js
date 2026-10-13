(function () {
  "use strict";
  var $ = function (i) { return document.getElementById(i); }, META = null, KT = {};
  var CH = [50,40,27,36,34,24,21,4,31,24,22,25,29,36,10,13,10,42,150,31,12,8,66,52,5,48,12,14,3,9,1,4,7,3,3,3,2,14,4,28,16,24,21,28,16,16,13,6,6,4,4,5,3,6,4,3,1,13,5,5,3,5,1,1,1,22];
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function meta() { return META ? Promise.resolve(META) : fetch("/search-meta.json").then(function (r) { return r.json(); }).then(function (j) { return META = j; }); }
  function expand(vs) { var o = {}; (vs || []).forEach(function (v) { var m = String(v).split("–"), a = +m[0], b = +(m[1] || m[0]); for (var i = a; i <= b && i - a < 80; i++) o[i] = 1; }); return o; }
  function bible(n, c) {
    return fetch("https://api.getbible.net/v2/vietnamese/" + n + "/" + c + ".json").then(function (r) { if (!r.ok) throw 0; return r.json(); }).then(function (j) { return (j.verses || []).map(function (v) { return [v.verse, (v.text || "").replace(/Ð/g, "Đ").replace(/ð/g, "đ").trim()]; }); });
  }
  function kt(n) { return KT[n] || (KT[n] = fetch("/kt/" + n + ".json").then(function (r) { return r.ok ? r.json() : {}; }).catch(function () { return {}; })); }
  async function show() {
    var n = +$("bk").value, c = +$("ch").value, M = await meta();
    $("st").textContent = "Đang tải…"; $("tx").innerHTML = ""; $("who").innerHTML = "";
    var res = await Promise.all([bible(n, c).catch(function () { return null; }), kt(n)]);
    var vs = res[0], ent = (res[1][String(c)] || []);
    if (!vs) { $("st").textContent = "Không tải được bản Kinh Thánh. Kiểm tra kết nối mạng rồi thử lại."; return; }
    var cited = {}; ent.forEach(function (e) { var ex = expand(e[2]); for (var k in ex) (cited[k] = cited[k] || []).push(e); });
    $("st").textContent = ent.length ? ent.length + " sách trong thư viện đã trích dẫn chương này. Câu có dấu • được nhắc tới; nhấn vào số câu để xem sách nào." : "Chưa có sách nào trong thư viện trích dẫn chương này.";
    $("tx").innerHTML = vs.map(function (v) { var k = cited[v[0]]; return '<p class="vs"><a href="#" data-v="' + v[0] + '" class="vn' + (k ? " ci" : "") + '">' + v[0] + (k ? "•" : "") + "</a> " + esc(v[1]) + "</p>"; }).join("");
    function list(es, label, noCount) {
      $("who").innerHTML = "<h2>" + label + "</h2><ul class='rs'>" + es.map(function (e) { var b = M.b[e[0]]; return '<li><a href="/reader.html?id=vn/' + b[0] + "&at=" + encodeURIComponent(e[3]) + '">' + esc(b[1]) + "</a> · " + esc(b[2]) + ' <span class="stt">(' + e[1] + " lần)</span></li>"; }).join("") + "</ul>";
    }
    if (ent.length) list(ent.slice(0, 25), "Sách đã trích dẫn chương này");
    $("tx").onclick = function (e) { var a = e.target.closest("a[data-v]"); if (!a) return; e.preventDefault(); var v = +a.dataset.v, k = cited[v]; if (k) list(k, "Sách đã trích dẫn câu " + v, true); else $("who").innerHTML = "<p class='m'>Chưa có sách nào trích riêng câu " + v + ".</p>"; };
  }
  function fillCh() { var n = +$("bk").value, h = ""; for (var i = 1; i <= CH[n - 1]; i++) h += '<option value="' + i + '">Chương ' + i + "</option>"; $("ch").innerHTML = h; }
  $("bk").onchange = function () { fillCh(); show(); }; $("ch").onchange = show;
  $("pv").onclick = function () { var c = +$("ch").value; if (c > 1) { $("ch").value = c - 1; show(); } };
  $("nx").onclick = function () { var c = +$("ch").value; if (c < CH[+$("bk").value - 1]) { $("ch").value = c + 1; show(); } };
  var h = (location.hash || "").match(/#(\d+)-(\d+)/); $("bk").value = h ? h[1] : 45; fillCh(); if (h) $("ch").value = h[2]; else $("ch").value = 8; show();
})();

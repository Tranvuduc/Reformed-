(function () {
  "use strict";
  var $ = function (i) { return document.getElementById(i); }, T = {}, ALL = [];
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function anchor(t) { var a = t.slice(0, 46); if (t.length > 46 && a.indexOf(" ") > 0 && a.slice(-1) !== " ") a = a.slice(0, a.lastIndexOf(" ")); return a.trim(); }
  var COL = ["Vàng", "Xanh", "Hồng"];
  function collect() {
    ALL = [];
    try { for (var i = 0; i < localStorage.length; i++) { var k = localStorage.key(i); if (k.indexOf("rv.hl.") !== 0) continue; var id = k.slice(6), arr = []; try { arr = JSON.parse(localStorage.getItem(k) || "[]"); } catch (e) { } arr.filter(function (h) { return !h.d; }).forEach(function (h) { ALL.push({ id: id, h: h }); }); } } catch (e) { }
    ALL.sort(function (a, b) { return (b.h.t || 0) - (a.h.t || 0); });
  }
  function title(id) { var s = id.replace(/^vn\//, ""); return T[s] ? T[s].t + " · " + T[s].a : id; }
  function render() {
    var by = {}; ALL.forEach(function (x) { (by[x.id] = by[x.id] || []).push(x.h); });
    var ids = Object.keys(by);
    $("st").textContent = ALL.length ? ALL.length + " đoạn đã đánh dấu trong " + ids.length + " sách (chỉ có trên thiết bị này)." : "Chưa có đoạn nào được đánh dấu trên thiết bị này. Khi đọc, hãy chạm vào một đoạn trong trình đọc để tô màu hoặc ghi chú.";
    $("ls").innerHTML = ids.map(function (id) { return "<section class='nc'><h2>" + esc(title(id)) + "</h2><ul>" + by[id].sort(function (a, b) { return a.g - b.g; }).map(function (h) { return "<li><a href='/reader.html?id=" + encodeURIComponent(id).replace(/%2F/g, "/") + "&at=" + encodeURIComponent(anchor(h.q || "")) + "'>" + esc((h.q || "").slice(0, 160)) + "</a>" + (h.n ? "<br><b>Ghi chú:</b> " + esc(h.n) : "") + " <span class='stt'>(" + (COL[h.c || 0] || "") + ")</span></li>"; }).join("") + "</ul></section>"; }).join("");
  }
  function text() {
    var by = {}; ALL.forEach(function (x) { (by[x.id] = by[x.id] || []).push(x.h); });
    var o = "SỔ HỌC CỦA TÔI\nXuất từ Reformed Vietnam · " + new Date().toLocaleDateString("vi-VN") + "\n\n";
    Object.keys(by).forEach(function (id) { o += "## " + title(id) + "\n\n"; by[id].sort(function (a, b) { return a.g - b.g; }).forEach(function (h) { o += "> " + (h.q || "").replace(/\s+/g, " ") + "\n"; if (h.n) o += "Ghi chú: " + h.n + "\n"; o += "\n"; }); });
    return o;
  }
  $("ex").onclick = function () { var b = new Blob([text()], { type: "text/plain;charset=utf-8" }), a = document.createElement("a"); a.href = URL.createObjectURL(b); a.download = "so-hoc-reformed-vietnam.txt"; document.body.appendChild(a); a.click(); setTimeout(function () { a.remove(); URL.revokeObjectURL(a.href); }, 3000); };
  $("cp").onclick = function () { var t = text(); (navigator.clipboard ? navigator.clipboard.writeText(t) : Promise.reject()).then(function () { $("st").textContent = "Đã sao chép."; }).catch(function () { $("st").textContent = "Không sao chép được. Hãy dùng nút Tải về."; }); };
  fetch("/tai-sach.json").then(function (r) { return r.json(); }).then(function (l) { l.forEach(function (b) { T[b.s] = b; }); }).catch(function () { }).then(function () { collect(); render(); });
})();

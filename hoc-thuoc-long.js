(function () {
  "use strict";
  var $ = function (i) { return document.getElementById(i); }, V = window.RV_VERSES, INT = [0, 1, 3, 7, 14, 30], S = {}, cur = null, txt = {}, dayMs = 864e5;
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function load() { try { S = JSON.parse(localStorage.getItem("rv.mem") || "{}"); } catch (e) { S = {}; } }
  function save() { try { localStorage.setItem("rv.mem", JSON.stringify(S)); } catch (e) { } }
  function today() { return Math.floor(Date.now() / dayMs); }
  function verse(v) {
    if (txt[v.r]) return Promise.resolve(txt[v.r]);
    return fetch("https://api.getbible.net/v2/vietnamese/" + v.b + "/" + v.c + ".json").then(function (r) { if (!r.ok) throw 0; return r.json(); }).then(function (j) {
      var t = (j.verses || []).filter(function (x) { return x.verse >= v.v[0] && x.verse <= v.v[1]; }).map(function (x) { return x.text.replace(/Ð/g, "Đ").replace(/ð/g, "đ").trim(); }).join(" ");
      if (!t) throw 0; return txt[v.r] = t;
    });
  }
  function due() { var t = today(); return V.filter(function (v) { var s = S[v.r]; return s && s.d <= t; }); }
  function fresh() { return V.filter(function (v) { return !S[v.r]; }); }
  function stats() {
    var n = Object.keys(S).length, m = V.filter(function (v) { return S[v.r] && S[v.r].b >= 5; }).length;
    $("sum").textContent = "Đang học: " + n + "/" + V.length + " câu · đã thuộc vững: " + m + " · đến hạn ôn hôm nay: " + due().length;
  }
  function hint(t, mode) { if (mode === "full") return esc(t); return t.split(/\s+/).map(function (w, i) { return mode === "half" && i % 2 ? "____" : (mode === "first" ? esc(w[0]) + "…" : esc(w)); }).join(" "); }
  async function next(forceNew) {
    var d = due(), pool = d.length && !forceNew ? d : fresh();
    if (!pool.length) { $("card").hidden = true; $("done").hidden = false; $("done").textContent = d.length ? "" : "Hôm nay đã ôn xong. Hãy quay lại ngày mai! Bạn có thể thêm câu mới bằng nút bên dưới."; stats(); return; }
    $("done").hidden = true; $("card").hidden = false; cur = pool[0]; $("ref").textContent = cur.r; $("tv").textContent = ""; $("rt").hidden = false; $("lv").hidden = true;
    stats();
    try { var t = await verse(cur); cur.t = t; $("tv").innerHTML = hint(t, $("md").value); } catch (e) { $("tv").textContent = "Không tải được câu Kinh Thánh. Kiểm tra mạng rồi thử lại."; }
  }
  function mark(ok) {
    var s = S[cur.r] || { b: 0 }, t = today();
    s.b = ok ? Math.min(5, s.b + 1) : 1; s.d = t + INT[s.b]; S[cur.r] = s; save(); next();
  }
  $("rt").onclick = function () { if (cur.t) { $("tv").innerHTML = esc(cur.t); } $("rt").hidden = true; $("lv").hidden = false; };
  $("ok").onclick = function () { mark(true); }; $("no").onclick = function () { mark(false); };
  $("add").onclick = function () { next(true); };
  $("md").onchange = function () { if (cur && cur.t) $("tv").innerHTML = hint(cur.t, $("md").value); };
  $("lv").hidden = true; load();
  document.getElementById("ls").innerHTML = V.map(function (v) { return "<li>" + esc(v.r) + "</li>"; }).join("");
  next();
})();

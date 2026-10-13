(function () {
  "use strict";
  var $ = function (i) { return document.getElementById(i); }, META = null, shardCache = {}, txtCache = {};
  function fold(s) { return String(s).toLowerCase().replace(/đ/g, "d").normalize("NFD").replace(/[̀-ͯ]/g, ""); }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function meta() { return META ? Promise.resolve(META) : fetch("/search-meta.json").then(function (r) { return r.json(); }).then(function (j) { j.stopSet = {}; j.stop.forEach(function (w) { j.stopSet[w] = 1; }); return META = j; }); }
  function shard(k, dir) {
    var ck = dir + k;
    if (shardCache[ck]) return shardCache[ck];
    return shardCache[ck] = fetch("/" + dir + "/" + k + ".bin").then(function (r) { return r.ok ? r.arrayBuffer() : new ArrayBuffer(0); }).then(function (ab) {
      var u = new Uint8Array(ab), i = 0, map = {}, dec = new TextDecoder();
      function vi() { var n = 0, sh = 0, b; do { b = u[i++]; n += (b & 127) * Math.pow(2, sh); sh += 7; } while (b & 128); return n; }
      while (i < u.length) { var wl = u[i++], w = dec.decode(u.subarray(i, i + wl)); i += wl; var c = vi(), p = [], prev = 0; for (var j = 0; j < c; j++) { prev += vi(); p.push(prev); } map[w] = p; }
      return map;
    });
  }
  function key(w) { return Array.from(w).slice(0, 2).map(function (c) { return c.codePointAt(0).toString(16); }).join("-"); }
  function nl(s) { return String(s).normalize("NFC").toLowerCase(); }
  function postings(t) { return shard(key(t), "s").then(function (m) { return m[t] || []; }); }
  function bpost(t) { return shard(key(t), "s2").then(function (m) { return m[t] || null; }); }
  function inter(a, b) { var o = [], i = 0, j = 0; while (i < a.length && j < b.length) { if (a[i] === b[j]) { o.push(a[i]); i++; j++; } else if (a[i] < b[j]) i++; else j++; } return o; }
  function getSec(stem, a, b) { return fetch("/txt/" + stem + ".txt", { headers: { Range: "bytes=" + a + "-" + (b - 1) } }).then(function (r) { return r.arrayBuffer().then(function (ab) { var u = new Uint8Array(ab); if (r.status !== 206) u = u.subarray(a, b); return new TextDecoder().decode(u); }); }); }
  function anchor(t) { var a = t.slice(0, 46); if (t.length > 46 && a.indexOf(" ") > 0 && a.slice(-1) !== " ") a = a.slice(0, a.lastIndexOf(" ")); return a.trim(); }
  async function run(q) {
    var M = await meta(), all = nl(q).match(/[\p{L}\p{N}]+/gu) || [], toks = all.filter(function (w) { return w.length >= 2; });
    var res = null;
    if (all.length >= 2) {
      var bis = []; for (var b0 = 0; b0 + 1 < all.length; b0++) bis.push(all[b0] + " " + all[b0 + 1]);
      var bl = (await Promise.all(bis.map(bpost))).filter(function (x) { return x; });
      if (bl.length) { bl.sort(function (a, b) { return a.length - b.length; }); res = bl[0]; for (var z = 1; z < bl.length && res.length; z++) res = inter(res, bl[z]); }
      if (res && !res.length && bl.length === bis.length) { $("st").textContent = "Không tìm thấy cụm từ này. Hãy thử ít từ hơn."; $("rs").innerHTML = ""; return; }
    }
    if (!res) {
      var use = toks.filter(function (w) { return !M.stopSet[w]; });
      if (!use.length) { $("st").textContent = toks.length ? "Các từ này xuất hiện ở rất nhiều đoạn nên chưa tìm được. Hãy thêm một từ hiếm hơn (tên riêng, thuật ngữ cụ thể)." : "Hãy gõ ít nhất một từ (có dấu tiếng Việt)."; $("rs").innerHTML = ""; return; }
      $("st").textContent = "Đang tìm…";
      var lists = await Promise.all(use.map(postings)); lists.sort(function (a, b) { return a.length - b.length; });
      res = lists[0]; for (var i = 1; i < lists.length && res.length; i++) res = inter(res, lists[i]);
    }
    var use = all.map(fold);
    if (!res.length) { $("st").textContent = "Không tìm thấy đoạn nào chứa tất cả các từ này."; $("rs").innerHTML = ""; return; }
    var total = res.length, cand = res.slice(0, 120), phrase = fold(nl(q)).replace(/[^a-z0-9]+/g, " ").trim(), out = [];
    $("st").textContent = "Đang kiểm tra " + cand.length + " đoạn…";
    for (var k0 = 0; k0 < cand.length; k0 += 12) {
      var got = await Promise.all(cand.slice(k0, k0 + 12).map(function (id) { var sec = M.s[id], stem = M.b[sec[0]][0]; return getSec(stem, sec[1], sec[2]).then(function (txt) { return { sec: sec, stem: stem, txt: txt }; }).catch(function () { return null; }); }));
      got.forEach(function (o) { if (!o) return; var f = " " + fold(o.txt).replace(/[^a-z0-9]+/g, " ") + " ", n = 0, p0 = 0, x; while ((x = f.indexOf(" " + phrase + " ", p0)) >= 0) { n++; p0 = x + 1; } o.exact = n > 0; o.score = n ? 100 + n : 0; if (n || all.length < 2) out.push(o); else out.push(o); });
    }
    var anyExact = out.some(function (o) { return o.exact; });
    if (anyExact) out = out.filter(function (o) { return o.exact; });
    out = out.slice(0, 200);
    out.sort(function (a, b) { return b.score - a.score; });
    $("st").textContent = anyExact ? "Có " + out.length + " đoạn chứa đúng cụm từ" + (total > cand.length ? " (trong " + cand.length + " đoạn đầu số " + total + " đoạn liên quan)" : "") + "." : "Có " + total + " đoạn chứa các từ này" + (all.length > 1 ? " (không thấy cụm từ liền nhau trong " + cand.length + " đoạn đầu)" : "") + ". Hiện " + Math.min(out.length, 40) + " đoạn đầu.";
    out = out.slice(0, 40);
    $("rs").innerHTML = out.map(function (o) {
      var plain = o.txt.replace(/[#*]+/g, "").replace(/\s+/g, " "), fp = fold(plain), at = 0, best = -1;
      /* tìm vị trí từ đầu tiên (theo chữ không dấu, cùng độ dài) */
      if (fp.length === plain.length) { best = fp.indexOf(use[0]); if (o.exact) { var pp = fp.replace(/[^a-z0-9]+/g, " ").indexOf(phrase); } }
      if (best < 0) best = 0; at = Math.max(0, best - 140);
      var sn = plain.slice(at, at + 420), hi = esc(sn);
      use.forEach(function (w) { }); 
      var fsn = fold(sn), marks = [];
      if (fsn.length === sn.length) use.forEach(function (w) { var p = 0, x; while ((x = fsn.indexOf(w, p)) >= 0) { marks.push([x, x + w.length]); p = x + w.length; } });
      marks.sort(function (a, b) { return a[0] - b[0]; });
      var h = "", last = 0; marks.forEach(function (m) { if (m[0] < last) return; h += esc(sn.slice(last, m[0])) + "<mark>" + esc(sn.slice(m[0], m[1])) + "</mark>"; last = m[1]; }); h += esc(sn.slice(last)); if (marks.length) hi = h;
      var first = o.txt.split(/\n[ \t]*\n/)[0].replace(/\s+/g, " ").trim(), b = M.b[o.sec[0]];
      return '<li style="margin:.9em 0"><a href="/reader.html?id=vn/' + b[0] + "&at=" + encodeURIComponent(anchor(first)) + '"><b>' + esc(b[1]) + "</b></a> · " + esc(b[2]) + (o.exact ? ' <span class="stt">(khớp cụm từ)</span>' : "") + '<br><span class="stt" style="opacity:.9">' + (at ? "… " : "") + hi + " …</span></li>";
    }).join("");
  }
  $("f").onsubmit = function (e) { e.preventDefault(); var q = $("q").value.trim(); if (q) { history.replaceState(null, "", "#" + encodeURIComponent(q)); run(q).catch(function () { $("st").textContent = "Lỗi khi tìm. Hãy thử lại."; }); } };
  var h = decodeURIComponent((location.hash || "").slice(1)); if (h) { $("q").value = h; $("f").onsubmit(new Event("submit")); }
})();

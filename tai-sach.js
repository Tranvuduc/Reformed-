/* Tải sách về máy: tạo EPUB ngay trong trình duyệt từ /txt/<slug>.txt, đóng gói ZIP theo phần. Không gửi dữ liệu đi đâu. */
(function () {
  "use strict";
  var $ = function (i) { return document.getElementById(i); };
  var enc = new TextEncoder();
  var LIST = [], SEL = {}, busy = false;

  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function fold(s) { return String(s).toLowerCase().replace(/đ/g, "d").normalize("NFD").replace(/[̀-ͯ]/g, ""); }
  function fmtMB(n) { return n >= 1048576 ? (n / 1048576).toFixed(1) + " MB" : Math.max(1, Math.round(n / 1024)) + " KB"; }

  /* ---------- CRC32 + ZIP ---------- */
  var CT = (function () { var t = new Uint32Array(256); for (var n = 0; n < 256; n++) { var c = n; for (var k = 0; k < 8; k++) c = c & 1 ? 0xEDB88320 ^ (c >>> 1) : c >>> 1; t[n] = c >>> 0; } return t; })();
  function crc32(u) { var c = 0xFFFFFFFF; for (var i = 0; i < u.length; i++) c = CT[(c ^ u[i]) & 255] ^ (c >>> 8); return (c ^ 0xFFFFFFFF) >>> 0; }
  var canDeflate = typeof CompressionStream === "function";
  function deflate(u) {
    return new Response(new Blob([u]).stream().pipeThrough(new CompressionStream("deflate-raw"))).arrayBuffer().then(function (b) { return new Uint8Array(b); });
  }
  function u16(v, o, n) { v[o] = n & 255; v[o + 1] = (n >>> 8) & 255; }
  function u32(v, o, n) { v[o] = n & 255; v[o + 1] = (n >>> 8) & 255; v[o + 2] = (n >>> 16) & 255; v[o + 3] = (n >>> 24) & 255; }
  /* files: [{name, data:Uint8Array, store:boolean}] -> Blob */
  async function zip(files, mime) {
    var parts = [], central = [], off = 0, d = new Date();
    var dt = ((d.getHours() << 11) | (d.getMinutes() << 5) | (d.getSeconds() >> 1)) & 0xFFFF;
    var dd = (((d.getFullYear() - 1980) << 9) | ((d.getMonth() + 1) << 5) | d.getDate()) & 0xFFFF;
    for (var i = 0; i < files.length; i++) {
      var f = files[i], name = enc.encode(f.name), raw = f.data, comp = raw, method = 0;
      if (!f.store && canDeflate && raw.length > 120) { try { var z = await deflate(raw); if (z.length < raw.length) { comp = z; method = 8; } } catch (e) { } }
      var crc = crc32(raw), lh = new Uint8Array(30 + name.length);
      u32(lh, 0, 0x04034b50); u16(lh, 4, 20); u16(lh, 6, 0x0800); u16(lh, 8, method); u16(lh, 10, dt); u16(lh, 12, dd);
      u32(lh, 14, crc); u32(lh, 18, comp.length); u32(lh, 22, raw.length); u16(lh, 26, name.length); u16(lh, 28, 0); lh.set(name, 30);
      var ch = new Uint8Array(46 + name.length);
      u32(ch, 0, 0x02014b50); u16(ch, 4, 20); u16(ch, 6, 20); u16(ch, 8, 0x0800); u16(ch, 10, method); u16(ch, 12, dt); u16(ch, 14, dd);
      u32(ch, 16, crc); u32(ch, 20, comp.length); u32(ch, 24, raw.length); u16(ch, 28, name.length); u32(ch, 42, off); ch.set(name, 46);
      parts.push(lh, comp); central.push(ch); off += lh.length + comp.length;
    }
    var cs = 0; central.forEach(function (c) { cs += c.length; });
    var end = new Uint8Array(22); u32(end, 0, 0x06054b50); u16(end, 8, files.length); u16(end, 10, files.length); u32(end, 12, cs); u32(end, 16, off);
    return new Blob(parts.concat(central, [end]), { type: mime || "application/zip" });
  }

  /* ---------- Văn bản -> XHTML ---------- */
  function inline(s) {
    s = esc(s);
    s = s.replace(/\*\*([^*\n]+?)\*\*/g, "<strong>$1</strong>").replace(/(^|[^*\w])\*([^*\n]+?)\*(?![*\w])/g, "$1<em>$2</em>");
    return s;
  }
  function isCaps(t) { return /[A-ZÀ-Ỹ]{3}/.test(t) && t === t.toUpperCase(); }
  function parse(txt, title) {
    txt = txt.replace(/\r/g, "").replace(/^﻿/, "");
    var raw = txt.split(/\n[ \t]*\n/), blocks = [];
    raw.forEach(function (r) {
      var lines = r.split("\n").map(function (x) { return x.replace(/\s+$/, ""); }).filter(function (x) { return x.trim(); });
      if (lines.length) blocks.push(lines);
    });
    /* bỏ khối đầu nếu chỉ lặp lại tên sách */
    if (blocks.length && blocks[0].length === 1 && fold(blocks[0][0].replace(/^#+\s*/, "")) === fold(title)) blocks.shift();
    var chapters = [], cur = null, nCh = 0;
    function open(t) { cur = { title: t, html: [], len: 0 }; chapters.push(cur); }
    blocks.forEach(function (lines) {
      var one = lines.length === 1 ? lines[0].trim() : "", m, h = null;
      if (one && (m = one.match(/^(#{1,4})\s+(.+)$/))) h = { l: m[1].length, t: m[2].replace(/\s#{2,}\s/g, " — ").replace(/\*+/g, "").trim() };
      else if (one && one.length <= 90 && !/[,;:]$/.test(one) && isCaps(one.replace(/^\d+[.)]\s*/, ""))) h = { l: 2, t: one };
      else if (one && one.length <= 60 && /^(chương|phần|lời tựa|lời nói đầu|kết luận|phụ lục|bài|ngày|hỏi)\b/i.test(one) && !/[.,;]$/.test(one)) h = { l: 2, t: one };
      if (h) {
        if (h.l <= 2) { if (cur && cur.title === h.t) return; if (!cur || cur.len > 200) { open(h.t); nCh++; } cur.html.push("<h2>" + inline(h.t) + "</h2>"); }
        else { if (!cur) open("Mở đầu"); cur.html.push("<h" + Math.min(h.l, 4) + ">" + inline(h.t) + "</h" + Math.min(h.l, 4) + ">"); }
        return;
      }
      if (!cur) open("Mở đầu");
      var out;
      if (lines.every(function (x) { return /^\s*[-*•]\s+/.test(x); })) out = "<ul>" + lines.map(function (x) { return "<li>" + inline(x.replace(/^\s*[-*•]\s+/, "")) + "</li>"; }).join("") + "</ul>";
      else if (lines.length >= 3 && lines.every(function (x) { return x.trim().length < 52; })) out = '<p class="verse">' + lines.map(function (x) { return inline(x.trim()); }).join("<br/>") + "</p>";
      else if (/^>\s?/.test(lines[0])) out = "<blockquote><p>" + inline(lines.map(function (x) { return x.replace(/^>\s?/, "").trim(); }).join(" ")) + "</p></blockquote>";
      else out = "<p>" + inline(lines.map(function (x) { return x.trim(); }).join(" ").replace(/\s{2,}/g, " ")) + "</p>";
      cur.html.push(out); cur.len += out.length;
    });
    /* chia nhỏ chương quá dài; gộp chương quá ngắn vào chương trước */
    var res = [];
    chapters.forEach(function (c) {
      if (res.length && c.len < 400 && res[res.length - 1].len < 90000) { var p = res[res.length - 1]; p.html = p.html.concat(c.html); p.len += c.len; return; }
      if (c.len <= 110000) { res.push(c); return; }
      var part = 1, buf = [], n = 0;
      c.html.forEach(function (x) { buf.push(x); n += x.length; if (n > 70000 && !/^<h/.test(x)) { res.push({ title: c.title + (part > 1 ? " (tiếp " + part + ")" : ""), html: buf, len: n }); buf = []; n = 0; part++; } });
      if (buf.length) res.push({ title: c.title + (part > 1 ? " (tiếp " + part + ")" : ""), html: buf, len: n });
    });
    if (res.length === 1 && res[0].len > 110000) res = [];
    return res;
  }

  /* ---------- Bìa ---------- */
  function wrap(ctx, text, w) { var words = text.split(/\s+/), lines = [], l = ""; words.forEach(function (x) { var t = l ? l + " " + x : x; if (ctx.measureText(t).width > w && l) { lines.push(l); l = x; } else l = t; }); if (l) lines.push(l); return lines; }
  function cover(b) {
    return new Promise(function (res) {
      try {
        var cv = document.createElement("canvas"); cv.width = 800; cv.height = 1200; var x = cv.getContext("2d");
        x.fillStyle = "#f6efe0"; x.fillRect(0, 0, 800, 1200);
        x.strokeStyle = "#5b3a1e"; x.lineWidth = 6; x.strokeRect(40, 40, 720, 1120); x.lineWidth = 2; x.strokeRect(58, 58, 684, 1084);
        x.fillStyle = "#3b2412"; x.textAlign = "center"; x.textBaseline = "alphabetic";
        var fs = 66, lines; do { x.font = "bold " + fs + "px 'Noto Serif', Georgia, 'Times New Roman', serif"; lines = wrap(x, b.t, 600); fs -= 4; } while ((lines.length > 6 || lines.length * (fs + 20) > 620) && fs > 30);
        var y = 360; lines.forEach(function (l) { x.fillText(l, 400, y); y += fs + 22; });
        x.strokeStyle = "#8a5a2b"; x.lineWidth = 3; x.beginPath(); x.moveTo(300, y + 10); x.lineTo(500, y + 10); x.stroke();
        x.font = "italic 40px 'Noto Serif', Georgia, serif"; x.fillStyle = "#5b3a1e";
        var ay = y + 90; wrap(x, b.a, 600).forEach(function (l) { x.fillText(l, 400, ay); ay += 52; });
        x.font = "28px 'Noto Serif', Georgia, serif"; x.fillStyle = "#7a5a3a"; x.fillText("Reformed Vietnam", 400, 1090);
        cv.toBlob(function (bl) { if (!bl) return res(null); bl.arrayBuffer().then(function (ab) { res(new Uint8Array(ab)); }); }, "image/png");
      } catch (e) { res(null); }
    });
  }

  /* ---------- EPUB ---------- */
  var CSS = "body{font-family:serif;line-height:1.55;margin:0 .6em}h1,h2,h3,h4{font-family:serif;line-height:1.25;page-break-after:avoid}h1{text-align:center;font-size:1.6em;margin:2em 0 .5em}h2{font-size:1.3em;margin:1.4em 0 .6em;text-align:center}h3{font-size:1.1em;margin:1.2em 0 .4em}h4{font-size:1em;font-style:italic}p{margin:0 0 .8em;text-indent:0;text-align:left}.verse{margin:1em 1.5em;font-style:italic}blockquote{margin:1em 1.5em;font-style:italic}.c{text-align:center}.small{font-size:.85em;color:#555}.t{margin-top:30%}.nav li{margin:.4em 0}";
  function xh(title, body) { return '<?xml version="1.0" encoding="utf-8"?>\n<!DOCTYPE html>\n<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" lang="vi" xml:lang="vi"><head><meta charset="utf-8"/><title>' + esc(title) + '</title><link rel="stylesheet" type="text/css" href="style.css"/></head><body>' + body + "</body></html>"; }
  function legal(b) {
    var r = [];
    if (b.k === "goc") r.push("Sách do Reformed Vietnam soạn, tác giả (bút danh): " + b.a + ". Bản nháp do AI hỗ trợ, chưa được mục sư duyệt giáo lý.");
    else r.push((b.o ? "Nguyên tác: " + b.o + ". " : "") + "Tác giả: " + b.a + ". Nguyên tác thuộc phạm vi công cộng. Bản tiếng Việt do AI hỗ trợ, chưa được mục sư duyệt giáo lý.");
    r.push("Hãy đối chiếu với Kinh Thánh (bản Việt ngữ 1934) và hỏi mục sư của bạn. Thấy lỗi? Gửi về reformedvn@gmail.com.");
    r.push("Miễn phí, không thương mại. Được sao chép và chia sẻ nguyên vẹn, vui lòng giữ nguyên trang này.");
    r.push("Nguồn: https://reformed-vietnam.vercel.app/");
    return r;
  }
  async function makeEpub(b, txt) {
    var chs = parse(txt, b.t);
    if (!chs.length) { var cs = txt.split(/\n[ \t]*\n/), buf = [], n = 0, i = 1; chs = []; cs.forEach(function (x) { var t = x.replace(/\s+/g, " ").trim(); if (!t) return; var p = "<p>" + inline(t) + "</p>"; buf.push(p); n += p.length; if (n > 60000) { chs.push({ title: "Phần " + i++, html: buf, len: n }); buf = []; n = 0; } }); if (buf.length) chs.push({ title: "Phần " + i, html: buf, len: n }); }
    var cov = await cover(b), files = [], man = [], spine = [], toc = [];
    files.push({ name: "mimetype", data: enc.encode("application/epub+zip"), store: true });
    files.push({ name: "META-INF/container.xml", data: enc.encode('<?xml version="1.0"?><container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container"><rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles></container>') });
    files.push({ name: "OEBPS/style.css", data: enc.encode(CSS) }); man.push('<item id="css" href="style.css" media-type="text/css"/>');
    if (cov) {
      files.push({ name: "OEBPS/cover.png", data: cov }); man.push('<item id="coverimg" href="cover.png" media-type="image/png" properties="cover-image"/>');
      files.push({ name: "OEBPS/cover.xhtml", data: enc.encode(xh(b.t, '<div class="c"><img src="cover.png" alt="' + esc(b.t) + '" style="max-width:100%;max-height:98vh"/></div>')) });
      man.push('<item id="cover" href="cover.xhtml" media-type="application/xhtml+xml"/>'); spine.push('<itemref idref="cover" linear="yes"/>');
    }
    files.push({ name: "OEBPS/title.xhtml", data: enc.encode(xh(b.t, '<div class="c t"><h1>' + esc(b.t) + "</h1><p>" + esc(b.a) + '</p><p class="small">Reformed Vietnam</p></div>')) });
    man.push('<item id="title" href="title.xhtml" media-type="application/xhtml+xml"/>'); spine.push('<itemref idref="title"/>');
    files.push({ name: "OEBPS/copyright.xhtml", data: enc.encode(xh("Bản quyền và ghi chú", "<h2>Bản quyền và ghi chú</h2>" + legal(b).map(function (x) { return "<p>" + esc(x) + "</p>"; }).join(""))) });
    man.push('<item id="legal" href="copyright.xhtml" media-type="application/xhtml+xml"/>'); spine.push('<itemref idref="legal"/>');
    chs.forEach(function (c, i) {
      var id = "c" + String(i + 1).padStart(3, "0"), nm = id + ".xhtml";
      files.push({ name: "OEBPS/" + nm, data: enc.encode(xh(c.title, c.html.join("\n"))) });
      man.push('<item id="' + id + '" href="' + nm + '" media-type="application/xhtml+xml"/>'); spine.push('<itemref idref="' + id + '"/>'); toc.push({ t: c.title, h: nm });
    });
    var nav = '<nav epub:type="toc" id="toc"><h2>Mục lục</h2><ol class="nav" style="list-style:none;padding:0">' + toc.map(function (c) { return '<li><a href="' + c.h + '">' + esc(c.t) + "</a></li>"; }).join("") + "</ol></nav>";
    files.push({ name: "OEBPS/nav.xhtml", data: enc.encode(xh("Mục lục", nav)) }); man.push('<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>');
    files.push({ name: "OEBPS/toc.ncx", data: enc.encode('<?xml version="1.0" encoding="utf-8"?><ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1"><head><meta name="dtb:uid" content="urn:rv:' + esc(b.s) + '"/></head><docTitle><text>' + esc(b.t) + "</text></docTitle><navMap>" + toc.map(function (c, i) { return '<navPoint id="n' + i + '" playOrder="' + (i + 1) + '"><navLabel><text>' + esc(c.t) + '</text></navLabel><content src="' + c.h + '"/></navPoint>'; }).join("") + "</navMap></ncx>") });
    man.push('<item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>');
    var d = new Date().toISOString().slice(0, 10);
    files.splice(2, 0, { name: "OEBPS/content.opf", data: enc.encode('<?xml version="1.0" encoding="utf-8"?><package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="uid" xml:lang="vi"><metadata xmlns:dc="http://purl.org/dc/elements/1.1/"><dc:identifier id="uid">urn:rv:' + esc(b.s) + "</dc:identifier><dc:title>" + esc(b.t) + "</dc:title><dc:creator>" + esc(b.a) + "</dc:creator><dc:language>vi</dc:language><dc:publisher>Reformed Vietnam</dc:publisher><dc:rights>Miễn phí, không thương mại</dc:rights><dc:source>https://reformed-vietnam.vercel.app/reader.html?id=vn/" + esc(b.s) + '</dc:source><meta property="dcterms:modified">' + d + "T00:00:00Z</meta></metadata><manifest>" + man.join("") + '</manifest><spine toc="ncx">' + spine.join("") + "</spine></package>") });
    return zip(files, "application/epub+zip");
  }

  /* ---------- UI ---------- */
  function fname(b) { return fold(b.a).replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "").slice(0, 20) + "_" + b.s.slice(0, 60) + ".epub"; }
  function save(blob, name) { var a = document.createElement("a"), u = URL.createObjectURL(blob); a.href = u; a.download = name; document.body.appendChild(a); a.click(); setTimeout(function () { a.remove(); URL.revokeObjectURL(u); }, 4000); }
  function status(t) { $("st").textContent = t; }
  function prog(p) { $("pg").hidden = p == null; if (p != null) $("pg").value = p; }
  async function build(b) { var r = await fetch("/txt/" + b.s + ".txt"); if (!r.ok) throw new Error(b.s); return makeEpub(b, await r.text()); }
  async function one(b) { if (busy) return; busy = true; try { status("Đang tạo “" + b.t + "”…"); var bl = await build(b); save(bl, fname(b)); status("Đã tạo: " + b.t + " (" + fmtMB(bl.size) + ")."); } catch (e) { status("Lỗi khi tạo sách. Hãy thử lại."); } busy = false; }
  async function many(list, name) {
    if (busy || !list.length) return; busy = true; var files = [], fail = 0;
    try {
      for (var i = 0; i < list.length; i++) {
        status("Đang tạo " + (i + 1) + "/" + list.length + ": " + list[i].t); prog(i / list.length);
        try { var bl = await build(list[i]); files.push({ name: fname(list[i]), data: new Uint8Array(await bl.arrayBuffer()), store: true }); } catch (e) { fail++; }
        await new Promise(function (r) { setTimeout(r, 0); });
      }
      status("Đang đóng gói ZIP…"); var z = await zip(files); save(z, name); status("Xong: " + files.length + " sách, " + fmtMB(z.size) + (fail ? " (" + fail + " sách lỗi)" : "") + ".");
    } catch (e) { status("Lỗi khi đóng gói. Hãy thử ít sách hơn."); }
    prog(null); busy = false;
  }
  function render() {
    var q = fold($("q").value.trim()), h = "", shown = 0;
    LIST.forEach(function (b, i) { if (q && fold(b.t + " " + b.a).indexOf(q) < 0) return; shown++;
      h += '<li><label><input type="checkbox" data-i="' + i + '"' + (SEL[i] ? " checked" : "") + '> <b>' + esc(b.t) + "</b></label> · " + esc(b.a) + ' <span class="stt">(~' + fmtMB(b.n * 0.3) + ')</span> <button type="button" class="ct" data-d="' + i + '">Tải EPUB</button></li>'; });
    $("ls").innerHTML = h || "<li>Không có sách phù hợp.</li>"; $("cnt").textContent = Object.keys(SEL).filter(function (k) { return SEL[k]; }).length + " sách đã chọn";
  }
  function parts(size) { var P = [], cur = [], n = 0; LIST.slice().sort(function (a, b) { return a.a.localeCompare(b.a) || a.t.localeCompare(b.t); }).forEach(function (b) { if (n + b.n > size && cur.length) { P.push(cur); cur = []; n = 0; } cur.push(b); n += b.n; }); if (cur.length) P.push(cur); return P; }
  function init(data) {
    LIST = data; render();
    var P = parts(18e6);
    $("parts").innerHTML = P.map(function (p, i) { return '<button type="button" class="btn s" data-p="' + i + '">Phần ' + (i + 1) + "/" + P.length + ": " + p.length + " sách (~" + fmtMB(p.reduce(function (a, b) { return a + b.n; }, 0) * 0.3) + ")</button> "; }).join("");
    $("parts").onclick = function (e) { var i = e.target.dataset && e.target.dataset.p; if (i != null) many(P[+i], "reformed-vietnam-epub-phan-" + (+i + 1) + ".zip"); };
    $("ls").onchange = function (e) { var i = e.target.dataset && e.target.dataset.i; if (i != null) { SEL[i] = e.target.checked; $("cnt").textContent = Object.keys(SEL).filter(function (k) { return SEL[k]; }).length + " sách đã chọn"; } };
    $("ls").onclick = function (e) { var i = e.target.dataset && e.target.dataset.d; if (i != null) one(LIST[+i]); };
    $("q").oninput = render;
    $("all").onclick = function () { LIST.forEach(function (_, i) { SEL[i] = true; }); render(); };
    $("none").onclick = function () { SEL = {}; render(); };
    $("dl").onclick = function () { var l = LIST.filter(function (_, i) { return SEL[i]; }); if (!l.length) { status("Hãy chọn ít nhất một sách."); return; } many(l, "reformed-vietnam-epub-da-chon.zip"); };
  }
  fetch("/tai-sach.json").then(function (r) { return r.json(); }).then(init).catch(function () { status("Không tải được danh sách sách. Hãy tải lại trang."); });
})();

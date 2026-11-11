#!/usr/bin/env python3
"""Phase 6.1/6.2 — Hoi Thu Vien (Ask the library / Ask a book).

Builds /hoi-thu-vien.html: RETRIEVAL, not generated answers. The visitor
types a question; the page finds matching passages in the site's own data
and shows them with citations (links back to the source pages). No AI API
is called, no backend, no invented passages. If nothing matches, it says so.

Two scopes, one page:
- Library-wide (?q=...): client-side keyword retrieval over
  /data/search-index.json — the same index /tim-kiem/ uses (books, Bible,
  catechism, encyclopedia, devotions, answers, sermons, hymns, journal,
  Academy). Accent-insensitive, title > subtitle > body, exact-phrase bonus.
- One book (?sach=<slug>): the same retriever scoped to that book's own
  text — fetches /txt/<slug>.txt on demand (streamed with a 4 MB cap; very
  long books say so plainly), splits it into passages by chapter headings,
  and returns the matching passages with the chapter label and links to the
  book page + reader. Book title/author come from the txt header lines.

The page states plainly, above the search box, that it finds passages and
does not write answers. Every ban-dich book page links here with
?Sach=<slug> ("Hoi sach nay", added by scripts/patch_ban_dich_phase6.py
and the page() template in tools/build-pages.py).
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from hub_page import (BASE, ROOT, head, header, footer, MINI_JS, share_row,
                      report_mailto, write_if_changed, check_links, sitemap_add)

URL = f"{BASE}/hoi-thu-vien.html"

CSS = r"""
      .big-search { max-width: 640px; margin: 14px auto 6px; display: flex; gap: 8px; }
      .big-search input { flex: 1; padding: 13px 16px; border: 1px solid var(--line); border-radius: 999px; font: inherit; font-size: 16px; background: var(--surface); color: var(--ink); }
      .group-head { max-width: 760px; margin: 26px auto 4px; font-size: 13px; font-weight: 700; letter-spacing: .07em; text-transform: uppercase; color: var(--gold-text); }
      .qa-cards { display: grid; gap: 12px; max-width: 760px; margin: 10px auto 8px; }
      .qa-card { display: block; background: var(--surface); border: 1px solid var(--line); border-radius: var(--radius); padding: 16px 20px; box-shadow: var(--shadow); text-decoration: none; }
      .qa-card h3 { font-family: "Noto Serif", serif; font-size: 17px; margin: 0 0 4px; color: var(--ink); line-height: 1.45; }
      .qa-card p { margin: 0; color: var(--ink-soft); font-size: 14px; line-height: 1.55; }
      .qa-card:hover h3 { color: var(--burgundy); }
      .status { text-align: center; color: var(--ink-soft); font-size: 15px; margin: 18px 0 4px; }
      .ask-note { max-width: 760px; margin: 14px auto 4px; padding: 14px 18px; border: 1px solid var(--gold-soft); border-radius: 12px; background: rgba(217, 164, 30, .08); font-size: 14.5px; line-height: 1.6; }
      .ask-note b { color: var(--burgundy); }
      .ask-note ul { margin: 6px 0 0; padding-left: 20px; }
      .ask-note li { margin: 3px 0; }
      .chips { display: flex; gap: 8px; flex-wrap: wrap; justify-content: center; max-width: 760px; margin: 10px auto 2px; }
      .chip { padding: 6px 14px; border: 1px solid var(--line); border-radius: 999px; background: var(--surface); color: var(--ink); font: 13.5px "Be Vietnam Pro", system-ui, sans-serif; cursor: pointer; }
      .chip:hover { border-color: var(--gold-text); color: var(--burgundy); }
      .book-banner { max-width: 760px; margin: 14px auto 4px; padding: 12px 18px; border: 1px solid var(--line); border-radius: 12px; background: var(--surface); font-size: 14.5px; line-height: 1.6; }
      .book-banner b { font-family: "Noto Serif", serif; font-size: 17px; }
      mark { background: #f3d98b; color: inherit; border-radius: 2px; padding: 0 1px; }
      .cite { font-size: 13px !important; color: var(--gold-text) !important; margin-top: 6px !important; }
      .cite a { color: var(--gold-text); font-weight: 700; }
"""

ASK_JS = r"""
<script>
(function () {
  "use strict";
  var $ = function (id) { return document.getElementById(id); };
  function fold(s) { return String(s || "").toLowerCase().replace(/đ/g, "d").normalize("NFD").replace(/[\u0300-\u036f]/g, ""); }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  // Stopwords: common Vietnamese function words only. Deliberately NOT in
  // this list: "an" (an = grace, an ui), "co" (co = aunt), "ma" (ma = demon)
  // — they fold identically to content words, so dropping them would hide
  // real passages.
  var STOP = { "la": 1, "va": 1, "cua": 1, "trong": 1, "nhung": 1, "cac": 1, "mot": 1, "gi": 1, "nao": 1, "thi": 1, "ma": 1, "de": 1, "cho": 1, "voi": 1, "ve": 1, "tu": 1, "den": 1, "o": 1, "duoc": 1, "nguoi": 1, "toi": 1, "ban": 1, "nay": 1, "do": 1, "khi": 1, "da": 1, "se": 1, "rat": 1, "cung": 1, "lai": 1, "nua": 1, "hay": 1, "neu": 1, "nhu": 1, "hoac": 1, "sao": 1, "the": 1, "lam": 1, "khong": 1 };
  function tokens(q) {
    var all = fold(q).match(/[a-z0-9]+/g) || [];
    return all.filter(function (w) { return w.length >= 2 && !STOP[w]; });
  }
  function hi(text, toks) {
    // Highlight whole folded words in the original (diacritic) text.
    return esc(text).split(/(\s+)/).map(function (w) {
      if (!w || /\s/.test(w)) return w;
      var f = fold(w).replace(/[^a-z0-9]/g, "");
      return toks.indexOf(f) !== -1 ? "<mark>" + w + "</mark>" : w;
    }).join("");
  }
  function excerpt(text, toks, len) {
    // Window around the first matching word. Word-by-word scan (not a
    // folded-string index): fold() lengthens Vietnamese text (NFD splits
    // diacritics), so a folded index does not map back onto the plain text.
    var plain = String(text).replace(/\s+/g, " ").replace(/-/g, " "), words = plain.split(" "), at = -1, pos = 0;
    for (var i = 0; i < words.length; i++) {
      var f = fold(words[i]).replace(/[^a-z0-9]/g, "");
      if (toks.indexOf(f) !== -1) { at = pos; break; }
      pos += words[i].length + 1;
    }
    if (at < 0) at = 0;
    var start = Math.max(0, at - 140), n = len || 420, sn = plain.slice(start, start + n);
    return (start > 0 ? "…" : "") + sn + (start + n < plain.length ? "…" : "");
  }

  var ORDER = ["Kinh Thánh", "Sách", "Giáo Lý", "Bách Khoa", "Tĩnh Nguyện", "Hỏi Đáp", "Học Viện", "Bài Giảng", "Thánh Ca", "Tạp Chí", "Hội Thánh", "Công Cụ"];
  var params = new URLSearchParams(location.search);
  var SACH = params.get("sach") || "";
  var input = $("q"), box = $("results"), status = $("st");
  var INDEX = null, cache = [], BOOK = null; // BOOK: {slug,title,author,chunks,folded,truncated}

  function renderLibrary(q) {
    var words = tokens(q);
    if (!words.length) {
      status.textContent = "Hãy gõ ít nhất một từ có nghĩa (tên riêng, thuật ngữ cụ thể) — các từ như “là”, “của”, “là gì” xuất hiện ở khắp nơi nên chưa tìm được.";
      box.innerHTML = ""; return;
    }
    if (!INDEX) { status.textContent = "Đang tải chỉ mục tìm kiếm…"; return; }
    var phrase = words.join(" "), groups = {}, total = 0;
    cache.forEach(function (c) {
      var hay = c.nt + " " + c.ns + " " + c.nb, score = 0, ok = true, bodyOnly = true;
      for (var i = 0; i < words.length; i++) {
        if (hay.indexOf(words[i]) === -1) { ok = false; break; }
        if (c.nt.indexOf(words[i]) !== -1) { score += 3; bodyOnly = false; }
        else if (c.ns.indexOf(words[i]) !== -1) { score += 2; bodyOnly = false; }
        else score += 1;
      }
      if (!ok) return;
      // A title that IS the question's phrase (e.g. "Ân điển" for "ân điển
      // là gì") is the definition the visitor wants — rank it first.
      if (c.nt.trim() === phrase) score += 20;
      if (c.nt.indexOf(phrase) !== -1) score += 3;
      else if (c.ns.indexOf(phrase) !== -1) score += 2;
      else if (c.nb.indexOf(phrase) !== -1) score += 1;
      (groups[c.it.g] = groups[c.it.g] || []).push({ it: c.it, score: score, bodyOnly: bodyOnly });
      total++;
    });
    box.innerHTML = "";
    if (!total) {
      status.textContent = "Không tìm thấy đoạn nào chứa tất cả các từ “" + q + "”. Đây không phải là câu trả lời — mà là không có đoạn văn nào khớp. Thử ít từ hơn, hoặc kiểm tra chính tả (gõ không dấu vẫn tìm được).";
      return;
    }
    status.textContent = "Tìm thấy " + total + " đoạn văn chứa các từ này cho “" + q + "” — đây là các đoạn trích có sẵn trên trang, kèm link về trang gốc để bạn tự đọc và đối chiếu. Trang này không tự soạn câu trả lời.";
    ORDER.forEach(function (g) {
      var list = groups[g];
      if (!list) return;
      list.sort(function (a, b) { return b.score - a.score; });
      var head = document.createElement("div");
      head.className = "group-head"; head.textContent = g + " · " + list.length;
      box.appendChild(head);
      var wrap = document.createElement("div");
      wrap.className = "qa-cards";
      list.slice(0, 8).forEach(function (r) {
        var a = document.createElement("a");
        a.className = "qa-card"; a.href = r.it.u;
        var sub = r.it.s;
        if (r.bodyOnly && r.it.b) sub = excerpt(r.it.b, words, 200);
        a.innerHTML = "<h3>" + hi(r.it.t, words) + "</h3>" + (sub ? "<p>" + hi(sub, words) + "</p>" : "") +
          "<p class=\"cite\">" + esc(g) + (r.it.a ? " · " + esc(r.it.a) : "") + "</p>";
        wrap.appendChild(a);
      });
      box.appendChild(wrap);
      if (list.length > 8) {
        var more = document.createElement("p");
        more.className = "status";
        more.textContent = "… và " + (list.length - 8) + " kết quả nữa trong mục " + g + " — hãy thêm từ khóa để thu hẹp.";
        box.appendChild(more);
      }
    });
  }

  function chunkText(txt) {
    var paras = txt.split(/\n\s*\n/), chunks = [], cur = "", label = "", head = "";
    function isHead(t) {
      if (t.length > 90) return false;
      if (/^(Chương|CHƯƠNG|Chuong|PHẦN|Phần|#)\b/.test(t)) return true;
      if (t === t.toUpperCase() && /[A-ZÀ-Ỹ]/.test(t) && t.length > 3 && !/[.!?]$/.test(t)) return true;
      return false;
    }
    function flushLong() {
      // A single long paragraph must not become one giant chunk: cut at a
      // sentence end, else a space, else hard at 600 chars.
      while (cur.length > 600) {
        var probe = cur.slice(0, 600), cut = probe.lastIndexOf(". "), end;
        if (cut >= 300) end = cut + 1;
        else { cut = probe.lastIndexOf(" "); end = cut >= 300 ? cut : 600; }
        chunks.push({ label: label, text: cur.slice(0, end).trim() });
        cur = cur.slice(end).trim();
      }
    }
    paras.forEach(function (p) {
      var t = p.replace(/\s+/g, " ").trim();
      if (!t) return;
      if (isHead(t)) { head = t; flushLong(); if (cur) { chunks.push({ label: label, text: cur }); cur = ""; } label = head; return; }
      cur += (cur ? " " : "") + t;
      flushLong();
    });
    if (cur) chunks.push({ label: label, text: cur });
    return chunks;
  }

  function loadBook() {
    var banner = $("bookBanner");
    banner.hidden = false;
    $("bookLink").href = "/ban-dich/" + encodeURIComponent(SACH) + ".html";
    $("readerLink").href = "/reader.html?id=vn/" + encodeURIComponent(SACH);
    $("allLink").href = "/hoi-thu-vien.html";
    // Stream the txt with a 4 MB cap (a few books are tens of MB; the cap
    // stops the transfer instead of downloading the whole file). A cut
    // mid-character is replaced by the decoder and is harmless.
    fetch("/txt/" + encodeURIComponent(SACH) + ".txt")
      .then(function (r) {
        if (!r.ok) throw new Error("HTTP " + r.status);
        var reader = r.body.getReader(), parts = [], total = 0, LIMIT = 4194304;
        function pump() {
          return reader.read().then(function (res) {
            if (res.done || total >= LIMIT) { reader.cancel(); return { truncated: total >= LIMIT && !res.done }; }
            parts.push(res.value); total += res.value.length;
            return pump();
          });
        }
        return pump().then(function (o) {
          var all = new Uint8Array(total), off = 0;
          parts.forEach(function (p) { all.set(p, off); off += p.length; });
          return { text: new TextDecoder().decode(all), truncated: o.truncated };
        });
      })
      .then(function (o) {
        var lines = o.text.split("\n").map(function (l) { return l.trim(); }).filter(Boolean);
        var title = lines[0] || SACH, author = "";
        if (lines[2]) {
          var a0 = lines[2].split("·")[0].trim();
          if (a0 && a0.length >= 2 && a0.length <= 40 && a0.indexOf("http") === -1 && a0.indexOf("Bản dịch") === -1) author = a0;
        }
        var chunks = chunkText(o.text).map(function (c) {
          c.fold = " " + fold(c.text).replace(/[^a-z0-9]+/g, " ") + " ";
          return c;
        });
        BOOK = { slug: SACH, title: title, author: author, chunks: chunks, truncated: o.truncated };
        $("bookTitle").textContent = title + (author ? " — " + author : "");
        $("bookMeta").textContent = chunks.length + " đoạn văn trong sách này" +
          (o.truncated ? " (sách rất dài — chỉ tìm trong 4 MB đầu của bản dịch)" : "") + ".";
        if (input.value) run(input.value);
        else status.textContent = "Đã tải xong toàn văn sách này. Gõ câu hỏi để tìm đoạn văn trong sách.";
      })
      .catch(function () {
        $("bookTitle").textContent = SACH;
        $("bookMeta").textContent = "Không tải được toàn văn sách này (có thể sách chưa có bản text). ";
        status.textContent = "Không tải được toàn văn sách này. Bạn vẫn có thể hỏi toàn thư viện — hoặc mở trang sách để đọc trực tiếp.";
      });
  }

  function renderBook(q) {
    var words = tokens(q);
    if (!words.length) {
      status.textContent = "Hãy gõ ít nhất một từ có nghĩa (tên riêng, thuật ngữ cụ thể).";
      box.innerHTML = ""; return;
    }
    if (!BOOK) { status.textContent = "Đang tải toàn văn sách này…"; return; }
    var phrase = " " + words.join(" ") + " ", out = [];
    BOOK.chunks.forEach(function (c) {
      var score = 0, ok = true;
      for (var i = 0; i < words.length; i++) {
        if (c.fold.indexOf(" " + words[i] + " ") === -1) { ok = false; break; }
        score += 1;
      }
      if (!ok) return;
      if (c.fold.indexOf(phrase) !== -1) score += 100;
      out.push({ c: c, score: score });
    });
    box.innerHTML = "";
    if (!out.length) {
      status.textContent = "Không tìm thấy đoạn nào trong sách này chứa tất cả các từ “" + q + "”. Trang không bịa thêm đoạn văn — thử ít từ hơn, hoặc hỏi toàn thư viện.";
      return;
    }
    out.sort(function (a, b) { return b.score - a.score; });
    status.textContent = "Tìm thấy " + out.length + " đoạn trong “" + BOOK.title + "” chứa các từ này" +
      (BOOK.truncated ? " (trong 4 MB đầu của bản dịch)" : "") +
      " — đây là đoạn trích nguyên văn, kèm link về trang sách để bạn đọc đầy đủ.";
    var wrap = document.createElement("div");
    wrap.className = "qa-cards";
    out.slice(0, 10).forEach(function (r) {
      var d = document.createElement("div");
      d.className = "qa-card";
      d.innerHTML = "<h3>" + (r.c.label ? hi(r.c.label, words) : "Đoạn trích") + "</h3>" +
        "<p>" + hi(excerpt(r.c.text, words, 420), words) + "</p>" +
        "<p class=\"cite\"><a href=\"/ban-dich/" + esc(BOOK.slug) + ".html\">Về trang sách</a> · " +
        "<a href=\"/reader.html?id=vn/" + esc(BOOK.slug) + "\">Mở trong trình đọc</a></p>";
      wrap.appendChild(d);
    });
    box.appendChild(wrap);
    if (out.length > 10) {
      var more = document.createElement("p");
      more.className = "status";
      more.textContent = "… và " + (out.length - 10) + " đoạn nữa — hãy thêm từ khóa để thu hẹp.";
      box.appendChild(more);
    }
  }

  function run(q) { if (SACH) renderBook(q); else renderLibrary(q); }

  function prepare() {
    cache = INDEX.items.map(function (it) {
      return { it: it, nt: fold(it.t), ns: fold(it.s), nb: fold(it.b || "") };
    });
  }

  var t = null;
  input.addEventListener("input", function () {
    clearTimeout(t);
    t = setTimeout(function () { run(input.value); }, 200);
  });
  $("askForm").addEventListener("submit", function (e) { e.preventDefault(); run(input.value); });
  document.querySelectorAll("[data-q]").forEach(function (el) {
    el.addEventListener("click", function () { input.value = el.getAttribute("data-q"); run(input.value); input.focus(); });
  });

  var q0 = params.get("q") || "";
  if (q0) input.value = q0;
  if (SACH) {
    loadBook();
    if (q0) status.textContent = "Đang tải toàn văn sách này…";
  } else {
    fetch("/data/search-index.json")
      .then(function (r) { return r.json(); })
      .then(function (d) { INDEX = d; prepare(); if (input.value) run(input.value); })
      .catch(function () { status.textContent = "Không tải được chỉ mục tìm kiếm. Xin thử tải lại trang."; });
    if (!q0) status.textContent = "Nhập câu hỏi hoặc từ khóa để tìm đoạn văn trong toàn bộ thư viện — sách, Kinh Thánh, giáo lý, bách khoa, tĩnh nguyện, Hỏi Đáp và học viện. Gõ không dấu cũng được.";
  }
})();
</script>
"""

SAMPLES = [
    "Ân điển là gì",
    "Làm sao biết mình được cứu",
    "Tiền định là gì",
    "Cầu nguyện thế nào",
    "Sự xưng công chính",
    "Báp-têm",
]

CHIPS = "".join(
    f'<button type="button" class="chip" data-q="{q}">{q}</button>' for q in SAMPLES
)


def main():
    body = f"""  <p class="crumb"><a href="/">Trang chủ</a> · Hỏi Thư Viện</p>
  <div class="cat-head">
    <div class="kicker">Hỏi Thư Viện</div>
    <h1>Tìm Đoạn Văn, Không Soạn Câu Trả Lời</h1>
  </div>
  <div class="ask-note">
    <b>Trang này tìm đoạn văn — không viết câu trả lời.</b>
    <ul>
      <li>Bạn gõ câu hỏi hoặc từ khóa; trang tìm những đoạn trong thư viện, Kinh Thánh, giáo lý, bách khoa, tĩnh nguyện và Hỏi Đáp có chứa các từ đó.</li>
      <li>Mỗi kết quả là đoạn trích nguyên văn, kèm link về đúng trang gốc để bạn tự đọc đầy đủ và đối chiếu với Kinh Thánh.</li>
      <li>Trang <b>không dùng AI để soạn câu trả lời</b>, không bịa thêm nội dung. Nếu không tìm thấy đoạn nào, trang sẽ nói rõ là không tìm thấy.</li>
    </ul>
  </div>
  <div class="book-banner" id="bookBanner" hidden>
    Đang hỏi trong sách: <b id="bookTitle">…</b><br>
    <span id="bookMeta">Đang tải toàn văn sách này…</span><br>
    <a id="bookLink" href="#">Về trang sách</a> · <a id="readerLink" href="#">Mở trong trình đọc</a> · <a id="allLink" href="/hoi-thu-vien.html">Hỏi toàn thư viện thay vào đó</a>
  </div>
  <form class="big-search" id="askForm" role="search">
    <input id="q" type="search" name="q" placeholder="Hỏi bằng câu đầy đủ, hoặc gõ vài từ khóa…" aria-label="Hỏi thư viện" autocomplete="off" />
    <button class="btn solid" type="submit">Tìm đoạn văn</button>
  </form>
  <div class="chips" aria-label="Câu hỏi gợi ý">{CHIPS}</div>
  <p class="status" id="st">Đang tải…</p>
  <div id="results"></div>
  <p class="status" style="margin-top:26px">Kết quả lấy từ chỉ mục tìm kiếm của trang và — khi hỏi một sách — từ toàn văn bản dịch của sách đó. Muốn tìm kiếm thông thường theo tựa đề và bộ lọc, xin dùng <a href="/tim-kiem/">trang Tìm Kiếm</a>.</p>
  {share_row(URL)}
  {report_mailto("Hỏi Thư Viện")}"""
    p = (head("Hỏi Thư Viện | Reformed Vietnam",
              "Gõ câu hỏi, trang tìm những đoạn trong thư viện, Kinh Thánh, giáo lý, bách khoa và Hỏi Đáp có chứa các từ đó — kèm link về trang gốc. Trang tìm đoạn văn, không tự soạn câu trả lời.",
              URL, CSS)
         + "<body><main>" + header + body + "</main>" + footer + MINI_JS + ASK_JS + "</body></html>")
    changed = write_if_changed(ROOT / "hoi-thu-vien.html", p)
    check_links(p, "/hoi-thu-vien.html")
    print(f"ask page: {'written' if changed else 'unchanged'}")
    print(f"sitemap: {sitemap_add(['/hoi-thu-vien.html'])} URLs added")
    print("DONE")


if __name__ == "__main__":
    main()

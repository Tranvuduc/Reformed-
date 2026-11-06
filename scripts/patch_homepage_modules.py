#!/usr/bin/env python3
"""Patch the homepage (index.html + hub.html) for the Daily Grace and
Bible Study module launches (2026-11-06):

1. Devotion panel (#tinh-nguyen): element ids + a rotation script that renders
   the visitor's actual today's entry from /data/devotions.json (Build Guide
   §8: always the real entry for the calendar date). The baked entry remains
   as the no-JS fallback, with its date stated. The "Sắp ra mắt" status line
   becomes real links (today's page, the 366 archive, the Bible reader).
2. Module directory (#phan-khu): the Ân Điển Mỗi Ngày card now links to
   /suy-ngam/ with a "Có sẵn" pill; the Học Kinh Thánh card becomes a link
   to /kinh-thanh/ with a "Có sẵn" pill.
"""
import re, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent

ROTATION_JS = """
<script>
  (function () {
    var days = ["Chủ Nhật", "Thứ Hai", "Thứ Ba", "Thứ Tư", "Thứ Năm", "Thứ Sáu", "Thứ Bảy"];
    fetch("/data/devotions.json").then(function (r) { return r.json(); }).then(function (data) {
      var now = new Date(), m = now.getMonth() + 1, d = now.getDate();
      var e = null;
      data.entries.forEach(function (x) { if (x.month === m && x.day === d) e = x; });
      if (!e) return;
      var pad = function (n) { return String(n).padStart(2, "0"); };
      var dd = document.getElementById("devDate");
      if (dd && dd.childNodes[0]) dd.childNodes[0].textContent = days[now.getDay()] + ", " + d + " tháng " + m + ", " + now.getFullYear() + " · Bài ngày " + d + "/" + m + " trong “Sổ Séc Của Đức Tin” (1888) — bài “" + e.title + "”";
      var v = document.getElementById("devVerse"); if (v) v.textContent = "“" + e.verse + "”";
      var rf = document.getElementById("devRef"); if (rf) rf.textContent = e.ref;
      var p1 = document.getElementById("devP1"), p2 = document.getElementById("devP2");
      if (p1 && e.paras[0]) p1.textContent = e.paras[0];
      if (p2) { if (e.paras[1]) { p2.textContent = e.paras[1]; p2.style.display = ""; } else { p2.style.display = "none"; } }
      var link = document.getElementById("devTodayLink");
      if (link) link.setAttribute("href", "/suy-ngam/" + pad(m) + "-" + pad(d) + ".html");
    }).catch(function () {});
  })();
</script>
"""

for name in ["index.html", "hub.html"]:
    p = ROOT / name
    t = p.read_text(encoding="utf-8")
    if 'id="devDate"' in t:
        print(name, "already patched, skipping"); continue

    # --- 1. devotion panel ids ---
    t = t.replace('<div class="dev-date">', '<div class="dev-date" id="devDate">', 1)
    t = t.replace('<blockquote class="dev-verse">', '<blockquote class="dev-verse" id="devVerse">', 1)
    t = t.replace('<div class="dev-ref">', '<div class="dev-ref" id="devRef">', 1)
    i = t.find('id="devRef"')
    seg = t[i:]
    paras = list(re.finditer(r"<p>", seg))
    assert len(paras) >= 2, name
    # insert ids into the first two <p> after dev-ref (document order)
    first = paras[0].start(); second = paras[1].start()
    seg = seg[:second] + '<p id="devP2">' + seg[second + 3:]
    seg = seg[:first] + '<p id="devP1">' + seg[first + 3:]
    t = t[:i] + seg

    # --- 2. status line -> real links ---
    old_status = '<p style="margin-top:auto"><span class="pill phase">Sắp ra mắt</span> Trọn bộ 366 bài tĩnh nguyện sẽ có ngay tại trang này.</p>'
    assert old_status in t, name + " status line"
    t = t.replace(old_status,
        '<p style="margin-top:auto"><a class="btn solid" id="devTodayLink" href="/suy-ngam/">Đọc bài hôm nay →</a> '
        '<a class="btn" href="/suy-ngam/">Tất cả 366 bài</a> '
        '<a class="btn" href="/kinh-thanh/">Đọc Kinh Thánh 1934</a></p>', 1)

    # --- 3. module cards ---
    i = t.find('id="phan-khu"'); j = t.find("</section>", i)
    seg = t[i:j]
    # Ân Điển Mỗi Ngày card
    seg = seg.replace('<a class="module" href="#tinh-nguyen">', '<a class="module" href="/suy-ngam/">', 1)
    seg = seg.replace('đang được đưa về chính trang này, mỗi ngày một bài ngay tại đây',
                      'một bài cho mỗi ngày trong năm, đọc ngay tại trang này', 1)
    # Học Kinh Thánh card: div -> a (the card whose h3 is Học Kinh Thánh)
    m = re.search(r'<div class="module">(.*?)</div>', seg, re.S)
    # find the specific card by walking module starts
    starts = [mm.start() for mm in re.finditer(r'<(?:a|div) class="module"', seg)]
    starts.append(len(seg))
    for k in range(len(starts) - 1):
        card = seg[starts[k]:starts[k + 1]]
        if "<h3>Học Kinh Thánh</h3>" in card:
            assert card.startswith('<div class="module">'), name + " bible card tag"
            card = card.replace('<div class="module">', '<a class="module" href="/kinh-thanh/">', 1)
            card = card.replace('đang được đưa về chính trang này', 'ngay tại trang này', 1)
            # close the card: its trailing </div> before the next card start
            idx = card.rfind("</div>")
            card = card[:idx] + "</a>" + card[idx + 6:]
            seg = seg[:starts[k]] + card + seg[starts[k + 1]:]
            break
    else:
        raise SystemExit(name + ": Hoc Kinh Thanh card not found")
    # pills for the two launched cards: the two "Sắp ra mắt" pills nearest after
    # the /suy-ngam/ and /kinh-thanh/ hrefs
    for href in ['href="/suy-ngam/"', 'href="/kinh-thanh/"']:
        k = seg.find(href)
        assert k >= 0, (name, href)
        pk = seg.find('<span class="pill phase">Sắp ra mắt</span>', k)
        assert pk >= 0, (name, href, "pill")
        seg = seg[:pk] + '<span class="pill live">Có sẵn</span>' + seg[pk + len('<span class="pill phase">Sắp ra mắt</span>'):]
    t = t[:i] + seg + t[j:]

    # --- 4. rotation script before </body> ---
    assert "</body>" in t
    t = t.replace("</body>", ROTATION_JS + "</body>", 1)
    p.write_text(t, encoding="utf-8")
    print(name, "patched: devotion rotation + module cards live")
print("DONE")

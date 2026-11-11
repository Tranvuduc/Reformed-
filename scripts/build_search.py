#!/usr/bin/env python3
"""Build the unified site search for Reformed Vietnam (post-review fix, 2026-11-07).

The Build Guide calls for one accent-insensitive search across the whole
site; the homepage previously searched only the 6 featured books. This
builder emits a single static index (data/search-index.json) covering the
book catalogue (validated against the sitemap — no dead links), the Bible
(66 books + 1,189 chapter summaries), Catechism, Encyclopedia, Daily Grace,
Answers, Sermons, Hymns, Journal and Academy courses/lessons, plus the
search page at /tim-kiem/ that queries it client-side. Search v2 (2026-11-07):
items also carry a body field ("b") — devotion text, hymn lyrics + tune,
catechism answers, encyclopedia bodies, answer bodies — so body words are
findable; title hits rank above subtitle, subtitle above body.
"""
import json, re, html, pathlib, urllib.request, datetime

ROOT = pathlib.Path(__file__).resolve().parent.parent
APP = ROOT.parent / "bible-app"
BASE = "https://reformedvietnam.com"

sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
live_urls = set(re.findall(r"<loc>([^<]+)</loc>", sitemap))

def alive(url):
    return (BASE + url) in live_urls

items = []
def add(t, s, u, g, b="", **extra):
    # "b" is body text: searched (lowest weight) but never shown as the
    # card title/subtitle. Added 2026-11-07 (search v2): the v1 index only
    # matched title+subtitle, so a word inside a devotion, a hymn's lyrics
    # or a tune name (e.g. NEW BRITAIN) found nothing.
    # **extra carries string facets (Phase 1.4): books add a=author,
    # tp=topics, lv=level (1/2/3), st=review_status. Every field must stay
    # a string — the search page calls .toLowerCase() on values.
    if t and u:
        it = {"t": t, "s": s or "", "u": u, "g": g}
        if b:
            # Body fields are strings in most modules but paragraph LISTS in
            # others (encyclopedia body_vi, journal intro/excerpt). A list
            # stored raw would break the search page: its norm() calls
            # .toLowerCase() on the value. Flatten first, always a string.
            if not isinstance(b, str):
                parts = []
                for x in b:
                    if isinstance(x, dict):
                        parts += [str(y) for y in x.values()]
                    else:
                        parts.append(str(x))
                b = " ".join(parts)
            it["b"] = b[:2500]
        for _k, _v in extra.items():
            if _v != "" and _v is not None:
                it[_k] = str(_v)
        assert all(isinstance(v, str) for v in it.values()), ("non-string index field", u, it)
        items.append(it)

# ---- books (live catalogue, sitemap-validated) ----
lite_path = ROOT / "translations/index-lite.json"
if lite_path.exists():
    lite = json.loads(lite_path.read_text(encoding="utf-8"))
else:
    with urllib.request.urlopen(BASE + "/translations/index-lite.json", timeout=60) as r:
        lite = json.loads(r.read().decode("utf-8"))
# reader fallback: books without a landing page are still readable —
# reader.html?id=vn/<base> loads /txt/<base>.txt (verified pattern).
txt_list = ROOT / "scripts/helper-data/txt-files.txt"
txt_bases = set()
if txt_list.exists():
    txt_bases = {ln.strip()[:-4] for ln in txt_list.read_text(encoding="utf-8").splitlines()
                 if ln.strip().endswith(".txt")}
nb = nr = 0
nskip = 0
for b in lite:
    u = f"/ban-dich/{b['slug']}.html"
    topics = " · ".join(b.get("topics") or [])
    _au = b.get("author", "")
    # Phase 1.4 facets (books only): author / topics / level / review status.
    _fac = {"a": _au, "tp": topics, "lv": str(b.get("level") or ""),
            "st": b.get("review_status") or "ai-draft"}
    if alive(u):
        add(b["short"], _au, u, "Sách", topics, **_fac); nb += 1
    else:
        base = b["slug"].rsplit("/", 1)[-1]
        if base in txt_bases:
            add(b["short"], _au, f"/reader.html?id=vn/{base}", "Sách", topics, **_fac); nr += 1
        else:
            nskip += 1
print(f"books indexed: {nb} landing pages + {nr} reader links of {len(lite)} "
      f"({nskip} catalogue entries have neither a landing page nor a txt file)")
sitemap_only = sorted({u.replace(BASE, "") for u in live_urls if "/ban-dich/" in u}
                      - {i["u"] for i in items if i["g"] == "Sách"})
print(f"note: {len(sitemap_only)} /ban-dich/ pages in the sitemap are NOT in the "
      f"catalogue (index-lite) — they are invisible to book search as landing pages")

# ---- Bible books + chapter summaries ----
books66 = json.loads((APP / "data/books.json").read_text(encoding="utf-8"))
names = {b["id"]: b["name"] for b in books66}
for b in books66:
    add(b["name"], "Sách Kinh Thánh", f"/kinh-thanh/{b['id']}/1.html", "Kinh Thánh")
cs = json.loads((ROOT / "data/chapter-summaries.json").read_text(encoding="utf-8"))["entries"]
for key, v in cs.items():
    bid, ch = key.rsplit(":", 1)
    add(f"{names.get(bid, bid)} {ch}", v.get("summary_vi", "")[:160],
        f"/kinh-thanh/{bid}/{ch}.html", "Kinh Thánh", v.get("summary_vi", ""))
print(f"bible indexed: {len(books66)} books + {len(cs)} chapters")

# ---- Phase 4: Bible study (characters, topics, book intros, timeline, maps) ----
nv = json.loads((ROOT / "data/nhanvat.json").read_text(encoding="utf-8"))
for e in nv:
    add(e["name"], "Nhân vật Kinh Thánh", f"/nhan-vat/{e['id']}.html", "Kinh Thánh", e.get("bio", ""))
tp = json.loads((ROOT / "data/topics.json").read_text(encoding="utf-8"))
for e in tp:
    add(e["title"], "Chủ đề Kinh Thánh", f"/chu-de-kinh-thanh/{e['id']}.html", "Kinh Thánh", e.get("intro", ""))
for b in books66:
    nch, nver = len(b["nc"]), sum(b["nc"])
    add(f"Giới thiệu sách {b['name']}", f"Giới thiệu sách · {nch} chương · {nver} câu",
        f"/kinh-thanh/gioi-thieu/{b['id']}.html", "Kinh Thánh",
        cs.get(f"{b['id']}:1", {}).get("summary_vi", ""))
add("Nhân vật Kinh Thánh", "50 nhân vật · A-đam đến Giu-đa", "/nhan-vat/", "Kinh Thánh")
add("Chủ đề Kinh Thánh", "20 chủ đề · Năm Sola · TULIP · Đời sống Cơ Đốc", "/chu-de-kinh-thanh/", "Kinh Thánh")
add("Giới thiệu các sách Kinh Thánh", "66 sách · tóm tắt từng chương", "/kinh-thanh/gioi-thieu/", "Kinh Thánh")
add("Dòng thời gian Kinh Thánh", "Từ Áp-ra-ham đến Khải Huyền", "/dong-thoi-gian-kinh-thanh.html", "Kinh Thánh")
add("Bản đồ & hành trình Kinh Thánh", "Xuất Hành · Ca-na-an · Ga-li-lê · Phao-lô · Giê-ru-sa-lem", "/ban-do-kinh-thanh.html", "Kinh Thánh")
add("Nghiên cứu Kinh Thánh", "Nhân vật · Chủ đề · Giới thiệu sách · Dòng thời gian · Bản đồ", "/nghien-cuu-kinh-thanh.html", "Kinh Thánh")
print(f"study indexed: {len(nv)} characters + {len(tp)} topics + {len(books66)} book intros + 6 hub pages")

# ---- Phase 5: engagement & quality (dashboard, tracker, roadmap) ----
add("Bảng đọc của tôi", "Sách đang đọc · đã đọc xong · đã lưu · dấu trang — chỉ trên thiết bị này",
    "/bang-doc-sach.html", "Công Cụ",
    "tiến độ đọc của tôi đang đọc đã đọc xong đã lưu dấu trang tiếp tục đọc")
add("Theo dõi dự án dịch thuật", "Còn bao nhiêu sách chưa dịch · vòng dịch mới nhất · chất lượng bản dịch",
    "/theo-doi-dich-thuat.html", "Công Cụ",
    "dự án dịch thuật hàng đợi còn lại vòng dịch Burroughs kiểm tra chất lượng")
add("Lộ trình phát triển", "Những giai đoạn đã hoàn tất, đang làm và còn chờ — việc nào cần người giúp",
    "/lo-trinh-phat-trien.html", "Công Cụ",
    "lộ trình phát triển giai đoạn kế hoạch tương lai cần người giúp")
print("phase5 indexed: 3 pages")

# ---- Phase 6: Ask the library (retrieval, no generated answers) ----
add("Hỏi Thư Viện", "Tìm đoạn văn theo câu hỏi · trích dẫn về trang gốc · không tự soạn câu trả lời",
    "/hoi-thu-vien.html", "Công Cụ",
    "hỏi thư viện hỏi sách tìm đoạn văn trích dẫn câu hỏi đáp án")
print("phase6 indexed: 1 page")

# ---- catechism ----
cat = json.loads((ROOT / "data/catechism-wsc.json").read_text(encoding="utf-8"))
for q in cat["questions"]:
    add(f"Câu {q['number']}: {q['question_vi']}", q["answer_vi"][:110],
        f"/giao-ly/cau-{q['number']}.html", "Giáo Lý", q["answer_vi"])

# ---- encyclopedia ----
enc = json.loads((ROOT / "data/encyclopedia.json").read_text(encoding="utf-8"))
for e in enc["entries"]:
    add(e["term_vi"], f"{e.get('term_en','')} — {e['definition_short_vi'][:90]}",
        f"/bach-khoa/{e['slug']}.html", "Bách Khoa", e.get("body_vi") or "")

# ---- devotions ----
dev = json.loads((ROOT / "data/devotions.json").read_text(encoding="utf-8"))
for d in dev["entries"]:
    body = " ".join(d.get("paras") or []) + " " + (d.get("summary") or "") \
        + " " + (d.get("reflection_question") or "") + " " + (d.get("prayer") or "")
    add(d["title"], f"Tĩnh nguyện {d['day']}/{d['month']} · {d.get('ref','')}",
        f"/suy-ngam/{d['month']:02d}-{d['day']:02d}.html", "Tĩnh Nguyện", body)

# ---- answers ----
ans = json.loads((ROOT / "data/answers.json").read_text(encoding="utf-8"))
for a in ans["entries"]:
    add(a["question_vi"], a["answer_short_vi"][:110], f"/hoi-dap/{a['slug']}.html",
        "Hỏi Đáp", " ".join(a.get("body_vi") or []))

# ---- sermons ----
ser = json.loads((ROOT / "data/sermons.json").read_text(encoding="utf-8"))
for s in ser["entries"]:
    add(s["title_vi"], f"{s['preacher']} · {s.get('text_ref_vi','')}",
        f"/bai-giang/{s['slug']}.html", "Bài Giảng")
for s in ser["vi_sermons"]:
    add(s["title_vi"], f"{s['preacher']} · {s.get('text_ref_vi','')}", s["local_url"], "Bài Giảng")
for s in ser["collections"]:
    add(s["title_vi"], s.get("author", ""), s["url"], "Bài Giảng")

# ---- hymns ----
hym = json.loads((ROOT / "data/hymns.json").read_text(encoding="utf-8"))
for h in hym["entries"]:
    def _flat(verses):
        return " ".join(" ".join(v) for v in (verses or []))
    hymn_body = " ".join(x for x in [
        h.get("tune") or "", h.get("tune_by") or "", h.get("meter") or "",
        _flat(h.get("vi")), _flat(h.get("en"))] if x)
    add(h["title_vi"], f"{h['title_en']} · {h['words_by']}", f"/thanh-ca/{h['slug']}.html",
        "Thánh Ca", hymn_body)

# ---- journal ----
jou = json.loads((ROOT / "data/journal.json").read_text(encoding="utf-8"))
def _txt(v):
    # prose fields come as plain strings, paragraph lists, or (key_terms)
    # lists of {term, def} dicts — flatten all of them to searchable text
    if isinstance(v, list):
        parts = []
        for x in v:
            if isinstance(x, dict):
                parts += [str(y) for y in x.values()]
            else:
                parts.append(str(x))
        return " ".join(parts)
    return v or ""

for a in jou["articles"]:
    add(a["title_vi"], a["author"], f"/tap-chi/{a['slug']}.html", "Tạp Chí",
        _txt(a.get("intro_vi")) + " " + _txt(a.get("excerpt_vi")))

# ---- church directory ----
chu = json.loads((ROOT / "data/churches.json").read_text(encoding="utf-8"))
for e in chu["entries"]:
    add(e["name"], f"{e.get('address','')} · {e.get('confession','')}", "/danh-ba/", "Hội Thánh")

# ---- academy: courses + lessons ----
acad = json.loads((ROOT / "data/academy.json").read_text(encoding="utf-8"))
course_titles = {}
for cert in acad["thirdmill_certificates"]:
    for c in cert["courses"]:
        course_titles[c["slug"]] = c["title_vi"]
        add(c["title_vi"], f"Khóa học · {cert['certificate_vi']} · {c.get('title_en','')} · Thirdmill",
            f"/hoc-vien/khoa/{c['slug']}/", "Học Viện")
comp = json.loads((ROOT / "data/thirdmill-companions.json").read_text(encoding="utf-8"))
for c in comp["companions"]:
    add(c.get("title_vi") or c.get("title_en", ""),
        f"Bài học · {course_titles.get(c['course_slug'], '')} · {c.get('title_en','')} · Thirdmill",
        f"/hoc-vien/khoa/{c['course_slug']}/", "Học Viện",
        _txt(c.get("summary_vi")) + " " + _txt(c.get("key_terms")))

out = {"generated": datetime.date.today().isoformat(), "count": len(items), "items": items}
(ROOT / "data/search-index.json").write_text(
    json.dumps(out, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
print(f"search index: {len(items)} items")

# ---- search page ----
hub = (ROOT / "hub.html").read_text(encoding="utf-8")
font_link = re.search(r'<link rel="stylesheet" href="data:text/css;base64,[^>]+>', hub).group(0)
style = re.search(r"<style>(.*?)</style>", hub, re.S).group(1)
header = re.search(r"<header.*?</header>", hub, re.S).group(0)
footer = re.search(r"<footer.*?</footer>", hub, re.S).group(0)

def rebase(block):
    block = block.replace('href="#top"', 'href="/"')
    return re.sub(r'href="#([a-z-]+)"', r'href="/#\1"', block)
header, footer = rebase(header), rebase(footer)

EXTRA_CSS = """
      /* nav-offset fallback: builders extract <main id=top> from hub.html;
         if a rebuild ever drops that wrapper, anchored sections still clear the fixed header */
      section[id] { scroll-margin-top: 76px; }

      /* ---------- search page ---------- */
      .crumb { font-size: 13.5px; color: var(--ink-soft); margin: 26px 0 6px; }
      .crumb a { color: var(--burgundy); text-decoration: none; }
      .cat-head { text-align: center; padding: 18px 0 6px; }
      .cat-head .kicker { color: var(--gold-text); font-weight: 700; letter-spacing: .08em; text-transform: uppercase; font-size: 12.5px; }
      .cat-head h1 { font-family: "Playfair Display", serif; font-size: clamp(25px, 4.4vw, 36px); margin: 8px 0 10px; line-height: 1.3; }
      .big-search { max-width: 640px; margin: 14px auto 6px; display: flex; gap: 8px; }
      .big-search input { flex: 1; padding: 13px 16px; border: 1px solid var(--line); border-radius: 999px; font: inherit; font-size: 16px; background: var(--surface); color: var(--ink); }
      .group-head { max-width: 760px; margin: 26px auto 4px; font-size: 13px; font-weight: 700; letter-spacing: .07em; text-transform: uppercase; color: var(--gold-text); }
      .qa-cards { display: grid; gap: 12px; max-width: 760px; margin: 10px auto 8px; }
      .qa-card { display: block; background: var(--surface); border: 1px solid var(--line); border-radius: var(--radius); padding: 16px 20px; box-shadow: var(--shadow); text-decoration: none; }
      .qa-card h3 { font-family: "Noto Serif", serif; font-size: 17px; margin: 0 0 4px; color: var(--ink); line-height: 1.45; }
      .qa-card p { margin: 0; color: var(--ink-soft); font-size: 14px; line-height: 1.55; }
      .qa-card:hover h3 { color: var(--burgundy); }
      .status { text-align: center; color: var(--ink-soft); font-size: 15px; margin: 18px 0 4px; }

      /* Phase 1.4: filter row (thu-vien select pattern) */
      .filters { display: flex; gap: 8px; flex-wrap: wrap; justify-content: center; margin: 12px auto 2px; max-width: 760px; }
      .filters select { padding: 9px 12px; border: 1px solid var(--line); border-radius: 999px; background: var(--surface); color: var(--ink); font: 14px "Be Vietnam Pro", system-ui, sans-serif; max-width: 13rem; }
      .filters select:disabled { opacity: .55; }
"""

SEARCH_JS = """
<script>
  (function () {
    var b = document.getElementById("menuBtn"), n = document.querySelector("nav.main");
    if (b && n) b.addEventListener("click", function () {
      var open = n.style.display === "flex";
      n.style.display = open ? "" : "flex";
      b.setAttribute("aria-expanded", String(!open));
    });
    var top = document.getElementById("toTop");
    if (top) top.addEventListener("click", function () { window.scrollTo({ top: 0, behavior: "smooth" }); });

    function norm(s) {
      return (s || "").toLowerCase().normalize("NFD").replace(/[\\u0300-\\u036f]/g, "").replace(/đ/g, "d");
    }
    var ORDER = ["Kinh Thánh", "Sách", "Giáo Lý", "Bách Khoa", "Tĩnh Nguyện", "Hỏi Đáp", "Học Viện", "Bài Giảng", "Thánh Ca", "Tạp Chí", "Hội Thánh"];
    var input = document.getElementById("q"), box = document.getElementById("results"),
        status = document.getElementById("status"), INDEX = null, cache = [];

    // Phase 1.4: filter selects (thu-vien pattern). Group/author/topic
    // options are filled from the index once it loads; level/status are
    // fixed sets in the HTML. A filter on a facet only matches items that
    // carry it, so topic/author/level/status narrow to books (the only
    // group with a/tp/lv/st facets).
    function filters() {
      return {
        g: document.getElementById("fGroup").value,
        a: document.getElementById("fAuthor").value,
        t: document.getElementById("fTopic").value,
        l: document.getElementById("fLevel").value,
        s: document.getElementById("fStatus").value
      };
    }
    function facetOk(it, f) {
      if (f.g && it.g !== f.g) return false;
      if (f.a && it.a !== f.a) return false;
      if (f.t && (it.tp || "").split(" · ").indexOf(f.t) === -1) return false;
      if (f.l && it.lv !== f.l) return false;
      if (f.s && it.st !== f.s) return false;
      return true;
    }
    function populateFilters() {
      var gSel = document.getElementById("fGroup");
      ORDER.forEach(function (g) {
        var o = document.createElement("option"); o.value = g; o.textContent = g; gSel.appendChild(o);
      });
      var authors = {}, topics = {};
      INDEX.items.forEach(function (it) {
        if (it.a) authors[it.a] = true;
        (it.tp || "").split(" · ").forEach(function (t) { if (t) topics[t] = true; });
      });
      var aSel = document.getElementById("fAuthor");
      Object.keys(authors).sort().forEach(function (a) {
        var o = document.createElement("option"); o.value = a; o.textContent = a; aSel.appendChild(o);
      });
      var tSel = document.getElementById("fTopic");
      Object.keys(topics).sort().forEach(function (t) {
        var o = document.createElement("option"); o.value = t; o.textContent = t; tSel.appendChild(o);
      });
    }
    function prepare() {
      cache = INDEX.items.map(function (it) {
        return { it: it, nt: norm(it.t), ns: norm(it.s), nb: norm(it.b || "") };
      });
      populateFilters();
    }
    function esc(s) {
      return s.replace(/[&<>"']/g, function (c) {
        return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
      });
    }
    function render(q) {
      box.innerHTML = "";
      var f = filters();
      var hasFilter = f.g || f.a || f.t || f.l || f.s;
      var words = norm(q).split(/\\s+/).filter(Boolean);
      if (!words.length && !hasFilter) { status.textContent = "Nhập từ khóa để tìm trong toàn bộ trang — sách, Kinh Thánh, giáo lý, bách khoa, tĩnh nguyện, bài giảng, thánh ca và học viện. Gõ không dấu cũng được."; return; }
      if (!INDEX) { status.textContent = "Đang tải chỉ mục tìm kiếm…"; return; }
      var note = document.getElementById("filterNote");
      if (note) note.hidden = !(f.a || f.t || f.l || f.s);
      var phrase = words.join(" "), groups = {}, total = 0;
      cache.forEach(function (c) {
        if (!facetOk(c.it, f)) return;
        // Title 3, subtitle 2, body text 1 per word — a body-only hit still
        // finds the page (devotion text, hymn lyrics, tune name), but a
        // title hit always ranks above it.
        var hay = c.nt + " " + c.ns + " " + c.nb, score = 0, ok = true, bodyOnly = true;
        for (var i = 0; i < words.length; i++) {
          if (hay.indexOf(words[i]) === -1) { ok = false; break; }
          if (c.nt.indexOf(words[i]) !== -1) { score += 3; bodyOnly = false; }
          else if (c.ns.indexOf(words[i]) !== -1) { score += 2; bodyOnly = false; }
          else score += 1;
        }
        if (!ok) return;
        if (!words.length) bodyOnly = false;
        if (words.length && c.nt.indexOf(phrase) !== -1) score += 3;
        else if (words.length && c.ns.indexOf(phrase) !== -1) score += 2;
        else if (words.length && c.nb.indexOf(phrase) !== -1) score += 1;
        (groups[c.it.g] = groups[c.it.g] || []).push({ it: c.it, score: score, bodyOnly: bodyOnly });
        total++;
      });
      if (!total) {
        status.textContent = words.length
          ? "Không tìm thấy kết quả cho “" + q + "”" + (hasFilter ? " với bộ lọc đã chọn" : "") + ". Thử ít từ hơn, hoặc kiểm tra chính tả — gõ không dấu vẫn tìm được."
          : "Không có mục nào khớp với bộ lọc đã chọn.";
        return;
      }
      status.textContent = "Tìm thấy " + total + " kết quả" + (words.length ? " cho “" + q + "”" : "") + (hasFilter ? " (đã lọc)" : "") + ".";
      ORDER.forEach(function (g) {
        var list = groups[g];
        if (!list) return;
        list.sort(function (a, b2) { return b2.score - a.score; });
        var head = document.createElement("div");
        head.className = "group-head";
        head.textContent = g + " · " + list.length;
        box.appendChild(head);
        var wrap = document.createElement("div");
        wrap.className = "qa-cards";
        list.slice(0, 10).forEach(function (r) {
          var a = document.createElement("a");
          a.className = "qa-card"; a.href = r.it.u;
          // Body-only match: show where it matched instead of the generic
          // subtitle, so the result explains itself.
          var sub = r.it.s;
          if (r.bodyOnly && r.it.b) sub = "…" + r.it.b.slice(0, 110) + "…";
          a.innerHTML = "<h3>" + esc(r.it.t) + "</h3>" + (sub ? "<p>" + esc(sub) + "</p>" : "");
          wrap.appendChild(a);
        });
        box.appendChild(wrap);
        if (list.length > 10) {
          var more = document.createElement("p");
          more.className = "status";
          more.textContent = "… và " + (list.length - 10) + " kết quả nữa trong mục " + g + " — hãy thêm từ khóa để thu hẹp.";
          box.appendChild(more);
        }
      });
    }
    // Phase 1.4: re-render when a filter select changes.
    ["fGroup", "fAuthor", "fTopic", "fLevel", "fStatus"].forEach(function (id) {
      document.getElementById(id).addEventListener("change", function () { render(input.value); });
    });
    var t = null;
    input.addEventListener("input", function () {
      clearTimeout(t);
      t = setTimeout(function () { render(input.value); }, 130);
    });
    document.getElementById("searchFormPage").addEventListener("submit", function (e) {
      e.preventDefault(); render(input.value);
    });
    var q0 = new URLSearchParams(location.search).get("q") || "";
    if (q0) input.value = q0;
    fetch("/data/search-index.json")
      .then(function (r) { return r.json(); })
      .then(function (d) { INDEX = d; prepare(); render(input.value); })
      .catch(function () { status.textContent = "Không tải được chỉ mục tìm kiếm. Xin thử tải lại trang."; });
    render(input.value);
  })();
</script>
"""

page = f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>Tìm Kiếm | Reformed Vietnam</title>
<meta name="description" content="Tìm trong toàn bộ Reformed Vietnam: thư viện sách, Kinh Thánh, giáo lý, bách khoa thần học, tĩnh nguyện, bài giảng, thánh ca và học viện — gõ không dấu cũng được." />
<link rel="canonical" href="{BASE}/tim-kiem/" />
<meta property="og:type" content="website" />
<meta property="og:title" content="Tìm Kiếm | Reformed Vietnam" />
<meta property="og:url" content="{BASE}/tim-kiem/" />
<meta property="og:image" content="{BASE}/og.jpg" />
<link rel="icon" href="/favicon.svg" type="image/svg+xml" />
{font_link}
<style>{style}{EXTRA_CSS}</style>
</head>
<body id="top">
{header}
<main class="wrap">
  <p class="crumb"><a href="/">Trang chủ</a> · Tìm Kiếm</p>
  <div class="cat-head">
    <div class="kicker">Tìm Kiếm</div>
    <h1>Tìm Trong Toàn Bộ Trang</h1>
  </div>
  <form class="big-search" id="searchFormPage" role="search">
    <input id="q" type="search" name="q" placeholder="Tìm sách, thuật ngữ, câu hỏi, bài giảng… (gõ không dấu cũng được)" aria-label="Tìm kiếm" autocomplete="off" />
    <button class="btn solid" type="submit">Tìm</button>
  </form>
  <p class="status">Muốn hỏi bằng câu đầy đủ? <a href="/hoi-thu-vien.html">Hỏi Thư Viện</a> — tìm đoạn văn có trích dẫn, không tự soạn câu trả lời. Trên trang sách, dùng “Hỏi sách này” để hỏi riêng một cuốn.</p>
  <div class="filters" id="filters" aria-label="Bộ lọc kết quả">
    <select id="fGroup" aria-label="Mục"><option value="">Tất cả các mục</option></select>
    <select id="fAuthor" aria-label="Tác giả"><option value="">Tất cả tác giả</option></select>
    <select id="fTopic" aria-label="Chủ đề"><option value="">Tất cả chủ đề</option></select>
    <select id="fLevel" aria-label="Độ khó"><option value="">Mọi độ khó</option><option value="1">Mới tin Chúa</option><option value="2">Đang lớn lên</option><option value="3">Học sâu</option></select>
    <select id="fStatus" aria-label="Trạng thái duyệt"><option value="">Mọi trạng thái</option><option value="ai-draft">AI, chưa duyệt</option><option value="in-review">Đang được duyệt</option><option value="reviewed">Đã được duyệt</option></select>
  </div>
  <p class="status" id="filterNote" hidden>Bộ lọc tác giả / chủ đề / độ khó / trạng thái chỉ áp dụng cho mục Sách — các mục khác không có dữ liệu này.</p>
  <p class="status" id="status">Đang tải chỉ mục tìm kiếm…</p>
  <div id="results"></div>
</main>
{footer}
{SEARCH_JS}
</body>
</html>"""
OUT = ROOT / "tim-kiem"
OUT.mkdir(exist_ok=True)
(OUT / "index.html").write_text(page, encoding="utf-8")

sm = ROOT / "sitemap.xml"
t = sm.read_text(encoding="utf-8")
loc = f"<loc>{BASE}/tim-kiem/</loc>"
if loc not in t:
    t = t.replace("</urlset>", f"<url>{loc}<changefreq>monthly</changefreq></url></urlset>")
    sm.write_text(t, encoding="utf-8")
    print("sitemap: /tim-kiem/ added")
print("DONE")

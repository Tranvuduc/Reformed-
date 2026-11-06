#!/usr/bin/env python3
"""Build the Catechism module (Westminster Shorter Catechism) for Reformed Vietnam.

Source of truth (owner ruling 2026-11-06: integrate the Bible app's content verbatim):
  - WSC text: Kinh-thanh-moi-ngay/data/giaoly.json (107 Q&A with proof refs)
  - Proof verse texts: the app repo's data/bible/*.json (1934 Vietnamese Bible)

Outputs (into the hub repo):
  - data/catechism-wsc.json   (Build Guide §10 shape, with verse texts filled in)
  - giao-ly/index.html        (module landing: today's question, modes, full index)
  - giao-ly/cau-1..107.html   (one question per page: prev/next, expandable proofs,
                               memorisation toggle, share buttons, AI label)
  - giao-ly/trac-nghiem.html  (simple quiz mode, reads the data JSON)
  - giao-ly-hang-ngay.html    (daily catechism page rebuilt on the canonical text)
  - sitemap.xml               (module URLs appended if missing)

Design system, header and footer are sliced from hub.html so module pages match
the homepage exactly. Run from the repo root.
"""
import json, re, sys, html, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
APP = ROOT.parent / "bible-app"  # sparse checkout of Tranvuduc/Kinh-thanh-moi-ngay
BASE = "https://reformed-vietnam.vercel.app"

# ---------- load sources ----------
giaoly = json.loads((APP / "data/giaoly.json").read_text(encoding="utf-8"))
assert len(giaoly) == 107, len(giaoly)

books = {}
bible_dir = APP / "data" / "bible"
for f in bible_dir.glob("*.json"):
    books[f.stem] = json.loads(f.read_text(encoding="utf-8"))

from text_corrections import fix_verse

def verse_text(key):
    book, ch, vs = key.split(":")
    return fix_verse(book, int(ch), int(vs),
                     books[book]["ch"][int(ch) - 1][int(vs) - 1]).strip()

questions, missing = [], []
for e in giaoly:
    proofs = []
    for r in e.get("refs", []):
        try:
            txt = verse_text(r["key"])
        except Exception:
            missing.append(r["key"]); txt = ""
        proofs.append({"ref_vi": r["ref"], "text_vi": txt, "key": r["key"]})
    questions.append({
        "number": e["n"], "question_vi": e["q"], "answer_vi": e["a"],
        "proof_texts": proofs,
    })
if missing:
    print("UNRESOLVED proof keys:", missing); sys.exit(1)
print(f"proof texts resolved: {sum(len(q['proof_texts']) for q in questions)} refs across 107 questions")

data = {
    "catechism": "wsc",
    "title_vi": "Tín Lý Yếu Lược Westminster (Westminster Shorter Catechism, 1647)",
    "source": "Kinh Thánh Mỗi Ngày — WSC translation",
    "label": "Bản dịch AI, chưa duyệt",
    "count": 107,
    "questions": questions,
}
(ROOT / "data/catechism-wsc.json").write_text(
    json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
print("data/catechism-wsc.json written (Guide §10 shape)")

# ---------- template parts from hub.html ----------
hub = (ROOT / "hub.html").read_text(encoding="utf-8")
font_link = re.search(r'<link rel="stylesheet" href="data:text/css;base64,[^>]+>', hub).group(0)
style = re.search(r"<style>(.*?)</style>", hub, re.S).group(1)
header = re.search(r"<header.*?</header>", hub, re.S).group(0)
footer = re.search(r"<footer.*?</footer>", hub, re.S).group(0)

def rebase(block):
    block = block.replace('href="#top"', 'href="/"')
    block = re.sub(r'href="#([a-z-]+)"', r'href="/#\1"', block)
    return block
header, footer = rebase(header), rebase(footer)

EXTRA_CSS = """
      /* ---------- catechism module ---------- */
      .crumb { font-size: 13.5px; color: var(--ink-soft); margin: 26px 0 6px; }
      .crumb a { color: var(--burgundy); text-decoration: none; }
      .cat-head { text-align: center; padding: 18px 0 6px; }
      .cat-head .kicker { color: var(--gold-text); font-weight: 700; letter-spacing: .08em; text-transform: uppercase; font-size: 12.5px; }
      .cat-head h1 { font-family: "Playfair Display", serif; font-size: clamp(26px, 4.6vw, 38px); margin: 8px 0 10px; }
      .cat-panel { max-width: 680px; margin: 18px auto 8px; background: var(--surface); border: 1px solid var(--line); border-radius: var(--radius); padding: 26px 26px 20px; box-shadow: var(--shadow); }
      .cat-q { font-family: "Noto Serif", serif; font-size: 20px; font-weight: 700; line-height: 1.5; }
      .cat-a { font-family: "Noto Serif", serif; font-size: 17.5px; line-height: 1.75; margin-top: 12px; }
      .cat-a.hidden-a { visibility: hidden; }
      .ai-label { display: inline-block; font-size: 12px; font-weight: 600; color: var(--burgundy); background: color-mix(in srgb, var(--burgundy) 9%, transparent); border: 1px solid color-mix(in srgb, var(--burgundy) 35%, transparent); padding: 2px 9px; border-radius: 999px; }
      .proof { border-top: 1px solid var(--line); padding: 9px 0; }
      .proof summary { cursor: pointer; font-weight: 600; color: var(--burgundy); font-size: 15px; }
      .proof p { font-family: "Noto Serif", serif; font-size: 15.5px; line-height: 1.7; margin: 8px 0 4px; color: var(--ink); }
      .cat-nav { display: flex; justify-content: space-between; gap: 10px; max-width: 680px; margin: 16px auto 6px; flex-wrap: wrap; }
      .share-row { display: flex; gap: 10px; justify-content: center; margin: 18px 0 4px; flex-wrap: wrap; }
      .cat-index { max-width: 860px; margin: 10px auto 30px; }
      .cat-index li { margin: 0 0 8px; line-height: 1.55; }
      .cat-index a { color: var(--ink); text-decoration: none; }
      .cat-index a:hover { color: var(--burgundy); text-decoration: underline; }
      .cat-index .n { color: var(--gold-text); font-weight: 700; margin-right: 6px; }
      .modes { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; max-width: 860px; margin: 20px auto; }
      @media (max-width: 720px) { .modes { grid-template-columns: 1fr; } }
      .mode-card { background: var(--surface); border: 1px solid var(--line); border-radius: var(--radius); padding: 20px; }
      .mode-card h3 { margin: 0 0 8px; font-family: "Playfair Display", serif; }
      .quiz-opt { display: block; width: 100%; text-align: left; margin: 8px 0; padding: 13px 16px; border: 1px solid var(--line); border-radius: 10px; background: var(--surface); font: inherit; font-size: 15.5px; cursor: pointer; }
      .quiz-opt.correct { border-color: var(--green); background: color-mix(in srgb, var(--green) 12%, transparent); }
      .quiz-opt.wrong { border-color: var(--burgundy); background: color-mix(in srgb, var(--burgundy) 10%, transparent); }
"""

MINI_JS = """
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
  })();
</script>
"""

def esc(s): return html.escape(s, quote=True)

def head(title, desc, url):
    return f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}" />
<link rel="canonical" href="{url}" />
<meta property="og:type" content="article" />
<meta property="og:title" content="{esc(title)}" />
<meta property="og:description" content="{esc(desc)}" />
<meta property="og:url" content="{url}" />
<meta property="og:image" content="{BASE}/og.jpg" />
<link rel="icon" href="/favicon.svg" type="image/svg+xml" />
{font_link}
<style>{style}{EXTRA_CSS}</style>
</head>"""

def share_row(url, text):
    u = html.escape(url, quote=True)
    return (f'<div class="share-row">'
            f'<a class="btn solid" target="_blank" rel="noopener" href="https://www.facebook.com/sharer/sharer.php?u={u}">Chia sẻ Facebook</a>'
            f'<a class="btn" target="_blank" rel="noopener" href="https://sp.zalo.me/share_inline?url={u}">Chia sẻ Zalo</a></div>')

def proofs_html(q):
    if not q["proof_texts"]:
        return ""
    items = "".join(
        f'<details class="proof"><summary>{esc(p["ref_vi"])}</summary><p>{esc(p["text_vi"])}</p></details>'
        for p in q["proof_texts"])
    return f'<div style="margin-top:16px"><h3 style="margin:0 0 4px">Căn cứ Kinh Thánh <span style="font-weight:400;font-size:13.5px;color:var(--ink-soft)">(bấm để đọc câu gốc — bản 1934)</span></h3>{items}</div>'

OUT = ROOT / "giao-ly"
OUT.mkdir(exist_ok=True)

# ---------- question pages ----------
for q in questions:
    n = q["number"]
    url = f"{BASE}/giao-ly/cau-{n}.html"
    title = f"Câu {n}: {q['question_vi']} | Tín Lý Yếu Lược Westminster"
    desc = q["answer_vi"][:155]
    prev_link = (f'<a class="btn" href="/giao-ly/cau-{n-1}.html">← Câu {n-1}</a>' if n > 1
                 else '<a class="btn" href="/giao-ly/">← Mục lục</a>')
    next_link = (f'<a class="btn solid" href="/giao-ly/cau-{n+1}.html">Câu {n+1} →</a>' if n < 107
                 else '<a class="btn solid" href="/giao-ly/">Về mục lục →</a>')
    page = f"""{head(title, desc, url)}
<body id="top">
{header}
<main class="wrap">
  <p class="crumb"><a href="/">Trang chủ</a> · <a href="/giao-ly/">Giáo Lý</a> · Câu {n}</p>
  <div class="cat-head">
    <div class="kicker">Tín Lý Yếu Lược Westminster · Câu {n} / 107</div>
    <p style="margin-top:10px"><span class="ai-label">Bản dịch AI, chưa duyệt</span></p>
  </div>
  <article class="cat-panel">
    <h1 class="cat-q">{esc(q['question_vi'])}</h1>
    <div class="cat-a" id="answerBody">{esc(q['answer_vi'])}</div>
    <p style="margin-top:14px"><button class="btn" type="button" id="memoBtn">Chế độ ghi nhớ: ẩn đáp án</button></p>
    {proofs_html(q)}
  </article>
  <nav class="cat-nav">{prev_link}<a class="btn" href="/giao-ly/">Mục lục 107 câu</a>{next_link}</nav>
  {share_row(url, q['question_vi'])}
  <p style="text-align:center;color:var(--ink-soft);font-size:13px;margin-bottom:34px">Nguồn bản dịch: Kinh Thánh Mỗi Ngày — Westminster Shorter Catechism (1647), thuộc phạm vi công cộng.</p>
</main>
{footer}
{MINI_JS}
<script>
  (function () {{
    var btn = document.getElementById("memoBtn"), body = document.getElementById("answerBody"), hidden = false;
    btn.addEventListener("click", function () {{
      hidden = !hidden;
      body.classList.toggle("hidden-a", hidden);
      btn.textContent = hidden ? "Hiện đáp án" : "Chế độ ghi nhớ: ẩn đáp án";
    }});
  }})();
</script>
</body>
</html>"""
    (OUT / f"cau-{n}.html").write_text(page, encoding="utf-8")
print("107 question pages written")

# ---------- landing page ----------
index_items = "\n".join(
    f'<li><span class="n">{q["number"]}.</span><a href="/giao-ly/cau-{q["number"]}.html">{esc(q["question_vi"])}</a></li>'
    for q in questions)
landing = f"""{head("Tín Lý Yếu Lược Westminster — 107 câu hỏi đáp | Reformed Vietnam",
                     "Học Tín Lý Yếu Lược Westminster (1647): trọn 107 câu hỏi đáp đức tin Cải Chánh, có căn cứ Kinh Thánh, chế độ ghi nhớ và trắc nghiệm.", BASE + "/giao-ly/")}
<body id="top">
{header}
<main class="wrap">
  <p class="crumb"><a href="/">Trang chủ</a> · Giáo Lý</p>
  <div class="cat-head">
    <div class="kicker">Giáo Lý · Tín Lý Yếu Lược Westminster</div>
    <h1>107 câu hỏi đáp về đức tin</h1>
    <p style="max-width:640px;margin:0 auto;color:var(--ink-soft)">Bản Tín Lý Yếu Lược Westminster (1647) tóm tắt đức tin Cơ Đốc trong 107 câu hỏi — đáp ngắn gọn. Đọc từng câu, tra cứu căn cứ Kinh Thánh ngay tại chỗ, học thuộc bằng chế độ ghi nhớ, và tự kiểm tra bằng trắc nghiệm.</p>
    <p style="margin-top:10px"><span class="ai-label">Bản dịch AI, chưa duyệt</span></p>
  </div>
  <article class="cat-panel" id="todayPanel">
    <div class="kicker" style="color:var(--gold-text);font-weight:700;font-size:12.5px;letter-spacing:.08em">CÂU HỎI HÔM NAY</div>
    <h2 class="cat-q" id="todayQ" style="margin-top:8px">{esc(questions[0]['question_vi'])}</h2>
    <div class="cat-a" id="todayA">{esc(questions[0]['answer_vi'])}</div>
    <p style="margin-top:14px"><a class="btn solid" id="todayLink" href="/giao-ly/cau-1.html">Mở trang câu này →</a></p>
  </article>
  <div class="modes">
    <div class="mode-card"><h3>Đọc từng câu</h3><p>Mỗi câu một trang riêng, có câu trước / câu sau và căn cứ Kinh Thánh mở ngay tại chỗ.</p><a class="btn solid" href="/giao-ly/cau-1.html">Bắt đầu từ Câu 1 →</a></div>
    <div class="mode-card"><h3>Ghi nhớ</h3><p>Trong từng trang câu hỏi, bật chế độ ghi nhớ để ẩn đáp án và tự nhẩm trước khi xem.</p><a class="btn" href="/giao-ly/cau-1.html">Thử với Câu 1 →</a></div>
    <div class="mode-card"><h3>Trắc nghiệm</h3><p>10 câu hỏi trắc nghiệm ngẫu nhiên từ trọn bộ 107 câu, chấm điểm ngay.</p><a class="btn" href="/giao-ly/trac-nghiem.html">Làm trắc nghiệm →</a></div>
  </div>
  {share_row(BASE + "/giao-ly/", "Tín Lý Yếu Lược Westminster")}
  <h2 style="font-family:'Playfair Display',serif;text-align:center;margin-top:26px">Mục lục trọn 107 câu</h2>
  <ol class="cat-index" style="list-style:none;padding:0">
{index_items}
  </ol>
  <p style="text-align:center;color:var(--ink-soft);font-size:13px;margin-bottom:34px">Nguồn bản dịch: Kinh Thánh Mỗi Ngày — Westminster Shorter Catechism (1647), thuộc phạm vi công cộng.</p>
</main>
{footer}
{MINI_JS}
<script>
  fetch("/data/catechism-wsc.json").then(function (r) {{ return r.json(); }}).then(function (d) {{
    var now = new Date(); var start = new Date(now.getFullYear(), 0, 0);
    var doy = Math.floor((now - start) / 864e5);
    var q = d.questions[doy % 107];
    document.getElementById("todayQ").textContent = q.question_vi;
    document.getElementById("todayA").textContent = q.answer_vi;
    document.getElementById("todayLink").href = "/giao-ly/cau-" + q.number + ".html";
  }}).catch(function () {{}});
</script>
</body>
</html>"""
(OUT / "index.html").write_text(landing, encoding="utf-8")
print("landing page written")

# ---------- quiz page ----------
quiz = f"""{head("Trắc nghiệm Tín Lý Yếu Lược Westminster | Reformed Vietnam",
                  "Tự kiểm tra kiến thức đức tin: 10 câu trắc nghiệm ngẫu nhiên từ 107 câu Tín Lý Yếu Lược Westminster, chấm điểm ngay.", BASE + "/giao-ly/trac-nghiem.html")}
<body id="top">
{header}
<main class="wrap">
  <p class="crumb"><a href="/">Trang chủ</a> · <a href="/giao-ly/">Giáo Lý</a> · Trắc nghiệm</p>
  <div class="cat-head">
    <div class="kicker">Trắc nghiệm · Tín Lý Yếu Lược Westminster</div>
    <h1>Kiểm tra trí nhớ đức tin</h1>
    <p style="color:var(--ink-soft)">Mỗi lượt 10 câu hỏi ngẫu nhiên từ trọn bộ 107 câu. Chọn đáp án đúng nhất.</p>
    <p style="margin-top:10px"><span class="ai-label">Bản dịch AI, chưa duyệt</span></p>
  </div>
  <article class="cat-panel" id="quizPanel">
    <p id="quizStatus" style="color:var(--ink-soft)">Đang tải câu hỏi…</p>
    <h2 class="cat-q" id="quizQ"></h2>
    <div id="quizOpts"></div>
    <p id="quizFeedback" style="margin-top:12px;font-weight:600"></p>
    <p style="margin-top:10px"><button class="btn solid" type="button" id="quizNext" style="display:none">Câu tiếp theo →</button>
    <button class="btn" type="button" id="quizRestart" style="display:none">Làm lại lượt mới</button></p>
  </article>
  <p style="text-align:center;margin-bottom:34px"><a class="btn" href="/giao-ly/">← Về mục lục 107 câu</a></p>
</main>
{footer}
{MINI_JS}
<script>
  var qs = [], round = [], idx = 0, score = 0;
  function shuffle(a) {{ for (var i = a.length - 1; i > 0; i--) {{ var j = Math.floor(Math.random() * (i + 1)); var t = a[i]; a[i] = a[j]; a[j] = t; }} return a; }}
  function start(d) {{
    qs = d.questions; round = shuffle(qs.slice()).slice(0, 10); idx = 0; score = 0;
    document.getElementById("quizRestart").style.display = "none";
    show();
  }}
  function show() {{
    var q = round[idx];
    document.getElementById("quizStatus").textContent = "Câu " + (idx + 1) + " / 10 · Điểm: " + score;
    document.getElementById("quizQ").textContent = q.question_vi;
    document.getElementById("quizFeedback").textContent = "";
    document.getElementById("quizNext").style.display = "none";
    var wrong = shuffle(qs.filter(function (x) {{ return x.number !== q.number; }})).slice(0, 3);
    var opts = shuffle([q].concat(wrong));
    var box = document.getElementById("quizOpts"); box.innerHTML = "";
    opts.forEach(function (o) {{
      var b = document.createElement("button");
      b.type = "button"; b.className = "quiz-opt"; b.textContent = o.answer_vi;
      b.addEventListener("click", function () {{
        var all = box.querySelectorAll("button");
        all.forEach(function (x) {{ x.disabled = true; }});
        if (o.number === q.number) {{ b.classList.add("correct"); score++; document.getElementById("quizFeedback").textContent = "Đúng rồi! "; }}
        else {{ b.classList.add("wrong"); document.getElementById("quizFeedback").textContent = "Chưa đúng. Đáp án đúng là đáp án của Câu " + q.number + ". "; }}
        var a = document.createElement("a");
        a.href = "/giao-ly/cau-" + q.number + ".html"; a.textContent = "Đọc Câu " + q.number + " →";
        document.getElementById("quizFeedback").appendChild(a);
        document.getElementById("quizStatus").textContent = "Câu " + (idx + 1) + " / 10 · Điểm: " + score;
        var nx = document.getElementById("quizNext");
        nx.textContent = idx === 9 ? "Xem kết quả →" : "Câu tiếp theo →";
        nx.style.display = "";
      }});
      box.appendChild(b);
    }});
  }}
  document.getElementById("quizNext").addEventListener("click", function () {{
    idx++;
    if (idx >= 10) {{
      document.getElementById("quizStatus").textContent = "Hoàn thành!";
      document.getElementById("quizQ").textContent = "Bạn đạt " + score + " / 10 điểm.";
      document.getElementById("quizOpts").innerHTML = "";
      document.getElementById("quizFeedback").textContent = score >= 8 ? "Rất vững! Hãy tiếp tục học các câu tiếp theo." : "Hãy đọc lại các câu trong mục lục rồi thử lại nhé.";
      document.getElementById("quizNext").style.display = "none";
      document.getElementById("quizRestart").style.display = "";
    }} else show();
  }});
  document.getElementById("quizRestart").addEventListener("click", function () {{ start({{ questions: qs }}); }});
  fetch("/data/catechism-wsc.json").then(function (r) {{ return r.json(); }}).then(start)
    .catch(function () {{ document.getElementById("quizStatus").textContent = "Không tải được câu hỏi — vui lòng thử lại."; }});
</script>
</body>
</html>"""
(OUT / "trac-nghiem.html").write_text(quiz, encoding="utf-8")
print("quiz page written")

# ---------- daily page (stub upgrade) ----------
daily = f"""{head("Giáo lý mỗi ngày: Tín Lý Yếu Lược Westminster | Reformed Vietnam",
                    "Mỗi ngày một câu hỏi đáp Tín Lý Yếu Lược Westminster, có căn cứ Kinh Thánh — học đức tin từng ngày.", BASE + "/giao-ly-hang-ngay.html")}
<body id="top">
{header}
<main class="wrap">
  <p class="crumb"><a href="/">Trang chủ</a> · <a href="/giao-ly/">Giáo Lý</a> · Mỗi ngày</p>
  <div class="cat-head">
    <div class="kicker">Giáo lý mỗi ngày · Tín Lý Yếu Lược Westminster</div>
    <h1 id="dailyTitle">Câu hỏi hôm nay</h1>
    <p style="margin-top:10px"><span class="ai-label">Bản dịch AI, chưa duyệt</span></p>
  </div>
  <article class="cat-panel">
    <div class="kicker" id="dailyNum" style="color:var(--gold-text);font-weight:700;font-size:12.5px;letter-spacing:.08em">CÂU 1 / 107</div>
    <h2 class="cat-q" id="dailyQ" style="margin-top:8px">{esc(questions[0]['question_vi'])}</h2>
    <div class="cat-a" id="dailyA">{esc(questions[0]['answer_vi'])}</div>
    <div id="dailyProofs"></div>
    <p style="margin-top:16px"><a class="btn solid" id="dailyLink" href="/giao-ly/cau-1.html">Mở trang câu này →</a>
    <a class="btn" href="/giao-ly/">Toàn bộ 107 câu</a></p>
  </article>
  <p style="text-align:center;color:var(--ink-soft);font-size:13px;margin-bottom:34px">Mỗi ngày trang này tự động chuyển sang câu tiếp theo trong bộ 107 câu. Nguồn bản dịch: Kinh Thánh Mỗi Ngày.</p>
</main>
{footer}
{MINI_JS}
<script>
  fetch("/data/catechism-wsc.json").then(function (r) {{ return r.json(); }}).then(function (d) {{
    var now = new Date(); var start = new Date(now.getFullYear(), 0, 0);
    var doy = Math.floor((now - start) / 864e5);
    var q = d.questions[doy % 107];
    document.getElementById("dailyNum").textContent = "CÂU " + q.number + " / 107";
    document.getElementById("dailyQ").textContent = q.question_vi;
    document.getElementById("dailyA").textContent = q.answer_vi;
    document.getElementById("dailyLink").href = "/giao-ly/cau-" + q.number + ".html";
    var box = document.getElementById("dailyProofs");
    q.proof_texts.forEach(function (p) {{
      var det = document.createElement("details"); det.className = "proof";
      var s = document.createElement("summary"); s.textContent = p.ref_vi;
      var para = document.createElement("p"); para.textContent = p.text_vi;
      det.appendChild(s); det.appendChild(para); box.appendChild(det);
    }});
  }}).catch(function () {{}});
</script>
</body>
</html>"""
(ROOT / "giao-ly-hang-ngay.html").write_text(daily, encoding="utf-8")
print("daily page rebuilt")

# ---------- sitemap ----------
sm_path = ROOT / "sitemap.xml"
sm = sm_path.read_text(encoding="utf-8")
new_urls = ["/giao-ly/", "/giao-ly/trac-nghiem.html", "/giao-ly-hang-ngay.html"] + \
           [f"/giao-ly/cau-{n}.html" for n in range(1, 108)]
added = 0
for u in new_urls:
    loc = f"<loc>{BASE}{u}</loc>"
    if loc not in sm:
        sm = sm.replace("</urlset>", f"<url>{loc}</url></urlset>")
        added += 1
sm_path.write_text(sm, encoding="utf-8")
print(f"sitemap: {added} URLs added")
print("DONE")

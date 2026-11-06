#!/usr/bin/env python3
"""Build the Reformed Academy (Guide Phase C, §7.4): /hoc-vien/ landing,
one course page + lesson pages per course in scripts/academy_content.py,
a §10-shaped data/academy.json, and sitemap entries. Three levels
(foundation / doctrine / ministry), first course per level complete:
lessons, readings into the site's own verified modules, and quizzes.
Progress is stored in the visitor's browser (localStorage) — no account."""
import json, re, html, pathlib, sys, random

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from academy_content import COURSES

BASE = "https://reformed-vietnam.vercel.app"
OUT = ROOT / "hoc-vien"
wsc = {q["number"]: q for q in json.loads((ROOT / "data/catechism-wsc.json").read_text(encoding="utf-8"))["questions"]}
enc = {e["slug"]: e for e in json.loads((ROOT / "data/encyclopedia.json").read_text(encoding="utf-8"))["entries"]}
books = {b["id"]: b["name"] for b in json.loads(pathlib.Path("~/workspace/repos/bible-app/data/books.json").expanduser().read_text(encoding="utf-8"))}
answers = {a["slug"]: a for a in json.loads((ROOT / "data/answers.json").read_text(encoding="utf-8"))["entries"]}

def esc(s): return html.escape(str(s), quote=True)

CSS_LINKS = '<link rel="stylesheet" href="/fonts.css" /><link rel="stylesheet" href="/tokens.css" /><link rel="stylesheet" href="/style.css" />'
MINI_JS = """<script>
(function(){var b=document.querySelector('.menu-btn'),n=document.querySelector('.mainnav');if(b&&n){b.addEventListener('click',function(){var o=n.classList.toggle('open');b.setAttribute('aria-expanded',o?'true':'false');});}
var done=[];try{done=JSON.parse(localStorage.getItem('rv-academy-done')||'[]');}catch(e){}
document.querySelectorAll('[data-progress-for]').forEach(function(el){
  var slug=el.getAttribute('data-progress-for'),total=parseInt(el.getAttribute('data-total'),10)||0;
  var n=done.filter(function(k){return k.indexOf(slug+':')===0;}).length;
  el.textContent=total?('Đã học '+n+'/'+total+' bài'):'';});
var mb=document.getElementById('markDone');
if(mb){var key=mb.getAttribute('data-key');
  function paint(){var on=done.indexOf(key)>=0;mb.textContent=on?'✓ Đã hoàn thành bài này':'Đánh dấu đã hoàn thành bài này';mb.classList.toggle('solid',on);}
  paint();
  mb.addEventListener('click',function(){var i=done.indexOf(key);if(i>=0){done.splice(i,1);}else{done.push(key);}try{localStorage.setItem('rv-academy-done',JSON.stringify(done));}catch(e){}paint();});}
var quiz=document.getElementById('lessonQuiz');
if(quiz){var data=null;try{data=JSON.parse(document.getElementById('quizData').textContent);}catch(e){}
  var btn=document.getElementById('quizCheck'),res=document.getElementById('quizResult');
  if(btn&&data){btn.addEventListener('click',function(){var score=0;
    data.forEach(function(item,qi){var sel=quiz.querySelector('input[name="q'+qi+'"]:checked');
      var wrap=quiz.querySelector('[data-qi="'+qi+'"]');var ok=sel&&parseInt(sel.value,10)===item.answer_index;
      if(ok)score++;if(wrap){wrap.style.borderColor=ok?'var(--sage)':'#b4552d';}});
    res.textContent='Bạn trả lời đúng '+score+'/'+data.length+' câu.'+(score===data.length?' Xuất sắc — bạn đã nắm vững bài này.':' Hãy xem lại phần bài đọc của những câu chưa đúng rồi thử lại.');
    res.style.display='block';});}}
})();
</script>"""

HEADER = """<header class="site-header">
  <div class="wrap header-inner">
    <a href="/" class="brand"><span class="brand-mark">✦</span><span class="brand-text">Reformed <em>Vietnam</em></span></a>
    <button class="menu-btn" aria-label="Mở menu" aria-expanded="false">☰</button>
    <nav class="mainnav" aria-label="Điều hướng chính">
      <a href="/#thu-vien">Thư Viện</a><a href="/#tinh-nguyen">Tĩnh Nguyện</a><a href="/#giao-ly">Giáo Lý</a><a href="/#bach-khoa">Bách Khoa</a><a href="/#hoi-dap">Hỏi Đáp</a><a href="/#cong-dong">Cộng Đồng</a>
    </nav>
    <div class="header-actions"><a class="btn ghost" href="/#lien-he">Nhận sách miễn phí</a></div>
  </div>
</header>"""
FOOTER = """<footer class="site-footer">
  <div class="wrap foot-grid">
    <div><div class="brand"><span class="brand-mark">✦</span><span class="brand-text">Reformed <em>Vietnam</em></span></div>
      <p>Thư viện sách Cải Chánh miễn phí cho Hội Thánh Việt Nam — Soli Deo Gloria.</p></div>
    <div><h4>Khám phá</h4><a href="/#thu-vien">Thư Viện</a><a href="/#giao-ly">Giáo Lý</a><a href="/#bach-khoa">Bách Khoa</a><a href="/#hoi-dap">Hỏi Đáp</a></div>
    <div><h4>Học Viện</h4><a href="/hoc-vien/">Tất cả khóa học</a><a href="/hoc-vien/nen-tang-duc-tin/">Nền Tảng Đức Tin</a><a href="/hoc-vien/than-hoc-he-thong-1/">Thần Học Hệ Thống I</a><a href="/hoc-vien/day-giao-ly-nhom-nho/">Dạy Giáo Lý Cho Nhóm Nhỏ</a></div>
    <div><h4>Liên hệ</h4><a href="mailto:reformedvn@gmail.com">reformedvn@gmail.com</a><a href="/#lien-he">Gửi yêu cầu sách</a></div>
  </div>
  <div class="wrap foot-base"><span>© 2026 Reformed Vietnam · Sola Scriptura · Sola Fide · Sola Gratia · Solus Christus · Soli Deo Gloria</span></div>
</footer>"""

def head(title, desc, url):
    return f"""<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}" />
<link rel="canonical" href="{url}" />
<meta property="og:type" content="article" /><meta property="og:title" content="{esc(title)}" />
<meta property="og:description" content="{esc(desc)}" /><meta property="og:url" content="{url}" />
<meta property="og:image" content="{BASE}/og.jpg" />
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>✦</text></svg>" />
{CSS_LINKS}
</head>"""

def lesson_quiz(course_slug, lesson_no, lesson):
    """Explicit quiz items win; otherwise generate from the lesson's WSC pool:
    choose the correct answer text among 4 (seeded, stable across rebuilds)."""
    if lesson.get("quiz"):
        return lesson["quiz"]
    pool = [wsc[n] for n in lesson.get("wsc", []) if n in wsc]
    if len(pool) < 2: return []
    rng = random.Random(f"{course_slug}-{lesson_no}")
    all_answers = [q["answer_vi"] for q in wsc.values()]
    items = []
    for q in pool[:5]:
        distract = rng.sample([a for a in all_answers if a != q["answer_vi"]], 3)
        opts = distract + [q["answer_vi"]]
        order = list(range(4)); rng.shuffle(order)
        shuffled = [opts[i] for i in order]
        items.append({"q_vi": q["question_vi"], "options_vi": shuffled,
                      "answer_index": shuffled.index(q["answer_vi"])})
    return items

def readings_html(lesson):
    groups = []
    if lesson.get("wsc"):
        links = "".join(f'<a class="btn" href="/giao-ly/cau-{n}.html">Câu {n}: {esc(wsc[n]["question_vi"])}</a>' for n in lesson["wsc"] if n in wsc)
        groups.append(f'<div class="rel" style="margin-top:14px"><h3 style="margin:0 0 10px">Giáo Lý Yếu Lược</h3><div style="display:flex;flex-wrap:wrap;gap:8px">{links}</div></div>')
    if lesson.get("enc"):
        links = "".join(f'<a class="btn" href="/bach-khoa/{s}.html">{esc(enc[s]["term_vi"])}</a>' for s in lesson["enc"] if s in enc)
        groups.append(f'<div class="rel" style="margin-top:14px"><h3 style="margin:0 0 10px">Bách Khoa Thần Học</h3><div style="display:flex;flex-wrap:wrap;gap:8px">{links}</div></div>')
    if lesson.get("bible"):
        links = "".join(f'<a class="btn" href="/kinh-thanh/{b}/{c}.html">{esc(books.get(b, b))} {c}</a>' for b, c in lesson["bible"])
        groups.append(f'<div class="rel" style="margin-top:14px"><h3 style="margin:0 0 10px">Đọc Kinh Thánh</h3><div style="display:flex;flex-wrap:wrap;gap:8px">{links}</div></div>')
    if lesson.get("books"):
        links = "".join(f'<a class="btn" href="{u}">{esc(label)}</a>' for label, u in lesson["books"])
        groups.append(f'<div class="rel" style="margin-top:14px"><h3 style="margin:0 0 10px">Đọc thêm trong Thư Viện</h3><div style="display:flex;flex-wrap:wrap;gap:8px">{links}</div></div>')
    if lesson.get("answers"):
        links = "".join(f'<a class="btn" href="/hoi-dap/{s}.html">{esc(answers[s]["question_vi"])}</a>' for s in lesson["answers"] if s in answers)
        groups.append(f'<div class="rel" style="margin-top:14px"><h3 style="margin:0 0 10px">Hỏi Đáp Cải Chánh</h3><div style="display:flex;flex-wrap:wrap;gap:8px">{links}</div></div>')
    return "".join(groups)

data_out = {"courses": []}
sitemap_urls = ["/hoc-vien/"]

for course in COURSES:
    cslug, lessons = course["slug"], course["lessons"]
    cdir = OUT / cslug
    cdir.mkdir(parents=True, exist_ok=True)
    sitemap_urls.append(f"/hoc-vien/{cslug}/")
    course_data = {"course_slug": cslug, "level": course["level"], "title_vi": course["title"], "lessons": []}

    # course page
    rows = "".join(
        f'<a class="qo-row" href="/hoc-vien/{cslug}/bai-{i}.html"><span class="qo-num">Bài {i}</span>'
        f'<span><strong>{esc(l["title"])}</strong><br /><span style="color:var(--ink-soft);font-size:14px">{esc(l["objective"])}</span></span></a>'
        for i, l in enumerate(lessons, 1))
    page = f"""{head(course["title"] + " | Học Viện Cải Chánh",
                     course["audience"], BASE + f"/hoc-vien/{cslug}/")}
<body id="top">
{HEADER}
<main class="wrap">
  <p class="crumb"><a href="/">Trang chủ</a> · <a href="/hoc-vien/">Học Viện Cải Chánh</a></p>
  <div class="cat-head">
    <div class="kicker">Học Viện Cải Chánh · {esc(course["level_vi"])}</div>
    <h1>{esc(course["title"])}</h1>
    <p style="color:var(--ink-soft)">{esc(course["audience"])}</p>
    <p style="margin-top:10px"><span class="ai-label">Nội dung AI soạn, chưa duyệt</span></p>
    <p style="margin-top:10px;color:var(--ink-soft)" data-progress-for="{cslug}" data-total="{len(lessons)}"></p>
  </div>
  <section style="margin-bottom:34px"><div class="qo-list">{rows}</div></section>
</main>
{FOOTER}
{MINI_JS}
</body>
</html>"""
    (cdir / "index.html").write_text(page, encoding="utf-8")

    # lesson pages
    for i, lesson in enumerate(lessons, 1):
        quiz = lesson_quiz(cslug, i, lesson)
        course_data["lessons"].append({
            "course_slug": cslug, "level": course["level"], "lesson": i,
            "title_vi": lesson["title"], "objective_vi": lesson["objective"],
            "reading_slugs": [f"cau-{n}" for n in lesson.get("wsc", [])] + lesson.get("enc", []),
            "youtube_id": "", "summary_vi": lesson["summary"], "quiz": quiz})
        quiz_html = ""
        if quiz:
            qs = []
            for qi, item in enumerate(quiz):
                opts = "".join(
                    f'<label style="display:block;margin:4px 0;font-size:15px"><input type="radio" name="q{qi}" value="{oi}" /> {esc(o)}</label>'
                    for oi, o in enumerate(item["options_vi"]))
                qs.append(f'<fieldset data-qi="{qi}" style="border:1px solid var(--line);border-radius:10px;padding:12px 14px;margin:0 0 12px">'
                          f'<legend style="font-weight:600;padding:0 6px">Câu {qi+1}. {esc(item["q_vi"])}</legend>{opts}</fieldset>')
            quiz_html = f"""<section style="margin-top:26px"><h2>Trắc nghiệm cuối bài</h2>
  <form id="lessonQuiz" onsubmit="return false">{"".join(qs)}
  <button class="btn solid" type="button" id="quizCheck">Kiểm tra đáp án</button>
  <p id="quizResult" style="display:none;margin-top:12px;font-weight:600"></p></form>
  <script type="application/json" id="quizData">{json.dumps(quiz, ensure_ascii=False)}</script></section>"""
        prev_link = f'<a class="btn" href="/hoc-vien/{cslug}/bai-{i-1}.html">← Bài {i-1}</a>' if i > 1 else f'<a class="btn" href="/hoc-vien/{cslug}/">← Trang khóa học</a>'
        next_link = f'<a class="btn solid" href="/hoc-vien/{cslug}/bai-{i+1}.html">Bài {i+1} →</a>' if i < len(lessons) else f'<a class="btn solid" href="/hoc-vien/{cslug}/">Hoàn thành khóa học ✓</a>'
        summary = "".join(f"<p>{esc(p)}</p>" for p in lesson["summary"])
        url = f"{BASE}/hoc-vien/{cslug}/bai-{i}.html"
        page = f"""{head(f"Bài {i}: {lesson['title']} — {course['title']} | Học Viện Cải Chánh",
                         lesson["objective"], url)}
<body id="top">
{HEADER}
<main class="wrap">
  <p class="crumb"><a href="/">Trang chủ</a> · <a href="/hoc-vien/">Học Viện</a> · <a href="/hoc-vien/{cslug}/">{esc(course["title"])}</a></p>
  <article class="qbody">
    <div class="kicker">{esc(course["level_vi"])} · Bài {i}/{len(lessons)}</div>
    <h1>{esc(lesson["title"])}</h1>
    <p><span class="ai-label">Nội dung AI soạn, chưa duyệt</span></p>
    <div class="objective" style="background:var(--card);border:1px solid var(--line);border-radius:12px;padding:14px 16px;margin:16px 0">
      <strong>Mục tiêu bài học:</strong> {esc(lesson["objective"])}
    </div>
    <h2>Bài đọc</h2>
    {readings_html(lesson)}
    <h2 style="margin-top:26px">Tóm tắt bài học</h2>
    {summary}
    {quiz_html}
    <div style="margin-top:26px"><button class="btn" id="markDone" data-key="{cslug}:{i}" type="button">Đánh dấu đã hoàn thành bài này</button></div>
  </article>
  <nav class="qnav"><div style="display:flex;justify-content:space-between;gap:10px;flex-wrap:wrap">{prev_link}{next_link}</div></nav>
</main>
{FOOTER}
{MINI_JS}
</body>
</html>"""
        (cdir / f"bai-{i}.html").write_text(page, encoding="utf-8")
        sitemap_urls.append(f"/hoc-vien/{cslug}/bai-{i}.html")
    data_out["courses"].append(course_data)
    print(f"course {cslug}: {len(lessons)} lessons")

# landing
LEVELS = [("foundation", "Cấp độ 1 · Nền tảng", "Đức tin căn bản cho mọi tín hữu — bắt đầu từ đây."),
          ("doctrine", "Cấp độ 2 · Thần học", "Thần học hệ thống theo thứ tự, ở độ sâu chủng viện phổ thông."),
          ("ministry", "Cấp độ 3 · Phục vụ", "Trang bị để dạy dỗ và phục vụ trong Hội Thánh địa phương.")]
sections = []
for key, label, blurb in LEVELS:
    cs = [c for c in COURSES if c["level"] == key]
    cards = "".join(
        f'<a class="mod-card" href="/hoc-vien/{c["slug"]}/"><span class="pill ok">Có sẵn</span>'
        f'<h3>{esc(c["title"])}</h3><p>{esc(c["audience"])}</p>'
        f'<p style="margin-top:8px;font-weight:600">{len(c["lessons"])} bài học · <span data-progress-for="{c["slug"]}" data-total="{len(c["lessons"])}"></span></p></a>'
        for c in cs)
    sections.append(f'<section style="margin-bottom:30px"><div class="section-head"><div class="rule"></div><h2>{label}</h2><p>{blurb}</p></div><div class="mod-grid">{cards}</div></section>')
landing = f"""{head("Học Viện Cải Chánh — Học thần học miễn phí, có lộ trình | Reformed Vietnam",
                    "Ba cấp độ học thần học trực tuyến miễn phí: nền tảng đức tin, thần học hệ thống và trang bị phục vụ — bài học, bài đọc và trắc nghiệm, không cần tài khoản.",
                    BASE + "/hoc-vien/")}
<body id="top">
{HEADER}
<main class="wrap">
  <p class="crumb"><a href="/">Trang chủ</a> · Học Viện Cải Chánh</p>
  <div class="cat-head">
    <div class="kicker">Học Viện Cải Chánh</div>
    <h1>Học thần học có lộ trình, miễn phí</h1>
    <p style="color:var(--ink-soft)">Ba cấp độ từ nền tảng đến phục vụ, phỏng theo mô hình giáo trình miễn phí của Third Millennium Ministries. Mỗi bài học gồm mục tiêu, bài đọc ngay trong trang web này, tóm tắt và trắc nghiệm. Tiến độ được lưu trên thiết bị của bạn — không cần tài khoản.</p>
    <p style="margin-top:10px"><span class="ai-label">Nội dung AI soạn, chưa duyệt</span></p>
  </div>
  {"".join(sections)}
  <section style="margin-bottom:34px"><div class="section-head"><div class="rule"></div><h2>Sắp ra mắt</h2>
  <p>Khảo Sát Kinh Thánh (tổng quan 66 sách, theo từng phần của giao ước) và Thần Học Hệ Thống II — Giáo Lý Về Sự Cứu Rỗi đang được soạn. Mỗi cấp độ sẽ thêm khóa mới sau khi khóa đầu tiên hoàn thiện.</p></div></section>
</main>
{FOOTER}
{MINI_JS}
</body>
</html>"""
OUT.mkdir(exist_ok=True)
(OUT / "index.html").write_text(landing, encoding="utf-8")
(ROOT / "data/academy.json").write_text(json.dumps(data_out, ensure_ascii=False, indent=1), encoding="utf-8")
print("landing + data/academy.json written")

# sitemap
sm_path = ROOT / "sitemap.xml"
sm = sm_path.read_text(encoding="utf-8")
have = set(re.findall(r"<loc>(.*?)</loc>", sm))
new = [u for u in sitemap_urls if BASE + u not in have]
if new:
    block = "".join(f'  <url><loc>{BASE}{u}</loc><changefreq>monthly</changefreq><priority>0.7</priority></url>\n' for u in new)
    sm = sm.replace("</urlset>", block + "</urlset>")
    sm_path.write_text(sm, encoding="utf-8")
print(f"sitemap: {len(new)} URLs added")
print("DONE")

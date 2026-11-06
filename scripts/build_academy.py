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
    _comp = {"nen-tang-duc-tin": "Lộ trình đồng hành tiếng Việt cho Chứng Chỉ Nền Tảng của Thirdmill Institute.",
             "than-hoc-he-thong-1": "Lộ trình đồng hành tiếng Việt cho khóa The Doctrine of God — Chứng Chỉ Nghiên Cứu Thần Học của Thirdmill Institute.",
             "day-giao-ly-nhom-nho": "Khóa trang bị phục vụ, đồng hành cùng các huy hiệu phục vụ (dạy Kinh Thánh, dẫn nhóm nhỏ) trong chương trình Thirdmill Institute."}.get(course["slug"])
    companion_line = f'<p style="margin-top:10px;color:var(--ink-soft)">{esc(_comp)}</p>' if _comp else ""
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
    {companion_line}
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

# ---------- Thirdmill Institute certificates (restructure approved by Duc 2026-11-06) ----------
# Lesson data verified by a research sweep of nexus.thirdmill.org series pages
# (scripts/helper-data/thirdmill-series.json): 26 series, 122 lessons. Videos
# are NOT embedded (Nexus publishes no YouTube links; lessons stream in
# Thirdmill's own player) — course pages link to each series on Nexus, which
# Thirdmill's reproduction policy encourages for ministry use.
tm_series = json.loads((ROOT / "scripts/helper-data/thirdmill-series.json").read_text(encoding="utf-8"))
def series_of(course_en):
    return [s for s in tm_series if s["course"].startswith(course_en + " (")]
CERTS = [
  {"id": "chung-chi-nen-tang", "vi": "Chứng Chỉ Nền Tảng", "en": "Foundations Certificate",
   "blurb": "Bốn khóa nhập môn về Kinh Thánh và thần học — điểm bắt đầu cho mọi học viên.",
   "courses": [
     {"slug": "nen-tang-kinh-thanh", "vi": "Nền Tảng Kinh Thánh", "en": "Biblical Foundations", "badge": "Truyền giảng"},
     {"slug": "nen-tang-than-hoc", "vi": "Nền Tảng Thần Học", "en": "Theological Foundations", "badge": "Cầu nguyện"},
     {"slug": "nen-tang-cuu-uoc", "vi": "Nền Tảng Cựu Ước", "en": "Old Testament Foundations", "badge": "Môn đồ hóa"},
     {"slug": "nen-tang-tan-uoc", "vi": "Nền Tảng Tân Ước", "en": "New Testament Foundations", "badge": "Giảng dạy", "note": "Loạt bài Công Vụ Các Sứ Đồ có 1 trong 3 bài đã có bản tiếng Việt trên Nexus."}]},
  {"id": "chung-chi-kinh-thanh", "vi": "Chứng Chỉ Nghiên Cứu Kinh Thánh", "en": "Certificate in Biblical Studies",
   "blurb": "Năm khóa đào sâu Kinh Thánh: truyện ký, tiên tri, Phao-lô, các thư tín và giải kinh.",
   "courses": [
     {"slug": "truyen-ky-cuu-uoc", "vi": "Truyện Ký Cựu Ước", "en": "Old Testament Narratives", "badge": "Tĩnh nguyện cá nhân"},
     {"slug": "tien-tri-cuu-uoc", "vi": "Các Tiên Tri Cựu Ước", "en": "Old Testament Prophets", "badge": "Đời sống gia đình"},
     {"slug": "nghien-cuu-phaolo", "vi": "Nghiên Cứu Về Phao-lô", "en": "Pauline Studies", "badge": "Chăm sóc bản thân"},
     {"slug": "thu-tin-tan-uoc", "vi": "Các Thư Tín Tân Ước", "en": "New Testament Epistles", "badge": "Nhân cách"},
     {"slug": "giai-kinh", "vi": "Giải Kinh", "en": "Biblical Interpretation", "badge": "Quản gia"}]},
  {"id": "chung-chi-than-hoc", "vi": "Chứng Chỉ Nghiên Cứu Thần Học", "en": "Certificate in Theological Studies",
   "blurb": "Năm khóa thần học hệ thống ở độ sâu chủng viện.",
   "courses": [
     {"slug": "giao-ly-duc-chua-troi", "vi": "Giáo Lý Về Đức Chúa Trời", "en": "The Doctrine of God", "badge": "Chuẩn bị bài học Kinh Thánh", "companion": "than-hoc-he-thong-1"},
     {"slug": "giao-ly-dang-christ", "vi": "Giáo Lý Về Đấng Christ", "en": "Christology", "badge": "Dẫn dắt nhóm nhỏ"},
     {"slug": "giao-ly-duc-thanh-linh", "vi": "Giáo Lý Về Đức Thánh Linh", "en": "Pneumatology", "badge": "Giảng luận"},
     {"slug": "con-nguoi-va-tan-the", "vi": "Con Người & Tận Thế", "en": "Anthropology & Eschatology", "badge": "Lãnh đạo tôi tớ"},
     {"slug": "dao-duc-kinh-thanh", "vi": "Đạo Đức Kinh Thánh", "en": "Biblical Ethics", "badge": "Truyền giảng Vương quốc"}]},
]
COMPANION_OF = {"than-hoc-he-thong-1": ("Giáo Lý Về Đức Chúa Trời", "/hoc-vien/khoa/giao-ly-duc-chua-troi/")}
tm_data = []
for cert in CERTS:
    cert_lessons = 0
    cert_data = {"certificate_vi": cert["vi"], "certificate_en": cert["en"], "courses": []}
    for c in cert["courses"]:
        series = series_of(c["en"])
        n_lessons = sum(s["lesson_count"] for s in series)
        cert_lessons += n_lessons
        cert_data["courses"].append({"slug": c["slug"], "title_vi": c["vi"], "title_en": c["en"],
                                     "badge_vi": c["badge"],
                                     "series": [{"series": s["series"], "lessons": s["lessons"],
                                                 "lesson_count": s["lesson_count"], "series_url": s["series_url"]} for s in series]})
        sitemap_urls.append(f"/hoc-vien/khoa/{c['slug']}/")
        # course page
        kdir = OUT / "khoa" / c["slug"]
        kdir.mkdir(parents=True, exist_ok=True)
        series_html = ""
        for s in series:
            items = "".join(f"<li>{esc(x)}</li>" for x in s["lessons"])
            series_html += f"""<section style="margin-bottom:26px">
    <h2 style="font-size:21px">{esc(s["series"])}</h2>
    <p style="color:var(--ink-soft)">{s["lesson_count"]} bài học · Thirdmill Nexus</p>
    <ol style="margin:10px 0 14px;padding-left:22px;line-height:1.75">{items}</ol>
    <p><a class="btn solid" href="{esc(s["series_url"])}" target="_blank" rel="noopener">Học loạt bài này trên Nexus →</a></p>
  </section>"""
        note = f'<p style="margin-top:10px;color:var(--ink-soft)">{esc(c["note"])}</p>' if c.get("note") else ""
        companion = ""
        if c.get("companion"):
            companion = f'<p style="margin-top:14px"><a class="btn" href="/hoc-vien/{c["companion"]}/">Lộ trình đồng hành tiếng Việt: {esc(next(x["title"] for x in COURSES if x["slug"] == c["companion"]))} →</a></p>'
        url = f"{BASE}/hoc-vien/khoa/{c['slug']}/"
        page = f"""{head(c["vi"] + " (" + c["en"] + ") — Thirdmill | Học Viện Cải Chánh",
                         f"Khóa {c['en']} của Thirdmill Institute: {len(series)} loạt bài, {n_lessons} bài học, học miễn phí trên Nexus.", url)}
<body id="top">
{HEADER}
<main class="wrap">
  <p class="crumb"><a href="/">Trang chủ</a> · <a href="/hoc-vien/">Học Viện</a> · {esc(cert["vi"])}</p>
  <div class="cat-head">
    <div class="kicker">Thirdmill Institute · {esc(cert["en"])}</div>
    <h1>{esc(c["vi"])}</h1>
    <p style="color:var(--ink-soft)">{esc(c["en"])} · {len(series)} loạt bài · {n_lessons} bài học · Huy hiệu phục vụ: {esc(c["badge"])}</p>
    {note}{companion}
  </div>
  <article class="qbody" style="margin-bottom:10px">
    <p>Đây là khóa học chính thức của <strong>Third Millennium Ministries</strong>, học miễn phí trên nền tảng Nexus của Thirdmill (bài học bằng tiếng Anh; Nexus có giao diện tiếng Việt). Reformed Vietnam không lưu trữ video — mỗi loạt bài liên kết thẳng đến Nexus, nơi bạn xem video, đọc bản văn và làm bài kiểm tra để tích lũy chứng chỉ.</p>
  </article>
  {series_html}
</main>
{FOOTER}
{MINI_JS}
</body>
</html>"""
        (kdir / "index.html").write_text(page, encoding="utf-8")
    cert["total_lessons"] = cert_lessons
    cert_data["total_lessons"] = cert_lessons
    tm_data.append(cert_data)
    print(f"certificate {cert['en']}: {len(cert['courses'])} courses, {cert_lessons} lessons")
data_out["thirdmill_certificates"] = tm_data

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
cert_sections = []
for cert in CERTS:
    cards = "".join(
        f'<a class="mod-card" href="/hoc-vien/khoa/{c["slug"]}/"><span class="pill ok">Thirdmill</span>'
        f'<h3>{esc(c["vi"])}</h3><p>{esc(c["en"])} · {len(series_of(c["en"]))} loạt bài · {sum(s["lesson_count"] for s in series_of(c["en"]))} bài học</p>'
        f'<p style="margin-top:8px;font-weight:600">Huy hiệu phục vụ: {esc(c["badge"])}</p></a>'
        for c in cert["courses"])
    cert_sections.append(f'<section id="{cert["id"]}" style="margin-bottom:30px"><div class="section-head"><div class="rule"></div><h2>{esc(cert["vi"])}</h2><p>{esc(cert["blurb"])} Tổng cộng {cert["total_lessons"]} bài học.</p></div><div class="mod-grid">{cards}</div></section>')
landing = f"""{head("Học Viện Cải Chánh — Chương trình Thirdmill miễn phí + lộ trình tiếng Việt | Reformed Vietnam",
                    "Học Viện Cải Chánh theo chương trình chính thức của Thirdmill Institute: 3 chứng chỉ, 14 khóa, 122 bài học miễn phí trên Nexus, kèm lộ trình đồng hành tiếng Việt.",
                    BASE + "/hoc-vien/")}
<body id="top">
{HEADER}
<main class="wrap">
  <p class="crumb"><a href="/">Trang chủ</a> · Học Viện Cải Chánh</p>
  <div class="cat-head">
    <div class="kicker">Học Viện Cải Chánh</div>
    <h1>Học thần học theo chương trình Thirdmill — miễn phí</h1>
    <p style="color:var(--ink-soft)">Học Viện chạy theo chương trình chính thức của <strong>Thirdmill Institute</strong> (Third Millennium Ministries): ba chứng chỉ, 14 khóa, 122 bài học cấp chủng viện, học miễn phí trên nền tảng Nexus. Hoàn thành cả ba chứng chỉ, học viên nhận Diploma in Christian Ministry từ Thirdmill Institute. Bên dưới chương trình chính là các lộ trình đồng hành tiếng Việt của Reformed Vietnam.</p>
  </div>
  <section style="margin-bottom:30px"><div class="section-head"><div class="rule"></div><h2>Cách học</h2></div>
    <div class="mod-grid">
      <div class="mod-card"><h3>1 · Học trên Nexus</h3><p>Mỗi khóa bên dưới liệt kê đầy đủ các loạt bài và bài học. Nút “Học trên Nexus” đưa bạn đến video, bản văn và bài kiểm tra chính thức (tiếng Anh; Nexus có giao diện tiếng Việt).</p></div>
      <div class="mod-card"><h3>2 · Đồng hành tiếng Việt</h3><p>Các lộ trình tiếng Việt của Reformed Vietnam đi kèm chương trình chính: bài đọc trong chính trang này, tóm tắt và trắc nghiệm — không cần tài khoản, tiến độ lưu trên thiết bị.</p></div>
      <div class="mod-card"><h3>3 · Chứng chỉ</h3><p>Tiến độ và chứng chỉ do Thirdmill Institute cấp trên Nexus. Lộ trình tiếng Việt chỉ là phần đồng hành — không thay thế bài kiểm tra chính thức.</p></div>
    </div>
    <p style="color:var(--ink-soft);font-size:14px">Ghi nhận: hiện chỉ 1 trong 3 bài của loạt Công Vụ Các Sứ Đồ đã có bản tiếng Việt trên Nexus; phần lớn bài học là tiếng Anh. Thirdmill cho phép phân phối miễn phí tài liệu của họ cho mục vụ — trang này liên kết đến Nexus thay vì sao chép nội dung.</p>
  </section>
  {"".join(cert_sections)}
  <section style="margin-bottom:30px"><div class="section-head"><div class="rule"></div><h2>Lộ Trình Đồng Hành Tiếng Việt</h2><p>Ba khóa tiếng Việt do Reformed Vietnam soạn, học kèm chương trình Thirdmill.</p></div></section>
  {"".join(sections)}
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

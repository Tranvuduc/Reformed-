#!/usr/bin/env python3
"""Build the Daily Grace module (Ân Điển Mỗi Ngày) for Reformed Vietnam.

Source: data/devotions.json in this repo — Spurgeon's Faith's Checkbook (1888)
in Vietnamese, integrated from Kinh Thánh Mỗi Ngày under the owner's override
of 2026-11-06, proofreading fixes applied (commit 30ca706). One real entry per
calendar date (Build Guide §8 rule); every page carries the label
"Bản dịch AI, chưa duyệt".

Outputs: suy-ngam/index.html (archive: today's card + search + month index),
suy-ngam/<mm>-<dd>.html x366 (one page per day), sitemap.xml updates.
The homepage rotation + module-card flips live in patch_homepage_modules.py.
"""
import json, re, html, pathlib, unicodedata

ROOT = pathlib.Path(__file__).resolve().parent.parent
APP = ROOT.parent / "bible-app"
BASE = "https://reformed-vietnam.vercel.app"
MONTHS = ["", "tháng 1", "tháng 2", "tháng 3", "tháng 4", "tháng 5", "tháng 6",
          "tháng 7", "tháng 8", "tháng 9", "tháng 10", "tháng 11", "tháng 12"]

raw = json.loads((ROOT / "data/devotions.json").read_text(encoding="utf-8"))
entries = raw["entries"]
assert len(entries) == 366, len(entries)
by_md = {(e["month"], e["day"]): e for e in entries}
assert len(by_md) == 366

enc_terms = {}
_enc_path = ROOT / "data/encyclopedia.json"
if _enc_path.exists():
    enc_terms = {e["slug"]: e["term_vi"] for e in json.loads(_enc_path.read_text(encoding="utf-8"))["entries"]}

books_meta = json.loads((APP / "data/books.json").read_text(encoding="utf-8"))
name2id = {}
for f in (APP / "data" / "bible").glob("*.json"):
    d = json.loads(f.read_text(encoding="utf-8"))
    name2id[d["name"].strip().lower()] = f.stem

ALIASES = {"công vụ": "act", "phục truyền": "deb"}  # abbreviated names used in some refs

def reader_link(ref):
    """'Thi Thiên 37:4' -> /kinh-thanh/psa/37.html#v4 (or None)"""
    m = re.match(r"^(.+?)\s+(\d+):(\d+)", ref.strip())
    if not m: return None
    key = m.group(1).strip().lower()
    bid = name2id.get(key) or ALIASES.get(key)
    if not bid: return None
    return f"/kinh-thanh/{bid}/{m.group(2)}.html#v{m.group(3)}"

links_ok = sum(1 for e in entries if reader_link(e["ref"]))
print(f"devotion refs resolving to reader chapters: {links_ok}/366")

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

      /* ---------- daily grace module ---------- */
      .crumb { font-size: 13.5px; color: var(--ink-soft); margin: 26px 0 6px; }
      .crumb a { color: var(--burgundy); text-decoration: none; }
      .cat-head { text-align: center; padding: 18px 0 6px; }
      .cat-head .kicker { color: var(--gold-text); font-weight: 700; letter-spacing: .08em; text-transform: uppercase; font-size: 12.5px; }
      .cat-head h1 { font-family: "Playfair Display", serif; font-size: clamp(26px, 4.6vw, 38px); margin: 8px 0 10px; }
      .cat-panel { max-width: 680px; margin: 18px auto 8px; background: var(--surface); border: 1px solid var(--line); border-radius: var(--radius); padding: 26px 26px 20px; box-shadow: var(--shadow); }
      .ai-label { display: inline-block; font-size: 12px; font-weight: 600; color: var(--burgundy); background: color-mix(in srgb, var(--burgundy) 9%, transparent); border: 1px solid color-mix(in srgb, var(--burgundy) 35%, transparent); padding: 2px 9px; border-radius: 999px; }
      .dev-verse-lg { font-family: "Noto Serif", serif; font-size: 19px; line-height: 1.75; border-left: 3px solid var(--gold); padding-left: 16px; margin: 14px 0 6px; }
      .dev-ref-lg { color: var(--burgundy); font-weight: 600; margin-bottom: 10px; }
      .dev-body p { font-family: "Noto Serif", serif; font-size: 16.5px; line-height: 1.8; }
      .qnav { display: flex; justify-content: space-between; gap: 10px; max-width: 680px; margin: 20px auto 6px; }
      .share-row { display: flex; gap: 10px; justify-content: center; margin: 18px 0 4px; flex-wrap: wrap; }
      .month-h { font-family: "Playfair Display", serif; font-size: 21px; color: var(--gold-text); margin: 24px 0 10px; }
      .day-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(158px, 1fr)); gap: 9px; }
      .day-chip { display: block; background: var(--surface); border: 1px solid var(--line); border-radius: 10px; padding: 10px 12px; text-decoration: none; }
      .day-chip .dn { font-weight: 700; color: var(--burgundy); font-size: 15px; }
      .day-chip .dt { display: block; font-size: 13px; color: var(--ink-soft); line-height: 1.45; margin-top: 2px; }
      .day-chip:hover { border-color: var(--burgundy); }
      .term-search { max-width: 560px; margin: 14px auto 4px; display: flex; gap: 8px; }
      .term-search input { flex: 1; padding: 12px 16px; border: 1px solid var(--line); border-radius: 999px; font: inherit; font-size: 15.5px; background: var(--surface); color: var(--ink); }
      /* ---------- design pass 2026-11: title band / prose kit ---------- */
      .title-band { max-width: 860px; margin: 16px auto 6px; background: linear-gradient(120deg, var(--burgundy-deep), var(--burgundy)); border-radius: var(--radius); box-shadow: var(--shadow); padding: 26px 28px; display: flex; gap: 22px; align-items: center; }
      .title-band .tb-kicker { color: #eccf8f; font-weight: 700; letter-spacing: .09em; text-transform: uppercase; font-size: 12.5px; }
      .title-band h1 { font-family: "Playfair Display", serif; font-size: clamp(24px, 4.2vw, 33px); line-height: 1.32; margin: 6px 0 4px; color: #fdf6e9; }
      .title-band .tb-sub { color: #efdfc2; font-size: 15px; margin: 4px 0 0; }
      .title-band .ai-label { background: rgba(255,255,255,.14); border-color: rgba(255,255,255,.45); color: #fdf6e9; }
      .medallion { flex: 0 0 auto; width: 84px; height: 84px; border-radius: 50%; border: 2px solid #eccf8f; display: flex; flex-direction: column; align-items: center; justify-content: center; font-family: "Playfair Display", serif; color: #fdf6e9; text-align: center; padding: 4px; }
      .medallion .m-big { font-size: 30px; font-weight: 700; line-height: 1; }
      .medallion .m-small { font-size: 10.5px; letter-spacing: .08em; text-transform: uppercase; font-family: "Be Vietnam Pro", sans-serif; margin-top: 3px; color: #eccf8f; }
      @media (max-width: 560px) { .title-band { flex-direction: column; text-align: center; padding: 22px 18px; } .medallion { width: 70px; height: 70px; } .medallion .m-big { font-size: 25px; } }
      @media (prefers-color-scheme: dark) { .title-band { background: linear-gradient(120deg, #241611, #571d22); } }
      .dev-teaser { max-width: 860px; margin: 12px auto 0; text-align: center; font-style: italic; color: var(--ink-soft); font-size: 15.5px; }
      .pull-quote { font-family: "Playfair Display", serif; font-style: italic; font-size: clamp(19px, 3vw, 23px); line-height: 1.6; color: var(--burgundy); border-left: 4px solid var(--gold-soft); padding: 4px 0 4px 18px; margin: 6px 0 10px; }
      .dropcap > p:first-of-type::first-letter { font-family: "Playfair Display", serif; font-weight: 700; font-size: 3.05em; float: left; line-height: .8; padding: 5px 10px 0 0; color: var(--burgundy); }
      .band-tint { background: color-mix(in srgb, var(--burgundy) 6%, var(--surface)); border-top: 2px solid var(--gold-soft); border-radius: 10px; padding: 14px 16px 6px; margin-top: 14px; }
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

def share_row(url):
    return (f'<div class="share-row">'
            f'<a class="btn solid" target="_blank" rel="noopener" href="https://www.facebook.com/sharer/sharer.php?u={url}">Chia sẻ Facebook</a>'
            f'<a class="btn" target="_blank" rel="noopener" href="https://sp.zalo.me/share_inline?url={url}">Chia sẻ Zalo</a></div>')

def slug_md(m, d): return f"{m:02d}-{d:02d}"

def slugify(s):
    s = s.replace("Đ", "d").replace("đ", "d")
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")

# theme index (from the merged tags in data/devotions.json)
THEMES = {}
for e in entries:
    for th in e.get("themes", []):
        THEMES.setdefault(th, []).append(e)
print(f"themes: {len(THEMES)}")

def ordered():
    return [by_md[(m, d)] for m in range(1, 13) for d in range(1, 32) if (m, d) in by_md]

seq = ordered()
pos = {slug_md(e["month"], e["day"]): i for i, e in enumerate(seq)}

OUT = ROOT / "suy-ngam"
OUT.mkdir(exist_ok=True)

for e in seq:
    m, d = e["month"], e["day"]
    s = slug_md(m, d)
    url = f"{BASE}/suy-ngam/{s}.html"
    i = pos[s]
    prev_e, next_e = seq[i - 1], seq[(i + 1) % 366]
    rl = reader_link(e["ref"])
    ref_html = (f'<div class="dev-ref-lg"><a href="{rl}" style="color:inherit">{esc(e["ref"])}</a></div>'
                if rl else f'<div class="dev-ref-lg">{esc(e["ref"])}</div>')
    paras = "".join(f"<p>{esc(p)}</p>" for p in e["paras"])
    title = f"{e['title']} — Tĩnh nguyện ngày {d} {MONTHS[m]} | Ân Điển Mỗi Ngày"
    desc = e.get("summary") or ((e["paras"][0][:150] + "…") if e["paras"] else e["title"])
    summary_html = f'<p style="font-style:italic;color:var(--ink-soft);font-size:15.5px">{esc(e["summary"])}</p>' if e.get("summary") else ""
    enrich_html = ""
    if e.get("reflection_question") and e.get("prayer"):
        rel = ""
        links = [f'<a class="btn" href="/bach-khoa/{s}.html">{esc(enc_terms.get(s, s))}</a>' for s in e.get("related_encyclopedia", []) if s in enc_terms]
        links += [f'<a class="btn" href="/giao-ly/cau-{n}.html">Giáo Lý Câu {n}</a>' for n in e.get("related_catechism", [])]
        if links:
            rel = f'<h3 style="margin:18px 0 10px">Đọc thêm</h3><div class="rel-links" style="display:flex;flex-wrap:wrap;gap:8px">{"".join(links)}</div>'
        enrich_html = f"""<div style="margin-top:22px;border-top:1px solid var(--line);padding-top:18px">
      <h3 style="margin:0 0 10px">Suy ngẫm &amp; cầu nguyện</h3>
      <p><span class="ai-label">Nội dung AI soạn, chưa duyệt</span></p>
      <p style="font-weight:600">{esc(e["reflection_question"])}</p>
      <h4 style="margin:16px 0 8px">Lời cầu nguyện gợi ý</h4>
      <p style="font-style:italic">{esc(e["prayer"])}</p>
      {rel}
    </div>"""
    theme_chips = ""
    if e.get("themes"):
        links = "".join(f'<a class="btn" href="/suy-ngam/chu-de/{slugify(th)}.html">{esc(th)}</a>' for th in e["themes"])
        theme_chips = f'<div style="margin-top:16px"><h3 style="margin:0 0 10px">Chủ đề</h3><div class="rel-links" style="display:flex;flex-wrap:wrap;gap:8px">{links}</div></div>'
    page = f"""{head(title, desc, url)}
<body id="top">
{header}
<main class="wrap">
  <p class="crumb"><a href="/">Trang chủ</a> · <a href="/suy-ngam/">Ân Điển Mỗi Ngày</a> · Ngày {d} {MONTHS[m]}</p>
  <div class="title-band">
    <div class="medallion"><span class="m-big">{d}</span><span class="m-small">{MONTHS[m]}</span></div>
    <div>
      <div class="tb-kicker">Ân Điển Mỗi Ngày · Sổ Séc Của Đức Tin (1888)</div>
      <h1>{esc(e['title'])}</h1>
      <p class="tb-sub">Bài tĩnh nguyện ngày {d} {MONTHS[m]} · C. H. Spurgeon &nbsp;<span class="ai-label">Bản dịch AI, chưa duyệt</span></p>
    </div>
  </div>
  <article class="cat-panel">
    <blockquote class="dev-verse-lg pull-quote">“{esc(e['verse'])}”</blockquote>
    {ref_html}
    {summary_html}
    <div class="dev-body dropcap">{paras}</div>
    {enrich_html}
    {theme_chips}
  </article>
  <nav class="qnav">
    <a class="btn" href="/suy-ngam/{slug_md(prev_e['month'], prev_e['day'])}.html">← Ngày {prev_e['day']}/{prev_e['month']}</a>
    <a class="btn" href="/suy-ngam/{slug_md(next_e['month'], next_e['day'])}.html">Ngày {next_e['day']}/{next_e['month']} →</a>
  </nav>
  {share_row(url)}
  <p style="text-align:center;color:var(--ink-soft);font-size:13px;margin-bottom:34px">Trọn bộ: <a href="/suy-ngam/">366 bài tĩnh nguyện</a> · Đọc thêm trong <a href="/kinh-thanh/">Kinh Thánh 1934</a>.</p>
</main>
{footer}
{MINI_JS}
</body>
</html>"""
    (OUT / f"{s}.html").write_text(page, encoding="utf-8")
print("366 day pages written")

# ---- theme pages ----
theme_dir = OUT / "chu-de"
theme_dir.mkdir(exist_ok=True)
for th, tes in THEMES.items():
    tslug = slugify(th)
    url = f"{BASE}/suy-ngam/chu-de/{tslug}.html"
    chips = "".join(
        f'<a class="day-chip" href="/suy-ngam/{slug_md(e["month"], e["day"])}.html"><span class="dn">{e["day"]}/{e["month"]}</span><span class="dt">{esc(e["title"])}</span></a>'
        for e in sorted(tes, key=lambda x: (x["month"], x["day"])))
    page = f"""{head(f"Tĩnh nguyện theo chủ đề: {th} | Ân Điển Mỗi Ngày",
                     f"{len(tes)} bài tĩnh nguyện của Spurgeon về chủ đề {th}.", url)}
<body id="top">
{header}
<main class="wrap">
  <p class="crumb"><a href="/">Trang chủ</a> · <a href="/suy-ngam/">Ân Điển Mỗi Ngày</a> · Chủ đề</p>
  <div class="cat-head">
    <div class="kicker">Tĩnh Nguyện Theo Chủ Đề</div>
    <h1>{esc(th)}</h1>
    <p style="color:var(--ink-soft)">{len(tes)} bài tĩnh nguyện về chủ đề này trong “Sổ Séc Của Đức Tin”.</p>
    <p style="margin-top:10px"><span class="ai-label">Bản dịch AI, chưa duyệt</span></p>
  </div>
  <section class="band-tint" style="max-width:860px;margin:14px auto 34px"><div class="day-grid">{chips}</div></section>
</main>
{footer}
{MINI_JS}
</body>
</html>"""
    (theme_dir / f"{tslug}.html").write_text(page, encoding="utf-8")
print(f"{len(THEMES)} theme pages written")

# ---- landing ----
import datetime
today = datetime.date(2026, 11, 6)
te = by_md[(today.month, today.day)]
month_blocks = ""
for m in range(1, 13):
    chips = "".join(
        f'<a class="day-chip" data-name="{esc((e["title"] + " " + e["ref"]).lower())}" href="/suy-ngam/{slug_md(m, e["day"])}.html"><span class="dn">{e["day"]}/{m}</span><span class="dt">{esc(e["title"])}</span></a>'
        for e in seq if e["month"] == m)
    month_blocks += f'<h2 class="month-h">Tháng {m}</h2><div class="day-grid">{chips}</div>'
landing = f"""{head("Ân Điển Mỗi Ngày — 366 bài tĩnh nguyện của Spurgeon | Reformed Vietnam",
                     "Mỗi ngày một bài tĩnh nguyện từ 'Sổ Séc Của Đức Tin' (1888) của C. H. Spurgeon: lời hứa của Đức Chúa Trời cho từng ngày trong năm.", BASE + "/suy-ngam/")}
<body id="top">
{header}
<main class="wrap">
  <p class="crumb"><a href="/">Trang chủ</a> · Ân Điển Mỗi Ngày</p>
  <div class="cat-head">
    <div class="kicker">Ân Điển Mỗi Ngày</div>
    <h1>366 bài tĩnh nguyện của Spurgeon</h1>
    <p style="max-width:620px;margin:0 auto;color:var(--ink-soft)">“Sổ Séc Của Đức Tin” (Faith's Checkbook, 1888) — mỗi bài là một lời hứa của Đức Chúa Trời cho một ngày, kèm lời suy ngẫm ngắn của C. H. Spurgeon.</p>
    <p style="margin-top:10px"><span class="ai-label">Bản dịch AI, chưa duyệt</span></p>
  </div>
  <article class="cat-panel">
    <div class="kicker" id="todayKicker" style="color:var(--gold-text);font-weight:700;font-size:12.5px;letter-spacing:.08em">BÀI NGÀY {today.day} {MONTHS[today.month].upper()}</div>
    <h2 id="todayTitle" style="font-family:'Noto Serif',serif;margin:8px 0 4px">{esc(te['title'])}</h2>
    <blockquote class="dev-verse-lg" id="todayVerse">“{esc(te['verse'])}”</blockquote>
    <div class="dev-ref-lg" id="todayRef">{esc(te['ref'])}</div>
    <p style="text-align:center;margin:14px 0 2px"><a class="btn solid" id="todayBtn" href="/suy-ngam/{slug_md(today.month, today.day)}.html">Đọc bài tĩnh nguyện →</a></p>
  </article>
  <h2 class="month-h" style="text-align:center">Duyệt theo chủ đề</h2>
  <div style="display:flex;flex-wrap:wrap;gap:8px;justify-content:center;max-width:760px;margin:0 auto">{"".join(f'<a class="btn" href="/suy-ngam/chu-de/{slugify(th)}.html">{esc(th)} ({len(tes)})</a>' for th, tes in sorted(THEMES.items(), key=lambda kv: -len(kv[1])))}</div>
  <div class="term-search">
    <input type="search" id="devSearch" placeholder="Tìm bài theo tựa đề hoặc câu Kinh Thánh…" aria-label="Tìm bài tĩnh nguyện" />
  </div>
  <div id="devIndex">
{month_blocks}
  </div>
  <p style="text-align:center;color:var(--ink-soft);font-size:13px;margin:26px 0 34px">Nguồn: C. H. Spurgeon, Faith's Checkbook (1888), qua Kinh Thánh Mỗi Ngày; bản dịch AI, chưa duyệt.</p>
</main>
{footer}
{MINI_JS}
<script>
  (function () {{
    function norm(s) {{ return s.toLowerCase().normalize("NFD").replace(/[\\u0300-\\u036f]/g, "").replace(/đ/g, "d").replace(/Đ/g, "d"); }}
    var input = document.getElementById("devSearch"), chips = document.querySelectorAll(".day-chip");
    input.addEventListener("input", function () {{
      var q = norm(input.value.trim());
      chips.forEach(function (c) {{ c.style.display = (!q || norm(c.getAttribute("data-name")).indexOf(q) >= 0) ? "" : "none"; }});
      document.querySelectorAll("#devIndex .month-h").forEach(function (h) {{
        var grid = h.nextElementSibling, any = false;
        grid.querySelectorAll(".day-chip").forEach(function (c) {{ if (c.style.display !== "none") any = true; }});
        h.style.display = any ? "" : "none"; grid.style.display = any ? "" : "none";
      }});
    }});
    // render the visitor's actual today's entry from the shared data file
    fetch("/data/devotions.json").then(function (r) {{ return r.json(); }}).then(function (data) {{
      var now = new Date(), m = now.getMonth() + 1, d = now.getDate();
      var e = null;
      data.entries.forEach(function (x) {{ if (x.month === m && x.day === d) e = x; }});
      if (!e) return;
      var pad = function (n) {{ return String(n).padStart(2, "0"); }};
      document.getElementById("todayKicker").textContent = "HÔM NAY · NGÀY " + d + " THÁNG " + m;
      document.getElementById("todayTitle").textContent = e.title;
      document.getElementById("todayVerse").textContent = "“" + e.verse + "”";
      document.getElementById("todayRef").textContent = e.ref;
      var btn = document.getElementById("todayBtn");
      btn.setAttribute("href", "/suy-ngam/" + pad(m) + "-" + pad(d) + ".html");
      btn.textContent = "Đọc bài hôm nay →";
    }}).catch(function () {{}});
  }})();
</script>
</body>
</html>"""
(OUT / "index.html").write_text(landing, encoding="utf-8")
print("landing page written")

sm_path = ROOT / "sitemap.xml"
sm = sm_path.read_text(encoding="utf-8")
added = 0
for u in ["/suy-ngam/"] + [f"/suy-ngam/{slug_md(e['month'], e['day'])}.html" for e in seq] + \
         [f"/suy-ngam/chu-de/{slugify(th)}.html" for th in THEMES]:
    loc = f"<loc>{BASE}{u}</loc>"
    if loc not in sm:
        sm = sm.replace("</urlset>", f"<url>{loc}</url></urlset>"); added += 1
sm_path.write_text(sm, encoding="utf-8")
print(f"sitemap: {added} URLs added")
print("DONE")

#!/usr/bin/env python3
"""Publish Reformed Vietnam's own Vietnamese translations (EPUBs in sach/).

For every book listed in BOOKS below this script:
  1. builds an in-site reading page doc/<slug>.html from the EPUB's chapters,
  2. (no cover images: covers were removed),
  3. upserts a catalog entry "rv-<slug>" at the top of mg.json["vn"]
     (url = reading page, epub = download), so the library app shows it.

Run from the repo root:  python3 tools/build-vn-books.py
Then run tools/build-pages.py so tieng-viet.html and sitemap.xml pick the books up.
To add a book: drop the EPUB in sach/<slug>.epub and add one entry to BOOKS.

2026-11-05 (Batch D, site design-consistency fix): doc/ pages now use the shared
site chrome -- /s.css?v=20261126, the canonical 7-link nav.top + #th theme toggle,
the unified header.site/footer.site shell from hub.html (roadmap items 1+2,
2026-11-26; frozen SHELL_HEADER/SHELL_FOOTER constants, kept in sync via
scripts/check_shell_sync.py) and the rv.ptheme theme bootstrap (previously a
third design system: inline-only CSS, 3-link nav, no theme toggle). In-content <h1> from EPUB
chapter bodies is demoted to <h2> (the hero <h1> is the page title; M8). Pages
whose sermon also has a bai-giang/ teaser get a back-link (H4). BOOKS gained the
two sermons that were live in doc/ but missing from this file (compel-them-to-
come-in, do-you-pray); their metadata comes from mg.json (rv-* entries).
"""
import json, os, re, zipfile
from html import escape as E

SITE = "https://reformedvietnam.com"
EMAIL = "reformedvn@gmail.com"

# slug: (author, year, type, colour, en title, vi subtitle/description, en description)
BOOKS = {
    "mccheyne-cac-con-hay-chay-den-cung-dang-christ": ("Robert Murray M'Cheyne", 1840, "sermons", "#264e60",
        "Reasons Why Children Should Fly to Christ Without Delay",
        "Bài giảng ngắn cho thiếu nhi: bốn lý do các em nên đến với Chúa Jêsus ngay hôm nay. Kèm bài thơ M'Cheyne viết cho trẻ em.",
        "A short sermon for children giving four reasons to come to Jesus now, with M'Cheyne's poem for children."),
    "edwards-bay-muoi-quyet-tam": ("Jonathan Edwards", 1723, "devotional", "#28344e",
        "The Resolutions",
        "Bảy mươi quyết tâm Edwards viết khi mới 19–20 tuổi để sống trọn đời cho vinh hiển Đức Chúa Trời.",
        "The seventy resolutions Edwards wrote at 19–20 to live wholly for the glory of God."),
    "mccheyne-banh-hang-ngay": ("Robert Murray M'Cheyne", 1842, "devotional", "#482c24",
        "Daily Bread (Bible Reading Calendar)",
        "Lá thư của M'Cheyne cùng lịch đọc trọn Kinh Thánh trong một năm: Cựu Ước một lần, Tân Ước và Thi-thiên hai lần.",
        "M'Cheyne's letter and one-year Bible reading calendar: Old Testament once, New Testament and Psalms twice."),
    "spurgeon-y-chi-tu-do-mot-ke-no-le": ("C. H. Spurgeon", 1855, "sermons", "#342c46",
        "Free Will — A Slave",
        "Bài giảng về Giăng 5:40: theo bản chất, con người không muốn đến với Đấng Christ, nhưng mọi người đến đều được sự sống.",
        "Sermon on John 5:40: by nature no one will come to Christ, yet all who come receive life."),
    "whitefield-con-duong-cua-an-dien": ("George Whitefield", 1741, "sermons", "#4a3a1e",
        "The Method of Grace",
        "Bài giảng phấn hưng về Giê-rê-mi 6:14: sự bình an thật và sự bình an giả dối, và con đường đến với Đấng Christ.",
        "Revival sermon on Jeremiah 6:14 on true and false peace and the way to Christ."),
    "edwards-toi-nhan-trong-tay-duc-chua-troi-thanh-no": ("Jonathan Edwards", 1741, "sermons", "#3c1e16",
        "Sinners in the Hands of an Angry God",
        "Bài giảng nổi tiếng nhất của cuộc Đại Phấn Hưng, giảng tại Enfield năm 1741, về Phục-truyền 32:35.",
        "The most famous sermon of the Great Awakening, preached at Enfield in 1741 on Deuteronomy 32:35."),
    "newton-cay-non-bong-lua-hot-chac": ("John Newton", 1772, "devotional", "#2c4634",
        "Grace in the Blade, the Ear, and the Full Corn",
        "Ba lá thư về ba giai đoạn tăng trưởng trong ân điển: khao khát, chiến đấu và chiêm ngưỡng (Mác 4:28).",
        "Three letters on growth in grace: desire, conflict and contemplation (Mark 4:28)."),
    "chalmers-quyen-nang-cua-mot-tinh-yeu-moi": ("Thomas Chalmers", 1819, "sermons", "#5c2228",
        "The Expulsive Power of a New Affection",
        "Bài giảng kinh điển về 1 Giăng 2:15: chỉ một tình yêu mới, lớn hơn — tình yêu Đức Chúa Trời — mới đuổi được lòng yêu thế gian.",
        "Classic sermon on 1 John 2:15: only a greater love for God can expel the love of the world."),
    "spurgeon-loi-benh-vuc-thuyet-calvin": ("C. H. Spurgeon", 1861, "doctrine", "#1e3a46",
        "A Defence of Calvinism",
        "Spurgeon kể cách ông học biết ân điển, và trả lời những lời cáo buộc thường gặp về các giáo lý ân điển.",
        "Spurgeon on how he learned the doctrines of grace, answering common charges against them."),
    "compel-them-to-come-in": ("Charles Spurgeon", 1858, "sermons", "#0d1b2a",
        "Compel Them to Come In",
        "Lời kêu gọi tha thiết đến với những ai còn xa lạ với Phúc Âm Đấng Christ",
        "Spurgeon's famous evangelistic sermon on the parable of the great supper."),
    "do-you-pray": ("J.C. Ryle", 1880, "devotional", "#0d1b2a",
        "Do You Pray?",
        "Bảy lý do vì sao sự cầu nguyện riêng tư là điều quan trọng nhất trong đời sống đạo",
        "J.C. Ryle's searching, practical tract on the necessity and marks of real prayer."),
}

FONT = ''  # was Google Fonts CDN (Noto Serif); fonts are now self-hosted via @font-face in s.css — see tools/build-pages.py _CSS_REST
CSS = """
.toc{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px 18px;font:15px/1.6 system-ui,sans-serif;margin:18px 0 8px}
.toc ol{margin:.3em 0 0;padding-left:1.2em}
.ch{border-top:1px solid var(--line);margin-top:2.5em;padding-top:.5em}
.sub{text-align:center;font-style:italic;color:var(--mut)}
.scripture-quote{font-style:italic;text-align:center;color:var(--acc)}
table.gloss{width:100%;border-collapse:collapse;font-size:.9em;margin:1em 0}
table.gloss td{border-bottom:1px solid var(--line);padding:.4em .5em;vertical-align:top}
.epi{margin:1.4em 8%;text-align:center;font-style:italic}.epi p{text-align:center}.epi .ref{display:block;font-style:normal;font-size:.9em;color:var(--mut)}
.salute{font-style:italic;margin-top:1.4em}.sign{text-align:right;font-style:italic}
.lbl,.num{font-weight:700}.date{font-size:.85em;font-style:italic;color:var(--mut);white-space:nowrap}
ol.res{list-style:none;padding:0}ol.res li{margin:0 0 1em}
.center{text-align:center}.orn{text-align:center;letter-spacing:.5em;color:var(--mut);margin:1.4em 0}
.note{font-size:.9em;color:var(--mut)}
table.cal{width:100%;border-collapse:collapse;font-size:.85em;margin-bottom:1.5em}
table.cal th{border-bottom:2px solid var(--fg);text-align:left;padding:.3em;font-family:system-ui,sans-serif}
table.cal td{border-bottom:1px solid var(--line);padding:.3em;vertical-align:top}table.cal td.d{font-weight:700;text-align:center;width:2.2em}
.acts{text-align:center;margin:16px 0}
.warn{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:10px 14px;font:14px/1.5 system-ui,sans-serif;color:var(--mut);margin:16px 0}
.top-btn{position:fixed;right:14px;bottom:14px;background:var(--acc);color:#fff;border-radius:50%;width:42px;height:42px;display:grid;place-items:center;text-decoration:none;font:20px system-ui;opacity:.85}
"""

# Unified site shell (roadmap items 1+2, 2026-11-26): the header/footer
# below mirror hub.html's <header class="site"> / <footer class="site">
# verbatim (extracted the same way scripts/hub_page.py does). They are
# FROZEN string constants — NOT a live hub_page import — so that doc/ pages
# use the exact same markup as tools/build-pages.py page() (which cannot
# import hub_page: gen4.py extracts page() by AST closure). If hub.html's
# shell changes, update these constants and run scripts/check_shell_sync.py.
SHELL_HEADER = """<header class="site">
      <div class="wrap">
        <div class="nav-row">
          <a class="brand" href="/#top">
            <span class="mark">Reformed Vietnam</span>
            <span class="sub">Thư viện Cải Chánh</span>
          </a>
          <button class="menu-btn" id="menuBtn" aria-label="Mở menu" aria-expanded="false">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><line x1="4" y1="7" x2="20" y2="7"/><line x1="4" y1="12" x2="20" y2="12"/><line x1="4" y1="17" x2="20" y2="17"/></svg>
          </button>
          <nav class="main" id="mainNav">
            <a href="/#thu-vien">Thư Viện<span class="gloss">Kho sách để đọc</span></a>
            <a href="/#giao-ly">Giáo Lý<span class="gloss">Câu hỏi đáp ngắn về đức tin</span></a>
            <a href="/#bach-khoa">Bách Khoa<span class="gloss">Giải nghĩa các từ thần học</span></a>
            <a href="/#hoi-dap">Hỏi Đáp<span class="gloss">Giải đáp thắc mắc thường gặp</span></a>
            <a href="/#hoc-vien">Học Viện<span class="gloss">Khóa học theo từng bước</span></a>
            <a href="/bai-giang/">Bài Giảng<span class="gloss">Nghe giảng theo đoạn Kinh Thánh</span></a>
            <a href="/thanh-ca/">Thánh Ca<span class="gloss">Bài hát thờ phượng</span></a>
          </nav>
          <button class="theme-btn" id="themeBtn" type="button" title="Sáng/Tối" aria-label="Chế độ sáng tối">◐</button>
          <a class="nav-cta" href="/#tinh-nguyen">Tĩnh Nguyện Hôm Nay</a>
        </div>
      </div>
    </header>"""
SHELL_FOOTER = """<footer class="site">
      <div class="wrap">
        <div class="foot-grid">
          <div>
            <h4>Reformed Vietnam</h4>
            <p class="foot-about">Thư viện thần học Cải Chánh tiếng Việt — dự án cá nhân độc lập. Bản dịch ghi nhãn rõ ràng, đang chờ duyệt thần học.</p>
          </div>
          <div>
            <h4>Học tập</h4>
            <ul>
              <li><a href="/#thu-vien">Thư Viện Sách</a></li>
              <li><a href="/#giao-ly">Giáo Lý Hỏi Đáp</a></li>
              <li><a href="/#bach-khoa">Bách Khoa Thần Học</a></li>
              <li><a href="/#hoc-vien">Học Viện Cải Chánh</a></li>
              <li><a href="/ai-dung-sau-trang-nay.html">Tuyên Xưng Đức Tin</a></li>
            </ul>
          </div>
          <div>
            <h4>Đời sống</h4>
            <ul>
              <li><a href="/#tinh-nguyen">Ân Điển Mỗi Ngày</a></li>
              <li><a href="/#sach-noi">Sách Nói</a></li>
              <li><a href="/#hoi-dap">Hỏi Đáp Cải Chánh</a></li>
              <li><a href="/bai-giang/">Bài Giảng</a></li>
              <li><a href="/thanh-ca/">Thánh Ca &amp; Thờ Phượng</a></li>
            </ul>
          </div>
          <div>
            <h4>Liên hệ</h4>
            <ul>
              <li><a href="mailto:reformedvn@gmail.com">reformedvn@gmail.com</a></li>
              <li><a href="mailto:reformedvn@gmail.com?subject=B%C3%A1o%20l%E1%BB%97i%20b%E1%BA%A3n%20d%E1%BB%8Bch">Báo lỗi bản dịch</a></li>
              <li><a href="mailto:reformedvn@gmail.com?subject=B%E1%BA%A3n%20quy%E1%BB%81n">Liên hệ bản quyền / gỡ nội dung</a></li>
                            <li><a href="https://www.facebook.com/profile.php?id=61587505389829" target="_blank" rel="noopener">Facebook — Reformed Vietnam</a></li>
              <li><a href="https://youtube.com/@reformedvietnam" target="_blank" rel="noopener">YouTube — @reformedvietnam</a></li>
              <li><a href="https://www.tiktok.com/@reformed.vietnam" target="_blank" rel="noopener">TikTok — @reformed.vietnam</a></li>
              <li><a href="https://www.threads.net/@reformedvietnam" target="_blank" rel="noopener">Threads — @reformedvietnam</a></li>
              <li><a href="https://www.instagram.com/reformedvietnam" target="_blank" rel="noopener">Instagram — @reformedvietnam</a></li>
              <li><a href="https://open.spotify.com/show/0uNIEUJtUUic9FYsu2rj8k" target="_blank" rel="noopener">Spotify — Sách Nói Cải Chánh (153 tập)</a></li>
              <li><a href="https://archive.org/search?query=creator%3A%22Reformed+Vietnam%22" target="_blank" rel="noopener">Archive.org — Nghe sách nói</a></li>
            </ul>
          </div>
        </div>
        <div class="share-bar" style="padding-top:22px">
          <span class="share-lbl">Chia sẻ trang này</span>
          <a class="share-btn fb" href="https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Freformedvietnam.com%2F" target="_blank" rel="noopener" aria-label="Chia sẻ lên Facebook">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M13.5 21v-7.2h2.4l.4-2.8h-2.8V9.2c0-.8.2-1.4 1.4-1.4h1.5V5.3c-.3 0-1.2-.1-2.2-.1-2.2 0-3.7 1.3-3.7 3.8v2H8v2.8h2.5V21h3z"/></svg>
            Facebook
          </a>
          <a class="share-btn zalo" href="https://sp.zalo.me/share_inline?url=https%3A%2F%2Freformedvietnam.com%2F" target="_blank" rel="noopener" aria-label="Chia sẻ qua Zalo">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 11.5a8.5 8.5 0 0 1-8.5 8.5c-1.5 0-2.9-.4-4.1-1L3 20l1.1-5.2A8.5 8.5 0 1 1 21 11.5z"/></svg>
            Zalo
          </a>
        </div>
        <div class="foot-bottom">
          <span>© 2026 Reformed Vietnam</span>
          <span>Sách dịch từ nguyên tác thuộc phạm vi công cộng hoặc được phép sử dụng miễn phí.</span>
        </div>
      </div>
    </footer>"""
# The hub footer's share-bar shares the HOMEPAGE url (hardcoded); doc/ pages
# have no per-page share row, so strip it (same rule as build-pages.py).
if '<div class="share-bar"' in SHELL_FOOTER:
    _stripped = re.sub(r'\s*<div class="share-bar".*?</div>(?=\s*<div class="foot-bottom">)', "", SHELL_FOOTER, flags=re.S)
    assert _stripped != SHELL_FOOTER, "shell footer share-bar present but strip pattern no longer matches hub.html"
    SHELL_FOOTER = _stripped

THEME_BOOT = '<script>try{var _t=localStorage.getItem("rv.theme")||localStorage.getItem("rv.ptheme");if(_t)document.documentElement.setAttribute("data-theme",_t)}catch(e){}</script>'
SHELL_JS = """<script>(function(){var b=document.getElementById("menuBtn"),n=document.getElementById("mainNav");if(b&&n){b.addEventListener("click",function(){var o=n.classList.toggle("open");b.setAttribute("aria-expanded",o?"true":"false")});n.addEventListener("click",function(e){if(e.target.tagName==="A")n.classList.remove("open")})}var t=document.getElementById("themeBtn");if(t)t.onclick=function(){var h=document.documentElement,d=h.getAttribute("data-theme")==="dark"||(!h.getAttribute("data-theme")&&matchMedia("(prefers-color-scheme:dark)").matches),c=d?"light":"dark";h.setAttribute("data-theme",c);try{localStorage.setItem("rv.theme",c);localStorage.setItem("rv.ptheme",c)}catch(e){}var mc=document.querySelector('meta[name="theme-color"]');if(mc)mc.setAttribute("content",c==="dark"?"#14171c":"#9a3412")}})()</script>"""
# Slugs that also have a bai-giang/ teaser page (H4 cross-link; the other 2 doc/
# sermons have no teaser, so no back-link is emitted for them).
BAI_GIANG = {
    "compel-them-to-come-in", "do-you-pray", "edwards-toi-nhan-trong-tay-duc-chua-troi-thanh-no",
    "mccheyne-cac-con-hay-chay-den-cung-dang-christ", "newton-cay-non-bong-lua-hot-chac",
    "spurgeon-loi-benh-vuc-thuyet-calvin", "spurgeon-y-chi-tu-do-mot-ke-no-le",
    "whitefield-con-duong-cua-an-dien", "chalmers-quyen-nang-cua-mot-tinh-yeu-moi",
}

def _demote_h1(html):
    """M8: EPUB chapter bodies may open with an <h1> duplicating the page title
    (the hero <h1> above the TOC is the page title). Demote every in-content
    <h1> to <h2> so each doc/ page has exactly one <h1>."""
    html = re.sub(r"<h1(\s[^>]*)?>", r"<h2\1>", html)
    return html.replace("</h1>", "</h2>")


def chapters(epub):
    z = zipfile.ZipFile(epub)
    opf = z.read("OEBPS/content.opf").decode()
    hrefs = dict(re.findall(r'<item id="([^"]+)" href="([^"]+)"', opf))
    spine = re.findall(r'<itemref idref="([^"]+)"', opf)
    nav = z.read("OEBPS/nav.xhtml").decode()
    titles = dict(re.findall(r'<a href="([^"]+)">([^<]+)</a>', nav))
    out = []
    for sid in spine:
        if sid in ("cover", "title"):
            continue
        h = hrefs[sid]
        body = re.search(r"<body>(.*)</body>", z.read("OEBPS/" + h).decode(), re.S).group(1).strip()
        out.append((sid, titles.get(h, sid), body))
    return z, out

def main():
    os.makedirs("doc", exist_ok=True)
    mg = json.load(open("mg.json", encoding="utf-8"))
    entries = []
    for slug, (author, year, ty, col, en_t, vi_d, en_d) in BOOKS.items():
        epub = f"sach/{slug}.epub"
        z, chs = chapters(epub)
        opf = z.read("OEBPS/content.opf").decode()
        vi_t = re.search(r"<dc:title>([^<]+)</dc:title>", opf).group(1)
        toc = "".join(f'<li><a href="#{sid}">{E(t)}</a></li>' for sid, t, _ in chs if sid != "colophon")
        body = "".join(f'<section class="ch" id="{sid}">{_demote_h1(html)}</section>' for sid, _, html in chs)
        path = f"doc/{slug}.html"
        url = f"{SITE}/{path}"
        title = f"{vi_t} – {author} | Đọc miễn phí bằng tiếng Việt"
        mail = f"mailto:{EMAIL}?subject=" + E(f"Góp ý bản dịch: {vi_t}")
        ld = {"@context": "https://schema.org", "@type": "Book", "name": vi_t, "inLanguage": "vi",
              "author": {"@type": "Person", "name": author}, "translationOfWork": {"@type": "Book", "name": en_t},
              "url": url, "isAccessibleForFree": True}
        back = f'<p class="m"><a href="/bai-giang/{slug}.html">← Về bài giới thiệu</a></p>' if slug in BAI_GIANG else ""
        page = f"""<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title><meta name="description" content="{E(vi_d)}"><link rel="canonical" href="{url}">
<meta property="og:type" content="book"><meta property="og:title" content="{E(vi_t)} – {E(author)}"><meta property="og:description" content="{E(vi_d)}"><meta property="og:url" content="{url}"><meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">{FONT}{THEME_BOOT}<style>{CSS}</style><link rel="stylesheet" href="/s.css?v=20261126"><script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script></head><body>{SHELL_HEADER}<main id="top">
<h1>{E(vi_t)}</h1><p class="m">{E(author)} · {year} · Nguyên tác: <i>{E(en_t)}</i></p>
<div class="acts"><a class="btn" href="/sach/{slug}.epub" download>⬇ Tải EPUB</a><a class="btn s" href="/reader.html?id=vn/{slug}&amp;pid=rv-{slug}">Mở trong trình đọc</a></div>
<p class="warn">Bản dịch tiếng Việt của Reformed Vietnam từ nguyên tác thuộc phạm vi công cộng. Đây là bản dịch sơ thảo, chưa được hiệu đính. Thấy lỗi? <a href="{mail}">Góp ý bản dịch</a>.</p>
<nav class="toc" aria-label="Mục lục"><b>Mục lục</b><ol>{toc}</ol></nav>
{body}
{back}
</main>
{SHELL_FOOTER}
<a class="top-btn" href="#top" aria-label="Lên đầu trang">↑</a>{SHELL_JS}</body></html>"""
        open(path, "w", encoding="utf-8").write(page)
        entries.append({"id": f"rv-{slug}", "ty": ty, "y": year, "col": col, "a": author,
                        "url": f"/{path}", "epub": f"/{epub}",
                        "en": {"t": f"{en_t} (Vietnamese)", "n": f"Reformed Vietnam translation (draft, unreviewed). {en_d}"},
                        "vi": {"t": vi_t, "n": f"Bản dịch của Reformed Vietnam (sơ thảo, chưa hiệu đính). {vi_d}"}})
        print("built", path, len(chs), "sections")
    ids = {e["id"] for e in entries}
    mg["vn"] = entries + [r for r in mg["vn"] if r["id"] not in ids and not r["id"].startswith("rv-")]
    open("mg.json", "w", encoding="utf-8").write(json.dumps(mg, ensure_ascii=False, separators=(",", ":")))
    print("mg.json vn entries:", len(mg["vn"]))

if __name__ == "__main__":
    main()

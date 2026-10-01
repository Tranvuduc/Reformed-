#!/usr/bin/env python3
"""Publish Reformed Vietnam's own Vietnamese translations (EPUBs in sach/).

For every book listed in BOOKS below this script:
  1. builds an in-site reading page doc/<slug>.html from the EPUB's chapters,
  2. extracts the cover to sach/<slug>.jpg,
  3. upserts a catalog entry "rv-<slug>" at the top of mg.json["vn"]
     (url = reading page, epub = download), so the library app shows it.

Run from the repo root:  python3 tools/build-vn-books.py
Then run tools/build-pages.py so tieng-viet.html and sitemap.xml pick the books up.
To add a book: drop the EPUB in sach/<slug>.epub and add one entry to BOOKS.
"""
import json, os, re, zipfile
from html import escape as E

SITE = "https://reformed-vietnam.vercel.app"
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
}

FONT = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@600;700&family=Noto+Serif:ital,wght@0,400;0,700;1,400&display=swap" rel="stylesheet">'
CSS = """
:root{--bg:#f4efe4;--fg:#26211a;--mut:#6f665a;--ac:#9a3412;--ln:#ddd3c2;--card:#fbf8f1}
@media (prefers-color-scheme:dark){:root{--bg:#1c1915;--fg:#ebe4d6;--mut:#a59a89;--ac:#f0a374;--ln:#3a342b;--card:#24201b}}
html{scroll-behavior:smooth}body{margin:0;background:var(--bg);color:var(--fg);font:18px/1.75 "Noto Serif",Georgia,serif}
main{max-width:40rem;margin:0 auto;padding:22px 18px 80px}a{color:var(--ac)}
nav.top{font:14px system-ui,sans-serif;margin-bottom:22px}
h1,h2,h3{font-family:"Be Vietnam Pro",system-ui,sans-serif;font-weight:600;line-height:1.3}
h1{font-size:1.9rem;margin:.6em 0 .2em;text-align:center}h2{font-size:1.35rem;margin:2.2em 0 .8em;text-align:center}h3{font-size:1.1rem;margin:1.8em 0 .5em}
p{margin:0 0 1em;text-align:justify}.m{color:var(--mut);font:14px system-ui,sans-serif;text-align:center}
.hero{text-align:center;margin-bottom:10px}.hero img{width:180px;max-width:50%;height:auto;border-radius:4px;box-shadow:0 6px 20px rgba(0,0,0,.25)}
.acts{text-align:center;margin:16px 0}.btn{display:inline-block;background:var(--ac);color:#fff;padding:9px 18px;border-radius:8px;text-decoration:none;font:600 15px system-ui,sans-serif;margin:4px}
.btn.s{background:none;color:var(--ac);border:1px solid var(--ac)}
.warn{background:var(--card);border:1px solid var(--ln);border-radius:10px;padding:10px 14px;font:14px/1.5 system-ui,sans-serif;color:var(--mut);margin:16px 0}
.toc{background:var(--card);border:1px solid var(--ln);border-radius:10px;padding:12px 18px;font:15px/1.6 system-ui,sans-serif;margin:18px 0 8px}
.toc ol{margin:.3em 0 0;padding-left:1.2em}
.ch{border-top:1px solid var(--ln);margin-top:2.5em;padding-top:.5em}
.sub{text-align:center;font-style:italic;color:var(--mut)}
.epi{margin:1.4em 8%;text-align:center;font-style:italic}.epi p{text-align:center}.epi .ref{display:block;font-style:normal;font-size:.9em;color:var(--mut)}
.salute{font-style:italic;margin-top:1.4em}.sign{text-align:right;font-style:italic}
.lbl,.num{font-weight:700}.date{font-size:.85em;font-style:italic;color:var(--mut);white-space:nowrap}
ol.res{list-style:none;padding:0}ol.res li{margin:0 0 1em}
.center{text-align:center}.orn{text-align:center;letter-spacing:.5em;color:var(--mut);margin:1.4em 0}
.note{font-size:.9em;color:var(--mut)}
table.cal{width:100%;border-collapse:collapse;font-size:.85em;margin-bottom:1.5em}
table.cal th{border-bottom:2px solid var(--fg);text-align:left;padding:.3em;font-family:"Be Vietnam Pro",system-ui,sans-serif}
table.cal td{border-bottom:1px solid var(--ln);padding:.3em;vertical-align:top}table.cal td.d{font-weight:700;text-align:center;width:2.2em}
footer{margin-top:50px;font:13px system-ui,sans-serif;color:var(--mut);text-align:center}
.top-btn{position:fixed;right:14px;bottom:14px;background:var(--ac);color:#fff;border-radius:50%;width:42px;height:42px;display:grid;place-items:center;text-decoration:none;font:20px system-ui;opacity:.85}
"""

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
        open(f"sach/{slug}.jpg", "wb").write(z.read("OEBPS/cover.jpg"))
        opf = z.read("OEBPS/content.opf").decode()
        vi_t = re.search(r"<dc:title>([^<]+)</dc:title>", opf).group(1)
        toc = "".join(f'<li><a href="#{sid}">{E(t)}</a></li>' for sid, t, _ in chs if sid != "colophon")
        body = "".join(f'<section class="ch" id="{sid}">{html}</section>' for sid, _, html in chs)
        path = f"doc/{slug}.html"
        url = f"{SITE}/{path}"
        title = f"{vi_t} – {author} | Đọc miễn phí bằng tiếng Việt"
        mail = f"mailto:{EMAIL}?subject=" + E(f"Góp ý bản dịch: {vi_t}")
        ld = {"@context": "https://schema.org", "@type": "Book", "name": vi_t, "inLanguage": "vi",
              "author": {"@type": "Person", "name": author}, "translationOfWork": {"@type": "Book", "name": en_t},
              "url": url, "image": f"{SITE}/sach/{slug}.jpg", "isAccessibleForFree": True}
        page = f"""<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title><meta name="description" content="{E(vi_d)}"><link rel="canonical" href="{url}">
<meta property="og:type" content="book"><meta property="og:title" content="{E(vi_t)} – {E(author)}"><meta property="og:description" content="{E(vi_d)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{SITE}/sach/{slug}.jpg"><meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">{FONT}<style>{CSS}</style><script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script></head><body><main id="top">
<nav class="top"><a href="/">Reformed Vietnam</a> · <a href="/tieng-viet.html">Sách tiếng Việt</a> · <a href="/tac-gia.html">Tác giả</a></nav>
<div class="hero"><img src="/sach/{slug}.jpg" alt="Bìa sách {E(vi_t)}" width="360" height="540"></div>
<h1>{E(vi_t)}</h1><p class="m">{E(author)} · {year} · Nguyên tác: <i>{E(en_t)}</i></p>
<div class="acts"><a class="btn" href="/sach/{slug}.epub" download>⬇ Tải EPUB</a><a class="btn s" href="#{chs[0][0]}">Đọc ngay</a></div>
<p class="warn">Bản dịch tiếng Việt của Reformed Vietnam từ nguyên tác thuộc phạm vi công cộng. Đây là bản dịch sơ thảo, chưa được hiệu đính. Thấy lỗi? <a href="{mail}">Góp ý bản dịch</a>.</p>
<nav class="toc" aria-label="Mục lục"><b>Mục lục</b><ol>{toc}</ol></nav>
{body}
<footer>Reformed Vietnam · Thư viện sách Cải Chánh miễn phí · <a href="/">Mở thư viện</a> · <a href="{mail}">{EMAIL}</a></footer></main>
<a class="top-btn" href="#top" aria-label="Lên đầu trang">↑</a></body></html>"""
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

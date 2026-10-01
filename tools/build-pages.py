#!/usr/bin/env python3
"""Generate static, crawlable pages: author pages (a/), book pages (b/), hubs and sitemap.xml.
Run from the repo root: python3 tools/build-pages.py"""
import json, os, re, shutil, unicodedata
from html import escape as E

SITE = "https://reformed-vietnam.vercel.app"
books = json.load(open("books.json", encoding="utf-8"))
mg = json.load(open("mg.json", encoding="utf-8"))
vi = json.load(open("vi.json", encoding="utf-8"))
desc = json.load(open("desc.json", encoding="utf-8"))["d"]
ia = json.load(open("ia.json", encoding="utf-8")) if os.path.exists("ia.json") else {"a": [], "b": []}

def slug(s):
    s = unicodedata.normalize("NFKD", s.replace("đ", "d").replace("Đ", "D"))
    s = "".join(c for c in s if not unicodedata.combining(c)).lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")[:70]

CSS = ("body{margin:0;background:#f4efe4;color:#26211a;font:17px/1.6 Georgia,serif}main{max-width:46rem;margin:0 auto;padding:24px 18px 60px}"
       "a{color:#9a3412}nav.top{font:14px system-ui,sans-serif;margin-bottom:18px}h1{font-size:1.9rem;line-height:1.2;margin:.2em 0 .5em}"
       "ul{padding-left:1.1em}li{margin:.5em 0}small,.m{color:#6f665a;font:14px system-ui,sans-serif}.btn{display:inline-block;background:#9a3412;color:#fff;"
       "padding:8px 16px;border-radius:8px;text-decoration:none;font:600 15px system-ui,sans-serif;margin:4px 6px 4px 0}.btn.s{background:none;color:#9a3412;border:1px solid #9a3412}"
       "footer{margin-top:40px;font:13px system-ui,sans-serif;color:#6f665a}")

def page(title, desc_, path, body, ld=None):
    url = f"{SITE}/{path}"
    j = f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>' if ld else ""
    return f'''<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title><meta name="description" content="{E(desc_)}"><link rel="canonical" href="{url}">
<meta property="og:type" content="article"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc_)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{SITE}/og.png"><meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.svg" type="image/svg+xml"><style>{CSS}</style>{j}</head><body><main>
<nav class="top"><a href="/">Reformed Vietnam</a> · <a href="/tac-gia.html">Tác giả</a> · <a href="/tieng-viet.html">Tiếng Việt</a> · <a href="/sach-noi.html">Sách nói</a> · <a href="/lo-trinh.html">Lộ trình đọc</a></nav>
{body}
<footer>Thư viện sách Cải Chánh miễn phí · <a href="/">Mở thư viện</a> · Liên hệ: reformedvn@gmail.com</footer></main></body></html>'''

for d in ("a", "b"):
    shutil.rmtree(d, ignore_errors=True); os.makedirs(d)

authors = {}  # slug -> dict(name, ccel:[], ia:[])
for au in books["authors"]:
    k = slug(au["name"]); a = authors.setdefault(k, {"name": au["name"], "ccel": [], "ia": [], "id": au["id"]})
    for b in au["books"]:
        a["ccel"].append((f'{au["id"]}/{b[0]}', b[1], b[2] if len(b) > 2 else 0))
for r in ia["b"]:
    nm = ia["a"][r[0]]; k = slug(nm)
    a = authors.setdefault(k, {"name": nm, "ccel": [], "ia": [], "id": ""})
    a["ia"].append(r)

urls = ["", "about.html", "tac-gia.html", "tieng-viet.html"]
count_b = 0

# book pages for described CCEL books
for k, a in authors.items():
    for bid, title, yr in a["ccel"]:
        if bid not in desc: continue
        en_d, vi_d = desc[bid]; vt = vi.get(bid, title)
        bs = slug(bid.replace("/", "-")); path = f"b/{bs}.html"
        ttl = f"{vt} – {a['name']} | Đọc miễn phí"
        body = (f'<h1>{E(vt)}</h1><p class="m">{E(title)} · {E(a["name"])}{f" · {yr}" if yr else ""}</p><p>{E(vi_d)}</p><p><small lang="en">{E(en_d)}</small></p>'
                f'<p><a class="btn" href="/reader.html?id={bid}">Đọc ngay</a> <a class="btn s" href="/a/{k}.html">Thêm sách của {E(a["name"])}</a></p>'
                '<p class="m">Tác phẩm thuộc phạm vi công cộng. Nguồn: Christian Classics Ethereal Library (CCEL). Đọc trực tuyến, tải EPUB/PDF và nghe đọc thành tiếng trong thư viện.</p>')
        ld = {"@context": "https://schema.org", "@type": "Book", "name": title, "alternateName": vt, "author": {"@type": "Person", "name": a["name"]},
              "inLanguage": "en", "isAccessibleForFree": True, "description": vi_d, "url": f"{SITE}/{path}"}
        open(path, "w", encoding="utf-8").write(page(ttl, vi_d, path, body, ld)); urls.append(path); count_b += 1
        a.setdefault("pages", {})[bid] = path

# author pages
for k, a in authors.items():
    items = []
    for bid, title, yr in a["ccel"][:80]:
        vt = vi.get(bid)
        link = "/" + a.get("pages", {}).get(bid, f"reader.html?id={bid}")
        lab = f"{E(vt)} <small>({E(title)})</small>" if vt and vt != title else E(title)
        d = f'<br><small>{E(desc[bid][1])}</small>' if bid in desc else ""
        items.append(f'<li><a href="{link}">{lab}</a>{f" <small>{yr}</small>" if yr else ""}{d}</li>')
    for r in a["ia"]:
        items.append(f'<li><a href="https://archive.org/details/{r[2]}" rel="noopener">{E(r[1])}</a> <small>{r[3] or ""}</small></li>')
    n = len(items)
    if n < 2: continue
    path = f"a/{k}.html"
    intro = f"{n} tác phẩm của {a['name']} có thể đọc hoặc tải miễn phí: sách thần học, bài giảng và tài liệu Cải Chánh thuộc phạm vi công cộng."
    body = f'<h1>{E(a["name"])} – sách miễn phí</h1><p>{E(intro)}</p><p><a class="btn" href="/?q={E(a["name"].split()[-1])}">Mở trong thư viện</a></p><ul>{"".join(items)}</ul>'
    ld = {"@context": "https://schema.org", "@type": "CollectionPage", "name": f"{a['name']} – sách miễn phí", "inLanguage": "vi", "url": f"{SITE}/{path}"}
    open(path, "w", encoding="utf-8").write(page(f"{a['name']} – sách miễn phí, đọc và tải | Reformed Vietnam", intro, path, body, ld)); urls.append(path); a["path"] = path

# author index
lis = "".join(f'<li><a href="/{a["path"]}">{E(a["name"])}</a> <small>({len(a["ccel"]) + len(a["ia"])})</small></li>' for a in sorted(authors.values(), key=lambda x: x["name"]) if "path" in a)
open("tac-gia.html", "w", encoding="utf-8").write(page("Tác giả Cải Chánh và Thanh giáo – sách miễn phí | Reformed Vietnam",
    "Danh sách tác giả Cải Chánh, Thanh giáo và Trưởng Lão: Calvin, Owen, Spurgeon, Ryle, Bunyan và nhiều người khác, với sách đọc miễn phí.", "tac-gia.html",
    f"<h1>Tác giả Cải Chánh và Thanh giáo</h1><p>Chọn một tác giả để xem sách đọc hoặc tải miễn phí.</p><ul>{lis}</ul>"))

# Vietnamese hub
vn = "".join(f'<li><a href="{E(r["url"])}" rel="noopener">{E(r["vi"]["t"])}</a> <small>· {E(r["a"])}</small></li>' for r in mg["vn"] if not r.get("au"))
open("tieng-viet.html", "w", encoding="utf-8").write(page("Sách và bài viết tiếng Việt về thần học Cải Chánh | Reformed Vietnam",
    "Tuyển chọn sách, tín điều, giáo lý và bài viết thần học Cải Chánh bằng tiếng Việt, đọc miễn phí từ Mục vụ Tiên Phong, 9Marks và các nguồn khác.", "tieng-viet.html",
    f"<h1>Sách và bài viết tiếng Việt</h1><p>{len([r for r in mg['vn'] if not r.get('au')])} tài liệu thần học Cải Chánh bằng tiếng Việt, dẫn đến nguồn gốc của từng tài liệu. Cảm ơn Mục vụ Tiên Phong và 9Marks đã chia sẻ.</p><ul>{vn}</ul>"))

# Audio hub
AUD=[("LibriVox trên Internet Archive","https://archive.org/details/librivoxaudio","Sách nói miễn phí do tình nguyện viên đọc (tiếng Anh): Bunyan, Spurgeon, Ryle, Bonar, Edwards và nhiều tác giả khác."),
("CCEL – các tác phẩm có bản nghe MP3","https://www.ccel.org/index/format/mp3","135 tác phẩm cổ điển có bản nghe MP3: Pilgrim's Progress, Calvin, Owen, Spurgeon, Westminster Confession."),
("Puritan Downloads – MP3 Thanh giáo và Cải Chánh","https://www.puritandownloads.com/free-puritan-reformation-mp3-audio-sermons-books/","Sách nói và bài giảng MP3 Thanh giáo miễn phí."),
("Kinh Thánh nghe – Bible.com (Kinh Thánh Hiện Đại)","https://www.bible.com/vi/audio-bible-app-versions/1638-vcb-vietnamese-contemporary-bible","Kinh Thánh tiếng Việt có âm thanh, nghe trên điện thoại."),
("Kinh Thánh nghe – Bản Dịch Mới (NVB)","https://www.bible.com/audio-bible-app-versions/449-nvb-kinh-th%C3%A1nh-b%E1%BA%A3n-d%E1%BB%8Bch-m%E1%BB%9Bi","Bản Dịch Mới, có âm thanh."),
("Ligonier – loạt bài giảng của R.C. Sproul","https://www.ligonier.org/learn/series","Nhiều loạt bài giảng âm thanh miễn phí (tiếng Anh)."),
("Desiring God – bài giảng của John Piper","https://www.desiringgod.org/messages","Bài giảng âm thanh miễn phí (tiếng Anh).")]
lis_a = "".join(f'<li><a href="{E(u)}" rel="noopener">{E(t)}</a><br><small>{E(d)}</small></li>' for t,u,d in AUD)
open("sach-noi.html", "w", encoding="utf-8").write(page("Sách nói và bài giảng Cải Chánh miễn phí | Reformed Vietnam",
    "Nơi nghe sách nói, bài giảng và Kinh Thánh âm thanh miễn phí: LibriVox, CCEL, Puritan Downloads, Bible.com, Ligonier, Desiring God.", "sach-noi.html",
    f"<h1>Sách nói và bài giảng miễn phí</h1><p>Các nguồn nghe miễn phí mà thư viện dẫn đến. Trong thư viện, lọc \"Có bản nghe\" để xem các sách có bản nghe. Trình đọc của chúng tôi cũng đọc to bằng giọng của thiết bị.</p><ul>{lis_a}</ul><p><a class=\"btn\" href=\"/?q=\">Mở thư viện</a></p>"))
urls.append("sach-noi.html")

exec(open('tools/plan.py', encoding='utf-8').read())
exec(open('tools/today.py', encoding='utf-8').read())

# sitemap
sm = "".join(f"<url><loc>{SITE}/{u}</loc></url>" for u in urls)
open("sitemap.xml", "w", encoding="utf-8").write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>\n')
print("pages:", len(urls), "book pages:", count_b, "author pages:", sum(1 for a in authors.values() if "path" in a))

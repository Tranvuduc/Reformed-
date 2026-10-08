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

CSS = ("body{margin:0;background:#f4efe4;color:#26211a;font:17px/1.6 'Noto Serif',Georgia,serif}main{max-width:46rem;margin:0 auto;padding:24px 18px 60px}"
       "a{color:#9a3412}nav.top{font:14px system-ui,sans-serif;margin-bottom:18px}h1{font-size:1.9rem;line-height:1.2;margin:.2em 0 .5em}"
       "ul{padding-left:1.1em}li{margin:.5em 0}small,.m{color:#6f665a;font:14px system-ui,sans-serif}.btn{display:inline-block;background:#9a3412;color:#fff;"
       "padding:8px 16px;border-radius:8px;text-decoration:none;font:600 15px system-ui,sans-serif;margin:4px 6px 4px 0}.btn.s{background:none;color:#9a3412;border:1px solid #9a3412}"
       ".shr{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:28px 0 0;font:14px system-ui,sans-serif}.shr span{color:#6f665a}.shr a,.shr button{border:1px solid #9a3412;color:#9a3412;background:none;border-radius:8px;padding:6px 12px;font:600 14px system-ui,sans-serif;text-decoration:none;cursor:pointer}.shr a.fb{background:#1877f2;border-color:#1877f2;color:#fff}"
       "footer{margin-top:40px;font:13px system-ui,sans-serif;color:#6f665a}")

exec(open("tools/og_images.py", encoding="utf-8").read())
import json as _sj
_su=_sj.load(open('subscribe.json')).get('url','')
SUBL=(f' · <a href="{_su}" rel="noopener">Nhận bài qua email</a>' if _su else '')
import re as _re_bc

from urllib.parse import quote as _q
def _share(url, title):
    t = re.split(r"\s+[|–]\s+", title)[0]
    return (f'<div class="shr" data-u="{E(url)}" data-t="{E(t)}"><span>Chia sẻ:</span>'
            f'<a class="fb" href="https://www.facebook.com/sharer/sharer.php?u={_q(url, safe="")}" target="_blank" rel="noopener">Facebook</a>'
            f'<a href="https://twitter.com/intent/tweet?url={_q(url, safe="")}&amp;text={_q(t)}" target="_blank" rel="noopener">X</a>'
            '<button type="button" data-cp>Sao chép liên kết</button></div>'
            '<script>(function(){var s=document.querySelector(".shr");if(!s)return;var c=s.querySelector("[data-cp]");c.onclick=function(){var u=s.dataset.u;'
            'if(navigator.share){navigator.share({title:s.dataset.t,url:u}).catch(function(){});return}'
            'if(navigator.clipboard){navigator.clipboard.writeText(u);c.textContent="✓ Đã sao chép"}};})()</script>')

def page(title, desc_, path, body, ld=None):
    url = f"{SITE}/{path}"
    j = f'<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>' if ld else ""
    if path.startswith(("a/", "b/")):
        _nm = _re_bc.split(r"\s+[–|]\s+", title)[0]
        _mid = ("Tác giả", f"{SITE}/tac-gia.html") if path.startswith("a/") else ("Sách tiếng Việt", f"{SITE}/tieng-viet.html")
        _bc = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Trang chủ", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": _mid[0], "item": _mid[1]},
            {"@type": "ListItem", "position": 3, "name": _nm, "item": url}]}
        j += f'<script type="application/ld+json">{json.dumps(_bc, ensure_ascii=False)}</script>'
    _og = f"{SITE}/{og_image(path, title, desc_)}"
    _sh = _share(url, title)
    return f'''<!doctype html><html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)}</title><meta name="description" content="{E(desc_)}"><link rel="canonical" href="{url}">
<meta property="og:type" content="article"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc_)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{_og}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:site_name" content="Reformed Vietnam"><meta property="og:locale" content="vi_VN"><meta name="twitter:image" content="{_og}"><meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="/favicon.svg" type="image/svg+xml"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Serif:ital,wght@0,400;0,700;1,400&display=swap"><style>{CSS}</style>{j}</head><body><main>
<nav class="top"><a href="/">Reformed Vietnam</a> · <a href="/tac-gia.html">Tác giả</a> · <a href="/tieng-viet.html">Tiếng Việt</a> · <a href="/sach-noi.html">Sách nói</a> · <a href="/lo-trinh.html">Lộ trình đọc</a> · <a href="/khoa-hoc.html">Học trực tuyến</a> · <a href="/trich-dan.html">Trích dẫn</a> · <a href="/bai-viet/">Bài viết</a></nav>
{body}
{_sh}
<footer>Thư viện sách Cải Chánh miễn phí · <a href="/">Mở thư viện</a>{SUBL} · Liên hệ: reformedvn@gmail.com</footer></main></body></html>'''

for d in ("a", "b"):
    shutil.rmtree(d, ignore_errors=True); os.makedirs(d)

authors = {}  # slug -> dict(name, ccel:[], ia:[])
for au in books["authors"]:
    k = slug(au["name"]); a = authors.setdefault(k, {"name": au["name"], "ccel": [], "ia": [], "id": au["id"]})
    for b in au["books"]:
        a["ccel"].append((f'{au["id"]}/{b[0]}', b[1], b[2] if len(b) > 2 else 0))
# Normalize duplicate/malformed Internet Archive author names to canonical forms.
# Without this, "Jean Calvin" vs "John Calvin", dated variants like
# "1616-1683 Owen, John", and authority strings like "Saint, Bishop of Hippo
# Augustine" each become separate author pages.
AUTHOR_ALIASES = {
    "Jean Calvin": "John Calvin",
    "1616-1683 Owen, John": "John Owen",
    "1628-1688 Bunyan, John": "John Bunyan",
    "Théodore de Bèze": "Theodore Beza",
    "B. B. Warfield": "Benjamin Warfield",
    "Benjamin Palmer": "Benjamin Morgan Palmer",
    "Saint, Bishop of Hippo Augustine": "Augustine of Hippo",
    "Saint, Patriarch of Alexandria, d. 373 Athanasius": "Athanasius of Alexandria",
    "Paul, d. 1617 Baynes": "Paul Baynes",
    "Thomas, d. 1632 Beard": "Thomas Beard",
}
for r in ia["b"]:
    nm = AUTHOR_ALIASES.get(ia["a"][r[0]], ia["a"][r[0]]); k = slug(nm)
    a = authors.setdefault(k, {"name": nm, "ccel": [], "ia": [], "id": ""})
    a["ia"].append(r)
import re as _re
def _pretty(n):
    m = _re.match(r"^(\d{3,4})\s*-\s*(\d{3,4})?\s*([^,]+),\s*(.+)$", n)
    return f"{m.group(4)} {m.group(3)} ({m.group(1)}\u2013{m.group(2) or ''})" if m else n
for _a in authors.values(): _a["name"] = _pretty(_a["name"])

urls = ["", "about.html", "tac-gia.html", "tieng-viet.html"]
count_b = 0
PLAIN_B = []
NR = set(books.get('noread', []))

# book pages for described CCEL books
# One-line significance notes for the most-read Reformed/Puritan authors (SEO + reader orientation)
_AUTH_SIG = {
 "john-owen": "Được mệnh danh là 'vị vương tử của các nhà Thanh giáo', John Owen (1616–1683) là nhà thần học Thanh giáo có ảnh hưởng sâu rộng nhất, nổi tiếng với các luận thuyết về tội lỗi, sự nên thánh và Đức Thánh Linh.",
 "john-calvin": "John Calvin (1509–1564), nhà cải chánh Geneva, là kiến trúc sư của thần học Cải Chánh với bộ 'Thể chế Cơ Đốc giáo' (Institutes) làm nền tảng cho toàn bộ truyền thống Trưởng Lão và Cải Chánh.",
 "martin-luther": "Martin Luther (1483–1546) là người khơi mào cuộc Cải Chánh với 95 luận đề năm 1517, khôi phục giáo lý xưng công chính bởi đức tin cho Hội Thánh.",
 "charles-spurgeon": "Charles Spurgeon (1834–1892), 'vị vương tử của các nhà giảng đạo', là nhà giảng thuyết Baptist vĩ đại nhất thế kỷ 19 với hàng ngàn bài giảng đầy ân điển và quyền năng.",
 "jonathan-edwards": "Jonathan Edwards (1703–1758), nhà thần học vĩ đại nhất của Mỹ, là linh hồn của cuộc Đại Tỉnh Thức với những phân tích sâu sắc về ân điển, ý chí và cảm xúc thuộc linh.",
 "john-bunyan": "John Bunyan (1628–1688), người thợ thiếc trở thành nhà văn, là tác giả 'Thiên lộ lịch trình' — cuốn sách Cơ Đốc được đọc nhiều thứ hai sau Kinh Thánh.",
 "j-c-ryle": "J. C. Ryle (1816–1900), giám mục Liverpool, nổi tiếng với lối viết rõ ràng, thực tiễn và đầy lòng yêu mến bầy chiên qua các sách linh tu kinh điển.",
 "thomas-watson": "Thomas Watson (khoảng 1620–1686) là một trong những nhà Thanh giáo được yêu mến nhất, với lối giảng ấm áp, đầy hình ảnh minh họa và ứng dụng thực tiễn cho đời sống hằng ngày.",
 "richard-baxter": "Richard Baxter (1615–1691) là mục sư chăn bầy mẫu mực của Kidderminster và tác giả nhiều tác phẩm thực tiễn sâu sắc về đời sống Cơ Đốc.",
 "john-flavel": "John Flavel (khoảng 1630–1691) là nhà Thanh giáo nổi tiếng với những trang viết đầy cảm xúc về vẻ đẹp và vinh hiển của Đấng Christ.",
 "richard-sibbes": "Richard Sibbes (1577–1635), 'người nhỏ giọt mật ngọt', là tiếng nói êm dịu nhất của phong trào Thanh giáo, chuyên an ủi những tâm hồn tan vỡ.",
 "thomas-brooks": "Thomas Brooks (1608–1680) là nhà Thanh giáo thực tiễn, sắc bén trong việc vạch trần mưu chước của Sa-tan và hướng dẫn đời sống thánh khiết.",
 "jeremiah-burroughs": "Jeremiah Burroughs (1599–1646) để lại kiệt tác về sự thỏa lòng trong Đấng Christ — 'món báu vật hiếm có' cho mọi tín hữu.",
 "thomas-boston": "Thomas Boston (1676–1732), mục sư Scotland khiêm nhường, được yêu mến qua những suy ngẫm sâu sắc về chủ quyền Chúa và ân điển trong hoạn nạn.",
 "samuel-rutherford": "Samuel Rutherford (1600–1661), mục sư Scotland bị lưu đày, để lại những lá thư đầy lửa yêu mến Đấng Christ, được xem là kho tàng an ủi của Hội Thánh.",
 "john-knox": "John Knox (khoảng 1514–1572) là nhà cải chánh Scotland can đảm, người đặt nền móng cho Hội Thánh Trưởng Lão và viết nên lịch sử Cải Chánh Scotland.",
 "herman-bavinck": "Herman Bavinck (1854–1921) là nhà thần học Cải Chánh Hà Lan vĩ đại, với bộ 'Giáo lý Cải Chánh' (Reformed Dogmatics) được xem là đỉnh cao của thần học hệ thống hiện đại.",
 "abraham-kuyper": "Abraham Kuyper (1837–1920), vừa là nhà thần học vừa là thủ tướng Hà Lan, là người đặt nền cho thế giới quan Cải Chánh về mọi lãnh vực đời sống.",
 "charles-hodge": "Charles Hodge (1797–1878), giáo sư Princeton, là người bảo vệ đức tin Cải Chánh trước trào lưu tự do thần học thế kỷ 19.",
 "loraine-boettner": "Loraine Boettner (1901–1990) nổi tiếng với khả năng trình bày giáo lý tiền định và năm điểm Calvin một cách rõ ràng, có hệ thống cho độc giả hiện đại.",
 "james-p-boyce": "James P. Boyce (1827–1888), người sáng lập Chủng viện Southern Baptist, để lại bản tóm tắt thần học hệ thống súc tích và trung thành với Kinh Thánh.",
 "louis-berkhof": "Louis Berkhof (1873–1957) là tác giả các giáo trình thần học hệ thống được dùng rộng rãi nhất trong các chủng viện Cải Chánh thế kỷ 20.",
 "horatius-bonar": "Horatius Bonar (1808–1889), mục sư Scotland, nổi tiếng với những trang viết đơn sơ mà sâu sắc về Phúc Âm cho người mới tin.",
 "stephen-charnock": "Stephen Charnock (1628–1680) là nhà Thanh giáo uyên bác, với các luận thuyết kinh điển về thuộc tính Đức Chúa Trời và sự tái sinh.",
 "archibald-alexander": "Archibald Alexander (1772–1851), giáo sư đầu tiên của Chủng viện Princeton, là người đặt nền cho thần học Princeton với các tác phẩm biện giáo và chính điển học.",
 "lewis-bayly": "Lewis Bayly (khoảng 1565–1631), giám mục Bangor, là tác giả 'Thực hành lòng tin kính' — cuốn sách linh tu được yêu mến suốt nhiều thế kỷ.",
 "joseph-alleine": "Joseph Alleine (1634–1668) là nhà truyền giảng Thanh giáo đầy lửa, với 'Tiếng chuông báo động' kêu gọi tội nhân ăn năn.",
 "philip-doddridge": "Philip Doddridge (1702–1751) là mục sư và nhà giáo dục với những tác phẩm hướng dẫn đời sống Cơ Đốc từng bước rõ ràng, dễ hiểu.",
}
def _auth_sig(k):
    for frag, note in _AUTH_SIG.items():
        if frag in k: return note
    return ""

for k, a in authors.items():
    for bid, title, yr in a["ccel"]:
        if bid in NR: continue
        _plain = bid not in desc
        en_d, vi_d = desc[bid] if not _plain else ("", f"{title} của {a['name']}, sách thuộc phạm vi công cộng. Đọc trực tuyến miễn phí, nghe đọc thành tiếng hoặc tải EPUB/PDF trong thư viện Reformed Vietnam.")
        vt = vi.get(bid, title)
        _en_p = ('<p><small lang="en">' + E(en_d) + "</small></p>") if en_d else ""
        bs = slug(bid.replace("/", "-")); path = f"b/{bs}.html"
        ttl = f"{vt} – {a['name']} | Đọc miễn phí"
        body = (f'<h1>{E(vt)}</h1><p class="m">{E(title)} · {E(a["name"])}{f" · {yr}" if yr else ""}</p><p>{E(vi_d)}</p>{_en_p}'
                f'<p><a class="btn" href="/reader.html?id={bid}">Đọc ngay</a> <a class="btn s" href="/a/{k}.html">Xem thêm sách của {E(a["name"])}</a></p>'
                '<p class="m">Tác phẩm thuộc phạm vi công cộng. Nguồn: Christian Classics Ethereal Library (CCEL). Đọc trực tuyến, tải EPUB/PDF và nghe đọc thành tiếng trong thư viện.</p>')
        ld = {"@context": "https://schema.org", "@type": "Book", "name": title, "alternateName": vt, "author": {"@type": "Person", "name": a["name"]},
              "inLanguage": "en", "isAccessibleForFree": True, "description": vi_d, "url": f"{SITE}/{path}"}
        open(path, "w", encoding="utf-8").write(page(ttl, vi_d, path, body, ld)); urls.append(path); count_b += 1
        if _plain: PLAIN_B.append(path)
        a.setdefault("pages", {})[bid] = path

# author pages
for k, a in authors.items():
    items = []
    for bid, title, yr in a["ccel"][:80]:
        vt = vi.get(bid)
        link = ("https://ccel.org/ccel/" + bid) if bid in NR else "/" + a.get("pages", {}).get(bid, f"reader.html?id={bid}")
        lab = f"{E(vt)} <small>({E(title)})</small>" if vt and vt != title else E(title)
        d = f'<br><small>{E(desc[bid][1])}</small>' if bid in desc else ""
        items.append(f'<li><a href="{link}">{lab}</a>{f" <small>{yr}</small>" if yr else ""}{d}</li>')
    for r in a["ia"]:
        items.append(f'<li><a href="https://archive.org/details/{r[2]}" rel="noopener">{E(r[1])}</a> <small>{r[3] or ""}</small></li>')
    n = len(items)
    if n < 2: continue
    path = f"a/{k}.html"
    _sig = _auth_sig(k)
    intro = ((_sig + " ") if _sig else "") + f"Trang này tập hợp {n} tác phẩm của {a['name']} thuộc phạm vi công cộng: sách thần học, bài giảng, luận thuyết và tài liệu linh tu của truyền thống Cải Chánh và Thanh giáo. Tất cả đều có thể đọc trực tuyến, nghe đọc thành tiếng hoặc tải EPUB/PDF miễn phí trong thư viện Reformed Vietnam."
    body = f'<h1>{E(a["name"])} – sách miễn phí</h1><p>{E(intro)}</p><p><a class="btn" href="/?q={E(a["name"].split()[-1])}">Mở trong thư viện</a></p><ul>{"".join(items)}</ul>'
    ld = {"@context": "https://schema.org", "@type": "CollectionPage", "name": f"{a['name']} – sách miễn phí", "inLanguage": "vi", "url": f"{SITE}/{path}"}
    open(path, "w", encoding="utf-8").write(page(f"{a['name']} – sách miễn phí, đọc và tải | Reformed Vietnam", intro, path, body, ld)); urls.append(path); a["path"] = path

# redirect pages for merged/renamed author slugs (old bookmarks, search engines)
for _alias, _canon in AUTHOR_ALIASES.items():
    _ak, _ck = slug(_alias), slug(_canon)
    if _ak != _ck and _ck in authors and "path" in authors[_ck]:
        _cn = authors[_ck]["name"]
        open(f"a/{_ak}.html", "w", encoding="utf-8").write(
            '<!doctype html><html lang="vi"><head><meta charset="utf-8">\n'
            f'<title>{E(_cn)} – Reformed Vietnam</title>\n'
            f'<link rel="canonical" href="{SITE}/a/{_ck}.html">\n'
            f'<meta http-equiv="refresh" content="0; url=/a/{_ck}.html">\n'
            '<meta name="robots" content="noindex">\n'
            f'</head><body><p>Trang này đã chuyển đến <a href="/a/{_ck}.html">{E(_cn)}</a>.</p></body></html>\n')

# author index
lis = "".join(f'<li><a href="/{a["path"]}">{E(a["name"])}</a> <small>({len(a["ccel"]) + len(a["ia"])})</small></li>' for a in sorted(authors.values(), key=lambda x: x["name"]) if "path" in a)
open("tac-gia.html", "w", encoding="utf-8").write(page("Tác giả Cải Chánh và Thanh giáo – sách miễn phí | Reformed Vietnam",
    "Danh sách tác giả Cải Chánh, Thanh giáo và Trưởng Lão: Calvin, Owen, Spurgeon, Ryle, Bunyan và nhiều người khác, với sách đọc miễn phí.", "tac-gia.html",
    f"<h1>Tác giả Cải Chánh và Thanh giáo</h1><p>Chọn một tác giả để xem sách đọc hoặc tải miễn phí.</p><ul>{lis}</ul>"))

# Vietnamese hub: our own translations first, then partner sources
rv = [r for r in mg["vn"] if r["id"].startswith("rv-")]
vnb = [r for r in mg["vn"] if r.get("vnb")]
oth = [r for r in mg["vn"] if not r.get("au") and not r["id"].startswith("rv-") and not r.get("vnb")]
rvl = "".join(f'<li><a href="{E(r["url"])}">{E(r["vi"]["t"])}</a> <small>· {E(r["a"])} · AI, chưa duyệt · <a href="{E(r["epub"])}" download>EPUB</a></small></li>' for r in rv)
vnbl = "".join(f'<li><a href="{E(r["url"])}">{E(r["vi"]["t"])}</a> <small>· {E(r["a"])} · AI, chưa duyệt</small></li>' for r in vnb)
vn = "".join(f'<li><a href="{E(r["url"])}" rel="noopener">{E(r["vi"]["t"])}</a> <small>· {E(r["a"])}</small></li>' for r in oth)
rv_sec = (f"<h2>Bản dịch của Reformed Vietnam</h2><p>{len(rv)} tác phẩm cổ điển thuộc phạm vi công cộng, do Reformed Vietnam dịch sang tiếng Việt. Đọc ngay trên trang hoặc tải EPUB. Bản dịch sơ thảo, chưa hiệu đính.</p><ul>{rvl}</ul>") if rv else ""
vnb_sec = (f"<h2>Bản dịch sách tiếng Việt</h2><p>{len(vnb)} cuốn sách cổ điển thuộc phạm vi công cộng, do Reformed Vietnam dịch sang tiếng Việt. Đọc ngay trên trang hoặc trong trình đọc của thư viện. Bản dịch do AI hỗ trợ, chưa được mục sư duyệt giáo lý.</p><ul>{vnbl}</ul>") if vnb else ""
open("tieng-viet.html", "w", encoding="utf-8").write(page("Sách và bài viết tiếng Việt về thần học Cải Chánh | Reformed Vietnam",
    "Tuyển chọn sách, tín điều, giáo lý và bài viết thần học Cải Chánh bằng tiếng Việt, đọc miễn phí: bản dịch của Reformed Vietnam, Mục vụ Tiên Phong, 9Marks và các nguồn khác.", "tieng-viet.html",
    f"<h1>Sách và bài viết tiếng Việt</h1>{rv_sec}{vnb_sec}<h2>Từ các nguồn khác</h2><p>{len(oth)} tài liệu thần học Cải Chánh bằng tiếng Việt, mỗi tài liệu đều có liên kết về nguồn gốc. Xin cảm ơn Mục vụ Tiên Phong và 9Marks đã chia sẻ.</p><ul>{vn}</ul>"))
urls += [r["url"].lstrip("/") for r in rv]

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
    f"<h1>Sách nói và bài giảng miễn phí</h1><p>Đây là những nguồn nghe miễn phí mà thư viện giới thiệu. Trong thư viện, hãy chọn bộ lọc \"Có bản nghe\" để xem các sách có bản nghe. Trình đọc của chúng tôi cũng có thể đọc to bằng giọng đọc của thiết bị.</p><ul>{lis_a}</ul><p><a class=\"btn\" href=\"/?q=\">Mở thư viện</a></p>"))
urls.append("sach-noi.html")

exec(open('tools/plan.py', encoding='utf-8').read())
exec(open('tools/today.py', encoding='utf-8').read())
exec(open('tools/topics.py', encoding='utf-8').read())
exec(open('tools/courses.py', encoding='utf-8').read())
exec(open('tools/quotes.py', encoding='utf-8').read())
exec(open('tools/glossary.py', encoding='utf-8').read())
exec(open('tools/vn_context.py', encoding='utf-8').read())
exec(open('tools/subscribe_page.py', encoding='utf-8').read())
exec(open('tools/vi_books.py', encoding='utf-8').read())
exec(open('tools/articles.py', encoding='utf-8').read())

# shared home image; author pages without a bio share it instead of getting their own file
_h = og_image("", "Thư Viện Cơ Đốc & Thần Học Cải Chánh Tiếng Việt", "Sách Cải Chánh miễn phí: đọc, nghe, tải. Từng bước nhỏ, từ Phúc Âm đến một đời sống theo Chúa.")
os.replace(_h, "og.jpg")
for _fn in os.listdir("a"):
    _pp = f"a/{_fn}"; _t = open(_pp, encoding="utf-8").read()
    if 'class="bio"' in _t: continue
    _n = "og/" + re.sub(r"[^a-z0-9]+", "-", _pp.lower().replace(".html", "")).strip("-") + ".jpg"
    if os.path.exists(_n): os.remove(_n)
    open(_pp, "w", encoding="utf-8").write(_t.replace(f"{SITE}/{_n}", f"{SITE}/og.jpg"))
json.dump(sorted(u for u in urls if u.startswith(("b/", "ban-dich/")) and not u.endswith("index.html")), open("bp.json", "w"))
for _pp in PLAIN_B:  # books without a hand-written description share the home image
    _t = open(_pp, encoding="utf-8").read(); _n = "og/" + re.sub(r"[^a-z0-9]+", "-", _pp.lower().replace(".html", "")).strip("-") + ".jpg"
    if os.path.exists(_n): os.remove(_n)
    open(_pp, "w", encoding="utf-8").write(_t.replace(f"{SITE}/{_n}", f"{SITE}/og.jpg"))
# sitemap
# drop links to author pages that were not generated (authors with fewer than 2 items)
import glob as _g
for _f in _g.glob("b/*.html"):
    _t = open(_f, encoding="utf-8").read()
    _n = re.sub(r' ?<a class="btn s" href="/a/([^"]+\.html)">[^<]*</a>', lambda m: m.group(0) if os.path.exists("a/" + m.group(1)) else "", _t)
    if _n != _t: open(_f, "w", encoding="utf-8").write(_n)
print("pages:", len(urls), "book pages:", count_b, "author pages:", sum(1 for a in authors.values() if "path" in a))
exec(open('tools/moi_tin.py', encoding='utf-8').read())
exec(open('tools/pillars.py', encoding='utf-8').read())
exec(open('tools/authors_plus.py', encoding='utf-8').read())
exec(open('tools/book_info.py', encoding='utf-8').read())
exec(open('tools/sermon_pages.py', encoding='utf-8').read())
exec(open('tools/reformed101.py', encoding='utf-8').read())
exec(open('tools/static_txt.py', encoding='utf-8').read())
sm = "".join(f"<url><loc>{SITE}/{u}</loc></url>" for u in urls)
open("sitemap.xml", "w", encoding="utf-8").write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>\n')

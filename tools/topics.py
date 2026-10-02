# Executed from build-pages.py (uses: page, E, urls, books, mg). Builds chu-de/*.html topic hubs
import os, re
os.makedirs("chu-de", exist_ok=True)
_T = {}
for _a in books["authors"]:
    for _b in _a["books"]:
        _T[_a["id"] + "/" + _b[0]] = (_a["name"], _b[1])
_VI = books["vi"]
_PRI = ["calvin","luther","owen","edwards","spurgeon","bunyan","ryle","watson","bavinck","warfield","hodge","machen","packer","sproul","ames","flavel","sibbes","brooks","boston","bonar","charnock","goodwin","witsius","turretin","augustine","athanasius","kuyper","vos","murray","lloyd-jones"]
def _score(key, name):
    a = key.split("/")[0]
    return _PRI.index(a) if a in _PRI else 99
TOPICS = [
 ("an-dien-tin-lanh", "Ân điển và Tin Lành", "Tin Lành là gì, ân điển của Đức Chúa Trời, đức tin và sự ăn năn.", r"\bgrace\b|gospel|good news|faith|repent|saving|salvation|born again|regenerat|new birth", r"ân điển|tin lành|đức tin|ăn năn|cứu rỗi|tái sinh|tái sanh|cứu chuộc"),
 ("xung-cong-binh", "Xưng công bình bởi đức tin", "Giáo lý trung tâm của Cải Chánh: được kể là công chính chỉ nhờ ân điển.", r"justif|righteous|imputed|romans|galatians|bondage of the will|faith alone", r"xưng công bình|công chính|công bình|rô-ma|ga-la-ti"),
 ("nen-thanh", "Nên thánh và đời sống Cơ Đốc", "Lớn lên trong sự thánh khiết, chiến đấu với tội lỗi, học biết bằng lòng và vác thập tự giá.", r"holiness|sanctif|mortif|sin\b|temptation|contentment|christian life|self-denial|pilgrim|godliness|humility", r"nên thánh|thánh khiết|tội lỗi|bằng lòng|đời sống|môn đồ|khiêm nhường"),
 ("ba-ngoi", "Ba Ngôi và Đức Chúa Trời", "Bản tính, các thuộc tính và sự quan phòng của Đức Chúa Trời.", r"trinity|attributes|existence and attributes|nature of god|providence|knowledge of god|holiness of god|god's|names of god", r"ba ngôi|đức chúa trời|thuộc tính|quan phòng"),
 ("chua-christ", "Đấng Christ và sự chuộc tội", "Thân vị và công việc của Chúa Giê-xu: chuộc tội, thập tự giá, sự sống lại.", r"christ|jesus|atonement|cross|redemption|death of death|crucif|resurrection|mediator|saviour|savior|lamb", r"chúa jesus|đấng christ|chuộc tội|thập tự|sống lại|cứu chúa"),
 ("duc-thanh-linh", "Đức Thánh Linh", "Công việc của Đức Thánh Linh trong sự tái sinh, nên thánh và đời sống Hội Thánh.", r"holy spirit|holy ghost|the spirit|pneumat|comfort", r"thánh linh"),
 ("kinh-thanh", "Kinh Thánh", "Thẩm quyền, sự cảm thúc và cách đọc, giảng giải Kinh Thánh.", r"scripture|bible|word of god|inspiration|authority|inerran|canon|commentary|exposition|hermeneutic|preaching", r"kinh thánh|lời chúa|thẩm quyền|giảng giải|đọc kinh"),
 ("hoi-thanh", "Hội Thánh", "Hội Thánh là gì, dấu hiệu, kỷ luật, báp-têm, Tiệc Thánh và chức vụ.", r"church|ministry|pastor|baptism|lord's supper|sacrament|worship|elder|discipline|ecclesi", r"hội thánh|mục sư|báp-têm|tiệc thánh|thờ phượng|trưởng lão|chức vụ"),
 ("cau-nguyen", "Cầu nguyện và thờ phượng", "Học cầu nguyện và thờ phượng theo Kinh Thánh.", r"prayer|pray\b|lord's prayer|worship|psalm|devotion|communion with god|meditat", r"cầu nguyện|thờ phượng|thi thiên|suy gẫm"),
 ("giao-uoc", "Giao ước và Thần học Cải Chánh", "Thần học giao ước, các Tín điều và Giáo lý của truyền thống Cải Chánh.", r"covenant|confession|catechism|westminster|heidelberg|canons of dort|reformed|institutes|creed|synod|dort", r"giao ước|tín điều|giáo lý|westminster|heidelberg|cải chánh"),
 ("tien-dinh", "Tiền định và Chủ quyền của Đức Chúa Trời", "Sự chọn lựa, ý chí con người và chủ quyền Đức Chúa Trời.", r"predestin|election|sovereign|free will|bondage of the will|freedom of the will|decrees|arminian|calvinis|perseverance|eternal", r"tiền định|chọn lựa|chủ quyền|ý chí|calvin"),
 ("lich-su-cai-chanh", "Lịch sử Cải Chánh", "Luther, Calvin, Puritan và sử Hội Thánh.", r"reformation|luther|calvin|puritan|history|martyr|church history|knox|zwingli|latimer|huguenot|history of the", r"cải chánh|lịch sử|luther|calvin|thanh giáo|tử vì đạo"),
 ("muc-vu-giang-dao", "Chức vụ, giảng đạo và mục vụ", "Dành cho mục sư, người hầu việc Chúa và người dạy Kinh Thánh.", r"preach|pastor|minister|sermon|shepherd|lectures to my students|ministry|evangel|missions?|soul", r"giảng|mục sư|bài giảng|truyền giáo|chăn"),
]
_X = {x["id"]: x for x in books["extra"]}
_pages = []
for slug, name, intro, ren, rvi in TOPICS:
    rx, rv = re.compile(ren, re.I), re.compile(rvi, re.I)
    cc = []
    for key, (au, en) in _T.items():
        if key in NR: continue
        if rx.search(en) or rx.search(_VI.get(key, "")) or rv.search(_VI.get(key, "")):
            cc.append((_score(key, au), en, key, au))
    cc.sort(key=lambda t: (t[0], t[1]))
    cc = cc[:36]
    vv = []
    for x in mg["vn"]:
        t = x["vi"]["t"]
        if rv.search(t) or rv.search(x.get("a", "")) and False:
            vv.append((t, x["url"], x.get("a", "")))
    for x in books["extra"]:
        t = x["vi"]["t"]
        if rv.search(t) and x.get("url"):
            vv.append((t, x["url"], x.get("a", "")))
    vv = vv[:30]
    def li_c(c):
        _, en, key, au = c
        vt = _VI.get(key)
        t = f'{E(vt)} <small>({E(en)})</small>' if vt else E(en)
        return f'<li><a href="/reader.html?id={E(key)}"><b>{t}</b></a> <small>· {E(au)}</small></li>'
    body = f'''<p class="m"><a href="/chu-de/">← Tất cả chủ đề</a> · <a href="/lo-trinh.html">Lộ trình đọc</a></p>
<h1>{E(name)}</h1><p>{E(intro)}</p>
<div class="note"><b>Lưu ý:</b> danh sách này do máy lọc theo từ khóa, ưu tiên các tác giả Cải Chánh kinh điển, và chưa được mục sư thẩm định. Sách tiếng Anh có nút 🌐 để dịch máy sang tiếng Việt trong trình đọc (có thể còn sai sót).</div>
<h2>Sách tiếng Việt ({len(vv)})</h2>
<ul>{"".join(f'<li><a href="{E(u)}" target="_blank" rel="noopener"><b>{E(t)}</b></a> <small>· {E(a)}</small></li>' for t, u, a in vv) or "<li>Chưa có.</li>"}</ul>
<h2>Sách kinh điển miễn phí, đọc trong thư viện ({len(cc)})</h2>
<ul>{"".join(li_c(c) for c in cc)}</ul>'''
    p = f"chu-de/{slug}.html"
    open(p, "w", encoding="utf-8").write(page(f"{name} – sách Cải Chánh miễn phí | Reformed Vietnam", intro + " Sách miễn phí tiếng Việt và tiếng Anh.", p, body))
    urls.append(p); _pages.append((slug, name, intro, len(cc) + len(vv)))
body = '<h1>Học theo chủ đề</h1><p>Chọn một chủ đề để xem sách miễn phí liên quan.</p><ul>' + "".join(f'<li><a href="/chu-de/{s}.html"><b>{E(n)}</b></a> <small>· {k} sách</small><br>{E(i)}</li>' for s, n, i, k in _pages) + '</ul>'
open("chu-de/index.html", "w", encoding="utf-8").write(page("Học theo chủ đề | Reformed Vietnam", "Sách Cải Chánh miễn phí theo chủ đề: ân điển, xưng công bình, Ba Ngôi, Hội Thánh, cầu nguyện, tiền định và nhiều hơn.", "chu-de/index.html", body))
urls.append("chu-de/index.html")

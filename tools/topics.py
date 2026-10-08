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
 ("an-dien-tin-lanh", "Ân điển và Phúc Âm", "Phúc Âm là tin mừng về những gì Đức Chúa Trời đã làm để cứu tội nhân: ân điển nhưng không, đức tin nơi Đấng Christ, và sự ăn năn thật dẫn đến sự sống mới. Chuyên mục này tập hợp các sách Cải Chánh kinh điển giải thích rõ ràng Phúc Âm là gì, ân điển của Đức Chúa Trời vận hành thế nào, và làm sao một người được tái sinh. Đọc miễn phí bằng tiếng Việt và tiếng Anh, phù hợp cho người mới tin lẫn tín hữu lâu năm muốn nắm chắc nền tảng đức tin.", r"\bgrace\b|gospel|good news|faith|repent|saving|salvation|born again|regenerat|new birth", r"ân điển|tin lành|phúc âm|đức tin|ăn năn|cứu rỗi|tái sinh|tái sanh|cứu chuộc"),
 ("xung-cong-binh", "Xưng công bình bởi đức tin", "Được kể là công chính trước mặt Đức Chúa Trời chỉ bởi ân điển, chỉ qua đức tin nơi Đấng Christ — đây là giáo lý trung tâm của cuộc Cải Chánh và của toàn bộ Kinh Thánh. Các sách trong chuyên mục này trình bày sự xưng công chính là gì, sự quy gán công chính của Đấng Christ nghĩa ra sao, và vì sao không ai được cứu bởi việc làm. Tài liệu quý cho người muốn hiểu sâu Rô-ma, Ga-la-ti và nền tảng của sự bảo đảm cứu rỗi.", r"justif|righteous|imputed|romans|galatians|bondage of the will|faith alone", r"xưng công bình|công chính|công bình|rô-ma|ga-la-ti"),
 ("nen-thanh", "Nên thánh và đời sống Cơ Đốc", "Được cứu bởi ân điển không có nghĩa sống buông thả: tín hữu được kêu gọi lớn lên trong sự thánh khiết, giết chết tội lỗi mỗi ngày và vác thập tự giá theo Chúa. Chuyên mục này gồm các tác phẩm Thanh giáo và Cải Chánh về sự nên thánh, chiến đấu với cám dỗ, học biết bằng lòng trong mọi hoàn cảnh và sống khiêm nhường. Đọc miễn phí, thích hợp cho đời sống linh tu hằng ngày.", r"holiness|sanctif|mortif|sin\b|temptation|contentment|christian life|self-denial|pilgrim|godliness|humility", r"nên thánh|thánh khiết|tội lỗi|bằng lòng|đời sống|môn đồ|khiêm nhường"),
 ("ba-ngoi", "Ba Ngôi và Đức Chúa Trời", "Đức Chúa Trời là ai? Ba Ngôi nghĩa là gì, các thuộc tính của Ngài ra sao, và sự quan phòng của Ngài vận hành thế nào trong thế gian? Chuyên mục này tập hợp các luận thuyết kinh điển về bản tính Đức Chúa Trời, thần học về sự thánh khiết, tình yêu, công chính và chủ quyền của Ngài. Nền tảng không thể thiếu cho mọi tín hữu muốn biết Chúa sâu nhiệm hơn.", r"trinity|attributes|existence and attributes|nature of god|providence|knowledge of god|holiness of god|god's|names of god", r"ba ngôi|đức chúa trời|thuộc tính|quan phòng"),
 ("chua-christ", "Đấng Christ và sự chuộc tội", "Chúa Giê-xu Christ là ai và Ngài đã làm gì để cứu chúng ta? Chuyên mục này trình bày thân vị và công việc của Đấng Christ: sự chuộc tội trên thập tự giá, sự sống lại, chức vụ Trung Bảo và vinh hiển của Ngài. Các sách của Owen, Flavel, Spurgeon và nhiều tác giả Cải Chánh khác giúp độc giả chiêm ngưỡng Đấng Christ trọn vẹn hơn. Đọc miễn phí bằng tiếng Việt và tiếng Anh.", r"christ|jesus|atonement|cross|redemption|death of death|crucif|resurrection|mediator|saviour|savior|lamb", r"chúa jesus|đấng christ|chuộc tội|thập tự|sống lại|cứu chúa"),
 ("duc-thanh-linh", "Đức Thánh Linh", "Đức Thánh Linh làm gì trong đời sống tín hữu? Chuyên mục này gồm các sách về công việc của Đức Thánh Linh trong sự tái sinh, sự nên thánh, sự cầu nguyện và đời sống Hội Thánh. Từ luận thuyết kinh điển của Kuyper, Owen đến các bài linh tu ngắn, đây là nguồn tài liệu quý để hiểu đúng về Ngôi Ba và kinh nghiệm quyền năng Ngài mỗi ngày.", r"holy spirit|holy ghost|the spirit|pneumat|comfort", r"thánh linh"),
 ("kinh-thanh", "Kinh Thánh", "Kinh Thánh có thẩm quyền tuyệt đối vì là Lời Đức Chúa Trời được linh cảm, không hề sai lầm. Chuyên mục này tập hợp sách về sự cảm thúc và thẩm quyền của Kinh Thánh, chính điển, cùng phương pháp đọc, học và giảng giải Kinh Thánh đúng đắn. Thích hợp cho người muốn đào sâu Lời Chúa, chuẩn bị bài giảng hoặc dạy Kinh Thánh trong nhóm nhỏ và gia đình.", r"scripture|bible|word of god|inspiration|authority|inerran|canon|commentary|exposition|hermeneutic|preaching", r"kinh thánh|lời chúa|thẩm quyền|giảng giải|đọc kinh"),
 ("hoi-thanh", "Hội Thánh", "Hội Thánh là gì, dấu hiệu của một Hội Thánh thật ra sao, và đời sống trong Hội Thánh nên thế nào? Chuyên mục này gồm sách về bản chất Hội Thánh, kỷ luật, báp-têm, Tiệc Thánh, sự thờ phượng và chức vụ trưởng lão, mục sư. Tài liệu cần thiết cho mọi tín hữu muốn gắn bó đúng đắn với Hội Thánh địa phương và phục vụ trong nhà Chúa.", r"church|ministry|pastor|baptism|lord's supper|sacrament|worship|elder|discipline|ecclesi", r"hội thánh|mục sư|báp-têm|tiệc thánh|thờ phượng|trưởng lão|chức vụ"),
 ("cau-nguyen", "Cầu nguyện và thờ phượng", "Cầu nguyện là hơi thở của đời sống Cơ Đốc, và thờ phượng là mục đích tối cao của con người. Chuyên mục này hướng dẫn cầu nguyện theo Kinh Thánh — từ Kinh Lạy Cha đến đời sống cầu nguyện riêng tư — cùng nguyên tắc thờ phượng đẹp lòng Đức Chúa Trời. Gồm các tác phẩm kinh điển của Knox, Watson, Bunyan và nhiều tác giả Thanh giáo khác.", r"prayer|pray\b|lord's prayer|worship|psalm|devotion|communion with god|meditat", r"cầu nguyện|thờ phượng|thi thiên|suy gẫm"),
 ("giao-uoc", "Giao ước và Thần học Cải Chánh", "Thần học giao ước là khung xương sống của tư tưởng Cải Chánh: Đức Chúa Trời hành động trong lịch sử qua các giao ước ân điển. Chuyên mục này gồm sách về thần học giao ước, các Tín điều và Giáo lý vấn đáp (Westminster, Heidelberg), cùng những luận thuyết nền tảng của truyền thống Cải Chánh. Dành cho người muốn nắm vững hệ thống giáo lý một cách có thứ tự.", r"covenant|confession|catechism|westminster|heidelberg|canons of dort|reformed|institutes|creed|synod|dort", r"giao ước|tín điều|giáo lý|westminster|heidelberg|cải chánh"),
 ("tien-dinh", "Tiền định và Chủ quyền của Đức Chúa Trời", "Đức Chúa Trời có chủ quyền tuyệt đối trên mọi sự, kể cả sự cứu rỗi: Ngài chọn lựa ai được cứu theo ý muốn tốt lành của Ngài. Chuyên mục này trình bày giáo lý tiền định, sự tuyển chọn, mối quan hệ giữa chủ quyền Chúa và trách nhiệm con người, cùng cuộc tranh luận với thuyết Arminius. Các tác phẩm của Calvin, Edwards, Boettner và Owen giúp độc giả hiểu đúng ân điển chủ quyền.", r"predestin|election|sovereign|free will|bondage of the will|freedom of the will|decrees|arminian|calvinis|perseverance|eternal", r"tiền định|chọn lựa|chủ quyền|ý chí|calvin"),
 ("lich-su-cai-chanh", "Lịch sử Cải Chánh", "Cuộc Cải Chánh thế kỷ 16 là một trong những bước ngoặt lớn nhất của lịch sử Hội Thánh: Luther, Calvin, Knox và các nhà Thanh giáo đã đứng lên vì Phúc Âm. Chuyên mục này gồm sách lịch sử Hội Thánh, tiểu sử các nhà cải chánh và chứng đạo sử, giúp độc giả hiểu gốc gác đức tin mình và noi gương trung tín của các thánh đồ xưa.", r"reformation|luther|calvin|puritan|history|martyr|church history|knox|zwingli|latimer|huguenot|history of the", r"cải chánh|lịch sử|luther|calvin|thanh giáo|tử vì đạo"),
 ("muc-vu-giang-dao", "Chức vụ, giảng đạo và mục vụ", "Được Chúa kêu gọi hầu việc Ngài là đặc ân lớn, cũng là trách nhiệm nặng: rao giảng Lời Chúa cách trung thực và chăn dắt bầy chiên bằng tình yêu thương. Chuyên mục này dành cho mục sư, người giảng dạy Kinh Thánh, trưởng nhóm nhỏ và mọi tín hữu muốn phục vụ: nghệ thuật giảng đạo, chăm sóc linh hồn, truyền giáo và đời sống gương mẫu của người hầu việc Chúa.", r"preach|pastor|minister|sermon|shepherd|lectures to my students|ministry|evangel|missions?|soul", r"giảng|mục sư|bài giảng|truyền giáo|chăn"),
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

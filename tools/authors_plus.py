# Executed from build-pages.py AFTER author pages exist. Adds short profiles to author pages and builds bai-giang.html (sermon compilation).
# Draft: AI-assisted, not pastor-reviewed. Only hosted works are public-domain or our own AI translations.
import os as _os
_AB = [  # slugs, name, years, tradition, bio, works, hosted vn slugs
 (["john-calvin","jean-calvin"], "John Calvin", "1509–1564", "Cải cách Thụy Sĩ (Geneva)", "Nhà cải cách người Pháp, mục sư và giảng sư ở Geneva. Ông có ảnh hưởng lớn nhất đến truyền thống Cải Chánh qua việc giảng dạy Kinh Thánh từng sách một và hệ thống hóa giáo lý.", ["Institutes of the Christian Religion (Cơ Đốc Giáo Cương Yếu)", "Các bài chú giải Kinh Thánh"], ["calvin-prayer", "calvin-chr-life"]),
 (["c-h-spurgeon"], "Charles H. Spurgeon", "1834–1892", "Báp-tít Cải Chánh (Particular Baptist)", "Mục sư Báp-tít người Anh, giảng đạo tại Metropolitan Tabernacle ở London. Ông được gọi là “Hoàng tử của các nhà giảng đạo”, nổi tiếng với bài giảng giản dị, nhiều hình ảnh, tập trung vào Phúc Âm.", ["Hàng ngàn bài giảng (Metropolitan Tabernacle Pulpit)", "Morning and Evening", "Lectures to My Students"], ["spurgeon-loi-benh-vuc-thuyet-calvin", "spurgeon-y-chi-tu-do-mot-ke-no-le", "compel-them-to-come-in", "spurgeon-puritan-catechism"]),
 (["john-owen","1616-1683-owen-john"], "John Owen", "1616–1683", "Thanh giáo Anh (Hội Chúng)", "Nhà thần học Thanh giáo, mục sư và từng là phó viện trưởng Đại học Oxford. Các tác phẩm của ông sâu và dày, bàn về tội lỗi, Thánh Linh, sự cứu chuộc và sự hiệp thông với Đức Chúa Trời.", ["The Mortification of Sin", "Communion with God", "The Death of Death in the Death of Christ", "Chú giải thư Hê-bơ-rơ"], ["owen-catechisms"]),
 (["jonathan-edwards"], "Jonathan Edwards", "1703–1758", "Cải Chánh Mỹ (Hội Chúng)", "Mục sư và nhà thần học Mỹ, một nhân vật chính của cuộc Phục hưng lớn (Great Awakening). Ông kết hợp tư duy sâu sắc với lòng yêu mến Đức Chúa Trời.", ["Sinners in the Hands of an Angry God (1741)", "Religious Affections", "The Freedom of the Will", "Resolutions"], ["edwards-toi-nhan-trong-tay-duc-chua-troi-thanh-no", "edwards-bay-muoi-quyet-tam"]),
 (["john-bunyan","1628-1688-bunyan-john"], "John Bunyan", "1628–1688", "Báp-tít Anh", "Thợ hàn nồi và nhà giảng đạo người Anh, từng bị bỏ tù vì giảng đạo không có phép. Ông viết sách bằng ngôn ngữ giản dị của người bình dân.", ["The Pilgrim’s Progress (1678, Thiên Lộ Lịch Trình)", "Grace Abounding to the Chief of Sinners"], []),
 (["j-c-ryle"], "J. C. Ryle", "1816–1900", "Anh giáo Tin Lành", "Giám mục Anh giáo đầu tiên của Liverpool. Ông viết ngắn gọn, thẳng thắn và dễ đọc về đời sống Cơ Đốc và sự thánh khiết.", ["Holiness", "Expository Thoughts on the Gospels", "Bạn có cầu nguyện không? (bài viết ngắn)"], ["do-you-pray"]),
 (["thomas-watson"], "Thomas Watson", "khoảng 1620–1686", "Thanh giáo Anh (Trưởng Lão)", "Mục sư Thanh giáo ở London, nổi tiếng với lối viết ngắn gọn, nhiều hình ảnh và áp dụng thực tế.", ["A Body of Divinity", "The Godly Man’s Picture", "The Art of Divine Contentment"], []),
 (["richard-sibbes"], "Richard Sibbes", "1577–1635", "Thanh giáo Anh", "Giảng sư ở Cambridge và Gray’s Inn. Ông được biết đến với giọng văn dịu dàng khi nói về lòng thương xót của Đấng Christ đối với người yếu đuối.", ["The Bruised Reed (Cây Sậy Bị Bầm Giập)", "The Soul’s Conflict"], []),
 (["george-whitefield"], "George Whitefield", "1714–1770", "Anh giáo, Giám Lý theo Calvin", "Nhà giảng đạo lưu động người Anh, một trong những giảng sư có sức ảnh hưởng nhất của cuộc Phục hưng lớn ở Anh và Mỹ.", ["Các bài giảng, trong đó có The Method of Grace"], ["whitefield-con-duong-cua-an-dien"]),
 (["john-newton"], "John Newton", "1725–1807", "Anh giáo Tin Lành", "Từng là thuyền trưởng tàu buôn nô lệ, sau được Chúa cứu và trở thành mục sư, tác giả bài thánh ca “Amazing Grace”. Thư từ và bài giảng của ông ấm áp và thực tế.", ["Olney Hymns", "Letters of John Newton", "Cây non, bông lúa, hột chắc"], ["newton-cay-non-bong-lua-hot-chac"]),
 (["robert-m-cheyne"], "Robert Murray M’Cheyne", "1813–1843", "Giáo hội Scotland (Trưởng Lão)", "Mục sư trẻ ở Dundee, mất năm 29 tuổi. Lòng sốt sắng, sự cầu nguyện và kế hoạch đọc Kinh Thánh trong một năm của ông vẫn được nhiều người dùng.", ["Bible Reading Calendar", "Memoir and Remains"], ["mccheyne-banh-hang-ngay", "mccheyne-cac-con-hay-chay-den-cung-dang-christ"]),
 (["horatius-bonar"], "Horatius Bonar", "1808–1889", "Giáo hội Tự do Scotland", "Mục sư và tác giả nhiều bài thánh ca, nổi tiếng với các sách bàn về sự thánh khiết và ân điển.", ["God’s Way of Peace", "Words to Winners of Souls"], []),
 (["john-knox"], "John Knox", "khoảng 1514–1572", "Cải cách Scotland (Trưởng Lão)", "Nhà cải cách chính của Scotland, học trò của Calvin ở Geneva, người đặt nền cho Hội Thánh Trưởng Lão Scotland.", ["The First Book of Discipline", "History of the Reformation in Scotland"], []),
 (["b-b-warfield","benjamin-warfield"], "B. B. Warfield", "1851–1921", "Trưởng Lão (Princeton)", "Giáo sư thần học ở Princeton, nổi tiếng với các bài viết bảo vệ thẩm quyền và sự đáng tin cậy của Kinh Thánh.", ["The Inspiration and Authority of the Bible", "Biblical and Theological Studies"], []),
 (["herman-bavinck"], "Herman Bavinck", "1854–1921", "Cải Chánh Hà Lan", "Nhà thần học Hà Lan, tác giả bộ thần học hệ thống Reformed Dogmatics, được xem là một đỉnh cao của thần học Cải Chánh hiện đại.", ["Reformed Dogmatics", "The Philosophy of Revelation"], []),
 (["martin-luther"], "Martin Luther", "1483–1546", "Cải cách Đức (Lutheran)", "Tu sĩ và giáo sư người Đức, người khởi đầu cuộc Cải cách năm 1517. Ông nhấn mạnh sự xưng công bình bởi đức tin và thẩm quyền của Kinh Thánh. Ông thuộc truyền thống Lutheran, không phải Cải Chánh theo nghĩa hẹp.", ["Ninety-five Theses", "The Bondage of the Will", "Small Catechism"], []),
 (["richard-baxter"], "Richard Baxter", "1615–1691", "Thanh giáo Anh (không theo quốc giáo)", "Mục sư ở Kidderminster, nổi tiếng với việc chăm sóc mục vụ cá nhân từng gia đình.", ["The Reformed Pastor", "The Saints’ Everlasting Rest"], []),
 (["thomas-brooks"], "Thomas Brooks", "1608–1680", "Thanh giáo Anh", "Mục sư Thanh giáo, nổi tiếng với những hình ảnh sinh động và lời khuyên thực tế chống lại cám dỗ.", ["Precious Remedies Against Satan’s Devices"], []),
 (["john-flavel"], "John Flavel", "khoảng 1627–1691", "Thanh giáo Anh (Trưởng Lão)", "Mục sư ở Dartmouth, viết về sự quan phòng của Đức Chúa Trời và đời sống thuộc linh với giọng ấm áp.", ["The Mystery of Providence", "The Fountain of Life"], []),
 (["matthew-henry"], "Matthew Henry", "1662–1714", "Trưởng Lão Anh", "Mục sư và tác giả bộ chú giải Kinh Thánh nổi tiếng, được đọc suốt nhiều thế kỷ vì lối áp dụng thực tế.", ["Exposition of the Old and New Testaments"], []),
 (["thomas-boston"], "Thomas Boston", "1676–1732", "Giáo hội Scotland (Trưởng Lão)", "Mục sư vùng quê Scotland, viết sách thần học dễ hiểu cho người bình dân.", ["Human Nature in Its Fourfold State"], []),
 (["stephen-charnock"], "Stephen Charnock", "1628–1680", "Thanh giáo Anh", "Mục sư Thanh giáo, nổi tiếng với những bài giảng sâu về bản tính và các thuộc tính của Đức Chúa Trời.", ["The Existence and Attributes of God"], []),
 (["charles-hodge"], "Charles Hodge", "1797–1878", "Trưởng Lão (Princeton)", "Giáo sư thần học ở Princeton nhiều thập kỷ, tác giả bộ Systematic Theology được dùng rộng rãi.", ["Systematic Theology", "Chú giải thư Rô-ma"], []),
 (["abraham-kuyper"], "Abraham Kuyper", "1837–1920", "Cải Chánh Hà Lan", "Mục sư, chính trị gia và thủ tướng Hà Lan; ông dạy rằng quyền làm Chúa của Đấng Christ bao trùm mọi lãnh vực đời sống.", ["Lectures on Calvinism", "To Be Near Unto God"], []),
 (["charles-bridges"], "Charles Bridges", "1794–1869", "Anh giáo Tin Lành", "Mục sư Anh giáo, tác giả các bài giải nghĩa Châm-ngôn và Thi-thiên 119 và bàn về chức vụ mục sư.", ["The Christian Ministry", "An Exposition of Proverbs"], []),
 (["arthur-pink"], "Arthur W. Pink", "1886–1952", "Cải Chánh (độc lập)", "Giáo sư Kinh Thánh người Anh, viết nhiều về chủ quyền của Đức Chúa Trời.", ["The Sovereignty of God", "The Attributes of God"], []),
 (["heinrich-bullinger"], "Heinrich Bullinger", "1504–1575", "Cải cách Thụy Sĩ (Zürich)", "Người kế vị Zwingli ở Zürich; ông viết Tuyên Xưng Đức Tin Helvetic thứ hai, có ảnh hưởng ở nhiều Hội Thánh Cải Chánh.", ["The Decades", "Second Helvetic Confession"], []),
 (["thomas-goodwin"], "Thomas Goodwin", "1600–1680", "Thanh giáo Anh (Hội Chúng)", "Nhà thần học Thanh giáo, thành viên Hội đồng Westminster, viết về lòng của Đấng Christ đối với tội nhân.", ["The Heart of Christ in Heaven", "Christ Set Forth"], []),
 (["john-gill"], "John Gill", "1697–1771", "Báp-tít Cải Chánh", "Mục sư Báp-tít ở London, tác giả bộ chú giải Kinh Thánh đồ sộ và bộ thần học hệ thống.", ["Exposition of the Entire Bible", "Body of Doctrinal Divinity"], []),
]
import json as _json
for _s, _d in _json.load(open("tools/author_bios_more.json", encoding="utf-8")).items():
    if not any(_s in x[0] for x in _AB):
        _AB.append(([_s], _d["name"], _d.get("years", ""), _d.get("tradition", ""), _d["bio"], _d.get("works", []), []))
_VT = {}
for _f in _os.listdir("txt"):
    if _f.endswith(".txt"):
        _L = [l.strip() for l in open("txt/" + _f, encoding="utf-8").read().split("\n", 6)[:5] if l.strip()]
        _VT[_f[:-4]] = (_L[0].title() if _L else _f, len(open("txt/" + _f, encoding="utf-8").read()))
def _min(s): return max(1, round(_VT[s][1] / 1100))
_apage = '<style>.bio{margin:12px 0 18px;padding:14px 16px;border-radius:10px;background:#8881}.bio p{margin:.3em 0}.bio dl{display:grid;grid-template-columns:auto 1fr;gap:4px 12px;margin:.6em 0;font-size:.92rem}.bio dt{opacity:.7}.bio dd{margin:0}.bio ul{margin:.3em 0 .3em 1.2em;padding:0}</style>'
for _sl, _nm, _yr, _tr, _bio, _wk, _vn in _AB:
    _dl = (f'<dt>Sống</dt><dd>{E(_yr)}</dd>' if _yr else '') + (f'<dt>Truyền thống</dt><dd>{E(_tr)}</dd>' if _tr else '') + (f'<dt>Tác phẩm tiêu biểu</dt><dd>{E("; ".join(_wk))}</dd>' if _wk else '')
    _blk = (f'<div class="bio"><p>{E(_bio)}</p><dl>{_dl}</dl>'
            + ('<p><b>Đọc tiếng Việt ngay:</b></p><ul>' + "".join(f'<li><a href="/reader.html?id=vn/{s}">{E(_VT[s][0])}</a> (khoảng {_min(s)} phút, bản dịch AI chưa duyệt)</li>' for s in _vn if s in _VT) + '</ul>' if _vn else '')
            + '<p><small>Tiểu sử tóm tắt do AI soạn, chưa được mục sư duyệt. Hãy đối chiếu với nguồn lịch sử đáng tin cậy.</small></p></div>')
    for _s in _sl:
        _p = f"a/{_s}.html"
        if not _os.path.exists(_p): continue
        _t = open(_p, encoding="utf-8").read()
        if 'class="bio"' in _t: continue
        _t = _t.replace("</h1>", "</h1>" + _apage + _blk, 1)
        open(_p, "w", encoding="utf-8").write(_t)
# sermon compilation
_SG = [
 ("Lời kêu gọi đến với Chúa", [
   ("compel-them-to-come-in", "Charles Spurgeon", "Lời kêu gọi tha thiết dành cho người chưa tin, dựa trên dụ ngôn tiệc lớn (Lu-ca 14)."),
   ("whitefield-con-duong-cua-an-dien", "George Whitefield, 1741", "Bài giảng từ Giê-rê-mi 8:11, cảnh báo về sự bình an giả và nói về cách Đức Chúa Trời đem tội nhân đến với Đấng Christ."),
   ("mccheyne-cac-con-hay-chay-den-cung-dang-christ", "Robert Murray M’Cheyne, 1840", "Những lý do trẻ em nên đến với Đấng Christ ngay, không trì hoãn.")]),
 ("Ân điển và chủ quyền của Đức Chúa Trời", [
   ("spurgeon-y-chi-tu-do-mot-ke-no-le", "Charles Spurgeon, 1855", "Spurgeon nói về sự nô lệ của ý chí con người khi chưa được ân điển giải cứu."),
   ("spurgeon-loi-benh-vuc-thuyet-calvin", "Charles Spurgeon, 1861", "Spurgeon giải thích vì sao ông tin các giáo lý ân điển của Calvin, và gọi đó là Phúc Âm."),
   ("edwards-toi-nhan-trong-tay-duc-chua-troi-thanh-no", "Jonathan Edwards, 1741", "Bài giảng nổi tiếng về sự nghiêm trọng của tội lỗi và sự nhịn nhục của Đức Chúa Trời.")]),
 ("Đời sống đức tin hằng ngày", [
   ("chalmers-quyen-nang-cua-mot-tinh-yeu-moi", "Thomas Chalmers, 1819", "Lòng yêu mến thế gian chỉ được thay thế khi có một tình yêu mới, tình yêu dành cho Chúa."),
   ("newton-cay-non-bong-lua-hot-chac", "John Newton, 1772", "Ba giai đoạn tăng trưởng của đời sống thuộc linh, từ Mác 4:28."),
   ("do-you-pray", "J. C. Ryle", "Bảy lý do vì sao sự cầu nguyện riêng tư rất quan trọng."),
   ("edwards-bay-muoi-quyet-tam", "Jonathan Edwards, 1723", "Bảy mươi quyết tâm của Edwards khi còn trẻ, để sống cho vinh hiển Chúa."),
   ("mccheyne-banh-hang-ngay", "Robert Murray M’Cheyne, 1842", "Lịch đọc Kinh Thánh cả năm để đi hết Kinh Thánh.")]),
]
_bg = "".join(f'<h2>{E(g)}</h2>' + "".join(f'<div class="sm"><h3><a href="/reader.html?id=vn/{s}">{E(_VT[s][0])}</a></h3><p class="m"><small>{E(a)} · khoảng {_min(s)} phút đọc</small></p><p>{E(d)}</p></div>' for s, a, d in L if s in _VT) for g, L in _SG)
_bgp = ('<style>.sm{margin:12px 0;padding:10px 14px;border-left:3px solid var(--acc);background:#8881;border-radius:6px}.sm h3{margin:0 0 .2em;font-size:1.05rem}.sm p{margin:.2em 0}.dr{padding:.6em .9em;border-radius:8px;background:#d9a20022;font-size:.9rem}</style>'
        '<h1>Tuyển tập bài giảng</h1><p class="dr">Các bài giảng dưới đây thuộc phạm vi công cộng. Bản tiếng Việt do AI hỗ trợ dịch và chưa được mục sư duyệt. Hãy đọc với tinh thần Bê-rê và đối chiếu Kinh Thánh.</p>'
        '<p>Mỗi bài đọc được trong khoảng 10 đến 60 phút. Hãy bắt đầu với bài đầu tiên của nhóm bạn quan tâm.</p>' + _bg
        + '<h2>Nghe thêm bài giảng</h2><p>Thư viện chưa lưu bài giảng của người khác để tôn trọng bản quyền. Các nguồn nghe bài giảng miễn phí được giới thiệu ở trang <a href="/sach-noi.html">Sách nói và bài giảng</a>.</p>')
open("bai-giang.html", "w", encoding="utf-8").write(page("Tuyển tập bài giảng Cải Chánh tiếng Việt: Spurgeon, Edwards, Whitefield | Reformed Vietnam", "Bài giảng Cải Chánh thuộc phạm vi công cộng bằng tiếng Việt, chia theo chủ đề: lời kêu gọi đến với Chúa, ân điển và chủ quyền của Đức Chúa Trời, đời sống đức tin.", "bai-giang.html", _bgp))
urls.append("bai-giang.html")

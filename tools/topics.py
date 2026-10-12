# Executed from build-pages.py (uses: page, E, urls, books, mg). Builds chu-de/*.html topic hubs
import os, re, json
os.makedirs("chu-de", exist_ok=True)
_T = {}
for _a in books["authors"]:
    for _b in _a["books"]:
        _T[_a["id"] + "/" + _b[0]] = (_a["name"], _b[1])
_VI = books["vi"]
_TRI = json.load(open("translations/index.json", encoding="utf-8"))
_TR = []
for x in _TRI:
    _f = "translations/" + x["file"]
    if x.get("hold") or not os.path.exists(_f):
        continue  # same skip rule as tools/vi_books.py: no txt -> no ban-dich page
    _TR.append((x.get("author", "?"), x.get("title", ""), x.get("orig", ""), os.path.splitext(x["file"])[0]))
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
 ("an-nan", "Sự ăn năn và sự trở lại", "Ăn năn không chỉ là hối tiếc mà là quay hẳn khỏi tội lỗi để trở về cùng Đức Chúa Trời — dấu hiệu không thể thiếu của sự cứu rỗi thật. Chuyên mục này cũng dành cho những ai đã sa ngã, bội đạo: lời kêu gọi trở lại cùng Chúa nhân từ, Đấng vui mừng đón kẻ hoang đàng quay về.", r"repent|peniten|contrit|broken heart|godly sorrow|backslid|apostas|returning|prodigal", r"ăn năn|hối cải|thống hối|bội đạo|lui đi|sa ngã|trở lại|hoang đàng"),
 ("tai-sinh", "Sự tái sinh", "Không ai thấy được Nước Đức Chúa Trời nếu không được sinh lại bởi Đức Thánh Linh. Chuyên mục này trình bày giáo lý tái sinh: bản chất con người sa ngã cần được dựng nên mới, công việc chủ quyền của Thánh Linh trong sự tái sinh, và những dấu hiệu của một đời sống đã được sinh lại.", r"regenerat|new birth|born again|effectual calling|quickening|new creature|second birth", r"tái sinh|tái sanh|sinh lại|người mới|được dựng nên mới"),
 ("bao-dam-cuu-roi", "Sự bảo đảm cứu rỗi", "Làm sao biết chắc mình đã được cứu? Chuyên mục này gồm các sách giúp tín hữu có sự bảo đảm vững chắc về sự cứu rỗi — không dựa vào cảm xúc mà dựa vào lời hứa của Đức Chúa Trời, công việc của Đấng Christ, những bằng chứng ân điển trong đời sống và sự bền đỗ đến cuối cùng.", r"assurance|security of|perseverance|confidence|full assurance|infallible|eternal security", r"bảo đảm|chắc chắn|vững chắc|kiên trì|bền đỗ|bình an thuộc linh"),
 ("thien-dang-dia-nguc", "Thiên đàng và địa ngục", "Chết rồi đi đâu? Chuyên mục này trình bày những gì Kinh Thánh dạy về sự chết, thiên đàng, địa ngục và sự phán xét cuối cùng — khích lệ tín hữu sống với viễn cảnh đời đời và cảnh tỉnh những ai còn sống trong tội lỗi.", r"heaven|hell|eternal punishment|everlasting|life after death|glory to come|judgment day|day of judgment|second death|lake of fire", r"thiên đàng|địa ngục|đời đời|sự chết|phán xét|sự sống đời đời"),
 ("chiu-kho", "Sự chịu khổ", "Tại sao người công chính phải chịu khổ? Chuyên mục này gồm các sách an ủi những ai đang trong hoạn nạn: mục đích của sự chịu khổ trong chương trình của Đức Chúa Trời, cách chịu khổ như người Cơ Đốc, và niềm hy vọng vượt trên mọi đau đớn đời này.", r"suffer|afflict|tribulation|trial|adversity|chastisement|comfort in|grief|sorrow|burden|crook in the lot", r"chịu khổ|hoạn nạn|đau khổ|thử thách|an ủi|gian truân|nét cong|chỗ cong"),
 ("chien-tran-thuoc-linh", "Chiến trận thuộc linh", "Đời sống Cơ Đốc là một trận chiến: chống lại xác thịt, thế gian và ma quỷ. Chuyên mục này tập hợp các tác phẩm Thanh giáo kinh điển về chiến trận thuộc linh — nhận diện kẻ thù, mặc lấy áo giáp của Đức Chúa Trời và đứng vững trong Đấng Christ.", r"spiritual warfare|warfare|armor of god|whole armor|satan|devil|demon|principalit|wiles of|spiritual combat|holy war", r"chiến trận|ma quỷ|sa-tan|áo giáp|mưu kế"),
 ("hon-nhan-gia-dinh", "Hôn nhân và gia đình", "Hôn nhân là giao ước thánh do Đức Chúa Trời lập nên, và gia đình là hội thánh đầu tiên của con cái Ngài. Chuyên mục này gồm sách về hôn nhân Cơ Đốc, bổn phận vợ chồng, nuôi dạy con cái trong đường lối Chúa và xây dựng gia đình tin kính.", r"marriage|family|husband|wife|parenting|children|household|domestic|wedlock|nurture|family worship", r"hôn nhân|gia đình|vợ chồng|con cái|nuôi dạy|cha mẹ"),
 ("truyen-giao", "Truyền giáo và chứng đạo", "Phúc Âm phải được rao ra cho muôn dân. Chuyên mục này tập hợp sách về truyền giáo, chứng đạo cá nhân, công việc cứu linh hồn và tấm lòng của Đức Chúa Trời đối với người hư mất — khích lệ mọi tín hữu tham gia vào đại mạng lệnh.", r"evangelis|missions?|soul.?winning|witness|great commission|lost|perishing|compassion for|missionary", r"truyền giáo|chứng đạo|cứu linh hồn|người hư mất|đại mạng lệnh|sứ mạng|rao giảng"),
 ("tha-thu", "Sự tha thứ", "Được Chúa tha thứ mọi tội lỗi, tín hữu cũng được kêu gọi tha thứ cho người khác. Chuyên mục này trình bày sự tha thứ của Đức Chúa Trời trong Đấng Christ và bổn phận tha thứ, hòa giải với anh em — chữa lành những mối quan hệ đổ vỡ.", r"forgiv|pardon|remission|reconciliation|seventy times seven|forgiving one another", r"tha thứ|hòa giải|khoan dung|nhân nhượng|làm hòa"),
 ("vui-mung-binh-an", "Sự vui mừng và bình an", "Niềm vui và bình an thật không đến từ hoàn cảnh mà từ Đấng Christ. Chuyên mục này gồm các sách giúp tín hữu tìm được sự vui mừng bền vững và bình an vượt quá mọi sự hiểu biết, ngay cả giữa giông bão cuộc đời.", r"\bjoy\b|rejoic|peace|gladness|cheerful|content|tranquil", r"vui mừng|bình an|vui vẻ|hân hoan|bằng lòng"),
 ("lo-lang-so-hai", "Lo lắng và sợ hãi", "Lo lắng đè nặng lòng người, nhưng Đức Chúa Trời kêu gọi con cái Ngài trao mọi lo âu cho Ngài. Chuyên mục này gồm sách giúp đối diện với lo lắng, sợ hãi và trầm cảm bằng lời hứa của Kinh Thánh và sự quan phòng đầy yêu thương của Cha trên trời.", r"anxiet|worry|fear|afraid|despair|depress|melanchol|troubled|cast.*care|fear not", r"lo lắng|lo âu|sợ hãi|trầm cảm|tuyệt vọng|nản lòng"),
 ("tien-bac", "Tiền bạc và sự dâng hiến", "Tiền bạc là đầy tớ tốt nhưng là ông chủ tồi. Chuyên mục này gồm sách về quan điểm Cơ Đốc về tiền bạc: quản lý trung tín của cải Chúa giao, tránh tham lam và nợ nần, dâng hiến vui vẻ — kể cả dâng một phần mười — và sống đơn sơ vì Nước Trời.", r"money|wealth|riches|covetous|steward|giving|tithe|generos|mammon|debt|rich and poor", r"tiền bạc|của cải|dâng hiến|tham lam|rộng rãi|quản lý|phần mười|giàu|nghèo"),
 ("cong-viec", "Công việc và ơn gọi", "Mọi công việc lương thiện đều là sự kêu gọi từ Đức Chúa Trời. Chuyên mục này trình bày thần học Cải Chánh về lao động: làm việc như làm cho Chúa, nghỉ ngơi đúng đắn, và dùng nghề nghiệp để phục vụ tha nhân và làm vinh hiển danh Ngài.", r"vocation|calling|work|labour|labor|business|trade|profession|diligence|idleness", r"công việc|nghề nghiệp|lao động|siêng năng|lười biếng|ơn gọi"),
 ("tinh-ban", "Tình yêu thương và sự thông công", "Dấu hiệu nhận biết môn đồ Đấng Christ là tình yêu thương nhau. Chuyên mục này gồm sách về tình yêu thương theo 1 Cô-rinh-tô 13, tình bạn Cơ Đốc, sự thông công trong Hội Thánh và bổn phận đối xử với tha nhân bằng ân điển.", r"\blove\b|charity|friendship|fellowship|brotherly|one another|neighbor|compassion|kindness", r"tình yêu|yêu thương|tình bạn|thông công|tha nhân|lân cận|nhân từ"),
 ("khon-ngoan", "Sự khôn ngoan", "Khởi đầu sự khôn ngoan là kính sợ Đức Giê-hô-va. Chuyên mục này tập hợp sách về sự khôn ngoan trong Châm Ngôn và toàn bộ Kinh Thánh: phân biệt khôn ngoan thật với khôn ngoan thế gian, và sống khôn ngoan trong mọi quyết định đời sống.", r"wisdom|wise|proverbs|prudence|folly|fool|understanding|discretion", r"khôn ngoan|châm ngôn|dại dột|thận trọng|hiểu biết"),
 ("thi-thien", "Thi Thiên và sự tĩnh nguyện", "Sách Thi Thiên là sách cầu nguyện và ca ngợi của Hội Thánh qua mọi thời đại. Chuyên mục này gồm sách giải nghĩa Thi Thiên và hướng dẫn đời sống tĩnh nguyện: suy gẫm Lời Chúa, cầu nguyện riêng tư và thờ phượng Chúa mỗi ngày.", r"psalm|devotion|quiet time|meditation|contemplation|morning and evening|daily|secret prayer|closet", r"thi thiên|tĩnh nguyện|suy gẫm|linh tu|mỗi ngày"),
 ("vinh-hien", "Sự vinh hiển của Đức Chúa Trời", "Mục đích tối cao của muôn vật là làm vinh hiển Đức Chúa Trời. Chuyên mục này gồm các sách giúp chiêm ngưỡng vinh quang của Chúa — trong Đấng Christ, trong công việc cứu chuộc và trong thiên đàng — để đời sống chúng ta phản chiếu vinh hiển Ngài.", r"glory|glorious|glorif", r"vinh hiển|vinh quang|vinh danh|làm vinh hiển"),
 ("bien-giao", "Biện giáo và sự phân biệt", "Hãy sẵn sàng trả lời mọi kẻ hỏi lẽ về sự trông cậy trong anh em. Chuyên mục này gồm sách biện giáo — bảo vệ đức tin trước sự tấn công của vô thần, hoài nghi và các hệ tư tưởng — cùng nguyên tắc phân biệt lẽ thật khỏi sự dối trá.", r"apologet|defense of|evidences|reason for the hope|discernment|atheis|sceptic|skeptic|worldview", r"biện giáo|bảo vệ đức tin|phân biệt|vô thần|hoài nghi|thế giới quan"),
 ("ta-giao", "Tà giáo và sự cảnh giác", "Sói đội lốt chiên luôn rình rập bầy chiên. Chuyên mục này gồm sách giúp nhận diện tà giáo, các giáo phái lạc giáo và sự dối trá thuộc linh — trang bị cho tín hữu sự cảnh giác và lòng trung thành với lẽ thật của Kinh Thánh.", r"heresy|heretic|cult|false teach|deception|wolves|error|antichrist|popery|romanism", r"tà giáo|dị giáo|lạc giáo|dối trá|sói đội lốt"),
 ("loi-hua", "Những lời hứa của Đức Chúa Trời", "Lời hứa của Đức Chúa Trời trong Đấng Christ đều là 'vâng' và 'a-men' — quý báu và chắc chắn. Chuyên mục này tập hợp các sách khai triển những lời hứa quý báu của Phúc Âm: nguồn an ủi vững chắc cho tín hữu trong mọi hoàn cảnh đời sống.", r"precious promises|promises of|yea and amen", r"lời hứa|quý báu|vâng và a-men|hứa nguyện"),
 ("bap-tem-tiec-thanh", "Báp-têm và Tiệc Thánh", "Báp-têm và Tiệc Thánh là hai thánh lễ Đấng Christ đã lập cho Hội Thánh. Chuyên mục này gồm sách trình bày ý nghĩa, cách thức và đối tượng của báp-têm cùng Tiệc Thánh theo quan điểm Cải Chánh, và cách dự phần xứng đáng.", r"baptism|sacrament|lord's supper|communion|eucharist|ordinance|paedobaptism|believer's baptism", r"báp-têm|tiệc thánh|thánh lễ|rửa tội|bí tích"),
 ("canh-chung", "Sự trở lại của Đấng Christ", "Đấng Christ sẽ trở lại trong vinh hiển để phán xét kẻ sống và kẻ chết. Chuyên mục này trình bày giáo lý cánh chung theo quan điểm Cải Chánh: sự tái lâm, sự sống lại, phán xét cuối cùng và trời mới đất mới — khích lệ tín hữu sống tỉnh thức và trông đợi.", r"second coming|eschatolog|last days|end times|millennium|rapture|resurrection|new heavens|revelation", r"tái lâm|cánh chung|ngày cuối cùng|sự sống lại|trời mới đất mới|khải huyền"),
 ("muoi-dieu-ran", "Mười Điều Răn", "Mười Điều Răn là bản tóm tắt thánh ý Đức Chúa Trời cho đời sống con người. Chuyên mục này gồm sách giải nghĩa từng điều răn theo truyền thống Cải Chánh — luật pháp như tấm gương chỉ tội, như người dẫn đến Đấng Christ và như quy tắc sống cho người đã được cứu.", r"ten commandments|decalogue|commandments|moral law|law of god|exodus 20|deuteronomy 5", r"mười điều răn|điều răn|luật pháp|luật đạo đức"),
 ("toi-loi-sa-nga", "Tội lỗi và sự sa ngã", "Tội lỗi là gì, nó đến từ đâu và tàn phá con người ra sao? Chuyên mục này trình bày giáo lý về tội lỗi theo quan điểm Cải Chánh: sự sa ngã của A-đam, nguyên tội, bản chất hư hoại toàn diện của con người — nền tảng để hiểu vì sao chúng ta cần Đấng Cứu Thế.", r"total depravity|original sin|the fall|sinfulness|doctrine of sin|indwelling sin|body of death", r"tội lỗi|sa ngã|nguyên tội|bản chất tội|hư hoại"),
 ("hiep-mot", "Sự hiệp một của Hội Thánh", "Đấng Christ cầu nguyện cho Hội Thánh được hiệp một. Chuyên mục này gồm sách về sự hiệp một Cơ Đốc: hiệp một trong lẽ thật — không phải hiệp một bằng mọi giá — tình yêu thương giữa các tín hữu và cách xử lý sự chia rẽ trong Hội Thánh.", r"unity|union|one body|schism|division|ecumenical", r"hiệp một|hiệp nhất|chia rẽ|một thân"),
 ("phuc-hung", "Sự phục hưng", "Xin Chúa phục hưng công việc Ngài giữa vòng chúng con. Chuyên mục này gồm sách về các cuộc phục hưng trong lịch sử Hội Thánh — đặc biệt cuộc Đại Tỉnh Thức — cùng những nguyên tắc Kinh Thánh về sự thăm viếng đặc biệt của Đức Thánh Linh.", r"revival|awakening|great awakening|outpouring|faithful narrative|surprising work", r"phục hưng|tỉnh thức|thức tỉnh|đại tỉnh thức"),
]
_X = {x["id"]: x for x in books["extra"]}
_TOPIC_LIST = [(s, n) for s, n, i, ren, rvi in TOPICS]
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
    tv = []
    for au, t, o, s in _TR:
        if rv.search(t) or rx.search(o):
            tv.append((au, t, s))
    tv.sort(key=lambda z: (z[0].lower(), z[1].lower()))
    tv = tv[:24]
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
        t = vt if vt else en
        return bcard(t, au, f"/reader.html?id={key}", kicker="Đọc trong thư viện", desc_=None if t == en else en)
    _vv_cards = "".join(bcard(t, a, u, kicker="Liên kết ngoài", ext=True) for t, u, a in vv)
    _cc_cards = "".join(li_c(c) for c in cc)
    _tv_cards = "".join(bcard(t, au, f"/ban-dich/{s}.html", badge="AI, chưa duyệt", kicker="Bản dịch RV") for au, t, s in tv)
    _rel = " ".join(f'<a href="/chu-de/{s}.html">{E(n)}</a>' for s, n in _TOPIC_LIST if s != slug)
    _kt = ('<p><a class="btn" href="/kinh-thanh-index.html">📖 Tìm sách theo phân đoạn Kinh Thánh</a></p>\n'
             if slug == "kinh-thanh" else "")
    body = f'''<p class="m"><a href="/chu-de/">← Tất cả chủ đề</a> · <a href="/lo-trinh.html">Lộ trình đọc</a></p>
{_kt}<h1>{E(name)}</h1><p>{E(intro)}</p>
<div class="note"><b>Lưu ý:</b> danh sách này do máy lọc theo từ khóa, ưu tiên các tác giả Cải Chánh kinh điển, và chưa được mục sư thẩm định. Sách tiếng Anh có nút 🌐 để dịch máy sang tiếng Việt trong trình đọc (có thể còn sai sót).</div>
<h2>Bản dịch tiếng Việt ({len(tv)})</h2>
{("<p>Chưa có.</p>" if not tv else bkgrid(_tv_cards))}
<h2>Sách tiếng Việt ({len(vv)})</h2>
{("<p>Chưa có.</p>" if not vv else bkgrid(_vv_cards))}
<h2>Sách kinh điển miễn phí, đọc trong thư viện ({len(cc)})</h2>
{bkgrid(_cc_cards)}
<h2>Chủ đề liên quan</h2><p class="rel">{_rel}</p>'''
    p = f"chu-de/{slug}.html"
    open(p, "w", encoding="utf-8").write(page(f"{name} – sách Cải Chánh miễn phí | Reformed Vietnam", intro + " Sách miễn phí tiếng Việt và tiếng Anh.", p, body))
    urls.append(p); _pages.append((slug, name, intro, len(cc) + len(vv)))
body = '<h1>Học theo chủ đề</h1><p>Chọn một chủ đề để xem sách miễn phí liên quan.</p><ul>' + "".join(f'<li><a href="/chu-de/{s}.html"><b>{E(n)}</b></a> <small>· {k} sách</small><br>{E(i)}</li>' for s, n, i, k in _pages) + '</ul>'
open("chu-de/index.html", "w", encoding="utf-8").write(page("Học theo chủ đề | Reformed Vietnam", "Sách Cải Chánh miễn phí theo chủ đề: ân điển, xưng công bình, Ba Ngôi, Hội Thánh, cầu nguyện, tiền định và nhiều hơn.", "chu-de/index.html", body))
urls.append("chu-de/index.html")

# Academy course content for Reformed Vietnam (Phase C).
# Authored by the integrator (Molly) 2026-11-06; every course page carries the
# "Nội dung AI soạn, chưa duyệt" label. Lessons are pathways through verified
# site content: WSC questions (verbatim), encyclopedia entries, Bible chapters,
# library books, and Reformed Answers. Quizzes for foundation/doctrine lessons
# are generated from the lesson's own WSC pool (choose the correct answer);
# ministry lessons carry hand-written quiz items in the Guide §10 shape.
#
# Lesson fields: title, objective, wsc[], enc[], bible[(book_id, chapter)],
# books[(label, url)], answers[slugs], summary[paragraphs], quiz (optional).

COURSES = [
{
  "slug": "nen-tang-duc-tin",
  "level": "foundation",
  "level_vi": "Cấp độ 1 · Nền tảng",
  "title": "Nền Tảng Đức Tin",
  "audience": "Cho người mới tin Chúa và bất cứ ai muốn nắm vững đức tin Cơ Đốc từ đầu, theo thứ tự của Tín Lý Yếu Lược Westminster.",
  "lessons": [
    {"title": "Mục đích của đời người",
     "objective": "Hiểu mục đích chính của đời người theo Kinh Thánh và vì sao mọi điều khác trong đức tin đều bắt đầu từ đây.",
     "wsc": [1], "enc": [], "bible": [("psa", 73)], "books": [], "answers": [],
     "summary": [
       "Tín Lý Yếu Lược bắt đầu không phải bằng tội lỗi hay luật pháp, mà bằng mục đích: đời người được dựng nên để làm vinh hiển Đức Chúa Trời và vui hưởng Ngài mãi mãi. Mọi bài học tiếp theo trong khóa này đều là sự triển khai của câu trả lời đầu tiên này.",
       "“Làm vinh hiển Đức Chúa Trời” nghĩa là sống sao cho người khác thấy Ngài là Đấng quý trọng nhất; “vui hưởng Ngài” nghĩa là tìm thấy niềm vui sâu nhất của mình trong chính Ngài. Hai điều này không tách rời: chúng ta làm vinh hiển Ngài nhất khi chúng ta vui hưởng Ngài nhất."]},
    {"title": "Kinh Thánh — quy tắc của đức tin",
     "objective": "Biết Đức Chúa Trời ban quy tắc nào để hướng dẫn đời sống đức tin, và Kinh Thánh chủ yếu dạy điều gì.",
     "wsc": [2, 3], "enc": ["duy-kinh-thanh"], "bible": [("2tim", 3)], "books": [], "answers": ["nguoi-moi-tin-chua-nen-bat-dau-doc-gi-truoc"],
     "summary": [
       "Đức Chúa Trời không để chúng ta tự đoán cách tôn vinh và vui hưởng Ngài: Ngài ban Lời Ngài — Kinh Thánh Cựu Ước và Tân Ước — làm quy tắc duy nhất và đầy đủ cho đức tin và đời sống.",
       "Nội dung chính của Kinh Thánh gồm hai phần: con người phải tin gì về Đức Chúa Trời, và Đức Chúa Trời đòi hỏi con người làm gì. Toàn bộ khóa học này đi theo đúng hai phần ấy: trước là những điều phải tin, sau là bổn phận phải làm."]},
    {"title": "Đức Chúa Trời là Đấng như thế nào?",
     "objective": "Nhận biết bản thể và các thuộc tính của Đức Chúa Trời, và chân lý Ngài là một nhưng có ba Ngôi.",
     "wsc": [4, 5, 6], "enc": ["ba-ngoi"], "bible": [("psa", 139)], "books": [], "answers": [],
     "summary": [
       "Đức Chúa Trời là Thần, vô hạn, đời đời và không thay đổi trong bản thể, quyền năng, thánh khiết, công chính, nhân lành và chân thật của Ngài. Ngài không bị giới hạn bởi thời gian, không gian hay sự yếu đuối như loài người.",
       "Chỉ có một Đức Chúa Trời chân thật và hằng sống, nhưng trong một bản thể ấy có ba Ngôi — Cha, Con và Thánh Linh — đồng bản chất, đồng quyền năng và vinh hiển. Đây là nền tảng của mọi giáo lý tiếp theo."]},
    {"title": "Sắc lệnh, sáng tạo và quan phòng",
     "objective": "Hiểu Đức Chúa Trời đã định chương trình đời đời của Ngài ra sao, và cách Ngài dựng nên cùng cai quản muôn vật.",
     "wsc": [7, 8, 9, 10, 11], "enc": ["su-tien-dinh", "su-quan-phong"], "bible": [("gen", 1)], "books": [], "answers": ["tien-dinh-co-phai-so-phan-mu-quang-khong"],
     "summary": [
       "Từ đời đời, Đức Chúa Trời đã định trước mọi điều sẽ xảy ra theo ý muốn khôn ngoan và thánh khiết của Ngài — nhưng Ngài không phải là tác giả của tội lỗi, và con người vẫn thật sự chịu trách nhiệm về lựa chọn của mình.",
       "Ngài thi hành chương trình ấy qua sự sáng tạo (dựng nên mọi vật từ hư vô trong sáu ngày) và sự quan phòng (gìn giữ và cai quản mọi loài thọ tạo cùng mọi hành động của chúng). Không có điều gì là ngẫu nhiên dưới tay Ngài."]},
    {"title": "Con người và sự sa ngã",
     "objective": "Biết con người được dựng nên thế nào, giao ước đầu tiên ra sao, và tội lỗi đã đem nhân loại vào tình trạng nào.",
     "wsc": [12, 13, 14, 16, 17, 18, 19], "enc": ["toi-loi"], "bible": [("gen", 3)], "books": [], "answers": [],
     "summary": [
       "Con người được dựng nên theo hình ảnh Đức Chúa Trời, có sự hiểu biết, công chính và thánh khiết, cùng quyền cai quản muôn loài. Nhưng tổ phụ chúng ta đã chọn phạm tội ăn trái cấm, và cả nhân loại — được đại diện bởi A-đam — sa ngã theo người.",
       "Tình trạng sa ngã gồm: tội tổ tông, mất sự công chính ban đầu, bản tính bại hoại, cùng mọi đau khổ đời này, sự chết và hình phạt đời đời. Đây là tin xấu mà Phúc Âm sẽ trả lời."]},
    {"title": "Đấng Christ — Đấng Trung Bảo",
     "objective": "Hiểu vì sao nhân loại cần một Đấng Trung Bảo, và Đấng Christ là ai: thật Chúa, thật người, thi hành ba chức vụ.",
     "wsc": [20, 21, 22, 23, 24, 25, 26], "enc": ["dang-christ", "dang-trung-bao"], "bible": [("isa", 53)], "books": [], "answers": [],
     "summary": [
       "Đức Chúa Trời không bỏ mặc cả nhân loại hư mất: từ đời đời Ngài đã chọn một dân cho Con Ngài và lập giao ước ân điển, ban Đấng Christ làm Đấng Trung Bảo duy nhất giữa Đức Chúa Trời và con người.",
       "Đấng Christ là Con Đức Chúa Trời trở nên người thật — hai bản tính trọn vẹn trong một Ngôi — để có thể thi hành chức vụ tiên tri (rao Lời Chúa), thầy tế lễ (dâng chính mình làm của lễ và cầu thay) và Vua (cai trị và bảo vệ dân Ngài)."]},
    {"title": "Sự cứu rỗi được áp dụng: xưng công chính và nên thánh",
     "objective": "Phân biệt và nối kết hai ơn lớn: Đức Chúa Trời xưng tội nhân là công chính, và Đức Thánh Linh làm họ nên thánh.",
     "wsc": [29, 30, 31, 32, 33, 35], "enc": ["su-cong-chinh", "su-nen-thanh"], "bible": [("rom", 8)], "books": [], "answers": ["xung-cong-chinh-khac-nen-thanh-o-cho-nao"],
     "summary": [
       "Sự xưng công chính là hành động một lần của Đức Chúa Trời: Ngài tha tội và kể sự công chính của Đấng Christ cho người tin — địa vị của họ thay đổi ngay và trọn vẹn, chỉ bởi đức tin, không bởi việc làm.",
       "Sự nên thánh là công việc dần dần của Đức Thánh Linh suốt đời tín đồ: chết dần với tội và sống càng ngày càng giống Đấng Christ. Hai ơn này khác nhau nhưng không bao giờ tách rời — ai được xưng công chính thì chắc chắn cũng được nên thánh."]},
    {"title": "Đức tin và sự ăn năn",
     "objective": "Hiểu đức tin cứu rỗi là gì, ăn năn dẫn đến sự sống là gì, và hai điều này liên kết với nhau ra sao.",
     "wsc": [86, 87], "enc": ["duc-tin", "an-nan"], "bible": [("mar", 1)], "books": [], "answers": [],
     "summary": [
       "Đức tin nơi Chúa Giê-xu Christ là ân điển cứu rỗi: nhờ đó chúng ta tiếp nhận và yên nghỉ một mình nơi Ngài để được cứu — không phải tin một cách mơ hồ, mà là nương cậy vào chính Con Người và công việc của Ngài.",
       "Sự ăn năn dẫn đến sự sống là khi tội nhân thật sự nhận biết tội mình, cảm biết lòng thương xót của Đức Chúa Trời trong Đấng Christ, đau buồn vì tội, ghét tội và quyết tâm từ bỏ nó để vâng lời Chúa. Đức tin và ăn năn luôn đi đôi với nhau."]},
    {"title": "Luật pháp của Đức Chúa Trời",
     "objective": "Nắm khung của Mười Điều Răn: luật pháp bày tỏ ý muốn Chúa, chỉ ra tội lỗi và hướng dẫn đời sống biết ơn.",
     "wsc": [39, 40, 41, 42, 43, 44], "enc": ["luat-phap"], "bible": [("exo", 20)], "books": [], "answers": [],
     "summary": [
       "Bổn phận Đức Chúa Trời đòi hỏi nơi con người là vâng theo ý muốn đã bày tỏ của Ngài. Ý muốn ấy được tóm tắt trong Mười Điều Răn: bốn điều đầu hướng về Đức Chúa Trời, sáu điều sau hướng về người lân cận.",
       "Luật pháp không cứu được ai — nó như tấm gương chỉ ra tội và đưa chúng ta đến với Đấng Christ. Nhưng với người đã được cứu, luật pháp trở thành bản đồ của đời sống biết ơn: chúng ta vâng lời vì đã được yêu, không phải để được yêu."]},
    {"title": "Các phương tiện ân điển: Lời Chúa, Báp-têm và Tiệc Thánh",
     "objective": "Biết Đức Thánh Linh thường dùng những phương tiện nào để ban ơn, và hai Thánh lễ của Hội Thánh có ý nghĩa gì.",
     "wsc": [88, 89, 90, 91, 94, 95, 96, 97], "enc": ["bap-tem", "tiec-thanh"], "bible": [("act", 2)], "books": [], "answers": [],
     "summary": [
       "Các phương tiện bên ngoài và thông thường mà Đấng Christ dùng để ban ơn cứu chuộc là: Lời Chúa (đọc và nghe giảng), các Thánh lễ và sự cầu nguyện. Lời Chúa được giảng dạy là phương tiện chính — vì vậy Hội Thánh coi trọng việc giảng dạy trung tín.",
       "Báp-têm là dấu và ấn của giao ước ân điển, bày tỏ sự kết hiệp với Đấng Christ. Tiệc Thánh là sự tưởng nhớ sự chết của Chúa và bữa tiệc của giao ước, trong đó tín hữu được nuôi dưỡng thuộc linh khi dự bằng đức tin."]},
    {"title": "Cầu nguyện và Bài Cầu Nguyện Chung",
     "objective": "Hiểu cầu nguyện là gì, vì sao người tin Chúa vẫn cầu nguyện dù Đức Chúa Trời tể trị, và học khung của Bài Cầu Nguyện Chung.",
     "wsc": [98, 99, 100], "enc": ["cau-nguyen"], "bible": [("mat", 6)], "books": [], "answers": ["neu-duc-chua-troi-da-dinh-moi-su-tai-sao-con-phai-cau-nguyen"],
     "summary": [
       "Cầu nguyện là dâng lên Đức Chúa Trời những ước muốn của chúng ta về những điều hợp ý Ngài, nhân danh Đấng Christ, với sự xưng tội và lòng biết ơn. Đức Chúa Trời định cả kết quả lẫn phương tiện — và cầu nguyện là một trong những phương tiện Ngài đã định.",
       "Bài Cầu Nguyện Chung là khuôn mẫu Chúa Giê-xu dạy: bắt đầu bằng lời ngợi khen và vương quốc của Cha, rồi mới đến nhu cầu của chúng ta — bánh hằng ngày, sự tha thứ, sự giải cứu khỏi cám dỗ. Thứ tự ấy dạy chúng ta cầu nguyện theo ưu tiên của Đức Chúa Trời."]},
    {"title": "Đời sống mới và hy vọng đời đời",
     "objective": "Biết những ơn ích tín hữu nhận trong đời này, trong sự chết và trong sự sống lại — và sống với hy vọng ấy mỗi ngày.",
     "wsc": [36, 37, 38], "enc": [], "bible": [("rev", 21)], "books": [], "answers": ["cai-chanh-reformed-nghia-la-gi"],
     "summary": [
       "Ngay trong đời này, người được kêu gọi cách hiệu quả đã nhận sự xưng công chính, địa vị làm con và sự nên thánh, cùng sự bình an lương tâm, niềm vui trong Đức Thánh Linh và sự tăng trưởng trong ân điển.",
       "Trong sự chết, linh hồn tín hữu được nên thánh trọn vẹn và vào vinh hiển; thân thể yên nghỉ chờ ngày sống lại. Trong sự sống lại, họ được vinh hiển, được Đức Chúa Trời công khai nhìn nhận và hưởng phước trọn vẹn trong Ngài mãi mãi. Khóa học kết thúc nơi nó bắt đầu: vui hưởng Đức Chúa Trời đời đời."]},
  ],
},
]

COURSES.append({
  "slug": "than-hoc-he-thong-1",
  "level": "doctrine",
  "level_vi": "Cấp độ 2 · Thần học",
  "title": "Thần Học Hệ Thống I — Giáo Lý Về Đức Chúa Trời",
  "audience": "Cho tín hữu đã có nền tảng, muốn đào sâu giáo lý về Đức Chúa Trời theo thứ tự hệ thống: thuộc tính, Ba Ngôi, sắc lệnh, sáng tạo, quan phòng, giao ước và sự chuộc tội.",
  "lessons": [
    {"title": "Các thuộc tính của Đức Chúa Trời",
     "objective": "Phân biệt thuộc tính không thông truyền và thông truyền được của Đức Chúa Trời, và biết mỗi thuộc tính kêu gọi một đáp ứng thờ phượng cụ thể.",
     "wsc": [4], "enc": ["su-cong-chinh"], "bible": [("psa", 139)],
     "books": [("Thần Tính Của Đức Chúa Trời — A. W. Pink", "/ban-dich/pink-godhood.html")], "answers": [],
     "summary": [
       "Khi Giáo Lý nói Đức Chúa Trời là Thần “vô hạn, đời đời, không thay đổi” trong bản thể, quyền năng, thánh khiết, công chính, nhân lành và chân thật, đó không phải là danh sách khô khan: mỗi thuộc tính là một lý do để tin cậy và thờ phượng.",
       "Các nhà thần học thường chia thuộc tính làm hai nhóm: những điều chỉ thuộc về Đức Chúa Trời (vô hạn, đời đời, không thay đổi, toàn năng) và những điều con người được phản chiếu một phần (khôn ngoan, nhân lành, công chính, chân thật). Chúng ta không bao giờ hiểu hết Ngài — nhưng điều Kinh Thánh bày tỏ là đủ để biết Ngài thật."]},
    {"title": "Ba Ngôi — một Đức Chúa Trời, ba Ngôi",
     "objective": "Trình bày được giáo lý Ba Ngôi từ Kinh Thánh và tránh hai cực đoan: chia Đức Chúa Trời thành ba thần, hoặc xóa nhòa các Ngôi thành các vai trò.",
     "wsc": [5, 6], "enc": ["ba-ngoi"], "bible": [("mat", 28)], "books": [], "answers": [],
     "summary": [
       "Kinh Thánh dạy một Đức Chúa Trời duy nhất, và dạy Cha là Đức Chúa Trời, Con là Đức Chúa Trời, Thánh Linh là Đức Chúa Trời — ba Ngôi phân biệt, đồng bản chất, đồng quyền năng và vinh hiển. Giáo lý Ba Ngôi không phải là toán học cần giải, mà là bản tính của Đấng chúng ta thờ phượng cần được tuyên xưng.",
       "Trong công việc cứu rỗi, ba Ngôi hành động không tách rời: Cha hoạch định và sai Con; Con thi hành sự cứu chuộc; Thánh Linh áp dụng cho tội nhân. Hiểu Ba Ngôi giúp chúng ta cầu nguyện, hát thờ phượng và đọc Kinh Thánh với con mắt nhìn thấy cả ba Ngôi."]},
    {"title": "Sắc lệnh đời đời và sự tuyển chọn",
     "objective": "Hiểu sắc lệnh của Đức Chúa Trời và giáo lý tuyển chọn theo cách Kinh Thánh giữ cả hai: chủ quyền của Chúa và trách nhiệm của con người.",
     "wsc": [7, 8, 20], "enc": ["su-tien-dinh", "su-tuyen-chon"], "bible": [("eph", 1)],
     "books": [("Chủ Quyền Của Đức Chúa Trời — A. W. Pink", "/ban-dich/mg1-049-sovereignty-of-god-pink.html")],
     "answers": ["tien-dinh-co-phai-so-phan-mu-quang-khong"],
     "summary": [
       "Sắc lệnh của Đức Chúa Trời là chương trình đời đời của Ngài, theo ý muốn tự do và không thay đổi của Ngài, vì vinh hiển Ngài, về mọi điều sẽ xảy ra. Trong chương trình ấy, sự tuyển chọn là hành động ân điển: từ đời đời Ngài đã chọn một số người cho sự sống đời đời trong Đấng Christ — không dựa trên bất cứ điều gì Ngài thấy trước nơi họ.",
       "Giáo lý này thường bị hiểu lầm là lạnh lùng. Trong Kinh Thánh, nó được ban cho để an ủi: sự cứu rỗi của chúng ta bắt đầu từ ý định yêu thương của Đức Chúa Trời trước khi sáng thế, nên nó không thể bị cướp mất bởi sự yếu đuối của chúng ta. Đồng thời, Phúc Âm vẫn được rao cho mọi người, và ai đến với Đấng Christ đều được tiếp nhận."]},
    {"title": "Sự sáng tạo",
     "objective": "Biết Đức Chúa Trời dựng nên muôn vật từ hư vô trong sáu ngày, tất cả đều rất tốt lành — và điều này nền tảng cho mọi giáo lý về con người.",
     "wsc": [9, 10], "enc": [], "bible": [("gen", 1), ("gen", 2)], "books": [], "answers": [],
     "summary": [
       "Công việc sáng tạo là Đức Chúa Trời, trong ban đầu, dựng nên mọi vật từ hư vô bởi Lời quyền năng của Ngài, trong sáu ngày, và tất cả đều rất tốt lành. Con người được dựng nên sau cùng, theo hình ảnh Ngài, có linh hồn sống đời đời — đỉnh điểm và là người quản gia của công trình sáng tạo.",
       "Giáo lý sáng tạo bảo vệ ba điều: Đức Chúa Trời là chủ của muôn vật (không phải chúng ta); vật chất là tốt (không phải tù ngục của linh hồn); và mỗi con người đều có phẩm giá vì mang hình ảnh Ngài."]},
    {"title": "Sự quan phòng",
     "objective": "Hiểu cách Đức Chúa Trời gìn giữ và cai quản mọi loài thọ tạo, kể cả qua những nguyên nhân thứ cấp và cả trong sự đau khổ.",
     "wsc": [11, 12], "enc": ["su-quan-phong"], "bible": [("rom", 8)], "books": [], "answers": [],
     "summary": [
       "Sự quan phòng là công việc thánh khiết, khôn ngoan và quyền năng của Đức Chúa Trời: Ngài gìn giữ và cai quản mọi loài thọ tạo cùng mọi hành động của chúng. Không một sợi tóc nào rơi ngoài ý Cha — nhưng Ngài cai quản qua các phương tiện thông thường: thời tiết, quyết định của con người, và cả những bàn tay của kẻ ác mà Ngài biến thành điều lành, như câu chuyện Giô-sép cho thấy.",
       "Quan phòng không hứa rằng tín hữu được miễn đau khổ; nó hứa rằng đau khổ của họ không vô nghĩa và không nằm ngoài tay Cha. Đó là gối đầu của tín hữu trong mọi hoàn cảnh."]},
    {"title": "Giao ước công việc và giao ước ân điển",
     "objective": "Phân biệt hai giao ước lớn trong Kinh Thánh và thấy cấu trúc giao ước là xương sống của toàn bộ câu chuyện cứu rỗi.",
     "wsc": [12, 20], "enc": ["giao-uoc", "giao-uoc-an-dien"], "bible": [("gal", 3)], "books": [], "answers": [],
     "summary": [
       "Với A-đam, Đức Chúa Trời lập giao ước công việc: sự sống được hứa cho sự vâng lời trọn vẹn, sự chết đe dọa khi bất tuân. A-đam phá vỡ giao ước ấy, và vì ông là đầu đại diện, cả nhân loại ở trong ông đều sa ngã.",
       "Ngay sau sự sa ngã, Đức Chúa Trời — hoàn toàn bởi ân điển — lập giao ước ân điển: Ngài ban Đấng Christ làm Đấng Trung Bảo và hứa sự sống đời đời cho mọi kẻ tin. Từ Áp-ra-ham qua Môi-se đến Đa-vít, giao ước ân điển được quản trị qua nhiều thời kỳ, nhưng chỉ có một giao ước và một Đấng Cứu Rỗi."]},
    {"title": "Tội lỗi, cơn thạnh nộ và sự đoán phạt",
     "objective": "Trình bày giáo lý về tội lỗi theo Kinh Thánh: bản chất, tính phổ quát và hậu quả đời đời của nó trước mặt Đức Chúa Trời thánh khiết.",
     "wsc": [14, 18, 19, 84], "enc": ["toi-loi", "con-thanh-no-cua-duc-chua-troi"], "bible": [("rom", 3)],
     "books": [("Kẻ Có Tội Trong Tay Đức Chúa Trời Thạnh Nộ — Jonathan Edwards", "/ban-dich/308-sinners-in-the-hands-of-an-angry-god-edwards.html")], "answers": [],
     "summary": [
       "Tội lỗi là mọi sự không phù hợp với luật pháp của Đức Chúa Trời hoặc vi phạm luật pháp ấy — trong hành động, lời nói, tư tưởng và cả bản tính. Tội không chỉ là “làm điều xấu”; nó là sự phản nghịch cá nhân chống lại một Đức Chúa Trời thánh khiết.",
       "Vì Đức Chúa Trời công chính, tội lỗi đáng bị cơn thạnh nộ và sự rủa sả của Ngài cả đời này lẫn đời sau. Đây là phần của Phúc Âm mà thời đại chúng ta ít muốn nghe nhất — nhưng nếu không thấy sự nguy hiểm, chúng ta sẽ không bao giờ thấy sự quý giá của Đấng Cứu Rỗi."]},
    {"title": "Đấng Christ — Tiên Tri, Thầy Tế Lễ, Vua",
     "objective": "Hiểu ba chức vụ của Đấng Trung Bảo và ý nghĩa của mỗi chức vụ đối với đời sống đức tin hằng ngày.",
     "wsc": [23, 24, 25, 26], "enc": ["dang-trung-bao"], "bible": [("heb", 4)], "books": [], "answers": [],
     "summary": [
       "Đấng Christ thi hành chức vụ Đấng Trung Bảo qua ba chức vụ mà Cựu Ước đã báo trước. Là Tiên Tri, Ngài bày tỏ ý muốn của Đức Chúa Trời cho sự cứu rỗi của chúng ta bằng Lời Ngài và Thánh Linh Ngài. Là Thầy Tế Lễ, Ngài dâng chính mình làm của lễ một lần đủ cả để thỏa mãn công lý của Đức Chúa Trời, và hiện đang cầu thay cho dân Ngài. Là Vua, Ngài chinh phục chúng ta cho Ngài, cai trị, bảo vệ và cuối cùng khuất phục mọi kẻ thù.",
       "Ba chức vụ trả lời ba nhu cầu sâu nhất của tội nhân: sự ngu dốt (cần được dạy), tội lỗi (cần được tha và có Đấng cầu thay), và sự yếu đuối (cần được cai trị và bảo vệ)."]},
    {"title": "Sự chuộc tội — Đấng Christ chết thay cho ai?",
     "objective": "Hiểu bản chất của sự chuộc tội (thay thế và thỏa mãn công lý) và phạm vi của nó theo thần học Cải Chánh.",
     "wsc": [25, 44], "enc": ["su-chuoc-toi", "su-chuoc-toi-dac-biet"], "bible": [("2cor", 5)],
     "books": [("Sự Chết Của Sự Chết Trong Sự Chết Của Đấng Christ — John Owen", "/ban-dich/arch-owen-death-of-death.html")], "answers": [],
     "summary": [
       "Trên thập tự giá, Đấng Christ gánh thay cơn thạnh nộ mà tội nhân đáng chịu: Ngài bị đối xử như chúng ta đáng bị, để chúng ta được đối xử như Ngài đáng được. Đây là sự thay thế hình phạt — trung tâm của Phúc Âm và là lý do thập tự giá không phải là một bi kịch mà là một chiến thắng.",
       "Thần học Cải Chánh dạy sự chuộc tội có phạm vi xác định: Đấng Christ chết với ý định cứu chuộc thật sự những người Cha đã ban cho Ngài — và mọi người Ngài đã chết thay đều chắc chắn được cứu. Lời mời của Phúc Âm vẫn được rao cho mọi người không phân biệt, và không ai đến với Đấng Christ mà bị từ chối."]},
    {"title": "Đức Thánh Linh — Đấng áp dụng sự cứu rỗi",
     "objective": "Biết Đức Thánh Linh là ai và Ngài áp dụng công việc của Đấng Christ cho tội nhân qua sự kêu gọi hiệu quả và tái sinh như thế nào.",
     "wsc": [29, 30, 31], "enc": ["duc-thanh-linh", "su-tai-sinh"], "bible": [("joh", 3)], "books": [], "answers": [],
     "summary": [
       "Đức Thánh Linh là Ngôi thứ ba của Ba Ngôi, thật là Đức Chúa Trời như Cha và Con. Công việc đặc biệt của Ngài trong sự cứu rỗi là áp dụng: những gì Đấng Christ đã hoàn thành ngoài chúng ta trong lịch sử, Thánh Linh thực hiện trong chúng ta.",
       "Sự kêu gọi hiệu quả là khi Thánh Linh, qua Lời Chúa, thuyết phục tội nhân về tội và sự khốn khổ, soi sáng tâm trí để biết Đấng Christ, đổi mới ý chí và kéo họ đến với Đấng Christ cách hữu hiệu — để họ tự nguyện ôm lấy Ngài. Con người không cộng tác tạo ra sự tái sinh; họ là kết quả của nó."]},
  ],
})

COURSES.append({
  "slug": "day-giao-ly-nhom-nho",
  "level": "ministry",
  "level_vi": "Cấp độ 3 · Phục vụ",
  "title": "Dạy Giáo Lý Cho Nhóm Nhỏ",
  "audience": "Cho người dẫn nhóm nhỏ, giáo viên Trường Chúa Nhật và tín hữu muốn dạy Tín Lý Yếu Lược cho gia đình hoặc nhóm của mình — thực hành, từng bước.",
  "lessons": [
    {"title": "Vì sao dạy giáo lý?",
     "objective": "Nắm được lý do Kinh Thánh của việc dạy giáo lý có hệ thống và vai trò của nó trong đời sống Hội Thánh.",
     "wsc": [1, 2, 3], "enc": [], "bible": [("mat", 28)], "books": [], "answers": [],
     "summary": [
       "Trước khi thăng thiên, Chúa Giê-xu truyền cho Hội Thánh dạy muôn dân “giữ mọi điều” Ngài đã truyền — không chỉ cảm xúc đức tin, mà nội dung đức tin. Giáo lý (catechism) là công cụ Hội Thánh đã dùng suốt nhiều thế kỷ để làm việc này: những câu hỏi đáp ngắn, có thứ tự, dễ nhớ, bao phủ toàn bộ đức tin.",
       "Dạy giáo lý không thay thế việc giảng dạy hay đọc Kinh Thánh; nó cho người học một bộ khung để mọi bài giảng và mọi đoạn Kinh Thánh đều có chỗ để gắn vào. Người có khung sẽ lớn lên nhanh và vững hơn người chỉ có những mảnh rời rạc."],
     "quiz": [
       {"q_vi": "Theo Đại Mạng Lệnh (Ma-thi-ơ 28), Hội Thánh được truyền làm gì với muôn dân?",
        "options_vi": ["Chỉ rao giảng mà không cần dạy dỗ thêm", "Dạy họ giữ mọi điều Chúa đã truyền", "Tổ chức các sự kiện lớn", "Thu thập danh sách tín hữu"], "answer_index": 1},
       {"q_vi": "Lợi ích chính của việc học giáo lý theo câu hỏi đáp là gì?",
        "options_vi": ["Học thuộc để thi đua với người khác", "Có một bộ khung có hệ thống cho toàn bộ đức tin, dễ nhớ và dễ ôn lại", "Thay thế hoàn toàn việc đọc Kinh Thánh", "Chỉ dành cho mục sư"], "answer_index": 1},
       {"q_vi": "Câu 1 của Tín Lý Yếu Lược nói mục đích chính của đời người là gì?",
        "options_vi": ["Sống hạnh phúc và thành công", "Làm vinh hiển Đức Chúa Trời và vui hưởng Ngài mãi mãi", "Trở nên người tốt trong xã hội", "Đi nhà thờ đều đặn"], "answer_index": 1}]},
    {"title": "Chuẩn bị một buổi học giáo lý",
     "objective": "Biết cấu trúc một buổi học 45–60 phút: mở đầu, đọc câu hỏi đáp, giải nghĩa, áp dụng và cầu nguyện.",
     "wsc": [98], "enc": ["cau-nguyen"], "bible": [("2tim", 3)], "books": [], "answers": [],
     "summary": [
       "Một buổi học giáo lý tốt có nhịp đơn giản: (1) ôn lại câu tuần trước bằng cách hỏi bất kỳ một thành viên; (2) đọc câu mới nhiều lần cùng nhau; (3) giải nghĩa từng cụm từ khó bằng lời của nhóm; (4) đọc câu Kinh Thánh căn cứ; (5) áp dụng bằng một câu hỏi đời thường; (6) kết thúc bằng cầu nguyện theo nội dung bài học.",
       "Chuẩn bị của người dẫn không nằm ở sự hùng biện mà ở ba việc: thuộc lòng câu hỏi đáp của tuần, đọc trước phần giải nghĩa (trang Bách Khoa của thuật ngữ chính là đủ), và viết sẵn hai câu hỏi thảo luận. Đừng giảng dài — giáo lý học tốt nhất khi người học tự nói lại bằng lời của mình."],
     "quiz": [
       {"q_vi": "Bước nào nên đứng đầu một buổi học giáo lý?",
        "options_vi": ["Giải nghĩa ngay câu mới", "Ôn lại câu của tuần trước", "Chia nhóm cầu nguyện dài", "Đọc hết 107 câu"], "answer_index": 1},
       {"q_vi": "Ba việc chuẩn bị quan trọng nhất của người dẫn là gì?",
        "options_vi": ["Chuẩn bị trình chiếu đẹp, âm thanh tốt, ghế ngồi thoải mái", "Thuộc câu hỏi đáp của tuần, đọc trước phần giải nghĩa, viết sẵn câu hỏi thảo luận", "In nhiều tài liệu phát tay", "Mời diễn giả khách"], "answer_index": 1},
       {"q_vi": "Theo Câu 98, cầu nguyện là gì?",
        "options_vi": ["Nghi thức mở đầu buổi nhóm", "Dâng lên Đức Chúa Trời những ước muốn hợp ý Ngài, nhân danh Đấng Christ, với xưng tội và biết ơn", "Đọc lại các bài cầu nguyện có sẵn", "Chỉ dành cho người lãnh đạo"], "answer_index": 1}]},
    {"title": "Dẫn thảo luận và trả lời câu hỏi khó",
     "objective": "Biết cách khuyến khích mọi người tham gia và xử lý những câu hỏi hóc búa (như tiền định) cách bình tĩnh, trung thực.",
     "wsc": [7], "enc": ["su-tien-dinh"], "bible": [("2tim", 2)], "books": [],
     "answers": ["tien-dinh-co-phai-so-phan-mu-quang-khong", "neu-duc-chua-troi-da-dinh-moi-su-tai-sao-con-phai-cau-nguyen"],
     "summary": [
       "Người dẫn tốt nói ít hơn người học. Hãy hỏi “theo bạn, câu này có nghĩa là gì?” trước khi giải thích; ghi nhận mọi đóng góp; và khi nhóm yên lặng, hãy chờ — sự im lặng vài giây thường là lúc người nhút nhát nhất sắp lên tiếng.",
       "Với câu hỏi khó, có ba câu trả lời luôn đúng: “Kinh Thánh dạy điều này — chúng ta cùng đọc đoạn gốc”; “phần này có chỗ tôi chưa hiểu hết, tôi sẽ tìm hiểu và trả lời tuần sau” (rồi giữ lời hứa); và “đây là chỗ các tín hữu chân thành có thể khác nhau — chúng ta tôn trọng nhau”. Đừng bao giờ bịa một câu trả lời để giữ thể diện."]},
    {"title": "Dạy trẻ em và người mới tin",
     "objective": "Điều chỉnh nhịp độ và ngôn ngữ khi dạy giáo lý cho trẻ em và người mới tin Chúa mà không làm mất nội dung.",
     "wsc": [1, 4], "enc": [], "bible": [("mar", 10)],
     "books": [("Giáo Lý Vấn Đáp Đơn Giản Cho Trẻ Em — Matthew Henry", "/ban-dich/095-a-plain-catechism-for-children-henry.html")], "answers": [],
     "summary": [
       "Trẻ em học giáo lý tốt hơn người lớn tưởng: trí nhớ của các em mạnh, và những câu trả lời ngắn, có vần điệu tự nhiên sẽ ở lại suốt đời. Bí quyết là mỗi buổi chỉ một câu, lặp lại nhiều cách (đọc, hỏi, đố vui), và luôn nối câu giáo lý với một câu chuyện Kinh Thánh cụ thể.",
       "Với người mới tin, đừng giả định họ biết các thuật ngữ: “giao ước”, “xưng công chính”, “Thánh lễ” đều cần được giải nghĩa bằng lời đời thường trước. Các trang Bách Khoa của trang web được viết đúng cho mục đích này — hãy cho người học đọc trước ở nhà."]},
    {"title": "Gốc rễ lịch sử: Hội Nghị Westminster",
     "objective": "Biết Tín Lý Yếu Lược ra đời trong hoàn cảnh nào và vì sao nguồn gốc ấy giúp chúng ta tin cậy lẫn khiêm nhường khi dạy.",
     "wsc": [], "enc": [], "bible": [],
     "books": [("Sự Hình Thành Bản Tuyên Xưng Đức Tin Westminster — B. B. Warfield", "/ban-dich/858-su-hinh-thanh-ban-tin-nguong-westminster.html")], "answers": [],
     "summary": [
       "Năm 1643, giữa nội chiến Anh, Quốc hội triệu tập hơn một trăm mục sư và nhà thần học tại Tu viện Westminster để cải tổ Hội Thánh Anh theo Kinh Thánh. Trong gần sáu năm, họ soạn Bản Tuyên Xưng Đức Tin, Giáo Lý Lớn và Giáo Lý Yếu Lược — những văn kiện mà Hội Thánh Cải Chánh khắp thế giới dùng cho đến nay.",
       "Hai điều từ lịch sử này khích lệ người dạy giáo lý hôm nay: thứ nhất, giáo lý được soạn bởi một hội đồng trong nhiều năm cầu nguyện và tranh luận — nó không phải ý kiến của một cá nhân nên đáng để học cho kỹ; thứ hai, chính các tác giả cũng là những người phục vụ Hội Thánh địa phương — giáo lý sinh ra từ bục giảng, không phải từ tháp ngà."]},
    {"title": "Ôn tập, khích lệ và nhân rộng nhóm",
     "objective": "Biết cách ôn tập theo chu kỳ, khích lệ người học hoàn thành 107 câu và chuẩn bị người dẫn tiếp theo.",
     "wsc": [107], "enc": [], "bible": [("2tim", 2)], "books": [], "answers": [],
     "summary": [
       "Trí nhớ cần ôn tập có khoảng cách: ôn câu cũ sau một tuần, một tháng, rồi một quý. Cuối mỗi phần lớn của Giáo Lý (đức tin — điều răn — cầu nguyện), hãy dành một buổi chỉ để ôn và đố vui cả nhóm; trang trắc nghiệm của mục Giáo Lý trên trang web làm việc này rất tốt.",
       "Mục tiêu cuối cùng không chỉ là một nhóm thuộc 107 câu, mà là những người học trở thành người dạy. Ngay từ giữa khóa, hãy để các thành viên thay phiên dẫn phần ôn tập; khi khóa kết thúc, người tốt nhất trong nhóm chính là người dẫn của nhóm tiếp theo. Nhân rộng là dấu hiệu của một nhóm khỏe mạnh."]},
  ],
})

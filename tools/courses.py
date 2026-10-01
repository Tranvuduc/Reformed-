# Executed from build-pages.py (uses: page, E, urls). Builds khoa-hoc.html: free online theology courses with detailed info.
_C = [
 dict(n="Thirdmill Institute", u="https://thirdmillinstitute.org/", kind="Chương trình chứng chỉ",
  d="Chương trình học thần học theo từng bước: ba chứng chỉ nối tiếp nhau, hoàn thành cả ba thì nhận Văn bằng Mục vụ Cơ Đốc (Diploma in Christian Ministry).",
  rows=[("Cấu trúc","14 môn: Chứng chỉ Nền tảng (4 môn), Chứng chỉ Nghiên cứu Kinh Thánh (5 môn), Chứng chỉ Thần học (5 môn). Mỗi môn gồm 1–3 chuỗi bài giảng."),
        ("Chi phí","Miễn phí."),
        ("Ngôn ngữ","Chủ yếu tiếng Anh. Chứng chỉ Nền tảng có nhiều ngôn ngữ (Trung, Pháp, Tây Ban Nha, Indonesia, Thái, Hindi…) nhưng danh sách trên trang chưa ghi tiếng Việt."),
        ("Hình thức","Bài giảng video và tài liệu học; có người hướng dẫn (trainer) đồng hành."),
        ("Chứng nhận","Chứng chỉ và văn bằng của Thirdmill. Đây không phải bằng cấp được kiểm định."),
        ("Phù hợp","Người muốn một lộ trình có thứ tự, từ cơ bản đến thần học Cải Chánh, kèm mục tiêu hoàn thành rõ ràng.")],
  tip="Bắt đầu với Chứng chỉ Nền tảng (4 môn), rồi mới sang Kinh Thánh và Thần học."),
 dict(n="Thirdmill E-Learning", u="https://elearning.thirdmill.org/", kind="Cổng học trực tuyến",
  d="Cổng học của Thirdmill để đăng ký các khóa, theo dõi tiến độ và làm bài kiểm tra.",
  rows=[("Chi phí","Miễn phí khi học các chương trình của Thirdmill."),("Ngôn ngữ","Tiếng Anh (cùng các ngôn ngữ mà từng khóa hỗ trợ)."),("Hình thức","Tài khoản học viên, bài học, bài kiểm tra trực tuyến."),("Phù hợp","Người đã chọn học chương trình của Thirdmill Institute và cần nơi làm bài, lưu tiến độ.")],
  tip="Dùng cùng trang Thirdmill Institute: chọn khóa ở Institute, học và làm bài ở E-Learning."),
 dict(n="Thirdmill – lớp học video", u="https://thirdmill.org/watch.asp", kind="Video",
  d="Thư viện lớp thần học dạng video do Thirdmill thực hiện, xem tự do không cần đăng ký.",
  rows=[("Chi phí","Miễn phí."),("Ngôn ngữ","Tiếng Anh; Thirdmill có bản nhiều ngôn ngữ cho một số khóa, hãy kiểm tra trên trang."),("Hình thức","Video bài giảng kèm tài liệu học."),("Phù hợp","Người muốn xem thử một chủ đề trước khi theo cả chương trình.")],
  tip="Có thể bật phụ đề tự dịch của YouTube hoặc trình duyệt khi xem."),
 dict(n="BiblicalTraining.org", u="https://www.biblicaltraining.org/", kind="Thư viện lớp học",
  d="Thư viện lớp học Kinh Thánh và thần học miễn phí lớn nhất của giới Tin Lành, phần lớn quay trong lớp học chủng viện thật.",
  rows=[("Quy mô","Khoảng 150 khóa, hơn 1.000 giờ học."),("Chi phí","Hoàn toàn miễn phí, không có gói trả phí; sống nhờ quyên góp."),("Giảng viên","Wayne Grudem, Bruce Ware, Gerald Bray, Tim Mackie, Bill Mounce và nhiều người khác."),("Hình thức","Video và âm thanh, có bản chép lời và ghi chú lớp; ứng dụng di động xem ngoại tuyến."),("Chứng nhận","Có chương trình chứng chỉ miễn phí (cần làm bài kiểm tra) nhưng không được kiểm định và không chuyển đổi thành tín chỉ."),("Quan điểm","Tin Lành, nghiêng về Cải Chánh."),("Lưu ý","Chất lượng quay là quay lớp học, không có tương tác với giảng viên, khá khó tìm khóa nếu không theo chương trình.")],
  tip="Theo ba chương trình có sẵn (Nền tảng, Nghề nghiệp, Lãnh đạo) thay vì chọn từng khóa lẻ. Có cả chuỗi Hy Lạp và Hê-bơ-rơ."),
 dict(n="TGC Courses", u="https://www.thegospelcoalition.org/courses/", kind="Khóa ngắn",
  d="Các khóa học ngắn của The Gospel Coalition, thiết kế gọn, dễ xem trên điện thoại, mỗi phần có đường dẫn riêng.",
  rows=[("Chi phí","Miễn phí, không cần đăng ký hay đăng nhập."),("Chủ đề","Sách Kinh Thánh (như Lu-ca, Rô-ma, Ga-la-ti, Giăng), hình thành Tân Ước, Năm Solas, Cải Chánh, đời sống Cơ Đốc và mục vụ."),("Giảng viên","D. A. Carson, Michael Kruger và các học giả đối tác."),("Quan điểm","Tin Lành, theo các Tài liệu Nền tảng của TGC (Cải Chánh rộng)."),("Phù hợp","Người bận rộn muốn học từng chủ đề ngắn, không cần cam kết cả chương trình.")],
  tip="Chọn khóa theo sách Kinh Thánh bạn đang đọc."),
 dict(n="Learn Ligonier", u="https://learn.ligonier.org/", kind="Bài giảng",
  d="Kho bài giảng của R.C. Sproul và Ligonier về thần học Cải Chánh, rõ ràng và dễ theo dõi.",
  rows=[("Quy mô","Hơn 170 chuỗi bài giảng, hơn 1.400 bài, hơn 500 giờ (âm thanh và video)."),("Chi phí","Các chuỗi bài giảng của R.C. Sproul miễn phí vĩnh viễn. Các khóa Ligonier Connect (có giảng viên) có thể tính phí; hãy kiểm tra trên trang."),("Nội dung nổi bật","Foundations (tổng quan thần học hệ thống), Dust to Glory (Kinh Thánh), Defending Your Faith (biện giáo)."),("Quan điểm","Cải Chánh, đặc biệt dễ tiếp cận cho người mới."),("Hình thức","Web và ứng dụng Ligonier.")],
  tip="Mở đầu với Foundations: chuỗi bài đi qua các giáo lý chính của đức tin Cải Chánh."),
 dict(n="Covenant Worldwide", u="https://worldwide.covenantseminary.edu/", kind="Chủng viện",
  d="Các khóa mức Thạc sĩ Thần học (MDiv) của Covenant Theological Seminary, chủng viện của Hội Thánh Trưởng Lão PCA.",
  rows=[("Chi phí","Hoàn toàn miễn phí."),("Nội dung","Cựu Ước, Tân Ước, thần học hệ thống và lịch sử, giải kinh, mục vụ."),("Hình thức","Mỗi khóa gồm bài giảng âm thanh, bản chép lời đầy đủ và hướng dẫn học."),("Chứng nhận","Không có tín chỉ hay điểm số. Muốn lấy tín chỉ phải đăng ký riêng với chủng viện."),("Quan điểm","Cải Chánh – Trưởng Lão nhất quán."),("Lưu ý","Không có phản hồi từ giảng viên; cần tự giữ kỷ luật. Chỉ là phần được tuyển chọn của kho bài.")],
  tip="Bản chép lời giúp bạn đọc song song và dịch từng đoạn bằng công cụ của trình duyệt."),
 dict(n="Reformed Theological Seminary (RTS)", u="https://rts.edu/", kind="Chủng viện",
  d="Bài giảng chủng viện Cải Chánh từ RTS, cùng giảng viên và tài liệu với chương trình có cấp bằng.",
  rows=[("Chi phí","Miễn phí để nghe và tải."),("Nội dung","Cựu Ước, Tân Ước, thần học hệ thống, thần học lịch sử, biện giáo, đạo đức học, mục vụ."),("Hình thức","Chủ yếu âm thanh (tải về hoặc podcast), sắp xếp theo từng khóa trọn vẹn."),("Chứng nhận","Không có tín chỉ, điểm hay học bạ cho phần nghe miễn phí."),("Quan điểm","Cải Chánh – Trưởng Lão, ghi rõ lập trường thần học."),("Lưu ý","Tìm khóa trọn vẹn đôi khi phải lục qua nhiều nền tảng; tìm theo tên môn và giảng viên.")],
  tip="Nghe theo từng khóa từ bài đầu đến bài cuối, đừng nghe lẻ."),
 dict(n="Monergism – thư mục lớp học chủng viện miễn phí", u="https://www.monergism.com/topics/education-academia/library-free-online-seminary-courses", kind="Danh mục",
  d="Danh mục tuyển chọn các khóa và bài giảng chủng viện miễn phí từ nhiều trường Cải Chánh.",
  rows=[("Chi phí","Miễn phí; mỗi mục dẫn đến trường hoặc tổ chức riêng."),("Ngôn ngữ","Chủ yếu tiếng Anh."),("Phù hợp","Người đã học hết một chương trình và cần tìm thêm khóa sâu hơn theo môn.")],
  tip="Dùng để tìm môn cụ thể (thí dụ giáo lý Cải Chánh, lịch sử Hội Thánh) khi các trang trên chưa đủ."),
]
def _card(c):
    rows = "".join(f"<tr><th>{E(k)}</th><td>{E(v)}</td></tr>" for k, v in c["rows"])
    return f'''<li class="cr"><div class="ch"><b>{E(c["n"])}</b><span class="kd">{E(c["kind"])}</span></div><p>{E(c["d"])}</p><table>{rows}</table><p class="tp">💡 {E(c["tip"])}</p><div class="ca"><a class="go" href="{E(c["u"])}" rel="noopener" target="_blank">Mở khóa học ↗</a></div></li>'''
_cards = "".join(_card(c) for c in _C)
_css = '<style>.cr{list-style:none;margin:0 0 16px;padding:16px 18px;border:1px solid #8884;border-radius:12px}ul.cl{padding:0}.ch{display:flex;gap:10px;align-items:baseline;flex-wrap:wrap}.ch b{font-size:1.1rem}.kd{font-size:.75rem;padding:2px 8px;border:1px solid #8886;border-radius:999px;opacity:.8}.cr p{margin:8px 0}.cr table{width:100%;border-collapse:collapse;font-size:.92rem;margin:6px 0}.cr th{width:28%;text-align:left;vertical-align:top;padding:5px 10px 5px 0;opacity:.7;font-weight:600}.cr td{padding:5px 0;border-top:1px solid #8883}.cr tr:first-child td,.cr tr:first-child th{border-top:0}.tp{font-size:.92rem;background:#9a34120f;padding:8px 10px;border-radius:8px}.ca{margin-top:8px}.go{font-weight:700}@media(max-width:560px){.cr th{width:34%}.cr{padding:14px}}small{color:#5a5f68}</style>'
_body = f'''{_css}<h1>Học thần học trực tuyến miễn phí</h1><p class="m">Các khóa học dưới đây do các trường và tổ chức bên ngoài cung cấp. Reformed Vietnam chỉ giới thiệu và không tổ chức lớp.</p>
<p>Chín nguồn học thần học trực tuyến, miễn phí hoặc có phần miễn phí. Mỗi mục ghi chi phí, nội dung, hình thức, chứng nhận và điều cần lưu ý. Hầu hết bằng tiếng Anh.</p>
<h2>Chọn nhanh</h2>
<ul><li><b>Muốn có lộ trình và chứng chỉ:</b> Thirdmill Institute hoặc BiblicalTraining.org.</li><li><b>Mới bắt đầu, thích nghe giảng dễ hiểu:</b> Learn Ligonier (Foundations).</li><li><b>Muốn học như sinh viên chủng viện:</b> Covenant Worldwide hoặc RTS.</li><li><b>Muốn học từng sách Kinh Thánh, ngắn gọn:</b> TGC Courses.</li></ul>
<p><small>Không nguồn nào trong danh sách cho tín chỉ được kiểm định. Chứng chỉ chỉ là xác nhận hoàn thành của chính tổ chức đó.</small></p>
<ul class="cl">{_cards}</ul>
<h2>Mẹo học hiệu quả</h2>
<ul><li>Chọn một chương trình và học đều: 20–30 phút mỗi ngày tốt hơn một buổi dài mỗi tuần.</li><li>Bài giảng dùng thuật ngữ Cải Chánh nhiều; đối chiếu Kinh Thánh và hỏi mục sư hoặc người hướng dẫn của bạn.</li><li>Đọc sách liên quan trong <a href="/">thư viện</a> và <a href="/lo-trinh.html">lộ trình đọc</a> để học sâu hơn.</li></ul>
<p><small>Thông tin lấy từ chính các trang và đánh giá công khai, có thể đã thay đổi; hãy kiểm tra trên trang gốc. Các liên kết dẫn đến trang bên ngoài. Reformed Vietnam không liên kết chính thức với các trường này.</small></p>'''
open("khoa-hoc.html", "w", encoding="utf-8").write(page("Khóa học thần học trực tuyến miễn phí (Thirdmill, Ligonier, RTS…) | Reformed Vietnam", "Chín nguồn học thần học trực tuyến miễn phí: Thirdmill, BiblicalTraining, Ligonier, Covenant, RTS, TGC. Chi phí, nội dung, hình thức và chứng nhận của từng nơi.", "khoa-hoc.html", _body))
urls.append("khoa-hoc.html")

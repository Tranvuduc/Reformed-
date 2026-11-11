# Báo cáo kiểm tra chất lượng bản dịch — 2026-11-11

Kiểm tra bằng `scripts/check_translations.py` trên toàn bộ `translations/*.txt` (3,211 tệp) và chỉ mục (2,960 mục). Script này KHÔNG sửa bản dịch — mọi mục dưới đây đều cần quyết định của người duyệt trước khi sửa.

## Tổng quan

- Dòng đầu "AI, chưa duyệt": 224 có / 2,987 thiếu (hầu hết là tệp nhập hàng loạt cũ; nhãn "Bản dịch AI, chưa duyệt" vẫn hiện trên mọi trang sách qua huy hiệu duyệt).
- Thiếu chân trang TRANSLATION STATUS: 48 tệp; thiếu TERMINOLOGY ISSUES: 50 tệp.
- Dấu [NEEDS REVIEW]: 142,058 dấu trong 2,199 tệp (ghi chú phục dựng OCR / chỗ chưa chắc — không tự nó là lỗi).
- Đoạn tiếng Anh chưa dịch (ngưỡng: >10 dòng và >2% số dòng): 67 tệp, tổng 9,769 dòng.
- "công bình": 54,197 lượt trong 2,042 tệp — PHẦN LỚN là trích dẫn Kinh Thánh 1934 nguyên văn (ví dụ Ê-sai 64:5: “Chúa đón kẻ vui mừng làm sự công bình”), nơi từ này là đúng. Chỉ sai khi là giọng văn của chính bản dịch — cần rà soát thủ công từng chỗ, không sửa hàng loạt.
- "Kinh Lạy Cha": 995 lượt (250 tệp) và "Kinh Tin Kính": 526 lượt (161 tệp) — đối chiếu mẫu cho thấy phần lớn là tên gọi quen thuộc của bài cầu nguyện / tín điều BÊN TRONG văn bản được dịch (“đọc kinh Lạy Cha”, “đã học thuộc Kinh Tin Kính”), không phải giọng văn riêng của trang. Thuật ngữ khóa “Bài Cầu Nguyện Chung” / “Tín Điều Các Sứ Đồ” áp dụng cho giọng văn của trang; có sửa các chỗ trong bản dịch hay không là quyết định duyệt theo ngữ cảnh, không sửa hàng loạt.
- "nước Đức Chúa Trời": 8,770 lượt trong 1,429 tệp — như "công bình": đúng trong trích dẫn 1934, giọng văn riêng dùng "Vương quốc Đức Chúa Trời". Cần rà soát thủ công.
- Dấu hiệu markdown trong văn bản thuần: backtick 88 tệp, liên kết markdown 0 tệp, trích dẫn `>` 67 tệp, thẻ HTML 91 tệp.
- Tệp rất ngắn (<200 ký tự): 0 tệp; không có dòng tựa: 0 tệp.
- Chỉ mục thiếu tệp: 0 mục; tệp txt chưa có trong chỉ mục: 257 tệp — trong đó 79 tệp có khả năng là bản dịch khác của tác phẩm đã có (đối chiếu tên tệp; ví dụ 003-marrow-modern-divinity-fisher.txt và mg1-1094-marrow-divinity-fisher.txt là hai bản dịch khác nhau của cùng một tác phẩm Fisher), còn 178 tệp không khớp tác phẩm nào trong chỉ mục. Cần đối chiếu từng tệp trước khi quyết định giữ, liệt kê hay dọn.

## Tệp có nhiều đoạn tiếng Anh nhất

- `mg1-790-ladies-of-the-reformation-memoirs-of-distinguished-anderson.txt` — 290 dòng — ví dụ: _1. Bruce’s Free Thoughts on the Toleration of Popery, tr. 127._
- `mg1-974-the-christian-doctrine-of-prayer-reformed-theology-hastings.txt` — 271 dòng — ví dụ: _Brooke, H., One Faith and One Family (1907)._
- `mg1-793-letters-of-samuel-rutherford-rutherford.txt` — 184 dòng — ví dụ: _M      More happy than imaginèd can be,_
- `878.txt` — 164 dòng — ví dụ: _"There are in fact, as we might have anticipated, but two_
- `mg1-1026-the-end-of-infidelity-reformed-theology-ebook-hays.txt` — 140 dòng — ví dụ: _TEC = The End Of Christianity_
- `mg1-688-dispensationalism-today-yesterday-and-tomorrow-ref-gunn.txt` — 132 dòng — ví dụ: _1. Charles Caldwell Ryrie, The Basis of the Premillennial Faith (Neptune, N.J.: Loizeaux Brothers, 1953), trang 17, so sánh trang 33._
- `arch-analogyconsidere00buch.txt` — 112 dòng — ví dụ: _* F. D. Maurice, “What is Revelation?”, tr. 173, 176._
- `052-s-austin-his-place-history-christian-cunningham.txt` — 110 dòng — ví dụ: _^ So sánh chính ngôn ngữ của ông về sự tôn trọng dành cho ý kiến của mình: Sane cum in omnibus litteris meis non solum pium lectorem, sed etiam liberum correcto_
- `mg1-1007-the-doctrine-of-justification-an-outline-of-its-hi-buchanan.txt` — 107 dòng — ví dụ: _‘Thirty Years’ Correspondence between Bishop Jebb and Mr. Knox,’ 2 tập, khổ 8vo, 1834._
- `mg1-761-history-reformation-daubigne.txt` — 106 dòng — ví dụ: _Oi=a tij h`li,ou bolh,. Eusebius. Hist. Eccles. H.S. ↩ Thessalonians 2. ↩ John 5:11. ↩ John 6:45. ↩ Acts 15:23. ↩ Thessalonians 2. ↩ Suburbicaria loca. — Xem gi_
- `sach-21-kinh-thanh-va-nghe-nghiep.txt` — 101 dòng — ví dụ: _THE BIBLE AND YOUR WORK_
- `sach-20-giua-hai-nen-van-hoa.txt` — 99 dòng — ví dụ: _Faith, Family, and Identity for Young Vietnamese Abroad_
- `sach-19-nam-solas-song-ngu.txt` — 94 dòng — ví dụ: _Five Reformation Watchwords in Vietnamese and English_
- `book-common-order-knox.txt` — 92 dòng — ví dụ: _Leis an Easpuig Carsuel (in ms.)_
- `mg1-777-in-search-for-the-beginning-a-seekers-journey-to-t-davis.txt` — 90 dòng — ví dụ: _CC: Crash Course on the New Age_
- `sach-18-duc-tin-cai-chanh-trong-15-phut.txt` — 90 dòng — ví dụ: _Eight Foundations for Young Vietnamese at Home and Abroad_
- `bavinck-revelation.txt` — 89 dòng — ví dụ: _Một số bài giảng cũng đã được giảng tại Grand Rapids và Holland, Michigan; Chicago; Louisville; New Brunswick và Paterson, New Jersey; và New York._
- `821-hoi-nghi-westminster-va-cong-viec-cua-hoi-nghi.txt` — 88 dòng — ví dụ: _1. Originally printed in The Princeton Theological Review, vi. 1908, pp. 177–210._
- `list-940-cuoc-hanh-trinh-cua-dao-that-keach.txt` — 82 dòng — ví dụ: _Reynolds's Triumphs of Gods Revenge against the crying and execrable Sin of Murder, thể hiện qua nhiều câu chuyện bi thảm; ấn bản thứ sáu, hiệu đính cẩn thận: k_
- `mg1-466-the-history-of-christian-doctrines-church-history-berkhof.txt` — 78 dòng — ví dụ: _Tài liệu tham khảo: Harnack, History of Dogma I, tr. 1–40; Seeberg, History of Doctrines I, tr. 19–27; Loofs, Handboek der Dogmengeschiedenis, tr. 1–9; Neander,_

## Tệp có nhiều dấu [NEEDS REVIEW] nhất

- `arch-bim_early-english-books-1641-1700_the-preeminence-of-th.txt` — 4414 dấu
- `arch-bim_early-english-books-1641-1700_the-doctrine-of-the-s.txt` — 4341 dấu
- `719-sermons-m-john-calvin-1574-calvin.txt` — 3372 dấu
- `w1-r0481.txt` — 2952 dấu
- `arch-fourbooksonelev00burrgoog.txt` — 2864 dấu
- `arch-survspiva00ruth.txt` — 2492 dấu
- `hervey-meditations-contemplations.txt` — 1976 dấu
- `arch-bim_early-english-books-1641-1700_of-the-constitution-r.txt` — 1793 dấu
- `rutherford-temperate-plea.txt` — 1617 dấu
- `arch-bim_early-english-books-1475-1640_a-commentarie-of-john.txt` — 1597 dấu
- `arch-divinerightofchu00ruth.txt` — 1561 dấu
- `arch-bim_early-english-books-1641-1700_a-learned-commentary-.txt` — 1351 dấu
- `arch-sibbes-souls-conflict-1635.txt` — 1305 dấu
- `mg1-500-the-virgin-birth-of-christ-biblical-studies-ebook-machen.txt` — 1135 dấu
- `686-summary-natural-religion-containing-proof-being-johnson.txt` — 1076 dấu
- `arch-10411071bsb.txt` — 1019 dấu
- `896-the-pleasantness-of-a-religious-life-henry.txt` — 1016 dấu
- `096-bovvels-opened-1648-sibbes.txt` — 993 dấu
- `manton-sermons-1678.txt` — 979 dấu
- `whitefield-works-vol2.txt` — 963 dấu

## Tệp có nhiều "công bình" nhất (cần rà soát thủ công)

- `mg1-641-christ-crucified-72-sermons-on-isaiah-53-sermons-e-durham.txt` — 1080 lượt
- `mg1-1219-the-works-of-john-macduff-macduff.txt` — 708 lượt
- `mg1-507-a-body-of-divinity-lectures-on-the-assemblys-large-ridgley.txt` — 664 lượt
- `mg1-428-the-existence-and-attributes-of-god-reformed-theol-charnock.txt` — 643 lượt
- `mg1-584-a-treatise-on-the-covenant-of-grace-reformed-theol-colquhoun.txt` — 615 lượt
- `mg1-270-the-works-of-octavius-winslow-winslow.txt` — 523 lượt
- `mg1-564-a-system-or-body-of-divinity-reformed-theology-ebo-leigh.txt` — 444 lượt
- `mg1-1197-the-true-doctrine-of-justification-reformed-theolo-burgess.txt` — 408 lượt
- `mg1-928-syntagma-theologiae-christianae-reformed-theology-polanus.txt` — 389 lượt
- `mg1-071-select-sermons-of-thomas-manton-sermons-ebook-manton.txt` — 384 lượt
- `mg1-413-the-works-of-thomas-brooks-collected-works-ebook-brooks.txt` — 352 lượt
- `013-commentary-romans-calvin.txt` — 349 lượt
- `mg1-868-practical-observations-upon-the-book-of-job-bible-caryl.txt` — 344 lượt
- `mg1-1155-the-sermons-of-the-rev-samuel-davies-sermons-ebook-davies.txt` — 343 lượt
- `mg1-1129-the-reasonable-service-of-god-reformed-theology-eb-a-brakel.txt` — 307 lượt
- `mg1-514-a-collection-of-the-promises-of-the-gospel-colquhoun.txt` — 283 lượt
- `mg1-241d-spurgeon-sermons-vol28-36.txt` — 280 lượt
- `mg1-587-a-treatise-on-the-law-and-the-gospel-reformed-theo-colquhoun.txt` — 273 lượt
- `calvin-commentary-isaiah-vol4.txt` — 263 lượt
- `manton-works-vol07.txt` — 251 lượt

## Tệp txt chưa có trong chỉ mục (10 ví dụ đầu)

- `003-marrow-modern-divinity-fisher.txt` (1,068,815 ký tự)
- `004-a-letter-on-the-death-of-a-child-plumer.txt` (10,007 ký tự)
- `007-charity-its-fruits-christian-love-as-edwards.txt` (636,977 ký tự)
- `012-a-beautiful-robe-plumer.txt` (10,816 ký tự)
- `027-angels-and-men-plumer.txt` (13,758 ký tự)
- `034-the-efficacy-of-the-sacraments-rutherford.txt` (14,170 ký tự)
- `046-four-hymns-and-some-religious-verses-warfield.txt` (11,733 ký tự)
- `055-light-from-heaven-discovering-fountaine-opened-sibbes.txt` (742,738 ký tự)
- `066-retvrning-backslider-commentarie-upon-whole-xiiii-sibbes.txt` (704,626 ký tự)
- `088-no-more-crying-ryle.txt` (18,488 ký tự)

## Không tự sửa

Không có mục nào ở trên được sửa tự động trong đợt này: thêm dòng đầu "AI, chưa duyệt" cho ~3.000 tệp cũ là thao tác hàng loạt, cần tái tạo cả `txt/` và trang đọc; thêm chân trang TRANSLATION STATUS đồng nghĩa khẳng định trạng thái mà script không biết. Các mục này chờ quyết định duyệt theo từng đợt.

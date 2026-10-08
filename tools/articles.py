# Executed from build-pages.py (uses: page, E, urls, SITE). Builds bai-viet/*.html SEO articles.
import os
os.makedirs("bai-viet", exist_ok=True)

ARTICLES = [
("sach-co-doc-hay-nen-doc",
 "10 cuốn sách Cơ Đốc hay nên đọc nhất (miễn phí)",
 "Gợi ý 10 cuốn sách Cơ Đốc hay nhất mọi thời đại: Spurgeon, Bunyan, Watson, Ryle và các tác phẩm Thanh giáo kinh điển. Đọc miễn phí bản dịch tiếng Việt.",
 """<p>Bạn đang tìm <b>sách Cơ Đốc hay</b> để đọc nhưng không biết bắt đầu từ đâu? Giữa hàng ngàn đầu sách, mười tác phẩm dưới đây đã đứng vững qua hàng thế kỷ, nuôi dưỡng đức tin của hàng triệu tín hữu — và tất cả đều có <b>bản dịch tiếng Việt đọc miễn phí</b> trong thư viện Reformed Vietnam.</p>
<h2>1. Tất Cả Bởi Ân Điển — Spurgeon</h2>
<p>Nếu chỉ được đọc một cuốn sách về Phúc Âm, hãy đọc cuốn này. Spurgeon trình bày con đường cứu rỗi một cách đơn sơ mà sâu sắc: <a href="/ban-dich/spurgeon-grace.html"><b>Tất Cả Bởi Ân Điển</b></a> là điểm khởi đầu lý tưởng cho người mới tìm hiểu đức tin.</p>
<h2>2. Ân Điển Dư Dật — Bunyan</h2>
<p>Tự truyện thuộc linh của tác giả <i>Thiên lộ lịch trình</i>, kể hành trình từ tuyệt vọng đến đức tin. <a href="/ban-dich/bunyan-grace.html"><b>Ân Điển Dư Dật</b></a> an ủi đặc biệt những ai đang vật lộn với sự bảo đảm cứu rỗi.</p>
<h2>3. Nghệ Thuật Sống Thỏa Lòng — Watson</h2>
<p>Thomas Watson dạy cách bằng lòng trong mọi hoàn cảnh — chủ đề gần gũi với người Việt. Đọc <a href="/ban-dich/watson-contentment.html"><b>Nghệ Thuật Sống Thỏa Lòng</b></a> để học bí quyết bình an thật.</p>
<h2>4. Sự Nên Thánh — Ryle</h2>
<p>Kinh điển về đời sống thánh khiết: tội lỗi là gì, vì sao phải chiến đấu với nó, và năng lực ở đâu. <a href="/ban-dich/ryle-holiness.html"><b>Sự Nên Thánh</b></a> của J. C. Ryle thực tiễn và đầy lòng thương xót.</p>
<h2>5. Cây Sậy Dập — Sibbes</h2>
<p>Được mệnh danh là cuốn sách êm dịu nhất của phong trào Thanh giáo, <a href="/ban-dich/sibbes-bruisedreed.html"><b>Cây Sậy Dập</b></a> (theo Ê-sai 42:3) an ủi những tâm hồn tan vỡ: Đấng Christ không dập tắt tim đèn còn khói.</p>
<h2>6–10. Đọc tiếp</h2>
<p><a href="/ban-dich/baxter-unconverted.html"><b>Lời Kêu Gọi Người Chưa Cải Đạo</b></a> (Baxter), <a href="/ban-dich/bonar-peace.html"><b>Con Đường Bình An Của Đức Chúa Trời</b></a> (Bonar), <a href="/ban-dich/owen-mort.html"><b>Giết Chết Tội Lỗi</b></a> (Owen), <a href="/ban-dich/burroughs-contentment.html"><b>Báu Vật Hiếm: Sự Thỏa Lòng</b></a> (Burroughs) và <a href="/ban-dich/brooks-remedies.html"><b>Phương Thuốc Quý Chống Mưu Chước Sa-tan</b></a> (Brooks) hoàn tất danh sách. Xem thêm theo <a href="/chu-de/">chủ đề</a> hoặc khám phá <a href="/tieng-viet.html">toàn bộ sách tiếng Việt</a>.</p>"""),

("than-hoc-cai-chanh-la-gi",
 "Thần học Cải Chánh là gì? Giải thích đơn giản cho người mới",
 "Thần học Cải Chánh là gì? Tìm hiểu 5 Sola, nguồn gốc cuộc Cải Chánh, và những điểm khác biệt cốt lõi với các truyền thống khác. Bài viết dễ hiểu cho người Việt mới tìm hiểu.",
 """<p><b>Thần học Cải Chánh</b> (Reformed theology) là dòng thần học bắt nguồn từ cuộc Cải Chánh thế kỷ 16 qua Luther, Calvin, Knox và được hệ thống hóa bởi các nhà Thanh giáo. Nhiều người Việt nghe đến 'Cải Chánh' nhưng chưa rõ nó dạy gì — bài viết này giải thích đơn giản.</p>
<h2>Năm Sola — trái tim của Cải Chánh</h2>
<p>Toàn bộ thần học Cải Chánh có thể tóm gọn trong <b>năm Sola</b>: <i>Sola Scriptura</i> (chỉ Kinh Thánh), <i>Sola Fide</i> (chỉ đức tin), <i>Sola Gratia</i> (chỉ ân điển), <i>Solus Christus</i> (chỉ Đấng Christ), <i>Soli Deo Gloria</i> (chỉ vinh hiển Đức Chúa Trời). Nghĩa là: Kinh Thánh là thẩm quyền tối cao, con người được cứu chỉ bởi ân điển qua đức tin nơi Đấng Christ, mọi vinh hiển thuộc về Đức Chúa Trời.</p>
<h2>Những điểm nhấn đặc trưng</h2>
<p>Thần học Cải Chánh nhấn mạnh <b>chủ quyền tuyệt đối của Đức Chúa Trời</b> trên mọi sự kể cả sự cứu rỗi (xem chuyên mục <a href="/chu-de/tien-dinh.html">tiền định</a>), <b>thần học giao ước</b> (<a href="/chu-de/giao-uoc.html">giao ước và tín điều</a>), và đời sống thánh khiết biết ơn đáp lại ân điển (<a href="/chu-de/nen-thanh.html">nên thánh</a>).</p>
<h2>Đọc gì để hiểu sâu hơn?</h2>
<p>Bắt đầu với <a href="/ban-dich/berkhof-summary.html"><b>Tóm Tắt Giáo Lý Cơ Đốc</b></a> của Berkhof — giáo trình hệ thống súc tích nhất. Muốn hiểu lịch sử, đọc <a href="/ban-dich/knox-history.html"><b>Lịch Sử Cải Chánh Scotland</b></a> của Knox. Muốn thấy tinh thần Cải Chánh đối diện thờ hình tượng, đọc <a href="/ban-dich/calvin-relics.html"><b>Luận Về Di Vật</b></a> của Calvin — ngắn mà sắc bén.</p>"""),

("nam-diem-tulip",
 "5 điểm của chủ nghĩa Calvin (TULIP) là gì? Giải thích dễ hiểu",
 "TULIP là gì? Giải thích 5 điểm của chủ nghĩa Calvin: tội lỗi hoàn toàn, chọn lựa vô điều kiện, chuộc tội giới hạn, ân điển không cưỡng lại được, sự bền đỗ của thánh đồ. Kèm sách đọc thêm miễn phí.",
 """<p><b>TULIP</b> là chữ viết tắt của năm điểm giáo lý được Hội nghị Dort (1618–1619) xác nhận để đáp lại thuyết Arminius. Đây là tóm tắt cốt lõi của <b>chủ nghĩa Calvin về sự cứu rỗi</b>:</p>
<h2>1. T — Total Depravity (Tội lỗi hoàn toàn)</h2>
<p>Con người sa ngã hoàn toàn: mọi phương diện — trí, tình cảm, ý chí — đều bị tội lỗi làm ô uế, nên không ai tự mình tìm kiếm Đức Chúa Trời (Rô-ma 3:10–12).</p>
<h2>2. U — Unconditional Election (Chọn lựa vô điều kiện)</h2>
<p>Trước khi sáng thế, Đức Chúa Trời đã chọn một số người để cứu — không dựa trên điều kiện nào nơi họ, mà hoàn toàn theo ý muốn tốt lành của Ngài (Ê-phê-sô 1:4–5).</p>
<h2>3. L — Limited Atonement (Chuộc tội giới hạn)</h2>
<p>Sự chết của Đấng Christ chắc chắn cứu được tất cả những ai Cha đã ban cho Ngài (Giăng 6:37–39). Hiệu quả của sự chuộc tội không thất bại.</p>
<h2>4. I — Irresistible Grace (Ân điển không cưỡng lại được)</h2>
<p>Khi Đức Thánh Linh kêu gọi một người cách hiệu quả, người ấy chắc chắn đáp lại bằng đức tin — ân điển Chúa không bao giờ vô hiệu.</p>
<h2>5. P — Perseverance of the Saints (Sự bền đỗ của thánh đồ)</h2>
<p>Những ai thật sự được cứu sẽ bền đỗ đến cuối cùng, vì chính Đức Chúa Trời gìn giữ họ (Phi-líp 1:6).</p>
<h2>Đọc sâu hơn</h2>
<p>Cuốn <a href="/ban-dich/boettner-predestination.html"><b>Giáo Lý Cải Chánh Về Tiền Định</b></a> của Boettner giải thích TULIP rõ ràng và có hệ thống nhất cho độc giả hiện đại. Muốn đào sâu triết-thần, đọc <a href="/ban-dich/edwards-will.html"><b>Tự Do Của Ý Chí</b></a> của Edwards. Xem thêm <a href="/chu-de/tien-dinh.html">chuyên mục tiền định</a>.</p>"""),

("xung-cong-binh-boi-duc-tin-la-gi",
 "Sự xưng công chính bởi đức tin là gì? Giáo lý trung tâm của Cải Chánh",
 "Xưng công chính bởi đức tin là gì? Giải thích giáo lý trung tâm của cuộc Cải Chánh: được kể là công chính chỉ bởi ân điển qua đức tin, không bởi việc làm. Kèm sách đọc miễn phí.",
 """<p><b>Sự xưng công chính bởi đức tin</b> là giáo lý mà Luther gọi là 'điều mà Hội Thánh đứng hay ngã theo đó'. Hiểu đơn giản: <b>xưng công chính</b> nghĩa là Đức Chúa Trời <i>kể</i> tội nhân là công chính — không phải vì họ xứng đáng, mà vì công chính của Đấng Christ được <i>quy gán</i> cho họ khi họ tin.</p>
<h2>Ba chữ 'chỉ' quyết định</h2>
<p>Cải Chánh dạy con người được xưng công chính <b>chỉ bởi ân điển</b> (không do công đức), <b>chỉ qua đức tin</b> (không bởi việc làm), <b>chỉ trong Đấng Christ</b> (không nhờ ai khác). Rô-ma 3:28: 'người ta được xưng công chính bởi đức tin, chẳng phải bởi việc làm theo luật pháp.'</p>
<h2>Vì sao giáo lý này quan trọng?</h2>
<p>Nếu sự cứu rỗi phụ thuộc dù chỉ một phần vào việc làm của ta, thì không ai có sự bảo đảm — vì không ai làm đủ tốt. Xưng công chính bởi đức tin ban cho tín hữu <b>sự bình an chắc chắn</b>: địa vị trước mặt Chúa không lay chuyển theo cảm xúc hay thành tích mỗi ngày.</p>
<h2>Sách nên đọc</h2>
<p><a href="/ban-dich/owen-justification.html"><b>Giáo Lý Xưng Công Chính Bởi Đức Tin</b></a> của John Owen là luận thuyết đầy đủ và sâu sắc nhất về đề tài này. Ngắn gọn hơn: <a href="/ban-dich/hooker-just.html"><b>Luận Về Sự Xưng Công Chính</b></a> của Richard Hooker và <a href="/ban-dich/spurgeon-grace.html"><b>Tất Cả Bởi Ân Điển</b></a> của Spurgeon. Xem thêm <a href="/chu-de/xung-cong-binh.html">chuyên mục xưng công bình</a>.</p>"""),

("sach-thanh-giao-hay",
 "Sách Thanh giáo hay nên đọc: 8 tác phẩm kinh điển",
 "Tuyển 8 cuốn sách Thanh giáo (Puritan) hay nhất: Owen, Watson, Flavel, Brooks, Bunyan. Bản dịch tiếng Việt đọc miễn phí, kèm hướng dẫn chọn sách theo nhu cầu.",
 """<p><b>Thanh giáo (Puritan)</b> là phong trào cải cách Hội Thánh Anh thế kỷ 16–17, để lại kho tàng sách vở đồ sộ về đời sống thuộc linh thực tiễn. Người Việt thường hỏi: nên đọc sách Thanh giáo nào trước? Dưới đây là 8 gợi ý theo nhu cầu.</p>
<h2>Muốn chiến đấu với tội lỗi</h2>
<p><a href="/ban-dich/owen-mort.html"><b>Giết Chết Tội Lỗi</b></a> (Owen) là luận văn kinh điển nhất về đề tài này; đọc kèm <a href="/ban-dich/owen-temptation.html"><b>Về Sự Cám Dỗ</b></a>. Muốn nhận diện mưu chước ma quỷ, đọc <a href="/ban-dich/brooks-remedies.html"><b>Phương Thuốc Quý Chống Mưu Chước Sa-tan</b></a> (Brooks).</p>
<h2>Muốn học thần học có hệ thống</h2>
<p><a href="/ban-dich/watson-bodyofdivinity.html"><b>Thân Thể Thần Học</b></a> của Thomas Watson giảng giải toàn bộ giáo lý theo từng câu Hỏi-Đáp Westminster — vừa sâu vừa ấm áp, rất hợp để học theo nhóm.</p>
<h2>Muốn chiêm ngưỡng Đấng Christ</h2>
<p><a href="/ban-dich/flavel-methodofgrace.html"><b>Phương Pháp Của Ân Điển</b></a> và <a href="/ban-dich/flavel-fountainoflife.html"><b>Nguồn Sống Mở Ra</b></a> của Flavel đưa độc giả đến gần Đấng Christ hơn qua từng trang.</p>
<h2>Muốn an ủi trong hoạn nạn</h2>
<p><a href="/ban-dich/bunyan-grace.html"><b>Ân Điển Dư Dật</b></a> (Bunyan) và <a href="/ban-dich/watson-cordial.html"><b>Liều Thuốc Bổ Thiêng Liêng</b></a> (Watson, về Rô-ma 8:28) là thuốc bổ cho tâm hồn đau thương. Duyệt thêm theo <a href="/a/thomas-watson.html">tác giả Thomas Watson</a> hoặc <a href="/a/john-owen.html">John Owen</a>.</p>
<h2>Đọc sách Thanh giáo thế nào cho hiệu quả?</h2>
<p>Văn Thanh giáo thế kỷ 17 đôi khi dài dòng với độc giả hiện đại. Bí quyết là đọc chậm, mỗi ngày một đoạn ngắn, và dừng lại suy ngẫm mỗi khi gặp một chân lý chạm đến lòng. Đừng cố đọc cho xong, hãy đọc để được biến đổi. Nhiều cuốn trong thư viện có bản <b>dịch tiếng Việt hiện đại, dễ đọc</b> — bạn không cần vật lộn với tiếng Anh cổ. Hãy bắt đầu với một cuốn mỏng như <a href="/ban-dich/sibbes-bruisedreed.html"><b>Cây Sậy Dập</b></a> trước khi bước vào những luận thuyết dài của Owen.</p>"""),

("doc-kinh-thanh-moi-ngay",
 "Đọc Kinh Thánh mỗi ngày như thế nào? 5 bí quyết thực tế",
 "Hướng dẫn đọc Kinh Thánh mỗi ngày hiệu quả: 5 bí quyết thực tế cho người bận rộn, kèm tài liệu tĩnh nguyện hằng ngày miễn phí (Spurgeon, Kuyper).",
 """<p>Nhiều tín hữu muốn <b>đọc Kinh Thánh mỗi ngày</b> nhưng bỏ cuộc sau vài tuần vì không biết bắt đầu từ đâu hoặc thấy khô khan. Năm bí quyết dưới đây đã giúp vô số người duy trì thói quen này suốt đời.</p>
<h2>1. Đặt giờ cố định và bắt đầu nhỏ</h2>
<p>Chọn một khung giờ không ai quấy rầy — thường là buổi sáng — và bắt đầu chỉ 10–15 phút. Thói quen nhỏ bền hơn quyết tâm lớn.</p>
<h2>2. Đọc có kế hoạch, không đọc tùy hứng</h2>
<p>Dùng lịch đọc Kinh Thánh trong một năm, hoặc đọc lần lượt từng sách. Đọc tùy hứng dễ bỏ dở giữa chừng.</p>
<h2>3. Đọc kèm một cuốn tĩnh nguyện</h2>
<p>Một đoạn suy ngẫm ngắn mỗi ngày giúp Lời Chúa thấm sâu. Gợi ý: <a href="/ban-dich/spurgeon-morningevening.html"><b>Buổi Sáng Và Buổi Chiều</b></a> của Spurgeon (732 bài cho cả năm), <a href="/ban-dich/kuyper-neartogod.html"><b>Gần Bên Chúa</b></a> của Kuyper (110 bài), hoặc <a href="/ban-dich/daily-meditations.html"><b>Suy Ngẫm Và Cầu Nguyện Hằng Ngày</b></a>.</p>
<h2>4. Cầu nguyện trước và sau khi đọc</h2>
<p>Xin Đức Thánh Linh mở mắt trước khi đọc (Thi Thiên 119:18), và đáp lại bằng lời cầu nguyện sau khi đọc. Đọc Kinh Thánh là cuộc trò chuyện, không phải bài tập.</p>
<h2>5. Ghi chép một điều áp dụng</h2>
<p>Mỗi ngày viết ra một điều Chúa dạy và một việc sẽ làm theo. Sổ tay thuộc linh biến kiến thức thành đời sống. Tìm hiểu thêm tại <a href="/chu-de/kinh-thanh.html">chuyên mục Kinh Thánh</a>.</p>"""),

("phan-biet-tin-lanh-cong-giao",
 "Phân biệt Tin Lành và Công Giáo: 5 khác biệt cốt lõi",
 "Tin Lành và Công Giáo khác nhau ở đâu? 5 khác biệt cốt lõi về thẩm quyền Kinh Thánh, sự cứu rỗi, vai trò Hội Thánh. Bài viết trung thực, dễ hiểu cho người Việt.",
 """<p>Ở Việt Nam, nhiều người vẫn nhầm lẫn <b>Tin Lành và Công Giáo</b>. Cả hai đều xưng mình theo Đấng Christ, nhưng có những khác biệt thần học cốt lõi bắt nguồn từ cuộc Cải Chánh thế kỷ 16. Bài viết trình bày trung thực để bạn đọc tự tìm hiểu.</p>
<h2>1. Thẩm quyền tối cao</h2>
<p>Tin Lành: <b>chỉ Kinh Thánh</b> (<i>Sola Scriptura</i>) là thẩm quyền tuyệt đối. Công Giáo: Kinh Thánh cộng với truyền thống Hội Thánh và huấn quyền của giáo hoàng.</p>
<h2>2. Con đường cứu rỗi</h2>
<p>Tin Lành: được cứu <b>chỉ bởi ân điển qua đức tin</b>, không bởi việc làm hay công đức (<a href="/chu-de/xung-cong-binh.html">xưng công bình</a>). Công Giáo: ân điển cộng với các bí tích và việc lành.</p>
<h2>3. Vai trò của Hội Thánh và chức sắc</h2>
<p>Tin Lành nhấn mạnh <b>chức tư tế của mọi tín hữu</b>: ai cũng có thể trực tiếp đến với Chúa qua Đấng Christ, không cần trung gian. Công Giáo coi linh mục có vai trò trung gian trong các bí tích.</p>
<h2>4. Ma-ri và các thánh</h2>
<p>Tin Lành kính trọng Ma-ri nhưng <b>chỉ thờ phượng Đức Chúa Trời</b> và chỉ cầu nguyện nhân danh Đấng Christ. Công Giáo cầu xin Ma-ri và các thánh chuyển cầu.</p>
<h2>5. Luyện ngục và các thực hành khác</h2>
<p>Tin Lành không chấp nhận giáo lý luyện ngục, vì sự chuộc tội của Đấng Christ đã trọn vẹn một lần đủ cả (Hê-bơ-rơ 10:14).</p>
<h2>Tìm hiểu thêm</h2>
<p>Đọc <a href="/ban-dich/calvin-relics.html"><b>Luận Về Di Vật</b></a> của Calvin để hiểu lập luận Cải Chánh, <a href="/ban-dich/knox-history.html"><b>Lịch Sử Cải Chánh Scotland</b></a> để thấy bối cảnh lịch sử, và <a href="/chu-de/giao-uoc.html">chuyên mục thần học Cải Chánh</a>.</p>"""),

("an-dien-la-gi",
 "Ân điển là gì? Ý nghĩa sâu sắc nhất của Phúc Âm",
 "Ân điển là gì? Giải thích ý nghĩa ân điển của Đức Chúa Trời trong Kinh Thánh: ân điển cứu rỗi, ân điển ban cho hằng ngày, và đời sống đáp lại ân điển. Kèm sách đọc miễn phí.",
 """<p><b>Ân điển</b> là chữ đẹp nhất trong Kinh Thánh: <i>ơn nhưng không của Đức Chúa Trời ban cho kẻ không xứng đáng</i>. Hiểu đúng ân điển sẽ biến đổi toàn bộ đời sống đức tin của bạn.</p>
<h2>Ân điển cứu rỗi</h2>
<p>'Ấy là nhờ ân điển, bởi đức tin, mà anh em được cứu, điều đó không phải đến từ anh em, bèn là sự ban cho của Đức Chúa Trời' (Ê-phê-sô 2:8). Ân điển nghĩa là: Chúa làm <b>tất cả</b>, ta chỉ <b>nhận lãnh</b> bằng đức tin. Không ai 'đủ tốt' để được cứu — và đó chính là tin mừng.</p>
<h2>Ân điển ban cho hằng ngày</h2>
<p>Ân điển không chỉ cho lúc tin Chúa, mà nuôi ta mỗi ngày: sức mới buổi sáng (Ca Thương 3:22–23), sự tha thứ khi vấp ngã (1 Giăng 1:9), năng lực để nên thánh (Tít 2:11–12). Người hiểu ân điển không sống buông thả, mà sống biết ơn.</p>
<h2>Đáp lại ân điển thế nào?</h2>
<p>Đáp lại đúng đắn không phải là 'trả ơn' bằng việc làm để được cứu, mà là <b>sống thánh khiết vì đã được cứu</b> — vâng lời trong tình yêu, phục vụ trong vui mừng, và rao truyền ân điển cho người khác.</p>
<h2>Sách nên đọc</h2>
<p><a href="/ban-dich/spurgeon-grace.html"><b>Tất Cả Bởi Ân Điển</b></a> (Spurgeon) là cuốn sách hay nhất để bắt đầu. <a href="/ban-dich/edwards-grace.html"><b>Luận Về Ân Điển</b></a> (Edwards) định nghĩa sâu sắc. <a href="/ban-dich/bonar-peace.html"><b>Con Đường Bình An</b></a> (Bonar) dẫn người mới tin đến sự bình an chắc chắn. Xem thêm <a href="/chu-de/an-dien-tin-lanh.html">chuyên mục ân điển và Phúc Âm</a>.</p>"""),
]

for _slug, _title, _desc, _body in ARTICLES:
    _path = f"bai-viet/{_slug}.html"
    _ld = {"@context": "https://schema.org", "@type": "Article",
           "headline": _title, "inLanguage": "vi",
           "author": {"@type": "Organization", "name": "Reformed Vietnam", "url": SITE},
           "url": f"{SITE}/{_path}", "datePublished": "2026-10-08"}
    _html = (f'<p class="m"><a href="/bai-viet/">← Tất cả bài viết</a> · <a href="/tieng-viet.html">Sách tiếng Việt</a></p>\n'
             f'<h1>{E(_title)}</h1>\n{_body}\n'
             f'<hr><p><i>Bài viết thuộc thư viện Reformed Vietnam. Tìm sách đọc thêm tại <a href="/tieng-viet.html">Sách tiếng Việt</a> hoặc <a href="/chu-de/">học theo chủ đề</a>.</i></p>')
    open(_path, "w", encoding="utf-8").write(page(_title + " | Reformed Vietnam", _desc, _path, _html, _ld))
    urls.append(_path)

_hub = ('<h1>Bài viết</h1><p>Các bài viết ngắn giúp bạn tìm hiểu đức tin Cải Chánh: sách nên đọc, giáo lý căn bản và đời sống hằng ngày. Mỗi bài đều dẫn đến sách đọc miễn phí trong thư viện.</p><ul>' +
        "".join(f'<li><a href="/bai-viet/{s}.html"><b>{E(t)}</b></a><br><small>{E(d)}</small></li>' for s, t, d, _ in ARTICLES) +
        '</ul><p><a class="btn" href="/">Về thư viện</a></p>')
open("bai-viet/index.html", "w", encoding="utf-8").write(page("Bài viết về đức tin Cải Chánh | Reformed Vietnam",
    "Các bài viết ngắn về đức tin Cải Chánh: sách Cơ Đốc hay nên đọc, TULIP, xưng công chính bởi đức tin, ân điển, đọc Kinh Thánh mỗi ngày.",
    "bai-viet/index.html", _hub))
urls.append("bai-viet/index.html")
print("articles:", len(ARTICLES))

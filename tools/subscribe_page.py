# Executed from build-pages.py. Builds nhan-bai.html with the MailerLite embedded form.
_body = '''<h1>Nhận bài qua email</h1>
<p>Mỗi tuần một thư ngắn: một trích dẫn Cải Chánh, một cuốn sách để đọc và một câu Kinh Thánh để suy ngẫm. Miễn phí, bạn có thể hủy bất cứ lúc nào, và chúng tôi không chia sẻ email của bạn.</p>
<div class="ml-embedded" data-form="nlPLmR"></div>
<script>(function(w,d,e,u,f,l,n){w[f]=w[f]||function(){(w[f].q=w[f].q||[]).push(arguments);},l=d.createElement(e),l.async=1,l.src=u,n=d.getElementsByTagName(e)[0],n.parentNode.insertBefore(l,n);})(window,document,'script','https://assets.mailerlite.com/js/universal.js','ml');ml('account','2675773');</script>
<p class="m"><small>Dịch vụ gửi thư: MailerLite. Email chỉ dùng để gửi bản tin này.</small></p>'''
open("nhan-bai.html", "w", encoding="utf-8").write(page("Nhận bài qua email | Reformed Vietnam", "Đăng ký nhận thư hằng tuần: trích dẫn Cải Chánh, sách nên đọc và câu Kinh Thánh. Miễn phí.", "nhan-bai.html", _body))
urls.append("nhan-bai.html")

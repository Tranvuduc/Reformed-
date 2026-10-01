# Bản dịch tay (Claude / Gemini)

Mỗi sách = một file `.txt` UTF-8 trong thư mục này, và một dòng trong `index.json`:

```json
{"id":"knox/prayer","file":"knox-prayer.txt","title":"Luận về Sự cầu nguyện","orig":"A Treatise on Prayer","author":"John Knox","by":"Claude","reviewed":false}
```

- `reviewed`: đổi thành `true` chỉ khi mục sư đã duyệt giáo lý. Khi đó nhãn "bản dịch AI chưa duyệt" được thay bằng "đã được mục sư xem lại".
- Dòng chương bắt đầu bằng `Chương`, `Phần` hoặc `Lời nói đầu`. Các dòng `THUẬT NGỮ MỚI:` và `CẦN DUYỆT:` cuối mỗi chương không hiện công khai, được gom vào `review/<tên-file>.txt`.
- Chạy `python3 tools/build-pages.py` để dựng trang `ban-dich/<tên-file>.html`.

# Sách nói giọng tự nhiên (tạo sẵn)
1. Azure Speech (gói F0 miễn phí ≈500K ký tự/tháng) → tạo khóa; đặt secret `AZURE_SPEECH_KEY`, `AZURE_SPEECH_REGION` trong GitHub (hoặc biến môi trường trên máy).
2. `python3 tools/tts_gen.py do-you-pray --dry-run` (đếm ký tự) rồi chạy thật; hoặc Actions → "Tạo sách nói (Azure)".
3. Tải `tts_out/<slug>/` lên nơi lưu trữ có link công khai (Cloudflare R2, repo GitHub Pages riêng...).
4. Sửa `tts/index.json`: `{"base":"https://.../","books":{"do-you-pray":30}}` (số = số đoạn). Trình đọc sẽ có giọng "Giọng tự nhiên (tạo sẵn)" cho sách đó, lỗi thì tự quay về giọng cũ.

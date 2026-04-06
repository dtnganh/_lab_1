# Ngày 1 — Bài Tập & Phản Ánh
## Nền Tảng LLM API | Phiếu Thực Hành

**Thời lượng:** 1:30 giờ  
**Cấu trúc:** Lập trình cốt lõi (60 phút) → Bài tập mở rộng (30 phút)

---

## Phần 1 — Lập Trình Cốt Lõi (0:00–1:00)

Chạy các ví dụ trong Google Colab tại: https://colab.research.google.com/drive/172zCiXpLr1FEXMRCAbmZoqTrKiSkUERm?usp=sharing

Triển khai tất cả TODO trong `template.py`. Chạy `pytest tests/` để kiểm tra tiến độ.

**Điểm kiểm tra:** Sau khi hoàn thành 4 nhiệm vụ, chạy:
```bash
python template.py
```
Bạn sẽ thấy output so sánh phản hồi của GPT-4o và GPT-4o-mini.

---

## Phần 2 — Bài Tập Mở Rộng (1:00–1:30)

### Bài tập 2.1 — Độ Nhạy Của Temperature
Gọi `call_openai` với các giá trị temperature 0.0, 0.5, 1.0 và 1.5 sử dụng prompt **"Hãy kể cho tôi một sự thật thú vị về Việt Nam."**

**Bạn nhận thấy quy luật gì qua bốn phản hồi?** (2–3 câu)
> Temperature thấp thì câu trả lời tập trung vào các số liệu chính xác và có cấu trúc chặt chẽ. Khi tăng temperature lên thì nội dung diễn đạt sáng tạo hơn nhưng đôi khi không chính xác.

**Bạn sẽ đặt temperature bao nhiêu cho chatbot hỗ trợ khách hàng, và tại sao?**
> Em sẽ đặt temperature trong khoảng 0.2 đến 0.4. Lý do là vì chatbot hỗ trợ khách hàng cần ưu tiên sự chính xác, nhất quán và không nên đưa ra các thông tin sai lệch.

---

### Bài tập 2.2 — Đánh Đổi Chi Phí
Xem xét kịch bản: 10.000 người dùng hoạt động mỗi ngày, mỗi người thực hiện 3 lần gọi API, mỗi lần trung bình ~350 token.

**Ước tính xem GPT-4o đắt hơn GPT-4o-mini bao nhiêu lần cho workload này:**
> Tổng lưu lượng token mỗi ngày là 10.500.000 token. Với đơn giá hiện tại ($0.010 so với $0.0006 cho mỗi 1K token), chi phí cho GPT-4o là khoảng $105/ngày, trong khi GPT-4o-mini chỉ tốn khoảng $6.3/ngày. Như vậy, GPT-4o đắt hơn GPT-4o-mini khoảng 16.6 lần.

**Mô tả một trường hợp mà chi phí cao hơn của GPT-4o là xứng đáng, và một trường hợp GPT-4o-mini là lựa chọn tốt hơn:**
> GPT-4o xứng đáng khi cần xử lý các tác vụ đòi hỏi tư duy logic cao như viết code phức tạp, giải toán hoặc trích xuất thông tin rắc rối từ tài liệu chuyên ngành. Ngược lại, GPT-4o-mini là lựa chọn tốt cho các tác vụ đơn giản, lặp đi lặp lại.

---

### Bài tập 2.3 — Trải Nghiệm Người Dùng với Streaming
**Streaming quan trọng nhất trong trường hợp nào, và khi nào thì non-streaming lại phù hợp hơn?** (1 đoạn văn)
> Streaming quan trọng nhất khi AI cần trả lời một đoạn văn dài hoặc viết nội dung sáng tạo, giúp giảm cảm giác chờ đợi bằng cách cho người dùng đọc phần đầu ngay khi AI đang viết tiếp. Ngược lại, non-streaming phù hợp hơn khi kết quả của AI được dùng để xử lý logic nội bộ (ví dụ: trả về dữ liệu định dạng JSON để nạp vào database) hoặc khi câu trả lời cực ngắn, nơi mà việc hiển thị từng ký tự không mang lại giá trị trải nghiệm rõ rệt.


## Danh Sách Kiểm Tra Nộp Bài
- [ ] Tất cả tests pass: `pytest tests/ -v`
- [ ] `call_openai` đã triển khai và kiểm thử
- [ ] `call_openai_mini` đã triển khai và kiểm thử
- [ ] `compare_models` đã triển khai và kiểm thử
- [ ] `streaming_chatbot` đã triển khai và kiểm thử
- [ ] `retry_with_backoff` đã triển khai và kiểm thử
- [ ] `batch_compare` đã triển khai và kiểm thử
- [ ] `format_comparison_table` đã triển khai và kiểm thử
- [ ] `exercises.md` đã điền đầy đủ
- [ ] Sao chép bài làm vào folder `solution` và đặt tên theo quy định 

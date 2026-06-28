# Chương 04: Quy trình quay Video Demo sản phẩm dài 2 phút hút khách

## 1. Deep Dive (Phân tích chuyên sâu)

### Quy tắc Vàng: 2 Phút Vàng Ngọc (The 2-Minute Demo Rule)
Khách hàng B2B vô cùng bận rộn. Nếu video demo của bạn dài 10 phút, bắt đầu bằng việc giải thích code Python dòng này dòng kia dòng nọ, họ sẽ tắt video sau 10 giây đầu tiên.
Kịch bản video demo tiêu chuẩn 120 giây của một Kỹ sư AI Automation chuyên nghiệp:
- **0s - 30s (WOW Factor)**: Đi thẳng vào kết quả cuối cùng. Hiển thị màn hình biểu mẫu gửi đi, bấm nút và hiển thị tin nhắn Telegram báo về tức thì cùng điểm số AI chấm điểm. Nói: *"Hệ thống tự động chấm điểm lead chạy trong 3 giây..."*.
- **30s - 90s (Luồng Nghiệp Vụ - Business Flow)**: Giải thích luồng công việc diễn ra thế nào ở giao diện n8n hoặc FastAPI. Cho thấy dữ liệu được ghi nhận vào Google Sheets hay CRM tự động ra sao.
- **90s - 120s (Kỹ thuật tối giản)**: Lướt nhanh qua cấu trúc code hoặc sơ đồ kiến trúc để chứng minh bạn làm chủ công nghệ thực sự.

### Kỹ thuật quay video chuyên nghiệp
1. **Độ phân giải và Zoom**: Đảm bảo màn hình quay rõ ràng, zoom to màn hình dòng lệnh và giao diện (ít nhất 125%) để người xem trên điện thoại di động vẫn có thể đọc được chữ.
2. **Giọng nói thuyết minh**: Nói rõ ràng, tự tin, tập trung vào từ khóa giá trị nghiệp vụ (Ví dụ: "tiết kiệm thời gian", "bảo mật dữ liệu", "tự động hóa hoàn toàn").
3. **Chuẩn bị dữ liệu test đẹp**: Sử dụng các tên giả lập thực tế, mô tả dự án hấp dẫn, tránh nhập các chữ vô nghĩa như "test1", "abc", "xyz".

---

## 2. Demo: Kịch bản thuyết minh Video Demo của AI CRM Agent

### Mục tiêu
Cung cấp kịch bản chi tiết (Storyboard) từng giây giúp bạn tự tin nói khi quay màn hình demo dự án CRM.

### Bảng Kịch bản Thuyết minh (Storyboard)
- **[00:00 - 00:15]**: (Mở màn hình Form đăng ký của Web). *"Xin chào các bạn, đây là hệ thống tự động tiếp nhận và thẩm định khách hàng tiềm năng bằng AI. Giả sử tôi là khách hàng có ngân sách 5,000 USD đăng ký tư vấn..."* (Bấm submit form).
- **[00:15 - 00:40]**: (Chuyển sang màn hình Telegram chat bot). *"Ngay lập tức, trong vòng chưa đầy 3 giây, bot Telegram của đội ngũ Sales đã nhận được thông báo khẩn cấp. AI đã đọc hiểu mô tả yêu cầu, chấm điểm lead này đạt 85/100 điểm và phân loại đây là khách hàng Qualified cần liên hệ ngay."*
- **[00:40 - 01:10]**: (Chuyển sang màn hình n8n workflow). *"Quy trình này hoạt động tự động thông qua nhạc trưởng n8n. Webhook tiếp nhận sự kiện, gọi sang API FastAPI bảo mật cục bộ của chúng tôi để xử lý."*
- **[01:10 - 01:45]**: (Chuyển sang màn hình database/Google sheets). *"Đồng thời, dữ liệu đã được lưu trữ bền vững vào cơ sở dữ liệu để phục vụ báo cáo. Lead không đủ điều kiện ngân sách sẽ tự động được lọc riêng để chăm sóc sau."*
- **[01:45 - 02:00]**: (Mở sơ đồ kiến trúc). *"Hệ thống được đóng gói hoàn toàn bằng Docker, sẵn sàng triển khai lên VPS của doanh nghiệp chỉ trong 5 phút. Cảm ơn các bạn đã theo dõi."*

---

## 3. Mini Project

### Bài tập 1: Lập kịch bản quay Video Demo sản phẩm AI (Mức độ: Trung bình)
* **Đề bài**: Hãy soạn thảo một kịch bản chi tiết dài 2 phút để quay video giới thiệu (Demo Video) cho ứng dụng AI Agent của bạn. Kịch bản phải nêu rõ: Phần mở đầu (giới thiệu nỗi đau khách hàng), Phần trọng tâm (trình diễn tính năng cốt lõi của AI), và Phần kêu gọi hành động (CTA).
* **Tài liệu sườn mẫu (`demo_script.md`)**:
```markdown
# Kịch bản Video Demo: AI Invoice Processor (Thời lượng: 120 giây)

* **0 - 20s: Khởi động (The Pain)**: 
  - Quay cảnh màn hình đống hóa đơn PDF ngập tràn.
  - Lời thoại: "Bạn mệt mỏi vì phải nhập liệu hóa đơn thủ công hàng giờ liền?"
* **20 - 90s: Demo Tính năng (The Solution)**:
  - Thao tác kéo thả file hóa đơn vào ứng dụng.
  - Cho người xem thấy AI tự động điền dữ liệu vào bảng Excel chính xác 100% trong 2 giây.
* **90 - 120s: Kêu gọi (CTA)**:
  - Hiển thị link GitHub dự án.
  - Lời thoại: "Hãy trải nghiệm ngay tại link bên dưới!"
```

### Bài tập 2: Thiết kế ảnh động GIF tương tác sản phẩm cho README (Mức độ: Khó)
* **Đề bài**: Hãy thực hiện quay lại màn hình thao tác sử dụng công cụ AI của bạn (dưới 15 giây), sau đó chuyển đổi video đó sang định dạng ảnh động `.gif` chất lượng cao, tối ưu dung lượng dưới 5MB để nhúng thẳng vào đầu trang README dự án.
* **Yêu cầu**: Học viên tự hoàn thành không có tài liệu mẫu.
* **Gợi ý triển khai (Workflow Hints)**:
  - Sử dụng các phần mềm quay màn hình miễn phí như OBS Studio, Loom hoặc GIPHY Capture.
  - Sử dụng công cụ chuyển đổi hoặc trang web Ezgif để tối ưu hóa màu sắc, giảm tốc độ khung hình (FPS xuống 10-12) nhằm nén dung lượng ảnh động.


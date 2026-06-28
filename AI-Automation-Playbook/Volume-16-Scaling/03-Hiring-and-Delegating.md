# Chương 03: Tuyển dụng, Kiểm thử năng lực & Ủy quyền lập trình

## 1. Deep Dive (Phân tích chuyên sâu)

### Bước chuyển mình từ Freelancer sang Agency Owner
Khi khối lượng công việc vượt quá 60 giờ/tuần, bạn phải tuyển dụng nhân sự hỗ trợ. Nếu không, chất lượng sản phẩm bàn giao cho khách hàng sẽ bắt đầu giảm sút nghiêm trọng.

Tuy nhiên, lập trình viên Junior thường thiếu kinh nghiệm thực chiến. Để ủy quyền hiệu quả mà không làm hỏng dự án:
1. **Thiết lập quy trình tuyển dụng dựa trên thực hành**: Bỏ qua các câu hỏi phỏng vấn lý thuyết mẹo. Hãy bắt ứng viên giải quyết 1 bài toán thực tế của Agency bạn (ví dụ: viết code parse hóa đơn bằng Pydantic) trong vòng 24h có trả phí nhẹ. Điều này giúp đánh giá chính xác: tốc độ code, phong cách đặt tên biến, cách xử lý lỗi và tính kỷ luật (đúng hạn).
2. **Quy tắc ủy quyền (Task Delegation)**: Giao việc kèm theo file SOP hướng dẫn rõ ràng. Junior Dev chỉ được phép code trên các nhánh phụ (Feature branches). Lead Engineer (là bạn) bắt buộc phải thực hiện Review Code trước khi cho phép gộp (Merge) vào nhánh Production.

---

## 2. Demo: Mẫu Bài kiểm tra năng lực tuyển dụng Junior Developer

### Mục tiêu
Cung cấp mẫu tài liệu bài test thực tế dùng để gửi cho ứng viên Junior Python/AI Developer để sàng lọc thực lực.

### Nội dung Bài Test (`developer_assessment.md`)
```markdown
# BÀI KIỂM TRA NĂNG LỰC: LẬP TRÌNH VIÊN PYTHON AI - ANTIGRAWITY AI

### 1. Yêu cầu bài toán (Task Specification)
Hãy viết một script Python hoàn chỉnh thực hiện các yêu cầu sau:
- Đọc file cấu hình JSON chứa thông tin cấu hình API.
- Gọi API của OpenAI sử dụng thư viện `openai` bản mới nhất (v1.0.0+) để tóm tắt một đoạn văn bản thô được cung cấp sẵn.
- Trích xuất dữ liệu tóm tắt thành định dạng có cấu trúc sử dụng Pydantic gồm: `summary` (str) và `keywords` (List of strings).
- Bắt tất cả các lỗi ngoại lệ (connection error, rate limit) và ghi log chi tiết ra file `app.log` bằng thư viện `logging` của Python.

### 2. Tiêu chí đánh giá (Evaluation Criteria)
- **Tính đúng đắn**: Mã nguồn chạy thành công không sinh lỗi (50%).
- **Tác phong code**: Đặt tên biến rõ nghĩa, cấu trúc thư mục gọn gàng, viết docstring đầy đủ (20%).
- **Xử lý ngoại lệ**: Bắt lỗi và ghi log chuyên nghiệp thay vì dùng print (20%).
- **Thời gian hoàn thành**: Nộp bài trong vòng 24 giờ kể từ khi nhận đề (10%).
```

---

## 3. Mini Project

### Bài tập 1: Soạn tin tuyển dụng Kỹ sư AI Automation thực tập (Mức độ: Trung bình)
* **Đề bài**: Soạn thảo một bản tin tuyển dụng (Job Description - JD) cho vị trí Thực tập sinh lập trình viên AI Automation (Intern AI Engineer) cho Agency của bạn. JD cần nêu rõ: Mô tả công việc, Yêu cầu kỹ thuật bắt buộc và Quyền lợi.
* **Tài liệu sườn mẫu (`intern_jd.md`)**:
```markdown
# Tuyển dụng: Thực tập sinh AI Automation Engineer (Intern)

### 1. Mô tả công việc
* Tham gia hỗ trợ thiết kế các chatbot RAG và tích hợp API mô hình lớn (Gemini).
* Thiết kế và xây dựng các luồng tự động hóa quy trình nghiệp vụ trên nền tảng n8n.

### 2. Yêu cầu kỹ năng
* Đang học hoặc đã tốt nghiệp chuyên ngành CNTT, Khoa học máy tính hoặc tương đương.
* Có nền tảng lập trình Python cơ bản tốt. Đã từng gọi thử nghiệm API của OpenAI/Gemini.
* Biết sử dụng Git cơ bản.

### 3. Quyền lợi
* Được đào tạo trực tiếp bởi các Senior AI Engineers.
* Phụ cấp thực tập: $200 - $300/tháng.
```

### Bài tập 2: Quy trình Đánh giá bài test năng lực lập trình viên đầu vào (Mức độ: Khó)
* **Đề bài**: Thiết kế một bài test năng lực thực hành (Technical Assessment Task) dài 4 giờ dành cho ứng viên lập trình viên AI ứng tuyển vào công ty của bạn. Bài test phải yêu cầu ứng viên xây dựng một script Python giải quyết một bài toán cụ thể và đánh giá chất lượng viết code của họ.
* **Yêu cầu**: Học viên tự hoàn thành không có tài liệu mẫu.
* **Gợi ý triển khai (Workflow Hints)**:
  - Đề bài đề xuất: Viết script Python trích xuất thông tin thực thể từ đoạn văn bản thô sử dụng Structured Outputs.
  - Thiết lập các tiêu chuẩn đánh giá code: Khả năng bắt lỗi (Error Handling), cấu trúc thư mục sạch sẽ, tốc độ xử lý của code và cách viết tài liệu hướng dẫn chạy.


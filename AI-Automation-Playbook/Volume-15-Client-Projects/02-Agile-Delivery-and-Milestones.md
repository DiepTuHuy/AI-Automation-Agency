# Chương 02: Kế hoạch triển khai 4 tuần chuẩn Agile

## 1. Deep Dive (Phân tích chuyên sâu)

### Tại sao mô hình Thác Nước (Waterfall) thất bại trong AI?
Trong mô hình Waterfall truyền thống, bạn lập kế hoạch chi tiết, biến mất đi code và chỉ giao sản phẩm vào ngày cuối cùng của hợp đồng. 
Phương pháp này cực kỳ nguy hiểm trong dự án AI vì:
- Khách hàng không thể tưởng tượng AI hoạt động thế nào cho đến khi nhìn thấy trực quan.
- Dữ liệu thực tế của khách hàng có thể chứa nhiều edge cases gây lỗi prompt mà bạn không biết trước.

### Quy trình triển khai 4 tuần chuẩn Agile
Chúng ta chia dự án thành các mốc bàn giao ngắn hạn (Sprints/Milestones) hàng tuần:

```
+-----------------------------------------------------------------+
| Tuần 1: Thiết lập nền tảng & Thiết kế DB                         |
| - Mốc bàn giao (Milestone 1): Sơ đồ database & Cấu hình môi trường|
+-----------------------------------------------------------------+
                               │
                               ▼
+-----------------------------------------------------------------+
| Tuần 2: Xây dựng AI Core & Giao diện tối giản (MVP)              |
| - Mốc bàn giao (Milestone 2): Khách hàng có bản MVP chạy thử được|
+-----------------------------------------------------------------+
                               │
                               ▼
+-----------------------------------------------------------------+
| Tuần 3: Tích hợp hệ thống & Bắt lỗi                             |
| - Mốc bàn giao (Milestone 3): Đồng bộ hóa API, n8n và database  |
+-----------------------------------------------------------------+
                               │
                               ▼
+-----------------------------------------------------------------+
| Tuần 4: Đào tạo, Go-live & Nghiệm thu                           |
| - Mốc bàn giao (Milestone 4): Biên bản nghiệm thu và bàn giao   |
+-----------------------------------------------------------------+
```

---

## 2. Demo: Mẫu Kế hoạch Tiến độ Dự án (Gantt Chart mẫu)

### Mục tiêu
Cung cấp bảng tiến độ dự án chi tiết để chèn vào Proposal gửi khách hàng, giúp thống nhất mốc thanh toán theo tiến độ.

### Tiến độ chi tiết (`project_timeline.md`)
| Tuần | Công việc chi tiết | Kết quả bàn giao (Deliverables) | Mốc thanh toán liên quan |
| :--- | :--- | :--- | :--- |
| **Tuần 1** | - Khảo sát chi tiết cấu trúc dữ liệu.<br>- Thiết lập cơ sở dữ liệu Postgres.<br>- Đóng gói Docker dự án. | Tài liệu thiết kế Database Schema và sơ đồ kiến trúc hệ thống được duyệt. | **Giải ngân Đợt 1 (50%):** Ngay sau khi ký hợp đồng. |
| **Tuần 2** | - Lập trình FastAPI endpoint xử lý AI.<br>- Thiết lập prompt và validate Pydantic.<br>- Dựng giao diện Streamlit cơ bản. | Bản chạy thử **MVP cục bộ**: Khách hàng có thể upload file test thử chất lượng trích xuất của AI. | |
| **Tuần 3** | - Kết nối n8n workflow.<br>- Thiết lập webhook bắt dữ liệu thật.<br>- Tích hợp bot Telegram gửi thông báo. | Hệ thống chạy thông suốt tự động từ Email -> FastAPI -> DB -> Telegram. | |
| **Tuần 4** | - Viết tài liệu hướng dẫn sử dụng.<br>- Quay video đào tạo nhân sự.<br>- Triển khai lên VPS Production. | Ký Biên bản bàn giao bàn giao và nghiệm thu dự án. | **Giải ngân Đợt 2 (50%):** Sau khi ký Biên bản nghiệm thu. |

---

## 3. Mini Project

### Bài tập 1: Lập Kế hoạch các mốc bàn giao dự án (Milestones Plan) (Mức độ: Trung bình)
* **Đề bài**: Lập bảng kế hoạch các mốc thời gian bàn giao (Milestones) cho một dự án xây dựng chatbot nội bộ trong vòng 4 tuần sử dụng phương pháp quản lý dự án Agile/Scrum.
* **Tài liệu sườn mẫu (`project_milestones.md`)**:
```markdown
# Kế hoạch bàn giao dự án: AI Knowledge Base Chatbot

| Tuần | Mốc bàn giao (Milestones) | Kết quả bàn giao (Deliverables) | Trạng thái |
| :--- | :--- | :--- | :--- |
| **Tuần 1** | Hoàn tất thiết kế & Scoping | Tài liệu PRD + Sơ đồ Mermaid hệ thống | Đã duyệt |
| **Tuần 2** | Hoàn tất xây dựng Database | Collection ChromaDB chứa dữ liệu tri thức mẫu | Chờ chạy |
| **Tuần 3** | Tích hợp Core AI & API | API FastAPI chat nội bộ chạy thử nghiệm | Chờ chạy |
| **Tuần 4** | UAT & Chuyển giao | Hướng dẫn vận hành + Bàn giao source code | Chờ chạy |
```

### Bài tập 2: Xây dựng Kế hoạch quản lý rủi ro dự án (Risk Management) (Mức độ: Khó)
* **Đề bài**: Thiết lập bảng quản lý rủi ro cho dự án ở Bài tập 1. Đưa ra 3 rủi ro thường gặp nhất trong dự án AI (ví dụ: Dữ liệu khách hàng quá bẩn, API thay đổi cấu trúc, vượt tiến độ timeline) và đề xuất phương án giảm thiểu rủi ro tương ứng.
* **Yêu cầu**: Học viên tự hoàn thành không có tài liệu mẫu.
* **Gợi ý triển khai (Workflow Hints)**:
  - Định nghĩa các cột: Mô tả rủi ro, Khả năng xảy ra (Cao/Trung bình/Thấp), Mức độ ảnh hưởng, Phương án phòng ngừa & khắc phục.


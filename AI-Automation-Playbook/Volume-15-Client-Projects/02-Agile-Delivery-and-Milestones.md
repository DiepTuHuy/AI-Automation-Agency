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
Hãy tự lập một bảng tiến độ dự án (Gantt Chart) chi tiết tương tự cho dự án **Project 04 (AI Customer Support với MCP)**, điều chỉnh mốc thời gian và công việc phù hợp với thực tế triển khai của bạn.

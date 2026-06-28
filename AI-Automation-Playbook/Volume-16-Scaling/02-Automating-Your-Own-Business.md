# Chương 02: Ứng dụng n8n để tự động hóa vận hành Agency của bạn

## 1. Deep Dive (Phân tích chuyên sâu)

### Hãy tự động hóa chính mình (Eat Your Own Dog Food)
Là một kỹ sư AI Automation, nếu bạn vẫn đang làm các việc hành chính nội bộ bằng tay như:
- Check hòm thư để tìm email khách hàng mới hỏi giá.
- Copy thông tin khách hàng vào file Excel.
- Viết hóa đơn PDF bằng Word rồi gửi mail thủ công.
Thì bạn đang lãng phí thời gian và làm giảm uy tín thương hiệu của bạn khi gặp khách hàng.

Chúng ta sử dụng **n8n** để tự động hóa toàn bộ hệ thống quản trị nội bộ của Agency (Internal CRM):
- **Săn lead tự động**: Tự động quét các diễn đàn, LinkedIn, hoặc Upwork theo từ khóa để gửi tin nhắn báo động về Slack của bạn.
- **Tiếp nhận lead**: Khi khách hàng điền form trên web của bạn, AI sẽ tự động phân loại, lưu vào Notion và đặt lịch hẹn họp trên Calendly.
- **Gửi hóa đơn tự động**: Tự động tạo và gửi link thanh toán của Stripe khi khách hàng đồng ý ký hợp đồng trên Notion.

---

## 2. Demo: Workflow n8n tự động hóa Onboarding Khách hàng mới

### Mục tiêu
Thiết kế luồng hoạt động tự động của n8n khi phát hiện trạng thái dự án trên Notion chuyển sang "Đã Ký Hợp Đồng".

### Sơ đồ hoạt động trong n8n
```
[Trigger: Notion Updated] (Khi trạng thái = 'Contract Signed')
           │
           ▼
[HTTP Request: Stripe API] (Tự động tạo Invoice gửi khách hàng)
           │
           ▼
[Google Drive Node] (Tự động tạo thư mục dự án 'Tên_Khách_Hàng')
           │
           ▼
[Gmail Node] (Gửi email chào mừng kèm link Drive và liên kết đặt lịch họp)
           │
           ▼
[Slack / Telegram Node] (Thông báo cho Team kỹ thuật bắt đầu làm việc)
```

---

## 3. Mini Project

### Bài tập 1: Thiết kế luồng tự động hóa tiếp nhận khách hàng cho Agency của bạn (Mức độ: Trung bình)
* **Đề bài**: Hãy thiết kế một quy trình tự động hóa tiếp nhận khách hàng (Customer Onboarding Workflow) cho chính AI Agency của bạn bằng công cụ n8n hoặc Make.
* **Tài liệu hướng dẫn & Sườn mẫu Workflow**:
```markdown
# Quy trình Onboarding Khách hàng tự động

### 1. Luồng hoạt động:
* Khách hàng điền thông tin đăng ký tư vấn trên Form (Typeform/Google Forms).
* n8n nhận dữ liệu -> Tự động tạo hồ sơ khách hàng mới trong CRM (như Notion hoặc Hubspot).
* Tự động gửi email chào mừng kèm link đặt lịch họp tư vấn qua Calendly.

### 2. Các Node cần sử dụng:
* Google Forms Trigger -> Notion Card Creator -> Gmail Send Email.
```

### Bài tập 2: Hệ thống báo cáo tài chính nội bộ tự động hàng tuần (Mức độ: Khó)
* **Đề bài**: Thiết kế một hệ thống tự động hóa nội bộ: Mỗi tối thứ Sáu, hệ thống tự động quét danh sách đơn hàng đã thanh toán trong CRM, tính toán doanh thu của tuần và gửi báo cáo tóm tắt đẹp mắt vào nhóm Slack của công ty.
* **Yêu cầu**: Học viên tự hoàn thành không có tài liệu mẫu.
* **Gợi ý triển khai (Workflow Hints)**:
  - Sử dụng Node Schedule Trigger đặt lịch định kỳ chạy vào 17:00 chiều thứ Sáu.
  - Sử dụng Node truy vấn dữ liệu CRM để lấy danh sách giao dịch trong tuần.
  - Sử dụng Code Node (JS) tính tổng doanh thu và Slack Node để gửi tin nhắn.


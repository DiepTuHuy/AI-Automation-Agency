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
Hãy tự dựng một workflow n8n cục bộ kết nối với tài khoản Notion cá nhân của bạn (hoặc Trello). Thiết lập trigger: khi bạn kéo một thẻ dự án sang cột "Done", n8n tự động gửi một email báo cáo tổng kết tiến độ tới địa chỉ email cá nhân của bạn. Xuất file JSON của workflow này.

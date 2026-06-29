# Chương 02: Kích hoạt quy trình tự động bằng Webhooks

## 1. Deep Dive (Phân tích chuyên sâu)

### Webhook hoạt động như thế nào?
Webhook là một phương thức cung cấp dữ liệu thời gian thực giữa các ứng dụng phần mềm. Thay vì n8n phải liên tục hỏi ứng dụng gửi (ví dụ: Google Sheets): *"Có hàng mới chưa?"* cứ mỗi 5 phút (gọi là Polling - tốn tài nguyên và bị trễ), ứng dụng gửi sẽ chủ động gửi một gói dữ liệu HTTP POST đến một URL Webhook do n8n cung cấp ngay tại thời điểm sự kiện phát sinh.

### Tích hợp Webhook trong n8n
Node **Webhook** trong n8n hoạt động như một máy chủ web thu nhỏ, liên tục lắng nghe các request gửi đến.
Có hai loại URL Webhook trong n8n:
1. **Test Webhook URL**: Dùng cho quá trình phát triển (Development). Bạn phải mở giao diện n8n và bấm nút "Listen for test event" thì URL này mới hoạt động. Nó hiển thị đầy đủ log dữ liệu đầu vào để debug.
2. **Production Webhook URL**: Dùng khi workflow đã được kích hoạt (Active). Nó chạy ngầm và không hiển thị dữ liệu trực quan trên màn hình thiết kế.

---

## 2. Demo: Nhận và Phân tích Webhook từ Biểu mẫu trực tuyến

### Mục tiêu
Thiết lập một Webhook Node trong n8n lắng nghe dữ liệu gửi lên từ công cụ POST test (như Postman hoặc Curl), tự động trích xuất các trường thông tin.

### Các bước thực hiện
1. Tạo workflow n8n mới, kéo node **Webhook** vào màn hình.
2. Cấu hình node:
   - HTTP Method: `POST`
   - Path: `new-lead`
   - Response Mode: `onReceived`
3. Copy **Test URL** của Webhook (ví dụ: `http://localhost:5678/webhook-test/new-lead`).
4. Bấm nút **Listen for test event** trong n8n.
5. Mở Terminal máy bạn và gửi một gói dữ liệu mock bằng lệnh `curl`:
   ```bash
   curl -X POST http://localhost:5678/webhook-test/new-lead \
   -H "Content-Type: application/json" \
   -d '{"name": "Nguyen Van A", "email": "a@example.com", "budget": 10000}'
   ```
6. Quay lại màn hình n8n, kiểm tra dữ liệu JSON đã được bắt thành công hiển thị trên giao diện trực quan.

---

## 3. Mini Project

### Bài tập 1: Tạo Webhook bắt thông tin đơn hàng WooCommerce (Mức độ: Trung bình)
* **Đề bài**: Thiết kế một Webhook Node trong n8n đóng vai trò là điểm nhận (Endpoint) dữ liệu từ WooCommerce khi có đơn hàng mới và in ra log thông tin chi tiết đơn hàng đó.
* **Tài liệu hướng dẫn & Sườn mẫu Workflow**:
```markdown
# Cấu hình n8n Webhook Listener

### 1. Cấu hình Webhook Node:
* **HTTP Method**: `POST`
* **Path**: `woo-order-created`
* **Response Mode**: `On Received` với status `200` để báo nhận thành công lập tức.

### 2. Cách kiểm thử:
1. Bấm nút "Listen for test event" trên n8n.
2. Sử dụng Postman hoặc Curl gửi một request POST giả lập dữ liệu đơn hàng tới URL Webhook Test của n8n.
```

### Bài tập 2: Tự động gửi tin nhắn báo doanh thu đơn hàng VIP (Mức độ: Khó)
* **Đề bài**: Nâng cấp Webhook ở Bài tập 1. Khi đơn hàng gửi tới có giá trị trên 5,000,000 VND (VIP), tự động kích hoạt gửi một tin nhắn cảnh báo đơn hàng giá trị cao đến kênh Telegram của quản lý.
* **Yêu cầu**: Bạn hãy tự hoàn thành không có tài liệu mẫu.
* **Gợi ý triển khai (Workflow Hints)**:
  - Sử dụng Node `IF` để so sánh trường tổng tiền: `{{ $json.total }} >= 5000000`.
  - Sử dụng Telegram Node (hoặc HTTP Request gọi API Telegram Bot) kết nối vào nhánh True để gửi tin nhắn.

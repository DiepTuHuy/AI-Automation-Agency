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
Hãy cấu hình tiếp trong workflow trên: Kết nối node Webhook đó với một node **If** (Phân nhánh logic). Thiết lập điều kiện: NẾU `budget` lớn hơn hoặc bằng 5000 -> THÌ rẽ nhánh TRUE, NGƯỢC LẠI rẽ nhánh FALSE. Chạy test lại bằng Curl với 2 mức budget khác nhau (3000 và 7000) để kiểm tra luồng phân nhánh chạy chính xác.

# Chương 03: HTTP Request Node - Gọi các Dịch vụ Ngoài từ n8n

## 1. Deep Dive (Phân tích chuyên sâu)

Mặc dù n8n có sẵn các node tích hợp sẵn cho OpenAI hay Google Sheets, tuy nhiên trong các dự án thực tế, bạn sẽ thường xuyên phải gọi các dịch vụ API tùy chỉnh do chính bạn viết (như FastAPI backend của bạn ở Vol 04) hoặc các API bên thứ ba chưa có node dựng sẵn trên n8n.

**HTTP Request Node** là vũ khí mạnh nhất của n8n cho phép bạn gửi bất kỳ HTTP request nào (GET, POST, PUT, DELETE) kèm theo cấu hình:
- Headers (chứa Authorization, API Keys).
- Query Parameters.
- Body (JSON payload, form-data cho file upload).
- Tùy chọn xác thực nâng cao (OAuth2, SSL).

---

## 2. Demo: Gọi FastAPI Backend trích xuất thông tin khách hàng từ n8n

### Mục tiêu
Thiết lập n8n HTTP Request node để gọi endpoint FastAPI cục bộ (đang chạy ở cổng 8000), truyền dữ liệu động từ webhook trước đó sang FastAPI để xử lý.

### Cấu hình Node HTTP Request trong n8n
1. Kéo node **HTTP Request** nối sau node Webhook nhận thông tin lead.
2. Cấu hình các thông số:
   - Method: `POST`
   - URL: `http://host.docker.internal:8000/api/v1/analyze-feedback`
     *(Lưu ý kỹ thuật: Vì n8n chạy trong Docker container, để gọi cổng 8000 trên máy host của bạn, bạn phải dùng địa chỉ đặc biệt `host.docker.internal` thay vì `localhost`)*.
   - Send Headers: Bật
     - Name: `X-API-Key` | Value: `your_system_secret_key`
   - Send Body: Bật
     - Body Content Type: `JSON`
     - Specify Body: `Using Fields Below`
       - Name: `customer_email` | Value: `{{ $json.body.email }}`
       - Name: `feedback_text` | Value: `{{ $json.body.message }}`
       - Name: `priority` | Value: `3`

---

## 3. Mini Project

### Bài tập 1: Gọi API thời tiết và lưu trữ lịch sử bằng n8n (Mức độ: Trung bình)
* **Đề bài**: Thiết kế workflow n8n sử dụng HTTP Request Node để gọi API thời tiết mở, trích xuất nhiệt độ và ghi vào file CSV cục bộ để theo dõi.
* **Tài liệu hướng dẫn & Sườn mẫu Workflow**:
```markdown
# Cấu hình HTTP Request gọi API ngoài

### 1. HTTP Request Node:
* **Method**: `GET`
* **URL**: `https://api.open-meteo.com/v1/forecast?latitude=21.0285&longitude=105.8542&current_weather=true`
* **Authentication**: None (API công cộng).

### 2. Trích xuất dữ liệu:
* Dữ liệu trả về sẽ nằm trong biến: `{{ $json.current_weather.temperature }}`.
```

### Bài tập 2: Quét thông tin tỷ giá ngoại tệ và cảnh báo biến động (Mức độ: Khó)
* **Đề bài**: Thiết kế workflow tự động chạy mỗi sáng (cron trigger). Gọi API tỷ giá USD/VND, nếu tỷ giá vượt ngưỡng 25,400 VND, tự động gửi email thông báo khẩn cấp tới phòng kế toán.
* **Yêu cầu**: Học viên tự hoàn thành không có tài liệu mẫu.
* **Gợi ý triển khai (Workflow Hints)**:
  - Sử dụng Node `Schedule Trigger` đặt thời gian chạy định kỳ.
  - Sử dụng Node `HTTP Request` lấy tỷ giá từ API hối đoái.
  - Sử dụng Node `IF` để so sánh tỷ giá với con số `25400`.


# Chương 01: Tổng quan về n8n & Thiết lập môi trường Docker cục bộ

## 1. Deep Dive (Phân tích chuyên sâu)

### n8n là gì?
n8n là một công cụ tự động hóa quy trình nghiệp vụ (Workflow Automation) mở và có khả năng mở rộng cực cao. Nó cho phép bạn kết nối hơn 400 ứng dụng phổ biến (như Google Drive, Slack, Gmail, HubSpot) và bất kỳ REST API nào bằng phương pháp kéo thả trực quan.

### Tại sao n8n vượt trội hơn Zapier và Make đối với Kỹ sư AI?
1. **Khả năng tự host (Self-hostable)**: Bạn có thể cài đặt n8n hoàn toàn miễn phí trên VPS cá nhân bằng Docker. Zapier tính phí theo số lượng tác vụ (tasks) khiến hóa đơn hàng tháng có thể lên tới hàng nghìn USD đối với các tác vụ AI quét dữ liệu hàng loạt. n8n tự host không bị giới hạn số lượng tasks chạy.
2. **Bảo mật dữ liệu tuyệt đối**: Dữ liệu của khách hàng doanh nghiệp B2B (đặc biệt là ngân hàng, y tế) không được phép đi qua máy chủ bên thứ ba. n8n tự host cho phép chạy hoàn toàn trong mạng nội bộ của doanh nghiệp.
3. **Mã nguồn mở và tùy biến cao**: n8n cho phép viết mã nguồn JavaScript/TypeScript trực tiếp để xử lý dữ liệu phức tạp mà không có rào cản kỹ thuật.

---

## 2. Demo: Khởi động n8n cục bộ bằng Docker CLI

### Mục tiêu
Cài đặt và khởi chạy một container n8n trên máy tính cá nhân của bạn thông qua Docker, tạo tài khoản Admin đầu tiên.

### Các bước thực hiện
1. Đảm bảo máy bạn đã cài đặt **Docker Desktop** (Tải về từ docker.com).
2. Mở Terminal và chạy lệnh khởi chạy container n8n:
   ```bash
   docker run -d --name n8n -p 5678:5678 -v n8n_data:/home/node/.n8n -e N8N_SECURE_COOKIE=false n8nio/n8n
   ```
   *Giải thích tham số*:
   - `-d`: Chạy ẩn container trong nền (detached mode).
   - `--name n8n`: Đặt tên container là `n8n`.
   - `-p 5678:5678`: Ánh xạ cổng 5678 của container ra cổng 5678 của máy bạn.
   - `-v n8n_data:/home/node/.n8n`: Mount một Docker Volume tên là `n8n_data` để lưu trữ vĩnh viễn các workflow của bạn, tránh bị mất khi tắt container.
3. Truy cập trình duyệt web tại địa chỉ: `http://localhost:5678`.
4. Thiết lập tài khoản email/mật khẩu Admin ban đầu để đăng nhập giao diện làm việc.

---

## 3. Mini Project

### Bài tập 1: Xây dựng quy trình tự động chuyển dữ liệu sang Google Sheets (Mức độ: Trung bình)
* **Đề bài**: Hãy thiết kế một workflow n8n nhận dữ liệu từ một nguồn giả lập (Mock Data) và tự động ghi dữ liệu đó vào một bảng tính Google Sheets.
* **Tài liệu hướng dẫn & Sườn mẫu Workflow**:
```markdown
# Hướng dẫn cấu hình n8n Google Sheets Workflow

### 1. Các Node sử dụng:
* **Webhook / Schedule Trigger**: Kích hoạt workflow tự động.
* **Set Node (hoặc Edit Fields)**: Tạo các biến dữ liệu giả lập (tên, email, ngày đăng ký).
* **Google Sheets Node**: Ghi đè hoặc thêm dòng mới vào file Google Sheets được chỉ định.

### 2. Các bước cấu hình:
1. Tạo một bảng tính Google Sheets trống trên Drive của bạn.
2. Cấu hình Credentials của Google Sheets trên n8n sử dụng tài khoản Google.
3. Liên kết Sheet ID và chọn hành động `Append` để tự động thêm dòng dữ liệu mới.
```

### Bài tập 2: Đồng bộ danh sách khách hàng tự động với điều kiện lọc (Mức độ: Khó)
* **Đề bài**: Nâng cấp workflow ở Bài tập 1. Sử dụng thêm node IF để lọc dữ liệu. Chỉ những khách hàng có trạng thái đăng ký là `Active` và có email hợp lệ mới được ghi vào Google Sheets, những khách hàng khác sẽ được ghi vào một file log riêng biệt hoặc gửi thông báo cảnh báo.
* **Yêu cầu**: Học viên tự hoàn thành không có tài liệu mẫu.
* **Gợi ý triển khai (Workflow Hints)**:
  - Sử dụng Node `IF` để kiểm tra điều kiện: `{{ $json.status }} EQUALS active`.
  - Kết nối nhánh True của `IF` Node vào Google Sheets Node.
  - Nhánh False kết nối vào một Node gửi email cảnh báo hoặc ghi dữ liệu khác.


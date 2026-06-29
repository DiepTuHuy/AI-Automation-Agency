# Hướng dẫn cấu hình n8n Google Sheets Workflow

### 1. Các Node sử dụng:
* **Webhook / Schedule Trigger**: Kích hoạt workflow tự động.
* **Set Node (hoặc Edit Fields)**: Tạo các biến dữ liệu giả lập (tên, email, ngày đăng ký).
* **Google Sheets Node**: Ghi đè hoặc thêm dòng mới vào file Google Sheets được chỉ định.

### 2. Các bước cấu hình:
1. Tạo một bảng tính Google Sheets trống trên Drive của bạn.
2. Cấu hình Credentials của Google Sheets trên n8n sử dụng tài khoản Google.
3. Liên kết Sheet ID và chọn hành động `Append` để tự động thêm dòng dữ liệu mới.
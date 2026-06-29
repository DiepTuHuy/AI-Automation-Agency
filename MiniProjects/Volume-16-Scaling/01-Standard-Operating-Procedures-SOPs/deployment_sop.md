# SOP: Quy trình triển khai sản phẩm lên VPS khách hàng

* **Mã quy trình**: SOP-DEP-01
* **Mục tiêu**: Đảm bảo toàn bộ ứng dụng được deploy an toàn, không xung đột thư viện.
* **Các bước thực hiện**:
  1. Đăng nhập vào VPS qua SSH sử dụng khóa bảo mật.
  2. Tạo thư mục dự án và thực hiện `git clone` mã nguồn từ nhánh `main`.
  3. Khởi tạo môi trường ảo Python và chạy cài đặt: `pip install -r requirements.txt`.
  4. Tạo tệp `.env` cấu hình API Key thực tế của khách hàng.
  5. Khởi động dịch vụ dưới nền bằng `systemd` hoặc `docker-compose`.
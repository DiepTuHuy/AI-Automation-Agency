# Chương 03: Thiết lập Nginx Reverse Proxy & Chứng chỉ SSL HTTPS

## 1. Deep Dive (Phân tích chuyên sâu)

### Reverse Proxy là gì?
Khi bạn chạy Docker container FastAPI trên VPS, ứng dụng sẽ lắng nghe ở một cổng nội bộ (ví dụ: `8000`). Trình duyệt web của người dùng không nên kết nối trực tiếp vào cổng này.
Chúng ta sử dụng **Nginx** làm Reverse Proxy ở phía trước:
- Nginx đứng ở cổng công cộng `80` và `443` nhận request từ người dùng.
- Nginx kiểm tra xem tên miền yêu cầu là gì (ví dụ: `api.mycrm.com`) và điều hướng request nội bộ (proxy pass) tới container chạy ở cổng `8000`.
- Nginx quản lý và giải mã chứng chỉ bảo mật SSL/TLS để cung cấp giao thức **HTTPS** mã hóa dữ liệu đường truyền an toàn.

---

## 2. Demo: File cấu hình Nginx Server Block & Cài đặt SSL bằng Certbot

### Mục tiêu
Cấu hình file Nginx Server Block điều hướng tên miền riêng về cổng 8000 và lấy HTTPS SSL miễn phí từ Let's Encrypt.

### File cấu hình Nginx (`/etc/nginx/sites-available/myapi`)
```nginx
server {
    listen 80;
    server_name api.mycrm.com; # Thay thế bằng tên miền thực tế của bạn

    # Giới hạn kích thước file upload tối đa qua Nginx là 10MB
    client_max_body_size 10M;

    location / {
        # Điều hướng request về cổng 8000 của FastAPI chạy cục bộ
        proxy_pass http://127.0.0.1:8000;
        
        # Truyền thông tin header gốc của client cho FastAPI đọc
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Các bước cài đặt HTTPS tự động bằng Certbot (Let's Encrypt)
1. Cài đặt Certbot và plugin Nginx trên Ubuntu:
   ```bash
   sudo apt update
   sudo apt install certbot python3-certbot-nginx -y
   ```
2. Chạy Certbot quét và cấu hình tự động file Nginx block:
   ```bash
   sudo certbot --nginx -d api.mycrm.com
   ```
   *Certbot sẽ tự động sinh mã hóa HTTPS, tạo file SSL, sửa đổi file cấu hình Nginx ở trên và thiết lập cron-job tự động gia hạn (auto-renew) chứng chỉ SSL sau mỗi 90 ngày*.

---

## 3. Mini Project

### Bài tập 1: Cấu hình Nginx làm Reverse Proxy cho FastAPI (Mức độ: Trung bình)
* **Đề bài**: Hãy viết một tệp cấu hình Nginx Server Block để làm Reverse Proxy chuyển tiếp các request từ cổng `80` của tên miền công cộng vào ứng dụng FastAPI đang chạy ở cổng `8000`.
* **Mã nguồn mẫu (`nginx.conf`)**:
```nginx
server {
    listen 80;
    server_name example.com; # Thay thế bằng tên miền của bạn

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Bài tập 2: Cấu hình tự động cài đặt chứng chỉ SSL Let's Encrypt (Mức độ: Khó)
* **Đề bài**: Hãy viết hướng dẫn các bước sử dụng công cụ `certbot` để xin chứng chỉ bảo mật SSL Let's Encrypt miễn phí và cấu hình tự động gia hạn chứng chỉ cho máy chủ Nginx.
* **Yêu cầu**: Học viên tự hoàn thành không có tài liệu mẫu.
* **Gợi ý triển khai (Workflow Hints)**:
  - Cài đặt Certbot thông qua câu lệnh: `sudo apt install certbot python3-certbot-nginx -y`.
  - Xin chứng chỉ SSL bằng lệnh: `sudo certbot --nginx -d example.com`.
  - Kiểm tra tính năng tự động gia hạn (Dry-run) qua: `sudo certbot renew --dry-run`.


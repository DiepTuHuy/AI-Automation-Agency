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
Hãy viết sơ đồ kiến trúc dòng lưu lượng dữ liệu (Traffic Flow Diagram) chi tiết mô tả đường đi của một request gửi đi từ trình duyệt web của người dùng tại Việt Nam, đi qua phân giải DNS, chạm vào Nginx của VPS tại Singapore, đi vào Docker container FastAPI, và phản hồi ngược lại.

# Chương 02: Quản trị Linux VPS & Cấu hình Tường lửa Bảo mật

## 1. Deep Dive (Phân tích chuyên sâu)

### Thuê và quản trị Linux VPS
Khi triển khai ứng dụng Production, bạn sẽ thuê một máy chủ ảo riêng (Virtual Private Server - VPS) chạy hệ điều hành Linux (khuyến nghị sử dụng **Ubuntu Server 22.04 LTS** hoặc phiên bản mới nhất vì tính ổn định và cộng đồng hỗ trợ lớn).

Để quản lý server từ xa, ta sử dụng giao thức bảo mật **SSH (Secure Shell)**.

### Bảo mật Linux Server cơ bản
Một máy chủ Linux khi vừa mở IP ra Internet sẽ lập tức bị hàng vạn botnet quét IP dò tìm mật khẩu. Quy trình bảo mật tối thiểu bạn phải làm là:
1. **Sử dụng SSH Key**: Tạo cặp khóa SSH (Public Key lưu trên server, Private Key lưu an toàn trên máy của bạn). Chỉ người sở hữu Private Key mới được đăng nhập.
2. **Cấu hình tường lửa UFW (Uncomplicated Firewall)**: Chặn toàn bộ các cổng mạng không sử dụng. Chỉ cho phép các cổng:
   - Cổng `22`: Để bạn kết nối SSH.
   - Cổng `80` (HTTP): Nhận truy cập web thông thường.
   - Cổng `443` (HTTPS): Nhận truy cập web bảo mật mã hóa SSL.

---

## 2. Demo: SSH key setup & Cấu hình UFW từng bước trên Terminal

### Mục tiêu
Tạo SSH Key từ máy cá nhân của bạn, thêm vào VPS và cấu hình tường lửa UFW bảo mật trên Ubuntu Server.

### Các lệnh thực hiện (macOS/Linux Terminal)
1. **Tạo SSH Key trên máy cá nhân của bạn**:
   ```bash
   ssh-keygen -t ed25519 -C "admin_key_vps"
   ```
   *Kết quả*: Hệ thống tạo ra 2 file khóa: `id_ed25519` (Private Key - KHÔNG được tiết lộ) và `id_ed25519.pub` (Public Key).
2. **Copy Public Key lên VPS Ubuntu của bạn**:
   ```bash
   ssh-copy-id -i ~/.ssh/id_ed25519.pub root@your_server_ip
   ```
3. **Đăng nhập vào VPS bằng SSH Key**:
   ```bash
   ssh root@your_server_ip
   ```
4. **Cấu hình tường lửa UFW trên VPS**:
   ```bash
   # Kiểm tra trạng thái hiện tại (mặc định là inactive)
   ufw status
   
   # Cấu hình chặn toàn bộ mặc định đầu vào, cho phép mặc định đầu ra
   ufw default deny incoming
   ufw default allow outgoing
   
   # Cho phép các cổng mạng thiết yếu
   ufw allow 22/tcp     # Cho phép SSH
   ufw allow 80/tcp     # Cho phép HTTP
   ufw allow 443/tcp    # Cho phép HTTPS
   
   # Kích hoạt tường lửa hoạt động
   ufw enable
   
   # Xem lại bảng cấu hình thực tế
   ufw status verbose
   ```

---

## 3. Mini Project
Hãy viết một file tài liệu cheat-sheet ghi chú lại 15 câu lệnh Linux cơ bản nhất thường dùng trong quản lý VPS (ví dụ: `ls`, `cd`, `pwd`, `sudo`, `apt update`, `df -h`, `free -m`, `htop`, `systemctl`, `journalctl`...) kèm mô tả chi tiết chức năng để làm tài liệu tham khảo nhanh cho bản thân.

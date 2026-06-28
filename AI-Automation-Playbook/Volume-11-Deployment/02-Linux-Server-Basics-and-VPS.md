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

### Bài tập 1: Các lệnh quản trị Linux cơ bản trên VPS (Mức độ: Trung bình)
* **Đề bài**: Hãy liệt kê và mô tả các dòng lệnh Linux cơ bản dùng để thực thi các tác vụ: Cập nhật hệ thống, cài đặt thư viện Python, kiểm tra dung lượng ổ đĩa, và xem các cổng mạng đang mở trên máy chủ VPS Ubuntu.
* **Tài liệu sườn mẫu (`vps_commands.sh`)**:
```bash
# 1. Cập nhật hệ thống
sudo apt update && sudo apt upgrade -y

# 2. Cài đặt Python và Pip
sudo apt install python3 python3-pip -y

# 3. Kiểm tra dung lượng ổ đĩa
df -h

# 4. Xem các cổng mạng đang mở lắng nghe
sudo ss -tunlp
```

### Bài tập 2: Thiết lập tường lửa bảo mật UFW cho VPS (Mức độ: Khó)
* **Đề bài**: Hãy viết hướng dẫn cấu hình tường lửa UFW (Uncomplicated Firewall) trên máy chủ VPS. Yêu cầu chỉ cho phép truy cập cổng SSH (`22`), HTTP (`80`), HTTPS (`443`) và chặn toàn bộ các cổng mạng không được cấu hình khác để ngăn chặn tấn công mạng.
* **Yêu cầu**: Học viên tự hoàn thành không có tài liệu mẫu.
* **Gợi ý triển khai (Workflow Hints)**:
  - Sử dụng lệnh `sudo ufw allow 22/tcp` để cho phép SSH (Quan trọng: Không làm mất kết nối hiện tại).
  - Sử dụng `sudo ufw allow 80` và `sudo ufw allow 443`.
  - Kích hoạt tường lửa bằng lệnh `sudo ufw enable` và kiểm tra trạng thái qua `sudo ufw status`.


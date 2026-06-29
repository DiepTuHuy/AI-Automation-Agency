# Chương 01: Quy trình Vận hành Chuẩn (SOPs) - Chìa khóa nhân bản năng lực

## 1. Deep Dive (Phân tích chuyên sâu)

### Tại sao bạn bị quá tải khi dự án tăng lên?
Khi bạn có 1 khách hàng, bạn nhớ hết cấu hình server của họ. Khi bạn có 5 khách hàng cùng lúc, bạn sẽ bắt đầu nhầm lẫn:
- Server của khách hàng A dùng cổng nào?
- File backup của khách hàng B lưu ở đâu?
- Prompt của khách hàng C đã cập nhật phiên bản mới chưa?

Mỗi lần phát sinh lỗi nhỏ, bạn lại phải mất cả tiếng đồng hồ lục lại lịch sử code để tìm nguyên nhân. Đây là dấu hiệu bạn thiếu **SOP (Standard Operating Procedure)**.

### Cách viết một SOP Kỹ thuật chuẩn hóa
Một SOP kỹ thuật hiệu quả phải được viết dưới dạng danh sách việc cần làm (Checklist) chi tiết, từng câu lệnh rõ ràng, không mơ hồ:
1. **Mục đích**: Tác vụ này giải quyết việc gì?
2. **Ai thực hiện**: Vai trò nào được quyền làm?
3. **Các bước thực hiện**: Ghi rõ chính xác các câu lệnh terminal cần gõ, các file cần chỉnh sửa.
4. **Cách kiểm tra kết quả**: Làm sao để biết bước này đã chạy đúng?
5. **Xử lý sự cố (Troubleshooting)**: Nếu gặp lỗi X thì sửa thế nào?

---

## 2. Demo: SOP Triển khai FastAPI lên VPS Ubuntu mới cứng

### Mục tiêu
Cung cấp mẫu tài liệu SOP kỹ thuật hoàn chỉnh hướng dẫn cài đặt môi trường và chạy ứng dụng web.

### Nội dung SOP mẫu (`sop_vps_setup.md`)
```markdown
# SOP: CẤU HÌNH & TRIỂN KHAI BACKEND LÊN VPS UBUNTU MỚI

- **Mã SOP**: SOP-DEV-001
- **Phiên bản**: 1.2
- **Người chịu trách nhiệm**: Lead DevOps Engineer

### Bước 1: Đăng nhập và cập nhật hệ thống
1. Đăng nhập vào VPS bằng SSH Key:
   ```bash
   ssh -i ~/.ssh/my_private_key root@server_ip
   ```
2. Thực hiện cập nhật danh sách gói phần mềm:
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

### Bước 2: Cài đặt Docker và Docker Compose
1. Chạy lệnh cài đặt tự động từ script chính thức:
   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   ```
2. Kiểm tra xem Docker đã hoạt động chưa:
   ```bash
   docker --version
   systemctl status docker # Phải hiển thị 'active (running)'
   ```

### Bước 3: Cấu hình Tường lửa UFW
1. Khóa toàn bộ cổng, chỉ cho phép cổng quản trị và web:
   ```bash
   sudo ufw default deny incoming
   sudo ufw default allow outgoing
   sudo ufw allow 22/tcp
   sudo ufw allow 80/tcp
   sudo ufw allow 443/tcp
   sudo ufw enable # Bấm Y để đồng ý
   ```

### Bước 4: Kiểm tra kết quả deploy
1. Gửi request test thử cổng HTTP thông thường:
   ```bash
   curl http://localhost
   ```
   *Kết quả mong đợi: Nhận phản hồi lỗi 502 của Nginx (vì chưa cấu hình backend) hoặc trang welcome mặc định. Nếu báo 'Connection refused' nghĩa là tường lửa đã chặn sai cổng*.
```

---

## 3. Mini Project

### Bài tập 1: Soạn quy trình vận hành chuẩn SOP cho việc bàn giao dự án (Mức độ: Trung bình)
* **Đề bài**: Hãy thiết lập một tài liệu Quy trình vận hành tiêu chuẩn (SOP - Standard Operating Procedure) cho các kỹ sư trong AI Agency của bạn khi thực hiện bàn giao mã nguồn lên máy chủ VPS của khách hàng.
* **Tài liệu sườn mẫu (`deployment_sop.md`)**:
```markdown
# SOP: Quy trình triển khai sản phẩm lên VPS khách hàng

* **Mã quy trình**: SOP-DEP-01
* **Mục tiêu**: Đảm bảo toàn bộ ứng dụng được deploy an toàn, không xung đột thư viện.
* **Các bước thực hiện**:
  1. Đăng nhập vào VPS qua SSH sử dụng khóa bảo mật.
  2. Tạo thư mục dự án và thực hiện `git clone` mã nguồn từ nhánh `main`.
  3. Khởi tạo môi trường ảo Python và chạy cài đặt: `pip install -r requirements.txt`.
  4. Tạo tệp `.env` cấu hình API Key thực tế của khách hàng.
  5. Khởi động dịch vụ dưới nền bằng `systemd` hoặc `docker-compose`.
```

### Bài tập 2: SOP Xử lý Khắc phục sự cố khẩn cấp khi hệ thống AI bị lỗi (Mức độ: Khó)
* **Đề bài**: Thiết lập tài liệu SOP hướng dẫn xử lý sự cố khẩn cấp (Incident Response SOP) khi khách hàng báo lỗi hệ thống AI ngừng phản hồi. SOP phải bao gồm các bước kiểm tra log nhanh, khởi động lại dịch vụ và liên hệ hỗ trợ khẩn cấp.
* **Yêu cầu**: Bạn hãy tự hoàn thành không có tài liệu mẫu.
* **Gợi ý triển khai (Workflow Hints)**:
  - Phân chia nhiệm vụ rõ ràng: Ai là người tiếp nhận thông tin lỗi, ai thực hiện debug kỹ thuật.
  - Viết chi tiết các câu lệnh kiểm tra log hệ thống nhanh (ví dụ: `docker logs web_service` hoặc `journalctl -u api_service`).

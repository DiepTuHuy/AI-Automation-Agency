# Chương 03: Hướng dẫn sử dụng Playbook & Setup Môi trường

## 1. Deep Dive (Phân tích chuyên sâu)

### Cách học Playbook hiệu quả nhất: Learn by Building
Playbook này được thiết kế để bạn hành động. Với mỗi chương:
1. **Đọc hiểu bản chất** (First Principles và Mental Models).
2. **Gõ lại mã nguồn** trong phần Demo trên máy cá nhân của bạn. Không copy-paste. Việc tự gõ giúp cơ bắp và não bộ của bạn ghi nhớ cú pháp và logic.
3. **Hoàn thành Mini Project** để tự kiểm tra khả năng ứng dụng.
4. **Vượt qua bài test trắc nghiệm** ở phần cuối mỗi Volume với điểm số >= 80%.

### Cài đặt môi trường làm việc chuẩn Kỹ sư (Developer Environment)
Bạn cần cài đặt các công cụ sau:
1. **Homebrew** (Dành cho macOS) để cài đặt các gói phần mềm dễ dàng.
2. **VS Code (Visual Studio Code)**: Trình soạn thảo mã nguồn phổ biến nhất thế giới.
3. **Python 3.10+**: Ngôn ngữ lập trình chính được sử dụng để xây dựng AI Automation.
4. **Git**: Hệ thống quản lý phiên bản code.
5. **Terminal/iTerm2**: Giao diện dòng lệnh để giao tiếp với hệ điều hành.

---

## 2. Demo: Hướng dẫn Setup từng bước bằng CLI (Command Line Interface)

### Mục tiêu
Cài đặt Python, Git và cấu hình VS Code sẵn sàng cho việc lập trình.

### Các bước thực hiện (macOS/Linux)
1. Mở Terminal và kiểm tra xem Python đã được cài đặt chưa:
   ```bash
   python3 --version
   ```
2. Nếu chưa cài đặt, sử dụng Homebrew để cài:
   ```bash
   brew install python
   ```
3. Kiểm tra cài đặt Git:
   ```bash
   git --version
   ```
4. Cấu hình thông tin Git cá nhân của bạn:
   ```bash
   git config --global user.name "Tên Của Bạn"
   git config --global user.email "email_cua_ban@example.com"
   ```
5. Cài đặt các Extension cần thiết trên VS Code:
   - Python (Microsoft)
   - Pylance
   - Prettier (Định dạng code)
   - Markdown All in One (Để viết và xem tài liệu tốt hơn)

---

## 3. Mini Project
Tạo một thư mục dự án mới tên là `ai-automation-test` bằng Terminal, tạo một tệp tin `app.py` bên trong, viết mã nguồn Python đơn giản: `print("Môi trường của tôi đã sẵn sàng!")`, chạy file đó bằng Terminal và chụp ảnh màn hình kết quả chạy thành công để lưu vào báo cáo học tập của bạn.

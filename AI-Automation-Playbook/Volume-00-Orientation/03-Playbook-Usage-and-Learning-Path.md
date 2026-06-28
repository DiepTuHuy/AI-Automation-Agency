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

### Bài tập 1: Xây dựng Kế hoạch học tập Cá nhân hóa (Mức độ: Trung bình)
* **Đề bài**: Dựa vào mục tiêu nghề nghiệp cá nhân (ví dụ: làm Freelancer, xây dựng AI Agency riêng, hay thăng tiến thành Solution Architect), hãy lập sơ đồ lộ trình học tập chi tiết của bạn trong 6 tháng tới dựa trên các Volume của Playbook này.
* **Tài liệu sườn mẫu (`learning_plan.md`)**:
```markdown
# Lộ trình học tập AI Automation của: [Tên của bạn]

* **Mục tiêu**: Xây dựng AI Agency tự động hóa quy trình nghiệp vụ cho doanh nghiệp.
* **Tháng 1-2 (Trọng tâm: Nền tảng kỹ thuật)**: Học kỹ Volume 01 (LLM), Volume 02 (Prompt Engineering) và Volume 03 (Python). Hoàn thành 2 dự án đầu tiên.
* **Tháng 3-4 (Trọng tâm: Tự động hóa & Database)**: Học Volume 05 (n8n), Volume 06 (Database) và Volume 07-08 (RAG).
* **Tháng 5-6 (Trọng tâm: Kinh doanh & Chuyển giao)**: Học Volume 14 (Sales Outreach) và Volume 15 (Discovery Session).
```

### Bài tập 2: Thiết kế Dự án Capstone Cá nhân (Mức độ: Khó)
* **Đề bài**: Thiết kế đề cương chi tiết cho Dự án Capstone tốt nghiệp của bạn. Dự án phải giải quyết một bài toán thực tế của khách hàng doanh nghiệp, sử dụng ít nhất 3 công nghệ học từ Playbook (ví dụ: FastAPI, n8n, ChromaDB, Gemini).
* **Yêu cầu**: Học viên tự hoàn thành không có tài liệu mẫu.
* **Gợi ý triển khai (Workflow Hints)**:
  - Mô tả rõ: Tên dự án, Đối tượng khách hàng mục tiêu, Bài toán nghiệp vụ cần giải quyết.
  - Vẽ sơ đồ kiến trúc hệ thống mô phỏng dòng chảy dữ liệu từ nguồn cấp đến đầu ra API.


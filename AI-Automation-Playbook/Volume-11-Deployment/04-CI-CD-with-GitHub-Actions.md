# Chương 04: Tự động hóa triển khai (CI/CD) bằng GitHub Actions

## 1. Deep Dive (Phân tích chuyên sâu)

### Triết lý CI/CD trong phát triển phần mềm hiện đại
- **CI (Continuous Integration - Tích hợp liên tục)**: Mỗi khi lập trình viên đẩy code mới lên GitHub, hệ thống tự động khởi chạy môi trường ảo, cài đặt dependencies, chạy các công cụ kiểm tra chất lượng code (linter như flake8) và chạy bộ unit tests (pytest) để đảm bảo code mới không làm hỏng tính năng cũ.
- **CD (Continuous Deployment - Triển khai liên tục)**: Khi code đã vượt qua vòng kiểm tra CI trên nhánh chính (`main`), hệ thống tự động đăng nhập vào VPS qua SSH, kéo code mới nhất từ kho lưu trữ và khởi động lại dịch vụ Docker để cập nhật ứng dụng tự động.

---

## 2. Demo: File cấu hình Workflow GitHub Actions hoàn chỉnh

### Mục tiêu
Viết tệp tin cấu hình YAML của GitHub Actions tự động đăng nhập vào VPS để build và khởi chạy lại Docker Compose mỗi khi bạn push code mới lên nhánh main.

### Đường dẫn file trong dự án của bạn
`.github/workflows/deploy.yml`

### Nội dung cấu hình (`deploy.yml`)
```yaml
name: Deploy Production Backend

on:
  push:
    branches:
      - main # Kích hoạt tự động khi push code lên nhánh main

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository code
        uses: actions/checkout@v3

      # Thiết lập SSH Key bí mật để đăng nhập vào VPS
      - name: Execute deployment commands via SSH
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.SERVER_IP }} # Lưu trong Settings -> Secrets của GitHub repo
          username: root
          key: ${{ secrets.SSH_PRIVATE_KEY }} # Lưu Private Key của bạn trong Secrets
          port: 22
          script: |
            # Di chuyển vào thư mục dự án trên VPS
            cd /var/www/ai-crm-backend
            
            # Kéo code mới nhất từ GitHub về VPS
            git pull origin main
            
            # Khởi động lại hệ thống container Docker
            docker-compose down
            docker-compose up -d --build
            
            echo "--- ĐÃ TRIỂN KHAI THÀNH CÔNG CODE MỚI LÊN VPS ---"
```

---

## 3. Mini Project
Hãy viết một file cấu hình GitHub Actions cơ bản thực hiện công việc kiểm tra chất lượng code Python (chạy lệnh kiểm lỗi cú pháp `flake8` hoặc chạy `black` format code) mỗi khi có lập trình viên gửi một Pull Request mới vào nhánh `main` của dự án.

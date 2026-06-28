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

### Bài tập 1: Viết file cấu hình GitHub Actions Linting tự động (Mức độ: Trung bình)
* **Đề bài**: Hãy viết một tệp cấu hình Workflow cho GitHub Actions (`.github/workflows/lint.yml`) để tự động chạy kiểm thử cú pháp Python (Black hoặc Flake8) bất kỳ khi nào có lập trình viên push code lên nhánh `main`.
* **Mã nguồn mẫu (`lint.yml`)**:
```yaml
name: Python Code Linting

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
    - name: Checkout code
      uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: "3.10"

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install black flake8

    - name: Run Black formatter check
      run: black --check .
```

### Bài tập 2: Cấu hình tự động build và push Docker Image lên Docker Hub (Mức độ: Khó)
* **Đề bài**: Viết một tệp cấu hình CI/CD hoàn chỉnh trong GitHub Actions. Mỗi khi có thẻ phiên bản mới (`tag` dạng `v*`) được tạo, tự động thực hiện build Docker Image từ mã nguồn và đẩy trực tiếp lên Docker Hub sử dụng biến bí mật Secrets.
* **Yêu cầu**: Học viên tự hoàn thành không có tài liệu mẫu.
* **Gợi ý triển khai (Workflow Hints)**:
  - Cấu hình điều kiện trigger: `on.push.tags = ["v*"]`.
  - Sử dụng các Action có sẵn: `docker/login-action` và `docker/build-push-action`.
  - Đăng ký và sử dụng tài khoản mật khẩu Docker Hub qua `secrets.DOCKER_HUB_USERNAME` và `secrets.DOCKER_HUB_TOKEN`.


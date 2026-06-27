# Chương 01: Đóng gói Container bằng Docker & Docker Compose

## 1. Deep Dive (Phân tích chuyên sâu)

### Sự khác biệt giữa VM (Virtual Machine) và Container
- **Virtual Machine (Máy ảo)**: Chạy một hệ điều hành khách (Guest OS) hoàn chỉnh trên lớp phần cứng ảo hóa. Mỗi máy ảo tốn hàng chục GB ổ cứng và hàng GB RAM chỉ để chạy hệ điều hành khách này, gây lãng phí tài nguyên và khởi động rất chậm (vài phút).
- **Docker Container**: Các container dùng chung nhân hệ điều hành (Kernel) của máy chủ (Host OS) nhưng được cô lập hoàn toàn về mặt tài nguyên và không gian bộ nhớ. Container cực kỳ nhẹ (chỉ chứa ứng dụng và thư viện phụ thuộc), khởi động trong vòng vài mili-giây và chiếm rất ít RAM.

### Cấu trúc một Dockerfile tối ưu
Dockerfile là kịch bản hướng dẫn xây dựng ảnh Docker (Image). Một Dockerfile tốt cần:
- Sử dụng base image phiên bản tối giản (ví dụ: `python:3.10-slim` thay vì `python:3.10` đầy đủ để giảm dung lượng đĩa cứng).
- Tận dụng cơ chế lưu cache layer của Docker: Cài đặt thư viện phụ thuộc trước (`pip install -r requirements.txt`) rồi mới copy file code sau. Điều này giúp tăng tốc độ build lên gấp nhiều lần ở những lần sau khi code thay đổi nhưng requirements giữ nguyên.

---

## 2. Demo: Viết Dockerfile & Docker Compose cho FastAPI Project

### Mục tiêu
Viết file cấu hình đóng gói ứng dụng FastAPI kết nối với DB PostgreSQL chạy trong container Docker đồng bộ cục bộ.

### Dockerfile (`Dockerfile`)
```dockerfile
# Bước 1: Sử dụng base image Python tối giản
FROM python:3.10-slim

# Thiết lập thư mục làm việc bên trong container
WORKDIR /app

# Cài đặt các công cụ hệ thống cần thiết cho thư viện DB
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Sao chép file danh sách thư viện và cài đặt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ mã nguồn của dự án vào container
COPY . .

# Khai báo cổng container sẽ mở ra ngoài
EXPOSE 8000

# Lệnh thực thi chính khi container khởi chạy (Uvicorn)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose (`docker-compose.yml`)
```yaml
version: '3.8'

services:
  # Dịch vụ 1: FastAPI Web Application
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://crm_user:crm_password@db:5432/crm_leads_db
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    depends_on:
      - db
    restart: always

  # Dịch vụ 2: Cơ sở dữ liệu PostgreSQL
  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=crm_user
      - POSTGRES_PASSWORD=crm_password
      - POSTGRES_DB=crm_leads_db
    ports:
      - "5432:5432"
    volumes:
      # Lưu dữ liệu database ra ổ đĩa cứng của máy chủ để tránh mất dữ liệu
      - postgres_data:/var/lib/postgresql/data
    restart: always

volumes:
  postgres_data:
```

---

## 3. Mini Project
Hãy tạo một thư mục dự án Python FastAPI đơn giản, copy Dockerfile và docker-compose.yml phía trên vào. Chạy lệnh: `docker-compose up --build` trong Terminal và kiểm chứng xem cả ứng dụng web và database có khởi chạy đồng thời thành công không. Ghi lại log khởi động.

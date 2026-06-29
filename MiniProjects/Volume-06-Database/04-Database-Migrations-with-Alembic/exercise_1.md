# Hướng dẫn khởi tạo Alembic Migration

### 1. Các lệnh cài đặt và cấu hình:
* Cài đặt: `pip install alembic`
* Khởi tạo: `alembic init alembic`
* Cấu hình URL database: Sửa dòng `sqlalchemy.url` trong file `alembic.ini` thành:
  `sqlalchemy.url = sqlite:///app_database.db`

### 2. Tạo bản Migration tự động:
* Sửa file `alembic/env.py` để liên kết `target_metadata = Base.metadata`.
* Tạo tệp migration: `alembic revision --autogenerate -m "create users table"`
* Thực thi lên database: `alembic upgrade head`
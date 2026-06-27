# Chương 04: Quản lý nâng cấp Cấu trúc Database bằng Alembic

## 1. Deep Dive (Phân tích chuyên sâu)

### Tại sao lệnh `create_all()` của SQLAlchemy thất bại khi cập nhật?
Khi bạn định nghĩa lại Class Model trong Python (ví dụ: thêm cột `phone` vào Class `User`), lệnh `Base.metadata.create_all(engine)` sẽ **KHÔNG tự động cập nhật** cột mới này vào bảng đã tồn tại trong database. Lệnh này chỉ tạo các bảng mới chưa tồn tại.

Nếu bạn drop (xóa) toàn bộ bảng đi và chạy lại `create_all()`, bạn sẽ làm mất sạch dữ liệu khách hàng hiện tại trên server Production - đây là một tai họa không thể chấp nhận.

**Alembic** giải quyết bài toán này. Nó so sánh cấu trúc Class trong code của bạn với cấu trúc thực tế của database, tự động sinh ra một file script chứa các lệnh nâng cấp (`upgrade`) và hạ cấp (`downgrade`) để cập nhật cấu trúc database mà không làm mất dữ liệu hiện có.

---

## 2. Demo: Tạo và Chạy Migration nâng cấp Schema

### Mục tiêu
Cấu hình và sử dụng Alembic để thêm cột mới `phone` vào bảng `users` đã được tạo ở Chương 3.

### Hướng dẫn thực hành từng bước bằng CLI
1. Cài đặt thư viện:
   ```bash
   pip install alembic
   ```
2. Khởi tạo môi trường Alembic trong dự án của bạn:
   ```bash
   alembic init migrations
   ```
   *Kết quả*: Hệ thống tạo ra thư mục `migrations/` và file cấu hình `alembic.ini`.
3. Mở file `alembic.ini`, chỉnh sửa đường dẫn kết nối database tại dòng `sqlalchemy.url`:
   ```ini
   sqlalchemy.url = sqlite:///orm_database.db
   ```
4. Mở file `migrations/env.py`, import class Base của bạn từ file code và gán vào biến `target_metadata` để Alembic tự động phát hiện thay đổi schema:
   ```python
   # Import mô hình của bạn
   from orm_crud import Base
   target_metadata = Base.metadata
   ```
5. Chỉnh sửa file `orm_crud.py` của bạn để thêm một cột mới vào bảng User:
   ```python
   phone = Column(String(20), nullable=True) # Cột mới thêm
   ```
6. Chạy lệnh tự động phát hiện thay đổi cấu trúc và tạo file script migration:
   ```bash
   alembic revision --autogenerate -m "Add phone column to user table"
   ```
   *Kết quả*: File script mới được tạo trong thư mục `migrations/versions/`.
7. Kiểm tra nội dung file script vừa được tạo, sau đó chạy lệnh áp dụng thay đổi vào file database thực tế:
   ```bash
   alembic upgrade head
   ```
8. Mở file database bằng công cụ quản lý DB (như DBeaver hoặc DB Browser for SQLite) và kiểm tra cột `phone` đã được thêm thành công.

---

## 3. Mini Project
Hãy viết một file script migration Alembic tiếp theo để thêm một bảng mới mang tên `logs_activity` (bao gồm: id, user_id liên kết khóa ngoại với users, action_name, created_at) vào database của bạn và thực thi lệnh áp dụng upgrade thành công. Ghi lại các lệnh terminal đã sử dụng vào file báo cáo.

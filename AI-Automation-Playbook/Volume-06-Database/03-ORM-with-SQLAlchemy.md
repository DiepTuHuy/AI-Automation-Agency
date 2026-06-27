# Chương 03: Thao tác Cơ sở dữ liệu hướng đối tượng bằng SQLAlchemy ORM

## 1. Deep Dive (Phân tích chuyên sâu)

### ORM (Object-Relational Mapping) là gì?
Viết các câu lệnh SQL thô dưới dạng chuỗi văn bản trong code Python (như `"SELECT * FROM leads WHERE budget > " + str(budget)`) rất dễ gây ra lỗi cú pháp, khó bảo trì khi dự án lớn và tạo ra lỗ hổng bảo mật nghiêm trọng (SQL Injection).

**SQLAlchemy** là thư viện ORM phổ biến nhất trong hệ sinh thái Python. Nó ánh xạ:
- Mỗi bảng (Table) trong database -> Một Class trong Python.
- Mỗi bản ghi (Row) trong bảng -> Một Object (thể hiện của Class đó).
- Mỗi cột (Column) -> Một thuộc tính của Class.

Nhờ đó, bạn có thể thực hiện mọi thao tác thêm, sửa, xóa, tìm kiếm dữ liệu hoàn toàn bằng code Python thuần túy mà không cần viết một dòng SQL nào.

---

## 2. Demo: Triển khai CRUD hoàn chỉnh bằng SQLAlchemy

### Mục tiêu
Xây dựng mô hình bảng người dùng, thực hiện kết nối database SQLite, tạo bảng và thực thi đầy đủ các thao tác: Thêm mới, Tìm kiếm, Cập nhật thông tin và Xóa dữ liệu bằng SQLAlchemy 2.0.

### Mã nguồn (`orm_crud.py`)
Yêu cầu cài đặt: `pip install sqlalchemy`

```python
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. Định nghĩa Base class phục vụ ánh xạ Declarative
Base = declarative_base()

# 2. Khai báo Class ánh xạ tới bảng 'users'
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    role = Column(String(20), default="user")

# 3. Khởi tạo engine kết nối (Sử dụng SQLite lưu file cục bộ)
engine = create_engine("sqlite:///orm_database.db", echo=True) # echo=True để hiển thị log SQL thô ra terminal

# 4. Tạo các bảng thực tế dựa trên các Class đã khai báo
Base.metadata.create_all(engine)

# 5. Khởi tạo Session factory quản lý kết nối giao dịch
SessionLocal = sessionmaker(bind=engine)

def db_operations():
    session = SessionLocal()
    
    try:
        # ---- CREATE (Thêm mới) ----
        new_user = User(username="dieptuhuy", email="huy@example.com", role="admin")
        session.add(new_user)
        session.commit() # Ghi nhận giao dịch thành công vào database
        print(f"Đã thêm user thành công! ID: {new_user.id}")
        
        # ---- READ (Tìm kiếm) ----
        # Tìm user đầu tiên có tên username là 'dieptuhuy'
        user = session.query(User).filter(User.username == "dieptuhuy").first()
        print(f"Tìm thấy: {user.username} | Email: {user.email}")
        
        # ---- UPDATE (Cập nhật) ----
        user.email = "huy.new_email@example.com"
        session.commit()
        print("Đã cập nhật email thành công!")
        
        # ---- DELETE (Xóa) ----
        # session.delete(user)
        # session.commit()
        
    except Exception as e:
        session.rollback() # Hoàn tác nếu có lỗi xảy ra
        print(f"Giao dịch thất bại, đã rollback: {e}")
    finally:
        session.close() # Luôn đóng session để trả lại kết nối cho pool

if __name__ == "__main__":
    db_operations()
```

---

## 3. Mini Project
Hãy viết một endpoint FastAPI nhận dữ liệu đăng ký khách hàng tiềm năng qua route POST, sử dụng SQLAlchemy để lưu thông tin khách hàng đó trực tiếp vào cơ sở dữ liệu SQLite, sau đó trả về thông tin ID vừa được tạo tự động từ cơ sở dữ liệu cho client.

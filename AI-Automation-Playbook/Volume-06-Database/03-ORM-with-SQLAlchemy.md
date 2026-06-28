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

### Bài tập 1: Tương tác với cơ sở dữ liệu qua SQLAlchemy ORM (Mức độ: Trung bình)
* **Đề bài**: Sử dụng SQLAlchemy để thiết kế model `Product` (id, name, price, stock) và viết script chèn một sản phẩm mới, sau đó cập nhật số lượng tồn kho của sản phẩm đó.
* **Mã nguồn mẫu (`sqlalchemy_orm.py`)**:
```python
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

# 1. Định nghĩa model ORM
class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)

if __name__ == "__main__":
    # Kết nối SQLite trong bộ nhớ phục vụ test nhanh
    engine = create_engine('sqlite:///:memory:', echo=False)
    Base.metadata.create_all(engine)
    
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # 2. Thêm sản phẩm mới
    new_prod = Product(name="Bàn phím Leopold", price=150.0, stock=20)
    session.add(new_prod)
    session.commit()
    print(f"Đã thêm sản phẩm: {new_prod.name} (ID: {new_prod.id})")
    
    # 3. Cập nhật số lượng tồn kho
    prod_to_update = session.query(Product).filter_by(name="Bàn phím Leopold").first()
    prod_to_update.stock = 15
    session.commit()
    print(f"Đã cập nhật tồn kho mới: {prod_to_update.stock} chiếc.")
```

### Bài tập 2: Truy vấn sản phẩm bán chạy với quan hệ một-nhiều (Mức độ: Khó)
* **Đề bài**: Thiết kế thêm model `Order` liên kết với `Product` qua khóa ngoại. Viết truy vấn sử dụng SQLAlchemy ORM để tìm tất cả các đơn hàng chứa sản phẩm có đơn giá lớn hơn 100 USD.
* **Yêu cầu**: Học viên tự hoàn thành không có code mẫu.
* **Gợi ý triển khai (Workflow Hints)**:
  1. Thêm khóa ngoại `product_id = Column(Integer, ForeignKey('products.id'))` trong class `Order`.
  2. Sử dụng SQLAlchemy `session.query(Order).join(Product).filter(Product.price > 100).all()` để lọc dữ liệu.


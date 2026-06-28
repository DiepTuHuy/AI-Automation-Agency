# Chương 02: Thiết lập SQLite & PostgreSQL trong dự án Python

## 1. Deep Dive (Phân tích chuyên sâu)

### SQLite vs PostgreSQL: Khi nào dùng?
| Đặc điểm | SQLite | PostgreSQL |
| :--- | :--- | :--- |
| **Kiến trúc** | File-based (Toàn bộ DB lưu trong 1 file `.db` duy nhất) | Server-client (Chạy như một dịch vụ mạng độc lập) |
| **Cài đặt** | Tích hợp sẵn trong Python, không cần cài đặt gì thêm | Cần cài đặt phần mềm PostgreSQL và cấu hình cổng kết nối |
| **Phù hợp** | Môi trường Dev, ứng dụng nhỏ, kiểm thử tự động | Môi trường Production, hệ thống xử lý đồng thời lớn |
| **Mở rộng** | Giới hạn khi ghi đồng thời (chỉ cho phép 1 tiến trình ghi tại 1 thời điểm) | Hỗ trợ hàng nghìn kết nối đồng thời cực tốt |

---

## 2. Demo: Tương tác CSDL SQLite bằng thư viện `sqlite3` của Python

### Mục tiêu
Viết một script Python sử dụng thư viện tích hợp sẵn `sqlite3` để khởi tạo database, chèn thông tin lead tự động và truy vấn dữ liệu ra màn hình.

### Mã nguồn (`sqlite_demo.py`)
```python
import sqlite3

def run_db_operations():
    # 1. Kết nối tới file database SQLite (nếu chưa có file sẽ tự động tạo mới)
    conn = sqlite3.connect("leads_database.db")
    
    # 2. Khởi tạo đối tượng cursor để thực thi các câu lệnh SQL
    cursor = conn.cursor()
    
    # 3. Tạo bảng leads
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            budget INTEGER
        )
    """)
    
    # 4. Chèn dữ liệu (Sử dụng dấu ? để phòng ngừa lỗi SQL Injection bảo mật)
    try:
        cursor.execute(
            "INSERT INTO leads (name, email, budget) VALUES (?, ?, ?)",
            ("Huy AI", "huy@antigravity.vn", 7500)
        )
        # Lưu lại thay đổi vào file đĩa cứng
        conn.commit()
        print("Đã chèn dữ liệu lead mới thành công!")
    except sqlite3.IntegrityError:
        print("Email đã tồn tại trong database, bỏ qua bước chèn.")
        
    # 5. Truy vấn đọc dữ liệu ra
    cursor.execute("SELECT * FROM leads WHERE budget >= ?", (5000,))
    rows = cursor.fetchall()
    
    print("\nDanh sách lead ngân sách lớn:")
    for row in rows:
        print(f"ID: {row[0]} | Tên: {row[1]} | Email: {row[2]} | Ngân sách: {row[3]} USD")
        
    # 6. Đóng kết nối để giải phóng tài nguyên file khóa
    conn.close()

if __name__ == "__main__":
    run_db_operations()
```

---

## 3. Mini Project

### Bài tập 1: Kết nối và tương tác với SQLite bằng Python (Mức độ: Trung bình)
* **Đề bài**: Viết một script Python sử dụng thư viện `sqlite3` để tạo một database cục bộ, tạo bảng lưu thông tin người dùng và chèn dữ liệu mẫu vào bảng.
* **Mã nguồn mẫu (`sqlite_connector.py`)**:
```python
import sqlite3

def init_db():
    # Kết nối đến file database SQLite cục bộ
    conn = sqlite3.connect("users_database.db")
    cursor = conn.cursor()
    
    # Tạo bảng
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        role TEXT DEFAULT 'user'
    )
    """)
    
    # Chèn dữ liệu mẫu
    cursor.execute("INSERT INTO users (username, role) VALUES ('admin_huy', 'admin')")
    cursor.execute("INSERT INTO users (username, role) VALUES ('student_a', 'user')")
    conn.commit()
    
    # Truy vấn hiển thị dữ liệu
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    print("Danh sách user trong SQLite:")
    for r in rows:
        print(f"ID: {r[0]}, Username: {r[1]}, Role: {r[2]}")
        
    conn.close()

if __name__ == "__main__":
    init_db()
```

### Bài tập 2: Quản lý kết nối PostgreSQL bằng Connection Pool (Mức độ: Khó)
* **Đề bài**: Viết một script Python sử dụng thư viện `psycopg2` để kết nối đến một database PostgreSQL từ xa. Sử dụng `SimpleConnectionPool` để tối ưu quản lý kết nối khi có nhiều truy vấn xảy ra đồng thời.
* **Yêu cầu**: Học viên tự hoàn thành không có code mẫu.
* **Gợi ý triển khai (Workflow Hints)**:
  1. Sử dụng thư viện `psycopg2.pool.SimpleConnectionPool` để mở pool kết nối tối thiểu là 1 và tối đa là 10.
  2. Sử dụng cấu trúc `try-except-finally` để lấy kết nối ra từ pool và trả lại pool sau khi thực thi thành công.


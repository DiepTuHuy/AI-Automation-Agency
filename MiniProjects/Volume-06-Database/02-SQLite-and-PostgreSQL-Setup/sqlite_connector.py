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
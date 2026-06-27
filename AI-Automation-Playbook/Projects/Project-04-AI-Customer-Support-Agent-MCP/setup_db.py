import sqlite3

def init_db():
    conn = sqlite3.connect("orders.db")
    cursor = conn.cursor()
    
    # Tạo bảng đơn hàng
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id TEXT PRIMARY KEY,
            customer_name TEXT,
            product TEXT,
            status TEXT,
            price REAL
        )
    """)
    
    # Chèn dữ liệu mẫu
    cursor.execute("INSERT OR REPLACE INTO orders VALUES ('OR-111', 'Nguyen Van A', 'Khoa hoc AI Automation', 'da_giao_hang', 2500000.0)")
    cursor.execute("INSERT OR REPLACE INTO orders VALUES ('OR-222', 'Tran Thi B', 'AI Chatbot Setup', 'dang_van_chuyen', 15000000.0)")
    
    conn.commit()
    conn.close()
    print("Đã tạo và nạp dữ liệu mẫu vào orders.db!")

if __name__ == "__main__":
    init_db()

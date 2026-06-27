# Chương 01: Nguyên lý Cơ sở dữ liệu Quan hệ & Truy vấn SQL căn bản

## 1. Deep Dive (Phân tích chuyên sâu)

### Tại sao File văn bản và JSON thất bại trong Production?
Khi mới bắt đầu, bạn có thể nghĩ: *"Tại sao không lưu thông tin khách hàng vào một file `leads.json` cho đơn giản?"*.
Cách tiếp cận này sẽ sụp đổ ngay khi:
1. **Xử lý đồng thời (Concurrency)**: Khi có 2 người dùng đăng ký cùng một mili-giây, cả hai tiến trình Python sẽ cùng mở file JSON, ghi đè lên nhau, gây ra hiện tượng mất mát dữ liệu (Race Condition).
2. **Hiệu năng truy vấn (Performance)**: Khi file đạt 100,000 dòng, để tìm kiếm một khách hàng có email cụ thể, Python buộc phải tải toàn bộ file vào RAM và duyệt qua từng dòng (độ phức tạp $O(N)$) -> gây chậm và tốn tài nguyên.
3. **Mối quan hệ dữ liệu**: Rất khó để liên kết thông tin giữa các file JSON độc lập mà không viết hàng trăm dòng code xử lý thủ công.

### Cơ sở dữ liệu quan hệ (RDBMS)
RDBMS giải quyết triệt để các vấn đề trên nhờ lưu trữ dữ liệu dạng bảng biểu có cấu trúc nghiêm ngặt và hỗ trợ giao dịch (Transactions) đảm bảo an toàn dữ liệu tuyệt đối (chuẩn ACID).

Các từ khóa cốt lõi cần nhớ:
- **Table (Bảng)**: Tập hợp các bản ghi có cùng cấu trúc.
- **Primary Key (Khóa chính)**: Một cột duy nhất dùng để định danh cho từng dòng trong bảng (thường là số nguyên tự tăng hoặc chuỗi UUID).
- **Foreign Key (Khóa ngoại)**: Một cột trong bảng này trỏ đến Khóa chính của bảng khác để thiết lập mối quan hệ.

---

## 2. Demo: Truy vấn SQL thực tế

### Mục tiêu
Viết các câu lệnh SQL để khởi tạo cấu trúc cơ bản và thực hiện các câu lệnh truy vấn liên kết dữ liệu giữa khách hàng và đơn hàng.

### Các câu lệnh SQL mẫu (`queries.sql`)
```sql
-- 1. Tạo bảng Khách hàng
CREATE TABLE customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Tạo bảng Đơn hàng (Có khóa ngoại liên kết tới bảng Khách hàng)
CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    product_name TEXT NOT NULL,
    price REAL NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

-- 3. Chèn dữ liệu mẫu
INSERT INTO customers (name, email) VALUES ('Nguyen Van A', 'a@example.com');
INSERT INTO customers (name, email) VALUES ('Tran Thi B', 'b@example.com');

INSERT INTO orders (customer_id, product_name, price) VALUES (1, 'Khóa học AI Automation', 2500000);
INSERT INTO orders (customer_id, product_name, price) VALUES (1, 'Tư vấn AI Agent', 10000000);

-- 4. Truy vấn kết nối JOIN lấy danh sách đơn hàng kèm tên khách hàng tương ứng
SELECT 
    orders.id AS order_id,
    customers.name AS customer_name,
    orders.product_name,
    orders.price
FROM orders
INNER JOIN customers ON orders.customer_id = customers.id;
```

---

## 3. Mini Project
Hãy viết một kịch bản SQL thiết lập cơ sở dữ liệu lưu lịch sử chat của AI Chatbot. Bao gồm bảng `conversations` (Lưu thông tin phiên chat: ID, Tên người dùng) và bảng `messages` (Lưu các tin nhắn trong phiên chat đó: ID, ID phiên chat, Người gửi là User/Assistant, Nội dung tin nhắn, Thời gian gửi). Viết câu lệnh truy vấn lấy toàn bộ lịch sử tin nhắn của một phiên chat cụ thể dựa trên ID.

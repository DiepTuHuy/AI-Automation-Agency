-- 1. Tạo bảng khách hàng
CREATE TABLE customers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE
);

-- 2. Tạo bảng đơn hàng
CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    order_date DATE,
    total_amount REAL,
    FOREIGN KEY(customer_id) REFERENCES customers(id)
);

-- 3. Truy vấn SQL tính tổng doanh thu theo từng khách hàng
SELECT c.name, SUM(o.total_amount) as total_spent
FROM customers c
LEFT JOIN orders o ON c.id = o.customer_id
GROUP BY c.id;
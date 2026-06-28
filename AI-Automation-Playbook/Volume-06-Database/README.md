# Volume 06: Database - Lưu Trữ & Quản Lý Dữ Liệu Bền Vững

Hệ thống tự động hóa không thể lưu trữ toàn bộ lịch sử trò chuyện, thông tin hóa đơn và cấu hình khách hàng vào các tệp tin text hay biến nhớ RAM tạm thời. Khi server khởi động lại hoặc gặp sự cố, dữ liệu đó sẽ biến mất hoàn toàn. Để xây dựng hệ thống cấp Production, kỹ sư AI Automation bắt buộc phải hiểu cách thiết kế, lưu trữ và truy vấn dữ liệu thông qua các Hệ quản trị cơ sở dữ liệu quan hệ (RDBMS). Volume này hướng dẫn bạn từ các câu lệnh SQL cơ bản, thiết lập SQLite và PostgreSQL, đến cách tương tác với DB bằng ORM (SQLAlchemy) và quản lý thay đổi schema bằng Alembic.

---

## 1. Learning Objectives (Mục tiêu học tập)
Sau khi hoàn thành Volume này, bạn sẽ:
- **Làm chủ thiết kế DB**: Hiểu rõ mô hình thực thể quan hệ, khóa chính (Primary Key), khóa ngoại (Foreign Key) và các loại mối quan hệ bảng.
- **Thực thi SQL cơ bản**: Viết thành thạo các câu lệnh truy vấn SQL (CRUD: Create, Read, Update, Delete) và các phép kết nối bảng (JOIN).
- **Phân biệt hệ CSDL**: Biết cách chọn và cài đặt SQLite cho môi trường dev và PostgreSQL cho môi trường production.
- **Tương tác CSDL bằng Code**: Sử dụng SQLAlchemy (ORM) để thao tác với cơ sở dữ liệu dưới dạng các Object Python thuần túy.
- **Quản lý lịch sử Schema**: Sử dụng Alembic để tạo và áp dụng các bản cập nhật cấu trúc cơ sở dữ liệu (Database Migrations) an toàn.

---

## 2. Prerequisites (Điều kiện tiên quyết)
- Hoàn thành Volume 03 (Python Automation).
- Đã cài đặt Python và biết cách chạy các script Python cục bộ.

---

## 3. Big Picture (Bức tranh tổng thể)
Cơ sở dữ liệu là "Trí nhớ dài hạn" của hệ thống AI Automation. Nó lưu trữ thông tin khách hàng, lịch sử chat của Agent, và trạng thái của các task chạy ngầm để FastAPI và n8n có thể truy cập bất kỳ lúc nào.

```
[FastAPI Backend / n8n Workflow]
      │
      ├─(SQLAlchemy ORM)
      │
      ▼
[Database Engine]
   ├── SQLite (Local Development)
   └── PostgreSQL (Cloud Production)
```

---

## 4. First Principles (Nguyên lý gốc)
- **Dữ liệu có tính toàn vẹn (Data Integrity)**: Dữ liệu lưu trong DB phải tuân thủ nghiêm ngặt các ràng buộc kiểu dữ liệu, khóa chính và khóa ngoại để ngăn chặn hiện tượng dữ liệu rác hoặc mâu thuẫn lẫn nhau.
- **Khóa ngoại là sợi dây liên kết**: Không có bảng dữ liệu nào đứng độc lập trong một hệ thống doanh nghiệp. Khóa ngoại giúp duy trì mối quan hệ chặt chẽ giữa các thực thể (ví dụ: một hóa đơn phải thuộc về một khách hàng cụ thể).
- **Schema Evolution (Tiến hóa cấu trúc)**: Cấu trúc cơ sở dữ liệu sẽ thay đổi liên tục theo thời gian phát triển dự án. Sử dụng migration tool (Alembic) là cách duy nhất để cập nhật cấu trúc DB mà không làm mất dữ liệu hiện có của khách hàng.

---

## 5. Mental Models (Mô hình tư duy)
- **Tủ hồ sơ của thủ thư (Relational Database)**: Hãy tưởng tượng cơ sở dữ liệu giống như một phòng lưu trữ hồ sơ của thư viện. Mỗi bảng (Table) là một ngăn tủ chứa các kẹp hồ sơ cùng loại (ví dụ ngăn tủ chứa Hồ sơ độc giả, ngăn tủ chứa Danh mục sách). Khóa ngoại giống như một tấm thẻ ghi chú gắn trên hồ sơ sách: *"Cuốn sách này hiện đang được mượn bởi độc giả có ID là 123"*, giúp thủ thư nhanh chóng kết nối thông tin giữa các tủ hồ sơ mà không cần chép lại thông tin độc giả vào hồ sơ sách.

---

## 6. Core Concepts (Khái niệm cốt lõi)
1. **RDBMS**: Hệ quản trị cơ sở dữ liệu quan hệ (như SQLite, PostgreSQL, MySQL) lưu trữ dữ liệu dưới dạng các bảng hai chiều có cấu trúc nghiêm ngặt.
2. **ORM (Object-Relational Mapping)**: Kỹ thuật lập trình cho phép ánh xạ các bảng trong database thành các Class trong Python, biến các truy vấn SQL thô thành các thao tác hướng đối tượng.
3. **Database Migration**: Quá trình lưu vết và áp dụng các thay đổi về mặt cấu trúc (schema) của database theo thời gian (giống như Git dành cho database).

---

## 8. Best Practices (Quy chuẩn thực chiến)
- **Luôn đóng Session/Connection**: Sử dụng context manager hoặc tắt session sau khi thực hiện truy vấn để tránh rò rỉ kết nối (Connection Leak) làm cạn kiệt tài nguyên DB.
- **Sử dụng Connection Pooling**: Trong production, cấu hình Pooling (ví dụ qua SQLAlchemy) để tái sử dụng các kết nối cũ, giảm thiểu chi phí khởi tạo kết nối mới cho mỗi request.
- **Index các cột hay tìm kiếm**: Tạo chỉ mục (Index) cho các cột thường xuyên nằm trong điều kiện tìm kiếm (như `email`, `phone`, `created_at`) để tăng tốc độ truy vấn lên gấp hàng trăm lần.

---

## 9. Common Mistakes (Sai lầm thường gặp)
- **Thay đổi trực tiếp Schema trên database Production bằng lệnh SQL thủ công**: Dẫn đến việc code dev và database production bị lệch cấu trúc (mismatch), gây lỗi sập hệ thống khi deploy code mới. *Cách sửa*: Luôn thực hiện thay đổi schema thông qua Alembic migrations.
- **Lỗi N+1 Query**: Gọi truy vấn lấy danh sách 100 khách hàng, sau đó chạy vòng lặp 100 lần để gọi thêm 100 truy vấn lấy thông tin hóa đơn của từng khách hàng. *Cách sửa*: Sử dụng kỹ thuật Eager Loading (`joinedload` trong SQLAlchemy) để lấy toàn bộ dữ liệu chỉ với 1 câu lệnh JOIN duy nhất.

---

## 10. Engineering Mindset (Tư duy kỹ sư)
Một kỹ sư cơ sở dữ liệu giỏi luôn thiết kế schema hướng tới tương lai. Họ không chỉ hỏi: *"Bảng này cần lưu cái gì bây giờ?"* Họ hỏi: *"Mối quan hệ giữa các bảng này là gì? Nếu sau này khách hàng có nhiều dự án, và mỗi dự án có nhiều hóa đơn, thiết kế hiện tại có bị phá vỡ không?"*

---

## 13. Capstone Project (Dự án kết khóa Volume)
Xem mô tả chi tiết tại [Project-02](file:///Users/dieptuhuy/Documents/AI%20Automation/AI-Automation-Playbook/Projects/Project-02-AI-CRM-Automation-Lead-Qualification/README.md).

---

## 14. Review Questions (Bloom Taxonomy - 30 câu hỏi)
### Level 1 — Remember (Nhớ)
1. Cơ sở dữ liệu quan hệ (RDBMS) là gì?
2. Khóa chính (Primary Key) là gì?
3. Khóa ngoại (Foreign Key) là gì?
4. SQL là viết tắt của từ gì?
5. Alembic là công cụ dùng để làm gì?

### Level 2 — Understand (Hiểu)
6. Giải thích sự khác biệt giữa SQLite và PostgreSQL. Khi nào nên chuyển từ SQLite sang PostgreSQL?
7. Ưu điểm và nhược điểm của việc sử dụng ORM so với viết câu lệnh SQL thô là gì?
8. Giải thích mối quan hệ Một-nhiều (One-to-Many) và Nhiều-nhiều (Many-to-Many). Cho ví dụ thực tế.
9. Tại sao chúng ta cần sử dụng Database Migration thay vì chỉ cần drop và tạo lại bảng mới?
10. Eager Loading và Lazy Loading trong ORM khác nhau thế nào?

### Level 3 — Apply (Áp dụng)
11. Viết câu lệnh SQL tạo bảng `customers` gồm có: `id` (khóa chính, tự tăng), `name` (văn bản), `email` (văn bản, duy nhất), và `created_at` (thời gian mặc định hiện tại).
12. Viết câu lệnh SQL chèn một khách hàng mới và câu lệnh lấy tất cả khách hàng đăng ký trong ngày hôm nay.
13. Định nghĩa một SQLAlchemy model trong Python đại diện cho thực thể `Customer` trên.
14. Khởi tạo cấu hình Alembic trong thư mục dự án của bạn bằng Terminal.
15. Viết một script Python sử dụng SQLAlchemy session để thực hiện cập nhật email của một khách hàng có ID là 1.

### Level 4 — Analyze (Phân tích)
16. Phân tích nguyên nhân tại sao việc không sử dụng Index cho cột `email` lại làm chậm hệ thống khi số lượng dòng dữ liệu đạt đến con số 1 triệu dòng.
17. So sánh hiệu năng và độ phức tạp khi thực hiện phép tính tổng doanh thu bằng lệnh SQL `SUM` trực tiếp trong database so với tải toàn bộ dữ liệu về Python để tính bằng vòng lặp.
18. Đánh giá rủi ro khi dính lỗi SQL Injection khi ghép chuỗi SQL thủ công từ dữ liệu người dùng nhập và cách ORM phòng chống lỗi này mặc định.
19. Phân tích tại sao việc xóa một dòng trong bảng Cha (ví dụ: Khách hàng) lại có thể gây ra lỗi vi phạm ràng buộc khóa ngoại ở bảng Con (ví dụ: Hóa đơn).
20. Tại sao việc lưu trữ mật khẩu dưới dạng văn bản thô (Plaintext) trong database lại là một thảm họa bảo mật và cách dùng thuật toán băm (Hashing) để khắc phục?

### Level 5 — Design (Thiết kế)
21. Thiết kế cơ sở dữ liệu quan hệ cho một hệ thống AI Chatbot gồm các bảng: `users`, `conversations`, `messages` đảm bảo tối ưu hóa truy vấn lấy lịch sử chat theo cuộc hội thoại.
22. Đề xuất sơ đồ DB phục vụ quản lý bán hàng của một cửa hàng thương mại điện tử đơn giản (Khách hàng, Sản phẩm, Đơn hàng, Chi tiết đơn hàng).
23. Thiết kế file migration Alembic bổ sung thêm cột `avatar_url` (cho phép trống) vào bảng `users` đã có dữ liệu.
24. Đề xuất quy trình sao lưu (Backup) tự động hàng ngày cho database PostgreSQL chạy trên VPS.
25. Thiết kế cơ chế "Xóa mềm" (Soft Delete - sử dụng cột `is_deleted`) để tránh việc nhân viên lỡ tay xóa mất dữ liệu quan trọng của khách hàng.

### Level 6 — Evaluate (Đánh giá)
26. Đánh giá tính hiệu quả của việc chuyển dịch cơ sở dữ liệu của một startup từ PostgreSQL sang mô hình NoSQL như MongoDB khi sản phẩm thay đổi cấu trúc dữ liệu liên tục.
27. Đánh giá sự đánh đổi giữa tính nhất quán dữ liệu nghiêm ngặt (ACID) và tốc độ ghi dữ liệu của hệ thống.
28. Kiểm chứng độ an toàn của một phiên bản migration Alembic khi chạy nâng cấp (upgrade) và hạ cấp (downgrade) thử nghiệm trên database Staging trước khi lên Production.
29. Đánh giá mức độ ảnh hưởng của việc khóa bảng (Table Locking) khi thực hiện cập nhật schema lớn đối với trải nghiệm của người dùng đang truy cập hệ thống thời gian thực.
30. Lập luận bác bỏ hoặc đồng ý với quan điểm: *"Kỹ sư AI Automation chỉ cần biết sử dụng n8n để lưu dữ liệu vào Google Sheets là đủ, không cần học SQL hay cơ sở dữ liệu phức tạp"*.

---

## 15. Checklist hoàn thành
- [ ] Hiểu rõ mô hình cơ sở dữ liệu quan hệ và các phép JOIN.
- [ ] Viết được mã nguồn SQLAlchemy kết nối thành công với SQLite/PostgreSQL.
- [ ] Thực hiện thành thạo các thao tác CRUD thông qua SQLAlchemy Session.
- [ ] Tạo và chạy thành công migration Alembic để cập nhật cấu trúc database.
- [ ] Hoàn thành Capstone Project (Project 02).

---

## 16. Resources (Tài liệu tham khảo)
- **SQLAlchemy**: [SQLAlchemy Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html)
- **Alembic**: [Alembic Documentation](https://alembic.sqlalchemy.org/en/latest/)
- **Học SQL**: [W3Schools SQL Tutorial](https://www.w3schools.com/sql/)
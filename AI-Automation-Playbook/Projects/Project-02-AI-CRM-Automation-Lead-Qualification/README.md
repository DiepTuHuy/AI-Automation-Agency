# Project 02: AI CRM Automation & Lead Qualification

Dự án này kết hợp kiến thức từ Volume 04 (FastAPI), Volume 05 (n8n) và Volume 06 (Database) để xây dựng hệ thống tự động hóa tiếp nhận khách hàng tiềm năng (leads), chấm điểm và phân loại lead bằng AI (Lead Qualification), lưu trữ bền vững vào cơ sở dữ liệu và thông báo cho phòng Sales.

---

## 1. Architecture Diagram (Kiến trúc hệ thống)

```
[Khách hàng điền Form]
           │
           ▼ (Webhook)
    [n8n Workflow]
           │
           ├─(HTTP POST /api/v1/leads)
           │
           ▼
    [FastAPI Server]
           │
           ├─(Gọi LLM gemini-2.5-flash đánh giá chất lượng lead dựa trên budget & mô tả)
           │
           ├─(SQLAlchemy ORM) ──> [Lưu DB SQLite/PostgreSQL]
           │
           ▼ (Trả kết quả JSON qualification)
    [n8n Workflow (Tiếp tục)]
           │
           ├── (Nếu Lead tốt) ──> [Telegram Alert cho Sales]
           └── (Nếu Lead xấu) ──> [Google Sheets Lưu trữ lưu vết]
```

---

## 2. Source Tree (Cấu trúc mã nguồn)
```
Project-02-AI-CRM-Automation-Lead-Qualification/
├── README.md
├── requirements.txt
├── .env.example
├── db.py
├── models.py
├── main.py
└── workflow.json
```

---

## 3. Deployment Guide (Hướng dẫn triển khai)

### Bước 1: Chuẩn bị môi trường
1. Kích hoạt môi trường ảo:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. Cài đặt các thư viện phụ thuộc:
   ```bash
   pip install -r requirements.txt
   ```

### Bước 2: Cấu hình biến môi trường
1. Sao chép và cấu hình file `.env`:
   ```bash
   cp .env.example .env
   ```
2. Điền các khóa bảo mật cần thiết vào file `.env`:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   SYSTEM_API_KEY=crm_secret_key_123
   DATABASE_URL=sqlite:///crm_leads.db
   ```

### Bước 3: Chạy ứng dụng FastAPI
Chạy server bằng Uvicorn:
```bash
python3 main.py
```
*Giao diện tài liệu Swagger sẽ sẵn sàng tại `http://127.0.0.1:8000/docs`*.

### Bước 4: Thiết lập n8n Workflow
1. Mở n8n của bạn, tạo workflow mới.
2. Sử dụng tính năng **Import from File** và chọn file `workflow.json` trong thư mục này.
3. Kích hoạt (Active) workflow và test gửi lead thực tế từ biểu mẫu.

---

## 4. Lessons Learned (Bài học rút ra)
- **Tách biệt Database Layer**: Việc cấu hình file `db.py` và `models.py` độc lập giúp dễ dàng chuyển đổi từ SQLite sang PostgreSQL khi scale hệ thống lớn mà không cần sửa code API chính.
- **Bảo mật Server-to-Server**: Sử dụng `SYSTEM_API_KEY` tĩnh trong header giúp ngăn chặn người ngoài gửi request ảo vào API của bạn để spam dữ liệu.
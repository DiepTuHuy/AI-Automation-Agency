# Project 04: AI Customer Support Agent with MCP

Dự án này tích hợp kiến thức từ Volume 10 (MCP), Volume 11 (Deployment) và Volume 12 (Production Engineering) để xây dựng một hệ thống Trợ lý ảo Hỗ trợ khách hàng tự hành (Customer Support Agent) được kết nối với hệ thống cơ sở dữ liệu nội bộ thông qua giao thức Model Context Protocol (MCP).

---

## 1. Architecture Diagram (Kiến trúc hệ thống)

```
[Khách hàng gõ câu hỏi: "Kiểm tra đơn hàng OR-999"]
                     │
                     ▼
             [client.py (Client)] ──(Tự động kích hoạt Tracing LangSmith)
                     │
             (JSON-RPC qua STDIO)
                     │
            [server.py (MCP Server)]
                     │
             (Query SQLite orders.db)
                     │
                     ▼
       [Trả kết quả cho Client & LLM] ──> [Trả lời người dùng]
```

---

## 2. Source Tree (Cấu trúc mã nguồn)
```
Project-04-AI-Customer-Support-Agent-MCP/
├── README.md
├── requirements.txt
├── .env.example
├── server.py
├── client.py
└── setup_db.py
```

---

## 3. Deployment Guide (Hướng dẫn triển khai)

### Bước 1: Khởi tạo database mẫu
Chạy script tạo file database SQLite chứa thông tin đơn hàng giả lập để test:
```bash
python3 setup_db.py
```
*Kết quả*: Tạo file `orders.db` chứa 2 đơn hàng mẫu.

### Bước 2: Cài đặt thư viện phụ thuộc
```bash
pip install -r requirements.txt
```

### Bước 3: Chạy chương trình Client giả lập cuộc chat
Thực thi client:
```bash
python3 client.py
```
*Client sẽ tự động khởi chạy server.py ngầm làm MCP subprocess qua STDIO, kết nối với OpenAI, giải quyết câu hỏi kiểm tra đơn hàng và in kết quả ra terminal*.

---

## 4. Lessons Learned (Bài học rút ra)
- **Tương tác cục bộ qua STDIO cực kỳ an toàn**: Không cần mở cổng port internet hay cấu hình xác thực token phức tạp cho server, luồng dữ liệu chạy hoàn toàn cô lập trong tiến trình con của hệ điều hành.
- **Log debug qua STDERR**: Việc ghi log debug ra file hoặc luồng STDERR giúp giữ luồng STDOUT hoàn toàn sạch để truyền tin nhắn giao thức JSON-RPC.

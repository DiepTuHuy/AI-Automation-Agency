# Chương 02: Kiến trúc Máy chủ MCP & Các lớp Truyền tải

## 1. Deep Dive (Phân tích chuyên sâu)

### 3 Thành phần chính trong kiến trúc MCP
1. **MCP Host**: Ứng dụng gốc nơi người dùng tương tác với AI (như Claude Desktop App, Cursor IDE, Web App). Host chứa Client.
2. **MCP Client**: Thành phần chạy bên trong Host, chịu trách nhiệm thiết lập kết nối bảo mật, gửi yêu cầu JSON-RPC và chuyển kết quả nhận được cho LLM.
3. **MCP Server**: Chương trình độc lập (viết bằng Python, NodeJS, Go...) chạy ngầm trong hệ thống, trực tiếp thực thi mã nguồn để đọc ghi file, truy cập mạng hoặc query database.

### 2 Lớp truyền tải dữ liệu (Transport Layers)
Giao thức MCP hỗ trợ hai kênh truyền tải chính tùy thuộc vào vị trí của máy chủ:
1. **STDIO Transport**: Client khởi chạy server như một tiến trình con (Subprocess) trực tiếp trên máy tính. Dữ liệu JSON-RPC được truyền trực tiếp qua luồng dữ liệu chuẩn **Standard Input/Output**. 
   - *Ưu điểm*: Cực kỳ an toàn vì không mở cổng mạng ra Internet, không sợ bị hacker tấn công từ xa. Tốc độ truyền tải tức thì.
2. **SSE Transport (Server-Sent Events)**: Dùng khi MCP Server được host online trên đám mây (Cloud). Kết nối được thiết lập qua giao thức HTTP, Server đẩy dữ liệu cập nhật về Client qua SSE stream, và Client gửi lại yêu cầu qua HTTP POST.

---

## 2. Demo: Cấu trúc thư mục của một MCP Server chuẩn bằng Python

### Mục tiêu
Khởi tạo cấu trúc dự án chuẩn để xây dựng máy chủ MCP sử dụng thư viện SDK chính thức của Anthropic.

### Source Tree chuẩn
```
mcp-server-demo/
├── .venv/
├── .env
├── pyproject.toml
└── server.py
```

### Nội dung cấu hình môi trường (`pyproject.toml`)
```toml
[project]
name = "mcp-server-demo"
version = "0.1.0"
description = "Custom MCP Server for Python Automation"
readme = "README.md"
requires-python = ">=3.10"
dependencies = [
    "mcp>=1.0.0",
]
```

---

## 3. Mini Project
Hãy tạo thư mục dự án theo cấu trúc trên trên máy tính của bạn. Tạo môi trường ảo `.venv`, cài đặt thư viện `mcp` và kiểm tra xem thư viện đã được cài đặt thành công không bằng lệnh: `pip show mcp`. Ghi lại thông tin phiên bản thư viện nhận được.

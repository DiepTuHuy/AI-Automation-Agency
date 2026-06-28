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

### Bài tập 1: Mô tả sơ đồ truyền nhận bản tin trong MCP Protocol (Mức độ: Trung bình)
* **Đề bài**: Hãy vẽ sơ đồ hoặc viết đặc tả mô phỏng quy trình trao đổi dữ liệu JSON-RPC giữa Client (Claude Desktop) và Host MCP Server khi thực hiện gọi một Tool.
* **Tài liệu sườn mẫu**:
```markdown
# Bản tin JSON-RPC gọi Tool trong MCP

### 1. Request từ Client gửi lên Server:
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "get_current_time",
    "arguments": {}
  },
  "id": 1
}
```

### 2. Response từ Server trả về:
```json
{
  "jsonrpc": "2.0",
  "result": {
    "content": [
      {
        "type": "text",
        "text": "Thời gian hiện tại: 15:30"
      }
    ]
  },
  "id": 1
}
```
```

### Bài tập 2: Thiết kế đặc tả gói tin cho một MCP Server quản lý nhắc nhở (Mức độ: Khó)
* **Đề bài**: Thiết kế bản tin JSON-RPC chuẩn MCP cho một kịch bản: Client yêu cầu Server tạo một lời nhắc công việc mới với các tham số: `task_name`, `due_date`, và `priority`. Hãy viết chi tiết cấu trúc Request và Response tương ứng.
* **Yêu cầu**: Học viên tự hoàn thành không có tài liệu mẫu.
* **Gợi ý triển khai (Workflow Hints)**:
  - Định nghĩa trường `method` là `tools/call`.
  - Đóng gói các tham số yêu cầu bên trong `params.arguments`.
  - Phản hồi chứa thông tin trạng thái thành công kèm theo ID của reminder vừa tạo.


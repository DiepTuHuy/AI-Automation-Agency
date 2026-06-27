# Chương 01: Giới thiệu giao thức Model Context Protocol (MCP)

## 1. Deep Dive (Phân tích chuyên sâu)

### Bài toán phân mảnh công nghiệp AI
Trước khi tiêu chuẩn MCP ra đời, hệ sinh thái AI gặp phải một vấn đề lớn:
- Bạn viết một Agent tuyệt vời có khả năng đọc Database SQL bằng Python code.
- Nếu bạn muốn đưa Agent đó vào Cursor IDE, bạn phải viết lại code định nghĩa tool theo chuẩn của Cursor.
- Nếu muốn đưa vào Claude Desktop, bạn phải cấu hình theo chuẩn của Anthropic.
- Nếu đưa vào một Web App tự xây, bạn lại phải viết một adapter API riêng.

Điều này tạo ra sự lãng phí tài nguyên lập trình cực lớn.

### Giải pháp MCP (Model Context Protocol)
MCP định nghĩa một **Giao thức chuẩn chung** (tương tự như cách chuẩn HTTP định nghĩa cách web client giao tiếp với web server).
- Chỉ cần viết một **MCP Server** duy nhất (ví dụ: máy chủ kết nối Database).
- Mọi **MCP Client** (như Cursor, Claude Desktop, các AI framework) đều có thể cắm trực tiếp vào server này và tự động nhận diện danh sách công cụ mà không cần cấu hình lại mã nguồn.

---

## 2. Demo: Phân tích luồng hoạt động JSON-RPC 2.0

### Mục tiêu
Hiểu rõ cấu trúc tin nhắn JSON-RPC 2.0 truyền qua lại giữa Client và Server khi thực hiện tác vụ gọi công cụ.

### Ví dụ luồng gói tin thực tế
1. **Client gửi yêu cầu lấy danh sách công cụ (Tools List Request)**:
   ```json
   {
     "jsonrpc": "2.0",
     "method": "tools/list",
     "id": 1
   }
   ```
2. **Server phản hồi danh sách công cụ có sẵn (Tools List Response)**:
   ```json
   {
     "jsonrpc": "2.0",
     "result": {
       "tools": [
         {
           "name": "calculate_tax",
           "description": "Tính thuế thu nhập cá nhân",
           "inputSchema": {
             "type": "object",
             "properties": {
               "income": {"type": "number"}
             }
           }
         }
       ]
     },
     "id": 1
   }
   ```
3. **Client yêu cầu thực thi công cụ (Tool Call Request)**:
   ```json
   {
     "jsonrpc": "2.0",
     "method": "tools/call",
     "params": {
       "name": "calculate_tax",
       "arguments": {
         "income": 50000
       }
     },
     "id": 2
   }
   ```

---

## 3. Mini Project
Hãy viết một sơ đồ khối (Sử dụng sơ đồ ASCII hoặc công cụ thiết kế) mô tả chi tiết 5 bước truyền nhận tin nhắn giữa: Người dùng -> Claude Desktop (Client) -> MCP Server -> Dịch vụ database cục bộ -> Trả kết quả ngược lại.

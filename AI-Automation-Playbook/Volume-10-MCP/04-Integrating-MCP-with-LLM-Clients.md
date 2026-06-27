# Chương 04: Tích hợp Custom MCP Server vào Claude Desktop & Cursor

## 1. Deep Dive (Phân tích chuyên sâu)

### Kết nối MCP Server với LLM Clients
Sau khi đã lập trình xong MCP Server chạy qua luồng truyền tải STDIO ở Chương 3, làm thế nào để kích hoạt nó hoạt động thực tế trên các ứng dụng chat AI như Claude Desktop?

Chúng ta thực hiện bằng cách khai báo cấu hình trong file cài đặt của Client.
Khi Client khởi động:
1. Nó đọc file cấu hình.
2. Nó tự động chạy lệnh Terminal được chỉ định để khởi chạy MCP Server như một tiến trình con (Subprocess).
3. Client liên tục lắng nghe và sử dụng luồng Standard Input/Output của tiến trình con này để trao đổi tin nhắn JSON-RPC.

---

## 2. Demo: Cấu hình tích hợp chi tiết cho Claude Desktop

### Mục tiêu
Cấu hình thành công Claude Desktop để sử dụng máy chủ MCP đọc ghi logs đã lập trình ở Chương 3.

### Các bước thực hiện
1. Tìm đường dẫn file cấu hình của Claude Desktop trên hệ điều hành của bạn:
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%\\Claude\\claude_desktop_config.json`
2. Mở hoặc tạo mới file này bằng VS Code và chèn nội dung cấu hình sau:
   ```json
   {
     "mcpServers": {
       "system-logger": {
         "command": "/Users/dieptuhuy/Documents/AI Automation/AI-Automation-Playbook/.venv/bin/python3",
         "args": [
           "/Users/dieptuhuy/Documents/AI Automation/AI-Automation-Playbook/Volume-10-MCP/server.py"
         ]
       }
     }
   }
   ```
   *(Lưu ý: Thay đổi các đường dẫn tuyệt đối cho chính xác với máy tính của bạn. Luôn trỏ trực tiếp tới tệp python trong môi trường ảo `.venv`)*.
3. Khởi động lại (Restart) ứng dụng Claude Desktop hoàn toàn.
4. Kiểm tra góc phải khung chat, bạn sẽ thấy biểu tượng cổng cắm kết nối (Plug icon) hiển thị màu xanh lá cùng tên: `system-logger`.
5. Gõ lệnh chat trực tiếp thử nghiệm: *"Hãy đọc cho tôi 5 dòng log cuối cùng trong file app.log"*. AI sẽ tự động kích hoạt công cụ chạy cục bộ và trả kết quả chính xác lên màn hình chat.

---

## 3. Mini Project
Hãy thực hiện cấu hình tương tự máy chủ MCP của bạn vào Cursor IDE (Vào phần Settings -> Features -> MCP trong giao diện Cursor). Chụp ảnh màn hình giao diện Cursor đã kết nối thành công MCP Server và hiển thị danh sách các Tools khả dụng để lưu vào báo cáo.

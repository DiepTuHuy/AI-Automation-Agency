# Volume 10: Model Context Protocol (MCP) - Tiêu Chuẩn Kết Nối AI Với Thế Giới Vật Lý

Trước khi có MCP, mỗi ứng dụng AI, IDE (như Cursor, VS Code) hoặc AI Agent đều phải tự viết code kết nối với các công cụ riêng lẻ (như Database, Web Search, Terminal) theo các giao thức phân mảnh khác nhau. **Model Context Protocol (MCP)** là một tiêu chuẩn mở đột phá được khởi xướng bởi Anthropic, định nghĩa một giao thức giao tiếp chung giúp kết nối các mô hình LLM với dữ liệu và công cụ cục bộ một cách an toàn và nhất quán. Volume này hướng dẫn bạn hiểu sâu cấu trúc MCP, lập trình các máy chủ MCP tùy chỉnh (Custom MCP Servers) bằng Python và tích hợp chúng trực tiếp vào các Client như Claude Desktop và Cursor IDE.

---

## 1. Learning Objectives (Mục tiêu học tập)
Sau khi hoàn thành Volume này, bạn sẽ:
- **Hiểu rõ Giao thức MCP**: Giải thích được vai trò của Host, Client, và Server trong mô hình kết nối MCP.
- **Phân biệt lớp truyền tải (Transport Layers)**: Hiểu rõ sự khác biệt và cách dùng STDIO và SSE (Server-Sent Events) trong MCP.
- **Xây dựng Custom MCP Server**: Sử dụng Python SDK tự lập trình các máy chủ cung cấp tài nguyên (Resources) và công cụ (Tools) riêng.
- **Tích hợp IDE & Clients**: Cấu hình kết nối thành công MCP Server tự viết với Claude Desktop, Cursor và các IDE hỗ trợ AI.
- **Thiết kế Bảo mật MCP**: Triển khai các chính sách phân quyền và giới hạn thư mục truy cập an toàn cho Agent.

---

## 2. Prerequisites (Điều kiện tiên quyết)
- Hoàn thành Volume 04 (FastAPI) và Volume 09 (AI Agents).
- Hiểu rõ cơ chế Function Calling.

---

## 3. Big Picture (Bức tranh tổng thể)
MCP đóng vai trò như cổng USB chuẩn hóa: thay vì viết adapter riêng cho từng thiết bị, bạn chỉ cần cắm chuẩn MCP. Mọi LLM Client hỗ trợ MCP đều có thể gọi tất cả các công cụ của MCP Server ngay lập tức.

```
[Claude Desktop / Cursor IDE] (Client)
             │
             ▼ (Giao tiếp qua chuẩn JSON-RPC 2.0 - STDIO)
      [MCP Server API]
             ├── Tools (Thực thi lệnh: đọc file, chạy lệnh SQL)
             ├── Resources (Dữ liệu tĩnh: file cấu hình, logs)
             └── Prompts (Mẫu câu lệnh cấu hình sẵn)
```

---

## 4. First Principles (Nguyên lý gốc)
- **Chuẩn hóa Giao diện (Interface Standardization)**: Loại bỏ sự phân mảnh. MCP tách biệt vai trò của mô hình ngôn ngữ (chỉ cần biết cách dùng API MCP) và môi trường thực thi (chịu trách nhiệm chạy code thực tế).
- **JSON-RPC 2.0**: Mọi thông điệp giao tiếp giữa Client và Server trong MCP đều sử dụng định dạng tin nhắn JSON-RPC chuẩn hóa qua luồng dữ liệu chuẩn đầu vào/đầu ra (STDIO) hoặc giao thức web (SSE).
- **Quyền lực thuộc về Client**: MCP Server chỉ đề xuất các công cụ có sẵn. Việc quyết định có gọi công cụ đó hay không và khi nào gọi hoàn toàn do LLM Client kiểm soát.

---

## 5. Mental Models (Mô hình tư duy)
- **Cổng cắm USB vạn năng (The USB Hub)**: Trước khi có cổng USB, chuột máy tính có cổng cắm riêng, bàn phím cổng riêng, máy in cổng riêng. Khi chuẩn USB ra đời, máy tính chỉ cần trang bị cổng USB, mọi thiết bị ngoại vi đều sản xuất theo cổng USB và cắm chạy ngay lập tức. MCP chính là cổng USB dành cho AI. Client là máy tính, Server là chuột/bàn phím. Chỉ cần viết đúng chuẩn MCP, AI của bạn có thể sử dụng bất kỳ cơ sở dữ liệu hay thư mục đĩa cứng nào mà không cần viết lại driver.

---

## 6. Core Concepts (Khái niệm cốt lõi)
1. **Host**: Ứng dụng điều phối quy trình làm việc chung (như Cursor IDE, Claude Desktop).
2. **Client**: Thành phần nằm trong Host thiết lập kết nối kết nối trực tiếp với Server.
3. **Server**: Chương trình nhỏ gọn cục bộ hoặc trên internet trực tiếp cung cấp các tài nguyên (Resources) hoặc công cụ hành động (Tools).
4. **STDIO Transport**: Lớp truyền tải tin nhắn sử dụng luồng dữ liệu thô của hệ thống (Standard Input/Output) - nhanh và bảo mật tuyệt đối vì chỉ chạy cục bộ trên máy tính của bạn.

---

## 8. Best Practices (Quy chuẩn thực chiến)
- **Giới hạn quyền truy cập thư mục (Sandboxing)**: Khi viết MCP Server đọc file, luôn kiểm tra đường dẫn file (Path validation) để đảm bảo Agent không thể đọc trộm các file nhạy cảm hệ thống ngoài thư mục dự án được cấp phép.
- **Log lỗi ra STDERR**: Vì luồng STDOUT được dành riêng để truyền tin nhắn giao thức JSON-RPC, mọi lệnh `print()` debug thông thường của bạn phải được chuyển hướng ghi ra STDERR (`sys.stderr.write`), nếu không sẽ làm hỏng parser của Client và gãy kết nối.
- **Tận dụng Prompts**: Cung cấp các mẫu prompt cấu hình sẵn trong MCP Server để định hướng nhanh cho LLM cách tương tác tốt nhất với tài nguyên bạn cung cấp.

---

## 9. Common Mistakes (Sai lầm thường gặp)
- **Sử dụng lệnh `print()` thông thường trong code MCP Server**: Làm đảo lộn luồng STDOUT khiến client báo lỗi *"Invalid JSON-RPC message"*. *Cách sửa*: Sử dụng thư viện `logging` được cấu hình ghi ra file hoặc STDERR.
- **Đường dẫn Python không hợp lệ trong file cấu hình**: Khi chỉ định lệnh khởi chạy trong `claude_desktop_config.json`, sử dụng lệnh `python` chung chung có thể trỏ sai môi trường ảo `.venv`. *Cách sửa*: Sử dụng đường dẫn tuyệt đối dẫn trực tiếp tới file thực thi python của môi trường ảo (ví dụ: `/Users/username/project/.venv/bin/python3`).

---

## 10. Engineering Mindset (Tư duy kỹ sư)
Một kỹ sư AI thực chiến coi MCP là công cụ cốt lõi để xây dựng hệ điều hành riêng cho Agent. Thay vì viết hàng trăm API Endpoint bảo mật phức tạp, họ đóng gói các công cụ nội bộ thành các MCP server cục bộ giúp việc tương tác đĩa cứng, quản lý file, và tương tác DB của Agent diễn ra trực tiếp và an toàn nhất.

---

## 13. Capstone Project (Dự án kết khóa Volume)
Xem mô tả chi tiết tại [Project-04](file:///Users/dieptuhuy/Documents/AI%20Automation/AI-Automation-Playbook/Projects/Project-04-AI-Customer-Support-Agent-MCP/README.md).

---

## 14. Review Questions (Bloom Taxonomy - 30 câu hỏi)
### Level 1 — Remember (Nhớ)
1. MCP là viết tắt của từ gì?
2. Tổ chức nào khởi xướng tiêu chuẩn MCP và vào năm nào?
3. Nêu 3 thành phần cốt lõi của giao thức MCP.
4. Giao thức tin nhắn nào được sử dụng trong giao tiếp MCP?
5. Luồng dữ liệu hệ thống nào được dùng làm kênh truyền mặc định của lớp STDIO Transport?

### Level 2 — Understand (Hiểu)
6. Giải thích sự khác biệt giữa Resources và Tools trong định nghĩa của một MCP Server.
7. Tại sao STDIO lại là phương thức truyền tải (Transport) được ưa chuộng hơn SSE đối với các MCP Server chạy cục bộ?
8. Tại sao việc sử dụng lệnh `print()` thông thường trong code MCP Server lại gây hỏng kết nối hệ thống?
9. Cơ chế hoạt động của JSON-RPC 2.0 trong việc xác định cặp tin nhắn Request và Response giữa Client và Server.
10. Claude Desktop đọc file cấu hình nào để thiết lập kết nối tới các MCP Server?

### Level 3 — Apply (Áp dụng)
11. Viết cấu trúc file cấu hình JSON để Claude Desktop gọi một MCP Server chạy bằng lệnh node/python.
12. Sử dụng Python SDK của MCP định nghĩa một schema tài nguyên (Resource) đơn giản trích xuất danh sách file log.
13. Chuyển hướng một thông báo lỗi gõ ra màn hình console sang luồng STDERR bằng Python.
14. Khai báo một công cụ (Tool) MCP nhận đầu vào là tên thư mục và trả về danh sách dung lượng của các file bên trong.
15. Cài đặt thư viện MCP SDK bằng PIP trong môi trường ảo của bạn.

### Level 4 — Analyze (Phân tích)
16. Phân tích sự khác biệt về kiến trúc bảo mật giữa việc cho phép LLM gọi API web thông thường và gọi công cụ qua MCP Server cục bộ.
17. So sánh ưu thế của MCP so với các giải pháp tích hợp công cụ tùy chỉnh của riêng từng IDE (như các extensions của VS Code).
18. Phân tích nguyên nhân tại sao Client báo lỗi "Connection closed" ngay khi vừa khởi động MCP Server và cách kiểm tra file log của Client để truy vết.
19. Đánh giá tính khả thi khi xây dựng một MCP Server đóng vai trò là Gateway trung gian kết nối với hàng trăm database SQL nội bộ doanh nghiệp.
20. Tại sao việc kiểm tra bảo mật đường dẫn (Path Traversal validation) lại cực kỳ quan trọng đối với các công cụ MCP cho phép đọc file đĩa cứng?

### Level 5 — Design (Thiết kế)
21. Thiết kế một Custom MCP Server bằng Python hỗ trợ 3 công cụ: đọc dữ liệu từ bảng SQL, ghi dữ liệu vào bảng SQL, và thực thi câu lệnh truy vấn báo cáo.
22. Đề xuất kiến trúc hệ thống MCP Server chạy qua môi trường Web (SSE Transport) hỗ trợ phân quyền người dùng bằng token JWT.
23. Thiết kế giải pháp phân tách môi trường chạy (Sandboxing) an toàn cho MCP Server sử dụng Docker Container để chạy các đoạn code python do Agent tự viết.
24. Đề xuất quy trình đồng bộ cấu hình MCP Server tự động cho toàn bộ đội ngũ lập trình viên trong công ty.
25. Thiết kế công cụ MCP tích hợp với Git giúp Agent tự động tạo nhánh, commit code và đẩy lên GitHub.

### Level 6 — Evaluate (Đánh giá)
26. Đánh giá tiềm năng phát triển của tiêu chuẩn MCP đối với tương lai của ngành lập trình phần mềm hỗ trợ bởi AI.
27. Đánh giá sự đánh đổi giữa việc tự lập trình MCP Server riêng và sử dụng các MCP Server mã nguồn mở có sẵn trên kho cộng đồng (như mcp-get).
28. Kiểm chứng độ ổn định và độ trễ của việc truyền tải dữ liệu dung lượng lớn (như file ảnh 10MB) qua giao thức STDIO JSON-RPC.
29. Đánh giá khả năng tương thích của Cursor IDE đối với các chuẩn định nghĩa Tool Schema mới nhất của MCP.
30. Lập luận bảo vệ hoặc bác bỏ luận điểm: *"MCP chỉ là công cụ quảng cáo của Anthropic và sẽ sớm bị thay thế bởi các tiêu chuẩn của OpenAI hoặc Microsoft"*.

---

## 15. Checklist hoàn thành
- [ ] Hiểu rõ mô hình hoạt động của Model Context Protocol.
- [ ] Viết được Custom MCP Server cơ bản bằng Python chạy qua STDIO.
- [ ] Chuyển hướng thành công log debug sang STDERR hoặc ghi file log riêng.
- [ ] Cấu hình tích hợp thành công MCP Server tự viết vào Claude Desktop hoặc Cursor.
- [ ] Hoàn thành Capstone Project (Project 04).

---

## 16. Resources (Tài liệu tham khảo)
- **Trang chủ chính thức**: [Model Context Protocol (Anthropic)](https://modelcontextprotocol.io/)
- **Mã nguồn SDK**: [MCP Python SDK GitHub Repository](https://github.com/modelcontextprotocol/python-sdk)
- **Kho máy chủ**: [Awesome MCP Servers (Danh sách máy chủ cộng đồng)](https://github.com/punkpeye/awesome-mcp-servers)

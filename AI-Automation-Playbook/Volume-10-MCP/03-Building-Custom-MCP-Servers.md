# Chương 03: Tự lập trình Máy chủ MCP bằng Python SDK

## 1. Deep Dive (Phân tích chuyên sâu)

### Xây dựng MCP Server bằng Python SDK
Anthropic cung cấp gói thư viện chính thức `mcp` giúp việc dựng máy chủ trở nên vô cùng đơn giản thông qua kỹ thuật lập trình trang trí (Decorators) tương tự như FastAPI.

Hai decorator cốt lõi bạn sẽ dùng:
1. **`@mcp.resource()`**: Dùng để cung cấp dữ liệu tĩnh (ví dụ: file log, quy chế tài liệu nội bộ). LLM chỉ có thể đọc, không thể thay đổi dữ liệu này.
2. **`@mcp.tool()`**: Dùng để cung cấp công cụ hành động (như tạo file mới, gọi API bên thứ ba, chạy truy vấn SQL). Đây là các hàm có khả năng tương tác làm thay đổi trạng thái của máy tính.

---

## 2. Demo: Máy chủ MCP đọc File Logs hệ thống an toàn

### Mục tiêu
Xây dựng một MCP Server hoàn chỉnh bằng Python, cung cấp công cụ đọc các dòng log cuối cùng của hệ thống, hỗ trợ giới hạn quyền đọc chỉ trong thư mục quy định để bảo mật.

### Mã nguồn máy chủ (`server.py`)
```python
import os
import sys
from pathlib import Path
from mcp.server.fastmcp import FastMCP

# 1. Khởi tạo FastMCP Server
mcp = FastMCP("System Logger Service")

# Thư mục an toàn được cấp phép đọc file
SAFE_LOG_DIR = Path("./logs").resolve()
SAFE_LOG_DIR.mkdir(exist_ok=True)

# Tạo file log mẫu để test
(SAFE_LOG_DIR / "app.log").write_text("2026-06-28 00:00:01 - INFO - Server started successfully.\n2026-06-28 00:05:22 - ERROR - Database connection timeout.")

# 2. Định nghĩa Tool MCP cung cấp cho AI
@mcp.tool()
def read_system_logs(filename: str, num_lines: int = 10) -> str:
    """Đọc các dòng log cuối cùng của một tệp tin log cụ thể trong thư mục an toàn."""
    # Ngăn chặn tấn công Path Traversal (đọc trộm file ngoài thư mục)
    target_path = (SAFE_LOG_DIR / filename).resolve()
    
    if not target_path.is_relative_to(SAFE_LOG_DIR):
        return f"Lỗi bảo mật: Không được phép truy cập ngoài thư mục {SAFE_LOG_DIR.name}!"
        
    if not target_path.exists():
        return f"Lỗi: File log '{filename}' không tồn tại."
        
    try:
        with open(target_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            return "".join(lines[-num_lines:])
    except Exception as e:
        return f"Lỗi khi đọc file: {str(e)}"

if __name__ == "__main__":
    # Chạy MCP server qua lớp truyền tải STDIO
    # FastMCP tự động quản lý luồng đầu vào/ra JSON-RPC
    mcp.run()
```

---

## 3. Mini Project

### Bài tập 1: Xây dựng Custom MCP Server tính toán tài chính (Mức độ: Trung bình)
* **Đề bài**: Viết một MCP Server bằng Python sử dụng thư viện `mcp` SDK để cung cấp một công cụ tính thuế thu nhập cá nhân đơn giản.
* **Mã nguồn mẫu (`custom_finance_mcp.py`)**:
```python
from mcp.server.fastmcp import FastMCP

# Khởi tạo FastMCP Server
mcp = FastMCP("FinanceAssistant")

# Định nghĩa Tool tính thuế
@mcp.tool()
def calculate_income_tax(income_usd: float) -> str:
    """Tính toán thuế thu nhập cá nhân ước tính (10% cho thu nhập dưới 50k, 20% cho trên 50k)."""
    if income_usd < 50000:
        tax = income_usd * 0.1
    else:
        tax = (50000 * 0.1) + ((income_usd - 50000) * 0.2)
    return f"Thuế thu nhập cá nhân ước tính cho mức ${income_usd:,.2f} là: ${tax:,.2f}"

if __name__ == "__main__":
    mcp.run()
```

### Bài tập 2: Custom MCP Server truy vấn dữ liệu từ SQLite (Mức độ: Khó)
* **Đề bài**: Viết một Custom MCP Server bằng Python kết nối với cơ sở dữ liệu SQLite của công ty. Server cung cấp một công cụ `search_inventory` cho phép mô hình ngôn ngữ lớn có thể truy vấn số lượng tồn kho của sản phẩm bằng cách truyền tên sản phẩm.
* **Yêu cầu**: Học viên tự hoàn thành không có code mẫu.
* **Gợi ý triển khai (Workflow Hints)**:
  1. Import thư viện `sqlite3` trong file custom MCP server.
  2. Viết hàm Python kết nối tới file `.db` và thực hiện câu lệnh `SELECT` để tìm sản phẩm.
  3. Đăng ký hàm đó bằng decorator `@mcp.tool()` để AI Client có thể gọi trực tiếp.


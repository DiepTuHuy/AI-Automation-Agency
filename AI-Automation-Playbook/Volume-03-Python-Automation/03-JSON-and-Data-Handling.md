# Chương 03: Xử lý dữ liệu định dạng JSON trong Python

## 1. Deep Dive (Phân tích chuyên sâu)

### JSON (JavaScript Object Notation) là gì?
JSON là tiêu chuẩn trao đổi dữ liệu phổ biến nhất trên web và trong các hệ thống AI. Nó biểu diễn dữ liệu dưới dạng cặp `key-value` tương tự như kiểu dữ liệu Dictionary của Python.

### Xử lý JSON trong Python
Python cung cấp thư viện built-in `json` vô cùng mạnh mẽ:
- **`json.loads()`** (Load String): Chuyển đổi một chuỗi văn bản định dạng JSON thành một Dictionary trong Python để dễ dàng truy cập phần tử.
- **`json.dumps()`** (Dump String): Chuyển đổi một Dictionary Python thành chuỗi JSON để truyền qua mạng Internet hoặc ghi vào file.
- **`json.load()`** và **`json.dump()`**: Thực hiện các thao tác đọc và ghi trực tiếp từ/vào tệp tin cứng.

---

## 2. Demo: Quản lý file cấu hình API key tự động

### Mục tiêu
Xây dựng một hệ thống đọc, sửa đổi và lưu trữ tệp cấu hình JSON (`config.json`) dùng để quản lý trạng thái của các API trong ứng dụng tự động hóa.

### Mã nguồn (`config_manager.py`)
```python
import json
from pathlib import Path

class ConfigManager:
    def __init__(self, config_file: str = "config.json"):
        self.config_path = Path(config_file)
        self.config_data = {}
        self.load_config()

    def load_config(self):
        # Nếu file chưa tồn tại, khởi tạo cấu hình mặc định
        if not self.config_path.exists():
            self.config_data = {
                "system_status": "active",
                "api_retries": 3,
                "enabled_models": ["gpt-4o-mini", "claude-3-haiku"]
            }
            self.save_config()
        else:
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    self.config_data = json.load(f)
            except json.JSONDecodeError:
                print("Lỗi định dạng file JSON! Khởi tạo cấu hình mặc định.")
                self.config_data = {}

    def save_config(self):
        with open(self.config_path, "w", encoding="utf-8") as f:
            # indent=4 giúp định dạng file JSON đẹp, dễ đọc bằng mắt
            json.dump(self.config_data, f, indent=4, ensure_ascii=False)

    def update_key(self, key: str, value):
        self.config_data[key] = value
        self.save_config()
        print(f"Đã cập nhật {key} -> {value}")

if __name__ == "__main__":
    manager = ConfigManager()
    print("Cấu hình hiện tại:", manager.config_data)
    
    # Cập nhật số lần thử lại API
    manager.update_key("api_retries", 5)
    manager.update_key("system_status", "maintenance")
```

---

## 3. Mini Project
Hãy viết một script Python đọc một file JSON chứa thông tin lịch sử giao dịch khách hàng (bao gồm ID khách hàng, Danh sách mặt hàng, Tổng tiền). Hãy tính tổng chi tiêu của từng khách hàng, lọc ra các khách hàng Vip chi tiêu trên 10 triệu đồng, và xuất kết quả ra một file JSON mới mang tên `vip_customers.json`.

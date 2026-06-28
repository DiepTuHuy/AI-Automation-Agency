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

### Bài tập 1: Đọc và tính toán báo cáo doanh thu từ JSON (Mức độ: Trung bình)
* **Đề bài**: Viết một script Python đọc một file JSON chứa danh sách các giao dịch bán hàng, tính tổng doanh thu và in danh sách các sản phẩm bán chạy nhất.
* **Mã nguồn mẫu (`sales_report.py`)**:
```python
import json

json_data = '''
[
    {"transaction_id": "T01", "product": "Bàn phím cơ", "price": 80.0, "quantity": 3},
    {"transaction_id": "T02", "product": "Chuột không dây", "price": 45.0, "quantity": 5},
    {"transaction_id": "T03", "product": "Bàn phím cơ", "price": 80.0, "quantity": 1},
    {"transaction_id": "T04", "product": "Tai nghe", "price": 120.0, "quantity": 2}
]
'''

def generate_report(data_str: str):
    transactions = json.loads(data_str)
    total_revenue = 0
    product_sales = {}
    
    for t in transactions:
        revenue = t["price"] * t["quantity"]
        total_revenue += revenue
        
        prod = t["product"]
        product_sales[prod] = product_sales.get(prod, 0) + t["quantity"]
        
    print(f"Tổng doanh thu: ${total_revenue:.2f}")
    print("Số lượng bán ra của từng sản phẩm:")
    for prod, qty in product_sales.items():
        print(f"- {prod}: {qty} chiếc")

if __name__ == "__main__":
    generate_report(json_data)
```

### Bài tập 2: Cập nhật tồn kho tự động trong file JSON lớn (Mức độ: Khó)
* **Đề bài**: Viết một script đọc tệp cấu hình tồn kho dạng JSON. Nếu số lượng một mặt hàng giảm xuống dưới 10, tự động cập nhật trạng thái `restock_needed: true` và ghi đè dữ liệu mới cập nhật lại vào tệp JSON ban đầu.
* **Yêu cầu**: Học viên tự hoàn thành không có code mẫu.
* **Gợi ý triển khai (Workflow Hints)**:
  1. Sử dụng `json.load()` để đọc tệp từ đĩa cứng.
  2. Duyệt qua mảng sản phẩm bằng vòng lặp và cập nhật điều kiện.
  3. Ghi lại dữ liệu bằng `json.dump(data, f, indent=4)` để lưu đè thay đổi.


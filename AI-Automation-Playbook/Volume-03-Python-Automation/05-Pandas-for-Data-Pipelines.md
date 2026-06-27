# Chương 05: Xử lý dữ liệu bảng bằng `pandas`

## 1. Deep Dive (Phân tích chuyên sâu)

### Pandas là gì và Tại sao AI Engineer cần nó?
Trong các dự án tự động hóa doanh nghiệp, dữ liệu thường được lưu trữ dưới dạng bảng biểu Excel hoặc CSV (ví dụ: danh sách khách hàng tiềm năng, lịch sử giao dịch, phản hồi khảo sát). 

**Pandas** là thư viện xử lý dữ liệu dạng bảng hàng đầu trong Python. Nó cho phép bạn:
- Đọc và ghi hàng triệu dòng dữ liệu từ CSV, Excel, SQL chỉ với 1 dòng code.
- Làm sạch dữ liệu nhanh chóng (xử lý dữ liệu trống, chuẩn hóa định dạng chữ).
- Lọc (filter) và nhóm (group-by) dữ liệu theo các điều kiện nghiệp vụ một cách hiệu quả.

---

## 2. Demo: Làm sạch dữ liệu Leads trước khi đưa vào AI

### Mục tiêu
Đọc một file CSV chứa danh sách đăng ký tư vấn khách hàng, tiến hành lọc bỏ các dòng bị trống số điện thoại hoặc email không đúng định dạng, chuẩn hóa lại cột tên, và xuất ra file CSV sạch.

### Mã nguồn (`pandas_cleaning.py`)
Cài đặt thư viện: `pip install pandas openpyxl`

```python
import pandas as pd

def clean_leads_data(input_file: str, output_file: str):
    # Đọc file CSV
    df = pd.read_csv(input_file)
    print("Dữ liệu thô ban đầu:")
    print(df)
    
    # 1. Loại bỏ các dòng bị trống hoàn toàn Số điện thoại (NaN)
    df = df.dropna(subset=["Phone"])
    
    # 2. Chuẩn hóa tên: Viết hoa chữ cái đầu của mỗi từ
    df["Name"] = df["Name"].str.strip().str.title()
    
    # 3. Lọc chỉ lấy các khách hàng đăng ký từ nguồn 'Facebook' hoặc 'Google'
    df = df[df["Source"].isin(["Facebook", "Google"])]
    
    # 4. Lưu dữ liệu sạch ra file CSV mới
    df.to_csv(output_file, index=False)
    print("\nDữ liệu sau khi làm sạch:")
    print(df)

if __name__ == "__main__":
    # Giả lập tạo file CSV dữ liệu thô ban đầu
    raw_data = {
        "Name": [" nguyen van a ", "Tran Thi B", "Le Van C", "Hoang Lan"],
        "Phone": ["0987654321", None, "0912345678", "0909090909"],
        "Source": ["Facebook", "Google", "TikTok", "Facebook"]
    }
    
    temp_raw_path = "raw_leads.csv"
    temp_clean_path = "clean_leads.csv"
    
    pd.DataFrame(raw_data).to_csv(temp_raw_path, index=False)
    
    clean_leads_data(temp_raw_path, temp_clean_path)
```

---

## 3. Mini Project
Hãy viết một script đọc một file CSV chứa thông tin chi tiêu quảng cáo (bao gồm cột: Tháng, Kênh quảng cáo, Chi phí, Doanh thu mang lại). Sử dụng Pandas để tính chỉ số ROI (Doanh thu / Chi phí) của từng kênh, sắp xếp các kênh có ROI từ cao xuống thấp và ghi kết quả vào một file Excel mới.

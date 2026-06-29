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

### Bài tập 1: Chuẩn hóa dữ liệu khách hàng bằng Pandas (Mức độ: Trung bình)
* **Đề bài**: Viết một script Python sử dụng `pandas` để làm sạch dữ liệu khách hàng: loại bỏ các dòng bị trùng lặp, điền dữ liệu mặc định cho các ô trống và chuẩn hóa định dạng chữ hoa đầu từ cho cột tên.
* **Mã nguồn mẫu (`pandas_pipeline.py`)**:
```python
import pandas as pd

raw_data = {
    "Name": ["nguyen van a", "Nguyen Van A", "Tran thi B", "Le van C"],
    "Email": ["a@example.com", "a@example.com", "b@example.com", None],
    "Age": [25, 25, 30, 22]
}

def clean_data():
    df = pd.DataFrame(raw_data)
    print("Dữ liệu thô ban đầu:")
    print(df, "
")
    
    # 1. Chuẩn hóa tên thành viết hoa chữ cái đầu
    df["Name"] = df["Name"].str.title()
    
    # 2. Loại bỏ bản ghi trùng lặp
    df = df.drop_duplicates()
    
    # 3. Điền giá trị mặc định cho ô trống (Email)
    df["Email"] = df["Email"].fillna("no_email@example.com")
    
    print("Dữ liệu sau khi làm sạch:")
    print(df)

if __name__ == "__main__":
    clean_data()
```

### Bài tập 2: Phân tích doanh thu và xuất báo cáo Excel (Mức độ: Khó)
* **Đề bài**: Đọc một file dữ liệu CSV chứa lịch sử mua hàng của doanh nghiệp (Tải tệp tin mẫu [transactions.csv](../../resources/transactions.csv) về máy). Sử dụng Pandas để gom nhóm (`groupby`) theo tên khách hàng (`client_name`), tính tổng chi tiêu của từng khách hàng và lưu kết quả báo cáo sạch sẽ sang một file Excel (`report.xlsx`).
* **Yêu cầu**: Học viên tự hoàn thành không có code mẫu.
* **Gợi ý triển khai (Workflow Hints)**:
  1. Sử dụng `pd.read_csv()` để nạp tệp dữ liệu [transactions.csv](../../resources/transactions.csv).
  2. Sử dụng `df.groupby("client_name")["amount_usd"].sum()` để tổng hợp dữ liệu.
  3. Ghi dữ liệu ra file Excel bằng hàm `to_excel()`.

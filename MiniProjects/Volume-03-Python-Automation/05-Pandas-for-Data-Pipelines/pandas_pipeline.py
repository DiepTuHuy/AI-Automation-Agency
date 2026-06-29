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
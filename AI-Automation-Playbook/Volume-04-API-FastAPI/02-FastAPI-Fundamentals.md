# Chương 02: Khởi tạo ứng dụng FastAPI & Cấu hình Uvicorn

## 1. Deep Dive (Phân tích chuyên sâu)

### Tại sao FastAPI trở thành chuẩn công nghiệp?
Trước đây, Flask và Django là hai framework Python thống trị. Tuy nhiên, FastAPI ra đời và nhanh chóng chiếm lĩnh nhờ:
1. **Hiệu năng vượt trội**: Xây dựng trên Starlette và Uvicorn, FastAPI cho tốc độ xử lý tương đương Go và NodeJS (nhờ kiến trúc async bất đồng bộ).
2. **Tự động sinh tài liệu**: Khai báo code bằng Type Hints giúp FastAPI tự động tạo ra trang tài liệu tương tác tuyệt đẹp (Swagger UI tại `/docs` và ReDoc tại `/redoc`) mà không cần viết thêm cấu hình.
3. **Xác thực dữ liệu tức thì**: Tích hợp sâu với Pydantic giúp tự động parse và validate request payload đầu vào.

---

## 2. Demo: Xây dựng ứng dụng FastAPI "Hello World" đầu tiên

### Mục tiêu
Khởi tạo một dự án FastAPI cơ bản, chạy bằng máy chủ ASGI Uvicorn và truy cập trang tài liệu Swagger để test thử API trực quan.

### Source Tree
```
fastapi-basics/
├── requirements.txt
└── main.py
```

### Mã nguồn (`main.py`)
Trước khi chạy, cài đặt: `pip install fastapi uvicorn`

```python
from fastapi import FastAPI

# Khởi tạo instance ứng dụng FastAPI chính
app = FastAPI(
    title="Hệ thống AI Automation API",
    description="Cung cấp các cổng kết nối dịch vụ tự động hóa quy trình nghiệp vụ.",
    version="1.0.0"
)

# Định nghĩa route GET cơ bản
@app.get("/", tags=["Hệ thống"])
async def root():
    return {
        "status": "online",
        "message": "Chào mừng bạn đến với AI Automation Gateway API!"
    }

# Định nghĩa route GET có nhận tham số Query Parameter
@app.get("/api/v1/greet", tags=["Tiện ích"])
async def greet_user(name: str = "Khách"):
    return {
        "greeting": f"Xin chào {name}! Chúc bạn một ngày làm việc hiệu quả."
    }

if __name__ == "__main__":
    import uvicorn
    # Chạy uvicorn server: main đại diện cho file main.py, app đại diện cho instance app
    # reload=True tự động khởi động lại server khi bạn thay đổi code (môi trường Dev)
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
```

---

## 3. Mini Project

### Bài tập 1: Xây dựng REST API tính toán chỉ số sức khỏe bằng FastAPI (Mức độ: Trung bình)
* **Đề bài**: Viết một ứng dụng FastAPI cung cấp một endpoint nhận chiều cao và cân nặng thông qua query parameters, sau đó tính toán chỉ số khối cơ thể (BMI) và trả về kết quả kèm phân loại sức khỏe dạng JSON.
* **Mã nguồn mẫu (`bmi_api.py`)**:
```python
from fastapi import FastAPI

app = FastAPI(title="Health Calculator API")

@app.get("/api/v1/bmi")
def calculate_bmi(weight_kg: float, height_m: float):
    if height_m <= 0:
        return {"error": "Chiều cao phải lớn hơn 0"}
    
    bmi = weight_kg / (height_m ** 2)
    category = ""
    if bmi < 18.5:
        category = "Gầy"
    elif bmi < 24.9:
        category = "Bình thường"
    else:
        category = "Thừa cân"
        
    return {
        "weight": weight_kg,
        "height": height_m,
        "bmi": round(bmi, 2),
        "category": category
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
```

### Bài tập 2: API Quản lý danh sách lời khuyên sức khỏe hàng ngày (Mức độ: Khó)
* **Đề bài**: Xây dựng một ứng dụng FastAPI quản lý danh sách lời khuyên sức khỏe (Tips) trong bộ nhớ (Memory List). API cần hỗ trợ: Lấy ngẫu nhiên 1 lời khuyên (`GET`), và Thêm một lời khuyên mới vào danh sách (`POST`).
* **Yêu cầu**: Học viên tự hoàn thành không có code mẫu.
* **Gợi ý triển khai (Workflow Hints)**:
  1. Khai báo danh sách danh ngôn sức khỏe mẫu làm cơ sở dữ liệu trong bộ nhớ.
  2. Sử dụng thư viện `random` để lấy phần tử ngẫu nhiên khi người dùng gửi request `GET`.
  3. Sử dụng mô hình Pydantic đơn giản để nhận dữ liệu đầu vào cho yêu cầu `POST`.


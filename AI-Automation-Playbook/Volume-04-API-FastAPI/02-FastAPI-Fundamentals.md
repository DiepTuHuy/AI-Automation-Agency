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
Hãy bổ sung thêm một route POST `/api/v1/echo` vào ứng dụng trên. Route này nhận vào một payload JSON tự do và trả lại chính xác những gì người dùng gửi lên kèm theo thông tin thời gian hiện tại trên server. Kiểm thử endpoint này bằng giao diện Swagger UI `/docs`.

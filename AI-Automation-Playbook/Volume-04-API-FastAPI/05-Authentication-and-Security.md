# Chương 05: Bảo mật API bằng Header API Key & Cấu hình CORS

## 1. Deep Dive (Phân tích chuyên sâu)

### Tại sao cần bảo mật API?
Khi API của bạn được deploy lên Internet, bất kỳ ai biết URL endpoint cũng có thể gọi và làm cạn kiệt tài khoản OpenAI của bạn. Do đó, bạn cần thiết lập cơ chế xác thực bảo mật.

### Các phương thức bảo mật thông dụng
1. **API Key qua Header**: Client phải gửi kèm một chuỗi ký tự bí mật trong HTTP Header (ví dụ: `X-API-Key: my_super_secret_key`). Đây là giải pháp đơn giản và hiệu quả nhất cho kết nối giữa các hệ thống tự động (Server-to-Server) như n8n gọi FastAPI.
2. **OAuth2 & JWT Tokens**: Phức tạp hơn, dùng cho hệ thống người dùng đăng nhập trực tiếp (Client-to-Server).

### CORS (Cross-Origin Resource Sharing)
Mặc định, trình duyệt web chặn các đoạn script ở trang web A gọi tới API ở trang web B. Để cho phép ứng dụng frontend (ví dụ React chạy trên localhost) gọi được tới FastAPI của bạn, bạn phải cấu hình CORS Middleware để khai báo danh sách tên miền được phép truy cập.

---

## 2. Demo: API bảo mật bằng X-API-Key & Cấu hình CORS đầy đủ

### Mục tiêu
Xây dựng ứng dụng FastAPI cấu hình CORS cho phép ứng dụng frontend truy cập, đồng thời khóa tất cả các endpoint bằng cơ chế xác thực Header API Key.

### Mã nguồn (`secure_api.py`)
```python
import os
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

# Lấy mã API Key bí mật của hệ thống từ file .env
SYSTEM_API_KEY = os.getenv("SYSTEM_API_KEY", "default_secret_key")

app = FastAPI()

# Cấu hình CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://myportfolio.com"], # Chỉ cho phép các domain này gọi API
    allow_credentials=True,
    allow_methods=["*"], # Cho phép tất cả các method (GET, POST...)
    allow_headers=["*"], # Cho phép tất cả các HTTP Headers
)

# Khởi tạo đối tượng security để đọc API Key từ header có tên X-API-Key
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

# Hàm Dependency dùng để kiểm tra bảo mật
async def verify_api_key(api_key: str = Depends(api_key_header)):
    if not api_key or api_key != SYSTEM_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key không hợp lệ hoặc bị thiếu!"
        )
    return api_key

# Endpoint công cộng (Public)
@app.get("/api/v1/public")
async def public_endpoint():
    return {"message": "Đây là thông tin công cộng công khai."}

# Endpoint bảo mật (Private - Được bảo vệ bởi verify_api_key)
@app.get("/api/v1/private", dependencies=[Depends(verify_api_key)])
async def private_endpoint():
    return {
        "status": "authorized",
        "secret_data": "Hóa đơn tháng này của đối tác đã được duyệt chi 100 triệu VNĐ."
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("secure_api:app", host="127.0.0.1", port=8000, reload=True)
```

---

## 3. Mini Project
Hãy viết một script Python mô phỏng một API client gửi request gọi endpoint `/api/v1/private` phía trên.
1. Thử gửi request không kèm header -> Kiểm tra xem có nhận được lỗi 401 không.
2. Gửi request kèm header sai key -> Kiểm tra mã lỗi.
3. Gửi request kèm header đúng key -> In ra thông tin bí mật nhận được.

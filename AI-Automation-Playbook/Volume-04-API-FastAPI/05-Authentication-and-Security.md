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

### Bài tập 1: Bảo mật API bằng API Key đơn giản (Mức độ: Trung bình)
* **Đề bài**: Viết một ứng dụng FastAPI có một endpoint nhạy cảm chứa dữ liệu doanh thu. Hãy viết mã bảo mật endpoint này bằng cơ chế xác thực API Key thông qua HTTP Header.
* **Mã nguồn mẫu (`api_key_auth.py`)**:
```python
from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader

app = FastAPI()

API_KEY = "super_secret_key_123"
API_KEY_NAME = "X-API-KEY"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

def validate_api_key(key: str = Depends(api_key_header)):
    if key != API_KEY:
        raise HTTPException(
            status_code=403,
            detail="Quyền truy cập bị từ chối. API Key không hợp lệ."
        )
    return key

@app.get("/api/v1/revenue")
def get_revenue(api_key: str = Depends(validate_api_key)):
    # Chỉ những request có đúng header X-API-KEY mới vào được đây
    return {
        "month": "July 2026",
        "revenue_usd": 150000.0,
        "status": "Success"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
```

### Bài tập 2: Xác thực phân quyền Người dùng với JWT Token (Mức độ: Khó)
* **Đề bài**: Xây dựng hệ thống đăng nhập trả về JSON Web Token (JWT) trong FastAPI. Tạo hai endpoint: `/api/v1/profile` (yêu cầu token hợp lệ của mọi user) và `/api/v1/admin/settings` (chỉ chấp nhận token của những người dùng có trường vai trò `role` là `admin`).
* **Yêu cầu**: Bạn hãy tự hoàn thành không có code mẫu.
* **Gợi ý triển khai (Workflow Hints)**:
  1. Sử dụng thư viện `PyJWT` (hoặc `jose`) để mã hóa và giải mã token.
  2. Tạo hàm dependency giải mã token, trích xuất thông tin người dùng và vai trò.
  3. Báo lỗi `401 Unauthorized` nếu token hết hạn, và `403 Forbidden` nếu người dùng không phải admin.

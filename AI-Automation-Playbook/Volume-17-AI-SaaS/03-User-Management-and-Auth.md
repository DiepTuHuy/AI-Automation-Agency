# Chương 03: Xác thực người dùng bằng JWT Token & Mã hóa Bcrypt

## 1. Deep Dive (Phân tích chuyên sâu)

### Đăng ký, Đăng nhập & Xác thực trong Web API
Mọi ứng dụng SaaS đều phải bảo vệ các tính năng trả phí của mình bằng lớp **Authentication (Xác thực)**.
1. **Đăng ký (Register)**:
   - Người dùng gửi email và mật khẩu thô.
   - Server băm mật khẩu thô bằng thư viện `bcrypt` (ví dụ: chuỗi `"123456"` biến thành `"2y$12$K8y..."` không thể giải mã ngược).
   - Lưu email và chuỗi mật khẩu đã băm vào database.
2. **Đăng nhập (Login)**:
   - Người dùng gửi email và mật khẩu thô.
   - Server lấy mật khẩu đã băm tương ứng của email đó từ DB lên và sử dụng hàm `bcrypt.checkpw()` để so sánh đối chiếu.
   - Nếu khớp, server sinh ra một chuỗi **JWT Token** (chứa ID người dùng đã được ký số bằng mã khóa bí mật của server) và trả về cho trình duyệt.
3. **Gọi API được bảo vệ (Protected Routes)**:
   - Client gửi kèm JWT Token này trong HTTP Header `Authorization: Bearer token_here` của mỗi request tiếp theo.
   - FastAPI đọc và giải mã token để xác định danh tính người dùng đang gọi mà không bắt họ phải đăng nhập lại.

---

## 2. Demo: Lập trình hệ thống Auth hoàn chỉnh trong FastAPI

### Mục tiêu
Xây dựng đầy đủ các endpoint: đăng ký người dùng mới, đăng nhập trả về JWT và bảo mật một route thông tin VIP bằng FastAPI.

### Mã nguồn (`auth_app.py`)
Yêu cầu cài đặt: `pip install passlib[bcrypt] pyjwt fastapi uvicorn`

```python
import jwt
import datetime
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext

# Cấu hình băm mật khẩu
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Cấu hình JWT
JWT_SECRET = "my_super_secret_signing_key_for_jwt_tokens"
ALGORITHM = "HS256"

app = FastAPI()

# Database giả lập lưu trữ tạm thời trong RAM
users_db = {}

# Schema dữ liệu
class UserAuthSchema(BaseModel):
    email: EmailStr
    password: str

# Khởi tạo security helper để đọc token từ header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

# Hàm băm mật khẩu
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Hàm kiểm tra mật khẩu
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

@app.post("/api/v1/auth/register")
async def register(payload: UserAuthSchema):
    if payload.email in users_db:
        raise HTTPException(status_code=400, detail="Email đã được sử dụng!")
        
    hashed_pwd = hash_password(payload.password)
    users_db[payload.email] = {
        "email": payload.email,
        "hashed_password": hashed_pwd,
        "is_vip": False
    }
    return {"status": "success", "message": "Đăng ký tài khoản thành công!"}

@app.post("/api/v1/auth/login")
async def login(payload: UserAuthSchema):
    user = users_db.get(payload.email)
    if not user or not verify_password(payload.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Email hoặc mật khẩu không chính xác!")
        
    # Tạo JWT Token hết hạn sau 15 phút
    expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    token_payload = {
        "sub": user["email"],
        "exp": expire
    }
    token = jwt.encode(token_payload, JWT_SECRET, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}

# Hàm Dependency dùng để bảo mật các route
async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        # Giải mã và kiểm tra hạn sử dụng của token
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email not in users_db:
            raise HTTPException(status_code=401, detail="Người dùng không tồn tại")
        return users_db[email]
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token không hợp lệ hoặc đã hết hạn!")

@app.get("/api/v1/vip-data")
async def get_vip_features(current_user: dict = Depends(get_current_user)):
    # Chỉ những request gửi kèm JWT hợp lệ mới chạy được vào đây
    return {
        "status": "authorized",
        "email": current_user["email"],
        "premium_content": "Chào mừng VIP! Đây là dữ liệu báo cáo chuyên sâu của AI."
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("auth_app:app", host="127.0.0.1", port=8000, reload=True)
```

---

## 3. Mini Project

### Bài tập 1: Xây dựng API Đăng nhập và tạo JWT Token (Mức độ: Trung bình)
* **Đề bài**: Viết một ứng dụng FastAPI đơn giản hỗ trợ xác thực tài khoản và trả về mã khóa JWT (JSON Web Token) cho người dùng đăng nhập thành công.
* **Mã nguồn mẫu (`jwt_auth_api.py`)**:
```python
from datetime import datetime, timedelta
from fastapi import FastAPI, HTTPException, status
from jose import jwt
from pydantic import BaseModel

app = FastAPI()
SECRET_KEY = "super_secret_jwt_key_here"
ALGORITHM = "HS256"

class LoginRequest(BaseModel):
    username: str
    password: str

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@app.post("/api/v1/login")
def login(payload: LoginRequest):
    # Xác thực tài khoản giả lập đơn giản phục vụ test
    if payload.username == "admin" and payload.password == "password123":
        access_token = create_access_token(
            data={"sub": payload.username, "role": "admin"},
            expires_delta=timedelta(minutes=30)
        )
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tên đăng nhập hoặc mật khẩu không đúng."
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
```

### Bài tập 2: Middleware kiểm tra hạn sử dụng Token trên mọi Request (Mức độ: Khó)
* **Đề bài**: Viết một hàm bảo mật dependency trong FastAPI giải mã token gửi lên từ client. Nếu token hết hạn hoặc chữ ký bị sai lệch, ngay lập tức ném ra lỗi `401 Unauthorized`. Nếu hợp lệ, trả về thông tin user đã đăng nhập.
* **Yêu cầu**: Bạn hãy tự hoàn thành không có code mẫu.
* **Gợi ý triển khai (Workflow Hints)**:
  1. Sử dụng thư viện `FastAPI` Depend `OAuth2PasswordBearer(tokenUrl="login")`.
  2. Giải mã token bằng `jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])`.
  3. Bắt lỗi `jwt.ExpiredSignatureError` and `jwt.JWTError`.

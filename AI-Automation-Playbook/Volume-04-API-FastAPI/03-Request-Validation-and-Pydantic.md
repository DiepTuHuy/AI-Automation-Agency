# Chương 03: Xác thực dữ liệu đầu vào bằng Pydantic trong FastAPI

## 1. Deep Dive (Phân tích chuyên sâu)

### Cơ chế tự động lọc dữ liệu bẩn của FastAPI
Khi client gửi request POST chứa dữ liệu JSON lên server, nếu không xác thực, code của bạn sẽ dễ bị crash nếu thiếu trường dữ liệu hoặc kiểu dữ liệu bị sai (ví dụ: client gửi chuỗi `"abc"` vào trường số điện thoại).

FastAPI giải quyết vấn đề này bằng cách sử dụng **Pydantic Models**:
1. Client gửi request POST kèm JSON body.
2. FastAPI chuyển đổi JSON thành instance của Pydantic Model đã khai báo.
3. Pydantic tự động ép kiểu và xác thực:
   - Nếu dữ liệu hợp lệ: code endpoint của bạn được thực thi.
   - Nếu dữ liệu không hợp lệ: FastAPI lập tức ngắt request, trả về HTTP status code `422 Unprocessable Entity` kèm thông tin chi tiết trường nào bị sai kiểu dữ liệu mà không chạy vào logic backend.

---

## 2. Demo: Endpoint Phân tích Ý kiến Khách hàng có Validation

### Mục tiêu
Xây dựng endpoint `/api/v1/analyze-feedback` nhận payload JSON chứa nội dung phản hồi của khách hàng và mức độ ưu tiên mong muốn, thực hiện validate kiểu dữ liệu nghiêm ngặt.

### Mã nguồn (`main.py`)
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, EmailStr

app = FastAPI()

# Định nghĩa Pydantic Model dùng để validate request body
class FeedbackRequest(BaseModel):
    customer_email: EmailStr = Field(..., description="Email của khách hàng (bắt buộc đúng định dạng).")
    feedback_text: str = Field(..., min_length=10, max_length=1000, description="Nội dung phản hồi từ 10 đến 1000 ký tự.")
    priority: int = Field(default=1, ge=1, le=5, description="Mức độ ưu tiên từ 1 (Thấp) đến 5 (Khẩn cấp).")

@app.post("/api/v1/analyze-feedback")
async def analyze_feedback(payload: FeedbackRequest):
    # Do dữ liệu đã được Pydantic validate trước khi vào đây, ta có thể tự tin sử dụng trực tiếp
    print(f"Nhận phản hồi từ: {payload.customer_email}")
    print(f"Mức độ ưu tiên: {payload.priority}")
    
    # Logic xử lý giả lập (ví dụ phân loại bằng AI)
    category = "Hỗ trợ Kỹ thuật" if "lỗi" in payload.feedback_text.lower() else "Góp ý chung"
    
    return {
        "status": "success",
        "extracted_data": {
            "email": payload.customer_email,
            "category": category,
            "is_high_priority": payload.priority >= 4
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
```

---

## 3. Mini Project

### Bài tập 1: Xác thực thông tin đăng ký tài khoản với Pydantic (Mức độ: Trung bình)
* **Đề bài**: Viết một ứng dụng FastAPI có một endpoint `POST /register` nhận thông tin đăng ký tài khoản của người dùng. Sử dụng Pydantic để bắt buộc mật khẩu phải dài từ 8 ký tự trở lên và email phải đúng định dạng.
* **Mã nguồn mẫu (`auth_validator.py`)**:
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field

app = FastAPI()

class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=20)
    email: EmailStr
    password: str = Field(..., min_length=8)

@app.post("/register")
def register_user(user: UserRegister):
    # Dữ liệu đi qua được đây nghĩa là đã được Pydantic xác thực thành công
    return {
        "message": "Đăng ký tài khoản thành công!",
        "username": user.username,
        "email": user.email
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
```

### Bài tập 2: Xác thực hóa đơn mua hàng có cấu trúc lồng nhau (Mức độ: Khó)
* **Đề bài**: Xây dựng API nhận thông tin một đơn đặt hàng trực tuyến. Sử dụng Pydantic để xác thực một đơn hàng lồng nhau chứa: thông tin khách hàng, danh sách các sản phẩm (mỗi sản phẩm gồm ID, số lượng > 0, đơn giá > 0), và mã giảm giá (tùy chọn).
* **Yêu cầu**: Học viên tự hoàn thành không có code mẫu.
* **Gợi ý triển khai (Workflow Hints)**:
  1. Tạo class Pydantic `OrderItem` đại diện cho sản phẩm với thuộc tính `gt=0` (greater than 0) cho số lượng và đơn giá.
  2. Tạo class `Order` chứa trường `items: List[OrderItem]`.
  3. Định nghĩa endpoint `POST /orders` nhận tham số body là class `Order`.

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
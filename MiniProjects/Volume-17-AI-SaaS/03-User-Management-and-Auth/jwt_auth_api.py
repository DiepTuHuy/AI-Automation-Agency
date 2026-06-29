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
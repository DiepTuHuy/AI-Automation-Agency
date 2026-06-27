import os
import jwt
import datetime
import stripe
from fastapi import FastAPI, Depends, HTTPException, status, Request, Header
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, Field, EmailStr
from passlib.context import CryptContext
from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, Session

# Tải cấu hình
JWT_SECRET = os.getenv("JWT_SECRET", "super_secret_signing_key_123")
STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "whsec_mock")
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# Cấu hình DB
DATABASE_URL = "sqlite:///saas_database.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Cấu hình bảo mật
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

# --- DATABASE MODELS ---
class TenantUser(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tenant_id = Column(String(50), index=True, nullable=False) # Định danh doanh nghiệp/tenant
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(100), nullable=False)
    is_vip = Column(Boolean, default=False)

class TenantData(Base):
    __tablename__ = "tenant_data"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tenant_id = Column(String(50), ForeignKey("users.tenant_id"), index=True, nullable=False)
    data_content = Column(String(255), nullable=False)

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI SaaS Platform Engine", version="1.0.0")

# Dependency DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- AUTH UTILS ---
class RegisterSchema(BaseModel):
    email: EmailStr
    password: str
    tenant_name: str = Field(..., example="Công ty A")

class LoginSchema(BaseModel):
    email: EmailStr
    password: str

@app.post("/api/v1/auth/register")
async def register_tenant(payload: RegisterSchema, db: Session = Depends(get_db)):
    # Tạo tenant ID duy nhất dựa trên tên
    tenant_id = f"tenant_{payload.tenant_name.lower().replace(' ', '_')}"
    
    # Kiểm tra email tồn tại
    existing_user = db.query(TenantUser).filter(TenantUser.email == payload.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email đã được đăng ký!")
        
    db_user = TenantUser(
        tenant_id=tenant_id,
        email=payload.email,
        hashed_password=pwd_context.hash(payload.password),
        is_vip=False
    )
    db.add(db_user)
    db.commit()
    return {"status": "success", "tenant_id": tenant_id, "message": "Đăng ký doanh nghiệp thành công!"}

@app.post("/api/v1/auth/login")
async def login_tenant(payload: LoginSchema, db: Session = Depends(get_db)):
    user = db.query(TenantUser).filter(TenantUser.email == payload.email).first()
    if not user or not pwd_context.verify(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Tài khoản hoặc mật khẩu không chính xác!")
        
    # Tạo JWT token chứa email và tenant_id
    expire = datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    token_payload = {
        "sub": user.email,
        "tenant_id": user.tenant_id,
        "exp": expire
    }
    token = jwt.encode(token_payload, JWT_SECRET, algorithm="HS256")
    return {"access_token": token, "token_type": "bearer"}

async def get_current_user_tenant(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> TenantUser:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        email: str = payload.get("sub")
        user = db.query(TenantUser).filter(TenantUser.email == email).first()
        if not user:
            raise HTTPException(status_code=401, detail="User không tồn tại")
        return user
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token không hợp lệ hoặc đã hết hạn!")

# --- SECURE MULTI-TENANT ENDPOINTS ---
@app.post("/api/v1/data")
async def add_tenant_data(content: str, current_user: TenantUser = Depends(get_current_user_tenant), db: Session = Depends(get_db)):
    # Luôn tự động gắn tenant_id của user đang login vào dữ liệu ghi nhận
    new_data = TenantData(
        tenant_id=current_user.tenant_id,
        data_content=content
    )
    db.add(new_data)
    db.commit()
    return {"status": "success", "message": f"Đã lưu dữ liệu vào phân vùng: {current_user.tenant_id}"}

@app.get("/api/v1/data")
async def get_tenant_data(current_user: TenantUser = Depends(get_current_user_tenant), db: Session = Depends(get_db)):
    # Đảm bảo tuyệt đối: Chỉ tìm kiếm dữ liệu thuộc về tenant_id của user hiện tại
    data = db.query(TenantData).filter(TenantData.tenant_id == current_user.tenant_id).all()
    return {
        "tenant_id": current_user.tenant_id,
        "records": [item.data_content for item in data]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)

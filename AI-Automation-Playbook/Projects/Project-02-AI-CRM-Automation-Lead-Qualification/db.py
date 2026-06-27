import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///crm_leads.db")

# Khởi tạo engine database (Sử dụng pool_pre_ping để tự kiểm tra kết nối còn sống)
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency cung cấp database session cho API endpoint
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

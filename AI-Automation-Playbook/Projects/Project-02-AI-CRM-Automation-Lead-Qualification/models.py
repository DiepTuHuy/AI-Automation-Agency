from sqlalchemy import Column, Integer, String, Text, Boolean, Float, DateTime
from datetime import datetime
from db import Base

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    company = Column(String(100), nullable=True)
    budget = Column(Float, default=0.0)
    project_description = Column(Text, nullable=False)
    
    # Kết quả chấm điểm bằng AI
    is_qualified = Column(Boolean, default=False)
    qualification_score = Column(Integer, default=0) # Thang điểm 1-100
    ai_reasoning = Column(Text, nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)

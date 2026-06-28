import os
from fastapi import FastAPI, Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field, EmailStr
import google.generativeai as genai
from dotenv import load_dotenv

from db import engine, Base, get_db
from models import Lead

# Tải cấu hình
load_dotenv()
SYSTEM_API_KEY = os.getenv("SYSTEM_API_KEY", "crm_secret_key_123")
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    # Fallback central config load
    from pathlib import Path
    load_dotenv(Path(__file__).resolve().parents[3] / "AI-Playbook-Platform" / ".env")
    api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)

# Khởi tạo bảng dữ liệu
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI CRM Lead Qualification Backend", version="1.0.0")

# Định nghĩa Schema dữ liệu gửi lên từ n8n
class LeadCreateSchema(BaseModel):
    name: str = Field(..., example="Nguyen Van A")
    email: EmailStr = Field(..., example="a@example.com")
    company: str = Field(None, example="Công ty TNHH Hoàng Hà")
    budget: float = Field(..., ge=0, example=5000.0)
    project_description: str = Field(..., example="Cần xây dựng chatbot tự động trả lời Fanpage kết nối CRM.")

# Định nghĩa Schema của AI trả về khi chấm điểm
class AIQualificationSchema(BaseModel):
    is_qualified: bool = Field(description="Lead có đạt yêu cầu tiềm năng hay không (Budget >= 3000 USD và mô tả rõ ràng).")
    qualification_score: int = Field(description="Điểm đánh giá từ 1 đến 100 dựa trên mức độ tiềm năng hợp tác.")
    ai_reasoning: str = Field(description="Giải thích ngắn gọn lý do cho số điểm trên.")

# Dependency xác thực API Key của hệ thống
def verify_api_key(x_api_key: str = Header(..., description="API Key xác thực hệ thống")):
    if x_api_key != SYSTEM_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Không có quyền truy cập API!"
        )

def qualify_lead_with_ai(lead_data: LeadCreateSchema) -> AIQualificationSchema:
    prompt = f"""Hãy đánh giá mức độ tiềm năng của khách hàng này dựa trên thông tin sau:
- Tên khách hàng: {lead_data.name}
- Ngân sách dự chi: {lead_data.budget} USD
- Yêu cầu dự án: {lead_data.project_description}

Tiêu chí đánh giá:
1. is_qualified: Đánh giá là True nếu ngân sách >= 3000 USD và mô tả dự án rõ ràng, khả thi. Ngược lại là False.
2. qualification_score: Cho điểm từ 1-100. Ngân sách càng cao điểm càng cao. Mô tả càng chi tiết điểm càng tốt.
3. ai_reasoning: Giải thích ngắn gọn lý do vì sao cho điểm như vậy.
"""
    
    model = genai.GenerativeModel(
        "gemini-2.5-flash",
        system_instruction="Bạn là chuyên gia thẩm định dự án và chấm điểm khách hàng tiềm năng."
    )
    
    response = model.generate_content(
        prompt,
        generation_config={
            "response_mime_type": "application/json",
            "response_schema": AIQualificationSchema,
            "temperature": 0.0
        }
    )
    return AIQualificationSchema.model_validate_json(response.text)

@app.post("/api/v1/leads", dependencies=[Depends(verify_api_key)], response_model=dict)
async def create_and_qualify_lead(payload: LeadCreateSchema, db: Session = Depends(get_db)):
    print(f"Nhận lead mới: {payload.name} ({payload.email})")
    
    # 1. Gọi AI để chấm điểm lead
    try:
        ai_evaluation = qualify_lead_with_ai(payload)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Lỗi khi gọi AI chấm điểm: {str(e)}"
        )
        
    # 2. Tạo đối tượng DB Lead và lưu vào SQL
    db_lead = Lead(
        name=payload.name,
        email=payload.email,
        company=payload.company,
        budget=payload.budget,
        project_description=payload.project_description,
        is_qualified=ai_evaluation.is_qualified,
        qualification_score=ai_evaluation.qualification_score,
        ai_reasoning=ai_evaluation.ai_reasoning
    )
    
    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)
    
    return {
        "status": "success",
        "lead_id": db_lead.id,
        "is_qualified": db_lead.is_qualified,
        "score": db_lead.qualification_score,
        "reason": db_lead.ai_reasoning
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

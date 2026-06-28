import os
import json
import logging
from pathlib import Path
from typing import List
from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, Field
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Playbook Quiz Service", version="1.0.0")

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Quiz_Service")

PLAYBOOK_DIR = Path(os.getenv("PLAYBOOK_DIR", "../AI-Automation-Playbook")).resolve()
if not PLAYBOOK_DIR.exists():
    PLAYBOOK_DIR = Path("/Users/dieptuhuy/Documents/AI Automation/AI-Automation-Playbook").resolve()

logger.info(f"Quiz Service initialized with Playbook Base: {PLAYBOOK_DIR}")

class ConfigPayload(BaseModel):
    gemini_api_key: str

def validate_safe_path(requested_path_str: str) -> Path:
    requested_path = Path(requested_path_str).resolve()
    if not requested_path.is_relative_to(PLAYBOOK_DIR):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Truy cập bị từ chối: Đường dẫn không an toàn!"
        )
    if not requested_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tệp tin không tồn tại!"
        )
    return requested_path

@app.get("/api/config")
async def check_config():
    key = os.getenv("GEMINI_API_KEY")
    return {"key_configured": bool(key)}

@app.post("/api/config")
async def update_config(payload: ConfigPayload):
    try:
        # Write to root-level .env (which is up one level from quiz-service directory, or relative to current run dir)
        env_path = Path(".env")
        lines = []
        key_written = False
        
        if env_path.exists():
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith("GEMINI_API_KEY="):
                        lines.append(f"GEMINI_API_KEY={payload.gemini_api_key}\n")
                        key_written = True
                    else:
                        lines.append(line)
        
        if not key_written:
            lines.append(f"GEMINI_API_KEY={payload.gemini_api_key}\n")
            lines.append(f"PLAYBOOK_DIR={PLAYBOOK_DIR}\n")
            
        with open(env_path, "w", encoding="utf-8") as f:
            f.writelines(lines)
            
        os.environ["GEMINI_API_KEY"] = payload.gemini_api_key
        logger.info("Successfully updated GEMINI_API_KEY")
        return {"status": "success", "message": "API Key updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi ghi cấu hình: {str(e)}")

@app.get("/api/quiz")
async def generate_quiz_from_file(
    path: str = Query(..., description="Absolute path of the chapter file"),
    difficulty: str = Query("medium", description="Difficulty level: easy, medium, hard"),
    limit: int = Query(5, description="Number of questions to generate (1 to 30)")
):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Vui lòng cấu hình GEMINI_API_KEY trước khi tạo trắc nghiệm!"
        )
        
    safe_path = validate_safe_path(path)
    
    try:
        content = safe_path.read_text(encoding="utf-8")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi đọc file: {str(e)}")
        
    # Map difficulty to Vietnamese description
    diff_text = {
        "easy": "DỄ (nhận biết trực tiếp kiến thức trong bài giảng, các câu hỏi cơ bản)",
        "medium": "TRUNG BÌNH (thông hiểu và áp dụng, đòi hỏi phân tích nhẹ)",
        "hard": "KHÓ (phân tích sâu, suy luận logic, giải quyết tình huống thực tế phức tạp)"
    }.get(difficulty, "TRUNG BÌNH")

    prompt = f"""Dưới đây là nội dung bài giảng của một chương trong tài liệu 'AI Automation Engineer Playbook'.
Nhiệm vụ của bạn là biên soạn đúng chính xác {limit} câu hỏi trắc nghiệm tiếng Việt chất lượng cao với mức độ khó: {diff_text} để kiểm tra mức độ hiểu bài của học sinh dựa trên nội dung này.

Yêu cầu kỹ thuật:
1. Mỗi câu hỏi phải có chính xác 4 lựa chọn (A, B, C, D).
2. Phải có 1 chỉ thị correct_index (số nguyên từ 0 đến 3) đại diện cho đáp án đúng.
3. Phải cung cấp phần 'explanation' (giải thích ngắn gọn vì sao đáp án đó đúng và các đáp án khác sai dựa trên nội dung bài giảng).
4. Quy định nghiêm ngặt về cấu trúc đáp án để đảm bảo tính phân loại và đòi hỏi tư duy cao:
   - Cả 4 lựa chọn (A, B, C, D) phải có độ dài tương đồng nhau, viết cùng một cấu trúc ngữ pháp và mức độ chi tiết như nhau. Tuyệt đối KHÔNG được để đáp án đúng dài hơn hoặc chi tiết hơn hẳn các đáp án sai.
   - Các đáp án sai (phương án nhiễu) phải cực kỳ tương đồng về mặt từ ngữ, thuật ngữ và cấu trúc với đáp án đúng, chỉ khác biệt rất ít ở các chi tiết kỹ thuật cốt lõi (ví dụ: đổi tên hàm, thay đổi logic tham số, hoặc đảo ngược nguyên lý hoạt động). Học sinh phải đọc kỹ và phân tích sâu sắc mới phân biệt được.
5. Bạn BẮT BUỘC phải trả về dữ liệu đúng cấu trúc JSON định hình sau:
{{
  "questions": [
    {{
      "question": "Câu hỏi số 1...",
      "options": ["Lựa chọn A", "Lựa chọn B", "Lựa chọn C", "Lựa chọn D"],
      "correct_index": 0,
      "explanation": "Giải thích chi tiết..."
    }}
  ]
}}

Nội dung bài giảng chương:
{content}
"""

    try:
        genai.configure(api_key=api_key)
        # Using gemini-2.5-flash for fast and cost-effective structured responses
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(
            prompt,
            generation_config={"response_mime_type": "application/json"}
        )
        quiz_data = json.loads(response.text)
        return quiz_data
    except Exception as e:
        logger.error(f"Error calling Gemini API: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Lỗi kết nối hoặc xử lý của Gemini API: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8002, reload=True)

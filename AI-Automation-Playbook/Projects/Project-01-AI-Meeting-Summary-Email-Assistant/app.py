import os
import json
from typing import List
from pathlib import Path
from pydantic import BaseModel, Field
import google.generativeai as genai
from dotenv import load_dotenv

# Tải biến môi trường
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    # Fallback to loading from the central platform .env if running from this context
    load_dotenv(Path(__file__).resolve().parents[3] / "AI-Playbook-Platform" / ".env")
    api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)

# Định nghĩa Pydantic Schema cho kết quả tóm tắt cuộc họp
class ActionItem(BaseModel):
    assignee: str = Field(description="Tên người chịu trách nhiệm thực hiện.")
    task: str = Field(description="Mô tả công việc chi tiết cần làm.")
    deadline: str = Field(description="Thời hạn hoàn thành công việc (nếu có đề cập, nếu không thì ghi 'N/A').")

class MeetingSummary(BaseModel):
    project_name: str = Field(description="Tên dự án được thảo luận trong cuộc họp.")
    key_decisions: List[str] = Field(description="Danh sách các quyết định hoặc thống nhất quan trọng đạt được.")
    action_items: List[ActionItem] = Field(description="Danh sách các đầu việc cần làm và phân công cụ thể.")

def analyze_meeting(transcript_path: Path) -> MeetingSummary:
    if not transcript_path.exists():
        raise FileNotFoundError(f"Không tìm thấy file: {transcript_path}")

    transcript = transcript_path.read_text(encoding="utf-8")

    print("[Step 1] Đang gửi biên bản cuộc họp tới Gemini để phân tích cấu trúc...")
    
    # Sử dụng gemini-2.5-flash cho tác vụ xử lý thông tin nhanh
    model = genai.GenerativeModel("gemini-2.5-flash")
    
    prompt = f"""Bạn là thư ký ảo chuyên nghiệp. Hãy đọc biên bản cuộc họp sau và trích xuất tóm tắt chính xác theo định dạng yêu cầu.
Biên bản cuộc họp:
{transcript}"""

    response = model.generate_content(
        prompt,
        generation_config={
            "response_mime_type": "application/json",
            "response_schema": MeetingSummary,
            "temperature": 0.0
        }
    )
    
    return MeetingSummary.model_validate_json(response.text)

def generate_email_draft(summary: MeetingSummary) -> str:
    print("[Step 2] Đang tự động viết bản thảo email dựa trên kết quả phân tích...")
    
    # Chuyển đổi đối tượng summary thành chuỗi JSON để gửi làm ngữ cảnh
    summary_json = json.dumps(summary.model_dump(), indent=2, ensure_ascii=False)
    
    prompt = f"""Dựa trên thông tin tóm tắt cuộc họp dưới đây, hãy viết một email gửi toàn thể đội ngũ dự án.
Email cần có cấu trúc:
- Tiêu đề email rõ ràng, chuyên nghiệp.
- Lời chào mừng.
- Tóm tắt các quyết định chính đạt được.
- Bảng phân công công việc (Action Items) chi tiết cho từng người.
- Lời chúc và nhắc nhở thời hạn.

Dữ liệu cuộc họp:
{summary_json}
"""

    model = genai.GenerativeModel(
        "gemini-2.5-flash",
        system_instruction="Bạn là CEO viết email truyền cảm hứng và rõ ràng cho nhân viên."
    )
    
    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": 0.7
        }
    )
    return response.text

if __name__ == "__main__":
    current_dir = Path(__file__).parent
    transcript_file = current_dir / "meeting_transcript.txt"
    summary_output_file = current_dir / "summary.json"
    email_draft_file = current_dir / "email_draft.txt"

    try:
        # Bước 1: Phân tích cuộc họp
        summary_result = analyze_meeting(transcript_file)
        
        # Lưu kết quả tóm tắt dạng JSON
        with open(summary_output_file, "w", encoding="utf-8") as f:
            json.dump(summary_result.model_dump(), f, indent=4, ensure_ascii=False)
        print(f"-> Đã lưu kết quả phân tích vào: {summary_output_file.name}")

        # Bước 2: Sinh email nháp
        email_content = generate_email_draft(summary_result)
        
        # Lưu email nháp dạng text
        with open(email_draft_file, "w", encoding="utf-8") as f:
            f.write(email_content)
        print(f"-> Đã lưu bản thảo email vào: {email_draft_file.name}")
        
        print("\n=== NỘI DUNG EMAIL BẢN THẢO SINH RA ===")
        print(email_content)
        print("========================================")

    except Exception as e:
        print(f"Đã xảy ra lỗi trong quá trình chạy: {e}")

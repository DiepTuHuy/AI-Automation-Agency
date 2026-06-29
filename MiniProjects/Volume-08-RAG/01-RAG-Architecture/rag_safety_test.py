import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

kb_documents = {
    "doc_01": "Chính sách gửi xe: Nhân viên được công ty hỗ trợ 100% chi phí gửi xe máy tại hầm tòa nhà Landmark.",
    "doc_02": "Quy chế giờ giấc: Giờ làm việc bắt đầu từ 8:30 sáng và kết thúc lúc 5:30 chiều, từ thứ Hai đến thứ Sáu."
}

def mock_retrieval(query: str) -> str:
    # Trả về chuỗi rỗng nếu không tìm thấy từ khóa liên quan
    query_lower = query.lower()
    for content in kb_documents.values():
        if "gửi xe" in query_lower or "giờ làm" in query_lower:
            return content
    return ""

def ask_rag_system(query: str) -> str:
    context = mock_retrieval(query)
    
    system_prompt = f"""Bạn là trợ lý giải đáp thắc mắc nội bộ của công ty.
Hãy trả lời câu hỏi của người dùng một cách chính xác dựa trên phần Ngữ cảnh được cung cấp dưới đây.
Quy tắc bắt buộc:
1. Nếu câu hỏi không thể trả lời dựa trên Ngữ cảnh, hãy trả lời 'Tôi không tìm thấy thông tin này trong tài liệu hướng dẫn nội bộ.'
2. Tuyệt đối không tự ý bịa đặt hoặc dùng kiến thức bên ngoài.

Ngữ cảnh:
{context}
"""
    model = genai.GenerativeModel(
        "gemini-2.5-flash",
        system_instruction=system_prompt
    )
    response = model.generate_content(
        query,
        generation_config={"temperature": 0.0}
    )
    return response.text

if __name__ == "__main__":
    out_of_scope_query = "Thủ đô của nước Pháp là gì?"
    print(f"Câu hỏi: {out_of_scope_query}")
    answer = ask_rag_system(out_of_scope_query)
    print(f"AI phản hồi: {answer}")
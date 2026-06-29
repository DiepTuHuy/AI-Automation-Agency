import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

documents = [
    "Quy định nghỉ lễ: Công ty nghỉ làm việc vào các ngày lễ Tết quốc gia theo luật lao động.",
    "Hỗ trợ gửi xe: Công ty hỗ trợ tiền gửi xe máy 200k/tháng cho nhân viên chính thức.",
    "Lịch nghỉ hè: Công ty tổ chức du lịch hè cho toàn thể nhân viên vào tháng 7 hàng năm."
]

def rerank_documents(query: str, docs: list) -> list:
    model = genai.GenerativeModel("gemini-2.5-flash")
    scored_docs = []
    
    for doc in docs:
        prompt = f"Đánh giá độ liên quan của Tài liệu dưới đây với Câu hỏi. Trả về một con số từ 0.0 (hoàn toàn không liên quan) đến 1.0 (hoàn toàn liên quan). Chỉ trả về số.\n\nCâu hỏi: {query}\nTài liệu: {doc}"
        res = model.generate_content(prompt)
        try:
            score = float(res.text.strip())
        except ValueError:
            score = 0.0
        scored_docs.append((score, doc))
        
    # Sắp xếp giảm dần theo điểm số
    scored_docs.sort(key=lambda x: x[0], reverse=True)
    return scored_docs

if __name__ == "__main__":
    question = "Khi nào công ty đi du lịch hè?"
    ranked = rerank_documents(question, documents)
    print(f"Câu hỏi: {question}\nKết quả xếp hạng lại:")
    for score, doc in ranked:
        print(f"[{score:.2f}] - {doc}")
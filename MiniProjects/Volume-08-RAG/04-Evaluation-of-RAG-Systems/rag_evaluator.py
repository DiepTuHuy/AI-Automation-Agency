import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

context = "Chính sách: Công ty trợ cấp 100% tiền gửi xe máy tại tòa nhà văn phòng."
rag_answer = "Nhân viên sẽ được công ty thanh toán toàn bộ tiền gửi xe máy và cả tiền gửi ô tô."

def evaluate_faithfulness(ctx: str, ans: str) -> str:
    prompt = f"""Bạn là chuyên gia kiểm định chất lượng AI. Hãy đánh giá xem Câu trả lời có hoàn toàn trung thực và chỉ dựa vào Ngữ cảnh được cung cấp hay không.
Nếu Câu trả lời chứa thông tin không có trong Ngữ cảnh (bị ảo tưởng/bịa đặt), hãy đánh giá là [FAILED] kèm lý do. Nếu hoàn toàn chính xác, đánh giá là [PASSED].

Ngữ cảnh:
{ctx}

Câu trả lời:
{ans}

Kết quả kiểm định:"""

    model = genai.GenerativeModel("gemini-2.5-flash")
    res = model.generate_content(prompt, generation_config={"temperature": 0.0})
    return res.text.strip()

if __name__ == "__main__":
    result = evaluate_faithfulness(context, rag_answer)
    print("Kết quả đánh giá hệ thống:")
    print(result)
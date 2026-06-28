# Chương 04: Đánh giá chất lượng hệ thống RAG bằng LLM-as-a-Judge

## 1. Deep Dive (Phân tích chuyên sâu)

Làm thế nào để biết hệ thống RAG của bạn hoạt động tốt và an toàn trước khi bàn giao cho khách hàng? Bạn không thể ngồi đọc thủ công 1,000 câu trả lời mỗi khi thay đổi prompt hoặc cấu hình chunk size.

Chúng ta cần tự động hóa việc đánh giá bằng cách sử dụng chính LLM làm giám khảo (**LLM-as-a-judge**).

### Ba chỉ số cốt lõi đánh giá RAG (RAG Triad)
1. **Context Relevance (Độ liên quan của ngữ cảnh)**: Đo lường xem tài liệu truy xuất được từ DB có thực sự chứa thông tin để trả lời câu hỏi không.
2. **Groundedness / Faithfulness (Độ trung thực)**: Đo lường xem câu trả lời của AI có hoàn toàn dựa trên ngữ cảnh được cung cấp hay tự bịa ra kiến thức ngoài (ảo tưởng).
3. **Answer Relevance (Độ liên quan của câu trả lời)**: Đo lường xem câu trả lời của AI có giải quyết trực tiếp câu hỏi người dùng đặt ra không, hay trả lời lan man lạc đề.

---

## 2. Demo: Viết script tự động chấm điểm Groundedness

### Mục tiêu
Xây dựng một module Python sử dụng mô hình GPT-4o-mini đóng vai trò giám khảo, phân tích câu trả lời của AI so với ngữ cảnh gốc và xuất ra điểm số từ 1 đến 5 kèm lời giải thích.

### Mã nguồn (`rag_evaluator.py`)
```python
import os
from pydantic import BaseModel, Field
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Định nghĩa Schema kết quả đánh giá của giám khảo
class EvaluationResult(BaseModel):
    groundedness_score: int = Field(description="Điểm độ trung thực từ 1 (Hoàn toàn bịa đặt) đến 5 (Hoàn toàn dựa trên ngữ cảnh).")
    explanation: str = Field(description="Giải thích chi tiết tại sao cho điểm số này, chỉ ra câu nào bịa đặt nếu có.")

def evaluate_groundedness(context: str, answer: str) -> EvaluationResult:
    prompt = f"""Bạn là giám khảo kiểm định chất lượng AI độc lập. Hãy chấm điểm chỉ số Groundedness (Độ trung thực).
Nhiệm vụ: Hãy kiểm tra xem Câu trả lời có hoàn toàn được suy ra trực tiếp từ phần Ngữ cảnh hay không.

Ngữ cảnh:
{context}

Câu trả lời của AI:
{answer}
"""
    
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Bạn là chuyên gia kiểm định chất lượng RAG."},
            {"role": "user", "content": prompt}
        ],
        response_format=EvaluationResult,
        temperature=0
    )
    return completion.choices[0].message.parsed

if __name__ == "__main__":
    context_data = "Công ty TNHH Antigravity được thành lập vào năm 2024 bởi Huy Diep, chuyên cung cấp giải pháp AI tự động hóa quy trình nghiệp vụ."
    
    # Test case 1: Câu trả lời trung thực
    good_answer = "Công ty Antigravity do Huy Diep sáng lập vào năm 2024."
    res_1 = evaluate_groundedness(context_data, good_answer)
    print(f"--- Đánh giá Test 1 (Trung thực) ---")
    print(f"Điểm: {res_1.groundedness_score}/5 | Lý do: {res_1.explanation}\n")
    
    # Test case 2: Câu trả lời có ảo tưởng thêm thông tin ngoài
    hallucinated_answer = "Công ty Antigravity do Huy Diep thành lập vào năm 2024 và có trụ sở chính tại thành phố Hồ Chí Minh."
    res_2 = evaluate_groundedness(context_data, hallucinated_answer)
    print(f"--- Đánh giá Test 2 (Ảo tưởng địa chỉ) ---")
    print(f"Điểm: {res_2.groundedness_score}/5 | Lý do: {res_2.explanation}")
```

---

## 3. Mini Project

### Bài tập 1: Đánh giá chất lượng câu trả lời RAG bằng LLM (Mức độ: Trung bình)
* **Đề bài**: Viết một script Python sử dụng mô hình Gemini đóng vai trò là giám khảo (LLM-as-a-Judge) để chấm điểm câu trả lời của hệ thống RAG dựa trên thông tin ngữ cảnh nguồn (kiểm tra xem câu trả lời có bịa đặt thông tin không).
* **Mã nguồn mẫu (`rag_evaluator.py`)**:
```python
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
```

### Bài tập 2: Xây dựng bộ khung kiểm thử tự động hệ thống RAG (Mức độ: Khó)
* **Đề bài**: Viết một script chạy kiểm thử tự động trên một bộ dữ liệu gồm 5 câu hỏi test (Test Set). Thực hiện gọi hệ thống RAG của bạn, lấy câu trả lời và tự động chấm điểm độ chính xác cho từng câu. Xuất báo cáo thống kê tỷ lệ % vượt qua kiểm thử (Pass Rate) ra file markdown.
* **Yêu cầu**: Học viên tự hoàn thành không có code mẫu.
* **Gợi ý triển khai (Workflow Hints)**:
  1. Tạo danh sách các test cases gồm câu hỏi và context chuẩn.
  2. Viết vòng lặp gửi request kiểm tra và gọi hàm đánh giá `evaluate_faithfulness`.
  3. Tính toán tỷ lệ phần trăm: \text{Pass Rate} = \frac{\text{Số câu PASSED}}{\text{Tổng số câu}} \times 100\%.

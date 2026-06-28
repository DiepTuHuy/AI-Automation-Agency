# Chương 01: Kiến trúc RAG cơ bản & Luồng chạy dữ liệu

## 1. Deep Dive (Phân tích chuyên sâu)

### Giới hạn của mô hình ngôn ngữ tĩnh
Khi một mô hình LLM được huấn luyện xong, bộ não (weights) của nó hoàn toàn đóng băng. Nó không biết về các sự kiện xảy ra sau ngày huấn luyện cuối cùng, và tuyệt đối không biết gì về dữ liệu nội bộ riêng tư của bạn.

Để giải quyết, chúng ta có hai cách tiếp cận chính:
1. **Fine-tuning (Tinh chỉnh)**: Tiếp tục huấn luyện mô hình trên dữ liệu mới.
   - *Hạn chế*: Cực kỳ đắt đỏ, mất nhiều thời gian, dữ liệu bị ghi nhớ tĩnh (không thể cập nhật theo thời gian thực), và dễ gây ra hiện tượng mô hình bị quên kiến thức cũ.
2. **RAG (Retrieval-Augmented Generation)**: Tiếp cận theo hướng cung cấp thông tin động (In-Context Learning). RAG tách biệt hoàn toàn phần bộ nhớ tri thức (lưu trữ ngoài DB) và phần suy luận ngôn ngữ (LLM).

### 3 Pha của quy trình RAG
```
1. INGESTION (Nạp dữ liệu)
   [Tài liệu gốc PDF] ──> [Cắt nhỏ thành Chunk] ──> [Nhúng thành Vector] ──> [Lưu Vector DB]

2. RETRIEVAL (Truy xuất)
   [Câu hỏi người dùng] ──> [Nhúng thành Vector] ──> [Truy vấn Vector DB] ──> [Lấy ra Top K Chunks]

3. GENERATION (Sinh câu trả lời)
   [Prompt + Top K Chunks + Câu hỏi] ──> [LLM] ──> [Câu trả lời chính xác dẫn nguồn]
```

---

## 2. Demo: Hệ thống RAG tối giản bằng Python thuần

### Mục tiêu
Xây dựng một chương trình RAG đơn giản sử dụng một database nhỏ dạng Python Dictionary giả lập để hiểu rõ cơ chế nhét ngữ cảnh vào prompt.

### Mã nguồn (`simple_rag.py`)
```python
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Kho dữ liệu nội bộ giả lập của công ty (Knowledge Base)
kb_documents = {
    "doc_01": "Chính sách gửi xe: Nhân viên được công ty hỗ trợ 100% chi phí gửi xe máy tại hầm tòa nhà Landmark.",
    "doc_02": "Quy chế giờ giấc: Giờ làm việc bắt đầu từ 8:30 sáng và kết thúc lúc 5:30 chiều, từ thứ Hai đến thứ Sáu.",
    "doc_03": "Chế độ thai sản: Lao động nữ được nghỉ thai sản 6 tháng theo quy định pháp luật và nhận gói quà trị giá 5 triệu VND từ công ty."
}

def retrieve_context(query: str) -> str:
    query_lower = query.lower()
    matched_chunks = []
    
    for doc_id, content in kb_documents.items():
        keywords = ["gửi xe", "giờ làm", "thai sản", "mấy giờ", "xe máy"]
        for kw in keywords:
            if kw in query_lower and kw in content.lower():
                matched_chunks.append(content)
                break
                
    return "\n".join(matched_chunks)

def generate_answer(query: str, context: str) -> str:
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
    query_user = "Tôi có được miễn phí gửi xe máy không và gửi ở đâu?"
    
    print(f"Câu hỏi: {query_user}")
    # 1. Truy xuất
    context = retrieve_context(query_user)
    print(f"Ngữ cảnh tìm được:\n{context}\n")
    
    # 2. Sinh câu trả lời
    answer = generate_answer(query_user, context)
    print(f"AI phản hồi:\n{answer}")
```

---

## 3. Mini Project
Hãy chạy thử nghiệm script trên với một câu hỏi hoàn toàn ngoài phạm vi tài liệu (ví dụ: "Thủ đô của nước Pháp là gì?"). Kiểm tra xem AI có nghiêm túc tuân thủ quy tắc từ chối trả lời không. Chụp màn hình console kết quả chạy của bạn.

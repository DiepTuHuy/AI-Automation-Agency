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

### Bài tập 1: Kiểm thử an toàn thông tin RAG (Mức độ: Trung bình)
* **Đề bài**: Sử dụng mã nguồn đơn giản của RAG đã học ở chương này để chạy kiểm thử với câu hỏi nằm ngoài phạm vi tài liệu (Ví dụ: "Thủ đô của nước Pháp là gì?"). Hãy đảm bảo AI tuân thủ nghiêm ngặt quy tắc từ chối trả lời thay vì ảo tưởng (hallucination).
* **Mã nguồn mẫu (`rag_safety_test.py`)**:
```python
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
```

### Bài tập 2: Hệ thống RAG chẩn đoán triệu chứng thiết bị (Mức độ: Khó)
* **Đề bài**: Xây dựng hệ thống RAG chẩn đoán lỗi phần cứng máy tính. Cơ sở dữ liệu chứa 3 chỉ dẫn chẩn đoán lỗi (ví dụ: máy kêu tít tít, máy màn hình xanh chữ trắng, máy không nhận ổ cứng). Khi người dùng nhập mô tả lỗi, hệ thống truy xuất chỉ dẫn đúng và hiển thị cách sửa. Nếu người dùng nhập lỗi lạ không có trong database, AI phải báo không chẩn đoán được và đề xuất đem máy ra trung tâm bảo hành gần nhất.
* **Yêu cầu**: Học viên tự hoàn thành không có code mẫu.
* **Gợi ý triển khai (Workflow Hints)**:
  1. Tạo dictionary chứa 3 lỗi và cách khắc phục tương ứng.
  2. Viết hàm chẩn đoán nhận câu hỏi, thực hiện tìm kiếm từ khóa chẩn đoán thô (hoặc dùng ChromaDB nếu đã học ở chương trước).
  3. Viết system prompt ra lệnh ép AI từ chối suy đoán bừa các lỗi không được cấp thông tin chẩn đoán.

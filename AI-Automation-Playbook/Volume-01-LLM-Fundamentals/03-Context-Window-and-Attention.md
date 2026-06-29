# Chương 03: Quản lý Cửa sổ Ngữ cảnh (Context Window)

## 1. Deep Dive (Phân tích chuyên sâu)

### Giới hạn Cửa sổ Ngữ cảnh (Context Window)
Cửa sổ ngữ cảnh là tổng số lượng token tối đa mà hệ thống có thể tiếp nhận và sinh ra trong một chu kỳ làm việc.
- GPT-4o có context window 128,000 tokens.
- Gemini 1.5 Pro hỗ trợ lên tới 2,000,000 tokens.

Tuy nhiên, **ĐỪNG lạm dụng việc nhồi nhét dữ liệu vào context window lớn** vì 3 lý do kỹ thuật Production:
1. **Độ trễ tăng cao (High Latency)**: LLM xử lý càng nhiều token đầu vào thì thời gian phản hồi (Time to First Token) càng lâu do thuật toán tự chú ý có độ phức tạp tính toán phi tuyến tính $O(N^2)$.
2. **Chi phí gia tăng (Cost escalation)**: Chi phí tỷ lệ thuận với số lượng token gửi đi. Mỗi lượt chat gửi lại toàn bộ tài liệu dài sẽ làm hóa đơn API tăng chóng mặt.
3. **Hiện tượng suy giảm độ chính xác (Lost in the Middle)**: Các nghiên cứu chỉ ra rằng LLM rất dễ bỏ quên hoặc bỏ qua các thông tin quan trọng nằm ở phần giữa của prompt đầu vào dài.

---

## 2. Demo: Tự động Cắt ngắn Lịch sử Chat (Context Window Truncation)

### Mục tiêu
Xây dựng một bộ lọc lịch sử trò chuyện (Chat Memory Manager) để đảm bảo tổng số lượng token của cuộc hội thoại luôn nằm trong giới hạn an toàn quy định trước.

### Mã nguồn (`memory_manager.py`)
```python
import tiktoken

class ChatMemoryManager:
    def __init__(self, max_token_limit: int = 2000, model_name: str = "gpt-4o"):
        self.max_token_limit = max_token_limit
        self.encoding = tiktoken.encoding_for_model(model_name)
        self.history = [] # Lưu danh sách dict dạng {"role": "...", "content": "..."}

    def add_message(self, role: str, content: str):
        self.history.append({"role": role, "content": content})
        self._truncate_memory()

    def _count_tokens_in_message(self, message: dict) -> int:
        # Đếm thô token của nội dung tin nhắn
        return len(self.encoding.encode(message["content"])) + 4

    def _truncate_memory(self):
        # Tính tổng số token hiện tại
        total_tokens = sum(self._count_tokens_in_message(msg) for msg in self.history)
        
        # Nếu vượt quá giới hạn, tiến hành loại bỏ các tin nhắn cũ nhất (nhưng giữ lại System Prompt ở vị trí index 0)
        while total_tokens > self.max_token_limit and len(self.history) > 2:
            removed_msg = self.history.pop(1) # Loại bỏ tin nhắn cũ ngay sau System prompt
            total_tokens -= self._count_tokens_in_message(removed_msg)
            print(f"[Memory Alert] Đã xóa tin nhắn cũ để giải phóng ngữ cảnh. Token hiện tại: {total_tokens}")

    def get_messages_for_api(self):
        return self.history

if __name__ == "__main__":
    manager = ChatMemoryManager(max_token_limit=100) # Giới hạn cực thấp để test truncation
    manager.add_message("system", "Bạn là một trợ lý ảo.")
    manager.add_message("user", "Xin chào, tôi là Huy, tôi làm về AI Automation.")
    manager.add_message("assistant", "Chào Huy! Rất vui được hỗ trợ bạn.")
    manager.add_message("user", "Hãy kể cho tôi nghe một câu chuyện dài về công nghệ tương lai và cách nó thay đổi thế giới của chúng ta.")
    
    print("\nLịch sử gửi API cuối cùng:")
    for msg in manager.get_messages_for_api():
        print(f"{msg['role'].upper()}: {msg['content'][:50]}...")
```

---

## 3. Mini Project

### Bài tập 1: Tóm tắt bài báo dài bằng kỹ thuật phân đoạn (Mức độ: Trung bình)
* **Đề bài**: Viết một script Python nhận một tệp văn bản dài vượt quá giới hạn ngữ cảnh test (giả định là 4,000 tokens). Tiến hành chia nhỏ văn bản thành 2 đoạn, gửi đi tóm tắt từng đoạn rồi ghép lại thành một bản tóm tắt tổng thể hoàn chỉnh.
* **Mã nguồn mẫu (`chunk_summarizer.py`)**:
```python
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

long_text = "Văn bản mẫu dài..." * 500  # Giả lập văn bản dài

def summarize_chunks(text: str, chunk_size: int = 3000) -> str:
    # 1. Phân đoạn văn bản thô theo số ký tự
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    model = genai.GenerativeModel("gemini-2.5-flash")
    chunk_summaries = []
    
    # 2. Tóm tắt từng đoạn
    for idx, chunk in enumerate(chunks):
        print(f"Đang tóm tắt đoạn {idx+1}/{len(chunks)}...")
        res = model.generate_content(f"Tóm tắt đoạn văn sau ngắn gọn trong 1 câu: \n\n{chunk}")
        chunk_summaries.append(res.text.strip())
        
    # 3. Tổng hợp các bản tóm tắt
    combined_prompt = "Hãy tổng hợp các ý chính sau thành một bản tóm tắt hoàn chỉnh:\n\n" + "\n".join(chunk_summaries)
    final_res = model.generate_content(combined_prompt)
    return final_res.text

if __name__ == "__main__":
    summary = summarize_chunks(long_text)
    print("\nBản tóm tắt cuối cùng:")
    print(summary)
```

### Bài tập 2: Hệ thống hỏi đáp tài liệu dài tích hợp phân đoạn thông minh (Mức độ: Khó)
* **Đề bài**: Viết một script nhận một file tài liệu tài chính dài. Thay vì tóm tắt đơn thuần, hãy viết code phân đoạn tài liệu, sau đó sử dụng prompt yêu cầu AI trích xuất tất cả các số liệu về doanh thu xuất hiện trong từng phân đoạn. Cuối cùng, tổng hợp danh sách số liệu này thành một bảng JSON chuẩn.
* **Yêu cầu**: Bạn hãy tự hoàn thành không có code mẫu.
* **Gợi ý triển khai (Workflow Hints)**:
  1. Sử dụng vòng lặp phân đoạn văn bản và gọi prompt trích xuất số liệu: "Liệt kê các số liệu doanh thu trong đoạn dưới đây dưới dạng: Năm - Số tiền".
  2. Gộp tất cả các kết quả trích xuất trung gian thành một prompt tổng hợp cấu trúc JSON đầu ra sử dụng `response_mime_type="application/json"`.

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
Hãy tích hợp `ChatMemoryManager` phía trên vào script gọi API của bạn ở Chương 01 để tạo ra một ứng dụng chat CLI liên tục tương tác với AI nhưng không bao giờ lo bị tràn bộ nhớ API.

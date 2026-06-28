# Chương 02: Cơ chế Lập kế hoạch (Planning) & Trí nhớ của Agent

## 1. Deep Dive (Phân tích chuyên sâu)

### 1. Cơ chế Lập kế hoạch (Planning)
Khi nhận một nhiệm vụ phức tạp (như "Hãy viết báo cáo so sánh doanh thu của 3 đối thủ cạnh tranh"), Agent cần có khả năng tự lên kế hoạch hành động.
Các phương pháp phổ biến:
- **ReAct (Reason + Act)**: Agent liên tục lặp chu trình: Suy nghĩ -> Chọn công cụ -> Xem kết quả -> Suy nghĩ bước tiếp theo.
- **Plan-and-Solve**: Agent viết ra toàn bộ danh sách các bước cần làm trước (Ví dụ: Bước 1 tìm kiếm, Bước 2 tổng hợp, Bước 3 định dạng), sau đó thực hiện tuần tự từng bước và kiểm tra tiến độ.

### 2. Trí nhớ của Agent (Memory)
- **Short-term Memory (Trí nhớ ngắn hạn)**: Lịch sử cuộc hội thoại hiện tại. Giúp Agent nhớ người dùng vừa nói gì ở câu trước.
- **Long-term Memory (Trí nhớ dài hạn)**: Lưu trữ thông tin bền vững qua nhiều ngày, nhiều tháng. Ví dụ: sở thích của người dùng, tên công ty của họ. Thường được lưu trữ vào cơ sở dữ liệu quan hệ (PostgreSQL) hoặc Vector DB để Agent có thể truy xuất (Recall) khi người dùng quay lại sau một thời gian dài.

---

## 2. Demo: Xây dựng ReAct Agent đơn giản bằng Python thô

### Mục tiêu
Lập trình một cấu trúc ReAct loop thô sơ, cho phép Agent tự quyết định gọi công cụ tính toán toán học để trả lời câu hỏi của người dùng.

### Mã nguồn (`react_loop.py`)
```python
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Định nghĩa các công cụ tính toán thực tế phía Python
def get_stock_price(symbol: str) -> int:
    if symbol.upper() == "AAPL":
        return 180
    elif symbol.upper() == "MSFT":
        return 400
    return 0

def run_agent_loop(query: str):
    # Khai báo hướng dẫn ReAct cho LLM
    system_prompt = """Bạn là Agent hỗ trợ thông tin cổ phiếu.
Bạn có quyền sử dụng công cụ sau:
- get_stock_price(symbol): Trả về giá cổ phiếu hiện tại dưới dạng số nguyên USD.

Hãy suy nghĩ từng bước theo cấu trúc sau:
Thought: Suy nghĩ của bạn về những gì cần làm.
Action: Tên công cụ cần gọi (chỉ trả về dạng get_stock_price('MÃ'))
Observation: Kết quả nhận được từ công cụ (sẽ được điền sau).
... (Lặp lại Thought/Action nếu cần)
Final Answer: Câu trả lời cuối cùng cho người dùng.

Câu hỏi: {query}
"""
    
    prompt = system_prompt.format(query=query)
    
    # Bước 1: Gọi LLM lấy Thought và Action đầu tiên
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    
    llm_output = response.choices[0].message.content
    print("=== LẦN CHẠY 1 (AI SUY NGHĨ) ===")
    print(llm_output)
    
    # Parser thô sơ để mô phỏng gọi công cụ
    if "Action:" in llm_output:
        # Giả lập trích xuất tên mã cổ phiếu AAPL
        symbol = "AAPL"
        result = get_stock_price(symbol)
        print(f"\n[Hệ thống] Đang thực thi công cụ get_stock_price('{symbol}') -> Kết quả: {result} USD")
        
        # Bước 2: Gửi kết quả công cụ (Observation) ngược lại cho AI để lấy câu trả lời cuối cùng
        next_prompt = prompt + f"\n{llm_output}\nObservation: {result} USD\nThought:"
        
        response_final = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": next_prompt}],
            temperature=0
        )
        print("\n=== LẦN CHẠY 2 (AI RA KẾT LUẬN) ===")
        print(response_final.choices[0].message.content)

if __name__ == "__main__":
    run_agent_loop("Hãy kiểm tra giá cổ phiếu AAPL hiện tại.")
```

---

## 3. Mini Project

### Bài tập 1: Xây dựng Chatbot có bộ nhớ đệm lịch sử (Mức độ: Trung bình)
* **Đề bài**: Viết một script Python xây dựng một Chatbot ghi nhớ tối đa 3 lượt hội thoại gần nhất (Short-term Memory) để tránh làm quá tải context window của LLM khi trò chuyện dài.
* **Mã nguồn mẫu (`memory_chatbot.py`)**:
```python
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

class ChatWithMemory:
    def __init__(self, max_memory: int = 3):
        self.max_memory = max_memory
        self.history = []
        self.model = genai.GenerativeModel("gemini-2.5-flash")
        
    def chat(self, user_message: str) -> str:
        # 1. Ghép lịch sử hội thoại giới hạn vào prompt
        prompt = ""
        for turn in self.history[-self.max_memory:]:
            prompt += f"User: {turn['user']}\nAI: {turn['ai']}\n"
        prompt += f"User: {user_message}\nAI:"
        
        res = self.model.generate_content(prompt)
        ai_reply = res.text.strip()
        
        # 2. Lưu vào lịch sử bộ nhớ
        self.history.append({"user": user_message, "ai": ai_reply})
        return ai_reply

if __name__ == "__main__":
    bot = ChatWithMemory(max_memory=2)
    print("Bot:", bot.chat("Chào bạn, tôi tên là Huy."))
    print("Bot:", bot.chat("Tôi làm việc trong ngành AI Automation."))
    print("Bot:", bot.chat("Tên tôi là gì và tôi làm ngành gì?"))
```

### Bài tập 2: Thiết kế hệ thống bộ nhớ dài hạn lưu trữ SQLite (Mức độ: Khó)
* **Đề bài**: Nâng cấp Chatbot ở Bài tập 1 thành hệ thống có bộ nhớ dài hạn (Long-term Memory). Mỗi khi kết thúc phiên trò chuyện, AI tự động trích xuất các sự kiện quan trọng về người dùng (ví dụ: tên, sở thích, dự án) và lưu trữ trực tiếp vào cơ sở dữ liệu SQLite để nạp lại ở phiên chat tiếp theo.
* **Yêu cầu**: Học viên tự hoàn thành không có code mẫu.
* **Gợi ý triển khai (Workflow Hints)**:
  1. Tạo bảng `user_memories` trong SQLite gồm các trường: `key`, `value`.
  2. Viết prompt yêu cầu AI phân tích đoạn chat để trích xuất thông tin quan trọng dưới dạng cặp key-value.
  3. Tự động chèn/cập nhật thông tin vào DB và nạp lên làm System Instruction ở đầu phiên chat mới.


# Chương 03: Rào chắn an toàn (Guardrails) & Tự động Dự phòng lỗi (Fallbacks)

## 1. Deep Dive (Phân tích chuyên sâu)

### 1. Guardrails (Rào chắn kiểm duyệt)
Trong môi trường doanh nghiệp, AI Agent tuyệt đối không được sử dụng ngôn từ kích động, phân biệt đối xử, hoặc thảo luận các chủ đề cấm (ví dụ: tư vấn chính trị trong app ngân hàng).
- **Input Guardrails**: Kiểm quét câu hỏi của người dùng trước khi gửi cho LLM để chặn đứng các cuộc tấn công phá hoại (Prompt Injection, Jailbreaking).
- **Output Guardrails**: Kiểm quét câu trả lời do AI sinh ra trước khi hiển thị cho người dùng để đảm bảo thông tin chính xác, lịch sự, không vi phạm chính sách bảo mật nội bộ.

### 2. API Fallback (Dự phòng lỗi)
Khi API của OpenAI gặp sự cố mất kết nối toàn cầu (Downtime) hoặc dính lỗi Rate Limit (HTTP 429), ứng dụng của bạn sẽ bị tê liệt.
Thiết kế Production đòi hỏi cơ chế **Fallback**: tự động chuyển hướng request sang API dự phòng của nhà cung cấp khác (như Anthropic Claude hoặc Gemini) ngay lập tức để duy trì hoạt động liên tục của ứng dụng.

---

## 2. Demo: Triển khai Fallback Strategy Pattern trong Python

### Mục tiêu
Lập trình một hàm gọi API hỗ trợ tự động chuyển đổi từ mô hình chính (GPT-4o-mini của OpenAI) sang mô hình dự phòng (Gemini 1.5 Flash của Google) khi gặp lỗi kết nối.

### Mã nguồn (`fallback_client.py`)
```python
import os
from openai import OpenAI
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Khởi tạo 2 Client độc lập
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def call_llm_with_fallback(prompt: str) -> str:
    print("[Primary] Đang thử gọi OpenAI API (Mô hình chính)...")
    try:
        # Giả lập lỗi bằng cách kiểm tra nếu prompt chứa từ khóa 'simulate_fail'
        # Trong thực tế, lỗi sẽ là các ngoại lệ mất mạng, API timeout...
        if "simulate_fail" in prompt:
            raise Exception("Lỗi kết nối API OpenAI (HTTP 502 Bad Gateway)")
            
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            timeout=5 # Giới hạn thời gian chờ tối đa 5s để chuyển fallback nhanh
        )
        return f"[OpenAI] {response.choices[0].message.content}"
        
    except Exception as e:
        print(f"-> Lỗi phát hiện ở mô hình chính: {e}")
        print("[Fallback] Đang tự động chuyển hướng sang Gemini API (Dự phòng nóng)...")
        
        try:
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(prompt)
            return f"[Gemini] {response.text}"
        except Exception as e_fallback:
            return f"Lỗi nghiêm trọng: Cả hệ thống chính và dự phòng đều thất bại! Chi tiết: {str(e_fallback)}"

if __name__ == "__main__":
    # Lượt chạy 1: Bình thường
    print(call_llm_with_fallback("Hãy viết slogan ngắn cho AI Agent."))
    
    print("\n" + "="*40 + "\n")
    
    # Lượt chạy 2: Giả lập sự cố sập API chính
    print(call_llm_with_fallback("simulate_fail: Hãy viết slogan ngắn cho AI Agent."))
```

---

## 3. Mini Project
Hãy viết một kịch bản Output Guardrail bằng Python. Hàm nhận đầu vào là câu trả lời của AI. Sử dụng biểu thức chính quy (Regex) hoặc một cuộc gọi AI nhỏ thứ hai để kiểm quét xem câu trả lời có vô tình tiết lộ mã API Key nào không (như chuỗi bắt đầu bằng `sk-proj-`). Nếu phát hiện rò rỉ, chặn đứng không gửi về client và ghi log ERROR khẩn cấp.

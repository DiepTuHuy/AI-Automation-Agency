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

### Bài tập 1: Cơ chế xử lý dự phòng (Fallback) sang mô hình nhỏ hơn khi lỗi (Mức độ: Trung bình)
* **Đề bài**: Viết một script gọi mô hình cao cấp (ví dụ: `gemini-2.5-pro`). Nếu xảy ra lỗi kết nối hoặc hết hạn quota (HTTP 429/500), tự động bắt lỗi và chuyển hướng cuộc gọi (Fallback) sang mô hình miễn phí/nhỏ hơn (`gemini-2.5-flash`) để đảm bảo hệ thống không bị gián đoạn.
* **Mã nguồn mẫu (`api_fallback.py`)**:
```python
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

def ask_with_fallback(prompt: str) -> str:
    # Thử gọi model Pro trước
    try:
        print("Đang thử kết nối mô hình Gemini 2.5 Pro...")
        # Giả lập model sai tên để kích hoạt ngoại lệ tự động phục vụ test
        model = genai.GenerativeModel("gemini-2.5-pro-wrong-name-test")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Lỗi xảy ra với model Pro: {e}")
        print("-> Tự động kích hoạt cơ chế dự phòng: Chuyển sang Gemini 2.5 Flash...")
        try:
            model_flash = genai.GenerativeModel("gemini-2.5-flash")
            response = model_flash.generate_content(prompt)
            return response.text
        except Exception as flash_err:
            return f"Cả hai mô hình đều thất bại: {flash_err}"

if __name__ == "__main__":
    result = ask_with_fallback("Viết slogan cho dịch vụ sửa xe lưu động")
    print(f"\nKết quả cuối cùng: {result}")
```

### Bài tập 2: Bộ lọc từ ngữ nhạy cảm (Content Guardrails) (Mức độ: Khó)
* **Đề bài**: Viết một script Python làm nhiệm vụ kiểm duyệt nội dung đầu vào. Trước khi gửi câu hỏi lên LLM, script sẽ quét các từ cấm trong file [blacklist.txt](../../resources/blacklist.txt) (Tải tệp tin mẫu về máy). Nếu phát hiện từ cấm, lập tức chặn cuộc gọi và báo lỗi. Sau khi nhận kết quả từ LLM, tiếp tục quét xem nội dung đầu ra có vi phạm chính sách an toàn không trước khi trả về cho khách hàng.
* **Yêu cầu**: Bạn hãy tự hoàn thành không có code mẫu.
* **Gợi ý triển khai (Workflow Hints)**:
  1. Tạo danh sách các từ cấm (Blacklist) đọc từ file [blacklist.txt](../../resources/blacklist.txt).
  2. Viết hàm kiểm tra đầu vào trước khi thực thi gọi API.
  3. Cấu hình tham số "safety_settings" của Gemini API để tăng cường bộ lọc phía máy chủ.

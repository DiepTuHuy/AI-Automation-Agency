# Chương 03: Gọi hàm tự động (Function Calling) bằng API OpenAI

## 1. Deep Dive (Phân tích chuyên sâu)

### Bản chất của Function Calling
Một quan niệm sai lầm phổ biến là LLM tự chạy hàm Python của bạn. Thực chất:
1. Bạn khai báo cho LLM danh sách các hàm của bạn kèm theo mô tả chi tiết (Tên hàm, chức năng, các tham số đầu vào và kiểu dữ liệu).
2. Bạn gửi câu hỏi của người dùng kèm theo danh sách hàm này cho LLM.
3. LLM đọc câu hỏi, tự phân tích xem có cần dùng hàm nào không.
   - Nếu cần: LLM **trả về một yêu cầu gọi hàm dưới dạng đối tượng JSON** chứa tên hàm và giá trị cụ thể của các tham số (ví dụ: `{"name": "get_weather", "arguments": {"location": "Hà Nội"}}`).
   - Nếu không cần: LLM trả về text thông thường.
4. Code Python của bạn nhận JSON này, thực thi hàm thực tế trên máy chủ của bạn để lấy kết quả (ví dụ gọi DB hoặc API).
5. Bạn gửi kết quả của hàm ngược lại cho LLM để mô hình tổng hợp thành câu trả lời tự nhiên cho người dùng.

---

## 2. Demo: Lập trình tích hợp Tool hoàn chỉnh

### Mục tiêu
Xây dựng một hệ thống Python hoàn chỉnh khai báo và thực thi một công cụ tính thuế thu nhập cá nhân tự động do LLM kích hoạt.

### Mã nguồn (`tool_calling.py`)
```python
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# 1. Định nghĩa hàm Python thực tế sẽ chạy trên server
# Lưu ý: Cần viết rõ docstring và kiểu dữ liệu tham số để Gemini tự động trích xuất schema
def calculate_income_tax(income: float) -> float:
    """Tính toán tiền thuế thu nhập cá nhân phải nộp dựa trên tổng thu nhập hàng năm.
    
    Args:
        income: Tổng thu nhập hàng năm quy đổi ra đơn vị USD.
    """
    print(f"[Tool Execution] Đang tính thuế cho thu nhập: {income} USD...")
    return income * 0.10

if __name__ == "__main__":
    # 2. Khởi tạo mô hình và truyền trực tiếp hàm Python vào tham số tools
    model = genai.GenerativeModel(
        "gemini-2.5-flash",
        tools=[calculate_income_tax],
        system_instruction="Bạn là trợ lý tài chính chuyên nghiệp. Hãy luôn tra cứu thông tin bằng công cụ trước khi đưa ra câu trả lời."
    )

    # 3. Sử dụng chat với tính năng gọi hàm tự động (Automatic Function Calling) của Gemini
    chat = model.start_chat(enable_automatic_function_calling=True)
    
    query = "Tôi kiếm được 50,000 USD năm nay, tôi phải nộp bao nhiêu tiền thuế?"
    print(f"Câu hỏi: {query}\n")
    
    response = chat.send_message(query)
    
    print("\nAI phản hồi cuối cùng:")
    print(response.text)
```

---

## 3. Mini Project
Hãy bổ sung thêm một công cụ thứ hai mang tên `send_email_notification(email_address, subject, content)` (chỉ cần in ra màn hình terminal để giả lập việc gửi). Sửa đổi script trên để khi người dùng hỏi: "Hãy tính thuế cho thu nhập 80k USD của tôi và gửi kết quả về email huy@example.com", AI sẽ tự động kích hoạt tuần tự cả hai công cụ.

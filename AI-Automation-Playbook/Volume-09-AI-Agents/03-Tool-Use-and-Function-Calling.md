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

### Bài tập 1: Tích hợp công cụ tra cứu thời tiết bằng Function Calling (Mức độ: Trung bình)
* **Đề bài**: Viết một script Python định nghĩa một tool đơn giản lấy thông tin thời tiết (`get_weather`) theo địa điểm và tích hợp nó vào Gemini Agent bằng cơ chế Function Calling tự động.
* **Mã nguồn mẫu (`weather_agent.py`)**:
```python
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# 1. Định nghĩa hàm Python làm công cụ cho AI
def get_weather(city: str) -> str:
    """Tra cứu thời tiết hiện tại của một thành phố cụ thể.
    
    Args:
        city: Tên thành phố cần tra cứu (ví dụ: 'Hanoi', 'Saigon').
    """
    city_lower = city.lower()
    if "hanoi" in city_lower or "hà nội" in city_lower:
        return "Nhiệt độ 28°C, trời nhiều mây, có mưa rào nhẹ."
    elif "saigon" in city_lower or "hồ chí minh" in city_lower:
        return "Nhiệt độ 33°C, trời nắng nóng, độ ẩm cao."
    else:
        return "Không có dữ liệu thời tiết tại khu vực này."

if __name__ == "__main__":
    # 2. Đăng ký hàm làm công cụ thông qua tham số tools
    # Bật enable_automatic_function_calling=True để SDK tự động gọi hàm khi model yêu cầu
    model = genai.GenerativeModel(
        "gemini-2.5-flash",
        tools=[get_weather]
    )
    
    chat = model.start_chat(enable_automatic_function_calling=True)
    
    query = "Thời tiết ở Hà Nội hôm nay thế nào em?"
    print(f"Câu hỏi: {query}")
    res = chat.send_message(query)
    
    print("\nKết quả gọi tool và trả lời của AI:")
    print(res.text)
```

### Bài tập 2: Trợ lý giao dịch ví cá nhân an toàn (Mức độ: Khó)
* **Đề bài**: Định nghĩa 2 công cụ Python mô phỏng: `get_wallet_balance(user_id: str) -> float` và `send_money(user_id: str, recipient: str, amount: float) -> str`. Xây dựng một Gemini Agent hỗ trợ chuyển tiền. Yêu cầu AI trước khi chuyển tiền bắt buộc phải gọi tool `get_wallet_balance` kiểm tra số dư. Nếu số dư đủ mới thực hiện chuyển tiền qua `send_money`, ngược lại báo lỗi từ chối giao dịch.
* **Yêu cầu**: Học viên tự hoàn thành không có code mẫu.
* **Gợi ý triển khai (Workflow Hints)**:
  1. Định nghĩa rõ docstring cho 2 hàm để Gemini hiểu tham số đầu vào.
  2. Bật tính năng gọi hàm tự động trong cuộc hội thoại chat của Gemini SDK.
  3. Thử nghiệm kịch bản: chuyển số tiền nhỏ (thành công) và chuyển số tiền lớn hơn số dư (AI báo lỗi không đủ tiền mà không thực hiện chuyển khoản).
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
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 1. Định nghĩa hàm Python thực tế sẽ chạy trên server
def calculate_income_tax(income: float) -> float:
    # Công thức tính thuế giả lập đơn giản: 10% tổng thu nhập
    return income * 0.10

if __name__ == "__main__":
    # 2. Khai báo mô tả công cụ cho OpenAI API dưới dạng JSON Schema
    tools = [
        {
            "type": "function",
            "function": {
                "name": "calculate_income_tax",
                "description": "Tính toán tiền thuế thu nhập cá nhân phải nộp dựa trên tổng thu nhập hàng năm.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "income": {
                            "type": "number",
                            "description": "Tổng thu nhập hàng năm quy đổi ra đơn vị USD."
                        }
                    },
                    "required": ["income"]
                }
            }
        }
    ]

    messages = [{"role": "user", "content": "Tôi kiếm được 50,000 USD năm nay, tôi phải nộp bao nhiêu tiền thuế?"}]

    # 3. Gửi yêu cầu kèm danh sách Tools
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=tools,
        tool_choice="auto" # Cho phép AI tự quyết định có gọi hay không
    )

    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls

    # 4. Kiểm tra xem AI có yêu cầu gọi hàm không
    if tool_calls:
        print("AI yêu cầu gọi công cụ:")
        for tool_call in tool_calls:
            print(f"- Hàm: {tool_call.function.name}")
            print(f"- Tham số: {tool_call.function.arguments}")
            
            # Thực thi hàm Python tương ứng
            if tool_call.function.name == "calculate_income_tax":
                arguments = json.loads(tool_call.function.arguments)
                tax_result = calculate_income_tax(arguments["income"])
                
                # 5. Gửi kết quả ngược lại cho AI để sinh câu trả lời tự nhiên
                messages.append(response_message) # Thêm tin nhắn yêu cầu của AI vào luồng
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": "calculate_income_tax",
                    "content": str(tax_result)
                })
                
                final_response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages
                )
                print("\nAI phản hồi cuối cùng:")
                print(final_response.choices[0].message.content)
```

---

## 3. Mini Project
Hãy bổ sung thêm một công cụ thứ hai mang tên `send_email_notification(email_address, subject, content)` (chỉ cần in ra màn hình terminal để giả lập việc gửi). Sửa đổi script trên để khi người dùng hỏi: "Hãy tính thuế cho thu nhập 80k USD của tôi và gửi kết quả về email huy@example.com", AI sẽ tự động kích hoạt tuần tự cả hai công cụ.

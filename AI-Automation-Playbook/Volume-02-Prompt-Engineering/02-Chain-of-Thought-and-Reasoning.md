# Chương 02: Kích hoạt khả năng suy luận bằng Chain-of-Thought (CoT)

## 1. Deep Dive (Phân tích chuyên sâu)

### Chain-of-Thought (Chuỗi suy luận) là gì?
Nếu bạn giao cho một đứa trẻ một bài toán đố phức tạp và bắt chúng đưa ra đáp án ngay lập tức trong 1 giây, chúng có xu hướng đoán bừa và sai. LLM cũng vậy. 
Khi bạn yêu cầu LLM đưa ra kết quả ngay lập tức, mô hình bị giới hạn số lượng token tính toán trung gian. 

**Chain-of-Thought (CoT)** hoạt động bằng cách hướng dẫn mô hình phân tích bài toán thành các bước logic tuần tự trước khi đưa ra kết quả cuối cùng. Kỹ thuật này giúp:
- Tăng khả năng giải quyết các bài toán toán học, logic, lập trình và đưa ra quyết định nghiệp vụ phức tạp.
- Giảm thiểu đáng kể hiện tượng ảo tưởng (hallucination) vì mô hình có thời gian để tự kiểm tra tính logic của các bước trước đó.

### Kỹ thuật Zero-Shot CoT
Chỉ đơn giản bằng cách thêm cụm từ thần chú: **"Hãy suy nghĩ từng bước một" (Let's think step by step)** vào cuối prompt, bạn đã kích hoạt khả năng suy luận logic của mô hình một cách tự động mà không cần viết ví dụ dài dòng.

---

## 2. Demo: Giải bài toán phân bổ nguồn lực nhân sự phức tạp

### Mục tiêu
Giải quyết bài toán chia dự án cho các lập trình viên dựa trên thời gian rảnh và kỹ năng của họ, so sánh kết quả khi có và không có CoT.

### Mã nguồn (`cot_demo.py`)
```python
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

puzzle = """Công ty có 3 dự án: Dự án A (yêu cầu Python), Dự án B (yêu cầu JavaScript), Dự án C (yêu cầu Go).
Có 3 lập trình viên: Huy (biết Python, JS, có 10h rảnh/tuần), Nam (biết JS, Go, có 20h rảnh/tuần), An (biết Python, Go, có 5h rảnh/tuần).
Dự án A cần tối thiểu 12h Python. Dự án B cần tối thiểu 15h JS. Dự án C cần 5h Go.
Lập kế hoạch phân bổ nhân sự tối ưu nhất để hoàn thành tối đa số lượng dự án."""

def solve_without_cot(text: str) -> str:
    model = genai.GenerativeModel(
        "gemini-2.5-flash",
        system_instruction="Bạn là chuyên gia quản lý dự án. Hãy trả lời đáp án trực tiếp, ngắn gọn nhất."
    )
    response = model.generate_content(
        text,
        generation_config={"temperature": 0.0}
    )
    return response.text

def solve_with_cot(text: str) -> str:
    model = genai.GenerativeModel(
        "gemini-2.5-flash",
        system_instruction="Bạn là chuyên gia quản lý dự án. Hãy phân tích từng bước chi tiết trước khi đưa ra kết luận phân bổ."
    )
    response = model.generate_content(
        f"{text}\n\nHãy phân tích từng bước chi tiết.",
        generation_config={"temperature": 0.0}
    )
    return response.text

if __name__ == "__main__":
    print("=== GIẢI KHÔNG CÓ COT (TRẢ LỜI NGAY) ===")
    print(solve_without_cot(puzzle))
    print("\n" + "="*40 + "\n")
    print("=== GIẢI CÓ COT (SUY LUẬN TỪNG BƯỚC) ===")
    print(solve_with_cot(puzzle))
```

---

## 3. Mini Project

### Bài tập 1: Tính toán tiền phạt nợ gốc ngân hàng có giải trình (CoT) (Mức độ: Trung bình)
* **Đề bài**: Viết một script Python giải quyết bài toán tính tổng tiền phạt chậm nợ gốc của ngân hàng với công thức lũy tiến. Yêu cầu mô hình phải giải thích rõ ràng cách tính của từng tháng (CoT) trước khi hiển thị con số tổng tiền phạt cuối cùng.
* **Mã nguồn mẫu (`cot_calculator.py`)**:
```python
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

def calculate_debt_penalty(principal: float, delay_months: int) -> str:
    # prompt hướng dẫn chuỗi suy luận CoT để giải toán tài chính phức tạp
    prompt = f"""Bạn là trợ lý ảo kiểm toán ngân hàng. Hãy tính toán tiền phạt chậm trả nợ gốc lũy tiến theo quy tắc sau:
- Tháng thứ 1: phạt 2% trên nợ gốc.
- Tháng thứ 2: phạt 5% trên nợ gốc.
- Từ tháng thứ 3 trở đi: phạt 10% trên nợ gốc mỗi tháng.

Nợ gốc ban đầu: {principal} USD.
Số tháng trễ hạn: {delay_months} tháng.

Yêu cầu:
1. Hãy suy nghĩ và giải thích chi tiết cách tính tiền phạt của từng tháng.
2. In ra tổng số tiền phạt cuối cùng sau cùng.
"""
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(
        prompt,
        generation_config={"temperature": 0.0}
    )
    return response.text

if __name__ == "__main__":
    principal_amount = 10000.0  # 10k USD nợ gốc
    months = 4  # Trễ 4 tháng
    
    print("Đang tính toán tiền phạt...")
    result_log = calculate_debt_penalty(principal_amount, months)
    print("\nKết quả tính toán chi tiết từ AI:")
    print(result_log)
```

### Bài tập 2: Lập lịch phân công công việc thông minh (CoT) (Mức độ: Khó)
* **Đề bài**: Viết một script Python giải quyết bài toán phân chia công việc cho một dự án phát triển phần mềm gồm 3 dự án nhỏ cho 4 lập trình viên dựa trên thời gian rảnh và kỹ năng chuyên môn của họ. Yêu cầu mô hình bắt buộc phải phân tích khả năng của từng người và thời hạn (CoT) trước khi đưa ra kết quả phân bổ cuối cùng để tránh bị quá tải nhân lực.
* **Yêu cầu**: Bạn hãy tự hoàn thành không có code mẫu.
* **Gợi ý triển khai (Workflow Hints)**:
  1. Thiết lập bài toán với thông tin chi tiết của 4 lập trình viên (Kỹ năng, số giờ rảnh) và 3 dự án (Thời gian hoàn thành cần thiết, công nghệ sử dụng).
  2. Prompt yêu cầu mô hình phân tích: Bước 1 (Liệt kê tổng cung giờ rảnh theo ngôn ngữ), Bước 2 (Phân phối dự án ưu tiên cao nhất), Bước 3 (Kiểm tra xem có ai bị quá tải không).
  3. Cấu hình `temperature = 0.0` để có kết quả phân chia ổn định và đúng logic nhất.
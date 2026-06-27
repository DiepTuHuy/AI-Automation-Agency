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
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

puzzle = """Công ty có 3 dự án: Dự án A (yêu cầu Python), Dự án B (yêu cầu JavaScript), Dự án C (yêu cầu Go).
Có 3 lập trình viên: Huy (biết Python, JS, có 10h rảnh/tuần), Nam (biết JS, Go, có 20h rảnh/tuần), An (biết Python, Go, có 5h rảnh/tuần).
Dự án A cần tối thiểu 12h Python. Dự án B cần tối thiểu 15h JS. Dự án C cần 5h Go.
Lập kế hoạch phân bổ nhân sự tối ưu nhất để hoàn thành tối đa số lượng dự án."""

def solve_without_cot(text: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Bạn là chuyên gia quản lý dự án. Hãy trả lời đáp án trực tiếp, ngắn gọn nhất."},
            {"role": "user", "content": text}
        ],
        temperature=0
    )
    return response.choices[0].message.content

def solve_with_cot(text: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Bạn là chuyên gia quản lý dự án. Hãy phân tích từng bước chi tiết trước khi đưa ra kết luận phân bổ."},
            {"role": "user", "content": f"{text}\n\nãy phân tích từng bước chi tiết."}
        ],
        temperature=0
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    print("=== GIẢI KHÔNG CÓ COT (TRẢ LỜI NGAY) ===")
    print(solve_without_cot(puzzle))
    print("\n" + "="*40 + "\n")
    print("=== GIẢI CÓ COT (SUY LUẬN TỪNG BƯỚC) ===")
    print(solve_with_cot(puzzle))
```

---

## 3. Mini Project
Hãy viết một script Python giải quyết bài toán tính tổng tiền phạt chậm nợ gốc của ngân hàng với công thức lũy tiến. Yêu cầu mô hình phải giải thích rõ ràng cách tính của từng tháng (CoT) trước khi hiển thị con số tổng tiền phạt cuối cùng.

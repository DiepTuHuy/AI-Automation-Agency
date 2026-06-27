# Chương 04: Làm chủ Tham số Mô hình (Temperature & Top-P)

## 1. Deep Dive (Phân tích chuyên sâu)

Khi gọi API của các LLM, ngoài câu lệnh prompt, bạn có thể điều chỉnh cách mô hình lựa chọn từ ngữ đầu ra qua các tham số điều hướng xác suất:

### Temperature (Nhiệt độ)
Kiểm soát mức độ ngẫu nhiên của các token được sinh ra.
- **Temperature = 0 (Deterministic)**: Mô hình luôn chọn từ có xác suất cao nhất. Kết quả trả về giống hệt nhau giữa các lần chạy. *Khi nào dùng*: Trích xuất dữ liệu, viết code, sinh JSON, phân tích logic chính xác.
- **Temperature = 0.7 - 1.0 (Creative)**: Mô hình chọn cả các từ có xác suất thấp hơn, tạo ra sự sáng tạo, đa dạng. *Khi nào dùng*: Viết blog, lên ý tưởng kịch bản quảng cáo, brainstorming.

### Top-p (Nucleus Sampling)
Một cách tiếp cận khác để kiểm soát độ sáng tạo thông qua việc giới hạn tập hợp các từ được chọn dựa trên tích lũy xác suất.
- *Ví dụ*: `top_p = 0.1` nghĩa là mô hình chỉ được lựa chọn từ trong nhóm 10% các từ có xác suất xuất hiện cao nhất.
- **Khuyến nghị**: Không điều chỉnh đồng thời cả `temperature` và `top_p` trong cùng một lượt gọi vì chúng sẽ triệt tiêu và làm méo mó phân phối xác suất của nhau. Hãy giữ một trong hai tham số ở giá trị mặc định.

### Frequency Penalty & Presence Penalty
- **Frequency Penalty**: Phạt các từ dựa trên tần suất xuất hiện của chúng trong đoạn văn đã tạo (giúp giảm thiểu lỗi lặp lại cùng một từ quá nhiều lần).
- **Presence Penalty**: Phạt các từ dựa trên sự xuất hiện của chúng (khuyến khích mô hình chuyển sang các chủ đề/từ vựng mới).

---

## 2. Demo: So sánh tác động của Temperature trong sinh dữ liệu mẫu

### Mục tiêu
Chạy một câu hỏi với các mức cấu hình `temperature` khác nhau (0.0, 0.7, 1.5) để phân tích trực quan sự khác biệt của kết quả trả về.

### Mã nguồn (`temp_comparison.py`)
```python
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_slogan(temp: float) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": "Viết 1 câu slogan ngắn gọn cho thương hiệu cà phê thông minh tự pha bằng robot."}
        ],
        temperature=temp
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    print("--- Thử nghiệm Temperature = 0.0 (Tính nhất quán cao) ---")
    for i in range(3):
        print(f"Lượt {i+1}: {generate_slogan(0.0)}")
        
    print("\n--- Thử nghiệm Temperature = 0.8 (Sáng tạo vừa phải) ---")
    for i in range(3):
        print(f"Lượt {i+1}: {generate_slogan(0.8)}")

    print("\n--- Thử nghiệm Temperature = 1.5 (Cực kỳ hỗn loạn) ---")
    for i in range(3):
        try:
            print(f"Lượt {i+1}: {generate_slogan(1.5)}")
        except Exception as e:
            print(f"Lỗi: {e} (Mức độ ngẫu nhiên quá cao có thể gây lỗi sinh token không hợp lệ)")
```

---

## 3. Mini Project
Hãy viết một script Python tự động thực thi các tác vụ: nhận một email phản hồi của khách hàng rác, tiến hành phân loại cảm xúc (Tích cực/Tiêu cực/Trung lập) bằng cách cấu hình tham số thích hợp nhất để đảm bảo kết quả trả về luôn ổn định và không đổi định dạng.

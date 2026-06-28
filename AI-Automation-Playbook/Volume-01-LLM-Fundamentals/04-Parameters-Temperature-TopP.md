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
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

def generate_slogan(temp: float) -> str:
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(
        "Viết 1 câu slogan ngắn gọn cho thương hiệu cà phê thông minh tự pha bằng robot.",
        generation_config={
            "temperature": temp
        }
    )
    return response.text

if __name__ == "__main__":
    print("--- Thử nghiệm Temperature = 0.0 (Tính nhất quán cao) ---")
    for i in range(3):
        print(f"Lượt {i+1}: {generate_slogan(0.0)}")
        
    print("\n--- Thử nghiệm Temperature = 0.8 (Sáng tạo vừa phải) ---")
    for i in range(3):
        print(f"Lượt {i+1}: {generate_slogan(0.8)}")

    print("\n--- Thử nghiệm Temperature = 1.8 (Cực kỳ hỗn loạn) ---")
    for i in range(3):
        try:
            print(f"Lượt {i+1}: {generate_slogan(1.8)}")
        except Exception as e:
            print(f"Lỗi: {e} (Mức độ ngẫu nhiên quá cao có thể gây lỗi sinh token không hợp lệ)")
```

---

## 3. Mini Project

### Bài tập 1: Phân loại cảm xúc email khách hàng (Mức độ: Trung bình)
* **Đề bài**: Viết một script Python nhận phản hồi của khách hàng, tiến hành phân loại cảm xúc (Tích cực/Tiêu cực/Trung lập). Sử dụng cấu hình tham số thích hợp để kết quả trả về luôn ổn định, nhất quán qua các lượt chạy.
* **Mã nguồn mẫu (`classify_email.py`)**:
```python
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

def classify_feedback(text: str) -> str:
    # Sử dụng temperature = 0.0 để kết quả luôn chính xác và không thay đổi
    model = genai.GenerativeModel("gemini-2.5-flash")
    prompt = f"Phân loại cảm xúc của phản hồi sau vào 1 trong các nhóm [Tích cực], [Tiêu cực], [Trung lập]. Chỉ trả về tên nhóm.\n\nPhản hồi: {text}"
    
    response = model.generate_content(
        prompt,
        generation_config={
            "temperature": 0.0
        }
    )
    return response.text.strip()

if __name__ == "__main__":
    email_sample = "Sản phẩm đóng gói cẩn thận nhưng giao hàng hơi chậm, nhân viên nhiệt tình."
    result = classify_feedback(email_sample)
    print(f"Phản hồi: {email_sample}")
    print(f"Phân loại cảm xúc: {result}")
```

### Bài tập 2: Sinh biến thể quảng cáo sáng tạo (Mức độ: Khó)
* **Đề bài**: Viết một script Python tự động tạo ra 3 biến thể slogan quảng cáo cho sản phẩm "Giày chạy bộ thông minh". Để đảm bảo các slogan có tính sáng tạo cao và không bị lặp lại, hãy cấu hình tham số `temperature` và `top_p` phù hợp.
* **Yêu cầu**: Học viên tự hoàn thành không có code mẫu.
* **Gợi ý triển khai (Workflow Hints)**:
  1. Sử dụng `temperature = 1.0` (hoặc cao hơn) để khuyến khích mô hình tư duy sáng tạo từ vựng mới.
  2. Cấu hình `top_p = 0.9` (Nucleus Sampling) để giới hạn mô hình chỉ chọn các từ trong nhóm 90% từ có độ phổ biến cao, tránh sinh ra các từ vô nghĩa.
  3. Sử dụng vòng lặp trong Python hoặc viết prompt yêu cầu mô hình sinh 3 slogan độc lập trong một lượt gọi.

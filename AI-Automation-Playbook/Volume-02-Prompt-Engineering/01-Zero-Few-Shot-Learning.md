# Chương 01: Kỹ thuật Zero-Shot & Few-Shot Prompting

## 1. Deep Dive (Phân tích chuyên sâu)

### Zero-Shot Prompting
Zero-shot là kỹ thuật gửi trực tiếp tác vụ cho LLM mà không cung cấp bất kỳ ví dụ minh họa nào. Mô hình dựa hoàn toàn vào kiến thức đã học trong giai đoạn pre-training để xử lý yêu cầu.
* Khi nào dùng:
  - Các tác vụ phổ biến, đơn giản (ví dụ: dịch thuật cơ bản, tóm tắt văn bản ngắn, phân loại cảm xúc tích cực/tiêu cực rõ ràng).
  - Khi cần tốc độ phản hồi nhanh và tiết kiệm tối đa token đầu vào.
* Khi nào không dùng:
  - Khi cần định dạng đầu ra phức tạp hoặc không theo quy chuẩn thông thường.
  - Khi tác vụ mang tính chất ngách, chuyên sâu của doanh nghiệp.

### Few-Shot Prompting
Few-shot là kỹ thuật cung cấp một hoặc một vài ví dụ minh họa (in-context learning) trực tiếp trong prompt trước khi đưa ra câu hỏi thực tế.
* Tại sao Few-shot hoạt động mạnh mẽ:
  - Nó định hình rõ cấu trúc câu trả lời (ví dụ: độ dài, định dạng, phong cách ngôn ngữ).
  - Nó hướng dẫn mô hình cách xử lý các trường hợp biên (edge cases).
* Số lượng ví dụ tối ưu: Thường là từ **3 đến 5 ví dụ** là đủ. Vượt quá số lượng này sẽ làm loãng ngữ cảnh và gây lãng phí token mà không cải thiện hiệu suất đáng kể (quy luật hiệu suất giảm dần).

---

## 2. Demo: Phân loại ý kiến khách hàng bằng Zero-shot và Few-shot

### Mục tiêu
Phân loại các phản hồi phức tạp của khách hàng về sản phẩm công nghệ thành các danh mục chi tiết bằng cách so sánh hiệu quả giữa Zero-shot và Few-shot.

### Mã nguồn (`shot_comparison.py`)
```python
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Email khách hàng phức tạp cần phân loại
complex_feedback = "Sản phẩm dùng rất mượt khi mới mua, tuy nhiên sau khi cập nhật hệ điều hành mới thì máy rất nhanh nóng và sập nguồn liên tục. Tôi muốn đổi trả!"

def run_zero_shot(text: str) -> str:
    prompt = f"""Phân loại phản hồi sau vào 1 trong các nhóm: [Lỗi phần cứng], [Lỗi phần mềm], [Giao hàng], [Tư vấn bán hàng].
Phản hồi: "{text}"
Kết quả:"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return response.choices[0].message.content.strip()

def run_few_shot(text: str) -> str:
    prompt = f"""Bạn là bộ lọc phân loại phản hồi khách hàng chuyên nghiệp. Hãy phân loại chính xác dựa trên các ví dụ sau:

Ví dụ 1:
Phản hồi: "Màn hình điện thoại bị sọc xanh sau khi rơi nhẹ, camera không bật lên được."
Phân tích: Hỏng hóc vật lý và linh kiện phần cứng.
Kết quả: [Lỗi phần cứng]

Ví dụ 2:
Phản hồi: "Ứng dụng liên tục báo lỗi kết nối mạng mặc dù wifi vẫn hoạt động tốt."
Phân tích: Trục trặc liên quan đến code và ứng dụng phần mềm.
Kết quả: [Lỗi phần mềm]

Ví dụ 3:
Phản hồi: "Máy dùng tốt nhưng cập nhật lên bản mới thì bị nóng và sập nguồn, tôi cần bảo hành đổi trả."
Phân tích: Trục trặc phát sinh sau khi cập nhật phần mềm dẫn đến lỗi hệ thống và yêu cầu chính sách đổi trả.
Kết quả: [Lỗi phần mềm - Yêu cầu bảo hành]

Tác vụ thực tế cần phân loại:
Phản hồi: "{text}"
Phân tích:
Kết quả:"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )
    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    print("--- Chạy Zero-shot ---")
    print(run_zero_shot(complex_feedback))
    
    print("\n--- Chạy Few-shot ---")
    print(run_few_shot(complex_feedback))
```

---

## 3. Mini Project
Hãy viết một script Python sử dụng Few-shot để giải quyết tác vụ chuẩn hóa tên địa chỉ hành chính viết tay của Việt Nam (Ví dụ: "Hà lội" -> "Hà Nội", "Q1 Tp HCM" -> "Quận 1, Thành phố Hồ Chí Minh"). Hãy cung cấp ít nhất 3 cặp ví dụ chuẩn hóa trong prompt của bạn.

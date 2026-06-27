# Chương 01: Mô hình Ngôn ngữ Lớn (LLM) Hoạt động Thế nào?

## 1. Deep Dive (Phân tích chuyên sâu)

### Kiến trúc Transformer: Cuộc cách mạng AI
Hầu hết các LLM hiện đại (như GPT, Claude, Llama, Gemini) đều được xây dựng trên kiến trúc mạng neural mang tên **Transformer**, cụ thể là nhánh **Decoder-only** (Chỉ giải mã).

Khác với các kiến trúc cũ như RNN hay LSTM xử lý thông tin tuần tự từng từ một (gây chậm và mất trí nhớ khi câu dài), Transformer xử lý toàn bộ câu cùng một lúc thông qua cơ chế **Self-Attention (Tự chú ý)**. 

Cơ chế này cho phép mỗi từ trong câu "nhìn" vào tất cả các từ khác để hiểu ngữ cảnh:
*Ví dụ*: Trong câu *"Con sông này có dòng chảy rất mạnh vì nước lũ từ thượng nguồn đổ về"*, từ *"mạnh"* sẽ được liên kết rất chặt chẽ với *"dòng chảy"* và *"nước lũ"*.

### Vòng đời của một LLM
1. **Pre-training (Tiền huấn luyện)**: Mô hình được cho đọc hàng nghìn tỷ từ trên Internet. Nhiệm vụ duy nhất là: dự đoán từ tiếp theo. Giai đoạn này tiêu tốn hàng triệu USD tiền điện và phần cứng (GPU), tạo ra mô hình nền tảng (Base Model) có khả năng ngôn ngữ tốt nhưng chưa biết nghe lời (chỉ thích viết tiếp văn bản).
2. **Fine-tuning (Tinh chỉnh)**: Huấn luyện mô hình base trên các tập dữ liệu chọn lọc dạng hỏi-đáp (Instruction Dataset). Lúc này mô hình học cách trở thành một trợ lý hữu ích (Assistant).
3. **RLHF (Reinforcement Learning from Human Feedback)**: Huấn luyện nâng cao bằng phản hồi từ con người để căn chỉnh mô hình không tạo ra nội dung độc hại, thiên vị và luôn an toàn, lịch sự.

---

## 2. Demo: Gọi API LLM bằng Python

### Mục tiêu
Viết một script Python cơ bản, kết nối với API của OpenAI (hoặc Gemini) để gửi câu hỏi và nhận câu trả lời.

### Kiến trúc hoạt động
```
[app.py (Python)] ──(HTTP POST + Bearer Token)──> [OpenAI API Gateway] ──> [LLM Engine]
      ▲                                                                          │
      └──────────────────(JSON Response)─────────────────────────────────────────┘
```

### Source Tree
```
llm-demo/
├── .env
├── requirements.txt
└── app.py
```

### Mã nguồn (`app.py`)
Trước khi chạy, hãy cài thư viện: `pip install openai python-dotenv`

```python
import os
from openai import OpenAI
from dotenv import load_dotenv

# Tải biến môi trường từ file .env
load_dotenv()

# Khởi tạo client OpenAI sử dụng API Key từ biến môi trường
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_ai(prompt: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini", # Sử dụng mô hình rẻ và nhanh cho demo
            messages=[
                {"role": "system", "content": "Bạn là một kỹ sư AI thực chiến tối giản và thực tế."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        # Trích xuất nội dung câu trả lời từ cấu trúc JSON phản hồi
        return response.choices[0].message.content
    except Exception as e:
        return f"Đã xảy ra lỗi: {str(e)}"

if __name__ == "__main__":
    prompt = "Giải thích ngắn gọn cơ chế hoạt động của LLM cho người mới học lập trình."
    print("Đang gửi yêu cầu tới AI...")
    result = ask_ai(prompt)
    print("\nKết quả phản hồi:")
    print(result)
```

---

## 3. Mini Project
Hãy đăng ký một API key miễn phí từ Google AI Studio (Gemini API) hoặc sử dụng API Key của OpenAI, sau đó sửa đổi mã nguồn Demo trên để gọi mô hình Gemini 1.5 Flash và in ra kết quả. Viết nhận xét về sự khác biệt về tốc độ phản hồi.

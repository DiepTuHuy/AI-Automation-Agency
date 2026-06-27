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

## 2. Demo: Gọi API LLM bằng Python (Sử dụng Gemini)

### Mục tiêu
Viết một script Python cơ bản, kết nối với API của Google Gemini để gửi câu hỏi và nhận câu trả lời.

### Kiến trúc hoạt động
```
[app.py (Python)] ──(HTTP POST + API Key)──> [Google Gemini API Gateway] ──> [Gemini 2.5 Flash]
      ▲                                                                            │
      └─────────────────────(JSON Response / Text)─────────────────────────────────┘
```

### Source Tree
Cấu trúc cây thư mục của dự án thực hành demo:
```
llm-demo/
├── .env              # Lưu trữ API Key bảo mật
├── requirements.txt  # Khai báo các thư viện phụ thuộc
└── app.py            # Mã nguồn chính của ứng dụng
```

### Chi tiết tệp phụ thuộc & cấu hình
Để bài học chạy ổn định, hãy chuẩn bị các tệp cấu hình sau:

#### 📄 `requirements.txt`
```text
google-generativeai
python-dotenv
```

#### 📄 `.env`
```env
GEMINI_API_KEY=AIzaSy... # Điền API Key của bạn lấy từ Google AI Studio
```

### Mã nguồn chính (`app.py`)
Trước khi chạy, hãy tiến hành cài đặt các thư viện trong thư mục dự án demo: `pip install -r requirements.txt`

```python
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Tải biến môi trường từ file .env
load_dotenv()

# Lấy API Key từ file .env
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("LỖI: Không tìm thấy GEMINI_API_KEY trong file .env!")

# Cấu hình thư viện Gemini API
genai.configure(api_key=api_key)

def ask_ai(prompt: str) -> str:
    try:
        # Sử dụng mô hình gemini-2.5-flash nhanh và tối ưu chi phí
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.7  # Độ sáng tạo từ 0.0 đến 2.0 (0.7 là mức cân bằng tốt)
            }
        )
        # Trích xuất văn bản trả về trực tiếp từ phản hồi của mô hình
        return response.text
    except Exception as e:
        return f"Đã xảy ra lỗi kết nối Gemini API: {str(e)}"

if __name__ == "__main__":
    prompt = "Giải thích ngắn gọn cơ chế hoạt động của LLM cho người mới học lập trình."
    print("Đang gửi yêu cầu tới Gemini AI...")
    result = ask_ai(prompt)
    print("\nKết quả phản hồi từ Gemini:")
    print(result)
```

---

## 3. Mini Project
Hãy cài đặt thư mục `llm-demo` địa phương như hướng dẫn, điền API Key vào `.env`, chạy thử script `app.py`. Sau đó, thử thay đổi tham số `temperature` xuống `0.1` (kiểm tra tính nhất quán của câu trả lời) và lên `1.5` (kiểm tra tính sáng tạo). Ghi lại nhận xét của bạn vào tài liệu học tập cá nhân.


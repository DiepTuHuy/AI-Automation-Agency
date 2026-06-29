# Chương 02: Tokens & Tối ưu hóa chi phí API

## 1. Deep Dive (Phân tích chuyên sâu)

### Tokenizer hoạt động như thế nào?
LLM không đọc chữ cái, nó đọc **Tokens**. Thuật toán Tokenizer (thông dụng nhất là Byte-Pair Encoding - BPE) chia nhỏ từ ngữ thành các cụm ký tự phổ biến.
- *Quy tắc chung đối với tiếng Anh*: 1 token tương đương khoảng 4 ký tự hoặc 0.75 từ.
- *Bài toán tiếng Việt*: Tiếng Việt sử dụng các ký tự có dấu phức tạp (như: á, ớ, ề, ự). Nhiều tokenizer của các mô hình thế hệ cũ không được tối ưu cho tiếng Việt, dẫn đến việc một từ tiếng Việt có dấu bị phân tách thành 2-4 tokens (so với tiếng Anh chỉ là 1 token). điều này làm chi phí API tăng lên gấp nhiều lần và giảm tốc độ sinh chữ của mô hình.

### Công thức tính chi phí sử dụng API

Chi phí sử dụng mô hình ngôn ngữ lớn được tính toán dựa trên số lượng token thực tế tiêu thụ theo công thức sau:

$$\text{Chi phí (USD)} = \frac{\text{Số lượng Token}}{1.000.000} \times \text{Đơn giá mỗi triệu (M) tokens}$$

---

## 2. Demo: Đếm Token bằng thư viện `tiktoken`

### Mục tiêu
Đếm chính xác số lượng token của một văn bản tiếng Việt và tính toán chi phí trước khi gửi văn bản đó tới API của OpenAI.

### Mã nguồn (`token_counter.py`)
Cài đặt thư viện: `pip install tiktoken`

```python
import tiktoken

def calculate_tokens_and_cost(text: str, model_name: str = "gpt-4o") -> dict:
    # Lấy bộ mã hóa (encoding) phù hợp với mô hình được chọn
    try:
        encoding = tiktoken.encoding_for_model(model_name)
    except KeyError:
        # Fallback về bộ mã hóa cl100k_base của GPT-4
        encoding = tiktoken.get_encoding("cl100k_base")
        
    token_list = encoding.encode(text)
    num_tokens = len(token_list)
    
    # Định nghĩa giá cả (Ví dụ tại thời điểm hiện tại của GPT-4o)
    price_per_million_input = 5.00 # USD
    cost = (num_tokens / 1_000_000) * price_per_million_input
    
    return {
        "text": text,
        "tokens": num_tokens,
        "cost_usd": cost,
        "token_preview": [encoding.decode([token]) for token in token_list[:10]] # Preview 10 tokens đầu tiên
    }

if __name__ == "__main__":
    text_en = "Hello world! This is a simple test to count tokens in English language."
    text_vi = "Xin chào thế giới! Đây là một bài thử nghiệm đơn giản để đếm số token trong tiếng Việt."
    
    res_en = calculate_tokens_and_cost(text_en)
    res_vi = calculate_tokens_and_cost(text_vi)
    
    print(f"Bản English: {res_en['tokens']} tokens. Chi phí ước lượng: ${res_en['cost_usd']:.8f}")
    print(f"Bản Tiếng Việt: {res_vi['tokens']} tokens. Chi phí ước lượng: ${res_vi['cost_usd']:.8f}")
    print(f"Cụm token tiếng Việt phân tách: {res_vi['token_preview']}")
```

---

## 3. Mini Project

### Bài tập 1: Tính toán chi phí gọi API giả lập (Mức độ: Trung bình)
* **Đề bài**: Hãy viết một script Python ước tính số lượng token và chi phí sử dụng API của mô hình `gemini-2.5-flash` dựa trên bảng giá chuẩn cho một đoạn văn bản đầu vào dài 2,000 từ.
* **Mã nguồn mẫu (`token_cost_estimator.py`)**:
```python
def estimate_cost(word_count: int):
    # Quy đổi ước lượng: 1 từ tiếng Việt ~ 1.5 đến 2.0 tokens
    estimated_tokens = int(word_count * 1.8)
    
    # Bảng giá gemini-2.5-flash: $0.075 / 1 triệu input tokens
    input_price_per_million = 0.075
    estimated_cost_usd = (estimated_tokens / 1_000_000) * input_price_per_million
    
    print(f"Số từ đầu vào: {word_count} từ")
    print(f"Ước lượng số tokens: {estimated_tokens:,} tokens")
    print(f"Chi phí ước tính: ${estimated_cost_usd:.6f} USD")
    print(f"Quy đổi VND: {estimated_cost_usd * 25400:.2f} VND")

if __name__ == "__main__":
    estimate_cost(2000)
```

### Bài tập 2: Bộ đếm và tính toán chi phí token thời gian thực (Mức độ: Khó)
* **Đề bài**: Viết một script Python nhận văn bản đầu vào từ file [document.txt](../../resources/document.txt). Sử dụng thư viện gọi API Gemini để đếm chính xác số lượng token của tệp tin này bằng hàm `count_tokens()` của SDK, sau đó tự động tính toán chi phí gọi API thực tế của cả luồng Input và Output.
* **Yêu cầu**: Học viên tự hoàn thành không có code mẫu.
* **Gợi ý triển khai (Workflow Hints)**:
  1. Đọc nội dung file văn bản bằng `Path("document.txt").read_text()` (Tải tệp tin [document.txt](../../resources/document.txt) về máy để làm tài liệu đầu vào).
  2. Gọi `model.count_tokens(text)` để nhận số lượng token chính xác từ server Google.
  3. Áp dụng đơn giá thực tế của Gemini 2.5 Flash để in ra bảng chi phí chi tiết.

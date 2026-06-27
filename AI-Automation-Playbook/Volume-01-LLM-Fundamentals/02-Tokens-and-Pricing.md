# Chương 02: Tokens & Tối ưu hóa chi phí API

## 1. Deep Dive (Phân tích chuyên sâu)

### Tokenizer hoạt động như thế nào?
LLM không đọc chữ cái, nó đọc **Tokens**. Thuật toán Tokenizer (thông dụng nhất là Byte-Pair Encoding - BPE) chia nhỏ từ ngữ thành các cụm ký tự phổ biến.
- *Quy tắc chung đối với tiếng Anh*: 1 token tương đương khoảng 4 ký tự hoặc 0.75 từ.
- *Bài toán tiếng Việt*: Tiếng Việt sử dụng các ký tự có dấu phức tạp (như: á, ớ, ề, ự). Nhiều tokenizer của các mô hình thế hệ cũ không được tối ưu cho tiếng Việt, dẫn đến việc một từ tiếng Việt có dấu bị phân tách thành 2-4 tokens (so với tiếng Anh chỉ là 1 token). điều này làm chi phí API tăng lên gấp nhiều lần và giảm tốc độ sinh chữ của mô hình.

### Cách tính giá API thực tế
Các nhà cung cấp tính tiền dựa trên đơn vị $1.000.000$ tokens (M tokens) cho Input (đầu vào) và Output (đầu ra).
Ví dụ bảng giá GPT-4o:
- Input: $5.00 / M tokens
- Output: $15.00 / M tokens

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
Hãy viết một script Python đọc nội dung của một file văn bản dài bất kỳ trên máy bạn, tính toán số token của file đó khi chạy trên 3 mô hình: `gpt-4`, `gpt-3.5-turbo` và `gpt-4o`, sau đó xuất ra một bảng so sánh chi phí API đầu vào.

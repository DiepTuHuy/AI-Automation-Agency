import tiktoken

def calculate_tokens_count(text: str, model: str="gemini-2.5-flash") -> dict:
    """
    Lấy bộ mã hoá phù hợp với mô hình, và tính toán số lượng token trong văn bản đầu vào.
    Nếu mô hình không được hỗ trợ, sử dụng bộ mã hoá mặc định "cl100k_base".
    """
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")

    token_list = encoding.encode(text)
    token_count = len(token_list)

    price_per_million_tokens = 5.00
    cost = (token_count / 1_000_000) * price_per_million_tokens

    return {
        "text": text,
        "token_count": token_count,
        "cost": cost,
        "token_preview": [encoding.decode([token]) for token in token_list[:10]]  # Hiển thị 10 token đầu tiên để xem trước
    }

if __name__ == "__main__":
    text_en = "Hello world! This is a simple test to count tokens in English language."
    text_vi = "Xin chào thế giới! Đây là một bài thử nghiệm đơn giản để đếm số token trong tiếng Việt."
    
    res_en = calculate_tokens_count(text_en)
    res_vi = calculate_tokens_count(text_vi)
    
    print(f"Bản English: {res_en['token_count']} tokens. Chi phí ước lượng: ${res_en['cost']:.8f}")
    print(f"Bản Tiếng Việt: {res_vi['token_count']} tokens. Chi phí ước lượng: ${res_vi['cost']:.8f}")
    print(f"Cụm token tiếng Việt phân tách: {res_vi['token_preview']}")
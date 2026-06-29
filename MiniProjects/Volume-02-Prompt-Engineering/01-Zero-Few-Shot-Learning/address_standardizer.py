import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

def standardize_address(raw_address: str) -> str:
    # prompt Few-shot định hình cấu trúc đầu ra
    prompt = f"""Bạn là chuyên gia địa lý hành chính Việt Nam. Hãy chuẩn hóa địa chỉ sau về dạng viết đúng chính tả và đầy đủ.

Ví dụ 1:
Địa chỉ gốc: "Hà lội"
Kết quả: "Thành phố Hà Nội"

Ví dụ 2:
Địa chỉ gốc: "Q1 Tp HCM"
Kết quả: "Quận 1, Thành phố Hồ Chí Minh"

Ví dụ 3:
Địa chỉ gốc: "p. Bến Nghé, Q.1"
Kết quả: "Phường Bến Nghé, Quận 1"

Tác vụ thực tế:
Địa chỉ gốc: "{raw_address}"
Kết quả:"""

    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(
        prompt,
        generation_config={"temperature": 0.0}
    )
    return response.text.strip()

if __name__ == "__main__":
    test_addr = "HN, Cầu Giấy, p. Dịch Vọng"
    standardized = standardize_address(test_addr)
    print(f"Địa chỉ thô: {test_addr}")
    print(f"Địa chỉ chuẩn hóa: {standardized}")
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

def calculate_debt_penalty(principal: float, delay_months: int) -> str:
    # prompt hướng dẫn chuỗi suy luận CoT để giải toán tài chính phức tạp
    prompt = f"""Bạn là trợ lý ảo kiểm toán ngân hàng. Hãy tính toán tiền phạt chậm trả nợ gốc lũy tiến theo quy tắc sau:
- Tháng thứ 1: phạt 2% trên nợ gốc.
- Tháng thứ 2: phạt 5% trên nợ gốc.
- Từ tháng thứ 3 trở đi: phạt 10% trên nợ gốc mỗi tháng.

Nợ gốc ban đầu: {principal} USD.
Số tháng trễ hạn: {delay_months} tháng.

Yêu cầu:
1. Hãy suy nghĩ và giải thích chi tiết cách tính tiền phạt của từng tháng.
2. In ra tổng số tiền phạt cuối cùng sau cùng.
"""
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(
        prompt,
        generation_config={"temperature": 0.0}
    )
    return response.text

if __name__ == "__main__":
    principal_amount = 10000.0  # 10k USD nợ gốc
    months = 4  # Trễ 4 tháng
    
    print("Đang tính toán tiền phạt...")
    result_log = calculate_debt_penalty(principal_amount, months)
    print("\nKết quả tính toán chi tiết từ AI:")
    print(result_log)
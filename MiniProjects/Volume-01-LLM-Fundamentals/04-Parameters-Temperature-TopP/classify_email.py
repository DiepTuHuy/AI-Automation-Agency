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
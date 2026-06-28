import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

def generate_slogan(temp: float) -> str:
    model = genai.GenerativeModel("gemini-2.5-flash")
    response = model.generate_content(
        "viết 1 câu slogan ngắn gọn cho thương hiệu cafe thông minh tự pha bằng robot",
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
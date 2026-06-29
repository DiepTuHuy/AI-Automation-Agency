import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

def ask_with_fallback(prompt: str) -> str:
    # Thử gọi model Pro trước
    try:
        print("Đang thử kết nối mô hình Gemini 2.5 Pro...")
        # Giả lập model sai tên để kích hoạt ngoại lệ tự động phục vụ test
        model = genai.GenerativeModel("gemini-2.5-pro-wrong-name-test")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Lỗi xảy ra với model Pro: {e}")
        print("-> Tự động kích hoạt cơ chế dự phòng: Chuyển sang Gemini 2.5 Flash...")
        try:
            model_flash = genai.GenerativeModel("gemini-2.5-flash")
            response = model_flash.generate_content(prompt)
            return response.text
        except Exception as flash_err:
            return f"Cả hai mô hình đều thất bại: {flash_err}"

if __name__ == "__main__":
    result = ask_with_fallback("Viết slogan cho dịch vụ sửa xe lưu động")
    print(f"\nKết quả cuối cùng: {result}")
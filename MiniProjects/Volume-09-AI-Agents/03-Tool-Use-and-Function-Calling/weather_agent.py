import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# 1. Định nghĩa hàm Python làm công cụ cho AI
def get_weather(city: str) -> str:
    """Tra cứu thời tiết hiện tại của một thành phố cụ thể.
    
    Args:
        city: Tên thành phố cần tra cứu (ví dụ: 'Hanoi', 'Saigon').
    """
    city_lower = city.lower()
    if "hanoi" in city_lower or "hà nội" in city_lower:
        return "Nhiệt độ 28°C, trời nhiều mây, có mưa rào nhẹ."
    elif "saigon" in city_lower or "hồ chí minh" in city_lower:
        return "Nhiệt độ 33°C, trời nắng nóng, độ ẩm cao."
    else:
        return "Không có dữ liệu thời tiết tại khu vực này."

if __name__ == "__main__":
    # 2. Đăng ký hàm làm công cụ thông qua tham số tools
    # Bật enable_automatic_function_calling=True để SDK tự động gọi hàm khi model yêu cầu
    model = genai.GenerativeModel(
        "gemini-2.5-flash",
        tools=[get_weather]
    )
    
    chat = model.start_chat(enable_automatic_function_calling=True)
    
    query = "Thời tiết ở Hà Nội hôm nay thế nào em?"
    print(f"Câu hỏi: {query}")
    res = chat.send_message(query)
    
    print("\nKết quả gọi tool và trả lời của AI:")
    print(res.text)
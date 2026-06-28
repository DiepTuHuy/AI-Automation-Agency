import os
import sys
import asyncio
import google.generativeai as genai
from dotenv import load_dotenv

# Tải biến môi trường
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    # Central config load
    from pathlib import Path
    load_dotenv(Path(__file__).resolve().parents[3] / "AI-Playbook-Platform" / ".env")
    api_key = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=api_key)

from server import get_order_status

# Định nghĩa hàm wrapper để ghi log trực quan cho học sinh theo dõi
def get_order_status_wrapper(order_id: str) -> str:
    """Kiểm tra trạng thái của một đơn hàng cụ thể dựa trên Mã đơn hàng (Ví dụ: 'OR-111')."""
    print(f"[Client -> MCP Server Tool] Yêu cầu gọi: get_order_status('{order_id}')")
    result = get_order_status(order_id)
    print(f"[MCP Server -> Client] Phản hồi từ database: {result}\n")
    return result

def ask_agent(query: str):
    print(f"Khách hàng: {query}\n")
    
    # Khởi tạo mô hình với đăng ký công cụ tự động
    model = genai.GenerativeModel(
        "gemini-2.5-flash",
        tools=[get_order_status_wrapper],
        system_instruction="Bạn là trợ lý chăm sóc khách hàng. Hãy luôn tra cứu thông tin bằng công cụ trước khi đưa ra câu trả lời cuối cùng cho khách hàng."
    )
    
    # Sử dụng tính năng gọi hàm tự động (automatic function calling) cực kỳ mạnh mẽ của Gemini
    chat = model.start_chat(enable_automatic_function_calling=True)
    response = chat.send_message(query)
    
    print(f"Trợ lý AI: {response.text}")

if __name__ == "__main__":
    # Đảm bảo database đã được tạo trước
    if not os.path.exists("orders.db"):
        print("Database chưa được khởi tạo. Đang tạo...")
        import subprocess
        subprocess.run(["python3", "setup_db.py"])
        
    ask_agent("Tôi muốn kiểm tra đơn hàng mã OR-111 xem khi nào giao?")

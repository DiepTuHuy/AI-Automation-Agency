import os
import sys
import asyncio
from openai import OpenAI
from dotenv import load_dotenv

# Tải biến môi trường
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Mock Client kết nối đơn giản qua STDIO
# Trong thực tế, bạn sẽ dùng mcp.client để kết nối trực tiếp với server.py
# Để chạy demo này đơn giản nhất, ta định nghĩa cấu trúc tool schema của MCP Server
# và gọi hàm trực tiếp khi AI yêu cầu.

from server import get_order_status

def ask_agent(query: str):
    print(f"Khách hàng: {query}\n")
    
    # 1. Định nghĩa công cụ tương ứng với MCP Server Tools
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_order_status",
                "description": "Kiểm tra trạng thái đơn hàng bằng mã đơn hàng (Ví dụ: 'OR-111').",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "order_id": {"type": "string", "description": "Mã đơn hàng cần tra cứu."}
                    },
                    "required": ["order_id"]
                }
            }
        }
    ]
    
    messages = [
        {"role": "system", "content": "Bạn là trợ lý chăm sóc khách hàng. Hãy tra cứu thông tin bằng công cụ trước khi trả lời."},
        {"role": "user", "content": query}
    ]
    
    # Lượt 1: AI suy nghĩ và chọn gọi Tool của MCP Server
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=tools,
        temperature=0
    )
    
    msg = response.choices[0].message
    tool_calls = msg.tool_calls
    
    if tool_calls:
        for tool_call in tool_calls:
            if tool_call.function.name == "get_order_status":
                import json
                args = json.loads(tool_call.function.arguments)
                order_id = args["order_id"]
                
                print(f"[Client -> MCP Server] Yêu cầu gọi: get_order_status('{order_id}')")
                
                # Gọi trực tiếp logic của MCP Server
                result = get_order_status(order_id)
                print(f"[MCP Server -> Client] Phản hồi: {result}\n")
                
                # Gửi kết quả ngược lại cho AI
                messages.append(msg)
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": "get_order_status",
                    "content": result
                })
                
                final_response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages
                )
                print(f"Trợ lý AI: {final_response.choices[0].message.content}")
    else:
        print(f"Trợ lý AI: {msg.content}")

if __name__ == "__main__":
    # Đảm bảo database đã được tạo trước
    if not os.path.exists("orders.db"):
        print("Database chưa được khởi tạo. Đang tạo...")
        import subprocess
        subprocess.run(["python3", "setup_db.py"])
        
    ask_agent("Tôi muốn kiểm tra đơn hàng mã OR-111 xem khi nào giao?")

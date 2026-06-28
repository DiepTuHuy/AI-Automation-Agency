# Chương 01: Giám sát & Quản lý dấu vết (Observability) bằng LangSmith

## 1. Deep Dive (Phân tích chuyên sâu)

### Tại sao logs thông thường thất bại trong AI?
Trong lập trình backend truyền thống, khi API lỗi, bạn chỉ cần đọc log traceback để biết dòng code nào bị crash.
Tuy nhiên, trong hệ thống AI Agent:
- Code không bị crash (trả về HTTP 200).
- Nhưng AI trả lời sai do gọi sai công cụ hoặc prompt ngữ cảnh bị loãng.
- Để sửa lỗi, bạn cần biết: *Hành trình suy nghĩ của AI ở bước 1 là gì? Nó đã lấy gì từ database? Dữ liệu prompt chính xác gửi lên API ở bước 2 là gì?*

### LangSmith và LangFuse
Đây là các nền tảng **Observability (Giám sát toàn diện)** chuyên dụng cho LLMs. Chúng cung cấp khả năng tự động ghi nhận (Auto-tracing) toàn bộ luồng suy luận của AI dưới dạng sơ đồ cây trực quan (Trace Tree) hiển thị chi tiết:
- Toàn bộ Prompt gửi đi và Response nhận về của từng node.
- Số lượng token tiêu thụ và chi phí ước lượng của mỗi lượt chạy.
- Thời gian thực thi (Latency) của từng bước trung gian.
- Kết quả trả về của các công cụ (Tools execution).

---

## 2. Demo: Tích hợp Tracing tự động vào Python Script

### Mục tiêu
Cấu hình dự án Python tự động gửi log tracing lên dashboard của LangSmith mà không cần sửa đổi nhiều cấu trúc code chính.

### Các bước thực hiện
1. Đăng ký tài khoản miễn phí tại `smith.langchain.com`.
2. Tạo một dự án mới và sinh **API Key**.
3. Cài đặt thư viện: `pip install langchain-openai`
4. Cấu hình biến môi trường và chạy mã nguồn (`trace_demo.py`):

```python
import os
from openai import OpenAI
from dotenv import load_dotenv

# 1. Kích hoạt Tracing bằng cách cấu hình biến môi trường hệ thống
# Các thư viện tích hợp như LangChain hoặc OpenAI Client (khi bật debug) 
# sẽ tự động đọc các biến này để gửi log lên cloud
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGSMITH_API_KEY", "your_api_key_here")
os.environ["LANGCHAIN_PROJECT"] = "CRM_Agent_Monitoring"

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def run_monitored_agent():
    print("Đang chạy Agent và gửi dấu vết lên LangSmith...")
    
    # Một cuộc hội thoại mẫu
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Bạn là kỹ sư AI giám sát hệ thống."},
            {"role": "user", "content": "Hãy giải thích sự khác biệt giữa Tracing và Logging."}
        ],
        temperature=0
    )
    print("Hoàn thành! Hãy mở Dashboard LangSmith để kiểm tra sơ đồ Trace Tree.")
    return response.choices[0].message.content

if __name__ == "__main__":
    run_monitored_agent()
```

---

## 3. Mini Project

### Bài tập 1: Thiết lập ghi Log giám sát cuộc gọi API (Mức độ: Trung bình)
* **Đề bài**: Viết một script Python bọc cuộc gọi tới Gemini API và ghi nhận chi tiết thông số cuộc gọi: Thời gian phản hồi (Latency), Số lượng token sử dụng, Trạng thái thành công hay thất bại vào file log cục bộ.
* **Mã nguồn mẫu (`api_monitor.py`)**:
```python
import os
import time
import logging
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

logging.basicConfig(filename="api_metrics.log", level=logging.INFO, format="%(asctime)s - %(message)s")

def monitored_call(prompt: str):
    model = genai.GenerativeModel("gemini-2.5-flash")
    start_time = time.time()
    
    try:
        response = model.generate_content(prompt)
        latency = time.time() - start_time
        
        # Ghi log metrics
        logging.info(
            f"Prompt: '{prompt[:20]}...' | Status: SUCCESS | "
            f"Latency: {latency:.2f}s | Response length: {len(response.text)} chars"
        )
        return response.text
    except Exception as e:
        latency = time.time() - start_time
        logging.error(f"Prompt: '{prompt[:20]}...' | Status: FAILED | Latency: {latency:.2f}s | Error: {e}")
        return None

if __name__ == "__main__":
    monitored_call("Giải thích về tính năng giám sát hệ thống AI.")
```

### Bài tập 2: Tự động thống kê hiệu năng vận hành API hàng tuần (Mức độ: Khó)
* **Đề bài**: Viết một script Python đọc file `api_metrics.log`. Phân tích toàn bộ dữ liệu log thu thập được để tính toán các chỉ số: Tỷ lệ thành công (Success Rate), Thời gian phản hồi trung bình (Average Latency) và in báo cáo tổng quan.
* **Yêu cầu**: Học viên tự hoàn thành không có code mẫu.
* **Gợi ý triển khai (Workflow Hints)**:
  1. Sử dụng thư viện `pandas` hoặc đọc file dòng-bằng-dòng để phân tích log.
  2. Trích xuất thời gian chạy (Latency) từ chuỗi log bằng Regular Expression (Regex).
  3. Tính toán các chỉ số trung bình và in báo cáo dạng bảng trực quan.


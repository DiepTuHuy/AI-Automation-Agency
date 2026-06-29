# Chương 04: Lập trình Bất đồng bộ với `asyncio` & `aiohttp`

## 1. Deep Dive (Phân tích chuyên sâu)

### Tại sao Lập trình Đồng bộ là rào cản lớn?
Trong lập trình đồng bộ (Synchronous), các lệnh được thực thi tuần tự. Nếu bạn gọi API của OpenAI và mất 3 giây để nhận phản hồi, chương trình của bạn sẽ bị "đóng băng" (blocked) hoàn toàn trong 3 giây đó. Nếu bạn cần xử lý 100 văn bản độc lập, tổng thời gian sẽ là $100 	imes 3 = 300$ giây (5 phút!).

### Lập trình Bất đồng bộ (Asynchronous)
Bằng cách sử dụng **`asyncio`** và thư viện HTTP client async như **`aiohttp`**, Python có thể gửi đi 100 yêu cầu API cùng một lúc. Trong lúc chờ đợi phản hồi từ mạng Internet, CPU sẽ chuyển sang xử lý các tác vụ khác. Khi có kết quả trả về, event loop sẽ tự động xử lý. Tổng thời gian xử lý 100 văn bản có thể giảm xuống chỉ còn khoảng 3-5 giây!

---

## 2. Demo: Gọi API OpenAI song song hàng loạt

### Mục tiêu
Gửi 5 prompt sáng tạo khác nhau tới API OpenAI đồng thời và đo tổng thời gian chạy để thấy rõ sức mạnh của lập trình bất đồng bộ.

### Mã nguồn (`async_openai.py`)
Cài đặt thư viện: `pip install aiohttp`

```python
import os
import time
import asyncio
import aiohttp
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENAI_API_KEY")

async def fetch_ai_response(session: aiohttp.ClientSession, prompt: str, task_id: int):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    
    print(f"[Task {task_id}] Đang gửi yêu cầu...")
    start_time = time.time()
    
    try:
        async with session.post(url, headers=headers, json=payload) as response:
            result = await response.json()
            answer = result["choices"][0]["message"]["content"].strip()
            duration = time.time() - start_time
            print(f"[Task {task_id}] Hoàn thành sau {duration:.2f}s. Trả lời: {answer[:30]}...")
            return answer
    except Exception as e:
        print(f"[Task {task_id}] Lỗi: {str(e)}")
        return None

async def main():
    prompts = [
        "Kể một trò đùa về lập trình viên Python.",
        "Kể một trò đùa về lập trình viên JavaScript.",
        "Kể một trò đùa về lập trình viên C++.",
        "Kể một trò đùa về AI Engineer.",
        "Kể một trò đùa về Project Manager."
    ]
    
    start_all = time.time()
    
    # Khởi tạo một session HTTP bất đồng bộ
    async with aiohttp.ClientSession() as session:
        # Tạo danh sách các task coroutine cần chạy
        tasks = [fetch_ai_response(session, prompt, i+1) for i, prompt in enumerate(prompts)]
        
        # Chạy song song tất cả các task và gom kết quả
        results = await asyncio.gather(*tasks)
        
    print(f"\nTổng thời gian xử lý song song: {time.time() - start_all:.2f} giây!")

if __name__ == "__main__":
    # Kích hoạt Event Loop của asyncio
    asyncio.run(main())
```

---

## 3. Mini Project

### Bài tập 1: Quét trạng thái nhiều website đồng thời bằng Asyncio (Mức độ: Trung bình)
* **Đề bài**: Viết một script Python sử dụng thư viện `asyncio` và `httpx` để kiểm tra mã trạng thái HTTP (status code) của 3 trang web cùng một lúc.
* **Mã nguồn mẫu (`async_status_checker.py`)**:
```python
import asyncio
import httpx

urls = [
    "https://httpbin.org/status/200",
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/500"
]

async def check_url(client: httpx.AsyncClient, url: str):
    try:
        response = await client.get(url)
        print(f"URL: {url} -> Status: {response.status_code}")
    except Exception as e:
        print(f"URL: {url} -> Lỗi kết nối: {e}")

async def main():
    async with httpx.AsyncClient() as client:
        # Tạo danh sách các task chạy song song
        tasks = [check_url(client, url) for url in urls]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
```

### Bài tập 2: Hệ thống quét giá sản phẩm thời gian thực (Mức độ: Khó)
* **Đề bài**: Xây dựng một script bất đồng bộ tải thông tin giá của 5 mã cổ phiếu hoặc 5 mặt hàng từ API giả lập. Giới hạn thời gian tối đa cho mỗi request là 3 giây (timeout). Nếu quá thời gian, hủy tác vụ đó và chuyển sang xử lý kết quả của các tác vụ hoàn thành khác để tránh treo hệ thống.
* **Yêu cầu**: Bạn hãy tự hoàn thành không có code mẫu.
* **Gợi ý triển khai (Workflow Hints)**:
  1. Sử dụng `asyncio.wait_for()` để thiết lập timeout cho từng task bất đồng bộ.
  2. Bọc khối lệnh trong `try-except asyncio.TimeoutError`.
  3. Thu thập và in báo cáo thống kê các tác vụ thành công.

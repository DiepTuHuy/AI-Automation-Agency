# Chương 02: Tương tác REST API bằng `requests`

## 1. Deep Dive (Phân tích chuyên sâu)

### Giao thức HTTP và REST API
Hầu hết các hệ thống trên thế giới kết nối với nhau thông qua HTTP/HTTPS REST API. Để gọi các dịch vụ AI hoặc gửi tin nhắn thông báo, bạn phải nắm rõ:
1. **HTTP Methods**:
   - `GET`: Yêu cầu lấy dữ liệu từ server (ví dụ: lấy thông tin thời tiết).
   - `POST`: Gửi dữ liệu mới lên server để xử lý (ví dụ: gửi prompt lên OpenAI để sinh văn bản).
2. **HTTP Status Codes**:
   - `200 OK`, `201 Created`: Thành công.
   - `400 Bad Request`: Lỗi định dạng dữ liệu gửi lên.
   - `401 Unauthorized`: API Key bị sai hoặc hết hạn.
   - `429 Too Many Requests`: Gửi request quá nhanh vượt giới hạn của server (Rate Limit).
   - `500 Internal Server Error`: Lỗi máy chủ bên đối tác bị hỏng.

---

## 2. Demo: Tự động gửi tin nhắn báo cáo lên Telegram

### Mục tiêu
Viết một module Python kết nối với Telegram API, tự động gửi một tin nhắn báo cáo trạng thái hệ thống tới kênh Telegram cá nhân của bạn thông qua HTTP POST.

### Mã nguồn (`telegram_sender.py`)
```python
import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Lấy token và chat ID từ file .env
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_alert(message: str) -> bool:
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("[Lỗi] Thiếu thông tin cấu hình Telegram trong file .env!")
        return False
        
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    
    # Định nghĩa dữ liệu gửi đi dạng JSON
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    try:
        # Gửi request POST
        response = requests.post(url, json=payload, timeout=10)
        
        # Kiểm tra mã trạng thái trả về (nếu không phải 2xx sẽ ném ngoại lệ)
        response.raise_for_status()
        print("Đã gửi tin nhắn Telegram thành công!")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Gửi tin nhắn thất bại: {str(e)}")
        return False

if __name__ == "__main__":
    # Để chạy demo này, bạn cần cấu hình thực tế Token của Bot Telegram
    # Tạm thời chạy thử thông báo kiểm tra cấu hình
    print("Đang thử kết nối...")
    send_telegram_alert("*BÁO CÁO HỆ THỐNG*\nTrạng thái: Hoạt động bình thường\nCPU: 12% | RAM: 45%")
```

---

## 3. Mini Project

### Bài tập 1: Lấy tỷ giá hối đoái tự động bằng Requests (Mức độ: Trung bình)
* **Đề bài**: Viết một script Python sử dụng thư viện `requests` để gọi API tỷ giá hối đoái công cộng và in ra tỷ giá của đồng USD so với VND.
* **Mã nguồn mẫu (`exchange_rate.py`)**:
```python
import requests

def get_usd_to_vnd():
    url = "https://open.er-api.com/v6/latest/USD"
    try:
        response = requests.get(url)
        response.raise_for_status() # Báo lỗi nếu HTTP status không phải 200
        
        data = response.json()
        rates = data.get("rates", {})
        vnd_rate = rates.get("VND")
        
        if vnd_rate:
            print(f"1 USD = {vnd_rate:,.2f} VND")
            print(f"Cập nhật lúc: {data.get('time_last_update_utc')}")
        else:
            print("Không tìm thấy thông tin tỷ giá VND.")
    except requests.exceptions.RequestException as e:
        print(f"Lỗi khi kết nối API: {e}")

if __name__ == "__main__":
    get_usd_to_vnd()
```

### Bài tập 2: Tự động gửi thông tin thời tiết qua Discord/Telegram Webhook (Mức độ: Khó)
* **Đề bài**: Viết một script Python tích hợp: Đầu tiên gọi API thời tiết công cộng để lấy nhiệt độ hiện tại của Hà Nội, sau đó gửi một tin nhắn được định dạng đẹp mắt (Markdown) thông báo thời tiết đó đến một kênh Discord hoặc Telegram thông qua cơ chế Webhook.
* **Yêu cầu**: Học viên tự hoàn thành không có code mẫu.
* **Gợi ý triển khai (Workflow Hints)**:
  1. Sử dụng URL API thời tiết mở: `https://api.open-meteo.com/v1/forecast?latitude=21.0285&longitude=105.8542&current_weather=true`.
  2. Tạo một webhook URL trên server Discord của bạn.
  3. Gửi request dạng `POST` bằng `requests.post()` chứa payload JSON `{"content": "Thông điệp thời tiết..."}` lên webhook đó.

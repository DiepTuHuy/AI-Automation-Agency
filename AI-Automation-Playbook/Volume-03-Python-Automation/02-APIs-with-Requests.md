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
Hãy viết một script Python kết nối với một API thời tiết công cộng miễn phí (ví dụ: OpenWeatherMap hoặc WeatherAPI), trích xuất thông tin nhiệt độ và độ ẩm hiện tại của Hà Nội, sau đó định dạng thành một tin nhắn Markdown đẹp đẽ và gửi tự động tới Telegram của bạn.

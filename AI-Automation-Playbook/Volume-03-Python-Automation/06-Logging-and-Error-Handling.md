# Chương 06: Bắt lỗi & Ghi nhật ký hệ thống (Logging)

## 1. Deep Dive (Phân tích chuyên sâu)

### Tư duy thiết kế phòng vệ (Defensive Programming)
Hệ thống tự động chạy trên Production sẽ gặp hàng trăm lỗi không lường trước:
- Mất kết nối internet đột ngột.
- Khách hàng tải lên file PDF bị hỏng hoặc sai định dạng.
- API OpenAI bị quá tải dính lỗi Rate Limit.
- Cơ sở dữ liệu bị khóa tạm thời.

Do đó, bạn phải luôn bao bọc các đoạn code dễ gãy trong khối **`try-except-finally`**.

### Thay thế `print()` bằng thư viện `logging`
Khi script của bạn chạy ẩn trong nền hệ thống (Background Task), không có ai ngồi nhìn màn hình console để xem các lệnh `print()`. 
Thư viện **`logging`** tích hợp sẵn của Python giúp ghi lại lịch sử hoạt động vào các tệp tin lưu trữ lâu dài trên đĩa cứng, kèm theo các thông tin vô giá để debug:
- Mức độ lỗi (INFO, WARNING, ERROR, CRITICAL).
- Dòng code gây lỗi.
- Thời điểm chính xác xảy ra sự cố (Timestamp).

---

## 2. Demo: Hệ thống bắt lỗi và Log xoay vòng tự động

### Mục tiêu
Thiết lập một Logger chuyên nghiệp ghi log ra file, giới hạn dung lượng file log và tự động xoay vòng (tạo file mới khi file cũ đầy) để tránh làm tràn ổ cứng server.

### Mã nguồn (`logger_setup.py`)
```python
import logging
from logging.handlers import RotatingFileHandler

def setup_logger():
    # Khởi tạo Logger chính
    logger = logging.getLogger("AI_Automation_System")
    logger.setLevel(logging.DEBUG) # Ghi nhận tất cả các mức log
    
    # Định dạng hiển thị của log
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s')
    
    # Handler 1: Ghi ra file log xoay vòng (Max 1MB/file, lưu tối đa 3 file backup)
    file_handler = RotatingFileHandler("system.log", maxBytes=1024*1024, backupCount=3, encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    
    # Handler 2: In ra màn hình console để lập trình viên theo dõi nhanh
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    
    # Thêm các handler vào logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

logger = setup_logger()

def divide_budget(total_budget: float, num_channels: int):
    logger.info(f"Bắt đầu chia ngân sách: {total_budget} cho {num_channels} kênh.")
    try:
        result = total_budget / num_channels
        logger.info(f"Chia ngân sách thành công. Mỗi kênh nhận: {result}")
        return result
    except ZeroDivisionError:
        logger.error("Lỗi chia cho 0! Số lượng kênh quảng cáo không thể bằng 0.")
        return 0
    except TypeError as e:
        logger.warning(f"Lỗi kiểu dữ liệu truyền vào: {str(e)}")
        return 0

if __name__ == "__main__":
    divide_budget(1000, 5)
    divide_budget(1000, 0) # Gây lỗi ZeroDivisionError
    divide_budget("Một nghìn", 2) # Gây lỗi TypeError
```

---

## 3. Mini Project
Hãy xây dựng một module Python thực hiện đọc ghi tệp cấu hình JSON từ Chương 3. Bổ sung hệ thống bắt lỗi (try-except) khi file JSON bị hỏng cấu trúc cú pháp, ghi log chi tiết lỗi định dạng vào file log, và gửi cảnh báo trực tiếp về kênh Telegram của bạn khi phát hiện lỗi nghiêm trọng.

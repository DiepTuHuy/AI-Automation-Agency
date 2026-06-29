import logging

# Cấu hình logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log", encoding="utf-8"),
        logging.StreamHandler() # Ghi ra console
    ]
)

def divide_numbers(a, b):
    logging.info(f"Bắt đầu thực hiện phép chia: {a} / {b}")
    try:
        result = a / b
        logging.info(f"Phép chia thành công. Kết quả: {result}")
        return result
    except ZeroDivisionError as e:
        logging.error(f"Lỗi chia cho 0 xảy ra: {e}", exc_info=True)
        return None

if __name__ == "__main__":
    divide_numbers(10, 2)
    divide_numbers(10, 0)
# Chương 02: Tích hợp Cổng thanh toán tự động hóa với Stripe API

## 1. Deep Dive (Phân tích chuyên sâu)

### Stripe - Chuẩn mực thanh toán toàn cầu cho SaaS
Để biến phần mềm của bạn thành cỗ máy in tiền tự động, bạn cần tích hợp một cổng thanh toán trực tuyến xử lý thẻ quốc tế tự động. **Stripe** là sự lựa chọn số 1 của thế giới khởi nghiệp công nghệ.

### Luồng chạy thanh toán của Stripe Checkout & Webhook
```
1. Client bấm nút "Nâng cấp gói Pro" -> Gọi FastAPI của bạn.
2. FastAPI gọi Stripe SDK tạo một cổng checkout (Stripe Checkout Session URL) và trả link về cho Client.
3. Người dùng chuyển hướng sang trang thanh toán bảo mật của Stripe, điền thẻ và thanh toán thành công.
4. Stripe gửi một Webhook POST (Sự kiện: 'checkout.session.completed') về API endpoint của bạn.
5. FastAPI của bạn nhận webhook, xác thực chữ ký an toàn, cập nhật cột 'is_active = True' cho người dùng trong database nội bộ.
```

---

## 2. Demo: Viết Webhook API tiếp nhận thanh toán trong FastAPI

### Mục tiêu
Xây dựng endpoint FastAPI tiếp nhận webhook từ Stripe để tự động kích hoạt tính năng Premium cho tài khoản người dùng sau khi họ thanh toán thành công.

### Mã nguồn (`stripe_webhook.py`)
Yêu cầu cài đặt: `pip install stripe fastapi`

```python
import os
import stripe
from fastapi import FastAPI, Request, Header, HTTPException
from dotenv import load_dotenv

load_dotenv()
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
# Chìa khóa bí mật dùng để xác thực webhook gửi đúng từ Stripe
ENDPOINT_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")

app = FastAPI()

@app.post("/api/v1/stripe/webhook")
async def stripe_webhook(request: Request, stripe_signature: str = Header(None)):
    # 1. Đọc nội dung body thô gửi từ Stripe
    payload = await request.body()
    
    try:
        # 2. Xác thực tính đúng đắn của chữ ký để chống request giả lập
        event = stripe.Webhook.construct_event(
            payload, stripe_signature, ENDPOINT_SECRET
        )
    except ValueError as e:
        # Lỗi payload không hợp lệ
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError as e:
        # Lỗi chữ ký giả mạo
        raise HTTPException(status_code=400, detail="Invalid signature")

    # 3. Xử lý sự kiện thanh toán thành công
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        
        # Trích xuất metadata email đã gửi kèm khi tạo checkout session
        customer_email = session.get('customer_details', {}).get('email')
        client_reference_id = session.get('client_reference_id') # Thường chứa User ID của bạn
        
        print(f"Thanh toán thành công từ khách hàng: {customer_email} (User ID: {client_reference_id})")
        # Logic backend của bạn: Cập nhật trạng thái VIP cho User ID này trong database
        # update_user_status_to_vip(client_reference_id)
        
    return {"status": "success"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("stripe_webhook:app", host="127.0.0.1", port=8000, reload=True)
```

---

## 3. Mini Project
Hãy viết một script Python độc lập tạo một Stripe Checkout Session cho sản phẩm thuê bao định kỳ trị giá 29 USD/tháng, cấu hình `client_reference_id` truyền vào là chuỗi `"user_test_999"`, và in ra đường dẫn URL thanh toán Stripe trả về để test trên trình duyệt.

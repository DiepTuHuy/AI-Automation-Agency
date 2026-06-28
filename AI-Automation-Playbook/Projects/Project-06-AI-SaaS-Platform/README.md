# Project 06: AI SaaS Platform

Dự án này là đỉnh cao của toàn bộ playbook, kết hợp kiến thức từ Volume 16 (Scaling) và Volume 17 (AI SaaS) để xây dựng một nền tảng SaaS hoàn chỉnh: hỗ trợ đăng ký người dùng, phân quyền (Authentication), thu phí tự động qua Stripe Subscriptions, và cô lập dữ liệu theo Tenant ID để phục vụ hàng nghìn doanh nghiệp khách thuê cùng lúc.

---

## 1. Architecture Diagram (Kiến trúc hệ thống)

```
[Khách hàng vãng lai] ──> [Đăng ký / Đăng nhập (FastAPI Auth)] ──> [Sinh JWT Token]
                                     │
                                     ▼
                      [Thanh toán qua Stripe Checkout Link]
                                     │
                                     ▼ (Webhook)
                   [Cập nhật trạng thái VIP trong database]
                                     │
                                     ▼
                    [Sử dụng các endpoint AI trích xuất]
                      (Luôn tự động lọc: tenant_id = X)
```

---

## 2. Source Tree (Cấu trúc mã nguồn)
```
Project-06-AI-SaaS-Platform/
├── README.md
├── requirements.txt
├── .env.example
└── app.py
```

---

## 3. Deployment Guide (Hướng dẫn triển khai)

### Bước 1: Khởi động môi trường ảo
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Bước 2: Cấu hình biến môi trường
Sao chép `.env.example` thành `.env` và điền đầy đủ các khóa:
```env
GEMINI_API_KEY=your_gemini_api_key_here
STRIPE_SECRET_KEY=sk_test_xxxxxx
STRIPE_WEBHOOK_SECRET=whsec_xxxxxx
JWT_SECRET=super_secret_signing_key_123
```

### Bước 3: Chạy ứng dụng SaaS Backend
Thực thi lệnh:
```bash
python3 app.py
```
*Mở `http://127.0.0.1:8000/docs` trên trình duyệt để kiểm thử toàn bộ luồng Auth, Stripe Webhook và các protected endpoints*.

---

## 4. Lessons Learned (Bài học rút ra)
- **Kiến trúc Multi-tenant cô lập**: Việc chèn bộ lọc Tenant ID ở tầng middleware của cơ sở dữ liệu giúp loại bỏ 100% rủi ro lập trình viên vô tình viết thiếu lệnh filter ở code nghiệp vụ thông thường.
- **Idempotency (Tính không thay đổi của Webhook)**: Stripe Webhook có thể gửi một sự kiện nhiều lần. Việc kiểm tra xem ID giao dịch đã xử lý chưa trước khi cộng hạn mức cho người dùng là bắt buộc để tránh bị khai thác lỗi.

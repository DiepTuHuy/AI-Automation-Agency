# Quy trình Onboarding Khách hàng tự động

### 1. Luồng hoạt động:
* Khách hàng điền thông tin đăng ký tư vấn trên Form (Typeform/Google Forms).
* n8n nhận dữ liệu -> Tự động tạo hồ sơ khách hàng mới trong CRM (như Notion hoặc Hubspot).
* Tự động gửi email chào mừng kèm link đặt lịch họp tư vấn qua Calendly.

### 2. Các Node cần sử dụng:
* Google Forms Trigger -> Notion Card Creator -> Gmail Send Email.
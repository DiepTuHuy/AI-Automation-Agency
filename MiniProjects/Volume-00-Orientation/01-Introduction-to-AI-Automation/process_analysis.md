# Phân tích quy trình thủ công: Nhập liệu hóa đơn

### 1. Quy trình hiện tại (As-Is):
* Nhân viên nhận file PDF hóa đơn từ email khách hàng.
* Mở file PDF và copy-paste thủ công các trường: Số hóa đơn, Ngày, Tổng tiền, Thuế vào file Excel.
* Mất trung bình 5-7 phút cho mỗi hóa đơn. Tỷ lệ sai sót nhập liệu khoảng 5%.

### 2. Đề xuất tự động hóa tích hợp AI (To-Be):
* Sử dụng n8n tự động bắt webhook từ email mới nhận.
* Gửi file PDF hóa đơn qua Gemini API (Structured Outputs) để trích xuất dữ liệu JSON sạch.
* Ghi tự động dữ liệu vào Google Sheets.
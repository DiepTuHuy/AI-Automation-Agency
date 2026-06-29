# Hướng dẫn cấu hình hệ thống AI Agent cho vận hành viên

### Bước 1: Truy cập tệp cấu hình môi trường
* Mở thư mục gốc của ứng dụng trên máy chủ hoặc máy tính của bạn.
* Tìm tệp tin mang tên `.env`.

### Bước 2: Cập nhật Google Gemini API Key mới
* Mở tệp `.env` bằng phần mềm Notepad hoặc bất kỳ trình soạn thảo văn bản nào.
* Tìm dòng: `GEMINI_API_KEY=cũ_của_bên_phát_triển`
* Thay thế bằng khóa bảo mật mới của công ty bạn: `GEMINI_API_KEY=AIzaSyNewKey...`
* Lưu tệp tin lại và khởi động lại dịch vụ.
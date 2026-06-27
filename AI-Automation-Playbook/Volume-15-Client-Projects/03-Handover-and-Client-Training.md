# Chương 03: Quy trình Bàn giao, Đào tạo nhân sự & Nghiệm thu dự án

## 1. Deep Dive (Phân tích chuyên sâu)

### 1. Tài liệu bàn giao kỹ thuật (Handover Document)
Tài liệu bàn giao là văn bản chứng minh bạn đã hoàn thành đầy đủ nghĩa vụ cam kết trong hợp đồng. Nó giúp đội ngũ IT hoặc người quản trị phía khách hàng có thể tiếp quản và vận hành hệ thống bền vững.
Tài liệu bàn giao bắt buộc phải chứa:
- Sơ đồ kiến trúc thực tế.
- Hướng dẫn cấu hình biến môi trường (API Keys, database URL).
- Danh sách tài khoản quản trị (Admin credentials).
- Hướng dẫn vận hành cơ bản (cách khởi động lại server, cách đọc log lỗi).

### 2. Đào tạo người dùng cuối (User Training)
Người sử dụng trực tiếp hệ thống thường là nhân viên văn phòng, kế toán hoặc sales - những người không biết lập trình. Do đó:
- Không giải thích mã nguồn Python.
- Hãy tập trung hướng dẫn: *"Bấm vào nút này để upload file, xem kết quả ở cột này, và phải làm gì nếu AI chấm điểm sai"*.
- Quay video Loom ngắn (2-3 phút) cho từng tính năng và lưu trữ trong thư mục tài liệu chung để họ có thể tự xem lại khi quên.

---

## 2. Demo: Mẫu Biên bản Nghiệm thu & Bàn giao dự án (Acceptance Certificate)

### Mục tiêu
Cung cấp mẫu biên bản nghiệm thu chuẩn pháp lý để hai bên ký kết kết thúc dự án, giải ngân số tiền còn lại.

### Nội dung Biên bản mẫu (`acceptance_certificate.md`)
```markdown
# BIÊN BẢN BÀN GIAO VÀ NGHIỆM THU DỰ ÁN

Hôm nay, ngày 28 tháng 06 năm 2026, tại văn phòng Công ty TNHH Giải pháp AI Antigravity, chúng tôi gồm:

**BÊN A (Bên Yêu Cầu Dịch Vụ): CÔNG TY CỔ PHẦN THƯƠNG MẠI HOÀNG HÀ**
- Đại diện: Ông Nguyễn Văn A | Chức vụ: Giám đốc Điều hành.

**BÊN B (Bên Cung Cấp Dịch Vụ): CÔNG TY TNHH GIẢI PHÁP AI ANTIGRAVITY**
- Đại diện: Ông Huy Điệp | Chức vụ: Giám đốc Kỹ thuật.

Hai bên cùng tiến hành ký xác nhận các nội dung bàn giao dưới đây:

### 1. Nội dung bàn giao kỹ thuật
Bên B đã tiến hành cài đặt và bàn giao đầy đủ cho Bên A các hạng mục:
- Mã nguồn hệ thống AI CRM Backend đóng gói trong Docker Container.
- Tài khoản quản trị hệ thống n8n tự host trên máy chủ VPS của Bên A.
- 01 Tài liệu hướng dẫn sử dụng dạng PDF và 03 Video hướng dẫn thao tác gửi qua Loom.
- File cơ sở dữ liệu SQLite ban đầu.

### 2. Xác nhận nghiệm thu
- Bên A xác nhận hệ thống hoạt động ổn định, trích xuất thông tin chính xác đạt tỷ lệ trên 90% theo đúng cam kết tại Phụ lục SOW.
- Bên A đồng ý nghiệm thu toàn phần dự án và tiến hành thủ tục thanh toán đợt cuối (50% giá trị hợp đồng còn lại) cho Bên B trong vòng 5 ngày làm việc kể từ ngày ký biên bản này.

Biên bản được lập thành hai (02) bản có giá trị pháp lý tương đương nhau, mỗi bên giữ một (01) bản.

ĐẠI DIỆN BÊN A                               ĐẠI DIỆN BÊN B
(Ký, ghi rõ họ tên)                          (Ký, ghi rõ họ tên)
```

---

## 3. Mini Project
Hãy soạn thảo một cuốn tài liệu Hướng dẫn sử dụng dài 1 trang Markdown dành riêng cho nhân viên kế toán hướng dẫn cách sử dụng ứng dụng **Project 02 (AI CRM Lead Qualification)**. Hãy viết thật dễ hiểu, sử dụng các ký tự Markdown đẹp đẽ để làm nổi bật các bước thao tác.

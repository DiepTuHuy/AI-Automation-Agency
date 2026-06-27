# Chương 04: Soạn thảo Bản Đề xuất Dự án & Hợp đồng B2B an toàn

## 1. Deep Dive (Phân tích chuyên sâu)

### 1. Bản Đề xuất Dự án (Proposal) là gì?
Sau khi gặp mặt và làm việc với khách hàng ở buổi họp đầu tiên để thống nhất yêu cầu (Scoping Session), bạn cần gửi cho họ một bản **Proposal**. Bản tài liệu này hệ thống hóa lại:
- Vấn đề hiện tại của khách hàng.
- Giải pháp đề xuất chi tiết.
- Các mốc thời gian bàn giao (Milestones).
- Chi phí triển khai và phương thức thanh toán.

### 2. Thiết kế Hợp đồng B2B bảo vệ Kỹ sư AI
Khi ký hợp đồng dịch vụ triển khai AI, bạn bắt buộc phải lưu ý các điều khoản pháp lý sau để bảo vệ bản thân:
- **Scope Creep Control (Kiểm soát phạm vi)**: Ghi rõ trong hợp đồng: *"Mọi yêu cầu tính năng phát sinh ngoài phụ lục SOW này sẽ được tính phí bổ sung là 50 USD/giờ làm việc"*.
- **Intellectual Property (Sở hữu trí tuệ)**: Khách hàng sở hữu dữ liệu của họ và sản phẩm cuối cùng. Tuy nhiên, bạn được quyền sở hữu và tái sử dụng các đoạn code thư viện lõi, prompt template chung mà bạn đã tự phát triển từ trước.
- **Limitation of Liability (Giới hạn trách nhiệm)**: Vì AI hoạt động dựa trên xác suất, bạn phải ghi rõ: *"Chúng tôi không chịu trách nhiệm tài chính cho các thiệt hại kinh tế phát sinh trực tiếp từ các câu trả lời sai lệch (hallucination) của AI Agent"* và giới hạn tổng mức bồi thường tối đa bằng số tiền khách hàng đã thanh toán cho hợp đồng.

---

## 2. Demo: Mẫu Phụ lục Phạm vi Công việc (SOW) chuẩn hóa

### Mục tiêu
Cung cấp mẫu phụ lục SOW chi tiết cho dự án AI Chat PDF giúp phân định rõ ràng ranh giới bàn giao, tránh tranh chấp nghiệm thu.

### Nội dung SOW mẫu (`sow_template.md`)
```markdown
# PHỤ LỤC PHẠM VI CÔNG VIỆC (SCOPE OF WORK - SOW)
Dự án: Triển khai Trợ lý ảo tra cứu tài liệu nội bộ (AI Chat PDF)

### 1. Danh sách tính năng bàn giao (In-Scope)
Hệ thống bàn giao bao gồm các tính năng sau:
- **Cổng tải lên tài liệu**: Hỗ trợ tải lên file định dạng `.txt`, dung lượng tối đa 5MB/file.
- **Cơ sở dữ liệu tri thức**: Khởi tạo database ChromaDB lưu trữ cục bộ trên server khách hàng.
- **AI Agent Core**: Tích hợp API GPT-4o-mini thực hiện trích xuất thông tin, trả lời câu hỏi dựa trên tài liệu.
- **Trí nhớ Agent**: Lưu giữ lịch sử 5 lượt chat gần nhất của phiên làm việc.
- **Giao diện Web**: Một trang giao diện Streamlit đơn giản gồm khung chat và sidebar upload file.

### 2. Các phần nằm ngoài phạm vi (Out-of-Scope)
Các tính năng sau KHÔNG nằm trong hợp đồng này (sẽ tính phí bổ sung nếu yêu cầu):
- Hỗ trợ tải lên các định dạng file scan ảnh, file Word (.docx) hoặc file Excel (.xlsx).
- Tích hợp chatbot vào các kênh thứ ba như Fanpage Facebook, Zalo, hoặc Telegram.
- Thiết kế hệ thống phân quyền tài liệu chi tiết cho từng tài khoản nhân viên.

### 3. Kế hoạch nghiệm thu & Thanh toán
- **Đợt 1**: Thanh toán 50% ngay sau khi ký hợp đồng để khởi động dự án.
- **Đợt 2**: Thanh toán 50% còn lại sau khi nghiệm thu chạy thử hệ thống trên máy chủ test và ký biên bản bàn giao bàn giao mã nguồn.
```

---

## 3. Mini Project
Hãy tự viết một bản hợp đồng dịch vụ AI Automation tối giản dài khoảng 1-2 trang giấy, bao gồm các điều khoản cơ bản: Thông tin hai bên, Phạm vi dịch vụ, Chi phí và điều khoản thanh toán, Bảo mật thông tin, và Giới hạn trách nhiệm pháp lý. Lưu file này dưới dạng file Markdown để làm mẫu sử dụng sau này.

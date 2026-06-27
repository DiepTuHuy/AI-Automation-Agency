# Chương 01: Quy trình Khảo sát nghiệp vụ & Thẩm định Dự án (Scoping Session)

## 1. Deep Dive (Phân tích chuyên sâu)

### Mục tiêu của Discovery Session
Trước khi báo giá dự án, bạn bắt buộc phải có ít nhất một buổi họp khảo sát (Discovery Session) dài 45-60 phút với khách hàng. Mục tiêu duy nhất: **Hiểu rõ quy trình thủ công hiện tại của họ hoạt động thế nào và tìm ra nút cổ chai (bottlenecks)**.

### Bộ câu hỏi khảo sát nghiệp vụ chuẩn hóa
Để tránh việc khách hàng nói lan man, hãy hướng dẫn họ trả lời theo 5 nhóm thông tin:
1. **Quy trình thô (As-Is Process)**: *"Anh/chị hãy mô tả chi tiết từng bước từ khi nhận thông tin đầu vào đến khi có kết quả đầu ra. Ai là người làm việc này?"*
2. **Thể tích dữ liệu (Volume)**: *"Mỗi ngày/mỗi tuần bên mình phải xử lý bao nhiêu tác vụ này? (ví dụ: bao nhiêu email, bao nhiêu hóa đơn)"*
3. **Thời gian & Nhân lực**: *"Mỗi tác vụ tốn bao nhiêu phút xử lý? Có bao nhiêu nhân sự chuyên trách làm việc này?"*
4. **Hệ thống hiện tại**: *"Bên mình đang lưu dữ liệu ở đâu? (Google Sheets, Excel, phần mềm CRM chuyên dụng nào? Có hỗ trợ API không?)"*
5. **Nỗi đau lớn nhất**: *"Điểm nào trong quy trình này dễ bị sai sót nhất và khiến anh/chị mệt mỏi nhất?"*

Sau buổi họp, bạn phải vẽ lại được sơ đồ quy trình hiện tại (As-Is) và đề xuất sơ đồ tự động hóa tương lai (To-Be).

---

## 2. Demo: Mẫu Biên bản Khảo sát nghiệp vụ (Discovery Document)

### Mục tiêu
Cung cấp mẫu tài liệu ghi nhận thông tin khảo sát thực tế sau buổi họp để gửi xác nhận lại với khách hàng.

### Nội dung Biên bản mẫu (`discovery_report.md`)
```markdown
# BIÊN BẢN KHẢO SÁT NGHIỆP VỤ - KHÁCH HÀNG: LOGISTICS THÀNH ĐỒNG

- **Ngày thực hiện**: 2026-06-28
- **Người thực hiện**: Huy Diep (AI Automation Architect)
- **Đại diện khách hàng**: Anh Nam (Trưởng phòng Vận hành)

### 1. Hiện trạng quy trình thủ công (As-Is)
1. Nhân viên nhận file hóa đơn PDF từ các đối tác gửi qua Email.
2. Tải file xuống, đọc thông tin bằng mắt: Số hóa đơn, Ngày xuất, Tên đối tác, Tổng tiền, Mã số thuế.
3. Mở phần mềm quản lý kho nội bộ, copy-paste các trường thông tin trên vào hệ thống để tạo phiếu nhập kho.
4. Chụp ảnh màn hình phiếu nhập kho gửi vào nhóm Zalo để kế toán duyệt chi.

### 2. Số liệu thống kê
- Số lượng hóa đơn: Trung bình 80 file/ngày.
- Thời gian xử lý: 6 phút/hóa đơn.
- Số lượng nhân sự: 2 nhân viên văn phòng chuyên trách.
- **Tình trạng**: Nhân viên thường xuyên nhập sai mã số thuế hoặc gõ nhầm số tiền gây lệch sổ sách cuối tháng.

### 3. Giải pháp AI Automation đề xuất (To-Be)
Xây dựng hệ thống n8n kết nối FastAPI OCR:
- n8n tự động quét hòm thư email để nhận file PDF hóa đơn mới.
- Gọi FastAPI OCR sử dụng LLM trích xuất chính xác 100% thông tin hóa đơn ra JSON.
- n8n tự động gọi API của phần mềm kho nội bộ để nhập dữ liệu.
- Gửi tin nhắn duyệt chi tự động kèm ảnh hóa đơn gốc vào nhóm Zalo.
```

---

## 3. Mini Project
Hãy giả lập một buổi khảo sát với một người quen đang làm công việc kinh doanh online hoặc quản lý văn phòng. Hãy đặt câu hỏi, thu thập thông tin và viết một bản Discovery Document tương tự mẫu trên để trình bày giải pháp tự động hóa bằng AI của bạn.

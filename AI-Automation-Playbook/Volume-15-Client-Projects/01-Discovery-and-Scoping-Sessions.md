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

### Bài tập 1: Lập bộ câu hỏi phỏng vấn khảo sát khách hàng (Discovery Questionnaire) (Mức độ: Trung bình)
* **Đề bài**: Hãy soạn thảo bộ 5 câu hỏi trọng tâm dùng để phỏng vấn Giám đốc Vận hành của một công ty Logistics nhằm tìm ra các điểm nghẽn (Pain points) có thể giải quyết bằng tự động hóa AI.
* **Tài liệu sườn mẫu (`discovery_questions.md`)**:
```markdown
# Bộ câu hỏi khảo sát: Ngành Logistics & Vận tải

1. Hiện tại quy trình tiếp nhận thông tin từ vận đơn (Bill of Lading) của công ty đang được thực hiện như thế nào? Có mất nhiều thời gian nhập liệu thủ công không?
2. Bộ phận chăm sóc khách hàng đang tốn bao nhiêu thời gian mỗi ngày để trả lời các câu hỏi về trạng thái hành trình đơn hàng?
3. Công ty đang sử dụng các phần mềm quản lý (ERP, CRM, Excel) nào? Các phần mềm này đã có API kết nối chưa?
4. Đâu là lỗi vận hành xảy ra thường xuyên nhất gây thiệt hại chi phí cho công ty trong 3 tháng qua?
5. Mức ngân sách dự kiến của công ty cho việc nâng cấp tự động hóa hệ thống là bao nhiêu?
```

### Bài tập 2: Lập tài liệu mô tả yêu cầu nghiệp vụ (PRD - Product Requirement Document) (Mức độ: Khó)
* **Đề bài**: Dựa trên câu trả lời giả định của khách hàng Logistics ở Bài tập 1, hãy lập tài liệu mô tả yêu cầu hệ thống (PRD) chi tiết giới thiệu dự án "AI Vận Đơn". PRD cần nêu rõ: Yêu cầu chức năng (Functional Requirements) và Yêu cầu phi chức năng (Non-functional Requirements).
* **Yêu cầu**: Học viên tự hoàn thành không có tài liệu mẫu.
* **Gợi ý triển khai (Workflow Hints)**:
  - Yêu cầu chức năng: AI tự động đọc file PDF vận đơn, trích xuất dữ liệu ra bảng Excel.
  - Yêu cầu phi chức năng: Thời gian xử lý của mô hình dưới 5 giây/hóa đơn, tỷ lệ chính xác trích xuất tối thiểu đạt 98%.


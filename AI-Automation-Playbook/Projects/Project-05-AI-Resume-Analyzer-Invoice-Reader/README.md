# Project 05: AI Resume Analyzer & Invoice Reader

Dự án này là sản phẩm bàn giao thực tế cho khách hàng, kết hợp toàn bộ kiến thức kỹ thuật và quy trình quản lý dự án đã học ở Volume 13, 14 và 15. Hệ thống cung cấp hai cổng dịch vụ độc lập: trích xuất thông tin hóa đơn (Invoice Reader) và phân tích hồ sơ ứng viên (Resume Analyzer) tích hợp giao diện Web và xuất file Excel báo cáo.

---

## 1. Architecture Diagram (Kiến trúc hệ thống)

```
[Người dùng tải lên Hóa đơn / CV] ──> [Streamlit Web UI]
                                            │
                                            ▼
                             [FastAPI Backend /api/v1/extract]
                                            │
                             (Kiểm quét bằng Pydantic Model)
                                            │
                             (OpenAI GPT-4o-mini Structured)
                                            │
                                            ▼
                              [JSON Schema Kết quả] ──> [Đồng bộ lưu file CSV]
```

---

## 2. Source Tree (Cấu trúc mã nguồn)
```
Project-05-AI-Resume-Analyzer-Invoice-Reader/
├── README.md
├── requirements.txt
├── .env.example
├── invoice_sample.txt
└── app.py
```

---

## 3. Deployment Guide (Hướng dẫn triển khai)

### Bước 1: Chuẩn bị môi trường ảo
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Bước 2: Cấu hình biến môi trường
Sao chép `.env.example` thành `.env` và cấu hình:
```env
OPENAI_API_KEY=sk-proj-xxxxxx
```

### Bước 3: Khởi chạy ứng dụng
Chạy giao diện trực quan Streamlit:
```bash
streamlit run app.py
```
*Giao diện Web sẽ mở tại `http://localhost:8501`. Người dùng có thể chọn Tab "Trích xuất Hóa Đơn" hoặc "Phân Tích CV" để sử dụng.*

---

## 4. Lessons Learned (Bài học rút ra)
- **Tận dụng tối đa Pydantic validation**: Định nghĩa rõ ràng kiểu dữ liệu của hóa đơn (Số tiền phải là float, mã số thuế là string) giúp gạt bỏ 99% lỗi khi ghi nhận vào hệ thống kế toán doanh nghiệp.
- **Đóng gói giải pháp**: Thiết kế UI tab đơn giản giúp nâng cao trải nghiệm người dùng cuối không biết code.

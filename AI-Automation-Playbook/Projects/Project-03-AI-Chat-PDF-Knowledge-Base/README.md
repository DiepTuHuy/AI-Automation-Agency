# Project 03: AI Chat PDF & Knowledge Base

Dự án này kết hợp kiến thức từ Volume 07 (Embedding & Vector DB), Volume 08 (RAG) và Volume 09 (AI Agents) để xây dựng một ứng dụng hoàn chỉnh cho phép người dùng tải lên file PDF tài liệu, tự động phân tách và nhúng dữ liệu vào ChromaDB, đồng thời thiết kế một AI Agent có lịch sử trò chuyện (Memory) để trả lời các câu hỏi phức tạp dựa trên tài liệu đó.

---

## 1. Architecture Diagram (Kiến trúc hệ thống)

```
[Người dùng tải lên file PDF] ──> [Đọc văn bản bằng PyPDF2] 
                                            │
                                            ▼
                           [Cắt nhỏ bằng RecursiveCharacterTextSplitter]
                                            │
                                            ▼
                           [Tạo Vector nhúng (OpenAI Embeddings)]
                                            │
                                            ▼
                           [Lưu vào Vector DB (ChromaDB cục bộ)]

[Người dùng chat hỏi] ───────> [AI Agent (ReAct Loop + Memory)]
                                            │
                                            ├─(Công cụ: Lục tìm tài liệu tương đồng trong ChromaDB)
                                            │
                                            ▼
                                [Trả lời chính xác dẫn nguồn]
```

---

## 2. Source Tree (Cấu trúc mã nguồn)
```
Project-03-AI-Chat-PDF-Knowledge-Base/
├── README.md
├── requirements.txt
├── .env.example
├── app.py
└── doc_sample.txt
```

---

## 3. Deployment Guide (Hướng dẫn triển khai)

### Bước 1: Cấu hình môi trường ảo
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Bước 2: Cấu hình biến môi trường
Sao chép `.env.example` thành `.env` và điền:
```env
OPENAI_API_KEY=sk-proj-xxxxxx
```

### Bước 3: Chạy ứng dụng giao diện trực quan
Dự án này sử dụng **Streamlit** để dựng nhanh giao diện UI Web tuyệt đẹp chỉ bằng code Python:
```bash
streamlit run app.py
```
*Mở trình duyệt truy cập `http://localhost:8501` để bắt đầu Chat với PDF*.

---

## 4. Lessons Learned (Bài học rút ra)
- **Tách biệt Ingestion và Query**: Tránh việc nhúng đi nhúng lại file PDF mỗi lần chat. File chỉ cần nhúng 1 lần duy nhất khi upload và lưu đĩa cứng, các lượt chat sau chỉ cần gọi truy vấn.
- **Quản lý lịch sử chat của Agent**: Chèn lịch sử chat vào prompt một cách có chọn lọc giúp Agent không bị quên ngữ cảnh đang thảo luận.

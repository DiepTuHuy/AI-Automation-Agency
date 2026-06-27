# Project 01: AI Meeting Summary & Email Assistant

Dự án này kết hợp kiến thức từ Volume 01, 02 và 03 để xây dựng một công cụ tự động hóa quy trình hậu cuộc họp: đọc hiểu biên bản ghi âm cuộc họp (transcript), tóm tắt các quyết định chính, liệt kê các đầu việc cần làm (action items) của từng người, và tự động sinh bản thảo email gửi cho toàn bộ đội ngũ.

---

## 1. Architecture Diagram (Kiến trúc hệ thống)

```
[meeting_transcript.txt] (Văn bản cuộc họp thô)
           │
           ▼
     [app.py (Python)]
           │
           ├─(tiktoken)──> [Đếm & Tối ưu token]
           │
           ├─(OpenAI API gpt-4o-mini)
           │     ├─ System Prompt: Chuyên gia phân tích hành vi cuộc họp
           │     └─ Structured Output: Pydantic Schema (MeetingSummary)
           │
           ▼
[Output: summary.json] ──> [Sinh Bản Thảo Email] ──> [Lưu email_draft.txt]
```

---

## 2. Source Tree (Cấu trúc mã nguồn)
```
Project-01-AI-Meeting-Summary-Email-Assistant/
├── README.md
├── requirements.txt
├── .env.example
├── meeting_transcript.txt
└── app.py
```

---

## 3. Deployment Guide (Hướng dẫn triển khai)

### Bước 1: Chuẩn bị môi trường
1. Tạo thư mục ảo và kích hoạt:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # Trên macOS/Linux
   # .venv\\Scripts\\activate  # Trên Windows
   ```
2. Cài đặt các thư viện phụ thuộc:
   ```bash
   pip install -r requirements.txt
   ```

### Bước 2: Cấu hình biến môi trường
1. Copy file `.env.example` thành `.env`:
   ```bash
   cp .env.example .env
   ```
2. Điền API Key của bạn vào `.env`:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

### Bước 3: Chạy chương trình
Thực thi lệnh sau trên Terminal:
```bash
python3 app.py
```

---

## 4. Lessons Learned (Bài học rút ra)
- **Tầm quan trọng của Structured Output**: Việc ép cấu hình đầu ra dạng JSON giúp việc đọc thông tin của từng người dễ dàng mà không sợ LLM sinh thêm các câu chào hỏi thừa thãi.
- **Tiết kiệm chi phí bằng cách phân vùng**: Thay vì gửi toàn bộ text dài vô ích, việc lọc bỏ các đoạn hội thoại rác (chào hỏi đầu giờ, đùa cợt) giúp tiết kiệm 20% token.

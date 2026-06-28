# Chương 03: Vẽ sơ đồ Kiến trúc Hệ thống bằng Mermaid.js

## 1. Deep Dive (Phân tích chuyên sâu)

### Tại sao sơ đồ kiến trúc lại quan trọng?
Một bức ảnh có giá trị bằng một vạn lời nói. Khi trình bày giải pháp AI Automation phức tạp cho khách hàng doanh nghiệp:
- Nếu bạn giải thích bằng miệng: *"Chúng tôi nhận webhook rồi gọi FastAPI rồi chạy OpenAI rồi ghi Postgres..."* -> Khách hàng sẽ bị rối và cảm thấy hệ thống không an toàn.
- Nếu bạn đưa ra một sơ đồ khối rõ ràng: Khách hàng sẽ nhìn thấy ngay đường đi của dữ liệu, cấu trúc bảo mật của hệ thống và cảm thấy vô cùng tin tưởng.

### Mermaid.js là gì?
Mermaid.js là một công cụ vẽ sơ đồ bằng mã nguồn (Diagrams-as-Code). Thay vì phải vẽ thủ công trên các công cụ như Photoshop hay PowerPoint rồi xuất file ảnh, bạn chỉ cần viết các câu lệnh text đơn giản. Trình duyệt web và GitHub sẽ tự động biên dịch đoạn text đó thành một sơ đồ trực quan tương tác.

---

## 2. Demo: Các mẫu Sơ đồ thông dụng trong AI Automation

### Mục tiêu
Cung cấp cú pháp mã nguồn Mermaid để vẽ sơ đồ dòng chạy dữ liệu (Flowchart) và sơ đồ tuần tự cuộc gọi API (Sequence Diagram).

### 1. Sơ đồ dòng chạy dữ liệu (Flowchart)
```markdown
```mermaid
graph LR
    User[Khách hàng] -->|1. Gửi câu hỏi| UI[Streamlit Frontend]
    UI -->|2. Tìm kiếm ngữ cảnh| DB[(Vector DB)]
    DB -->|3. Trả về Chunks| UI
    UI -->|4. Gửi Prompt + Chunks| LLM[OpenAI API]
    LLM -->|5. Trả câu trả lời| UI
    UI -->|6. Hiển thị| User
```
```

### 2. Sơ đồ tuần tự cuộc gọi API (Sequence Diagram)
```markdown
```mermaid
sequenceDiagram
    participant User as Người dùng
    participant API as FastAPI Backend
    participant LLM as OpenAI GPT
    participant DB as SQLite DB

    User->>API: POST /api/v1/leads (Gửi Lead)
    Note over API: Pydantic xác thực đầu vào
    API->>LLM: Gửi Prompt chấm điểm
    LLM-->>API: Trả về JSON (is_qualified)
    API->>DB: Ghi dữ liệu khách hàng
    DB-->>API: Trả về ID vừa tạo
    API-->>User: HTTP 200 (Thành công)
```
```

---

## 3. Mini Project

### Bài tập 1: Vẽ sơ đồ kiến trúc hệ thống RAG bằng Mermaid (Mức độ: Trung bình)
* **Đề bài**: Hãy soạn thảo sơ đồ kiến trúc luồng đi của hệ thống RAG (Retrieval-Augmented Generation) bằng cú pháp Mermaid để nhúng trực tiếp vào file tài liệu giới thiệu dự án.
* **Tài liệu sườn mẫu (`architecture.md`)**:
```mermaid
graph LR
    User[Người dùng] -->|Gửi câu hỏi| Orchestrator[AI Orchestrator]
    Orchestrator -->|Tìm kiếm tương đồng| VectorDB[(Chroma Vector DB)]
    VectorDB -->|Trả về tài liệu liên quan| Orchestrator
    Orchestrator -->|Gửi Context + Prompt| Gemini[Gemini API]
    Gemini -->|Trả về câu trả lời| Orchestrator
    Orchestrator -->|Phản hồi kết quả| User
```

### Bài tập 2: Thiết kế sơ đồ kiến trúc hệ thống Multi-Agent phức tạp (Mức độ: Khó)
* **Đề bài**: Vẽ sơ đồ kiến trúc dạng Sequence Diagram bằng Mermaid mô tả luồng giao tiếp tương tác giữa 3 thực thể: Client App, Gateway API, và 2 Sub-Agents chạy nền (Agent Viết nội dung và Agent Phê duyệt). Thể hiện rõ các mốc thời gian gọi công cụ ngoài.
* **Yêu cầu**: Học viên tự hoàn thành không có tài liệu mẫu.
* **Gợi ý triển khai (Workflow Hints)**:
  - Sử dụng từ khóa `sequenceDiagram` trong Mermaid.
  - Sử dụng cấu trúc `participant` để định nghĩa rõ các thực thể trong hệ thống.
  - Vẽ mũi tên có hướng `Actor->>Target: Thông điệp` thể hiện đúng trình tự tương tác từ trên xuống dưới.


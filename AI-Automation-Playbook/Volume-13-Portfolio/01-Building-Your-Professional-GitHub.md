# Chương 01: Thiết lập trang cá nhân GitHub Profile chuyên nghiệp

## 1. Deep Dive (Phân tích chuyên sâu)

### GitHub là sơ yếu lý lịch của Lập trình viên
Trong thế giới công nghệ, một trang hồ sơ cá nhân GitHub Profile hoạt động như một CV trực quan sinh động nhất. Khách hàng hoặc nhà tuyển dụng có thể đánh giá ngay lập tức:
1. **Tác phong làm việc**: Bạn có thường xuyên code không (thể hiện qua Contribution Graph xanh)?
2. **Kỹ năng quản lý**: Bạn có tổ chức thư mục gọn gàng, viết mô tả commit rõ ràng hay viết kịch bản bừa bãi?
3. **Khả năng đóng gói**: Bạn có biết viết tài liệu hướng dẫn cài đặt không?

### Cấu trúc một trang GitHub Profile README thu hút
GitHub cho phép bạn tạo một repository trùng với tên username của bạn để hiển thị một trang giới thiệu bản thân đặc biệt. Trang này nên chứa:
- **Tiêu đề ngắn gọn**: Tên bạn + Định hướng công việc (Ví dụ: "Huy Diep | AI Automation Engineer").
- **Giới thiệu bản thân**: Nêu bật các giải pháp bạn có thể cung cấp cho doanh nghiệp.
- **Kỹ năng chuyên môn**: Hiển thị dạng badges đẹp đẽ (Python, FastAPI, Docker, n8n, LangGraph).
- **Các dự án ghim (Pinned Projects)**: Chọn ra 3-4 dự án chạy thực tế tốt nhất để hiển thị nổi bật.

---

## 2. Demo: Mẫu GitHub Profile README Markdown chuẩn hóa

### Mục tiêu
Cung cấp và giải thích chi tiết cấu trúc mã nguồn file Markdown chuẩn hóa để bạn tự tạo trang giới thiệu cá nhân trên GitHub.

### Mã nguồn (`README.md`)
```markdown
# Xin chào, tôi là Huy Diep 👋

### AI Automation Engineer & Solution Architect

Tôi là kỹ sư chuyên nghiệp chuyên thiết kế và triển khai các hệ thống tự động hóa sử dụng trí tuệ nhân tạo (AI Automation) giúp doanh nghiệp tối ưu hóa vận hành, cắt giảm 80% chi phí xử lý thủ công.

---

### 🛠️ Công cụ & Công nghệ sử dụng
- **AI Brains:** OpenAI API, Anthropic Claude SDK, Gemini API
- **AI Agentic:** LangChain, LangGraph, Model Context Protocol (MCP)
- **Backend & APIs:** Python, FastAPI, RESTful, Pydantic
- **Databases:** SQLite, PostgreSQL, ChromaDB, Redis
- **DevOps & Automation:** Docker, Docker Compose, Linux, Nginx, n8n, GitHub Actions

---

### 📂 Dự án AI Automation Tiêu Biểu
1. **[AI CRM Lead Qualification](https://github.com/username/ai-crm-qualification)**
   - Hệ thống tự động chấm điểm khách hàng tiềm năng bằng AI tích hợp n8n và FastAPI.
   - *Kết quả:* Giúp đội ngũ Sales lọc bỏ 70% leads rác tự động.

2. **[Conversational Chat PDF Agent](https://github.com/username/chat-pdf-knowledge-base)**
   - Trợ lý ảo đọc hiểu và truy vấn chính xác tài liệu nội bộ doanh nghiệp sử dụng ChromaDB RAG.

---

### 📫 Kết nối với tôi
- Email: contact@mydomain.com
- LinkedIn: [linkedin.com/in/username](https://linkedin.com)
```

---

## 3. Mini Project

### Bài tập 1: Chuẩn bị cấu trúc thư mục Dự án trên GitHub (Mức độ: Trung bình)
* **Đề bài**: Hãy thiết lập một thư mục dự án cục bộ theo chuẩn cấu hình kho lưu trữ (Repository) chuyên nghiệp trên GitHub, bao gồm đầy đủ tệp `.gitignore`, file cấu hình môi trường mẫu `.env.example`, và file `requirements.txt`.
* **Tài liệu sườn mẫu cấu trúc thư mục**:
```markdown
# Cấu trúc thư mục dự án chuẩn hóa

my-ai-agent-project/
├── .gitignore          # Chứa danh sách các file bỏ qua (như .env, __pycache__)
├── .env.example        # File cấu hình môi trường mẫu không chứa API Key thật
├── requirements.txt    # Danh sách các thư viện Python phụ thuộc cần cài đặt
├── main.py             # File chạy chính của chương trình
└── README.md           # Tài liệu hướng dẫn sử dụng dự án
```

### Bài tập 2: Cấu hình quy trình Git Workflow bảo vệ nhánh chính (Mức độ: Khó)
* **Đề bài**: Tạo repository trên GitHub. Thực hiện thiết lập luật bảo vệ nhánh chính (Branch Protection Rules): Chặn việc push trực tiếp lên nhánh `main`, bắt buộc toàn bộ code mới phải đi qua nhánh phụ và thực hiện Pull Request (PR) kèm theo xét duyệt của ít nhất 1 thành viên khác trước khi merge.
* **Yêu cầu**: Học viên tự hoàn thành không có tài liệu mẫu.
* **Gợi ý triển khai (Workflow Hints)**:
  - Truy cập vào mục Settings -> Branches trên trang GitHub Repository của bạn.
  - Chọn "Add branch protection rule" và nhập tên nhánh `main`.
  - Tích chọn "Require a pull request before merging" và lưu lại.


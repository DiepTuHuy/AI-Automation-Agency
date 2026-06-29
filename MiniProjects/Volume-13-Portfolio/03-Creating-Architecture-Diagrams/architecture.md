graph LR
    User[Người dùng] -->|Gửi câu hỏi| Orchestrator[AI Orchestrator]
    Orchestrator -->|Tìm kiếm tương đồng| VectorDB[(Chroma Vector DB)]
    VectorDB -->|Trả về tài liệu liên quan| Orchestrator
    Orchestrator -->|Gửi Context + Prompt| Gemini[Gemini API]
    Gemini -->|Trả về câu trả lời| Orchestrator
    Orchestrator -->|Phản hồi kết quả| User
# Chương 04: Lập trình Đa tác nhân (Multi-Agent) bằng LangGraph

## 1. Deep Dive (Phân tích chuyên sâu)

### Tại sao cần hệ thống Đa tác nhân (Multi-Agent)?
Khi ứng dụng của bạn mở rộng (ví dụ: một trợ lý ảo vận hành cả một startup tự động), một Agent đơn lẻ chứa quá nhiều prompt chỉ dẫn và công cụ sẽ bắt đầu bị rối, gọi sai công cụ hoặc quên quy tắc.

Giải pháp là chia để trị: xây dựng một đội ngũ các Agent chuyên biệt.
- **Node (Nút)**: Đại diện cho một Agent (hoặc một hàm xử lý). Mỗi node nhận trạng thái hiện tại (State), thực thi logic của mình, và ghi đè kết quả mới vào State.
- **Edge (Cạnh)**: Định tuyến luồng chạy giữa các node. Có thể là cạnh tĩnh (Node A luôn sang Node B) hoặc cạnh điều kiện (Conditional Edge: Node A kiểm tra chất lượng, nếu tốt sang Node C, nếu lỗi quay lại Node B).
- **State (Trạng thái)**: Đối tượng bộ nhớ dùng chung chứa toàn bộ lịch sử trò chuyện và các biến dùng chung để các Node đọc ghi dữ liệu đồng bộ.

---

## 2. Demo: Đồ thị Duyệt bài viết tự động (Writer & Editor Graph)

### Mục tiêu
Xây dựng một hệ thống đa tác nhân gồm: Agent Writer (Viết bài) -> chuyển sang Agent Editor (Biên tập). Agent Editor kiểm tra xem bài viết có chứa từ nhạy cảm không, nếu có bắt Writer viết lại, nếu sạch sẽ cho phép xuất bản.

### Sơ đồ luồng hoạt động
```
[Start] ──> [Writer Node (Viết bài)] ──> [Editor Node (Kiểm tra)]
                                              │
                                       (Có từ nhạy cảm?)
                                        ├── Yes ──> [Quay lại Writer Node]
                                        └── No ───> [End: Xuất bản]
```

### Mã nguồn (`langgraph_demo.py`)
Yêu cầu cài đặt: `pip install langgraph`

```python
from typing import TypedDict, List
from langgraph.graph import StateGraph, START, END

# 1. Định nghĩa đối tượng Trạng thái dùng chung của Đồ thị (State)
class AgentState(TypedDict):
    topic: str
    article: str
    feedback: str
    revision_count: int

# 2. Định nghĩa Node 1: Writer Agent
def writer_node(state: AgentState):
    print("\n[Writer] Đang viết bài...")
    revision = state.get("revision_count", 0)
    topic = state["topic"]
    
    if revision == 0:
        article = f"Đây là một bài viết tuyệt vời về {topic}. AI sẽ thay đổi tương lai."
    else:
        article = f"Đây là bài viết đã được chỉnh sửa về {topic}. Công nghệ tự động hóa AI mang lại giá trị lớn."
        
    return {
        "article": article,
        "revision_count": revision + 1
    }

# 3. Định nghĩa Node 2: Editor Agent
def editor_node(state: AgentState):
    print("[Editor] Đang biên tập bài viết...")
    article = state["article"]
    
    # Luật: Không được chứa từ nhạy cảm 'tương lai' (giả lập lỗi)
    if "tương lai" in article.lower() and state["revision_count"] < 2:
        return {
            "feedback": "Bài viết chứa từ nhạy cảm 'tương lai'. Hãy viết lại!"
        }
    return {"feedback": "approved"}

# 4. Định nghĩa Edge điều kiện phân nhánh
def route_after_editor(state: AgentState):
    if state["feedback"] == "approved":
        return "end"
    return "writer"

if __name__ == "__main__":
    # 5. Khởi tạo Đồ thị trạng thái
    workflow = StateGraph(AgentState)
    
    # 6. Thêm các Node vào đồ thị
    workflow.add_node("writer", writer_node)
    workflow.add_node("editor", editor_node)
    
    # 7. Thiết lập các kết nối (Edges)
    workflow.add_edge(START, "writer")
    workflow.add_edge("writer", "editor")
    
    # Thêm cạnh điều kiện rẽ nhánh từ Editor
    workflow.add_conditional_edges(
        "editor",
        route_after_editor,
        {
            "writer": "writer",
            "end": END
        }
    )
    
    # 8. Biên dịch đồ thị thành ứng dụng chạy được
    app = workflow.compile()
    
    # 9. Chạy thử nghiệm đồ thị
    initial_state = {"topic": "AI Automation"}
    result = app.invoke(initial_state)
    
    print("\n=== KẾT QUẢ CUỐI CÙNG ===")
    print(f"Bài viết xuất bản: {result['article']}")
```

---

## 3. Mini Project
Hãy vẽ sơ đồ khối kiến trúc của hệ thống Writer & Editor phía trên bằng Mermaid.js (Tìm hiểu cú pháp sơ đồ Mermaid) và chèn đoạn code Mermaid đó vào file Markdown báo cáo.

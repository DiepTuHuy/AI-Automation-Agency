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

### Bài tập 1: Mô phỏng hệ thống Multi-Agent biên dịch và sửa bài viết (Mức độ: Trung bình)
* **Đề bài**: Viết một script Python giả lập kiến trúc Multi-Agent đơn giản gồm 2 Agent: Agent 1 (Translator) dịch bài đăng từ tiếng Anh sang tiếng Việt, Agent 2 (Editor) nhận kết quả từ Agent 1 để sửa lỗi chính tả và làm mượt văn phong.
* **Mã nguồn mẫu (`multi_agent_pipeline.py`)**:
```python
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

class MultiAgentSystem:
    def __init__(self):
        self.model = genai.GenerativeModel("gemini-2.5-flash")
        
    def agent_translator(self, text: str) -> str:
        prompt = f"Dịch đoạn văn bản sau sang tiếng Việt sát nghĩa nhất:\n\n{text}"
        res = self.model.generate_content(prompt)
        return res.text.strip()
        
    def agent_editor(self, translated_text: str) -> str:
        prompt = f"Hãy sửa lỗi chính tả, ngữ pháp và tối ưu văn phong cho đoạn dịch sau tự nhiên hơn:\n\n{translated_text}"
        res = self.model.generate_content(prompt)
        return res.text.strip()
        
    def run_pipeline(self, english_text: str) -> str:
        print("-> Agent 1 (Translator) đang dịch bài...")
        translated = self.agent_translator(english_text)
        print("-> Agent 2 (Editor) đang tinh chỉnh bản dịch...")
        final_output = self.agent_editor(translated)
        return final_output

if __name__ == "__main__":
    system = MultiAgentSystem()
    input_text = "AI agents are transforming how we build software today."
    output = system.run_pipeline(input_text)
    print("\nKết quả cuối cùng:")
    print(output)
```

### Bài tập 2: Hệ thống phản hồi đa tác nhân có vòng phản hồi (Feedback Loop) (Mức độ: Khó)
* **Đề bài**: Xây dựng kiến trúc Multi-Agent có vòng kiểm duyệt chéo: Agent 1 viết bài đăng quảng cáo sản phẩm. Agent 2 (Reviewer) đọc bài viết và đưa ra nhận xét sửa đổi. Agent 1 nhận phản hồi từ Agent 2, tự động sửa đổi bài đăng và xuất ra phiên bản hoàn thiện cuối cùng.
* **Yêu cầu**: Học viên tự hoàn thành không có code mẫu.
* **Gợi ý triển khai (Workflow Hints)**:
  - Thiết kế vòng lặp giao tiếp giữa Agent 1 và Agent 2.
  - Thiết lập điều kiện dừng: Nếu Agent 2 đánh giá bài viết đạt từ 8/10 điểm trở lên, kết thúc vòng lặp và in ra kết quả.
  - Cấu hình `temperature = 0.5` cho Agent viết để tăng tính sáng tạo từ vựng.

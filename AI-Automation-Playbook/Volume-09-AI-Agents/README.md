# Volume 09: AI Agents - Thiết Kế Hệ Thống Tự Hành Bậc Cao

Một chatbot RAG tĩnh hay một workflow n8n chỉ có thể đi theo một luồng công việc được xác định cứng từ trước. Khi gặp các bài toán đòi hỏi sự linh hoạt, tự động ra quyết định, phân chia công việc cho các phòng ban hoặc tự sửa sai khi gặp lỗi, bạn cần đến **AI Agents (Trợ lý tự hành)**. Volume này là đỉnh cao của chuỗi kiến thức AI thực chiến: bạn sẽ học cách thiết kế cấu trúc Agent (ReAct, Planning, Memory), tích hợp công cụ (Function Calling) và xây dựng hệ thống đa tác nhân (Multi-Agent) sử dụng thư viện hàng đầu **LangGraph**.

---

## 1. Learning Objectives (Mục tiêu học tập)
Sau khi hoàn thành Volume này, bạn sẽ:
- **Phân biệt Agentic và Linear**: Hiểu rõ sự khác biệt giữa Agentic Workflow (ra quyết định động, lặp) và luồng tuyến tính tĩnh.
- **Làm chủ Trí nhớ Agent**: Thiết kế thành thạo Short-term memory (trong context window) và Long-term memory (lưu database).
- **Tích hợp Công cụ (Function Calling)**: Lập trình cho LLM khả năng tự nhận diện và gọi các hàm Python bên ngoài để tương tác vật lý.
- **Xây dựng Đa tác nhân (Multi-Agent)**: Thiết kế và vận hành các đồ thị trạng thái phức tạp bằng LangGraph.
- **Tự sửa sai (Self-Correction)**: Cấu hình Agent tự phát hiện mã lỗi hoặc kết quả sai và tự sửa đổi prompt chạy lại đến khi đúng.

---

## 2. Prerequisites (Điều kiện tiên quyết)
- Hoàn thành Volume 07 (Vector Database) và Volume 08 (RAG).
- Thành thạo lập trình Python hướng đối tượng.

---

## 3. Big Picture (Bức tranh tổng thể)
AI Agent là một chu kỳ lặp khép kín: Nhận thức (câu hỏi) -> Lập kế hoạch (suy nghĩ) -> Hành động (gọi công cụ) -> Quan sát kết quả -> Lặp lại đến khi hoàn thành mục tiêu.

```
                  ┌────────────────────────┐
                  ▼                        │
[User Goal] ──> [LLM Brain: Planning] ──> [Action: Call Tools] 
                                           │
                                           ▼ (Execute tool)
                                    [Observation: Result]
```

---

## 4. First Principles (Nguyên lý gốc)
- **Agent không phải là ma thuật**: Agent thực chất là một vòng lặp `while` chạy liên tục, gửi prompt tới LLM yêu cầu: *"Hãy cho tôi biết bước tiếp theo cần làm gì?"* và thực thi lệnh Python tương ứng.
- **Công cụ là mở rộng của mô hình**: LLM bị giới hạn khả năng tính toán và cập nhật. Bằng cách cho LLM dùng công cụ (như Calculator, Web Search, Database Reader), ta giải phóng hoàn toàn giới hạn năng lực của nó.
- **Trạng thái là sợi dây liên kết**: Trong hệ thống đa tác nhân, các Agent giao tiếp với nhau bằng cách đọc và ghi chung vào một đối tượng bộ nhớ trạng thái duy nhất (State).

---

## 5. Mental Models (Mô hình tư duy)
- **Vòng lặp ReAct (Reason + Act)**: Hãy tưởng tượng bạn đang lắp ráp một chiếc tủ gỗ IKEA phức tạp mà không có sách hướng dẫn.
  - *Bước 1 (Reason - Suy nghĩ)*: Bạn nhìn vào đống gỗ và nghĩ: *"Mình cần tìm 4 chiếc chân tủ trước"*.
  - *Bước 2 (Act - Hành động)*: Bạn lục tìm trong hộp và lấy ra 4 thanh gỗ ngắn (Gọi công cụ).
  - *Bước 3 (Observe - Quan sát)*: Bạn đếm lại: *"Đủ 4 chiếc chân tủ rồi"*.
  - *Bước 4 (Reason)*: Bạn nghĩ tiếp: *"Bây giờ mình cần vít để bắt chúng vào mặt bàn tủ"*.
  Chu trình Suy nghĩ -> Hành động -> Quan sát lặp đi lặp lại đến khi chiếc tủ hoàn thành. Đó là ReAct.

---

## 6. Core Concepts (Khái niệm cốt lõi)
1. **Function Calling (Gọi hàm)**: Tính năng của LLM cho phép trả về tên hàm và các tham số đầu vào ở định dạng JSON để code Python thực thi, thay vì trả về text tự do.
2. **LangGraph**: Thư viện xây dựng ứng dụng Agentic dưới dạng đồ thị có hướng (Graphs), trong đó mỗi Node là một hàm xử lý, mỗi Edge là đường dẫn logic phân luồng, hỗ trợ lưu trữ trạng thái cực kỳ mạnh mẽ.
3. **Short-Term Memory**: Quản lý lịch sử chat của phiên hiện tại dưới dạng danh sách các tin nhắn gửi nhận.

---

## 8. Best Practices (Quy chuẩn thực chiến)
- **Thiết kế công cụ tối giản**: Khai báo mô tả công cụ (Tool Description) rõ ràng, chi tiết vì LLM hoàn toàn dựa vào đoạn mô tả này để quyết định có chọn công cụ đó hay không.
- **Đặt giới hạn vòng lặp tối đa (Max Iterations)**: Luôn đặt biến `max_iterations = 5` hoặc `10` trong vòng lặp của Agent. Tránh việc Agent bị kẹt vào vòng lặp vô tận (loop) gọi API liên tục làm cạn kiệt tài khoản của bạn trong 5 phút.
- **Sử dụng State Graph có kiểm soát**: Tránh cấu hình Agent tự do hoàn toàn (Fully Autonomous). Hãy thiết kế đồ thị LangGraph có các đường rẽ nhánh rõ ràng để dễ kiểm soát luồng chạy của hệ thống.

---

## 9. Common Mistakes (Sai lầm thường gặp)
- **Giả định LLM tự chạy được code**: Viết prompt: *"Hãy chạy hàm Python sau..."* mà không thiết lập parser và Executor bên phía Python code. LLM chỉ có thể viết code hoặc sinh tham số JSON, việc chạy code phải do máy chủ của bạn thực hiện.
- **Thiếu Human-in-the-loop cho các tác vụ nhạy cảm**: Cho phép Agent tự động gửi email trực tiếp cho khách hàng hoặc thực hiện giao dịch chuyển tiền mà không có nút bấm duyệt của con người. *Cách sửa*: Thiết kế một cổng chờ duyệt (Approval Node) trên LangGraph.

---

## 10. Engineering Mindset (Tư duy kỹ sư)
Một Kỹ sư Agent chuyên nghiệp không xây dựng một Agent vạn năng làm được mọi việc. Họ chia nhỏ bài toán thành các tác nhân chuyên biệt (Specialist Agents) có nhiệm vụ rõ ràng (ví dụ: Writer Agent chuyên viết, Editor Agent chuyên kiểm lỗi, Researcher Agent chuyên tìm thông tin) và điều phối họ làm việc nhóm với nhau.

---

## 13. Capstone Project (Dự án kết khóa Volume)
Xem mô tả chi tiết tại [Project-03](file:///Users/dieptuhuy/Documents/AI%20Automation/AI-Automation-Playbook/Projects/Project-03-AI-Chat-PDF-Knowledge-Base/README.md).

---

## 14. Review Questions (Bloom Taxonomy - 30 câu hỏi)
### Level 1 — Remember (Nhớ)
1. AI Agent là gì?
2. Sự khác biệt chính giữa Agent và Chatbot thông thường là gì?
3. ReAct là viết tắt của hai từ gì trong Prompt Engineering?
4. Function Calling là gì?
5. LangGraph là thư viện do công ty nào phát triển?

### Level 2 — Understand (Hiểu)
6. Giải thích cách một mô hình LLM quyết định gọi một công cụ cụ thể dựa trên thông tin mô tả công cụ (Tool Definition).
7. Tại sao lập trình Agentic Workflow lại đạt tỷ lệ thành công cao hơn việc gọi một prompt đơn lẻ đối với các bài toán phức tạp?
8. Phân biệt Short-term Memory và Long-term Memory của một AI Agent.
9. Trong đồ thị LangGraph, Node và Edge đại diện cho các thành phần nào trong mã nguồn Python?
10. Giải thích cơ chế kiểm duyệt của con người (Human-in-the-loop) trong luồng chạy đồ thị LangGraph.

### Level 3 — Apply (Áp dụng)
11. Định nghĩa một Tool Schema bằng Python dictionary để khai báo hàm tính toán chi phí lãi suất ngân hàng.
12. Viết vòng lặp `while` cơ bản mô phỏng cơ chế ReAct nhận diện kết quả từ LLM và gọi hàm Python tương ứng.
13. Khởi tạo một đồ thị LangGraph đơn giản gồm 2 Node kết nối tuần tự.
14. Cấu hình một Edge điều kiện (Conditional Edge) rẽ nhánh dựa trên biến trạng thái của đồ thị.
15. Thiết lập mã nguồn giới hạn số lượt lặp tối đa của Agent bằng 5 để chống loop vô hạn.

### Level 4 — Analyze (Phân tích)
16. Phân tích sự đánh đổi về chi phí API và thời gian phản hồi (latency) khi chuyển đổi từ một Chatbot RAG tĩnh sang một Agent sử dụng ReAct.
17. So sánh hiệu năng của việc chạy Multi-Agent song song với chạy tuần tự trong bài toán lập trình và kiểm thử code tự động.
18. Phân tích nguyên nhân khiến Agent quyết định gọi sai công cụ hoặc bị kẹt vào vòng lặp gọi đi gọi lại một công cụ duy nhất.
19. Đánh giá mức độ an toàn bảo mật khi cho phép AI Agent truy cập trực tiếp vào công cụ thực thi dòng lệnh terminal (`Bash Tool`).
20. Tại sao việc quản lý Trạng thái (State) trong LangGraph lại giúp giải quyết bài toán mất lịch sử hội thoại khi phân nhánh Agent?

### Level 5 — Design (Thiết kế)
21. Thiết kế kiến trúc hệ thống Multi-Agent hỗ trợ khách hàng: Agent Router phân loại câu hỏi -> Chuyển tiếp tới Technical Agent hoặc Billing Agent chuyên biệt.
22. Đề xuất sơ đồ đồ thị LangGraph có cơ chế tự sửa lỗi (Self-Correction): Agent viết code -> Node chạy thử code gặp lỗi -> Edge điều kiện phát hiện lỗi và chuyển lại Node viết code kèm log lỗi để sửa.
23. Thiết kế công cụ tích hợp cho phép AI Agent truy vấn thông tin tồn kho trực tiếp từ database SQL.
24. Đề xuất quy trình lưu trữ và tải lại Trí nhớ dài hạn (Long-term memory) của khách hàng dựa trên ID người dùng qua mỗi phiên chat mới.
25. Thiết kế kịch bản Agent nghiên cứu thị trường tự động: Quét Google Search lấy 10 link -> Đọc nội dung từng link -> Tổng hợp báo cáo Markdown -> Gửi Slack.

### Level 6 — Evaluate (Đánh giá)
26. Đánh giá hiệu quả kinh tế và độ ổn định của việc xây dựng hệ thống đa tác nhân bằng LangGraph so với việc sử dụng framework CrewAI hay Autogen.
27. Đánh giá tính khả thi khi triển khai hệ thống Agent tự động hóa 100% quy trình xuất hóa đơn và thanh toán tài chính cho doanh nghiệp B2B.
28. Kiểm chứng chất lượng đầu ra của một Agent viết bài quảng cáo bằng cách thiết lập Agent phê bình (Critic Agent) chấm điểm và kiểm thử 20 bài viết khác nhau.
29. Đánh giá rủi ro đạo đức và pháp lý khi một AI Agent tự động quyết định khóa tài khoản khách hàng khi phát hiện dấu hiệu gian lận.
30. Lập luận bác bỏ hoặc đồng ý với quan điểm: *"AI Agent có khả năng tự lập kế hoạch sẽ thay thế hoàn toàn công việc của các Project Manager và Business Analyst trong tương lai"*.

---

## 15. Checklist hoàn thành
- [ ] Hiểu rõ chu trình hoạt động của Agent và ReAct loop.
- [ ] Thực hiện thành công Function Calling gọi hàm Python cục bộ từ LLM.
- [ ] Xây dựng được Agent có trí nhớ lịch sử hội thoại ổn định.
- [ ] Viết và vận hành được đồ thị StateGraph cơ bản bằng LangGraph.
- [ ] Hoàn thành Capstone Project (Project 03).

---

## 16. Resources (Tài liệu tham khảo)
- **LangGraph**: [LangGraph Developer Guide](https://langchain-ai.github.io/langgraph/)
- **Học thuật**: *"ReAct: Synergizing Reasoning and Acting in Language Models"* (Yao et al., 2022) - Paper nền tảng.
- **Khóa học**: *AI Agents in Creative Workflows by DeepLearning.AI.*

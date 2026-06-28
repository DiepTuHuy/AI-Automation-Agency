# Volume 02: Prompt Engineering - Nghệ thuật Giao tiếp & Định hình Tư duy AI

Prompt Engineering không phải là việc "thử và sai" một cách vô định hướng. Đây là bộ môn kỹ thuật thực sự liên quan đến thiết kế ngữ cảnh, định hình cấu trúc dữ liệu và điều hướng logic suy luận của LLM để đạt được kết quả đầu ra có độ tin cậy 99% trong môi trường Production.

---

## 1. Learning Objectives (Mục tiêu học tập)
Sau khi hoàn thành Volume này, bạn sẽ:
- **Làm chủ kỹ thuật cốt lõi**: Thành thạo Zero-shot, Few-shot và Chain of Thought (CoT).
- **Thiết kế System Prompt chuẩn doanh nghiệp**: Xây dựng được các Agent Role hoạt động ổn định và bảo mật cao.
- **Trích xuất dữ liệu có cấu trúc**: Trích xuất dữ liệu từ văn bản thô ra JSON chính xác 100% bằng JSON Mode và Pydantic.
- **Đảm bảo an toàn**: Thiết kế các rào chắn chống tấn công Prompt Injection (đè lệnh).

---

## 2. Prerequisites (Điều kiện tiên quyết)
- Hoàn thành Volume 01.
- Hiểu rõ khái niệm Tokens và Context Window.

---

## 3. Big Picture (Bức tranh tổng thể)
Trong Production, Prompt đóng vai trò như mã nguồn logic. Nó định hình hành vi của AI trước khi AI được kết nối với các API và Cơ sở dữ liệu khác. Một prompt tốt làm giảm nhu cầu lập trình hậu xử lý (Post-processing code).

```
[Raw User Input] 
       │
       ▼
[System Prompt Wrapper (Roles + Constraints + Examples + JSON Schema)]
       │
       ▼
 [LLM Reasoning] ────> [Valid Structured JSON] ────> [API / Database]
```

---

## 4. First Principles (Nguyên lý gốc)
- **Rõ ràng triệt tiêu mơ hồ (Specificity Over Ambiguity)**: LLM không có khả năng đọc vị ý nghĩ của bạn. Mọi chỉ dẫn mơ hồ đều dẫn đến kết quả ngẫu nhiên.
- **Show, Don't Tell (Đưa ví dụ thay vì định nghĩa)**: Cung cấp 2-3 ví dụ thực tế (Few-shot) luôn mang lại hiệu quả định dạng tốt hơn việc viết hàng nghìn từ mô tả lý thuyết.
- **Phân rã logic (Divide and Conquer)**: Bắt LLM giải bài toán lớn ngay lập tức sẽ tăng tỷ lệ lỗi. Hãy bắt nó chia nhỏ bài toán và viết ra các bước suy luận trước khi đưa ra kết quả cuối cùng.

---

## 5. Mental Models (Mohình tư duy)
- **Tư duy Thư ký mới tuyển (The Junior Intern)**: Hãy coi LLM giống như một thực tập sinh thông minh nhưng chưa có kinh nghiệm thực tế. Bạn cần hướng dẫn họ: làm việc gì, làm như thế nào, xem ví dụ ở đâu, định dạng báo cáo ra sao và phải xử lý thế nào nếu gặp lỗi.
- **Bảng chỉ dẫn phân luồng (Railroad Track)**: Hãy xây dựng các quy tắc ràng buộc chặt chẽ trong prompt để hướng dòng suy nghĩ của LLM đi đúng đường ray mong muốn, không cho phép nó đi lạc sang các chủ đề khác.

---

## 6. Core Concepts (Khái niệm cốt lõi)
1. **Few-Shot Prompting**: Kỹ thuật cung cấp một vài ví dụ minh họa về cặp (Input, Output) trong prompt để định hình hành vi và định dạng của mô hình.
2. **Chain of Thought (CoT)**: Kỹ thuật kích hoạt khả năng suy luận logic của LLM bằng cách yêu cầu mô hình giải thích từng bước giải quyết vấn đề trước khi đưa ra câu trả lời cuối cùng.
3. **Structured Output (Pydantic/Function Calling)**: Cơ chế bắt buộc LLM trả về kết quả tuân theo cấu trúc JSON định hình trước (JSON Schema) để code hệ thống có thể đọc hiểu trực tiếp mà không bị lỗi cú pháp.

---

## 8. Best Practices (Quy chuẩn thực chiến)
- **Đặt phân tách rõ ràng (Delimiters)**: Sử dụng các dấu phân tách như `"""`, `---`, `<xml-tags>` để giúp LLM phân biệt rạch ròi đâu là chỉ thị (Instruction), đâu là dữ liệu đầu vào (Input Data).
- **Luôn yêu cầu giải thích trước, kết luận sau**: Đảm bảo LLM đi qua các bước suy luận (CoT) trước khi đưa ra kết quả. Nếu đưa kết quả trước, mô hình rất dễ bị sai do không có không gian suy luận (Compute-on-demand).
- **Tách biệt System và User Prompt**: Luôn đặt các chỉ thị cấu hình cốt lõi vào System Prompt, và chỉ đặt dữ liệu người dùng gửi vào User Prompt để ngăn chặn Prompt Injection.

---

## 9. Common Mistakes (Sai lầm thường gặp)
- **Viết Prompt phủ định**: Viết *"Không được dùng từ chuyên ngành"* thay vì chỉ định rõ *"Hãy sử dụng ngôn từ phổ thông dễ hiểu cho học sinh lớp 5"*. *Cách sửa*: Tập trung vào những gì AI NÊN làm.
- **Sử dụng Regex để parse JSON từ văn bản tự do của LLM**: Rất dễ gãy do LLM đôi khi chèn thêm các ký tự markdown như \`\`\`json ở đầu và cuối. *Cách sửa*: Sử dụng thư viện hỗ trợ Structured Output của OpenAI/Pydantic để kiểm soát định dạng tự động.

---

## 10. Engineering Mindset (Tư duy kỹ sư)
Một kỹ sư Prompt không viết prompt dựa trên cảm tính. Họ lưu trữ prompt trong code, thiết kế các bộ testcases để kiểm nghiệm độ ổn định của prompt qua nhiều lần chạy (Prompt Evaluation), và phiên bản hóa (version control) prompt giống như phiên bản hóa source code.

---

## 13. Capstone Project (Dự án kết khóa Volume)
Thiết kế hệ thống phân loại và trích xuất thông tin tự động từ các email phản hồi khách hàng (Customer Feedback Parser). Hệ thống phải phân loại phản hồi thành 4 loại (Lỗi kỹ thuật, Yêu cầu hoàn tiền, Khen ngợi, Hỏi giá), tự động trích xuất các thông tin: Tên khách hàng, Mã đơn hàng, Chi tiết lỗi, và mức độ khẩn cấp (Thấp, Trung bình, Cao). Đầu ra bắt buộc phải là một đối tượng JSON chuẩn định hình bởi Pydantic.

---

## 14. Review Questions (Bloom Taxonomy - 30 câu hỏi)
### Level 1 — Remember (Nhớ)
1. Zero-shot prompting là gì?
2. Chain of Thought (CoT) là gì và câu lệnh kích hoạt phổ biến nhất của nó là gì?
3. Prompt Injection là gì?
4. Ký tự phân tách (Delimiter) là gì và cho ví dụ?
5. JSON Schema là gì?

### Level 2 — Understand (Hiểu)
6. Giải thích sự khác biệt giữa Zero-shot và Few-shot prompting. Khi nào nên dùng Few-shot?
7. Tại sao yêu cầu LLM đưa ra câu trả lời ngay lập tức (không qua suy luận từng bước) lại làm tăng khả năng bị lỗi logic?
8. Tại sao System Prompt lại có mức độ ưu tiên và quyền kiểm soát hành vi mô hình cao hơn User Prompt?
9. Phân biệt sự khác nhau giữa JSON Mode cơ bản và Structured Outputs (sử dụng JSON Schema/Pydantic).
10. Tại sao việc sử dụng các thẻ định dạng dạng XML (ví dụ: `<context></context>`) lại hiệu quả đối với các mô hình của Anthropic hay OpenAI?

### Level 3 — Apply (Áp dụng)
11. Viết một prompt sử dụng kỹ thuật Few-shot để chuẩn hóa định dạng số điện thoại từ nhiều nguồn khác nhau về chuẩn quốc tế `+84`.
12. Thiết kế một System Prompt để cấu hình AI đóng vai trò là một Code Reviewer khó tính, chỉ ra lỗi bảo mật và đề xuất cách tối ưu.
13. Sử dụng thư viện Pydantic định nghĩa một class chứa thông tin ứng viên (Họ tên, Năm sinh, Email, Kỹ năng) và viết code Python gọi OpenAI API yêu cầu trả về đúng schema này.
14. Áp dụng kỹ thuật Chain of Thought để bắt AI giải thích bài toán chia tài sản thừa kế phức tạp.
15. Viết một prompt có khả năng phòng thủ trước nỗ lực của người dùng nhằm bắt AI tiết lộ System Prompt gốc.

### Level 4 — Analyze (Phân tích)
16. Phân tích tại sao việc chèn ví dụ sai (bad examples) trong Few-shot prompt lại làm giảm sút nghiêm trọng hiệu năng suy luận của LLM.
17. Đánh giá sự khác biệt về kết quả và thời gian phản hồi (latency) của một prompt khi bật và tắt cơ chế Chain of Thought.
18. Phân tích cơ chế hoạt động của cuộc tấn công "Jailbreaking" và tại sao các giải pháp Prompt Engineering thông thường khó phòng chống triệt để.
19. Đánh giá tính ổn định của việc ép định dạng đầu ra bằng Prompt so với việc dùng API hỗ trợ Structured Outputs của nhà cung cấp.
20. Tại sao các mô hình có kích thước nhỏ (như GPT-4o-mini) cần nhiều ví dụ Few-shot hơn để đạt cùng độ chính xác định dạng so với mô hình lớn?

### Level 5 — Design (Thiết kế)
21. Thiết kế một hệ thống Prompt hai bước (Chain of Prompts): Bước 1 lọc thông tin nhạy cảm, Bước 2 sinh câu trả lời.
22. Đề xuất kiến trúc kiểm thử Prompt (Prompt Evaluation Pipeline) để đo lường độ chính xác của Prompt khi thay đổi phiên bản.
23. Thiết kế cấu trúc Prompt tối ưu cho bài toán dịch thuật đa ngôn ngữ giữ nguyên các biến code (như `{user_name}`, `{booking_id}`).
24. Đề xuất quy trình xử lý lỗi tự động (Error Handling) khi LLM trả về chuỗi JSON bị lỗi cú pháp không thể parse.
25. Thiết kế prompt cho một chatbot tư vấn luật pháp đảm bảo AI luôn dẫn nguồn điều luật cụ thể và từ chối trả lời nếu nằm ngoài phạm vi luật dân sự.

### Level 6 — Evaluate (Đánh giá)
26. Đánh giá hiệu quả kinh tế và kỹ thuật của việc chuyển đổi từ cấu hình Prompt phức tạp (nhiều Few-shot) sang Fine-tuning mô hình nhỏ hơn.
27. Lập luận phản bác quan điểm: *"Prompt Engineering chỉ là giải pháp tạm thời, tương lai AI sẽ tự hiểu người dùng muốn gì mà không cần kỹ thuật prompt"*.
28. Kiểm chứng chất lượng của một Prompt trích xuất thông tin qua 100 mẫu thử nghiệm khác nhau và đưa ra báo cáo tỷ lệ gãy (Error Rate).
29. Đánh giá các nguy cơ về an toàn thông tin khi cho phép người dùng tự do nhập dữ liệu đầu vào trực tiếp cho LLM mà không qua lớp làm sạch dữ liệu.
30. Đánh giá mức độ đóng góp của kỹ thuật CoT trong việc giải quyết các bài toán toán học lớp 5 so với việc sử dụng module Python tính toán.

---

## 15. Checklist hoàn thành
- [ ] Thiết kế được System Prompt chuẩn bảo mật và chống injection cơ bản.
- [ ] Thành thạo viết prompt Few-shot và kích hoạt CoT.
- [ ] Gọi thành công API trả về JSON chuẩn hóa qua Pydantic.
- [ ] Trả lời đúng tối thiểu 80% câu hỏi ôn tập.

---

## 16. Resources (Tài liệu tham khảo)
- **Tài liệu hướng dẫn**: [OpenAI Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)
- **Khóa học khuyến nghị**: *Prompt Engineering for Developers by Andrew Ng (DeepLearning.AI).*
- **Nghiên cứu khoa học**: *"Chain-of-Thought Prompting Elicits Reasoning in Large Language Models"* (Wei et al.).
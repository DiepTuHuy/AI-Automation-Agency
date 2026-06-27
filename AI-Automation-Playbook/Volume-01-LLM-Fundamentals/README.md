# Volume 01: LLM Fundamentals - Bản chất của Mô hình Ngôn ngữ Lớn

Học về AI Automation mà không hiểu bản chất hoạt động của LLM giống như xây nhà trên cát. Volume này cung cấp các nguyên lý cơ bản nhất về cách LLM suy luận, cách tính toán token, tối ưu hóa cửa sổ ngữ cảnh và cấu hình tham số mô hình trong môi trường Production.

---

## 1. Learning Objectives (Mục tiêu học tập)
Sau khi học xong Volume này, bạn sẽ:
- **Hiểu sâu cấu trúc**: Giải thích được cách Transformer (Decoder-only) dự đoán từ tiếp theo.
- **Tối ưu hóa chi phí**: Biết cách đếm token, tối ưu hóa độ dài prompt và tính toán chi phí vận hành chính xác cho dự án thực tế.
- **Quản lý ngữ cảnh**: Hiểu rõ giới hạn của cửa sổ ngữ cảnh (Context Window) và hiện tượng suy giảm hiệu năng (Lost in the Middle).
- **Làm chủ tham số**: Biết cách phối hợp cấu hình `Temperature`, `Top-p`, `Presence Penalty`, và `Frequency Penalty` theo từng bài toán cụ thể.

---

## 2. Prerequisites (Điều kiện tiên quyết)
- Đã hoàn thành Volume 00.
- Đã cấu hình xong môi trường lập trình Python cơ bản.

---

## 3. Big Picture (Bức tranh tổng thể)
LLM là trái tim của mọi hệ thống AI Agent và Workflow tự động. Nó nhận ngữ cảnh thô (Unstructured Context), thực hiện suy luận logic để trích xuất hoặc đưa ra quyết định, và trả về kết quả có cấu trúc (Structured Outputs).

```
[Raw Context (Dữ liệu thô)]
           │
           ▼
 [LLM Reasoning Engine]  <--- Cấu hình bằng (Temperature, Top-P, Tokens)
           │
           ▼
[Structured Response (JSON)] -> Chuyển tiếp tới các API/Database
```

---

## 4. First Principles (Nguyên lý gốc)
- **LLM không hiểu ý nghĩa thực sự của từ ngữ**: Nó chuyển đổi từ ngữ thành các con số vector và tính toán xác suất liên kết giữa chúng.
- **Mọi tương tác đều là vô trạng thái (Stateless)**: LLM không nhớ cuộc trò chuyện trước đó trừ khi bạn gửi lại toàn bộ lịch sử trò chuyện dưới dạng ngữ cảnh mới.
- **Tiếng Việt tốn kém hơn Tiếng Anh**: Do thuật toán phân tách token (Tokenizer) được tối ưu cho tiếng Anh, một từ tiếng Việt thường bị bẻ nhỏ thành nhiều token hơn, dẫn đến tăng chi phí và giảm tốc độ xử lý.

---

## 5. Mental Models (Mô hình tư duy)
- **Tự động điền văn bản nâng cao (Predictive Autocomplete on Steroids)**: Hãy nghĩ về LLM giống như bàn phím điện thoại của bạn khi bạn gõ tin nhắn, nhưng thay vì chỉ đoán 1 từ tiếp theo, nó có khả năng dự đoán cả một đoạn văn logic cực kỳ dài dựa trên hàng tỷ trang sách đã đọc.
- **Chú ý có chọn lọc (Attention Mechanism)**: Khi bạn đọc một câu, mắt bạn tự động tập trung vào những từ khóa quan trọng nhất. LLM sử dụng cơ chế "Self-Attention" để làm điều tương tự, giúp nó liên kết các từ ở xa nhau trong một đoạn văn.

---

## 6. Core Concepts (Khái niệm cốt lõi)
1. **Tokens**: Đơn vị cơ bản mà LLM dùng để đọc và viết văn bản. Một token có thể là một từ, một phần của từ, hoặc thậm chí là một dấu cách.
2. **Context Window**: Dung lượng bộ nhớ đệm tối đa mà mô hình có thể nhận và xử lý trong một lượt gọi (bao gồm cả Input và Output).
3. **Loss of Attention (Lost in the Middle)**: Hiện tượng mô hình chú ý tốt ở đầu và cuối prompt, nhưng bỏ sót thông tin nằm ở giữa khi ngữ cảnh quá dài.

---

## 8. Best Practices (Quy chuẩn thực chiến)
- **Luôn đặt giới hạn `max_tokens`**: Tránh việc LLM bị lặp vô tận (loop) làm cạn kiệt tài khoản API.
- **Chọn mô hình phù hợp**: Dùng mô hình nhỏ, rẻ (như GPT-4o-mini, Gemini 1.5 Flash) cho các tác vụ phân loại đơn giản; chỉ dùng mô hình lớn (GPT-4o, Claude 3.5 Sonnet) cho các tác vụ suy luận phức tạp hoặc viết code.
- **Lưu cache prompt (Prompt Caching)**: Sử dụng các mô hình hỗ trợ cache ngữ cảnh để giảm đến 90% chi phí đầu vào đối với các tài liệu dài cố định.

---

## 9. Common Mistakes (Sai lầm thường gặp)
- **Temperature = 1 cho các tác vụ trả về JSON**: Làm cho kết quả trả về không ổn định và dễ gãy cú pháp JSON. *Cách sửa*: Sử dụng `temperature = 0` và kích hoạt chế độ `response_format={"type": "json_object"}`.
- **Quá tải context**: Nhồi nhét hàng nghìn trang tài liệu vào prompt mà không lọc trước. *Cách sửa*: Sử dụng kỹ thuật RAG (Volume 08) để lọc dữ liệu liên quan trước khi gửi cho LLM.

---

## 10. Engineering Mindset (Tư duy kỹ sư)
Một Kỹ sư AI luôn tính toán chi phí trước khi code:
$$	ext{Total Cost} = (	ext{Input Tokens} 	imes 	ext{Input Price}) + (	ext{Output Tokens} 	imes 	ext{Output Price})$$
Nếu hệ thống của bạn xử lý 10,000 khách hàng/ngày, việc tối ưu hóa 100 token/lượt gọi prompt sẽ giúp doanh nghiệp tiết kiệm hàng nghìn USD mỗi năm.

---

## 13. Capstone Project (Dự án kết khóa Volume)
Xây dựng một chương trình CLI phân tích chi phí dự án AI: Chương trình nhận đầu vào là một file tài liệu (txt/pdf thô), đếm số token tiếng Việt thực tế, ước lượng chi phí khi sử dụng 3 API khác nhau (OpenAI, Anthropic, Gemini), và tự động xuất ra file báo cáo so sánh dưới dạng CSV.

---

## 14. Review Questions (Bloom Taxonomy - 30 câu hỏi)
### Level 1 — Remember (Nhớ)
1. Token là gì?
2. Transformer là cấu trúc mạng gì? Ai đề xuất và vào năm nào?
3. Cửa sổ ngữ cảnh (Context Window) là gì?
4. Đơn vị tính tiền của các API LLM thương mại hiện nay là gì?
5. `temperature` trong LLM nhận giá trị trong khoảng nào?

### Level 2 — Understand (Hiểu)
6. Giải thích sự khác biệt giữa thuật toán tokenization tiếng Việt và tiếng Anh.
7. Tại sao LLM lại gặp khó khăn trong việc thực hiện các phép tính toán học phức tạp hoặc đếm ký tự trong từ?
8. Tại sao nói LLM là một hệ thống "Stateless"? Làm cách nào để duy trì cuộc trò chuyện liên tục?
9. Cơ chế Attention (Chú ý) giải quyết vấn đề gì của mạng RNN truyền thống?
10. Giải thích hiện tượng "Lost in the Middle".

### Level 3 — Apply (Áp dụng)
11. Sử dụng thư viện `tiktoken` viết hàm Python đếm số lượng token của một chuỗi văn bản cho trước.
12. Tính toán chi phí xử lý một tài liệu 50,000 từ tiếng Anh bằng mô hình GPT-4o (Giá: $5/M input, $15/M output), giả định output trả về khoảng 2,000 từ.
13. Cấu hình các tham số gọi API của OpenAI để sinh ra một kết quả sáng tạo, không trùng lặp (viết truyện).
14. Thiết lập cấu hình API để trích xuất thông tin khách hàng từ email thô dưới dạng một định dạng cố định và chính xác 100%.
15. Sử dụng môi trường ảo (virtualenv) để quản lý các thư viện cần dùng cho API LLM.

### Level 4 — Analyze (Phân tích)
16. Phân tích tác động của việc tăng `presence_penalty` đối với nội dung văn bản sinh ra bởi LLM.
17. Tại sao việc tăng kích thước cửa sổ ngữ cảnh (ví dụ: lên 1 triệu token của Gemini) lại làm tăng độ trễ (latency) của phản hồi?
18. So sánh ưu thế về chi phí và hiệu năng giữa GPT-4o và GPT-4o-mini trong bài toán phân loại email rác hàng loạt.
19. Phân tích tại sao mô hình tự nhiên sinh ra lỗi lặp từ vô hạn và cách dùng cấu hình tham số để can thiệp.
20. Tại sao tokenizer của các mô hình LLM đời cũ thường mã hóa ký tự emoji thành rất nhiều token?

### Level 5 — Design (Thiết kế)
21. Thiết kế cấu trúc dữ liệu lưu trữ lịch sử chat tối ưu để gửi lại cho LLM mà không làm vượt ngưỡng token cho phép.
22. Đề xuất thuật toán tự động cắt ngắn (truncate) lịch sử hội thoại dựa trên số lượng token thay vì số câu tin nhắn.
23. Thiết kế hệ thống cảnh báo (alert) tự động khi chi phí API vượt quá ngân sách hàng ngày đặt trước.
24. Thiết kế cơ chế gọi API song song (Concurrent Requests) để xử lý hàng loạt tài liệu lớn mà không bị dính giới hạn Rate Limit (TPM - Tokens Per Minute).
25. Đề xuất giải pháp kỹ thuật để xử lý một cuốn sách dài 2 triệu token bằng mô hình chỉ có context window 128k tokens.

### Level 6 — Evaluate (Đánh giá)
26. Đánh giá chất lượng dịch thuật của LLM khi sử dụng tokenizer chuẩn hóa đa ngôn ngữ.
27. Đánh giá sự đánh đổi giữa việc tăng tốc độ phản hồi (Time to First Token) và chất lượng tư duy suy luận khi chọn mô hình.
28. Kiểm chứng độ tin cậy của chế độ Structured Output (JSON Mode) khi chạy thử 1,000 lượt yêu cầu liên tục.
29. Đánh giá hiệu quả kinh tế của việc áp dụng Prompt Caching trong hệ thống hỏi đáp tự động về tài liệu nội bộ công ty.
30. Lập luận bác bỏ hoặc đồng ý với quan điểm: *"Context Window càng lớn thì công nghệ RAG càng trở nên vô dụng"*.

---

## 15. Checklist hoàn thành
- [ ] Hiểu rõ khái niệm Token và cách tính giá API.
- [ ] Viết được script Python kết nối thành công với API LLM (OpenAI/Gemini/Anthropic).
- [ ] Thành thạo cách sử dụng tiktoken để tối ưu hóa dữ liệu đầu vào.
- [ ] Trả lời đúng tối thiểu 80% câu hỏi ôn tập.

---

## 16. Resources (Tài liệu tham khảo)
- **Tài liệu chính thức**: [OpenAI API Reference](https://platform.openai.com/docs)
- **Đọc thêm**: *"Attention Is All You Need"* (Vaswani et al., 2017) - Paper nền tảng của Transformer.
- **Công cụ trực quan**: [OpenAI Tokenizer Tool](https://platform.openai.com/tokenizer)

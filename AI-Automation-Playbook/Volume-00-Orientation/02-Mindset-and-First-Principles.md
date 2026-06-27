# Chương 02: Tư duy Nguyên lý gốc & Systems Thinking

## 1. Deep Dive (Phân tích chuyên sâu)

### Nguyên lý gốc (First Principles Thinking) trong AI
First Principles là phương pháp phân rã một vấn đề phức tạp thành các sự thật cơ bản nhất không thể chia nhỏ hơn được nữa, sau đó xây dựng giải pháp từ mặt đất đi lên.
Trong AI Automation, thay vì hỏi: *"Làm thế nào để bắt chước quy trình của đối thủ bằng LangChain?"*, hãy hỏi:
- *Dữ liệu đầu vào của quy trình này thực chất là gì?* (Text, Image, Audio)
- *Mục tiêu đầu ra cuối cùng là gì?* (Một quyết định phê duyệt, một email phản hồi, hay dữ liệu được cập nhật vào database)
- *Mô hình AI nào xử lý tác vụ suy luận này tối ưu nhất về mặt chi phí?*

Bằng cách này, bạn sẽ tránh được việc lạm dụng công nghệ phức tạp khi chỉ cần một câu lệnh điều kiện đơn giản hoặc một prompt ngắn là đủ giải quyết vấn đề.

### Systems Thinking (Tư duy hệ thống)
Hệ thống AI Automation không đứng độc lập. Nó bao gồm nhiều thành phần tương tác lẫn nhau:
1. **Inputs (Đầu vào)**: Dữ liệu từ khách hàng, API bên thứ ba.
2. **Processes (Xử lý)**: LLM, Python scripts, database queries.
3. **Outputs (Đầu ra)**: Thông báo gửi đi, báo cáo, cập nhật hệ thống.
4. **Feedback Loop (Vòng phản hồi)**: Sự đánh giá của con người (Human-in-the-loop) để cải tiến mô hình prompt hoặc hệ thống.

Một lỗi ở bất kỳ mắt xích nào cũng có thể làm sụp đổ toàn bộ hệ thống. Do đó, bạn phải luôn thiết kế hệ thống với tư duy phòng ngừa rủi ro và xử lý ngoại lệ (Exception Handling).

---

## 2. Demo: Áp dụng First Principles phân tích lỗi Hallucination (Ảo tưởng)

### Mục tiêu
Tìm ra nguyên nhân gốc rễ tại sao AI tạo ra thông tin sai lệch (hallucination) trong một tác vụ trích xuất dữ liệu doanh nghiệp và cách khắc phục triệt để.

### Phân tích nguyên lý gốc
- **Sự thật 1**: LLM hoạt động bằng cách dự đoán token tiếp theo có xác suất cao nhất dựa trên dữ liệu huấn luyện. Nó không có khái niệm về "sự thật khách quan".
- **Sự thật 2**: Nếu ngữ cảnh đầu vào (Context) không chứa thông tin cần thiết, LLM buộc phải "suy đoán" và tạo ra thông tin giả trông có vẻ thuyết phục.
- **Giải pháp**: Không bao giờ hỏi LLM những câu hỏi mở về dữ liệu riêng tư của bạn mà không cung cấp dữ liệu đó làm ngữ cảnh đầu vào. Cung cấp chỉ dẫn rõ ràng: *"Nếu không tìm thấy thông tin trong tài liệu được cung cấp, hãy trả lời 'Tôi không biết', không được tự ý bịa đặt."*

---

## 3. Mini Project
Hãy thiết lập một thử nghiệm nhỏ với ChatGPT/Claude:
1. Hỏi AI một sự kiện rất ngách, không phổ biến và xem cách nó bịa ra câu trả lời.
2. Cung cấp một đoạn văn ngắn chứa thông tin đúng về sự kiện đó, yêu cầu AI trả lời lại dựa trên đoạn văn.
3. So sánh kết quả và viết báo cáo ngắn rút ra bài học về tầm quan trọng của Context.

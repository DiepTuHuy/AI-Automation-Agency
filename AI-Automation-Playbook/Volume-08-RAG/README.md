# Volume 08: RAG (Retrieval-Augmented Generation) - Triển Khai Hệ Thống Hỏi Đáp Tài Liệu Doanh Nghiệp

Mô hình LLM thương mại dù thông minh đến đâu cũng không thể biết về các thông tin nội bộ của doanh nghiệp (như báo cáo tài chính nội bộ, hợp đồng khách hàng, quy trình kỹ thuật độc quyền). Fine-tune mô hình vừa đắt đỏ, vừa không thể cập nhật dữ liệu hàng giờ và không hỗ trợ phân quyền người dùng. **RAG (Retrieval-Augmented Generation)** là giải pháp tiêu chuẩn công nghiệp hiện nay: kết hợp tìm kiếm thông tin ngữ nghĩa với khả năng suy luận của LLM để tạo ra các chatbot hỏi đáp tài liệu chính xác tuyệt đối, không ảo tưởng và dẫn nguồn rõ ràng.

---

## 1. Learning Objectives (Mục tiêu học tập)
Sau khi hoàn thành Volume này, bạn sẽ:
- **Làm chủ Kiến trúc RAG**: Hiểu rõ 3 pha của hệ thống RAG: Ingestion (Nạp dữ liệu), Retrieval (Truy xuất) và Generation (Sinh câu trả lời).
- **Tối ưu hóa Phân đoạn (Chunking)**: Thành thạo các kỹ thuật cắt nhỏ văn bản (Recursive Text Splitter, Semantic Chunking) và cấu hình tham số Overlap.
- **Nâng cao khả năng truy xuất (Retrieval)**: Hiểu rõ cơ chế Reranking (Xếp hạng lại) để đưa ra ngữ cảnh chính xác nhất cho LLM.
- **Đánh giá hệ thống RAG**: Sử dụng mô hình LLM-as-a-judge để tự động đánh giá các chỉ số: Context Relevance, Groundedness và Answer Relevance.
- **Xây dựng RAG Pipeline hoàn chỉnh**: Tự tay lập trình hệ thống hỏi đáp tài liệu doanh nghiệp chất lượng Production.

---

## 2. Prerequisites (Điều kiện tiên quyết)
- Hoàn thành Volume 07 (Embedding & Vector Database).
- Hiểu rõ cách gọi API OpenAI và sử dụng Python.

---

## 3. Big Picture (Bức tranh tổng thể)
RAG biến câu hỏi mở của người dùng thành một bài toán đọc hiểu văn bản khép kín: hệ thống lục tìm tài liệu liên quan trong Vector DB -> Nhét tài liệu đó vào prompt làm "phao thi" -> LLM chỉ việc đọc phao và trả lời chính xác.

```
[Câu hỏi người dùng]
        │
        ▼
[Truy vấn Vector DB] ──> [Lấy ra 3 đoạn văn bản liên quan nhất]
                                      │
                                      ▼
[System Prompt: "Hãy trả lời câu hỏi CHỈ dựa trên thông tin sau..."] + [3 đoạn văn]
                                      │
                                      ▼
                             [LLM sinh câu trả lời]
```

---

## 4. First Principles (Nguyên lý gốc)
- **Garbage In, Garbage Out (Rác vào, Rác ra)**: Nếu bước truy xuất tài liệu (Retrieval) trả về thông tin sai lệch hoặc không liên quan, LLM chắc chắn sẽ sinh ra câu trả lời sai dù prompt có tốt đến đâu.
- **Ràng buộc ngữ cảnh khép kín**: Để loại bỏ ảo tưởng (hallucination), bạn phải ràng buộc LLM không được sử dụng kiến thức bên ngoài nếu ngữ cảnh được cung cấp không đề cập tới.
- **Bảo toàn cấu trúc ngữ nghĩa**: Khi cắt nhỏ tài liệu dài thành các chunk, việc giữ lại một phần dữ liệu gối đầu (Overlap) giữa hai chunk liên tiếp là bắt buộc để tránh làm mất mối liên kết câu ở ranh giới cắt.

---

## 5. Mental Models (Mô hình tư duy)
- **Kỳ thi sách mở (Open Book Exam)**: Hãy tưởng tượng LLM là một học sinh cực kỳ thông minh trong phòng thi nhưng không học bài trước (Base Model).
  - *Không có RAG*: Học sinh tự nhớ lại kiến thức cũ -> dễ bị nhớ nhầm hoặc bịa ra đáp án trông có vẻ đúng.
  - *Có RAG*: Giám thị tìm đúng trang sách chứa câu trả lời và đặt trước mặt học sinh -> học sinh chỉ việc đọc hiểu trang sách đó và viết ra câu trả lời chuẩn xác.

---

## 6. Core Concepts (Khái niệm cốt lõi)
1. **Chunking**: Quá trình phân tách các file tài liệu dài (như PDF, Word) thành các đoạn văn ngắn có kích thước phù hợp với context window của mô hình.
2. **Overlap**: Số lượng ký tự hoặc token trùng lặp được giữ lại ở điểm giao nhau của hai đoạn văn kế tiếp để duy trì mạch thông tin liên tục.
3. **Reranking**: Quá trình sử dụng một mô hình deep learning chuyên dụng để tính toán lại điểm số tương đồng của các tài liệu tìm được từ bước trước, đẩy các tài liệu thực sự liên quan lên đầu.

---

## 8. Best Practices (Quy chuẩn thực chiến)
- **Đặt giới hạn chặn (Confidence Threshold)**: Nếu kết quả truy vấn từ Vector DB có điểm tương đồng Cosine quá thấp (ví dụ dưới 0.65), hãy lập tức báo cho người dùng: *"Tôi không tìm thấy thông tin này trong tài liệu"* thay vì cho LLM suy đoán bừa bãi.
- **Sử dụng RecursiveCharacterTextSplitter**: Luôn ưu tiên bộ chia cắt văn bản đệ quy vì nó tự động ưu tiên cắt ở các ký tự ngắt dòng kép `\n\n` (đoạn văn), ngắt dòng đơn `\n` (câu), rồi mới đến dấu cách (từ), giúp bảo toàn cấu trúc văn bản tự nhiên.
- **Metadata Tagging**: Ghi nhãn metadata nguồn (tên file, số trang) và bắt LLM trích dẫn nguồn cụ thể ở cuối câu trả lời (Citation) để người dùng tự kiểm chứng.

---

## 9. Common Mistakes (Sai lầm thường gặp)
- **Nhồi quá nhiều tài liệu tìm được vào Prompt**: Dẫn đến việc LLM bị quá tải thông tin, gây hiện tượng Lost in the Middle và làm tăng chi phí API vô ích. *Cách sửa*: Sử dụng Reranking để chọn ra tối đa 3-5 đoạn thực sự giá trị nhất.
- **Cắt văn bản quá nhỏ hoặc quá lớn**: Chunk quá nhỏ làm mất ngữ cảnh bao quanh câu; Chunk quá lớn làm loãng vector ý nghĩa và lãng phí token. *Cách sửa*: Kích thước tối ưu thường là **500 - 1000 characters** với Overlap **10% - 20%**.

---

## 10. Engineering Mindset (Tư duy kỹ sư)
Kỹ sư AI Automation luôn đo lường RAG bằng 3 chỉ số vàng (RAG Triad):
1. **Context Relevance**: Ngữ cảnh tìm được có thực sự chứa câu trả lời không?
2. **Groundedness (Faithfulness)**: Câu trả lời của AI có hoàn toàn dựa trên ngữ cảnh không, hay tự bịa ra?
3. **Answer Relevance**: Câu trả lời của AI có đi đúng vào trọng tâm câu hỏi của người dùng không?

---

## 13. Capstone Project (Dự án kết khóa Volume)
Xem mô tả chi tiết tại [Project-03](file:///Users/dieptuhuy/Documents/AI%20Automation/AI-Automation-Playbook/Projects/Project-03-AI-Chat-PDF-Knowledge-Base/README.md).

---

## 14. Review Questions (Bloom Taxonomy - 30 câu hỏi)
### Level 1 — Remember (Nhớ)
1. RAG là viết tắt của cụm từ gì?
2. Nêu 3 pha chính trong một hệ thống RAG cơ bản.
3. Kích thước chunk (Chunk Size) và Overlap là gì?
4. Nêu tên 3 thư viện mã nguồn mở phổ biến hỗ trợ xây dựng RAG trong Python.
5. Reranker hoạt động ở bước nào trong quy trình RAG?

### Level 2 — Understand (Hiểu)
6. Tại sao nói RAG là giải pháp tối ưu hơn Fine-tuning đối với bài toán hỏi đáp tài liệu nội bộ doanh nghiệp thay đổi liên tục?
7. Giải thích hiện tượng "Hallucination" trong RAG và cách thiết lập prompt để ngăn ngừa.
8. Tại sao việc chia văn bản theo số lượng ký tự thuần túy (CharacterTextSplitter) lại dễ làm hỏng cấu trúc câu?
9. Cơ chế hoạt động của thuật toán Reranking (sử dụng Cross-Encoder) khác gì so với tìm kiếm vector thông thường (Bi-Encoder)?
10. Giải thích 3 chỉ số của mô hình RAG Triad.

### Level 3 — Apply (Áp dụng)
11. Sử dụng Python viết hàm chia nhỏ một đoạn văn bản dài bằng kỹ thuật cắt thủ công dựa trên dấu xuống dòng kép `\n\n`.
12. Viết cấu trúc Prompt hoàn chỉnh cho một RAG Agent yêu cầu không được dùng kiến thức bên ngoài và phải dẫn nguồn cụ thể.
13. Cài đặt thư viện LangChain và viết code sử dụng `RecursiveCharacterTextSplitter` cấu hình chunk size 500, overlap 50.
14. Thiết lập code Python kết hợp kết quả truy vấn từ ChromaDB nhét vào chuỗi prompt gửi tới GPT-4o-mini.
15. Lập trình một hệ thống kiểm tra nhanh độ tương đồng của câu hỏi và ngữ cảnh tìm được, nếu dưới 0.7 thì trả về thông báo lỗi mặc định.

### Level 4 — Analyze (Phân tích)
16. Phân tích sự đánh đổi về chi phí, tốc độ và chất lượng câu trả lời khi tăng số lượng tài liệu tham chiếu (K-value) từ 3 lên 15.
17. So sánh hiệu năng của RAG khi sử dụng mô hình embedding nhỏ của HuggingFace chạy local với mô hình lớn của OpenAI qua API.
18. Phân tích nguyên nhân tại sao AI trả lời sai dù thông tin đúng nằm ở trang thứ 5 của tài liệu đã được nạp vào Vector DB.
19. Đánh giá tính hiệu quả của việc chèn siêu dữ liệu (Metadata) như tiêu đề chương vào từng chunk trước khi lưu vào DB.
20. Tại sao việc phân quyền truy cập tài liệu (Document ACL) lại là bài toán khó giải quyết nhất trong kiến trúc RAG doanh nghiệp?

### Level 5 — Design (Thiết kế)
21. Thiết kế quy trình nạp tài liệu tự động (Ingestion Pipeline) nhận file PDF, quét ảnh bằng OCR nếu là PDF quét, chia chunk, tạo vector và lưu DB.
22. Đề xuất kiến trúc RAG nâng cao sử dụng kỹ thuật Parent Document Retriever (Lưu chunk nhỏ để tìm kiếm nhưng lấy chunk lớn hơn để gửi LLM).
23. Thiết kế hệ thống LLM-as-a-judge tự động đánh giá độ trung thực (Faithfulness) của câu trả lời AI bằng cách so sánh từng khẳng định với ngữ cảnh gốc.
24. Đề xuất giải pháp lưu trữ lịch sử chat của người dùng để làm ngữ cảnh hội thoại (Conversational RAG) không làm loãng kết quả tìm kiếm ngữ nghĩa mới.
25. Thiết kế kiến trúc RAG cho doanh nghiệp có hệ thống phân quyền: Nhân viên phòng nhân sự chỉ được tìm thấy tài liệu nhân sự, không được tìm thấy tài liệu tài chính.

### Level 6 — Evaluate (Đánh giá)
26. Đánh giá hiệu năng thực tế của hệ thống RAG khi áp dụng kỹ thuật Query Rewriting (AI tự viết lại câu hỏi của người dùng trước khi tìm kiếm).
27. Đánh giá sự đánh đổi giữa việc tự host mô hình Rerank (như bge-reranker) trên GPU riêng và sử dụng dịch vụ API của Cohere.
28. Kiểm chứng chất lượng câu trả lời của hệ thống RAG đối với các câu hỏi so sánh số liệu tài chính giữa nhiều năm khác nhau.
29. Đánh giá độ bảo mật và rủi ro rò rỉ dữ liệu nhạy cảm của doanh nghiệp khi sử dụng mô hình LLM công cộng làm bộ não Generation trong RAG.
30. Lập luận bác bỏ hoặc đồng ý với quan điểm: *"Với sự ra đời của các mô hình có Context Window siêu lớn (như 2 triệu token), RAG sẽ hoàn toàn bị thay thế bởi việc nhét toàn bộ file vào prompt"*.

---

## 15. Checklist hoàn thành
- [ ] Hiểu rõ kiến trúc và quy trình vận hành RAG.
- [ ] Thực hiện thành thạo việc chia nhỏ tài liệu (Chunking) bằng thư viện Python.
- [ ] Lập trình thành công hệ thống RAG thô (gọi Vector DB -> chèn prompt -> gọi LLM).
- [ ] Viết được script tự động đánh giá chất lượng câu trả lời bằng LLM-as-a-judge.
- [ ] Hoàn thành Capstone Project (Project 03).

---

## 16. Resources (Tài liệu tham khảo)
- **Tài liệu**: [LangChain RAG Tutorial](https://python.langchain.com/v0.2/docs/tutorials/rag/)
- **Đọc thêm**: *"Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"* (Lewis et al., 2020) - Paper khai sinh RAG.
- **Đo lường**: [Ragas Framework Documentation](https://docs.ragas.io/en/stable/)

# Volume 07: Embedding & Vector Database - Cơ Sở Của Trí Nhớ AI

Để AI có khả năng tìm kiếm thông tin ngữ cảnh chính xác từ hàng triệu tài liệu doanh nghiệp, nó không thể dùng phương pháp tìm từ khóa (Keyword search) truyền thống. Khóa học này giới thiệu về **Vector Embeddings** và **Vector Databases** - hai công nghệ nền tảng giúp chuyển hóa ngôn ngữ tự nhiên thành tọa độ toán học để so sánh ý nghĩa ngữ nghĩa (Semantic Search). Bạn sẽ làm chủ từ toán học đo độ tương đồng vector, đến cách thiết lập ChromaDB (cục bộ) và Pinecone (cloud) để phục vụ tìm kiếm thông tin thời gian thực với độ trễ thấp.

---

## 1. Learning Objectives (Mục tiêu học tập)
Sau khi hoàn thành Volume này, bạn sẽ:
- **Hiểu bản chất Vector**: Giải thích được cách các mô hình biến đổi chữ viết thành các chuỗi số thực nhiều chiều (Dense Vectors).
- **Làm chủ toán học tương đồng**: Hiểu rõ và tính toán được khoảng cách Cosine, Tích vô hướng (Dot Product) và khoảng cách Euclidean.
- **Vận hành Vector DB cục bộ**: Cài đặt và thao tác thành thạo ChromaDB để lưu trữ và truy vấn vector.
- **Sử dụng Vector DB đám mây**: Thiết lập tài khoản Pinecone và tích hợp vào dự án.
- **Truy vấn lai (Hybrid Query)**: Biết cách kết hợp tìm kiếm ngữ nghĩa bằng vector với các điều kiện lọc siêu dữ liệu (Metadata Filtering).

---

## 2. Prerequisites (Điều kiện tiên quyết)
- Hoàn thành Volume 03 (Python Automation).
- Nắm vững kiến thức toán học ma trận cơ bản và lập trình Python.

---

## 3. Big Picture (Bức tranh tổng thể)
Vector Database đóng vai trò là "Kho tri thức ngữ nghĩa" của AI. Hệ thống tải dữ liệu thô -> Chuyển thành Vector qua Embedding API -> Lưu vào Vector DB -> Khi người dùng hỏi, chuyển câu hỏi thành vector -> Truy vấn tìm 3 đoạn văn bản có nghĩa gần nhất -> Nhét vào prompt gửi LLM.

```
[Văn bản thô] ──(Embedding Model)──> [Vector (Chuỗi số 1536 chiều)] ──> [Vector DB (ChromaDB)]
                                                                               ▲
                                                                               │ (Query Vector)
[Câu hỏi người dùng] ──(Embedding Model) ──────────────────────────────────────┘
```

---

## 4. First Principles (Nguyên lý gốc)
- **Semantic Space (Không gian ngữ nghĩa)**: Các từ hoặc câu có ý nghĩa tương tự nhau sẽ được xếp gần nhau trong không gian vector nhiều chiều (ví dụ: vector của "vua" và "hoàng hậu" sẽ có khoảng cách rất ngắn).
- **Embedding là phép ánh xạ một chiều**: Một khi đã biến chữ thành vector, bạn không thể dịch ngược vector đó ra chữ gốc. Nó chỉ dùng để so sánh khoảng cách.
- **Số chiều cố định (Fixed Dimensions)**: Một bộ mã hóa embedding luôn trả về vector có số chiều cố định (ví dụ OpenAI `text-embedding-3-small` luôn trả về 1536 số thực) dù đầu vào là 1 từ hay 1 đoạn văn 1000 từ.

---

## 5. Mental Models (Mô hình tư duy)
- **Tọa độ GPS ý nghĩa (Semantic GPS)**: Hãy tưởng tượng mỗi câu văn giống như một địa điểm trên thế giới. Địa điểm có kinh độ và vĩ độ. Vector Embedding chính là tọa độ GPS của ý nghĩa câu văn. Câu *"Hôm nay trời nóng quá"* và *"Nhiệt độ ngoài trời đang tăng cao"* sẽ có tọa độ GPS nằm sát cạnh nhau. Còn câu *"Tôi thích học lập trình Python"* sẽ nằm ở một múi giờ hoàn toàn khác cách xa hàng nghìn cây số. So sánh vector thực chất là tính khoảng cách địa lý giữa các tọa độ này.

---

## 6. Core Concepts (Khái niệm cốt lõi)
1. **Vector Embedding**: Chuỗi các số thực đại diện cho ngữ nghĩa của một đối tượng (văn bản, hình ảnh, âm thanh).
2. **Cosine Similarity**: Phép đo góc giữa hai vector trong không gian nhiều chiều. Giá trị tiệm cận 1 nghĩa là hai câu rất gần nghĩa nhau, tiệm cận 0 là không liên quan.
3. **ChromaDB**: Cơ sở dữ liệu vector mã nguồn mở gọn nhẹ, tự chạy trong RAM hoặc lưu file đĩa cứng cục bộ, rất phù hợp cho phát triển phần mềm nhanh.

---

## 8. Best Practices (Quy chuẩn thực chiến)
- **Chuẩn hóa Vector trước khi so sánh**: Luôn sử dụng phép tính Cosine Similarity hoặc chuẩn hóa độ dài vector về 1 để phép tính Tích vô hướng (Dot Product) diễn ra nhanh nhất.
- **Lưu kèm Metadata**: Luôn chèn các thông tin phụ (như `source_file`, `created_at`, `category`) vào metadata của vector để phục vụ việc lọc dữ liệu cứng nhanh chóng mà không cần chạy thuật toán tìm kiếm vector tốn kém.
- **Đồng bộ hóa Embedding Model**: Tuyệt đối không dùng mô hình A để sinh vector lưu trữ và dùng mô hình B để truy vấn. Kết quả tìm kiếm sẽ bị sai lệch hoàn toàn.

---

## 9. Common Mistakes (Sai lầm thường gặp)
- **Sử dụng CSDL SQL truyền thống để tìm kiếm vector**: Thực hiện tính khoảng cách trên hàng triệu dòng bằng hàm Python tự viết sẽ gây nghẽn CPU và mất hàng chục giây. *Cách sửa*: Chuyển sang sử dụng thuật toán chỉ mục chuyên dụng như HNSW được tích hợp sẵn trong các Vector DB chuyên nghiệp.
- **Không xử lý nhiễu dữ liệu**: Nhét toàn bộ file PDF chứa ảnh, bảng biểu thô vào embedding model làm loãng tọa độ vector ngữ nghĩa. *Cách sửa*: Làm sạch văn bản, loại bỏ các ký tự đặc biệt thừa trước khi nhúng.

---

## 10. Engineering Mindset (Tư duy kỹ sư)
Một kỹ sư AI Automation luôn cân bằng giữa độ chính xác và tài nguyên. Họ hiểu rằng việc tăng số chiều vector (ví dụ từ 1536 lên 3072 chiều) sẽ cải thiện một chút độ chính xác nhưng sẽ làm tăng gấp đôi dung lượng lưu trữ đĩa cứng và tăng 50% độ trễ truy vấn. Hãy chọn số chiều tối giản vừa đủ dùng cho bài toán thực tế.

---

## 13. Capstone Project (Dự án kết khóa Volume)
Thiết kế hệ thống tìm kiếm tài liệu thông minh (FAQ Semantic Search Engine): Viết script Python đọc danh sách câu hỏi thường gặp FAQ của công ty từ file CSV, tự động gọi API nhúng của OpenAI để tạo vector, nạp vào ChromaDB. Xây dựng một ứng dụng FastAPI có cổng POST `/api/v1/search` nhận câu hỏi tự nhiên của người dùng, thực hiện truy vấn trong ChromaDB và trả về câu trả lời FAQ có độ tương đồng cao nhất kèm theo điểm số phần trăm tin cậy.

---

## 14. Review Questions (Bloom Taxonomy - 30 câu hỏi)
### Level 1 — Remember (Nhớ)
1. Vector Embedding là gì?
2. Số lượng chiều (Dimensions) mặc định của mô hình nhúng `text-embedding-3-small` của OpenAI là bao nhiêu?
3. Nêu 3 chỉ số đo độ tương đồng giữa hai vector.
4. ChromaDB mặc định lưu trữ dữ liệu ở đâu?
5. Thuật toán HNSW viết tắt của cụm từ gì?

### Level 2 — Understand (Hiểu)
6. Giải thích sự khác biệt giữa tìm kiếm từ khóa (Keyword Search) và tìm kiếm ngữ nghĩa (Semantic Search).
7. Tại sao Tích vô hướng (Dot Product) lại hoạt động cực nhanh đối với các vector đã được chuẩn hóa độ dài về 1?
8. Tại sao cơ sở dữ liệu quan hệ (như PostgreSQL) cần cài thêm extension (như `pgvector`) để lưu trữ vector thay vì dùng cột text thông thường?
9. Lọc siêu dữ liệu (Metadata Filtering) giải quyết bài toán gì trong truy vấn Vector DB?
10. Hiện tượng "Dimensionality Curse" (Lời nguyền số chiều nhiều) ảnh hưởng thế nào đến tính khoảng cách vector?

### Level 3 — Apply (Áp dụng)
11. Viết code Python gọi API của OpenAI để sinh vector embedding cho chuỗi "Học AI Automation rất thú vị".
12. Sử dụng thư viện NumPy viết hàm tính Cosine Similarity giữa hai mảng vector số thực đơn giản.
13. Khởi tạo một ChromaDB client cục bộ, tạo một collection mới có tên `company_policy`.
14. Nạp 3 đoạn văn bản nội quy công ty vào collection ChromaDB kèm theo metadata `author="HR"`.
15. Thực hiện truy vấn (query) tìm kiếm 2 đoạn văn bản tương đồng nhất với câu "Lịch nghỉ phép năm thế nào?".

### Level 4 — Analyze (Phân tích)
16. Phân tích sự ảnh hưởng của việc chọn mô hình nhúng mã nguồn mở chạy local (như BGE-small) so với API trả phí của OpenAI đối với độ trễ hệ thống.
17. So sánh ưu thế và nhược điểm của Pinecone (Cloud SaaS) và ChromaDB (Local file) trong thiết kế kiến trúc hệ thống B2B.
18. Phân tích tại sao câu "Tôi không thích ăn táo" và câu "Tôi rất ghét quả táo" lại có khoảng cách tương đồng rất gần nhau dù chúng không chung từ khóa nào.
19. Phân tích nguyên nhân làm giảm sút chất lượng tìm kiếm vector khi tài liệu đầu vào có chứa quá nhiều ngôn ngữ code lập trình hoặc bảng biểu hỗn loạn.
20. Tại sao việc chuẩn hóa độ dài vector (L2 Normalization) lại giúp tối ưu hóa thuật toán tìm kiếm K-lân cận gần nhất (KNN)?

### Level 5 — Design (Thiết kế)
21. Thiết kế cấu trúc lưu trữ Metadata tối ưu cho bài toán tìm kiếm bài viết blog theo chuyên mục và thẻ tag.
22. Đề xuất kiến trúc hệ thống cập nhật tự động cơ sở dữ liệu Vector DB khi file tài liệu gốc trên Google Drive có sự thay đổi (Thêm/Sửa/Xóa).
23. Thiết kế giải pháp phân vùng dữ liệu (Multitenancy) trong Pinecone để đảm bảo dữ liệu của Khách hàng A không bao giờ bị lẫn sang Khách hàng B.
24. Đề xuất quy trình kiểm thử chất lượng tìm kiếm (Retrieval Evaluation) của hệ thống Vector Search sử dụng độ đo Recall@K.
25. Thiết kế công thức tính điểm kết hợp (Hybrid Search Score) giữa tìm kiếm từ khóa truyền thống (BM25) và tìm kiếm ngữ nghĩa vector.

### Level 6 — Evaluate (Đánh giá)
26. Đánh giá tính kinh tế khi lưu trữ 10 triệu vector embedding 1536 chiều trên bộ nhớ RAM Redis so với giải pháp đĩa cứng Pinecone.
27. Đánh giá sự đánh đổi giữa tốc độ truy vấn (latency) và độ chính xác (recall) khi cấu hình tham số chỉ mục HNSW `M` và `ef_construction` trong Vector DB.
28. Kiểm chứng độ ổn định của việc tìm kiếm ngữ nghĩa khi người dùng nhập câu hỏi bằng nhiều ngôn ngữ khác nhau (tiếng Việt, tiếng Anh, tiếng Nhật) truy vấn cùng một DB tiếng Việt.
29. Đánh giá mức độ ảnh hưởng của việc nâng cấp mô hình embedding mới đối với toàn bộ dữ liệu vector cũ đã lưu trong DB.
30. Lập luận bác bỏ hoặc đồng ý với quan điểm: *"Mô hình ngôn ngữ trong tương lai sẽ tự ghi nhớ mọi thứ trực tiếp trên weights của nó, khiến Vector Database biến mất"*.

---

## 15. Checklist hoàn thành
- [ ] Hiểu rõ bản chất toán học của Vector Embedding.
- [ ] Viết được script Python sinh vector qua OpenAI Embedding API.
- [ ] Cài đặt thành công ChromaDB và chạy được các lệnh thêm, truy vấn vector cục bộ.
- [ ] Thực hiện được việc lọc kết quả bằng Metadata.
- [ ] Trả lời đúng tối thiểu 80% câu hỏi ôn tập.

---

## 16. Resources (Tài liệu tham khảo)
- **Tài liệu**: [ChromaDB Official Documentation](https://docs.trychroma.com/)
- **Học thuật**: [Pinecone Learning Center (Vector Database concepts)](https://www.pinecone.io/learn/)
- **Thư viện toán**: [NumPy Reference Guide](https://numpy.org/doc/stable/)
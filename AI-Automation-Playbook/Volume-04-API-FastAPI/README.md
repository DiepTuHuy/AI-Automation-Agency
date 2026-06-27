# Volume 04: API & FastAPI - Cổng Kết Nối & Đóng Gói Dịch Vụ AI

Một script Python chạy trên máy cá nhân không thể phục vụ hàng triệu người dùng. Để biến mô hình prompt và logic automation của bạn thành sản phẩm có thể thương mại hóa, bạn cần đóng gói chúng dưới dạng Web API. Volume này hướng dẫn bạn sử dụng FastAPI - framework phát triển API hiện đại, nhanh nhất của Python để xây dựng các API an toàn, ổn định và tự động sinh tài liệu chuẩn doanh nghiệp.

---

## 1. Learning Objectives (Mục tiêu học tập)
Sau khi hoàn thành Volume này, bạn sẽ:
- **Nắm vững RESTful**: Hiểu sâu các nguyên lý thiết kế API RESTful, cách sử dụng các phương thức HTTP và mã trạng thái (status codes).
- **Tự tin viết FastAPI**: Xây dựng được ứng dụng FastAPI hoàn chỉnh từ đầu, hỗ trợ xử lý bất đồng bộ (async/await).
- **Kiểm soát dữ liệu đầu vào**: Sử dụng Pydantic để tự động xác thực (validate) dữ liệu đầu vào và đầu ra của API.
- **Xử lý tệp tin chuyên nghiệp**: Xây dựng API tiếp nhận upload file (PDF, hình ảnh) tối ưu hiệu năng.
- **Bảo mật API**: Triển khai các phương thức xác thực như API Key và Bearer Token, cấu hình CORS Middleware bảo vệ API.

---

## 2. Prerequisites (Điều kiện tiên quyết)
- Hoàn thành Volume 03 (Python Automation).
- Đã cài đặt Python và hiểu cơ bản về HTTP Request.

---

## 3. Big Picture (Bức tranh tổng thể)
FastAPI đóng vai trò là chiếc cầu nối giữa thế giới bên ngoài (Frontend React, thiết bị di động, nền tảng tự động hóa như n8n) và hệ thống logic nội bộ (LLM Client, Python Scripts, Database).

```
[Frontend Client / n8n] ──(HTTP POST + Bearer Token)──> [FastAPI Server]
                                                               │
                                         (Pydantic Validation) │ (Async LLM calls)
                                                               ▼
                                                       [AI Agent Engine]
```

---

## 4. First Principles (Nguyên lý gốc)
- **API là một hợp đồng cam kết (Contract-driven)**: API đã public cho khách hàng thì cấu trúc dữ liệu không được tự ý thay đổi mà không báo trước (Versioning).
- **Không bao giờ tin tưởng Client**: Dữ liệu do người dùng gửi lên API có thể chứa mã độc hoặc bị lệch định dạng. Việc xác thực chặt chẽ ở lớp Gateway (Pydantic) là bắt buộc.
- **Statelessness (Không trạng thái)**: Mỗi request gửi lên API phải chứa đầy đủ thông tin xác thực và ngữ cảnh. Server không lưu giữ trạng thái session của client để dễ dàng mở rộng quy mô (Scale-out).

---

## 5. Mental Models (Mô hình tư duy)
- **Người gác cổng nhà hàng (FastAPI + Pydantic)**: Hãy tưởng tượng FastAPI như một nhà hàng sang trọng. Khách hàng gửi yêu cầu (Request) vào. Pydantic đóng vai trò người gác cửa: kiểm tra xem khách có mặc đúng trang phục yêu cầu không (đúng kiểu dữ liệu), nếu không đúng sẽ mời ra ngoài ngay lập tức (Lỗi 422 Unprocessable Entity) mà không cần làm phiền đầu bếp (LLM Engine) bên trong.

---

## 6. Core Concepts (Khái niệm cốt lõi)
1. **FastAPI**: Web framework viết bằng Python, tận dụng kiểu dữ liệu Type Hints để tự động hóa việc sinh tài liệu Swagger UI.
2. **Pydantic**: Thư viện phân tích cú pháp và xác thực dữ liệu nhanh nhất của Python.
3. **CORS (Cross-Origin Resource Sharing)**: Cơ chế bảo mật của trình duyệt ngăn chặn việc một trang web ở tên miền khác gọi API của bạn trừ khi được cấp phép rõ ràng.

---

## 8. Best Practices (Quy chuẩn thực chiến)
- **Luôn sử dụng `UploadFile` thay vì `bytes`**: Đối với tác vụ nhận file, `UploadFile` ghi dữ liệu tạm ra đĩa cứng khi file quá dung lượng RAM, tránh làm sập server do cạn kiệt bộ nhớ.
- **Sử dụng Dependency Injection**: Sử dụng tính năng `Depends` của FastAPI để quản lý kết nối Database hoặc kiểm tra Token xác thực tập trung.
- **Khai báo kiểu dữ liệu rõ ràng (Type Hinting)**: Giúp FastAPI tự động tạo tài liệu API tương tác Swagger tại đường dẫn `/docs`.

---

## 9. Common Mistakes (Sai lầm thường gặp)
- **Thiếu CORS Middleware**: Dẫn đến việc lập trình viên Frontend gọi API từ local React app (`localhost:3000`) bị trình duyệt block hoàn toàn. *Cách sửa*: Cấu hình `CORSMiddleware` cho phép các nguồn gốc được phép.
- **Đặt logic nặng chạy đồng bộ trực tiếp trong Endpoint**: Chạy hàm đọc ghi file lớn đồng bộ làm block toàn bộ luồng xử lý của Uvicorn, khiến các request khác bị xếp hàng chờ. *Cách sửa*: Sử dụng từ khóa `async def` kết hợp với thư viện bất đồng bộ.

---

## 10. Engineering Mindset (Tư duy kỹ sư)
Một kỹ sư API thiết kế endpoint thân thiện với lập trình viên khác sử dụng: đặt tên route theo danh từ số nhiều (ví dụ: `POST /api/v1/summaries`), trả về cấu trúc lỗi chuẩn (ví dụ: `{ "detail": "Không tìm thấy file" }`), và luôn có tài liệu hướng dẫn tham chiếu đầy đủ.

---

## 13. Capstone Project (Dự án kết khóa Volume)
Xây dựng API Backend trích xuất CV tự động: API có endpoint `/api/v1/cv/extract` nhận file PDF/DOCX ứng viên, trích xuất text, gửi qua LLM để lấy thông tin có cấu trúc (Họ tên, SĐT, Kỹ năng, Kinh nghiệm) bằng Pydantic, và trả về dữ liệu JSON sạch. API được bảo mật bằng cơ chế API Key xác thực.

---

## 14. Review Questions (Bloom Taxonomy - 30 câu hỏi)
### Level 1 — Remember (Nhớ)
1. FastAPI là gì?
2. Sự khác biệt giữa Uvicorn và FastAPI là gì?
3. Swagger UI là gì và đường dẫn mặc định của nó trong FastAPI là gì?
4. CORS là viết tắt của từ gì?
5. Mã HTTP 422 biểu thị lỗi gì?

### Level 2 — Understand (Hiểu)
6. Giải thích sự khác biệt giữa Path Parameter và Query Parameter trong thiết kế URL API.
7. Tại sao Pydantic lại đóng vai trò quan trọng trong việc xác thực dữ liệu cho FastAPI?
8. Tại sao việc sử dụng `async def` lại có lợi thế lớn khi gọi các API của bên thứ ba như OpenAI?
9. Phân biệt cách xử lý file upload bằng `bytes` và `UploadFile`.
10. Cơ chế Dependency Injection trong FastAPI hoạt động như thế nào?

### Level 3 — Apply (Áp dụng)
11. Tạo một ứng dụng FastAPI đơn giản chạy trên cổng 8000 chứa một route GET `/` trả về JSON `{"message": "Hello"}`.
12. Định nghĩa một Pydantic model cho đối tượng `Product` gồm: `id` (int), `name` (str), `price` (float, phải lớn hơn 0), và `tags` (danh sách string).
13. Viết một API POST `/api/v1/analyze` nhận payload là class `Product` trên và in thông tin ra terminal.
14. Thiết lập CORS Middleware cho phép mọi nguồn truy cập (đáp ứng môi trường phát triển thử nghiệm).
15. Tạo một hàm kiểm tra API Key thông qua HTTP Header `X-API-Key` sử dụng Dependency Injection (`Depends`).

### Level 4 — Analyze (Phân tích)
16. Phân tích nguyên nhân tại sao việc đặt tên endpoint dạng động詞 (ví dụ: `/getProducts`) lại không đúng chuẩn RESTful.
17. So sánh hiệu năng của FastAPI với các framework truyền thống như Flask hay Django trong các tác vụ I/O bound.
18. Đánh giá rủi ro bảo mật khi bật CORS cho phép tất cả các domain (`allow_origins=["*"]`) trên môi trường Production.
19. Phân tích cách FastAPI tự động chuyển đổi lỗi xác thực của Pydantic thành phản hồi JSON trả về cho Client.
20. Tại sao việc sử dụng biến môi trường (Environment Variables) trong FastAPI lại quan trọng đối với việc chuyển đổi từ Staging sang Production?

### Level 5 — Design (Thiết kế)
21. Thiết kế kiến trúc API cho một hệ thống AI Chatbot gồm các endpoint: tạo hội thoại, gửi tin nhắn, lấy lịch sử chat.
22. Đề xuất giải pháp giới hạn kích thước file upload tối đa là 5MB trong FastAPI và trả về mã lỗi 400 nếu vượt quá.
23. Thiết kế hệ thống phân quyền cơ bản (Admin/User) cho các endpoint sử dụng JWT Token trong FastAPI.
24. Đề xuất quy trình xử lý lỗi tập trung sử dụng `@app.exception_handler` để định dạng lại mọi thông báo lỗi hệ thống gửi về cho frontend.
25. Thiết kế cấu trúc lưu trữ file upload tạm thời trên server trước khi đồng bộ lên cloud storage (S3).

### Level 6 — Evaluate (Đánh giá)
26. Đánh giá tính sẵn sàng của FastAPI đối với dự án enterprise lớn đòi hỏi khả năng scale cao.
27. Đánh giá sự đánh đổi giữa việc tự viết logic xác thực dữ liệu bằng code thuần và việc dùng Pydantic.
28. Kiểm chứng độ an toàn bảo mật của việc sử dụng API Key tĩnh lưu trong file `.env` đối với ứng dụng di động công cộng.
29. Đánh giá hiệu năng của FastAPI khi xử lý 1,000 requests upload file đồng thời trên một server cấu hình thấp.
30. So sánh và lựa chọn phương thức truyền tải dữ liệu lớn: Server-Sent Events (SSE) vs WebSockets trong FastAPI đối với ứng dụng AI Chatbot thời gian thực.

---

## 15. Checklist hoàn thành
- [ ] Dựng được ứng dụng FastAPI chạy trên local với Uvicorn.
- [ ] Viết được các API GET/POST chuẩn xác thực dữ liệu đầu vào bằng Pydantic.
- [ ] Tiếp nhận và xử lý file upload an toàn.
- [ ] Bảo mật API cơ bản bằng Header API Key.
- [ ] Trả lời đúng tối thiểu 80% câu hỏi ôn tập.

---

## 16. Resources (Tài liệu tham khảo)
- **Tài liệu chính thức**: [FastAPI Documentation](https://fastapi.tiangolo.com/)
- **Đọc thêm**: [Pydantic Docs](https://docs.pydantic.dev/latest/)
- **Tiêu chuẩn**: [REST API Tutorial](https://restfulapi.net/)

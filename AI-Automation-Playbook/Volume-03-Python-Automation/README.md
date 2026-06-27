# Volume 03: Python Automation - Xương Sườn của Hệ Thống Tự Động Hóa

AI chỉ có thể làm bộ não suy nghĩ, còn Python là tay chân giúp AI tương tác với thế giới bên ngoài. Trong Volume này, bạn sẽ học cách viết code Python chuẩn lập trình chuyên nghiệp để xử lý file, thao tác dữ liệu cấu trúc lớn, gọi các API bên thứ ba và thực thi bất đồng bộ (Asynchronous) để tối ưu hóa hiệu năng hệ thống.

---

## 1. Learning Objectives (Mục tiêu học tập)
Sau khi hoàn thành Volume này, bạn sẽ:
- **Làm chủ cấu trúc file**: Sử dụng thư viện `pathlib` để làm việc với tệp tin và đường dẫn đa nền tảng (Mac/Windows/Linux) mà không lỗi.
- **Tương tác API chuẩn xác**: Thành thạo thư viện `requests` để gửi nhận dữ liệu với bất kỳ REST API nào.
- **Xử lý bất đồng bộ (Concurrency)**: Sử dụng `asyncio` để thực hiện hàng trăm lượt gọi API song song, giảm 90% thời gian chờ đợi.
- **Thao tác dữ liệu lớn**: Dùng `pandas` để đọc, xử lý và làm sạch dữ liệu từ Excel/CSV trước khi đưa vào AI.
- **Xây dựng hệ thống giám sát**: Cấu hình hệ thống lưu vết (`logging`) chuẩn Production thay thế hoàn toàn cho câu lệnh `print()`.

---

## 2. Prerequisites (Điều kiện tiên quyết)
- Hoàn thành Volume 01 và Volume 02.
- Nắm vững cú pháp cơ bản của Python (Biến, Vòng lặp, Hàm).

---

## 3. Big Picture (Bức tranh tổng thể)
Python hoạt động như một chất keo kết nối: Đọc dữ liệu từ file cứng -> Sử dụng Pandas làm sạch -> Gửi bất đồng bộ lên LLM API -> Lưu kết quả vào file JSON hoặc gửi tới hệ thống bên thứ ba qua API.

```
[CSV / Excel Files] ─(Pandas)─> [Python Async Pipeline] ─(Requests)─> [LLMs API]
                                         │
                                         ▼ (Logging & Error Handling)
                               [Discord / Slack Notifications]
```

---

## 4. First Principles (Nguyên lý gốc)
- **I/O Bound là nút cổ chai**: Phần lớn thời gian của hệ thống AI Automation là chờ phản hồi từ Internet (API, Webhook, DB). Viết code đồng bộ (Synchronous) sẽ block toàn bộ CPU một cách lãng phí.
- **Đừng tin tưởng dữ liệu đầu vào**: Dữ liệu từ file CSV, API bên ngoài luôn có nguy cơ bị trống (null), sai định dạng hoặc lỗi ký tự (encoding).
- **Hộp đen logging**: Một hệ thống tự chạy trên cloud mà không có logging giống như lái xe trong đêm tối tắt đèn pha. Khi xảy ra lỗi, bạn không có cách nào biết hệ thống chết ở dòng code nào.

---

## 5. Mental Models (Mô hình tư duy)
- **Bàn làm việc đồng bộ vs Bếp nhà hàng bất đồng bộ**: Code đồng bộ giống như một người phục vụ chỉ nhận order của bàn số 1, bê vào bếp đợi nấu xong, bê ra cho khách rồi mới sang bàn số 2. Code bất đồng bộ (`asyncio`) giống như một đầu bếp chuyên nghiệp: nướng bánh trong lò, trong lúc đợi bánh chín thì đi thái thịt, trong lúc thịt chín thì pha nước sốt. Mọi việc chạy song song hiệu quả.

---

## 6. Core Concepts (Khái niệm cốt lõi)
1. **Pathlib**: Thư viện xử lý đường dẫn hướng đối tượng, tự động định dạng dấu gạch chéo `/` hoặc `\` tùy thuộc vào hệ điều hành đang chạy.
2. **Event Loop & Coroutine**: Trái tim của lập trình bất đồng bộ Python, quản lý việc chuyển đổi giữa các tác vụ đang chờ I/O.
3. **Structured Logging**: Ghi chép nhật ký hệ thống kèm timestamp, cấp độ lỗi (INFO, WARNING, ERROR) và lưu ra file để truy vết.

---

## 8. Best Practices (Quy chuẩn thực chiến)
- **Sử dụng môi trường ảo (`.venv`)**: Luôn tạo môi trường ảo cho mỗi dự án để tránh xung đột phiên bản thư viện.
- **Luôn đóng kết nối (Context Managers)**: Sử dụng cú pháp `with open(...)` để Python tự động giải phóng tài nguyên hệ thống sau khi đọc ghi file kết thúc.
- **Tuyệt đối không hardcode API Key**: Luôn lưu key bảo mật trong file `.env` và đọc bằng `os.getenv()`.

---

## 9. Common Mistakes (Sai lầm thường gặp)
- **Sử dụng `print()` để debug trên server**: Khi deploy lên server (như Docker/VPS), các lệnh `print()` sẽ bị trôi mất hoặc chiếm bộ nhớ đệm mà không có phân loại mức độ nghiêm trọng của lỗi. *Cách sửa*: Chuyển sang dùng thư viện `logging`.
- **Quên xử lý Exception ngoại lệ HTTP**: Gửi request tới API bên ngoài mà không đặt trong khối `try-except` dẫn đến việc toàn bộ chương trình crash khi mất mạng hoặc API bên kia bị nghẽn. *Cách sửa*: Luôn bắt `requests.exceptions.RequestException`.

---

## 10. Engineering Mindset (Tư duy kỹ sư)
Một kỹ sư tự động hóa viết code để chạy bền bỉ suốt 365 ngày mà không cần giám sát. Họ luôn viết code với tư định nghĩa rõ ràng: *"Nếu bước này lỗi, hệ thống sẽ retry mấy lần? Sau đó báo cáo lỗi qua kênh nào (Slack/Email) và tiếp tục xử lý các phần việc khác như thế nào?"*

---

## 13. Capstone Project (Dự án kết khóa Volume)
Xem mô tả chi tiết tại [Project-01](file:///Users/dieptuhuy/Documents/AI%20Automation/AI-Automation-Playbook/Projects/Project-01-AI-Meeting-Summary-Email-Assistant/README.md).

---

## 14. Review Questions (Bloom Taxonomy - 30 câu hỏi)
### Level 1 — Remember (Nhớ)
1. Thư viện nào của Python được khuyến nghị để xử lý đường dẫn tệp tin?
2. Sự khác biệt giữa `requests.get()` và `requests.post()` là gì?
3. JSON là viết tắt của cụm từ gì?
4. Ý nghĩa của từ khóa `async` và `await` trong Python là gì?
5. DataFrame trong Pandas là cấu trúc dữ liệu mấy chiều?

### Level 2 — Understand (Hiểu)
6. Tại sao sử dụng `pathlib` lại tốt hơn việc ghép chuỗi đường dẫn thủ công (ví dụ: `path + "/" + filename`)?
7. Giải thích sự khác biệt giữa các cấp độ logging: DEBUG, INFO, WARNING, ERROR, CRITICAL.
8. Khi nào nên dùng lập trình bất đồng bộ (`asyncio`) thay vì đa tiến trình (multiprocessing)?
9. Giải thích khái niệm Serialization và Deserialization của JSON.
10. Tại sao Pandas lại được coi là công cụ chuẩn để xử lý và làm sạch dữ liệu bảng?

### Level 3 — Apply (Áp dụng)
11. Viết code tạo một thư mục mới có tên `logs` nằm bên trong thư mục hiện tại nếu nó chưa tồn tại bằng `pathlib`.
12. Gửi một HTTP POST request chứa dữ liệu JSON đến một mock API và lấy mã trạng thái (status code) trả về.
13. Đọc một file cấu hình JSON từ đĩa cứng, thay đổi giá trị một thuộc tính, và ghi đè lại file đó.
14. Sử dụng `asyncio.gather` để chạy song song 3 hàm ngủ (`asyncio.sleep`) với thời gian khác nhau và đo tổng thời gian thực thi.
15. Cấu hình logger ghi log đồng thời ra cả màn hình console và file `debug.log`.

### Level 4 — Analyze (Phân tích)
16. Phân tích nguyên nhân tại sao một script đồng bộ tải 100 trang web mất 50 giây, trong khi phiên bản async chỉ mất 3 giây.
17. So sánh sự khác biệt khi dùng `requests` và `aiohttp` để gọi API trong một ứng dụng async.
18. Đánh giá tính an toàn khi sử dụng hàm `json.loads()` đối với dữ liệu không rõ nguồn gốc từ người dùng nhập.
19. Phân tích sự ảnh hưởng của việc log quá nhiều thông tin cấp độ DEBUG đối với dung lượng ổ cứng của server Production.
20. Tại sao việc thao tác trên Pandas DataFrame lại nhanh hơn rất nhiều so với dùng vòng lặp `for` lồng nhau trên list Python truyền thống?

### Level 5 — Design (Thiết kế)
21. Thiết kế một hệ thống quản lý file tạm tự động dọn dẹp các tệp tin cũ hơn 7 ngày.
22. Thiết kế module API Client hỗ trợ cơ chế tự động thử lại (Retry) kèm theo độ trễ tăng dần (Exponential Backoff) khi gặp lỗi kết nối mạng.
23. Đề xuất sơ đồ luồng dữ liệu xử lý lỗi bất đồng bộ khi một trong số 10 tác vụ chạy song song bị thất bại giữa chừng.
24. Thiết kế cấu trúc bảng log (Log Schema) để dễ dàng truy vấn lỗi theo phiên người dùng (Session ID).
25. Đề xuất quy trình làm sạch dữ liệu khách hàng từ file Excel bị mất số điện thoại và trùng lặp email bằng Pandas.

### Level 6 — Evaluate (Đánh giá)
26. Đánh giá hiệu năng và mức độ phức tạp khi chuyển đổi một hệ thống ETL (Extract-Transform-Load) từ đồng bộ sang bất đồng bộ.
27. Đánh giá sự đánh đổi giữa việc dùng thư viện log có sẵn của Python và các thư viện bên thứ ba như Loguru.
28. Đánh giá hiệu quả của việc tiền lọc dữ liệu bằng Pandas trước khi gửi dữ liệu sang mô hình RAG để giảm thiểu chi phí API.
29. Phản biện luận điểm: *"Mọi tác vụ lặp lại trong doanh nghiệp đều nên viết script Python để tự động hóa"*.
30. Đánh giá độ tin cậy của mã nguồn Python tự động hóa khi chạy trên môi trường Windows so với môi trường Linux VPS.

---

## 15. Checklist hoàn thành
- [ ] Thành thạo thao tác file với pathlib không lỗi đường dẫn.
- [ ] Biết gọi API và xử lý JSON linh hoạt.
- [ ] Viết được mã nguồn bất đồng bộ gọi song song nhiều tác vụ.
- [ ] Thiết lập hệ thống logging cho mọi dự án.
- [ ] Hoàn thành Capstone Project (Project 01).

---

## 16. Resources (Tài liệu tham khảo)
- **Tài liệu**: [Python Official Documentation](https://docs.python.org/3/)
- **Đọc thêm**: *Automate the Boring Stuff with Python by Al Sweigart.*
- **Pandas**: [Pandas User Guide](https://pandas.pydata.org/docs/user_guide/index.html)

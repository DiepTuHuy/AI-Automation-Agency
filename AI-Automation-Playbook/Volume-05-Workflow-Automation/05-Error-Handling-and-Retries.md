# Chương 05: Xây dựng Hệ thống Chịu lỗi & Cảnh báo Lỗi trung tâm

## 1. Deep Dive (Phân tích chuyên sâu)

### Tại sao các luồng tự động hóa hay bị lỗi ngầm?
Trong thế giới thực, API của các hệ thống B2B thường xuyên gặp sự cố:
- Hạn mức API của bạn bị cạn (Rate Limit).
- Server của đối tác bảo trì đột xuất.
- File CSV tải lên bị mất cột dữ liệu cần thiết gây lỗi code.

Nếu bạn không thiết kế cơ chế xử lý lỗi, workflow n8n của bạn sẽ dừng chạy đột ngột, dữ liệu khách hàng bị treo lơ lửng, và bạn không hề biết cho đến khi khách hàng khiếu nại.

### Các chiến lược chống lỗi của n8n
1. **On Fail: Retry (Thử lại tự động)**: Cấu hình cho node tự động gửi lại request sau một khoảng thời gian nếu gặp sự cố kết nối mạng tạm thời.
2. **On Fail: Continue (Bỏ qua lỗi)**: Cho phép luồng chạy tiếp sang node sau dù node hiện tại bị lỗi (phù hợp cho các tác vụ không quan trọng, ví dụ gửi log).
3. **Error Trigger Node (Bắt lỗi toàn cục)**: Một workflow chuyên biệt lắng nghe lỗi từ tất cả các workflow khác, tự động thu thập thông tin lỗi (tên workflow, node gây lỗi, thông báo lỗi) và gửi thông báo khẩn cấp cho đội kỹ thuật.

---

## 2. Demo: Thiết lập Workflow Cảnh báo Lỗi trung tâm về Telegram

### Mục tiêu
Xây dựng một workflow lắng nghe mọi lỗi phát sinh trong hệ thống n8n và tự động gửi tin nhắn báo động chi tiết đến Telegram của Admin kỹ thuật.

### Các bước thực hiện
1. Tạo một workflow mới tên là `Centralized Error Handler`.
2. Kéo node **Error Trigger** làm điểm khởi đầu. Node này tự động bắt các lỗi từ các workflow khác khi được liên kết.
3. Kết nối node này với một node **HTTP Request** để gửi tin nhắn Telegram.
4. Cấu hình nội dung tin nhắn gửi đi sử dụng các biến lỗi động của n8n:
   ```markdown
   🚨 *CẢNH BÁO LỖI HỆ THỐNG n8n* 🚨
   
   - *Workflow:* {{ $json.workflow.name }} (ID: {{ $json.workflow.id }})
   - *Node gây lỗi:* {{ $json.execution.error.node.name }}
   - *Thông báo lỗi:* `{{ $json.execution.error.message }}`
   - *Thời gian:* {{ $json.execution.lastActive }}
   ```
5. Kích hoạt (Active) workflow cảnh báo lỗi này.
6. Mở một workflow test khác, cố tình cấu hình sai một node HTTP Request để gây lỗi, bật liên kết xử lý lỗi tới `Centralized Error Handler` và kiểm tra tin nhắn Telegram báo về tức thì.

---

## 3. Mini Project

### Bài tập 1: Cấu hình Retry khi gọi API thất bại (Mức độ: Trung bình)
* **Đề bài**: Hãy thiết kế một workflow n8n gọi một API giả lập có tỷ lệ lỗi cao. Cấu hình Node HTTP Request để tự động thử lại (Retry) 3 lần, mỗi lần cách nhau 5 giây trước khi thực sự báo lỗi.
* **Tài liệu hướng dẫn & Sườn mẫu Workflow**:
```markdown
# Cấu hình Error Handling trên Node n8n

### 1. Các bước cấu hình Settings:
1. Mở cài đặt chi tiết của Node HTTP Request.
2. Chọn tab **Settings**.
3. Bật tùy chọn **On Fail** -> Chọn `Retry`.
4. Cấu hình:
   * **Number of Retries**: 3
   * **Delay Between Retries (ms)**: 5000
```

### Bài tập 2: Tự động gửi cảnh báo Slack khi lỗi sập hệ thống (Mức độ: Khó)
* **Đề bài**: Thiết kế một workflow tổng đài xử lý lỗi. Khi bất kỳ node nào trong workflow chính bị lỗi, tự động chuyển hướng luồng xử lý sang một Sub-workflow riêng chuyên gửi cảnh báo lỗi chi tiết (gồm tên Node lỗi, mã lỗi) sang Telegram hoặc Email.
* **Yêu cầu**: Học viên tự hoàn thành không có tài liệu mẫu.
* **Gợi ý triển khai (Workflow Hints)**:
  - Sử dụng tính năng **Error Trigger** Node để bắt mọi lỗi xảy ra trong Workflows của hệ thống n8n.
  - Đọc thông tin lỗi từ payload của Error Trigger Node để tạo nội dung cảnh báo chi tiết.


# Chương 01: Nguyên lý thiết kế REST API chuẩn quốc tế

## 1. Deep Dive (Phân tích chuyên sâu)

### REST (Representational State Transfer) là gì?
REST là một phong cách kiến trúc phần mềm định nghĩa tập hợp các ràng buộc để xây dựng Web Services. Một API tuân thủ các nguyên lý REST được gọi là **RESTful API**.

### Các nguyên tắc vàng trong thiết kế REST API
1. **Sử dụng danh từ làm tài nguyên (Resource-oriented)**: Đường dẫn URL đại diện cho tài nguyên thực thể, không đại diện cho hành động.
   - *Sai*: `GET /get_all_customers`
   - *Đúng*: `GET /customers`
2. **Sử dụng đúng HTTP Methods**:
   - `GET /customers`: Lấy danh sách khách hàng.
   - `POST /customers`: Tạo mới khách hàng.
   - `PUT /customers/123`: Cập nhật toàn bộ thông tin khách hàng ID 123.
   - `DELETE /customers/123`: Xóa khách hàng ID 123.
3. **Statelessness (Không lưu trạng thái)**: Mỗi request gửi lên server phải độc lập và chứa toàn bộ thông tin cần thiết để xử lý (như authentication token). Server không lưu session của client.
4. **Phân cấp phiên bản (Versioning)**: Luôn khai báo phiên bản trên đường dẫn để tránh làm gãy ứng dụng của khách hàng cũ khi nâng cấp hệ thống.
   - *Ví dụ*: `/api/v1/models`

---

## 2. Demo: Phác thảo thiết kế API Spec chuẩn OpenAPI

### Mục tiêu
Viết tài liệu thiết kế API (API Specification) cho tính năng phân tích tài liệu bằng AI sử dụng cú pháp YAML chuẩn OpenAPI 3.0.

### Nội dung thiết kế (`openapi.yaml`)
```yaml
openapi: 3.0.0
info:
  title: AI Document Analyzer API
  version: 1.0.0
  description: API cung cấp dịch vụ phân tích hóa đơn và hợp đồng tự động.
paths:
  /api/v1/documents:
    post:
      summary: Gửi tài liệu phân tích mới
      requestBody:
        required: true
        content:
          multipart/form-data:
            schema:
              type: object
              properties:
                file:
                  type: string
                  format: binary
                  description: File PDF hoặc ảnh hóa đơn cần phân tích.
      responses:
        '202':
          description: Đã tiếp nhận yêu cầu phân tích, đang xử lý ngầm (async).
          content:
            application/json:
              schema:
                type: object
                properties:
                  task_id:
                    type: string
                    example: "task_abc123"
                  status:
                    type: string
                    example: "processing"
```

---

## 3. Mini Project
Hãy tự thiết kế một bản đặc tả API (API Spec) đầy đủ cho hệ thống Quản lý Agent hỗ trợ khách hàng, bao gồm các endpoint để: tạo cuộc hội thoại mới, gửi tin nhắn của khách hàng, và lấy lịch sử tin nhắn của cuộc hội thoại đó. Ghi tài liệu này ra file Markdown.

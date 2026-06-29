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

### Bài tập 1: Thiết kế đặc tả API cho hệ thống đặt phòng khách sạn (Mức độ: Trung bình)
* **Đề bài**: Hãy thiết kế một bản tài liệu đặc tả API (API Spec) bằng định dạng Markdown cho hệ thống quản lý đặt phòng khách sạn. Đặc tả cần tuân thủ nghiêm ngặt 5 nguyên tắc thiết kế REST API đã học (sử dụng đúng HTTP Method, định dạng URI danh từ số nhiều, trả về HTTP status code phù hợp).
* **Tài liệu sườn mẫu (`hotel_api_spec.md`)**:
```markdown
# Tài liệu đặc tả API quản lý đặt phòng (RESTful Spec)

### 1. Lấy danh sách phòng trống
* **URL**: `/api/v1/rooms`
* **Method**: `GET`
* **Params**: `status=available`
* **Response (200 OK)**:
```json
[
  {"id": 101, "type": "Deluxe", "price_per_night": 120.0, "status": "available"}
]
```

### 2. Tạo đơn đặt phòng mới
* **URL**: `/api/v1/bookings`
* **Method**: `POST`
* **Payload**:
```json
{
  "room_id": 101,
  "customer_name": "Nguyen Van A",
  "check_in_date": "2026-07-01",
  "nights": 3
}
```
* **Response (201 Created)**:
```json
{
  "booking_id": "BK-9982",
  "status": "confirmed"
}
```
```

### Bài tập 2: Thiết kế hệ thống API quản lý kho hàng thương mại điện tử (Mức độ: Khó)
* **Đề bài**: Hãy viết tài liệu đặc tả API thiết kế hệ thống quản lý kho (Inventory). Đặc tả phải bao gồm đầy đủ các API: Lấy thông tin tồn kho của một sản phẩm, Cập nhật số lượng kho hàng khi có đơn mới, Báo cáo các sản phẩm sắp hết hàng. Chú ý thiết kế các endpoint có cấu trúc lồng nhau hợp lệ (Nested Resources).
* **Yêu cầu**: Bạn hãy tự hoàn thành không có tài liệu mẫu.
* **Gợi ý triển khai (Workflow Hints)**:
  1. Định nghĩa endpoint lồng nhau cho sản phẩm và tồn kho, ví dụ: `/api/v1/products/{product_id}/inventory`.
  2. Xác định các HTTP Method phù hợp: `GET` để truy vấn, `PATCH` hoặc `PUT` để cập nhật số lượng tồn kho.
  3. Lựa chọn các mã lỗi chuẩn như `404 Not Found` khi sản phẩm không tồn tại, hoặc `400 Bad Request` khi cập nhật số lượng âm.

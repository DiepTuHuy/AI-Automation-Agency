# Cấu hình n8n Webhook Listener

### 1. Cấu hình Webhook Node:
* **HTTP Method**: `POST`
* **Path**: `woo-order-created`
* **Response Mode**: `On Received` với status `200` để báo nhận thành công lập tức.

### 2. Cách kiểm thử:
1. Bấm nút "Listen for test event" trên n8n.
2. Sử dụng Postman hoặc Curl gửi một request POST giả lập dữ liệu đơn hàng tới URL Webhook Test của n8n.
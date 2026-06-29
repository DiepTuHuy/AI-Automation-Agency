# Cấu hình Error Handling trên Node n8n

### 1. Các bước cấu hình Settings:
1. Mở cài đặt chi tiết của Node HTTP Request.
2. Chọn tab **Settings**.
3. Bật tùy chọn **On Fail** -> Chọn `Retry`.
4. Cấu hình:
   * **Number of Retries**: 3
   * **Delay Between Retries (ms)**: 5000
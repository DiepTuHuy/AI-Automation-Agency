# Cấu hình HTTP Request gọi API ngoài

### 1. HTTP Request Node:
* **Method**: `GET`
* **URL**: `https://api.open-meteo.com/v1/forecast?latitude=21.0285&longitude=105.8542&current_weather=true`
* **Authentication**: None (API công cộng).

### 2. Trích xuất dữ liệu:
* Dữ liệu trả về sẽ nằm trong biến: `{{ $json.current_weather.temperature }}`.
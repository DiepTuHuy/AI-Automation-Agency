# Chương 04: Thao tác dữ liệu nâng cao bằng JavaScript Code Node

## 1. Deep Dive (Phân tích chuyên sâu)

### Cấu trúc dữ liệu "Items" của n8n
Một trong những điểm gây bối rối nhất của n8n là cách nó quản lý dữ liệu. n8n luôn coi dữ liệu di chuyển giữa các node là một **Mảng danh sách các phần tử (Array of Items)**:
```json
[
  {
    "json": {
      "name": "Nguyen Van A",
      "email": "a@example.com"
    }
  },
  {
    "json": {
      "name": "Tran Thi B",
      "email": "b@example.com"
    }
  }
]
```

### Node Code (JavaScript) trong n8n
Khi bạn cần thực hiện các thuật toán biến đổi dữ liệu phức tạp (ví dụ: gộp hai danh sách, định dạng lại định dạng ngày tháng, hoặc lọc bỏ các ký tự đặc biệt) mà các node kéo thả thông thường không làm được, bạn cần dùng node **Code**.
n8n cho phép bạn viết JavaScript hiện đại (ES6+) chạy trực tiếp trên môi trường NodeJS của container.

---

## 2. Demo: Gộp và chuẩn hóa danh sách khách hàng hàng loạt

### Mục tiêu
Nhận một mảng dữ liệu khách hàng thô bị sai định dạng tên và email, sử dụng JavaScript để chuẩn hóa và lọc ra các khách hàng hợp lệ.

### Mã nguồn JavaScript trong n8n Code Node
```javascript
// Dữ liệu đầu vào tự động được gán vào mảng `item` của hàm
const inputItems = $input.all();

const processedItems = inputItems.map(item => {
    let rawData = item.json;
    
    // 1. Chuẩn hóa tên (Viết hoa chữ cái đầu và xóa khoảng trắng thừa)
    let cleanedName = rawData.name.trim().toLowerCase().replace(/(^|\s)\S/g, l => l.toUpperCase());
    
    // 2. Chuẩn hóa email về chữ thường
    let cleanedEmail = rawData.email.trim().toLowerCase();
    
    // Trả về định dạng đúng quy chuẩn của n8n
    return {
        json: {
            name: cleanedName,
            email: cleanedEmail,
            source: rawData.source || "Unknown",
            processed_at: new Date().toISOString()
        }
    };
});

return processedItems;
```

---

## 3. Mini Project
Hãy viết một script trong node Code nhận vào danh sách các giao dịch (mỗi giao dịch có: tên sản phẩm, số tiền). Hãy viết logic tính tổng số tiền của toàn bộ các giao dịch, và xuất ra một kết quả duy nhất chứa trường `total_revenue` và mảng danh sách tên các sản phẩm đã mua.

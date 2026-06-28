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

### Bài tập 1: Viết JS Code chuẩn hóa định dạng số điện thoại trong n8n (Mức độ: Trung bình)
* **Đề bài**: Viết một đoạn code JavaScript trong n8n Node (Code Node) để chuẩn hóa danh sách số điện thoại của khách hàng về định dạng chuẩn quốc tế `+84...`.
* **Mã nguồn mẫu (`n8n_code_standardizer.js`)**:
```javascript
// JS code chạy trong Code Node của n8n
for (const item of $input.all()) {
  let phone = item.json.phone_number;
  if (phone) {
    // Loại bỏ ký tự đặc biệt
    phone = phone.replace(/[\s-.()]/g, '');
    // Chuyển 0 đầu thành +84
    if (phone.startsWith('0')) {
      phone = '+84' + phone.substring(1);
    }
    item.json.phone_normalized = phone;
  } else {
    item.json.phone_normalized = 'N/A';
  }
}
return $input.all();
```

### Bài tập 2: Tính tổng doanh thu và chia sẻ hoa hồng tự động (Mức độ: Khó)
* **Đề bài**: Viết một đoạn code JS trong Code Node để xử lý danh sách 10 giao dịch của đại lý. Tính tổng doanh thu và tự động phân chia 10% hoa hồng cho từng đại lý tương ứng dưới dạng danh sách đối tượng mới.
* **Yêu cầu**: Học viên tự hoàn thành không có code mẫu.
* **Gợi ý triển khai (Workflow Hints)**:
  - Sử dụng vòng lặp `for...of` duyệt qua danh sách các items của `$input.all()`.
  - Tính toán trường dữ liệu mới: `item.json.commission = item.json.amount * 0.1`.
  - Return lại mảng kết quả hoàn chỉnh để chuyển tiếp cho các node tiếp theo.


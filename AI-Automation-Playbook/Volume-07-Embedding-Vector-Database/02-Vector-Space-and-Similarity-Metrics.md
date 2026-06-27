# Chương 02: Các phép toán tính khoảng cách và Độ tương đồng Vector

## 1. Deep Dive (Phân tích chuyên sâu)

Khi đã biểu diễn văn bản dưới dạng các vector tọa độ, làm thế nào để thuật toán so sánh xem hai văn bản có gần nghĩa nhau không? Chúng ta sử dụng các phép đo khoảng cách toán học:

### 1. Cosine Similarity (Độ tương đồng Cosine)
Đo góc giữa hai vector trong không gian nhiều chiều, bất kể độ dài của vector.
- **Công thức**:
  $$	ext{Cosine Similarity} = rac{A \cdot B}{\|A\| \|B\|}$$
- **Giá trị**: Từ -1 đến 1. Trong so sánh văn bản, giá trị thường từ 0 (không liên quan) đến 1 (trùng lặp ý nghĩa).
- *Tại sao được ưa chuộng*: Phù hợp nhất cho văn bản vì nó không bị ảnh hưởng bởi độ dài ngắn của đoạn văn (độ dài vector).

### 2. Dot Product (Tích vô hướng)
Nếu hai vector đã được chuẩn hóa độ dài về 1 (L2 Normalized), Tích vô hướng tương đương hoàn toàn với Cosine Similarity nhưng có tốc độ tính toán nhanh hơn hàng chục lần vì bỏ qua được phép chia khai căn ở mẫu số.

### 3. Euclidean Distance (Khoảng cách L2)
Đo khoảng cách vật lý đường thẳng nối liền hai đầu mút vector. Khoảng cách càng nhỏ nghĩa là hai vector càng tương đồng.

---

## 2. Demo: Tính toán Cosine Similarity bằng NumPy

### Mục tiêu
Tính toán độ tương đồng ngữ nghĩa giữa các câu khác nhau để kiểm chứng trực quan bằng thư viện tính toán ma trận NumPy.

### Mã nguồn (`cosine_math.py`)
Cài đặt thư viện: `pip install numpy`

```python
import numpy as np

def calculate_cosine_similarity(vec_a: list, vec_b: list) -> float:
    # Chuyển đổi list Python thành array NumPy để tính toán ma trận
    a = np.array(vec_a)
    b = np.array(vec_b)
    
    # Tính tích vô hướng tử số
    dot_product = np.dot(a, b)
    
    # Tính độ dài của từng vector ở mẫu số
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    
    if norm_a == 0 or norm_b == 0:
        return 0.0
        
    return float(dot_product / (norm_a * norm_b))

if __name__ == "__main__":
    # Giả lập vector 3 chiều đơn giản để kiểm tra tính đúng đắn của hàm
    v1 = [1, 2, 3]
    v2 = [1, 2, 3] # Trùng nhau hoàn toàn -> Cosine phải bằng 1.0
    v3 = [-1, -2, -3] # Ngược nhau hoàn toàn -> Cosine phải bằng -1.0
    
    print(f"Độ tương đồng v1 và v2: {calculate_cosine_similarity(v1, v2):.2f}")
    print(f"Độ tương đồng v1 và v3: {calculate_cosine_similarity(v1, v3):.2f}")
```

---

## 3. Mini Project
Hãy kết hợp gọi API nhúng của OpenAI ở Chương 1 để viết script Python nhận vào 3 câu đầu vào tự chọn từ người dùng. Tính toán độ tương đồng Cosine Similarity giữa Câu 1 với Câu 2, và Câu 1 với Câu 3. Xuất ra màn hình báo cáo so sánh xem cặp câu nào gần nghĩa với nhau nhất.

# Chương 01: Vector Embeddings - Bản chất kỹ thuật

## 1. Deep Dive (Phân tích chuyên sâu)

### Máy tính hiểu ngôn ngữ thế nào?
Để máy tính có thể xử lý ngôn ngữ tự nhiên, ta phải chuyển đổi từ ngữ thành các con số.
- **Phương pháp cũ (One-hot encoding / Bag of words)**: Biểu diễn mỗi từ bằng một vector có độ dài bằng từ điển, chứa toàn số 0 và duy nhất một số 1 ở vị trí từ đó.
  - *Ví dụ*: "táo" -> `[1, 0, 0]`, "cam" -> `[0, 1, 0]`.
  - *Hạn chế*: Phép tính toán học giữa vector "táo" và "cam" sẽ cho khoảng cách bằng nhau như giữa "táo" và "lập trình". Máy tính hoàn toàn không hiểu mối tương quan ý nghĩa ngữ nghĩa giữa các từ.

### Vector nhúng mật độ cao (Dense Embeddings)
Mô hình Embedding (được huấn luyện trên kho văn bản khổng lồ) chuyển hóa mỗi từ hoặc đoạn văn thành một chuỗi số thực nhiều chiều (ví dụ: 1536 chiều). Mỗi chiều đại diện cho một thuộc tính ẩn ngữ nghĩa mà con người không thể định nghĩa trực tiếp.

Trong không gian này:
- Các từ liên quan chặt chẽ sẽ nằm sát nhau.
- Khoảng cách giữa các vector thể hiện mối quan hệ ngữ nghĩa thực tế.
- Hỗ trợ các phép toán tương tự lý thuyết: $	ext{Vector("Vua")} - 	ext{Vector("Nam")} + 	ext{Vector("Nữ")} pprox 	ext{Vector("Hoàng hậu")}$.

---

## 2. Demo: Gọi API tạo Vector bằng Python

### Mục tiêu
Gửi chuỗi văn bản lên OpenAI Embedding API, kiểm tra cấu trúc mảng số thực trả về và số lượng chiều của vector.

### Mã nguồn (`get_embedding.py`)
```python
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_text_embedding(text: str, model: str = "text-embedding-3-small") -> list:
    response = client.embeddings.create(
        input=[text],
        model=model
    )
    # Trích xuất mảng vector số thực từ JSON kết quả
    return response.data[0].embedding

if __name__ == "__main__":
    text_sample = "Xây dựng AI Agent tự động hóa quy trình nghiệp vụ."
    
    print("Đang tạo vector embedding...")
    vector = get_text_embedding(text_sample)
    
    print(f"\nKết quả thành công!")
    print(f"Kiểu dữ liệu đầu ra: {type(vector)}")
    print(f"Số lượng chiều (Dimensions) của vector: {len(vector)}")
    print(f"Preview 5 phần tử số thực đầu tiên: {vector[:5]}")
```

---

## 3. Mini Project
Hãy viết một script Python sinh vector embedding cho một danh sách gồm 5 câu khác nhau (trong đó có 3 câu cùng chủ đề công nghệ và 2 câu chủ đề ẩm thực). In ra màn hình để kiểm tra xem kiểu định dạng dữ liệu có đồng nhất không và lưu các vector này vào file JSON để phục vụ chương tiếp theo.

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
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

def get_text_embedding(text: str, model: str = "models/text-embedding-004") -> list:
    response = genai.embed_content(
        model=model,
        contents=[text],
        task_type="retrieval_document"
    )
    # Trích xuất mảng vector số thực từ JSON kết quả
    return response['embedding'][0]

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

### Bài tập 1: Tạo và lưu trữ Vector Embeddings hàng loạt (Mức độ: Trung bình)
* **Đề bài**: Viết một script Python sinh vector embedding cho một danh sách gồm 5 câu khác nhau (trong đó có 3 câu cùng chủ đề công nghệ và 2 câu chủ đề ẩm thực) bằng Gemini API. In ra màn hình kiểm tra số chiều của vector và lưu toàn bộ kết quả vào một file JSON cục bộ (`embeddings.json`).
* **Mã nguồn mẫu (`generate_batch_embeddings.py`)**:
```python
import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

sentences = [
    "Hệ thống AI Agent tự động hóa quy trình nghiệp vụ doanh nghiệp.",
    "Lập trình Python giúp xây dựng API nhanh chóng với FastAPI.",
    "Mô hình ngôn ngữ lớn hoạt động dựa trên cơ chế Attention.",
    "Phở bò Hà Nội là món ăn truyền thống nổi tiếng thế giới.",
    "Bánh mì kẹp thịt Việt Nam ngon và tiện lợi cho bữa sáng."
]

def save_embeddings_to_json(text_list: list, output_filepath: str):
    data_to_save = []
    
    for text in text_list:
        # Gọi Gemini embedding model
        response = genai.embed_content(
            model="models/text-embedding-004",
            contents=[text],
            task_type="retrieval_document"
        )
        vector = response['embedding'][0]
        data_to_save.append({
            "text": text,
            "embedding": vector
        })
        print(f"Đã nhúng câu: '{text[:20]}...' -> Vector {len(vector)} chiều.")
        
    with open(output_filepath, "w", encoding="utf-8") as f:
        json.dump(data_to_save, f, ensure_ascii=False, indent=4)
    print(f"-> Đã lưu file: {output_filepath}")

if __name__ == "__main__":
    output_file = "embeddings.json"
    save_embeddings_to_json(sentences, output_file)
```

### Bài tập 2: Tính toán độ tương đồng Cosine (Cosine Similarity) (Mức độ: Khó)
* **Đề bài**: Viết một script Python đọc file `embeddings.json` đã lưu từ Bài tập 1. Nhận một câu truy vấn thô từ người dùng (ví dụ: "Tôi thích ăn bánh mì kẹp"), tiến hành sinh vector embedding cho câu truy vấn đó, và tính toán điểm Cosine Similarity với 5 câu có sẵn trong file JSON để tìm ra câu có nghĩa tương đồng nhất.
* **Yêu cầu**: Học viên tự hoàn thành không có code mẫu.
* **Gợi ý triển khai (Workflow Hints)**:
  1. Sử dụng thư viện `numpy` (hoặc viết hàm thuần Python) để tính Cosine Similarity:
     $$\text{Cosine Similarity} = \frac{A \cdot B}{\|A\| \|B\|}$$
  2. Đọc file `embeddings.json` lên thành danh sách đối tượng chứa text và vector tương ứng.
  3. Duyệt danh sách, tính điểm tương đồng với câu truy vấn và sắp xếp giảm dần để in ra kết quả khớp nhất.

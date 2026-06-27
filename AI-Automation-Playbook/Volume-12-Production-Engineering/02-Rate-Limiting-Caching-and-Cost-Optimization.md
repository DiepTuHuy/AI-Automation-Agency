# Chương 02: Tối ưu chi phí bằng Semantic Caching & Rate Limiting

## 1. Deep Dive (Phân tích chuyên sâu)

### 1. Semantic Caching (Bộ nhớ đệm ngữ nghĩa)
Trong các hệ thống CSKH, khách hàng thường xuyên hỏi các câu gần nghĩa nhau (ví dụ: "Làm sao để đổi trả hàng?" và "Tôi muốn trả lại sản phẩm đã mua").
- **Cache truyền thống**: So khớp chuỗi ký tự chính xác. Hai câu trên khác chữ nên không khớp cache -> Phải gọi LLM sinh chữ mới tốn tiền.
- **Semantic Cache**: Chuyển câu hỏi mới thành vector nhúng. Truy vấn trong cơ sở dữ liệu cache (như Redis). Nếu khoảng cách tương đồng Cosine lớn hơn mức quy định (ví dụ > 0.92), hệ thống lấy trực tiếp câu trả lời đã lưu của câu hỏi trước trả về.
- *Kết quả*: Độ trễ giảm từ 3 giây xuống 0.05 giây; Chi phí API giảm về 0 USD cho lượt truy cập đó.

### 2. Rate Limiting (Giới hạn tần suất gọi)
Để tránh việc người dùng dùng công cụ tự động gửi hàng nghìn request liên tục gây cạn tài khoản API của bạn hoặc làm sập server, bạn cần cài đặt Rate Limiter tại cổng FastAPI Gateway.

---

## 2. Demo: Tự lập trình Semantic Cache thô sơ bằng Python

### Mục tiêu
Xây dựng một Class quản lý Semantic Cache lưu trên bộ nhớ tạm, sử dụng Cosine Similarity để so khớp và trả kết quả tức thì cho câu hỏi gần nghĩa.

### Mã nguồn (`semantic_cache.py`)
```python
import numpy as np
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class SimpleSemanticCache:
    def __init__(self, threshold: float = 0.90):
        self.threshold = threshold
        # Lưu trữ cache dạng danh sách dict: {"question": str, "vector": list, "answer": str}
        self.storage = []

    def _get_vector(self, text: str) -> np.ndarray:
        response = client.embeddings.create(
            input=[text],
            model="text-embedding-3-small"
        )
        return np.array(response.data[0].embedding)

    def get(self, question: str) -> str:
        if not self.storage:
            return None
            
        q_vector = self._get_vector(question)
        
        # Duyệt qua các câu hỏi cũ trong cache để tìm câu tương đồng nhất
        best_score = -1.0
        best_answer = None
        
        for item in self.storage:
            # Tính Cosine Similarity
            dot = np.dot(q_vector, item["vector"])
            norm_q = np.linalg.norm(q_vector)
            norm_cached = np.linalg.norm(item["vector"])
            similarity = dot / (norm_q * norm_cached)
            
            if similarity > best_score:
                best_score = similarity
                best_answer = item["answer"]
                
        print(f"[Cache Check] Độ tương đồng cao nhất tìm thấy: {best_score:.4f}")
        if best_score >= self.threshold:
            return best_answer
        return None

    def set(self, question: str, answer: str):
        q_vector = self._get_vector(question)
        self.storage.append({
            "question": question,
            "vector": q_vector,
            "answer": answer
        })
        print(f"[Cache Store] Đã lưu câu hỏi mới vào cache.")

if __name__ == "__main__":
    cache = SimpleSemanticCache(threshold=0.92)
    
    # Lần chạy 1: Chưa có trong cache -> Gọi AI và lưu cache
    q1 = "Làm thế nào để đăng ký tài khoản mới trên trang web?"
    a1 = "Để đăng ký, bạn bấm vào nút Đăng ký ở góc phải màn hình, điền email và xác nhận mật khẩu."
    cache.set(q1, a1)
    
    # Lần chạy 2: Câu hỏi gần nghĩa -> Trả kết quả trực tiếp từ cache không cần gọi AI
    q2 = "Cách tạo tài khoản mới như thế nào vậy?"
    print(f"\nTruy vấn: '{q2}'")
    cached_answer = cache.get(q2)
    
    if cached_answer:
        print(f"=> KẾT QUẢ TỪ CACHE: {cached_answer}")
    else:
        print("=> Không khớp cache, phải gọi API OpenAI.")
```

---

## 3. Mini Project
Hãy viết một endpoint FastAPI nhận câu hỏi, tích hợp class `SimpleSemanticCache` phía trên vào. Nếu khớp cache thì trả về JSON kết quả kèm thuộc tính `"source": "cache"`; nếu không khớp thì gọi OpenAI, trả về kết quả kèm thuộc tính `"source": "openai_api"`.

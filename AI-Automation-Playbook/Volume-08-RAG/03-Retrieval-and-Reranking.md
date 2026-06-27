# Chương 03: Tối ưu hóa Truy xuất & Kỹ thuật Reranking

## 1. Deep Dive (Phân tích chuyên sâu)

### Vấn đề của Tìm kiếm Vector thuần túy (Vector Similarity Search)
Mô hình nhúng (Embedding Model) được thiết kế để tìm kiếm sự tương đồng tổng thể về mặt ngữ nghĩa (Bi-Encoder). Tuy nhiên, nó đôi khi hoạt động kém hiệu quả đối với các truy vấn đòi hỏi độ chính xác cao về chi tiết nhỏ.
- *Ví dụ*: Người dùng hỏi: "Hỗ trợ thiết bị cho nhân viên thử việc là máy Dell hay Macbook?"
- Kết quả tìm kiếm vector có thể trả về 5 đoạn tài liệu nói chung về "Macbook của công ty" hoặc "Dell của phòng IT" nhưng không chứa đúng câu trả lời cho nhân viên thử việc ở đầu trang.

### Kỹ thuật Reranking (Xếp hạng lại)
Để giải quyết, chúng ta sử dụng quy trình truy xuất 2 bước (Two-stage Retrieval):
1. **Bước 1 (Retrieval)**: Dùng Vector DB tìm kiếm nhanh lấy ra Top 20-30 tài liệu có khả năng liên quan nhất. Bước này diễn ra rất nhanh (độ trễ thấp).
2. **Bước 2 (Reranking)**: Gửi 20 tài liệu này kèm theo câu hỏi gốc qua một mô hình **Reranker** (Cross-Encoder). Reranker thực hiện so sánh đối chiếu chéo từng từ giữa câu hỏi và câu trả lời để tính toán điểm số chính xác ngữ nghĩa sâu sắc. Bước này chậm hơn nhưng do chỉ tính trên 20 tài liệu nên tổng độ trễ vẫn ở mức cho phép. Reranker sẽ đẩy tài liệu thực sự chứa câu trả lời chính xác lên vị trí số 1.

---

## 2. Demo: Tự dựng Reranker cục bộ bằng HuggingFace Cross-Encoder

### Mục tiêu
Sử dụng thư viện HuggingFace chạy offline một mô hình Cross-Encoder nhỏ để chấm điểm lại danh sách tài liệu truy vấn từ database.

### Mã nguồn (`rerank_demo.py`)
Cài đặt thư viện: `pip install sentence-transformers`

```python
from sentence_transformers import CrossEncoder

def run_reranking():
    # 1. Khởi tạo mô hình Cross-Encoder nhỏ của HuggingFace chạy offline cục bộ
    # (Có thể dùng mô hình chuyên dụng cho tiếng Việt hoặc đa ngôn ngữ)
    model = CrossEncoder("mixedbread-ai/mxbai-rerank-xsmall-v1")
    
    query = "Quy định cấp máy tính làm việc Dell hay Macbook cho nhân viên thử việc"
    
    # Giả lập danh sách tài liệu tìm được từ bước truy vấn Vector DB trước đó
    retrieved_documents = [
        "Quy định trang phục: Nhân viên mặc trang phục lịch sự khi đi làm.",
        "IT hỗ trợ cài đặt phần mềm bản quyền trên các máy Dell chạy hệ điều hành Windows.",
        "Hỗ trợ thiết bị làm việc: Công ty cấp máy tính Macbook hoặc Dell cho nhân viên thử việc đạt yêu cầu.",
        "Macbook Pro của sếp được bảo hành tại trung tâm ủy quyền Apple Việt Nam."
    ]
    
    # 2. Xây dựng các cặp (câu hỏi, tài liệu) để đưa vào mô hình chấm điểm chéo
    pairs = [[query, doc] for doc in retrieved_documents]
    
    # 3. Chạy mô hình dự đoán điểm số tương đồng thực tế
    scores = model.predict(pairs)
    
    # 4. Gộp kết quả và sắp xếp lại từ cao xuống thấp
    results = sorted(zip(scores, retrieved_documents), key=lambda x: x[0], reverse=True)
    
    print("=== KẾT QUẢ SAU KHI RERANKING ===")
    for score, doc in results:
        print(f"Điểm số: {score:.4f} | Nội dung: {doc}")

if __name__ == "__main__":
    print("Đang tải mô hình Reranker offline (lần đầu chạy sẽ mất vài phút)...")
    run_reranking()
```

---

## 3. Mini Project
Hãy viết một script Python kết hợp: Truy vấn 5 tài liệu từ ChromaDB (đã dựng ở Volume 7) dựa trên câu hỏi của bạn, sau đó sử dụng Cross-Encoder phía trên để xếp hạng lại 5 tài liệu này và in ra màn hình tài liệu có điểm số rerank cao nhất.

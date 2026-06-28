# Chương 03: Vận hành Cơ sở dữ liệu Vector cục bộ bằng ChromaDB

## 1. Deep Dive (Phân tích chuyên sâu)

### Tại sao cần Cơ sở dữ liệu Vector chuyên dụng?
Nếu bạn có 1,000,000 đoạn văn bản đã nhúng thành vector. Khi người dùng hỏi một câu mới, để tìm đoạn văn tương đồng nhất, bạn phải tính Cosine Similarity 1,000,000 lần. Việc tính toán này chạy tuần tự trên CPU sẽ mất khoảng 2-5 giây - quá chậm cho ứng dụng web.

**Vector Database** (như ChromaDB, Pinecone, Milvus) sử dụng các cấu trúc chỉ mục thuật toán đặc biệt (như Hierarchical Navigable Small World - **HNSW**):
- Nó tổ chức các vector thành một mạng lưới đồ thị liên kết.
- Khi tìm kiếm, nó bỏ qua 99% các vector ở xa và nhanh chóng đi theo các nút đồ thị gần nhất (tìm kiếm K-lân cận xấp xỉ - ANN).
- Tốc độ tìm kiếm giảm xuống chỉ còn vài phần nghìn giây (miliseconds) trên hàng triệu bản ghi.

---

## 2. Demo: Thêm và Truy vấn tài liệu trên ChromaDB

### Mục tiêu
Cài đặt ChromaDB, tạo Collection, nạp tài liệu và thực hiện tìm kiếm ngữ nghĩa cục bộ không cần kết nối cloud.

### Mã nguồn (`chroma_demo.py`)
Cài đặt thư viện: `pip install chromadb`

```python
import chromadb

def run_chroma_database():
    # 1. Khởi tạo client lưu file database cục bộ trong thư mục 'chroma_db_store'
    client = chromadb.PersistentClient(path="./chroma_db_store")
    
    # 2. Tạo hoặc gọi Collection (Tương đương với Bảng trong SQL)
    # Mặc định ChromaDB sẽ tự động tải mô hình nhúng mặc định của nó chạy offline cục bộ nếu bạn không khai báo mô hình ngoài
    collection = client.get_or_create_collection("company_policies")
    
    # 3. Thêm tài liệu thô (ChromaDB sẽ tự nhúng thành vector và lưu)
    collection.add(
        documents=[
            "Chính sách nghỉ phép của công ty: Mỗi nhân viên được nghỉ 12 ngày phép năm hưởng lương đầy đủ.",
            "Quy định trang phục: Nhân viên mặc trang phục lịch sự, chỉnh tề khi đi làm từ thứ Hai đến thứ Năm.",
            "Hỗ trợ thiết bị làm việc: Công ty cấp máy tính Macbook hoặc Dell cho nhân viên thử việc đạt yêu cầu."
        ],
        metadatas=[
            {"category": "HR", "importance": "high"},
            {"category": "Operation", "importance": "medium"},
            {"category": "IT", "importance": "high"}
        ],
        ids=["doc_hr_01", "doc_op_01", "doc_it_01"]
    )
    print("Đã nạp tài liệu vào ChromaDB thành công!")

    # 4. Truy vấn tìm kiếm ngữ nghĩa
    query_text = "Tôi muốn biết quy định đi làm mặc đồ thế nào?"
    print(f"\nTruy vấn: '{query_text}'")
    
    results = collection.query(
        query_texts=[query_text],
        n_results=1 # Lấy 1 kết quả tốt nhất
    )
    
    # 5. In kết quả tìm kiếm
    print("Kết quả tương đồng nhất tìm được:")
    print(f"- Nội dung: {results['documents'][0][0]}")
    print(f"- ID tài liệu: {results['ids'][0][0]}")
    print(f"- Metadata: {results['metadatas'][0][0]}")
    print(f"- Khoảng cách tương đồng (nhỏ hơn là gần hơn): {results['distances'][0][0]:.4f}")

if __name__ == "__main__":
    run_chroma_database()
```

---

## 3. Mini Project

### Bài tập 1: Tích hợp Vector nhúng của Gemini vào ChromaDB (Mức độ: Trung bình)
* **Đề bài**: Viết một script Python tự tính toán vector nhúng bằng mô hình `models/text-embedding-004` thông qua hàm `genai.embed_content` rồi lưu trực tiếp các vector này kèm văn bản và metadata vào ChromaDB cục bộ. Sau đó thực hiện câu lệnh truy vấn tìm kiếm tương đồng.
* **Mã nguồn mẫu (`chroma_gemini_integration.py`)**:
```python
import os
import chromadb
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

def get_gemini_embeddings(texts: list) -> list:
    embeddings = []
    for text in texts:
        res = genai.embed_content(
            model="models/text-embedding-004",
            contents=[text],
            task_type="retrieval_document"
        )
        embeddings.append(res['embedding'][0])
    return embeddings

if __name__ == "__main__":
    # 1. Khởi tạo ChromaDB cục bộ
    chroma_client = chromadb.PersistentClient(path="./chroma_gemini_store")
    collection = chroma_client.get_or_create_collection("policy_database")
    
    # 2. Dữ liệu văn bản mẫu
    documents_list = [
        "Chính sách nghỉ phép của công ty: Mỗi nhân viên được nghỉ 12 ngày phép năm hưởng lương đầy đủ.",
        "Quy định trang phục: Nhân viên mặc trang phục lịch sự, chỉnh tề khi đi làm từ thứ Hai đến thứ Năm.",
        "Hỗ trợ thiết bị làm việc: Công ty cấp máy tính Macbook hoặc Dell cho nhân viên thử việc đạt yêu cầu."
    ]
    metadatas_list = [
        {"category": "HR", "importance": "high"},
        {"category": "Operation", "importance": "medium"},
        {"category": "IT", "importance": "high"}
    ]
    ids_list = ["doc_hr_01", "doc_op_01", "doc_it_01"]
    
    # 3. Tính toán vector bằng Gemini
    print("Đang tính toán vector nhúng bằng Gemini...")
    vectors = get_gemini_embeddings(documents_list)
    
    # 4. Lưu vào ChromaDB (Truyền thủ công danh sách embeddings)
    collection.add(
        embeddings=vectors,
        documents=documents_list,
        metadatas=metadatas_list,
        ids=ids_list
    )
    print("Nạp dữ liệu vector vào database thành công!")
    
    # 5. Truy vấn dữ liệu
    query_text = "Quy định mặc quần áo đi làm"
    query_vector = get_gemini_embeddings([query_text])[0]
    
    results = collection.query(
        query_embeddings=[query_vector],
        n_results=1
    )
    print(f"\nKết quả truy vấn tốt nhất cho câu hỏi '{query_text}':")
    print(f"- Nội dung: {results['documents'][0][0]}")
    print(f"- Khoảng cách: {results['distances'][0][0]:.4f}")
```

### Bài tập 2: Bộ tìm kiếm nội quy nhân sự tích hợp bộ lọc Metadata (Mức độ: Khó)
* **Đề bài**: Nâng cấp script ở Bài tập 1 để hỗ trợ bộ lọc metadata khi truy vấn. Khi người dùng nhập một câu hỏi về "máy tính", hãy cấu hình truy vấn ChromaDB để chỉ tìm kiếm trong danh sách các tài liệu thuộc nhóm Công nghệ thông tin (`category` là `IT`).
* **Yêu cầu**: Học viên tự hoàn thành không có code mẫu.
* **Gợi ý triển khai (Workflow Hints)**:
  1. Sử dụng tham số `where` trong câu lệnh `collection.query`.
  2. Cấu hình điều kiện lọc dạng: `where={"category": "IT"}`.
  3. Kiểm tra xem kết quả trả về có chính xác nằm trong nhóm IT hay bị trôi sang các nhóm khác.
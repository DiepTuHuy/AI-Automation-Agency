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
Hãy sửa đổi file demo trên để sử dụng mô hình nhúng của OpenAI (`text-embedding-3-small`) khi nạp và truy vấn dữ liệu trong ChromaDB (Tham khảo hướng dẫn tích hợp OpenAI trong tài liệu của ChromaDB).

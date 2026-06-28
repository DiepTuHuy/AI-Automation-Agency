# Chương 04: Kỹ thuật lọc Metadata và Truy vấn Lai (Hybrid Query)

## 1. Deep Dive (Phân tích chuyên sâu)

### Bài toán lọc siêu dữ liệu (Metadata Filtering)
Trong thực tế, bạn không bao giờ muốn tìm kiếm ngữ nghĩa trên toàn bộ kho dữ liệu hỗn loạn.
- *Ví dụ*: Người dùng hỏi về "Chính sách bảo hiểm của phòng kỹ thuật năm 2026". 
- Nếu chỉ tìm kiếm vector thuần túy, thuật toán có thể trả về tài liệu bảo hiểm của phòng kinh doanh hoặc tài liệu của năm 2025 vì chúng có các vector ý nghĩa rất tương đồng.
- Để giải quyết, bạn cần **Lọc Metadata**: Giới hạn phạm vi tìm kiếm chỉ trong các tài liệu có thuộc tính `department = "engineering"` và `year = 2026` trước khi tính toán tương đồng vector. Điều này giúp tăng độ chính xác lên tuyệt đối và tiết kiệm tài nguyên tính toán.

---

## 2. Demo: Truy vấn lọc Metadata nâng cao trong ChromaDB

### Mục tiêu
Thực hiện truy vấn tìm kiếm vector trong ChromaDB kết hợp các toán tử điều kiện lọc phức tạp trên metadata của tài liệu.

### Mã nguồn (`metadata_filter.py`)
```python
import chromadb

def run_advanced_query():
    client = chromadb.PersistentClient(path="./chroma_db_store")
    collection = client.get_or_create_collection("company_policies")
    
    # Thực hiện truy vấn tìm kiếm ngữ nghĩa kèm bộ lọc metadata
    query_question = "Quy định về máy tính làm việc"
    
    print(f"Đang tìm kiếm câu: '{query_question}' với bộ lọc category = 'IT'...")
    
    results = collection.query(
        query_texts=[query_question],
        n_results=2,
        # Cấu hình bộ lọc metadata sử dụng cú pháp JSON
        where={
            "category": "IT"
        }
    )
    
    # In kết quả
    for i in range(len(results['ids'][0])):
        print(f"\nKết quả #{i+1}:")
        print(f"- Nội dung: {results['documents'][0][i]}")
        print(f"- Metadata: {results['metadatas'][0][i]}")

if __name__ == "__main__":
    run_advanced_query()
```

---

## 3. Mini Project

### Bài tập 1: Đánh chỉ mục và Truy vấn thông tin sản phẩm trong ChromaDB (Mức độ: Trung bình)
* **Đề bài**: Viết một script Python sử dụng ChromaDB để tạo một collection, thêm 3 tài liệu mô tả sản phẩm kèm theo ID và truy vấn tìm kiếm sản phẩm liên quan đến từ khóa "không dây".
* **Mã nguồn mẫu (`chroma_search.py`)**:
```python
import chromadb

def run_db_search():
    # Khởi tạo ChromaDB client trong bộ nhớ phục vụ test
    client = chromadb.EphemeralClient()
    collection = client.create_collection(name="products_store")
    
    # Thêm tài liệu (ChromaDB sẽ tự động sử dụng mô hình nhúng mặc định nếu không khai báo)
    collection.add(
        documents=[
            "Chuột máy tính không dây Logitech bền bỉ.",
            "Bàn phím cơ có dây Keychron lực nhấn tốt.",
            "Tai nghe chụp tai Bluetooth khử tiếng ồn chủ động."
        ],
        ids=["p1", "p2", "p3"]
    )
    
    # Truy vấn
    results = collection.query(
        query_texts=["thiết bị không dây"],
        n_results=1
    )
    print("Kết quả tìm kiếm phù hợp nhất:")
    print(f"- ID: {results['ids'][0][0]}")
    print(f"- Văn bản: {results['documents'][0][0]}")

if __name__ == "__main__":
    run_db_search()
```

### Bài tập 2: Quản lý vòng đời bộ sưu tập dữ liệu chỉ mục (Mức độ: Khó)
* **Đề bài**: Viết một script Python thực thi đầy đủ vòng đời (CRUD) của dữ liệu trong Vector DB: Tạo collection, nạp dữ liệu, thực hiện cập nhật nội dung của một tài liệu đã có qua ID, thực hiện xóa một tài liệu và kiểm thử lại kết quả truy vấn sau khi xóa.
* **Yêu cầu**: Học viên tự hoàn thành không có code mẫu.
* **Gợi ý triển khai (Workflow Hints)**:
  1. Sử dụng hàm `collection.update(ids=["..."], documents=["Nội dung mới"])` để cập nhật dữ liệu.
  2. Sử dụng `collection.delete(ids=["..."])` để xóa bản ghi.
  3. Thực hiện câu lệnh query để đảm bảo tài liệu đã xóa không còn xuất hiện trong kết quả trả về.

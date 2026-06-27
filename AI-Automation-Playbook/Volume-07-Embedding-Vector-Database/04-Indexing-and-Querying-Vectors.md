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
Hãy viết một script Python nạp 10 tin tức công nghệ vào ChromaDB, mỗi tin có metadata lưu trữ: `author` (tên tác giả), và `view_count` (số lượt xem). Hãy viết câu lệnh truy vấn tìm tin tức ngữ nghĩa tương tự với chủ đề "AI di động" nhưng bắt buộc chỉ lấy các tin của tác giả "Admin" và có số lượt xem lớn hơn 1000 lượt (Tìm hiểu cú pháp lọc toán tử so sánh `$gt` của ChromaDB).

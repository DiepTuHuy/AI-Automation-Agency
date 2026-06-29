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
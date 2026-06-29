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
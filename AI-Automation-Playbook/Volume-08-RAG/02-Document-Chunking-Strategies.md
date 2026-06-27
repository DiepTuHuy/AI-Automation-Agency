# Chương 02: Kỹ thuật phân tách văn bản (Document Chunking)

## 1. Deep Dive (Phân tích chuyên sâu)

### Tại sao không thể nhét nguyên cuốn sách vào Prompt?
Dù context window của LLM ngày càng lớn, việc nhét nguyên một tài liệu dài hàng nghìn trang vào prompt vẫn mang lại hiệu năng kém:
1. **Lãng phí chi phí**: Chi phí API tính tiền trên mỗi token. Nhồi tài liệu dài cho mỗi câu hỏi ngắn sẽ làm chi phí tăng lũy tiến.
2. **Lost in the Middle**: LLM sẽ bắt đầu bỏ sót thông tin nằm giữa tài liệu.

Do đó, ta phải chia nhỏ tài liệu thành các **Chunks**.

### Các chiến lược Chunking phổ biến
1. **Character Chunking**: Cắt văn bản theo số lượng ký tự cố định.
   - *Hạn chế*: Có thể cắt trúng giữa một từ hoặc câu, làm mất nghĩa của từ đó.
2. **Recursive Character Chunking**: Cắt đệ quy dựa trên danh sách các ký tự phân tách (ngắt dòng kép, ngắt dòng đơn, dấu cách). Giúp cố gắng giữ các câu và đoạn văn trọn vẹn nhất có thể.
3. **Semantic Chunking**: Sử dụng mô hình nhúng để tính toán sự thay đổi ngữ nghĩa giữa các câu liên tiếp, tự động cắt chunk khi ý nghĩa câu chuyển sang chủ đề khác.

---

## 2. Demo: So sánh các bộ chia cắt bằng LangChain

### Mục tiêu
Sử dụng thư viện LangChain trong Python để thực hiện chia cắt một đoạn văn bản mẫu bằng 2 thuật toán khác nhau, phân tích sự khác biệt về kết quả đầu ra.

### Mã nguồn (`chunking_test.py`)
Cài đặt thư viện: `pip install langchain-text-splitters`

```python
from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter

raw_text = """
Học phần 1: Thiết lập môi trường làm việc. Đây là bước đầu tiên để trở thành kỹ sư thực chiến. Bạn cần cài đặt Python, Git và VS Code.
Học phần 2: Lập trình FastAPI. Framework này rất nhanh và tự động sinh tài liệu Swagger UI. Bạn sẽ viết các endpoint GET/POST để kết nối frontend.
Học phần 3: Sử dụng n8n tự động hóa. Công cụ kéo thả này giúp bạn kết nối Google Sheets, Telegram dễ dàng mà không cần code nhiều.
"""

def test_splitters():
    # 1. Thử nghiệm CharacterTextSplitter (Cắt cứng theo ký tự ngắt câu)
    char_splitter = CharacterTextSplitter(
        separator=".",
        chunk_size=100,
        chunk_overlap=10
    )
    char_chunks = char_splitter.split_text(raw_text)
    
    # 2. Thử nghiệm RecursiveCharacterTextSplitter (Đệ quy thông minh)
    recursive_splitter = RecursiveCharacterTextSplitter(
        chunk_size=120,
        chunk_overlap=20
    )
    rec_chunks = recursive_splitter.split_text(raw_text)
    
    print(f"=== KẾT QUẢ CHARACTER SPLITTER (Số lượng: {len(char_chunks)}) ===")
    for i, chunk in enumerate(char_chunks):
        print(f"Chunk {i+1} (Dài {len(chunk)}): {chunk.strip()}")
        
    print("\n" + "="*40 + "\n")
    
    print(f"=== KẾT QUẢ RECURSIVE CHARACTER SPLITTER (Số lượng: {len(rec_chunks)}) ===")
    for i, chunk in enumerate(rec_chunks):
        print(f"Chunk {i+1} (Dài {len(chunk)}): {chunk.strip()}")

if __name__ == "__main__":
    test_splitters()
```

---

## 3. Mini Project
Hãy viết một script Python đọc một file nội dung điều khoản sử dụng dài, áp dụng `RecursiveCharacterTextSplitter` với chunk size = 800 và overlap = 150. Ghi kết quả các chunk tìm được ra một thư mục `chunks/` dưới dạng các file nhỏ `chunk_1.txt`, `chunk_2.txt`... để kiểm tra trực quan sản phẩm.

# Chương 04: Tiếp nhận & Xử lý Tệp tin tải lên (File Uploads)

## 1. Deep Dive (Phân tích chuyên sâu)

### upload file trong Production: `bytes` vs `UploadFile`
FastAPI cung cấp hai cách chính để nhận file từ Client:
1. **`bytes`**: FastAPI đọc toàn bộ file vào bộ nhớ RAM của server dưới dạng mảng byte.
   - *Hạn chế*: Nếu người dùng upload một file dung lượng 2GB, server của bạn sẽ lập tức tốn 2GB RAM. Nhiều file tải lên đồng thời sẽ gây cạn kiệt tài nguyên RAM và làm sập toàn bộ hệ thống (Out of Memory).
2. **`UploadFile`**: FastAPI sử dụng tệp tin tạm (SpooledTemporaryFile) lưu trữ trên ổ đĩa cứng của server khi file vượt quá giới hạn RAM cho phép (thường là 1MB).
   - *Ưu điểm*: Tiết kiệm RAM, hỗ trợ đọc file dạng stream, dễ dàng lấy metadata của file (tên file, content-type).

---

## 2. Demo: API tải lên tài liệu PDF để phân tích

### Mục tiêu
Xây dựng endpoint nhận một file PDF tải lên từ client, kiểm tra định dạng file có phải là PDF hay không, và lưu file đó vào thư mục lưu trữ cục bộ trên server.

### Mã nguồn (`upload_server.py`)
```python
import shutil
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, HTTPException

app = FastAPI()
UPLOAD_DIR = Path("./uploaded_documents")
UPLOAD_DIR.mkdir(exist_ok=True)

@app.post("/api/v1/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    # 1. Kiểm tra định dạng file bằng Content-Type
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400, 
            detail="Định dạng file không hợp lệ! Hệ thống chỉ chấp nhận file PDF."
        )
        
    # 2. Định nghĩa đường dẫn lưu file cứng trên server
    save_path = UPLOAD_DIR / file.filename
    
    try:
        # 3. Ghi file từ bộ nhớ tạm ra đĩa cứng một cách tối ưu
        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi khi lưu file: {str(e)}")
    finally:
        # Luôn giải phóng file tạm của FastAPI
        await file.close()
        
    return {
        "filename": file.filename,
        "saved_path": str(save_path),
        "size_bytes": save_path.stat().st_size,
        "status": "uploaded_successfully"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("upload_server:app", host="127.0.0.1", port=8000, reload=True)
```

---

## 3. Mini Project
Hãy kết hợp module này với API OpenAI ở Volume 01. Viết một endpoint nhận file văn bản `.txt` tải lên, đọc nội dung văn bản đó, gửi sang OpenAI nhờ tóm tắt ngắn gọn và trả kết quả tóm tắt trực tiếp về cho client.

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

### Bài tập 1: Xây dựng API tải lên hình ảnh đại diện (Mức độ: Trung bình)
* **Đề bài**: Viết một API FastAPI cho phép người dùng tải lên một tệp tin hình ảnh đại diện (avatar). Kiểm tra xem tệp tải lên có định dạng ảnh hợp lệ không (`.png`, `.jpg`, `.jpeg`) và lưu tệp vào thư mục `static/uploads/`.
* **Mã nguồn mẫu (`avatar_uploader.py`)**:
```python
import os
from fastapi import FastAPI, File, UploadFile, HTTPException
from pathlib import Path

app = FastAPI()
UPLOAD_DIR = Path("static/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@app.post("/upload/avatar")
async def upload_avatar(file: UploadFile = File(...)):
    suffix = Path(file.filename).suffix.lower()
    if suffix not in [".png", ".jpg", ".jpeg"]:
        raise HTTPException(status_code=400, detail="Chỉ chấp nhận file ảnh định dạng PNG hoặc JPG.")
        
    file_path = UPLOAD_DIR / file.filename
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
        
    return {
        "filename": file.filename,
        "saved_path": str(file_path),
        "size_bytes": len(content)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
```

### Bài tập 2: API phân tích cấu trúc file CSV được tải lên (Mức độ: Khó)
* **Đề bài**: Xây dựng API tiếp nhận tải lên một file CSV chứa bảng lương nhân viên. Script xử lý bất đồng bộ file CSV vừa tải lên, sử dụng thư viện `pandas` để tính tổng lương thực lĩnh của toàn bộ nhân viên và trả về kết quả phân tích thống kê dạng JSON.
* **Yêu cầu**: Bạn hãy tự hoàn thành không có code mẫu.
* **Gợi ý triển khai (Workflow Hints)**:
  1. Đọc nội dung file CSV trực tiếp bằng `io.StringIO` từ tệp UploadFile mà không cần lưu xuống đĩa.
  2. Sử dụng `pd.read_csv()` để nạp dữ liệu vào DataFrame.
  3. Tính tổng cột lương và trả kết quả tổng quan về cho khách hàng.

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
import os
import logging
from pathlib import Path
from typing import List
from fastapi import FastAPI, HTTPException, Query, status
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Playbook Content Service", version="1.0.0")

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Content_Service")

PLAYBOOK_DIR = Path(os.getenv("PLAYBOOK_DIR", "../AI-Automation-Playbook")).resolve()
if not PLAYBOOK_DIR.exists():
    PLAYBOOK_DIR = Path("/Users/dieptuhuy/Documents/AI Automation/AI-Automation-Playbook").resolve()

logger.info(f"Content Service initialized with Playbook Base: {PLAYBOOK_DIR}")

def validate_safe_path(requested_path_str: str) -> Path:
    requested_path = Path(requested_path_str).resolve()
    if not requested_path.is_relative_to(PLAYBOOK_DIR):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Truy cập bị từ chối: Đường dẫn không an toàn!"
        )
    if not requested_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tệp tin không tồn tại!"
        )
    return requested_path

@app.get("/api/volumes")
async def list_volumes():
    if not PLAYBOOK_DIR.exists():
        raise HTTPException(status_code=500, detail="Không tìm thấy thư mục Playbook!")
        
    volumes = []
    for item in sorted(PLAYBOOK_DIR.iterdir()):
        if item.is_dir() and (item.name.startswith("Volume-") or item.name == "Projects"):
            md_files = []
            if item.name == "Projects":
                for sub_item in sorted(item.iterdir()):
                    if sub_item.is_dir():
                        readme = sub_item / "README.md"
                        if readme.exists():
                            md_files.append(f"{sub_item.name}/README.md")
                    elif sub_item.name == "README.md":
                        md_files.append("README.md")
            else:
                for sub_file in sorted(item.iterdir()):
                    if sub_file.is_file() and sub_file.suffix == ".md":
                        md_files.append(sub_file.name)
                        
            volumes.append({
                "name": item.name,
                "path": str(item),
                "files": md_files
            })
    return volumes

@app.get("/api/content")
async def read_file_content(path: str = Query(..., description="Absolute path of the markdown file")):
    safe_path = validate_safe_path(path)
    try:
        content = safe_path.read_text(encoding="utf-8")
        return {"filename": safe_path.name, "content": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi đọc file: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)

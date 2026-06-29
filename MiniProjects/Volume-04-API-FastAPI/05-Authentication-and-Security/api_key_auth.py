from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader

app = FastAPI()

API_KEY = "super_secret_key_123"
API_KEY_NAME = "X-API-KEY"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

def validate_api_key(key: str = Depends(api_key_header)):
    if key != API_KEY:
        raise HTTPException(
            status_code=403,
            detail="Quyền truy cập bị từ chối. API Key không hợp lệ."
        )
    return key

@app.get("/api/v1/revenue")
def get_revenue(api_key: str = Depends(validate_api_key)):
    # Chỉ những request có đúng header X-API-KEY mới vào được đây
    return {
        "month": "July 2026",
        "revenue_usd": 150000.0,
        "status": "Success"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
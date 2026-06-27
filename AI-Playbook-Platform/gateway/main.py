import os
from pathlib import Path
import httpx
from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI(title="AI Playbook API Gateway", version="1.0.0")

CONTENT_SERVICE_URL = os.getenv("CONTENT_SERVICE_URL", "http://127.0.0.1:8001")
QUIZ_SERVICE_URL = os.getenv("QUIZ_SERVICE_URL", "http://127.0.0.1:8002")

# Create AsyncClient for connection reuse
client = httpx.AsyncClient()

@app.on_event("shutdown")
async def shutdown_event():
    await client.aclose()

# --- PROXY ENDPOINTS ---

@app.get("/api/volumes")
async def proxy_volumes():
    try:
        res = await client.get(f"{CONTENT_SERVICE_URL}/api/volumes")
        return Response(content=res.content, status_code=res.status_code, media_type=res.headers.get("content-type"))
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Content Service unavailable: {str(e)}")

@app.get("/api/content")
async def proxy_content(path: str):
    try:
        res = await client.get(f"{CONTENT_SERVICE_URL}/api/content", params={"path": path})
        return Response(content=res.content, status_code=res.status_code, media_type=res.headers.get("content-type"))
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Content Service unavailable: {str(str(e))}")

@app.get("/api/config")
async def proxy_get_config():
    try:
        res = await client.get(f"{QUIZ_SERVICE_URL}/api/config")
        return Response(content=res.content, status_code=res.status_code, media_type=res.headers.get("content-type"))
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Quiz Service unavailable: {str(e)}")

@app.post("/api/config")
async def proxy_post_config(request: Request):
    try:
        body = await request.body()
        res = await client.post(f"{QUIZ_SERVICE_URL}/api/config", content=body, headers={"Content-Type": "application/json"})
        return Response(content=res.content, status_code=res.status_code, media_type=res.headers.get("content-type"))
    except Exception as e:
        raise HTTPException(status_code=533, detail=f"Quiz Service unavailable: {str(e)}")

@app.get("/api/quiz")
async def proxy_quiz(path: str, difficulty: str = "medium", limit: int = 5):
    try:
        res = await client.get(
            f"{QUIZ_SERVICE_URL}/api/quiz", 
            params={"path": path, "difficulty": difficulty, "limit": limit}, 
            timeout=90.0
        )
        return Response(content=res.content, status_code=res.status_code, media_type=res.headers.get("content-type"))
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Quiz Service unavailable: {str(e)}")

# --- STATIC ASSETS ---

# Serves static frontend files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def serve_home():
    html_path = Path("static/index.html")
    if html_path.exists():
        return FileResponse(html_path)
    raise HTTPException(status_code=404, detail="Static index.html not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

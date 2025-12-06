from fastapi import FastAPI, Query
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from downloader import fetch_douyin_video, normalize_url

app = FastAPI(title="Douyin Downloader Pro", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"status": "running", "message": "Douyin API Ready"}

@app.get("/api/info")
async def info(url: str = Query(..., description="Douyin URL")):
    real_url = normalize_url(url)
    data = await fetch_douyin_video(real_url)

    if "error" in data:
        return JSONResponse({"success": False, "error": data["error"]}, status_code=400)

    return {"success": True, "data": data}

# LOGIC BARU: Endpoint download menerima parameter 'quality'
@app.get("/api/download")
async def download(url: str, quality: str = "sd"):
    real_url = normalize_url(url)
    data = await fetch_douyin_video(real_url)

    if "error" in data:
        return JSONResponse({"success": False, "error": data["error"]}, status_code=400)

    # Cek user minta apa
    if quality == "hd":
        return RedirectResponse(data["video_hd"]) # Redirect ke RAW
    else:
        return RedirectResponse(data["video_sd"]) # Redirect ke Biasa
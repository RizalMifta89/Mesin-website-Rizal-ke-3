import httpx

def normalize_url(url: str) -> str:
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
        }
        with httpx.Client(follow_redirects=True, timeout=10, headers=headers) as client:
            response = client.get(url)
            return str(response.url)
    except Exception:
        return url

async def fetch_douyin_video(url: str) -> dict:
    # API Douyin
    api_endpoint = "https://api.douyin.wtf/api" 

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.get(api_endpoint, params={"url": url})
            data = r.json()

        if data.get("status") != "success":
            raise Exception("Gagal mengambil data. Pastikan link Douyin benar.")

        result = data

        # LOGIC BARU: Ambil KEDUA link (SD dan HD)
        video_sd = result.get("nwm_video_url")       # Kualitas Biasa
        video_hd = result.get("nwm_video_url_HQ")    # Kualitas RAW
        
        # Jika HD tidak tersedia, pakai SD sebagai cadangan
        if not video_hd:
            video_hd = video_sd

        return {
            "title": result.get("desc", "Douyin Video"),
            "author": result.get("author", {}).get("nickname", "User"),
            "cover": result.get("cover_url", ""),
            "video_sd": video_sd, # Link Biasa
            "video_hd": video_hd  # Link RAW
        }

    except Exception as e:
        return {"error": str(e)}
import httpx
import re

def normalize_url(text: str) -> str:
    """
    Fungsi Pintar:
    Menerima teks panjang (campur emoji/mandarin),
    Mencari link 'http...' di dalamnya,
    Lalu mengubah shortlink (v.douyin) menjadi link asli.
    """
    try:
        # 1. CARI LINK DALAM TEKS (Regex)
        # Mencari pattern https://... di antara teks sampah
        url_match = re.search(r'https?://(?:www\.|v\.)?douyin\.com/[a-zA-Z0-9/]+', text)
        
        if url_match:
            url = url_match.group(0) # Ambil link-nya saja
        else:
            url = text # Kalau tidak ketemu, coba pakai text aslinya

        # 2. UBAH SHORTLINK JADI REAL LINK
        # Header user-agent penting supaya tidak dianggap bot
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
        }
        
        with httpx.Client(follow_redirects=True, timeout=10, headers=headers) as client:
            response = client.get(url)
            return str(response.url)
            
    except Exception:
        # Jika gagal, kembalikan apa adanya (biar ditangani fetcher)
        return text

async def fetch_douyin_video(url: str) -> dict:
    # Gunakan TikWM (Support Douyin & TikTok)
    api_endpoint = "https://www.tikwm.com/api/"

    try:
        async with httpx.AsyncClient(timeout=20) as client:
            # Kirim data
            r = await client.post(api_endpoint, data={"url": url})
            
            try:
                data = r.json()
            except Exception:
                raise Exception("API sibuk. Coba lagi nanti.")

        if data.get("code") != 0:
            raise Exception("Video tidak ditemukan atau Link Privat/Dihapus.")

        result = data["data"]

        # LOGIC KUALITAS (HD Priority)
        video_sd = result.get("play")
        video_hd = result.get("hdplay")
        
        if not video_hd:
            video_hd = video_sd
        
        if not video_sd:
            video_sd = result.get("wmplay")

        return {
            "title": result.get("title", "Douyin Video"),
            "author": result.get("author", {}).get("unique_id", "User"),
            "cover": result.get("cover", ""),
            "video_sd": video_sd, 
            "video_hd": video_hd 
        }

    except Exception as e:
        print(f"ERROR: {str(e)}") 
        return {"error": str(e)}
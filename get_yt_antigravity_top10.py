import subprocess
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

def search_yt_videos():
    query = "ytsearch30:Google Antigravity 2 tutorial"
    print(f"Searching YouTube with yt-dlp query: '{query}'...")
    
    cmd = [
        "yt-dlp",
        query,
        "--dump-single-json",
        "--flat-playlist",
        "--ignore-errors"
    ]
    
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        if res.returncode != 0:
            print("yt-dlp warning/error:", res.stderr[:500])
        
        data = json.loads(res.stdout)
        entries = data.get("entries", [])
        print(f"Retrieved {len(entries)} candidate videos.")
        
        video_list = []
        for entry in entries:
            if not entry:
                continue
            v_id = entry.get("id")
            title = entry.get("title")
            url = entry.get("url") or f"https://www.youtube.com/watch?v={v_id}"
            view_count = entry.get("view_count") or 0
            uploader = entry.get("uploader") or entry.get("channel") or "Unknown"
            duration = entry.get("duration") or 0
            description = entry.get("description") or ""

            video_list.append({
                "id": v_id,
                "title": title,
                "url": url,
                "view_count": view_count,
                "uploader": uploader,
                "duration": duration,
                "description": description[:200]
            })

        # 按 view_count 严格倒序排序
        video_list.sort(key=lambda x: x["view_count"], reverse=True)

        top10 = video_list[:10]
        with open("yt_top10_antigravity.json", "w", encoding="utf-8") as f:
            json.dump(top10, f, ensure_ascii=False, indent=2)

        print(f"Top 10 videos written to yt_top10_antigravity.json")
        for idx, item in enumerate(top10, 1):
            print(f"{idx}. [{item['view_count']:,} views] {item['title']} - {item['url']}")

    except Exception as e:
        print(f"Error executing search: {e}")

if __name__ == "__main__":
    search_yt_videos()

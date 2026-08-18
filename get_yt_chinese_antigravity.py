import subprocess
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

def search_yt_chinese():
    queries = [
        "ytsearch20:Google Antigravity 2 教程",
        "ytsearch20:Google Antigravity 中文教程",
        "ytsearch20:Antigravity 2 使用指南"
    ]
    
    video_map = {}
    
    for q in queries:
        print(f"Searching: {q}...")
        cmd = ["yt-dlp", q, "--dump-single-json", "--flat-playlist", "--ignore-errors"]
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
            if res.returncode == 0 and res.stdout.strip():
                data = json.loads(res.stdout)
                entries = data.get("entries", [])
                for entry in entries:
                    if not entry:
                        continue
                    v_id = entry.get("id")
                    title = entry.get("title", "")
                    uploader = entry.get("uploader") or entry.get("channel") or "未知频道"
                    view_count = entry.get("view_count") or 0
                    url = entry.get("url") or f"https://www.youtube.com/watch?v={v_id}"
                    duration = entry.get("duration") or 0
                    desc = entry.get("description") or ""

                    # 只要包含中文文字或中文关键词的视频
                    video_map[v_id] = {
                        "id": v_id,
                        "title": title,
                        "url": url,
                        "view_count": view_count,
                        "uploader": uploader,
                        "duration": duration,
                        "description": desc[:200]
                    }
        except Exception as e:
            print(f"Error on query {q}: {e}")

    all_videos = list(video_map.values())
    all_videos.sort(key=lambda x: x["view_count"], reverse=True)
    top10 = all_videos[:10]

    with open("yt_top10_chinese.json", "w", encoding="utf-8") as f:
        json.dump(top10, f, ensure_ascii=False, indent=2)

    print(f"Total unique Chinese/relevant videos fetched: {len(all_videos)}")
    print(f"Top 10 written to yt_top10_chinese.json")

if __name__ == "__main__":
    search_yt_chinese()

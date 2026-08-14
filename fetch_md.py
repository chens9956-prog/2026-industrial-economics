from youtube_transcript_api import YouTubeTranscriptApi
import math

video_id = "3s2Q1nViZ1w"

def format_time(seconds):
    mins = math.floor(seconds / 60)
    secs = int(seconds % 60)
    return f"{mins:02d}:{secs:02d}"

try:
    transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
    transcript = transcript_list.find_transcript(['zh-TW', 'zh-HK', 'zh-CN', 'zh', 'zh-Hans', 'zh-Hant', 'en'])
    data = transcript.fetch()
    
    md_content = f"# YouTube Video Transcript ({video_id})\n\n"
    
    for item in data:
        start_time = item.get('start', 0)
        text = item.get('text', '').replace('\n', ' ')
        time_str = format_time(start_time)
        md_content += f"- **[{time_str}]** {text}\n"

    with open("3s2Q1nViZ1w_transcript.md", "w", encoding="utf-8") as f:
        f.write(md_content)
    
    print("SUCCESS: 3s2Q1nViZ1w_transcript.md generated.")
except Exception as e:
    print(f"Error: {e}")

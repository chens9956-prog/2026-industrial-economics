from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import WebVTTFormatter

video_id = "3s2Q1nViZ1w"

try:
    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['zh-TW', 'zh-HK', 'zh-CN', 'zh', 'zh-Hans', 'zh-Hant', 'en'])
    formatter = WebVTTFormatter()
    vtt_formatted = formatter.format_transcript(transcript)
    
    with open("transcript.vtt", "w", encoding="utf-8") as f:
        f.write(vtt_formatted)
        
    md_formatted = "# 字幕档 (Video ID: " + video_id + ")\n\n"
    for item in transcript:
        md_formatted += f"[{item['start']:.2f}s] {item['text']}\n\n"
        
    with open("transcript.md", "w", encoding="utf-8") as f:
        f.write(md_formatted)
        
    print("SUCCESS")
except Exception as e:
    print(f"Error: {e}")

import json
import math

def format_time(seconds):
    mins = math.floor(seconds / 60)
    secs = int(seconds % 60)
    return f"{mins:02d}:{secs:02d}"

try:
    with open("transcript.json", "r", encoding="utf-16") as f:
        data = json.load(f)

    md_content = "# YouTube Video Transcript (3s2Q1nViZ1w)\n\n"
    
    # If it's a list, it's just the transcript items.
    # If it's a dict, maybe it has video id as key. Let's handle both.
    items = []
    if isinstance(data, list):
        items = data
    elif isinstance(data, dict):
        # usually CLI outputs a dict if multiple videos are requested, wait no, standard output for one video is a list
        if "3s2Q1nViZ1w" in data:
            items = data["3s2Q1nViZ1w"]
        else:
            items = list(data.values())[0] if data else []

    for item in items:
        start_time = item.get('start', 0)
        text = item.get('text', '').replace('\n', ' ')
        time_str = format_time(start_time)
        md_content += f"- **[{time_str}]** {text}\n"

    with open("3s2Q1nViZ1w_transcript.md", "w", encoding="utf-8") as f:
        f.write(md_content)
    
    print("SUCCESS")
except Exception as e:
    print(f"Error: {e}")

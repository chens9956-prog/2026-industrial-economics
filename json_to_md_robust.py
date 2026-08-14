import json
import math

def format_time(seconds):
    mins = math.floor(seconds / 60)
    secs = int(seconds % 60)
    return f"{mins:02d}:{secs:02d}"

try:
    with open("transcript.json", "r", encoding="utf-16") as f:
        content = f.read().strip()
        if not content:
            print("File is empty.")
            exit(1)
        data = json.loads(content)

    md_content = "# YouTube Video Transcript (3s2Q1nViZ1w)\n\n"
    
    if isinstance(data, list):
        if len(data) > 0 and isinstance(data[0], list):
            items = data[0]
        else:
            items = data
    elif isinstance(data, dict):
        key = list(data.keys())[0]
        items = data[key]
    else:
        items = []

    for item in items:
        if isinstance(item, dict):
            start_time = item.get('start', 0)
            text = item.get('text', '').replace('\n', ' ')
            time_str = format_time(start_time)
            md_content += f"- **[{time_str}]** {text}\n"

    with open("3s2Q1nViZ1w_transcript.md", "w", encoding="utf-8") as f:
        f.write(md_content)
    
    print("SUCCESS: 3s2Q1nViZ1w_transcript.md generated")
except Exception as e:
    import traceback
    traceback.print_exc()

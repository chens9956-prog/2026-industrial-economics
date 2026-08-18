import json
import os

transcript_path = r'C:\Users\ausu\.gemini\antigravity\brain\48a8be4f-7705-48d3-9456-30d2f3f49048\.system_generated\logs\transcript.jsonl'
lines = open(transcript_path, 'r', encoding='utf-8').readlines()
ans_list = []
for line in lines:
    try:
        data = json.loads(line)
        if data.get('type') == 'MCP_TOOL':
            content = data.get('content', '')
            ans = ''
            if '{"status":"success"' in content and '"answer"' in content:
                ans = json.loads(content[content.find('{"status":"success"'):]).get('answer', '')
            elif 'The output was large and was saved to: file://' in content:
                file_path = content.split('file:///')[1].strip().replace('/', '\\')
                if os.path.exists(file_path):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        file_content = f.read()
                        if '{"status":"success"' in file_content and '"answer"' in file_content:
                            ans = json.loads(file_content[file_content.find('{"status":"success"'):]).get('answer', '')
            if ans: 
                ans_list.append(ans)
    except:
        pass

for i, a in enumerate(ans_list[-10:]):
    print(f'Ans {i+1}: {a[:30]}...')

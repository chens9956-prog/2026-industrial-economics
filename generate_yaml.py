import os
import json
import re

def extract_answers():
    transcript_path = r"C:\Users\ausu\.gemini\antigravity\brain\48a8be4f-7705-48d3-9456-30d2f3f49048\.system_generated\logs\transcript.jsonl"
    with open(transcript_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
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

    answers = {}
    last_10 = ans_list[-10:]
    for i, a in enumerate(last_10):
        answers[i + 1] = a
    return answers

def generate_yaml():
    output_dir = r"I:\4产业经济学\简报施工图"
    os.makedirs(output_dir, exist_ok=True)
    
    answers = extract_answers()
    
    for ch_num, answer in answers.items():
        ch_str = f"CH{ch_num:02d}"
        
        # Parse points
        points = []
        for p in answer.split('\n'):
            p = p.strip()
            if p:
                # Remove markdown asterisks and numbers like "1. "
                clean_p = p.replace("**", "")
                clean_p = re.sub(r"^\d+\.\s*", "", clean_p)
                points.append(clean_p)
                
        # We need at least some points to fill the layout. If less than 7, we handle gracefully.
        p1 = points[0] if len(points) > 0 else ""
        p2 = points[1] if len(points) > 1 else ""
        p3 = points[2] if len(points) > 2 else ""
        p4 = points[3] if len(points) > 3 else ""
        p5 = points[4] if len(points) > 4 else ""
        p6 = points[5] if len(points) > 5 else ""
        rest_points = points[6:] if len(points) > 6 else []

        yaml_content = f"""# ==========================================
# NotebookLM 简报施工图 Blueprint
# 产业经济学 {ch_str}
# ==========================================
Style: "McKinsey Blue"
Font: "Noto Sans TC"
Language: "Simplified Chinese"

global_config:
  language: "Simplified Chinese"
  font: "Noto Sans TC"

Slides:
  - Title: "产业经济学 {ch_str} 核心精要"
    Layout: Hero
    Content:
      - "{p1}"

  - Title: "关键理论与现象对比"
    Layout: Side-by-Side
    Content:
      Left: "{p2}"
      Right: "{p3}"

  - Title: "核心推演路径"
    Layout: Three-column
    Content:
      Col1: "{p4}"
      Col2: "{p5}"
      Col3: "{p6}"

  - Title: "本章知识盘点 (Checklist)"
    Layout: Summary-check
    Content:"""
        
        for rp in rest_points:
            yaml_content += f"\n      - \"{rp}\""
            
        file_path = os.path.join(output_dir, f"产业经济学{ch_str}_简报施工图.yaml")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(yaml_content)
            
        print(f"Generated {file_path}")

if __name__ == "__main__":
    generate_yaml()

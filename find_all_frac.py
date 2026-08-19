import json

with open(r'l:\我的云端硬盘\2026产业经济学\online-exam-system\questions_data.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

with open(r'l:\我的云端硬盘\2026产业经济学\frac_matches.txt', 'w', encoding='utf-8') as out:
    for q in questions:
        q_str = json.dumps(q, ensure_ascii=False)
        if 'frac' in q_str:
            out.write(f"=== Question ID {q['id']} ===\n")
            out.write(f"Title: {q['title']}\n")
            for opt in q['options']:
                out.write(f"  {opt['key']}: {opt['text']}\n")
            out.write(f"Explanation: {q['explanation']}\n\n")

print("Saved frac matches to frac_matches.txt")

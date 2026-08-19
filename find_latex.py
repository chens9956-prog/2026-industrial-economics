import json

with open(r'l:\我的云端硬盘\2026产业经济学\online-exam-system\questions_data.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

print("Questions containing $: ")
for q in questions:
    has_dollar = False
    if '$' in q['title']:
        print(f"Q{q['id']} title -> {q['title']}")
    if '$' in q['explanation']:
        print(f"Q{q['id']} explanation -> {q['explanation']}")
    for opt in q['options']:
        if '$' in opt['text']:
            print(f"Q{q['id']} option {opt['key']} -> {opt['text']}")

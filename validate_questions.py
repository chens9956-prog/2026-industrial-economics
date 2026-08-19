import json

with open(r'l:\我的云端硬盘\2026产业经济学\online-exam-system\questions_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

singles = [q for q in data if q['type'] == 'single']
multiples = [q for q in data if q['type'] == 'multiple']

print(f"Total questions: {len(data)}")
print(f"Single choice count: {len(singles)} (IDs {singles[0]['id']} to {singles[-1]['id']})")
print(f"Multiple choice count: {len(multiples)} (IDs {multiples[0]['id']} to {multiples[-1]['id']})")

for q in data:
    assert 'id' in q and 'type' in q and 'chapter' in q and 'title' in q and 'options' in q and 'answer' in q and 'explanation' in q
    if q['type'] == 'single':
        assert len(q['answer']) == 1
    else:
        assert len(q['answer']) >= 1

print("Validation passed successfully!")

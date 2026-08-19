import json

# Read current build_60_advanced_questions.py and fix ID 49
with open(r'l:\我的云端硬盘\2026产业经济学\build_60_advanced_questions.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Add ID 49
id_49_str = """  {
    "id": 49,
    "type": "multiple",
    "chapter": "第四章",
    "title": "下列关于产品质量（Quality）与垂直差异化模型的说法，正确的有（ ）。",
    "options": [
      {"key": "A", "text": "当消费者对质量的边际支付意愿不同时，市场上可以同时容纳多种不同质量与价格的产品"},
      {"key": "B", "text": "若高质量与低质量产品以相同价格出售，低质量产品将获得零需求"},
      {"key": "C", "text": "垂直差异化能够帮助企业避免完全价格竞争带来的零利润困境"},
      {"key": "D", "text": "高质量产品必须依赖政府的强制行政管制才能在市场上存续"}
    ],
    "answer": "ABC",
    "explanation": "正确答案是 ABC。A、B、C正确：垂直差异化模型（Mussa-Rosen, Shaked-Sutton）证明，由于消费者收入或偏好导致的对质量支付意愿差异，企通过提供不同质量等级的产品并实施差异化定价，能有效缓解同质削价大战并共享市场。D错误：市场自主价格机制即可维持垂直差异化产品共存。"
  },
"""

code = code.replace('# --- 第五章多选题 ---', id_49_str + '  # --- 第五章多选题 ---')

with open(r'l:\我的云端硬盘\2026产业经济学\build_60_advanced_questions.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Updated script to insert ID 49!")

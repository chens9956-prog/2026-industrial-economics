import re

with open(r'l:\我的云端硬盘\2026产业经济学\build_60_advanced_questions.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Exact text replacements in build_60_advanced_questions.py

replacements = [
    # Q5
    (
        r'"explanation": "正确答案是 A。哈伯格三角（Harberger Triangle）公式 \$DWL = \\frac\{1\}\{2\} \\Delta P \\cdot \\Delta Q = \\frac\{1\}\{2\} P Q \\eta \(\\frac\{P-MC\}\{P\}\)\^2\$ 表明，垄断带来的社会福利净损失取决于垄断加价率（勒纳指数）及需求的价格弹性 \$\\eta\$。"',
        r'"explanation": "正确答案是 A。哈伯格三角（Harberger Triangle）福利损失公式 DWL = 1/2 × ΔP × ΔQ 表明，垄断带来的社会福利净损失取决于垄断加价率（勒纳指数）及需求的价格弹性 η。"'
    ),

    # Q9
    (
        r'"title": "在古诺（Cournot）双寡头模型中，假设两家企业的边际成本均恒定为 \$c\$，市场需求函数为 \$P = a - b\(q_1 \+ q_2\)\$。在纳什均衡状态下，行业总产量为（ ）。"',
        r'"title": "在古诺（Cournot）双寡头模型中，假设两家企业的边际成本均恒定为 c，市场需求函数为 P = a - b(q₁ + q₂)。在纳什均衡状态下，行业总产量为（ ）。"'
    ),
    (
        r'\{"key": "A", "text": "\\$\\frac\{a-c\}\{b\}\\$"\},\n\s*\{"key": "B", "text": "\\$\\frac\{2\(a-c\)\}\{3b\}\\$"\},\n\s*\{"key": "C", "text": "\\$\\frac\{a-c\}\{2b\}\\$"\},\n\s*\{"key": "D", "text": "\\$\\frac\{3\(a-c\)\}\{4b\}\\$"\}',
        r'{"key": "A", "text": "(a - c) / b"},\n      {"key": "B", "text": "2(a - c) / (3b)"},\n      {"key": "C", "text": "(a - c) / (2b)"},\n      {"key": "D", "text": "3(a - c) / (4b)"}'
    ),
    (
        r'"explanation": "正确答案是 B。古诺双寡头均衡下，每家企业的均衡产量为 \$q_1\^\* = q_2\^\* = \\frac\{a-c\}\{3b\}\$，行业总产量 \$Q\^\* = q_1\^\* \+ q_2\^\* = \\frac\{2\(a-c\)\}\{3b\}\$。相较于完全垄断产量 \\$\\frac\{a-c\}\{2b\}\\$ 更高，低于完全竞争产量 \\$\\frac\{a-c\}\{b\}\\$。"',
        r'"explanation": "正确答案是 B。古诺双寡头均衡下，每家企业的均衡产量为 q₁* = q₂* = (a - c) / (3b)，行业总产量 Q* = q₁* + q₂* = 2(a - c) / (3b)。相较于完全垄断产量 (a - c) / (2b) 更高，低于完全竞争产量 (a - c) / b。"'
    ),

    # Q10
    (
        r'\{"key": "B", "text": "价格等于边际成本（\$P = MC\$），出现“伯特兰德悖论”"\}',
        r'{"key": "B", "text": "价格等于边际成本（P = MC），出现“伯特兰德悖论\""}'
    ),
    (
        r'\$P_1 = P_2 = MC\$',
        r'P₁ = P₂ = MC'
    ),

    # Q11
    (
        r'\$q_2\(q_1\)\$',
        r'q₂(q₁)'
    ),

    # Q15
    (
        r'\$n\^\*\$',
        r'n*'
    ),
    (
        r'\$n\^\{soc\}\$',
        r'n_soc'
    ),

    # Q17
    (
        r'\$MR=P\$',
        r'MR = P'
    ),
    (
        r'\$P=MC\$',
        r'P = MC'
    ),

    # Q19
    (
        r'"title": "垄断企业在两个可分割子市场实施三级价格歧视，若市场1的需求弹性绝对值大于市场2（\$\|\\eta_1\| > \|\\eta_2\|\$），则其最优定价策略为（ ）。"',
        r'"title": "垄断企业在两个可分割子市场实施三级价格歧视，若市场1的需求弹性绝对值大于市场2（|η₁| > |η₂|），则其最优定价策略为（ ）。"'
    ),
    (
        r'\{"key": "A", "text": "\$P_1 < P_2\$（弹性越大，定的价格越低）"\}',
        r'{"key": "A", "text": "P₁ < P₂（弹性越大，定的价格越低）"}'
    ),
    (
        r'\{"key": "B", "text": "\$P_1 > P_2\$（弹性越大，定的价格越高）"\}',
        r'{"key": "B", "text": "P₁ > P₂（弹性越大，定的价格越高）"}'
    ),
    (
        r'\{"key": "C", "text": "\$P_1 = P_2\$（两市场价格相同）"\}',
        r'{"key": "C", "text": "P₁ = P₂（两市场价格相同）"}'
    ),
    (
        r'\$P\(1 - \\frac\{1\}\{\|\\eta\|\}\) = MC\$',
        r'P(1 - 1/|η|) = MC'
    ),
    (
        r'\$P_1\(1 - \\frac\{1\}\{\|\\eta_1\|\}\) = P_2\(1 - \\frac\{1\}\{\|\\eta_2\|\}\)\$',
        r'P₁(1 - 1/|η₁|) = P₂(1 - 1/|η₂|)'
    ),

    # Q20
    (
        r'（\$P = MC\$）',
        r'（P = MC）'
    ),
    (
        r'\$F = CS\$',
        r'F = CS'
    ),

    # Q21
    (
        r'"title": "多夫曼-施泰纳定理（Dorfman-Steiner Condition）给出了垄断企业最优广告密度（广告支出与销售收入之比 \$A/PQ\$）的决定公式，即最优广告密度等于（ ）。"',
        r'"title": "多夫曼-施泰纳定理（Dorfman-Steiner Condition）给出了垄断企业最优广告密度（广告支出与销售收入之比 A / (P × Q)）的决定公式，即最优广告密度等于（ ）。"'
    ),
    (
        r'\{"key": "A", "text": "需求广告弹性与需求价格弹性绝对值之比（\$\\frac\{\\epsilon_A\}\{\|\\eta\|\}\$）"\}',
        r'{"key": "A", "text": "需求广告弹性与需求价格弹性绝对值之比（ε_A / |η|）"}'
    ),
    (
        r'\\frac\{A\}\{P Q\} = \\frac\{\\epsilon_A\}\{\|\\eta\|\}\$',
        r'A / (P × Q) = ε_A / |η|'
    ),
    (
        r'\$\\epsilon_A\$',
        r'ε_A'
    ),
    (
        r'\$|\\eta|\$',
        r'|η|'
    ),

    # Q30
    (
        r'\$Q_L\$',
        r'Q_L'
    ),

    # Q33
    (
        r'回报率 \$s\$ 高于企业实际资本市场成本 \$r\$',
        r'回报率 s 高于企业实际资本市场成本 r'
    ),

    # Q34
    (
        r'（即 \$CPI - X\$ 公式）',
        r'（即 CPI - X 公式）'
    ),
    (
        r'\$CPI-X\$',
        r'CPI - X'
    ),
    (
        r'其中 \$CPI\$ 为通货膨胀率，\$X\$ 为预期',
        r'其中 CPI 为通货膨胀率，X 为预期'
    ),

    # Q38
    (
        r'（\$HHI = \\sum s_i\^2\$）',
        r'（HHI = ∑ Sᵢ²）'
    ),
    (
        r'\$HHI = \\sum_\{i=1\}\^n S_i\^2\$（其中 \$S_i\$ 为第 \$i\$ 家企业',
        r'HHI = ∑ Sᵢ²（其中 Sᵢ 为第 i 家企业'
    ),

    # Q53
    (
        r'"title": "多夫曼-施泰纳（Dorfman-Steiner）模型表明，企业倾向于保持更高广告密度的情形包括（ ）。"',
        r'"title": "多夫曼-施泰纳（Dorfman-Steiner）模型表明，企业倾向于保持更高广告密度的情形包括（ ）。"'
    ),
    (
        r'\{"key": "A", "text": "产品需求对广告投入的弹性（\$\\epsilon_A\$）非常高"\}',
        r'{"key": "A", "text": "产品需求对广告投入的弹性（ε_A）非常高"}'
    ),
    (
        r'\{"key": "B", "text": "产品需求的价格弹性（\$|\\eta|\$）非常低（即企业拥有较高的垄断加价率）"\}',
        r'{"key": "B", "text": "产品需求的价格弹性（|η|）非常低（即企业拥有较高的垄断加价率）"}'
    ),
    (
        r'\\frac\{A\}\{PQ\} = \\frac\{\\epsilon_A\}\{\|\\eta\|\}\$',
        r'A / (P × Q) = ε_A / |η|'
    ),

    # Q58
    (
        r'（\$P = MC\$）',
        r'（P = MC）'
    ),
    (
        r'（\$MC < ATC\$）',
        r'（MC < ATC）'
    ),
    (
        r'（\$P = ATC\$）',
        r'（P = ATC）'
    ),

    # Q59
    (
        r'（Price Cap Regulation, \$CPI-X\$）',
        r'（Price Cap Regulation, CPI - X）'
    )
]

for old, new in replacements:
    code = re.sub(old, new, code)

# Clean any remaining $ in code
# Find any remaining lines with $ in python dictionary literals
lines = code.splitlines()
new_lines = []
for line in lines:
    if 'text": "' in line or 'title": "' in line or 'explanation": "' in line:
        line = line.replace('$', '')
    new_lines.append(line)

new_code = '\n'.join(new_lines)

with open(r'l:\我的云端硬盘\2026产业经济学\build_60_advanced_questions.py', 'w', encoding='utf-8') as f:
    f.write(new_code)

print("Updated build_60_advanced_questions.py source code cleanly!")

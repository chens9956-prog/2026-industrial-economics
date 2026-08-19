import json
import re

def clean_text(text):
    if not text:
        return text

    # Specific formula replacements
    replacements = [
        (r'\$DWL = \\frac\{1\}\{2\} \\Delta P \\cdot \\Delta Q = \\frac\{1\}\{2\} P Q \\eta \(\\frac\{P-MC\}\{P\}\)\^2\$', 'DWL = 1/2 × ΔP × ΔQ'),
        (r'\$\\frac\{a-c\}\{b\}\$', '(a - c) / b'),
        (r'\$\\frac\{2\(a-c\)\}\{3b\}\$', '2(a - c) / (3b)'),
        (r'\$\\frac\{a-c\}\{2b\}\$', '(a - c) / (2b)'),
        (r'\$\\frac\{3\(a-c\)\}\{4b\}\$', '3(a - c) / (4b)'),
        (r'\$q_1\^\* = q_2\^\* = \\frac\{a-c\}\{3b\}\$', 'q₁* = q₂* = (a - c) / (3b)'),
        (r'\$Q\^\* = q_1\^\* \+ q_2\^\* = \\frac\{2\(a-c\)\}\{3b\}\$', 'Q* = q₁* + q₂* = 2(a - c) / (3b)'),
        (r'\$\\frac\{a-c\}\{2b\}\$', '(a - c) / (2b)'),
        (r'\$\\frac\{a-c\}\{b\}\$', '(a - c) / b'),
        (r'\$P = a - b\(q_1 \+ q_2\)\$', 'P = a - b(q₁ + q₂)'),
        (r'\$P_1 = P_2 = MC\$', 'P₁ = P₂ = MC'),
        (r'\$P = MC\$', 'P = MC'),
        (r'\$q_2\(q_1\)\$', 'q₂(q₁)'),
        (r'\$n\^\*\$', 'n*'),
        (r'\$n\^\{soc\}\$', 'n_soc'),
        (r'\$MR=P\$', 'MR = P'),
        (r'\$|\=\\eta_1| > |\\eta_2|\$', '|η₁| > |η₂|'),
        (r'\$P_1 < P_2\$', 'P₁ < P₂'),
        (r'\$P_1 > P_2\$', 'P₁ > P₂'),
        (r'\$P_1 = P_2\$', 'P₁ = P₂'),
        (r'\$P\(1 - \\frac\{1\}\{\|\\eta\|\}\) = MC\$', 'P(1 - 1/|η|) = MC'),
        (r'\$P_1\(1 - \\frac\{1\}\{\|\\eta_1\|\}\) = P_2\(1 - \\frac\{1\}\{\|\\eta_2\|\}\)\$', 'P₁(1 - 1/|η₁|) = P₂(1 - 1/|η₂|)'),
        (r'\$F = CS\$', 'F = CS'),
        (r'\\frac\{A\}\{PQ\} = \\frac\{\\epsilon_A\}\{\|\\eta\|\}\$', 'A / (P × Q) = ε_A / |η|'),
        (r'\$\\frac\{\\epsilon_A\}\{\|\\eta\|\}\$', 'ε_A / |η|'),
        (r'\\frac\{A\}\{P Q\} = \\frac\{\\epsilon_A\}\{\|\\eta\|\}\$', 'A / (P × Q) = ε_A / |η|'),
        (r'\$\\epsilon_A\$', 'ε_A'),
        (r'\$|\\eta|\$', '|η|'),
        (r'\$Q_L\$', 'Q_L'),
        (r'\$s\$', 's'),
        (r'\$r\$', 'r'),
        (r'\$CPI - X\$', 'CPI - X'),
        (r'\$CPI-X\$', 'CPI - X'),
        (r'\$CPI\$', 'CPI'),
        (r'\$X\$', 'X'),
        (r'\$HHI = \\sum s_i\^2\$', 'HHI = ∑ Sᵢ²'),
        (r'\$HHI = \\sum_\{i=1\}\^n S_i\^2\$', 'HHI = ∑ Sᵢ²'),
        (r'\$S_i\$', 'Sᵢ'),
        (r'\$i\$', 'i'),
        (r'\$MC < ATC\$', 'MC < ATC'),
        (r'\$P = ATC\$', 'P = ATC'),
        (r'\$c\$', 'c')
    ]

    for pat, repl in replacements:
        text = re.sub(pat, repl, text)

    # General cleanup for any remaining stray $ or latex tags
    text = text.replace('$', '')
    return text

# Load questions_data.json
with open(r'l:\我的云端硬盘\2026产业经济学\online-exam-system\questions_data.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

for q in questions:
    q['title'] = clean_text(q['title'])
    q['explanation'] = clean_text(q['explanation'])
    for opt in q['options']:
        opt['text'] = clean_text(opt['text'])

# Save to online-exam-system/questions_data.json
with open(r'l:\我的云端硬盘\2026产业经济学\online-exam-system\questions_data.json', 'w', encoding='utf-8') as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

# Save to industrial-economics-wxapp/data/questions.js
js_content = "module.exports = " + json.dumps(questions, ensure_ascii=False, indent=2) + ";\n"
with open(r'l:\我的云端硬盘\2026产业经济学\industrial-economics-wxapp\data\questions.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print("Cleaned LaTeX math from questions dataset successfully!")

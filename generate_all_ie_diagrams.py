import os
import sys
import numpy as np
import matplotlib.pyplot as plt

sys.stdout.reconfigure(encoding='utf-8')

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans', 'Arial']
plt.rcParams['axes.unicode_minus'] = False

C_NAVY   = '#1B3A5C'  # 深海蓝
C_BLUE   = '#2E86C1'  # 科技蓝
C_GOLD   = '#C88C1B'  # 暖琥珀金
C_GREEN  = '#1A8C5D'  # 翡翠绿
C_RED    = '#C84B1B'  # 砖红
C_GRAY   = '#6B6B6B'  # 灰色
C_BG     = '#FDFDFD'  # 纯净背景

def set_spine(ax, title="", xlabel="", ylabel=""):
    ax.set_facecolor(C_BG)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color('#333333')
    ax.spines['bottom'].set_color('#333333')
    ax.spines['left'].set_linewidth(1.5)
    ax.spines['bottom'].set_linewidth(1.5)
    if title:
        ax.set_title(title, fontsize=10.0, fontweight='bold', color=C_NAVY, pad=8)
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=8.5, fontweight='bold', color='#333333', loc='right')
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=8.5, fontweight='bold', color='#333333', loc='top')

out_base = r"L:\我的云端硬盘\2026产业经济学\ie_diagrams"
os.makedirs(out_base, exist_ok=True)

# -------------------------------------------------------------
# CH 02 Diagrams
# -------------------------------------------------------------
d2 = os.path.join(out_base, "ch02"); os.makedirs(d2, exist_ok=True)

# 1. 垄断定价与死重损失
fig, ax = plt.subplots(figsize=(6.0, 4.0), dpi=300)
set_spine(ax, "垄断市场均衡定价与哈伯格三角死重损失", xlabel="产量 Q", ylabel="价格 P")
q = np.linspace(0, 10, 100)
p_d = 10 - q
mr = 10 - 2*q
mc = np.full_like(q, 3.0)
ax.plot(q, p_d, color=C_NAVY, lw=2.2, label='市场需求 D: P = 10 - Q')
ax.plot(q, mr, color=C_BLUE, lw=2.0, label='边际收益 MR = 10 - 2Q')
ax.axhline(3.0, color=C_RED, lw=2.0, label='边际成本 MC = 3.0')
# 垄断交点 MR=MC ➔ 10-2Q=3 ➔ Qm=3.5, Pm=6.5; 竞争 Qc=7, Pc=3
ax.plot(3.5, 6.5, 'o', color=C_GOLD, markersize=7)
ax.plot(3.5, 3.0, 'o', color=C_GREEN, markersize=7)
# 阴影: 利润 A (0~3.5, 3~6.5), 死重损失 DWL (3.5~7, 3~P_d)
ax.fill_between([0, 3.5], [3.0, 3.0], [6.5, 6.5], color='#FCF3CF', alpha=0.6, label='垄断超额利润 (A)')
q_dwl = np.linspace(3.5, 7.0, 50)
ax.fill_between(q_dwl, 3.0, 10 - q_dwl, color='#FADBD8', alpha=0.7, label='哈伯格死重损失 (DWL)')
ax.text(4.2, 4.2, 'DWL\n纯福利损失', fontsize=7.5, color=C_RED, fontweight='bold')
ax.set_xlim(0, 9); ax.set_ylim(0, 11); ax.legend(fontsize=6.5, loc='upper right')
plt.tight_layout(); fig.savefig(os.path.join(d2, "chart01_monopoly_deadweight_loss.png")); plt.close(fig)

# 2. 古诺双寡头反应曲线
fig, ax = plt.subplots(figsize=(6.0, 4.0), dpi=300)
set_spine(ax, "古诺双寡头反应函数曲线与纳什均衡点", xlabel="企业 1 产量 q1", ylabel="企业 2 产量 q2")
q1 = np.linspace(0, 10, 100)
r1 = 4.5 - 0.5*q1  # q2 = (a-c)/2b - 0.5q1
r2 = 9.0 - 2.0*q1  # q1 = (a-c)/2b - 0.5q2 ➔ q2 = 9 - 2q1
ax.plot(q1, r1, color=C_BLUE, lw=2.2, label='企业 1 反应曲线: R1(q2)')
ax.plot(q1, r2, color=C_RED, lw=2.2, label='企业 2 反应曲线: R2(q1)')
# 交点 q1*=3, q2*=3
ax.plot(3.0, 3.0, 'o', color=C_GOLD, markersize=9)
ax.text(3.3, 3.3, '古诺纳什均衡 (q1*=3, q2*=3)\n行业总产出 Q=6\n价格高于竞争但低于垄断', fontsize=7.5, color=C_NAVY, fontweight='bold')
ax.set_xlim(0, 7); ax.set_ylim(0, 7); ax.legend(fontsize=7.0, loc='upper right')
plt.tight_layout(); fig.savefig(os.path.join(d2, "chart02_cournot_duopoly_reaction.png")); plt.close(fig)

# 3. 伯川德价格竞争与悖论
fig, ax = plt.subplots(figsize=(6.0, 4.0), dpi=300)
set_spine(ax, "伯川德价格竞争模型与伯川德悖论", xlabel="企业 1 价格 p1", ylabel="企业 2 价格 p2")
p = np.linspace(0, 10, 100)
ax.plot(p, p, color=C_GRAY, ls='--', lw=1.5, label='45° 等价线 p1 = p2')
# 纳什均衡点 p1=p2=c
ax.plot(3.0, 3.0, 'o', color=C_RED, markersize=9)
ax.axhline(3.0, color=C_BLUE, ls=':', lw=1.2)
ax.axvline(3.0, color=C_BLUE, ls=':', lw=1.2)
ax.text(3.3, 2.2, '伯川德悖论均衡:\np1* = p2* = MC = 3\n仅需 2 家企业即退化为完全竞争！', fontsize=7.5, color=C_RED, fontweight='bold')
ax.text(0.8, 6.5, '【消解悖论的途径】\n1. 产品差异化 (非同质)\n2. 产能约束 (埃奇沃思)\n3. 动态重复博弈合谋', fontsize=7.5, color=C_NAVY, bbox=dict(boxstyle='round,pad=0.4', facecolor='#EAEDED', edgecolor=C_NAVY))
ax.set_xlim(0, 8); ax.set_ylim(0, 8); ax.legend(fontsize=7.0, loc='upper left')
plt.tight_layout(); fig.savefig(os.path.join(d2, "chart03_bertrand_price_competition.png")); plt.close(fig)

# 4. 垄断竞争长期切线均衡与过剩产能
fig, ax = plt.subplots(figsize=(6.0, 4.0), dpi=300)
set_spine(ax, "垄断竞争长期切线均衡与过剩生产力 (Chamberlin)", xlabel="产量 Q", ylabel="价格 / 成本")
qc = np.linspace(1, 10, 100)
lac = 3 + 12 / qc + 0.3 * (qc - 6)**2
d_sr = 12 - 1.2*qc
ax.plot(qc, lac, color=C_NAVY, lw=2.2, label='长期平均成本 LAC')
ax.plot(qc, d_sr, color=C_BLUE, lw=2.0, label='主观需求曲线 d (切线)')
# 切点 Qm=4, P=7.2, 最低成本点 Q_opt=6
ax.plot(4.0, 7.2, 'o', color=C_GOLD, markersize=8)
ax.plot(6.0, 5.0, 'o', color=C_GREEN, markersize=8)
ax.plot([4.0, 6.0], [7.2, 5.0], color=C_RED, ls='--', lw=1.2)
ax.text(4.2, 7.5, '长期切点均衡 (P = LAC, 经济利润=0)', fontsize=7.0, color=C_GOLD, fontweight='bold')
ax.text(3.5, 3.2, '过剩生产能力 (Excess Capacity) = Q_opt - Qm\n消费者为多样性支付适度溢价', fontsize=7.5, color=C_RED, bbox=dict(boxstyle='round,pad=0.3', facecolor='#FADBD8', edgecolor=C_RED))
ax.set_xlim(1, 9); ax.set_ylim(2, 12); ax.legend(fontsize=6.5, loc='upper right')
plt.tight_layout(); fig.savefig(os.path.join(d2, "chart04_monopolistic_competition_equilibrium.png")); plt.close(fig)

# -------------------------------------------------------------
# CH 03 Diagrams
# -------------------------------------------------------------
d3 = os.path.join(out_base, "ch03"); os.makedirs(d3, exist_ok=True)

# 1. 勒纳指数与 HHI
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.6, 3.8), dpi=300)
fig.patch.set_facecolor(C_BG)
set_spine(ax1, "勒纳指数 L = (P-MC)/P = 1/|ε|", xlabel="需求弹性 |ε|", ylabel="市场势力勒纳指数 L")
eps = np.linspace(1.1, 10, 100)
l_val = 1.0 / eps
ax1.plot(eps, l_val, color=C_NAVY, lw=2.2)
ax1.plot(2.0, 0.5, 'o', color=C_RED, markersize=7)
ax1.text(2.3, 0.52, '|ε|=2 ➔ L=0.50', fontsize=7.0, color=C_RED, fontweight='bold')
ax1.set_xlim(1, 10); ax1.set_ylim(0, 1.0)

set_spine(ax2, "赫芬达尔指数 HHI = ∑ si² 集中度", xlabel="行业前4大企业份额", ylabel="HHI 指数 (0~10000)")
hhi_levels = [500, 1200, 1800, 3500]
h_names = ['低集中\n(<1000)', '中低集中\n(1000~1500)', '中高集中\n(1500~2500)', '高集中垄断\n(>2500)']
ax2.bar(h_names, hhi_levels, color=[C_GREEN, C_BLUE, C_GOLD, C_RED], width=0.55)
ax2.set_ylim(0, 4000)
plt.tight_layout(); fig.savefig(os.path.join(d3, "chart01_lerner_herfindahl_index.png")); plt.close(fig)

# 2. SCP 范式框架
fig, ax = plt.subplots(figsize=(6.2, 4.0), dpi=300)
ax.set_facecolor(C_BG); ax.axis('off')
ax.set_title("哈佛学派 SCP 范式与新产业组织理论 (NEIO) 框架", fontsize=10.0, fontweight='bold', color=C_NAVY, pad=8)
boxes = [
    (0.18, 0.65, '市场结构 Structure\n· 集中度 CR/HHI\n· 进入与退出壁垒\n· 产品差异化程度', C_BLUE),
    (0.50, 0.65, '市场行为 Conduct\n· 价格竞争与合谋\n· 广告与研发投资\n· 策略性进入阻碍', C_GOLD),
    (0.82, 0.65, '市场绩效 Performance\n· 资源配置效率\n· 利润率与技术进步\n· 消费者与社会福利', C_GREEN)
]
for x, y, lab, col in boxes:
    ax.plot(x, y, 's', color=col, markersize=26)
    ax.text(x - 0.12, y - 0.05, lab, color='#FFFFFF', fontweight='bold', fontsize=6.8)
ax.annotate('', xy=(0.35, 0.65), xytext=(0.28, 0.65), arrowprops=dict(arrowstyle="->", lw=2, color=C_NAVY))
ax.annotate('', xy=(0.67, 0.65), xytext=(0.60, 0.65), arrowprops=dict(arrowstyle="->", lw=2, color=C_NAVY))
ax.text(0.12, 0.20, '【双向反馈演进】\n· 传统哈佛学派：S 决定 C 决定 P（单向因果链）；\n· 芝加哥学派 & 现代博弈论：企业策略行为 C 反作用于市场结构 S（如掠夺性定价构筑壁垒）。', fontsize=7.5, color=C_NAVY, bbox=dict(boxstyle='round,pad=0.4', facecolor='#EAEDED', edgecolor=C_NAVY))
ax.set_xlim(0, 1.0); ax.set_ylim(0, 1.0)
plt.tight_layout(); fig.savefig(os.path.join(d3, "chart02_scp_paradigm_framework.png")); plt.close(fig)

# 3. 集中度与利润率关系拟合
fig, ax = plt.subplots(figsize=(6.0, 4.0), dpi=300)
set_spine(ax, "行业集中度 (CR4) 与行业利润率 (PCM) 计量检验", xlabel="行业集中度 CR4 (%)", ylabel="价格-成本加成率 PCM (%)")
np.random.seed(42)
cr_data = np.linspace(15, 85, 20)
pcm_data = 5 + 0.25*cr_data + np.random.normal(0, 3, 20)
ax.scatter(cr_data, pcm_data, color=C_BLUE, s=45, label='各产业观测样本点')
slope, intercept = np.polyfit(cr_data, pcm_data, 1)
ax.plot(cr_data, intercept + slope*cr_data, color=C_RED, lw=2.2, label=f'拟合回归线: PCM = {intercept:.1f} + {slope:.2f} CR4')
ax.text(18, 22, '【实证争鸣】\n· 共谋假说 (Collusion): 高集中促进价格协同;\n· 效率假说 (Demsetz Efficiency): 效率更高的企业自然获得更高市场份额。', fontsize=7.0, color=C_NAVY, bbox=dict(boxstyle='round,pad=0.3', facecolor='#EAEDED', edgecolor=C_NAVY))
ax.set_xlim(10, 90); ax.set_ylim(0, 32); ax.legend(fontsize=6.5, loc='lower right')
plt.tight_layout(); fig.savefig(os.path.join(d3, "chart03_concentration_profit_relation.png")); plt.close(fig)

# 4. 市场势力福利损失实证测算
fig, ax = plt.subplots(figsize=(6.0, 4.0), dpi=300)
set_spine(ax, "哈伯格与考林-穆勒市场势力福利损失模型", xlabel="市场产出 Q", ylabel="价格 P")
q = np.linspace(0, 10, 100)
ax.plot(q, 10 - q, color=C_NAVY, lw=2.0, label='需求曲线 D')
ax.axhline(3.0, color=C_GREEN, lw=1.8, label='边际成本 MC')
ax.plot([0, 4, 4], [7, 7, 3], color=C_RED, ls=':', lw=1.2)
ax.fill_between([0, 4], [3, 3], [7, 7], color='#FCF3CF', alpha=0.6, label='垄断租金 A (寻租成本/Tullock 耗散)')
q_t = np.linspace(4, 7, 50)
ax.fill_between(q_t, 3.0, 10 - q_t, color='#FADBD8', alpha=0.7, label='传统哈伯格三角 W')
ax.text(1.2, 5.0, '租金 A\n(若完全寻租耗散\n损失达 GDP 5~10%)', fontsize=7.0, color=C_GOLD, fontweight='bold')
ax.text(4.5, 4.0, '三角 W (哈伯格测算\n仅占 GDP 0.1%)', fontsize=7.0, color=C_RED, fontweight='bold')
ax.set_xlim(0, 9); ax.set_ylim(0, 11); ax.legend(fontsize=6.5, loc='upper right')
plt.tight_layout(); fig.savefig(os.path.join(d3, "chart04_welfare_loss_harberger.png")); plt.close(fig)

# -------------------------------------------------------------
# CH 04 ~ CH 10 Diagrams (batch generated)
# -------------------------------------------------------------
for ch_idx in range(4, 11):
    cdir = os.path.join(out_base, f"ch{ch_idx:02d}"); os.makedirs(cdir, exist_ok=True)

# CH 04: Hotelling, Salop, etc.
d4 = os.path.join(out_base, "ch04")
fig, ax = plt.subplots(figsize=(6.0, 4.0), dpi=300)
set_spine(ax, "霍特林线形城市模型与产品定位 (Hotelling Linear City)", xlabel="空间距离 / 产品特征 x", ylabel="消费者承担的总支出 (P + tx)")
x = np.linspace(0, 1, 100)
# A 在 0 处, B 在 1 处
ax.plot(x, 2 + 1.5*x, color=C_BLUE, lw=2.2, label='从厂商 A 购买总支出: PA + tx')
ax.plot(x, 2.5 + 1.5*(1-x), color=C_RED, lw=2.2, label='从厂商 B 购买总支出: PB + t(1-x)')
# 交点无差异消费者 x_hat (2 + 1.5x = 2.5 + 1.5 - 1.5x ➔ 3x = 2 ➔ x = 0.67)
ax.plot(0.67, 3.0, 'o', color=C_GOLD, markersize=8)
ax.axvline(0.67, color=C_GRAY, ls=':', lw=1.2)
ax.text(0.69, 3.2, '无差异分界点 x*\n左侧买 A，右侧买 B', fontsize=7.5, color=C_NAVY, fontweight='bold')
ax.set_xlim(0, 1); ax.set_ylim(1, 5); ax.legend(fontsize=7.0, loc='upper center')
plt.tight_layout(); fig.savefig(os.path.join(d4, "chart01_hotelling_linear_city.png")); plt.close(fig)

fig, ax = plt.subplots(figsize=(6.0, 4.0), dpi=300)
ax.set_facecolor(C_BG); ax.axis('off')
ax.set_title("萨洛普圆形城市模型 (Salop Circular City)", fontsize=10.0, fontweight='bold', color=C_NAVY, pad=8)
theta = np.linspace(0, 2*np.pi, 200)
ax.plot(np.cos(theta), np.sin(theta), color=C_NAVY, lw=2.5)
# 4 个均匀分布店铺
pts = np.linspace(0, 2*np.pi, 5)[:-1]
for i, p in enumerate(pts):
    ax.plot(np.cos(p), np.sin(p), 'o', color=[C_BLUE, C_RED, C_GREEN, C_GOLD][i], markersize=10)
    ax.text(1.2*np.cos(p) - 0.1, 1.2*np.sin(p), f'店铺 {i+1}', fontsize=7.5, fontweight='bold', color=C_NAVY)
ax.text(-0.65, -0.1, '【自由进入均衡】\n均衡店铺数量 n* = √(t / F)\n在产品多样性与固定成本间权衡', fontsize=7.5, color=C_NAVY, bbox=dict(boxstyle='round,pad=0.4', facecolor='#EAEDED', edgecolor=C_NAVY))
ax.set_xlim(-1.5, 1.5); ax.set_ylim(-1.5, 1.5)
plt.tight_layout(); fig.savefig(os.path.join(d4, "chart02_salop_circular_city.png")); plt.close(fig)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.6, 3.8), dpi=300)
fig.patch.set_facecolor(C_BG)
set_spine(ax1, "横向差异 (Horizontal): 口味不同", xlabel="特征属性 (如甜度/颜色)", ylabel="消费者偏好分布")
ax1.plot([0, 1], [1, 1], color=C_BLUE, lw=3)
ax1.text(0.1, 0.5, '同价下无绝对优劣\n各有所爱', fontsize=7.5, color=C_NAVY)
set_spine(ax2, "纵向差异 (Vertical): 质量档次", xlabel="质量等级 s (低 ➔ 高)", ylabel="支付意愿 (P_high > P_low)")
ax2.plot([1, 5], [2, 8], color=C_GREEN, lw=3)
ax2.text(1.5, 6.0, '同价下所有人\n均偏好高质量', fontsize=7.5, color=C_GREEN, fontweight='bold')
plt.tight_layout(); fig.savefig(os.path.join(d4, "chart03_horizontal_vertical_differentiation.png")); plt.close(fig)

fig, ax = plt.subplots(figsize=(6.0, 4.0), dpi=300)
set_spine(ax, "产品差异化缓解价格战博弈机理", xlabel="产品差异化程度 Δ", ylabel="均衡价格与企业利润")
delta = np.linspace(0.1, 5, 100)
p_eq = 2 + 1.2*delta
prof = 0.8 * delta
ax.plot(delta, p_eq, color=C_BLUE, lw=2.2, label='均衡价格 P* = c + tΔ')
ax.plot(delta, prof, color=C_RED, lw=2.2, label='企业均衡利润 π*')
ax.text(0.5, 5.0, '最大差异化原则 (Principle of Max Differentiation):\n差异化越显著 ➔ 需求交叉弹性越低 ➔ 规避恶性价格战！', fontsize=7.0, color=C_NAVY, bbox=dict(boxstyle='round,pad=0.3', facecolor='#EAEDED', edgecolor=C_NAVY))
ax.set_xlim(0, 5); ax.set_ylim(0, 9); ax.legend(fontsize=7.0, loc='lower right')
plt.tight_layout(); fig.savefig(os.path.join(d4, "chart04_chamberlin_monopolistic_diff.png")); plt.close(fig)

# CH 05: Price Discrimination
d5 = os.path.join(out_base, "ch05")
fig, ax = plt.subplots(figsize=(6.0, 4.0), dpi=300)
set_spine(ax, "一、二、三级价格歧视消费者剩余剥夺", xlabel="消费数量 Q", ylabel="价格 P")
q = np.linspace(0, 10, 100)
ax.plot(q, 10 - q, color=C_NAVY, lw=2.2, label='需求曲线 D')
ax.axhline(2.0, color=C_GREEN, lw=1.8, label='边际成本 MC = 2')
ax.fill_between(q[q <= 8], 2.0, 10 - q[q <= 8], color='#FCF3CF', alpha=0.7, label='一级价格歧视: 全部消费者剩余转化为利润')
ax.set_xlim(0, 10); ax.set_ylim(0, 11); ax.legend(fontsize=6.5, loc='upper right')
plt.tight_layout(); fig.savefig(os.path.join(d5, "chart01_first_second_third_degree.png")); plt.close(fig)

fig, ax = plt.subplots(figsize=(6.0, 4.0), dpi=300)
set_spine(ax, "两段收费制 (Two-Part Tariff) 最优定价模型", xlabel="使用量 q", ylabel="单价 P 与 入场费 T")
ax.plot(q, 10 - q, color=C_NAVY, lw=2.2, label='消费者需求 D')
ax.axhline(2.0, color=C_RED, lw=2.0, label='按边际成本定价: P* = MC = 2')
ax.fill_between(q[q <= 8], 2.0, 10 - q[q <= 8], color='#D4E6F1', alpha=0.7, label='固定入场费 T* = 剩余 CS (游乐园门票)')
ax.text(1.5, 4.5, '最优两段收费:\n1. 使用费定为 P = MC (无死重损失!)\n2. 入场费 T 提取全部消费者剩余', fontsize=7.5, color=C_NAVY, bbox=dict(boxstyle='round,pad=0.3', facecolor='#EAEDED', edgecolor=C_NAVY))
ax.set_xlim(0, 10); ax.set_ylim(0, 11); ax.legend(fontsize=6.5, loc='upper right')
plt.tight_layout(); fig.savefig(os.path.join(d5, "chart02_two_part_tariff.png")); plt.close(fig)

fig, ax = plt.subplots(figsize=(6.0, 4.0), dpi=300)
set_spine(ax, "商品捆绑销售 (Bundling) 收益扩张矩阵", xlabel="消费者对商品 1 估价 r1", ylabel="消费者对商品 2 估价 r2")
ax.axhline(4.0, color=C_GRAY, ls=':', lw=1.2)
ax.axvline(4.0, color=C_GRAY, ls=':', lw=1.2)
ax.plot([0, 7], [7, 0], color=C_RED, lw=2.2, label='捆绑包价格线: r1 + r2 = Pb = 7')
ax.text(4.2, 4.2, '单独购买两者', fontsize=7.0, color=C_NAVY, fontweight='bold')
ax.text(1.0, 4.5, '捆绑购买区\n(r1+r2 ≥ Pb)', fontsize=7.0, color=C_RED, fontweight='bold')
ax.text(0.5, 1.5, '不购买任何产品', fontsize=7.0, color=C_GRAY)
ax.set_xlim(0, 8); ax.set_ylim(0, 8); ax.legend(fontsize=7.0, loc='upper right')
plt.tight_layout(); fig.savefig(os.path.join(d5, "chart03_bundling_tying_surplus.png")); plt.close(fig)

fig, ax = plt.subplots(figsize=(6.0, 4.0), dpi=300)
set_spine(ax, "耐用品垄断与科斯猜想 (Coase Conjecture)", xlabel="交易时期 t", ylabel="耐用品价格 Pt")
t = np.arange(1, 8)
p_coase = 10 / (1 + 0.6*t)
ax.plot(t, p_coase, 'o-', color=C_RED, lw=2.2, label='垄断降价路径')
ax.axhline(2.0, color=C_GREEN, lw=1.8, ls='--', label='边际成本 MC = 2')
ax.text(2.0, 6.0, '【科斯猜想】\n消费者理性预期未来必降价而推迟购买，\n垄断者被迫在一瞬间将价格降至 MC！\n解决对策：只租不售、保价承诺、产品升级。', fontsize=7.0, color=C_NAVY, bbox=dict(boxstyle='round,pad=0.3', facecolor='#EAEDED', edgecolor=C_NAVY))
ax.set_xlim(0.5, 7.5); ax.set_ylim(0, 10); ax.legend(fontsize=7.0, loc='upper right')
plt.tight_layout(); fig.savefig(os.path.join(d5, "chart04_durable_goods_coase_conjecture.png")); plt.close(fig)

# CH 06: Advertising
d6 = os.path.join(out_base, "ch06")
fig, ax = plt.subplots(figsize=(6.0, 4.0), dpi=300)
set_spine(ax, "多夫曼-施泰纳定理: 最优广告强度 A/(PQ) = εa/εp", xlabel="广告需求弹性 εa", ylabel="最优广告强度 A/PQ (%)")
ea = np.linspace(0.05, 0.5, 100)
ax.plot(ea, (ea / 2.0)*100, color=C_BLUE, lw=2.2, label='价格弹性 εp = 2.0')
ax.plot(ea, (ea / 1.0)*100, color=C_RED, lw=2.2, label='价格弹性 εp = 1.0 (高垄断溢价)')
ax.text(0.08, 32, 'Dorfman-Steiner 定理:\n最优广告费用比率 = 广告弹性 / 价格弹性\n垄断程度越高 (εp小) 或广告拉动越强 ➔ 广告投入比越大', fontsize=7.0, color=C_NAVY, bbox=dict(boxstyle='round,pad=0.3', facecolor='#EAEDED', edgecolor=C_NAVY))
ax.set_xlim(0.05, 0.5); ax.set_ylim(0, 50); ax.legend(fontsize=6.5, loc='lower right')
plt.tight_layout(); fig.savefig(os.path.join(d6, "chart01_dorfman_steiner_condition.png")); plt.close(fig)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.6, 3.8), dpi=300)
fig.patch.set_facecolor(C_BG)
set_spine(ax1, "搜寻品 (Search Goods)", xlabel="", ylabel="")
ax1.bar(['信息性广告\n(告知价格/规格)'], [80], color=C_BLUE, width=0.4)
ax1.set_ylim(0, 100); ax1.text(-0.25, 45, '购买前即可\n检验真实质量', fontsize=7.0, color='#FFFFFF', fontweight='bold')
set_spine(ax2, "经验品 (Experience Goods)", xlabel="", ylabel="")
ax2.bar(['劝说与信号\n(巨额烧钱广告)'], [90], color=C_GOLD, width=0.4)
ax2.set_ylim(0, 100); ax2.text(-0.25, 45, '巨额广告作为\n高质量承诺抵押', fontsize=7.0, color='#FFFFFF', fontweight='bold')
plt.tight_layout(); fig.savefig(os.path.join(d6, "chart02_search_experience_goods.png")); plt.close(fig)

fig, ax = plt.subplots(figsize=(6.0, 4.0), dpi=300)
set_spine(ax, "广告强度与行业集中度倒 U 形假说", xlabel="行业集中度 CR4 (%)", ylabel="行业平均广告销售比 A/S (%)")
cr = np.linspace(0, 100, 100)
ad_u = 1 + 0.18*cr - 0.0018*cr**2
ax.plot(cr, ad_u, color=C_NAVY, lw=2.5, label='倒 U 形曲线假说')
ax.plot(50, 5.5, 'o', color=C_RED, markersize=8)
ax.text(40, 6.0, '中度集中寡头市场\n广告竞争最白热化', fontsize=7.5, color=C_RED, fontweight='bold')
ax.text(5, 1.5, '完全竞争:\n搭便车不愿做', fontsize=6.8, color=C_GRAY)
ax.text(78, 1.5, '高度垄断:\n缺乏竞争无需做', fontsize=6.8, color=C_GRAY)
ax.set_xlim(0, 100); ax.set_ylim(0, 7.5); ax.legend(fontsize=7.0, loc='upper left')
plt.tight_layout(); fig.savefig(os.path.join(d6, "chart03_advertising_market_structure.png")); plt.close(fig)

fig, ax = plt.subplots(figsize=(6.0, 4.0), dpi=300)
set_spine(ax, "互联网程序化广告与广义第二价格拍卖 (GSP)", xlabel="广告主竞价排名", ylabel="点击竞价出价 vs 实际结算价")
ranks = ['第1位 (CTR高)', '第2位 (CTR中)', '第3位 (CTR低)']
bid = [10.0, 8.0, 5.0]
pay = [8.01, 5.01, 3.01]
x_pos = np.arange(len(ranks))
ax.bar(x_pos - 0.15, bid, width=0.3, label='广告主出价 Bid', color=C_BLUE)
ax.bar(x_pos + 0.15, pay, width=0.3, label='实际支付价 (第二名+0.01)', color=C_GREEN)
ax.set_xticks(x_pos); ax.set_xticklabels(ranks, fontsize=7.5)
ax.legend(fontsize=7.0, loc='upper right')
plt.tight_layout(); fig.savefig(os.path.join(d6, "chart04_internet_ad_pricing_cpc.png")); plt.close(fig)

# CH 07: R&D and Innovation
d7 = os.path.join(out_base, "ch07")
fig, ax = plt.subplots(figsize=(6.0, 4.0), dpi=300)
set_spine(ax, "熊彼特假说 vs 阿罗替代效应创新激励对比", xlabel="市场竞争程度", ylabel="企业创新研发投入")
comp = np.linspace(0, 10, 100)
schumpeter = 8 - 0.6*comp
arrow = 2 + 0.6*comp
ax.plot(comp, schumpeter, color=C_RED, lw=2.2, label='熊彼特假说: 垄断超额利润为创新提供充沛资金')
ax.plot(comp, arrow, color=C_BLUE, lw=2.2, label='阿罗替代效应: 竞争市场创新收益 > 垄断企业替换自身')
ax.text(2.5, 4.8, '阿吉翁倒 U 型创新关系:\n适度竞争最能激发创新动力！', fontsize=7.5, color=C_NAVY, bbox=dict(boxstyle='round,pad=0.3', facecolor='#EAEDED', edgecolor=C_NAVY))
ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.legend(fontsize=6.5, loc='lower center')
plt.tight_layout(); fig.savefig(os.path.join(d7, "chart01_schumpeterian_hypothesis.png")); plt.close(fig)

fig, ax = plt.subplots(figsize=(6.0, 4.0), dpi=300)
set_spine(ax, "工艺创新 (降成本) 社会福利收益模型", xlabel="产量 Q", ylabel="价格 / 成本 P, MC")
q = np.linspace(0, 10, 100)
ax.plot(q, 10 - q, color=C_NAVY, lw=2.0, label='需求 D')
ax.axhline(6.0, color=C_RED, lw=1.8, label='创新前成本 MC0')
ax.axhline(3.0, color=C_GREEN, lw=1.8, label='创新后成本 MC1')
ax.fill_between([0, 4], [3, 3], [6, 6], color='#D5F5E3', alpha=0.7, label='成本节约总福利增加')
ax.text(1.2, 4.2, '节约生产成本 ΔMC × Q', fontsize=7.5, color=C_GREEN, fontweight='bold')
ax.set_xlim(0, 9); ax.set_ylim(0, 11); ax.legend(fontsize=6.5, loc='upper right')
plt.tight_layout(); fig.savefig(os.path.join(d7, "chart02_process_product_innovation.png")); plt.close(fig)

fig, ax = plt.subplots(figsize=(6.0, 4.0), dpi=300)
set_spine(ax, "专利竞赛 (Patent Race) 研发过度投资博弈", xlabel="行业总研发投入经费 R", ylabel="各企业期望净收益 E(π)")
r = np.linspace(0, 10, 100)
exp_pi = 6 + 2*r - 0.4*r**2
social_opt = 6 + 2*r - 0.6*r**2
ax.plot(r, exp_pi, color=C_RED, lw=2.2, label='私有专利竞赛投入均衡 (赢者通吃过度研发)')
ax.plot(r, social_opt, color=C_GREEN, lw=2.2, label='社会最优研发投入水平')
ax.text(4.0, 2.0, '专利战零和博弈：\n追求首发效应导致企业过度投入研发！', fontsize=7.0, color=C_RED, bbox=dict(boxstyle='round,pad=0.3', facecolor='#FADBD8', edgecolor=C_RED))
ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.legend(fontsize=6.5, loc='upper right')
plt.tight_layout(); fig.savefig(os.path.join(d7, "chart03_patent_race_game.png")); plt.close(fig)

fig, ax = plt.subplots(figsize=(6.0, 4.0), dpi=300)
set_spine(ax, "新技术采纳扩散的 S 形曲线 (Logistic Diffusion)", xlabel="时间 t", ylabel="新技术市场普及率 y(t) (%)")
t = np.linspace(-6, 6, 100)
y_s = 100 / (1 + np.exp(-t))
ax.plot(t, y_s, color=C_NAVY, lw=2.5, label='Logistic 扩散曲线')
ax.axhline(50, color=C_GRAY, ls=':', lw=1.2)
ax.text(-5, 15, '导入期 (早期先锋)', fontsize=7.0, color=C_GRAY)
ax.text(-1, 55, '爆发成长期 (主流采纳)', fontsize=7.0, color=C_GREEN, fontweight='bold')
ax.text(3, 88, '成熟饱和期', fontsize=7.0, color=C_GRAY)
ax.set_xlim(-6, 6); ax.set_ylim(0, 105); ax.legend(fontsize=7.0, loc='lower right')
plt.tight_layout(); fig.savefig(os.path.join(d7, "chart04_technology_diffusion_s_curve.png")); plt.close(fig)

# CH 08: Entry and Exit
d8 = os.path.join(out_base, "ch08")
fig, ax = plt.subplots(figsize=(6.0, 4.0), dpi=300)
set_spine(ax, "贝恩-西洛斯限制性定价模型 (Limit Pricing)", xlabel="产量 Q", ylabel="价格 P")
q = np.linspace(0, 10, 100)
ax.plot(q, 10 - q, color=C_NAVY, lw=2.2, label='市场总需求 D')
ax.axhline(4.5, color=C_RED, lw=2.0, ls='--', label='限制性价格 Pl (潜在进入者 LAC 最低点)')
ax.plot(5.5, 4.5, 'o', color=C_GOLD, markersize=8)
ax.text(1.0, 2.5, '【在位者策略】\n在位企业定产 QL = 5.5, 定价 Pl = 4.5\n使进入者剩余需求曲线完全位于其 LAC 下方，\n进入必亏损，从而成功阻碍进入！', fontsize=7.0, color=C_NAVY, bbox=dict(boxstyle='round,pad=0.4', facecolor='#EAEDED', edgecolor=C_NAVY))
ax.set_xlim(0, 9); ax.set_ylim(0, 11); ax.legend(fontsize=6.5, loc='upper right')
plt.tight_layout(); fig.savefig(os.path.join(d8, "chart01_bain_sylos_limit_pricing.png")); plt.close(fig)

fig, ax = plt.subplots(figsize=(6.0, 4.0), dpi=300)
set_spine(ax, "迪克西特产能承诺可信威胁模型 (Dixit Commitment)", xlabel="在位者产能 K1", ylabel="在位者与进入者利润")
k = np.linspace(0, 10, 100)
ax.plot(k, 2 + 0.8*k, color=C_BLUE, lw=2.2, label='在位者收益')
ax.plot(k, 8 - 1.0*k, color=C_RED, lw=2.2, label='进入者预期收益')
ax.axhline(0, color=C_GRAY, ls='-', lw=1.0)
ax.axvline(8.0, color=C_GOLD, ls=':', lw=1.5)
ax.text(5.0, 6.5, '预先沉淀超额产能 K1 ≥ 8 ➔\n发生进入时发动价格战变成可信威胁！', fontsize=7.0, color=C_RED, bbox=dict(boxstyle='round,pad=0.3', facecolor='#FADBD8', edgecolor=C_RED))
ax.set_xlim(0, 10); ax.set_ylim(-2, 11); ax.legend(fontsize=6.5, loc='upper right')
plt.tight_layout(); fig.savefig(os.path.join(d8, "chart02_dixit_capacity_commitment.png")); plt.close(fig)

fig, ax = plt.subplots(figsize=(6.0, 4.0), dpi=300)
ax.set_facecolor(C_BG); ax.axis('off')
ax.set_title("结构性壁垒 vs 策略性进入壁垒与退出壁垒矩阵", fontsize=10.0, fontweight='bold', color=C_NAVY, pad=8)
bars = [
    (0.25, 0.65, '结构性进入壁垒\n(客观外部环境)\n· 规模经济与巨额投资\n· 绝对成本与资源卡位\n· 转换成本与消费者黏性', C_BLUE),
    (0.75, 0.65, '策略性进入壁垒\n(在位者博弈行为)\n· 限制性定价与掠夺定价\n· 沉没性超额产能投资\n· 纵向排他性排他契约', C_RED),
    (0.50, 0.22, '退出壁垒 (Exit Barriers)\n· 专用性资产残值损失沉没 · 员工解雇补偿与违约金 · 政府行政管制与声誉羁绊', C_GOLD)
]
for x, y, lab, col in bars:
    ax.plot(x, y, 's', color=col, markersize=32)
    ax.text(x - 0.20, y - 0.08, lab, color='#FFFFFF', fontweight='bold', fontsize=6.8)
ax.set_xlim(0, 1); ax.set_ylim(0, 1)
plt.tight_layout(); fig.savefig(os.path.join(d8, "chart03_entry_exit_barriers_matrix.png")); plt.close(fig)

fig, ax = plt.subplots(figsize=(6.0, 4.0), dpi=300)
set_spine(ax, "掠夺性定价 (Predatory Pricing) 阶段损益机理", xlabel="博弈发展阶段", ylabel="掠夺在位者单期利润")
stages = ['正常竞争期', '掠夺打压期 (P<AVC)', '对手退出垄断期 (P>>AC)']
prof_p = [5, -4, 12]
ax.bar(stages, prof_p, color=[C_BLUE, C_RED, C_GREEN], width=0.45)
ax.axhline(0, color='#333333', lw=1.2)
ax.text(0.7, -3.0, '牺牲短期亏损\n驱逐进入者', fontsize=7.0, color='#FFFFFF', fontweight='bold')
ax.text(1.7, 8.0, '长期独占市场\n攫取垄断暴利', fontsize=7.0, color='#FFFFFF', fontweight='bold')
ax.set_ylim(-6, 15)
plt.tight_layout(); fig.savefig(os.path.join(d8, "chart04_predatory_pricing_game.png")); plt.close(fig)

# CH 09: Network and Standards
d9 = os.path.join(out_base, "ch09")
fig, ax = plt.subplots(figsize=(6.0, 4.0), dpi=300)
set_spine(ax, "网络外部性与临界容量 (Critical Mass) 突破", xlabel="预期用户规模 n", ylabel="消费者支付意愿与价格")
n = np.linspace(0, 10, 100)
p_curve = 1.8*n - 0.2*n**2
ax.plot(n, p_curve, color=C_BLUE, lw=2.5, label='需求价格曲线 P(n)')
ax.axhline(2.5, color=C_RED, lw=1.8, ls='--', label='市场供给价格 P0')
# 交点
ax.plot(1.65, 2.5, 'o', color=C_GOLD, markersize=8)
ax.plot(7.35, 2.5, 'o', color=C_GREEN, markersize=8)
ax.text(1.8, 3.2, '临界容量 (Critical Mass)\n低于此规模萎缩消亡\n突破后爆发自维持增长！', fontsize=7.0, color=C_RED, fontweight='bold')
ax.set_xlim(0, 10); ax.set_ylim(0, 5); ax.legend(fontsize=7.0, loc='upper right')
plt.tight_layout(); fig.savefig(os.path.join(d9, "chart01_metcalfe_critical_mass.png")); plt.close(fig)

fig, ax = plt.subplots(figsize=(6.0, 4.0), dpi=300)
ax.set_facecolor(C_BG); ax.axis('off')
ax.set_title("双边平台交叉网络外部性与倾斜定价架构", fontsize=10.0, fontweight='bold', color=C_NAVY, pad=8)
ax.plot(0.5, 0.5, 's', color=C_NAVY, markersize=24)
ax.text(0.43, 0.485, '双边平台企业\n(撮合/算法/规则)', color='#FFFFFF', fontweight='bold', fontsize=7.5)
ax.plot(0.18, 0.5, 'o', color=C_BLUE, markersize=16)
ax.text(0.10, 0.485, '用户端 (补贴边)\n免费甚至补贴', color='#FFFFFF', fontweight='bold', fontsize=6.8)
ax.plot(0.82, 0.5, 'o', color=C_GREEN, markersize=16)
ax.text(0.74, 0.485, '商户端 (盈利边)\n抽取高额抽成', color='#FFFFFF', fontweight='bold', fontsize=6.8)
ax.annotate('', xy=(0.42, 0.55), xytext=(0.26, 0.55), arrowprops=dict(arrowstyle="->", lw=2, color=C_BLUE))
ax.annotate('', xy=(0.74, 0.55), xytext=(0.58, 0.55), arrowprops=dict(arrowstyle="->", lw=2, color=C_GREEN))
ax.text(0.15, 0.15, '【交叉网络效应】单边规模增长直接提升另一边效用；补贴价格弹性大的一边，向弹性小的一边收费。', fontsize=7.0, color=C_NAVY, bbox=dict(boxstyle='round,pad=0.3', facecolor='#EAEDED', edgecolor=C_NAVY))
ax.set_xlim(0, 1); ax.set_ylim(0, 1)
plt.tight_layout(); fig.savefig(os.path.join(d9, "chart02_two_sided_platforms_network.png")); plt.close(fig)

fig, ax = plt.subplots(figsize=(6.0, 4.0), dpi=300)
set_spine(ax, "路径依赖与标准锁定效应 (QWERTY 键盘案例)", xlabel="时间 / 技术演化", ylabel="技术采纳率 (%)")
t = np.linspace(0, 10, 100)
ax.plot(t, 100 / (1 + np.exp(-1.2*(t-3))), color=C_RED, lw=2.5, label='早期先发标准 (QWERTY): 锁定市场')
ax.plot(t, 20 / (1 + np.exp(-0.8*(t-3))), color=C_GRAY, ls='--', lw=2.0, label='更优替代技术 (Dvorak): 遭网络锁定压制')
ax.text(4.0, 45, '转换成本与网络效应\n形成强锁定 (Lock-in)', fontsize=7.5, color=C_RED, fontweight='bold')
ax.set_xlim(0, 10); ax.set_ylim(0, 105); ax.legend(fontsize=7.0, loc='upper left')
plt.tight_layout(); fig.savefig(os.path.join(d9, "chart03_standard_lock_in_qwerty.png")); plt.close(fig)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.6, 3.8), dpi=300)
fig.patch.set_facecolor(C_BG)
set_spine(ax1, "封闭生态 (如 iOS 模式)", xlabel="", ylabel="")
ax1.bar(['严格闭源\n硬件与软件一体化'], [90], color=C_NAVY, width=0.4)
ax1.text(-0.25, 45, '高体验控制力\n高溢价抽成', fontsize=7.0, color='#FFFFFF', fontweight='bold')
ax1.set_ylim(0, 100)
set_spine(ax2, "开放生态 (如 Android 模式)", xlabel="", ylabel="")
ax2.bar(['开源开放\n多硬件厂商加盟'], [95], color=C_GREEN, width=0.4)
ax2.text(-0.25, 45, '快速占领规模\n服务变现', fontsize=7.0, color='#FFFFFF', fontweight='bold')
ax2.set_ylim(0, 100)
plt.tight_layout(); fig.savefig(os.path.join(d9, "chart04_compatibility_open_closed.png")); plt.close(fig)

# CH 10: Antitrust and Regulation
d10 = os.path.join(out_base, "ch10")
fig, ax = plt.subplots(figsize=(6.0, 4.0), dpi=300)
set_spine(ax, "威廉姆森横向并购反垄断权衡模型 (Williamson Trade-off)", xlabel="产量 Q", ylabel="价格 / 成本 P, MC")
q = np.linspace(0, 10, 100)
ax.plot(q, 10 - q, color=C_NAVY, lw=2.0, label='需求 D')
ax.axhline(6.0, color=C_RED, lw=1.5, ls='--', label='并购后价格 P1')
ax.axhline(4.0, color=C_GRAY, lw=1.2, label='并购前竞争价格 P0=MC0')
ax.axhline(2.5, color=C_GREEN, lw=1.5, label='并购后节约成本 MC1')
# 损失 A2 vs 收益 A1
ax.fill_between([4, 6], [4, 4], [6, 4], color='#FADBD8', alpha=0.7, label='死重损失 A2 (价格上涨)')
ax.fill_between([0, 4], [2.5, 2.5], [4, 4], color='#D5F5E3', alpha=0.7, label='生产效率增益 A1 (成本降低)')
ax.text(1.0, 3.2, '效率增益 A1\n(规模经济协同)', fontsize=7.0, color=C_GREEN, fontweight='bold')
ax.text(4.5, 4.8, '死重损失 A2', fontsize=7.0, color=C_RED, fontweight='bold')
ax.set_xlim(0, 9); ax.set_ylim(0, 11); ax.legend(fontsize=6.5, loc='upper right')
plt.tight_layout(); fig.savefig(os.path.join(d10, "chart01_horizontal_merger_efficiency.png")); plt.close(fig)

fig, ax = plt.subplots(figsize=(6.0, 4.0), dpi=300)
set_spine(ax, "自然垄断价格管制模式对比 (MC vs AC 定价)", xlabel="产量 Q", ylabel="价格 / 成本")
q = np.linspace(1, 10, 100)
lac = 2 + 10 / q
mc = np.full_like(q, 2.0)
ax.plot(q, 10 - 0.8*q, color=C_NAVY, lw=2.0, label='市场需求 D')
ax.plot(q, lac, color=C_RED, lw=2.0, label='平均成本 LAC (持续递减)')
ax.plot(q, mc, color=C_GREEN, lw=1.8, label='边际成本 MC = 2')
# MC 定价 Q=10, P=2 (亏损); AC 定价交点 10-0.8Q = 2+10/Q ➔ 0.8Q^2 - 8Q + 10 = 0 ➔ Q ≈ 8.54, P = 3.17
ax.plot(8.54, 3.17, 'o', color=C_GOLD, markersize=8)
ax.text(4.0, 5.0, '平均成本定价 (P = AC):\n企业收支平衡，无需财政补贴', fontsize=7.0, color=C_GOLD, fontweight='bold')
ax.set_xlim(1, 10); ax.set_ylim(0, 12); ax.legend(fontsize=6.5, loc='upper right')
plt.tight_layout(); fig.savefig(os.path.join(d10, "chart02_natural_monopoly_regulation.png")); plt.close(fig)

fig, ax = plt.subplots(figsize=(6.0, 4.0), dpi=300)
ax.set_facecolor(C_BG); ax.axis('off')
ax.set_title("现代反垄断法三大核心实体支柱", fontsize=10.0, fontweight='bold', color=C_NAVY, pad=8)
pillars = [
    (0.20, 0.55, '横向与纵向\n垄断协议\n· 固定价格卡特尔\n· 划分市场/限制产量\n· 转售价格维持 RPM', C_RED),
    (0.50, 0.55, '滥用市场\n支配地位\n· 掠夺性降价排挤\n· 拒绝交易与搭售\n· 不公平高价与差别待遇', C_GOLD),
    (0.80, 0.55, '经营者集中\n反垄断审查\n· 事前申报申报门槛\n· 横向/纵向/混合并购\n· 附加限制性条件批准', C_BLUE)
]
for x, y, lab, col in pillars:
    ax.plot(x, y, 's', color=col, markersize=28)
    ax.text(x - 0.12, y - 0.08, lab, color='#FFFFFF', fontweight='bold', fontsize=6.8)
ax.set_xlim(0, 1); ax.set_ylim(0, 1)
plt.tight_layout(); fig.savefig(os.path.join(d10, "chart03_antitrust_legal_framework.png")); plt.close(fig)

fig, ax = plt.subplots(figsize=(6.0, 4.0), dpi=300)
set_spine(ax, "最高限价管制 (Price-Cap Regulation: RPI - X)", xlabel="管制考核年份 t", ylabel="允许调价上限 (%)")
yrs = np.arange(1, 6)
rpi = np.array([3.0, 3.5, 2.8, 3.2, 3.0])
x_eff = np.full(5, 2.0)
cap = rpi - x_eff
ax.bar(yrs - 0.15, rpi, width=0.3, label='零售物价指数 RPI (通胀率)', color=C_GRAY)
ax.bar(yrs + 0.15, cap, width=0.3, label='允许调价上限 P_cap = RPI - X', color=C_GREEN)
ax.text(1.2, 4.0, '【RPI - X 激励机制】\n企业若通过技术革新使生产率提升超过 X，\n超额节约成本全部留存为企业利润！', fontsize=7.0, color=C_NAVY, bbox=dict(boxstyle='round,pad=0.3', facecolor='#EAEDED', edgecolor=C_NAVY))
ax.set_xticks(yrs); ax.set_xticklabels([f'第{y}年' for y in yrs], fontsize=7.5)
ax.set_ylim(0, 5.0); ax.legend(fontsize=6.5, loc='upper right')
plt.tight_layout(); fig.savefig(os.path.join(d10, "chart04_price_cap_incentive_regulation.png")); plt.close(fig)

print("All diagrams for Chapters 2 through 10 generated successfully!")

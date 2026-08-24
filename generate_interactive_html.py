import sys

html_content = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>《生态文明和生态安全：人与自然共生演化理论》全书4层思维导图</title>
    <style>
        body { font-family: 'Microsoft YaHei', sans-serif; background-color: #f8fafc; color: #1e293b; margin: 0; padding: 20px; }
        .header { text-align: center; margin-bottom: 25px; padding: 20px; background: #fff; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }
        .header h1 { color: #1f4e79; margin: 0 0 10px 0; font-size: 24px; }
        .header p { color: #64748b; margin: 0; font-size: 14px; }
        .tree { background: #fff; padding: 30px; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }
        .tree ul { padding-left: 20px; list-style-type: none; position: relative; }
        .tree ul ul::before { content: ''; position: absolute; top: 0; bottom: 0; left: 8px; width: 2px; background: #cbd5e1; }
        .tree li { margin: 10px 0; position: relative; font-size: 15px; }
        .tree li::before { content: ''; position: absolute; top: 12px; left: -12px; width: 10px; height: 2px; background: #cbd5e1; }
        .l1 { font-weight: bold; font-size: 18px; color: #1f4e79; background: #e0f2fe; padding: 8px 14px; border-radius: 8px; display: inline-block; }
        .l2 { font-weight: bold; font-size: 16px; color: #2f5597; background: #f1f5f9; padding: 6px 12px; border-radius: 6px; display: inline-block; margin-top: 8px; }
        .l3 { font-weight: 600; font-size: 14px; color: #334155; }
        .l4 { font-size: 13.5px; color: #475569; background: #fafafa; padding: 4px 8px; border-radius: 4px; display: inline-block; border-left: 3px solid #3b82f6; }
    </style>
</head>
<body>
    <div class="header">
        <h1>《生态文明和生态安全：人与自然共生演化理论》（张智光 著）</h1>
        <p>第九届高等学校科学研究优秀成果奖（人文社会科学）获奖著作 · 全书四层系统思维导图</p>
    </div>
    <div class="tree">
        <ul>
            <li>
                <span class="l1">🌳 核心主题：《生态文明和生态安全：人与自然共生演化理论》</span>
                <ul>
                    <li>
                        <span class="l2">📘 第一篇 总论：理论基础与总体框架构筑</span>
                        <ul>
                            <li><span class="l3">第一章 生态文明与生态安全的理论基础</span>
                                <ul>
                                    <li><span class="l4">概念界定：生态文明内涵、生态安全构成、两者“共生-安全”耦合关联</span></li>
                                    <li><span class="l4">哲学与经济学基础：浅层/深层生态学、文明形态史观、循环经济与低碳经济</span></li>
                                    <li><span class="l4">生态学与生态经济学基础：共生理论、生态系统健康、资源-环境-经济复合系统</span></li>
                                    <li><span class="l4">管理学与社会学基础：生态系统服务价值评估、环境风险评价、生态文化理论</span></li>
                                </ul>
                            </li>
                            <li><span class="l3">第二章 我国生态文明与生态安全的现状与问题</span>
                                <ul>
                                    <li><span class="l4">自然环境子系统：土地、水域、大气、生物多样性与外来物种入侵</span></li>
                                    <li><span class="l4">人类活动子系统：生态经济、生态科技、生态法律制度与行为文明</span></li>
                                    <li><span class="l4">林业生态调控影响：森林对水源涵养、大气污染物沉降与重金属修复作用</span></li>
                                </ul>
                            </li>
                            <li><span class="l3">第三章 总体理论构筑：人与自然共生演化理论</span>
                                <ul>
                                    <li><span class="l4">理论起源与逻辑起点：“人-自然-经济-社会”四维共生演化理论框架</span></li>
                                    <li><span class="l4">演进模型：复合共生系统平衡与演进模型（Symbiotic Evolution Model）</span></li>
                                    <li><span class="l4">运行机制：微观-中观-宏观三级共生运行机制与协同路径</span></li>
                                </ul>
                            </li>
                            <li><span class="l3">第四章 微观-企业层共生：企业绿色科技创新</span>
                                <ul>
                                    <li><span class="l4">驱动模型：企业绿色创新的“意愿-行为-绩效”（WBP）三阶模型</span></li>
                                    <li><span class="l4">绿色响应：环境规制与市场激励双重驱动下的企业绿色响应机理</span></li>
                                    <li><span class="l4">双赢机制：企业生态效益与经济效益“双赢”（Win-Win）实现机制</span></li>
                                </ul>
                            </li>
                            <li><span class="l3">第五章 中观-供应链共生：绿色共生型供应链</span>
                                <ul>
                                    <li><span class="l4">驱动力：绿色共生型供应链内在驱动力与上下游节点协同博弈</span></li>
                                    <li><span class="l4">生态重构：物质循环与能量梯级利用的产业链生态化重构</span></li>
                                    <li><span class="l4">评价管控：共生供应链绩效评价指标体系与生态风险管控</span></li>
                                </ul>
                            </li>
                            <li><span class="l3">第六章 宏观-全社会共生：超循环经济理论与实例</span>
                                <ul>
                                    <li><span class="l4">理论模型：超循环经济（Hypercyclic Economy）自组织与正反馈理论模型</span></li>
                                    <li><span class="l4">大循环机制：社会-经济-生态三大子系统的大循环耦合机制</span></li>
                                    <li><span class="l4">实践案例：国内外超循环经济示范区典型案例与经验借鉴</span></li>
                                </ul>
                            </li>
                        </ul>
                    </li>
                    <li>
                        <span class="l2">📗 第二篇 生态文明论：概念界定、测度模型与时空演化</span>
                        <ul>
                            <li><span class="l3">第七章 生态文明国内外研究综述</span>
                                <ul>
                                    <li><span class="l4">演进脉络：从环境保护到“文明形态”研究演进脉络综述</span></li>
                                    <li><span class="l4">指标对比：国内外生态文明评价指标体系对比分析</span></li>
                                    <li><span class="l4">创新突破：现有测度方法的创新突破点与未尽议题</span></li>
                                </ul>
                            </li>
                            <li><span class="l3">第八章 生态文明观：新时代的发展观</span>
                                <ul>
                                    <li><span class="l4">核心内涵：生态文明观的核心价值观与导向演进</span></li>
                                    <li><span class="l4">两山理论：“绿水青山就是金山银山”两山转化理论逻辑</span></li>
                                    <li><span class="l4">战略定位：生态文明在国家现代化建设中的战略定位</span></li>
                                </ul>
                            </li>
                            <li><span class="l3">第九章 生态文明“阈值”与“绿值”二步测度方法</span>
                                <ul>
                                    <li><span class="l4">模型创新：“二步测度法”（Two-Step Measurement Method）创新思路与模型</span></li>
                                    <li><span class="l4">阈值判定：临界“阈值”（Threshold）判定与生态安全下限标准</span></li>
                                    <li><span class="l4">绿值量化：发展“绿值”（Green Value）综合量化与动态权重构建</span></li>
                                </ul>
                            </li>
                            <li><span class="l3">第十章 生态文明测度的 PSIR-SEM 建模</span>
                                <ul>
                                    <li><span class="l4">框架构建：PSIR（压力-状态-影响-响应）扩展框架构建</span></li>
                                    <li><span class="l4">SEM应用：结构方程模型（SEM）在潜变量量化中的应用</span></li>
                                    <li><span class="l4">方法比较：与传统熵权法/主成分分析法的优劣比较与检验</span></li>
                                </ul>
                            </li>
                            <li><span class="l3">第十一章 中国生态文明测度及其时空演化规律分析</span>
                                <ul>
                                    <li><span class="l4">测度结果：全国及 31 省域生态文明二步测度实证结果</span></li>
                                    <li><span class="l4">时空特征：时空演化特征（东中西部梯度演进与区域收敛趋势）</span></li>
                                    <li><span class="l4">阶段判定：生态文明发展阶段分类判定与政策契合度</span></li>
                                </ul>
                            </li>
                            <li><span class="l3">第十二章 林业对生态文明的贡献及其“结构微笑曲线”</span>
                                <ul>
                                    <li><span class="l4">基础地位：林业在生态文明建设中的基础与枢纽地位</span></li>
                                    <li><span class="l4">微笑曲线：林业产业链“结构微笑曲线”（Structure Smile Curve）模型</span></li>
                                    <li><span class="l4">提升路径：前端生态保育与后端生态旅游高附加值段提升路径</span></li>
                                </ul>
                            </li>
                            <li><span class="l3">第十三章 中国生态文明状况的根源回溯与对策建议</span>
                                <ul>
                                    <li><span class="l4">根源剖析：制度缺失、市场失灵与行为滞后的深层根源剖析</span></li>
                                    <li><span class="l4">三位一体：制度创新、绿色科技与全民参与三位一体对策</span></li>
                                    <li><span class="l4">路线图：面向 2035/2050 年生态文明建设路线图与政策组合拳</span></li>
                                </ul>
                            </li>
                        </ul>
                    </li>
                    <li>
                        <span class="l2">📙 第三篇 生态安全论：安全指数、空间测度与屏障构筑</span>
                        <ul>
                            <li><span class="l3">第十四章 生态安全的国内外研究综述</span>
                                <ul>
                                    <li><span class="l4">概念演变：生态安全概念演变、内涵界定与预警机制综述</span></li>
                                    <li><span class="l4">方法对比：区域与产业生态安全评价方法对比</span></li>
                                    <li><span class="l4">范式转向：生态安全研究前沿趋势与共生范式转向</span></li>
                                </ul>
                            </li>
                            <li><span class="l3">第十五章 生态安全指数的共生空间测度方法</span>
                                <ul>
                                    <li><span class="l4">维度构建：共生空间（Symbiotic Space）概念维度与几何表征</span></li>
                                    <li><span class="l4">算法设计：生态安全指数共生空间测度模型与算法设计</span></li>
                                    <li><span class="l4">协同机制：空间溢出效应与跨区域协同安全机制</span></li>
                                </ul>
                            </li>
                            <li><span class="l3">第十六章 生态安全测度的 PSIR-SEM 建模</span>
                                <ul>
                                    <li><span class="l4">潜变量设计：生态安全 PSIR-SEM 结构方程潜变量设计</span></li>
                                    <li><span class="l4">因果验证：模型路径系数拟合与安全因果链条验证</span></li>
                                    <li><span class="l4">预警触发：关键敏感因子识别与早期预警阈值触发机制</span></li>
                                </ul>
                            </li>
                            <li><span class="l3">第十七章 中国生态安全指数测度及其时空演化（以林业为例）</span>
                                <ul>
                                    <li><span class="l4">时间测算：国家与省域林业生态安全指数时间序列测算</span></li>
                                    <li><span class="l4">轨迹演进：生态安全屏障空间格局演进与区域分化轨迹</span></li>
                                    <li><span class="l4">动态调控：林业生态安全预警等级划分与动态调控</span></li>
                                </ul>
                            </li>
                            <li><span class="l3">第十八章 林业产业的生态安全性评估</span>
                                <ul>
                                    <li><span class="l4">环境负荷：木材加工与林产化工的资源环境负荷评估</span></li>
                                    <li><span class="l4">指标体系：林业产业生态安全性综合评价指标体系</span></li>
                                    <li><span class="l4">转型路径：传统林产工业的清洁生产与绿色转型路径</span></li>
                                </ul>
                            </li>
                            <li><span class="l3">第十九章 森林旅游业的生态安全性评估</span>
                                <ul>
                                    <li><span class="l4">承载力测算：森林生态旅游的环境承载力（Carrying Capacity）测算</span></li>
                                    <li><span class="l4">演化博弈：旅游开发强度与生态保护的演化博弈模型</span></li>
                                    <li><span class="l4">低碳模式：低碳森林旅游模式与生态预警控制机制</span></li>
                                </ul>
                            </li>
                            <li><span class="l3">第二十章 森林食品业的生态安全性评估</span>
                                <ul>
                                    <li><span class="l4">质量评估：森林食品产地环境质量与土壤/水质安全评估</span></li>
                                    <li><span class="l4">保障体系：“从森林到餐桌”全产业链生态安全保障体系</span></li>
                                    <li><span class="l4">品牌价值：森林有机食品品牌价值与生态产品价值实现</span></li>
                                </ul>
                            </li>
                            <li><span class="l3">第二十一章 中国生态安全屏障的构筑</span>
                                <ul>
                                    <li><span class="l4">总体布局：“三区四带”国家生态安全屏障总体战略布局</span></li>
                                    <li><span class="l4">联防联控：跨区域生态补偿与安全共建联防联控机制</span></li>
                                    <li><span class="l4">长效战略：面向未来的国家生态安全长效保障战略与制度安排</span></li>
                                </ul>
                            </li>
                        </ul>
                    </li>
                </ul>
            </li>
        </ul>
    </div>
</body>
</html>
"""

with open("张智光_生态文明和生态安全_4层思维导图.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("Successfully generated HTML mindmap!")

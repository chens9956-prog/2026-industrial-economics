---
name: academic-slide-designer
description: 顶级高校学术课件与经管类专业 PPT 视觉设计规范。当使用者说「学术课件」「经管课件」「CH 01 风格」「精美课件设计」「高校PPT制作」「卡片式排版」「经济学课件」时载入。
---

# 顶级学术课件设计规范 (Academic Slide Designer v1.0)
> 本技能源于《产业经济学》（刘志彪第3版）金牌课件 `CH 01.pptx` 的深度逆向工程与设计体系提炼。专为高校教师、研究生及经管类专业课程打造，将厚重晦涩的学术文本转化为高信息密度、高视觉质感、逻辑极度清晰的现代化课件。

---

## 🧭 一、 核心设计哲学 (Design Philosophy)

1. **容器化思维 (Containerization)**：
   - 彻底告别大段无边界纯文本与单调的列表项目符号。
   - 每一个知识点、理论模型或机制推导，必须收纳在具有微浅底色（如 `#F2F2F2`）和清晰色块顶栏的**「信息卡片容器 (Card Container)」**中。
2. **逻辑降维与分块 (Logical Deconstruction)**：
   - **L1 篇章** -> 导航顶部小标
   - **L2 章节** -> 醒目主标题（带彩色高亮底线）
   - **L3 大标题 / 模块** -> 卡片色块顶栏（深海蓝/科技蓝）
   - **L4 小标题 / 维度** -> 加粗主题色字头或双位数编号（`01`, `02`, `03`...）
   - **L5 说明正文** -> 提炼为 1-2 句短语，以「破折号」或「圆点」呈现，严格限制单行字数。
3. **极简主义留白与呼吸感 (Generous White Space)**：
   - 页面四周预留标准安全边距（左/右 0.5 in，上 0.5 in，下 0.6 in）。
   - 避免将单页撑满，单张幻灯片聚焦 1~2 个核心逻辑单元（或 2~4 个并列维度）。

---

## 🎨 二、 经典学术配色系统 (Color Palette)

课件统一基于 **16:9 宽屏（13.333" × 7.5"）** 画布构建，配色采用严谨稳重的经管学者色系：

| 色彩角色 | 16进制 Hex | RGB 数值 | 视觉用途与语义 |
| :--- | :--- | :--- | :--- |
| **主基调·深海蓝** | `#1B3A5C` | `(27, 58, 92)` | 顶部导航细条、核心卡片顶栏、第一主标题、高权威强调 |
| **辅助·科技蓝** | `#2E86C1` | `(46, 134, 193)` | 左侧基准竖线、副标题/导航标、次要分类卡顶栏、链接元素 |
| **高亮·暖琥珀金** | `#C88C1B` | `(200, 140, 27)` | 标题下方 0.04" 强调装饰线、关键概念字头、重要提示标签 |
| **正向·翡翠绿** | `#1A8C5D` | `(26, 140, 93)` | 成功案例、正向激励、收益特征、效率提升标签 |
| **警示·砖红** | `#C84B1B` | `(200, 75, 27)` | 敲竹杠风险、市场失灵、委托代理问题、制度缺陷警示 |
| **容器浅灰底** | `#F2F2F2` | `(242, 242, 242)` | 信息卡片大底色（营造卡片浮层感与结构感） |
| **强调浅蓝底** | `#D6EAF8` | `(214, 234, 248)` | 核心结论行、对比重点单元格背景 |
| **案例暖杏底** | `#FDF6E3` | `(253, 246, 227)` | 案例专栏背景底色、思考讨论题卡片背景 |
| **正文暗炭灰** | `#2C2C2C` | `(44, 44, 44)` | 正文文字（避免纯黑 `#000000` 造成的生硬刺眼感） |
| **次要中灰** | `#6B6B6B` | `(107, 107, 107)` | 页脚出处、页码编号、次要说明文字 |

---

## 📐 三、 字体与排版层级标准 (Typography Hierarchy)

### 1. 字体搭配铁律
- **中文字体**：优先使用 `微软雅黑 (Microsoft YaHei)` 或 `思源黑体 (Source Han Sans)` 呈现清晰现代感；在严谨学术出版场合，可选用高质量 `宋体 (SimSun)`。
- **英文字体与数字**：统一使用 `Times New Roman` 或 `Arial`，数字编号统一采用两位数补零格式（`01`, `02`, `03`...）。

### 2. 字号与属性规范

| 层级 (Level) | 建议字号 | 字重 (Weight) | 颜色 | 典型位置与坐标 (X, Y, W, H) |
| :--- | :--- | :--- | :--- | :--- |
| **L1 章节大标** | `12pt - 14pt` | 加粗 (Bold) | `#2E86C1` | 左上角 `(0.50", 0.22", 6.00", 0.35")` |
| **L2 本页核心标题** | `26pt - 30pt` | 加粗 (Bold) | `#1B3A5C` | 标题区 `(0.50", 0.55", 11.50", 0.60")` |
| **L2 装饰高亮线** | `H: 0.04"` | - | `#C88C1B` | 标题下方 `(0.50", 1.18", 1.20", 0.04")` |
| **L3 卡片模块标题** | `18pt - 20pt` | 加粗 (Bold) | `#FFFFFF` | 卡片顶栏内 `(X+0.3", Y+0.05", W-0.6", 0.50")` |
| **L4 分点项标题** | `15pt - 16pt` | 加粗 (Bold) | `#1B3A5C` / `#2E86C1` | 卡片正文区内起首行 |
| **L5 阐述正文/要点** | `13pt - 14pt` | 常规 (Normal) | `#2C2C2C` | 行距 1.2~1.3 倍，短句列表 |
| **页脚书籍信息** | `10pt` | 常规 (Normal) | `#6B6B6B` | 左下角 `(0.50", 7.00", 4.00", 0.35")` |
| **页码** | `11pt` | 常规 (Normal) | `#6B6B6B` | 右下角 `(12.30", 7.00", 0.80", 0.35")` |

---

## 🏛️ 四、 8 大核心母版版式积木 (8 Layout Archetypes)

在规划一章完整的学术课件（20~30 页）时，应灵活穿插以下 8 种标准版式：

### 1. 全幅主封面 (Hero Chapter Cover)
- **用途**：课程总起、章节开篇。
- **构思**：左侧/居中大字号章名（36-40pt），右上角带有简洁章节徽标（如 `CH 01`），下方附带主讲教材出处与本章 4~5 个核心要点预览清单。

### 2. 本章概览与逻辑框架 (Overview Framework Grid)
- **用途**：展示全章 3~4 节的逻辑推进链条。
- **构思**：采用水平 4 列卡片矩阵（`01 企业的本质` -> `02 企业的目标` -> `03 企业的结构` -> `04 国有企业`），底部附带一根「核心逻辑推演链」贯穿条。

### 3. 极简节段导航过渡页 (Minimalist Section Bridge)
- **用途**：进入新一节（Section）时的视觉缓冲。
- **构思**：大字号 `第一节`（深蓝） + 节名称（32pt） + 底部副标题列出本节 3 个核心理论关键词。

### 4. 双栏对比卡片 (Side-by-Side Dual Cards)
- **用途**：两种对立机制/理论的横向对比（如：市场 vs 企业，前向一体化 vs 后向一体化）。
- **构思**：
  - 左卡（深蓝顶栏 `#1B3A5C`，宽 5.8"）：展示维度 A 的特征与适用场景。
  - 右卡（科技蓝顶栏 `#2E86C1`，宽 5.8"）：展示维度 B 的特征与适用场景。
  - 底部可加通栏结论条（高亮强调两者的替代与互补边界）。

### 5. 四列编号指标矩阵 (4-Column Numbered Matrix)
- **用途**：阐述四大成因、四种类型、四个维度（如：交易成本的 4 种类型）。
- **构思**：
  - 水平排列 4 个独立小卡片（每张宽 2.8"~2.9"）。
  - 顶部配大号圆角数字徽章（`01`, `02`, `03`, `04`）。
  - 中间为概念名称（16pt 粗体），下方为 2~3 行精炼解释。

### 6. 机制推导与分类卡 (Mechanisms & Taxonomy Breakdown)
- **用途**：深入剖析某一理论的底层驱动因素（如：人的因素 vs 交易因素）。
- **构思**：左右不等宽或等宽卡片，内部嵌套二级微标签（如：`有限理性`、`机会主义`），使用破折号并列推导逻辑。

### 7. 经典案例专栏时间轴 (Case Study Timeline)
- **用途**：教科书配套 Case Study（如：通用汽车收购费雪车身公司案例）。
- **构思**：
  - 顶部大卡片标题标注 `案例专栏 1-1`（杏黄色或特色底色）。
  - 横向或纵向 4~5 个演化阶段节点（`1919年前` -> `1919年` -> `1919-1924` -> `1925-1926` -> `1926年收购`）。
  - 底部设独立的「案例启示与学术理论映射」总结框。

### 8. 本章小结与思考讨论 (Summary & Seminar Discussion)
- **用途**：课程尾声复盘与考研/课后讨论题。
- **构思**：左侧为本章核心结论思维导图式提炼，右侧为 2~3 道启发式思考题卡片。

---

## 💻 五、 Python-PPTX 自动化构建模版 (Code Implementation Template)

以下为标准 Python-pptx 实现模版，可直接引入脚本中实现像素级复刻：

```python
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.xmlchemy import OxmlElement

# 1. 调色板常量
COLOR_DARK_BLUE = RGBColor(27, 58, 92)     # #1B3A5C
COLOR_MED_BLUE  = RGBColor(46, 134, 193)    # #2E86C1
COLOR_AMBER     = RGBColor(200, 140, 27)    # #C88C1B
COLOR_LIGHT_GREY= RGBColor(242, 242, 242)   # #F2F2F2
COLOR_TEXT_DARK = RGBColor(44, 44, 44)      # #2C2C2C
COLOR_TEXT_MUTED= RGBColor(107, 107, 107)   # #6B6B6B
COLOR_WHITE     = RGBColor(255, 255, 255)

class AcademicSlideDeck:
    def __init__(self):
        self.prs = Presentation()
        self.prs.slide_width = Inches(13.333)
        self.prs.slide_height = Inches(7.5)
        self.blank_layout = self.prs.slide_layouts[6]
        self.slide_count = 0

    def _apply_font(self, run, size_pt, bold=False, color=None, east_asia_font="SimSun"):
        run.font.name = 'Times New Roman'
        run.font.size = Pt(size_pt)
        run.font.bold = bold
        if color:
            run.font.color.rgb = color
        rPr = run._r.get_or_add_rPr()
        ea = OxmlElement('a:ea')
        ea.set('typeface', east_asia_font)
        rPr.insert(0, ea)

    def _add_p(self, text_frame, text, size_pt, bold=False, color=None, align=None, is_first=False):
        p = text_frame.paragraphs[0] if is_first else text_frame.add_paragraph()
        if align:
            p.alignment = align
        run = p.add_run()
        run.text = text
        self._apply_font(run, size_pt, bold, color)
        return p

    def create_base_slide(self, l1_chapter, l2_section):
        """生成标准页面骨架：顶线、左基准线、L1/L2标题、琥珀金高亮线、页脚及页码"""
        self.slide_count += 1
        slide = self.prs.slides.add_slide(self.blank_layout)

        # 顶部深蓝标线
        top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(0.08))
        top_bar.fill.solid(); top_bar.fill.fore_color.rgb = COLOR_DARK_BLUE; top_bar.line.fill.background()

        # 左侧科技蓝基准线
        left_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, Inches(0.08), Inches(7.42))
        left_bar.fill.solid(); left_bar.fill.fore_color.rgb = COLOR_MED_BLUE; left_bar.line.fill.background()

        # L1 章节标
        tx_l1 = slide.shapes.add_textbox(Inches(0.50), Inches(0.22), Inches(6.00), Inches(0.35))
        self._add_p(tx_l1.text_frame, l1_chapter, 12, True, COLOR_MED_BLUE, is_first=True)

        # L2 核心标题
        tx_l2 = slide.shapes.add_textbox(Inches(0.50), Inches(0.55), Inches(11.50), Inches(0.60))
        self._add_p(tx_l2.text_frame, l2_section, 26, True, COLOR_DARK_BLUE, is_first=True)

        # 琥珀金高亮线
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.50), Inches(1.18), Inches(1.20), Inches(0.04))
        line.fill.solid(); line.fill.fore_color.rgb = COLOR_AMBER; line.line.fill.background()

        # 页脚
        tx_foot = slide.shapes.add_textbox(Inches(0.50), Inches(7.00), Inches(5.00), Inches(0.35))
        self._add_p(tx_foot.text_frame, "产业经济学 · 刘志彪（第3版）", 10, False, COLOR_TEXT_MUTED, is_first=True)

        # 页码
        tx_num = slide.shapes.add_textbox(Inches(12.30), Inches(7.00), Inches(0.80), Inches(0.35))
        self._add_p(tx_num.text_frame, str(self.slide_count), 11, False, COLOR_TEXT_MUTED, is_first=True)

        return slide

    def add_dual_cards(self, slide, left_title, left_points, right_title, right_points):
        """渲染双栏对比卡片"""
        cards = [
            (Inches(0.50), Inches(5.80), COLOR_DARK_BLUE, left_title, left_points),
            (Inches(6.60), Inches(6.20), COLOR_MED_BLUE, right_title, right_points)
        ]
        for left_x, width, h_color, title, points in cards:
            # 浅灰底容器
            bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left_x, Inches(1.50), width, Inches(5.30))
            bg.fill.solid(); bg.fill.fore_color.rgb = COLOR_LIGHT_GREY; bg.line.fill.background()

            # 色块标题顶栏
            h_bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left_x, Inches(1.50), width, Inches(0.60))
            h_bg.fill.solid(); h_bg.fill.fore_color.rgb = h_color; h_bg.line.fill.background()

            # 顶栏文字
            tx_h = slide.shapes.add_textbox(left_x + Inches(0.30), Inches(1.55), width - Inches(0.60), Inches(0.50))
            self._add_p(tx_h.text_frame, title, 18, True, COLOR_WHITE, is_first=True)

            # 内容文字
            tx_c = slide.shapes.add_textbox(left_x + Inches(0.30), Inches(2.25), width - Inches(0.60), Inches(4.45))
            tf = tx_c.text_frame
            tf.word_wrap = True
            for i, pt in enumerate(points):
                self._add_p(tf, f"• {pt}", 13, False, COLOR_TEXT_DARK, is_first=(i == 0))
```

---

## ⚡ 六、 文本转化实战范例 (Transformation Walkthrough)

### 原始教材段落（晦涩难读）：
> 科斯在1937年发表的《企业的性质》中探讨了企业为什么存在的问题。在新古典微观经济学中，企业被视为一个黑箱或简单的生产函数，并不探讨企业的内部结构。然而，科斯指出，使用市场的价格机制是有成本的，即交易成本。交易成本包括价格发现成本、谈判与签约成本、执行合约成本以及不确定性风险。企业通过管理指令替代市场交易，能够显著降低这些交易成本。

### 学术卡片化提炼（契合 Slide 04 & 05 设计）：
- **页面标题**：`第一节 企业的本质` -> `交易成本与企业的性质`
- **左卡（理论基石）**：
  - 顶栏：`科斯定理（Coase, 1937）`
  - 要点 1：`企业本质上是一种资源配置方式`
  - 要点 2：`企业内部通过管理者「看得见的手」配置资源`
  - 要点 3：`两者并存根源：使用价格机制存在不可忽略的交易成本`
- **右卡（市场 vs 企业）**：
  - 顶栏：`资源配置方式对比`
  - 对比 1：`市场：价格信号协调 ｜ 适合简单重复交易`
  - 对比 2：`企业：管理指令协调 ｜ 适合复杂与资产专用性投资`
- **底部总结条**：
  - `企业通过内部交易取代市场交易降低成本，但规模扩张亦受内部组织成本制约。`

---

## 🛠️ 七、 课件生成质量自检清单 (Self-Audit Checklist)

每次执行课件输出或评审时，必须自检以下 6 项指标：
1. [ ] **是否全幅宽屏**：确认设定为 16:9 (`13.333" × 7.5"`)。
2. [ ] **色系是否纯正**：主深蓝 `#1B3A5C`、辅科技蓝 `#2E86C1`、高亮琥珀金 `#C88C1B`、底浅灰 `#F2F2F2`。
3. [ ] **容器卡片化率**：页面主体是否 100% 采用卡片/网格封装，杜绝任何无边际漂浮文字。
4. [ ] **字号层级清晰**：大标题 26pt+、模块标 18pt+、分点 14-16pt、正文 12-14pt。
5. [ ] **双语字体合规**：中文字符统一为黑体/宋体，英文字母与数字统一为 Times New Roman/Arial。
6. [ ] **分页呼吸感**：单页正文行数不超过 10 行，避免文字重叠或拥挤。

# 2026产业经济学（专案蓝图）

> 本档为跨 Agent 通用的专案蓝图（AGENTS.md 开放标准）。任何 Agent 的每个 session 都应先读本档＋`handoff.md`。

## 专案简介
本专案为“2026产业经济学”相关的课程建设与教学资料整理，包含教学大纲、课件讲义、核心参考指南及考研题库，同时包含随堂测试系统与萌宠科学计算器等衍生教学工具。

## 关键时程
- (暂无关键时程，有需要时可补充)

## 目标与路线图
- [x] 阶段一：梳理并完善各章节教学资料与课件 (已完成1-10章单页PDF要点、第1章4层级结构试做，并完成基于 CH 01 金牌课件的 academic-slide-designer 学术课件设计规范体系)
- [x] 阶段二：集成随堂测试系统（50题/75分钟/上下双得分卡/深浅色主题/Netlify部署+原生微信小程序版）与企鹅萌宠科学计算器小程序
- [x] 阶段三：依据教材知识体系完成《产业经济学》全书 1~10 章标准高校学术课件（18~23页/章，40幅全矢量高清学术图表，讲练融合与案例融合，零双引号与纯净数学规范），全部保存于 `I:\4产业经济学\分章PDF\`

## 资料夹结构
```text
2026产业经济学/
├── 01_教学大纲与课程方案_DOCX/
├── 02_985与211名校课件讲义_PPTX/
├── 03_经典教材与核心参考指南_DOCX/
├── 04_产业经济学学术档案_PDF/
├── 05_历年考研与学术考核题库_DOCX/
├── skills/                           # 专案专属技能库 (含 academic-slide-designer, textbook-slide-maker 等)
├── ie_diagrams/                      # 产业经济学 1~10 章全量 300 DPI 矢量学术图表库
├── slide_generator_engine.py         # 金牌高校学术课件核心渲染引擎
├── safe_save_helper.py               # 安全文件写入与原子替换辅助模块
├── clasp-netlify-mcp-guide/          # 部署与配置指南
├── gem-to-agent-kit/
├── glass-calculator/                 # 高颜值科学计算器 Web 版
├── glass-calculator-wxapp/           # 企鹅萌宠科学计算器原生微信小程序包
├── industrial-economics-quiz/        # 随堂测试系统相关
├── industrial-economics-wxapp/       # 产业经济学随堂测试系统原生微信小程序包
├── online-exam-system/               # 在线随堂考试系统 Web 版（Netlify部署）
├── padlet-mcp/
├── voxcpm2-voice-cloner/             # 语音克隆工具
├── handoff.md                        # 交接状态文件
├── CHINESE_PUNCTUATION_RULE.md       # 全局字体、标点与换行符排版规范
├── execute_plan_a.py                 # 云盘垃圾与重复文件安全隔离脚本
├── scan_junk_duplicates.py           # 全盘垃圾与重复文件只读扫描脚本
├── find_docx.py                      # 全盘 Word 文档（产业经济学）检索脚本
├── generate_doc.py                   # NotebookLM 提示词中英文对照 Word 生成脚本
├── generate_executive_report.py      # AI Agent 总裁报告 Word 生成脚本
├── get_yt_chinese_antigravity.py     # YouTube 热门中文 Antigravity 2 教程检索脚本
├── notebooklm-watermark-remover/     # NotebookLM 水印粉碎器 Pro (独立 EXE 与桌面 GUI)
├── convert_svg_to_pdf.py            # SVG 思维导图转 PDF 与合并脚本
├── scan_and_clean_pdfs.py           # 扫描与清理指定格式 PDF 脚本
├── build_mindmap_structure.py        # PDF 专著目录提取与思维导图结构化脚本
├── generate_mindmap_files.py         # 专著 4 层架构 Word/Markdown 思维导图生成脚本
├── generate_interactive_html.py      # 专著 4 层交互式 HTML 思维导图网页生成脚本
├── fetch_md.py                       # 抓取 YouTube 字幕脚本
├── json_to_md_robust.py              # 强健版 JSON 转 Markdown 字幕处理脚本
└── ... (各类课件 pptx 及文档资料)
```

## 同步层级（本专案初始化至第 3 层级）

| 层级 | 平台 | 位置 | 读取时机 |
|------|------|------|---------|
| L1 | 本地（GDrive） | `AGENTS.md`＋`handoff.md` | 每个 session |
| L2 | GitHub | https://github.com/chens9956-prog/2026-industrial-economics | 指定时 |
| L3 | Obsidian | 2026产业经济学/专案工作流程.md | 有需要时 |

## 工作约定
- 任何 Agent、任何电脑：**开工先读 `handoff.md`，收工必更新 `handoff.md`**
- 修改共用档案前先读最新内容，避免覆盖其他 Agent 的变更
- **全局语言规范（强制执行）**：所有回复、交互讯息、Commit Message、文档与课件生成统一且严格使用**中文简体 (Simplified Chinese)**。
- **字体与标点规范（强制执行）**：所有导出的文档及文字生成中，中文字体统一使用**宋体 (SimSun)**或**微软雅黑 (Microsoft YaHei)**，英文与数字统一使用 **Times New Roman (新罗马字体)**；中文回复中的所有引号必须严格使用全角中文弯双引号“与”（嵌套使用中文单引号‘与’），中文冒号：、逗号，、句号。、顿号、等标点亦统一使用全角中文标点（代码与技术指令除外）。**特别例外：文末参考文献（References）的标点符号严格使用学术规范中的半角/英文标点。**
- **换行符规范（强制执行）**：Word 文档生成与排版中，段落换行统一使用**硬回车 (Paragraph Break ↵)**，严禁混用向下箭头的软回车 (Line Break ↓ / 手动换行符)。
- 修改前先确认计画，优先保留原有资料结构

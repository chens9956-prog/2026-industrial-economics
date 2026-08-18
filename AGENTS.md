# 2026产业经济学（专案蓝图）

> 本档为跨 Agent 通用的专案蓝图（AGENTS.md 开放标准）。任何 Agent 的每个 session 都应先读本档＋`handoff.md`。

## 专案简介
本专案为“2026产业经济学”相关的课程建设与教学资料整理，包含教学大纲、课件讲义、核心参考指南及考研题库，同时包含随堂测试系统与萌宠科学计算器等衍生教学工具。

## 关键时程
- (暂无关键时程，有需要时可补充)

## 目标与路线图
- [x] 阶段一：梳理并完善各章节教学资料与课件 (已完成1-10章单页PDF要点与第1章4层级结构课件试做)
- [x] 阶段二：集成随堂测试系统（50题/75分钟/上下双得分卡/深浅色主题/Netlify部署+原生微信小程序版）与企鹅萌宠科学计算器小程序

## 资料夹结构
```text
2026产业经济学/
├── 01_教学大纲与课程方案_DOCX/
├── 02_985与211名校课件讲义_PPTX/
├── 03_经典教材与核心参考指南_DOCX/
├── 04_产业经济学学术档案_PDF/
├── 05_历年考研与学术考核题库_DOCX/
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
- 所有回应与文件使用繁体中文（但根据用户偏好全局使用简体中文回复）
- 修改前先确认计画，优先保留原有资料结构

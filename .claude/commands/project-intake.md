---
description: 采集项目画像 —— 生成 .harness/docs/PROJECT.md 并消除 CLAUDE.md 初始化横幅
---

# Project-Intake 项目画像采集

走 `project-intake` skill 的 6 步流程：

读 README → 扫目录 → 读构建配置 → 起草 `.harness/docs/PROJECT.md`（Proposed）→ 改写 CLAUDE.md（概述真实化 + 删初始化横幅）→ 人工校对转 Accepted。

> 触发时机：注入后首次会话（CLAUDE.md 带横幅时强制）。

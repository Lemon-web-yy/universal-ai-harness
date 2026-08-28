---
description: 落地 Harness 治理结构 —— 新项目注入或新模块孵化
---

# Bootstrap 治理落地

把 Harness 治理结构落到目标工程，按上下文二选一。

## A. 新项目注入（空目录 / 全新工程）

在工作区根目录（含 `universal-ai-harness/harness_installer.py`）执行：

```bash
python universal-ai-harness/harness_installer.py --target <目标路径> --profile single|multi [--name 项目名]
```

- `single`：单模块自治（designer / reviewer / builder 三角色）
- `multi`：多模块集成（五角色 + cross-module-change 协同）
- 注入后改写生成的 `CLAUDE.md` 项目概述 + 目录结构 + 编译命令
- 收尾：`python tools/audit_harness.py`

## B. 新模块落地（已有项目内新增模块）

走 `harness-setup` skill 的 9 步流程：

选模板 → 复制改名 → 改写 CLAUDE.md → 改写 core-beliefs / ARCHITECTURE → 落地 design-docs → 写 progress → 定制三角色 → 更新根级引用。

> 嵌入式组合用法：先 `extract_kit.py` 提代码骨架，再注入治理框架。

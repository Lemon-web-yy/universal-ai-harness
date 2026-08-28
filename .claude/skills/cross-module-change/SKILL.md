---
name: cross-module-change
description: "Orchestrates the cross-module workflow for changes spanning 2+ modules. Use this whenever a user asks to implement/fix/refactor something that touches multiple modules — dispatches Coordinator (contract writing + sub-agent dispatch + closing) and Architect-Reviewer (architecture review) agents, writes contract archive before coding, runs compile + integration + on-target verification. Even if the user just says 'add cross-module X' or 'fix protocol Y' without mentioning the workflow, use this skill to ensure cross-module contracts are documented before coding."
---

# Cross-Module Change Workflow（跨模块变更编排）

编排跨模块变更流程：契约先行 → 并行派发 → 架构审核 → 收尾归档。确保跨模块需求在编码前落档契约，各端并行实现后经架构审核收尾。

## When to Use

**触发条件** — 需求涉及 2+ 模块时：

- 跨模块接口变更（消息格式 / 数据结构 / 调用约定语义）
- 跨模块功能集成（数据流穿通多端）
- 用户说"跨模块 X" / "fix protocol Y" / "add cross-module X"

**不触发**：
- 单模块内部需求 → 模块内 Designer → Reviewer → Builder 流程
- 新模块 harness 落地 → harness-setup skill

**判断方法：** 需求是否涉及多个模块目录 + 是否需要接口同步。是 → 先做 L0-L3 评级（见 `contracts/workflows/cross-module-change.md`），L1 及以上走本 skill。

## 分步流程

### L1 — 契约同步（3 步）

1. Coordinator 写 `contracts/NNN_*.md`（5 章节）
2. 用户审核契约（spec review gate）
3. 各模块按需 Read 契约 → 各自走 L0 流程实现

### L2/L3 — 协调/统一编排（五步）

1. **定契约**：派发 Coordinator 写契约档案（此时不写代码）
2. **用户 spec review gate（硬停止）**：契约是架构决策，agent 不能替用户做——用户不点头不往下走
3. **并行派发**：按契约派发 Builder 子 agent（仅列实际参与者，prompt 给路径不给全文）
4. **架构审核**：派发 Architect-Reviewer（六维审核，P0 必修）
5. **收尾归档**：三层验证 + 更新索引 + `tools/audit_harness.py` 核对

## 关键决策

### 1. L0-L3 评级决定流程重量

能 L0 不 L1，能 L1 不 L2，能 L2 不 L3。联系强度 = 涉及模块数 + 是否接口同步。

### 2. 用户 spec review gate 硬停止

契约写完必须停下来给用户审。契约是架构决策，用户不点头不派发子 agent。

**为什么：** 契约决定"做什么、各端边界、不做什么"，这些是用户决策域，agent 替用户拍板会埋下返工。

### 3. 子 agent 按需列 + prompt 给路径

只列实际参与的模块（不默认列全）；prompt 给契约路径，要求子 agent 自行 Read。

**为什么：** 多拉一个模块多一份风险面；粘贴全文引入版本不一致。

### 4. 单端先行合法

契约可按接口边界分段覆盖，先打通一端另一端跟进。

## Key Discipline

### 1. 契约先行，先档案后代码

**为什么：** 各端对接口理解不一致，实现后才发现接口歧义的返工成本远超先定契约的成本。

### 2. 架构审核 P0 必修

Architect-Reviewer 的 P0 问题必须修复后才能收尾，P1/P2 可延后。

**为什么：** 边界/命名/重复这些问题在收尾前修复成本最低，拖到后期变成系统性债。

### 3. 收尾必跑索引自检

`python tools/audit_harness.py` 确认契约索引与实体一致。

**为什么：** 索引漂移让后续 agent 按索引导航扑空。

## Reference Files

| 读取什么 | 从哪读 |
|----------|--------|
| L0-L3 评级与流程 | `contracts/workflows/cross-module-change.md` |
| 契约格式 | `contracts/_template.md` |
| 根级核心规则 | `docs/core-beliefs.md` |
| 角色定义 | `.claude/agents/coordinator.md`、`.claude/agents/architect-reviewer.md` |
| 经验教训（编号引用） | `contracts/workflows/cross-module-change.md` 经验教训区 |

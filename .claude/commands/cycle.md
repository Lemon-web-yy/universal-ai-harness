---
description: 对一条需求执行完整开发闭环 —— 设计 → 审核 → 实现 → 验证
---

# Cycle 开发闭环

对一条需求执行完整开发闭环。先评级，再走对应流程。

## 0. L0-L3 评级

判定需求联系强度：单模块内部 → L0；涉及 2+ 模块 → L1/L2/L3（详见 `docs/core-beliefs.md`）。能 L0 不 L1。

## 单模块（L0）

1. **Designer** 设计架构，写 `docs/design-docs/NNN_*.md` 草稿
2. **Reviewer** 审核（需求 + 架构 + 格式）
3. 用户确认设计
4. **Builder** 按 Scope 实现 + 本地编译/单测自检
5. **Reviewer** 架构审核（决策符合度 + core-beliefs）
6. 用户真实环境测试 → 状态转 Accepted

## 跨模块（L1-L3）

走 `cross-module-change` skill：定契约 → 用户 spec review gate → 并行派发 → 架构审核 → 收尾归档。

## 收尾

`python tools/audit_harness.py` 索引自检，确认契约索引与实体一致、无编号漂移。

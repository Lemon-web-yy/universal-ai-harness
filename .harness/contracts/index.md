# 契约索引 — {{PROJECT_NAME}} 跨模块契约档案

> **定位：** 跨模块契约档案（L1 发布点）的权威索引。**收尾归档前必须核对本索引与实体文件一致**（`python .harness/audit_harness.py`）。

## 档案列表

| 编号 | 标题 | 日期 | 摘要 |
|------|------|------|------|
| （空 — 第一份契约用 `.harness/contracts/_template.md` 起草，编号从 001 开始） | | | |

## 写入纪律

1. 新契约编号 = 当前最大编号 + 1（三位数字递增）
2. 文件名 `NNN_<kebab-case-english-name>.md`，起草前先读 `.harness/contracts/_template.md`
3. 状态流转：Proposed（agent 写完）→ Accepted（**用户真实环境测试后拍板**）→ Deprecated
4. 每条摘要内嵌状态回写（Accepted 后补"已 Accepted + 验证日期"）
5. 摘要一句话，详情进档案本体

## 工作流入口

- 跨模块变更流程：[workflows/cross-module-change.md](workflows/cross-module-change.md)
- 契约编写流程：根级 `.claude/skills/contract-writing/SKILL.md`

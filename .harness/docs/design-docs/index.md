# 设计档案索引 — {{PROJECT_NAME}} 模块内部决策

> **定位：** 模块内 ADR 档案的权威索引。**收尾归档前必须核对本索引与实体文件一致**（`python .harness/audit_harness.py`）。

## 档案列表

| 编号 | 标题 | 日期 | 摘要 |
|------|------|------|------|
| 001 | .harness 命名空间隔离与项目画像采集 | 2026-09-10 | 治理文件收进 `.harness/` 解决混居；新增 PROJECT.md + project-intake skill + audit P1 硬约束补齐项目画像闭环 |
| 002 | P1 欠账与一致性批量修复 | 2026-09-10 | 幽灵引用/四级名实/测试规范通用化/模板落空/后缀漂移/L 编号冲突/占位符污染/README 缺行，8 项清账 |

## 写入纪律

1. 新档案编号 = 当前最大编号 + 1（三位数字递增，与契约编号各自独立）
2. 文件名 `NNN_<kebab-case-english-name>.md`，起草前先读 `_template.md`
3. 状态流转：Proposed（agent 写完）→ Accepted（用户真实环境验证后拍板）→ Deprecated
4. Scope 必须精确到文件/函数——Builder 的执行边界
5. 摘要一句话，详情进档案本体

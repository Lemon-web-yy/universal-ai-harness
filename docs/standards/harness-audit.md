# Harness 索引自检规范

> **定位：** 补强项——源工程真实翻车案例：根级 CLAUDE.md 写"契约 001-004"实际已积累到 007，agent 按索引导航找档案扑空。本规范 + `tools/audit_harness.py` 让索引漂移在每次收尾时被机械拦截。

## 1. 检查项清单

| # | 检查项 | 判定 | 级别 |
|---|--------|------|------|
| 1 | 契约索引 vs 实体 | `contracts/index.md` 表中每个编号都有对应 `NNN_*.md` 文件；每个契约文件都在表中有行 | P0 |
| 2 | 契约编号冲突 | 无两个契约同编号 | P0 |
| 3 | ADR 索引 vs 实体 | 每个模块 `docs/design-docs/` 的 `index.md`（如有）与 `NNN_*.md` 实体一致 | P1 |
| 4 | ADR 编号连续性 | 各模块编号无跳号/重复（允许预留空洞但需 index 说明） | P2 |
| 5 | CLAUDE.md 体量 | 根级与各模块 CLAUDE.md 行数 60~120，`## ` 段数 4~12 | P1 |
| 6 | progress.md 新鲜度 | `harness/progress.md` 存在且含"下一 session"段 | P1 |
| 7 | 占位符残留 | 项目化后不应残留 `{{PROJECT_NAME}}`（模板态除外） | P2 |
| 8 | 三角色齐全 | 各模块 `.claude/agents/` 含 designer/reviewer/builder | P1 |

**级别含义：** P0 = 必须修复才能收尾；P1 = 本轮内修复；P2 = 登记 Known Issues 可延后。

## 2. 使用方法

```bash
python tools/audit_harness.py              # 审计当前目录
python tools/audit_harness.py --root path  # 审计指定项目根
python tools/audit_harness.py --strict     # P1 也视为失败（CI 用）
```

- 退出码 0 = 全过；非 0 = 存在问题（输出明细）
- **接入点：** 跨模块工作流第四步收尾必跑（core-beliefs 第 6 条）；单模块收尾也建议跑

## 3. 人工抽查项（脚本测不了的）

- [ ] CLAUDE.md 是否退化成内容仓库（内容下沉 docs/，索引只留路由）
- [ ] core-beliefs 每条规则是否还能回答"防止了哪种真实失败"
- [ ] progress.md 交接班内容是否与实际状态相符（脚本只能查存在性，查不了真实性）
- [ ] ADR 的 Scope 是否精确到文件/函数（抽查最近 3 份）

## 4. 修复流程

发现漂移 → 以**实体文件为准**修索引（不是反过来）→ 若实体本身命名违规（如非 kebab-case），修实体并同步全部引用 → 重跑脚本确认全绿 → 修复记录写入 progress.md 已知问题表。

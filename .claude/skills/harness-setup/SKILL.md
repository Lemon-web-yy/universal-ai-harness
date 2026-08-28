---
name: harness-setup
description: "Bootstraps the harness structure (docs/ + harness/ + .claude/agents/) for a new module when its source enters the project. Use this whenever a new module's source is being onboarded — copies the matching module template, writes CLAUDE.md + docs trio + design-docs template + experience-library + harness/progress.md, customizes designer/reviewer/builder agents, and updates root-level references. Even if the user just says 'set up harness for module X' or 'onboard the new module' without mentioning the template, use this skill to ensure the standard structure is followed."
---

# Harness-Setup Workflow（新模块 Harness 落地）

为新模块落地标准 Harness 三层结构（docs/ + harness/ + .claude/agents/），并更新根级引用。

## When to Use

**触发条件** — 新模块源码进入项目时：

- 新模块首次落地
- 用户说"set up harness for module X" / "onboard the new module" / "新模块落地"

**不触发**：
- 已有模块内部需求 → 模块内流程
- 跨模块变更 → cross-module-change skill

## 落地流程（9 步）

1. **选模板**：按模块形态选对应的模块模板（技术栈无关的通用结构，或项目内已有同类模块）
2. **复制改名**：复制到根级，改名为 `<Xxx_Module>`（项目命名）
3. **改写 CLAUDE.md**：项目概述 + 真实目录结构 + 硬规则按模块定制
4. **改写 docs/core-beliefs.md**（每条注"防止了什么失败"）
5. **改写 docs/ARCHITECTURE.md**（真实分层 + 数据流 + 依赖/模块映射）
6. **落地 design-docs/**：`_template.md` + 空 `index.md`
7. **写 harness/progress.md** 初始状态
8. **定制 .claude/agents/ 三角色**（模块名 + 构建方式 + 架构规则）
9. **更新根级引用**：根级 CLAUDE.md 模块概览表 + 根级 harness/progress.md 模块状态表

## 关键决策

### 1. core-beliefs 必须逐条定制，禁止直接复制

**为什么：** 直接复制模板的 core-beliefs 会导致审核变橡皮图章——规则与本模块脱节，agent 也不会认真执行。每条规则必须能回答"防止了本模块哪种真实失败"。

### 2. 选对形态模板

不同技术栈/形态的构建方式、编译验证能力、硬规则各不相同，选错模板等于从错误基线出发。

### 3. 构建登记 checklist 落地

每个模块的 CLAUDE.md 必须含"新模块登记 checklist"（构建登记点：依赖清单 / 构建脚本 / 模块注册表）。

## 验证（含量化指标）

- [ ] CLAUDE.md 行数 80~100（`wc -l`）
- [ ] CLAUDE.md 段落数 `grep -c "^## "` ≈ 8（6~9 区间）
- [ ] 无 `{{PROJECT_NAME}}` 残留：`grep -r "{{PROJECT_NAME}}" --include="*.md"` 应只在明确待定制处命中
- [ ] 三角色齐全：`.claude/agents/` 含 designer/reviewer/builder
- [ ] 根级 CLAUDE.md 模块概览表已加行
- [ ] `python tools/audit_harness.py` 通过

## Key Discipline

### 1. 先读标准再动手

读 `docs/standards/harness-template.md`（标准结构 + 文件职责清单 + 落地 checklist）。

**为什么：** 标准是单一真相源，含"该写什么/不该写什么"双向清单，跳过会漏项。

### 2. 镜像同类模块实证

落地时参考项目中同形态模块的既有文件（尤其 CLAUDE.md 结构），保持模块间一致性。

**为什么：** 同类模块结构一致，后来者切换模块零学习成本。

## Reference Files

| 读取什么 | 从哪读 |
|----------|--------|
| Harness 标准模板 | `docs/standards/harness-template.md` |
| Mock 与测试规范 | `docs/standards/mock-and-testing.md` |
| 索引自检规范 | `docs/standards/harness-audit.md` |
| 根级核心规则 | `docs/core-beliefs.md` |

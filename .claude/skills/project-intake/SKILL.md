---
name: project-intake
description: "Collects the project profile (what it is / how to run / hard constraints) into .harness/docs/PROJECT.md and rewrites the root CLAUDE.md project-context sections, removing the initialization banner. Use this whenever the root CLAUDE.md still shows the {{INTAKE_PENDING}} banner, right after harness injection, or when the user says '采集项目画像' / '项目信息补全' / 'intake'. Agent scans README / directory structure / build configs to draft PROJECT.md as Proposed; human review flips it to Accepted."
---

# Project-Intake Workflow（项目画像采集）

注入后的第一件事：把"项目是什么"从项目本体采集进治理档案，消除 CLAUDE.md 初始化横幅。

## When to Use

**触发条件**：

- 根级 CLAUDE.md 顶部存在 `{{INTAKE_PENDING}}` 横幅（每次会话必查——入口读物带横幅即初始化未完成）
- 用户说"采集画像 / 项目信息补全 / intake"

**不触发**：

- 横幅已消除且用户未要求重采 → 直接走正常需求流程
- 新模块落地 → `harness-setup` skill（模块级 CLAUDE.md 定制内含该模块信息采集）

## 采集流程（6 步）

1. **读项目自述**：README.md（及项目内既有说明文档，如有）
2. **扫目录结构**：列出根级全部目录（排除 `.git` / `.harness` / `.claude` / 依赖缓存等），逐目录看入口文件推断职责
3. **读构建配置**：按存在性读 CMakeLists.txt / package.xml / package.json / requirements.txt / pyproject.toml / go.mod / Cargo.toml / Makefile 等
4. **起草 PROJECT.md**：按 `.harness/docs/_project.md` 结构写 `.harness/docs/PROJECT.md`，状态 Proposed、日期填今日；不确定的字段标 `（待确认）`，推断内容标 `（推断）`，禁止编造
5. **改写 CLAUDE.md**：项目概述段真实化（引用 PROJECT.md）、目录结构段补项目真实目录导读、编译命令速查 / 关键约定按采集结果登记、**删除 `{{INTAKE_PENDING}}` 横幅两行**
6. **交人工校对**：请用户确认 PROJECT.md 内容 → 确认后状态转 Accepted（用户拍板，agent 不得代翻）

## 关键决策

### 1. 采集而非询问

信息优先从项目本体（README / 代码 / 构建配置）提取，仅缺失处向用户提问。**为什么：** 项目本体是单一真相源；凭空询问会把采集变成低效访谈，且易引入与代码不符的描述。

### 2. 不确定必标注

推断的内容（如从目录名猜职责）以"（推断）"标注。**为什么：** 画像是后续所有 agent 的上下文底座，错误信息会被持续放大。

### 3. 只动两处文件

本流程改动限于 `.harness/docs/PROJECT.md`（新建）与根级 `CLAUDE.md`（改写概述 / 目录 / 命令段 + 删横幅）。**为什么：** ARCHITECTURE.md 的模块边界 / 数据流属于架构设计（designer 职责），intake 不越界。

## 验证（含量化指标）

- [ ] `.harness/docs/PROJECT.md` 存在，六段齐全，行数 ≤120（`wc -l`）
- [ ] CLAUDE.md 中横幅占位符零命中（grep 不到大括号形式）
- [ ] `grep -r "PROJECT_NAME"` 仅模板文件（`_` 前缀）命中
- [ ] CLAUDE.md 行数仍在 60~120 区间
- [ ] `python .harness/audit_harness.py` 通过（横幅残留本为 P1，消除后应全绿）

## Key Discipline

### 1. 先读横幅再干活

任何会话开始，若 CLAUDE.md 带横幅，第一件事就是引导 / 执行本流程。**为什么：** 横幅是初始化未完成的机械标记（audit P1），带病运行等于在缺失项目上下文的状态下工作。

### 2. 画像是一级档案

PROJECT.md 遵循档案纪律：Proposed → Accepted 由用户翻转；后续大改走 `.harness/docs/design-docs/`。

## Reference Files

| 读取什么 | 从哪读 |
|----------|--------|
| 画像模板 | `.harness/docs/_project.md` |
| 核心规则 | `.harness/docs/core-beliefs.md` |
| CLAUDE.md 规范 | `.harness/docs/standards/harness-template.md` |

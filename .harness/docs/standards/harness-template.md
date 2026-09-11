# 模块 Harness 标准模板

> **定位：** 新模块落地 harness 或检查已有模块 harness 健康度时按此模板。
> **通用性：** 本模板与语言/技术栈无关，适用于任意模块（服务、库、前端、嵌入式等）。

## 1. 标准目录结构

```
<模块>/
├── CLAUDE.md                 # 索引（80~100 行，## 段 6~9 个）
├── docs/
│   ├── core-beliefs.md       # 核心规则（6~8 条）
│   ├── ARCHITECTURE.md       # 架构详情（分层+数据流+依赖/模块映射）
│   ├── design-docs/          # ADR 档案（决策价值，agent 热路径）
│   │   ├── _template.md      # 精简 ADR 模板
│   │   ├── index.md          # 档案索引
│   │   └── NNN_*.md          # 决策档案
│   └── experience-library/   # 经验库
│       └── lessons.md
├── .harness/progress.md       # 运行时进度（跨 session 交接班账本）
└── .claude/agents/           # 角色定义
    ├── designer.md
    ├── reviewer.md
    └── builder.md
```

## 2. 文件职责清单

| 文件 | 该写什么 | 不该写什么 |
|------|----------|------------|
| `CLAUDE.md` | 项目概述 + 目录结构 + 硬规则（精简）+ 工作流 + 构建命令 + **新模块登记 checklist** + 入口路由表 | 架构详情（归 ARCHITECTURE.md）、核心规则全文（归 core-beliefs.md）、ADR 列表（归 design-docs/index.md） |
| `.harness/docs/core-beliefs.md` | 6~8 条核心规则（每条能回答"防止了哪种真实失败"） | 架构详情、临时规则（归 experience-library） |
| `.harness/docs/ARCHITECTURE.md` | 分层 + 模块职责 + 数据流 + 依赖/通道映射 + 接口 + 构建部署 | 核心规则、运行时进度 |
| `.harness/docs/design-docs/_template.md` | 固定结构模板（元信息+Context/Decision/Consequences+Scope+状态） | 具体决策内容 |
| `.harness/docs/design-docs/index.md` | 档案列表（编号+日期+标题+一句话简介）+ 写入纪律 | 具体决策内容 |
| `.harness/docs/experience-library/lessons.md` | 踩坑教训（无编号通用原则） | 规则 |
| `.harness/progress.md` | 已完成（含验证结论）+ 待办 + 已知问题表 + 下一 session 交接班 | 决策记录（归 design-docs/） |
| `.claude/agents/*.md` | 角色"职责+不做"双向定义 | 具体决策/代码内容 |

## 3. 新模块落地步骤（checklist）

落地新模块时：

1. [ ] 选择对应形态模板（或项目内已有同类模块），复制到根级并改名为 `<Xxx_Module>`
2. [ ] 改写 `CLAUDE.md`：项目概述 + 真实目录结构 + 硬规则按模块定制（**core-beliefs 禁止直接复制，必须逐条按本模块重写**，否则审核变橡皮图章）
3. [ ] 改写 `.harness/docs/core-beliefs.md`（每条注"防止了什么失败"）
4. [ ] 改写 `.harness/docs/ARCHITECTURE.md`（真实分层+数据流+依赖映射）
5. [ ] `.harness/docs/design-docs/` 落地 `_template.md` + 空 `index.md`
6. [ ] `.harness/progress.md` 写初始状态
7. [ ] 定制 `.claude/agents/` 三角色（模块名 + 构建方式 + 架构规则）
8. [ ] 更新根级 `CLAUDE.md` 模块概览表 + 根级 `.harness/progress.md` 模块状态表
9. [ ] 运行 `python .harness/audit_harness.py` 验证
10. [ ] 验证：ls 三层目录 + grep 路径引用无残留（`grep -r "{{PROJECT_NAME}}" --include="*.md"` 应只在待定制处命中）

## 4. 命名策略

- ADR 命名：英文 kebab-case（`NNN_<kebab-case-english-name>.md`），三位数字递增（新项目从 001 起）
- 状态字段：Proposed → Accepted → Deprecated
- **Scope 必须精确到文件/函数** — Builder subagent 据此编程
- 契约编号与 ADR 编号各自独立递增，互不占用

## 5. 新模块登记 checklist（补强项）

> **背景：** 源工程痛点——多种构建体系各自手工维护文件清单，新增模块漏登记导致编译失败或文件不被编译。

新增一个模块/组件时，**必须逐项核对构建登记点**：

| 形态 | 登记点 | checklist |
|------|--------|-----------|
| 构建脚本 | 依赖清单 / 构建配置 | [ ] 模块目录已加入依赖 [ ] 搜索路径已加 [ ] 新文件落在已登记目录内 |
| 通用 | `.harness/docs/ARCHITECTURE.md` | [ ] 模块表加行 [ ] 数据流图补链路 |
| 通用 | 模块 `CLAUDE.md` | [ ] 目录结构段同步（仅当新增顶层目录） |

## 6. 工作流速查

### 单模块工作流（L0）

1. **Designer** 写 `design-docs/NNN_*.md` 草稿
2. **Reviewer** 审核设计（需求+架构+格式）
3. 用户审 spec（review gate）
4. **Builder** 按 Scope 实现 + 编译验证（无法编译标 `[未验证]`）+ 构建登记 checklist
5. **Reviewer** 审核架构（决策符合度 + core-beliefs）
6. 用户真实环境测试 → 状态 Proposed → Accepted

### 跨模块工作流（L1-L3）

见 `.harness/contracts/workflows/cross-module-change.md`。

## 7. 健康度自检

每次收尾归档前：`python .harness/audit_harness.py`（详见 `harness-audit.md`）。人工抽查项：
- CLAUDE.md 是否又变成内容仓库（行数 >110 即报警）
- core-beliefs 是否有答不上"防止什么失败"的规则（删除或降级到 experience-library）
- progress.md 的"下一 session 交接班"是否还新鲜

# 001 — .harness 命名空间隔离与项目画像采集（harness-namespace-and-project-intake）

*日期：2026-09-10*
*状态：Proposed*

> **定位：** 模块内部架构决策档案（精简 ADR）。触发：架构调整 / 接口变更。流程：先写本档案再动代码。

## Context

### 需求来源

2026-09-10 将 harness 以 multi profile 注入 `lemo_linux`（ROS 多模块工程）实测，用户反馈两个缺陷。

### 痛点

1. **目录混居**：注入使用通用目录名（`contracts/`、`docs/`、`tools/`），与目标仓库既有同名目录合流。实测 `tools/` 被混入 `audit_harness.py`（与项目 5 个工具脚本同居）；换任何已有 `docs/` 的项目会被静默覆盖。installer（`copytree(dirs_exist_ok=True)`）无任何冲突检测。
2. **项目画像缺失**：注入产物只描述治理框架自身，不描述项目。根级 CLAUDE.md 的目录树画的是注入物而非项目真实结构（误导性），构建命令为空 TODO，"补齐项目上下文"完全依赖纯人工的"注入后必做三件事"，无引导、无采集机制、无完成判定。与 `SOP.md` 自身矛盾：4.2 节明确"CLAUDE.md 作用是声明项目上下文，替代每次会话的人工说明"，5.2 节的一键实现反而丢失了这一定位（对照：Claude Code 内置 `/init` 即具备项目采集能力）。

### 约束

- **生态硬约定不可破坏**：根级 `CLAUDE.md`（Claude Code 仅自动读取根级及父目录链）与 `.claude/`（agents/skills/commands 固定检索路径）不得迁移。
- 治理机制本身（角色分离 / L0-L3 评级 / 档案纪律）不动。
- 本机（Windows）无 Python 运行时，installer 与 audit 的脚本原生可执行性无法在本机验证。

## Decision

### D1：治理文件集中收进 `.harness/` 单一命名空间（解决混居）

- 迁移：`contracts/` → `.harness/contracts/`、`docs/` → `.harness/docs/`、`harness/progress.md` → `.harness/progress.md`、`tools/audit_harness.py` → `.harness/audit_harness.py`。
- 根级新增物仅剩 `CLAUDE.md` + `.claude/`（生态必需项）。项目自身 `docs/`、`tools/`、`contracts/` 完全归项目支配。
- **不选**冲突检测+MANIFEST 方案：仍留 5 个通用名目录与项目合流，隔离不彻底。`.harness/` 目录本身即清单——卸载 = 删 `.harness/` + `.claude/` + `CLAUDE.md`，无需独立 MANIFEST（YAGNI）。
- **不选**全部收进 `.harness/`（含 CLAUDE.md/.claude）方案：破坏 Claude Code 检索约定，框架失效。
- 模板仓库自身布局同步迁移（源布局 = 注入产物布局，所见即所得；避免"模板仓库一套结构、注入产物另一套"的双重心智）。

### D2：项目画像 = `PROJECT.md` 档案 + `project-intake` skill + audit 硬约束（解决画像缺失）

- **承载位**：`.harness/docs/PROJECT.md`，模板 `_project.md`（下划线前缀，与 `contracts/_template.md` 同模式）。结构：项目定位 / 技术栈与运行环境 / 目录结构导读（项目真实目录）/ 构建与运行 / 外部依赖与接口 / 硬约束。体量红线 ≤120 行。
- **采集机制**：新增 `project-intake` skill（agent 驱动）：读目标 README → 扫真实目录 → 读构建配置 → 起草 `PROJECT.md`（状态 Proposed）→ 同步改写根级 CLAUDE.md（概述真实化、目录树替换为项目真实结构、移除横幅）→ 人工校对转 Accepted。
  - **不选** installer 内置启发式采集：跨语言可靠性差、每种构建系统一套解析器，违背 KISS/YAGNI。采集是理解型工作，归 agent（SOP 3.4"机械归脚本、智能归 agent"哲学）。
- **闭环保障**：CLAUDE.md 顶部横幅含专用占位符 `{{INTAKE_PENDING}}`（agent 每次会话必读 CLAUDE.md，必然可见）；audit 占位符检查区分等级——`{{INTAKE_PENDING}}` 残留 = **P1**（本轮内必须修复），其余占位符维持 P2。收尾必跑 audit，画像不采集完无法收尾。零新增检查机制，仅加一条分级规则。

### D3：`find_board_dirs` 注释修正（顺带，不改逻辑）

实测确认 multi/single 注入后根目录同时含 `builder.md` 与 `design-docs/`，会被计入模块数。经用户确认：**根级计入是正确语义**（根级即根治理单元，计数 1 = 根，孵化子模块后递增），逻辑不动，仅将 `audit_harness.py` 中"根级不含这两者"的过时注释改正。

## Scope（改动清单 —— Builder 的执行边界）

| 文件 | 改动类型 | 说明 |
|------|---------|------|
| `contracts/` → `.harness/contracts/` | 迁移 | 纯 `mv`（不碰 git index），内容不变 |
| `docs/` → `.harness/docs/` | 迁移 | 纯 `mv`（不碰 git index），内容不变 |
| `harness/progress.md` → `.harness/progress.md` | 迁移 | `harness/` 目录随之消失 |
| `tools/audit_harness.py` → `.harness/audit_harness.py` | 迁移+修改 | `tools/` 目录随之消失；路径逻辑见下 |
| `.harness/audit_harness.py` | 修改 | `check_contracts()`：`root/contracts` → `root/.harness/contracts`；`find_board_dirs()`：`docs/design-docs` → `.harness/docs/design-docs` + 注释修正（D3）；`check_placeholder()`：区分占位符等级（`{{INTAKE_PENDING}}` → P1，其余 → P2）；`main()`：progress 路径 `root/harness/progress.md` → `root/.harness/progress.md` |
| `harness_installer.py` | 修改 | `copy_contracts()`/`copy_docs()`：目标改 `.harness/` 下；`copy_tools()` 改为单文件复制至 `target/.harness/audit_harness.py`；`write_progress()`：目标 `target/.harness/progress.md`；`MULTI_CLAUDE_TEMPLATE`/`SINGLE_CLAUDE_TEMPLATE` 重写（路径引用、目录树改 `.harness/` 简图+项目结构待采集标记、顶部 `{{INTAKE_PENDING}}` 横幅、概述引用 PROJECT.md）；`run()` 尾部提示：第一条 `/project-intake`，audit 命令 `python .harness/audit_harness.py` |
| `.harness/docs/_project.md` | 新建 | PROJECT.md 画像模板（D2 六段结构） |
| `.claude/skills/project-intake/SKILL.md` | 新建 | 采集流程（D2 agent 执行序列） |
| `.claude/commands/project-intake.md` | 新建 | 快捷指令（跟随 bootstrap 双注册模式） |
| `.claude/skills/harness-setup/SKILL.md` | 修改 | 内部路径引用同步（`docs/`→`.harness/docs/` 等） |
| `.claude/skills/contract-writing/SKILL.md` | 修改 | `contracts/` → `.harness/contracts/` |
| `.claude/skills/cross-module-change/SKILL.md` | 修改 | 路径引用同步 |
| `.claude/commands/bootstrap.md`、`.claude/commands/cycle.md` | 修改 | audit 命令与路径引用同步 |
| `.claude/agents/{coordinator,architect-reviewer,designer,reviewer,builder}.md` | 修改 | 角色定义内路径引用同步（`docs/ARCHITECTURE.md` → `.harness/docs/ARCHITECTURE.md` 等） |
| `.harness/docs/{core-beliefs,ARCHITECTURE}.md`、`.harness/docs/standards/*.md` | 修改 | 交叉引用路径同步（迁移后全量核对） |
| `README.md`、`SOP.md`、`QUICKSTART.md` | 修改 | 注入内容清单、目录树、audit 命令、"注入后必做三件事"改为新流程（含 `/project-intake`）；SOP 6 章 Q&A"会覆盖现有文件吗"答案更新 |
| `docs/design-docs/index.md` | 修改 | 登记本档案（迁移后位于 `.harness/docs/design-docs/index.md`） |
| `.harness/progress.md`（模板仓库自身） | 修改 | 待办表登记：脚本原生回归（有 Python 环境）；已完成表登记本档案实施 |
| `extract_kit.py` | 检查 | 核对其内部引用是否涉及被迁移目录，涉及则同步（不涉及则不动） |

> 清单外一律不改。Builder 据此实现，Reviewer 据此核对。

## Consequences

### 正向

- 混居面从"5 目录 + 1 文件"缩小至 `CLAUDE.md` + `.claude/` 两个生态必需项；项目 `tools/`、`docs/` 零打扰。
- 卸载/识别平凡化：`.harness/` 目录即边界，删除即完整移除。
- 项目画像有了承载位（PROJECT.md）、生成流程（project-intake）、完成判定（audit P1）三件套闭环，补齐 SOP 4.2 与 5.2 的割裂。
- 模板仓库布局 = 注入产物布局，消除双重心智。

### 负向 / 待办

- 全部内部路径引用一次性改写（机械成本，本档案 Scope 已穷举）。
- audit 调用方式变化（`python .harness/audit_harness.py`），既有文档/习惯需同步。
- **既有已注入项目无自动迁移路径**（旧布局 → 新布局需手动迁移或重注入）——当前仅 lemo_linux 一例且将重注入，暂不做迁移脚本（YAGNI），用户确认规模化需求出现时另立档案。
- installer/audit 脚本原生可执行性本机未验证（无 Python）——待有 Python 环境跑一次真脚本回归，登记于 progress.md 待办。

## 验证

> 以下清单交由用户另行指派的执行 agent 在 lemo_linux 上执行（本档案作者不执行删除/注入操作）。

- [ ] **卸载旧注入**：删除 lemo_linux 下 `.claude/`、`CLAUDE.md`、`contracts/`、`docs/`、`harness/`、`tools/audit_harness.py`（git 备份兜底）
- [ ] **重新注入**（手动等价或真脚本）：`.harness/` 单一命名空间落位（contracts/docs/progress.md/audit_harness.py 齐全）；项目 `tools/` 无 `audit_harness.py` 混入
- [ ] **横幅存在**：根级 CLAUDE.md 顶部含 `{{INTAKE_PENDING}}` 横幅与 `/project-intake` 指引
- [ ] **采集跑通**：执行 `/project-intake` → 生成 `.harness/docs/PROJECT.md`（状态 Proposed，六段齐全，≤120 行）→ CLAUDE.md 概述/目录树真实化且横幅消除
- [ ] **audit 全绿**：采集完成后手动核对（或真脚本运行）无 P0/P1；采集完成前 `{{INTAKE_PENDING}}` 残留应报 P1
- [ ] **脚本原生回归**（待办，有 Python 环境）：`python harness_installer.py --target <沙箱> --profile multi` 与 `python .harness/audit_harness.py` 无语法/运行错误

---

**状态流转：** Proposed（agent 写完）→ Accepted（用户真实环境验证后拍板）→ Deprecated

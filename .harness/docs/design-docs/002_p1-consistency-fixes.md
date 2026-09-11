# 002 — P1 欠账与一致性批量修复（p1-consistency-fixes）

*日期：2026-09-10*
*状态：Proposed*

> **定位：** 模块内部架构决策档案（精简 ADR）。触发：ADR-001 实施后的遗留清账（既有 P1 × 6 + 新发现 × 2）。

## Context

### 需求来源

ADR-001 实施完成后盘点遗留：此前全量梳理发现的 6 项 P1 全部未处理，本次实施又新发现 2 项。用户指示"能修复的先修复"（无 Python 环境仅影响验证，不影响修复——8 项均为文档/常量层修改）。

### 痛点

8 项一致性问题，逐项见 Decision。

### 约束

- 全部为文档/清单/文本修改，不涉及可执行逻辑变更（.hpp 后缀补齐为元组字面变更，语义向后兼容）。
- 修复不得引入新概念（YAGNI）：不补建 extract_kit.py、不建模块模板目录。

## Decision

| # | 问题 | 修复 |
|---|------|------|
| 1 | 幽灵引用：`extract_kit.py` / `init_project.py` 不存在但被三处引用 | 删除全部引用：installer / audit 的 tool_scripts 名单移除这两个名字；bootstrap.md 删"嵌入式组合用法"提示行。不补建文件（YAGNI） |
| 2 | "档案四级体系"名实不符（实际两级：根级 contracts + 模块级 design-docs） | 三处改"两级体系"：core-beliefs.md §4 标题、README 特性行、installer MULTI 模板档案纪律段 |
| 3 | mock-and-testing.md 通用化不彻底（C/嵌入式视角）；builder.md "Host 编译"同源 | 多语言化表述：断言示例标注"C 示例"并补 Python/JS 等价物；`#ifdef TEST` 标注为条件编译示例；"真机"→"真实环境"；builder.md "Host 编译"→"本地构建"（2 处） |
| 4 | harness-setup 第 1 步"选模块模板"在全新项目落空 | 改为条件分支：项目内有同类模块 → 镜像之；无 → 按标准结构（harness-template.md）从零落地。"关键决策 2"同步适配 |
| 5 | 占位符后缀清单双文件漂移（installer 含 `.hpp`，audit 不含） | audit 后缀元组补 `.hpp`；两处加"须与对方同步"注释（不做跨文件 import——installer 需自包含分发，单一常量源的强收敛不可行，弱收敛 + 注释互指） |
| 6 | 两套 L 编号语义冲突：L0-L3 评级（core-beliefs）vs L1-L4 分层（ARCHITECTURE） | ARCHITECTURE.md 分层记号文字化：L4/L3/L2/L1 → 层4/层3/层2/层1（含铁律行）；mock-and-testing.md §1 架构前提里的 L3/L1 引用顺带去除（与 #3 合并处理） |
| 7 | skill 验证清单里的字面 `{{PROJECT_NAME}}` 会被注入替换，破坏指引语义 | 两处 grep 示例去掉双大括号（`grep -r "PROJECT_NAME"` 检索效果等同），改"项目名占位符"文字表述 |
| 8 | README 结构图缺 `.claude/commands/` | 目录树补一行（含 project-intake） |

> **修正记录（2026-09-10，用户澄清后）：** #2 方向修正——"四级"本意为 **L0-L3 评级**（档案纪律随评级加权：L0 → 模块 ADR；L1 → 契约发布；L2/L3 → 契约+派发+审核+收尾），非按位置分四级。core-beliefs §4 标题改为"档案体系（随 L0-L3 评级加权）"并补评级映射行；README / installer 恢复"四级"表述；位置维度的两级表格（根级/模块级）保留。

## Scope（改动清单 —— Builder 的执行边界）

| 文件 | 改动类型 | 说明 |
|------|---------|------|
| `harness_installer.py` | 修改 | L127 tool_scripts 删 2 个幽灵名；L121 TEXT_SUFFIXES 加同步注释；L250"四级体系"→"两级体系" |
| `.harness/audit_harness.py` | 修改 | L136 tool_scripts 删 2 个幽灵名；L138 后缀元组补 `.hpp` + 同步注释 |
| `.claude/commands/bootstrap.md` | 修改 | 删"嵌入式组合用法"行 |
| `README.md` | 修改 | "档案四级体系"→"两级体系"；目录树补 commands/ 行 |
| `.harness/docs/core-beliefs.md` | 修改 | §4 标题"档案四级体系"→"档案两级体系" |
| `.harness/docs/standards/mock-and-testing.md` | 修改 | §1 去层编号引用；§3 断言多语言化（CHECK 宏标注 C 示例）；§5 `#ifdef TEST` 通用化、真机→真实环境 |
| `.harness/docs/ARCHITECTURE.md` | 修改 | 分层表 L4-L1 → 层4-层1；铁律行同步 |
| `.claude/agents/builder.md` | 修改 | "Host 编译"→"本地构建"（2 处） |
| `.claude/skills/harness-setup/SKILL.md` | 修改 | 第 1 步条件分支化；"关键决策 2"适配；L51 grep 示例去大括号 |
| `.claude/skills/project-intake/SKILL.md` | 修改 | L49 grep 示例去大括号 |
| `.harness/docs/design-docs/index.md` | 修改 | 登记本档案 |

> 清单外一律不改。ADR-001 Scope 表中的 extract_kit 行属历史记录，不因 #1 修改。

## Consequences

### 正向

- 三处幽灵引用清零；名实一致（两级）；测试规范与"彻底通用化"声明相符；全新项目可走 harness-setup；后缀清单对齐；L 编号语义唯一化（L* 仅指评级）；注入后 skill 指引不再被污染；README 结构完整。

### 负向 / 待办

- 弱收敛的后缀清单仍依赖人工同步（注释互指），强收敛需 installer 支持包导入——留待 Python 环境回归时评估。
- 本档案全部改动沿用 ADR-001 的验证待办：有 Python 环境后跑一次 installer/audit 原生回归。

## 验证

- [ ] `grep -rn "extract_kit\|init_project"` 仅 ADR 档案命中（历史记录）
- [ ] `grep -rn "四级"` 零命中
- [ ] `grep -rn "{{PROJECT_NAME}}" .claude/` 零命中（占位符示例已去大括号）
- [ ] audit 与 installer 后缀清单一致（均含 `.hpp`）
- [ ] 分层记号检索 `L4|L3 业务|L2 协议|L1 基础` 零命中（ARCHITECTURE 已文字化）
- [ ] README 目录树含 commands/ 行
- [ ] （待办，有 Python 环境）`python .harness/audit_harness.py` 原生运行通过

---

**状态流转：** Proposed（agent 写完）→ Accepted（用户真实环境验证后拍板）→ Deprecated

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
universal-ai-harness 一键注入脚本

将通用 AI 治理框架（.claude + .harness 单一命名空间）注入任意目标项目，
并根据 --profile 生成符合规范的初始 CLAUDE.md（含 {{INTAKE_PENDING}} 初始化横幅）与 .harness/progress.md。

用法：
    # 多模块项目（含跨模块协同：coordinator + architect-reviewer + contracts + cross-module-change）
    python harness_installer.py --target /path/to/my_project --profile multi

    # 单模块项目（模块自治：仅三角色，不含 coordinator/architect-reviewer + cross-module-change）
    python harness_installer.py --target /path/to/my_project --profile single

    # 指定项目名（默认取 target 目录名）
    python harness_installer.py --target /path/to/my_project --profile single --name my_project

--profile: single | multi
"""
import argparse
import datetime
import shutil
import sys
from pathlib import Path

PLACEHOLDER = "{{PROJECT_NAME}}"

# 治理框架自身根目录（本脚本所在目录）
HARNESS_ROOT = Path(__file__).resolve().parent

# 各 profile 注入的 agent 角色
AGENTS = {
    "single": ("designer", "reviewer", "builder"),
    "multi": ("coordinator", "architect-reviewer", "designer", "reviewer", "builder"),
}

# 各 profile 注入的 skills（cross-module-change 仅多模块需要）
SKILLS = {
    "single": ("contract-writing", "harness-setup"),
    "multi": ("contract-writing", "cross-module-change", "harness-setup"),
}

PROFILE_LABEL = {"single": "单模块", "multi": "多模块"}


def copy_agents(target: Path, profile: str):
    """注入 .claude/agents/ 指定角色。"""
    src = HARNESS_ROOT / ".claude" / "agents"
    dst = target / ".claude" / "agents"
    dst.mkdir(parents=True, exist_ok=True)
    for role in AGENTS[profile]:
        s = src / f"{role}.md"
        if s.exists():
            shutil.copy2(str(s), str(dst / f"{role}.md"))


def copy_skills(target: Path, profile: str):
    """注入 .claude/skills/ 指定技能。"""
    src = HARNESS_ROOT / ".claude" / "skills"
    dst = target / ".claude" / "skills"
    for skill in SKILLS[profile]:
        s = src / skill
        if s.is_dir():
            shutil.copytree(str(s), str(dst / skill), dirs_exist_ok=True)


def copy_commands(target: Path):
    """注入 .claude/commands/ 快捷指令（bootstrap / cycle 等）。"""
    src = HARNESS_ROOT / ".claude" / "commands"
    dst = target / ".claude" / "commands"
    if src.is_dir():
        shutil.copytree(str(src), str(dst), dirs_exist_ok=True)


def copy_contracts(target: Path):
    """注入 .harness/contracts/（跨模块契约体系）。"""
    src = HARNESS_ROOT / ".harness" / "contracts"
    shutil.copytree(str(src), str(target / ".harness" / "contracts"), dirs_exist_ok=True)


def copy_docs(target: Path):
    """注入 .harness/docs/（core-beliefs + ARCHITECTURE + standards + experience-library + _project 模板）。"""
    src = HARNESS_ROOT / ".harness" / "docs"
    shutil.copytree(str(src), str(target / ".harness" / "docs"), dirs_exist_ok=True)


def copy_audit_script(target: Path):
    """注入 .harness/audit_harness.py（不触碰目标项目自有 tools/ 等目录）。"""
    src = HARNESS_ROOT / ".harness" / "audit_harness.py"
    dst = target / ".harness"
    dst.mkdir(parents=True, exist_ok=True)
    shutil.copy2(str(src), str(dst / "audit_harness.py"))


def write_claude_md(target: Path, name: str, profile: str):
    """按 profile 生成目标根级 CLAUDE.md。"""
    if profile == "multi":
        text = MULTI_CLAUDE_TEMPLATE
    else:
        text = SINGLE_CLAUDE_TEMPLATE
    text = text.replace(PLACEHOLDER, name)
    (target / "CLAUDE.md").write_text(text, encoding="utf-8")


def write_progress(target: Path, name: str, profile: str):
    """生成目标 .harness/progress.md。"""
    src = HARNESS_ROOT / ".harness" / "progress.md"
    text = src.read_text(encoding="utf-8")
    today = datetime.date.today().isoformat()
    text = (
        text.replace(PLACEHOLDER, name)
        .replace("YYYY-MM-DD", today)
        .replace("__PROFILE__", PROFILE_LABEL[profile])
    )
    dst = target / ".harness"
    dst.mkdir(parents=True, exist_ok=True)
    (dst / "progress.md").write_text(text, encoding="utf-8")


# 占位符替换的文本后缀清单（须与 .harness/audit_harness.py 的检查清单保持同步）
TEXT_SUFFIXES = (".md", ".py", ".pro", ".c", ".h", ".cpp", ".hpp", ".yml", ".yaml", ".rs", ".js", ".ts", ".go", ".java")


def replace_placeholders(root: Path, name: str):
    """递归替换已注入模板中的 {{PROJECT_NAME}}。"""
    # 工具脚本自身定义 PLACEHOLDER 常量，属功能必需，须排除
    tool_scripts = {"harness_installer.py", "audit_harness.py"}
    count = 0
    for p in root.rglob("*"):
        if not p.is_file() or p.suffix not in TEXT_SUFFIXES:
            continue
        if p.name in tool_scripts:
            continue
        try:
            text = p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        if PLACEHOLDER in text:
            p.write_text(text.replace(PLACEHOLDER, name), encoding="utf-8")
            count += 1
    return count


def run(args):
    target = Path(args.target).resolve()
    if not target.exists():
        print(f"错误：目标目录 {target} 不存在。请先创建项目目录。")
        return 1

    name = args.name or target.name
    profile = args.profile

    print(f"[注入] universal-ai-harness → {target}")
    print(f"[profile] {PROFILE_LABEL[profile]}（{profile}）")

    copy_agents(target, profile)
    copy_skills(target, profile)
    copy_commands(target)
    copy_contracts(target)
    copy_docs(target)
    copy_audit_script(target)
    write_claude_md(target, name, profile)
    write_progress(target, name, profile)
    n = replace_placeholders(target, name)
    print(f"[替换] 占位符 {PLACEHOLDER} → {name}（{n} 个文件）")

    print("\n" + "=" * 60)
    print("注入完成。下一步：")
    print("=" * 60)
    print(f"1. 进入项目：cd {target}")
    print(f"2. 执行 /project-intake 采集项目画像（生成 .harness/docs/PROJECT.md，")
    print(f"   改写 CLAUDE.md 概述/目录结构段并消除初始化横幅）")
    print(f"3. 改写 .harness/docs/ARCHITECTURE.md 分层/数据流/模块映射")
    if profile == "multi":
        print(f"4. 用 harness-setup 流程落地各模块")
    else:
        print(f"4. 确认 commit 分支策略并回填 CLAUDE.md")
    print(f"5. 自检：python .harness/audit_harness.py")
    print("=" * 60)
    return 0


# ─────────────────────────────────────────────────────────────
# CLAUDE.md 模板（注入时替换 {{PROJECT_NAME}}）
# ─────────────────────────────────────────────────────────────

MULTI_CLAUDE_TEMPLATE = """# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

> ⚠️ **初始化未完成** {{INTAKE_PENDING}} — 项目画像未采集。
> **立即执行 `/project-intake`**：生成 `.harness/docs/PROJECT.md` 并改写本文件概述/目录结构段，横幅随之消除。

## 项目概述

{{PROJECT_NAME}} — 基于 universal-ai-harness 治理框架生成的多模块集成项目。

> 本段为占位描述；项目真实定位/技术栈/运行方式由 `/project-intake` 采集至 `.harness/docs/PROJECT.md`。

本仓库当前为**多模块集成形态**：根级统筹协调，各模块自治开发。跨模块通过契约档案（`.harness/contracts/`）对齐接口，模块内按各自 CLAUDE.md 自治。

## 模块概览

| 模块 | 目录 | 性质 | 技术栈 | 详情入口 |
|------|------|------|--------|----------|
| （待 `/project-intake` 采集 / 模块孵化后更新） | | | | |

## 目录结构

```
{{PROJECT_NAME}}/
├── CLAUDE.md                  ← 本文件（agent 入口路由）
├── .claude/                   ← 根级角色（coordinator + architect-reviewer）+ skills
└── .harness/                  ← 治理框架单一命名空间（卸载即删此目录）
    ├── contracts/             ← 跨模块契约档案（L1 发布点）
    ├── docs/                  ← 知识库 + PROJECT.md 项目画像
    ├── progress.md            ← 根级运行时进度
    └── audit_harness.py       ← 索引自检脚本
```

> 项目自身源码目录（src/ 等）的结构导读由 `/project-intake` 采集后补充。

## 跨模块协同

**L0-L3 评级**（联系强度，详见 `.harness/docs/core-beliefs.md`）：L0 独立实现 → L1 契约发布到 `.harness/contracts/` → L2 根 agent 轻度协调 → L3 根 agent 全程主导。**能 L0 不 L1，能 L1 不 L2。**

**跨模块流程**：需求涉及 2+ 模块时，遵循 `.harness/contracts/workflows/cross-module-change.md`（定契约 → 派发子 agent → 各自治实现 → 架构审核 → 收尾归档）。

## Skill 路由表

| 场景 | 触发条件 | 走什么流程 |
|------|----------|-----------|
| 项目画像采集 | CLAUDE.md 存在初始化横幅 | `project-intake` skill |
| L0 单模块 | 需求只涉及单个模块内部 | 模块内 Designer → Reviewer → Builder 流程 |
| L1/L2/L3 跨模块 | 需求涉及 2+ 模块 | `cross-module-change` skill |
| 新模块落地 | 新模块源码进入项目 | `harness-setup` skill |
| 契约编写 | 编写跨模块契约档案 | `contract-writing` skill |
| 收尾自检 | 任何收尾归档前 | `python .harness/audit_harness.py` |

## 编译命令速查

> 待 `/project-intake` 采集后登记（agent 可否执行编译验证一并标注）。

## 关键约定

> 待 `/project-intake` 采集后登记跨模块通信介质（消息总线 / 队列 / API 等）。

## 档案纪律

**四级体系**（随 L0-L3 评级加权，详见 `.harness/docs/core-beliefs.md`）：根级 `.harness/contracts/` 发布跨模块契约（L1），各模块 `.harness/docs/design-docs/` 记录内部决策；档案要求随评级加重（L0 仅模块 ADR → L2/L3 契约+派发+审核+收尾）。格式：精简 ADR（Context / Decision / Consequences），命名 `NNN_<kebab-case>.md`。触发：架构调整 / 跨模块修改 / 接口变更。流程：先写 md 再动代码。

## 入口文档

| 文档 | 路径 | 说明 |
|------|------|------|
| 项目画像 | `.harness/docs/PROJECT.md` | 项目是什么/怎么跑/硬约束（intake 产物） |
| 核心信念 | `.harness/docs/core-beliefs.md` | L0-L3 评级 + 档案纪律 + 协作规则 |
| 架构总览 | `.harness/docs/ARCHITECTURE.md` | 模块边界 + 通信协议（需项目化更新） |
| 标准规范 | `.harness/docs/standards/` | Harness 模板 + Mock 规范 + 自检规范 |
| 经验库 | `.harness/docs/experience-library/` | 教训沉淀 |
| 契约索引 | `.harness/contracts/index.md` | 跨模块契约档案列表 |
| 工作流 | `.harness/contracts/workflows/cross-module-change.md` | L0-L3 评级分段协同流程 |
| 自检工具 | `.harness/audit_harness.py` | 索引/编号/体量核对 |

## Commit 策略

> TODO(项目定制)：登记分支策略。模板默认建议：受保护分支（agent 不代提交）+ 日常分支（允许代提交），由用户在初始化时确认。
"""

SINGLE_CLAUDE_TEMPLATE = """# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

> ⚠️ **初始化未完成** {{INTAKE_PENDING}} — 项目画像未采集。
> **立即执行 `/project-intake`**：生成 `.harness/docs/PROJECT.md` 并改写本文件概述/目录结构段，横幅随之消除。

## 项目概述

{{PROJECT_NAME}} — 基于 universal-ai-harness 治理框架生成的单模块项目。

> 本段为占位描述；项目真实定位/技术栈/运行方式由 `/project-intake` 采集至 `.harness/docs/PROJECT.md`。

本仓库当前为**单模块自治形态**：模块内按 Designer → Reviewer → Builder 流程自治开发，无跨模块协同层。

## 目录结构

```
{{PROJECT_NAME}}/
├── CLAUDE.md                  ← 本文件（agent 入口路由）
├── .claude/                   ← 角色（designer + reviewer + builder）+ skills
└── .harness/                  ← 治理框架单一命名空间（卸载即删此目录）
    ├── contracts/             ← 契约档案（5 章节规范体系）
    ├── docs/                  ← 知识库 + PROJECT.md 项目画像
    ├── progress.md            ← 运行时进度
    └── audit_harness.py       ← 索引自检脚本
```

> 项目自身源码目录（src/ 等）的结构导读由 `/project-intake` 采集后补充。

## 工作流

新增需求 → 模块内 Designer → Reviewer → Builder 流程（详见 `.harness/docs/core-beliefs.md`）：

1. **Designer** 设计架构，写 `.harness/docs/design-docs/NNN_*.md` 草稿
2. **Reviewer** 审核设计（需求 + 架构 + 格式）
3. 用户确认设计
4. **Builder** 按 Scope 实现 + 编译验证（无法编译标 `[未验证]`）
5. **Reviewer** 审核架构（决策符合度 + core-beliefs）
6. 用户真实环境测试 → 状态转 Accepted

## Skill 路由表

| 场景 | 触发条件 | 走什么流程 |
|------|----------|-----------|
| 项目画像采集 | CLAUDE.md 存在初始化横幅 | `project-intake` skill |
| 单模块需求 | 需求只涉及模块内部 | Designer → Reviewer → Builder 流程 |
| 契约编写 | 记录模块内部决策/接口 | `contract-writing` skill |
| 收尾自检 | 任何收尾归档前 | `python .harness/audit_harness.py` |

## 编译命令速查

> 待 `/project-intake` 采集后登记（agent 可否执行编译验证一并标注）。

## 档案纪律

**档案体系**（详见 `.harness/docs/core-beliefs.md`）：模块 `.harness/docs/design-docs/` 记录内部决策。格式：精简 ADR（Context / Decision / Consequences），命名 `NNN_<kebab-case>.md`。触发：架构调整 / 接口变更。流程：先写 md 再动代码。

## 入口文档

| 文档 | 路径 | 说明 |
|------|------|------|
| 项目画像 | `.harness/docs/PROJECT.md` | 项目是什么/怎么跑/硬约束（intake 产物） |
| 核心信念 | `.harness/docs/core-beliefs.md` | 协作规则 + 档案纪律 |
| 架构总览 | `.harness/docs/ARCHITECTURE.md` | 分层 + 数据流（需项目化更新） |
| 标准规范 | `.harness/docs/standards/` | Harness 模板 + Mock 规范 + 自检规范 |
| 经验库 | `.harness/docs/experience-library/` | 教训沉淀 |
| 自检工具 | `.harness/audit_harness.py` | 索引/编号/体量核对 |

## Commit 策略

> TODO(项目定制)：登记分支策略。不确定时问用户，不要自作主张提交。
"""


def main():
    ap = argparse.ArgumentParser(description="universal-ai-harness 一键注入")
    ap.add_argument("--target", required=True, help="目标项目路径")
    ap.add_argument("--profile", choices=["single", "multi"], required=True, help="注入形态")
    ap.add_argument("--name", help="项目名（默认取 target 目录名）")
    args = ap.parse_args()
    return run(args)


if __name__ == "__main__":
    sys.exit(main())

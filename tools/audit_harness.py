#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Harness 索引自检脚本

用途：拦截索引与实体漂移（源工程真实翻车：CLAUDE.md 写"契约 001-004"实际已 007）。
接入点：跨模块工作流收尾必跑；单模块收尾建议跑。

用法：
    python tools/audit_harness.py               # 审计当前目录
    python tools/audit_harness.py --root PATH   # 审计指定项目根
    python tools/audit_harness.py --strict      # P1 也视为失败（CI 用）

退出码：0 = 全过；1 = 存在 P0；2 = 仅存在 P1/P2（非 strict 时）
"""
import argparse
import re
import sys
from pathlib import Path

PLACEHOLDER = "{{PROJECT_NAME}}"


def find_board_dirs(root: Path):
    """模块目录 = 同时含 docs/design-docs/ 与 .claude/agents/builder.md 的目录（根级不含这两者）。"""
    boards = []
    for builder in root.rglob(".claude/agents/builder.md"):
        # builder.md → agents/ → .claude/ → 模块根目录（三级 parent）
        d = builder.parent.parent.parent
        if (d / "docs" / "design-docs").is_dir():
            boards.append(d)
    return sorted(set(boards))


def check_contracts(root: Path):
    """契约索引 vs 实体；编号冲突。"""
    problems = []
    idx = root / "contracts" / "index.md"
    if not idx.exists():
        return problems  # 单模块裁剪后无 contracts/，跳过
    # 实体文件
    entities = {}
    for p in (root / "contracts").glob("*.md"):
        m = re.match(r"(\d{3})_", p.name)
        if m:
            n = int(m.group(1))
            entities.setdefault(n, []).append(p.name)
    # 编号冲突
    for n, names in entities.items():
        if len(names) > 1:
            problems.append(("P0", f"契约编号 {n:03d} 冲突：{names}"))
    # 索引中列出的编号。只认两种合法登记形式，避免把说明文字（如"编号从 001 开始"）误判为已登记：
    #   a) 表格数据行：| 001 | 标题 | ...
    #   b) 文件名/链接引用：001_kebab-case.md
    index_nums = set()
    for line in idx.read_text(encoding="utf-8").splitlines():
        m = re.search(r"\|\s*(\d{3})\s*\|", line) or re.search(r"\b(\d{3})_[a-z0-9-]+", line)
        if m:
            index_nums.add(int(m.group(1)))
    # 实体有但索引无
    for n in entities:
        if n not in index_nums:
            problems.append(("P0", f"契约 {n:03d} 存在实体但 contracts/index.md 未登记"))
    # 索引有但实体无（允许 index 刚起空表，无数字时跳过）
    if index_nums:
        for n in index_nums:
            if n not in entities:
                problems.append(("P0", f"contracts/index.md 登记 {n:03d} 但实体文件缺失"))
    return problems


def check_design_docs(board: Path):
    """模块 ADR 索引 vs 实体；编号连续性。"""
    problems = []
    dd = board / "docs" / "design-docs"
    entities = {}
    for p in dd.glob("*.md"):
        if p.name.startswith("_"):
            continue
        m = re.match(r"(\d{3})_", p.name)
        if m:
            entities[int(m.group(1))] = p.name
    if not entities:
        return problems  # 空模块，正常
    idx = dd / "index.md"
    if not idx.exists():
        problems.append(("P1", f"{board.name}/docs/design-docs/index.md 缺失"))
    # 编号跳号
    nums = sorted(entities)
    for expect, actual in zip(range(1, len(nums) + 1), nums):
        if expect != actual:
            problems.append(("P2", f"{board.name} ADR 编号跳号：期望 {expect:03d} 实得 {actual:03d}"))
            break
    return problems


def check_claude_md(path: Path):
    problems = []
    if not path.exists():
        problems.append(("P1", f"{path} 缺失"))
        return problems
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    n_sections = len([l for l in lines if l.startswith("## ")])
    if not (60 <= len(lines) <= 120):
        problems.append(("P1", f"{path} 行数 {len(lines)} 超出 60~120 区间（可能退化成内容仓库）"))
    if not (4 <= n_sections <= 12):
        problems.append(("P1", f"{path} 段落数 {n_sections} 超出 4~12 区间"))
    return problems


def check_progress(path: Path):
    problems = []
    if not path.exists():
        problems.append(("P1", f"{path} 缺失"))
        return problems
    text = path.read_text(encoding="utf-8")
    if "下一 session" not in text and "交接班" not in text:
        problems.append(("P1", f"{path} 缺少'下一 session 交接班'段"))
    return problems


def check_agents(board: Path):
    problems = []
    for role in ("designer", "reviewer", "builder"):
        if not (board / ".claude" / "agents" / f"{role}.md").exists():
            problems.append(("P1", f"{board.name}/.claude/agents/{role}.md 缺失"))
    return problems


def check_placeholder(root: Path):
    problems = []
    # 工具脚本自身定义 PLACEHOLDER 常量，属功能必需，不视为残留
    tool_scripts = {"harness_installer.py", "audit_harness.py", "extract_kit.py", "init_project.py"}
    for p in root.rglob("*"):
        if not p.is_file() or p.suffix not in (".md", ".py", ".pro", ".c", ".h", ".cpp", ".yml", ".yaml", ".rs", ".js", ".ts", ".go", ".java"):
            continue
        if p.name in tool_scripts:
            continue
        try:
            if PLACEHOLDER in p.read_text(encoding="utf-8"):
                problems.append(("P2", f"{p.relative_to(root)} 残留占位符 {PLACEHOLDER}"))
        except (UnicodeDecodeError, OSError):
            pass
    return problems


def main():
    ap = argparse.ArgumentParser(description="Harness 索引自检")
    ap.add_argument("--root", type=Path, default=Path.cwd())
    ap.add_argument("--strict", action="store_true", help="P1 也视为失败")
    args = ap.parse_args()
    root = args.root.resolve()

    all_problems = []
    all_problems += check_contracts(root)
    boards = find_board_dirs(root)
    for b in boards:
        all_problems += check_design_docs(b)
        all_problems += check_agents(b)
        all_problems += check_progress(b / "harness" / "progress.md")
    all_problems += check_claude_md(root / "CLAUDE.md")
    all_problems += check_progress(root / "harness" / "progress.md")
    all_problems += check_placeholder(root)

    # 输出
    if not all_problems:
        print(f"[OK] Harness 自检通过。模块数：{len(boards)}")
        return 0

    levels = {"P0": 0, "P1": 1, "P2": 2}
    for lvl, msg in sorted(all_problems, key=lambda x: levels.get(x[0], 3)):
        print(f"  [{lvl}] {msg}")
    p0 = sum(1 for l, _ in all_problems if l == "P0")
    p1 = sum(1 for l, _ in all_problems if l == "P1")
    print(f"[FAIL] P0={p0} P1={p1} 共 {len(all_problems)} 项")
    if p0:
        return 1
    if args.strict and p1:
        return 1
    return 2 if p1 else 0


if __name__ == "__main__":
    sys.exit(main())

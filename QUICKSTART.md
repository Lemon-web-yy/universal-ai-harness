# QUICKSTART — 5 秒注入 Harness

## 场景一：纯 Python / Web / Rust / 任意单体项目

```bash
# 1. 注入（single 形态：模块自治，无跨模块协同层）
python harness_installer.py --target /path/to/my_app --profile single

# 2. 进入项目
cd /path/to/my_app

# 3. 自检（应显示 [OK] Harness 自检通过）
python .harness/audit_harness.py
```

注入后你得到：

- `.claude/agents/` — designer / reviewer / builder 三角色
- `.claude/skills/` — contract-writing + harness-setup + project-intake
- `.harness/contracts/` — 契约模板与索引
- `.harness/docs/` — core-beliefs + ARCHITECTURE + _project 画像模板 + standards + experience-library
- `.harness/progress.md` + `.harness/audit_harness.py`
- 根级 `CLAUDE.md`（单模块自治版，顶部带初始化横幅）

## 场景二：微服务 / 前后端分离 / 多模块项目

```bash
# 1. 注入（multi 形态：含 coordinator + architect-reviewer + cross-module-change）
python harness_installer.py --target /path/to/my_monorepo --profile multi

# 2. 进入项目
cd /path/to/my_monorepo

# 3. 自检
python .harness/audit_harness.py
```

multi 比 single 多出：

- 根级 `coordinator` + `architect-reviewer` 角色
- `cross-module-change` 技能（L0-L3 跨模块协同流程）
- 根级 CLAUDE.md 含模块概览表与跨模块路由

## 注入后必做的 3 件事

1. **执行 `/project-intake`** — agent 扫描 README / 目录 / 构建配置，生成 `.harness/docs/PROJECT.md` 项目画像，改写根级 CLAUDE.md 并消除初始化横幅（横幅残留 = audit P1，不采集完无法收尾）
2. **改写 .harness/docs/ARCHITECTURE.md** — 真实分层 + 数据流 + 模块映射
3. **落地模块**（multi）— 用 `harness-setup` skill 为每个模块生成独立 Harness

## 常见问题

**Q：注入会覆盖我的现有文件吗？**
A：治理文件全部收在 `.harness/` 单一命名空间，不碰你项目的 `docs/`、`tools/` 等自有目录（卸载 = 删 `.harness/` + `.claude/` + `CLAUDE.md`）。唯一例外：根级 `CLAUDE.md` 会被覆盖，已有请先备份。

**Q：single 和 multi 能互相切换吗？**
A：可以。用另一个 profile 重新注入即可（会补齐/覆盖对应角色与技能）。

**Q：支持什么语言？**
A：全部。治理机制与语言无关；`audit_harness.py` 已覆盖 `.py/.rs/.js/.ts/.go/.java/.c/.h/.cpp` 等常见扩展名的占位符检查。

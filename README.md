# universal-ai-harness — 通用 AI 治理框架库

> **一句话：** 一套与语言、技术栈无关的 AI 协作治理框架（Meta-Framework），5 秒注入任意新老项目。

本仓库从真实嵌入式工程逆向提炼并**彻底通用化**——剥离了串口/FIFO/STM32/Qt 等一切领域语义，只保留可复用的治理机制：

- **L0-L3 评级路由** — 按需求联系强度选择流程重量（能轻不重）
- **契约先行** — 跨模块变更先写 5 章节契约档案，再动代码
- **三角色分工** — Designer（设计）/ Reviewer（审核）/ Builder（实现）+ 根级 Coordinator / Architect-Reviewer
- **档案四级体系** — 精简 ADR（Context/Decision/Consequences）防决策蒸发
- **镜像参考模板** — 强制标注镜像源，防同类模块发散
- **索引自检** — 脚本机械拦截索引与实体漂移

## 适用场景

| 你的项目 | 用什么 profile |
|----------|---------------|
| 纯 Python 脚本 / Web 后端 / Rust CLI 等**单体**项目 | `single` |
| 微服务 / 多仓库 / 前后端分离 / 多模块协同项目 | `multi` |

**不限于任何语言**：Python、JavaScript/TypeScript、Go、Rust、Java、C/C++、C#… 治理机制与语言无关。

## 目录结构

```
universal-ai-harness/
├── harness_installer.py        # 一键注入脚本
├── README.md                   # 本文件
├── QUICKSTART.md               # 5 秒上手
├── .claude/
│   ├── agents/                 # 五角色：coordinator / architect-reviewer / designer / reviewer / builder
│   └── skills/                 # 三技能：contract-writing / cross-module-change / harness-setup
├── contracts/                  # 跨模块契约体系（5 章节模板 + 索引 + 工作流）
├── docs/                       # core-beliefs + ARCHITECTURE + standards + experience-library
├── harness/progress.md         # 运行时进度模板
└── tools/audit_harness.py      # 索引自检工具
```

## 快速开始

```bash
# 注入到你的项目（以 multi 为例）
python harness_installer.py --target /path/to/your_project --profile multi

# 进入项目跑自检
cd /path/to/your_project
python tools/audit_harness.py
```

详见 [QUICKSTART.md](QUICKSTART.md)。

## 核心概念速览

### L0-L3 评级

| 评级 | 联系强度 | 流程 |
|------|---------|------|
| L0 | 单模块独立 | 模块内自治，不跨流程 |
| L1 | 契约同步 | 只发契约，不派发子 agent |
| L2 | 协调开发 | 契约 + 并行派发 + 架构审核 + 收尾 |
| L3 | 统一编排 | 全程主导的完整流程 |

### 契约 5 章节

1. **接口契约** — 边界、消息格式、数据流、异常场景
2. **责任划分** — 各端职责、公开 API、改动清单
3. **不做的事** — 明确边界（每条带理由）
4. **镜像参考模板** — 标注镜像源（强制/建议）
5. **验证清单** — 编译 / 集成 / 真实环境三层

### 三角色

| 角色 | 职责 | 不做 |
|------|------|------|
| Designer | 架构设计，写 ADR 草稿 | 编程、审核 |
| Reviewer | 审核设计与代码 | 设计、编程 |
| Builder | 按 Scope 编程实现 | 设计、审核 |

## 与 embedded-code-kits 的关系

本仓库是**治理层**，与代码无关。需要嵌入式 C/C++ 代码骨架时，配合 [../embedded-code-kits](../embedded-code-kits) 使用——两者平级解耦，各司其职。

## License

（由使用者自行添加）

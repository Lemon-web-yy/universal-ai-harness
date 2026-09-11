---
name: contract-writing
description: "Writes the contract archive for cross-module changes. Use this whenever a cross-module change needs a contract documented before coding — creates the 5-section archive (interface contract / responsibility split / out-of-scope / mirror template reference / verification checklist), confirms the NNN number from the contract index, and sets status to Proposed. Even if the user just says 'write the contract for X' or 'document the cross-module agreement' without mentioning the 5-section format, use this skill to ensure the standard structure is followed."
---

# Contract-Writing Workflow（契约档案编写）

编排跨模块契约档案编写流程，用于跨模块需求定契约阶段。工作流确保契约档案在编码前落档，5 章节结构齐全，编号无冲突。

## When to Use

**触发条件** — 需要编写契约档案时：

- 跨模块需求定契约阶段
- 用户说"写契约" / "定契约" / "document the cross-module agreement"
- 跨模块变更流程的定契约步骤

常见触发语："给这个跨模块需求写契约"、"定契约档案"、"加个新契约条目"——只要是跨模块契约编写。

**不触发**（走其他流程）：
- 单模块内部需求 → 走模块内 Designer → Reviewer → Builder 流程
- 新模块 harness 落地 → 走 harness-setup skill
- 纯代码修改（无契约变更）→ 直接做
- 用户明确说跳过契约

**判断方法：** agent 读取项目 CLAUDE.md 了解契约档案目录 + 5 章节规范。如果需求是"为跨模块变更编写契约档案"，就是本 skill 场景。

## 契约档案 5 章节结构

契约档案必须包含 5 个章节：

| 章节 | 写什么 | 防止什么 |
|------|--------|----------|
| **1. 接口契约** | 跨模块边界全部写清：通道/接口/数据结构、消息格式、调用约定、数据流方向、边界条件、异常场景 | 接口歧义（各端理解不一致） |
| **2. 责任划分** | 各端各自的职责、公开 API、改动文件清单、构建脚本改动 | 职责重叠或遗漏 |
| **3. 不做的事** | 明确划定边界（如"不做重试 / 不做业务推断 / 不做持久化"） | 子 agent 自由发挥 |
| **4. 镜像参考模板** | 标注本需求镜像哪个已有模块套路（强制/建议两级，含差异点） | 发散模式 |
| **5. 验证清单** | 编译验证 / 集成验证 / 真实环境验证三层次，每项可勾选 | 验证遗漏 |

**5 章节缺一不可。** 完整格式参考 `.harness/contracts/_template.md`。

## 编写流程（6 步）

### Step 1: 确认编号

读契约索引 `.harness/contracts/index.md`，取当前最大编号 +1 作为新契约编号。

- 编号格式：三位数字递增（NNN）
- 文件名：`NNN_<kebab-case-english-name>.md`

### Step 2: 写 Context（背景）

写 Context 段落：需求来源 / 痛点 / 已对齐的需求边界（用户已确认不可推翻）/ 相关 ADR 与教训引用。

### Step 3: 写 Decision 5 章节

按 `.harness/contracts/_template.md` 的 5 章节结构写 Decision 段：

#### 3.1 接口契约 — 消息/接口定义逐字段表 + 全组合速查 + 示例 + 容量/性能预算
#### 3.2 责任划分 — 各端新增/修改文件清单 + 公开 API + 关键约束
#### 3.3 不做的事 — 每条带理由，不是附录
#### 3.4 镜像参考模板 — 镜像源路径 + 镜像内容 + 差异点（强制/建议两级）
#### 3.5 验证清单 — 编译/集成/真实环境三层勾选

### Step 4: 写 Consequences（后果）

正向（打通了什么）+ 负向/待办（已知技术债归属哪个未来 ADR）+ 验证清单重复（带勾选状态）。

### Step 5: 更新契约索引

在 `.harness/contracts/index.md` 追加新条目（编号 + 标题 + 日期 + 一句话摘要）。

### Step 6: 状态 Proposed

契约档案状态字段设为 `Proposed`。

- **Proposed** — agent 写完后的初始状态
- **Accepted** — 用户真实环境测试后的确认状态（用户拍板，agent 不能自作主张翻）
- **Deprecated** — 已废弃

## Key Discipline

### 1. 先读格式参考再动手

编写契约前必须先读 `.harness/contracts/_template.md`（5 章节标准格式）。它包含全部细节结构，是单一真相源。

**为什么：** skill 是流程编排器，不重复模板内容。跳过格式参考直接动手会漏章节或格式不一致。

### 2. 5 章节必备

5 章节缺一不可。**"不做的事"防止子 agent 自由发挥，"镜像参考模板"防止发散模式。**

### 3. 镜像参考模板必须显式标注

契约必须显式标注镜像路径，禁止自由发挥——发散的模式难以维护。

### 4. 编号取当前最大 +1

读契约索引确认当前最大编号，取 +1。防止编号冲突。

### 5. 状态 Proposed → Accepted 由用户拍板

agent 只写 Proposed，不能自作主张翻 Accepted。

### 6. 子 agent prompt 不重复契约全文

后续派发时 prompt 只给路径，要求子 agent 自行 Read 完整契约。

**为什么：** 契约是单一真相源，粘贴会引入版本不一致风险。

## Reference Files

| 读取什么 | 从哪读 |
|----------|--------|
| 契约格式参考 | `.harness/contracts/_template.md` |
| 契约索引路径 | `.harness/contracts/index.md` |
| 跨模块流程与教训 | `.harness/contracts/workflows/cross-module-change.md` |
| 项目 commit 策略 | 根级 CLAUDE.md |

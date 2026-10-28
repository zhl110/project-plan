# USAGE.md — project-plan-z 使用适配指南（可选阅读）

> **本文件是可选说明文档，不强制加载，不会进 SKILL.md 常驻上下文。**
>
> 与 `README.md` 的区别：
> - `README.md` 讲「skill 内部流程与结构」——它是什么、怎么走（路由、三模式、红线、循环）。
> - **本文件讲「不同 agent / 不同工作区配置下，怎么用它才真正好用」**——落地坑在哪、各 agent 差异是什么、怎么让生成的档案真的被遵守。
>
> 只读 README 也能用本 skill；读这本解决的是「我建了 AGENTS.md 为什么没生效」「换一个 agent 用法一样吗」这类实际问题。

---

## 0. 一句话前提

**规则写在哪 ≠ agent 会读哪。**

本 skill 能生成 `AGENTS.md` / `PRD.md` / `PLAN.md` / `progress.md`，但它**不能强制任何 agent 自动去读这些文件**。文件会不会被读，取决于 agent / 平台的行为，不在本 skill 控制范围内。

所以本 skill 的价值分两半：
1. 生成一套好档案（创建 / 补录 / 跟踪）；
2. 让档案**真的被用上**——这后半截是本文件要解决的重点。

---

## 1. agent 怎么读到档案：只有两条路

没有任何 agent 会"自动扫描"项目目录里的 `AGENTS.md` / `PRD` / `PLAN` / `progress`。读取只有两条途径：

1. **平台自动注入某一层的 `AGENTS.md`**（见第 2 节各 agent 差异）。
2. **skill 被调用，其指令驱动 agent 去读**（本 skill 的跟踪 / 补录模式就是这么设计的：先读 AGENTS → PLAN → progress）。

推论：如果你直接开聊、没触发本 skill，子项目的 `AGENTS.md` 对 agent 是**隐形**的——规则不会被遵守，三件套也不会被续上。因此「所有项目任务都以本 skill 开场」是一种纪律性兜底（见第 3 节）。

---

## 2. 不同 agent / 平台的差异（关键）

### 2.1 WorkBuddy

- 只自动读取**当前 workspace folder（工作区文件夹）** 那一层级的 `AGENTS.md`，注入为 `project_guidance`。
- 子文件夹里的 `AGENTS.md` **不自动读**。
- 因此：
  - 若工作区 = 整个仓库（如 `D:\mycode`），则只有根 `AGENTS.md` 自动生效，**所有子项目 `AGENTS.md` 都不自动读**。本 skill 在子项目里建的 `AGENTS.md` 对你"隐形"，除非你：
    - **(a)** 把 WorkBuddy 的 workspace folder **指向具体子项目**（如 `D:\mycode\your-project`），该子项目 `AGENTS.md` 即自动生效；或
    - **(b)** 在根 `AGENTS.md` 里加一行指针：「进入 `xxx` 子项目时读 `xxx/AGENTS.md` + `xxx/.plan/`」；或
    - **(c)** 任务都以本 skill 开场，靠 skill 指令驱动读取。
  - ⚠️ 在仓库内用 `cd` 进子目录**改不了** workspace folder，注入层不变——只有改配置的工作区才变。

### 2.2 Claude Code / 类 IDE agent

- 通常以 **cwd 所在项目根** 的 `AGENTS.md` 作为项目上下文（在索引 / 上下文中）。把工作目录设为项目根，`AGENTS.md` 即生效。
- 与 WorkBuddy 不同：这类 agent 跟随 cwd，切到子项目就自然读子项目的 `AGENTS.md`。

### 2.3 通用结论

- 真正「每次会话都必守」的硬规则，应沉淀进**自动注入层**（记忆系统 / 工作区根 `AGENTS.md`），不要只放在子项目文件里。
- 项目特有的连续性（`PRD` / `PLAN` / `progress`）放在子项目文件，靠本 skill 跟踪模式维护。

---

## 3. 怎么用才真正好用（最佳实践）

### 3.1 选对工作区

- **单项目深度工作**：直接把 host 的 workspace folder 指向该项目，让 `AGENTS.md` 自动生效。
- **整仓库多项目**：在根 `AGENTS.md` 挂「子项目档案指针」，或约定所有项目任务以本 skill 开场。

### 3.2 分层放置规则

- **全局硬规则**（跨项目都该守）：进记忆层或根 `AGENTS.md`（自动注入）。
- **项目规则 + 连续性**：进子项目 `AGENTS.md` + `.plan/`（靠 skill 驱动读）。

### 3.3 让循环真正转起来

- 任务都以本 skill 开场 → 跟踪模式读断点 → 每动作追加 `progress` → 阶段切换即更新 `PLAN`。
- 收工前用哨兵复核「进度是否连续无空窗」，别让三件套停在建档那一刻。

### 3.4 补录模式的正确打开

- 半路项目来补档案：先 `scaffold.py` 非破坏补骨架 → 侦察兵盘点证据 → `L1/L2/L3` 分级反写 → 哨兵核验。
- 别让 agent 凭空编历史：推不出的标「待确认」。

### 3.5 配合 WorkBuddy 的实操建议

- 如果你平时用「整个 `D:\mycode` 一个工作区」：本 skill 生成的子项目 `AGENTS.md` **不会自动生效**，请走 2.1 的 (b) 或 (c) 兜底。
- 如果你「每个项目单独开工作区」：本 skill 建的 `AGENTS.md` 会被自动读，无需额外处理——此时 SKILL.md 可在「何时用」里写明「建议把工作区指向本项目以让 `AGENTS.md` 自动生效」。

---

## 4. 常见误区

- ❌ 「我建了 `AGENTS.md` 它就会自动生效」——只在它是 workspace-folder 那一层时才成立。
- ❌ 「子项目有 `AGENTS.md` 就够了」——WorkBuddy 不读子文件夹，除非工作区指向它。
- ❌ 「skill 会替我保证 agent 读文件」——skill 只能驱动，不能强制；平台行为才是关键。
- ❌ 「`cd` 进子项目就能让规则生效」——改不了注入用的 workspace folder。

---

## 5. 与本 skill 其他文档的关系

| 文档 | 角色 | 是否强制加载 |
|------|------|------|
| `README.md` | 结构 / 流程 / 红线（了解 skill 本身） | 按需（路由索引可指） |
| `references/*.md` | 按需加载的详细规则（建档 / 循环 / 门禁等） | 按需 |
| **`USAGE.md`（本文件）** | 跨 agent 适配与使用诀窍 | **可选，不强制加载** |

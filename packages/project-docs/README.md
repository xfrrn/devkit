# 项目文档基线 (Project Docs)

> devkit · `packages/project-docs` · 状态：✅ 可用
>
> 用一套克制、固定、可持续维护的文档结构，完成新项目初始化、既有项目补档和关键决策记录。

---

## 定位

这不是要求每个项目写大量文档的“文档工程”。默认只创建项目总纲、需求和系统设计，其余模板按项目需要选用，并明确区分：

- **计划**：`07-roadmap.md`
- **实际进展**：`09-progress-log.md`
- **关键决策及原因**：`decisions/ADR-*.md`
- **当前产品与技术事实**：其余主题文档

本包同时提供：

1. 可直接复制的 `docs/` 模板；
2. 符合开放 Agent Skills 结构的 `SKILL.md`；
3. 一个零依赖的 Python 初始化脚本。

## 适用场景

适合：

- 开发前从一句项目想法开始，经过访谈形成可执行文档；
- 开发中补齐、更新和审计文档，并同步计划、进度和关键决策；
- 让 Claude Code、Codex 或其他支持 Agent Skills 的开发 Agent 按同一方法创建和维护文档；
- 个人开发、小团队、早期创业项目；
- 需要在多个项目间复用相同文档规范。

不适合：

- 只需要一次性写一页说明的小实验；
- 强监管行业中已经有法定文档体系的项目；
- 用模板代替真实分析，批量生成空泛文档；
- 把所有实现细节提前设计完，再开始验证需求。

---

## 目录

```text
project-docs/
├── README.md
├── SKILL.md
├── assets/
│   └── docs/
│       ├── 00-project-brief.md
│       ├── 01-requirements.md
│       ├── 02-system-design.md
│       ├── 03-domain-model.md
│       ├── 04-api-contract.md
│       ├── 05-data-design.md
│       ├── 06-security-and-compliance.md
│       ├── 07-roadmap.md
│       ├── 08-testing-strategy.md
│       ├── 09-progress-log.md
│       └── decisions/
│           └── ADR-000-template.md
├── references/
│   ├── initialization-interview.md
│   ├── development-maintenance.md
│   ├── document-map.md
│   └── quality-checklist.md
└── scripts/
    └── init_project_docs.py
```

完整模板集如下；默认初始化只创建前三份：

```text
docs/
├── 00-project-brief.md
├── 01-requirements.md
├── 02-system-design.md
├── 03-domain-model.md
├── 04-api-contract.md
├── 05-data-design.md
├── 06-security-and-compliance.md
├── 07-roadmap.md
├── 08-testing-strategy.md
├── 09-progress-log.md
└── decisions/
    └── ADR-000-template.md
```

---

## 各文档回答什么

| 文档 | 只负责回答 |
|---|---|
| `00-project-brief.md` | 为什么做、给谁用、做什么、不做什么、怎样算成功 |
| `01-requirements.md` | 用户要完成什么、系统必须具备什么行为和质量 |
| `02-system-design.md` | 系统怎样组织、模块怎样协作、技术方案怎样落地 |
| `03-domain-model.md` | 核心业务对象、术语、关系、状态与业务规则是什么 |
| `04-api-contract.md` | 系统边界之间如何通过稳定契约交换数据 |
| `05-data-design.md` | 数据如何持久化、约束、索引、迁移、缓存和清理 |
| `06-security-and-compliance.md` | 权限、敏感数据、安全边界、依赖和合规要求是什么 |
| `07-roadmap.md` | 未来准备按照什么阶段推进 |
| `08-testing-strategy.md` | 如何证明需求、接口、数据和系统行为是正确的 |
| `09-progress-log.md` | 实际做到哪里、发生了什么、下一步是什么 |
| `decisions/ADR-*.md` | 为什么作出某个重要且难以逆转的技术决策 |

更详细的事实来源和依赖关系见 `references/document-map.md`。

---

## 核心原则

### 1. 克制优于堆砌

十份文档是可选上限，不是每个项目的基线。没有对应内容就不创建；缺少少量关键信息时写 `[待确认]`，不要用泛泛而谈的文字填满页面。

### 2. 先业务，后设计

正确顺序是：

```text
目标与范围
  → 场景与需求
  → 领域对象
  → 系统设计
  → API 与数据
  → 安全、测试和路线图
```

编号是阅读顺序，不代表必须机械地按文件编号完成全部内容。

### 3. 单一事实来源

同一事实只在一个文档中详细定义，其他文档只引用：

- 功能事实以 `01-requirements.md` 为准；
- 业务对象以 `03-domain-model.md` 为准；
- API 以 OpenAPI 或 `04-api-contract.md` 为准；
- 数据库实际结构以 migration/schema 为准；
- 关键决策原因以 ADR 为准；
- 实际进展以 `09-progress-log.md` 为准。

### 4. 不编造信息

从仓库、用户说明和已有文档中找不到依据的内容必须标注为：

```text
[假设]
[待确认]
[暂定]
```

### 5. 计划、事实、历史分开

- Roadmap 可以修改，因为计划会变化；
- Progress Log 以追加为主，保留真实历史；
- 已接受 ADR 不直接重写，通过新 ADR 取代旧决策。

---

## 使用方式一：运行初始化脚本

在 `devkit` 仓库根目录运行：

```bash
python packages/project-docs/scripts/init_project_docs.py \
  --target ../my-project \
  --name "My Project" \
  --owner "Your Name" \
  --summary "一句话描述项目"
```

Windows PowerShell：

```powershell
python packages/project-docs/scripts/init_project_docs.py `
  --target ..\my-project `
  --name "My Project" `
  --owner "Your Name" `
  --summary "一句话描述项目"
```

默认行为：

- 在目标项目中创建 `docs/` 和三份核心文档；
- 替换项目名称、负责人、日期和一句话描述；
- 不覆盖已有文件；
- 使用 `--force` 才覆盖同名文件；
- 使用 `--dry-run` 只预览将执行的操作。

明确需要完整模板集时增加 `--all`：

```bash
python packages/project-docs/scripts/init_project_docs.py --target ../my-project --all
```

`--docs-dir` 必须指向目标项目内部，不能通过绝对路径或 `..` 写到项目之外。

---

## 使用方式二：作为 Agent Skill

本目录本身就是一个 Skill。复制时必须保持目录名为 `project-docs`，因为开放规范要求目录名与 `SKILL.md` 中的 `name` 一致。

### Claude Code：项目级 Skill

```bash
mkdir -p .claude/skills/project-docs
cp -R /path/to/devkit/packages/project-docs/* .claude/skills/project-docs/
```

然后可显式调用：

```text
/project-docs 初始化当前项目的文档基线
```

### Codex：项目级 Skill

```bash
mkdir -p .agents/skills/project-docs
cp -R /path/to/devkit/packages/project-docs/* .agents/skills/project-docs/
```

然后在 Codex 中通过 Skills 选择器或 `$project-docs` 调用。

### 不复制 Skill

也可以让 Agent 直接读取：

```text
请读取 /path/to/devkit/packages/project-docs/SKILL.md，按其中流程初始化当前项目文档。
```

---

## 推荐工作流

本 Skill 有两个主要入口：

| 项目阶段 | Skill 行为 |
|---|---|
| 尚未开始开发 | 主动访谈，形成开发前文档基线 |
| 正在开发 | 读取文档和代码证据，只维护本次变化影响的内容 |

### 新项目

```text
1. 用户简单说明项目想法并调用 Skill
2. Skill 提取已有信息，集中询问阻塞问题
3. 先确认目标、用户、MVP、非目标和核心流程
4. 生成 Brief 和 Requirements
5. 按项目实际情况增加 Domain、System、API、Data、Security、Testing 和 Roadmap
6. 通过开发就绪检查后再开始实现
7. 开发开始后记录 Progress，重要取舍使用 ADR
```

最简调用示例：

```text
$project-docs 我想做一个帮助家庭管理食品保质期的应用，请引导我完成开发前文档。
```

用户不需要预先准备完整需求；Initialize 模式会读取 `references/initialization-interview.md` 主动完成需求访谈。

### 正在开发的项目

```text
1. 读取本次变更相关的文档、diff、代码、测试和配置
2. 区分 Planned、In Progress、Implemented 和 Diverged
3. 根据变更影响只更新相关文档
4. 需求变化先更新 Requirements，再检查下游设计
5. 完成项需要实现和验证证据
6. 同步 Roadmap、Progress Log，重要取舍使用 ADR
7. 保留并报告无法判断的文档—实现冲突
```

---

## 维护规则

- 每次需求范围变化：更新 Brief、Requirements，必要时更新 Roadmap。
- 每次领域对象或业务规则变化：更新 Domain Model，并检查 API/Data。
- 每次公开接口变化：先更新 OpenAPI/Contract，再更新实现。
- 每次数据库结构变化：通过 migration 落地，再同步 Data Design。
- 每次安全边界变化：更新 Security，并补测试。
- 每个重要开发节点：追加 Progress Log。
- 每个重大技术取舍：新增 ADR。

---

## 反模式

| 不要这样做 | 应该改成 |
|---|---|
| 一次生成十份充满套话的长文档 | 只写有证据的内容，未知项明确标记 |
| 在 README、PRD、API 文档重复维护同一字段 | 指定一个事实来源，其余引用 |
| 先设计数据库，再思考业务对象 | 先领域模型，再数据设计 |
| Roadmap 与 Progress Log 混在一起 | 一个记录未来，一个记录真实历史 |
| 把每个普通实现选择都写成 ADR | 只记录重要、跨模块、难逆转的决策 |
| 已接受 ADR 被直接修改成新结论 | 新建 ADR，并标记旧 ADR 被取代 |
| 项目结构文档只有目录树 | 同时写清职责、边界和依赖方向 |
| 文档写完后永久不更新 | 将更新动作绑定到需求、接口、迁移和发布流程 |

---

## 加入 devkit 根级索引

在根级 `README.md` 的 Package 索引中增加：

```markdown
| `project-docs` | ✅ 可用 | 新项目文档基线、模板与 Agent Skill | `packages/project-docs/README.md` |
```

在目录结构中增加：

```text
│   ├── project-docs/              ← 项目文档基线、模板与 Agent Skill
```

> 原则：文档不是开发前的一次性仪式，而是项目当前事实、计划、历史和决策的最小可维护载体。

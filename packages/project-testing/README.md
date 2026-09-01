# 项目测试工作流 (Project Testing)

> devkit · `packages/project-testing` · 状态：✅ 可用
>
> 让开发 Agent 根据改动类型、风险和项目技术栈，自动选择并执行最小但足够的测试。

---

## 定位

这不是新的测试框架，也不要求所有项目使用同一种目录或命令。它提供一个可直接复制的 Agent Skill，用来解决四件事：

1. 识别这次改动实际影响了什么；
2. 从单元、集成、契约、功能、回归、冒烟、E2E 等测试中选择必要组合；
3. 适配目标项目已有语言、包管理器、测试框架和 CI 命令；
4. 如实处理失败、零测试、flaky、环境阻塞和未执行范围。

核心原则：

> **先运行能直接证明改动的最小测试，再按照边界和风险扩大回归范围。**

```text
代码改动
  → 识别行为与调用方
  → 判断边界和风险
  → 选择测试类型
  → 映射现有项目命令
  → 定向测试 → 受影响套件 → 必要时全量回归
```

---

## 测试维度

测试名称不是一张互斥清单：

| 维度 | 类型 |
|---|---|
| 测试层级 | Unit、Component、Integration、Contract、E2E |
| 测试目的 | Functional、Acceptance、Regression、Smoke |
| 质量属性 | Performance、Security、Reliability、Compatibility、Accessibility、Visual |

一个 API 集成测试可以同时是功能测试、验收测试和回归测试。Skill 不会为了凑齐名称重复创建三套测试。

---

## 默认适配

| 改动 | 默认验证 |
|---|---|
| 普通业务逻辑 | 定向单元/功能测试 + 邻近回归 |
| Bug 修复 | 复现根因的回归测试 + 受影响套件 |
| 重构 | 既有回归测试；仅在真实缺口处补测试 |
| API、事件或 Schema | 行为测试 + 契约 + 相关集成 |
| 数据库或 migration | 隔离环境中的 migration/集成测试 + 数据不变量 |
| 外部服务 | 客户端行为、超时/错误映射、契约；已有 sandbox 才访问真实环境 |
| UI 交互 | Component/Functional；跨边界关键流程才增加 E2E |
| UI 视觉 | 渲染检查或已有视觉回归，不能用单元测试代替视觉验收 |
| 配置、依赖、启动 | Build/Typecheck + Smoke |
| 权限、金额、并发、破坏性数据 | 定向测试 + 集成 + 更广回归 |

更完整的变化矩阵见 `references/test-selection.md`；多语言和 monorepo 命令选择见 `references/stack-adapters.md`。

---

## 包结构

```text
packages/project-testing/
├── README.md
├── SKILL.md
└── references/
    ├── test-selection.md
    └── stack-adapters.md
```

首版没有通用测试脚本：目标仓库已有命令才是事实来源，额外脚本只会重复或误判项目配置。

---

## 使用方式

目录名必须保持为 `project-testing`，与 `SKILL.md` 中的 `name` 一致。

### Codex：项目级 Skill

```bash
mkdir -p .agents/skills/project-testing
cp -R /path/to/devkit/packages/project-testing/* .agents/skills/project-testing/
```

`SKILL.md` 的 description 覆盖代码实现、修改和 Bug 修复，因此允许 Codex 在匹配开发任务时隐式调用；也可以显式使用 `$project-testing`。

为了把“完成前必须验证”变成项目固定约定，可以在目标项目根目录 `AGENTS.md` 增加：

```markdown
- 完成代码修改前使用 project-testing 工作流运行最相关的测试；零测试、未运行、失败或环境阻塞必须明确报告。
```

### Claude Code：项目级 Skill

```bash
mkdir -p .claude/skills/project-testing
cp -R /path/to/devkit/packages/project-testing/* .claude/skills/project-testing/
```

### 不复制 Skill

```text
请读取 /path/to/devkit/packages/project-testing/SKILL.md，按其中流程验证当前改动。
```

---

## 典型调用

### 开发完成前验证

```text
$project-testing 根据当前 diff 选择最小但足够的测试，运行后报告覆盖范围和未运行项。
```

### Bug 回归

```text
$project-testing 为这个分页末页重复数据问题补一个复现根因的回归测试，并运行受影响套件。
```

### 接口变化

```text
$project-testing 验证这次 API response schema 修改，适配项目现有测试栈并覆盖消费者契约。
```

### 只审计

```text
$project-testing 审计当前项目测试缺口和测试命令，不修改代码。
```

---

## 边界

Skill 默认不会：

- 为统一风格替换项目已有测试框架；
- 为小改动机械运行所有昂贵套件；
- 把 lint、typecheck 或 build 冒充行为测试；
- 访问生产、共享账号、付费 API 或破坏性数据库；
- 反复重跑 flaky 测试直到偶然变绿；
- 为覆盖率数字编写无意义断言；
- 在普通功能测试中顺带展开完整性能或安全审计。

当真实项目多次出现无法可靠发现命令的情况，再考虑增加确定性检测脚本；首版保持说明型 Skill。

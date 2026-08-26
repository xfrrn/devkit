# devkit

> 我的个人开发套件：沉淀跨项目可复用的设计规范、工程实践与方法论。
> 每个项目都能从这里 clone / 拷贝需要的一块，直接落地。

---

## 这是什么

不是组件库、不是框架，而是一套**「可以直接抄走用」的工程资产**。
按领域分包，每个 package 自包含：**规范文档（README）+ 可拷贝的代码骨架**。

复用方式统一为 **clone 后拷贝文件**——无构建、无版本、无安装，最轻。

## 结构

```
devkit/
├── README.md                     ← 你在这里（套件总览 / 索引 / 复用方式）
├── packages/
│   ├── design-system/            ← UI 设计规范（按风格分类）
│   │   ├── README.md             ←   风格索引
│   │   └── quiet-native/         ←   静谧原生设计规范（通用 Web/PWA）
│   │       ├── README.md         ←     设计规范（15 节）
│   │       ├── tokens.css        ←     语义 Token（浅/深）
│   │       ├── tailwind.config.ts ←    Tailwind 骨架
│   │       └── globals.css       ←     全局 base + 工具类
│   └── project-docs/             ← 项目文档模板与 Agent Skill
├── tests/
│   └── design-system/
│       └── quiet-native/
│           └── README.md         ← 测试内容、提示词与运行配置
└── docs/
    └── principles.md             ← 跨领域的通用工程原则
```

## Package 索引

| Package | 状态 | 一句话 | 入口 |
|---|---|---|---|
| `design-system` | ✅ 可用 | 按风格分类的 UI 设计规范 | `packages/design-system/README.md` |
| `project-docs` | ✅ 可用 | 按需创建和维护项目文档 | `packages/project-docs/README.md` |

## 怎么用（三步）

1. **clone** 本仓库到本地。
2. 找到需要的 package，读它的 `README.md`（规范 + 落地步骤）。
3. **拷贝**该 package 里的代码骨架进你的项目，按其 README 调整。

以设计系统为例：
```
packages/design-system/quiet-native/ 的 tokens.css + globals.css + tailwind.config.ts
  → 拷进新项目 → 入口按 tokens.css 再 globals.css 引入 → 改品牌色即可
```

## 新增一个 package 的约定

每个新领域都遵循同一形态：

1. 在 `packages/` 下建目录：`packages/<name>/`
2. 必有一个 `README.md`：写**规范 / 原则 / 反模式 / 落地步骤**。
3. 代码骨架直接平铺在该目录，拷走即用。
4. 在本文件的「Package 索引」表格里登记一行。

`design-system` 按风格再分一层：`packages/design-system/<style>/`，每套风格自包含 `README.md` 与代码骨架。

> 原则：**规范优先于代码**。代码骨架是规范的可执行示例，文档才是本体。

## 演进

- 现在：**纯文件拷贝**——最轻、零成本。
- 当某个 package 被多个项目高频复用、需要版本锁定时，再单独把它升级成可安装依赖包（加 `package.json` 导出，或拆成独立 repo）。套件其余部分不受影响。

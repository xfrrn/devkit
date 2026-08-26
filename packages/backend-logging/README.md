# 通用项目日志系统 (Backend Logging)

> devkit · `packages/backend-logging` · 状态：✅ 可用
>
> 让开发 Agent 在不同语言项目中实现同一套日志原则：**终端有明确颜色、列对齐且美观，生产 JSON 稳定可查**。

---

## 定位

本包不是某个日志库的二次封装，也不要求所有项目使用同一种依赖。它提供：

1. 一个可直接交给 Claude Code、Codex 等开发 Agent 的 `SKILL.md`；
2. 跨语言的日志事件与 Pretty Terminal 视觉契约；
3. 常见语言生态的适配选择；
4. 固定终端主题、彩色预览脚本、JSON Schema 与零依赖 NDJSON 校验脚本。

核心原则只有一句：

> **调用方只记录一次结构化事件，Pretty Terminal 与 JSON 只是两个渲染器。**

```text
业务代码
   ↓
结构化事件 + 关联上下文
   ↓
规范化 / 脱敏 / 错误序列化
   ↓
Pretty Terminal      NDJSON
```

因此不会出现开发环境写一套“彩色字符串日志”，生产环境又维护另一套 JSON 字段的情况。

---

## 输出目标

### Pretty Terminal

```text
13:42:18.604  INFO   http.access           Request completed               method=GET route=/v1/posts/:id status=200 duration=38.4ms request_id=req_01K3N7VZ7HY5TQH6E4K4X8NFKG
13:42:20.087  WARN   db.query              Slow query                      operation=list_posts duration=842.7ms rows=24
13:42:21.311  ERROR  publisher.x           Publish failed                  account_id=acc_7 attempt=2
              ╰─ TimeoutError: upstream timed out after 10s
                 at publisher/client.ts:184
                 at worker/run.ts:72
```

设计要求：

- 交互式 TTY 默认开启颜色，`DEBUG/INFO/WARN/ERROR/FATAL` 使用固定语义色；
- 时间 12、level 5、scope 20、message 30 个终端显示单元格，列间固定两个空格；
- ANSI 转义序列不计入宽度，中文和其他宽字符按终端显示宽度对齐；
- logger/scope 使用统一强调色，不随机给组件分配颜色；
- message 简短，动态值放结构化字段；
- context 顺序稳定，普通事件保持一个物理行；
- 错误类型醒目、堆栈弱化并缩进展示；
- 只给结构和少量语义值上色，不给整行染色；
- 不使用 Emoji、Logo、方框、彩虹对象和随机字段顺序；
- `NO_COLOR`、`TERM=dumb`、非 TTY 或重定向时不残留 ANSI，去色后布局不变。

参考配色见 `assets/terminal-theme.json`。可以直接运行：

```bash
python packages/backend-logging/scripts/preview_terminal_theme.py --force-color
```

完整规则见 `references/terminal-style.md`。

### NDJSON

实际生产输出为一行一个 JSON 对象：

```json
{"ts":"2026-08-26T05:42:18.604Z","level":"info","msg":"Request completed","event":"http.request.completed","service":"api","env":"production","version":"1.8.0","logger":"http.access","request_id":"req_01K3N7VZ7HY5TQH6E4K4X8NFKG","trace_id":"4bf92f3577b34da6a3ce929d0e0e4736","span_id":"00f067aa0ba902b7","ctx":{"method":"GET","route":"/v1/posts/:id","status":200,"duration_ms":38.4}}
```

最低字段：

```text
ts       UTC RFC 3339 时间
level    小写级别
msg      面向人的简短说明
```

重要事件增加稳定的 `event` 名；高频关联字段使用 `request_id`、`trace_id`、`span_id`；事件特有值放入 `ctx`；失败详情放入 `error`。

JSON 必须：

- UTF-8；
- 一事件一物理行；
- 紧凑、不缩进；
- 保留 number、boolean、array、object 等原生类型；
- 不包含 ANSI；
- 不把 `ctx` 或 `error` 再序列化成字符串。

完整字段契约见 `references/logging-contract.md`。

---

## 包结构

```text
packages/backend-logging/
├── README.md
├── SKILL.md
├── assets/
│   ├── log-event.schema.json
│   └── terminal-theme.json
├── references/
│   ├── logging-contract.md
│   ├── terminal-style.md
│   ├── language-adapters.md
│   └── quality-checklist.md
└── scripts/
    ├── check_json_logs.py
    └── preview_terminal_theme.py
```

| 文件 | 职责 |
|---|---|
| `SKILL.md` | Agent 的执行流程、边界和验收标准 |
| `logging-contract.md` | 字段、级别、事件、错误、上下文、脱敏和边界事件 |
| `terminal-style.md` | Pretty Terminal 的列、色彩、值格式与错误展示 |
| `language-adapters.md` | 不同语言的优先实现路径与注意事项 |
| `quality-checklist.md` | 完成前审计清单 |
| `log-event.schema.json` | 可复制的语言无关 JSON Schema |
| `terminal-theme.json` | Pretty Terminal 固定列宽、语义颜色与视觉禁用项 |
| `check_json_logs.py` | 零第三方依赖的 NDJSON 校验器 |
| `preview_terminal_theme.py` | 零依赖彩色终端预览与中英文对齐参考实现 |

---

## 支持范围

Skill 根据目标仓库的真实依赖选择实现，不按语言写死。

| 生态 | 推荐起点 |
|---|---|
| Node.js / TypeScript | Pino；已有 Winston 等成熟 logger 时优先扩展现有方案 |
| Python | structlog + stdlib logging，或统一现有 logging formatter |
| Go | `log/slog` + Pretty Handler |
| Rust | `tracing` + `tracing-subscriber` |
| Java / Kotlin | SLF4J + Logback/项目既有 provider |
| .NET | `ILogger<T>`；已有 Serilog/NLog 时继续使用 |
| PHP | Monolog |
| 其他语言 | 原生结构化 logger + 一个小型 formatter/adapter |

适用于服务、API、worker、scheduler、CLI 和桌面/local runtime。浏览器前端日志默认不在范围内，除非任务明确要求。

---

## 默认配置语义

具体变量名可以遵循项目已有习惯，但应提供等价能力：

```text
LOG_LEVEL=debug|info|warn|error
LOG_FORMAT=auto|pretty|json
LOG_COLOR=auto|always|never
LOG_PRETTY_MODE=auto|full|compact|minimal
```

`auto` 的默认行为：

```text
交互式 TTY + 非 production/staging → Pretty
非 TTY 或 production/staging       → JSON
NO_COLOR                            → 保留列宽和排版，关闭 ANSI
```

格式只在 logger bootstrap 中选择一次，业务代码不判断环境。

---

## 使用方式

目录名必须保持为 `backend-logging`，与 `SKILL.md` 中的 `name` 一致。

### Claude Code：项目级 Skill

```bash
mkdir -p .claude/skills/backend-logging
cp -R /path/to/devkit/packages/backend-logging/* .claude/skills/backend-logging/
```

调用：

```text
/backend-logging 为当前项目实现漂亮终端日志和生产 NDJSON 日志
```

### Codex：项目级 Skill

```bash
mkdir -p .agents/skills/backend-logging
cp -R /path/to/devkit/packages/backend-logging/* .agents/skills/backend-logging/
```

然后通过 Skills 选择器或 `$backend-logging` 调用。

### 不复制 Skill

```text
请读取 /path/to/devkit/packages/backend-logging/SKILL.md，按其中流程升级当前项目日志系统。
```

---

## 典型调用

### 新项目

```text
$backend-logging 为当前 Go API 实现日志系统。本地使用漂亮单行终端日志，生产输出 NDJSON；接入 HTTP request_id，保留已有 OpenTelemetry trace_id/span_id，并替换本次范围内的 fmt.Printf。
```

### 已有项目升级

```text
$backend-logging 升级当前 Node.js 项目的 Pino 配置。不要替换 Pino。重点解决终端对象多行展开、生产 level 为数字、错误堆栈丢失、access log 重复和 token 脱敏。
```

### 只审计

```text
$backend-logging 审计当前项目，不改代码。检查 Pretty、JSON、上下文传播、重复错误、敏感信息和关键路径覆盖，并按优先级报告问题。
```

### 单独扩展 worker

```text
$backend-logging 为发布 worker 增加 completed、retry_exhausted、failed 事件，包含 task_id、account_id、attempt 和 duration_ms。不要把每个内部步骤都记录为 INFO。
```

---

## 校验 JSON 日志

文件输入：

```bash
python packages/backend-logging/scripts/check_json_logs.py app.ndjson
```

标准输入：

```bash
cat app.ndjson | python packages/backend-logging/scripts/check_json_logs.py -
```

要求所有记录带稳定 `event`：

```bash
python packages/backend-logging/scripts/check_json_logs.py app.ndjson --require-event
```

成功输出：

```text
OK: 128 JSON log event(s) validated
```

校验器检查一行一对象、必需字段、UTC 时间、level、event、`ctx`/`error` 类型、trace/span ID、ANSI 和顶层 null。

---

## 必须避免的反模式

| 不要这样做 | 应该改成 |
|---|---|
| 开发调用 `logPretty()`，生产调用 `logJson()` | 记录一次结构化事件，由 bootstrap 选择 renderer |
| `"publish failed for " + accountId` | `msg="Publish failed"`，动态值放结构化字段 |
| 每层 catch 都打印完整堆栈 | 最终拥有 retry/response/fail 结果的边界记录一次 |
| 每个函数、循环项和成功 SQL 都记录 INFO | 记录生命周期、终态、失败、降级和慢操作 |
| 终端无颜色或列宽漂移 | level 使用固定语义色，按 ANSI 感知的 Unicode 显示宽度对齐 |
| 终端用大量 Emoji、边框和对象展开 | 使用稳定列、固定主题和单行摘要 |
| JSON 中混入颜色或多行 pretty object | 一物理行一个紧凑 JSON object |
| 在每个调用点手动删除 token | 在 logger pipeline 中集中脱敏 |
| 为了日志字段完整临时制造 tracing | tracing 已存在才关联 trace/span；否则使用 request/operation ID |
| 容器服务自行滚动日志文件 | 输出进程流，由运行环境收集和保留 |

---

## 为什么不附七套固定代码骨架

不同语言和框架的 logger API、middleware、异步上下文与配置体系差异很大，固定样例会迅速过时，也容易诱导 Agent 无视目标项目已有方案。

因此本包采用：

```text
稳定契约 + Skill 工作流 + 固定终端主题 + 语言适配指南 + Schema + 通用校验器
```

规范保持稳定，具体实现由 Agent 基于目标仓库生成。已有成熟 logger 时优先扩展，而不是为了统一名字扩大改动。

---

## 维护原则

- 字段语义保持向后兼容；
- 修改稳定 `event` 名视为查询契约变化；
- Pretty 可以演进视觉，但不能改变事件语义；
- JSON 始终保持 NDJSON、无 ANSI、可逐行解析；
- 新增语言只扩展 `language-adapters.md`，不复制整套 Skill；
- 遵循根级 `docs/principles.md`：克制、语义化、约定优于配置、可观测、规范优先于代码。
